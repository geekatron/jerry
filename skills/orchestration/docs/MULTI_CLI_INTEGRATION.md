---
title: Multi-CLI Parallel Execution Integration
version: "1.0.0"
skill: orchestration
pattern: consensus-panel
---

# Multi-CLI Parallel Execution Integration

> **Version:** 1.0.0
> **Skill:** orchestration
> **Purpose:** Reference guide for invoking Gemini CLI and Codex CLI as parallel peer processes during orchestrated workflows.
> **Pattern:** Consensus Panel (Pattern 6 in PATTERNS.md)

---

## Overview

The Consensus Panel pattern invokes **three independent AI CLIs** (Claude, Codex, Gemini) as parallel peer processes via `Bash`. Because these are external subprocesses — not Jerry sub-agents — they are **P-003 compliant**: they do not increase agent nesting depth. The orchestrator launches all three, waits for all three to complete, then reads their file-based outputs.

```
Orchestrator (main context)
    │
    ├──► Bash: claude  --dangerously-skip-permissions ... &  (PEER PROCESS)
    ├──► Bash: codex   --yolo ...                         &  (PEER PROCESS)
    ├──► Bash: gemini  --yolo ...                         &  (PEER PROCESS)
    │
    └──► wait  ← blocks until all three processes exit
```

This is **file-mediated integration**: each CLI writes its output to a dedicated file, and the orchestrator reads all three files after the wait.

---

## CLI Detection (Phase 0)

Before launching, verify which CLIs are available. Run these checks once at workflow start:

```bash
# Detect available CLIs and store for later use
CLAUDE_CLI=""
CODEX_CLI=""
GEMINI_CLI=""

command -v claude  >/dev/null 2>&1 && CLAUDE_CLI="claude"
command -v codex   >/dev/null 2>&1 && CODEX_CLI="codex"
command -v gemini  >/dev/null 2>&1 && GEMINI_CLI="gemini"

echo "Available: claude=${CLAUDE_CLI:-MISSING} codex=${CODEX_CLI:-MISSING} gemini=${GEMINI_CLI:-MISSING}"
```

**Minimum requirement:** At least 2 CLIs must be available for the Consensus Panel to add value over a single-agent approach. With only 1 available, fall back to Pattern 3 (Fan-Out with Jerry sub-agents) or single-agent execution.

---

## CLI Reference Table

| CLI | Invocation Pattern | Notes |
|-----|--------------------|-------|
| **Claude** | `claude --dangerously-skip-permissions --model claude-opus-4-6 --thinking-budget high -p "<prompt>"` | `-p` is the prompt flag; `--thinking-budget high` for complex tasks |
| **Codex** | `codex --yolo --model gpt-5.2 --reasoning-effort high --full-auto exec "<prompt>"` | `--yolo` skips confirmations; `--full-auto exec` for autonomous execution |
| **Gemini** | `gemini --yolo --model gemini-2.5-pro --prompt "<prompt>"` | `--yolo` skips confirmations; `--prompt` is the prompt flag |

**Model Fallbacks (when specific model unavailable):**

| CLI | Primary Model | Fallback |
|-----|--------------|----------|
| Claude | `claude-opus-4-6` | `claude-sonnet-4-6` |
| Codex | `gpt-5.2` | `gpt-4o` |
| Gemini | `gemini-2.5-pro` | `gemini-1.5-pro` |

---

## File Layout

Consensus Panel artifacts follow the standard orchestration path scheme, with a dedicated `consensus/` subdirectory:

```
orchestration/{workflow_id}/consensus/
├── {phase_id}-intent.md           # Shared seed document (orchestrator writes)
├── {phase_id}-claude-draft.md     # Claude CLI output
├── {phase_id}-codex-draft.md      # Codex CLI output
├── {phase_id}-gemini-draft.md     # Gemini CLI output
├── {phase_id}-claude-critique.md  # Claude critiques Codex+Gemini
├── {phase_id}-codex-critique.md   # Codex critiques Claude+Gemini
├── {phase_id}-gemini-critique.md  # Gemini critiques Claude+Codex
└── {phase_id}-synthesis.md        # orch-synthesizer final output
```

---

## Parallel Launch Pattern

### Draft Phase (all three write independently)

