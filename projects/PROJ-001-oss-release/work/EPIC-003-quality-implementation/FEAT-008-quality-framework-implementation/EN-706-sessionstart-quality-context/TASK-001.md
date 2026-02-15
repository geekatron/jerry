# TASK-001: Create SessionQualityContextGenerator Class

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
id: "TASK-001"
work_type: TASK
title: "Create SessionQualityContextGenerator Class"
description: |
  Create the SessionQualityContextGenerator class in
  src/infrastructure/internal/enforcement/session_quality_context_generator.py.
  Assembles the XML quality preamble with 4 sections: quality gate,
  constitutional principles, adversarial strategies, and decision criticality.
classification: ENABLER
status: DONE
resolution: null
priority: HIGH
assignee: ""
created_by: "Claude"
created_at: "2026-02-14"
updated_at: "2026-02-14"
parent_id: "EN-706"
tags:
  - "enforcement"
  - "session-start"
  - "L1"
  - "preamble"
  - "quality-context"
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Summary

Create the `SessionQualityContextGenerator` class that assembles the XML quality preamble for injection at session start. The preamble contains 4 structured sections: (1) Quality Gate -- 0.92 threshold, creator-critic-revision cycle with minimum 3 iterations, scoring rubric reference; (2) Constitutional Principles -- P-003 (No Recursive Subagents), P-020 (User Authority), P-022 (No Deception); (3) Adversarial Strategy Encodings -- S-001 through S-014 with brief descriptions; (4) Decision Criticality Definitions -- C1 through C4 with escalation rules. This class keeps enforcement logic separated from the session start hook infrastructure per hexagonal architecture.

## Acceptance Criteria

- [ ] `SessionQualityContextGenerator` class created in `src/infrastructure/internal/enforcement/session_quality_context_generator.py`
- [ ] Generator produces XML-structured `<quality-context>` block
- [ ] Quality Gate section includes 0.92 threshold and creator-critic-revision cycle
- [ ] Constitutional Principles section includes P-003, P-020, P-022
- [ ] Adversarial Strategy Encodings section includes S-001 through S-014
- [ ] Decision Criticality Definitions section includes C1 through C4 with escalation rules
- [ ] Generator has a `generate()` method returning the complete preamble string
- [ ] Class follows hexagonal architecture (no CLI/hook dependencies)

## Implementation Notes

- Location: `src/infrastructure/internal/enforcement/session_quality_context_generator.py`
- Use XML structure for the preamble (Claude parses XML effectively)
- Each section should be a sub-element of `<quality-context>`
- Strategy encodings can be brief (identifier + one-line description)
- Decision criticality definitions:
  - C1: Reversible, low impact -- proceed without escalation
  - C2: Reversible, moderate impact -- document decision
  - C3: Irreversible, moderate impact -- seek review
  - C4: Irreversible, high impact -- require explicit user approval
- Consider using string templates or f-strings for content assembly

**Design Source:** EPIC-002 EN-403/TASK-004 (SessionStart design), EN-405/TASK-006 (preamble content)

## Related Items

- Parent: [EN-706: SessionStart Quality Context Enhancement](EN-706-sessionstart-quality-context.md)
- Related: TASK-002 (token budget enforcement)
- Related: TASK-003 (hook integration)
- Related: EN-705 TASK-002 (PromptReinforcementEngine -- similar preamble pattern for L2)

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
