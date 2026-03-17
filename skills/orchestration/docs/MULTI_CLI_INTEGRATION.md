---
title: Multi-CLI Parallel Execution Integration
version: "1.4.0"
skill: orchestration
pattern: consensus-panel
---

# Multi-CLI Parallel Execution Integration

> **Version:** 1.4.0
> **Skill:** orchestration
> **Purpose:** Reference guide for invoking Gemini CLI and Codex CLI as parallel peer processes during orchestrated workflows.
> **Pattern:** Consensus Panel (Pattern 6 in PATTERNS.md)

---

## Overview

The Consensus Panel pattern invokes **three independent AI models** (Claude, Codex, Gemini) as parallel workers via `Bash`. Because these are external subprocesses — not Jerry sub-agents — they are **P-003 compliant**: they do not increase agent nesting depth. The orchestrator launches all three, waits for all three to complete, then reads their file-based outputs.

Each model is invoked via a **transport-agnostic resolution chain**: CLI binary → API endpoint → Jerry sub-agent fallback. This ensures the pattern works in any environment.

```
Orchestrator (main context)
    │
    ├──► Resolve transport for each model (CLI | API | sub-agent)
    ├──► Run pre-flight checks (auth, availability)
    ├──► Gate: confirm panel composition with user if degraded
    │
    ├──► Launch claude  worker (background) &
    ├──► Launch codex   worker (background) &
    ├──► Launch gemini  worker (background) &
    │
    └──► wait with timeout  ← captures each PID's exit code individually
```

This is **file-mediated integration**: each worker writes its output to a dedicated file, and the orchestrator reads all three files after the wait.

**Implementation:** `skills/orchestration/templates/consensus-panel.sh` contains all bash functions (`launch_worker`, `wait_with_timeout`, `verify_outputs`, API wrappers). Copy-adapt from there rather than writing from scratch.

---

## Phase 0: Pre-Flight Resolution

Run the full resolution chain **before** launching any parallel work. Never skip this phase.

### Step 0a: Platform Detection

```bash
# Git Bash (MSYS2) on Windows DOES support bash & background jobs (T-001).
# Only cmd.exe / PowerShell without WSL require sequential fallback.
if [ -n "$WSL_DISTRO_NAME" ] || uname -s | grep -qi linux; then
  PLATFORM="linux"
  PARALLEL_SUPPORTED=true
elif echo "$OSTYPE" | grep -qi msys || echo "$OSTYPE" | grep -qi mingw \
  || uname -s | grep -qi mingw || uname -s | grep -qi cygwin; then
  PLATFORM="windows-gitbash"
  PARALLEL_SUPPORTED=true
else
  PLATFORM="unknown"
  PARALLEL_SUPPORTED=true  # assume linux-like
fi
echo "Platform: $PLATFORM | Parallel supported: $PARALLEL_SUPPORTED"
```

If `PARALLEL_SUPPORTED=false` (Windows native cmd/PowerShell without Git Bash or WSL), warn the user and offer sequential execution or WSL/Git Bash.

### Step 0b: CLI Detection

```bash
CLAUDE_TRANSPORT=""
CODEX_TRANSPORT=""
GEMINI_TRANSPORT=""

command -v claude  >/dev/null 2>&1 && CLAUDE_TRANSPORT="cli"
command -v codex   >/dev/null 2>&1 && CODEX_TRANSPORT="cli"
command -v gemini  >/dev/null 2>&1 && GEMINI_TRANSPORT="cli"

# T-002: nested claude CLI hangs inside a running Claude Code session.
# Downgrade to "" here; API fallback (Step 0d) takes over if key is set.
if [ "$CLAUDE_TRANSPORT" = "cli" ] && [ -n "$CLAUDECODE" ]; then
  echo "INFO: Running inside Claude Code session (CLAUDECODE=1) — nested claude CLI blocked (T-002)"
  CLAUDE_TRANSPORT=""
fi
```

### Step 0c: Auth Validation

