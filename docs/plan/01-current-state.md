# 01 · Current State Snapshot

> **목적**: Step 1–7 shipped 상태를 단일 문서로 요약. plan의 모든 의사결정이 이 snapshot 위에 위치.
> **마지막 검증**: 2026-05-12 · 108 회귀 테스트 · CI success · master fast-forward sync.

---

## 1 · Step별 ship 결과

| Step | 시점 | 핵심 산출물 | 검증 |
|---|---|---|---|
| **1 — Skeleton** | 2026-05-09 | 23 carry-over + 6 fresh files | clean tree |
| **2 — SKILL.md body** | 2026-05-09 → 05-10 | 6 sections (Junior Designer / Anti-AI-slop / App prototype / Slide deck / Tweaks / Critique) | 시각 smoke 통과 |
| **3 — Design knowledge** | 2026-05-10 | design-styles.md (18) + scene-templates.md (9) + animation engine + best-practices + 16 showcases | 19 easing tests + asset scan clean |
| **4 — Internal-fit hardening** | 2026-05-10 | codename catalog + GitHub Actions CI + asset host allowlist | 19/19 codename tests |
| **5 — Operational defaults + Figma ingestion** | 2026-05-11 | web3-game-style-stats + team-brand-spec.default.json + figma-to-brand-spec.py + Default Studio identity + 4 SVG placeholders | 13 figma-extractor tests |
| **6 — Figma support hardening** | 2026-05-12 | figma-viewer.py + figma-mcp-setup.md + figma-image-export.md + figma-page-organization.md | 15 viewer tests, 108 total |
| **7 — Onboarding + plugin install** | 2026-05-12 | QUICKSTART.md + .claude-plugin/plugin.json + marketplace.json | adopter install 검증 (사용자 측 통과) |

후속 follow-ups (post-Step 단위 commits):
- Step 5.5 — Default Studio identity (§6 restructure)
- Step 5.6 — §6 (c) guides shipped (mirror recipe + non-GitHub CI templates)
- post-Step-7 — plugin install schema fixes (source string → url object → HTTPS URL → repository string)
- CI bump — Dependabot PR #1 merged (actions/* @v4/v5 → v6)
- ci-template sync — references/ci-template.md snippet 갱신 (v4/v5 → v6)

## 2 · Code surface

### Scripts (10 files, stdlib only)

| 스크립트 | 줄 수 (≈) | tests |
|---|---|---|
| `scripts/svg-sanitize.py` | 350 | `test_svg_sanitize.py` 18 |
| `scripts/scan_assets.py` | 280 | `test_scan_assets.py` 13 |
| `scripts/codex-image-import.py` | 470 | `test_codex_image_import.py` 19 |
| `scripts/test_animations_easing.js` | 200 | (자체 19 tests) |
| `scripts/init-brand.py` | 150 | `test_init_brand.py` 11 |
| `scripts/figma-to-brand-spec.py` | 280 | `test_figma_to_brand_spec.py` 13 |
| `scripts/figma-viewer.py` | 360 | `test_figma_viewer.py` 15 |
| `scripts/install-hooks.sh` | 60 | (smoke) |

**총 회귀 테스트: 18 + 13 + 19 + 19 + 11 + 13 + 15 = 108**.

### Assets

| Asset | 형식 | 용도 |
|---|---|---|
| `assets/team-brand-spec.default.json` | JSON | Default Studio identity + Step 5.2 evidence-anchored tokens |
| `assets/ios_frame.jsx`, `android_frame.jsx` | React JSX | device frame wrappers |
| `assets/deck_stage.js`, `tweaks.js`, `animations.jsx`, `easing.js` | JS / JSX | runtime components |
| `assets/default-brand/{logo,logo-white,wordmark,icon}.svg` | SVG | Default Studio placeholder marks (sanitiser-clean) |
| `assets/showcase-brand/generated/*.png` (16) | PNG | prebuilt visual demos (Codex CLI + gpt-image-2) |
| `assets/showcase-brand/PROVENANCE.md`, `README.md` | Markdown | 16 PNG 감사 추적 + 페이지별 preview catalog |

