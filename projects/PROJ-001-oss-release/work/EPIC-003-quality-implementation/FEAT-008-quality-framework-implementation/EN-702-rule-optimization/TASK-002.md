# TASK-002: Content Audit — Categorize Rules by Tier, Identify Redundancy

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** pending
> **Priority:** HIGH
> **Activity:** RESEARCH
> **Agents:** ps-investigator
> **Created:** 2026-02-14
> **Parent:** EN-702

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

Audit all 10 rule files and CLAUDE.md to categorize every rule as HARD, MEDIUM, or SOFT tier. Identify redundant content across files (e.g., layer boundary rules appearing in both coding-standards and architecture-standards). Flag verbose explanations that can be compressed and low-value content that can be removed. Produce an audit report with per-rule tier classification and redundancy map.

### Acceptance Criteria

- [ ] Every rule in all 10 files categorized as HARD, MEDIUM, or SOFT
- [ ] Cross-file redundancy identified and documented
- [ ] Verbose explanations flagged for compression
- [ ] Low-value content flagged for removal
- [ ] Audit report produced with per-rule tier classification
- [ ] Redundancy map showing which rules appear in multiple files
- [ ] Estimated token savings per optimization action documented

### Related Items

- Parent: [EN-702: Rule File Token Optimization](EN-702-rule-optimization.md)
- Depends on: TASK-001 (baseline measurement)
- Blocks: TASK-003 (rule ID assignment)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Content audit report | Research artifact | -- |
| Redundancy map | Analysis artifact | -- |

### Verification

- [ ] Acceptance criteria verified
- [ ] All rules categorized with tier classification
- [ ] Redundancy map complete

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. Critical analysis task -- tier classification drives all subsequent optimization work. |
