# Implementation Plan: TD-015 CLI Architecture Remediation

> **Status**: 🔴 REMEDIATION REQUIRED - Design Canon Violations Found
> **Priority**: CRITICAL
> **Source**: BUG-006, DISC-011, DISC-012, DISC-013
> **Created**: 2026-01-12
> **Revised**: 2026-01-12 (Post-implementation review)
> **Author**: Claude
> **Detailed Plan**: See `IMPL-TD-015-DETAILED.md` for BDD scenarios, edge cases, failure scenarios, and evidence criteria

---

## ⚠️ IMPLEMENTATION STATUS: REMEDIATION REQUIRED

### Process Violation

Implementation was started without presenting the plan for user approval. This violates the established process.

### Current State (Implemented But Non-Compliant)

| Phase | Files Created | Tests | Issue |
|-------|---------------|-------|-------|
| Phase 1 | `src/application/ports/dispatcher.py`, `src/application/dispatchers/query_dispatcher.py`, `src/application/handlers/*.py` | 44 | Wrong structure |
| Phase 2 | `src/bootstrap.py`, `tests/architecture/test_composition_root.py`, `tests/integration/test_bootstrap.py` | 13 | Tests pass, wrong structure |
| Phase 3 | `src/interface/cli/adapter.py`, `tests/integration/cli/test_cli_dispatcher_integration.py` | 6 | Tests pass, wrong structure |

### Design Canon Violations

| ID | Requirement (Per Design Canon) | Current Implementation | Citation |
|----|--------------------------------|------------------------|----------|
| V-001 | Separate file per port: `iquerydispatcher.py` | Combined in `dispatcher.py` | Teaching Edition L750 |
| V-002 | Queries in `application/queries/` | Embedded in handler files | Design Canon PAT-CQRS-002 |
| V-003 | Naming: `RetrieveProjectContextQuery` | `GetProjectContextQueryData` | User feedback |
| V-004 | Events in separate files | Not implemented | User feedback |
| V-005 | Projections in `application/projections/` | Not implemented | Teaching Edition L754 |
| V-006 | Read models in `infrastructure/read_models/` | Not implemented | Teaching Edition L765 |

### Remediation Required Before Proceeding

1. **Split ports into separate files** per design canon
2. **Move query data objects** to `application/queries/` directory
3. **Rename to follow conventions** (Retrieve vs Get)
4. **Update all tests** to reference new file structure
5. **Present revised plan for user approval** before Phase 4+

---

## Executive Summary

The current CLI implementation uses "Poor Man's DI" pattern where the adapter directly instantiates infrastructure adapters. This violates Clean Architecture principles and is NOT acceptable per user requirements. This plan details the remediation to implement proper Dispatcher pattern with external composition root.

---

## Current State (WRONG)

```
┌──────────────────────────────────────────────────────────────┐
│                         CLI ADAPTER                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ def cmd_init(args):                                    │ │
│  │     query = GetProjectContextQuery(                    │ │
│  │         repository=FilesystemProjectAdapter(),  # ❌   │ │
│  │         environment=OsEnvironmentAdapter(),     # ❌   │ │
│  │         base_path=get_projects_directory(),            │ │
│  │     )                                                  │ │
│  │     result = query.execute()  # Direct execution ❌    │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

**Violations:**
1. Adapter instantiates infrastructure adapters directly
2. Query objects execute themselves (no handler separation)
3. No dispatcher for routing
4. Composition root inside adapter

---

## Target State (CORRECT)

```
┌──────────────────────────────────────────────────────────────┐
│                    COMPOSITION ROOT                           │
│                    (src/bootstrap.py)                         │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ def create_application() -> CLIAdapter:                │ │
│  │     repository = FilesystemProjectAdapter()            │ │
│  │     environment = OsEnvironmentAdapter()               │ │
│  │     handlers = { Query: Handler(deps), ... }           │ │
│  │     dispatcher = QueryDispatcher(handlers)             │ │
│  │     return CLIAdapter(dispatcher)                      │ │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────────────────┬─────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────┐
│                         CLI ADAPTER                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ class CLIAdapter:                                      │ │
│  │     def __init__(self, dispatcher: IQueryDispatcher):  │ │
│  │         self._dispatcher = dispatcher                  │ │
│  │                                                        │ │
│  │     def cmd_init(self, args):                          │ │
│  │         query = GetProjectContextQuery(base_path)      │ │
│  │         result = self._dispatcher.dispatch(query) # ✅ │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

