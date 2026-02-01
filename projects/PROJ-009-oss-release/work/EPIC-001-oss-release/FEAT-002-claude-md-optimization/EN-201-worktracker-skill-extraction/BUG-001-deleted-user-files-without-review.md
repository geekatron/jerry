# EN-201:BUG-001: Deleted User's Manual Files Without Proper Review

<!--
TEMPLATE: Bug
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.10
CREATED: 2026-02-01 (User feedback)
PURPOSE: Document process failure in EN-201 extraction
-->

> **Type:** bug
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-02-01T16:00:00Z
> **Due:** -
> **Completed:** 2026-02-01T16:30:00Z
> **Parent:** EN-201
> **Owner:** Claude
> **Found In:** EN-201 QG-1 Iteration 2
> **Fix Version:** EN-201

---

## Summary

During EN-201 QG-1 Iteration 2, Claude deleted 3 files created by the user without properly reviewing their content. The nse-qa audit flagged them as "obsolete" because they didn't match the new naming convention, but the files contained:
1. **Valuable content not in CLAUDE.md** (project-based vs repository-based hierarchy)
2. **Corrected bugs** (template path was correct in user's file)
3. **Cleaner formatting** (better table structure)

**Key Details:**
- **Symptom:** User's manual decomposition work was discarded
- **Frequency:** One-time process failure
- **Workaround:** Content recoverable from git history

---

## Files Deleted

| File | Status | Notable Content |
|------|--------|-----------------|
| `worktracker-entity-rules.md` | Content preserved | Same as CLAUDE.md, split into two files |
| `worktracker-folder-structure-and-hierarchy-rules.md` | **CONTENT LOST** | Project-based vs Repository-based hierarchy NOT in CLAUDE.md |
| `worktracker-template-usage-rules.md` | Better version discarded | Correct paths, cleaner format |

---

## Root Cause Analysis

### Investigation Summary

The nse-qa QG-1 audit identified 3 files that didn't match the naming scheme and flagged them as NCR-006 (obsolete files). Claude deleted them without:
1. Reading the file contents
2. Comparing to extracted content
3. Checking if they had unique value
4. Asking the user about their purpose

### Root Cause

**Process failure:** Trusted audit recommendation without verification. The audit correctly identified naming mismatch but incorrectly labeled them "obsolete" (implying no value).

### Contributing Factors

- Adversarial review protocol focused on compliance, not content value
- No "compare before delete" step in remediation process
- Assumption that all worktracker content was in CLAUDE.md
- Did not recognize these were user-authored additions

---

## Content Lost

### Project-based vs Repository-based Hierarchy

This content was in user's `worktracker-folder-structure-and-hierarchy-rules.md` but NOT in CLAUDE.md:

```markdown
## Project-based Folder Structure and Hierarchy (ONE-OF)

Used for by projects like Forge that require project based work tracking hierarchy.

{RepositoryRoot}/
└── projects/
    └── {ProjectId}/
        ├── PLAN.md
        └── {WORKTRACKER Directory Structure}/

## Repository-based Folder Structure and Hierarchy (ONE-OF)

Used projects that require repository based work tracking hierarchy.

{RepositoryRoot}/
└── {WORKTRACKER Directory Structure}/
```

This documents TWO alternative patterns for worktracker placement that should be preserved.

---

## Fix Description

### Solution Approach

1. Recover lost content from git history
2. Merge into existing `worktracker-directory-structure.md`
3. Update SKILL.md if needed
4. Document lesson learned in DEC-003

### Changes Made

- [x] Add "Project-based vs Repository-based" section to `worktracker-directory-structure.md`
- [x] Verify template path is correct in `worktracker-templates.md` (already documented as BUG-003 for EN-202)
- [ ] Create DEC-003 documenting "compare before delete" lesson (deferred - captured in this bug)

---

## Acceptance Criteria

### Fix Verification

- [ ] Lost content merged into appropriate rule file
- [ ] User confirms content is preserved
- [ ] Process lesson documented

### Quality Checklist

- [ ] No content lost from user's work
- [ ] Documentation reflects both hierarchy patterns

---

## Related Items

### Hierarchy

- **Parent:** [EN-201: Worktracker Skill Extraction](./EN-201-worktracker-skill-extraction.md)

### Related Items

- **Recovery Source:** Git commit `dbe2d16b79e3329db3abbc83c5d179d7d9a551d9^`
- **Related Bug:** [EN-202:BUG-003](../EN-202-claude-md-rewrite/BUG-003-template-path-inconsistency.md) - User's file had correct path

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-01T16:00:00Z | Claude | in_progress | Bug identified by user feedback |
| 2026-02-01T16:30:00Z | Claude | completed | Recovered content from git, merged into worktracker-directory-structure.md |

---

## Lesson Learned

**ALWAYS compare content before deleting files, even if an audit recommends removal.** The audit identified naming non-compliance, not content value. Files may contain:
- Unique content not in other sources
- Corrections to known bugs
- Better formatting or structure
- User's manual work that shouldn't be discarded
