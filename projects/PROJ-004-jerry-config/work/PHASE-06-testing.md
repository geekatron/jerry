# PHASE-06: Testing & Validation

| Field | Value |
|-------|-------|
| **Phase ID** | PHASE-06 |
| **Title** | Testing & Validation |
| **Status** | PENDING |
| **Parallelizable** | Yes (tests can run in parallel) |
| **Work Items** | WI-017, WI-018 |
| **Assignee** | WT-Test |
| **Started** | - |
| **Completed** | - |

---

## Objective

Implement comprehensive tests for the configuration system: architecture tests validating hexagonal boundaries, integration tests for concurrent access and atomic writes, E2E tests for CLI commands, and contract tests for hook output format.

---

## Work Items

| ID | Title | Status | File |
|----|-------|--------|------|
| WI-017 | Architecture Tests | PENDING | [wi-017-arch-tests.md](wi-017-arch-tests.md) |
| WI-018 | Integration & E2E Tests | PENDING | [wi-018-integration-tests.md](wi-018-integration-tests.md) |

---

## Blockers

| Blocker | Status | Resolution |
|---------|--------|------------|
| WI-015, WI-016 (CLI Integration) | PENDING | Must complete PHASE-05 |

---

## Parallelization Strategy

### Worktree Assignment

| Branch | Work Items | Files Modified |
|--------|------------|----------------|
| `PROJ-004-config-tests` | WI-017, WI-018 | `tests/**` |

---

## Test Pyramid

```
                    ┌─────────────┐
                    │    E2E      │ ← CLI workflows (5%)
                   ┌┴─────────────┴┐
                   │   Contract    │ ← Hook output (5%)
                  ┌┴───────────────┴┐
                  │   Integration   │ ← Concurrent access (15%)
                 ┌┴─────────────────┴┐
                 │       Unit        │ ← Domain logic (60%)
                ┌┴───────────────────┴┐
                │    Architecture     │ ← Layer boundaries (15%)
                └─────────────────────┘
```

---

## Deliverables

### Architecture Tests (WI-017)

```
tests/architecture/
└── test_config_boundaries.py
    ├── test_domain_has_no_infrastructure_imports()
    ├── test_domain_has_no_application_imports()
    ├── test_adapters_implement_port_interfaces()
    └── test_composition_root_is_sole_importer()
```

### Integration Tests (WI-018)

```
tests/integration/
├── test_atomic_file_adapter.py
│   ├── test_concurrent_writes_dont_corrupt()
│   ├── test_read_with_lock_blocks_writes()
│   └── test_write_atomic_survives_crash()
└── test_layered_config.py
    ├── test_env_overrides_project_config()
    ├── test_project_overrides_root_config()
    └── test_missing_files_return_defaults()
```

### E2E Tests (WI-018)

```
tests/e2e/
└── test_config_cli.py
    ├── test_config_show_outputs_table()
    ├── test_config_show_json_is_valid()
    ├── test_config_get_returns_value()
    └── test_config_set_writes_to_file()
```

### Contract Tests (WI-018)

```
tests/contract/
└── test_session_hook.py
    ├── test_hook_outputs_project_context_tag()
    ├── test_hook_outputs_project_required_tag()
    └── test_hook_outputs_project_error_tag()
```

---

## Coverage Requirements

| Module | Target Coverage |
|--------|-----------------|
| `src/domain/value_objects/config_*.py` | 95%+ |
| `src/domain/aggregates/configuration.py` | 95%+ |
| `src/infrastructure/adapters/configuration/*.py` | 90%+ |
| `src/interface/cli/commands/config_commands.py` | 85%+ |
| **Overall configuration module** | **90%+** |

---

## Success Criteria

1. All architecture tests pass (layer boundaries enforced)
2. Concurrent access tests demonstrate no data corruption
3. Atomic write tests demonstrate crash safety
4. CLI E2E tests verify all commands work
5. Contract tests verify hook output format unchanged
6. Overall coverage ≥ 90%
7. All tests pass in CI pipeline

---

## Phase Summary

This final phase ensures the configuration system is robust, well-tested, and maintains the hexagonal architecture constraints. Tests are designed to catch regressions and validate the system under concurrent and failure conditions.

---

## Navigation

- **Previous Phase**: [PHASE-05: Integration & CLI](PHASE-05-integration.md)
- **Next Phase**: N/A (Final phase)
- **WORKTRACKER**: [../WORKTRACKER.md](../WORKTRACKER.md)
