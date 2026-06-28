# STORY-026: Unify CI + Scheduled Security Audit into One Shared Composite Action (DRY)

> **Type:** story
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Created:** 2026-06-22
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

- [ ] A shared composite action exists (e.g., `.github/actions/security-audit/action.yml`) implementing `uv export --all-extras | pip-audit --stdin`
- [ ] `ci.yml` invokes the composite action instead of its inline pip-audit step
- [ ] `security-scan.yml` invokes the same composite action instead of its inline `pip-audit .` step
- [ ] Both workflows produce identical CVE lists when run against the same dependency set (parity verified)
- [ ] No inline `pip-audit` invocation remains in either `ci.yml` or `security-scan.yml` outside the shared action

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
| PR #302 — Scanner hardening | [geekatron/jerry#302](https://github.com/geekatron/jerry/pull/302) | 81c7c61c | DRY composite action implemented; pending merge — close on merge + AC verification |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-06-22 | pending | Story created |
| 2026-06-23 | in_progress | PR #302 (commit 81c7c61c) delivers shared composite action; pending merge |
