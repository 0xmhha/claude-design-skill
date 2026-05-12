# 05 · Parallel Execution Plan

> **목적**: `04-dependencies-dag.md`의 parallel-safe levels를 worker별로 배분 + sync points 명시.

---

## 1 · worker capability matrix

| Worker | 역할 | 가능 작업 종류 |
|---|---|---|
| **W1 · maintainer (human)** | release engineering, doc 갱신, code change | 모든 D / C 작업, A-04 합성 |
| **W2 · designer / user** | dogfood 실행 | A-01 (디자인 작업), A-02 (Figma 환경), A-03 (Codex 환경) |
| **W3 · AI agent (Claude Code)** | doc 작성, manifest 갱신, commit drafting | D-01·D-02·D-03·D-06 보조, B-00 작성, ADR 초안 |
| **W4 · Dependabot / GitHub** | 자동 PR (action bumps), security advisories | 별도 작업 — 의존 없음 |

## 2 · Level별 batch schedule

| Level | tasks | suggested worker | duration |
|---|---|---|---|
| **L0** | D-01, D-02, B-00 | W1 + W3 (W3가 draft → W1 review) | 0.5 h (parallel) |
| **L1** | D-03 | W1 + W3 | 0.3 h |
| **L2** | D-04 | W1 only (git tag push는 human approval) | 0.2 h |
| **L3** | D-05, D-06 | W1 (D-05) + W3 (D-06 doc) | 0.3 h (parallel) |
| **L4** | A-01, A-02, A-03 | W2 (사용자가 1~3 시나리오 실행) | 1.5 h (parallel — 세 환경) |
| **L5** | A-04 | W1 (피드백 합성) | 1.0 h |
| **L6** | C-01, C-02, C-03 | W1 (script) + W3 (ADR draft) | 5.5 h (parallel) |

총 critical-path duration: **L0 → L5 = 3.8 hours** (W2 dependence). L6 optional이라 *release ship*은 L5 시점 가능.

## 3 · sync points

| Sync # | after | before | 누가 확인 |
|---|---|---|---|
| **S1** | D-03 commit | D-04 tag push | W1: `git status` clean + `git log --oneline -1` 확인 |
| **S2** | D-04 + D-05 | A-01·A-02·A-03 시작 | W1 → W2: "v1.0.0 ship, dogfood 시작 OK" 통지 |
| **S3** | A-01·A-02·A-03 모두 끝 | A-04 시작 | W2 → W1: dogfood log 3개 share |
| **S4** | A-04 결과 | C-01·C-02·C-03 진행 여부 결정 | W1: backlog 검토 후 priority 결정 |

## 4 · AI agent (W3) 활용 패턴

### 4.1 doc 작성 → human review

W3가 다음 doc/commit drafts를 작성:
- D-01: CHANGELOG `[Unreleased]` → `[1.0.0]` 분할 draft (heading + 날짜만)
- D-03: README / HANDOFF / SKILL.md / PROJECT-PLAN의 `1.0.0` 갱신 (find-replace 패턴)
- D-06: QUICKSTART + figma-mcp-setup에 `--ref v1.0.0` 안내 삽입
- B-00: 6 guide 항목 각각 *어디서 안내되는지* checklist 작성
- C-03: telemetry ADR 초안 (status: proposed)

W3의 출력은 *모두 git diff* 형태로 W1이 review → merge.

### 4.2 script 작성 → human integration

C-01·C-02는 W3가 script + tests 초안 작성, W1이 CI workflow 통합 + 검증.

### 4.3 dogfood log 합성 (A-04)

W2가 3개 dogfood log를 markdown으로 제공하면 W3가 *마찰점 추출 + GitHub Issue draft*. W1이 *우선순위 결정* + Issue 생성.

## 5 · bottleneck mitigation

| bottleneck | mitigation |
|---|---|
| W2 (사용자) 시간 가용성 | A-01·A-02·A-03 *어느 하나만이라도* 실행해 A-04로 진입 가능. 3개 다 기다리지 않음. |
| Figma MCP server 환경 구축 | A-02 skip → MCP-absent fallback path만 검증. C-02도 같이 deferred. |
| Codex CLI 환경 미준비 | A-03 skip → fixture-based 회귀 (19 tests)로 충분. C-01도 deferred. |
| GitHub release notes 작성 | W3가 `awk '/## \[1.0.0\]/,/## \[/'`로 CHANGELOG에서 자동 추출 |

## 6 · 권장 실행 순서 (단일 calendar day)

```
day-0 (release)
  09:00 — L0 시작 (D-01, D-02, B-00 병렬)
  09:30 — L1 (D-03) commit
  09:45 — L2 (D-04) tag push
  10:00 — L3 (D-05 + D-06)
  10:30 — release 검증 + 사용자에게 dogfood 진입 안내
  
day-1+ (dogfood, 사용자 시간에 맞춰)
  사용자가 A-01·A-02·A-03 중 가능한 시나리오 실행
  
day-2+ (enhancement, 선택)
  W1이 A-04 합성 + C-* 우선순위 결정
```

본 plan은 **day-0 끝 (release ship)이 첫 milestone**. 그 이후는 사용자 인풋에 의존.

## 다음 문서

- `06-acceptance-criteria.md` — task별 *완료 판정* 기준
- `07-timeline.md` — calendar timeline (best/expected/p90/worst)
