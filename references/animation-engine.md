# Stage / Sprite animation engine

A small React-based timeline. The agent reaches for it whenever a
deliverable needs more than a CSS transition but less than a full
motion-design tool. Three nouns: a clock (`Stage`), a clip
(`Sprite`), and a number map (`interpolate`). Two hooks (`useTime`,
`useSprite`). One frozen pack (`Easing`).

The engine ships in `assets/animations.jsx` (component code) and
`assets/easing.js` (pure easing functions). The easing pack has
its own regression suite at `scripts/test_animations_easing.js`.

This document is the engine reference. For best-practices and
anti-patterns (timing, narrative pacing, common pitfalls), see
`references/animation-best-practices.md` and
`references/animation-pitfalls.md`.

---

## API surface

| Symbol | Shape | Purpose |
|---|---|---|
| `<Stage>` | component | Root timeline; owns the clock |
| `<Sprite>` | component | Time-windowed clip inside a Stage |
| `useTime()` | hook | Stage time in ms |
| `useSprite()` | hook | Local progress 0..1 inside a Sprite |
| `interpolate(t, in, out, easing?, extrapolate?)` | function | Map a number across ranges |
| `Easing` | frozen object | Easing curves: `linear`, `easeIn/Out/InOut Quad/Cubic/Expo`, `easeIn/Out/InOut Back`, `easeOutElastic` |

Browser globals: `Stage`, `Sprite`, `useTime`, `useSprite`,
`interpolate` are set on `window` after `animations.jsx` evaluates;
`Easing` is set on `window` after `easing.js` evaluates. Load
`easing.js` **before** `animations.jsx` in the page.

---

## `<Stage>` props

```jsx
<Stage
  duration={3000}            // total clock length, ms
  loop={false}               // wrap back to 0 at duration
  paused={false}             // freeze the clock at current time
  time={undefined}           // controlled mode: exact ms; bypasses rAF
  respectReducedMotion       // default true; jumps to end if user requests it
  onTimeUpdate={fn}          // optional ms callback per frame
>
  ...
</Stage>
```

Two modes:

- **Uncontrolled** (default) — Stage runs a `requestAnimationFrame`
  loop and advances `time` from 0 to `duration`. Single re-render
  per frame; expensive subtrees should be memoized.
- **Controlled** — pass `time` as a prop. The Stage uses that exact
  value and stops the rAF loop. Use this for snapshot tests,
  scrubbable timelines, and visual smoke screenshots at deterministic
  times.

The Stage exposes `(time, duration, playing)` to descendants via
React context. `Sprite` and the hooks read from there.

---

## `<Sprite>` props

```jsx
<Sprite
  start={0}                 // ms, inclusive
  end={1000}                // ms, inclusive
  keepAfter={false}         // keep rendering past `end` (final state held)
  freezeBefore={false}      // render at progress=0 from time=0 (instead of nothing)
>
  ...
</Sprite>
```

Lifecycle:

- Before `start` (and `freezeBefore` is false): renders nothing.
- During `[start, end]`: renders children; `useSprite()` returns
  local progress 0..1 over that window.
- After `end` (and `keepAfter` is false): renders nothing.

`useSprite()` outside a `<Sprite>` falls back to
`stageTime / duration` so simple animations don't need a
clip wrapper.

---

## `interpolate(t, inputRange, outputRange, easing?, extrapolate?)`

Maps a number from one range to another. Optional easing reshapes
the normalized progress before output mapping.

```js
const opacity = interpolate(p, [0, 1], [0, 1], Easing.easeOutCubic);
const dy      = interpolate(p, [0, 1], [24, 0], Easing.easeOutCubic);
```

Arguments:

- `t` — input value.
- `inputRange` — `[inMin, inMax]`. Both must be finite. If
  `inMin === inMax`, the function returns `outMin` (no division).
- `outputRange` — `[outMin, outMax]`. Output is `outMin + eased *
  (outMax - outMin)`.
- `easing` — optional pure function `[0, 1] → [0, 1]`. Defaults
  to identity.
- `extrapolate` — `"clamp"` (default) or `"extend"`. Clamp keeps
  the input ratio inside `[0, 1]`; extend lets it run past.

Return is always a number; combine multiple calls for compound
animations (opacity + transform + color, etc.).

---

## `Easing` pack

`assets/easing.js` exports a frozen object with these functions:

| Name | Shape |
|---|---|
| `linear` | `t` (identity) |
| `easeInQuad` / `easeOutQuad` / `easeInOutQuad` | quadratic acceleration / deceleration |
| `easeInCubic` / `easeOutCubic` / `easeInOutCubic` | cubic acceleration / deceleration |
| `easeInExpo` / `easeOutExpo` / `easeInOutExpo` | exponential family — strong dec/acceleration |
| `easeInBack` / `easeOutBack` / `easeInOutBack` | overshoots `[0, 1]` by ~10% — anticipation / settle |
| `easeOutElastic` | spring-style oscillation around 1 near the end |

