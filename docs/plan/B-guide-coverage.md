# B · Per-fork Guide Coverage Check

> **목적**: PROJECT-PLAN.md §6 (b) 의 6 항목이 *현재 repo의 guide doc + 명령어 예시*로 충분히 cover되는지 점검.
> task_id: **B-00** in `03-task-decomposition.md`.

---

## checklist

| ID | 항목 | guide doc | 명령어 예시 | 상태 |
|---|---|---|---|---|
| **B-1** | `team-brand-spec.json` 실제 값 stamp | `references/brand-spec-fields.md` (필드별 ref) + `QUICKSTART.md §4` (override 단계) | `python3 scripts/init-brand.py` → `$EDITOR team-brand-spec.json` | ✅ |
| **B-2** | 내부 codename namespace 추가 | `references/security-config.md §1.5` (conservative-pairing rule) + `scripts/codex-image-import.py:DEFAULT_CODENAME_PATTERNS` (4 default patterns) | `DEFAULT_CODENAME_PATTERNS = [..., r'(?i)\bproject[-_ ]?neptune\b', ...]` 추가 후 `test_codex_image_import.py` 회귀 | ✅ |
| **B-3** | `watermark.enabled` 정책 결정 | `references/brand-spec-fields.md §watermark` (keep-it-off-until-explicitly-approved) + `team-brand-spec.default.json` (default `enabled: false`) | `team-brand-spec.json` 의 `watermark.enabled: true` + `watermark.text` set | ✅ |
| **B-4** | 내부 asset host allowlist 추가 | `examples/dot-claude-settings.json:permissions.ask` + `references/security-config.md §1.2 Team-extensible additions` | settings.json `permissions.ask` 에 host pattern 추가 + 동일 host 를 `security-config.md §1.2` 표에 mirror | ✅ |
| **B-5** | 내부 git host 로 mirror | `CONTRIBUTING.md §For fork operators §9 Mirror to your internal git host` (5단계 bash recipe) | `git remote add internal …` + `git push internal master --tags` + tag divergence point | ✅ |
| **B-6** | 비-GitHub CI host 로 워크플로 포팅 | `references/ci-template.md` (GitLab CI / Bitbucket Pipelines / Buildkite snippet + GH Enterprise / Jenkins / CircleCI / Drone notes) | snippet 복사 → CI host 적용 → 7-suite 108 tests 그대로 통과 확인 | ✅ |

## summary

6/6 ✅. 빠진 guide 없음. 각 항목마다 *guide doc + 명령어 패턴* 둘 다 ship된 상태.

## 미세 부족 (개선 후보, 우선순위 낮음)

| 영역 | 개선 후보 |
|---|---|
| B-2 codename | conservative-pairing 규칙의 *false-positive 케이스 카탈로그* 추가 (예: "stealth fighter aesthetic" 같은 generic 디자인 언어가 *왜 통과*하는지) — 1-page note |
| B-4 asset host | internal host 추가 시 *settings.json + security-config.md + team-brand-spec.json (approved_asset_hosts.internal)* 3개를 동시에 갱신해야 하는데, 그 *동기화 verification* 자동화 (선택) |
| B-5 mirror | mirror 후 *upstream sync 정책* (cherry-pick / rebase / merge) ADR — `docs/plan/adr/002-mirror-sync-policy.md` 작성 가능 (선택) |

이 3개 미세 부족 항목은 *adopter 가 mirror 후 운영 단계에서 마주칠 수 있는 trade-off* 영역. 본 plan에서는 *defer* — 실 adopter 의 요청이 발생하면 그때 진행.

## 결론

PROJECT-PLAN.md §6 (b) 의 6 항목 모두 *현재 repo의 guide로 충분히 cover*. adopter team 이 *self-serve* 가능. 본 task (B-00) 완료.

## 참조

- `docs/plan/02-remaining-work-inventory.md` §B
- `docs/plan/06-acceptance-criteria.md §4`
- `PROJECT-PLAN.md §6 (b)` / `§6 (c)`
