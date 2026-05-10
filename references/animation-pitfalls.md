# Animation pitfalls

The patterns below are how agent-driven animation goes wrong. Each
one is a pattern the maintainer keeps catching in review. Pair
this list with `references/animation-best-practices.md` (the
positive guidance) and the engine reference
(`references/animation-engine.md`).

For every pitfall: **why it's bad** → **symptom you'll see** →
**fix**.

---

## 1 · Bounce-on-everything

**Why it's bad**: `easeOutBack` and `easeOutElastic` overshoot
their target. Used on every entry, the page reads as a children's
app — the overshoot signals "look at me!" and there's nothing
worth looking at the tenth time.

**Symptom**: every list row, every card, every dropdown
overshoots and settles. The page feels twitchy.

**Fix**: reserve overshoot for celebratory affordances —
achievement unlocks, transaction confirmations, first-run
flourishes. Default to `easeOutCubic` everywhere else
(`references/animation-best-practices.md` · easing table).

---

## 2 · Linear easing as default

**Why it's bad**: `linear` reads as mechanical because real-world
motion has acceleration and deceleration. The brain treats
constant velocity as machine output, not user feedback.

**Symptom**: a hover state that feels like an industrial robot
arm. A modal that opens at the same speed it closes, with no
narrative arc.

**Fix**: use `linear` only for spinners and ambient continuous
loops. For everything else, pick `easeOutCubic` (entrance),
`easeInCubic` (exit), or `easeInOutCubic` (in-place state
change). The CSS Easing Functions spec gives the full set.

---

## 3 · One duration applied to every animation

**Why it's bad**: 250 ms applied to a hover feels sluggish; 250
ms applied to a hero feels rushed. A flat duration system
flattens the perceived hierarchy.

**Symptom**: hover lag-feel + hero-cuts-in-too-fast in the same
deliverable. Reviewer feedback uses words like "off" or
"unbalanced" without naming the cause.

**Fix**: pick a 5-tier scale and stick to it (Feedback / Small /
Medium / Entrance / Heroic). `references/animation-best-practices.md`
has the table. Match the tier to the content type, not to a
project-wide token.

---

## 4 · Animated gradient mesh behind hero copy

**Why it's bad**: a WebGL gradient orb pulsing behind the
headline is the AI-design tell. It distracts from the content,
fights for attention with the type, and scales every page in the
deliverable to feel like the same template.

**Symptom**: the user looks at the gradient first, the headline
second. Eye-tracking on this kind of hero spends 60 % of attention
on the wrong region.

**Fix**: if the brief calls for atmosphere, use a static
restrained gradient (Anti-AI-slop §8 in SKILL.md). If the brief
calls for motion, animate the *content* instead — kinetic
typography, a single hero illustration that drifts on scroll.
Background motion is rarely the answer to "this feels static".

---

## 5 · Autoplay loops on hero video

**Why it's bad**: a 12-second loop that runs forever behind copy
guarantees the user catches the loop boundary. Every loop seam
is a small visual hiccup; cumulative fatigue is real.

**Symptom**: visitors mention "this site has too much going on"
without being able to point at what. Bounce rate up, scroll depth
down on hero-heavy pages.

**Fix**: play the hero video once (`<video autoplay muted
playsinline>` without `loop`), then park on the final frame. If
the brief insists on continuous video, make it a slow-paced
ambient cycle (≥ 30 s) with no hard cuts; even then, prefer a
poster image and a Play button over autoplay.

---

## 6 · Animating the wrong CSS property

**Why it's bad**: animating `width`, `height`, `top`, `left`,
`margin` triggers layout on every frame. Animating `box-shadow`,
`filter`, or `border-radius` triggers paint. The page drops
frames, the animation jutters, the user can't say why.

**Symptom**: smooth-looking demo on the laptop; janky on a mid-
range Android phone. Chrome DevTools' "Paint flashing" lights up
the whole region.

**Fix**: animate `transform` (translate / scale / rotate) and
`opacity`. These run on the GPU compositor. Replace
`width: 100px → 200px` with `transform: scaleX(2)`; replace
`top` with `translateY()`. The full table is in
`references/animation-best-practices.md` · performance budget.

---

## 7 · Synchronized fade for groups

**Why it's bad**: 5 cards all fading in at the same time gives
the user no story — they read as "everything appeared". A 60–100
ms stagger between elements turns the same fade into "this
happened, then that happened".

**Symptom**: a list view that "pops" into existence. Hero grids
where the eye doesn't know where to land.

**Fix**: stagger entries with a 60–100 ms per-element delay (3–4
elements) or 40–60 ms (5–8 elements). The stagger total runway
should not exceed the entrance duration, or the stagger reads as
loading lag instead of pacing.

---

## 8 · Forgetting `prefers-reduced-motion`

