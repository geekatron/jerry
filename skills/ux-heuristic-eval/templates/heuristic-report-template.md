<!-- TEMPLATE: heuristic-report-template.md | VERSION: 1.9.0 | DATE: 2026-03-04 | REVISION: Add LOW confidence classification to Synthesis Judgments section per synthesis-validation.md Gate Definitions -->
<!-- SKILL: /ux-heuristic-eval | AGENT: ux-heuristic-evaluator -->
<!-- SOURCE: SKILL.md [Output Specification], agent <output> section, heuristic-evaluation-rules.md [Report Structure] -->
<!-- USAGE: Fill {{PLACEHOLDER}} fields. Copy REPEATABLE BLOCK markers for each finding. -->

# Heuristic Evaluation: {{TOPIC}}

> **Engagement:** {{ENGAGEMENT_ID}}
> **Product:** {{PRODUCT_NAME}}
> **Date:** {{EVALUATION_DATE}}
> **Evaluator:** {{EVALUATOR}}

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | L0: Top findings, severity distribution, overall assessment |
| [Evaluation Context](#evaluation-context) | L1: Product, target users, screens, input modality, MCP status, evaluation scope |
| [Methodology](#methodology) | Non-fill-in prose: evaluation workflow and AI supplement conditions |
| [Findings by Heuristic](#findings-by-heuristic) | L1: All findings organized by heuristic (H1-H10, AI-1/AI-2/AI-3) |
| [Heuristic Coverage Matrix](#heuristic-coverage-matrix) | H1-H10 + AI supplements vs. screens evaluated |
| [Ranked Findings Summary](#ranked-findings-summary) | L1: All findings in a single table ranked by severity descending |
| [Remediation Roadmap](#remediation-roadmap) | L1: Priority-ordered remediation actions grouped by effort |
| [Synthesis Judgments Summary](#synthesis-judgments-summary) | L1: AI judgment calls for synthesis gate compliance |
| [Strategic Implications](#strategic-implications) | L2: Cross-product usability patterns, organizational UX maturity |
| [Limitations and Reliability](#limitations-and-reliability) | L2: Single-evaluator disclosure, mode limitations |
| [Self-Review Checklist](#self-review-checklist) | S-010: Pre-persistence verification checklist |
| [Handoff Data](#handoff-data) | Structured data for downstream sub-skill consumption |

---

## Executive Summary

**Severity Distribution:**

| Severity | Name | Count |
|----------|------|-------|
| 4 | Usability catastrophe | {{COUNT_SEV4}} |
| 3 | Major usability problem | {{COUNT_SEV3}} |
| 2 | Minor usability problem | {{COUNT_SEV2}} |
| 1 | Cosmetic problem only | {{COUNT_SEV1}} |
| 0 | Not a usability problem | {{COUNT_SEV0}} |
| **Total** | | **{{TOTAL_FINDINGS}}** |

**Critical Findings (Severity 3-4):** {{CRITICAL_COUNT}} findings require immediate attention.

**Top Findings:**

1. **F-{{NNN}}:** {{one-line description}} (Severity {{N}}, {{heuristic}})
2. **F-{{NNN}}:** {{one-line description}} (Severity {{N}}, {{heuristic}})
3. **F-{{NNN}}:** {{one-line description}} (Severity {{N}}, {{heuristic}})
<!-- Add up to 5 top findings by severity -->

**Overall Usability Assessment:**

{{One paragraph covering: (1) key strengths observed, (2) critical weaknesses identified, (3) overall release readiness assessment. All three elements required.}}

**Heuristic Coverage Confirmation:** All {{HEURISTIC_COUNT}} heuristics evaluated across {{SCREEN_COUNT}} screens.

---

## Evaluation Context

**Product:** {{PRODUCT_NAME}}
**Domain:** {{PRODUCT_DOMAIN}}
**Target Users:** {{TARGET_USER_DESCRIPTION}}

**Screens/Flows Evaluated:**

| # | Screen/Flow | Description |
|---|-------------|-------------|
| 1 | {{screen_name}} | {{brief description of what this screen presents}} |
| 2 | {{screen_name}} | {{brief description}} |
<!-- Add one row per screen or flow step evaluated -->

**Input Modality:** {{Figma MCP | screenshot-input | text description}}
**MCP Status:** {{Figma available | DEGRADED MODE -- screenshot-input}}
**Evaluation Scope:** {{screen-level | flow-level}}

<!-- Include this block ONLY in degraded mode -->
<!-- [DEGRADED MODE] This evaluation was produced without Figma MCP access.
     Input was provided via screenshot-input mode. Some features are reduced:
     - Cannot inspect component states or interactive behaviors
     - Cannot verify responsive behavior across breakpoints
     - Cannot access style tokens or design system variables programmatically -->

---

## Methodology

<!-- Do not modify this section -- describes the standard methodology applied to every evaluation. -->

This evaluation applies Nielsen's 10 usability heuristics (H1 through H10) systematically to every screen under review. Each heuristic is evaluated independently per screen to ensure complete coverage. Findings are documented using Nielsen's 0-4 severity scale: 0 (not a usability problem), 1 (cosmetic), 2 (minor), 3 (major), 4 (catastrophe). The evaluation process follows the workflow defined in `heuristic-evaluation-rules.md` [Evaluation Workflow]: (1) systematic per-screen heuristic application, (2) finding documentation with specific evidence, (3) deduplication of same-root-cause violations, (4) severity ranking and Finding ID assignment.

When the AI Product Flag is enabled, three supplementary heuristics (AI-1: Transparency, AI-2: Controllability, AI-3: Error Recovery) are applied in addition to H1-H10. These supplements synthesize principles from Amershi et al. (2019) and Google PAIR (2019) and are NOT published extensions of Nielsen's original framework (P-022 disclosure).

All fill-in fields for evaluation scope, screens, input modality, and MCP status are captured in the [Evaluation Context](#evaluation-context) section above.

---

## Findings by Heuristic

Findings are organized by heuristic (H1 through H10, then AI-1 through AI-3 if applicable), per `heuristic-evaluation-rules.md` [Report Structure] section 4. Within each heuristic section, findings are ordered by severity (highest first). Heuristics with no findings are noted as "No violations identified."

<!-- DEDUPLICATION CHECK: Before populating findings, consolidate same-root-cause violations per heuristic-evaluation-rules.md [Deduplication Rules]. -->
<!-- IMPORTANT: Assign F-{NNN} IDs only after all findings are ranked by severity (Step 4 of evaluation workflow). Do not assign IDs as you document findings. -->

### H1: Visibility of System Status

<!-- H1 checkpoints: action feedback, loading/progress states, completion confirmation, state change visibility, current location indicator -->

<!-- If no H1 findings: -->
<!-- No violations identified for H1. -->

<!-- REPEATABLE BLOCK: FINDING START -->
#### Finding F-{{NNN}}: {{brief description}}

- **Heuristic:** H1 -- Visibility of System Status
- **Severity:** {{0-4}} ({{Nielsen severity name}})
- **Screen/Flow:** {{affected screen or user flow}}
- **Evidence:** {{specific interface observation demonstrating the violation}}
<!-- For acceptable vs. unacceptable evidence examples, see heuristic-evaluation-rules.md [Evidence Quality Standard]. Evidence should include specific UI element references, not vague descriptions.
     Acceptable: "The 'Save' button produces no visual feedback after click -- no spinner, no confirmation toast, no state change."
     Acceptable: "The error message reads 'Error 422' with no plain-language explanation or recovery suggestion."
     Acceptable: "The settings page uses 'Provisioning Cadence' while the dashboard uses 'Update Schedule' for the same feature."
     Unacceptable: "The form feels confusing" (unacceptable -- subjective, no interface element reference).
     Unacceptable: "Users probably struggle here" (unacceptable -- speculative claim, no observed behavior or interface element reference).
     Unacceptable: "This violates H1" (unacceptable -- circular, restates the heuristic without citing a specific interface element or behavior). -->
- **Remediation:** {{actionable fix recommendation}}
- **Effort:** {{Low | Medium | High}}
<!-- REPEATABLE BLOCK: FINDING END -->

---

### H2: Match Between System and Real World

<!-- H2 checkpoints: user-appropriate terminology, real-world icon conventions, logical information order, locale-appropriate formats -->

<!-- If no H2 findings: -->
<!-- No violations identified for H2. -->

<!-- Repeat FINDING blocks as needed -->

---

### H3: User Control and Freedom

<!-- H3 checkpoints: undo/redo, cancel in-progress operations, back navigation without data loss, destructive action confirmation -->

<!-- If no H3 findings: -->
<!-- No violations identified for H3. -->

<!-- Repeat FINDING blocks as needed -->

---

### H4: Consistency and Standards

<!-- H4 checkpoints: consistent element styling/position, platform conventions, consistent terminology, consistent interactive behavior, established visual hierarchy -->

<!-- If no H4 findings: -->
<!-- No violations identified for H4. -->

<!-- Repeat FINDING blocks as needed -->

---

### H5: Error Prevention

<!-- H5 checkpoints: input constraints, confirmation before irreversible actions, sensible defaults, real-time validation, dangerous action visual distinction -->

<!-- If no H5 findings: -->
<!-- No violations identified for H5. -->

<!-- Repeat FINDING blocks as needed -->

---

### H6: Recognition Rather Than Recall

<!-- H6 checkpoints: visible options, contextual help available, recent items/autocomplete, no cross-screen recall required -->

<!-- If no H6 findings: -->
<!-- No violations identified for H6. -->

<!-- Repeat FINDING blocks as needed -->

---

### H7: Flexibility and Efficiency of Use

<!-- H7 checkpoints: keyboard shortcuts, bypass introductory steps, customization/personalization, bulk action accelerators -->

<!-- If no H7 findings: -->
<!-- No violations identified for H7. -->

<!-- Repeat FINDING blocks as needed -->

---

### H8: Aesthetic and Minimalist Design

<!-- H8 checkpoints: essential info priority, minimal visual clutter, rarely-needed options hidden, signal-to-noise ratio -->

<!-- If no H8 findings: -->
<!-- No violations identified for H8. -->

<!-- Repeat FINDING blocks as needed -->

---

### H9: Help Users Recognize, Diagnose, and Recover from Errors

<!-- H9 checkpoints: plain language errors, precise problem identification, recovery suggestions, error proximity to input, visually distinct error states -->

<!-- If no H9 findings: -->
<!-- No violations identified for H9. -->

<!-- Repeat FINDING blocks as needed -->

---

### H10: Help and Documentation

<!-- H10 checkpoints: contextual help at decision points, searchable task-oriented docs, help without leaving workflow, onboarding/tooltips -->

<!-- If no H10 findings: -->
<!-- No violations identified for H10. -->

<!-- Repeat FINDING blocks as needed -->

---

<!-- Include AI supplement heuristic sections ONLY when AI Product Flag = true -->
<!-- ### AI-1: Transparency [AI-SUPPLEMENT] -->
<!-- AI-1 checkpoints: AI decision disclosure, confidence/uncertainty indicators, explainability of AI output, AI vs human content boundary -->
<!-- If no AI-1 findings: -->
<!-- No violations identified for AI-1. -->
<!-- Repeat FINDING blocks as needed -->

<!-- ### AI-2: Controllability [AI-SUPPLEMENT] -->
<!-- AI-2 checkpoints: override/dismiss suggestions, correct AI mistakes with feedback, adjust AI sensitivity/scope, disable AI features -->
<!-- If no AI-2 findings: -->
<!-- No violations identified for AI-2. -->
<!-- Repeat FINDING blocks as needed -->

<!-- ### AI-3: Error Recovery [AI-SUPPLEMENT] -->
<!-- AI-3 checkpoints: undo AI-initiated actions, report/flag AI errors, graceful low-confidence degradation, revert to non-AI workflow -->
<!-- If no AI-3 findings: -->
<!-- No violations identified for AI-3. -->
<!-- Repeat FINDING blocks as needed -->

---

## Heuristic Coverage Matrix

Each cell shows the count of findings for that heuristic on that screen. A dash (--) indicates the heuristic was evaluated with no violations found.

<!-- Coverage Matrix format: template-defined extension. Section purpose aligns with heuristic-evaluation-rules.md [Self-Review Checklist (S-010)] item 1: "All 10 Nielsen heuristics evaluated." AI supplement rows (AI-1, AI-2, AI-3) are conditional on AI Product Flag = true in Evaluation Context. -->

> **Column count:** Add or remove screen columns to match the actual screen count for this evaluation. Minimum 1 screen column required.

| Heuristic | {{Screen_1}} | {{Screen_2}} | {{Screen_3}} | Total |
|-----------|:---:|:---:|:---:|:---:|
| H1: Visibility of System Status | {{N or --}} | {{N or --}} | {{N or --}} | {{N}} |
| H2: Match Between System and Real World | {{N or --}} | {{N or --}} | {{N or --}} | {{N}} |
| H3: User Control and Freedom | {{N or --}} | {{N or --}} | {{N or --}} | {{N}} |
| H4: Consistency and Standards | {{N or --}} | {{N or --}} | {{N or --}} | {{N}} |
| H5: Error Prevention | {{N or --}} | {{N or --}} | {{N or --}} | {{N}} |
| H6: Recognition Rather Than Recall | {{N or --}} | {{N or --}} | {{N or --}} | {{N}} |
| H7: Flexibility and Efficiency of Use | {{N or --}} | {{N or --}} | {{N or --}} | {{N}} |
| H8: Aesthetic and Minimalist Design | {{N or --}} | {{N or --}} | {{N or --}} | {{N}} |
| H9: Help Users Recognize, Diagnose, and Recover from Errors | {{N or --}} | {{N or --}} | {{N or --}} | {{N}} |
| H10: Help and Documentation | {{N or --}} | {{N or --}} | {{N or --}} | {{N}} |
<!-- Include AI supplement rows ONLY when AI Product Flag = true -->
<!-- | AI-1: Transparency [AI-SUPPLEMENT] | {{N or --}} | {{N or --}} | {{N or --}} | {{N}} | -->
<!-- | AI-2: Controllability [AI-SUPPLEMENT] | {{N or --}} | {{N or --}} | {{N or --}} | {{N}} | -->
<!-- | AI-3: Error Recovery [AI-SUPPLEMENT] | {{N or --}} | {{N or --}} | {{N or --}} | {{N}} | -->
| **Total per screen** | {{N}} | {{N}} | {{N}} | **{{TOTAL_FINDINGS}}** |

**Coverage note:** {{Flag any heuristic with zero findings across all screens. If 3+ heuristics have zero findings, note as a potential systematic blind spot per heuristic-evaluation-rules.md [Single-Evaluator Reliability].}}

---

## Ranked Findings Summary

All findings ranked by severity descending. Within the same severity, ordered by number of affected screens (most first).

| Finding ID | Heuristic | Severity | Screen/Flow | Brief Description | Effort |
|-----------|-----------|----------|-------------|-------------------|--------|
| F-{{NNN}} | H{{N}} | {{0-4}} | {{screen}} | {{one-line description}} | {{Low / Medium / High}} |
<!-- Repeat rows for each finding, ranked by severity descending -->

---

## Remediation Roadmap

Priority-ordered remediation actions grouped by effort level. Within each group, findings are ordered by severity (highest first).

### Quick Wins (Low Effort)

| Priority | Finding | Severity | Recommendation |
|----------|---------|----------|----------------|
| 1 | F-{{NNN}} | {{0-4}} | {{actionable fix}} |
<!-- Repeat rows as needed -->

### Medium Effort

| Priority | Finding | Severity | Recommendation |
|----------|---------|----------|----------------|
| {{N}} | F-{{NNN}} | {{0-4}} | {{actionable fix}} |
<!-- Repeat rows as needed -->

### High Effort

| Priority | Finding | Severity | Recommendation |
|----------|---------|----------|----------------|
| {{N}} | F-{{NNN}} | {{0-4}} | {{actionable fix}} |
<!-- Repeat rows as needed -->

**Suggested Implementation Order:** {{Brief paragraph describing the recommended sequence -- typically severity 4 first regardless of effort, then quick wins for momentum, then medium/high effort items by severity.}}

---

## Synthesis Judgments Summary

<!-- Required: document at minimum one judgment per category present in the evaluation (severity calibration, deduplication, effort estimation, AI-supplement applicability, cross-heuristic pattern grouping). -->

Each AI judgment call made during this evaluation is listed below for synthesis confidence gate compliance per `skills/user-experience/rules/synthesis-validation.md` [Confidence Classification].

| # | Judgment Type | Decision | Rationale | Confidence |
|---|--------------|----------|-----------|------------|
| 1 | Severity calibration | {{e.g., "F-003 rated severity 3 vs. 2"}} | {{why this rating was chosen over the alternative}} | {{HIGH | MEDIUM}} |
| 2 | Deduplication | {{e.g., "F-005 and F-008 consolidated"}} | {{same root cause, same remediation}} | {{HIGH | MEDIUM}} |
| 3 | Effort estimate | {{e.g., "F-002 rated High effort"}} | {{requires design system changes across multiple components}} | {{HIGH | MEDIUM}} |
| 4 | AI-supplement applicability | {{e.g., "F-010 classified under AI-2 vs. H3"}} | {{Describe decision to include/exclude AI-supplement heuristic and basis for applicability assessment}} | {{HIGH | MEDIUM}} |
| 5 | Cross-heuristic pattern grouping | {{e.g., "F-004, F-007, F-011 grouped as systemic feedback pattern"}} | {{Describe how related findings across multiple heuristics were grouped and rationale for the pattern}} | {{HIGH | MEDIUM}} |
<!-- Repeat rows for each judgment call -->

**Confidence classification:**
- **HIGH:** Based on systematic checklist with observable evidence; acknowledgment required before design recommendations are generated.
- **MEDIUM:** Involves subjective calibration across heuristics; validation against real user data or expert review recommended before acting on design recommendations.
- **LOW:** Single-framework finding with weak evidence, contradiction present, or AI inference without empirical grounding. LOW findings are permanently labeled reference-only; design recommendations structurally omitted.

---

## Strategic Implications

<!-- Required: identify at least one pattern per subsection. Minimum two sentences per subsection. -->

### Cross-Product Usability Patterns

{{Identify patterns that transcend individual findings -- systemic issues that suggest broader product or organizational themes. Examples: consistent lack of error prevention across all flows suggests missing design system error components; repeated H4 violations suggest absence of a centralized style guide.}}

### Organizational UX Maturity Observations

{{Based on the finding distribution and severity patterns, characterize the product team's UX maturity. Examples: high severity-3-4 count on core flows suggests UX is not integrated into the development process; low finding count with mostly severity 1-2 suggests mature UX practice with room for polish.}}

### Design Evolution Recommendations

{{Suggest strategic directions beyond individual finding remediation. Examples: invest in a design system to prevent H4 recurrence; establish usability testing cadence to catch H1/H9 issues earlier; consider accessibility audit to complement heuristic evaluation.}}

---

## Limitations and Reliability

### Single-Evaluator Disclosure (P-022)

Nielsen's methodology recommends 3-5 independent evaluators for reliable problem detection. Individual evaluators typically find only 35% of usability problems (Nielsen, 1994c). This evaluation was conducted by a **single AI evaluator**.

**Compensating factors:**
- Systematic sequential application of all {{HEURISTIC_COUNT}} heuristics to every screen -- no heuristic skipped
- Consistent severity calibration using the same 0-4 scale criteria across all findings
- Consistent evaluation depth across all {{SCREEN_COUNT}} screens

**Residual limitations:**
- No perspective diversity from multiple human evaluators
- Context-specific issues requiring domain expertise or cultural familiarity may be missed
- Issues discoverable only through live interaction (gesture feel, animation timing) cannot be evaluated from static inputs

### Input Modality Limitations

<!-- If Figma MCP: document any design tokens or prototype states not accessible. If screenshot-input: note inability to evaluate visual hierarchy or spacing precisely, and any heuristics affected per skills/ux-heuristic-eval/rules/mcp-runbook.md [Text-Description Caveats]. If text description: note all visual assessment limitations. -->
{{Describe any limitations specific to the input mode used for this evaluation.}}

<!-- Include for screenshot-input mode: -->
<!-- - Cannot inspect component states (hover, focus, active, disabled) -->
<!-- - Cannot verify responsive behavior across breakpoints -->
<!-- - Cannot access style tokens or design system variables -->

### Recommendation for High-Stakes Findings

For findings rated **severity 3 or 4**, supplement this evaluation with at least one human evaluator review before making major design decisions. This is especially important when:
- The product serves specialized user populations
- Findings will drive significant engineering investment (> 1 sprint)
- The evaluation was conducted in screenshot-input degraded mode

---

## Self-Review Checklist

Before persisting the report, verify all items below per `heuristic-evaluation-rules.md` [Self-Review Checklist (S-010)]:

- [ ] 1. All 10 heuristics were evaluated for every screen (no heuristic skipped)
- [ ] 2. Every finding has all required fields per [Finding Documentation Rules](skills/ux-heuristic-eval/rules/heuristic-evaluation-rules.md#finding-documentation-rules)
- [ ] 3. Every finding has specific interface evidence (not generic assertions)
- [ ] 4. Findings are deduplicated per [Deduplication Rules](skills/ux-heuristic-eval/rules/heuristic-evaluation-rules.md#deduplication-rules)
- [ ] 5. Findings are ranked by severity descending in the Ranked Findings Summary
- [ ] 6. The navigation table is present with correct anchor links (H-23)
- [ ] 7. Degraded mode disclosure is present if operating without Figma MCP
- [ ] 8. The Synthesis Judgments Summary lists each AI judgment call
- [ ] 9. Handoff Data includes only severity >= 2 findings
- [ ] 10. Finding IDs are sequential (`F-001`, `F-002`, ...) with no gaps

---

## Handoff Data

Structured data for downstream sub-skill consumption (Behavior Design, HEART Metrics). Only findings with **severity >= 2** are included per the cross-framework handoff threshold.

### Findings for Downstream Consumption

| Finding ID | Heuristic | Severity | Affected Screen | Candidate HEART Category |
|-----------|-----------|----------|-----------------|--------------------------|
| F-{{NNN}} | H{{N}} | {{2-4}} | {{screen}} | {{Happiness | Engagement | Adoption | Retention | Task success}} |
<!-- Repeat rows for each finding with severity >= 2 -->
<!-- See heuristic-evaluation-rules.md [Heuristic-to-HEART Category Mapping] for H1-H10 mappings. H6/H8/H9 are context-dependent: map to Happiness for satisfaction findings, Task Success for error/functional findings. -->

### Handoff YAML

```yaml
# Structured handoff for ux-orchestrator and downstream sub-skills
# Fields marked [handoff-v2] follow docs/schemas/handoff-v2.schema.json
# Fields marked [ux-ext] are ux-heuristic-eval sub-skill extensions

# --- handoff-v2 schema fields ---
from_agent: ux-heuristic-evaluator          # [handoff-v2] required
to_agent: ux-orchestrator                    # [handoff-v2] required
task: "Heuristic evaluation of {{TOPIC}}"    # [handoff-v2] required
success_criteria:                            # [handoff-v2] required, min 1
  - "All {{HEURISTIC_COUNT}} heuristics evaluated across {{SCREEN_COUNT}} screens"
  - "Every finding has severity rating with specific evidence"
  - "Findings deduplicated and ranked by severity"
artifacts:                                   # [handoff-v2] required
  - "projects/${JERRY_PROJECT}/engagements/{{ENGAGEMENT_ID}}/ux-heuristic-evaluator-{{TOPIC_SLUG}}.md"
key_findings:                                # [handoff-v2] required, 3-5 entries per CB-04
  - "{{top finding 1 summary}}"
  - "{{top finding 2 summary}}"
  - "{{top finding 3 summary}}"
blockers: []                                 # [handoff-v2] required
confidence: {{0.0-1.0}}                      # [handoff-v2] required
criticality: {{C1 | C2 | C3 | C4}}          # [handoff-v2] required

# --- ux-heuristic-eval extension fields ---
engagement_id: {{ENGAGEMENT_ID}}             # [ux-ext] UX-{NNNN} format
total_findings: {{TOTAL_FINDINGS}}           # [ux-ext]
severity_distribution:                       # [ux-ext]
  0: {{COUNT_SEV0}}
  1: {{COUNT_SEV1}}
  2: {{COUNT_SEV2}}
  3: {{COUNT_SEV3}}
  4: {{COUNT_SEV4}}
heuristics_evaluated: {{HEURISTIC_COUNT}}    # [ux-ext]
screens_evaluated: {{SCREEN_COUNT}}          # [ux-ext]
degraded_mode: {{true | false}}              # [ux-ext]
handoff_findings_count: {{count of severity >= 2 findings}}  # [ux-ext]
```

---

*Template Version: 1.9.0 | /ux-heuristic-eval Sub-Skill | PROJ-022 User Experience Skill*
*Source: SKILL.md [Output Specification], agent [output] section, heuristic-evaluation-rules.md [Report Structure]*
*Heuristic framework: Nielsen (1994a, 1994b, 1994c, 2020). AI supplements: Amershi et al. (2019), Google PAIR (2019).*
*HEART framework: Rodden, K., Hutchinson, H., & Fu, X. (2010). "Measuring the User Experience on a Large Scale: Quality-Related Factors in Web Search." CHI '10.*
*Handoff schema: `docs/schemas/handoff-v2.schema.json` (JSON Schema Draft 2020-12)*
*ORCHESTRATION: projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml*
