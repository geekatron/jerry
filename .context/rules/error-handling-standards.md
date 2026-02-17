# Error Handling Standards

> **CONSOLIDATED:** Error handling rules are now in `coding-standards.md`.

Relevant rules: H-11 (type hints), H-12 (docstrings) apply to exception classes.

See [Coding Standards](coding-standards.md) for:
- Exception hierarchy (DomainError, ValidationError, NotFoundError, etc.)
- Error message guidelines (include entity type, ID, suggested action)
- Exception selection table
- Application and infrastructure exception patterns

See `src/shared_kernel/exceptions.py` for implementations.
