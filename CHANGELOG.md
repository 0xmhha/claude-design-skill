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

### Added — Showcase gallery (Step 3.6 · Step 3 complete)

- 16 prebuilt visual demos under `assets/showcase-brand/generated/01..16-*.png`. Each PNG was generated fresh via Codex CLI + gpt-image-2 (`codex-cli 0.130.0`, OAuth via `codex login`) and imported through `scripts/codex-image-import.py` — the strip-then-scan gate stripped the `caBX` C2PA / JUMBF chunk (~23–26 KB per file), re-ran `scan_assets.py` on the stripped output, and recorded a single `PROVENANCE.md` entry covering source generator, Codex session id, full prompt + prompt SHA-256, source / output PNG SHA-256, stripped-chunk list, and post-strip stego-scan result (PASS for every file).
- **Sampling matrix**: 16 cells from the 9-scene × 18-philosophy cross-product, weighted toward the maintainer's game / web3 IP-track (`references/design-styles.md` §15–18 and `references/scene-templates.md` §06–09 occupy 4 of the 16 cells). Coverage: deck cover × editorial-identity / atmospheric gradient; mid-deck × neo-grotesque utility / data-dense ledger; web hero × editorial-spatial cinematic / kinetic typographic poster; infographic × data-dense ledger / print-translation editorial; mobile app × Apple-system glass / soft-tactile; game HUD × Game HUD / high-contrast graphic poster (Bauhaus cross); NFT marketplace × NFT Marketplace / Web3 Minimalism; wallet × Web3 Minimalism; onboarding × Onboarding-Game-Loop. Detail per cell in PROJECT-PLAN.md decisions log.
- Path note: the carrier directory is `assets/showcase-brand/` (a `scripts/codex-image-import.py` path convention — `<brand>-brand/generated/`); HANDOFF §7.6's mention of `assets/showcases/` is conceptual. HANDOFF §7.6 carries a *Status: shipped* banner pointing at the real path. SKILL.md References routing table gains the matching row.
- Validation: 47 python regression + 19 easing + JSON template all still pass; `scan_assets.py --dir assets/showcase-brand/generated/` returns "clean" for every file. License-clean: predecessor's `assets/showcases/` was not opened or copied; each PNG is freshly generated and individually attributable through the audit trail.

### Hardened — Codename pattern catalog (Step 4.2)

- `scripts/codex-image-import.py` `DEFAULT_CODENAME_PATTERNS` gains 2 conservative-pairing patterns: `\b(stealth|skunkworks|moonshot)[-_ ](launch|product|asset|hero|build|alpha|beta|prerelease|prototype)\b` (the keyword **must** be paired with an asset / build noun, so "stealth fighter aesthetic" passes through and only "stealth-launch hero" fires the gate); `\bv\d+(?:\.\d+)?[-_ ](stealth|internal|prerelease|preview)\b` (versioned phase codes like "v3-stealth", "v2 internal" — bare "v3 update" passes). The conservative-pairing trade-off is documented inline in the script and in `references/security-config.md §1.5`.
- `scripts/test_codex_image_import.py` gains 3 new cases: `test_internal_phase_noun_caught` (positive — "stealth-launch hero" → exit 4), `test_versioned_phase_caught` (positive — "v3-stealth marketing" → exit 4), `test_generic_adjective_use_not_blocked` (negative — "stealth fighter aesthetic, v3 update marketing visual" → exit 0). 16 → **19/19 OK**.
- `references/security-config.md §1.5` table gains 2 rows + a *Conservative-pairing rule* paragraph that names the trade-off (a determined leaker using a bare keyword passes; the WebSearch manual checklist + per-call user approval is the policy of last resort).
- HANDOFF.md §1 verification block + PROJECT-PLAN.md §8 Validation expected counts updated to `16/16 → 19/19` for `test_codex_image_import.py`.

### Skipped — SFX library (Step 3.5, out of scope per user instruction)

