# Figma Workflow · Entry Point

> Hub document for designer workflows that originate in Figma. Pairs with the four task-specific guides:
> - `figma-selection-aware.md` — work on the layer the user has currently selected (and confirm before acting)
> - `figma-layer-naming.md` — assign meaningful names to unnamed layers
> - `figma-component-grouping.md` — propose / create components from repeating ungrouped patterns
> - `figma-brand-spec-import.md` — pull color tokens / typography / logo out of a Figma library into `team-brand-spec.json`

---

## 0 · Why this section exists

In a game / web3 studio, designers work in Figma and planners produce wireframes in Figma. When that work meets an LLM-driven design skill, three failure modes show up consistently:

1. **The LLM doesn't know which layer the user is talking about.** The user says "make the button bigger" while their cursor sits on a specific frame, and the LLM operates on the wrong layer (or the page root, or a misnamed sibling).
2. **Layers are unnamed (`Frame 152`, `Rectangle 31`).** Without semantic names, the LLM can't reason about what each layer *is*, so it can't make accurate CSS layer mappings or component proposals.
3. **Designs ship as a flat pile of layers.** A Figma file with no components is technically valid but practically unmaintainable — the LLM has no `Button` symbol to reuse, just 47 individual rounded rectangles with text inside.

This skill addresses all three. The four sub-guides above are how. **This document is the entry point that tells the agent which sub-guide to enter.**

---

## 1 · MCP-aware vs MCP-absent paths

The skill supports both:

| Environment | What "the agent reads from Figma" looks like |
|---|---|
| **Figma MCP available** (e.g., the user has a Figma MCP server running and exposes tools like `figma_get_selection`, `figma_get_node`, `figma_get_file`, `figma_set_node_name`) | Direct programmatic read/write. The agent can pull selection state, walk the layer tree, propose names, and apply changes via tool calls. |
| **Figma MCP absent** | The user manually copies a Figma share link or paste the JSON of a node, or the user takes a screenshot of the current selection. The agent works from that user-provided artifact and writes proposed changes back as instructions for the user to apply. |

Each sub-guide marks both paths in its workflow. The agent **detects which environment is available** by looking for tool names matching `figma_*` in the available toolset. If none, fall back to the manual path.

> **Security**: Figma MCP runs locally over its own protocol, not via the `curl` allowlist in `references/security-config.md`. Adding a Figma MCP doesn't require updating the security config. But if any workflow downloads asset URLs returned by Figma (e.g., exported PNG hosted on `figma-alpha-api.s3.us-west-2.amazonaws.com`), those URLs go through the standard allowlist gate — add the host to `security-config.md` §1.2 first.

---

## 2 · Triggering each sub-guide

When the user is mid-Figma workflow, route to the right sub-guide based on the user's request:

| User said something like… | Route to |
|---|---|
| "fix this layer" / "change the button" / "this should be bigger" | `figma-selection-aware.md` — confirm what "this" is first |
| "the layers are all `Frame 47` / `Rectangle 31`" / "rename these so I can find them" | `figma-layer-naming.md` |
| "this button is everywhere — can it be a component?" / "componentize this" / "extract" | `figma-component-grouping.md` |
| "pull the colors from our Figma library" / "import design tokens" / "set up the brand-spec from Figma" | `figma-brand-spec-import.md` |
| Two or more of the above | walk them in this order: import brand-spec first → name layers → group into components → then make selection-aware edits |

If the user's request is ambiguous, ask. Don't guess between "rename" and "componentize" — the answer changes the work.

---

## 3 · The shared confirmation principle

Every sub-guide ends a chunk of work with one explicit confirmation step. This is the hardest single change vs the upstream skill, which tended to bulk-edit and then summarize at the end. In Figma work that pattern fails because:

- The user's mental model is a specific layer; the LLM's mental model is text. They diverge silently.
- One bad rename or one bad re-grouping is hard to undo (Figma history is per-action; bulk LLM edits become one giant action).

So: every workflow proposes its changes as a list, lets the user confirm or edit the list, **then** applies. Granularity per guide:
- Selection-aware: confirm "is this the layer?" before any edit.
- Layer naming: propose 5–20 name renames in a table, let the user accept/reject each row before applying.
- Component grouping: propose component candidates with a screenshot and 3 hits per candidate, let the user pick which to commit.
- Brand-spec import: propose the diff against `team-brand-spec.json`, let the user accept whole or per-key.

Never apply silently. The whole point of this Phase is to remove the "agent operates on the wrong thing" failure mode — confirmation is the mechanism.

---

## 4 · Output of every Figma workflow

When a Figma workflow ends, the deliverables are some subset of:

1. **Renamed Figma layers** (if `figma_set_node_name` was used)
2. **New Figma components** (if `figma_create_component` was used)
3. **`team-brand-spec.json` updates** committed to the project repo
4. **A markdown report** under `assets/figma-reports/<date>-<workflow>.md` recording what was changed, with screenshots of before/after where applicable

The markdown report is required even when MCP did the changes directly — it makes the work auditable and reversible. Template:

```markdown
# Figma <workflow-name> · 2026-MM-DD

## What ran
- Workflow: layer-naming / component-grouping / selection-edit / brand-spec-import
- Figma file: <link>
- Page: <name>
- MCP available: yes/no

## Selection at start
<screenshot of the selected node tree>

## Proposed changes
<table of before → after>

## User decision
<which rows accepted, rejected, modified>

## Applied changes
<final list of what was actually committed>
```

---

## 5 · Relationship to other skill workflows

Figma is **upstream** of the rest of the skill. Most workflows assume `team-brand-spec.json` exists and accurate — `figma-brand-spec-import.md` is how that file gets populated. Most prototype work assumes the designer has a Figma source — `figma-selection-aware.md` is how iteration happens between Figma and the prototype HTML.

So a typical engagement looks like:

1. **Once per project**: `figma-brand-spec-import.md` — set up the spec
2. **Once at file creation**: `figma-layer-naming.md` and `figma-component-grouping.md` — clean up the file
3. **Continuously during iteration**: `figma-selection-aware.md` — the everyday workflow

Sub-guide details follow in their own files. Read this hub doc first, then jump to the relevant one.

---

**Owner**: Internal design platform team
**Last reviewed**: 2026-05-08
**Related**: `PROJECT-PLAN.md` Phase 3 · `team-brand-spec.example.json` · `security-config.md` (allowlist for Figma asset hosts)
