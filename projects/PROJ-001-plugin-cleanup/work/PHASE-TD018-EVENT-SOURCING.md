# Phase TD-018: Event Sourcing for WorkItem Repository

**Status**: ✅ COMPLETE
**Started**: 2026-01-12
**Completed**: 2026-01-12
**Priority**: HIGH
**Branch**: cc/clean-up-jerry

---

## Overview

Implement end-to-end event sourcing for WorkItem aggregates with **persistent storage**. This addresses:

1. **DISC-019**: `InMemoryEventStore` loses all events on process restart
2. **DISC-018**: `CommandDispatcher` not implemented (dict-based workaround)
3. **Design Canon**: WorkItem should be event-sourced per PAT-REPO-002

### Design Decision

**FileSystemEventStore** (Option A) chosen over SQLite because:
- Aligns with Jerry's "filesystem as infinite memory" philosophy
- Human-readable JSON Lines format
- Git-friendly (text diffs)
- Simple implementation, no external dependencies

SQLite deferred to TD-019 for future high-volume scenarios.

---

## Navigation

| Link | Description |
|------|-------------|
| [<- WORKTRACKER](../WORKTRACKER.md) | Back to index |
| [PHASE-04-CLI-NAMESPACES](PHASE-04-CLI-NAMESPACES.md) | Previous phase (complete) |
| [PHASE-TECHDEBT](PHASE-TECHDEBT.md) | TD-018 and TD-019 definitions |
| [PHASE-DISCOVERY](PHASE-DISCOVERY.md) | DISC-018, DISC-019 |

---

## Implementation Tasks

### Phase 1: FileSystemEventStore (DISC-019 Resolution) ✅ COMPLETE

| Task | Description | Status | Evidence |
|------|-------------|--------|----------|
| 1.1 | Create FileSystemEventStore | ✅ COMPLETE | `src/work_tracking/infrastructure/persistence/filesystem_event_store.py` (340 lines) |
| 1.1.1 | Implement `IEventStore` protocol | ✅ COMPLETE | 5 methods: append, read, get_version, stream_exists, delete_stream |
| 1.1.2 | Use JSON Lines format (one event per line) | ✅ COMPLETE | JSON Lines with `json.dumps()` per line |
| 1.1.3 | Store in `projects/PROJ-XXX/.jerry/data/events/` | ✅ COMPLETE | `{base_path}/.jerry/data/events/{stream_id}.jsonl` |
| 1.1.4 | Thread-safe file operations with locking | ✅ COMPLETE | `threading.RLock` + `fcntl.flock` (POSIX) |
| 1.1.5 | Implement optimistic concurrency via version checking | ✅ COMPLETE | `ConcurrencyError` on version mismatch |
| 1.2 | Unit tests for FileSystemEventStore | ✅ COMPLETE | `tests/work_tracking/unit/infrastructure/persistence/test_filesystem_event_store.py` (47 tests) |
| 1.2.1 | Test append/read round-trip | ✅ COMPLETE | 8 tests: TestAppend + TestRead classes |
| 1.2.2 | Test concurrency error on version mismatch | ✅ COMPLETE | 5 tests: TestThreadSafety, TestAppend concurrency |
| 1.2.3 | Test stream isolation | ✅ COMPLETE | 3 tests: TestIsolation class |
| 1.2.4 | Test persistence across "restarts" | ✅ COMPLETE | 5 tests: TestPersistence class |

### Phase 2: EventSourcedWorkItemRepository ✅ COMPLETE

| Task | Description | Status | Evidence |
|------|-------------|--------|----------|
| 2.1 | Create EventSourcedWorkItemRepository | ✅ COMPLETE | `src/work_tracking/infrastructure/adapters/event_sourced_work_item_repository.py` |
| 2.1.1 | Implement `IWorkItemRepository` protocol | ✅ COMPLETE | 7 methods: get, get_or_raise, save, delete, exists, list_all, count |
| 2.1.2 | Use `IEventStore` for persistence (injected) | ✅ COMPLETE | Constructor injection with IEventStoreWithUtilities |
| 2.1.3 | Implement `get()` via `WorkItem.load_from_history()` | ✅ COMPLETE | Event replay with EventRegistry |
| 2.1.4 | Implement `save()` via `work_item.collect_events()` | ✅ COMPLETE | DomainEvent → StoredEvent conversion |
| 2.1.5 | Handle version for optimistic concurrency | ✅ COMPLETE | expected_version calculated from first pending event |
| 2.2 | Unit tests for EventSourcedWorkItemRepository | ✅ COMPLETE | 29 tests in `tests/work_tracking/unit/infrastructure/adapters/test_event_sourced_work_item_repository.py` |
| 2.2.1 | Test save and retrieve round-trip | ✅ COMPLETE | TestEventSourcedRepositorySaveAndGet (5 tests) |
| 2.2.2 | Test WorkItem reconstitution from events | ✅ COMPLETE | TestEventSourcedRepositoryReconstitution (3 tests) |
| 2.2.3 | Test filesystem persistence | ✅ COMPLETE | TestEventSourcedRepositoryWithFileSystem (2 tests) |
| 2.2.4 | Test get_or_raise, exists, delete | ✅ COMPLETE | Multiple test classes covering all methods