**Why it's bad**: the W3C WAI animation guidance treats
`prefers-reduced-motion` as a real user signal. A hero that's
purely decorative animation breaks for users with vestibular
disorders, motion sensitivity, or attention disorders. Beyond
accessibility, it also fails on systems where the OS has reduced
motion enabled by default (modern macOS, recent iOS).

**Symptom**: deliverable passes manual review, fails an automated
accessibility audit. Or worse, ships and gets a complaint that
the page makes a real human dizzy.

**Fix**: the Stage / Sprite engine respects this by default
(`<Stage respectReducedMotion>`). For animation outside the
engine, wrap CSS animations in
`@media (prefers-reduced-motion: no-preference)` — that way the
default is *no* animation, and only users who haven't opted out
see motion.

---

## 9 · Decorative chrome on every state

**Why it's bad**: every hover bounces, every focus pulses, every
loaded card confettis. Each individual animation is fine; the
combination is fatigue. Users learn to ignore motion when motion
is everywhere.

**Symptom**: the user clicks something important and notices
nothing — because they've stopped registering motion as a signal.

**Fix**: motion is a signal *budget*. Spend it on transitions
that carry meaning (state change, navigation, success
confirmation). Don't spend it on chrome that already
communicates the same thing through shape, color, or text.

---

## 10 · Stagger that's too aggressive

**Why it's bad**: a 300 ms+ delay between element entries in a
short list reads as "the page is loading slowly", not as
"intentional pacing". The user starts to interact before the
animation finishes; they tap a card that hasn't entered yet.

**Symptom**: the third card in a 4-card grid doesn't render in
time for the click. The user thinks the click was lost when in
fact the card just didn't exist yet.

**Fix**: keep stagger total runway under the entrance duration.
If entrance is 400 ms, the last element must start by 300 ms
(per-element delay × element count ≤ 300 ms). For larger groups,
shorten the per-element delay rather than letting the runway
extend.

---

## 11 · Inconsistent timing across the deliverable

**Why it's bad**: 200 ms hover here, 240 ms there, 380 ms on
modals, 420 ms on sheets. None of the values are wrong; the
absence of a system is. The user reads the inconsistency as
"this is built by a committee".

**Symptom**: the deliverable feels unfinished even though every
individual animation is fine. Reviewers can't say what's wrong.

**Fix**: declare the timing scale once at the project root — as
CSS variables, as Tailwind tokens, as design-system constants —
and reach for those names everywhere. The 5-tier scale in
`references/animation-best-practices.md` is a sufficient default;
project-specific scales should still pick a fixed N and stop
there.

---

## 12 · Ambient loops with no escape

**Why it's bad**: an ambient pulse that never settles drains
attention battery. The user's peripheral vision keeps catching
motion they have to actively suppress to read the page.

**Symptom**: returning visitors describe the site as "tiring"
without being able to say why. Time-on-page suspiciously drops
across sessions.

**Fix**: every ambient loop should have an escape — settle to
rest after N seconds of viewer attention, after the user
scrolls past, or on a focus-within event. The classic example
is the cursor on a search input that pulses *until the user
focuses the input*. After that, motion stops.

---

## 13 · Animating during scroll without `will-change` or layer hints

**Why it's bad**: scroll-triggered transforms recalculate layout
on a thread that's already busy with scroll. Without GPU hints,
the page jutters precisely where it should feel kinetic.

**Symptom**: parallax that looks fine while idle, juddery the
moment the user actually scrolls. Especially visible on
trackpads with high event rates.

**Fix**: add `will-change: transform` (or `will-change: opacity`)
to elements that will animate during scroll. **Remove the hint
when the animation completes** — `will-change` permanently
applied is itself a performance regression because it forces
layer creation forever. Pair `will-change` with
`backface-visibility: hidden` only when needed (Safari quirk).

---

## 14 · Hero animation budget over 4 seconds

**Why it's bad**: a hero entrance that takes 5 seconds is a
lecture. The user has decided whether to engage with the page
within ~2 seconds; making them wait for the show to end before
the page is interactive is hostile.

**Symptom**: high bounce rate from above-the-fold hero pages.
Users hit refresh halfway through the animation, suspecting the
page has hung.

**Fix**: the Heroic tier in
`references/animation-best-practices.md` is 600–900 ms — and
that's for a *celebratory* moment, not the default hero entry.
Most hero entries should land in the Entrance tier (380–450 ms).
Anything longer needs an explicit narrative reason and, ideally,
a "skip" affordance for repeat visitors.

---

## How to use this list

Run a single mental pass over the deliverable's motion before
declaring done. Three or more pitfalls present means motion
needs a structural rethink, not a fix-list. One or two means
patch them and ship.

The Critique guide's threshold rule (SKILL.md
`## Critique guide`) applies here too: scoring "Motion &
micro-interactions" against this list is exactly what dimension
5 is for.
