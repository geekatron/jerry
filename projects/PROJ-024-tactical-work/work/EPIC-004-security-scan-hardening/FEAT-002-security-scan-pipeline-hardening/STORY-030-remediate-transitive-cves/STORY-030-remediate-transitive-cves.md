# STORY-030: Remediate the 9 Current Transitive CVEs

> **Type:** story
> **Status:** in_progress
> **Priority:** critical
> **Impact:** high
> **Created:** 2026-06-22
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

---

## Acceptance Criteria

- [ ] Red state confirmed: the fixed scanner (from STORY-026) reports at least 1 CVE for each of the 5 affected packages before any version bumps are applied
- [ ] Green state confirmed: after bumping each package to its patched version, the fixed scanner exits 0 with no unaccepted CVEs reported
- [ ] `uv.lock` is updated to reflect the patched transitive versions
- [ ] Any package that cannot reach its patched version due to dependency conflicts is documented and added to the CVE accept-list (from STORY-027) with rationale and expiry date
- [ ] No new CVEs are introduced by the version bumps (scanner exits clean after bumps)

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
| PR #303 — CVE remediation | [geekatron/jerry#303](https://github.com/geekatron/jerry/pull/303) | e372e418 | Transitive CVE remediation delivered; pending merge — close on merge + AC verification (red/green confirmed) |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-06-22 | pending | Story created |
| 2026-06-23 | in_progress | PR #303 (commit e372e418) delivers CVE remediation; pending merge |
