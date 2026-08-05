# FEAT-002: Security-Scan Pipeline Hardening

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
PURPOSE: Significant deliverable containing Stories, Enablers, and Bugs for security-scan pipeline hardening
-->

> **Type:** feature
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Created:** 2026-06-22
> **Due:**
> **Completed:**
> **Parent:** EPIC-004
> **Owner:** adam.nowak
> **Target Sprint:**
> **GitHub Issue:** [#301](https://github.com/geekatron/jerry/issues/301)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Feature overview and value proposition |
| [Benefit Hypothesis](#benefit-hypothesis) | Expected benefits |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [MVP Definition](#mvp-definition) | Minimum viable scope |
| [Children Stories/Enablers](#children-storiesenablers) | Work decomposition |
| [Progress Summary](#progress-summary) | Overall progress |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## Summary

Harden the dependency security-scan pipeline by inserting a Feature container that groups the Enabler, Stories, and Bug that together fix the false-green scheduled scan, unify CI and scheduled audit into a shared composite action, add owner governance (CVE accept-list, rolling GitHub issue alerting), harden the silent-failure guard, and remediate the 9 current transitive CVEs.

**Value Proposition:**
- Scheduled scan correctly detects transitive CVEs (currently false-green every run)
- Single composite action eliminates CI/scheduled-scan drift
- Owner-governed accept-list prevents stale CVE suppression
- Rolling GitHub issue provides human-visible alerting without manual log inspection
- 9 known transitive CVEs remediated, reducing actual risk

---

## Benefit Hypothesis

**We believe that** unifying the CI and scheduled security scans into a hardened, owner-governed composite action

**Will result in** correct transitive CVE detection on every scheduled run, elimination of drift between the two scans, and timely owner alerting

**We will know we have succeeded when** the scheduled scan detects the same CVEs as the CI scan, the accept-list governs temporary suppressions with mandatory expiry, and all 9 current transitive CVEs are resolved or formally accepted

---

## Acceptance Criteria

### Definition of Done

- [x] BUG-008 resolved: scheduled scan detects transitive CVEs (parity with CI scan)
- [x] STORY-026: shared composite action is the authoritative audit implementation for both workflows
- [x] STORY-027: CVE accept-list with mandatory expiry exists and is enforced
- [ ] STORY-028: rolling GitHub issue is auto-created/updated when CVEs are found (in_progress — AC-4 failed, AC-2/AC-3 unproven at runtime; verified 60%)
- [x] STORY-029: silent-failure guard verifies non-zero package count, not just non-empty output
- [x] STORY-030: all 9 transitive CVEs resolved or accepted with documented rationale and expiry
- [ ] TASK-035: Dependabot security updates and vulnerability alerts confirmed enabled (externally confirmed NOT enabled as of 2026-08-05 — action outstanding)

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Scheduled scan detects the same CVEs as CI scan (parity) | [x] STORY-026/BUG-008 (2026-08-05) |
| AC-2 | Single composite action is shared by both workflows | [x] STORY-026 (2026-08-05) |
| AC-3 | CVE accept-list with expiry enforcement exists | [x] STORY-027 (2026-08-05) |
| AC-4 | Rolling GitHub issue alerting implemented | [ ] STORY-028 (60% verified — open) |
| AC-5 | Silent-failure guard validates non-zero audit scope | [x] STORY-029 (2026-08-05) |
| AC-6 | All 9 transitive CVEs remediated or formally accepted | [x] STORY-030 (2026-08-05; post-remediation click CVE tracked as BUG-009) |
| AC-7 | Dependabot settings confirmed enabled | [ ] TASK-035 (confirmed NOT enabled 2026-08-05) |

---

## MVP Definition

### In Scope (MVP)

- Fix false-green root defect (BUG-008)
- Shared composite action (STORY-026)
- CVE accept-list governance (STORY-027)
- Owner alerting via rolling issue (STORY-028)
- Silent-failure guard hardening (STORY-029)
- Transitive CVE remediation (STORY-030)
- Dependabot settings verification (TASK-035)

### Out of Scope (Future)

- SBOM generation integration (separate feature)
- Multi-project CVE tracking (separate feature)

---

## Children Stories/Enablers

### Story/Enabler Inventory

| ID | Type | Title | Status | Priority | Effort |
|----|------|-------|--------|----------|--------|
| EN-007 | Enabler | Dependency security-scan pipeline hardening | in_progress | high | — |
| BUG-008 | Bug | Scheduled security scan is false-green — audits only the local project, misses all transitive CVEs | completed (2026-08-05) | critical | — |
| BUG-009 | Bug | click 8.3.1 transitive command injection in click.edit() — PYSEC-2026-2132 (GH #336) | pending | high | — |
| STORY-026 | Story | Unify CI + scheduled security audit into one shared composite action (DRY) | completed (2026-08-05) | high | — |
| STORY-027 | Story | Add owner-governed CVE accept-list with mandatory expiry/re-review | completed (2026-08-05) | high | — |
| STORY-028 | Story | Add owner alerting via an auto-managed rolling GitHub issue | in_progress | medium | — |
| STORY-029 | Story | Fix the silent-failure guard to verify a meaningful audit (not just non-empty output) | completed (2026-08-05) | high | — |
| STORY-030 | Story | Remediate the 9 current transitive CVEs | completed (2026-08-05) | critical | — |
| TASK-035 | Task | Confirm Dependabot security updates + vulnerability alerts are enabled in repo Settings | pending | medium | — |

### Work Item Links

- [EN-007: Dependency Security-Scan Pipeline Hardening](./EN-007-security-scan-pipeline-hardening/EN-007-security-scan-pipeline-hardening.md)
- [BUG-008: Scheduled security scan is false-green](./BUG-008-scheduled-scan-false-green.md)
- [BUG-009: click 8.3.1 transitive command injection (PYSEC-2026-2132)](./BUG-009-click-command-injection/BUG-009-click-command-injection.md)
- [STORY-026: Unify CI + scheduled security audit](./STORY-026-unify-ci-scheduled-scan/STORY-026-unify-ci-scheduled-scan.md)
- [STORY-027: Add owner-governed CVE accept-list](./STORY-027-cve-accept-list/STORY-027-cve-accept-list.md)
- [STORY-028: Add owner alerting via rolling GitHub issue](./STORY-028-owner-alerting-github-issue/STORY-028-owner-alerting-github-issue.md)
- [STORY-029: Fix the silent-failure guard](./STORY-029-fix-silent-failure-guard/STORY-029-fix-silent-failure-guard.md)
- [STORY-030: Remediate the 9 current transitive CVEs](./STORY-030-remediate-transitive-cves/STORY-030-remediate-transitive-cves.md)

---

## Progress Summary

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Stories:   [################....] 80% (4/5 completed)              |
| Enablers:  [....................] 0% (0/1 completed)               |
| Bugs:      [##########..........] 50% (1/2 completed)              |
| Tasks:     [....................] 0% (0/1 completed)               |
+------------------------------------------------------------------+
| Overall:   [###########.........] 56% (5/9 items)                  |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Stories** | 5 |
| **Completed Stories** | 4 (STORY-026, STORY-027, STORY-029, STORY-030 — closed 2026-08-05) |
| **Open Stories** | 1 (STORY-028, in_progress — verified 60%, AC-4 failed) |
| **Total Enablers** | 1 |
| **Completed Enablers** | 0 |
| **Open Enablers** | 1 (EN-007, in_progress — open solely pending TASK-035) |
| **Total Bugs** | 2 |
| **Completed Bugs** | 1 (BUG-008 — closed 2026-08-05) |
| **Open Bugs** | 1 (BUG-009, pending — click 8.3.1 / GH #336) |
| **Total Tasks** | 1 |
| **Completed Tasks** | 0 |
| **Open Tasks** | 1 (TASK-035, pending — Dependabot confirmed NOT enabled) |
| **Completion %** | 56% (5/9 items) |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-004: Dependency Security-Scan Pipeline Hardening](../EPIC-004-security-scan-hardening.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Blocks | CI scan reliability | Hardened pipeline needed for correct daily CVE coverage |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-06-22 | claude | pending | Feature created to provide required hierarchy container between EPIC-004 and delivery items (EN-007, Stories, Bug); resolves E-001 hierarchy violation |
| 2026-06-23 | claude | in_progress | BUG-008, STORY-026..029 delivered via PR #302 (81c7c61c); STORY-030 via PR #303 (e372e418) — both merged 2026-06-23, reached main via merge PR #304 (687a3214); TASK-035 pending manual repo-settings action |
| 2026-08-05 | claude | in_progress | wt-verifier pass closed BUG-008, STORY-026, STORY-027, STORY-029, STORY-030. Remaining open: STORY-028 (60% — AC-4 failed, AC-2/3 unproven), EN-007/TASK-035 (Dependabot confirmed NOT enabled), and new BUG-009 (click 8.3.1 / GH #336, track-and-defer). |
