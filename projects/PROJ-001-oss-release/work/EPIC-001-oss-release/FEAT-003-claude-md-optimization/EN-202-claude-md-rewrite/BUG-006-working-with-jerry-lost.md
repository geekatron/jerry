# EN-202:BUG-006: Working with Jerry Section Lost (46 Lines)

<!--
TEMPLATE: Bug
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.10
CREATED: 2026-02-02 (Gap Analysis GAP-003)
PURPOSE: Document critical gap - Working with Jerry operational guidance completely lost
-->

> **Type:** bug
> **Status:** closed
> **Resolution:** fixed
> **Priority:** critical
> **Impact:** critical
> **Severity:** major
> **Created:** 2026-02-02T05:00:00Z
> **Due:** 2026-02-03T00:00:00Z
> **Completed:** 2026-02-02T06:00:00Z
> **Parent:** EN-202
> **Owner:** Claude
> **Found In:** CLAUDE.md (rewritten)
> **Fix Version:** EN-202

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Bug overview and key details |
| [Reproduction Steps](#reproduction-steps) | How to identify the gap |
| [Environment](#environment) | System configuration |
| [Evidence](#evidence) | Gap analysis documentation |
| [Root Cause Analysis](#root-cause-analysis) | Cause identification |
| [Fix Description](#fix-description) | Required remediation |
| [Acceptance Criteria](#acceptance-criteria) | Fix verification |
| [Related Items](#related-items) | Hierarchy and references |
| [History](#history) | Change log |
| [System Mapping](#system-mapping) | External system mappings |

---

## Summary

The "Working with Jerry" section (lines 475-520, **46 lines**) was **COMPLETELY LOST** during the CLAUDE.md rewrite. This section contains critical operational guidance including Before/During/After work workflows and project creation steps. Only partial coverage exists in the Active Project section.

**Key Details:**
- **Symptom:** New sessions lack step-by-step operational workflow guidance
- **Frequency:** Every new session or contributor - no Before/During/After guidance
- **Workaround:** Partial - Active Project section covers project selection but not workflow

---

## Reproduction Steps

### Prerequisites

Access to gap analysis traceability matrix and both CLAUDE.md versions.

### Steps to Reproduce

1. Open new CLAUDE.md (80 lines)
2. Search for "Before Starting Work" - no results
3. Search for "During Work" - no results
4. Search for "After Completing Work" - no results
5. Search for "Creating a New Project" - no results
6. Compare with CLAUDE.md.backup lines 475-520 - content completely missing

### Expected Result

Operational workflow guidance should be preserved either:
- In CLAUDE.md (condensed)
- In a dedicated `.claude/rules/project-workflow.md` file
- In the worktracker skill

### Actual Result

Content is completely missing. Active Project section covers hook output interpretation but lacks workflow steps.

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | Any |
| **Browser/Runtime** | N/A (documentation file) |
| **Application Version** | CLAUDE.md (rewritten) |
| **Configuration** | Default |
| **Deployment** | Repository root |

---

## Evidence

### Bug Documentation

| Evidence | Type | Description | Date |
|----------|------|-------------|------|
| Gap Analysis traceability-matrix.md | Report | GAP-003 identified (CRITICAL) | 2026-02-02 |
| CLAUDE.md.backup lines 475-520 | Source | Original 46 lines | 2026-02-02 |
| New CLAUDE.md | Verification | Content absent | 2026-02-02 |

### Lost Content (46 lines)

```markdown
## Working with Jerry

### Project-Based Workflow

Jerry uses isolated project workspaces. Each project has its own `PLAN.md` and `WORKTRACKER.md`.

**Active Project Resolution:**
1. Set `JERRY_PROJECT` environment variable (e.g., `export JERRY_PROJECT=PROJ-001-plugin-cleanup`)
2. If not set, Claude will prompt you to specify which project to work on
3. See `projects/README.md` for the project registry

**Project Structure:**
```
projects/PROJ-{nnn}-{slug}/
├── PLAN.md              # Project implementation plan
├── WORKTRACKER.md       # Work tracking document
└── .jerry/data/items/   # Operational state (work items)
```

### Before Starting Work

1. Set `JERRY_PROJECT` environment variable for your target project
2. Check `projects/${JERRY_PROJECT}/PLAN.md` for current plan
3. Review `projects/${JERRY_PROJECT}/WORKTRACKER.md` for task state
4. Read relevant `docs/knowledge/` for domain context

### During Work

1. Use Work Tracker to persist task state to `projects/${JERRY_PROJECT}/WORKTRACKER.md`
2. Update PLAN.md as implementation progresses
3. Document decisions in `docs/design/`

### After Completing Work

1. Update Work Tracker with completion status
2. Capture learnings in `docs/experience/` or `docs/wisdom/`
3. Commit with clear, semantic messages

### Creating a New Project

1. Check `projects/README.md` for next project number
2. Create directory: `mkdir -p projects/PROJ-{nnn}-{slug}/.jerry/data/items`
3. Create `PLAN.md` and `WORKTRACKER.md`
4. Add entry to `projects/README.md`
5. Set `JERRY_PROJECT` environment variable
```

---

## Root Cause Analysis

### Root Cause

The "Working with Jerry" section was not identified for preservation during the CLAUDE.md rewrite. It was incorrectly assumed that the Active Project section adequately covered this content, but Active Project only covers hook output interpretation, not workflow steps.

### Contributing Factors

- Active Project section overlap led to false assumption of coverage
- Before/During/After workflow guidance is operational, not just structural
- No specific task to "preserve workflow guidance" in EN-202

---

## Fix Description

### Solution Approach

Create `.claude/rules/project-workflow.md` containing the Before/During/After work guidance. This file will be auto-loaded by Claude Code's `.claude/rules/` mechanism.

### Required Changes

1. Create `.claude/rules/project-workflow.md` with full content
2. Include Before Starting Work steps
3. Include During Work steps
4. Include After Completing Work steps
5. Include Creating a New Project steps
6. Also include AskUserQuestion Flow (GAP-005) since related

### Target File

`.claude/rules/project-workflow.md`

---

## Acceptance Criteria

### Fix Verification

- [ ] "Before Starting Work" 4 steps preserved
- [ ] "During Work" 3 steps preserved
- [ ] "After Completing Work" 3 steps preserved
- [ ] "Creating a New Project" 5 steps preserved
- [ ] Project structure diagram preserved
- [ ] File placed in `.claude/rules/` for auto-loading

### Quality Checklist

- [ ] Content matches original CLAUDE.md.backup lines 475-520
- [ ] Rules file follows `.claude/rules/` formatting conventions
- [ ] No operational guidance lost
- [ ] File is auto-loaded by Claude Code

---

## Related Items

### Hierarchy

- **Parent:** [EN-202: CLAUDE.md Rewrite](./EN-202-claude-md-rewrite.md)

### Related Items

- **Gap Analysis:** [traceability-matrix.md](./gap-analysis/traceability-matrix.md) (GAP-003)
- **Related Gap:** GAP-005 (AskUserQuestion Flow) - should be combined in same file
- **Original Source:** CLAUDE.md.backup lines 475-520
- **Partial Coverage:** Active Project section (CLAUDE.md lines 32-44)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-02T05:00:00Z | Claude | pending | Initial report from gap analysis (GAP-003) |
| 2026-02-02T06:00:00Z | Claude | closed | FIXED: Created `.claude/rules/project-workflow.md` with Before/During/After work guidance (46 lines) preserved. |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Bug |
| **SAFe** | Defect |
| **JIRA** | Bug |
