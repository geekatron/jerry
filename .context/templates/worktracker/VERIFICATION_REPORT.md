# Verification Report: {{WORK_ITEM_ID}}

> **Type:** verification-report
> **Generated:** {{TIMESTAMP}}
> **Agent:** wt-verifier
> **Scope:** {{VERIFICATION_SCOPE}}

---

## Navigation

| Previous | Up | Next |
|----------|----|----- |
| [AUDIT_REPORT.md](AUDIT_REPORT.md) | [.context/templates](../..) | - |

---

## Summary

| Metric | Value |
|--------|-------|
| **Work Item** | {{WORK_ITEM_ID}} |
| **Status** | {{CURRENT_STATUS}} |
| **Verification Score** | {{SCORE}}% |
| **Verdict** | {{PASSED_OR_FAILED}} |

---

## Acceptance Criteria Verification

| # | Criterion | Verified | Evidence |
|---|-----------|----------|----------|
{{AC_TABLE}}

**Verification Score Calculation:**
- Total criteria: {{TOTAL_CRITERIA}}
- Verified: {{VERIFIED_CRITERIA}}
- Score: {{SCORE}}% ({{VERIFIED_CRITERIA}} / {{TOTAL_CRITERIA}} × 100)

**Threshold:** 80% required for closure

---

## Blocking Issues

{{BLOCKING_ISSUES_OR_NONE}}

---

## Recommendations

{{RECOMMENDATIONS_OR_NONE}}

---

## Ready for Closure

**{{YES_NO}}** - {{RATIONALE}}

**Closure Criteria Assessment:**

| Criterion | Met? | Details |
|-----------|------|---------|
| 80%+ acceptance criteria verified | {{AC_MET}} | {{AC_DETAILS}} |
| Evidence section has ≥1 link | {{EVIDENCE_MET}} | {{EVIDENCE_DETAILS}} |
| All child items completed | {{CHILDREN_MET}} | {{CHILDREN_DETAILS}} |
| No blocking impediments | {{IMPEDIMENTS_MET}} | {{IMPEDIMENTS_DETAILS}} |

---

## Work Item Details

**ID:** {{WORK_ITEM_ID}}

**Title:** {{WORK_ITEM_TITLE}}

**Type:** {{WORK_ITEM_TYPE}}

**Current Status:** {{CURRENT_STATUS}}

**Parent:** {{PARENT_ID}} - {{PARENT_TITLE}}

**Children:** {{CHILD_COUNT}}
{{CHILD_LIST}}

---

## Evidence Summary

**Total Evidence Links:** {{EVIDENCE_COUNT}}

**Evidence Quality:**
{{EVIDENCE_QUALITY_ASSESSMENT}}

**Evidence Links:**
{{EVIDENCE_LINKS_LIST}}

---

## Detailed Verification

### Acceptance Criteria Analysis

{{AC_DETAILED_ANALYSIS}}

### Child Item Status

{{CHILD_STATUS_ANALYSIS}}

### Impediments Check

{{IMPEDIMENTS_ANALYSIS}}

### Evidence Validation

{{EVIDENCE_VALIDATION_ANALYSIS}}

---

## Verification Timeline

| Timestamp | Event |
|-----------|-------|
{{VERIFICATION_TIMELINE}}

---

## Next Actions

### If Approved for Closure

1. Update status to DONE in work item file
2. Update parent reference to mark complete
3. Add completion timestamp
4. Archive verification report

### If Rejected

1. Address blocking issues: {{BLOCKING_ISSUES_SUMMARY}}
2. Complete missing acceptance criteria: {{MISSING_AC_SUMMARY}}
3. Add required evidence links
4. Re-verify when ready

---

## Appendix

### WTI Rule Compliance

| Rule | Status | Notes |
|------|--------|-------|
| WTI-001: Real-Time State | {{WTI_001_STATUS}} | {{WTI_001_NOTES}} |
| WTI-002: No Closure Without Verification | {{WTI_002_STATUS}} | {{WTI_002_NOTES}} |
| WTI-003: Truthful State | {{WTI_003_STATUS}} | {{WTI_003_NOTES}} |
| WTI-005: Atomic State Updates | {{WTI_005_STATUS}} | {{WTI_005_NOTES}} |
| WTI-006: Evidence-Based Closure | {{WTI_006_STATUS}} | {{WTI_006_NOTES}} |

