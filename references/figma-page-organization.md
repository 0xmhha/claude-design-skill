# Figma page organization · folder / group / page cleanup · reference

> Sibling doc to `figma-component-grouping.md`. *That* one is about
> identifying repeating UI patterns and promoting them to components.
> *This* one is about **shaping the file itself** — what each page is for,
> how frames cluster into groups, when a page should be split, and how to
> name folders so a stranger can navigate in 30 seconds.
>
> Distinction: *componentization* is "this rounded button appears 14
> times — make it a component." *Page organization* is "we have 47
> frames on Page 1 — split into Pages: Foundations / Components /
> Templates / In-progress, and group the templates by section."

---

## 1 · Three levels of organization

| Level | What it is | When it matters |
|---|---|---|
| **Page** (CANVAS) | Top-level tab inside a Figma file | When the file has more than ~30 frames or more than one *kind* of thing (tokens vs templates vs in-progress) |
| **Section / Group** | Container inside a page that groups related frames | When a single page has more than one *theme* (e.g. all wallet screens vs all onboarding screens on the same page) |
| **Layer naming + folder slashes** | `Templates / Onboarding / Step 3` style names that Figma renders as folders | Always — even a single-page file benefits from naming convention |

The skill handles each level differently — the MCP-aware path calls
different Figma APIs at each level (`figma_create_page`,
`figma_create_section`, `figma_set_node_name`), and the MCP-absent path
emits step-by-step user instructions per level.

---

## 2 · Recommended page layout

Most design files in the team's adoption context fall into one of these
shapes. The skill proposes whichever fits the brief.

### Shape A · "Single product" (most common)

```
Page · Foundations         · colour / typography / icon swatches
Page · Components          · button / input / card / chip + variants
Page · Templates / Marketing · landing / about / pricing layouts
Page · Templates / Product · app screens, dashboards
Page · In-progress         · sketches, work-in-flight
Page · Archive             · superseded work, ready-to-delete
```

Why: separates *tokens* (rarely changes) from *components* (changes
weekly) from *templates* (changes daily) from *in-progress*
(changes hourly). Lets reviewers ignore the noisy bottom pages and
focus on the stable upper ones.

### Shape B · "Multi-product" (one Figma file, several apps)

```
Page · 🌐 Shared / Foundations
Page · 🌐 Shared / Components
Page · 📱 Wallet / Templates
Page · 📱 Wallet / In-progress
Page · 🖥 Dashboard / Templates
Page · 🖥 Dashboard / In-progress
```

Emoji prefix is **purely visual**, but it lets Figma's collapsed
left-rail still show which product owns which page. Use the same set
of emoji across all team files.

### Shape C · "Design exploration" (research / brainstorm)

```
Page · Brief
Page · Moodboard
Page · Direction A
Page · Direction B
Page · Direction C
Page · Synthesis
Page · Final
```

One direction per page so reviewers can A/B compare with arrow keys.
Final lands on its own page so the file can be reused as the starting
point for the production work.

---

## 3 · Sections / groups (within a page)

Once a page is chosen, the next decision is whether to group its
frames. Heuristics:

| Trigger | Action |
|---|---|
| One page has more than 15 frames | Add **Sections** (`figma_create_section`) for visual clusters. Sections render as labelled boxes in the canvas. |
| Frames are conceptually a list (e.g. icon set) | Use a **single Section** containing all of them, named with the list's purpose ("Icons · 24 px set"). |
| Frames represent variants of one screen | Use a Section *and* promote to a component variant set (`figma-component-grouping.md`). |
| Frames are entirely independent | Don't group them — section overhead isn't worth it. |

Section naming: `<category> · <count>` so a glance tells you how many
items are inside (`Wallet screens · 6`, `Onboarding · 4`, `States · 3`).

---

## 4 · Folder slash naming convention

Figma renders layer / page names containing `/` as folder hierarchies
in the left-rail tree. The convention this skill uses (matches the
naming in `team-brand-spec.default.json`, `figma-to-brand-spec.md`,
and `figma-layer-naming.md`):

