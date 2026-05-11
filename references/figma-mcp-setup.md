# Figma MCP server · setup + detection · reference

> The skill's Figma workflows (`figma-workflow.md`, `figma-selection-aware.md`,
> `figma-layer-naming.md`, `figma-component-grouping.md`) all *assume* a Figma
> MCP server is attached to the agent. This doc covers (a) how an adopter
> connects one, (b) how the skill detects whether it's available, and (c)
> what falls back to manual when it's not.

---

## 1 · What is Figma MCP

Figma MCP servers expose the Figma REST + Plugin APIs to LLM agents through
the Model Context Protocol. The skill calls them via tool names matching
`figma_*` (e.g. `figma_get_selection`, `figma_set_node_name`,
`figma_create_component`).

There are several public implementations. Pick one and follow its install
docs; this guide is *contract-level* (which tool names must exist, what
auth flow the skill expects), not implementation-specific.

| Implementation | Repo / docs | Notes |
|---|---|---|
| `framelink-figma-mcp` | <https://github.com/GLips/Figma-Context-MCP> | Most common Claude Desktop integration; uses Personal Access Token |
| Figma's own Dev Mode MCP | <https://help.figma.com/hc/en-us/articles/32132100833559> | Built into Figma Dev Mode (paid seats) |
| Other community servers | various | Look for one that publishes the `figma_*` tool surface this skill expects |

---

## 2 · Authentication

All known Figma MCP servers use a **Personal Access Token (PAT)** — the same
token used by `scripts/figma-to-brand-spec.py` and `scripts/figma-viewer.py`.

### Generate a token

1. Open <https://www.figma.com/developers/api#access-tokens> in a browser.
2. Click *Get personal access token* (or *Create new token*).
3. Scopes: **read** is sufficient for view-only workflows
   (`figma-viewer.py`, `figma-to-brand-spec.py`, selection inspection).
   **read + write** is required for renaming layers, creating components,
   editing nodes (Step 3 / Step 4 of the SKILL.md Figma section).
4. Copy the token immediately — Figma shows it only once.

### Store the token safely

- **Never commit** the token to a repo. Add a project-local `.env` (already
  in `.gitignore`) or an OS keychain entry.
- **Rotate after sensitive work**: when a contract ends, when a teammate
  leaves, when you suspect leak.
- **Don't reuse personal-account tokens for production agents** — create a
  dedicated *service* Figma account if the workflow runs unattended.

### Wire it into the MCP server

Most servers expect `FIGMA_API_KEY` (sometimes `FIGMA_TOKEN`) in env. Add
to your Claude Desktop / Claude Code MCP config:

```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["-y", "figma-developer-mcp", "--stdio"],
      "env": {
        "FIGMA_API_KEY": "<YOUR_FIGMA_PERSONAL_ACCESS_TOKEN>"
      }
    }
  }
}
```

(Adjust `command` / `args` to match the implementation you chose. The
`env.FIGMA_API_KEY` line is the contract.)

Restart the agent process after editing the config.

---

## 3 · Detection (skill side)

Before any Figma workflow step, the skill checks whether MCP is attached
and routes accordingly. The current pattern (see `SKILL.md §Figma workflow`
and `figma-workflow.md §1`):

1. **Inspect the available tool list** for names matching `figma_*`.
2. If at least `figma_get_selection` (or `figma_get_node`) exists, the
   skill routes to the **MCP-aware** path — direct API calls, with the
   user confirming destructive operations before they fire.
3. If no `figma_*` tools exist, the skill routes to the **MCP-absent**
   path — the agent produces *instructions* the user applies manually in
   Figma desktop / web (e.g. "rename these 12 layers as follows…",
   "promote this repeated frame to a component"), plus screenshots if
   any are exchanged.

### Detection contract (what skill code expects)

| Tool name | Severity | What the skill assumes about it |
|---|---|---|
| `figma_get_selection` | **required for MCP path** | returns the currently-selected node(s) in the active Figma file |
| `figma_get_node` | **required for MCP path** | returns a node's tree given an id; supports `depth=-1` for full tree |
| `figma_export_image` | optional | returns a PNG / JPG / SVG of a node; used for visual confirmation |
| `figma_set_node_name` | required for *naming* workflows | renames a node (`figma-layer-naming.md`) |
| `figma_set_node_size` / `figma_set_node_fill` / `figma_set_node_text` | optional | direct edits (`figma-selection-aware.md`) |
| `figma_create_component` | required for *componentization* | promotes a frame to a component (`figma-component-grouping.md`) |
| `figma_replace_with_instance` | optional | replaces a frame with a component instance |
| `figma_combine_as_variants` | optional | combines components into a variant set |

