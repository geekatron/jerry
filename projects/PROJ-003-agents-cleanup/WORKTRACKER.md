# PROJ-003-agents-cleanup Work Tracker

> **Project:** Agent and Skill Structure Cleanup + Python Environment Standardization
> **Status:** COMPLETED
> **Branch:** `cc/clean-up-agents`
> **Created:** 2026-01-12
> **Reopened:** 2026-01-12 (Phase 7 added)
> **Last Updated:** 2026-01-12
> **Completed:** 2026-01-12

---

## Quick Reference

| Metric | Value |
|--------|-------|
| Total Work Items | 36 |
| Completed | 36 |
| In Progress | 0 |
| Pending | 0 |
| Blocked | 0 |

---

## Phase Index

| Phase | Name | Status | Work Items | Duration Est. |
|-------|------|--------|------------|---------------|
| 0 | Research | COMPLETED | 7/7 | - |
| 1 | Plugin Infrastructure | COMPLETED | 4/4 | - |
| 2 | Skill Frontmatter | COMPLETED | 4/4 | - |
| 3 | Agent Standardization | COMPLETED | 4/4 | - |
| 4 | Hook System | COMPLETED | 4/4 | - |
| 5 | Registry Update | COMPLETED | 1/1 | - |
| 6 | Framework Agent Removal | COMPLETED | 6/6 | - |
| 7 | Python Environment Standardization | COMPLETED | 6/6 | - |

---

## Phase 0: Research (COMPLETED)

| ID | Title | Status | File |
|----|-------|--------|------|
| wi-00-001 | Research Claude Code plugin best practices | DONE | [wi-00-001.md](work/wi-00-001.md) |
| wi-00-002 | Research plugins prior art | DONE | [wi-00-002.md](work/wi-00-002.md) |
| wi-00-003 | Research architecture patterns | DONE | [wi-00-003.md](work/wi-00-003.md) |
| wi-00-004 | Extract PROJ-001 knowledge | DONE | [wi-00-004.md](work/wi-00-004.md) |
| wi-00-005 | Gap analysis | DONE | [wi-00-005.md](work/wi-00-005.md) |
| wi-00-006 | Synthesis | DONE | [wi-00-006.md](work/wi-00-006.md) |
| wi-00-007 | Create ADR | DONE | [wi-00-007.md](work/wi-00-007.md) |

---

## Phase 1: Plugin Infrastructure (COMPLETED)

| ID | Title | Status | File |
|----|-------|--------|------|
| wi-01-001 | Rename manifest.json to plugin.json | DONE | [wi-01-001.md](work/wi-01-001.md) |
| wi-01-002 | Update plugin.json schema and fields | DONE | [wi-01-002.md](work/wi-01-002.md) |
| wi-01-003 | Create commands directory and move files | DONE | [wi-01-003.md](work/wi-01-003.md) |
| wi-01-004 | Cleanup and validate plugin structure | DONE | [wi-01-004.md](work/wi-01-004.md) |

---

## Phase 2: Skill Frontmatter (COMPLETED)

| ID | Title | Status | File |
|----|-------|--------|------|
| wi-02-001 | Add frontmatter to worktracker SKILL.md | DONE | [wi-02-001.md](work/wi-02-001.md) |
| wi-02-002 | Add frontmatter to architecture SKILL.md | DONE | [wi-02-002.md](work/wi-02-002.md) |
| wi-02-003 | Add frontmatter to worktracker-decomposition SKILL.md | DONE | [wi-02-003.md](work/wi-02-003.md) |
| wi-02-004 | Update problem-solving SKILL.md trigger phrases | DONE | [wi-02-004.md](work/wi-02-004.md) |

---

## Phase 3: Agent Standardization (COMPLETED)

| ID | Title | Status | File |
|----|-------|--------|------|
| wi-03-001 | Add frontmatter to orchestrator.md | DONE | [wi-03-001.md](work/wi-03-001.md) |
| wi-03-002 | Add frontmatter to qa-engineer.md | DONE | [wi-03-002.md](work/wi-03-002.md) |
| wi-03-003 | Add frontmatter to security-auditor.md | DONE | [wi-03-003.md](work/wi-03-003.md) |
| wi-03-004 | Update TEMPLATE.md and validate Phase 3 | DONE | [wi-03-004.md](work/wi-03-004.md) |

---

## Phase 4: Hook System (COMPLETED)

| ID | Title | Status | File |
|----|-------|--------|------|
| wi-04-001 | Update hooks.json paths to use CLAUDE_PLUGIN_ROOT | DONE | [wi-04-001.md](work/wi-04-001.md) |
| wi-04-002 | Add PreToolUse hook for Write/Edit validation | DONE | [wi-04-002.md](work/wi-04-002.md) |
| wi-04-003 | Migrate scripts from .claude/hooks/ | DONE | [wi-04-003.md](work/wi-04-003.md) |
| wi-04-004 | Cleanup and validate hook system | DONE | [wi-04-004.md](work/wi-04-004.md) |

---

## Phase 5: Registry Update (COMPLETED)

| ID | Title | Status | File |
|----|-------|--------|------|
| wi-05-001 | Update AGENTS.md with complete registry | DONE | [wi-05-001.md](work/wi-05-001.md) |

---

## Phase 6: Framework Agent Removal (COMPLETED)

| ID | Title | Status | File |
|----|-------|--------|------|
| wi-06-001 | Remove agents from .claude/settings.json | DONE | [wi-06-001.md](work/wi-06-001.md) |
| wi-06-002 | Remove agents from plugin.json | DONE | [wi-06-002.md](work/wi-06-002.md) |
| wi-06-003 | Update AGENTS.md to remove framework agents | DONE | [wi-06-003.md](work/wi-06-003.md) |
| wi-06-004 | Update CLAUDE.md agents section | DONE | [wi-06-004.md](work/wi-06-004.md) |
| wi-06-005 | Delete .claude/agents/ directory | DONE | [wi-06-005.md](work/wi-06-005.md) |
| wi-06-006 | Validate and commit Phase 6 | DONE | [wi-06-006.md](work/wi-06-006.md) |

