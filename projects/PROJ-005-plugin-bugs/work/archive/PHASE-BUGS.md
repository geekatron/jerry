# PHASE-BUGS: Bug Tracking

> **Project:** PROJ-005-plugin-bugs
> **Purpose:** Track bugs discovered during and after initial project completion
> **Last Updated:** 2026-01-13

---

## Active Bugs

### BUG-007: Plugin hook scripts require pip installation

**Status:** OPEN
**Severity:** HIGH
**Discovered:** 2026-01-13
**Reporter:** User via conversation
**Phase:** PHASE-05 (Reopened)

#### Problem Description

The plugin's SessionStart hook (`scripts/session_start.py`) does not execute, preventing the Jerry Framework startup message from appearing. The root cause is that the script delegates to modules that require `pip install -e .` to function.

#### Reproduction Steps

1. Install Jerry plugin via local marketplace (succeeds)
2. Start a new Claude Code session
3. **Expected:** Jerry Framework startup message appears with project context
4. **Actual:** No startup message appears

#### Root Cause Analysis

**File:** `scripts/session_start.py` (lines 25-49)

The script is labeled "Legacy Wrapper" and attempts three execution paths, ALL requiring pip:

| Execution Path | Requirement | Evidence |
|----------------|-------------|----------|
| `.venv/bin/jerry-session-start` | Entry point requires `pip install -e .` | `pyproject.toml:48` defines entry point |
| `.venv/bin/python -m src.interface.cli.session_start` | Requires venv with package installed | Module import path |
| `sys.executable -m src.interface.cli.session_start` | Requires `pip install -e .` | Module import path |

**File:** `src/interface/cli/session_start.py` (lines 44-51)

The actual implementation imports from internal packages:
```python
from src.infrastructure.adapters.configuration.layered_config_adapter import LayeredConfigAdapter
from src.infrastructure.adapters.persistence.atomic_file_adapter import AtomicFileAdapter
from src.session_management.application import GetProjectContextQuery
from src.session_management.infrastructure import FilesystemProjectAdapter, OsEnvironmentAdapter
```

These imports require the `src` package to be installed.

#### Evidence Sources

