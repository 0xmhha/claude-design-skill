# Codex CLI design workflow — GPT-5.5 reasoning + gpt-image-2 generation

> Version: internal-fork v0.2.0 · Last updated 2026-05-09

This guide wires OpenAI's **Codex CLI** (with built-in `gpt-image-2`) into the
internal-design-skill so designers can ask one agent — Codex, powered by GPT-5.5 —
to reason about a design brief and generate brand-correct illustrations in one
hop, then have the result land in `assets/<brand>-brand/generated/` only after a
hard PROVENANCE + stego-resistant gate.

## What lives where

| Layer | Tool / file | Purpose |
|---|---|---|
| Reasoning + image gen | OpenAI **Codex CLI** v0.115+ (March 2026) | GPT-5.5 thinks about the prompt, calls `gpt-image-2` (April 2026, 2K, native reasoning, multi-language dense text) automatically when an image is needed |
| Drop zone | `~/.codex/generated_images/` (or `$CODEX_HOME/generated_images/`) | Codex writes PNGs here. We never trust this directory. |
| Confidentiality gate | `SKILL.md §0` step 1 + `references/security-config.md §1.5` | Internal codenames must not be sent to Codex. The script (`codex-image-import.py`) re-checks the prompt before any move. |
| Stego gate | `scripts/scan_assets.py` (re-used) | PNG chunk scan. WARN = exit 2, CRITICAL = exit 3. Hard-fail by default. |
| Importer | `scripts/codex-image-import.py` | Picks the latest PNG from the drop zone, runs the gate, atomic-moves into `assets/<brand>-brand/generated/`, appends PROVENANCE with prompt SHA-256, source SHA-256, output SHA-256, and Codex session id. |
| Audit | `assets/<brand>-brand/PROVENANCE.md` | Append-only ledger. Both successful imports and BLOCKED rejections land here so the audit trail captures attempts, not just outcomes. |

## When to use this guide

- The brand is approved (the user can name it externally) and Codex CLI is
  installed locally (`codex --version` works).
- The brief has been narrowed to a specific asset: one logo, one hero image, one
  illustration set. Codex is not the right tool for "design me a website".
- An external brand is in scope. Internal codename / NDA names follow the
  confidentiality gate before any Codex call.

If any of those is false, fall back to Wikimedia / Unsplash / Met / Pexels
(the existing allowlist in `references/security-config.md §1.1`).

## The 5-step workflow

### Step 1 · Confidentiality gate (mandatory, before any Codex call)

Treat the prompt the same way `WebSearch` is treated in SKILL.md §0:

> Is the term a publicly released external brand/product, or could it be an
> internal codename / unreleased team product / partner NDA name?

If the second, **stop**. Ask the user to either:
- replace the codename with a generic placeholder ("the new feature"),
- or choose a different fallback (Wikimedia / hand sketch).

`scripts/codex-image-import.py` will run the same regex check at import time and
exit 4 if the prompt slipped through, so this step is the human checkpoint, not
the only one.

### Step 2 · Pre-flight Codex install check

```bash
which codex || npm install -g @openai/codex
codex --version    # Must be v0.115 or later for gpt-image-2 access
```

If you've never used Codex on this machine: `codex login` (ChatGPT OAuth).
The skill never receives the API key — it lives in Codex's own config.

### Step 3 · Generate via Codex

Two equivalent invocations. Pick whichever fits your editor.

**Natural language (Codex picks the tool):**

```bash
codex exec "Generate a brand-correct hero image for DJI Pocket 4: \
  matte black handheld gimbal camera, charcoal background, \
  soft directional lighting from upper left, no text, no logo, \
  16:9 composition, photoreal but editorial — not catalog. \
  Save as PNG."
```

**Explicit `$imagegen` invocation (use when Codex hesitates):**

```bash
codex exec "$imagegen Generate a 1920x1080 PNG: matte black DJI Pocket 4, \
  charcoal background, editorial lighting, no text"
```

Codex prints a session id (look for `thread.started` in `--json` output).
Note it down — it goes into PROVENANCE so future audits can trace which
Codex run produced which asset.

The PNG lands in `~/.codex/generated_images/<session-id>/ig_<hash>.png`
(Codex CLI v0.130 layout — confirmed by live validation 2026-05-09).
**Do not** copy it into the fork manually. The next step does that
with the gates applied.

### Step 4 · Import with strip + hard-fail gate

```bash
python3 scripts/codex-image-import.py \
  --brand dji \
  --name pocket4-hero \
  --prompt "matte black DJI Pocket 4, charcoal background, editorial lighting, no text" \
  --codex-session 0193f9aa-...   # paste the id from step 3
```

The importer runs three stages in order:

