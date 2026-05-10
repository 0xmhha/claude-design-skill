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

## Tweaks live-tuning system

When the user says "show me a cooler version" or "what does this
look like denser?", the wrong move is to ask the LLM to re-render
the whole artifact. The right move is to expose the variation as a
live toggle the user can flip themselves — no re-prompt, no
regenerated layout, no taste drift between rounds.

`assets/tweaks.js` ships a small two-element component for that —
`<tweak-panel>` plus `<tweak>` children — that turns a handful of
attribute declarations into a floating panel of segmented controls.

### Why this exists

- **Re-rendering is expensive and lossy.** Every full re-render
  through an LLM risks landing on a different version of "the same
  design", and small details drift between rounds.
- **Designers want to compare, not regenerate.** Switching between
  warm and cool palette in 100 ms next to each other is a different
  decision-making mode than reading two regenerated versions
  separately.
- **Most design variations are CSS variables.** Palette, density,
  accent, radius scale, type scale — the variation lives in tokens,
  not layout. A live toggle exposes the tokens to the user without
  the agent in the loop.

### Public API

Caller markup (place at end of `<body>`; one panel per page):

```html
<tweak-panel position="bottom-right">
  <tweak name="palette"
         options="warm|cool|neutral"
         default="warm"
         label="Palette"></tweak>
  <tweak name="density"
         options="compact|comfortable|spacious"
         default="comfortable"
         label="Density"></tweak>
  <tweak name="accent"
         options="orange|blue|green"
         default="orange"
         label="Accent"></tweak>
</tweak-panel>
```

`<tweak-panel>` attributes:

- `position` — `"bottom-right"` (default), `"bottom-left"`,
  `"top-right"`, `"top-left"`.
- `open` — present means the panel starts visible. Absent means
  hidden until the hotkey is pressed.
- `hotkey` — toggle key, default `"t"`. Pass `hotkey=""` to disable
  the hotkey entirely (use the `.set()` API instead).

`<tweak>` attributes:

- `name` — required. Becomes `data-tweak-<name>` on `<html>`.
  Lowercase, kebab-case (`palette`, `card-radius`).
- `options` — required. Pipe-separated value list (`"a|b|c"`).
- `default` — required. One of the options.
- `label` — optional. Display name in the panel; defaults to `name`.

### Caller CSS pattern (no JavaScript on the caller side)

The panel writes the chosen values onto `<html>` as
`data-tweak-<name>` attributes. Caller CSS reads them back with
attribute selectors and rewrites design tokens:

```css
:root[data-tweak-palette="warm"]    { --bg: #fef3c7; --fg: #1a1a1a; }
:root[data-tweak-palette="cool"]    { --bg: #dbeafe; --fg: #0f172a; }
:root[data-tweak-density="compact"] { --gap: 14px; }
:root[data-tweak-accent="orange"]   { --accent: #f97316; }
```

The page itself binds those tokens (`background: var(--bg)`,
`gap: var(--gap)`, etc.). No caller JS is required for the live
update — the cascade does the work.

### Persistence, hotkey, event

- **localStorage** — selections persist per `(pathname, name)` pair
  under the `tweak::` namespace; reload remembers them. The panel's
  built-in **Reset** button (top-right of the panel) restores
  defaults and clears storage.
- **Hotkey** — `t` toggles the panel; `Esc` closes it when open.
  Both are scoped: typing in `<input>`, `<textarea>`, `<select>`,
  or a `contenteditable` element does not trigger the hotkey.
- **Event** — every change dispatches a `tweakchange` CustomEvent
  on `document`. `event.detail` is `{ name, value, source }` where
  `source` is `"user"` (panel click or `.set()`) or `"restore"`
  (initial localStorage replay). Use this if app code needs to
  reload data on density change, swap an icon set on accent change,
  etc.

### Public methods

The panel exposes a small JS API for programmatic use:

- `.set(name, value)` — change a tweak from code (e.g. URL
  parameter, A/B routing, or a "magic key" cheat in dev).
- `.get(name)` — read the current value.
- `.values` — `{ name: value, … }` snapshot.
- `.reset()` — restore defaults and clear localStorage.

### Worked example

A runnable demo lives at `examples/tweaks-demo.html`. It declares
three tweaks (palette / density / accent), wires the matching CSS
on `<html>`, and lets the page background, grid gap, card padding,
and accent move live as the panel toggles. Open it, press `t`,
change a value, reload the page — the choice survives.

### When *not* to use it

- A one-off A/B that does not need live exploration. Just render
  both side by side.
- Variations that change layout structure, not just tokens. Layout
  changes warrant a real re-render — the tweak panel is for token
  swaps, not whole-page restructure.
- Production apps. Tweak-panel is a design-review tool. Strip it
  out before shipping (or hide it behind a `?tweaks=1` URL guard
  if you want it preserved as a dev affordance).

