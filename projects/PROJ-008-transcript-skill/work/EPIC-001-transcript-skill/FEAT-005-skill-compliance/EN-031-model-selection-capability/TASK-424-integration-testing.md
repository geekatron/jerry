# TASK-424: Integration testing with different models

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "TASK-424"
work_type: TASK
title: "Integration testing with different models"
status: BACKLOG
priority: MEDIUM
assignee: "Claude"
created_at: "2026-01-30T16:00:00Z"
parent_id: "EN-031"
effort: 8
activity: TESTING
```

---

## Description

Run integration tests with different model combinations to validate model selection works correctly and measure quality/cost tradeoffs.

**Test scope:**
- Model parameter passthrough to Task tool
- Profile resolution
- Quality comparison across model configurations
- Cost measurement

**Depends on:** TASK-420, TASK-422, TASK-423

---

## Acceptance Criteria

- [ ] All model combinations produce valid output
- [ ] Economy profile completes successfully (all haiku)
- [ ] Quality profile produces higher extraction quality
- [ ] Cost measurements documented per profile
- [ ] Quality regression thresholds established

---

## Implementation Notes

### Test Matrix

| Test Case | Profile | Expected Outcome |
|-----------|---------|------------------|
| T-001 | economy | Valid output, lower quality OK |
| T-002 | balanced | Valid output, baseline quality |
| T-003 | quality | Valid output, highest quality |
| T-004 | custom (mixed) | Valid output |
| T-005 | invalid model | Clear error message |

### Test Transcript

Use standard test transcript:
- `skills/transcript/test_data/validation/live-test-internal-sample/`

### Quality Metrics to Measure

| Metric | Description |
|--------|-------------|
| Extraction precision | Correct entities / extracted entities |
| Extraction recall | Correct entities / total entities in source |
| Confidence scores | Average confidence of extractions |
| ps-critic score | Overall quality score |

### Expected Quality by Profile

| Profile | Expected ps-critic Score | Notes |
|---------|-------------------------|-------|
| economy | >= 0.80 | May have lower extraction quality |
| balanced | >= 0.90 | Baseline threshold |
| quality | >= 0.95 | Highest quality |

### Test Commands

```bash
# Economy profile test
uv run jerry transcript parse test.vtt --profile economy --output-dir /tmp/economy

# Balanced profile test
uv run jerry transcript parse test.vtt --profile balanced --output-dir /tmp/balanced

# Quality profile test
uv run jerry transcript parse test.vtt --profile quality --output-dir /tmp/quality

# Compare outputs
diff /tmp/economy/extraction-report.json /tmp/quality/extraction-report.json
```

### Cost Measurement

Record API costs for each profile:
- Token counts (input/output per agent)
- Total cost per run
- Cost per 1000 segments processed

---

## Related Items

- Parent: [EN-031: Model Selection Capability](./EN-031-model-selection-capability.md)
- Depends on: TASK-420, TASK-422, TASK-423
- Test data: skills/transcript/test_data/validation/

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Test results | Report | test_data/validation/model-selection-tests/ |
| Cost analysis | Report | docs/analysis/model-selection-cost.md |

### Verification

- [ ] All profiles produce valid output
- [ ] Quality thresholds documented
- [ ] Cost data captured
- [ ] Regression thresholds established

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation per EN-031 |
