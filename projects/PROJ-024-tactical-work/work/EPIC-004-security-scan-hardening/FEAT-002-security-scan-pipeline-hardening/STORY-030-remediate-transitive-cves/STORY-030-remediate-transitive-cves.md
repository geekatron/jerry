# STORY-030: Remediate the 9 Current Transitive CVEs

> **Type:** story
> **Status:** completed
> **Priority:** critical
> **Impact:** high
> **Created:** 2026-06-22
> **Completed:** 2026-08-05
> **Parent:** FEAT-002
> **GitHub Issue:** [#301](https://github.com/geekatron/jerry/issues/301)

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | Role / goal / benefit |
| [Summary](#summary) | Scope, CVE list, and test-first approach |
| [Acceptance Criteria](#acceptance-criteria) | Red/green test-first criteria |
| [Children (Tasks)](#children-tasks) | Task inventory |
| [Progress Summary](#progress-summary) | Status tracking |
| [Related Items](#related-items) | Hierarchy |
| [Delivery Evidence](#delivery-evidence) | PR and commit evidence |
| [History](#history) | Status changes |

---

## User Story

As a repository maintainer, I want the 9 known transitive CVEs to be resolved by bumping the affected packages to their patched versions, so that the security scan exits clean and no known vulnerabilities remain unaddressed.

---

## Summary

The fixed scanner from STORY-026 will go RED on the following 9 CVEs once the false-green root defect is fixed. Each requires bumping a transitive dependency to its patched version. The test-first acceptance criteria define the red state (scan detects CVEs) and the green state (scan exits 0 after bumps).

**CVEs to remediate (package → patched version):**

| Package | Patched Version |
|---------|----------------|
| mako | 1.3.12 |
| urllib3 | 2.7.0 |
| msgpack | 1.2.1 |
| pydantic-settings | 2.14.2 |
| pip | 26.1.2 |

Note: Some packages appear more than once across different CVEs; the table lists the minimum version that resolves all known CVEs for that package.

> **Count reconciliation (W-004, 2026-08-05):** the title's "9 CVEs" refers to the original 9-CVE / 7-package inventory; this story's 5 in-scope packages account for 8 distinct advisory IDs (commit e372e418: urllib3 ×2, pip ×3, pydantic-settings ×1, msgpack ×1, mako ×1), and the remainder (idna, pymdown-extensions) were resolved by separate routine dependency bumps outside this story.

---

## Acceptance Criteria

- [ ] Red state confirmed: the fixed scanner (from STORY-026) reports at least 1 CVE for each of the 5 affected packages before any version bumps are applied — **PARTIAL**: per-package advisory IDs in commit e372e418 / PR #303 prove a red state existed for all 5 packages, but it was captured via the local pre-push hook (`pip-audit --skip-editable`), not the STORY-026 composite scanner — the remediation branch was never rebased onto commit 81c7c61c, so no CI log of the fixed scanner in a red state exists
- [x] Green state confirmed: after bumping each package to its patched version, the fixed scanner exits 0 with no unaccepted CVEs reported (proven 3 independent ways — see Delivery Evidence)
- [x] `uv.lock` is updated to reflect the patched transitive versions
- [x] Any package that cannot reach its patched version due to dependency conflicts is documented and added to the CVE accept-list (from STORY-027) with rationale and expiry date (vacuously satisfied — no conflicts; allowlist is empty by design with rationale comment)
- [x] No new CVEs are introduced by the version bumps (scanner exits clean after bumps; the sole current finding, click 8.3.1, is an unrelated post-remediation CVE — see scope note)

> **Scope note (2026-08-05):** click 8.3.1 (PYSEC-2026-2132) is a post-remediation CVE published after this story's delivery. It is out of scope here and tracked as [BUG-009](../BUG-009-click-command-injection/BUG-009-click-command-injection.md) / [GH #336](https://github.com/geekatron/jerry/issues/336). Closed at 90% verification (4 verified + 1 partial), above the 80% WTI-002 threshold, with the AC-1 provenance gap honestly recorded above.

---

## Children (Tasks)

| ID | Title | Status |
|----|-------|--------|
| (tasks to be decomposed during implementation) | | |

---

## Progress Summary

| Metric | Value |
|--------|-------|
| Total Tasks | 0 |
| Completed | 0 |
| Completion % | 0% |

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-002: Security-scan pipeline hardening](../FEAT-002-security-scan-pipeline-hardening.md)

### Related Items

- **Depends on:** [STORY-026: Unify CI + scheduled security audit](../STORY-026-unify-ci-scheduled-scan/STORY-026-unify-ci-scheduled-scan.md) (scanner must be fixed before red state can be verified)
- **Uses:** [STORY-027: CVE accept-list](../STORY-027-cve-accept-list/STORY-027-cve-accept-list.md) (for any CVEs blocked by upstream constraints)

---

## Delivery Evidence

| Artifact | Link | Commit | Notes |
|----------|------|--------|-------|
| PR #303 — CVE remediation | [geekatron/jerry#303](https://github.com/geekatron/jerry/pull/303) | e372e418 | Transitive CVE remediation delivered. **Merged 2026-06-23** alongside PR #302 (commit 81c7c61c, CI hardening); reached main via merge PR #304 (merge commit 687a3214, includes docs commit 38b9d23b). All confirmed ancestors of origin/main. |
| Red-state record (AC-1) | [Commit e372e418](https://github.com/geekatron/jerry/commit/e372e418177b776460e927133695853f3e11b854) | e372e418 | Per-package pre-bump advisory IDs: urllib3 (PYSEC-2026-141/142), pip (PYSEC-2026-196, CVE-2026-3219, CVE-2026-6357), pydantic-settings (GHSA-4xgf-cpjx-pc3j), msgpack (GHSA-6v7p-g79w-8964), mako (CVE-2026-44307). Captured via local pre-push `pip-audit`, not the STORY-026 scanner (AC-1 PARTIAL). |
| Verification report | [wt-verifier-STORY-030-20260805.md](../../verification/wt-verifier-STORY-030-20260805.md) | — | Verdict 90% READY (4 verified + 1 partial). `uv.lock` pins mako 1.3.12 / urllib3 2.7.0 / msgpack 1.2.1 / pydantic-settings 2.14.2 / pip 26.1.2; green state proven 3 independent ways (merge-time local audit, live scheduled run [31039187847](https://github.com/geekatron/jerry/actions/runs/31039187847), verifier's own live pip-audit run); allowlist empty (AC-4 vacuous). |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-06-22 | pending | Story created |
| 2026-06-23 | in_progress | PR #303 (commit e372e418) delivers CVE remediation; merged same day (evidence trail corrected 2026-08-05) |
| 2026-08-05 | completed | Verified by wt-verifier at 90% (4/5 verified, AC-1 partial on red-state provenance); closed above the 80% threshold with gap recorded. click 8.3.1 tracked separately as BUG-009 / GH #336. |