### Phase 3: CommandDispatcher (DISC-018 Resolution) ✅ COMPLETE

| Task | Description | Status | Evidence |
|------|-------------|--------|----------|
| 3.1 | Create CommandDispatcher | ✅ COMPLETE | `src/application/dispatchers/command_dispatcher.py` (125 lines) |
| 3.1.1 | Implement `ICommandDispatcher` protocol | ✅ COMPLETE | Protocol impl with dispatch() method |
| 3.1.2 | Type-safe handler registration | ✅ COMPLETE | `register()` method with method chaining |
| 3.1.3 | Dispatch with `CommandHandlerNotFoundError` | ✅ COMPLETE | `dispatch()` method with exact type matching |
| 3.1.4 | Add `CommandHandlerNotFoundError` exception | ✅ COMPLETE | `src/application/ports/primary/icommanddispatcher.py` |
| 3.2 | Unit tests for CommandDispatcher | ✅ COMPLETE | `tests/unit/application/dispatchers/test_command_dispatcher.py` (16 tests) |
| 3.2.1 | Test handler registration | ✅ COMPLETE | 7 happy path tests |
| 3.2.2 | Test dispatch routing | ✅ COMPLETE | test_dispatch_routes_to_handler, test_dispatch_returns_handler_events |
| 3.2.3 | Test error on missing handler | ✅ COMPLETE | test_dispatch_unregistered_command_raises |
| 3.2.4 | Test edge cases | ✅ COMPLETE | 6 edge case tests (None, subclass, has_handler, registered_types) |

### Phase 4: Composition Root Wiring ✅ COMPLETE

| Task | Description | Status | Evidence |
|------|-------------|--------|----------|
| 4.1 | Update bootstrap.py | ✅ COMPLETE | Added factories for all new components |
| 4.1.1 | Instantiate FileSystemEventStore with project path | ✅ COMPLETE | `create_event_store()` factory method |
| 4.1.2 | Replace InMemoryWorkItemRepository with EventSourced | ✅ COMPLETE | `create_work_item_repository()` + `get_work_item_repository()` |
| 4.1.3 | Create CommandDispatcher and register handlers | ✅ COMPLETE | `create_command_dispatcher()` with 3 session handlers |
| 4.1.4 | Add reset_singletons for testing | ✅ COMPLETE | `reset_singletons()` function |
| 4.2 | Integration tests | ✅ COMPLETE | 12 tests in `tests/integration/test_event_sourcing_wiring.py` |
| 4.2.1 | Test Factory functions | ✅ COMPLETE | TestBootstrapFactories (6 tests) |
| 4.2.2 | Test event persistence survives "restart" | ✅ COMPLETE | TestEventSourcingPersistence (3 tests) |
| 4.2.3 | Test CommandDispatcher integration | ✅ COMPLETE | TestCommandDispatcherIntegration (3 tests) |

### Phase 5: Snapshot Support (Optional, Deferred)

| Task | Description | Status | Evidence |
|------|-------------|--------|----------|
| 5.1 | Create SnapshottingWorkItemRepository decorator | ⏳ DEFERRED | Future |
| 5.2 | Configure snapshot frequency (every 10 events) | ⏳ DEFERRED | Future |
| 5.3 | Integration with FileSystemSnapshotStore | ⏳ DEFERRED | Future |

---

## Files to Create/Modify

| File | Action | Description | Status |
|------|--------|-------------|--------|
| `src/work_tracking/infrastructure/persistence/filesystem_event_store.py` | **CREATE** | Persistent event store | ✅ COMPLETE |
| `src/work_tracking/infrastructure/adapters/event_sourced_work_item_repository.py` | **CREATE** | Event-sourced repository | ✅ COMPLETE |
| `src/application/dispatchers/command_dispatcher.py` | **CREATE** | CommandDispatcher | ✅ COMPLETE |
| `src/application/ports/primary/icommanddispatcher.py` | **MODIFY** | Added CommandHandlerNotFoundError | ✅ COMPLETE |
| `src/bootstrap.py` | **MODIFY** | Wire all new components | ⏳ PENDING |
| `tests/work_tracking/unit/infrastructure/persistence/test_filesystem_event_store.py` | **CREATE** | FileSystemEventStore tests | ✅ COMPLETE |
| `tests/work_tracking/unit/infrastructure/adapters/test_event_sourced_work_item_repository.py` | **CREATE** | Repository tests | ✅ COMPLETE |
| `tests/unit/application/dispatchers/test_command_dispatcher.py` | **CREATE** | CommandDispatcher tests | ✅ COMPLETE |

---

## FileSystemEventStore Design

### Storage Path

```
projects/PROJ-001/.jerry/data/events/
├── work_item-WORK-001.jsonl    # Append-only event log
├── work_item-WORK-002.jsonl    # One JSON event per line
└── ...
```

### JSON Lines Format

Each line is a `StoredEvent` serialized as JSON:

