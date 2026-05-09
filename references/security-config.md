# Security Configuration · Internal Fork

> Hardened defaults for in-company use (game / web3 studios).
> Replaces the open-internet defaults of the upstream `huashu-design` skill.

---

## 0 · Why this exists

Upstream `huashu-design` was designed for solo content creators with the open internet as a free asset library — `curl` any brand site, `yt-dlp` any product launch video, auto-read `~/.claude/memory/personal-asset-index.json`. That worked for a personal blog / WeChat creator workflow.

For an in-company designer working on game / web3 products, the same defaults become risks:
- Internal product codenames leaking into external query logs
- Attacker-controlled URL injected via prompt → silent download → SSRF / zip bomb / prompt-injection-carrying SVG
- Personal name / email / WeChat ID auto-baked into deliverables
- ToS violations (User-Agent forgery, YouTube download)

This document is the **single source of truth** for what the skill is allowed to fetch automatically and what requires user approval.

---

## 1 · Asset Source Allowlist

The skill may automatically download assets **only** from the domains below. All other domains require explicit per-call user approval.

### 1.1 Default allowlist

| Domain | Purpose | License |
|---|---|---|
| `commons.wikimedia.org` | Public-domain art, museum images, historical content | Public domain / CC |
| `*.metmuseum.org` (Open Access API) | Museum-grade artwork | CC0 (Open Access subset only) |
| `*.artic.edu` (API) | Art Institute of Chicago Open Access | CC0 |
| `unsplash.com` / `images.unsplash.com` | Photography (lifestyle, nature, generic) | Unsplash License |
| `pexels.com` / `images.pexels.com` | Photography | Pexels License |
| `fonts.googleapis.com` / `fonts.gstatic.com` | Web font CSS + WOFF/WOFF2 | OFL / Apache 2.0 |
| `unpkg.com/react@*` `unpkg.com/react-dom@*` `unpkg.com/@babel/standalone@*` | React + Babel pinned versions for prototype HTML (required by `references/react-setup.md`) | MIT (with SRI integrity hash) |

**Rules of the allowlist**:
- Pinned versions only (no `@latest`, no unpinned majors)
- SRI `integrity=sha384-…` is **mandatory** for unpkg.com
- Wildcard subdomain expansion is allowed only where listed (`*.metmuseum.org`)
- HTTP is forbidden — every entry is HTTPS

### 1.2 Team-extensible additions

Internal hosts the team adds — append below. Format: `<host> · <purpose> · <added by> · <date>`.

```
# example placeholder lines — replace with real internal hosts
# assets.example-corp.internal · internal brand assets CDN · @designer · 2026-MM-DD
# figma-export.s3.example-corp.com · Figma export bucket · @platform · 2026-MM-DD
```

**How to add**:
1. Edit this file (commit goes through normal review)
2. Update `.claude/settings.json` permissions to match (see §3)
3. Note the purpose so future reviewers can prune unused entries

---

## 1.3 · WebSearch policy

`WebSearch` is allowed but constrained. The skill's `SKILL.md` §0 confidentiality gate is the first filter; this section is the second.

**Allowed terms** (auto-search OK):
- Publicly released external brand / product names (Apple, DJI, Stripe, Pentagram, Anthropic, etc.)
- Public technology names (React, esbuild, Cloudflare Workers, etc.)
- Public design references (Pentagram identity systems, Müller-Brockmann posters, etc.)

**Forbidden terms** (must ask the user instead — never type into a search engine):
- Internal codenames / project names not yet announced
- Unreleased team product names
- Partner / publisher names under NDA
- Internal system names, internal repo names, internal employee names
- Any string that appears in `team-brand-spec.json` `current_project` block — by definition team-confidential

**Recommended harness setting** for highly sensitive teams:
```jsonc
{
  "permissions": {
    "ask": [
      "WebSearch(*)"   // require user approval per call; the user re-checks the search term
    ]
  }
}
```

This forces a per-call review, which catches accidental codename leakage even when the skill's own gate fails.

---

## 1.4 · OpenAI Codex CLI policy (GPT-5.5 + gpt-image-2)

OpenAI Codex CLI (v0.115+, March 2026) ships GPT-5.5 reasoning + automatic
`gpt-image-2` invocation as a single tool. The skill uses Codex CLI for
brand-correct illustration generation — see `references/codex-design-workflow.md`.

**Three call paths and their policies:**

