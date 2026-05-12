# 03 · Task Decomposition

> **목적**: `02-remaining-work-inventory.md`의 10개 항목을 *atomic task* (single-PR scope, single-actor 작업 단위, ≤ 2시간)로 분해.
> **task_id 규칙**: `{category}-{seq}-{slug}` (예: D-01-changelog-split, A-01-default-dogfood).

---

## task table

각 task의 필수 속성: `actor_track / estimated_hours / dependencies / acceptance`.

### D · Release engineering tasks

| task_id | title | actor_track | hours | dependencies | acceptance |
|---|---|---|---|---|---|
| **D-01-changelog-split** | CHANGELOG.md `[Unreleased]` 섹션을 `[1.0.0] · 2026-05-12`로 cut + Unreleased 비우기 | maintainer | 0.3 | — | CHANGELOG.md에 `## [1.0.0]` 헤더 존재, `## [Unreleased]` 헤더는 빈 placeholder 한 줄만 |
| **D-02-plugin-version-bump** | `.claude-plugin/plugin.json` `version: "0.1.0" → "1.0.0"` + `.claude-plugin/marketplace.json` plugins[0].version 동기 | maintainer | 0.2 | — | 두 JSON 파일 모두 `"version": "1.0.0"`, parse OK |
| **D-03-doc-version-bump** | README status line, HANDOFF active version, SKILL.md status 헤더, PROJECT-PLAN §6.5 모두 `1.0.0` 명시 | maintainer | 0.3 | D-01 · D-02 | 4 doc surface 모두 v1.0.0 명시, `grep "0.1.0"` 결과 0 |
| **D-04-git-tag-push** | `git tag -a v1.0.0 -m "..." && git push origin v1.0.0` | maintainer | 0.2 | D-01 · D-02 · D-03 commit 완료 | `git tag --list v1.0.0` 출력 + GitHub에 tag 노출 |
| **D-05-github-release** | `gh release create v1.0.0 --title "..." --notes-file <(awk '/## \[1.0.0\]/,/## \[/' CHANGELOG.md)` | maintainer | 0.3 | D-04 | GitHub release page에 v1.0.0 ship, notes에 CHANGELOG `[1.0.0]` 내용 포함 |
| **D-06-marketplace-ref-pin** | `references/figma-mcp-setup.md`와 `QUICKSTART.md`에서 plugin install 명령 옆에 *optional* `--ref v1.0.0` 안내 (어떻게 pinning하는지) | maintainer | 0.3 | D-04 | 두 doc에 `--ref` 옵션 명시, working tree clean |

D 총 6 atomic tasks · 1.6 hours · single PR로 묶을 수 있는 doc + manifest + git 작업.

### A · Adopter dogfooding tasks

| task_id | title | actor_track | hours | dependencies | acceptance |
|---|---|---|---|---|---|
| **A-01-default-dogfood-spec** | Default Studio identity로 *NFT 마켓플레이스 카드* 시안 1건 명세 (Junior Designer workflow 4-stage 적용) | user (designer) | 1.0 | D 카테고리 완료 권장 | docs/dogfood/01-nft-card-spec.md 작성: assumptions list, reasoning, placeholder mockup, anti-AI-slop self-score |
| **A-02-figma-mcp-smoke** | MCP server attached 환경에서 `figma_get_selection` → batch rename → component promotion 1 cycle | user (MCP env) | 1.5 | Figma MCP install 완료, 작업할 Figma 파일 준비 | 명시적 결과: dogfood log에 어느 단계가 작동·작동안함 기록 |
| **A-03-codex-e2e-smoke** | Codex CLI로 hero 이미지 1건 생성 + `codex-image-import.py` 통과 + (옵션) Figma 배치 | user (Codex env) | 1.0 | Codex CLI installed | dogfood log: PNG SHA-256, PROVENANCE.md entry, 마찰점 기록 |
| **A-04-feedback-backlog** | A-01·A-02·A-03 결과 마찰점을 `PROJECT-PLAN.md §7` decisions-log entry 또는 GitHub Issues로 변환 | maintainer | 1.0 | A-01·A-02·A-03 끝남 | 마찰점 N개 → Issue N개 또는 decisions-log entry 1개 |

A 총 4 tasks · 4.5 hours · 사용자 인풋 의존.

### C · Step 8+ optional enhancement tasks

| task_id | title | actor_track | hours | dependencies | acceptance |
|---|---|---|---|---|---|
| **C-01-codex-e2e-script** | `scripts/test_codex_e2e.py` — Codex CLI 환경 감지 + `codex` 호출 + import gate 1 cycle. CI에서는 `[ -z "$CODEX_TOKEN" ] && exit 0` 형식 conditional skip | maintainer | 2.0 | A-03 학습 | local dev에서 PASS, CI에서 skip 정상, dogfood 결과의 manual 단계 자동화 |
| **C-02-figma-mcp-smoke-script** | `scripts/test_figma_mcp.py` — `FIGMA_TOKEN` + sample file key 있을 때 MCP server를 직접 spawn해 tool list 검증. CI conditional skip | maintainer | 2.0 | A-02 학습 | local PASS, CI skip 정상, 회귀 자동 검출 |
| **C-03-usage-telemetry-adr** | `docs/plan/adr/001-usage-telemetry.md` — opt-in usage tracking 설계 ADR (privacy-first, no PII, no codename). 구현 X, ADR만. | maintainer | 1.5 | A-04 결과 | ADR 작성, status: proposed/accepted/rejected 명시 |

C 총 3 tasks · 5.5 hours. C-3은 ADR-only.

### B · Per-fork (verification-only)

이 repo *진행 X*. *현재 guide의 충분성만 verify*:

| task_id | title | actor_track | hours | dependencies | acceptance |
|---|---|---|---|---|---|
| **B-00-guide-coverage-check** | B-1 ~ B-6 각 항목에 대해 *대응 guide doc + 대응 명령어 예시* 존재 확인. checklist 1매. | maintainer | 0.5 | — | docs/plan/B-guide-coverage.md 작성, 6/6 ✅ 또는 missing 식별 |

B 총 1 task. 실 작업 X.

## 총 task 수

| 카테고리 | atomic tasks | hours |
|---|---|---|
| D · Release | 6 | 1.6 |
| A · Adopter | 4 | 4.5 |
| C · Enhancement | 3 | 5.5 |
| B · Guide check | 1 | 0.5 |
| **합계** | **14** | **12.1 hours** |

## task 단위 산출물

각 task가 만드는 결과는 *commit 또는 doc 또는 release event*:

- **D-01 ~ D-03** → 1 commit (`release: prepare v1.0.0`)
- **D-04** → git tag + push (별도 외부 effect)
- **D-05** → GitHub release (외부 effect)
- **D-06** → 1 commit (`docs: --ref v1.0.0 install option`)
- **A-01** → docs/dogfood/01-nft-card-spec.md 신규
- **A-02** → docs/dogfood/02-figma-mcp-smoke.md 신규
- **A-03** → docs/dogfood/03-codex-e2e-smoke.md 신규
- **A-04** → PROJECT-PLAN §7 entry 또는 GitHub Issues N개
- **C-01** → 신규 script + test + CI step
- **C-02** → 동일 패턴
- **C-03** → docs/plan/adr/001-usage-telemetry.md
- **B-00** → docs/plan/B-guide-coverage.md

## 다음 문서

- `04-dependencies-dag.md` — task 간 의존성 그래프 + critical path
- `08-buddy-skill-mapping.md` — 각 task에 어떤 buddy skill 호출할지
