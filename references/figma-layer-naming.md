# Figma Layer Naming · Assigning Meaningful Names to Unnamed Layers

> Most Figma files arrive with layers named `Frame 47`, `Rectangle 31`, `Group 12`. This is the single biggest blocker to LLM-assisted design work — without semantic names, every downstream workflow degrades.
>
> This guide turns the unnamed pile into a named tree, with the user in the loop for every batch.

---

## 0 · Why this matters more than it looks

Unnamed layers cause:
- **Selection-aware edits fail** — "the button" doesn't match `Rectangle 31`
- **Component grouping is impossible** — repeated patterns can't be found if every instance is named differently auto-incrementally
- **CSS layer mapping breaks** — code generation needs semantic names (`.primary-button`, `.user-card`) not `frame-47`
- **The next designer can't onboard** — Figma file becomes write-only

A 20-minute pass that renames the right 50 layers unblocks weeks of downstream LLM work. This is high-leverage.

---

## 1 · Naming convention (apply consistently)

Match the project's broader convention if `team-brand-spec.json` `design_system.layer_naming_convention` is set. If not set, default to:

| Layer type | Convention | Example |
|---|---|---|
| Page | `<area> · <state>` (Title Case + middle dot) | `Onboarding · Step 1`, `Profile · Logged Out` |
| Frame (screen) | `<screen-name>` (kebab-case, lowercase) | `home-screen`, `wallet-deposit` |
| Frame (region inside screen) | `<region>--<modifier>` | `header--scrolled`, `card-list--empty` |
| Component (master) | `Component / <Category> / <Name>` (slashes for nesting in Figma's lib) | `Component / Button / Primary`, `Component / Card / NFT-tile` |
| Component instance | inherit master name (don't rename instances unless clarifying) | (auto) |
| Variants | `<state>=<value>, <prop>=<value>` | `state=hover, size=lg` |
| Atomic shapes (rect, circle, vector) | `<role-noun>` (kebab) | `avatar-mask`, `divider-line`, `chevron` |
| Text | the literal text content if short, otherwise `<role>-text` | `"Sign in"`, `headline-text` |
| Image | `<subject>-image` | `hero-image`, `logo-image` |
| Vector / icon | `icon-<name>` | `icon-arrow-right`, `icon-check` |
| Group (utility) | `g/<purpose>` | `g/avatar-stack`, `g/cta-row` |

**Rules**:
- **Never** keep `Frame N`, `Rectangle N`, `Group N`. Those are the targets to fix.
- **Lowercase kebab** for everything except component master names (which use `Component / Path / Like / This` with slashes — Figma's convention for library nesting).
- **No spaces in technical layer names** (use `-`); spaces are fine in page names.
- **No emojis**, no Chinese unless `team-brand-spec.json` brand language is Chinese.

---

## 2 · Workflow with Figma MCP

### Step 1 · Scope the rename

Ask the user which scope to clean up:
1. The current selection
2. The current page
3. The whole file

Default: **current page**. File-wide is risky and slow; ask before doing it.

### Step 2 · Walk the layer tree

```
tool: figma_get_node
args: { nodeId: <page or selected node>, depth: -1 }   // full tree
```

For each node, build a record:
```
{ id, current_name, type, has_default_name (bool), siblings_count, children_count, visual_summary }
```

`has_default_name` flags any name matching `^(Frame|Rectangle|Ellipse|Group|Vector|Polygon|Star|Component) \d+$` — the generic auto-names.

### Step 3 · Propose names (in batches)

Generate name proposals for the flagged nodes. Use the visual + structural context:
- A `Rectangle` with `cornerRadius=999` and child text "Sign in" → `btn-sign-in`
- A `Frame` with `Image` child + nothing else → `<image-subject>-card` (ask user for subject if unclear)
- A `Group` containing 3 sibling avatars → `avatar-stack`
- An `Ellipse` 40×40 with image fill → `avatar`

Present in batches of **10–20**:

```markdown
## Layer naming · batch 1 of 3

| # | id | current → proposed | reason |
|---|----|--------------------|--------|
| 1 | 1:42 | `Frame 47` → `home-hero` | first-screen frame at top of Home page |
| 2 | 1:43 | `Rectangle 31` → `cta-button` | child has text "Get started", radius 999 |
| 3 | 1:44 | `Group 12` → `feature-row` | 3 sibling cards in a horizontal flex |
| … | | | |
| 20 | … | … | … |

Confirm:
  - "all" → apply all 20
  - "1, 2, 5-8" → apply selected
  - "skip 3, 7" → apply rest
  - "edit 4: btn-primary" → use that name instead, then apply all
  - "no" → don't rename anything in this batch
```

Wait for the user. Don't apply silently.

### Step 4 · Apply

```
tool: figma_set_node_name
args: { nodeId, name }
```

Loop through accepted rows. After each successful rename, re-fetch the node and confirm the rename landed.

If the user accepted a row but the rename fails (e.g., layer was deleted in the meantime), report the failure — don't move on silently.

### Step 5 · Repeat for next batch

Continue Steps 3-4 in batches of 10-20 until all flagged nodes are processed (or the user says "stop, that's enough for now").

### Step 6 · Report

Save to `assets/figma-reports/<date>-layer-naming.md`:
- Scope (selection / page / file)
- Total flagged nodes
- Total renamed (per batch breakdown)
- Final count of remaining default-named nodes (should be 0 if scope was completed)

---

## 3 · Workflow without Figma MCP

### Step 1 · Ask the user to export the layer tree

The user can do this two ways:

**Easy path** — paste the layer panel as text:
The user expands the relevant frame in Figma's layer panel, screenshots it, and pastes. Or they install a plugin like "JSON to Figma" / "Figma to Code" that exports the tree as JSON.

**Plugin-free path** — share link + targeted screenshots:
The user shares the file link and screenshots a few specific frames. Less complete but workable.

### Step 2 · Build proposals from text alone

Without the tree as JSON, the agent works from screenshots and any text the user provided. Proposals are necessarily approximate — be explicit about that:

```markdown
Based on the screenshots, here are 12 proposed renames. I can't see the full tree, so this batch is partial — once you apply these, share the next screenshot for the next batch.

| # | What I see | proposed name |
| 1 | Top-of-screen frame with logo + "Connect Wallet" button | `home-header` |
…
```

### Step 3 · Output as user checklist

Without MCP write access, the output is a checklist the user applies in Figma:

```markdown
In Figma, rename these layers (double-click name in the left panel):

- Top-of-screen frame  →  `home-header`
- The yellow rounded rectangle with text "Connect Wallet"  →  `btn-connect-wallet`
- The 3-card row below  →  `feature-row`
- Each card in that row  →  `feature-card` (Figma will auto-suffix to `feature-card`, `feature-card 2`, `feature-card 3` — that's expected; rename each to `feature-card--<topic>`)
…
```

Same confirmation gate before generating the checklist — show the proposals in a table, get user approval, then output.

---

## 4 · Special cases

### 4.1 · Localized text content

If the screen text is in Korean / Japanese / Chinese, **don't** use the literal text as the layer name. Use the role:
- ✅ `headline-text` for `"NFT 프로필을 시작하세요"`
- ❌ `NFT 프로필을 시작하세요`

Reason: file-wide search and code generation mix poorly with non-ASCII layer names.

### 4.2 · Already-named layers that are misnamed

The user may have layers named `aaa`, `temp`, `delete-me`, or accidentally helpful-sounding names that are wrong (`button` for a non-interactive label). Treat these as candidates too:

```markdown
| # | id | current → proposed | reason |
| 17 | 1:88 | `aaa` → `divider-line` | single 1px horizontal line |
| 18 | 1:89 | `button` → `status-badge` | non-clickable label, not a button |
```

Flag in the table, get user confirmation per row.

### 4.3 · Component masters

When a component master ends up as `Component 7`, propose the slash-nested form:

```markdown
| # | id | current → proposed | reason |
| 22 | 1:114 | `Component 7` → `Component / Card / NFT-tile` | used by 14 instances; visually a media card |
```

This requires reading the variants and instance count — note this in the reason.

### 4.4 · Deeply nested groups (vector boolean operations)

Vector layers like `Union 3` / `Subtract 1` inside an icon often **shouldn't** be renamed. They're internal boolean ops Figma needs. Skip nodes whose type is `BOOLEAN_OPERATION` and whose parent is a single icon component.

---

## 5 · Quality bar

- **Aim for 100% rename within the chosen scope.** Half-named files are worse than fully default-named ones — readers get false confidence.
- **Aim for 0 false positives.** If the user rejects more than 20% of proposals in a batch, stop, ask what convention they actually want, and re-propose with the corrected pattern.
- **Don't prosecute aesthetic preferences.** If the user has a name they prefer ("ctaBtn" instead of "cta-button"), accept it and use it for the rest of the file. Adjust the batch in flight.

---

## 6 · Self-check before delivery

- [ ] Scope was confirmed at Step 1?
- [ ] Proposals were shown in batches of 10–20, not all at once and not silently?
- [ ] User accepted/rejected per row before any rename was applied?
- [ ] Each successful rename was verified via re-fetch (MCP path)?
- [ ] Report written to `assets/figma-reports/<date>-layer-naming.md`?
- [ ] If user rejected >20% of a batch, did I stop and re-align on convention?

---

**Owner**: Internal design platform team
**Last reviewed**: 2026-05-08
**Related**: `figma-workflow.md` · `figma-component-grouping.md` (next step after naming) · `figma-selection-aware.md` (depends on names being right)