1. **Confidentiality re-check** — refuses if the prompt matches a
   codename pattern that slipped past step 1.
2. **PNG chunk strip** — removes any chunk whose tag is not in
   `scan_assets.PNG_WHITELIST` (the same allowlist the scanner uses,
   so the strip and the scan stay in sync). gpt-image-2 routinely
   embeds a `caBX` C2PA / JUMBF block (~25 KB of upstream provenance
   metadata); this is dropped. Trailing bytes after `IEND` are also
   dropped because the strip stops emitting at `IEND`. Both are
   recorded in PROVENANCE so the audit trail is honest about what
   was removed.
3. **Re-scan** — runs `scan_assets.py` on the stripped output. Only
   threats that survive the strip (truncation, missing signature,
   oversized text inside a whitelisted chunk) reach this stage.

Outcomes:

| Original PNG state | After strip + scan | Importer action | Exit |
|---|---|---|---|
| Codename in prompt | (strip not reached) | Block, no PROVENANCE entry, source untouched | `4` |
| Plain clean PNG (no extra chunks) | clean | Move + PROVENANCE (no Stripped chunks line) | `0` |
| gpt-image-2 with `caBX` C2PA chunk | clean after strip | Move + PROVENANCE records `Stripped chunks: caBX(N B)` and `AI provenance:` line | `0` |
| Trailing bytes after `IEND` | clean after strip | Move + PROVENANCE records `trailing-bytes(N B)` | `0` |
| Oversized `tEXt`/`iTXt` chunk in a whitelisted slot | WARN (exit 2) | **Block.** Source PNG kept. PROVENANCE records `BLOCKED` + the chunks that were stripped before the scan ran. | `2` |
| Missing PNG signature, truncated container | CRITICAL (exit 3) | **Block.** Same as WARN, just exit 3. | `3` |

When blocked, re-prompt Codex (or scrub the prompt) and try again. The
fork's asset directory never sees a flagged PNG.

### Step 5 · Use the imported asset

The PNG is now at `assets/<brand>-brand/generated/<name>.png` with a clean
PROVENANCE chain back to the prompt. Reference it from your HTML/JSX:

```jsx
<img src="../assets/dji-brand/generated/pocket4-hero.png" alt="..." />
```

If the asset is going into a deck or animation, run
`python3 scripts/scan_assets.py --dir assets/<brand>-brand/generated/`
again at deliverable time — defense in depth.

## Iterating on a generated image

Codex CLI keeps a session per `thread.started` id. To refine:

```bash
codex exec resume <session-id> "Same composition, but the gimbal arm \
  rotated 30 degrees clockwise. Keep lighting and background identical."
```

Each iteration writes a new PNG to `~/.codex/generated_images/`. Run the
importer again with a new `--name` (e.g. `pocket4-hero-v2`) so you keep
both versions and the PROVENANCE captures both prompts.

## What this workflow does NOT do

- **No silent retry on a blocked import.** The user always sees the rejection
  and decides whether to retry or change the prompt. Silent retry would defeat
  the audit point.
- **No automatic Figma sync.** That's `references/figma-image-export.md`'s job
  (Phase 6.3, optional). This guide stops at the file-on-disk milestone.
- **No image editing in place.** Codex CLI's `gpt-image-2` supports edit mode
  via the API (`v1/images/edits`), but exposing that here would let an attacker
  who slipped a prompt through one gate keep mutating an already-imported
  asset. Edits go through a fresh import + a new PROVENANCE entry.
- **No prompt-only retry through this script.** If `--brand` or `--name`
  are wrong, fix the CLI args and re-run; the importer is idempotent on
  source-PNG basis (it deletes the source after a successful move).

## Confidentiality gate — what's blocked

`scripts/codex-image-import.py` re-runs the gate at import time. Default
patterns (real list in `references/security-config.md §1.5`):

```
\bproject[-_ ]?[a-z]{4,}\b           # "project Falcon", "project_phoenix"
\b(internal|nda|confidential)[-_ ]…  # "internal-prototype", "nda assets"
```

Per-team additions: pass extra regex via the `--codename-pattern` flag once
that's wired (Phase 5). Until then, edit the constant in the script.

## Cross-references

- `references/security-config.md §1.5` — confidentiality patterns, deny/ask
  policy for `Bash(codex *)` and `Bash(python3 scripts/codex-image-import.py *)`
- `references/svg-sanitize.md` — sister gate for SVG inputs
- `scripts/codex-image-import.py` — the importer
- `scripts/test_codex_image_import.py` — 10 regression tests covering every gate
- `examples/dot-claude-settings.json` — harness permissions for codex
- `SKILL.md §0` step 1 — confidentiality gate (the upstream rule this hooks into)
