# EN-202:BUG-003: Template path inconsistency in CLAUDE.md

<!--
TEMPLATE: Bug
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.10
CREATED: 2026-02-01 (EN-201 QG-1 Finding)
PURPOSE: Document defect requiring fix in CLAUDE.md rewrite
-->

> **Type:** bug
> **Status:** closed
> **Resolution:** fixed
> **Priority:** medium
> **Impact:** medium
> **Severity:** minor
> **Created:** 2026-02-01T14:30:00Z
> **Due:** -
> **Completed:** 2026-02-02T03:00:00Z
> **Parent:** EN-202
> **Owner:** Claude
> **Found In:** CLAUDE.md (current)
> **Fix Version:** EN-202

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Bug overview and key details |
| [Reproduction Steps](#reproduction-steps) | How to reproduce the bug |
| [Environment](#environment) | System configuration |
| [Evidence](#evidence) | Bug documentation and path verification |
| [Root Cause Analysis](#root-cause-analysis) | Cause identification |
| [Acceptance Criteria](#acceptance-criteria) | Fix verification |
| [Related Items](#related-items) | Hierarchy and references |
| [History](#history) | Change log |
| [System Mapping](#system-mapping) | External system mappings |

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

- [x] All template paths use `.context/templates/` (Navigation table line 26)
- [x] No references to `docs/templates/` in new CLAUDE.md
- [x] Path references match actual filesystem location

### Quality Checklist

- [x] Part of EN-202 rewrite deliverable
- [x] All path references validated against filesystem
- [x] Consistent path format throughout document

### Resolution

**Resolution:** FIXED - The new 80-line CLAUDE.md uses the correct `.context/templates/` path in the Navigation table (line 26). The conflicting `docs/templates/` references no longer exist because the detailed worktracker content was extracted to the `/worktracker` skill. Fix applied during TASK-002 (Navigation Section) in Phase 1.

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
| 2026-02-02T03:00:00Z | Claude | closed | FIXED in TASK-002 Navigation section. New CLAUDE.md uses `.context/templates/` consistently. |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Bug |
| **SAFe** | Defect |
| **JIRA** | Bug |
