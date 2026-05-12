# Dogfood Log Template

> **목적**: A-01 · A-02 · A-03 dogfood 시나리오의 *공통 schema*. 모든 log가 같은 5개 섹션을 따른다 → A-04 (`feedback-backlog`) 합성이 grep + section-by-section diff로 자동화 가능.
>
> **사용법**:
> 1. 이 파일을 `01-nft-card-spec.md` / `02-figma-mcp-smoke.md` / `03-codex-e2e-smoke.md`로 복사
> 2. 5개 H2 섹션은 *제목 그대로 유지* (rename 금지) — A-04 합성기가 section 헤딩으로 파싱
> 3. 빈 섹션은 `_(none)_` 로 명시 (생략 금지)

---

## scenario

*무엇을 / 왜* — 한 단락 (3~5문장). adopter 입장에서 본 시나리오의 의도, 가설, 입력 자료.

예: "NFT 카드 컴포넌트 사양 작성. Figma 없이 SKILL의 4-stage workflow가 어디까지 도달하는지 확인."

## steps

번호 매긴 *행동* — 명령어, 클릭, 파일 편집 순서. 재현 가능하게.

```
1. `python3 scripts/init-brand.py --example` 실행
2. `team-brand-spec.json` 의 `team.company` 를 "Default Studio" → "<own>" 으로 교체
3. SKILL.md §4-stage workflow 의 step 1 (assumptions) 부터 순서대로 실행
4. ...
```

각 step은 1줄. 부연이 필요하면 sub-bullet (`  - ...`).

## observed

*무엇이 실제로 일어났는가* — 기대 vs 실측. 예상 밖 동작·출력·error.

- Expected: `init-brand.py --example` 가 `team-brand-spec.json` 생성
- Actual: ✅ 생성됨. 단 `_source` 필드가 status colors에만 있고 surface/text에는 없음
- Captured artefacts: `<path>` (mockup PNG, console output, etc.)

## friction

*잘 안 되었거나 추가 학습이 필요했던 지점* — adopter 관점의 마찰점. P0/P1/P2 라벨 부여.

**Priority rule**: *install path 단계 (clone / marketplace add / plugin install / config drop-in / brand stamp 직전까지)에서 발생한 마찰은 무조건 P0*. install이 막히면 adopter는 *first deliverable에 도달하지 못한다* — magical moment 자체가 차단되므로 P0. 그 뒤 단계의 마찰은 시나리오 영향도로 P1/P2.

| ID | priority | description | suggested fix |
|----|----------|-------------|---------------|
| F-01 | P1 | `init-brand.py --example` 와 `--default` 가 동일 동작인지 명시 안 됨 | README §Quickstart에 alias 한 줄 추가 |
| F-02 | P2 | ... | ... |

마찰 없으면 `_(none)_`.

## score

Anti-AI-slop self-score (0~5, 낮을수록 좋음). SKILL.md §Anti-AI-slop 의 5개 criterion 각각:

| criterion | hit (0/1) | note |
|-----------|-----------|------|
| 1. 일반론 / cliché | | |
| 2. 검증되지 않은 주장 | | |
| 3. 구체 evidence 부재 | | |
| 4. 부풀린 어휘 | | |
| 5. AI artifact (uncanny pattern) | | |
| **total** | **N** | threshold: < 3 PASS |

---

## A-04 합성 시 사용 grep recipe

```bash
# 모든 dogfood log의 friction을 한 번에 수집
grep -h "^| F-" docs/dogfood/0?-*.md | sort -t'|' -k3
# priority별 그룹핑
grep -h "^| F-" docs/dogfood/0?-*.md | awk -F'|' '{print $3}' | sort | uniq -c
```

A-04 acceptance에서 `PROJECT-PLAN.md §7` 결정 로그에 들어가는 backlog는 위 grep 결과를 그대로 1차 후보로 삼는다.
