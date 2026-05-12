# Quickstart · 15 minutes from clone to first design

> Designer- and adopter-facing walkthrough. Hardened defaults are already
> shipped in the skill (Step 5 evidence-anchored values + Default Studio
> identity); this guide is the steps **each user runs** to apply them on
> their own machine.
>
> Reference docs (read on demand): `README.md` · `references/security-config.md`
> · `references/figma-workflow.md` · `references/figma-mcp-setup.md`.

---

## Who this is for

Three audiences, three different "first 15 minutes":

| Audience | Goal | Section |
|---|---|---|
| **Individual designer / agent user** | Drop the skill into one project, get a Default Studio render | §1 → §5 |
| **Team lead onboarding 5–20 designers** | Same setup, *repeatable* per teammate, including the Figma MCP | §1 → §5 → §6 *Team rollout* |
| **Read-only reviewer** (no Claude Code seat) | Just inspect the artefacts, run the test suite, view a sample | §7 *Read-only verification path* |

---

## §0 · Prerequisites (≈2 minutes)

Check once per machine:

```bash
# Python 3.10+ (stdlib only; no pip install)
python3 --version   # expect 3.10 or newer

# Node 22+ (for the easing regression suite)
node --version      # expect v22 or newer

# Claude Code (or compatible markdown-skill host)
claude --version    # any recent version
```

Optional but recommended:

```bash
# git (for clone + future updates)
git --version

# A modern browser (to open the figma-viewer output)
# Any one of: Chrome, Safari, Firefox, Edge
```

---

## §1 · Clone + verify (≈2 minutes)

```bash
# Pick a stable home for skill repos. ~/skills/ is a convention.
mkdir -p ~/skills
git clone https://github.com/0xmhha/claude-design-skill ~/skills/claude-design-skill
cd ~/skills/claude-design-skill

# Run the full guard chain locally. This proves your environment can
# run every sanitiser the CI gates on — *before* you wire the skill
# into any project.
python3 scripts/test_svg_sanitize.py        # 18 tests
python3 scripts/test_scan_assets.py         # 13 tests
python3 scripts/test_codex_image_import.py  # 19 tests
node    scripts/test_animations_easing.js   # 19 tests
python3 scripts/test_init_brand.py          # 11 tests
python3 scripts/test_figma_to_brand_spec.py # 13 tests
python3 scripts/test_figma_viewer.py        # 15 tests
# Expected: 108 / 108 OK across the 7 suites.
```

If any suite fails, **stop** and check `python3 --version` / `node --version`.
The suites are stdlib-only — no `pip install`, no `npm install`, so a
failure means your interpreter version is below the supported floor.

---

## §2 · Smoke the Figma viewer (≈1 minute, no Figma account needed)

You can render a synthetic Figma file to a self-contained HTML page
*without a token* or *a Figma account*. This proves the viewer round-trips.

```bash
python3 scripts/figma-viewer.py \
  --fixture scripts/fixtures/figma_viewer_sample.json \
  --output /tmp/viewer.html

# macOS
open /tmp/viewer.html
# Linux
xdg-open /tmp/viewer.html
# Windows (WSL)
start /tmp/viewer.html
```

You should see a 2-page layout (Cover · Tokens) with a `#5B7CFA` accent
swatch, "Design that ships." headline, and a Tokens page with three
colour swatches. Press `→` / `←` to switch pages, `d` to toggle dark
chrome.

---

## §3 · Drop the skill into your design project (≈3 minutes)

```bash
cd /path/to/your-design-project   # NOT the skill repo

# Security baseline (denies yt-dlp / wget / unrestricted curl,
# asks per-call for allowlisted hosts)
mkdir -p .claude
cp ~/skills/claude-design-skill/examples/dot-claude-settings.json \
   .claude/settings.json

# Remove the _template_meta block — JSON has no comments.
$EDITOR .claude/settings.json

# Optional: install the pre-commit hook so staged SVG / PNG go through
# the sanitiser before they enter a commit
~/skills/claude-design-skill/scripts/install-hooks.sh
```

What you just enabled:

- **denied outright**: `yt-dlp`, `youtube-dl`, unrestricted `curl`, `wget`.
- **ask-per-call**: `curl` to the 5 allowlisted hosts (Lucide CDN ×2,
  Phosphor CDN ×2, MDN), `WebSearch`.
