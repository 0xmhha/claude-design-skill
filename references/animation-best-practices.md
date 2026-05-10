# Animation best practices

How to make motion feel intentional rather than ornamental. The
guidance below leans on three external authorities — [Material
Design 3 motion](https://m3.material.io/styles/motion/overview),
[Apple HIG · Motion](https://developer.apple.com/design/human-interface-guidelines/motion),
and the [CSS Easing Functions Level 1 spec](https://www.w3.org/TR/css-easing-1/) —
plus practice the maintainer has accumulated. Pair this document
with the engine reference (`references/animation-engine.md`) and
the pitfalls list (`references/animation-pitfalls.md`).

---

## A 5-tier timing scale

The single biggest improvement to LLM-generated animation is
**applying any consistent timing system at all**. Pick a tier;
use it. Five tiers cover almost every case:

| Tier | Duration | Use for |
|---|---|---|
| **Feedback** | 60–80 ms | hover lift, focus ring, tap response, toggle flip |
| **Small** | 150–180 ms | dropdown open, tooltip in/out, inline state change |
| **Medium** | 250–280 ms | sheet open, modal in, list-row reorder |
| **Entrance** | 380–450 ms | hero entry, full-screen route change, reveal sequence |
| **Heroic** | 600–900 ms | celebratory animation, single-shot delight moment |

A 250 ms applied to feedback feels sluggish; a 250 ms applied to a
hero feels rushed. Mismatching the tier to the content is the
fastest way to make a deliverable feel "off" without anyone being
able to point at why. Material 3's standard tokens
(`short1`/`short2`/.../ `long4`) follow the same general shape.

The sub-100 ms band is where Apple's HIG recommends *no animation*
for state that must feel instant (Apple HIG · Motion). For input
feedback, prefer the bottom of the **Feedback** tier (60 ms) over
no animation at all — instantaneous visual change reads as glitch
to many users.

---

## Easing selection — quick table

| Situation | Easing | Why |
|---|---|---|
| Element entering the screen | `easeOutCubic` / `easeOutQuart` | Decelerates into rest — gravity-aligned, calm |
| Element leaving | `easeInCubic` / `easeInQuad` | Accelerates away — gone fast, doesn't linger |
| State change in place (toggle, sheet expand) | `easeInOutCubic` | Symmetric — neither side feels privileged |
| Loading spinner / continuous loop | `linear` | Anything else creates a jarring rhythm |
| Celebratory affordance (achievement unlock, confetti) | `easeOutBack` (modest, ~10 % overshoot) | Anticipation builds the reward |
| Ambient drift (gradient mesh, idle character) | `linear` or `easeInOutQuad` on a long loop | Eye must not catch a "tick" |

Defaulting to `easeOutCubic` on everything is wrong but **less
wrong than defaulting to `linear`**. `linear` reads as mechanical
because real-world motion almost always has acceleration or
deceleration; the brain expects ease. (CSS Easing Functions
Level 1 spec, §3.1.)

The Back / Elastic family overshoots. Reserve them for moments
the user *should* notice. Applying `easeOutBack` to body-list
entries makes the page feel like a children's app.

---

## Stagger discipline

When 3–5 elements enter together, never bulk-fade. Bulk-fade has
no story; staggered entry tells the user "this list, then that
list".

| Group size | Per-element delay | Total runway |
|---|---|---|
| 2 elements | 80–120 ms | feels intentional, not slow |
| 3–4 elements | 60–100 ms | the sweet spot |
| 5–8 elements | 40–60 ms | risk of feeling like a wave |
| 9+ elements | 20–40 ms or skip stagger entirely | beyond this, stagger reads as lag |

The ratio that matters is **per-element delay vs the entrance
duration**. If entrance is 400 ms and per-element delay is 100 ms,
the last element starts at 300 ms — a 4-element list takes
700 ms total, which feels right. If the per-element delay exceeds
the entrance duration, the stagger reads as broken loading instead
of intentional pacing.

Implementation in this engine: assign each `<Sprite>` a
`start` value offset by `delay × index`. The pattern lives in
`references/animation-engine.md` worked example 2.

---

## Direction conventions

For most contexts (Western reading order, gravity-aligned web /
mobile), motion follows two conventions:

- **Enter from below**, exit downward — Material Motion's
  default for surface elevation and the iOS sheet transition.
  Counter-cultural: enter from above (use sparingly; reads as
  "notification" or "system message").
- **Forward motion is left-to-right; back motion is
  right-to-left** — applies to navigation transitions and
  carousel slides. The CSS direction (`dir="rtl"`) inverts this
  pair correctly when respected.

For game / web3 chrome: HUD elements often enter from the edge
they live on (top-left identity, top-right wallet status, etc.),
not from below. The convention is "enter from your home edge" —
which is *not* the same as the marketing-page convention.

---

## Reduced-motion is first-class, not a fallback

`@media (prefers-reduced-motion: reduce)` is a real user signal,
not a corner case. The W3C WAI's animation guidance treats it as
the default for some users and a hard requirement for any
deliverable that ships to a public audience.

Three patterns satisfy it:

1. **Static fallback** — the entrance state is the final state;
   nothing animates. Often the cleanest answer.
2. **Reduced-amplitude animation** — same duration, but
   transform offsets are zeroed (no `translateY`); only opacity
   moves. Useful for narrative pacing where rhythm matters but
   movement doesn't.
3. **Reduced-frequency loops** — ambient loops jump straight to
   their resting frame instead of repeating.

The Stage / Sprite engine handles this by jumping `time` to
`duration` immediately when `prefers-reduced-motion: reduce` is
set (`<Stage respectReducedMotion>`, default true). Caller code
should still avoid placing critical information *only* in motion
— a reduced-motion viewer must still be able to read the page.

---

## Performance budget

60 fps means 16.7 ms per frame. Two properties animate cheaply on
the GPU compositor: `transform` and `opacity`. Everything else
(width, height, top, left, color, box-shadow, filter) forces
layout or paint. The W3C recommendation and Chrome's animation
guide both say the same thing: **animate transform and opacity
only on hot paths**.

- `width / height` → use `scale()` instead.
- `top / left` → use `translate()` instead.
- `color` → if the cross-fade is critical, animate two layers
  with `opacity`; if not, switch instantly.
- `box-shadow` / `filter` → expensive paint. Animate sparingly,
  prefer pre-composited shadows.

Profile in DevTools' Rendering panel ("Paint flashing" / "Layer
borders") if a sequence drops frames. Cheap to check, expensive
to ignore.

---

## Loop discipline

Loop only when the narrative says "ambient":

- **Loading indicator** — loop until loaded.
- **Live state** (recording, sync-in-progress) — loop until the
  state changes.
- **Continuous environment** (idle character breathing, ambient
  particle drift) — loop, but keep the amplitude small.

Do *not* loop:

- Hero entries. The entry happens once. Replaying it on every
  scroll-revisit is fatigue.
- Decorative gradient mesh behind hero copy. Looping is what
  makes this read as AI-generated (see Anti-AI-slop §10 in
  SKILL.md).
- Anything the user is asked to *read*. Looping motion behind
  text actively prevents reading.

If a loop is unavoidable, pick `linear` easing or a slow
`easeInOutQuad`. Anything sharper makes the brain catch the loop
boundary, which converts ambient motion into nervous tic.

---

## Cross-fade vs morph

Two paradigms for transitioning between content:

- **Cross-fade** — content A fades out; content B fades in.
  Default for *unrelated* content (route changes, list-empty →
  list-populated). Reads as "different thing now".
- **Morph** — content A's elements transform into content B's
  positions. Default for *related* content (filtered list view,
  detail expansion from a card). Reads as "same thing,
  rearranged".

Picking morph when the contents are unrelated reads as confused;
picking cross-fade when they're related loses the relationship
the user could have used to track.

The Stage / Sprite engine handles cross-fade naturally
(`keepAfter` on the outgoing Sprite while the incoming sprite
enters). Morph requires layout-shared elements; for that, FLIP
(First-Last-Invert-Play) is the standard technique — outside this
engine's scope, but documented in
[Paul Lewis's FLIP introduction](https://aerotwist.com/blog/flip-your-animations/).

---

## Use-case routing

Quick map from common briefs to the right shape:

- **Deck cover reveal** — Heroic tier (600–900 ms), entrance from
  below with `easeOutCubic`, stagger 80–100 ms across title /
  subtitle / meta, single-shot (no loop).
- **App screen entry** — Entrance tier (380–450 ms), per Material
  Motion choreography (sheet from below, `easeOutCubic`),
  stagger if multiple cards at 60 ms apart, respect reduced-motion.
- **Modal / sheet** — Medium tier (250–280 ms),
  `easeInOutCubic` for symmetric in/out, opacity + scale
  (96 % → 100 %), no offset translate.
- **Hover affordance** — Feedback tier (60–80 ms),
  `easeOutQuad`, transform-only.
- **Loading indicator** — Linear loop, total cycle 800–1200 ms.
- **State acknowledgment** (success toast, save confirmation) —
  Small tier (150–180 ms) entrance, hold 1.5–2 s, Small tier
  exit. Color emits state; motion confirms it landed.
- **Game HUD damage flash** — Feedback tier (80 ms) full,
  `linear` for combat readability (deceleration would feel
  delayed), red overlay opacity.
- **Wallet transaction confirmation** — Heroic tier on success
  (one-shot, modest `easeOutBack`); Medium tier on pending
  (looped progress).

When in doubt, smaller and faster reads better than larger and
slower. The most-cited HIG advice from both Apple and Material —
*reduce motion, prefer purpose* — is the right default here too.

---

## External references

- [Material Design 3 · Motion overview](https://m3.material.io/styles/motion/overview)
- [Material Design 3 · Easing & duration tokens](https://m3.material.io/styles/motion/easing-and-duration/tokens-specs)
- [Apple HIG · Motion](https://developer.apple.com/design/human-interface-guidelines/motion)
- [CSS Easing Functions Level 1 (W3C)](https://www.w3.org/TR/css-easing-1/)
- [WCAG 2.2 · Animation from Interactions (2.3.3)](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html)
- [Paul Lewis — FLIP technique](https://aerotwist.com/blog/flip-your-animations/)
- [Chrome — Animations performance](https://web.dev/articles/animations-guide)

Cite these externally when explaining a choice; do **not**
paraphrase their prose into the deliverable. The point of a link
is the link.