| Source | Reference | Citation |
|--------|-----------|----------|
| scripts/session_start.py | Lines 1-16 | Docstring states "DEPRECATED: This script is a legacy wrapper" |
| scripts/session_start.py | Lines 29-49 | All three fallback paths require pip installation |
| hooks/hooks.json | Line 10 | Hook invokes: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session_start.py` |
| pyproject.toml | Line 48 | Entry point: `jerry-session-start = "src.interface.cli.session_start:main"` |
| src/interface/cli/session_start.py | Lines 44-51 | Imports from `src.*` packages |

#### Design Violation

This violates the plugin self-containment principle:

> **Plugin Design Principle:** A Claude Code plugin MUST be self-contained and work immediately upon installation without requiring users to run additional setup commands like `pip install`.

#### Blast Radius Assessment

**Status:** COMPLETED
**Audit Date:** 2026-01-13

| Script | Status | Imports | Evidence |
|--------|--------|---------|----------|
| `scripts/session_start.py` | **AFFECTED** | Delegates to `src.*` modules | Lines 29-49: All paths require pip |
| `scripts/pre_tool_use.py` | SAFE | stdlib + local `patterns/` | Lines 23-43: Only json, os, sys, pathlib; patterns has fallback |
| `scripts/subagent_stop.py` | SAFE | stdlib only | Lines 16-20: Only json, os, sys, datetime |
| `scripts/post_tool_use.py` | SAFE | stdlib + local `patterns/` | Lines 22-42: Only json, re, sys, pathlib; patterns has fallback |

**Conclusion:** Only `scripts/session_start.py` is affected. Blast radius is limited to SessionStart hook.

**Evidence Details:**

1. **pre_tool_use.py** (SAFE)
   - Line 23-27: `import json, os, sys; from pathlib import Path`
   - Line 29-42: Graceful fallback if `patterns` import fails
   - No `src.*` imports

2. **subagent_stop.py** (SAFE)
   - Line 16-20: `import json, os, sys; from datetime import datetime`
   - No external dependencies whatsoever
   - No `src.*` imports

3. **post_tool_use.py** (SAFE)
   - Line 22-26: `import json, re, sys; from pathlib import Path`
   - Line 28-42: Graceful fallback if `patterns` import fails
   - No `src.*` imports

#### Proposed Fix

Rewrite `scripts/session_start.py` as a standalone script that:
1. Uses only Python stdlib (no pip dependencies)
2. Implements session start logic directly
3. Checks `JERRY_PROJECT` env var
4. Scans `projects/` directory
5. Outputs structured XML tags (`<project-context>`, `<project-required>`, `<project-error>`)

#### Acceptance Criteria

- [ ] `scripts/session_start.py` executes without pip installation
- [ ] SessionStart hook produces expected output
- [ ] All hook scripts audited for pip dependencies
- [ ] Any affected scripts fixed to be standalone

---

### DISC-004: ps-* Artifact Naming Convention Violation

**Status:** OPEN
**Severity:** LOW (cosmetic, but impacts traceability)
**Discovered:** 2026-01-13
**Reporter:** User via conversation
**Phase:** PHASE-06

#### Problem Description

Research artifacts created during PHASE-06 planning do not follow the canonical ps-* naming convention defined in `skills/problem-solving/agents/PS_EXTENSION.md`.

#### Canonical Convention

Per `PS_EXTENSION.md` lines 101-111:

```
Pattern: {ps-id}-{entry-id}-{description}.md
- All artifacts use e-XXX format (sequential starting from e-001)
- Entry IDs are sequential within a project
```

| Agent | Correct Pattern | Example |
|-------|-----------------|---------|
| ps-investigator | `{ps-id}-e-001-investigation.md` | `PROJ-005-e-001-investigation.md` |
| ps-researcher | `{ps-id}-e-002-{topic}.md` | `PROJ-005-e-002-plugin-patterns.md` |
| ps-analyst | `{ps-id}-e-003-{analysis-type}.md` | `PROJ-005-e-003-tradeoffs.md` |
| ps-architect | `{ps-id}-e-004-adr-{slug}.md` | `PROJ-005-e-004-adr-session-start.md` |
| ps-validator | `{ps-id}-e-005-validation.md` | `PROJ-005-e-005-validation.md` |

#### What Was Created (Incorrect)

| File | Wrong ID | Correct ID | Issue |
|------|----------|------------|-------|
| `PROJ-005-e-006-functional-requirements.md` | e-006 | e-001 | Wrong starting number |
| `PROJ-005-e-007-plugin-patterns.md` | e-007 | e-002 | Wrong number |
| `PROJ-005-a-001-tradeoffs.md` | a-001 | e-003 | Wrong prefix (a- vs e-) |
| `ADR-PROJ005-001-standalone-session-start.md` | ADR format | e-004 | Wrong naming convention |
| `PROJ-005-a-002-validation.md` | a-002 | e-005 | Wrong prefix (a- vs e-) |

#### Root Cause

1. **Entry IDs started at e-006 instead of e-001**: When PLAN.md was updated for PHASE-06, entry IDs were incorrectly assigned starting at e-006, implying e-001 through e-005 existed (they don't).

2. **Used `a-XXX` prefix for analysis files**: Analysis artifacts incorrectly used `a-001`, `a-002` instead of sequential `e-XXX` format.

3. **ADR used different naming convention**: Architecture Decision Record used `ADR-PROJ005-001` format instead of `PROJ-005-e-004-adr-{slug}.md`.

#### Evidence

| Source | Reference | Citation |
|--------|-----------|----------|
| PS_EXTENSION.md | Lines 101-111 | Defines canonical naming: `{ps-id}-{entry-id}-{description}.md` |
| PS_EXTENSION.md | Lines 103-111 | ALL agents use `e-XXX` format, not `a-XXX` |
| Filesystem | `projects/PROJ-005-plugin-bugs/` | No e-001 through e-005 files exist |

#### Impact

- **Traceability**: Entry ID gaps (e-001 to e-005 missing) break sequential audit trail
- **Convention Compliance**: Files don't match ps-* skill contract
- **Cross-Reference**: Other documents reference wrong IDs (e-006, e-007, a-001, a-002)

#### Proposed Fix

1. Rename artifacts to follow canonical convention:
   - `PROJ-005-e-006-*` → `PROJ-005-e-001-*`
   - `PROJ-005-e-007-*` → `PROJ-005-e-002-*`
   - `PROJ-005-a-001-*` → `PROJ-005-e-003-*`
   - `ADR-PROJ005-001-*` → `PROJ-005-e-004-adr-*`
   - `PROJ-005-a-002-*` → `PROJ-005-e-005-*`

2. Update all cross-references in:
   - PLAN.md
   - WORKTRACKER.md
   - All research artifacts (internal references)

---

## Resolved Bugs (PHASE-01 to PHASE-04)

| ID | Description | Resolution | Phase |
|----|-------------|------------|-------|
| BUG-001 | plugin.json had 6 unrecognized fields | Removed invalid fields | PHASE-02 |
| BUG-002 | plugin.json paths missing ./ prefix | Added ./ prefix | PHASE-02 |
| BUG-003 | plugin.json skills used file paths instead of directory | Changed to directory format | PHASE-02 |
| BUG-004 | marketplace.json has invalid 'skills' field | Removed field | PHASE-03 |
| BUG-005 | marketplace.json has invalid 'strict' field | Removed field | PHASE-03 |
| BUG-006 | marketplace.json email typo (gmial) | Corrected to gmail | PHASE-03 |

---

## Change Log

| Date | Bug ID | Action | Author |
|------|--------|--------|--------|
| 2026-01-13 | BUG-007 | Completed blast radius audit - only session_start.py affected | Claude |
| 2026-01-13 | BUG-007 | Created bug report with root cause analysis | Claude |
