# claude-design-skill

> Claude Code-based design skill for hi-fi prototyping and Figma MCP-driven precision design work.
> **Status: v0.1.0-alpha · skeleton · 2026-05-09 · clean-room rewrite, no upstream skill inherited.**

> 🟡 **If you're an AI agent picking this repo up in a fresh session, read [`HANDOFF.md`](HANDOFF.md) FIRST.** It contains the project context, the user's working style, the anti-patterns to avoid, and the decision tree for the next move. Skipping it costs tokens.

## What this is

A skill package for Claude Code (and any markdown-skill-capable agent) that turns a design brief into hi-fi HTML prototypes, Figma-driven precision edits, and brand-correct illustrations through Codex CLI + gpt-image-2 — with security gates baked in at every boundary.

Three load-bearing rules govern every external call:

1. **Fact verification before assumptions.** WebSearch is the first action on any unfamiliar product, version, or release date. No memory-based factual claims.
2. **Confidentiality gate before any external call.** Internal codenames, NDA partners, unreleased products never leave the local agent — not via WebSearch, not via Codex CLI, not via image-gen prompts. Pattern table in `references/security-config.md §1.5`.
3. **Strip-then-scan import gate** for every external asset. SVGs go through whitelist sanitize + CSP + visibility comment. PNGs go through chunk scan + AI metadata strip. Sanitizer rejection is never silent — every reject lands in PROVENANCE.

## What's in here (v0.1.0-alpha skeleton)

```
claude-design-skill/
├── HANDOFF.md                        # ⭐ READ FIRST in a new session — context briefing + anti-patterns
├── SKILL.md                          # main agent doc (skeleton)
├── README.md                         # this file
├── LICENSE                           # MIT
├── CHANGELOG.md                      # release log
├── PROJECT-PLAN.md                   # decision log + Step 2/3 plan
├── .gitignore
├── .githooks/
│   └── pre-commit                    # opt-in: SVG sanitize + asset scan on staged files
├── references/                       # task-specific guides
│   ├── security-config.md            # allowlist · WebSearch policy · Codex policy · codename patterns
│   ├── svg-sanitize.md               # XXE guard · whitelist · CSP · visibility comment
│   ├── production-boundaries.md      # prototype ↔ production migration table
│   ├── codex-design-workflow.md      # GPT-5.5 + gpt-image-2 with strip-then-scan import
│   ├── figma-workflow.md             # Figma MCP hub
│   ├── figma-selection-aware.md      # confirm what 'this layer' is before editing
│   ├── figma-layer-naming.md         # rename Frame 47 → semantic
│   ├── figma-component-grouping.md   # detect repeats and promote to components
│   ├── figma-brand-spec-import.md    # Figma → team-brand-spec.json
│   ├── brand-spec-fields.md          # field reference for team-brand-spec.example.json
│   └── ci-template.md                # GitHub Actions / GitLab CI templates
├── scripts/
│   ├── svg-sanitize.py               # whitelist-based SVG sanitizer (stdlib only)
│   ├── test_svg_sanitize.py          # 18 regression tests
│   ├── scan_assets.py                # PNG chunk + JPG segment scanner (stdlib only)
│   ├── test_scan_assets.py           # 13 regression tests
│   ├── codex-image-import.py         # Codex PNG → strip caBX → scan → import
│   ├── test_codex_image_import.py    # 16 regression tests
│   └── install-hooks.sh              # opt-in pre-commit hook installer
├── assets/
│   ├── team-brand-spec.example.json  # team brand-spec template
│   └── android_frame.jsx             # Pixel 8 / 8 Pro mockup wrapper
└── examples/
    ├── dot-claude-settings.json      # drop-in Claude Code permissions baseline
    └── README.md                     # how to wire up the settings
```

47/47 tests green. `python3 scripts/test_svg_sanitize.py && python3 scripts/test_scan_assets.py && python3 scripts/test_codex_image_import.py`

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

## What's missing (intentionally)

The skill body — design philosophies, scene templates, animation rules, slide layouts, anti-AI-slop checklist — is **not** in this skeleton. The skeleton ships only what's already authored from scratch by this project's maintainer in a previous fork. Skill body sections are authored fresh in Step 2 / Step 3 (see `PROJECT-PLAN.md`).

Until those sections land, when the user asks for design direction the skill should ask for concrete references rather than propose from memory — Core Principle #0 still applies.

## License

MIT. See `LICENSE`.

This repository is a clean-room rewrite. No third-party design skill is inherited — every file is either authored from scratch by this project's maintainer or is the maintainer's own previous work carried over with attribution.

If your team needs a different license (internal-only, Apache 2.0, source-available), replace `LICENSE` before any external publication.

## Roadmap

- **v0.1.0-alpha (this release)** — skeleton: security gates, sanitizers, Figma MCP routing, Codex bridge, Android frame.
- **v0.2.0** — SKILL.md body authored: Junior Designer workflow, anti-AI-slop checklist, app prototype rules including iOS frame.
- **v0.3.0** — Design philosophy catalog (authored from scratch), scene templates (cover / slide / infographic / hero animation), critique guide.
- **v0.4.0** — Animation engine (Stage / Sprite) rewrite, slide deck conventions, Tweaks live-tuning.
- **v1.0.0** — Internal brand wired in, CI workflow active, designer dogfooding pass complete.

## Contributing

Internal R&D. External contributions are not currently accepted. If your team adopts this skill, fork it into your private git host and customize `team-brand-spec.json`, the codename pattern list in `references/security-config.md §1.5`, and the allowlist hosts in `references/security-config.md §1.2`.
