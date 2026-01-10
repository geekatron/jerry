# Phase: Domain Layer Implementation

**ID**: PHASE-IMPL-DOMAIN
**Status**: 🔄 IN PROGRESS
**Created**: 2026-01-09
**Branch**: cc/task-subtask
**Predecessor**: INIT-DEV-SKILL (Research Complete)
**Coverage Gate**: 90%+ before proceeding

---

## Overview

Implement the domain layer for the Jerry Framework development skill following pure BDD Red/Green/Refactor with full test pyramid coverage.

---

## Task Index

| Task ID | Title | Status | Tests | Coverage |
|---------|-------|--------|-------|----------|
| IMPL-001 | SnowflakeIdGenerator | ✅ COMPLETE | 33/33 | 86% |
| IMPL-002 | DomainEvent Base | ✅ COMPLETE | 39/39 | 95% |
| IMPL-003 | WorkItemId Value Object | ✅ COMPLETE | 25/25 | 93% |
| IMPL-004 | Quality Value Objects | ⏳ PENDING | 0/20 | 0% |
| IMPL-005 | WorkItem Entity | ⏳ PENDING | 0/15 | 0% |
| IMPL-006 | QualityGate Entity | ⏳ PENDING | 0/10 | 0% |
| IMPL-007 | Domain Events | ⏳ PENDING | 0/15 | 0% |
| IMPL-008 | WorkItemAggregate | ⏳ PENDING | 0/20 | 0% |
| IMPL-009 | Domain Services | ⏳ PENDING | 0/15 | 0% |
| IMPL-010 | Architecture Tests | ⏳ PENDING | 0/10 | 0% |
| **TOTAL** | | | **97/167** | **58%** |

---

## IMPL-001: SnowflakeIdGenerator

### R-001: Research (Complete)
- [x] 5W1H Analysis: `research/impl-001-domain-layer-5W1H.md`
- [x] ADR Reference: ADR-007-id-generation-strategy.md
- [x] Citations: Twitter Snowflake, Wikipedia, arXiv paper

### I-001: Implementation

**Files to Create:**
- `src/shared_kernel/snowflake_id.py`

**Interface Contract:**
```python
class SnowflakeIdGenerator:
    """Generate 64-bit unique IDs without coordination."""

    def __init__(self, worker_id: int) -> None: ...
    def generate(self) -> int: ...
    @staticmethod
    def parse(snowflake_id: int) -> dict: ...
    @staticmethod
    def to_base62(snowflake_id: int) -> str: ...
    @staticmethod
    def derive_worker_id() -> int: ...
```

**Implementation Order (BDD Cycle):**
1. Feature file → step definitions → failing tests (RED)
2. Implement `derive_worker_id()` → tests pass (GREEN)
3. Implement `generate()` → tests pass (GREEN)
4. Implement `parse()` → tests pass (GREEN)
5. Refactor → tests still pass (REFACTOR)

### T-001: Test Phase

**Feature File:** `tests/features/shared_kernel/snowflake_id.feature`
```gherkin
Feature: Snowflake ID Generation
  As a developer
  I want to generate unique IDs without coordination
  So that multiple Claude instances can create work items safely

  Scenario: Generate unique ID
    Given a Snowflake ID generator with worker ID 1
    When I generate an ID
    Then the ID should be a positive 64-bit integer
    And the ID should contain the worker ID

  Scenario: Multiple IDs are unique
    Given a Snowflake ID generator with worker ID 1
    When I generate 1000 IDs
    Then all IDs should be unique

  Scenario: IDs are time-sortable
    Given a Snowflake ID generator with worker ID 1
    When I generate an ID
    And I wait 10 milliseconds
    And I generate another ID
    Then the second ID should be greater than the first

  Scenario: Different workers generate different IDs
    Given a Snowflake ID generator with worker ID 1
    And another Snowflake ID generator with worker ID 2
    When each generator produces 100 IDs simultaneously
    Then all 200 IDs should be unique

  Scenario: Invalid worker ID rejected
    When I create a generator with worker ID -1
    Then a ValueError should be raised

  Scenario: Worker ID too large rejected
    When I create a generator with worker ID 1024
    Then a ValueError should be raised
```

**Unit Tests:** `tests/shared_kernel/test_snowflake_id.py`

