# Dogfood 01 · NFT Card Spec

> **task**: A-01 `default-dogfood-spec` (per `docs/plan/03 §A-01` + `docs/plan/06 §2 A-01`)
> **schema**: `docs/dogfood/_template.md` (5 H2 sections, do not rename)
> **status**: ⏳ **TODO — designer fills this in**. AI must not author the 4-stage workflow content.

> *Auto-generated skeleton on 2026-05-12 by `/buddy:autoplan` delta review. Sections below are placeholders for the human designer. Each placeholder is intentionally short — replace with concrete observations.*

---

## scenario

> *Replace this block with 3~5 sentences describing what you set out to design and why. Anchor on a real adopter need ("I want to mock an NFT card to test the Default Studio identity against the 11-service evidence sweep") rather than a generic exercise.*

`<TODO: 3-5 sentences>`

## steps

> *Numbered, reproducible. Start with the v1.0.0 self-install (autoplan delta review · 2026-05-12) — if install fails, log it in `friction` as P0 per `_template.md` priority rule and stop.*

1. **v1.0.0 plugin self-install verification** (fresh checkout, separate directory from this repo):
   ```bash
   cd $(mktemp -d) && git clone https://github.com/0xmhha/claude-design-skill.git
   cd claude-design-skill && git log -1 --oneline   # expect: 3699b6a or later
   # optional — plugin path (requires Claude Code 2.1.x+):
   claude plugin marketplace add 0xmhha/claude-design-skill
   claude plugin install claude-design-skill
   ```
   - Measure: clone-to-install elapsed seconds
   - Verify: `/skill` listing includes `claude-design-skill` (or equivalent detection)
   - If any step fails → `friction` row with **P0** priority

2. **Brand stamp** (uses the v1.0.0 carrier):
   ```bash
   python3 scripts/init-brand.py
   # override team.company / brand.name to match the adopter context
   ```

3. **4-stage workflow** (per `SKILL.md §Junior Designer workflow`):
   - 3.1 assumptions list (≥ 5 entries, each tagged `(verified)` / `(inferred)` / `(open)`)
   - 3.2 reasoning paragraph (1 short paragraph, contract-style)
   - 3.3 placeholder mockup (ASCII or SVG via `assets/default-brand/` or a `figma-viewer.py` fixture)
   - 3.4 anti-AI-slop self-score (12 patterns from `SKILL.md §Anti-AI-slop`, must score < 3 hits)

4. `<TODO: any adopter-specific extension>`

## observed

> *What actually happened. Expected vs actual, every artefact path captured.*

- **Install timing**: `<TODO: seconds>`
- **Install verification result**: `<TODO: PASS / FAIL with output>`
- **Brand stamp result**: `<TODO>`
- **4-stage workflow output**:
  - Assumptions: `<TODO: list 5+ entries>`
  - Reasoning: `<TODO: 1 paragraph>`
  - Mockup: `<TODO: path or inline ASCII>`
  - Self-score: `<TODO: N hits, list which patterns>`
- **Captured artefacts**: `<TODO: paths>`

## friction

> *Adopter-perspective friction. Priority rule (per `_template.md`): install-path friction = P0. Later-stage friction = P1/P2.*

| ID | priority | description | suggested fix |
|----|----------|-------------|---------------|
| F-01 | `<TODO>` | `<TODO>` | `<TODO>` |

마찰 없으면 `_(none)_`.

## score

> *Self-score against `SKILL.md §Anti-AI-slop` 12 patterns. Threshold: total hits must be < 3 to ship.*

| criterion | hit (0/1) | note |
|-----------|-----------|------|
| 1. 일반론 / cliché | | |
| 2. 검증되지 않은 주장 | | |
| 3. 구체 evidence 부재 | | |
| 4. 부풀린 어휘 | | |
| 5. AI artifact (uncanny pattern) | | |
| **total** | **`<TODO: N>`** | threshold: < 3 PASS |
