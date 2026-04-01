<!-- TEMPLATE: persona-spectrum-template.md | VERSION: 1.1.0 | DATE: 2026-03-04 | REVISION: iter2 -- add GOVERNANCE ID INDEX footer, rule ID citations to section headers, WCAG source blockquote, LOW confidence suppression note, required judgment categories, limitations disclosure checklist item -->
<!-- SKILL: /ux-inclusive-design | AGENT: ux-inclusive-evaluator -->
<!-- SOURCE: SKILL.md [Methodology § Microsoft Inclusive Design], agent <methodology> Step 6, inclusive-design-rules.md (PS-010 through PS-014, IP-001 through IP-003, MX-001 through MX-003) -->
<!-- COMPANION: accessibility-report-template.md — this persona spectrum analysis is incorporated into the full accessibility audit report. See skills/ux-inclusive-design/templates/accessibility-report-template.md -->
<!-- USAGE: Fill {{PLACEHOLDER}} fields. Copy REPEATABLE BLOCK markers for each interaction pattern. See inclusive-design-rules.md for rule IDs governing each section. -->

# Persona Spectrum Analysis: {{TOPIC}}

> **Engagement:** {{ENGAGEMENT_ID}}
> **Product:** {{PRODUCT_NAME}}
> **Domain:** {{PRODUCT_DOMAIN}}
> **Date:** {{EVALUATION_DATE}}
> **Evaluator:** ux-inclusive-evaluator
> **Methodology:** Microsoft Inclusive Design Persona Spectrum (Microsoft, 2016)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Evaluation Context](#evaluation-context) | Product, users, evaluated interface, input artifacts |
| [Microsoft Inclusive Design Principles](#microsoft-inclusive-design-principles) | Three principles applied in this analysis |
| [Interaction Pattern Inventory](#interaction-pattern-inventory) | Identified interaction patterns for Persona Spectrum mapping |
| [Persona Spectrum Profiles](#persona-spectrum-profiles) | Per-interaction-pattern 4x3 matrix with exclusion analysis |
| [Exclusion Summary](#exclusion-summary) | Aggregated exclusion points across all interaction patterns |
| [Design Opportunities](#design-opportunities) | "Solve for one, extend to many" recommendations |
| [WCAG Cross-Reference](#wcag-cross-reference) | Persona Spectrum findings mapped to WCAG success criteria |
| [Synthesis Judgments Summary](#synthesis-judgments-summary) | AI judgment calls with confidence classification |
| [Self-Review Checklist](#self-review-checklist) | S-010: Pre-persistence verification checklist |
| [Handoff Data](#handoff-data) | Structured data for downstream sub-skill consumption |

---

## Evaluation Context

**Product:** {{PRODUCT_NAME}}
**Domain:** {{PRODUCT_DOMAIN}}
**Target Users:** {{TARGET_USER_DESCRIPTION}}
**Evaluated Interface/Flow:** {{EVALUATED_INTERFACE_DESCRIPTION}}

**Input Artifacts:**

| Source | Artifact | Description |
|--------|----------|-------------|
| {{source or "User-provided"}} | {{artifact path or description}} | {{brief description of the input}} |
<!-- Include rows for: design screenshots, component inventory from /ux-atomic-design, markup references, Figma links. Remove rows that do not apply. -->

**MCP Status:** {{Figma available | DEGRADED MODE -- screenshot-input}}

<!-- Include this block ONLY in degraded mode -->
<!-- [DEGRADED MODE] This output was produced without Figma MCP access.
     Input was provided via screenshot-input mode. Some features are reduced:
     - Cannot inspect design layers or component hierarchy programmatically
     - Cannot extract exact color values for automated contrast ratio computation
     - Cannot evaluate interactive states (animations, transitions, dynamic content)
     - Cannot access design token definitions or systematic color palette information -->

---

## Microsoft Inclusive Design Principles (ID-001 through ID-003)

This analysis applies the three principles of Microsoft Inclusive Design (Microsoft, 2016):

| Principle | Description | How Applied in This Analysis |
|-----------|-------------|-------------------------------|
| **Recognize Exclusion** | Identify who is being excluded by current design decisions | Each interaction pattern is analyzed across 4 disability types x 3 duration categories to systematically identify exclusion points |
| **Solve for One, Extend to Many** | Design for the most constrained scenario; the solution benefits everyone | Each profile identifies the permanent disability scenario as the design target; temporary and situational benefits are documented |
| **Learn from Diversity** | People who adapt to exclusion develop expertise that informs better design | Where applicable, adaptation strategies from the disability community are noted as design insights |

---

## Interaction Pattern Inventory (IP-001 through IP-003)

Interaction patterns are discrete user tasks or actions identified from the evaluated interface (IP-001, IP-002). Each pattern receives a full Persona Spectrum profile.

| Pattern ID | Interaction Pattern | Description | UI Context |
|-----------|-------------------|-------------|------------|
| INT-{{NNN}} | {{pattern name, e.g., "Complete checkout form"}} | {{brief description of the user task/action}} | {{screen, component, or flow where this interaction occurs}} |
<!-- REPEATABLE ROW: Copy row above for each interaction pattern. Identify at minimum 2 patterns per evaluated interface (IP-003). -->

**Total interaction patterns identified:** {{TOTAL_PATTERNS}}

---

## Persona Spectrum Profiles (PS-010 through PS-014, MX-001 through MX-003)

<!-- IMPORTANT: Every interaction pattern from the inventory MUST have a complete Persona Spectrum profile (PS-010). -->
<!-- Every cell in the 4x3 matrix MUST be populated (PS-012). -->
<!-- When a scenario is not applicable, state "Low exclusion risk for this combination: {brief reason}" rather than leaving the cell empty. -->

<!-- REPEATABLE BLOCK: PERSONA SPECTRUM PROFILE START -->
### Persona Spectrum: {{INTERACTION_PATTERN_NAME}}

**Pattern ID:** INT-{{NNN}}
**Interaction:** {{description of the user task/action}}

| Disability Type | Permanent | Temporary | Situational |
|----------------|-----------|-----------|-------------|
| **Visual** | {{scenario: e.g., "Blind user relying on screen reader to navigate form fields and submit order"}} | {{scenario: e.g., "User recovering from cataract surgery with temporarily reduced visual acuity"}} | {{scenario: e.g., "User completing checkout on phone in bright sunlight with screen glare"}} |
| **Motor** | {{scenario: e.g., "Single-arm user navigating form via keyboard only; cannot use mouse for field selection"}} | {{scenario: e.g., "User with arm in cast using non-dominant hand for all form interactions"}} | {{scenario: e.g., "Parent holding an infant while completing checkout one-handed on mobile"}} |
| **Auditory** | {{scenario: e.g., "Deaf user who cannot hear audio feedback or error alerts during form submission"}} | {{scenario: e.g., "User with ear infection experiencing temporary hearing loss; misses audio cues"}} | {{scenario: e.g., "User in loud coffee shop unable to hear audio confirmation sounds"}} |
| **Cognitive** | {{scenario: e.g., "User with learning disability struggling with complex form layout and unclear error messages"}} | {{scenario: e.g., "User recovering from concussion with reduced concentration and processing speed"}} | {{scenario: e.g., "User distracted by children while multitasking; loses place in multi-step form"}} |

**Exclusion Points:** {{Specific design decisions that create barriers for users in the scenarios above. Example: "Multi-step form lacks progress indicator, creating uncertainty for users with cognitive impairments; form validation errors displayed only in red text without icons, inaccessible to colorblind users; audio confirmation on submit with no visual equivalent."}}

**Design Opportunity:** {{How solving for the permanent disability scenario extends benefits to all. Example: "Adding clear progress indicators, visual+text error feedback, and visible submission confirmation benefits blind users (screen reader announces progress), users in bright sunlight (visual indicators visible), distracted parents (can easily re-orient), and users with temporary cognitive impairment (reduced memory load)."}}

**Current Compliance:** {{WCAG success criteria relevant to this interaction pattern. Example: "SC 1.3.1 (Info and Relationships), SC 3.3.1 (Error Identification), SC 3.3.3 (Error Suggestion), SC 2.4.7 (Focus Visible), SC 1.4.1 (Use of Color)"}}

**Adaptation Insights:** {{Optional: adaptation strategies observed in the disability community that inform design. Example: "Screen reader users often navigate forms by tabbing through fields rather than reading sequentially; this implies logical tab order is more critical than visual layout for this interaction pattern."}}
<!-- REPEATABLE BLOCK: PERSONA SPECTRUM PROFILE END -->

---

## Exclusion Summary

Aggregated exclusion points across all interaction patterns, organized by disability type.

### Exclusion Heat Map

| Disability Type | Exclusion Count | Most Critical Exclusion | Affected Patterns |
|----------------|----------------|------------------------|-------------------|
| Visual | {{N}} | {{most critical visual exclusion point}} | INT-{{NNN}}, INT-{{NNN}} |
| Motor | {{N}} | {{most critical motor exclusion point}} | INT-{{NNN}}, INT-{{NNN}} |
| Auditory | {{N}} | {{most critical auditory exclusion point}} | INT-{{NNN}}, INT-{{NNN}} |
| Cognitive | {{N}} | {{most critical cognitive exclusion point}} | INT-{{NNN}}, INT-{{NNN}} |
<!-- Row per disability type. Exclusion count = number of interaction patterns where this disability type has a non-"Low exclusion risk" permanent scenario. -->

### Cross-Pattern Exclusion Themes

{{Identify recurring exclusion patterns that appear across multiple interaction patterns. Example: "Color-only status indicators appear in 3 of 4 interaction patterns, creating consistent barriers for colorblind users across the checkout flow. Text-only error feedback without audio or haptic alternatives appears in 2 patterns, affecting both deaf users and users in noisy environments."}}

---

## Design Opportunities (ID-002)

"Solve for one, extend to many" recommendations aggregated across all Persona Spectrum profiles.

| Priority | Design Recommendation | Solves For (Permanent) | Extends To (Temporary + Situational) | Affected Patterns | WCAG Alignment |
|----------|----------------------|------------------------|--------------------------------------|-------------------|----------------|
| {{rank}} | {{specific design recommendation}} | {{permanent disability scenario}} | {{temporary and situational scenarios that benefit}} | INT-{{NNN}}, INT-{{NNN}} | SC {{X.Y.Z}} |
<!-- REPEATABLE ROW: Copy row above for each design recommendation. Order by priority (highest impact first). -->

---

## WCAG Cross-Reference

> **Source:** W3C (2023). Web Content Accessibility Guidelines (WCAG) 2.2. W3C Recommendation, 05 October 2023.

Persona Spectrum findings mapped to specific WCAG 2.2 success criteria for compliance integration.

| Persona Spectrum Finding | Disability Types Affected | WCAG Criterion | Principle | Level | Cross-Reference Note |
|--------------------------|--------------------------|---------------|-----------|-------|---------------------|
| {{exclusion point or design recommendation}} | {{Visual, Motor, Auditory, Cognitive}} | SC {{X.Y.Z}} | {{P/O/U/R}} | {{A/AA/AAA}} | {{how the Persona Spectrum finding relates to the WCAG criterion}} |
<!-- REPEATABLE ROW: Copy row above for each cross-reference. This table bridges the Inclusive Design and WCAG frameworks. -->

---

## Synthesis Judgments Summary (PS-014)

<!-- Required: document every AI-generated judgment (persona scenario generation, exclusion point identification, design recommendation priority, cross-reference mapping) with a confidence classification and rationale. -->
<!-- Required judgment categories: (1) at least one persona scenario generation judgment, (2) at least one exclusion point identification judgment, (3) at least one design recommendation priority judgment, (4) at least one WCAG cross-reference mapping judgment. -->

Each AI judgment call made during this Persona Spectrum analysis is listed below for synthesis confidence gate compliance per `skills/user-experience/rules/synthesis-validation.md` [Confidence Classification].

| # | Judgment Type | Decision | Rationale | Confidence |
|---|--------------|----------|-----------|------------|
| 1 | Persona scenario generation | {{e.g., "Visual-Permanent scenario for INT-001"}} | {{why this scenario was selected as representative}} | {{HIGH / MEDIUM / LOW}} |
| 2 | Exclusion point identification | {{e.g., "Color-only status indicator identified as barrier"}} | {{evidence from input artifacts supporting identification}} | {{HIGH / MEDIUM / LOW}} |
| 3 | Design recommendation priority | {{e.g., "Progress indicator ranked above error feedback"}} | {{rationale based on exclusion count and severity}} | {{HIGH / MEDIUM / LOW}} |
| 4 | WCAG cross-reference mapping | {{e.g., "Exclusion point mapped to SC 1.4.1 vs. SC 1.3.3"}} | {{why this criterion is the primary alignment}} | {{HIGH / MEDIUM / LOW}} |
<!-- REPEATABLE ROW: Add one row per AI judgment call. At minimum, one judgment per category present in the analysis. -->

**Confidence classification:**
- **HIGH:** Multiple input artifacts converge; finding is supported by both WCAG criterion evidence and multiple Persona Spectrum scenarios identifying the same barrier.
- **MEDIUM:** Single-framework reasoning; persona scenario based on AI inference from the Microsoft Inclusive Design methodology without empirical user data. Include "Validation Required" note; withhold definitive recommendation until validated with real assistive technology users.
- **LOW:** Insufficient input data; scenario speculative or based on limited artifact detail. LOW findings are permanently labeled reference-only; design recommendations structurally omitted. Flag for human review.

**Note:** All Persona Spectrum profiles carry a baseline confidence of MEDIUM per PS-014. They are heuristic models (Microsoft, 2016), not empirically grounded user research. Individual judgments within the profiles may be HIGH (when convergent with WCAG findings) or LOW (when input data is insufficient).

---

## Self-Review Checklist

Before persisting the Persona Spectrum analysis, verify all items below (S-010):

- [ ] 1. Every interaction pattern from the inventory has a complete Persona Spectrum profile (PS-010)
- [ ] 2. Every 4x3 matrix has all 12 cells populated -- no empty cells (PS-012)
- [ ] 3. Scenarios progress from Permanent to Temporary to Situational in decreasing severity (MX-002)
- [ ] 4. Each scenario is specific to the interaction pattern, not a generic disability description (MX-001)
- [ ] 5. Every profile includes Exclusion Points, Design Opportunity, and Current Compliance fields (PS-013)
- [ ] 6. The Exclusion Summary aggregates findings across all interaction patterns
- [ ] 7. Design Opportunities follow the "Solve for one, extend to many" principle (ID-002)
- [ ] 8. WCAG cross-references map Persona Spectrum findings to specific success criteria
- [ ] 9. The Synthesis Judgments Summary lists each AI judgment call with confidence classification (PS-014)
- [ ] 10. The navigation table is present with correct anchor links (H-23)
- [ ] 11. Degraded mode disclosure is present if operating without Figma MCP (P-022)
- [ ] 12. At minimum 2 interaction patterns are identified (IP-003)
- [ ] 13. Required judgment categories present in Synthesis Judgments Summary: persona scenario generation, exclusion point identification, design recommendation priority, WCAG cross-reference mapping (PS-014)
- [ ] 14. Limitations disclosure is present in the companion accessibility-report-template.md [Limitations and Reliability] section; this persona spectrum analysis inherits that disclosure (LM-001)

---

## Handoff Data

Structured data for downstream sub-skill consumption (ux-orchestrator cross-framework synthesis, `/ux-heuristic-eval` convergence detection).

### Persona Spectrum Findings for Downstream Consumption

| Pattern ID | Interaction Pattern | Exclusion Count | Most Critical Disability | Design Opportunity Summary | WCAG Criteria |
|-----------|-------------------|----------------|--------------------------|----------------------------|---------------|
| INT-{{NNN}} | {{pattern name}} | {{N exclusion points}} | {{disability type with highest impact}} | {{one-line design recommendation}} | SC {{X.Y.Z}}, SC {{X.Y.Z}} |
<!-- REPEATABLE ROW: Copy row above for each interaction pattern. -->

### Handoff YAML

```yaml
# Structured handoff for ux-orchestrator and downstream sub-skills
# Fields marked [handoff-v2] follow docs/schemas/handoff-v2.schema.json
# Fields marked [ux-ext] are ux-inclusive-design sub-skill extensions

# --- handoff-v2 schema fields ---
from_agent: ux-inclusive-evaluator                    # [handoff-v2] required
to_agent: ux-orchestrator                             # [handoff-v2] required
task: "Persona Spectrum analysis for {{TOPIC}}"         # [handoff-v2] required
success_criteria:                                     # [handoff-v2] required, min 1
  - "Every interaction pattern has a complete 4x3 Persona Spectrum profile"
  - "All 12 cells populated per profile (no empty cells)"
  - "Exclusion points identified per pattern with design opportunities"
  - "WCAG cross-references present for all findings"
artifacts:                                            # [handoff-v2] required
  - "projects/${JERRY_PROJECT}/engagements/{{ENGAGEMENT_ID}}/persona-spectrum-{{TOPIC_SLUG}}.md"
key_findings:                                         # [handoff-v2] required, 3-5 entries per CB-04
  - "{{top exclusion finding 1}}"
  - "{{top exclusion finding 2}}"
  - "{{top design opportunity}}"
blockers: []                                          # [handoff-v2] required
confidence: {{0.0-1.0}}                                # [handoff-v2] required
criticality: {{C1 / C2 / C3 / C4}}                     # [handoff-v2] required

# --- ux-inclusive-design extension fields ---
engagement_id: {{ENGAGEMENT_ID}}                        # [ux-ext] UX-{{NNNN}} format
interaction_patterns_evaluated: {{TOTAL_PATTERNS}}      # [ux-ext]
total_exclusion_points: {{TOTAL_EXCLUSION_POINTS}}      # [ux-ext]
exclusion_by_disability:                              # [ux-ext]
  visual: {{N}}
  motor: {{N}}
  auditory: {{N}}
  cognitive: {{N}}
design_opportunities_count: {{N}}                       # [ux-ext]
wcag_cross_references_count: {{N}}                      # [ux-ext]
degraded_mode: {{true / false}}                         # [ux-ext]
artifact_path: "projects/${JERRY_PROJECT}/engagements/{{ENGAGEMENT_ID}}/persona-spectrum-{{TOPIC_SLUG}}.md"  # [ux-ext]
```

---

<!-- GOVERNANCE ID INDEX: PS-010 through PS-014 (persona spectrum profiles), IP-001 through IP-003 (interaction pattern identification), MX-001 through MX-003 (matrix population), ID-001 through ID-003 (inclusive design principles), LM-001 (limitations disclosure) -->

*Template Version: 1.1.0 | /ux-inclusive-design Sub-Skill | PROJ-022 User Experience Skill*
*Source: SKILL.md [Methodology § Microsoft Inclusive Design], agent <methodology> Step 6*
*Microsoft Inclusive Design: Microsoft Corporation (2016). Microsoft Inclusive Design Toolkit. microsoft.com/design/inclusive.*
*Persona Spectrum methodology: Microsoft Inclusive Design Toolkit (2016). Permanent, Temporary, Situational disability spectrum.*
*Methodology rules: `skills/ux-inclusive-design/rules/inclusive-design-rules.md` (PS, IP, MX, ID rule families)*
*Handoff schema: `docs/schemas/handoff-v2.schema.json` (JSON Schema Draft 2020-12)*
*ORCHESTRATION: projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml*
