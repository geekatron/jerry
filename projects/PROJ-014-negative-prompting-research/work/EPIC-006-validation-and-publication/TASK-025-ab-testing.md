# TASK-025: A/B Testing — Positive vs Negative vs Negative with Consequence

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-02-28
> **Parent:** EPIC-006
> **Owner:** —
> **Activity:** RESEARCH

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

Design and execute A/B tests comparing three prompting approaches: positive-only framing, negative (bare prohibition), and negative with consequence (NPT-009 structured negation). Measure LLM compliance rates to validate the PROJ-014 research findings empirically.

---

## Content

### Description

The PROJ-014 research produced a taxonomy of 14 negative prompting patterns and concluded that NPT-009 (structured negation with consequence) outperforms bare prohibition (NPT-014). This task validates that conclusion through controlled A/B testing across representative prompting scenarios.

### Acceptance Criteria

- [ ] Test design covering at least 3 representative constraint types (e.g., tool usage, output format, behavioral boundary)
- [ ] Each variant tested: (A) positive-only, (B) negative bare prohibition, (C) negative with consequence
- [ ] Compliance rate measured for each variant across multiple runs
- [ ] Results documented with statistical significance assessment
- [ ] Findings compared against PROJ-014 research predictions

### Related Items

- Parent: [EPIC-006: Validation & Publication](./EPIC-006-validation-and-publication.md)
- Depends On: TASK-019 (C4 tournament — research findings)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| A/B test results | Research artifact | TBD |

### Verification

- [ ] Acceptance criteria verified

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-28 | Created | Initial creation |
