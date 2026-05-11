# Figma image-export · Codex PNG → Figma placement · reference

> The skill generates hero images, illustrations, and visual references via
> Codex CLI + gpt-image-2 (see `references/codex-design-workflow.md` +
> `scripts/codex-image-import.py`). Those PNGs land in
> `assets/<brand>/generated/` after the strip-then-scan gate. This doc
> covers the *next* step: getting them into Figma so designers can place
> them in real layouts.

---

## 1 · Two paths

| Path | When | How |
|---|---|---|
| **MCP-aware** | A Figma MCP server is attached and the user has write scope on the target file | Agent uploads the PNG via `figma_create_image` (or equivalent) and positions a rectangle / frame fill at the chosen page coordinates |
| **MCP-absent** | No Figma MCP attached, or Figma MCP read-only | Agent surfaces the PNG path + an *insertion instruction* (page name, target frame, drop position, suggested layer name) for the user to apply manually via Figma's `File → Place image…` or drag-drop |

Both paths share the same **provenance + naming + safety** rules below.

---

## 2 · Provenance — every imported PNG carries its lineage

The skill ships `assets/showcase-brand/PROVENANCE.md` as the canonical
format. When a new Codex-generated PNG is placed in Figma, the user (or
the agent in MCP-aware mode) records the same fields in the team's brand
PROVENANCE file:

| Field | Source |
|---|---|
| `source_generator` | `codex-cli` (with version, e.g. `0.130.0`) |
| `codex_session_id` | from the Codex output `session_id`, recorded by `scripts/codex-image-import.py` |
| `prompt` | the full prompt fed to Codex, verbatim |
| `prompt_sha256` | hash of the prompt string |
| `source_png_sha256` | hash of the file *before* the strip-then-scan gate |
| `output_png_sha256` | hash of the file *after* `caBX` (C2PA) chunk removal |
| `stripped_chunks` | what the gate removed (typically `caBX 23-26 KB`) |
| `post_strip_scan_result` | `PASS` (mandatory — see `scripts/scan_assets.py`) |
| `figma_file_key` | the Figma file the PNG was placed into |
| `figma_node_id` | the frame / page the PNG was placed inside (e.g. `1:42`) |
| `placed_at` | ISO-8601 UTC |

The fields up to `post_strip_scan_result` come for free from
`scripts/codex-image-import.py`. The last three (`figma_file_key`,
`figma_node_id`, `placed_at`) are appended at placement time.

---

## 3 · MCP-aware path (preferred)

Pre-conditions:

- Figma MCP server attached (see `references/figma-mcp-setup.md`).
- Token has *read + write* scope on the target file.
- The PNG has already passed `scripts/codex-image-import.py` (gate
  passed → file in `assets/<brand>/generated/`).

Workflow:

1. **Confirm the destination**. Agent reads the active selection
   (`figma_get_selection`) and asks:
   > "Place hero image (`assets/default-brand/generated/03-hero.png`,
   > 1920×1080, SHA `9f58…`) into *Page · Cover* → frame *Cover Hero*
   > at coords (0, 0) at native resolution?"
2. **Upload + insert**. Agent calls the MCP server:
   - `figma_create_image_fill` or equivalent — uploads the PNG bytes and
     gets back an image hash.
   - `figma_set_node_fill(node_id=<frame>, fill={"type":"IMAGE","imageRef":<hash>,"scaleMode":"FIT"})`
     — applies it as a frame fill, or
   - `figma_create_rectangle(parent_id=<page>, x=0, y=0, width=1920, height=1080)`
     + fill — creates a new rect with the image as its fill.
3. **Verify**. Agent re-reads the node (`figma_get_node`) and confirms
   `fills[0].imageRef` matches the upload hash.
4. **Record provenance**. Appends an entry to the team's PROVENANCE.md
   with `figma_file_key` + `figma_node_id` + `placed_at`.
5. **Report**. One-line summary back to the user with the Figma URL +
   the node id.

If any step fails, the rectangle / frame is left where the user can see
it but the fill is *not* applied — better visible "placeholder we
couldn't fill" than silent failure.

---

## 4 · MCP-absent path (fallback)

Pre-conditions:

- No Figma MCP attached or token is read-only.
- The PNG has passed `scripts/codex-image-import.py`.

Workflow:

