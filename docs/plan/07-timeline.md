# 07 · Calendar Timeline

> **목적**: 14 atomic task의 calendar timeline 합성. confidence interval (best/expected/p90/worst) + risk buffer.

---

## 1 · estimation 가정

| 가정 | 값 |
|---|---|
| W1 (maintainer) 가용성 | 0.5 hour/day (외부 일정과 병행) |
| W2 (designer/user) 가용성 | dogfood 1 시나리오당 1 contiguous block (≤ 2 hours) |
| W3 (AI agent) 가용성 | 무제한, *human review*만이 bottleneck |
| W4 (Dependabot) | 자동 — 별도 시간 없음 |
| holiday / 외부 일정 | weekday 가정, 2026-05-13 / 14 평일 |

## 2 · 단계별 단순 estimate

| Level | tasks | hours (parallel-safe) | sequential hours |
|---|---|---|---|
| L0 | D-01, D-02, B-00 | 0.5 | 1.0 |
| L1 | D-03 | 0.3 | 0.3 |
| L2 | D-04 | 0.2 | 0.2 |
| L3 | D-05, D-06 | 0.3 | 0.5 |
| L4 | A-01·A-02·A-03 | 1.5 (3 사용자 환경 동시 시) | 3.5 (1 사용자 sequential) |
| L5 | A-04 | 1.0 | 1.0 |
| L6 | C-01·C-02·C-03 | 5.5 (모두 동시) | 5.5 |

## 3 · scenario별 timeline

### scenario A · best case (parallel + ideal)

| day | task | end-state |
|---|---|---|
| day-0 morning | L0 (D-01·D-02·B-00) → L1 (D-03) → L2 (D-04) → L3 (D-05·D-06) | **v1.0.0 ship** |
| day-0 afternoon | W2가 A-01·A-02·A-03 동시 (3 환경 준비 됨) | dogfood log 3개 ready |
| day-1 morning | A-04 | backlog ready |
| day-1 ~ day-3 | C-01·C-02·C-03 W1 + W3 협업 | enhancement ship |

**best total**: 3 days.

### scenario B · expected case (semi-parallel)

| day | task | end-state |
|---|---|---|
| day-0 | L0 ~ L3 (release ship) | v1.0.0 |
| day-1 ~ day-3 | A-01 (designer 가용 시), A-02 (Figma MCP 환경 준비) | dogfood 부분 진행 |
| day-4 | A-03 (Codex 환경), A-04 합성 | backlog |
| day-5 ~ day-8 | C-01·C-02 (script 작성 + CI 통합) | enhancement |
| day-9 | C-03 (ADR draft) | ADR ready |

**expected total**: 9 days.

### scenario C · p90 (한 환경 미준비)

A-02 또는 A-03 환경 구축에 추가 시간 필요한 경우.

| day | task | end-state |
|---|---|---|
| day-0 | release ship | v1.0.0 |
| day-1 ~ day-2 | A-01 (가능한 dogfood만) | partial backlog |
| day-3 ~ day-7 | A-02 또는 A-03 환경 setup + 진행 | 환경 구축 완료 후 smoke |
| day-8 ~ day-9 | A-04 합성 + 마찰점 분류 | backlog |
| day-10 ~ day-14 | C 카테고리 진행 (우선순위 재산정) | enhancement partial |

**p90 total**: 14 days.

### scenario D · worst case (multiple blockers)

- W2 시간 가용성 < 1 hour/week
- Figma MCP server 호환성 이슈 발견 (A-02 막힘)
- Codex CLI upgrade 필요 (A-03 막힘)

| day | task | end-state |
|---|---|---|
| day-0 | release ship | v1.0.0 |
| week-2 | A-01만 진행 (designer 시간) | partial dogfood |
| week-3 ~ week-4 | A-02 / A-03 환경 협상 + 외부 도움 | environment issues |
| week-5 | A-04 (가능한 마찰점만) | partial backlog |
| month-2 | C 카테고리 진행 여부 재결정 | deferred or partial |

**worst total**: 6 weeks (30 days).

## 4 · timeline matrix

| scenario | release ship | dogfood 결과 | enhancement |
|---|---|---|---|
| **best** | day-0 | day-0 끝 | day-3 |
| **expected** (commit 권장) | day-0 | day-4 | day-9 |
| **p90** | day-0 | day-9 | day-14 |
| **worst** | day-0 | week-5 | month-2 |

**commit 권장 답**: *release(v1.0.0)은 day-0에 끝낸다*. dogfood + enhancement는 expected 9 days, p90 14 days.

## 5 · risk buffer

각 stage에 *15% buffer*:

| stage | base | +15% buffer | 적용 사유 |
|---|---|---|---|
| L0 ~ L3 (release) | 1.3 h | 1.5 h | doc bump 잔재 찾기에 추가 시간 가능성 |
| L4 (dogfood) | 1.5 h (parallel) | 1.7 h | Figma / Codex 환경 이슈 |
| L5 (backlog) | 1.0 h | 1.2 h | 마찰점 분류 미세 조정 |
| L6 (enhancement) | 5.5 h | 6.3 h | script + CI 통합 정밀도 |

## 6 · GA (general availability) 결정 지점

**v1.0.0 = release ship 후 즉시 GA** 권장. 이유:

1. 108 회귀 테스트 + CI green + 사용자 plugin install 검증 완료
2. dogfood 결과는 *v1.1.0 / v1.0.1* 로 후속 ship 가능
3. *조기 release + 빠른 iteration*이 *적은 사용자 풀에서 perfect 추구*보다 가치 큼

dogfood 결과 *critical* 마찰점 발견 시 v1.0.1 hotfix path 별도 마련.

## 7 · milestone marker

| milestone | 시점 | criteria |
|---|---|---|
| **M1 · v1.0.0 ship** | day-0 | D 6 tasks complete, GitHub release published |
| **M2 · first dogfood** | day-0 ~ day-4 | A ≥ 1 시나리오 완료 |
| **M3 · backlog ready** | day-4 ~ day-9 | A-04 완료, P0/P1 마찰점 식별 |
| **M4 · enhancement ship** | day-9 ~ day-14 | C ≥ 1 항목 ship (조건부) |
| **M5 · v1.1.0 (선택)** | week-3 ~ week-4 | P0 마찰점 모두 해결 후 |

## 8 · plan 자체 검증 timeline

본 plan 문서 작성 자체:

| 단계 | 시점 |
|---|---|
| **plan-build orchestrator 호출** | 2026-05-12 (현재 세션) |
| **9개 plan 문서 작성** | 1 hour |
| **commit + push** | 0.2 hours |
| **autoplan 4-mode review** (옵션) | 1 hour |

plan 자체는 *총 2.2 hours*, 단일 세션 내 완료 가능.

## 다음 문서

- `08-buddy-skill-mapping.md` — 각 task에 buddy skill 매핑 (이 plan의 *실행 매뉴얼*)
