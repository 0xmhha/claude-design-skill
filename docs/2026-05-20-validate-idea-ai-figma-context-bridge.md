<!-- AUTOPLAN RESTORE POINT: docs/.autoplan-backups/2026-05-20-validate-idea-ai-figma-context-bridge.20260521140101.md (revert via `cp` to undo autoplan mutations) -->
# Design: AI-Figma Context Binding Bridge (working title)

Date: 2026-05-20
Status: DRAFT
Mode: Startup

> **Origin**: buddy cycle-3 §B.1 plugin path. `/buddy:concretize-idea` → `validate-idea` Stage 1 출력. 본 doc 의 *진짜 IP 소유자* = 사용자. 후속 cycle 진척 시 claude-design-skill repo 또는 별도 idea repo 로 이동 권장.

---

## Problem Statement

AI 기반 디자인 작업을 수행하는 designer 들 (특히 web3/game vertical) 이 Claude Code + Figma MCP chain 에서 일관된 마찰을 겪고 있음. AI 가 HTML+CSS base design 을 생성하면, Figma 에 적용하려면 manual rebuild 필요 — Figma MCP 가 *font 변경 같은 basic operation* 조차 안정적으로 수행 못함. 매 prompt 마다 project/page/element triplet 을 manual 입력해야 함. 결과: AI base work 의 가치가 *figma 수작업* 으로 *재구축* 되며, designer 가 컴포넌트를 처음부터 figma 에서 다시 만듦.

---

## Demand Evidence

- **Survey**: 익명 survey, web3/game vertical designer 대상. 80%+ 가 AI-Figma chain 마찰을 *top pain point* 로 응답
- **Founder self-use**: 본인 (engineer doing product building) 이 same chain breakage 직접 경험. claude-design-skill v1.0.0 의 maintainer 이자 daily user
- **Sibling internal designers**: founder 의 인접 디자이너 그룹이 *동일 survey 응답*. Follow-up 가능
- **Named anchor**: **Anchor-A** *(PII-safe placeholder)*, web3 vertical Series A startup lead designer (1:1 미팅 evidence). Team: small designer cohort + 1 engineer. 새 브랜딩 + 주 2 건 publishing + frontend code 도 lead designer 가 챙기는 시도 → **2 달 이상 초과 근무**
- **Measured cost**: claude-design-skill 에서 *간단한 wireframe 1 회 생성* = token limit 의 9%. 즉 ~11 wireframes / session — 1 프로젝트도 session 안에 못 끝냄
- **Self-reported time waste**: 20h/week (methodology = self-report only — *behavioral observation upgrade* obligation 으로 P2 에 기록)

---

## Status Quo

**Designer workflow** (Anchor-A + 사내 디자이너 그룹의 보고):
- AI 출력 (HTML+CSS) → Figma 수작업 적용
- Figma MCP 의 font 변경 시도 → 실패
- 컴포넌트 *처음부터* Figma 에서 직접 작업
- 또는: ChatGPT image gen / 또는 reference + 직접 figma

**Engineer (founder) workflow**:
- 컨셉 + 산업군 + reference 사이트 → AI design 생성
- Frontend 먼저 구현이라 코드에 바로 적용
- 디자인 수정 시 *코드 baseline 으로 tag 하나하나 지정* 필요
- AI 가 *vanilla code + CSS* 출력 (componentized X) → 재사용성 깨짐

**Cross-cutting frustration**: "ai 로 프로그래밍의 영역은 자동화가 잘되어가는데, 디자인 영역은 여전히 큰 허들이 존재하는 점에서 짜증이남" (user 의 정확 단어)

---

## Target User & Narrowest Wedge

**Anchor user**: Anchor-A — web3 vertical Series A startup lead designer, small designer cohort + 1 engineer. KPI = 브랜딩 완성도 (실패 시 투자 철회 risk). Velocity-focused boss. 매일 9-11 am 가 *AI 도구 base 시도 → 만족 안 되어 figma 수작업* 시간대.

**Persona split** (Q3 에서 surface):
- Primary: lead designer at Series A startup (1-5 designer team)
- Secondary: engineer doing product building (founder 본인)
- Hybrid possible: Anchor-A case 처럼 lead designer 가 frontend code 도 시도 — *single-product-for-hybrid-persona* 가설

