# 06 · Acceptance Criteria

> **목적**: 14개 atomic task별 *완료 판정* 기준. test / lint / smoke / human-judgement 어느 방식으로 PASS/FAIL 판정.
> **§6 verify-quality phase 입력**: 본 문서가 그대로 release-gate 체크리스트.

---

## 1 · D · Release engineering

### D-01-changelog-split

**판정 방식**: lint + grep
- ✅ `## [1.0.0] · 2026-05-12` 헤딩 존재
- ✅ `## [Unreleased]` 섹션이 *빈 placeholder* 한 줄 또는 *후속 작업 entry 없음*
- ✅ `[1.0.0]` 섹션은 기존 `[Unreleased]` 내용 그대로 (Step 1~7 + post-Step + bump entries)
- ✅ CHANGELOG.md 전체가 `markdownlint` (선택) 통과

**verify**:
```bash
grep -n "^## \[1.0.0\]" CHANGELOG.md
grep -n "^## \[Unreleased\]" CHANGELOG.md
```

### D-02-plugin-version-bump

**판정 방식**: JSON parse + value check
- ✅ `.claude-plugin/plugin.json` `version: "1.0.0"`
- ✅ `.claude-plugin/marketplace.json` `plugins[0].version: "1.0.0"`
- ✅ 두 파일 모두 valid JSON

**verify**:
```bash
python3 -c "import json; assert json.load(open('.claude-plugin/plugin.json'))['version'] == '1.0.0'"
python3 -c "import json; assert json.load(open('.claude-plugin/marketplace.json'))['plugins'][0]['version'] == '1.0.0'"
```

### D-03-doc-version-bump

**판정 방식**: grep으로 잔재 0
- ✅ `README.md` status line: `Step 1–7 shipped … 1.0.0 …`
- ✅ `HANDOFF.md` active version line + Step 7 block 모두 `v1.0.0`
- ✅ `SKILL.md` status header에 `v1.0.0`
- ✅ `PROJECT-PLAN.md` §6.5 / §7 latest entry 모두 `v1.0.0`
- ✅ `grep "0.1.0" README.md HANDOFF.md SKILL.md PROJECT-PLAN.md` 결과 0 (또는 historical decisions-log entry만)

**verify**:
```bash
grep -rE "0\.1\.0" README.md HANDOFF.md SKILL.md PROJECT-PLAN.md | grep -v "decisions log entry"
# 기대 출력: 0줄 (또는 의도된 historical 참조만)
```

### D-04-git-tag-push

**판정 방식**: git tag 존재 + origin sync
- ✅ `git tag --list v1.0.0` 출력 = `v1.0.0`
- ✅ `git ls-remote --tags origin | grep v1.0.0` 출력 비어있지 않음
- ✅ tag commit hash = master HEAD commit hash (release 직전 마지막 commit)

**verify**:
```bash
git tag --list v1.0.0
git ls-remote --tags origin | grep v1.0.0
[[ "$(git rev-parse v1.0.0)" = "$(git rev-parse master)" ]] && echo "tag = HEAD"
```

**rollback** (tag을 잘못 찍었거나 D-05 직전에 취소해야 할 때):
```bash
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0
```

### D-05-github-release

**판정 방식**: GitHub API 응답
- ✅ `gh release view v1.0.0` exit 0
- ✅ release body가 CHANGELOG `[1.0.0]` 섹션 내용 포함
- ✅ release tag 자동 `v1.0.0`

**verify**:
```bash
gh release view v1.0.0 --json tagName,body -q '{tag:.tagName,body_lines:(.body|split("\n")|length)}'
```

**rollback** (release note 오류 또는 잘못된 tag으로 publish 했을 때):
```bash
gh release delete v1.0.0 --yes
# 필요 시 D-04 rollback 함께 실행해서 tag 자체도 제거
```

### D-06-marketplace-ref-pin

**판정 방식**: grep + doc 검증
- ✅ `QUICKSTART.md` §6 단계 4에 `--ref v1.0.0` 안내 존재
- ✅ `references/figma-mcp-setup.md`도 동일 안내 (필요 시)
- ✅ `claude plugin marketplace add 0xmhha/claude-design-skill@v1.0.0` 또는 동등한 표기법

**verify**:
```bash
grep -n "v1.0.0" QUICKSTART.md references/figma-mcp-setup.md 2>/dev/null
```

## 2 · A · Adopter dogfooding

### A-01-default-dogfood-spec

