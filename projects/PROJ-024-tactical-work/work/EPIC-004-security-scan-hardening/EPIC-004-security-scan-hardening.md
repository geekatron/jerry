# EPIC-004: Dependency Security-Scan Pipeline Hardening

> **Type:** epic
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Created:** 2026-06-22
> **Parent:** PROJ-024
> **GitHub Issue:** [#301](https://github.com/geekatron/jerry/issues/301)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Epic scope and motivation |
| [Children Features/Capabilities](#children-featurescapabilities) | Work item decomposition table |
| [Progress Summary](#progress-summary) | Current status of all work items |
| [History](#history) | Status changes |

---

## Summary

The CI security audit (`ci.yml`) correctly detects transitive CVEs, but the scheduled scan (`security-scan.yml`) is false-green because it audits only the local project and misses all transitive CVEs. Additionally, the two scans have drifted and duplicated logic, the silent-failure guard is ineffective, and there are 9 open transitive CVEs. This epic hardens the pipeline into one shared, correct, owner-governed scanner.

---

## Children Features/Capabilities

| ID | Type | Title | Status |
|----|------|-------|--------|
| FEAT-002 | Feature | Security-scan pipeline hardening | in_progress |

### Feature Links

- [FEAT-002: Security-scan pipeline hardening](./FEAT-002-security-scan-pipeline-hardening/FEAT-002-security-scan-pipeline-hardening.md)

---

## Progress Summary

| ID | Type | Status |
|----|------|--------|
| FEAT-002 | Feature | in_progress |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-06-22 | pending | Epic created for security-scan pipeline hardening |
| 2026-06-23 | in_progress | FEAT-002 children in review via PR #302 (81c7c61c) and PR #303 (e372e418); pending merge |
