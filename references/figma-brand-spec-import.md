# Figma → `team-brand-spec.json` Import

> Pull design tokens (colors, typography, logo, product images) from a Figma library into the project's `team-brand-spec.json` so every other workflow in this skill can use them.
>
> This is the **upstream half** of the Core Asset Protocol (`SKILL.md` §1.a). Once `team-brand-spec.json` is populated from Figma, downstream workflows read it instead of asking the user every time.

---

## 0 · When to run this

- **At project start** — once, to set up the brand spec
- **When the brand changes** — re-import to refresh the spec
- **When a designer joins** — after they're given access to the Figma library, run import to verify the spec matches what they see

If `team-brand-spec.json` already exists, this workflow produces a **diff against the existing file** and asks the user to accept changes per-key. It does not blow away the existing spec.

---

## 1 · What gets imported

| Spec field | Source in Figma | Strategy |
|---|---|---|
| `colors.primary` / `accent` / `background` / `ink` / `muted` / `hairline` | Figma color styles named `primary` / `accent` / etc. | Direct value lift |
| `colors.forbidden` | Not in Figma — kept manual | (skip; preserve existing) |
| `typography.display` / `body` / `mono` | Figma text styles named `display-*` / `body-*` / `mono-*` (or `Display / Heading / Body / Mono` if using Material-ish naming) | Lift the font family + smallest of each style class |
| `logo.primary` / `primary_inverse` / `wordmark` / `icon` | Figma components named `Logo / Primary`, `Logo / Inverse`, `Logo / Wordmark`, `Logo / Icon` | Export each component as SVG, **run through `scripts/svg-sanitize.py`**, save to `assets/<brand>-brand/`, write the path |
| `product_assets.hero_image` | Figma frame named `Product / Hero` (or similar) | Export PNG @ 2x, save, write path |
| `ui_screenshots.home` / `feature_pages.*` | Figma frames named `UI / Home`, `UI / Feature / *` | Export PNG @ 2x, save, write path |
| `design_system.spacing_scale` | Figma's number variables under `spacing` collection (if using Figma Variables) | Lift the array |
| `design_system.shadow_tokens` | Figma effect styles named `shadow / *` | Lift the value (may need conversion to CSS) |
| `design_system.figma_library_url` | The file URL itself | Lift the URL |
| `current_project.figma_url` | Whichever file the user invoked the workflow from | Lift |

Anything not findable in Figma is **left blank in the proposed diff** with a note `(not found in Figma — keep existing or fill manually)`. The user decides what to do.

---

## 2 · MCP path

### Step 1 · Identify the Figma source

Two cases:

**Case A · A team library file is provided**:
The user shares the library URL. Use `figma_get_file` with the file's key.

**Case B · Use the current project file**:
The user is in their working file, no separate library. Use `figma_get_selection` to get the file key. Note this in the report — it means the brand-spec is being inferred from the project, not from a maintained library.

### Step 2 · Read styles + components

```
tool: figma_get_file_styles
args: { fileKey }
returns: { color: [{name, value, id}], text: [...], effect: [...] }
```

```
tool: figma_get_file_components
args: { fileKey }
returns: [{ name, id, description }]
```

```
tool: figma_get_file_variables    // newer Figma Variables (2024+)
args: { fileKey }
returns: { collections: [{ name, modes, variables: [...] }] }
```

Build the full inventory:
- Color styles map → `{name → hex}`
- Text styles map → `{name → {fontFamily, fontSize, fontWeight}}`
- Components named `Logo / *` → `{name → componentId}`
- Effect styles map → `{name → cssShadow}`
- Variables collections → spacing, radius, etc.

### Step 3 · Map to spec keys

Use heuristics + the user's existing `team-brand-spec.json` (if any) to map Figma names to spec keys:

```python
# pseudocode
def find_color(name_candidates, figma_color_styles):
    """Return the first match (case-insensitive) from candidates list."""
    for candidate in name_candidates:
        for style in figma_color_styles:
            if style.name.lower() == candidate.lower():
                return style.value
    return None

primary = find_color(['primary', 'brand/primary', 'color/primary', 'main'], color_styles)
accent  = find_color(['accent',  'brand/accent',  'color/accent', 'highlight'], color_styles)
# … etc
```

If multiple candidates match (e.g., both `primary` and `brand/primary` exist with different values), **don't pick one silently** — present the conflict to the user.

### Step 4 · Export logo / product / UI assets

For each found component / frame:

```
tool: figma_export_image
args: { nodeId: <componentId>, format: "SVG", scale: 1 }   // for logo
returns: bytes
```

For SVG exports, **immediately** run through `scripts/svg-sanitize.py`:

```bash
# pseudocode
write_bytes(temp_path, svg_bytes)
subprocess.run([
  "python3", "scripts/svg-sanitize.py",
  "--in",  temp_path,
  "--out", final_path,
  "--report", "assets/<brand>-brand/PROVENANCE.md",
  "--source-url", f"figma://{fileKey}/{componentId}",
])
```

For PNG exports (product / UI screenshots), no sanitize step needed but record the SHA-256 in PROVENANCE.md anyway (consistency).

### Step 5 · Build the proposed spec

Produce a JSON diff against the existing `team-brand-spec.json`:

