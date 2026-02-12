# EN-202:BUG-008: AskUserQuestion Flow Lost (24 Lines)

<!--
TEMPLATE: Bug
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.10
CREATED: 2026-02-02 (Gap Analysis GAP-005)
PURPOSE: Document high-severity gap - AskUserQuestion project selection flow not preserved
-->

> **Type:** bug
> **Status:** closed
> **Resolution:** fixed
> **Priority:** high
> **Impact:** high
> **Severity:** minor
> **Created:** 2026-02-02T05:00:00Z
> **Due:** 2026-02-05T00:00:00Z
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

The "Required AskUserQuestion Flow" subsection (lines 604-627, 24 lines) was not preserved during the CLAUDE.md rewrite. This section provides explicit instructions for how Claude should handle project selection when `<project-required>` or `<project-error>` tags are received, including the exact AskUserQuestion structure to use.

**Key Details:**
- **Symptom:** Claude may not know exact flow for project selection prompts
- **Frequency:** When JERRY_PROJECT is not set and project selection is needed
- **Workaround:** Partial - Active Project section mentions hook tags but lacks detail

---

## Reproduction Steps

### Prerequisites

Access to gap analysis traceability matrix and both CLAUDE.md versions.

### Steps to Reproduce

1. Open new CLAUDE.md (80 lines)
2. Search for "Required AskUserQuestion Flow" - no results
3. Search for "Parse the available projects" - no results
4. Search for "Create new project option" - no results
5. Compare with CLAUDE.md.backup lines 604-627 - content missing

### Expected Result

AskUserQuestion flow guidance should be preserved either:
- In Active Project section (detailed)
- In a dedicated `.claude/rules/project-workflow.md` file
- In project selection documentation

### Actual Result

Active Project section only shows hook tag meanings and basic actions. Detailed AskUserQuestion flow with example structure is missing.

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
| Gap Analysis traceability-matrix.md | Report | GAP-005 identified (HIGH) | 2026-02-02 |
| CLAUDE.md.backup lines 604-627 | Source | Original 24 lines | 2026-02-02 |
| New CLAUDE.md | Verification | Content absent | 2026-02-02 |

### Lost Content (24 lines)

```markdown
### Required AskUserQuestion Flow

When `<project-required>` or `<project-error>` is received, Claude **MUST**:

1. **Parse** the available projects from the hook output
2. **Present options** via `AskUserQuestion`:
   - List available projects (from `AvailableProjects`)
   - Offer "Create new project" option
3. **Handle response**:
   - If existing project selected → instruct user to set `JERRY_PROJECT`
   - If new project → guide through creation flow
4. **DO NOT** proceed with unrelated work until resolved

Example AskUserQuestion structure:
```yaml
question: "Which project would you like to work on?"
header: "Project"
options:
  - label: "PROJ-001-plugin-cleanup"
    description: "[ACTIVE] Plugin system cleanup and refactoring"
  - label: "PROJ-002-example"
    description: "[DRAFT] Example project description"
  - label: "Create new project"
    description: "Start a new project workspace"
```
```

---

## Root Cause Analysis

### Root Cause

The Project Enforcement section was condensed during rewrite, keeping only the hook tag interpretation table. The detailed AskUserQuestion flow instructions and example structure were not identified as critical behavioral content.

### Contributing Factors

- Active Project section focuses on "what to do" not "how to do it"
- AskUserQuestion example structure is implementation detail that was overlooked
- No explicit task to "preserve project selection flow"

---

## Fix Description

### Solution Approach

Include AskUserQuestion flow in `.claude/rules/project-workflow.md` alongside the Before/During/After work guidance (BUG-006).

### Required Changes

1. Add to `.claude/rules/project-workflow.md` (same file as BUG-006 fix)
2. Include the 4-step flow
3. Include the AskUserQuestion example structure
4. Reference from Active Project section if needed

### Target File

`.claude/rules/project-workflow.md`

---

## Acceptance Criteria

### Fix Verification

- [ ] 4-step AskUserQuestion flow preserved
- [ ] Parse step documented
- [ ] Present options step with requirements documented
- [ ] Handle response step with both paths documented
- [ ] Example AskUserQuestion YAML structure preserved
- [ ] "DO NOT proceed" warning preserved

### Quality Checklist

- [ ] Content matches original CLAUDE.md.backup lines 604-627
- [ ] Combined with BUG-006 fix in same file
- [ ] Flow is actionable and specific

---

## Related Items

### Hierarchy

- **Parent:** [EN-202: CLAUDE.md Rewrite](./EN-202-claude-md-rewrite.md)

### Related Items

- **Gap Analysis:** [traceability-matrix.md](./gap-analysis/traceability-matrix.md) (GAP-005)
- **Related Bug:** [BUG-006](./BUG-006-working-with-jerry-lost.md) - combine in same fix file
- **Original Source:** CLAUDE.md.backup lines 604-627
- **Partial Coverage:** Active Project section (CLAUDE.md lines 36-42)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-02T05:00:00Z | Claude | pending | Initial report from gap analysis (GAP-005) |
| 2026-02-02T06:00:00Z | Claude | closed | FIXED: Added to `.claude/rules/project-workflow.md` with full AskUserQuestion flow (24 lines) and example YAML. |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Bug |
| **SAFe** | Defect |
| **JIRA** | Bug |
