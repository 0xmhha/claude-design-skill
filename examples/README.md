# Examples · ready-to-copy templates

Copy-paste starting points for the most common per-project setup tasks.

| File | Drop into | Purpose |
|---|---|---|
| `dot-claude-settings.json` | `<your-project>/.claude/settings.json` | Harness-level security baseline — `deny` for `yt-dlp` / `wget` / unrestricted `curl`; `ask` per-call for allowlisted hosts and `WebSearch`. Mirrors `references/security-config.md` §3. |
| `tweaks-demo.html` | open in any browser (or serve over `python3 -m http.server`) | Runnable worked example for the `<tweak-panel>` live-tuning component (`assets/tweaks.js`). Three knobs (palette · density · accent) drive five CSS variables on a real layout. Press `t` to reveal the panel. |

## Using `dot-claude-settings.json`

```bash
mkdir -p .claude
cp /path/to/internal-design-skill/examples/dot-claude-settings.json .claude/settings.json
$EDITOR .claude/settings.json   # remove the _template_meta block; add internal hosts
```

After copying:
1. **Remove the `_template_meta` block.** Strict JSON does not support comments; this object is a placeholder that the harness will ignore but should not stay long-term.
2. **Add internal hosts to `permissions.ask`** as needed (your design-system CDN, internal Figma export bucket, etc.). Mirror these additions in `references/security-config.md` §1.2.
3. **Restart the agent** so the new permissions take effect.

## What this file does

- `permissions.deny` is absolute — any matching command is rejected without a prompt.
- `permissions.ask` requires one explicit user approval per call. The user can decline at any prompt.
- `WebSearch(*)` under `ask` forces the user to confirm each search, so internal codenames cannot leak silently into a search-engine query log (see `SKILL.md` §0 confidentiality gate).

## Verifying

After copying, ask the agent something that should be blocked:
```
Run: curl https://example.com -o test.html
```
The agent should refuse (or ask) — not silently fetch. If it silently fetches, the settings file isn't being picked up. Check that the path is exactly `.claude/settings.json` relative to where the agent is launched.

## Using `tweaks-demo.html`

The demo links to `../assets/tweaks.js` directly, so you need to serve
the repo root (or the `examples/` directory's parent) for the relative
path to resolve:

```bash
cd /path/to/internal-design-skill
python3 -m http.server 8000
# then open http://127.0.0.1:8000/examples/tweaks-demo.html
```

Press `t` to toggle the floating panel; press `Esc` to close it. The
**Reset** button in the panel header clears the localStorage state and
restores the defaults. For the full API and the *when not to use it*
list, see `SKILL.md ## Tweaks live-tuning system` and the engine
reference at `assets/tweaks.js`.
