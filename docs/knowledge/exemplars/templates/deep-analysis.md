# {Analysis Type}: {Topic}

> **PS:** {PS_ID}
> **Exploration:** {ENTRY_ID}
> **Created:** {DATE}
> **Status:** ANALYSIS
> **Agent:** ps-analyst
> **Type:** {ANALYSIS_TYPE}

---

## Executive Summary

<!-- 2-3 paragraphs summarizing the analysis, key findings, and primary recommendation -->

{summary}

---

## Analysis Scope & Method

### Scope

| Dimension | Value |
|-----------|-------|
| Subject | {what_is_being_analyzed} |
| Boundaries | {in_scope_vs_out_of_scope} |
| Timeframe | {temporal_scope} |
| Data Sources | {sources_consulted} |

### Method

<!-- Describe the analytical frameworks applied -->

| Framework | Purpose | Applied To |
|-----------|---------|------------|
| 5 Whys | Root cause identification | {problem_area} |
| Trade-off Matrix | Option comparison | {decision_area} |
| Gap Analysis | Current vs desired | {capability_area} |
| FMEA | Risk assessment | {system_area} |

---

## Root Cause Analysis (5 Whys)

<!-- Applied when type is root-cause or investigation -->

### Problem Statement

{clear_problem_statement}

### 5 Whys Table

| Level | Question | Answer | Evidence |
|-------|----------|--------|----------|
| Why 1 | Why is {symptom}? | {answer_1} | {evidence_1} |
| Why 2 | Why is {answer_1}? | {answer_2} | {evidence_2} |
| Why 3 | Why is {answer_2}? | {answer_3} | {evidence_3} |
| Why 4 | Why is {answer_3}? | {answer_4} | {evidence_4} |
| Why 5 | Why is {answer_4}? | **ROOT CAUSE:** {root_cause} | {evidence_5} |

### Root Cause Determination

**Primary Root Cause:** {root_cause}

**Contributing Factors:**
1. {factor_1}
2. {factor_2}
3. {factor_3}

---

## Trade-off Analysis

<!-- Applied when type is trade-off or decision-support -->

### Options Considered

| Option | Description |
|--------|-------------|
| {option_1} | {description_1} |
| {option_2} | {description_2} |
| {option_3} | {description_3} |

### Evaluation Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| {criterion_1} | {weight_1} | {description_1} |
| {criterion_2} | {weight_2} | {description_2} |
| {criterion_3} | {weight_3} | {description_3} |
| {criterion_4} | {weight_4} | {description_4} |

### Trade-off Matrix

| Criterion (Weight) | {Option 1} | {Option 2} | {Option 3} |
|--------------------|------------|------------|------------|
| {C1} ({W1}) | {score} | {score} | {score} |
| {C2} ({W2}) | {score} | {score} | {score} |
| {C3} ({W3}) | {score} | {score} | {score} |
| {C4} ({W4}) | {score} | {score} | {score} |
| **Weighted Total** | **{total}** | **{total}** | **{total}** |

### Recommendation

**Recommended Option:** {recommended_option}

**Rationale:** {why_this_option}

---

## Gap Analysis

<!-- Applied when type is gap or assessment -->

### Current State

| Aspect | Current Status | Evidence |
|--------|---------------|----------|
| {aspect_1} | {current_1} | {evidence_1} |
| {aspect_2} | {current_2} | {evidence_2} |
| {aspect_3} | {current_3} | {evidence_3} |

### Desired State

| Aspect | Desired Status | Success Criteria |
|--------|---------------|------------------|
| {aspect_1} | {desired_1} | {criteria_1} |
| {aspect_2} | {desired_2} | {criteria_2} |
| {aspect_3} | {desired_3} | {criteria_3} |

### Gap Summary

| Aspect | Gap Description | Priority | Effort |
|--------|-----------------|----------|--------|
| {aspect_1} | {gap_1} | HIGH/MEDIUM/LOW | S/M/L |
| {aspect_2} | {gap_2} | HIGH/MEDIUM/LOW | S/M/L |
| {aspect_3} | {gap_3} | HIGH/MEDIUM/LOW | S/M/L |

---

## Risk Assessment

<!-- Applied when type includes risk evaluation -->

### Risk Matrix (FMEA Format)

| ID | Failure Mode | Effect | Cause | Severity (1-10) | Occurrence (1-10) | Detection (1-10) | RPN |
|----|--------------|--------|-------|-----------------|-------------------|------------------|-----|
| R1 | {mode_1} | {effect_1} | {cause_1} | {S} | {O} | {D} | {RPN} |
| R2 | {mode_2} | {effect_2} | {cause_2} | {S} | {O} | {D} | {RPN} |
| R3 | {mode_3} | {effect_3} | {cause_3} | {S} | {O} | {D} | {RPN} |

**RPN = Severity x Occurrence x Detection** (Higher = More Risk)

### High-Risk Items (RPN > 100)

| Risk | Current RPN | Mitigation | Residual RPN |
|------|-------------|------------|--------------|
| {risk_1} | {current} | {mitigation} | {residual} |

---

## Conclusions

### Key Findings

1. **{Finding 1}:** {description}
2. **{Finding 2}:** {description}
3. **{Finding 3}:** {description}

### Implications

{what_these_findings_mean_for_the_project}

---

## Recommendations

| Priority | Recommendation | Rationale | Effort | Impact |
|----------|---------------|-----------|--------|--------|
| HIGH | {recommendation_1} | {why} | S/M/L | HIGH/MED/LOW |
| HIGH | {recommendation_2} | {why} | S/M/L | HIGH/MED/LOW |
| MEDIUM | {recommendation_3} | {why} | S/M/L | HIGH/MED/LOW |

### Recommended Next Steps

1. {step_1}
2. {step_2}
3. {step_3}

---

## PS Integration

| Action | Command | Status |
|--------|---------|--------|
| Exploration Entry | `add-entry {PS_ID} "{topic}"` | Done ({ENTRY_ID}) |
| Entry Type | `--type ANALYSIS` | Done |
| Artifact Link | `link-artifact {PS_ID} {ENTRY_ID} FILE "docs/analysis/..."` | {PENDING/Done} |

---

**Generated by:** ps-analyst agent
**Template Version:** 1.0 (Phase 38.17)
**Prior Art:** Toyota 5 Whys, NASA FMEA, Kepner-Tregoe Decision Analysis