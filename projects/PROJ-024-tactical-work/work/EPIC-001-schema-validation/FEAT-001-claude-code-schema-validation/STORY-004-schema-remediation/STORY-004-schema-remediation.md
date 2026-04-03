# STORY-004: Schema Remediation from C4 Review Findings

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: Fix schema issues identified by C4 adversarial review, DX review, and security review
-->

> **Type:** story
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-26T23:30:00Z
> **Due:**
> **Completed:** 2026-03-27T01:00:00Z
> **Parent:** FEAT-001
> **Owner:** adam.nowak
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | Remediation scope |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Progress Summary](#progress-summary) | Overall progress |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** Jerry framework developer creating agent or skill definitions

**I want** schema descriptions that prevent common mistakes and clearly communicate field behavior

**So that** I can author valid definitions without consulting external documentation

---

## Summary

Fix schema issues identified by the C4 adversarial review (0.79 REVISE), DX heuristic evaluation (1 severe, 10 major), and STRIDE security review. Focus on description text improvements, field validation tightening, and cross-schema confusion prevention.

**Scope:**
- Fix `model` field validation (too permissive -- accepts typos)
- Fix `allowed-tools` description (security-critical warning buried)
- Fix `hooks` description (opaque, no structural example)
- Fix `disallowedTools` description (no example tool names)
- Fix `name` regex (add no-consecutive-hyphens constraint)

---

## Acceptance Criteria

- [ ] `model` field in agent schema constrains to known aliases + documented full model ID pattern
- [ ] `allowed-tools` description leads with security warning ("grants permission, does NOT restrict")
- [ ] `hooks` description includes at least one structural YAML example in the description text
- [ ] `disallowedTools` description includes example tool names matching PascalCase convention
- [ ] `name` pattern in both schemas rejects consecutive hyphens (`--`)
- [ ] All 89 existing agent definitions still validate against updated schema
- [ ] All 30 existing SKILL.md files still validate against updated schema

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Owner |
|----|-------|--------|-------|
| TASK-001 | Fix model field validation (agent schema) | pending | -- |
| TASK-002 | Fix allowed-tools description (skill schema) | pending | -- |
| TASK-003 | Fix hooks description (both schemas) | pending | -- |
| TASK-004 | Fix disallowedTools description (agent schema) | pending | -- |
| TASK-005 | Fix name regex (both schemas) | pending | -- |
| TASK-006 | Validate all existing definitions against updated schemas | pending | -- |

---

## Progress Summary

```
+------------------------------------------------------------------+
|                    STORY PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Tasks:     [....................] 0% (0/6 completed)              |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                               |
+------------------------------------------------------------------+
```

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: Claude Code Schema Validation](../FEAT-001-claude-code-schema-validation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | C4 adversarial review | Findings drive remediation scope |
| Depends On | DX heuristic evaluation | Findings drive description improvements |
| Depends On | STRIDE threat model | Security findings inform field constraints |

### Source Findings

| Finding ID | Source | Description |
|-----------|--------|-------------|
| FM-004 | C4 FMEA | model field accepts any string |
| DA-003 | C4 Devil's Advocate | model typos pass validation |
| DX-AG-001 | DX review | disallowedTools no examples |
| DX-SK-001 | DX review | allowed-tools security warning buried |
| DX-CS-001 | DX review | hooks description opaque |
| SM-002 | C4 Steelman | name pattern missing reserved word constraint |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-26 | adam.nowak | pending | Story created from C4/DX/security review findings |
