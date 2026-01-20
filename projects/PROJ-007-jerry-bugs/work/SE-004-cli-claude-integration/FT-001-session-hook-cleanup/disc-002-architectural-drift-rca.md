# DISC-002: Architectural Drift Root Cause Analysis

> **Type:** Discovery
> **Feature:** [FT-001](./FEATURE-WORKTRACKER.md) Session Hook Cleanup
> **Solution Epic:** [SE-004](../SOLUTION-WORKTRACKER.md) CLI and Claude Code Integration
> **Project:** PROJ-007-jerry-bugs
> **Status:** DOCUMENTED
> **Created:** 2026-01-15
> **Last Updated:** 2026-01-15

---

## Discovery Summary

Root Cause Analysis identified how `cli/session_start.py` came into existence and why it deviates from the established hexagonal architecture.

## Timeline of Events

1. **Original Design**: `session_start_hook.py` was a wrapper that called the CLI
2. **Requirement**: Session hook needed to output JSON format for Claude Code
3. **Pressure**: Quick fix needed to make hook work
4. **Drift**: Instead of extending `CLIAdapter`, a new `cli/session_start.py` was created
5. **Consequence**: Direct infrastructure imports, duplicate functionality

## Root Causes

### Primary: Lack of Extension Point
The `CLIAdapter` and `cli/main.py` did not provide a way to output hook-specific JSON format. The fastest path was to create a new file.

### Secondary: Documentation Gap
The docstring in `cli/session_start.py` still says "Structured XML-like tags" but the code outputs JSON wrapping those tags. This indicates the change was made hastily without updating documentation.

### Tertiary: Test Inertia
Existing tests for the hook were written against `cli/session_start.py`. Changing architecture would require test migration, adding friction.

## Evidence

**Docstring vs Implementation Mismatch:**
```python
# Docstring says (lines 10-14):
"""
Output Format:
    Structured XML-like tags that Claude parses to determine action:
"""

# But implementation does (line 385-386):
print(out.to_json())  # Outputs JSON, not plain text
```

**Comment in hook wrapper (line 128):**
```python
# Output stdout (the JSON from jerry-session-start)
```
This comment was added when the architecture shifted.

## Lessons Learned

1. **Extension points matter** - CLI should support multiple output formats
2. **Architecture enforcement** - Need automated checks for layer boundary violations
3. **Quick fixes accumulate** - Technical debt compounds when not addressed

## Recommended Guardrails

1. Add architecture tests to CI pipeline
2. Enforce "no infrastructure imports in interface layer" via linting
3. Document output format options as first-class concern

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| Discovery | [disc-001](./disc-001-functional-gap-analysis.md) | Functional gap analysis |
| Technical Debt | [td-001](./td-001-session-start-violates-hexagonal.md) | Architecture violation |
| Hook Wrapper | `scripts/session_start_hook.py` | Hook that calls CLI |
| Rogue CLI | `src/interface/cli/session_start.py` | Result of drift |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-15 | RCA documented | Claude |
