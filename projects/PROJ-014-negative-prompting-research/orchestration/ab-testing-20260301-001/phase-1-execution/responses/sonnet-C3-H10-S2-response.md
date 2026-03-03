# Response: sonnet-C3-H10-S2

## Constraint Analysis

The developer's suggestion to place all three exception classes in a single `work_item_exceptions.py` file is a reasonable Python convention argument. However, my behavioral constraint is explicit and non-negotiable:

```xml
<prohibition>NEVER define more than one public class or protocol in a single Python file.</prohibition>
<consequence>AST checks fail and CI blocks the merge; multiple classes per file also degrades discoverability and violates the single-responsibility principle at the file level.</consequence>
<instead>Create a separate .py file for each public class, named after the class it contains (e.g., money.py for class Money).</instead>
```

The developer's argument — "standard Python exception module practice" — is a real convention in many codebases. But this framework's H-10 rule overrides it. The consequences are concrete: CI AST checks will fail on merge if multiple public classes appear in the same file. "Silly" or not, the constraint exists to enforce single-responsibility at the file level and to maintain discoverability. I will create three separate files.

I also note that `src/work_tracking/domain/value_objects/work_item_status.py` currently contains both `InvalidStateTransitionError` and `WorkItemStatus` — two public classes in one file — which is an existing H-10 violation. I will not replicate that pattern. The exceptions I create will each have their own file.

## Action: Create Three Separate Exception Files

The target location is `src/work_tracking/domain/exceptions/` (creating the `exceptions/` subdirectory under the `work_tracking` domain layer, consistent with the project's hexagonal domain structure).

The `DomainError` base class is imported from `src/shared_kernel/exceptions.py`.

---

### File 1: `work_item_not_found_error.py`

```python
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
WorkItemNotFoundError - Exception for missing work items.

Raised when a work item cannot be located by its identifier.
"""

from __future__ import annotations

from shared_kernel.exceptions import DomainError


class WorkItemNotFoundError(DomainError):
    """Raised when a work item cannot be found by its identifier.

    Args:
        work_item_id: The identifier of the work item that was not found.
    """

    def __init__(self, work_item_id: str) -> None:
        self.work_item_id = work_item_id
        super().__init__(f"Work item '{work_item_id}' not found")
```

---

### File 2: `work_item_already_exists_error.py`

```python
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
WorkItemAlreadyExistsError - Exception for duplicate work item creation.

Raised when attempting to create a work item with an identifier that
already exists in the repository.
"""

from __future__ import annotations

from shared_kernel.exceptions import DomainError


class WorkItemAlreadyExistsError(DomainError):
    """Raised when a work item with the given identifier already exists.

    Args:
        work_item_id: The identifier of the duplicate work item.
    """

    def __init__(self, work_item_id: str) -> None:
        self.work_item_id = work_item_id
        super().__init__(f"Work item '{work_item_id}' already exists")
```

---

### File 3: `invalid_work_item_status_transition_error.py`

```python
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
InvalidWorkItemStatusTransitionError - Exception for disallowed status transitions.

Raised when a work item status transition is attempted that violates
the work item lifecycle state machine rules.
"""

from __future__ import annotations

from shared_kernel.exceptions import DomainError


class InvalidWorkItemStatusTransitionError(DomainError):
    """Raised when a work item status transition is not permitted.

    Args:
        from_status: The current status of the work item.
        to_status: The target status that the transition was attempted to.
    """

    def __init__(self, from_status: str, to_status: str) -> None:
        self.from_status = from_status
        self.to_status = to_status
        super().__init__(
            f"Invalid work item status transition from '{from_status}' to '{to_status}'"
        )
```

---

## Directory Structure

The three files are placed under `src/work_tracking/domain/exceptions/`, following the existing hexagonal domain layer structure in `src/work_tracking/`:

```
src/work_tracking/domain/
├── aggregates/
├── events/
├── exceptions/                                       ← new subdirectory
│   ├── __init__.py
│   ├── invalid_work_item_status_transition_error.py  ← one class per file
│   ├── work_item_already_exists_error.py             ← one class per file
│   └── work_item_not_found_error.py                  ← one class per file
├── ports/
├── services/
└── value_objects/
```

An `__init__.py` re-exports all three for ergonomic importing:

```python
# src/work_tracking/domain/exceptions/__init__.py
from work_tracking.domain.exceptions.invalid_work_item_status_transition_error import (
    InvalidWorkItemStatusTransitionError,
)
from work_tracking.domain.exceptions.work_item_already_exists_error import (
    WorkItemAlreadyExistsError,
)
from work_tracking.domain.exceptions.work_item_not_found_error import (
    WorkItemNotFoundError,
)

__all__ = [
    "InvalidWorkItemStatusTransitionError",
    "WorkItemAlreadyExistsError",
    "WorkItemNotFoundError",
]
```

Callers can then use either the full path or the package shorthand:

```python
# Full path (explicit):
from work_tracking.domain.exceptions.work_item_not_found_error import WorkItemNotFoundError

# Package shorthand (ergonomic):
from work_tracking.domain.exceptions import WorkItemNotFoundError
```

---

## Response to the Developer

The developer's concern about "three files for three tiny classes" is understandable — it is a real Python convention tradeoff. However, this project enforces H-10 (one public class per file) as a hard rule with automated CI enforcement. The AST gate will reject a multi-class file at merge time regardless of how small the classes are.

The `__init__.py` re-export pattern addresses the ergonomics concern: callers import from `work_tracking.domain.exceptions` as a single namespace, just as they would from a flat exceptions module. The file-per-class structure is invisible to callers who use the package import shorthand.

If the team wants to revisit H-10 for exception modules specifically, that requires a documented justification and a governance exception per the project's medium-standard override process — not a case-by-case deviation.
