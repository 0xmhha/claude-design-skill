# CI template · sanitizer + JSON + asset-scan guards

> The reference workflow ships at `.github/workflows/sanitizers.yml`
> and runs on this repo's GitHub. Use the snippets below as a
> drop-in template for forks that target a different CI platform
> (GitLab, Bitbucket, internal Buildkite, etc.) — copy-paste, do
> not `cp`, the right path depends on the platform.
>
> Local equivalent: `./scripts/install-hooks.sh` activates the
> pre-commit hook that runs the same checks (`.githooks/pre-commit`).

---

## What the CI does

| Job | Severity | What |
|---|---|---|
| SVG sanitizer regression tests | **hard-fail** | `python3 scripts/test_svg_sanitize.py` — 18 tests, regression in policy = block merge |
| `scan_assets` self-tests | **hard-fail** | `python3 scripts/test_scan_assets.py` — 13 tests, sanity-checks the scanner against synthetic adversarial input |
| Codex-image-import gate tests | **hard-fail** | `python3 scripts/test_codex_image_import.py` — 19 tests, including the conservative-pairing codename catalog |
| Animations easing regression tests | **hard-fail** | `node scripts/test_animations_easing.js` — 19 tests, asserts every easing curve is `0→0`, `1→1`, monotonic ordering, frozen pack |
| `init-brand` bootstrap helper tests | **hard-fail** | `python3 scripts/test_init_brand.py` — 11 tests for the cp + meta-strip + JSON-validate contract + color-token-groups invariant + status-source attribution survival |
| `figma-to-brand-spec` extractor tests | **hard-fail** | `python3 scripts/test_figma_to_brand_spec.py` — 13 tests covering colour + text mapping, hex rounding, unmapped-style preservation, merge / no-merge, all error paths (fixture-based, network-free) |
| `figma-viewer` tests | **hard-fail** | `python3 scripts/test_figma_viewer.py` — 15 tests for the HTML viewer (well-formed doctype + title, every CANVAS becomes a section, RGBA + corner radius rendering, font escape against hostile fontFamily, self-containment invariant, all error paths, empty document, unsupported node placeholder) |
| JSON template lint | **hard-fail** | `examples/dot-claude-settings.json` + `assets/team-brand-spec.default.json` parse cleanly |
| Asset scan | **advisory** | `python3 scripts/scan_assets.py --dir assets/ --advisory` — reports without blocking |

Promote the asset scan from advisory to hard-fail (drop `--advisory`) once the catalog is clean.

---

## GitHub Actions (`.github/workflows/sanitizers.yml`)

This repo ships the workflow at `.github/workflows/sanitizers.yml`.
The reference body:

```yaml
name: sanitizers

on:
  push:
    branches: [master, main]
  pull_request:

permissions:
  contents: read

jobs:
  guards:
    name: Sanitizer / JSON / asset-scan / easing guards
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"
      - uses: actions/setup-node@v4
        with:
          node-version: "22"

      - name: SVG sanitizer regression tests
        run: python3 scripts/test_svg_sanitize.py

      - name: scan_assets self-check
        run: python3 scripts/test_scan_assets.py

      - name: codex-image-import gate tests
        run: python3 scripts/test_codex_image_import.py

      - name: Animations easing regression tests
        run: node scripts/test_animations_easing.js

      - name: init-brand bootstrap helper tests
        run: python3 scripts/test_init_brand.py

      - name: JSON template lint
        run: |
          python3 -c "import json; json.load(open('examples/dot-claude-settings.json'))"
          python3 -c "import json; json.load(open('assets/team-brand-spec.default.json'))"

      - name: Image asset scan (advisory)
        run: python3 scripts/scan_assets.py --dir assets/ --advisory
```

Notes:
- `permissions: contents: read` keeps the workflow from being able to push back into the repo. This is the secure default.
- No untrusted input (PR titles, commit messages, branch refs) is interpolated into `run:` steps — workflow is injection-safe.
- Pinned major versions (`@v4`, `@v5`); pin to specific commit SHAs if your security policy requires it.
- Node 22 matches the maintainer's local runtime (`nvm` v22.16.0 verified 2026-05-10).

---

## GitLab CI (`.gitlab-ci.yml`)

