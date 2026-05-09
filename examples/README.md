# Examples · ready-to-copy templates

Copy-paste starting points for the most common per-project setup tasks.

| File | Drop into | Purpose |
|---|---|---|
| `dot-claude-settings.json` | `<your-project>/.claude/settings.json` | Harness-level security baseline — `deny` for `yt-dlp` / `wget` / unrestricted `curl`; `ask` per-call for allowlisted hosts and `WebSearch`. Mirrors `references/security-config.md` §3. |

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
