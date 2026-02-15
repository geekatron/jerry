# TASK-004: Write criticality-based strategy selection tests

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** DONE
> **Priority:** HIGH
> **Activity:** DEVELOPMENT
> **Agents:** ps-architect
> **Created:** 2026-02-14
> **Parent:** EN-812

---

## Document Sections
| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Time Tracking](#time-tracking) | Effort estimates and actuals |
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Parent and dependencies |
| [History](#history) | Change log |

---

## Summary

Write pytest E2E tests that validate the criticality-based strategy selection logic in `skills/adversary/agents/adv-selector.md`. These tests form the fourth category of the E2E test suite in `tests/e2e/test_adversary_templates_e2e.py`.

The tests must verify that adv-selector.md correctly maps each criticality level to its required strategy set as defined in quality-enforcement.md:

- **C1 (Routine)**: {S-010} -- Self-Refine only. Scope: reversible in 1 session, <3 files. Enforcement: HARD only.
- **C2 (Standard)**: {S-007, S-002, S-014} -- Constitutional AI Critique + Devil's Advocate + LLM-as-Judge. Scope: reversible in 1 day, 3-10 files. Enforcement: HARD + MEDIUM.
- **C3 (Significant)**: C2 + {S-004, S-012, S-013} -- Adds Pre-Mortem + FMEA + Inversion. Total: {S-002, S-004, S-007, S-012, S-013, S-014}. Scope: >1 day to reverse, >10 files, API changes. Enforcement: All tiers.
- **C4 (Critical)**: All 10 selected strategies -- {S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014}. Scope: irreversible, architecture/governance/public. Enforcement: All tiers + tournament.

Test implementation approach:
- Parse `skills/adversary/agents/adv-selector.md` to extract the criticality-to-strategy mapping
- Use regex to find strategy ID sets associated with each criticality level (C1, C2, C3, C4)
- Compare extracted sets against the expected sets from quality-enforcement.md
- Verify that C3 is a superset of C2 (cumulative)
- Verify that C4 is a superset of C3 (cumulative)
- Verify that C4 contains exactly all 10 selected strategies
- Also parse quality-enforcement.md Criticality Levels table as the authoritative source for comparison
- Use `pytest.mark.parametrize` for each criticality level
- Mark tests with `@pytest.mark.e2e`

Additional tests:
- Verify execution ordering: S-003 Steelman must precede S-002 Devil's Advocate (H-16) in any criticality level that includes both
- Verify strategy set completeness: the union of all criticality-level strategy sets must equal exactly the 10 selected strategies (no orphans, no gaps)

### Acceptance Criteria
- [ ] Tests verify C1 maps to {S-010}
- [ ] Tests verify C2 maps to {S-007, S-002, S-014}
- [ ] Tests verify C3 maps to C2 + {S-004, S-012, S-013}
- [ ] Tests verify C4 maps to all 10 strategies {S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014}
- [ ] Tests verify cumulative property: C3 is superset of C2, C4 is superset of C3
- [ ] Tests verify execution ordering: S-003 before S-002 (H-16) when both present
- [ ] Tests verify strategy set completeness: union equals exactly 10 selected
- [ ] Tests parse adv-selector.md for the mapping
- [ ] Tests parse quality-enforcement.md for the authoritative reference
- [ ] Tests use `pytest.mark.parametrize` for each criticality level
- [ ] Tests use `@pytest.mark.e2e` marker
- [ ] Test file includes type hints (H-11) and docstrings (H-12)
- [ ] Quality gate: Deliverable reviewed via creator-critic-revision cycle (min 3 iterations)
- [ ] Quality gate: Score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] Quality gate: S-003 Steelman applied before S-002 Devil's Advocate critique

### Related Items
- Parent: [EN-812: Integration Testing](EN-812-integration-testing.md)
- Depends on: EN-810 TASK-001 (adv-selector.md must exist with criticality mapping)
- Depends on: quality-enforcement.md (authoritative criticality-to-strategy mapping)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | — |
| Remaining Work | 0 hours |
| Time Spent | — |

---

## Evidence
### Deliverables
| Deliverable | Type | Link |
|-------------|------|------|
| Criticality-based strategy selection tests | Python test file | `tests/e2e/test_adversary_templates_e2e.py` (criticality mapping section) |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History
| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. |
