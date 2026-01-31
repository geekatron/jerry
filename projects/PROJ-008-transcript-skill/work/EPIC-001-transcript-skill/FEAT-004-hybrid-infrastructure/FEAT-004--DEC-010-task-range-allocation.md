# FEAT-004:DEC-010: Task Range Allocation for Hybrid Infrastructure

<!--
TEMPLATE: Decision
VERSION: 1.0.0
SOURCE: worktracker.md (Decision File), ADR/MADR best practices
CREATED: 2026-01-28 (FEAT-004 Hybrid Infrastructure)
PURPOSE: Document task ID range allocation to avoid FEAT-002 conflict
-->

> **Type:** decision
> **Status:** ACCEPTED
> **Priority:** HIGH
> **Created:** 2026-01-28T23:00:00Z
> **Parent:** FEAT-004
> **Owner:** Claude
> **Related:** FEAT-002, EN-014, EN-020, EN-021, EN-022, EN-023

---

## Frontmatter

```yaml
id: "FEAT-004:DEC-010"
work_type: DECISION
title: "Task Range Allocation for Hybrid Infrastructure"
status: ACCEPTED
priority: HIGH
created_by: "Claude"
participants:
  - "Adam Nowak"
  - "Claude"
created_at: "2026-01-28T23:00:00Z"
updated_at: "2026-01-28T23:00:00Z"
decided_at: "2026-01-28T23:00:00Z"
parent_id: "FEAT-004"
tags: ["task-allocation", "id-conflict", "feat-004"]
decision_count: 1
superseded_by: null
supersedes: null
```

---

## Summary

Allocates TASK-200+ range to FEAT-004 (Hybrid Infrastructure) enablers to avoid ID conflict with FEAT-002 EN-014 (Domain Context Files) which uses TASK-150-159.

**Decisions Captured:** 1

**Key Outcomes:**
- FEAT-004 tasks renumbered to TASK-200+ range
- EN-020 (Python Parser): TASK-200-205
- EN-021 (Chunking Strategy): TASK-210-214
- EN-022 (Extractor Adaptation): TASK-220-223
- EN-023 (Integration Testing): TASK-230-235

---

## Decision Context

### Background

During FEAT-004 creation (Hybrid Infrastructure for large transcript processing), enablers EN-020 through EN-023 were defined with task ranges:

- EN-020: TASK-150 through TASK-155
- EN-021: TASK-160 through TASK-164
- EN-022: TASK-170 through TASK-173
- EN-023: TASK-180 through TASK-185

However, ORCHESTRATION.yaml for FEAT-002 already allocates:

- EN-014: TASK-126 through TASK-159 (with TASK-150-159 for EN-006 artifact promotion per DISC-005)
- EN-019: TASK-160 through TASK-163

This creates a direct ID collision that would break work tracker traceability.

### Constraints

- Task IDs must be globally unique within PROJ-008
- Existing EN-014 and EN-019 task ranges cannot change (already referenced in ORCHESTRATION.yaml)
- FEAT-004 is new and can be renumbered without impact

### Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| Adam Nowak | Project Owner | Clean task ID space, no collisions |
| Claude | Implementer | Consistent task tracking |

---

## Decisions

### D-001: FEAT-004 Task Range 200+

**Date:** 2026-01-28
**Participants:** Adam Nowak, Claude

#### Question/Context

During FEAT-004 enabler creation, Claude asked:

> "I noticed a potential ID conflict: EN-014's TASK-150..159 overlaps with EN-020's TASK-150..155. How should we resolve this?"

Options were:
- **Option A**: Renumber FEAT-004 tasks to TASK-200+ range (new feature gets new range)
- **Option B**: Renumber EN-014 expanded tasks (existing feature modified)
- **Option C**: Use enabler-scoped task numbering (TASK-001 within each enabler)

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Renumber FEAT-004 to TASK-200+ | Clean separation, no FEAT-002 changes, future-proof | Larger task ID gap |
| **B** | Renumber EN-014 to higher range | Keeps lower numbers contiguous | Modifies existing ORCHESTRATION.yaml |
| **C** | Enabler-scoped numbering | No global conflicts | Breaks established global ID pattern |

#### Decision

**We decided:** Option A - Renumber all FEAT-004 tasks to TASK-200+ range.

FEAT-004 task allocation:

| Enabler | Range | Tasks |
|---------|-------|-------|
| EN-020 (Python Parser) | 200-205 | TASK-200, 201, 202, 203, 204, 205 |
| EN-021 (Chunking Strategy) | 210-214 | TASK-210, 211, 212, 213, 214 |
| EN-022 (Extractor Adaptation) | 220-223 | TASK-220, 221, 222, 223 |
| EN-023 (Integration Testing) | 230-235 | TASK-230, 231, 232, 233, 234, 235 |

#### Rationale

1. **No impact on existing FEAT-002**: EN-014 and EN-019 task allocations remain unchanged
2. **Clear feature separation**: TASK-100s for FEAT-002, TASK-200s for FEAT-004
3. **Future-proof**: TASK-300s available for FEAT-005+ if needed
4. **Follows precedent**: Similar to DEC-003 enabler-scoped numbering for EN-009

#### Implications

- **Positive:** Clean task ID space with feature-based segmentation
- **Negative:** Larger gap between FEAT-002 and FEAT-004 task IDs
- **Follow-up required:** Update EN-020 through EN-023 enabler documents with corrected task ranges

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-001 | FEAT-004 tasks use TASK-200+ range | 2026-01-28 | ACCEPTED |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-004-hybrid-infrastructure.md](./FEAT-004-hybrid-infrastructure.md) | Parent feature |
| Reference | [ORCHESTRATION.yaml](../FEAT-002-implementation/ORCHESTRATION.yaml) | FEAT-002 task allocations |
| Related | [EN-014](../FEAT-002-implementation/EN-014-domain-context/EN-014-domain-context.md) | Domain Context Files (TASK-150-159) |
| Related | [EN-020](./EN-020-python-parser/EN-020-python-parser.md) | Python Parser (to be updated) |
| Related | [EN-021](./EN-021-chunking-strategy/EN-021-chunking-strategy.md) | Chunking Strategy (to be updated) |
| Related | [EN-022](./EN-022-extractor-adaptation/EN-022-extractor-adaptation.md) | Extractor Adaptation (to be updated) |
| Related | [EN-023](./EN-023-integration-testing/EN-023-integration-testing.md) | Integration Testing (to be updated) |
| Convention | [docs/conventions/worktracker.md](../../../conventions/worktracker.md) | Worktracker conventions |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Created decision document, accepted by Adam Nowak |

---

## Metadata

```yaml
id: "FEAT-004:DEC-010"
parent_id: "FEAT-004"
work_type: DECISION
title: "Task Range Allocation for Hybrid Infrastructure"
status: ACCEPTED
priority: HIGH
created_by: "Claude"
created_at: "2026-01-28T23:00:00Z"
updated_at: "2026-01-28T23:00:00Z"
decided_at: "2026-01-28T23:00:00Z"
participants: ["Adam Nowak", "Claude"]
tags: ["task-allocation", "id-conflict", "feat-004"]
decision_count: 1
superseded_by: null
supersedes: null
```
