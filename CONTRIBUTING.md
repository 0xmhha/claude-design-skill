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

A fork is the expected adoption path. After Step 5 the repo ships
a **Default Studio** identity in `assets/team-brand-spec.default.json`
plus four placeholder SVGs under `assets/default-brand/`, so the
skill is fully usable out of the box. Adopters *override* — they
don't build from scratch.

### Override the identity (run the bootstrap)

```bash
# Stamp the default carrier into your project root
python3 scripts/init-brand.py
# → writes team-brand-spec.json (with _meta / _note stripped)
```

Then override:

1. **Identity fields**: `team.company`, `team.division`,
   `brand.name`, `brand.tagline_short`, `brand.tone_keywords`,
   `brand.forbidden_zones`.
2. **Logo paths**: replace the `assets/default-brand/*.svg` paths
   with your team's SVGs (1:1 mark, 4:1 wordmark, inverse for dark
   backgrounds, optional small icon). Run any external SVGs
   through `scripts/svg-sanitize.py` before committing.
3. **Brand colour**: `colors.accent.primary` defaults to `#5B7CFA`
   (deliberately neutral — not any of the 11 reference services'
   brand colour). Replace with your real accent. The
   `colors.status.*` block is Uniswap-Spore-attributed; rewrite the
   `_source` line if you replace those values.
4. **Custom typography (optional)**: swap `typography.display.family`
   and `typography.body.family`. Keep the `system_stack` lines as
   the fallback. If you have a Figma library with named text
   styles, prefer:

   ```bash
   FIGMA_TOKEN='<YOUR_TOKEN>' \
     python3 scripts/figma-to-brand-spec.py <YOUR_FIGMA_FILE_KEY>
   ```

5. **Product imagery**: fill `product_assets.*` (physical product)
   or `ui_screenshots.*` (digital product) paths. Default Studio
   is fictional so these ship empty.

### Extend the security defaults

6. **Codename namespace**: append your team's internal codename
   patterns to
   `scripts/codex-image-import.py:DEFAULT_CODENAME_PATTERNS` and
   mirror the row in `references/security-config.md §1.5`. Follow
   the *conservative-pairing* rule documented there — a bare
   single-word codename will false-positive on generic design
   language.

7. **Internal asset hosts**: add them under
   `approved_asset_hosts.internal` in your `team-brand-spec.json`,
   under `permissions.ask` in
   `examples/dot-claude-settings.json` (or your `.claude/settings.json`),
   and mirror the rows in `references/security-config.md §1.2
   Team-extensible additions`.

8. **Watermark policy**: `watermark.enabled` defaults to `false`.
   Flip to `true` and set `watermark.text` only after explicit
   approval — and only for animation / showcase exports, not for
   third-party brand work (set
   `watermark.exclude_for_third_party_brand_work: true`).

### Mirror to your internal git host

9. **Mirror.** The reference upstream is at
   `0xmhha/claude-design-skill`. For internal use:

   ```bash
   # 1. Create the empty private repo on your internal git host
   #    (GH Enterprise / GitLab / Bitbucket Server / Gitea / etc.)

   # 2. Add the internal as a second remote — keep origin for
   #    upstream fetches while your team is still tracking changes.
   git remote add internal git@your-internal-host:team/claude-design-skill.git

   # 3. Push every branch + tag once.
   git push internal master
   git push internal --tags

   # 4. Verify the mirror has the same history.
   git ls-remote internal | head -5

   # 5. Tag the divergence point so it's greppable later.
   git tag -a internal-fork-$(date +%F) -m "Forked from upstream 0xmhha/claude-design-skill"
   git push internal internal-fork-$(date +%F)
   ```

   Once your team owns the canonical copy, switch the default
   tracking branch to `internal/master`. Strip any team-specific
   text before any push to a *public* mirror if your team also
   publishes one — the skill ships nothing team-specific by
   default, so the only team-specific values are
   `team-brand-spec.json` (your override) and the
   `approved_asset_hosts.internal` array.

10. **License**: replace `LICENSE` and `NOTICE` if your team needs
    a different licence (internal-only, source-available, another
    open licence). The Apache-2.0 grant in this repo applies only
    to its own commits; downstream forks are free to relicense
    their own modifications under Apache §4(b).

### Port the CI workflow

11. **CI port.** The reference workflow
    `.github/workflows/sanitizers.yml` runs on GitHub Actions; if
    your internal git host uses a different CI system, copy the
    matching snippet from `references/ci-template.md` — it ships
    ready-to-paste templates for **GitLab CI**, **Bitbucket
    Pipelines**, and **Buildkite**, plus translation notes for
    GitHub Enterprise, Jenkins, CircleCI, and Drone. All three
    templates run the identical 6-suite guard chain (93 tests +
    JSON parses + advisory asset scan) — only the wrapping YAML
    syntax differs.

The full Step 4 + Step 5 checklist with current ✓ / ⏳ status lives
in `PROJECT-PLAN.md §6` (split into `(a)` repo-level defaults
shipped, `(b)` default-ships-here · adopter overrides, `(c)`
repo-external operations).

## For security reporters

See `SECURITY.md`. Use GitHub's private security advisories rather
than opening a public issue.

## For PR contributors (rare)

If you do open a PR despite the above:

- The PR must pass `.github/workflows/sanitizers.yml` (93 regression
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
