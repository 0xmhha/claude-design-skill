# SVG Sanitization · Mandatory Pass for Any External SVG

> Even SVGs from allowlisted hosts (Wikimedia / press kits / user-shared files) **must** pass this sanitizer before being inlined into HTML/JSX. SVG is an active container — it can carry `<script>`, `<foreignObject>`, event handlers, and external resource references.
>
> Pairs with `references/security-config.md` (allowlist) — together they form the external-asset trust boundary.

---

## 0 · Threat model

A "logo SVG from Wikimedia Commons" is not equivalent to a PNG of that logo. SVG can do all of the following inside a single file:

| Vector | Effect when inlined |
|---|---|
| `<script>` element | Immediate JS execution in the host document |
| `<foreignObject>` + `<iframe>` / `<body>` | Arbitrary HTML/JS injection into the SVG namespace |
| Event handlers (`onload`, `onclick`, `onmouseover`, `onbegin`, …) | JS runs on user interaction or animation start |
| `xlink:href` / `href` to external URL | SSRF, tracking pixel, cache poisoning, asset substitution |
| `<image href="javascript:…">` | XSS via javascript: URL |
| `<use href="…#id">` to external doc | Loads an attacker-controlled SVG, then includes a fragment of it |
| `<style>` with `url(...)`, `@import`, `expression(...)` | External CSS load / IE-era expression injection |
| External `<!ENTITY …>` (XXE) | XML external entity attack against the parser |
| `<animate>` with `attributeName="href"` | Sneaky href mutation post-load |

Therefore: **never inline an SVG that hasn't passed this sanitizer.**

---

## 1 · Allowed tags (whitelist)

Anything outside this list is **stripped**.

```
svg defs g use symbol marker
path circle rect line polyline polygon ellipse
text tspan textPath
title desc
linearGradient radialGradient stop pattern
clipPath mask
filter feGaussianBlur feOffset feFlood feComposite feColorMatrix
        feMerge feMergeNode feTurbulence feDisplacementMap feMorphology
        feBlend feSpecularLighting feDiffuseLighting feDistantLight fePointLight
animate animateTransform   ← OK structurally; event-bearing attrs still stripped
```

**Forbidden tags (always stripped, even if listed elsewhere)**:
```
script foreignObject iframe object embed image audio video
handler set
```

Note: `image` (with lowercase `i`) is forbidden because of the `javascript:` URL attack and external raster fetch. If you genuinely need a raster inside an SVG, downscale to PNG and reference via `<img>` outside the SVG.

---

## 2 · Allowed attributes

```
# Geometry
x y x1 y1 x2 y2 cx cy r rx ry width height
points d transform viewBox preserveAspectRatio

# Visual
fill stroke stroke-width stroke-linecap stroke-linejoin
stroke-dasharray stroke-dashoffset stroke-miterlimit
stroke-opacity fill-opacity opacity
fill-rule clip-rule
stop-color stop-opacity offset
gradientUnits gradientTransform spreadMethod
mask clip-path filter

# Typography
font-family font-size font-weight font-style
text-anchor letter-spacing word-spacing
dominant-baseline alignment-baseline

# Identification + a11y
id class
aria-label aria-labelledby aria-describedby role

# SVG namespace
xmlns xmlns:xlink xml:space

# Animation declarative attrs (no event handlers!)
attributeName from to dur begin end repeatCount values keyTimes
```

**Special handling — `href` / `xlink:href`**:
- Allowed **only** on `<use>` and only if the value matches `^#[A-Za-z][A-Za-z0-9_-]*$` (intra-document fragment).
- `data:` URLs are **forbidden** (unless an explicit allowlist of `data:image/png;base64,…` for embedded raster is added per project — default is forbidden).
- All other URL-bearing attributes (`src`, external `href`, `xlink:href` on non-`<use>`) → **stripped**.

**Always stripped** (even if the value looks innocuous):
```
on*               # every on-prefixed event handler attribute
javascript:*      # any value starting with javascript:
expression(*)     # IE-era CSS expressions
behavior:*        # IE-era behaviors
```

**`<style>` and inline `style=""`**:
- Allowed **after secondary CSS sanitize**: strip any token containing `url(`, `@import`, `expression(`, `javascript:`, or `behavior:`.
- Multi-pass — sanitize the SVG, then sanitize the CSS inside it.

---

## 3 · `scripts/svg-sanitize.py` — the implementation

The skill ships a Python sanitizer at `scripts/svg-sanitize.py`. **Always run it after downloading any SVG**, before inlining or copying into the project's `assets/<brand>-brand/`:

```bash
python scripts/svg-sanitize.py \
  --in  assets/<brand>-brand/logo-source.svg \
  --out assets/<brand>-brand/logo.svg \
  --report assets/<brand>-brand/PROVENANCE.md
```

Behavior:
1. Parse with `lxml` (defusedxml-style: external entity resolution disabled, billion-laughs guarded).
2. Walk the tree; drop disallowed tags, attributes, and CSS tokens per §1–§2.
3. Compute SHA-256 of input and output; both go into the report.
4. If anything was stripped, **the output is still produced**, but the report records every removal so the team can review what changed.
5. Exit code: `0` clean, `0` clean-after-strip, `2` parse error, `3` policy violation flagged for review (`<script>` was found).

