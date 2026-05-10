# claude-design-skill · Project Plan

> Started: 2026-05-09
> Goal: Claude Code-based design skill for hi-fi prototyping + Figma MCP precision work, license-clean from day one.

---

## 0. One-line summary

A clean-room design skill. Step 1 ships the security gates and tooling already authored from scratch by this maintainer. Step 2 / Step 3 author the design body (philosophies, scenes, workflows, animation rules) from scratch — no upstream skill is inherited.

---

## 1. Why a clean-room rewrite

Predecessor work (a security-hardened fork at `0xmhha/huashu-design`) demonstrated the security gates, the Figma MCP integration, and the Codex/gpt-image-2 bridge. That fork is licensed for personal R&D only — the upstream `huashu-design` skill it forked from is licensed for personal use only, with commercial / team use requiring a USD 1,800–3,500 license from the upstream author.

This project takes a different route — option (b) from the fork's `PROJECT-PLAN.md §5.2`: rewrite the design body from scratch and carry over only the maintainer's own work. That keeps the license clean and avoids both the licensing fee and the legal ambiguity of "substantial derivative work".

**Result**: this repo is MIT-licensed, depends on no upstream design skill, and can be migrated to a private internal git host without any inherited obligations.

---

## 2. What was carried over (Step 1 — done 2026-05-09)

23 files. Every one of them is authored from scratch by this maintainer in the previous fork's Phase 1–4.2. No upstream prose is included.

### Scripts (7 files, stdlib only)

| File | Origin |
|---|---|
| `scripts/svg-sanitize.py` | Phase 1 Group B (new in fork) |
| `scripts/scan_assets.py` | Phase 4.2 (new in fork) |
| `scripts/test_svg_sanitize.py` | Phase 4.1 (new in fork) |
| `scripts/test_scan_assets.py` | Phase 4.2 (new in fork) |
| `scripts/codex-image-import.py` | Fork v0.2 (new — codex bridge) |
| `scripts/test_codex_image_import.py` | Fork v0.2 (new — codex bridge tests) |
| `scripts/install-hooks.sh` | Phase 4.2 (new in fork) |

### References (11 files)

| File | Origin |
|---|---|
| `references/security-config.md` | Phase 1 Groups A + E (new) |
| `references/svg-sanitize.md` | Phase 1 Group B (new) |
| `references/production-boundaries.md` | Phase 1 Group C (new) |
| `references/figma-workflow.md` | Phase 3 (new) |
| `references/figma-selection-aware.md` | Phase 3 (new) |
| `references/figma-layer-naming.md` | Phase 3 (new) |
| `references/figma-component-grouping.md` | Phase 3 (new) |
| `references/figma-brand-spec-import.md` | Phase 3 (new) |
| `references/codex-design-workflow.md` | Fork v0.2 (new) |
| `references/brand-spec-fields.md` | Phase 4.2 (new) |
| `references/ci-template.md` | Phase 4.2 (new) |

### Assets (2 files)

| File | Origin |
|---|---|
| `assets/team-brand-spec.example.json` | Phase 1 Group A (replaces upstream `personal-asset-index`) |
| `assets/android_frame.jsx` | Phase 2 (rewritten from scratch to Pixel 8 / 8 Pro spec) |

### Examples + git hooks (3 files)

| File | Origin |
|---|---|
| `examples/dot-claude-settings.json` | Phase 4.1 (new) |
| `examples/README.md` | Phase 4.1 (new) |
| `.githooks/pre-commit` | Phase 4.2 (new) |

### Authored fresh in this repo (5 files)

| File | Status |
|---|---|
| `SKILL.md` | New skeleton authored 2026-05-09. No upstream prose. |
| `README.md` | New, authored 2026-05-09. |
| `LICENSE` | MIT, new. |
| `CHANGELOG.md` | New, starting at v0.1.0-alpha. |
| `.gitignore` | New, tailored to this layout. |
| `PROJECT-PLAN.md` (this file) | New. |

---

## 3. What is intentionally NOT here yet

