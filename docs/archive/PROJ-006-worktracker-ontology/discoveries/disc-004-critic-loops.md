# DISC-004: Critic Loops for Quality Feedback

> **Discovery ID:** DISC-004
> **Type:** Discovery
> **Status:** IMPLEMENTED
> **Discovered During:** SYNC BARRIER 3 Review
> **Discovered By:** User + Claude
> **Date:** 2026-01-14
> **Related Work Item:** EN-004

---

## Summary

During the SYNC BARRIER 3 review (post-synthesis), we identified that the original orchestration plan lacked quality feedback loops before human approval gates. This discovery led to the implementation of a formal **Critic Loop Architecture** that provides automated validation of artifacts before phase transitions.

---

## Problem Statement

### Original State

The original ORCHESTRATION_PLAN.md (v1.0) defined sync barriers as simple human approval gates:

```
Enabler → Artifact → SYNC BARRIER → Human Approval → Next Phase
```

### Gap Identified

Without automated quality validation before human review:
1. Human reviewers receive potentially inconsistent or incomplete artifacts
2. No mechanism for iterative refinement before escalation
3. Quality issues discovered late require expensive rework
4. No audit trail of validation decisions

---

## Solution: Critic Loop Architecture

### Pattern

```
Producer ──► Artifact ──► Critic ──► Decision
                              │
             ┌────────────────┼────────────────┐
             ▼                ▼                ▼
          APPROVE          REVISE       DOCUMENT_PROCEED
             │                │                │
             ▼                ▼                ▼
        Next Phase    Return to         Accept with
                      Producer          Risk Documentation
```

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Max 2 iterations | Prevents infinite loops; escalates to human after 2 attempts |
| Lightweight at convergence | Research/analysis phases validated in batch |
| Full review at synthesis | Critical design phases require comprehensive validation |
| Document-and-proceed option | Allows forward progress with explicit risk acceptance |

### Critic Criteria Types

| Type | Weight | Example Check |
|------|--------|---------------|
| **Critical** | Blocking | Accuracy of mappings |
| **High** | Strong signal | Completeness, consistency |
| **Medium** | Advisory | Coverage of edge cases |

---

## Implementation

### Artifacts Created/Modified

| Artifact | Change |
|----------|--------|
| `ORCHESTRATION_PLAN.md` | Added Critic Loop Architecture section (v2.0) |
| `ORCHESTRATION.yaml` | Added `critic_config` and `critic_loops` sections |
| `reviews/REVIEW-TEMPLATE.md` | Created standard review document template |
| `en-004.md` | Added Critic Loop Review section |
| `FEATURE-WORKTRACKER.md` | Added Critic columns to tables |
| `SOLUTION-WORKTRACKER.md` | Added Critic Loops section |
| `WORKTRACKER.md` | Added Critic Loops section |

### Critic Loops Defined

| ID | Name | Reviews | Gate | Status |
|----|------|---------|------|--------|
| CL-003 | Synthesis Review | EN-004 | SYNC-3 | PENDING |
| CL-004 | Ontology Review | WI-001 | SYNC-4 | BLOCKED |
| CL-005 | Templates Review | WI-002 | SYNC-5 | BLOCKED |

---

## Lessons Learned

### What Worked

1. **User-AI collaboration** identified the gap during natural checkpoint review
2. **Incremental enhancement** - didn't require rework of completed phases
3. **Forward-compatible** - critic loops can be applied retroactively

### What to Improve

1. **Earlier consideration** - critic loops should be planned in initial orchestration design
2. **Template first** - having a review template before execution helps consistency
3. **Metrics** - consider tracking iteration counts and cycle times

---

## Recommendations

### For Future Orchestration Plans

1. Include critic loop planning in initial design phase
2. Define review criteria before production begins
3. Allocate explicit time for critic iterations
4. Consider lightweight critics even for parallel research streams

### For Jerry Framework

Consider promoting the Critic Loop pattern to the orchestration skill:
- Standard critic loop schema in YAML
- Review template generation
- Integration with worktracker for status tracking

---

## References

- [ORCHESTRATION_PLAN.md](../../ORCHESTRATION_PLAN.md) - Updated to v2.0
- [ORCHESTRATION.yaml](./ORCHESTRATION.yaml) - Updated to v2.0
- [EN-004](./en-004.md) - First work item subject to critic review
- [REVIEW-TEMPLATE.md](./reviews/REVIEW-TEMPLATE.md) - Standard review format

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-14 | Created discovery document | Claude |