```json
{"event_id":"EVT-123","event_type":"WorkItemCreated","aggregate_id":"WORK-001","aggregate_type":"WorkItem","version":1,"payload":{"title":"Implement login"},"timestamp":"2026-01-12T12:00:00Z"}
{"event_id":"EVT-124","event_type":"StatusChanged","aggregate_id":"WORK-001","aggregate_type":"WorkItem","version":2,"payload":{"old_status":"pending","new_status":"in_progress"},"timestamp":"2026-01-12T12:01:00Z"}
```

### Thread Safety

- Use `threading.RLock()` for file operations
- File locking with `fcntl.flock()` (POSIX) for cross-process safety

---

## Acceptance Criteria

| ID | Criterion | Evidence | Status |
|----|-----------|----------|--------|
| AC-01 | FileSystemEventStore implements IEventStore | Code inspection + protocol compliance tests | ✅ |
| AC-02 | Events persisted to disk as JSON Lines | test_jsonl_format_human_readable | ✅ |
| AC-03 | Events survive process restart | TestPersistence class (5 tests) | ✅ |
| AC-04 | EventSourcedWorkItemRepository implements IWorkItemRepository | 7 methods implemented, protocol assertion | ✅ |
| AC-05 | WorkItems saved as event streams | test_save_and_get_work_item + event store files | ✅ |
| AC-06 | WorkItems loaded via history replay | TestReconstitution class (3 tests) | ✅ |
| AC-07 | Optimistic concurrency enforced | expected_version in save() | ✅ |
| AC-08 | CommandDispatcher implements ICommandDispatcher | Protocol compliance test + 16 tests | ✅ |
| AC-09 | InMemoryEventStore/WorkItemRepository remain for unit testing | Backward compatibility | ✅ |
| AC-10 | All existing tests pass | 1586 passed, 3 skipped | ✅ |

---

## Test Summary

| Phase | Unit | Integration | Total | Status |
|-------|------|-------------|-------|--------|
| 1 FileSystemEventStore | 47 | - | 47 | ✅ COMPLETE |
| 2 EventSourcedRepository | 29 | - | 29 | ✅ COMPLETE |
| 3 CommandDispatcher | 16 | - | 16 | ✅ COMPLETE |
| 4 Wiring | - | 12 | 12 | ✅ COMPLETE |
| **Total** | **92** | **12** | **104** | ✅ |

---

## Progress Tracking

| Date | Activity | Status |
|------|----------|--------|
| 2026-01-12 | DISC-019 logged: InMemoryEventStore not persistent | ✅ |
| 2026-01-12 | TD-018 revised with FileSystemEventStore scope | ✅ |
| 2026-01-12 | TD-019 created for SQLite (future) | ✅ |
| 2026-01-12 | PHASE-TD018-EVENT-SOURCING.md worktracker created | ✅ |
| 2026-01-12 | Task 1.1: FileSystemEventStore created (340 lines) | ✅ |
| 2026-01-12 | Task 1.2: Unit tests for FileSystemEventStore (47 tests) | ✅ |
| 2026-01-12 | **Phase 1 COMPLETE** | ✅ |
| 2026-01-12 | Task 2.1: EventSourcedWorkItemRepository created | ✅ |
| 2026-01-12 | Task 2.2: Unit tests for EventSourcedWorkItemRepository (29 tests) | ✅ |
| 2026-01-12 | **Phase 2 COMPLETE** | ✅ |
| 2026-01-12 | Task 3.1: CommandDispatcher created (125 lines) | ✅ |
| 2026-01-12 | Task 3.1.4: CommandHandlerNotFoundError added | ✅ |
| 2026-01-12 | Task 3.2: Unit tests for CommandDispatcher (16 tests) | ✅ |
| 2026-01-12 | **Phase 3 COMPLETE** (DISC-018 resolved) | ✅ |
| 2026-01-12 | Task 4.1: bootstrap.py updated with new factories | ✅ |
| 2026-01-12 | Task 4.2: Integration tests (12 tests) | ✅ |
| 2026-01-12 | **Phase 4 COMPLETE** | ✅ |
| 2026-01-12 | **TD-018 COMPLETE** - All 104 tests passing | ✅ |

---

## Discoveries

| ID | Discovery | Impact | Action |
|----|-----------|--------|--------|
| DISC-018 | CommandDispatcher not implemented | MEDIUM | Include in Phase 3 |
| DISC-019 | InMemoryEventStore not persistent | HIGH | FileSystemEventStore in Phase 1 |

---

## References

| Document | Path | Relevance |
|----------|------|-----------|
| TD-018 Definition | `work/PHASE-TECHDEBT.md` | Full spec |
| TD-019 Definition | `work/PHASE-TECHDEBT.md` | Future SQLite |
| IEventStore Protocol | `src/work_tracking/domain/ports/event_store.py` | Port definition |
| InMemoryEventStore | `src/work_tracking/infrastructure/persistence/in_memory_event_store.py` | Reference impl |
| WorkItem Aggregate | `src/work_tracking/domain/aggregates/work_item.py` | Has `load_from_history()` |
| Event-Sourced Repository | `.claude/patterns/repository/event-sourced-repository.md` | Pattern guide |