The skill body — design knowledge, scenes, workflows — is **deliberately empty in this skeleton**. Rationale: those sections in the upstream skill are the parts that risk being "substantial derivative" if copied or paraphrased. Authoring them from scratch with our own voice and our own taxonomy keeps the project license-clean and lets us tailor the body to game / web3 design needs.

Step 2 and Step 3 below cover this.

---

## 4. Step 2 — SKILL.md body author pass (next session)

Goal: fill in SKILL.md body sections that govern day-to-day skill behavior. Author from scratch. No upstream prose.

- [x] Junior Designer workflow — assumptions → reasoning → placeholders → review loop. Our own structure. (2026-05-10)
- [x] Anti-AI-slop checklist — generic gradient avoidance, layout symmetry, font pairing pitfalls. Our own list. (2026-05-10)
- [x] App prototype rules — `IosFrame` (new mockup engine, written from scratch — `assets/android_frame.jsx` already in) + real-image policy + Playwright verification. (2026-05-09)
- [x] Slide deck conventions — 1920×1080 layout primitives, speaker-notes panel. (2026-05-10)
- [ ] Tweaks live-tuning system — design decisions toggle-able at runtime.
- [ ] Critique guide — N-dimension scoring after delivery, with our own dimensions.

Rough budget: 1 session per section (= 6 sessions). Each section may grow into its own `references/*.md` if it crosses ~150 lines.

---

## 5. Step 3 — Design knowledge catalog (subsequent sessions)

Goal: author the design philosophy and scene template catalogs. This is where the upstream's most-substantial content lives — we deliberately do not copy or paraphrase. We restart from first principles.

- [ ] `references/design-styles.md` — design philosophy catalog. Our taxonomy: e.g. minimal-editorial, kinetic, spatial-3D, brutalist, game-HUD, web3-minimal, NFT-marketplace, onboarding-game-loop. 4–6 schools × 4–6 philosophies. Each entry: prompt DNA + identifying features + reference works (cited externally). Author cleanly — no upstream wording.
- [ ] `references/scene-templates.md` — scene catalog: cover, infographic, slide, hero animation, game HUD overlay, NFT marketplace card, wallet/DEX, onboarding game-loop. Each entry: layout primitives + key elements + recommended styles + prompt template. Author cleanly.
- [ ] `references/animation-engine.md` + `assets/animations.jsx` — Stage / Sprite engine, rewritten from scratch. Public API: `<Stage duration>`, `<Sprite start end>`, `useTime()`, `useSprite()`, `interpolate()`, `Easing`. Same shape as the upstream API (which is functional, not protected), our own implementation.
- [ ] `references/animation-best-practices.md` + `references/animation-pitfalls.md` — animation conventions. Author cleanly. Generic best practices can be cited; specific upstream examples must be replaced.
- [ ] `references/sfx-library.md` + `assets/sfx/` — sound effect catalog. Sourced from CC0 / freesound with PROVENANCE.md per file. Authored cleanly.
- [ ] `assets/showcases/` — prebuilt visual demos. Generated from scratch per scene + style combination. Each PNG gets PROVENANCE.md with prompt + Codex session id.

---

## 6. Step 4 — Internal brand integration (when team brand is finalized)

- [ ] Replace placeholder values in `team-brand-spec.json` (logo, colors, typography stack).
- [ ] Add the team's codename namespace to `references/security-config.md §1.5` and `scripts/codex-image-import.py` `DEFAULT_CODENAME_PATTERNS`.
- [ ] Decide `watermark.enabled` policy.
- [ ] Add internal asset hosts to `references/security-config.md §1.2` and `examples/dot-claude-settings.json` permissions.ask.
- [ ] Mirror to internal git host. Once internal-only, this README and the LICENSE may need replacement per team policy.
- [ ] Activate `references/ci-template.md` on the internal CI host — sanitizer regression tests + JSON lint as hard-fail; asset scan as advisory.

---

## 7. Decisions log

### 2026-05-09 · Step 1 complete

