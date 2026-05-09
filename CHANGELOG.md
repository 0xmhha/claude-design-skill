# Changelog

All notable changes to this project are recorded here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

This project is a clean-room rewrite. The history is independent. See `PROJECT-PLAN.md` for the per-step decision log.

---

## [0.1.0-alpha] · 2026-05-09

### Initial skeleton

Skill skeleton with security gates, sanitizers, Figma MCP routing, Codex CLI bridge, and the Android frame mockup. Body sections (design philosophies, scene templates, slide rules, animation rules, prototype scaffolding) are intentionally TBD — authored from scratch in Step 2 / Step 3 to keep the project license-clean.

#### Added — security gates

- `references/security-config.md` · allowlist of fetch hosts, deny rules, WebSearch policy, Codex CLI policy (§1.4), codename pattern table (§1.5) shared by WebSearch + Codex prompt gates.
- `references/svg-sanitize.md` · threat model + whitelist tags/attrs + CSS sub-sanitizer + CSP block + failure-mode placeholder + visibility comment policy.
- `references/production-boundaries.md` · 10-item prototype ↔ production migration table, React vendor procedure, proxy-backend pattern, pre-prod checklist.

#### Added — sanitizers (stdlib only, no PIL / lxml / defusedxml)

- `scripts/svg-sanitize.py` · XXE-guarded XML parse, tag/attr whitelist (50/60), CSS sub-sanitizer (`url()`, `@import`, `expression(`, `javascript:`, `behavior:`, `data:text/html`), SHA-256 PROVENANCE entry, dangerous-tag flag → exit 3, in-file visibility comment.
- `scripts/test_svg_sanitize.py` · 18 regression tests.
- `scripts/scan_assets.py` · PNG chunk + JPG segment scanner. Detects trailing data, non-whitelist chunks, oversized text/COM metadata, truncated containers. Severity 3-tier.
- `scripts/test_scan_assets.py` · 13 regression tests.

#### Added — Codex CLI bridge

- `references/codex-design-workflow.md` · 5-step workflow: confidentiality gate → codex install check → `codex exec` → strip-then-scan import gate → use the imported asset.
- `scripts/codex-image-import.py` · stdlib-only importer. Confidentiality gate (exit 4 on codename) + recursive PNG discovery in `~/.codex/generated_images/<session-id>/` + non-whitelist chunk strip (caBX / C2PA, trailing bytes) + scan_assets re-run on stripped output + atomic move + PROVENANCE entry with prompt SHA-256, source hash, output hash, Codex session id, stripped chunk list.
- `scripts/test_codex_image_import.py` · 16 regression tests covering every gate (codename block, oversized tEXt block, recursive discovery, dry-run, explicit `--src`, caBX strip, trailing-bytes audit, whitelist parity with scan_assets).

#### Added — Figma MCP workflow

- `references/figma-workflow.md` · meta hub, MCP-aware vs MCP-absent decision rules, audit report template.
- `references/figma-selection-aware.md` · `figma_get_selection` + image export + user confirm gate before any edit.
- `references/figma-layer-naming.md` · semantic naming convention, 10–20 batch propose-confirm-apply flow.
- `references/figma-component-grouping.md` · signature-based detection, 3+ instance threshold for promotion.
- `references/figma-brand-spec-import.md` · Figma → `team-brand-spec.json` per-section diff confirm; SVG path forced through `scripts/svg-sanitize.py`.

#### Added — assets

- `assets/team-brand-spec.example.json` · template for the per-project brand spec.
- `assets/android_frame.jsx` · Pixel 8 / 8 Pro mockup (Material 3 status bar 36 px, punch-hole 13×13 top:9, gesture indicator 72×4). `model="pixel8|pixel8pro"` prop.
- `references/brand-spec-fields.md` · field-by-field reference for `team-brand-spec.example.json`.

#### Added — examples / hooks / CI

- `examples/dot-claude-settings.json` · drop-in `.claude/settings.json` baseline. Deny: `yt-dlp`, `youtube-dl`, unrestricted `curl`, `wget`. Ask: allowlisted CDN hosts, `Bash(codex *)`, `Bash(python3 scripts/codex-image-import.py *)`, `WebSearch(*)`.
- `examples/README.md` · how to wire up the settings.
- `.githooks/pre-commit` + `scripts/install-hooks.sh` · opt-in pre-commit hook that runs `svg-sanitize.py --strict` on staged SVGs and `scan_assets.py` on staged PNG/JPG/GIF.
- `references/ci-template.md` · GitHub Actions + GitLab CI templates. Sanitizer regression tests + JSON template lint = hard-fail; asset scan = advisory.

### Pending — Step 2 / Step 3

See `PROJECT-PLAN.md`. Body sections (design philosophies, scene templates, Junior Designer workflow, anti-AI-slop checklist, slide deck conventions, animation rules, Tweaks system, critique guide, iOS frame mockup) are authored from scratch in subsequent releases.

---

## Tags

- `0.1.0-alpha` corresponds to the initial skeleton commit on 2026-05-09.
