# EN-003: Validate Solution Hypothesis

> **Enabler ID:** EN-003
> **Feature:** FT-002-plugin-loading-fix
> **Project:** PROJ-007-jerry-bugs
> **Status:** IN PROGRESS
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

| ID | Description | Status | Notes |
|----|-------------|--------|-------|
| T-001 | Remove PEP 723 metadata (local test) | PENDING | Modify session_start.py locally |
| T-002 | Test `uv run` from plugin root | PENDING | `cd ${PLUGIN_ROOT} && uv run ...` |
| T-003 | Test `uv run` from arbitrary directory | PENDING | `cd /tmp && uv run ${PLUGIN_ROOT}/...` |
| T-004 | Document validation results | PENDING | Update disc-001 with findings |

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

| Type | ID | Description |
|------|-----|-------------|
| ENABLES | UoW-001 | Implementation cannot proceed until validation confirms solution |

---

## Expected Outcome

| Result | Next Action |
|--------|-------------|
| ✅ PASS | Proceed with UoW-001 implementation using TDD/BDD |
| ❌ FAIL | Re-evaluate solution options in disc-001 |

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
