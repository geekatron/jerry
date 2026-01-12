# Detailed Implementation Plan: TD-015 CLI Architecture Remediation

> **Status**: SPECIFICATION COMPLETE - READY FOR IMPLEMENTATION
> **Priority**: CRITICAL
> **Source**: BUG-006, DISC-011, DISC-012, DISC-013
> **Created**: 2026-01-12
> **Revised**: 2026-01-12
> **Author**: Claude

---

## Implementation Standards

### Test Coverage Requirements

Per `impl-es-e-003-bdd-tdd-patterns.md` and `dev-skill-e-009-test-strategy.md`:

| Test Layer | Distribution | Coverage Target |
|------------|--------------|-----------------|
| Unit | 65-75% of tests | >90% line, >85% branch |
| Integration | 20-25% of tests | >80% line |
| System/E2E | 5-10% of tests | Critical paths |
| Architecture | As needed | Boundary enforcement |

### Within Each Test Layer

| Category | Percentage | Focus |
|----------|------------|-------|
| **Happy Path** | 60-70% | Valid inputs, successful scenarios |
| **Negative** | 20-30% | Invalid inputs, error conditions, violations |
| **Edge Cases** | 10-15% | Boundaries, nulls, empty, max/min |

### Quality Standards

- **Red/Green/Refactor**: Every implementation sub-task starts with RED (failing test)
- **No Placeholders**: All tests must use real data and assertions
- **Evidence Required**: Each task completion requires validatable evidence
- **Patterns Reference**: Follow `impl-es-e-003` for BDD, `dev-skill-e-009` for test strategy

---

## Phase 1: Application Layer Infrastructure

### 1.1 Dispatcher Port Interfaces

| Sub-task | Description | Evidence |
|----------|-------------|----------|
| 1.1.1 | Create `src/application/__init__.py` | File exists |
| 1.1.2 | Create `src/application/ports/__init__.py` | File exists |
| 1.1.3 | Create `src/application/ports/dispatcher.py` | File exists |
| 1.1.4 | Define `IQueryDispatcher` Protocol | `grep "class IQueryDispatcher" src/application/ports/dispatcher.py` |
| 1.1.5 | Define `ICommandDispatcher` Protocol | `grep "class ICommandDispatcher" src/application/ports/dispatcher.py` |
| 1.1.6 | Define `QueryHandlerNotFoundError` exception | Exception class exists |
| 1.1.7 | Define `DuplicateHandlerError` exception | Exception class exists |
| 1.1.8 | Type hints complete | `pyright src/application/ports/dispatcher.py` passes |

**Tests for 1.1** (`tests/unit/application/ports/test_dispatcher_protocol.py`):

| Test Category | Count | Focus |
|---------------|-------|-------|
| Happy Path (60%) | 3 | Protocol definition, type correctness, docstrings |
| Negative (30%) | 2 | Missing methods, wrong signatures |
| Edge (10%) | 1 | Generic type constraints |

---

### 1.2 Query Dispatcher Implementation

| Sub-task | Description | Evidence |
|----------|-------------|----------|
| 1.2.1 | Create `src/application/dispatchers/__init__.py` | File exists |
| 1.2.2 | Create `src/application/dispatchers/query_dispatcher.py` | File exists |
| 1.2.3 | RED: Write `test_dispatch_routes_to_handler` | Test fails |
| 1.2.4 | GREEN: Implement basic dispatch | Test passes |
| 1.2.5 | RED: Write `test_dispatch_unknown_query_raises` | Test fails |
| 1.2.6 | GREEN: Implement error handling | Test passes |
| 1.2.7 | RED: Write negative/edge tests | Tests fail |
| 1.2.8 | GREEN: Handle all scenarios | All tests pass |
| 1.2.9 | REFACTOR: Add type hints, docstrings | `pyright` passes |

**Tests for 1.2** (`tests/unit/application/dispatchers/test_query_dispatcher.py`):

| Test Category | Count | Focus |
|---------------|-------|-------|
| Happy Path (60%) | 6 | Dispatch returns result, correct handler invoked, multiple handlers |
| Negative (30%) | 3 | None query, unregistered query, handler exception |
| Edge (10%) | 2 | Handler returns None, subclass query routing |

---

### 1.3 Query Handlers

#### 1.3.1 GetProjectContextHandler

