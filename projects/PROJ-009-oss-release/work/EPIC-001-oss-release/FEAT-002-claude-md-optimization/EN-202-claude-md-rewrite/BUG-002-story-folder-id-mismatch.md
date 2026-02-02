# EN-202:BUG-002: Story folder uses {EnablerId} instead of {StoryId}

<!--
TEMPLATE: Bug
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.10
CREATED: 2026-02-01 (EN-201 QG-1 Finding)
PURPOSE: Document defect requiring fix in CLAUDE.md rewrite
-->

> **Type:** bug
> **Status:** closed
> **Resolution:** not_applicable
> **Priority:** medium
> **Impact:** medium
> **Severity:** minor
> **Created:** 2026-02-01T14:30:00Z
> **Due:** -
> **Completed:** 2026-02-02T04:00:00Z
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
| [Evidence](#evidence) | Bug documentation |
| [Root Cause Analysis](#root-cause-analysis) | Cause identification |
| [Acceptance Criteria](#acceptance-criteria) | Fix verification |
| [Related Items](#related-items) | Hierarchy and references |
| [History](#history) | Change log |
| [System Mapping](#system-mapping) | External system mappings |

---

## Summary

CLAUDE.md line 232 incorrectly documents Story folder naming as `{EnablerId}-{slug}` instead of `{StoryId}-{slug}`. This creates inconsistency between Enabler and Story folder naming conventions.

**Key Details:**
- **Symptom:** Copy-paste error in folder naming convention documentation
- **Frequency:** Consistent (present in source)
- **Workaround:** Follow correct pattern ({StoryId}-{slug} for Story folders)

---

## Reproduction Steps

### Prerequisites

Access to CLAUDE.md in repository root.

### Steps to Reproduce

1. Open CLAUDE.md
2. Navigate to line 232 (in `<worktracker>` section)
3. Observe text: "A folder (`{EnablerId}-{slug}`) is created for each Story..."

### Expected Result

Text should read: "A folder (`{StoryId}-{slug}`) is created for each Story..."

### Actual Result

Text incorrectly uses `{EnablerId}` for Story folders.

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
| EN-201 QG-1 nse-qa-audit-v3.md | Report | NCR-010/BUG-002 identified | 2026-02-01 |
| CLAUDE.md line 232 | Source | Actual error location | 2026-02-01 |
| worktracker-behavior-rules.md line 24 | Extraction | Faithfully preserved source defect | 2026-02-01 |

---

## Root Cause Analysis

### Root Cause

Copy-paste error when duplicating the Enabler folder pattern to create the Story folder documentation. The author copied the Enabler section and changed "Enabler" to "Story" in the description but forgot to change `{EnablerId}` to `{StoryId}`.

### Contributing Factors

- Similar structure between Enabler and Story sections
- Manual documentation without validation

---

## Acceptance Criteria

### Fix Verification

- [x] N/A - Content containing error was removed in rewrite (worktracker section extracted to skill)
- [x] New CLAUDE.md has no directory structure content

### Quality Checklist

- [x] Part of EN-202 rewrite deliverable
- [x] No similar copy-paste errors exist

### Resolution

**Resolution:** NOT_APPLICABLE - The worktracker directory structure content containing this error was extracted to the `/worktracker` skill during EN-201. The new 80-line CLAUDE.md does not include this content, so the bug no longer applies. Note: The fix should be applied in the extracted worktracker skill rules file (`skills/worktracker/rules/worktracker-folder-structure-and-hierarchy-rules.md`) as a separate task.

---

## Related Items

### Hierarchy

- **Parent:** [EN-202: CLAUDE.md Rewrite](./EN-202-claude-md-rewrite.md)

### Related Items

- **Discovered By:** [EN-201: Worktracker Skill Extraction](../EN-201-worktracker-skill-extraction/EN-201-worktracker-skill-extraction.md)
- **Evidence:** EN-201 QG-1 nse-qa-audit-v3.md (NCR-010)
- **Extracted Copy:** worktracker-behavior-rules.md line 24 (preserved source defect)

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
