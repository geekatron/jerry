# Agent Research 001: Claude Code Agent Mechanics

**Document ID:** AGENT-RESEARCH-001
**Date:** 2026-01-09
**Author:** ps-researcher (Claude Opus 4.5)
**Status:** Complete
**Classification:** RESEARCH ONLY - No Implementation

---

## Executive Summary

This research document provides a comprehensive technical analysis of Claude Code's agent architecture, focusing on the Task tool, subagent spawning mechanisms, and integration patterns. Claude Code implements an **orchestrator-worker pattern** where a lead agent (typically Claude Opus 4) coordinates specialized subagents (typically Claude Sonnet 4) operating in parallel.

Key findings:

1. **Task Tool as Core Mechanism**: Subagents are spawned via the Task tool, which creates isolated agent instances with separate context windows
2. **Single Nesting Constraint**: Subagents cannot spawn other subagents (P-003 compliance), preventing infinite recursion
3. **Context Isolation**: Each subagent maintains its own 200K token context window; only summarized results return to the orchestrator
4. **Parallel Execution**: Up to 10 concurrent subagents, processed in batches with queue management for larger workloads
5. **State Management**: File-based persistence is the primary pattern; context compaction handles long-running sessions

---

## Table of Contents

1. [Technical Architecture](#1-technical-architecture)
2. [Task Tool Mechanics](#2-task-tool-mechanics)
3. [Subagent Types and Configuration](#3-subagent-types-and-configuration)
4. [Context Passing and Inheritance](#4-context-passing-and-inheritance)
5. [Parallel Execution Model](#5-parallel-execution-model)
6. [State Management Patterns](#6-state-management-patterns)
7. [Claude Agent SDK Integration](#7-claude-agent-sdk-integration)
8. [MCP Extensibility](#8-mcp-extensibility)
9. [Limitations and Constraints](#9-limitations-and-constraints)
10. [Best Practices](#10-best-practices)
11. [Sources](#11-sources)

---

## 1. Technical Architecture

### 1.1 Core Design Philosophy

Claude Code operates on a **feedback loop model**: gather context → take action → verify work → repeat. The architecture follows Unix philosophy principles: composable, scriptable, and unopinionated.

> "Claude needs the same tools that programmers use every day. It needs to be able to find appropriate files in a codebase, write and edit files, lint the code, run it, debug, edit, and sometimes take these actions iteratively until the code succeeds."
> — [Anthropic Engineering Blog](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)

### 1.2 Orchestrator-Worker Pattern

The multi-agent architecture employs a lead agent that coordinates while delegating to specialized subagents operating in parallel:

```
┌─────────────────────────────────────────────────────────────┐
│                     LEAD AGENT (Orchestrator)               │
│                     [Claude Opus 4 - Recommended]           │
│                                                             │
│  Responsibilities:                                          │
│  - Task decomposition                                       │
│  - Subagent spawning                                        │
│  - Result aggregation                                       │
│  - Quality control                                          │
└───────────────┬─────────────────────────────────────────────┘
                │
                │ Task Tool Invocations
                │
    ┌───────────┼───────────┬───────────┬───────────┐
    ▼           ▼           ▼           ▼           ▼
┌───────┐   ┌───────┐   ┌───────┐   ┌───────┐   ┌───────┐
│Worker │   │Worker │   │Worker │   │Worker │   │Worker │
│  1    │   │  2    │   │  3    │   │  4    │   │ ...n  │
└───────┘   └───────┘   └───────┘   └───────┘   └───────┘
[Sonnet 4]  [Sonnet 4]  [Sonnet 4]  [Sonnet 4]  [Sonnet 4]

Each worker has:
- Own 200K token context window
- Independent permissions
- Isolated tool access
- Fresh context per invocation
```

### 1.3 Performance Characteristics

From Anthropic's internal evaluations:

| Metric | Value |
|--------|-------|
| Multi-agent vs. single-agent improvement | 90%+ |
| Token usage (agent vs. chat) | 4x higher |
| Token usage (multi-agent vs. chat) | 15x higher |
| Token usage explains performance variance | 80% |

---

## 2. Task Tool Mechanics

### 2.1 Task Tool Overview

The Task tool is Claude Code's primary mechanism for delegating work to subagents. It launches specialized autonomous agents designed to handle complex, multi-step tasks.

**Token cost:** ~1210 tokens for the tool description alone.

### 2.2 Task Tool Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `subagent_type` | string | Yes | Selects which agent type to use |
| `prompt` | string | Yes | Detailed task description with context |
| `description` | string | Recommended | 3-5 word summary of agent objective |
| `resume` | string | No | Agent ID to continue previous invocation |
| `run_in_background` | boolean | No | Execute asynchronously while continuing work |

### 2.3 Task Tool Invocation Pattern

```python
# Conceptual representation of Task tool usage
{
    "name": "Task",
    "input": {
        "subagent_type": "code-reviewer",
        "description": "Review authentication module security",
        "prompt": """Analyze the authentication module for:
        - Security vulnerabilities (SQL injection, XSS, CSRF)
        - Authentication flow correctness
        - Session management issues

        Return findings with severity ratings and remediation steps."""
    }
}
```

### 2.4 Result Communication

When the agent completes:
1. Returns a single message back to the orchestrator
2. Includes an agent ID for potential resumption
3. Output is initially invisible to users
4. Orchestrator must summarize findings in a visible message
5. Background agents create output files retrievable via file-reading tools

---

## 3. Subagent Types and Configuration

### 3.1 Built-in Subagent Types

| Type | Purpose | Tools | Model |
|------|---------|-------|-------|
| **Explore** | Haiku-powered codebase search | Read, Grep, Glob, limited Bash | Haiku |
| **Plan** | Dedicated planning with resumption | Full research capabilities | Varies |
| **General-Purpose** | Complex multi-step tasks | All available tools | Inherits |
| **statusline-setup** | Configure status line | Read, Edit | - |
| **output-style-setup** | Create output styles | Read, Write, Edit, Glob, LS, Grep | - |

### 3.2 Explore Subagent Details

The Explore subagent (v2.0.17) is a **read-only** file search specialist:

- Thoroughness levels: `quick`, `medium`, `very thorough`
- Strictly prohibited from creating or modifying files
- Keeps exploration results out of main conversation context
- Starts with fresh context (search tasks are often independent)

### 3.3 Plan Subagent Details

The Plan subagent (v2.0.28) enables:

- Dedicated planning with subagent resumption capabilities
- Research agent for plan mode to gather context
- Inherits full context from parent conversation

### 3.4 Custom Subagent Configuration

Custom subagents are defined via markdown files in `.claude/agents/` directories:

```yaml
# ~/.claude/agents/security-auditor.md
---
name: security-auditor
description: Security code review specialist for vulnerability detection
tools:
  - Read
  - Grep
  - Glob
  - Bash
model: opus
permissionMode: bypassPermissions  # Use with caution
---

You are a security auditor specializing in:
- OWASP Top 10 vulnerabilities
- Authentication/authorization flaws
- Data exposure risks

When reviewing code:
1. Identify security issues with severity ratings
2. Provide specific remediation steps
3. Reference security best practices
```

### 3.5 AgentDefinition Schema (SDK)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `description` | string | Yes | Natural language description of when to use |
| `prompt` | string | Yes | System prompt defining role and behavior |
| `tools` | string[] | No | Allowed tool names (inherits all if omitted) |
| `model` | enum | No | 'sonnet', 'opus', 'haiku', or 'inherit' |

### 3.6 Common Tool Combinations

| Use Case | Tools | Description |
|----------|-------|-------------|
| Read-only analysis | Read, Grep, Glob | Examine but not modify |
| Test execution | Bash, Read, Grep | Run commands and analyze |
| Code modification | Read, Edit, Write, Grep, Glob | Full R/W without execution |
| Research | Read, Grep, Glob, WebFetch, WebSearch | Gather information |
| Full access | (omit field) | Inherits all tools |

---

## 4. Context Passing and Inheritance

### 4.1 Current Context Model

**Critical limitation**: Subagents currently start with **zero context**. The orchestrator summarizes what it thinks is relevant, but this is lossy.

```
┌─────────────────────────────────────────┐
│         ORCHESTRATOR CONTEXT            │
│                                         │
│  [Full conversation history]            │
│  [All tool results]                     │
│  [User messages]                        │
│                                         │
│         │                               │
│         ▼ Task Tool                     │
│  ┌──────────────────┐                   │
│  │ Summarized prompt │                  │
│  │ (Lossy transfer) │                   │
│  └────────┬─────────┘                   │
│           │                             │
└───────────┼─────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────┐
│         SUBAGENT CONTEXT                │
│                                         │
│  [Fresh context window - 200K tokens]   │
│  [Summarized prompt only]               │
│  [No access to parent tool results]     │
│                                         │
└─────────────────────────────────────────┘
```

### 4.2 Context Access Types

Some agents have "access to current context" and can see the full conversation history before the tool call:

- **Full context access**: General-purpose, Plan subagents
- **Fresh context**: Explore subagent (search tasks are independent)

When using context-access agents:
```
# Concise prompts that reference earlier context work:
"Investigate the error discussed above"

# Instead of repeating all information
```

### 4.3 Permission Inheritance

Built-in subagents inherit the parent conversation's permissions with additional tool restrictions:

```python
# Parent has full permissions
allowed_tools = ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "Task"]

# Subagent can be restricted
subagent_tools = ["Read", "Grep", "Glob"]  # Read-only subset
```

### 4.4 Known Context Passing Issues

From GitHub issue discussions:

1. **No file content visibility**: Parent agent doesn't know contents of files created by subagents
2. **Information flow bottleneck**: Synchronous execution routes everything through lead agent
3. **Game of telephone effect**: Multi-hop information transfer degrades quality

**Proposed solutions** (feature requests):
- `fork_context` option for full conversation inheritance
- Hooks to bridge context between sub-agents and parent
- Background agent execution for async support

---

## 5. Parallel Execution Model

### 5.1 Concurrency Limits

| Limit | Value | Notes |
|-------|-------|-------|
| Maximum parallel subagents | 10 | Additional tasks queued |
| Batch processing | Yes | Waits for batch completion |
| Queue support | Unlimited | Tasks queued if >10 |

### 5.2 Batch Execution Pattern

```
Parallelism Level: 4
Total Tasks: 10

Batch 1: Tasks 1-4 (parallel) → Complete
Batch 2: Tasks 5-8 (parallel) → Complete
Batch 3: Tasks 9-10 (parallel) → Complete

Note: Tasks pull from queue immediately as slots become available
```

### 5.3 Launching Parallel Agents

```python
# Launch multiple agents concurrently in a single message
for await (const message of query({
  prompt: "Analyze this codebase",
  options: {
    allowedTools: ['Read', 'Grep', 'Glob', 'Task'],
    // Multiple Task tool invocations in single response
  }
}))
```

Best practice: "Launch multiple agents concurrently whenever possible, to maximize performance; to do that, use a single message with multiple tool uses."

### 5.4 Git Worktrees for True Parallelism

For independent file modifications:

```bash
# Create isolated worktrees for parallel Claude Code sessions
git worktree add ../feature-1 -b feature-1
git worktree add ../feature-2 -b feature-2
git worktree add ../feature-3 -b feature-3

# Each worktree has independent file state
# Changes in one don't affect others
# All share Git history and remote connections
```

---

## 6. State Management Patterns

### 6.1 Session State Object

Claude Code uses a global state object (internally `r0`):

```javascript
{
  sessionId: "uuid-xxx",      // For persistence and telemetry
  originalCwd: "/path/start", // Launch directory
  cwd: "/path/current",       // Current working directory
  // ... additional state
}
```

### 6.2 Session Persistence

Sessions are stored in `~/.claude/projects/` with:

- Complete development environment state
- Background processes
- File contexts
- Permissions
- Working directories

### 6.3 CLI Session Commands

| Command | Effect |
|---------|--------|
| `claude --continue` | Resume most recent conversation |
| `claude -c` | Shorthand for continue |
| `/compact` | Summarize and compress context |
| `/clear` | Wipe conversation history |

### 6.4 Context Compaction

Auto-compact triggers at ~95% context capacity (or 25% remaining):

```
Before Compaction:
┌──────────────────────────────────────────┐
│ Full conversation history (95% full)     │
│ All tool results                         │
│ Every message verbatim                   │
└──────────────────────────────────────────┘

After Compaction:
┌──────────────────────────────────────────┐
│ Summarized context (~30% full)           │
│ Key decisions preserved                  │
│ Salient facts retained                   │
└──────────────────────────────────────────┘
```

**Manual compaction guidance:**
- Run at 70% capacity proactively
- Use at natural task breakpoints
- Can provide custom instructions for what to summarize

### 6.5 File-Based Memory

The file system serves as contextual data storage:

```
# Agents use selective loading instead of full files
grep -n "pattern" file.py  # Selective line retrieval
tail -f app.log            # Streaming recent data

# Folder structure becomes a retrieval mechanism
project/
├── context/          # Active working memory
├── decisions/        # Persisted decisions
├── research/         # Accumulated knowledge
└── checkpoints/      # State snapshots
```

---

## 7. Claude Agent SDK Integration

### 7.1 SDK Overview

The Claude Agent SDK (formerly Claude Code SDK) enables programmatic agent building with:

- **Context management**: Automatic compaction
- **Rich tool ecosystem**: File ops, code execution, web search, MCP
- **Advanced permissions**: Fine-grained capability control
- **Production essentials**: Error handling, session management, monitoring
- **Optimized Claude integration**: Prompt caching, performance optimizations

### 7.2 SDK Languages

| Language | Package | Status |
|----------|---------|--------|
| Python | `claude-agent-sdk` | GA |
| TypeScript | `@anthropic-ai/claude-agent-sdk` | GA |

### 7.3 Python SDK Example

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

async def main():
    async for message in query(
        prompt="Review the authentication module for security issues",
        options=ClaudeAgentOptions(
            # Task tool required for subagent invocation
            allowed_tools=["Read", "Grep", "Glob", "Task"],
            agents={
                "code-reviewer": AgentDefinition(
                    description="Expert code review specialist",
                    prompt="""You are a code review specialist with expertise
                    in security, performance, and best practices.

                    When reviewing code:
                    - Identify security vulnerabilities
                    - Check for performance issues
                    - Verify adherence to coding standards
                    - Suggest specific improvements""",
                    tools=["Read", "Grep", "Glob"],
                    model="sonnet"
                )
            }
        )
    ):
        if hasattr(message, "result"):
            print(message.result)

asyncio.run(main())
```

### 7.4 TypeScript SDK Example

```typescript
import { query } from '@anthropic-ai/claude-agent-sdk';

for await (const message of query({
  prompt: "Review the authentication module",
  options: {
    allowedTools: ['Read', 'Grep', 'Glob', 'Task'],
    agents: {
      'code-reviewer': {
        description: 'Expert code review specialist',
        prompt: `You are a code review specialist...`,
        tools: ['Read', 'Grep', 'Glob'],
        model: 'sonnet'
      }
    }
  }
})) {
  if ('result' in message) console.log(message.result);
}
```

### 7.5 Detecting Subagent Invocation

```python
async for message in query(...):
    # Check for subagent invocation
    if hasattr(message, 'content') and message.content:
        for block in message.content:
            if getattr(block, 'type', None) == 'tool_use' and block.name == 'Task':
                print(f"Subagent invoked: {block.input.get('subagent_type')}")

    # Check if message is from within subagent context
    if hasattr(message, 'parent_tool_use_id') and message.parent_tool_use_id:
        print("  (running inside subagent)")
```

### 7.6 Custom Tools and Hooks

```python
from claude_agent_sdk import ClaudeSDKClient

# Custom tool as Python function (runs as in-process MCP server)
def analyze_dependencies(package_json: str) -> dict:
    """Analyze package.json for security issues"""
    # Implementation
    return {"vulnerabilities": [...]}

# Hook invoked at specific points in agent loop
def on_tool_call(tool_name: str, input: dict) -> None:
    """Called before each tool invocation"""
    log(f"Tool called: {tool_name}")
```

---

## 8. MCP Extensibility

### 8.1 Model Context Protocol Overview

MCP provides a standardized way to connect Claude Code to external tools and data sources. Think of it as "universal USB-C for AI applications."

### 8.2 Configuration Scopes

| Scope | Location | Visibility | Use Case |
|-------|----------|------------|----------|
| Local | `~/.claude.json` (project path) | Private | Personal development |
| Project | `.claude/mcp.json` | Shared | Team configurations |
| Enterprise | `managed-mcp.json` | Managed | Policy-controlled deployment |

### 8.3 MCP Server Configuration

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://..."
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "..."
      }
    }
  }
}
```

### 8.4 Desktop Extensions

New packaging format (.mcpb files) for one-click MCP server installation:

- Bundles entire MCP server with dependencies
- No terminal, no configuration files
- No dependency conflicts
- Single installable package

---

## 9. Limitations and Constraints

### 9.1 Architectural Constraints

| Constraint | Description | Rationale |
|------------|-------------|-----------|
| **P-003: Single Nesting** | Subagents cannot spawn subagents | Prevents infinite recursion |
| **Context Isolation** | Subagents start with zero/minimal context | Prevents context pollution |
| **Synchronous Default** | Task tool blocks until completion | Simpler control flow |
| **No Nested Task Tool** | Don't include Task in subagent's tools | Enforces P-003 |

### 9.2 Current Technical Limitations

1. **Context Passing is Lossy**
   - Manual context in Task prompt is verbose
   - Subagent may miss important context
   - No conversation forking programmatically

2. **Parent-Child Communication Gap**
   - Parent has no knowledge of files created by subagents
   - Cannot monitor sub-agent activities until completion
   - No ability to detect strategy abandonment

3. **Windows Command Line Limits**
   - Long prompts (>8191 chars) may fail
   - Use filesystem-based agents for complex instructions

4. **API Rate Limits**
   - Heavy parallelization hits rate limits
   - Consider upgrading to Max plan ($100/month) for parallel work

### 9.3 Anti-Patterns from Production

From Anthropic's lessons learned:

> "Early agents made errors like spawning 50 subagents for simple queries, scouring the web endlessly for nonexistent sources, and distracting each other with excessive updates."

**Mitigations:**
- Embed scaling rules (simple: 1 agent, 3-10 calls; complex: 10+ subagents)
- Provide explicit tool-selection heuristics
- Teach orchestrators detailed delegation instructions

---

## 10. Best Practices

### 10.1 Task Delegation

1. **Be Explicit**: Like programming with threads, explicit orchestration yields best results
2. **Group Related Tasks**: More efficient than creating separate agents per operation
3. **Provide Clear Boundaries**: "Each task handles ONLY specified files or file types"
4. **Use Read Operations Primarily**: Avoid parallel write conflicts

### 10.2 Subagent Configuration

```yaml
# Good: Clear, focused description
description: "Security code review specialist for vulnerability detection"

# Bad: Vague description
description: "Code helper"

# Good: Specific tool restrictions
tools: ["Read", "Grep", "Glob"]  # Read-only for reviewers

# Bad: Full access when not needed
tools: []  # Inherits everything
```

### 10.3 Context Management

1. **Monitor Context Meter**: Compact at 70% capacity proactively
2. **Use CLAUDE.md**: Persistent memory instead of repeating instructions
3. **Natural Breakpoints**: Compact when finishing tasks
4. **Disable Unused MCP Servers**: `@server-name disable` before compacting

### 10.4 Parallel Execution

```python
# Good: 7-task parallel structure for features
tasks = [
    "Component file creation",
    "Styles/CSS development",
    "Test file generation",
    "Type definitions",
    "Custom hooks/utilities",
    "Integration (routing, imports)",
    "Configuration updates"
]

# Each task handles ONLY specified files
```

### 10.5 Error Handling

From Anthropic:

> "The compound nature of errors in agentic systems means that minor issues for traditional software can derail agents entirely. One step failing can cause agents to explore entirely different trajectories."

**Recommendations:**
- Use rule-based feedback with explicit failure explanations
- Add visual feedback for UI verification
- Build representative test sets for programmatic evaluation
- Examine failure cases to improve agent performance

---

## 11. Sources

### Official Anthropic Documentation

- [Create custom subagents - Claude Code Docs](https://code.claude.com/docs/en/sub-agents)
- [Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Claude Code: Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Agent SDK overview - Claude Docs](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Subagents in the SDK - Claude Docs](https://platform.claude.com/docs/en/agent-sdk/subagents)
- [Session Management - Claude Docs](https://platform.claude.com/docs/en/agent-sdk/sessions)
- [MCP in the SDK - Claude Docs](https://platform.claude.com/docs/en/agent-sdk/mcp)
- [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)

### GitHub Resources

- [anthropics/claude-code](https://github.com/anthropics/claude-code) - Main repository
- [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python)
- [anthropics/claude-agent-sdk-typescript](https://github.com/anthropics/claude-agent-sdk-typescript)
- [anthropics/claude-agent-sdk-demos](https://github.com/anthropics/claude-agent-sdk-demos)
- [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) - System prompt documentation
- [Issue #4182: Sub-Agent Task Tool Not Exposed](https://github.com/anthropics/claude-code/issues/4182)
- [Issue #1770: Parent-Child Agent Communication](https://github.com/anthropics/claude-code/issues/1770)
- [Issue #16153: Add fork_context option](https://github.com/anthropics/claude-code/issues/16153)
- [Issue #5812: Hooks to Bridge Context](https://github.com/anthropics/claude-code/issues/5812)
- [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) - 100+ subagent collection

### Community Resources

- [ClaudeLog - Task/Agent Tools](https://claudelog.com/mechanics/task-agent-tools/)
- [ClaudeLog - Sub-agents](https://claudelog.com/mechanics/sub-agents/)
- [Claude Code Subagent Deep Dive - Code Centre](https://cuong.io/blog/2025/06/24-claude-code-subagent-deep-dive)
- [Claude Code customization guide - alexop.dev](https://alexop.dev/posts/claude-code-customization-guide-claudemd-skills-subagents/)
- [How to Use Claude Code Subagents - Zach Wills](https://zachwills.net/how-to-use-claude-code-subagents-to-parallelize-development/)
- [Claude Code Best Practices: Memory Management](https://cuong.io/blog/2025/06/15-claude-code-best-practices-memory-management)
- [Inside Claude Code Skills - Mikhail Shilkov](https://mikhail.io/2025/10/claude-code-skills/)
- [Claude Code Internals, Part 6: Session State Management](https://kotrotsos.medium.com/claude-code-internals-part-6-session-state-management-e729f49c8bb9)

### Courses and Tutorials

- [Claude Code: A Highly Agentic Coding Assistant - DeepLearning.AI](https://learn.deeplearning.ai/courses/claude-code-a-highly-agentic-coding-assistant/)
- [Claude Agent SDK Tutorial - DataCamp](https://www.datacamp.com/tutorial/how-to-use-claude-agent-sdk)

---

## Appendix A: Jerry Constitution Alignment

This research validates the following Jerry Constitution principles:

| Principle | Research Finding | Alignment |
|-----------|------------------|-----------|
| **P-003: No Recursive Subagents** | Subagents cannot spawn subagents | **Confirmed** |
| **P-002: File Persistence** | File system as infinite memory | **Supported** |
| **P-004: Decision Documentation** | CLAUDE.md for persistent memory | **Aligned** |
| **P-010: Task Tracking** | Session persistence + /compact | **Compatible** |

---

## Appendix B: Version Information

| Component | Version | Date |
|-----------|---------|------|
| Claude Code | v2.1.1 | 2026-01-07 |
| Explore Subagent | v2.0.17 | - |
| Plan Subagent | v2.0.28 | - |
| Claude Agent SDK | GA | 2025 |
| This Document | 1.0 | 2026-01-09 |

---

*This research document is classified as RESEARCH ONLY. No implementation has been performed.*
