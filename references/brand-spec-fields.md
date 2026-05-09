# Brand spec fields · reference

> Companion doc for `assets/team-brand-spec.example.json`.
>
> Each field below explains **what** the field is, **why** it exists, and **what value to put in**. The skill reads `<project-root>/team-brand-spec.json` (not the `.example.json` template) at runtime. See also `references/security-config.md §4` and `references/figma-brand-spec-import.md`.

---

## Top-level layout

```
team           — who owns the spec
brand          — name, voice, hard "no" rules
watermark      — opt-in attribution on animation exports
logo           — primary / inverse / wordmark / icon paths
colors         — single source of truth for design tokens
typography     — font stacks
product_assets — physical-product hero / detail / scene
ui_screenshots — digital-product home / feature pages
design_system  — links to tokens repo + Figma library
approved_asset_hosts — internal hosts the agent may fetch from
current_project      — narrows scope for this run
```

---

## `team`

| Field | What | Why |
|---|---|---|
| `company` | Legal or display company name | Used in deliverables instead of "Acme Studios" placeholder |
| `division` | Division / studio name (e.g. "Game / Web3 product") | Disambiguates when a holding company runs multiple studios |
| `primary_contact_role` | Role that owns this spec (e.g. "Design Platform") | The agent quotes the role, not a person — survives staff changes |
| `design_repo_url` | URL of the design system repo | Read-only reference for the agent; not auto-cloned |

---

## `brand`

| Field | What | Why |
|---|---|---|
| `name` | Brand name as it appears on output | Distinct from `team.company` if the company runs multiple brands |
| `tagline_short` | One-line product tagline (≤8 words) | Used directly in hero sections |
| `tone_keywords` | Array of 3–5 voice descriptors | Guides copy + visual mood. Examples: `["confident","playful","technical"]` |
| `forbidden_zones` | Array of hard "no" rules | Prevents the agent from defaulting to common-but-wrong patterns. Examples: "No purple gradients", "No emoji icons in product UI" |

`forbidden_zones` is enforced at generation time. If the agent proposes a violation, it must visibly call out the conflict and pause for confirmation.

---

## `watermark`

**Default `enabled: false` — keep it that way until the team explicitly approves a watermark.**

| Field | What | Why |
|---|---|---|
| `enabled` | Boolean, defaults to `false` | Upstream `huashu-design` auto-injected "Created by Huashu-Design"; this fork removes that and gates anything on this flag |
| `text` | Watermark text when enabled | Replaces upstream's hard-coded self-attribution |
| `exclude_for_third_party_brand_work` | Boolean | When working under another studio's brand (client work), force watermark off regardless of `enabled` |

---

## `logo`

| Field | What | Why |
|---|---|---|
| `primary` | Path to primary logo SVG | Default for light backgrounds |
| `primary_inverse` | Path to white / inverted logo SVG | Used on dark backgrounds — required for contrast |
| `wordmark` | Path to text-only mark | Used when icon would be too small |
| `icon` | Path to symbol-only mark | Used in tight spaces (favicons, app icons) |
| `minimum_size_px` | Smallest allowed render | Prevents the agent from generating sub-legibility marks |
| `clear_space_rule` | Plain-language clear-space rule | The agent honours this when laying out hero sections |
| `forbidden_distortions` | Array of "do not" rules | Examples: "no stretch", "no recolor", "no outline added" |

All logo paths must point to files inside the project repo (`assets/<brand>-brand/...`). External URLs are not auto-fetched; the allowlist in `references/security-config.md §1` applies.

---

## `colors`

Single source of truth for design tokens. The agent reads these instead of inventing palette values.

| Field | What |
|---|---|
| `primary` | Brand primary, used for top-of-page emphasis |
| `background` | Default canvas |
| `ink` | Body text |
| `accent` | Interaction / link / call-to-action |
| `muted` | Secondary text and disabled states |
| `hairline` | Borders, dividers |
| `forbidden` | Array of colors / gradients the agent must not use |

Hex strings preferred. The agent maps these to CSS custom properties (`--color-primary`, etc.) when generating.

---

## `typography`

Font-stack strings, copied verbatim into generated CSS.

| Field | What | Default if blank |
|---|---|---|
| `display` | Headings / hero text | Inter (skill default) — replace to escape AI-default look |
| `body` | Body copy | Inter — replace with brand body face |
| `mono` | Code / numerical | JetBrains Mono (skill default) |

---

## `product_assets` (physical products only)

| Field | What |
|---|---|
| `hero_image` | Front-facing product shot |
| `detail_images` | Array of close-up detail shots |
| `scene_image` | Product in environment |

Leave blank for digital products — use `ui_screenshots` instead.

---

## `ui_screenshots` (digital products only)

| Field | What |
|---|---|
| `home` | Home / landing screenshot |
| `feature_pages` | Object: `{ feature_name: path }` per major feature page |

Used as visual context when the agent generates marketing pages, decks, or animations referring to the product.

---

## `design_system`

| Field | What |
|---|---|
| `tokens_repo_url` | URL of the design tokens repo (read-only reference) |
| `figma_library_url` | Figma library URL — used by `references/figma-brand-spec-import.md` |
| `spacing_scale` | Array of px values for spacing tokens |
| `border_radius_scale` | Array of px values |
| `shadow_tokens` | Object: `{ name: css-shadow-string }` |

The agent uses `spacing_scale` and `border_radius_scale` to choose values consistent with the system rather than picking arbitrary numbers.

---

## `approved_asset_hosts`

| Field | What | Why |
|---|---|---|
| `hosts` | Array of host strings | Internal asset-host allowlist (e.g. `["cdn.example.com"]`) — adds to the public allowlist in `references/security-config.md §1` |

Mirror any addition here in `references/security-config.md §1.2` so reviewers see why the host is trusted.

---

## `current_project`

Optional. Narrows scope for the current run.

| Field | What |
|---|---|
| `name` | Project / codename |
| `brief_path` | Path to project brief markdown |
| `figma_url` | Project-specific Figma file URL |
| `deadline` | ISO date string |
| `target_platforms` | `["ios"]` / `["android"]` / `["ios","android"]` — answers the platform-routing question once |

Setting `target_platforms` removes the platform-confirmation prompt that `SKILL.md` Platform routing otherwise asks on every run.

---

## What goes in `_meta` and `_note`

The example file uses `_meta` (top-level) and `_note` (per-section) keys for inline guidance. They are ignored at runtime — feel free to keep, edit, or strip them.

---

## Validation

Before committing, validate JSON with:

```bash
python3 -c "import json; json.load(open('team-brand-spec.json')); print('OK')"
```

CI runs the same check on `assets/team-brand-spec.example.json`. If you add new top-level keys to your project's `team-brand-spec.json`, document them in this file and update the example template too.

---

## Related

- `assets/team-brand-spec.example.json` — the template to copy.
- `references/security-config.md §4` — how the skill loads the spec.
- `references/figma-brand-spec-import.md` — populating the spec from Figma.
- `QUICKSTART.md` Step 2 — designer-facing walkthrough.
