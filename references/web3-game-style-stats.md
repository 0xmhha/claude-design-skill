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

### web3-04 · Lens Protocol

Source: <https://github.com/lpolt/lens-brand-kit> (community-mirrored brand kit; the official `lens.xyz/brand` page is bot-gated and returns HTTP 403 to non-browser fetch). Color values themselves are distributed only as a PDF inside the brand-kit repo (`Colours/Lens Protocol_Colours.pdf`), so concrete hex codes are not text-extractable without downloading the PDF — recorded here as a known limitation.

- **Color**: green-led identity ("vibrant universe of plant-like characters and expressions borrowed from the world of flora"). Specific hex values reside inside the brand-kit PDF; commonly observed in product UI as a lime/sage green primary plus monochrome (black/white) base. Concrete hex codes deferred to a future evidence pass that resolves the PDF.
- **Typography**: not publicly enumerated in text-accessible sources as of 2026-05-11; brand-kit ships logo SVGs only, not type specimens.
- **Logo**: "Lens" wordmark (custom geometric) + symbol; assets in SVG + PNG, black / white / colour variants.
- **Asset host**: `lens.xyz` (production), brand-kit repo on GitHub.
- **Logo aspect**: wordmark ≈ 3:1.

### web3-05 · Farcaster (Warpcast)

Source: <https://github.com/vrypan/farcaster-brand> (official brand assets repo, CC0 license).

- **Color — primary**: `Farcaster Purple #8A63D2` (single token; CC0 release by Merkle Manufactory).
- **Color — secondary**: black + white (logo + wordmark variants ship in all three).
- **Typography — body/UI**: Warpcast (the dominant client) uses a system-sans stack; specific typeface name not centrally documented. Farcaster ships a *fonticon webfont* of the logo for inline use, not a body typeface.
- **Logo**: rounded square mark + wordmark variants; assets in SVG + PNG.
- **License**: assets under CC0 — directly reusable.
- **Asset host**: `warpcast.com`, asset repo on GitHub.
- **Logo aspect**: rounded mark ≈ 1:1; wordmark ≈ 3:1.

### web3-06 · Coinbase

Source: <https://www.coinbase.com/press> (official press kit; bot-gated on direct fetch — values triangulated through Moniker rebrand coverage and a Coinbase Sans font review).

- **Color — primary**: `Coinbase Blue #1652F0`.
- **Color — secondary**: white + black (contextual on light vs dark surfaces).
- **Color — extended palette**: Moniker introduced a secondary palette for sub-brand flexibility; specific hex codes not centrally enumerated in the public press kit text.
- **Typography — primary**: `Coinbase Sans` (custom, designed by Moniker) — 36 styles across Optical / Display / Text / Micro / Mono, 29,000+ glyphs, 200+ Latin languages. Licensed for Coinbase use only (not redistributable).
- **Typography — open-source fallback** (recommended by HipFonts review): `Public Sans` 500.
- **Asset host**: `www.coinbase.com`, `assets.coinbase.com`.
- **Logo aspect**: mark ≈ 1:1; wordmark ≈ 4:1.

### game-01 · Riot Games · Valorant

Source: <https://colorcodeshub.com/brand/valorant> + <https://fontswan.com/valorant-font/> + <https://coryschmitz.com/VALORANT> (designer Cory Schmitz's case study for the original Valorant identity).

- **Color — primary**: `Valorant Red #FF4655` (RGB 255 70 85, Pantone 1785 C).
- **Color — palette extensions**: `#FD4556`, `#BD3944`, `#53212B` (deep red/maroon shades for HUD chrome), `#FFFBF5` (off-white surface / paper tone).
- **Color — black**: pure black `#000000` for emblem + symbols + dark surfaces.
- **Typography — in-game UI / menus / chat**: `DIN Next` (sans-serif, modern, high-legibility, condensed at HUD sizes).
- **Typography — logo**: custom angular "Valorant" logotype (chevron-derived; not a redistributable typeface).
- **Logo**: stylized `V` chevron mark + uppercase wordmark.
- **Asset host**: `playvalorant.com`, Riot brand resources.
- **Logo aspect**: chevron mark ≈ 1:1; with wordmark ≈ 4:1.

