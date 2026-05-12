# claude-design-skill — Plan Overview

> **목적**: HANDOFF.md 기준 Step 1–7 shipped 이후의 *남은 작업*을 actor track으로 분해하고, 각 항목에 buddy lifecycle skill을 매핑해 단계별 실행 plan을 수립.
> **작성일**: 2026-05-12
> **트리거**: `/buddy:plan-build` invocation. 4단계 implementation-plan orchestrator의 산출물.
> **참조 문서**: `/HANDOFF.md` §0–§8, `/PROJECT-PLAN.md` §6–§7.

---

## 1 · 한 줄 요약

claude-design-skill은 *visual-only design skill* 자체로는 **Step 1–7 완료** 상태이며, 남은 작업은 (a) adopter dogfooding, (b) per-fork brand integration, (c) Step 8+ optional enhancements 세 갈래로 갈린다. buddy 9-phase lifecycle 중 §5 (Development) · §6 (Quality) · §7 (Release & Beta) · §8 (Operate & Iterate)에 주로 매핑된다.

## 2 · plan 문서 구조

| 문서 | 내용 |
|---|---|
| `00-overview.md` | 이 파일 — 전체 plan map + buddy phase 매핑 |
| `01-current-state.md` | Step 1–7 shipped 상태 snapshot + 검증된 invariant |
| `02-remaining-work-inventory.md` | 남은 작업 raw inventory (4 카테고리 × 13 항목) |
| `03-task-decomposition.md` | 각 항목을 atomic task (single-PR scope)로 분해 |
| `04-dependencies-dag.md` | task 간 의존성 + critical path + parallel-safe levels |
| `05-parallel-execution.md` | track별 worker 분배 + sync points + AI agent 활용 |
| `06-acceptance-criteria.md` | task별 완료 기준 + 검증 방법 (test / lint / smoke) |
| `07-timeline.md` | calendar timeline (best/expected/p90/worst) |
| `08-buddy-skill-mapping.md` | 각 task에 어떤 buddy skill을 호출할지 매핑 |

## 3 · buddy 9-phase 매핑 요약

본 plan은 *기존 product를 운영·확장하는* 단계라 buddy의 §1 (Idea) ~ §4 (Plan)는 이미 통과한 상태로 본다. 활용 phase:

| Phase | 사용 여부 | 적용 task 카테고리 |
|---|---|---|
| §1 concretize-idea | ✗ | — (이미 shipped product) |
| §2 define-features | ✗ | — (feature set 확정) |
| §3 design-system | 부분 | per-fork integration ADR (옵션) |
| §4 plan-build | ✅ **본 문서** | — |
| §5 build-feature | ✅ | adopter dogfooding 피드백 → 코드 수정 |
| §6 verify-quality | ✅ | 회귀 테스트 확장 + Figma MCP end-to-end smoke |
| §7 ship-release | ✅ | semantic version tag (v0.1.0 → v0.2.0) + plugin marketplace 갱신 |
| §8 iterate-product | ✅ | adopter telemetry + 사용 패턴 수집 + 개선 backlog |
| §9 manage-lifecycle | 잠재적 | predecessor fork (huashu-design)의 EOL 결정 시 |

크로스-phase 보조:
- `autoplan` — 모든 plan 단계의 4-mode review (review-scope / engineering / design / devex)
- `consult-codex` — design 의사결정 시 second opinion
- `save-context` / `restore-context` — 세션 간 컨텍스트 이전

## 4 · 남은 작업 4 카테고리

상세는 `02-remaining-work-inventory.md` 참조.

| 카테고리 | 항목 수 | 책임 주체 | buddy phase |
|---|---|---|---|
| **A. Adopter dogfooding** (실 사용 피드백) | 4 | 이 repo 유지보수자 | §5 §6 §8 |
| **B. Per-fork brand integration** (adopter team owns) | 6 | 도입팀 | repo 외부 |
| **C. Step 8+ optional enhancements** | 3 | 이 repo 유지보수자 | §3 §5 §6 §7 |
| **D. Release engineering** | 4 | 이 repo 유지보수자 | §7 §8 |

총 17개 항목, 그 중 11개가 이 repo 내부 작업.

## 5 · 실행 우선순위

| 순서 | 카테고리 | 항목 |
|---|---|---|
| **1** | D · Release | v0.1.0 → v0.2.0 semantic tag + plugin marketplace 갱신 |
| **2** | A · Adopter | first real-world dogfood (사용자 직접 사용 시나리오) |
| **3** | A · Adopter | dogfood 피드백 → 우선순위 backlog로 변환 |
| **4** | C · Enhancement | (선택) Codex CLI end-to-end smoke 자동화 |
| **5** | C · Enhancement | (선택) Figma MCP end-to-end smoke 자동화 |
| **6** | D · Release | telemetry / 사용 추적 mechanism 검토 |

B 카테고리는 adopter team의 결정 영역이므로 본 plan에서 *실행 X*, *guide만 제공* (기존 `CONTRIBUTING.md §For fork operators` 보강).

## 6 · 다음 단계

- `01-current-state.md` 읽기 → 현재 상태 확인
- `02-remaining-work-inventory.md` 읽기 → 작업 raw inventory
- `08-buddy-skill-mapping.md` 읽기 → 어떤 buddy skill을 어떻게 호출할지

본 plan의 첫 실행 행위는 `08-buddy-skill-mapping.md §3 항목 1`의 *release tagging* 부터.

## 7 · 검증 기준 (plan-level)

본 plan 문서 자체가 다음을 만족해야 통과:

- [ ] `docs/plan/00-overview.md` ~ `08-buddy-skill-mapping.md` 모두 존재
- [ ] HANDOFF.md `§Active version`과 동기화
- [ ] PROJECT-PLAN.md §6 (a/b/c) bucket과 일관 (default-ships-here / repo-external / per-fork)
- [ ] 9개 plan 문서 합쳐 ≥ 1500 lines (사용자 요청 *단계별 계획*의 분량 기준)
- [ ] 각 문서 끝에 *다음 문서 / 참조* 라우팅 포함

본 plan-build orchestrator의 산출물로서 commit message는 `docs: docs/plan/ — implementation plan via /buddy:plan-build` 형식.
