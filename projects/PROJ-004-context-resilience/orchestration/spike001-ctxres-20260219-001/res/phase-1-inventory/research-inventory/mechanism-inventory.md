# Mechanism Inventory: Context Awareness in Claude Code & Anthropic API

<!-- PS-ID: SPIKE-001 | ENTRY-ID: phase-1-inventory | DATE: 2026-02-19 -->
<!-- AGENT: ps-researcher v2.2.0 | MODEL: claude-opus-4-6 -->

> Comprehensive inventory of all existing mechanisms for context awareness, token tracking,
> and session management available through Claude Code and the Anthropic API.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Summary](#l0-summary) | Executive summary for stakeholders |
| [Area 1: API Token Counting & Context Management](#area-1-api-token-counting--context-management) | Anthropic API mechanisms for token counting, compaction, context editing |
| [Area 2: Claude Code Hook System](#area-2-claude-code-hook-system) | Hook events, transcript access, context injection |
| [Area 3: System-Reminder Messages](#area-3-system-reminder-messages) | Injected context, reinforcement, compaction signals |
| [Area 4: Existing Framework Handling (AE-006)](#area-4-existing-framework-handling-ae-006) | Current Jerry framework rules for token exhaustion |
| [Area 5: Status Line Integration](#area-5-status-line-integration) | ECW status line context monitoring |
| [L2 Capability Matrix](#l2-capability-matrix) | Scored comparison of all mechanisms |
| [Gaps & Limitations](#gaps--limitations) | What mechanisms do not exist that we need |
| [References](#references) | All sources with URLs |

---

## L0 Summary

Claude Code and the Anthropic API provide several mechanisms for monitoring and managing context window usage, but **no single mechanism provides a complete, proactive context exhaustion detection system suitable for multi-orchestration workflows**.

The Anthropic API offers a dedicated token counting endpoint (`POST /v1/messages/count_tokens`), detailed usage objects in every API response (including per-iteration breakdowns for compaction), and a server-side compaction system (`compact_20260112`) that automatically summarizes conversations when token thresholds are exceeded. Claude Code extends this with a hook system that provides `$TRANSCRIPT_PATH` access to the full session transcript, a `PreCompact` event that fires before compaction occurs, and `UserPromptSubmit` hooks that can inject context into every prompt.

However, **none of these mechanisms are currently accessible to the LLM itself during a session**. The status line script (ECW v2.1.0) reads context window data from Claude Code's status line JSON feed and can detect compaction via token-count deltas, but this data is displayed to the human operator, not exposed to the model. The Jerry framework's AE-006 rule mandates "mandatory human escalation" when token exhaustion occurs at C3+ criticality, but has no automated detection mechanism -- it relies entirely on the operator or the model noticing degradation after the fact.

The primary gap is a **proactive, model-accessible context fill signal** that enables the orchestrator to checkpoint and hand off before degradation occurs, rather than reacting after context rot has already impacted output quality.

---

## Area 1: API Token Counting & Context Management

### M-001: Token Counting Endpoint

**Mechanism:** `POST /v1/messages/count_tokens`

**What it does:** Counts the number of input tokens for a given message payload *before* sending it to Claude. Accepts the same structured inputs as the Messages API (system prompts, tools, images, PDFs).

**Response format:**
```json
{ "input_tokens": 14 }
```

When used with `context_management.edits` containing compaction, also returns:
```json
{
  "input_tokens": 25000,
  "context_management": {
    "original_input_tokens": 70000
  }
}
```

**Key properties:**
- Free to use (separate rate limits from message creation)
- Rate limits: 100 RPM (Tier 1) to 8,000 RPM (Tier 4)
- Returns an estimate; actual token count may differ slightly
- May include system-added tokens (not billed)
- Does NOT use prompt caching logic
- Applies existing `compaction` blocks but does NOT trigger new compactions
- Supports all active models

**Relevance to context detection:** This is the most accurate pre-send token count available. However, it requires an API call from the *client* (Claude Code), not from the LLM itself. The LLM cannot invoke this endpoint during a session.

**Source:** [Token Counting - Anthropic API Docs](https://platform.claude.com/docs/en/build-with-claude/token-counting), [Count Tokens API Reference](https://platform.claude.com/docs/en/api/messages-count-tokens)

---

### M-002: Usage Objects in API Responses

**Mechanism:** `usage` field in every Messages API response.

**What it provides:**
```json
{
  "usage": {
    "input_tokens": 45000,
    "output_tokens": 1234,
    "cache_creation_input_tokens": 5000,
    "cache_read_input_tokens": 30000
  }
}
```

When compaction is enabled and triggered, the response includes an `iterations` array:
```json
{
  "usage": {
    "input_tokens": 45000,
    "output_tokens": 1234,
    "iterations": [
      {
        "type": "compaction",
        "input_tokens": 180000,
        "output_tokens": 3500
      },
      {
        "type": "message",
        "input_tokens": 23000,
        "output_tokens": 1000
      }
    ]
  }
}
```

**Key properties:**
- Available in every API response
- Top-level `input_tokens` and `output_tokens` exclude compaction iteration usage
- `iterations` array only populated when a *new* compaction is triggered
- To calculate total tokens consumed, sum across all entries in `usage.iterations`
- `cache_creation_input_tokens` and `cache_read_input_tokens` show prompt caching behavior

**Relevance to context detection:** Usage data is returned to Claude Code (the client), not to the LLM. The LLM does not have direct access to usage metadata from previous turns.

**Source:** [Compaction - Understanding Usage](https://platform.claude.com/docs/en/build-with-claude/compaction), [Context Editing - Response](https://platform.claude.com/docs/en/build-with-claude/context-editing)

---

### M-003: Server-Side Compaction (compact_20260112)

**Mechanism:** `context_management.edits` with `type: "compact_20260112"` in Messages API requests.

**What it does:** Automatically summarizes conversation when input tokens exceed a configured trigger threshold. The API generates a `compaction` block containing the summary and continues the response with the compacted context.

**Configuration parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `type` | string | Required | `"compact_20260112"` |
| `trigger.type` | string | `"input_tokens"` | Trigger type |
| `trigger.value` | number | 150,000 | Token threshold (minimum 50,000) |
| `pause_after_compaction` | boolean | `false` | Pause after generating summary |
| `instructions` | string | null | Custom summarization prompt (replaces default entirely) |

**Default summarization prompt:** Instructs Claude to write a summary preserving state, next steps, and learnings, wrapped in `<summary></summary>` tags.

**Compaction block format:**
```json
{
  "content": [
    {
      "type": "compaction",
      "content": "Summary of the conversation..."
    },
    {
      "type": "text",
      "text": "Based on our conversation so far..."
    }
  ]
}
```

**Key behaviors:**
- When `pause_after_compaction` is true, returns with `stop_reason: "compaction"` -- enables adding preserved messages before continuing
- All message blocks prior to the last `compaction` block are dropped on subsequent requests
- Can combine with prompt caching (add `cache_control` on compaction blocks)
- Supported models: Claude Opus 4.6, Claude Sonnet 4.6
- Beta header required: `compact-2026-01-12`
- Can count compactions to enforce a total token budget

**Relevance to context detection:** Compaction is the primary API-level mechanism for managing long conversations. The `pause_after_compaction` + compaction counter pattern enables budget enforcement. However, compaction is triggered and managed by the *client*, not the LLM. The LLM experiences compaction as a loss of earlier context -- it does not receive a signal that compaction occurred unless the client injects one.

**Source:** [Compaction - Anthropic API Docs](https://platform.claude.com/docs/en/build-with-claude/compaction)

---

### M-004: Context Editing (Tool Result & Thinking Clearing)

**Mechanism:** `context_management.edits` with `type: "clear_tool_uses_20250919"` or `type: "clear_thinking_20251015"`.

**What it does:** Selectively clears specific content from conversation history when thresholds are exceeded.

**Tool result clearing (`clear_tool_uses_20250919`):**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `trigger` | 100,000 input tokens | When to activate clearing |
| `keep` | 3 tool uses | Recent tool use/result pairs to preserve |
| `clear_at_least` | None | Minimum tokens to clear (for cache invalidation tradeoff) |
| `exclude_tools` | None | Tool names to never clear |
| `clear_tool_inputs` | `false` | Whether to also clear tool call parameters |

**Thinking block clearing (`clear_thinking_20251015`):**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `keep` | 1 thinking turn | How many recent assistant turns with thinking to preserve |

**Response includes applied edits:**
```json
{
  "context_management": {
    "applied_edits": [
      {
        "type": "clear_tool_uses_20250919",
        "cleared_tool_uses": 8,
        "cleared_input_tokens": 50000
      }
    ]
  }
}
```

**Key properties:**
- Applied server-side before prompt reaches Claude
- Client maintains full, unmodified history (no sync needed)
- Cleared results replaced with placeholder text
- Can combine with Memory Tool for preserving important information before clearing
- Beta header: `context-management-2025-06-27`
- Supported models: Claude Opus 4.6, Sonnet 4.6, Opus 4.5, Opus 4.1, Opus 4, Sonnet 4.5, Sonnet 4, Haiku 4.5

**Relevance to context detection:** Like compaction, context editing is managed by the client. Claude receives an "automatic warning to preserve important information" when combined with the Memory Tool, but does not otherwise receive a signal about clearing events.

**Source:** [Context Editing - Anthropic API Docs](https://platform.claude.com/docs/en/build-with-claude/context-editing)

---

### M-005: Context Window Limits per Model

| Model | Standard Context | Extended Context (Beta) | Max Output |
|-------|-----------------|------------------------|------------|
| Claude Opus 4.6 | 200K tokens | 1M tokens (Tier 4+) | 128K tokens |
| Claude Sonnet 4.6 | 200K tokens | 1M tokens (Tier 4+) | 128K tokens |
| Claude Sonnet 4.5 | 200K tokens | 1M tokens (Tier 4+) | 128K tokens |
| Claude Haiku 4.5 | 200K tokens | N/A | 64K tokens |

**Note:** The 1M token context window is currently in beta for organizations in usage tier 4 and organizations with custom rate limits.

**Relevance to context detection:** The default context window for Claude Code sessions is 200K tokens. The status line script defaults to 200,000 (`context_window_size`). The Jerry framework's enforcement budget is calculated against 200K (15,100 tokens = 7.6% of 200K).

**Source:** [Context Windows - Anthropic API Docs](https://platform.claude.com/docs/en/build-with-claude/context-windows), [What's New in Claude 4.6](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-6)

---

## Area 2: Claude Code Hook System

### M-006: Hook Event Types

Claude Code provides a hook system with multiple event types. The following table summarizes all events and their relevance to context monitoring:

| Hook Event | When Fired | Decision Control | Context Injection | Context Relevance |
|------------|-----------|-----------------|-------------------|-------------------|
| `SessionStart` | Session begins | No (cannot block) | Yes (`additionalContext`) | Can inject initial context awareness instructions |
| `UserPromptSubmit` | User submits prompt | Yes (can block) | Yes (`additionalContext`) | **HIGH** -- fires every prompt, can inject context fill data |
| `PreToolUse` | Before tool execution | Yes (approve/block) | No | Can gate tool use based on context state |
| `PostToolUse` | After tool execution | Yes (can block) | No | Can inspect tool results |
| `Stop` | Agent about to stop | Yes (can block stop) | No | **HIGH** -- can prevent stop and inject checkpoint instructions |
| `SubagentStop` | Subagent completes | Yes (can block) | No | Can monitor subagent completion |
| `PreCompact` | Before compaction | No | No | **CRITICAL** -- signals compaction is about to happen |
| `Notification` | System notification | No | No | Low relevance |

**Key discovery -- PreCompact event:** The `PreCompact` hook fires *before* context compaction occurs. Its input includes `trigger` (manual/auto) and `custom_instructions`. This is the most direct signal that context exhaustion is imminent. However, `PreCompact` has no decision control and no ability to inject context -- it can only run side-effect scripts (e.g., checkpoint state to files).

**Source:** [Claude Code Hooks Documentation](https://code.claude.com/docs/en/hooks), [Context7 /anthropics/claude-code](https://github.com/anthropics/claude-code), Prior Jerry research (PROJ-001 fix-researcher-task006)

---

### M-007: $TRANSCRIPT_PATH Environment Variable

**Mechanism:** `$TRANSCRIPT_PATH` is available to all hook scripts. It points to the full session transcript file (JSONL format).

**What the transcript contains:**
- All user and assistant messages
- Tool use blocks (name, input, tool_use_id)
- Tool result blocks
- Usage objects per turn (input_tokens, output_tokens)

**Key properties:**
- Available in ALL hook events as an environment variable
- Also available in the hook input JSON as `transcript_path`
- The transcript is a JSONL file -- one JSON object per line
- Can be parsed to count cumulative tokens, tool uses, turn count, etc.
- Size grows continuously throughout the session

**Relevance to context detection:** A hook script could parse the transcript to estimate current context fill by summing usage data across turns. The ECW status line already does a version of this for tool token tracking. However, this would be a *heuristic* estimate -- the transcript records what was sent, not what is currently in the context window after compaction or editing.

**Source:** [Claude Code Advanced Hooks](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/hook-development/references/advanced.md), ECW statusline.py (codebase)

---

### M-008: Hook Types (Command vs. Prompt)

| Type | What It Does | Context Access |
|------|-------------|---------------|
| `command` | Executes shell command | Full filesystem + env vars + `$TRANSCRIPT_PATH` |
| `prompt` | Sends prompt to LLM | Can reference `$TRANSCRIPT_PATH` in prompt text |

**Prompt hooks** are particularly relevant because they instruct the LLM to review the transcript and make decisions. Example from Context7:
```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Review the full transcript at $TRANSCRIPT_PATH. Check: 1) Were tests run after code changes? ..."
        }
      ]
    }
  ]
}
```

**Relevance to context detection:** A prompt hook on `Stop` or `UserPromptSubmit` could instruct the LLM to analyze the transcript for context fill signals. However, prompt hooks consume additional tokens and add latency. A command hook that computes metrics and injects them as `additionalContext` would be more efficient.

**Source:** [Claude Code Hooks Documentation](https://code.claude.com/docs/en/hooks), [Context7 /anthropics/claude-code](https://github.com/anthropics/claude-code)

---

### M-009: Hook Output Schemas

The Jerry framework has documented hook output schemas in `schemas/hooks/`. Key capabilities:

| Schema | Key Fields | Context Injection |
|--------|-----------|-------------------|
| `session-start-output` | `hookSpecificOutput.additionalContext` | Yes -- concatenated from multiple hooks |
| `user-prompt-submit-output` | `hookSpecificOutput.additionalContext`, `decision` | Yes -- added to Claude's context window |
| `stop-output` | `decision: "block"`, `reason` | No -- but `reason` tells Claude why to continue |
| `hook-output-base` | `continue`, `stopReason`, `suppressOutput`, `systemMessage` | `systemMessage` shown to user, not to Claude |

**The `additionalContext` field in `UserPromptSubmit` is the primary mechanism for injecting per-prompt data into Claude's context window.** This is already used by Jerry's L2 reinforcement system (`user-prompt-submit.py` + `PromptReinforcementEngine`).

**Source:** Codebase schemas (`/schemas/hooks/*.json`), Prior Jerry research

---

### M-010: Existing Jerry Hook Implementations

The Jerry framework currently has the following hooks configured:

| Hook | Script | Purpose |
|------|--------|---------|
| `SessionStart` | `scripts/session_start_hook.py` | Project context injection |
| `UserPromptSubmit` | `hooks/user-prompt-submit.py` | L2 quality rule reinforcement |
| `PreToolUse` | `scripts/pre_tool_use.py` | Tool use gating |
| `SubagentStop` | `scripts/subagent_stop.py` | Subagent completion handling |

**No context monitoring hooks exist.** The `UserPromptSubmit` hook is purely for quality rule injection; it does not measure or report context fill.

**Source:** Codebase (`hooks/hooks.json`, `.claude/settings.local.json`)

---

## Area 3: System-Reminder Messages

### M-011: system-reminder Tags

Claude Code injects `<system-reminder>` tags into the conversation. Based on observation, these tags contain:

- **CLAUDE.md contents** -- Project instructions loaded at session start
- **Rule file contents** -- Files from `.context/rules/` loaded via `.claude/rules/` symlinks
- **currentDate** -- Current date injected as `# currentDate` section
- **Hook-injected content** -- Content from `SessionStart` and `UserPromptSubmit` hook `additionalContext`

**What system-reminder does NOT contain:**
- Current token usage or context fill percentage
- Context window size
- Compaction status or history
- Warning about approaching context limits

**Relevance to context detection:** System-reminder is the delivery mechanism for injected context, but it does not itself carry any context-fill metadata. If we inject context fill data via a `UserPromptSubmit` hook, it would appear inside a `<system-reminder>` tag.

**Source:** Direct observation of system-reminder content in current session

---

### M-012: Quality Reinforcement Injection (L2)

**Mechanism:** The `UserPromptSubmit` hook injects `<quality-reinforcement>` tags containing L2-REINJECT markers from `quality-enforcement.md`.

**How it works:**
1. `user-prompt-submit.py` runs on every user prompt
2. `PromptReinforcementEngine` reads `quality-enforcement.md`
3. Parses `<!-- L2-REINJECT: rank=N, tokens=M, content="..." -->` markers
4. Assembles a token-budgeted preamble (600 tokens max)
5. Returns via `hookSpecificOutput.additionalContext`
6. Claude Code wraps in `<quality-reinforcement>` or `<system-reminder>` tags

**Current budget:** ~600 tokens per prompt for L2 reinforcement.

**Relevance to context detection:** This is the proven pattern for injecting per-prompt data into Claude's context. A context-fill signal could be added to this same injection pipeline or as a parallel `UserPromptSubmit` hook.

**Source:** Codebase (`hooks/user-prompt-submit.py`, `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py`)

---

### M-013: Compaction Notifications

**Does Claude Code notify the LLM when compaction occurs?**

Based on research:
- The API returns a `compaction` block in the response content, which gets passed back on subsequent requests
- Claude Code uses compaction internally; the `PreCompact` hook fires before compaction
- The default compaction summarization prompt instructs Claude to write a summary preserving state, next steps, and learnings
- **There is no documented mechanism by which Claude Code injects a "compaction just occurred" notification into the LLM's context after compaction completes**

The LLM experiences compaction as a sudden loss of earlier conversation detail, replaced by a summary. It may or may not "know" that compaction happened -- this depends on whether the summary includes a note about being a compaction summary.

**Relevance to context detection:** This is a significant gap. If compaction occurs, the LLM should be informed so it can re-orient and verify that critical state was preserved.

**Source:** [Compaction - Anthropic API Docs](https://platform.claude.com/docs/en/build-with-claude/compaction), [Anthropic Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

---

## Area 4: Existing Framework Handling (AE-006)

### M-014: AE-006 Auto-Escalation Rule

**Current specification** from `quality-enforcement.md`:

| ID | Condition | Escalation |
|----|-----------|------------|
| AE-006 | Token exhaustion at C3+ (context compaction triggered) | Mandatory human escalation |

**What AE-006 mandates:**
- When token exhaustion occurs during C3+ criticality work
- And context compaction is triggered
- The response MUST be: mandatory human escalation

**What AE-006 does NOT specify:**
- How to *detect* that token exhaustion has occurred
- What "token exhaustion" means quantitatively (threshold)
- How to detect that "context compaction triggered"
- What the escalation protocol looks like (who to escalate to, what information to provide)
- How to checkpoint state before escalation
- How to resume after the human reviews

**Implementation status:** AE-006 is a *policy* rule with **no automated implementation**. There is:
- No hook that monitors context fill
- No mechanism that detects compaction programmatically
- No escalation workflow triggered automatically
- No checkpoint protocol defined

The rule relies entirely on the human operator or the model recognizing degradation symptoms (rule violations, inconsistent output, forgotten constraints) after the fact.

**Source:** `.context/rules/quality-enforcement.md` (lines 138-145)

---

### M-015: Enforcement Architecture Context Rot Assessment

The enforcement architecture (ADR-EPIC002-002) explicitly documents context rot vulnerability by layer:

| Layer | Context Rot Vulnerability |
|-------|--------------------------|
| L1 (Session start) | **Vulnerable** -- degrades with context fill |
| L2 (Every prompt) | **Immune** -- re-injected every prompt |
| L3 (Pre-tool-call) | **Immune** -- deterministic gating |
| L4 (Post-tool-call) | **Mixed** -- deterministic gating immune, self-correction vulnerable |
| L5 (Commit/CI) | **Immune** -- runs outside context |

**Key insight:** L1 rules (CLAUDE.md, rule files) are loaded once at session start and degrade as context fills. L2 re-injection was designed specifically to counter this degradation for critical rules. But there is no mechanism to detect *when* L1 degradation is occurring or how severe it is.

**Source:** `.context/rules/quality-enforcement.md` (lines 149-161)

---

### M-016: DISC-001 Context Rot Threshold

The Jerry knowledge base documents the "context rot threshold" discovery:

> "Chroma Research identified 'context rot' as a phenomenon where LLM accuracy degrades significantly as the context window fills, even when total token count is well within the advertised technical limit. Their research shows that at approximately 256k tokens, performance degradation becomes severe enough to impact practical applications."

**Relevance:** The 256K threshold provides a research-backed anchor for detection thresholds, though it predates the 4.6 model family. The SPIKE-001 hypothesis proposes warning at ~70% and critical at ~85% of context window.

**Source:** `docs/knowledge/DISCOVERIES_EXPANDED.md` (DISC-001), [Chroma Research: Context Rot](https://research.trychroma.com/context-rot)

---

## Area 5: Status Line Integration

### M-017: ECW Status Line (statusline.py v2.1.0)

**Mechanism:** A Python script (`/.claude/statusline.py`) that reads JSON data from Claude Code's stdin and renders a status line for the human operator.

**Data it extracts from the Claude Code status line JSON feed:**

| Data Point | JSON Path | Description |
|-----------|-----------|-------------|
| Context window size | `context_window.context_window_size` | Default: 200,000 |
| Current input tokens | `context_window.current_usage.input_tokens` | Fresh (non-cached) tokens |
| Cache creation tokens | `context_window.current_usage.cache_creation_input_tokens` | Tokens being cached |
| Cache read tokens | `context_window.current_usage.cache_read_input_tokens` | Tokens read from cache |
| Total input tokens | `context_window.total_input_tokens` | Cumulative input tokens |
| Total output tokens | `context_window.total_output_tokens` | Cumulative output tokens |
| Total cost | `cost.total_cost_usd` | Session cost in USD |
| Duration | `cost.total_duration_ms` | Session duration |
| Model info | `model.display_name`, `model.id` | Current model |
| Transcript path | `transcript_path` | Path to transcript JSONL |
| Workspace dir | `workspace.current_dir` | Current directory |

**Compaction detection algorithm:**
The status line tracks `previous_context_tokens` in a state file (`~/.claude/ecw-statusline-state.json`). If the current context token count drops by more than `detection_threshold` (default: 10,000 tokens) compared to the previous count, compaction is detected.

**Context fill thresholds:**
- Warning: 65% of context window (configurable)
- Critical: 85% of context window (configurable)

**Key insight:** The status line JSON feed from Claude Code contains `context_window.current_usage` with detailed token breakdowns. This data is available to scripts that can read Claude Code's status line input but is **not available to hooks or to the LLM itself**.

**Limitation (P-022):** It is unclear whether the status line JSON data is the same data available to hooks, or whether hooks receive a different (more limited) input schema. The hook input schema documented in prior research (M-006) does not include `context_window` data -- it provides `session_id`, `transcript_path`, `cwd`, and event-specific fields. **This is a critical gap that needs verification.**

**Source:** Codebase (`.claude/statusline.py`), ECW Status Line documentation (embedded in file)

---

## L2 Capability Matrix

Each mechanism is scored on four dimensions (1-5 scale):

| Dimension | Definition |
|-----------|------------|
| **Availability** | How readily accessible is this mechanism? (5 = always available, 1 = requires special setup) |
| **Reliability** | How accurate/trustworthy is the data? (5 = exact, 1 = rough heuristic) |
| **Overhead** | Token/latency cost of using it (5 = zero overhead, 1 = significant cost) |
| **Granularity** | How detailed is the information? (5 = per-token detail, 1 = binary signal) |

| ID | Mechanism | Availability | Reliability | Overhead | Granularity | Accessible to LLM? |
|----|-----------|:---:|:---:|:---:|:---:|:---:|
| M-001 | Token Counting API | 4 | 5 | 4 | 5 | No (client-side) |
| M-002 | Usage Objects | 5 | 5 | 5 | 4 | No (client-side) |
| M-003 | Server-Side Compaction | 4 | 4 | 3 | 3 | Indirect (summary) |
| M-004 | Context Editing | 4 | 4 | 4 | 3 | No (client-side) |
| M-005 | Context Window Limits | 5 | 5 | 5 | 1 | Yes (documented) |
| M-006 | Hook Events | 5 | 5 | 4 | 2 | No (script-side) |
| M-007 | $TRANSCRIPT_PATH | 5 | 3 | 3 | 3 | No (script-side) |
| M-008 | Prompt Hooks | 4 | 3 | 2 | 3 | Yes (via LLM prompt) |
| M-009 | Hook Output (additionalContext) | 5 | 5 | 4 | N/A | Yes (injected) |
| M-010 | Jerry L2 Reinforcement | 5 | 5 | 4 | N/A | Yes (injected) |
| M-011 | system-reminder Tags | 5 | 5 | 4 | 1 | Yes (visible) |
| M-012 | Quality Reinforcement | 5 | 5 | 4 | N/A | Yes (injected) |
| M-013 | Compaction Notifications | 1 | 1 | 5 | 1 | No (not implemented) |
| M-014 | AE-006 Rule | 5 | N/A | 5 | 1 | Yes (rule text) |
| M-015 | Enforcement Rot Assessment | 5 | 4 | 5 | 2 | Yes (documented) |
| M-016 | DISC-001 Threshold | 5 | 3 | 5 | 2 | Yes (documented) |
| M-017 | ECW Status Line | 4 | 4 | 5 | 4 | No (operator-only) |

### Key Observations from Matrix

1. **The most reliable mechanisms (M-001, M-002) are client-side only** -- the LLM cannot access them.
2. **The injection pathway exists and is proven (M-009, M-010, M-012)** -- the `UserPromptSubmit` hook's `additionalContext` successfully injects per-prompt data into Claude's context.
3. **The detection data exists (M-017)** -- the ECW status line reads `context_window.current_usage` from Claude Code's JSON feed, but this is not available to hooks.
4. **The PreCompact event (M-006) is the most direct compaction signal** -- but it fires too late for proactive checkpointing and has no context injection capability.

---

## Gaps & Limitations

### GAP-001: No Model-Accessible Context Fill Signal

**What's missing:** There is no mechanism by which the LLM knows its current context fill percentage during a session. The model cannot call `count_tokens` on its own context. No system message reports token usage.

**Impact:** The model cannot proactively decide to checkpoint or escalate based on context fill. It must rely on external signals (human operator, hooks injecting data) or detect degradation symptoms after they occur.

**Proposed solution path:** A `UserPromptSubmit` command hook that reads context fill data (either from the status line JSON feed, transcript parsing, or a token counting heuristic) and injects it as `additionalContext`.

---

### GAP-002: No Automated AE-006 Implementation

**What's missing:** AE-006 mandates "mandatory human escalation" on token exhaustion at C3+, but there is no automated detection, no escalation workflow, and no checkpoint protocol.

**Impact:** Token exhaustion at C3+ criticality results in silent degradation until the human or model notices quality issues.

**Proposed solution path:** Implement AE-006 as a concrete workflow: detection hook (GAP-001) triggers escalation when critical threshold is reached during C3+ work.

---

### GAP-003: Hook Input Does Not Include Context Window Data

**What's missing:** Hook input JSON provides `session_id`, `transcript_path`, `cwd`, and event-specific fields, but does NOT include `context_window` data (current usage, window size, fill percentage).

**Impact:** A `UserPromptSubmit` hook cannot directly read context fill from its input. It must estimate context fill through alternative means (transcript parsing, external API call, status line data pipe).

**Proposed solution path:** (a) Parse `$TRANSCRIPT_PATH` to sum usage data across turns as a heuristic, or (b) investigate whether the status line JSON data can be accessed from hook scripts, or (c) call the `count_tokens` API from a hook script (requires API key access and adds latency).

---

### GAP-004: No Post-Compaction Notification to LLM

**What's missing:** After compaction occurs, the LLM is not explicitly told "compaction just happened." The compaction summary replaces earlier context, but the LLM may not recognize this as a compaction event.

**Impact:** The orchestrator cannot reliably verify that critical state (work tracker status, orchestration position, quality gate progress) survived compaction.

**Proposed solution path:** Use the `PreCompact` hook to write a checkpoint file, then use a `UserPromptSubmit` hook to detect that a checkpoint file exists and inject a "compaction occurred, re-orient from checkpoint" message.

---

### GAP-005: No Threshold Calibration Data

**What's missing:** The DISC-001 discovery cites 256K tokens as a degradation threshold based on older models. There is no calibrated data for Claude Opus 4.6 or Sonnet 4.6, especially with 200K or 1M context windows.

**Impact:** Detection thresholds are based on hypothesis (70% warning, 85% critical) rather than empirical data for current models.

**Proposed solution path:** This gap will be addressed by SPIKE-001 Phase 2 (analysis of real orchestration runs).

---

### GAP-006: Transcript Parsing Token Estimation is Approximate

**What's missing:** The transcript JSONL contains usage data per turn, but summing `input_tokens` across turns does not give the current context window fill because: (a) compaction reduces effective context, (b) context editing clears content, (c) prompt caching changes what's "in" the window.

**Impact:** Any transcript-based context fill estimate is a heuristic, not an exact measurement.

**Proposed solution path:** Use transcript-based estimation as a floor/ceiling heuristic, calibrated against known context window sizes. The `count_tokens` API could provide periodic exact measurements if latency is acceptable.

---

## References

| # | Source | URL / Path | Access Date |
|---|--------|------------|-------------|
| 1 | Token Counting - Anthropic API Docs | https://platform.claude.com/docs/en/build-with-claude/token-counting | 2026-02-19 |
| 2 | Count Tokens API Reference | https://platform.claude.com/docs/en/api/messages-count-tokens | 2026-02-19 |
| 3 | Compaction - Anthropic API Docs | https://platform.claude.com/docs/en/build-with-claude/compaction | 2026-02-19 |
| 4 | Context Editing - Anthropic API Docs | https://platform.claude.com/docs/en/build-with-claude/context-editing | 2026-02-19 |
| 5 | Context Windows - Anthropic API Docs | https://platform.claude.com/docs/en/build-with-claude/context-windows | 2026-02-19 |
| 6 | What's New in Claude 4.6 | https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-6 | 2026-02-19 |
| 7 | Claude Code Hooks Documentation | https://code.claude.com/docs/en/hooks | 2026-02-17 |
| 8 | Context7 /anthropics/claude-code | https://github.com/anthropics/claude-code | 2026-02-19 |
| 9 | Effective Context Engineering for AI Agents | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | 2026-02-19 |
| 10 | Chroma Research: Context Rot | https://research.trychroma.com/context-rot | (via DISC-001) |
| 11 | Jerry quality-enforcement.md | `.context/rules/quality-enforcement.md` | 2026-02-19 |
| 12 | Jerry ECW statusline.py v2.1.0 | `.claude/statusline.py` | 2026-02-19 |
| 13 | Jerry hooks/hooks.json | `hooks/hooks.json` | 2026-02-19 |
| 14 | Jerry user-prompt-submit.py | `hooks/user-prompt-submit.py` | 2026-02-19 |
| 15 | Jerry PromptReinforcementEngine | `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py` | 2026-02-19 |
| 16 | Jerry DISCOVERIES_EXPANDED.md | `docs/knowledge/DISCOVERIES_EXPANDED.md` | 2026-02-19 |
| 17 | Jerry PROJ-001 Hook Research (task006) | `projects/PROJ-001-oss-release/orchestration/.../context7-research.md` | 2026-02-19 |
| 18 | Hook Output Schemas | `schemas/hooks/*.json` | 2026-02-19 |
| 19 | Claude Code Hook SDK (mizunashi-mana) | https://github.com/mizunashi-mana/claude-code-hook-sdk | 2026-02-19 |
