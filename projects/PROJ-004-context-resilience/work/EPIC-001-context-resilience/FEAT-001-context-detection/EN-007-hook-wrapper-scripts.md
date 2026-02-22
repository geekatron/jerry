# EN-007: Hook Wrapper Scripts + hooks.json Registration

> **Type:** enabler
> **Status:** completed
> **Priority:** critical
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-19
> **Due:** --
> **Completed:** 2026-02-21
> **Parent:** FEAT-001
> **Owner:** --
> **Effort:** 1.5-2h

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Technical scope |
| [Wrapper Pattern](#wrapper-pattern) | Script template |
| [Acceptance Criteria](#acceptance-criteria) | BDD scenarios and checklist |
| [Technical Approach](#technical-approach) | Implementation approach |
| [Dependencies](#dependencies) | Relationships |
| [History](#history) | Status changes |

---

## Summary

Create the four thin hook wrapper scripts and update `hooks/hooks.json` to register all hook events. Each wrapper is ~10 lines: reads stdin from Claude Code, calls `jerry hooks <event>` via subprocess, pipes stdout back. All logic lives in bounded context + CLI commands (EN-003, EN-004, EN-006). Scripts contain NO imports from `src/`.

---

## Wrapper Pattern

```python
#!/usr/bin/env python3
"""<HookEvent> hook wrapper. Delegates to jerry hooks <event>."""
import subprocess
import sys

result = subprocess.run(
    ["uv", "run", "--directory", "${CLAUDE_PLUGIN_ROOT}", "jerry", "--json", "hooks", "<event>"],
    input=sys.stdin.buffer.read(),
    capture_output=True,
    timeout=<N>,  # 4s for 5s hooks, 9s for 10s hooks
)
sys.stdout.buffer.write(result.stdout)
sys.exit(0)  # Always exit 0 (fail-open)
```

**Files:**

| Script | Hook Event | Subprocess Timeout | hooks.json Timeout |
|--------|-----------|-------------------|-------------------|
| `hooks/user-prompt-submit.py` | UserPromptSubmit | 4s | 5000ms |
| `hooks/session-start.py` | SessionStart | 9s | 10000ms |
| `hooks/pre-compact.py` | PreCompact | 9s | 10000ms |
| `hooks/pre-tool-use.py` | PreToolUse | 4s | 5000ms |

---

## Acceptance Criteria

### BDD Scenarios (pytest-bdd)

```gherkin
Feature: Hook wrapper scripts delegate to CLI

  Scenario Outline: Wrapper script calls correct CLI command
    Given a <hook_event> JSON payload on stdin
    When hooks/<script_name> is executed
    Then it should call "jerry --json hooks <cli_command>" via subprocess
    And pipe stdin to the subprocess
    And pipe stdout back to the caller
    And always exit with code 0

    Examples:
      | hook_event        | script_name             | cli_command    |
      | UserPromptSubmit  | user-prompt-submit.py   | prompt-submit  |
      | SessionStart      | session-start.py        | session-start  |
      | PreCompact        | pre-compact.py          | pre-compact    |
      | PreToolUse        | pre-tool-use.py         | pre-tool-use   |

  Scenario: Wrapper contains no src/ imports
    Given hooks/user-prompt-submit.py
    When I inspect the file contents
    Then it should not contain "from src" or "import src"
    And it should be 15 lines or fewer

  Scenario: hooks.json correctly registers all hooks
    Given hooks/hooks.json
    Then SessionStart should point to "hooks/session-start.py" with timeout 10000
    And UserPromptSubmit should point to "hooks/user-prompt-submit.py" with timeout 5000
    And PreCompact should exist with timeout 10000
    And PreToolUse should point to "hooks/pre-tool-use.py" with timeout 5000

  Scenario: Old session_start_hook.py retired
    When I check the scripts/ directory
    Then scripts/session_start_hook.py should be removed or marked as retired
```

### Acceptance Checklist

- [x] `hooks/user-prompt-submit.py` created (<=15 lines, no `src/` imports, exits 0)
- [x] `hooks/session-start.py` created (<=15 lines, no `src/` imports, exits 0)
- [x] `hooks/pre-compact.py` created (<=15 lines, no `src/` imports, exits 0)
- [x] `hooks/pre-tool-use.py` created (<=15 lines, no `src/` imports, exits 0)
- [x] `hooks/hooks.json` updated: SessionStart -> `hooks/session-start.py`, PreCompact added, PreToolUse -> `hooks/pre-tool-use.py`
- [x] `scripts/session_start_hook.py` retired
- [x] Subprocess timeout 1s below hook timeout for each wrapper
- [x] All wrappers correctly pipe stdin/stdout
- [x] End-to-end test: wrapper with sample JSON stdin returns expected output

---

## Technical Approach

Create four thin hook wrapper scripts and update `hooks/hooks.json` to register all hook events. Each wrapper reads stdin from Claude Code, calls `jerry hooks <event>` via subprocess, and pipes stdout back. All logic lives in bounded context and CLI commands. Scripts contain no imports from `src/`. Completed as part of parent feature.

---

## Dependencies

**Depends On:** EN-006 (CLI commands must exist before wrappers can call them)

**Enables:** ST-003 (system operational end-to-end)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-19 | Claude | pending | Enabler created from CWI-11. |
| 2026-02-21 | Claude | completed | Implemented and verified as part of FEAT-001. |
