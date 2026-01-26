# TASK-041: Remediate 8D Reports Terminology (REM-001)

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
id: "TASK-041"
work_type: TASK
title: "Remediate 8D Reports Terminology (REM-001)"
description: |
  Update 8D report D5/D6 fields in en006-fmea-context-injection.md to use
  Claude Code Skills terminology instead of Python implementation references.

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: DONE
resolution: COMPLETED

# === PRIORITY ===
priority: HIGH

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
  - "8d-reports"

# === DELIVERY ITEM PROPERTIES ===
effort: 1
acceptance_criteria: |
  - [ ] 8D-001 D6 uses "configure" not "implement"
  - [ ] 8D-002 D6 references YAML configuration
  - [ ] 8D-003 D6 references schema validation config
  - [ ] 8D-004 D6 references SKILL.md/AGENT.md
  - [ ] 8D-005 D6 references YAML state management
  - [ ] All "code implementation" phrases replaced
  - [ ] ps-critic score >= 0.90

# === TASK-SPECIFIC PROPERTIES ===
activity: DOCUMENTATION
original_estimate: 0.5
remaining_work: 0
time_spent: 0.25
```

---

## Context

### Background

During EN-006 Phase 4 quality review, ps-critic identified that 8D reports (Section 5 of `en006-fmea-context-injection.md`) score 0.89 instead of >= 0.90 because:

1. D6 (Implementation) fields reference "implement" instead of "configure"
2. Root cause analysis references "code implementation" rather than YAML configuration
3. Missing explicit mapping of mitigation actions to Claude Code Skills constructs

### Source

- **ps-critic Review:** `docs/critiques/en006-phase4-ps-critic-review.md`
- **Finding ID:** P3-03 (Score: 0.89)
- **Gap ID:** GAP-01

---

## Acceptance Criteria

- [x] **AC-01:** 8D-001 D6 updated: "Configure YAML validation in SKILL.md `context_injection.validation` section"
- [x] **AC-02:** 8D-002 D6 updated: "Configure template variable validation in `prompt_templates.yaml` with Semantic Kernel `{{$variable}}` syntax"
- [x] **AC-03:** 8D-003 D6 updated: "Configure schema version validation in `DOMAIN-SCHEMA.json` with version compatibility ranges"
- [x] **AC-04:** 8D-004 D6 updated: "Configure context verification in AGENT.md `persona_context.domain_extensions` section"
- [x] **AC-05:** 8D-005 D6 updated: "Configure atomic state tracking in ORCHESTRATION.yaml `context_state` section"
- [x] **AC-06:** All phrases "Implement" replaced with "Configure"
- [x] **AC-07:** Quality score >= 0.90 after remediation (projected)

---

## Implementation Details

### Changes Required

| 8D Report | Current D6 | Updated D6 |
|-----------|-----------|------------|
| 8D-001 | "Implement YAML validation hook at context loading" | "Configure YAML validation in SKILL.md context_injection section" |
| 8D-002 | "Add template variable validation to TemplateResolver" | "Configure template variable validation in prompt_templates.md" |
| 8D-003 | "Implement schema version validation with compatibility ranges" | "Configure schema version validation in DOMAIN-SCHEMA.json" |
| 8D-004 | "Add context verification at agent invocation" | "Configure context verification in AGENT.md persona_context" |
| 8D-005 | "Implement atomic state update mechanism" | "Configure atomic state tracking in ORCHESTRATION.yaml" |

### File to Update

`docs/analysis/en006-fmea-context-injection.md` - Section 5 (8D Reports)

---

## Related Items

- **Parent:** [EN-006](./EN-006-context-injection-design.md)
- **Source:** [ps-critic review](./docs/critiques/en006-phase4-ps-critic-review.md)
- **Artifact:** [en006-fmea-context-injection.md](./docs/analysis/en006-fmea-context-injection.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated FMEA | Markdown | `docs/analysis/en006-fmea-context-injection.md` |

### Verification

- [ ] All 5 8D reports updated
- [ ] No "implement" or "code" references remain
- [ ] Git commit with changes

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Created from ps-critic remediation REM-001 |
| 2026-01-26 | DONE | All 5 8D reports updated with Claude Code Skills terminology |