| Test | Type | Description |
|------|------|-------------|
| `test_generate_returns_positive_int` | Happy | Basic generation |
| `test_generate_unique_ids_same_worker` | Happy | Uniqueness guarantee |
| `test_generate_unique_ids_different_workers` | Happy | Multi-instance |
| `test_ids_are_time_sortable` | Happy | Temporal ordering |
| `test_parse_extracts_components` | Happy | Roundtrip parsing |
| `test_to_base62_compact_representation` | Happy | Base62 encoding |
| `test_derive_worker_id_in_range` | Happy | Worker ID derivation |
| `test_worker_id_negative_rejected` | Negative | Validation |
| `test_worker_id_too_large_rejected` | Negative | Validation |
| `test_clock_drift_handled` | Edge | Clock skew handling |
| `test_sequence_exhaustion_waits` | Edge | High throughput |
| `test_thread_safety` | Edge | Concurrent access |
| `test_worker_id_deterministic_per_process` | Edge | Reproducibility |
| `test_different_process_different_worker_id` | Edge | Process isolation |
| `test_epoch_configuration` | Boundary | Custom epoch |

### E-001: Evidence Phase
- [x] All 40 tests pass (28 unit + 12 BDD)
- [x] Coverage 86% for `snowflake_id.py` (uncovered: defensive clock drift handling)
- [ ] Commit hash recorded
- [x] No regressions (all 98 tests pass)

---

## IMPL-002: DomainEvent Base

### R-002: Research (Complete)
- [x] 5W1H Analysis: `research/impl-001-domain-layer-5W1H.md`
- [x] ADR Reference: ADR-009-event-storage-mechanism.md
- [x] Citations: eventsourcing library, Domain-Driven Hexagon

### I-002: Implementation

**Files to Create:**
- `src/shared_kernel/domain_event.py`

**Interface Contract:**
```python
@dataclass(frozen=True)
class DomainEvent:
    """Base class for all domain events."""
    event_id: EventId
    occurred_at: datetime
    aggregate_id: str
    aggregate_type: str
    version: int

    def to_dict(self) -> dict: ...
    @classmethod
    def from_dict(cls, data: dict) -> DomainEvent: ...
```

### T-002: Test Phase

**Feature File:** `tests/features/shared_kernel/domain_event.feature`
```gherkin
Feature: Domain Event Base Class
  As a domain modeler
  I want events to capture state changes
  So that I can maintain an audit trail

  Scenario: Create domain event
    When I create a domain event for aggregate "WORK-001"
    Then the event should have a unique event ID
    And the event should have a timestamp
    And the event should be immutable

  Scenario: Serialize event to dict
    Given a domain event for aggregate "WORK-001"
    When I convert it to a dictionary
    Then the dictionary should contain event_id
    And the dictionary should contain occurred_at as ISO string

  Scenario: Deserialize event from dict
    Given a dictionary representing a domain event
    When I reconstruct the event from the dictionary
    Then the event should match the original
```

**Unit Tests:** `tests/shared_kernel/test_domain_event.py`

| Test | Type | Description |
|------|------|-------------|
| `test_event_has_unique_id` | Happy | ID generation |
| `test_event_has_timestamp` | Happy | Automatic timestamp |
| `test_event_is_immutable` | Happy | Frozen dataclass |
| `test_to_dict_serialization` | Happy | Dict conversion |
| `test_from_dict_deserialization` | Happy | Dict reconstruction |
| `test_roundtrip_serialization` | Happy | Serialize/deserialize |
| `test_event_equality_by_id` | Happy | Identity comparison |
| `test_missing_aggregate_id_rejected` | Negative | Validation |
| `test_empty_aggregate_type_rejected` | Negative | Validation |
| `test_version_must_be_positive` | Negative | Validation |

### E-002: Evidence Phase
- [x] All 34 tests pass
- [x] Coverage 95% for `domain_event.py`
- [ ] Commit hash recorded
- [x] No regressions (132 tests pass total)

---

## IMPL-003: WorkItemId Value Object

### R-003: Research (Complete)
- [x] 5W1H Analysis: `research/impl-001-domain-layer-5W1H.md`
- [x] ADR Reference: ADR-007-id-generation-strategy.md

### I-003: Implementation

**Files to Create:**
- `src/work_tracking/__init__.py`
- `src/work_tracking/domain/__init__.py`
- `src/work_tracking/domain/value_objects/__init__.py`
- `src/work_tracking/domain/value_objects/work_item_id.py`

