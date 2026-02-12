# EN-202:BUG-007: Problem-Solving Templates Reference Lost (18 Lines)

<!--
TEMPLATE: Bug
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.10
CREATED: 2026-02-02 (Gap Analysis GAP-004)
PURPOSE: Document high-severity gap - Problem-solving templates reference not preserved
-->

> **Type:** bug
> **Status:** closed
> **Resolution:** fixed
> **Priority:** high
> **Impact:** medium
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

The "Problem-Solving & Knowledge Templates" subsection (lines 303-320, 18 lines) was not preserved during the CLAUDE.md rewrite. This section documents the location and purpose of templates in `docs/knowledge/exemplars/templates/` including ADR, research, analysis, synthesis, review, and investigation templates.

**Key Details:**
- **Symptom:** Users looking for problem-solving templates won't find location guidance
- **Frequency:** When creating ADRs, research docs, or analysis artifacts
- **Workaround:** Templates exist but location is not documented

---

## Reproduction Steps

### Prerequisites

Access to gap analysis traceability matrix and both CLAUDE.md versions.

### Steps to Reproduce

1. Open new CLAUDE.md (80 lines)
2. Search for "Problem-Solving & Knowledge Templates" - no results
3. Search for "docs/knowledge/exemplars/templates" - no results
4. Search for "adr.md" template reference - no results
5. Compare with CLAUDE.md.backup lines 303-320 - content missing

### Expected Result

Problem-solving templates reference should be preserved either:
- In CLAUDE.md Templates section
- In `/problem-solving` skill documentation
- In a separate templates navigation

### Actual Result

Only worktracker templates are documented. Problem-solving templates location is not referenced.

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
| Gap Analysis traceability-matrix.md | Report | GAP-004 identified (HIGH) | 2026-02-02 |
| CLAUDE.md.backup lines 303-320 | Source | Original 18 lines | 2026-02-02 |
| New CLAUDE.md | Verification | Content absent | 2026-02-02 |

### Lost Content (18 lines)

```markdown
### Problem-Solving & Knowledge Templates

**Location:** `docs/knowledge/exemplars/templates/`

Templates for problem-solving artifacts and knowledge documents:

| Template | Use For | Path |
|----------|---------|------|
| `adr.md` | Architecture Decision Records | `docs/knowledge/exemplars/templates/adr.md` |
| `research.md` | Research artifacts | `docs/knowledge/exemplars/templates/research.md` |
| `analysis.md` | Analysis artifacts | `docs/knowledge/exemplars/templates/analysis.md` |
| `deep-analysis.md` | Deep analysis | `docs/knowledge/exemplars/templates/deep-analysis.md` |
| `synthesis.md` | Synthesis documents | `docs/knowledge/exemplars/templates/synthesis.md` |
| `review.md` | Review artifacts | `docs/knowledge/exemplars/templates/review.md` |
| `investigation.md` | Investigation reports | `docs/knowledge/exemplars/templates/investigation.md` |
| `jrn.md` | Journal entries | `docs/knowledge/exemplars/templates/jrn.md` |
| `use-case-template.md` | Use case specifications | `docs/knowledge/exemplars/templates/use-case-template.md` |
```

---

## Root Cause Analysis

### Root Cause

The Templates section in the CLAUDE.md rewrite focused exclusively on worktracker templates. The Problem-Solving & Knowledge Templates subsection was overlooked during content inventory and not included in extraction planning.

### Contributing Factors

- Templates section extraction focused on worktracker
- Problem-solving templates are used by `/problem-solving` skill but not documented there
- No cross-reference verification performed

---

## Fix Description

### Solution Approach

Add problem-solving templates reference to the `/problem-solving` skill SKILL.md or create a dedicated templates section.

### Required Changes

Option A (Preferred): Add to `/problem-solving` SKILL.md
- Add "Templates" section referencing `docs/knowledge/exemplars/templates/`
- Include the full template table

Option B: Add to CLAUDE.md Navigation table
- Add row pointing to templates location

### Target File

`skills/problem-solving/SKILL.md` (Option A) or CLAUDE.md (Option B)

---

## Acceptance Criteria

### Fix Verification

- [ ] Problem-solving templates location documented
- [ ] Template table with 9 entries preserved
- [ ] ADR, research, analysis, synthesis, review, investigation templates listed
- [ ] Path references accurate

### Quality Checklist

- [ ] Content matches original CLAUDE.md.backup lines 303-320
- [ ] Template paths verified to exist
- [ ] Users can discover templates through documented location

---

## Related Items

### Hierarchy

- **Parent:** [EN-202: CLAUDE.md Rewrite](./EN-202-claude-md-rewrite.md)

### Related Items

- **Gap Analysis:** [traceability-matrix.md](./gap-analysis/traceability-matrix.md) (GAP-004)
- **Original Source:** CLAUDE.md.backup lines 303-320
- **Target Skill:** `/problem-solving`
- **Template Location:** `docs/knowledge/exemplars/templates/`

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-02T05:00:00Z | Claude | pending | Initial report from gap analysis (GAP-004) |
| 2026-02-02T06:00:00Z | Claude | closed | FIXED: Added Templates section to `skills/problem-solving/SKILL.md` with all 9 template references. |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Bug |
| **SAFe** | Defect |
| **JIRA** | Bug |
