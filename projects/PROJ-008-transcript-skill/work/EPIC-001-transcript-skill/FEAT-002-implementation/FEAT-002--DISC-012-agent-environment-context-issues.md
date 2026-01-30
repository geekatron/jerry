# FEAT-002:DISC-012: Agent Environment and Context Management Issues

<!--
TEMPLATE: Discovery
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9, worktracker.md (Discovery File)
CREATED: 2026-01-30
PURPOSE: Document critical findings about agent environment, CLI invocation, and file handling
-->

> **Type:** discovery
> **Status:** DOCUMENTED
> **Priority:** HIGH
> **Impact:** HIGH
> **Created:** 2026-01-30T03:00:00Z
> **Completed:** 2026-01-30T03:30:00Z
> **Parent:** FEAT-002
> **Owner:** Claude
> **Source:** Live skill invocation testing (EN-025, TASK-253)

---

## Summary

During live skill invocation testing, multiple environment and context management issues were discovered that caused skill execution failures and performance degradation. The issues span three categories: (1) Python environment management, (2) CLI invocation patterns, and (3) agent file consumption rules.

**Key Findings:**
- System Python invocation fails because UV-managed dependencies are not available to system Python
- Verbose CLI invocation (`uv run python -m src.interface.cli.main`) obscures the proper entry point
- Large file consumption (`canonical-transcript.json` ~930KB) overwhelms agent context windows
- Chunked architecture (DISC-009) was designed to solve large file issues but agents weren't properly instructed

**Validation:** All findings verified through live testing and remediated with rule/documentation updates.

---

## Context

### Background

During EN-025 integration testing, the transcript skill was invoked to process `meeting-006-all-hands.vtt` (90K+ tokens). Multiple failures occurred:

1. **Initial failure:** `command not found: python` when using system Python
2. **Dependency error:** webvtt-py not found when using system Python (even though installed via UV)
3. **Performance degradation:** Agent context overwhelmed by 930KB canonical-transcript.json
4. **Confusion:** Verbose CLI patterns vs proper `uv run jerry` entry point

### Research Question

Why does the skill invocation fail repeatedly, and what systemic issues are preventing reliable agent execution?

### Investigation Approach

1. Executed live skill invocation with `meeting-006-all-hands.vtt`
2. Analyzed error messages from each failure mode
3. Traced dependency management to UV vs system Python confusion
4. Identified CLI entry point in pyproject.toml
5. Measured file sizes to understand context window impact
6. Created remediation rules and documentation updates

---

## Finding

### F-001: UV vs System Python Environment Confusion

**Root Cause:** The Jerry framework uses UV for Python dependency management, but agents were invoking system Python which doesn't have access to UV-managed packages.

**Evidence:**
```bash
# WRONG - System Python doesn't have dependencies
python3 -m src.interface.cli.main transcript parse ...
# Error: ModuleNotFoundError: No module named 'webvtt'

# WRONG - pip installs to system, not UV environment
pip3 install webvtt-py
# Still fails because UV environment is separate

# CORRECT - UV runs with project dependencies
uv run python -m src.interface.cli.main transcript parse ...
# Works because UV provides the virtual environment
```

**Impact:** HIGH - Skill invocation fails completely when using system Python.

### F-002: CLI Entry Point Obscured by Verbose Invocation

**Root Cause:** pyproject.toml defines a CLI entry point `jerry = "src.interface.cli.main:main"`, but agents were using verbose module paths instead.

**Evidence:**
```toml
# pyproject.toml line 56
[project.scripts]
jerry = "src.interface.cli.main:main"
```

```bash
# VERBOSE (works but obscures intent)
uv run python -m src.interface.cli.main transcript parse <file>

# CORRECT (uses defined entry point)
uv run jerry transcript parse <file>
```

**Impact:** MEDIUM - Works but causes confusion and inconsistency.

### F-003: Large File Consumption Overwhelms Agent Context

**Root Cause:** The chunking architecture (DISC-009, TDD-FEAT-004) was designed to solve the large file problem, but agent definitions and orchestration documentation still referenced `canonical-transcript.json` as valid input.

**File Size Analysis:**

| File | Size | Suitable for Agent? |
|------|------|---------------------|
| `canonical-transcript.json` | 929 KB | **NO** - Too large |
| `index.json` | 8 KB | Yes - Metadata only |
| `chunks/chunk-NNN.json` | ~130 KB each | Yes - Manageable |
| `extraction-report.json` | 33 KB | Yes - Manageable |

**Evidence from SKILL.md (before fix):**
```markdown
# Orchestration Flow - STEP 2: EXTRACT
Input: index.json + chunks/*.json (or canonical-transcript.json for small files)
```

This "or canonical-transcript.json" clause allowed agents to use the large file.

**Impact:** HIGH - Context window overflow causes:
- Performance degradation (context rot)
- Data loss (99.8% per DISC-009)
- Increased token costs
- Reduced accuracy

### F-004: Dependency Management Architecture Gap

**Root Cause:** User expected dependencies to be installed at the Jerry framework level so orchestrator can call CLI directly, but agents were attempting to install dependencies within their execution context.

**Expected Architecture:**
```
Jerry Framework (UV-managed)
    │
    └── CLI Entry Point (uv run jerry)
            │
            └── All dependencies pre-installed via pyproject.toml
```