If only `figma_get_selection` + `figma_get_node` exist, the skill can
*read* Figma but proposes edits as instructions, not direct API calls.

---

## 4 · Verifying detection works

Quick smoke after install:

1. Open Figma desktop / web, select any node.
2. In your agent, say: *"What's selected in Figma right now?"*
3. The agent should answer with a node id + name (MCP available) or with
   "I don't have a Figma MCP attached; please paste a screenshot or the
   selection JSON" (MCP absent).

If the agent claims MCP is unavailable when it should be:

- Re-check the env: `echo $FIGMA_API_KEY` (must not be empty).
- Re-check the config JSON syntax (one missing comma breaks loading).
- Re-check the MCP server logs (most implementations log to stderr; check
  the agent host's MCP log path).
- Try the server's own smoke (`npx -y figma-developer-mcp --stdio` and
  send a `tools/list` request manually).

---

## 5 · Network + confidentiality posture

- Figma MCP servers **call Figma's API over HTTPS** with your PAT. That
  traffic stays between the MCP server and `api.figma.com`; the skill
  agent only sees the structured JSON the MCP server returns.
- Files you ask the agent to read **may include internal codenames /
  NDA / unreleased product names**. The confidentiality gate in
  `references/security-config.md §1.5` and
  `scripts/codex-image-import.py:DEFAULT_CODENAME_PATTERNS` still apply:
  before *forwarding* anything from Figma to WebSearch / Codex / external
  tooling, scan for codename patterns.
- The MCP server itself does **not** trigger `curl` / `wget` /
  `yt-dlp`-style external fetches. Asset URLs returned by Figma (e.g.
  `figma-alpha-api.s3.us-west-2.amazonaws.com`) only get fetched when
  *the skill* (or `figma-viewer.py` / `figma-to-brand-spec.py`) chooses to
  call them — and those calls go through the allowlist gate in
  `references/security-config.md §1.1`.

---

## 6 · Fallback path (MCP absent)

When the skill can't see `figma_*` tools, it doesn't refuse — it switches
modes:

| Workflow | MCP-aware path | MCP-absent path |
|---|---|---|
| Read selection (`figma-selection-aware.md`) | `figma_get_selection` + `figma_get_node` | User pastes Figma share link + screenshot; agent asks clarifying questions |
| Layer renaming (`figma-layer-naming.md`) | `figma_set_node_name` batch | Agent emits a rename plan (`Frame 47 → Hero / Background`, …) the user applies via Figma Selection → Right-click → Rename |
| Componentization (`figma-component-grouping.md`) | `figma_create_component` / `figma_replace_with_instance` | Agent emits the candidate list + instructions ("convert the 3 'Card 1', 'Card 2', 'Card 3' frames to a component named Card; replace the other 7 visually-matching frames with instances") |
| Brand spec extraction | `scripts/figma-to-brand-spec.py` (uses REST directly, doesn't need MCP) | same — script doesn't depend on MCP |
| Visual review | `scripts/figma-viewer.py` (uses REST directly) | same — script doesn't depend on MCP |

Note: `figma-to-brand-spec.py` and `figma-viewer.py` are **independent of
MCP**. They call the Figma REST API directly with a PAT, so adopters can
run them even when an MCP server isn't set up.

---

## 7 · Related

- `references/figma-workflow.md` — workflow hub, routing table.
- `references/figma-selection-aware.md` — confirm selection before editing.
- `references/figma-layer-naming.md` — batch rename workflow.
- `references/figma-component-grouping.md` — repeat detection + componentize.
- `references/figma-page-organization.md` — page / folder / group cleanup.
- `references/figma-brand-spec-import.md` — design tokens → `team-brand-spec.json`.
- `references/figma-to-brand-spec.md` + `scripts/figma-to-brand-spec.py` — REST extractor (MCP-independent).
- `references/figma-viewer.md` + `scripts/figma-viewer.py` — REST viewer (MCP-independent).
- `references/figma-image-export.md` — Codex PNG → Figma placement.
