# TASK-042: Remediate DISC-001 SPEC Reference (REM-002)

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
STATUS: BACKLOG
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "TASK-042"
work_type: TASK
title: "Remediate DISC-001 SPEC Reference (REM-002)"
description: |
  Update EN-006--DISC-001-feat002-implementation-scope.md to add reference
  to SPEC-context-injection.md Section 3 (Claude Code Skills Mapping) and
  clarify FEAT-002 produces contexts/*.yaml files, not Python code.

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: DONE
resolution: COMPLETED

# === PRIORITY ===
priority: MEDIUM

# === PEOPLE ===
assignee: "Claude"
created_by: "Claude"

# === TIMESTAMPS ===
created_at: "2026-01-26T14:30:00Z"
updated_at: "2026-01-26T14:30:00Z"

# === HIERARCHY ===
parent_id: "EN-006"

# === TAGS ===
tags:
  - "remediation"
  - "quality"
  - "claude-code-skills"
  - "discovery"

# === DELIVERY ITEM PROPERTIES ===
effort: 1
acceptance_criteria: |
  - [ ] Reference to SPEC Section 3 added
  - [ ] YAML-only implementation clarified
  - [ ] Related Artifacts section updated
  - [ ] ps-critic score >= 0.90

# === TASK-SPECIFIC PROPERTIES ===
activity: DOCUMENTATION
original_estimate: 0.25
remaining_work: 0
time_spent: 0.15
```

---

## Context

### Background

During EN-006 Phase 4 quality review, ps-critic identified that DISC-001 (`EN-006--DISC-001-feat002-implementation-scope.md`) scores 0.88 instead of >= 0.90 because:

1. Missing explicit reference to SPEC-context-injection.md Section 3 mapping
2. References "implementation" without clarifying YAML-only scope
3. Doesn't explicitly state FEAT-002 produces contexts/*.yaml, not Python code

### Source

- **ps-critic Review:** `docs/critiques/en006-phase4-ps-critic-review.md`
- **Finding ID:** SD-04 (Score: 0.88)
- **Gap ID:** GAP-02

---

## Acceptance Criteria

- [x] **AC-01:** Add reference to SPEC-context-injection.md Section 3 in "Related Artifacts"
- [x] **AC-02:** Add clarification note in "Key Findings" section (YAML-only callout)
- [x] **AC-03:** Update "Category 1" header to clarify YAML-only deliverables
- [x] **AC-04:** Quality score >= 0.90 after remediation (projected)

---

## Implementation Details

### Changes Required

1. **Add to Related Artifacts Section:**
   ```markdown
   | Spec | [SPEC-context-injection.md Section 3](./docs/specs/SPEC-context-injection.md#3-claude-code-skills-mapping) | Claude Code Skills Mapping |
   ```

2. **Add clarification to Finding section:**
   ```markdown
   > **IMPORTANT:** All FEAT-002 implementation tasks produce **YAML configuration files only**
   > (contexts/*.yaml, SKILL.md, AGENT.md). No Python or executable code is created.
   > See [SPEC-context-injection.md Section 3](./docs/specs/SPEC-context-injection.md) for
   > Claude Code Skills mapping patterns.
   ```

3. **Update Category 1 header:**
   ```markdown
   #### Category 1: Context File Implementation (YAML Only)
   ```

### File to Update

`EN-006--DISC-001-feat002-implementation-scope.md`

---

## Related Items

- **Parent:** [EN-006](./EN-006-context-injection-design.md)
- **Source:** [ps-critic review](./docs/critiques/en006-phase4-ps-critic-review.md)
- **Artifact:** [EN-006--DISC-001-feat002-implementation-scope.md](./EN-006--DISC-001-feat002-implementation-scope.md)
- **Reference:** [SPEC-context-injection.md Section 3](./docs/specs/SPEC-context-injection.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated DISC-001 | Markdown | `EN-006--DISC-001-feat002-implementation-scope.md` |

### Verification

- [ ] SPEC Section 3 reference added
- [ ] YAML-only clarification added
- [ ] Git commit with changes

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Created from ps-critic remediation REM-002 |
| 2026-01-26 | DONE | SPEC Section 3 reference added, YAML-only clarification added |
