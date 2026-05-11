# Web3 + Game Style Stats — Step 5.2 evidence

> **Purpose**: gather observable design-language values from 11 trusted production services (6 web3, 5 game) so the `team-brand-spec.default.json` (Step 5.1) is grounded in real-world evidence, not LLM-imagined defaults. Every value carries a source line.

**Service set (fixed by user 2026-05-11):**

- **web3 (6)**: Uniswap · OpenSea · Phantom · Lens Protocol · Farcaster (Warpcast) · Coinbase
- **game (5)**: Riot Valorant · miHoYo Genshin Impact · Bungie Destiny 2 · Supergiant Hades · Supercell Clash Royale

**Dimensions** (per service):
color tokens · typography · spacing · radius · motion · iconography · logo aspect · asset hosts.

**Methodology:**

1. *Prefer public design-system code* (e.g. Uniswap's `Spore` tokens shipped under GPL-3.0) when concrete values are committed and observable.
2. *Fall back to official brand guidelines* (logo / brand pages, support docs) when the design system isn't open-sourced.
3. *Defer to public game wikis* (Fandom, IGN style refs) when a studio doesn't ship a public brand kit — these are observation-based, not derivative.
4. Every row names its *source URL* so the evidence is auditable; values are quoted verbatim, never inferred.

**License posture:** evidence quotation of design-system values is a fact citation, not a derivative work. Where a source ships its tokens under GPL-3.0 (Uniswap), we cite — never copy code; values are noted as observations with attribution. `assets/team-brand-spec.default.json` (Step 5.1) does not re-publish any source repo's code.

---

## Per-service evidence

### web3-01 · Uniswap

Source: <https://github.com/Uniswap/interface/tree/main/packages/ui/src/theme> (Uniswap "Spore" design system, GPL-3.0, fetched via `gh api` 2026-05-11).

- **Color — light surfaces**: `surface1 #FFFFFF` · `surface2 #F9F9F9` · `surface3 rgba(19,19,19,0.08)` · `surface3Solid #F2F2F2`
- **Color — dark surfaces**: `surface1 #131313` · `surface2 #1F1F1F` · `surface3 rgba(255,255,255,0.12)` · `surface3Solid #393939`
- **Color — text neutrals (light)**: `neutral1 #131313` · `neutral2 rgba(19,19,19,0.63)` · `neutral3 rgba(19,19,19,0.35)`
- **Color — text neutrals (dark)**: `neutral1 #FFFFFF` · `neutral2 rgba(255,255,255,0.65)` · `neutral3 rgba(255,255,255,0.38)`
- **Color — brand accent**: `accent1 #FF37C7` (Uniswap pink, identical light/dark) · `accent1Hovered #E500A5`
- **Color — status (light)**: success `#0C8911` · warning `#996F01` · critical `#E10F0F`
- **Color — status (dark)**: success `#21C95E` · warning `#FFBF17` · critical `#FF593C`
- **Typography — display/body**: custom "Basel Grotesk" family; web fallback stack `Basel, -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`. Weights: Book 400 (native) / 485 (web) · Medium 500.
- **Typography — mono**: `ui-monospace, SFMono-Regular, SF Mono, Menlo, Monaco, "Cascadia Mono", "Segoe UI Mono", "Roboto Mono", "Courier New", monospace`
- **Spacing** (px): `0, 1, 2, 4, 6, 8, 12, 16, 18, 20, 24, 28, 32, 36, 40, 48, 60` (4-px-grid biased)
- **Radius** (px): `0, 4, 6, 8, 12, 16, 20, 24, 32, full(999999)`
- **Icon sizes** (px): `8, 12, 16, 18, 20, 24, 28, 32, 36, 40, 44, 48, 56, 64, 70, 100`
- **Motion**: token file present at `packages/ui/src/theme/animations/`, used for inter-platform timing variants; specific ms scale not enumerated as a flat table in the source.
- **Logo / mark**: unicorn 🦄 + wordmark; aspect ratio in mark only ≈ 1:1; with wordmark ≈ 4:1.
- **Asset hosts**: `app.uniswap.org`, `static.uniswap.org` (CDN).

### web3-02 · OpenSea

Source: <https://docs.opensea.io/docs/logos> (OpenSea developer docs, official brand assets section).

- **Color — official palette** (5 tokens):
  - `Dark Sea #1868B7`
  - `Sea Blue #2081E2` (primary brand)
  - `Marina Blue #15B2E5`
  - `Aqua #2BCDE4`
  - `Fog #E5E8EB` (light neutral surface)
- **Typography**: sans-serif logotype, Arial-like wordmark; specific UI typeface not publicly documented as of 2026-05-11. Production-site inspection (out-of-scope for this snapshot) typically resolves to system sans + Inter on web.
- **Spacing / radius / motion**: not publicly documented; product UI commonly resolves to 4-/8-px grid with 12–16 px card radii (observation, unconfirmed).
- **Asset host**: `static.seadn.io` (mark asset CDN per the linked docs).
- **Logo aspect**: stylized "O" mark ≈ 1:1; mark + wordmark ≈ 5:1.

### web3-03 · Phantom

Source: <https://phantom.com/learn/blog/introducing-phantom-s-new-brand-identity> (rebrand announcement) + <https://docs.phantom.com/resources/assets> (developer asset page).

- **Color**: primary purple/violet, rebrand emphasizes "modern tones and vibrant complementary colors that are more lively and expressive". Specific hex codes are not enumerated in the public blog or developer docs as of 2026-05-11. Visual identity hosts a ghost mascot on a violet field.
- **Typography**: custom typeface "Phantom" (F37 Foundry collaboration) — rounded and expressive, designed to "complement the dynamic, floating nature of the new ghost icon".
- **Mascot**: ghost (rebranded 2023; "more dynamic, distinctive, and sleeker"); designed by Bakken & Baeck.
- **Asset host**: `phantom.com`, asset zip in developer docs.
- **Logo aspect**: ghost mark ≈ 1:1; with wordmark ≈ 3.5:1.

---

## Sub-step status

- [x] Uniswap (full token evidence)
- [x] OpenSea (brand palette + partial typography)
- [x] Phantom (brand description; hex not publicly enumerated)
- [ ] Lens Protocol — Batch 2
- [ ] Farcaster (Warpcast) — Batch 2
- [ ] Coinbase — Batch 2
- [ ] Valorant — Batch 3
- [ ] Genshin Impact — Batch 3
- [ ] Destiny 2 — Batch 3
- [ ] Hades — Batch 4
- [ ] Clash Royale — Batch 4
- [ ] Aggregate decision values — Batch 5

---

## Out-of-scope (deliberate)

- **Production-site CSS scraping**: rejected per Step 5 plan — too volatile across deploys, raises bot-detection/ToS questions for some services.
- **Round-trip back to source**: this file is one-way evidence; aggregate values feed Step 5.1 but do not flow back to any source service.
- **Per-service motion timing tables**: most sources do not publish enumerated ms scales. The aggregate (Batch 5) will derive motion timing from CSS spec defaults (Material Motion + Apple HIG generic) rather than per-service inference.
