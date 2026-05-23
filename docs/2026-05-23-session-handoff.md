# Session Handoff — AI-Figma Context Binding Bridge

Date: 2026-05-23
Purpose: 이전 세션(5/21)의 전체 컨텍스트를 새 세션에서 이어서 작업할 수 있도록 정리

---

## 1. 프로젝트 개요

**AI-Figma Context Binding Bridge** — AI가 생성한 디자인을 Figma에 자동 적용할 때 발생하는 마찰(layer naming, context binding, session state)을 해소하는 도구.

**North Star**: AI가 생성한 디자인을 사람이 했는지 AI가 했는지 구분 불가능한 수준으로 끌어올리는 것. 측정 = blind test pass rate → 50% convergence.

**Wedge (P3 reframed)**: Figma 공식 MCP 위에 "3 piece thin wrapper"
1. **Session-state cache** — 5min TTL + explicit reset + scan-on-restart
2. **Collision detector** — page-level granularity (다른 페이지 작업 = 정상)
3. **Globally-unique naming enforcement** — `<page>__<section>__<element>__<variant>`

**접근 방식**: A→B sequence. A = layer naming wrapper (3-5일). B = context binding sub-platform (2-4주). C = design intent language (6-12개월, month-6 gate).

---

## 2. 완료된 작업 (이전 세션)

| # | 작업 | 상태 | 산출물 |
|---|------|------|--------|
| 1 | **autoplan** (4-phase) | ✓ APPROVED | `docs/2026-05-20-validate-idea-ai-figma-context-bridge.md` 내 annotation + 46-row decision audit trail |
| 2 | **validate-advanced-edge-idea** (Stage 2 grilling) | ✓ 완료 | 동 문서 내 D5/D2/D3 findings, 6 boxed edge cases, 7 assumption ledger entries |
| 3 | **PRE-02 spike** (Figma MCP inventory) | ✓ 완료 | `docs/2026-05-21-figma-mcp-inventory.md` — Plan A 확정, Plan B priority ↓↓ |
| 4 | **PRE-01 preparation** | ✓ prep 완료 | `docs/2026-05-21-pre01-prep.md` — 4 components (discussion guide, observation setup, paper mockup, U-01/U-02 cheat sheet) + expected outcomes |
| 5 | **PII 익명화** | ✓ 완료 | 모든 문서 "세민" → "Anchor-A", 회사 정보 일반화. `.gitignore`에 backup 디렉토리 추가 |
| 6 | **Expected outcomes 정리** | ✓ 완료 | `docs/2026-05-21-pre01-prep.md` 하단 — C1-C4, I1-I6, N1-N5 + decision tree + minimal yaml package |

---

## 3. 핵심 문서 맵

```
docs/
├── 2026-05-20-validate-idea-ai-figma-context-bridge.md  ← 메인 설계 문서 (Stage 1 + autoplan + grilling 결과 전부 포함)
├── 2026-05-21-figma-mcp-inventory.md                    ← PRE-02 spike (Figma MCP 도구 8 read + 8 write 분석)
├── 2026-05-21-pre01-prep.md                             ← PRE-01 미팅 준비 자료 (4 components + expected outcomes)
├── TODOS-autoplan.md                                     ← 전체 TODO 추적 (PRE/POST/MONTH-6/REJECTED)
├── pii-anonymization-git-safety.md                       ← PII 익명화 규칙 + grilling specificity 재정의
└── .autoplan-backups/                                    ← restore point (gitignored, PII 포함 가능)
```

---

## 4. 남은 작업 — 무엇을 해야 하는가

### 4.1 PRE-01: 외부 실행 (Claude 불가, founder 직접)

**Anchor-A 미팅 30분 + 1주 trial**. 절차는 `docs/2026-05-21-pre01-prep.md` 그대로.

미팅에서 얻어야 할 것:
- **C1**: 1주 RescueTime/Toggl trial 동의 (yes/no)
- **C2**: Paper mockup Venmo response — raw quote + 카테고리 (strong_positive / conditional / hedge / indifferent)
- **C3**: Figma plan + seat type (Professional+Dev 등)
- **C4**: 1주 aggregate trial 데이터 (yaml 형식)
- **I1**: U-01 atomic batch write 결과 (all_reverted / partial_commit)
- **I2**: U-02 timestamp 필드 존재 여부 (layer-level / file-level / none)
- **I3**: U-03 conditional write 필드 (yes/no)
- **I4**: Walkthrough memo + screenshots
- **I5**: 컨펌 round 수 baseline
- **I6**: Prompt 빈도
- **N1-N5**: nice-to-have (답 없어도 진행 가능)

### 4.2 다음 세션 진입 방법

