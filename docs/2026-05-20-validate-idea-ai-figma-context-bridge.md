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
- **Sibling internal designers**: 본인 회사 내 디자이너들이 *동일 survey 응답*. Follow-up 가능
- **Named anchor**: **세민**, web3 research startup lead designer (전 동료, 1 주 전 주말 직접 만나 들음). Team: 3 designer + 1 full-stack dev. Post Series A. 새 브랜딩 + 주 2 건 publishing + frontend code 도 lead designer 가 챙기는 시도 → **2 달 이상 초과 근무**
- **Measured cost**: claude-design-skill 에서 *간단한 wireframe 1 회 생성* = token limit 의 9%. 즉 ~11 wireframes / session — 1 프로젝트도 session 안에 못 끝냄
- **Self-reported time waste**: 20h/week (methodology = self-report only — *behavioral observation upgrade* obligation 으로 P2 에 기록)

---

## Status Quo

**Designer workflow** (세민 + 사내 디자이너들의 보고):
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

**Anchor user**: 세민 — web3 research startup lead designer, 3 designers + 1 full-stack engineer team, post Series A. KPI = 브랜딩 완성도 (실패 시 투자 철회 risk). Velocity-focused boss. 매일 9-11 am 가 *AI 도구 base 시도 → 만족 안 되어 figma 수작업* 시간대.

**Persona split** (Q3 에서 surface):
- Primary: lead designer at Series A startup (1-5 designer team)
- Secondary: engineer doing product building (founder 본인)
- Hybrid possible: 세민 case 처럼 lead designer 가 frontend code 도 시도 — *single-product-for-hybrid-persona* 가설

