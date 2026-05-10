# Design Philosophy Catalog · 18 directions

> A flat catalog (no schools, no grid). Eighteen design directions
> the agent can recommend when a brief is vague — pick one before
> generating, and it sets the rules for typography, color, motion,
> and chrome.
>
> The first **14** are author-original to this skill (2026-05-10).
> The last **4** (§15–18, the game / web3 domain pack) carry over
> verbatim from the maintainer's prior fork-author work in the
> predecessor repo's Phase 4 — same author, same IP, just relocated.
> Section numbering shifts (predecessor §21–24 → this catalog
> §15–18); prose is unchanged.

---

## How to use this catalog

When the user's brief is anything more concrete than "make it
look nice", the brief itself constrains the philosophy choice —
default to whatever the brief points at. When the brief is
genuinely vague:

1. **Pick one philosophy** before generating. Mixing two is allowed
   only when the brief explicitly asks for a combination, and even
   then only when the two philosophies share a typographic or
   palette stance (e.g. *editorial-identity* + *atmospheric
   gradient (deliberate)* both stay restrained; *kinetic
   typographic poster* + *documentary photographic* fight each
   other).
2. **Cite the philosophy in Stage 2 reasoning** (see
   `SKILL.md ## Junior Designer workflow`). The reasoning
   paragraph names the philosophy and the studio lineage, so a
   reviewer can push back on the direction itself, not just the
   pixels.
3. **Use the Prompt DNA blocks verbatim** when reaching for
   Codex / gpt-image-2 illustrations. The DNA blocks are tuned
   so a `codex exec` call lands in the right aesthetic without
   further prompting.
4. **External references stay external.** This catalog cites the
   reference works — it does not paraphrase them. If the user
   asks for "more Pentagram", open Pentagram's site; don't
   regenerate from this entry.

---

## The eighteen directions

### 01 — Editorial-identity (Pentagram / Build / Atlas lineage)

**Philosophy**: the brand is the wordmark and the whitespace around it; everything else is chrome to remove.

**Signature traits**:
- Wordmark or single graphic device dominates; chrome stays absent
- Asymmetric grid, generous whitespace; nothing centers by default
- One restrained accent (often desaturated); type carries the weight
- Photography or single graphic device, never both — pick one and let it own the page
- Type pairing reads as a deliberate choice, not "Inter + system fallback"

**Prompt DNA**:
```
Editorial-identity aesthetic (Pentagram / Build Studio / Atlas Magazine lineage):
- Wordmark or monogram dominates; surrounding chrome strips out
- Asymmetric grid, generous whitespace, nothing centered by default
- One restrained accent (desaturated); large display type, hairline rules
- Either photography or graphic device — never both on the same page
- Display + body type pairing is intentional (e.g. GT Sectra display + Söhne body)
- No glass, no gradient, no animated background
```