```bash
INTENT_FILE="orchestration/{workflow_id}/consensus/{phase_id}-intent.md"
CLAUDE_OUT="orchestration/{workflow_id}/consensus/{phase_id}-claude-draft.md"
CODEX_OUT="orchestration/{workflow_id}/consensus/{phase_id}-codex-draft.md"
GEMINI_OUT="orchestration/{workflow_id}/consensus/{phase_id}-gemini-draft.md"

# Launch all three in parallel
if [ -n "$CLAUDE_CLI" ]; then
  $CLAUDE_CLI --dangerously-skip-permissions --model claude-opus-4-6 \
    --thinking-budget high -p \
    "Read ${INTENT_FILE} and write an independent analysis to ${CLAUDE_OUT}. {task_instructions}" &
  CLAUDE_PID=$!
fi

if [ -n "$CODEX_CLI" ]; then
  $CODEX_CLI --yolo --model gpt-5.2 --reasoning-effort high --full-auto exec \
    "Read ${INTENT_FILE} and write an independent analysis to ${CODEX_OUT}. {task_instructions}" &
  CODEX_PID=$!
fi

if [ -n "$GEMINI_CLI" ]; then
  $GEMINI_CLI --yolo --model gemini-2.5-pro \
    --prompt "Read ${INTENT_FILE} and write an independent analysis to ${GEMINI_DRAFT}. {task_instructions}" &
  GEMINI_PID=$!
fi

# Wait for all to complete
wait $CLAUDE_PID $CODEX_PID $GEMINI_PID
echo "Draft phase complete. Exit codes: claude=$? codex=$? gemini=$?"
```

### Cross-Critique Phase (each critiques the other two)

```bash
CLAUDE_CRIT="orchestration/{workflow_id}/consensus/{phase_id}-claude-critique.md"
CODEX_CRIT="orchestration/{workflow_id}/consensus/{phase_id}-codex-critique.md"
GEMINI_CRIT="orchestration/{workflow_id}/consensus/{phase_id}-gemini-critique.md"

# Claude critiques Codex + Gemini
if [ -n "$CLAUDE_CLI" ]; then
  $CLAUDE_CLI --dangerously-skip-permissions --model claude-opus-4-6 \
    --thinking-budget high -p \
    "Read ${CODEX_OUT} and ${GEMINI_OUT}. Write a critique to ${CLAUDE_CRIT}. Identify strengths, weaknesses, gaps, and missed edge cases in each." &
  CLAUDE_PID=$!
fi

# Codex critiques Claude + Gemini
if [ -n "$CODEX_CLI" ]; then
  $CODEX_CLI --yolo --model gpt-5.2 --reasoning-effort high --full-auto exec \
    "Read ${CLAUDE_OUT} and ${GEMINI_OUT}. Write a critique to ${CODEX_CRIT}. Identify strengths, weaknesses, gaps, and missed edge cases in each." &
  CODEX_PID=$!
fi

# Gemini critiques Claude + Codex
if [ -n "$GEMINI_CLI" ]; then
  $GEMINI_CLI --yolo --model gemini-2.5-pro \
    --prompt "Read ${CLAUDE_OUT} and ${CODEX_OUT}. Write a critique to ${GEMINI_CRIT}. Identify strengths, weaknesses, gaps, and missed edge cases in each." &
  GEMINI_PID=$!
fi

wait $CLAUDE_PID $CODEX_PID $GEMINI_PID
echo "Critique phase complete."
```

---

## Exit Code Handling

Each CLI process exits with a standard Unix exit code. The orchestrator MUST check for failures:

```bash
# After wait, verify outputs exist
MISSING=()
[ -n "$CLAUDE_CLI" ] && [ ! -f "$CLAUDE_OUT" ] && MISSING+=("claude-draft")
[ -n "$CODEX_CLI"  ] && [ ! -f "$CODEX_OUT"  ] && MISSING+=("codex-draft")
[ -n "$GEMINI_CLI" ] && [ ! -f "$GEMINI_OUT" ] && MISSING+=("gemini-draft")

if [ ${#MISSING[@]} -gt 0 ]; then
  echo "WARNING: Missing outputs: ${MISSING[*]}"
  echo "Proceeding with available outputs. Synthesis will note gaps."
fi
```

**Degradation strategy:** If one CLI fails, proceed with the remaining outputs and note the gap in the synthesis. A single-CLI failure should not abort the workflow.