## Critique guide

The agent's biggest review failure isn't shipping bad work — it's
shipping work that has obvious issues a designer would catch in
thirty seconds. The fix is a structured pass over the artifact,
scored on six concrete dimensions, before declaring done. The
Junior Designer workflow's Stage 4 (`## Junior Designer workflow`)
calls this section; this is where the actual critique runs.

### Why six dimensions

Five dimensions is the most common shape, which is why this skill
deliberately uses six. The split that matters is putting **color
& contrast** on its own axis (so accessibility doesn't hide inside
"visual"), and putting **spacing & rhythm** on its own axis (so
density choices show up in the score). Both move differently from
hierarchy and typography and deserve their own evaluation.

### The six dimensions

Each dimension is defined in concrete behavior — what passes, what
fails — not adjectives.

#### 1 · Visual hierarchy

Can the eye find the primary message in under two seconds without
reading? Score how well size, weight, contrast, and position route
attention. A 10 has one obvious entry point and a clear secondary
read; a 4 has the headline, a sub-section, and a CTA all competing
for first place.

Common fail: every card weighs the same — same border, same
padding, same heading size — so nothing leads.

#### 2 · Typography

Are the typeface, scale, line-height, and tracking deliberate, or
are they the LLM defaults (Inter, 16 px, 1.5 line-height,
auto-tracking)? Score the *intent* visible in the choices, not the
choices themselves. Geist at 16 px is a 9; Inter at 16 px is a 6
unless there's an explicit reason ("we standardized on Inter
because the brand spec says so" → 8).

Common fail: display heading at body line-height (1.5). Tight
display copy needs 1.05–1.15.

#### 3 · Color & contrast

Does the palette have a role-system (primary surface, secondary
surface, accent, danger, muted text), and does every text block
hit WCAG AA contrast ratios at the actual sizes used?

The role-system check is structural: a 9 says "this is the muted
text token, used in 3 places consistently"; a 5 says "I can find
six grays in the file with no obvious reason for any of them."

The contrast check is mechanical: pick the worst-case body text
on the worst-case background and compute the ratio. Below 4.5:1
on body, below 3:1 on large display, score drops by 2.

#### 4 · Spacing & rhythm

Is the vertical cadence varied across hero / content / dense /
footer regions, or does every section get the same `py-24`?
Spacing is half the design — sections that read "uniform" usually
read "AI" because the LLM doesn't see page rhythm.

Score the *cadence variation*, not the absolute spacing. A 9
breathes in the hero, compresses through dense lists, lets the
footer step down. A 5 paints every region the same height.

#### 5 · Motion & micro-interactions

Do animations reinforce hierarchy and state, or just decorate?
Hover affordance, focus rings, state transitions, list reorder —
these earn motion. Ambient orb pulses behind the headline don't.

Specifically score:

- Does every interactive element have a hover *and* focus state?
- Are state transitions (loading → loaded, closed → open)
  animated to communicate the change, not to dress it up?
- Is reduced-motion respected (`@media (prefers-reduced-motion)`)?

A 9 reinforces; a 4 decorates; a 1 has no motion at all and a
non-trivial number of interactive elements.

#### 6 · Copy & narrative

Does the copy say something specific to this product, or is it
placeholder marketing fill? "Empower your team to do more" plugs
into any product, so it says nothing. Real copy mentions the
actual feature, the actual pain, the actual user.

Score the *specificity*. A 9 has a sentence the user could read
and identify the product cold. A 5 reads like marketing-template
copy. A 2 has lorem ipsum still in production positions.

### Scoring shape

Each dimension gets a single line: **score / 10 · one-sentence
reason · one concrete fix**. No essay paragraphs. The point of the
critique is to land actionable fixes, not to admire the analysis.

Aggregate score is the sum / 60 (or the average × 10). Use it as
a delivery gate, not a vanity metric:

| Total | Action |
|---|---|
| 51–60 | Ship. Apply any fix that costs <5 minutes; let the rest go to v2. |
| 39–50 | Apply every named fix, then re-score. Do not ship the unfixed pass. |
| 27–38 | Return to Stage 2 reasoning. The direction itself is drifting; restating the contract usually surfaces what's wrong. |
| <27 | Scrap. The brief or the chosen direction is wrong. Don't polish a wrong direction. |

The threshold matters because the agent's natural failure mode is
to declare "looks fine" at a 35 and ship.

### Worked critique · `examples/tweaks-demo.html`

Applied to a real prior deliverable from this skill — the
tweak-panel demo, viewed at desktop 1280 × 900 in three states
(default warm-comfortable-orange, panel revealed, cool-spacious-
blue). The screenshots from Step 2.5's visual smoke are the
evidence base.

