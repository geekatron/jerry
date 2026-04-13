<!-- TEMPLATE: assumption-map-template.md | VERSION: 1.2.1 | DATE: 2026-03-04 | REVISION: iter4 micro-fixes -- Quadrant Boundary rule IDs, experiment type cross-reference, Q4 ASM-005 framing note -->
<!-- SKILL: /ux-lean-ux | AGENT: ux-lean-ux-facilitator -->
<!-- SOURCE: SKILL.md [Methodology § Assumption Mapping], agent <methodology> Step 2, heuristic-report-template.md (structural pattern) -->
<!-- USAGE: Fill {{PLACEHOLDER}} fields. Copy REPEATABLE BLOCK markers for each assumption. This is a standalone assumption mapping worksheet for Step 2 of the Lean UX methodology. It can be used independently of the full hypothesis backlog. -->

# Assumption Map: {{TOPIC}}

> **Engagement:** {{ENGAGEMENT_ID}}
> **Product:** {{PRODUCT_NAME}}
> **Domain:** {{PRODUCT_DOMAIN}}
> **Date:** {{MAPPING_DATE}}
> **Facilitator:** {{FACILITATOR}}

## Document Sections

| Section | Purpose |
|---------|---------|
| [Product Context](#product-context) | Product/feature description, design change under assessment, target users |
| [Quadrant Boundary Definitions](#quadrant-boundary-definitions) | Instructional guidance: what distinguishes Known from Unknown, High Risk from Low Risk |
| [Assumption Inventory](#assumption-inventory) | Complete inventory of assumptions with categories and sources |
| [4-Quadrant Assumption Map](#4-quadrant-assumption-map) | Assumptions placed into Q1-Q4 with rationale and recommended actions |
| [Assumption Movement Tracking](#assumption-movement-tracking-optional) | Optional: tracks quadrant changes across cycles (ASM-005) |
| [Prioritized Testing Queue](#prioritized-testing-queue) | Q1 and Q2 assumptions ordered by ICE score with linked hypothesis IDs |
| [Synthesis Judgments Summary](#synthesis-judgments-summary) | AI judgment calls for quadrant placements and priority decisions |
| [Self-Review Checklist](#self-review-checklist) | S-010: Pre-persistence verification checklist |
| [Handoff Data](#handoff-data) | Structured data for downstream consumption (experiment design, hypothesis backlog) |

---

## Product Context

**Product:** {{PRODUCT_NAME}}
**Domain:** {{PRODUCT_DOMAIN}}
**Target Users:** {{TARGET_USER_DESCRIPTION}}

### Design Change Under Assessment

{{DESIGN_CHANGE_DESCRIPTION -- Describe the product change, feature addition, or design direction being assessed. Include what prompted this change (user feedback, business goal, prior experiment result, heuristic evaluation finding). This context anchors all assumptions to a specific design decision.}}

### Prior Research Inputs

<!-- List any upstream artifacts that inform assumption generation. Remove rows that do not apply. -->

| Source | Artifact | Key Takeaway |
|--------|----------|--------------|
| JTBD Analysis | {{path or "N/A"}} | {{one-line summary of relevant job statements or switch forces}} |
| Heuristic Evaluation | {{path or "N/A"}} | {{one-line summary of relevant severity >= 2 findings}} |
| Design Sprint | {{path or "N/A"}} | {{one-line summary of Day 4 interview findings or prototype validation}} |
| Prior Experiments | {{path or "N/A"}} | {{one-line summary of prior Build-Measure-Learn cycle outcomes}} |
| Stakeholder Input | {{source or "N/A"}} | {{one-line summary of stakeholder assumptions or business constraints}} |

---

## Quadrant Boundary Definitions

<!-- Do not modify this section -- it provides the classification criteria used to place assumptions into the 4-quadrant map. These definitions ensure consistent, defensible placements. Rules ASM-001, ASM-002, ASM-003 govern quadrant placement requirements and distribution validation. -->

The assumption map uses two independent axes to classify each assumption. Every assumption is assessed on both axes and placed into the quadrant at their intersection.

### Axis 1: Knowledge (Known vs. Unknown)

| Classification | Definition | Evidence Required |
|---------------|------------|-------------------|
| **Known** | The team has direct evidence supporting or refuting this assumption. Evidence comes from: completed experiments, production analytics, published research with relevant sample populations, direct user observation, or established industry benchmarks with documented applicability. | Cite the specific evidence source (experiment ID, analytics dashboard, study reference, observation record). If the evidence is older than 6 months, note the staleness risk. |
| **Unknown** | The team lacks direct evidence. The assumption is based on: gut feeling, analogy to different contexts, stakeholder opinion without supporting data, extrapolation from unrelated domains, or untested internal beliefs. | State explicitly what evidence is missing and what type of evidence would move this assumption to "Known" (e.g., "Requires A/B test with N=200 sample" or "Needs 5 user interviews with target segment"). |

**Boundary judgment:** When uncertain whether evidence qualifies as "Known," ask: "Would a skeptical colleague accept this evidence as sufficient to make a product decision?" If no, classify as Unknown. When uncertain between adjacent classifications, choose Unknown -- under-classifying knowledge is safer than over-classifying it (rating discipline per Gothelf & Seiden, 2021).

### Axis 2: Risk (High Risk vs. Low Risk)

| Classification | Definition | Indicators |
|---------------|------------|------------|
| **High Risk** | If this assumption is wrong, the design change will fail to achieve its goal, cause user harm, or require significant rework (> 1 sprint). The assumption is load-bearing -- other assumptions depend on it being true. | (1) Large user population affected (> 25% of target segment), (2) irreversible or costly-to-reverse change, (3) multiple downstream decisions depend on this assumption, (4) contradicts existing user behavior patterns. |
| **Low Risk** | If this assumption is wrong, the impact is contained. The design change can still succeed, the issue is cosmetic or affects a small segment, and course correction is inexpensive (< 1 sprint). | (1) Small user population affected (< 10% of target segment), (2) easily reversible change, (3) no downstream dependencies, (4) aligned with existing user behavior patterns. |

**Boundary judgment:** When uncertain about risk level, ask: "If we ship this and the assumption is wrong, what is the blast radius?" If the answer involves user churn, revenue loss, or multi-sprint rework, classify as High Risk. When uncertain between adjacent classifications, choose High Risk -- under-estimating risk leads to untested critical assumptions (rating discipline per Gothelf & Seiden, 2021).

### Quadrant Summary

```
                    HIGH RISK
                       |
    +---------+--------+--------+---------+
    |                  |                  |
    |  Q2: Known       |  Q1: Unknown     |
    |  High Risk       |  High Risk       |
    |                  |                  |
    |  ACTION:         |  ACTION:         |
    |  Monitor --      |  Validate        |
    |  revisit if      |  immediately --  |
    |  conditions      |  riskiest        |
    |  change          |  unknowns        |
    |                  |                  |
KNOWN -----------------+----------------- UNKNOWN
    |                  |                  |
    |  Q3: Known       |  Q4: Unknown     |
    |  Low Risk        |  Low Risk        |
    |                  |                  |
    |  ACTION:         |  ACTION:         |
    |  Accept --       |  Defer -- test   |
    |  no action       |  only if         |
    |  needed          |  resources       |
    |                  |  allow           |
    |                  |                  |
    +---------+--------+--------+---------+
                       |
                    LOW RISK
```

---

## Assumption Inventory

List all assumptions identified for the design change. Each assumption receives a unique ID and is classified by category and source before quadrant placement.

### Assumption Categories

| Category | Definition | Upstream Signal |
|----------|------------|-----------------|
| **Value** | "Users want this outcome" -- the design change delivers something users find valuable | JTBD job statements, switch forces, user interview data |
| **Usability** | "Users can accomplish this task" -- users can successfully interact with the design change | Heuristic evaluation findings (severity >= 2), task completion data |
| **Feasibility** | "We can build this within constraints" -- the design change is technically implementable within time, budget, and team capacity | Technical spike results, architecture reviews, prior implementation experience |

<!-- REPEATABLE BLOCK: ASSUMPTION INVENTORY ROW START -->

| ID | Assumption Statement | Category | Source |
|----|---------------------|----------|--------|
| ASM-{{NNN}} | {{Clearly state what is assumed to be true. Use the format: "We assume that [specific claim about users, value, usability, or feasibility]." Avoid vague language -- each assumption must be specific enough to be testable.}} | {{Value / Usability / Feasibility}} | {{User research / Stakeholder input / Domain expertise / Prior experiments / Analytics data / Heuristic evaluation / JTBD analysis / Design Sprint findings}} |
<!-- Repeat rows for each assumption. Aim for 8-15 assumptions per design change. Fewer than 5 suggests under-exploration; more than 20 suggests the design change scope is too broad and should be decomposed. -->

<!-- REPEATABLE BLOCK: ASSUMPTION INVENTORY ROW END -->

---

## 4-Quadrant Assumption Map

Place each assumption from the inventory into the appropriate quadrant using the [Quadrant Boundary Definitions](#quadrant-boundary-definitions). Every placement requires a one-line rationale explaining the risk and knowledge assessment.

### Q1: Unknown + High Risk -- Validate Immediately

**Priority:** HIGHEST. These are the riskiest unknowns that could invalidate the entire design approach. Test these first.

**Action:** Design experiments to validate or invalidate these assumptions before committing engineering resources. Q1 assumptions flow directly to the [Prioritized Testing Queue](#prioritized-testing-queue).

<!-- REPEATABLE BLOCK: Q1 ASSUMPTION START -->

| Assumption ID | Assumption Statement | Placement Rationale | Recommended Action |
|--------------|---------------------|--------------------|--------------------|
| ASM-{{NNN}} | {{assumption statement from inventory}} | {{One-line rationale: why this is Unknown (what evidence is missing?) AND why this is High Risk (what fails if this assumption is wrong?)}} | {{Specific next step: e.g., "Design A/B test targeting N=200 users" or "Run 5 user interviews with target segment" or "Build fake door test for feature demand validation"}} |
<!-- Repeat rows for each Q1 assumption -->

<!-- REPEATABLE BLOCK: Q1 ASSUMPTION END -->

**Q1 count:** {{N}} assumptions require immediate validation.

---

### Q2: Known + High Risk -- Monitor

**Priority:** MEDIUM. These assumptions are supported by evidence but carry high impact if conditions change. They do not need immediate testing but require ongoing monitoring.

**Action:** Document the evidence supporting each assumption. Set review triggers (e.g., "re-evaluate if conversion drops below X%" or "re-evaluate after next product release"). Q2 assumptions may escalate to Q1 if supporting evidence becomes stale or conditions change.

> **Re-evaluation triggers:** Re-evaluate Q2 assumptions when: (a) new user data arrives that changes confidence in the supporting evidence, (b) 2+ sprint cycles pass without validation activity, or (c) a related Q1 assumption is validated or invalidated, shifting the risk landscape. Monitoring triggers SHOULD be quantitative where possible (e.g., "re-evaluate if conversion rate drops below 15%") rather than qualitative observations that may not fire reliably.

<!-- REPEATABLE BLOCK: Q2 ASSUMPTION START -->

| Assumption ID | Assumption Statement | Placement Rationale | Monitoring Trigger |
|--------------|---------------------|--------------------|--------------------|
| ASM-{{NNN}} | {{assumption statement from inventory}} | {{One-line rationale: why this is Known (what evidence supports it?) AND why this is High Risk (what fails if conditions change?)}} | {{Specific condition that would trigger re-evaluation: e.g., "Re-evaluate if user segment demographics shift" or "Re-evaluate quarterly against updated analytics"}} |
<!-- Repeat rows for each Q2 assumption -->

<!-- REPEATABLE BLOCK: Q2 ASSUMPTION END -->

**Q2 count:** {{N}} assumptions are validated but require monitoring.

---

### Q3: Known + Low Risk -- Accept

**Priority:** LOW. These assumptions are supported by evidence and carry low impact. No action needed beyond documentation.

**Action:** Accept and move on. These assumptions do not warrant experimentation effort. Archive for reference.

<!-- REPEATABLE BLOCK: Q3 ASSUMPTION START -->

| Assumption ID | Assumption Statement | Placement Rationale | Notes |
|--------------|---------------------|--------------------|--------------------|
| ASM-{{NNN}} | {{assumption statement from inventory}} | {{One-line rationale: why this is Known (what evidence supports it?) AND why this is Low Risk (why is impact contained?)}} | {{Any relevant context or reference for future use}} |
<!-- Repeat rows for each Q3 assumption -->

<!-- REPEATABLE BLOCK: Q3 ASSUMPTION END -->

**Q3 count:** {{N}} assumptions accepted without further action.

---

### Q4: Unknown + Low Risk -- Defer

**Priority:** LOWEST. These assumptions lack evidence but carry low impact. Test only if resources allow after Q1 and Q2 are addressed.

**Action:** Defer to a future Build-Measure-Learn cycle. If team capacity allows after high-priority assumptions are resolved, include these in opportunistic testing. Q4 assumptions may escalate to Q1 or Q2 if the design change evolves and their risk profile increases.

<!-- REPEATABLE BLOCK: Q4 ASSUMPTION START -->

| Assumption ID | Assumption Statement | Placement Rationale | Escalation Condition (ASM-005) |
|--------------|---------------------|--------------------|--------------------|
| ASM-{{NNN}} | {{assumption statement from inventory}} | {{One-line rationale: why this is Unknown (what evidence is missing?) AND why this is Low Risk (why is impact contained?)}} | {{Condition under which this assumption would escalate to a higher-priority quadrant: e.g., "Escalates to Q1 if feature scope expands to include enterprise users." Note: ASM-005 governs post-hoc movement recording; the proactive escalation trigger here is a practitioner extension for forward-looking risk management.}} |
<!-- Repeat rows for each Q4 assumption -->

<!-- REPEATABLE BLOCK: Q4 ASSUMPTION END -->

**Q4 count:** {{N}} assumptions deferred to future cycles.

---

### Quadrant Distribution Summary

| Quadrant | Count | Percentage |
|----------|-------|------------|
| Q1: Unknown + High Risk | {{N}} | {{N}}% |
| Q2: Known + High Risk | {{N}} | {{N}}% |
| Q3: Known + Low Risk | {{N}} | {{N}}% |
| Q4: Unknown + Low Risk | {{N}} | {{N}}% |
| **Total** | **{{TOTAL_ASSUMPTIONS}}** | **100%** |

**Distribution health check:** A healthy assumption map for an early-stage design change typically shows 30-50% in Q1 (many unknowns to test), 10-20% in Q2 (some validated high-risk items), 20-30% in Q3 (baseline knowns), and 10-20% in Q4 (low-priority unknowns). If > 60% of assumptions land in Q3/Q4, the design change may be well-understood and Lean UX experimentation may be unnecessary. If > 60% land in Q1, the design change may need decomposition before experimentation. *Note: These percentages are heuristic practitioner guidance from Lean UX practice, not empirically validated thresholds. Calibrate against your product domain and prior mapping experience.*

### Assumption Movement Tracking (Optional)

<!-- Optional section per ASM-005 (MEDIUM). Include when iterating the assumption map across multiple Build-Measure-Learn cycles. Tracks quadrant movement as evidence accumulates. Remove this section if this is a single-cycle mapping. -->

When assumptions move between quadrants due to new evidence (e.g., Q1 to Q2 after experiment validation, Q4 to Q1 after scope expansion), record the movement below per ASM-005.

| Assumption ID | From Quadrant | To Quadrant | Evidence Triggering Move | Cycle / Date |
|--------------|---------------|-------------|--------------------------|--------------|
| ASM-{{NNN}} | {{Q1 / Q2 / Q3 / Q4}} | {{Q1 / Q2 / Q3 / Q4}} | {{Brief description of the evidence that changed the risk or knowledge classification}} | {{cycle number or date}} |
<!-- Repeat rows for each quadrant movement -->

---

## Prioritized Testing Queue

Assumptions from Q1 (Unknown + High Risk) and Q2 (Known + High Risk, where monitoring triggers have fired) ordered by ICE score. This queue feeds directly into hypothesis generation and experiment design (Steps 1 and 3 of the Lean UX methodology).

### ICE Scoring Reference

Each assumption is scored on three dimensions using a 1-10 scale. Composite ICE score = `(Impact + Confidence + Ease) / 3`. ICE scoring framework originated in the growth hacking community (Sean Ellis, GrowthHackers, circa 2015). Adapted here for assumption testing prioritization.

> Full 6-anchor scales below. Source: `skills/ux-lean-ux/rules/lean-ux-methodology-rules.md` [ICE Scoring Rules § Scale Anchors].

#### Impact (How many users are affected and how significantly?)

| Score | Anchor | Definition |
|-------|--------|------------|
| 1 | Minimal | Affects < 1% of users OR negligible behavior change |
| 2-3 | Low | Affects 1-10% of users with minor behavior change |
| 4-5 | Moderate | Affects ~25% of users with moderate behavior change |
| 6-7 | Significant | Affects ~50% of users with notable behavior change |
| 8-9 | High | Affects ~75% of users with significant behavior change |
| 10 | Transformative | Affects > 75% of users with fundamental behavior change |

#### Confidence (How much evidence supports this assumption?)

| Score | Anchor | Definition |
|-------|--------|------------|
| 1 | Gut feeling | No data, no analogies, no prior research; pure team intuition |
| 2-3 | Weak signal | Anecdotal evidence, single user complaint, informal observation |
| 4-5 | Indirect evidence | Analytics trends, competitor benchmarks, related heuristic findings, general UX principles |
| 6-7 | Moderate evidence | User research findings (interviews, surveys), heuristic evaluation severity >= 2 findings, JTBD job statements |
| 8-9 | Strong evidence | Prior Build-Measure-Learn cycle data, A/B test results from related experiments |
| 10 | Direct validation | Statistically significant A/B test data directly testing this assumption |

#### Ease (How quickly can we test this assumption?)

| Score | Anchor | Definition |
|-------|--------|------------|
| 1 | Very difficult | > 1 month of engineering/design effort to build the experiment |
| 2-3 | Difficult | 2-4 weeks effort; requires significant coordination or new infrastructure |
| 4-5 | Moderate | 1-2 weeks effort; requires moderate coordination |
| 6-7 | Easy | 3-5 days effort; uses existing tools with minor setup |
| 8-9 | Very easy | 1-2 days effort; uses existing tools directly |
| 10 | Trivial | < 1 day; can test with a simple survey or existing analytics |

**Rating discipline:** When uncertain between two adjacent scores, choose the LOWER score. Over-estimating ICE scores leads to misallocated experimentation effort (P-022 compliance).

### Testing Queue

| Priority | Assumption ID | Assumption Statement | Quadrant | Impact (I) | Confidence (C) | Ease (E) | ICE Score | Linked Hypothesis | Recommended Experiment Type |
|----------|--------------|---------------------|----------|-----------|----------------|---------|-----------|-------------------|---------------------------|
| 1 | ASM-{{NNN}} | {{assumption statement}} | Q1 | {{1-10}} | {{1-10}} | {{1-10}} | {{(I+C+E)/3}} | HYP-{{NNN}} | {{A/B test / Fake door / Concierge MVP / Wizard of Oz / Paper prototype / Smoke test / One-question survey}} |
| 2 | ASM-{{NNN}} | {{assumption statement}} | Q1 | {{1-10}} | {{1-10}} | {{1-10}} | {{(I+C+E)/3}} | HYP-{{NNN}} | {{experiment type}} |
<!-- Repeat rows ordered by ICE score descending. Include all Q1 assumptions and any Q2 assumptions whose monitoring triggers have fired. -->

**Queue coverage:** {{N}} of {{TOTAL_Q1_Q2}} high-priority assumptions have linked hypotheses and experiment recommendations.

**Experiment type selection guide:**
- Sufficient traffic + narrow measurable hypothesis: **A/B test**
- Feature does not exist yet: **Fake door test** or **Smoke test** for demand validation
- Complex workflow hypothesis: **Wizard of Oz** (usability) or **Concierge MVP** (value)
- Early concept stage: **Paper prototype**
- Single-question answer needed: **One-question survey**

> For the full 7-condition priority-ordered decision path (including EXP-007 residual cases), see `skills/ux-lean-ux/rules/lean-ux-methodology-rules.md` [Experiment Type Selection Rules § Selection Decision Path].

---

## Synthesis Judgments Summary

<!-- Required: document at minimum one judgment per category present in the mapping (quadrant placement, priority ordering, ICE scoring, category classification). -->

Each AI judgment call made during this assumption mapping is listed below for synthesis confidence gate compliance per `skills/user-experience/rules/synthesis-validation.md` [Confidence Classification].

| # | Judgment Type | Decision | Rationale | Confidence |
|---|--------------|----------|-----------|------------|
| 1 | Quadrant placement | {{e.g., "ASM-003 placed in Q1 vs. Q2"}} | {{why this classification was chosen over the alternative}} | {{HIGH / MEDIUM / LOW}} |
| 2 | Category classification | {{e.g., "ASM-005 classified as Value vs. Usability"}} | {{reasoning for category selection}} | {{HIGH / MEDIUM / LOW}} |
| 3 | ICE scoring | {{e.g., "ASM-001 Impact rated 8 vs. 6"}} | {{evidence supporting the score selection}} | {{HIGH / MEDIUM / LOW}} |
| 4 | Priority ordering | {{e.g., "ASM-002 prioritized above ASM-004 despite equal ICE"}} | {{tiebreaker rationale}} | {{HIGH / MEDIUM / LOW}} |
<!-- Repeat rows for each judgment call -->

**Confidence classification:**
- **HIGH:** Based on multiple converging data sources or validated experiment evidence; recommendation is actionable.
- **MEDIUM:** Based on single-framework reasoning or assumption-based assessment without empirical validation; include "Validation Required" note.
- **LOW:** Insufficient data or speculative assessment; flag for human review before acting. LOW judgments are reference-only; definitive recommendations structurally omitted.

---

## Self-Review Checklist

Before persisting the assumption map, verify all items below (S-010):

- [ ] 1. All assumptions have unique IDs in `ASM-{{NNN}}` format with no gaps (ASM-001)
- [ ] 2. Every assumption has a category classification (Value, Usability, or Feasibility) per ASM-004
- [ ] 3. Every assumption has a source citation (not "unknown" or blank)
- [ ] 4. Every assumption is placed in exactly one quadrant (Q1-Q4) with a one-line placement rationale (ASM-001, ASM-002)
- [ ] 5. No assumption appears in multiple quadrants (no duplicates across Q1-Q4 tables) (ASM-001)
- [ ] 6. Q1 and Q2 assumptions appear in the Prioritized Testing Queue with ICE scores (ASM-006, ICE-001)
- [ ] 7. ICE scores use the 1-10 scale consistently (no scores outside range) (ICE-006)
- [ ] 8. The Quadrant Distribution Summary counts match the actual assumption placements (ASM-003)
- [ ] 9. The Synthesis Judgments Summary lists at least one judgment per category present (CLS-001)
- [ ] 10. The navigation table is present with correct anchor links (H-23)
- [ ] 11. Degraded mode disclosure is present if operating without Miro MCP (P-022, VLD-007)

---

## Handoff Data

Structured data for downstream consumption by the hypothesis backlog (Step 1), experiment design (Step 3), and ux-orchestrator coordination.

> **Companion template:** [hypothesis-backlog-template.md](../templates/hypothesis-backlog-template.md) -- assumptions validated here feed into hypotheses tracked in the hypothesis backlog.

### High-Priority Assumptions for Downstream Consumption

| Assumption ID | Quadrant | Category | ICE Score | Linked Hypothesis | Status |
|--------------|----------|----------|-----------|-------------------|--------|
| ASM-{{NNN}} | Q1 | {{Value / Usability / Feasibility}} | {{(I+C+E)/3}} | HYP-{{NNN}} or -- | {{Pending validation / Experiment designed / Validated / Invalidated}} |
<!-- Include only Q1 and Q2 assumptions. Q3 and Q4 are excluded from downstream handoff. -->

### Handoff YAML

```yaml
# Structured handoff for ux-orchestrator and downstream methodology steps
# Fields marked [handoff-v2] follow docs/schemas/handoff-v2.schema.json
# Fields marked [ux-ext] are ux-lean-ux sub-skill extensions

# --- handoff-v2 schema fields ---
from_agent: ux-lean-ux-facilitator          # [handoff-v2] required
to_agent: ux-orchestrator                    # [handoff-v2] required
task: "Assumption mapping for {{TOPIC}}"       # [handoff-v2] required
success_criteria:                            # [handoff-v2] required, min 1
  - "All assumptions classified into categories with sources"
  - "Every assumption placed in exactly one quadrant with rationale"
  - "Q1 and Q2 assumptions scored with ICE and linked to hypotheses"
  - "Quadrant distribution summary matches actual placements"
artifacts:                                   # [handoff-v2] required
  - "projects/${JERRY_PROJECT}/engagements/{{ENGAGEMENT_ID}}/assumption-map-{{TOPIC_SLUG}}.md"
key_findings:                                # [handoff-v2] required, 3-5 entries per CB-04
  - "{{top Q1 assumption summary}}"
  - "{{second Q1 assumption summary}}"
  - "{{key distribution insight, e.g., 'X% of assumptions are Unknown+High Risk'}}"
blockers: []                                 # [handoff-v2] required
confidence: {{0.0-1.0}}                       # [handoff-v2] required
criticality: {{C1 / C2 / C3 / C4}}           # [handoff-v2] required

# --- ux-lean-ux extension fields ---
engagement_id: {{ENGAGEMENT_ID}}               # [ux-ext] UX-{{NNNN}} format
total_assumptions: {{TOTAL_ASSUMPTIONS}}       # [ux-ext]
quadrant_distribution:                       # [ux-ext]
  Q1: {{N}}
  Q2: {{N}}
  Q3: {{N}}
  Q4: {{N}}
categories_represented:                      # [ux-ext]
  value: {{N}}
  usability: {{N}}
  feasibility: {{N}}
q1_assumptions_with_hypotheses: {{N}}          # [ux-ext] Q1 assumptions linked to HYP-{{NNN}}
highest_ice_score: {{N.N}}                     # [ux-ext] top ICE score in testing queue
degraded_mode: {{true / false}}               # [ux-ext] Miro MCP availability
```

---

*Template Version: 1.2.1 | /ux-lean-ux Sub-Skill | PROJ-022 User Experience Skill*
*Source: SKILL.md [Methodology § Assumption Mapping], agent <methodology> Step 2, heuristic-report-template.md (structural pattern)*
*Methodology: Gothelf, J. & Seiden, J. (2021). "Lean UX: Applying Lean Principles to Improve User Experience" (3rd ed.). O'Reilly Media.*
*ICE Scoring: Sean Ellis, GrowthHackers (circa 2015). Adapted for Lean UX assumption prioritization.*
*Handoff schema: `docs/schemas/handoff-v2.schema.json` (JSON Schema Draft 2020-12)*
*ORCHESTRATION: projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml*
