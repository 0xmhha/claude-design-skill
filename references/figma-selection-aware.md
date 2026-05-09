# Figma Selection-Aware Workflow

> "The user said 'make this bigger' — what is 'this'?"
> This guide makes that question answerable. Read after `figma-workflow.md`.

---

## 0 · The failure mode this fixes

The user is in Figma. Their cursor selects a layer. They switch to chat and type:

> "make this 20% larger and use our brand orange instead"

Without selection-awareness, the agent has three bad options:
1. **Guess** — pick "the most recent thing we discussed" or "the page root". Often wrong.
2. **Ask back vaguely** — "Which element?" The user loses momentum.
3. **Apply globally** — change every orange-ish thing on the page. Worst case.

This guide gives a fourth, correct option: **read the user's selection from Figma, show it back, confirm, then act.**

---

## 1 · Workflow with Figma MCP

When a Figma MCP server is available (look for tool names like `figma_get_selection`, `figma_get_node`, `figma_export_image`):

### Step 1 · Read the current selection

```
tool: figma_get_selection
returns: { nodeId, name, type, parents: [...], page: { id, name }, fileKey }
```

If `nodeId` is empty (nothing selected), tell the user:
> "Nothing is selected in Figma. Select the layer you want to edit, then send the request again."

Don't proceed to Step 2 with no selection.

### Step 2 · Capture a visual + structural snapshot

```
tool: figma_export_image
args: { nodeId, format: "PNG", scale: 2 }
returns: image bytes
```

```
tool: figma_get_node
args: { nodeId, depth: 2 }
returns: full node JSON (children up to 2 levels, with name, type, sizes, fills)
```

Save the image to `assets/figma-reports/selection-<short-id>.png` and record the node JSON.

### Step 3 · Confirm with the user (mandatory)

Before any edit, present:

```markdown
You selected:
  • **<name>** (<type>) — id `<nodeId>` on page **<page.name>**
  • Path: <parent.name> › <parent.parent.name> › …
  • Size: <w>×<h> · Fills: <colors>

[ image: assets/figma-reports/selection-<short-id>.png ]

You asked: "make this 20% larger and use our brand orange instead"

Plan I would apply:
  1. Resize node `<nodeId>` to <newW>×<newH>
  2. Change its primary fill to `team-brand-spec.json` `colors.accent` = `#D97757`

Confirm? [yes / no / edit]
```

Wait for yes / no / edit. Don't use language like "I'll proceed unless you say otherwise" — that defeats the gate.

### Step 4 · Apply via MCP

Only after confirmation. Use the smallest scope tools available:
- `figma_set_node_size` for resize
- `figma_set_node_fill` for color
- `figma_set_node_name` for rename

After each call, request `figma_get_node` again and diff against the plan to verify the edit landed.

### Step 5 · Report

Append to `assets/figma-reports/<date>-selection-edit.md`:
- Selection summary
- User's request verbatim
- The plan (Step 3)
- The actual API calls (Step 4)
- Verification diff

---

## 2 · Workflow without Figma MCP

When no Figma MCP is available, the user is the bridge.

### Step 1 · Ask the user to share the selection

Pick whichever the user can give fastest:

| User has | Send |
|---|---|
| Figma desktop / web open | "Select the layer in Figma, then `Cmd+L` to copy its share link, paste here." |
| Screenshot tool | "Drag-select the layer, take a screenshot of the layer tree panel + the canvas, paste here." |
| Both | Ask for both — link disambiguates the node id, screenshot disambiguates the visual |

If the share link includes `?node-id=<id>`, that's the node id you'll need.

### Step 2 · Confirm what was sent

The user pasted a link / screenshot / both. Echo back what you understood:

```markdown
Got it — you're pointing at:
  • <description from screenshot>
  • Figma node id: `<id>` (from the link's node-id parameter)

You asked: "<user's request>"

Plan:
  1. <step 1>
  2. <step 2>

Since I don't have direct Figma write access, I'll describe the changes you can apply yourself.

Confirm? [yes / no / edit]
```

Same gate as Step 3 of the MCP path.

### Step 3 · Output as user-applicable instructions

Without MCP, the agent can't apply changes itself. Instead, write a numbered checklist the user can follow:

```markdown
Apply in Figma:

1. Select node `<id>` (or click `<name>` in the layer panel)
2. Property panel → W: <newW>, H: <newH>
3. Fill swatch → enter `#D97757` (team-brand-spec.json `colors.accent`)
4. (verify) Right panel → confirm fill is now solid `#D97757`
```

Save the checklist to `assets/figma-reports/<date>-selection-edit.md` so the user can re-run later.

### Step 4 · Optional: prepare a diff for the next round

If the user comes back with "step 3 didn't change the right layer", that's the layer-naming problem in disguise. Route them to `figma-layer-naming.md` first, then resume.

---

## 3 · Selection ambiguity edge cases

| Edge case | What to do |
|---|---|
| User selected a **group** but their request only makes sense for a **child** of the group ("make the icon bigger") | Confirm: "You selected the group `<name>`. Did you mean the icon child `<child.name>`?" — name both options |
| User selected **multiple nodes** at once | Show the list and ask which one(s) the request applies to. Don't assume "all of them" |
| User selected a **component instance**; the change should propagate to the master | Tell the user explicitly: "This is an instance of master `<name>`. Apply to: [this instance only / the master so all instances update]?" |
| User selected a **locked** layer | Don't try to bypass. Tell the user the layer is locked and ask if they want to unlock |
| Selection straddles two **pages** | Reject — operations on cross-page selections are usually a mistake. Ask which page |

---

## 4 · Things this workflow does NOT do

- It does **not** silently apply changes. The confirmation gate (§1 Step 3 / §2 Step 2) is mandatory.
- It does **not** infer selection from chat history when Figma says nothing is selected. If selection is empty, that's the answer.
- It does **not** rename layers as a side effect (use `figma-layer-naming.md` for that).
- It does **not** create new components as a side effect (use `figma-component-grouping.md`).
- It does **not** modify `team-brand-spec.json` as a side effect (use `figma-brand-spec-import.md`).

Each of those is its own deliberate workflow with its own confirmation pattern. Selection-aware edit is for **direct property changes on a confirmed target** — nothing else.

---

## 5 · Self-check before delivery

- [ ] Did I read selection state (or get the user's selection link/screenshot) before proposing changes?
- [ ] Did I show the selection back as **name + path + size + fill + image** so the user can verify it's the right layer?
- [ ] Did I get explicit confirmation of the change plan before applying?
- [ ] Did I produce a report under `assets/figma-reports/`?
- [ ] If I used MCP, did I verify each edit landed via a follow-up `figma_get_node`?

---

**Owner**: Internal design platform team
**Last reviewed**: 2026-05-08
**Related**: `figma-workflow.md` · `figma-layer-naming.md` (when selection is unclear because layers are unnamed)
