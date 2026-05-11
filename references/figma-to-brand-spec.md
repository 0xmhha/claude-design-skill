# Figma → team-brand-spec extractor · reference

> Companion doc for `scripts/figma-to-brand-spec.py`.
>
> The extractor turns a Figma file's named styles into a JSON spec compatible
> with `assets/team-brand-spec.default.json`. The goal: adopter teams describe
> their brand once in Figma (the surface designers already work in) and let
> the skill pull values from there, instead of hand-editing JSON in two places.

---

## 1 · How extraction works

The tool calls Figma's REST API (`GET /v1/files/{file_key}`), walks the
document tree, and resolves each *named style* to its concrete value:

| Figma style type | Resolved value | Spec slot example |
|---|---|---|
| `FILL` solid | `#RRGGBB` (Figma 0-1 RGB rounded to 0-255 HEX) | `colors.accent.primary` |
| `TEXT` style | `{family, weight, size, line_height_px}` | `typography.display.family` |
| `EFFECT` (shadow) | (planned — currently passes through to `_unmapped`) | `design_system.shadow_tokens.subtle` |

The mapping from Figma style name → spec slot follows a slash convention:

```
color/accent/primary       → colors.accent.primary
color/surface/base_dark    → colors.surface.base_dark
color/status/success_light → colors.status.success_light
text/display/family        → typography.display.family
text/body/family           → typography.body.family
```

Recognised top-level prefixes (case-insensitive):

| Figma prefix | Spec base |
|---|---|
| `color` / `colors` | `colors` |
| `text` / `type` / `typography` | `typography` |
| `effect` / `shadow` | `design_system.shadow_tokens` |

Anything that doesn't match a prefix lands in `_meta.unmapped_styles` so the
adopter can see what was skipped and either rename the Figma styles or extend
their carrier file manually.

---

## 2 · Naming convention in Figma

The extractor doesn't try to guess: if the Figma styles aren't named to match
the spec layout, the values won't land in the right slots. Recommended naming
in your design library:

```
color/
  surface/
    base_light     · the page background in light mode
    base_dark      · the page background in dark mode
    raised_light   · cards / popovers / one tier up
    raised_dark
  text/
    primary_light
    primary_dark
    secondary_light
    secondary_dark
  accent/
    primary        · the brand accent (button bg, link)
    contrast       · text colour on top of accent.primary
  status/
    success_light
    success_dark
    warning_light
    warning_dark
    critical_light
    critical_dark
text/
  display/
    family
  body/
    family
  mono/
    family
```

Anything outside this layout is preserved under `_meta.unmapped_styles`, not
dropped. That's a deliberate choice — silent skips cause "where did my green
token go" debugging sessions, so the extractor surfaces them in the output.

---

## 3 · Usage

### Authentication

Get a Figma personal access token at
<https://www.figma.com/developers/api#access-tokens> and put it in your env:

```bash
# Paste the token you generated at the URL above (starts with `figd_`).
export FIGMA_TOKEN='<YOUR_FIGMA_PERSONAL_ACCESS_TOKEN>'
```

The token is **read-only** for our purpose — never commit it to a repo, and
prefer rotating it after extraction is done.

### One-shot extraction

```bash
# File key is the segment in the Figma URL after /file/ or /design/
python3 scripts/figma-to-brand-spec.py 1abc2DEF3ghi4JKL5mno6PQR
```

By default this:

1. Fetches the file via the API,
2. Walks the document tree and resolves named styles,
3. Merges the extracted values *on top of* `assets/team-brand-spec.default.json`
   so untouched groups (iconography, motion, etc.) keep their evidence-anchored
   defaults,
4. Writes `team-brand-spec.json` to the current directory.

### Output to a custom path

```bash
python3 scripts/figma-to-brand-spec.py <FILE_KEY> --output ./brand/spec.json
```

### Don't merge (emit only extracted slots)

```bash
python3 scripts/figma-to-brand-spec.py <FILE_KEY> --no-merge
```

