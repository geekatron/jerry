<!-- TEMPLATE: accessibility-report-template.md | VERSION: 1.1.0 | DATE: 2026-03-04 | REVISION: iter2 -- add GOVERNANCE ID INDEX footer, rule ID citations to section headers, REPEATABLE BLOCK markers for O/U/R WCAG subsections, legal source blockquote, new-in-2.2 annotations, companion template note in Persona Spectrum section -->
<!-- SKILL: /ux-inclusive-design | AGENT: ux-inclusive-evaluator -->
<!-- SOURCE: SKILL.md [Output Specification], agent <output> section, agent <methodology> section, inclusive-design-rules.md -->
<!-- COMPANION: persona-spectrum-template.md — produces the standalone Persona Spectrum analysis (Step 6 worksheet) that is incorporated into this report. See skills/ux-inclusive-design/templates/persona-spectrum-template.md -->
<!-- USAGE: Fill {{PLACEHOLDER}} fields. Copy REPEATABLE BLOCK markers for each criterion, element, finding, pattern, and remediation item. See inclusive-design-rules.md for rule IDs governing each section. -->

# Inclusive Design Evaluation: {{TOPIC}}

> **Engagement:** {{ENGAGEMENT_ID}}
> **Product:** {{PRODUCT_NAME}}
> **Domain:** {{PRODUCT_DOMAIN}}
> **Date:** {{EVALUATION_DATE}}
> **Evaluator:** ux-inclusive-evaluator
> **Target Conformance Level:** {{A | AA | AAA}}

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | L0: Conformance level, critical violations, Persona Spectrum coverage, top remediation priorities |
| [Engagement Context](#engagement-context) | L1: Product, users, target level, input artifacts, MCP status |
| [WCAG 2.2 Compliance Audit](#wcag-22-compliance-audit) | L1: Per-criterion pass/fail by POUR principle with evidence and severity |
| [Color Contrast Analysis](#color-contrast-analysis) | L1: Per-element contrast ratios with pass/fail status |
| [Keyboard Navigation Audit](#keyboard-navigation-audit) | L1: Tab order, focus visibility, keyboard traps, shortcut conflicts |
| [Screen Reader Compatibility](#screen-reader-compatibility) | L1: Heading hierarchy, ARIA landmarks, alt text, form labels, live regions |
| [Cognitive Load Assessment](#cognitive-load-assessment) | L1: Reading level, navigation consistency, error prevention, input assistance |
| [Persona Spectrum Analysis](#persona-spectrum-analysis) | L1: Per-interaction-pattern profiles with permanent/temporary/situational mapping |
| [Remediation Priorities](#remediation-priorities) | L1: Prioritized remediation list with WCAG references and severity |
| [Strategic Implications](#strategic-implications) | L2: Accessibility maturity, legal compliance gaps, accessibility debt, adoption roadmap |
| [Synthesis Judgments Summary](#synthesis-judgments-summary) | L1: AI judgment calls for synthesis gate |
| [Limitations and Reliability](#limitations-and-reliability) | L2: Single-evaluator disclosure, mode limitations |
| [Self-Review Checklist](#self-review-checklist) | S-010: Pre-persistence verification checklist |
| [Handoff Data](#handoff-data) | L1: Structured data for downstream sub-skills |

---

## Executive Summary

**Conformance Level:**

| Target | Achieved | Gap |
|--------|----------|-----|
| {{A / AA / AAA}} | {{A / AA / AAA / None}} | {{N criteria failed at target level}} |

**POUR Principle Results:**

| Principle | Status |
|-----------|--------|
| Perceivable | {{PASS / FAIL}} |
| Operable | {{PASS / FAIL}} |
| Understandable | {{PASS / FAIL}} |
| Robust | {{PASS / FAIL}} |

**Violation Summary:**

| Severity | Count | Label |
|----------|-------|-------|
| 4 | {{N}} | Critical -- blocks access |
| 3 | {{N}} | Major barrier |
| 2 | {{N}} | Minor barrier |
| 1 | {{N}} | Cosmetic |
| **Total FAIL** | **{{N}}** | |

**Persona Spectrum Coverage:**
- {{N}} interaction patterns evaluated
- {{N}} exclusion points identified
- Most affected disability type: {{Visual / Motor / Auditory / Cognitive}}

**Top Remediation Priorities:**

1. {{SC X.Y.Z: Brief description -- Severity 4}}
2. {{SC X.Y.Z: Brief description -- Severity 3-4}}
3. {{SC X.Y.Z: Brief description -- Severity 3}}
4. {{SC X.Y.Z: Brief description -- Severity 2-3}}
5. {{SC X.Y.Z: Brief description -- Severity 2}}
<!-- List up to 5 items ordered by severity descending then conformance level ascending (RP-001) -->

**MCP Status:** {{Figma available | DEGRADED MODE -- screenshot-input}}

---

## Engagement Context

**Product:** {{PRODUCT_NAME}}
**Domain:** {{PRODUCT_DOMAIN}}
**Target Users:** {{TARGET_USER_DESCRIPTION}}
**Target Conformance Level:** {{A | AA | AAA}}

**Input Artifacts:**

| Source | Artifact | Description |
|--------|----------|-------------|
| {{source}} | {{artifact path or description}} | {{brief description}} |
<!-- Include rows for: design screenshots, component inventory from /ux-atomic-design, markup references, Figma links. -->

**Upstream Sub-Skill Data:**

| From Sub-Skill | Artifact | Key Inputs Used |
|----------------|----------|-----------------|
| {{sub-skill name or "None"}} | {{artifact path or "N/A"}} | {{what was extracted and used}} |
<!-- Include rows for: /ux-heuristic-eval (severity >= 2 findings), /ux-atomic-design (component inventory). Remove rows with no upstream input. -->

**MCP Status:** {{Figma available | DEGRADED MODE -- screenshot-input}}

<!-- Include this block ONLY in degraded mode -->
<!-- [DEGRADED MODE] This output was produced without Figma MCP access.
     Input was provided via screenshot-input mode. Some features are reduced:
     - Cannot inspect design layers or component hierarchy programmatically
     - Cannot extract exact color values for automated contrast ratio computation
     - Cannot evaluate interactive states (animations, transitions, dynamic content)
     - Cannot access design token definitions or systematic color palette information -->

---

## WCAG 2.2 Compliance Audit (PR-001 through PR-003, SC-001 through SC-006)

Per-criterion evaluation organized by POUR principle. Each criterion evaluated up to and including the target conformance level ({{A / AA / AAA}}).

> **Evaluation methodology:** WCAG 2.2 (W3C, 2023). Principles evaluated in POUR order (PR-001). Severity aligned with Nielsen (1994b) scale (inclusive-design-rules.md [Severity Scale]).

### Perceivable (P)

<!-- REPEATABLE BLOCK: CRITERION START -->
#### SC {{X.Y.Z}}: {{Success Criterion Name}} [{{Level}}]

- **Status:** {{PASS | FAIL | NOT APPLICABLE}}
- **Evidence:** {{specific observation, measurement, or test result -- not a restatement of the criterion (SC-003)}}
- **Affected Elements:** {{specific UI element references, selectors, or screen locations (SC-004)}}
- **Severity:** {{0 | 1 | 2 | 3 | 4}} {{(not a problem) | (cosmetic) | (minor barrier) | (major barrier) | (critical -- blocks access)}}
- **Remediation:** {{specific fix with WCAG technique reference, e.g., "Apply ARIA-label per Technique ARIA14" (SC-006)}}
<!-- REPEATABLE BLOCK: CRITERION END -->
<!-- Repeat for each Perceivable success criterion at the target conformance level -->
<!-- Key criteria: 1.1.1 (A), 1.3.1-1.3.6 (A-AA), 1.4.1-1.4.13 (A-AAA) -->

### Operable (O)

<!-- REPEATABLE BLOCK: CRITERION START -->
#### SC {{X.Y.Z}}: {{Success Criterion Name}} [{{Level}}]

- **Status:** {{PASS | FAIL | NOT APPLICABLE}}
- **Evidence:** {{specific observation, measurement, or test result -- not a restatement of the criterion (SC-003)}}
- **Affected Elements:** {{specific UI element references, selectors, or screen locations (SC-004)}}
- **Severity:** {{0 | 1 | 2 | 3 | 4}} {{(not a problem) | (cosmetic) | (minor barrier) | (major barrier) | (critical -- blocks access)}}
- **Remediation:** {{specific fix with WCAG technique reference, e.g., "Apply keyboard handler per Technique G202" (SC-006)}}
<!-- REPEATABLE BLOCK: CRITERION END -->
<!-- Repeat for each Operable success criterion at the target conformance level -->
<!-- Key criteria: 2.1.1-2.1.4 (A), 2.2.1-2.2.6 (A-AAA), 2.3.1-2.3.3 (A-AAA), 2.4.1-2.4.13 (A-AAA), 2.5.1-2.5.8 (A-AAA) -->

### Understandable (U)

<!-- REPEATABLE BLOCK: CRITERION START -->
#### SC {{X.Y.Z}}: {{Success Criterion Name}} [{{Level}}]

- **Status:** {{PASS | FAIL | NOT APPLICABLE}}
- **Evidence:** {{specific observation, measurement, or test result -- not a restatement of the criterion (SC-003)}}
- **Affected Elements:** {{specific UI element references, selectors, or screen locations (SC-004)}}
- **Severity:** {{0 | 1 | 2 | 3 | 4}} {{(not a problem) | (cosmetic) | (minor barrier) | (major barrier) | (critical -- blocks access)}}
- **Remediation:** {{specific fix with WCAG technique reference, e.g., "Use clear language per Technique G86" (SC-006)}}
<!-- REPEATABLE BLOCK: CRITERION END -->
<!-- Repeat for each Understandable success criterion at the target conformance level -->
<!-- Key criteria: 3.1.1-3.1.6 (A-AAA), 3.2.1-3.2.6 (A-AAA), 3.3.1-3.3.9 (A-AAA) -->

### Robust (R)

<!-- REPEATABLE BLOCK: CRITERION START -->
#### SC {{X.Y.Z}}: {{Success Criterion Name}} [{{Level}}]

- **Status:** {{PASS | FAIL | NOT APPLICABLE}}
- **Evidence:** {{specific observation, measurement, or test result -- not a restatement of the criterion (SC-003)}}
- **Affected Elements:** {{specific UI element references, selectors, or screen locations (SC-004)}}
- **Severity:** {{0 | 1 | 2 | 3 | 4}} {{(not a problem) | (cosmetic) | (minor barrier) | (major barrier) | (critical -- blocks access)}}
- **Remediation:** {{specific fix with WCAG technique reference, e.g., "Add name/role/value per Technique ARIA16" (SC-006)}}
<!-- REPEATABLE BLOCK: CRITERION END -->
<!-- Repeat for each Robust success criterion at the target conformance level -->
<!-- Key criteria: 4.1.2 (A), 4.1.3 (AA) -->
<!-- Note: WCAG 2.2 removed SC 4.1.1 (Parsing) -->

### Audit Summary

| Principle | Criteria Evaluated | PASS | FAIL | N/A |
|-----------|-------------------|------|------|-----|
| Perceivable | {{N}} | {{N}} | {{N}} | {{N}} |
| Operable | {{N}} | {{N}} | {{N}} | {{N}} |
| Understandable | {{N}} | {{N}} | {{N}} | {{N}} |
| Robust | {{N}} | {{N}} | {{N}} | {{N}} |
| **Total** | **{{N}}** | **{{N}}** | **{{N}}** | **{{N}}** |

**Conformance determination (CD-001 through CD-005):**
<!-- Use exactly one of these statements: -->
<!-- "Conformance level A achieved: all Level A criteria PASS or N/A." -->
<!-- "Conformance level AA achieved: all Level A and Level AA criteria PASS or N/A." -->
<!-- "Conformance level AAA achieved: all criteria at all levels PASS or N/A." -->
<!-- "Conformance level: None achieved. {{N}} Level A criteria failed." -->
<!-- "Target: {{target}}. Achieved: {{achieved}}. {{N}} criteria at {{target level}} failed." -->

---

## Color Contrast Analysis (CC-001 through CC-005)

Per-element color contrast ratio measurements with pass/fail status against target conformance level thresholds.

> **Methodology:** Contrast ratio computed as relative luminance ratio per WCAG 2.2 SC 1.4.3 (AA) and SC 1.4.6 (AAA). Thresholds: Normal text AA >= 4.5:1, AAA >= 7:1; Large text AA >= 3:1, AAA >= 4.5:1; UI components >= 3:1; Focus indicators >= 3:1. (inclusive-design-rules.md [Color Contrast Assessment Rules])

### Contrast Measurements

| Element | Type | Foreground | Background | Ratio | Target | Status |
|---------|------|-----------|-----------|-------|--------|--------|
| {{element reference}} | {{Normal text / Large text / UI component / Focus indicator}} | {{#RRGGBB or rgb(R,G,B)}} | {{#RRGGBB or rgb(R,G,B)}} | {{N.N}}:1 | {{threshold for target level}} | {{PASS / FAIL}} |
<!-- REPEATABLE ROW: Copy row above for each element measured. -->
<!-- CC-001: Every row must have foreground, background, computed ratio, target, and status -->
<!-- CC-003: NEVER claim PASS without computed ratio from hex/RGB values -->
<!-- CC-005: Document whether text is normal or large per element -->

### Elements Requiring Manual Measurement

<!-- Include this section ONLY in degraded mode -->
<!-- CC-004: In screenshot-input mode, elements with potentially insufficient contrast that lack hex/RGB values -->

| Element | Visual Assessment | Manual Verification Note |
|---------|-------------------|-------------------------|
| {{element reference}} | {{visual observation, e.g., "Light gray text on white background appears insufficient"}} | Manual verification required -- hex/RGB values not available from screenshot |
<!-- REPEATABLE ROW: Copy row for each element requiring manual measurement -->

### Contrast Summary

| Category | Measured | PASS | FAIL | Manual Required |
|----------|----------|------|------|-----------------|
| Normal text | {{N}} | {{N}} | {{N}} | {{N}} |
| Large text | {{N}} | {{N}} | {{N}} | {{N}} |
| UI components | {{N}} | {{N}} | {{N}} | {{N}} |
| Focus indicators | {{N}} | {{N}} | {{N}} | {{N}} |
| **Total** | **{{N}}** | **{{N}}** | **{{N}}** | **{{N}}** |

---

## Keyboard Navigation Audit (KB-001 through KB-005)

Keyboard-only operability assessment including focus order, focus visibility, keyboard traps, and shortcut key conflicts.

> **Methodology:** WCAG 2.2 Guideline 2.1 (Keyboard Accessible) and Guideline 2.4 (Navigable). (inclusive-design-rules.md [Keyboard Navigation Test Protocol])

### Keyboard Test Results

| Test | WCAG Criterion | Level | Status | Details |
|------|---------------|-------|--------|---------|
| Tab order completeness | 2.1.1 | A | {{PASS / FAIL}} | {{specific findings: unreachable elements, illogical order}} |
| Focus visibility | 2.4.7 (AA), 2.4.11 (AA) | AA | {{PASS / FAIL}} | {{specific findings: missing or insufficient focus indicators}} |
| No keyboard traps | 2.1.2 | A | {{PASS / FAIL}} | {{specific findings: components that trap focus}} |
| Shortcut conflicts | 2.1.4 | A | {{PASS / FAIL}} | {{specific findings: single-character shortcuts that cannot be remapped}} |
| Skip navigation | 2.4.1 | A | {{PASS / FAIL}} | {{specific findings: skip-to-content mechanism presence}} |
| Focus not obscured | 2.4.12 (AA, new in 2.2) | AA | {{PASS / FAIL}} | {{specific findings: focused elements hidden by sticky headers, modals}} |

### Keyboard Navigation Issues

<!-- Include this section only when FAIL findings exist -->

<!-- REPEATABLE BLOCK: KEYBOARD ISSUE START -->
#### KB-{{NNN}}: {{brief issue description}}

- **Affected Element:** {{specific element reference (KB-001)}}
- **Expected Behavior:** {{what should happen when the element receives keyboard focus or interaction}}
- **Observed Behavior:** {{what actually happens, or what is inferred from visual layout in degraded mode}}
- **WCAG Criterion:** {{SC X.Y.Z}}
- **Severity:** {{1-4}}
<!-- REPEATABLE BLOCK: KEYBOARD ISSUE END -->

<!-- In degraded mode, include: -->
<!-- "Structural assessment only; manual keyboard testing required" (KB-005) -->

---

## Screen Reader Compatibility (SR-001 through SR-005)

Semantic HTML structure, ARIA implementation, and assistive technology compatibility assessment.

> **Methodology:** WCAG 2.2 Principles 1 (Perceivable) and 4 (Robust). ARIA Authoring Practices Guide (APG) 1.2 (W3C, 2023). (inclusive-design-rules.md [Screen Reader Compatibility Test Protocol])

### Screen Reader Test Results

| Test | WCAG Criterion | Level | Status | Details |
|------|---------------|-------|--------|---------|
| Heading hierarchy | 1.3.1 | A | {{PASS / FAIL}} | {{findings: skipped levels, missing h1, logical structure}} |
| ARIA landmarks | 1.3.1, 4.1.2 | A | {{PASS / FAIL}} | {{findings: main, nav, banner, contentinfo presence and correctness}} |
| Alternative text | 1.1.1 | A | {{PASS / FAIL}} | {{findings: missing alt, non-descriptive alt, decorative image handling}} |
| Form labels | 1.3.1, 3.3.2 | A | {{PASS / FAIL}} | {{findings: unlabeled controls, label-input association}} |
| Live regions | 4.1.3 | AA | {{PASS / FAIL}} | {{findings: dynamic content announcement, ARIA live region usage}} |
| Error identification | 3.3.1 | A | {{PASS / FAIL}} | {{findings: error message association with invalid fields}} |

### Screen Reader Issues

<!-- Include this section only when FAIL findings exist -->

<!-- REPEATABLE BLOCK: SCREEN READER ISSUE START -->
#### SR-{{NNN}}: {{brief issue description}}

- **Affected Element:** {{specific element reference (SR-005)}}
- **Evidence:** {{specific observation from input artifacts}}
- **WCAG Criterion:** {{SC X.Y.Z}}
- **Severity:** {{1-4}}
- **Remediation:** {{specific fix with ARIA technique reference}}
<!-- REPEATABLE BLOCK: SCREEN READER ISSUE END -->

### Structural Assessment Limitation (P-022)

This screen reader compatibility assessment is structural (semantic HTML, ARIA implementation), not experiential. The evaluator assesses markup structure and ARIA usage from input artifacts but cannot simulate the actual screen reader experience across different assistive technology combinations (JAWS, NVDA, VoiceOver with different browsers). Validate findings with manual screen reader testing (SR-004).

---

## Cognitive Load Assessment (CG-001 through CG-005)

Information density, reading level, navigation consistency, error prevention, and input assistance evaluation.

> **Methodology:** WCAG 2.2 Principle 3 (Understandable). (inclusive-design-rules.md [Cognitive Load Assessment Protocol])

### Cognitive Load Test Results

| Test | WCAG Criterion | Level | Status | Details |
|------|---------------|-------|--------|---------|
| Reading level | 3.1.5 | AAA | {{PASS / FAIL / N/A}} | {{Flesch-Kincaid score if computable; otherwise AI-assessed reading level with MEDIUM confidence flag (CG-001, CG-002)}} |
| Consistent navigation | 3.2.3 | AA | {{PASS / FAIL}} | {{findings across pages/screens; or "Single-page assessment" if only one page provided (CG-003)}} |
| Error prevention | 3.3.4 (AA), 3.3.6 (AAA) | AA/AAA | {{PASS / FAIL}} | {{reversibility of submissions, confirmation dialogs for consequential actions (CG-004)}} |
| Input assistance | 3.3.2 (A), 3.3.3 (AA) | A/AA | {{PASS / FAIL}} | {{labels, instructions, suggestions for user input}} |
| Redundant entry | 3.3.7 (A, new in 2.2) | A | {{PASS / FAIL}} | {{auto-population of previously entered information}} |
| Consistent help | 3.2.6 (A, new in 2.2) | A | {{PASS / FAIL}} | {{help mechanism consistency across pages}} |

### Cognitive Load Issues

<!-- Include this section only when FAIL findings exist -->

<!-- REPEATABLE BLOCK: COGNITIVE LOAD ISSUE START -->
#### CL-{{NNN}}: {{brief issue description}}

- **Affected Element/Area:** {{specific area or content section}}
- **Evidence:** {{specific observation; for reading level: Flesch-Kincaid score or AI assessment notation}}
- **WCAG Criterion:** {{SC X.Y.Z}}
- **Severity:** {{1-4}}
- **Confidence:** {{HIGH / MEDIUM}} <!-- CG-005: cognitive load judgments are MEDIUM when based on AI assessment -->
<!-- REPEATABLE BLOCK: COGNITIVE LOAD ISSUE END -->

---

## Persona Spectrum Analysis (PS-010 through PS-014, ID-001 through ID-003)

> **Companion template:** Full standalone Persona Spectrum analysis: `skills/ux-inclusive-design/templates/persona-spectrum-template.md`. The profiles below are incorporated from that analysis.

Microsoft Inclusive Design Persona Spectrum profiles for each interaction pattern identified in the evaluated interface.

> **Methodology:** Microsoft Inclusive Design Toolkit (Microsoft, 2016). Three principles: Recognize Exclusion, Solve for One Extend to Many, Learn from Diversity. (inclusive-design-rules.md [Microsoft Inclusive Design Rules], [Persona Spectrum Methodology Rules])

<!-- REPEATABLE BLOCK: PERSONA SPECTRUM PROFILE START -->
### Persona Spectrum: {{INTERACTION_PATTERN_NAME}}

**Pattern ID:** INT-{{NNN}}
**Interaction:** {{description of the user task/action}}

| Disability Type | Permanent | Temporary | Situational |
|----------------|-----------|-----------|-------------|
| **Visual** | {{scenario}} | {{scenario}} | {{scenario}} |
| **Motor** | {{scenario}} | {{scenario}} | {{scenario}} |
| **Auditory** | {{scenario}} | {{scenario}} | {{scenario}} |
| **Cognitive** | {{scenario}} | {{scenario}} | {{scenario}} |

**Exclusion Points:** {{specific design decisions that create barriers}}
**Design Opportunity:** {{how solving for permanent extends to all}}
**Current Compliance:** {{WCAG success criteria relevant to this pattern}}
<!-- REPEATABLE BLOCK: PERSONA SPECTRUM PROFILE END -->

<!-- PS-010: Every interaction pattern MUST have a profile -->
<!-- PS-012: Every cell MUST be populated; use "Low exclusion risk for this combination: {reason}" when N/A -->
<!-- PS-013: Every profile MUST include Exclusion Points, Design Opportunity, Current Compliance -->

### Persona Spectrum Summary

| Pattern ID | Interaction Pattern | Exclusion Count | Most Critical Disability | Design Opportunity |
|-----------|-------------------|----------------|--------------------------|---------------------|
| INT-{{NNN}} | {{pattern name}} | {{N}} | {{disability type}} | {{one-line recommendation}} |
<!-- REPEATABLE ROW: One per interaction pattern -->

---

## Remediation Priorities (RP-001 through RP-005)

Prioritized remediation list ranked by: (1) severity descending, (2) conformance level ascending within severity, (3) estimated user impact (RP-001).

| Priority | WCAG Criterion | Severity | Affected Element | Remediation | Effort Estimate | Impact |
|----------|---------------|----------|-----------------|-------------|-----------------|--------|
| {{rank}} | SC {{X.Y.Z}} [{{Level}}] | {{1-4}} | {{element reference}} | {{specific fix with WCAG technique reference (RP-002)}} | {{Low / Medium / High}} (RP-003) | {{who benefits, persona reference when applicable (RP-004)}} |
<!-- REPEATABLE ROW: Copy row for each remediation item. -->
<!-- Order by severity descending (4 first), then level ascending (A first), then impact. -->
<!-- RP-005: Remediation priority ranking is MEDIUM synthesis confidence. -->

### Effort Estimate Key

| Estimate | Definition |
|----------|-----------|
| Low | < 1 day of engineering effort |
| Medium | 1-3 days of engineering effort |
| High | > 3 days of engineering effort |

---

## Strategic Implications

### Organizational Accessibility Maturity Assessment

<!-- Output format: 2-3 sentence assessment + one-sentence summary of highest-priority maturity gap. -->

{{Assess the organization's current accessibility maturity based on: WCAG conformance level achieved vs. target, severity distribution of findings, presence/absence of accessibility infrastructure (automated testing, manual testing processes, accessibility design guidelines), and the ratio of critical (severity 4) to cosmetic (severity 1) findings. Example: "The product achieves partial Level A conformance with 3 Level A failures remaining. The concentration of severity 3-4 findings in Perceivable and Operable principles suggests foundational accessibility practices are not yet established."}}

### Legal Compliance Gap Analysis

> **Legal frameworks:** US DOJ (2024). "Guidance on Web Accessibility and the ADA" (ADA Title III); European Parliament (2019). Directive (EU) 2019/882 -- European Accessibility Act (EAA); Section 508, 29 U.S.C. 794d.

{{Analyze the gap between current conformance level and applicable legal requirements (ADA Title III, EAA, Section 508). Reference the specific legal frameworks relevant to the product's jurisdiction and market. Example: "The European Accessibility Act (EAA, effective June 2025) requires WCAG 2.1 AA conformance for digital products sold in the EU. Current Level A failures in keyboard navigation (SC 2.1.1) and form labeling (SC 1.3.1) represent non-compliance with both EAA and ADA Title III expectations."}}

### Accessibility Debt Quantification

{{Quantify the accumulated accessibility barriers as a remediation backlog. Summarize: total findings by severity, estimated total remediation effort, and recommended sprint allocation. Example: "Accessibility debt: 2 critical (severity 4, ~2 days each), 5 major (severity 3, ~1-3 days each), 8 minor (severity 2, ~0.5 days each). Estimated total remediation: 15-25 engineering days. Recommended: allocate 20% of next 3 sprints to accessibility remediation, prioritizing severity 4 items first."}}

### Inclusive Design Adoption Roadmap

{{Recommend a phased approach for improving accessibility practices. Include: immediate fixes (severity 4), short-term improvements (severity 3), medium-term process changes (accessibility testing integration, design system updates), and long-term cultural changes (accessibility training, disability inclusion). Reference the Persona Spectrum analysis to frame the roadmap in terms of who benefits at each phase.}}

### Cross-Product Accessibility Pattern Analysis

{{Optional: When multiple engagements have been conducted, identify recurring accessibility patterns across products. Example: "Color contrast failures appear in 3 of 4 evaluated products, suggesting a systematic gap in the design system's color palette. Keyboard trap findings appear in all modal dialog implementations, suggesting a shared component library issue."}}

---

## Synthesis Judgments Summary (SD-004, PS-014, CG-005, RP-005)

<!-- Required: document every AI-generated judgment (severity assignment, Persona Spectrum scenario mapping, remediation priority ranking, cognitive load assessment, reading level evaluation) with a confidence classification and rationale. -->

Each AI judgment call made during this evaluation is listed below for synthesis confidence gate compliance per `skills/user-experience/rules/synthesis-validation.md` [Confidence Classification].

| # | Judgment Type | Decision | Rationale | Confidence |
|---|--------------|----------|-----------|------------|
| 1 | Severity assignment | {{e.g., "SC 1.4.3 rated severity 3 vs. 2"}} | {{evidence supporting severity level selection}} | {{HIGH / MEDIUM / LOW}} |
| 2 | Persona Spectrum mapping | {{e.g., "Motor-Situational scenario for INT-001"}} | {{why this scenario was selected as representative}} | {{HIGH / MEDIUM / LOW}} |
| 3 | Remediation priority | {{e.g., "SC 2.1.1 ranked above SC 1.1.1"}} | {{severity and conformance level ranking rationale}} | {{HIGH / MEDIUM / LOW}} |
| 4 | Cognitive load assessment | {{e.g., "Reading level assessed at grade 10 vs. grade 8"}} | {{Flesch-Kincaid computation or AI assessment basis}} | {{HIGH / MEDIUM / LOW}} |
| 5 | Conformance determination | {{e.g., "Achieved Level A vs. None"}} | {{aggregate criterion results supporting determination}} | {{HIGH / MEDIUM / LOW}} |
<!-- REPEATABLE ROW: Add one row per AI judgment call. At minimum, one judgment per category present in the evaluation. -->

**Confidence classification:**
- **HIGH:** Deterministic WCAG pass/fail based on measurable criteria; or convergent evidence from multiple frameworks. Proceed with finding.
- **MEDIUM:** AI judgment about user impact, persona scenarios, severity levels, or reading levels; single-framework reasoning. Include "Validation Required" note; withhold definitive recommendation.
- **LOW:** Insufficient input data; cannot evaluate due to missing artifacts or degraded mode limitations. Flag for human review; do not make compliance claims.

---

## Limitations and Reliability (LM-001)

### Single-Evaluator Disclosure (P-022)

Full WCAG 2.2 compliance testing requires manual testing with assistive technologies (screen readers, switch devices, voice control), automated testing tools (axe-core, Lighthouse, WAVE), and user testing with people who have disabilities. This evaluation was conducted by a **single AI evaluator**.

**Compensating factors:**
- Systematic dual-framework coverage (WCAG 2.2 POUR + Microsoft Inclusive Design Persona Spectrum) eliminates the ad-hoc approach that causes tiny teams to miss systematic accessibility barriers
- Every POUR principle is evaluated, every testing protocol is applied, and every interaction pattern is mapped through the full Persona Spectrum
- Findings are evidence-based with per-criterion WCAG references

**Residual limitations:**
- Cannot replicate comprehensive manual assistive technology testing
- Cannot simulate the actual screen reader experience across different AT combinations
- Color contrast ratios in screenshot-input mode require user-provided hex/RGB values for precision
- Persona Spectrum profiles are heuristic models, not empirically grounded user research
- AI-assigned severity levels involve judgment and carry MEDIUM confidence

### Input Mode Limitations

<!-- If Figma MCP available, use this block: -->
<!-- Full Figma design inspection available. No mode-specific limitations. -->

<!-- If degraded mode, use this block: -->
**[DEGRADED MODE]** This output was produced without Figma MCP access. Input was provided via screenshot-input mode. The following features are reduced:

- Cannot inspect design layers or component hierarchy programmatically
- Cannot extract exact color values for automated contrast ratio computation
- Cannot evaluate interactive states (animations, transitions, dynamic content)
- Cannot access design token definitions or systematic color palette information

<!-- Delete whichever block above does not apply. -->

### Recommendation for High-Severity Findings

For severity 3-4 findings (major barriers and access blockers):
- Supplement AI evaluation with automated scanning tools (axe-core, Lighthouse, WAVE) for code-level validation
- Conduct manual testing with screen readers (JAWS, NVDA, VoiceOver), keyboard-only navigation, and voice control
- Where possible, conduct user testing with people who have disabilities to validate severity assignments and remediation effectiveness

---

## Self-Review Checklist

Before persisting the report, verify all items below (S-010):

- [ ] 1. All four POUR principles have been evaluated with per-criterion pass/fail status (PR-001, PS-001)
- [ ] 2. The conformance level result is correctly determined -- all criteria at that level PASS (CD-001 through CD-005)
- [ ] 3. Every color contrast element has foreground/background values and computed ratios, or is flagged for manual measurement in degraded mode (CC-001, CC-003, CC-004)
- [ ] 4. Every keyboard navigation issue has the affected element, expected behavior, observed behavior, and WCAG criterion (KB-001)
- [ ] 5. Every screen reader finding has evidence and WCAG criterion reference (SR-005)
- [ ] 6. Every interaction pattern has a complete Persona Spectrum profile with all 12 cells populated (PS-012)
- [ ] 7. Every FAIL finding has a severity rating of 1-4; every PASS finding has severity 0 (SD-001, SD-002)
- [ ] 8. Every remediation recommendation references a WCAG technique (RP-002)
- [ ] 9. The Synthesis Judgments Summary lists each AI judgment call with confidence classification (SD-004, PS-014, CG-005, RP-005)
- [ ] 10. The navigation table is present and all anchors resolve (H-23)
- [ ] 11. Degraded mode disclosure is present if Figma MCP was unavailable (P-022)
- [ ] 12. Remediation priorities are ranked by severity descending, then conformance level ascending (RP-001)
- [ ] 13. Handoff data includes only findings with severity >= 2 (handoff threshold)
- [ ] 14. The executive summary states the achieved conformance level and critical violation count (CD-004, CD-005)
- [ ] 15. Screen reader structural assessment limitation is disclosed (SR-004)
- [ ] 16. PASS criteria have severity 0; FAIL criteria have severity 1-4 (no contradictions)

---

## Handoff Data

Structured data for downstream sub-skill and cross-framework synthesis consumption. Only findings with severity >= 2 (minor barrier or above) are included in handoff data per the cross-framework handoff threshold.

### Findings for Downstream Consumption

| Finding ID | WCAG Criterion | Principle | Severity | Remediation | Persona Spectrum Impact |
|-----------|---------------|-----------|----------|-------------|------------------------|
| {{ID}} | SC {{X.Y.Z}} | {{P / O / U / R}} | {{2-4}} | {{recommendation with technique reference}} | {{which persona scenarios affected, e.g., "Visual-Permanent, Visual-Situational, Motor-Temporary"}} |
<!-- REPEATABLE ROW: Copy row for each finding with severity >= 2. -->
<!-- Severity 0 and 1 findings are excluded from handoff data. -->

### Handoff YAML

```yaml
# Structured handoff for ux-orchestrator and downstream sub-skills
# Fields marked [handoff-v2] follow docs/schemas/handoff-v2.schema.json
# Fields marked [ux-ext] are ux-inclusive-design sub-skill extensions

# --- handoff-v2 schema fields ---
from_agent: ux-inclusive-evaluator                    # [handoff-v2] required
to_agent: ux-orchestrator                             # [handoff-v2] required
task: "Inclusive design evaluation for {{TOPIC}}"       # [handoff-v2] required
success_criteria:                                     # [handoff-v2] required, min 1
  - "All four POUR principles evaluated with per-criterion pass/fail"
  - "Conformance level correctly determined"
  - "Color contrast ratios computed with hex/RGB values"
  - "Persona Spectrum profiles complete for all interaction patterns"
  - "Remediation priorities ranked with WCAG technique references"
artifacts:                                            # [handoff-v2] required
  - "projects/${JERRY_PROJECT}/engagements/{{ENGAGEMENT_ID}}/ux-inclusive-evaluator-{{TOPIC_SLUG}}.md"
key_findings:                                         # [handoff-v2] required, 3-5 entries per CB-04
  - "{{top finding 1 summary}}"
  - "{{top finding 2 summary}}"
  - "{{top finding 3 summary}}"
blockers: []                                          # [handoff-v2] required
confidence: {{0.0-1.0}}                                # [handoff-v2] required
criticality: {{C1 / C2 / C3 / C4}}                     # [handoff-v2] required

# --- ux-inclusive-design extension fields ---
engagement_id: {{ENGAGEMENT_ID}}                        # [ux-ext] UX-{{NNNN}} format
target_conformance_level: {{A / AA / AAA}}              # [ux-ext]
conformance_result:                                   # [ux-ext]
  achieved_level: {{A / AA / AAA / none}}
  perceivable: {{PASS / FAIL}}
  operable: {{PASS / FAIL}}
  understandable: {{PASS / FAIL}}
  robust: {{PASS / FAIL}}
total_criteria_evaluated: {{N}}                         # [ux-ext]
criteria_passed: {{N}}                                  # [ux-ext]
criteria_failed: {{N}}                                  # [ux-ext]
criteria_not_applicable: {{N}}                          # [ux-ext]
critical_violations: {{N}}                              # [ux-ext] severity 4
major_violations: {{N}}                                 # [ux-ext] severity 3
persona_spectrums_produced: {{N}}                       # [ux-ext]
interaction_patterns_evaluated: {{N}}                   # [ux-ext]
degraded_mode: {{true / false}}                         # [ux-ext]
artifact_path: "projects/${JERRY_PROJECT}/engagements/{{ENGAGEMENT_ID}}/ux-inclusive-evaluator-{{TOPIC_SLUG}}.md"  # [ux-ext]
synthesis_judgments_count: {{N}}                         # [ux-ext]
```

---

<!-- GOVERNANCE ID INDEX: EV-001 through EV-005 (workflow sequencing), PR-001 through PR-003 (principle evaluation), PS-001 through PS-003 (principle scope), SC-001 through SC-006 (criterion format), SD-001 through SD-004 (severity-decision), CC-001 through CC-005 (color contrast), KB-001 through KB-005 (keyboard navigation), SR-001 through SR-005 (screen reader), CG-001 through CG-005 (cognitive load), CD-001 through CD-005 (conformance determination), RP-001 through RP-005 (remediation priority), ID-001 through ID-003 (inclusive design), PS-010 through PS-014 (persona spectrum), LM-001 (limitations disclosure) -->

*Template Version: 1.1.0 | /ux-inclusive-design Sub-Skill | PROJ-022 User Experience Skill*
*Source: SKILL.md [Output Specification], agent <output> section, agent <methodology> section*
*WCAG 2.2: W3C (2023). Web Content Accessibility Guidelines (WCAG) 2.2. W3C Recommendation.*
*Microsoft Inclusive Design: Microsoft Corporation (2016). Microsoft Inclusive Design Toolkit.*
*Nielsen severity scale: Nielsen, J. (1994b). Severity ratings for usability problems. In "Usability Inspection Methods", pp. 413-414. John Wiley & Sons.*
*ARIA APG: W3C (2023). ARIA Authoring Practices Guide (APG) 1.2. W3C Group Note.*
*Methodology rules: `skills/ux-inclusive-design/rules/inclusive-design-rules.md` (EV, PR, PS, SC, SD, ID, CC, KB, SR, CG, CD, RP rule families)*
*Handoff schema: `docs/schemas/handoff-v2.schema.json` (JSON Schema Draft 2020-12)*
*ORCHESTRATION: projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml*