`--strict` mode: exits non-zero if **any** strip happened — fail builds on suspicious SVG.

---

## 4 · Audit trail — PROVENANCE.md

For every external SVG used in the project, append an entry:

```markdown
## logo-source.svg → logo.svg
- Date: 2026-MM-DD
- Source: https://commons.wikimedia.org/wiki/File:Foo.svg
- License: Public Domain
- Input SHA-256:  e3b0c44298fc1c149afbf4c8996fb924…
- Output SHA-256: 27cd4da25ebf8b6948c8bcfbcd1f2c4d…
- Sanitizer findings:
  - Stripped 1× `<script>` block (lines 12–18 of source)
  - Stripped `onload="track()"` attribute on root `<svg>`
  - 0 disallowed tags remaining
- Used in: slides/03-hero.html
```

The hash pair lets future audits detect tampering: if `logo.svg` no longer matches the recorded output hash, something modified it after sanitization.

### 4.1 · In-file visibility comment

Whenever the sanitizer drops anything (dangerous tag, non-allowlist tag, event handler, dangerous-value attribute, CSS forbidden token), the output SVG also receives a leading `<!-- svg-sanitize: stripped N item(s) [POLICY-VIOLATION] - … -->` XML comment. This makes the audit trail discoverable from the file alone — useful when an SVG is shared without its `PROVENANCE.md`. The comment is plain XML, content-safe (`--` sequences escaped), and never affects rendering. Regression-tested by `scripts/test_svg_sanitize.py::TestVisibilityMetaComment`.

---

## 5 · Failure-mode placeholder (graceful degradation)

If sanitize finds **dangerous content** (`<script>`, `<foreignObject>`, `javascript:` URL, external `href`):

1. The output SVG is **not used**.
2. In its place, generate a visual placeholder:

```html
<!--
  SVG SANITIZE FAILED · 2026-MM-DD
  Source: <url>
  Reason: <script> element found at line 12
  Action: replaced with placeholder. Manual review required.
  See: assets/<brand>-brand/PROVENANCE.md
-->
<div style="
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 200px;
  height: 60px;
  background: repeating-linear-gradient(
    45deg, #FEE2E2, #FEE2E2 8px, #FCA5A5 8px, #FCA5A5 16px
  );
  color: #7F1D1D;
  font-family: monospace;
  font-size: 11px;
  border: 1px dashed #B91C1C;
  border-radius: 4px;
">
  ⚠ SVG REJECTED · review PROVENANCE.md
</div>
```

This makes the failure visible — the designer notices on first preview and can supply an alternative asset. Silent fallback to "no image" hides the problem.

---

## 6 · Content Security Policy meta tag (defense in depth)

Even with sanitization, every generated HTML deliverable should include a CSP meta tag at the top of `<head>`. This is the second line of defense — if sanitize misses something, CSP blocks runtime exploitation.

**Default CSP for prototype HTML using the React+Babel pinned setup**:

```html
<meta http-equiv="Content-Security-Policy" content="
  default-src 'self';
  script-src 'self' 'unsafe-inline'
    https://unpkg.com/react@18.3.1/
    https://unpkg.com/react-dom@18.3.1/
    https://unpkg.com/@babel/standalone@7.29.0/;
  style-src  'self' 'unsafe-inline' https://fonts.googleapis.com;
  font-src   'self' https://fonts.gstatic.com;
  img-src    'self' data: https://commons.wikimedia.org https://images.unsplash.com https://images.pexels.com;
  connect-src 'self';
  frame-src  'none';
  object-src 'none';
  base-uri   'self';
">
```

Notes:
- `'unsafe-inline'` for script is required because the React+Babel prototype pattern uses `<script type="text/babel">` blocks. This is acceptable for prototype delivery (not production).
- `frame-src 'none'` and `object-src 'none'` neutralize the `<iframe>`/`<object>`/`<embed>` vectors even if sanitize missed them.
- `img-src` lists the allowlist hosts (mirrors `security-config.md` §1).
- For production deliveries, the CSP must be tightened further (no `'unsafe-inline'`, no Babel — pre-compile).

The skill's HTML starter templates (in `references/react-setup.md`) include this CSP block by default.

---

## 7 · Workflow integration

Where this fits in the broader skill flow:

```
Core Asset Protocol Step 3 (allowlist download)
   │
   ├─> SVG file downloaded to assets/<brand>-brand/<name>-source.svg
   │
   ├─> python scripts/svg-sanitize.py --in <name>-source.svg --out <name>.svg --report PROVENANCE.md
   │
   ├─> sanitize result:
   │     ✅ clean   → use <name>.svg in HTML
   │     ⚠ stripped → use <name>.svg, log strip details to PROVENANCE.md, notify user
   │     ❌ rejected → emit visual placeholder, halt and ask user for alternative
   │
   └─> generated HTML always includes the CSP meta tag (see §6)
```

Forbidden by default (per `security-config.md` §2): inline-grepping `<svg>` straight out of `homepage.html` and pasting it into the deliverable. That bypass is explicitly removed in this fork.

---

**Owner**: Internal design platform team
**Last reviewed**: 2026-05-08
**Related**: `security-config.md` · `react-setup.md` (CSP block) · `PROJECT-PLAN.md` Phase 1 Group B
