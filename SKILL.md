---
name: claude-design-skill
description: |
  Claude Code-based design skill for hi-fi prototyping and Figma MCP-driven
  precision design work. Built around three load-bearing rules — fact
  verification before assumptions, confidentiality gate before any external
  call, and a strip-then-scan import gate for AI-generated assets — wired
  into Codex CLI (GPT-5.5 reasoning, gpt-image-2 image generation) and the
  Figma MCP toolchain. Triggers — Claude design skill, Figma MCP workflow,
  Figma selection-aware edit, Figma layer rename, Figma component grouping,
  brand spec from Figma, codex image asset, brand-correct illustration via
  gpt-image-2, prototype security baseline, sanitize external SVG, prototype
  vs production boundary, Pixel 8 mockup, Android prototype, app prototype.
  This skill is a clean-room rewrite — no upstream design skill is inherited.
---

# claude-design-skill

> Status: **v0.1.0-alpha · skeleton · 2026-05-09**
> Body sections marked TBD are filled in Step 2 / Step 3 of the project
> plan (see PROJECT-PLAN.md). Security and routing rules are already
> live and load-bearing — they govern every external call this skill
> can make.
>
> **For AI agents in a fresh session**: read `HANDOFF.md` at the repo root
> first. It contains the working-style briefing and anti-pattern list
> that prevents the most common rework loops.

## What this skill is for

Hi-fi prototypes, slide decks, animations, and Figma-MCP-driven precision
design work, executed by an LLM agent through Claude Code. The skill
provides:

- **Security baselines** that govern every external fetch (allowlist,
  WebSearch policy, Codex CLI policy, codename redaction).
- **Sanitizers** for external assets (SVG XXE/script removal, PNG chunk
  scan, AI-generated PNG strip-and-import).
- **Figma MCP workflow** with five sub-guides covering selection-aware
  edits, layer renames, component grouping, brand-spec import, and the
  meta hub.
- **Codex CLI bridge** for GPT-5.5 reasoning + gpt-image-2 image
  generation, with a hard-fail import gate that strips C2PA
  metadata and re-scans the result.

The body — design philosophies, scene templates, slide rules, animation
rules, prototype scaffolding — is **deliberately empty in this skeleton**
and will be authored from scratch in subsequent steps. This avoids
inheriting any prose from an upstream skill and keeps the project
license-clean.

## Core Principle #0 · Fact verification before assumptions

Any factual claim about the existence, release status, version number,
or specifications of a specific product, technology, event, or person —
**the first action MUST be `WebSearch`**. Asserting from training-corpus
memory is forbidden.

### Trigger conditions (any one)

- The user mentions a specific product name you are not familiar with
  or unsure about.
- Anything involving release timelines, version numbers, or specs from
  2025 onward.
- You catch yourself thinking "I think it's…", "should not have launched
  yet", "probably around…", "might not exist".
- The user requests design materials for a specific product or company.

### Hard procedure (execute before clarifying questions)

1. **Confidentiality gate (must answer before any external call)**: is
   the term a publicly released external brand or product (e.g., DJI
   Pocket 4, Apple Vision Pro, Stripe), or could it be an internal
   codename, unreleased team product, or partner under NDA? If the
   second — **do not search and do not send to Codex**. Ask the user
   instead. The same gate applies to `WebSearch`, `Bash(curl …)`,
   `Bash(codex exec …)`, and any image-generation prompt. Pattern
   table lives in `references/security-config.md §1.5`;
   `scripts/codex-image-import.py` re-runs the check at file-move time
   and exits 4 on any match.
2. `WebSearch` for the product name + a recent time keyword
   ("2026 latest", "launch date", "release", "specs") — only for public
   external brands cleared in step 1.
3. Read 1–3 authoritative results to confirm: existence, release
   status, latest version, key specs.
4. Write the facts into the project's `product-facts.md` (per-project
   scratch file, gitignored). Don't rely on memory.
5. Can't find anything or results are ambiguous → ask the user, don't
   assume.

### Forbidden phrasing

