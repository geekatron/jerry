# Phase 4.5: Items Commands

**Status**: ⏳ IN_PROGRESS
**Started**: 2026-01-12
**Priority**: HIGH
**Branch**: cc/clean-up-jerry
**Prerequisite**: TD-018 Event Sourcing ✅ COMPLETE

---

## Overview

Implement CLI commands for work item mutations. This phase was deferred until TD-018 (Event Sourcing) was complete to ensure mission-critical reliability.

**Commands to Implement:**
- `jerry items create <title>` - Create a new work item
- `jerry items start <id>` - Start work on an item
- `jerry items complete <id>` - Complete a work item
- `jerry items block <id> <reason>` - Block a work item
- `jerry items cancel <id> [reason]` - Cancel a work item

**Prerequisite Discoveries:**
- DISC-015: Phase 4.5 Requires Event Sourcing for Mission-Critical Reliability
- TD-018: Event Sourcing complete with 104 tests

---

## Navigation

| Link | Description |
|------|-------------|
| [<- WORKTRACKER](../WORKTRACKER.md) | Back to index |
| [PHASE-TD018-EVENT-SOURCING](PHASE-TD018-EVENT-SOURCING.md) | Prerequisite (complete) |
| [PHASE-04-CLI-NAMESPACES](PHASE-04-CLI-NAMESPACES.md) | Previous phase (complete) |
| [ADR-CLI-002](../decisions/ADR-CLI-002-namespace-implementation.md) | CLI design decision |

---

## Implementation Tasks

### Task 4.5.1: Create Work Item Command Definitions ✅ COMPLETE

| Subtask | Description | Status | Evidence |
|---------|-------------|--------|----------|
| 4.5.1.1 | Create `commands/` directory structure | ✅ DONE | `src/work_tracking/application/commands/` |
| 4.5.1.2 | CreateWorkItemCommand | ✅ DONE | `create_work_item_command.py` |
| 4.5.1.3 | StartWorkItemCommand | ✅ DONE | `start_work_item_command.py` |
| 4.5.1.4 | CompleteWorkItemCommand | ✅ DONE | `complete_work_item_command.py` |
| 4.5.1.5 | BlockWorkItemCommand | ✅ DONE | `block_work_item_command.py` |
| 4.5.1.6 | CancelWorkItemCommand | ✅ DONE | `cancel_work_item_command.py` |
| 4.5.1.7 | Commands `__init__.py` with exports | ✅ DONE | Package initialization |

### Task 4.5.2: Create Work Item Command Handlers ✅ COMPLETE

| Subtask | Description | Status | Evidence |
|---------|-------------|--------|----------|
| 4.5.2.1 | Create `handlers/commands/` directory | ✅ DONE | `src/work_tracking/application/handlers/commands/` |
| 4.5.2.2 | CreateWorkItemCommandHandler | ✅ DONE | Uses WorkItem.create() + IWorkItemIdGenerator |
| 4.5.2.3 | StartWorkItemCommandHandler | ✅ DONE | Uses work_item.start_work() |
| 4.5.2.4 | CompleteWorkItemCommandHandler | ✅ DONE | Uses work_item.complete() |
| 4.5.2.5 | BlockWorkItemCommandHandler | ✅ DONE | Uses work_item.block() |
| 4.5.2.6 | CancelWorkItemCommandHandler | ✅ DONE | Uses work_item.cancel() |
| 4.5.2.7 | Handlers `__init__.py` with exports | ✅ DONE | Package + parent __init__.py updated |

### Task 4.5.3: Wire to CommandDispatcher ✅ COMPLETE

| Subtask | Description | Status | Evidence |
|---------|-------------|--------|----------|
| 4.5.3.1 | Import commands in bootstrap.py | ✅ DONE | Commands + handlers + IdGenerator imported |
| 4.5.3.2 | Create command handlers with repository | ✅ DONE | Constructor injection + get_id_generator() singleton |
| 4.5.3.3 | Register handlers in create_command_dispatcher() | ✅ DONE | 5 work item + 3 session = 8 total registrations |

### Task 4.5.4: Update CLIAdapter ✅ COMPLETE

