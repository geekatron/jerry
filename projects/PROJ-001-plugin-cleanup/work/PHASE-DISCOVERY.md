# Phase DISCOVERY: Technical Discoveries

> **Status**: 🔄 ONGOING
> **Purpose**: Track technical discoveries, insights, and findings during implementation work.

---

## Navigation

| Link | Description |
|------|-------------|
| [← WORKTRACKER](../WORKTRACKER.md) | Back to index |
| [BUGS](PHASE-BUGS.md) | Bug tracking |
| [TECHDEBT](PHASE-TECHDEBT.md) | Technical debt |
| [INITIATIVE-WT-SKILLS](INITIATIVE-WORKTRACKER-SKILLS.md) | Related initiative |

---

## Discovery Summary

| ID | Title | Status | Related |
|----|-------|--------|---------|
| DISC-001 | ProjectId Already Extends VertexId | ACTIONED | 008d.1 |
| DISC-002 | ProjectInfo EntityBase Design Tension | ACTIONED | 008d.2 |
| DISC-003 | link-artifact CLI Missing | ELEVATED | TD-010 |
| DISC-004 | ps-* Orchestration Validates Composed Architecture | ACTIONED | INIT-WT-SKILLS |
| DISC-005 | Release Pipeline Missing from CI/CD | ELEVATED | TD-013 |
| DISC-006 | Broken CLI Entry Point in pyproject.toml | ELEVATED | TD-014 |
| DISC-007 | TD-013 Misunderstood Distribution Model | REVISED | TD-013 |
| DISC-008 | System Python vs Venv Portability | ACTIONED | TD-014 |
| DISC-009 | New Files Created Without Format Check | ACTIONED | TD-013.6 |
| DISC-010 | Release Workflow Missing Dev Dependencies | ACTIONED | TD-013.6 |
| DISC-011 | Architecture Pattern Research Initiative | COMPLETED | BUG-006, TD-015 |
| DISC-012 | TOON Format Required as Primary Output | ACTIONED | ADR-CLI-001, TD-015 |
| DISC-013 | CLI Namespaces per Bounded Context | ACTIONED | ADR-CLI-001, TD-015 |
| DISC-014 | Domain Events Use aggregate_id Not Entity-Specific ID | ACTIONED | Phase 4.3.8 |
| DISC-015 | Phase 4.5 Requires Event Sourcing for Mission-Critical Reliability | ACTIONED | TD-018, Phase 4.6 |
| DISC-016 | InMemoryWorkItemRepository is Simplified, Not Event-Sourced | LOGGED | TD-018 |
| DISC-017 | RuntimeWarning When Running CLI with -m Flag | LOGGED | Phase 4.6.1 |
| DISC-018 | CommandDispatcher Not Implemented - Dict-Based Workaround Used | LOGGED | Phase 4.6.2, TD-018 |
| DISC-019 | InMemoryEventStore Not Persistent - Events Lost on Restart | ACTIONED | TD-018 (FileSystemEventStore), TD-019 (SQLite future) |
| DISC-020 | CreateWorkItemCommandHandler Expects Numeric parent_id | LOGGED | Phase 4.5.5 |

---

## Discovery Log

### Format

Each discovery follows this format:

```
### DISC-{nnn}: {Title}

**Date**: YYYY-MM-DD
**Context**: {Where/how this was discovered}
**Finding**: {What was discovered}
**Impact**: {How this affects the project}
**Action**: {What should be done, if anything}
**Status**: LOGGED | INVESTIGATED | ACTIONED | ARCHIVED
```

---

## Active Discoveries

### DISC-001: ProjectId Already Extends VertexId

**Date**: 2026-01-10
**Context**: Starting 008d.1.1 (ProjectId VertexId compliance), reviewed current implementation
**Finding**: `src/session_management/domain/value_objects/project_id.py` already extends `VertexId`:
- Line 23: `from src.shared_kernel.vertex_id import VertexId`
- Line 36: `class ProjectId(VertexId):`
- Implements `_is_valid_format()`, `from_string()`, `generate()` (raises NotImplementedError)
- Has `number` and `slug` convenience properties (lines 204-228)

**Impact**: 008d.1 (Value Object Refactoring) is FULLY COMPLETE:
- 008d.1.1: VertexId compliance (10 tests) ✅
- 008d.1.2: number/slug properties (5 tests) ✅
- 008d.1.3: Format + Edge case tests (21 tests) ✅
- Total: 36 tests all passing

