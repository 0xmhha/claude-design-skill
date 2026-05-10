#!/usr/bin/env node
/**
 * Regression tests for assets/easing.js.
 *
 * Stdlib only (node:assert) — no external runner. Run as:
 *   node scripts/test_animations_easing.js
 *
 * Mirrors the convention of the other suites in this repo
 * (svg-sanitize, scan_assets, codex-image-import): print one line
 * per test case, then a summary, exit non-zero on any failure.
 */
'use strict';

const assert = require('node:assert/strict');
const path = require('node:path');

const Easing = require(path.join(__dirname, '..', 'assets', 'easing.js'));

const TOL = 1e-9;

let passed = 0;
let failed = 0;
const failures = [];

function test(name, fn) {
  try {
    fn();
    passed++;
    console.log(`  ok   ${name}`);
  } catch (e) {
    failed++;
    failures.push({ name, message: e.message });
    console.log(`  FAIL ${name}`);
    console.log(`       ${e.message}`);
  }
}

function near(actual, expected, tol = TOL, label = '') {
  if (!Number.isFinite(actual)) {
    throw new Error(`${label || 'value'} not finite: ${actual}`);
  }
  if (Math.abs(actual - expected) > tol) {
    throw new Error(
      `${label || 'value'}: got ${actual}, expected ${expected} (tol ${tol})`,
    );
  }
}

const ALL = Object.keys(Easing);

const FRAME_FUNCTIONS = ALL.filter(
  (n) => n !== 'easeInBack', // easeInBack(0) is 0 but undershoots negative mid-curve;
);                            // it still maps t=0 to 0, kept in framing test below.

/* -------- shape: every easing is a finite function on [0, 1] -------- */

test('every easing is exposed as a function', () => {
  for (const name of ALL) {
    assert.equal(typeof Easing[name], 'function', `${name} not a function`);
  }
});

test('every easing maps t=0 to 0 (within TOL)', () => {
  for (const name of ALL) {
    near(Easing[name](0), 0, TOL, `${name}(0)`);
  }
});

test('every easing maps t=1 to 1 (within TOL)', () => {
  for (const name of ALL) {
    near(Easing[name](1), 1, TOL, `${name}(1)`);
  }
});

test('every easing returns finite values across t = 0, 0.25, 0.5, 0.75, 1', () => {
  for (const name of ALL) {
    for (const t of [0, 0.25, 0.5, 0.75, 1]) {
      const v = Easing[name](t);
      assert.equal(Number.isFinite(v), true, `${name}(${t}) -> ${v}`);
    }
  }
});

/* -------- linear: identity -------- */

test('linear is identity over the unit interval', () => {
  for (let i = 0; i <= 10; i++) {
    const t = i / 10;
    near(Easing.linear(t), t, TOL, `linear(${t})`);
  }
});

/* -------- shape: easeIn vs easeOut symmetry around y = x -------- */

test('easeOutQuad(t) === 1 - easeInQuad(1 - t)', () => {
  for (const t of [0.1, 0.25, 0.4, 0.6, 0.75, 0.9]) {
    near(
      Easing.easeOutQuad(t),
      1 - Easing.easeInQuad(1 - t),
      TOL,
      `quad symmetry @ t=${t}`,
    );
  }
});

test('easeOutCubic(t) === 1 - easeInCubic(1 - t)', () => {
  for (const t of [0.1, 0.25, 0.4, 0.6, 0.75, 0.9]) {
    near(
      Easing.easeOutCubic(t),
      1 - Easing.easeInCubic(1 - t),
      TOL,
      `cubic symmetry @ t=${t}`,
    );
  }
});

test('easeOutExpo(t) === 1 - easeInExpo(1 - t) for t in (0, 1)', () => {
  // The piecewise endpoints (t = 0 and t = 1) are exact by construction,
  // so we test the open interval where the formula identity must hold.
  for (const t of [0.1, 0.25, 0.4, 0.6, 0.75, 0.9]) {
    near(
      Easing.easeOutExpo(t),
      1 - Easing.easeInExpo(1 - t),
      TOL,
      `expo symmetry @ t=${t}`,
    );
  }
});

