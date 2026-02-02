# Audit Report: {{AUDIT_SCOPE}}

> **Type:** audit-report
> **Generated:** {{TIMESTAMP}}
> **Agent:** wt-auditor
> **Audit Type:** {{AUDIT_TYPE}}
> **Scope:** {{AUDIT_SCOPE}}

---

## Navigation

| Previous | Up | Next |
|----------|----|----- |
| [WTI_RULES.md](WTI_RULES.md) | [.context/templates](../..) | [VERIFICATION_REPORT.md](VERIFICATION_REPORT.md) |

---

## Summary

| Metric | Value |
|--------|-------|
| **Files Checked** | {{FILES_CHECKED}} |
| **Coverage** | {{COVERAGE_PCT}}% |
| **Total Issues** | {{TOTAL_ISSUES}} |
| **Errors** | {{ERROR_COUNT}} |
| **Warnings** | {{WARNING_COUNT}} |
| **Info** | {{INFO_COUNT}} |
| **Verdict** | {{PASSED_OR_FAILED}} |

---

## Issues Found

### Errors

| ID | File | Issue | Remediation |
|----|------|-------|-------------|
{{ERROR_TABLE}}

### Warnings

| ID | File | Issue | Remediation |
|----|------|-------|-------------|
{{WARNING_TABLE}}

### Info

| ID | File | Issue | Remediation |
|----|------|-------|-------------|
{{INFO_TABLE}}

---

## Remediation Plan

{{REMEDIATION_PLAN}}

---

## Files Audited

{{FILE_LIST}}

---

## Audit Scope Details

**Audit Type:** {{AUDIT_TYPE}}

**Scope Description:** {{AUDIT_SCOPE}}

**Coverage Analysis:**
- Total work items in scope: {{TOTAL_IN_SCOPE}}
- Work items audited: {{FILES_CHECKED}}
- Coverage percentage: {{COVERAGE_PCT}}%
- Files excluded: {{EXCLUDED_COUNT}} (see exclusion list below)

**Exclusion Criteria:**
{{EXCLUSION_CRITERIA}}

---

## Issue Categories

### WTI Rule Violations

Distribution of issues by Worktracker Integrity rule:

| Rule | Violations | Severity Breakdown |
|------|------------|-------------------|
{{WTI_VIOLATION_TABLE}}

### Structural Issues

| Issue Type | Count |
|------------|-------|
| Missing required sections | {{MISSING_SECTIONS_COUNT}} |
| Malformed YAML frontmatter | {{YAML_ERROR_COUNT}} |
| Broken relationships | {{BROKEN_REL_COUNT}} |
| Orphaned work items | {{ORPHAN_COUNT}} |

---

## Detailed Findings

### Critical Issues (Require Immediate Action)

{{CRITICAL_ISSUES_DETAIL}}

### High-Priority Issues

{{HIGH_PRIORITY_ISSUES_DETAIL}}

### Medium-Priority Issues

{{MEDIUM_PRIORITY_ISSUES_DETAIL}}

### Low-Priority Issues

{{LOW_PRIORITY_ISSUES_DETAIL}}

---

## Compliance Metrics

### Overall WTI Compliance

| Rule | Compliance % | Pass/Fail |
|------|--------------|-----------|
| WTI-001: Real-Time State | {{WTI_001_COMPLIANCE}}% | {{WTI_001_STATUS}} |
| WTI-002: No Closure Without Verification | {{WTI_002_COMPLIANCE}}% | {{WTI_002_STATUS}} |
| WTI-003: Truthful State | {{WTI_003_COMPLIANCE}}% | {{WTI_003_STATUS}} |
| WTI-004: Synchronize Before Reporting | {{WTI_004_COMPLIANCE}}% | {{WTI_004_STATUS}} |
| WTI-005: Atomic State Updates | {{WTI_005_COMPLIANCE}}% | {{WTI_005_STATUS}} |
| WTI-006: Evidence-Based Closure | {{WTI_006_COMPLIANCE}}% | {{WTI_006_STATUS}} |

**Overall Compliance:** {{OVERALL_COMPLIANCE}}%

---