| Sub-task | Description | Evidence |
|----------|-------------|----------|
| 1.3.1.1 | Create `src/application/handlers/__init__.py` | File exists |
| 1.3.1.2 | Create `src/application/handlers/get_project_context_handler.py` | File exists |
| 1.3.1.3 | RED: Write unit tests with mocked deps | Tests fail |
| 1.3.1.4 | GREEN: Implement handler | Tests pass |
| 1.3.1.5 | RED: Write negative/edge tests | Tests fail |
| 1.3.1.6 | GREEN: Handle all scenarios | All tests pass |
| 1.3.1.7 | REFACTOR: Type hints, docstrings | `pyright` passes |

**Tests for 1.3.1** (`tests/unit/application/handlers/test_get_project_context_handler.py`):

| Test Category | Count | Focus |
|---------------|-------|-------|
| Happy Path (60%) | 4 | Valid project, project not set, available projects |
| Negative (30%) | 2 | Invalid project format, permission denied |
| Edge (10%) | 1 | Empty project directory, JERRY_PROJECT empty string |

**Reference**: Follow handler pattern in `dev-skill-e-009` §Integration Tests (lines 359-517)

---

#### 1.3.2 ScanProjectsHandler

| Sub-task | Description | Evidence |
|----------|-------------|----------|
| 1.3.2.1 | Create handler file | File exists |
| 1.3.2.2 | RED: Write unit tests | Tests fail |
| 1.3.2.3 | GREEN: Implement handler | Tests pass |
| 1.3.2.4 | REFACTOR | `pyright` passes |

**Tests**: Same distribution as 1.3.1 (4 happy, 2 negative, 1 edge)

---

#### 1.3.3 ValidateProjectHandler

| Sub-task | Description | Evidence |
|----------|-------------|----------|
| 1.3.3.1 | Create handler file | File exists |
| 1.3.3.2 | RED: Write unit tests | Tests fail |
| 1.3.3.3 | GREEN: Implement handler | Tests pass |
| 1.3.3.4 | REFACTOR | `pyright` passes |

**Tests**: Same distribution as 1.3.1

---

## Phase 2: Composition Root

### 2.1 Bootstrap Module

| Sub-task | Description | Evidence |
|----------|-------------|----------|
| 2.1.1 | Create `src/bootstrap.py` | File exists |
| 2.1.2 | Import infrastructure adapters | Imports present |
| 2.1.3 | Wire handlers with dependencies | Code inspection |
| 2.1.4 | Create dispatcher with handlers | Code inspection |
| 2.1.5 | Create `create_cli_application()` factory | Function exists |
| 2.1.6 | RED: Write integration test for factory | Test fails |
| 2.1.7 | GREEN: Factory returns configured adapter | Test passes |

**Tests for 2.1** (`tests/integration/test_bootstrap.py`):

| Test Category | Count | Focus |
|---------------|-------|-------|
| Happy Path (60%) | 3 | Factory returns adapter, dispatcher has handlers, handlers have deps |
| Negative (30%) | 2 | Missing dependency raises, duplicate handler raises |
| Edge (10%) | 1 | Empty handler registry |

---

### 2.2 Architecture Tests

| Sub-task | Description | Evidence |
|----------|-------------|----------|
| 2.2.1 | Create `tests/architecture/test_composition_root.py` | File exists |
| 2.2.2 | Write `test_bootstrap_is_sole_infrastructure_importer` | Test passes |
| 2.2.3 | Write `test_cli_adapter_has_no_infrastructure_imports` | Test passes |
| 2.2.4 | Write `test_application_layer_has_no_infrastructure_imports` | Test passes |

**Reference**: Use `pytest-archon` per existing architecture tests in `tests/work_tracking/architecture/`

---

## Phase 3: CLI Adapter Refactor

### 3.1 Convert to Class-Based Adapter

| Sub-task | Description | Evidence |
|----------|-------------|----------|
| 3.1.1 | Create `CLIAdapter` class | Class exists |
| 3.1.2 | Constructor receives `IQueryDispatcher` | DI via constructor |
| 3.1.3 | Remove all infrastructure imports | `grep "from src.infrastructure" src/interface/cli/main.py` empty |
| 3.1.4 | Refactor `cmd_init` to use dispatcher | Code inspection |
| 3.1.5 | Update entry point to use bootstrap | `main()` calls `create_cli_application()` |
| 3.1.6 | RED: Write integration tests | Tests fail |
| 3.1.7 | GREEN: All commands route through dispatcher | Tests pass |

**Tests for 3.1** (`tests/integration/cli/test_cli_dispatcher_integration.py`):

