# FEAT-014: Framework Synchronization

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
CREATED: 2026-02-17 (Claude)
PURPOSE: Synchronize framework docs, rules, skills, and tests with EPIC-002/003 deliverables
-->

> **Type:** feature
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-17
> **Due:** ---
> **Completed:** 2026-02-17
> **Parent:** EPIC-003
> **Owner:** ---
> **Target Sprint:** Sprint 4

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this feature delivers |
| [Benefit Hypothesis](#benefit-hypothesis) | Expected benefits |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Children (Enablers)](#children-enablers) | Enabler inventory |
| [Enabler Dependencies](#enabler-dependencies) | Execution ordering and parallelism |
| [Progress Summary](#progress-summary) | Overall feature progress |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [History](#history) | Change log |

---

## Summary

Synchronize the Jerry framework's documentation, agent registry, rules, skill files, and tests with the infrastructure delivered by EPIC-002 (quality design) and EPIC-003 (quality implementation). The rapid implementation left gaps: AGENTS.md is severely incomplete (8 of 24+ agents documented), mandatory-skill-usage rules don't cover the /adversary skill, architecture and bootstrap skill files are truncated, and no tests validate adversarial template integrity.

**Value Proposition:**
- Ensures all framework consumers can discover and use the full agent catalog
- Completes mandatory skill invocation rules for quality enforcement
- Brings all skill documentation to consistent quality standard
- Adds test coverage for adversarial strategy templates

---

## Benefit Hypothesis

**We believe that** synchronizing all framework documentation, rules, and tests with the EPIC-002/003 deliverables

**Will result in** a framework where every component is discoverable, consistently documented, and test-verified

**We will know we have succeeded when:**
- AGENTS.md documents all 24+ agents across all skills
- /adversary is integrated into mandatory-skill-usage rules
- All skill SKILL.md files follow the triple-lens structure
- Adversarial template tests pass in CI

---

## Acceptance Criteria

### Definition of Done

- [ ] AGENTS.md updated with all agents across all skills (ps, nse, orch, adversary, transcript, worktracker)
- [ ] mandatory-skill-usage.md includes /adversary trigger keywords and rule text
- [ ] quality-enforcement.md references /adversary as implementation skill
- [ ] architecture/SKILL.md complete with triple-lens structure and navigation table
- [ ] bootstrap/SKILL.md complete with navigation table
- [ ] skills/shared/ documented or clarified
- [ ] Adversarial template integrity tests created and passing
- [ ] All quality scores >= 0.92

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | AGENTS.md lists all agents with role, file path, and cognitive mode | [ ] |
| AC-2 | H-22 trigger map includes /adversary keywords | [ ] |
| AC-3 | quality-enforcement.md has Implementation section referencing /adversary | [ ] |
| AC-4 | architecture/SKILL.md >= 150 lines with proper sections | [ ] |
| AC-5 | bootstrap/SKILL.md >= 100 lines with navigation table | [ ] |
| AC-6 | Adversarial template test validates all 10 templates | [ ] |
| AC-7 | All existing tests continue to pass | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | All modified files maintain H-23 navigation tables | [ ] |
| NFC-2 | All files follow H-24 anchor link syntax | [ ] |
| NFC-3 | No worktracker ontology violations | [ ] |

---

## Children (Enablers)

### Enabler Inventory

| ID | Type | Title | Status | Priority | Effort |
|----|------|-------|--------|----------|--------|
| EN-925 | Enabler | Agent Registry Completion | pending | critical | 5 |
| EN-926 | Enabler | Rule Synchronization | pending | high | 3 |
| EN-927 | Enabler | Skill Documentation Completion | pending | high | 5 |
| EN-928 | Enabler | Test Coverage Expansion | pending | medium | 3 |
| EN-929 | Enabler | Minor Documentation Cleanup | pending | low | 2 |

### Work Item Links

- [EN-925: Agent Registry Completion](EN-925-agent-registry-completion/EN-925-agent-registry-completion.md)
- [EN-926: Rule Synchronization](EN-926-rule-synchronization/EN-926-rule-synchronization.md)
- [EN-927: Skill Documentation Completion](EN-927-skill-documentation/EN-927-skill-documentation.md)
- [EN-928: Test Coverage Expansion](EN-928-test-coverage/EN-928-test-coverage.md)
- [EN-929: Minor Documentation Cleanup](EN-929-documentation-cleanup/EN-929-documentation-cleanup.md)

---

## Enabler Dependencies

```
EN-925 (Agent Registry) [can start immediately]
EN-926 (Rule Sync) [can start immediately, parallel with EN-925]
EN-927 (Skill Docs) [can start immediately, parallel]
EN-928 (Tests) [depends on EN-925, EN-926 for accurate references]
EN-929 (Cleanup) [can start immediately, parallel]
```

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Enablers:  [....................] 0% (0/5 completed)              |
| Effort:    [....................] 0% (0/18 points)                |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                               |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Enablers** | 5 |
| **Completed Enablers** | 0 |
| **Total Effort (points)** | 18 |
| **Completed Effort** | 0 |
| **Completion %** | 0% |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-003: Quality Framework Implementation](../EPIC-003-quality-implementation.md)

### Related Features

- [FEAT-008: Quality Framework Implementation](../FEAT-008-quality-framework-implementation/FEAT-008-quality-framework-implementation.md) - Quality framework code
- [FEAT-009: Adversarial Strategy Templates](../FEAT-009-adversarial-strategy-templates/FEAT-009-adversarial-strategy-templates.md) - Adversarial templates
- [FEAT-010: Tournament Remediation](../FEAT-010-tournament-remediation/FEAT-010-tournament-remediation.md) - Tournament remediation

### Source

- PROJ-001 codebase gap analysis (2026-02-17)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-17 | Claude | pending | Feature created under EPIC-003. 5 enablers (EN-925--929), 18 effort points. Addresses 15 gaps identified by codebase audit: incomplete AGENTS.md, missing /adversary rule triggers, truncated skill docs, no adversarial template tests. |