- Repo created at `/Users/kevin/work/github/0xmhha/claude-design-skill`.
- 23 maintainer-authored files carried over from `huashu-design` fork.
- 6 fresh files authored: SKILL.md (skeleton), README.md, LICENSE (MIT), CHANGELOG.md, .gitignore, this PROJECT-PLAN.md.
- License: MIT for now, replaceable per team policy before any external publication.
- Next: Step 2 — SKILL.md body author pass.

### 2026-05-09 · Step 2.3 — App prototype rules + IosFrame

- `assets/ios_frame.jsx` authored from scratch. iPhone 15 Pro / Pro Max model registry (393×852 / 430×932 logical px), titanium-edge gradient body, Dynamic Island as a children-receiving slot with 220×48 floor + 240 ms expand transition, SF-styled status bar, home indicator. Same public API surface as the predecessor's `IosFrame` (interface is not protected); implementation written fresh — no code copied from `huashu-design/assets/ios_frame.jsx`.
- `SKILL.md` gains a `## App prototype rules (iOS / Android)` section: Rule 1 frame wrapping (hard reject browser-window mockups for iOS / Android briefs), Rule 2 real images over placeholder grays, Rule 3 click-test before declaring done, plus the Dynamic Island slot guidance. References routing table updated; the matching item is removed from the TBD list.
- Validated: 47/47 regression tests still pass (svg-sanitize 18 + scan_assets 13 + codex-image-import 16); JSON template parses; visual smoke through Playwright with four cases (default, dark mode, Pro Max + Live-Activity-style island, no-chrome) all rendered correctly.
- Next: Step 2 — Junior Designer workflow OR Anti-AI-slop checklist OR Slide deck conventions (Tweaks live-tuning / Critique guide are later).

### 2026-05-10 · Step 2.4 — Slide deck conventions + deck_stage.js

- `assets/deck_stage.js` authored from scratch as a `<deck-stage>` web component. 1920×1080 fixed canvas with letterbox auto-fit, colocated `<aside slot="notes">` speaker-notes pattern, in-canvas notes overlay (toggle with `n`), blackout (`b`), keyboard surface (←/→/space/pgup/pgdown/home/end/1–9/esc), localStorage position memory, hash deep-link, opt-in postMessage broadcast (no wildcard, same security stance as the predecessor), and a `@page` print sheet that emits one canvas-sized page per slide. CSS variable hooks (`--deck-bg`, `--deck-slide-bg`, `--deck-stage-shadow`, `--deck-font`) for theming without forking. Same custom-element name and similar attribute set as the predecessor; implementation is original — different shadow-DOM bootstrap (`createElement`-based, no static `innerHTML`), different method decomposition, different localStorage key prefix, brand-new notes overlay (predecessor had none).
- `SKILL.md` gains a `## Slide deck conventions` section: Rule 1 fixed canvas (not flow layout, browser-window mockup is a hard reject), Rule 2 colocated speaker notes (`<aside slot="notes">` inside each `<section>`, never orphaned in `<head>`), Rule 3 print = one canvas-sized page per slide (Cmd / Ctrl + P verified before delivery), Rule 4 keyboard as user surface; plus CSS hooks and the broadcast-origin policy. References routing table updated; the matching item is removed from the TBD list.
- Two distribution bugs found by visual smoke and fixed in the same change: (1) per-slide light-DOM `display: flex` overrode `::slotted(section) { display: none }` because `::slotted` styles lose the cascade to the slotted-element's own light-DOM CSS — fixed by `::slotted(section:not(.is-active)) { display: none !important }`. (2) `<aside slot="notes">` is a grandchild of the shadow host (nested in `<section>`), and the slot algorithm only distributes direct children; the aside leaked into the slide canvas — fixed by detaching `aside` from light DOM during `_collect()` and cloning its contents into the overlay on each render.
- Validated: 47/47 regression tests still pass; JSON template parses; visual smoke through Playwright with four cases (cover default, cover + notes overlay, agenda + notes with `<ul>/<strong>` markup, outro + notes with `<em>` markup) — all rendered correctly after the fixes.
- Next: Step 2 — Junior Designer workflow OR Anti-AI-slop checklist (Tweaks live-tuning / Critique guide are later); Step 3 design-styles catalog is the highest-IP-risk section.

