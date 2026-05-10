# Scene Template Library · 9 templates

> Output-type-anchored layouts. When the user's brief points at a
> known shape (deck cover, app screen, infographic, NFT card), the
> matching scene template gives dimensions, layout primitives, and
> a copy-paste prompt block — to be paired with one or more design
> philosophies from `references/design-styles.md`.
>
> Templates **01–05** are author-original to this skill (2026-05-10).
> Templates **06–09** (game / web3 domain pack) carry over verbatim
> from the maintainer's prior fork-author work in the predecessor
> repo (`references/scene-templates.md §9–12`), with one functional
> change: the **Recommended philosophies** line in each carry-over
> has been re-numbered to point at this skill's design-styles
> catalog rather than the predecessor's. All other prose is
> unchanged. The numbering shift (predecessor §9–12 → this catalog
> §06–09) is purely positional.

---

## How to use this catalog

When the brief is concrete ("design our login screen", "make a
deck cover for the seed talk"), the brief itself selects the
template — match it, then pair with a philosophy.

When the brief is vague:

1. **Pick the scene template first**, then the philosophy.
   Templates anchor *what's on the canvas* (an app screen vs a
   deck slide vs an infographic); philosophies anchor *how it
   should feel*. Same template + different philosophy = same
   layout, different aesthetic; that's the point.
2. **Cross-reference numbers**: every template lists 2–3
   compatible philosophies from `references/design-styles.md`
   by number. The first listed is the strongest match;
   alternates exist for variation.
3. **Use the prompt template verbatim** for `codex exec` /
   `gpt-image-2`. Replace `[insert philosophy DNA here]` with the
   matching Prompt DNA block from the catalog. Two copy-pastes
   land you at the right intersection.
4. **One template per artifact.** Mixing templates in a single
   artifact (deck cover with app-screen overlay, infographic with
   game HUD elements) is a smell — split into two artifacts and
   compose them, don't fuse.

---

## The nine templates

### 01 — Deck cover slide / hero

**Specs**:
- 1920×1080 (16:9) default — see `assets/deck_stage.js`
- 1080×1080 (square) for social-share
- 1080×1920 (9:16) for mobile vertical decks
- Single canvas — never paginate the cover

**Key design elements**:
- Display headline two lines max, oversized (≥120 px on a 1920×1080 canvas), tight tracking
- Eyebrow row above the headline — date, chapter index, or brand wordmark; one line only
- Optional lede paragraph below the headline (18–22 px, muted) — drop entirely if the headline is the whole message
- Meta strip at the bottom (presenter name, domain, chapter index)
- Background: solid, single-hue gradient, **or** one image — pick one and commit; don't combine two

**Recommended philosophies**: §01 Editorial-identity · §08 Atmospheric gradient (deliberate) · §10 High-contrast graphic poster

**Scene prompt template**:
```
[insert philosophy DNA here]
- Deck cover slide, 1920x1080
- Display headline 2 lines max, oversized (120+ px), tight tracking
- Eyebrow row above the headline (date / chapter index / brand wordmark)
- Optional lede paragraph below (18-22 px, muted) — drop if the headline carries the meaning
- Meta strip at the bottom (presenter / domain / chapter index)
- Background: solid, single-hue gradient, OR one image — pick exactly one
```

---

### 02 — Mid-deck content slide

**Specs**:
- 1920×1080 (16:9) — same canvas as the cover, see `assets/deck_stage.js`
- One layout primitive per slide; if mixing is needed, split to two slides

**Key design elements**:
- Heading + sub-heading anchored top-left (~96 px / 24 px)
- Body region uses **one** layout primitive: bullets, two-column compare, 4-tile KPI, full-bleed quote, or table
- Page-number / footer chrome optional and restrained — declared once on the deck shell, not per slide
- Padding cadence consistent across the deck — heroes breathe, dense lists compress, but rhythm holds
- Speaker notes go in `<aside slot="notes">` (per `assets/deck_stage.js` API), not on the canvas

**Recommended philosophies**: §02 Neo-grotesque utility · §07 Data-dense ledger · §06 Print-translation editorial

**Scene prompt template**:
```
[insert philosophy DNA here]
- Mid-deck content slide, 1920x1080
- Heading + sub-heading anchored top-left
- ONE layout primitive: bullets / two-column compare / 4-tile KPI / quote / table
- No mixing of layouts on a single slide; split if needed
- Restrained page-number / footer chrome (optional, declared at deck shell)
- Speaker notes go to the aside, never the canvas
```

---

### 03 — Web hero with motion

**Specs**:
- 1440×900 default, 1920×1200 for full-bleed
- 390×844 mobile companion (status bar inset preserved by `<IosFrame>`)
- Above-the-fold only — below-the-fold reverts to standard content rules

**Key design elements**:
- Big display type (≈10 vw at desktop) as the primary entry point
- **One** narrative-driving motion: scroll-revealed transform, autoplay-once video, **or** a canvas hero — never all three
- CTA below the display type, centered or left-anchored — never floating in the gradient
- 6–8 elements maximum above the fold, including chrome (nav, eyebrow, headline, lede, CTA, mark)
- Reduced-motion fallback: a static composition that still tells the story

