<!-- TEMPLATE: feature-priority-template.md | VERSION: 1.2.0 | DATE: 2026-03-04 -->
<!-- SKILL: /ux-kano-model | AGENT: ux-kano-analyst -->
<!-- SOURCE: SKILL.md v1.2.0 [Output Specification], agent <output> section v1.1.0, agent <methodology> Phase 5 -->
<!-- COMPANION: kano-survey-template.md v1.0.0 — produces the survey questionnaire that generates the response data analyzed in this report. -->
<!-- USAGE: Fill {{PLACEHOLDER}} fields. Copy REPEATABLE BLOCK markers for each feature, split feature, lifecycle entry, and judgment entry. See kano-methodology-rules.md for rule IDs. -->

# Kano Model Feature Classification: {{TOPIC}}

> **Engagement:** {{ENGAGEMENT_ID}}
> **Product:** {{PRODUCT_NAME}}
> **Date:** {{ANALYSIS_DATE}}
> **Analyst:** ux-kano-analyst
> **Respondent Count:** {{RESPONDENT_COUNT}}
> **Statistical Adequacy:** {{Anecdotal (1-4) | Directional (5-8) | Increasingly Stable (9-19) | Statistical (20+) | Segment-Capable (50+)}}

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | L0: Feature counts by category, top priorities, sample size disclosure |
| [Engagement Context](#engagement-context) | L1: Product, users, feature list source, survey details |
| [Feature Classification Table](#feature-classification-table) | L1: Per-feature category, response distribution, confidence |
| [CS Coefficient Analysis](#cs-coefficient-analysis) | L1: Per-feature Better/Worse coefficients |
| [Priority Matrix](#priority-matrix) | L1: Better vs. |Worse| scatter with quadrant assignments |
| [Split Classification Analysis](#split-classification-analysis) | L1: Features with no majority, resolution prompts |
| [Feature Lifecycle Assessment](#feature-lifecycle-assessment) | L2: Migration trajectories, competitive context |
| [Strategic Implications](#strategic-implications) | L2: Product maturity, competitive positioning, roadmap |
| [Synthesis Judgments Summary](#synthesis-judgments-summary) | L1: AI judgment calls for synthesis gate |
| [Handoff Data](#handoff-data) | L1: Structured data for downstream sub-skills |

---

## Executive Summary

| Category | Symbol | Count | Percentage |
|----------|--------|-------|------------|
| Must-be | M | {{N}} | {{N}}% |
| Performance | O | {{N}} | {{N}}% |
| Attractive | A | {{N}} | {{N}}% |
| Indifferent | I | {{N}} | {{N}}% |
| Reverse | R | {{N}} | {{N}}% |
| **Total** | -- | **{{TOTAL_FEATURES}}** | **100%** |

**Sample Size:** {{RESPONDENT_COUNT}} respondents -- {{Anecdotal (LOW) | Directional (MEDIUM) | Increasingly Stable (MEDIUM-HIGH) | Statistically reliable (HIGH) | Segment-Capable (Very High)}}

**Top Must-be Features:** 1. {{FEATURE}} 2. {{FEATURE}} 3. {{FEATURE}}

**Top Attractive Features:** 1. {{FEATURE}} 2. {{FEATURE}} 3. {{FEATURE}}

**Split Classifications:** {{N}} features require domain expert resolution.

**Overall Recommendation:**
1. Must-be gaps: {{features requiring immediate implementation}}
2. Performance investments: {{features for competitive parity}}
3. Attractive differentiators: {{features for differentiation}}
4. Deprioritize: {{Indifferent features to defer or drop}}

{{One additional sentence on confidence level and validation needs.}}

<!-- SSC-004: When respondent count < 20, the following blockquote MUST be rendered (remove the conditional comment wrapper). -->
> **Note (if < 20 respondents):** Classification based on {{RESPONDENT_COUNT}} respondents (directional). Berger et al. (1993) recommend >= 20 for statistical reliability.

---

## Engagement Context

**Product:** {{PRODUCT_NAME}} | **Domain:** {{PRODUCT_DOMAIN}} | **Target Users:** {{TARGET_USER_DESCRIPTION}}
**Feature List Source:** {{SOURCE_DESCRIPTION}} | **Survey Administration:** {{METHOD_DESCRIPTION}}

| Source Sub-Skill | Artifact | Key Inputs Used |
|-----------------|----------|-----------------|
| {{sub-skill name or "None"}} | {{artifact path or "N/A"}} | {{what was extracted}} |
<!-- REPEATABLE ROW: Add one row per upstream sub-skill (e.g., /ux-jtbd, /ux-heuristic-eval). -->

<!-- If JTBD upstream data present: map push forces -> expected Must-be candidates, pull forces -> expected Attractive candidates. Note divergences between JTBD-predicted categories and actual Kano classifications in the Synthesis Judgments Summary (Feature Classification judgment type). -->

---

## Feature Classification Table

<!-- EVT-001/002: Canonical 5x5 table applied. EVT-004: R/Q retained in display. SPL-005: Flag [QUESTION CLARITY ISSUE] when Q > 10% for any feature. SPL-006: Flag [DOMAIN EXPERT REQUIRED] and note user-segment disagreement when R > 20% for any feature. -->

| Feature | Majority | M | O | A | I | R | Q | M% | O% | A% | I% | R% | Q% | Confidence | Split? |
|---------|----------|---|---|---|---|---|---|----|----|----|----|----|----|----|--------|
| {{FEATURE_NAME}} | {{M/O/A/I/R}} | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} | {{%}} | {{%}} | {{%}} | {{%}} | {{%}} | {{%}} | {{HIGH/MEDIUM/LOW}} | {{Y/N}} |
<!-- REPEATABLE ROW: Copy for each feature. Order: Must-be, Performance, Attractive, Indifferent, Reverse. -->

---

## CS Coefficient Analysis

<!-- CSC-001: R/Q excluded from denominator. CSC-004: Show counts. CSC-005: Display coefficients to 2 decimal places; retain full precision in handoff YAML. SPL-004: Split features included; mark Rank cell with [SPLIT] indicator. Better=(A+O)/(A+O+M+I), Worse=-(O+M)/(A+O+M+I). -->

| Feature | A | O | M | I | R(excl) | Q(excl) | Better | Worse | |Worse| | Quadrant | Rank |
|---------|---|---|---|---|---------|---------|--------|-------|--------|----------|------|
| {{FEATURE_NAME}} | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} | {{0.00}} | {{-0.00}} | {{0.00}} | {{Attractive/Performance/Must-be/Indifferent}} | {{N}} |
<!-- REPEATABLE ROW: Copy for each feature. Order by Rank ascending. SPL-004: If this feature has a split classification, append [SPLIT] to the Rank cell. -->

---

## Priority Matrix

<!-- PMC-001: Better x-axis, |Worse| y-axis. PMC-002: All 4 quadrants labeled. PMC-007: Flag [CATEGORY-QUADRANT MISMATCH] when majority category from 5x5 table differs from CS-derived quadrant. Note: y-axis top = High |Worse| (conventional orientation); kano-methodology-rules.md PMC table uses different directional labeling but identical strategic interpretation. -->

```
        |Worse| (dissatisfaction risk)
    1.0 |  Must-be              Performance
        |  (implement now)      (stay competitive)
    0.5 |-------------------------------------------
        |  Indifferent          Attractive
        |  (deprioritize)       (differentiate)
    0.0 +-------------------------------------------
       0.0               0.5                 1.0
              Better (satisfaction potential)
```

| Feature | Better | |Worse| | Quadrant | Boundary? | Mismatch? | Notes |
|---------|--------|--------|----------|-----------|-----------|-------|
| {{FEATURE_NAME}} | {{0.00}} | {{0.00}} | {{Quadrant}} | {{Y/N}} | {{Y/N}} | {{notes}} |
<!-- REPEATABLE ROW: Copy for each feature. PMC-004: Flag within 0.05 of 0.5 threshold. PMC-007: Set Mismatch?=Y and add [CATEGORY-QUADRANT MISMATCH] in Notes when majority category from 5x5 table differs from CS-derived quadrant. -->

**Priority Ranking:** Must-be (|Worse| desc) > Performance (|Worse| desc) > Attractive (Better desc) > Indifferent

| Rank | Feature | Category | Action |
|------|---------|----------|--------|
| {{N}} | {{FEATURE_NAME}} | {{Category}} | {{Action}} |
<!-- REPEATABLE ROW: Copy for each feature. PMC-006 ordering. -->

---

## Split Classification Analysis

<!-- SPL-001: No single category > 50%. If none: "No split classifications detected." SPL-002: Flag with [SPLIT CLASSIFICATION] marker; show full M/O/A/I/R/Q distribution. SPL-003: Include [DOMAIN EXPERT REQUIRED] with top 2 competing categories and resolution criteria. -->

<!-- REPEATABLE BLOCK: [SPLIT CLASSIFICATION] FEATURE START -->
### [SPLIT CLASSIFICATION] {{FEATURE_NAME}}

| Category | Count | Percentage |
|----------|-------|------------|
| M | {{n}} | {{%}} |
| O | {{n}} | {{%}} |
| A | {{n}} | {{%}} |
| I | {{n}} | {{%}} |
| R | {{n}} | {{%}} |
| Q | {{n}} | {{%}} |

**Top Competing:** {{CATEGORY_1}} ({{%}}) vs. {{CATEGORY_2}} ({{%}})

**CS Coefficients (provisional):** Better={{0.00}}, |Worse|={{0.00}}, Quadrant={{Quadrant}} (treat as directional pending resolution).

**[DOMAIN EXPERT REQUIRED]** {{Resolution prompt with context-specific criteria: present competing categories, suggest resolution criteria (e.g., "This feature splits between {{CATEGORY_1}} and {{CATEGORY_2}}. Consider: Is competitive pressure making this an expected feature?"). Cite SPL-003.}}
<!-- REPEATABLE BLOCK: [SPLIT CLASSIFICATION] FEATURE END -->

---

## Feature Lifecycle Assessment

<!-- LCY-001: Only with product history. LCY-002: MEDIUM confidence. If no history: "Insufficient product history for lifecycle assessment." -->

| Feature | Current | Prior | Prior Date | Migration | Stage | Re-evaluate |
|---------|---------|-------|-----------|-----------|-------|-------------|
| {{FEATURE_NAME}} | {{M/O/A/I/R}} | {{M/O/A/I/R}} | {{DATE}} | {{A->O / Stable}} | {{Early/Transitioning/Mature}} | {{interval}} |
<!-- REPEATABLE ROW: Features with lifecycle data only. -->

Migration: Attractive -> Performance -> Must-be (Kano et al., 1984; Matzler & Hinterhuber, 1998).

---

## Strategic Implications

**Product Maturity:** {{Assessment based on category distribution: high Must-be% = mature market; high Attractive% = emerging market; balanced = competitive.}}

**Competitive Positioning:** {{Must-be = table stakes (absence loses customers), Attractive = differentiators (presence wins customers), Performance = battleground (competitive parity).}}

**Roadmap Implications:**
1. Must-be prerequisites: {{features with highest |Worse| in Must-be quadrant}}
2. Performance investments: {{features in Performance quadrant, ranked by |Worse| desc}}
3. Attractive differentiators: {{features in Attractive quadrant, ranked by Better desc}}
4. Deprioritize: {{Indifferent features}}

**Investment Rationale:** {{Cite: Feature X (Better={{N}}, |Worse|={{N}}, {{Quadrant}}) justifies {{investment level}} because {{competitive/satisfaction rationale}}. Feature Y (Better={{N}}, |Worse|={{N}}, {{Quadrant}}) justifies {{deprioritize/defer}} because {{low impact rationale}}.}}

---

## Synthesis Judgments Summary

<!-- CLS-001: Every AI judgment with confidence and rationale. -->

| # | Judgment Type | Decision | Rationale | Confidence |
|---|--------------|----------|-----------|------------|
| 1 | Feature classification | {{decision}} | {{rationale}} | {{HIGH/MEDIUM/LOW}} |
| 2 | CS interpretation | {{decision}} | {{rationale}} | {{HIGH/MEDIUM/LOW}} |
| 3 | Priority ranking | {{decision}} | {{rationale}} | {{HIGH/MEDIUM/LOW}} |
| 4 | Split resolution | {{decision}} | {{rationale}} | {{HIGH/MEDIUM/LOW}} |
| 5 | Lifecycle stage | {{decision}} | {{rationale}} | {{HIGH/MEDIUM/LOW}} |
<!-- REPEATABLE ROW: One per AI judgment call. -->

**Confidence:** HIGH = 20+ respondents, clear majority, convergent. MEDIUM = directional, CS interpretation, lifecycle. LOW = split resolution, priority conflict; `[DOMAIN EXPERT REQUIRED]`.

**Sample size (P-022):** {{RESPONDENT_COUNT}} respondents, {{adequacy tier}}. Single AI analyst -- 5x5 table is deterministic; split resolution and lifecycle timing require domain expertise. Validate with product managers before roadmap commitments.

---

## Handoff Data

| Feature | Category | Better | |Worse| | Quadrant | Confidence | Split? |
|---------|----------|--------|--------|----------|------------|--------|
| {{FEATURE_NAME}} | {{M/O/A/I/R}} | {{0.00}} | {{0.00}} | {{Quadrant}} | {{HIGH/MEDIUM/LOW}} | {{Y/N}} |
<!-- REPEATABLE ROW: All classified features. Split features flagged for domain expert resolution. -->

```yaml
# handoff-v2 + ux_ext
from_agent: ux-kano-analyst                            # [handoff-v2]
to_agent: ux-orchestrator                              # [handoff-v2]
task: "Kano feature classification for {{TOPIC}}"      # [handoff-v2]
success_criteria:                                      # [handoff-v2]
  - "All features classified using canonical 5x5 evaluation table"
  - "CS coefficients calculated with R/Q exclusion"
  - "Priority matrix with 4 quadrants labeled"
  - "Sample size disclosure with confidence tier"
artifacts:                                             # [handoff-v2]
  - "projects/${JERRY_PROJECT}/engagements/{{ENGAGEMENT_ID}}/ux-kano-analyst-{{TOPIC_SLUG}}.md"
key_findings:                                          # [handoff-v2]
  - "{{finding 1}}"
  - "{{finding 2}}"
  - "{{finding 3}}"
blockers: []                                           # [handoff-v2]
confidence: {{0.0-1.0}}                                # [handoff-v2]
criticality: {{C1/C2/C3/C4}}                           # [handoff-v2]
# --- ux_ext ---
engagement_id: {{ENGAGEMENT_ID}}                       # [ux-ext]
feature_count: {{N}}                                   # [ux-ext]
respondent_count: {{N}}                                # [ux-ext]
statistical_adequacy: "{{directional|statistical}}"    # [ux-ext]
category_distribution:                                 # [ux-ext]
  must_be: {{N}}
  performance: {{N}}
  attractive: {{N}}
  indifferent: {{N}}
  reverse: {{N}}
split_count: {{N}}                                     # [ux-ext]
conflict_count: {{N}}                                  # [ux-ext]
sample_size_confidence: "{{HIGH|MEDIUM|LOW}}"          # [ux-ext]
lifecycle_features_assessed: {{N}}                     # [ux-ext]
artifact_path: "projects/${JERRY_PROJECT}/engagements/{{ENGAGEMENT_ID}}/ux-kano-analyst-{{TOPIC_SLUG}}.md"
handoff_features_count: {{N}}                          # [ux-ext]
feature_classifications:                               # [ux-ext] per-feature detail per SKILL.md Handoff Data
  - feature: "{{FEATURE_NAME}}"                        # REPEATABLE per classified feature
    category: "{{M/O/A/I/R}}"
    confidence: "{{HIGH/MEDIUM/LOW}}"
    better: {{0.00}}
    worse: {{-0.00}}
    quadrant: "{{Attractive/Performance/Must-be/Indifferent}}"
```

---

*Template Version: 1.2.0 | /ux-kano-model Sub-Skill | PROJ-022 User Experience Skill*
*Methodology: Kano et al. (1984). Berger et al. (1993). Matzler & Hinterhuber (1998).*
*Rules: `skills/ux-kano-model/rules/kano-methodology-rules.md`*
*Handoff schema: `docs/schemas/handoff-v2.schema.json`*
