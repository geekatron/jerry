# Research: Option C - Hook-Based Trigger for Automatic Agent Invocation

> **PS:** phase-38.17
> **Exploration:** e-123
> **Created:** 2026-01-04
> **Status:** COMPLETE
> **Agent:** ps-researcher
> **Session:** Phase 38.17 Agent Portfolio

---

## Executive Summary

This research investigates the feasibility of using Claude Code hooks as triggers for automatic agent invocation when Problem Statement entries are created. The investigation reveals that while hooks CAN detect PS operations and signal intent, they CANNOT directly invoke agents due to fundamental subprocess isolation constraints (LES-030). However, a viable **file-based signaling pattern** can bridge this gap, where hooks write signal files that the main Claude context reads and acts upon.

**Key Finding:** Hook-based triggers are FEASIBLE but require a two-phase architecture:
1. **Phase 1:** Hook detects operation and writes signal file with invocation request
2. **Phase 2:** Main context (via Stop hook prompt or next turn) reads signal and invokes Task

**Recommendation:** Implement as a complementary mechanism to Option E (SDK orchestrator), not as a standalone solution. Hook signals can queue invocations that the orchestrator executes.

---

## Research Questions

1. What are Claude Code hook capabilities and limitations for detecting PS operations?
2. Can hooks modify tool input/output to inject agent invocation instructions?
3. What communication mechanisms exist between hooks and the main Claude context?
4. What implementation patterns from prior art (GitHub Actions, webhook systems) apply?
5. Is file-based signaling between hook and main context architecturally sound?

---

## Methodology

### Web Research
- **Keywords:** event-driven agent orchestration, webhook triggers, GitHub Actions workflow triggers, observer pattern, file-based IPC
- **Sources Consulted:** 15+ sources including Confluent, Microsoft Azure, Docker, GitHub Docs
- **Date Range:** 2025-2026

### Documentation Review
- **Official Docs:** Claude Code hooks documentation via Context7
- **Community Resources:** Event-driven architecture patterns, multi-agent orchestration guides
- **ECW Internal:** LES-030 (hook-mcp-limitation.md), existing hook implementations

### Codebase Analysis
- **Files Examined:** 7 hook scripts in `.claude/hooks/`
- **Patterns Searched:** PreToolUse, PostToolUse, signal files, JSON output

---

## Findings

### Finding 1: Hook Subprocess Isolation is Fundamental

**Source:** `evolve-claude/sidequests/evolving-claude-workflow/docs/knowledge/hook-mcp-limitation.md`
**Confidence:** HIGH
**Relevance:** Critical architectural constraint that shapes all implementation options

Hooks in Claude Code run as subprocesses and cannot access the MCP (Model Context Protocol) context. This is documented extensively in LES-030 from Phase 34:

```
Claude Code Process
├── MCP Context Available ✅
│   ├── Claude's direct tool calls
│   ├── SessionStart can call context_*
│   └── User commands can trigger MCP
│
└── Hook Subprocess (spawned)
    ├── MCP Context NOT Available ❌
    ├── No access to context_save()
    ├── No access to context_get()
    └── Can only use filesystem/network/git
```

**Implications for Option C:**
- Hooks CANNOT call the Task tool directly
- Hooks CANNOT invoke agents through MCP
- Hooks CAN write files, return JSON, and set exit codes
- Communication to main context must be indirect

### Finding 2: Hook JSON Output Can Include System Messages

**Source:** [Context7 - Claude Code Hooks Documentation](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/hook-development/SKILL.md)
**Confidence:** HIGH
**Relevance:** Enables passing instructions to Claude's main context

Hooks can return structured JSON with a `systemMessage` field that Claude receives:

```json
{
  "hookSpecificOutput": {
    "permissionDecision": "allow|deny|ask",
    "updatedInput": {"field": "modified_value"}
  },
  "systemMessage": "Explanation for Claude"
}
```

For Stop hooks specifically:
```json
{
  "decision": "approve|block",
  "reason": "Explanation",
  "systemMessage": "Additional context"
}
```

**Key Insight:** The `systemMessage` field provides a channel to communicate intent to Claude, though it cannot force action.

### Finding 3: Stop Hook Can Block and Inject Instructions

**Source:** [Context7 - Claude Code Advanced Hooks](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/hook-development/references/advanced.md)
**Confidence:** HIGH
**Relevance:** Provides mechanism for loop continuation with agent invocation

Stop hooks can block the stop event and return a reason that becomes Claude's next prompt:

```bash
jq -n \
  --arg prompt "$PROMPT_TEXT" \
  --arg msg "Agent invocation required" \
  '{
    "decision": "block",
    "reason": $prompt,
    "systemMessage": $msg
  }'
```