## Recommendations

### Short-Term Actions (This Session)

{{SHORT_TERM_RECOMMENDATIONS}}

### Medium-Term Actions (This Week)

{{MEDIUM_TERM_RECOMMENDATIONS}}

### Long-Term Improvements (Systemic)

{{LONG_TERM_RECOMMENDATIONS}}

---

## Trends and Patterns

**Common Issues Identified:**

{{COMMON_ISSUES_ANALYSIS}}

**Root Cause Analysis:**

{{ROOT_CAUSE_ANALYSIS}}

**Preventative Measures:**

{{PREVENTATIVE_MEASURES}}

---

## Excluded Files

The following files were excluded from this audit:

{{EXCLUDED_FILES_LIST}}

**Exclusion Reasons:**
{{EXCLUSION_REASONS}}

---

## Audit Methodology

**Tools Used:**
- wt-auditor agent (version {{AGENT_VERSION}})
- WTI_RULES.md (version {{WTI_RULES_VERSION}})

**Validation Steps:**
1. File structure validation
2. YAML frontmatter parsing
3. Relationship graph verification
4. Evidence link validation
5. Status consistency checks
6. Parent-child synchronization
7. Acceptance criteria coverage

**Limitations:**
{{AUDIT_LIMITATIONS}}

---

## Next Steps

1. **Immediate:** {{IMMEDIATE_NEXT_STEP}}
2. **Follow-up:** {{FOLLOWUP_NEXT_STEP}}
3. **Re-audit:** {{REAUDIT_SCHEDULE}}

---

## Appendix

### Raw Audit Data

{{RAW_AUDIT_DATA_JSON}}

### Glossary

- **WTI:** Worktracker Integrity (rule set)
- **Compliance:** Percentage of work items following WTI rules
- **Coverage:** Percentage of in-scope work items audited
- **Verdict:** PASSED (no errors) or FAILED (errors found)

---

## Template Usage Instructions

**For wt-auditor agent:**

Replace placeholders with actual audit data:

| Placeholder | Type | Example |
|-------------|------|---------|
| `{{TIMESTAMP}}` | ISO8601 | `2026-02-02T14:30:00Z` |
| `{{AUDIT_TYPE}}` | String | `full-epic`, `partial-feature`, `single-item` |
| `{{AUDIT_SCOPE}}` | String | `EPIC-001-oss-release` |
| `{{FILES_CHECKED}}` | Integer | `42` |
| `{{COVERAGE_PCT}}` | Float | `95.2` |
| `{{TOTAL_ISSUES}}` | Integer | `7` |
| `{{ERROR_COUNT}}` | Integer | `2` |
| `{{WARNING_COUNT}}` | Integer | `4` |
| `{{INFO_COUNT}}` | Integer | `1` |
| `{{PASSED_OR_FAILED}}` | String | `PASSED` or `FAILED` |
| `{{ERROR_TABLE}}` | Markdown table | See example below |
| `{{WARNING_TABLE}}` | Markdown table | See example below |
| `{{INFO_TABLE}}` | Markdown table | See example below |
| `{{REMEDIATION_PLAN}}` | Markdown list | Prioritized action items |
| `{{FILE_LIST}}` | Markdown list | Bullet list of audited files |

**Example ERROR_TABLE:**
```markdown
| E-001 | EN-002-example.md | WTI-002 violation: DONE without evidence | Add evidence links to Evidence section |
| E-002 | FEAT-001-example.md | WTI-005 violation: Parent-child mismatch | Synchronize child status in parent file |
```

**Example REMEDIATION_PLAN:**
```markdown
1. **Critical (E-001, E-002):** Revert EN-002 to IN_PROGRESS until evidence added; synchronize FEAT-001
2. **High (W-001, W-002):** Add missing acceptance criteria to EN-003 and EN-004
3. **Medium (W-003):** Fix typo in EPIC-001 title
4. **Info (I-001):** Consider splitting large FEAT-002 into multiple features
```

---

*Template Version: 1.0*
*Last Updated: 2026-02-02*
*Design Source: synthesis-worktracker-agent-design.md (lines 607-667)*