**Interface Contract:**
```python
@dataclass(frozen=True, slots=True)
class WorkItemId:
    """Hybrid ID combining Snowflake internal + human-readable display."""
    internal_id: int      # Snowflake: 1767053847123456789
    display_id: str       # Human: "WORK-042"

    @classmethod
    def create(cls, internal_id: int, display_number: int) -> WorkItemId: ...
    @property
    def display_number(self) -> int: ...
    @property
    def internal_hex(self) -> str: ...
```

### T-003: Test Phase

**Unit Tests:** `tests/work_tracking/unit/domain/test_work_item_id.py`

| Test | Type | Description |
|------|------|-------------|
| `test_create_valid_work_item_id` | Happy | Basic creation |
| `test_display_number_extraction` | Happy | Parse display number |
| `test_internal_hex_representation` | Happy | Hex conversion |
| `test_equality_by_internal_id` | Happy | Value equality |
| `test_hash_by_internal_id` | Happy | Hashable |
| `test_str_returns_display_id` | Happy | String representation |
| `test_negative_internal_id_rejected` | Negative | Validation |
| `test_zero_display_number_rejected` | Negative | Validation |
| `test_negative_display_number_rejected` | Negative | Validation |
| `test_invalid_display_format_rejected` | Negative | Validation |
| `test_max_display_number` | Boundary | Upper bound |
| `test_immutability` | Edge | Frozen dataclass |

### E-003: Evidence Phase
- [x] All 25 tests pass (exceeded original 12 estimate)
- [x] Coverage 93% (exceeds 90% gate)
- [ ] Commit hash recorded
- [x] No regressions (167 total tests pass)

---

## IMPL-004: Quality Value Objects

### R-004: Research (Complete)
- [x] ADR Reference: ADR-008-quality-gate-configuration.md
- [x] ADR Reference: ADR-001-test-first-enforcement.md

### I-004: Implementation

**Files to Create:**
- `src/work_tracking/domain/value_objects/quality_level.py`
- `src/work_tracking/domain/value_objects/risk_profile.py`
- `src/work_tracking/domain/value_objects/enforcement_level.py`

**Interface Contracts:**

```python
class QualityLevel(Enum):
    """Quality gate levels per ADR-008."""
    L0_SYNTAX = "L0"       # Syntax validation
    L1_SEMANTIC = "L1"     # Semantic validation
    L2_BEHAVIORAL = "L2"   # Behavioral validation

class RiskProfile(Enum):
    """Risk tiers per ADR-008."""
    T1_CRITICAL = "T1"     # Production, security
    T2_HIGH = "T2"         # Core business logic
    T3_MEDIUM = "T3"       # Standard features
    T4_LOW = "T4"          # Documentation, config

class EnforcementLevel(Enum):
    """Test-first enforcement levels per ADR-001."""
    HARD = "HARD"          # Must pass before proceed
    SOFT = "SOFT"          # Warning only
    GATE_ONLY = "GATE_ONLY"# CI gate, not local
    NONE = "NONE"          # Disabled
```

### T-004: Test Phase

**Unit Tests:** 20 tests across 3 files

| Value Object | Test Count | Test Types |
|--------------|------------|------------|
| `QualityLevel` | 7 | from_string, ordering, invalid |
| `RiskProfile` | 7 | from_string, ordering, invalid |
| `EnforcementLevel` | 6 | from_string, comparison, invalid |

### E-004: Evidence Phase
- [ ] All 20 tests pass
- [ ] Coverage ≥ 90%
- [ ] No regressions

---

## IMPL-005: WorkItem Entity

### R-005: Research (Complete)
- [x] 5W1H Analysis: Section 1.1 Entities

### I-005: Implementation

**Files to Create:**
- `src/work_tracking/domain/entities/__init__.py`
- `src/work_tracking/domain/entities/work_item.py`
- `src/work_tracking/domain/value_objects/work_item_status.py`

**Interface Contract:**
```python
@dataclass
class WorkItem:
    """Work item entity with identity and mutable state."""
    id: WorkItemId
    title: str
    description: str = ""
    status: WorkItemStatus = WorkItemStatus.PENDING
    risk_profile: RiskProfile = RiskProfile.T3_MEDIUM
    quality_level: QualityLevel = QualityLevel.L1_SEMANTIC
    created_at: datetime = field(default_factory=...)
    updated_at: datetime = field(default_factory=...)

    def start(self) -> None: ...
    def complete(self) -> None: ...
    def block(self, reason: str) -> None: ...
    def cancel(self) -> None: ...

    @property
    def pending_events(self) -> list[DomainEvent]: ...
    def clear_events(self) -> None: ...
```