```bash
# Claude: accept if API key set OR credential files exist.
# Do NOT call `claude auth status` — it may hang in partial session state.
if [ "$CLAUDE_TRANSPORT" = "cli" ]; then
  CLAUDE_AUTH_DIR="${HOME}/.claude"
  if [ -z "$ANTHROPIC_API_KEY" ] && \
     ! ls "${CLAUDE_AUTH_DIR}"/.credentials* >/dev/null 2>&1 && \
     ! ls "${CLAUDE_AUTH_DIR}"/auth* >/dev/null 2>&1; then
    echo "WARNING: claude CLI found but no auth detected"
    CLAUDE_TRANSPORT="auth-warning"
  fi
fi

# Codex: OPENAI_API_KEY not required if codex login stored credentials exist.
if [ "$CODEX_TRANSPORT" = "cli" ]; then
  if [ -z "$OPENAI_API_KEY" ]; then
    echo "INFO: codex CLI found but OPENAI_API_KEY not set — relying on stored credentials"
  fi
fi

# Gemini: T-003 — exits with code 41 if neither API key is set. No stored OAuth fallback.
if [ "$GEMINI_TRANSPORT" = "cli" ]; then
  if [ -z "$GEMINI_API_KEY" ] && [ -z "$GOOGLE_API_KEY" ]; then
    echo "WARNING: gemini CLI found but no API key set — exit code 41 expected (T-003)"
    GEMINI_TRANSPORT="auth-warning"
  fi
fi
```

### Step 0d: API Fallback Resolution

If a CLI is missing or has auth issues, fall back to direct API invocation. This makes the pattern work on CI/CD systems and restricted machines.

```bash
[ "$CLAUDE_TRANSPORT" != "cli" ] && [ -n "$ANTHROPIC_API_KEY" ] && \
  CLAUDE_TRANSPORT="api" && echo "claude: using API transport"

[ "$CODEX_TRANSPORT" != "cli" ] && [ -n "$OPENAI_API_KEY" ] && \
  CODEX_TRANSPORT="api" && echo "codex: using API transport"

{ [ "$GEMINI_TRANSPORT" != "cli" ] && \
  { [ -n "$GEMINI_API_KEY" ] || [ -n "$GOOGLE_API_KEY" ]; }; } && \
  GEMINI_TRANSPORT="api" && echo "gemini: using API transport"
```

API wrapper implementations are in `templates/consensus-panel.sh` (`invoke_claude_api`, `invoke_codex_api`, `invoke_gemini_api`).

### Step 0e: Panel Composition Summary + User Gate

```bash
AVAILABLE=0
[ -n "$CLAUDE_TRANSPORT" ]  && AVAILABLE=$((AVAILABLE + 1))
[ -n "$CODEX_TRANSPORT" ]   && AVAILABLE=$((AVAILABLE + 1))
[ -n "$GEMINI_TRANSPORT" ]  && AVAILABLE=$((AVAILABLE + 1))

echo ""
echo "=== Consensus Panel Pre-Flight Report ==="
echo "  Claude : ${CLAUDE_TRANSPORT:-UNAVAILABLE}"
echo "  Codex  : ${CODEX_TRANSPORT:-UNAVAILABLE}"
echo "  Gemini : ${GEMINI_TRANSPORT:-UNAVAILABLE}"
echo "  Workers available: $AVAILABLE / 3"
echo "========================================="
```

**User gate logic (H-31 compliance):**

| Available | Action |
|-----------|--------|
| 3 of 3 | Proceed automatically — full panel, no gate needed |
| 2 of 3 | **Ask user:** "One model unavailable. Proceed with 2-model panel, or cancel?" |
| 1 of 3 | **Ask user:** "Only 1 model available. Proceed as single-model draft, fall back to Jerry sub-agents, or cancel?" |
| 0 of 3 | **Ask user:** "No external models available. Fall back to Jerry sub-agents, or cancel workflow?" |

Present the pre-flight report as context when asking. Do NOT silently proceed with a degraded panel.

---

## CLI Reference Table

| CLI | Invocation Pattern | Transport |
|-----|--------------------|-----------|
| **Claude** | `claude --dangerously-skip-permissions --model claude-opus-4-6 --thinking-budget high -p "<prompt>"` | CLI |
| **Codex** | `codex exec --full-auto -m gpt-4o "<prompt>"` | CLI (T-004) |
| **Gemini** | `gemini --yolo --model gemini-2.5-pro --prompt "<prompt>"` | CLI |
| **Claude** | `invoke_claude_api prompt_file output_file` | API |
| **Codex** | `invoke_codex_api prompt_file output_file` | API |
| **Gemini** | `invoke_gemini_api prompt_file output_file` | API |

**Model fallbacks:**

