# Figma viewer · reference

> Companion doc for `scripts/figma-viewer.py`.
>
> The viewer renders a Figma file to a **single self-contained HTML page**
> so designers and reviewers can sanity-check layouts without opening Figma.
> Useful when (a) the team isn't on Figma yet, (b) the reviewer doesn't have
> view access, (c) you want a quick visual diff of two extracts.

---

## 1 · What it renders

| Figma node type | Viewer output |
|---|---|
| `CANVAS` (page) | `<section class="figma-canvas">` with a header (page index, name, dimensions) + a stage at the canvas's union-of-bounds size. |
| `FRAME` / `COMPONENT` / `INSTANCE` / `GROUP` / `COMPONENT_SET` | `<div class="figma-frame">` with the frame's solid fill + corner radius, descendants nested inside. |
| `RECTANGLE` / `ELLIPSE` / `REGULAR_POLYGON` / `STAR` / `VECTOR` | `<div class="figma-shape">` with solid fill + corner radius (ellipse → `border-radius:50%`). |
| `TEXT` | `<div class="figma-text">` wrapping a `<p>` with `font-family` / `font-weight` / `font-size` / `line-height` from the node's `style`. `characters` text is HTML-escaped. |
| anything else (`BOOLEAN_OPERATION`, `SLICE`, etc.) | dashed-outline placeholder labelled with the node type — the layout slot is preserved, the renderer doesn't pretend to have painted it. |

**Intentionally minimal**: vector path data (`d`), images (`fills.type=IMAGE`),
masks, effects (shadows / blurs / glows), auto-layout, and component overrides
are *not* re-rendered. The goal is "review what landed in Figma without
opening Figma" — a visual smoke, not a full Figma replacement.

---

## 2 · Quick start

### Online (Figma REST API)

```bash
# Token from https://www.figma.com/developers/api#access-tokens
export FIGMA_TOKEN='<YOUR_FIGMA_PERSONAL_ACCESS_TOKEN>'

# File key is the segment after /file/ or /design/ in the Figma URL
python3 scripts/figma-viewer.py 1abc2DEF3ghi4JKL5mno6PQR --output viewer.html

open viewer.html   # or xdg-open / start, depending on OS
```

### Offline (fixture / CI / dry-run)

```bash
python3 scripts/figma-viewer.py \
  --fixture scripts/fixtures/figma_viewer_sample.json \
  --output viewer.html
```

The fixture is a tiny synthetic Figma response (2 pages, ~10 nodes). Use it
as a smoke test in CI or as a starting template when authoring a new fixture
for your team's design library.

---

## 3 · Keyboard shortcuts (in the rendered HTML)

| Key | Action |
|---|---|
| `→` | Next page |
| `←` | Previous page |
| `1`..`9` | Jump to page N |
| `d` | Toggle dark page chrome |

---

## 4 · Self-contained output

The generated HTML embeds **all** CSS and JS inline. No external `<link>`,
no `<script src="…">`, no `@import`. Open the file from any disk path,
email it as an attachment, or paste it into a review comment.

This is enforced by the test suite (`test_html_is_self_contained`).

---

## 5 · Security posture

- The script reads from Figma's REST API or a local fixture. **No network
  calls happen during fixture mode**, so CI runs the 15-test suite without
  a `FIGMA_TOKEN`.
- All Figma-supplied strings (`fontFamily`, `name`, `characters`,
  `data-name`, etc.) are HTML-escaped before being placed in inline style
  attributes / text content / data-attributes. The
  `test_text_family_with_quote_chars_is_escaped` test pins this invariant:
  a `fontFamily` of `Inter"><script>alert(1)</script>` from a hostile Figma
  payload cannot break the inline style attribute.
- The script never executes Figma node contents; it lays them out
  declaratively.
- Output HTML uses `data-theme="light"` / `dark` toggle but contains no
  external resource references — usable air-gapped.

---

## 6 · Use cases

| Use case | Approach |
|---|---|
| Quick visual review without Figma access | `python3 scripts/figma-viewer.py <FILE_KEY>` → open `viewer.html`. Reviewer never touches Figma. |
| Pre-Figma prototyping | Author a fixture JSON describing your draft layout. Run the viewer to see it before transcribing to Figma. |
| Visual diff between two extracts | Run viewer on the same file before / after a Figma edit; open both HTML files side-by-side. |
| CI smoke that "the file still parses" | Add the viewer step to CI: it exits non-zero on malformed JSON, missing CANVAS, etc. |
| Air-gapped review | Generate viewer.html on a connected machine; copy the single file to the air-gapped reviewer. |

---

## 7 · What's NOT in scope (deliberate)

- **Vector path rendering**: `d` attribute on VECTOR nodes is currently a
  bounding box. To support: emit `<svg><path d="..."/></svg>` per node.
  Adds complexity; out of scope for v1.
- **Image fills**: `fills[].type=IMAGE` references a Figma image hash that
  the REST API serves via `/v1/images/...`. Out of scope to keep the script
  network-only-on-`--file-key` and stdlib-only.
- **Effects**: drop shadows, glows, layer blurs. Can be added incrementally
  as CSS `filter:`/`box-shadow:` later.
- **Auto-layout reflow**: Figma's auto-layout is laid out by the browser
  here only through absolute coordinates. Frames render where Figma placed
  them, not where auto-layout would re-compute them on different content.
- **Constraints + Smart Animate / Prototype**: this viewer is static-frame
  only.
- **Component instance overrides**: the viewer renders an INSTANCE the same
  as its FRAME children — overrides are *applied at the Figma side*
  before extraction, so what the API returns is what the viewer paints.

---

## 8 · Related

- `scripts/figma-to-brand-spec.py` — the *other* Figma extractor; pulls
  named styles into `team-brand-spec.json`. Shares the same fixture shape
  and the same FILL hex-rounding logic.
- `assets/team-brand-spec.default.json` — the spec the viewer's defaults
  (font stack, surface chrome) loosely match.
- `assets/deck_stage.js` — sister visual-review tool for 1920×1080 slide
  decks. Use that for slide reviews, this for arbitrary Figma layouts.
- `references/figma-workflow.md` — entry point for any Figma-related task.
