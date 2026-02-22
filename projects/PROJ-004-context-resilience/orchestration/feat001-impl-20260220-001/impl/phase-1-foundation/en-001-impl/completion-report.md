# EN-001 Implementation Completion Report

> EventSourcedSessionRepository -- Event-sourced session persistence via FileSystemEventStore.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What was implemented |
| [Files Changed](#files-changed) | All created and modified files |
| [Design Decisions](#design-decisions) | Key architectural choices |
| [Test Coverage](#test-coverage) | BDD scenarios and test results |
| [Issues Resolved](#issues-resolved) | Problems encountered and solutions |
| [Pre-Existing Failures](#pre-existing-failures) | Known failures not caused by EN-001 |
| [Compliance](#compliance) | Rule verification |

---

## Summary

Implemented `EventSourcedSessionRepository` as a file-backed, event-sourced implementation of `ISessionRepository`. Session aggregates are now persisted as event streams via `FileSystemEventStore`, enabling cross-process persistence. Sessions survive process termination and can be reconstituted from event history.

The implementation follows the established `EventSourcedWorkItemRepository` pattern from TD-018, ensuring consistency across the codebase.

**Entity:** EN-001 (FileSystemSessionRepository)
**Status:** DONE
**Date:** 2026-02-20

---

## Files Changed

### Created (4 files)

| File | Purpose |
|------|---------|
| `src/session_management/infrastructure/adapters/event_sourced_session_repository.py` | Event-sourced session repository implementation |
| `tests/unit/session_management/infrastructure/test_event_sourced_session_repository.py` | 18 BDD tests for the repository |
| `tests/unit/session_management/__init__.py` | Package init (empty) |
| `tests/unit/session_management/infrastructure/__init__.py` | Package init (empty) |

### Modified (7 files)

| File | Change |
|------|--------|
| `src/session_management/domain/events/session_events.py` | Added `_payload()` and `from_dict()` to all 4 session events for EventRegistry serialization |
| `src/session_management/application/ports/session_repository.py` | Changed `save()` return type to `list[DomainEvent]` |
| `src/session_management/infrastructure/adapters/in_memory_session_repository.py` | Updated `save()` to collect and return events |
| `src/session_management/application/handlers/commands/create_session_command_handler.py` | Changed to `return self._repository.save(session)` |
| `src/session_management/application/handlers/commands/end_session_command_handler.py` | Changed to `return self._repository.save(session)` |
| `src/session_management/application/handlers/commands/abandon_session_command_handler.py` | Changed to `return self._repository.save(session)` |
| `src/bootstrap.py` | Wired `EventSourcedSessionRepository` as default session repository |

### Test Fixes (3 files)

| File | Change |
|------|--------|
| `tests/integration/cli/test_jerry_cli_subprocess.py` | Added `env.pop("JERRY_PROJECT", None)` to prevent persistent session leakage |
| `tests/integration/test_event_sourcing_wiring.py` | Added `monkeypatch.delenv("JERRY_PROJECT")` for same reason |
| `tests/session_management/unit/application/test_session_handlers.py` | Updated mock fixture to return events from `save()` |

---

## Design Decisions

### 1. Repository save() returns list[DomainEvent]

The `ISessionRepository.save()` protocol was updated from returning `None` to returning `list[DomainEvent]`. This aligns with the existing `IWorkItemRepository.save()` pattern and resolves the "events drained by save()" issue where `EventSourcedSessionRepository.save()` internally calls `collect_events()`, draining the aggregate's pending events before handlers could return them.

### 2. Event stream convention

Session event streams use the prefix `session-{session_id}`, consistent with the `workitem-{work_item_id}` convention used by `EventSourcedWorkItemRepository`.

### 3. get_active() scans all session streams

The `get_active()` method scans all streams with the `session-` prefix, reconstituting each session to check its status. This is acceptable for the current scale (few concurrent sessions) but could be optimized with an index if needed.

### 4. IEventStoreWithUtilities protocol

A local protocol extends `IEventStore` with `get_all_stream_ids()` to support `get_active()`. Both `FileSystemEventStore` and `InMemoryEventStore` already implement this method.

### 5. Session events enhanced with _payload() and from_dict()

All 4 session events (`SessionCreated`, `SessionCompleted`, `SessionAbandoned`, `SessionProjectLinked`) were enhanced with `_payload()` and `from_dict()` methods required by `EventRegistry` for serialization/deserialization through the event store.

---

## Test Coverage

### BDD Scenarios (18 tests, all PASS)

| Scenario | Tests |
|----------|-------|
| Save and retrieve a session | 3 tests (round-trip, description, nonexistent) |
| Cross-process persistence | 2 tests (new repo instance, new event store instance) |
| Get active session | 5 tests (active, exclude completed, exclude abandoned, no active, empty repo) |
| Abandon session with reason | 2 tests (status+reason, event in stream) |
| Optimistic concurrency | 1 test (concurrent saves conflict) |
| Event replay reconstitution | 2 tests (full lifecycle, version preservation) |
| Exists method | 2 tests (saved, unsaved) |
| Save idempotency | 1 test (no pending events is no-op) |

### Full Test Suite

```
3358 passed, 60 skipped, 29 deselected in 93.87s
```

The 29 deselected tests include 2 pre-existing failures and their parameterized variants.

---

## Issues Resolved

### 1. Events drained by save()

**Problem:** `EventSourcedSessionRepository.save()` calls `session.collect_events()` which drains pending events. When handlers subsequently called `session.collect_events()` again, they received empty lists.

**Solution:** Updated `ISessionRepository.save()` to return `list[DomainEvent]` (matching `IWorkItemRepository`), and updated all 3 command handlers to `return self._repository.save(session)`.

### 2. Persistent session state leaking into tests

**Problem:** With `EventSourcedSessionRepository` backed by `FileSystemEventStore`, previously persisted active sessions were found during integration tests, causing `SessionAlreadyActiveError`.

**Solution:** Added `env.pop("JERRY_PROJECT", None)` in subprocess tests and `monkeypatch.delenv("JERRY_PROJECT", raising=False)` in dispatcher integration tests, ensuring tests fall back to `InMemoryEventStore`.

### 3. Mock fixture not returning events from save()

**Problem:** The mock repository's `save()` returned a `Mock` object instead of a list, causing `TypeError: object of type 'Mock' has no len()`.

**Solution:** Configured the mock fixture with `mock.save.side_effect = lambda session: list(session.collect_events())`.

---

## Pre-Existing Failures

Two test failures exist that are NOT caused by EN-001 changes:

1. `test_path_conventions.py::TestProjectIsolation::test_no_cross_project_references[PROJ-004-context-resilience]` -- cross-project reference in ORCHESTRATION_PLAN.md
2. `test_resumption_schema.py::TestTemplateContainsAll7SubSections::test_template_file_contains_all_sub_sections` -- missing `recovery_state` sub-section

---

## Compliance

| Rule | Status | Notes |
|------|--------|-------|
| H-05/H-06 | PASS | All execution via `uv run` |
| H-07 | PASS | Domain layer has no external imports |
| H-08 | PASS | Application layer has no infra imports |
| H-09 | PASS | Only `bootstrap.py` wires dependencies |
| H-10 | PASS | One class per file |
| H-11 | PASS | All public methods have type hints |
| H-12 | PASS | All public methods have docstrings |
| H-15 | PASS | Self-review completed |
| H-20 | PASS | BDD tests written before implementation |