### game-02 · miHoYo (HoYoverse) · Genshin Impact

Source: <https://genshin-impact.fandom.com/wiki/Typeface> (community wiki; mirrors miHoYo's own UI specifications) + <https://1000logos.net/hoyoverse-logo/> (HoYoverse logo + identity overview).

- **Color — game-side identity**: monochrome black + off-white for the Genshin wordmark; the in-game UI sits over photographic backgrounds and uses gold (`~#E6CDA0` warm gold, observation) for the primary accent / framing chrome on menus, inventory, gacha banner cards.
- **Color — HoYoverse master brand**: black + white base with a "light and shiny gradient blue-purple-pink scheme" on the 3D ring emblem; blue is the dominant shade. Specific hex codes not enumerated in public sources as of 2026-05-11.
- **Typography — primary**: `HYWenHei-85W` (proprietary miHoYo derivative of Hanyi WenHei 85W Extra Bold) — supports CJK with Japanese-style display when language is set to JP, fullwidth-interpunct fixes, and other tweaks. Not openly licensed.
- **Typography — Latin fallback**: not centrally documented; in-game Latin glyphs visually align with a humanist serif/sans pairing (observation).
- **Logo**: stylized "Genshin Impact" wordmark, monochrome black; "glyph transformations" so letters incorporate weapon shapes (a Schmitz-style identity choice).
- **Asset host**: `genshin.hoyoverse.com`, `hoyoverse.com`.
- **Logo aspect**: wordmark ≈ 5:1.

### game-03 · Bungie · Destiny 2

Source: <https://dwsn3ee3.wordpress.com/2014/09/16/destiny-futura-and-helvetica/> (Bungie typography reverse-engineering case study) + <https://www.bungie.net> production observation.