| Subtask | Description | Status | Evidence |
|---------|-------------|--------|----------|
| 4.5.4.1 | Add command_dispatcher parameter to CLIAdapter | ✅ DONE | Constructor takes ICommandDispatcher |
| 4.5.4.2 | Implement cmd_items_create | ✅ DONE | CreateWorkItemCommand + validation |
| 4.5.4.3 | Implement cmd_items_start | ✅ DONE | StartWorkItemCommand + error handling |
| 4.5.4.4 | Implement cmd_items_complete | ✅ DONE | CompleteWorkItemCommand + error handling |
| 4.5.4.5 | Implement cmd_items_block | ✅ DONE | BlockWorkItemCommand + reason required |
| 4.5.4.6 | Implement cmd_items_cancel | ✅ DONE | CancelWorkItemCommand + error handling |

### Task 4.5.5: Unit Tests ✅ COMPLETE

| Subtask | Description | Status | Evidence |
|---------|-------------|--------|----------|
| 4.5.5.1 | Command definition tests | ✅ DONE | 15 tests in test_work_item_commands.py |
| 4.5.5.2 | CreateWorkItemCommandHandler tests | ✅ DONE | 3 tests (success, defaults, parent) |
| 4.5.5.3 | StartWorkItemCommandHandler tests | ✅ DONE | 3 tests (success, not_found, invalid_state) |
| 4.5.5.4 | CompleteWorkItemCommandHandler tests | ✅ DONE | 3 tests (success, not_found, invalid_state) |
| 4.5.5.5 | BlockWorkItemCommandHandler tests | ✅ DONE | 3 tests (success, not_found, invalid_state) |
| 4.5.5.6 | CancelWorkItemCommandHandler tests | ✅ DONE | 4 tests (pending, blocked, not_found, invalid_state) |

### Task 4.5.6: Integration Tests

| Subtask | Description | Status | Evidence |
|---------|-------------|--------|----------|
| 4.5.6.1 | CLI -> CommandDispatcher -> Handler -> Repository | ⏳ PENDING | E2E flow |
| 4.5.6.2 | Event persistence verification | ⏳ PENDING | Events in filesystem |
| 4.5.6.3 | Full work item lifecycle test | ⏳ PENDING | create -> start -> complete |

---

## Files to Create/Modify

| File | Action | Description | Status |
|------|--------|-------------|--------|
| `src/work_tracking/application/commands/__init__.py` | **CREATE** | Package init | ✅ |
| `src/work_tracking/application/commands/create_work_item_command.py` | **CREATE** | Command | ✅ |
| `src/work_tracking/application/commands/start_work_item_command.py` | **CREATE** | Command | ✅ |
| `src/work_tracking/application/commands/complete_work_item_command.py` | **CREATE** | Command | ✅ |
| `src/work_tracking/application/commands/block_work_item_command.py` | **CREATE** | Command | ✅ |
| `src/work_tracking/application/commands/cancel_work_item_command.py` | **CREATE** | Command | ✅ |
| `src/work_tracking/application/handlers/commands/__init__.py` | **CREATE** | Package init | ✅ |
| `src/work_tracking/application/handlers/commands/create_work_item_command_handler.py` | **CREATE** | Handler | ✅ |
| `src/work_tracking/application/handlers/commands/start_work_item_command_handler.py` | **CREATE** | Handler | ✅ |
| `src/work_tracking/application/handlers/commands/complete_work_item_command_handler.py` | **CREATE** | Handler | ✅ |
| `src/work_tracking/application/handlers/commands/block_work_item_command_handler.py` | **CREATE** | Handler | ✅ |
| `src/work_tracking/application/handlers/commands/cancel_work_item_command_handler.py` | **CREATE** | Handler | ✅ |
| `src/bootstrap.py` | **MODIFY** | Wire command handlers | ✅ |
| `src/interface/cli/adapter.py` | **MODIFY** | Implement items commands | ✅ |
| `tests/work_tracking/unit/application/commands/` | **CREATE** | Command tests | ✅ |
| `tests/work_tracking/unit/application/handlers/commands/` | **CREATE** | Handler tests | ✅ |
| `tests/integration/test_items_commands.py` | **CREATE** | Integration tests | ⏳ |

---

## Command Specifications

### CreateWorkItemCommand

