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
| [Agent Assignment](#agent-assignment) | Specific skill+agent mappings |
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

## Agent Assignment

| Step | Skill | Agent | Purpose |
|------|-------|-------|---------|
| 1 | `/eng-team` | `eng-qa` | Author the 6 golden packets (clean, drift-detected, multi-violation, large-packet, bracket-canonical, ascii-fallback) with `expected.json` per packet |
| 2 | `/eng-team` | `eng-qa` | Author conftest.py fixtures and parameterized runner; configure ≥90% coverage gate |
| 3 | `/eng-team` | `eng-backend` | Wire stub adapters (FilesystemPacketLoader stub, SubprocessSandbox stub) for hermetic unit tests |
| 4 | `/eng-team` | `eng-qa` | Initial Red phase: confirm all 17 rule tests fail (implementations don't exist yet) |
| 5 | `/adversary` | `adv-executor` + `adv-scorer` | C4 ≥0.95 review on harness design + golden packets |
| 6 | `/worktracker` | `wt-verifier` | Validate AC; close |

---

## Acceptance Criteria

- [ ] All 6 golden packets exist under `test_data/golden/` with `expected.json`.
- [ ] **Per ps-architect D-6.3:** if the audit packet is unshareable (per EN-005 inputs note "audit packet (if shareable)"), `bracket-canonical` golden is synthesized from PDD-0102 patterns referenced in BUG-006 root cause section. Synthesized packet must reproduce the parse-error condition (failing render via `mmdc`) before bracket-escape fix is applied.
- [ ] Pytest harness at `tests/transcript/validation/golden/test_packet_validation.py` discovers golden packets via glob and parameterizes per directory.
- [ ] Conftest fixtures wire PacketValidator with stub adapters for hermetic execution.
- [ ] Initial test run: all 17 rules **fail** (Red phase confirmation — implementations don't exist yet).
- [ ] Coverage gate set to ≥90% on the validation module (will be enforced as STORY-003..006 implement rules).
- [ ] CI workflow stub added (will be filled in by STORY-012 with the actual gate).
- [ ] Documentation: `tests/transcript/validation/README.md` (within tests/, not skill folder per H-25 c) explains how to add a golden packet.

---

## Children Tasks

| ID | Title | Owner | Status |
|----|-------|-------|--------|
| [TASK-003](./TASK-003-build-clean-packet-golden.md) | Build clean-packet golden where all 17 validation rules pass | `eng-qa` | pending |
| [TASK-057](./TASK-057-build-drift-detected-golden.md) | Build drift-detected golden packet | `eng-qa` | pending |
| [TASK-058](./TASK-058-build-multi-violation-golden.md) | Build multi-violation golden packet | `eng-qa` | pending |
| [TASK-059](./TASK-059-build-large-packet-golden.md) | Build large-packet golden (1000+ chunks/segments) | `eng-qa` | pending |
| [TASK-060](./TASK-060-build-bracket-canonical-golden.md) | Build bracket-canonical golden (mindmap labels with [...]) | `eng-qa` | pending |
| [TASK-061](./TASK-061-build-ascii-fallback-golden.md) | Build ascii-fallback golden (ts-mindmap-ascii output) | `eng-qa` | pending |
| [TASK-062](./TASK-062-author-conftest-and-fixtures.md) | Author conftest.py with fixtures and stub adapters | `eng-qa` | pending |
| [TASK-063](./TASK-063-author-parameterized-runner-and-coverage.md) | Author parameterized test runner; configure coverage gate | `eng-qa` | pending |
| [TASK-064](./TASK-064-run-adversary-c4-on-harness.md) | Run /adversary C4 review on harness design + golden packets | `adv-executor` | pending |

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
