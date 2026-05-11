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

**Result**: this repo is **Apache-2.0 licensed** (changed from MIT on 2026-05-10), depends on no upstream design skill, and can be migrated to a private internal git host without any inherited obligations. The upstream `alchaincyf/huashu-design` Personal-Use license is separate and unaffected — this repo does not derive from it.

---

## 2. What was carried over (Step 1 — done 2026-05-09)

23 files. Every one of them is authored from scratch by this maintainer in the previous fork's Phase 1–4.2. No upstream prose is included.

### Scripts (7 carry-over + 2 post-Step-4 fork-bootstrap = 9 files, stdlib only)

| File | Origin |
|---|---|
| `scripts/svg-sanitize.py` | Phase 1 Group B (new in fork) |
| `scripts/scan_assets.py` | Phase 4.2 (new in fork) |
| `scripts/test_svg_sanitize.py` | Phase 4.1 (new in fork) |
| `scripts/test_scan_assets.py` | Phase 4.2 (new in fork) |
| `scripts/codex-image-import.py` | Fork v0.2 (new — codex bridge) |
| `scripts/test_codex_image_import.py` | Fork v0.2 (new — codex bridge tests) |
| `scripts/install-hooks.sh` | Phase 4.2 (new in fork) |
| `scripts/init-brand.py` | Post-Step-4 (2026-05-10, `62c0928`) — fork-bootstrap helper |
| `scripts/test_init_brand.py` | Post-Step-4 (2026-05-10, `62c0928`) — 9/9 OK |

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
| `assets/team-brand-spec.default.json` | Phase 1 Group A as `*.example.json`; promoted to `*.default.json` operational defaults in Step 5.1 (2026-05-11) |
| `assets/android_frame.jsx` | Phase 2 (rewritten from scratch to Pixel 8 / 8 Pro spec) |

### Examples + git hooks (3 files)

| File | Origin |
|---|---|
| `examples/dot-claude-settings.json` | Phase 4.1 (new) |
| `examples/README.md` | Phase 4.1 (new) |
| `.githooks/pre-commit` | Phase 4.2 (new) |

### Authored fresh in this repo (6 files at Step 1)

| File | Status |
|---|---|
| `SKILL.md` | New skeleton authored 2026-05-09. No upstream prose. |
| `README.md` | New, authored 2026-05-09. |
| `LICENSE` | MIT at Step 1; replaced with Apache 2.0 on 2026-05-10 (`8dbd325`). |
| `CHANGELOG.md` | New, starting from Step 1. |
| `.gitignore` | New, tailored to this layout. |
| `PROJECT-PLAN.md` (this file) | New. |

### Post-Step-4 additions (2026-05-10 → 2026-05-11)

Not part of the original 23-file carry-over; shipped as doc/policy hygiene
after Step 4 closed. Listed here so the inventory matches the current tree.

| File | Origin |
|---|---|
| `NOTICE` | License change (`8dbd325`) — required by Apache §4(d). |
| `SECURITY.md` | Repo hygiene (`3cd7e74`) — vulnerability disclosure pointer. |
| `CONTRIBUTING.md` | Repo hygiene (`3cd7e74`). |
| `.github/dependabot.yml` | Repo hygiene (`3cd7e74`) — weekly Actions / pip / npm bumps. |
| `assets/showcase-brand/README.md` | Showcase gallery preview catalog (`ab155f7`). |
| `assets/showcase-brand/PROVENANCE.md` | Step 3.6 audit trail (16 PNGs, shipped at `22cc9cf`). |

---

## 3. What was deliberately empty at Step 1, and how it was filled

The skill body — design knowledge, scenes, workflows — was deliberately empty at the end of Step 1 (the initial skeleton). Rationale: those sections in the upstream skill are the parts that risk being "substantial derivative" if copied or paraphrased. Authoring them from scratch with our own voice and our own taxonomy keeps the project license-clean and lets us tailor the body to game / web3 design needs.

Step 2 (SKILL.md body) and Step 3 (design-knowledge catalog) covered this in 2026-05-09 → 2026-05-10. See the per-step decisions log entries below for the license-clean evidence each section recorded (predecessor read scope, fresh-author scope, verbatim carry-over scope where applicable).

---

## 4. Step 2 — SKILL.md body author pass (next session)

Goal: fill in SKILL.md body sections that govern day-to-day skill behavior. Author from scratch. No upstream prose.

- [x] Junior Designer workflow — assumptions → reasoning → placeholders → review loop. Our own structure. (2026-05-10)
- [x] Anti-AI-slop checklist — generic gradient avoidance, layout symmetry, font pairing pitfalls. Our own list. (2026-05-10)
- [x] App prototype rules — `IosFrame` (new mockup engine, written from scratch — `assets/android_frame.jsx` already in) + real-image policy + Playwright verification. (2026-05-09)
- [x] Slide deck conventions — 1920×1080 layout primitives, speaker-notes panel. (2026-05-10)
- [x] Tweaks live-tuning system — design decisions toggle-able at runtime. (2026-05-10)
- [x] Critique guide — N-dimension scoring after delivery, with our own dimensions. (2026-05-10)

Rough budget: 1 session per section (= 6 sessions). Each section may grow into its own `references/*.md` if it crosses ~150 lines.

---

## 5. Step 3 — Design knowledge catalog (subsequent sessions)

Goal: author the design philosophy and scene template catalogs. This is where the upstream's most-substantial content lives — we deliberately do not copy or paraphrase. We restart from first principles.

- [x] `references/design-styles.md` — design philosophy catalog. Flat 18 directions (no schools, no grid). 14 author-original + 4 game/web3 verbatim carry-over from prior fork-author work. (2026-05-10)
- [x] `references/scene-templates.md` — scene catalog: 9 templates (5 fresh + 4 game/web3 verbatim carry-over). Each entry: dimensions + key elements + recommended-philosophy cross-refs + prompt template. (2026-05-10)
- [x] `references/animation-engine.md` + `assets/animations.jsx` + `assets/easing.js` — Stage / Sprite engine + 14-curve Easing pack. Public API matches the established `<Stage>` / `<Sprite>` / `useTime` / `useSprite` / `interpolate` / `Easing` shape (interface only, not protected); implementation original. Easing has its own regression suite (`scripts/test_animations_easing.js`, 19/19). (2026-05-10)
- [x] `references/animation-best-practices.md` + `references/animation-pitfalls.md` — animation conventions. Generic best practices cited externally (Material 3, Apple HIG, CSS Easing spec); no upstream-specific case studies retained. (2026-05-10)
- [—] ~~`references/sfx-library.md` + `assets/sfx/`~~ — **out of scope per user instruction 2026-05-10**. Visual-only project; no SFX library will be authored, no audio assets vendored. (See decisions log entry below.)
- [x] `assets/showcases/` — prebuilt visual demos. 16 PNGs at `assets/showcase-brand/generated/` (codex-image-import.py path convention). Generated fresh from Codex CLI + gpt-image-2 per scene × philosophy combination. PROVENANCE.md per file with prompt SHA-256, Codex session id, stripped chunks. (2026-05-10)

---

## 6. Step 4 — Internal brand integration

Step 4 + Step 5 split cleanly into three buckets:

- **(a) Repo-level defaults shipped here** — automation + bootstrap. Done.
- **(b) Default-ships-here · adopter overrides** — values that *do* have a default value (identity, codenames, watermark, asset hosts) and where the only adopter action is to override toward their brand. Done.
- **(c) Repo-external operations** — actions that *cannot* have a default because they happen outside this repo (mirror to internal git host, port the CI workflow to another host). Adopter-only.

The earlier "per-fork actions" framing collapsed (b) and (c) into one bucket and read like the repo was incomplete; the split clarifies that *nothing functional is missing* — adopters edit values, not implement features.

### (a) Shipped in this repo (defaults + bootstrap)

- [x] **Default codename pattern catalog** — `scripts/codex-image-import.py:DEFAULT_CODENAME_PATTERNS` ships 4 conservative-pairing patterns; `references/security-config.md §1.5` mirrors them with the *Conservative-pairing rule* paragraph. (`eb33448`, 2026-05-10)
- [x] **Default `watermark.enabled` policy** — `assets/team-brand-spec.default.json` ships `enabled: false` (file was `*.example.json` until Step 5.1 2026-05-11 promoted it); `references/brand-spec-fields.md §watermark` documents the keep-it-off-until-explicitly-approved policy. (2026-05-10)
- [x] **Default public asset host allowlist** — `examples/dot-claude-settings.json:permissions.ask` and `references/security-config.md §1.1` ship 5 generic-public host entries (Lucide / Phosphor CDN mirrors + MDN). (`2ea3bb8`, 2026-05-10)
- [x] **GitHub Actions CI activated** — `.github/workflows/sanitizers.yml` runs the full guard chain (18 + 13 + 19 + 19 + JSON + advisory asset scan) on every push to `master` / `main` and every pull request. (`d5dba7b`, 2026-05-10)
- [x] **Fork-bootstrap helper** — `scripts/init-brand.py` (+ 11/11 tests as of Step 5.1) stamps a per-team brand carrier from `assets/team-brand-spec.default.json` (was `*.example.json` until Step 5.1 promotion) so adopters can bootstrap without hand-editing JSON. (`62c0928`, 2026-05-10; rewired in Step 5.1, 2026-05-11)

### (b) Default-ships-here · adopter overrides (override-only slots)

These items already have a default value shipped in this repo (via Step 4 + Step 5). Adopters use them as-is until they want to customise; the only *adopter action* is to override toward their own brand. None of these are missing functionality.

