# Barrier 1 Handoff: SPIKE-001 → SPIKE-002

> **Direction:** spike-001 (SDK vs CLI) → spike-002 (Worktree Lifecycle)
> **Barrier:** barrier-1 (Phase 1 Cross-Pollination)
> **Date:** 2026-02-20
> **Source:** agent-a-001-research.md

---

## Purpose

Provide SPIKE-002's Phase 2 analysis (session lifecycle design) with the instance management capabilities and constraints of each approach, so the lifecycle can be designed with knowledge of what each approach supports.

---

## Key Findings for SPIKE-002

### Three Approaches Available

1. **Anthropic Python SDK** — Direct API, custom tools only, no built-in file/shell tools, manual session persistence
2. **Claude Agent SDK** (`claude-agent-sdk`) — Python wrapper around Claude Code CLI subprocess, full tool surface, programmatic subagents, hooks, session resume/fork, `cwd` per instance
3. **Claude Code CLI** — Subprocess spawning, full tool surface, `--worktree` flag, `--resume`/`--continue`, `--output-format json`, `--max-budget-usd`

### Session Binding Capabilities Per Approach

| Capability | Anthropic SDK | Agent SDK | CLI |
|-----------|--------------|-----------|-----|
| Set working directory | N/A (your process) | `cwd` option | Process `cwd` or `--worktree` |
| Set environment variables | N/A (your process) | `env` dict in options | Subprocess `env` param |
| Resume session by ID | Manual serialization | `resume="<id>"` | `--resume <id>` |
| Continue last session | Manual | `continue_conversation=True` | `--continue` |
| Fork session | Manual copy | `fork_session=True` | `--fork-session` |
| Set allowed tools | Tool schema list | `allowed_tools` list | `--allowedTools` |
| Set system prompt | `system` param | `system_prompt` option | `--system-prompt` / `--append-system-prompt` |
| Max turns | Manual loop limit | `max_turns` option | `--max-turns` |
| Cost cap | Manual tracking | Not documented | `--max-budget-usd` |

### Critical Constraints for Lifecycle Design

1. **Agent SDK `cwd` option provides the cleanest per-instance working directory isolation** — no shell `cd` needed, set programmatically per `query()` call.

2. **Agent SDK `env` dict allows per-instance `JERRY_PROJECT`** — the lifecycle can set this without subprocess env manipulation.

3. **CLI `--worktree` creates worktrees at `.claude/worktrees/<name>/`** with branch name `worktree-<name>` — this does NOT match Jerry's `feat/proj-NNN-slug` convention. **SPIKE-002 should design its own worktree management, not rely on `--worktree`.**

4. **Session resume/fork is available in both Agent SDK and CLI** — the lifecycle can support long-running multi-turn workflows by capturing session IDs.

5. **Hooks (Agent SDK only)** — `PreToolUse` and `SubagentStop` hooks enable deterministic quality gating within instances. CLI has file-based lifecycle hooks but not in-process.

6. **In-process MCP servers (Agent SDK only)** — Custom tools can be defined as Python functions and injected per instance without external processes.

7. **Cost control differs:** Agent SDK has no documented per-instance budget cap. CLI has `--max-budget-usd`. Anthropic SDK requires manual tracking.

### Hybrid Recommendation from SPIKE-001

The recommended architecture is:
- **Agent SDK for orchestrator** (hooks, MCP, programmatic control)
- **Agent SDK `query()` or CLI subprocess for workers** (per-instance `cwd` + `env`)
- **Session forking for parallel analyses** after initial context gathering
- **Anthropic SDK for lightweight metadata/scoring tasks** (lower token overhead)

### What SPIKE-002 Phase 2 Should Do With This

1. Design session lifecycle state machine for **Agent SDK `query()` as the primary dispatch mechanism** — `cwd` for working directory, `env` for `JERRY_PROJECT`, `resume` for session continuation
2. Also design the **CLI subprocess fallback** — process spawning, stdout capture, `--output-format json` parsing, `--resume` for continuation
3. Factor in that **provisioning (uv sync, hooks) happens BEFORE instance binding** — the approach doesn't change provisioning
4. Design monitoring patterns that work for both: Agent SDK returns async messages; CLI returns process exit + JSON output

---

*Source: agent-a-001-research.md (SPIKE-001 Phase 1)*
*Generated: 2026-02-20*
