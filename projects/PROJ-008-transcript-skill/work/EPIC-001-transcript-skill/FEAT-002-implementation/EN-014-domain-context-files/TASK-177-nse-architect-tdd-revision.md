# TASK-177: nse-architect TDD Revision

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-014 (Domain Context Files Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-177"
work_type: TASK
title: "nse-architect TDD Revision"
description: |
  Revise TDD-EN014-domain-schema-v2.md to address all 9 implementation gaps
  identified in TASK-176 gap analysis. Add Sections 6-11 for implementation
  architecture, runtime environment, testing strategy, CI/CD, CLI integration,
  and implementability checklist.

classification: ENABLER
status: DONE
resolution: COMPLETED
priority: CRITICAL
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-29T15:30:00Z"
updated_at: "2026-01-29T16:00:00Z"

parent_id: "EN-014"

tags:
  - "tdd-revision"
  - "implementation-architecture"
  - "cli-integration"
  - "testing-strategy"
  - "ci-cd"

effort: 3
acceptance_criteria: |
  - Section 6: Integration Specification added (sequence diagrams)
  - Section 7: Runtime Environment added (Python, deps, venv)
  - Section 8: Testing Strategy added (RED/GREEN/REFACTOR)
  - Section 9: CI/CD Specification added (GitHub Actions YAML)
  - Section 10: Jerry CLI Integration added (parser, adapter, bootstrap)
  - Section 11: Implementability Checklist added
  - Section 5.2 revised (hexagonal paths, caller chain)
  - TDD version bumped to 3.0.0
  - All 9 gaps resolved

due_date: null

activity: DESIGN
original_estimate: 3
remaining_work: 0
time_spent: 3
```

---

## State Machine

**Current State:** `DONE`

```
BACKLOG → IN_PROGRESS → DONE
```

---

## Content

### Description

This task revises TDD-EN014-domain-schema-v2.md from v2.0 to v3.0.0 to address all implementation gaps identified in the ps-analyst gap analysis (TASK-176).

### New Sections Added

| Section | Title | Content |
|---------|-------|---------|
| 6 | Integration Specification | Sequence diagrams for skill, CLI, CI integration |
| 7 | Runtime Environment | Python 3.11+, pyproject.toml deps, venv setup |
| 8 | Testing Strategy | RED/GREEN/REFACTOR, test pyramid, coverage targets |
| 9 | CI/CD Specification | GitHub Actions workflow YAML, quality gates |
| 10 | Jerry CLI Integration | Parser, main routing, adapter, bootstrap wiring |
| 11 | Implementability Checklist | Self-assessment gate for TDD completeness |

### Section 5.2 Revisions

| Change | Before | After |
|--------|--------|-------|
| Validator Location | `skills/transcript/validators/` | `src/transcript/domain/validators/` |
| SV-006 Context | Dangling function | Full call chain from CLI |
| Error Handling | Not specified | try/except with ValidationError |
| Port/Adapter | Not separated | IValidator protocol defined |

### User Decisions Incorporated (from DEC-001)

- **D-001:** All validators are runnable Python code (not LLM specs)
- **D-002:** CLI namespace: `jerry transcript validate-domain <path>`

### Acceptance Criteria

- [x] Section 6: Integration Specification with sequence diagrams
- [x] Section 7: Runtime Environment (Python 3.11+, deps, venv)
- [x] Section 8: Testing Strategy (RED/GREEN/REFACTOR, 10 test files)
- [x] Section 9: CI/CD Specification (complete workflow YAML)
- [x] Section 10: Jerry CLI Integration (parser, adapter, bootstrap)
- [x] Section 11: Implementability Checklist
- [x] Section 5.2.1 validator location fixed
- [x] Section 5.2.2 SV-006 caller chain added
- [x] TDD version bumped to 3.0.0
- [x] All 9 gaps from TASK-176 resolved

### Related Items

- Parent: [EN-014: Domain Context Files Implementation](./EN-014-domain-context-files.md)
- Blocked By: [TASK-176: ps-analyst Gap Analysis](./TASK-176-ps-analyst-gap-analysis.md)
- Blocks: [TASK-178: ps-critic TDD Validation](./TASK-178-ps-critic-tdd-validation.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| TDD v3.0.0 | Design Document | docs/design/TDD-EN014-domain-schema-v2.md |

### Verification

- [x] All 6 new sections (6-11) added
- [x] Section 5.2 revised with hexagonal paths
- [x] Version 3.0.0 with revision history updated
- [x] DEC-001 decisions incorporated
- [x] Follows Jerry architecture patterns
- [x] Reviewed by: TASK-178 ps-critic (0.96 score)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-29 | Created | Created per DISC-008 remediation plan |
| 2026-01-29 | DONE | TDD revised to v3.0.0. Added Sections 6-11 (Integration, Runtime, Testing, CI/CD, CLI, Implementability). Fixed Section 5.2 paths. All 9 gaps resolved. |