- [x] **Identity defaults in `team-brand-spec.default.json`** — `team.company = "Default Studio"`, `brand.name = "Default"`, `brand.tagline_short = "Design that ships."`, `brand.tone_keywords = ["precise", "expressive", "credible"]`, `brand.forbidden_zones` evidence-anchored. Logos under `assets/default-brand/*.svg` (mark + inverse + wordmark + icon, all sanitiser-clean). Token values (colour / type / spacing / radius / motion / iconography) all evidence-anchored to `references/web3-game-style-stats.md`. *Adopter override*: edit `team-brand-spec.json` (or stamp via `init-brand.py` / `figma-to-brand-spec.py`).
- [x] **Codename pattern catalog** — `scripts/codex-image-import.py:DEFAULT_CODENAME_PATTERNS` ships 4 conservative-pairing patterns; `references/security-config.md §1.5` mirrors. *Adopter override*: append team-specific patterns alongside the defaults.
- [x] **Watermark policy** — `assets/team-brand-spec.default.json:watermark.enabled = false`; `references/brand-spec-fields.md §watermark` documents *keep-it-off-until-explicitly-approved*. *Adopter override*: flip to `true` and set `watermark.text` after explicit approval.
- [x] **Public asset host allowlist** — `examples/dot-claude-settings.json:permissions.ask` + `references/security-config.md §1.1` ship 5 generic-public hosts (Lucide / Phosphor / MDN). *Adopter override*: add team-internal hosts under `approved_asset_hosts.internal` + `security-config.md §1.2 Team-extensible additions`.

### (c) Repo-external operations (no default possible · guides ship here)

These actions happen *outside* this repo (different git host, different CI system). The repo cannot run the *doing* for the adopter; what it can do — and now does — is ship **concrete, copy-paste-ready** guides for each step. The `[ ]` boxes below stay open by design: the *adopter* checks them once their internal infrastructure is up.

- [ ] **Mirror to the team's internal git host.** Adopter-only action. `CONTRIBUTING.md §For fork operators / Mirror to your internal git host` ships the 5-step bash recipe (create empty private repo → `git remote add internal` → push branches + tags → verify ls-remote → tag the divergence point), plus the *which-stays-public* policy (Default Studio identity in `team-brand-spec.json`, team-internal hosts in `approved_asset_hosts.internal`).
- [ ] **Port the CI workflow to a non-GitHub host.** Adopter-only action. `references/ci-template.md` ships ready-to-paste templates for **GitLab CI**, **Bitbucket Pipelines**, and **Buildkite** — each runs the identical 6-suite guard chain (93 tests + 2 JSON parses + 1 advisory scan); only the wrapping YAML differs. Translation notes cover GitHub Enterprise (identical to the reference workflow), Jenkins (declarative pipeline pattern), and CircleCI / Drone. License / replacement of `LICENSE` + `NOTICE` is a sub-step of the mirror action above and ships as item 10 in the same CONTRIBUTING list.

---

## 6.5. Step 5 — operational defaults + Figma ingestion (complete 2026-05-11)

Step 5 changes the contract of `team-brand-spec`: from *placeholder example* to *operational default*. The default values are evidence-based — pulled from style analysis of trusted web3 + game services — so that an agent producing design output without any team override still ships **non-AI-slop** results. A second path lets adopters extract their own spec from Figma instead of hand-editing JSON.

User decisions (2026-05-11):

- **Reference service set (11 services)** — web3 (6): Uniswap, OpenSea, Phantom, Lens Protocol, Farcaster (Warpcast), Coinbase; game (5): Riot Valorant, miHoYo Genshin Impact, Bungie Destiny 2, Supergiant Hades, Supercell Clash Royale. All have publicly observable design language (official design system docs, brand pages, or production sites).
- **Field scope** — full spec coverage: core (color tokens, typography stack, spacing, radius, motion timing) + iconography (family, stroke, weight) + watermark + logo defaults (shape, aspect ratio) + asset host hints.
- **Sequence** — 5.2 stats → 5.1 default file → 5.3 Figma tool → 5.4 verify-and-doc. Each sub-step ships as its own commit.

Sub-steps:

- [x] **5.2** — `references/web3-game-style-stats.md` (316 lines): per-service evidence rows for 11 services, then aggregated decision values per dimension. Shipped across 5 batch commits.
- [x] **5.1** — `assets/team-brand-spec.default.json` operational default; `scripts/init-brand.py` rewired; tests 9 → 11. (`4c3d7ef`)
- [x] **5.3** — `scripts/figma-to-brand-spec.py` (REST + fixture) + 13 tests + `references/figma-to-brand-spec.md` + CI step. (`de2b3f2`)
- [x] **5.4** — verify-and-doc consistency pass; SKILL.md routing rows added; status headers bumped; CHANGELOG entry; 93-test full guard chain re-validated.

Out of scope for Step 5:

- Round-trip (spec → Figma write-back) — extraction only.
- Auto-update from production sites (CSS scraping) — too volatile; 5.2 is a one-time research snapshot, refreshable on user instruction.

---

## 7. Decisions log

### 2026-05-09 · Step 1 complete

- Repo created at <https://github.com/0xmhha/claude-design-skill> (local clone path was on the original-author machine; abstracted to `<repo-root>` in 2026-05-11 doc-path normalization).
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

### 2026-05-10 · Step 2.5 — Tweaks live-tuning system

- `assets/tweaks.js` authored from scratch as a `<tweak-panel>` web component plus plain `<tweak>` children. Floating panel (bottom-right by default), hidden until `t` (Esc to close), built-in **Reset** button, position attribute (`bottom-right` / `bottom-left` / `top-right` / `top-left`), `open` / `hotkey=""` overrides. Each `<tweak>` declares `name`, `options="a|b|c"`, `default`, optional `label`. Panel writes `data-tweak-<name>` onto `<html>` so caller CSS uses pure attribute selectors — **no caller JS required**. Selections persist under `tweak::<pathname>::<name>` in localStorage; every change emits a `document` `tweakchange` CustomEvent (`{name, value, source: "user"|"restore"}`). Public methods: `.set()`, `.get()`, `.values`, `.reset()`. License-clean: predecessor `tweaks-system.md` and the predecessor's tweaks asset were not read; element name (`<tweak-panel>` + plain `<tweak>`), localStorage key shape, event name, panel chrome, and Reset behavior are own choices.
- `examples/tweaks-demo.html` ships a runnable worked example. Three live tweaks (palette / density / accent) drive five CSS variables (`--bg`, `--fg`, `--muted`, `--gap`, `--accent`) on a real layout — page background, card padding, grid gap, accent CTA, and pill swatches all move when a tweak is toggled. The page declares its own CSS responses to `:root[data-tweak-palette="cool"]` etc.; toggle survives reload via localStorage.
- `SKILL.md` gains a `## Tweaks live-tuning system` section: why the pattern exists (re-rendering through an LLM is lossy and slow; designers want to compare, not regenerate; most variations are CSS-variable swaps), full public API for both elements, the caller CSS pattern, persistence/hotkey/event contract, public methods, the example reference, and a *when not to use it* list (one-off A/Bs, layout-structure changes, production apps). References routing table updated; the matching item is removed from the TBD list.
- One bug caught by visual smoke and fixed in this commit: `customElements.define('tweak', Tweak)` threw a `SyntaxError` because the web-components spec requires a hyphen in registered names — `tweak` is illegal as a registered custom-element name. Fixed by leaving `<tweak>` as a plain unknown HTML element (panel reads attributes off the children; no registered element needed), and explicitly hiding `<tweak>` children in `_collect()` so their default inline box does not affect surrounding layout.
- Validated: 47/47 regression tests still pass; JSON template parses; visual smoke through Playwright with three states (default warm/comfortable/orange, panel revealed via `t` hotkey, panel after `.set()` of cool/spacious/blue) all rendered correctly; `data-tweak-*` attributes verified on `<html>`, three localStorage keys verified.
- Next: Step 2 — Critique guide (§6.6, the last Step 2 item); Step 3 design-styles catalog and animation engine remain the highest-IP-risk sections.

### 2026-05-10 · Step 2.6 — Critique guide (Step 2 complete)

- `SKILL.md` gains a `## Critique guide` section (211 lines). Six dimensions, defined in concrete behavior rather than adjectives: (1) Visual hierarchy — eye finds primary message in <2 s without reading; (2) Typography — typeface / scale / line-height / tracking visibly *intent*; (3) Color & contrast — role-system + WCAG AA, on its own axis so accessibility is not buried inside "visual"; (4) Spacing & rhythm — vertical cadence variation across hero / content / dense / footer; (5) Motion & micro-interactions — hover, focus, state transitions, `prefers-reduced-motion`; (6) Copy & narrative — specificity vs marketing-template fill. **N = 6 deliberately**: HANDOFF.md §6.6 requires N ≠ 5 (predecessor uses 5); the split that earned the seat is putting color & contrast and spacing & rhythm on their own axes.
- Scoring shape stated: each dimension yields one line — `score / 10 · one-sentence reason · one concrete fix`. Threshold table: 51–60 ship, 39–50 fix-and-rescore, 27–38 return to Stage 2 reasoning, <27 scrap. The threshold matters because the agent's natural failure mode is to declare "looks fine" at a 35.
- Worked critique applied to `examples/tweaks-demo.html` — a real prior deliverable from this session, viewed in three states during Step 2.5's visual smoke. Total: 38 / 60 unfixed, with motion (4) and the placeholder "Hypothetical CTA" copy as the largest gaps. The closing turn is the load-bearing one: 38 sits in the "return to Stage 2" band, but the *brief-relative* score (the demo's brief is "prove the API", not "publish a marketing page") is materially higher; the rule is to re-score against the actual brief before scrapping. That single turn is what stops the next fresh agent from auto-failing demonstration artifacts.
- Limitations stated explicitly: critique reflects only what the agent can see (no exposure to internal brand taste); single passes score state, not trajectory (Stage-3 placeholders read low on several axes by design); overall <27 means brief or direction is wrong, not that the agent is bad at design — fix one level up at Stage 2 reasoning, not at this layer.
- License-clean: predecessor's critique section (5 dimensions) was not read; N = 6 by design; dimension definitions, scoring shape, threshold table, and worked critique are all original. SKILL.md contains no reference to "huashu-design" (verified by grep).
- Validated: 47/47 regression tests still pass; JSON template parses; no visual smoke needed (text-only change).
- **Step 2 complete.** All six body sections (§6.1 Junior Designer workflow, §6.2 Anti-AI-slop checklist, §6.3 App prototype rules + IosFrame, §6.4 Slide deck conventions + deck_stage.js, §6.5 Tweaks live-tuning system, §6.6 Critique guide) are authored. Next milestone is Step 3 (design philosophy catalog, scene templates, animation engine, animation best-practices, SFX library, showcase generation) — the highest-IP-risk sections of the upstream.