---

## Phase 7: Python Environment Standardization (COMPLETED)

> **Goal:** Standardize Python environment management using uv with venv compatibility.
> Ensure tests run reliably locally and in CI pipelines.
> Research best practices for Claude Code plugin/skill portability.

| ID | Title | Status | File |
|----|-------|--------|------|
| wi-07-001 | Quick fix pytest pythonpath issue | DONE | [wi-07-001.md](work/wi-07-001.md) |
| wi-07-002 | Research venv best practices for Python portability | DONE | [wi-07-002.md](work/wi-07-002.md) |
| wi-07-003 | Research macOS system Python versions | DONE (merged into wi-07-002) | - |
| wi-07-004 | Investigate dual support (uv + standard venv/pip) | DONE (merged into wi-07-002) | - |
| wi-07-005 | Create and execute action plan for venv standardization | DONE | [wi-07-005.md](work/wi-07-005.md) |
| wi-07-006 | Update CI pipelines for venv compatibility | DONE (merged into wi-07-005 Task 5.3) | - |

---

## Bugs

| ID | Title | Severity | Status | Related WI |
|----|-------|----------|--------|------------|
| BUG-001 | pytest.ini `pythonpath=src` conflicts with `--import-mode=importlib` | HIGH | FIXED | wi-07-001 |

### BUG-001: pytest pythonpath conflict

**Discovered:** 2026-01-12
**Symptoms:** 52 test collection errors with `ModuleNotFoundError: No module named 'src'`
**Root Cause:** `pytest.ini` sets `pythonpath = src` which adds `/project/src` to sys.path.
Combined with `--import-mode=importlib`, this interferes with the editable install's package resolution.
Tests import `from src.xxx` expecting project root on path, not `src/` directory.

**Evidence:**
- Direct Python import succeeds: `.venv/bin/python -c "from src.infrastructure.adapters.file_repository import FileRepository; print('SUCCESS')"`
- pytest fails: `uv run pytest` → 52 collection errors
- Workaround verified: `uv run pytest --override-ini="pythonpath="` → 241 passed, 1 failed

**Fix:** Remove `pythonpath = src` from pytest.ini (editable install handles package resolution)

---

## Discoveries

| ID | Title | Impact | Related WI |
|----|-------|--------|------------|
| DISC-001 | Hybrid agent org is industry-aligned | Positive - no reorg needed | wi-00-003 |
| DISC-002 | ps-* agents already compliant | Positive - only framework agents need update | wi-00-005 |
| DISC-003 | Migration completed with all 23 gaps addressed | Positive - Jerry now Claude Code compliant | wi-05-001 |
| DISC-004 | Framework agents (.claude/agents/) were half-baked | Corrective - removed in favor of skill agents | wi-06-001 |
| DISC-005 | Project validation tests use incorrect absolute paths | Negative - 5 tests fail looking for `/projects/...` | wi-07-001 |

### DISC-005: Project validation test path issue

**Discovered:** 2026-01-12
**Tests Affected:** 5 tests in `tests/project_validation/`
**Symptoms:** Tests fail looking for `/projects/PROJ-001-plugin-cleanup/PLAN.md` (absolute path from filesystem root)
**Root Cause:** Test fixtures construct paths incorrectly - using absolute `/projects/` instead of relative paths

**Evidence:**
```
FAILED tests/project_validation/architecture/test_path_conventions.py::TestProjectIsolation::test_project_has_required_structure[PROJ-001-plugin-cleanup]
E   AssertionError: Missing required file: PLAN.md
E   assert False
E    +  where exists = PosixPath('/projects/PROJ-001-plugin-cleanup/PLAN.md').exists
```

**Note:** This is a pre-existing issue unrelated to the pytest pythonpath fix. Tracked as potential tech debt.

---

## Technical Debt

| ID | Title | Priority | Related WI |
|----|-------|----------|------------|
| TD-001 | Project validation tests use incorrect absolute paths | MEDIUM | wi-07-001 |

### TD-001: Project validation test path issue

**Identified:** 2026-01-12
**Related Discovery:** DISC-005
**Effort:** ~1 hour
**Impact:** 5 tests permanently fail in CI and locally

**Description:** Tests in `tests/project_validation/` construct paths as `/projects/...` (absolute from root) instead of relative to project root. This means:
1. Tests fail on every machine
2. CI may be ignoring these failures or they're new

**Suggested Fix:** Update test fixtures to use relative paths or `Path(__file__).parent.parent.parent / "projects"`

---

## References

| Document | Path | Purpose |
|----------|------|---------|
| ADR-PROJ003-001 | [decisions/ADR-PROJ003-001-agent-skill-cleanup-strategy.md](decisions/ADR-PROJ003-001-agent-skill-cleanup-strategy.md) | Migration strategy |
| Synthesis | [synthesis/proj-003-e-006-synthesis.md](synthesis/proj-003-e-006-synthesis.md) | Unified findings |
| Gap Analysis | [analysis/proj-003-e-005-gap-analysis.md](analysis/proj-003-e-005-gap-analysis.md) | 23 gaps identified |

---

## Status Legend

| Status | Meaning |
|--------|---------|
| PENDING | Not started |
| IN_PROGRESS | Currently being worked on |
| BLOCKED | Cannot proceed (see notes) |
| DONE | Completed and verified |

---

*This file is the index. See `work/wi-*.md` for detailed work items.*
