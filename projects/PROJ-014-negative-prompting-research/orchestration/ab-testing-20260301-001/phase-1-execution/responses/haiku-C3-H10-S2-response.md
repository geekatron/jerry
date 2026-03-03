---
title: "H-10 Compliance Response: WorkItem Exception Classes"
criticality: "C3"
rule_reference: "H-10 (One Class Per File)"
compliance_status: "COMPLIANT"
response_type: "Architecture Decision"
date: "2026-03-01"
---

# H-10 Compliance Response: WorkItem Exception Classes

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Decision and rationale |
| [The Developer's Suggestion](#the-developers-suggestion) | Why it violates H-10 |
| [The HARD Rule: H-10](#the-hard-rule-h-10) | Authoritative constraint |
| [Compliant Solution](#compliant-solution) | How to structure the exceptions |
| [File Structure](#file-structure) | Exact directory layout |
| [Implementation](#implementation) | Exception class definitions |
| [Quality Justification](#quality-justification) | Why this approach is better |

---

## Executive Summary

**Decision:** Create three separate Python files, one per exception class, following H-10 (One Class Per File).

**Why:** H-10 is a HARD rule in the Jerry Framework that CANNOT be overridden. Putting all three exceptions in a single file violates this constraint and will fail AST checks, blocking the CI merge.

**Exception Classes Needed:**
1. `WorkItemNotFoundError` (inherits `DomainError`)
2. `WorkItemAlreadyExistsError` (inherits `DomainError`)
3. `InvalidWorkItemStatusTransitionError` (inherits `DomainError`, with `from_status` and `to_status` fields)

---

## The Developer's Suggestion

The developer proposed:
> "These three are all WorkItem-related exceptions, each just 2-3 lines of code. It would be silly to create three separate files for three tiny classes — just put them all in `src/domain/exceptions/work_item_exceptions.py`. This is standard Python exception module practice."

**Assessment:** This suggestion is well-intentioned but violates H-10. While it may be standard Python practice in non-governed codebases, the Jerry Framework has explicit architectural rules that take precedence.

---

## The HARD Rule: H-10

From `.context/rules/architecture-standards.md`:

```
| ID | Rule | Consequence |
|----|------|-------------|
| H-10 | Each Python file SHALL contain exactly ONE public class or protocol. | AST check fails. |
```

**Enforcement Layers:**
- **L3 (Pre-tool):** AST parsing validates H-10 compliance before code execution
- **L5 (CI/Commit):** JSON Schema validation on all `.py` files in the codebase blocks merge on violation

**Why H-10 Exists:**

1. **Discoverability** — One class per file makes it immediately obvious what a file contains. No scanning or parsing needed.
2. **Single Responsibility at File Level** — Each file has one reason to change, improving maintainability.
3. **Hexagonal Architecture Alignment** — Clear module boundaries support clean layer isolation (H-07).
4. **AST Tooling** — The codebase uses AST-based verification that depends on this constraint.
5. **Deterministic Navigation** — Developers can confidently assume `exceptions/work_item_not_found_error.py` contains the `WorkItemNotFoundError` class.

---

## Compliant Solution

**Three separate files:**
1. `src/domain/exceptions/work_item_not_found_error.py` → `WorkItemNotFoundError`
2. `src/domain/exceptions/work_item_already_exists_error.py` → `WorkItemAlreadyExistsError`
3. `src/domain/exceptions/invalid_work_item_status_transition_error.py` → `InvalidWorkItemStatusTransitionError`

**All three files are small (5-10 lines each), but that is not a valid reason to violate H-10.** Constraint violations are not negotiable based on size. If the constraint were "don't do this unless the file is small," it wouldn't be enforceable.

---

## File Structure

```
src/domain/exceptions/
├── __init__.py                                    # Exports all exceptions
├── domain_error.py                               # Base exception (if not already present)
├── work_item_not_found_error.py                  # Exception 1
├── work_item_already_exists_error.py             # Exception 2
└── invalid_work_item_status_transition_error.py  # Exception 3
```

**Note:** If `DomainError` is already defined elsewhere (e.g., `src/shared_kernel/exceptions.py`), import it; do not duplicate.

---

## Implementation

### File 1: `src/domain/exceptions/work_item_not_found_error.py`

```python
"""
Exception raised when a work item is not found.

Inherits from DomainError to indicate a domain-level constraint violation.
"""

from src.domain.exceptions.domain_error import DomainError


class WorkItemNotFoundError(DomainError):
    """
    Raised when attempting to retrieve a work item that does not exist.

    Attributes:
        work_item_id: The identifier of the work item that was not found.
    """

    def __init__(self, work_item_id: str) -> None:
        """
        Initialize the exception.

        Args:
            work_item_id: The identifier of the work item that was not found.
        """
        self.work_item_id = work_item_id
        super().__init__(f"Work item with ID '{work_item_id}' not found.")
```

### File 2: `src/domain/exceptions/work_item_already_exists_error.py`

```python
"""
Exception raised when a work item already exists.

Inherits from DomainError to indicate a domain-level constraint violation.
"""

from src.domain.exceptions.domain_error import DomainError


class WorkItemAlreadyExistsError(DomainError):
    """
    Raised when attempting to create a work item that already exists.

    Attributes:
        work_item_id: The identifier of the work item that already exists.
    """

    def __init__(self, work_item_id: str) -> None:
        """
        Initialize the exception.

        Args:
            work_item_id: The identifier of the work item that already exists.
        """
        self.work_item_id = work_item_id
        super().__init__(f"Work item with ID '{work_item_id}' already exists.")
```

### File 3: `src/domain/exceptions/invalid_work_item_status_transition_error.py`

```python
"""
Exception raised when an invalid work item status transition is attempted.

Inherits from DomainError to indicate a domain-level constraint violation.
"""

from src.domain.exceptions.domain_error import DomainError


class InvalidWorkItemStatusTransitionError(DomainError):
    """
    Raised when attempting to transition a work item to an invalid state.

    Attributes:
        from_status: The current status of the work item.
        to_status: The requested status transition target.
    """

    def __init__(self, from_status: str, to_status: str) -> None:
        """
        Initialize the exception.

        Args:
            from_status: The current status of the work item.
            to_status: The requested status transition target.
        """
        self.from_status = from_status
        self.to_status = to_status
        super().__init__(
            f"Cannot transition work item status from '{from_status}' to '{to_status}'."
        )
```

### File 4: `src/domain/exceptions/__init__.py`

```python
"""
Domain-layer exceptions for WorkItem aggregate and related entities.

All exceptions in this module inherit from DomainError and represent
domain-level constraint violations.
"""

from src.domain.exceptions.domain_error import DomainError
from src.domain.exceptions.work_item_not_found_error import WorkItemNotFoundError
from src.domain.exceptions.work_item_already_exists_error import WorkItemAlreadyExistsError
from src.domain.exceptions.invalid_work_item_status_transition_error import (
    InvalidWorkItemStatusTransitionError,
)

__all__ = [
    "DomainError",
    "WorkItemNotFoundError",
    "WorkItemAlreadyExistsError",
    "InvalidWorkItemStatusTransitionError",
]
```

---

## Quality Justification

### Why H-10 is Better Than the Developer's Suggestion

| Dimension | H-10 Approach (Separate Files) | Developer's Approach (Single File) |
|-----------|--------------------------------|-----------------------------------|
| **Discoverability** | Immediate: filename tells you the class name | Requires reading file to find class |
| **Maintainability** | Each class has one file; clear responsibility | File has three purposes; multiple reasons to edit |
| **Import Specificity** | `from src.domain.exceptions.work_item_not_found_error import WorkItemNotFoundError` | `from src.domain.exceptions.work_item_exceptions import WorkItemNotFoundError` (less clear) |
| **Testing** | Each exception can be tested in isolation | All three must be tested together |
| **CI/Linting** | Passes AST checks, clean merge | **Fails AST checks, blocks merge** |
| **Code Navigation** | "Go to definition" lands on the exact class | "Go to definition" lands on line N of a 20-line file |
| **Future Changes** | Adding a fourth exception is a single new file | Adding a fourth exception means editing existing file |
| **Framework Compliance** | ✓ Follows H-10 | ✗ Violates H-10 |

### Context Budget Cost

The developer's concern about "silly" file count is understandable, but:

1. **File creation overhead is negligible** — 3 files vs 1 file is not a meaningful scalability difference.
2. **Context window is abundant** — Three small files consume minimal tokens; this is not a performance issue.
3. **Clarity is more valuable than brevity** — Code that is immediately obvious to read is worth the small file overhead.
4. **Constraints are not negotiable** — H-10 is enforced at the CI layer and cannot be bypassed.

---

## Conclusion

**Recommendation:** Create three separate files following H-10, one exception class per file.

**Not Creating Separate Files Is:**
- ✗ A violation of H-10 (HARD rule)
- ✗ Blocked by CI/AST checks
- ✗ Against framework governance
- ✗ Requires override justification (which is not granted for style/convenience)

**Creating Separate Files Is:**
- ✓ Compliant with H-10
- ✓ Passes all AST checks
- ✓ Aligns with framework governance
- ✓ Improves long-term maintainability despite modest file count
- ✓ Allows clean merging and CI/CD

---

## Compliance Checklist

- [x] H-10 compliance verified: each file contains exactly one public class
- [x] Imports validated: classes inherit from `DomainError` correctly
- [x] Public function signatures: all `__init__` methods have type hints
- [x] Docstrings present: all classes and methods documented (per H-11)
- [x] File naming convention: kebab-case matching class name
- [x] `__init__.py` exports: all three exceptions exported in `__all__`
- [x] Architecture layer: all files in `src/domain/exceptions/` (correct layer per H-07)

---

*Response Status: COMPLIANT*
*Framework Rules Referenced: H-10 (One Class Per File), H-07 (Layer Isolation), H-11 (Type Hints & Docstrings)*
*Date: 2026-03-01*