**판정 방식**: human (designer) judgement
- ✅ `docs/dogfood/01-nft-card-spec.md` 신규 (1 파일) — `docs/dogfood/_template.md` schema 따름 (5 H2 섹션: scenario / steps / observed / friction / score)
- ✅ **Steps 첫 부분에 v1.0.0 plugin self-install verification** (fresh checkout · `claude plugin marketplace add` · `claude plugin install` · `/skill` 검출 + 소요시간 측정). install 단계 마찰은 `_template.md` priority rule 따라 **P0**로 기록.
- ✅ 4-stage workflow 단계 모두 명시: assumptions list (≥ 5 entries with `(verified)` / `(inferred)` / `(open)` tags), reasoning paragraph, placeholder mockup (ASCII 또는 SVG 또는 figma-viewer.py 결과), anti-AI-slop self-score
- ✅ self-score < 3 hits (threshold rule by `SKILL.md §Anti-AI-slop`)

### A-02-figma-mcp-smoke

**판정 방식**: dogfood log + 외부 effect 검증
- ✅ `docs/dogfood/02-figma-mcp-smoke.md` 신규 — `_template.md` schema 따름
- ✅ `figma_get_selection` 호출 결과 캡처 (node id + name) → `observed` 섹션
- ✅ batch rename 결과 (current → new 매핑 N개) → `observed`
- ✅ component promotion 결과 (component name + instance count) → `observed`
- ✅ 마찰점 (있다면) → `friction` 섹션 (P0/P1/P2 라벨)

### A-03-codex-e2e-smoke

**판정 방식**: dogfood log + file 검증
- ✅ `docs/dogfood/03-codex-e2e-smoke.md` 신규 — `_template.md` schema 따름
- ✅ Codex CLI 명령 + 출력 PNG SHA-256 → `steps` + `observed`
- ✅ `codex-image-import.py` exit code 0 + 새 PROVENANCE.md entry → `observed`
- ✅ (옵션) Figma 배치 또는 manual placement instruction 출력 → `observed`
- ✅ 마찰점 명시 → `friction` 섹션 (P0/P1/P2 라벨)

### A-04-feedback-backlog

**판정 방식**: artefact 존재
- ✅ A-01·A-02·A-03 마찰점 N개 → `PROJECT-PLAN.md §7` decisions-log entry 1개 (날짜 + 항목 list)
- ✅ 또는 GitHub Issues N개 (link 기록)
- ✅ 각 마찰점에 *우선순위* (P0/P1/P2) 부여
- ✅ 합성 입력: 세 dogfood log의 `friction` 섹션을 `_template.md` 의 grep recipe로 수집 — `grep -h "^| F-" docs/dogfood/0?-*.md`

## 3 · C · Step 8+ enhancement

### C-01-codex-e2e-script

**판정 방식**: test PASS + CI skip 정상
- ✅ `scripts/test_codex_e2e.py` 신규
- ✅ local에 Codex CLI 있을 때 PASS
- ✅ `CODEX_TOKEN` 또는 codex CLI 없을 때 `exit 0` (skip)
- ✅ CI workflow에 conditional step 추가, CI 환경에서 skip 출력 정상
- ✅ doc 갱신: `references/codex-design-workflow.md`에 자동화 안내

### C-02-figma-mcp-smoke-script

**판정 방식**: 동일 패턴
- ✅ `scripts/test_figma_mcp.py` 신규
- ✅ `FIGMA_TOKEN` + sample file key 있을 때 PASS
- ✅ 없을 때 skip
- ✅ CI workflow conditional step
- ✅ `references/figma-mcp-setup.md` 갱신

### C-03-usage-telemetry-adr

**판정 방식**: doc 검증
- ✅ `docs/plan/adr/001-usage-telemetry.md` 신규
- ✅ ADR 표준 형식: context / decision / consequences / alternatives / status
- ✅ status는 `proposed` 또는 `accepted` 또는 `rejected` 중 하나
- ✅ privacy-first 명시 (no PII, no codename, opt-in only)
- ✅ 코드 변경 X — ADR-only

## 4 · B · Guide coverage check

### B-00-guide-coverage-check

**판정 방식**: checklist 6/6
- ✅ `docs/plan/B-guide-coverage.md` 신규
- ✅ B-1 ~ B-6 각 항목 행:
  - 항목 description (한 줄)
  - 대응 guide doc path
  - 대응 명령어 예시 (있다면)
  - ✅ / 🟡 / ❌ 라벨
- ✅ 모두 ✅ 또는 명확히 missing 식별

## 5 · cross-task acceptance

전체 plan-build orchestrator가 PASS로 인정되는 조건 (release-gate):

- [ ] 14개 atomic task 중 D 카테고리 6개 완료 (release ship)
- [ ] B-00 완료 (guide 충분성 검증)
- [ ] A 카테고리 ≥ 1개 완료 (적어도 한 dogfood 시나리오)
- [ ] A-04 완료 (피드백 1개 이상 backlog로 변환)
- [ ] C 카테고리는 *우선순위 결정만* 필수, 구현은 선택

108 회귀 테스트는 *모든 task 후* 그대로 통과해야 함 (regression 0 invariant).

## 다음 문서

- `07-timeline.md` — calendar timeline + best/expected/p90/worst
- `08-buddy-skill-mapping.md` — 각 task에 buddy skill 매핑