- ❌ "I remember X hasn't launched yet"
- ❌ "X is currently version N" (an unsearched claim)
- ❌ "X probably doesn't exist"
- ❌ "As I recall, X's specs are…"
- ✅ "Let me `WebSearch` X's latest status"
- ✅ "Authoritative sources I found say X is…"

This principle outranks "ask clarifying questions" — asking questions
presupposes the facts are right. If facts are wrong, every question is
skewed.

## Core Principle #1 · Security-first asset handling

Every external asset must pass through a sanitizer before it lands in
this repository. The sanitizer is whitelist-based and recorded by SHA-256
in PROVENANCE so future audits can detect tampering.

| Asset type | Gate | Implementation |
|---|---|---|
| External SVG (logos, illustrations) | XXE-guarded XML parse + tag/attr whitelist + CSS sub-sanitize + visibility comment | `scripts/svg-sanitize.py` + `references/svg-sanitize.md` |
| External PNG / JPG | Chunk/segment scan: trailing data, non-whitelist chunks, oversized text metadata | `scripts/scan_assets.py` |
| Codex / gpt-image-2 generated PNG | C2PA `caBX` strip + recursive discovery + scan re-run + hard-fail | `scripts/codex-image-import.py` + `references/codex-design-workflow.md` |
| External fetch (curl, wget, etc.) | Domain allowlist + per-call user approval + WebSearch policy | `references/security-config.md` + `examples/dot-claude-settings.json` |
| Prototype-only patterns (CDN, Babel-standalone, in-DOM API keys) | Production-boundaries checklist | `references/production-boundaries.md` |

If a sanitizer rejects an asset, **do not silently retry** with a
different fetch path. Surface the rejection to the user, log it in
PROVENANCE, and ask for an alternative source.

## Figma MCP workflow

When work originates in Figma — selection-aware edits, layer renames,
component promotions, brand-token imports — start at the workflow hub
and dispatch to the relevant sub-guide:

| Situation | Read |
|---|---|
| Entry point — MCP-aware vs MCP-absent decision rules, audit report template | `references/figma-workflow.md` |
| The user said "this layer" — confirm what was actually selected | `references/figma-selection-aware.md` |
| Many layers named `Frame 47` / `Rectangle 31` — assign meaningful names | `references/figma-layer-naming.md` |
| Repeated patterns appearing 3+ times — propose component promotion | `references/figma-component-grouping.md` |
| Pull design tokens (colors, typography, logos) from Figma into `team-brand-spec.json` | `references/figma-brand-spec-import.md` |

## Codex CLI design workflow

For brand-correct illustration generation via GPT-5.5 reasoning +
gpt-image-2 image gen, with the strip-then-scan import gate:

→ `references/codex-design-workflow.md`

Key facts (validated against codex-cli 0.130.0 on 2026-05-09):

- Codex CLI default model is **gpt-5.5**.
- Image generation runs through Codex's built-in `image_generation`
  tool, no `OPENAI_API_KEY` env var required (codex-cli's own OAuth
  token covers it).
- PNGs land at `~/.codex/generated_images/<session-id>/ig_<hash>.png`.
- Every gpt-image-2 PNG carries a `caBX` C2PA chunk (~25 KB). The
  importer strips it and substitutes the fork's own PROVENANCE entry.

## App prototype rules (iOS / Android)

When the user's brief is "iOS prototype" or "Android mockup", three
rules apply before the work can be called done. Skipping any one of
them is the tell that distinguishes a polished prototype from a
screenshot of a landing page.

### Rule 1 · Wrap every screen in a device frame

- iOS → `assets/ios_frame.jsx` (`<IosFrame />`, iPhone 15 Pro / Pro Max
  via `model="iphone15pro"` | `"iphone15promax"`).
- Android → `assets/android_frame.jsx` (`<AndroidFrame />`, Pixel 8 /
  Pixel 8 Pro via `model="pixel8"` | `"pixel8pro"`).
- Both frames render their own status bar, system chrome, and bottom
  inset. **Do not redraw any of these inside your screen content** —
  the result is double status bars or a duplicated home indicator,
  which immediately betrays the mockup as agent-generated.
