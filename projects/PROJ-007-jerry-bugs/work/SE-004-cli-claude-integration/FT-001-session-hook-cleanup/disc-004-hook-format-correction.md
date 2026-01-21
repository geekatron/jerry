# DISC-004: Hook Output Format Correction

> **Type:** Discovery (Correction)
> **Feature:** [FT-001](./FEATURE-WORKTRACKER.md) Session Hook Cleanup
> **Solution Epic:** [SE-004](../SOLUTION-WORKTRACKER.md) CLI and Claude Code Integration
> **Project:** PROJ-007-jerry-bugs
> **Status:** DOCUMENTED
> **Created:** 2026-01-20
> **Last Updated:** 2026-01-20

---

## Discovery Summary

**CORRECTION**: DISC-003 incorrectly labeled Jerry's `hookSpecificOutput.additionalContext` format as "phantom syntax." Deep research with authoritative sources reveals this format IS the official Claude Code Advanced JSON output format for SessionStart hooks.

---

## 5W1H Analysis

### What Happened?

1. DISC-003 concluded that `hookSpecificOutput` was incorrectly cargo-culted from PreToolUse hooks
2. This was based on incomplete evidence (Hook SDK TypeScript types)
3. Deep research revealed the format IS documented in official Anthropic docs
4. A bug in Claude Code v2.0.65 caused stdout to be silently dropped (Issue #13650)
5. The bug was fixed in v2.0.76

### Who Is Affected?

- Jerry Framework SessionStart hook implementation
- EN-001 task definitions
- Documentation referencing "phantom syntax"

### Where Is the Evidence?

| Source | URL | Finding |
|--------|-----|---------|
| Official Anthropic Docs | https://code.claude.com/docs/en/hooks#advanced:-json-output | Documents `hookSpecificOutput.additionalContext` for SessionStart |
| GitHub Issue #13650 | https://github.com/anthropics/claude-code/issues/13650 | Bug where stdout was dropped, fixed in v2.0.76 |
| Hook SDK (incomplete) | Context7 `/anthropics/claude-code` | Only showed PreToolUse example, missing SessionStart |

### When Did This Occur?

- **2026-01-09**: ADR-002 designed XML tags in plain stdout
- **2026-01-15**: DISC-003 created labeling format as "phantom"
- **2026-01-20**: Deep research corrected understanding

### Why Was DISC-003 Wrong?

1. **Incomplete source**: Hook SDK TypeScript types are incomplete
2. **Missing context**: Bug #13650 caused confusion about what works
3. **Assumption cascade**: Once labeled "phantom," subsequent analysis built on that assumption

### How Should We Proceed?

1. Use the **Advanced JSON output format** (user's explicit decision)
2. Keep `hookSpecificOutput.additionalContext` structure
3. Focus EN-001 on architecture cleanup, not format change
4. Add comprehensive BDD tests for contract compliance

---

## Official Claude Code Hook Formats

### SessionStart - Advanced JSON Output (CORRECT)

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "My additional context here"
  }
}
```

**Source:** https://code.claude.com/docs/en/hooks#advanced:-json-output

### SessionStart Limitations

> "SessionStart hooks only support the `additionalContext` field via `hookSpecificOutput`. They cannot use decision control, `continue`, or `stopReason` fields since they run at session initialization and cannot block session startup."

**Source:** https://code.claude.com/docs/en/hooks#advanced:-json-output

### Field Definitions

| Field | Type | Purpose | Who Sees It |
|-------|------|---------|-------------|
| `continue` | boolean | Control flow (not for SessionStart) | System |
| `stopReason` | string | Why hook stopped (not for SessionStart) | System |
| `suppressOutput` | boolean | Hide output from transcript | System |
| `systemMessage` | string | Warning shown to USER | **User (terminal)** |
| `additionalContext` | string | Content added to CLAUDE's context | **Claude (LLM)** |

### Plain Text Alternative (Also Valid)

SessionStart hooks can output plain text to stdout instead of JSON:

```bash
#!/bin/bash
echo "My context message for Claude"
```

This text also goes to Claude's context.

---

## What Jerry Currently Implements

### `src/interface/cli/session_start.py` (Lines 66-72)

```python
def to_json(self) -> str:
    return json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": content
        }
    })
