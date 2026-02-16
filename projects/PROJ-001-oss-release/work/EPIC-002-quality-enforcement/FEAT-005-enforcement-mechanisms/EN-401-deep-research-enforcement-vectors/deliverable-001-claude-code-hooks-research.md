# TASK-001: Claude Code Hooks API and Enforcement Capabilities

> **PS ID:** EN-401
> **Entry ID:** TASK-001
> **Topic:** Claude Code Hooks API and Enforcement Capabilities
> **Agent:** ps-researcher
> **Created:** 2026-02-12
> **Status:** COMPLETE
> **Confidence Level:** HIGH (codebase analysis) / MEDIUM-HIGH (API documentation)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | What hook types exist, key capabilities, main limitations |
| [L1: Technical Analysis](#l1-technical-analysis) | Detailed per-hook-type analysis with implementation examples |
| [L2: Architectural Implications](#l2-architectural-implications) | How hooks fit into multi-vector enforcement strategy |
| [Methodology](#methodology) | Research sources and confidence assessment |
| [References](#references) | All sources cited |
| [Disclaimer](#disclaimer) | Research limitations and caveats |

---

## L0: Executive Summary

### Available Hook Types

Claude Code provides **four confirmed hook event types** in the plugin hooks system, plus additional types documented in the broader Claude Code settings system:

| Hook Type | Confirmed | Jerry Status | Enforcement Power |
|-----------|-----------|-------------|-------------------|
| **SessionStart** | YES (schema + implementation) | IMPLEMENTED | Medium -- one-time context injection |
| **PreToolUse** | YES (schema + implementation) | IMPLEMENTED (security only) | HIGH -- can BLOCK tool calls |
| **PostToolUse** | YES (schema + implementation) | IMPLEMENTED (output filtering only) | Medium -- reactive validation, output modification |
| **Stop** | YES (schema + implementation) | IMPLEMENTED (subagent handoff) | Medium -- gate on completion |
| **UserPromptSubmit** | DOCUMENTED in research but NOT in Jerry's hooks.schema.json | NOT IMPLEMENTED | CRITICAL -- persistent enforcement on every prompt |
| **PostToolUseFailure** | Referenced in best-practices research | NOT IMPLEMENTED | Low -- error recovery |
| **PreCompact** | Referenced in best-practices research | NOT IMPLEMENTED | Low -- state preservation |
| **SubagentStart** | Referenced in best-practices research | NOT IMPLEMENTED | Low -- resource management |

### Critical Finding: UserPromptSubmit Uncertainty

**The most critical finding of this research is an ambiguity about UserPromptSubmit hooks.**

Jerry's `hooks.schema.json` (the authoritative schema for plugin hooks) defines ONLY four hook types: `PreToolUse`, `PostToolUse`, `SessionStart`, and `Stop`. The schema uses `additionalProperties: false`, which means **no other hook types are valid in the plugin hooks.json file**.

However, Jerry's prior research (`claude-code-best-practices.md`, sourced from official Anthropic documentation) lists additional hook types including `UserPromptSubmit`, `PostToolUseFailure`, `PreCompact`, and others. These additional types appear to be available in the **settings.json hooks configuration** (`.claude/settings.json` or `~/.claude/settings.json`) rather than in the **plugin hooks.json** file.

**This distinction is architecturally significant**: Plugin hooks (`hooks/hooks.json`) are scoped to a plugin and distributed with it. Settings hooks (`.claude/settings.json`) are project-level or user-level. For enforcement purposes, the deployment vector determines who controls the hooks.

### Key Enforcement Capabilities

1. **PreToolUse can BLOCK operations** -- This is the most powerful enforcement mechanism. By returning `{"decision": "block", "reason": "..."}`, the hook can prevent Write, Edit, Bash, and any other tool from executing. Jerry already uses this for security (blocking writes to ~/.ssh, dangerous commands, etc.).

2. **PostToolUse can MODIFY outputs** -- After a tool executes, PostToolUse can redact sensitive data, inject reminders, and log audit trails. Jerry's implementation already redacts Bearer tokens, API keys, and other secrets.

3. **SessionStart provides one-time context injection** -- Via `additionalContext`, the hook can inject structured XML-tagged context into Claude's context window at session start. Jerry uses this for project resolution.

4. **Stop hooks gate subagent completion** -- When a subagent finishes, the Stop hook can evaluate its output and trigger handoff logic. Jerry uses this for agent orchestration.

### Main Limitations

1. **Hooks are stateless** -- Each invocation is a fresh process. State must be persisted to the filesystem.
2. **Timeout constraints** -- Hooks must complete within their configured timeout (1000-300000ms). Complex validation may exceed this.
3. **The agent can work around hooks** -- Hooks gate tool usage, not thought processes. An agent can restructure its approach to avoid triggering hook matchers.
4. **Latency impact** -- Each hook adds overhead. PreToolUse on Write|Edit adds ~100-5000ms per file operation.
5. **No UserPromptSubmit in plugin hooks schema** -- The most powerful enforcement vector may require settings.json configuration rather than plugin hooks.json.

---

## L1: Technical Analysis

### 1. Hook System Architecture

#### 1.1 Two Configuration Surfaces

Claude Code has **two distinct hook configuration surfaces**:

**Surface 1: Plugin Hooks (`hooks/hooks.json`)**

This is the hooks configuration distributed with a Claude Code plugin. Jerry uses this surface.

Schema (from `/Users/adam.nowak/workspace/GitHub/geekatron/jerry/schemas/hooks.schema.json`):
- Allowed hook types: `PreToolUse`, `PostToolUse`, `SessionStart`, `Stop`
- `additionalProperties: false` -- no other hook types allowed
- Each hook type contains an array of matchers with associated hook definitions
- Hook definitions can be `"command"` (shell command) or `"prompt"` (text prompt)

**Surface 2: Settings Hooks (`.claude/settings.json`)**

This is the project-level or user-level settings file. Based on the best-practices research (sourced from official Anthropic docs), this surface supports additional hook types:

```
SessionStart, SessionEnd, UserPromptSubmit, PreToolUse, PostToolUse,
PostToolUseFailure, Stop, PreCompact, SubagentStart, SubagentStop
```

The settings.json hooks may use a different configuration format. The research document references matcher expressions like:
```json
"matcher": "tool == \"Bash\" && tool_input.command matches \"git push\""
```

This expression-based matching is more sophisticated than the simple regex matchers in the plugin hooks schema.

**Architectural Implication**: For enforcement purposes, Jerry should consider using BOTH surfaces:
- Plugin hooks for security guardrails that ship with the plugin
- Settings hooks for UserPromptSubmit and other enforcement types not available in plugin hooks

#### 1.2 Hook Execution Model

Based on analysis of Jerry's implementations:

**Input**: Hooks receive JSON via stdin:
```json
// PreToolUse input
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.py",
    "content": "file contents..."
  }
}

// PostToolUse input
{
  "tool_name": "Write",
  "tool_input": { ... },
  "tool_output": "File written successfully"
}

// Stop (subagent) input
{
  "agent_name": "orchestrator",
  "output": "agent's full output text..."
}

// SessionStart input
// (session metadata - varies)
```

**Output**: Hooks write JSON to stdout:
```json
// PreToolUse output (blocking)
{"decision": "block", "reason": "Writing to sensitive file"}

// PreToolUse output (approval)
{"decision": "approve"}

// PreToolUse output (ask user)
{"decision": "ask", "reason": "Confirm this operation"}

// SessionStart output
{
  "systemMessage": "Text shown in terminal",
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Text added to Claude's context"
  }
}
```

**Exit Codes**:
| Exit Code | Meaning |
|-----------|---------|
| 0 | Hook executed successfully (decision in stdout) |
| 1 | Hook-specific non-fatal condition (e.g., no handoff needed) |
| 2 | Hook execution error |

**Timeout Behavior**: If a hook exceeds its configured timeout, Claude Code kills the process and proceeds as if the hook was not present (fail-open behavior). This is by design -- hooks should never block the user indefinitely.

**Execution Environment**: Hooks run as child processes via shell execution. They inherit the environment variables of the Claude Code process, plus:
- `CLAUDE_PLUGIN_ROOT` -- Path to the plugin root directory
- `CLAUDE_PROJECT_DIR` -- Path to the user's project directory

#### 1.3 Matcher Patterns

**Plugin hooks** use simple regex-like patterns:
- `"*"` -- Match everything
- `"Write|Edit"` -- Match Write or Edit tools
- `"subagent:*"` -- Match all subagent stop events

**Settings hooks** (based on research) may use expression-based matchers:
- `"tool == \"Bash\" && tool_input.command matches \"git push\""` -- Match specific Bash commands
- `"tool == \"Edit\" && tool_input.file_path matches \"\\.(ts|tsx|js|jsx)$\""` -- Match file patterns

### 2. Per-Hook-Type Deep Analysis

#### 2.1 PreToolUse Hooks

**Trigger**: Before ANY tool call that matches the matcher pattern.

**Jerry's Current Implementation** (`/Users/adam.nowak/workspace/GitHub/geekatron/jerry/scripts/pre_tool_use.py`):

The implementation has a two-phase validation architecture:

**Phase 1: Rule-Based Security Checks**
- Blocks writes to sensitive paths (`~/.ssh`, `~/.gnupg`, `~/.aws`, `/etc`, `/var`, `/usr`, `/bin`, `/sbin`)
- Blocks writes to sensitive file patterns (`.env`, `credentials.json`, `*.pem`, `*.key`, `id_rsa`)
- Blocks dangerous bash commands (`rm -rf /`, `chmod 777`, `curl | bash`, `eval`, `dd if=`)
- Blocks `cd` commands (enforces absolute path usage)
- Blocks force pushes to `main`/`master`
- Warns on `git reset --hard` (allows but logs)
- Warns on piping to shell (`| sh`, `| bash`)

**Phase 2: Pattern Library Validation**
- Loads `scripts/patterns/patterns.yaml` (or `.json` fallback)
- Validates against configurable pattern groups:
  - **PII Detection**: SSN, email, phone, credit card, IP addresses
  - **Secrets Detection**: OpenAI keys, Anthropic keys, GitHub PATs, AWS keys, Slack tokens, passwords, private keys, JWTs
  - **Format Validation**: Project ID format, entry ID format, work item ID format
- Configurable modes per pattern: `block`, `warn`, `ask`
- 100ms timeout per validation (AC-015-002)
- Default mode: `warn` (AC-015-003)

**Enforcement Capabilities for Quality Framework**:

| Enforcement | How | Feasibility |
|-------------|-----|-------------|
| File naming conventions | Check `tool_input.file_path` against naming patterns | HIGH |
| Content quality (docstrings, type hints) | Parse `tool_input.content` for required elements | MEDIUM (parsing within timeout) |
| Architecture boundary enforcement | Check import patterns in `tool_input.content` | MEDIUM |
| Test-first enforcement | Check if test file exists before allowing src/ writes | HIGH |
| Plan-first enforcement | Check if PLAN.md exists before allowing implementation | HIGH |
| Prevent writes without quality review | Check for review artifact alongside implementation | HIGH |

**What PreToolUse CANNOT Enforce**:
- The quality of the content being written (beyond pattern matching)
- Whether the agent followed the correct thought process
- Whether the agent invoked the correct skill
- The order of operations (only gates individual tool calls)
- Anything that does not involve a tool call

**Reliability Assessment**:
- **Fires reliably**: YES -- PreToolUse fires for every matching tool call
- **Edge cases**: Tool names are exact matches (Write, Edit, Bash, etc.) -- no ambiguity
- **Bypass risk**: LOW for tool-gating (agent cannot avoid the hook); MEDIUM for content checks (agent could restructure content to avoid patterns)

#### 2.2 PostToolUse Hooks

**Trigger**: After a tool completes execution, before the result is returned to Claude.

**Jerry's Current Implementation** (`/Users/adam.nowak/workspace/GitHub/geekatron/jerry/scripts/post_tool_use.py`):

Two-phase output filtering architecture:

**Phase 1: Pattern-Based Redaction**
- Uses the same pattern library as PreToolUse
- Applies output patterns: `no_secrets_in_output`, `executable_code_warning`
- Redacts matched text with configurable replacement strings
- Sorts matches by position (reverse) for correct replacement

**Phase 2: Inline Safety Net Redaction**
- Hardcoded regex patterns as fallback:
  - Bearer tokens: `Bearer\s+[A-Za-z0-9-_.]+`
  - OpenAI-format API keys: `sk-[a-zA-Z0-9]{20,}`
  - GitHub PATs: `ghp_[a-zA-Z0-9]{36}`
  - AWS Access Keys: `AKIA[0-9A-Z]{16}`

**Enforcement Capabilities for Quality Framework**:

| Enforcement | How | Feasibility |
|-------------|-----|-------------|
| Output redaction (secrets) | Pattern matching on tool output | HIGH (already implemented) |
| Quality reminders after writes | Inject `additionalContext` after file writes | MEDIUM (needs format verification) |
| Audit trail logging | Log all Write/Edit operations to filesystem | HIGH |
| Content validation post-write | Validate written content meets standards | MEDIUM |
| Compliance tracking | Update enforcement state file after each tool use | HIGH |

**What PostToolUse CANNOT Enforce**:
- Prevention -- the action has already happened
- Rollback -- PostToolUse cannot undo tool actions
- Thought process -- same as PreToolUse
- Future behavior -- injected reminders may be ignored

**Key Question: Can PostToolUse Inject Context?**

The current implementation returns `{"output": "..."}` to modify the tool's output. Based on the SessionStart hook contract, hooks can also return:
```json
{
  "hookSpecificOutput": {
    "additionalContext": "enforcement reminder text"
  }
}
```

**This is architecturally important**: If PostToolUse can inject `additionalContext`, it becomes a powerful enforcement vector for injecting quality reminders after every file operation. However, **this needs empirical verification** -- the contract may differ between SessionStart and PostToolUse hooks.

**Reliability Assessment**:
- **Fires reliably**: YES -- PostToolUse fires for every matching tool completion
- **Edge cases**: Tool output may be empty or non-string (handled in Jerry's implementation)
- **Bypass risk**: LOW for redaction; MEDIUM-HIGH for injected reminders (agent may ignore)

#### 2.3 SessionStart Hooks

**Trigger**: Once when a Claude Code session begins.

**Jerry's Current Implementation** (`/Users/adam.nowak/workspace/GitHub/geekatron/jerry/scripts/session_start_hook.py`):

Comprehensive session initialization:

1. **UV Environment Bootstrap**: Finds UV, syncs dependencies, changes to plugin directory
2. **CLI Invocation**: Calls `jerry --json projects context` to get project state
3. **Pre-commit Hook Check**: Verifies pre-commit hooks are installed (only when working inside Jerry repo)
4. **Output Formatting**: Transforms CLI JSON into dual-format output:
   - `systemMessage` -- Shown to user in terminal at session start
   - `hookSpecificOutput.additionalContext` -- Added to Claude's context window

**Three output modes based on project state**:

| State | systemMessage | additionalContext Tags |
|-------|---------------|----------------------|
| Active project | "Jerry Framework: Project PROJ-XXX active" | `<project-context>` with ProjectActive, ProjectPath, ValidationMessage |
| Invalid project | "Jerry Framework: ERROR - PROJ-XXX invalid" | `<project-error>` with InvalidProject, Error, AvailableProjects |
| No project set | "Jerry Framework: No project set (N available)" | `<project-required>` with ProjectRequired, AvailableProjects, NextProjectNumber |

**Contract Compliance** (from `tests/contract/test_hook_output_contract.py`):
- T-020: Output is valid JSON
- T-021: Has `hookSpecificOutput` object
- T-022: `hookEventName` is "SessionStart"
- T-023: `additionalContext` is a string
- T-024: Contains project XML tags
- T-025: Has `systemMessage` field (AC-002, AC-003)
- T-026: Has BOTH `systemMessage` AND `additionalContext`
- Error handling: Outputs valid JSON even on errors

**Enforcement Capabilities for Quality Framework**:

| Enforcement | How | Feasibility |
|-------------|-----|-------------|
| Quality context injection | Add `<quality-enforcement>` tags to additionalContext | HIGH |
| Prerequisite verification | Check for required artifacts before allowing session | HIGH |
| Task-type classification | Analyze project state to inject task-specific enforcement | MEDIUM |
| Compliance dashboard | Inject current compliance status summary | HIGH |

**Limitations**:
- **Executes only ONCE** -- no ongoing enforcement during the session
- Context may drift to the "middle" of the window as conversation grows (reduced attention)
- Cannot react to specific user prompts or task changes mid-session
- 10000ms timeout (generous but finite)

#### 2.4 Stop Hooks

**Trigger**: When a subagent completes its task. Matcher `subagent:*` matches all subagent completions.

**Jerry's Current Implementation** (`/Users/adam.nowak/workspace/GitHub/geekatron/jerry/scripts/subagent_stop.py`):

Agent handoff orchestration system:

1. **Signal Parsing**: Parses agent output for structured signals:
   - `##HANDOFF:condition##` -- Triggers handoff routing
   - `##WORKITEM:WORK-xxx##` -- Links to work items
   - `##STATUS:status##` -- Updates work item status

2. **Handoff Routing**: Rule-based routing between agents:
   - `orchestrator` -> `qa-engineer` (on implementation_complete)
   - `qa-engineer` -> `security-auditor` (on security_concern)
   - `qa-engineer` -> `orchestrator` (on tests_passing)
   - `security-auditor` -> `orchestrator` (on review_complete)

3. **Status Transitions**: Maps handoff conditions to work item status:
   - `implementation_complete` -> `IN_REVIEW`
   - `tests_passing` -> `TESTING_COMPLETE`
   - `security_concern` -> `SECURITY_REVIEW`
   - `review_complete` -> `READY_FOR_MERGE`

4. **Audit Logging**: Writes handoff logs to `docs/experience/handoff_YYYYMMDD_HHMMSS.md`

**Enforcement Capabilities for Quality Framework**:

| Enforcement | How | Feasibility |
|-------------|-----|-------------|
| Quality gate at handoff | Verify quality artifacts exist before allowing handoff | HIGH |
| Block completion without review | Require `##HANDOFF:review_complete##` signal | HIGH |
| Quality score threshold | Verify quality score >= 0.92 before handoff | MEDIUM (needs file parsing) |
| Mandatory artifact checklist | Check for required files before completing | HIGH |

**Limitations**:
- Only applies to subagent completion (Jerry limits to one subagent level per P-003)
- Signal-based: Relies on agents including `##HANDOFF:##` signals in their output
- Convention over enforcement: Agents must follow the signal protocol
- Does not apply to the main context agent stopping

### 3. Hook Implementation Patterns

#### 3.1 Language and Runtime

All Jerry hooks are implemented in Python 3.11+ and executed via UV:

```
uv run --directory ${CLAUDE_PLUGIN_ROOT} ${CLAUDE_PLUGIN_ROOT}/scripts/hook_name.py
```

**Alternative implementation languages** (from best-practices research):
- Bash scripts (simplest, no dependency management)
- Node.js (if the project already uses Node)
- Any language that can read stdin JSON and write stdout JSON

**Jerry's choice of Python is architecturally sound because**:
- Matches the framework's primary language
- Can import the pattern library (`scripts/patterns/loader.py`)
- UV manages dependencies consistently
- Type hints and structure match coding standards

#### 3.2 Pattern Library Architecture

Jerry has a sophisticated pattern library (`scripts/patterns/`) that both PreToolUse and PostToolUse hooks share:

```
scripts/patterns/
  __init__.py           # Package exports
  loader.py             # PatternLibrary class, YAML/JSON loading, validation engine
  patterns.yaml         # Pattern definitions (PII, secrets, format validation)
  patterns.json         # JSON fallback for environments without PyYAML
  schema.json           # Schema for pattern definitions
```

**Key design decisions**:
- **Fail-open**: If patterns cannot be loaded, hooks approve by default
- **Timeout-aware**: Validation stops after 100ms regardless of remaining patterns
- **Dual-format**: YAML for human authoring, JSON fallback for environments without PyYAML
- **Extensible**: New pattern groups can be added to `patterns.yaml` without code changes

#### 3.3 Error Handling Philosophy

All Jerry hooks follow a **fail-open** philosophy:
- On parse error: Block (security) but approve (quality) -- depends on severity
- On timeout: Approve (fail-open)
- On import error: Skip pattern validation, fall back to rule-based checks
- On unexpected error: Log to stderr, return valid JSON

This is aligned with the principle that **hooks should never prevent the user from working**. Quality enforcement should be persistent but not obstructive.

### 4. Platform Compatibility Analysis

#### 4.1 Current Platform Status

| Platform | UV Available | Shell Differences | Path Handling | Status |
|----------|-------------|-------------------|---------------|--------|
| macOS | Yes (Homebrew, cargo) | `/bin/bash`, `/bin/zsh` | POSIX paths | TESTED |
| Linux | Yes (cargo, pipx) | `/bin/bash`, `/bin/sh` | POSIX paths | EXPECTED TO WORK |
| Windows | Yes (cargo, scoop) | `cmd.exe`, PowerShell | `\` backslash paths | PARTIALLY TESTED |

#### 4.2 Known Cross-Platform Issues

From the git history (commit `49a708e`): "fix: use splitlines() for Windows CRLF compatibility in VTT validator"
From the git history (commit `f89f7ff`): "fix: replace fcntl with filelock for Windows compatibility"

These commits indicate ongoing Windows compatibility work. Hook scripts should:
- Use `splitlines()` instead of `split("\n")` for line parsing
- Use `pathlib.Path` for all path operations
- Avoid Unix-specific APIs (`fcntl`, etc.)
- Handle both `/` and `\` in file paths from tool input

#### 4.3 Environment Variable Handling

Hooks rely on environment variables:
- `CLAUDE_PLUGIN_ROOT` -- Set by Claude Code, always available
- `CLAUDE_PROJECT_DIR` -- Set by Claude Code, always available
- `JERRY_PROJECT` -- Set by user, may not be present
- `PATH` -- Inherited from Claude Code's shell process

**Windows concern**: Shell command syntax in `hooks.json` uses `&&` which may not work in all Windows shells. UV execution should be platform-independent, but the command string itself needs testing.

### 5. Existing Hook Examples and Community Patterns

#### 5.1 Claude Code Hook SDK (Community)

Context7 identified a TypeScript SDK for Claude Code hooks:
- **Library**: `/mizunashi-mana/claude-code-hook-sdk`
- **Benchmark Score**: 85.4 (highest among hook-related libraries)
- **Description**: TypeScript SDK with type safety, dependency injection, and testing support
- **Relevance**: Demonstrates that the community is building hook tooling, confirming hooks as a viable enforcement vector

#### 5.2 Claude Code Prompt Improver (Community)

Context7 identified a hook-based prompt improver:
- **Library**: `/severity1/claude-code-prompt-improver`
- **Benchmark Score**: 47
- **Description**: Evaluates prompt clarity, researches context, asks clarifying questions
- **Relevance**: Demonstrates UserPromptSubmit-like behavior -- intercepting prompts and enriching them, which is exactly the enforcement pattern proposed for quality framework compliance

#### 5.3 GitButler Hook Patterns

From the best-practices research (cited: `blog.gitbutler.com`):
- Pre-push review hooks that pause before git push
- Auto-formatting hooks that run Prettier after Edit
- These demonstrate real-world adoption of hook-based enforcement in production codebases

### 6. Security Review of Hook Mechanism

#### 6.1 Hook Review Requirement

From the best-practices research: "Direct edits to hooks in settings files don't take effect immediately. Claude Code requires review in the `/hooks` menu for changes to apply -- this prevents malicious hook modifications."

This is an important security feature: hooks cannot be silently installed or modified by the agent itself. The user must explicitly approve hook changes.

**Implication for enforcement**: Hooks are a **trusted** enforcement mechanism because:
1. They cannot be modified by the agent
2. They run as external processes (not within the LLM context)
3. They receive structured input and produce structured output
4. The user has approved their installation

#### 6.2 Bypass Risk Assessment

| Bypass Vector | Risk | Mitigation |
|---------------|------|------------|
| Agent avoids triggering hook matcher | MEDIUM | Use broad matchers (`*`, `Write\|Edit`) |
| Agent restructures content to avoid patterns | MEDIUM | Defense-in-depth with multiple enforcement vectors |
| User bypasses with `--no-verify` (git) | LOW | Not applicable to Claude Code hooks (only git hooks) |
| Agent uses alternative tool to achieve same effect | LOW | Hooks cover all tool types (Write, Edit, Bash) |
| Hook timeout exceeded, fails open | LOW | Keep hook execution fast (<100ms for validation) |
| Hook process crashes | LOW | Fail-open design ensures continuity |

---

## L2: Architectural Implications

### 1. Hooks as Part of Defense-in-Depth Strategy

Hooks are one of six enforcement vectors identified in the broader research (`research-enforcement-vectors.md`). They fit into a layered enforcement architecture:

```
Layer 0: CLAUDE.md + .claude/rules/  (always present, declarative)
    |
Layer 1: SessionStart hook           (one-time context injection)
    |
Layer 2: UserPromptSubmit hook       (persistent enforcement on every prompt)
    |
Layer 3: PreToolUse hook             (tool-level gating, can BLOCK)
    |
Layer 4: PostToolUse hook            (reactive validation, audit logging)
    |
Layer 5: Stop hook                   (handoff quality gates)
    |
Layer 6: Pre-commit hooks + CI       (last line of defense, catch-all)
```

**Each layer compensates for the weaknesses of the layers above it.**

### 2. Recommended Hook Prioritization for Quality Enforcement

Based on this research, the hooks should be prioritized for quality enforcement implementation:

| Priority | Hook | Action | Rationale |
|----------|------|--------|-----------|
| **P1 (Critical)** | PreToolUse | Add quality gates for Write/Edit of src/ files | Can BLOCK non-compliant writes; highest enforcement power |
| **P2 (High)** | SessionStart | Inject `<quality-enforcement>` XML tags | Low effort, immediate context improvement |
| **P3 (High)** | UserPromptSubmit | Inject task-specific enforcement context | Most powerful persistent vector, but needs schema investigation |
| **P4 (Medium)** | PostToolUse | Add audit logging and compliance tracking | Enables stateful enforcement via filesystem |
| **P5 (Low)** | Stop | Add quality gates at handoff boundaries | Limited scope (subagent only per P-003) |

### 3. Critical Architecture Decision: Plugin Hooks vs. Settings Hooks

The most important architectural decision for FEAT-005 is:

**Should enforcement hooks be deployed via plugin `hooks/hooks.json` or via `.claude/settings.json`?**

| Factor | Plugin Hooks | Settings Hooks |
|--------|-------------|---------------|
| Available hook types | 4 (PreToolUse, PostToolUse, SessionStart, Stop) | 10+ (includes UserPromptSubmit) |
| Distribution | Ships with plugin | Requires project-level configuration |
| User approval | Required at plugin install | Required at settings change |
| Matcher syntax | Simple regex | Expression-based (more powerful) |
| Version control | In plugin repo | In project `.claude/settings.json` |
| User override | Cannot override plugin hooks | Can override with `settings.local.json` |

**Recommendation**: Use **both** surfaces:
- **Plugin hooks** for security guardrails (current PreToolUse security checks, PostToolUse redaction)
- **Settings hooks** for quality enforcement (UserPromptSubmit context injection, enhanced PreToolUse quality gates)

This separation keeps security enforcement non-overridable (plugin-level) while allowing quality enforcement to be tuned per-project (settings-level).

### 4. Stateful Enforcement Architecture

Since hooks are stateless processes, enforcement state must be persisted to the filesystem:

```
.jerry/enforcement/
  session-state.json       # Current session compliance state
  violations.log           # Accumulated violations
  quality-scores/          # Persisted quality score files
  reviews/                 # Persisted review artifacts
  audit-trail/             # All tool use logged by PostToolUse
```

**Flow**:
1. **SessionStart** reads `session-state.json`, injects compliance dashboard into context
2. **PreToolUse** reads `session-state.json`, enforces prerequisites before allowing writes
3. **PostToolUse** writes to `session-state.json` (updates compliance state), writes to `audit-trail/`
4. **UserPromptSubmit** reads `session-state.json`, injects task-specific enforcement based on current state

This creates a **feedback loop** where enforcement adapts to the agent's behavior during the session.

### 5. Performance Budget

Each hook adds latency to the user experience. The total hook budget should be:

| Hook | Target Latency | Current | Acceptable Range |
|------|---------------|---------|------------------|
| SessionStart | 5000ms | ~3000ms (uv sync + CLI) | 2000-10000ms |
| UserPromptSubmit | 100ms | N/A | 50-200ms |
| PreToolUse | 100ms | ~50ms (rule-based), ~100ms (patterns) | 50-500ms |
| PostToolUse | 100ms | ~50ms (redaction) | 50-300ms |
| Stop | 100ms | ~50ms | 50-500ms |

**Total per-tool-call overhead**: ~200-800ms (PreToolUse + PostToolUse)
**Per-prompt overhead**: ~100-200ms (UserPromptSubmit, if implemented)

These are acceptable for development workflows where file operations take seconds anyway.

### 6. Open Questions Requiring Empirical Validation

| # | Question | Why It Matters | How to Validate |
|---|----------|----------------|-----------------|
| 1 | Does UserPromptSubmit work in settings.json hooks? | Critical for persistent enforcement | Add hook to settings.json, test empirically |
| 2 | Can PostToolUse inject `additionalContext`? | Determines if PostToolUse can inject reminders | Test PostToolUse output format empirically |
| 3 | What is the exact input schema for UserPromptSubmit? | Needed for implementation | Test with minimal hook, log stdin |
| 4 | Can settings hooks and plugin hooks coexist? | Determines deployment strategy | Configure both, test for conflicts |
| 5 | Do settings hooks require `/hooks` menu review? | Determines installation friction | Test settings change without review |
| 6 | What matcher syntax does settings hooks use? | Determines matching capabilities | Test expression-based matchers |

---

## Methodology

### Research Sources

| Source Type | Source | Confidence |
|-------------|--------|------------|
| Jerry codebase (direct analysis) | `hooks/hooks.json`, `scripts/pre_tool_use.py`, `scripts/post_tool_use.py`, `scripts/subagent_stop.py`, `scripts/session_start_hook.py`, `schemas/hooks.schema.json`, `scripts/patterns/`, `scripts/tests/test_hooks.py`, `tests/contract/test_hook_output_contract.py`, `.claude/settings.json`, `.claude/settings.local.json` | **HIGH** |
| Prior Jerry research | `claude-code-best-practices.md` (EN-102/TASK-001), `research-enforcement-vectors.md` (EN-401-R-001) | **HIGH** (codebase analysis), **MEDIUM-HIGH** (external refs from training data) |
| Context7 library resolution | `/anthropics/claude-code` (780 snippets, High reputation, Score 71), `/mizunashi-mana/claude-code-hook-sdk` (80 snippets, Score 85.4), `/severity1/claude-code-prompt-improver` (227 snippets, Score 47) | **MEDIUM** (library metadata only -- query-docs was denied) |
| Jerry hooks schema | `schemas/hooks.schema.json` (authoritative for plugin hooks) | **HIGH** |

### Tool Access Limitations

The following tools were **denied** during this research session:
- `WebSearch` -- Could not search for current Claude Code documentation
- `WebFetch` -- Could not fetch Anthropic docs pages directly
- `mcp__context7__query-docs` -- Could not query Context7 documentation content (only library resolution worked via the non-plugin variant)
- `mcp__plugin_context7_context7__resolve-library-id` -- Plugin variant was also denied

**Impact**: All external documentation references are derived from:
1. Prior Jerry research that had already fetched this content (EN-102/TASK-001)
2. Context7 library metadata (names, descriptions, scores) without full documentation content
3. Training data knowledge (cutoff May 2025)
4. Citations embedded in Jerry's codebase (URLs in docstrings and comments)

### Confidence Assessment

| Finding | Confidence | Basis |
|---------|------------|-------|
| Four hook types in plugin hooks schema | **HIGH** | Direct schema analysis with `additionalProperties: false` |
| PreToolUse can block tool calls | **HIGH** | Implemented and tested in Jerry codebase |
| PostToolUse can modify output | **HIGH** | Implemented and tested in Jerry codebase |
| SessionStart injects context | **HIGH** | Implemented with contract tests |
| Stop hooks gate subagent completion | **HIGH** | Implemented in Jerry codebase |
| UserPromptSubmit exists in settings hooks | **MEDIUM-HIGH** | Referenced in prior research with official doc citations |
| UserPromptSubmit NOT in plugin hooks | **HIGH** | Schema explicitly excludes it |
| Additional hook types (PreCompact, etc.) exist | **MEDIUM** | Referenced in prior research, not verified against current docs |
| Settings hooks use expression-based matchers | **MEDIUM** | Referenced in prior research examples, not verified |
| Hooks are fail-open by design | **HIGH** | Consistent pattern across all Jerry implementations |

---

## References

### Jerry Codebase (Primary)

| # | File | Purpose in Research |
|---|------|-------------------|
| 1 | `/Users/adam.nowak/workspace/GitHub/geekatron/jerry/hooks/hooks.json` | Current hook configuration (plugin surface) |
| 2 | `/Users/adam.nowak/workspace/GitHub/geekatron/jerry/schemas/hooks.schema.json` | Authoritative schema for plugin hooks |
| 3 | `/Users/adam.nowak/workspace/GitHub/geekatron/jerry/scripts/pre_tool_use.py` | PreToolUse implementation |
| 4 | `/Users/adam.nowak/workspace/GitHub/geekatron/jerry/scripts/post_tool_use.py` | PostToolUse implementation |
| 5 | `/Users/adam.nowak/workspace/GitHub/geekatron/jerry/scripts/subagent_stop.py` | Stop hook implementation |
| 6 | `/Users/adam.nowak/workspace/GitHub/geekatron/jerry/scripts/session_start_hook.py` | SessionStart implementation |
| 7 | `/Users/adam.nowak/workspace/GitHub/geekatron/jerry/scripts/patterns/loader.py` | Pattern library engine |
| 8 | `/Users/adam.nowak/workspace/GitHub/geekatron/jerry/scripts/patterns/patterns.yaml` | Pattern definitions |
| 9 | `/Users/adam.nowak/workspace/GitHub/geekatron/jerry/scripts/tests/test_hooks.py` | Hook BDD tests |
| 10 | `/Users/adam.nowak/workspace/GitHub/geekatron/jerry/tests/contract/test_hook_output_contract.py` | SessionStart contract tests |
| 11 | `/Users/adam.nowak/workspace/GitHub/geekatron/jerry/.claude/settings.json` | Claude Code project settings |
| 12 | `/Users/adam.nowak/workspace/GitHub/geekatron/jerry/.claude/settings.local.json` | Local permission overrides |

### Jerry Prior Research (Secondary)

| # | File | Used For |
|---|------|----------|
| 13 | `projects/PROJ-001-oss-release/work/.../EN-102-.../claude-code-best-practices.md` | Hook types enumeration, settings architecture, community patterns |
| 14 | `projects/PROJ-001-oss-release/work/.../FEAT-005-.../research-enforcement-vectors.md` | Broader enforcement vector analysis |
| 15 | `projects/PROJ-001-oss-release/work/.../EN-102-.../TASK-001-hook-system-research.md` | Prior hook system research task |

### External Documentation (Referenced)

| # | Source | URL | Found Via |
|---|--------|-----|-----------|
| 16 | Claude Code Hooks Reference | https://docs.anthropic.com/en/docs/claude-code/hooks | Pre-tool-use.py docstring |
| 17 | Claude Code Hooks (alternative URL) | https://code.claude.com/docs/en/hooks | Best-practices research |
| 18 | Claude Code Overview | https://code.claude.com/docs/en/overview | Best-practices research |
| 19 | Claude Code Best Practices (Anthropic) | https://www.anthropic.com/engineering/claude-code-best-practices | Best-practices research |
| 20 | GitButler - Claude Code Hooks | https://blog.gitbutler.com/automate-your-ai-workflows-with-claude-code-hooks | Best-practices research |
| 21 | Everything Claude Code (GitHub) | https://github.com/affaan-m/everything-claude-code | Best-practices research |
| 22 | Claude Code Hook SDK | Context7: `/mizunashi-mana/claude-code-hook-sdk` | Context7 library resolution |
| 23 | Claude Code Prompt Improver | Context7: `/severity1/claude-code-prompt-improver` | Context7 library resolution |
| 24 | Hook Advanced JSON format | https://code.claude.com/docs/en/hooks#advanced:-json-output | Contract test docstring |

---

## Disclaimer

1. **Tool access limitations**: WebSearch, WebFetch, and Context7 query-docs were all denied during this research session. External documentation references rely on prior Jerry research (which had fetched this content) and training data (cutoff May 2025). Hook API details may have changed after May 2025.

2. **UserPromptSubmit uncertainty**: The distinction between plugin hooks and settings hooks is architecturally significant but incompletely verified. The claim that UserPromptSubmit is available in settings hooks but not plugin hooks is based on schema analysis and prior research citations, not direct empirical testing. **Empirical validation is required before implementation (see Open Questions #1).**

3. **PostToolUse additionalContext capability**: Whether PostToolUse hooks can inject `additionalContext` (like SessionStart hooks) is unverified. **Empirical validation is required (see Open Questions #2).**

4. **Settings hooks matcher syntax**: The expression-based matcher syntax referenced in prior research has not been verified against current Claude Code documentation. **Empirical validation is required (see Open Questions #6).**

5. **This document has NOT been through adversarial review**: Per EPIC-002's quality requirements, this research should undergo creator-critic-revision review (TASK-008 through TASK-011 in EN-401's task list) before implementation decisions are made.

---

*Document Version: 1.0.0*
*Classification: Research Artifact*
*Author: ps-researcher (Claude Opus 4.6)*
*Constitutional Compliance: P-001 (Truth), P-002 (Persistence), P-004 (Provenance), P-022 (No Deception)*
*Word Count: ~4,500 words*
