# 08 · Buddy Skill Mapping

> **목적**: 14 atomic task 각각에 *어떤 buddy skill (slash command)을 호출해 실행할지* 매핑. 본 plan의 *실행 매뉴얼*.
> **참조**: `/Users/wm-it-22-00661/.claude/plugins/cache/buddy/buddy/1.0.8/skills/router/SKILL.md` 의 9-phase 표.

---

## 1 · buddy 9-phase recap

| Phase | orchestrator | 사용처 |
|---|---|---|
| §1 idea | `concretize-idea` | ✗ (이미 shipped product) |
| §2 features | `define-features` | ✗ |
| §3 design-system | `design-system` | △ ADR 옵션 |
| §4 plan-build | `plan-build` | ✅ (본 문서) |
| §5 build-feature | `build-feature` | ✅ A·C 카테고리 |
| §6 verify-quality | `verify-quality` | ✅ release gate |
| §7 ship-release | `ship-release` | ✅ D 카테고리 |
| §8 iterate-product | `iterate-product` | ✅ A-04 backlog |
| §9 manage-lifecycle | `manage-lifecycle` | ✗ (deprecation 없음) |

크로스-phase 보조: `autoplan`, `consult-codex`, `save-context`, `restore-context`.

## 2 · task별 buddy command 매핑

### D · Release engineering

| task_id | buddy command | 이유 |
|---|---|---|
| **D-01-changelog-split** | `/buddy:ship-release` (Stage: prepare-changelog) | §7 의 release preparation 단계 |
| **D-02-plugin-version-bump** | `/buddy:ship-release` (Stage: version-bump) | 동일 |
| **D-03-doc-version-bump** | `/buddy:ship-release` 또는 직접 W3 작업 | D-01 / D-02 chain의 일부 |
| **D-04-git-tag-push** | `/buddy:ship-release` (Stage: tag) | tag push는 ship-release의 core |
| **D-05-github-release** | `/buddy:ship-release` (Stage: release-notes) | GitHub release publish |
| **D-06-marketplace-ref-pin** | `/buddy:ship-release` 또는 별도 doc PR | doc-only follow-up |

**호출 권장**: D-01 ~ D-05를 하나의 `/buddy:ship-release` 호출에 묶고, D-06은 별도 doc commit.

```
/buddy:ship-release -- "v1.0.0 release: CHANGELOG split, plugin/marketplace version bump, doc bump, git tag, GitHub release"
```

ship-release skill이 *자체 PROCEDURE에서* changelog → version → tag → release 흐름을 가지고 있을 가능성이 큼.

### A · Adopter dogfooding

| task_id | buddy command | 이유 |
|---|---|---|
| **A-01-default-dogfood-spec** | 직접 (skill 활용) | 사용자 + agent 협업. `/buddy:build-feature`는 *implementation* 단계라 fit X. dogfood는 *사용 검증*에 가깝다. |
| **A-02-figma-mcp-smoke** | 동일 | 외부 MCP 환경 작동 검증 |
| **A-03-codex-e2e-smoke** | 동일 | 외부 Codex CLI 작동 검증 |
| **A-04-feedback-backlog** | `/buddy:iterate-product` (Stage: feedback-synthesis) | §8 의 첫 stage. dogfood log → backlog 변환은 iterate-product의 분명한 trigger |

```
# A-04
/buddy:iterate-product -- "dogfood logs at docs/dogfood/01..03 → backlog with P0/P1/P2 priority"
```

### C · Step 8+ enhancement

| task_id | buddy command | 이유 |
|---|---|---|
| **C-01-codex-e2e-script** | `/buddy:build-feature` (TDD loop) | 새 script + test → §5 build-feature 의 정공법 |
| **C-02-figma-mcp-smoke-script** | 동일 | 동일 패턴 |
| **C-03-usage-telemetry-adr** | `/buddy:write-adr` | ADR 표준 양식 + Index 갱신을 자체 처리 |

```
# C-01
/buddy:build-feature -- "scripts/test_codex_e2e.py — Codex CLI conditional smoke + CI step"

# C-03
/buddy:write-adr -- "001 · opt-in usage telemetry: privacy-first, no PII, no codename"
```

### B · Guide coverage check

| task_id | buddy command | 이유 |
|---|---|---|
| **B-00-guide-coverage-check** | 직접 (간단한 checklist 작성) | 매우 작은 작업, orchestrator 호출 비용 > 작업 자체 |

## 3 · 추천 실행 chain

본 plan의 첫 *실행 가능한 명령*. 사용자가 *day-0 release ship*을 진행하려면:

```bash
/buddy:ship-release -- "v1.0.0 release of claude-design-skill: CHANGELOG split (Unreleased → [1.0.0]), bump .claude-plugin/plugin.json + marketplace.json to 1.0.0, doc version bumps (README / HANDOFF / SKILL.md / PROJECT-PLAN.md), git tag v1.0.0, GitHub release create with notes from CHANGELOG [1.0.0]. Reference: docs/plan/03-task-decomposition.md §D, docs/plan/06-acceptance-criteria.md §1."
```

ship-release가 끝나면 *M1 (v1.0.0 ship)* milestone 달성.

이후 dogfood + backlog cycle:

```bash
# 사용자가 dogfood 1~3 시나리오 진행 (수동)
# ↓ 사용자가 docs/dogfood/01..03.md 작성
# ↓
/buddy:iterate-product -- "synthesize feedback from docs/dogfood/01..03 into prioritised backlog. Reference: docs/plan/06-acceptance-criteria.md §2 (A-04)"
```

## 4 · cross-phase 활용

### 4.1 plan 자체의 리뷰

본 plan 문서 9개 작성 완료 후 *4-mode review*:

```bash
/buddy:autoplan -- "docs/plan/00-overview.md ~ docs/plan/08-buddy-skill-mapping.md 의 plan에 대해 review-scope (작업 범위 적정성) + review-engineering (DAG · timeline 현실성) + review-design (audience-aware split의 일관성) + review-devex (executor 친화성)"
```

autoplan은 4 review skill을 sequential dispatch + 결과 합성.

### 4.2 release 결정 시 second opinion

D-04 (git tag push) 직전 *second opinion* 필요 시:

```bash
/buddy:consult-codex -- "v1.0.0 tag push 전 마지막 검토: 108 회귀 테스트 통과 + plugin install 검증 완료 + CHANGELOG split + version bump. 빠진 release-gate 항목이 있나?"
```

### 4.3 세션 간 컨텍스트 이전

plan 실행 중 세션 끊김 시:

```bash
# 세션 끝 직전
/buddy:save-context -- "plan-build executed; D 카테고리 D-01 ~ D-03 완료, D-04 git tag 직전. next: D-04 → D-05 → D-06 → A 카테고리."

# 새 세션 시작
/buddy:restore-context
```

## 5 · 매핑 요약 표

| task_id | primary buddy command | optional support | category |
|---|---|---|---|
| D-01 ~ D-05 | `/buddy:ship-release` | `/buddy:consult-codex` (release 전 final check) | D |
| D-06 | 직접 doc commit | — | D |
| A-01 ~ A-03 | 직접 (사용자 실행) | — | A |
| A-04 | `/buddy:iterate-product` | `/buddy:autoplan` (backlog review) | A |
| B-00 | 직접 checklist 작성 | — | B |
| C-01 ~ C-02 | `/buddy:build-feature` | `/buddy:verify-quality` (CI 통합 후) | C |
| C-03 | `/buddy:write-adr` | `/buddy:consult-codex` (telemetry trade-off) | C |

## 6 · plan-build orchestrator의 자기-종료 기준

본 plan-build invocation 자체는 다음 산출물이 commit되면 *완료*:

- [ ] `docs/plan/00-overview.md` ~ `docs/plan/08-buddy-skill-mapping.md` 9 파일 commit
- [ ] PROJECT-PLAN.md §7에 *plan-build 실행 entry* append
- [ ] CHANGELOG.md `[Unreleased]`에 *Added — docs/plan/ implementation plan* entry
- [ ] 108 회귀 테스트 그대로 통과

이후 *실행 권한은 사용자에게 이전*. 사용자가 `/buddy:ship-release` 호출로 D 카테고리 시작.

## 7 · plan 사용 매뉴얼 (요약)

```
1. docs/plan/00-overview.md 읽기 (5분)
2. docs/plan/08-buddy-skill-mapping.md §3 의 첫 명령 복사
3. /buddy:ship-release 실행 (M1 ship)
4. 사용자가 dogfood (A-01..A-03 중 가능한 시나리오)
5. /buddy:iterate-product 실행 (A-04, M3 backlog)
6. priority 결정에 따라 C 카테고리 진행
```

이 매뉴얼 단계 *6개*가 본 plan의 *외부 인터페이스*.

## 다음 행동

- 본 plan 9 파일 commit + push (plan-build orchestrator 자기-종료)
- 사용자 검토 후 `/buddy:ship-release` 호출 또는 *plan 자체 review* (`/buddy:autoplan`)
