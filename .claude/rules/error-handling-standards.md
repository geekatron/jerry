# Error Handling Standards

> Exception hierarchy, error patterns, and error handling guidelines for Jerry.
> These standards ensure consistent, informative, and actionable error handling.

**Authoritative Pattern Source**: `.claude/patterns/PATTERN-CATALOG.md`

---

## Exception Hierarchy

### Base Classes

```
Exception (Python built-in)
└── DomainError
    ├── ValidationError
    ├── NotFoundError
    │   └── AggregateNotFoundError
    ├── InvalidStateError
    │   └── InvalidStateTransitionError
    ├── InvariantViolationError
    ├── ConcurrencyError
    └── QualityGateError

└── ApplicationError
    ├── HandlerNotFoundError
    ├── UnauthorizedError
    └── ConfigurationError

└── InfrastructureError
    ├── PersistenceError
    ├── EventStoreError
    │   └── StreamNotFoundError
    └── ExternalServiceError
```

---

## Domain Exceptions

### Location

`src/shared_kernel/exceptions.py`

### Base Domain Error

```python
class DomainError(Exception):
    """Base class for all domain errors.

    Domain errors represent violations of business rules or invariants.
    They should be caught and translated by interface adapters.
    """
    pass
```

### Validation Error

```python
class ValidationError(DomainError):
    """Field validation failed.

    Use for:
    - Empty required fields
    - Invalid format (email, phone, etc.)
    - Value out of range
    - Type mismatches
    """

    def __init__(
        self,
        field: str,
        message: str,
        value: Any = None,
    ) -> None:
        self.field = field
        self.validation_message = message
        self.invalid_value = value
        super().__init__(f"Validation failed for '{field}': {message}")
```

### Not Found Error

```python
class NotFoundError(DomainError):
    """Entity or resource not found.

    Use for:
    - Aggregate not in repository
    - Reference to non-existent entity
    - Missing required resource
    """

    def __init__(
        self,
        entity_type: str,
        entity_id: str,
        message: str | None = None,
    ) -> None:
        self.entity_type = entity_type
        self.entity_id = entity_id
        msg = message or f"{entity_type} with ID '{entity_id}' not found"
        super().__init__(msg)


class AggregateNotFoundError(NotFoundError):
    """Aggregate root not found in repository."""
    pass
```

### Invalid State Error

```python
class InvalidStateError(DomainError):
    """Operation invalid for current entity state.

    Use for:
    - Modifying completed/cancelled entities
    - Operations requiring different status
    - Lifecycle violations
    """

    def __init__(
        self,
        entity_type: str,
        entity_id: str,
        current_state: str,
        message: str,
    ) -> None:
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.current_state = current_state
        super().__init__(message)


class InvalidStateTransitionError(InvalidStateError):
    """State machine transition not allowed.

    Use for:
    - Status changes that violate state machine
    - Workflow violations
    """

    def __init__(
        self,
        current_state: str,
        target_state: str,
        valid_targets: set[str] | None = None,
    ) -> None:
        self.target_state = target_state
        self.valid_targets = valid_targets or set()
        super().__init__(
            entity_type="State",
            entity_id="",
            current_state=current_state,
            message=(
                f"Cannot transition from '{current_state}' to '{target_state}'. "
                f"Valid transitions: {self.valid_targets or 'none'}"
            ),
        )
```

### Invariant Violation Error

```python
class InvariantViolationError(DomainError):
    """Business invariant violated.

    Use for:
    - Domain rule violations
    - Cross-aggregate constraints
    - Business logic failures
    """

    def __init__(
        self,
        invariant: str,
        message: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        self.invariant = invariant
        self.context = context or {}
        super().__init__(f"Invariant '{invariant}' violated: {message}")
```

### Concurrency Error

```python
class ConcurrencyError(DomainError):
    """Optimistic concurrency conflict.

    Use for:
    - Version mismatch during save
    - Concurrent modification detection
    - Stale data updates
    """

    def __init__(
        self,
        entity_type: str,
        entity_id: str,
        expected_version: int,
        actual_version: int,
    ) -> None:
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.expected_version = expected_version
        self.actual_version = actual_version
        super().__init__(
            f"Concurrency conflict for {entity_type} '{entity_id}': "
            f"expected version {expected_version}, found {actual_version}. "
            f"Reload and retry."
        )
```