---

## Implementation Phases

### Phase 1: Application Layer Infrastructure

**Goal:** Create dispatcher pattern infrastructure in application layer.

| Task | File | Description |
|------|------|-------------|
| 1.1 | `src/application/ports/dispatcher.py` | Define `IQueryDispatcher`, `ICommandDispatcher` interfaces |
| 1.2 | `src/application/dispatchers/__init__.py` | Package init |
| 1.3 | `src/application/dispatchers/query_dispatcher.py` | `QueryDispatcher` implementation |
| 1.4 | `src/application/handlers/__init__.py` | Package init |
| 1.5 | `src/application/handlers/get_project_context_handler.py` | Handler for GetProjectContextQuery |
| 1.6 | `src/application/handlers/scan_projects_handler.py` | Handler for ScanProjectsQuery |
| 1.7 | `src/application/handlers/validate_project_handler.py` | Handler for ValidateProjectQuery |

**Acceptance Criteria:**
- [ ] `IQueryDispatcher` protocol defined with `dispatch(query: TQuery) -> TResult`
- [ ] `QueryDispatcher` routes queries to registered handlers
- [ ] Handlers accept dependencies via constructor
- [ ] Handlers call underlying query execution
- [ ] Unit tests for dispatcher routing
- [ ] Unit tests for each handler

### Phase 2: Composition Root

**Goal:** Create external composition root that wires all dependencies.

| Task | File | Description |
|------|------|-------------|
| 2.1 | `src/bootstrap.py` | Main composition root |
| 2.2 | - | Wire infrastructure adapters |
| 2.3 | - | Create handlers with dependencies |
| 2.4 | - | Register handlers with dispatcher |
| 2.5 | - | Factory function for CLI adapter |

**Acceptance Criteria:**
- [ ] `src/bootstrap.py` exists
- [ ] All infrastructure adapters instantiated here
- [ ] All handlers wired with dependencies here
- [ ] Dispatcher configured with handler registry
- [ ] `create_cli_application() -> CLIAdapter` exported
- [ ] CLI adapter receives dispatcher via injection
- [ ] No infrastructure imports in CLI adapter

### Phase 3: CLI Adapter Refactor

**Goal:** Refactor CLI adapter to receive dispatcher and route through it.

| Task | File | Description |
|------|------|-------------|
| 3.1 | `src/interface/cli/main.py` | Refactor to class-based adapter |
| 3.2 | - | Constructor receives `IQueryDispatcher` |
| 3.3 | - | Remove all infrastructure imports |
| 3.4 | - | Route commands through dispatcher |
| 3.5 | - | Update entry point to use bootstrap |

**Acceptance Criteria:**
- [ ] `CLIAdapter` class receives dispatcher in constructor
- [ ] No imports from `src/infrastructure/` in CLI adapter
- [ ] All commands dispatch through `self._dispatcher.dispatch(query)`
- [ ] Entry point calls `create_cli_application()` from bootstrap
- [ ] Architecture tests verify no infrastructure imports
- [ ] E2E tests still pass

### Phase 4: CLI Namespaces per Bounded Context

**Goal:** Restructure CLI to have separate namespaces per bounded context.

| Task | File | Description |
|------|------|-------------|
| 4.1 | `src/interface/cli/commands/projects.py` | Projects namespace (existing) |
| 4.2 | `src/interface/cli/commands/session.py` | Session Management namespace |
| 4.3 | `src/interface/cli/commands/worktracker.py` | Work Tracker namespace |
| 4.4 | `src/interface/cli/main.py` | Register all namespaces |

**Target CLI Structure:**
```
jerry
├── init                        # Root command
├── projects                    # Project Management BC
│   ├── list
│   └── validate <id>
├── session                     # Session Management BC (future)
│   └── (commands TBD)
└── worktracker                 # Work Tracker BC (future)
    └── (commands TBD)
```

**Acceptance Criteria:**
- [ ] `jerry projects <cmd>` namespace works
- [ ] `jerry session <cmd>` namespace scaffolded
- [ ] `jerry worktracker <cmd>` namespace scaffolded
- [ ] Each namespace routes to distinct application port
- [ ] CLI help shows all namespaces

### Phase 5: TOON Format Integration

**Goal:** Implement TOON as default output format per DISC-012.

