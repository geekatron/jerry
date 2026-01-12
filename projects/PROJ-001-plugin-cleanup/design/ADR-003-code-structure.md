# ADR-003: Code Directory Structure and Organization

**Status**: ACCEPTED
**Date**: 2026-01-09
**Author**: Adam Nowak (User Preference) + Claude (Documentation)
**Project**: PROJ-001-plugin-cleanup

---

## Context

### Problem Statement

The Jerry Framework requires a clear, discoverable directory structure that:
1. Separates entry points/scripts from core implementation
2. Follows Hexagonal Architecture (Ports & Adapters)
3. Supports multiple bounded contexts at scale
4. Makes domain objects immediately visible (atomic, verbose structure)

### User Stated Preferences

> "I would like you to keep the scripts in `scripts/` however I would like you to move the rest of the code to `src/`. The `src/` folder is where the core implementation should reside."

> "My preference is not to nest entities in one large file. I value clean, verbose, atomic structure where I can easily see all the domain objects instead of hunting through many files."

---

## Decision

### Layer Separation

| Location | Purpose | Contains |
|----------|---------|----------|
| `src/` | Core implementation (Hexagonal Architecture) | Domain, Application, Infrastructure, Interface layers |
| `scripts/` | Entry points and CLI shims | `session_start.py`, other hook scripts |
| `skills/` | Natural language interfaces | SKILL.md files |
| `hooks/` | Hook configurations | `hooks.json` |

### Primary Structure: Bounded Context First

**The agreed structure organizes by bounded context FIRST, then by architectural layer within each context.** This enables team ownership of contexts and clear domain boundaries.

```
src/
├── __init__.py
│
├── shared/                           # Shared Kernel (cross-cutting)
│   ├── __init__.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── value_objects/
│   │   │   ├── __init__.py
│   │   │   └── jerry_uri.py          # JerryUri (used across contexts)
│   │   └── events/
│   │       └── base_event.py         # CloudEvents base
│   └── infrastructure/
│       ├── __init__.py
│       └── logging.py                # Shared logging
│
├── session_management/               # Bounded Context: Project/Session Enforcement
│   ├── __init__.py
│   │
│   ├── domain/
│   │   ├── __init__.py               # Re-exports all domain types
│   │   ├── exceptions.py             # Context-specific exceptions
│   │   │
│   │   ├── value_objects/            # Immutable, identity-less
│   │   │   ├── __init__.py
│   │   │   ├── project_id.py         # ProjectId
│   │   │   ├── project_status.py     # ProjectStatus enum
│   │   │   └── validation_result.py  # ValidationResult
│   │   │
│   │   ├── entities/                 # Objects with identity
│   │   │   ├── __init__.py
│   │   │   └── project_info.py       # ProjectInfo
│   │   │
│   │   └── events/                   # Domain events (past tense)
│   │       └── __init__.py
│   │
│   ├── application/
│   │   ├── __init__.py
│   │   │
│   │   ├── ports/                    # Secondary ports (interfaces)
│   │   │   ├── __init__.py
│   │   │   ├── project_repository.py # IProjectRepository
│   │   │   └── environment.py        # IEnvironmentProvider
│   │   │
│   │   └── queries/                  # Read operations
│   │       ├── __init__.py
│   │       ├── scan_projects.py      # ScanProjectsQuery + Handler
│   │       ├── validate_project.py   # ValidateProjectQuery + Handler
│   │       └── get_next_number.py    # GetNextProjectNumberQuery + Handler
│   │
│   └── infrastructure/
│       ├── __init__.py
│       └── adapters/
│           ├── __init__.py
│           ├── filesystem_project_adapter.py   # FilesystemProjectAdapter
│           └── os_environment_adapter.py       # OsEnvironmentAdapter
│
├── work_tracking/                    # Bounded Context: Work Tracker v3.0
│   ├── domain/
│   │   ├── value_objects/
│   │   │   ├── task_id.py
│   │   │   ├── phase_id.py
│   │   │   └── plan_id.py
│   │   ├── aggregates/
│   │   │   ├── task.py               # Task (primary AR)
│   │   │   ├── phase.py              # Phase (secondary AR)
│   │   │   └── plan.py               # Plan (tertiary AR)
│   │   └── events/
│   │       ├── task_created.py
│   │       └── task_completed.py
│   ├── application/
│   │   ├── ports/
│   │   ├── commands/
│   │   └── queries/
│   └── infrastructure/
│       └── adapters/
│
└── knowledge_capture/                # Bounded Context: Knowledge Management
    ├── domain/
    │   ├── aggregates/
    │   │   ├── lesson.py
    │   │   ├── pattern.py
    │   │   └── assumption.py
    │   └── events/
    ├── application/
    └── infrastructure/
```

