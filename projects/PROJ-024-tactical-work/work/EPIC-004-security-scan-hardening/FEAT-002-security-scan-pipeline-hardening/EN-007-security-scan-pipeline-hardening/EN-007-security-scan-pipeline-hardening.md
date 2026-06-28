# EN-007: Dependency Security-Scan Pipeline Hardening

> **Type:** enabler
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-06-22
> **Parent:** FEAT-002
> **GitHub Issue:** [#301](https://github.com/geekatron/jerry/issues/301)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Enabler scope and motivation |
| [Problem Statement](#problem-statement) | Why this enabler is needed |
| [Business Value](#business-value) | How this hardening supports reliability |
| [Technical Approach](#technical-approach) | Implementation strategy |
| [Children](#children) | Tasks under this enabler |
| [Progress Summary](#progress-summary) | Overall enabler progress |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Risks and Mitigations](#risks-and-mitigations) | Known risks |
| [History](#history) | Status changes |

---

## Summary

The CI security audit (`ci.yml`) correctly detects transitive CVEs using `uv export --all-extras | pip-audit`, but the scheduled scan (`security-scan.yml`) is false-green: it runs `pip-audit` against only the local project directory and misses all transitive CVEs. The two scans have also drifted — duplicated logic with diverging behaviour. The silent-failure guard checks only for non-empty output, which `pip-audit` produces even when it skips all transitive packages. There are also 9 open transitive CVEs currently undetected by the scheduled scan.

**Technical Scope:**
- Unify CI + scheduled scans into a shared composite action (single source of truth)
- Fix the false-green root defect in the scheduled scan
- Add an owner-governed CVE accept-list with mandatory expiry and re-review
- Add owner alerting via a rolling GitHub issue
- Fix the silent-failure guard to verify a meaningful audit result
- Remediate 9 current transitive CVEs

---

## Problem Statement

The scheduled scan (`security-scan.yml`) logs `Dependency not found on PyPI: jerry` and exits 0 — a false-green. This defeats the purpose of the scheduled scan as a compensating control. The CI scan does catch transitive CVEs, but the two scans have diverged and the duplication makes future maintenance error-prone. The silent-failure guard (`wc -l` check on output) passes even when `pip-audit` only audits the project stub and skips all transitive packages.

---

## Business Value

A correct, unified scanner ensures:
- CVEs in transitive dependencies are visible on every scheduled run, not only in CI
- A single composite action is the authoritative audit implementation — no drift
- Owner-governed accept-list prevents stale CVE suppressions
- Rolling GitHub issues alert the owner when new CVEs are found
- The 9 current transitive CVEs are remediated, reducing actual risk

---

## Technical Approach

Implement in layers: fix the root defect first (BUG-008), then unify the scans (STORY-026), then add governance (STORY-027, STORY-028), then harden the guard (STORY-029), then remediate current CVEs (STORY-030), then verify Dependabot settings (TASK-035).

---

## Children

| ID | Type | Title | Status |
|----|------|-------|--------|
| TASK-035 | Task | Confirm Dependabot security updates + vulnerability alerts are enabled in repo Settings | pending |

### Task Links

- [TASK-035: Confirm Dependabot settings](./TASK-035-confirm-dependabot-settings.md)

---

## Progress Summary

| Metric | Value |
|--------|-------|
| Total items | 1 |
| Completed | 0 |
| In Progress | 0 |
| Pending | 1 |
| Completion % | 0% (children in review; pending merge of PR #302) |

---

## Acceptance Criteria

- [ ] Scheduled scan detects the same CVEs as the CI scan (parity verified by running both and comparing output)
- [ ] Single composite action is the shared audit implementation for both CI and scheduled scan
- [ ] Owner-governed CVE accept-list exists with at least one entry format validated (package, CVE, expiry, rationale)
- [ ] Rolling GitHub issue is auto-created or updated when new CVEs are found by the scheduled scan
- [ ] Silent-failure guard rejects a run that audits zero packages (not merely non-empty output)
- [ ] All 9 known transitive CVEs are resolved or explicitly accepted with documented rationale and expiry
- [ ] Dependabot security updates and vulnerability alerts are confirmed enabled in repo Settings

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Some CVE remediations are blocked by upstream release schedules | medium | medium | Accept-list with mandatory expiry covers interim period |
| Composite action increases workflow complexity | low | low | Single shared action reduces total YAML; net simplification |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-06-22 | pending | Enabler created for security-scan pipeline hardening |
| 2026-06-23 | in_progress | Stories/BUG in review via PR #302 (commit 81c7c61c) and PR #303 (commit e372e418); TASK-035 pending manual repo-settings action |