| Test Category | Count | Focus |
|---------------|-------|-------|
| Happy Path (60%) | 3 | init dispatches query, handler result returned |
| Negative (30%) | 2 | Dispatcher None raises, handler error propagates |
| Edge (10%) | 1 | Empty result handling |

---

### 3.2 E2E Regression Tests

| Sub-task | Description | Evidence |
|----------|-------------|----------|
| 3.2.1 | Create `tests/e2e/cli/test_cli_regression.py` | File exists |
| 3.2.2 | Write `test_jerry_init_still_works` | Test passes |
| 3.2.3 | Write `test_jerry_help_still_works` | Test passes |
| 3.2.4 | Write `test_jerry_version_still_works` | Test passes |
| 3.2.5 | Write `test_invalid_command_shows_error` | Test passes |

**Reference**: Follow E2E pattern in `dev-skill-e-009` §Layer 4: E2E Tests (lines 880-1025)

---

## Phase 4: CLI Namespaces

### 4.1 Projects Namespace

| Sub-task | Description | Evidence |
|----------|-------------|----------|
| 4.1.1 | Create `src/interface/cli/commands/__init__.py` | File exists |
| 4.1.2 | Create `src/interface/cli/commands/projects.py` | File exists |
| 4.1.3 | Implement `jerry projects list` | CLI output verified |
| 4.1.4 | Implement `jerry projects validate <id>` | CLI output verified |
| 4.1.5 | Register namespace in main | Namespace registered |
| 4.1.6 | RED: Write system tests | Tests fail |
| 4.1.7 | GREEN: All commands work | Tests pass |

**Tests for 4.1** (`tests/system/cli/test_projects_namespace.py`):

| Test Category | Count | Focus |
|---------------|-------|-------|
| Happy Path (60%) | 3 | list works, validate works, help shows commands |
| Negative (30%) | 2 | validate invalid id, unknown subcommand |
| Edge (10%) | 1 | Empty projects directory |

---

### 4.2 Session Namespace (Scaffold)

| Sub-task | Description | Evidence |
|----------|-------------|----------|
| 4.2.1 | Create `src/interface/cli/commands/session.py` | File exists |
| 4.2.2 | Register namespace | Namespace registered |
| 4.2.3 | `jerry session --help` shows placeholder | Help output verified |

---

### 4.3 Worktracker Namespace (Scaffold)

| Sub-task | Description | Evidence |
|----------|-------------|----------|
| 4.3.1 | Create `src/interface/cli/commands/worktracker.py` | File exists |
| 4.3.2 | Register namespace | Namespace registered |
| 4.3.3 | `jerry worktracker --help` shows placeholder | Help output verified |

---

## Phase 5: TOON Format Integration

### 5.1 Add Dependency

| Sub-task | Description | Evidence |
|----------|-------------|----------|
| 5.1.1 | Add `python-toon>=0.1.0` to pyproject.toml | Entry exists |
| 5.1.2 | Run `pip install -e .` | Installs without error |
| 5.1.3 | Verify import works | `python -c "import toon"` succeeds |

**Reference**: TOON spec in `projects/archive/research/TOON_FORMAT_ANALYSIS.md`

---

### 5.2 Formatters

#### 5.2.1 TOON Formatter

| Sub-task | Description | Evidence |
|----------|-------------|----------|
| 5.2.1.1 | Create `src/interface/cli/formatters/__init__.py` | File exists |
| 5.2.1.2 | Create `src/interface/cli/formatters/toon_formatter.py` | File exists |
| 5.2.1.3 | RED: Write unit tests | Tests fail |
| 5.2.1.4 | GREEN: Implement formatter | Tests pass |
| 5.2.1.5 | RED: Write contract tests for TOON spec | Tests fail |
| 5.2.1.6 | GREEN: Output conforms to TOON spec | Tests pass |

**Tests for 5.2.1** (`tests/unit/interface/cli/formatters/test_toon_formatter.py`):

| Test Category | Count | Focus |
|---------------|-------|-------|
| Happy Path (60%) | 4 | Format dict, format list, format scalar, smaller than JSON |
| Negative (30%) | 2 | Invalid input type, serialization error |
| Edge (10%) | 1 | None, empty list, tabs/newlines in data |

**Contract Tests** (`tests/contract/output_formats/test_toon_contract.py`):

| Test | Focus |
|------|-------|
| `test_toon_output_parses` | Output parseable |
| `test_toon_delimiter_is_tab` | Correct delimiter |
| `test_toon_escaping` | Special chars escaped |

**Reference**: Implementation guide `impl-es-e-002-toon-serialization.md`

---

#### 5.2.2 JSON Formatter

