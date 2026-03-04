# ps-critic Scoring Rubric and Evaluation Criteria

> Complete evaluation criteria framework, quality score calculation, and improvement feedback format for the ps-critic agent.

## Evaluation Criteria Framework

> **SSOT Reference:** The authoritative quality dimensions and weights are defined in `.context/rules/quality-enforcement.md` (Quality Gate section). Use those for C2+ deliverables.

### SSOT Quality Dimensions (C2+ Deliverables -- REQUIRED)

Per the SSOT, C2+ deliverables MUST use these dimensions and weights:

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Completeness | 0.20 | Does output address all requirements? |
| Internal Consistency | 0.20 | Are claims, data, and conclusions mutually consistent? |
| Methodological Rigor | 0.20 | Does the approach follow established methods? |
| Evidence Quality | 0.15 | Are claims supported by credible evidence? |
| Actionability | 0.15 | Can output be acted upon with clear next steps? |
| Traceability | 0.10 | Can claims be traced to sources and requirements? |

### Legacy Quality Dimensions (C1 Deliverables)

For C1 (Routine) deliverables, these simplified dimensions MAY be used:

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Completeness | 0.25 | Does output address all requirements? |
| Accuracy | 0.25 | Is information correct and verifiable? |
| Clarity | 0.20 | Is output clear and understandable? |
| Actionability | 0.15 | Can output be acted upon? |
| Alignment | 0.15 | Does output align with goals/constraints? |

### Custom Criteria

When custom criteria are provided in the invocation, use those instead:

```yaml
evaluation_criteria:
  - name: "{criterion_name}"
    weight: {0.0-1.0}
    description: "{what_to_evaluate}"
    scoring_rubric:
      excellent: "{0.9-1.0 criteria}"
      good: "{0.7-0.89 criteria}"
      acceptable: "{0.5-0.69 criteria}"
      needs_work: "{0.3-0.49 criteria}"
      poor: "{0.0-0.29 criteria}"
```

## Quality Score Calculation

**Formula:** `quality_score = Σ(criterion_score × criterion_weight)`

**Example:**
```
Completeness:  0.80 × 0.25 = 0.200
Accuracy:      0.90 × 0.25 = 0.225
Clarity:       0.85 × 0.20 = 0.170
Actionability: 0.70 × 0.15 = 0.105
Alignment:     0.95 × 0.15 = 0.143
─────────────────────────────────
Total Quality Score:       0.843
```

**Threshold Interpretation (C2+ deliverables per SSOT H-13):**
| Score Range | Assessment | Recommendation |
|-------------|------------|----------------|
| 0.92 - 1.00 | EXCELLENT | Accept -- quality gate PASSED |
| 0.85 - 0.91 | GOOD | Revision REQUIRED to meet threshold (0.92) |
| 0.70 - 0.84 | ACCEPTABLE | Revision required -- significant gaps |
| 0.50 - 0.69 | NEEDS_WORK | Major revision required |
| 0.00 - 0.49 | POOR | Fundamental revision required |

**Note:** The acceptance threshold for C2+ deliverables is >= 0.92 (SSOT H-13), not 0.85. The 0.85 threshold is legacy and applies only to C1 deliverables.

## Improvement Feedback Format

Each improvement area MUST follow this structure:

```markdown
### Improvement Area: {Area Name}

| Attribute | Value |
|-----------|-------|
| **Criterion** | {which criterion this affects} |
| **Current Score** | {0.0-1.0} |
| **Target Score** | {0.0-1.0} |
| **Priority** | HIGH / MEDIUM / LOW |

**Gap Description:** {specific issue identified}

**Evidence:**
{quote or reference from artifact showing the gap}

**Recommendation:**
{specific, actionable steps to improve}

**Expected Impact:**
{how addressing this will improve the quality score}
```
