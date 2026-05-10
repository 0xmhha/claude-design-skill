/**
 * Stage / Sprite timeline engine
 *
 * Lightweight React-based timeline. Public API:
 *
 *   <Stage duration={3000} loop>...</Stage>
 *     - Root container; manages a clock in milliseconds.
 *     - `loop`     : when true, time wraps back to 0 at duration.
 *     - `paused`   : freeze the clock at the current time.
 *     - `time`     : controlled-mode override; if provided, the
 *                    Stage uses this exact time instead of running
 *                    a requestAnimationFrame loop. Useful for
 *                    deterministic snapshots and tests.
 *     - `respectReducedMotion` (default true): when the user has
 *                    `prefers-reduced-motion: reduce`, the Stage
 *                    jumps to `time = duration` immediately and
 *                    stays there.
 *
 *   <Sprite start={0} end={1000}>{children}</Sprite>
 *     - Active during [start, end] in ms. Renders nothing outside
 *       the window unless `keepAfter` or `freezeBefore` is set.
 *     - `keepAfter`    : keep rendering after `end` (final state
 *                        held).
 *     - `freezeBefore` : render at progress 0 from `time = 0`
 *                        instead of nothing.
 *
 *   useTime()
 *     - Hook returning the Stage's current time (ms).
 *
 *   useSprite()
 *     - Hook returning local progress 0..1 inside a <Sprite>.
 *       Outside <Sprite>, falls back to (stageTime / duration).
 *
 *   interpolate(t, [inMin, inMax], [outMin, outMax], easing?, extrapolate?)
 *     - Maps `t` from input range to output range with an optional
 *       easing function. `extrapolate` is "clamp" (default) or
 *       "extend" (let values run outside [outMin, outMax]).
 *
 *   Easing
 *     - The frozen pack from `assets/easing.js`. Loaded as
 *       `window.Easing` if `easing.js` was included before this
 *       file in the page.
 *
 * Pre-load order in HTML:
 *   <script src="easing.js"></script>
 *   <script src="animations.jsx" type="text/babel"></script>
 *
 * Worked example:
 *   <Stage duration={3000}>
 *     <Sprite start={0} end={500}>
 *       <Title />
 *     </Sprite>
 *     <Sprite start={400} end={1500} keepAfter>
 *       <Subtitle />
 *     </Sprite>
 *   </Stage>
 *
 *   // inside Subtitle:
 *   const p = useSprite();             // 0..1 over 400..1500 ms
 *   const eased = window.Easing.easeOutCubic(p);
 *   const opacity = interpolate(eased, [0, 1], [0, 1]);
 *   const dy = interpolate(eased, [0, 1], [24, 0]);
 */

const StageContext = React.createContext({
  time: 0,
  duration: 1000,
  playing: false,
});

const SpriteContext = React.createContext(null);

function Stage({
  duration = 1000,
  loop = false,
  paused = false,
  time: controlledTime,
  respectReducedMotion = true,
  onTimeUpdate,
  children,
}) {
  const [internalTime, setInternalTime] = React.useState(0);
  const [reducedMotion, setReducedMotion] = React.useState(false);

  // Detect prefers-reduced-motion once on mount + on change.
  React.useEffect(() => {
    if (!respectReducedMotion) { setReducedMotion(false); return; }
    if (typeof window === 'undefined' || !window.matchMedia) return;
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    const apply = (e) => setReducedMotion(e.matches);
    apply(mq);
    if (mq.addEventListener) {
      mq.addEventListener('change', apply);
      return () => mq.removeEventListener('change', apply);
    }
  }, [respectReducedMotion]);

  // Drive internal clock with rAF when uncontrolled, not paused, no reduced-motion.
  React.useEffect(() => {
    if (controlledTime !== undefined) return;     // controlled mode: skip rAF
    if (paused) return;
    if (reducedMotion) {
      setInternalTime(duration);
      return;
    }
    let raf = null;
    let originMs = null;
    const tick = (now) => {
      if (originMs == null) originMs = now - internalTime;
      let t = now - originMs;
      if (loop) {
        t = duration > 0 ? ((t % duration) + duration) % duration : 0;
      } else if (t > duration) {
        t = duration;
      }
      setInternalTime(t);
      if (onTimeUpdate) onTimeUpdate(t);
      if (loop || t < duration) {
        raf = requestAnimationFrame(tick);
      }
    };
    raf = requestAnimationFrame(tick);
    return () => { if (raf != null) cancelAnimationFrame(raf); };
    // We intentionally exclude internalTime / onTimeUpdate from deps
    // so the rAF loop is not torn down on every frame.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [duration, loop, paused, reducedMotion, controlledTime]);

  const time = controlledTime !== undefined ? controlledTime : internalTime;

  const value = React.useMemo(
    () => ({ time, duration, playing: !paused && controlledTime === undefined }),
    [time, duration, paused, controlledTime],
  );

  return React.createElement(StageContext.Provider, { value }, children);
}

function Sprite({
  start = 0,
  end = 1,
  keepAfter = false,
  freezeBefore = false,
  children,
}) {
  const { time } = React.useContext(StageContext);

  const inWindow = time >= start && time <= end;
  const visible =
    inWindow ||
    (keepAfter && time > end) ||
    (freezeBefore && time < start);

  // Local progress 0..1 within [start, end]. Clamped: when before the
  // window, 0; when after, 1. (Avoids divide-by-zero on degenerate ranges.)
  let progress;
  if (end <= start) {
    progress = time >= end ? 1 : 0;
  } else {
    progress = (time - start) / (end - start);
    if (progress < 0) progress = 0;
    if (progress > 1) progress = 1;
  }

  const value = React.useMemo(
    () => ({ start, end, active: inWindow, progress, visible }),
    [start, end, inWindow, progress, visible],
  );

  if (!visible) return null;
  return React.createElement(SpriteContext.Provider, { value }, children);
}

function useTime() {
  const ctx = React.useContext(StageContext);
  return ctx ? ctx.time : 0;
}

function useSprite() {
  const sp = React.useContext(SpriteContext);
  const stage = React.useContext(StageContext);
  if (sp) return sp.progress;
  if (!stage || !stage.duration) return 0;
  let p = stage.time / stage.duration;
  if (p < 0) p = 0;
  if (p > 1) p = 1;
  return p;
}

function interpolate(t, inputRange, outputRange, easing, extrapolate) {
  const ease = typeof easing === 'function' ? easing : (x) => x;
  const mode = extrapolate === 'extend' ? 'extend' : 'clamp';

  const inMin = inputRange[0];
  const inMax = inputRange[1];
  const outMin = outputRange[0];
  const outMax = outputRange[1];

  if (inMax === inMin) return outMin;

  let norm = (t - inMin) / (inMax - inMin);
  if (mode === 'clamp') {
    if (norm < 0) norm = 0;
    if (norm > 1) norm = 1;
  }
  const eased = ease(norm);
  return outMin + eased * (outMax - outMin);
}

if (typeof window !== 'undefined') {
  window.Stage = Stage;
  window.Sprite = Sprite;
  window.useTime = useTime;
  window.useSprite = useSprite;
  window.interpolate = interpolate;
  // window.Easing is set by easing.js (loaded earlier).
}
