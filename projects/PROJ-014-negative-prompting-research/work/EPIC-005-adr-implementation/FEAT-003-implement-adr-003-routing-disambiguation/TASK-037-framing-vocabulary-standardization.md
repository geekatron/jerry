# TASK-037: Component B — Framing Vocabulary Standardization

> **Type:** task
> **Status:** pending
> **Priority:** low
> **Created:** 2026-02-28
> **Parent:** FEAT-003
> **Owner:** —
> **Activity:** IMPLEMENTATION

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description |
| [Content](#content) | Description and acceptance criteria |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes |

---

## Summary

Conditional on TASK-025 (A/B testing) results: standardize the framing vocabulary of routing disambiguation sections across all 13 skills. If framing effect confirmed, apply NPT-010 "MUST NOT use when:" framing; if null effect, adopt community-preferred vocabulary.

---

## Content

### Description

ADR-003 Component B (conditional). This task is BLOCKED until TASK-025 (A/B testing) produces results. Based on those results:

- **If framing effect confirmed:** Apply NPT-010 "MUST NOT use when:" framing to all routing disambiguation sections.
- **If null framing effect:** Retain consequence documentation (Component A); adopt the vocabulary the framework community prefers for readability and consistency.
- **If inconclusive:** Retain consequence documentation; defer framing standardization to a follow-up experiment.

### Acceptance Criteria

- [ ] TASK-025 A/B testing results available
- [ ] Framing vocabulary decision made based on evidence
- [ ] All 13 routing disambiguation sections updated with standardized vocabulary
- [ ] Consistency verified across all skills

### Related Items

- Parent: [FEAT-003: Implement ADR-003](./FEAT-003-implement-adr-003-routing-disambiguation.md)
- Blocked By: TASK-025 (A/B testing results)
- References: ADR-003 Component B

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated SKILL.md files (13) | Skill modifications | `skills/*/SKILL.md` |

### Verification

- [ ] Acceptance criteria verified

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-28 | Created | Initial creation — blocked by TASK-025 |