| CLI | Primary | Fallback |
|-----|---------|----------|
| Claude | `claude-opus-4-6` | `claude-sonnet-4-6` |
| Codex | `gpt-4o` | — |
| Gemini | `gemini-2.5-pro` | `gemini-1.5-pro` |

> **Security note:** `--dangerously-skip-permissions` and `--yolo` give broad file system access. Always write intent files from the orchestrator itself — never pass user-supplied raw text as a file path. Sanitize `{workflow_id}` and `{phase_id}` before path construction (remove `..`, `/`, special characters).

---

## File Layout

```
orchestration/{workflow_id}/consensus/
├── {phase_id}-intent.md           # Shared seed document (orchestrator writes)
├── {phase_id}-claude-draft.md     # Claude worker output
├── {phase_id}-codex-draft.md      # Codex worker output
├── {phase_id}-gemini-draft.md     # Gemini worker output
├── {phase_id}-claude-critique.md  # Claude critiques Codex+Gemini
├── {phase_id}-codex-critique.md   # Codex critiques Claude+Gemini
├── {phase_id}-gemini-critique.md  # Gemini critiques Claude+Codex
└── {phase_id}-synthesis.md        # orch-synthesizer final output
```

**Path sanitization (required before use):**
```bash
WORKFLOW_ID=$(echo "$WORKFLOW_ID" | tr -cd 'a-zA-Z0-9_-')
PHASE_ID=$(echo "$PHASE_ID"       | tr -cd 'a-zA-Z0-9_-')
CONSENSUS_DIR="orchestration/${WORKFLOW_ID}/consensus"
mkdir -p "$CONSENSUS_DIR"
```

---

## Parallel Launch Pattern

See `templates/consensus-panel.sh` for full implementations. Summary of the key functions:

| Function | Purpose |
|----------|---------|
| `launch_worker <model> <transport> <prompt_file> <output_file>` | Dispatch to CLI or API, background the process, echo PID |
| `wait_with_timeout <pid> <model> <timeout>` | Wait for PID with watchdog kill; return exit code |
| `verify_outputs <phase_label> [label path ...]` | Report missing/empty outputs after a phase |

**Draft phase sketch:**

```bash
TIMEOUT=${CONSENSUS_TIMEOUT:-300}

CLAUDE_PID=$([ -n "$CLAUDE_TRANSPORT" ] && \
  launch_worker claude "$CLAUDE_TRANSPORT" "$CLAUDE_PROMPT" "$CLAUDE_OUT" || echo "")
CODEX_PID=$([ -n "$CODEX_TRANSPORT" ] && \
  launch_worker codex  "$CODEX_TRANSPORT"  "$CODEX_PROMPT"  "$CODEX_OUT"  || echo "")
GEMINI_PID=$([ -n "$GEMINI_TRANSPORT" ] && \
  launch_worker gemini "$GEMINI_TRANSPORT" "$GEMINI_PROMPT" "$GEMINI_OUT" || echo "")

wait_with_timeout "$CLAUDE_PID" "claude" "$TIMEOUT"; CLAUDE_EXIT=$?
wait_with_timeout "$CODEX_PID"  "codex"  "$TIMEOUT"; CODEX_EXIT=$?
wait_with_timeout "$GEMINI_PID" "gemini" "$TIMEOUT"; GEMINI_EXIT=$?

verify_outputs "draft" "claude" "$CLAUDE_OUT" "codex" "$CODEX_OUT" "gemini" "$GEMINI_OUT"
```

**Critique phase:** same pattern, but gate each worker launch on peer draft files existing:
```bash
CLAUDE_CRIT_PID=$([ -f "$CODEX_OUT" ] && [ -f "$GEMINI_OUT" ] && [ -n "$CLAUDE_TRANSPORT" ] && \
  launch_worker claude "$CLAUDE_TRANSPORT" "$CLAUDE_CRIT_PROMPT" "$CLAUDE_CRIT" || echo "")
# ... repeat for codex and gemini, checking their respective peer files
```

---

## Synthesis Handoff

After parallel phases complete, invoke `orch-synthesizer` via the Task tool:

