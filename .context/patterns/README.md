# Jerry Pattern Catalog - Executable Code Patterns

> Standalone Python pattern files for few-shot learning and code generation.
> Each file contains valid, executable Python demonstrating canonical patterns.

**Purpose**: Provide Claude with concrete code examples instead of prose descriptions.

**Last Updated**: 2026-02-16
**Pattern Count**: 6 executable Python patterns

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Pattern Files](#pattern-files) | Executable Python patterns by category |
| [How to Use](#how-to-use) | When and how to reference patterns |
| [Pattern Standards](#pattern-standards) | What makes a good pattern file |
| [Relationship to Markdown Patterns](#relationship-to-markdown-patterns) | How this complements existing docs |

---

## Pattern Files

### Core Domain Patterns

| File | Demonstrates | Key Rules |
|------|-------------|-----------|
| `value_object_pattern.py` | Frozen dataclasses, validation in `__post_init__`, factory methods | H-11 (type hints, docstrings) |
| `domain_event_pattern.py` | Past-tense naming, EVENT_TYPE, payload serialization, from_dict() factory | Immutability, `_payload()` pattern |
| `aggregate_pattern.py` | `_apply()`, `collect_events()`, factory methods, invariant enforcement | H-07 (no external imports) |

### Application Layer Patterns

| File | Demonstrates | Key Rules |
|------|-------------|-----------|
| `command_handler_pattern.py` | Command/Query classes, Handler classes, dependency injection, CQRS separation | Commands return None, Queries return DTOs |

### Infrastructure Patterns

| File | Demonstrates | Key Rules |
|------|-------------|-----------|
| `repository_pattern.py` | IRepository protocol, InMemoryRepository, FileRepository adapter, optimistic locking | H-07 (composition root only) |

### Shared Kernel Patterns

| File | Demonstrates | Key Rules |
|------|-------------|-----------|
| `exception_hierarchy_pattern.py` | DomainError base class, structured exceptions, error messages with context | Include entity type, ID, action |

---

## How to Use

### When to Reference

1. **Before creating a new class** - Check if a pattern exists for that type
2. **When implementing CQRS** - Use `command_handler_pattern.py` as template
3. **When validating value objects** - Copy `__post_init__` pattern from `value_object_pattern.py`
4. **When raising domain events** - Follow `domain_event_pattern.py` serialization approach
5. **When implementing aggregates** - Use `aggregate_pattern.py` lifecycle methods

### How to Reference

**In prompts to Claude:**
```
"Create a new value object for Email following the pattern in
.context/patterns/value_object_pattern.py"
```

**In code reviews:**
```
"Does this event class follow domain_event_pattern.py conventions?"
```

**During implementation:**
1. Read the pattern file
2. Copy the relevant section
3. Adapt to your specific domain
4. Maintain the structural conventions

---

## Pattern Standards

### What Makes a Good Pattern File

✅ **Valid Python** - Must pass `ruff check` and `mypy`
✅ **Type Hints** - All public functions (H-11)
✅ **Docstrings** - All public classes and functions (H-11)
✅ **Examples** - Docstring examples showing usage
✅ **Self-Contained** - Can be read independently
✅ **Commented** - Explain WHY, not just WHAT
✅ **Multiple Variants** - Show simple and complex cases

### File Structure Template

```python
"""
{Pattern Name} - Canonical implementation for Jerry Framework.

{Brief description of pattern and when to use it.}

References:
    - {Link to architecture-standards.md or other docs}
    - {Link to actual codebase file}
    - {External reference if applicable}

Exports:
    {What this pattern demonstrates}
"""

from __future__ import annotations

# Imports...

# =============================================================================
# Pattern 1: Simple Case
# =============================================================================

# Pattern code with docstrings and examples...

# =============================================================================
# Pattern 2: Complex Case
# =============================================================================

# More advanced variant...
```

---

## Relationship to Markdown Patterns

### Markdown Patterns (`.context/patterns/{category}/*.md`)

**Purpose**: Detailed documentation, architecture decisions, tradeoffs
**Audience**: Human readers, design reviews, onboarding
**Format**: Prose, diagrams, decision rationale
**Examples**: `cqrs/command-pattern.md`, `repository/generic-repository.md`

### Python Patterns (`.context/patterns/*.py`)

**Purpose**: Few-shot learning, code generation templates
**Audience**: Claude, automated tooling, code generation
**Format**: Executable Python with inline comments
**Examples**: `command_handler_pattern.py`, `repository_pattern.py`

### When to Use Each

| Need | Use |
|------|-----|
| Understand why we use CQRS | Read `cqrs/command-pattern.md` |
| Implement a new command handler | Copy from `command_handler_pattern.py` |
| Review aggregate design decisions | Read `aggregate/aggregate-root.md` |
| Create a new aggregate | Follow `aggregate_pattern.py` |
| Understand repository tradeoffs | Read `repository/generic-repository.md` |
| Implement a new repository | Copy from `repository_pattern.py` |

**Both are valuable** - Markdown for understanding, Python for doing.

---

## Adding New Patterns

### Criteria for New Pattern File

Add a new `.py` pattern file when:

1. ✅ Pattern is used 3+ times in codebase
2. ✅ Pattern has specific Jerry conventions (not generic Python)
3. ✅ Pattern frequently causes confusion or errors
4. ✅ Pattern has H-rules (HARD constraints) associated with it

### Process

1. Extract pattern from actual working code
2. Simplify to essential structure
3. Add 2-3 variants (simple, standard, complex)
4. Include docstring examples
5. Add to this README.md table
6. Verify with `uv run ruff check` and `uv run mypy`

### Example Candidates for Future Patterns

- `port_pattern.py` - Protocol definitions for primary/secondary ports
- `adapter_pattern.py` - Infrastructure adapter composition
- `factory_pattern.py` - Aggregate factory methods
- `snapshot_pattern.py` - Aggregate snapshotting for optimization

---

## References

| Document | Purpose |
|----------|---------|
| `.context/rules/architecture-standards.md` | Source of truth for naming conventions |
| `.context/rules/coding-standards.md` | Type hints, docstrings, error handling |
| `.context/patterns/PATTERN-CATALOG.md` | Markdown pattern index |
| `src/shared_kernel/` | Canonical implementations |
| `src/work_tracking/domain/` | Real-world aggregate examples |

---

## Maintenance

**Validation**: All pattern files MUST pass:
```bash
uv run ruff check .context/patterns/*.py
uv run mypy .context/patterns/*.py
```

**Updates**: When architecture-standards.md changes, review pattern files for alignment.

**Ownership**: Pattern files maintained by project architect (currently Claude Opus 4.6).

---

*Pattern catalog created 2026-02-16 as part of FEAT-012 Phase 1 (EN-903)*