Conventions used here follow [easings.net](https://easings.net) /
the CSS Easing Functions Level 1 spec. Each function is pure (no
state, no side effects) and frozen at module load. The regression
suite asserts:

- `f(0) ≈ 0` and `f(1) ≈ 1` for every function.
- `easeOutX(t) ≈ 1 - easeInX(1 - t)` for the Quad, Cubic, Expo
  families.
- `easeOutBack` overshoots above 1 somewhere in `(0, 1)`.
- `easeInBack` undershoots below 0 somewhere in `(0, 1)`.
- `easeOutElastic` stays inside `[-0.5, 1.5]`.
- Determinism: every function returns the same value for the same
  input on repeat calls.
- The pack is frozen (mutating attempts no-op or throw).

Run the suite locally with `node scripts/test_animations_easing.js`
(see `HANDOFF.md §1`).

---

## Worked example 1 — single fade-in

```jsx
function FadeInTitle() {
  const p = useSprite(); // 0..1 over the parent Sprite window
  const opacity = interpolate(p, [0, 1], [0, 1], Easing.easeOutCubic);
  const dy      = interpolate(p, [0, 1], [16, 0], Easing.easeOutCubic);
  return (
    <h1 style={{ opacity, transform: `translateY(${dy}px)` }}>
      Hello
    </h1>
  );
}

function App() {
  return (
    <Stage duration={1500}>
      <Sprite start={0} end={800} keepAfter>
        <FadeInTitle />
      </Sprite>
    </Stage>
  );
}
```

The title fades in over 800 ms with cubic-out (faster early, slower
late). `keepAfter` holds the final state for the remaining 700 ms
of the Stage.

---

## Worked example 2 — staggered three-line title

```jsx
function Line({ text }) {
  const p = useSprite();
  const opacity = interpolate(p, [0, 1], [0, 1], Easing.easeOutCubic);
  const dy      = interpolate(p, [0, 1], [24, 0], Easing.easeOutCubic);
  return (
    <div style={{ opacity, transform: `translateY(${dy}px)`, fontSize: 64 }}>
      {text}
    </div>
  );
}

function App() {
  return (
    <Stage duration={3000}>
      <Sprite start={0}    end={700}  keepAfter><Line text="Three knobs."   /></Sprite>
      <Sprite start={250}  end={950}  keepAfter><Line text="No re-render."  /></Sprite>
      <Sprite start={500}  end={1200} keepAfter><Line text="Live tuning."   /></Sprite>
    </Stage>
  );
}
```

A 250 ms stagger between line entries. Each Sprite has its own
0..1 progress, so each `<Line>` re-uses the same component. After
1200 ms, all three lines stay in their final state for the
remaining ~1.8 s.

---

## Worked example 3 — controlled Stage for snapshot testing

```jsx
function App({ frame }) {
  return (
    <Stage duration={3000} time={frame} paused>
      <Sprite start={0} end={1500} keepAfter>
        <Card />
      </Sprite>
    </Stage>
  );
}

// In a Playwright smoke test:
//   render <App frame={0} />    → screenshot "initial"
//   render <App frame={750} />  → screenshot "mid"
//   render <App frame={1500} /> → screenshot "settled"
```

Controlled mode disables the rAF loop; the Stage renders exactly
the time you pass. Pair with `assets/deck_stage.js` or any
visual-smoke harness to capture deterministic frames at known
times.

---

## Worked example 4 — easing showcase

```jsx
function Bar({ name, easing }) {
  const p = useSprite();
  const w = interpolate(p, [0, 1], [0, 100], easing);
  return (
    <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
      <span style={{ width: 120, fontSize: 13 }}>{name}</span>
      <div style={{ flex: 1, height: 8, background: '#eee', borderRadius: 4 }}>
        <div style={{
          width: `${w}%`, height: '100%',
          background: '#0a84ff', borderRadius: 4,
        }} />
      </div>
    </div>
  );
}

function App() {
  return (
    <Stage duration={2000} loop>
      <Sprite start={0} end={2000}>
        <Bar name="linear"          easing={Easing.linear}        />
        <Bar name="easeOutCubic"    easing={Easing.easeOutCubic}  />
        <Bar name="easeInOutCubic"  easing={Easing.easeInOutCubic}/>
        <Bar name="easeOutBack"     easing={Easing.easeOutBack}   />
        <Bar name="easeOutElastic"  easing={Easing.easeOutElastic}/>
      </Sprite>
    </Stage>
  );
}
```

Looping Stage; five bars that all fill simultaneously but on
different curves. Useful as a side-by-side reference when picking
an easing for a specific animation.

---

## Performance notes

- `<Stage>` re-renders on every animation frame in uncontrolled
  mode. Memoize children that don't depend on time
  (`React.memo`, `useMemo`) so only the time-dependent leaves
  re-evaluate.
- `interpolate` is allocation-free (returns a primitive number);
  call it freely inside render.
- `Easing` functions are pure and trivially fast; no need to
  cache results.
- For very deep trees, prefer one Sprite per *animated* leaf
  rather than wrapping a parent Sprite around a static layout —
  the Sprite is the re-render boundary.

---

## When *not* to reach for the engine

- A pure CSS transition will do (e.g. opacity on hover, a single
  property change on state). CSS handles those better.
- A real motion-design pipeline is in scope (Lottie, After Effects
  exports). Use those, then mount their output here as a child.
- The animation lives entirely inside a single component's
  internal state with no need for a global clock. `useState` +
  `useEffect` + a setTimeout is simpler.

The engine earns its place when *multiple* clips need to share a
clock (staggered title runs, deck-cover reveal sequences,
data-viz step-throughs) or when controlled-mode deterministic
snapshots are required.
