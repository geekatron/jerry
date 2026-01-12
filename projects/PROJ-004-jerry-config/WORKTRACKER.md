# WORKTRACKER: PROJ-004-jerry-config

> **Project**: Jerry Configuration System
> **Status**: IN_PROGRESS
> **Created**: 2026-01-12
> **Branch**: PROJ-004-jerry-config

---

## Overview

Implement a configuration object for the Jerry framework to store framework and project state in `.jerry/` folders at both repository root and project levels.

### Objectives

1. Create configuration system for Jerry framework settings and state
2. Support JSON (with json5 for comments if available) serialization
3. Ensure runtime collision avoidance (file locking, atomic writes)
4. Enable worktree-safe independent state that can be merged
5. Implement env var override precedence (env > config file)
6. Token-efficient loading based on active project

---

## Phase Index

| Phase | Title | Status | Work Items |
|-------|-------|--------|------------|
| PHASE-00 | Project Setup | COMPLETED | WI-001, WI-002 |
| PHASE-01 | Research & Discovery | COMPLETED | WI-003, WI-004, WI-005, WI-006 |
| PHASE-02 | Architecture & Design | IN_PROGRESS | WI-007, WI-008 |
| PHASE-03 | Domain Implementation | PENDING | WI-009, WI-010, WI-011 |
| PHASE-04 | Infrastructure Adapters | PENDING | WI-012, WI-013, WI-014 |
| PHASE-05 | Integration & CLI | PENDING | WI-015, WI-016 |
| PHASE-06 | Testing & Validation | PENDING | WI-017, WI-018 |
| PHASE-BUGS | Bug Tracking | ONGOING | - |
| PHASE-DISCOVERY | Discoveries | ONGOING | - |
| PHASE-TECHDEBT | Technical Debt | ONGOING | - |

---

## PHASE-00: Project Setup

### WI-001: Create Project Structure

| Field | Value |
|-------|-------|
| ID | WI-001 |
| Title | Create PROJ-004 folder structure |
| Type | Task |
| Status | COMPLETED |
| Priority | HIGH |
| Created | 2026-01-12 |

#### Description
Create the project directory structure following Jerry conventions.

#### Acceptance Criteria
- [x] AC-001.1: Project folder exists at `projects/PROJ-004-jerry-config/`
- [x] AC-001.2: `.jerry/data/items/` subdirectory created
- [x] AC-001.3: Standard folders created (work, research, analysis, synthesis, decisions, reports, runbooks, reviews)
- [x] AC-001.4: Git branch `PROJ-004-jerry-config` created

#### Evidence
| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-001.1 | `mkdir -p projects/PROJ-004-jerry-config/` executed successfully | Bash tool output |
| AC-001.2 | `mkdir -p .jerry/data/items` executed successfully | Bash tool output |
| AC-001.3 | `mkdir -p {work,research,analysis,synthesis,decisions,reports,runbooks,reviews}` executed | Bash tool output |
| AC-001.4 | `git checkout -b PROJ-004-jerry-config` returned "Switched to a new branch" | Bash tool output |

#### Progress Log
| Timestamp | Update | Actor |
|-----------|--------|-------|
| 2026-01-12T10:00:00Z | Work item created | Claude |
| 2026-01-12T10:01:00Z | Branch created, directories created | Claude |
| 2026-01-12T10:02:00Z | All acceptance criteria verified, WI-001 COMPLETED | Claude |

---

### WI-002: Initialize WORKTRACKER.md

| Field | Value |
|-------|-------|
| ID | WI-002 |
| Title | Initialize WORKTRACKER.md with phases and work items |
| Type | Task |
| Status | COMPLETED |
| Priority | HIGH |
| Created | 2026-01-12 |

#### Description
Create comprehensive WORKTRACKER.md with all phases, work items, tasks, and acceptance criteria.

#### Acceptance Criteria
- [x] AC-002.1: WORKTRACKER.md exists in project root
- [x] AC-002.2: All phases documented with status
- [x] AC-002.3: Work items have acceptance criteria
- [x] AC-002.4: Evidence sections included for traceability

#### Evidence
| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-002.1 | File created at `projects/PROJ-004-jerry-config/WORKTRACKER.md` | Write tool output |
| AC-002.2 | 9 phases documented (PHASE-00 through PHASE-06 plus BUGS/DISCOVERY/TECHDEBT) | This file, Phase Index section |
| AC-002.3 | 18 work items (WI-001 through WI-018) with AC-* acceptance criteria | This file |
| AC-002.4 | Every WI has Evidence table with Criterion/Evidence/Source columns | This file |