**Actual Behavior During Failure:**
```
Agent spawned
    │
    └── Tried system Python (no dependencies)
            │
            └── Tried pip install (wrong environment)
```

**Resolution:** All Python execution must go through `uv run` to use the correct environment.

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Error Log | "command not found: python" | Live invocation | 2026-01-30 |
| E-002 | Error Log | "ModuleNotFoundError: No module named 'webvtt'" | Live invocation | 2026-01-30 |
| E-003 | Config | CLI entry point in pyproject.toml | pyproject.toml:56 | 2026-01-30 |
| E-004 | Measurement | canonical-transcript.json = 929 KB | File system | 2026-01-30 |
| E-005 | Measurement | index.json = 8 KB | File system | 2026-01-30 |
| E-006 | Documentation | DISC-009 chunking rationale | DISC-009.md | 2026-01-29 |

### Reference Material

- **Source:** TDD-FEAT-004 Hybrid Infrastructure
- **Relevance:** Defines chunking architecture that solves large file problem

- **Source:** pyproject.toml
- **Relevance:** Defines UV dependencies and CLI entry point

---

## Implications

### Impact on Project

This discovery impacts:
1. **All agent definitions** - Must specify correct file handling rules
2. **SKILL.md orchestration** - Must enforce chunked file usage
3. **PLAYBOOK.md** - Must use correct CLI invocation patterns
4. **Developer experience** - Must follow UV-only rule

### Design Decisions Affected

- **Decision:** TDD-FEAT-004 Hybrid Architecture
  - **Impact:** Validated - chunking is correct approach
  - **Rationale:** Large files must not be sent to agents

- **Decision:** ADR-001 Agent Architecture
  - **Impact:** Requires amendment for Python preprocessing layer
  - **Rationale:** Agents orchestrate, Python CLI does heavy lifting

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Future agents use system Python | HIGH | Created `.claude/rules/python-environment.md` |
| Agents read canonical-transcript.json | HIGH | Added "Agent File Consumption Rules" to SKILL.md |
| Inconsistent CLI invocation | MEDIUM | Documented `uv run jerry` as standard |

---

## Relationships

### Creates

- [.claude/rules/python-environment.md](../../../../../.claude/rules/python-environment.md) - UV usage and large file handling rules
- BUG-001-question-count-inflation.md - Related bug discovered during testing

### Informs

- [SKILL.md](../../../../../skills/transcript/SKILL.md) - Agent file consumption rules added
- [ts-extractor.md](../../../../../skills/transcript/agents/ts-extractor.md) - Format A deprecated
- [ts-formatter.md](../../../../../skills/transcript/agents/ts-formatter.md) - File size warning added
- [PLAYBOOK.md](../../../../../skills/transcript/docs/PLAYBOOK.md) - Updated to use chunked files

### Related Discoveries

- [DISC-009](./FEAT-002--DISC-009-agent-only-architecture-limitation.md) - Agent-only architecture limitation (precursor)
- [DISC-011](./FEAT-002--DISC-011-disc009-operational-findings-gap.md) - DISC-009 operational findings gap

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-002](./FEAT-002-implementation.md) | Implementation feature |
| Rule | [python-environment.md](../../../../../.claude/rules/python-environment.md) | UV and file handling rules |
| Test Output | [live-test-2026-01-30-run2/](../../../../../skills/transcript/test_data/validation/live-test-2026-01-30-run2/) | Clean test run |

---

## Recommendations

### Immediate Actions

1. ✅ **DONE:** Created `.claude/rules/python-environment.md` enforcing UV usage
2. ✅ **DONE:** Added "Agent File Consumption Rules" section to SKILL.md
3. ✅ **DONE:** Updated ts-extractor.md to deprecate Format A (canonical-transcript.json)
4. ✅ **DONE:** Updated ts-formatter.md with file size violation warning
5. ✅ **DONE:** Updated PLAYBOOK.md to use index.json + chunks

### Long-term Considerations

- **Pre-commit hook:** Consider adding hook that validates agent definitions don't reference canonical-transcript.json
- **CI validation:** Add test that measures agent input file sizes
- **Documentation audit:** Review all agent definitions for large file references

---

## Open Questions

### Questions for Follow-up

1. **Q:** Should we add automated validation that agents don't read files > 100KB?
   - **Investigation Method:** Research Claude Code hooks for file access validation
   - **Priority:** MEDIUM

2. **Q:** Should canonical-transcript.json be generated at all, or only on explicit request?
   - **Investigation Method:** Survey use cases where full transcript is needed
   - **Priority:** LOW

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-30 | Claude | Created discovery with all findings documented |

---

## Metadata

```yaml
id: "FEAT-002:DISC-012"
parent_id: "FEAT-002"
work_type: DISCOVERY
title: "Agent Environment and Context Management Issues"
status: DOCUMENTED
priority: HIGH
impact: HIGH
created_by: "Claude"
created_at: "2026-01-30T03:00:00Z"
updated_at: "2026-01-30T03:30:00Z"
completed_at: "2026-01-30T03:30:00Z"
tags: [environment, uv, python, file-handling, context-management, agents]
source: "Live skill invocation testing"
finding_type: GAP
confidence_level: HIGH
validated: true
```
