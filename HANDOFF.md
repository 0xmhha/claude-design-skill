# HANDOFF · Session Context for the Next Agent

> **Read this BEFORE you do anything else.** This file exists because the
> next session has no memory of the prior work. Skipping it costs tokens
> and creates rework — the failure mode this document was written to
> prevent.

**Last updated**: 2026-05-11
**Active version**: Step 1–4 shipped (2026-05-10) + post-Step-4 doc/policy follow-ups (2026-05-10 → 2026-05-11)
**Repo**: `/Users/kevin/work/github/0xmhha/claude-design-skill`
**User**: 0xmhha (Kevin) — internal design platform R&D, game/web3 studio.
**Language preference**: Korean response with English technical terms allowed.

---

## 0 · The 60-second briefing (read all of it)

### What this project is

A **Claude Code-based design skill**, license-clean from day one, that turns design briefs into hi-fi prototypes through Figma MCP-driven precision edits and Codex CLI / gpt-image-2 image generation. **Three load-bearing security rules** govern every external call (see §3).

### Why it exists separately from the predecessor fork

The maintainer previously hardened a fork at `0xmhha/huashu-design`. That fork descends from `alchaincyf/huashu-design`, a personal-use-only design skill (commercial license: USD 1,800–3,500 from the upstream author). The fork is kept as **internal R&D and reference**, but **must not** be used in client deliverables, public products, or revenue-generating contexts.

