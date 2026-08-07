# STORY-029: Fix the Silent-Failure Guard to Verify a Meaningful Audit (Not Just Non-Empty Output)

> **Type:** story
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-06-22
> **Completed:** 2026-08-05
> **Parent:** FEAT-002
> **GitHub Issue:** [#301](https://github.com/geekatron/jerry/issues/301)

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | Role / goal / benefit |
| [Summary](#summary) | Scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |
| [Children (Tasks)](#children-tasks) | Task inventory |
| [Progress Summary](#progress-summary) | Status tracking |
| [Related Items](#related-items) | Hierarchy |
| [Delivery Evidence](#delivery-evidence) | PR and commit evidence |
| [History](#history) | Status changes |

---

## User Story

As a repository maintainer, I want the security audit's silent-failure guard to verify that `pip-audit` actually audited a non-zero number of packages, so that a misconfigured audit invocation fails loudly rather than producing a false-green result.

---

## Summary

The current silent-failure guard checks that `pip-audit` produced at least one line of output. This check is satisfied by the warning `Dependency not found on PyPI: jerry` — which `pip-audit` emits even when it audits zero packages. The guard must instead verify that `pip-audit` audited at least one package from its input. This can be achieved by checking that `pip-audit` output contains a package audit result line (not only a warning), or by counting the number of packages passed to `--stdin` from `uv export` and asserting it is greater than zero before invoking `pip-audit`.

---

## Acceptance Criteria

- [x] The silent-failure guard fails with a non-zero exit code and a descriptive error message when `pip-audit` audits zero packages
- [x] A run where `uv export --all-extras` produces zero packages causes the scan step to fail (not silently pass)
- [x] The guard check is documented with a comment explaining what it validates and why
- [x] Existing passing audit runs (where packages are audited and no CVEs are found) continue to exit 0

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

- **Root defect:** [BUG-008: Scheduled security scan is false-green](../BUG-008-scheduled-scan-false-green.md)
- **Depends on:** [STORY-026: Unify CI + scheduled security audit](../STORY-026-unify-ci-scheduled-scan/STORY-026-unify-ci-scheduled-scan.md) (guard lives in the composite action)

---

## Delivery Evidence

| Artifact | Link | Commit | Notes |
|----------|------|--------|-------|
| PR #302 — Scanner hardening | [geekatron/jerry#302](https://github.com/geekatron/jerry/pull/302) | 81c7c61c | Silent-failure guard fix implemented. **Merged 2026-06-23** alongside PR #303 (commit e372e418, CVE remediation); reached main via merge PR #304 (merge commit 687a3214, includes docs commit 38b9d23b). All confirmed ancestors of origin/main. |
| Verification report | [wt-verifier-STORY-029-20260805.md](../../verification/wt-verifier-STORY-029-20260805.md) | — | Verdict 4/4 READY (100%). D5 guard in `action.yml` (verdict sentinel + 20-package floor, fully commented); local claims G-1/G-2 PASS (`verification-evidence-20260805.md`); happy-path green proven by run [29231285315](https://github.com/geekatron/jerry/actions/runs/29231285315) (2026-07-13, "No known vulnerabilities found", 103 packages, conclusion: success). |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-06-22 | pending | Story created |
| 2026-06-23 | in_progress | PR #302 (commit 81c7c61c) delivers guard fix; merged same day (evidence trail corrected 2026-08-05) |
| 2026-08-05 | completed | All 4 ACs verified by wt-verifier (4/4 READY, 100%) via code review + local repro claims + live green/red run logs; closed. See Delivery Evidence. |