- **never silent**: every external call now prompts you.

Verify:

```
In your agent, say: "Run: curl https://example.com -o test.html"
The agent should refuse or ask. If it silently fetches, the settings
file isn't being read — check that the path is exactly
`.claude/settings.json` relative to where the agent is launched.
```

---

## §4 · Stamp your team's brand spec (≈3 minutes)

The skill ships an *operational* Default Studio identity. You override
the identity slots and inherit the evidence-anchored token defaults
(11-service style sweep — `references/web3-game-style-stats.md`).

```bash
cd /path/to/your-design-project

# Stamp the default carrier into your project root
python3 ~/skills/claude-design-skill/scripts/init-brand.py
# → writes team-brand-spec.json (_meta / _note guidance blocks stripped)

$EDITOR team-brand-spec.json
```

Override the **identity slots** (the rest of the file already ships
sensible defaults):

| Field | Replace with |
|---|---|
| `team.company` | Your real company name |
| `team.division` | Your division / studio |
| `brand.name` | Your brand name (1–2 words) |
| `brand.tagline_short` | One-line product tagline (≤ 8 words) |
| `brand.tone_keywords` | 3–5 voice descriptors |
| `logo.primary` | Path to your team's logo SVG (run through `svg-sanitize.py` first) |
| `colors.accent.primary` | Your real brand accent hex (default `#5B7CFA` is deliberately neutral — not anyone's brand) |

Verify the result is still valid JSON:

```bash
python3 -c "import json; json.load(open('team-brand-spec.json'))" && echo "OK"
```

---

## §5 · First deliverable (≈2 minutes)

Talk to the skill via your agent (Claude Code, Cursor, Trae, any
markdown-skill host) — try one of these prompts:

```
"Read team-brand-spec.json and tell me what's overridden vs default."
"Generate a hero image for our staking flow with codex." (requires Codex CLI)
"Sanitize this external SVG before I inline it." (drop the SVG path)
"Componentize this Figma file — too many ad-hoc rounded buttons." (requires Figma MCP — §6)
```

If the agent does the right thing on the first prompt, you're done. If
the skill isn't picked up, the agent doesn't know about the brand spec
— check that `team-brand-spec.json` is in the same directory the agent
is launched from.

---

## §6 · Team rollout (5–20 designers)

The setup above is **per-machine + per-project**. For a team:

1. **Mirror the skill repo to your internal git host.** Each teammate
   clones from there, not from `0xmhha/claude-design-skill`, so internal
   additions (codename patterns, internal asset hosts) live in one place.
   See `CONTRIBUTING.md §For fork operators / Mirror to your internal git host`.
2. **Ship a single `team-brand-spec.json`.** Commit it to your design
   project repo (not the skill repo). Every teammate inherits the same
   identity overrides — they only need to clone the project.
3. **Wire the Figma MCP server** if your workflow involves Figma editing.
   See `references/figma-mcp-setup.md` — the team-lead needs to issue a
   *service* Figma PAT, wire `FIGMA_API_KEY` into each teammate's
   Claude config, and verify with the *smoke* in §4 of that doc.
4. **Optional: install via Claude Code plugin** (when adopting the
   plugin form). After your internal mirror is up:

   ```bash
   # If a prior version of the marketplace is registered, remove it first
   claude plugin marketplace remove claude-design-skill 2>/dev/null || true

   # Each teammate runs:
   claude plugin marketplace add 0xmhha/claude-design-skill
   #   (or your internal mirror: <your-internal-git-host>/claude-design-skill)
   #   marketplace.json source.ref pins v1.0.0 — the install resolves to
   #   that git tag, not master. Upgrading to a future v1.x release
   #   requires the maintainer to bump source.ref and re-publish; adopters
   #   then re-run `marketplace add` to refresh the pin.
   claude plugin install claude-design-skill
   ```

   The plugin's `.claude-plugin/plugin.json` + `marketplace.json` are
   in the repo root. The marketplace's plugin entry uses a
   `github` source pointing at this repo, so `marketplace add` may
   accept either a `owner/repo` shorthand or a full git URL.

   **Troubleshooting**:
   - *"This plugin uses a source type your Claude Code version does
     not support"*: run `claude --version`. Versions before 2.1.x do
     not recognise the `url` source form. Upgrade Claude Code or
     fall back to manual setup (§3 + §4).
   - *"ssh: connect to host github.com port 22: Operation timed out"*
     or *"Failed to clone repository"*: your network blocks outbound
     SSH (port 22). The marketplace ships with an HTTPS `url` source
     to work around this — if you still see the SSH error, your local
     git is rewriting `https://` URLs to `git@github.com:` via
     `insteadOf`. Run `git config --global --get-all url.git@github.com:.insteadOf`
     and remove any matching rule, or override per-clone with
     `git config --global url.https://github.com/.insteadOf git@github.com:`
     (HTTPS-first).

5. **CI for the design project.** If your design project (not the skill
   repo) ships its own CI, copy the matching snippet from
   `references/ci-template.md` so every PR lint-checks
   `team-brand-spec.json` and (if applicable) re-runs `figma-viewer.py`
   against latest pages. The 7-suite chain runs in ~30 seconds on
   GitHub-hosted runners; identical on GitLab / Bitbucket / Buildkite
   via the snippets in that doc.

---

## §7 · Read-only verification path (no Claude Code seat needed)

If you're reviewing the skill but don't intend to *use* it as an agent
extension, you can still verify everything:

```bash
git clone https://github.com/0xmhha/claude-design-skill /tmp/skill-review
cd /tmp/skill-review

# 1. Read the docs in this order
less README.md                       # 1-page overview + directory tree
less HANDOFF.md                      # session-handoff briefing
less PROJECT-PLAN.md                 # decisions log §7
less SKILL.md                        # the actual skill body

# 2. Run all 108 tests (proves the gates work)
python3 scripts/test_svg_sanitize.py
python3 scripts/test_scan_assets.py
python3 scripts/test_codex_image_import.py
node    scripts/test_animations_easing.js
python3 scripts/test_init_brand.py
python3 scripts/test_figma_to_brand_spec.py
python3 scripts/test_figma_viewer.py

# 3. Visual smoke on the Figma viewer (no token needed)
python3 scripts/figma-viewer.py \
  --fixture scripts/fixtures/figma_viewer_sample.json \
  --output /tmp/viewer.html
open /tmp/viewer.html
```

You now have everything to make a yes/no adoption decision: the
sanitiser surface, the evidence trail behind the defaults, the test
guarantees, and a running viewer.

---

## §8 · Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `python3 scripts/test_*.py` reports `Ran 0 tests` | wrong CWD | `cd` into the skill repo root before running |
| `node scripts/test_animations_easing.js` errors with `SyntaxError` | Node version < 22 | install Node 22+ via `nvm install 22` |
| `init-brand.py` exits with `target already exists` | a prior `team-brand-spec.json` is in the project root | re-run with `--force`, or pick a different `--target` |
| `figma-viewer.py` writes the file but opens to a blank page | the browser cached an older viewer.html | hard-reload the page (`Cmd+Shift+R`) or output to a fresh path |
| Agent silently fetches `curl https://example.com` | `.claude/settings.json` not loaded | check the path is relative to the agent's launch CWD |
| Figma MCP tools (`figma_*`) don't appear | server config not loaded | see `references/figma-mcp-setup.md §4 Verifying detection works` |
| `python3 scripts/test_figma_to_brand_spec.py` fails on a fresh machine | the OS shipped a Python older than 3.10 | install via `pyenv` / `brew install python@3.10` |

---

## §9 · Where to go from here

- `SKILL.md` — full skill body (Junior Designer workflow, Anti-AI-slop
  checklist, App prototype rules, Slide deck conventions, Tweaks live-
  tuning, Critique guide).
- `references/figma-workflow.md` — Figma routing hub.
- `references/codex-design-workflow.md` — Codex CLI + gpt-image-2.
- `CONTRIBUTING.md` — fork operator path (mirror + LICENSE + CI port).
- `PROJECT-PLAN.md §7` — decisions log (every design choice's *why*).
- `references/web3-game-style-stats.md` — the 11-service evidence
  behind every default value.
