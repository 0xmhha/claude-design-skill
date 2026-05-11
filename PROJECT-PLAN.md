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
| `assets/team-brand-spec.example.json` | Phase 1 Group A (replaces upstream `personal-asset-index`) |
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

The skill body — design knowledge, scenes, workflows — was deliberately empty in the v0.1.0-alpha skeleton. Rationale: those sections in the upstream skill are the parts that risk being "substantial derivative" if copied or paraphrased. Authoring them from scratch with our own voice and our own taxonomy keeps the project license-clean and lets us tailor the body to game / web3 design needs.

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

Step 4 splits cleanly into **(a) repo-level defaults shipped here** and **(b) per-fork
actions owned by the adopter team**. (a) is done; (b) is by design left empty in
this public repo so it carries no team-specific text.

### (a) Shipped in this repo (defaults + bootstrap)

- [x] **Default codename pattern catalog** — `scripts/codex-image-import.py:DEFAULT_CODENAME_PATTERNS` ships 4 conservative-pairing patterns; `references/security-config.md §1.5` mirrors them with the *Conservative-pairing rule* paragraph. (`eb33448`, 2026-05-10)
- [x] **Default `watermark.enabled` policy** — `assets/team-brand-spec.example.json` ships `enabled: false`; `references/brand-spec-fields.md §watermark` documents the keep-it-off-until-explicitly-approved policy. (2026-05-10)
- [x] **Default public asset host allowlist** — `examples/dot-claude-settings.json:permissions.ask` and `references/security-config.md §1.1` ship 5 generic-public host entries (Lucide / Phosphor CDN mirrors + MDN). (`2ea3bb8`, 2026-05-10)
- [x] **GitHub Actions CI activated** — `.github/workflows/sanitizers.yml` runs the full guard chain (18 + 13 + 19 + 19 + JSON + advisory asset scan) on every push to `master` / `main` and every pull request. (`d5dba7b`, 2026-05-10)
- [x] **Fork-bootstrap helper** — `scripts/init-brand.py` (+ 9/9 tests) stamps a per-team brand carrier from `assets/team-brand-spec.example.json` so adopters can bootstrap without hand-editing JSON. (`62c0928`, 2026-05-10)

### (b) Per-fork actions (adopter team owns)

These are intentionally left as TODO in this repo and become checkboxes for the
team that adopts the skill into an internal context.

- [ ] Replace placeholder values in `team-brand-spec.json` (logo, colors, typography stack) — use `scripts/init-brand.py` to stamp the carrier file.
- [ ] Add the team's codename namespace to `references/security-config.md §1.5` and `scripts/codex-image-import.py:DEFAULT_CODENAME_PATTERNS`.
- [ ] Decide `watermark.enabled` policy for the team (default ships disabled; flip only with explicit approval).
- [ ] Add internal asset hosts to `references/security-config.md §1.2 Team-extensible additions` and `examples/dot-claude-settings.json:permissions.ask`.
- [ ] Mirror to the team's internal git host. Once internal-only, this README and the LICENSE may need replacement per team policy.
- [ ] Port `references/ci-template.md` to the internal CI host (GitLab CI / Bitbucket / Buildkite) — sanitizer regression tests + JSON lint as hard-fail; asset scan as advisory. The reference GitHub Actions workflow is already live for public CI.

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

### 2026-05-11 · Doc sync — HANDOFF / PROJECT-PLAN ↔ tree state

- Triggered by a fresh-session audit comparing `HANDOFF.md` and `PROJECT-PLAN.md` against the actual tree. Eight commits (`e82418d` → `3cd7e74`) had landed after the 2026-05-10 Step-4 close and were not reflected in the briefing docs; PROJECT-PLAN.md §6 Step-4 checkboxes were still all unchecked despite four of the items being shipped.
- **HANDOFF.md**: `Last updated` bumped to 2026-05-11; `Active version` line names the post-Step-4 follow-ups; §0 gains a *Post-Step-4 follow-ups already in tree* paragraph that lists the license change (MIT → Apache 2.0 + NOTICE), the `scripts/init-brand.py` fork-bootstrap helper, the repo-hygiene additions (`SECURITY.md`, `CONTRIBUTING.md`, `.github/dependabot.yml`, `assets/showcase-brand/README.md`), and the stale-references scrub.
- **PROJECT-PLAN.md**: §2 Scripts table extended from 7 to 9 rows (init-brand + its test); §2 Authored-fresh table now reflects MIT → Apache 2.0 history on the `LICENSE` row and gains a *Post-Step-4 additions* sub-table covering `NOTICE`, `SECURITY.md`, `CONTRIBUTING.md`, `.github/dependabot.yml`, and the two `assets/showcase-brand/*.md` files. §6 Step 4 split into (a) repo-level defaults shipped (5 items, `[x]`) and (b) per-fork actions (6 items, `[ ]` — adopter-owned by design). §8 Validation block names the team-brand-spec JSON parse alongside the settings JSON, and the closing line records the 2026-05-11 full-chain pass (78 tests).
- License-clean: doc-only change; no new code, no upstream prose. Tests rerun before this commit: 18 / 13 / 19 / 19 / 9, all OK; both JSON templates parse; `scan_assets.py --dir assets/` reports clean for every showcase PNG.
- Items deliberately NOT touched in this pass: `HANDOFF.md §0` `Repo` path (still `/Users/kevin/...`) — operational policy decision (preserve original-author path vs abstract). Surfaced as A-2 in the audit for a future session to decide.

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
python3 -c "import json; json.load(open('assets/team-brand-spec.example.json'))"
```

Step 1 validation: SVG / scan_assets / codex-image-import / JSON all green on 2026-05-09.
Step 3.3 added animations-easing (19/19). Post-Step-4 added init_brand (9/9).
Last full-chain pass: 2026-05-11 (18 + 13 + 19 + 19 + 9 = 78 tests, all OK; advisory asset scan clean for all 16 showcase PNGs).
