<!-- TEMPLATE: component-inventory-template.md | VERSION: 1.1.0 | DATE: 2026-03-04 | REVISION: iter2 — add storybook_mol_org_coverage_pct to YAML, replace two-block degraded mode with conditional single block, version-pin synthesis-validation.md, add CLS rule citations, add Design Token Categories to Organisms table, clarify Upstream Inputs instruction -->
<!-- SKILL: /ux-atomic-design | AGENT: ux-atomic-architect -->
<!-- SOURCE: SKILL.md [Output Specification], agent <output> section, agent <methodology> section, atomic-design-rules.md -->
<!-- USAGE: Fill {{PLACEHOLDER}} fields. Copy REPEATABLE BLOCK markers for each component, token category, consolidation pair, and judgment entry. See atomic-design-rules.md for rule IDs governing each section. -->

# Atomic Design Component Taxonomy: {{TOPIC}}

> **Engagement:** {{ENGAGEMENT_ID}}
> **Product:** {{PRODUCT_NAME}}
> **Date:** {{ANALYSIS_DATE}}
> **Architect:** ux-atomic-architect
> **MCP Mode:** {{Storybook-connected | Manual Component Inventory Mode}}

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | L0: Component counts, token consistency, Storybook coverage, top consolidation opportunities |
| [Engagement Context](#engagement-context) | L1: Product, users, scope, design system references, MCP status |
| [Component Inventory](#component-inventory) | L1: Full 5-level inventory with classification, variants, reuse, Storybook status |
| [Design Token Audit](#design-token-audit) | L1: Token categories, drift ratios, naming assessment, inconsistencies |
| [Composition Rules](#composition-rules) | L1: Assembly patterns, forbidden compositions, optional compositions |
| [Storybook Coverage Report](#storybook-coverage-report) | L1: Coverage percentages by level and granularity, gap prioritization |
| [Consolidation Candidates](#consolidation-candidates) | L1: Duplicate pairs, similarity, recommendations, design debt |
| [Strategic Implications](#strategic-implications) | L2: Maturity assessment, consolidation roadmap, governance recommendations |
| [Synthesis Judgments Summary](#synthesis-judgments-summary) | L1: AI judgment calls for synthesis gate |
| [Limitations and Reliability](#limitations-and-reliability) | L2: Single-architect disclosure, mode limitations |
| [Self-Review Checklist](#self-review-checklist) | S-010: Pre-persistence verification checklist |
| [Handoff Data](#handoff-data) | L1: Structured data for /ux-inclusive-design |

---

## Executive Summary

**Component Inventory Summary:**

| Level | Count |
|-------|-------|
| Atoms | {{COUNT_ATOMS}} |
| Molecules | {{COUNT_MOLECULES}} |
| Organisms | {{COUNT_ORGANISMS}} |
| Templates | {{COUNT_TEMPLATES}} |
| Pages | {{COUNT_PAGES}} |
| **Total** | **{{TOTAL_COMPONENTS}}** |

**Design Token Consistency:**
- Overall drift ratio: {{OVERALL_DRIFT_RATIO}}
- Categories with drift ratio > 0.20 (FAIL): {{FAIL_CATEGORIES_COUNT}} of 7
- Token naming convention: {{systematic | ad hoc | mixed}}

**Storybook Coverage:**
- Atom component coverage: {{ATOM_COVERAGE_PCT}}% (target: >= 80%)
- Molecule/organism component coverage: {{MOL_ORG_COVERAGE_PCT}}% (target: >= 60%)

**Design System Maturity:** {{Nascent | Developing | Mature | Optimized}}

**Top Consolidation Opportunities:**

1. {{COMPONENT_A}} / {{COMPONENT_B}} -- {{recommendation}} (effort: {{Low/Medium/High}})
2. {{COMPONENT_A}} / {{COMPONENT_B}} -- {{recommendation}} (effort: {{Low/Medium/High}})
3. {{COMPONENT_A}} / {{COMPONENT_B}} -- {{recommendation}} (effort: {{Low/Medium/High}})
<!-- List up to 5 consolidation opportunities ordered by priority (reuse frequency, then effort). -->

---

## Engagement Context

**Product:** {{PRODUCT_NAME}}
**Domain:** {{PRODUCT_DOMAIN}}
**Target Users:** {{TARGET_USER_DESCRIPTION}}
**Component Scope:** {{SCOPE_DESCRIPTION -- which screens, flows, or feature areas are inventoried}}

**Design System References:**

| Reference | URL/Path | Type |
|-----------|----------|------|
| {{Component library}} | {{URL or file path}} | {{Library / Documentation / Storybook instance}} |
<!-- REPEATABLE ROW: Add one row per design system reference. -->

**Upstream Inputs:**

| Source Sub-Skill | Artifact | Key Inputs Used |
|-----------------|----------|-----------------|
| {{sub-skill name or "None"}} | {{artifact path or "N/A"}} | {{what was extracted and used}} |
<!-- Include rows for: /ux-heuristic-eval (severity >= 2 component findings). Replace the example row placeholder with actual upstream inputs; remove this table row entirely if no upstream input applies. -->

**MCP Status:** {{Storybook-connected | DEGRADED MODE -- manual component inventory}}

<!-- Include this block ONLY in degraded mode -->
<!-- [DEGRADED MODE] This output was produced without Storybook MCP access.
     Input was provided via manual component inventory mode. Some features are reduced:
     - Cannot browse or validate live component stories
     - Cannot inspect component variants, states, or props interactively
     - Cannot verify design token usage in component implementations
     - Coverage assessment accuracy depends on user-provided inventory completeness -->

---

## Component Inventory

<!-- IMPORTANT: Inventory constructed bottom-up per TAX-003: atoms first, then molecules, organisms, templates, pages. -->
<!-- Every component MUST have a classification level (TAX-001). Ambiguous classifications require rationale (TAX-002). -->

### Atoms (Level 1)

| Component Name | Variant Count | Reuse Frequency | Storybook Status | Design Token Categories Used |
|---------------|--------------|-----------------|------------------|------------------------------|
| {{name}} | {{N}} | {{High / Medium / Low}} | {{Documented / Undocumented / Partial}} | {{color, typography, spacing, etc.}} |
<!-- REPEATABLE ROW: Copy row above for each atom. -->

### Molecules (Level 2)

| Component Name | Composed Of (Atoms) | Variant Count | Reuse Frequency | Storybook Status | Composition Parent(s) |
|---------------|---------------------|--------------|-----------------|------------------|-----------------------|
| {{name}} | {{atom1, atom2, ...}} | {{N}} | {{High / Medium / Low}} | {{Documented / Undocumented / Partial}} | {{parent organism(s) or "--"}} |
<!-- REPEATABLE ROW: Copy row above for each molecule. Every molecule MUST reference at least one atom (CMP-001). -->

### Organisms (Level 3)

| Component Name | Composed Of (Molecules/Atoms) | Variant Count | Reuse Frequency | Storybook Status | Composition Parent(s) | Layout Logic | Design Token Categories Used |
|---------------|-------------------------------|--------------|-----------------|------------------|-----------------------|-------------|------------------------------|
| {{name}} | {{molecule1, molecule2, atom1, ...}} | {{N}} | {{High / Medium / Low}} | {{Documented / Undocumented / Partial}} | {{parent template(s) or "--"}} | {{brief layout description}} | {{color, typography, spacing, etc.}} |
<!-- REPEATABLE ROW: Copy row above for each organism. Every organism MUST reference at least one molecule (CMP-002). -->

### Templates (Level 4)

| Template Name | Composed Of (Organisms) | Page Instances | Layout Purpose |
|--------------|-------------------------|----------------|----------------|
| {{name}} | {{organism1, organism2, ...}} | {{N}} | {{layout description}} |
<!-- REPEATABLE ROW: Copy row above for each template. Every template MUST reference at least one organism (CMP-003). -->

### Pages (Level 5)

| Page Name | Template | Content Variation Tested | Validation Notes |
|-----------|----------|-------------------------|-----------------|
| {{name}} | {{template name}} | {{what content variation this page tests}} | {{edge cases, empty states, error states tested}} |
<!-- REPEATABLE ROW: Copy row above for each page. Every page MUST reference exactly one template (CMP-004, TAX-006). -->

### Orphaned Components and Dangling References

<!-- TAX-007: Flag any orphaned components (referenced by no parent) or dangling references (parent references non-existent child). -->
<!-- If none, state: "No orphaned components or dangling references detected." -->

| Issue Type | Component | Description |
|-----------|-----------|-------------|
| {{Orphan / Dangling Reference}} | {{component name}} | {{explanation}} |
<!-- REPEATABLE ROW: Copy row above for each issue. -->

---

## Design Token Audit

<!-- TKN-001: All 7 token categories MUST be audited. TKN-002: Drift ratio per category, not aggregate only. -->

### Token Category Summary

| # | Token Category | Defined Tokens | Drift Ratio | Threshold Status | Drift Instances | Naming Convention |
|---|---------------|---------------|-------------|-----------------|-----------------|-------------------|
| 1 | Color | {{N}} | {{ratio}} | {{PASS / FAIL vs 0.20}} | {{count}} | {{systematic / ad hoc}} |
| 2 | Typography | {{N}} | {{ratio}} | {{PASS / FAIL vs 0.20}} | {{count}} | {{systematic / ad hoc}} |
| 3 | Spacing | {{N}} | {{ratio}} | {{PASS / FAIL vs 0.20}} | {{count}} | {{systematic / ad hoc}} |
| 4 | Breakpoints | {{N}} | {{ratio}} | {{PASS / FAIL vs 0.20}} | {{count}} | {{systematic / ad hoc}} |
| 5 | Elevation | {{N}} | {{ratio}} | {{PASS / FAIL vs 0.20}} | {{count}} | {{systematic / ad hoc}} |
| 6 | Border | {{N}} | {{ratio}} | {{PASS / FAIL vs 0.20}} | {{count}} | {{systematic / ad hoc}} |
| 7 | Motion | {{N}} | {{ratio}} | {{PASS / FAIL vs 0.20}} | {{count}} | {{systematic / ad hoc}} |

**Overall Drift Ratio:** {{OVERALL_DRIFT_RATIO}} (weighted average across categories)

**Formula:** `drift_ratio = hardcoded_values / total_style_values`

### Drift Instances

<!-- TKN-003: Every drift instance MUST list component name, hardcoded value, and suggested token replacement. -->

| Component | Token Category | Hardcoded Value | Suggested Token Replacement |
|-----------|---------------|-----------------|----------------------------|
| {{component name}} | {{category}} | {{hardcoded value, e.g., "#3B82F6"}} | {{suggested token, e.g., "color-primary-500"}} |
<!-- REPEATABLE ROW: Copy row above for each drift instance. -->

### Cross-Component Token Inconsistencies

<!-- TKN-005: Cases where two components use different tokens for the same visual purpose. -->
<!-- If none, state: "No cross-component token inconsistencies detected." -->

| Visual Purpose | Component A | Token Used | Component B | Token Used | Recommendation |
|---------------|------------|------------|------------|------------|----------------|
| {{e.g., "card padding"}} | {{name}} | {{token}} | {{name}} | {{different token}} | {{which token should be canonical}} |
<!-- REPEATABLE ROW: Copy row above for each inconsistency. -->

### Token Naming Convention Assessment

**Convention type:** {{systematic | ad hoc | mixed}}

{{One paragraph assessing the naming convention used across the design system. Systematic naming follows a predictable pattern (e.g., `{category}-{variant}-{scale}`). Ad hoc naming uses inconsistent patterns (e.g., `blue3`, `mainColor`, `sm-padding`). Mixed naming has systematic tokens in some categories and ad hoc in others. Include specific examples.}}

---

## Composition Rules

### Atom-to-Molecule Compositions

| Molecule | Atom Components | Assembly Pattern |
|----------|----------------|------------------|
| {{molecule name}} | {{atom1 + atom2 + ...}} | {{how atoms combine to form the molecule's single purpose}} |
<!-- REPEATABLE ROW: Copy row above for each atom-to-molecule composition. -->

### Molecule-to-Organism Compositions

| Organism | Molecule/Atom Components | Layout Logic |
|----------|-------------------------|-------------|
| {{organism name}} | {{molecule1 + molecule2 + atom1 + ...}} | {{internal layout description: grid, flex, positioning}} |
<!-- REPEATABLE ROW: Copy row above for each molecule-to-organism composition. -->

### Organism-to-Template Compositions

| Template | Organism Components | Spatial Arrangement |
|----------|-------------------|---------------------|
| {{template name}} | {{organism1 + organism2 + ...}} | {{how organisms are arranged on the page}} |
<!-- REPEATABLE ROW: Copy row above for each organism-to-template composition. -->

### Forbidden Compositions

<!-- CMP-005, CMP-006: Document compositions that violate design system intent. -->
<!-- If none identified, state: "No forbidden compositions identified beyond standard hierarchy constraints." -->

| Forbidden Pattern | Reason | Correct Alternative |
|------------------|--------|---------------------|
| {{e.g., "Organism nested inside organism"}} | {{why this violates the hierarchy}} | {{what to do instead}} |
<!-- REPEATABLE ROW: Copy row above for each forbidden composition. -->

### Optional Compositions

<!-- CMP-007: Components that may or may not appear in a parent. -->

| Parent Component | Optional Child | Condition |
|-----------------|---------------|-----------|
| {{parent name}} | {{optional child name}} | {{when the child appears vs. when it is absent}} |
<!-- REPEATABLE ROW: Copy row above for each optional composition. -->

---

## Storybook Coverage Report

<!-- COV-001: Coverage calculated per hierarchy level. COV-002: Compared against heuristic targets with PASS/FAIL. -->

### Component Coverage by Level

| Level | Total Components | Documented | Coverage % | Target | Status |
|-------|-----------------|-----------|-----------|--------|--------|
| Atoms | {{N}} | {{N}} | {{%}} | >= 80% | {{PASS / FAIL}} |
| Molecules | {{N}} | {{N}} | {{%}} | >= 60% | {{PASS / FAIL}} |
| Organisms | {{N}} | {{N}} | {{%}} | >= 60% | {{PASS / FAIL}} |
| Templates | {{N}} | {{N}} | {{%}} | -- | {{N/A}} |
| Pages | {{N}} | {{N}} | {{%}} | -- | {{N/A}} |

### State Coverage (Atoms and Molecules)

<!-- COV-005: State coverage assessed at atom and molecule levels only. -->

| Level | Total Applicable States | Documented States | Coverage % | Target | Status |
|-------|------------------------|-------------------|-----------|--------|--------|
| Atoms | {{N}} | {{N}} | {{%}} | >= 70% | {{PASS / FAIL}} |
| Molecules | {{N}} | {{N}} | {{%}} | >= 50% | {{PASS / FAIL}} |

**States assessed:** default, hover, active, disabled, error, loading

### Variant Coverage (Atoms and Molecules)

| Level | Total Variants | Documented Variants | Coverage % | Target | Status |
|-------|---------------|--------------------|-----------| --------|--------|
| Atoms | {{N}} | {{N}} | {{%}} | >= 60% | {{PASS / FAIL}} |
| Molecules | {{N}} | {{N}} | {{%}} | >= 40% | {{PASS / FAIL}} |

### Undocumented Components (Prioritized)

<!-- COV-003: Prioritized by reuse frequency, then hierarchy level, then complexity. -->

| Priority | Component Name | Level | Reuse Frequency | Variant Count | Gap Severity |
|----------|---------------|-------|-----------------|--------------|-------------|
| 1 | {{name}} | {{level}} | {{High / Medium / Low}} | {{N}} | {{HIGH / MEDIUM / LOW}} |
<!-- REPEATABLE ROW: Copy row above for each undocumented component. Order by priority descending. -->
<!-- Gap severity: HIGH = high-reuse atom with multiple variants. MEDIUM = moderate-reuse molecule. LOW = low-reuse organism. -->

---

## Consolidation Candidates

<!-- CSL-001: Each pair MUST include similarity, recommendation, and effort. -->
<!-- CSL-004: Prioritized by reuse frequency, estimated effort, downstream impact. -->

| Priority | Component A | Component B | Similarity | Recommendation | Estimated Effort | Rationale |
|----------|------------|------------|-----------|----------------|-----------------|-----------|
| 1 | {{name}} | {{name}} | {{HIGH / MEDIUM}} | {{Merge / Deduplicate / Keep both}} | {{Low / Medium / High}} | {{one-line rationale}} |
<!-- REPEATABLE ROW: Copy row above for each consolidation pair. -->

### Design Debt Summary

| Debt Factor | Count | Severity |
|-------------|-------|----------|
| Token drift violations (categories > 0.20) | {{N}} | HIGH |
| Undocumented Storybook stories | {{N}} | MEDIUM |
| Orphaned components | {{N}} | MEDIUM |
| Dangling references | {{N}} | HIGH |
| Naming inconsistencies | {{N}} | LOW |
| HIGH-similarity consolidation candidates | {{N}} | MEDIUM |
| **Total design debt items** | **{{TOTAL}}** | |

---

## Strategic Implications

<!-- Required: identify at least one finding per subsection. Minimum two sentences per subsection. -->

### Design System Maturity Assessment

**Classification:** {{Nascent | Developing | Mature | Optimized}}

**Evidence:**
- Component coverage: {{PCT}}% (threshold: {{maturity level boundary}})
- Average drift ratio: {{RATIO}} (threshold: {{maturity level boundary}})
- Composition rules: {{documented / partially documented / undocumented}}

{{One paragraph explaining how the coverage and drift ratio evidence supports this maturity classification, including any cases where the two dimensions point to different maturity levels (MAT-003: classify at the lower level).}}

### Component Consolidation Roadmap

{{Ordered list of consolidation actions with estimated effort and expected benefit. Start with low-effort, high-reuse-frequency consolidations. Group by hierarchy level where applicable. Example: "Phase 1 (1-2 weeks): Merge ButtonPrimary/ButtonNew atoms -- reduces atom count by 1, affects 12 molecules. Phase 2 (2-3 weeks): Deduplicate CardHeader variants across dashboard and product organisms."}}

### Design Debt Reduction Trajectory

{{Assessment of the current design debt level and recommended reduction sequence. Reference the Design Debt Summary counts. Example: "Current debt: 15 items (3 HIGH, 8 MEDIUM, 4 LOW). Priority reduction path: resolve 3 HIGH items (token drift in Color and Spacing categories, 2 dangling references) within the first sprint. Target: reduce total debt to < 8 items within 3 sprints."}}

### Design System Governance Recommendations

{{Recommendations for ongoing design system governance based on findings. Examples: "Establish a token review gate for new components -- no PR merges without token compliance check"; "Implement automated Storybook coverage reporting in CI to maintain > 80% atom coverage"; "Schedule quarterly component consolidation reviews to prevent duplicate proliferation."}}

---

## Synthesis Judgments Summary

<!-- Required: document every AI-generated judgment with confidence classification (CLS-001). -->

Each AI judgment call made during this taxonomy construction is listed below for synthesis confidence gate compliance per `skills/user-experience/rules/synthesis-validation.md` (v1.1.0) [Confidence Classification].

| # | Judgment Type | Decision | Rationale | Confidence |
|---|--------------|----------|-----------|------------|
| 1 | Component classification | {{e.g., "SearchForm classified as molecule vs. organism"}} | {{why this level was chosen; cite adjudication check number if applicable}} | {{HIGH / MEDIUM / LOW}} |
| 2 | Boundary adjudication | {{e.g., "Header classified as organism using ADJ check 1 (contains molecules)"}} | {{which adjudication check determined the classification}} | {{HIGH / MEDIUM / LOW}} |
| 3 | Drift ratio assessment | {{e.g., "Color category drift ratio 0.25 based on 5/20 hardcoded values"}} | {{data source and calculation basis}} | {{HIGH / MEDIUM / LOW}} |
| 4 | Consolidation recommendation | {{e.g., "ButtonPrimary / ButtonNew recommended for Merge"}} | {{similarity evidence and reuse frequency}} | {{HIGH / MEDIUM / LOW}} |
| 5 | Maturity classification | {{e.g., "Design system classified as Developing"}} | {{coverage and drift ratio evidence supporting the classification}} | {{HIGH / MEDIUM / LOW}} |
<!-- REPEATABLE ROW: Add one row per AI judgment call. At minimum, one judgment per category present in the analysis. -->

**Confidence classification** (reflects CLS-001 through CLS-004 from `atomic-design-rules.md`):
- **HIGH:** Multiple data sources converge; validated by Storybook inspection or multiple upstream sub-skill findings. Acknowledgment required before acting on design recommendations. (CLS-002 criterion: NEVER classified HIGH in manual inventory mode without multiple independent data sources.)
- **MEDIUM:** Single-framework reasoning; classification based on methodology criteria without live Storybook verification. Include "Validation Required" note; confirm against live component library before restructuring. (CLS-001: rationale required.)
- **LOW:** Insufficient data; AI inference from text descriptions without programmatic component inspection. LOW findings are permanently labeled reference-only; design restructuring recommendations structurally omitted. Flag for human review before acting (CLS-001). (CLS-003: design token consistency from text descriptions MUST be LOW. CLS-004: composite findings use lowest contributing confidence.)

---

## Limitations and Reliability

### Single-Architect Disclosure (P-022)

Brad Frost's Atomic Design methodology recommends collaborative component classification with the full design and development team for shared vocabulary establishment (Frost, 2016). This taxonomy was constructed by a **single AI architect**.

**Compensating factors:**
- Systematic 5-phase methodology coverage with structured identification criteria per hierarchy level
- Deterministic boundary adjudication procedure for ambiguous molecule/organism classifications
- Consistent drift ratio calculation using the same formula across all token categories
- Bottom-up inventory construction order ensuring foundational components are classified first

**Residual limitations:**
- No perspective diversity from cross-functional team collaboration
- Component classification boundary decisions may differ from the team's established conventions
- Design system context-specific patterns (organizational naming conventions, historical component decisions) may be missed
- Component inventories are starting points for team discussion, not definitive taxonomies

### Input Mode Limitations (P-022 compliance required)

<!-- CONDITIONAL BLOCK: Replace {{INPUT_MODE_LIMITATIONS}} with ONE of the two options below based on MCP status. -->
<!-- OPTION A (Storybook-connected): "Full Storybook component inspection available. No mode-specific limitations." -->
<!-- OPTION B (Degraded mode): Use the full degraded mode block below. -->

{{INPUT_MODE_LIMITATIONS}}

<!-- BEGIN OPTION B (Degraded mode) — copy this block when MCP Status = DEGRADED MODE -->
<!-- **[DEGRADED MODE]** This output was produced without Storybook MCP access. Input was provided via manual component inventory mode. The following features are reduced:
- Component inventories produced from user-provided lists and documentation; programmatic component discovery not available
- Variant counts are user-reported estimates; exhaustive enumeration not possible
- State coverage based on user-listed states; unlisted states not assessed
- Design token audit based on documentation analysis; CSS/style declaration inspection not available
- Storybook coverage percentages depend on completeness of user-provided inventory data
- Composition rules inferred from descriptions; programmatic import tree analysis not available -->
<!-- END OPTION B -->

### Recommendation for Design System Restructuring

For component taxonomies that will drive **design system restructuring decisions** (component library reorganization, design token refactoring, composition rule enforcement):
- Validate the component inventory against the live Storybook instance or codebase before acting on restructuring recommendations
- Review boundary adjudication decisions (molecule vs. organism) with the design team to confirm alignment with team conventions
- Confirm design token drift instances by inspecting actual CSS/style declarations, not just documentation
- Treat consolidation recommendations as starting points for team discussion, not mandates

---

## Self-Review Checklist

Before persisting the report, verify all items below (S-010):

- [ ] 1. All 5 hierarchy levels represented in inventory (or explicitly empty with rationale) (TAX-001)
- [ ] 2. Every ambiguous classification includes a rationale with adjudication check number (TAX-002, ADJ-002)
- [ ] 3. Inventory constructed bottom-up: atoms, molecules, organisms, templates, pages (TAX-003)
- [ ] 4. Every molecule references at least one atom (CMP-001)
- [ ] 5. Every organism references at least one molecule (CMP-002)
- [ ] 6. Every template references at least one organism; every page references exactly one template (CMP-003, CMP-004)
- [ ] 7. Orphaned components and dangling references flagged and listed (TAX-007)
- [ ] 8. All 7 token categories audited with drift ratio per category (TKN-001, TKN-002)
- [ ] 9. Every drift instance lists component name, hardcoded value, and suggested replacement (TKN-003)
- [ ] 10. Storybook coverage calculated per level with PASS/FAIL against targets (COV-001, COV-002)
- [ ] 11. Undocumented components prioritized by reuse frequency, hierarchy level, complexity (COV-003)
- [ ] 12. Consolidation candidates include similarity, recommendation, and estimated effort (CSL-001)
- [ ] 13. Design system maturity classified with coverage and drift ratio evidence (MAT-001, MAT-002)
- [ ] 14. Synthesis Judgments Summary lists every AI judgment call with confidence classification (CLS-001)
- [ ] 15. Navigation table present with correct anchor links (H-23, quality-enforcement.md)
- [ ] 16. Degraded mode disclosure present if operating in Manual Component Inventory Mode (P-022)
- [ ] 17. Handoff Data section populated for `/ux-inclusive-design` downstream consumption
- [ ] 18. Same component pattern classified consistently across the entire inventory (ADJ-004)

---

## Handoff Data

Structured data for downstream sub-skill consumption (`/ux-inclusive-design`). Only components with classification level assigned (atom through page) and at least a name and variant count are included per the cross-framework handoff threshold.

### Components for Downstream Consumption

| Component Name | Level | Variant Count | Storybook URL | Design Token Categories Used |
|---------------|-------|--------------|---------------|------------------------------|
| {{name}} | {{Atom / Molecule / Organism / Template / Page}} | {{N}} | {{URL or N/A}} | {{color, typography, spacing, etc.}} |
<!-- REPEATABLE ROW: Copy row above for each component meeting the handoff threshold. -->
<!-- Components identified but not yet classified are NOT included in handoff data. -->

### Handoff YAML

```yaml
# Structured handoff for ux-orchestrator and downstream sub-skills
# Fields marked [handoff-v2] follow docs/schemas/handoff-v2.schema.json
# Fields marked [ux-ext] are ux-atomic-design sub-skill extensions

# --- handoff-v2 schema fields ---
from_agent: ux-atomic-architect                    # [handoff-v2] required
to_agent: ux-orchestrator                          # [handoff-v2] required
task: "Atomic Design component taxonomy for {{TOPIC}}"  # [handoff-v2] required
success_criteria:                                  # [handoff-v2] required, min 1
  - "All 5 hierarchy levels represented in inventory"
  - "All 7 token categories audited with drift ratio"
  - "Storybook coverage calculated per level with PASS/FAIL"
  - "Consolidation candidates identified with recommendations"
  - "Design system maturity classified with evidence"
artifacts:                                         # [handoff-v2] required
  - "projects/${JERRY_PROJECT}/engagements/{{ENGAGEMENT_ID}}/ux-atomic-architect-{{TOPIC_SLUG}}.md"
key_findings:                                      # [handoff-v2] required, 3-5 entries per CB-04
  - "{{top finding 1 summary}}"
  - "{{top finding 2 summary}}"
  - "{{top finding 3 summary}}"
blockers: []                                       # [handoff-v2] required
confidence: {{0.0-1.0}}                             # [handoff-v2] required
criticality: {{C1 / C2 / C3 / C4}}                  # [handoff-v2] required

# --- ux-atomic-design extension fields ---
engagement_id: {{ENGAGEMENT_ID}}                     # [ux-ext] UX-{NNNN} format
total_components: {{TOTAL_COMPONENTS}}               # [ux-ext]
component_distribution:                            # [ux-ext]
  atoms: {{COUNT_ATOMS}}
  molecules: {{COUNT_MOLECULES}}
  organisms: {{COUNT_ORGANISMS}}
  templates: {{COUNT_TEMPLATES}}
  pages: {{COUNT_PAGES}}
design_token_drift_ratio: {{OVERALL_DRIFT_RATIO}}    # [ux-ext] overall drift ratio
storybook_coverage_pct: {{ATOM_COVERAGE_PCT}}        # [ux-ext] component-level coverage (atoms)
storybook_mol_org_coverage_pct: {{MOL_ORG_COVERAGE_PCT}}  # [ux-ext] component-level coverage (molecules/organisms)
consolidation_candidates: {{CONSOLIDATION_COUNT}}    # [ux-ext]
design_system_maturity: {{nascent | developing | mature | optimized}}  # [ux-ext]
degraded_mode: {{true / false}}                      # [ux-ext]
artifact_path: "projects/${JERRY_PROJECT}/engagements/{{ENGAGEMENT_ID}}/ux-atomic-architect-{{TOPIC_SLUG}}.md"  # [ux-ext]
handoff_components_count: {{HANDOFF_COUNT}}           # [ux-ext] components meeting handoff threshold for /ux-inclusive-design
```

---

*Template Version: 1.1.0 | /ux-atomic-design Sub-Skill | PROJ-022 User Experience Skill*
*Source: SKILL.md [Output Specification], agent [output] section, agent [methodology] section*
*Atomic Design framework: Frost, B. (2016). "Atomic Design." Self-published. atomicdesign.bradfrost.com.*
*Storybook coverage model: Storybook (2024). "Introduction to Storybook." storybook.js.org/tutorials/intro-to-storybook/*
*Methodology rules: `skills/ux-atomic-design/rules/atomic-design-rules.md` (TAX, CMP, ADJ, TKN, COV, CSL, MAT, CLS, QG rule families)*
*Handoff schema: `docs/schemas/handoff-v2.schema.json` (JSON Schema Draft 2020-12, schema v2.0.0)*
*ORCHESTRATION: projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml*
