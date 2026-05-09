---
name: claude-design-skill
description: |
  Claude Code-based design skill for hi-fi prototyping and Figma MCP-driven
  precision design work. Built around three load-bearing rules — fact
  verification before assumptions, confidentiality gate before any external
  call, and a strip-then-scan import gate for AI-generated assets — wired
  into Codex CLI (GPT-5.5 reasoning, gpt-image-2 image generation) and the
  Figma MCP toolchain. Triggers — Claude design skill, Figma MCP workflow,
  Figma selection-aware edit, Figma layer rename, Figma component grouping,
  brand spec from Figma, codex image asset, brand-correct illustration via
  gpt-image-2, prototype security baseline, sanitize external SVG, prototype
  vs production boundary, Pixel 8 mockup, Android prototype, app prototype.
  This skill is a clean-room rewrite — no upstream design skill is inherited.
---

# claude-design-skill

> Status: **v0.1.0-alpha · skeleton · 2026-05-09**
> Body sections marked TBD are filled in Step 2 / Step 3 of the project
> plan (see PROJECT-PLAN.md). Security and routing rules are already
> live and load-bearing — they govern every external call this skill
> can make.
>
> **For AI agents in a fresh session**: read `HANDOFF.md` at the repo root
> first. It contains the working-style briefing and anti-pattern list
> that prevents the most common rework loops.

## What this skill is for

Hi-fi prototypes, slide decks, animations, and Figma-MCP-driven precision
design work, executed by an LLM agent through Claude Code. The skill
provides:

- **Security baselines** that govern every external fetch (allowlist,
  WebSearch policy, Codex CLI policy, codename redaction).
- **Sanitizers** for external assets (SVG XXE/script removal, PNG chunk
  scan, AI-generated PNG strip-and-import).
- **Figma MCP workflow** with five sub-guides covering selection-aware
  edits, layer renames, component grouping, brand-spec import, and the
  meta hub.
- **Codex CLI bridge** for GPT-5.5 reasoning + gpt-image-2 image
  generation, with a hard-fail import gate that strips C2PA
  metadata and re-scans the result.

The body — design philosophies, scene templates, slide rules, animation
rules, prototype scaffolding — is **deliberately empty in this skeleton**
and will be authored from scratch in subsequent steps. This avoids
inheriting any prose from an upstream skill and keeps the project
license-clean.

## Core Principle #0 · Fact verification before assumptions

Any factual claim about the existence, release status, version number,
or specifications of a specific product, technology, event, or person —
**the first action MUST be `WebSearch`**. Asserting from training-corpus
memory is forbidden.

### Trigger conditions (any one)

- The user mentions a specific product name you are not familiar with
  or unsure about.
- Anything involving release timelines, version numbers, or specs from
  2025 onward.
- You catch yourself thinking "I think it's…", "should not have launched
  yet", "probably around…", "might not exist".
- The user requests design materials for a specific product or company.

### Hard procedure (execute before clarifying questions)

1. **Confidentiality gate (must answer before any external call)**: is
   the term a publicly released external brand or product (e.g., DJI
   Pocket 4, Apple Vision Pro, Stripe), or could it be an internal
   codename, unreleased team product, or partner under NDA? If the
   second — **do not search and do not send to Codex**. Ask the user
   instead. The same gate applies to `WebSearch`, `Bash(curl …)`,
   `Bash(codex exec …)`, and any image-generation prompt. Pattern
   table lives in `references/security-config.md §1.5`;
   `scripts/codex-image-import.py` re-runs the check at file-move time
   and exits 4 on any match.
2. `WebSearch` for the product name + a recent time keyword
   ("2026 latest", "launch date", "release", "specs") — only for public
   external brands cleared in step 1.
3. Read 1–3 authoritative results to confirm: existence, release
   status, latest version, key specs.
4. Write the facts into the project's `product-facts.md` (per-project
   scratch file, gitignored). Don't rely on memory.
5. Can't find anything or results are ambiguous → ask the user, don't
   assume.

### Forbidden phrasing

- ❌ "I remember X hasn't launched yet"
- ❌ "X is currently version N" (an unsearched claim)
- ❌ "X probably doesn't exist"
- ❌ "As I recall, X's specs are…"
- ✅ "Let me `WebSearch` X's latest status"
- ✅ "Authoritative sources I found say X is…"

This principle outranks "ask clarifying questions" — asking questions
presupposes the facts are right. If facts are wrong, every question is
skewed.

## Core Principle #1 · Security-first asset handling

Every external asset must pass through a sanitizer before it lands in
this repository. The sanitizer is whitelist-based and recorded by SHA-256
in PROVENANCE so future audits can detect tampering.

| Asset type | Gate | Implementation |
|---|---|---|
| External SVG (logos, illustrations) | XXE-guarded XML parse + tag/attr whitelist + CSS sub-sanitize + visibility comment | `scripts/svg-sanitize.py` + `references/svg-sanitize.md` |
| External PNG / JPG | Chunk/segment scan: trailing data, non-whitelist chunks, oversized text metadata | `scripts/scan_assets.py` |
| Codex / gpt-image-2 generated PNG | C2PA `caBX` strip + recursive discovery + scan re-run + hard-fail | `scripts/codex-image-import.py` + `references/codex-design-workflow.md` |
| External fetch (curl, wget, etc.) | Domain allowlist + per-call user approval + WebSearch policy | `references/security-config.md` + `examples/dot-claude-settings.json` |
| Prototype-only patterns (CDN, Babel-standalone, in-DOM API keys) | Production-boundaries checklist | `references/production-boundaries.md` |