- User instruction 2026-05-10: this project is visual-only. No `references/sfx-library.md`, no `assets/sfx/`, no audio sanitizer. The HANDOFF.md §7.5 done-when bar (20+ SFX with PROVENANCE) is retired for this repo. HANDOFF.md §7.5 carries a *Status: out of scope* banner so future fresh-session agents do not re-open the work. PROJECT-PLAN.md decisions log records the reasoning. Carry-over phrases that mention sound elsewhere (e.g. `references/design-styles.md §18 Onboarding-Game-Loop`'s verbatim "haptic + animation + sound") stay as aesthetic-spec mentions, not sourcing commitments.

### Added — Animation best-practices + pitfalls (Step 3.4)

- `references/animation-best-practices.md` · 5-tier timing scale (Feedback 60–80 ms / Small 150–180 ms / Medium 250–280 ms / Entrance 380–450 ms / Heroic 600–900 ms); easing selection table; stagger discipline (per-element delay × group size, runway-vs-duration rule); direction conventions (Material gravity-aligned + the game-HUD "home edge" exception); `prefers-reduced-motion` as first-class; performance budget (transform / opacity hot path); loop discipline; cross-fade vs morph; use-case routing for deck cover / app screen / modal / hover / loading / state ack / game HUD damage flash / wallet transaction confirmation. Seven external references (Material Motion, Apple HIG Motion, CSS Easing Level 1, WCAG 2.2, FLIP, Chrome animations guide).
- `references/animation-pitfalls.md` · 14 pitfalls each formatted as **why it's bad → symptom → fix**: bounce-on-everything, linear-as-default, single-duration system, animated gradient mesh behind hero copy, autoplay-loop hero video, wrong CSS property animated, synchronized group fade, missing `prefers-reduced-motion`, decorative chrome on every state, stagger too aggressive, inconsistent timing, ambient loops with no escape, scroll-jutter without `will-change`, hero animation budget over 4 s. Closes with the threshold rule ("3+ pitfalls = structural rethink") and a cross-link to dimension 5 (Motion & micro-interactions) of the Critique guide.
- License-clean: generic best practices cited via external links; the upstream's *Apple Gallery showcase* anchor (named in HANDOFF §7.4) is absent. Predecessor's animation-best-practices and animation-pitfalls files were not opened.
- SKILL.md References routing table gains both rows; the TBD list loses the *Animation rules* item (engine in 3.3 + best-practices/pitfalls in 3.4 close the bundle).

### Added — Animation engine (Step 3.3)

- `assets/animations.jsx` · Stage / Sprite timeline written from scratch. `<Stage duration loop paused time respectReducedMotion onTimeUpdate>` (uncontrolled rAF mode and controlled `time`-prop mode), `<Sprite start end keepAfter freezeBefore>`, `useTime()`, `useSprite()`, `interpolate(t, [in], [out], easing?, extrapolate?)` with `clamp` (default) / `extend` modes. Public API matches the established Stage / Sprite shape (interface only); implementation original — predecessor's `assets/animations.jsx` was not opened.
- `assets/easing.js` · 14-curve frozen Easing pack as a pure CommonJS-friendly module. Dual export: `module.exports` for Node, `window.Easing` for the browser. Curves: `linear` · `easeIn/Out/InOut Quad` · `easeIn/Out/InOut Cubic` · `easeIn/Out/InOut Expo` · `easeIn/Out/InOut Back` · `easeOutElastic`. Pure functions, frozen at module load.
- `scripts/test_animations_easing.js` · regression suite required by the section spec (19 tests, stdlib only via `node:assert/strict`). Asserts `f(0)≈0` / `f(1)≈1` for every curve, `easeOut(t) ≈ 1 − easeIn(1−t)` symmetry for Quad / Cubic / Expo, fast-early / slow-late ordering vs linear, midpoint values, documented Back overshoot, sane Elastic band, pure-function determinism, and frozen-pack mutation safety. Run as `node scripts/test_animations_easing.js`. **19/19 OK.**
- `references/animation-engine.md` · engine reference. API surface table, `<Stage>` props (controlled vs uncontrolled), `<Sprite>` lifecycle, `useTime` / `useSprite` semantics, `interpolate` signature, 14-curve shape descriptions, four worked examples (single fade-in; staggered three-line title; controlled-mode snapshot testing; easing showcase), performance notes, and a *when not to reach for the engine* list.
- `HANDOFF.md §1` · verification block updated to include the new Node test, expected count `18/18, 13/13, 16/16, 19/19`. `PROJECT-PLAN.md §8` Validation block updated to match.
- SKILL.md References routing table gains the matching row.

### Added — Scene template library (Step 3.2)

- `references/scene-templates.md` · 9 output-type-anchored layouts (5 author-original + 4 game/web3 verbatim carry-over). Each: **Specs** (canvas + aspect variants), **Key design elements** (5–6 layout primitives), **Recommended philosophies** (cross-refs into `references/design-styles.md` by number), **Scene prompt template** (copy-paste-ready 6–7-line prompt block). Fresh five: deck cover slide / hero, mid-deck content slide, web hero with motion, infographic / data narrative, mobile app screen mock (cross-refs `assets/ios_frame.jsx` and `assets/android_frame.jsx`). Carry-over four (renumbered from predecessor §9–12 to §06–09): game HUD overlay, NFT marketplace card / collection grid, wallet / DEX interface, onboarding game-loop. The only modification on carry-overs is the **Recommended philosophies** line — re-numbered to point at this skill's design-styles catalog rather than the predecessor's. Document closes with a 16-row fast-mapping table (scene × brief-shape → philosophy) and a no-fusion rule. SKILL.md References routing table gains the matching row; the TBD list loses the matching reservation.

### Added — Design philosophy catalog (Step 3.1)

- `references/design-styles.md` · 578-line flat catalog of 18 design directions (no school grouping, no `N × M` math, deliberately structurally distinct from the upstream's `5 × 20` or `6 × 24`). Each entry: **Philosophy** (one-line core idea), **Signature traits** (4–5 bullets), **Prompt DNA** (copy-paste-ready 6-line prompt block tuned for `codex exec` / `gpt-image-2`), **Representative work** (external links to studios / sites — never paraphrased), **Search keywords** (search-engine-friendly phrases for the agent to fetch live references). 14 entries author-original to this repo (editorial-identity, neo-grotesque utility, brutalist reactive, editorial-spatial cinematic, Apple-system glass, print-translation editorial, data-dense ledger, atmospheric gradient (deliberate), soft-tactile / paper-like, high-contrast graphic poster, editorial dark, component-system minimal, kinetic typographic poster, documentary photographic). Four entries (§15–18: Game HUD, Web3 Minimalism, NFT Marketplace, Onboarding-Game-Loop) carry over verbatim from the maintainer's prior fork-author work in the predecessor repo's Phase 4 — same author, same IP, just renumbered. Document closes with a *pairings that hold up* list (5 valid two-philosophy combinations) and a *pairings that fight* list (4 combinations to refuse). SKILL.md References routing table gains the matching row; the TBD list loses the matching reservation.

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
