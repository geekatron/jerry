# BUG-008: Scheduled Security Scan Is False-Green — Audits Only the Local Project, Misses All Transitive CVEs

> **Type:** bug
> **Status:** in_progress
> **Priority:** critical
> **Impact:** critical
> **Severity:** critical
> **Created:** 2026-06-22
> **Parent:** FEAT-002
> **GitHub Issue:** [#301](https://github.com/geekatron/jerry/issues/301)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Bug description and evidence |
| [Steps to Reproduce](#steps-to-reproduce) | How to confirm the defect |
| [Environment](#environment) | Where the bug occurs |
| [Acceptance Criteria](#acceptance-criteria) | What a correct fix looks like |
| [Root Cause Analysis](#root-cause-analysis) | Known cause |
| [Related Items](#related-items) | Hierarchy |
| [Delivery Evidence](#delivery-evidence) | PR and commit evidence |
| [History](#history) | Status changes |

---

## Summary

The scheduled security scan (`security-scan.yml`) exits 0 with a false-green result. It runs `pip-audit` against the local project directory (`pip-audit .`) which resolves only the stub `jerry` package — not its transitive dependencies. The output line `Dependency not found on PyPI: jerry` is emitted and `pip-audit` exits 0. The silent-failure guard only checks that the output has at least one line, so the zero-package audit passes the guard. All transitive CVEs are invisible to the scheduled scan.

**Key Details:**
- **Symptom:** Scheduled scan reports no CVEs even when transitive dependencies have known CVEs that the CI scan detects
- **Frequency:** Every scheduled run
- **Workaround:** None — CI scan catches transitive CVEs in PRs, but daily schedule misses them entirely

---

## Steps to Reproduce

### Prerequisites

A Jerry environment with at least one transitive dependency affected by a known CVE (currently 9 are present).

### Reproduction

1. Trigger a run of `security-scan.yml` (or wait for the daily schedule)
2. Observe the log output: `Dependency not found on PyPI: jerry` appears in the `pip-audit` step
3. Observe that `pip-audit` exits 0 despite not having audited any packages from PyPI
4. Observe that the silent-failure guard passes (output is non-empty)
5. Observe the CI scan (`ci.yml`) run: it uses `uv export --all-extras | pip-audit --stdin` and detects the same transitive CVEs

### Expected Result

Scheduled scan detects the same CVEs as the CI scan, or fails with a clear error when the audit scope is zero.

### Actual Result

Scheduled scan exits 0, logs `Dependency not found on PyPI: jerry`, audits zero PyPI packages, and passes the silent-failure guard. False-green result.

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Workflow file** | `.github/workflows/security-scan.yml` |
| **pip-audit invocation** | `pip-audit .` (directory mode — audits only local project, not transitive deps) |
| **Silent-failure guard** | Checks `wc -l` of output — passes on any non-empty output |
| **CI scan (correct)** | `uv export --all-extras \| pip-audit --stdin` |

---

## Acceptance Criteria

- [ ] Scheduled scan detects at least the 9 known transitive CVEs that the CI scan detects (parity verified by running both workflows and comparing CVE lists)
- [ ] Running the scheduled scan against the current codebase produces a non-zero exit code (audit fails due to open CVEs, not a false-green pass)
- [ ] The log no longer contains `Dependency not found on PyPI: jerry` as the primary audit result
- [ ] Silent-failure guard rejects a scheduled scan run that audits zero PyPI packages

---

## Root Cause Analysis

### Root Cause

`security-scan.yml` invokes `pip-audit .` (directory/project mode). In directory mode, `pip-audit` reads the local package metadata and resolves dependencies declared in `pyproject.toml`. The Jerry package itself (`jerry`) is a local project and is not on PyPI; `pip-audit` logs `Dependency not found on PyPI: jerry` and exits 0 without auditing any transitive packages. The correct invocation is `uv export --all-extras | pip-audit --stdin` which exports the full resolved dependency tree including all transitive packages before piping to `pip-audit`.

### Contributing Factors

- CI scan (`ci.yml`) was implemented correctly using `uv export | pip-audit --stdin` but scheduled scan was implemented separately and uses the wrong invocation pattern
- Silent-failure guard checks only for non-empty output (`wc -l >= 1`), which is satisfied by the `Dependency not found on PyPI` warning line
- No parity test between CI and scheduled scan outputs

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-002: Security-scan pipeline hardening](FEAT-002-security-scan-pipeline-hardening.md)

### Cross-Links

- **Fixed by:** STORY-026 (unification into shared composite action) + STORY-029 (guard fix)

---

## Delivery Evidence

| Artifact | Link | Commit | Notes |
|----------|------|--------|-------|
| PR #302 — Scanner hardening | [geekatron/jerry#302](https://github.com/geekatron/jerry/pull/302) | 81c7c61c | Fix delivered via STORY-026 (DRY composite action) + STORY-029 (guard fix); pending merge — close on merge + AC verification |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-06-22 | pending | Bug filed based on scan behaviour analysis |
| 2026-06-23 | in_progress | PR #302 (commit 81c7c61c) delivers fix via STORY-026 composite action + STORY-029 guard fix; pending merge |
