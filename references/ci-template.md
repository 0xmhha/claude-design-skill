# CI template · sanitizer + JSON + asset-scan guards

> Drop-in template for GitHub Actions, GitLab CI, or any platform. **Copy-paste**, don't `cp` — the right path depends on which CI platform your team uses.
>
> Why a template instead of a committed workflow: this fork stays platform-agnostic until the team commits to a CI host. See `PROJECT-PLAN.md` Phase 5 §5.3.

---

## What the CI does

| Job | Severity | What |
|---|---|---|
| SVG sanitizer regression tests | **hard-fail** | `python3 scripts/test_svg_sanitize.py` — 16 tests, regression in policy = block merge |
| JSON template lint | **hard-fail** | `examples/dot-claude-settings.json` + `assets/team-brand-spec.example.json` parse cleanly |
| Asset scan | **advisory** | `python3 scripts/scan_assets.py --dir assets/ --advisory` — reports without blocking |
| `scan_assets` self-tests | **hard-fail** | `python3 scripts/test_scan_assets.py` — sanity-checks the scanner against synthetic adversarial input |

Promote the asset scan from advisory to hard-fail (drop `--advisory`) once the catalog is clean.

---

## GitHub Actions (`.github/workflows/ci.yml`)

```yaml
name: CI

on:
  push:
    branches: [master, main]
  pull_request:

permissions:
  contents: read

jobs:
  guards:
    name: Sanitizer + JSON + asset-scan guards
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: SVG sanitizer regression tests
        run: python3 scripts/test_svg_sanitize.py

      - name: JSON template lint
        run: |
          python3 -c "import json; json.load(open('examples/dot-claude-settings.json'))"
          python3 -c "import json; json.load(open('assets/team-brand-spec.example.json'))"

      - name: Image asset scan (advisory)
        run: python3 scripts/scan_assets.py --dir assets/ --advisory

      - name: scan_assets self-check
        run: python3 scripts/test_scan_assets.py
```

Notes:
- `permissions: contents: read` keeps the workflow from being able to push back into the repo. This is the secure default.
- No untrusted input (PR titles, commit messages, branch refs) is interpolated into `run:` steps — workflow is injection-safe.
- The workflow uses pinned major versions (`@v4`, `@v5`); pin to specific SHAs if your security policy requires it.

To activate:

```bash
mkdir -p .github/workflows
$EDITOR .github/workflows/ci.yml   # paste the YAML above
git add .github/workflows/ci.yml
```

---

## GitLab CI (`.gitlab-ci.yml`)

```yaml
default:
  image: python:3.10

stages: [test]

guards:
  stage: test
  script:
    - python3 scripts/test_svg_sanitize.py
    - python3 -c "import json; json.load(open('examples/dot-claude-settings.json'))"
    - python3 -c "import json; json.load(open('assets/team-brand-spec.example.json'))"
    - python3 scripts/scan_assets.py --dir assets/ --advisory
    - python3 scripts/test_scan_assets.py
  rules:
    - if: $CI_PIPELINE_SOURCE == "push"
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

---

## Internal GH Enterprise / Bitbucket / Buildkite

The guards are stdlib-Python only — they run on any container with Python 3.10+. Translate the four steps to your CI's native syntax. The shell commands are identical.

---

## Local equivalent (without CI)

The same checks run locally as the pre-commit hook — see `.githooks/pre-commit` and `scripts/install-hooks.sh`. Activate with:

```bash
./scripts/install-hooks.sh
```

---

## Failure-mode reference

| Symptom | What broke | Fix |
|---|---|---|
| `test_svg_sanitize.py` exits non-zero | A change to `scripts/svg-sanitize.py` weakened policy | Inspect failed test class — if the change is intentional, update the test, never the rule |
| JSON template lint fails | Trailing comma, smart quotes, or unclosed brace in a template | Open in `$EDITOR` and re-validate with `python3 -c "import json; json.load(open(...))"` |
| `scan_assets --advisory` reports CRITICAL | Asset has trailing bytes after `IEND` / `EOI`, or a non-whitelist chunk | Re-export from source, or pipe through `optipng` / `jpegtran -optimize` |
| `test_scan_assets.py` exits non-zero | Synthetic adversarial input no longer trips the scanner | Regression in `scripts/scan_assets.py` policy — investigate before merging |

---

## Related

- `scripts/svg-sanitize.py` — sanitizer
- `scripts/scan_assets.py` — image scanner
- `scripts/test_svg_sanitize.py` — sanitizer regression tests
- `scripts/test_scan_assets.py` — scanner sanity tests
- `.githooks/pre-commit` — local equivalent
- `PROJECT-PLAN.md` Phase 5 §5.3 — note about retargeting CI to internal host