| Sub-task | Description | Evidence |
|----------|-------------|----------|
| 5.2.2.1 | Create `json_formatter.py` | File exists |
| 5.2.2.2 | RED: Write tests | Tests fail |
| 5.2.2.3 | GREEN: Implement | Tests pass |

**Tests**: 3 happy, 1 negative, 1 edge

---

#### 5.2.3 Human Formatter

| Sub-task | Description | Evidence |
|----------|-------------|----------|
| 5.2.3.1 | Create `human_formatter.py` | File exists |
| 5.2.3.2 | RED: Write tests | Tests fail |
| 5.2.3.3 | GREEN: Implement | Tests pass |

**Tests**: 3 happy, 1 negative, 1 edge

---

### 5.3 Format Flags

| Sub-task | Description | Evidence |
|----------|-------------|----------|
| 5.3.1 | Add `--toon` flag (default) | Flag in argparse |
| 5.3.2 | Add `--json` flag | Flag in argparse |
| 5.3.3 | Add `--human` flag | Flag in argparse |
| 5.3.4 | Implement format selection | Correct formatter chosen |
| 5.3.5 | RED: Write system tests | Tests fail |
| 5.3.6 | GREEN: All flags work | Tests pass |

**Tests for 5.3** (`tests/system/cli/test_format_flags.py`):

| Test Category | Count | Focus |
|---------------|-------|-------|
| Happy Path (60%) | 3 | Default is TOON, --json works, --human works |
| Negative (30%) | 2 | Conflicting flags, unknown format |
| Edge (10%) | 1 | Empty output formatting |

---

## Acceptance Criteria Matrix

| ID | Criterion | Phase | Evidence Type |
|----|-----------|-------|---------------|
| AC-01 | CLI adapter receives dispatcher via constructor | 3 | Code inspection |
| AC-02 | No infrastructure imports in CLI adapter | 3 | Architecture test PASS |
| AC-03 | All queries routed through dispatcher | 3 | Integration test PASS |
| AC-04 | Composition root external to adapters | 2 | `src/bootstrap.py` exists |
| AC-05 | Handler tests with mocked dependencies | 1 | Unit tests PASS |
| AC-06 | `jerry session` namespace exists | 4 | System test PASS |
| AC-07 | `jerry worktracker` namespace exists | 4 | System test PASS |
| AC-08 | `jerry projects` namespace exists | 4 | System test PASS |
| AC-09 | TOON is default output format | 5 | System test PASS |
| AC-10 | `--json` flag works | 5 | System test PASS |
| AC-11 | `--human` flag works | 5 | System test PASS |
| AC-12 | E2E regression tests pass | 3 | All E2E tests PASS |

---

## Parallel Execution Strategy

Tasks that can be executed in parallel (no dependencies):

| Group | Tasks |
|-------|-------|
| Group A | 1.1 (Dispatcher Ports) + 1.3.1 through 1.3.3 (Handlers) |
| Group B | 2.2 (Architecture Tests) - write first, fail initially |
| Group C | 4.2 (Session scaffold) + 4.3 (Worktracker scaffold) |
| Group D | 5.2.1 (TOON) + 5.2.2 (JSON) + 5.2.3 (Human) formatters |

Sequential dependencies:
- 1.2 (Dispatcher) depends on 1.1 (Ports)
- 2.1 (Bootstrap) depends on 1.2 + 1.3.*
- 3.1 (CLI Refactor) depends on 2.1
- 4.1 (Projects namespace) depends on 3.1
- 5.3 (Format flags) depends on 5.2.*

---

## References

| Document | Path | Use |
|----------|------|-----|
| BDD/TDD Patterns | `impl-es-e-003-bdd-tdd-patterns.md` | Test distribution ratios |
| Test Strategy | `dev-skill-e-009-test-strategy.md` | Test pyramid, fixtures, CI |
| ADR Test-First | `ADR-001-test-first-enforcement.md` | Enforcement levels |
| TOON Analysis | `TOON_FORMAT_ANALYSIS.md` | TOON spec v3.0 |
| TOON Implementation | `impl-es-e-002-toon-serialization.md` | Serializer patterns |
| Architecture Standards | `PYTHON-ARCHITECTURE-STANDARDS.md` | Dispatcher pattern |
| ADR-CLI-001 | `ADR-CLI-001-primary-adapter.md` | D2-AMENDED decisions |

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-12 | Claude | Initial creation with BDD scenarios (verbose) |
| 2026-01-12 | Claude | **REVISED**: Task-oriented format with coverage requirements |
