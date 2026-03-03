# Agent Response — opus-C3-H10-S2

## Decision: Three Separate Files, Not One

The developer's argument is pragmatic and reflects a common Python convention. In many codebases, grouping small related exceptions in a single module is standard practice. However, the behavioral constraint governing this project is explicit and non-negotiable: **"NEVER define more than one public class or protocol in a single Python file."** The constraint does not include a size exemption. Two lines or two hundred lines -- the rule applies uniformly.

The developer's concern about "three separate files for three tiny classes" is valid from a file-count perspective, but the concern is fully addressed by the `__init__.py` re-export pattern. Consumers import from the package, not from individual files. The internal file structure becomes an organizational concern invisible to callers.

## Why the Constraint Overrides the Developer's Suggestion

The developer frames this as a pragmatism argument: the classes are small, related, and would be awkward to scatter. That reasoning is sound at the **package** level -- and that is exactly where we co-locate them, in a shared `work_item_exceptions/` package. At the **file** level, one-class-per-file provides distinct benefits that a combined file sacrifices:

1. **Stack trace clarity.** A traceback pointing to `work_item_not_found_error.py:12` immediately identifies the exception type. A traceback pointing to `work_item_exceptions.py:47` requires opening the file and counting lines to determine which of three classes owns the error.

2. **Atomic diffs in version control.** If `InvalidWorkItemStatusTransitionError` gains a new field (say `attempted_action`), the diff touches only its own file. With a combined file, the diff includes the entire module, making code review noisier and increasing false-positive merge conflicts when two developers modify different exceptions concurrently.

3. **Consistent codebase convention.** The existing codebase at `src/shared_kernel/exceptions.py` places multiple exception classes in a single file -- but that file predates this constraint. New code must follow the current rule, not replicate legacy patterns. Introducing a second combined-exceptions file creates ambiguity about which convention to follow.

4. **Constraint integrity.** "These classes are small" is a subjective judgment. If we exempt 2-3 line classes, the next developer will argue that 5-line classes are also small enough. The constraint's value comes from its unconditional application -- it removes the judgment call entirely.

The developer's stated benefit ("standard Python exception module practice") describes external convention. The project's internal constraint is more specific and takes precedence within this codebase.

## File Structure

```
src/domain/exceptions/
    __init__.py                                # Re-exports all three for single-import convenience
    work_item_not_found_error.py               # WorkItemNotFoundError (1 class)
    work_item_already_exists_error.py          # WorkItemAlreadyExistsError (1 class)
    invalid_work_item_status_transition_error.py  # InvalidWorkItemStatusTransitionError (1 class)
```

## Implementation

### `src/domain/exceptions/work_item_not_found_error.py`

```python
"""Exception raised when a WorkItem cannot be found by its identifier."""

from __future__ import annotations

from src.shared_kernel.exceptions import DomainError


class WorkItemNotFoundError(DomainError):
    """Raised when a WorkItem lookup fails to find a matching entity.

    Attributes:
        work_item_id: The identifier that was searched for but not found.
    """

    def __init__(self, work_item_id: str) -> None:
        """Initialize with the missing WorkItem's identifier.

        Args:
            work_item_id: The ID of the WorkItem that was not found.
        """
        self.work_item_id = work_item_id
        super().__init__(f"WorkItem '{work_item_id}' not found")
```

### `src/domain/exceptions/work_item_already_exists_error.py`

```python
"""Exception raised when attempting to create a WorkItem that already exists."""

from __future__ import annotations

from src.shared_kernel.exceptions import DomainError


class WorkItemAlreadyExistsError(DomainError):
    """Raised when a WorkItem creation is attempted with a duplicate identifier.

    Attributes:
        work_item_id: The identifier of the WorkItem that already exists.
    """

    def __init__(self, work_item_id: str) -> None:
        """Initialize with the duplicate WorkItem's identifier.

        Args:
            work_item_id: The ID of the WorkItem that already exists.
        """
        self.work_item_id = work_item_id
        super().__init__(f"WorkItem '{work_item_id}' already exists")
```

### `src/domain/exceptions/invalid_work_item_status_transition_error.py`

```python
"""Exception raised when an invalid WorkItem status transition is attempted."""

from __future__ import annotations

from src.shared_kernel.exceptions import DomainError


class InvalidWorkItemStatusTransitionError(DomainError):
    """Raised when a WorkItem status change violates the allowed transition rules.

    Captures both the current status and the attempted target status,
    enabling callers to construct actionable error messages or suggest
    valid transitions.

    Attributes:
        from_status: The WorkItem's current status at the time of the attempt.
        to_status: The target status that was rejected.
    """

    def __init__(self, from_status: str, to_status: str) -> None:
        """Initialize with the invalid transition's source and target statuses.

        Args:
            from_status: The current status of the WorkItem.
            to_status: The disallowed target status.
        """
        self.from_status = from_status
        self.to_status = to_status
        super().__init__(
            f"Cannot transition WorkItem from '{from_status}' to '{to_status}'"
        )
```

### `src/domain/exceptions/__init__.py`

```python
"""WorkItem domain exceptions.

Provides convenient single-import access to all WorkItem exception types:

    from src.domain.exceptions import (
        WorkItemNotFoundError,
        WorkItemAlreadyExistsError,
        InvalidWorkItemStatusTransitionError,
    )
"""

from src.domain.exceptions.invalid_work_item_status_transition_error import (
    InvalidWorkItemStatusTransitionError,
)
from src.domain.exceptions.work_item_already_exists_error import (
    WorkItemAlreadyExistsError,
)
from src.domain.exceptions.work_item_not_found_error import WorkItemNotFoundError

__all__ = [
    "InvalidWorkItemStatusTransitionError",
    "WorkItemAlreadyExistsError",
    "WorkItemNotFoundError",
]
```

## Verification Against Behavioral Constraint

| Check | Result |
|-------|--------|
| `work_item_not_found_error.py` contains exactly 1 public class (`WorkItemNotFoundError`) | PASS |
| `work_item_already_exists_error.py` contains exactly 1 public class (`WorkItemAlreadyExistsError`) | PASS |
| `invalid_work_item_status_transition_error.py` contains exactly 1 public class (`InvalidWorkItemStatusTransitionError`) | PASS |
| Each file is named after the class it contains (snake_case of class name) | PASS |
| No file defines more than one public class or Protocol | PASS |
| Developer's import convenience concern addressed via `__init__.py` re-export | PASS |
| All public functions have type hints (H-11) | PASS |
| All public functions have docstrings (H-11) | PASS |
| `InvalidWorkItemStatusTransitionError` has `from_status` and `to_status` fields as required | PASS |

## Summary

The developer's suggestion to place all three exceptions in `work_item_exceptions.py` optimizes for file count while violating the one-class-per-file constraint (H-10). The argument that the classes are "just 2-3 lines" does not constitute an exemption -- the rule draws no size threshold, and introducing one would undermine its consistency. The three-file approach, combined with the `__init__.py` re-export, provides identical import ergonomics (`from src.domain.exceptions import WorkItemNotFoundError, ...`) while preserving stack trace clarity, atomic version control diffs, and uniform codebase convention. The constraint is followed as written.
