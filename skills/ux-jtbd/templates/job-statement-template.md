<!-- TEMPLATE: job-statement-template.md | VERSION: 1.4.0 | DATE: 2026-03-04 -->
<!-- SKILL: /ux-jtbd | AGENT: ux-jtbd-analyst | PARENT: /user-experience -->
<!-- METHODOLOGY: Christensen JTBD (2016), Ulwick ODI (2016), Moesta Four Forces (2020) -->
<!-- Replace all {{PLACEHOLDER}} values. Duplicate <!-- REPEATABLE BLOCK --> sections per item. -->

# JTBD Analysis: {{TOPIC}}

> **Engagement ID:** {{ENGAGEMENT_ID}}
> **Product:** {{PRODUCT_NAME}}
> **Analysis Date:** {{ANALYSIS_DATE}}
> **Analyst:** {{ANALYST}}
> **Synthesis Confidence:** {{OVERALL_CONFIDENCE}}

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Top jobs, switch forces, strategic recommendation |
| [L1: Job Inventory](#l1-job-inventory) | Full job catalog with classification and scoring |
| [L1: Opportunity Score Matrix](#l1-opportunity-score-matrix) | Ranked opportunity scores with service classification |
| [L1: Switch Force Analysis](#l1-switch-force-analysis) | Moesta four forces per job |
| [L1: Job Map](#l1-job-map) | Ulwick 8-step universal job process |
| [L1: Hiring Criteria](#l1-hiring-criteria) | Criterion table with measurement and weight per job |
| [L2: Synthesis and Prioritization](#l2-synthesis-and-prioritization) | Cross-job patterns, hierarchy, focus areas |
| [L2: Confidence Summary](#l2-confidence-summary) | Per-job confidence with justification |
| [Handoff Data](#handoff-data) | Structured YAML for downstream consumption |

---

## L0: Executive Summary

**Total jobs identified:** {{TOTAL_JOB_COUNT}} ({{FUNCTIONAL_COUNT}} functional, {{SOCIAL_COUNT}} social, {{EMOTIONAL_COUNT}} emotional)

**Top underserved jobs:**
1. {{TOP_JOB_1_STATEMENT}} (Opportunity Score: {{TOP_JOB_1_SCORE}})
2. {{TOP_JOB_2_STATEMENT}} (Opportunity Score: {{TOP_JOB_2_SCORE}})
3. {{TOP_JOB_3_STATEMENT}} (Opportunity Score: {{TOP_JOB_3_SCORE}})

**Key switch forces:** Push: {{DOMINANT_PUSH_SUMMARY}} | Pull: {{DOMINANT_PULL_SUMMARY}} | Primary barrier: {{PRIMARY_BARRIER_SUMMARY}}

**Strategic recommendation:** {{STRATEGIC_RECOMMENDATION}}

**Critical validation needed:** {{CRITICAL_VALIDATION_NEEDED}}
<!-- {{CRITICAL_VALIDATION_NEEDED}}: Identify the 1-2 most important findings that require validation against primary user data before informing design decisions. Format: "Validate [specific finding] via [validation method, e.g., switch interviews, behavioral analytics]." -->

> **Synthesis caveat:** All findings are AI-synthesized from secondary research and carry {{OVERALL_CONFIDENCE}} confidence by default. Treat as directional hypotheses requiring validation against primary user data before informing design decisions.

---

## L1: Job Inventory

<!-- Target: 3-7 main functional jobs per engagement (scope rule). -->
<!-- Jobs are split by type per agent definition required sections: Functional, Social, Emotional. -->
<!-- Classification decision procedure: check emotional language first, social second, default to functional. See jtbd-methodology-rules.md [Job Classification Rules]. -->

### Functional Jobs

<!-- REPEATABLE BLOCK: Duplicate this block for each identified FUNCTIONAL job. -->
<!-- Functional jobs answer: "What is the user trying to get done?" Outcome describes an observable action or result. -->

#### {{JOB_ID}}: {{JOB_TITLE}}

| Field | Value |
|-------|-------|
| **Job ID** | {{JOB_ID}} |
| **Job Statement** | "When I am {{SITUATION}}, I want to {{MOTIVATION}}, so I can {{EXPECTED_OUTCOME}}." |
| **Classification** | Functional |
| **Job Category** | {{JOB_CATEGORY}} |
| **Importance** | {{IMPORTANCE}} / 10 |
| **Satisfaction** | {{SATISFACTION}} / 10 |
| **Opportunity Score** | {{OPPORTUNITY_SCORE}} = {{IMPORTANCE}} + max({{IMPORTANCE}} - {{SATISFACTION}}, 0) |
| **Service Classification** | {{SERVICE_CLASSIFICATION}} |
<!-- Opportunity scoring thresholds: >=10 = Underserved (innovation opportunity), 6-9 = Appropriately served, <6 = Overserved. Source: Ulwick (2016) [Tier 2]. See jtbd-methodology-rules.md [Opportunity Scoring]. -->
| **Confidence** | {{JOB_CONFIDENCE}} |
| **Evidence Sources** | {{EVIDENCE_SOURCES}} |
<!-- Source format: "Source name (Year) [Tier 1|2|3]" per jtbd-methodology-rules.md [Source Authority Rules]. Tier 1=primary research data, Tier 2=published methodology, Tier 3=tertiary. Multiple sources: comma-separated. HARD rule: Tier 3 MUST NOT be the sole evidence source. -->

| Criterion | Measurement | Weight | Current Score |
|-----------|-------------|--------|---------------|
| {{CRITERION_1}} | {{MEASUREMENT_1}} | {{WEIGHT_1}} | {{SCORE_1}} / 10 |
| {{CRITERION_2}} | {{MEASUREMENT_2}} | {{WEIGHT_2}} | {{SCORE_2}} / 10 |
| {{CRITERION_3}} | {{MEASUREMENT_3}} | {{WEIGHT_3}} | {{SCORE_3}} / 10 |
<!-- Hiring criteria preview -- see L1: Hiring Criteria section for full criterion table with weights and thresholds. -->

<!-- END REPEATABLE BLOCK (Functional Job) -->

### Social Jobs

<!-- REPEATABLE BLOCK: Duplicate this block for each identified SOCIAL job. -->
<!-- Social jobs answer: "How does the user want to be perceived by others?" Outcome references reputation, status, belonging, or professional identity. -->

#### {{JOB_ID}}: {{JOB_TITLE}}

| Field | Value |
|-------|-------|
| **Job ID** | {{JOB_ID}} |
| **Job Statement** | "When I am {{SITUATION}}, I want to {{MOTIVATION}}, so I can {{EXPECTED_OUTCOME}}." |
| **Classification** | Social |
| **Job Category** | {{JOB_CATEGORY}} |
| **Importance** | {{IMPORTANCE}} / 10 |
| **Satisfaction** | {{SATISFACTION}} / 10 |
| **Opportunity Score** | {{OPPORTUNITY_SCORE}} = {{IMPORTANCE}} + max({{IMPORTANCE}} - {{SATISFACTION}}, 0) |
| **Service Classification** | {{SERVICE_CLASSIFICATION}} |
<!-- Opportunity scoring thresholds: >=10 = Underserved (innovation opportunity), 6-9 = Appropriately served, <6 = Overserved. Source: Ulwick (2016) [Tier 2]. See jtbd-methodology-rules.md [Opportunity Scoring]. -->
| **Confidence** | {{JOB_CONFIDENCE}} |
| **Evidence Sources** | {{EVIDENCE_SOURCES}} |
<!-- Source format: "Source name (Year) [Tier 1|2|3]" per jtbd-methodology-rules.md [Source Authority Rules]. Tier 1=primary research data, Tier 2=published methodology, Tier 3=tertiary. Multiple sources: comma-separated. HARD rule: Tier 3 MUST NOT be the sole evidence source. -->

| Criterion | Measurement | Weight | Current Score |
|-----------|-------------|--------|---------------|
| {{CRITERION_1}} | {{MEASUREMENT_1}} | {{WEIGHT_1}} | {{SCORE_1}} / 10 |
| {{CRITERION_2}} | {{MEASUREMENT_2}} | {{WEIGHT_2}} | {{SCORE_2}} / 10 |
| {{CRITERION_3}} | {{MEASUREMENT_3}} | {{WEIGHT_3}} | {{SCORE_3}} / 10 |
<!-- Hiring criteria preview -- see L1: Hiring Criteria section for full criterion table with weights and thresholds. -->

<!-- END REPEATABLE BLOCK (Social Job) -->

### Emotional Jobs

<!-- REPEATABLE BLOCK: Duplicate this block for each identified EMOTIONAL job. -->
<!-- Emotional jobs answer: "How does the user want to feel?" Outcome references an internal emotional state. -->

#### {{JOB_ID}}: {{JOB_TITLE}}

| Field | Value |
|-------|-------|
| **Job ID** | {{JOB_ID}} |
| **Job Statement** | "When I am {{SITUATION}}, I want to {{MOTIVATION}}, so I can {{EXPECTED_OUTCOME}}." |
| **Classification** | Emotional |
| **Job Category** | {{JOB_CATEGORY}} |
| **Importance** | {{IMPORTANCE}} / 10 |
| **Satisfaction** | {{SATISFACTION}} / 10 |
| **Opportunity Score** | {{OPPORTUNITY_SCORE}} = {{IMPORTANCE}} + max({{IMPORTANCE}} - {{SATISFACTION}}, 0) |
| **Service Classification** | {{SERVICE_CLASSIFICATION}} |
<!-- Opportunity scoring thresholds: >=10 = Underserved (innovation opportunity), 6-9 = Appropriately served, <6 = Overserved. Source: Ulwick (2016) [Tier 2]. See jtbd-methodology-rules.md [Opportunity Scoring]. -->
| **Confidence** | {{JOB_CONFIDENCE}} |
| **Evidence Sources** | {{EVIDENCE_SOURCES}} |
<!-- Source format: "Source name (Year) [Tier 1|2|3]" per jtbd-methodology-rules.md [Source Authority Rules]. Tier 1=primary research data, Tier 2=published methodology, Tier 3=tertiary. Multiple sources: comma-separated. HARD rule: Tier 3 MUST NOT be the sole evidence source. -->

| Criterion | Measurement | Weight | Current Score |
|-----------|-------------|--------|---------------|
| {{CRITERION_1}} | {{MEASUREMENT_1}} | {{WEIGHT_1}} | {{SCORE_1}} / 10 |
| {{CRITERION_2}} | {{MEASUREMENT_2}} | {{WEIGHT_2}} | {{SCORE_2}} / 10 |
| {{CRITERION_3}} | {{MEASUREMENT_3}} | {{WEIGHT_3}} | {{SCORE_3}} / 10 |
<!-- Hiring criteria preview -- see L1: Hiring Criteria section for full criterion table with weights and thresholds. -->

<!-- END REPEATABLE BLOCK (Emotional Job) -->

---

## L1: Opportunity Score Matrix

<!-- Formula: Opportunity Score = Importance + max(Importance - Satisfaction, 0). AI-synthesized estimates. -->

| Rank | Job ID | Job Statement (abbreviated) | Importance | Satisfaction | Opportunity Score | Service Classification |
|------|--------|----------------------------|------------|-------------|-------------------|------------------------|
| 1 | {{RANK_1_JOB_ID}} | {{RANK_1_STATEMENT}} | {{RANK_1_IMP}} | {{RANK_1_SAT}} | {{RANK_1_SCORE}} | {{RANK_1_CLASS}} |
| 2 | {{RANK_2_JOB_ID}} | {{RANK_2_STATEMENT}} | {{RANK_2_IMP}} | {{RANK_2_SAT}} | {{RANK_2_SCORE}} | {{RANK_2_CLASS}} |
| 3 | {{RANK_3_JOB_ID}} | {{RANK_3_STATEMENT}} | {{RANK_3_IMP}} | {{RANK_3_SAT}} | {{RANK_3_SCORE}} | {{RANK_3_CLASS}} |
| 4 | {{RANK_4_JOB_ID}} | {{RANK_4_STATEMENT}} | {{RANK_4_IMP}} | {{RANK_4_SAT}} | {{RANK_4_SCORE}} | {{RANK_4_CLASS}} |

<!-- Minimum 3 rows, maximum 7 per jtbd-methodology-rules.md [Scope Rules]. Add or remove rows to match actual job count. -->

---

## L1: Switch Force Analysis

<!-- REPEATABLE BLOCK: Duplicate this block for each main job analyzed for switch forces. -->

### Switch Forces: {{JOB_ID}} -- {{JOB_TITLE}}

| Force | Direction | Rating | Evidence Summary | Source |
|-------|-----------|--------|------------------|--------|
| **Push** (current pain) | Drives change | {{PUSH_RATING}} / 5 | {{PUSH_EVIDENCE}} | {{PUSH_SOURCE}} |
<!-- Rating scale: 1=Minimal (<3 instances), 2=Low (3-5 instances), 3=Moderate (6-10 instances), 4=Strong (10+ instances or 3+ source types), 5=Dominant (pervasive across all sources). See jtbd-methodology-rules.md [Switch Force Analysis Rules]. -->
<!-- Source format for {{PUSH_SOURCE}}: "Source name (Year) [Tier 1|2|3]" per jtbd-methodology-rules.md [Source Authority Rules]. -->
| **Pull** (new attraction) | Drives change | {{PULL_RATING}} / 5 | {{PULL_EVIDENCE}} | {{PULL_SOURCE}} |
<!-- Source format for {{PULL_SOURCE}}: "Source name (Year) [Tier 1|2|3]" per jtbd-methodology-rules.md [Source Authority Rules]. -->
| **Anxiety** (switching fear) | Resists change | {{ANXIETY_RATING}} / 5 | {{ANXIETY_EVIDENCE}} | {{ANXIETY_SOURCE}} |
<!-- Source format for {{ANXIETY_SOURCE}}: "Source name (Year) [Tier 1|2|3]" per jtbd-methodology-rules.md [Source Authority Rules]. -->
| **Habit** (inertia) | Resists change | {{HABIT_RATING}} / 5 | {{HABIT_EVIDENCE}} | {{HABIT_SOURCE}} |
<!-- Source format for {{HABIT_SOURCE}}: "Source name (Year) [Tier 1|2|3]" per jtbd-methodology-rules.md [Source Authority Rules]. -->

**Net Force:** ({{PUSH_RATING}} + {{PULL_RATING}}) - ({{ANXIETY_RATING}} + {{HABIT_RATING}}) = {{DRIVING_TOTAL}} - {{RESISTING_TOTAL}} = **{{NET_FORCE}}**

**Interpretation:** {{NET_FORCE_INTERPRETATION}}
<!-- {{NET_FORCE_INTERPRETATION}}: Positive net force: switching likely; focus on reducing remaining anxiety/habit barriers. Zero net force: uncertain; identify weakest resisting force to target. Negative net force: switching unlikely; must increase push/pull or decrease anxiety/habit. See jtbd-methodology-rules.md [Net Force Calculation] for strategic implications per sign. -->

<!-- END REPEATABLE BLOCK (Switch Force Analysis) -->

---

## L1: Job Map

<!-- Ulwick 8-step universal job process. Omitted steps noted with rationale. -->

<!-- REPEATABLE BLOCK: Duplicate this block for each main job mapped. -->

### Job Map: {{JOB_ID}} -- {{JOB_TITLE}}

| Step | Universal Process | Domain-Specific Action | Outcome Expectations | Importance | Satisfaction | Opportunity Score | Priority |
|------|------------------|----------------------|---------------------|------------|-------------|-------------------|----------|
| 1 | **Define** | {{DEFINE_ACTION}} | {{DEFINE_OUTCOMES}} | {{DEFINE_IMP}} | {{DEFINE_SAT}} | {{DEFINE_SCORE}} | {{DEFINE_PRI}} |
| 2 | **Locate** | {{LOCATE_ACTION}} | {{LOCATE_OUTCOMES}} | {{LOCATE_IMP}} | {{LOCATE_SAT}} | {{LOCATE_SCORE}} | {{LOCATE_PRI}} |
| 3 | **Prepare** | {{PREPARE_ACTION}} | {{PREPARE_OUTCOMES}} | {{PREPARE_IMP}} | {{PREPARE_SAT}} | {{PREPARE_SCORE}} | {{PREPARE_PRI}} |
| 4 | **Confirm** | {{CONFIRM_ACTION}} | {{CONFIRM_OUTCOMES}} | {{CONFIRM_IMP}} | {{CONFIRM_SAT}} | {{CONFIRM_SCORE}} | {{CONFIRM_PRI}} |
| 5 | **Execute** | {{EXECUTE_ACTION}} | {{EXECUTE_OUTCOMES}} | {{EXECUTE_IMP}} | {{EXECUTE_SAT}} | {{EXECUTE_SCORE}} | {{EXECUTE_PRI}} |
| 6 | **Monitor** | {{MONITOR_ACTION}} | {{MONITOR_OUTCOMES}} | {{MONITOR_IMP}} | {{MONITOR_SAT}} | {{MONITOR_SCORE}} | {{MONITOR_PRI}} |
| 7 | **Modify** | {{MODIFY_ACTION}} | {{MODIFY_OUTCOMES}} | {{MODIFY_IMP}} | {{MODIFY_SAT}} | {{MODIFY_SCORE}} | {{MODIFY_PRI}} |
| 8 | **Conclude** | {{CONCLUDE_ACTION}} | {{CONCLUDE_OUTCOMES}} | {{CONCLUDE_IMP}} | {{CONCLUDE_SAT}} | {{CONCLUDE_SCORE}} | {{CONCLUDE_PRI}} |

**Omitted steps:** {{OMITTED_STEPS_RATIONALE}}
<!-- Example: "Steps 3 (Prepare) and 7 (Conclude) were omitted because the product scope covers only the core execution phase, not setup or teardown." -->
<!-- Outcome formats (select appropriate type per step):
  Speed:   "Minimize the time it takes to [outcome]"
  Risk:    "Minimize the likelihood of [undesired outcome]"
  Success: "Increase the likelihood of [desired outcome]"
  Quality: "Minimize the variability of [quality measure]"
  Source: Ulwick ODI (2016) [Tier 2] via jtbd-methodology-rules.md [Opportunity Scoring Rules]
-->

<!-- END REPEATABLE BLOCK (Job Map) -->

---

## L1: Hiring Criteria

<!-- REPEATABLE BLOCK: Duplicate this block for each main job with hiring criteria (Phase 5). -->
<!-- Hiring criteria are the measurable attributes users evaluate when "hiring" a product for a specific job. -->
<!-- Weight scale: Deal-breaker=3, Important=2, Nice-to-have=1 per Phase 5 methodology in ux-jtbd-analyst.md. -->
<!-- Composite rank = sum(criterion_weight x criterion_score) / sum(weights). -->

### Hiring Criteria: {{JOB_ID}} -- {{JOB_TITLE}}

| Field | Value |
|-------|-------|
| **Job Statement** | "When I am {{SITUATION}}, I want to {{MOTIVATION}}, so I can {{EXPECTED_OUTCOME}}." |
| **Current Solution Hired** | {{CURRENT_SOLUTION}} |
<!-- Current solution: the product/approach/workaround users currently "hire" for this job. -->
| **Satisfaction with Current** | {{CURRENT_SATISFACTION}} / 10 |
<!-- Satisfaction with the currently hired solution on the 1-10 scale per jtbd-methodology-rules.md [Opportunity Scoring Rules]. -->
| **Firing Triggers** | {{FIRING_TRIGGERS}} |
<!-- Firing triggers: specific conditions under which users "fire" the current solution. Derived from push forces in Switch Force Analysis. -->
| **New Solution Hiring Criteria** | See table below |

| Criterion | Measurement | Weight | Min Threshold | Current Score |
|-----------|-------------|--------|---------------|---------------|
| {{HC_CRITERION_1}} | {{HC_MEASUREMENT_1}} | {{HC_WEIGHT_1}} | {{HC_MIN_THRESHOLD_1}} | {{HC_SCORE_1}} / 10 |
| {{HC_CRITERION_2}} | {{HC_MEASUREMENT_2}} | {{HC_WEIGHT_2}} | {{HC_MIN_THRESHOLD_2}} | {{HC_SCORE_2}} / 10 |
| {{HC_CRITERION_3}} | {{HC_MEASUREMENT_3}} | {{HC_WEIGHT_3}} | {{HC_MIN_THRESHOLD_3}} | {{HC_SCORE_3}} / 10 |

<!-- Weight values: 3=Deal-breaker, 2=Important, 1=Nice-to-have. -->
<!-- Deal-breaker classification rule: (1) opportunity score >= 15, OR (2) user explicitly states non-negotiable, OR (3) push rating >= 4 in switch force analysis. -->
<!-- Min Threshold: minimum acceptable performance on this criterion (1-10 scale). -->
<!-- Current Score: how well the current hired solution performs on this criterion (1-10 scale). -->
<!-- Composite rank: sum(weight x score) / sum(weights). Use for cross-job comparison of underserved hiring criteria. -->

**Composite Rank:** {{COMPOSITE_RANK}}

<!-- END REPEATABLE BLOCK (Hiring Criteria) -->

---

## L2: Synthesis and Prioritization

### Cross-Job Patterns

{{CROSS_JOB_PATTERNS}}
<!-- List 3-5 cross-job patterns (e.g., shared triggers, force patterns, underserved steps). -->

### Job Hierarchy

| Parent Job | Child Jobs | Relationship |
|-----------|------------|--------------|
| {{PARENT_JOB_ID}}: {{PARENT_JOB_TITLE}} | {{CHILD_JOB_IDS}} | {{RELATIONSHIP_DESC}} |

<!-- Max 2 levels. If none: "All identified jobs are independent (no parent-child relationships)." -->

### Recommended Focus Areas

| Priority | Job ID | Rationale | Recommended Action |
|----------|--------|-----------|-------------------|
| 1 | {{FOCUS_1_JOB_ID}} | {{FOCUS_1_RATIONALE}} | {{FOCUS_1_ACTION}} |
| 2 | {{FOCUS_2_JOB_ID}} | {{FOCUS_2_RATIONALE}} | {{FOCUS_2_ACTION}} |
| 3 | {{FOCUS_3_JOB_ID}} | {{FOCUS_3_RATIONALE}} | {{FOCUS_3_ACTION}} |

<!-- Prioritize by: opportunity score, force balance, job frequency. Ties: higher Importance > lower Satisfaction > broader segment. -->

### Innovation Trajectory

{{INNOVATION_TRAJECTORY}}
<!-- {{INNOVATION_TRAJECTORY}}: Describe where AI augmentation opportunities exist, competitive differentiation direction, and organizational recommendations. Include: (1) which underserved jobs point to innovation opportunities, (2) where demand-side gaps suggest new product categories or features, (3) recommendations for the team's next steps. 2-4 sentences. -->

---

## L2: Confidence Summary

| Job ID | Confidence | Justification | Validation Method |
|--------|-----------|---------------|-------------------|
| {{CONF_JOB_ID}} | {{CONF_LEVEL}} | {{CONF_JUSTIFICATION}} | {{CONF_VALIDATION_METHOD}} |
<!-- {{CONF_JUSTIFICATION}} Example: "Synthesized from competitor reviews (T2) and domain literature (T2); no direct user interview data (T1) available. Confidence limited by absence of primary research." -->
<!-- {{CONF_VALIDATION_METHOD}} Options: "Switch interviews", "Expert review", "Behavioral analytics correlation", "Support ticket analysis". Select the method that would most reduce uncertainty. Source: skills/ux-jtbd/SKILL.md [Synthesis Hypothesis Validation]. -->
<!-- REPEATABLE: One row per identified job. -->

**Overall:** {{OVERALL_CONFIDENCE}} -- HIGH: {{HIGH_CONF_COUNT}}/{{TOTAL_JOB_COUNT}}, MEDIUM: {{MEDIUM_CONF_COUNT}}/{{TOTAL_JOB_COUNT}}, LOW: {{LOW_CONF_COUNT}}/{{TOTAL_JOB_COUNT}}
<!-- If LOW > 50%: add low-confidence majority banner per synthesis-validation.md. -->

### P-022 Disclosure

> **Transparency statement:** This JTBD analysis was produced by the `ux-jtbd-analyst` agent using AI-augmented secondary research synthesis. All job statements, switch force assessments, and opportunity scores are derived from {{PRIMARY_EVIDENCE_TYPE}} and carry {{OVERALL_CONFIDENCE}} confidence. Traditional ODI research recommends N=50-200 respondents per user segment; this analysis operates below that threshold. All significant AI judgment calls are enumerated in the Synthesis Judgments Summary below.
<!-- {{PRIMARY_EVIDENCE_TYPE}}: describe the evidence types used, e.g., "secondary research (competitor reviews, domain literature)" or "limited primary data (3 user interviews) supplemented by secondary research". Source format: "Source name (Year) [Tier 1|2|3]" per jtbd-methodology-rules.md [Source Authority Rules]. -->

### Synthesis Judgments Summary

1. {{JUDGMENT_1}}
2. {{JUDGMENT_2}}
3. {{JUDGMENT_3}}

<!-- REQUIRED: Enumerate every AI inference. See jtbd-methodology-rules.md for examples. -->

### Validation Required

| Field | Value |
|-------|-------|
| **Validation status** | PENDING |
| **Required validation source** | {{VALIDATION_SOURCE}} |
| **Minimum threshold** | {{VALIDATION_THRESHOLD}} |
| **Recommended validation method** | {{VALIDATION_METHOD}} |

<!-- See synthesis-validation.md for MEDIUM->HIGH validation methods. -->

---

## Handoff Data

<!-- Handoff fields follow docs/schemas/handoff-v2.schema.json. Sub-skill extensions marked with [ux-ext]. -->

```yaml
from_agent: ux-jtbd-analyst
to_agent: "{{DOWNSTREAM_AGENT}}"
engagement_id: "{{ENGAGEMENT_ID}}"
task: "JTBD analysis for {{PRODUCT_NAME}} -- {{TOPIC}}"
success_criteria:
  - "Job statements in canonical format with classification and scoring"
  - "Switch forces assessed with Moesta four forces model"
  - "All findings cite evidence sources with tier classification"
artifacts:
  - "projects/${JERRY_PROJECT}/engagements/{{ENGAGEMENT_ID}}/ux-jtbd-analyst-{{TOPIC_SLUG}}.md"
key_findings:
  - "{{KEY_FINDING_1}}"
  - "{{KEY_FINDING_2}}"
  - "{{KEY_FINDING_3}}"
  - "{{KEY_FINDING_4}}"
blockers: {{BLOCKERS}}  # array per handoff-v2 schema; use [] if no blockers; prefix persistent blockers with "[PERSISTENT]". Example: ["[PERSISTENT] Missing primary user data"]
confidence: {{CONFIDENCE_NUMERIC_0_TO_1}}  # numeric 0.0-1.0 per handoff-v2.schema.json. Map from qualitative: HIGH=0.80-0.95, MEDIUM=0.50-0.79, LOW=0.15-0.49
criticality: "{{CRITICALITY}}"
job_count: {{TOTAL_JOB_COUNT}}
top_opportunity_score: {{TOP_OPPORTUNITY_SCORE}}
top_underserved_jobs:
  - job_id: "{{TOP_UNDERSERVED_1_ID}}"
    statement: "{{TOP_UNDERSERVED_1_STATEMENT}}"
    score: {{TOP_UNDERSERVED_1_SCORE}}
  - job_id: "{{TOP_UNDERSERVED_2_ID}}"
    statement: "{{TOP_UNDERSERVED_2_STATEMENT}}"
    score: {{TOP_UNDERSERVED_2_SCORE}}
switch_force_summary:
  dominant_push: "{{DOMINANT_PUSH_SUMMARY}}"
  dominant_pull: "{{DOMINANT_PULL_SUMMARY}}"
  primary_barrier: "{{PRIMARY_BARRIER_SUMMARY}}"
  net_force_direction: "{{NET_FORCE_DIRECTION}}"
```

---

*Template Version: 1.4.0 | /ux-jtbd Sub-Skill | PROJ-022 User Experience Skill*
*Methodology: Christensen JTBD (2016), Ulwick ODI (2016), Moesta Four Forces (2020)*
*Agent: ux-jtbd-analyst | Parent Skill: /user-experience*