```
color/accent/primary         → folder: color · subfolder: accent · leaf: primary
text/display/family          → folder: text · subfolder: display · leaf: family
templates/Onboarding/Step 1  → folder: templates · subfolder: Onboarding · leaf: Step 1
```

Slashes are read **left-to-right as nesting**, like a filesystem path.
Apply consistently:

- **Tokens & styles**: lowercase, `slash/separated`, leaves are
  `snake_case` (e.g. `color/status/success_dark`).
- **Templates & screens**: TitleCase, ` / ` (space-slash-space)
  separated (e.g. `Templates / Onboarding / Step 3`).
- **Components**: TitleCase, slash for variants
  (e.g. `Button / primary / default`, `Button / primary / hover`).

The MCP-aware path applies these via `figma_set_node_name` in batches
(10–20 nodes at a time so the user can review the diff in Figma's
history). MCP-absent path produces a rename plan as a markdown table
the user pastes into Figma via *Right-click → Rename* on each
selection.

---

## 5 · Five-step organization workflow

The skill follows this order when the user says *"clean up this file"*
or *"organize this page"*.

1. **Inventory** (`figma_get_node(file_root, depth=2)`) — list every
   page + the top-level frames on each. Output: a compact tree showing
   counts.
2. **Propose page split** — if any single page has > 20 frames *and*
   the frames clearly belong to multiple categories, propose splitting
   into N pages with names from §2's Shape table. Wait for user OK.
3. **Apply page split** (MCP-aware: `figma_create_page` + node moves;
   MCP-absent: emit instructions). Verify each new page after creation.
4. **Section the frames** (`figma_create_section` per cluster). Use
   the heuristics in §3. Name each section `<category> · <count>`.
5. **Rename layers** to match §4. This is the
   `figma-layer-naming.md` workflow; the page-organization workflow
   ends by handing off to it.

### Idempotency

The workflow is **idempotent** — running it a second time on a file
that's already organized should produce no diff. The MCP-aware path
checks `figma_get_node` results against the proposed structure before
making any change; the MCP-absent path notes "no changes needed for
this page" in the rename plan.

---

## 6 · What this workflow does NOT do

- **Visual layout reorganization**: the workflow doesn't *move frames
  around the canvas* to look prettier. It groups them logically (into
  pages / sections) but leaves the x/y coordinates as the designer
  set them.
- **Component promotion**: that's `figma-component-grouping.md`'s job.
  The page-organization workflow may notice repeating frames and
  *suggest* componentization but won't perform it.
- **Deletion / archival**: if a frame looks superseded, the workflow
  proposes moving it to *Page · Archive*, never deletes it. User
  approves deletion as a separate explicit action.
- **Cross-file moves**: the workflow operates inside a single Figma
  file. Moving frames between two files is out of scope (different
  permissions, different version histories).

---

## 7 · Sample output (rename plan, MCP-absent path)

When MCP isn't attached, the agent produces a table like:

| Current name | New name | Action |
|---|---|---|
| `Page 1` | `Foundations` | Right-click page → Rename |
| `Page 2` | `Components` | Right-click page → Rename |
| `Rectangle 47` | `color/accent/primary` | (on Foundations) select → F2 → paste |
| `Frame 38` | `Button / primary / default` | (on Components) select → F2 → paste |
| `Frame 39` | `Button / primary / hover` | (on Components) select → F2 → paste |
| `Group 12` (untitled section) | `Wallet screens · 6` | Wrap selection → Section → name |

The user applies row-by-row. Each row is independent (idempotent),
so partial application is safe.

---

## 8 · Related

- `references/figma-workflow.md` — workflow hub. Decides between
  selection-aware / layer-naming / componentization / page-organization
  based on the user's request.
- `references/figma-layer-naming.md` — leaf-level renaming workflow
  (this doc hands off to it in step 5).
- `references/figma-component-grouping.md` — repeat detection and
  componentization (sibling concern, not this doc's job).
- `references/figma-selection-aware.md` — selection confirmation
  pattern, used to verify which page / section / frame is currently
  active before each step.
- `references/figma-mcp-setup.md` — MCP detection contract for the
  `figma_create_page` / `figma_create_section` / `figma_set_node_name`
  calls used in the MCP-aware path.