### 2026-05-10 · Step 3.1 — `references/design-styles.md`

- `references/design-styles.md` written from scratch (578 lines, exceeds the ≥400-line floor in HANDOFF §7.1 done-when). Taxonomy chosen explicitly to differ from the upstream's "5 schools × 20 philosophies" or "6 schools × 24 philosophies" math: a **flat 18-entry catalog with no school grouping**. The flat structure itself is the structural-similarity firewall — no school chapters, no nested 4×N math. Numbering 01–18 with the four game / web3 entries occupying §15–18.
- 14 author-original entries: editorial-identity (Pentagram / Build / Atlas), neo-grotesque utility (Stripe / Linear / Vercel docs), brutalist reactive (Are.na / Pirx / contemporary indie web), editorial-spatial cinematic (Active Theory / Field.io / Resn), Apple-system glass (HIG iOS 18 / macOS Sonoma), print-translation editorial (New Yorker / The Pudding / NYT magazine), data-dense ledger (Bloomberg / DefiLlama / Polymarket), atmospheric gradient (deliberate) (Vercel 2024 / OpenAI / Anthropic), soft-tactile / paper-like (Things 3 / Notion 2024 / Maven), high-contrast graphic poster (Bauhaus / MoMA / Verso Books), editorial dark (Pitchfork / Substack reader / Are.na dark), component-system minimal (Linear / Radix / shadcn-ui), kinetic typographic poster (DIA Studio / Pangram Pangram / Hyperaktiv), documentary photographic (Magnum / M Le Mag / Atlas Obscura). Each entry: **Philosophy** (one-line core idea) + **Signature traits** (4–5 bullets) + **Prompt DNA** (copy-paste-ready 6-line prompt) + **Representative work** (external links — never paraphrased) + **Search keywords**.
- 4 verbatim carry-over from the maintainer's prior fork-author work in the predecessor repo's `references/design-styles.md §21–24` (Phase 4): §15 Game HUD · Diablo / Destiny / Genshin lineage, §16 Web3 Minimalism · Uniswap / Lens / Farcaster lineage, §17 NFT Marketplace · OpenSea / Blur / Magic Eden lineage, §18 Onboarding-Game-Loop · Polished mobile game / web3 onboarding hybrid. Section numbering shifts (predecessor §21–24 → §15–18); prose itself is unchanged. License: same author, same IP, just relocated — explicitly permitted by HANDOFF §7.1.
- Document closes with two utility sections: a **pairings-that-hold-up** list (5 valid two-philosophy combinations that share typographic / palette stance — *editorial-identity* + *atmospheric gradient*, *neo-grotesque utility* + *data-dense ledger*, etc.) and a **pairings-that-fight** list (4 combinations to refuse — e.g. *kinetic typographic poster* vs *documentary photographic* — type-first vs image-first, one always wins). The pairings table is original framing.
- License-clean: predecessor's prose for §1–20 was not read; only §21–24 (the verbatim-carry section) was opened. SKILL.md / `references/design-styles.md` contain no reference to "huashu-design" string (verified by grep). Validated: 47/47 regression tests still pass; JSON template parses; no visual smoke needed (prose only).
- SKILL.md References routing table updated; `Design philosophy catalog` item removed from the TBD list.
- Next: Step 3.2 — `references/scene-templates.md` (8–12 scenes, with the four maintainer-authored game/web3 scenes carried verbatim).

### 2026-05-10 · Step 3.2 — `references/scene-templates.md`