### Raw Verification Data

```json
{{RAW_VERIFICATION_JSON}}
```

---

## Template Usage Instructions

**For wt-verifier agent:**

Replace placeholders with actual verification data:

| Placeholder | Type | Example |
|-------------|------|---------|
| `{{WORK_ITEM_ID}}` | String | `EN-001` |
| `{{TIMESTAMP}}` | ISO8601 | `2026-02-02T14:30:00Z` |
| `{{VERIFICATION_SCOPE}}` | String | `Enabler EN-001 completion verification` |
| `{{CURRENT_STATUS}}` | String | `IN_PROGRESS` |
| `{{SCORE}}` | Float | `85.7` |
| `{{PASSED_OR_FAILED}}` | String | `PASSED` or `FAILED` |
| `{{AC_TABLE}}` | Markdown table | See example below |
| `{{BLOCKING_ISSUES_OR_NONE}}` | Markdown | `None` or issue list |
| `{{RECOMMENDATIONS_OR_NONE}}` | Markdown | `None` or recommendations |
| `{{YES_NO}}` | String | `YES` or `NO` |
| `{{RATIONALE}}` | String | Explanation of verdict |

**Example AC_TABLE:**
```markdown
| 1 | Agent template created | ✅ | [wt-verifier.md](../agents/wt-verifier.md) |
| 2 | Verification logic implemented | ✅ | [Commit abc123](https://github.com/.../commit/abc123) |
| 3 | Tests passing | ✅ | [Test results](./test-output.txt) |
| 4 | Documentation updated | ❌ | Missing - SKILL.md needs update |
| 5 | Reviewed by peer | ⏳ | In progress - PR #45 |
| 6 | Integration tested | ✅ | [CI Build](https://ci/build/123) |
```

**Legend:**
- ✅ Verified (with evidence link)
- ❌ Not verified (missing evidence)
- ⏳ Partially verified (in progress)

**Example BLOCKING_ISSUES_OR_NONE:**
```markdown
### Critical Blockers

1. **Missing Documentation** (AC #4)
   - Impact: Cannot close without updated SKILL.md
   - Remediation: Update skill documentation with wt-verifier usage
   - Estimated effort: 30 minutes

2. **Incomplete Peer Review** (AC #5)
   - Impact: Quality gate requirement
   - Remediation: Complete PR #45 review
   - Estimated effort: 1 hour
```

**Example RECOMMENDATIONS_OR_NONE:**
```markdown
### Optional Improvements

1. **Add Performance Tests**
   - Current: Only unit tests
   - Suggestion: Add performance benchmarks for large worktracker audits
   - Priority: Low

2. **Expand Evidence Types**
   - Current: Git commits only
   - Suggestion: Add screenshots for UI-related work
   - Priority: Medium
```

**Score Calculation Example:**
```
Total Criteria: 6
Verified (✅): 4
Partially (⏳): 1
Not Verified (❌): 1

Score = (4 + 0.5×1) / 6 × 100 = 75%
Verdict = FAILED (below 80% threshold)
```

**Closure Decision Logic:**
```
if score >= 80%
   and evidence_count >= 1
   and blocking_issues == 0
   and (child_count == 0 or all_children_complete):
    verdict = PASSED
    ready_for_closure = YES
else:
    verdict = FAILED
    ready_for_closure = NO
```

---

## Verification Workflow

```
┌─────────────────────────────────────────┐
│   wt-verifier Verification Workflow    │
└─────────────────────────────────────────┘
                    │
                    ▼
         ┌──────────────────┐
         │ Read work item   │
         └──────────────────┘
                    │
                    ▼
         ┌──────────────────┐
         │ Parse AC section │
         └──────────────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │ Verify each AC       │
         │ - Check evidence     │
         │ - Validate links     │
         └──────────────────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │ Check child items    │
         └──────────────────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │ Check impediments    │
         └──────────────────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │ Calculate score      │
         └──────────────────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │ Generate report      │
         │ (this template)      │
         └──────────────────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │ Return verdict:      │
         │ PASSED or FAILED     │
         └──────────────────────┘
```

---

*Template Version: 1.0*
*Last Updated: 2026-02-02*
*Design Source: synthesis-worktracker-agent-design.md (lines 669-717)*
