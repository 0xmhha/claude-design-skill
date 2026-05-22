# TODOS — Autoplan Deferred Items

> Origin: `/buddy:autoplan` 실행 결과 (2026-05-21) on `docs/2026-05-20-validate-idea-ai-figma-context-bridge.md`.
> APPROVED status: Phase 4 게이트 통과, 6 taste decisions 모두 recommended option 채택.

---

## PRE-IMPLEMENTATION (block — *코드 시작 전 의무*)

| ID | Item | Owner | Effort | Why |
|----|------|-------|--------|-----|
| PRE-01 | **The Assignment 실행** — Anchor-A 미팅 30분 (1주 RescueTime/Toggl trial 동의 + paper mockup Venmo response + walkthrough 녹취 + paid plan/seat type 확인 + U-01 atomic write 직접 호출 검증 + U-02 timestamp 응답 JSON inspect) | founder | 1 week | F-04 critical-gap mitigation. wound vs itch 판별. doc P2 obligation. PRE-02 의 U-01/U-02 잔존 검증 포함. |
| PRE-02 | **Figma MCP write API 한계 mapping** — ✓ 1차 완료 (`docs/2026-05-21-figma-mcp-inventory.md`). Plan A 확정 (hard gates PASS). 잔존 U-01/U-02/U-03 의 실증 검증은 PRE-01 에 통합 | founder | ✓ done | F-01 critical-gap 1차 완료. spike = Plan A 강한 default, Plan B 우선순위 ↓↓. |

→ 두 항목 완료 전 implementation 진입 차단.

---

## POST-APPROVAL (autoplan 결정 → 후속 작업)

### Phase 2 (Design) action items

- `team-brand-spec.default.json` 에 `element-naming.pattern` field 신규 추가 — 값: `<page>__<section>__<element>__<variant>`
- §S2 의 6-state spec → Figma plugin panel mockup (PRE-01 trial 결과 반영 후)
- Naming character set spec: Latin + 숫자 + `_` only. layer name 자체는 한글 허용 별 field.

### Phase 3 (Engineering) action items

- 신규 sub-skill 디렉토리: `claude-design-skill/skills/design-naming/` (A approach) + `skills/design-context-binding/` (B approach)
- 신규 scripts (test file 과 짝):
  - `scripts/element-id-resolver.py` ↔ `tests/element_id_resolver_test.py` (8 unit)
  - `scripts/session-state.py` ↔ `tests/session_state_test.py` (3 unit + 2 integration)
  - `scripts/collision-detector.py` ↔ `tests/collision_detector_test.py` (3 unit)
  - `tests/figma_mcp_integration_test.py` (4 integration with mock)
- 기존 108 tests CI block (regression rule)
- D-01 atomic write 대응: write batch 마다 read-back verify + diff log + rollback script
- C-01 session TTL = 5 min + explicit `claude-design session reset`
- P-02 batch figma write API (MCP 지원 시) 또는 transactional write group

### Phase 3.5 (DevEx) action items

- `npx @claude-design/install` script — claude-code missing 감지 + guide URL
- First-run wizard: `claude-design auth figma` (interactive token guide)
- Demo 명령: `claude-design naming demo` — sample figma + sample AI output + before/after diff
- Error format Tier 1 (Elm-style): 문제 + 원인 + fix + docs URL 강제. example template 작성.
- README 4-섹션 standardize: install / quickstart / troubleshoot / recipes (QUICKSTART.md 기존)
- SemVer + 6-month deprecation + codemod for naming-pattern 변경
- CI matrix: Mac / Linux / Windows
- TTHW telemetry opt-in with prominent prompt
- Pricing anchor = $39/mo per seat (marketplace listing 에 반영)
- Community = Github discussions only (claude-design-skill repo)

---

## MONTH-6 GATE (PMF signal 후 evaluate)

| ID | Item | Trigger |
|----|------|---------|
| M6-01 | C approach (design intent language) evaluation | 30 paid seats + 80% retention 3개월 (doc line 122) |
| M6-02 | Standalone Figma plugin (TTHW Champion <2min) | Series B fund-raise 또는 enterprise pilot 1+ |
| M6-03 | Multi-user share session sync (R-01) | per-seat 가 team-tier 로 upgrade 요청 5건+ |

---

## POST-PMF (no trigger yet — 평가 대기)

- Vertical expansion: e-commerce / fintech / SaaS — web3/game wedge sharpness 검증 후
- Self-hosted enterprise tier — SaaS per-seat saturation 후
- AI 모델 fine-tune / proprietary model — token cost 가 pricing floor 위협 시
- Sketch / Adobe XD / Penpot 통합 — C approach 의 일부
- TAM 측정 (Series A web3/game ICP 모수) — PMF 후 정확도 향상

---

## REJECTED (Phase 1 명시 배제)

- C first-bet — "플랫폼 신기루" (doc line 102, autoplan audit row #14)
- Figma MCP plugin fork (B approach) — upstream sync 부담 (audit row #27)
- 별도 plugin 신규 marketplace listing — sub-skill 로 통합 (audit row #28)