| Task | File | Description |
|------|------|-------------|
| 5.1 | `pyproject.toml` | Add `python-toon` dependency |
| 5.2 | `src/interface/cli/formatters/__init__.py` | Package init |
| 5.3 | `src/interface/cli/formatters/toon_formatter.py` | TOON output formatter |
| 5.4 | `src/interface/cli/formatters/json_formatter.py` | JSON output formatter |
| 5.5 | `src/interface/cli/formatters/human_formatter.py` | Human-readable formatter |
| 5.6 | `src/interface/cli/main.py` | Add format flags |

**Output Format Priority:**
| Flag | Format | Priority |
|------|--------|----------|
| (default) | TOON | PRIMARY |
| `--toon` | TOON | Explicit |
| `--json` | JSON | SECONDARY |
| `--human` | Human | TERTIARY |

**Acceptance Criteria:**
- [ ] Default output is TOON format
- [ ] `--toon` flag produces TOON output
- [ ] `--json` flag produces JSON output
- [ ] `--human` flag produces human-readable output
- [ ] TOON output is valid per spec
- [ ] Contract tests for output formats

---

## Testing Strategy

### Unit Tests

| Test File | Scope |
|-----------|-------|
| `tests/application/dispatchers/test_query_dispatcher.py` | Dispatcher routing |
| `tests/application/handlers/test_*.py` | Handler logic |
| `tests/interface/cli/test_formatters.py` | Output formatting |

### Integration Tests

| Test File | Scope |
|-----------|-------|
| `tests/interface/cli/integration/test_cli_e2e.py` | End-to-end CLI |
| `tests/interface/cli/integration/test_dispatcher_integration.py` | CLI → Dispatcher → Handler |

### Architecture Tests

| Test File | Scope |
|-----------|-------|
| `tests/architecture/test_cli_boundaries.py` | No infrastructure imports in CLI |
| `tests/architecture/test_composition_root.py` | Bootstrap owns all wiring |

---

## Acceptance Criteria Summary

| ID | Criterion | Evidence | Status |
|----|-----------|----------|--------|
| AC-01 | CLI adapter receives dispatcher via constructor | Code inspection | [ ] |
| AC-02 | No infrastructure imports in CLI adapter | Architecture test | [ ] |
| AC-03 | All queries routed through dispatcher | Code inspection | [ ] |
| AC-04 | Composition root external to all adapters | `src/bootstrap.py` exists | [ ] |
| AC-05 | Handler tests with mocked dependencies | pytest results | [ ] |
| AC-06 | `jerry session` namespace exists | CLI help output | [ ] |
| AC-07 | `jerry worktracker` namespace exists | CLI help output | [ ] |
| AC-08 | `jerry projects` namespace exists | CLI help output | [ ] |
| AC-09 | TOON is default output format | CLI default output | [ ] |
| AC-10 | `--json` flag works | CLI output | [ ] |
| AC-11 | `--human` flag works | CLI output | [ ] |
| AC-12 | All existing E2E tests pass | pytest results | [ ] |

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Breaking existing CLI functionality | E2E tests must pass at each phase |
| Over-engineering | Follow minimal implementation, no premature abstraction |
| Test coverage gaps | Architecture tests enforce boundaries |
| TOON library issues | `python-toon` is mature; fallback to custom if needed |

---

## Definition of Done

1. All acceptance criteria met
2. All tests pass (unit, integration, architecture, E2E)
3. No infrastructure imports in CLI adapter
4. Composition root is sole owner of dependency wiring
5. TOON is default output format
6. CLI namespaces per bounded context scaffolded
7. BUG-006 can be marked RESOLVED
8. Documentation updated

---

## References

| Document | Path |
|----------|------|
| Architecture Standards | `docs/design/PYTHON-ARCHITECTURE-STANDARDS.md` |
| ADR-CLI-001 (Amended) | `projects/PROJ-001-plugin-cleanup/decisions/ADR-CLI-001-primary-adapter.md` |
| TOON Research | `projects/archive/research/TOON_FORMAT_ANALYSIS.md` |
| TOON Implementation | `projects/PROJ-001-plugin-cleanup/research/impl-es-e-002-toon-serialization.md` |
| BUG-006 | `projects/PROJ-001-plugin-cleanup/work/PHASE-BUGS.md` |
| TD-015 | `projects/PROJ-001-plugin-cleanup/work/PHASE-TECHDEBT.md` |
| Teaching Edition | `docs/knowledge/exemplars/architecture/work_tracker_architecture_hexagonal_ddd_cqrs_layered_teaching_edition.md` |

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-12 | Claude | Initial creation |