**Wedge — (d') AI prompt ↔ Figma MCP context binding 자동화**:
- *Project/page/element triplet* 의 implicit resolution (session state)
- Naming convention 강제 (globally unique element id)
- Naming collision 발생 시 *visual disambiguation* prompt-back
- Sub-feature (d): AI 출력 element 이름 → figma layer 이름 자동 적용 (independent ship-able)

---

## Premises

User agreed (2026-05-20):
1. **P1 — Demand**: web3/game vertical designer (survey 80% + 세민 verified). Primary = lead designer at Series A startup. Secondary = engineer doing product building.
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

**Rationale**: A 의 3-5 일 ship 이 *세민 + 사내 2 명 실 trial* 데이터 확보 (P2 의 behavioral observation upgrade obligation 직접 충족). 2 주 내 B 의 context binding 추가. 3-6 개월 paid user growth + churn 측정 후 C 의 tool-neutral 베팅 평가. C 를 first-bet 으로 가는 건 *플랫폼 신기루 의 가장 위험한 변형* (6 개월 burn 없이 validation 0).

---

## Open Questions

1. **Figma MCP API 의 write 권한 한계** — 어느 ops 가능 / 불가능? B 의 4 주 ship 범위에 직접 영향. 답 없으면 B 의 effort 추정이 틀릴 risk
2. **P2 의 behavioral observation upgrade** — 세민 또는 사내 디자이너 1 명의 1-week RescueTime/Toggl trial 은 누가, 언제 진행? *The Assignment* 의 핵심
3. **Series A web3/game startup TAM 측정** — 세민 같은 ICP 의 모수가 wedge sharpness 의 trade-off 결정
4. **Naming convention 수용성** — A ship 후 첫 trial 사용자가 naming convention 거부하면 B 의 wedge 약화. 거부 시 fallback design?
5. **C 의 thesis disruption risk** — Figma 의 향후 12 개월 AI roadmap 공지 시점 = C 의 contrarian validity 의 가장 큰 위협

---

## Success Criteria

| Phase | Window | Metric | Pass |
|-------|--------|--------|------|
| **Week 1 (A ship)** | 3-5 일 | 세민 + 사내 2 명 = 3 trial users *used ≥ 1 회* | 3/3 |
| **Week 2-4 (B ship + first $)** | 2-4 주 | Per-seat paid commitment ≥ 1 / 3 at $29/mo | ≥ 1 |
| **Month 3 (PMF signal)** | 3 개월 | 10 paid seats ($290/mo) | ≥ 10 seats |
| **Month 6 (C decision gate)** | 6 개월 | 30 paid seats / 80%+ retention 3 개월 | C bet justified iff $1000/mo + retention > 80% |

---

## Dependencies

- **Figma MCP API** (external, 권한 한계 not under control)
- **claude-design-skill repo** (own codebase, 자유 수정 가능)
- **Claude API token cost** (per-prompt cost — pricing floor 결정 변수)
- **세민의 actual trial 동의** (현재 no commitment — *The Assignment* 가 직접 target)

---

## The Assignment

**이번 주 — 세민 미팅 1 회**. 30 분. 3 specific asks:

1. **1 주 trial 동의 받기**: RescueTime / Toggl 측정값을 next session 에 가져옴. P2 의 behavioral observation upgrade 직접 충족.
2. **(A) paper mockup 보여줌**: 1 page. "layer naming AI 출력 → figma 자동 적용" before/after gif. 세민이 *"Venmo 보내고 싶은지"* 직접 반응 측정.
3. **세민의 layer naming + context binding 정확 pain 의 단계별 walkthrough recording** (또는 자필 메모) 동의.

**Outcome**: meeting 후 다음 cycle-3 §B.1 update — 세민 trial 데이터 + paper mockup 반응. 만약 *"Venmo"* 응답 → (A) 빌드 start. *"not exactly"* 응답 → wedge re-formulate.

---

## What I noticed

- 사용자가 *"figma mcp 를 통해 font 변경도 수행되지 않는 문제"* 정확 phrasing — 일반적 "figma 연동 어려움" 이 아닌 **single API operation 의 specific failure**. 그 specificity 가 wedge root cause analysis 가능하게 만든 핵심.
- Q3 에서 *"예시 거의 그대로"* 답 인정한 뒤 *"추가로 더 입력하면, 세민..."* 으로 self-correct — escape hatch + voluntary follow-up. Founder 가 anti-sycophancy 의 의도 *이해했음* 의 unfakeable 증거. Mimicry → real anchor 의 *한 발화 회수* 가 본 세션의 가장 강한 signal.
- Q5 의 *"매번 입력해주고 있어서 놀라웠으며"* 의 *"놀라웠으며"* 단어 — 사용자가 *예상* 한 것과 *경험* 한 것 사이 gap 을 본인이 정확히 명명. (d) → (d') wedge upgrade 의 진짜 entry point. PROCEDURE 의 "Gold: 제품이 설계 안 된 것 사용자가 하는 것" 정의 그대로 발동.
- *"이 두 가지 기능만 가능해도 나머지는 모두 확장이 개념이기 때문에 스켈레톤"* (Q4 답) — 플랫폼 신기루 진단의 솔직한 자료. Push 받은 후 (d) → (d') 로 narrow 함. *솔직한 reframe 능력* 이 founder 의 좋은 trait.

---

## 다음 단계 (핸드오프)

본 doc 의 입력 상태 = **"아이디어의 논리적 완결성 보완"** (구현 단계 무결성). PROCEDURE 의 handoff 표 per 본 case → `validate-advanced-edge-idea` (Stage 2). 단, cycle-3 §B.1 의 *Stage 1 만 우선* 결정 — validate-advanced-edge-idea 는 **별 세션 권장**.

**Recommended sequence**:
1. *이번 주*: The Assignment 실행 (세민 미팅) → behavioral observation 데이터 수집
2. *Next session* (Assignment 결과 가져온 뒤): `/buddy:validate-advanced-edge-idea` 진입 — edge case + hidden assumption grilling
3. *그 후*: 아래 둘 중 하나
   - 데모 가능한 prototype 시작 → A 의 3-5 일 build
   - 또는: concretize-idea Stage 3+ (`assess-business-viability`, `analyze-competition-and-substitutes`, `review-pricing-and-gtm`, `map-customer-segments`) 로 사업성 더 정제

핸드오프 규칙 (PROCEDURE 명시): "사용자에게 '다음 단계로 [skill] 을 invoke 할까요?' 형태로 명시 확인. **자동 전환 금지**."