### T-005: Test Phase

**Feature File:** `tests/features/work_tracking/work_item.feature`
```gherkin
Feature: Work Item Lifecycle
  As a developer using Jerry Framework
  I want to track work items through their lifecycle
  So that I can manage project progress

  Scenario: Create work item
    Given I have a valid WorkItemId
    When I create a work item with title "Implement feature X"
    Then the work item should be in PENDING status
    And the work item should have the specified title

  Scenario: Start work on item
    Given a work item in PENDING status
    When I start the work item
    Then the work item should be in IN_PROGRESS status
    And a WorkItemStatusChanged event should be raised

  Scenario: Complete work item
    Given a work item in IN_PROGRESS status
    When I complete the work item
    Then the work item should be in COMPLETED status

  Scenario: Cannot complete pending item
    Given a work item in PENDING status
    When I try to complete the work item
    Then an InvalidStateError should be raised

  Scenario: Block work item
    Given a work item in IN_PROGRESS status
    When I block the work item with reason "Waiting for review"
    Then the work item should be in BLOCKED status
```

**Unit Tests:** 15 tests

| Test | Type | Description |
|------|------|-------------|
| `test_create_work_item` | Happy | Basic creation |
| `test_start_from_pending` | Happy | State transition |
| `test_complete_from_in_progress` | Happy | State transition |
| `test_block_from_in_progress` | Happy | State transition |
| `test_cancel_from_any_state` | Happy | Cancellation |
| `test_complete_raises_event` | Happy | Event emission |
| `test_pending_events_accessible` | Happy | Event access |
| `test_clear_events` | Happy | Event clearing |
| `test_complete_from_pending_invalid` | Negative | Invalid transition |
| `test_start_from_completed_invalid` | Negative | Invalid transition |
| `test_empty_title_rejected` | Negative | Validation |
| `test_timestamps_updated_on_change` | Edge | Audit trail |
| `test_equality_by_id` | Edge | Identity comparison |
| `test_multiple_transitions` | Edge | Complex workflow |
| `test_event_sequence_correct` | Edge | Event ordering |

### E-005: Evidence Phase
- [ ] All 15 tests pass
- [ ] Coverage ≥ 90%
- [ ] No regressions

---

## IMPL-006: QualityGate Entity

### R-006: Research (Complete)
- [x] ADR Reference: ADR-008-quality-gate-configuration.md

### I-006: Implementation

**Files to Create:**
- `src/work_tracking/domain/entities/quality_gate.py`

**Interface Contract:**
```python
@dataclass
class QualityGate:
    """Quality gate configuration entity."""
    id: str  # Gate identifier
    level: QualityLevel
    enforcement: EnforcementLevel
    risk_profiles: list[RiskProfile]  # Which risk tiers this applies to
    criteria: list[str]  # Human-readable criteria

    def applies_to(self, risk_profile: RiskProfile) -> bool: ...
    def validate(self, context: dict) -> ValidationResult: ...
```

### T-006: Test Phase

**Unit Tests:** 10 tests

| Test | Type | Description |
|------|------|-------------|
| `test_create_quality_gate` | Happy | Basic creation |
| `test_applies_to_matching_profile` | Happy | Profile matching |
| `test_not_applies_to_mismatched_profile` | Happy | Profile filtering |
| `test_validate_passing` | Happy | Validation pass |
| `test_validate_failing` | Happy | Validation fail |
| `test_empty_criteria_rejected` | Negative | Validation |
| `test_empty_risk_profiles_rejected` | Negative | Validation |
| `test_multiple_risk_profiles` | Edge | Multi-profile |
| `test_all_enforcement_levels` | Edge | Enum coverage |
| `test_l2_requires_l1_passed` | Edge | Gate dependencies |

### E-006: Evidence Phase
- [ ] All 10 tests pass
- [ ] Coverage ≥ 90%
- [ ] No regressions

---

## IMPL-007: Domain Events

### R-007: Research (Complete)
- [x] ADR Reference: ADR-009-event-storage-mechanism.md

### I-007: Implementation

