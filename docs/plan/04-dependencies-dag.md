# 04 · Dependencies DAG + Critical Path

> **목적**: `03-task-decomposition.md`의 14개 atomic task 간 의존성을 DAG로 표현. critical path + parallel-safe levels 식별.

---

## DAG (ASCII)

```
                              ┌─────────────────────────────────────┐
                              │  D · Release engineering            │
                              └─────────────────────────────────────┘

           D-01-changelog-split  ┐
                                 ├──► D-03-doc-version-bump ──► D-04-git-tag-push ──► D-05-github-release
           D-02-plugin-version  ─┘                                                 │
                                                                                   └──► D-06-marketplace-ref-pin

           ┌─────────────────────────────────────┐
           │  A · Adopter dogfooding             │   (D 완료 권장 — 강제 아님)
           └─────────────────────────────────────┘

           A-01-default-dogfood-spec  ──┐
           A-02-figma-mcp-smoke        ─┼──► A-04-feedback-backlog
           A-03-codex-e2e-smoke        ─┘

           ┌─────────────────────────────────────┐
           │  C · Step 8+ enhancement            │   (A 결과 학습 후)
           └─────────────────────────────────────┘

           A-02 ──► C-02-figma-mcp-smoke-script
           A-03 ──► C-01-codex-e2e-script
           A-04 ──► C-03-usage-telemetry-adr

           ┌─────────────────────────────────────┐
           │  B · Guide coverage check           │   (독립적, 어디서나 가능)
           └─────────────────────────────────────┘

           B-00-guide-coverage-check  (independent)
```

## edges 명시 list

| from | → | to | edge 유형 |
|---|---|---|---|
| D-01-changelog-split | → | D-03-doc-version-bump | content-flow (CHANGELOG `[1.0.0]` heading이 doc bump의 reference) |
| D-02-plugin-version-bump | → | D-03-doc-version-bump | content-flow (plugin/marketplace `1.0.0`이 doc 명시할 값) |
| D-03-doc-version-bump | → | D-04-git-tag-push | sequence (모든 doc 갱신 commit 후에야 tag 안전) |
| D-04-git-tag-push | → | D-05-github-release | sequence (tag 존재해야 release 생성 가능) |
| D-04-git-tag-push | → | D-06-marketplace-ref-pin | content-flow (`--ref v1.0.0` 안내가 실제 tag 존재 후 의미 있음) |
| A-02-figma-mcp-smoke | → | C-02-figma-mcp-smoke-script | learning (smoke에서 알게 된 마찰점이 자동화 script 설계 입력) |
| A-03-codex-e2e-smoke | → | C-01-codex-e2e-script | learning |
| A-04-feedback-backlog | → | C-03-usage-telemetry-adr | learning (backlog 결과가 telemetry 필요성의 evidence) |
| A-01·A-02·A-03 | → | A-04-feedback-backlog | content-flow (3개 dogfood 결과의 합산) |

independent (의존성 없음): **D-01**, **D-02**, **A-01**, **A-02**, **A-03**, **B-00**.

## critical path

D 카테고리 안에서: `D-01 → D-03 → D-04 → D-05` (4 nodes · 1.1 hours).
A 카테고리는 사용자 시간이 dominant: `A-01 + A-02 + A-03 → A-04` (3.5 hours sequential, 또는 1.5 hours parallel).
전체 critical: `D-01 → D-03 → D-04 → D-05 → A-* → A-04 → C-*`. 합 ≈ 6 hours 직렬, 그러나 A 안에서 병렬화 시 4 hours.

## parallel-safe levels

각 level의 task는 *서로 의존 없음*이라 동시 실행 가능.

| Level | tasks | rationale |
|---|---|---|
| **L0 (시작)** | D-01, D-02, B-00 | 의존성 없음 — 동시 시작 가능 |
| **L1** | D-03 (D-01·D-02 후) | doc bump |
| **L2** | D-04 (D-03 commit 후) | tag push |
| **L3** | D-05, D-06 (D-04 후) | release + marketplace-ref-pin 동시 가능 |
| **L4** | A-01, A-02, A-03 (release 후, 동시 시작) | 3개 dogfood 동시 가능 (다른 사용자 / 다른 환경) |
| **L5** | A-04 | 3개 dogfood 결과 수집 후 |
| **L6** | C-01, C-02, C-03 (각자 learning 입력 ready 후) | 동시 가능 |

## cycle 감지

DAG 위 edge로 cycle 없음. *learning* edge는 모두 단방향 (A → C). *content-flow* edge도 D 내부 + A-04 입력 외 cycle 없음.

## risk + mitigation

| risk | likelihood | mitigation |
|---|---|---|
| D-04 git tag push 후 v1.0.0 의 plugin install이 깨짐 발견 | low | release 전 `claude plugin install --ref v1.0.0` smoke 추가 (선택) |
| A-02 Figma MCP 환경 구축이 실패 | medium | `references/figma-mcp-setup.md`의 fallback path만 검증해도 plan 진행 가능 |
| A-03 Codex CLI 환경 미준비 | medium | A-03 skip 가능 — fixture-based 회귀 테스트로 충분히 cover |
| C-01·C-02 environment-dependent 자동화의 CI flakiness | medium | conditional skip 패턴 (env var 부재 시 exit 0) |

## 다음 문서

- `05-parallel-execution.md` — Level별 worker 분배 + sync points
- `06-acceptance-criteria.md` — task별 *완료 판정* 기준
