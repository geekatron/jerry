---
feature_id: FEAT-040-008
agent: ux-atomic-architect
status: under_review
criticality: C3
engagement_id: UX-0008
topic: Jerry Framework Documentation Component Taxonomy
product: Jerry Framework (AI workflow guardrails)
wave: 1-Phase-1a
degraded_mode: true
quality_score: 0.922
iteration: 4
revision_log:
  iter-2:
    date: 2026-04-17
    changes:
      - "P0-1: Reconciled style drift ratio contradiction — fixed Executive Summary to show 0.24 overall / 0.47 voice-tone; added denominator derivation table in Style Token Audit with 15-doc corpus breakdown"
      - "P0-2: Decomposed all 5 organisms into constituent molecules — added M-09 Goal Statement Block, M-10 Verification Block, M-11 Next Steps Block, M-12 Troubleshooting Table, M-13 Scope Callout; applied sub-element decomposition to O-01 through O-05"
      - "P0-3: Added concrete enforcement mechanism for INSTALLATION.md anti-pattern — HTML comment text ready to paste, Vale rule sketch, and P1 wave-action in FEAT-040-015 reference"
      - "P0-4: Added Taxonomy Discovery Pathway section with PLAN.md link, template header comment format, Wave 3/4 required-reading entry, and stub directory action"
      - "P1: Corrected TP-03 organism mapping from O-03 to O-04; reclassified TP-04 as DQ-01 selector guide; added Goal Statement section to TP-01; added PASS-doc scope qualifier; expanded A-08 with concrete Jerry fields; documented quality score basis"
      - "Other: Fixed Synthesis Judgments — added 8 additional classification rationale entries; added CC-002 quality score basis statement"
  iter-3:
    date: 2026-04-20
    changes:
      - "DA-001-2 (BLOCKER): Promoted M-10 (Verification Block) from Molecule to O-06 (Verification Organism) — M-10 contained M-03 (a molecule), violating boundary adjudication rule. M-10 tombstoned in Molecules Catalog. O-06 added to Organisms Catalog with full sub-element decomposition. All references updated: O-01 sub-element table, Composition Rules, structural template, internal ordering note."
      - "CC-001-2 (BLOCKER): Corrected voice/tone denominator from 15 to 13 (table had 13 in-scope rows; 2 out-of-scope rows excluded). Recalculated 7/13 = 0.54 (was 7/15 = 0.47). Updated Executive Summary, Token Category table, overall drift ratio (0.25, was 0.24). Derivation section rewritten with explicit CC-001-2 resolution note."
      - "FM-001-2 (P2): Added A-13 (Prose Action Sentence) to Atoms Catalog. Fixed O-01 and O-02 sub-element tables to reference A-13 instead of inline 'Atom: imperative sentence'. Atoms count 12→13."
      - "DA-002-2 (P2): Added 5 Synthesis Judgments entries for M-09, M-11, M-12, M-13, and O-06 promotion. All iter-2 molecules now have documented classification rationale."
      - "IN-001-2 (P3): Not addressed in iter-3 — path hardcoding is a Minor finding. Stable alias path (docs/reference/documentation-taxonomy.md) deferred to Wave 3 gate action. No regression introduced."
  iter-4:
    date: 2026-04-20
    changes:
      - "DA-002-3 (P1): Resequenced A-12 before A-13 in Atoms Catalog body. A-13 section moved to follow A-12 — numeric ordering now correct. No content changes."
      - "DA-001-3 (P1): Added type-vs-instance classification principle to Boundary Adjudication section: 'Classification applies at the type level — an organism is classified by its type definition, not by whether a specific instance includes all optional sub-elements.'"
      - "PM-001-3 (P2): Added Wave 4 action item to A-13 catalog entry designating docs/runbooks/getting-started.md Steps 1-3 as provisional canonical exemplar. Notes that Atoms coverage FAIL (77%) closes to 85% PASS once designation is ratified."
---

[DEGRADED MODE] This output was produced without Storybook MCP access.
Input was provided via manual component inventory mode. Some features are reduced:
- Cannot browse or validate live component stories
- Cannot inspect component variants, states, or props interactively
- Cannot verify design token usage in component implementations
- Coverage assessment accuracy depends on user-provided inventory completeness

---

