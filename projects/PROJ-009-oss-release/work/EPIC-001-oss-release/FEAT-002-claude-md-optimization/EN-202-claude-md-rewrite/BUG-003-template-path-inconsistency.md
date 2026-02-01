# EN-202:BUG-003: Template path inconsistency in CLAUDE.md

<!--
TEMPLATE: Bug
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.10
CREATED: 2026-02-01 (EN-201 QG-1 Finding)
PURPOSE: Document defect requiring fix in CLAUDE.md rewrite
-->

> **Type:** bug
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Severity:** minor
> **Created:** 2026-02-01T14:30:00Z
> **Due:** -
> **Completed:** -
> **Parent:** EN-202
> **Owner:** -
> **Found In:** CLAUDE.md (current)
> **Fix Version:** EN-202

---

## Summary

CLAUDE.md contains conflicting template path references: `docs/templates/worktracker/` in description text versus `.context/templates/worktracker/` in Location headers and tables. This inconsistency could confuse Claude agents about where templates actually reside.

**Key Details:**
- **Symptom:** Two different paths documented for same templates
- **Frequency:** Consistent (present in multiple sections)
- **Workaround:** Use `.context/templates/worktracker/` (correct path)

---

## Reproduction Steps

### Prerequisites

Access to CLAUDE.md in repository root.

### Steps to Reproduce

1. Open CLAUDE.md
2. Navigate to line 244 (first worktracker templates section)
3. Observe description text: "stored in the `docs/templates/worktracker/` folder"
4. Navigate to line 292 (second worktracker templates section)
5. Observe Location header: "`.context/templates/worktracker/`"
6. Note the conflicting paths

### Expected Result

All template path references should consistently use `.context/templates/worktracker/`.

### Actual Result

Two different paths are documented:
- Description text uses `docs/templates/worktracker/`
- Location headers and tables use `.context/templates/worktracker/`

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | Any |
| **Browser/Runtime** | N/A (documentation file) |
| **Application Version** | CLAUDE.md current |
| **Configuration** | Default |
| **Deployment** | Repository root |

---

## Evidence

### Bug Documentation

| Evidence | Type | Description | Date |
|----------|------|-------------|------|
| EN-201 QG-1 nse-qa-audit-v3.md | Report | NCR-008 identified | 2026-02-01 |
| CLAUDE.md lines 244, 292 | Source | Conflicting path locations | 2026-02-01 |
| worktracker-templates.md | Extraction | Faithfully preserved source defect | 2026-02-01 |

### Actual Path Verification

```bash
$ ls .context/templates/worktracker/
BUG.md      DECISION.md  DISCOVERY.md  ENABLER.md  EPIC.md
FEATURE.md  IMPEDIMENT.md  SPIKE.md    STORY.md    TASK.md
```

The correct path is `.context/templates/worktracker/`.

---

## Root Cause Analysis

### Root Cause

Documentation drift during repository evolution. The templates were originally in `docs/templates/worktracker/` and later moved to `.context/templates/worktracker/`. The description text was not updated to reflect the new location.

### Contributing Factors

- Manual documentation maintenance
- No automated validation of path references
- Multiple sections describing the same content

---

## Acceptance Criteria

### Fix Verification

- [ ] All template paths use `.context/templates/worktracker/`
- [ ] No references to `docs/templates/worktracker/` remain
- [ ] Path references match actual filesystem location

### Quality Checklist

- [ ] Part of EN-202 rewrite deliverable
- [ ] All path references validated against filesystem
- [ ] Consistent path format throughout document

---

## Related Items

### Hierarchy

- **Parent:** [EN-202: CLAUDE.md Rewrite](./EN-202-claude-md-rewrite.md)

### Related Items

- **Discovered By:** [EN-201: Worktracker Skill Extraction](../EN-201-worktracker-skill-extraction/EN-201-worktracker-skill-extraction.md)
- **Evidence:** EN-201 QG-1 nse-qa-audit-v3.md (NCR-008)
- **Extracted Copy:** worktracker-templates.md (preserved both paths)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-01T14:30:00Z | Claude | pending | Initial report from EN-201 QG-1 |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Bug |
| **SAFe** | Defect |
| **JIRA** | Bug |
