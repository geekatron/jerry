# TASK-004: Integration Design with Existing session_start_hook.py

<!--
DOCUMENT-ID: FEAT-005:EN-405:TASK-004
TEMPLATE: Integration Design
VERSION: 1.0.0
AGENT: ps-architect-405 (Claude Opus 4.6)
DATE: 2026-02-14
PARENT: EN-405 (Session Context Enforcement Injection)
FEATURE: FEAT-005 (Quality Framework Enforcement Mechanisms)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
QUALITY-TARGET: >= 0.92
REQUIREMENTS-COVERED: IR-405-001 through IR-405-007, EH-405-001 through EH-405-004
-->

> **Version:** 1.0.0
> **Agent:** ps-architect-405 (Claude Opus 4.6)
> **Status:** COMPLETE
> **Created:** 2026-02-14

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Current Hook Analysis](#current-hook-analysis) | What session_start_hook.py does today |
| [Extension Points](#extension-points) | Where quality context is injected |
| [Modification Specification](#modification-specification) | Exact changes to make, line by line |
| [Backward Compatibility Guarantees](#backward-compatibility-guarantees) | What does NOT change and how to verify |
| [Data Flow Analysis](#data-flow-analysis) | How data flows through the enhanced hook |
| [Failure Mode Analysis](#failure-mode-analysis) | All failure scenarios and their outcomes |
| [Deployment Strategy](#deployment-strategy) | How to roll out and roll back |
| [Test Strategy for Integration Verification](#test-strategy-for-integration-verification) | Integration tests that prove compatibility |
| [Traceability](#traceability) | Requirements coverage |
| [References](#references) | Source documents |

---

## Current Hook Analysis

### File: `scripts/session_start_hook.py`

**Location:** `/Users/adam.nowak/workspace/GitHub/geekatron/jerry/scripts/session_start_hook.py`
**Lines:** 324
**Language:** Python 3.11+
**Shebang:** `#!/usr/bin/env -S uv run python`

### Current Functions

| Function | Lines | Purpose |
|----------|-------|---------|
| `output_json(system_message, additional_context)` | 25-44 | Outputs combined JSON with systemMessage and additionalContext |
| `output_error(message, log_file)` | 47-59 | Outputs error as valid hook JSON |
| `get_log_file(plugin_root)` | 62-68 | Determines log file location |
| `log_error(log_file, message)` | 71-81 | Appends error to log file |
| `find_uv()` | 84-101 | Finds uv executable in PATH or common locations |
| `check_precommit_hooks(plugin_root)` | 104-140 | Checks if pre-commit hooks are installed |
| `format_hook_output(cli_data, precommit_warning)` | 143-219 | Transforms CLI JSON to (systemMessage, additionalContext) tuple |
| `main()` | 222-324 | Main entry point: orchestrates the full flow |

### Current `main()` Flow

```
main() [line 222]
  ├── Resolve plugin_root and log_file        [lines 225-229]
  ├── Log startup                              [line 232]
  ├── Find uv                                  [lines 235-239]
  ├── Change to plugin directory               [lines 244-250]
  ├── try:
  │   ├── uv sync --quiet                      [lines 256-261]
  │   ├── Run jerry --json projects context    [lines 264-282]
  │   ├── Parse CLI JSON                       [lines 285-290]
  │   ├── Check pre-commit hooks               [lines 294-298]
  │   ├── format_hook_output()                 [line 301]
  │   │   -> Returns (system_message, additional_context)
  │   ├── output_json(system_message, additional_context)  [line 302]  <-- MODIFICATION POINT
  │   └── Log stderr                           [lines 304-306]
  ├── except TimeoutExpired                    [lines 311-313]
  ├── except Exception                         [lines 315-317]
  └── finally: os.chdir(original_cwd)          [lines 319-320]
```

### Current Imports (Lines 15-22)

```python
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import UTC
from pathlib import Path
```

### Current Output Format

The hook outputs JSON with two fields:
- `systemMessage`: Concise user-visible message (shown in terminal)
- `hookSpecificOutput.additionalContext`: Detailed XML-tagged context (injected into Claude's context window)

Three cases for `additionalContext`:
1. **Valid project:** `<project-context>` tag with project info
2. **Invalid project:** `<project-error>` tag with error details
3. **No project set:** `<project-required>` tag with available projects

Optional `<dev-environment-warning>` tag appended if pre-commit hooks are missing.

---

## Extension Points

### Primary Extension Point: Between `format_hook_output()` and `output_json()`

The quality context injection occurs between the `format_hook_output()` return and the `output_json()` call. **Line numbers are approximate** based on the current hook state (324 lines) and must be re-evaluated at implementation time. Use pattern-based identification: find `system_message, additional_context = format_hook_output(...)` followed by `output_json(system_message, additional_context)`.

**EN-403 ordering dependency:** EN-403 also modifies `session_start_hook.py` (per EN-403 TASK-004). EN-405 hook modifications MUST be applied AFTER EN-403 modifications. The pattern-based insertion point is stable regardless of EN-403 line number changes.

**Current (approximately line 301-302):**
```python
        system_message, additional_context = format_hook_output(cli_data, precommit_warning)
        output_json(system_message, additional_context)
```

**Enhanced:**
```python
        system_message, additional_context = format_hook_output(cli_data, precommit_warning)

        # Generate quality framework context (EN-405)
        quality_context = ""
        if QUALITY_CONTEXT_AVAILABLE:
            try:
                generator = SessionQualityContextGenerator()
                quality_context = generator.generate()
            except Exception as e:
                log_error(log_file, f"WARNING: Quality context generation failed: {e}")
                quality_context = ""  # Fail-open

        if quality_context:
            additional_context = additional_context + "\n\n" + quality_context

        output_json(system_message, additional_context)
```

### Secondary Extension Point: Import Section (After Existing Imports)

**Location:** After the last existing import (`from pathlib import Path`). Use pattern-based identification, not absolute line numbers.

**Current:**
```python
from pathlib import Path
```

**Enhanced:**
```python
from pathlib import Path

# Quality framework context injection (EN-405)
_project_root = str(Path(__file__).resolve().parent.parent)
try:
    sys.path.insert(0, _project_root)
    from src.infrastructure.internal.enforcement.session_quality_context import (
        SessionQualityContextGenerator,
    )
    QUALITY_CONTEXT_AVAILABLE = True
except Exception:
    QUALITY_CONTEXT_AVAILABLE = False
finally:
    # Clean up sys.path to avoid shadowing stdlib modules
    if _project_root in sys.path:
        sys.path.remove(_project_root)
```

### Why These Extension Points Are Safe

| Point | Risk | Mitigation |
|-------|------|-----------|
| Import block | Module not found | `except Exception` catches ALL import-time failures; flag prevents any usage attempt |
| Import block | SyntaxError/AttributeError in module | `except Exception` catches these; user sees no error (fail-open) |
| Import block | sys.path pollution | `finally` block removes project root from sys.path after import attempt |
| main() block | Generator raises exception | try/except catches ALL exceptions; logs and continues |
| main() block | Slow generation | Generator is pure string concat; << 1ms; no I/O |
| main() block | Malformed output | Only appended if non-empty; `\n\n` separator keeps it distinct |

---

## Modification Specification

### Change 1: Import Block

**Location:** After existing imports (anchor: `from pathlib import Path`). Use pattern-based identification.
**Lines added:** 11

```python
# Quality framework context injection (EN-405)
_project_root = str(Path(__file__).resolve().parent.parent)
try:
    sys.path.insert(0, _project_root)
    from src.infrastructure.internal.enforcement.session_quality_context import (
        SessionQualityContextGenerator,
    )
    QUALITY_CONTEXT_AVAILABLE = True
except Exception:
    QUALITY_CONTEXT_AVAILABLE = False
finally:
    if _project_root in sys.path:
        sys.path.remove(_project_root)
```

### Change 2: Quality Context Generation in `main()`

**Location:** Between `format_hook_output()` return and `output_json()` call. Use pattern-based identification (see Extension Points section).
**Lines added:** 10

```python
        # Generate quality framework context (EN-405)
        quality_context = ""
        if QUALITY_CONTEXT_AVAILABLE:
            try:
                generator = SessionQualityContextGenerator()
                quality_context = generator.generate()
            except Exception as e:
                log_error(log_file, f"WARNING: Quality context generation failed: {e}")
                quality_context = ""  # Fail-open

        if quality_context:
            additional_context = additional_context + "\n\n" + quality_context
```

### Total Impact

| Metric | Value |
|--------|-------|
| Lines added | 21 (11 import block with sys.path cleanup + 10 main) |
| Lines modified | 0 |
| Lines removed | 0 |
| Functions added | 0 |
| Functions modified | 1 (main, additive only) |
| New imports | 1 (conditional, from own codebase) |
| New dependencies | 0 (stdlib only) |

---

## Backward Compatibility Guarantees

### Guaranteed Unchanged Behaviors

| # | Behavior | How to Verify |
|---|----------|---------------|
| BC-001 | `systemMessage` content is identical for all 3 cases (valid/invalid/no project) | Integration test: compare systemMessage with and without quality context module |
| BC-002 | `<project-context>` output format and content identical | Integration test: parse project-context XML; verify all fields present |
| BC-003 | `<project-error>` output format and content identical | Integration test: trigger invalid project; verify error XML |
| BC-004 | `<project-required>` output format and content identical | Integration test: unset JERRY_PROJECT; verify required XML |
| BC-005 | `<dev-environment-warning>` present when pre-commit hooks missing | Integration test: remove pre-commit hook; verify warning |
| BC-006 | Error handling for uv not found produces valid JSON | Integration test: mock uv absence; verify JSON output |
| BC-007 | Error handling for jerry CLI failure produces valid JSON | Integration test: mock CLI failure; verify JSON output |
| BC-008 | Hook returns exit code 0 in all scenarios | Integration test: verify exit code for all paths |
| BC-009 | Hook works when quality context module is NOT deployed | Integration test: remove module; verify original output |
| BC-010 | Hook JSON structure is valid and parseable | Integration test: json.loads() on all output scenarios |

### Backward Compatibility Test Script (Sketch)

```python
"""Integration test: backward compatibility for session_start_hook.py."""

def test_bc_001_system_message_unchanged():
    """systemMessage identical with and without quality context."""
    # Run hook without quality module -> capture systemMessage
    # Deploy quality module -> run hook -> capture systemMessage
    # Assert identical

def test_bc_009_works_without_module():
    """Hook works when SessionQualityContextGenerator not deployed."""
    # Ensure module does NOT exist
    # Run hook
    # Assert: valid JSON output
    # Assert: contains project context
    # Assert: does NOT contain <quality-framework>

def test_bc_010_valid_json_all_scenarios():
    """Hook output is valid JSON in all scenarios."""
    for scenario in [valid_project, invalid_project, no_project]:
        output = run_hook(scenario)
        data = json.loads(output)
        assert "systemMessage" in data
        assert "hookSpecificOutput" in data
```

---

## Data Flow Analysis

### Enhanced Data Flow

```
session_start_hook.py main()
    │
    ├── INPUTS:
    │   ├── Environment: JERRY_PROJECT, CLAUDE_PROJECT_DIR
    │   ├── Filesystem: pyproject.toml (uv sync), .git/ (pre-commit check)
    │   └── CLI: jerry --json projects context -> JSON
    │
    ├── PROCESSING:
    │   ├── cli_data = json.loads(stdout)
    │   ├── precommit_warning = check_precommit_hooks(plugin_root)
    │   ├── (system_message, additional_context) = format_hook_output(cli_data, precommit_warning)
    │   ├── quality_context = SessionQualityContextGenerator().generate()  (NEW)
    │   └── additional_context += "\n\n" + quality_context                (NEW)
    │
    └── OUTPUT:
        └── JSON:
            ├── systemMessage: str              (UNCHANGED)
            └── hookSpecificOutput:
                ├── hookEventName: "SessionStart" (UNCHANGED)
                └── additionalContext: str       (EXTENDED with quality context)
```

### Data Separation

| Data | Source | Mutable? | Quality Context Dependency? |
|------|--------|----------|---------------------------|
| Project context | jerry CLI -> format_hook_output() | No | None (independent) |
| Pre-commit warning | check_precommit_hooks() | No | None (independent) |
| Quality context | SessionQualityContextGenerator.generate() | No | None (self-contained) |

The three content sources are completely independent. Quality context generation cannot affect project context or pre-commit warning, and vice versa.

---

## Failure Mode Analysis

### Failure Mode 1: Module Not Deployed

| Aspect | Detail |
|--------|--------|
| **Trigger** | `session_quality_context.py` does not exist at import time |
| **Detection** | `ImportError` caught in import block |
| **Result** | `QUALITY_CONTEXT_AVAILABLE = False` |
| **Impact** | Hook runs exactly as before; no quality context appended |
| **User visible** | No -- session starts normally |
| **Recovery** | Deploy the module; next session will include quality context |

### Failure Mode 2: Module Import Error (Non-ImportError)

| Aspect | Detail |
|--------|--------|
| **Trigger** | Module exists but has syntax error or other import-time exception |
| **Detection** | `except Exception` catches ALL import-time failures including SyntaxError, AttributeError, TypeError |
| **Result** | `QUALITY_CONTEXT_AVAILABLE = False`; hook runs without quality context |
| **Impact** | No quality context appended; existing content unaffected |
| **User visible** | No -- fail-open design ensures no user-visible errors from quality context import failures |
| **Decision** | Changed from `except ImportError` to `except Exception` per adversarial critique Finding 2. The fail-open design intent requires that quality context failures are invisible to the user. The outer `try/except` in `main()` would call `output_error()` which produces user-visible terminal output -- unacceptable for a quality context failure. |

### Failure Mode 3: Generator Raises Exception

| Aspect | Detail |
|--------|--------|
| **Trigger** | `generator.generate()` raises any exception |
| **Detection** | `except Exception as e` in main() |
| **Result** | Error logged; `quality_context = ""`; hook continues |
| **Impact** | No quality context appended; existing content unaffected |
| **User visible** | No -- session starts normally |

### Failure Mode 4: Generator Returns Malformed XML

| Aspect | Detail |
|--------|--------|
| **Trigger** | `generator.generate()` returns truncated or malformed string |
| **Detection** | Not detected at hook level (no XML validation in hook) |
| **Result** | Malformed XML appended to additionalContext |
| **Impact** | Claude may partially parse quality context; project context unaffected |
| **Mitigation** | Unit tests verify output format; generator is deterministic |

### Failure Mode 5: Performance Degradation

| Aspect | Detail |
|--------|--------|
| **Trigger** | Generator takes unexpectedly long |
| **Detection** | No timeout on generator (it is pure string concat) |
| **Result** | Not realistic -- string concatenation is O(1) in practice, << 1ms |
| **Mitigation** | If future dynamic content adds I/O, add timeout wrapper |

---

## Deployment Strategy

### Phase 1: Module Deployment (No Hook Change)

1. Create `src/infrastructure/internal/enforcement/__init__.py`
2. Create `src/infrastructure/internal/enforcement/session_quality_context.py`
3. Run unit tests for the generator module
4. Commit module (no hook changes yet)

**Result:** Module exists but hook does not import it. No behavior change.

**AC-5 status during Phase 1:** NOT SATISFIED. The quality preamble does not load at session start because the hook has not been modified to import it. This is an intentional intermediate state that enables independent testing of the generator module before integration. AC-5 is satisfied only after Phase 2 is complete.

### Phase 2: Hook Integration

1. Add import block to session_start_hook.py (with `except Exception` and sys.path cleanup)
2. Add quality context generation block to main()
3. Run integration tests (including end-to-end: session start -> hook fires -> module loads -> preamble appears in Claude's context)
4. Verify backward compatibility (BC-001 through BC-010)
5. Commit hook changes

**Result:** Hook now imports and uses the module. Quality context appears in additionalContext.

**AC-5 status after Phase 2:** SATISFIED. The full path is verified: session start -> hook fires -> module loads -> preamble injected into `additionalContext` -> Claude receives quality framework context. The "every session" and "without manual intervention" aspects are verified by integration test (see Test Strategy below).

### Rollback Path

| Scenario | Action | Time |
|----------|--------|------|
| Module has bugs | Delete or rename `session_quality_context.py` | Immediate; next session reverts to original |
| Hook changes have bugs | Revert the 21 lines added to session_start_hook.py | 1 commit |
| Quality context content wrong | Modify `session_quality_context.py` only | No hook changes needed |

### Rollback Safety

The `QUALITY_CONTEXT_AVAILABLE` flag ensures:
- If the module is deleted, the flag is `False`, and no quality context code runs
- If the module is renamed, same effect
- The hook's core logic is NEVER gated on the flag -- only the quality context injection

---

## Test Strategy for Integration Verification

### Test Categories

| Category | Count | Purpose |
|----------|-------|---------|
| Backward compatibility | 10 | Verify BC-001 through BC-010 |
| Quality context presence | 3 | Verify quality context appears in output |
| Fail-open behavior | 3 | Verify graceful degradation |
| Content verification | 5 | Verify XML structure and key content |

### Test 1: Quality Context Present in Output

```python
def test_hook_includes_quality_context_when_module_available():
    """Quality context appears in additionalContext when module is deployed."""
    output = run_hook_with_valid_project()
    data = json.loads(output)
    additional = data["hookSpecificOutput"]["additionalContext"]
    assert '<quality-framework version="1.0">' in additional
    assert "</quality-framework>" in additional
```

### Test 2: Backward Compatibility -- Project Context Preserved

```python
def test_project_context_preserved_with_quality_context():
    """Existing project context content unchanged when quality context added."""
    output = run_hook_with_valid_project()
    data = json.loads(output)
    additional = data["hookSpecificOutput"]["additionalContext"]
    assert "<project-context>" in additional
    assert "ProjectActive:" in additional
    assert "ValidationMessage:" in additional
```

### Test 3: Fail-Open -- Module Unavailable

```python
def test_hook_works_without_quality_module(monkeypatch):
    """Hook produces valid output when quality module is not available."""
    monkeypatch.setattr("session_start_hook.QUALITY_CONTEXT_AVAILABLE", False)
    output = run_hook_with_valid_project()
    data = json.loads(output)
    # Should have project context but NO quality context
    additional = data["hookSpecificOutput"]["additionalContext"]
    assert "<project-context>" in additional
    assert "<quality-framework" not in additional
```

### Test 4: Fail-Open -- Generator Exception

```python
def test_hook_continues_when_generator_raises(monkeypatch):
    """Hook produces valid output when generator raises an exception."""
    def broken_generate(self):
        raise RuntimeError("Generator broken")
    monkeypatch.setattr(SessionQualityContextGenerator, "generate", broken_generate)
    output = run_hook_with_valid_project()
    data = json.loads(output)
    # Should have project context but NO quality context
    additional = data["hookSpecificOutput"]["additionalContext"]
    assert "<project-context>" in additional
    assert "<quality-framework" not in additional
```

### Test 5: systemMessage Unchanged

```python
def test_system_message_unchanged_with_quality_context():
    """systemMessage is identical whether quality context is present or not."""
    output_with = run_hook_with_quality_module()
    output_without = run_hook_without_quality_module()
    assert json.loads(output_with)["systemMessage"] == json.loads(output_without)["systemMessage"]
```

---

## Traceability

### Requirements Covered

| Requirement | Coverage |
|-------------|----------|
| IR-405-001 | Additive design verified; BC-001 through BC-010 guarantee backward compatibility |
| IR-405-002 | Quality context appended to additionalContext with `\n\n` separator |
| IR-405-003 | systemMessage not touched; BC-001, Test 5 verify |
| IR-405-004 | Module in `src/infrastructure/internal/enforcement/` per file layout |
| IR-405-005 | try/except import with QUALITY_CONTEXT_AVAILABLE flag |
| IR-405-006 | Extension point between format_hook_output() and output_json() |
| IR-405-007 | BC-001 through BC-010 enumerate and verify unchanged behaviors |
| EH-405-001 | Failure mode 3: except Exception -> empty string |
| EH-405-002 | Failure mode 3: log_error() on generation failure |
| EH-405-003 | L2 independence documented in failure cascade |
| EH-405-004 | Failure mode 1 and 2: Any Exception (including ImportError) -> flag = False; sys.path cleaned up |

---

## References

| # | Document | Content Used |
|---|----------|--------------|
| 1 | Current session_start_hook.py | `scripts/session_start_hook.py` -- line-by-line analysis |
| 2 | EN-403 TASK-004 (SessionStart Design) | Integration flow, modification points, error handling |
| 3 | TASK-001 (this enabler's requirements) | IR-405-xxx, EH-405-xxx |
| 4 | TASK-003 (this enabler's hook enhancement design) | Architecture, extension points, file layout |

---

*Agent: ps-architect-405 (Claude Opus 4.6)*
*Date: 2026-02-14*
*Parent: EN-405 Session Context Enforcement Injection*
*Quality Target: >= 0.92*
*Lines Added: 21 to session_start_hook.py (0 modified, 0 removed)*
*Backward Compatibility Tests: 10*
