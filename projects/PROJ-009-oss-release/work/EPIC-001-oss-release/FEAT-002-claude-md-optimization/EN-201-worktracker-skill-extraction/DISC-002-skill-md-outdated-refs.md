# EN-201:DISC-002: SKILL.md Had Outdated File References

<!--
TEMPLATE: Discovery
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9, worktracker.md (Discovery File)
CREATED: 2026-02-01 (EN-201 QG-2 Finding)
PURPOSE: Document finding about SKILL.md reference maintenance
-->

> **Type:** discovery
> **Status:** DOCUMENTED
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-01T15:00:00Z
> **Completed:** 2026-02-01T15:00:00Z
> **Parent:** EN-201
> **Owner:** Claude
> **Source:** EN-201 QG-2 integration-qa-report.md (FND-001)

---

## Summary

During QG-2 integration testing, the nse-qa agent discovered that SKILL.md contained references to non-existent rule files. The SKILL.md was referencing outdated file names from before the extraction refactoring, causing potential 404 errors when agents tried to load the rules.

**Key Findings:**
- SKILL.md referenced 3 files that didn't exist
- The actual rule files had different names
- This was a phase transition artifact (QG-1 to QG-2)

**Validation:** Confirmed by nse-qa QG-2 audit (FND-001 CRITICAL finding)

---

## Context

### Background

During EN-201 QG-1, the extraction process underwent 3 iterations. The original extraction created files with names like `worktracker-entity-rules.md`, but these were later refactored to `worktracker-entity-hierarchy.md` etc. The SKILL.md was not updated to reflect the new file names.

### Research Question

How do we prevent reference drift during multi-iteration extraction processes?

### Investigation Approach

1. Completed QG-1 with 3 iterations
2. Proceeded to QG-2 integration testing
3. nse-qa discovered SKILL.md pointed to wrong files
4. Fixed SKILL.md to reference actual files

---

## Finding

### Reference Mismatch Pattern

**SKILL.md Referenced (non-existent):**
```markdown
- worktracker-entity-rules.md
- worktracker-folder-structure-and-hierarchy-rules.md
- worktracker-template-usage-rules.md
```

**Actual Files (in skills/worktracker/rules/):**
```markdown
- worktracker-entity-hierarchy.md
- worktracker-directory-structure.md
- worktracker-templates.md
- worktracker-behavior-rules.md
- worktracker-system-mappings.md
```

**Key Observations:**
1. File naming evolved during QG-1 iterations
2. SKILL.md was created early and not updated
3. QG-2 integration testing caught the issue
4. Fix required updating SKILL.md "Additional Resources" section

### Root Cause

The QG-1 process focused on the rule file content and extraction fidelity. The SKILL.md references were not part of the QG-1 verification checklist. QG-2 integration testing, which validates "does the skill actually work?", caught the issue.

### Lesson Learned

**Cross-artifact reference validation should be part of QG-1**, not just content fidelity. When extraction produces multiple related files, all references between them must be verified.

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Audit Report | FND-001 finding | integration-qa-report.md | 2026-02-01 |
| E-002 | Before State | SKILL.md with wrong refs | skills/worktracker/SKILL.md (git history) | 2026-02-01 |
| E-003 | After State | SKILL.md with correct refs | skills/worktracker/SKILL.md | 2026-02-01 |

---

## Implications

### Impact on Project

This discovery highlights the importance of integration testing after extraction. QG-1 (content fidelity) is necessary but not sufficient; QG-2 (integration) catches reference errors.

### Design Decisions Affected

- **Decision:** Add cross-reference validation to QG-1 checklist
  - **Impact:** Prevents phase transition artifacts
  - **Rationale:** Earlier detection reduces rework

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Reference drift in multi-file extractions | Medium | Add reference validation to QG-1 |
| Silent failures when agents load skills | High | Integration testing (QG-2) |

### Recommendations

1. **Immediate:** Add "verify SKILL.md references" to extraction checklists
2. **Long-term:** Create automated validation that checks all relative links in markdown files

---

## Relationships

### Creates

- (none - fix was applied inline)

### Informs

- Future extraction enablers (EN-203, EN-204, etc.)
- Orchestration quality gate definitions

### Related Discoveries

- [DISC-001](./DISC-001-redundant-template-sections.md) - Related to content structure

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [EN-201](./EN-201-worktracker-skill-extraction.md) | Parent enabler |
| Evidence | quality-gates/qg-2/integration-qa-report.md | FND-001 finding |
| Fixed | skills/worktracker/SKILL.md | Corrected references |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-01T15:00:00Z | Claude | Created discovery |

---

## Metadata

```yaml
id: "EN-201:DISC-002"
parent_id: "EN-201"
work_type: DISCOVERY
title: "SKILL.md Had Outdated File References"
status: DOCUMENTED
priority: HIGH
impact: HIGH
created_by: "Claude"
created_at: "2026-02-01T15:00:00Z"
updated_at: "2026-02-01T15:00:00Z"
completed_at: "2026-02-01T15:00:00Z"
tags: [skill, reference, integration, qa]
source: "EN-201 QG-2"
finding_type: GAP
confidence_level: HIGH
validated: true
```