### Quality Gate Error

```python
class QualityGateError(DomainError):
    """Quality gate check failed.

    Use for:
    - Completion blocked by quality requirements
    - Test coverage insufficient
    - Required reviews missing
    """

    def __init__(
        self,
        work_item_id: str,
        gate_level: str,
        failures: list[str] | None = None,
    ) -> None:
        self.work_item_id = work_item_id
        self.gate_level = gate_level
        self.failures = failures or []
        super().__init__(
            f"Quality gate '{gate_level}' failed for work item '{work_item_id}': "
            f"{', '.join(self.failures) or 'unspecified failure'}"
        )
```

---

## Application Exceptions

### Location

`src/application/exceptions.py`

```python
class ApplicationError(Exception):
    """Base class for application layer errors."""
    pass


class HandlerNotFoundError(ApplicationError):
    """No handler registered for command/query type."""

    def __init__(self, message_type: type) -> None:
        self.message_type = message_type
        super().__init__(f"No handler registered for {message_type.__name__}")


class UnauthorizedError(ApplicationError):
    """Operation not permitted for current user/context."""

    def __init__(self, operation: str, reason: str = "") -> None:
        self.operation = operation
        self.reason = reason
        super().__init__(f"Unauthorized: {operation}. {reason}".strip())


class ConfigurationError(ApplicationError):
    """Application configuration is invalid or missing."""

    def __init__(self, key: str, message: str) -> None:
        self.key = key
        super().__init__(f"Configuration error for '{key}': {message}")
```

---

## Infrastructure Exceptions

### Location

`src/infrastructure/exceptions.py`

```python
class InfrastructureError(Exception):
    """Base class for infrastructure layer errors."""
    pass


class PersistenceError(InfrastructureError):
    """Database or storage operation failed."""

    def __init__(self, operation: str, message: str) -> None:
        self.operation = operation
        super().__init__(f"Persistence error during {operation}: {message}")


class EventStoreError(InfrastructureError):
    """Event store operation failed."""
    pass


class StreamNotFoundError(EventStoreError):
    """Event stream does not exist."""

    def __init__(self, stream_id: str) -> None:
        self.stream_id = stream_id
        super().__init__(f"Event stream '{stream_id}' not found")


class ExternalServiceError(InfrastructureError):
    """External service call failed."""

    def __init__(
        self,
        service_name: str,
        operation: str,
        message: str,
    ) -> None:
        self.service_name = service_name
        self.operation = operation
        super().__init__(
            f"External service '{service_name}' failed during {operation}: {message}"
        )
```

---

## Exception Selection Guidelines

| Situation | Exception | Example |
|-----------|-----------|---------|
| Empty/invalid field value | `ValidationError` | Empty title, invalid email |
| Entity doesn't exist | `NotFoundError` / `AggregateNotFoundError` | Get work item that doesn't exist |
| Operation wrong for current state | `InvalidStateError` | Modify completed item |
| Status transition not allowed | `InvalidStateTransitionError` | Complete from pending |
| Business rule violated | `InvariantViolationError` | Circular dependency |
| Concurrent modification | `ConcurrencyError` | Save with stale version |
| Quality check failed | `QualityGateError` | Complete without tests |
| Missing handler | `HandlerNotFoundError` | Unknown command type |
| Permission denied | `UnauthorizedError` | Edit without rights |
| Config missing | `ConfigurationError` | No database URL |
| DB/storage failure | `PersistenceError` | Write failed |
| Event store issue | `EventStoreError` | Append failed |
| External API failure | `ExternalServiceError` | API timeout |

---

## Error Message Guidelines

### Include Context

```python
# GOOD: Specific with context
raise NotFoundError(
    entity_type="WorkItem",
    entity_id="WORK-001",
    message="Work item 'WORK-001' not found. It may have been deleted.",
)

# BAD: Vague
raise Exception("Not found")
```

### Suggest Action

```python
# GOOD: Actionable
raise ConcurrencyError(
    entity_type="WorkItem",
    entity_id="WORK-001",
    expected_version=5,
    actual_version=6,
    # Message includes "Reload and retry."
)

# BAD: No action suggested
raise Exception("Version conflict")
```

