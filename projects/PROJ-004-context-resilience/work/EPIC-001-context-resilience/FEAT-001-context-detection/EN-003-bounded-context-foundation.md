# EN-003: Context Monitoring Bounded Context Foundation

> **Type:** enabler
> **Status:** completed
> **Priority:** critical
> **Impact:** critical
> **Enabler Type:** architecture
> **Created:** 2026-02-19
> **Due:** --
> **Completed:** 2026-02-21
> **Parent:** FEAT-001
> **Owner:** --
> **Effort:** 4-6h

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Technical scope |
| [Bounded Context Structure](#bounded-context-structure) | Directory and component listing |
| [Acceptance Criteria](#acceptance-criteria) | BDD scenarios and checklist |
| [Technical Approach](#technical-approach) | Implementation approach |
| [Dependencies](#dependencies) | What this enables |
| [History](#history) | Status changes |

---

## Summary

Create the `src/context_monitoring/` bounded context with proper hexagonal architecture following `session_management` and `work_tracking` patterns. This item establishes: directory structure, domain value objects, domain events, CheckpointService application service, ICheckpointRepository port, and FilesystemCheckpointRepository adapter.

**Technical Scope:**
- Full directory structure: `domain/value_objects/`, `domain/events/`, `application/services/`, `application/ports/`, `infrastructure/adapters/`
- 4 value objects: ThresholdTier, FillEstimate, CheckpointData, ContextState
- 3 domain events: ContextThresholdReached, CompactionDetected, CheckpointCreated (one file each per H-10)
- 1 application service: CheckpointService
- 1 port: ICheckpointRepository
- 1 adapter: FilesystemCheckpointRepository
- Composition root wiring in `bootstrap.py`

---

## Bounded Context Structure

```
src/context_monitoring/
  __init__.py
  domain/
    __init__.py
    value_objects/
      __init__.py
      threshold_tier.py          # ThresholdTier enum
      fill_estimate.py           # FillEstimate frozen dataclass
      checkpoint_data.py         # CheckpointData frozen dataclass
      context_state.py           # ContextState frozen dataclass
    events/
      __init__.py
      context_threshold_reached.py  # ContextThresholdReached
      compaction_detected.py        # CompactionDetected
      checkpoint_created.py         # CheckpointCreated
  application/
    __init__.py
    services/
      __init__.py
      checkpoint_service.py      # CheckpointService
    ports/
      __init__.py
      checkpoint_repository.py   # ICheckpointRepository Protocol
  infrastructure/
    __init__.py
    adapters/
      __init__.py
      filesystem_checkpoint_repository.py  # FilesystemCheckpointRepository
```

---

## Acceptance Criteria

### BDD Scenarios (pytest-bdd)

```gherkin
Feature: Context monitoring domain value objects

  Scenario: ThresholdTier enum has all 5 levels
    When I import ThresholdTier
    Then it should have members: NOMINAL, LOW, WARNING, CRITICAL, EMERGENCY

  Scenario: FillEstimate is immutable
    Given a FillEstimate with fill_percentage=0.72 and tier=WARNING
    When I attempt to modify fill_percentage
    Then a FrozenInstanceError should be raised

  Scenario: CheckpointData captures resumption state
    Given a CheckpointData with resumption_state from ORCHESTRATION.yaml
    Then checkpoint_id should be a string
    And context_state should be a FillEstimate
    And resumption_state should be a dict or None


Feature: Checkpoint persistence via FilesystemCheckpointRepository

  Scenario: Save and retrieve a checkpoint
    Given a FilesystemCheckpointRepository pointing to ".jerry/checkpoints/"
    And a CheckpointData with id "cx-001"
    When I save the checkpoint
    And I call get_latest_unacknowledged()
    Then the returned checkpoint should have id "cx-001"

  Scenario: Sequential checkpoint ID generation
    Given checkpoints cx-001 and cx-002 already exist
    When CheckpointService creates a new checkpoint
    Then the checkpoint id should be "cx-003"

  Scenario: Acknowledged checkpoints are excluded
    Given checkpoint "cx-001" is saved and then acknowledged
    When I call get_latest_unacknowledged()
    Then None should be returned

  Scenario: Acknowledgment creates marker file
    Given checkpoint "cx-001" is saved
    When I call acknowledge("cx-001")
    Then file ".jerry/checkpoints/cx-001-checkpoint.json.acknowledged" should exist

  Scenario: Checkpoint directory auto-created
    Given no ".jerry/checkpoints/" directory exists
    When I save a checkpoint
    Then the directory should be created automatically
    And the checkpoint should be saved successfully

  Scenario: Acknowledgment after response delivery (DEF-005)
    Given an unacknowledged checkpoint "cx-001"
    When the session-start handler reads the checkpoint
    Then acknowledge() is called AFTER checkpoint data is formatted for response
    And if the handler times out, the checkpoint remains unacknowledged


Feature: CheckpointService orchestrates checkpoint lifecycle

  Scenario: CheckpointService creates checkpoint on pre-compact
    Given a CheckpointService with ICheckpointRepository and IThresholdConfiguration
    And context monitoring is enabled
    When create_checkpoint is called with fill estimate and session info
    Then a CheckpointData should be persisted via ICheckpointRepository
    And the checkpoint should contain resumption_state from ORCHESTRATION.yaml if present

  Scenario: CheckpointService is fail-open when ORCHESTRATION.yaml absent
    Given no ORCHESTRATION.yaml exists in the project
    When create_checkpoint is called
    Then a checkpoint should still be created
    And resumption_state should be None
```

### Acceptance Checklist

- [ ] `src/context_monitoring/` directory structure created with `__init__.py` at each level
- [ ] 4 value objects: frozen dataclasses with type hints and docstrings (H-10, H-11, H-12)
- [ ] 3 domain events: frozen dataclasses, one class per file (H-10)
- [ ] `ICheckpointRepository` Protocol: `save()`, `get_latest_unacknowledged()`, `acknowledge()`, `list_all()` (H-11, H-12)
- [ ] `FilesystemCheckpointRepository`: atomic writes via `AtomicFileAdapter`, `.acknowledged` marker files
- [ ] Sequential checkpoint IDs (cx-001, cx-002, ...)
- [ ] `CheckpointService`: reads ORCHESTRATION.yaml (fail-open), assembles CheckpointData, calls repository
- [ ] Acknowledgment timing: `acknowledge()` called AFTER data included in response (DEF-005)
- [ ] `bootstrap.py` wires `FilesystemCheckpointRepository` -> `ICheckpointRepository`
- [ ] H-07: domain layer has no external imports
- [ ] H-08: application layer has no infrastructure imports
- [ ] Unit tests: value object immutability, event construction, checkpoint CRUD, sequential IDs, acknowledged filtering, fail-open

---

## Technical Approach

Create the `src/context_monitoring/` bounded context with proper hexagonal architecture following `session_management` and `work_tracking` patterns. Establish directory structure, domain value objects, domain events, CheckpointService application service, ICheckpointRepository port, and FilesystemCheckpointRepository adapter. Completed as part of parent feature.

---

## Dependencies

**Depends On:**
- EN-001 (FileSystemSessionRepository for session domain events)
- EN-002 (ConfigThresholdAdapter for threshold reading)
- ST-001 (resumption schema for CheckpointData.resumption_state)

**Enables:**
- EN-004 (ContextFillEstimator + ResumptionContextGenerator use CheckpointService)
- EN-006 (CLI commands use CheckpointService)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-19 | Claude | pending | Enabler created from CWI-02. Major redesign from v1. |