#### Progress Log
| Timestamp | Update | Actor |
|-----------|--------|-------|
| 2026-01-12T10:02:00Z | Initial WORKTRACKER created with structure | Claude |
| 2026-01-12T10:03:00Z | Projects README.md updated with PROJ-004 entry | Claude |
| 2026-01-12T10:04:00Z | All acceptance criteria verified, WI-002 COMPLETED | Claude |

---

## PHASE-01: Research & Discovery

### WI-003: JSON5 Python Support Investigation

| Field | Value |
|-------|-------|
| ID | WI-003 |
| Title | Research JSON5 support in Python ecosystem |
| Type | Research |
| Status | COMPLETED |
| Priority | HIGH |
| Created | 2026-01-12 |
| Completed | 2026-01-12 |

#### Description
Investigate JSON5 library support in Python 3.11+ for configuration files with comments.

#### Acceptance Criteria
- [x] AC-003.1: Identify available json5 Python libraries
- [x] AC-003.2: Evaluate stdlib compatibility (no external deps for domain)
- [x] AC-003.3: Assess read/write capability
- [x] AC-003.4: Document recommendation with trade-offs

#### Evidence
| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-003.1 | `json5` (pure Python, zero deps) and `pyjson5` (Cython, fast) identified | PROJ-004-e-001, Section 1 |
| AC-003.2 | `tomllib` is stdlib in Python 3.11+ (read-only TOML); no JSON5 stdlib | PROJ-004-e-001, Section 2.1-2.2 |
| AC-003.3 | json5: read/write, pyjson5: read/write, tomllib: read-only (need tomli-w for write) | PROJ-004-e-001, Section 3 |
| AC-003.4 | **Recommendation: TOML with tomllib** - zero deps, Python ecosystem aligned | PROJ-004-e-001, L2 Section |

#### Sub-tasks
- [x] ST-003.1: Search PyPI for json5 packages
- [x] ST-003.2: Review pyjson5, json5 library docs
- [x] ST-003.3: Check if tomllib (stdlib) is a viable alternative
- [x] ST-003.4: Create research artifact with findings

#### Research Artifact
`projects/PROJ-004-jerry-config/research/PROJ-004-e-001-json5-python-support.md`

#### Key Finding
**TOML recommended over JSON5** for Jerry configuration:
- `tomllib` is stdlib (zero dependencies)
- Python ecosystem standard (pyproject.toml)
- Native comment support
- json5 is 200-6000x slower than stdlib json

---

### WI-004: Runtime Collision Avoidance Patterns

| Field | Value |
|-------|-------|
| ID | WI-004 |
| Title | Research runtime collision avoidance patterns |
| Type | Research |
| Status | COMPLETED |
| Priority | CRITICAL |
| Created | 2026-01-12 |
| Completed | 2026-01-12 |

#### Description
Research patterns for preventing runtime file collisions when multiple processes access config.

#### Acceptance Criteria
- [x] AC-004.1: Document file locking strategies (fcntl, portalocker)
- [x] AC-004.2: Evaluate atomic write patterns (write-rename)
- [x] AC-004.3: Assess lock file approaches
- [x] AC-004.4: Recommend approach for Jerry

#### Evidence
| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-004.1 | `fcntl.flock()` (BSD), `fcntl.lockf()` (POSIX recommended), `msvcrt` (Windows) documented | PROJ-004-e-002, Section 1.1-1.2 |
| AC-004.2 | Atomic write: `tempfile.mkstemp()` + `os.fsync()` + `os.replace()` pattern documented | PROJ-004-e-002, Section 1.3 |
| AC-004.3 | Lock file pattern with `O_CREAT | O_EXCL` + PID tracking + stale detection | PROJ-004-e-002, Section 1.4, 3.2 |
| AC-004.4 | **Phase 1: stdlib (fcntl.lockf + atomic writes)**, Phase 2: filelock library for Windows | PROJ-004-e-002, L2 Section |

#### Sub-tasks
- [x] ST-004.1: Research Python fcntl module
- [x] ST-004.2: Research atomic file operations
- [x] ST-004.3: Analyze existing Jerry file operations
- [x] ST-004.4: Create research artifact with findings

#### Research Artifact
`projects/PROJ-004-jerry-config/research/PROJ-004-e-002-runtime-collision-avoidance.md`

#### Key Findings
1. **Separate lock files** - Never lock data file directly
2. **Combine locking + atomic writes** - Belt and suspenders approach
3. **Use `os.replace()` not `os.rename()`** - Cross-platform atomicity
4. **OS-level locks auto-release** - On process crash, locks are freed
5. **filelock library** - Best for cross-platform if external deps allowed