- A browser-window mockup (window-control dots, URL bar, tab strip)
  delivered for an iOS / Android brief is a hard reject. Re-render
  inside the device frame.

### Rule 2 · Real images, not placeholder grays

- Product photography, avatars, and brand marks come from real assets:
  Codex / `gpt-image-2` (passed through `scripts/codex-image-import.py`),
  user-supplied files, or CC0 sources with PROVENANCE entries.
- Solid grey blocks, generic stock photography, and
  `<div style="background:#ddd">` standins are silent failure modes —
  the layout passes a quick eyeball check and the design has no taste.
  The first reviewer with design instincts spots it before the user
  does.
- When you genuinely cannot source a real image, ask the user. Do not
  ship a placeholder under a "looks fine" justification.

### Rule 3 · Click-test before declaring done

- Wire up at least one critical interaction (tap a primary button,
  open a sheet, switch tabs) and verify it with Playwright or the
  equivalent in the user's browser-automation toolset.
- A static screen that "looks like" the prototype but has no working
  taps is a static screen, not a prototype. Label it as such if that
  is what the user asked for; otherwise the click-test is part of the
  deliverable.
- Smoke-test at the real device dimensions exposed by the frame
  (`<IosFrame />` at 393×852 or 430×932, not a scaled-up desktop
  preview). Long content, dark mode, and any custom Dynamic Island
  content used in the run all need a quick visual pass.

### Dynamic Island slot (iOS only)

`<IosFrame island={…}>` accepts a ReactNode rendered inside the
Dynamic Island region — pass a now-playing pill, a timer, or a Live
Activity mock to demo state-aware UI. Omit the prop and it falls back
to the static black pill. The slot auto-expands to at least 220 × 48 px
with a 240 ms transition, keeping the ergonomics close to the real
Live Activity expand without prescribing layout inside the slot.

## Slide deck conventions

When the user asks for a "slide deck", "presentation", or "투표 자료",
the deliverable is a deck — not a scrollable web page. The four rules
below separate decks from landing pages.

### Rule 1 · Fixed canvas, not flow layout

- Canvas is **1920 × 1080 by default** (16:9). Portrait, square, or
  any other ratio is fine — declare it once on the deck shell, never
  per slide.
- Wrap every slide deck in `<deck-stage>` from `assets/deck_stage.js`.
  The component pins the canvas size, scales to the viewport with
  letterbox bars, and lets the user keep designing at canvas pixels
  even on a 1280 × 720 laptop screen.
- A slide that needs scrolling to read is a layout failure, not a
  deck. If the content does not fit, split the slide; do not ship a
  scrollable section. (Speaker notes are the exception — they live in
  the notes overlay, not on the slide canvas.)
- Markup shape: each slide is a `<section>` child of `<deck-stage>`.
  No outer `<main>`, no scrollable wrapper.

### Rule 2 · Speaker notes are colocated, not orphaned

- Notes belong **with** the slide they annotate, as
  `<aside slot="notes">…</aside>` nested inside the matching
  `<section>`. The component routes the slot into the in-canvas notes
  overlay (`n` to toggle).
- Notes can carry markup — bold, lists, emphasis, links — and the
  overlay clones the live DOM, so author markup renders. (No
  untrusted HTML flows in; the page is the source.)
- Empty notes render an explicit `— no notes —` placeholder. Don't
  omit the slot just to hide the placeholder; an explicit "no notes
  for this slide" is information.

### Rule 3 · Print = one canvas-sized page per slide

- The deck must export to PDF cleanly via `Cmd / Ctrl + P`.
- `<deck-stage>` injects an `@page` rule that matches the canvas
  size and a `@media print` block that strips the counter, click-zone
  navs, notes overlay, and blackout layer. One slide → one page.
- Verify before delivery: open the deck, print to PDF, confirm one
  slide per page at the right dimensions, no scrollbar bleed, no
  cropped text. A deck that "looks great in the browser but renders
  4 slides per page in PDF" is a deck that has not been tested.