| Call | Default | Where the gate is |
|---|---|---|
| `codex review` / `codex challenge` | `ask` (user approves each diff send) | gstack:codex skill applies the filesystem boundary; read-only sandbox prevents file writes |
| `codex exec "<prompt>"` (image gen) | `ask` per call | Confidentiality gate (§1.5) runs in-skill before the call; importer (`scripts/codex-image-import.py`) re-checks at file move time |
| `codex login` | one-time, manual | OAuth via ChatGPT — skill never sees the token |

**Outbound data:** every Codex call sends the prompt to OpenAI. Treat the
prompt as something that will be **logged at OpenAI** — apply the same
confidentiality discipline as `WebSearch`.

**Outbound data — image-2 specifically:** in addition to the prompt, Codex
sends any reference images you attach. If the attached image is a screenshot
of an unreleased internal screen, that screen is now in OpenAI's logs. Don't
attach internal screenshots to a Codex image-gen call without confirming
the screen is publicly visible.

**Inbound metadata — C2PA strip policy (added 2026-05-09):** every
gpt-image-2 PNG carries a `caBX` (C2PA / JUMBF) chunk between IHDR and
IDAT — typically ~25 KB of upstream provenance metadata signed by
OpenAI. `scripts/codex-image-import.py` **strips** this chunk before
importing, on the grounds that:

1. The fork has no tool to validate the C2PA payload's contents
   (it's binary, signed by an external party, and could in principle
   carry arbitrary data inside the JUMBF wrapper).
2. The fork's own PROVENANCE.md entry records the same provenance
   facts that matter (Source: codex-cli, gpt-image-2, prompt SHA-256,
   Codex session id) — so AI-generated traceability is preserved
   without trusting the upstream signature.
3. Image bytes themselves are unaffected; only the metadata
   container is removed.

If the team later needs to *retain* C2PA signatures for downstream
verification (e.g. to prove an asset came from OpenAI to a third
party), update `scripts/codex-image-import.py` to record the
stripped C2PA bytes to a parallel `assets/<brand>-brand/c2pa/<name>.cab`
file and document the verification flow in this section. Do not add
`caBX` to `scan_assets.PNG_WHITELIST` without a corresponding
verification tool — that would silently trust whatever bytes the chunk
contains.

---

## 1.5 · Codename / NDA pattern policy (applies to WebSearch + Codex CLI prompts)

**Single source of truth** — both the WebSearch gate (§1.3) and the Codex
image importer (`scripts/codex-image-import.py`) enforce the same rules
listed here. If the patterns below change, both gates pick the change up.

**Default blocked patterns** (regex, case-insensitive):

| Pattern | Catches | Example |
|---|---|---|
| `\bproject[-_ ]?[a-z]{4,}\b` | "project Falcon", "project_phoenix", "project-eagle" | "logo for project Phoenix" → blocked |
| `\b(internal\|nda\|confidential)[-_ ][a-z]+` | "internal-prototype", "nda assets", "confidential-roadmap" | "render the internal-prototype hero" → blocked |

**Per-team additions**: the team's own codename namespace (e.g. studio
codenames, partner publisher names under NDA, internal milestone
names like "M3-Q2" if those are sensitive). Add by:

1. Edit the `DEFAULT_CODENAME_PATTERNS` constant in
   `scripts/codex-image-import.py` (until the `--codename-pattern`
   flag is wired in Phase 5).
2. Mirror the pattern here as a row in the table above.
3. Add the pattern to the WebSearch gate's manual checklist in §1.3.

**Why a regex list and not a YAML file**: a YAML file lives in the repo,
and a contributor with push access could remove a pattern as part of a
"refactor" PR. Keeping the patterns in source code surfaces every change
in code review where a pattern removal stands out.

**False-positive handling**: if a legitimate prompt is blocked (e.g.
"project Apollo" referring to NASA, not an internal codename), the script
exits 4 and the user can either rephrase the prompt or run with a future
`--allow-pattern` flag (Phase 5). **No silent override** — every bypass
goes through an explicit flag the user has to type.

---

## 2 · Forbidden by Default

These tools / patterns are **not allowed** to run automatically. The skill must not propose them in workflows.

| Tool / pattern | Reason | Replacement |
|---|---|---|
| `yt-dlp` (any subcommand) | YouTube ToS gray-area + downloaded frames are third-party copyright | Ask user to share their own screen recording, or get assets from the brand's official press kit / Figma library |
| `curl -A "Mozilla/5.0"` (User-Agent forgery) | ToS violation signal + bypasses bot detection | Use the default `curl` UA, or ask user to download manually |
| Unbounded `curl` to arbitrary domain | SSRF / zip bomb / prompt-injection vector | Allowlist in §1, or per-call user approval |
| `wget` to arbitrary domain | Same as `curl` | Same |
| Reading `~/.claude/memory/personal-asset-index.json` | Sensitive personal data (real name / email / WeChat / local paths) auto-loaded into LLM context | `team-brand-spec.json` (§4) |

