# Detailed Implementation Plan: TD-015 CLI Architecture Remediation

> **Status**: SPECIFICATION COMPLETE - READY FOR IMPLEMENTATION
> **Priority**: CRITICAL
> **Source**: BUG-006, DISC-011, DISC-012, DISC-013
> **Created**: 2026-01-12
> **Author**: Claude
> **Summary Document**: `IMPL-TD-015-CLI-ARCHITECTURE-REMEDIATION.md`

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [BDD Approach](#bdd-approach)
3. [Test Pyramid Structure](#test-pyramid-structure)
4. [Phase 1: Application Layer Infrastructure](#phase-1-application-layer-infrastructure)
5. [Phase 2: Composition Root](#phase-2-composition-root)
6. [Phase 3: CLI Adapter Refactor](#phase-3-cli-adapter-refactor)
7. [Phase 4: CLI Namespaces](#phase-4-cli-namespaces)
8. [Phase 5: TOON Format Integration](#phase-5-toon-format-integration)
9. [Cross-Cutting Concerns](#cross-cutting-concerns)
10. [Acceptance Criteria Matrix](#acceptance-criteria-matrix)
11. [Evidence Registry](#evidence-registry)

---

## Executive Summary

This document provides atomic-level task breakdown for TD-015 remediation with:
- **pytest-bdd** Gherkin feature files
- **Test pyramid** organized by layer
- **Edge cases** and **failure scenarios** enumerated
- **Evidence criteria** per task
- **Red/Green/Refactor** iteration cycles

---

## BDD Approach

### Framework

- **pytest-bdd** for Gherkin feature files
- Feature files: `tests/features/{domain}/*.feature`
- Step definitions: `tests/step_defs/{domain}/test_*.py`
- Conftest fixtures: `tests/conftest.py`

### Naming Convention

```
Feature: {Component} - {Capability}
  Scenario: {Given}_{When}_{Then}

Test function: test_{scenario_name}
```

---

## Test Pyramid Structure

```
tests/
├── features/                    # Gherkin feature files
│   ├── dispatcher/
│   │   ├── query_dispatch.feature
│   │   └── handler_registration.feature
│   ├── composition_root/
│   │   └── dependency_wiring.feature
│   ├── cli/
│   │   ├── command_routing.feature
│   │   └── namespace_isolation.feature
│   └── formatters/
│       └── toon_output.feature
├── step_defs/                   # BDD step definitions
│   ├── dispatcher/
│   ├── composition_root/
│   ├── cli/
│   └── formatters/
├── unit/                        # Pure unit tests
│   ├── application/
│   │   ├── dispatchers/
│   │   └── handlers/
│   └── interface/
│       └── cli/
│           └── formatters/
├── integration/                 # Cross-layer tests
│   └── cli/
├── system/                      # Full system tests
│   └── cli/
├── e2e/                         # End-to-end tests
│   └── cli/
├── contract/                    # Schema/contract tests
│   └── output_formats/
├── architecture/                # Boundary tests
│   └── cli/
└── conftest.py                  # Shared fixtures
```

---

## Phase 1: Application Layer Infrastructure

### 1.1 Create Dispatcher Port Interfaces

#### Task 1.1.1: Define IQueryDispatcher Protocol

**File**: `src/application/ports/dispatcher.py`

**BDD Feature** (`tests/features/dispatcher/query_dispatch.feature`):

```gherkin
Feature: Query Dispatcher - Routing
  As the application layer
  I want to dispatch queries to their handlers
  So that adapters don't need to know about handler implementations

  Background:
    Given a dispatcher with registered handlers

  Scenario: Dispatch known query type to registered handler
    Given a handler is registered for "GetProjectContextQuery"
    When I dispatch a GetProjectContextQuery
    Then the registered handler should be invoked
    And the handler result should be returned

  Scenario: Dispatch unknown query type raises error
    Given no handler is registered for "UnknownQuery"
    When I dispatch an UnknownQuery
    Then a QueryHandlerNotFoundError should be raised
    And the error message should contain "UnknownQuery"

  Scenario: Dispatch with None query raises error
    When I dispatch None as a query
    Then a ValueError should be raised
    And the error message should indicate "query cannot be None"

  Scenario: Handler raises exception propagates to caller
    Given a handler that raises RuntimeError
    When I dispatch a query to that handler
    Then the RuntimeError should propagate to the caller
    And the original exception message should be preserved
```

**Edge Cases**:

| ID | Edge Case | Expected Behavior | Test |
|----|-----------|-------------------|------|
| EC-1.1.1-A | Query is None | Raise ValueError | `test_dispatch_none_query_raises_value_error` |
| EC-1.1.1-B | Query type not registered | Raise QueryHandlerNotFoundError | `test_dispatch_unknown_query_raises_not_found` |
| EC-1.1.1-C | Handler returns None | Return None (valid) | `test_handler_returning_none_is_valid` |
| EC-1.1.1-D | Handler raises exception | Propagate exception | `test_handler_exception_propagates` |
| EC-1.1.1-E | Duplicate handler registration | Raise DuplicateHandlerError | `test_duplicate_registration_raises_error` |

**Failure Scenarios**:

| ID | Failure | Handling | Test |
|----|---------|----------|------|
| FS-1.1.1-A | Handler import fails | Fail fast at registration | `test_invalid_handler_fails_registration` |
| FS-1.1.1-B | Handler missing execute method | Raise TypeError at registration | `test_handler_without_execute_fails` |

**Sub-tasks**:

| ID | Task | Evidence | Status |
|----|------|----------|--------|
| 1.1.1.1 | Create `src/application/__init__.py` | File exists | [ ] |
| 1.1.1.2 | Create `src/application/ports/__init__.py` | File exists | [ ] |
| 1.1.1.3 | Define `IQueryDispatcher` Protocol | `grep "class IQueryDispatcher" src/application/ports/dispatcher.py` returns match | [ ] |
| 1.1.1.4 | Define `ICommandDispatcher` Protocol | `grep "class ICommandDispatcher" src/application/ports/dispatcher.py` returns match | [ ] |
| 1.1.1.5 | Define `QueryHandlerNotFoundError` exception | Exception class exists | [ ] |
| 1.1.1.6 | Define `DuplicateHandlerError` exception | Exception class exists | [ ] |
| 1.1.1.7 | Type hints complete | `pyright src/application/ports/dispatcher.py` passes | [ ] |
| 1.1.1.8 | Docstrings complete | All public members documented | [ ] |

**Red/Green/Refactor Cycle**:

```
Iteration 1 (RED):
  - Write test_dispatch_known_query_returns_result
  - Run pytest → FAIL (no dispatcher.py)

Iteration 2 (GREEN):
  - Create minimal IQueryDispatcher protocol
  - Run pytest → PASS

Iteration 3 (REFACTOR):
  - Add type hints
  - Add docstrings
  - Run pytest → PASS

Iteration 4 (RED):
  - Write test_dispatch_unknown_query_raises_not_found
  - Run pytest → FAIL

Iteration 5 (GREEN):
  - Implement QueryHandlerNotFoundError
  - Run pytest → PASS

... continue for all edge cases
```

---

#### Task 1.1.2: Define IQueryHandler Protocol

**File**: `src/application/ports/handler.py`

**BDD Feature** (`tests/features/dispatcher/handler_registration.feature`):

```gherkin
Feature: Query Handler - Contract
  As a handler implementer
  I want a clear contract for handlers
  So that I can implement handlers correctly

  Scenario: Handler implements execute method
    Given a class implementing IQueryHandler
    When the class has an execute(query) method
    Then the class should be a valid handler
    And the handler should be registrable with a dispatcher

  Scenario: Handler without execute method is invalid
    Given a class without execute method
    When I try to register it as a handler
    Then a TypeError should be raised

  Scenario: Handler with wrong execute signature is invalid
    Given a class with execute() taking no arguments
    When I try to register it as a handler
    Then a TypeError should be raised
```

**Sub-tasks**:

| ID | Task | Evidence | Status |
|----|------|----------|--------|
| 1.1.2.1 | Create `src/application/ports/handler.py` | File exists | [ ] |
| 1.1.2.2 | Define `IQueryHandler[TQuery, TResult]` Protocol | Protocol with Generic types | [ ] |
| 1.1.2.3 | Define `ICommandHandler[TCommand, TResult]` Protocol | Protocol with Generic types | [ ] |
| 1.1.2.4 | Type hints complete | `pyright` passes | [ ] |

---

### 1.2 Create Query Dispatcher Implementation

#### Task 1.2.1: Implement QueryDispatcher

**File**: `src/application/dispatchers/query_dispatcher.py`

**Unit Tests** (`tests/unit/application/dispatchers/test_query_dispatcher.py`):

```python
"""
Unit tests for QueryDispatcher.

Test Categories:
- Happy Path: Successful dispatch scenarios
- Edge Cases: Boundary conditions
- Failure Scenarios: Error handling
"""

# Happy Path Tests
def test_dispatch_returns_handler_result():
    """Handler result is returned by dispatcher."""

def test_dispatch_invokes_correct_handler():
    """Correct handler is invoked for query type."""

def test_multiple_handlers_dispatch_correctly():
    """Multiple registered handlers route correctly."""

# Edge Case Tests
def test_handler_returning_none_is_valid():
    """None is a valid handler return value."""

def test_handler_returning_empty_list_is_valid():
    """Empty list is a valid handler return value."""

def test_dispatch_with_subclass_query_uses_exact_match():
    """Query subclasses don't match parent handler."""

# Failure Scenario Tests
def test_dispatch_none_raises_value_error():
    """Dispatching None raises ValueError."""

def test_dispatch_unregistered_query_raises_not_found():
    """Dispatching unregistered query raises QueryHandlerNotFoundError."""

def test_handler_exception_propagates():
    """Handler exceptions propagate to caller."""

def test_duplicate_registration_raises_error():
    """Registering same query type twice raises DuplicateHandlerError."""
```

**Sub-tasks**:

| ID | Task | Evidence | Status |
|----|------|----------|--------|
| 1.2.1.1 | Create `src/application/dispatchers/__init__.py` | File exists | [ ] |
| 1.2.1.2 | Create `QueryDispatcher` class | Class exists | [ ] |
| 1.2.1.3 | Implement `register(query_type, handler)` | Method exists | [ ] |
| 1.2.1.4 | Implement `dispatch(query) -> result` | Method exists | [ ] |
| 1.2.1.5 | Write RED test: dispatch returns result | Test fails initially | [ ] |
| 1.2.1.6 | Write GREEN: minimal implementation | Test passes | [ ] |
| 1.2.1.7 | Write RED test: unknown query raises error | Test fails initially | [ ] |
| 1.2.1.8 | Write GREEN: error handling | Test passes | [ ] |
| 1.2.1.9 | REFACTOR: type hints and docs | pyright passes | [ ] |
| 1.2.1.10 | All edge case tests pass | pytest results | [ ] |
| 1.2.1.11 | All failure scenario tests pass | pytest results | [ ] |

---

### 1.3 Create Query Handlers

#### Task 1.3.1: GetProjectContextHandler

**File**: `src/application/handlers/get_project_context_handler.py`

**BDD Feature** (`tests/features/dispatcher/get_project_context.feature`):

```gherkin
Feature: GetProjectContext Handler
  As the session management bounded context
  I want to retrieve project context
  So that CLI can display current project state

  Scenario: Get context for valid project
    Given JERRY_PROJECT is set to "PROJ-001-plugin-cleanup"
    And the project directory exists
    When I execute GetProjectContextQuery
    Then I should receive a ProjectContext result
    And the result should contain project_id "PROJ-001-plugin-cleanup"
    And the result should contain project_path

  Scenario: Get context when no project set
    Given JERRY_PROJECT is not set
    When I execute GetProjectContextQuery
    Then I should receive a ProjectContext result
    And project_active should be False
    And available_projects should be populated

  Scenario: Get context for invalid project
    Given JERRY_PROJECT is set to "INVALID-PROJECT"
    When I execute GetProjectContextQuery
    Then I should receive a ProjectContext result
    And validation_error should contain error message

  Scenario: Get context when projects directory missing
    Given the projects directory does not exist
    When I execute GetProjectContextQuery
    Then a ProjectsDirectoryNotFoundError should be raised
```

**Edge Cases**:

| ID | Edge Case | Expected Behavior | Test |
|----|-----------|-------------------|------|
| EC-1.3.1-A | JERRY_PROJECT empty string | Treat as not set | `test_empty_project_env_treated_as_not_set` |
| EC-1.3.1-B | Project dir exists but empty | Return context with empty data | `test_empty_project_directory` |
| EC-1.3.1-C | Project ID format invalid | Return validation error in context | `test_invalid_project_id_format` |
| EC-1.3.1-D | Projects dir has no PROJ-* dirs | Return empty available_projects | `test_no_projects_available` |
| EC-1.3.1-E | Multiple projects exist | Return all in available_projects | `test_multiple_projects_listed` |

**Failure Scenarios**:

| ID | Failure | Handling | Test |
|----|---------|----------|------|
| FS-1.3.1-A | Repository raises IOError | Propagate with context | `test_repository_io_error_propagates` |
| FS-1.3.1-B | Environment adapter fails | Propagate with context | `test_environment_error_propagates` |
| FS-1.3.1-C | Permission denied on directory | Raise PermissionDeniedError | `test_permission_denied_error` |

**Sub-tasks**:

| ID | Task | Evidence | Status |
|----|------|----------|--------|
| 1.3.1.1 | Create `src/application/handlers/__init__.py` | File exists | [ ] |
| 1.3.1.2 | Create handler file | File exists | [ ] |
| 1.3.1.3 | Define `GetProjectContextHandler` class | Class exists | [ ] |
| 1.3.1.4 | Constructor accepts repository, environment ports | DI via constructor | [ ] |
| 1.3.1.5 | Implement `execute(query)` method | Method exists | [ ] |
| 1.3.1.6 | Unit tests with mocked dependencies | All tests pass | [ ] |
| 1.3.1.7 | Edge case tests | All pass | [ ] |
| 1.3.1.8 | Failure scenario tests | All pass | [ ] |

---

#### Task 1.3.2: ScanProjectsHandler

**File**: `src/application/handlers/scan_projects_handler.py`

**Similar structure to 1.3.1** (abbreviated for space)

**Sub-tasks**:

| ID | Task | Evidence | Status |
|----|------|----------|--------|
| 1.3.2.1 | Create handler file | File exists | [ ] |
| 1.3.2.2 | Define `ScanProjectsHandler` class | Class exists | [ ] |
| 1.3.2.3 | Unit tests with mocked dependencies | All tests pass | [ ] |
| 1.3.2.4 | Edge case tests | All pass | [ ] |
| 1.3.2.5 | Failure scenario tests | All pass | [ ] |

---

#### Task 1.3.3: ValidateProjectHandler

**File**: `src/application/handlers/validate_project_handler.py`

**Sub-tasks**:

| ID | Task | Evidence | Status |
|----|------|----------|--------|
| 1.3.3.1 | Create handler file | File exists | [ ] |
| 1.3.3.2 | Define `ValidateProjectHandler` class | Class exists | [ ] |
| 1.3.3.3 | Unit tests with mocked dependencies | All tests pass | [ ] |
| 1.3.3.4 | Edge case tests | All pass | [ ] |
| 1.3.3.5 | Failure scenario tests | All pass | [ ] |

---

## Phase 2: Composition Root

### 2.1 Create Bootstrap Module

#### Task 2.1.1: Implement Composition Root

**File**: `src/bootstrap.py`

**BDD Feature** (`tests/features/composition_root/dependency_wiring.feature`):

```gherkin
Feature: Composition Root - Dependency Wiring
  As the application startup
  I want all dependencies wired in one place
  So that adapters receive pre-configured components

  Scenario: Create CLI application with all dependencies
    When I call create_cli_application()
    Then I should receive a CLIAdapter instance
    And the adapter should have a dispatcher injected
    And the dispatcher should have all handlers registered

  Scenario: Handlers receive repository dependencies
    When I call create_cli_application()
    Then GetProjectContextHandler should have repository injected
    And GetProjectContextHandler should have environment adapter injected

  Scenario: Composition root is the only place with infrastructure imports
    When I analyze the codebase imports
    Then src/bootstrap.py should import from src/infrastructure/
    And src/interface/cli/ should NOT import from src/infrastructure/
    And src/application/ should NOT import from src/infrastructure/
```

**Architecture Test** (`tests/architecture/test_composition_root.py`):

```python
"""
Architecture tests for composition root boundaries.

These tests enforce that:
1. Only bootstrap.py imports infrastructure
2. CLI adapter has no infrastructure dependencies
3. Application layer has no infrastructure dependencies
"""

def test_bootstrap_is_sole_infrastructure_importer():
    """Only src/bootstrap.py may import from src/infrastructure/."""

def test_cli_adapter_has_no_infrastructure_imports():
    """src/interface/cli/*.py must not import src/infrastructure/."""

def test_application_layer_has_no_infrastructure_imports():
    """src/application/**/*.py must not import src/infrastructure/."""

def test_domain_layer_has_no_external_imports():
    """src/domain/**/*.py must only import stdlib."""
```

**Sub-tasks**:

| ID | Task | Evidence | Status |
|----|------|----------|--------|
| 2.1.1.1 | Create `src/bootstrap.py` | File exists | [ ] |
| 2.1.1.2 | Import infrastructure adapters | Imports present | [ ] |
| 2.1.1.3 | Create repository instances | Instances created | [ ] |
| 2.1.1.4 | Create environment adapter instance | Instance created | [ ] |
| 2.1.1.5 | Create handlers with dependencies | Handlers instantiated | [ ] |
| 2.1.1.6 | Create dispatcher with handlers | Dispatcher configured | [ ] |
| 2.1.1.7 | Create `create_cli_application()` factory | Factory exists | [ ] |
| 2.1.1.8 | Architecture tests pass | pytest results | [ ] |
| 2.1.1.9 | Integration test: factory returns valid adapter | Test passes | [ ] |

---

## Phase 3: CLI Adapter Refactor

### 3.1 Refactor CLIAdapter to Class

#### Task 3.1.1: Convert to Class-Based Adapter

**File**: `src/interface/cli/main.py`

**BDD Feature** (`tests/features/cli/command_routing.feature`):

```gherkin
Feature: CLI Command Routing
  As the CLI adapter
  I want to route commands through the dispatcher
  So that business logic stays in handlers

  Background:
    Given a CLI adapter with injected dispatcher

  Scenario: Init command dispatches GetProjectContextQuery
    When I run "jerry init"
    Then GetProjectContextQuery should be dispatched
    And the handler result should be formatted and printed

  Scenario: Projects list command dispatches ScanProjectsQuery
    When I run "jerry projects list"
    Then ScanProjectsQuery should be dispatched

  Scenario: Projects validate command dispatches ValidateProjectQuery
    When I run "jerry projects validate PROJ-001"
    Then ValidateProjectQuery should be dispatched
    And the query should contain project_id "PROJ-001"
```

**Integration Tests** (`tests/integration/cli/test_cli_dispatcher_integration.py`):

```python
"""
Integration tests for CLI → Dispatcher → Handler chain.

These tests verify the full routing from CLI command to handler execution.
"""

def test_init_command_dispatches_get_project_context():
    """jerry init dispatches GetProjectContextQuery to handler."""

def test_handler_result_returned_to_cli():
    """Handler result is returned through dispatcher to CLI."""

def test_cli_does_not_call_infrastructure_directly():
    """CLI adapter only interacts with dispatcher, not infrastructure."""
```

**E2E Regression Tests** (`tests/e2e/cli/test_cli_commands_e2e.py`):

```python
"""
End-to-end tests ensuring existing CLI functionality still works.

CRITICAL: These tests prevent regression when refactoring.
"""

def test_jerry_init_displays_project_context():
    """jerry init shows project context (regression from TD-014)."""

def test_jerry_help_displays_usage():
    """jerry --help shows usage information."""

def test_jerry_version_displays_version():
    """jerry --version shows version number."""

def test_jerry_with_invalid_command_shows_error():
    """jerry invalid-cmd shows helpful error."""
```

**Edge Cases**:

| ID | Edge Case | Expected Behavior | Test |
|----|-----------|-------------------|------|
| EC-3.1.1-A | Dispatcher is None | Raise ConfigurationError at startup | `test_adapter_requires_dispatcher` |
| EC-3.1.1-B | Unknown command | argparse shows error and exits | `test_unknown_command_exits_with_error` |
| EC-3.1.1-C | Missing required argument | argparse shows error | `test_missing_arg_shows_error` |
| EC-3.1.1-D | Handler raises exception | CLI catches and displays error | `test_handler_exception_displayed` |

**Sub-tasks**:

| ID | Task | Evidence | Status |
|----|------|----------|--------|
| 3.1.1.1 | Create `CLIAdapter` class | Class exists | [ ] |
| 3.1.1.2 | Constructor receives `IQueryDispatcher` | DI via constructor | [ ] |
| 3.1.1.3 | Remove all infrastructure imports | `grep "from src.infrastructure" src/interface/cli/main.py` returns empty | [ ] |
| 3.1.1.4 | Implement `cmd_init` using dispatcher | Method dispatches query | [ ] |
| 3.1.1.5 | Implement `cmd_projects_list` using dispatcher | Method dispatches query | [ ] |
| 3.1.1.6 | Implement `cmd_projects_validate` using dispatcher | Method dispatches query | [ ] |
| 3.1.1.7 | Update entry point to use bootstrap | `main()` calls `create_cli_application()` | [ ] |
| 3.1.1.8 | E2E regression tests pass | All existing functionality works | [ ] |
| 3.1.1.9 | Architecture tests pass | No infrastructure imports | [ ] |
| 3.1.1.10 | Integration tests pass | Dispatcher routing verified | [ ] |

---

## Phase 4: CLI Namespaces

### 4.1 Create Namespace Structure

#### Task 4.1.1: Projects Namespace

**File**: `src/interface/cli/commands/projects.py`

**BDD Feature** (`tests/features/cli/namespace_isolation.feature`):

```gherkin
Feature: CLI Namespace Isolation
  As the CLI designer
  I want commands organized by bounded context
  So that security and authorization boundaries are clear

  Scenario: Projects namespace contains project commands
    When I run "jerry projects --help"
    Then I should see "list" as a subcommand
    And I should see "validate" as a subcommand
    And I should NOT see session or worktracker commands

  Scenario: Session namespace contains session commands
    When I run "jerry session --help"
    Then I should see session-specific commands
    And I should NOT see project or worktracker commands

  Scenario: Worktracker namespace contains worktracker commands
    When I run "jerry worktracker --help"
    Then I should see worktracker-specific commands
    And I should NOT see project or session commands

  Scenario: Unknown namespace shows error
    When I run "jerry unknown-namespace"
    Then the exit code should be non-zero
    And I should see an error message
```

**Sub-tasks**:

| ID | Task | Evidence | Status |
|----|------|----------|--------|
| 4.1.1.1 | Create `src/interface/cli/commands/__init__.py` | File exists | [ ] |
| 4.1.1.2 | Create `projects.py` with subcommands | File exists | [ ] |
| 4.1.1.3 | Register projects namespace in main | Namespace registered | [ ] |
| 4.1.1.4 | `jerry projects list` works | CLI output verified | [ ] |
| 4.1.1.5 | `jerry projects validate <id>` works | CLI output verified | [ ] |
| 4.1.1.6 | `jerry projects --help` shows commands | Help output verified | [ ] |

#### Task 4.1.2: Session Namespace (Scaffold)

**File**: `src/interface/cli/commands/session.py`

**Sub-tasks**:

| ID | Task | Evidence | Status |
|----|------|----------|--------|
| 4.1.2.1 | Create `session.py` scaffold | File exists | [ ] |
| 4.1.2.2 | Register session namespace | Namespace registered | [ ] |
| 4.1.2.3 | `jerry session --help` shows placeholder | Help output verified | [ ] |

#### Task 4.1.3: Worktracker Namespace (Scaffold)

**File**: `src/interface/cli/commands/worktracker.py`

**Sub-tasks**:

| ID | Task | Evidence | Status |
|----|------|----------|--------|
| 4.1.3.1 | Create `worktracker.py` scaffold | File exists | [ ] |
| 4.1.3.2 | Register worktracker namespace | Namespace registered | [ ] |
| 4.1.3.3 | `jerry worktracker --help` shows placeholder | Help output verified | [ ] |

---

## Phase 5: TOON Format Integration

### 5.1 Add TOON Dependency

#### Task 5.1.1: Add python-toon to Dependencies

**File**: `pyproject.toml`

**Sub-tasks**:

| ID | Task | Evidence | Status |
|----|------|----------|--------|
| 5.1.1.1 | Add `python-toon>=0.1.0` to dependencies | Entry in pyproject.toml | [ ] |
| 5.1.1.2 | Run `pip install -e .` | Installs without error | [ ] |
| 5.1.1.3 | Verify import works | `python -c "import toon"` succeeds | [ ] |

---

### 5.2 Create Formatters

#### Task 5.2.1: TOON Formatter

**File**: `src/interface/cli/formatters/toon_formatter.py`

**BDD Feature** (`tests/features/formatters/toon_output.feature`):

```gherkin
Feature: TOON Output Format
  As a CLI user
  I want output in TOON format by default
  So that token efficiency is maximized

  Scenario: Format project context as TOON
    Given a ProjectContext result
    When I format with ToonFormatter
    Then the output should be valid TOON
    And the output should be smaller than JSON equivalent

  Scenario: Format project list as TOON
    Given a list of 5 projects
    When I format with ToonFormatter
    Then the output should be valid TOON table
    And each project should be a row

  Scenario: Empty data produces valid TOON
    Given an empty project list
    When I format with ToonFormatter
    Then the output should be valid TOON
    And the output should indicate empty

  Scenario: Nested data falls back to hybrid format
    Given a deeply nested data structure
    When I format with ToonFormatter
    Then the nested part should use JSON-in-TOON
```

**Contract Tests** (`tests/contract/output_formats/test_toon_contract.py`):

```python
"""
Contract tests for TOON output format.

These tests validate that output conforms to TOON spec v3.0.
"""

def test_toon_output_parses_as_valid_toon():
    """All TOON output must parse without errors."""

def test_toon_header_row_present():
    """TOON tables must have header row."""

def test_toon_delimiter_is_tab():
    """TOON uses tab as field delimiter."""

def test_toon_escaping_correct():
    """Special characters are properly escaped."""

def test_toon_output_smaller_than_json():
    """TOON output is at least 20% smaller than JSON."""
```

**Edge Cases**:

| ID | Edge Case | Expected Behavior | Test |
|----|-----------|-------------------|------|
| EC-5.2.1-A | Data contains tab character | Tab is escaped | `test_tab_in_data_escaped` |
| EC-5.2.1-B | Data contains newline | Newline is escaped | `test_newline_in_data_escaped` |
| EC-5.2.1-C | Data is None | Output "null" or empty | `test_none_data_handled` |
| EC-5.2.1-D | Data is very large | No truncation, streams output | `test_large_data_not_truncated` |
| EC-5.2.1-E | Data is single scalar | Valid TOON scalar | `test_scalar_output_valid` |

**Sub-tasks**:

| ID | Task | Evidence | Status |
|----|------|----------|--------|
| 5.2.1.1 | Create `src/interface/cli/formatters/__init__.py` | File exists | [ ] |
| 5.2.1.2 | Create `toon_formatter.py` | File exists | [ ] |
| 5.2.1.3 | Define `ToonFormatter` class | Class exists | [ ] |
| 5.2.1.4 | Implement `format(data) -> str` | Method exists | [ ] |
| 5.2.1.5 | Unit tests pass | All pass | [ ] |
| 5.2.1.6 | Contract tests pass | All pass | [ ] |
| 5.2.1.7 | Edge case tests pass | All pass | [ ] |

---

#### Task 5.2.2: JSON Formatter

**File**: `src/interface/cli/formatters/json_formatter.py`

**Sub-tasks**:

| ID | Task | Evidence | Status |
|----|------|----------|--------|
| 5.2.2.1 | Create `json_formatter.py` | File exists | [ ] |
| 5.2.2.2 | Define `JsonFormatter` class | Class exists | [ ] |
| 5.2.2.3 | Implement `format(data) -> str` | Method exists | [ ] |
| 5.2.2.4 | Unit tests pass | All pass | [ ] |

---

#### Task 5.2.3: Human-Readable Formatter

**File**: `src/interface/cli/formatters/human_formatter.py`

**Sub-tasks**:

| ID | Task | Evidence | Status |
|----|------|----------|--------|
| 5.2.3.1 | Create `human_formatter.py` | File exists | [ ] |
| 5.2.3.2 | Define `HumanFormatter` class | Class exists | [ ] |
| 5.2.3.3 | Implement `format(data) -> str` | Method exists | [ ] |
| 5.2.3.4 | Unit tests pass | All pass | [ ] |

---

### 5.3 Integrate Format Flags

#### Task 5.3.1: Add Format Arguments to CLI

**File**: `src/interface/cli/main.py`

**System Tests** (`tests/system/cli/test_format_flags.py`):

```python
"""
System tests for CLI format flag behavior.
"""

def test_default_format_is_toon():
    """Without flags, output is TOON."""

def test_toon_flag_produces_toon():
    """--toon flag produces TOON output."""

def test_json_flag_produces_json():
    """--json flag produces JSON output."""

def test_human_flag_produces_human():
    """--human flag produces human-readable output."""

def test_conflicting_flags_shows_error():
    """--toon --json together shows error."""
```

**Sub-tasks**:

| ID | Task | Evidence | Status |
|----|------|----------|--------|
| 5.3.1.1 | Add `--toon` flag (default) | Flag in argparse | [ ] |
| 5.3.1.2 | Add `--json` flag | Flag in argparse | [ ] |
| 5.3.1.3 | Add `--human` flag | Flag in argparse | [ ] |
| 5.3.1.4 | Format selection logic | Correct formatter chosen | [ ] |
| 5.3.1.5 | System tests pass | All pass | [ ] |

---

## Cross-Cutting Concerns

### Architecture Tests

**File**: `tests/architecture/cli/test_cli_boundaries.py`

```python
"""
Architecture boundary tests for CLI adapter.

Uses pytest-archon for import analysis.
"""

def test_cli_does_not_import_infrastructure():
    """src/interface/cli/ must not import src/infrastructure/."""

def test_cli_does_not_import_domain_directly():
    """src/interface/cli/ should use application layer, not domain."""

def test_handlers_do_not_import_cli():
    """src/application/handlers/ must not import src/interface/."""

def test_dispatchers_do_not_import_infrastructure():
    """src/application/dispatchers/ must not import src/infrastructure/."""
```

---

## Acceptance Criteria Matrix

| ID | Criterion | Phase | Evidence Type | Status |
|----|-----------|-------|---------------|--------|
| AC-01 | CLI adapter receives dispatcher via constructor | 3 | Code inspection: `grep "__init__.*dispatcher" src/interface/cli/main.py` | [ ] |
| AC-02 | No infrastructure imports in CLI adapter | 3 | Architecture test: `test_cli_does_not_import_infrastructure` PASS | [ ] |
| AC-03 | All queries routed through dispatcher | 3 | Integration test: `test_init_command_dispatches_get_project_context` PASS | [ ] |
| AC-04 | Composition root external to adapters | 2 | File exists: `src/bootstrap.py` | [ ] |
| AC-05 | Handler tests with mocked dependencies | 1 | Unit tests pass for all handlers | [ ] |
| AC-06 | `jerry session` namespace exists | 4 | System test: `jerry session --help` returns 0 | [ ] |
| AC-07 | `jerry worktracker` namespace exists | 4 | System test: `jerry worktracker --help` returns 0 | [ ] |
| AC-08 | `jerry projects` namespace exists | 4 | System test: `jerry projects --help` returns 0 | [ ] |
| AC-09 | TOON is default output format | 5 | System test: `test_default_format_is_toon` PASS | [ ] |
| AC-10 | `--json` flag works | 5 | System test: `test_json_flag_produces_json` PASS | [ ] |
| AC-11 | `--human` flag works | 5 | System test: `test_human_flag_produces_human` PASS | [ ] |
| AC-12 | E2E regression tests pass | 3 | All E2E tests in `tests/e2e/cli/` PASS | [ ] |

---

## Evidence Registry

All evidence for completed tasks will be registered here with:

| Task ID | Evidence Type | Evidence Value | Timestamp |
|---------|---------------|----------------|-----------|
| (filled during implementation) | | | |

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-12 | Claude | Initial creation with full BDD scenarios |
