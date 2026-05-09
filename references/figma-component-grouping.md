# Figma Component Grouping · Detect Repeating Patterns and Promote to Components

> A Figma file with 47 individually-drawn rounded buttons is unmaintainable. This guide finds the repetitions, proposes which to promote to a component, and lets the user commit them in batches.
>
> Read `figma-layer-naming.md` first. Component grouping without good names produces components named `Component / Frame 47 / Rectangle 31`, which is worse than no components.

---

## 0 · The problem this solves

Designers (especially planners doing wireframes, or designers new to Figma) often:
- Copy-paste a button 12 times instead of making it a component
- Build "almost the same card" 8 times with slight variations
- Inline icons as raw vectors instead of icon components

Result: when the brand color changes, the designer has to find and update each instance manually. Components exist exactly to prevent this.

The agent's job here is **detection + proposal + batched apply**, not unilateral componentization.

---

## 1 · What counts as a "repetition"

A node is a candidate for componentization when at least **3 instances** share:
- Same **type** (Frame / Group / Vector)
- Approximately same **size** (within ±10% on width and height)
- Same **structural signature** — i.e., the same set of child types in the same order
- Approximately same **fills** (same primary color, ignoring text content)

Three is the floor. Two-only patterns are too easy to false-positive on accidental similarity. Four+ is high-confidence.

---

## 2 · Detection algorithm (MCP path)

### Step 1 · Crawl the page

```
tool: figma_get_node
args: { nodeId: <page>, depth: -1 }
```

Build a flat list of all FRAME and GROUP nodes (skip atomic shapes — they rarely become components individually).

### Step 2 · Compute signatures

For each node, compute a **signature** that captures structure but ignores trivial differences:

```
signature = {
  type,
  width: round(width / 10) * 10,
  height: round(height / 10) * 10,
  child_types: [type for child in children],   // ordered
  primary_fill: hex(first solid fill, normalized to nearest brand token if close),
  has_text_child: bool,
}
signature_hash = sha1(JSON.stringify(signature))
```

Group nodes by `signature_hash`. Any group with **3 or more** members is a candidate cluster.

### Step 3 · Score candidates

For each candidate cluster, compute a "componentization value" score:

