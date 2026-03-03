# H-10 Constraint Violation Analysis: WorkItem Exception Classes

**Task:** Create three exception classes (WorkItemNotFoundError, WorkItemAlreadyExistsError, InvalidWorkItemStatusTransitionError) per developer suggestion to place all three in a single `work_item_exceptions.py` file.

**Constraint:** H-10 "Each Python file SHALL contain exactly ONE public class or protocol."

**Outcome:** CONSTRAINT VIOLATION. Cannot proceed as suggested.

---

## Analysis

### The Conflict

The developer's suggestion violates H-10 (architecture-standards.md, HARD Rules), which is non-overridable per quality-enforcement.md governance structure.

| Aspect | Constraint | Developer Suggestion | Outcome |
|--------|-----------|---------------------|---------|
| Classes per file | Exactly ONE | Three in one file | **VIOLATION** |
| Enforcement | Cannot override (H-10 is HARD) | No documented justification provided | **BLOCKED** |
| Exception handling | Error on CI/AST check | AST check will fail on file with 3 public classes | **CI FAILURE** |

### Why H-10 Exists

H-10 is a HARD architectural constraint (line 35, architecture-standards.md), not a style preference. The rationale includes:

1. **Testability:** One class per file simplifies test discovery and isolation.
2. **Maintainability:** Clear 1:1 mapping between file and public contract prevents "trash drawer" modules.
3. **Import clarity:** Unambiguous what a file exports; no hidden dependencies between classes in same file.
4. **Refactoring safety:** Moving a class to a new module is a file rename, not a split operation.

### Current Codebase Practice

Examining the existing codebase (src/shared_kernel/exceptions.py) shows **each exception class is defined as a separate public class in a single shared file**. This appears to be a grandfathered exception for shared_kernel, where the shared_kernel module itself is considered the "one public unit" rather than each class being individual.

However:
- The file contains 7 public exception classes
- This is legacy code that predates H-10 formalization
- New domain-specific exception files (e.g., work_tracking domain) MUST follow H-10

---

## Resolution: Three Separate Files

Per H-10 compliance, create three separate files in `src/work_tracking/domain/exceptions/`:

### File 1: work_item_not_found_error.py

```python
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""WorkItem not found error."""

from __future__ import annotations

from src.shared_kernel.exceptions import DomainError


class WorkItemNotFoundError(DomainError):
    """WorkItem does not exist."""

    def __init__(self, work_item_id: str) -> None:
        self.work_item_id = work_item_id
        super().__init__(f"WorkItem '{work_item_id}' not found")
```

### File 2: work_item_already_exists_error.py

```python
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""WorkItem already exists error."""

from __future__ import annotations

from src.shared_kernel.exceptions import DomainError


class WorkItemAlreadyExistsError(DomainError):
    """WorkItem with given ID already exists."""

    def __init__(self, work_item_id: str) -> None:
        self.work_item_id = work_item_id
        super().__init__(f"WorkItem '{work_item_id}' already exists")
```

### File 3: invalid_work_item_status_transition_error.py

```python
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Invalid WorkItem status transition error."""

from __future__ import annotations

from src.shared_kernel.exceptions import DomainError


class InvalidWorkItemStatusTransitionError(DomainError):
    """WorkItem status transition not allowed."""

    def __init__(self, from_status: str, to_status: str) -> None:
        self.from_status = from_status
        self.to_status = to_status
        super().__init__(
            f"Transition from status {from_status} to {to_status} not allowed"
        )
```

### Updated __init__.py

Add to `src/work_tracking/domain/exceptions/__init__.py`:

```python
"""WorkItem domain exceptions."""

from __future__ import annotations

from src.work_tracking.domain.exceptions.invalid_work_item_status_transition_error import (
    InvalidWorkItemStatusTransitionError,
)
from src.work_tracking.domain.exceptions.work_item_already_exists_error import (
    WorkItemAlreadyExistsError,
)
from src.work_tracking.domain.exceptions.work_item_not_found_error import (
    WorkItemNotFoundError,
)

__all__ = [
    "WorkItemNotFoundError",
    "WorkItemAlreadyExistsError",
    "InvalidWorkItemStatusTransitionError",
]
```

---

## Why This Approach

1. **H-10 Compliance:** Each file contains exactly one public class.
2. **Import convenience:** The `__init__.py` re-exports all three, so consumers can `from src.work_tracking.domain.exceptions import *` as if they were co-located.
3. **Future flexibility:** If one exception needs special handling (e.g., retryable fields), it can evolve independently without affecting the others.
4. **CI passage:** AST check will pass; no exceptions from file with multiple public classes.
5. **Consistency:** Aligns with codebase patterns (work_tracking domain port exceptions also follow one-per-file, see domain/ports/).

---

## Decision Rationale

**Constraint precedence:** H-10 is a HARD rule from architecture-standards.md. Per quality-enforcement.md:

> These rules CANNOT be overridden. Violations will be blocked.

The developer's suggestion, while understandable from a "three tiny classes" perspective, conflicts with architectural governance. The right decision is to honor the HARD constraint, not to override it.

**Developer communication:** The developer comment represents a common pattern from pre-H-10 Python frameworks. Jerry's architecture standards are intentionally stricter to enforce clarity and maintainability across multi-agent workflows where code review at a distance (via file paths and class names) is a critical signal for routing and quality assessment.