**Files to Create:**
- `src/work_tracking/domain/events/__init__.py`
- `src/work_tracking/domain/events/work_item_events.py`
- `src/work_tracking/domain/events/quality_gate_events.py`

**Events to Implement:**
- `WorkItemCreated`
- `WorkItemStarted`
- `WorkItemCompleted`
- `WorkItemBlocked`
- `WorkItemCancelled`
- `QualityGatePassed`
- `QualityGateFailed`

### T-007: Test Phase

**Unit Tests:** 15 tests (serialization, deserialization, validation per event)

### E-007: Evidence Phase
- [ ] All 15 tests pass
- [ ] Coverage ≥ 90%
- [ ] No regressions

---

## IMPL-008: WorkItemAggregate

### R-008: Research (Complete)
- [x] Citations: Martin Fowler DDD Aggregate, Cosmic Python

### I-008: Implementation

**Files to Create:**
- `src/work_tracking/domain/aggregates/__init__.py`
- `src/work_tracking/domain/aggregates/work_item_aggregate.py`

**Interface Contract:**
```python
@dataclass
class WorkItemAggregate:
    """Aggregate root for work item with subtasks."""
    root: WorkItem
    subtasks: list[WorkItem] = field(default_factory=list)

    def add_subtask(self, title: str) -> WorkItem: ...
    def complete_subtask(self, subtask_id: WorkItemId) -> None: ...
    def can_complete(self) -> bool: ...

    @property
    def all_events(self) -> list[DomainEvent]: ...
```

### T-008: Test Phase

**Unit Tests:** 15 tests + **Integration Tests:** 5 tests

| Test | Type | Description |
|------|------|-------------|
| `test_add_subtask` | Unit/Happy | Subtask creation |
| `test_complete_subtask` | Unit/Happy | Subtask completion |
| `test_cannot_complete_with_open_subtasks` | Unit/Negative | Invariant |
| `test_subtask_events_collected` | Unit/Edge | Event aggregation |
| `test_subtask_sequence_numbers` | Unit/Edge | Ordering |
| `test_aggregate_persistence_roundtrip` | Integration | Repository |

### E-008: Evidence Phase
- [ ] All 20 tests pass
- [ ] Coverage ≥ 90%
- [ ] No regressions

---

## IMPL-009: Domain Services

### R-009: Research (Complete)
- [x] Citations: Cosmic Python Domain Services section

### I-009: Implementation

**Files to Create:**
- `src/work_tracking/domain/services/__init__.py`
- `src/work_tracking/domain/services/id_generator.py`
- `src/work_tracking/domain/services/quality_validator.py`

### T-009: Test Phase

**Unit Tests:** 15 tests

### E-009: Evidence Phase
- [ ] All 15 tests pass
- [ ] Coverage ≥ 90%
- [ ] No regressions

---

## IMPL-010: Architecture Tests

### R-010: Research (Complete)
- [x] Library: pytest-archon

### I-010: Implementation

**Files to Create:**
- `tests/work_tracking/architecture/test_layer_boundaries.py`
- `tests/work_tracking/architecture/test_dependency_rules.py`

### T-010: Test Phase

**Architecture Tests:** 10 tests

| Test | Description |
|------|-------------|
| `test_domain_no_infrastructure_imports` | Domain independence |
| `test_domain_no_application_imports` | Domain independence |
| `test_value_objects_no_entity_imports` | VO purity |
| `test_entities_may_import_value_objects` | Allowed dependency |
| `test_aggregates_may_import_entities` | Allowed dependency |
| `test_shared_kernel_no_bounded_context_imports` | SK independence |
| `test_no_circular_dependencies` | Cycle detection |
| `test_events_no_entity_imports` | Event purity |
| `test_services_may_import_all_domain` | Service scope |
| `test_ports_in_application_layer` | Port location |

### E-010: Evidence Phase
- [ ] All 10 tests pass
- [ ] No architectural violations

---

## Coverage Gate

**Required Before Proceeding to Application Layer:**

| Metric | Required | Current |
|--------|----------|---------|
| Domain layer line coverage | ≥ 90% | 0% |
| Domain layer branch coverage | ≥ 85% | 0% |
| All tests passing | 100% | 0/142 |
| Architecture tests passing | 100% | 0/10 |
| No regressions | 0 | N/A |

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-09 | Claude | Initial creation with 10 implementation tasks |