**Recommended philosophies**: §04 Editorial-spatial cinematic · §13 Kinetic typographic poster · §08 Atmospheric gradient (deliberate)

**Scene prompt template**:
```
[insert philosophy DNA here]
- Web hero, above-the-fold, 1440x900 desktop / 390x844 mobile companion
- Big display type (~10 vw) as the primary entry point
- ONE narrative motion: scroll-reveal / autoplay-once video / canvas hero — never all three
- CTA below the display type; centered or left-anchored, never floating
- 6-8 elements max above the fold, including chrome
- prefers-reduced-motion fallback that still tells the story
```

---

### 04 — Infographic / data narrative

**Specs**:
- 1080×1920 (9:16 vertical) for social-share long-scroll
- 1200×1500 for embed in articles / decks
- 1920×1080 for in-deck data slides

**Key design elements**:
- Reading order is obvious top-to-bottom (vertical) **or** left-to-right (landscape) — never diagonal, never both
- Hero metric or thesis at the start, supporting metrics in sequence, conclusion at the end
- Charts share the same color / stroke / label system across panels — variation between charts in one infographic is a layout failure
- Source citations footer always present, even on social-share format
- Type hierarchy explicit: thesis 60+ px, metric 36–48 px, body 16–18 px

**Recommended philosophies**: §07 Data-dense ledger · §06 Print-translation editorial · §02 Neo-grotesque utility

**Scene prompt template**:
```
[insert philosophy DNA here]
- Infographic / data narrative, [1080x1920 vertical / 1200x1500 embed / 1920x1080 in-deck]
- Reading order obvious: top-to-bottom OR left-to-right — never both, never diagonal
- Hero metric / thesis first, supporting metrics in sequence, conclusion last
- Charts share the same color / stroke / label system across panels
- Source citations footer always present
- Type hierarchy: thesis 60+ px, metric 36-48 px, body 16-18 px
```

---

### 05 — Mobile app screen mock

**Specs**:
- iPhone 15 Pro: 393×852 — wrap in `<IosFrame model="iphone15pro">` (`assets/ios_frame.jsx`)
- iPhone 15 Pro Max: 430×932 — `<IosFrame model="iphone15promax">`
- Pixel 8: 412×915 — `<AndroidFrame model="pixel8">` (`assets/android_frame.jsx`)
- Always wrap in the device frame — see `## App prototype rules` in SKILL.md

**Key design elements**:
- Status bar + bottom inset are owned by the device frame; **design only the content region** between them
- One primary action per screen; the primary CTA is bottom-anchored or sits in the nav-bar
- Real images, never placeholder grays (per Rule 2 of `## App prototype rules`)
- Tap targets ≥ 44×44 pt (iOS) / 48×48 dp (Android)
- Click-test at least one interaction with Playwright before delivery (Rule 3)

**Recommended philosophies**: §05 Apple-system glass · §09 Soft-tactile / paper-like · §16 Web3 Minimalism (for crypto-app screens)

**Scene prompt template**:
```
[insert philosophy DNA here]
- Mobile app screen, [iPhone 15 Pro 393x852 / Pixel 8 412x915]
- Wrap in <IosFrame> or <AndroidFrame>; do not redraw status bar / home indicator inside
- Design only the content region (top: status-bar-height, bottom: home-indicator-inset)
- One primary action per screen, bottom-anchored or in the nav-bar
- Real images only; no placeholder grays
- Tap targets ≥ 44 pt (iOS) / 48 dp (Android)
```

---

## Game / web3 domain pack — carried over verbatim

The four templates below were authored by the same maintainer in the
predecessor fork's Phase 4 (`references/scene-templates.md §9–12` in
that repo). They are fork-author IP and carry over to this clean-room
rewrite verbatim. Section numbering shifts (predecessor §9–12 → this
catalog §06–09); the only other modification is the **Recommended
philosophies** line in each entry — re-numbered to point at this
skill's `references/design-styles.md` catalog. All other prose is
unchanged.

### 06 — Game HUD overlay (in-fork, game / web3 studios)

**Specs**:
- Landscape: 1920×1080 or 2560×1440 (PC), 2436×1125 (mobile landscape)
- Portrait gacha-style mobile: 1170×2532
- HUD elements live on edges; center stays clear for gameplay

**Key design elements**:
- Edge-anchored UI (top-left = identity / mini-map; top-right = currency / status; bottom = action bar)
- Functional color: red=danger, gold=reward, blue=cooldown
- Diegetic ambient indicators when possible (in-world bars on the character) — non-diegetic for menu / inventory
- Read-time target: <200ms — no body copy in the HUD
- Distinct shapes per state (not just colors) for accessibility

**Recommended philosophies**: §15 Game HUD · §07 Data-dense ledger (game stats, cooldown numerics) · §10 High-contrast graphic poster (HUD bold geometric chrome)

