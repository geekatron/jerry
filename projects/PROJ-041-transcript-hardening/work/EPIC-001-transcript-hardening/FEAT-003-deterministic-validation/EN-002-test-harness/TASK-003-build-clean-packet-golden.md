# TASK-003: Build clean-packet golden where all 17 validation rules pass

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** EN-002
> **Owner:** eng-qa

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Build the baseline golden packet at `test_data/golden/clean-packet/` where every one of the 17 ADR-007 §4 validation rules (FILE-001..003, CONTENT-001..003, ANCHOR-001..003, SCHEMA-001..008) passes. Ship a sibling `expected.json` declaring all 17 rule results as `PASS` so the parameterized pytest harness can assert validator output against ground truth.

This golden is the reference packet against which all violation goldens (drift-detected, multi-violation, large-packet, bracket-canonical, ascii-fallback) are compared. If clean-packet ever fails after STORY-003..006 land, the implementation has regressed — not the test data.

---

## Acceptance Criteria

- [ ] `test_data/golden/clean-packet/` directory contains a complete `/transcript` packet (rendered .md files + sidecar JSON files)
- [ ] `test_data/golden/clean-packet/expected.json` declares all 17 rule_ids with `result: PASS`
- [ ] Pytest fixture in `tests/transcript/validation/conftest.py` loads this packet successfully
- [ ] During TDD Red phase (before STORY-003..006 implementations exist), tests fail with "rule not implemented", not "golden malformed"
- [ ] Manual review against `skills/transcript/SKILL.md` MUST-USE table confirms packet is structurally compliant with the spec
