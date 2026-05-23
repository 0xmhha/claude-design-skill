---
name: pii-anonymization-git-safety
description: 산출 문서에 anchor 인물 실명 등 PII 금지 — placeholder identifier 사용. grilling skill (validate-idea / validate-advanced-edge-idea / office-hours) 적용 시에도 specificity 단위를 이름 아닌 행동/시점/구조로 재정의.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6e51cb1c-fe1e-4fd6-a646-22f35d674b01
---

문서 작성 시 anchor 인물의 *실명* 을 직접 기재하지 않는다. Placeholder identifier — `Anchor-A`, `Anchor-B`, ... — 또는 generic role 호칭 ("lead designer", "엔지니어") 로 대체.

**Why**: 사용자 명시 발언 (2026-05-21) — "개인정보이기때문에 git 에 commit 할수 없어". idea validation / planning 문서는 git tracked 위치 (`docs/`) 에 작성되는데 PII 가 들어가면 *사후 redaction* 필요. 사전 placeholder 가 cheaper + 누락 risk 0.

**How to apply (문서 작성)**:
- `/buddy:validate-idea`, `office-hours`, `/buddy:concretize-idea` 류 idea-stage skill 실행 시 anchor 인물 이름 등장하면 placeholder 사용.
- *Anchor identifier* 가 의미상 필요한 위치는 placeholder 도입 ("Anchor-A", "Anchor-B"). 일반 role 호칭은 "디자이너" / "엔지니어" 그대로.
- 회사 식별 가능 정보 (정확한 startup 이름, "전 동료 — 1 주 전 주말 만남" 같은 시점·관계 단서) 도 generic 화 가능하면 generic 화.
- 동시에 `.gitignore` 에 `docs/.autoplan-backups/` 같은 임시 backup 경로 추가 — pre-mutation snapshot 도 보호.

**How to apply (grilling skill 적용 시 framing 재정의)** — 2026-05-21 추가:
- PROCEDURE (예: `validate-idea` line 257 "Sarah, 50명 logistics 회사 ops 매니저") 가 *이름 + 직함* 을 specificity default 로 가정 → PII 익명화된 doc 에선 framing 충돌.
- **재정의**: specificity = *이름* 이 아니라 *행동* (어느 도구, 어느 단계, 어느 metric) + *시점* (언제, 얼마나 자주) + *숫자* (분/시간/% 단위 측정값) + *관계 구조* (power asymmetry / bias / sample 구성).
- "익명화로 evidence 가 약해진다" 류 grilling push **금지** — fingerprint 만 제거, 구조는 그대로.
- 적용 예시: "사내 디자이너 그룹 (founder power 영향권)" + "20h/week self-report" + "1-week RescueTime/Toggl trial" 은 이미 충분 specific. 추가 이름 요구는 PII 규칙 위반.
- Anti-pattern 회피: "Anchor-A 의 실제 이름은?" / "사내 그룹 구성원이 누구?" / "구체적 회사명?" 같은 질문 자체가 PII 강제 — 절대 사용 금지.

**관련 작업물** (2026-05-21 세션):
- `docs/2026-05-20-validate-idea-ai-figma-context-bridge.md` — "세민" → "Anchor-A" placeholder 도입 + 회사 식별 정보 generic 화.
- `docs/.autoplan-backups/` — `.gitignore` 추가됨.
- grilling skill 적용 사례 — D5 Ethical Blind Spot 의 founder=anchor 충돌 grilling 을 이름 비의존 framing 으로 진행.