```

**Verdict:** This format IS CORRECT per official documentation.

### XML Tags Inside `additionalContext`

Jerry uses XML-like tags to structure the content:

```
<project-context>
ProjectActive: PROJ-007-jerry-bugs
ProjectPath: projects/PROJ-007-jerry-bugs/
</project-context>
```

**Verdict:** This is VALID per Anthropic's prompt engineering best practices for structuring data for LLMs.

---

## What DISC-003 Got Wrong

| Claim in DISC-003 | Actual Truth |
|-------------------|--------------|
| `hookSpecificOutput` is not part of Claude Code API for SessionStart | IS documented at code.claude.com/docs/en/hooks |
| Format was "cargo-culted" from PreToolUse | Format IS the official Advanced JSON format |
| "Phantom syntax" created without basis | Based on official specification |
| SDK shows it only for PreToolUse | SDK is incomplete, official docs are authoritative |

---

## Impact on EN-001

### What Changes

| Original EN-001 Task | Revised Understanding |
|---------------------|----------------------|
| Remove `hookSpecificOutput` | **KEEP** - It's the correct format |
| Remove XML tags | **KEEP** - Valid prompt engineering |
| Use standard `systemMessage` | **NO** - That's for user warnings, not Claude context |

### What Stays the Same

1. **Architecture cleanup**: Delete `cli/session_start.py` (violates hexagonal)
2. **Single entry point**: Hook adapter calls `jerry projects context --json`
3. **Transformation layer**: Hook adapter transforms CLI JSON to hook format
4. **Local context support**: Add `.jerry/local/context.toml` reading

### New Focus

EN-001 should focus on:
1. **Architectural compliance** - Not format changes
2. **BDD test coverage** - Unit, Integration, System, E2E, Contract, Architecture
3. **Separation of concerns** - CLI generic, hook adapter handles transformation

---

## XML Tags: Still Valid

The XML-like tags (`<project-context>`, `<project-required>`, `<project-error>`) are:

1. **Not Claude Code API syntax** - They're content formatting
2. **Valid for Claude (LLM)** - Anthropic recommends XML for structuring prompts
3. **A Jerry convention** - For Claude to parse project state

**Decision:** Keep XML tags inside `additionalContext` - they help Claude parse project information.

---

## Evidence: Bug #13650

### Issue Description

> "The SessionStart hook's stdout is being silently dropped in version 2.0.65"

### Resolution

> "Fixed in v2.0.76 - SessionStart stdout now properly captured"

### Implication

The confusion about "what works" for SessionStart hooks was partially due to this bug. Before v2.0.76, both plain text AND JSON output were being dropped.

---

## Corrected Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code Hook System                       │
└───────────────────────────────────┬─────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│              scripts/session_start_hook.py                       │
│  ADAPTER LAYER - Transforms CLI output for Claude                │
│                                                                  │
│  Output Format (Official Claude Code Advanced JSON):             │
│  {                                                               │
│    "hookSpecificOutput": {                                       │
│      "hookEventName": "SessionStart",                            │
│      "additionalContext": "Jerry Framework initialized.\n..."    │
│    }                                                             │
│  }                                                               │
└───────────────────────────────────┬─────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                   jerry projects context --json                  │
│  GENERIC CLI - Clean JSON output (no hook-specific format)       │
└───────────────────────────────────┬─────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Application Layer                           │
│  RetrieveProjectContextQuery                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| Discovery (INCORRECT) | [disc-003](./disc-003-phantom-xml-syntax.md) | Contains incorrect "phantom syntax" conclusion |
| Enabler | [en-001](./en-001-session-hook-tdd.md) | Needs revision based on this discovery |
| ADR | [ADR-002](../../../../design/ADR-002-project-enforcement.md) | Original design (XML in stdout) |
| Official Docs | https://code.claude.com/docs/en/hooks | Authoritative source |
| Bug Report | https://github.com/anthropics/claude-code/issues/13650 | stdout dropping bug |

---

## Recommendations

1. **Update DISC-003** - Add correction notice pointing to this discovery
2. **Revise EN-001** - Focus on architecture, keep `hookSpecificOutput` format
3. **Keep XML tags** - Valid prompt engineering for Claude
4. **Add Contract Tests** - Verify output matches official spec
5. **Test on v2.0.76+** - Ensure bug fix is in effect

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-20 | Discovery documented with authoritative sources | Claude |
