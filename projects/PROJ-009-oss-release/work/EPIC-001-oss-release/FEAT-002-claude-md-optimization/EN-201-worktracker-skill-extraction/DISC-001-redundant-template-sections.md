# EN-201:DISC-001: Redundant Template Sections in CLAUDE.md

<!--
TEMPLATE: Discovery
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9, worktracker.md (Discovery File)
CREATED: 2026-02-01 (EN-201 QG-1 Finding)
PURPOSE: Document finding about redundant content in CLAUDE.md
-->

> **Type:** discovery
> **Status:** DOCUMENTED
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-02-01T14:30:00Z
> **Completed:** 2026-02-01T14:30:00Z
> **Parent:** EN-201
> **Owner:** Claude
> **Source:** EN-201 QG-1 nse-qa-audit-v3.md (F-001)

---

## Summary

CLAUDE.md contains duplicated template content. Lines 9-31 and lines 35-117 in the `worktracker-templates.md` extraction contain overlapping information about worktracker templates, increasing cognitive load and document size.

**Key Findings:**
- Two separate sections describe the same template directory
- Both sections list the same 10 template files
- Content was faithfully extracted but represents source redundancy

**Validation:** Confirmed by nse-qa QG-1 audit (F-001 IMPROVEMENT finding)

---

## Context

### Background

During EN-201 Worktracker Skill Extraction, the extraction process faithfully preserved all content from CLAUDE.md's `<worktracker>` section. This included two separate template documentation sections that were already redundant in the source.

### Research Question

Why does CLAUDE.md have two sections describing worktracker templates, and should they be consolidated?

### Investigation Approach

1. Extracted `<worktracker>` content from CLAUDE.md
2. Created `worktracker-templates.md` rule file
3. nse-qa QG-1 audit identified duplicated content

---

## Finding

### Content Duplication Pattern

**First Section (lines 9-31 of extraction):**
```markdown
## Work Tracker (worktracker) Templates

Description:
- Work tracker (worktracker) templates are stored in the `docs/templates/worktracker/` folder.
- These templates provide a standardized structure...
```

**Second Section (lines 35-117 of extraction):**
```markdown
## Templates (MANDATORY)

> **CRITICAL:** You MUST use the repository templates...

### Work Tracker (worktracker) Templates

**Location:** `.context/templates/worktracker/`

Description:
- Work tracker (worktracker) templates are stored in the `docs/templates/worktracker/` folder.
```

**Key Observations:**
1. Both sections list the same 10 template files (BUG.md, DECISION.md, etc.)
2. Both sections include a directory structure ASCII diagram
3. The second section adds mandatory usage rules not present in the first
4. Path inconsistency exists between the sections (see BUG-003)

### Impact Analysis

| Metric | Value |
|--------|-------|
| Duplicated lines | ~60 lines |
| Token overhead | ~1,500 tokens |
| Cognitive load | Medium (readers may wonder if sections differ) |

### Validation

The nse-qa QG-1 audit documented this as F-001 (IMPROVEMENT finding):
> "worktracker-templates.md contains duplicated content (lines 9-31 vs 35-117) - faithfully preserved from source but increases cognitive load"

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Audit Report | F-001 finding | nse-qa-audit-v3.md | 2026-02-01 |
| E-002 | Source File | Original CLAUDE.md | CLAUDE.md lines 244-356 | 2026-02-01 |
| E-003 | Extracted File | worktracker-templates.md | skills/worktracker/rules/ | 2026-02-01 |

---

## Implications

### Impact on Project

This discovery confirms that CLAUDE.md content needs consolidation during EN-202 rewrite. The redundancy contributes to the 914-line count and ~10,000 token load.

### Design Decisions Affected

- **Decision:** EN-202 should consolidate template documentation
  - **Impact:** Reduce template section from ~120 lines to ~30 lines
  - **Rationale:** Eliminate redundancy, reduce token count

### Recommendations

During EN-202 CLAUDE.md Rewrite:
1. Keep only the "Templates (MANDATORY)" section
2. Remove the earlier descriptive section
3. Fix the path inconsistency (BUG-003)
4. Point to skill rule file for detailed structure

---

## Relationships

### Creates

- [EN-202:BUG-003](../EN-202-claude-md-rewrite/BUG-003-template-path-inconsistency.md) - Path inconsistency fix

### Informs

- [EN-202: CLAUDE.md Rewrite](../EN-202-claude-md-rewrite/EN-202-claude-md-rewrite.md) - Consolidation target

### Related Discoveries

- (none)

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [EN-201](./EN-201-worktracker-skill-extraction.md) | Parent enabler |
| Evidence | quality-gates/qg-1/nse-qa-audit-v3.md | F-001 finding |
| Extracted | skills/worktracker/rules/worktracker-templates.md | Preserved redundancy |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-01T14:30:00Z | Claude | Created discovery |

---

## Metadata

```yaml
id: "EN-201:DISC-001"
parent_id: "EN-201"
work_type: DISCOVERY
title: "Redundant Template Sections in CLAUDE.md"
status: DOCUMENTED
priority: MEDIUM
impact: MEDIUM
created_by: "Claude"
created_at: "2026-02-01T14:30:00Z"
updated_at: "2026-02-01T14:30:00Z"
completed_at: "2026-02-01T14:30:00Z"
tags: [redundancy, template, claude-md]
source: "EN-201 QG-1"
finding_type: GAP
confidence_level: HIGH
validated: true
```
