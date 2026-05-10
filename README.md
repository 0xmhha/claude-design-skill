# claude-design-skill

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![sanitizers](https://github.com/0xmhha/claude-design-skill/actions/workflows/sanitizers.yml/badge.svg)](https://github.com/0xmhha/claude-design-skill/actions/workflows/sanitizers.yml)

> Claude Code-based design skill for hi-fi prototyping and Figma MCP-driven precision design work.
> **Status: Step 1–4 shipped · 2026-05-10 · clean-room rewrite, no upstream skill inherited.**
> CI: GitHub Actions on every push and PR. 18 + 13 + 19 + 19 + 9 regression tests across the five sanitizer / engine / fork-helper suites; 16 prebuilt visual showcases under `assets/showcase-brand/generated/`.

> 🟡 **If you're an AI agent picking this repo up in a fresh session, read [`HANDOFF.md`](HANDOFF.md) FIRST.** It contains the project context, the user's working style, the anti-patterns to avoid, and the decision tree for the next move. Skipping it costs tokens.

## What this is

A skill package for Claude Code (and any markdown-skill-capable agent) that turns a design brief into hi-fi HTML prototypes, Figma-driven precision edits, and brand-correct illustrations through Codex CLI + gpt-image-2 — with security gates baked in at every boundary.

Three load-bearing rules govern every external call:

1. **Fact verification before assumptions.** WebSearch is the first action on any unfamiliar product, version, or release date. No memory-based factual claims.
2. **Confidentiality gate before any external call.** Internal codenames, NDA partners, unreleased products never leave the local agent — not via WebSearch, not via Codex CLI, not via image-gen prompts. Pattern table in `references/security-config.md §1.5`.
3. **Strip-then-scan import gate** for every external asset. SVGs go through whitelist sanitize + CSP + visibility comment. PNGs go through chunk scan + AI metadata strip. Sanitizer rejection is never silent — every reject lands in PROVENANCE.

## What's in here

```
claude-design-skill/
├── HANDOFF.md                        # ⭐ READ FIRST in a new session — context briefing + anti-patterns
├── SKILL.md                          # main agent doc — workflows, App / Slide / Anti-slop / Junior Designer / Tweaks / Critique sections
├── README.md                         # this file
├── LICENSE                           # Apache-2.0
├── NOTICE                            # required by Apache §4(d) — clean-room rewrite attribution
├── SECURITY.md                       # vulnerability disclosure policy (private advisories)
├── CONTRIBUTING.md                   # fork operator / security reporter / rare-PR paths
├── CHANGELOG.md                      # release log
├── PROJECT-PLAN.md                   # decision log
├── .gitignore                        # also names the showcase-pack exception
├── .github/
│   ├── workflows/
│   │   └── sanitizers.yml            # CI on every push + PR
│   └── dependabot.yml                # auto-update pinned GitHub Actions weekly
├── .githooks/
│   └── pre-commit                    # opt-in local equivalent: SVG sanitize + asset scan on staged files
├── references/                       # task-specific guides
│   ├── security-config.md            # allowlist · WebSearch policy · Codex policy · codename pattern catalog
│   ├── svg-sanitize.md               # XXE guard · whitelist · CSP · visibility comment
│   ├── production-boundaries.md      # prototype ↔ production migration table
│   ├── codex-design-workflow.md      # GPT-5.5 + gpt-image-2 with strip-then-scan import
│   ├── figma-workflow.md             # Figma MCP hub
│   ├── figma-selection-aware.md      # confirm what 'this layer' is before editing
│   ├── figma-layer-naming.md         # rename Frame 47 → semantic
│   ├── figma-component-grouping.md   # detect repeats and promote to components
│   ├── figma-brand-spec-import.md    # Figma → team-brand-spec.json
│   ├── brand-spec-fields.md          # field reference for team-brand-spec.example.json
│   ├── ci-template.md                # live GitHub workflow + alternate-platform snippets
│   ├── design-styles.md              # 18-direction design philosophy catalog (14 fresh + 4 game/web3 carry-over)
│   ├── scene-templates.md            # 9 output-type templates (5 fresh + 4 game/web3 carry-over)
│   ├── animation-engine.md           # <Stage> / <Sprite> reference + worked examples
│   ├── animation-best-practices.md   # 5-tier timing scale, easing selection, stagger, reduced-motion
│   └── animation-pitfalls.md         # 14 anti-patterns with why-bad / symptom / fix
├── scripts/
│   ├── svg-sanitize.py               # whitelist-based SVG sanitizer (stdlib only)
│   ├── test_svg_sanitize.py          # 18 regression tests
│   ├── scan_assets.py                # PNG chunk + JPG segment scanner (stdlib only)
│   ├── test_scan_assets.py           # 13 regression tests
│   ├── codex-image-import.py         # Codex PNG → strip caBX → scan → import (with conservative-pairing codename catalog)
│   ├── test_codex_image_import.py    # 19 regression tests
│   ├── test_animations_easing.js     # 19 regression tests for the Easing pack (Node, stdlib only)
│   └── install-hooks.sh              # opt-in pre-commit hook installer
├── assets/
│   ├── team-brand-spec.example.json  # team brand-spec template
│   ├── ios_frame.jsx                 # iPhone 15 Pro / Pro Max device frame
│   ├── android_frame.jsx             # Pixel 8 / 8 Pro device frame
│   ├── deck_stage.js                 # <deck-stage> 1920×1080 web component
│   ├── tweaks.js                     # <tweak-panel> live design-tuning controls
│   ├── animations.jsx                # Stage / Sprite timeline engine
│   ├── easing.js                     # 14-curve frozen Easing pack (CommonJS + window)
│   └── showcase-brand/
│       ├── PROVENANCE.md             # 213-line audit trail for the 16 showcase PNGs
│       └── generated/                # 16 prebuilt visual demos (gpt-image-2)
└── examples/
    ├── dot-claude-settings.json      # drop-in Claude Code permissions baseline
    ├── tweaks-demo.html              # runnable <tweak-panel> example
    └── README.md                     # how to wire up the settings
```

Run the full guard chain locally:

```bash
python3 scripts/test_svg_sanitize.py        # 18/18
python3 scripts/test_scan_assets.py         # 13/13
python3 scripts/test_codex_image_import.py  # 19/19
node    scripts/test_animations_easing.js   # 19/19
python3 -c "import json; json.load(open('examples/dot-claude-settings.json'))"
python3 -c "import json; json.load(open('assets/team-brand-spec.example.json'))"
```

GitHub Actions runs the same chain on every push and PR.

## Quick start

```bash
# Clone (replace URL with your internal git host once mirrored)
git clone <repo-url> claude-design-skill
cd claude-design-skill

# Wire the settings.json baseline into your project
cp examples/dot-claude-settings.json /path/to/your-project/.claude/settings.json
# then remove the _template_meta block from settings.json

# (optional) install the pre-commit hook so staged SVGs / PNGs are gated locally
./scripts/install-hooks.sh
```

Then talk to your agent (Claude Code, Cursor, Trae, or any markdown-skill-capable host):

```
"Pull the brand colors from this Figma library and update team-brand-spec.json"
"Componentize this Figma file — too many ad-hoc rounded buttons"
"Generate a hero image for our staking flow with codex"
"Sanitize this external SVG before I inline it"
```

## What ships (vs what's intentionally out of scope)

**In the box (Step 1–4 shipped, 2026-05-10):**
- Security gates · sanitizers · Figma MCP routing · Codex CLI bridge with strip-then-scan import (Step 1)
- SKILL.md body: Junior Designer workflow · Anti-AI-slop checklist (12 patterns) · App prototype rules (`<IosFrame>` + `<AndroidFrame>`) · Slide deck conventions (`<deck-stage>`) · Tweaks live-tuning system (`<tweak-panel>`) · Critique guide (6 dimensions, threshold rule, worked critique) (Step 2)
- Design knowledge catalog: 18-direction design philosophy catalog · 9 scene templates · Stage / Sprite animation engine + 14-curve Easing pack · animation best-practices + pitfalls · 16 prebuilt visual showcases (Step 3)
- Internal-fit hardening: codename pattern catalog with conservative-pairing rule · GitHub Actions CI · external asset hosts whitelist (Step 4)

**Intentionally out of scope:**
- **Sound effects (Step 3.5)** — retired by user instruction 2026-05-10. This project is visual-only; deliverables that need sound source it per-deliverable rather than vendoring an SFX pack here.
- **Internal brand integration (Step 4 fork-specific)** — `team-brand-spec.json` real values, internal codenames added to the pattern list, internal asset hosts added to the allowlist. These are per-fork actions; the templates live in this repo (`references/brand-spec-fields.md`, `references/security-config.md §1.2`, `scripts/codex-image-import.py:DEFAULT_CODENAME_PATTERNS`).

## License

**Apache License 2.0**, recorded in `LICENSE`. Per Apache §4(d), the
attribution `NOTICE` file ships alongside.

This repository is a **clean-room rewrite**. No third-party design skill
is inherited — every file is either authored from scratch by the project
maintainer or is the maintainer's own prior fork-author work
(`0xmhha/huashu-design`, Phase 1–4.2). The 23 carry-over files are
enumerated in `PROJECT-PLAN.md §2`; the verbatim game / web3 domain
sections inside `references/design-styles.md §15–18` and
`references/scene-templates.md §06–09` are similarly maintainer-original
work, documented in `PROJECT-PLAN.md §7`.

The upstream `alchaincyf/huashu-design` skill carries a separate
Personal-Use license. This repository does **not derive from** the
upstream, so the upstream license is unaffected by the Apache 2.0 grant
recorded here. The license was changed from MIT to Apache 2.0 on
2026-05-10 to gain the explicit patent grant (Apache §3) and the
contributor / trademark clarity (Apache §6) that MIT does not provide.

If a fork operator needs a different license (internal-only,
source-available, etc.), replace `LICENSE` and `NOTICE` before any
external publication.

## Roadmap

- **v0.1.0-alpha (2026-05-09)** — skeleton: security gates, sanitizers, Figma MCP routing, Codex bridge, Android frame.
- **Step 2 (2026-05-09 → 05-10)** — SKILL.md body authored: Junior Designer workflow · Anti-AI-slop checklist · App prototype rules + IosFrame · Slide deck conventions + deck_stage.js · Tweaks live-tuning system + tweaks.js + worked example · Critique guide.
- **Step 3 (2026-05-10)** — Design knowledge catalog: design-styles.md (18 directions) · scene-templates.md (9 templates) · animation engine (animations.jsx + easing.js + 19 regression tests) · animation best-practices + pitfalls · 16 showcase PNGs. (Step 3.5 SFX library retired by user instruction.)
- **Step 4 (2026-05-10)** — Internal-fit hardening: codename catalog conservative-pairing rule · GitHub Actions CI active · external asset hosts whitelist boost. Internal brand spec values + LICENSE / mirror policy remain per-fork actions.
- **Next** — designer dogfooding pass · per-fork brand integration when a team adopts the skill.

## Contributing

Internal R&D. External contributions are not currently sought. If you
have a fix or improvement, read [`CONTRIBUTING.md`](CONTRIBUTING.md)
first — it covers the fork-operator path, the security-reporter path,
and the rare-PR path.

For security regressions in the sanitizer / scanner / import-gate /
codename catalog stack, use GitHub's private security advisories
(see [`SECURITY.md`](SECURITY.md)) rather than opening a public issue.
