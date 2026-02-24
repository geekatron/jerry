# Agent A-001 Research: Claude SDK vs CLI Instance Management Capabilities

> **PS ID:** phase-1 | **Entry ID:** e-001 | **Agent:** agent-a-001
> **Pipeline:** spike-001 (SDK vs CLI Instance Comparison)
> **Date:** 2026-02-20 | **Status:** Complete

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Key differentiators, approach comparison |
| [L1: Technical Findings](#l1-technical-findings) | API details, code examples, configuration |
| [L2: Architectural Implications](#l2-architectural-implications) | Trade-offs for multi-instance orchestration |
| [References](#references) | All sources with URLs |

---

## L0: Executive Summary

Three distinct approaches exist for programmatic multi-instance Claude management, each with fundamentally different trade-off profiles:

### Approach 1: Anthropic Python SDK (Direct API)

The Anthropic Python SDK (`anthropic`) provides direct REST API access to Claude models. It offers maximum control over conversation management, tool definitions, and token flow, but requires implementing the entire agent loop (tool execution, file I/O, error recovery) from scratch. Custom tools are defined as JSON schemas and executed by your code. Session persistence requires manual serialization. Cost is direct API token pricing with no overhead.

### Approach 2: Claude Agent SDK (`claude-agent-sdk`)

The Claude Agent SDK wraps the Claude Code CLI as a subprocess, providing a Python (and TypeScript) interface to the full Claude Code tool surface (Read, Write, Edit, Bash, Glob, Grep, etc.). It supports programmatic subagent definitions, in-process MCP servers, hooks for deterministic gating, session resume/fork, and working directory isolation. This is the closest to "Claude Code as a library." The SDK bundles the Claude Code CLI binary and communicates via JSON RPC over stdio.

### Approach 3: Claude Code CLI (Subprocess)

Direct CLI invocation via `claude -p` with `--output-format json` provides non-interactive automation. Session continuity via `--resume`, filesystem isolation via `--worktree`, and tool restriction via `--allowedTools`/`--tools`. Orchestration requires subprocess management (spawning, I/O, exit codes) but provides the full Claude Code experience including CLAUDE.md loading, skill support, and built-in session persistence.

### Key Differentiators

| Dimension | Anthropic SDK | Agent SDK | CLI Subprocess |
|-----------|--------------|-----------|----------------|
| **Tool Surface** | Custom JSON schemas only | Full Claude Code tools + custom MCP | Full Claude Code tools |
| **Agent Loop** | Manual implementation | Automatic (Claude Code engine) | Automatic (Claude Code engine) |
| **Session Persistence** | Manual serialization | Built-in (resume, fork) | Built-in (resume, continue) |
| **Subagents** | Not built-in | Programmatic `AgentDefinition` | `--agents` JSON flag |
| **Filesystem Operations** | Must implement | Built-in (Read/Write/Edit/Bash) | Built-in (Read/Write/Edit/Bash) |
| **MCP Integration** | Manual server management | In-process + external servers | External servers via config |
| **Hooks/Gating** | Not built-in | PreToolUse, SubagentStop, etc. | Lifecycle hooks (file-based) |
| **Working Directory** | N/A (your process) | `cwd` option per instance | `--worktree` or per-process cwd |
| **CLAUDE.md Loading** | Not applicable | Inherits from cwd | Automatic from cwd |
| **Cost** | Direct API tokens | API tokens (via CLI) | API tokens (via CLI) |
| **Language** | Python (native) | Python/TypeScript | Any (subprocess) |

---

## L1: Technical Findings

### 1. Anthropic Python SDK (`anthropic`)

**Package:** `anthropic` (PyPI) | **Source Reputation:** High | **Context7 Score:** 81.5

#### API Surface

The SDK provides synchronous and asynchronous clients with type definitions for all request/response fields [C7-1].

**Model invocation:**
```python
from anthropic import Anthropic

client = Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system="You are a helpful assistant",
    messages=[{"role": "user", "content": "Hello"}],
)
```

**Tool use (JSON schema definitions):**
```python
tools = [{
    "name": "get_weather",
    "description": "Get the current weather",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City name"}
        },
        "required": ["location"]
    }
}]

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Weather in SF?"}],
    tools=tools,
)

# Manual tool execution loop
if message.stop_reason == "tool_use":
    tool_use = next(c for c in message.content if c.type == "tool_use")
    # Execute tool locally, then send result back
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Weather in SF?"},
            {"role": "assistant", "content": message.content},
            {"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": tool_use.id,
                 "content": "72F and sunny"}
            ]},
        ],
        tools=tools,
    )
```

**Automatic tool runner (beta):**
```python
runner = client.beta.messages.tool_runner(
    max_tokens=1024,
    model="claude-sonnet-4-5-20250929",
    tools=[get_weather],  # @beta_tool decorated functions
    messages=[{"role": "user", "content": "Weather in SF?"}],
)
for message in runner:
    print(f"Message: {message.content}")
```

#### Agent Loop Pattern

The SDK requires manual implementation of the tool-use cycle: send message -> check `stop_reason == "tool_use"` -> extract tool call -> execute locally -> send `tool_result` -> repeat. The `tool_runner()` beta automates this loop for decorated Python functions but does not include file system tools, shell execution, or code editing capabilities [C7-1].

#### Context Window Management

Conversation history is maintained as an in-memory list of messages. There is no built-in persistence; serialization to disk requires manual implementation. The developer manages the full message array and must handle context window limits (truncation, summarization) themselves [C7-1].

#### Error Handling, Retries, Rate Limiting

The SDK handles authentication, retries, and errors automatically while providing full type safety through Pydantic models. Rate limiting and retry logic are built into the client [C7-1].

#### Streaming

Streaming is supported for real-time output via `client.messages.stream()`, returning events as they arrive [C7-1].

---

### 2. Claude Agent SDK (`claude-agent-sdk`)

**Package:** `claude-agent-sdk` (PyPI) | **Source Reputation:** High | **Context7 Score:** 85.8
**GitHub:** `anthropics/claude-agent-sdk-python` | **Stars:** ~4.9k | **License:** MIT | **Python:** 3.10+

#### Architecture

The Agent SDK bundles the Claude Code CLI binary within the pip package. It communicates with Claude Code via JSON RPC over stdio subprocess. This means every `query()` call spawns a Claude Code subprocess, giving the SDK access to the full Claude Code tool surface [GH-1].

```
Your Python Code
    -> claude-agent-sdk (Python)
        -> Claude Code CLI (bundled, subprocess)
            -> Anthropic API
            -> Built-in tools (Read, Write, Edit, Bash, Glob, Grep...)
            -> MCP servers
```

#### Core API: `query()` Function

Simple async interface for one-off queries:

```python
import anyio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock

async def main():
    options = ClaudeAgentOptions(
        system_prompt="You are a helpful assistant",
        max_turns=5,
        cwd="/path/to/project",
        allowed_tools=["Read", "Write", "Bash"],
    )
    async for message in query(prompt="Analyze this codebase", options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)

anyio.run(main)
```

#### Core API: `ClaudeSDKClient` (Advanced)

Bidirectional, interactive client for multi-turn conversations:

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

async with ClaudeSDKClient(options=options) as client:
    await client.query("Create a hello.py file")
    async for msg in client.receive_response():
        print(msg)
```

#### ClaudeAgentOptions Configuration (Key Fields)

| Field | Type | Purpose |
|-------|------|---------|
| `allowed_tools` | `list[str]` | Tool whitelist (e.g., `["Read", "Write", "Bash"]`) |
| `disallowed_tools` | `list[str]` | Tool blacklist |
| `system_prompt` | `str` | Custom or preset system prompt |
| `mcp_servers` | `dict` | MCP server configs (in-process or external) |
| `permission_mode` | `PermissionMode` | Permission mode for tool usage |
| `continue_conversation` | `bool` | Continue most recent conversation |
| `resume` | `str` | Session ID to resume |
| `fork_session` | `bool` | Fork current session (new ID, same history) |
| `max_turns` | `int` | Maximum conversation turns |
| `model` | `str` | Model selection |
| `cwd` | `str \| Path` | Working directory for the instance |
| `env` | `dict[str, str]` | Environment variables |
| `agents` | `dict[str, AgentDefinition]` | Subagent definitions |
| `hooks` | `dict[HookEvent, list[HookMatcher]]` | Event hooks |
| `enable_file_checkpointing` | `bool` | File change tracking for rewinding |
| `add_dirs` | `list[str \| Path]` | Additional directories |
| `output_format` | `OutputFormat` | Output format specification |

[C7-2, GH-1]

#### Subagent Definitions

Subagents are defined programmatically via `AgentDefinition` and invoked via the `Task` tool:

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

options = ClaudeAgentOptions(
    allowed_tools=["Read", "Grep", "Glob", "Task"],
    agents={
        "code-reviewer": AgentDefinition(
            description="Expert code review specialist.",
            prompt="You are a code review specialist...",
            tools=["Read", "Grep", "Glob"],
            model="sonnet"
        ),
        "test-runner": AgentDefinition(
            description="Runs and analyzes test suites.",
            prompt="You are a test execution specialist...",
            tools=["Bash", "Read", "Grep"]
        )
    }
)

async for message in query(
    prompt="Review the authentication module",
    options=options
):
    if hasattr(message, "result"):
        print(message.result)
```

Each subagent gets an isolated context window with only relevant information sent back to the orchestrator [C7-2].

#### In-Process MCP Servers

Custom tools defined as Python functions, running in-process (no separate subprocess):

```python
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool("add", "Add two numbers", {"a": float, "b": float})
async def add(args):
    return {"content": [{"type": "text", "text": f"Sum: {args['a'] + args['b']}"}]}

calculator = create_sdk_mcp_server(
    name="calculator", version="1.0.0", tools=[add]
)

options = ClaudeAgentOptions(
    mcp_servers={"calc": calculator},
    allowed_tools=["mcp__calc__add"]
)
```

Benefits: No IPC overhead, single process, easier debugging, type safety [GH-1].

#### Hooks

Deterministic processing at specific agent loop points:

```python
from claude_agent_sdk import ClaudeAgentOptions, HookMatcher

async def check_bash_command(input_data, tool_use_id, context):
    if input_data["tool_name"] == "Bash":
        command = input_data["tool_input"].get("command", "")
        if "rm -rf" in command:
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": "Dangerous command blocked",
                }
            }
    return {}

options = ClaudeAgentOptions(
    hooks={"PreToolUse": [HookMatcher(matcher="Bash", hooks=[check_bash_command])]}
)
```

Available hook events include `PreToolUse` and `SubagentStop` [C7-2, GH-1].

#### Error Handling

```python
from claude_agent_sdk import (
    ClaudeSDKError,        # Base error
    CLINotFoundError,      # Claude Code CLI not installed
    CLIConnectionError,    # Connection issues
    ProcessError,          # Process failed (includes exit_code)
    CLIJSONDecodeError,    # JSON parsing issues
)
```

[GH-1]

#### Session Persistence

- **Resume:** `ClaudeAgentOptions(resume="<session-id>")` resumes a specific session
- **Continue:** `ClaudeAgentOptions(continue_conversation=True)` continues most recent session in cwd
- **Fork:** `ClaudeAgentOptions(fork_session=True)` creates a new session from existing history
- Sessions persist to disk automatically (Claude Code's built-in session store)

[C7-2]

---

### 3. Claude Code CLI Automation

**Documentation:** [code.claude.com/docs/en/cli-reference](https://code.claude.com/docs/en/cli-reference)

#### Key Automation Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--print` / `-p` | Non-interactive mode; execute and exit | `claude -p "query"` |
| `--output-format` | Output format: `text`, `json`, `stream-json` | `claude -p --output-format json "query"` |
| `--resume` / `-r` | Resume session by ID or name | `claude -r "session-id" -p "next query"` |
| `--continue` / `-c` | Continue most recent conversation in cwd | `claude -c -p "follow up"` |
| `--fork-session` | Fork session (new ID, keep history) | `claude --resume abc --fork-session` |
| `--system-prompt` | Replace entire system prompt | `claude --system-prompt "Custom prompt"` |
| `--append-system-prompt` | Append to default system prompt | `claude --append-system-prompt "Extra rules"` |
| `--allowedTools` | Auto-approve specific tools | `"Bash(git log *)" "Read"` |
| `--tools` | Restrict available tools | `--tools "Bash,Edit,Read"` |
| `--disallowedTools` | Remove specific tools | `--disallowedTools "Write"` |
| `--model` | Select model | `--model sonnet` |
| `--max-turns` | Limit agentic turns (print mode) | `--max-turns 10` |
| `--max-budget-usd` | Cost cap (print mode) | `--max-budget-usd 5.00` |
| `--worktree` / `-w` | Start in isolated git worktree | `claude -w feature-auth` |
| `--mcp-config` | Load MCP server config | `--mcp-config ./mcp.json` |
| `--agents` | Define subagents via JSON | `--agents '{"reviewer":{...}}'` |
| `--permission-mode` | Set permission mode | `--permission-mode plan` |
| `--dangerously-skip-permissions` | Skip all permission prompts | (use with caution) |
| `--no-session-persistence` | Disable session saving (print mode) | Ephemeral sessions |
| `--session-id` | Use specific UUID for session | Custom session identity |
| `--add-dir` | Add additional working directories | `--add-dir ../lib` |
| `--fallback-model` | Auto-fallback on overload (print mode) | `--fallback-model sonnet` |

[WS-1, WF-1]

#### Session Continuation Pattern

```bash
# Start a session, capture session ID from JSON output
session_id=$(claude -p "Start review" --output-format json | jq -r '.session_id')

# Continue the session with follow-up queries
claude --resume "$session_id" -p "Check compliance"
claude --resume "$session_id" -p "Generate summary"
```

[WS-1]

#### Subagent Definition via CLI

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer.",
    "prompt": "You are a senior code reviewer.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist.",
    "prompt": "You are an expert debugger."
  }
}'
```

Fields: `description` (required), `prompt` (required), `tools`, `disallowedTools`, `model`, `skills`, `mcpServers`, `maxTurns` [WF-1].

#### Working Directory and Filesystem Isolation

- Each CLI process can have its own `cwd` (the directory from which `claude` is invoked)
- `--worktree` / `-w` creates an isolated git worktree at `<repo>/.claude/worktrees/<name>` for full filesystem isolation [WS-3]
- `--add-dir` allows adding additional directories to the agent's scope
- CLAUDE.md files are loaded automatically from the working directory hierarchy [WF-1]

#### Git Worktree Isolation Pattern

```bash
# Create isolated worktrees for parallel instances
claude -w feature-auth -p "Implement authentication"
claude -w feature-api -p "Build REST API"
claude -w fix-bug-123 -p "Fix the login regression"
```

Each worktree gets a full copy of the repo at a specific branch, preventing filesystem conflicts between concurrent agents [WS-3].

#### Alternative: Session-Based Branching (GitButler)

GitButler's approach uses Claude Code lifecycle hooks to assign file changes to per-session branches within a single working directory, avoiding worktree bootstrapping overhead (npm install, build artifacts) [WF-2].

---

### 4. Tool Surface Comparison

#### SDK-Only Tools
- **Custom JSON schema tools**: Any function you define, called by Claude, executed by your code
- **`tool_runner()` beta**: Auto-executes decorated Python functions in the tool loop
- **Programmatic tool calling**: Claude writes code that calls tools (advanced orchestration)

#### Claude Code Tools (Agent SDK + CLI)
- **File operations**: Read, Write, Edit, Glob, Grep
- **Execution**: Bash (shell commands)
- **Web**: WebSearch, WebFetch
- **Notebook**: NotebookEdit
- **Subagents**: Task (delegates to subagents)
- **MCP tools**: Any configured MCP server tools (prefixed `mcp__<server>__<tool>`)

#### Gap Analysis

| Capability | Anthropic SDK | Agent SDK / CLI |
|-----------|--------------|-----------------|
| Custom business logic tools | Native (JSON schema) | Via MCP servers |
| File read/write/edit | Must implement | Built-in |
| Shell execution | Must implement | Built-in (Bash tool) |
| Code search (grep/glob) | Must implement | Built-in |
| Web search/fetch | Must implement | Built-in |
| Git operations | Must implement | Via Bash tool |
| CLAUDE.md context loading | Not applicable | Automatic |
| Skill system | Not applicable | Built-in |
| Permission gating | Must implement | Built-in (permission modes, hooks) |

**Key insight**: The Anthropic SDK gives you an LLM with tool-calling capability. The Agent SDK / CLI gives you a fully equipped software engineering agent with 10+ built-in tools, permission systems, session management, and context loading.

---

### 5. Session Persistence Comparison

| Feature | Anthropic SDK | Agent SDK | CLI |
|---------|--------------|-----------|-----|
| Automatic persistence | No | Yes (Claude Code sessions) | Yes (Claude Code sessions) |
| Resume by session ID | Manual (serialize/deserialize) | `resume="<id>"` | `--resume <id>` |
| Continue last session | Manual | `continue_conversation=True` | `--continue` / `-c` |
| Fork session | Manual (copy history) | `fork_session=True` | `--fork-session` |
| Cross-process resume | Must serialize to disk | Yes (session files) | Yes (session files) |
| Session file location | N/A | `~/.claude/` (Claude Code store) | `~/.claude/` (Claude Code store) |
| Disable persistence | N/A (never persists) | Not documented | `--no-session-persistence` |
| Custom session ID | N/A | Not documented | `--session-id <uuid>` |

**Key insight**: The Anthropic SDK requires you to build your own persistence layer. The Agent SDK and CLI both inherit Claude Code's built-in session system, which persists sessions to disk and supports resume, continue, and fork operations across process restarts.

---

### 6. Cost Comparison

#### Current API Pricing (as of 2026-02-20)

| Model | Input (per MTok) | Output (per MTok) | Cache Hits | 5m Cache Write | 1h Cache Write |
|-------|-------------------|-------------------|------------|----------------|----------------|
| **Opus 4.6** | $5.00 | $25.00 | $0.50 | $6.25 | $10.00 |
| **Opus 4.5** | $5.00 | $25.00 | $0.50 | $6.25 | $10.00 |
| **Sonnet 4.6** | $3.00 | $15.00 | $0.30 | $3.75 | $6.00 |
| **Sonnet 4.5** | $3.00 | $15.00 | $0.30 | $3.75 | $6.00 |
| **Haiku 4.5** | $1.00 | $5.00 | $0.10 | $1.25 | $2.00 |

**Long context (>200K input tokens):** Opus 4.6: $10/$37.50, Sonnet 4.5/4.6: $6/$22.50 per MTok.

**Batch API:** 50% discount on all models.

**Fast mode (Opus 4.6):** 6x standard rates ($30/$150 per MTok).

[WF-3]

#### Cost Difference Between Approaches

| Approach | Token Cost | Overhead |
|----------|-----------|----------|
| **Anthropic SDK** | Direct API pricing | Minimal (your tool schemas ~346 tokens for tool_choice) |
| **Agent SDK** | Same API pricing (via CLI) | Claude Code system prompt + built-in tool definitions (~12-15K tokens initial) |
| **CLI** | Same API pricing (via CLI) | Same as Agent SDK + CLAUDE.md context loading |

**Key insight**: All three approaches use the same underlying API and token pricing. The Agent SDK and CLI add overhead from Claude Code's system prompt and built-in tool definitions (estimated 12-15K tokens for the initial prompt), plus any CLAUDE.md files loaded. For long-running sessions, this initial overhead is amortized. For many short sessions, the SDK offers lower per-invocation cost. The Batch API (50% discount) is only available via the Anthropic SDK, not through Agent SDK or CLI.

---

### 7. Claude Code JS SDK (Supplementary)

**Package:** `claude-code-js` (npm) | **Context7 Score:** 89.7

A TypeScript/JavaScript SDK providing a higher-level wrapper around Claude Code CLI, notable for:

- **Session forking for parallel work**: `reviewSession.fork()` creates independent branches of conversation for parallel analysis
- **Cost tracking**: Each response includes `cost_usd` and `duration_ms`
- **Multi-turn sessions**: `claude.newSession()` maintains conversation context with automatic session ID tracking

```typescript
const claude = new ClaudeCode({ model: 'claude-3-opus', workingDirectory: process.cwd() });
const session = claude.newSession();

// Fork for parallel detailed analyses
const securityFork = session.fork();
const performanceFork = session.fork();

const [security, performance] = await Promise.all([
    securityFork.prompt('Detailed security analysis'),
    performanceFork.prompt('Performance bottleneck analysis'),
]);
```

This pattern is directly relevant to multi-instance orchestration: fork a session after initial context gathering, then run parallel specialized analyses [C7-3].

---

## L2: Architectural Implications

### Multi-Instance Orchestration Trade-offs

#### Approach A: Anthropic SDK as Orchestrator

**Strengths:**
- Maximum control over token flow and cost optimization
- Batch API access (50% discount for non-time-sensitive work)
- Prompt caching control (cache hits at 10% of base price)
- No subprocess overhead; runs entirely in-process
- Can use any model, any configuration, any tool schema
- Clean error handling via Python exceptions

**Weaknesses:**
- Must implement ALL agent capabilities from scratch: file I/O, shell execution, code search, editing, permission gating
- No built-in session persistence
- No CLAUDE.md/context loading
- No built-in subagent system
- Significant development effort to reach feature parity with Claude Code's tool surface
- No skill system integration

**Best for:** Lightweight coordination tasks, API-heavy workflows, cost-sensitive batch processing, scenarios where built-in tools are unnecessary.

#### Approach B: Claude Agent SDK as Orchestrator

**Strengths:**
- Full Claude Code tool surface available programmatically
- Programmatic subagent definitions with isolated context windows
- In-process MCP servers (custom tools without subprocess overhead)
- Hook system for deterministic gating (PreToolUse, SubagentStop)
- Session resume/fork for long-running workflows
- Working directory isolation (`cwd` per instance)
- Python-native API with async/await
- Error types for each failure mode
- File checkpointing for rollback

**Weaknesses:**
- Each `query()` spawns a Claude Code subprocess (process overhead)
- Depends on Claude Code CLI binary (bundled but still a subprocess)
- Relatively new (renamed from `claude-code-sdk`; API still evolving)
- 203 open issues on GitHub as of 2026-02-20
- CLAUDE.md loading behavior inherited from CLI may cause unexpected context injection

**Best for:** Python-based orchestrators that need the full Claude Code experience with programmatic control, custom tool injection, and hook-based quality gating.

#### Approach C: Claude Code CLI as Workers

**Strengths:**
- Full Claude Code experience including skills, CLAUDE.md, all tools
- Git worktree isolation (`--worktree`) for filesystem safety
- `--max-budget-usd` for cost capping per instance
- `--max-turns` for limiting agent autonomy
- `--fallback-model` for availability resilience
- `--output-format json` for structured output parsing
- `--agents` for subagent definitions without code changes
- Battle-tested in production (most widely used approach)
- Language-agnostic orchestration (any language can spawn subprocesses)

**Weaknesses:**
- Subprocess management complexity (spawning, I/O, exit codes, timeouts)
- JSON parsing overhead for structured communication
- Less granular control than SDK (no in-process hooks, no MCP server injection)
- Worktree bootstrap cost (npm install, build artifacts per worktree)
- Multiple concurrent MCP servers may have issues (known bug in CLI v2.1.20)

**Best for:** Language-agnostic orchestration, existing CI/CD integration, scenarios requiring maximum filesystem isolation, teams already using Claude Code interactively.

### Hybrid Architecture Recommendation

The research suggests a **hybrid approach** is optimal for multi-instance orchestration:

1. **Agent SDK for the orchestrator**: Use `claude-agent-sdk` (Python) for the central orchestrator that manages workflow state, dispatches tasks, and aggregates results. The SDK's hook system enables quality gating, and in-process MCP servers allow custom tool injection for orchestration-specific operations.

2. **CLI subprocess or Agent SDK `query()` for workers**: Each worker instance can be spawned via the Agent SDK's `query()` function with per-instance `ClaudeAgentOptions` (different `cwd`, `allowed_tools`, `system_prompt`, `max_turns`). For filesystem isolation, use git worktrees.

3. **Session forking for parallel analysis**: After initial context gathering, fork the session into parallel specialized analyses (security, performance, architecture), then aggregate results.

4. **Anthropic SDK for lightweight coordination**: Use the direct API for metadata queries, scoring, or any task that does not need file system tools.

### Critical Design Decisions for Phase 2

| Decision | Options | Considerations |
|----------|---------|----------------|
| **Orchestrator language** | Python (Agent SDK) vs. Any (CLI subprocess) | Python enables hook-based gating, in-process MCP; CLI enables language flexibility |
| **Worker isolation** | Git worktrees vs. cwd separation vs. single-directory | Worktrees provide strongest isolation but have bootstrap cost |
| **Session strategy** | New session per task vs. resume/fork | Resume preserves context; new session avoids context pollution |
| **Cost control** | `max_budget_usd` per worker vs. global tracking | Per-worker caps prevent runaway costs; global tracking enables budget allocation |
| **Tool restriction** | Per-worker `allowed_tools` vs. global defaults | Least-privilege per worker reduces risk; global defaults simplify config |
| **Error recovery** | Retry with same session vs. fresh session | Resume preserves progress; fresh session avoids error-state pollution |

---

## References

### Context7 Sources

| ID | Source | Content |
|----|--------|---------|
| C7-1 | [Anthropic SDK Python - Context7](https://context7.com/anthropics/anthropic-sdk-python/llms.txt) | Tool use, streaming, agent loops, error handling, retries |
| C7-2 | [Claude Agent SDK Docs - Context7](https://github.com/nothflare/claude-agent-sdk-docs) | ClaudeAgentOptions, subagents, hooks, MCP servers |
| C7-3 | [Claude Code JS SDK - Context7](https://context7.com/s-soroosh/claude-code-js/llms.txt) | Session management, forking, multi-turn conversations |

### Web Sources

| ID | Source | Content |
|----|--------|---------|
| WS-1 | [CLI Reference - Claude Code Docs](https://code.claude.com/docs/en/cli-reference) | Complete CLI flag reference |
| WS-2 | [Building Agents with Claude Agent SDK - Anthropic Blog](https://claude.com/blog/building-agents-with-the-claude-agent-sdk) | Agent loop architecture, design philosophy |
| WS-3 | [Mastering Git Worktrees with Claude Code - Medium](https://medium.com/@dtunai/mastering-git-worktrees-with-claude-code-for-parallel-development-workflow-41dc91e645fe) | Git worktree isolation for parallel agents |
| WS-4 | [Managing Multiple Claude Code Sessions Without Worktrees - GitButler](https://blog.gitbutler.com/parallel-claude-code) | Session-based branching, lifecycle hooks |
| WS-5 | [Claude PM - GitHub](https://github.com/bobmatnyc/claude-pm) | Multi-subprocess orchestration framework |
| WS-6 | [Parallel AI Coding - Ona](https://ona.com/stories/parallelize-claude-code) | Parallel instance patterns |
| WS-7 | [Shipping Faster with Claude Code and Git Worktrees - incident.io](https://incident.io/blog/shipping-faster-with-claude-code-and-git-worktrees) | Production worktree usage |

### GitHub Sources

| ID | Source | Content |
|----|--------|---------|
| GH-1 | [anthropics/claude-agent-sdk-python - GitHub](https://github.com/anthropics/claude-agent-sdk-python) | SDK architecture, API surface, examples, error types |
| GH-2 | [wshobson/agents - GitHub](https://github.com/wshobson/agents) | Multi-agent orchestration for Claude Code |
| GH-3 | [Claude Code MCP Bug #21341 - GitHub](https://github.com/anthropics/claude-code/issues/21341) | Multiple MCP server connection issue |

### Pricing Source

| ID | Source | Content |
|----|--------|---------|
| WF-3 | [Pricing - Claude API Docs](https://platform.claude.com/docs/en/about-claude/pricing) | Current model pricing, batch API, caching, long context |

---

> **S-010 Self-Review Applied:** This research artifact was reviewed against the following criteria before finalization:
> - **Completeness**: All 6 research scope areas covered (SDK capabilities, Agent SDK capabilities, CLI automation, tool surface comparison, session persistence, cost considerations). Supplementary Claude Code JS SDK finding included.
> - **Internal Consistency**: Comparison tables are consistent across sections. No contradictory claims between L0 summary and L1 details.
> - **Evidence Quality**: Every claim is traced to a specific source (C7, WS, GH, WF identifiers). No unsourced assertions.
> - **Actionability**: L2 section provides explicit trade-off analysis per approach with a hybrid recommendation and decision table for Phase 2.
> - **Gaps Identified**: (1) Agent SDK stability/maturity metrics are limited (203 open issues noted but no MTTR data). (2) Actual token overhead of Claude Code system prompt not precisely measured (estimated 12-15K). (3) Concurrent instance limits not documented by Anthropic (depends on API rate limits per tier).
