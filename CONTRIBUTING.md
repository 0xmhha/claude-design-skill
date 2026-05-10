# Contributing

This project is an internal R&D Claude Code skill, maintained by a
single owner. The most likely audiences are:

1. **Fork operators** adopting the skill for their team.
2. **Security reporters** finding regressions in the sanitizer,
   scanner, import gate, or codename catalog.
3. **Casual readers** treating the repo as a reference.

External contributions in the form of unsolicited PRs are not
currently sought. If you have a fix or improvement, read the rest of
this file before opening one.

## For fork operators

A fork is the expected adoption path. The repo ships
`scripts/init-brand.py` to bootstrap your per-fork
`team-brand-spec.json` (see `references/brand-spec-fields.md
§Bootstrap script`). After that:

1. Replace placeholder values in `team-brand-spec.json`.
2. Add your team's codename namespace to
   `scripts/codex-image-import.py:DEFAULT_CODENAME_PATTERNS` and
   mirror the row in `references/security-config.md §1.5`.
3. Add internal asset hosts to
   `examples/dot-claude-settings.json:permissions.ask` and mirror
   the row in `references/security-config.md §1.2`.
4. Decide `watermark.enabled` — default off; opt-in only.
5. Replace `LICENSE` and `NOTICE` if your team needs a different
   license (internal-only, source-available, or another open license).
   The Apache-2.0 grant in this repo applies only to its own commits;
   downstream forks are free to relicense their own modifications.
6. Mirror to your private git host. Strip any team-specific text
   from a public copy if you keep one.

The full Step 4 checklist with current ✓ / ⏳ status lives in
`HANDOFF.md §8`.

## For security reporters

See `SECURITY.md`. Use GitHub's private security advisories rather
than opening a public issue.

## For PR contributors (rare)

If you do open a PR despite the above:

- The PR must pass `.github/workflows/sanitizers.yml` (78 regression
  tests + JSON template lint + advisory asset scan). PRs that turn
  any hard-fail step amber will not be merged.
- The license-clean read discipline is non-negotiable. **Do not** open
  PRs that paraphrase the upstream `alchaincyf/huashu-design`. The
  test for "did this PR paraphrase the upstream" is whether the PR
  author can reproduce the same prose without re-reading the
  upstream — see `HANDOFF.md §0` and the `PROJECT-PLAN.md §7`
  decisions log entries for what license-clean evidence looks like.
- Sanitizer and gate changes must be accompanied by a regression
  test in the matching `scripts/test_*` suite. Coverage rules are in
  the per-suite docstring.
- Animation engine changes must keep `<Stage>` / `<Sprite>` /
  `useTime` / `useSprite` / `interpolate` / `Easing` API-compatible
  unless the PR explicitly documents the breakage with a migration
  note in `references/animation-engine.md`.
- Doc-only PRs are welcome and follow the same workflow.
- By submitting a PR, you agree your contribution is licensed under
  Apache License 2.0 (see `LICENSE`). The repository does not require
  a separate CLA on top of Apache §5.

## Project conventions

- Commit messages: imperative present tense, ≤72-char subject, body
  describes the *why* and lists the *what*. See `git log` for the
  shape used through Step 1–4.
- No `Co-Authored-By: Claude` (or any AI assistant) trailers unless
  the maintainer explicitly invites them. See `HANDOFF.md §5.4`.
- Test counts in commit messages should be quoted as `N/N OK`
  (matching the regression-suite output) so future readers can verify
  without re-running.
- The decisions log in `PROJECT-PLAN.md §7` is append-only — past
  entries are correct at the time of writing and do not get rewritten
  to match later state.