### Rule 4 · Treat the keyboard as a user surface

- Built-in shortcuts (designed; document them in any handout):
  `← / →`, `space`, `pgup / pgdown`, `home / end`, `1–9` (jump to
  slide N), `n` (toggle speaker-notes overlay), `b` (blackout to
  pure black; press again to restore), `esc` (close blackout or
  notes).
- The presenter should never have to touch the mouse during a live
  talk. If a deliverable hides a critical interaction behind a click,
  add the keyboard equivalent or move the interaction into the
  slide's static layout.

### CSS hooks (theming without forking the component)

`<deck-stage>` exposes four CSS variables on the host:
`--deck-bg` (letterbox color), `--deck-slide-bg` (canvas background
when the slide doesn't paint its own), `--deck-stage-shadow`
(canvas drop-shadow), `--deck-font` (counter / notes font). Set
them inline on the element, in the document stylesheet, or per
slide for chapter-color treatments.

### Slide-change broadcast (opt-in only)

`broadcast-origin="self"` posts a slide-change message to the
parent same-origin window. An explicit `https://host.example` value
posts only to that origin. The wildcard `"*"` is intentionally
unsupported — receivers must always be specified. Off by default.

## Anti-AI-slop checklist

The patterns below are the AI-generated UI tells the maintainer keeps
running into. Each one looks fine in isolation; together they read as
"an LLM made this" within five seconds of opening the page. Run a
mental pass over the deliverable before declaring it done — if more
than one pattern is present, treat it as a draft, not a delivery.

Each entry is structured as: **why it's slop** → **what to do instead**.

1. **Rainbow / sunset gradient as the primary identity.** Why it's
   slop: orange → pink → purple is the LLM's reflex whenever the
   brief mentions "modern" — every ChatGPT-flavored landing page
   wears the same coat. → Pick one accent hue plus neutrals. If a
   gradient is unavoidable, hold it to two adjacent hues, narrow the
   angle, and apply it to one element only.

2. **Perfectly symmetric, centered layouts.** Why it's slop:
   centered hero + 3-column features + centered CTA is the framework
   demo, not a design. → Use asymmetry deliberately. Off-center text,
   mixed grid widths, deliberate vertical breaks. Symmetry should be
   a choice, not a default.

3. **Generic glassmorphism.** Why it's slop:
   `backdrop-filter: blur(20px)` over a gradient mesh is the 2025
   Bootstrap stripe — it shows up regardless of the brand. → Reserve
   frosted surfaces for genuinely interactive layers (modals,
   command palettes). Default cards should use real shadow on
   opaque material.

4. **Default type stack: Inter, 16 px body, 1.5 line-height.** Why
   it's slop: those are the Tailwind starter defaults. Technically
   correct, signature-free. → Tighten display line-height (1.05–1.15)
   for headings, hand-set tracking on display sizes, and consider
   body fonts beyond Inter (Geist, Söhne, Atlas Grotesk, Untitled
   Sans). Different scales for marketing vs UI vs data.

5. **Emoji-as-icon (🚀 fast, 💡 ideas, ⚡ performance).** Why it's
   slop: it's the Pictionary clue of AI design — the agent picked the
   most obvious metaphor and stopped. → Use a real icon set
   (Lucide, Phosphor, custom SVGs) with a single stroke discipline.
   Reserve emoji for places where the platform expects one.

6. **One border-radius applied to every box.** Why it's slop:
   12 px or 16 px corners on cards, buttons, inputs, and badges
   collapse the visual hierarchy — nothing feels different from
   anything else. → Pick at least three radii with intent. Sharper
   for buttons, softer for cards, full pills for status,
   sharp-zero for headers. Radius communicates role.

7. **Uniform vertical padding everywhere.** Why it's slop: every
   section gets `py-24` because the LLM doesn't see page rhythm —
   hero, content, footer all read at the same density. → Vary
   vertical rhythm: heroes breathe, dense lists compress, mid-content
   alternates. Padding cadence is half the deck.

8. **Placeholder marketing copy
   ("Disrupt. Innovate. Iterate.").** Why it's slop: copy that
   could plug into any product is copy that says nothing. → Either
   real copy or no copy. An empty section is more honest than
   "Empower your team to do more" — and ships less reputational
   damage.

9. **Stock content — Unsplash photography and Spline-style 3D
   blobs.** Why it's slop: the diverse-team-laughing-around-laptop
   stock photo and the pastel isometric 3D shape are both the
   "fetched a generic asset" tell, no matter the medium. → Real
   product imagery, real customer assets with consent, or a
   deliberately authored illustration in your own style. No stock
   people, no stock 3D.

10. **Animated gradient-mesh backgrounds behind hero copy.** Why
    it's slop: a WebGL orb that pulses behind the headline is every
    AI agent's idea of "make it feel alive". It distracts from the
    actual product and signals the same template across deliverables.
    → Animate to reinforce hierarchy: button micro-interactions,
    focus reveals on scroll, intentional parallax. Background
    animation is rarely the answer to "this feels static".

11. **Default cyberpunk-neon palette for anything web3.** Why it's
    slop: every NFT marketplace and wallet mockup defaults to cyan
    + magenta + pure-black + glow + grid. The aesthetic was
    distinctive five years ago; today it reads as "I asked the LLM
    for a web3 UI". → Treat the project's actual brand or product
    as the source. If the chain has no identity yet, prefer
    restrained material (paper-white, off-black, single accent)
    over reflexive cyberpunk.

12. **Cargo-cult game-HUD detail.** Why it's slop: fake
    nine-segment displays, gratuitous "SYSTEM: ONLINE" overlays,
    decorative data readouts that show nothing real — game-UI
    cosplay without function. The LLM clutters game and web3
    surfaces with this on instinct. → Every HUD element earns its
    place by carrying live data the player or user actually needs.
    Decorative chrome belongs in the wallpaper, not in the
    interface.

If the deliverable contains one of these, fix it before delivery.
If it contains three or more, the design hasn't started yet — go
back to references, pick a direction, and try again.

## Junior Designer workflow

Most failure modes in agent-driven design come from one move: the
agent skips the slow part of the work and goes straight to high-
fidelity output. The result looks finished and tastes generic — the
LLM baseline. This section defines a four-stage loop that forces
slowness at the points where it matters and speed at the points
where it doesn't.

### Why this section exists

When a brief is vague ("design our wallet onboarding", "make a
deck cover for the seed-round talk"), the path of least resistance
is to start drawing. Drawing without an explicit thinking pass
means taste fills the gaps, and the agent's taste is, by default,
the average of every Behance hero shot since 2022. Run the loop
even when the brief feels small. The loop is short.

### The four stages

Every design pass walks the same loop:

1. **Assumptions, explicit** — write down what the brief left unsaid,
   before any pixel is drawn.
2. **Reasoning, visible** — explain the design direction in one short
   paragraph, before opening the artifact.
3. **Placeholders, before details** — block out structure with
   deliberately rough content first; refine after the bones are
   right.
4. **Review, before delivery** — score the artifact against the
   brief, the assumptions, and the anti-slop checklist before
   declaring done.

Skipping a stage is allowed. Skipping a stage *implicitly* is the
failure. If you skip Stage 1 because the brief is genuinely clear,
say so out loud. If you skip Stage 3 because the artifact is one
trivial change, say so. Implicit skipping is how the loop becomes
ornamental.

### Stage 1 · Assumptions, explicit

Most briefs are vague. The agent's job in Stage 1 is to surface the
gaps, not paper over them.

- Open the response (or a fresh note) with a numbered list of
  claims about the brief.
- Each claim ends in one of three markers: `(verified)` if the
  brief states it, `(inferred)` if a sibling brief or the project
  brand spec states it, `(open)` if neither — a real gap that
  needs a default or a question.
- Group every `(open)` claim and decide once: ask the user now, or
  proceed with a default and flag it on delivery. Asking too often
  is annoying; defaulting silently is the failure mode that
  produces generic output.

The deliverable from Stage 1 is the numbered list itself, plus one
consolidated message to the user if any open question is too costly
to default. One message — not seven, scattered across stages.

**Failure mode**: assumptions made implicitly ("game and web3 means
dark mode, of course") and never written down. The next round of
feedback then asks "why dark?" and the agent has no answer except
"it felt right".

### Stage 2 · Reasoning, visible

Before generating the artifact, write the design reasoning as one
short paragraph. Not a thesis. Three to five sentences that connect
the brief, the assumptions, and the chosen direction.

A worked shape:

> The brief is a wallet onboarding flow for a new chain. The
> audience is power users moving over from existing wallets — not
> first-time crypto users — so the explanation step compresses.
> Reasoning: lead with the chain identity, fold the seed-phrase
> warning into one screen with stronger affordance, drop the
> educational interstitial. Direction: minimal-editorial,
> restrained typography, single accent (chain hex).

The reasoning paragraph is a **contract**. When the artifact is
reviewed, the reasoning is what the reviewer pushes against — not
the final pixels alone. A reviewer who only critiques pixels gets
"I'll change the corner radius"; a reviewer who critiques the
reasoning gets "the audience assumption is wrong, here's why".

**Failure mode**: starting the artifact with no written reasoning,
then post-rationalizing during review. The post-rationalization is
always too generous to the work that already exists.

### Stage 3 · Placeholders, before details

Block out structure first. Refine later. The placeholder is
*supposed* to look unfinished — that's the point. Polishing one
region while three others are wrong is the most expensive thing
the agent can do.

- For typography: `[heading]`, `[subhead]`, `[body 80–120 words]`.
  Real type on placeholder copy is fine — placeholder copy in real
  type is the goal.
- For images: a flat colored block at the right aspect ratio,
  labeled `[3:2 product still]` or `[NFT 4:5]`, not the first
  Unsplash result.
- For data: `[42]`, `[2.4 ETH]`, `[12 holders]`. The shape of the
  number, not the number.

Stage 3 exposes the layout's bones. If the bones are wrong — if
the price field is fighting the title for emphasis, if the artwork
crop is half a card too tight — that becomes obvious in placeholder
form within a minute, instead of after an hour of polish.

**Failure mode**: skipping placeholders and starting hi-fi from
the first stroke. The agent then becomes attached to the first
hi-fi version, can't critique it, and ships it.

### Stage 4 · Review, before delivery

Before declaring done, score the artifact against three concrete
checklists:

- **The brief**: does each requested element exist? (binary check)
- **The assumptions**: did any Stage-1 assumption get violated
  silently? (most common failure)
- **The anti-slop checklist** (`## Anti-AI-slop checklist` in this
  skill): how many patterns are present?

If three or more anti-slop patterns are present, treat the artifact
as a draft. Go back to Stage 2 (reasoning) and try a different
direction — the direction itself is what's drifting toward LLM
baseline.

If zero or one anti-slop patterns are present and assumptions are
intact, declare done. **Surface the artifact with the Stage-2
reasoning paragraph attached.** The reviewer should see what was
decided, not just what was made. Without the reasoning, the only
thing reviewable is the pixels, and pixel-level review tends to be
too kind to the work.

**Failure mode**: review against "does it look fine?" and ship.
"Looks fine" is the LLM design baseline; shipping that is shipping
the LLM baseline.

### Worked example · NFT marketplace catalog card

A real walk-through. The brief from the user: "Design a card for
an NFT marketplace catalog. Mid-fidelity — clickable but not
finished."

#### Stage 1 · assumptions

1. Card is clicked through to a detail page. `(verified)` — "clickable" in brief.
2. Catalog shows 3–5 cards per row on desktop, 2 on tablet, 1 on phone. `(open)` — defaulted; flagged.
3. Each NFT carries: artwork, title, collection name, current price, last sale, holder count. `(inferred)` — common marketplace schema; if the project's schema differs, regenerate.
4. Price uses the chain's native token with fiat conversion in muted text. `(inferred)` — convention.
5. Card hover reveals nothing essential — affordance only. `(inferred)` — revealed-on-hover content is mobile-hostile.
6. Card width sits at roughly 280–320 px on desktop default. `(inferred)`
7. Card uses the project's brand spec; no project-brand was supplied yet. `(open)` — neutral material until brand spec arrives, flagged.

The two `(open)` claims fold into one message to the user:
*"Two defaults applied — confirm or change: card grid columns
(default 4 on desktop), brand spec source (using neutral material
until you supply one). Both flagged on the artifact."*

#### Stage 2 · reasoning

> Marketplace catalog cards live in a dense scan-grid; the card has
> to communicate identity, price, and "is this still hot" within a
> glance. Direction: artwork dominates (top ~65 % of the card), a
> compact text rail beneath promotes price as the primary data
> point, with title and collection demoted to supporting context.
> Restrained chrome — neutral surface, hairline edge — so the
> artwork carries the visual weight, not the card itself.

Three things review will push against: artwork-dominant ratio,
price-as-primary-data, and muted chrome.

#### Stage 3 · placeholders

The first artifact is intentionally rough:

- Artwork: solid `#E5E5E5` block, 4:5 aspect, labeled `[NFT 4:5]`.
- Title: `[Collection Name #0042]` in display weight, single line, ellipsis on overflow.
- Collection: `[creator handle]` in muted body weight.
- Price row: `[2.4 ETH]` primary, `[~$8,300]` secondary in `0.7` opacity.
- Stat row: `[12 holders]` and `[last 1.9 ETH]`, separated by a thin divider.
- Hairline 1 px border on the card; 12 px radius on the card chrome, 8 px on the artwork crop.

This pass is delivered with the Stage-2 reasoning paragraph
attached. No real artwork, no chosen typeface, no animation.
Speed-of-iteration over polish.

#### Stage 4 · review

Run the checks before declaring done.

- **Brief check**: clickable card, mid-fidelity. ✓ (placeholder is mid-fi by design.)
- **Assumption check**: card width 296 px (within range); grid count flagged for user; brand neutrality flagged for user; no silent violations.
- **Anti-slop check**: zero rainbow gradients, no glassmorphism, no emoji, hairline border + neutral surface, two radii (card / artwork crop) instead of one. The single in-flight pattern is the default-neutral palette — acceptable because it is explicitly flagged as a Stage-1 open question. Score: 1 of 12 patterns, with that one already on the open-question list.
- **Final**: deliver with the reasoning paragraph plus the open-question list. The user sees what was decided and what is still open.

If the user redirects ("price isn't the primary data — holder
count is, this is a collector audience"), the reasoning paragraph
gets edited first, then Stages 3 + 4 re-run. Stages 1 + 2 don't
restart unless the brief itself changed.

### Failure modes (consolidated)

1. **Skipping Stage 1, claiming the brief was clear.** Cure: every
   brief surfaces at least one assumption. If you find none, you
   didn't read closely enough.
2. **Writing the reasoning paragraph after the artifact.** Cure:
   reasoning before pixels. If reasoning comes second, the
   artifact already chose the direction and reasoning is just
   defending it.
3. **Hi-fi from the first stroke.** Cure: even on a small brief,
   label the first artifact "draft" and refine before delivery.
   Ten minutes of placeholder work prevents thirty minutes of
   subtle backtracking.
4. **Reviewing against "looks fine".** Cure: review against the
   assumptions list and the anti-slop checklist. Both are
   concrete; "looks fine" is not.
5. **Asking the user every open question at every stage.** Cure:
   bundle. Stage 1 produces one consolidated message; Stage 4
   produces one consolidated delivery message. Two checkpoints per
   round, not seven.

### When to short-circuit the loop

Some briefs don't need the full loop:

- A single CSS-value tweak. **Stage 4 alone** (review the change in
  context) is enough.
- A direct copy-edit. **Stage 1 + Stage 4** are enough (was the
  rewrite intent stated? does the new copy match the brief?).
- A repeat task with all stages established last round. **Stage 3 +
  Stage 4** suffice — apply the established direction, review.

For anything above "tweak" — anything that involves a layout
decision, a typography decision, or a new artifact — run all four
stages. The discipline is what stops the work from regressing to
LLM baseline.

## References routing table

| Task | Read |
|---|---|
| **Security baseline** — allowlist, deny rules, settings.json template, audit trail | `references/security-config.md` |
| **External SVG sanitization** — threat model, whitelist, CSP, failure placeholder, visibility comment policy | `references/svg-sanitize.md` + `scripts/svg-sanitize.py` |
| **Prototype ↔ production boundary** — vendoring, pre-compile, proxy backend, pre-prod checklist | `references/production-boundaries.md` |
| **Figma workflow hub** — entry point when work originates in Figma | `references/figma-workflow.md` |
| **Figma selection-aware edits** — confirm what the user meant by "this layer" | `references/figma-selection-aware.md` |
| **Figma layer naming pass** — assign meaningful names | `references/figma-layer-naming.md` |
| **Figma component grouping** — detect repeats, promote to components | `references/figma-component-grouping.md` |
| **Figma brand-spec import** — design tokens / typography / logo into `team-brand-spec.json` | `references/figma-brand-spec-import.md` |
| **Codex CLI design workflow** — GPT-5.5 reasoning + auto gpt-image-2, with import gate | `references/codex-design-workflow.md` + `scripts/codex-image-import.py` |
| **Brand spec field reference** — what every key in `team-brand-spec.example.json` means | `references/brand-spec-fields.md` |
| **CI workflow templates** — GitHub Actions / GitLab CI for sanitizer regression + asset scan | `references/ci-template.md` |
| **App prototype rules** — iOS / Android device-frame wrapping, real-image policy, Playwright click-test | `## App prototype rules` (this skill) + `assets/ios_frame.jsx` + `assets/android_frame.jsx` |
| **Slide deck conventions** — 1920×1080 fixed canvas, colocated speaker notes, print-to-PDF rules, keyboard surface | `## Slide deck conventions` (this skill) + `assets/deck_stage.js` |
| **Anti-AI-slop checklist** — 12 generated-UI tells (gradients, glassmorphism, emoji icons, default type, cyberpunk-by-reflex, fake HUD detail) with fixes | `## Anti-AI-slop checklist` (this skill) |
| **Junior Designer workflow** — 4-stage loop (assumptions → reasoning → placeholders → review), worked NFT marketplace card example, failure modes, short-circuit rules | `## Junior Designer workflow` (this skill) |

## Body sections — TBD (authored in Step 2 / Step 3)

These sections will be authored from scratch in subsequent steps. Do
not pull text from any third-party design skill. Each section will get
its own `references/<topic>.md` file when it grows beyond a few
paragraphs.

- **Design philosophy catalog** — design schools and their identifying
  features. Authored in Step 3, not before. Until then, when the user
  needs design direction, ask the user for references rather than
  proposing from memory.
- **Scene templates** — cover, infographic, slide deck, hero animation,
  game HUD, NFT marketplace, wallet/DEX, onboarding game-loop. Step 3.
- **Animation rules** — Stage / Sprite engine, Expo easing, narrative
  pacing, anti-pitfall checklist. Step 3 (engine code rewrite needed).
- **Tweaks live-tuning system** — toggling design variations. Step 3.
- **Critique guide** — N-dimension scoring after delivery. Step 3.

## Cross-agent environment adaptation

This skill is designed for Claude Code as the host agent. It also runs
under any markdown-skill-capable agent (Cursor, Trae, etc.) provided
the harness honors `permissions.deny` / `permissions.ask` in
`.claude/settings.json`. If your agent does not, the skill's security
guarantees degrade — sanitizers still run on demand, but external
fetches are no longer gated by the harness.

For Codex CLI integration specifically, install codex-cli ≥ v0.115
locally and run `codex login` once. The skill assumes codex-cli's own
OAuth token; no API key lives in any settings file in this repo.
