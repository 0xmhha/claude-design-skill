/**
 * Easing pack — pure functions in [0, 1] → [0, 1]
 *
 * Every easing here takes a normalized time `t` (0..1) and returns
 * a normalized progress (0..1, with overshoot allowed for the
 * Back / Elastic family). Functions are pure: no state, no side
 * effects, no globals. Safe to memoize, run in workers, snapshot,
 * etc.
 *
 * The `linear` function is identity. Every other function passes
 * through `(0, 0)` and `(1, 1)` exactly (modulo IEEE rounding) —
 * regression-tested by `scripts/test_animations_easing.js`.
 *
 * Names follow the convention used in `easings.net` and the CSS
 * Easing Functions Level 1 spec: `easeIn` accelerates, `easeOut`
 * decelerates, `easeInOut` does both. Suffixes (`Quad`, `Cubic`,
 * `Expo`, `Back`, `Elastic`) name the curve family.
 *
 * Dual-export: importable as a CommonJS module from Node (test
 * harness) and exposed on `window.Easing` in the browser
 * (`<script src="easing.js">` before `animations.jsx`).
 */
(function (root, factory) {
  const Easing = factory();
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = Easing;
  }
  if (typeof window !== 'undefined') {
    window.Easing = Easing;
  }
})(typeof self !== 'undefined' ? self : this, function () {
  const PI2 = 2 * Math.PI;
  const BACK_C1 = 1.70158;
  const BACK_C2 = BACK_C1 * 1.525;
  const BACK_C3 = BACK_C1 + 1;

  function linear(t) {
    return t;
  }

  function easeInQuad(t) {
    return t * t;
  }

  function easeOutQuad(t) {
    return 1 - (1 - t) * (1 - t);
  }

  function easeInOutQuad(t) {
    return t < 0.5
      ? 2 * t * t
      : 1 - Math.pow(-2 * t + 2, 2) / 2;
  }

  function easeInCubic(t) {
    return t * t * t;
  }

  function easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
  }

  function easeInOutCubic(t) {
    return t < 0.5
      ? 4 * t * t * t
      : 1 - Math.pow(-2 * t + 2, 3) / 2;
  }

  function easeInExpo(t) {
    if (t === 0) return 0;
    return Math.pow(2, 10 * t - 10);
  }

  function easeOutExpo(t) {
    if (t === 1) return 1;
    return 1 - Math.pow(2, -10 * t);
  }

  function easeInOutExpo(t) {
    if (t === 0) return 0;
    if (t === 1) return 1;
    return t < 0.5
      ? Math.pow(2, 20 * t - 10) / 2
      : (2 - Math.pow(2, -20 * t + 10)) / 2;
  }

  function easeInBack(t) {
    // BACK_C3·t³ − BACK_C1·t² — overshoots below 0 near t≈0.6.
    return BACK_C3 * t * t * t - BACK_C1 * t * t;
  }

  function easeOutBack(t) {
    // Mirror of easeInBack: overshoots above 1 near t≈0.4 from end.
    return 1 + BACK_C3 * Math.pow(t - 1, 3) + BACK_C1 * Math.pow(t - 1, 2);
  }

  function easeInOutBack(t) {
    return t < 0.5
      ? (Math.pow(2 * t, 2) * ((BACK_C2 + 1) * 2 * t - BACK_C2)) / 2
      : (Math.pow(2 * t - 2, 2) * ((BACK_C2 + 1) * (t * 2 - 2) + BACK_C2) + 2) / 2;
  }

  function easeOutElastic(t) {
    if (t === 0 || t === 1) return t;
    const c4 = PI2 / 3;
    return Math.pow(2, -10 * t) * Math.sin((t * 10 - 0.75) * c4) + 1;
  }

  return Object.freeze({
    linear,
    easeInQuad, easeOutQuad, easeInOutQuad,
    easeInCubic, easeOutCubic, easeInOutCubic,
    easeInExpo, easeOutExpo, easeInOutExpo,
    easeInBack, easeOutBack, easeInOutBack,
    easeOutElastic,
  });
});