**Action**: Mark 008d.1 as complete, proceed to 008d.2 (Entity Refactoring)
**Status**: ACTIONED

### DISC-002: ProjectInfo EntityBase Design Tension

**Date**: 2026-01-10
**Context**: Starting 008d.2 (ProjectInfo extends EntityBase), reviewed both implementations
**Finding**: Design tension between R-008d and current implementation:
- R-008d specifies: "ProjectInfo extends EntityBase"
- Current ProjectInfo: `@dataclass(frozen=True, slots=True)` - immutable snapshot
- EntityBase: Mutable, has `_touch()` and `_increment_version()` methods
- These are incompatible: frozen dataclass cannot have mutation methods

**Options**:
1. Make ProjectInfo mutable (extend EntityBase, lose immutability)
2. Keep ProjectInfo frozen (add audit fields directly, don't extend EntityBase)
3. Create ImmutableEntityBase variant (new base class)

**Analysis (Distinguished Engineer)**:
- ProjectInfo is described as "immutable snapshot" - this is VALUE OBJECT pattern
- Entities typically have identity AND mutable state
- ProjectInfo acts more like a read-only projection than a mutable entity
- Changing to mutable would break existing code expecting frozen behavior

**Decision**: Option 2 - Add audit metadata directly to ProjectInfo without extending EntityBase.
This preserves immutability guarantees and backward compatibility.

**Impact**: R-008d revision applied - ProjectInfo does NOT extend EntityBase
**Action**: Implemented audit fields on frozen ProjectInfo, updated tests (35 pass)
**Status**: ACTIONED

### DISC-003: link-artifact CLI Command Does Not Exist

**Date**: 2026-01-11
**Context**: Preparing to execute INIT-WT-SKILLS orchestration with ps-* agents
**Finding**: All 8 ps-* agents reference `python3 scripts/cli.py link-artifact` in their MANDATORY PERSISTENCE protocol, but this command does not exist:
- `scripts/cli.py` does not exist (only `scripts/session_start.py` found)
- `src/**/cli*.py` pattern returns no matches
- `link-artifact` is referenced in 25 files:
  - 8 ps-* agent definitions
  - 1 PS_AGENT_TEMPLATE.md
  - 6 template files in `docs/knowledge/exemplars/templates/`
  - 1 orchestration doc
  - 9 aspiration/archive files

**Scope of References**:
```
skills/problem-solving/agents/*.md (9 files)
docs/knowledge/exemplars/templates/*.md (6 files)
skills/problem-solving/docs/ORCHESTRATION.md
docs/knowledge/DISCOVERIES_EXPANDED.md
projects/archive/**/*.md (2 files)
docs/knowledge/dragonsbelurkin/**/*.md (5 files)
```

**Impact**:
- ps-* agents cannot complete their mandatory persistence protocol as designed
- Artifact linking is aspirational, not functional
- Orchestration dependent on non-existent infrastructure

**Action**: Created TD-010 to implement `scripts/cli.py link-artifact` command
**Status**: LOGGED → Elevated to TECHDEBT (TD-010)

---

### DISC-004: ps-* Agent Orchestration Validates Composed Architecture

**Date**: 2026-01-11
**Context**: Executing INIT-WT-SKILLS research initiative using ps-* agents
**Finding**: Successfully orchestrated 10 ps-* agent invocations in a fan-out/fan-in pattern:

| Phase | Pattern | Agents | Result |
|-------|---------|--------|--------|
| 1 | Fan-out | 4 ps-researcher | 4 research docs |
| 2 | Fan-in | 2 ps-analyst | 2 analysis docs |
| 3 | Sequential | 1 ps-synthesizer | 1 synthesis |
| 4-6 | Parallel | 3 agents (architect, validator, reviewer) | ADR + validation + review |

**Key Observations**:
1. **API Resilience**: 3 agents failed with connection errors but successfully relaunched
2. **Artifact Quality**: All 11 documents produced with L0/L1/L2 structure
3. **P-003 Compliance**: Single-level nesting maintained throughout
4. **Context Efficiency**: ~3,000 tokens per agent vs 12,000+ for monolithic approach

**Evidence**:
- Trade-off analysis scored Option C (Composed) at 8.60/10
- 4,345 lines of research artifacts committed (`cd91d0b`)
- Synthesis approved with 5/5 quality rating

**Impact**: Validates that Composed Architecture (Option C) is viable for worktracker skill enhancement.

**Related**:
- ADR: `decisions/ADR-INIT-WT-SKILLS-composed-architecture.md`
- Synthesis: `synthesis/init-wt-skills-e-007-unified-synthesis.md`
- Initiative: `work/INITIATIVE-WORKTRACKER-SKILLS.md`

**Status**: ACTIONED (informs implementation roadmap)

---

### DISC-005: Release Pipeline Missing from CI/CD

**Date**: 2026-01-11
**Context**: User review of CI-002 completion; comparing ADR-CI-001 stated intent vs implementation
**Finding**: ADR-CI-001 explicitly states intent to release Jerry publicly but defines no release mechanism:

**Evidence from ADR-CI-001**:
- Line 96: *"Jerry will be released publicly; vulnerable dependencies are unacceptable."*
- Line 109: *"Portability assured - Matrix testing catches Python version issues"*
- Line 72: Rationale for Python matrix: *"Jerry will be released for others to use"*

**What Exists**:
- Pre-commit hooks (Layer 1) ✅
- GitHub Actions CI (Layer 2) ✅
  - Lint & Format ✅
  - Type Check ✅
  - Security Scan ✅
  - Test Matrix (3.11-3.14) ✅
  - Coverage Report ✅

**What is Missing**:
- No release workflow in `.github/workflows/`
- No artifact generation (binaries, wheels)
- No GitHub Releases integration
- No cross-platform distribution strategy (user requirement: macOS + Windows)

**User Requirements** (2026-01-11):
- GitHub Releases (not PyPI at this time)
- Downloadable artifacts for macOS and Windows
- Distribution to friends without requiring Python installation

**Impact**:
- Users cannot install Jerry without cloning the repo
- No versioned releases for distribution
- No cross-platform binaries for non-Python users
- ADR-CI-001 stated intent unfulfilled

**Action**: Created TD-013 to implement GitHub Releases pipeline
**Status**: LOGGED → Elevated to TECHDEBT (TD-013) → REVISED by DISC-007

---

### DISC-006: Broken CLI Entry Point in pyproject.toml

**Date**: 2026-01-11
**Context**: Investigating TD-013 release pipeline; checked pyproject.toml for entry points
**Finding**: pyproject.toml defines CLI entry points that do not exist:

**Evidence from pyproject.toml (lines 46-48)**:
```toml
[project.scripts]
jerry = "src.interface.cli.main:main"          # ← FILE DOES NOT EXIST
jerry-session-start = "src.interface.cli.session_start:main"  # ← EXISTS
```

**Verification**:
```bash
$ ls src/interface/cli/
__init__.py  session_start.py  # NO main.py
```

**Impact**:
- `pip install jerry` or `pip install -e .` will **FAIL** when creating console scripts
- Package is fundamentally broken - cannot be installed
- Violates regression-free principle (P-REGRESS)
- Interface layer (Primary Adapters) is architecturally incomplete

**Hexagonal Architecture Violation**:
The CLI is a **Primary Adapter** (drives the application). Its absence means:
- Domain layer exists ✅
- Application layer (Use Cases) exists ✅
- Infrastructure layer (Secondary Adapters) exists ✅
- **Interface layer (Primary Adapters) is INCOMPLETE** ❌

**Relationship to DISC-003**:
- DISC-003 identified `link-artifact` CLI command missing
- DISC-006 identifies the **entire CLI entry point** missing
- DISC-003 is a subset of DISC-006

**Action**: Created TD-014 to implement CLI following Hexagonal Architecture
**Status**: LOGGED → Elevated to TECHDEBT (TD-014)

---

### DISC-007: TD-013 Misunderstood Distribution Model

**Date**: 2026-01-11
**Context**: User clarification during TD-013 planning
**Finding**: TD-013 was designed for Python package distribution (PyInstaller binaries), but Jerry is a **Claude Code Plugin**, not a standalone application.

**Original (Incorrect) Understanding**:
- Distribute standalone binaries via PyInstaller
- Target macOS and Windows executables
- Users download and run `jerry` CLI

**Correct Understanding**:
- Jerry is a **Claude Code Plugin**
- Distribution is the plugin structure itself:
  - `.claude/` (hooks, agents, rules)
  - `skills/` (natural language interfaces)
  - `CLAUDE.md` (context)
  - `src/` (hexagonal core)
- Users clone/install the plugin into their Claude Code environment
- The `jerry` CLI is for **internal tooling**, not end-user distribution

**Impact on TD-013**:
- Remove PyInstaller approach
- Focus on GitHub Releases with plugin archive
- Release artifacts: `.tar.gz`/`.zip` of plugin structure
- Documentation for Claude Code Plugin installation

**Action**: Revise TD-013 to reflect Claude Code Plugin distribution model
**Status**: REVISED

---

### DISC-008: System Python vs Venv Portability

**Date**: 2026-01-12
**Context**: Testing TD-014 CLI implementation, using `python3` directly instead of venv
**Finding**: Testing and development must use the project venv at `.venv/bin/python3` to ensure:
- Consistent Python version (macOS system Python may differ)
- All dependencies available (project deps installed in venv)
- Portability across macOS/Linux/Windows
- Reproducible CI behavior

**Evidence**:
- Project uses `.venv/` for virtual environment
- `pyproject.toml` specifies `requires-python = ">=3.11"`
- macOS system Python may be different version
- CI/CD runs in isolated environments with installed deps

**Impact**:
- Using `python3` directly may work but is not portable
- Dependencies may be missing in system Python
- Tests may behave differently than CI

**Correct Commands**:
```bash
# Use venv Python
.venv/bin/python3 -m src.interface.cli.main --help

# Or activate venv first
source .venv/bin/activate && python3 -m src.interface.cli.main --help
```

**Action**: Always use `.venv/bin/python3` for testing and development
**Status**: ACTIONED (using venv for TD-014 testing)

---

### DISC-009: New Files Created Without Format Check

**Date**: 2026-01-12
**Context**: TD-013.6 release verification - first release attempt failed at format check
**Finding**: When creating `src/interface/cli/main.py` during TD-014, the file was not run through `ruff format` before committing. This caused the release workflow to fail at the "Run format check" step.

**Evidence**:
GitHub Actions logs from release run `20906566599`:
```
Would reformat: src/interface/cli/main.py
1 file would be reformatted, 162 files already formatted
##[error]Process completed with exit code 1.
```

**Root Cause**:
- File was created using the Write tool
- No automatic format check before commit
- Pre-commit hooks exist but weren't run (direct commit)

**Pattern Identified**:
When creating new Python files, must run:
```bash
.venv/bin/ruff format <file>
.venv/bin/ruff check <file> --fix
```

**Impact**:
- Release workflow failed
- Required tag deletion and recreation
- Delayed v0.0.1 release

**Action**: Fixed by running `ruff format src/interface/cli/main.py` and committing the formatted version.

**Lesson Learned**: Always run format/lint checks on new files before committing, especially when bypassing pre-commit hooks.

**Status**: ACTIONED

---

### DISC-010: Release Workflow Missing Dev Dependencies

**Date**: 2026-01-12
**Context**: TD-013.6 release verification - second release attempt failed at type check
**Finding**: The release workflow's CI job installed `pip install -e ".[test]"` but pyright requires `filelock` which is in the `[dev]` dependencies, not `[test]`.

**Evidence**:
GitHub Actions logs from release run `20906593992`:
```
venv .venv subdirectory not found in venv path /home/runner/work/jerry/jerry.
/home/runner/work/jerry/jerry/src/infrastructure/internal/file_store.py:24:10 - error: Import "filelock" could not be resolved (reportMissingImports)
/home/runner/work/jerry/jerry/src/infrastructure/internal/file_store.py:25:10 - error: Import "filelock" could not be resolved (reportMissingImports)
2 errors, 0 warnings, 0 informations
```

**Root Cause**:
- `filelock` is in `[dev]` optional dependencies
- Release workflow CI job only installed `[test]`
- pyproject.toml dependency groups:
  ```toml
  [project.optional-dependencies]
  dev = ["filelock>=3.18.0", "mypy>=1.14.0", "ruff>=0.9.2"]
  test = ["pytest>=8.0", "pytest-cov>=7.0", ...]
  ```

**Impact**:
- Type check job failed
- Release workflow blocked
- Required workflow fix and tag recreation

**Fix Applied**:
Changed line 77 in `.github/workflows/release.yml`:
```yaml
# From:
pip install -e ".[test]"

# To:
pip install -e ".[dev,test]"
```

**Lesson Learned**: When creating CI workflows that run type checking, ensure all dependencies required by the type checker are installed. The main `ci.yml` already had this correct (`pip install -e ".[dev]"` on line 66), but the release workflow was written separately and didn't follow the same pattern.

**Consistency Check Added to Checklist**:
- [ ] New workflows should match dependency installation patterns from existing workflows

**Status**: ACTIONED

---

### DISC-011: Architecture Pattern Research Initiative

**Date**: 2026-01-12
**Context**: BUG-006 identified critical CQRS/Hexagonal Architecture violation in CLI adapter
**Finding**: Comprehensive research completed using 5 parallel agents.

**Research Results**:

| Agent | Focus | Key Finding |
|-------|-------|-------------|
| Dispatcher | `src/**/*.py` | **No Dispatcher exists** - queries execute themselves |
| Architecture Docs | `projects/*/research/`, `decisions/` | 25+ patterns documented, extensive prior art |
| Knowledge Patterns | `docs/knowledge/`, `docs/design/` | 14 pattern categories, Teaching Edition as reference |
| Application Layer | `src/*/application/` | 4 Queries exist, 0 Handlers - queries are self-executing |
| Adapter Violations | `src/interface/cli/` | CLI uses "Poor Man's DI" (Factory Composition Root) |

**Critical Findings**:

1. **No Dispatcher Pattern**: Current architecture uses "Query Object" pattern where queries instantiate their own dependencies and execute themselves.

2. **"Poor Man's DI" Identified**: The current CLI implementation wires infrastructure adapters directly in the adapter layer. This was initially assessed as "compliant" but **user clarified this is NOT acceptable**.

3. **Correct Pattern Required**: Adapter → Dispatcher → Handler → Query chain is MANDATORY per user requirements.

**User Clarification (Verbatim)**:
> "To us this is a shortcut. We will not take a 'Poor Man's DI' approach as that violates our principles of clean architecture. This is a hard requirement for us."

**Synthesis Output**:
Created `docs/design/PYTHON-ARCHITECTURE-STANDARDS.md` documenting:
- CQRS Pattern (Dispatcher → Handler → Query/Command)
- CLI Standards (thin adapter, receives dispatcher)
- Port Design (Use Cases, not interfaces)
- Adapter Boundaries (what MAY/MAY NOT do)

**Related Documents Updated**:
- `ADR-CLI-001-primary-adapter.md`: D2 REJECTED, D2-AMENDED added
- `PHASE-BUGS.md`: BUG-006 Research Assessment added
- `PHASE-TECHDEBT.md`: TD-015 created

**Action**: Research complete, TD-015 created for remediation
**Status**: COMPLETED

---

### DISC-012: TOON Format Required as Primary Output

**Date**: 2026-01-12
**Context**: User clarified output format priorities during DISC-011 research
**Finding**: TOON (Token-Object Oriented Notation) is required as the PRIMARY output format for all CLI commands.

**User Requirements**:
- TOON default (`--toon` or no flag)
- JSON secondary (`--json`)
- Human-readable tertiary (`--human`)

**Research Found**:
| Location | Document |
|----------|----------|
| `projects/archive/research/TOON_FORMAT_ANALYSIS.md` | Comprehensive spec analysis |
| `projects/PROJ-001-plugin-cleanup/research/impl-es-e-002-toon-serialization.md` | Implementation guide |
| PyPI | `python-toon` package available |

**Token Efficiency**:
- 30-60% token reduction vs JSON
- 4% accuracy improvement in LLM comprehension
- Ideal for tabular/array data

**Decision Matrix**:
| Data Type | Format |
|-----------|--------|
| Tabular arrays | TOON |
| Deeply nested objects | JSON |
| Human readable | Human-formatted text |

**Action**: Added TOON to ADR-CLI-001 D5 amendment, included in TD-015 Phase 5
**Status**: ACTIONED

---

### DISC-013: CLI Namespaces per Bounded Context

**Date**: 2026-01-12
**Context**: User specified CLI architecture requirements during DISC-011 discussion
**Finding**: Each bounded context MUST have its own CLI subcommand namespace.

**User Requirements (Verbatim)**:
> "It should have its own CLI subcommand namespace (aka Separate CLI Subcommand Namespaces). This mirrors: Bounded Contexts, Authorization scopes, Threat models"

**Required Namespaces**:
```
jerry session <command>      # Session Management BC
jerry worktracker <command>  # Work Tracker BC
jerry projects <command>     # Project Management BC
```

**Architecture Rules**:
1. **CLI is a Primary Adapter**: Translates user intent → use case invocation
2. **CLI NEVER contains business logic**
3. **CLI NEVER knows infrastructure details**
4. **Ports represent Use Cases, NOT interfaces**
5. **Each namespace routes to distinct application port**

**Relationship to Authorization**:
- Each bounded context = separate authorization boundary
- CLI namespace structure mirrors security model
- Future: role-based access per namespace

**Action**: Added to ADR-CLI-001 D6 (NEW), included in TD-015 Phase 4
**Status**: ACTIONED

---

### DISC-014: Domain Events Use aggregate_id Not Entity-Specific ID

**Date**: 2026-01-12
**Context**: Phase 4.3.8 CLI adapter integration, extracting session ID from events
**Finding**: Domain events inherit from `DomainEvent` base class and store entity identity in `aggregate_id`, not entity-specific fields like `session_id`.

**Evidence from session_events.py**:
```python
@dataclass(frozen=True)
class SessionCreated(DomainEvent):
    # Session ID is in aggregate_id, NOT a separate session_id field
    description: str = ""
    project_id: str | None = None
```

**Impact**:
- CLI adapter initially tried `events[0].session_id` - AttributeError
- Correct pattern: `events[0].aggregate_id`
- This is consistent with event sourcing pattern (aggregate_id identifies the stream)
- All CLI command outputs should use `aggregate_id` for entity identification

**Pattern Documentation**:
- `DomainEvent.aggregate_id` → The entity's identity (SessionId, WorkItemId, etc.)
- `DomainEvent.aggregate_type` → The entity type ("Session", "WorkItem", etc.)
- `DomainEvent.version` → Event version in the aggregate's stream

**Action**: Fixed in adapter.py, documented pattern for future CLI integrations
**Status**: ACTIONED

---

### DISC-015: Phase 4.5 Requires Event Sourcing for Mission-Critical Reliability

**Date**: 2026-01-12
**Context**: Planning Phase 4.5 (Items Commands) after completing Phase 4.4 (Items Queries)
**Finding**: Phase 4.5 implements write operations (`jerry items create`, `jerry items start`, `jerry items complete`) that mutate work item state. For mission-critical software, these operations require event sourcing to ensure:

1. **Audit Trail**: Complete history of all state changes
2. **Recoverability**: Ability to reconstruct state from events
3. **Consistency**: Event-based state transitions prevent data corruption
4. **Debugging**: Full visibility into what happened and when

**Current State**:
- Phase 4.4 completed with `InMemoryWorkItemRepository` (simplified, not event-sourced)
- Read operations (list, show) work with current implementation
- Write operations would create state without audit trail

**User Decision (2026-01-12)**:
> "Skip to Phase 4.6 and then we will circle back to Phase 4.5 and discussing tackling full blown event sourcing, which we need to have for this mission critical app"

**Impact**:
- Phase 4.5 deferred until TD-018 (Event Sourcing) is addressed
- Phase 4.6 (Integration & Documentation) proceeds as next step
- Ensures mission-critical reliability is not compromised

**Related**:
- TD-018: Event Sourcing for Work Item Repository
- Phase 4.4: Items Namespace (Queries) - COMPLETE
- Phase 4.5: Items Namespace (Commands) - DEFERRED

**Action**: Proceed with Phase 4.6, defer Phase 4.5 until post-TD-018
**Status**: ACTIONED

---

### DISC-016: InMemoryWorkItemRepository is Simplified, Not Event-Sourced

**Date**: 2026-01-12
**Context**: Phase 4.4 implementation of work tracking application layer
**Finding**: The `InMemoryWorkItemRepository` created in Phase 4.4 is a simplified implementation that stores work items directly in a dictionary, not as event streams.

**Current Implementation** (`src/work_tracking/infrastructure/adapters/in_memory_work_item_repository.py`):
```python
class InMemoryWorkItemRepository:
    def __init__(self) -> None:
        self._items: dict[str, WorkItem] = {}  # Direct storage, NOT event streams
        self._lock = threading.RLock()
```

**What Event Sourcing Would Require**:
```python
class EventSourcedWorkItemRepository:
    def __init__(self, event_store: IEventStore) -> None:
        self._event_store = event_store

    def get(self, id: WorkItemId) -> WorkItem | None:
        events = self._event_store.read(f"work_item-{id}")
        return WorkItem.reconstitute(events) if events else None

    def save(self, work_item: WorkItem) -> None:
        events = work_item.collect_events()
        self._event_store.append(f"work_item-{work_item.id}", events, work_item.version)
```

**Gap Analysis**:
| Feature | Current | Required |
|---------|---------|----------|
| State Storage | Direct dict | Event streams |
| Audit Trail | None | Complete |
| Version Control | None | Optimistic concurrency |
| State Reconstruction | N/A | From events |

**Impact**:
- Read operations (Phase 4.4) work correctly
- Write operations (Phase 4.5) would lose audit trail
- Concurrency control not enforced
- No ability to replay/reconstruct state

**Action**: Documented in TD-018 for post-Phase 4 remediation
**Status**: LOGGED

---

### DISC-017: RuntimeWarning When Running CLI with -m Flag

**Date**: 2026-01-12
**Context**: Phase 4.6.1 verification of main.py using new parser
**Finding**: When running the CLI with `python3 -m src.interface.cli.main`, a RuntimeWarning is displayed:

```
<frozen runpy>:128: RuntimeWarning: 'src.interface.cli.main' found in sys.modules
after import of package 'src.interface.cli', but prior to execution of
'src.interface.cli.main'; this may result in unpredictable behaviour
```

**Root Cause**:
- Python's `-m` flag executes a module as `__main__`
- The `src.interface.cli` package is imported before `main.py` is executed
- This is due to how Python handles relative imports within packages

**Impact**:
- WARNING ONLY - functionality is not affected
- CLI commands work correctly
- All namespaces route properly

**Workarounds**:
1. Run via entry point: `jerry <command>` (after pip install)
2. Run directly: `python3 src/interface/cli/main.py`
3. Suppress warning: `python3 -W ignore::RuntimeWarning -m src.interface.cli.main`

**Priority**: LOW - cosmetic issue only

**Action**: Logged for future cleanup, not blocking Phase 4.6
**Status**: LOGGED

---

### DISC-018: CommandDispatcher Not Implemented - Dict-Based Workaround Used

**Date**: 2026-01-12
**Context**: Phase 4.6.2 verification of bootstrap.py dispatcher wiring
**Finding**: The codebase has an `ICommandDispatcher` protocol defined but NO concrete `CommandDispatcher` implementation.

**What Exists**:
- `src/application/ports/primary/icommanddispatcher.py` - Protocol definition ✅
- `src/application/dispatchers/query_dispatcher.py` - QueryDispatcher implementation ✅
- `src/application/dispatchers/` - NO command_dispatcher.py ❌

**Current Workaround**:
Session commands use a dict-based approach in `bootstrap.py`:
```python
def create_session_command_handlers() -> dict:
    return {
        "create": CreateSessionCommandHandler(repository=session_repository),
        "end": EndSessionCommandHandler(repository=session_repository),
        "abandon": AbandonSessionCommandHandler(repository=session_repository),
    }
```

**What Full CQRS Would Require**:
```python
# src/application/dispatchers/command_dispatcher.py
class CommandDispatcher:
    def __init__(self) -> None:
        self._handlers: dict[type, Callable] = {}

    def register(self, command_type: type, handler: Callable) -> None:
        self._handlers[command_type] = handler

    def dispatch(self, command: Any) -> list[DomainEvent]:
        handler = self._handlers.get(type(command))
        if handler is None:
            raise CommandHandlerNotFoundError(type(command))
        return handler(command)
```

**Impact Assessment**:
| Aspect | Current (Dict) | Full CommandDispatcher |
|--------|----------------|------------------------|
| Type Safety | Weak (string keys) | Strong (type keys) |
| Discoverability | Manual | Automatic via protocol |
| Extensibility | Manual additions | Register pattern |
| Consistency | Inconsistent with QueryDispatcher | Symmetric CQRS |

**Why This is Acceptable for Now**:
1. Phase 4.5 (Items Commands) is deferred until event sourcing
2. Session commands are limited scope (3 commands)
3. Full CommandDispatcher should be added with event sourcing (TD-018)

**Related**:
- ICommandDispatcher: `src/application/ports/primary/icommanddispatcher.py`
- TD-018: Event Sourcing for Work Items (includes CommandDispatcher)
- Phase 4.5: Items Commands (deferred)

**Action**: Include CommandDispatcher implementation in TD-018 scope
**Status**: LOGGED

---

### DISC-019: InMemoryEventStore Not Persistent - Events Lost on Restart

**Date**: 2026-01-12
**Context**: TD-018 Event Sourcing implementation planning
**Finding**: The only `IEventStore` implementation is `InMemoryEventStore`, which stores events in RAM. All events are lost when the process exits.

**What Exists**:
- `src/work_tracking/domain/ports/event_store.py` - IEventStore protocol ✅
- `src/work_tracking/infrastructure/persistence/in_memory_event_store.py` - RAM-only storage ⚠️

**Current Implementation**:
```python
class InMemoryEventStore:
    def __init__(self) -> None:
        self._streams: dict[str, list[StoredEvent]] = {}  # RAM only
        self._lock = threading.RLock()
```

**Problem**:
| Aspect | Current State | Impact |
|--------|---------------|--------|
| Persistence | None (RAM only) | Events lost on restart |
| Durability | None | No disaster recovery |
| Audit Trail | Lost on exit | Compliance risk |
| Mission-Critical | NOT SUITABLE | Violates Jerry design principles |

**Decision Made**:
1. **TD-018 (NOW)**: Implement `FileSystemEventStore` using JSON Lines format
   - Aligns with Jerry's "filesystem as infinite memory" philosophy
   - Human-readable, git-friendly
   - Events stored in `projects/PROJ-XXX/.jerry/data/events/`

2. **TD-019 (FUTURE)**: SQLite Event Store for higher-volume scenarios
   - Single file database
   - ACID transactions
   - Better for high-volume, concurrent access

**FileSystemEventStore Design**:
```
projects/PROJ-001/.jerry/data/events/
├── work_item-WORK-001.jsonl    # Append-only event log
├── work_item-WORK-002.jsonl    # One event per line
└── ...
```

**Related**:
- TD-018: Event Sourcing for Work Items (revised to include FileSystemEventStore)
- TD-019: SQLite Event Store (new, future work)
- DISC-015: Phase 4.5 Requires Event Sourcing for Mission-Critical Reliability

**Action**:
1. Revise TD-018 scope to include FileSystemEventStore
2. Create TD-019 for SQLite Event Store (future)
3. Create new worktracker: PHASE-TD018-EVENT-SOURCING.md

**Status**: ACTIONED

---

## Archived Discoveries

*None yet*

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-10 | Claude | Initial creation |
| 2026-01-11 | Claude | Added DISC-003: link-artifact CLI missing |
| 2026-01-11 | Claude | Added DISC-004: ps-* orchestration validates Composed Architecture |
| 2026-01-11 | Claude | Added DISC-005: Release Pipeline Missing from CI/CD (elevated to TD-013) |
| 2026-01-11 | Claude | Added DISC-006: Broken CLI Entry Point in pyproject.toml (elevated to TD-014) |
| 2026-01-11 | Claude | Added DISC-007: TD-013 Misunderstood Distribution Model (TD-013 revised) |
| 2026-01-12 | Claude | Added DISC-008: System Python vs Venv Portability |
| 2026-01-12 | Claude | Added DISC-009: New Files Created Without Format Check |
| 2026-01-12 | Claude | Added DISC-010: Release Workflow Missing Dev Dependencies |
| 2026-01-12 | Claude | Added DISC-011: Architecture Pattern Research Initiative |
| 2026-01-12 | Claude | COMPLETED DISC-011: Research findings documented, TD-015 created |
| 2026-01-12 | Claude | Added DISC-012: TOON Format Required as Primary Output |
| 2026-01-12 | Claude | Added DISC-013: CLI Namespaces per Bounded Context |
| 2026-01-12 | Claude | Added DISC-014: Domain Events Use aggregate_id Not Entity-Specific ID (Phase 4.3) |
| 2026-01-12 | Claude | Added DISC-015: Phase 4.5 Requires Event Sourcing for Mission-Critical Reliability |
| 2026-01-12 | Claude | Added DISC-016: InMemoryWorkItemRepository is Simplified, Not Event-Sourced |
| 2026-01-12 | Claude | Added DISC-017: RuntimeWarning When Running CLI with -m Flag |
| 2026-01-12 | Claude | Added DISC-018: CommandDispatcher Not Implemented |
| 2026-01-12 | Claude | Added DISC-019: InMemoryEventStore Not Persistent - Events Lost on Restart |
