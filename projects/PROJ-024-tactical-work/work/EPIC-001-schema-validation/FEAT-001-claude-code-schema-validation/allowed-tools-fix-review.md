# Security Review: allowed-tools Task-to-Agent Rename + MCP Warning Removal

**Reviewer:** eng-security
**Date:** 2026-03-26
**Scope:** STORY-007 (Task -> Agent rename in SKILL.md files) + MCP warning removal in validate_frontmatter_command.py
**Criticality:** C2 (standard -- reversible, < 10 files, no API changes)

---

## Overall Result: PASS

Both changes are correct and complete. No security issues found. No dead code left behind.

---

## Change 1: Task -> Agent Rename in SKILL.md allowed-tools

**Verdict: PASS**

### What Was Verified

The six modified SKILL.md files were read directly and their `allowed-tools` frontmatter fields inspected. A codebase-wide grep (`allowed-tools:.*Task`) across all `skills/*/SKILL.md` files returned zero matches, confirming no file was missed.

### Per-File Findings

| File | allowed-tools field | Task present | Agent present | Status |
|------|---------------------|:------------:|:-------------:|--------|
| skills/problem-solving/SKILL.md | `Read, Write, Edit, Glob, Grep, Bash, Agent, WebSearch, WebFetch, mcp__context7__*, mcp__memory-keeper__*` | No | Yes | PASS |
| skills/worktracker/SKILL.md | `Read, Write, Glob, Agent, Edit` | No | Yes | PASS |
| skills/nasa-se/SKILL.md | `Read, Write, Edit, Glob, Grep, Bash, Agent, WebSearch, WebFetch, mcp__context7__*, mcp__memory-keeper__*` | No | Yes | PASS |
| skills/orchestration/SKILL.md | `Read, Write, Edit, Glob, Grep, Bash, Agent, WebSearch, WebFetch, mcp__memory-keeper__*` | No | Yes | PASS |
| skills/transcript/SKILL.md | `Read, Write, Glob, Agent, Bash(*), mcp__memory-keeper__*` | No | Yes | PASS |
| skills/user-experience/SKILL.md | `Read, Write, Edit, Glob, Grep, Bash, Agent, WebSearch, WebFetch, mcp__context7__*, mcp__memory-keeper__*` | No | Yes | PASS |

### Security Relevance

The `Task` tool enables recursive subagent spawning (P-003 violation, H-35). Its presence in a SKILL.md `allowed-tools` field would grant skill-level agents the ability to delegate recursively, bypassing the single-level orchestrator-worker topology enforced by H-01. The rename to `Agent` preserves delegation capability while restricting it to the correct platform primitive. No skill was missed.

---

## Change 2: MCP Warning Removal from validate_frontmatter_command.py

**Verdict: PASS -- clean removal, no dead code**

### What Was Verified

The full handler file was read (`src/agents/application/commands/validate_frontmatter_command.py`, 639 lines). The `_validate_skill_file` method was inspected end-to-end.

### Findings

The warning block that previously fired when `mcp__*` tools appeared in `allowed-tools` has been replaced with a single explanatory comment at lines 627-629:

```python
# NOTE: MCP tools (mcp__*) in allowed-tools are valid per Anthropic platform
# docs (https://platform.claude.com/docs/en/agent-sdk/custom-tools).
# Previously warned here, but the warning was a false positive.
```

No residual logic referencing `mcp_tools_in_allowed_tools` exists anywhere in the `src/` tree (confirmed by grep). The removal is complete.

The analogous check in `_validate_agent_file` (lines 491-507) correctly remains. That check fires on the `tools` field (agent frontmatter) where MCP tools genuinely do not belong -- they should be declared in `mcpServers` instead. The two fields are structurally distinct:

- Agent `tools` field: MCP tools are invalid here. Warning retained. Correct.
- Skill `allowed-tools` field: MCP tools are valid per platform docs. Warning removed. Correct.

There is no dead code, no unreachable branch, and no orphaned constant or regex related to the removed check.

---

## Summary

| Check | Result | Evidence |
|-------|--------|----------|
| `grep allowed-tools:.*Task` across all SKILL.md files | PASS | Zero matches returned |
| All 6 named SKILL.md files contain `Agent` in allowed-tools | PASS | Direct read of each file |
| `mcp_tools_in_allowed_tools` identifier absent from src/ | PASS | Zero matches returned |
| No dead code in _validate_skill_file after removal | PASS | Full method read; clean comment in place |
| Agent `tools` field MCP warning (unrelated) still present | PASS | Correctly retained at lines 491-507 |

No issues require remediation.