---

## Synthesis Handoff

After parallel phases complete, invoke `orch-synthesizer` via the standard Task tool:

```python
Task(
    description="orch-synthesizer: Synthesize consensus panel outputs",
    subagent_type="orch-synthesizer",
    prompt="""
You are orch-synthesizer. Synthesize outputs from the Consensus Panel.

## Inputs
- Intent document: {intent_file}
- Claude draft: {claude_out} (present: {claude_present})
- Codex draft:  {codex_out}  (present: {codex_present})
- Gemini draft: {gemini_out} (present: {gemini_present})
- Claude critique: {claude_crit} (present: {claude_crit_present})
- Codex critique:  {codex_crit}  (present: {codex_crit_present})
- Gemini critique: {gemini_crit} (present: {gemini_crit_present})

## Task
1. Read ALL available draft and critique files.
2. Extract strongest elements from each draft.
3. Identify points where all CLIs agree (high-confidence findings).
4. Identify points where CLIs diverge (requires human judgment or further analysis).
5. Note gaps from any missing CLI outputs.
6. Write synthesis to: {synthesis_out}

Apply S-014 (LLM-as-Judge) self-scoring after writing.
"""
)
```

---

## ORCHESTRATION.yaml Extensions

When a workflow uses the Consensus Panel pattern, the ORCHESTRATION.yaml includes a `consensus_panel` section:

```yaml
consensus_panel:
  enabled: true
  phase_id: "{phase_id}"
  cli_availability:
    claude: "{detected|unavailable}"
    codex:  "{detected|unavailable}"
    gemini: "{detected|unavailable}"
  cli_commands:
    claude: "claude --dangerously-skip-permissions --model claude-opus-4-6 --thinking-budget high -p"
    codex:  "codex --yolo --model gpt-5.2 --reasoning-effort high --full-auto exec"
    gemini: "gemini --yolo --model gemini-2.5-pro --prompt"
  artifacts:
    intent:         "orchestration/{workflow_id}/consensus/{phase_id}-intent.md"
    claude_draft:   "orchestration/{workflow_id}/consensus/{phase_id}-claude-draft.md"
    codex_draft:    "orchestration/{workflow_id}/consensus/{phase_id}-codex-draft.md"
    gemini_draft:   "orchestration/{workflow_id}/consensus/{phase_id}-gemini-draft.md"
    claude_critique: "orchestration/{workflow_id}/consensus/{phase_id}-claude-critique.md"
    codex_critique:  "orchestration/{workflow_id}/consensus/{phase_id}-codex-critique.md"
    gemini_critique: "orchestration/{workflow_id}/consensus/{phase_id}-gemini-critique.md"
    synthesis:      "orchestration/{workflow_id}/consensus/{phase_id}-synthesis.md"
  status:
    draft_phase:    "PENDING|IN_PROGRESS|COMPLETE|PARTIAL|FAILED"
    critique_phase: "PENDING|IN_PROGRESS|COMPLETE|PARTIAL|FAILED"
    synthesis:      "PENDING|IN_PROGRESS|COMPLETE|FAILED"
  results:
    consensus_points: []    # Populated by orch-synthesizer
    divergence_points: []   # Populated by orch-synthesizer
    cli_failures: []        # Populated by orchestrator after wait
```

---

## P-003 Compliance Note

External CLI processes invoked via `Bash` are **not** Jerry sub-agents. They do not consume Claude context budget, do not have access to Jerry tools, and do not spawn further agents. They are OS-level subprocesses that read input files and write output files. The P-003 constraint (max one level of agent nesting) applies only to `Task(subagent_type=...)` invocations, not to `Bash` subprocess launches.

```
P-003 scope:
  MAIN CONTEXT
      └──► Task(subagent_type="orch-synthesizer")  ← ONE level (allowed)
               └──► (no further Task calls)         ← compliant

NOT in P-003 scope:
  MAIN CONTEXT
      └──► Bash("claude --dangerously-skip-permissions ...")  ← OS subprocess (not an agent)
      └──► Bash("codex --yolo ...")                           ← OS subprocess (not an agent)
      └──► Bash("gemini --yolo ...")                          ← OS subprocess (not an agent)
```

---

*Document Version: 1.0.0*
*Skill: orchestration*
*Pattern: Consensus Panel*
