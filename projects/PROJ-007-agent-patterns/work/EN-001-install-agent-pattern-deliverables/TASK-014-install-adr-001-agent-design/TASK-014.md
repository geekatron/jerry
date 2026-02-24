# TASK-014: Install ADR-PROJ007-001 into docs/design

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Criticality:** C3 (AE-003)
> **Created:** 2026-02-21T23:59:00Z
> **Parent:** EN-001
> **Owner:** --
> **Effort:** 1
> **Activity:** documentation

---

## Summary

Install ADR-PROJ007-001 (agent design) into `docs/design/` and update status to Accepted.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Description](#description) | What this task requires |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical approach and constraints |
| [Related Items](#related-items) | Parent and related work |
| [History](#history) | Status changes |

---

## Description

Copy `ps-architect-001-adr-agent-design.md` from the PROJ-007 orchestration output to `docs/design/ADR-PROJ007-001-agent-design.md`. Update the ADR status field from Draft to Accepted. Verify cross-references within the document resolve correctly (links to rule files, schema paths, other ADRs).

**AE-003 applies:** This is a new ADR — auto-C3 minimum criticality.

### Steps

1. Locate source artifact: `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps-architect-001-adr-agent-design.md`
2. Copy to `docs/design/ADR-PROJ007-001-agent-design.md`
3. Update status field: `Status: Draft` → `Status: Accepted`
4. Update date field to reflect acceptance date: `2026-02-21`
5. Verify all internal cross-references resolve (paths to rule files, schema, companion ADR-002)

---

## Acceptance Criteria

- [ ] AC-1: ADR exists at `docs/design/ADR-PROJ007-001-agent-design.md`
- [ ] AC-2: Status field reads `Accepted`
- [ ] AC-3: All cross-references within the ADR resolve to existing files
- [ ] AC-4: Content matches source orchestration artifact (beyond status/date update)

---

## Implementation Notes

### Files to Create

| File | Action |
|------|--------|
| `docs/design/ADR-PROJ007-001-agent-design.md` | Copy from orchestration output; update status to Accepted |

### Cross-Reference Verification

Check that all paths referenced in the ADR body exist in the repository:
- Links to `.context/rules/agent-development-standards.md` (installed by TASK-012)
- Links to `docs/schemas/agent-definition-v1.schema.json` (created by TASK-018)
- Links to companion `ADR-PROJ007-002-routing-framework.md` (installed by TASK-015)

Note: TASK-012, TASK-015, and TASK-018 may need to complete before all cross-references resolve. Document any unresolved references at time of installation.

### AE-003 Note

New ADR is auto-C3. Self-review (S-010) required before marking done.

---

## Related Items

- **Parent:** [EN-001](../EN-001.md)
- **AE-003:** New ADR — auto-C3 minimum
- **Source artifact:** `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps-architect-001-adr-agent-design.md`
- **Companion:** TASK-015 installs ADR-PROJ007-002 (routing framework)
- **Schema dependency:** TASK-018 generates the JSON Schema referenced by this ADR

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-21 | pending | Created — awaiting installation of orchestration output |
