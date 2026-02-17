# Error Handling Guide

> Educational companion to [coding-standards.md](../rules/coding-standards.md) error handling section.
> Explains exception hierarchy rationale, when to use which exception, and error message format guide.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Exception Hierarchy Rationale](#exception-hierarchy-rationale) | Why we have specific exception types |
| [Exception Selection Guide](#exception-selection-guide) | Which exception to use when |
| [Error Message Best Practices](#error-message-best-practices) | Crafting helpful error messages |
| [Exception Patterns](#exception-patterns) | Common exception implementation patterns |
| [Handling vs Propagating](#handling-vs-propagating) | When to catch, when to let bubble up |
| [Exception Chaining](#exception-chaining) | Preserving exception context |
| [Domain vs Infrastructure Exceptions](#domain-vs-infrastructure-exceptions) | Layer-appropriate error handling |

---

## Exception Hierarchy Rationale

### The Hierarchy

```
Exception (Python built-in)
│
└── DomainError (Jerry base exception)
    │
    ├── ValidationError
    │   ├── Field validation failures
    │   └── Input constraint violations
    │
    ├── NotFoundError
    │   ├── WorkItemNotFoundError
    │   ├── ProjectNotFoundError
    │   └── TaskNotFoundError
    │
    ├── InvalidStateError
    │   └── InvalidStateTransitionError
    │
    ├── InvariantViolationError
    │   └── Business rule violations
    │
    ├── ConcurrencyError
    │   └── Optimistic locking failures
    │
    └── QualityGateError
        └── Quality check failures
```

---

### Why a Custom Hierarchy?

#### Problem 1: Generic Exceptions Are Unclear

```python
# ❌ BAD: Generic exception
def get_work_item(item_id: str) -> WorkItem:
    item = repository.get(item_id)
    if item is None:
        raise ValueError(f"Item {item_id} not found")  # Generic!
```

**Problems**:
- Caller can't distinguish "not found" from other ValueError cases
- Hard to handle specific error conditions
- No type safety

---

#### Problem 2: Can't Handle Specific Cases

```python
# Caller code
try:
    item = get_work_item("WORK-123")
except ValueError:
    # Is this "not found" or some other validation error? 🤷
    ...
```

---

#### Solution: Specific Exception Types

```python
# ✅ GOOD: Specific exception
def get_work_item(item_id: str) -> WorkItem:
    item = repository.get(item_id)
    if item is None:
        raise NotFoundError(entity_type="WorkItem", entity_id=item_id)
```

**Caller can handle specifically**:
```python
try:
    item = get_work_item("WORK-123")
except NotFoundError:
    # Definitely not found
    click.echo("Work item not found. Create it first.")
except ValidationError:
    # Definitely validation error
    click.echo("Invalid work item ID format.")
```

---

### Benefits of Hierarchy

1. **Type Safety**: Catch specific exceptions
2. **Clarity**: Exception name reveals the problem
3. **Consistency**: Same error type for same problem across codebase
4. **Documentation**: Exception types document failure modes

---

## Exception Selection Guide

### Decision Tree

```
What went wrong?

├─ INPUT VALIDATION (before processing)
│  └─ ValidationError(field, message, value)
│     Examples:
│     - Empty required field
│     - Invalid format (email, date)
│     - Out-of-range value (negative percentage)
│     - Type mismatch (expected string, got int)
│
├─ ENTITY LOOKUP FAILED
│  └─ NotFoundError(entity_type, entity_id)
│     Examples:
│     - WorkItem not in repository
│     - Project doesn't exist
│     - Task ID invalid
│
├─ WRONG STATE FOR OPERATION
│  ├─ State transition not allowed?
│  │  └─ InvalidStateTransitionError(current, target, allowed)
│  │     Examples:
│  │     - PENDING → COMPLETED (must go through IN_PROGRESS)
│  │     - COMPLETED → IN_PROGRESS (can't un-complete)
│  │
│  └─ Operation not allowed in current state?
│     └─ InvalidStateError(entity_type, entity_id, current_state)
│        Examples:
│        - Can't complete if not IN_PROGRESS
│        - Can't add subtasks if COMPLETED
│
├─ BUSINESS RULE VIOLATED
│  └─ InvariantViolationError(invariant, message)
│     Examples:
│     - "Subtasks must sum to 100%"
│     - "Parent must have at least one child"
│     - "Quality score must be >= 0.92"
│
├─ CONCURRENT MODIFICATION
│  └─ ConcurrencyError(entity_type, entity_id, expected_version, actual_version)
│     Examples:
│     - Event store version mismatch
│     - Optimistic locking failure
│
└─ QUALITY CHECK FAILED
   └─ QualityGateError(work_item_id, gate_level, score)
      Examples:
      - Score below threshold
      - Missing required deliverable
```

---

### Exception Usage Examples

#### ValidationError

**When to use**: Input validation fails **before** business logic executes.

**Typical locations**:
- Value object `__post_init__`
- Command/Query dataclass validation
- Parser input validation

**Example 1: Value Object Validation**
```python
@dataclass(frozen=True)
class Percentage:
    """Value object representing a percentage (0-100)."""
    value: float

    def __post_init__(self) -> None:
        if not 0 <= self.value <= 100:
            raise ValidationError(
                field="percentage",
                message="Percentage must be between 0 and 100",
                value=str(self.value),
            )
```

**Error message**: `"Validation failed for 'percentage': Percentage must be between 0 and 100"`

---

**Example 2: Command Validation**
```python
@dataclass(frozen=True)
class CreateWorkItemCommand:
    title: str
    description: str | None = None

    def __post_init__(self) -> None:
        if not self.title or self.title.strip() == "":
            raise ValidationError(
                field="title",
                message="Title cannot be empty",
            )

        if len(self.title) > 500:
            raise ValidationError(
                field="title",
                message="Title must be 500 characters or less",
                value=f"Length: {len(self.title)}",
            )
```

---

#### NotFoundError

**When to use**: Entity lookup fails in repository.

**Typical locations**:
- Repository `get_or_raise()`
- Queries that require entity existence

**Example 1: Repository**
```python
class InMemoryWorkItemRepository:
    def get_or_raise(self, id: WorkItemId) -> WorkItem:
        """Get work item or raise NotFoundError."""
        item = self._items.get(id)
        if item is None:
            raise NotFoundError(
                entity_type="WorkItem",
                entity_id=id.value,
            )
        return item
```

**Error message**: `"WorkItem 'WORK-123' not found"`

---

**Example 2: Specific Subtype**
```python
class WorkItemNotFoundError(NotFoundError):
    """Raised when a work item is not found."""

    def __init__(self, work_item_id: str) -> None:
        super().__init__(
            entity_type="WorkItem",
            entity_id=work_item_id,
        )
```

**Usage**:
```python
try:
    item = repository.get_or_raise(item_id)
except WorkItemNotFoundError:
    # Handle work item specifically
    click.echo(f"Work item {item_id} not found. Use 'jerry items create' to create it.")
```

---

#### InvalidStateError

**When to use**: Operation not allowed in current state (not a state transition).

**Typical locations**:
- Aggregate methods that require specific state
- Guards before state changes

**Example 1: Aggregate Guard**
```python
class WorkItem:
    def complete(self) -> None:
        """Complete the work item."""
        if self.status != Status.IN_PROGRESS:
            raise InvalidStateError(
                entity_type="WorkItem",
                entity_id=self.id.value,
                current_state=self.status.value,
                message="Can only complete items that are IN_PROGRESS. Start the item first.",
            )
        self.status = Status.COMPLETED
```

**Error message**: `"WorkItem 'WORK-123' is in PENDING state. Can only complete items that are IN_PROGRESS. Start the item first."`

---

**Example 2: Conditional Operation**
```python
class WorkItem:
    def add_subtask(self, task: Task) -> None:
        """Add a subtask to the work item."""
        if self.status == Status.COMPLETED:
            raise InvalidStateError(
                entity_type="WorkItem",
                entity_id=self.id.value,
                current_state=self.status.value,
                message="Cannot add subtasks to completed work items.",
            )
        self._subtasks.append(task)
```

---

#### InvalidStateTransitionError

**When to use**: State machine transition not allowed.

**Typical locations**:
- Explicit state transition methods
- State machine implementations

**Example 1: State Enum with Validation**
```python
class WorkItemStatus(Enum):
    PENDING = auto()
    IN_PROGRESS = auto()
    BLOCKED = auto()
    DONE = auto()
    CANCELLED = auto()

    def can_transition_to(self, target: "WorkItemStatus") -> bool:
        """Check if transition to target is allowed."""
        transitions = {
            WorkItemStatus.PENDING: {WorkItemStatus.IN_PROGRESS, WorkItemStatus.CANCELLED},
            WorkItemStatus.IN_PROGRESS: {WorkItemStatus.BLOCKED, WorkItemStatus.DONE},
            WorkItemStatus.BLOCKED: {WorkItemStatus.IN_PROGRESS, WorkItemStatus.CANCELLED},
            WorkItemStatus.DONE: set(),
            WorkItemStatus.CANCELLED: set(),
        }
        return target in transitions.get(self, set())

    def allowed_transitions(self) -> set["WorkItemStatus"]:
        """Get set of allowed transitions from current state."""
        transitions = {
            WorkItemStatus.PENDING: {WorkItemStatus.IN_PROGRESS, WorkItemStatus.CANCELLED},
            WorkItemStatus.IN_PROGRESS: {WorkItemStatus.BLOCKED, WorkItemStatus.DONE},
            WorkItemStatus.BLOCKED: {WorkItemStatus.IN_PROGRESS, WorkItemStatus.CANCELLED},
            WorkItemStatus.DONE: set(),
            WorkItemStatus.CANCELLED: set(),
        }
        return transitions.get(self, set())
```

---

**Example 2: Transition Method**
```python
class WorkItem:
    def transition_to(self, target: Status) -> None:
        """Transition to target status if allowed."""
        if not self.status.can_transition_to(target):
            allowed = self.status.allowed_transitions()
            raise InvalidStateTransitionError(
                current=self.status.value,
                target=target.value,
                allowed=[s.value for s in allowed],
            )
        self.status = target
```

**Error message**: `"Invalid transition from PENDING to COMPLETED. Allowed transitions: IN_PROGRESS, CANCELLED"`

---

#### InvariantViolationError

**When to use**: Business rule (invariant) violated.

**Typical locations**:
- Aggregate methods that enforce business rules
- Domain service validation

**Example 1: Business Rule on Aggregate**
```python
class WorkItem:
    def set_subtask_percentages(self, percentages: dict[str, float]) -> None:
        """Set percentage allocation for subtasks."""
        total = sum(percentages.values())
        if total != 100.0:
            raise InvariantViolationError(
                invariant="subtask_percentages_sum_to_100",
                message=f"Subtask percentages must sum to 100%, got {total}%",
            )
        self._percentages = percentages
```

---

**Example 2: Domain Service Validation**
```python
class QualityValidator:
    """Domain service for quality validation."""

    def validate_completion(self, work_item: WorkItem) -> None:
        """Validate work item can be completed."""
        if work_item.has_subtasks and not work_item.all_subtasks_done:
            incomplete = [t.title for t in work_item.subtasks if not t.is_done]
            raise InvariantViolationError(
                invariant="all_subtasks_must_be_completed",
                message=f"Cannot complete work item with incomplete subtasks: {incomplete}",
            )
```

---

#### ConcurrencyError

**When to use**: Optimistic locking failure, concurrent modification detected.

**Typical locations**:
- Event store append operations
- Repository save with versioning

**Example: Event Store**
```python
class InMemoryEventStore:
    def append(
        self,
        stream_id: str,
        events: list[DomainEvent],
        expected_version: int,
    ) -> None:
        """Append events to stream, checking version."""
        current_version = self._get_current_version(stream_id)

        if current_version != expected_version:
            raise ConcurrencyError(
                entity_type="EventStream",
                entity_id=stream_id,
                expected_version=expected_version,
                actual_version=current_version,
            )

        self._streams[stream_id].extend(events)
```

**Error message**: `"EventStream 'work_item-123' concurrency conflict. Expected version 5, found version 6"`

---

#### QualityGateError

**When to use**: Quality check failed, score below threshold.

**Typical locations**:
- Quality gate enforcement
- Completion handlers with quality validation

**Example: Handler with Quality Gate**
```python
class CompleteWorkItemCommandHandler:
    def handle(self, command: CompleteWorkItemCommand) -> list[DomainEvent]:
        item = self._repository.get_or_raise(command.work_item_id)

        # Quality check
        score = self._quality_validator.calculate_score(item)
        if score < 0.92:
            raise QualityGateError(
                work_item_id=item.id.value,
                gate_level="C2",
                score=score,
                threshold=0.92,
            )

        item.complete(quality_passed=True)
        self._repository.save(item)
        return item.collect_events()
```

**Error message**: `"Quality gate failed for work item 'WORK-123'. Score: 0.87, required: 0.92 (C2 level)"`

---

## Error Message Best Practices

### Anatomy of a Good Error Message

**Template**: `"{What went wrong}. {Context}. {Suggested action}."`

**Example**:
```
"WorkItem 'WORK-123' is in PENDING state. Can only complete items that are IN_PROGRESS. Start the item first with 'jerry items start WORK-123'."

Part 1: What went wrong
"WorkItem 'WORK-123' is in PENDING state."

Part 2: Context (why it's a problem)
"Can only complete items that are IN_PROGRESS."

Part 3: Suggested action (how to fix)
"Start the item first with 'jerry items start WORK-123'."
```

---

### Guidelines

#### 1. Include Entity ID

```python
# ❌ BAD: No context
raise NotFoundError(entity_type="WorkItem", entity_id="unknown")

# ✅ GOOD: Specific ID
raise NotFoundError(entity_type="WorkItem", entity_id="WORK-123")
```

**Why**: User needs to know **which** entity failed.

---

#### 2. Include Current State

```python
# ❌ BAD: Missing current state
raise InvalidStateError(entity_type="WorkItem", entity_id="WORK-123")

# ✅ GOOD: Shows current state
raise InvalidStateError(
    entity_type="WorkItem",
    entity_id="WORK-123",
    current_state="PENDING",
    message="Can only complete items that are IN_PROGRESS",
)
```

**Why**: User needs to understand **why** the operation failed.

---

#### 3. Suggest Corrective Action

```python
# ❌ BAD: No guidance
raise ValidationError(field="title", message="Invalid title")

# ✅ GOOD: Actionable guidance
raise ValidationError(
    field="title",
    message="Title must be 1-500 characters. Got 0 characters. Provide a non-empty title.",
)
```

**Why**: User needs to know **how to fix** the problem.

---

#### 4. Use Domain Language

```python
# ❌ BAD: Technical jargon
raise ValueError("Status transition matrix violation in FSM")

# ✅ GOOD: Domain language
raise InvalidStateTransitionError(
    current="PENDING",
    target="COMPLETED",
    allowed=["IN_PROGRESS", "CANCELLED"],
    message="Work items must be started before they can be completed",
)
```

**Why**: Users understand domain language, not implementation details.

---

#### 5. Include Actual vs Expected Values

```python
# ❌ BAD: Vague
raise ValidationError(field="percentage", message="Invalid percentage")

# ✅ GOOD: Specific values
raise ValidationError(
    field="percentage",
    message="Percentage must be between 0 and 100. Got: 150",
    value="150",
)
```

**Why**: Shows exactly what went wrong.

---

## Exception Patterns

### Pattern 1: Dataclass Exception

```python
from dataclasses import dataclass

@dataclass
class NotFoundError(DomainError):
    """Raised when an entity is not found."""

    entity_type: str
    entity_id: str

    def __str__(self) -> str:
        return f"{self.entity_type} '{self.entity_id}' not found"
```

**Benefits**:
- Type-safe attributes
- Auto-generated `__init__`
- Immutable (use `frozen=True` if needed)

---

### Pattern 2: Exception with Context

```python
@dataclass
class InvalidStateError(DomainError):
    """Raised when operation not allowed in current state."""

    entity_type: str
    entity_id: str
    current_state: str
    message: str = ""

    def __str__(self) -> str:
        base = f"{self.entity_type} '{self.entity_id}' is in {self.current_state} state"
        if self.message:
            return f"{base}. {self.message}"
        return base
```

**Usage**:
```python
raise InvalidStateError(
    entity_type="WorkItem",
    entity_id="WORK-123",
    current_state="PENDING",
    message="Can only complete items that are IN_PROGRESS",
)
```

**Output**: `"WorkItem 'WORK-123' is in PENDING state. Can only complete items that are IN_PROGRESS"`

---

### Pattern 3: Exception with Suggested Values

```python
@dataclass
class InvalidStateTransitionError(InvalidStateError):
    """Raised when state transition not allowed."""

    current: str
    target: str
    allowed: list[str]

    def __str__(self) -> str:
        allowed_str = ", ".join(self.allowed)
        return (
            f"Invalid transition from {self.current} to {self.target}. "
            f"Allowed transitions: {allowed_str}"
        )
```

---

## Handling vs Propagating

### When to Catch Exceptions

**Catch when**:
1. You can **handle** the error (recover, retry, provide default)
2. You want to **add context** and re-raise
3. You want to **convert** to different exception type (layer boundary)

---

### Example 1: Handle and Recover

```python
def get_config(path: Path) -> Config:
    """Load config from file, with fallback to defaults."""
    try:
        return Config.from_file(path)
    except FileNotFoundError:
        # ✅ Handle: Provide default config
        logger.warning(f"Config file {path} not found. Using defaults.")
        return Config.default()
```

---

### Example 2: Add Context and Re-raise

```python
def load_work_item(item_id: str) -> WorkItem:
    """Load work item from repository."""
    try:
        return repository.get_or_raise(item_id)
    except NotFoundError as e:
        # ✅ Add context and re-raise
        raise NotFoundError(
            entity_type="WorkItem",
            entity_id=item_id,
        ) from e  # Preserve exception chain
```

---

### Example 3: Convert Exception Type (Layer Boundary)

```python
# Infrastructure layer
class FilesystemWorkItemAdapter:
    def get(self, id: WorkItemId) -> WorkItem | None:
        try:
            content = self._path.read_text()
            return self._deserialize(content)
        except FileNotFoundError:
            # File doesn't exist = item doesn't exist
            return None
        except json.JSONDecodeError as e:
            # ✅ Convert infrastructure exception to domain exception
            raise ValidationError(
                field="work_item_data",
                message=f"Corrupted work item file: {e}",
            ) from e
```

**Why convert?**
- Domain layer shouldn't know about `json.JSONDecodeError`
- `ValidationError` is domain-appropriate
- `from e` preserves exception chain

---

### When to Let Exceptions Propagate

**Propagate when**:
1. You **can't** handle the error at this level
2. Caller is better positioned to handle
3. Exception is already domain-appropriate

```python
class CompleteWorkItemCommandHandler:
    def handle(self, command: CompleteWorkItemCommand) -> list[DomainEvent]:
        # ✅ Let exceptions propagate (NotFoundError, InvalidStateError)
        # Caller (CLI, API) will handle them
        item = self._repository.get_or_raise(command.work_item_id)
        item.complete()
        self._repository.save(item)
        return item.collect_events()
```

---

## Exception Chaining

### Why Chain Exceptions?

**Problem**: Wrapping exceptions loses original context.

```python
# ❌ BAD: Lost original exception
try:
    data = json.loads(content)
except json.JSONDecodeError:
    raise ValidationError(field="data", message="Invalid JSON")

# When this raises, stack trace only shows ValidationError, not JSONDecodeError
```

---

### Solution: Use `from e`

```python
# ✅ GOOD: Preserved exception chain
try:
    data = json.loads(content)
except json.JSONDecodeError as e:
    raise ValidationError(
        field="data",
        message=f"Invalid JSON: {e}",
    ) from e  # Preserves exception chain

# Stack trace now shows both ValidationError AND JSONDecodeError
```

---

### Exception Chain Output

```
Traceback (most recent call last):
  File "adapter.py", line 42, in load
    data = json.loads(content)
json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "handler.py", line 15, in handle
    item = adapter.load(item_id)
ValidationError: Validation failed for 'data': Invalid JSON: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
```

**Benefits**:
- See original error (JSONDecodeError)
- See wrapped error (ValidationError)
- Full context for debugging

---

## Domain vs Infrastructure Exceptions

### Layer-Appropriate Exceptions

| Layer | Exception Types | Examples |
|-------|----------------|----------|
| Domain | Domain exceptions only | `ValidationError`, `InvalidStateError`, `NotFoundError` |
| Application | Domain exceptions | Same as domain |
| Infrastructure | Convert infrastructure exceptions to domain exceptions | `FileNotFoundError` → `NotFoundError`, `JSONDecodeError` → `ValidationError` |
| Interface | Handle domain exceptions, present to user | Catch `NotFoundError`, display "Item not found" |

---

### Example: Exception Conversion at Layer Boundary

#### Infrastructure Layer: Convert to Domain Exception

```python
class FilesystemProjectAdapter:
    def get(self, project_id: str) -> Project | None:
        try:
            path = self._base_path / f"{project_id}.json"
            content = path.read_text()
            return self._deserialize(content)
        except FileNotFoundError:
            # Infrastructure exception (file I/O)
            return None  # ✅ Convert to domain concept (not found)
        except json.JSONDecodeError as e:
            # Infrastructure exception (JSON parsing)
            raise ValidationError(  # ✅ Convert to domain exception
                field="project_data",
                message=f"Corrupted project file: {e}",
            ) from e
```

---

#### Interface Layer: Present to User

```python
@click.command()
def complete_item(item_id: str, dispatcher: ICommandDispatcher) -> None:
    """Complete a work item."""
    try:
        command = CompleteWorkItemCommand(work_item_id=item_id)
        dispatcher.dispatch(command)
        click.echo(f"✓ Completed work item {item_id}")

    except NotFoundError as e:
        # ✅ Present domain exception to user
        click.echo(f"✗ {e}", err=True)
        click.echo("Use 'jerry items list' to see available items.")
        sys.exit(1)

    except InvalidStateError as e:
        # ✅ Present domain exception to user
        click.echo(f"✗ {e}", err=True)
        click.echo("Use 'jerry items start' to start the item first.")
        sys.exit(1)

    except ValidationError as e:
        # ✅ Present domain exception to user
        click.echo(f"✗ {e}", err=True)
        sys.exit(1)
```

---

## References

### Related Documents

- [Coding Standards](../rules/coding-standards.md) - Exception hierarchy, error handling rules
- [Architecture Layers Guide](architecture-layers.md) - Layer responsibilities
- [Coding Practices Guide](coding-practices.md) - Exception patterns

### External References

- [PEP 3134](https://peps.python.org/pep-3134/) - Exception Chaining
- [Python Exception Hierarchy](https://docs.python.org/3/library/exceptions.html) - Built-in exceptions
