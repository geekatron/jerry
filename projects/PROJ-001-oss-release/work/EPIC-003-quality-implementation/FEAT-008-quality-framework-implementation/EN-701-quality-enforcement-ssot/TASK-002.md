# TASK-002: Organize Constants into Structured SSOT File

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** pending
> **Priority:** HIGH
> **Activity:** DEVELOPMENT
> **Agents:** ps-architect
> **Created:** 2026-02-14
> **Parent:** EN-701

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Parent and dependencies |
| [History](#history) | Change log |

---

## Summary

Take the constants inventory produced by TASK-001 and organize them into the structured `.context/rules/quality-enforcement.md` SSOT file. Group constants by category (criticality levels, quality thresholds, strategy catalog, cycle requirements, tier vocabulary, escalation rules, architecture layers). Follow markdown navigation standards (NAV-001 through NAV-006) and keep the file under 2000 tokens.

### Acceptance Criteria

- [ ] `.context/rules/quality-enforcement.md` file created
- [ ] Constants organized into logical categories
- [ ] Criticality levels (C1-C4) section with definitions and enforcement tier mapping
- [ ] Quality threshold (0.92) section with scoring dimensions
- [ ] Strategy encodings (S-001 through S-014) section with descriptions
- [ ] Cycle count (3 iterations minimum) section
- [ ] Tier vocabulary (HARD/MEDIUM/SOFT) section with definitions
- [ ] Auto-escalation rules (AE-001 through AE-006) section
- [ ] 5-layer architecture reference (L1-L5) section
- [ ] File follows NAV-001 through NAV-006 navigation standards
- [ ] File is under 2000 tokens

### Related Items

- Parent: [EN-701: Quality Enforcement SSOT](EN-701-quality-enforcement-ssot.md)
- Depends on: TASK-001 (constants inventory)
- Blocks: TASK-003 (validation)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| `.context/rules/quality-enforcement.md` | Rule file | — |

### Verification

- [ ] Acceptance criteria verified
- [ ] File structure reviewed for completeness
- [ ] Token count measured and within budget

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. Core deliverable task — produces the SSOT file that all downstream enablers reference. |
