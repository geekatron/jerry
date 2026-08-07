# STORY-026: Unify CI + Scheduled Security Audit into One Shared Composite Action (DRY)

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

As a repository maintainer, I want a single shared composite action that is the authoritative audit implementation for both CI and the scheduled scan, so that the two scans cannot drift apart and any fix to the audit logic is applied in one place.

---

## Summary

`ci.yml` and `security-scan.yml` both run `pip-audit` but with different invocations and in different configurations. This duplication means the scans can drift (and already have: CI uses `uv export --all-extras | pip-audit --stdin`; scheduled scan uses the incorrect `pip-audit .`). The fix is to extract the audit logic into a single local composite action (e.g., `.github/actions/security-audit/`) that both workflows call. The composite action uses the correct invocation pattern (`uv export --all-extras | pip-audit --stdin`), eliminating the root defect from BUG-008 and ensuring future changes apply once.

---

## Acceptance Criteria

- [x] A shared composite action exists (e.g., `.github/actions/security-audit/action.yml`) implementing `uv export --all-extras | pip-audit --stdin`
- [x] `ci.yml` invokes the composite action instead of its inline pip-audit step
- [x] `security-scan.yml` invokes the same composite action instead of its inline `pip-audit .` step
- [x] Both workflows produce identical CVE lists when run against the same dependency set (parity verified)
- [x] No inline `pip-audit` invocation remains in either `ci.yml` or `security-scan.yml` outside the shared action

> **AC-1 implementation note (2026-08-05):** the shipped action uses a file-based export (`uv export --no-hashes --frozen --all-extras --no-emit-project > file`) followed by `pip-audit --requirement file`, not a literal stdin pipe. This is functionally equivalent to the AC's `| pip-audit --stdin` wording and deliberately superior: the intermediate requirements file enables the D5 meaningful-audit guard's package-floor check and clean accept-list flag injection. Recorded per wt-verifier recommendation; no functional gap.

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

---

## Delivery Evidence

| Artifact | Link | Commit | Notes |
|----------|------|--------|-------|
| PR #302 — Scanner hardening | [geekatron/jerry#302](https://github.com/geekatron/jerry/pull/302) | 81c7c61c | DRY composite action implemented. **Merged 2026-06-23** alongside PR #303 (commit e372e418, CVE remediation); reached main via merge PR #304 (merge commit 687a3214, includes docs commit 38b9d23b). All confirmed ancestors of origin/main. |
| Verification report | [wt-verifier-STORY-026-20260805.md](../../verification/wt-verifier-STORY-026-20260805.md) | — | Verdict 5/5 READY (100%). `action.yml` (277 lines) invoked from both `ci.yml` and `security-scan.yml`; CVE parity proven empirically by a same-commit run pair — CI run [30934932209](https://github.com/geekatron/jerry/actions/runs/30934932209) vs scheduled run [30983157958](https://github.com/geekatron/jerry/actions/runs/30983157958), byte-identical findings at commit 83f39340. |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-06-22 | pending | Story created |
| 2026-06-23 | in_progress | PR #302 (commit 81c7c61c) delivers shared composite action; merged same day (evidence trail corrected 2026-08-05) |
| 2026-08-05 | completed | All 5 ACs verified by wt-verifier (5/5 READY, 100%) incl. live cross-workflow parity at a shared commit; closed. See Delivery Evidence. |