**Implementation Pattern:**
1. PostToolUse hook detects `add-entry` CLI command completion
2. Writes signal file: `.ecw/signals/pending-agent-invocation.json`
3. Stop hook reads signal file
4. If signal exists, blocks stop with `reason` containing Task invocation instruction
5. Claude receives the instruction and invokes the agent

### Finding 4: Event-Driven Agent Patterns from Industry

**Source:** [Confluent - Event-Driven Multi-Agent Systems](https://www.confluent.io/blog/event-driven-multi-agent-systems/)
**Confidence:** HIGH
**Relevance:** Validates orchestrator-worker pattern as proven approach

Four key patterns for multi-agent systems:
1. **Orchestrator-Worker** - Central orchestrator assigns tasks
2. **Hierarchical Agent** - Agents organized in hierarchy
3. **Blackboard** - Shared knowledge space agents read/write
4. **Market-Based** - Agents bid for tasks

For hook-based triggers, the **Blackboard pattern** is most applicable:
- Hook writes to shared signal file (blackboard)
- Main context reads signal file
- Signal contains agent invocation intent

```
┌─────────────────────────────────────────────────────────┐
│                    BLACKBOARD PATTERN                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  PostToolUse Hook ──writes──▶ Signal File (blackboard)   │
│                                      │                   │
│                                      ▼                   │
│  Stop Hook ◀──reads─────────────────┘                   │
│       │                                                  │
│       ▼                                                  │
│  Returns "block" with Task invocation in "reason"        │
│       │                                                  │
│       ▼                                                  │
│  Claude Main Context receives instruction                │
│       │                                                  │
│       ▼                                                  │
│  Invokes Task tool with agent specification              │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Finding 5: GitHub Actions Workflow Triggers Provide Model

**Source:** [GitHub Docs - Events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)
**Confidence:** MEDIUM
**Relevance:** Provides proven pattern for event-based automation

GitHub Actions uses event types + filters for trigger control:
- `push` with `branches` filter
- `pull_request` with `paths` filter
- `repository_dispatch` for webhook/external triggers

**Applicable Pattern for PS Hooks:**
```json
{
  "trigger_type": "ps_entry_created",
  "filters": {
    "entry_type": ["EXPLORATION", "RESEARCH"],
    "ps_id": "phase-38.*"
  },
  "action": {
    "agent": "ps-researcher",
    "prompt": "Research the topic described in entry {entry_id}"
  }
}
```

This could be stored in `.ecw/agent-triggers.json` and read by hooks.

### Finding 6: Webhook Real-Time Handoff Pattern

**Source:** [Moveworks - Webhooks for Ambient Agents](https://www.moveworks.com/us/en/resources/blog/webhooks-triggers-for-ambient-agents)
**Confidence:** MEDIUM
**Relevance:** Validates real-time event-driven agent activation

Key insight: "Event-driven design eliminates lag" - Polling wastes resources while webhooks enable real-time response.

**Applied to Option C:**
- PostToolUse is the "webhook" - fires immediately on CLI completion
- Signal file is the "event payload"
- Stop hook (or next turn) is the "webhook handler"

This is superior to polling because:
1. Trigger fires at exact moment of PS entry creation
2. No delay between event and agent invocation
3. No wasted cycles checking for changes

### Finding 7: Dual Storage Pattern Already Solved This

**Source:** `evolve-claude/sidequests/evolving-claude-workflow/docs/knowledge/hook-mcp-limitation.md`
**Confidence:** HIGH
**Relevance:** Existing pattern can be extended for agent signals

The ECW codebase already implements a Dual Storage Pattern for hook-MCP communication:

```python
class DualStorageManager:
    """
    Primary: Files (always work, no dependencies)
    Cache: SQLite (for performance when available)
    Sync: SessionStart copies files → Memory Keeper
    """
```

**Extension for Agent Signals:**
```python
class AgentSignalManager:
    """
    Signal Location: .ecw/signals/pending-invocations.json
    Signal Format: {agent, prompt, ps_id, entry_id, priority}
    Written By: PostToolUse hook on CLI operation detection
    Read By: Stop hook (for immediate), SessionStart (for deferred)
    Cleared By: Main context after successful Task invocation
    """
```

---

## Implementation Options Analysis

### Option C.1: PostToolUse + Stop Hook Chain

**Mechanism:**
1. PostToolUse detects `python3 cli.py add-entry` command
2. Writes signal file with agent invocation request
3. Stop hook reads signal file at end of turn
4. Blocks stop, returns Task invocation instruction
5. Claude executes Task with agent

**Pros:**
- Real-time (same turn or next)
- Uses existing hook infrastructure
- No external dependencies

**Cons:**
- Complex hook chain logic
- May interfere with normal Stop behavior
- Relies on implicit behavior

**Feasibility:** MEDIUM-HIGH

### Option C.2: PostToolUse + User Prompt Response

**Mechanism:**
1. PostToolUse detects CLI operation
2. Returns JSON with `systemMessage` containing agent prompt
3. Claude sees message, decides to invoke Task
4. Relies on Claude's judgment to act on message

**Pros:**
- Simpler implementation
- Non-blocking
- Claude maintains agency

**Cons:**
- No guarantee Claude acts on message
- Not truly "automatic"
- Relies on LLM interpretation

**Feasibility:** LOW (Not truly automatic)

### Option C.3: Hybrid Hook + External Orchestrator

**Mechanism:**
1. PostToolUse writes signal file
2. External Python orchestrator (Option E) watches signal file
3. Orchestrator invokes SDK to launch agent
4. Agent runs and reports back

**Pros:**
- Combines real-time detection with reliable execution
- Orchestrator has full SDK access
- Hooks remain lightweight

**Cons:**
- Requires external process
- More complex deployment
- Two-system coordination

**Feasibility:** HIGH (Recommended)

---

## Technical Constraints

### Constraint 1: Hook Cannot Call Task Tool
- **Severity:** HARD
- **Source:** LES-030
- **Impact:** Direct agent invocation from hook impossible
- **Workaround:** File-based signaling to main context

### Constraint 2: Hook Output Limits
- **Severity:** MEDIUM
- **Source:** Claude Code hook specification
- **Impact:** systemMessage has practical size limits
- **Workaround:** Reference signal file instead of inline content

### Constraint 3: Stop Hook Blocking Affects UX
- **Severity:** MEDIUM
- **Source:** Behavioral observation
- **Impact:** Blocking stop may confuse users
- **Workaround:** Use systemMessage for soft suggestion, not block

### Constraint 4: Race Conditions
- **Severity:** LOW
- **Source:** Multi-hook coordination
- **Impact:** Signal file may be read before fully written
- **Workaround:** Atomic write pattern (write to temp, rename)

---

## Conclusions

### Key Insights

1. **Hook-based triggers are architecturally feasible** but require indirect communication via file-based signaling rather than direct Task invocation.

2. **The Blackboard pattern** (shared signal file) provides a proven architecture for hook-to-context communication that extends the existing Dual Storage Pattern.

3. **Stop hook blocking** can inject agent invocation instructions into Claude's flow, but is fragile and may interfere with normal operation.

4. **Hybrid approach (C.3)** combining hooks for detection with external orchestrator for execution is the most robust solution.

5. **Real-time detection is valuable** - PostToolUse fires at the exact moment of CLI completion, enabling immediate response without polling overhead.

### Implications

Option C is best viewed as a **complementary mechanism** rather than a standalone solution:

- **Detection Layer:** Hooks excel at real-time event detection
- **Execution Layer:** External orchestrator (Option E) provides reliable Task invocation
- **Combined:** Hooks signal → Orchestrator executes → Agents run

This aligns with the industry trend toward **event-driven agent orchestration** where detection and execution are separated for reliability and scalability.

---

## Recommendations

| Priority | Recommendation | Rationale | Effort |
|----------|---------------|-----------|--------|
| HIGH | Implement signal file infrastructure | Foundation for hook-based detection | S |
| HIGH | Design PostToolUse detection logic for CLI commands | Enables real-time trigger capability | M |
| MEDIUM | Integrate with Option E orchestrator | Provides reliable execution path | L |
| LOW | Explore Stop hook blocking pattern | May enable same-turn invocation, but fragile | M |

---

## Sources

| # | Source | Type | Relevance | Accessed |
|---|--------|------|-----------|----------|
| 1 | [Confluent - Event-Driven Multi-Agent Systems](https://www.confluent.io/blog/event-driven-multi-agent-systems/) | Web | HIGH | 2026-01-04 |
| 2 | [GitHub Docs - Events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows) | Web | HIGH | 2026-01-04 |
| 3 | [Context7 - Claude Code Hooks](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/hook-development/SKILL.md) | Doc | HIGH | 2026-01-04 |
| 4 | [Moveworks - Webhooks for Ambient Agents](https://www.moveworks.com/us/en/resources/blog/webhooks-triggers-for-ambient-agents) | Web | MEDIUM | 2026-01-04 |
| 5 | [Microsoft - AI Agent Orchestration Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) | Web | MEDIUM | 2026-01-04 |
| 6 | hook-mcp-limitation.md | Code | HIGH | 2026-01-04 |
| 7 | post-tool-use.sh | Code | HIGH | 2026-01-04 |
| 8 | pre-tool-use.sh | Code | HIGH | 2026-01-04 |
| 9 | [Docker - Event-Driven Agents](https://www.docker.com/blog/beyond-the-chatbot-event-driven-agents-in-action/) | Web | MEDIUM | 2026-01-04 |
| 10 | [Codefresh - GitHub Actions Triggers](https://codefresh.io/learn/github-actions/github-actions-triggers-5-ways-to-trigger-a-workflow-with-code/) | Web | MEDIUM | 2026-01-04 |

---

## Knowledge Items Generated

### Assumptions (ASM)

- **ASM-082:** Hook signal files can be reliably read by Stop hooks within the same Claude turn
  - Context: Timing of hook execution within Claude Code lifecycle
  - Impact if Wrong: Signal may be missed, requiring next-turn or external processing
  - Confidence: MEDIUM

- **ASM-083:** Stop hook `systemMessage` containing Task instruction will prompt Claude to invoke the Task tool
  - Context: Claude's response to hook-provided instructions
  - Impact if Wrong: Agent invocation would not be "automatic" but require user confirmation
  - Confidence: LOW

### Lessons Learned (LES)

- **LES-058:** Hook-based agent triggers require file-based signaling, not direct invocation
  - Context: Option C research - hook subprocess isolation prevents Task calls
  - Prevention: Use Blackboard pattern (signal files) for hook-to-context communication

### Patterns (PAT)

- **PAT-063:** Hook Signal File Pattern
  - When to Use: When hooks need to communicate intent to main Claude context
  - Structure:
    ```
    PostToolUse ──writes──▶ .ecw/signals/{signal-type}.json
                                    │
    Stop Hook/SessionStart ◀──reads─┘
                    │
                    ▼
    Main context acts on signal (Task invocation, etc.)
    ```
  - Example: Agent invocation signal after PS entry creation

- **PAT-064:** Event-Driven Agent Detection Pattern
  - When to Use: Real-time agent activation based on tool operations
  - Implementation: PostToolUse hook detects CLI commands by parsing `tool_input.command`
  - Example: Detect `add-entry` → signal `ps-researcher` invocation

---

## PS Integration

| Action | Command | Status |
|--------|---------|--------|
| Exploration Entry | `add-entry phase-38.17 "Option C - Hook-Based Trigger"` | Done |
| Entry Type | `set-entry-type phase-38.17 e-123 RESEARCH` | Done |
| Artifact Link | `link-artifact phase-38.17 e-123 FILE "docs/research/phase-38.17-e-123-option-c-hook-trigger.md"` | Pending |
| Knowledge Refs | `add-knowledge phase-38.17 ASM-082 ASM-083 LES-058 PAT-063 PAT-064` | Pending |

---

## Appendix

### Raw Notes

**Hook Detection Logic for CLI Commands:**
```bash
# In post-tool-use.sh
if [[ "$TOOL_NAME" == "Bash" ]]; then
    COMMAND=$(echo "$TOOL_INPUT" | jq -r '.command // empty')

    # Detect PS CLI add-entry command
    if [[ "$COMMAND" =~ python3.*cli\.py.*add-entry ]]; then
        PS_ID=$(echo "$COMMAND" | grep -oP 'add-entry\s+\K[^\s]+')

        # Write signal file
        cat > .ecw/signals/agent-invocation.json <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "trigger": "ps_entry_created",
  "ps_id": "$PS_ID",
  "agent": "ps-researcher",
  "prompt": "Research the newly created PS entry"
}
EOF
    fi
fi
```

**Signal File Schema:**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["timestamp", "trigger", "agent"],
  "properties": {
    "timestamp": {"type": "string", "format": "date-time"},
    "trigger": {"enum": ["ps_entry_created", "ps_status_changed", "ps_question_added"]},
    "ps_id": {"type": "string"},
    "entry_id": {"type": "string"},
    "agent": {"enum": ["ps-researcher", "ps-reviewer", "ps-synthesizer", "ps-planner"]},
    "prompt": {"type": "string"},
    "priority": {"enum": ["immediate", "deferred"]}
  }
}
```

### Related Research

- [phase-38.17-e-066-orchestrator-feasibility.md](./phase-38.17-e-066-orchestrator-feasibility.md) - SDK constraint discovery
- [phase-38.17-e-071-option-e-sdk-orchestrator.md](./phase-38.17-e-071-option-e-sdk-orchestrator.md) - External orchestrator design
- [claude-code-hooks-best-practices.md](./claude-code-hooks-best-practices.md) - Hook implementation patterns

---

**Generated by:** ps-researcher agent
**Template Version:** 1.0 (Phase 38.16.7)