### References (17 files)

- 보안 / sanitiser: `security-config.md`, `svg-sanitize.md`, `production-boundaries.md`
- Figma 워크플로 (6): `figma-workflow.md`, `figma-selection-aware.md`, `figma-layer-naming.md`, `figma-component-grouping.md`, `figma-brand-spec-import.md`, `figma-to-brand-spec.md`, `figma-viewer.md`, `figma-mcp-setup.md`, `figma-image-export.md`, `figma-page-organization.md`
- Brand / 디자인 카탈로그: `brand-spec-fields.md`, `design-styles.md` (18), `scene-templates.md` (9), `web3-game-style-stats.md`
- Animation: `animation-engine.md`, `animation-best-practices.md`, `animation-pitfalls.md`
- CI / Codex: `ci-template.md`, `codex-design-workflow.md`

### Top-level docs

- `README.md`, `HANDOFF.md`, `QUICKSTART.md`, `SKILL.md`, `PROJECT-PLAN.md`, `CHANGELOG.md`
- `LICENSE` (Apache-2.0), `NOTICE` (§4.d), `SECURITY.md`, `CONTRIBUTING.md`
- `.github/workflows/sanitizers.yml`, `.github/dependabot.yml`
- `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`

## 3 · 검증된 invariants (변경 시 깨지면 안 되는 조건)

| Invariant | 검증 위치 |
|---|---|
| 108 회귀 테스트 모두 OK | `.github/workflows/sanitizers.yml` + 로컬 7-suite |
| 6 JSON 파일 valid (`settings`, `brand-spec.default`, 2 fixtures, plugin manifest, marketplace) | CI JSON lint step |
| 16 showcase PNG `scan_assets` clean | CI advisory scan |
| 4 placeholder SVG `svg-sanitize` clean | 수동 검증 (Step 5.5) |
| `colors.accent.primary == "#5B7CFA"` (Default Studio identity) | `test_init_brand.py` 핀 |
| `colors.status._source` Uniswap Spore attribution survives meta-strip | `test_init_brand.py` 핀 |
| Figma viewer 출력은 self-contained (`<link>` / `<script src>` / `@import` 부재) | `test_figma_viewer.py` 핀 |
| Figma viewer `fontFamily` HTML-escape (hostile `<script>` payload 차단) | `test_figma_viewer.py` 핀 |
| Codex PNG `caBX` C2PA chunk 제거 후에만 import | `test_codex_image_import.py` 19 tests |
| codename conservative-pairing rule (`v\d+` 단독은 통과, phase keyword와 결합 시 차단) | `test_codex_image_import.py` 핀 |
| 모든 commit에 Co-Authored-By trailer 없음 | git log 검사 |

## 4 · Plugin install 검증 (2026-05-12 사용자 측)

| 단계 | 결과 |
|---|---|
| `claude plugin marketplace add 0xmhha/claude-design-skill` | ✅ |
| `claude plugin install claude-design-skill` | ✅ (post `source: "url" + repository: string` 패치 후) |
| `claude plugin list` 출력 | claude-design-skill enabled |
| Claude Code 안에서 skill body 인식 | ✅ (Three load-bearing security rules 응답) |

이로써 *멀티유저가 한 줄로 설치* 가능한 plugin path가 *실제 사용자 환경에서* 검증됨.

## 5 · CI 상태

- 최신 master commit: `1702237 docs: sync ci-template snippet to actions/*@v6 (post-#1 bump)`
- CI run history (최근 5): 모두 SUCCESS, 평균 20–30초
- Dependabot active (weekly Monday 09:00 KST, max 3 open PRs, grouped `actions/*`)

## 6 · 다음 문서

- `02-remaining-work-inventory.md` — 남은 작업 4 카테고리 raw 리스트
- `08-buddy-skill-mapping.md` — 각 task에 buddy skill 매핑
