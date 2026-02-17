# TASK-002: Create PromptReinforcementEngine Class

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
title: "Create PromptReinforcementEngine Class"
description: |
  Create the PromptReinforcementEngine class in
  src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py.
  Extracts L2-REINJECT content from rules, assembles the reinforcement
  preamble, enforces the 600-token budget constraint, and returns
  structured reinforcement content.
classification: ENABLER
status: DONE
resolution: null
priority: CRITICAL
assignee: ""
created_by: "Claude"
created_at: "2026-02-14"
updated_at: "2026-02-14"
parent_id: "EN-705"
tags:
  - "enforcement"
  - "prompt-reinforcement"
  - "L2"
  - "context-rot"
  - "V-024"
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Summary

Create the `PromptReinforcementEngine` class that contains all L2 Per-Prompt Reinforcement logic, separated from the hook adapter per hexagonal architecture. The engine is responsible for: extracting L2-REINJECT content from rules files, assembling the reinforcement preamble (quality gate threshold 0.92, constitutional principles P-003/P-020/P-022, self-review reminder S-010, leniency bias calibration S-014, UV-only Python environment), enforcing the 600-token budget constraint, and returning structured reinforcement content.

## Acceptance Criteria

- [ ] `PromptReinforcementEngine` class created in `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py`
- [ ] Engine extracts L2-REINJECT content from rules files
- [ ] Preamble includes quality gate threshold (0.92)
- [ ] Preamble includes constitutional principles reminder (P-003, P-020, P-022)
- [ ] Preamble includes self-review reminder (S-010)
- [ ] Preamble includes leniency bias calibration (S-014)
- [ ] Preamble includes UV-only Python environment reminder
- [ ] 600-token budget constraint enforced (content trimmed if necessary)
- [ ] Engine returns structured reinforcement content (not raw strings)

## Implementation Notes

- Location: `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py`
- The engine should have a `generate_preamble()` method that returns the assembled content
- Token counting can be approximate (word-based heuristic: ~0.75 tokens per word for English)
- The preamble content should be an XML-structured block for Claude's parsing
- Content priority order if trimming needed: quality gate > constitutional > self-review > leniency > UV
- Consider making content sections configurable for future extensibility

**Design Source:** EPIC-002 EN-403/TASK-002 (UserPromptSubmit design), EN-405/TASK-006 (preamble content)

## Related Items

- Parent: [EN-705: UserPromptSubmit Quality Hook](EN-705-userpromptsubmit-hook.md)
- Related: TASK-001 (hook adapter that delegates to this engine)
- Related: EN-706 TASK-001 (SessionQualityContextGenerator -- similar preamble design but for L1)

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
