# TD-014-E-011: Use Case Inventory

> **Research Task:** TD-014.R1
> **Date:** 2026-01-11
> **Researcher:** ps-researcher (Agent a4cf650)
> **Status:** COMPLETE

---

## Executive Summary (L0)

The Jerry Framework currently has **4 Query use cases** defined in the application layer (session_management bounded context), focused exclusively on project management functionality. There are **0 Commands** currently implemented, representing a significant gap in the application layer CQRS pattern. The CLI primary adapter needs to be built on top of these existing queries, with a clear separation of concerns: queries handle information retrieval; future commands will handle state mutations.

---

## Technical Findings (L1)

### Current Use Cases in `src/application/`

**Location**: `src/session_management/application/`

#### Queries (Read Operations - Status: IMPLEMENTED)

| Query | Purpose | Dependencies | Returns |
|-------|---------|--------------|---------|
| `GetProjectContextQuery` | Get full context for session initialization | `IProjectRepository`, `IEnvironmentProvider` | `dict` with jerry_project, project_id, validation, available_projects, next_number |
| `ScanProjectsQuery` | List all available projects | `IProjectRepository` | `list[ProjectInfo]` |
| `ValidateProjectQuery` | Validate a specific project | `IProjectRepository` | `tuple[ProjectId \| None, ValidationResult]` |
| `GetNextProjectNumberQuery` | Get next available project number | `IProjectRepository` | `int` |

**File References**:
- `src/session_management/application/queries/get_project_context.py`
- `src/session_management/application/queries/scan_projects.py`
- `src/session_management/application/queries/validate_project.py`
- `src/session_management/application/queries/get_next_number.py`
- `src/session_management/application/queries/__init__.py`

#### Commands (Write Operations - Status: NOT IMPLEMENTED)

**Current**: None

**Planned** (from WORKTRACKER.md): Future commands will support project creation and lifecycle management, referenced in `src/session_management/application/__init__.py` line 10 as "commands/: Write operations (future)"

### Secondary Ports (Infrastructure Contracts)

**Ports** (defined in `src/session_management/application/ports/`):

| Port | Purpose | Methods | Implementation |
|------|---------|---------|----------------|
| `IProjectRepository` | Project data access | `scan_projects()`, `get_project()`, `validate_project()`, `project_exists()` | `FilesystemProjectAdapter` |
| `IEnvironmentProvider` | Environment variable access | `get_env()`, `get_env_or_default()` | `OsEnvironmentAdapter` |

**Implementation Locations**:
- `src/session_management/infrastructure/adapters/filesystem_project_adapter.py`
- `src/session_management/infrastructure/adapters/os_environment_adapter.py`

### Domain Models (Supporting Entities)

The queries operate on these domain objects:

| Entity | Location | Purpose |
|--------|----------|---------|
| `ProjectInfo` | `src/session_management/domain/entities/project_info.py` | Immutable snapshot of project state |
| `ProjectId` | `src/session_management/domain/value_objects/project_id.py` | Value object: PROJ-NNN-slug format |
| `ProjectStatus` | `src/session_management/domain/value_objects/project_status.py` | Enum: UNKNOWN, DRAFT, IN_PROGRESS, COMPLETED, ARCHIVED |
| `ValidationResult` | `src/session_management/domain/value_objects/validation_result.py` | Result object with success/failure + messages |
| `Session` | `src/session_management/domain/aggregates/session.py` | Event-sourced aggregate for session lifecycle |

### CQRS Structure Analysis

**Current Pattern** (Queries Only):
```
User Input → CLI (Primary Adapter) → Query (Use Case) → Port → Adapter
```

**File Structure** (Clean Separation):
```
src/
├── session_management/
│   ├── application/
│   │   ├── queries/        # Read operations (4 queries)
│   │   └── ports/          # Infrastructure contracts
│   ├── domain/             # Business logic
│   └── infrastructure/
│       └── adapters/       # Concrete implementations
└── interface/
    └── cli/                # Primary adapters
```

### Existing CLI Usage

The queries are already being used in production:

**File**: `src/interface/cli/session_start.py`
- Uses `GetProjectContextQuery` directly (lines 167-171)
- Wires dependencies manually (lines 162-163)
- Outputs structured XML-like tags for Claude consumption (lines 76-149)

---

## Strategic Implications (L2)

### 1. CLI Exposure Readiness

**Ready for CLI**:
- `GetProjectContextQuery`: Used by session_start hook; can be exposed as `jerry init`
- `ScanProjectsQuery`: Can be exposed as `jerry list` or `jerry projects`
- `ValidateProjectQuery`: Can be exposed as `jerry validate <project-id>`
- `GetNextProjectNumberQuery`: Internal use only (supports project creation flow)

### 2. Domain Capabilities Currently Underutilized

**Work Tracking Domain** (`src/work_tracking/`):
- Has domain models (WorkItem, QualityGate, WorkItemStatus)
- Has domain ports (IRepository, IEventStore, ISnapshotStore)
- Has NO application layer (commands/queries not yet implemented)
- **Gap**: CLI cannot expose work tracking capabilities yet

### 3. Recommended CLI Command Groups

Based on existing use cases and domain capabilities:

| Command Group | Primary Use Case | Status | Domain Support |
|---------------|------------------|--------|----------------|
| `jerry init` | GetProjectContextQuery | Ready | Yes |
| `jerry projects list` | ScanProjectsQuery | Ready | Yes |
| `jerry projects validate` | ValidateProjectQuery | Ready | Yes |
| `jerry session new` | (Command TBD) | Blocked | Session.create() exists |
| `jerry session link` | (Command TBD) | Blocked | Session.link_project() exists |
| `jerry items create` | (Command TBD) | Blocked | WorkItem domain exists |
| `jerry items list` | (Query TBD) | Blocked | WorkItem domain exists |

### 4. Blocking Constraints for TD-014

1. **Critical**: Define CommandDispatcher pattern (how CLI routes to commands)
2. **Critical**: Implement response/error normalization (DTOs for CLI output)
3. **Important**: Create commands for Session lifecycle
4. **Nice-to-Have**: Create commands/queries for WorkItem (not critical for v0.0.1)

---

## Summary Table: Use Case Inventory

| Layer | Component | Count | Status | CLI Ready |
|-------|-----------|-------|--------|-----------|
| Application | Queries | 4 | Implemented | Partial |
| Application | Commands | 0 | Missing | Blocked |
| Domain | WorkItem Aggregate | 1 | Implemented | No commands |
| Domain | Session Aggregate | 1 | Implemented | Methods exist |
| Infrastructure | Adapters | 2 | Implemented | Ready |
| Infrastructure | Ports | 2 | Defined | Ready |

---

## Document Lineage

| Artifact | Relationship |
|----------|--------------|
| TD-014 | Parent tech debt item |
| DISC-006 | Broken CLI entry point discovery |
| TD-014.R2 | Sibling research (domain capabilities) |
| TD-014.R3 | Sibling research (knowledge base patterns) |
