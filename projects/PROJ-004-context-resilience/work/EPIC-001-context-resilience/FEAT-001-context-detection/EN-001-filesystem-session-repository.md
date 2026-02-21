# EN-001: FileSystemSessionRepository

> **Type:** enabler
> **Status:** pending
> **Priority:** critical
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-19
> **Due:** --
> **Completed:** --
> **Parent:** FEAT-001
> **Owner:** --
> **Effort:** 3-4h

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Technical scope |
| [Acceptance Criteria](#acceptance-criteria) | BDD scenarios and checklist |
| [Dependencies](#dependencies) | What this enables |
| [History](#history) | Status changes |

---

## Summary

Implement `FileSystemSessionRepository` in `src/session_management/infrastructure/adapters/` that implements the existing `ISessionRepository` port by delegating to `FileSystemEventStore`. Follow the exact pattern established by `EventSourcedWorkItemRepository`: event registry for session events (`SessionCreated`, `SessionCompleted`, `SessionAbandoned`, `SessionProjectLinked`), stream ID convention (`session-{id}`), domain-to-stored event conversion, and aggregate reconstitution via `Session.load_from_history()`.

This eliminates the `InMemorySessionRepository` limitation ("Loses data on process termination") that blocks cross-process session state required by all context monitoring hooks.

**Technical Scope:**
- New file: `src/session_management/infrastructure/adapters/filesystem_session_repository.py`
- Event registry mapping 4 session events to stored events
- Stream ID convention: `session-{id}`
- Wire into `bootstrap.py` replacing `InMemorySessionRepository` in production
- Retain `InMemorySessionRepository` for unit testing

**Reference Implementations:**
- `src/work_tracking/infrastructure/adapters/event_sourced_work_item_repository.py` (431 lines — pattern to follow)
- `src/work_tracking/infrastructure/persistence/filesystem_event_store.py` (369 lines — reuse as-is)
- `src/session_management/application/ports/session_repository.py` (ISessionRepository port)
- `src/session_management/domain/aggregates/session.py` (Session.load_from_history(), lines 284-324)

---

## Acceptance Criteria

### BDD Scenarios (pytest-bdd)

```gherkin
Feature: FileSystemSessionRepository persists sessions across processes

  Background:
    Given a FileSystemSessionRepository backed by FileSystemEventStore
    And the events directory is ".jerry/data/events/"

  Scenario: Save and retrieve a session
    Given a new Session created with id "sess-001"
    When I save the session via the repository
    And I retrieve the session by id "sess-001" in a new repository instance
    Then the session id should be "sess-001"
    And the session status should be ACTIVE

  Scenario: Session survives process termination
    Given a session "sess-002" saved via the repository
    When I create a new FileSystemSessionRepository instance (simulating new process)
    And I call get("sess-002")
    Then the session should be returned with all events replayed

  Scenario: Get active session across all streams
    Given session "sess-003" with status ACTIVE
    And session "sess-004" with status COMPLETED
    When I call get_active()
    Then only session "sess-003" should be returned

  Scenario: Abandon session with reason
    Given an active session "sess-005"
    When I call abandon with reason "context compaction at 82%"
    And I save the session
    Then the session status should be ABANDONED
    And the abandon reason should be "context compaction at 82%"
    And the event stream should contain a SessionAbandoned event

  Scenario: Optimistic concurrency prevents concurrent writes
    Given a session "sess-006" at version 3
    When two concurrent save operations are attempted
    Then one should succeed and one should raise a concurrency error

  Scenario: Event replay reconstitutes session correctly
    Given a session "sess-007" with events: Created, ProjectLinked, Abandoned
    When I load from the event store and call Session.load_from_history()
    Then the session should have project_id set
    And the session status should be ABANDONED
```

### Acceptance Checklist

- [ ] `FileSystemSessionRepository` implements `ISessionRepository` protocol (H-11 type hints, H-12 docstrings)
- [ ] Session events persisted to `.jerry/data/events/session-{id}.jsonl`
- [ ] `jerry session start` creates a session that persists across process termination
- [ ] `jerry session status` in a new process retrieves the active session
- [ ] `jerry session abandon --reason "compaction"` correctly abandons persisted session
- [ ] `Session.load_from_history()` correctly reconstitutes from event replay
- [ ] Optimistic concurrency via `FileSystemEventStore` prevents concurrent writes
- [ ] `get_active()` returns the most recent ACTIVE session across all streams
- [ ] Unit tests: save/get round-trip, get_active, event replay, cross-process, concurrency
- [ ] `InMemorySessionRepository` retained for unit testing, not used in production wiring
- [ ] `bootstrap.py` wires `FileSystemSessionRepository` as `ISessionRepository` implementation
- [ ] One class per file (H-10)

---

## Dependencies

**Depends On:** Nothing (uses existing `FileSystemEventStore` as-is)

**Enables:**
- EN-003 (CheckpointService triggers session abandon)
- EN-006 (session-start and pre-compact CLI commands use session events)
- All context monitoring hooks (require cross-process session state)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-19 | Claude | pending | Enabler created from CWI-00. P0 foundation enabler. |
