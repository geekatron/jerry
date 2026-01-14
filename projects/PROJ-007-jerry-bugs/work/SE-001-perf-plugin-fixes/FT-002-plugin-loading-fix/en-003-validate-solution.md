# EN-003: Validate Solution Hypothesis

> **Enabler ID:** EN-003
> **Feature:** FT-002-plugin-loading-fix
> **Project:** PROJ-007-jerry-bugs
> **Status:** COMPLETE ✅
> **Result:** VALIDATION PASSED
> **Created:** 2026-01-14
> **Last Updated:** 2026-01-14

---

## Purpose

Validate the hypothesis that removing PEP 723 inline metadata from `session_start.py` will fix the plugin loading issue before implementing the full TDD/BDD solution in UoW-001.

---

## Hypothesis

**If we remove the PEP 723 inline metadata:**
```python
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
```

**Then:**
- `uv run` will use the project's `pyproject.toml` instead of creating an isolated environment
- PYTHONPATH will be respected
- `from src.infrastructure.*` imports will resolve correctly
- Hook will execute successfully from any working directory

---

## Tasks

| ID | Description | Status | Result |
|----|-------------|--------|--------|
| T-001 | Remove PEP 723 metadata (local test) | COMPLETE ✅ | Metadata removed, docstring added |
| T-002 | Test `uv run` from plugin root | COMPLETE ✅ | PASSED - Imports resolved |
| T-003 | Test `uv run` from arbitrary directory | COMPLETE ✅ | PASSED - Critical test passed |
| T-004 | Document validation results | COMPLETE ✅ | Results documented below |

---

## Validation Results (2026-01-14)

### Test 1: From Plugin Root ✅

```bash
$ cd PROJ-007-jerry-bugs/bugs_20260114_performance
$ PYTHONPATH="." uv run src/interface/cli/session_start.py

Jerry Framework initialized. See CLAUDE.md for context.
<project-context>
ProjectActive: PROJ-007-jerry-bugs
ProjectPath: projects/PROJ-007-jerry-bugs/
ValidationMessage: Project is properly configured
</project-context>
```

**Result:** PASSED - Imports resolved correctly.

### Test 2: From Arbitrary Directory ✅ (Critical Test)

```bash
$ cd /tmp
$ CLAUDE_PROJECT_DIR="/path/to/jerry" PYTHONPATH="/path/to/jerry" uv run /path/to/jerry/src/interface/cli/session_start.py

Jerry Framework initialized. See CLAUDE.md for context.
<project-context>
ProjectActive: PROJ-007-jerry-bugs
ProjectPath: projects/PROJ-007-jerry-bugs/
ValidationMessage: Project is properly configured
</project-context>
```

**Result:** PASSED - Works from arbitrary directory with CLAUDE_PROJECT_DIR set.

### Test 3: User Manual Verification ✅ (Acceptance Gate)

```bash
$ JERRY_PROJECT=PROJ-007-jerry-bugs CLAUDE_CONFIG_DIR=~/.claude-geek \
  claude --plugin-dir=/path/to/bugs_20260114_performance

⎿  SessionStart:startup hook succeeded: Jerry Framework initialized. See CLAUDE.md for context.
   <project-context>
   ProjectActive: PROJ-007-jerry-bugs
   ProjectPath: projects/PROJ-007-jerry-bugs/
   ValidationMessage: Project is properly configured
   </project-context>
```

**Result:** PASSED - User confirmed `claude --plugin-dir` works correctly.

### Conclusion

**HYPOTHESIS CONFIRMED AND USER VERIFIED:** Removing PEP 723 inline metadata fixes the plugin loading issue.

- Without PEP 723 `dependencies = []`, uv uses the project's `pyproject.toml`
- PYTHONPATH is respected
- `from src.infrastructure.*` imports resolve correctly
- Works from any working directory when CLAUDE_PROJECT_DIR is set
- **User manually verified via `claude --plugin-dir`** ✅

---

## Validation Criteria

| Criterion | Pass Condition |
|-----------|----------------|
| Import Resolution | `from src.infrastructure.*` imports succeed |
| Working Directory | Works from any directory, not just repo root |
| PYTHONPATH | Respects `PYTHONPATH="${CLAUDE_PLUGIN_ROOT}"` |
| Exit Code | Script exits with code 0 |
| Output | Produces expected `<project-context>` or `<project-required>` output |

---

## Test Commands

```bash
# From plugin root (should work)
cd /path/to/jerry
PYTHONPATH="." uv run src/interface/cli/session_start.py

# From arbitrary directory (this is what hooks do)
cd /tmp
PYTHONPATH="/path/to/jerry" uv run /path/to/jerry/src/interface/cli/session_start.py

# Simulating actual hook command
PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" uv run ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py
```

---

## Blocks

| Type | ID | Description | Status |
|------|-----|-------------|--------|
| ENABLES | UoW-001 | Implementation can now proceed | ✅ UNBLOCKED |

---

## Outcome

| Result | Status | Next Action |
|--------|--------|-------------|
| ✅ PASS | **ACHIEVED** | Proceed with UoW-001 implementation using TDD/BDD |

---

## Related Artifacts

| Type | Reference |
|------|-----------|
| Discovery | disc-001-uv-portability-requirement.md |
| Source | `src/interface/cli/session_start.py` |
| Hook Config | `hooks/hooks.json` |
| PROJ-005 ADR | `PROJ-005-e-010-adr-uv-session-start.md` |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-14 | EN-003 created for solution validation | Claude |
| 2026-01-14 | T-001 COMPLETE: PEP 723 metadata removed | Claude |
| 2026-01-14 | T-002 COMPLETE: Plugin root test PASSED | Claude |
| 2026-01-14 | T-003 COMPLETE: Arbitrary directory test PASSED | Claude |
| 2026-01-14 | T-004 COMPLETE: Results documented | Claude |
| 2026-01-14 | EN-003 COMPLETE: Hypothesis confirmed, UoW-001 unblocked | Claude |
| 2026-01-14 | USER VERIFICATION PASSED: `claude --plugin-dir` works | Adam Nowak |