**1 · Visual hierarchy** · 7 / 10. The hero sequences cleanly
(eyebrow → "Three knobs. No re-render." → lede → grid → CTA →
footnote). The three step-cards weigh exactly the same, though,
so the 1 → 2 → 3 sequence reads as parallel rather than ordered.
*Fix*: tone the Step 2 + Step 3 eyebrow color one notch muter, or
let Step 1's heading be slightly heavier. One change, ~2 min.

**2 · Typography** · 6 / 10. Display weight 800 with -1.4 px
tracking on the h1 shows intent. Body and inline `<code>` are
LLM-default — system stack on body, ad-hoc inline-styled `code`
spans inside the lede paragraph. The `code` styling is
copy-pasted from the card-detail block and not factored to a
shared token.
*Fix*: pull `<code>` into one shared rule (background, padding,
radius, font-family); pick a body font with character (Geist,
Söhne, or Untitled Sans).

**3 · Color & contrast** · 7 / 10. Palette × accent matrix
(3 × 3) all clear AA on body text against the page background.
Card surfaces are `rgba(255,255,255,0.5)` — fine on the warm
yellow palette, but on the `cool` palette (`#dbeafe`) the cards
nearly disappear because the white overlay reads almost identical
to the background.
*Fix*: make the card overlay palette-aware
(`:root[data-tweak-palette="cool"] .card { background:
rgba(255,255,255,0.7); }`), or switch to a darker translucent
overlay (`rgba(0,0,0,0.04)`).

**4 · Spacing & rhythm** · 6 / 10. The compact / comfortable /
spacious tweak shows that the *cadence engine* exists. The
delivered cadence itself, though, is uniform: hero, grid, CTA,
and footnote all sit at default `comfortable` rhythm. The hero
doesn't breathe more than the dense content does.
*Fix*: hero gets larger top/bottom padding, footnote gets smaller
top margin. Two CSS rules, one rhythm check.

**5 · Motion & micro-interactions** · 4 / 10. Tweak transitions
are well-tuned (240 ms ease on bg, gap, padding). Outside the
tweak panel itself, though, only the CTA has hover (`translateY`).
Cards, eyebrows, and pills have no hover or focus state. Reduced-
motion is not respected. Keyboard focus ring is browser-default
(invisible on the colored backgrounds).
*Fix*: ship a `:focus-visible { outline: 2px solid var(--accent);
outline-offset: 3px }` rule; add a subtle card hover (`box-shadow`
lift); wrap the existing transitions in
`@media (prefers-reduced-motion: no-preference)`.

**6 · Copy & narrative** · 8 / 10. "Three knobs. No re-render."
is direct, specific, marketing-fluff-free. Step descriptions name
the actual mechanism (`data-tweak-<name>` attribute, localStorage,
CustomEvent). The footnote is honest about what the page proves.
The single placeholder is "Hypothetical CTA" on the button — used
deliberately to signal it's a demo, but in any other context it
would itself be slop (Anti-slop pattern #8).
*Fix*: leave it for the demo, but flag it explicitly in the body
copy: change the CTA to "Hypothetical CTA — wire to real action"
or similar so the placeholder is self-labeled.

**Total: 38 / 60.** Threshold table places this in
**27–38: return to Stage 2 reasoning**.

But the demo's purpose was *narrow* — show that three knobs move
five CSS variables — not "publish a marketing landing page." The
brief is the lower bar. Re-scored against the actual brief
("worked example proving the tweak-panel API"), motion and
spacing weights drop and the artifact passes. **This is exactly
the case the threshold table is meant to surface**: the unfixed
score is a 38, but the *brief-relative* score is higher. Re-score
relative to the brief before scrapping; don't auto-fail on
absolute marks.

### Limitations

- The critique gates *what the agent can see*. If the brief
  involves a brand the agent has no exposure to, mechanical
  contrast and spacing checks still apply, but typography and
  copy critiques will miss brand-internal taste decisions.
- A single critique pass scores the *current state*, not the
  trajectory. If the artifact is a Stage-3 placeholder by design
  (per Junior Designer workflow), several dimensions will be
  intentionally unfinished — score against the *placeholder*
  brief, not the polish brief.
- Overall scores under 27 don't mean "the agent is bad at
  design"; they mean the brief or the chosen direction is wrong.
  The fix is one level up (Stage 2 reasoning), not at this
  layer.

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
| **Tweaks live-tuning system** — `<tweak-panel>` + `<tweak>` web component, data-attribute CSS pattern, localStorage persistence, hotkey, `tweakchange` event | `## Tweaks live-tuning system` (this skill) + `assets/tweaks.js` + `examples/tweaks-demo.html` |
| **Critique guide** — 6-dimension scoring (visual hierarchy, typography, color & contrast, spacing & rhythm, motion & micro-interactions, copy & narrative), threshold rule, worked critique on `tweaks-demo.html` | `## Critique guide` (this skill) |

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
