# Security policy

This repository is a Claude Code design skill that ships supply-chain
gates as load-bearing components — SVG sanitizer, PNG / JPG chunk
scanner, codex-image-import gate, codename-pattern catalog, and a
GitHub Actions workflow that runs all of them on every push and pull
request.

If you find a vulnerability in any of these components, or in the
documentation that describes how they should be used, please report it
privately rather than opening a public issue.

## Reporting a vulnerability

Preferred channel: GitHub's [private security advisories][1] for this
repository (`Security` tab → **Report a vulnerability**). The advisory
form will start a private thread between the reporter and the
maintainer.

[1]: https://github.com/0xmhha/claude-design-skill/security/advisories/new

If GitHub advisories are not available to you, send an email to the
maintainer through the contact information on
<https://github.com/0xmhha>. Use a subject line that begins with
`[claude-design-skill SECURITY]`.

## What to include

A useful report names:

1. The component (sanitizer / scanner / import gate / codename catalog
   / workflow / docs).
2. The exact regression: which input bypasses which gate, or which
   policy in the docs is wrong / out of date.
3. A minimal reproduction (preferably as a unit-test case in the
   format of `scripts/test_*.py` or `scripts/test_*.js`).
4. The repository SHA you tested against.

## Scope

In scope:

- The sanitizer and scanner scripts under `scripts/`
  (`svg-sanitize.py`, `scan_assets.py`, `codex-image-import.py`,
  `init-brand.py`, `easing.js`, and their regression suites).
- The GitHub Actions workflow at `.github/workflows/sanitizers.yml`.
- The codename pattern catalog and the host allowlist in
  `references/security-config.md`.
- The strip-then-scan import flow described in
  `references/codex-design-workflow.md` and
  `references/svg-sanitize.md`.
- The `examples/dot-claude-settings.json` template.

Out of scope:

- Third-party services referenced via the host allowlist (Lucide,
  Phosphor, MDN, Apple HIG, Wikimedia, Met Museum, Artic, Unsplash,
  Pexels, Google Fonts, unpkg / jsdelivr): report directly to those
  vendors.
- Vulnerabilities in `huashu-design` or `alchaincyf/huashu-design`:
  this repository does not derive from those projects (see `LICENSE`
  and `NOTICE` for the clean-room rewrite statement); report there
  separately.
- Fork-specific brand customization (`team-brand-spec.json` real
  values, internal codenames, internal asset hosts): owned by the
  fork operator; report through that fork's channel.

## Disclosure timeline

The maintainer is solo and contributes to this project as internal
R&D. No SLA is offered. As guidance:

- The maintainer aims to acknowledge a report within seven days.
- Fix timing depends on severity. The strip-then-scan gate, the
  codename pattern catalog, and the GitHub Actions workflow have
  hard-fail regression suites that any fix must pass before merging.
- Coordinated public disclosure is welcome; the reporter and the
  maintainer agree the timing in the private advisory thread before
  it goes public.

## What is not a vulnerability

- A reduced-strength regex in `DEFAULT_CODENAME_PATTERNS`. The
  catalog is conservative-pairing by design (see
  `references/security-config.md §1.5`); a "bypass" using a bare
  keyword without the paired noun is the documented trade-off, not
  a defect.
- The `prefers-reduced-motion` fallback in
  `assets/animations.jsx`. The Stage / Sprite engine respects the
  setting; if a deliverable that uses the engine still violates it,
  that is the deliverable's bug, not the engine's.
- Anything in the upstream `alchaincyf/huashu-design` skill. This
  repository does not derive from it.