```diff
{
  "brand": {
-   "name": "REPLACE_ME",
+   "name": "Example Studios",
    "tone_keywords": ["confident", "playful"]
  },
  "colors": {
-   "primary": "#000000",
+   "primary": "#1E40AF",
-   "accent":  "#3B82F6",
+   "accent":  "#D97757",
+   "background": "#FAF9F5"     // new — not in current spec
  },
  "logo": {
+   "primary": "assets/example-brand/logo.svg",
+   "primary_inverse": "assets/example-brand/logo-white.svg"
  },
  …
}
```

### Step 6 · Confirm with the user (mandatory, per-section)

```markdown
## Brand-spec import diff · 5 sections changed

### colors (3 changes)
- primary:    #000000 → #1E40AF
- accent:     #3B82F6 → #D97757
- background: (new)   → #FAF9F5

Apply this section? [yes / no / edit]

### typography (1 change)
- display: "Source Serif 4, …" → "Inter Display, …"
- body:    (no change)
- mono:    (no change)

Apply this section? [yes / no / edit]

### logo (2 new files)
- primary:         (new) → assets/example-brand/logo.svg         [SVG sanitize: clean, see PROVENANCE.md]
- primary_inverse: (new) → assets/example-brand/logo-white.svg   [SVG sanitize: clean]

Apply this section? [yes / no / edit]

…
```

Per-section, not per-key. Bulk confirmation per key is overkill; whole-spec confirmation hides important changes (a primary color change is a big deal).

### Step 7 · Apply

Merge accepted sections into `team-brand-spec.json`. Pretty-print, preserve existing order, retain comments (the `_meta` / `_note` blocks).

### Step 8 · Report

Save `assets/figma-reports/<date>-brand-spec-import.md` with:
- Source Figma file URL + access mode (library / project)
- Diff that was proposed
- Diff that was accepted
- Files written to `assets/<brand>-brand/`
- SVG sanitize results (clean / stripped count)

---

## 3 · Workflow without Figma MCP

### Step 1 · Ask the user to export from Figma

The user has two options:

**Option A · Use the Figma "Export" feature**:
1. Open Assets panel
2. For each color style: copy the hex (right-click → Copy as CSS)
3. For each text style: note the font + size
4. For each logo component: select → File → Export → SVG
5. Paste a single block to chat:

```
Colors:
- primary: #1E40AF
- accent: #D97757
- background: #FAF9F5

Typography:
- display: Inter Display, 32-72
- body: Inter, 14-16

Logo SVG (paste below):
<svg ...>...</svg>
```

**Option B · Use a Figma plugin** to export all styles as JSON (e.g., "Design Tokens", "Figma Tokens"). User pastes the JSON.

### Step 2 · Process whatever the user provided

Build the diff against existing `team-brand-spec.json` from the pasted content. If the user pasted SVG content directly:
- Save to `assets/<brand>-brand/logo-source.svg`
- Run `scripts/svg-sanitize.py` on it (just like the MCP path)
- Use the sanitized output as the spec value

### Step 3 · Same confirmation gate, same report

Steps 6-8 of the MCP path are identical. The diff format, the per-section confirmation, the report — all the same. Only the source-of-data differs.

---

## 4 · Conflict resolution

### 4.1 · Multiple candidates for one spec key

Figma has both `primary` (`#000000`) and `brand/primary` (`#1E40AF`). Which wins?

Don't guess. Present:
```
Ambiguous match for `colors.primary`:
  - Figma color style `primary` = #000000
  - Figma color style `brand/primary` = #1E40AF

Which should map to `team-brand-spec.json` `colors.primary`?
```

User picks. Save the user's preference as a hint for future re-imports (e.g., write a `_figma_mapping_hints` block in `team-brand-spec.json`).

### 4.2 · Existing spec value differs from Figma

The current spec has `colors.primary = #2563EB`, Figma has `#1E40AF`. Don't overwrite without confirmation. The current value may have been hand-tuned for a reason.

### 4.3 · Figma logo SVG fails sanitize policy

If `scripts/svg-sanitize.py` exits 3 (policy violation), the logo is rejected. Tell the user:

```
The logo SVG from Figma failed sanitize:
  - Found 1× <script> element (line 14)
  - Found 1× event handler `onload`

This is unusual for a designer-authored logo. Possible causes:
  - The logo was imported from an external source originally
  - A Figma plugin annotated it with metadata that included scripts

Action options:
  - Re-export from Figma after removing custom layer effects
  - Use the upstream logo file (the brand's actual logo, not the Figma-stored copy)
  - Skip the logo and ask the brand owner for a clean SVG
```

Don't bypass sanitize. Sanitize is the line.

---

## 5 · Self-check before delivery

- [ ] Read all relevant Figma styles (colors, text, effects, variables, logo components)?
- [ ] Built a diff against the existing `team-brand-spec.json`?
- [ ] Confirmed **per section**, not per-key or whole-file?
- [ ] Every SVG exported from Figma went through `scripts/svg-sanitize.py`?
- [ ] PROVENANCE.md updated with hashes for every asset file written?
- [ ] Report saved to `assets/figma-reports/<date>-brand-spec-import.md`?
- [ ] Naming-mapping conflicts surfaced explicitly, not silently resolved?

---

**Owner**: Internal design platform team
**Last reviewed**: 2026-05-08
**Related**: `figma-workflow.md` · `team-brand-spec.default.json` · `svg-sanitize.md` (mandatory for SVG exports) · `security-config.md` (allowlist if Figma exports point at S3 hosts)
