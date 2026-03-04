# WT Auditor: Audit Report Output Template

> Template for audit report output format. Loaded by wt-auditor when generating reports. Canonical template at `.context/templates/worktracker/AUDIT_REPORT.md`.

```markdown
# Audit Report: {AUDIT_SCOPE}

> **Type:** audit-report
> **Generated:** {ISO-8601-timestamp}
> **Agent:** wt-auditor
> **Audit Type:** {full|templates|relationships|orphans|status|id_format}
> **Scope:** {path-audited}

---

## Summary

| Metric | Value |
|--------|-------|
| **Files Checked** | {count} |
| **Coverage** | {percentage}% |
| **Total Issues** | {count} |
| **Errors** | {count} |
| **Warnings** | {count} |
| **Info** | {count} |
| **Verdict** | {PASSED|FAILED} |

---

## Issues Found

### Errors

| ID | File | Issue | Remediation |
|----|------|-------|-------------|
| E-001 | EN-001-example.md | Missing "Acceptance Criteria" section | Add section per template |
| E-002 | TASK-003-test.md | Parent FEAT-999 does not exist | Update parent_id to valid parent |

### Warnings

| ID | File | Issue | Remediation |
|----|------|-------|-------------|
| W-001 | EN-005-orphan.md | Not linked from any parent | Link from FEAT-002 Children section |

### Info

| ID | File | Issue | Remediation |
|----|------|-------|-------------|
| I-001 | TASK-1-bad.md | ID missing leading zeros | Rename to TASK-001-bad.md |

---

## Remediation Plan

1. **E-001 (Effort: low):** Add "Acceptance Criteria" section to EN-001-example.md
2. **E-002 (Effort: medium):** Create FEAT-999 or update TASK-003 parent_id
3. **W-001 (Effort: low):** Add EN-005 to FEAT-002 Children list

---

## Files Audited

- projects/PROJ-009/work/EPIC-001/EPIC-001-oss-release.md
- projects/PROJ-009/work/EPIC-001/FEAT-001-worktracker/FEAT-001-worktracker.md
- projects/PROJ-009/work/EPIC-001/FEAT-001-worktracker/EN-001-example/EN-001-example.md
- ... (total: {count} files)
```
