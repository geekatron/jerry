# DEC-001: Local Context Test Strategy

> **Type:** Decision
> **Feature:** [FT-001](./FEATURE-WORKTRACKER.md) Session Hook Cleanup
> **Solution Epic:** [SE-004](../SOLUTION-WORKTRACKER.md) CLI and Claude Code Integration
> **Project:** PROJ-007-jerry-bugs
> **Status:** DECIDED
> **Created:** 2026-01-21
> **Last Updated:** 2026-01-21

---

## Decision

**Write new tests for the proper architecture (application layer) rather than migrating tests from the rogue file.**

---

## Context

During EN-001 Phase 1 exploration, we discovered:

1. Local context functionality exists in `src/interface/cli/session_start.py` (the rogue file)
2. Tests for this functionality exist in `tests/unit/interface/cli/test_session_start_local_context.py`
3. The rogue file will be deleted as part of EN-001
4. The proper architecture requires local context reading in the application layer

---

## Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **1. Write new tests** | Create tests for `LocalContextReader` port/adapter | Proper abstraction, clean design | More work upfront |
| 2. Migrate existing tests | Adapt existing tests to new implementation | Less duplication | Tests wrong abstraction |
| 3. Both | New tests now, migrate later | Comprehensive | Potential duplication |

---

## Decision Rationale

**Option 1 chosen** because:

1. **Proper abstraction**: Tests should test the application-layer port (`ILocalContextReader`) not CLI functions
2. **Clean architecture**: Hexagonal architecture requires testing ports/adapters, not interface layer internals
3. **BDD approach**: RED phase should write tests for the target design, not the current (broken) implementation
4. **No technical debt**: Existing tests for rogue file will be deleted with the file

---

## Implications

1. New test file: `tests/unit/application/ports/test_local_context_reader.py`
2. Existing tests in `test_session_start_local_context.py` will be deleted with the rogue file
3. Tests will initially fail (RED phase) until implementation is complete

---

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| Enabler | [en-001](./en-001-session-hook-tdd.md) | Session Hook TDD Cleanup |
| Rogue File | `src/interface/cli/session_start.py` | Contains current local context impl |
| Existing Tests | `tests/unit/interface/cli/test_session_start_local_context.py` | Tests for rogue file |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-21 | Decision documented - Option 1 selected | Claude |
