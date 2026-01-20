# DISC-003: Phantom XML Syntax in Hook Output

> **Type:** Discovery
> **Feature:** [FT-001](./FEATURE-WORKTRACKER.md) Session Hook Cleanup
> **Solution Epic:** [SE-004](../SOLUTION-WORKTRACKER.md) CLI and Claude Code Integration
> **Project:** PROJ-007-jerry-bugs
> **Status:** DOCUMENTED
> **Created:** 2026-01-20
> **Last Updated:** 2026-01-20

---

## Discovery Summary

Investigation revealed that the XML-like tags (`<project-context>`, `<project-required>`, `<project-error>`) and the `hookSpecificOutput` JSON structure used in Jerry's SessionStart hook are **not part of the Claude Code API**. They are phantom conventions that were introduced without basis in the official specification.

---

## Investigation Method

1. Queried Context7 for authoritative Claude Code documentation
2. Searched for `hookSpecificOutput`, `additionalContext`, and XML tag patterns
3. Compared official hook output format with Jerry's implementation
4. Traced origin of XML-like tags through codebase

---

## Findings

### Official Claude Code SessionStart Hook Format

From Context7 (source: `/anthropics/claude-code`), the **standard hook output** is:

```json
{
  "continue": true,
  "suppressOutput": false,
  "systemMessage": "Message for Claude"
}
```

For SessionStart hooks specifically, the documentation shows:
- Simple bash scripts echoing messages to stdout
- Environment variable persistence via `$CLAUDE_ENV_FILE`
- **No special JSON structure required**

### What Jerry Implements (Incorrectly)

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Jerry Framework initialized.\n<project-context>\nProjectActive: PROJ-001\n...</project-context>"
  }
}
```

### Source of `hookSpecificOutput`

The `hookSpecificOutput` structure exists in Claude Code for **PreToolUse** hooks:

```json
{
  "hookSpecificOutput": {
    "permissionDecision": "allow|deny|ask",
    "updatedInput": {"field": "modified_value"}
  }
}
```

This was incorrectly adapted for SessionStart hooks, which don't use this structure.

### Source of XML-like Tags

The tags were introduced in `src/interface/cli/session_start.py` and documented in `CLAUDE.md`:

```markdown
## Project Enforcement (Hard Rule)
### Hook Output Format
The `scripts/session_start.py` hook produces structured output that Claude parses:
#### `<project-context>` - Valid Project Active
```

These tags are **Jerry's convention for Claude (LLM) to parse** - not a Claude Code API requirement.

---

## Impact Analysis

| Aspect | Impact |
|--------|--------|
| **Functionality** | Works by accident - Claude (LLM) parses the text regardless of format |
| **Maintainability** | Creates confusion about what's API vs convention |
| **Architecture** | Couples CLI to non-existent API requirements |
| **Documentation** | CLAUDE.md documents phantom syntax as if it were official |

---

## Root Cause

1. **Assumption:** SessionStart hooks need special JSON structure like PreToolUse
2. **Cargo Culting:** Borrowed `hookSpecificOutput` from PreToolUse without verification
3. **Documentation Drift:** Documented the phantom syntax as if it were required
4. **No Validation:** Never verified against official Claude Code documentation

---

## Correct Approach

### Standard Output Format

```json
{
  "continue": true,
  "systemMessage": "Jerry Framework initialized.\n\nProject: PROJ-007-jerry-bugs\nPath: projects/PROJ-007-jerry-bugs/\nStatus: Valid and configured"
}
```

Or even simpler - just text to stdout that becomes part of the system context.

### Architecture

```
Hook Script (Adapter)          CLI (Generic)
─────────────────────          ─────────────
Transforms for Claude    ←──   Returns clean JSON
Owns format decisions          No Claude-specific code
```

---

## Recommendations

1. **Remove XML-like tags** - Use plain text or structured JSON in `systemMessage`
2. **Remove `hookSpecificOutput`** - Use standard hook output format
3. **Update CLAUDE.md** - Document actual format, not phantom syntax
4. **CLI stays generic** - Output clean JSON, no Claude-specific formatting
5. **Hook script owns adaptation** - Transform CLI JSON → Claude format

---

## Files Affected

| File | Change |
|------|--------|
| `src/interface/cli/session_start.py` | DELETE (rogue file) |
| `scripts/session_start_hook.py` | Rewrite to transform CLI output |
| `CLAUDE.md` | Update hook output documentation |
| `tests/*/test_hook_contract.py` | Update contract tests |

---

## Evidence

### Context7 Query Results

Source: `https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/hook-development/SKILL.md`

> "Standard Hook Output Format with JSON: Defines the required JSON output format for all hooks including control flow flags (continue, suppressOutput) and system message to display to Claude."

No mention of `hookSpecificOutput` for SessionStart hooks.

### Codebase Search

- `hookSpecificOutput` appears only in Jerry code, not in any Claude Code reference
- XML-like tags appear in 36 files, all Jerry-specific documentation

---

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| Discovery | [disc-001](./disc-001-functional-gap-analysis.md) | Functional gap analysis |
| Discovery | [disc-002](./disc-002-architectural-drift-rca.md) | Architectural drift RCA |
| Rogue CLI | `src/interface/cli/session_start.py` | Source of phantom syntax |
| CLAUDE.md | `CLAUDE.md` | Documents phantom syntax |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-20 | Discovery documented via Context7 research | Claude |