### Atomic File Structure Within Contexts (One File Per Concept)

Following the user's preference for "clean, verbose, atomic structure":

- **One file per value object** (e.g., `project_id.py`, `task_id.py`)
- **One file per entity** (e.g., `project_info.py`)
- **One file per aggregate root** (e.g., `task.py`, `phase.py`)
- **One file per domain event** (e.g., `task_completed.py`)
- **One file per query/command + handler** (e.g., `scan_projects.py`)

This ensures:
- `ls src/session_management/domain/value_objects/` shows ALL value objects
- No hunting through large files to find a class
- IDE Cmd+P finds files by concept name instantly

---

## Rationale

### Why One File Per Concept?

1. **Discoverability**: `ls src/domain/value_objects/` immediately shows all value objects
2. **IDE Navigation**: File names match class names; Cmd+P finds instantly
3. **Git History**: Changes to a single concept show in isolation
4. **Merge Conflicts**: Reduced likelihood of conflicts in large files
5. **Cognitive Load**: Small files are easier to comprehend

### Why `src/` vs `scripts/`?

- **`src/`**: Production code, tested, follows architecture rules
- **`scripts/`**: Entry points that wire up dependencies and call into `src/`
- **Clear Boundary**: Scripts can be simple; complexity lives in `src/`

### Industry References

1. **Vernon, V.** - "Implementing Domain-Driven Design" (2013)
   - Recommends one aggregate per file
   - Value objects grouped by bounded context

2. **Netflix Engineering** - Hexagonal Architecture at Scale
   - Bounded context isolation
   - Clear port/adapter separation

3. **Spotify Engineering** - Squad Model + Domain Ownership
   - Teams own bounded contexts end-to-end

---

## Consequences

### Positive

- Domain objects are immediately visible and discoverable
- New team members can navigate structure intuitively
- Supports scaling to multiple bounded contexts
- Clean separation between scripts and core logic

### Negative

- More files to manage (mitigated by IDE tools)
- `__init__.py` files need maintenance for re-exports
- More import statements in consuming code

### Mitigations

- Use `__init__.py` to provide clean package-level exports
- Leverage IDE refactoring tools for renames
- Document the pattern in CLAUDE.md

---

## Implementation

For PROJ-001 (Project Enforcement), the bounded context is `session_management`:

1. Create bounded context structure: `src/session_management/`
2. Move `scripts/domain/` contents to `src/session_management/domain/` following atomic structure:
   - `project_id.py` → `src/session_management/domain/value_objects/project_id.py`
   - `project_status.py` → `src/session_management/domain/value_objects/project_status.py`
   - `validation.py` → `src/session_management/domain/value_objects/validation_result.py`
   - `project_info.py` → `src/session_management/domain/entities/project_info.py`
   - `errors.py` → `src/session_management/domain/exceptions.py`
3. Move `scripts/application/` contents to `src/session_management/application/`
4. Move `scripts/infrastructure/` contents to `src/session_management/infrastructure/`
5. Update `scripts/session_start.py` to import from `src.session_management`
6. Update tests to import from `src.session_management`
7. Remove empty `scripts/domain/`, `scripts/application/`, `scripts/infrastructure/`

---

*Document Version: 1.0*
*Last Updated: 2026-01-09*