```yaml
default:
  image: python:3.10

stages: [test]

variables:
  PIP_DISABLE_PIP_VERSION_CHECK: "1"

guards:
  stage: test
  before_script:
    - apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
    - curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
    - apt-get install -y nodejs
    - node --version && python3 --version
  script:
    - python3 scripts/test_svg_sanitize.py
    - python3 scripts/test_scan_assets.py
    - python3 scripts/test_codex_image_import.py
    - node    scripts/test_animations_easing.js
    - python3 scripts/test_init_brand.py
    - python3 scripts/test_figma_to_brand_spec.py
    - python3 scripts/test_figma_viewer.py
    - python3 -c "import json; json.load(open('examples/dot-claude-settings.json'))"
    - python3 -c "import json; json.load(open('assets/team-brand-spec.default.json'))"
    - python3 scripts/scan_assets.py --dir assets/ --advisory
  rules:
    - if: $CI_PIPELINE_SOURCE == "push"
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

---

## Bitbucket Pipelines (`bitbucket-pipelines.yml`)

```yaml
image: python:3.10

definitions:
  steps:
    - step: &guards
        name: Sanitizer / JSON / asset-scan / easing / init-brand / figma-extractor
        caches:
          - pip
        script:
          # Node 22 for the easing regression suite
          - apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
          - curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
          - apt-get install -y nodejs
          # Guard chain (mirrors .github/workflows/sanitizers.yml)
          - python3 scripts/test_svg_sanitize.py
          - python3 scripts/test_scan_assets.py
          - python3 scripts/test_codex_image_import.py
          - node    scripts/test_animations_easing.js
          - python3 scripts/test_init_brand.py
          - python3 scripts/test_figma_to_brand_spec.py
          - python3 scripts/test_figma_viewer.py
          - python3 -c "import json; json.load(open('examples/dot-claude-settings.json'))"
          - python3 -c "import json; json.load(open('assets/team-brand-spec.default.json'))"
          - python3 scripts/scan_assets.py --dir assets/ --advisory

pipelines:
  default:
    - step: *guards
  pull-requests:
    "**":
      - step: *guards
```

---

## Buildkite (`.buildkite/pipeline.yml`)

```yaml
steps:
  - label: ":lock: Sanitizer guards"
    plugins:
      - docker#v5.11.0:
          image: "python:3.10"
          shell: ["/bin/bash", "-e", "-c"]
    command: |
      apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
      curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
      apt-get install -y nodejs
      python3 scripts/test_svg_sanitize.py
      python3 scripts/test_scan_assets.py
      python3 scripts/test_codex_image_import.py
      node    scripts/test_animations_easing.js
      python3 scripts/test_init_brand.py
      python3 scripts/test_figma_to_brand_spec.py
      python3 scripts/test_figma_viewer.py
      python3 -c "import json; json.load(open('examples/dot-claude-settings.json'))"
      python3 -c "import json; json.load(open('assets/team-brand-spec.default.json'))"
      python3 scripts/scan_assets.py --dir assets/ --advisory
```

---

## Translation notes

All three pipelines run the **identical 6-suite guard chain** (93 tests + 2 JSON parses + 1 advisory scan). The shell commands never differ between hosts; only the surrounding YAML syntax does. The guards are stdlib-only — they need *only* Python 3.10+ and Node 22+, no `pip install` step, no `npm install` step.

**GitHub Enterprise**: identical to `.github/workflows/sanitizers.yml`; the workflow runs on self-hosted runners or GitHub-hosted runners with no change.

**Jenkins**: wrap the same shell block in a `pipeline { stages { stage('guards') { steps { sh '...' } } } }` `Jenkinsfile` declarative pipeline. Use the `python3.10` Docker agent image.

**CircleCI / Drone / Other**: same shell commands, same exit-code semantics (non-zero on any failure). Translate the wrapping YAML to the host's syntax.

When porting:

1. **Pin tool versions**: Python `3.10`, Node `22`. The guards work on newer versions but pin so the audit trail is reproducible.
2. **Hard-fail on test exit codes**: every test script exits non-zero on failure; do not wrap them in `|| true` or similar.
3. **Asset scan stays advisory** until your catalog is curated; flip to hard-fail (drop `--advisory`) once you control every PNG / SVG in `assets/`.
4. **Codex CLI integration is out of scope for CI**: `scripts/codex-image-import.py` is run locally during PNG ingestion, not in the CI pipeline.

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
