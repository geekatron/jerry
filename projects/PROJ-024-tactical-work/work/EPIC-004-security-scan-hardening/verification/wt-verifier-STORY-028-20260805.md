# Verification Report: STORY-028

> **Type:** verification-report
> **Generated:** 2026-08-05T20:15:00Z
> **Agent:** wt-verifier
> **Scope:** full — closure-readiness verification of STORY-028 (owner alerting via auto-managed rolling GitHub issue)

---

## Navigation

| Previous | Up | Next |
|----------|----|----- |
| - | [EPIC-004-security-scan-hardening](../EPIC-004-security-scan-hardening.md) | - |

---

## Summary

| Metric | Value |
|--------|-------|
| **Work Item** | STORY-028 — Owner Alerting via an Auto-Managed Rolling GitHub Issue |
| **Status** | in_progress |
| **Verification Score** | 60% (3.0 / 5.0) |
| **Verdict** | FAILED |

---

## Acceptance Criteria Verification

| # | Criterion | Verified | Evidence |
|---|-----------|----------|----------|
| 1 | Detects CVEs and creates/updates a GitHub issue with a canonical title listing CVE details | ✅ | Live run [31039187847](https://github.com/geekatron/jerry/actions/runs/31039187847) (workflow_dispatch, 2026-08-05T19:23:32Z) — "Run security audit" step `conclusion=failure` (real CVE: click 8.3.1 / PYSEC-2026-2132), "Create or update CVE alert issue" step `conclusion=success`, and GitHub Issue [#335](https://github.com/geekatron/jerry/issues/335) "Security Alert: CVEs found in dependency tree" auto-created at `2026-08-05T19:24:39Z` with the `security-alert` label. Title differs from the AC's literal example (`Security Scan: Open CVEs`) but the AC text explicitly permits "or equivalent canonical title" — accepted as equivalent. |
| 2 | On a subsequent clean scan, the rolling issue is closed automatically | ⏳ Partial | Code path exists and is logically correct: `.github/workflows/security-scan.yml` lines 139–164, step "Close CVE alert issue when clean", gated `if: always() && steps.audit.outputs.vuln-found == 'false'`. **No runtime evidence exists that this branch has ever executed successfully.** `gh run list --workflow=security-scan.yml --limit 20` shows 20/20 most recent runs (2026-07-18 → 2026-08-05, both scheduled and manual) with `conclusion: failure` — every run to date found CVEs, so the clean-scan / auto-close branch has never fired in production. Verified as code-correct only, not evidence-proven per WTI-006. |
| 3 | Rolling issue reused across runs, not duplicated (label/title search) | ⏳ Partial | Search-before-create/comment logic present in workflow lines 96–126 (`gh issue list --label security-alert --state open --jq 'select(.title == ...) .number'`). `gh issue list --repo geekatron/jerry --label security-alert --state all` and a title-text search both return exactly one issue (#335) — consistent with no duplication, but this is the *first* successful creation event (all 19 prior attempts 2026-07-18→2026-08-05T06:57 failed before any issue could be created — see Blocking Issues #2). The "found existing issue → append comment" reuse branch (lines 112–117) has **never executed live**, since no second CVE-positive run has occurred against an already-open issue. Verified as code-correct only for the create path; the reuse/comment path is unproven at runtime. |
| 4 | Issue body includes at minimum package name, affected version, CVE ID, and available fix version per finding | ❌ | `gh issue view 335 --json body` returns: `"**Scan run:** https://github.com/geekatron/jerry/actions/runs/31039187847\n**Date:** \n\npip-audit detected unfixed CVEs in the dependency tree. Check the [workflow run](...) for the full list.\n\n**Remediation:** bump the affected packages..."`. The body contains **no package name, affected version, CVE ID, or fix version** — it only links out to the workflow run and gives generic remediation boilerplate. This directly contradicts the AC requirement. Secondary defect noted: the `**Date:**` field renders empty because `github.run_started_at` (workflow line 91) is not a valid GitHub Actions `github` context property. |
| 5 | Issue creation/update step uses only `issues:write` permission (no broader permissions) | ✅ | Workflow top-level `permissions:` block (lines 42–44): `contents: read` (required for checkout) and `issues: write` only. No `pull-requests`, `contents: write`, or other broader scopes present. File verified against `origin/main` (`git diff origin/main -- .github/workflows/security-scan.yml` = empty diff — the read content is the live production file). |

**Verification Score Calculation:**
- Total criteria: 5
- Verified (✅ = 1.0): 2 (AC-1, AC-5)
- Partial (⏳ = 0.5): 2 (AC-2, AC-3)
- Not verified (❌ = 0.0): 1 (AC-4)
- Score: (1.0 + 0.5 + 0.5 + 0.0 + 1.0) / 5 × 100 = **60%**

**Threshold:** 80% required for closure — **NOT MET**

---

## Blocking Issues

### Critical Blockers

1. **AC-4 hard failure — issue body omits required CVE detail fields** (AC #4)
   - Impact: The delivered rolling issue does not meet the story's own definition of "alert" content; a maintainer reading issue #335 cannot see which packages/CVEs are affected without leaving GitHub and opening the workflow run logs — defeating the story's stated purpose ("so that I am alerted without needing to check workflow run logs manually").
   - Remediation: Extend `security-audit` composite action (or the workflow step) to emit a structured findings summary (package, installed version, CVE ID, fix version) as a step output or artifact, and interpolate it into `BODY_FRAGMENT` in the "Create or update CVE alert issue" step.
   - Secondary defect to fix in the same change: `SCAN_DATE: ${{ github.run_started_at }}` is not a valid Actions context expression and always renders empty; replace with a valid timestamp source (e.g., a `date -u +%FT%TZ` shell capture, or `github.event.head_commit.timestamp` / `steps.audit.outputs.*` if available).
   - Estimated effort: Medium (requires action output plumbing + workflow edit + one more live-fire verification run).

2. **AC-2 lacks runtime evidence — auto-close never observed in production** (AC #2)
   - Impact: The close-on-clean behavior is unverified. If it silently fails in production (e.g., a scoping bug analogous to the missing-label incident), the rolling issue would never close and would misrepresent current risk to the repo owner.
   - Remediation: Produce (or wait for) one production run where the dependency tree audits clean while issue #335 is open, and confirm the "Close CVE alert issue when clean" step executes with `conclusion: success` and the issue transitions to `state: CLOSED` with the expected closing comment.
   - Estimated effort: Low once a clean scan occurs naturally, or moderate if a controlled test scenario must be engineered (e.g., temporarily allow-listing the current CVE to force a clean run).

3. **AC-3 reuse-via-comment path lacks runtime evidence** (AC #3)
   - Impact: Only the "create new issue" branch has been exercised. The "existing issue found → append comment" branch (lines 112–117) — the actual "rolling" behavior the story is named for — has never run in production.
   - Remediation: Trigger a second CVE-positive scan while issue #335 remains open and confirm a comment is appended to #335 rather than a duplicate issue being created.
   - Estimated effort: Low — will self-resolve on the next scheduled run (daily cron) since issue #335 is currently open and unfixed CVEs remain, assuming AC-2/AC-4 fixes don't reset the issue's identity (title/label) in a way that breaks the search match.

### Evidence/Governance Hygiene (blocking under WTI-003, not a functional gap)

4. **Entity Delivery Evidence table is stale**
   - `STORY-028-owner-alerting-github-issue.md` Delivery Evidence row for PR #302 says *"pending merge — close on merge + AC verification"*, but `gh pr view 302` confirms `state: MERGED`, `mergedAt: 2026-06-23T16:37:26Z`, merge commit `f0152808ed0749b5927d114b1a9d7f97a4decd6b`. This is a truthful-state violation (WTI-003) that must be corrected regardless of AC outcome.

5. **Operational history not yet recorded in entity file (explicit instruction for this verification pass)**
   - The entity's Delivery Evidence and History sections currently contain **no record** of: (a) the one-time setup miss where the `security-alert` label was never created, causing all 19 scheduled/dispatched runs from 2026-07-18 (earliest observed) through 2026-08-05T06:57 to fail the "Create or update CVE alert issue" step with `could not add label: 'security-alert' not found` (confirmed via `gh run view <id> --log` on runs 30429944845 [2026-07-29] and 30983157958 [2026-08-05T06:57]); and (b) the 2026-08-05 remediation — label created (`color: B60205`, confirmed via `gh label list`) and a manual `workflow_dispatch` run (31039187847) dispatched to validate end-to-end, which succeeded in creating issue #335. This history **must** be added to the entity's Delivery Evidence / History tables before closure, per the task instructions and WTI-001/WTI-003.

---

## Recommendations

### Required Before Re-Verification

1. Implement structured CVE detail rendering in the issue body (package/version/CVE ID/fix version) — closes AC-4.
2. Fix the invalid `github.run_started_at` expression.
3. Allow the workflow to run at least once through the clean-scan/auto-close branch and at least once through the existing-issue/comment-reuse branch, and capture the run IDs as evidence — closes AC-2 and AC-3 with runtime proof rather than code review alone.
4. Update STORY-028's Delivery Evidence table to reflect PR #302's actual merged state (commit `f0152808`) and append a History/Delivery Evidence entry documenting the label-setup gap (2026-07-18/2026-07-29 → 2026-08-05, `could not add label` failures) and its fix (label created, `color B60205`; validated via manual dispatch run 31039187847 / issue #335).

### Optional Improvements

1. Consider adding a CI guard (or a `gh label create` step embedded in a one-time setup workflow / bootstrap script) so a missing `security-alert` label fails fast with an actionable error rather than silently degrading the alert channel for 19 consecutive days.
2. Consider adding a lightweight assertion/test (e.g., a workflow smoke test using a fixture-forced clean/dirty toggle) so AC-2/AC-3 branches can be exercised deterministically in CI rather than relying on production cron timing.

---

## Ready for Closure

**NO** — Score (60%) is below the 80% WTI-002 threshold. AC-4 has direct evidence of non-compliance (issue body omits required CVE detail fields), and AC-2/AC-3 have no runtime proof despite plausible code correctness. The entity correctly remains in `in_progress` status; this verification recommends it stay there until the blocking issues above are remediated and re-verified.

**Closure Criteria Assessment:**

| Criterion | Met? | Details |
|-----------|------|---------|
| 80%+ acceptance criteria verified | ❌ NO | 60% (3.0/5.0 weighted; 2 full pass, 2 partial, 1 fail) |
| Evidence section has ≥1 link | ✅ YES | Delivery Evidence table contains PR #302 link (though its status note is stale — see Blocking Issue #4) |
| All child items completed | ✅ YES (N/A) | No child tasks decomposed (`Children (Tasks)` table is a placeholder row); nothing to roll up |
| No blocking impediments | ✅ YES | No Impediment entities filed against STORY-028 in the worktracker |

---

## Work Item Details

**ID:** STORY-028

**Title:** Add Owner Alerting via an Auto-Managed Rolling GitHub Issue

**Type:** story

**Current Status:** in_progress

**Parent:** FEAT-002 — Security-scan pipeline hardening

**Children:** 0
(No child tasks decomposed; `Children (Tasks)` table contains only a placeholder row.)

---

## Evidence Summary

**Total Evidence Links:** 1 (entity Delivery Evidence table) + verification-derived evidence below

**Evidence Quality:**
The single entity-declared evidence link (PR #302) is a correct pointer to the delivering PR, but its accompanying note is stale (says "pending merge" for a PR merged 2026-06-23). This verification pass independently gathered and cross-checked additional live evidence not yet reflected in the entity file: workflow source content (diffed clean against `origin/main`), 20 recent `security-scan.yml` run records, two individual run logs (07-29 and 08-05T06:57) showing the `could not add label` failure, the current `security-alert` label definition, and issue #335's full body/labels/timestamps via `gh issue view`.

**Evidence Links:**
- PR #302 (entity-declared): https://github.com/geekatron/jerry/pull/302 — MERGED 2026-06-23T16:37:26Z, merge commit `f0152808ed0749b5927d114b1a9d7f97a4decd6b` (entity note "pending merge" is stale)
- Commit `81c7c61c` "ci: harden dependency security-scan pipeline (#301)" — present in history, part of merged PR #302
- Workflow file: `.github/workflows/security-scan.yml` (verified identical to `origin/main`)
- Run 31039187847 (manual dispatch, 2026-08-05T19:23:32Z): https://github.com/geekatron/jerry/actions/runs/31039187847 — audit failed (real CVE), alert-issue step succeeded, close step correctly skipped
- Run 30983157958 (scheduled, 2026-08-05T06:57:21Z): alert-issue step failed with `could not add label: 'security-alert' not found`
- Run 30429944845 (scheduled, 2026-07-29T06:58:15Z): same `could not add label` failure, confirmed via `gh run view --log`
- GitHub Issue #335: https://github.com/geekatron/jerry/issues/335 — created 2026-08-05T19:24:39Z, label `security-alert` (`color: B60205`), state OPEN
- Label `security-alert` (`gh label list`): `color: B60205`, description "Automated CVE alert from scheduled security scan"

---

## Detailed Verification

### Acceptance Criteria Analysis

See the [Acceptance Criteria Verification](#acceptance-criteria-verification) table above for the per-AC evidence mapping. Key finding: the workflow's create-path (AC-1) and permission scoping (AC-5) are solidly evidence-backed by a real, recent, end-to-end production run. The close-path (AC-2), the comment-reuse path (AC-3), and the issue body content requirement (AC-4) are either unproven at runtime or directly contradicted by the observed issue content.

### Child Item Status

No children exist for STORY-028. The `Children (Tasks)` table contains a single placeholder row ("(tasks to be decomposed during implementation)") with no linked entities. This does not block closure on its own (no incomplete children exist), but it does mean the story's delivery was not tracked via decomposed Task entities — a governance observation, not a blocker.

### Impediments Check

No Impediment entities were found referencing STORY-028 in the worktracker. Not a blocker.

### Evidence Validation

WTI-006 (Evidence-Based Closure) requires verifiable proof of completion. This verification distinguishes between **code-review evidence** (reading the workflow YAML and reasoning about correctness) and **runtime evidence** (observed `gh run`/`gh issue` state confirming the code executed as intended in production). AC-1 and AC-5 have runtime evidence. AC-2 and AC-3 have code-review evidence only — the relevant branches have not fired in the 20 most recent runs. AC-4 has runtime evidence that **contradicts** the requirement. Per the task's explicit instruction to judge each AC "against concrete evidence; no assumptions," AC-2 and AC-3 cannot be marked fully verified, and AC-4 must be marked failed.

---

## Verification Timeline

| Timestamp | Event |
|-----------|-------|
| 2026-08-05T20:00:00Z | Read entity file `STORY-028-owner-alerting-github-issue.md`; extracted 5 acceptance criteria |
| 2026-08-05T20:02:00Z | Read `.github/workflows/security-scan.yml`; diffed against `origin/main` (clean, confirms live production content) |
| 2026-08-05T20:04:00Z | `gh issue view 335` — confirmed issue title, label, timestamps, and body content (AC-4 evidence) |
| 2026-08-05T20:05:00Z | `gh pr view 302` — confirmed MERGED state, merge commit `f0152808` (contradicts entity's "pending merge" note) |
| 2026-08-05T20:06:00Z | `git log` cross-check of commit `81c7c61c` vs. merge commit `f0152808` — consistent, commit is part of the merged PR |
| 2026-08-05T20:08:00Z | `gh run view 31039187847` — confirmed step-level outcomes matching the supplied end-to-end proof narrative |
| 2026-08-05T20:10:00Z | `gh run list --workflow=security-scan.yml --limit 20` — confirmed 20/20 recent runs are `conclusion: failure` (no clean-scan run observed, AC-2 gap) |
| 2026-08-05T20:11:00Z | `gh label list --search security-alert` — confirmed label exists, `color: B60205` |
| 2026-08-05T20:12:00Z | `gh run view 30983157958 --json jobs` and `gh run view 30429944845 --log` — confirmed `could not add label` failures on 2026-08-05T06:57 and 2026-07-29 runs |
| 2026-08-05T20:13:00Z | `gh issue list --label security-alert --state all` and title-text search — confirmed exactly one issue (#335) exists, no duplicates |
| 2026-08-05T20:15:00Z | Verification report generated; verdict FAILED / NOT_READY |

---

## Next Actions

### If Approved for Closure

Not applicable — verdict is NOT_READY. Do not update entity status to done.

### If Rejected

1. Address blocking issues: AC-4 body content gap (missing package/version/CVE ID/fix version), AC-2 unproven auto-close, AC-3 unproven comment-reuse path, stale Delivery Evidence "pending merge" note, and missing record of the 2026-07-18→2026-08-05 label-setup incident and its fix.
2. Complete missing acceptance criteria: AC-2 and AC-3 need runtime (not just code) evidence; AC-4 needs an implementation fix.
3. Add required evidence links: link the specific run IDs (31039187847, and future clean-scan / comment-reuse runs) plus issue #335 directly in the entity's Delivery Evidence table.
4. Re-verify when ready (re-invoke wt-verifier once AC-2/AC-3/AC-4 have fresh runtime evidence).

---

## Appendix

### WTI Rule Compliance

| Rule | Status | Notes |
|------|--------|-------|
| WTI-001: Real-Time State | ⚠️ PARTIAL | Entity's status (`in_progress`) is currently accurate, but Delivery Evidence table is stale (PR #302 shown as "pending merge" though merged 2026-06-23) and omits the 2026-07-18→2026-08-05 label-setup incident/fix. |
| WTI-002: No Closure Without Verification | ✅ COMPLIANT | Entity is not marked done; no premature closure attempted. This report supports keeping it open. |
| WTI-003: Truthful State | ❌ FAIL | Stale "pending merge" note and missing operational-history record are both truthful-state gaps that must be corrected before closure. |
| WTI-005: Atomic State Updates | N/A | No status transition was performed by this verification pass (read-only per agent guardrails). |
| WTI-006: Evidence-Based Closure | ❌ FAIL | AC-4 evidence contradicts the requirement; AC-2/AC-3 lack runtime evidence. Overall score (60%) below the 80% threshold. |

### Raw Verification Data

```json
{
  "work_item_id": "STORY-028",
  "verification_scope": "full",
  "timestamp": "2026-08-05T20:15:00Z",
  "passed": false,
  "score": 0.60,
  "acceptance_criteria": {
    "total_criteria": 5,
    "verified_full": 2,
    "verified_partial": 2,
    "not_verified": 1,
    "percentage": 0.60,
    "passed": false,
    "detail": [
      {"id": "AC-1", "status": "verified", "evidence": ["run:31039187847", "issue:335"]},
      {"id": "AC-2", "status": "partial", "evidence_type": "code_review_only", "runtime_evidence": false},
      {"id": "AC-3", "status": "partial", "evidence_type": "code_review_plus_no_duplicates", "runtime_evidence_reuse_branch": false},
      {"id": "AC-4", "status": "not_verified", "evidence": ["issue:335 body lacks package/version/CVE/fix fields"]},
      {"id": "AC-5", "status": "verified", "evidence": ["workflow permissions block lines 42-44"]}
    ]
  },
  "evidence": {
    "total_links_declared_in_entity": 1,
    "total_links_gathered_by_verifier": 8,
    "passed": true
  },
  "child_rollup": {
    "applicable": false,
    "total_children": 0
  },
  "blocking_issues": [
    "AC-4: issue body omits package/version/CVE ID/fix version",
    "AC-2: auto-close branch never executed in production (20/20 recent runs conclusion=failure)",
    "AC-3: comment-reuse branch never executed in production",
    "Entity Delivery Evidence stale: PR #302 shown pending-merge though merged 2026-06-23T16:37:26Z",
    "Entity missing record of 2026-07-18..2026-08-05 label-setup gap and 2026-08-05 fix"
  ],
  "recommendations": [
    "Implement structured CVE detail rendering in issue body",
    "Fix invalid github.run_started_at expression",
    "Observe/produce a clean-scan run and a second CVE-positive run against an open issue to prove AC-2/AC-3",
    "Update entity Delivery Evidence and History tables with accurate PR status and label-setup incident record"
  ]
}
```

---

*Report generated by wt-verifier per `.context/templates/worktracker/VERIFICATION_REPORT.md`.*
*Entity file was NOT modified by this verification pass (read-only per P-020/guardrails).*