```python
Task(
    description="orch-synthesizer: Synthesize consensus panel outputs",
    subagent_type="orch-synthesizer",
    prompt="""
You are orch-synthesizer. Synthesize outputs from the Consensus Panel.

## Panel Composition
- Claude transport: {claude_transport}  (cli|api|unavailable)
- Codex transport:  {codex_transport}   (cli|api|unavailable)
- Gemini transport: {gemini_transport}  (cli|api|unavailable)

NOTE: If any model shows "unavailable", the synthesis is PARTIAL.
Surface this prominently — do not present a partial panel as full 3-way consensus.

## Inputs (only read files that exist)
- Intent:            {intent_file}
- Claude draft:      {claude_out}      (present: {claude_present})
- Codex draft:       {codex_out}       (present: {codex_present})
- Gemini draft:      {gemini_out}      (present: {gemini_present})
- Claude critique:   {claude_crit}     (present: {claude_crit_present})
- Codex critique:    {codex_crit}      (present: {codex_crit_present})
- Gemini critique:   {gemini_crit}     (present: {gemini_crit_present})

## Task
1. Read ALL available draft and critique files.
2. Extract strongest elements from each draft.
3. Identify CONSENSUS POINTS (all available models agree → high confidence).
4. Identify DIVERGENCE POINTS (models disagree → flag for human review).
5. If panel was partial: include a PANEL GAPS section listing absent models.
6. Write synthesis to: {synthesis_out}

Apply S-014 (LLM-as-Judge) self-scoring after writing.
"""
)
```

---

## Degradation Decision Tree

```
Pre-flight complete
        │
        ▼
 3 workers available? ──YES──► Launch parallel panel (no user gate)
        │
        NO
        ▼
 2 workers available? ──YES──► AskUserQuestion:
        │                       "1 model unavailable: {model}.
        │                        Proceed with 2-model panel?
        │                        Options: [Proceed] [Cancel]"
        │
        NO
        ▼
 1 worker available? ──YES──► AskUserQuestion:
        │                       "Only {model} available.
        │                        Options: [Proceed as single-model draft]
        │                                 [Fall back to Jerry sub-agents]
        │                                 [Cancel]"
        │
        NO
        ▼
 0 workers ──────────────────► AskUserQuestion:
                                "No external models available.
                                 Options: [Fall back to Jerry sub-agents]
                                          [Cancel workflow]"
```

**Jerry sub-agent fallback** (0 external models): invoke `orch-synthesizer` directly with the intent document, or use the Fan-Out pattern (Pattern 3) with Jerry agents instead of external CLIs.

---

## P-003 Compliance Note

External CLI and API processes invoked via `Bash` are **not** Jerry sub-agents. They do not consume Claude context budget and cannot spawn further agents. P-003 applies only to `Task(subagent_type=...)` invocations.

```
P-003 scope:
  MAIN CONTEXT
      └──► Task(subagent_type="orch-synthesizer")  ← ONE level (allowed)
               └──► (no further Task calls)         ← compliant

NOT in P-003 scope (OS processes):
  MAIN CONTEXT
      └──► Bash("claude ...")  ← OS subprocess
      └──► Bash("codex ...")   ← OS subprocess
      └──► Bash("curl ...")    ← API call via OS subprocess
```

---

## ORCHESTRATION.yaml Schema Extension

The `consensus_panel:` block added to ORCHESTRATION.yaml when this pattern is active is defined in `docs/STATE_SCHEMA.md` under **Consensus Panel Extension**.

---

## Real-World Findings Reference

| ID | Summary | Detail |
|----|---------|--------|
| T-001 | Git Bash (MSYS2) on Windows supports `bash &` | Original detection incorrectly set `PARALLEL_SUPPORTED=false` for `msys`/`mingw`. Only cmd.exe/PowerShell require sequential fallback. |
| T-002 | `claude -p` hangs when `CLAUDECODE=1` | Child process inherits env, attempts IPC via `/tmp/claude-*-cwd` sockets, never exits. Detect at pre-flight and downgrade transport before launch. |
| T-003 | `gemini` exits with code 41 without API key | Unlike Claude (stored OAuth) and Codex (`codex login`), Gemini CLI requires `GEMINI_API_KEY` or `GOOGLE_API_KEY` on every invocation. |
| T-004 | Codex v0.115.0+ has no `--yolo` flag | `--full-auto` and `--dangerously-bypass-approvals-and-sandbox` are mutually exclusive. Use `codex exec --full-auto -m gpt-4o` for sandboxed non-interactive execution. |

---

*Document Version: 1.4.0*
*Skill: orchestration*
*Pattern: Consensus Panel*
