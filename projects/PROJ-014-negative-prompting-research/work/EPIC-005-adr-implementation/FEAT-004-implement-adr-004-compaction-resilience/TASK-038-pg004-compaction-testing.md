# TASK-038: Decision 1 — PG-004 Compaction Testing Requirement

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-02-28
> **Parent:** FEAT-004
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

Establish PG-004 compaction testing requirement: all constraint-bearing artifacts must be tested for context compaction survival before deployment. Document the requirement in quality-enforcement.md or testing-standards.md.

---

## Content

### Description

ADR-004 Decision 1 (unconditional). Establish the PG-004 mandatory testing requirement for constraint-bearing artifacts. The requirement applies to: rule files with L2-REINJECT markers, rule files without L2-REINJECT markers, SKILL.md files with behavioral constraints, agent definition files with guardrails, and templates with creation constraints. This is unconditional — it does not depend on framing results. The specific test methodology, pass/fail thresholds, and automation approach are implementation details left to the implementer.

### Acceptance Criteria

- [ ] PG-004 compaction testing requirement documented in quality-enforcement.md or testing-standards.md
- [ ] Scope defined: which artifact types require compaction testing
- [ ] Test structure documented (load, simulate compaction, verify presence)
- [ ] Requirement integrated into C3+ quality gate checklist

### Related Items

- Parent: [FEAT-004: Implement ADR-004](./FEAT-004-implement-adr-004-compaction-resilience.md)
- References: ADR-004 Decision 1

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated quality-enforcement.md or testing-standards.md | Rule file modification | `.context/rules/` |

### Verification

- [ ] Acceptance criteria verified

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-28 | Created | Initial creation |