- `references/scene-templates.md` written from scratch (351 lines). **9 scenes** total (5 fresh + 4 verbatim) — odd count, deliberately differs from the predecessor's 12 to avoid count-match.
- 5 fresh templates: §01 Deck cover slide / hero (1920×1080 default with social and mobile variants, cross-refs `assets/deck_stage.js`); §02 Mid-deck content slide (single-layout-primitive rule, cross-refs the deck shell); §03 Web hero with motion (1440×900 / 1920×1200 with mobile companion, ONE narrative motion enforced); §04 Infographic / data narrative (vertical / embed / in-deck variants); §05 Mobile app screen mock (cross-refs `assets/ios_frame.jsx` and `assets/android_frame.jsx`, enforces App-prototype-rules). Each: **Specs** (canvas + variants) + **Key design elements** (5–6 layout primitives) + **Recommended philosophies** (2–3 numbered cross-refs into design-styles.md) + **Scene prompt template** (copy-paste-ready 6–7-line block tuned for codex / gpt-image-2).
- 4 verbatim templates: §06 Game HUD overlay, §07 NFT marketplace card / collection grid, §08 Wallet / DEX interface, §09 Onboarding game-loop. Carried over from the predecessor's `references/scene-templates.md §9–12`. Section numbering shifts (predecessor §9–12 → this catalog §06–09); the only other modification is the **Recommended philosophies** line, re-numbered to point at this skill's `references/design-styles.md` catalog rather than the predecessor's. Mapping applied: predecessor §21 Game HUD → this §15; §22 Web3 Minimal → §16; §23 NFT Marketplace → §17; §24 Onboarding-Loop → §18; predecessor entries not in this catalog (Territory Studio §16, Ash Thorp §15, Information Architects §03, Build §11 as a separate entry, Sagmeister §12, Takram §17) replaced with closest matches in this catalog. Replacement rationale stated in commit message. All other prose unchanged.
- Document closes with a **fast-mapping table** (16 rows, scene × brief-shape → recommended philosophy) and a no-fusion rule ("two-template combinations are smells, not features"). Original framing.
- License-clean: predecessor §1–8 prose was not read; only §9–12 (the verbatim-carry block) was opened. SKILL.md / `references/scene-templates.md` contain no reference to "huashu-design" string. SKILL.md References routing table updated; the matching item is removed from the TBD list.
- Validated: 47/47 regression tests still pass; JSON template parses; no visual smoke needed (prose only).
- Next: Step 3.3 — `references/animation-engine.md` + `assets/animations.jsx` (engine code rewrite from scratch; predecessor's `assets/animations.jsx` must NOT be carried over per HANDOFF §7.3).

### 2026-05-10 · Step 3.3 — animation engine (`assets/animations.jsx` + `assets/easing.js` + `scripts/test_animations_easing.js` + `references/animation-engine.md`)

- `assets/animations.jsx` written from scratch. Implements `<Stage>` (clock owner; uncontrolled rAF or controlled-via-`time` prop; `paused`, `loop`, `respectReducedMotion`, `onTimeUpdate`), `<Sprite>` (clip with `start` / `end` / `keepAfter` / `freezeBefore`), `useTime()`, `useSprite()`, `interpolate(t, [in], [out], easing?, extrapolate?)`. Public API matches the established Stage / Sprite shape (interface only, not protected by IP); implementation is original — predecessor's `assets/animations.jsx` was **not opened**, only the API spec from HANDOFF §7.3 was consumed.
- `assets/easing.js` separated as a pure CommonJS-friendly module (dual export: `module.exports` + `window.Easing`). 14 curves: `linear` · `easeIn/Out/InOut Quad` · `easeIn/Out/InOut Cubic` · `easeIn/Out/InOut Expo` · `easeIn/Out/InOut Back` · `easeOutElastic`. Pack is `Object.freeze`d; no state, no side effects.
- `scripts/test_animations_easing.js` is the regression suite required by HANDOFF §7.3 done-when. Stdlib only (`node:assert/strict`), 19 tests covering: every curve maps `0→0` and `1→1`; `easeOut` is the algebraic mirror of `easeIn` for the Quad / Cubic / Expo families; `easeOutCubic(0.25) > 0.25` (faster early than linear); `easeInCubic(0.75) < 0.75` (slower late); midpoint values for `easeInOutQuad/Cubic`; `easeOutBack` overshoots `[0, 1]` somewhere in `(0, 1)` and `easeInBack` undershoots; `easeOutElastic` stays in a sane `[-0.5, 1.5]` band; pure-function determinism; pack is frozen. **19/19 OK.**
- `references/animation-engine.md` ships the engine reference: API surface table, `<Stage>` props (controlled vs uncontrolled), `<Sprite>` lifecycle (active / `keepAfter` / `freezeBefore`), `useTime` / `useSprite` semantics, `interpolate` signature, the 14-curve table with shape descriptions, four worked examples (single fade-in; staggered three-line title; controlled-mode snapshot testing; easing showcase). Closes with performance notes and a "when *not* to reach for the engine" list.
- `HANDOFF.md §1` verification block updated to include `node scripts/test_animations_easing.js`. The `Expected:` line now reads "18/18, 13/13, 16/16, 19/19, all OK."
- Visual smoke through Playwright at three deterministic frames (controlled-mode `<Stage time={t}>`): t=0 (everything invisible — `freezeBefore` was deliberately omitted on the stagger sprites so they render nothing before `start`), t=500 (line 1 settled, line 2 mid-stagger, line 3 still hidden because `start=600 > 500`; easing bars at normalized progress 0.25 visibly diverge — linear 25 %, easeOutCubic ~58 %, easeInOutCubic ~6 %, easeOutBack ~80 %, easeOutElastic ~88 %), t=1500 (all lines settled via `keepAfter`; bars at normalized 0.75 — linear 75 %, easeOutCubic 98.4 %, easeOutBack **106.4 %** demonstrating overshoot, easeOutElastic 100.55 % showing settling oscillation). Cross-checked numerically via DOM inspection: every reading matches the closed-form value within IEEE rounding.
- License-clean: predecessor's `references/animation-engine.md` and `assets/animations.jsx` were not opened. The catalog under `references/animation-engine.md` references no "huashu-design" string.
- SKILL.md References routing table gains the matching row.
- Next: Step 3.4 — `references/animation-best-practices.md` + `references/animation-pitfalls.md` (timing conventions, narrative pacing, anti-pitfall checklist; cite generic best practices externally rather than paraphrasing the predecessor's distillation).

### 2026-05-10 · Step 3.4 — animation best-practices + pitfalls

- `references/animation-best-practices.md` (255 lines, exceeds the ≥120-line floor in HANDOFF §7.4 done-when). Sections: 5-tier timing scale (Feedback / Small / Medium / Entrance / Heroic with concrete ms ranges); easing selection table (entrance / exit / state-change / spinner / celebratory / ambient); stagger discipline (per-element delay × group size, runway-vs-duration rule); direction conventions (Material gravity-aligned + game-HUD "home edge"); reduced-motion as first-class with three satisfying patterns; performance budget (transform / opacity hot path); loop discipline (when to loop, when to refuse); cross-fade vs morph; use-case routing (deck cover / app screen / modal / hover / loading / state ack / game HUD damage flash / wallet transaction confirmation). Closes with seven external references (Material Motion, Apple HIG Motion, CSS Easing Level 1, WCAG 2.2, FLIP, Chrome animations guide).
- `references/animation-pitfalls.md` (282 lines, exceeds ≥120 floor). 14 pitfalls each formatted as **why it's bad → symptom → fix**: bounce-on-everything, linear-as-default, single-duration system, animated gradient mesh behind hero copy, autoplay-loop hero video, wrong CSS property animated, synchronized group fade, missing `prefers-reduced-motion`, decorative chrome on every state, stagger too aggressive, inconsistent timing, ambient loops with no escape, scroll-jutter without `will-change`, hero animation budget over 4 s. Closes with the threshold rule from `## Critique guide` ("3+ pitfalls = structural rethink, 1–2 = patch and ship") and a cross-link to dimension 5 (Motion & micro-interactions) of the Critique guide.
- License-clean: predecessor `animation-best-practices.md` and `animation-pitfalls.md` were not opened. Generic best practices cited via external links; the upstream-specific anchor *Apple Gallery showcase* mentioned in HANDOFF §7.4 is **absent** (verified by grep). No "huashu-design" string in either file.
- SKILL.md References routing table gains both rows; the TBD list loses the *Animation rules* item — which had bundled engine + best-practices + pitfalls. Step 3.3 + Step 3.4 together close the bundle.
- Validated: 47 python regression tests + 19 easing tests + JSON template all still pass; no visual smoke needed (prose only).
- Next: Step 3.5 — `references/sfx-library.md` + `assets/sfx/` (CC0 sourcing required; predecessor's `assets/sfx/*.mp3` must NOT be carried over per HANDOFF §7.5; provenance per file).

### 2026-05-10 · Step 3.5 — out of scope (user instruction)

- User instruction 2026-05-10: *"사운드는 필요 없어. 시각적인것만 잘 지원해도 충분한것 같아."* This project is visual-only.
- Decision: Step 3.5 is skipped entirely. No `references/sfx-library.md` will be authored. No `assets/sfx/` will be created. No audio sanitizer will be added to `scripts/`. The HANDOFF.md §7.5 done-when bar (20+ SFX with PROVENANCE) is retired for this repo.
- Reasoning surfaced before the decision: the only deliverables that would have benefited from vendored SFX are sound-bearing motion artifacts (deck cover reveal, app prototype interaction feedback, game HUD state changes, onboarding reward pings, wallet transaction confirmation, hero web animation). The user evaluated their actual deliverable mix as visual-only and chose to retire the section rather than ship a partial doc-only Step 3.5.
- Carry-over text that already references sound stays unchanged — `references/design-styles.md §18 Onboarding-Game-Loop` carries the predecessor's *"haptic + animation + sound"* phrase verbatim as part of its aesthetic spec; that's a reference to the *philosophy*, not a sourcing commitment from this repo.
- HANDOFF.md §7.5 updated with a *Status: out of scope* banner so a future fresh-session agent does not start authoring.
- Next: Step 3.6 — `assets/showcases/` (Codex CLI + gpt-image-2 generation; visual deliverable; the environment for it is already validated per HANDOFF §4).

### 2026-05-10 · Step 3.6 — `assets/showcase-brand/` (16 prebuilt visual demos)

- 16 PNGs generated via Codex CLI + gpt-image-2 (`codex-cli 0.130.0`, OAuth) and imported through `scripts/codex-image-import.py` (strip-then-scan gate, `caBX` C2PA chunk removed, `scan_assets.py` post-strip PASS for every file). Path: `assets/showcase-brand/generated/01..16-*.png`. The `<brand>-brand/generated/` carrier directory is the script's path convention; HANDOFF §7.6's mention of "`assets/showcases/`" is conceptual — the actual carrier is `assets/showcase-brand/generated/`. HANDOFF §7.6 carries a *Status: shipped* banner pointing at the real path so future agents do not look in the wrong directory.
- **Sampling matrix** — 16 cells from the 9-scene × 18-philosophy cross-product, weighted toward the maintainer's game / web3 IP-track (§06–09 game / web3 scenes occupy 4 of the 16 cells). Cells:
  | # | Scene | Philosophy | Topic |
  |---|---|---|---|
  | 01 | Deck cover | §01 Editorial-identity | "Three knobs. / No re-render." |
  | 02 | Deck cover | §08 Atmospheric gradient | "Decks, not / landing pages." (cool diffuse) |
  | 03 | Mid-deck content | §02 Neo-grotesque utility | Rate-limit table with state colors |
  | 04 | Mid-deck content | §07 Data-dense ledger | 24h volume snapshot (4 KPI tiles + sparklines) |
  | 05 | Web hero with motion | §04 Editorial-spatial cinematic | "Field-tested / motion." (off-black + film-grain stripe) |
  | 06 | Web hero with motion | §13 Kinetic typographic poster | "Type / performs." (extreme variable-font + ghost layer) |
  | 07 | Infographic | §07 Data-dense ledger | Q1 protocol-revenue vertical infographic |
  | 08 | Infographic | §06 Print-translation editorial | "Why deck cadence matters" essay-format infographic with drop cap |
  | 09 | Mobile app screen | §05 Apple-system glass | iOS 18 Today screen (Health / Calendar / Forecast) |
  | 10 | Mobile app screen | §09 Soft-tactile / paper-like | Things-3-style productivity Today screen |
  | 11 | Game HUD overlay | §15 Game HUD | Diablo / Destiny / Genshin HUD with edge-anchored chrome |
  | 12 | Game HUD overlay | §10 High-contrast graphic poster | Bauhaus-cross HUD (3-color discipline) |
  | 13 | NFT marketplace card | §17 NFT Marketplace | 4-up dark-mode card grid |
  | 14 | NFT marketplace card | §16 Web3 Minimalism | Type-first collection landing |
  | 15 | Wallet / DEX | §16 Web3 Minimalism | Uniswap-style mobile swap |
  | 16 | Onboarding game-loop | §18 Onboarding-Game-Loop | Step 3 / 7 chain-pick with friendly mascot |
- **Provenance audit trail** at `assets/showcase-brand/PROVENANCE.md` (213 lines): for each of the 16 files records source generator (`codex-cli` / gpt-image-2), Codex session id, full prompt text + prompt SHA-256, source PNG SHA-256, output (stripped) PNG SHA-256, stripped-chunk list (the C2PA `caBX` block — 23–26 KB per file — replaced by this PROVENANCE entry), post-strip stego-scan result (PASS), and final import status. Format follows the same single-PROVENANCE.md table convention as the other sanitizers (svg-sanitize, codex-image-import).
- **Validation**: 47 python regression + 19 easing + JSON template still pass; `scan_assets.py --dir assets/showcase-brand/generated/` returns "clean" for every one of the 16 files. License-clean: predecessor's `assets/showcases/` was not opened or copied; every PNG is freshly generated and individually attributable through the audit trail.
- SKILL.md References routing table gains the matching row.
- **Step 3 complete with this entry.** Step 3.5 was retired by user instruction (visual-only project); the remaining Step 3 work (3.1 design-styles, 3.2 scene-templates, 3.3 animation engine, 3.4 animation best-practices + pitfalls, 3.6 showcases) is shipped.

### 2026-05-10 · Step 4.2 — codename pattern catalog hardening

- `scripts/codex-image-import.py` `DEFAULT_CODENAME_PATTERNS` gains 2 conservative-pairing patterns that catch internal-phase leaks while leaving generic design language alone. The `stealth|skunkworks|moonshot` family must be paired with an asset / build noun (`launch|product|asset|hero|build|alpha|beta|prerelease|prototype`) — `stealth-launch hero` fires the gate, `stealth fighter aesthetic` does not. The `v\d+(?:\.\d+)?` family must be paired with a phase keyword (`stealth|internal|prerelease|preview`) — `v3-stealth marketing` fires, `v3 update` does not.
- `scripts/test_codex_image_import.py` 16 → 19 tests: 2 positive (stealth-launch noun-paired, v3-stealth versioned-phase) plus 1 negative (the must-not-false-positive contract — `stealth fighter aesthetic, v3 update marketing visual` must pass `0`).
- `references/security-config.md §1.5` table gains 2 rows + the *Conservative-pairing rule* paragraph, naming the trade-off explicitly: a determined leaker using a bare keyword passes the gate; the WebSearch manual checklist (§1.3) plus per-call user approval is the policy of last resort.
- HANDOFF.md §1 verification block + this file's §8 Validation block bumped to `19/19` for codex-image-import.

### 2026-05-10 · Step 4.3 — GitHub Actions CI activated

- `.github/workflows/sanitizers.yml` ships the reference workflow on this repo's GitHub. Triggers: push to `master` / `main` and any pull request. Steps: SVG sanitizer (18 tests), scan_assets self-check (13), codex-image-import gate (19), animations easing (19, Node), JSON template lint (settings + brand-spec example), advisory asset scan over `assets/`. Pinned `actions/checkout@v4`, `actions/setup-python@v5`, `actions/setup-node@v4`. `permissions: contents: read` so the workflow cannot push back into the repo. No untrusted GitHub-event input is interpolated into `run:` steps — workflow is injection-safe per the standard guidance.
- `references/ci-template.md` updated: the live workflow path is now named (`.github/workflows/sanitizers.yml`); test counts in the *What the CI does* table reflect Steps 3.3 + 4.2 (18 / 13 / 19 / 19); the GitHub Actions snippet matches the live workflow body. The non-GitHub CI host snippets (GitLab CI, internal Buildkite / Bitbucket migration notes) are preserved as the alternate-platform path.
- Validated locally: 18/13/19/19 + JSON OK before commit. The first run of the workflow on GitHub will confirm the full chain on Ubuntu / Python 3.10 / Node 22.

### 2026-05-10 · License change — MIT → Apache 2.0

- `LICENSE` replaced with the Apache License 2.0 standard text plus an appendix-style maintainer note. `NOTICE` added (required by Apache §4(d)) — single-author clean-room rewrite, with explicit pointers to `PROJECT-PLAN.md §2` (23 carry-over files inventory) and `PROJECT-PLAN.md §7` (verbatim sections in `references/design-styles.md §15–18` and `references/scene-templates.md §06–09`).
- **Rationale**: Apache 2.0 adds an explicit patent grant (§3) and trademark / contributor clarity (§6) that MIT does not. The change is unrelated to upstream / predecessor licensing — the upstream `alchaincyf/huashu-design` skill carries a separate Personal-Use license; this repository is a clean-room rewrite that does not derive from it; that upstream license is unaffected by the Apache 2.0 grant recorded here.
- **License-clean evidence reaffirmed**: the 23 carry-over files (`PROJECT-PLAN §2`) and the verbatim domain-pack sections (`§7.1`, `§7.2`) are all the maintainer's own original work — the maintainer holds the copyright and is free to dual-license that work into this repo under Apache 2.0. See the per-step decisions log entries above for the read-scope discipline followed throughout Step 2 / Step 3 (predecessor prose was opened only at the explicit verbatim-allowed sections; license-clean evidence recorded per commit).
- Doc updates: HANDOFF.md §0 banner + §14 closing list; README.md license section + directory-tree comment; this PROJECT-PLAN.md §1 result line; CHANGELOG.md `[Unreleased]` gets the matching entry. Historical Step 1 mentions of "MIT" inside this decisions log (entries dated 2026-05-09) are left unchanged — the decisions log is append-only and those statements were correct at the time of writing.

### 2026-05-12 · Step 7 — onboarding (`QUICKSTART.md`) + plugin install path (`.claude-plugin/`)

- Triggered by user question: *"huashu-design은 어떻게 설치해서 유저가 사용할 수 있도록 지원하고 있어? 그 방식은 편하다고 생각해? claude-design-skill 을 다수의 멀티 유저가 어떻게 쉽게 설치하고, mcp 까지 쉽게 사용할 수 있어?"* The comparison surfaced two gaps:
  1. huashu-design ships a 10-minute walkthrough (`QUICKSTART.md`) but assumes single-user, doesn't cover MCP setup, and treats agent-host installation as out-of-scope. Our previous Quick start in README was 5 lines — even less.
  2. Neither repo offered a `claude plugin install` path, so each teammate had to manually clone + copy files.
- **7.1 — `QUICKSTART.md`** (~ 320 lines, 9 sections). Three explicit audience paths:
  - *Individual designer / agent user*: §1 clone + verify (7-suite 108 tests) → §2 viewer smoke (no token / no Figma account) → §3 settings drop-in → §4 brand stamp → §5 first deliverable.
  - *Team lead onboarding 5-20 designers*: §1–§5 → §6 *Team rollout* — 4 sub-actions (mirror to internal git host with pointer to `CONTRIBUTING.md`, ship a single team-wide `team-brand-spec.json` to the design-project repo not the skill repo, wire the Figma MCP server via `references/figma-mcp-setup.md`, optional plugin install path).
  - *Read-only reviewer with no Claude Code seat*: §7 — clone, read the four canonical docs in order, run 108 tests, run viewer smoke. Lets a reviewer make a yes/no adoption decision without any agent setup.
  - §8 troubleshooting table (7 rows mapping symptom → likely cause → fix).
  - §9 next-steps router into SKILL.md / figma-workflow / codex-design-workflow / CONTRIBUTING / PROJECT-PLAN §7 / web3-game-style-stats.
- **7.2 — `.claude-plugin/plugin.json`** (root) declares the skill as a Claude Code plugin (`name: "claude-design-skill"`, `version: "0.1.0"`, Apache-2.0, homepage + repository pointers, 10 keywords for marketplace search).
- **7.2 — `.claude-plugin/marketplace.json`** (root) makes the repo itself a *single-plugin marketplace*. `plugins[0].source: "."` points at the same repo root. Teams add once:

  ```bash
  claude plugin marketplace add 0xmhha/claude-design-skill  # or internal mirror URL
  claude plugin install claude-design-skill
  ```

  After that any teammate runs the second line and the skill lands in their Claude Code config. The marketplace.json schema follows the pattern observed in `buddy` (`~/.claude/plugins/marketplaces/buddy/.claude-plugin/marketplace.json`) and `claude-plugins-official`.
- **Doc + README propagation**: README directory tree gains `QUICKSTART.md` + `.claude-plugin/` rows. README Quick start section rewritten to point at `QUICKSTART.md` first and include both the `git clone` + `claude plugin marketplace add` paths. HANDOFF.md §0 Active version line bumped + new §0 *Step 7* block mirrors the sub-step ship details.
- **License-clean**: doc + manifest only. No upstream paraphrase; the QUICKSTART structure (audience splits, verification-first, MCP setup in §6) is original framing — huashu-design's `QUICKSTART.md` is single-audience and does not surface plugin / read-only paths.
- **Validated**: 108/108 tests still OK (no test-affecting code changed); manifest files parse as valid JSON; `.claude-plugin/` layout mirrors the structure used by `buddy` and the Anthropic-official plugins surveyed.

### 2026-05-12 · Step 6 — Figma support hardening (viewer + MCP setup + image-export + page-organization)

- Triggered by a user-requested comparison vs the upstream huashu-design that surfaced four gaps in our Figma offering:
  1. No figma viewer for review-without-Figma scenarios.
  2. MCP server setup / auth / detection contract undocumented.
  3. Codex PNG → Figma placement workflow missing (the Phase 6.3 placeholder in `codex-design-workflow.md`).
  4. Page / section / folder *organization* conflated with componentization, gap surfaced by the Step 5 evidence pass and confirmed by the comparison.
- **6.1 — `figma-viewer.py` + minimal HTML viewer**: 360-line stdlib-only script reads Figma REST (`X-Figma-Token`) or a local fixture and emits a *single self-contained HTML page* — every CSS / JS inline, no external `<link>` or `<script src>`. Renders CANVAS pages as keyboard-navigable sections (← / → / 1..9 / `d` for dark chrome). Per-node mapping: FRAME / COMPONENT / INSTANCE / GROUP → fill + corner-radius div; RECTANGLE / ELLIPSE / VECTOR → shape div (ellipse uses `border-radius:50%`); TEXT → `<p>` with `fontFamily` / `fontWeight` / `fontSize` / `lineHeightPx`; unknown types → dashed-outline placeholder labelled with the type so the layout slot survives without claiming it was painted. 15 fixture-based tests; `test_text_family_with_quote_chars_is_escaped` pins the defence-in-depth invariant that a hostile `Inter"><script>alert(1)</script>` payload from Figma cannot break out of an inline style attribute. CI gains the `figma-viewer tests` step. Total tests **93 → 108**.
- **6.2 — `references/figma-mcp-setup.md`**: contract-level (not implementation-tied) doc covering MCP server choice (framelink / Dev Mode / community), PAT generation + scope, env wiring (`FIGMA_API_KEY`) with a Claude Desktop / Code JSON example, detection contract (table of `figma_*` tool names mapped to skill features + which are required vs optional), verification smoke (open Figma → select a node → ask the agent), MCP-absent fallback per workflow (selection / rename / componentize / brand spec / viewer all routed). License-clean: no upstream paraphrase; written from a comparison of public MCP server READMEs.
- **6.3 — `references/figma-image-export.md`**: Codex PNG → Figma placement. Two paths (MCP-aware vs MCP-absent), shared provenance schema with 11 fields where the first 8 come for free from `scripts/codex-image-import.py` and the last 3 (`figma_file_key` / `figma_node_id` / `placed_at`) are appended at placement. Naming convention `<role> · <where>` matches `figma-layer-naming.md`. Security posture re-stated: codename gate already runs at *generation* time (script's exit 4 hard-fail), C2PA strip already happens at *import* time, watermark (if enabled) is composed into the PNG bytes *before* upload so it can't be deleted as a separate Figma layer.
- **6.4 — `references/figma-page-organization.md`**: distinct from `figma-component-grouping.md`. Three levels (Page / Section / Layer-naming), three recommended page-layout shapes (single-product / multi-product / design-exploration), section heuristics (triggers + naming convention `<category> · <count>`), folder-slash convention applied consistently across token / template / component names, 5-step idempotent workflow that hands off to `figma-layer-naming.md` for the rename step, sample MCP-absent rename plan as a table. The doc *explicitly* doesn't move frames around the canvas, doesn't promote to components (sibling concern), doesn't delete (move-to-Archive instead).
- **SKILL.md routing table** gains four new rows (figma-viewer + figma-mcp-setup + figma-image-export + figma-page-organization). Status header bumped to "Step 1–6 shipped (2026-05-10 → 2026-05-12)". HANDOFF active version line + a new §0 *Step 6 — Figma support hardening* block mirrors the four sub-step summaries plus the new test total.
- **`references/ci-template.md`** updated: `What the CI does` table gains the figma-viewer row; all four CI snippets (GitHub Actions + GitLab + Bitbucket + Buildkite) gain the matching `test_figma_viewer.py` step. The 6-suite chain becomes a 7-suite chain.
- License-clean: doc-only for 6.2 / 6.3 / 6.4; 6.1's viewer code is original (no upstream paraphrase; renderer logic shares the FILL hex-rounding helper used by `figma-to-brand-spec.py` but the layout / HTML template / keyboard surface are new). New fixture is synthetic, constructed to render to the `#5B7CFA` Step 5.2 accent.
- Validated: 18 + 13 + 19 + 19 + 11 + 13 + 15 = **108 tests OK**; viewer smoke (`figma-viewer.py --fixture scripts/fixtures/figma_viewer_sample.json --output /tmp/viewer.html`) writes a 145-line self-contained HTML in 2 page(s); all three updated CI snippets (GitLab / Bitbucket / Buildkite) reviewed for syntax against each host's docs.

### 2026-05-11 · Step 5.6 — §6 (c) guides shipped (mirror + non-GitHub CI templates)

- After §6 restructured into 3 buckets in Step 5.5, the (c) bucket ("repo-external operations") still read as bare TODOs. This entry fills the *guide-ships-here* side so adopters have copy-paste-ready instructions even though the doing happens outside the repo.
- **`references/ci-template.md`** updated:
  - *What the CI does* table grew `init-brand` row from 9 → 11 tests (was stale since Step 5.1) and gained a new `figma-to-brand-spec extractor tests` row covering the 13-test fixture suite.
  - **GitLab CI snippet** rewritten — was a 4-step demo missing every Step 5 test. Now runs the full 6-suite chain (svg-sanitize · scan_assets · codex-image-import · animations-easing · init-brand · figma-to-brand-spec) plus both JSON parses and the advisory asset scan. Includes the `nodesource setup_22.x` install so `node scripts/test_animations_easing.js` runs on the default `python:3.10` image.
  - **Bitbucket Pipelines snippet** added — uses YAML anchors (`&guards` / `*guards`) so both the `default` push pipeline and `pull-requests` run the same step block.
  - **Buildkite snippet** added — uses the `docker#v5.11.0` plugin with the same `python:3.10` image and the identical command list.
  - **Translation notes** section added at the bottom: GitHub Enterprise (identical to the reference workflow), Jenkins (declarative pipeline pattern), CircleCI / Drone / Other (same shell, different YAML). Plus four porting principles (pin Python 3.10 + Node 22, hard-fail on test exit codes, asset scan stays advisory until catalog is curated, Codex CLI integration is out of scope for CI).
- **`CONTRIBUTING.md §For fork operators`** rewritten:
  - Acknowledges the Step 5 state ("Default Studio identity ships out of the box, adopters override").
  - Numbered checklist 1 → 11 covering: identity overrides (1-5), security extensions (6-8), mirror to internal git host (9 — full bash recipe), LICENSE / NOTICE replacement (10), CI port (11 — pointer to the new `ci-template.md` templates).
  - Mirror recipe is concrete and complete: create empty private repo → `git remote add internal …` → `git push internal master --tags` → `git ls-remote internal | head -5` → tag divergence point with the date.
  - Test count corrected `78 → 93` in the PR-rules block.
- **`PROJECT-PLAN.md §6 (c)`** rewritten to acknowledge guides-ship-here; checkboxes stay `[ ]` because they are *adopter actions*, not repo work.
- License-clean: doc-only change; no code, no upstream prose. New CI snippets are written from the running GitHub Actions workflow + each CI host's public docs (GitLab CI / Bitbucket Pipelines / Buildkite reference). Mirror recipe is generic git semantics — no upstream paraphrase.
- Validated: 93 tests OK after the edits; `ci-template.md` snippets manually verified shell-syntax-valid; CONTRIBUTING `mirror` snippet manually traced (dry-run `git remote add` wording).

### 2026-05-11 · Step 5.5 — Default Studio identity + section 6 restructure

- User flagged that the §6 (b) framing read like the repo was incomplete on Step 5.1's identity slots — *"P3 의 내용 모두 필요한데… 이것이 default 같은것으로 사용되는것"*. The token-side defaults from Step 5.1 / 5.2 were correct, but `team.*` / `brand.*` / `logo.*` were still placeholders ("Example Studios"), which made the *whole* spec look incomplete at a glance.
- **Default Studio identity** stamped into `assets/team-brand-spec.default.json`:
  - `team.company = "Default Studio"`, `team.division = "Game / Web3 product (fictional default)"`, `team.design_repo_url = ""` (per-fork).
  - `brand.name = "Default"`, `brand.tagline_short = "Design that ships."`, `brand.tone_keywords = ["precise", "expressive", "credible"]` (anchored to the 11-service evidence common ground: Uniswap's utility / Coinbase's trust / Phantom's expressiveness).
  - `brand.forbidden_zones` rewritten as evidence-anchored anti-slop guards (rainbow gradients, cyberpunk-neon reflex, emoji-as-icon, generic glassmorphism, default Inter-16-1.5 typography applied without intent) — pulled from the SKILL.md anti-AI-slop checklist.
  - `watermark.text = "Default Studio · {year}"` (matches `format`).
  - `logo.primary` / `logo.primary_inverse` / `logo.wordmark` / `logo.icon` point at real SVG files under `assets/default-brand/` (see below).
  - `product_assets.*` and `ui_screenshots.*` paths are now `""` empty — Default Studio is fictional, so it has no real product imagery; adopters fill these in for their real product, or delete the block.
  - `design_system.tokens_repo_url` / `figma_library_url` set to `""` empty (per-fork URLs).
- **Logo SVG placeholders** at `assets/default-brand/`:
  - `logo.svg` — 24×24 square mark, accent-coloured fill with a stylised `D` glyph.
  - `logo-white.svg` — inverse for dark backgrounds.
  - `wordmark.svg` — 96×24 (4:1 aspect, matching the median across the 11-service sweep) with mark + `DEFAULT` text.
  - `icon.svg` — 16×16 small mark variant.
  - All 4 files pass `scripts/svg-sanitize.py` clean (no scripts, no foreignObject, no external refs; only `rect` / `path` / `text` / `tspan` with stripe-safe attributes). All 4 pass `scripts/scan_assets.py --dir assets/default-brand/` with verdict `clean`.
- **§6 restructure** — the old `(a) shipped here / (b) per-fork actions owned by the adopter team` split collapsed two distinct categories. Replaced with three buckets:
  - `(a) Repo-level defaults shipped here` (automation + bootstrap — unchanged).
  - `(b) Default-ships-here · adopter overrides` — *new* bucket for slots where a default value *does* exist (identity, codename patterns, watermark policy, public asset hosts) and the only adopter action is to override toward their brand. All `[x]`.
  - `(c) Repo-external operations` — items that *cannot* have a default because the action happens outside the repo (mirror to internal git host, port CI to another host). Still `[ ]`, by design — adopter-owned.
- This restructuring is the substantive answer to the user's question. Nothing functional is missing in the repo; the prior framing made it *read* like something was missing.
- Validated: 18 + 13 + 19 + 19 + 11 + 13 = 93 tests OK; `assets/team-brand-spec.default.json` parses cleanly with the new structure; `scan_assets.py --dir assets/default-brand/` reports clean for all 4 new SVGs; `svg-sanitize.py` accepts each without stripping.

### 2026-05-11 · Step 5.4 — verify + doc consistency pass (Step 5 complete)

- **SKILL.md routing table** gains two rows: *Web3 + game style stats* pointing at `references/web3-game-style-stats.md` (the evidence behind the default values), and *Figma → team-brand-spec extractor* pointing at `references/figma-to-brand-spec.md` + `scripts/figma-to-brand-spec.py`. Placed right after the *Brand spec field reference* row so the three Step 5 docs cluster together in the routing table.
- **SKILL.md status header** bumped from "Step 1–4 shipped" to "Step 1–5 shipped (2026-05-10 → 2026-05-11)" with a one-line summary of what Step 5 added (operational defaults from evidence sweep + Figma ingestion path).
- **HANDOFF.md §0 Active version** flipped to "Step 1–5 shipped"; the §0 *Step 5 — in progress* block rewritten as *Step 5 — shipped 2026-05-11* with each sub-step marked ✅ and the total test count (93) stated. Section name change makes the *shipped* status the first thing a fresh-session agent reads in HANDOFF after the briefing.
- **PROJECT-PLAN.md §6.5** title changed from "in progress" to "complete"; sub-step checkboxes all marked `[x]` with commit references (`4c3d7ef`, `de2b3f2`).
- **CHANGELOG.md `[Unreleased]`** gets the Step 5 entry (Step 5.1 already had its own; Step 5.2 / 5.3 / 5.4 entries added under one *Step 5* changelog header for release-log clarity).
- **Validation**: full guard chain re-run before this commit — 18 + 13 + 19 + 19 + 11 + 13 = **93 tests OK**; all JSON templates parse (`assets/team-brand-spec.default.json`, `examples/dot-claude-settings.json`, `scripts/fixtures/figma_minimal.json`); `scan_assets.py --dir assets/` clean for every showcase PNG.
- **Step 5 retrospective** (so the next session has the design rationale at hand):
  - The decision *not to mimic any single service's brand color* was the highest-leverage call. Without it, every default-mode generation would have looked like Coinbase, OpenSea, or Phantom by reflex. `#5B7CFA` sits in a deliberate gap.
  - Two-slot typography (display + body) + the `_legacy` aliases preserved backwards compatibility *and* enabled the new nested layout — a pure rename would have broken every skill-internal reader of the flat keys.
  - Fixture-based tests for the Figma extractor are the difference between "CI gates the contract" and "tests run only when someone has a token." That choice multiplied the value of the 13 tests.
  - `_source` attribution as a *first-class field* in the JSON (not just a comment) lets adopters trace any value back to its origin — Uniswap Spore for status tokens, the 11-service sweep for the accent decision, etc. Future strip rules must continue to preserve `_source` (the test `test_status_source_attribution_preserved` pins this invariant).
- **What's next** (post-Step-5): no further repo-side Step is planned. Per-fork adopter actions (§6 (b)) remain `[ ]` by design. The skill is ready for adopter use; the next milestone is real-world usage feedback.

### 2026-05-11 · Step 5.3 — figma-to-brand-spec extractor

- `scripts/figma-to-brand-spec.py` (≈ 280 lines, stdlib only) reads a Figma file via the public REST API (`GET /v1/files/{file_key}`, `X-Figma-Token` header), walks the document tree, resolves nodes that reference named styles, and emits a JSON spec compatible with `assets/team-brand-spec.default.json`. Color styles round Figma's 0-1 RGB to 0-255 HEX; text styles capture `family` / `weight` / `size` / `line_height_px`. Unknown style names land in `_meta.unmapped_styles` (never silently dropped — adopters need visibility into what was skipped).
- **Naming convention** chosen as the slot-mapping contract: `color/<group>/<token>` → `colors.<group>.<token>`, `text/<role>/family` → `typography.<role>.family`, `effect/<token>` → `design_system.shadow_tokens.<token>`. Case-insensitive prefix table inside the script; deliberately strict (no fuzzy matching) so adopter Figma libraries either match the convention or surface their misses in `_meta`. The doc walks adopters through renaming their styles to land in the right slots.
- **Merge-by-default policy**: extracted slots overlay `assets/team-brand-spec.default.json` so untouched groups (`iconography`, `motion`, etc.) keep the evidence-anchored defaults from Step 5.2. `--no-merge` disables for review (see exactly what Figma defines); `--base <path>` accepts a custom carrier to layer over. The starter merge is the difference between a usable carrier on first run and a sparse half-spec that re-introduces the Step 5 motivation (LLM filling gaps with imagination).
- **Provenance**: every run records `_meta.extracted_from` (Figma `name`), `_meta.extracted_at` (Figma `lastModified` — same shape adopters can diff to detect drift), `_meta.tool` (this script path). The `_source` attribution fields from `team-brand-spec.default.json` survive the merge.
- **Fixture-based tests** so CI runs without network: `scripts/fixtures/figma_minimal.json` mimics a Figma file response with 6 named styles (4 mapped + 1 deliberate-mismatch + 1 unstyled black rect) across both FILL and TEXT style types. `scripts/test_figma_to_brand_spec.py` ships 13 tests covering the happy path (color + text mapping, hex rounding accuracy `#5B7CFA` from `0.357/0.486/0.980`, surface tokens, status tokens), unmapped preservation, unstyled-node leakage guard, metadata recording, merge / no-merge modes, missing-token + missing-fixture + invalid-JSON + output-collision error paths, `--force` overwrite, and round-trip JSON validity.
- **CI**: `.github/workflows/sanitizers.yml` gains the matching step. README directory tree and guard-chain command list updated. README status line moved from "Step 1-4 shipped" to "Step 1-4 shipped · Step 5 in progress" since 5.4 (verify + final doc pass) is still pending.
- **Doc**: `references/figma-to-brand-spec.md` (8 sections, ≈ 200 lines) — extraction model, Figma naming convention, usage table (one-shot / fixture / merge / no-merge / custom base), reference public Figma files (Material 3 Design Kit + iOS 18 community kit), output shape with provenance, out-of-scope boundaries (no round-trip, no CSS scraping, no image extraction, no auto-reextraction), license posture.
- **Out of scope deliberately**: Figma Variables API (`/v1/files/{key}/variables/local`) — the older Styles surface is universally supported across all paid + community files; Variables is paid-tier-only and not all adopters have it. Variables can be a v2 of this script.
- **License-clean**: script itself is original. The naming convention (`color/group/token`) is a generic convention used across multiple public design systems; not derived from any specific upstream. The fixture's RGB values for `accent.primary` are constructed to round to `#5B7CFA` (the Step 5.2 default) — fixture data is synthetic, not lifted from any real Figma file.
- Validated: `python3 scripts/test_figma_to_brand_spec.py` 13/13 OK. Full guard chain (18 + 13 + 19 + 19 + 11 + 13 = 93 tests) all OK. JSON template parses; smoke run against the fixture writes a parseable spec with correct hex and merge behaviour. Next: Step 5.4 (final verify + cross-doc sync + SKILL.md routing pointer to the new extractor doc + CHANGELOG `[Unreleased]` entry).

### 2026-05-11 · Step 5.1 — team-brand-spec.default.json + init-brand rewire

- `assets/team-brand-spec.example.json` removed; `assets/team-brand-spec.default.json` is the new operational default. Values pulled from `references/web3-game-style-stats.md` *Aggregate analysis* (Step 5.2):
  - **Color**: nested `surface` / `text` / `accent` / `status` groups for light + dark, plus flat aliases (`primary`, `background`, `ink`, `muted`, `hairline`) preserved for backwards compatibility with old skill code. `accent.primary` is `#5B7CFA` — deliberately not anyone's brand color from the 11-set. `status.*` cites Uniswap Spore in a `_source` field that survives the meta-strip.
  - **Typography**: two-slot pattern — `display` and `body` each carry `family` / `weights` / `system_stack`. Inter (OFL) is the default `family`; the system stack matches Uniswap's web fallback verbatim (cited via `_source` on `body`). `mono.system_stack` directly cites Uniswap's mono stack. Legacy flat `_legacy.display` / `_legacy.body` / `_legacy.mono` aliases preserved so old skill code that read the flat shape still works.
  - **New top-level groups**: `iconography` (Lucide primary, Phosphor fallback, 1.75 px stroke, 12 / 16 / 20 / 24 / 32 size scale) and `motion` (100 / 200 / 300 / 500 ms duration + Material standard / emphasized / decelerated easing curves).
  - **Spacing**: `[0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 96]` — pruned Uniswap-style scale.
  - **Radius**: `[0, 4, 8, 12, 16, 24]` + `pill 9999` + semantic shortcuts (`button 8`, `input 8`, `card 12`, `modal 16`).
  - **Asset hosts**: `public` array matches `examples/dot-claude-settings.json:permissions.ask` exactly (Lucide / Phosphor / MDN); `internal` is `[]` (per-fork slot); legacy `hosts` retained for the older shape.
- `scripts/init-brand.py`: `DEFAULT_EXAMPLE` renamed to `DEFAULT_SOURCE`; CLI gets `--source` as the canonical flag with `--example` preserved as an alias so pre-Step-5.1 invocations still work. Help text and error messages updated to say "source" instead of "example". `PLACEHOLDER_FIELDS` reshaped for the new nested structure — `colors.accent.primary` replaces flat `colors.primary` / `colors.background`; `typography.display.family` / `typography.body.family` replace flat aliases; `approved_asset_hosts.internal` added as the per-fork onboarding hint.
- `scripts/test_init_brand.py`: 9 → 11 tests. Two new cases: `test_color_token_groups_present` asserts both nested groups (`surface` / `text` / `accent` / `status`) and the flat legacy aliases are preserved, plus pins `accent.primary == #5B7CFA` so the deliberate-neutral choice can't drift back to a brand color. `test_status_source_attribution_preserved` asserts the `colors.status._source` Uniswap attribution survives the meta-strip (the strip targets `_meta` / `_note`; `_source` is an attribution field, not a guidance field). Existing `test_actual_fields_preserved` extended to require the four new top-level groups (`iconography`, `motion`, `design_system`, `approved_asset_hosts`).
- Doc + workflow propagation: every `team-brand-spec.example.json` reference in *active state* docs swapped to `*.default.json`:
  - `.github/workflows/sanitizers.yml` — JSON lint step.
  - `README.md` — directory tree + guard-chain command list.
  - `HANDOFF.md` — Step 5 in-progress block (marked ✅ shipped) + Step 4 per-fork action references + watermark policy reference.
  - `SKILL.md` — references routing table.
  - `references/brand-spec-fields.md` (header + 3 mentions), `references/security-config.md` (template note), `references/ci-template.md` (JSON-lint description + 2 snippets), `references/figma-brand-spec-import.md` (Related list), `references/figma-workflow.md` (Related list).
- Historical entries left as-is on purpose: `CHANGELOG.md` Unreleased + earlier sections describe the file at the time of writing (`*.example.json`); `PROJECT-PLAN.md §7 2026-05-10 Step 4.2 / Step 4.3 / Step 4.4` decisions-log entries similarly describe state at the time. The 2026-05-11 doc-path normalization policy (append-only with cross-link) applies — this entry above is the cross-link to the rename.
- License-clean: the new default carries `_source` attributions for any value lifted from a public design system (Uniswap Spore for status colors and the system / mono font stacks). Values originated as *facts* about a published system, not as code copies; the `_source` lines make the lineage auditable in the JSON itself.
- Validated: `python3 scripts/test_init_brand.py` 11/11 OK; full guard chain (18 + 13 + 19 + 19 + 11) all OK; both JSON templates parse; init-brand smoke test (`--target $TMP/team-brand-spec.json`) writes a parseable file with the new 4-group color block and the updated PLACEHOLDER_FIELDS guidance.

### 2026-05-11 · Step 5 plan sealed

- User decision (2026-05-11): elevate `team-brand-spec` from placeholder to operational default, source default values from evidence-based style analysis of trusted web3 + game services, and add a Figma → spec extraction path. Rationale: anti-AI-slop posture — defaults must reflect real production design, not LLM-imagined values; Figma is the actual day-to-day surface for adopter teams, so JSON hand-editing is a friction point.
- Reference service set fixed at 11 (web3 6 + game 5). Coinbase added on user request to widen the web3 sample beyond DEX / NFT / wallet / social — gives a CEX data point with strong trust-oriented design.
- Field scope: full spec coverage (core + iconography + watermark + logo defaults + asset host hints). Larger surface than minimum-viable; user picked completeness over speed because partial defaults invite the same "fill in the gaps with imagination" failure mode as no defaults.
- Sequence: 5.2 → 5.1 → 5.3 → 5.4. Evidence first, default file second so the default has citations behind every value; Figma tool third so it can validate against the same field shape; verify-and-doc last.
- This entry seals the plan in §6.5. Each sub-step gets its own decisions-log entry when it ships, recording evidence sources, aggregate methodology, and license-clean evidence.

### 2026-05-11 · README / SKILL drift sweep

- Audit pass on `README.md` against the tree state (post-Step-4 additions had not all propagated). Findings:
  - `README.md §What's in here` directory tree missing `scripts/init-brand.py` + `scripts/test_init_brand.py` and `assets/showcase-brand/README.md`. Added.
  - `README.md` *Run the full guard chain locally* command list missing `python3 scripts/test_init_brand.py # 9/9`, contradicting the headline "five suites · 18 + 13 + 19 + 19 + 9" on the status line. Added.
  - `README.md §License` short-form repo names (`0xmhha/huashu-design`, `alchaincyf/huashu-design`) replaced with Full URL (`<https://github.com/...>`) at the *location-identifier* slots, matching the 2026-05-11 doc-path normalization policy.
  - `README.md §Roadmap` first bullet still read *"v0.1.0-alpha (2026-05-09) — skeleton"* despite earlier scrub (`e82418d`). Relabeled to *"Step 1 (2026-05-09) — skeleton"* for consistency with the rest of the Roadmap.
- `SKILL.md` Status header still read *"v0.1.0-alpha · skeleton · 2026-05-09"* despite Step 1–4 being shipped. Replaced with *"Step 1–4 shipped · 2026-05-10"* + a short summary line that names the design-knowledge catalog, animation engine, and prebuilt showcases.
- `PROJECT-PLAN.md §3` opening sentence rewritten — *"deliberately empty in the v0.1.0-alpha skeleton"* → *"deliberately empty at the end of Step 1 (the initial skeleton)"* — same fact, no release-tag noise.
- Out of scope: `HANDOFF.md §0 Post-Step-4 follow-ups` line that names the *v0.1.0-alpha skeleton scrub* — that's a historical reference to commit `e82418d`'s scope, not an active claim about the current state, so it stays.
- License-clean: doc-only change. Tests rerun before commit: 18 / 13 / 19 / 19 / 9, all OK.

### 2026-05-11 · Doc path normalization (A-2 resolved)

- Policy decision (user, 2026-05-11): GitHub identifiers are written as **Full URL** (`<https://github.com/...>`) and local working directories use the **`<repo-root>`** placeholder. The append-only decisions-log gets a one-line update on past entries so the canonical repo location is consistent doc-wide.
- **HANDOFF.md**: 5 absolute paths replaced — `§0 Repo` header now points at <https://github.com/0xmhha/claude-design-skill> with a `<repo-root>` annotation; `§1` verification block `cd` line uses `<repo-root>`; `§4` validated-facts table renames the *Sibling repo path* row to *Predecessor repo (GitHub)* with URL; `§4` codex-CLI expected line drops the nvm install path and names PATH instead; `§12` *Files to read* predecessor-fork warning links to <https://github.com/0xmhha/huashu-design>. `§13` Glossary entries for *Predecessor fork* and *Upstream* gain URLs at the definition site.
- **PROJECT-PLAN.md**: §7 *2026-05-09 Step 1 complete* entry — the `Repo created at …` line now records the GitHub URL with a parenthetical noting that the original local path was on the author machine. Other historical entries reference repo names by short name (`huashu-design`), which remain unchanged because they are project-name references rather than location identifiers.
- Out-of-scope on purpose: short-form repo-name mentions inside prose (e.g. *"the predecessor at `0xmhha/huashu-design`"*) were not touched — those are name references, not path identifiers, and rewriting them to Full URL would degrade readability of the decisions log and §0 briefing. The Full URL is recorded at every *location identifier* slot (repo header, table rows, glossary, fork-warning anchor).
- License-clean: doc-only change. Tests rerun before commit: 18 / 13 / 19 / 19 / 9, all OK; both JSON templates parse.

### 2026-05-11 · Doc sync — HANDOFF / PROJECT-PLAN ↔ tree state

- Triggered by a fresh-session audit comparing `HANDOFF.md` and `PROJECT-PLAN.md` against the actual tree. Eight commits (`e82418d` → `3cd7e74`) had landed after the 2026-05-10 Step-4 close and were not reflected in the briefing docs; PROJECT-PLAN.md §6 Step-4 checkboxes were still all unchecked despite four of the items being shipped.
- **HANDOFF.md**: `Last updated` bumped to 2026-05-11; `Active version` line names the post-Step-4 follow-ups; §0 gains a *Post-Step-4 follow-ups already in tree* paragraph that lists the license change (MIT → Apache 2.0 + NOTICE), the `scripts/init-brand.py` fork-bootstrap helper, the repo-hygiene additions (`SECURITY.md`, `CONTRIBUTING.md`, `.github/dependabot.yml`, `assets/showcase-brand/README.md`), and the stale-references scrub.
- **PROJECT-PLAN.md**: §2 Scripts table extended from 7 to 9 rows (init-brand + its test); §2 Authored-fresh table now reflects MIT → Apache 2.0 history on the `LICENSE` row and gains a *Post-Step-4 additions* sub-table covering `NOTICE`, `SECURITY.md`, `CONTRIBUTING.md`, `.github/dependabot.yml`, and the two `assets/showcase-brand/*.md` files. §6 Step 4 split into (a) repo-level defaults shipped (5 items, `[x]`) and (b) per-fork actions (6 items, `[ ]` — adopter-owned by design). §8 Validation block names the team-brand-spec JSON parse alongside the settings JSON, and the closing line records the 2026-05-11 full-chain pass (78 tests).
- License-clean: doc-only change; no new code, no upstream prose. Tests rerun before this commit: 18 / 13 / 19 / 19 / 9, all OK; both JSON templates parse; `scan_assets.py --dir assets/` reports clean for every showcase PNG.
- Items deliberately NOT touched in this pass: `HANDOFF.md §0` `Repo` path (still the original-author absolute path) — operational policy decision (preserve original-author path vs abstract). Surfaced as A-2 in the audit for a future session to decide. *Resolved in the 2026-05-11 doc-path normalization entry above.*

### 2026-05-10 · Step 4.4 — external asset hosts whitelist boost

- `examples/dot-claude-settings.json` `permissions.ask` gains 5 generic-public host entries (3 host families): Lucide icons (`unpkg` + `jsdelivr` mirrors, ISC), Phosphor icons (`unpkg` + `jsdelivr` mirrors, MIT), MDN reference (`developer.mozilla.org/*`, CC-BY-SA 2.5). All pinned to major versions (`@*`) for the package CDNs; MDN is wildcard-path on the documentation host.
- `references/security-config.md §1.1` allowlist table mirrors the same 3 host families with purpose + license columns. SRI integrity hash policy and HTTPS-only rule continue to apply.
- Internal team-specific hosts continue to live under §1.2 *Team-extensible additions* — that template stays untouched (no fork-author work in this commit, only the public allowlist boost).
- The version stamp inside `_template_meta` bumped `2026-05-09 → 2026-05-10`.
- Validated: 18/13/19/19 regression + JSON template parse all still OK.

---

## 8. Validation

Before each step is marked done:

```bash
python3 scripts/test_svg_sanitize.py        # must be 18/18 OK
python3 scripts/test_scan_assets.py         # must be 13/13 OK
python3 scripts/test_codex_image_import.py  # must be 19/19 OK
node    scripts/test_animations_easing.js   # must be 19/19 OK
python3 scripts/test_init_brand.py          # must be  9/9  OK
python3 scripts/scan_assets.py --dir assets/  # must list 'clean' for every file
python3 -c "import json; json.load(open('examples/dot-claude-settings.json'))"
python3 -c "import json; json.load(open('assets/team-brand-spec.default.json'))"
```

Step 1 validation: SVG / scan_assets / codex-image-import / JSON all green on 2026-05-09.
Step 3.3 added animations-easing (19/19). Post-Step-4 added init_brand (9/9).
Last full-chain pass: 2026-05-11 (18 + 13 + 19 + 19 + 9 = 78 tests, all OK; advisory asset scan clean for all 16 showcase PNGs).