1. PRE-01 완료 후, `docs/2026-05-21-pre01-prep.md` 하단의 **minimal yaml package** 형식 그대로 채워서 세션 첫 메시지에 paste
2. 자동 decision tree 분기:
   - C2 강한 긍정 + C4 ≥20% 절감 → **`/buddy:plan-build` 진입** (A approach 3-5일 task graph)
   - C4 5-20% → wedge sharpening (3 piece 우선순위 재결정)
   - C4 ≤5% → wound 가설 깨짐 → validate-idea 재진입
   - C1 no → sample 재정의
   - C3 Starter/View → ICP 재정의

### 4.3 POST-APPROVAL 작업 (plan-build 진입 후)

`docs/TODOS-autoplan.md` 참조:
- **Phase 2 (Design)**: `team-brand-spec.default.json`에 naming pattern 추가, 6-state spec mockup
- **Phase 3 (Engineering)**: sub-skill 디렉토리 생성, 4개 스크립트+테스트 쌍, 기존 108 tests CI block
- **Phase 3.5 (DevEx)**: install script, first-run wizard, demo 명령, error format, README 표준화

### 4.4 MONTH-6 GATE

- M6-01: C approach (design intent language) — 30 paid seats + 80% retention 3개월
- M6-02: Standalone Figma plugin — Series B 또는 enterprise pilot
- M6-03: Multi-user session sync — team-tier upgrade 요청 5건+

---

## 5. 아키텍처 결정 사항

### Plan A (확정 default)
Figma 공식 MCP (`https://mcp.figma.com/mcp`) + thin wrapper 3 piece.

### Plan B (fallback, 현재 trigger unlikely)
Figma plugin 직접 구현 + plugin 호환 새 MCP server. Trigger: Figma MCP가 근본적으로 불충분할 때.

### 기술 결정
- **Session TTL**: 5min + explicit `claude-design session reset` + scan-on-restart (git fetch model)
- **Collision granularity**: page-level (파일 아닌 페이지 단위)
- **Notification**: CLI text 알림 충분 (GUI 불필요)
- **Bias 통제**: 3-tier (자동 측정 도구 + aggregate-only 가시성 + 본인 과거 baseline 비교, 20% threshold)
- **Naming**: Latin + 숫자 + `_` only. Layer name 자체는 한글 허용 (별도 field)
- **Skill 3분해**: Layer creation skill (atrophy OK) + Judging skill (유지/강화) + Intent verbalization skill (UI 통해 upgrade). M1+M2 합친 γ Hybrid thesis.

---

## 6. Grilling 에서 나온 핵심 findings

### D5 (Ethical Blind Spot)
- founder = anchor 이중 역할에 의한 bias risk → 3-tier bias 통제로 해결
- North Star 추가됨: blind test pass rate → 50% convergence
- PII 익명화 ↔ grilling specificity 충돌 → **specificity = 이름 아닌 행동/시점/구조** 로 재정의

### D2 (Second-Order Effect)
- "사람이 약해진다" 는 억지 가정 → M1+M2 합친 thesis 확인
- 3 skill 분해: creation (atrophy OK), judging (유지), verbalization (upgrade)

### D3 (Failure Mode)
- Multi-machine + 협업 동시 작업 → scan-on-restart로 해결
- Page-level collision detection (다른 페이지 = 정상)
- CLI text notification 충분

---

## 7. Git 상태

```
Branch: master (origin/master 와 동기화)
Uncommitted changes:
  M  .gitignore  ← docs/.autoplan-backups/ 항목 추가

Tracked but modified (이전 commit에 포함된 파일들):
  docs/2026-05-20-validate-idea-ai-figma-context-bridge.md  ← autoplan + grilling 결과 반영 완료
  docs/2026-05-21-figma-mcp-inventory.md                    ← PRE-02 spike 결과
  docs/2026-05-21-pre01-prep.md                             ← PRE-01 준비 자료
  docs/TODOS-autoplan.md                                     ← TODO 추적

주의: .gitignore 만 uncommitted. 나머지 docs/* 파일은 이미 tracked 상태.
```

---

## 8. PII 규칙

`docs/pii-anonymization-git-safety.md` — anchor 실명 대신 placeholder 사용 규칙 + grilling 시 specificity 재정의 (이름 아닌 행동/시점/구조). 새 세션에서 반드시 읽을 것.

---

## 9. 주의사항

1. **PII 보호**: 모든 문서에서 실명 사용 금지. "Anchor-A" placeholder 사용. git에 commit하는 모든 파일에서 확인 필수.
2. **Co-Authored-By 금지**: commit 메시지에 attribution 포함하지 않음 (사용자 명시 선호).
3. **Grilling specificity 재정의**: 구체성 = 특정 사람 이름이 아닌, *행동/시점/구조*로 표현.
4. **Means vs Ends**: P3 wedge는 궁극적 비전(North Star)이 아닌, 의도적으로 가장 작은 출발점. PROCEDURE의 narrowest-wedge forcing에 의한 것.
5. **Restore point**: `docs/.autoplan-backups/2026-05-20-validate-idea-ai-figma-context-bridge.20260521140101.md` (PII 익명화 완료, gitignored).