/* -------- shape: easeOut faster than linear early, slower late -------- */

test('easeOutCubic(0.25) > 0.25 (faster early than linear)', () => {
  const v = Easing.easeOutCubic(0.25);
  assert.equal(v > 0.25, true, `easeOutCubic(0.25) = ${v}, expected > 0.25`);
});

test('easeInCubic(0.75) < 0.75 (slower late than linear)', () => {
  const v = Easing.easeInCubic(0.75);
  assert.equal(v < 0.75, true, `easeInCubic(0.75) = ${v}, expected < 0.75`);
});

/* -------- known midpoint values -------- */

test('easeInOutQuad(0.5) === 0.5', () => {
  near(Easing.easeInOutQuad(0.5), 0.5, TOL, 'easeInOutQuad(0.5)');
});

test('easeInOutCubic(0.5) === 0.5', () => {
  near(Easing.easeInOutCubic(0.5), 0.5, TOL, 'easeInOutCubic(0.5)');
});

test('easeInQuad(0.5) === 0.25', () => {
  near(Easing.easeInQuad(0.5), 0.25, TOL, 'easeInQuad(0.5)');
});

test('easeOutQuad(0.5) === 0.75', () => {
  near(Easing.easeOutQuad(0.5), 0.75, TOL, 'easeOutQuad(0.5)');
});

/* -------- back family: documented overshoot in [-0.1, 1.1] -------- */

test('easeOutBack overshoots above 1 somewhere in (0, 1)', () => {
  let maxV = 0;
  for (let i = 1; i <= 99; i++) {
    const v = Easing.easeOutBack(i / 100);
    if (v > maxV) maxV = v;
  }
  assert.equal(
    maxV > 1.0,
    true,
    `easeOutBack max in (0,1) = ${maxV}, expected > 1`,
  );
  assert.equal(
    maxV < 1.15,
    true,
    `easeOutBack max in (0,1) = ${maxV}, expected < 1.15 (sane back overshoot)`,
  );
});

test('easeInBack undershoots below 0 somewhere in (0, 1)', () => {
  let minV = 1;
  for (let i = 1; i <= 99; i++) {
    const v = Easing.easeInBack(i / 100);
    if (v < minV) minV = v;
  }
  assert.equal(
    minV < 0,
    true,
    `easeInBack min in (0,1) = ${minV}, expected < 0`,
  );
});

/* -------- elastic: bounded oscillation around 1 near the end -------- */

test('easeOutElastic stays in a sane range across the unit interval', () => {
  for (let i = 0; i <= 100; i++) {
    const t = i / 100;
    const v = Easing.easeOutElastic(t);
    assert.equal(Number.isFinite(v), true, `easeOutElastic(${t}) -> ${v}`);
    assert.equal(
      v >= -0.5 && v <= 1.5,
      true,
      `easeOutElastic(${t}) = ${v} out of [-0.5, 1.5] sanity range`,
    );
  }
});

/* -------- determinism: same input → same output -------- */

test('every easing is pure (same input always returns same output)', () => {
  for (const name of ALL) {
    const t = 0.37;
    const a = Easing[name](t);
    const b = Easing[name](t);
    near(a, b, 0, `${name} determinism`);
  }
});

/* -------- frozen: pack cannot be mutated -------- */

test('Easing pack is frozen', () => {
  let threw = false;
  try {
    Easing.linear = () => 42;
  } catch (_) {
    threw = true;
  }
  // Strict mode throws; sloppy mode silently no-ops. Either way,
  // the value must not change.
  near(Easing.linear(0.5), 0.5, TOL, 'linear after mutation attempt');
});

/* -------- summary -------- */

console.log('');
console.log(`Ran ${passed + failed} tests`);
if (failed === 0) {
  console.log('OK');
  process.exit(0);
} else {
  console.log(`FAIL — ${failed} failed:`);
  for (const f of failures) {
    console.log(`  - ${f.name}: ${f.message}`);
  }
  process.exit(1);
}
