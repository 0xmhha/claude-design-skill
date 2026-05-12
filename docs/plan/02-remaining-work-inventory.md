# 02 · Remaining Work Inventory

> **목적**: Step 1–7 shipped 이후 남은 작업의 raw inventory. 의존성·우선순위·실행 plan은 후속 문서에서 다룬다.
> **분류**: 4 카테고리 × 17 항목.
> **출처**: HANDOFF.md §0 `What's intentionally NOT done`, PROJECT-PLAN.md §6 (b)·(c), 본 세션 누적 결정.

---

## 카테고리 A · Adopter dogfooding (4 항목)

이 repo 유지보수자가 *실제 사용자의 사용 시나리오*를 추적·반영하는 영역. 새 코드보다 *피드백 수집 + 우선순위화*에 가깝다.

| ID | 항목 | 트리거 |
|---|---|---|
| A-1 | first real-world dogfood — Default Studio identity로 시안 1건 작성 끝-내기 (Junior Designer 4-stage workflow 적용) | 사용자 직접 진행 |
| A-2 | Figma MCP end-to-end smoke — server attached 상태에서 `figma_get_selection` → rename → componentize 1 cycle | Figma MCP 등록 후 |
| A-3 | Codex CLI end-to-end smoke — Default Studio brand로 hero 이미지 1건 생성 + strip-then-scan + Figma 배치 (또는 manual fallback) | Codex CLI 환경 |
| A-4 | 사용자 피드백 → backlog 변환 — 위 3개 smoke의 마찰점을 GitHub Issues 또는 PROJECT-PLAN §7에 entry로 기록 | A-1 ~ A-3 후 |

## 카테고리 B · Per-fork brand integration (6 항목, adopter team owns)

PROJECT-PLAN.md §6 (b)·(c)와 일치. **이 repo가 *guide만* 제공하고 *실행은 도입팀이*** 하는 영역. 본 plan은 *진행 X*, *현재 guide의 충분성만 검증*.

| ID | 항목 | guide 위치 | 검증 |
|---|---|---|---|
| B-1 | `team-brand-spec.json` 실제 값 stamp | `scripts/init-brand.py` + `QUICKSTART.md §4` | adopter 측 |
| B-2 | 내부 codename namespace 추가 | `scripts/codex-image-import.py:DEFAULT_CODENAME_PATTERNS` + `references/security-config.md §1.5` | adopter 측 |
| B-3 | `watermark.enabled` 정책 결정 | `references/brand-spec-fields.md §watermark` (default off) | adopter 측 |
| B-4 | 내부 asset host allowlist 추가 | `examples/dot-claude-settings.json:permissions.ask` + `security-config.md §1.2` | adopter 측 |
| B-5 | 내부 git host로 mirror | `CONTRIBUTING.md §For fork operators §9` (5단계 bash recipe) | adopter 측 |
| B-6 | 비-GitHub CI host로 워크플로 포팅 | `references/ci-template.md` (GitLab CI / Bitbucket Pipelines / Buildkite snippet + Jenkins / CircleCI / Drone notes) | adopter 측 |

이 6 항목 모두 *현재 guide만 점검*하면 plan-level 처리 완료.

## 카테고리 C · Step 8+ optional enhancements (3 항목)

기능적 빠진 부분은 없지만 *adopter 마찰을 더 줄이는* 옵션. 사용자 우선순위 결정 후 진행.

| ID | 항목 | 효과 |
|---|---|---|
| C-1 | Codex CLI end-to-end smoke 자동화 — `scripts/test_codex_e2e.py` 또는 CI 별도 job (codex 환경 필요 시 conditional) | 회귀 자동 검출 |
| C-2 | Figma MCP end-to-end smoke 자동화 — fixture-based이 아닌 *실제 MCP server* 호출 smoke (CI에서는 skip, local dev 옵션) | MCP setup 변경 빠른 감지 |
| C-3 | telemetry / usage tracking — opt-in으로 plugin install 후 어떤 skill section이 가장 자주 조회되는지 (privacy-first 설계 필요) | 사용 패턴 데이터 |

이 항목들은 *현재 매우 우선순위 낮음*. 본 plan은 C-1·C-2만 *후보로 등록*, C-3는 *별도 ADR 필요 deferred*.

## 카테고리 D · Release engineering (4 항목)

product 자체의 *공식 release 흐름* 정립.

| ID | 항목 | 효과 |
|---|---|---|
| D-1 | semantic version tag — v0.1.0 (Step 1) → v0.2.0 (Step 5 promotion) 또는 v1.0.0 (Step 7 stable) | adopter가 `claude plugin marketplace add` 시 `ref: v1.0.0` 형식으로 핀 가능 |
| D-2 | CHANGELOG.md `[Unreleased]` → `[1.0.0]` 분할 + Unreleased는 새 작업용 비우기 | release 시점 명확화 |
| D-3 | `.claude-plugin/plugin.json` 안의 `version` 필드 갱신 (`0.1.0` → `1.0.0`) + marketplace.json 동기화 | plugin install 시 version mismatch 방지 |
| D-4 | GitHub release 자동 생성 (`gh release create`) + release notes (CHANGELOG에서 추출) | adopter UX 향상 |

## 카테고리별 우선순위 매트릭스

| 카테고리 | 우선순위 | 비고 |
|---|---|---|
| **D · Release engineering** | **1** | release tag가 있어야 마음 편히 dogfood. plugin install이 `master`에 고정되어 있어 release 안 끊으면 모든 commit이 사용자에게 즉시 노출 |
| **A · Adopter dogfooding** | **2** | release 후 사용 시나리오. 마찰점 발견 = 실제 가치 |
| **C · Step 8+ enhancement** | **3** | C-1 / C-2는 dogfood 결과에 따라 우선순위 재산정 |
| **B · Per-fork brand integration** | **4** | *이 repo가 손대지 않음*. guide 충분성만 검증 (B-checklist 별도) |

## raw 우선순위 1~10

| # | ID | 작업 | 카테고리 |
|---|---|---|---|
| 1 | D-2 | CHANGELOG `[Unreleased]` → `[1.0.0]` 분할 | D |
| 2 | D-3 | plugin.json + marketplace.json `version: "1.0.0"` 갱신 | D |
| 3 | D-1 | git tag v1.0.0 + push | D |
| 4 | D-4 | GitHub release 생성 + notes | D |
| 5 | A-1 | first real-world dogfood (Default Studio identity) | A |
| 6 | A-2 | Figma MCP end-to-end smoke | A |
| 7 | A-3 | Codex CLI end-to-end smoke | A |
| 8 | A-4 | dogfood 피드백 → backlog 변환 | A |
| 9 | C-1 | Codex CLI smoke 자동화 (조건부) | C |
| 10 | C-2 | Figma MCP smoke 자동화 (조건부) | C |

11번 이후는 dogfood 결과에 따라 결정.

## 다음 문서

- `03-task-decomposition.md` — 위 10개 항목을 atomic task로 분해
- `08-buddy-skill-mapping.md` — 각 task에 어떤 buddy skill 호출할지