Useful for review — see exactly what the Figma file defines, with nothing else.

### Merge into an existing carrier

```bash
python3 scripts/figma-to-brand-spec.py <FILE_KEY> --base team-brand-spec.json
```

Layers extracted values over your existing carrier (so you keep manual edits
in slots Figma doesn't define).

### Offline / fixture mode

```bash
python3 scripts/figma-to-brand-spec.py --fixture scripts/fixtures/figma_minimal.json
```

The fixture is a JSON file shaped like a Figma API response. The test suite
(`scripts/test_figma_to_brand_spec.py`) uses this path so CI runs without
network access.

---

## 4 · Reference Figma files

Two public files cover the most-common adopter context:

| Source | Figma community file | Why useful |
|---|---|---|
| Material 3 Design Kit (Google) | <https://www.figma.com/community/file/1035203688168086460> | Defines a complete colour / text style set under Material's own naming. After duplicating to your workspace, run the extractor to see the mapping output, then rename styles to match the slash convention if needed. |
| iOS 18 / iPadOS 18 (community-maintained mirror) | <https://www.figma.com/community/file/1248375255495415511> | Apple Human Interface Guidelines tokens. Same workflow. |

These aren't shipped as fixtures in this repo because each adopter needs to
duplicate to their own workspace and (typically) rename styles. The extractor
records what it didn't recognise, so the first run on Material 3 will produce
a long `_meta.unmapped_styles` list — that's expected.

---

## 5 · Output shape

The extractor writes a JSON document with the same top-level layout as
`assets/team-brand-spec.default.json`, with one addition: every run records
provenance in `_meta`:

```json
{
  "_meta": {
    "extracted_from": "Acme Brand Library",
    "extracted_at": "2026-05-11T08:42:01Z",
    "tool": "scripts/figma-to-brand-spec.py",
    "unmapped_styles": [
      {
        "figma_name": "primitives/Loose Random",
        "kind": "color",
        "value": "#808080"
      }
    ]
  },
  "colors": { … },
  "typography": { … },
  …
}
```

`_meta.extracted_at` mirrors Figma's `lastModified` so the carrier records
*which version* of the design library it was pulled from. Downstream automation
can compare that timestamp against the live Figma file to detect drift.

---

## 6 · What this tool does NOT do

These boundaries are deliberate; each was considered in Step 5 plan:

- **No round-trip**. The extractor reads Figma; it does not write back.
  Use a Figma plugin or the Figma API directly if you want JSON → Figma.
- **No CSS scraping**. Adopters who don't use Figma should fall back to
  hand-editing `team-brand-spec.json` (start from the default file) — CSS
  scraping was rejected as a path during Step 5 plan because production CSS
  is too volatile across deploys.
- **No image / icon extraction**. The extractor handles named token styles
  (color / text / effect) only. Logo SVGs, icon sets, and product imagery
  are out of scope — adopters reference those by path in the spec.
- **No automatic re-extraction on Figma changes**. Re-run the tool manually
  (or schedule it in your CI) when you want to refresh the carrier.

---

## 7 · License posture

- The extractor itself ships under this repo's Apache-2.0 licence.
- Output JSON belongs to the adopter (it describes their brand).
- When you run the extractor against a *public* Figma community file you've
  duplicated to your workspace, the *naming* and *structure* you get out
  is the community-file author's design choice — credit them in your
  carrier's `_meta.credits` (an optional free-form field) if you ship the
  spec publicly. The hex values themselves are facts about the file, not
  protected IP.

---

## 8 · Related

- `assets/team-brand-spec.default.json` — the canonical default the extractor
  merges into.
- `references/brand-spec-fields.md` — field-by-field reference for the spec
  shape.
- `references/web3-game-style-stats.md` — the 11-service evidence sweep
  behind the default values.
- `scripts/init-brand.py` — the lighter-weight alternative when you just want
  to stamp the default (no Figma involved).
- `references/security-config.md §1` — asset host allowlist; remember to add
  `api.figma.com` if your skill's settings need to reach the API directly.