# Atomic Design Component Taxonomy: Jerry Framework Documentation

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | L0: taxonomy overview, top Wave 3/4 recommendations |
| [Engagement Context](#engagement-context) | Scope, methodology adaptation, source artifacts |
| [Methodology: Atomic Design for Docs](#methodology-atomic-design-for-docs) | How Brad Frost's 5-level hierarchy maps to markdown components |
| [Atoms Catalog](#atoms-catalog) | Smallest reusable documentation units with canonical examples |
| [Molecules Catalog](#molecules-catalog) | Composed atom groups with single documentation purpose |
| [Organisms Catalog](#organisms-catalog) | Full Diataxis-quadrant section structures with sub-element decomposition |
| [Templates Catalog](#templates-catalog) | Ready-to-use skeletons for Wave 3/4 writers |
| [Selector Guides](#selector-guides) | Routing and quadrant-selection aids (distinct from Frost-style templates) |
| [Existing Pages Audit](#existing-pages-audit) | Which docs exemplify which templates |
| [Gaps Analysis](#gaps-analysis) | Patterns Jerry needs but does not have |
| [Composition Rules](#composition-rules) | Valid, forbidden, and optional assembly patterns |
| [Style Token Audit](#style-token-audit) | Documentation convention consistency (analog to design tokens) |
| [Taxonomy Discovery Pathway](#taxonomy-discovery-pathway) | How Wave 3/4 writers will find and use this taxonomy |
| [INSTALLATION.md Enforcement](#installationmd-enforcement) | Concrete mechanism to prevent anti-pattern propagation |
| [Synthesis Judgments Summary](#synthesis-judgments-summary) | AI judgment calls with confidence classification |

---

## Executive Summary

### Component Counts

| Level | Count | Notes |
|-------|-------|-------|
| Atoms | 13 | Callout types, code blocks, link styles, navigation table, severity/criticality/status tags, prose action sentence (A-13, new iter-3) |
| Molecules | 12 | Prerequisites block, when-to-use pair, command+output pair, Diataxis quadrant frontmatter, playbook header, criterion table, agent table, triple-lens table; + 4 new in iter-2: goal statement, next steps, troubleshooting table, scope callout. Verification Block promoted to O-06 in iter-3 (boundary rule). |
| Organisms | 6 | Tutorial skeleton, how-to skeleton, reference entry, explanation skeleton, skill landing page; + O-06 Verification Organism (promoted from M-10 in iter-3) |
| Templates | 3 | Per-skill how-to template (TP-01), agent reference entry template (TP-02), ADR template (TP-03) |
| Selector Guides | 1 | DQ-01 Diataxis Quadrant Selector (routing aid, not a Frost-style template) |
| Pages | 6 | Exemplar instantiations identified in existing corpus |

**Note on template count change from iter-1:** TP-04 has been reclassified as selector guide DQ-01. It is not a Frost-style template (no placeholder content to instantiate). The 3 remaining templates (TP-01 through TP-03) are genuine fill-in-the-blank skeletons. See [Selector Guides](#selector-guides).

### Documentation Style Consistency Score

Overall style drift ratio: **0.25** (voice/tone category: **0.54**) — both above the 0.20 heuristic threshold. Derivation:

- Overall 0.25 = arithmetic mean across 7 token categories (see [Style Token Audit](#style-token-audit)); updated in iter-3 after denominator correction
- Voice/tone 0.54 = 7 of 13 in-scope documents have identifiable voice drift (denominator corrected in iter-3 from 15 to 13 — see denominator derivation table in Style Token Audit)
- The 0.20 threshold is a framework-internal heuristic: drift above 0.20 means more than 1-in-5 style instances bypass the convention system, the practical boundary between incidental overrides and systematic drift requiring governance intervention. Source: ux-atomic-architect methodology, aligned with W3C Design Token Community Group draft categories.

### Exemplar Coverage

| Level | Total | Has Canonical Exemplar | Coverage % | Target |
|-------|-------|------------------------|------------|--------|
| Atoms | 13 | 10 | 77% | >= 80% — FAIL (A-13 new, no exemplar yet) |
| Molecules | 12 | 8 | 67% | >= 60% — PASS |
| Organisms | 6 | 4 | 67% | >= 60% — PASS |
| Templates | 3 | 2 | 67% | >= 60% — PASS |

**Quality score basis (CC-002 resolution):** In iter-1, template exemplar coverage was 50% (2 of 4 templates) against a 60% target — a self-identified FAIL. With TP-04 reclassified as DQ-01 (selector guide, not a template), the correct denominator is 3 templates. TP-01 (per-skill how-to) has `docs/playbooks/problem-solving.md` as a partial exemplar; TP-03 (ADR) has `docs/design/ADR-001.md` as a full exemplar; TP-02 (agent reference) has no exemplar. Coverage = 2/3 = 67% — PASS at the >= 60% target. The iter-1 self-score of 0.924 was unjustified given the internal consistency failures (0.47/0.24 contradiction, organism sub-element gaps). Iter-2 self-score is 0.87, reflecting resolved P0 blockers against remaining P1 gaps.

### Top 5 Recommendations for Wave 3/4

1. **Adopt the Reference Entry Template immediately.** `docs/reference/claude-code-permissions.md` and `docs/reference/ci-cd-pipeline-security.md` are full working exemplars for **Diataxis structural patterns** (R-01 through R-07). Writers can copy their section hierarchy, reference table format, and code example placement. Do NOT copy specific prose phrasings or link formats without checking against the Atoms Catalog for canonical form.
2. **Create the Per-Skill Doc Template before writing any skill docs.** The 30-skill gap means 120+ documents (4 quadrants each) are needed. TP-01 in this taxonomy provides the how-to skeleton. Start any skill doc by reading the [Taxonomy Discovery Pathway](#taxonomy-discovery-pathway) section and filling in the Goal Statement section of TP-01 first.
3. **Standardize the Prerequisites Molecule.** It appears in `docs/runbooks/getting-started.md` (compliant checklist form) and `docs/playbooks/problem-solving.md` (bullet list form) with different visual conventions. Canonical form: fenced blockquote with `> **Start state:**` line plus `- [ ]` checklist items.
4. **Do not use `docs/INSTALLATION.md` as a writing model.** It introduces the marketing-voice anti-pattern. An enforcement comment has been drafted — see [INSTALLATION.md Enforcement](#installationmd-enforcement). New writers should copy from `docs/reference/claude-code-permissions.md` for structure.
5. **The Explanation Skeleton organism does not have a full Jerry exemplar yet.** `docs/explanation/ci-cd-supply-chain-security.md` is the closest match (passes all E-01 through E-07) and should be designated the canonical reference.

### Design System Maturity: Nascent

Component coverage 67% at template level (passing threshold), but style drift ratio 0.25 (above 0.20 threshold) and page coverage at 5% (6 exemplar pages against 120+ needed — well below the 30% Nascent/Developing boundary). The taxonomy constructed here is the governance intervention that moves the system toward Developing.

---

## Engagement Context

**Product:** Jerry Framework v0.31.5 — AI workflow guardrails and multi-skill orchestration for Claude Code.

**Target users:** Framework users (developers using Jerry skills), and Jerry contributors (Wave 3/4 writers creating skill documentation).

**Component scope:** All user-facing markdown documentation and SKILL.md patterns across 30 skills. Focus on reusable structural patterns, not specific prose.

**Design system references:**
- Diataxis standards: `skills/diataxis/rules/diataxis-standards.md`
- Navigation standards: `.context/rules/markdown-navigation-standards.md` (H-23, H-24)
- Skill structure standards: `.context/rules/skill-standards.md` (H-25, H-26)
- Exemplar documents: `docs/reference/claude-code-permissions.md`, `docs/reference/ci-cd-pipeline-security.md`, `docs/explanation/ci-cd-supply-chain-security.md`, `docs/explanation/permission-security-model.md`

**Upstream inputs:** `projects/PROJ-040-documentation/reports/diataxis-audit-20260420.md` — C4-scored audit identifying 15 documents with classification and purity verdicts. Four documents confirmed PASS (the four new docs added since PROJ-015 baseline).

**MCP status:** Manual Component Inventory Mode. Component inspection performed via filesystem reads of existing docs. No live Storybook equivalent.

**Wave entry criteria:** Wave 1 Phase 1a — parallel to JTBD analysis. Documentation wave entry is independent; the audit report provides the documentary basis.

---

## Methodology: Atomic Design for Docs

Brad Frost's Atomic Design was developed for UI component systems. This taxonomy adapts it to markdown documentation structures. The hierarchy principle is identical: small reusable units compose into larger functional structures. The analogy holds because documentation has the same compositional problem as UI — ad-hoc creation leads to inconsistency, duplicate patterns, and undocumented conventions that break when new writers join.

### Hierarchy Mapping

| Frost Level | UI Meaning | Docs Equivalent | Classification Criterion |
|-------------|------------|-----------------|--------------------------|
| Atom | Single HTML element with one function | Single markdown pattern with one formatting purpose | Cannot be decomposed; maps to one markdown syntax element or a tightly-coupled text convention |
| Molecule | 2-5 atoms with single describable purpose | 2-5 atoms that form one named documentation block | Removing any atom degrades the block's function; block serves a single reader purpose |
| Organism | Complex interface section with layout logic | Complete section structure for one Diataxis criterion | Reusable across templates; has internal ordering logic; recognizable as a named section type; ALL sub-elements must be named as molecules or atoms |
| Template | Page-level layout using placeholder content | Diataxis-quadrant page structure with placeholder sections | Arranges organisms into complete page; multiple skill docs can instantiate it; genuine fill-in-the-blank skeleton |
| Selector Guide | N/A (Frost extension for docs) | Routing or decision aid for writers | Consulted as a decision aid, not copied as a skeleton; cannot be "instantiated" in the Frost sense |
| Page | Template instance with real content | An existing doc that instantiates a template | Identified by which template it matches |

**Template vs. Selector Guide distinction:** Three templates (TP-01 through TP-03) are genuine Frost-style placeholders — writers copy and fill in. DQ-01 (Diataxis Quadrant Selector) is a routing decision tree, not a fill-in-the-blank skeleton. Keeping it in the Template level misrepresents it to writers. This distinction is a deliberate extension of Frost for documentation contexts.

### Boundary Adjudication for Docs

The molecule/organism boundary is the hardest call. Rule applied: if a block contains other molecules as sub-blocks (e.g., a Prerequisites block that itself contains a Command+Output molecule), classify as organism. If the block is a flat group of atoms serving a single purpose in one step, classify as molecule.

**Organism completeness requirement:** Every element listed in an organism's composition MUST be either a named molecule or a named atom. Prose sections described only by their section heading (e.g., "Verification section," "What You Will Achieve section") without formal classification are an incomplete adaptation of Frost's hierarchy. This requirement drove the addition of M-09 through M-13 in iter-2.

**Type-vs-instance classification principle:** Classification applies at the type level — an organism is classified by its type definition, not by whether a specific instance includes all optional sub-elements.

---

## Atoms Catalog

Atoms are the smallest formatting and structural units that cannot be decomposed further without losing their documentation function.

### A-01: Admonition Callout

**Function:** Draws reader attention to information that falls outside the main flow — warnings, notes, tips.

**Variants:** Note (informational), Warning (risk of error), Tip (optional improvement), Important (must-read side effect).

**Canonical form:**
```markdown
> **Note:** {text}

> **Warning:** {text — risk of breakage}

> **Tip:** {text — optional improvement}

> **Important:** {text — must-read side effect}
```

**Jerry usage:** Blockquote with bold label. Confirmed in `docs/runbooks/getting-started.md` line 18 (`> **Start state:**`) and `docs/explanation/ci-cd-supply-chain-security.md` line 4 (`> **Scope:**`).

**Drift instances:** `docs/INSTALLATION.md` uses a bare blockquote for the marketing opening ("Let's get you set up and shredding") — a callout-shaped element used for non-informational content. Admonition atom violated. See [INSTALLATION.md Enforcement](#installationmd-enforcement).

---

### A-02: Code Block

**Function:** Displays commands, expected output, file contents, or configuration values in a fixed-width, copyable format.

**Variants:** bash (commands), python (code), yaml (config/frontmatter), json (settings/schema), markdown (doc structure), text (expected output, log output).

**Canonical form:**

~~~markdown
```bash
{command}
```

```yaml
{config}
```

```json
{schema}
```
~~~

**Jerry usage:** Confirmed across `docs/runbooks/getting-started.md` (bash + PowerShell blocks), `docs/reference/claude-code-permissions.md` (json example at line 50), `docs/reference/ci-cd-pipeline-security.md` (command steps).

**Drift instances:** `docs/INSTALLATION.md` uses unlabeled fenced blocks in some sections — language tag missing, preventing syntax highlighting.

---

### A-03: Internal Link

**Function:** Cross-references a section within the same document (anchor link) or a file within the repository (relative path).

**Variants:** Anchor link (`[text](#anchor)`), repo-relative link (`[text](path/to/file.md)`), external URL (`[text](https://...)`).

**Canonical form:**
```markdown
[Section Name](#section-name)
[path/to/file.md](path/to/file.md)
[External Source](https://example.com)
```

**Jerry usage:** H-23/H-24 mandate anchor links in navigation tables. `docs/reference/claude-code-permissions.md` uses all three variants. External links use `> Source:` blockquote form (`> Source: [Claude Code Settings](https://...)`).

---

### A-04: Navigation Table

**Function:** Provides a document-level table of contents with section names and purposes. Required for all Claude-consumed markdown over 30 lines (H-23).

**Variants:** Section Index format (standard, 2 columns), Triple-Lens format (3-audience variant for SKILL.md).

**Canonical form:**
```markdown
## Document Sections

| Section | Purpose |
|---------|---------|
| [Section Name](#section-name) | One-line description |
```

**Classification rationale (Atom, not Molecule):** The Navigation Table maps to a single markdown syntax element (a table) with one formatting purpose (document index). While its rows contain links (A-03), the table as a unit cannot be further decomposed without losing its index function. Compare: an HTML `<table>` element is an atom in Frost's UI hierarchy. The same applies here. If the Navigation Table were a Molecule, one would need to identify 2-5 distinct atoms whose removal degrades the function — but removing any single row does not degrade the table's index function; only removing the table element itself does. Classification: Atom.

**Jerry usage:** Present in all four PASS-verdict documents. `docs/reference/claude-code-permissions.md` lines 8-21 is the canonical exemplar.

**Drift instances:** `docs/CLAUDE-MD-GUIDE.md` and `docs/BOOTSTRAP.md` do not have a navigation table despite exceeding 30 lines — H-23 violation.

---

### A-05: Severity Tag

**Function:** Classifies a finding's impact in audit or review contexts.

**Variants:** Critical, Major, Minor.

**Canonical form:**
```markdown
| Major | {finding} |
| Minor | {finding} |
```

Used inline in tables (not as standalone callouts). Sourced from `skills/diataxis/rules/diataxis-standards.md` Section 2 anti-pattern tables and the diataxis audit report.

---

### A-06: Criticality Tag

**Function:** Classifies work item severity to determine required quality gates and governance procedures.

**Variants:** C1 (Routine), C2 (Standard), C3 (Significant), C4 (Critical).

**Canonical form:** Inline in frontmatter or table cells: `C1`, `C2`, `C3`, `C4`. In prose: `C3 (Significant)`.

**Jerry usage:** Present in all agent output frontmatter, quality-enforcement.md tables, and worktracker entities.

---

### A-07: Status Blockquote

**Function:** Communicates the processing or approval state of a document or work item in a scannable header position.

**Classification rationale (Atom, not Molecule):** A Status Blockquote maps to a single markdown blockquote element with a bold label and a status value. It does not combine multiple distinct atoms — it is a tightly-coupled text convention (bold label + value) with one formatting purpose. Candidate for Molecule would require identifying 2-5 atoms whose removal degrades function; a Status Blockquote without the label is just a blockquote (A-01), and without the value it conveys no state. The label+value pairing is the atom — analogous to a labeled input field in UI Atomic Design. Classification: Atom.

**Canonical form:**
```markdown
> **Status:** {ACCEPTED | DRAFT | NEEDS REVISION | PASS | REJECTED}
```

**Jerry usage:** ADR documents use `> **Status:** ACCEPTED`. Audit report uses PASS / NEEDS REVISION in inventory tables.

---

### A-08: YAML Frontmatter Block

**Function:** Machine-readable metadata at the start of a document, consumed by agents for routing, filtering, and validation.

**Variants:**

**(a) Agent output frontmatter** — required fields for agent-produced artifacts:
```yaml
---
feature_id: FEAT-040-008
agent: ux-atomic-architect
status: complete
criticality: C3
engagement_id: UX-0008
---
```

**(b) Diataxis quadrant frontmatter** — marks a document's quadrant and signals applicable criteria:
```yaml
---
quadrant: how-to
skill: problem-solving
---
```

**(c) Governance YAML frontmatter** — for agent definition `.governance.yaml` files:
```yaml
---
version: 1.0.0
tool_tier: T2
identity:
  role: "{role-name}"
  cognitive_mode: systematic
---
```

**Jerry usage:** Variant (a) present in all agent output documents. Variant (b) appears as HTML comment form in the four PASS documents. Variant (c) in all `skills/*/agents/*.governance.yaml` files.

---

### A-09: Checkbox List Item

**Function:** Communicates a verification requirement the reader must confirm before proceeding, or a state that can be ticked off.

**Canonical form:**
```markdown
- [ ] {Requirement the reader verifies}
- [x] {Requirement already confirmed}
```

**Jerry usage:** `docs/runbooks/getting-started.md` lines 20-22 (Prerequisites checklist). Also used in WAVE-progression signoff artifacts.

---

### A-10: Rule ID Reference

**Function:** Cites a specific governance rule by its canonical identifier, making the prose traceable to the governing constraint.

**Variants:** H-series (HARD rules: `H-04`, `H-23`), P-series (principles: `P-003`, `P-022`), T/H/R/E-series (Diataxis criteria: `T-01`, `H-02`, `R-05`), anti-pattern IDs (`TAP-01`, `HAP-03`).

**Canonical form:** Inline in prose as code span: `H-04`. As hyperlink where target exists: `[H-04](path/to/rule.md#hard-rule-index)`.

**Jerry usage:** `docs/runbooks/getting-started.md` line 34 links H-04 with full URL. Rule ID references appear in all governance docs.

---

### A-11: Horizontal Rule Separator

**Function:** Visually separates major document sections, providing white-space rhythm in long documents.

**Canonical form:**
```markdown
---
```

**Jerry usage:** Present after every `##` section in all four PASS-verdict documents. Convention: one blank line before, one blank line after.

---

### A-12: Criterion Table Row

**Function:** Documents a single quality criterion with its test method and pass condition, used inside criterion evaluation tables.

**Canonical form:**
```markdown
| {ID} | {Criterion description} | {Test method} | {Pass condition} |
```

**Jerry usage:** `skills/diataxis/rules/diataxis-standards.md` Section 1 tables (T-01 through T-08, H-01 through H-07, R-01 through R-07, E-01 through E-07).

---

### A-13: Prose Action Sentence (new, iter-3)

**Function:** Provides the human-readable instruction that frames a procedural step before a command block. Canonical form: imperative verb + object phrase. Cannot be decomposed without losing instructional direction — removing the verb eliminates the action signal; removing the object eliminates the scope signal.

**Classification rationale (Atom, not Molecule):** Organisms O-01 and O-02 list "Atom: imperative sentence" inline in their sub-element decomposition tables, but no catalog entry existed, leaving the claim "all sub-elements are formally named" partially false (FM-001-2). A Prose Action Sentence is a native documentation primitive analogous to a label element in UI Atomic Design — indivisible, single-purpose, maps to one text-unit convention. It does not combine independent atoms; the verb+object structure is the atom itself.

**Canonical form:**
```markdown
{Imperative verb phrase — what this command does}:
```

Examples:
- "Install the Jerry CLI package:"
- "Verify the session is active:"
- "Export the project context variable:"

**Jerry usage:** Appears as the introductory sentence before every `M-03` (Command+Output Pair) in tutorial and how-to documents. Confirmed in `docs/runbooks/getting-started.md` step prose (e.g., "Create a project directory:").

**Drift instances:** Some playbook step prose omits the imperative opener and begins directly with a code block — no instruction framing for the reader.

**Wave 4 action item:** Designate `docs/runbooks/getting-started.md` Steps 1-3 as the provisional A-13 Prose Action Sentence canonical exemplar. This closes the Atoms coverage FAIL (current 10/13 = 77%) once the designation is ratified, bringing Atoms coverage to 11/13 = 85% and meeting the >= 80% target.

---

## Molecules Catalog

Molecules are composed groups of 2-5 atoms that serve a single, nameable documentation purpose. Molecules M-01 through M-08 were cataloged in iter-1. Molecules M-09 through M-13 were added in iter-2 to complete organism sub-element decomposition (P0-2). In iter-3, M-10 (Verification Block) was promoted to O-06 (Verification Organism) per the boundary adjudication rule — it contains M-03 (a molecule), which meets the organism promotion criterion. The active molecule catalog is M-01 through M-09 and M-11 through M-13 (12 molecules total; M-10 ID retired to O-06).

### M-01: Prerequisites Block

**Atoms:** Admonition callout (A-01) + Checkbox list items (A-09) + Optional code block (A-02) for version verification command.

**Purpose:** Tells the reader what must be true before beginning a tutorial or how-to guide. Removing the callout degrades the "start state" framing. Removing the checklist items degrades the actionability.

**Canonical form:**
```markdown
## Prerequisites

> **Start state:** {One sentence describing required prior state}

- [ ] **{Requirement label}** — confirm with `{verification command}`
- [ ] **{Requirement label}** — run `{check command}` and verify `{expected output}`

If these are not in place, complete {linked prior step} first, then return here.
```

**Canonical exemplar:** `docs/runbooks/getting-started.md` lines 16-25.

**Drift instance:** `docs/playbooks/problem-solving.md` lines 48-55 uses an undelineated bullet list without the `> **Start state:**` callout and without checkboxes. Same purpose, different visual convention — consolidation needed.

---

### M-02: When to Use / When Not to Use Pair

**Atoms:** Two subsections (`### Use this skill when:`, `### Do NOT use this skill when:`) each containing a bullet list. Optionally bounded by A-11 (horizontal rule).

**Purpose:** Provides at-a-glance routing guidance for a skill or guide. Single purpose: help the reader decide whether to proceed or go elsewhere.

**Canonical form:**
```markdown
## When to Use

### Use this skill when:

- You need to {goal}
- You are {scenario}

### Do NOT use this skill when:

- You need to {different goal} — use `/{other-skill}` instead
- The task is {out-of-scope scenario}
```

**Canonical exemplar:** `docs/playbooks/problem-solving.md` lines 22-44.

---

### M-03: Command + Expected Output Pair

**Atoms:** Prose imperative sentence (action verb) + Code block (A-02, bash variant) + Code block (A-02, text/output variant) + Optional validation callout (A-01).

**Purpose:** Pairs a shell command with the result the reader should see, enabling verification at each step.

**Canonical form:**
```markdown
{Imperative verb phrase — what this command does}:

```bash
{command}
```

Expected result: {plain-English description}

```text
{sample output}
```
```

**Canonical exemplar:** `docs/runbooks/getting-started.md` Step 1 create-directory block (lines 36-58).

**Drift instance:** `docs/INSTALLATION.md` uses commands without "Expected result" annotation.

---

### M-04: Diataxis Quadrant Frontmatter

**Atoms:** YAML frontmatter block (A-08, variant b) + Quality-criteria comment block.

**Purpose:** Marks the document's quadrant classification and signals to writer agents which criteria and anti-patterns to apply during self-review.

**Canonical form:**
```yaml
---
quadrant: {tutorial | how-to | reference | explanation}
diataxis_version: "2.0"
---
```
```markdown
<!-- Quality criteria: skills/diataxis/rules/diataxis-standards.md Section 1 ({T/H/R/E}-01 through {T/H/R/E}-07) -->
<!-- Anti-patterns to avoid: {relevant anti-pattern IDs} -->
<!-- Voice: {quadrant voice descriptor} -->
```

**Canonical exemplar:** `docs/reference/claude-code-permissions.md` lines 4-6 (HTML comment form). Note: both YAML frontmatter and HTML comment form are acceptable; the four PASS documents use HTML comment form.

---

### M-05: Playbook Header Block

**Atoms:** H1 title + Skill-reference blockquote (A-07 variant) + Navigation table (A-04).

**Purpose:** Opens a how-to playbook with its skill identity and section map. Used in all four existing playbooks.

**Canonical form:**
```markdown
# {Skill Name} Playbook

> **Skill:** {skill-name}
> **SKILL.md:** [{skill-name}/SKILL.md]({url})
> **Trigger keywords:** {keyword, keyword, keyword}

## Document Sections

| Section | Purpose |
|---------|---------|
| [Section](#section) | Description |
```

**Canonical exemplar:** `docs/playbooks/problem-solving.md` lines 1-19.

---

### M-06: Criterion Evaluation Table

**Atoms:** Table header row + one or more criterion table rows (A-12) with Result and Evidence columns.

**Purpose:** Provides a structured, auditable pass/fail verdict for each quality criterion in a review or audit context.

**Canonical form:**
```markdown
| Criterion | Result | Evidence | Notes |
|-----------|--------|----------|-------|
| {T/H/R/E-NN} {description} | PASS/FAIL | Line {N}: "{verbatim quote}" | {optional} |
```

**Canonical exemplar:** `projects/PROJ-040-documentation/reports/diataxis-audit-20260420.md` Document 3 criterion table.

---

### M-07: Agent Table

**Atoms:** Table with Agent, Role, Output Location columns. Optionally Model column.

**Purpose:** Lists available agents for a skill with their specialization and where their output persists.

**Canonical form:**
```markdown
| Agent | Role | Output Location |
|-------|------|-----------------|
| `{agent-name}` | {Role description} | `{path/}` |
```

**Canonical exemplar:** `skills/problem-solving/SKILL.md` lines 76-88.

---

### M-08: Triple-Lens Audience Table

**Atoms:** Navigation table (A-04 variant) with Level, Audience, and Sections columns.

**Purpose:** Directs different reader types to the sections most relevant to their role, enabling progressive disclosure.

**Canonical form:**
```markdown
## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (ELI5)** | New users, stakeholders | [Purpose](#purpose), [When to Use](#when-to-use) |
| **L1 (Engineer)** | Developers invoking agents | [Available Agents](#available-agents), [Invoking an Agent](#invoking-an-agent) |
| **L2 (Architect)** | Workflow designers | [Integration Points](#integration-points), [P-003 Compliance](#p-003-compliance) |
```

**Canonical exemplar:** `skills/problem-solving/SKILL.md` lines 31-40.

---

### M-09: Goal Statement Block (new, iter-2)

**Atoms:** H2 section heading + Prose goal sentence + Optional scope qualifier callout (A-01).

**Purpose:** States the specific user goal a how-to guide or tutorial addresses. Scopes the guide to ONE user goal before the writer begins. Required in TP-01 to prevent writers from creating over-broad guides for multi-agent skills.

**Canonical form:**
```markdown
## Goal

This guide shows how to {specific user action} with `/{skill-name}`.

> **Scope:** This guide covers {specific sub-task}. For {adjacent goal}, see {companion guide}.
```

**Canonical exemplar:** No current document fully instantiates this molecule. Gap: requires addition to TP-01 and as the opening of all new skill how-to guides. The `docs/playbooks/problem-solving.md` opening paragraph ("This playbook covers...") is the closest informal equivalent.

---

### M-10: Verification Block — RECLASSIFIED as O-06 (iter-3)

**Reclassification note (DA-001-2 resolution):** M-10 was cataloged in iter-2 as a Molecule. However, M-10's own definition listed M-03 (Command+Output Pair, a Molecule) as a primary structural sub-element. By the boundary adjudication rule in the Methodology section — "if a block contains other molecules as sub-blocks, classify as organism" — M-10 meets the organism criterion. The reclassification was a regression introduced when iter-2 added M-10 without re-checking the boundary rule against the new molecule's own sub-element composition.

**Action:** M-10 promoted to O-06 (Verification Organism). See [O-06: Verification Organism](#o-06-verification-organism) in the Organisms Catalog. The M-10 ID is retired; all composition references updated to O-06.

---

### M-11: Next Steps Block (new, iter-2)

**Atoms:** H2 section heading + Bullet list of internal links (A-03) with one-line descriptions of each linked destination.

**Purpose:** Routes the reader to the next logical action after completing a tutorial or how-to guide. Provides the transition from learning/doing to the next related task.

**Canonical form:**
```markdown
## Next Steps

- [{How-To Guide Title}]({path}) — {what the reader will accomplish next}
- [{Reference Doc Title}]({path}) — {what the reader can look up}
- [{Explanation Doc Title}]({path}) — {what the reader can understand in depth}
```

**Canonical exemplar:** `docs/runbooks/getting-started.md` "What's Next?" section (implicit form). Not formalized as a molecule in iter-1. This molecule definition establishes the canonical form.

---

### M-12: Troubleshooting Table (new, iter-2)

**Atoms:** H2 section heading + Table with Symptom, Likely Cause, Resolution columns + Optional code block (A-02) for resolution commands.

**Purpose:** Provides scannable failure-mode guidance. Readers in troubleshooting mode scan for their symptom, not for narrative explanations. The table format is the canonical form — mixed prose and table in the same section is a drift pattern.

**Canonical form:**
```markdown
## Troubleshooting

| Symptom | Likely cause | Resolution |
|---------|-------------|------------|
| {Error or failure description} | {Root cause} | {Fix — one sentence or command} |
| {Error or failure description} | {Root cause} | {Fix} |
```

**Canonical exemplar:** `docs/runbooks/getting-started.md` Troubleshooting section (table form).

**Drift instance:** `docs/playbooks/problem-solving.md` Troubleshooting section uses mixed prose and table format — inconsistent.

---

### M-13: Scope Callout (new, iter-2)

**Atoms:** Admonition callout (A-01) with bold "Scope:" label + Explicit statement of what IS and IS NOT covered.

**Purpose:** Establishes E-06 compliance (bounded scope) for Explanation quadrant documents. Required in O-04 (Explanation Skeleton). The two-part structure (covered / not covered) is what makes this a named molecule rather than a plain callout: a single-clause callout is A-01; a callout with deliberate IS/IS-NOT structure is M-13.

**Canonical form:**
```markdown
> **Scope:** This document explains {what IS covered}. It does not cover {what IS NOT covered — and where to find it instead}.
```

**Canonical exemplars:** `docs/explanation/ci-cd-supply-chain-security.md` line 4, `docs/explanation/permission-security-model.md` lines 3-4.

---

## Organisms Catalog

Organisms are complete section structures for one Diataxis quadrant criterion group. Each organism has internal ordering logic and is reusable across multiple templates. **All sub-elements are formally named molecules or atoms.** Unnamed prose sections from iter-1 were decomposed in iter-2; the boundary error introduced by M-10 was corrected in iter-3 (M-10 promoted to O-06). There are now 6 organisms: O-01 through O-05 (iter-1/iter-2) and O-06 (iter-3 promotion).

### O-01: Tutorial Skeleton

**Diataxis criteria:** T-01 through T-08.

**Molecule composition (complete):**
- Navigation table (A-04) — required by H-23
- Goal Statement Block (M-09) — states the concrete achievement (T-07)
- Prerequisites Block (M-01) — establishes start state (T-06)
- Numbered steps section — each step: Prose Action Sentence (A-13) + Command+Output Pair (M-03) for command steps
- Verification Organism (O-06) — confirms tutorial success end-to-end (T-02 end-state); promoted from M-10 in iter-3
- Next Steps Block (M-11) — routes reader to follow-on guides

**Sub-element decomposition:**

| Sub-element | Molecule/Atom | Notes |
|-------------|---------------|-------|
| What you will achieve | M-09 (Goal Statement Block) | Appears at top per T-07 (endpoint shown upfront) |
| Numbered step prose | A-13 (Prose Action Sentence) | Single-function text unit; cannot decompose further |
| Numbered step command | M-03 (Command+Output Pair) | Each step with a command uses M-03 |
| Verification section | O-06 (Verification Organism) | End-to-end completion check; organism because it contains M-03 |
| Next Steps section | M-11 (Next Steps Block) | Transition to how-to guides |

**Internal ordering (required):** M-09 (Goal Statement) must precede M-01 (Prerequisites). M-01 must precede first numbered step. T-04 (no branches in a tutorial) means steps must be linear — any branch creates a new tutorial, not a section. O-06 (Verification Organism) must follow the final step. M-11 (Next Steps) must follow O-06.

**Canonical exemplar:** `docs/runbooks/getting-started.md` — closest existing match. NEEDS REVISION (CLI vs. plugin branching in Step 3 violates T-04), but overall structure is correct. Before Wave 4 tutorial writing, the T-04 branching violation must be remediated.

**Structural template (abbreviated):**
```markdown
# {Skill Name}: {Concrete Achievement Title}

{One-sentence description of what completing this tutorial achieves}

## Document Sections
{A-04 — navigation table}

---

## Goal
{M-09 — Goal Statement Block — what the reader will have at the end}

---

## Prerequisites
{M-01 — Prerequisites Block}

---

## Procedure

### Step 1: {Action Verb + Object}

{Imperative sentence}.

{M-03 — Command + Expected Output Pair}

### Step 2: ...

---

{O-06 — Verification Organism}

---

{M-11 — Next Steps Block}
```

---

### O-02: How-To Guide Skeleton

**Diataxis criteria:** H-01 through H-07.

**Molecule composition (complete):**
- Navigation table (A-04) — required by H-23
- Goal Statement Block (M-09) — establishes user goal scope (H-01, H-07)
- Prerequisites Block (M-01, lightweight) — 2-3 items max for competent-practitioner audience
- Numbered steps section — each step: prose imperative sentence (Atom) + optional M-03 for commands
- Troubleshooting Table (M-12) — failure modes at the end

**Sub-element decomposition:**

| Sub-element | Molecule/Atom | Notes |
|-------------|---------------|-------|
| Goal statement | M-09 (Goal Statement Block) | H-01 compliance: goal named explicitly |
| Lightweight prerequisites | M-01 (Prerequisites Block, condensed variant) | H-06: assume competence; 2-3 items only |
| Step prose | A-13 (Prose Action Sentence) | H-04: no "Why" paragraphs between steps |
| Step command (when present) | M-03 (Command+Output Pair) | H-03: real-world variation in If/Then branches |
| Troubleshooting | M-12 (Troubleshooting Table) | Failure modes; at end of guide |

**Internal ordering:** H-01 (goal in title) + H-07 (user framing) established in M-09. H-06 (assume competence) means M-01 is lightweight. H-03 (real-world variations) means at least one `If {condition}, do {action}` conditional appears in step prose. H-04 (no teaching) means no "Why" paragraphs between steps.

**Canonical exemplar:** `docs/playbooks/problem-solving.md` — best existing match, though NEEDS REVISION (embedded reference tables, H-02 violations).

---

### O-03: Reference Entry

**Diataxis criteria:** R-01 through R-07.

**Molecule composition (complete):**
- Navigation table (A-04)
- Overview paragraph (Atom: authoritative description sentence — R-02, no hedging)
- Structured entry tables — one or more tables per subject area (R-01: mirrors described structure, R-05: standard formatting)
- Code examples (A-02) for each entry that has executable usage (R-06)
- Source citations (A-03 external variant, `> Source:` form) for externally-derived content
- Optional Criterion Evaluation Table (M-06) for standards-reference docs

**Sub-element decomposition:**

| Sub-element | Molecule/Atom | Notes |
|-------------|---------------|-------|
| Authoritative description | Atom: declarative sentence | R-02: no hedging language |
| Entry tables | Atom: markdown table (structural) | R-01: structure mirrors the described system |
| Code examples | A-02 (Code Block) | R-06: usage examples present |
| Source citations | A-03 (Internal Link, external variant) | Present for externally-sourced claims |

**Internal ordering:** R-01 (mirrors described structure) means section hierarchy matches the system documented. R-02 (wholly authoritative) means no hedging anywhere. R-03 (complete specification) means no undocumented fields.

**Canonical exemplar:** `docs/reference/claude-code-permissions.md` — PASS on all R-01 through R-07.

---

### O-04: Explanation Skeleton

**Diataxis criteria:** E-01 through E-07.

**Molecule composition (complete):**
- Navigation table (A-04)
- Scope Callout (M-13) — E-06 compliance, appears near top
- Context section (Atom: discursive paragraph group — E-01, E-02)
- Conceptual sections — one or more sections with prose (Atom: discursive paragraph group)
- Connections section (Atom: prose + internal links A-03 — E-02)
- Alternative Perspectives section (Atom: prose — E-04)
- Related table (Atom: markdown table linking to companion quadrant docs)

**Sub-element decomposition:**

| Sub-element | Molecule/Atom | Notes |
|-------------|---------------|-------|
| Scope callout | M-13 (Scope Callout) | E-06: bounded scope explicitly stated |
| Context section prose | Atom: discursive paragraph | E-01: no numbered steps; "because", "however" language |
| Connections section | Atom: prose + A-03 links | E-02: explicit connections to related concepts |
| Alternative Perspectives | Atom: prose section | E-04: acknowledges other valid approaches |
| Related table | Atom: markdown table | Links to companion docs in other quadrants |

**Internal ordering:** E-06 (bounded scope) requires M-13 near the top. E-01 (discursive) means no numbered steps anywhere in the organism. E-04 (acknowledges perspective) requires Alternative Perspectives section — omission is a forbidden composition.

**Canonical exemplar:** `docs/explanation/ci-cd-supply-chain-security.md` — PASS on all E-01 through E-07.

---

### O-05: Skill Landing Page Structure

**Diataxis criteria:** Multi-quadrant (legitimate). Not a pure-quadrant document — it is the entry point that routes readers to pure-quadrant docs.

**Molecule composition (complete):**
- Version header blockquote (A-07 variant)
- Triple-Lens audience table (M-08)
- Purpose section — Key Capabilities list (Atom: bullet list)
- When to Use / Not Use pair (M-02)
- Available Agents table (M-07)
- P-003 Compliance diagram (Atom: ASCII diagram or markdown blockquote)
- Invocation Options section (Atom: prose + A-02 code blocks)
- Integration Points section (Atom: prose or table)
- References section (Atom: markdown table)

**Sub-element decomposition:**

| Sub-element | Molecule/Atom | Notes |
|-------------|---------------|-------|
| Version header | A-07 (Status Blockquote, version variant) | Version + constitutional compliance |
| Audience routing | M-08 (Triple-Lens Table) | Progressive disclosure for 3 audience types |
| Key capabilities | Atom: bullet list | What the skill enables |
| Routing guidance | M-02 (When/Not-To-Use Pair) | Required per skill-standards.md |
| Agent listing | M-07 (Agent Table) | Required for multi-agent skills |
| P-003 compliance | Atom: ASCII diagram | Orchestrator-worker topology visualization |
| Invocation examples | Atom: prose + A-02 | Example invocation patterns |
| Integration points | Atom: prose or table | Cross-skill connections |
| References | Atom: markdown table | Source citations |

**Internal ordering:** Per `skills/skill-standards.md` SKILL.md Body Structure, sections follow the prescribed order (H-25).

**Canonical exemplar:** `skills/problem-solving/SKILL.md` — most complete existing SKILL.md.

---

### O-06: Verification Organism (promoted from M-10, iter-3)

**Diataxis criteria:** T-02 (steps produce visible results), T-01 (tutorial is completable end-to-end).

**Reclassification rationale (DA-001-2 resolution):** Originally cataloged as M-10 (Verification Block) in iter-2. Promoted to organism status in iter-3 because M-10 contained M-03 (Command+Output Pair, a Molecule) as a primary structural sub-element. By the boundary adjudication rule — "if a block contains other molecules as sub-blocks, classify as organism" — M-10 meets the organism criterion. The Verification Organism is also the most reusable section structure after O-01 (Tutorial Skeleton), warranting organism-level documentation.

**Molecule composition (complete):**
- Navigation context: appears as a named section within O-01 (Tutorial Skeleton), after the final step
- Admonition callout (A-01, "Tip" or "Note" variant) — frames the verification purpose
- One or more Command+Output Pairs (M-03) — end-state verification command with expected output OR checklist items (A-09) — checklist-based confirmation of end-state (alternative to M-03 when verification is observational, not command-driven)

**Sub-element decomposition:**

| Sub-element | Molecule/Atom | Notes |
|-------------|---------------|-------|
| Verification callout | A-01 (Admonition, Tip variant) | Frames purpose: "Run this check to confirm..." |
| Verification command | M-03 (Command+Output Pair) | End-state command + expected output |
| Verification checklist | A-09 (Checkbox List Item) | Alternative to M-03 for observational verification |

**Composition rule:** M-03 and A-09 are mutually exclusive alternatives per step — one per verification item. The organism can contain multiple verification steps but each item uses either M-03 or A-09, not both.

**Internal ordering:** Callout (A-01) always precedes command/checklist items. Multiple verification steps follow a logical dependency order (check system state before checking application state).

**Canonical form:**
```markdown
## Verification

> **Tip:** Run this check to confirm the tutorial completed successfully.

{Imperative verb phrase — what this verification command confirms}:

```bash
{end-state verification command}
```

Expected result: {what success looks like}

```text
{sample success output}
```
```

**Canonical exemplar:** `docs/runbooks/getting-started.md` has an implicit verification pattern (the `jerry session status` command at the end of Step 2). Not fully formalized. O-06 establishes the canonical form for Wave 4 tutorial writing.

---

## Templates Catalog

Templates arrange organisms into complete page structures that multiple skill documents can instantiate. All three templates use placeholder content (fill-in-the-blank skeletons). TP-04 from iter-1 has been reclassified as DQ-01 in the [Selector Guides](#selector-guides) section — it is a routing decision tree, not a fill-in-the-blank skeleton.

### TP-01: Per-Skill How-To Guide Template

**Organisms:** How-To Guide Skeleton (O-02).

**Purpose:** The template Wave 3/4 writers will fill in to create how-to documentation for each of the 30 skills. Highest-priority template gap — 30 skills need it and none exists.

**Ready-to-use skeleton:**

```markdown
---
quadrant: how-to
skill: {skill-name}
---
<!-- Quality criteria: skills/diataxis/rules/diataxis-standards.md Section 1 (H-01 through H-07) -->
<!-- Anti-patterns to avoid: HAP-01 (conflating with tutorial), HAP-02 (tool-focused), HAP-04 (completeness over focus) -->
<!-- Voice: Direct, action-oriented, efficient. See Section 5. -->
<!-- Atomic taxonomy reference: projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-008/ux-atomic-architect-output.md -->
<!-- Copy from: docs/reference/claude-code-permissions.md (structure), docs/runbooks/getting-started.md (step format) -->
<!-- Do NOT copy from: docs/INSTALLATION.md (marketing voice), docs/BOOTSTRAP.md (quadrant mixing) -->

# How to {User Goal with /{skill-name}}

## Document Sections

| Section | Purpose |
|---------|---------|
| [Goal](#goal) | What this guide achieves |
| [Prerequisites](#prerequisites) | What must be true before starting |
| [Steps](#steps) | The procedure |
| [Variations](#variations) | Common real-world variations |
| [Troubleshooting](#troubleshooting) | Failure modes and fixes |

---

## Goal

This guide shows how to {specific user action} with `/{skill-name}`.

> **Note:** This guide covers {specific sub-task}. For {adjacent goal}, see {companion guide}.

> **Before you start:** State the specific user goal this guide addresses. A user goal is a concrete task a practitioner performs with this skill. If this skill has multiple agents, each agent's primary task is a candidate goal. Limit this guide to ONE goal. Consult the SKILL.md `When to Use` section for candidate goals.

---

## Prerequisites

> **Assumed competence:** This guide assumes you know {baseline skill context}.

- `JERRY_PROJECT` is set — confirm with `echo $JERRY_PROJECT`
- A Jerry session is active — confirm with `jerry session status`
- {Skill-specific prerequisite}

---

## Steps

1. {First imperative action — what the user does first}

   ```bash
   {command if applicable}
   ```

2. {Second action}

3. {Third action — include If/Then branch for H-03 compliance}

   If {real-world variation}, {action instead}:

   ```bash
   {variant command}
   ```

---

## Variations

### {Variation Scenario Title}

If you need to {variation goal}, {action}.

---

## Troubleshooting

| Symptom | Likely cause | Resolution |
|---------|-------------|------------|
| {Error or failure description} | {Root cause} | {Fix} |
```

**Canonical exemplar referencing:** `docs/playbooks/problem-solving.md` is the closest existing instantiation (partial compliance — reference tables embedded, H-02 violations in places).

---

### TP-02: Agent Reference Entry Template

**Organisms:** Reference Entry (O-03) scoped to a single agent.

**Purpose:** Documents a specific agent's interface — inputs, outputs, tools, example invocations, and behavioral constraints. Wave 4 deliverable.

**Ready-to-use skeleton:**

```markdown
---
quadrant: reference
agent: {agent-name}
skill: {parent-skill}
---
<!-- Quality criteria: skills/diataxis/rules/diataxis-standards.md Section 1 (R-01 through R-07) -->
<!-- Anti-patterns: RAP-01 (marketing), RAP-02 (instructions), RAP-03 (narrative) -->
<!-- Voice: Neutral, precise, austere. -->
<!-- Atomic taxonomy reference: projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-008/ux-atomic-architect-output.md -->

# {Agent Name} Reference

> {One-sentence authoritative description of what this agent does. No marketing.}

## Document Sections

| Section | Purpose |
|---------|---------|
| [Identity](#identity) | Role, cognitive mode, tool tier |
| [Inputs](#inputs) | Required and optional input fields |
| [Outputs](#outputs) | Output location, format, structure |
| [Tools](#tools) | Tools this agent uses |
| [Behavioral Constraints](#behavioral-constraints) | What this agent will and will not do |
| [Example Invocations](#example-invocations) | Usage patterns |

---

## Identity

| Field | Value |
|-------|-------|
| Agent name | `{agent-name}` |
| Parent skill | `{skill-name}` |
| Cognitive mode | {divergent / convergent / integrative / systematic / forensic} |
| Tool tier | T{N} |
| Model | {sonnet / opus / haiku} |
| Output location | `{default/path/}` |

---

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `{field}` | string | Yes/No | {description} |

---

## Outputs

| Artifact | Location | Format | L0/L1/L2 |
|----------|----------|--------|----------|
| {artifact name} | `{path}` | markdown | {yes/no} |

---

## Tools

| Tool | Purpose |
|------|---------|
| `Read` | {specific use} |
| `Write` | {specific use} |

---

## Behavioral Constraints

| Constraint | Source |
|-----------|--------|
| {What the agent will not do} | {P-NNN / H-NN} |

---

## Example Invocations

```
{Natural language invocation example 1}
```

```
{Natural language invocation example 2 — named agent explicit}
```
```

**Canonical exemplar:** No current document fully instantiates this template. `AGENTS.md` (703 lines) is the closest — a reference catalog but not per-agent entries in this format. Wave 4 deliverable.

---

### TP-03: ADR Template

**Organisms:** Explanation Skeleton (O-04) adapted for architectural decision records.

**Organism mapping correction (iter-2):** In iter-1, TP-03 was mapped to O-03 (Reference Entry). This was wrong. The ADR format uses the Nygard format — Context (discursive rationale), Decision (rationale narrative), Options Considered (alternative perspectives), Consequences (discursive outcome). This structure is closest to O-04 (Explanation Skeleton): it is discursive, acknowledges alternative perspectives (Options Considered = E-04 analog), and has a bounded scope (one decision). Reference Entry structure (structured lookup tables, no hedging, no narrative) does not match Nygard ADR. Corrected mapping: O-04 adapted.

**Ready-to-use skeleton:**

```markdown
# ADR-{NNN}: {Decision Title}

> **Status:** {DRAFT | PROPOSED | ACCEPTED | SUPERSEDED | DEPRECATED}
> **Date:** {YYYY-MM-DD}
> **Agent:** {creating-agent}
> **Supersedes:** {ADR-NNN or N/A}
> **Superseded By:** {ADR-NNN or N/A}

---

## Context

{What is the issue that motivates this decision?}

### Constraints

| ID | Constraint | Source |
|----|------------|--------|
| C-001 | {Constraint} | {Rule or principle} |

---

## Decision

{What is the change that is being proposed or has been accepted?}

---

## Options Considered

### Option A: {Name}

{Description}

**Pros:** {list}
**Cons:** {list}

### Option B: {Name}

{Description}

---

## Consequences

### Positive

- {Benefit}

### Negative

- {Trade-off or cost}

### Risks

| ID | Risk | Mitigation |
|----|------|-----------|
| R-001 | {Risk description} | {Mitigation} |

---

## References

| Source | Content | Location |
|--------|---------|----------|
| {source} | {content} | {path or URL} |
```

**Canonical exemplar:** `docs/adrs/ADR-001-agent-architecture.md` — active use. Also all ADRs under `docs/design/`.

---

## Selector Guides

Selector guides are routing aids that help writers choose among options. They differ from Templates in that they are consulted as decision trees, not copied as skeletons. This level is a deliberate extension of Frost's 5-level hierarchy for documentation contexts.

### DQ-01: Diataxis Quadrant Selector

**Classification rationale:** TP-04 in iter-1. Reclassified in iter-2. The Frost hierarchy's defining characteristic of Templates is that they instantiate the same layout with different real content (multiple skill docs can instantiate the same template). DQ-01 cannot be "instantiated" — a writer cannot copy it and fill in placeholders. It is a routing decision tree. Keeping it as a Template would misrepresent it to Wave 3/4 writers who expect a fill-in-the-blank skeleton.

**Purpose:** Helps writers determine which of the four Diataxis quadrants a document belongs to before they begin writing. Writers start here: select quadrant, then copy the corresponding organism skeleton or template.

**Quadrant selector:**

```
Is the reader LEARNING something new? (Acquisition axis)
  YES + Action → Tutorial (O-01) → Use TP-01 with Tutorial adaptations
  YES + Cognition → Explanation (O-04) → Use skeleton from O-04 section

Is the reader DOING something? (Application axis)
  YES + Action → How-To Guide (O-02) → Use TP-01
  YES + Cognition → Reference (O-03) → Use TP-02 (agent) or O-03 skeleton

Unsure? Use the two-axis test in skills/diataxis/rules/diataxis-standards.md Section 4.
```

**Canonical exemplar:** The four PASS documents each instantiate one quadrant.

---

## Existing Pages Audit

Which existing documents instantiate which templates, and how well.

### Pages that PASS (template exemplars)

| Document | Template Used | Compliance | Exemplar Quality | Notes |
|----------|--------------|------------|-----------------|-------|
| `docs/reference/claude-code-permissions.md` | TP-02 (Reference entry) | Full | HIGH | Best reference exemplar. R-01 through R-07 pass. Exemplar for **Diataxis structural patterns only** — do not copy specific prose phrasings without checking the Atoms Catalog. |
| `docs/reference/ci-cd-pipeline-security.md` | TP-02 (Reference entry) | Full | HIGH | Large-scale reference (636 lines). Demonstrates reference at scale. Same scope caveat as above. |
| `docs/explanation/ci-cd-supply-chain-security.md` | O-04 (Explanation skeleton) | Full | HIGH | Best explanation exemplar. E-01 through E-07 pass. Canonical explanation model. |
| `docs/explanation/permission-security-model.md` | O-04 (Explanation skeleton) | Full | HIGH | Shorter explanation with explicit Scope Callout (M-13). Good model for bounded-scope E-06 compliance. |
| `docs/runbooks/getting-started.md` | O-01 (Tutorial skeleton) via TP-01 | Partial | MEDIUM | Best tutorial attempt. Fails T-04 (CLI vs. plugin branching in Step 3). Prerequisites Block and Command+Output pairs are canonical-quality. Must fix T-04 before using as Wave 4 exemplar. |
| `docs/playbooks/problem-solving.md` | TP-01 (How-To via O-02) | Partial | MEDIUM | Best how-to attempt. Fails H-02 (reference tables embedded). When-to-Use / Not-Use pair and Prerequisites Block are canonical-quality. |

### Pages that NEED REVISION (anti-exemplars to avoid)

| Document | Template Mismatch | Primary Violations | Teaching Points for Writers |
|----------|-------------------|-------------------|-----------------------------|
| `docs/INSTALLATION.md` | TP-01 (How-To) with marketing contamination | HAP-01 (marketing voice in lines 1-3), HAP-04 (stale skills table), H-04 violations | **Do NOT use as a model.** See [INSTALLATION.md Enforcement](#installationmd-enforcement) for active controls. |
| `docs/BOOTSTRAP.md` | TP-01 (How-To) with explanation section | EAP-02 (explanation in how-to: "How It Works" block lines 63-82) | Extract "How It Works" → O-04 Explanation Skeleton. |
| `docs/CLAUDE-MD-GUIDE.md` | TP-01 (How-To) with explanation contamination | Quadrant mixing, missing navigation table (H-23 violation) | Shows H-23 violation — no navigation table on a 90-line document. |
| `AGENTS.md` | TP-02 (Reference) with explanation section | RAP-03 (narrative explanation: "Agent Philosophy" lines 36-44) | Extract philosophy → O-04 Explanation Skeleton. |

---

## Gaps Analysis

Patterns Jerry needs but does not have.

### G-01: Tutorial Coverage — Zero Docs Exist

**Gap:** `docs/tutorial/` directory does not exist. No skill has a tutorial. The Diataxis audit confirmed 0% tutorial coverage across all 30 skills.

**Impact on Wave 3/4:** Writers have no exemplar to copy for tutorial-quadrant docs. The O-01 Tutorial Skeleton in this taxonomy and `docs/runbooks/getting-started.md` (partial, T-04 violation) are the only available references.

**Recommendation:** Before Wave 4 begins tutorial writing, remediate `docs/runbooks/getting-started.md` T-04 branching violation. This is a Wave 3 gate action, not optional. Create `docs/tutorial/` directory with a stub README referencing this taxonomy. Wave 4 tutorial writing is gated on a working exemplar.

---

### G-02: Per-Skill How-To Guides — 26 of 30 Missing

**Gap:** Only 4 skills have partial how-to coverage (problem-solving, orchestration, transcript, plugin-development). 26 skills — including all 16 new skills added since PROJ-015 — have zero how-to documentation.

**Impact:** Users of `contract-design`, `test-spec`, `use-case`, `diataxis`, all UX sub-skills, and 20 others have no procedural documentation.

**Recommendation:** TP-01 (Per-Skill How-To Template) in this taxonomy is the primary deliverable for Wave 3/4. Prioritize the 10 UX sub-skills first (Wave 1 product context) then the remaining 16. Each writer must complete the Goal Statement section (M-09) before beginning a skill guide.

---

### G-03: Agent Reference Entries — None Exist as Per-Agent Docs

**Gap:** `AGENTS.md` provides a catalog but not per-agent reference entries. TP-02 (Agent Reference Entry Template) in this taxonomy is the target structure but has zero current instantiations.

**Impact:** Users cannot look up a specific agent's input schema, output location, or behavioral constraints without reading the full agent `.md` file in `skills/*/agents/`.

**Recommendation:** Wave 4 deliverable. Start with the 9 problem-solving agents (ps-researcher through ps-reporter) as they have the highest reuse frequency.

---

### G-04: Explanation Coverage for Skill Design Rationale — Zero Docs Exist

**Gap:** The two existing explanation docs cover CI/CD security topics, not skill design. No explanation doc covers why Context Rot is the core problem, how the wave progression works, why the hook-based enforcement model was chosen, or how the orchestrator-worker topology constrains agent design.

**Impact:** Users and contributors cannot understand the "why" behind Jerry's design without reading internal governance files.

**Recommendation:** Wave 4 minimum: one explanation doc per skill family. Priority: `/user-experience` skill family (Wave 1 context), problem-solving, orchestration.

---

### G-05: Troubleshooting Molecule — Now Named (M-12)

**Resolution:** This gap is closed in iter-2. M-12 (Troubleshooting Table) is now formally named with canonical form. See [M-12](#m-12-troubleshooting-table-new-iter-2).

---

### G-06: Scope Callout Molecule — Now Named (M-13)

**Resolution:** This gap is closed in iter-2. M-13 (Scope Callout) is now formally named with canonical form and canonical exemplars. See [M-13](#m-13-scope-callout-new-iter-2).

---

## Composition Rules

### Valid Compositions

| From | To | Rule |
|------|----|------|
| Atom A-01 (callout) | Molecule M-01 (prerequisites) | Callout provides "Start state" framing for checklist items |
| Atom A-02 (code block) | Molecule M-03 (command+output) | Code block is the functional core; output block is verification pair |
| Atom A-04 (nav table) | All organisms | Navigation table is required in every organism (H-23) |
| Atom A-01 (callout, Scope variant) | Molecule M-13 (scope callout) | Callout + IS/IS-NOT clause structure = M-13 |
| Molecule M-01 (prerequisites) | Organism O-01 (tutorial) | Prerequisites block appears immediately before Step 1 |
| Molecule M-01 (prerequisites) | Organism O-02 (how-to) | Lightweight prerequisites appear before steps |
| Molecule M-09 (goal statement) | Organism O-01 (tutorial) | Goal block at top per T-07 |
| Molecule M-09 (goal statement) | Organism O-02 (how-to) | Goal statement before prerequisites per H-01 |
| Organism O-06 (verification) | Organism O-01 (tutorial) | End-to-end completion check; organism composes smaller organism per Frost valid composition |
| Molecule M-11 (next steps) | Organism O-01 (tutorial) | Transition to follow-on how-to guides |
| Molecule M-12 (troubleshooting) | Organism O-02 (how-to) | Failure-mode table at end of guide |
| Molecule M-13 (scope callout) | Organism O-04 (explanation) | Required near top for E-06 compliance |
| Molecule M-02 (when/not-to-use) | Organism O-05 (skill landing) | Required in SKILL.md per skill-standards.md |
| Molecule M-03 (command+output) | Organism O-01 (tutorial) | Every tutorial step that has a command uses this molecule |
| Molecule M-07 (agent table) | Organism O-05 (skill landing) | Required for multi-agent SKILL.md per skill-standards.md |
| Organism O-02 (how-to) | Template TP-01 | One-to-one instantiation for skill how-to docs |
| Organism O-03 (reference) | Template TP-02 | One-to-one instantiation for agent reference docs |
| Organism O-04 (explanation) | Template TP-03 (ADR) | O-04 adapted for Nygard ADR format |

### Forbidden Compositions

| Forbidden | Rationale | Anti-Pattern ID |
|-----------|-----------|-----------------|
| Numbered step list inside O-03 (reference) | Instructions in reference contaminate quadrant | RAP-02 |
| "Why" explanatory paragraphs between steps in O-01 or O-02 | Explanation contamination | TAP-02, HAP-01 |
| Marketing voice callout in O-02 (how-to) opening | Misuse of A-01 callout atom for promotional content | RAP-01 |
| Agent table M-07 inside O-03 (reference entry) without a clear structure mirror | Reference must mirror described structure (R-01) | RAP-05 |
| M-13 (scope callout) omitted from O-04 (explanation) | E-06 requires bounded scope statement | EAP-05 |
| Alternative Perspectives section omitted from O-04 | E-04 requires perspective acknowledgment | EAP-04 |
| Navigation table A-04 omitted from any organism | H-23 violation for all docs over 30 lines | H-23 |
| Unnamed prose section inside any organism | Breaks Frost compositional hierarchy; sub-elements must be named molecules or atoms | Organism completeness requirement |
| TP-04 / DQ-01 used as a fill-in-the-blank template | It is a selector guide, not a skeleton | IN-002 resolution |

### Optional Compositions

| Optional | When to include | When to omit |
|----------|----------------|--------------|
| M-02 (when/not-to-use pair) in O-02 (how-to) | When the guide's audience or context is ambiguous | When the guide is part of a multi-doc skill where routing is handled at the SKILL.md level |
| M-06 (criterion table) in O-03 (reference) | When the reference documents a quality standard with pass/fail criteria | For non-criteria reference docs (parameter references, command references) |
| M-08 (triple-lens table) in organisms other than O-05 | When a reference or explanation document genuinely serves 3 distinct audiences | Not needed in most single-audience how-to or tutorial docs |
| M-11 (next steps) in O-02 (how-to) | When the how-to is part of a multi-step skill workflow | For standalone guides with no obvious successor |

---

## Style Token Audit

Analogous to a design token audit — examines consistency of documentation style conventions across the seven equivalent "token categories" for docs.

### Token Category Mapping

| Token Category (UI) | Docs Equivalent | Defined Convention | Drift Ratio | Threshold Status |
|---------------------|-----------------|-------------------|-------------|-----------------|
| Color | Voice/tone per quadrant | Diataxis Section 5 per-quadrant voice guidelines | 0.54 | FAIL (> 0.20) |
| Typography | Heading hierarchy (H1 title, H2 sections, H3 subsections) | H-23 + skill-standards.md | 0.13 | PASS |
| Spacing | Horizontal rule usage between sections | One `---` per `##` section boundary | 0.20 | PASS (at threshold) |
| Breakpoints | Navigation table presence | H-23: required at 30 lines | 0.33 | FAIL (> 0.20) |
| Elevation | YAML frontmatter presence on agent outputs | Required for all agent-output docs | 0.10 | PASS |
| Border | Code block language tags | Language tag always present on fenced blocks | 0.20 | PASS (at threshold) |
| Motion | Link format (internal vs. external vs. source citation) | Internal: `[text](path)`, External: `> Source: [text](url)` | 0.27 | FAIL (> 0.20) |

**Overall drift ratio: 0.25** (arithmetic mean of 7 category ratios: (0.54 + 0.13 + 0.20 + 0.33 + 0.10 + 0.20 + 0.27) / 7 = 1.77 / 7 = 0.253, rounded to 0.25; updated in iter-3 after denominator correction for voice/tone category). The 0.20 threshold is a framework-internal heuristic: drift above 0.20 means more than 1-in-5 style values bypass the convention system.

### Voice/Tone Drift Ratio Derivation

**Denominator clarification (CC-001-2 resolution, iter-3):** The derivation table below contains 13 in-scope user-facing documents. The iter-2 text claimed "7 of 15" using "all 15 from audit report" as denominator. However, the diataxis audit report enumerates 15 documents total, of which 2 are categorized as "Out of scope" in this voice/tone analysis (`.context/rules/` representative sample and `SKILL.md` representative sample — excluded because they are not Diataxis-quadrant documents). The in-scope corpus is therefore 13 documents, not 15. Corrected voice/tone drift ratio: 7/13 = 0.538, rounded to 0.54. This is slightly worse than the iter-2 figure (0.47) because the denominator shrinks while the numerator (7 documents with drift) is unchanged.

| Document | Voice Drift? | Category |
|----------|-------------|----------|
| `docs/reference/claude-code-permissions.md` | No | PASS |
| `docs/reference/ci-cd-pipeline-security.md` | No | PASS |
| `docs/explanation/ci-cd-supply-chain-security.md` | No | PASS |
| `docs/explanation/permission-security-model.md` | No | PASS |
| `docs/runbooks/getting-started.md` | No | Partial PASS |
| `docs/playbooks/problem-solving.md` | Yes — embedded reference language in how-to | NEEDS REVISION |
| `docs/playbooks/orchestration.md` | Yes — reference tables in how-to context | NEEDS REVISION |
| `docs/playbooks/transcript.md` | Yes — reference tables in how-to context | NEEDS REVISION |
| `docs/playbooks/plugin-development.md` | Yes — reference tables in how-to context | NEEDS REVISION |
| `docs/INSTALLATION.md` | Yes — "Let's get you set up and shredding", "battle-tested" | NEEDS REVISION |
| `docs/BOOTSTRAP.md` | Yes — "How It Works" explanation in how-to | NEEDS REVISION |
| `docs/CLAUDE-MD-GUIDE.md` | No (voice is appropriate; structural issues only) | NEEDS REVISION (structure) |
| `AGENTS.md` | Yes — "Agent Philosophy" narrative in reference catalog | NEEDS REVISION |
| `.context/rules/` (representative sample) | No (rule files are not Diataxis docs; excluded from drift count) | Out of scope |
| `SKILL.md` files (representative sample) | No (multi-quadrant by design; voice mixing is appropriate) | Out of scope |

**Corpus:** 13 in-scope user-facing docs (rules files and SKILL.md excluded from voice drift calculation as they are not Diataxis-quadrant documents). Voice drift in 7 of 13 in-scope docs: 7/13 = 0.538, rounded to 0.54. The diataxis audit report lists 15 total documents; 2 are excluded from the voice/tone calculation (shown as "Out of scope" in the table above). The table row count (13 in-scope) is now the authoritative denominator.

**Note:** Iter-1 Executive Summary incorrectly promoted the voice/tone figure into the "Overall" position. Iter-2 introduced a denominator mismatch (13 rows in table vs. 15-doc claim). Iter-3 corrects the denominator to 13. Overall drift ratio is 0.25 (arithmetic mean of 7 corrected category ratios). All figures exceed the 0.20 threshold and require remediation.

### Priority Drift Instances

| Instance | Category | Document | Canonical Replacement |
|----------|----------|----------|-----------------------|
| "Let's get you set up and shredding" | Voice/tone | `docs/INSTALLATION.md` line 3 | Remove blockquote; begin with `## Prerequisites` |
| "battle-tested on macOS" | Voice/tone | `docs/INSTALLATION.md` line 5 | "Built and tested primarily on macOS" |
| "Agent Philosophy" narrative block | Voice/tone | `AGENTS.md` lines 36-44 | Extract to O-04 Explanation Skeleton |
| Missing navigation table | Nav table presence | `docs/BOOTSTRAP.md`, `docs/CLAUDE-MD-GUIDE.md` | Add `## Document Sections` table per A-04 |
| `> Source:` citation omitted | Source citation | Some playbook external links | Add `> Source: [title](url)` below any externally-sourced claims |
| Embedded reference tables | Voice/tone | `docs/playbooks/*.md` | Extract to O-03 Reference Entry docs |

---

## Taxonomy Discovery Pathway

**This section addresses P0-4 (IN-001) from the adversarial review.** The taxonomy's value is zero if Wave 3/4 writers complete their work without reading it. This section specifies the concrete integration points that surface the taxonomy at the point of writing.

### Integration Point 1: Template Header Comment (Immediate)

Every template (TP-01, TP-02, TP-03) and organism skeleton already includes the following comment in iter-2:
```
<!-- Atomic taxonomy reference: projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-008/ux-atomic-architect-output.md -->
<!-- Copy from: docs/reference/claude-code-permissions.md (structure), docs/runbooks/getting-started.md (step format) -->
<!-- Do NOT copy from: docs/INSTALLATION.md (marketing voice), docs/BOOTSTRAP.md (quadrant mixing) -->
```
Writers loading any template will see this comment before writing the first line.

### Integration Point 2: PLAN.md Reference

**Action (Wave 3 gate):** Add the following entry to `projects/PROJ-040-documentation/PLAN.md` in the Wave 3 orchestration architecture section:

```markdown
### Required Reading for Wave 3/4 Writers

Before creating any new documentation:

1. **Atomic taxonomy:** `projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-008/ux-atomic-architect-output.md`
   — Defines canonical atoms, molecules, organisms, and templates. Use before writing any doc.
2. **Diataxis standards:** `skills/diataxis/rules/diataxis-standards.md`
   — Quality criteria (T-01 through E-07) and anti-pattern catalog.
3. **Anti-exemplars:** Do NOT copy `docs/INSTALLATION.md` or `docs/BOOTSTRAP.md` structure.
```

### Integration Point 3: Wave 3/4 Orchestration Plan Required-Reading

**Action (EPIC-040-001 orchestration plan update):** When the Wave 3 orchestration plan is produced, include the atomic taxonomy as a required artifact in the `prerequisites` block for every diataxis writer agent invocation:

```yaml
prerequisites:
  - projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-008/ux-atomic-architect-output.md
  - skills/diataxis/rules/diataxis-standards.md
```

### Integration Point 4: Stub Directory Structure (Pre-Wave-4 Gate)

**Action (Wave 3 completion gate):** Create the following stub files before Wave 4 tutorial writing begins:

```
docs/tutorial/
  README.md  ← contains link to taxonomy + O-01 skeleton
docs/how-to/
  README.md  ← contains link to taxonomy + TP-01
```

Each README stub states: "Before writing in this directory, read the Atomic Design Taxonomy at `projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-008/ux-atomic-architect-output.md`."

### Integration Point 5: SKILL.md Contributor Section

**Action (Wave 4):** Each SKILL.md contributor guide section should reference the taxonomy:
```markdown
## Writing Documentation for This Skill

Follow the Per-Skill How-To Template:
`projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-008/ux-atomic-architect-output.md#tp-01-per-skill-how-to-guide-template`
```

---

## INSTALLATION.md Enforcement

**This section addresses P0-3 (PM-001) from the adversarial review.** Advisory text buried in a taxonomy document is an insufficient control against writers copying the marketing-voice anti-pattern from `docs/INSTALLATION.md`.

### Mechanism 1: HTML Comment in INSTALLATION.md (Immediate, P1)

Add the following HTML comments directly to `docs/INSTALLATION.md` at the marketing-voice locations. This is the lowest-friction enforcement mechanism — writers editing the file will see the warning at the exact anti-pattern location.

At line 3 (before "Let's get you set up and shredding"):
```html
<!-- ANTI-EXEMPLAR: Voice drift (HAP-01 marketing voice). Do not copy this pattern.
     Canonical opening: begin with ## Prerequisites, not a marketing blockquote.
     See: docs/reference/claude-code-permissions.md for canonical reference style.
     Taxonomy: projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-008/ux-atomic-architect-output.md -->
```

At line 5 (near "battle-tested"):
```html
<!-- ANTI-EXEMPLAR: "battle-tested" is marketing language. Replace with factual claim.
     Canonical: "Built and tested primarily on macOS; tested on Linux." -->
```

This action is a direct file edit to `docs/INSTALLATION.md`. It is a Wave 3 P1 action.

### Mechanism 2: Vale Lint Rule (Wave 3, P2)

If the project adopts Vale for prose linting (recommended in the Wave 5 ps-researcher recommendation), a style rule can codify the marketing-voice prohibition:

```yaml
# .vale/styles/Jerry/MarketingVoice.yml
extends: existence
message: "Marketing voice detected: '%s'. Documentation must use neutral, factual language."
level: warning
tokens:
  - "Let's get"
  - "battle-tested"
  - "shred"
  - "awesome"
  - "powerful"
  - "seamlessly"
```

This rule would prevent new marketing-voice instances from landing in any document, not just INSTALLATION.md.

### Mechanism 3: Wave 3 P1 Removal Action (FEAT-040-015)

The marketing-voice content in `docs/INSTALLATION.md` is already referenced in EPIC-040-003 FEAT-040-015 as a P1 remediation action. The enforcement here is that this taxonomy explicitly gates Wave 4 writing on FEAT-040-015 completion — writers must not begin new how-to guides until the highest-visibility anti-exemplar is fixed.

**Summary of enforcement controls:**
| Control | Type | Timing | Coverage |
|---------|------|--------|----------|
| HTML comment in INSTALLATION.md | In-file warning | Immediate (Wave 3 P1) | INSTALLATION.md only |
| Vale MarketingVoice rule | Pre-commit lint | Wave 3 P2 | All docs |
| FEAT-040-015 remediation | File edit | Wave 3 P1 | INSTALLATION.md |
| Template header comment | Point-of-writing | Immediate (in TP-01/02/03) | All new docs using templates |

---

## Synthesis Judgments Summary

| Judgment | Type | Confidence | Rationale |
|----------|------|------------|-----------|
| Classifying the Navigation Table (A-04) as an Atom rather than a Molecule | Classification | HIGH | Maps to single markdown table element with one index function. Rows are content, not constituent atoms whose removal degrades the table's function. Analogous to HTML `<table>` as atom in Frost UI hierarchy. Full rationale in A-04 entry. |
| Classifying the Prerequisites Block (M-01) as a Molecule rather than an Organism | Classification | MEDIUM | Contains 2-3 atoms (callout + checklist + optional code block), serves one reader purpose (establish start state). `getting-started.md` instantiation is more complex, but complexity is in content not structure. Classified as Molecule because functional core is always 2-3 atoms. |
| Classifying `docs/runbooks/getting-started.md` as tutorial-quadrant (partial) | Classification | HIGH | Clear T-01 (completable end-to-end), T-06 (prerequisites stated), T-07 (endpoint shown), T-02 (steps with visible results). Fails only T-04 (branching). Tutorial classification unambiguous. |
| Voice/tone drift ratio: 0.54 for 7 of 13 in-scope docs (corrected iter-3, was 0.47 of 15 in iter-2) | Token Assessment | HIGH | The diataxis audit lists 15 docs; 2 are explicitly out-of-scope for voice/tone (rules files, SKILL.md). The in-scope corpus is 13, yielding 7/13 = 0.54. The denominator and table row count now match. Confidence raised to HIGH because the arithmetic is now verifiable end-to-end from the derivation table. |
| Overall drift ratio: 0.25 as arithmetic mean of 7 category ratios (corrected iter-3, was 0.24 in iter-2) | Token Assessment | HIGH | Arithmetic mean across the 7 token categories. Updated from 0.24 to 0.25 when voice/tone denominator corrected (0.47→0.54). A weighted mean could produce a different figure if categories were weighted by document count or reuse frequency. Arithmetic mean used for simplicity and transparency. Confidence raised to HIGH because all inputs are now verifiable from the derivation table. |
| Assigning O-05 (Skill Landing Page) as organism rather than template | Classification | MEDIUM | SKILL.md is instantiated 30 times, which suggests template-level. Classified as organism because it lacks placeholder content — each SKILL.md is written with real content from day one. Templates (TP-01 through TP-03) use placeholder content. |
| Maturity classified as Nascent | Token Assessment | HIGH | Page coverage 5% (6 exemplar pages against 120+ needed), well below 30% Nascent/Developing boundary. Style drift ratio 0.25 (corrected iter-3) above 0.20 Developing threshold. Both indicators converge on Nascent. |
| Reclassifying TP-04 to DQ-01 (Selector Guide) | Classification | HIGH | TP-04 is a decision tree, not a fill-in-the-blank skeleton. Cannot be "instantiated" in the Frost sense. Keeping it as a Template misrepresents it to writers. The Selector Guide level is a deliberate extension of Frost for documentation contexts. |
| Correcting TP-03 organism mapping from O-03 to O-04 | Classification | HIGH | Nygard ADR format is discursive (Context section, narrative Decision, Options Considered = alternative perspectives). This matches O-04 (Explanation: discursive, acknowledges alternatives, bounded scope). O-03 (Reference) requires structured lookup tables and no narrative — does not match ADR format. |
| Classifying A-07 (Status Blockquote) as Atom rather than Molecule | Classification | MEDIUM | Bold label + value is a tightly-coupled text convention, not a composition of 2+ distinct atoms. A blockquote without the label is A-01; a label without the blockquote is inline text. The pairing is indivisible for the status function. Analogous to a labeled HTML attribute. |
| Classifying M-04 (Quadrant Frontmatter) as Molecule rather than Atom | Classification | MEDIUM | Contains two distinct components: YAML frontmatter block (A-08) + quality-criteria comment block. Either component can exist independently — removing the comment block leaves a valid frontmatter block (A-08); removing the frontmatter leaves a valid comment block. Two independently-valid atoms whose combination serves a single purpose (quadrant + quality signal). Molecule classification justified. |
| Classifying M-05 (Playbook Header) as Molecule rather than Organism | Classification | MEDIUM | Contains H1 title + A-07 + A-04. Three atoms. Boundary check: does M-05 contain other molecules? A-04 (Navigation Table) is an Atom, not a Molecule. M-05 is a flat group of 3 atoms with single purpose (open a playbook with identity + section map). Classified as Molecule. If M-08 (Triple-Lens) were embedded in M-05, it would tip to Organism — but M-08 appears as a separate section after M-05 in SKILL.md, not inside M-05. |
| Recommending per-skill how-to as Wave 3/4 first deliverable over explanation docs | Consolidation | HIGH | Audit confirms 26 skills have zero how-to coverage. How-to guides address the highest-frequency user need (doing). Explanations address lower-frequency need (understanding design rationale). Priority ordering follows user impact. |
| Classifying M-09 (Goal Statement Block) as Molecule rather than Atom | Classification | MEDIUM | Contains H2 section heading + prose goal sentence + optional scope qualifier callout (A-01). Minimum two atoms (heading + prose) when scope qualifier is absent. The heading-plus-prose pairing is the functional unit: removing either degrades the reader's ability to scope the guide. Atom count 2 (minimum) satisfies the molecule criterion. Optional third atom (M-01-scope variant) does not destabilize the classification. |
| Classifying M-11 (Next Steps Block) as Molecule rather than Atom | Classification | MEDIUM | Contains H2 section heading + bullet list of internal links (A-03) with one-line descriptions. The heading (structural marker) and the link list (navigation content) are two distinct atoms: a heading without links provides no routing; links without the heading lack contextual framing. Two-atom composition with single purpose (route reader onward). Classified as Molecule. The boundary question raised in DA-002-2 — whether a bullet list of links is one atom or many — is resolved by treating the entire list as a single list-type atom per the H2+content convention; the list cannot be further decomposed without losing the routing function. |
| Classifying M-12 (Troubleshooting Table) as Molecule rather than Organism | Classification | MEDIUM | Contains H2 heading + markdown table with Symptom/Cause/Resolution columns + optional code block (A-02) for resolution commands. Boundary check: does M-12 contain other molecules? M-03 (Command+Output Pair) is not a sub-element — resolution commands appear as inline cells, not as full M-03 patterns with expected output blocks. Flat composition of 2-3 atoms with single purpose (scannable failure-mode guidance). Classified as Molecule. If a resolution column regularly contained full M-03 patterns, M-12 would tip to organism — the current canonical form keeps resolutions to a single sentence or inline command. |
| Classifying M-13 (Scope Callout) as Molecule rather than Atom | Classification | HIGH | Contains A-01 (Admonition callout) + deliberate IS/IS-NOT clause structure. The IS/IS-NOT structure is the defining characteristic: a plain callout (A-01) states one thing; M-13 states two things in intentional contrast. Removing the IS-NOT clause demotes M-13 to A-01. Two-clause composition (one atom with a specific second clause) with single purpose (E-06 bounded scope). Classified as Molecule. Confidence HIGH: two canonical exemplars confirm the IS/IS-NOT structure as the naming criterion. |
| Promoting M-10 (Verification Block) to O-06 (Verification Organism) | Classification | HIGH | M-10 in iter-2 listed M-03 (Command+Output Pair, a Molecule) as a primary structural sub-element. The boundary adjudication rule is explicit: "if a block contains other molecules as sub-blocks, classify as organism." The promotion resolves a self-contradiction introduced when M-10 was defined without re-checking the boundary rule against the new molecule's own sub-element composition. The alternative (Option B from the review — revise the boundary rule to allow shallow molecule composition) was rejected because M-03 is a primary structural load-bearing component of O-06, not an optional or interchangeable element. The rule revision would have required evidence of a wider pattern; no such pattern was found. |

---

*Agent Version: ux-atomic-architect 1.0.1*
*Engagement ID: UX-0008*
*Output Path: `projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-008/ux-atomic-architect-output.md`*
*Degraded Mode: true (Manual Component Inventory — no Storybook MCP)*
*Phase: Wave 1 Phase 1a / PROJ-040 documentation taxonomy*
*Iteration: 3*
*Created: 2026-04-17 | Revised: 2026-04-20*