---

## 3 · `.claude/settings.json` Recommended Defaults

Drop-in configuration that enforces the rules above at the harness level (the skill alone can only request — the harness enforces).

```jsonc
{
  "permissions": {
    "deny": [
      // Forbid the listed tools entirely
      "Bash(yt-dlp:*)",
      "Bash(youtube-dl:*)",

      // Forbid arbitrary curl/wget — see "ask" list for allowlisted use
      "Bash(curl:*)",
      "Bash(wget:*)"
    ],
    "ask": [
      // Allow curl ONLY for allowlisted hosts (with user prompt per call)
      // Replace example-corp with your real internal hosts
      "Bash(curl https://commons.wikimedia.org/*)",
      "Bash(curl https://*.metmuseum.org/*)",
      "Bash(curl https://*.artic.edu/*)",
      "Bash(curl https://images.unsplash.com/*)",
      "Bash(curl https://images.pexels.com/*)",
      "Bash(curl https://fonts.googleapis.com/*)",
      "Bash(curl https://fonts.gstatic.com/*)",
      "Bash(curl https://unpkg.com/react@*)",
      "Bash(curl https://unpkg.com/react-dom@*)",
      "Bash(curl https://unpkg.com/@babel/standalone@*)"
    ]
  }
}
```

**Notes**:
- `deny` is absolute (no override per call). `ask` requires user approval each time.
- The harness matches command prefixes — `Bash(curl:*)` matches any `curl …`. Listing specific URL patterns under `ask` overrides the broader `deny`.
- For full lockdown: remove the `ask` entries and require manual file delivery from the user.

---

## 4 · `team-brand-spec.json` (replaces `personal-asset-index.json`)

The team-shared, version-controlled equivalent of the upstream personal asset file. Lives in the **project repo** (not in `~/.claude/memory/`), so it's auditable and shared across designers.

**Template**: `assets/team-brand-spec.example.json` — copy to your project root as `team-brand-spec.json`, fill in real values, commit.

**Lookup order** (when the skill needs brand assets):
1. `<project>/team-brand-spec.json` — primary source
2. `<project>/brand-spec.md` — narrative spec written during Core Asset Protocol
3. Ask the user — never fabricate, never auto-fetch from the open internet outside the allowlist

**No automatic loading of personal data**: the skill does **not** read `~/.claude/memory/personal-asset-index.json` in this fork.

---

## 5 · External SVG Sanitization (handled in Group B)

Even when an SVG is downloaded from an allowlisted host, it is **not** safe to inline directly. SVG can carry `<script>`, `<foreignObject>`, and event handlers. See `references/svg-sanitize.md` (added in Group B) for the mandatory sanitization pass.

---

## 6 · Audit Trail

Every fetch from an allowlisted source should be logged in the project's `assets/<brand>-brand/PROVENANCE.md` with:

```
- 2026-MM-DD · curl https://commons.wikimedia.org/wiki/File:Foo.svg → assets/foo-brand/logo-source.svg
  License: Public Domain
  Sanitized: yes (svg-sanitize.md pass on 2026-MM-DD)
  Used in: slides/03-hero.html
```

This makes license review and security audit possible after the fact.

---

## 7 · Failure Modes / FAQ

**Q: The brand I need isn't on Wikimedia / Unsplash. What now?**
A: Ask the user to provide assets directly (drop into `assets/<brand>-brand/`). For real brand work, the user has — or should request — a press kit from the brand. The skill should never silently scrape `<brand>.com`.

**Q: I need a font that isn't on Google Fonts.**
A: Self-host. Add the font file to the project repo and reference it locally. Don't add new font CDNs to the allowlist without team review.

**Q: A coworker's design references a YouTube video.**
A: They should screen-record their own viewing and share that file. The skill won't `yt-dlp` for them.

**Q: We need to add `*.figma.com` for Figma MCP integration.**
A: Figma MCP communicates over its own protocol, not via `curl` from this skill. If a workflow does require HTTP fetch from Figma, add it to §1.2 with reviewer note. (Phase 3 of PROJECT-PLAN covers Figma in detail.)

---

**Owner**: Internal design platform team
**Last reviewed**: 2026-05-08
**Related**: `PROJECT-PLAN.md` Phase 1 Group A · `SKILL.md` §1.a · `references/svg-sanitize.md` (forthcoming)