1. **Surface the asset**. Agent reports the absolute path, dimensions,
   and SHA-256 of the imported PNG:
   ```
   assets/default-brand/generated/03-hero.png
   · 1920×1080 · SHA-256 9f58... · 412 KB
   · gate: PASS (caBX 25.2 KB stripped, scan_assets clean)
   ```
2. **Emit placement instructions**:
   ```
   In Figma:
   1. Open <FILE_NAME> (link if you have it)
   2. Navigate to Page · Cover
   3. Select frame "Cover Hero" (node id 1:42)
   4. File → Place image… → choose 03-hero.png
   5. Anchor at top-left (0, 0); use "Fill" scale mode
   6. Rename the new layer to "Hero image · Cover"
   ```
3. **Ask the user to confirm placement**. The agent doesn't know the
   placement landed until the user says so; the conversation continues
   only after that confirmation.
4. **Record provenance after confirmation**. Same PROVENANCE.md entry
   as the MCP-aware path; `figma_node_id` is filled in based on what the
   user reports (or left as the suggested target if the user didn't
   override).

---

## 5 · Naming convention for placed images

Default: `<role> · <where>` (matches the broader `references/figma-layer-naming.md` convention).

| Role | Example name |
|---|---|
| hero | `Hero image · Cover` |
| backdrop / surface | `Backdrop · Tokens page` |
| product shot | `Product · Wallet card` |
| illustration | `Illustration · Onboarding step 3` |

The MCP-aware path calls `figma_set_node_name` after `figma_create_*`.
The MCP-absent path includes the rename in the instruction list.

---

## 6 · Security posture (re-stated, since image-export touches all three)

- **Codename / NDA gate**: `scripts/codex-image-import.py` runs the
  codename regex check on the prompt *before* asking Codex to generate.
  An image whose source prompt mentioned a leaked codename never reaches
  this workflow — it's already been hard-rejected with exit code 4 at
  import time.
- **C2PA / metadata strip**: every Codex PNG arrives with a ~25 KB `caBX`
  chunk OpenAI signs. The strip-then-scan gate removes it; the *stripped*
  file is what Figma sees. The original signed file is recorded only by
  `source_png_sha256` in PROVENANCE for audit, never uploaded to Figma.
- **Asset host allowlist**: Figma stores the uploaded image on its CDN
  (`figma-alpha-api.s3.us-west-2.amazonaws.com` or similar). That host
  is **not** in the default `references/security-config.md §1.1`
  allowlist because the skill never *re-fetches* the image from there
  — once Figma has it, it stays on Figma's side. If a downstream
  workflow needs to pull the image back (e.g. for diff'ing), add the
  Figma S3 host to the *team-internal* allowlist
  (`§1.2 Team-extensible additions`).
- **Watermark**: if `team-brand-spec.json:watermark.enabled` is `true`,
  the watermark is composed into the PNG **before** Figma upload
  (so the watermark is part of the image bytes, not a separate Figma
  layer that can be deleted accidentally). When false (the default),
  no watermark is applied.

---

## 7 · Roadmap notes (not in this version)

| Capability | Why deferred |
|---|---|
| Automatic placement at frame insertion-point (e.g. inside an auto-layout container) | Figma auto-layout needs the parent's resize behaviour evaluated by Figma itself; emitting raw coordinates is correct for absolute layouts, brittle for auto-layout. Track-and-fix incrementally. |
| Variant generation (place 3 variants of the same prompt across 3 sibling frames) | Useful but doubles the surface area of MCP calls; build only after single-image placement is robust in production. |
| Image swap (replace existing image fill with a new Codex output) | Same flow as initial placement plus a node-search step (`figma_get_node` by name, then re-fill). Add when the team has a recurring "regenerate this hero" need. |
| Bulk import (multiple PNGs at once) | Same flow per file; agent loops with rate-limit awareness on the MCP server side. Add when batch ingestion is a real use case. |

---

## 8 · Related

- `references/codex-design-workflow.md` — Codex CLI + gpt-image-2
  generation workflow; this doc is the *post-generation* placement step.
- `scripts/codex-image-import.py` — the strip-then-scan gate that
  produces the PNGs this workflow places.
- `assets/showcase-brand/PROVENANCE.md` — canonical PROVENANCE format.
- `references/figma-mcp-setup.md` — how to attach the MCP server.
- `references/figma-selection-aware.md` — selection-confirmation
  pattern used by step 1 of the MCP-aware path.
- `references/figma-layer-naming.md` — naming convention reused by
  step 5 above.
- `references/security-config.md §1.5` — codename gate (re-stated
  in §6 above).
