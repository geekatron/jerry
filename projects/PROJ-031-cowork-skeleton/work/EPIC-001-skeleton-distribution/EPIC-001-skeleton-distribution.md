# EPIC-001: Jerry CoWork Skeleton Distribution

<!--
TEMPLATE: Epic
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.2
PURPOSE: Distribute Jerry as a Claude CoWork plugin via a derived, projects-stripped skeleton branch kept in sync by CI
-->

> **Type:** epic
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-06-26T12:00:00Z
> **Due:**
> **Completed:**
> **Parent:** PROJ-031
> **Owner:** adam.nowak

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this Epic covers |
| [Business Outcome Hypothesis](#business-outcome-hypothesis) | Expected outcome |
| [Children Features/Enablers](#children-featuresenablers) | Workstream inventory |
| [Progress Summary](#progress-summary) | Overall progress |
| [Containment Note](#containment-note) | Epic-level Enabler rationale |
| [Related Items](#related-items) | Links, dependencies, GitHub parity |
| [History](#history) | Status changes |

---

## Summary

Jerry cannot install as a plugin in Claude CoWork (Claude Desktop) because the repository exceeds CoWork's plugin-load limit of approximately 5,000 files. The `projects/` folder accounts for 4,600 of 6,344 tracked files (72%). This Epic delivers a derived `cowork-skeleton` distribution branch — the full Jerry repo with `projects/` stripped to a minimal stub — regenerated from `main` by CI on each release, plus the security hardening and user documentation required to make it safe and usable.

**Value Proposition:**
- Unblocks Jerry installation in Claude CoWork (tracked files drop from ~6,344 to ~1,744, well under 5,000)
- Keeps the distribution branch automatically in sync with `main` via regenerate-not-merge CI
- Preserves a working fresh install (minimal `projects/` stub satisfies H-04 bootstrap)

---

## Business Outcome Hypothesis

**We believe that** publishing a projects-stripped `cowork-skeleton` branch regenerated from `main` by CI

**Will result in** Jerry installing successfully as a Claude CoWork plugin without manual repository surgery by users

**We will know we have succeeded when** a fresh CoWork install loads the skeleton branch under the file limit, the plugin surface (`.claude-plugin/`, `skills/`, `.claude/`, `.context/`) is intact, and a user can bootstrap their own project from the stub

---

## Children Features/Enablers

| ID | Type | Title | Status | Priority |
|----|------|-------|--------|----------|
| FEAT-001 | Feature | Skeleton Generation | pending | high |
| EN-001 | Enabler | CI Sync Automation | pending | high |
| FEAT-002 | Feature | Security and Threat Model | pending | high |
| FEAT-003 | Feature | User Documentation (Diataxis) and MkDocs | pending | medium |
| EN-002 | Enabler | Adversarial Quality Gate | pending | high |

### Work Item Links

- [FEAT-001: Skeleton Generation](./FEAT-001-skeleton-generation/FEAT-001-skeleton-generation.md)
- [EN-001: CI Sync Automation](./EN-001-ci-sync-automation/EN-001-ci-sync-automation.md)
- [FEAT-002: Security and Threat Model](./FEAT-002-security-threat-model/FEAT-002-security-threat-model.md)
- [FEAT-003: User Documentation (Diataxis) and MkDocs](./FEAT-003-user-documentation/FEAT-003-user-documentation.md)
- [EN-002: Adversarial Quality Gate](./EN-002-adversarial-quality-gate/EN-002-adversarial-quality-gate.md)

---

## Progress Summary

```
+------------------------------------------------------------------+
|                   EPIC PROGRESS TRACKER                           |
+------------------------------------------------------------------+
| Features:  [....................] 0% (0/3 completed)              |
| Enablers:  [....................] 0% (0/2 completed)              |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                              |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Features** | 3 |
| **Total Enablers** | 2 |
| **Total Stories** | 9 |
| **Total Tasks** | 5 |
| **Completion %** | 0% |

---

## Containment Note

This Epic contains both Features and Enablers. EN-001 (CI Sync Automation) and EN-002 (Adversarial Quality Gate) are Epic-level Enablers per INV-EN03 (`Enabler.allowed_parents = [Feature, Epic]`), representing cross-cutting infrastructure and process work that does not belong to a single Feature. INV-E01 (no mixing of Capabilities and Features) is not violated — no Capabilities are present.

---

## Related Items

### Hierarchy

- **Parent Project:** [PROJ-031: Jerry CoWork Skeleton Distribution](../../PLAN.md)

### GitHub Issue Parity (H-32)

- **GitHub Issue:** [#305](https://github.com/geekatron/jerry/issues/305) — created per H-32 from [EPIC-001-github-issue-draft.md](../EPIC-001-github-issue-draft.md).

### Related

- CoWork plugin surface: `.claude-plugin/`, `skills/`, `.claude/`, `.context/`
- Distribution mechanism: derived `cowork-skeleton` branch, regenerated from `main`

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-06-26 | adam.nowak | pending | Epic created; five workstreams decomposed (3 Features, 2 Enablers) |
