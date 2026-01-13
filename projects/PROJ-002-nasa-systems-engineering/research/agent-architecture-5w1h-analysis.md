# Agent Architecture Analysis: 5W1H Framework

> **Document ID:** PROJ-002-R-019
> **Type:** Research Synthesis
> **Status:** COMPLETE
> **Date:** 2026-01-10
> **Work Item:** WI-SAO-019
> **Author:** Claude (Opus 4.5) via ps-researcher methodology

---

## Executive Summary

This document provides a comprehensive analysis of Claude Code's agent architecture, Jerry Framework's agent patterns, and industry best practices for multi-agent systems. The research addresses the fundamental question: *"What exactly are Claude Code subagents, and how do Jerry agents relate to them?"*

**Key Finding:** Jerry agents ARE Claude Code subagents when invoked via the Task tool. The distinction lies in WHERE agent definitions live and HOW they are discovered, not in their fundamental nature.

---

## Table of Contents

1. [Three-Level Explanation](#1-three-level-explanation)
2. [5W1H Analysis](#2-5w1h-analysis)
3. [Technical Deep Dive](#3-technical-deep-dive)
4. [Industry Patterns Comparison](#4-industry-patterns-comparison)
5. [Jerry Framework Implementation](#5-jerry-framework-implementation)
6. [Recommendations](#6-recommendations)
7. [References](#7-references)

---

## 1. Three-Level Explanation

### L0: ELI5 (Explain Like I'm 5)

**What are Claude Code subagents?**

Imagine you're the boss of a small company (that's Claude Code). When you get a big job, you can hire temporary helpers to do specific parts of the work. These helpers are called "subagents."

- **The Task tool** is like your phone - you use it to call a helper
- **Subagent types** are like different specialists - a plumber, electrician, or painter
- **Agent files** are like business cards that tell helpers what they're good at

When you need help with research, you call the research helper. When you need help with coding, you call the coding helper. Each helper works in their own room (isolated context), does their job, and brings back the result. They can't call more helpers themselves - only you (the main Claude) can hire people.

**Jerry's agents are just business cards stored in different filing cabinets:**
- `.claude/agents/` = Main office filing cabinet (general helpers)
- `skills/*/agents/` = Specialized department cabinets (domain experts)

---

### L1: Software Engineer Level

**What are Claude Code subagents?**

Subagents are isolated Claude instances spawned via the Task tool to handle focused subtasks. They provide:

1. **Context isolation** - Each subagent has its own context window, preventing information overload
2. **Parallelization** - Multiple subagents can run concurrently on independent tasks
3. **Specialization** - Subagents can have restricted tools and custom system prompts

**Key Technical Details:**

```typescript
// AgentDefinition type (Claude Agent SDK)
type AgentDefinition = {
  description: string;           // Triggers automatic delegation
  tools?: string[];              // Tool restrictions (inherits if omitted)
  prompt: string;                // System prompt for the subagent
  model?: 'sonnet' | 'opus' | 'haiku' | 'inherit';
};
```

**Task Tool Invocation:**
```json
{
  "name": "Task",
  "input": {
    "subagent_type": "general-purpose",
    "description": "Analyze codebase structure",
    "prompt": "Detailed instructions for the subagent..."
  }
}
```

**Built-in Subagent Types:**
| Type | Purpose | Context Access |
|------|---------|----------------|
| `general-purpose` | Read/write operations, complex reasoning | Full |
| `Explore` | Read-only codebase exploration | Read-only |
| `Plan` | Architecture and implementation planning | Read-only |
| `claude-code-guide` | Documentation lookup | Read + web |
| Custom (`plugin:agent-name`) | Plugin-defined specialists | Per-agent config |

**Subagent Discovery Mechanisms:**
1. **Static registration** - `.claude/settings.json` → `agents.available[]`
2. **Filesystem auto-discovery** - `.claude/agents/*.md` scanned at startup
3. **Plugin agents** - `plugins/*/agents/*.md` with namespace prefix
4. **Keyword matching** - Claude matches task to agent via `description` field

**Constraints:**
- Subagents **CANNOT** spawn other subagents (max 1 level of nesting)
- Subagents inherit parent permissions unless explicitly restricted
- Task tool must be in `allowedTools` for subagent invocation

---

### L2: Principal Architect Level

**Architectural Analysis: Claude Code Subagent System**

**1. Core Architecture Pattern: Orchestrator-Worker**

Claude Code implements a **single-level orchestrator-worker pattern**:

```
┌─────────────────────────────────────────────────────────────┐
│                    Main Claude Context                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │ Task Tool   │  │ Task Tool   │  │ Task Tool   │  ...     │
│  │ (Subagent)  │  │ (Subagent)  │  │ (Subagent)  │          │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘          │
└─────────┼────────────────┼────────────────┼─────────────────┘
          │                │                │
          ▼                ▼                ▼
    ┌───────────┐    ┌───────────┐    ┌───────────┐
    │ Subagent  │    │ Subagent  │    │ Subagent  │
    │ Context A │    │ Context B │    │ Context C │
    │ (Isolated)│    │ (Isolated)│    │ (Isolated)│
    └───────────┘    └───────────┘    └───────────┘
```

**Design Rationale (P-003 Constraint):**
- Prevents recursive agent spawning (potential infinite loops)
- Simplifies error handling and state management
- Reduces token consumption (multi-agent = 15× vs chat = 1×)
- Enables predictable cost modeling

**2. Agent Definition Taxonomy**

| Definition Type | Location | Discovery | Use Case |
|-----------------|----------|-----------|----------|
| Built-in | Hardcoded in Claude Code | Automatic | Core functionality (Explore, Plan) |
| Filesystem | `.claude/agents/*.md` | Auto-scan | Project-specific agents |
| Settings-registered | `settings.json` | Static | Framework-level agents |
| Plugin agents | `plugins/*/agents/*.md` | Namespace-prefixed | Plugin extensions |
| Programmatic (SDK) | Code | Runtime | SDK applications |

**3. Context Management Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    Orchestrator Context                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ System Prompt + CLAUDE.md + Conversation History     │   │
│  └──────────────────────────────────────────────────────┘   │
│                           │                                  │
│                    Task Tool Call                            │
│                           │                                  │
│                           ▼                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Subagent Context (Fresh per invocation)              │   │
│  │ - Agent's system prompt (from .md file)              │   │
│  │ - Parent's CLAUDE.md (inherited)                     │   │
│  │ - Task description + prompt (injected)               │   │
│  │ - Tool restrictions (per agent config)               │   │
│  └──────────────────────────────────────────────────────┘   │
│                           │                                  │
│                    Result Summary                            │
│                           │                                  │
│                           ▼                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Orchestrator receives: result + optional artifacts    │   │
│  │ (Full subagent context NOT returned - only summary)   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Key Insight:** Subagents maintain isolated context windows. Only the final result (not full reasoning trace) returns to the orchestrator, preventing context bloat.

**4. Jerry Framework Extension Points**

Jerry extends Claude Code's native subagent system with:

| Extension | Location | Purpose |
|-----------|----------|---------|
| Constitutional compliance | `docs/governance/JERRY_CONSTITUTION.md` | Hard constraints (P-003, P-020, P-022) |
| Structured frontmatter | `PS_AGENT_TEMPLATE.md` v2.0 | YAML + XML standardization |
| Output levels | L0/L1/L2 | Multi-audience communication |
| State management | `session_context.json` schema | Agent-to-agent handoffs |
| Mandatory persistence | P-002 | Context rot prevention |

**5. Trade-off Analysis**

| Concern | Claude Code Native | Jerry Extension | Trade-off |
|---------|-------------------|-----------------|-----------|
| Agent discovery | Filesystem auto-scan | Keyword routing | Flexibility vs predictability |
| State passing | Task result only | session_context schema | Simplicity vs richness |
| Output format | Freeform | L0/L1/L2 structured | Speed vs consistency |
| Validation | None | Input/output schemas | Performance vs reliability |
| Compliance | SDK defaults | Constitutional principles | Flexibility vs governance |

---

## 2. 5W1H Analysis

### WHO creates and uses Claude Code subagents?

**Creators:**
- **Anthropic** - Built-in subagents (Explore, Plan, general-purpose, claude-code-guide)
- **Plugin developers** - Custom agents in `plugins/*/agents/`
- **Project developers** - Project agents in `.claude/agents/`
- **SDK developers** - Programmatic agents via Claude Agent SDK

**Users:**
- **Claude (main thread)** - Automatically delegates based on task matching
- **Users (explicit)** - Can request specific agents by name
- **Orchestrators** - Spawn workers for parallel/specialized tasks

**Source:** [Claude Agent SDK Overview](https://platform.claude.com/docs/en/agent-sdk/overview), [Subagents in the SDK](https://platform.claude.com/docs/en/agent-sdk/subagents)

---

### WHAT exactly is a Claude Code subagent?

**Formal Definition:**
> A **subagent** is a separate Claude instance spawned via the Task tool to handle focused subtasks. Subagents have isolated context windows, optionally restricted tools, and specialized system prompts. They return results to the orchestrating context upon completion.

**Key Characteristics:**
1. **Isolated context** - Fresh context per invocation
2. **Configurable tools** - Can restrict available tools
3. **Custom system prompt** - Defined in agent file or programmatically
4. **Model selection** - Can use different Claude model (opus/sonnet/haiku)
5. **Single-level nesting** - Cannot spawn other subagents

**Agent File Format:**
```markdown
---
name: agent-identifier
description: Use this agent when [triggering conditions]...
model: inherit
color: blue
tools: ["Read", "Write", "Grep", "Bash"]
---

[Complete system prompt for the agent]
```

**Source:** [Create custom subagents](https://code.claude.com/docs/en/sub-agents), [Agent Development SKILL](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/agent-development/SKILL.md)

---

### WHEN should subagents be used vs direct tool calls?

| Scenario | Use Subagent | Use Direct Tools |
|----------|-------------|------------------|
| Complex multi-step task | ✅ | ❌ |
| Parallel independent tasks | ✅ | ❌ |
| Specialized domain expertise | ✅ | ❌ |
| Simple file read/write | ❌ | ✅ |
| Single tool call | ❌ | ✅ |
| Context isolation needed | ✅ | ❌ |
| Token budget constrained | ❌ | ✅ |

**Anthropic Guidance:**
> "When building applications with LLMs, find the simplest solution possible, and only increase complexity when needed. This might mean not building agentic systems at all. Agentic systems often trade latency and cost for better task performance."

**Token Economics:**
- Direct tool call: 1× token usage
- Single agent: 4× token usage
- Multi-agent: 15× token usage

**Source:** [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)

---

### WHERE do subagent definitions live?

**Claude Code Native Locations:**

| Location | Discovery | Scope | Example |
|----------|-----------|-------|---------|
| `.claude/agents/*.md` | Auto-scan | Project | `.claude/agents/code-reviewer.md` |
| `plugins/*/agents/*.md` | Plugin namespace | Plugin | `pr-review-toolkit:code-reviewer` |
| `settings.json` → `agents.available` | Static registration | Framework | `orchestrator`, `qa-engineer` |
| Programmatic (SDK) | Runtime injection | Application | `AgentDefinition` objects |

**Jerry Framework Locations:**

| Location | Purpose | Agent Count |
|----------|---------|-------------|
| `.claude/agents/` | Framework-level coordination | 3 (orchestrator, qa-engineer, security-auditor) |
| `skills/problem-solving/agents/` | Problem-solving specialists | 8 (ps-researcher, ps-analyst, etc.) |
| `skills/nasa-se/agents/` | NASA SE specialists | 8 (nse-architecture, nse-configuration, etc.) |
| `skills/orchestration/agents/` | Workflow coordinators | 3 (orch-planner, orch-synthesizer, etc.) |

**Key Insight:** Only `.claude/agents/` agents are registered in `settings.json`. Skill-level agents are discovered via keyword matching in ORCHESTRATION.md files.

---

### WHY were subagents designed this way?

**Design Goals:**

1. **Context Management** - Prevents context window overflow by isolating specialized tasks
2. **Parallelization** - Enables concurrent work on independent subtasks
3. **Specialization** - Allows domain-specific prompts and tool restrictions
4. **Safety** - Single-level nesting prevents recursive loops (P-003)
5. **Simplicity** - Minimal abstraction over Claude API calls

**Anthropic's Core Principle:**
> "The key design principle behind the Claude Agent SDK is to give agents a computer, allowing them to work like humans do."

**Context Rot Prevention:**
> "Context Rot is the phenomenon where an LLM's performance degrades as the context window fills up." - Chroma Research

Subagents address this by:
- Isolating specialized work in fresh contexts
- Returning only summaries (not full reasoning traces)
- Enabling filesystem persistence (offload state to files)

**Source:** [Context Rot Research](https://research.trychroma.com/context-rot), [Claude Agent SDK Engineering](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)

---

### HOW does the Task tool spawn subagents?

**Invocation Mechanism:**

```
1. Main Claude receives task requiring delegation
           │
           ▼
2. Claude calls Task tool with:
   - subagent_type: "general-purpose" | "Explore" | "Plan" | custom
   - description: "3-5 word task summary"
   - prompt: "Detailed instructions for subagent"
           │
           ▼
3. Claude Code runtime:
   a. Loads agent definition (if custom type)
   b. Creates fresh conversation context
   c. Injects agent's system prompt
   d. Injects task description + prompt
   e. Inherits parent's CLAUDE.md and permissions
   f. Applies tool restrictions (if specified)
           │
           ▼
4. Subagent executes autonomously:
   - Has access to configured tools
   - Operates in isolated context
   - Cannot spawn other subagents
           │
           ▼
5. Upon completion:
   - Returns TaskOutput with result
   - Optionally includes usage stats, cost, duration
   - Full subagent context discarded (only result persists)
```

**Task Tool Parameters:**

```typescript
interface AgentInput {
  description: string;      // Short (3-5 word) task summary
  prompt: string;           // Detailed instructions
  subagent_type: string;    // Agent type or custom identifier
  model?: string;           // Optional model override
  run_in_background?: boolean;  // Async execution
  resume?: string;          // Resume previous agent session
  max_turns?: number;       // Limit agentic turns
}

interface TaskOutput {
  result: string;           // Final result from subagent
  usage?: TokenUsage;       // Token statistics
  total_cost_usd?: number;  // Cost in USD
  duration_ms?: number;     // Execution time
}
```

**Agent Matching Algorithm:**
1. Check if `subagent_type` matches a built-in type (Explore, Plan, etc.)
2. If not, search `.claude/agents/` for matching filename
3. If not, search plugins for `plugin-name:agent-name` pattern
4. If not found, use `general-purpose` as fallback
5. Claude can also auto-delegate based on `description` field matching

**Source:** [Task Tool Definition](https://github.com/anthropics/claude-code), [Subagent Delegation](https://claudelog.com/faqs/what-is-sub-agent-delegation-in-claude-code/)

---

## 3. Technical Deep Dive

### 3.1 Agent Definition Schema Comparison

**Claude Code Native (Minimal):**
```yaml
---
name: agent-identifier
description: Use this agent when...
model: inherit
tools: ["Read", "Write", "Bash"]
---

System prompt content...
```

**Jerry Framework PS v2.0 (Comprehensive):**
```yaml
---
name: ps-researcher
version: "2.0.0"
description: "Deep research agent..."
model: opus

identity:
  role: "Research Specialist"
  expertise: [...]
  cognitive_mode: "divergent"

persona:
  tone: "professional"
  communication_style: "consultative"

capabilities:
  allowed_tools: [Read, Write, WebSearch, ...]
  forbidden_actions: ["Spawn recursive subagents (P-003)"]

guardrails:
  input_validation: [...]
  output_filtering: [...]

output:
  levels: [L0, L1, L2]
  location: "projects/${JERRY_PROJECT}/..."

constitution:
  principles_applied: [P-001, P-002, P-003, ...]

session_context:
  schema: "docs/schemas/session_context.json"
---

<agent>
<identity>...</identity>
<capabilities>...</capabilities>
<invocation_protocol>...</invocation_protocol>
<output_levels>...</output_levels>
</agent>
```

### 3.2 Agent Location Architecture

```
Jerry Framework Agent Hierarchy
================================

.claude/                          ← Framework-level (registered in settings.json)
├── agents/
│   ├── orchestrator.md           ← Master coordinator (Opus)
│   ├── qa-engineer.md            ← Quality assurance (Sonnet)
│   └── security-auditor.md       ← Security review (Sonnet)
└── settings.json                 ← Static agent registration

skills/                           ← Skill-level (keyword-routed)
├── problem-solving/
│   ├── agents/
│   │   ├── PS_AGENT_TEMPLATE.md  ← v2.0 template
│   │   ├── ps-researcher.md      ← Research (Opus)
│   │   ├── ps-analyst.md         ← Analysis (Sonnet)
│   │   ├── ps-architect.md       ← Architecture (Opus)
│   │   └── ...
│   └── docs/ORCHESTRATION.md     ← Keyword → agent mapping
│
├── nasa-se/
│   ├── agents/
│   │   ├── NSE_AGENT_TEMPLATE.md ← v1.0 template (NASA-enhanced)
│   │   ├── nse-architecture.md   ← Architecture (Opus)
│   │   ├── nse-configuration.md  ← Config mgmt (Haiku)
│   │   └── ...
│   └── docs/ORCHESTRATION.md     ← Process → agent mapping
│
└── orchestration/
    └── agents/
        ├── orch-planner.md       ← Workflow planning
        ├── orch-synthesizer.md   ← Result synthesis
        └── orch-tracker.md       ← State tracking
```

### 3.3 Discovery & Routing Mechanisms

| Mechanism | Trigger | Resolution |
|-----------|---------|------------|
| Explicit invocation | User says "use code-reviewer agent" | Direct name match |
| Auto-delegation | Task matches agent's `description` | LLM-based matching |
| Skill routing | Keywords in ORCHESTRATION.md | `research → ps-researcher` |
| Plugin namespace | `plugin:agent-name` format | Plugin agent lookup |
| Fallback | No match found | `general-purpose` subagent |

---

## 4. Industry Patterns Comparison

### 4.1 Multi-Agent Orchestration Patterns

| Pattern | Description | Used By | Jerry Implementation |
|---------|-------------|---------|---------------------|
| **Hierarchical** | Supervisor delegates to workers | CrewAI, Claude Code | `.claude/agents/orchestrator.md` |
| **Sequential** | Pipeline of agents | LangGraph | ORCHESTRATION.md phase definitions |
| **Parallel** | Concurrent independent agents | AutoGen, LangGraph | Task tool with `run_in_background` |
| **Group Chat** | Agents share single thread | AutoGen | Not implemented (violates P-003) |
| **Scatter-Gather** | Fan-out, aggregate results | LangGraph | orch-synthesizer pattern |

### 4.2 Framework Comparison

| Feature | Claude Code | LangGraph | CrewAI | AutoGen |
|---------|-------------|-----------|--------|---------|
| **Agent definition** | Markdown + YAML | Python code | YAML + Python | Python code |
| **State management** | Implicit (context) | Explicit (graph state) | Crews + Flows | Memory stores |
| **Orchestration** | Single-level | Graph-based | Hierarchical crews | Conversation patterns |
| **Nesting** | 1 level max | Unlimited (subgraphs) | Unlimited | Unlimited |
| **Tool restriction** | Per-agent `tools` field | Per-node tools | Per-agent tools | Per-agent tools |

### 4.3 Key Industry Insights

**Anthropic's Multi-Agent Research (June 2025):**
> "Multi-agent system with Claude Opus 4 as the lead agent and Claude Sonnet 4 subagents outperformed single-agent Claude Opus 4 by 90.2% on internal research evaluations."

**Token Economics:**
> "Agents typically use about 4× more tokens than chat interactions, and multi-agent systems use about 15× more tokens than chats."

**Handoff Best Practices:**
> "Reliability lives and dies in the handoffs. Most 'agent failures' are actually orchestration and context-transfer issues."

**Source:** [Anthropic Multi-Agent Research](https://simonwillison.net/2025/Jun/14/multi-agent-research-system/), [Best Practices for Multi-Agent Orchestration](https://skywork.ai/blog/ai-agent-orchestration-best-practices-handoffs/)

---

## 5. Jerry Framework Implementation

### 5.1 Relationship to Claude Code Subagents

**Statement Analysis:**
> "Jerry agents are NOT Claude Code subagents in the formal sense. They are invocation patterns."

**Revised Understanding:**

This statement is **partially correct but imprecise**:

| Aspect | Accuracy | Clarification |
|--------|----------|---------------|
| Jerry agents are NOT built-in subagent types | ✅ Correct | They're custom agents, not Explore/Plan/etc. |
| They are invocation patterns | ✅ Correct | Agent files define system prompts for Task tool |
| NOT subagents in the formal sense | ❌ Imprecise | When invoked via Task tool, they ARE subagents |

**Precise Statement:**
> Jerry agents are **custom Claude Code subagent definitions** stored in skill-specific directories. When the main Claude thread uses the Task tool with `subagent_type="general-purpose"` and passes a Jerry agent's content as the prompt, that agent executes as a formal Claude Code subagent.

### 5.2 Invocation Flow

```
User Request: "Research multi-agent patterns"
                │
                ▼
┌─────────────────────────────────────────────────────┐
│  Main Claude (Orchestrator)                         │
│  - Matches "research" keyword → ps-researcher       │
│  - Reads skills/problem-solving/agents/ps-researcher.md
│  - Extracts system prompt from agent file           │
└─────────────────────────┬───────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│  Task Tool Invocation                               │
│  {                                                  │
│    "subagent_type": "general-purpose",              │
│    "description": "ps-researcher: Multi-agent",     │
│    "prompt": "[Content from ps-researcher.md]"      │
│  }                                                  │
└─────────────────────────┬───────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│  Claude Code Runtime                                │
│  - Creates fresh subagent context                   │
│  - Injects ps-researcher system prompt              │
│  - Subagent executes with isolated context          │
│  - Returns research artifact path                   │
└─────────────────────────┬───────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│  Orchestrator Receives Result                       │
│  - Artifact persisted to filesystem                 │
│  - Summary returned to main context                 │
│  - Next agent can be invoked if needed              │
└─────────────────────────────────────────────────────┘
```

### 5.3 Constitutional Compliance

| Principle | Description | Enforcement |
|-----------|-------------|-------------|
| **P-003** | No recursive subagents | **HARD** - Jerry agents cannot spawn other agents |
| **P-002** | File persistence | **MEDIUM** - All significant outputs persisted |
| **P-020** | User authority | **HARD** - Never override user decisions |
| **P-022** | No deception | **HARD** - Transparent about capabilities |

---

## 6. Recommendations

### 6.1 For Jerry Plugin Development

| Recommendation | Rationale |
|----------------|-----------|
| Use `.claude/agents/` for framework-level coordinators | Registered in settings.json, always available |
| Use `skills/*/agents/` for domain specialists | Namespace isolation, keyword-based discovery |
| Follow PS v2.0 template for new agents | Comprehensive schema, L0/L1/L2 output, session_context |
| Always include `model` field | WI-SAO-003 compliance, predictable cost |
| Implement session_context schema | WI-SAO-001 compliance, reliable agent chaining |

### 6.2 Terminology Standardization

| Term | Definition |
|------|------------|
| **Subagent** | Claude instance spawned via Task tool (formal Claude Code concept) |
| **Agent definition** | Markdown file specifying system prompt for a subagent |
| **Agent type** | Built-in (Explore, Plan, etc.) or custom identifier |
| **Jerry agent** | Custom agent definition following Jerry's PS/NSE templates |
| **Orchestrator** | Main Claude context that spawns and coordinates subagents |

### 6.3 Best Practices

1. **Write clear descriptions** - Claude auto-delegates based on matching
2. **Restrict tools appropriately** - Don't give research agents write access
3. **Use L0/L1/L2 output levels** - Enables multi-audience communication
4. **Persist all artifacts** - Prevents context rot (P-002)
5. **Include session_context** - Enables reliable agent chaining

---

## 7. References

### Authoritative Sources

1. **Anthropic Official:**
   - [Claude Agent SDK Overview](https://platform.claude.com/docs/en/agent-sdk/overview)
   - [Subagents in the SDK](https://platform.claude.com/docs/en/agent-sdk/subagents)
   - [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
   - [Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)

2. **Claude Code Documentation:**
   - [Create custom subagents](https://code.claude.com/docs/en/sub-agents)
   - [GitHub: anthropics/claude-code](https://github.com/anthropics/claude-code)

3. **Industry Frameworks:**
   - [LangGraph Multi-Agent Workflows](https://blog.langchain.com/langgraph-multi-agent-workflows/)
   - [CrewAI Documentation](https://docs.crewai.com/)
   - [AutoGen: Multi-Agent Conversation](https://microsoft.github.io/autogen/)

4. **Research:**
   - [Context Rot Research (Chroma)](https://research.trychroma.com/context-rot)
   - [Multi-Agent Research System (Anthropic via Simon Willison)](https://simonwillison.net/2025/Jun/14/multi-agent-research-system/)

5. **Best Practices:**
   - [Claude Agent SDK Best Practices 2025](https://skywork.ai/blog/claude-agent-sdk-best-practices-ai-agents-2025/)
   - [AI Agent Orchestration Best Practices](https://skywork.ai/blog/ai-agent-orchestration-best-practices-handoffs/)

### Jerry Framework References

- `docs/governance/JERRY_CONSTITUTION.md` - Constitutional principles
- `skills/problem-solving/agents/PS_AGENT_TEMPLATE.md` - v2.0 template
- `skills/nasa-se/agents/NSE_AGENT_TEMPLATE.md` - v1.0 template
- `docs/schemas/session_context.json` - Agent handoff schema

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **5W1H** | Who, What, When, Where, Why, How - analysis framework |
| **Agentic system** | LLM autonomously directing its own processes and tool usage |
| **Context rot** | Performance degradation as context window fills |
| **Orchestrator** | Main Claude thread coordinating subagents |
| **Subagent** | Isolated Claude instance for focused subtasks |
| **Task tool** | Claude Code tool for spawning subagents |
| **Workflow** | LLMs orchestrated through predefined code paths |

---

**Document Version:** 1.0.0
**Last Updated:** 2026-01-10
**Status:** COMPLETE

---

*This research was conducted following NASA SE Handbook (NPR 7123.1D) Process 17: Decision Analysis methodology and Jerry Constitution principles P-001 (Truth and Accuracy), P-002 (File Persistence), and P-011 (Evidence-Based Decisions).*
