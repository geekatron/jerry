---
paths:
  - "src/**/*.py"
  - "tests/**/*.py"
  - "scripts/**/*.py"
  - ".context/patterns/**/*.py"
  - "hooks/**/*.py"
---

# Coding Standards

> Python coding rules, naming conventions, and error handling for Jerry.

<!-- L2-REINJECT: rank=7, tokens=60, content="Type hints REQUIRED on all public functions (H-11). Docstrings REQUIRED on all public functions/classes/modules (H-12). Google-style format." -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [HARD Rules](#hard-rules) | Coding constraints H-11, H-12 |
| [Standards (MEDIUM)](#standards-medium) | Naming, imports, docstrings, error handling |
| [Guidance (SOFT)](#guidance-soft) | Optional practices |

---

## HARD Rules

> These rules CANNOT be overridden. Violations will be blocked.

| ID | Rule | Consequence |
|----|------|-------------|
| H-11 | All public functions and methods MUST have type annotations. | mypy fails. CI blocks merge. |
| H-12 | All public functions, classes, and modules MUST have docstrings. | AST check fails. |

---

## Standards (MEDIUM)

Override requires documented justification.

### Type Hints

- `from __future__ import annotations` RECOMMENDED for forward references.
- Prefer `X | None` over `Optional[X]`, `list[T]` over `List[T]`.

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Modules | snake_case | `work_item.py` |
| Classes | PascalCase | `WorkItemRepository` |
| Functions | snake_case | `get_work_item` |
| Constants | UPPER_SNAKE | `MAX_RETRIES` |
| Private | `_prefix` | `_internal_helper` |
| Test files | `test_` prefix | `test_work_item.py` |

### Line Length

- Maximum **100 characters** RECOMMENDED. Exception: URLs in comments/docstrings.

### Imports

- Group imports: stdlib, third-party, local. Sort alphabetically within groups.
- Use absolute imports for cross-package. Use `TYPE_CHECKING` to avoid circular imports.

### Docstrings

- Google-style format PREFERRED with Args, Returns, Raises sections.

### Git Commits

- Conventional commits format RECOMMENDED: `<type>(<scope>): <subject>`.
- Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`.
- Branch naming: `feature/{id}-{desc}`, `fix/{id}-{desc}`, `release/v{ver}`.

### Error Handling

- DomainError hierarchy SHOULD be used for all domain exceptions.
- Error messages SHOULD include entity type, ID, and suggested action.
- Use `from e` when re-raising to preserve exception context.
- NEVER catch `Exception` broadly and silently swallow errors.

**Exception Hierarchy:**

| Exception | Use Case |
|-----------|----------|
| `ValidationError(field, message)` | Invalid input values |
| `NotFoundError(entity_type, entity_id)` | Entity not found |
| `InvalidStateError(entity_type, entity_id, current_state)` | Wrong state for operation |
| `InvalidStateTransitionError(current, target)` | State machine violation |
| `InvariantViolationError(invariant, message)` | Business rule violation |
| `ConcurrencyError(entity_type, entity_id, expected, actual)` | Version conflict |
| `QualityGateError(work_item_id, gate_level)` | Quality check failed |

See `src/shared_kernel/exceptions.py` for implementations.

---

## Guidance (SOFT)

*Optional best practices.*

- *`TYPE_CHECKING` pattern MAY be used to defer expensive imports.*
- *Factory `@classmethod` MAY be used on domain events for automatic timestamps.*
- *Module `__init__.py` MAY explicitly export public API via `__all__`.*