---

### WI-005: Worktree-Safe State Patterns

| Field | Value |
|-------|-------|
| ID | WI-005 |
| Title | Research git worktree-safe state patterns |
| Type | Research |
| Status | COMPLETED |
| Priority | CRITICAL |
| Created | 2026-01-12 |
| Completed | 2026-01-12 |

#### Description
Research how to maintain independent state per worktree that can be safely merged.

#### Acceptance Criteria
- [x] AC-005.1: Document worktree file isolation behavior
- [x] AC-005.2: Identify merge conflict patterns for state files
- [x] AC-005.3: Design state structure for safe merging
- [x] AC-005.4: Recommend worktree-aware design

#### Evidence
| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-005.1 | Worktrees share `.git/` but have independent working trees; each has own HEAD, index | PROJ-004-e-003, Section 1 |
| AC-005.2 | Single JSON files = HIGH conflict risk; One-file-per-entity = LOW risk | PROJ-004-e-003, Section 2 |
| AC-005.3 | `.jerry/local/` (gitignored) for runtime state; `.jerry/data/events/` for committed | PROJ-004-e-003, L2 Section |
| AC-005.4 | Jerry already uses one-file-per-entity with Snowflake IDs - already merge-safe! | PROJ-004-e-003, Appendix |

#### Sub-tasks
- [x] ST-005.1: Research git worktree documentation
- [x] ST-005.2: Analyze .jerry/ placement in worktrees
- [x] ST-005.3: Design mergeable state file format
- [x] ST-005.4: Create research artifact with findings

#### Research Artifact
`projects/PROJ-004-jerry-config/research/PROJ-004-e-003-worktree-safe-state.md`

#### Key Findings
1. **Jerry already merge-safe** - Existing one-file-per-entity with Snowflake IDs
2. **Add `.jerry/local/`** - Gitignored directory for worktree-specific runtime state
3. **Separate committed vs local** - `config.json` (committed), `local/context.json` (gitignored)
4. **Materialized views are regenerable** - Can rebuild from event streams if conflicts occur

#### Recommended .jerry/ Structure
```
.jerry/
├── config.json              # Committed: shared settings
├── data/events/{id}.jsonl   # Committed: event sourcing (merge-safe)
├── data/items/{id}.json     # Committed: materialized views
└── local/                   # GITIGNORED: worktree-local
    ├── context.json         # Active project, session
    ├── locks/               # File locks
    └── cache/               # Regenerable data
```

---

### WI-006: Configuration Precedence Investigation

| Field | Value |
|-------|-------|
| ID | WI-006 |
| Title | Research configuration precedence patterns |
| Type | Research |
| Status | COMPLETED |
| Priority | HIGH |
| Created | 2026-01-12 |
| Completed | 2026-01-12 |

#### Description
Research best practices for layered configuration with environment variable overrides.

#### Acceptance Criteria
- [x] AC-006.1: Document precedence patterns (env > file > defaults)
- [x] AC-006.2: Review existing Jerry env var usage
- [x] AC-006.3: Design override mechanism
- [x] AC-006.4: Document configuration loading order

#### Evidence
| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-006.1 | CLI > Env > Project Config > Root Config > Defaults (12-factor aligned) | PROJ-004-e-004, Section 1 |
| AC-006.2 | `JERRY_PROJECT`, `CLAUDE_PROJECT_DIR`, `ECW_DEBUG` currently used via direct os.environ.get() | PROJ-004-e-004, Section 2 |
| AC-006.3 | Double-underscore (`__`) for nested paths: `JERRY_LOGGING__LEVEL` → `logging.level` | PROJ-004-e-004, Section 4 |
| AC-006.4 | Env vars → Project .jerry/config.json → Root .jerry/config.json → Code defaults | PROJ-004-e-004, L2 Section |

#### Research Artifact
`projects/PROJ-004-jerry-config/research/PROJ-004-e-004-config-precedence.md`

#### Key Findings
1. **12-factor app aligned** - Environment variables override config files
2. **Existing port abstraction** - `IEnvironmentProvider` exists, extend to `IConfigurationProvider`
3. **Nested override pattern** - Use `__` separator for nested config paths
4. **Type conversion** - Auto-parse bool/int/float/JSON from string env vars
5. **pydantic-settings compatible** - Design allows future upgrade if needed

---

## PHASE-02: Architecture & Design

### WI-007: Create PLAN.md

| Field | Value |
|-------|-------|
| ID | WI-007 |
| Title | Create comprehensive PLAN.md |
| Type | Task |
| Status | COMPLETED |
| Priority | HIGH |
| Created | 2026-01-12 |
| Completed | 2026-01-12 |