**Scene prompt template**:
```
[insert style DNA here]
- Game HUD overlay, [landscape 1920×1080 / portrait 1170×2532]
- Edge-anchored: identity top-left, status top-right, action bar bottom
- Functional palette: red=damage, gold=reward, blue=cooldown
- Distinct shape per state (active / charging / locked)
- No body copy — readable in <200ms
- Center kept clear for gameplay
```

---

### 07 — NFT marketplace card / collection grid (in-fork, web3)

**Specs**:
- Card: 240×320 to 320×420 (image-first)
- Grid density toggle: 4-up / 6-up / 8-up
- Dark mode default

**Key design elements**:
- Image takes 70%+ of the card area
- Three data points max on the card: floor / last sale / rarity
- Hover state reveals: collection name, holder count, top traits
- Owner identity at the bottom: small avatar (jazzicon) + truncated address

**Recommended philosophies**: §17 NFT Marketplace · §16 Web3 Minimalism · §04 Editorial-spatial cinematic (collection landing pages)

**Scene prompt template**:
```
[insert style DNA here]
- NFT marketplace card / collection grid
- Card: image 70%+ · floor + last sale + rarity rank
- Dark mode (#0E0E10) default
- 4/6/8-up grid toggle
- Hover reveals: collection, holders, traits
- Wallet address as identity (truncated hex + jazzicon)
```

---

### 08 — Wallet / DEX interface (in-fork, web3)

**Specs**:
- Mobile: 390×844
- Desktop: 1280×800 (popup) or 1440×900 (full app)
- One primary action per screen

**Key design elements**:
- Type-first layout, heavy whitespace, single accent color
- Numbers as the visual focus — large display sizes with tabular-mono digits
- Wallet address: truncated `0x1234…abcd` with jazzicon
- Compact data tables for token lists
- No skeuomorphism: no card shadows, no gradient buttons, no glassmorphism

**Recommended philosophies**: §16 Web3 Minimalism · §02 Neo-grotesque utility · §07 Data-dense ledger (token-list rows, position tables)

**Scene prompt template**:
```
[insert style DNA here]
- Wallet / DEX interface, [mobile 390×844 / desktop popup 1280×800]
- Type-first, heavy whitespace, single accent
- Numbers in tabular-mono are the visual anchors
- Truncated wallet address + jazzicon as identity
- One primary action per screen
- Anti-skeuomorphism (no glow, no glass, no gradient)
```

---

### 09 — Onboarding game-loop (in-fork, mobile games · web3 dApps)

**Specs**:
- Mobile portrait: 390×844 or 412×915
- One step per screen, full-bleed visuals

**Key design elements**:
- One action per screen — single bottom-anchored primary button
- Progress dots / pills always visible at top
- Reward feedback at the end of each step (small animation, no body copy)
- Mascot or visual motif consistent across all steps
- Frictionless auth: social or wallet only — no email+password
- Return hooks: daily mission card / streak counter / collection summary

**Recommended philosophies**: §18 Onboarding-Game-Loop · §09 Soft-tactile / paper-like · §10 High-contrast graphic poster (mascot-led bold motif)

**Scene prompt template**:
```
[insert style DNA here]
- Onboarding game-loop, mobile portrait 390×844
- One action per screen, primary button bottom-anchored full-width
- Progress pills at top always visible
- End-of-step reward animation (small, ≤400ms)
- Consistent mascot / motif across all steps
- Frictionless auth (social / wallet, no email+password)
- Daily/streak hook on the home tab post-onboarding
```

---

## Combining scene with philosophy — fast-mapping table

For the most common scene + brief shapes, the fast pairings are:

| Scene | If brief is… | Pair with philosophy |
|---|---|---|
| 01 Deck cover | restrained brand-led talk | §01 Editorial-identity |
| 01 Deck cover | tech / launch keynote | §08 Atmospheric gradient (deliberate) |
| 01 Deck cover | manifesto / mission | §10 High-contrast graphic poster |
| 02 Mid-deck content | dev-tool / API talk | §02 Neo-grotesque utility |
| 02 Mid-deck content | data / metrics talk | §07 Data-dense ledger |
| 03 Web hero | brand microsite | §04 Editorial-spatial cinematic |
| 03 Web hero | type-led brand reveal | §13 Kinetic typographic poster |
| 04 Infographic | KPI / quarterly review | §07 Data-dense ledger |
| 04 Infographic | long-form essay support | §06 Print-translation editorial |
| 05 Mobile app screen | iOS-native consumer app | §05 Apple-system glass |
| 05 Mobile app screen | productivity / journaling | §09 Soft-tactile / paper-like |
| 05 Mobile app screen | wallet / DeFi mobile | §16 Web3 Minimalism |
| 06 Game HUD | mainline game UI | §15 Game HUD |
| 07 NFT marketplace | collection landing | §17 NFT Marketplace |
| 08 Wallet / DEX | trading interface | §16 Web3 Minimalism |
| 09 Onboarding | wallet first-launch | §18 Onboarding-Game-Loop |

Two-template combinations are smells, not features. If a brief
calls for an "infographic with game-HUD chrome" or an "NFT card on
a deck slide", split the artifact into two — the infographic, and
the deck slide that references it. Composition by reference is
clean; composition by fusion isn't.
