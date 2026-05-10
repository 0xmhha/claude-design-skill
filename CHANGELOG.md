# Changelog

All notable changes to this project are recorded here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

This project is a clean-room rewrite. The history is independent. See `PROJECT-PLAN.md` for the per-step decision log.

---

## [Unreleased]

### Added — session-handoff briefing

- `HANDOFF.md` — context briefing for fresh AI sessions. Covers project history, user's working style, anti-patterns observed in the predecessor session, decision tree, and a glossary. Read this before doing real work.
- README.md gets a top-of-file pointer to HANDOFF.md.

### Added — App prototype rules + IosFrame (Step 2.3)

- `assets/ios_frame.jsx` · iPhone 15 Pro / Pro Max device frame, authored from scratch. Model registry (`iphone15pro` / `iphone15promax`), titanium-edge gradient body, SF-styled status bar (signal / Wi-Fi / battery), home indicator, and a Dynamic Island that doubles as a children-receiving slot — pass an `island` ReactNode for now-playing / timer / Live Activity mocks; auto-expands to 220×48 with a 240 ms transition. Public API surface matches the predecessor's `<IosFrame>` (interface only, not protected); implementation is original.
- `SKILL.md` · new `## App prototype rules (iOS / Android)` section — Rule 1 frame wrapping (browser-window mockup is a hard reject for iOS / Android briefs), Rule 2 real images instead of placeholder grays, Rule 3 click-test before declaring done, plus the Dynamic Island slot guidance. References routing table gains the matching row; the TBD list loses the matching reservation.

### Added — Critique guide (Step 2.6 · Step 2 complete)

- `SKILL.md` · new `## Critique guide` section (211 lines). Six dimensions, defined in concrete behavior: (1) Visual hierarchy, (2) Typography, (3) Color & contrast, (4) Spacing & rhythm, (5) Motion & micro-interactions, (6) Copy & narrative. **N = 6 by design** — color & contrast and spacing & rhythm get their own axes. Each dimension is scored as `score / 10 · one-sentence reason · one concrete fix`. Threshold table (51–60 ship · 39–50 fix-and-rescore · 27–38 return to Stage 2 · <27 scrap), with the explicit rule that absolute scores must be re-evaluated against the actual brief before scrapping. Worked critique applied to `examples/tweaks-demo.html`, the real prior deliverable from Step 2.5; total 38 / 60 unfixed, with the closing turn showing how to re-score relative to the demo's narrow brief instead of an absolute marketing-page bar. Limitations section (no exposure to internal brand taste, single-pass scores state not trajectory, sub-27 means brief or direction is wrong). Authored from observation; predecessor's critique section was not read. References routing table gains the matching row; the TBD list loses the matching reservation. **Step 2 (SKILL.md body author pass) is complete with this section.**

### Added — Tweaks live-tuning system (Step 2.5)

- `assets/tweaks.js` · `<tweak-panel>` web component plus plain `<tweak>` children. Floating panel (bottom-right by default), hidden until `t` (Esc to close), built-in **Reset** button. Each `<tweak>` declares `name`, `options="a|b|c"`, `default`, optional `label`. Panel writes `data-tweak-<name>` onto `<html>` so caller CSS uses pure attribute selectors — no caller JavaScript required. Selections persist under `tweak::<pathname>::<name>` in localStorage and every change emits a `document` `tweakchange` CustomEvent. Public methods: `.set()`, `.get()`, `.values`, `.reset()`. Authored from scratch.
- `examples/tweaks-demo.html` · runnable worked example. Three live tweaks (palette / density / accent) drive five CSS variables on a real layout — page background, card padding, grid gap, accent CTA, and pill swatches all move when a tweak is toggled.
- `SKILL.md` · new `## Tweaks live-tuning system` section. Why the pattern exists, full public API for both elements, the caller CSS pattern, persistence / hotkey / event contract, public methods, the example reference, and a *when not to use it* list (one-off A/Bs, layout-structure changes, production apps). References routing table gains the matching row; the TBD list loses the matching reservation.

### Added — Junior Designer workflow (Step 2.1)

- `SKILL.md` · new `## Junior Designer workflow` section (241 lines). Four-stage loop: (1) **Assumptions, explicit** — numbered claims tagged `(verified)` / `(inferred)` / `(open)`, with rules for when to ask the user vs default-and-flag. (2) **Reasoning, visible** — one short paragraph framed as a contract that review pushes against, written before the artifact, never after. (3) **Placeholders, before details** — labeled gray blocks and `[bracketed]` text first; refine after the bones are right. (4) **Review, before delivery** — three concrete checklists (brief, assumptions, anti-slop) with the rule "≥3 anti-slop patterns means the design hasn't started yet". One worked example walked through all four stages: an NFT marketplace catalog card. Five consolidated failure modes plus a short-circuit rule (tweaks → Stage 4 only; copy-edits → Stage 1 + 4; repeat tasks → Stage 3 + 4; anything new → full loop). Authored from observation; predecessor's section was not read. References routing table gains the matching row; the TBD list loses the matching reservation.

### Added — Anti-AI-slop checklist (Step 2.2)

- `SKILL.md` · new `## Anti-AI-slop checklist` section. Twelve patterns formatted as "why it's slop → what to do instead", covering the most common AI-generated UI tells: rainbow / sunset gradient as primary identity, perfectly symmetric centered layouts, generic glassmorphism, default Inter / 16 px / 1.5 type, emoji-as-icon, single border-radius on everything, uniform vertical padding, placeholder marketing copy, stock content (Unsplash photography + Spline-style 3D), animated gradient-mesh hero backgrounds, default cyberpunk-neon palette for anything web3, and cargo-cult game-HUD detail. Last two are domain-specific to the maintainer's game / web3 context. Authored from observation, no upstream paraphrase. Threshold rule: one occurrence is a fix, three or more means the design has not started yet. References routing table gains the matching row; the TBD list loses the matching reservation.

### Added — Slide deck conventions + deck_stage.js (Step 2.4)

- `assets/deck_stage.js` · `<deck-stage>` web component, authored from scratch. 1920 × 1080 fixed canvas with letterbox auto-fit, colocated `<aside slot="notes">` speaker-notes pattern (detached from light DOM during collection so it never leaks onto the slide canvas), in-canvas notes overlay (toggle with `n`), blackout (`b`), keyboard surface (`←/→`, `space`, `pgup/pgdown`, `home/end`, `1–9` jump, `esc`), localStorage position memory, hash deep-link (`#slide-N`), opt-in postMessage broadcast (no wildcard — same security stance as the predecessor), and a `@page` print sheet that emits one canvas-sized page per slide. CSS variable hooks (`--deck-bg`, `--deck-slide-bg`, `--deck-stage-shadow`, `--deck-font`) for theming without forking. Same custom-element name and a similar attribute set as the predecessor; implementation is original.
- `SKILL.md` · new `## Slide deck conventions` section. Rule 1 fixed canvas (decks are not scrollable web pages; browser-window mockups are a hard reject for "deck" briefs), Rule 2 colocated speaker notes (`<aside slot="notes">` nested inside each `<section>`, never orphaned in `<head>`), Rule 3 print = one canvas-sized page per slide (verify the PDF before delivery), Rule 4 treat the keyboard as a user surface; plus CSS hooks and the broadcast-origin policy. References routing table gains the matching row; the TBD list loses the matching reservation.

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