#### Description
Create implementation plan based on research findings.

#### Acceptance Criteria
- [x] AC-007.1: PLAN.md exists in project root
- [x] AC-007.2: Architecture decisions documented
- [x] AC-007.3: Implementation phases detailed
- [x] AC-007.4: Risk mitigation addressed

#### Evidence
| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-007.1 | File created at `projects/PROJ-004-jerry-config/PLAN.md` | Write tool output |
| AC-007.2 | Key Decisions table + Hexagonal Architecture diagram | PLAN.md, Architecture Overview |
| AC-007.3 | 3 implementation phases with code examples | PLAN.md, Implementation Phases |
| AC-007.4 | Risk table with probability/impact/mitigation | PLAN.md, Risk Mitigation |

#### Key Deliverables
- Research synthesis from 4 ps-researcher artifacts
- Directory structure design for `.jerry/`
- Configuration schema (TOML format)
- Environment variable mapping
- Hexagonal architecture diagram
- Code examples for domain/infrastructure layers
- Testing strategy with coverage targets

---

### WI-008: Domain Model Design

| Field | Value |
|-------|-------|
| ID | WI-008 |
| Title | Design configuration domain model |
| Type | Task |
| Status | PENDING |
| Priority | HIGH |
| Created | 2026-01-12 |

#### Description
Design domain entities, value objects, and aggregates for configuration.

#### Acceptance Criteria
- [ ] AC-008.1: Configuration aggregate designed
- [ ] AC-008.2: Value objects identified (ConfigPath, ConfigKey, etc.)
- [ ] AC-008.3: Domain events defined
- [ ] AC-008.4: Repository port interface defined

---

## PHASE-03: Domain Implementation

### WI-009: Configuration Value Objects

| Field | Value |
|-------|-------|
| ID | WI-009 |
| Title | Implement configuration value objects |
| Type | Task |
| Status | PENDING |
| Priority | HIGH |
| Created | 2026-01-12 |

#### Description
Implement immutable value objects for configuration domain.

#### Acceptance Criteria
- [ ] AC-009.1: ConfigPath value object implemented
- [ ] AC-009.2: ConfigKey value object implemented
- [ ] AC-009.3: ConfigValue value object implemented
- [ ] AC-009.4: Unit tests pass at 90%+ coverage

---

### WI-010: Configuration Aggregate

| Field | Value |
|-------|-------|
| ID | WI-010 |
| Title | Implement Configuration aggregate root |
| Type | Task |
| Status | PENDING |
| Priority | HIGH |
| Created | 2026-01-12 |

#### Description
Implement the Configuration aggregate with domain logic.

#### Acceptance Criteria
- [ ] AC-010.1: Configuration aggregate implemented
- [ ] AC-010.2: Invariants enforced
- [ ] AC-010.3: Domain events raised
- [ ] AC-010.4: Unit tests pass

---

### WI-011: Configuration Domain Events

| Field | Value |
|-------|-------|
| ID | WI-011 |
| Title | Implement configuration domain events |
| Type | Task |
| Status | PENDING |
| Priority | MEDIUM |
| Created | 2026-01-12 |

#### Description
Implement domain events for configuration changes.

#### Acceptance Criteria
- [ ] AC-011.1: ConfigurationLoaded event
- [ ] AC-011.2: ConfigurationUpdated event
- [ ] AC-011.3: ProjectActivated event
- [ ] AC-011.4: Unit tests pass

---

## PHASE-04: Infrastructure Adapters

### WI-012: JSON File Adapter

| Field | Value |
|-------|-------|
| ID | WI-012 |
| Title | Implement JSON configuration file adapter |
| Type | Task |
| Status | PENDING |
| Priority | HIGH |
| Created | 2026-01-12 |

#### Description
Implement infrastructure adapter for JSON file persistence.

#### Acceptance Criteria
- [ ] AC-012.1: Read configuration from JSON file
- [ ] AC-012.2: Write configuration with atomic operations
- [ ] AC-012.3: File locking implemented
- [ ] AC-012.4: Integration tests pass

---

### WI-013: Environment Adapter

| Field | Value |
|-------|-------|
| ID | WI-013 |
| Title | Implement environment variable adapter |
| Type | Task |
| Status | PENDING |
| Priority | HIGH |
| Created | 2026-01-12 |

#### Description
Implement adapter for reading configuration from environment variables.

#### Acceptance Criteria
- [ ] AC-013.1: Read JERRY_* environment variables
- [ ] AC-013.2: Parse values correctly
- [ ] AC-013.3: Override config file values
- [ ] AC-013.4: Integration tests pass