**Wedge — (d') AI prompt ↔ Figma MCP context binding 자동화**:

*재산정 정의 (PRE-02 spike 2026-05-21 결과 — `docs/2026-05-21-figma-mcp-inventory.md`)*:

본 wedge 의 *대부분* 이 Figma 공식 MCP (`use_figma`, `generate_figma_design`, `get_design_context`, `get_metadata`) 위 thin wrapper. **신규 가치 영역 = 3 piece**:

1. **Session-state cache** — Project/page/element triplet 의 implicit resolution + 5min TTL + explicit reset + scan-on-restart. (figma 공식은 stateless 호출만, session 관리는 client 측 신규 구현)
2. **Collision detector** — globally-unique naming 강제 + collision 시 CLI 텍스트 알림 (git fetch 모델 transfer, D3 grilling 결정). figma 공식 미지원 영역.
3. **Visual disambiguation prompt-back** — CLI 텍스트 알림 형식 (시각적 UI 불필요, D3 grilling). naming pattern `<page>__<section>__<element>__<variant>` 강제.

*제거된 layer (figma 공식 흐름이 cover)*:
- ~~UI selection + explicit instruction~~ — `get_design_context(node_id)` + prompt 가 공식 흐름. 신규 구현 0.
- ~~Layer rename 자체~~ — `use_figma` 가 frame/component/variant/text 모두 지원.

*Figma-power 와의 관계*: complementary (충돌 아님). figma 공식 plugin (`claude plugin install figma@claude-plugins-official`) 위에 *3 piece thin wrapper* sub-skill 추가 형태.

- Sub-feature (d): AI 출력 element 이름 → figma layer 이름 자동 적용 (independent ship-able, piece 2+3 의 부분)

---

## Premises

User agreed (2026-05-20):
1. **P1 — Demand**: web3/game vertical designer (survey 80% + Anchor-A verified). Primary = lead designer at Series A startup. Secondary = engineer doing product building.
2. **P2 — Status quo**: ChatGPT image gen → manual figma. 20h/week wasted *self-reported* — **active obligation**: behavioral observation upgrade via 1-week trial measurement.
3. **P3 — Wedge**: (d') context binding 자동화. (d) layer naming 은 sub-feature.
4. **P4 — Thesis**: 디자인 자산 = AI 통신 언어의 source. Contrarian — Figma 가 native AI 로 vertical integrate 안 한다는 + 디자인 자산 표준이 vendor-fragment 안 된다는 가정 위.

---

## Approaches Considered

### A — Minimal Viable
- **Summary**: (d) only. AI 출력 element 이름 → figma layer 이름 자동 적용. claude-design-skill 의 figma extractor 위에 naming-only wrapper.
- **Effort**: S (3-5 일) / **Risk**: Low
- **Pros**: 1 주 안 데모 가능 / 측정 가능 (before/after layer tree) / claude-design-skill 인프라 재활용
- **Cons**: 단독 paid 약함 (figma plugin store free alts) / Q5 surprise (context binding) 미해결 / network effects 0
- **재사용**: claude-design-skill figma extractor + license/NOTICE infra

### B — Context Binding Sub-platform (recommended balance)
- **Summary**: (d') ship. Session-state-aware MCP wrapper + naming convention enforcement + collision disambiguation. (d) sub-feature 로 포함.
- **Effort**: M (2-4 주) / **Risk**: Med
- **Pros**: Q5 surprise 직접 해결 (Venmo-pain 직격) / A 가 B 의 first sprint / $29-49/mo paid commitment 가능 / Series A startup per-seat ICP
- **Cons**: Figma MCP API의 write 한계 / 2-4 주 ship 동안 figma native AI 발표 risk / naming convention designer 거부감 risk
- **재사용**: claude-design-skill 전체 — extractor + brand-spec + confidentiality gate + 108 regression test

### C — Design Intent Language (long-term ideal)
- **Summary**: Tool-neutral language (syntax/vocabulary/grammar) across Figma/Sketch/Adobe XD/Penpot 표준 spec + open standard 공개
- **Effort**: XL (6-12 개월) / **Risk**: High
- **Pros**: P4 thesis 100% alignment / tool-neutral moat / 5-10x TAM
- **Cons**: no validation between / 6-12m ship while figma may ship native AI / Series A pain 지금 해결 안 됨
- **재사용**: claude-design-skill 의 design-knowledge catalog 부분

---

## Recommended Approach

**A → B sequence**, C 는 *PMF 후 evaluate*.

**Rationale**: A 의 3-5 일 ship 이 *Anchor-A + 사내 2 명 실 trial* 데이터 확보 (P2 의 behavioral observation upgrade obligation 직접 충족). 2 주 내 B 의 context binding 추가. 3-6 개월 paid user growth + churn 측정 후 C 의 tool-neutral 베팅 평가. C 를 first-bet 으로 가는 건 *플랫폼 신기루 의 가장 위험한 변형* (6 개월 burn 없이 validation 0).

---

## Open Questions

1. **Figma MCP API 의 write 권한 한계** — 어느 ops 가능 / 불가능? B 의 4 주 ship 범위에 직접 영향. 답 없으면 B 의 effort 추정이 틀릴 risk. → *fallback*: PRE-02 spike 결과 "지원 부족" 일 때 §Validate-Advanced-Edge-Idea Grilling 의 **Plan B** (Figma plugin + 자체 MCP server) 트리거
2. **P2 의 behavioral observation upgrade** — Anchor-A 또는 사내 디자이너 1 명의 1-week RescueTime/Toggl trial 은 누가, 언제 진행? *The Assignment* 의 핵심
3. **Series A web3/game startup TAM 측정** — Anchor-A 같은 ICP 의 모수가 wedge sharpness 의 trade-off 결정
4. **Naming convention 수용성** — A ship 후 첫 trial 사용자가 naming convention 거부하면 B 의 wedge 약화. 거부 시 fallback design?
5. **C 의 thesis disruption risk** — Figma 의 향후 12 개월 AI roadmap 공지 시점 = C 의 contrarian validity 의 가장 큰 위협

---

## North Star (long-term ends)

**진짜 목표**: AI 가 생성한 디자인을 *리드 디자이너 (이론 + 경험 보유) 가 blind test 로 사람 작업과 구분 불가* 한 레벨로 끌어올리는 것.

**측정 (long-term)**: blind test 통과율 — 리드 디자이너에게 결과물만 제시 시 AI vs 사람 정확 식별률이 *50% (random) 에 수렴*.

**Wedge 와의 관계**: P3 의 context binding 자동화는 *수단* (means). North Star 는 *목적* (ends). means 가 ends 로 인과 작동하려면 **anti-slop + DESIGN.md 가드레일** 이 동시 작동 필요. 둘의 align 은 month-3 PMF gate (Success Criteria) 와 별도로 *6-month evaluation* 에서 측정.

> *출처*: `/buddy:validate-advanced-edge-idea` D5-Q1.d (2026-05-21) — founder 직접 발화 명시 시점. doc 초기 작성 시 누락된 north star 의 grilling-driven 추가.

## Success Criteria

| Phase | Window | Metric | Pass |
|-------|--------|--------|------|
| **Week 1 (A ship)** | 3-5 일 | Anchor-A + 사내 2 명 = 3 trial users *used ≥ 1 회* | 3/3 |
| **Week 2-4 (B ship + first $)** | 2-4 주 | Per-seat paid commitment ≥ 1 / 3 at $29/mo | ≥ 1 |
| **Month 3 (PMF signal)** | 3 개월 | 10 paid seats ($290/mo) | ≥ 10 seats |
| **Month 6 (C decision gate)** | 6 개월 | 30 paid seats / 80%+ retention 3 개월 | C bet justified iff $1000/mo + retention > 80% |

---

## Dependencies

- **Figma MCP API** (external, 권한 한계 not under control)
- **claude-design-skill repo** (own codebase, 자유 수정 가능)
- **Claude API token cost** (per-prompt cost — pricing floor 결정 변수)
- **Anchor-A 의 actual trial 동의** (현재 no commitment — *The Assignment* 가 직접 target)

---

## The Assignment

**이번 주 — Anchor-A 미팅 1 회**. 30 분. 3 specific asks:

1. **1 주 trial 동의 받기**: RescueTime / Toggl 측정값을 next session 에 가져옴. P2 의 behavioral observation upgrade 직접 충족.
2. **(A) paper mockup 보여줌**: 1 page. "layer naming AI 출력 → figma 자동 적용" before/after gif. Anchor-A 가 *"Venmo 보내고 싶은지"* 직접 반응 측정.
3. **Anchor-A 의 layer naming + context binding 정확 pain 의 단계별 walkthrough recording** (또는 자필 메모) 동의.

**Outcome**: meeting 후 다음 cycle-3 §B.1 update — Anchor-A trial 데이터 + paper mockup 반응. 만약 *"Venmo"* 응답 → (A) 빌드 start. *"not exactly"* 응답 → wedge re-formulate.

---

## What I noticed

- 사용자가 *"figma mcp 를 통해 font 변경도 수행되지 않는 문제"* 정확 phrasing — 일반적 "figma 연동 어려움" 이 아닌 **single API operation 의 specific failure**. 그 specificity 가 wedge root cause analysis 가능하게 만든 핵심.
- Q3 에서 *"예시 거의 그대로"* 답 인정한 뒤 *"추가로 더 입력하면, Anchor-A..."* 으로 self-correct — escape hatch + voluntary follow-up. Founder 가 anti-sycophancy 의 의도 *이해했음* 의 unfakeable 증거. Mimicry → real anchor 의 *한 발화 회수* 가 본 세션의 가장 강한 signal.
- Q5 의 *"매번 입력해주고 있어서 놀라웠으며"* 의 *"놀라웠으며"* 단어 — 사용자가 *예상* 한 것과 *경험* 한 것 사이 gap 을 본인이 정확히 명명. (d) → (d') wedge upgrade 의 진짜 entry point. PROCEDURE 의 "Gold: 제품이 설계 안 된 것 사용자가 하는 것" 정의 그대로 발동.
- *"이 두 가지 기능만 가능해도 나머지는 모두 확장이 개념이기 때문에 스켈레톤"* (Q4 답) — 플랫폼 신기루 진단의 솔직한 자료. Push 받은 후 (d) → (d') 로 narrow 함. *솔직한 reframe 능력* 이 founder 의 좋은 trait.

---

## 다음 단계 (핸드오프)

본 doc 의 입력 상태 = **"아이디어의 논리적 완결성 보완"** (구현 단계 무결성). PROCEDURE 의 handoff 표 per 본 case → `validate-advanced-edge-idea` (Stage 2). 단, cycle-3 §B.1 의 *Stage 1 만 우선* 결정 — validate-advanced-edge-idea 는 **별 세션 권장**.

**Recommended sequence**:
1. *이번 주*: The Assignment 실행 (Anchor-A 미팅) → behavioral observation 데이터 수집
2. *Next session* (Assignment 결과 가져온 뒤): `/buddy:validate-advanced-edge-idea` 진입 — edge case + hidden assumption grilling
3. *그 후*: 아래 둘 중 하나
   - 데모 가능한 prototype 시작 → A 의 3-5 일 build
   - 또는: concretize-idea Stage 3+ (`assess-business-viability`, `analyze-competition-and-substitutes`, `review-pricing-and-gtm`, `map-customer-segments`) 로 사업성 더 정제

핸드오프 규칙 (PROCEDURE 명시): "사용자에게 '다음 단계로 [skill] 을 invoke 할까요?' 형태로 명시 확인. **자동 전환 금지**."

---

## Autoplan Annotations (2026-05-21)

> 본 섹션은 `/buddy:autoplan` 실행 결과. PROCEDURE 의 phase-별 finding + 결정 audit trail. doc 본문은 변경하지 않고 *annotation* 으로만 부착.

### Phase 1: Scope 리뷰 (review-scope · SELECTIVE EXPANSION · single-voice)

**전제 게이트 결과 (2026-05-21)**: user 결정 = **P1~P4 hold + 진행**.

**전제 챌린지 결과**

| 전제 | 평가 | Stress test |
|------|------|-------------|
| P1 (Demand) | hold | Anchor-A + 사내 디자이너 그룹 self-report 강함. behavioral upgrade obligation 은 P2 격리. |
| P2 (Status quo, 20h/wk) | hold-with-flag | self-report only. **wound vs itch 판별의 single point** = The Assignment 의 RescueTime/Toggl trial. |
| P3 (Wedge) | hold | (d') context binding 자동화 핵심. (d) layer naming = sub-feature. |
| P4 (Thesis) | hold-with-risk | Figma native AI 발표 risk (Q5) 가 thesis disruption #1 위협. 6-month decision gate 가 risk hedge. |

**이미 존재하는 것** (sub-problem → 기존 코드 매핑)

| Sub-problem | 기존 코드 | 재사용 / rebuild |
|-------------|-----------|------------------|
| Figma layer 추출 | `scripts/figma-to-brand-spec.py` (figma extractor) | reuse |
| Brand-spec seed | `team-brand-spec.default.json` | reuse + extend |
| Confidentiality gate | claude-design-skill 의 redaction utility | reuse |
| Regression test harness | claude-design-skill 108 tests | reuse (test infra) |
| Figma MCP write API | external — Figma MCP plugin | wrapped (Q1 risk: write 한계) |
| Element ID 생성 | 없음 | **build (A)** |
| Session-state 관리 (project/page/element triplet) | 없음 | **build (B)** |
| Collision visual disambiguation prompt-back | 없음 | **build (B)** |

**Dream state delta**

- **CURRENT**: AI base 코드 → figma 수작업 재구축. 매 prompt triplet 수동 입력. 20h/wk 낭비 (self-report).
- **THIS PLAN (A→B)**: A 의 naming 자동화 → trial user 3명 확보. B 의 context binding → paid commitment 1+. claude-design-skill 인프라 위에 layered.
- **12-MO IDEAL (C alignment 시)**: tool-neutral design intent language (Figma/Sketch/XD/Penpot). 5-10x TAM. 단 PMF 후 평가.

**Delta 평가**: A→B 가 12-month ideal 로 향함 (incremental wedge → platform 진화). C 미실행 시 ideal 미달 가능하나, PMF signal 없이 C 진입은 "플랫폼 신기루" — trajectory 옳음.

**구현 대안**: doc line 75-94 의 A/B/C 가 effort/risk/pros/cons/reuses 포맷 충족 — Phase 1 에서 **새 대안 추가 없음** (P3 pragmatic).

**Scope 결정 테이블**

| # | Proposal | Effort | Decision | Reasoning |
|---|----------|--------|----------|-----------|
| 1 | A approach (layer naming wrapper) | S (3-5 일) | ACCEPT | P3 wedge first-week validation. 인프라 재활용. |
| 2 | B approach (context binding sub-platform) | M (2-4 주) | ACCEPT (A 의 first sprint 연장) | P3 의 (d') 직격. paid commitment gate. |
| 3 | C approach (design intent language) | XL (6-12 개월) | DEFER (month-6 gate) | P2 — blast radius 밖, multi-quarter. |
| 4 | The Assignment (Anchor-A trial) | S (1 주) | ACCEPT-FIRST | wound vs itch 판별. **코드 작성 전 선행 의무**. |
| 5 | Figma MCP write API 한계 mapping | S (1 일) | ACCEPT (Phase 3 prereq) | doc Q1. B 의 effort 추정 정확도의 single largest dependency. |
| 6 | Behavioral observation tooling (RescueTime/Toggl) | XS (0.5 일) | ACCEPT (Assignment 와 묶음) | P2 obligation 충족 수단. |
| 7 | Naming rejection fallback design | S (1 일) | DEFER to Phase 2 | doc Q4. trial 사용자 거부 신호 후 design. |
| 8 | Per-seat pricing model 확정 ($29-49/mo) | S (1 일) | DEFER to Phase 3.5 | wedge ship 후. |
| 9 | Series A web3/game TAM 측정 | M (1 주) | DEFER (post-PMF) | wedge sharpness — PMF signal 후 정확도 더 높음. |
| 10 | C first-bet 채택 | XL | REJECT | "플랫폼 신기루" — doc 자체 진단 (line 102). |

**NOT in scope**

- C first-bet — validation 0 의 6 개월 burn risk
- 다른 vertical (e-commerce, fintech) — web3/game wedge sharpness 우선
- Self-hosted enterprise tier — SaaS per-seat first wedge
- AI 모델 fine-tune / proprietary model — Claude API 직접 사용
- Sketch / Adobe XD 통합 — C approach 의 일부

**실패 모드 / 에러 registry (Phase 1 — Phase 3 가 확장)**

| ID | Failure mode | Severity | Mitigation |
|----|-------------|----------|------------|
| F-01 | Figma MCP write API 가 naming 자동 적용 불가 (read-only) | **critical** | Phase 3 prereq: write API mapping. fallback = Figma plugin 직접 작성. |
| F-02 | Naming convention 거부 (trial 사용자) | high | Phase 2 disambiguation UX. opt-in mode fallback. |
| F-03 | Figma native AI 발표 → wedge 무효 | high (12mo) | 6-month decision gate. C 평가 timing 의 single trigger. |
| F-04 | The Assignment 미실행 → wound 데이터 부재 | **critical** | autoplan 외부 — *코드 시작 전* Assignment 완료 = single prerequisite. |
| F-05 | Anchor-A trial 거부 → primary anchor 상실 | medium | 사내 디자이너 2명 fallback. survey 80% pool 확장. |
| F-06 | claude-design-skill v1.0.0 의 figma extractor breaking change | low | 본인 maintainer = 직접 control. |
| F-07 | Token cost (1 wireframe = 9%) 가 paid pricing floor 미달 | medium | Phase 3.5 DevEx pricing 결정. |

**Phase 1 → Phase 2 핸드오프**

- Mode 권장 (Phase 2): **POLISH** — A/B 의 wedge UX (naming convention + disambiguation) 가 작은 surface 지만 high-stakes (rejection → wedge 약화).
- Stress-test 우선 영역: Pass 2 (Interaction State) — disambiguation prompt-back 의 empty/error/partial state. Pass 7 (Unresolved decisions) — doc Q4 의 rejection fallback.
- Skip 영역: Pass 4 (AI Slop) — 본 doc 은 UI 디자인 명시 없음.

### Phase 2: Design 리뷰 (review-design · POLISH · single-voice)

**대상 UI surface** (본 doc 추출):
- (S1) Layer naming 결과 — A approach 의 figma 적용 후 designer 가 보는 layer tree.
- (S2) Collision visual disambiguation prompt-back — B approach 의 의사결정 UI.
- (S3) Paper mockup 1-page (The Assignment, line 141) — Anchor-A 미팅 before/after gif.

**Pass 별 score**

| Pass | Score 변화 | Fix-to-target |
|------|-----------|---------------|
| 1 Info Architecture | 2 → 6 | doc 에 UI hierarchy 명시 없음. Fix: (S2) primary/secondary 명시 (§S2-hierarchy). |
| 2 Interaction State Coverage | 3 → 7 | (S2) state table 없음. Fix: §S2-states. |
| 3 User Journey & Emotional Arc | 5 → 7 | "9-11am peak" + Venmo test 부분 arc. Fix: §journey. |
| 4 AI Slop Risk | N/A | graphical UI spec 부재 — skip per Action 편향. |
| 5 Design System Alignment | 4 → 6 | naming 의 brand-spec 정렬 미명시. Fix: §S1-brand. |
| 6 Responsive & A11y | N/A | CLI/MCP wrapper — viewport 부재. (S2) web surface 채택 시 재평가. |
| 7 Unresolved decisions | 8 → 8 | doc Q1-Q5 well-surfaced. Minor: Q4 stake 분석 (F-02 가 일부 cover). |

**§S2-states — Disambiguation prompt-back state table** *(auto-added per P5)*

| State | Designer 가 보는 것 |
|-------|---------------------|
| Loading | "Resolving element ID..." progress + element preview thumbnail |
| Empty (no collision) | silent apply — no prompt |
| Single collision | side-by-side thumbnail (existing vs new) + [Use existing / Create new with suffix / Cancel] |
| Multi-collision | list view, checkbox per element + bulk action |
| Error (Figma API timeout) | "Couldn't reach Figma. [Retry] [Apply locally only]" + error code |
| Partial (n/m applied) | "3/5 applied. 2 failed: [list with reason]. [Retry failed] [Skip]" |

**§S2-hierarchy — Disambiguation primary/secondary/tertiary**
1. Primary: thumbnail 비교 (3-sec visual scan)
2. Secondary: decision actions (use/create/cancel)
3. Tertiary: error code / debug context

**§journey — Designer 1주 trial storyboard**

| Step | Designer Does | Designer Feels | Plan Specifies? |
|------|---------------|----------------|-----------------|
| T+0 (Mon 9am) | RescueTime install + baseline measure | Skeptical | The Assignment — script 자동 setup |
| T+1d | First (A) layer-naming run | Curious — "이게 진짜 들어가?" | magic moment (Phase 3.5 와 align) |
| T+3d | Collision 발생 → disambiguation prompt | Surprise OR friction (taste) | §S2-states |
| T+5d | Before/after layer tree diff | Validation OR rejection signal | Phase 3 metric capture |
| T+7d | Founder 미팅 — Venmo response | Decision moment | line 142 The Assignment |

**§S1-brand — Naming convention brand-spec alignment**
- `team-brand-spec.default.json` 가 naming convention seed → A approach 는 신규 field `element-naming.pattern` 추가.
- Auto-added pattern: `<page>__<section>__<element>__<variant>` (Figma slash convention 회피 — naming 안전성).

**미해결 디자인 결정 (Phase 4 게이트 후보)**

| Decision needed | If deferred | Recommendation |
|----------------|-------------|----------------|
| Disambiguation surface (Figma plugin panel vs claude-code terminal vs web) | designer 어디서 결정? | **taste** → Phase 4 |
| Naming pattern character set (Latin only vs Unicode + Korean) | i18n / Korean designer 대응 미정 | **taste** → Phase 4 |

**Phase 2 → Phase 3 핸드오프**: (S2) state coverage 가 Phase 3 의 test 다이어그램 input. naming pattern character set 결정이 collision algorithm 의 비교 함수 design 에 영향.

### Phase 3: Engineering 리뷰 (review-engineering · single-voice · 7 dimensions + deep-module)

**1. Data Flow** — ASCII diagram (A approach base + B 추가):

```
AI prompt → [claude-code] → HTML+CSS with data-element-id
                ↓
         [claude-design-skill]
         ├─ figma-to-brand-spec (existing) ──→ current layer tree (read)
         ├─ NEW element-id resolver          ──→ <page>__<section>__<element>__<variant>
         ├─ NEW collision detector (B)       ──→ disambiguation prompt-back
         ├─ NEW session state (B)            ──→ (project, page, element) triplet cache
         └─ Figma MCP write ──────────────────→ layer rename applied
                ↓
         verification read-back (MCP read) ──→ confirm applied count
```

**Validation 경계**: AI output → resolver (regex 형식 검증), Figma MCP response → applied-count vs expected diff, claude-code RPC → schema validate.

**Issue D-01 (critical)**: Figma MCP write 의 atomic 보장 부재 — partial failure 시 layer tree inconsistent. **Recommendation**: write batch 마다 read-back verify + diff log + rollback script (수동 revert 가능 형태). (DRY: existing figma-extractor 의 read 코드 reuse)

**2. Caching** — A 무 cache (stateless). B 의 session state = 캐시.

**Issue C-01**: session state TTL 미정. **Auto-decision**: 5분 TTL (designer thinking time) + explicit `claude-design session reset`. (P5 explicit)

**Issue C-02 (high)**: stale data — 다른 designer 동시 figma 편집 시 cached element-id 가 stale. **Recommendation**: write 전 freshness check (figma read-back 의 modification-time 비교).

**3. Concurrency**:

- **Race R-01 (high)**: designer 수동 rename 동안 wrapper write → conflict. Fix: modification-time check + disambiguation fallback (§S2 의 Single collision state 연결).
- **Race R-02**: multi-prompt 동시 처리. Single-writer per session (claude-code single thread 가정 OK). Multi-user share session 시 → **taste decision** (Phase 4).

**4. Performance**:

- **P-01**: 1 wireframe = token 9% (doc line 23). A 의 layer-naming = +<2% 증분 목표. 측정 점 명시.
- **P-02**: N+1 figma write — 100-element 에 100 write call. Fix: batch API (MCP 지원 시) 또는 transactional write group.
- **P-03**: Cold start layer-tree read latency. Fix: lazy load on first prompt + background prefetch on session start.

**5. Edge cases**:

| Input | Risk | Coverage |
|-------|------|----------|
| Empty figma (zero layer) | naive case OK | test |
| 1000+ element figma | latency 폭증 (P-03 와 연결) | perf test |
| 비-Latin (Korean/Japanese/Chinese) name | character set 결정 미정 (Phase 2 taste) — NFC normalize 필수 | test |
| RTL language | (S2) thumbnail 영향 — (S2) web 채택 시 RTL CSS | test (defer to S2 surface 결정) |
| Multi-user concurrent edit | R-01 race | integration test |
| AI invalid element-id | regex reject + retry hint to AI | unit test |
| Naming rejection (F-02) | Phase 2 opt-out fallback | trial-eval |

**6. Test Coverage** — PROCEDURE skip 금지. ASCII coverage diagram:

```
CODE PATHS (planned)                          USER FLOWS (planned)
[+] scripts/element-id-resolver.py            [+] A trial: Anchor-A + 사내 2명
  ├── resolve(html, layer_tree)                 ├── [GAP] First-run (no collision)
  │   ├── [GAP] Latin name                       ├── [GAP] Collision encountered
  │   ├── [GAP] Unicode/Korean (NFC)             └── [GAP] Naming rejection (F-02)
  │   ├── [GAP] Empty layer tree              [+] B trial: paid commitment
  │   ├── [GAP] 1000+ tree (perf)               ├── [GAP] Session across prompts
  │   └── [GAP] Invalid id from AI              ├── [GAP] Concurrent figma race
  ├── verify_applied(figma_resp, expected)      └── [GAP] Multi-user file
  │   ├── [GAP] Partial write
  │   └── [GAP] Atomic failure                [+] Errors
[+] scripts/session-state.py (B)                ├── [GAP] Figma API timeout UX
  ├── load(project_id)                          ├── [GAP] Write-conflict prompt
  │   ├── [GAP] Cold start                      └── [GAP] Partial failure summary
  │   └── [GAP] Stale check
  └── invalidate(reason)
[+] scripts/collision-detector.py (B)
  └── detect(new_ids, current_tree)
      ├── [GAP] Zero collision
      ├── [GAP] Single
      └── [GAP] Multi (3+)

COVERAGE: 0/20 paths tested (doc 단계 normal). GAPS: 20.
REUSE: claude-design-skill 108-test pytest harness.
```

**Test file 계획** (각 GAP 별 spec):
- `tests/element_id_resolver_test.py` (8 unit)
- `tests/session_state_test.py` (3 unit + 2 integration)
- `tests/collision_detector_test.py` (3 unit)
- `tests/figma_mcp_integration_test.py` (4 integration with mock)

**Regression rule (mandatory)**: claude-design-skill v1.0.0 의 figma-extractor 기존 108 tests 는 A/B 진입 시 *반드시* pass. CI block.

**7. Architecture (deep-module 4-criteria)**:

| Criterion | A | B | Auto-decision |
|-----------|---|---|---------------|
| Deep module | ✓ small CLI iface, large impl | ✓ MCP wrapper 가 session/collision 숨김 | accept |
| Interface depth | medium — direct MCP 노출 가능 | high — wrapper 가 raw detail 차단 | B 에서 강화 |
| Locality | claude-design-skill repo 내 | 동일 | accept |
| Leverage | A → B 인프라 재활용 → C 신호 | high | accept |

**Issue A-01**: B 의 "session-state MCP wrapper" — Figma MCP plugin fork vs neuf MCP server? **Recommendation**: neuf MCP server (claude-design-skill sub-module). fork 회피 (upstream sync 부담). (P5 explicit > clever)

**Issue A-02**: Distribution — A/B 가 어떻게 designer install? claude-design-skill v1.0.0 의 plugin marketplace 이미 존재. **Recommendation**: 신규 plugin 아닌 claude-design-skill sub-skill (`design-naming`, `design-context-binding`) 추가. 1 marketplace listing 유지.

**실패 모드 통합 summary**

| ID | Failure | Test | Error handling | User sees | Class |
|----|---------|------|----------------|-----------|-------|
| F-01 | Figma MCP write 한계 | GAP | GAP | undefined | **critical** |
| F-02 | Naming rejection | GAP | Phase 2 §S2 partial | partial UX | high |
| F-03 | Figma native AI (12mo) | N/A | N/A | strategic | high |
| F-04 | Assignment 미실행 | N/A | N/A | external obligation | **critical** |
| F-05 | Anchor-A 거부 | N/A | N/A | external | medium |
| D-01 | Atomic write 부재 | GAP | GAP — verify+diff | partial UX | **critical** |
| C-01 | Session TTL stale | GAP | GAP — freshness | wrong layer applied | high |
| P-01 | Token budget 초과 | GAP — measure | N/A | session exhaustion | medium |
| P-02 | N+1 figma write | GAP — batch API | GAP | latency | medium |
| R-01 | Concurrent rename race | GAP | partial via §S2 | conflict prompt | high |

**NOT in scope (Phase 3)**

- Multi-tenant SaaS infra (per-seat billing → Phase 3.5)
- Self-hosted enterprise distribution (Phase 1 NOT-in-scope)
- Multi-user collaborative figma session sync (month-3+ post-PMF)
- Cache stampede defense (A/B 의 designer 개인 단위 scale 에서 unnecessary)

**이미 존재하는 것 (Phase 3 perspective)**

pytest harness 108 tests · figma-to-brand-spec.py · plugin marketplace ref · MCP protocol · Claude API token tracking.

**Phase 3 → Phase 3.5 핸드오프**: A-02 distribution path = Phase 3.5 install flow 의 single input. P-01 token budget = pricing dependency. §S2 state = Pass 1 (Getting Started) happy path.

### Phase 3.5: DevEx 리뷰 (review-devex · POLISH · single-voice)

**TARGET DEVELOPER PERSONA**

| Field | Value |
|-------|-------|
| Who | Lead designer at web3/game Series A startup. 3-5 designer team. Brand 완성도 = KPI. |
| Context | 매일 9-11am AI tool 시도 → 만족 안 되면 figma 수작업 (doc line 48) |
| Tolerance | 5분 — 학습보다 직접 figma 가 빠르다 판단 시 abandon |
| Expects | Figma 의존; claude-code/CLI 익숙도 없음; per-seat pricing 익숙 |

**공감 narrative (1인칭, Anchor-A perspective)**

> "친구가 figma 에서 AI 가 layer name 자동 넣어준다는 도구 추천. README 첫 줄 'Claude Code plugin' — 뭔지 모름. install 명령 보임. Cursor 안 쓰는데 claude-code 가 뭔지 검색 5분. npm install. 그 사이 figma 에서 layer 5 개 만듦. CLI 실행 — figma token 요청. 어디서? README setup 섹션 찾기 어렵. 10분째. token 발급 — figma 권한 페이지. 다시 CLI. 'No element-id in prompt' 에러. 무슨 뜻? 검색 결과 없음. github issue 던지고 다른 일."

→ **TTHW 추정 = 15-25 min (Red Flag tier)**.

**경쟁자 벤치마크**

| Tool | TTHW | Notable DX |
|------|------|------------|
| Stripe | <30s | 한 키, 한 curl, 돈 이동 |
| Vercel | <2min | `git push` → live URL |
| Figma plugin (typical) | 1-3min | 검색 + install + run |
| Cursor | ~3min | install + sign-in + first AI prompt |
| **THIS PRODUCT (current)** | 15-25min | **claude-code dependency = friction** |

**TIER decision (auto)**: **B) Competitive (2-5 min)** — designer 페르소나 Stripe-tier 기대치 아니지만 5분 초과 시 abandon risk. Champion tier 는 standalone Figma plugin 필요 (multi-quarter, P2 위반). Competitive 가 P1 + P2 둘 다 충족.

**Magical moment**: AI 가 만든 element 이름이 figma 에 *마술처럼* 들어가는 순간. **Delivery vehicle (auto)**: **B) Copy-paste 데모 명령** — `claude-design naming demo` 가 sample figma + sample AI output + before/after diff 를 1 명령으로 표시.

**Friction Point Trace (6 stages)**

| Stage | Path | Friction | Fix |
|-------|------|---------|-----|
| Discover | marketplace 검색 또는 친구 추천 | claude-code dep marketplace listing 미표시 | auto-add: "Works with Claude Code (free plugin)" first-line + 1-line install summary |
| Install | `npx @claude-design/install` | claude-code 미설치 시 안내 미정 | auto-add: install script 가 claude-code missing 감지 → guide URL |
| Hello World | `claude-design naming demo` | sample vs own file 구분 미명시 | auto-add: demo = read-only sample, "your own" 명령 별도 |
| Real usage | `claude-design naming apply --figma <url>` | figma token wizard 부재 | auto-add: first-run wizard `claude-design auth figma` interactive |
| Debug | Error message UX | Phase 3 의 D-01/C-01 시 format 미정 | auto-add: **Tier 1 (Elm-style)** — 문제 + 원인 + fix + docs URL. example: `Error: Element ID collision. Existing layer 'home__hero__cta' conflicts. Try '--on-collision=suffix' or 'claude-design naming disambiguate --interactive'. See https://.../collision` |
| Upgrade | claude-design v1 → v2 (B 추가) | breaking change policy 미정 | auto-add: SemVer + 6mo deprecation + codemod for naming-pattern 변경 |

**First-Time Developer Roleplay (Anchor-A)**

```
T+0:00  marketplace listing 클릭. "Works with Claude Code (free)" — 친구 추천 했으니 진행.
T+0:30  "Install Claude Code" 링크. anthropic.com. npm install 명령.
T+2:00  `npm install -g @anthropic-ai/claude-code` 성공.
T+3:00  `npx @claude-design/install`. plugin 자동 설치. demo 명령 안내.
T+3:30  `claude-design naming demo`. sample → before/after gif 또는 terminal 렌더.
T+5:00  본인 figma `claude-design naming apply --figma <url>`. token wizard 시작.
T+8:00  token 발급. apply 실행. 5 element 자동 명명.
T+10:00 본인 figma layer tree 확인 — 자동 명명 layer 보임. **"오 와, 진짜다"** moment.
T+11:00 collision 발생. disambiguation prompt-back. resolve.
Final: 성공 + 다음 prompt session 보존 — B 의 가치 직접 체감.
```

**8 Passes 점수**

| Pass | Score | Fix |
|------|-------|-----|
| 1 Getting Started | 3 → 7 | install 자동화 + token wizard + demo. Competitive tier 달성. |
| 2 API/CLI design | 5 → 8 | `claude-design <action> <noun>` convention (`apply`/`demo`/`auth`/`disambiguate`/`session`) |
| 3 Error messages | 2 → 8 | Tier 1 Elm-style 강제 — 모든 error = 문제 + 원인 + fix + docs |
| 4 Documentation | 4 → 7 | README install/quickstart/troubleshoot/recipes 4-섹션 (QUICKSTART.md 이미 존재) |
| 5 Upgrade path | 3 → 7 | SemVer + 6mo deprecation + codemod |
| 6 Dev environment | 6 → 8 | CI matrix Mac/Linux/Windows |
| 7 Community | 5 → 6 | claude-design-skill issue tracker 존재. 별도 채널 미정 — **taste** |
| 8 DX measurement | 1 → 5 | opt-in anonymous TTHW telemetry — **taste**: opt-in vs default-on |

**DX 스코어카드**

| 차원 | Score |  | Field | Value |
|------|-------|---|-------|-------|
| Getting Started | 7/10 |  | TTHW | 5 min (Competitive) |
| API/CLI/SDK | 8/10 |  | Magic vehicle | B (copy-paste demo) |
| Error Messages | 8/10 |  | Mode | POLISH |
| Documentation | 7/10 |  | Product Type | claude-code sub-skill |
| Upgrade Path | 7/10 |  | Overall DX | **6.6/10** |
| Dev Environment | 8/10 |  | | |
| Community | 6/10 |  | | |
| DX Measurement | 5/10 |  | | |

**미해결 결정 (Phase 4 후보)**

| Decision | If deferred | Recommendation |
|----------|-------------|----------------|
| TTHW telemetry opt-in vs default-on | adoption 측정 불가 | **taste** → Phase 4 |
| Community 채널 (Discord vs github discussions vs 미설치) | designer 도움 채널 미정 | **taste** → Phase 4 |
| Per-seat pricing anchor ($29 / $39 / $49 / mo) | per-seat ICP anchor 가격 부재 | **taste** → Phase 4 |
| Standalone Figma plugin (Champion tier 달성) | TTHW <2min 불가 | DEFER (PMF 후, Phase 1 의 C defer 와 align) |

**Phase 3.5 → Phase 4 핸드오프**: 4 taste decision + 0 user challenge.

---

<!-- AUTONOMOUS DECISION LOG -->
## Decision Audit Trail

| # | Phase | Decision | Classification | Principle | Rationale | Rejected |
|---|-------|----------|----------------|-----------|-----------|----------|
| 1 | Phase 0 | UI scope = yes (3 grep hits) | mechanical | — | PROCEDURE Step 3 trigger | — |
| 2 | Phase 0 | DX scope = yes (9 grep hits) | mechanical | — | PROCEDURE Step 3 trigger | — |
| 3 | Phase 0 | Restore point @ `docs/.autoplan-backups/2026-05-20-validate-idea-ai-figma-context-bridge.20260521140101.md` | mechanical | — | PROCEDURE Step 1 | — |
| 4 | Phase 0 | Single-voice (외부 voice 미구성) | mechanical | — | best-effort fallback | dual-voice |
| 5 | Phase 1 | Mode = SELECTIVE EXPANSION | mechanical | — | autoplan default | EXPANSION / REDUCTION |
| 6 | Phase 1 | **P1~P4 hold + 진행** | user-decided | — | user 명시 (2026-05-21) | re-scope / Stage 2 first |
| 7 | Phase 1 | A → B sequence ACCEPT | mechanical | P1 + P3 | doc line 100, wedge | — |
| 8 | Phase 1 | C DEFER to month-6 gate | mechanical | P2 (감당가능 범위) | XL 6-12mo, blast radius 밖 | C first-bet |
| 9 | Phase 1 | The Assignment ACCEPT-FIRST | mechanical | P1 (완성도) | wound vs itch 판별 obligation | skip |
| 10 | Phase 1 | Figma MCP write API mapping ACCEPT (Phase 3 prereq) | mechanical | P1 | F-01 mitigation | defer |
| 11 | Phase 1 | Naming rejection fallback DEFER to Phase 2 | taste | P5 | design 결정 — Phase 2 적합 | Phase 1 inline |
| 12 | Phase 1 | Pricing model DEFER to Phase 3.5 | mechanical | P3 | DevEx 영역 | — |
| 13 | Phase 1 | TAM 측정 DEFER (post-PMF) | mechanical | P6 (action 편향) | wedge sharpness PMF 후 정확도 더 높음 | — |
| 14 | Phase 1 | C first-bet REJECT | mechanical | P2 + P4 | 플랫폼 신기루 — doc 자체 진단 | — |
| 15 | Phase 2 | Pass 4 (AI Slop) skip | mechanical | P6 | doc 에 graphical UI spec 없음 | full pass |
| 16 | Phase 2 | Pass 6 (Responsive/A11y) N/A | mechanical | P6 | CLI/MCP tool, viewport 부재 | — |
| 17 | Phase 2 | §S2-states auto-added (6 states) | mechanical | P5 (explicit) | 구조적 gap auto-fix | — |
| 18 | Phase 2 | §journey storyboard auto-added | mechanical | P5 | 구조적 gap auto-fix | — |
| 19 | Phase 2 | Naming pattern `<page>__<section>__<element>__<variant>` auto-decision | mechanical | P5 | Figma slash convention 회피 — naming 안전성 | dot-separated / underscore-only |
| 20 | Phase 2 | Disambiguation surface (Figma panel vs terminal vs web) DEFER | taste | — | designer 어디서 결정? — Phase 4 게이트 | — |
| 21 | Phase 2 | Naming character set (Latin vs Unicode) DEFER | taste | — | Korean designer 대응 — Phase 4 | — |
| 22 | Phase 3 | D-01 atomic write — verify + diff log + rollback script | mechanical | P1 (완성도) + P5 | partial failure mitigation | "Figma가 알아서 해결" |
| 23 | Phase 3 | C-01 session TTL = 5 min + explicit reset | mechanical | P5 (explicit) | designer thinking time | longer/shorter TTL |
| 24 | Phase 3 | R-01 multi-user share session DEFER | taste | P6 | post-PMF 영역 | — |
| 25 | Phase 3 | P-01 token budget +<2% 증분 목표 + 측정 점 명시 | mechanical | P1 | 측정 가능 design | "측정 안 함" |
| 26 | Phase 3 | P-02 batch figma write API | mechanical | P5 | N+1 회피 | per-element write |
| 27 | Phase 3 | A-01 neuf MCP server (Figma MCP fork 회피) | mechanical | P5 (explicit > clever) | upstream sync 부담 회피 | fork |
| 28 | Phase 3 | A-02 distribution = claude-design-skill sub-skill | mechanical | P4 (DRY) | 신규 plugin listing 회피 | 별도 plugin |
| 29 | Phase 3 | Test plan = 4 test files (resolver/session/collision/integration) | mechanical | P1 (완성도) | review-engineering Section 3 명시 | "구현 시 결정" |
| 30 | Phase 3 | Regression rule — 기존 108 tests CI block | mechanical | — | PROCEDURE mandatory | — |
| 31 | Phase 3 | Architecture deep-module ✓ (A) + ✓ (B) | mechanical | P5 | 4-criteria 평가 통과 | re-design |
| 32 | Phase 3.5 | Persona = Series A lead designer (3-5 team) | mechanical | P6 | doc line 21-22 anchor (Anchor-A) | indie founder / OSS contributor |
| 33 | Phase 3.5 | TTHW target = Competitive (2-5 min) | mechanical | P5 + P2 | Champion 은 multi-quarter (P2 위반) | Champion / Needs Work |
| 34 | Phase 3.5 | Magical moment vehicle = B (copy-paste demo) | mechanical | P5 | CLI 도구 low-effort high-impact | playground / video |
| 35 | Phase 3.5 | Error message Tier 1 (Elm-style) 강제 | mechanical | P1 | 문제 + 원인 + fix + docs | Tier 2 / 3 |
| 36 | Phase 3.5 | SemVer + 6mo deprecation + codemod | mechanical | P5 | upgrade path 표준 | break free |
| 37 | Phase 3.5 | TTHW telemetry opt-in vs default-on DEFER | taste | — | privacy vs measurement trade-off | — |
| 38 | Phase 3.5 | Community channel DEFER | taste | — | designer 어디서 도움? | — |
| 39 | Phase 3.5 | Per-seat pricing anchor DEFER | taste | — | wedge ship 후 결정 | — |
| 40 | Phase 3.5 | Standalone Figma plugin DEFER (PMF 후) | mechanical | P2 | Phase 1 C defer 와 align | — |

**Cross-Phase Theme**

- **Theme — Figma MCP write API 한계가 critical-gap 의 single point**: Phase 1 (F-01), Phase 3 (D-01 atomic write + R-01 concurrency), Phase 3.5 (Pass 3 error UX) 가 같은 root cause 의 다른 표면. **고신뢰 신호** — Figma MCP write capability mapping 이 *코드 작성 전 single largest unknown*.
- **Theme — The Assignment 미실행 obligation**: Phase 1 (P2 + F-04) + Phase 3.5 (TTHW 측정 baseline 부재) — 동일 origin. behavioral data 없이 paid PMF 측정 불가 + wedge sharpness 가설 검증 불가.

---

## APPROVED — Phase 4 게이트 통과 (2026-05-21)

**User 결정**: A) As-is 승인 (추천 모두 수락) — 6 taste decisions 모두 recommended option 채택.

**Taste decisions 확정**

| Choice | 결정 | Phase | 비고 |
|--------|------|-------|------|
| 1. Disambiguation surface | **Figma plugin panel** | 2 | designer 가 figma 안에 있을 때 contextual. B 의 4주 scope 안. |
| 2. Naming character set | **Latin + 숫자 + `_`** | 2 | NFC 부담 회피. Korean designer 의 layer name 자체는 한글 OK (id 만 Latin). |
| 3. Multi-user share session | **DEFER post-PMF** | 3 | 개인 designer 단위가 first wedge. |
| 4. TTHW telemetry | **opt-in with prominent prompt** | 3.5 | privacy 민감도 존중. |
| 5. Community 채널 | **Github discussions only (ship 단계)** | 3.5 | claude-design-skill repo 활용. Discord = post-ship. |
| 6. Per-seat pricing anchor | **$39/mo per seat** | 3.5 | doc range 중간. Series A 3-5 seat = $117-195/mo clear value. |

**Audit trail 추가 (#41~#46)** — 위 6 결정 모두 user-decided (Phase 4 게이트, A) recommendation 채택. Classification = user-decided. Principle reference = 각 Choice 의 recommended option rationale.

**TODOS 작성**: `docs/TODOS-autoplan.md` 생성됨 (deferred items + pre-implementation prereq 의 작업 punch list).

**Next workflow step (PROCEDURE 핸드오프 규칙 — auto-invoke 금지, 사용자 명시 확인 필요)**:
1. **PRE-IMPLEMENTATION (block)**: ① The Assignment 실행 (Anchor-A 미팅 + 1-week RescueTime/Toggl trial) · ② Figma MCP write API 1-day mapping spike. *코드 시작 전 의무*.
2. **Stage 2 권장 (별 세션)**: `/buddy:validate-advanced-edge-idea` — edge case + hidden assumption grilling. doc line 161 자체 권장.
3. **Implementation plan**: Assignment 결과 가져온 뒤 `/buddy:plan-build` — A approach 의 3-5일 task graph + parallel execution plan.

---

## Validate-Advanced-Edge-Idea Grilling (2026-05-21)

> `/buddy:validate-advanced-edge-idea` 실행 결과. 5 압박 차원 중 D5 (Ethical Blind Spot) + D2 (Second-Order Effect) 2 차원 진행. D1/D3/D4 미수행 (별 session 또는 후속 진행 결정).

### D5 Findings (Ethical Blind Spot — closure)

| Q | Resolution | Strength |
|---|------------|---------|
| Q1.a — Founder=anchor user 충돌 | bias 통제 *3중* (작업관리 툴 자동 측정 + aggregate-only 결과 가시성 + 본인 과거 baseline) | ✓ valid |
| Q1.b — AI 사용 전/후 작업 단위 | "디자인 완성 컨펌된 deliverable" (예: 랜딩페이지 1개) — 컨펌 외부 기준이 quality 자동 반영 | ✓ valid |
| Q1.c — Standard drift | 동일 리드 디자이너 (이론+경험) + 현재 AI vs 사람 구분 명확 (blind test 자연) | ✓ valid at baseline |
| Q1.d — Means vs Ends | 모순 아님 — PROCEDURE narrowest-wedge 강제. *North Star 명시 누락* → §North Star 보강 완료 | ✓ resolved |

### D2 Findings (Second-Order Effect — closure)

| Q | Resolution |
|---|------------|
| Q1 — Skill erosion vs Moving target | **γ Hybrid (judgment 분리)** — North Star 의 "구분 불가" = creation 결과물 한정. judging + verbalization 은 사람 고유 |
| Q2 — Atrophy mechanism (vs GPS/계산기) | **M1 + M2 combined** — (M1) creation skill atrophy 수용 + judging skill 유지/강화 / (M2) Selection+instruction UI 가 verbalization skill 강제 운동 → upgrade |

### Boxed Edge Cases

```yaml
- dimension: ethical_founder_bias
  case: "사내 디자이너 그룹 + Founder self-use evidence chain bias"
  response: "작업관리 툴 자동 측정 + aggregate-only 결과 + 본인 과거 baseline"
  test_method: "PRE-01 trial 시점 사내 그룹도 동일 measurement 적용"

- dimension: ethical_standard_drift
  case: "AI 도입 전/후 컨펌 standard drift"
  response: "동일 리드 디자이너 + 이론 기반 standard + DESIGN.md align"
  test_method: "6-month gate 컨펌자 동일성 + AI 가시성 통제 (가능시 blind sample)"

- dimension: second_order_skill_erosion
  case: "Creation atrophy 가 judging+verbalization 강화로 상쇄"
  response: "γ Hybrid thesis — 3 skill 분리 자동화/강화"
  test_method: "month-3 데이터 컨펌 round 수 + prompt 정밀도 시계열. baseline 정의 우선 필요."
```

### Assumption Ledger

```yaml
- assumption: "Layer creation skill atrophy 가 judging+verbalization skill 강화로 net positive"
  confidence: medium
  test_required: "month-3 PMF 데이터의 컨펌 round 수 단축 + prompt 정밀도 향상 패턴"
  deadline: 2026-08-21 (PRE-01 trial 후 3mo)
  impact_if_false: "figma 외부 design 증가 → claude-code lock-in negative → 6-month retention 약화"

- assumption: "리드 디자이너 컨펌 standard 가 AI 도입 후에도 일관 유지"
  confidence: high
  test_required: "AI 사용 여부 가시성 통제 (blind sample 일부 포함 권장)"
  deadline: 2026-06-21 (PRE-01 시점)
  impact_if_false: "시간 measurement 의 lenient/strict bias → wedge PMF signal 왜곡"

- assumption: "(d') 의 세 layer 가 함께 작동해야 means → ends 인과"
  confidence: high (사용자 명시 — D2 grilling)
  test_required: "A ship (layer 1+3 만) 결과 — UI selection (layer 2) 없이도 AI 의도 이해율 충분한지"
  deadline: 2026-06-28 (A ship 후)
  impact_if_false: "B approach 의 UI selection layer 가 wedge 핵심 — A 만으로 PMF signal 약함. B 우선순위 재고."
```

### Remaining Ambiguity (구현 시 주의)

- Judging skill 측정 baseline — "여러 케이스 누적" 으로 지연. trial 시점 instrument 안 하면 6-month gate 에서 retroactive 측정 불가.
- Verbalization skill 측정 — prompt 정밀도 정량 지표 미정.
- D1 / D3 / D4 차원 grilling 미수행 — autoplan Phase 1/3/3.5 가 일부 cover. 별 session 권장.

### D3 Findings (Failure Mode — closure)

| Q | Resolution |
|---|------------|
| Q1 — 시간차 silent loss (Designer A stale + Designer B 수동 변경 race) | **β + scan-on-restart**: 매 작업 시작 시 timestamp 비교 → mismatch 면 figma 전체 scan + refresh. *git fetch* 모델 transfer. CLI 텍스트 알림 (시각적 disambiguation UI 불필요) |
| Q2 — Concurrent in-flight (multi-device 동시 prompt) | **α (CLI lock)**: 다중 device 동시 작업은 사용자 책임. lock acquisition + "session locked by [host/timestamp]" 텍스트 알림. CLI first-run 의 한 번 disclose |
| Q2-finding — 충돌 의 진짜 granularity | **페이지 단위** — 다른 페이지 동시 작업은 normal multi-collaboration (충돌 아님). collision detector 가 *page-scoped* 작동 → autoplan R-01 보다 narrow 한 design |

### D3 Plan B (Strategic Architectural Fallback) — *사용자 explicit 강조*

> **Figma MCP 의 지원 범위가 부족할 경우 (PRE-02 의 spike 결과에 따라):**
> - Figma 의 native plugin 시스템으로 *Figma plugin 직접 구현*
> - Plugin 과 호환되는 *자체 MCP server* 구현 (claude-code ↔ figma plugin bridge)

| 항목 | Plan A (default) | Plan B (fallback) |
|------|-----------------|-------------------|
| 의존성 | Figma MCP plugin (external) | 자체 plugin + 자체 MCP server |
| Effort | M (2-4주 — autoplan B approach) | L (1-2개월, plugin learning + MCP impl) |
| Distribution | claude-design-skill sub-skill | + Figma plugin marketplace listing |
| Trigger | default 진행 | PRE-02 결과 = "MCP 지원 부족" 일 때 |

### Boxed Edge Cases (D3 추가)

```yaml
- dimension: failure_mode_silent_loss
  case: "Designer 의 stale session cache vs figma 외부 변경 race"
  response: "scan-on-restart: timestamp 비교 + mismatch 시 figma 전체 scan + refresh + CLI 텍스트 알림"
  test_method: "PRE-02 spike 시 figma timestamp granularity 확인 (file-level vs layer-level vs page-level)"

- dimension: failure_mode_concurrent_inflight
  case: "Multi-device 동시 prompt 실행 race"
  response: "CLI lock (1 device only) + first-run 한 번 disclose"
  test_method: "lock acquisition / release timeout / 강제 release UX 의 trial 사용자 acceptance 확인"

- dimension: failure_mode_collision_granularity
  case: "충돌 의 진짜 단위 = 동일 페이지 동시 작업. 다른 페이지면 normal collaboration"
  response: "collision detector 의 page-scoped 작동"
  test_method: "figma timestamp 가 page-level 지원하는지 PRE-02 spike"
```

### Assumption Ledger (D3 추가)

```yaml
- assumption: "Figma 의 timestamp granularity 가 *page-level* 지원"
  confidence: medium (PRE-02 spike: 공식 docs 에 명시 안 됨 — U-02. mitigation 있음 — page-level 미지원이어도 layer name 비교로 fallback)
  test_required: "PRE-01 trial 시작 시 `get_metadata`/`get_design_context` 응답 JSON 의 lastModified/version 필드 inspect"
  deadline: 2026-05-28 (PRE-01 시점)
  impact_if_false: "file-level fallback → false positive 증가 (UX cost minor). Plan B 트리거 안 됨"

- assumption: "Figma MCP 의 지원 범위가 wedge 의 필요 op 를 커버"
  confidence: **high** (PRE-02 spike 통과 — hard gates #1, #7 모두 PASS. `use_figma` + `generate_figma_design` 이 본 wedge 의 write op cover)
  test_required: "✓ 완료 — `docs/2026-05-21-figma-mcp-inventory.md` 참조"
  deadline: 2026-05-21 ✓ (PRE-02 완료)
  impact_if_false: "n/a — 통과"

- assumption: "ICP (Series A 디자인 팀) 가 Figma Professional+ plan + Dev/Full seat 보유"
  confidence: high (사용자 명시 — 2026-05-21 PRE-02 결과 게이트)
  test_required: "PRE-01 미팅 시 Anchor-A 의 Figma plan + seat type 확인"
  deadline: 2026-06-21 (PRE-01)
  impact_if_false: "Starter/View/Collab seat 만 보유 시 월 6 write call 제한 → trial 자체 불가. ICP 재정의 또는 Anchor-A teams Figma 권한 확인"

- assumption: "본 wedge 가 thin wrapper 로 narrow 해진 후에도 paid commitment ($39/mo per-seat) 의 가치 명제 valid"
  confidence: medium (PRE-02 의 wedge sharpness 재산정 — *주변 friction 제거* 수준의 differentiation 이 paid 임. PRE-01 trial 데이터로 검증 필요)
  test_required: "PRE-01 Anchor-A trial 의 Venmo response — 3 piece (session/collision/naming) 만으로 paid commitment 의향 측정"
  deadline: 2026-06-21
  impact_if_false: "differentiation 약화 → free tier 으로 후퇴 또는 wedge 재구성 (figma-power 와의 differentiation 영역 재정의)"
```

### Verdict — **proceed-with-caveat**

- D5: bias 통제 valid, standard drift 의 6-month 재평가 필요
- D2: γ Hybrid thesis 채택, 측정 baseline 의 trial 시점 instrument 필요
- D3: scan-on-restart + CLI lock + page-level collision granularity. Figma MCP 의 unknown 영역 = **PRE-02 spike 의 single largest decision point** (Plan A vs Plan B 결정)
- 미수행 차원 (D1/D4): autoplan 의 Phase 1/3.5 가 부분 cover. 별 session 권장.

### PROCEDURE 압박 평가

- "최소 2회 '모르겠다' / '검토 안 했다' 끌어내야 충분 압박" — **달성** (D2 Q1 "여러 케이스 누적" + D3 Q2 "Figma MCP 지원 모름")
- 사용자 답 quality — D5/D2/D3 모두 sharp + structural specificity 강제 충족 (이름 의존 0)
- Doc 보강 4건 — North Star / 확장 (d') / D5+D2+D3 findings / Plan B + assumption ledger
