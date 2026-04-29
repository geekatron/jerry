# EN-002: Test harness + golden packets in test_data/

> **Type:** enabler
> **Enabler Type:** infrastructure
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-04-28T00:00:00Z
> **Parent:** FEAT-003
> **Owner:** adam.nowak
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this Enabler delivers |
| [Technical Approach](#technical-approach) | Golden packet strategy + test harness design |
| [Golden Packet Strategy](#golden-packet-strategy) | What packets are checked in |
| [Test Harness Design](#test-harness-design) | How rules are parameterized |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Change log |

---

## Summary

Stand up the test harness for FEAT-003 validators following TDD Red/Green/Refactor. Each of the 17 ADR-007 §4 rule IDs becomes a parameterized test case with a golden packet exercising both the pass and fail paths. Tests precede implementation (TDD discipline): write failing tests in EN-002, then green them in STORY-003..006, then refactor.

---

## Technical Approach

The test harness follows TDD Red/Green/Refactor: failing tests precede implementation in EN-002, then green them in STORY-003..006, then refactor for DRY. Subsections below specify the concrete shape.

---

## Golden Packet Strategy

| Packet | Purpose |
|--------|---------|
| `test_data/golden/clean-packet/` | All 17 rules pass; baseline |
| `test_data/golden/drift-detected/` | Declared counts ≠ walked truth (exercises declared-derived coupling fix) |
| `test_data/golden/multi-violation/` | Several rules fail simultaneously (exercises report aggregation) |
| `test_data/golden/large-packet/` | 1000+ chunks, 1000+ segments (exercises forward-compat regex from BUG-002, BUG-004) |
| `test_data/golden/bracket-canonical/` | Mindmap labels with bracketed canonical forms (exercises FEAT-005 BUG-006 fix) |
| `test_data/golden/ascii-fallback/` | ts-mindmap-ascii output (regression coverage) |

Each golden packet ships with a `expected.json` describing the expected validator output (rule_id → pass/fail, evidence count). Pytest parametrizes over `test_data/golden/*/` directories.

---

## Test Harness Design

| Component | Path | Responsibility |
|-----------|------|----------------|
| Pytest fixtures | `tests/transcript/validation/conftest.py` | Load golden packets, build PacketValidator with stub adapters |
| Parameterized runner | `tests/transcript/validation/golden/test_packet_validation.py` | Iterate over `test_data/golden/*/`, assert validator output matches `expected.json` |
| Stub adapters | `tests/transcript/validation/_stubs/` | Filesystem and subprocess stubs for hermetic unit tests |
| Coverage gate | `pyproject.toml` | ≥90% line coverage on `src/jerry/transcript/validation/` per H-20 |

---

## Acceptance Criteria

- [ ] All 6 golden packets exist under `test_data/golden/` with `expected.json`.
- [ ] Pytest harness at `tests/transcript/validation/golden/test_packet_validation.py` discovers golden packets via glob and parameterizes per directory.
- [ ] Conftest fixtures wire PacketValidator with stub adapters for hermetic execution.
- [ ] Initial test run: all 17 rules **fail** (Red phase confirmation — implementations don't exist yet).
- [ ] Coverage gate set to ≥90% on the validation module (will be enforced as STORY-003..006 implement rules).
- [ ] CI workflow stub added (will be filled in by STORY-012 with the actual gate).
- [ ] Documentation: `tests/transcript/validation/README.md` (within tests/, not skill folder per H-25 c) explains how to add a golden packet.

---

## Children Tasks

| ID | Title | Status |
|----|-------|--------|
| TASK-001 | Build clean-packet golden (all rules pass) | pending |
| TASK-002 | Build drift-detected golden | pending |
| TASK-003 | Build multi-violation golden | pending |
| TASK-004 | Build large-packet golden (1000+ chunks/segments) | pending |
| TASK-005 | Build bracket-canonical golden | pending |
| TASK-006 | Build ascii-fallback golden | pending |
| TASK-007 | Author conftest.py with fixtures and stub adapters | pending |
| TASK-008 | Author parameterized test runner | pending |
| TASK-009 | Configure coverage gate (≥90%) | pending |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-003](../FEAT-003-deterministic-validation.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | EN-001 | Module skeleton + ports must exist for stub adapters to wire |
| Blocks | STORY-003..STORY-006 | TDD Red phase requires failing tests in place first |
| Blocks | STORY-012 | CI workflow gates against this harness |

### Source

- [#273 §C5](https://github.com/geekatron/jerry/issues/273) — author's gist tests as starting reference

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Enabler created. TDD harness + 6 golden packet strategies captured. |
