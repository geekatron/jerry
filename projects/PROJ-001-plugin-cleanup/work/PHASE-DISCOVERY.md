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
