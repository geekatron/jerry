# TASK-180: nse-architect TDD v3.1.0 Revision (DISC-009 Integration)

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-014 (Domain Context Files Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-180"
work_type: TASK
title: "nse-architect TDD v3.1.0 Revision (DISC-009 Integration)"
description: |
  Revise TDD to v3.1.0 incorporating DISC-009 findings: add Section 12
  Hybrid Architecture Rationale, update existing sections to reference
  hybrid pipeline and FEAT-004.

classification: ENABLER
status: DONE
resolution: COMPLETED
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-29T17:00:00Z"
updated_at: "2026-01-29T18:00:00Z"
completed_at: "2026-01-29T18:00:00Z"

parent_id: "EN-014"

tags:
  - "nse-architect"
  - "tdd-revision"
  - "disc-009"
  - "hybrid-architecture"
  - "v3.1.0"

effort: 3
acceptance_criteria: |
  - Section 12: Hybrid Architecture Rationale added
  - Section 5.2 updated with DISC-009 reference
  - Section 7 updated with hybrid architecture context
  - Section 10 updated with hybrid pipeline integration
  - TDD version bumped to 3.1.0
  - All DISC-009 findings incorporated with citations

due_date: null

activity: DESIGN
original_estimate: 3
remaining_work: 0
time_spent: 3
```

---

## State Machine

**Current State:** `BACKLOG`

```
BACKLOG → IN_PROGRESS → DONE
```

---

## Content

### Description

This task revises TDD-EN014-domain-schema-v2.md from v3.0.0 to v3.1.0 to incorporate all DISC-009 findings per the gap analysis from TASK-179.

### Required Changes

| Section | Change Type | Description |
|---------|-------------|-------------|
| NEW Section 12 | Add | Hybrid Architecture Rationale |
| Section 5.2 | Update | Add DISC-009 reference for Python validators |
| Section 7 | Update | Connect runtime environment to hybrid architecture |
| Section 10 | Update | Explain CLI in context of hybrid pipeline |
| References | Update | Add DISC-009 citations |

### Section 12 Requirements

Section 12: Hybrid Architecture Rationale must include:

1. **Why Python Validators (Not LLM-Based)**
   - Agent definitions are behavioral specs, NOT executable code (DISC-009 finding)
   - LLM "Lost-in-the-Middle" problem (Stanford research)
   - 1,250x cost efficiency of Python vs. LLM (Meilisearch research)

2. **Connection to DISC-009**
   - Explicit reference to `FEAT-002--DISC-009-agent-only-architecture-limitation.md`
   - Evidence chain with citations

3. **Integration with FEAT-004**
   - How domain validation fits hybrid pipeline
   - Relationship to Python parsing layer

### Acceptance Criteria

- [ ] Section 12: Hybrid Architecture Rationale with full rationale
- [ ] Section 5.2 updated with DISC-009 reference
- [ ] Section 7 updated with hybrid context
- [ ] Section 10 updated with hybrid pipeline integration
- [ ] TDD version bumped to 3.1.0
- [ ] Revision history updated
- [ ] All DISC-009 findings incorporated with citations

### Related Items

- Parent: [EN-014: Domain Context Files Implementation](./EN-014-domain-context-files.md)
- Blocked By: [TASK-179: ps-analyst Gap Analysis](./TASK-179-ps-analyst-disc009-integration.md)
- Blocks: [TASK-181: ps-critic TDD v3.1.0 Validation](./TASK-181-ps-critic-tdd-v310-validation.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| TDD v3.1.0 | Design Document | docs/design/TDD-EN014-domain-schema-v2.md |

### Verification

- [ ] All 4 sections updated/added
- [ ] Version 3.1.0 with revision history
- [ ] DISC-009 findings incorporated with citations
- [ ] Follows hybrid architecture patterns
- [ ] Reviewed by: TASK-181 ps-critic

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-29 | Created | Created per DISC-010 remediation plan |
