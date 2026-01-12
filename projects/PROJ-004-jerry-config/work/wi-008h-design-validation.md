# WI-008h: Validate Domain Design

| Field | Value |
|-------|-------|
| **ID** | WI-008h |
| **Title** | Validate domain design against use cases |
| **Type** | Validation |
| **Status** | PENDING |
| **Priority** | HIGH |
| **Phase** | PHASE-02 |
| **Parent** | WI-008 |
| **Agent** | ps-validator |
| **Assignee** | WT-Main |
| **Created** | 2026-01-12 |
| **Completed** | - |

---

## Description

Validate the complete domain design against use cases, existing patterns, and extensibility requirements. This is the final gate before proceeding to implementation.

---

## Agent Invocation

### ps-validator Prompt

```
You are the ps-validator agent (v2.0.0).

## PS CONTEXT (REQUIRED)
- **PS ID:** PROJ-004
- **Entry ID:** e-012
- **Topic:** Jerry Domain Model Validation

## MANDATORY PERSISTENCE (P-002)
Create validation report at: projects/PROJ-004-jerry-config/analysis/PROJ-004-e-012-domain-validation.md

## VALIDATION TASK

Validate the domain design from ADRs against requirements.

### Use Cases to Validate

| ID | Use Case | Requirement |
|----|----------|-------------|
| UC-01 | Session Start | List projects, select active project |
| UC-02 | Skill Invocation | Get project context, resolve output paths |
| UC-03 | Work Tracker | Get work items path for active project |
| UC-04 | Multi-Worktree | Independent context per worktree |
| UC-05 | Config Override | Env → local → project → framework → defaults |
| UC-06 | Project Creation | Create new project with valid structure |
| UC-07 | Skill Discovery | List and invoke available skills |

### Validation Criteria

For each use case:
1. Can the design support this use case?
2. What entities/methods are involved?
3. Are there any gaps or missing capabilities?
4. What is the complexity of implementation?

### Design Documents to Review
- ADR-PROJ004-001-jerry-framework-aggregate.md
- ADR-PROJ004-002-jerry-project-aggregate.md
- ADR-PROJ004-003-jerry-skill-aggregate.md
- ADR-PROJ004-004-jerry-session-context.md

### Architecture Constraints to Verify
1. Domain layer has zero external dependencies
2. Ports define contracts, adapters implement
3. Aggregates enforce their invariants
4. Value objects are immutable

### Extensibility Check
- Can new entity types be added (e.g., JerryWorkspace)?
- Can new skills be added without domain changes?
- Can configuration format change (TOML → YAML)?
- Can new precedence levels be added?

## OUTPUT FORMAT
Create traceability matrix showing:
- Each use case → supporting entities/methods
- Each constraint → verification evidence
- Gaps identified with severity
- Recommendations for fixes
```

---

## Acceptance Criteria

- [ ] AC-008h.1: All 7 use cases validated
- [ ] AC-008h.2: Traceability matrix complete
- [ ] AC-008h.3: Architecture constraints verified
- [ ] AC-008h.4: Extensibility assessed
- [ ] AC-008h.5: Gaps identified with severity
- [ ] AC-008h.6: Recommendations documented
- [ ] AC-008h.7: Validation report created

---

## Use Case Traceability Template

| Use Case | Entities | Methods | Gaps | Severity |
|----------|----------|---------|------|----------|
| UC-01: Session Start | JerryFramework, JerrySession | `list_projects()`, `set_active_project()` | TBD | - |
| UC-02: Skill Invocation | JerrySkill, JerrySession | `get_output_path()`, `active_project` | TBD | - |
| UC-03: Work Tracker | JerryProject | `get_work_items_path()` | TBD | - |
| UC-04: Multi-Worktree | JerrySession, WorktreeInfo | `worktree_info` | TBD | - |
| UC-05: Config Override | JerrySession | `get_config()` | TBD | - |
| UC-06: Project Creation | JerryFramework | `create_project()` | TBD | - |
| UC-07: Skill Discovery | JerryFramework | `list_skills()`, `get_skill()` | TBD | - |

---

## Evidence

| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-008h.1 | - | - |
| AC-008h.2 | - | - |
| AC-008h.3 | - | - |
| AC-008h.4 | - | - |
| AC-008h.5 | - | - |
| AC-008h.6 | - | - |
| AC-008h.7 | - | - |

---

## Progress Log

| Timestamp | Update | Actor |
|-----------|--------|-------|
| 2026-01-12T12:00:00Z | Work item created | Claude |

---

## Dependencies

| Type | Work Item | Relationship |
|------|-----------|--------------|
| Part Of | WI-008 | Parent work item |
| Depends On | WI-008d, WI-008e, WI-008f, WI-008g | All ADRs must complete |
| Blocks | WI-009 through WI-018 | Implementation waits for validation |

---

## Related Artifacts

- **Output**: `analysis/PROJ-004-e-012-domain-validation.md`
- **ADR Inputs**: `decisions/ADR-PROJ004-00*.md`
- **Research Inputs**: `research/PROJ-004-e-005-*.md` through `research/PROJ-004-e-007-*.md`
