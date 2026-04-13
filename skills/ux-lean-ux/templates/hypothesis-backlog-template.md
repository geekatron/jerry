<!-- TEMPLATE: hypothesis-backlog-template.md | VERSION: 1.2.0 | DATE: 2026-03-04 | REVISION: iter3 — 4 missing HARD-rule checklist items (ASM-004, ASM-006, VLD-007, VLD-003), learning-documentation scope warning (BML-002), ICE 6-anchor scale alignment, ICE Score computed-value placeholder, sibling template cross-reference, synthesis-validation section anchor citation from iter2 score (0.923) -->
<!-- SKILL: /ux-lean-ux | AGENT: ux-lean-ux-facilitator -->
<!-- SOURCE: SKILL.md [Output Specification], agent <output> section, agent <methodology> section, lean-ux-methodology-rules.md -->
<!-- COMPANION: assumption-map-template.md — produces the standalone assumption map (Step 2 worksheet) that feeds this hypothesis backlog. See skills/ux-lean-ux/templates/assumption-map-template.md -->
<!-- USAGE: Fill {{PLACEHOLDER}} fields. Copy REPEATABLE BLOCK markers for each hypothesis, assumption, experiment, and learning entry. See lean-ux-methodology-rules.md for rule IDs governing each section. -->

# Lean UX Hypothesis Cycle: {{TOPIC}}

> **Engagement:** {{ENGAGEMENT_ID}}
> **Product:** {{PRODUCT_NAME}}
> **Date:** {{FACILITATION_DATE}}
> **Facilitator:** ux-lean-ux-facilitator
> **Cycle Scope:** {{CYCLE_SCOPE}}