```python
@dataclass(frozen=True)
class CreateWorkItemCommand:
    title: str
    work_type: str = "task"  # task, bug, story, spike
    priority: str = "medium"  # low, medium, high, critical
    description: str = ""
    parent_id: str | None = None
```

### StartWorkItemCommand

```python
@dataclass(frozen=True)
class StartWorkItemCommand:
    work_item_id: str
    reason: str | None = None
```

### CompleteWorkItemCommand

```python
@dataclass(frozen=True)
class CompleteWorkItemCommand:
    work_item_id: str
    reason: str | None = None
```

### BlockWorkItemCommand

```python
@dataclass(frozen=True)
class BlockWorkItemCommand:
    work_item_id: str
    reason: str
```

### CancelWorkItemCommand

```python
@dataclass(frozen=True)
class CancelWorkItemCommand:
    work_item_id: str
    reason: str | None = None
```

---

## Handler Patterns

All handlers follow this pattern:
1. Validate input
2. Get/create aggregate via repository
3. Call aggregate command method
4. Save aggregate
5. Return domain events

```python
class StartWorkItemCommandHandler:
    def __init__(self, repository: IWorkItemRepository) -> None:
        self._repository = repository

    def handle(self, command: StartWorkItemCommand) -> list[DomainEvent]:
        work_item = self._repository.get_or_raise(command.work_item_id)
        work_item.start_work(reason=command.reason)
        self._repository.save(work_item)
        return list(work_item.collect_events())
```

---

## Acceptance Criteria

| ID | Criterion | Evidence | Status |
|----|-----------|----------|--------|
| AC-01 | `jerry items create` creates work item | CLI test | ⏳ |
| AC-02 | `jerry items start` starts work item | CLI test | ⏳ |
| AC-03 | `jerry items complete` completes work item | CLI test | ⏳ |
| AC-04 | `jerry items block` blocks work item | CLI test | ⏳ |
| AC-05 | `jerry items cancel` cancels work item | CLI test | ⏳ |
| AC-06 | Events persisted via FileSystemEventStore | File inspection | ⏳ |
| AC-07 | Commands wired through CommandDispatcher | Bootstrap inspection | ⏳ |
| AC-08 | All existing tests pass | pytest | ⏳ |

---

## Test Summary

| Category | Unit | Integration | Total | Status |
|----------|------|-------------|-------|--------|
| Commands | TBD | - | TBD | ⏳ |
| Handlers | TBD | - | TBD | ⏳ |
| Integration | - | TBD | TBD | ⏳ |
| **Total** | **TBD** | **TBD** | **TBD** | ⏳ |

---

## Progress Tracking

| Date | Activity | Status |
|------|----------|--------|
| 2026-01-12 | DISC-015: Identified event sourcing requirement | ✅ |
| 2026-01-12 | Phase 4.5 deferred until TD-018 | ✅ |
| 2026-01-12 | TD-018 Event Sourcing completed (104 tests) | ✅ |
| 2026-01-12 | PHASE-45-ITEMS-COMMANDS.md worktracker created | ✅ |
| 2026-01-12 | Task 4.5.1: Command definitions (5 commands created) | ✅ |
| 2026-01-12 | Task 4.5.2: Command handlers (5 handlers created) | ✅ |
| 2026-01-12 | Task 4.5.3: Wiring (8 handlers in CommandDispatcher) | ✅ |
| 2026-01-12 | Task 4.5.4: CLIAdapter (5 cmd_items_* methods implemented) | ✅ |
| - | Task 4.5.5: Unit tests | ⏳ PENDING |
| - | Task 4.5.6: Integration tests | ⏳ PENDING |

---

## Discoveries

| ID | Discovery | Impact | Action |
|----|-----------|--------|--------|
| - | - | - | - |

---

## References

| Document | Path | Relevance |
|----------|------|-----------|
| TD-018 | `work/PHASE-TD018-EVENT-SOURCING.md` | Prerequisite |
| DISC-015 | `work/PHASE-DISCOVERY.md` | Decision rationale |
| ADR-CLI-002 | `decisions/ADR-CLI-002-namespace-implementation.md` | CLI design |
| WorkItem Aggregate | `src/work_tracking/domain/aggregates/work_item.py` | Domain methods |
| Session Commands | `src/session_management/application/commands/` | Pattern reference |
