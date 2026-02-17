# TASK-002: Enforce Token Budget for Preamble

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical guidance |
| [Time Tracking](#time-tracking) | Effort estimates and actuals |
| [Related Items](#related-items) | Cross-references and dependencies |
| [Evidence](#evidence) | Proof of completion |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-002"
work_type: TASK
title: "Enforce Token Budget for Preamble"
description: |
  Ensure the quality context preamble stays under 700 tokens to avoid
  excessive L1 context consumption. The generator validates content
  length and trims if necessary.
classification: ENABLER
status: DONE
resolution: null
priority: MEDIUM
assignee: ""
created_by: "Claude"
created_at: "2026-02-14"
updated_at: "2026-02-14"
parent_id: "EN-706"
tags:
  - "token-budget"
  - "preamble"
  - "L1"
  - "optimization"
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Summary

Implement token budget enforcement for the session start quality preamble. The preamble must stay under 700 tokens to avoid excessive L1 context consumption. The `SessionQualityContextGenerator` must validate content length after assembly and trim content if it exceeds the budget. Token counting uses an approximate heuristic since exact tokenization depends on the model.

## Acceptance Criteria

- [ ] Token counting implemented (approximate heuristic: ~0.75 tokens per word)
- [ ] Budget validation runs after preamble assembly
- [ ] Content trimmed if exceeding 700-token budget
- [ ] Trimming follows priority order (least important sections trimmed first)
- [ ] Budget validation result accessible for testing and diagnostics
- [ ] Warning logged if preamble approaches budget limit (>90%)

## Implementation Notes

- Token counting heuristic: split on whitespace, multiply by 1.33 (average tokens per word)
- Alternative: count characters and divide by 4 (rough approximation)
- Trimming priority (trim from bottom): strategy encodings details > criticality details > constitutional details > quality gate (never trim)
- The 700-token budget is defined in EN-706's technical approach
- Consider making the budget configurable for future tuning
- Add a `token_count` property to the generator for diagnostics

**Design Source:** EN-706 Technical Approach section (700-token budget requirement)

## Related Items

- Parent: [EN-706: SessionStart Quality Context Enhancement](EN-706-sessionstart-quality-context.md)
- Depends on: TASK-001 (generator class produces the content to budget-check)
- Related: EN-705 TASK-002 (same budget pattern with 600-token limit)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | — |
| Remaining Work | 0 hours |
| Time Spent | — |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| _None yet_ | — | — |

### Verification

- [ ] Acceptance criteria verified
- [ ] Code review passed
- [ ] Reviewed by: _pending_

---

## History

| Date | Status | Notes |
|------------|-------------|--------------------------------|
| 2026-02-14 | Created | Initial creation |