<!-- Cycle scope values: full-cycle | hypothesis-generation | assumption-mapping | experiment-design | learning-documentation -->
<!-- When cycle scope is not full-cycle, omit sections that fall outside the executed phases. -->
<!-- IMPORTANT: When cycle_scope is learning-documentation, prior experiment results MUST be provided via input. Without them, Steps 4-5 MUST NOT produce learning entries (VLD-007, BML-002) -- fabricating experiment results violates P-022. BML-002 limits output to documentation synthesis only. -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | L0: Top hypotheses, risk assumptions, experiment recommendations |
| [Engagement Context](#engagement-context) | L1: Product, users, design change, prior research, MCP status |
| [Hypothesis Backlog](#hypothesis-backlog) | L1: Full backlog with Lean UX format, ICE scores, lifecycle status |
| [Assumption Map](#assumption-map) | L1: 4-quadrant mapping with rationale and movement tracking |
| [Experiment Designs](#experiment-designs) | L1: Per-hypothesis experiment design with success criteria |
| [Validated Learning Log](#validated-learning-log) | L1: Completed cycle outcomes with evidence and decisions |
| [Synthesis Judgments Summary](#synthesis-judgments-summary) | L1: AI judgment calls with confidence classification |
| [Strategic Implications](#strategic-implications) | L2: Organizational learning patterns, maturity assessment |
| [Limitations and Reliability](#limitations-and-reliability) | L2: Single-facilitator disclosure, mode limitations |
| [Self-Review Checklist](#self-review-checklist) | S-010: Pre-persistence verification checklist |
| [Handoff Data](#handoff-data) | Structured data for downstream sub-skill consumption |

---

## Executive Summary

**Hypothesis Backlog Summary:**

| Status | Count |
|--------|-------|
| DRAFT | {{COUNT_DRAFT}} |
| ACTIVE | {{COUNT_ACTIVE}} |
| VALIDATED | {{COUNT_VALIDATED}} |
| INVALIDATED | {{COUNT_INVALIDATED}} |
| DEFERRED | {{COUNT_DEFERRED}} |
| **Total** | **{{TOTAL_HYPOTHESES}}** |

**Cycle Completion Status:** {{TOTAL_HYPOTHESES}} hypotheses tracked across {{CYCLE_COUNT}} Build-Measure-Learn cycles.

**Hypothesis Validation Rate:** {{VALIDATION_RATE}}
<!-- Validation rate = VALIDATED / (VALIDATED + INVALIDATED). If no cycles completed, state "No cycles completed yet -- validation rate not available." -->

**Top Hypotheses:**

1. **HYP-{{NNN}}:** {{one-line hypothesis summary}} (ICE: {{SCORE}}, Status: {{STATUS}})
2. **HYP-{{NNN}}:** {{one-line hypothesis summary}} (ICE: {{SCORE}}, Status: {{STATUS}})
3. **HYP-{{NNN}}:** {{one-line hypothesis summary}} (ICE: {{SCORE}}, Status: {{STATUS}})
<!-- List up to 5 hypotheses ordered by ICE score descending -->

**Highest-Risk Assumptions (Q1 -- Unknown + High Risk):**

- {{ASM-NNN}}: {{one-line assumption description}}
- {{ASM-NNN}}: {{one-line assumption description}}
<!-- List all Q1 assumptions. If none, state: "No Q1 assumptions identified -- all critical unknowns have been addressed or deferred." -->

**Experiment Recommendations:**

{{One paragraph summarizing: (1) which hypotheses should be tested next, (2) recommended experiment types, (3) estimated timeline. Written for stakeholder consumption.}}

---

## Engagement Context

**Product:** {{PRODUCT_NAME}}
**Domain:** {{PRODUCT_DOMAIN}}
**Target Users:** {{TARGET_USER_DESCRIPTION}}
**Design Change Under Consideration:** {{DESIGN_CHANGE_DESCRIPTION}}

**Prior Research Inputs:**

| Source Sub-Skill | Artifact | Key Inputs Used |
|-----------------|----------|-----------------|
| {{sub-skill name or "None"}} | {{artifact path or "N/A"}} | {{what was extracted and used}} |
<!-- Include rows for: /ux-jtbd (job statements, switch forces), /ux-heuristic-eval (severity >= 2 findings), /ux-design-sprint (Day 4 findings, validated prototype). Remove rows with no upstream input. -->

**MCP Status:** {{Miro available | DEGRADED MODE -- text-based exercise}}
**Cycle Scope:** {{full-cycle | hypothesis-generation | assumption-mapping | experiment-design | learning-documentation}}

<!-- Include this block ONLY in degraded mode -->
<!-- [DEGRADED MODE] This output was produced without Miro MCP access.
     Input was provided via text-based exercise mode. Some features are reduced:
     - Cannot create or update collaborative visual boards
     - Cannot visualize assumption movement between quadrants over time
     - Cannot embed experiment results alongside visual hypothesis boards -->

---

## Hypothesis Backlog

<!-- IMPORTANT: Every hypothesis MUST follow the canonical Lean UX format (all 4 components: outcome, users, change, evidence). -->
<!-- ICE score = (Impact + Confidence + Ease) / 3. When uncertain between adjacent scores, choose the LOWER score (P-022). -->
<!-- Re-score after each Build-Measure-Learn cycle as evidence changes confidence levels. -->

| ID | Hypothesis (Lean UX Format) | Category | Status | I | C | E | ICE Score | Priority | Linked Experiment |
|----|---------------------------|----------|--------|---|---|---|-----------|----------|-------------------|
| HYP-{{NNN}} | We believe {{outcome}} for {{users}} if {{change}} because {{evidence}} | {{Value / Usability / Feasibility}} | {{DRAFT / ACTIVE / VALIDATED / INVALIDATED / DEFERRED}} | {{1-10}} | {{1-10}} | {{1-10}} | {{ICE_SCORE}} | {{rank}} | EXP-{{NNN}} or -- |
<!-- ICE Score: Computed as (I + C + E) / 3. Replace {{ICE_SCORE}} with the decimal result. Example: (8 + 6 + 4) / 3 = 6.00 -->
<!-- REPEATABLE ROW: Copy row above for each hypothesis. Order by ICE score descending. When ICE scores are tied, prefer the hypothesis in the higher-risk assumption quadrant (Q1 > Q2 > Q4 > Q3). -->

**ICE Scoring Scale Reference:**

> Full 6-anchor scales. Source: `skills/ux-lean-ux/rules/lean-ux-methodology-rules.md` [ICE Scoring Rules § Scale Anchors].

#### Impact (How many users are affected and how significantly?)

| Score | Anchor | Definition |
|-------|--------|------------|
| 1 | Minimal | Affects < 1% of users OR negligible behavior change |
| 2-3 | Low | Affects 1-10% of users with minor behavior change |
| 4-5 | Moderate | Affects ~25% of users with moderate behavior change |
| 6-7 | Significant | Affects ~50% of users with notable behavior change |
| 8-9 | High | Affects ~75% of users with significant behavior change |
| 10 | Transformative | Affects > 75% of users with fundamental behavior change |

#### Confidence (How much evidence supports this hypothesis?)

| Score | Anchor | Definition |
|-------|--------|------------|
| 1 | Gut feeling | No data, no analogies, no prior research; pure team intuition |
| 2-3 | Weak signal | Anecdotal evidence, single user complaint, informal observation |
| 4-5 | Indirect evidence | Analytics trends, competitor benchmarks, related heuristic findings, general UX principles |
| 6-7 | Moderate evidence | User research findings (interviews, surveys), heuristic evaluation severity >= 2 findings, JTBD job statements |
| 8-9 | Strong evidence | Prior Build-Measure-Learn cycle data, A/B test results from related experiments |
| 10 | Direct validation | Statistically significant A/B test data directly testing this hypothesis |

#### Ease (How quickly can we test this hypothesis?)

| Score | Anchor | Definition |
|-------|--------|------------|
| 1 | Very difficult | > 1 month of engineering/design effort to build the experiment |
| 2-3 | Difficult | 2-4 weeks effort; requires significant coordination or new infrastructure |
| 4-5 | Moderate | 1-2 weeks effort; requires moderate coordination |
| 6-7 | Easy | 3-5 days effort; uses existing tools with minor setup |
| 8-9 | Very easy | 1-2 days effort; uses existing tools directly |
| 10 | Trivial | < 1 day; can test with a simple survey or existing analytics |

---

## Assumption Map

<!-- Each assumption requires a quadrant placement with a one-line rationale. When uncertain between adjacent quadrants, place in the HIGHER-risk quadrant (P-022). -->

### 4-Quadrant Visualization

```
                    HIGH RISK
                       |
    +---------+--------+--------+---------+
    |         |                 |         |
    |  Q2:    |    Q1:          |         |
    |  Known  |    Unknown      |         |
    |  High   |    High Risk    |         |
    |  Risk   |    (TEST FIRST) |         |
    |         |                 |         |
KNOWN --------+--------+--------+-------- UNKNOWN
    |         |                 |         |
    |  Q3:    |    Q4:          |         |
    |  Known  |    Unknown      |         |
    |  Low    |    Low Risk     |         |
    |  Risk   |    (DEFER)      |         |
    |         |                 |         |
    +---------+--------+--------+---------+
                       |
                    LOW RISK
```

### Assumption Inventory

| ID | Assumption | Category | Quadrant | Rationale | Related Hypothesis | Movement |
|----|-----------|----------|----------|-----------|-------------------|----------|
| ASM-{{NNN}} | {{assumption text}} | {{Value / Usability / Feasibility}} | {{Q1 / Q2 / Q3 / Q4}} | {{one-line rationale for risk and knowledge assessment}} | HYP-{{NNN}} or -- | {{initial placement or "initial -> current" if changed}} |
<!-- REPEATABLE ROW: Copy row above for each assumption. Order by quadrant priority: Q1 first, then Q2, Q4, Q3. -->

### Quadrant Summary

| Quadrant | Name | Count | Action |
|----------|------|-------|--------|
| Q1 | Unknown + High Risk | {{N}} | Test first -- riskiest unknowns |
| Q2 | Known + High Risk | {{N}} | Monitor -- validated but high-impact |
| Q3 | Known + Low Risk | {{N}} | Accept -- no action needed |
| Q4 | Unknown + Low Risk | {{N}} | Defer -- test only if resources allow |

---

## Experiment Designs

<!-- For each experiment, document all required fields. Success criteria MUST include a specific metric + threshold. -->
<!-- Experiment type selection: Q1 assumptions need higher-confidence experiments (A/B test, concierge MVP). Early-stage concepts use lower-confidence experiments (paper prototype, one-question survey). -->

<!-- REPEATABLE BLOCK: EXPERIMENT START -->
### Experiment EXP-{{NNN}}: {{brief description}}

- **Hypothesis:** HYP-{{NNN}} -- {{hypothesis statement summary}}
- **Type:** {{A/B Test / Fake Door Test / Concierge MVP / Wizard of Oz / Paper Prototype / Smoke Test / One-Question Survey}}
- **Description:** {{what will be tested and how}}
- **Duration:** {{estimated duration}}
- **Sample Size:** {{number of participants or traffic requirement, if quantitative; "N/A" for qualitative-only experiments}}
- **Success Criteria:** {{specific metric + threshold, e.g., "checkout completion rate increases by >= 10% over control"}}
- **Measurement Method:** {{how data will be collected, e.g., "analytics event tracking", "moderated session observations", "survey response aggregation"}}
<!-- REPEATABLE BLOCK: EXPERIMENT END -->

### Experiment Type Selection Reference

| If you need to... | Recommended Type | Time | Confidence | Min. User Base |
|---|---|---|---|---|
| Validate demand before building a feature | Fake Door Test | 1-2 weeks | MEDIUM | Existing traffic |
| Test a new workflow end-to-end with real users | Wizard of Oz | 1-2 weeks | MEDIUM | 5-10 participants |
| Prove users will pay for or use a complex service | Concierge MVP | 2-4 weeks | MEDIUM | 5-15 participants |
| Quantitatively compare two design variants | A/B Test | 1-4 weeks | HIGH | Sufficient traffic for statistical power |
| Validate usability of an early-stage concept | Paper Prototype | 1-3 days | LOW-MEDIUM | 5 participants |
| Gauge market interest before investing effort | Smoke Test | 1-2 weeks | MEDIUM | Existing traffic or ad spend |
| Validate a single specific assumption quickly | One-Question Survey | 1-3 days | LOW | Existing user base |

---

## Validated Learning Log

<!-- Each entry documents a completed Build-Measure-Learn cycle. Only include entries for hypotheses that have completed at least one cycle. -->
<!-- If no cycles have been completed yet, state: "No Build-Measure-Learn cycles completed yet. This section will be populated as experiments are executed and results are documented." -->

<!-- REPEATABLE BLOCK: LEARNING START -->
### Learning L-{{NNN}}: {{brief description}}

- **Hypothesis:** HYP-{{NNN}} -- {{hypothesis statement}}
- **Experiment:** EXP-{{NNN}} -- {{experiment type}}: {{experiment description}}
- **Duration:** {{start date}} to {{end date}}
- **Success Criteria:** {{what was measured and the threshold}}
- **Result:** {{VALIDATED / INVALIDATED}}
- **Evidence:** {{specific data, metrics, or observations supporting the result}}
- **Decision:** {{PIVOT / PERSEVERE / KILL}}
- **Next Action:** {{what changes based on this learning}}
- **ICE Re-Score Impact:** {{describe any ICE score changes for related hypotheses based on this learning, or "No re-scoring triggered"}}
<!-- ICE-003 (lean-ux-methodology-rules.md): ICE scores MUST be re-scored after each Build-Measure-Learn cycle as evidence accumulates -->
<!-- REPEATABLE BLOCK: LEARNING END -->

### Decision Framework Reference

| Decision | When | Action |
|----------|------|--------|
| **PERSEVERE** | Hypothesis validated -- evidence supports the expected outcome | Continue in the validated direction; feed to HEART Metrics for ongoing measurement |
| **PIVOT** | Hypothesis partially validated or invalidated with useful learning | Change approach based on evidence; generate new hypotheses and add to backlog |
| **KILL** | Hypothesis invalidated with strong counter-evidence | Abandon this direction; archive the hypothesis and document the learning |

---

## Synthesis Judgments Summary

<!-- Required: document every AI-generated judgment (assumption quadrant placement, hypothesis prioritization, experiment type recommendation) with a confidence classification and rationale. -->

Each AI judgment call made during this facilitation is listed below for synthesis confidence gate compliance per `skills/user-experience/rules/synthesis-validation.md` [Confidence Classification].

| # | Judgment Type | Decision | Rationale | Confidence |
|---|--------------|----------|-----------|------------|
| 1 | Assumption placement | {{e.g., "ASM-001 placed in Q1 vs. Q2"}} | {{why this quadrant was chosen over the alternative}} | {{HIGH / MEDIUM / LOW}} |
| 2 | Hypothesis prioritization | {{e.g., "HYP-003 ranked above HYP-001 despite similar ICE"}} | {{tiebreaker rationale based on assumption quadrant or risk assessment}} | {{HIGH / MEDIUM / LOW}} |
| 3 | Experiment type selection | {{e.g., "EXP-001 recommended as Fake Door vs. A/B Test"}} | {{rationale based on available traffic, hypothesis maturity, and resource constraints}} | {{HIGH / MEDIUM / LOW}} |
| 4 | ICE score calibration | {{e.g., "HYP-002 Confidence scored 3 vs. 5"}} | {{evidence base assessment and conservative scoring rationale}} | {{HIGH / MEDIUM / LOW}} |
| 5 | Learning result classification | {{e.g., "HYP-001 classified INVALIDATED vs. PIVOT"}} | {{evidence strength assessment and decision rationale}} | {{HIGH / MEDIUM / LOW}} |
<!-- REPEATABLE ROW: Add one row per AI judgment call. At minimum, one judgment per category present in the evaluation. -->

**Confidence classification:**
- **HIGH:** Multiple data sources converge; validated by prior experiment evidence or multiple upstream sub-skill findings. Acknowledgment required before acting on design recommendations.
- **MEDIUM:** Single-framework reasoning; assumption-based assessment without empirical validation. Include "Validation Required" note; withhold definitive recommendation until validated against real experiment data or expert review.
- **LOW:** Insufficient data; speculative assessment; AI inference without empirical grounding. LOW findings are permanently labeled reference-only; design recommendations structurally omitted. Flag for human review before acting.

---

## Strategic Implications

<!-- Required: identify at least one pattern per subsection. Minimum two sentences per subsection. -->

### Organizational Learning Patterns

{{Identify hypothesis validation rate patterns, common failure modes across cycles, and what the pattern of validated/invalidated hypotheses reveals about product assumptions. Examples: "3 of 5 value assumptions were invalidated, suggesting the team's mental model of user motivation diverges from actual behavior"; "All usability hypotheses were validated, indicating design execution quality is strong but value proposition remains unproven."}}

### Experimentation Maturity Assessment

{{Assess the team's experimentation maturity based on: cycle duration (shorter = more mature), hypothesis specificity (more specific = more mature), evidence quality (quantitative > qualitative), and decision discipline (clear pivot/persevere/kill decisions with evidence vs. opinion-based continuation). Examples: "The team runs 2-week cycles with specific success criteria -- intermediate maturity"; "Experiment durations exceed 4 weeks, suggesting hypothesis scope is too broad for tiny-team iteration velocity."}}

### Iteration Velocity Recommendations

{{Recommend changes to improve Build-Measure-Learn cycle velocity. Examples: "Decompose HYP-003 into 2-3 narrower hypotheses to enable 1-week cycle duration"; "Shift from concierge MVP to fake door tests for demand validation to reduce cycle time from 4 weeks to 2 weeks."}}

### Product Strategy Implications

{{Draw strategic conclusions from validated and invalidated hypotheses. Examples: "The consistent invalidation of upsell hypotheses suggests the pricing page redesign should focus on retention rather than expansion revenue"; "Validated mobile checkout hypotheses confirm the investment case for a mobile-first redesign."}}

---

## Limitations and Reliability

### Single-Facilitator Disclosure (P-022)

Lean UX methodology recommends collaborative hypothesis generation with the full team for diverse perspective inclusion (Gothelf & Seiden, 2021). This facilitation was conducted by a **single AI facilitator**.

**Compensating factors:**
- Systematic methodology coverage (all 5 Build-Measure-Learn cycle steps with structured formats)
- Consistent ICE scoring using the same 1-10 scale criteria across all hypotheses
- Structured assumption mapping with mandatory quadrant rationale for every placement

**Residual limitations:**
- No perspective diversity from cross-functional team collaboration
- Context-specific hypotheses requiring domain expertise, organizational knowledge, or direct user empathy may be missed
- Hypotheses are secondary-research-derived starting points, not empirically grounded predictions
- Assumption quadrant placements reflect AI judgment; real-world risk and knowledge levels may differ

### Input Mode Limitations

<!-- If Miro MCP available, use this block: -->
<!-- Full collaborative board access available. No mode-specific limitations. -->

<!-- If degraded mode, use this block: -->
**[DEGRADED MODE]** This output was produced without Miro MCP access. Input was provided via text-based exercise mode. The following features are reduced:

- Assumption maps produced as structured markdown tables; visual quadrant movement tracking not available
- Hypothesis backlogs maintained as markdown tables; interactive prioritization not available
- Build-Measure-Learn cycle tracking uses text-based status updates; visual progress boards not available
- Cannot create or update collaborative visual boards
- Cannot visualize assumption movement between quadrants over time
- Cannot embed experiment results alongside visual hypothesis boards

<!-- Delete whichever block above does not apply. -->

### Recommendation for High-Stakes Hypotheses

For hypotheses addressing **Q1 assumptions** (Unknown + High Risk) or requiring **significant engineering investment** (> 1 sprint):
- Supplement AI-facilitated hypothesis generation with team review before committing to experiment execution
- Validate assumption quadrant placements with domain experts who have direct user contact
- Consider running multiple experiment types for the same hypothesis to increase confidence

---

## Self-Review Checklist

Before persisting the report, verify all items below (S-010):

- [ ] 1. Every hypothesis follows the canonical Lean UX format (all 4 components: outcome, users, change, evidence) (HYP-001)
- [ ] 2. Every hypothesis has a unique ID (HYP-{{NNN}}) with no gaps in the sequence (HYP-005)
- [ ] 3. Every hypothesis has an ICE score with all three dimensions (Impact, Confidence, Ease) rated 1-10 (ICE-001)
- [ ] 4. Every assumption has a quadrant placement (Q1-Q4) with a one-line rationale (ASM-001, ASM-002)
- [ ] 5. Every assumption is classified into exactly one category (Value, Usability, or Feasibility) (ASM-004)
- [ ] 6. Every Q1 assumption has at least one linked experiment design (EXP-{NNN}) (ASM-006)
- [ ] 7. Every experiment design has measurable success criteria (specific metric + threshold) (EXP-002, EXP-006)
- [ ] 8. Validated Learning Log entries have evidence supporting the VALIDATED/INVALIDATED result (VLD-001)
- [ ] 9. No learning entries exist without corresponding experiment data -- do not fabricate results (VLD-007, P-022)
- [ ] 10. Decision fields are consistent with result fields (no PERSEVERE decision for INVALIDATED result) (VLD-003)
- [ ] 11. The Synthesis Judgments Summary lists each AI judgment call with confidence classification (CLS-001)
- [ ] 12. The navigation table is present with correct anchor links (H-23)
- [ ] 13. Degraded mode disclosure is present if operating without Miro MCP (P-022)
- [ ] 14. Handoff Data includes only VALIDATED or INVALIDATED hypotheses (not DRAFT/ACTIVE/DEFERRED)
- [ ] 15. Hypothesis backlog is ordered by ICE score descending
- [ ] 16. Assumption map quadrant summary counts match the assumption inventory
- [ ] 17. PIVOT hypotheses generated from Step 4 are added to the backlog with ICE scores before the next cycle (BML-005, ICE-007)

---

## Handoff Data

Structured data for downstream sub-skill consumption (HEART Metrics). Only hypotheses with status **VALIDATED** or **INVALIDATED** (completed at least one Build-Measure-Learn cycle) are included per the cross-framework handoff threshold.

### Hypotheses for Downstream Consumption

| Hypothesis ID | Status | Outcome Metric | Metric Implication | Candidate HEART Category |
|--------------|--------|----------------|--------------------|--------------------------|
| HYP-{{NNN}} | {{VALIDATED / INVALIDATED}} | {{metric tested}} | {{what the result means for ongoing measurement}} | {{Happiness / Engagement / Adoption / Retention / Task success}} |
<!-- REPEATABLE ROW: Copy row above for each hypothesis with status VALIDATED or INVALIDATED. -->
<!-- Hypotheses with status DRAFT, ACTIVE, or DEFERRED are NOT included in handoff data. -->

### Handoff YAML

```yaml
# Structured handoff for ux-orchestrator and downstream sub-skills
# Fields marked [handoff-v2] follow docs/schemas/handoff-v2.schema.json
# Fields marked [ux-ext] are ux-lean-ux sub-skill extensions

# --- handoff-v2 schema fields ---
from_agent: ux-lean-ux-facilitator                # [handoff-v2] required
to_agent: ux-orchestrator                          # [handoff-v2] required
task: "Lean UX hypothesis cycle for {{TOPIC}}"       # [handoff-v2] required
success_criteria:                                  # [handoff-v2] required, min 1
  - "All hypotheses follow canonical Lean UX format (4 components)"
  - "Every assumption has quadrant placement with rationale"
  - "Every experiment design has measurable success criteria"
  - "ICE scores present for all backlog hypotheses"
artifacts:                                         # [handoff-v2] required
  - "projects/${JERRY_PROJECT}/engagements/{{ENGAGEMENT_ID}}/ux-lean-ux-facilitator-{{TOPIC_SLUG}}.md"
key_findings:                                      # [handoff-v2] required, 3-5 entries per CB-04
  - "{{top finding 1 summary}}"
  - "{{top finding 2 summary}}"
  - "{{top finding 3 summary}}"
blockers: []                                       # [handoff-v2] required
confidence: {{0.0-1.0}}                             # [handoff-v2] required
criticality: {{C1 / C2 / C3 / C4}}                  # [handoff-v2] required

# --- ux-lean-ux extension fields ---
engagement_id: {{ENGAGEMENT_ID}}                     # [ux-ext] UX-{{NNNN}} format
total_hypotheses: {{TOTAL_HYPOTHESES}}               # [ux-ext]
hypothesis_status_distribution:                    # [ux-ext]
  DRAFT: {{COUNT_DRAFT}}
  ACTIVE: {{COUNT_ACTIVE}}
  VALIDATED: {{COUNT_VALIDATED}}
  INVALIDATED: {{COUNT_INVALIDATED}}
  DEFERRED: {{COUNT_DEFERRED}}
assumptions_mapped: {{TOTAL_ASSUMPTIONS}}            # [ux-ext]
q1_assumptions: {{Q1_COUNT}}                         # [ux-ext] highest-risk unknowns
experiments_designed: {{TOTAL_EXPERIMENTS}}           # [ux-ext]
cycles_completed: {{CYCLE_COUNT}}                    # [ux-ext]
degraded_mode: {{true / false}}                      # [ux-ext]
artifact_path: "projects/${JERRY_PROJECT}/engagements/{{ENGAGEMENT_ID}}/ux-lean-ux-facilitator-{{TOPIC_SLUG}}.md"  # [ux-ext]
handoff_hypotheses_count: {{HANDOFF_COUNT}}          # [ux-ext] VALIDATED + INVALIDATED count
```

---

*Template Version: 1.2.0 | /ux-lean-ux Sub-Skill | PROJ-022 User Experience Skill*
*Source: SKILL.md [Output Specification], agent [output] section, agent [methodology] section*
*Lean UX framework: Gothelf, J. & Seiden, J. (2021). "Lean UX: Applying Lean Principles to Improve User Experience." 3rd ed. O'Reilly.*
*ICE scoring: Sean Ellis, GrowthHackers (circa 2015). Adapted for Lean UX hypothesis prioritization.*
*Experiment taxonomy: Gothelf & Seiden (2021); Ries, E. (2011) "The Lean Startup" (Crown Business); Croll, A. & Yoskovitz, B. (2013) "Lean Analytics" (O'Reilly).*
*Methodology rules: `skills/ux-lean-ux/rules/lean-ux-methodology-rules.md` (BML, HYP, ASM, EXP, ICE, VLD, CLS, QG rule families)*
*Handoff schema: `docs/schemas/handoff-v2.schema.json` (JSON Schema Draft 2020-12)*
*ORCHESTRATION: projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml*
