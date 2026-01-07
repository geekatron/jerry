# Coding Standards

> These rules are enforced across all Jerry framework development.
> They are loaded at session start and apply to all agents.

---

## Language: Python 3.11+

### Type Hints

- **REQUIRED** on all public functions and methods
- **REQUIRED** on class attributes
- Use `from __future__ import annotations` for forward references
- Prefer `X | None` over `Optional[X]`
- Use `list[T]`, `dict[K, V]` over `List[T]`, `Dict[K, V]`

```python
# Good
def process_item(item: WorkItem, config: Config | None = None) -> Result:
    ...

# Bad
def process_item(item, config=None):
    ...
```

### Docstrings

- **REQUIRED** on all public functions, classes, and modules
- Use Google-style docstrings
- Include Args, Returns, Raises sections as appropriate

```python
def complete_work_item(item_id: str) -> WorkItem:
    """Mark a work item as completed.

    Args:
        item_id: The unique identifier of the work item.

    Returns:
        The updated WorkItem with completed status.

    Raises:
        WorkItemNotFoundError: If no item exists with the given ID.
        InvalidStateError: If the item cannot be completed from its current state.
    """
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Modules | snake_case | `work_item.py` |
| Classes | PascalCase | `WorkItemRepository` |
| Functions | snake_case | `get_work_item` |
| Constants | UPPER_SNAKE | `MAX_RETRIES` |
| Private | _prefix | `_internal_helper` |
| Type Vars | T, K, V | `T = TypeVar('T')` |

### Line Length

- Maximum **100 characters** per line
- Exception: URLs in comments/docstrings

### Imports

- Group imports: stdlib, third-party, local
- Sort alphabetically within groups
- Use absolute imports for cross-package

```python
# Good
import json
from pathlib import Path

from src.domain.aggregates.work_item import WorkItem
from src.domain.ports.repository import IRepository
```

---

## Architecture Rules

### Domain Layer (`src/domain/`)

- **NO external imports** (only stdlib)
- **NO imports from** application/, infrastructure/, interface/
- Entities enforce their own invariants
- Value objects are immutable (use `@dataclass(frozen=True)`)
- Domain events use past tense (`WorkItemCompleted`)

### Application Layer (`src/application/`)

- **MAY import from** domain/
- **NO imports from** infrastructure/, interface/
- Commands return `None` or domain events
- Queries return DTOs, never domain entities

### Infrastructure Layer (`src/infrastructure/`)

- **MAY import from** domain/, application/
- **NO imports from** interface/
- Adapters MUST implement port interfaces
- Technical details stay encapsulated here

### Interface Layer (`src/interface/`)

- **MAY import from** all inner layers
- Handles translation between external and internal formats
- No business logic—delegate to application layer

---

## Testing Standards

### Test File Naming

- Unit tests: `tests/unit/test_{module}.py`
- Integration tests: `tests/integration/test_{adapter}.py`
- E2E tests: `tests/e2e/test_{workflow}.py`

### Test Function Naming

Use `test_{scenario}_when_{condition}_then_{expected}`:

```python
def test_complete_item_when_in_progress_then_status_becomes_completed():
    ...

def test_complete_item_when_already_completed_then_raises_error():
    ...
```

### Test Structure

Use Arrange-Act-Assert (AAA) pattern:

```python
def test_example():
    # Arrange
    item = WorkItem(title="Test")

    # Act
    item.complete()

    # Assert
    assert item.status == Status.COMPLETED
```

---

## Git Standards

### Commit Messages

Use conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code change that neither fixes nor adds
- `docs`: Documentation only
- `test`: Adding/updating tests
- `chore`: Build, CI, tooling

Example:
```
feat(worktracker): add ability to set due dates

Work items can now have optional due dates. The domain enforces
that due dates must be in the future when set.

Closes: WORK-042
```

### Branch Naming

- Feature: `feature/{work-item-id}-{short-description}`
- Fix: `fix/{work-item-id}-{short-description}`
- Release: `release/v{version}`

---

## Error Handling

### Domain Exceptions

Define specific exceptions in `src/domain/exceptions.py`:

```python
class DomainError(Exception):
    """Base class for domain errors."""

class WorkItemNotFoundError(DomainError):
    """Raised when a work item cannot be found."""

class InvalidStateError(DomainError):
    """Raised when an operation is invalid for the current state."""
```

### Error Messages

- Be specific about what went wrong
- Include relevant context (IDs, values)
- Suggest corrective action when possible

```python
# Good
raise WorkItemNotFoundError(
    f"Work item '{item_id}' not found. "
    f"Check that the ID is correct and the item has not been deleted."
)

# Bad
raise Exception("Not found")
```

---

## Documentation Standards

### File Headers

All Python files should start with a module docstring:

```python
"""
Module description.

This module provides {what it does}.

References:
    - {Relevant documentation}
"""
```

### Knowledge Capture

- Decisions: `docs/design/`
- Research: `docs/research/`
- Learnings: `docs/experience/`
- Patterns: `docs/wisdom/`

All documents must include:
- Document ID
- Date
- Author
- References/citations

---

## Enforcement

These standards are checked by:

1. **Pre-commit hooks**: Format, lint, type check
2. **CI pipeline**: Full test suite, coverage
3. **Code review**: Human verification
4. **QA Agent**: Automated review for patterns