| Factor | Weight | Why |
|---|---|---|
| Cluster size (# of instances) | high | More instances = more leverage |
| Visual prominence (avg width × height of instances) | medium | A 200×40 button is more important than a 12×12 dot |
| Naming consistency (how many already share a name root) | medium | If 5 are named `card-something`, the user already thought "this is a thing" |
| Has text content | low | Text components carry more semantic value |
| Used across multiple pages | high | Multi-page reuse strongly suggests component |
| Already a Figma instance | **disqualifier** | Already componentized; skip |

Sort candidates by score. Top 10 go into the proposal.

### Step 4 · Propose to user

```markdown
## Component candidates · 8 patterns found

For each pattern: I'll show one example, the count, and a proposed component name.

### 1. NFT card · 14 instances
[ thumbnail of one example ]
- Pages: home, gallery, my-collection
- Proposed name: `Component / Card / NFT-tile`
- Variants suggested: `state=default | hover` (only 2 of 14 are in hover state)

### 2. Connect-wallet button · 9 instances
[ thumbnail ]
- Pages: home, deposit, settings
- Proposed name: `Component / Button / Connect-wallet`
- Variants suggested: none — all 9 are visually identical

### 3. Stat-row · 7 instances
[ thumbnail ]
- Pages: home, my-collection
- Proposed name: `Component / Row / Stat`
- Variants suggested: `value=high | low` (4 high, 3 low — different color)

…

Confirm:
  - "1, 2, 5" → componentize those, leave the rest
  - "all" → componentize all 8
  - "rename 1: Component / Card / NFT" → rename then proceed with whichever
  - "no" → don't componentize anything
```

Same confirmation gate as `figma-layer-naming.md`. Don't apply silently.

### Step 5 · Apply

For each accepted candidate:
1. Pick the **best** instance as the master (largest, most-recently-modified, highest naming consistency — pick one heuristic and stick to it).
2. Convert that instance to a component:
   ```
   tool: figma_create_component
   args: { nodeId: <best instance>, name: <proposed name> }
   returns: { componentId }
   ```
3. Replace each other instance with an instance of the new component:
   ```
   tool: figma_replace_with_instance
   args: { nodeId: <other instance>, componentId, preservePosition: true }
   ```
4. If the cluster had visual variants (different colors / states), create a component set with variants:
   ```
   tool: figma_combine_as_variants
   args: { componentIds: [...], variantProperties: [{name: "state", values: [...]}] }
   ```

After each step, re-read the affected nodes via `figma_get_node` to confirm the operation landed.

### Step 6 · Sanity check

After applying:
- Walk the page once more and re-compute signatures.
- The clusters that just became components should now show `INSTANCE` types (not `FRAME`).
- New clusters may appear (sub-patterns within the components). Don't re-propose immediately — that's the user's next session, not this one.

### Step 7 · Report

Save `assets/figma-reports/<date>-component-grouping.md`:
- Scope crawled
- Number of candidates found
- Per-candidate: name, instance count, accepted/rejected/modified, master id, variant structure if any

---

## 3 · Workflow without Figma MCP

Without write access, the agent does **detection + proposal**, the user does the apply manually in Figma.

### Step 1 · Get the layer tree

Same as `figma-layer-naming.md` §3 Step 1: ask for screenshots of the layer panel + canvas, or a plugin-exported JSON.

### Step 2 · Run detection on whatever's available

Detection on screenshots is noisier — without exact node ids and child-type lists, you're matching on visible appearance. Be conservative — propose only the highest-confidence patterns (clusters of 5+, with consistent fills).

### Step 3 · Output as Figma actions checklist

```markdown
In Figma, do these in order:

### Make the NFT card a component
1. Click on the card on `home` page (the leftmost one in the row)
2. Right-click → Create component (or Cmd+Alt+K)
3. Rename the component to `Component / Card / NFT-tile`

### Replace the other 13 to instances of that component
4. Open Assets panel (left sidebar, second tab)
5. For each remaining card on `gallery` and `my-collection`:
   a. Select the card
   b. Right-click → Replace with… → search "NFT-tile" → pick the component
   c. (or drag the component from Assets panel onto the card)

### (optional) Add hover variant
6. Find the 2 hover-state cards on `home` page
7. Select one, right-click on the master component → Add variant
8. In the new variant, paste the hover-state card's content
9. Set property `state=hover`

Verify: Assets panel should show `Component / Card / NFT-tile` with `14 instances` and `2 variants`.
```

Confirmation gate stays. The user can reject specific steps before doing them.

---

## 4 · Edge cases

### 4.1 · "Almost the same" instances

When a cluster has 8 instances and 1 is *clearly* different (different layout, not just color), that 1 is **not** a variant — it's a different component. Exclude it from the cluster, propose only the 7.

### 4.2 · Cross-file components

If `team-brand-spec.json` lists `design_system.figma_library_url`, components should ideally be promoted **into the library**, not just into the local file. This requires:
- The user has edit access on the library file
- A separate workflow (out of scope here — note in the report)

For now, create the component in the current file and tag it in the report:
> "Recommend promoting this component to the team library at `<url>` — see `figma-brand-spec-import.md` for the import direction."

### 4.3 · Components inside auto-layout

If the cluster items are inside an auto-layout parent, replacing with instances may shift the parent's sizing. Verify the parent post-replacement and report any size changes.

### 4.4 · The user wants more granular candidates

The user might say "I see only the ones with 8+ instances; what about the 3-4 instance patterns?" In that case, lower the threshold and re-propose:

```
Re-running detection with threshold 3+ instances. 22 additional candidates found, scored low. Showing the top 10:
…
```

---

## 5 · Quality bar

- **Don't suggest components for things that aren't repeated**. A unique hero illustration is not a component candidate.
- **Don't suggest variants when the differences are content, not state**. 14 cards showing 14 different NFTs are not 14 variants — they're 14 instances of one component with different image fills.
- **Confirmation rate target**: aim for >70% of proposals accepted on the first pass. Lower means the proposals are off — recalibrate.

---

## 6 · Self-check before delivery

- [ ] Detection ran with proper signature (size + child structure + fill), not just visual similarity?
- [ ] Each candidate has at least 3 instances?
- [ ] Each candidate was scored and ranked before showing top 10?
- [ ] User confirmed before any `figma_create_component` was called?
- [ ] After apply, did I re-crawl and verify the cluster is now `INSTANCE`-typed?
- [ ] Report written to `assets/figma-reports/<date>-component-grouping.md`?

---

**Owner**: Internal design platform team
**Last reviewed**: 2026-05-08
**Related**: `figma-workflow.md` · `figma-layer-naming.md` (prerequisite) · `figma-brand-spec-import.md` (when components should live in the team library)