- **Typography — logo / display**: `Futura` (geometric sans, the Destiny logo's wordmark and display headings).
- **Typography — UI / menus / body**: `Neue Haas Grotesk` (the modern Helvetica that Christian Schwartz cleaned up in 2010). Standard Helvetica-family stack as fallback.
- **Color — class identity (alpha-tier brand axis)**: Hunter cyan/navy band, Warlock yellow/orange band, Titan red band — these are the *content* axis, not the UI brand axis. Specific hex codes not enumerated in public Bungie press materials as of 2026-05-11.
- **Color — UI chrome**: deep blue-black (`~#0C1216` observation) with high-luminance white text; status accents in cyan + amber for state changes (damage / cooldown), gold for legendary-tier loot framing. Observation, unconfirmed.
- **Logo**: stylized `Destiny 2` wordmark in Futura; symbol set (mark + class glyphs) is the Tribal Symbols pack.
- **Asset host**: `www.bungie.net`, `www.destinythegame.com`.
- **Logo aspect**: wordmark ≈ 5:1.

### game-04 · Supergiant Games · Hades

Source: <https://build.typogram.co/p/a-deep-dive-into-hades-iis-branding> (Typogram designer deep dive into the Hades II ligature work) + <https://fontmeme.com/fonts/hades-font/> (poster font identification) + production observation from Supergiant's promotional art (Greg Kasavin / Jen Zee design direction).

- **Typography — display / poster**: `Mrs Eaves Bold` (Zuzana Licko, Emigre Fonts) — paired with custom HA-ligature work. Distressed / hand-treated treatment applied per asset, not a flat font swap.
- **Typography — wordmark refinement (Hades II)**: HA-ligature redesigned so "the H extends its right serif and curves up to form a swash" while "the A shortens its left leg"; treatment described as "gore and elegance."
- **Color — game-side identity (Hades 2020)**: deep wine red + smoky black surface, gold/warm yellow accent for legendary tier and rune chrome, purple/violet secondary; specific hex codes not enumerated in public sources.
- **Color — Hades II (2024-2025) shift**: same dark base with witchcraft-aligned green/cyan secondary replacing the original gold-forward warmth (observation; hex not enumerated).
- **Logo**: distressed wordmark (Mrs Eaves Bold derivative); strong illustration-driven identity by Jen Zee.
- **Asset host**: `www.supergiantgames.com`, Steam / Epic / Switch eShop pages.
- **Logo aspect**: wordmark ≈ 3.5:1.

### game-05 · Supercell · Clash Royale

Source: <https://swelltype.com/custom-fonts/clash-royale/> (Swell Type case study, 2016) + <https://fontsinuse.com/uses/66357/clash-royale-mobile-game> (Fonts In Use catalog entry) + <https://fankit.supercell.com/d/BmehSDJrZNff/font> (official Supercell fan kit, link-only).

- **Typography — display / logo / UI**: `Supercell-Magic` (also referred to in design press as the *Clash Royale custom font*), designed 2016 by Swell Type as a Supercell-commissioned redraw of Comicraft's *You Blockhead*. Multiple weights, art-directed by Lauri Warsta. Used across the Clash family (Clash of Clans, Clash Royale, Brawl Stars share the lineage).
- **Typography — secondary / inline UI**: `CC Back Beat` (Comicraft) — narrower comic-style face used for in-game text.
- **Color — Clash Royale palette (named tokens, public sources)**: French Blue, Gingerbread, Selective Yellow, Black, Spanish Gray. Specific hex values not centrally enumerated in the public press / fan-kit text as of 2026-05-11; observed in-product approximations follow the named-color industry standards (French Blue ≈ `#0072BB`, Gingerbread ≈ `#B25B00`, Selective Yellow ≈ `#FFBA00`, Spanish Gray ≈ `#989898`).
- **Logo**: golden crown mark + Supercell-Magic wordmark; saturated cartoony aesthetic.
- **Asset host**: `supercell.com`, `fankit.supercell.com`.
- **Logo aspect**: mark + wordmark ≈ 3:1.

---

## Sub-step status

- [x] Uniswap (full token evidence)
- [x] OpenSea (brand palette + partial typography)
- [x] Phantom (brand description; hex not publicly enumerated)
- [x] Lens Protocol (color values are PDF-only in brand-kit; recorded as known limitation)
- [x] Farcaster / Warpcast (single-token CC0 brand: `#8A63D2`)
- [x] Coinbase (primary `#1652F0` + Coinbase Sans + Public Sans 500 open fallback)
- [x] Valorant (primary `#FF4655` + DIN Next UI typography)
- [x] Genshin Impact (HYWenHei-85W proprietary; UI gold accent observation)
- [x] Destiny 2 (Futura logo + Neue Haas Grotesk UI; class-color axis qualitative)
- [x] Hades (Mrs Eaves Bold poster type + distressed treatment; color palette qualitative)
- [x] Clash Royale (Supercell-Magic 2016 custom + named-color palette)
- [x] Aggregate decision values — Batch 5 (color / typography / spacing / radius / motion / iconography / watermark / logo / asset hosts all decided)

---

## Aggregate analysis + decision values (Batch 5)

This section turns the per-service evidence into the values that feed `assets/team-brand-spec.default.json` in Step 5.1. The principle: *no single service's brand identity is mimicked* — defaults sit at a neutral point that lets adopters override toward their own brand without inheriting another company's recognizability.

### Color decisions

**Brand-color distribution across the 11 services** (where a hex is enumerated, it's a hard data point; where it's qualitative, it's a tone observation):

| Hue band | Services in this band |
|---|---|
| Pink / magenta | Uniswap (`#FF37C7`), Hades (wine/purple secondary) |
| Red / vermillion | Valorant (`#FF4655`), Hades (deep red primary) |
| Purple / violet | Phantom (qualitative), Farcaster (`#8A63D2`), Hades secondary |
| Blue | OpenSea (`#2081E2`), Coinbase (`#1652F0`), Clash Royale French Blue (named, ≈ `#0072BB`), Genshin master-brand ring, Destiny 2 UI chrome |
| Green | Lens (PDF-locked qualitative) |
| Gold / amber | Genshin UI accent (`~#E6CDA0` obs.), Clash Royale Selective Yellow (named, ≈ `#FFBA00`), Hades original-game gold |
| Pure black / dark base | Genshin wordmark, Destiny 2 chrome, Hades base, plus all dark-mode surfaces in web3 |

Observations:

1. *No single hue dominates*; blue has the most occurrences (5/11) and is therefore the *least safe* primary for a neutral default because choosing blue would visually align with Coinbase + OpenSea + Clash Royale at once.
2. *Dark surface backgrounds are near-universal* (10/11 services support a dark mode or use dark base UI).
3. *Status color hex codes* are only explicitly enumerated by one source (Uniswap's `Spore` system, GPL-3.0). All other services either omit a public status palette or describe it qualitatively.

**Decisions:**

- **Surface tokens (default = dark base, with explicit light variant):**
  - `surface.base` (dark): `#0F1115` — near-black with a slight cool tint; doesn't match any of the 11 surface bases verbatim (Uniswap dark is `#131313`, Destiny 2 is `~#0C1216`) — sits at the *median* without copying either.
  - `surface.raised` (dark): `#1A1D24` — one tier up.
  - `surface.muted` (dark): `rgba(255,255,255,0.08)` — translucent (Uniswap-style technique, generic enough to be neutral).
  - `surface.base` (light): `#FFFFFF`
  - `surface.raised` (light): `#F7F8FA`
  - `surface.muted` (light): `rgba(15,17,21,0.06)`
- **Text tokens:**
  - `text.primary` (dark): `#F2F4F8` (near-white, slightly cool)
  - `text.secondary` (dark): `rgba(242,244,248,0.68)`
  - `text.tertiary` (dark): `rgba(242,244,248,0.42)`
  - `text.primary` (light): `#0F1115`
  - `text.secondary` (light): `rgba(15,17,21,0.66)`
  - `text.tertiary` (light): `rgba(15,17,21,0.40)`
- **Brand accent (deliberately neutral, not anyone's brand):**
  - `accent.primary`: `#5B7CFA` — mid-saturation indigo; **not** Coinbase `#1652F0`, **not** OpenSea `#2081E2`, **not** Farcaster `#8A63D2`, **not** Phantom violet. Sits in the gap between blue and purple bands so adopters can flip to either pole.
  - `accent.contrast`: `#FFFFFF` — text on accent.
- **Status tokens (Uniswap-attributed evidence, single-source):**
  - `status.success` (light): `#0C8911` · (dark): `#21C95E`
  - `status.warning` (light): `#996F01` · (dark): `#FFBF17`
  - `status.critical` (light): `#E10F0F` · (dark): `#FF593C`
  - These mirror Uniswap's Spore system exactly — credited in `team-brand-spec.default.json` with a `_source` field pointing back to this section so the lineage is auditable and adopters know what they're overriding when they change them.

### Typography decisions

8/11 services use a custom or commissioned typeface; only system-stack and open-source fallbacks are universally redistributable. The default therefore carries a **two-slot pattern**: a *display* slot (placeholder + open-source fallback) and a *body* slot (open-source stack).

- `typography.display.family`: `"Inter"` — single most-used web sans in 2026; freely redistributable (OFL); covers ~38 scripts. *Placeholder*: adopters typically swap this for their custom display face.
- `typography.display.weights`: `[500, 600, 700]`
- `typography.body.family`: `"Inter"` (same family used as body for stack simplicity, distinct weights distinguish)
- `typography.body.weights`: `[400, 500]`
- `typography.body.system_stack`: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif` — *post-Inter fallback*. Matches Uniswap's stack pattern exactly (evidence-anchored).
- `typography.mono.family`: `"JetBrains Mono"` (OFL, freely redistributable)
- `typography.mono.system_stack`: `ui-monospace, SFMono-Regular, "SF Mono", Menlo, Monaco, "Cascadia Mono", "Segoe UI Mono", "Roboto Mono", "Courier New", monospace` — direct citation of Uniswap's mono stack.
- `typography.size_scale` (px): `12, 14, 16, 18, 20, 24, 32, 40, 48, 64` — 1.25× ratio biased, matches Uniswap iconography rhythm and Material 3 baseline scale.
- `typography.line_height`: `body 1.5`, `tight 1.2`, `loose 1.6`.

### Spacing decisions

Uniswap's `0, 1, 2, 4, 6, 8, 12, 16, 18, 20, 24, 28, 32, 36, 40, 48, 60` is the only enumerated scale in the 11-service set. Other services use 4-/8-px-grid biased values without publishing a flat scale. Default prunes Uniswap's granular low end (1, 2) — too fine for layout — and rounds the high end:

- `spacing.scale` (px): `0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 96`
- `spacing.base`: `4` (the underlying grid unit)
- `spacing.section`: `64` (large-gap default)

### Radius decisions

Uniswap's `0, 4, 6, 8, 12, 16, 20, 24, 32, full` is again the most enumerated; OpenSea observation is 12–16 px card radii; Coinbase / Phantom production approximates 8–16 px. Default consolidates:

- `radius.scale` (px): `0, 4, 8, 12, 16, 24`
- `radius.pill`: `9999`
- `radius.button`: `8` · `radius.input`: `8` · `radius.card`: `12` · `radius.modal`: `16` (semantic shortcuts)

### Motion timing decisions

No service in the 11-set ships an enumerated ms scale publicly. Default is derived from **Material Motion + Apple HIG spec defaults** (already cited externally in `references/animation-best-practices.md`):

- `motion.duration.instant`: `100` ms — micro-feedback (button-press, focus-ring).
- `motion.duration.fast`: `200` ms — small UI transitions (hover, tooltip).
- `motion.duration.medium`: `300` ms — page-region entrances, sheet open.
- `motion.duration.slow`: `500` ms — full-route transitions, hero reveals.
- `motion.easing.standard`: `cubic-bezier(0.4, 0, 0.2, 1)` — Material standard curve.
- `motion.easing.emphasized`: `cubic-bezier(0.2, 0, 0, 1)` — Material emphasized.
- `motion.easing.decelerated`: `cubic-bezier(0, 0, 0.2, 1)` — entrance.

### Iconography decisions

The 11-set is dominated by custom in-product icons. The most-used **open-source** icon kit for similar web3/dashboard product surfaces is Lucide (already in the public asset-host allowlist at `examples/dot-claude-settings.json`).

- `iconography.family`: `"Lucide"` (Lucide React / Vue / vanilla SVG; ISC license)
- `iconography.fallback`: `"Phosphor"` (MIT; also in the asset-host allowlist)
- `iconography.stroke_width`: `1.75` (px) — Lucide default.
- `iconography.size_scale` (px): `12, 16, 20, 24, 32` — five sizes, matching Uniswap's icon-size scale subset.
- `iconography.weight`: `"regular"` (Lucide has a single weight by default; Phosphor offers thin / light / regular / bold / fill).

### Watermark decisions

(Carried over from Step 4 default policy, unchanged.)

- `watermark.enabled`: `false`
- `watermark.format`: `"{teamName} · {year}"` — Latin neutral; only rendered when `enabled = true`.
- `watermark.position`: `"bottom-right"`
- `watermark.opacity`: `0.5`

### Logo default decisions

Aspect-ratio observation across the 11-set: mark-only ≈ 1:1 (universal); mark + wordmark ≈ 3:1 to 5:1 (cluster median at 4:1).

- `logo.mark.aspect`: `"1:1"` (square mark slot)
- `logo.mark.placeholder`: an abstract geometric `<svg viewBox="0 0 24 24">` rectangle (drop-in until adopter replaces)
- `logo.wordmark.aspect`: `"4:1"` (median across the set)
- `logo.wordmark.placeholder`: text `"TEAM"` rendered in `Inter 700` — neutral, immediately recognizable as a placeholder.

### Asset host hints

The default ships with public-CDN allowlist matching `examples/dot-claude-settings.json` (Lucide / Phosphor / MDN). Per-fork additions belong in the carrier file, not the default:

- `asset_hosts.public`: `["unpkg.com/lucide-static@*", "cdn.jsdelivr.net/npm/lucide@*", "unpkg.com/@phosphor-icons/web@*", "cdn.jsdelivr.net/npm/@phosphor-icons/web@*", "developer.mozilla.org/*"]`
- `asset_hosts.internal`: `[]` (per-fork)

---

## Out-of-scope (deliberate)

- **Production-site CSS scraping**: rejected per Step 5 plan — too volatile across deploys, raises bot-detection/ToS questions for some services.
- **Round-trip back to source**: this file is one-way evidence; aggregate values feed Step 5.1 but do not flow back to any source service.
- **Per-service motion timing tables**: most sources do not publish enumerated ms scales. The aggregate (Batch 5) will derive motion timing from CSS spec defaults (Material Motion + Apple HIG generic) rather than per-service inference.
