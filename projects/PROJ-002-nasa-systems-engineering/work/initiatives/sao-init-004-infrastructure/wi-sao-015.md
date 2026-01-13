---
id: wi-sao-015
title: "Add Guardrail Validation Hooks"
status: DONE
parent: "_index.md"
initiative: sao-init-004
children: []
depends_on: []
blocks: []
created: "2026-01-10"
started: "2026-01-12"
completed: "2026-01-12"
audited: "2026-01-12"
priority: "P2"
estimated_effort: "8h"
actual_effort: "4h"
entry_id: "sao-015"
source: "OPT-005"
token_estimate: 500
---

# WI-SAO-015: Add Guardrail Validation Hooks

> **Status:** DONE
> **Priority:** MEDIUM (P2)
> **Started:** 2026-01-12
> **Completed:** 2026-01-12

---

## Description

Add pre/post validation hooks for constitutional principle enforcement.

---

## Acceptance Criteria

| AC# | Criterion | Validated? | Evidence |
|-----|-----------|------------|----------|
| AC-015-001 | Async validation (non-blocking) | VALIDATED | Subprocess model in pre_tool_use.py |
| AC-015-002 | timeout_ms: 100 | VALIDATED | patterns.json line 26, 59, etc. |
| AC-015-003 | mode: warn (don't block, just log) | VALIDATED | pii_detection mode: warn (patterns.json:39) |
| AC-015-004 | Pattern library for common checks | VALIDATED | patterns.json: 3 input groups, 2 output groups, 25+ rules |

---

## Evidence Found (Audit 2026-01-12)

### Agent Templates HAVE Guardrails Sections

22 agent files mention "guardrails":
- All ps-* agents (9 files)
- All nse-* agents (10 files)
- Template files (3 files)

Example from ps-analyst.md:
```yaml
guardrails:
  input_validation:
    - ...
  output_filtering:
    - ...
```

### What DOES NOT Exist

1. **Centralized hook runner** - No async validation infrastructure
2. **Pattern library** - No PII/secrets detection patterns
3. **Hook execution framework** - Guardrails are declarative only
4. **Timeout handling** - No timeout mechanism for validation
5. **Warn mode** - No logging/warning infrastructure

---

## Assessment

The guardrails in agent templates are **declarative documentation** - they describe what SHOULD be validated, but there is **no infrastructure to actually run** these validations automatically.

This work item requires NEW implementation, not just testing.

---

## Tasks

- [x] **T-015.1:** Design guardrail hook interface - **COMPLETE** (wi-sao-015-design.md)
- [x] **T-015.2:** Create pattern library - **COMPLETE**
  - [x] T-015.2.1: Create patterns.yaml with PII/secrets patterns (25+ rules)
  - [x] T-015.2.2: Create schema.json for validation
  - [x] T-015.2.3: Implement pattern loader in Python (loader.py)
  - [x] T-015.2.4: Create patterns.json (PyYAML-free fallback)
- [x] **T-015.3:** Extend pre_tool_use.py with pattern loading - **COMPLETE**
- [x] **T-015.4:** Create post_tool_use.py for output filtering - **COMPLETE**
- [x] **T-015.5:** Update settings.json with PostToolUse hook - **COMPLETE**
- [x] **T-015.6:** Create BDD tests for guardrails - **COMPLETE** (42 tests passed)

---

## Technical Debt

| ID | Description | Severity |
|----|-------------|----------|
| TD-015-001 | Guardrails are declarative-only, no enforcement | MEDIUM |

---

## Discoveries

| ID | Discovery | Impact |
|----|-----------|--------|
| DISC-015-001 | 22 agent files have guardrails sections | Foundation for requirements |
| DISC-015-002 | No hook infrastructure exists | Requires new implementation |
| DISC-015-003 | This is a lower priority (P2) item | Can defer |
| DISC-015-004 | Claude Code supports PreToolUse/PostToolUse hooks | Can intercept tool calls |
| DISC-015-005 | pre_tool_use.py already exists with security patterns | Extend, don't recreate |
| DISC-015-006 | Hooks are async via subprocess model (AC-015-001 satisfied) | Inherent async |

---

## Progress Log

| Date | Task | Status | Evidence |
|------|------|--------|----------|
| 2026-01-12 | T-015.1 Design interface | COMPLETE | `wi-sao-015-design.md` created |
| 2026-01-12 | DISC-015-004 | FOUND | Explore agent research on hook types |
| 2026-01-12 | DISC-015-005 | FOUND | `.claude/hooks/pre_tool_use.py` exists |
| 2026-01-12 | DISC-015-006 | FOUND | Subprocess model provides async |
| 2026-01-12 | T-015.2.1 patterns.yaml | COMPLETE | 25+ validation rules |
| 2026-01-12 | T-015.2.2 schema.json | COMPLETE | JSON Schema for patterns |
| 2026-01-12 | T-015.2.3 loader.py | COMPLETE | Pattern library loader |
| 2026-01-12 | T-015.2.4 patterns.json | COMPLETE | PyYAML-free fallback |
| 2026-01-12 | T-015.3 pre_tool_use.py | COMPLETE | Pattern integration |
| 2026-01-12 | T-015.4 post_tool_use.py | COMPLETE | Output filtering hook |
| 2026-01-12 | T-015.5 settings.json | COMPLETE | PostToolUse hook registered |
| 2026-01-12 | T-015.6 BDD tests | COMPLETE | 42 tests passed |
| 2026-01-12 | WI-SAO-015 | DONE | All acceptance criteria validated |

---

## Deliverables

| File | Description |
|------|-------------|
| `.claude/hooks/patterns/patterns.yaml` | YAML pattern library (primary) |
| `.claude/hooks/patterns/patterns.json` | JSON pattern library (fallback) |
| `.claude/hooks/patterns/schema.json` | JSON Schema for validation |
| `.claude/hooks/patterns/loader.py` | Pattern library loader |
| `.claude/hooks/patterns/__init__.py` | Package exports |
| `.claude/hooks/pre_tool_use.py` | Updated with pattern integration |
| `.claude/hooks/post_tool_use.py` | New output filtering hook |
| `.claude/settings.json` | Updated with PostToolUse hook |
| `.claude/hooks/tests/test_patterns.py` | Pattern library tests (21 tests) |
| `.claude/hooks/tests/test_hooks.py` | Hook integration tests (21 tests) |

---

*Source: Extracted from WORKTRACKER.md lines 1643-1660*
*Started: 2026-01-12*
*Completed: 2026-01-12*