### Be Specific

```python
# GOOD: Specific exception
raise InvalidStateTransitionError(
    current_state="pending",
    target_state="done",
    valid_targets={"in_progress", "cancelled"},
)

# BAD: Generic exception
raise ValueError("Invalid transition")
```

---

## Error Handling in Handlers

```python
class CreateWorkItemCommandHandler:
    def handle(self, command: CreateWorkItemCommand) -> list[DomainEvent]:
        # Validation (raises ValidationError)
        if not command.title.strip():
            raise ValidationError(
                field="title",
                message="Title cannot be empty",
                value=command.title,
            )

        # Domain logic (may raise domain errors)
        try:
            work_item = WorkItem.create(
                id=self._generate_id(),
                title=command.title,
            )
        except ValueError as e:
            # Convert to domain error
            raise ValidationError(
                field="unknown",
                message=str(e),
            )

        # Persistence (may raise infrastructure errors)
        try:
            self._repository.save(work_item)
        except ConcurrencyError:
            raise  # Let it bubble up
        except Exception as e:
            raise PersistenceError(
                operation="save",
                message=str(e),
            )

        return list(work_item.collect_events())
```

---

## Error Handling in CLI Adapter

```python
class CLIAdapter:
    def create_work_item(self, title: str) -> int:
        try:
            command = CreateWorkItemCommand(title=title)
            self._dispatcher.dispatch(command)
            print(f"Created work item: {title}")
            return 0

        except ValidationError as e:
            print(f"Error: Invalid {e.field}: {e.validation_message}")
            return 1

        except NotFoundError as e:
            print(f"Error: {e.entity_type} '{e.entity_id}' not found")
            return 1

        except InvalidStateError as e:
            print(f"Error: Cannot perform operation in state '{e.current_state}'")
            return 1

        except ConcurrencyError as e:
            print(f"Error: Concurrent modification detected. Please retry.")
            return 1

        except DomainError as e:
            print(f"Error: {e}")
            return 1

        except Exception as e:
            print(f"Unexpected error: {e}")
            return 2  # Different exit code for unexpected
```

---

## Testing Exceptions

```python
def test_validation_error_includes_field():
    """ValidationError captures field name."""
    error = ValidationError(
        field="title",
        message="cannot be empty",
    )

    assert error.field == "title"
    assert "title" in str(error)


def test_concurrency_error_includes_versions():
    """ConcurrencyError captures version info."""
    error = ConcurrencyError(
        entity_type="WorkItem",
        entity_id="WORK-001",
        expected_version=5,
        actual_version=6,
    )

    assert error.expected_version == 5
    assert error.actual_version == 6
    assert "Reload and retry" in str(error)


def test_handler_raises_validation_error_for_empty_title():
    """Handler rejects empty title with proper error."""
    handler = CreateWorkItemCommandHandler(repository=mock_repo)

    with pytest.raises(ValidationError) as exc_info:
        handler.handle(CreateWorkItemCommand(title=""))

    assert exc_info.value.field == "title"
    assert "empty" in exc_info.value.validation_message.lower()
```

---

## Anti-Patterns

### 1. Using Generic Exceptions

```python
# WRONG
raise Exception("Something went wrong")
raise ValueError("Invalid input")

# CORRECT
raise ValidationError(field="title", message="cannot be empty")
raise InvariantViolationError(invariant="no_circular_deps", message="...")
```

### 2. Catching Too Broadly

```python
# WRONG
try:
    work_item.complete()
except Exception:
    pass  # Swallows all errors

# CORRECT
try:
    work_item.complete()
except InvalidStateTransitionError as e:
    logger.warning(f"Cannot complete: {e}")
    raise  # Re-raise for caller to handle
```

### 3. Losing Exception Context

```python
# WRONG
except Exception as e:
    raise RuntimeError("Failed")  # Original error lost

# CORRECT
except Exception as e:
    raise PersistenceError(operation="save", message=str(e)) from e
```

---

## References

- **Python Documentation**: [Exception Handling](https://docs.python.org/3/tutorial/errors.html)
- **Clean Code**: Error Handling chapter
- **Design Canon**: Section 4.3 - Error Handling
- **Related Patterns**: PAT-AGG-004 (Invariant Enforcement)