---

### WI-014: Configuration Loader Service

| Field | Value |
|-------|-------|
| ID | WI-014 |
| Title | Implement configuration loader application service |
| Type | Task |
| Status | PENDING |
| Priority | HIGH |
| Created | 2026-01-12 |

#### Description
Implement application service that orchestrates configuration loading with precedence.

#### Acceptance Criteria
- [ ] AC-014.1: Load from default locations
- [ ] AC-014.2: Apply environment overrides
- [ ] AC-014.3: Return merged configuration
- [ ] AC-014.4: Handle missing files gracefully

---

## PHASE-05: Integration & CLI

### WI-015: Update session_start.py Hook

| Field | Value |
|-------|-------|
| ID | WI-015 |
| Title | Update session_start.py to use configuration system |
| Type | Task |
| Status | PENDING |
| Priority | HIGH |
| Created | 2026-01-12 |

#### Description
Integrate configuration system into session start hook.

#### Acceptance Criteria
- [ ] AC-015.1: Load configuration at session start
- [ ] AC-015.2: Use config for project resolution
- [ ] AC-015.3: Maintain backward compatibility with JERRY_PROJECT
- [ ] AC-015.4: E2E tests pass

---

### WI-016: CLI Config Commands

| Field | Value |
|-------|-------|
| ID | WI-016 |
| Title | Implement jerry config CLI commands |
| Type | Task |
| Status | PENDING |
| Priority | MEDIUM |
| Created | 2026-01-12 |

#### Description
Add CLI commands for managing configuration.

#### Acceptance Criteria
- [ ] AC-016.1: `jerry config show` command
- [ ] AC-016.2: `jerry config set` command
- [ ] AC-016.3: `jerry config path` command
- [ ] AC-016.4: CLI tests pass

---

## PHASE-06: Testing & Validation

### WI-017: Architecture Tests

| Field | Value |
|-------|-------|
| ID | WI-017 |
| Title | Add architecture tests for configuration module |
| Type | Task |
| Status | PENDING |
| Priority | HIGH |
| Created | 2026-01-12 |

#### Description
Ensure configuration follows hexagonal architecture boundaries.

#### Acceptance Criteria
- [ ] AC-017.1: Domain has no infrastructure imports
- [ ] AC-017.2: Ports correctly defined
- [ ] AC-017.3: Adapters implement ports
- [ ] AC-017.4: All architecture tests pass

---

### WI-018: Integration & E2E Tests

| Field | Value |
|-------|-------|
| ID | WI-018 |
| Title | Create integration and E2E test suite |
| Type | Task |
| Status | PENDING |
| Priority | HIGH |
| Created | 2026-01-12 |

#### Description
Comprehensive test coverage for configuration system.

#### Acceptance Criteria
- [ ] AC-018.1: Integration tests for file adapter
- [ ] AC-018.2: Integration tests for env adapter
- [ ] AC-018.3: E2E tests for CLI commands
- [ ] AC-018.4: 90%+ code coverage

---

## PHASE-BUGS: Bug Tracking

| ID | Title | Status | Severity | Found In | Fixed In |
|----|-------|--------|----------|----------|----------|
| - | No bugs recorded yet | - | - | - | - |

---

## PHASE-DISCOVERY: Discoveries

| ID | Discovery | Impact | Found In | Action |
|----|-----------|--------|----------|--------|
| - | No discoveries yet | - | - | - |

---

## PHASE-TECHDEBT: Technical Debt

| ID | Description | Priority | Created | Resolved |
|----|-------------|----------|---------|----------|
| - | No tech debt recorded yet | - | - | - |

---

## Changelog

| Date | Change | Author |
|------|--------|--------|
| 2026-01-12 | Initial WORKTRACKER created | Claude |
| 2026-01-12 | PHASE-00 completed (WI-001, WI-002) | Claude |
| 2026-01-12 | Projects README.md updated with PROJ-004 registration | Claude |
| 2026-01-12 | PHASE-01 research completed via ps-researcher agents | Claude |
| 2026-01-12 | WI-003: JSON5 research complete - TOML recommended | Claude |
| 2026-01-12 | WI-004: Runtime collision patterns documented | Claude |
| 2026-01-12 | WI-005: Worktree-safe state patterns documented | Claude |
| 2026-01-12 | WI-006: Config precedence patterns documented | Claude |
| 2026-01-12 | 4 research artifacts created in research/ folder | Claude |
| 2026-01-12 | WI-007: PLAN.md created with architecture synthesis | Claude |
| 2026-01-12 | PHASE-02 started, WI-007 COMPLETED | Claude |