**Representative work**: [Pentagram New York](https://www.pentagram.com/work) · [Build Studio](https://www.build.london) · [Atlas Magazine](https://atlas.com)

**Search keywords**: pentagram brand identity case studies · build studio projects · atlas magazine art direction

---

### 02 — Neo-grotesque utility (Stripe / Linear / Vercel docs lineage)

**Philosophy**: the product is a tool; restraint is the trust signal.

**Signature traits**:
- 13–14 px UI body, hairline borders, no gradient
- Tabular numerals everywhere a number appears
- Monochrome palette + 1 accent reserved for state semantics
- Comfortable click targets despite the small body type
- Single typeface family at 4–5 weights (Inter, Geist, Söhne)

**Prompt DNA**:
```
Neo-grotesque utility aesthetic (Stripe / Linear / Vercel docs lineage):
- 13-14 px UI body, hairline 1 px borders, monochrome palette
- Single accent color used only for state semantics (info / success / warn / danger)
- Tabular monospaced numerals; data is the primary content
- Comfortable density: small type, large click targets
- Single sans family at 4-5 weights (no display vs body split)
- No gradient, no shadow drama, no decorative motion
```

**Representative work**: [Stripe](https://stripe.com) · [Linear](https://linear.app) · [Vercel docs](https://vercel.com/docs)

**Search keywords**: stripe.com design system · linear.app ui breakdown · vercel docs typography

---

### 03 — Brutalist reactive (Are.na / Pirx / contemporary indie web)

**Philosophy**: reject the polish; the unfinished is the look.

**Signature traits**:
- Thick black borders, hard color blocks, intentional misalignment
- Monospace headlines or system-default body
- Underline / strikethrough / marker-style annotation as ornament
- Few rasters; HTML, SVG, and type carry the page
- One vivid accent (acid green, hot pink, cobalt) on off-white or off-black

**Prompt DNA**:
```
Brutalist reactive aesthetic (Are.na / Pirx Studio / contemporary indie web):
- Thick (3-5 px) black borders, hard color blocks, no soft shadows
- Monospace or system-default typography; embrace the system feel
- Underline / strikethrough / marker-style annotation as ornament
- 1 vivid accent (acid green / hot pink / cobalt) on off-white background
- HTML / SVG / type only — no raster photography, no glass
- Slight intentional misalignment; nothing is grid-perfect
```

**Representative work**: [Are.na](https://www.are.na) · [Pirx Studio](https://pirx.studio) · [Useful Books](https://usefulbooks.com)

**Search keywords**: are.na ui design · brutalist web design 2025 · indie portfolio brutalist

---

### 04 — Editorial-spatial cinematic (Active Theory / Field.io / Resn lineage)

**Philosophy**: scrolling is a camera move; the page is a stage.

**Signature traits**:
- Scroll-triggered transforms, parallax depth, hero video moments
- Large display type drifts, fades, scales as story beats land
- WebGL / canvas reserved for one or two narrative cues, not background décor
- Cinematic transitions between sections (fade-to-color, push, dolly-in)
- Sound and `prefers-reduced-motion` treated as first-class concerns

**Prompt DNA**:
```
Editorial-spatial cinematic aesthetic (Active Theory / Field.io / Resn lineage):
- Scroll-triggered transforms; the page reveals itself as a camera move
- Large display type drifts, fades, scales on scroll beats
- Optional WebGL / canvas moment for ONE narrative cue (not background décor)
- Cinematic transitions between sections (fade-to-color, push, dolly-in)
- Hero video plays once and parks, not loops on autoplay-mute
- prefers-reduced-motion respected; everything has a static fallback
```

**Representative work**: [Active Theory](https://activetheory.net) · [Field.io](https://field.io) · [Resn](https://resn.co)

**Search keywords**: active theory case studies · field.io interactive · resn portfolio

---

### 05 — Apple-system glass (HIG iOS 18 / macOS Sonoma materials)

**Philosophy**: surface materials carry depth where it belongs — on interactive layers, not behind everything.

**Signature traits**:
- Frost / blur reserved for command palettes, sheets, popovers — never default cards
- SF Pro / SF Pro Display at platform scale (17 pt body, 13 pt caption)
- Native control feel: rounded buttons, segmented controls, sheet edges
- Subtle ambient gradient on background (rare), opaque cards on top
- `prefers-reduced-motion` and `prefers-reduced-transparency` respected

**Prompt DNA**:
```
Apple-system glass aesthetic (HIG iOS 18 / macOS Sonoma materials):
- Frost / blur on interactive layers only (sheets, popovers, command palettes)
- SF Pro Display + SF Pro Text; 17 pt body, 13 pt caption, system scale
- Rounded native buttons, segmented controls, native sheet drag-handle
- Subtle ambient gradient on background (low saturation), opaque cards
- Light + Dark variants both first-class; not afterthought
- prefers-reduced-motion / -transparency respected by default
```

**Representative work**: [Apple HIG · Materials](https://developer.apple.com/design/human-interface-guidelines/materials) · [iOS 18 marketing](https://www.apple.com/ios/ios-18) · [Things 3](https://culturedcode.com/things)

**Search keywords**: apple HIG materials guidelines · ios 18 design analysis · sf symbols ui

---

### 06 — Print-translation editorial (New Yorker / The Pudding / NYT magazine lineage)

**Philosophy**: bring the magazine to the screen — typography drives the layout, not blocks.

**Signature traits**:
- Drop caps, ligatures, mixed serif (display) + sans (body) at deliberate ratios
- Asymmetric column widths; pull-quotes; running heads
- Reading-first hierarchy — long-form essay layout, even on landing pages
- Photography full-bleed and infrequent; type carries 90 % of the page
- Section divisions feel like chapter changes, not nav

**Prompt DNA**:
```
Print-translation editorial aesthetic (New Yorker digital / NYT magazine / The Pudding):
- Drop caps, ligatures, mixed serif (display) + sans (body) typography
- Asymmetric column widths; one-column long-form, side notes, pull-quotes
- Page reads as essay first, then nav — reading-first hierarchy
- Photography full-bleed and rare; type carries 90% of the page
- Chapter-style section divisions (rule + roman numeral + drop cap)
- No glass, no gradient, no decorative motion
```

**Representative work**: [The New Yorker · long reads](https://www.newyorker.com/magazine) · [The Pudding](https://pudding.cool) · [NYT Magazine](https://www.nytimes.com/section/magazine)

**Search keywords**: new yorker digital long form · the pudding visual essays · nyt magazine feature design

---

### 07 — Data-dense ledger (Bloomberg / DefiLlama / Polymarket lineage)

**Philosophy**: every pixel earns its place by carrying information.

**Signature traits**:
- Monospaced tabular numbers across the whole UI, not just data tables
- Row-based hierarchy — sortable, filterable, deep-nested rows
- Sparkline + delta + state color around every metric, never lone numbers
- Neutral grayscale + 4-color state palette (info / success / warn / danger)
- Density toggle (compact / cozy / comfortable); compact is the working default

**Prompt DNA**:
```
Data-dense ledger aesthetic (Bloomberg Terminal / DefiLlama / Polymarket lineage):
- Monospaced tabular numbers across all UI, not just data tables
- Row-based hierarchy with sort, filter, expand-deep
- Sparkline + delta + state color around every metric, never lone numbers
- Neutral grayscale palette + 4 state colors (info / success / warn / danger)
- Density toggle (compact / cozy / comfortable); compact = default
- Charts inline at row scale (not large hero panels)
```

**Representative work**: [Bloomberg Terminal · Wikipedia](https://en.wikipedia.org/wiki/Bloomberg_Terminal) · [DefiLlama](https://defillama.com) · [Polymarket](https://polymarket.com)

**Search keywords**: bloomberg terminal ui · defillama dashboard design · polymarket ui

---

### 08 — Atmospheric gradient (deliberate) (Vercel 2024 / OpenAI / Anthropic lineage)

**Philosophy**: gradients live as ambient atmosphere — diffuse, off-stage, rare. Identity stays restrained around them.

**Signature traits**:
- Single soft gradient on background, low saturation, slow movement (or static)
- Type and chrome stay neutral — no gradient on text, no gradient on buttons
- One accent color, used sparingly (button, focus ring)
- Wide whitespace; gradient never crowds content
- No glassmorphism (the foreground stays opaque)

**Prompt DNA**:
```
Atmospheric gradient aesthetic (Vercel 2024 / OpenAI / Anthropic site lineage):
- Single soft diffuse gradient on background only; off-screen origin point
- Low saturation, narrow hue range (cool blues only, or warm oranges only)
- Type, chrome, buttons stay neutral and opaque — no gradient leakage
- Wide whitespace; gradient occupies <30% of any visible region
- One restrained accent (focus ring, primary button)
- No glassmorphism; foreground always opaque
```

**Representative work**: [Vercel](https://vercel.com) · [OpenAI](https://openai.com) · [Anthropic](https://www.anthropic.com)

**Search keywords**: vercel 2024 marketing design · openai homepage gradient · anthropic site

---

### 09 — Soft-tactile / paper-like (Things 3 / Notion 2024 / Maven lineage)

**Philosophy**: the interface is calm — soft shadows, paper-like surface, large radii.

**Signature traits**:
- Layered soft shadows (not crisp); paper-like cards on textured background
- Large radii (20–32 px); generous internal padding
- Muted palette (warm whites, beige, gray); 1 desaturated accent
- Friendly typography (Söhne, Untitled Sans, or Inter at relaxed line-height)
- Gentle micro-interactions only; the surface stays still

**Prompt DNA**:
```
Soft-tactile / paper-like aesthetic (Things 3 / Notion 2024 / Maven lineage):
- Layered soft shadows on cards; paper-like material, slightly off-white
- Large radii (20-32 px); generous internal padding
- Muted warm palette (beige, soft gray, off-white); 1 desaturated accent
- Friendly sans (Söhne, Untitled Sans) at relaxed 1.5-1.6 body line-height
- Gentle hover states (lift, tint); nothing fast-paced
- No glass, no neon, no aggressive gradient
```

**Representative work**: [Things 3 · Cultured Code](https://culturedcode.com/things) · [Notion 2024 redesign](https://www.notion.so) · [Maven](https://maven.com)

**Search keywords**: things 3 ios design · notion 2024 redesign analysis · maven cohort platform UI

---

### 10 — High-contrast graphic poster (Bauhaus / MoMA digital / Verso Books lineage)

**Philosophy**: a poster on the screen — bold, declarative, impossible to ignore.

**Signature traits**:
- Oversized type (20+ vw) carries whole sections; hierarchy is obvious
- Three-color discipline: black, white, one vivid (red, yellow, electric blue)
- Hard geometric shapes (circles, hard-stop diagonals, blocks)
- SVG illustration over photography; flat, bold outlines
- Display type pair (Druk, GT America Mono) with a quiet sans body

**Prompt DNA**:
```
High-contrast graphic poster aesthetic (Bauhaus / MoMA digital / Verso Books):
- Oversized display type (20+ vw) anchors each section
- Three-color discipline: black, white, one vivid (red, yellow, electric blue)
- Hard geometric shapes (circles, diagonals, blocks); no soft curves
- SVG illustration only — flat, bold outlines, no shading
- Strong display type (Druk, GT America Mono) + quiet sans body
- No photography, no gradient, no glass
```

**Representative work**: [MoMA online](https://www.moma.org/collection) · [Verso Books](https://www.versobooks.com) · [Bauhaus archive](https://www.bauhaus.de/en)

**Search keywords**: moma digital site design · verso books typography · bauhaus poster design archive

---

### 11 — Editorial dark (Pitchfork / Substack reader / Are.na dark lineage)

**Philosophy**: dark mode for reading, not for gaming — warm, content-first, restrained.

**Signature traits**:
- Off-black background (#0F0F0F or warmer #1A1612), never pure #000
- Body type 95 % white; muted text 60 %
- Single warm accent (amber, off-red, faded yellow); no cyan / magenta
- Serif body acceptable here (Tiempos, Crimson Pro, Charter)
- Generous spacing; no compressed cards, no glow

**Prompt DNA**:
```
Editorial dark aesthetic (Pitchfork dark / Substack reader / Are.na dark):
- Off-black background (#0F0F0F or warmer #1A1612); not pure black
- Body type 95% white; muted text 60%; never harsh stark contrast
- Single warm accent (amber, off-red, faded yellow); no cyan / magenta
- Serif body type is acceptable here (Tiempos, Crimson Pro, Charter)
- Generous spacing, no compressed cards, no glow effects
- Reading-mode hierarchy — long-form essay layout, even on grids
```

**Representative work**: [Pitchfork](https://pitchfork.com) · [Substack reader](https://substack.com/app) · [Are.na (dark)](https://www.are.na)

**Search keywords**: pitchfork dark mode design · substack reader ui · are.na dark mode

---

### 12 — Component-system minimal (Linear / Radix Themes / shadcn-ui lineage)

**Philosophy**: tokens, not designs — every surface is composed from a small set of named tokens.

**Signature traits**:
- Token-driven palette (`background`, `foreground`, `muted`, `accent`, `destructive`)
- Single radius scale (sm / md / lg) used consistently across button, card, input
- Focus-visible ring on every interactive element (token-driven, not ad-hoc)
- Light + dark themes via CSS variables; identical layout in both
- Comfortable density default with optional compact mode

**Prompt DNA**:
```
Component-system minimal aesthetic (Linear / Radix Themes / shadcn-ui lineage):
- Token-driven palette (background, foreground, muted, accent, destructive)
- Single radius scale (sm / md / lg); applied consistently across components
- Every interactive element has a token-driven focus-visible ring
- Light + dark themes via CSS variables; identical layout in both
- Minimal chrome; no decorative gradient, no shadow drama
- Comfortable density default; compact toggle for power users
```

**Representative work**: [Linear](https://linear.app) · [Radix Themes](https://www.radix-ui.com/themes) · [shadcn/ui](https://ui.shadcn.com)

**Search keywords**: linear.app component system · radix themes design tokens · shadcn ui case studies

---

### 13 — Kinetic typographic poster (DIA Studio / Pangram Pangram / Hyperaktiv lineage)

**Philosophy**: type is not placed — type performs.

**Signature traits**:
- Variable fonts animate weight, width, slant on hover or scroll
- Hero is a typographic sequence (a word morphs into another, then resolves)
- Type occupies 90 % of what's on screen; chrome is minimal
- One bold accent at most; usually monochrome
- Scroll or pointer drives motion; idle state is still

**Prompt DNA**:
```
Kinetic typographic poster aesthetic (DIA Studio / Pangram Pangram / Hyperaktiv lineage):
- Variable fonts animate weight / width / slant on hover or scroll
- Hero is a typographic sequence — word morphs to another word
- Type occupies 90% of the visible region; chrome is minimal
- Monochrome or single bold accent; typography carries the brand
- Scroll / pointer drives motion; idle state is still
- No glass, no gradient, no rasters — vector + type only
```

**Representative work**: [DIA Studio](https://dia.tv) · [Pangram Pangram](https://pangrampangram.com) · [Hyperaktiv](https://www.hyperaktiv.tools)

**Search keywords**: dia studio variable typography · pangram pangram showcase · hyperaktiv portfolio

---

### 14 — Documentary photographic (Magnum / M Le Mag / Atlas Obscura lineage)

**Philosophy**: real photography drives the page; everything else gets out of the way.

**Signature traits**:
- Full-bleed photography sequenced for storytelling (3–7 images per run)
- Captions in small mono / grotesk; restrained, never decorative
- Site chrome appears only in quiet sections — image regions stay clear
- 2-up or 3-up photo grids at large format; never thumbnail mode
- Type stays out of the way of imagery; pull-quotes between photo runs

**Prompt DNA**:
```
Documentary photographic aesthetic (Magnum / M Le Mag / Atlas Obscura lineage):
- Full-bleed photography sequenced as story (3-7 images per run)
- Captions in small mono / grotesk; restrained, never decorative
- Site chrome appears ONLY in quiet sections — image regions stay clear
- 2-up or 3-up photo grids at large format; never thumbnail mode
- Type stays out of the way of imagery; pull-quotes between photo runs
- Subtle film-grain or duotone treatments for cohesion (optional)
```

**Representative work**: [Magnum Photos](https://www.magnumphotos.com) · [M Le Mag du Monde](https://www.lemonde.fr/m-le-mag) · [Atlas Obscura](https://www.atlasobscura.com)

**Search keywords**: magnum photos digital design · m le mag layout · atlas obscura photography pages

---

## Game / web3 domain pack — carried over verbatim from prior fork-author work

The four entries below were authored by the same maintainer in the
predecessor fork's Phase 4 (`references/design-styles.md §21–24` in
that repo). They are fork-author IP and carry over to this clean-room
rewrite verbatim. Numbering shifts from §21–24 to §15–18 in this
catalog; the prose itself is unchanged.

### 15 — Game HUD · Diablo / Destiny / Genshin lineage
**Philosophy**: the UI is consumable in 200ms while the player is doing something else
**Signature traits**:
- Heavy **affordance signaling** (clear hit/miss, cooldown, resource bars)
- Edge-anchored layout (corners + bottom strip, center stays clear for action)
- Strong **state vocabulary** (active / charging / ready / locked) with distinct shapes, not just colors
- Diegetic vs non-diegetic split: diegetic chrome (in-world) for ambient state, non-diegetic overlays for menu / inventory
- Color is functional, not decorative (red = enemy/health, gold = currency, blue = mana/cooldown)

**Prompt DNA**:
```
Game HUD aesthetic (Diablo / Destiny / Genshin lineage):
- Edge-anchored UI; center of frame reserved for gameplay
- Diegetic ambient indicators (in-world bars, glow on the character)
- Non-diegetic overlay menus with strong affordance: distinct shapes for state
- Functional color: red=danger, gold=reward, blue=cooldown, green=stat-up
- Dense iconography, but every icon has a single unambiguous meaning
- Read in <200ms — no decorative type, no body copy in the HUD
```

**Representative work**: Genshin Impact in-game HUD; Destiny 2 ghost UI
**Search keywords**: genshin impact UI design analysis · destiny 2 hud breakdown

---

### 16 — Web3 Minimalism · Uniswap / Lens / Farcaster lineage
**Philosophy**: the trust signal is restraint
**Signature traits**:
- **Type-first** (Inter / Söhne / IBM Plex), heavy whitespace, almost no decoration
- Single accent color (purple / pink / green) used sparingly
- **Numbers as the visual focus** (price, volume, APY, balance) — large, mono-tabular, often with 4–6 decimal places
- Wallet address as a recognizable visual primitive (truncated `0x1234…abcd` + jazzicon / blockie)
- Compact, dense data tables — mobile-first, but desktop-mockable
- Anti-skeuomorphism: no fake "card" shadows, no glassmorphism, no gradient buttons

**Prompt DNA**:
```
Web3 minimalist aesthetic (Uniswap / Lens / Farcaster lineage):
- Heavy whitespace, single accent (purple/pink/green)
- Numbers in tabular-mono are the visual focus (large display sizes)
- Wallet addresses styled as truncated hex + jazzicon
- Restraint as trust signal — no glow, no glass, no gradient
- Inter or IBM Plex Mono typography
- Mobile-first dense tables; desktop is the same, scaled
```

**Representative work**: Uniswap v3 swap interface · Lens.xyz profile · Warpcast / Farcaster client
**Search keywords**: uniswap v3 ui · lens protocol design system · farcaster client UI

---

### 17 — NFT Marketplace · OpenSea / Blur / Magic Eden lineage
**Philosophy**: the artwork is the product; the chrome stays out of its way
**Signature traits**:
- **Image-first cards** (the art occupies 70%+ of card area)
- Dark mode default (artwork pops against dark)
- Floor price + last-sale + rarity rank as the only info on cards
- Hover states reveal more (collection, holder count, traits)
- Grid-driven layouts (4-up / 6-up / 8-up; user picks density)
- Owner identity is secondary (small avatar + truncated wallet at the bottom)

**Prompt DNA**:
```
NFT marketplace aesthetic (OpenSea / Blur / Magic Eden lineage):
- Image-first card layout (70%+ of card is the art)
- Dark mode default (#0E0E10 or similar near-black)
- 3 data points max on the card: floor / last sale / rarity
- Hover or click reveals: collection, holders, traits
- Dense grid (4/6/8-up toggle)
- Wallet address as identity, jazzicon as avatar
```

**Representative work**: OpenSea collection page · Blur trending feed · Magic Eden Solana grid
**Search keywords**: opensea collection page UI · blur marketplace UI · magic eden NFT grid

---

### 18 — Onboarding-Game-Loop · Polished mobile game / web3 onboarding hybrid
**Philosophy**: every screen is a level — small clear win, then the next one
**Signature traits**:
- **One action per screen** (no menus, no choices — the next button is the only thing to do)
- Progress visible at all times (step 3 of 7, or a horizontal pill row)
- Reward feedback: every step end has a small affirmation (haptic + animation + sound)
- Friction-allergic: no email-and-password, no captchas; if auth is needed, social or wallet
- Story / mascot threading: a character or visual motif runs through every step
- Return visit: the game-loop continues — daily missions, streak counter, collection view

**Prompt DNA**:
```
Polished onboarding game-loop aesthetic:
- One action per screen, large primary button bottom-anchored
- Progress dots / pills always visible at top
- Reward ping at the end of each step (small animation, no body copy)
- Mascot or visual motif consistent across screens
- Frictionless auth (social / wallet, never email+password)
- Daily/streak hooks for return visits (compact summary card)
```

**Representative work**: Duolingo onboarding · Wallet onboarding (Phantom / Rainbow / Coinbase Wallet first launch) · Sandbox / Decentraland tutorial
**Search keywords**: duolingo onboarding UX · phantom wallet first launch · rainbow wallet onboarding

---

## When the brief is web3 / game

Default to entries §15–18 first. They cover most in-domain briefs
the maintainer ships against. The other 14 still apply when the
project sits on the marketing / brand layer rather than the
in-product layer (a wallet's marketing site benefits from
*editorial-identity* or *atmospheric gradient (deliberate)*; the
wallet itself benefits from *web3 minimalism*).

## Pairings that hold up

These two-philosophy combinations carry the same typographic /
palette stance, so they don't fight each other:

- *editorial-identity* + *atmospheric gradient (deliberate)* — restrained marketing landing, brand-led gradient ambient.
- *neo-grotesque utility* + *data-dense ledger* — developer / financial dashboards.
- *editorial dark* + *editorial-spatial cinematic* — long-form essay with parallax storytelling.
- *web3 minimalism* + *editorial-identity* — token brand site that fronts a minimal wallet.
- *game HUD* + *onboarding-game-loop* — full game-product loop, in-game and pre-game.

These two-philosophy combinations **fight** each other and should
not be mixed:

- *kinetic typographic poster* vs *documentary photographic* — type-first vs image-first; one always wins.
- *brutalist reactive* vs *soft-tactile / paper-like* — opposite stances on polish.
- *high-contrast graphic poster* vs *editorial dark* — both demand a singular tonal vocabulary; they cancel.
- *atmospheric gradient (deliberate)* vs *NFT marketplace* — one needs negative space; the other needs density.