This repo (`claude-design-skill`) is the **clean-room rewrite** chosen as option (b) from the fork's `PROJECT-PLAN.md §5.2`: rewrite from scratch, carry over only the maintainer's own work from the fork, never inherit upstream prose. **Apache-2.0 licensed** (changed from MIT on 2026-05-10 to gain Apache's explicit patent grant and contributor / trademark clarity). The upstream `alchaincyf/huashu-design` Personal-Use license is unaffected — this repo does not derive from it.

### What's already done (Step 1 → Step 4, 2026-05-09 → 2026-05-10)

- **Step 1 · skeleton (2026-05-09)** — 23 files carried over from the predecessor fork (maintainer-authored, Phase 1–4.2; no upstream prose) plus 6 fresh files (`SKILL.md`, `README.md`, `LICENSE`, `CHANGELOG.md`, `.gitignore`, `PROJECT-PLAN.md`).
- **Step 2 · SKILL.md body (2026-05-09 → 2026-05-10)** — all six body sections shipped: §6.1 Junior Designer workflow · §6.2 Anti-AI-slop checklist (12 patterns) · §6.3 App prototype rules + `assets/ios_frame.jsx` · §6.4 Slide deck conventions + `assets/deck_stage.js` · §6.5 Tweaks live-tuning system + `assets/tweaks.js` + `examples/tweaks-demo.html` · §6.6 Critique guide.
- **Step 3 · Design knowledge (2026-05-10)** — §7.1 `references/design-styles.md` (18 directions, 14 fresh + 4 game/web3 carry-over) · §7.2 `references/scene-templates.md` (9 templates, 5 fresh + 4 carry-over) · §7.3 animation engine (`assets/animations.jsx` + `assets/easing.js` + `references/animation-engine.md` + 19-test regression suite) · §7.4 `references/animation-best-practices.md` + `references/animation-pitfalls.md` · §7.5 SFX library **out of scope per user instruction (visual-only project)** · §7.6 `assets/showcase-brand/generated/` — 16 prebuilt PNG showcases via Codex CLI + gpt-image-2.
- **Step 4 · Internal-fit hardening (2026-05-10)** — §8.2 codename pattern catalog (conservative-pairing rule, 19/19 test) · §8.3 GitHub Actions CI active (`.github/workflows/sanitizers.yml`) · §8.4 external asset hosts whitelist boost (Lucide / Phosphor / MDN). Internal brand spec values, LICENSE / mirror policy, and internal-host additions remain **per-fork actions** (see §8 below).
- **Validation today**: 18 + 13 + 19 + 19 regression tests pass; both JSON templates parse; `scan_assets.py --dir assets/` reports clean for every shipped PNG.

### Post-Step-4 follow-ups already in tree (2026-05-10 → 2026-05-11)

These shipped after the original Step-4 close and are part of the *current* tree
state. They are not new "Steps"; they are doc/policy hygiene around what Steps
1–4 already produced.

- **License**: MIT → **Apache 2.0** + `NOTICE` per Apache §4(d). The §1 result line and the directory tree reflect this; the upstream `alchaincyf/huashu-design` Personal-Use license remains separate and unaffected.
- **Fork-bootstrap helper**: `scripts/init-brand.py` (+ `scripts/test_init_brand.py`, 9/9 OK) so adopters can stamp a per-team brand carrier without hand-editing JSON. Verification block now runs 5 test scripts (18 + 13 + 19 + 19 + 9).
- **Repo hygiene**: `SECURITY.md` (vulnerability disclosure pointer), `CONTRIBUTING.md`, `.github/dependabot.yml` (weekly Actions / pip / npm bumps). Status badges + tweaks-demo pointer added to `README.md`; the showcase gallery has its own `assets/showcase-brand/README.md` (preview catalog) alongside the existing `PROVENANCE.md`.
- **Stale-references scrub**: every "v0.1.0-alpha skeleton" mention removed; HANDOFF / README / PROJECT-PLAN consistency pass.

### What's intentionally NOT done

Two things, deliberately, and one of them by user instruction:

1. **SFX library (§7.5)** — retired by user instruction 2026-05-10 (this project is visual-only). The HANDOFF section carries an *out of scope* banner so future fresh-session agents do not start authoring. Carry-over text that mentions sound elsewhere (e.g. `references/design-styles.md §18` Onboarding-Game-Loop's verbatim "haptic + animation + sound") stays as aesthetic-spec mentions, not sourcing commitments.
2. **Per-fork brand integration (§8 actions that are not §8.2 / §8.3 / §8.4)** — `team-brand-spec.json` real values, internal codename additions to `DEFAULT_CODENAME_PATTERNS`, internal-host additions to the allowlist, LICENSE policy, internal git-host migration. These are per-fork actions; the templates and the security policy live in this repo, but the actual values are owned by the team that adopts the skill.

If you find yourself "filling in" a body section by reading the upstream and rewording it, **stop** — that's the failure mode the clean-room rewrite was built to avoid. Author from first principles, ask the user for references, restart the section. (The original Step 2 / Step 3 body work followed this rule throughout. See `PROJECT-PLAN.md` decisions log for the per-step license-clean evidence.)

---

## 1 · Run this verification first (1 minute)

Before reading anything else, confirm the environment is sane.

```bash
cd /Users/kevin/work/github/0xmhha/claude-design-skill

# 1. Tests must all pass
python3 scripts/test_svg_sanitize.py 2>&1        | grep -E '^(Ran|OK|FAIL)'
python3 scripts/test_scan_assets.py 2>&1         | grep -E '^(Ran|OK|FAIL)'
python3 scripts/test_codex_image_import.py 2>&1  | grep -E '^(Ran|OK|FAIL)'
node    scripts/test_animations_easing.js 2>&1   | tail -3
python3 scripts/test_init_brand.py 2>&1          | grep -E '^(Ran|OK|FAIL)'
# Expected: 18/18, 13/13, 19/19, 19/19, 9/9, all OK.

# 2. Settings template must be valid JSON
python3 -c "import json; json.load(open('examples/dot-claude-settings.json'))" && echo "OK"

# 3. Repo state
git log --oneline -5
git status
# Expected: clean working tree. The most recent commits in a
# fresh clone are the Step 4 hardening commits (2026-05-10):
# Step 4.4 hosts whitelist · Step 4.3 GitHub Actions CI ·
# Step 4.2 codename pattern catalog · Step 3.6 showcase gallery
# (16 PNGs) · Step 3.5 SFX library out-of-scope marker. Run
# `git log --oneline | head -20` to scan the full Step 1-4 chain.

# 4. Codex CLI sanity (only if user asks for codex work)
which codex && codex --version
# Expected: /Users/kevin/.nvm/.../codex, version >= 0.130 (validated 2026-05-10).
```

If any of these fail, **stop and report**. Don't try to fix the environment by guessing — the user runs codex CLI from a node-version manager, has a private OAuth token, and changes there could be deliberate.

---

## 2 · Who the user is (so you respond correctly)

- **Role**: internal design platform R&D maintainer. Senior engineer.
- **Domain**: game / web3 studio context. Sensitive to: codename leakage, NDA-bound brand work, sandboxed tooling, supply-chain integrity.
- **Communication style**:
  - Direct and short. "commit it", "2번 진행해", "검증해" — terse instructions.
  - **Refuses meta-narration** ("I'll now proceed to..."). Output the result, not the announcement.
  - Will correct factual mistakes plainly. When corrected, **don't apologize at length** — accept, fix, move on.
  - Korean response with English technical terms is the default. Mixing is fine; pure English is fine when context is purely technical.
- **Decision style**:
  - Asks for verification (`검증해`, `테스트 돌려`) before trusting claims.
  - Picks options A/B/C from `AskUserQuestion` decisively. Don't re-ask the same axis.
  - Approves commits explicitly (`commit it`); does not auto-commit.
- **What they hate** (observed from prior sessions):
  - Speculation presented as fact. Always WebSearch for product / version / release-date claims (Core Principle #0 in `SKILL.md`).
  - Auto-added `Co-Authored-By` lines on commits. **Never include co-author trailers unless explicitly requested.**
  - Long sycophantic intros. Skip "Great question!" and just answer.
  - Re-confirming a decision the user already made.

---

## 3 · The three load-bearing security rules (DO NOT erode these)

These are not suggestions. They are how the skill stays safe in a game/web3 studio environment. They are documented in `SKILL.md` and re-implemented in `scripts/`.

### 3.1 Fact verification before assumptions

- Any factual claim about a product, version, release date, or spec → **`WebSearch` first**. Never assert from memory.
- Today's date is in the system context. Use it. Don't default to your training cutoff.
- If the user mentions an unfamiliar product (e.g., "image 2.0", "GPT-5.5"), `WebSearch` before responding. **This rule already saved one round of broken work in the predecessor session** — gpt-image-2 vs gpt-image-1, default model assumptions, and PNG storage paths were all wrong on first guess and corrected by verification.

### 3.2 Confidentiality gate (before any external call)

- The user is an internal-design maintainer. **Internal codenames, NDA partners, unreleased products** must not leak to:
  - WebSearch (search-engine query logs)
  - Codex CLI prompts (OpenAI logs)
  - `curl` to non-allowlisted hosts
  - any image-generation prompt
- Pattern table: `references/security-config.md §1.5`. The script `scripts/codex-image-import.py` re-runs the regex check at file-move time (exit 4 on any match).
- When in doubt: **ask the user**. Don't search.

### 3.3 Strip-then-scan import gate (every external asset)

- **External SVG**: `scripts/svg-sanitize.py` (whitelist + CSP + visibility comment). Never inline a raw external SVG.
- **External PNG / JPG**: `scripts/scan_assets.py` (chunk/segment scan, hard-fail on WARN/CRITICAL).
- **Codex / gpt-image-2 PNG**: `scripts/codex-image-import.py` strips non-whitelist chunks (notably `caBX` C2PA, ~25 KB) before re-scanning. Trailing bytes after IEND are also dropped and recorded in PROVENANCE.
- Sanitizer rejection is **never silent**. Every rejection lands in `PROVENANCE.md` with the source hash so the audit trail captures attempts, not just outcomes.

---

## 4 · Validated environment facts (don't re-verify unless they look stale)

These were verified live on 2026-05-09. They might shift; if your session is much later than that, run a quick `WebSearch` to confirm.

| Fact | Status |
|---|---|
| Codex CLI version on user's machine | `0.130.0` |
| Codex CLI default model | `gpt-5.5` (no `-m` flag needed) |
| Codex CLI image-gen feature flag | `image_generation: stable, true` |
| Codex CLI image model used | `gpt-image-2` (released 2026-04-21) |
| Codex CLI auth | OAuth via `codex login`, token in `~/.codex/auth.json`, **NOT** `OPENAI_API_KEY` env var |
| Generated PNG storage path | `~/.codex/generated_images/<session-id>/ig_<hash>.png` (one level deeper than the older flat layout) |
| Every gpt-image-2 PNG embeds | `caBX` C2PA / JUMBF chunk (~25 KB) between IHDR and IDAT |
| Predecessor fork status | Frozen at commit `528539f` on `master`, public at `0xmhha/huashu-design` |
| Sibling repo path (predecessor) | `/Users/kevin/work/github/0xmhha/huashu-design` |

### Tool versions / shell

- macOS Darwin 25.3.0, zsh.
- Python 3.11+ (via the system `python3`).
- Node 22.16.0 via `nvm`.
- Git user: `0xmhha`.

---

## 5 · Anti-patterns observed in the predecessor session (don't repeat)

Each of these wasted at least one round-trip in the prior work. Catching them early in this session means staying on the user's intent and budget.

### 5.1 Speculating about external services instead of WebSearching

**What happened**: Without verification, the agent assumed "image 2.0" must be `gpt-image-1` based on training memory. The user corrected: "Codex가 자동으로 image 2.0으로 생성해주지 않아? 서치하여 어떤 서비스이고… 파악하고 다시 결정사항을 물어보도록해." Verification revealed `gpt-image-2` (2026-04-21 release) and that Codex CLI auto-invokes it.

**Lesson**: When the user uses a brand or version name you don't recognize, **stop and `WebSearch` before answering**. Don't ask the user to clarify a name you could look up.

### 5.2 Hardcoding paths without live validation

**What happened**: The first version of `scripts/codex-image-import.py` looked at `~/.codex/generated_images/*.png` (one level deep). Reality: Codex CLI v0.130 uses `~/.codex/generated_images/<session-id>/ig_<hash>.png`. The bug only surfaced in live end-to-end validation, not in unit tests.

**Lesson**: For external tool integrations, **run an end-to-end smoke test** (real codex call, real PNG, real import) before declaring "done". Unit tests with synthetic fixtures don't catch path layout assumptions.

### 5.3 Hard-fail policies that 100% block real input

**What happened**: The first cut of `codex-image-import.py` used `scan_assets.py` as a hard-fail gate. Result: every gpt-image-2 PNG hit `caBX` (C2PA chunk, non-whitelist) and was blocked — 0% useful import rate.

**Lesson**: When you propose a hard-fail policy, **walk through what real production input looks like** before shipping. The fix here was strip-then-scan: drop non-whitelist chunks first, then run the hard-fail gate on the cleaned bytes. The audit trail still records the strip.

### 5.4 Adding Co-Authored-By trailers to commits without permission

**What happened**: The agent added `Co-Authored-By: Claude Opus ... <noreply@anthropic.com>` to a commit message. The user rejected it: "co-author 는 제거해."

**Lesson**: **Never add `Co-Authored-By` to a commit unless the user explicitly asks for it.** Same goes for "Generated with Claude Code" footers. Keep commits in the user's voice, not the agent's.

### 5.5 Long meta-explanations before doing the work

**What happened**: Multi-paragraph "I will now do A, then B, then C" preambles. The user prefers terse output and ignores the preamble.

**Lesson**: State what you're about to do in **one short sentence** if at all, then do it. Save the explanation for after, only when the result is non-obvious.

### 5.6 Inheriting upstream phrasing while believing you're writing fresh

**What happened (in the predecessor fork, not this repo)**: Some doc sections kept upstream's section titles and structure even after rewording. That's still substantial-similarity territory.

**Lesson for THIS repo**: When authoring Step 2 / Step 3 body sections, **pick your own structure first**. If the upstream uses "5-dimension critique" and you also end up at five dimensions with similar names, that's a flag. Use a different number, different dimensions, different framing. Cite reference works (Pentagram, Field.io, etc.) externally — don't paraphrase the upstream's distillation of them.

---

## 6 · Step 2 — SKILL.md body author pass (next plausible session goal)

These are the body sections SKILL.md currently marks TBD. **Each one must be authored from scratch.** No upstream paraphrasing.

For each section: the **goal**, the **problem if absent**, the **author-clean approach**, and a **done-when** check.

### 6.1 Junior Designer workflow

- **Goal**: Define how the agent iterates on design work — assumptions explicit, reasoning visible, placeholders before details, review before delivery.
- **Problem if absent**: The agent jumps to high-fidelity output on vague briefs and produces generic AI-slop.
- **Approach**: Author the four-stage loop in your own words. The structure (assumptions → reasoning → placeholders → review) is a generic engineering pattern, not the upstream's IP, so you can use it — but the prose, the examples, and the failure-mode list must be original.
- **Done-when**: SKILL.md has a "Junior Designer workflow" section ≥150 lines, with a worked example (one task walked through all four stages), and the user has read it once. No reference to "huashu-design" or its phrasing.
- **Status**: ✓ shipped 2026-05-10 @ `8192b8b` — 241-line section in `SKILL.md`, NFT marketplace catalog card worked example.

### 6.2 Anti-AI-slop checklist

- **Goal**: A concrete list of "don't do this" patterns that distinguish AI-generated UI from polished design.
- **Problem if absent**: The agent produces generic gradient-on-card layouts that look like every other ChatGPT artifact.
- **Approach**: Author from observation, not paraphrase. Walk through 5–10 real AI-slop sites and write down what makes them feel AI. Examples worth having: rainbow gradients used as primary identity, perfectly-symmetric layouts, font pairings that are technically correct but have no taste, generic glassmorphism, default Inter + 1.5 line-height + 16px body everywhere.
- **Done-when**: 8–12 patterns, each with a one-line "why it's slop" and a one-line "what to do instead". No upstream phrasing.
- **Status**: ✓ shipped 2026-05-10 @ `f906134` — 12 patterns in `SKILL.md`, last two domain-specific to game / web3.

### 6.3 App prototype rules (iOS / Android)

- **Goal**: When the brief is "make me an iOS prototype" or "Android mockup", the agent wraps every screen in a device frame, uses real images, and verifies interactions before declaring done.
- **Problem if absent**: Agent produces unwrapped browser-window mockups, uses generic placeholder grays for product images, ships without testing the interaction.
- **Approach**:
  - **Android frame is already in `assets/android_frame.jsx`** (Pixel 8 / 8 Pro spec). Re-use as-is.
  - **iOS frame must be authored from scratch.** The upstream skill had `ios_frame.jsx`; the predecessor fork carried it over but is upstream-derivative. **Do not copy.** Author a new `assets/ios_frame.jsx` with iPhone 15 Pro spec (Dynamic Island, rounded corners, status bar). Same public API as the upstream (`<IosFrame>` with width/height props) is fine — that's interface, not implementation — but the implementation code is yours.
  - Document the rule in SKILL.md: every iOS/Android prototype screen wraps in the appropriate frame; default-images-from-real-sources policy; Playwright click-test before delivery.
- **Done-when**: `assets/ios_frame.jsx` exists, references it in SKILL.md, no code copied from the predecessor fork's `assets/ios_frame.jsx` (you can read it for spec, you cannot reuse the code).
- **Status**: ✓ shipped 2026-05-09 @ `b771365` — `assets/ios_frame.jsx` (iPhone 15 Pro / Pro Max model registry, Dynamic Island as a children-receiving slot) + `## App prototype rules` section in SKILL.md. Predecessor `assets/ios_frame.jsx` was opened only for the public API surface; implementation original.

### 6.4 Slide deck conventions

- **Goal**: 1920×1080 deck layouts that look like decks, not web pages. Speaker-notes panel. Print-export rules.
- **Problem if absent**: Agent makes "deck"s that are actually scrollable Tailwind landing pages.
- **Approach**: Define the layout primitives in your own taxonomy. The upstream's `<deck-stage>` web component pattern is functional and you can reimplement (interface), but the JS code must be yours. Don't carry over `assets/deck_stage.js` from the predecessor.
- **Done-when**: SKILL.md slide section, plus `assets/deck_stage.js` newly authored if needed.
- **Status**: ✓ shipped 2026-05-10 @ `8913306` — `assets/deck_stage.js` (`<deck-stage>` web component, colocated `<aside slot="notes">` speaker-notes pattern, blackout key, `@page` print sheet) + `## Slide deck conventions` in SKILL.md. Two distribution bugs (light-DOM display cascade override; nested-aside slot routing) caught by visual smoke and fixed in the same commit.

### 6.5 Tweaks live-tuning system

- **Goal**: Letting the user toggle design variations live ("show me variant B") without re-prompting.
- **Problem if absent**: Every variation = a new full re-render.
- **Approach**: Design your own toggle pattern. State the public API in your own naming.
- **Done-when**: SKILL.md section + a worked HTML example.
- **Status**: ✓ shipped 2026-05-10 @ `49be74d` — `assets/tweaks.js` (`<tweak-panel>` web component, plain `<tweak>` children, data-attribute CSS pattern, localStorage persistence, `tweakchange` event) + `examples/tweaks-demo.html` (runnable 3-knob worked example) + `## Tweaks live-tuning system` in SKILL.md.

### 6.6 Critique guide (post-delivery scoring)

- **Goal**: After a deliverable is out, the agent scores it across multiple dimensions and offers fixes.
- **Problem if absent**: Agent declares "done" on output that has obvious issues a designer would catch in 30 seconds.
- **Approach**: Pick **N dimensions of your choice**, where N ≠ 5 (the upstream uses 5). For example: 4 dimensions (visual hierarchy, typography, motion, narrative coherence) or 6 (add color and spacing). Define each dimension in your own words. The act of scoring 0–10 is generic; the dimension list is where IP risk lives.
- **Done-when**: SKILL.md critique section + a sample critique on a real prior deliverable from the user.
- **Status**: ✓ shipped 2026-05-10 @ `00f6032` — 6 dimensions (N = 6, deliberately ≠ 5) in `SKILL.md`, threshold rule, worked critique applied to `examples/tweaks-demo.html` (the actual Step 2.5 deliverable). Step 2 closes with this section.

---

## 7 · Step 3 — Design knowledge catalogs (subsequent sessions)

These are the **highest-IP-risk** sections of the upstream. Author with maximum care.

### 7.1 `references/design-styles.md` — design philosophy catalog

- **Goal**: When the user's brief is vague ("make it look nice"), the agent can recommend N differentiated design directions.
- **Problem if absent**: Agent produces one default style for every brief.
- **Approach**:
  - **Pick your own taxonomy.** Don't use the upstream's "5 schools × 20 philosophies" or "6 schools × 24 philosophies". Try 4 schools × 4 philosophies, or 5 schools × 6, or skip the school-grouping entirely and present 18 flat philosophies. The math itself signals derivation.
  - For each philosophy: a **prompt DNA line** (3–5 keywords that nail the vibe), **identifying features** (3 bullets), **reference works** cited externally (Pentagram identity, Apple Human Interface Guidelines, Field.io case studies — link to the original, don't paraphrase), and a **when-to-use** line.
  - Game / web3 specific philosophies (HUD, NFT marketplace, wallet, onboarding) are part of this catalog from day one — that's the maintainer's own work in the predecessor fork's Phase 4. The maintainer's prior text on those four philosophies (`references/design-styles.md §21–24` in the predecessor) is fork-author IP and may be carried over verbatim. The other 16–20 philosophies must be authored fresh.
- **Done-when**: `references/design-styles.md` ≥400 lines, structurally distinct from the upstream, with the four maintainer-authored game/web3 entries carried verbatim.
- **Status**: ✓ shipped 2026-05-10 @ `e1d4fa7` — flat 18-direction catalog (no school grouping, no `N × M` math), 14 author-original + 4 game/web3 verbatim carry-over. 578 lines. Predecessor §1–20 prose was not opened; only §21–24 (the verbatim block) was read.

### 7.2 `references/scene-templates.md` — scene catalog

- **Goal**: For common output types (cover, slide, infographic, hero animation, game HUD, NFT marketplace card, wallet/DEX, onboarding loop), the agent has a concrete starting layout.
- **Problem if absent**: Agent rebuilds layout primitives from zero on every brief.
- **Approach**:
  - The four maintainer-authored scenes (game HUD overlay, NFT marketplace card, wallet/DEX, onboarding loop) carry over verbatim from the predecessor's `references/scene-templates.md §9–12`.
  - Other scenes — author fresh. Each scene: dimensions, key elements, recommended philosophies (cross-reference §7.1), prompt template.
- **Done-when**: `references/scene-templates.md` covers 8–12 scenes total, with the four maintainer-authored game/web3 scenes carried verbatim.
- **Status**: ✓ shipped 2026-05-10 @ `8f29827` — 9 scenes total (5 author-original + 4 game/web3 verbatim carry-over, predecessor §9–12 → this catalog §06–09). Cross-reference numbers in the carry-over `Recommended philosophies` lines were re-mapped to this catalog's design-styles numbering; all other prose unchanged. 351 lines.

### 7.3 `references/animation-engine.md` + `assets/animations.jsx`

- **Goal**: Lightweight Stage / Sprite timeline engine for animation work.
- **Problem if absent**: Every animation is hand-rolled with raw `requestAnimationFrame`.
- **Approach**:
  - Public API can match the upstream's (`<Stage duration>`, `<Sprite start end>`, `useTime`, `useSprite`, `interpolate`, `Easing`) — that's interface, not protected IP. **Implementation must be yours.** Don't copy the upstream's `assets/animations.jsx`.
  - Document the engine in `references/animation-engine.md` with worked examples.
- **Done-when**: `assets/animations.jsx` newly authored, regression test exists for the easing functions, SKILL.md animation section references the doc.
- **Status**: ✓ shipped 2026-05-10 @ `ee55f2d` — `assets/animations.jsx` (`<Stage>` controlled / uncontrolled modes, `<Sprite>`, `useTime` / `useSprite`, `interpolate`) + `assets/easing.js` (14-curve frozen pack, dual export) + `scripts/test_animations_easing.js` (Node, 19/19 OK) + `references/animation-engine.md` (4 worked examples). Predecessor `assets/animations.jsx` was not opened; the public API spec from this section was the only input.

### 7.4 `references/animation-best-practices.md` + `references/animation-pitfalls.md`

- **Goal**: Conventions for animation timing, narrative pacing, and what to avoid.
- **Approach**: Generic best practices (Expo easing, anti-bounce-on-everything, etc.) can be cited from CSS/Material/Apple guidelines. **Specific upstream examples** (e.g., the upstream's "Apple Gallery showcase" case study) **must be replaced** with your own examples or omitted.
- **Done-when**: Both files exist, each ≥120 lines, no upstream-specific case studies retained.
- **Status**: ✓ shipped 2026-05-10 @ `a1a2ceb` — `references/animation-best-practices.md` (255 lines: 5-tier timing scale, easing selection, stagger discipline, direction conventions, reduced-motion first-class, performance budget, loop discipline, cross-fade vs morph, use-case routing) + `references/animation-pitfalls.md` (282 lines: 14 anti-patterns, `why-bad → symptom → fix`). External references only (Material Motion, Apple HIG, CSS Easing Level 1, WCAG 2.2, FLIP, Chrome animations); the upstream-specific *Apple Gallery showcase* anchor named in this section is absent (verified by grep).

### 7.5 `references/sfx-library.md` + `assets/sfx/`

> **Status: out of scope per user instruction 2026-05-10.** This
> project is visual-only — no sound deliverables. Do not author
> the SFX catalog, do not source CC0 mp3s, do not build an audio
> sanitizer. If a future deliverable needs sound, the caller is
> responsible for sourcing per-deliverable; this skill will not
> ship vendored audio.

- ~~**Goal**: Sound effect catalog for animation deliverables.~~ (skipped)
- ~~**Approach**: Source from CC0 / freesound with PROVENANCE.md per file.~~ (skipped)
- ~~**Done-when**: 20+ SFX, every file has a PROVENANCE entry.~~ (skipped)

The carry-over notes referencing sound that already shipped (e.g.
`references/design-styles.md §18 Onboarding-Game-Loop` mentions
"haptic + animation + sound" as part of the verbatim-carried
predecessor prose) stay as-is — that's an aesthetic-spec mention,
not a sourcing commitment.

### 7.6 `assets/showcases/` — prebuilt visual demos

> **Status: shipped 2026-05-10 at `assets/showcase-brand/generated/`**
> (the `<brand>-brand/generated/` path is a `scripts/codex-image-import.py`
> convention; the spec mention "`assets/showcases/`" is conceptual).
> 16 PNGs, each with a `PROVENANCE.md` entry. See PROJECT-PLAN §7 entry
> for the sampling matrix.

- **Goal**: When the user asks "what could this look like?", the agent shows ~24 prebuilt visual demos (8 scenes × 3 styles, or whatever your taxonomy lands on).
- **Approach**: Generate **fresh via Codex CLI** using `scripts/codex-image-import.py`. Each PNG gets PROVENANCE.md with prompt + Codex session id + stripped-chunks list. Do not copy from the predecessor's `assets/showcases/`.
- **Done-when**: 16+ showcases on disk, each with PROVENANCE.

---

## 8 · Step 4 — Internal brand integration

> **Status:** Three of the six items below are **shipped** as autonomous
> work (the parts that do not require team-specific knowledge: the
> generic codename catalog, GitHub Actions CI, and the public-asset-host
> allowlist). The remaining three — real `team-brand-spec.json` values,
> internal-host additions, and LICENSE / mirror policy — are **per-fork
> actions** owned by the team that adopts the skill.

When the team brand is finalized:

- ⏳ **Per-fork action**: Replace placeholder values in `team-brand-spec.json` (logo, colors, typography stack). The template (`assets/team-brand-spec.example.json`) and the field reference (`references/brand-spec-fields.md`, 195 lines) are in this repo and ready to copy.
- ✓ shipped 2026-05-10 @ `eb33448` (default catalog) / ⏳ **per-fork action** (team-specific additions): `scripts/codex-image-import.py:DEFAULT_CODENAME_PATTERNS` ships 4 conservative-pairing patterns (project / internal-NDA-confidential / stealth-skunkworks-moonshot × asset-noun / `v\d+`× phase-keyword); `references/security-config.md §1.5` mirrors them with the *Conservative-pairing rule* paragraph that names the trade-off. Per-fork additions go through the same edit point.
- ✓ shipped — default `enabled: false` in `assets/team-brand-spec.example.json`; `references/brand-spec-fields.md §watermark` documents the keep-it-off-until-explicitly-approved policy.
- ✓ shipped 2026-05-10 @ `2ea3bb8` (public asset hosts) / ⏳ **per-fork action** (internal hosts): `examples/dot-claude-settings.json:permissions.ask` and `references/security-config.md §1.1` ship 5 generic-public host entries (Lucide / Phosphor CDN mirrors + MDN). Internal hosts go in `references/security-config.md §1.2 Team-extensible additions`.
- ⏳ **Per-fork action**: **Mirror to the team's private git host.** While the repo is on public GitHub (`0xmhha/claude-design-skill`), keep all team-specific text out of commits. Once internal-only, this README and the LICENSE may need replacement per team policy.
- ✓ shipped 2026-05-10 @ `d5dba7b`: `.github/workflows/sanitizers.yml` runs the full guard chain (SVG sanitizer 18 + scan_assets 13 + codex-image-import 19 + animations easing 19 + JSON template lint + advisory asset scan) on every push to `master` / `main` and every pull request. Translating to an internal CI host (GitLab / Bitbucket / Buildkite) is documented in `references/ci-template.md` *Internal GH Enterprise / Bitbucket / Buildkite* section.

---

## 9 · How to take instructions from this user (decision tree)

When the user gives you a request, work through this tree before doing anything.

```
User request received
│
├─ Does the request involve a security / legal / data-loss / system-stability concern?
│    YES → State the concern in the FIRST sentence. Use "필요합니다" / "누락되었습니다"
│          for security/legal/system. Use "권장합니다" otherwise.
│          Concerns ALWAYS go before any positive framing.
│    NO → continue
│
├─ Is the request a fact claim about an external product / version / release?
│    YES → WebSearch FIRST. Do not answer from memory. (Core Principle #0)
│    NO → continue
│
├─ Does the request require code changes?
│    YES → Check the license-clean rule:
│          - Carrying over maintainer-authored files? OK.
│          - Paraphrasing upstream prose? STOP. Author from scratch.
│          - Using a different N (5→4 or 6) for a list-of-N pattern? OK if natural.
│          - Same naming + same examples + same structure as upstream? Refactor.
│    NO → continue
│
├─ Is the request ambiguous or multi-step?
│    YES, ambiguous → Ask ONE clarifying question (AskUserQuestion, single question,
│                     2-3 options, no "Other" - it's added automatically).
│    YES, multi-step → State the goal/output/constraint in one line, then proceed.
│    NO → execute directly.
│
├─ About to call a tool (Bash, Edit, Write, etc.)?
│    Independent calls → batch them in ONE response (parallel).
│    Dependent → sequential, each call after the prior result.
│
├─ About to commit?
│    NEVER auto-commit. Wait for explicit "commit it" or "커밋해줘".
│    NEVER include Co-Authored-By unless explicitly requested.
│    Commit message: English, short (subject line ≤72 chars), no emoji unless asked.
│
└─ About to reply?
    Skip the meta-narration. State the result. End with what to do next.
    Confidence labels (High/Mid/Low/None) on factual claims when uncertainty matters.
    Korean response, English technical terms allowed.
```

---

## 10 · Common requests and what each one means

A short translation table for the user's terse style.

| User says | What it means | What you do |
|---|---|---|
| `commit it` | Commit current staged changes with a short English message. NO co-author. | `git status` → review → `git commit` with HEREDOC. |
| `검증해` / `verify it` | Run end-to-end with real input, not just unit tests. | Run the actual codex / playwright / shell command and report. |
| `다음 단계 추천해` | Give 2–4 concrete next-step options with effort estimates. | Use `AskUserQuestion` if the choice has tradeoffs; else state and let user pick. |
| `이거 왜 이래` | Investigate before fixing. State the root cause first. | Reproduce → diagnose → propose fix → wait for approval. |
| `짧게 / 요약해` | Cut everything except the result and the action. | Strip preambles. Lead with the outcome. |
| `2번 진행해` | Execute option 2 from the most recent AskUserQuestion. | Re-state the option in one line, then execute. |
| `검토해` (regarding code) | Critical review. Find issues before listing strengths. | Issues first (with severity), then strengths if asked. |
| `정리해` | Tidy the artifact (commit, doc, file structure). | Make the change small and reversible. |
| `[silent / no specific request]` | Continue the prior task. | If no prior task, ask one clarifying question. |

---

## 11 · The PROJECT-PLAN.md ↔ HANDOFF.md split

- **PROJECT-PLAN.md** is the inventory. What was carried over, in what state, what files exist, version log. Read it for "what is here right now".
- **HANDOFF.md** (this file) is the briefing. Why we're doing this, how to talk to the user, anti-patterns, decision tree. Read it for "how to act in the next session".
- They are **not** duplicates. Don't merge them. Update both when something changes.

When you finish a meaningful chunk of work in your session, update HANDOFF.md's "Last updated" date and any anti-pattern entries that are now obsolete or new. Update PROJECT-PLAN.md's decisions log with the date and what was decided.

---

## 12 · Files to read before doing real work, in order

1. **`HANDOFF.md`** (this file) — context and decision tree.
2. **`PROJECT-PLAN.md`** — what's here, what was done, what's next; the per-step decisions log is canonical.
3. **`SKILL.md`** — Core Principles #0 / #1 (fact verification, security-first), Figma MCP routing, Codex CLI bridge, plus the body sections shipped in Step 2 (App prototype rules, Slide deck conventions, Anti-AI-slop checklist, Junior Designer workflow, Tweaks live-tuning system, Critique guide).
4. **`README.md`** — public-facing summary; ships the directory tree and the local guard-chain runner.
5. **`CHANGELOG.md`** — release log; entries from `[Unreleased]` map back to Step 2 / Step 3 / Step 4 commits (2026-05-09 → 2026-05-10).
6. The specific reference doc for the section you're working on (e.g., for an animation pass, read `references/animation-engine.md`, `references/animation-best-practices.md`, `references/animation-pitfalls.md`; for a vague design brief, start at `references/design-styles.md`).

Don't read the predecessor fork at `/Users/kevin/work/github/0xmhha/huashu-design` for prose. You can read it for code spec on files that have a maintainer-authored counterpart (e.g., `assets/android_frame.jsx`) — but `SKILL.md` and `references/design-styles.md` and `references/scene-templates.md` etc. **must not be a paraphrase source**. If you find yourself reading them for "inspiration", stop.

---

## 13 · Glossary (terms you'll see in this repo)

- **Predecessor fork** — `0xmhha/huashu-design`, the security-hardened fork of the upstream `huashu-design` skill. Frozen at commit `528539f` on 2026-05-09. Public on GitHub.
- **Upstream** — `alchaincyf/huashu-design`. The original skill the predecessor forked from. Personal-use license.
- **Carryover** — files brought from the predecessor fork that are 100% maintainer-authored (Phase 1–4.2 work). License-clean to bring here.
- **Step 1 / Step 2 / Step 3 / Step 4** — see `PROJECT-PLAN.md`. Steps 1–4 all shipped on 2026-05-10; Step 3.5 SFX library was retired by user instruction (visual-only project). The remaining work is per-fork (real `team-brand-spec.json` values, internal codenames, internal hosts, LICENSE / mirror policy).
- **Confidentiality gate** — the codename / NDA / unreleased-product check that fires before any external call. Patterns in `references/security-config.md §1.5`.
- **Strip-then-scan** — the gpt-image-2 import gate: drop non-whitelist PNG chunks (caBX C2PA), then run `scan_assets.py` on the cleaned bytes. If it still fails, hard-block.
- **caBX** — the C2PA / JUMBF chunk OpenAI auto-injects in every gpt-image-2 PNG (~25 KB of provenance metadata signed by OpenAI). The fork's strip removes it; the fork's PROVENANCE.md replaces it.
- **PROVENANCE.md** — the per-brand audit trail. Both successful imports and rejected attempts land here. Auto-maintained by `scripts/svg-sanitize.py` and `scripts/codex-image-import.py`.
- **Hard-fail** — sanitizer rejection that stops the workflow. The user sees the rejection, the file does not move into `assets/`. No silent retries.

---

## 14 · End of briefing

You now know:
- What this project is (clean-room rewrite, Apache 2.0, no upstream inheritance; the upstream `alchaincyf/huashu-design` Personal-Use license is separate and unaffected).
- What's done (Steps 1–4 all shipped on 2026-05-10; 18 + 13 + 19 + 19 regression tests pass; 16 prebuilt visual showcases; CI on every push and PR).
- What's retired (Step 3.5 SFX library, by user instruction — visual-only project).
- What's still per-fork (real `team-brand-spec.json` values, internal codenames added to the pattern list, internal hosts added to the allowlist, LICENSE / mirror policy).
- How to act (terse, verify before claiming, no co-author, no meta-preamble, license-clean prose).
- What to avoid (speculation, paraphrasing upstream, hard-fail without strip, sycophancy).

If your next instruction from the user is unclear after reading this, ask **one** clarifying question. If it's clear, do the work and report the result.

Good luck.