If a sanitizer rejects an asset, **do not silently retry** with a
different fetch path. Surface the rejection to the user, log it in
PROVENANCE, and ask for an alternative source.

## Figma MCP workflow

When work originates in Figma — selection-aware edits, layer renames,
component promotions, brand-token imports — start at the workflow hub
and dispatch to the relevant sub-guide:

| Situation | Read |
|---|---|
| Entry point — MCP-aware vs MCP-absent decision rules, audit report template | `references/figma-workflow.md` |
| The user said "this layer" — confirm what was actually selected | `references/figma-selection-aware.md` |
| Many layers named `Frame 47` / `Rectangle 31` — assign meaningful names | `references/figma-layer-naming.md` |
| Repeated patterns appearing 3+ times — propose component promotion | `references/figma-component-grouping.md` |
| Pull design tokens (colors, typography, logos) from Figma into `team-brand-spec.json` | `references/figma-brand-spec-import.md` |

## Codex CLI design workflow

For brand-correct illustration generation via GPT-5.5 reasoning +
gpt-image-2 image gen, with the strip-then-scan import gate:

→ `references/codex-design-workflow.md`

Key facts (validated against codex-cli 0.130.0 on 2026-05-09):

- Codex CLI default model is **gpt-5.5**.
- Image generation runs through Codex's built-in `image_generation`
  tool, no `OPENAI_API_KEY` env var required (codex-cli's own OAuth
  token covers it).
- PNGs land at `~/.codex/generated_images/<session-id>/ig_<hash>.png`.
- Every gpt-image-2 PNG carries a `caBX` C2PA chunk (~25 KB). The
  importer strips it and substitutes the fork's own PROVENANCE entry.

## References routing table

| Task | Read |
|---|---|
| **Security baseline** — allowlist, deny rules, settings.json template, audit trail | `references/security-config.md` |
| **External SVG sanitization** — threat model, whitelist, CSP, failure placeholder, visibility comment policy | `references/svg-sanitize.md` + `scripts/svg-sanitize.py` |
| **Prototype ↔ production boundary** — vendoring, pre-compile, proxy backend, pre-prod checklist | `references/production-boundaries.md` |
| **Figma workflow hub** — entry point when work originates in Figma | `references/figma-workflow.md` |
| **Figma selection-aware edits** — confirm what the user meant by "this layer" | `references/figma-selection-aware.md` |
| **Figma layer naming pass** — assign meaningful names | `references/figma-layer-naming.md` |
| **Figma component grouping** — detect repeats, promote to components | `references/figma-component-grouping.md` |
| **Figma brand-spec import** — design tokens / typography / logo into `team-brand-spec.json` | `references/figma-brand-spec-import.md` |
| **Codex CLI design workflow** — GPT-5.5 reasoning + auto gpt-image-2, with import gate | `references/codex-design-workflow.md` + `scripts/codex-image-import.py` |
| **Brand spec field reference** — what every key in `team-brand-spec.example.json` means | `references/brand-spec-fields.md` |
| **CI workflow templates** — GitHub Actions / GitLab CI for sanitizer regression + asset scan | `references/ci-template.md` |

## Body sections — TBD (authored in Step 2 / Step 3)

These sections will be authored from scratch in subsequent steps. Do
not pull text from any third-party design skill. Each section will get
its own `references/<topic>.md` file when it grows beyond a few
paragraphs.

- **Design philosophy catalog** — design schools and their identifying
  features. Authored in Step 3, not before. Until then, when the user
  needs design direction, ask the user for references rather than
  proposing from memory.
- **Scene templates** — cover, infographic, slide deck, hero animation,
  game HUD, NFT marketplace, wallet/DEX, onboarding game-loop. Step 3.
- **Junior Designer workflow** — the iterative
  assumptions → reasoning → placeholders → review loop. Step 3.
- **Anti-AI-slop checklist** — what to avoid in generated UI. Step 3.
- **App prototype rules (iOS / Android)** — `IosFrame` / `AndroidFrame`
  device wrapping, real-image policy, Playwright verification.
  Currently `assets/android_frame.jsx` is the only mockup engine
  shipped — `IosFrame` will be authored from scratch in Step 3.
- **Slide deck conventions** — 1920×1080 layouts, speaker-notes panel.
  Step 3.
- **Animation rules** — Stage / Sprite engine, Expo easing, narrative
  pacing, anti-pitfall checklist. Step 3 (engine code rewrite needed).
- **Tweaks live-tuning system** — toggling design variations. Step 3.
- **Critique guide** — N-dimension scoring after delivery. Step 3.

## Cross-agent environment adaptation

This skill is designed for Claude Code as the host agent. It also runs
under any markdown-skill-capable agent (Cursor, Trae, etc.) provided
the harness honors `permissions.deny` / `permissions.ask` in
`.claude/settings.json`. If your agent does not, the skill's security
guarantees degrade — sanitizers still run on demand, but external
fetches are no longer gated by the harness.

For Codex CLI integration specifically, install codex-cli ≥ v0.115
locally and run `codex login` once. The skill assumes codex-cli's own
OAuth token; no API key lives in any settings file in this repo.