### 2026-05-10 · Step 2.2 — Anti-AI-slop checklist

- `SKILL.md` gains a `## Anti-AI-slop checklist` section. Twelve patterns, each formatted as **why it's slop → what to do instead** in one or two sentences: rainbow / sunset gradient as primary identity, perfectly symmetric centered layouts, generic glassmorphism, default Inter / 16 px / 1.5 type stack, emoji-as-icon, single border-radius applied to everything, uniform vertical padding, placeholder marketing copy, stock content (Unsplash + Spline-style 3D), animated gradient-mesh hero backgrounds, default cyberpunk-neon palette for anything web3, and cargo-cult game-HUD detail. The last two are domain-specific to the maintainer's game / web3 context. Authored from observation; predecessor's anti-slop section was not read. References routing table updated; the matching item is removed from the TBD list.
- A delivery threshold is stated explicitly: one occurrence is a fix, three or more means the design has not started yet — go back to references and try again. Concrete enough to be a real review gate, not a checklist that decorates the doc.
- Validated: 47/47 regression tests still pass (text-only change to SKILL.md and the doc index files); JSON template parses; no visual smoke needed (no new code or asset).
- Next: Step 2 — Junior Designer workflow (most foundational of the remaining), OR Tweaks live-tuning system, OR Critique guide; Step 3 design-styles catalog and animation engine remain the highest-IP-risk sections.

### 2026-05-10 · Step 2.1 — Junior Designer workflow

- `SKILL.md` gains a `## Junior Designer workflow` section (241 lines, exceeds the ≥150-line floor in HANDOFF §6.1 done-when). Four stages: (1) assumptions, explicit — numbered claims tagged `(verified)` / `(inferred)` / `(open)`; (2) reasoning, visible — one short paragraph framed as a contract that review pushes against; (3) placeholders, before details — labeled gray blocks and `[bracketed]` text before any polish; (4) review, before delivery — three concrete checklists (brief, assumptions, anti-slop). Each stage carries an explicit failure mode.
- One worked example walked through all four stages: an NFT-marketplace catalog card. Domain-aligned with the maintainer's game / web3 IP-track. Stage 1 surfaces seven assumptions including two `(open)` defaults to flag with the user; Stage 2 fixes the artwork-dominant + price-as-primary direction; Stage 3 ships rough placeholders (`[NFT 4:5]`, `[2.4 ETH]`, `[12 holders]`); Stage 4 scores the artifact 1/12 anti-slop with the in-flight pattern already on the open-question list.
- Consolidated failure-mode list (5 items) plus a short-circuit rule: tweaks need only Stage 4, copy-edits need Stage 1 + 4, repeat tasks need Stage 3 + 4, anything new runs the full loop.
- License-clean: predecessor SKILL.md "Junior Designer" content was not read; the four-stage structure is a generic engineering pattern (HANDOFF §6.1 explicitly allows it); prose, examples, and failure modes are original. SKILL.md contains no reference to "huashu-design" (verified by grep). References routing table updated; the matching item is removed from the TBD list.
- Validated: 47/47 regression tests still pass (text-only change); JSON template parses; no visual smoke needed.
- Next: Step 2 — Tweaks live-tuning system (§6.5) OR Critique guide (§6.6) — the last two Step 2 items; Step 3 design-styles catalog and animation engine remain the highest-IP-risk sections.

---

## 8. Validation

Before each step is marked done:

```bash
python3 scripts/test_svg_sanitize.py        # must be 18/18 OK
python3 scripts/test_scan_assets.py         # must be 13/13 OK
python3 scripts/test_codex_image_import.py  # must be 16/16 OK
python3 scripts/scan_assets.py --dir assets/  # must list 'clean' for every file
python3 -c "import json; json.load(open('examples/dot-claude-settings.json'))"
```

Step 1 validation: all five pass on 2026-05-09.
