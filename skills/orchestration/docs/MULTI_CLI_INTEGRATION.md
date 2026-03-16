---
title: Multi-CLI Parallel Execution Integration
version: "1.1.0"
skill: orchestration
pattern: consensus-panel
---

# Multi-CLI Parallel Execution Integration

> **Version:** 1.1.0 (revised from 1.0.0 — C4 adversarial review findings F-001 through F-009)
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

---

## Phase 0: Pre-Flight Resolution

Run the full resolution chain **before** launching any parallel work. Never skip this phase.

### Step 0a: Platform Detection

```bash
# Detect execution environment
if [ -n "$WSL_DISTRO_NAME" ] || uname -s | grep -qi linux; then
  PLATFORM="linux"
  PARALLEL_SUPPORTED=true
elif uname -s | grep -qi mingw || uname -s | grep -qi cygwin; then
  PLATFORM="windows-native"
  PARALLEL_SUPPORTED=false
else
  PLATFORM="unknown"
  PARALLEL_SUPPORTED=true  # assume linux-like
fi
echo "Platform: $PLATFORM | Parallel supported: $PARALLEL_SUPPORTED"
```

If `PARALLEL_SUPPORTED=false` (Windows native without WSL), warn the user: bash `&` background execution is unavailable. Offer to run sequentially or switch to WSL.

### Step 0b: CLI Detection

```bash
CLAUDE_TRANSPORT=""
CODEX_TRANSPORT=""
GEMINI_TRANSPORT=""

command -v claude  >/dev/null 2>&1 && CLAUDE_TRANSPORT="cli"
command -v codex   >/dev/null 2>&1 && CODEX_TRANSPORT="cli"
command -v gemini  >/dev/null 2>&1 && GEMINI_TRANSPORT="cli"
```

### Step 0c: Auth Validation

For each detected CLI, validate that authentication is functional — not just that the binary exists.

```bash
# Claude: check API key present (actual validation requires a test call)
if [ "$CLAUDE_TRANSPORT" = "cli" ]; then
  if [ -z "$ANTHROPIC_API_KEY" ] && ! claude auth status >/dev/null 2>&1; then
    echo "WARNING: claude CLI found but auth may not be configured"
    CLAUDE_TRANSPORT="auth-warning"
  fi
fi

# Codex: check OpenAI key
if [ "$CODEX_TRANSPORT" = "cli" ]; then
  if [ -z "$OPENAI_API_KEY" ]; then
    echo "WARNING: codex CLI found but OPENAI_API_KEY not set"
    CODEX_TRANSPORT="auth-warning"
  fi
fi

# Gemini: check Google key
if [ "$GEMINI_TRANSPORT" = "cli" ]; then
  if [ -z "$GEMINI_API_KEY" ] && [ -z "$GOOGLE_API_KEY" ]; then
    echo "WARNING: gemini CLI found but GEMINI_API_KEY / GOOGLE_API_KEY not set"
    GEMINI_TRANSPORT="auth-warning"
  fi
fi
```

### Step 0d: API Fallback Resolution

If a CLI is missing or has auth issues, attempt API-based invocation. This makes the pattern work on CI/CD systems, restricted machines, or anywhere the CLI binary isn't installed but API keys are available.

```bash
# API fallback: if CLI missing/broken but API key present, mark as api transport
if [ "$CLAUDE_TRANSPORT" != "cli" ] && [ -n "$ANTHROPIC_API_KEY" ]; then
  CLAUDE_TRANSPORT="api"
  echo "claude: using API transport (ANTHROPIC_API_KEY set)"
fi

if [ "$CODEX_TRANSPORT" != "cli" ] && [ -n "$OPENAI_API_KEY" ]; then
  CODEX_TRANSPORT="api"
  echo "codex: using API transport (OPENAI_API_KEY set)"
fi

if [ "$GEMINI_TRANSPORT" != "cli" ] && \
   ([ -n "$GEMINI_API_KEY" ] || [ -n "$GOOGLE_API_KEY" ]); then
  GEMINI_TRANSPORT="api"
  echo "gemini: using API transport (API key set)"
fi
```

**API invocation wrappers** (when transport = "api"):

For Claude API:
```bash
invoke_claude_api() {
  local prompt_file="$1" output_file="$2"
  curl -s "https://api.anthropic.com/v1/messages" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d "{
      \"model\": \"claude-opus-4-6\",
      \"max_tokens\": 8192,
      \"messages\": [{\"role\": \"user\", \"content\": $(cat "$prompt_file" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')}]
    }" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['content'][0]['text'])" > "$output_file"
}
```

For OpenAI API (Codex):
```bash
invoke_codex_api() {
  local prompt_file="$1" output_file="$2"
  curl -s "https://api.openai.com/v1/chat/completions" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
      \"model\": \"gpt-4o\",
      \"messages\": [{\"role\": \"user\", \"content\": $(cat "$prompt_file" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')}]
    }" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['choices'][0]['message']['content'])" > "$output_file"
}
```

For Gemini API:
```bash
invoke_gemini_api() {
  local prompt_file="$1" output_file="$2"
  local api_key="${GEMINI_API_KEY:-$GOOGLE_API_KEY}"
  curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key=$api_key" \
    -H "Content-Type: application/json" \
    -d "{
      \"contents\": [{\"parts\": [{\"text\": $(cat "$prompt_file" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')}]}]
    }" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['candidates'][0]['content']['parts'][0]['text'])" > "$output_file"
}
```

### Step 0e: Panel Composition Summary + User Gate

After resolution, compute how many workers are available and **ask the user before proceeding if the panel is degraded**.

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
| 2 of 3 | **Ask user:** "One model is unavailable. Proceed with 2-model panel, or cancel?" |
| 1 of 3 | **Ask user:** "Only 1 model available. This is no longer a consensus panel. Continue as single-model draft, or cancel?" |
| 0 of 3 | **Ask user:** "No external models available. Fall back to Jerry sub-agent drafts, or cancel workflow?" |

When the orchestrator uses `AskUserQuestion`, present the panel report (above) as context so the user can make an informed decision. Do NOT silently proceed with a degraded panel.

---

## CLI Reference Table

| CLI | Invocation Pattern | Transport |
|-----|--------------------|-----------|
| **Claude** | `claude --dangerously-skip-permissions --model claude-opus-4-6 --thinking-budget high -p "<prompt>"` | CLI |
| **Codex** | `codex --yolo --model gpt-5.2 --reasoning-effort high --full-auto exec "<prompt>"` | CLI |
| **Gemini** | `gemini --yolo --model gemini-2.5-pro --prompt "<prompt>"` | CLI |
| **Claude** | `invoke_claude_api prompt_file output_file` | API |
| **Codex** | `invoke_codex_api prompt_file output_file` | API |
| **Gemini** | `invoke_gemini_api prompt_file output_file` | API |

**Model Fallbacks (when specific model unavailable):**

| CLI | Primary Model | Fallback |
|-----|--------------|----------|
| Claude | `claude-opus-4-6` | `claude-sonnet-4-6` |
| Codex | `gpt-5.2` | `gpt-4o` |
| Gemini | `gemini-2.5-pro` | `gemini-1.5-pro` |

> **Security note:** The `--dangerously-skip-permissions` and `--yolo` flags give each CLI broad file system access. Ensure the intent file is written by the orchestrator itself (never pass user-supplied raw text directly as a file path). Normalize `{workflow_id}` and `{phase_id}` to remove any `..` or `/` characters before constructing paths.

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
# Sanitize workflow_id and phase_id — no path traversal characters
WORKFLOW_ID=$(echo "$WORKFLOW_ID" | tr -cd 'a-zA-Z0-9_-')
PHASE_ID=$(echo "$PHASE_ID" | tr -cd 'a-zA-Z0-9_-')
CONSENSUS_DIR="orchestration/${WORKFLOW_ID}/consensus"
mkdir -p "$CONSENSUS_DIR"
```

---

## Parallel Launch Pattern

### Launch Helper

Use a unified launch helper that dispatches to CLI or API transport, writes output to file, and records the PID:

```bash
launch_worker() {
  local model="$1"        # "claude" | "codex" | "gemini"
  local transport="$2"    # "cli" | "api"
  local prompt_file="$3"  # path to prompt (intent + task instructions)
  local output_file="$4"  # path for output

  case "$model:$transport" in
    claude:cli)
      claude --dangerously-skip-permissions --model claude-opus-4-6 \
        --thinking-budget high -p "$(cat "$prompt_file")" > "$output_file" 2>&1 &
      echo $!
      ;;
    codex:cli)
      codex --yolo --model gpt-5.2 --reasoning-effort high --full-auto exec \
        "$(cat "$prompt_file")" > "$output_file" 2>&1 &
      echo $!
      ;;
    gemini:cli)
      gemini --yolo --model gemini-2.5-pro \
        --prompt "$(cat "$prompt_file")" > "$output_file" 2>&1 &
      echo $!
      ;;
    claude:api)
      invoke_claude_api "$prompt_file" "$output_file" &
      echo $!
      ;;
    codex:api)
      invoke_codex_api "$prompt_file" "$output_file" &
      echo $!
      ;;
    gemini:api)
      invoke_gemini_api "$prompt_file" "$output_file" &
      echo $!
      ;;
    *)
      echo ""  # no PID — not launched
      ;;
  esac
}
```

### Draft Phase

```bash
INTENT="$CONSENSUS_DIR/${PHASE_ID}-intent.md"
CLAUDE_OUT="$CONSENSUS_DIR/${PHASE_ID}-claude-draft.md"
CODEX_OUT="$CONSENSUS_DIR/${PHASE_ID}-codex-draft.md"
GEMINI_OUT="$CONSENSUS_DIR/${PHASE_ID}-gemini-draft.md"

# Write task instructions into prompt files (one per model)
# (orchestrator writes these before launching workers)
CLAUDE_PROMPT="$CONSENSUS_DIR/${PHASE_ID}-claude-prompt.md"
CODEX_PROMPT="$CONSENSUS_DIR/${PHASE_ID}-codex-prompt.md"
GEMINI_PROMPT="$CONSENSUS_DIR/${PHASE_ID}-gemini-prompt.md"

cat > "$CLAUDE_PROMPT" <<EOF
Read $INTENT and write an independent draft to $CLAUDE_OUT.
Follow the structure: Overview, Approach, Implementation, Risks, Open Questions.
EOF

# ... similarly for CODEX_PROMPT and GEMINI_PROMPT

# Launch workers
CLAUDE_PID=$([ -n "$CLAUDE_TRANSPORT" ] && \
  launch_worker claude "$CLAUDE_TRANSPORT" "$CLAUDE_PROMPT" "$CLAUDE_OUT" || echo "")
CODEX_PID=$([ -n "$CODEX_TRANSPORT" ] && \
  launch_worker codex "$CODEX_TRANSPORT" "$CODEX_PROMPT" "$CODEX_OUT" || echo "")
GEMINI_PID=$([ -n "$GEMINI_TRANSPORT" ] && \
  launch_worker gemini "$GEMINI_TRANSPORT" "$GEMINI_PROMPT" "$GEMINI_OUT" || echo "")

# Wait with per-PID exit code capture and timeout (300s default)
TIMEOUT=${CONSENSUS_TIMEOUT:-300}
wait_with_timeout() {
  local pid="$1" model="$2" timeout="$3"
  if [ -z "$pid" ]; then return 0; fi
  ( sleep "$timeout" && kill "$pid" 2>/dev/null ) &
  local watchdog=$!
  wait "$pid"
  local code=$?
  kill "$watchdog" 2>/dev/null
  if [ $code -ne 0 ]; then
    echo "WARNING: $model worker exited with code $code"
  fi
  return $code
}

wait_with_timeout "$CLAUDE_PID" "claude" "$TIMEOUT"
CLAUDE_EXIT=$?
wait_with_timeout "$CODEX_PID"  "codex"  "$TIMEOUT"
CODEX_EXIT=$?
wait_with_timeout "$GEMINI_PID" "gemini" "$TIMEOUT"
GEMINI_EXIT=$?

echo "Draft exits: claude=$CLAUDE_EXIT codex=$CODEX_EXIT gemini=$GEMINI_EXIT"
```

### Output Verification After Each Phase

```bash
verify_outputs() {
  local phase_label="$1"
  shift
  local missing=()
  while [ "$#" -gt 0 ]; do
    local label="$1" path="$2"
    shift 2
    if [ ! -s "$path" ]; then
      missing+=("$label ($path)")
    fi
  done
  if [ ${#missing[@]} -gt 0 ]; then
    echo "MISSING $phase_label outputs:"
    for m in "${missing[@]}"; do echo "  - $m"; done
    echo "These gaps will be noted in synthesis."
  fi
}

verify_outputs "draft" \
  "claude" "$CLAUDE_OUT" \
  "codex"  "$CODEX_OUT" \
  "gemini" "$GEMINI_OUT"
```

### Cross-Critique Phase

```bash
CLAUDE_CRIT="$CONSENSUS_DIR/${PHASE_ID}-claude-critique.md"
CODEX_CRIT="$CONSENSUS_DIR/${PHASE_ID}-codex-critique.md"
GEMINI_CRIT="$CONSENSUS_DIR/${PHASE_ID}-gemini-critique.md"

# Only launch critique if the draft files to critique actually exist
CLAUDE_CRIT_PROMPT="$CONSENSUS_DIR/${PHASE_ID}-claude-critique-prompt.md"
cat > "$CLAUDE_CRIT_PROMPT" <<EOF
Read the following drafts and write a critique to $CLAUDE_CRIT.
Identify strengths, weaknesses, gaps, and missed edge cases in each.
Codex draft: $CODEX_OUT
Gemini draft: $GEMINI_OUT
EOF

# ... similarly for CODEX_CRIT_PROMPT (reads claude+gemini) and GEMINI_CRIT_PROMPT

CLAUDE_CRIT_PID=$([ -f "$CODEX_OUT" ] && [ -f "$GEMINI_OUT" ] && [ -n "$CLAUDE_TRANSPORT" ] && \
  launch_worker claude "$CLAUDE_TRANSPORT" "$CLAUDE_CRIT_PROMPT" "$CLAUDE_CRIT" || echo "")
CODEX_CRIT_PID=$([ -f "$CLAUDE_OUT" ] && [ -f "$GEMINI_OUT" ] && [ -n "$CODEX_TRANSPORT" ] && \
  launch_worker codex "$CODEX_TRANSPORT" "$CODEX_CRIT_PROMPT" "$CODEX_CRIT" || echo "")
GEMINI_CRIT_PID=$([ -f "$CLAUDE_OUT" ] && [ -f "$CODEX_OUT" ] && [ -n "$GEMINI_TRANSPORT" ] && \
  launch_worker gemini "$GEMINI_TRANSPORT" "$GEMINI_CRIT_PROMPT" "$GEMINI_CRIT" || echo "")

wait_with_timeout "$CLAUDE_CRIT_PID" "claude-critique" "$TIMEOUT"
wait_with_timeout "$CODEX_CRIT_PID"  "codex-critique"  "$TIMEOUT"
wait_with_timeout "$GEMINI_CRIT_PID" "gemini-critique" "$TIMEOUT"

verify_outputs "critique" \
  "claude-critique" "$CLAUDE_CRIT" \
  "codex-critique"  "$CODEX_CRIT" \
  "gemini-critique" "$GEMINI_CRIT"
```

---

## Synthesis Handoff

After parallel phases complete, invoke `orch-synthesizer` via the standard Task tool:

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
Surface this prominently in the synthesis output — do not present a partial
panel as if it were full 3-way consensus.

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
5. If panel was partial: include a PANEL GAPS section listing which models
   were absent and what perspectives may be missing as a result.
6. Write synthesis to: {synthesis_out}

Apply S-014 (LLM-as-Judge) self-scoring after writing.
"""
)
```

---

## ORCHESTRATION.yaml Extensions

```yaml
consensus_panel:
  enabled: true
  phase_id: "{phase_id}"
  platform: "{linux|windows-native|unknown}"
  parallel_supported: "{true|false}"
  cli_availability:
    claude: "{cli|api|unavailable}"
    codex:  "{cli|api|unavailable}"
    gemini: "{cli|api|unavailable}"
  workers_available: "{0|1|2|3}"
  user_confirmed_degraded: "{true|false|n/a}"  # n/a when full panel
  timeout_seconds: 300
  cli_commands:
    claude: "claude --dangerously-skip-permissions --model claude-opus-4-6 --thinking-budget high -p"
    codex:  "codex --yolo --model gpt-5.2 --reasoning-effort high --full-auto exec"
    gemini: "gemini --yolo --model gemini-2.5-pro --prompt"
  api_fallback_used:
    claude: "{true|false}"
    codex:  "{true|false}"
    gemini: "{true|false}"
  artifacts:
    intent:          "orchestration/{workflow_id}/consensus/{phase_id}-intent.md"
    claude_draft:    "orchestration/{workflow_id}/consensus/{phase_id}-claude-draft.md"
    codex_draft:     "orchestration/{workflow_id}/consensus/{phase_id}-codex-draft.md"
    gemini_draft:    "orchestration/{workflow_id}/consensus/{phase_id}-gemini-draft.md"
    claude_critique: "orchestration/{workflow_id}/consensus/{phase_id}-claude-critique.md"
    codex_critique:  "orchestration/{workflow_id}/consensus/{phase_id}-codex-critique.md"
    gemini_critique: "orchestration/{workflow_id}/consensus/{phase_id}-gemini-critique.md"
    synthesis:       "orchestration/{workflow_id}/consensus/{phase_id}-synthesis.md"
  exit_codes:
    claude_draft:    "{0|1|timeout|-1}"  # -1 = not launched
    codex_draft:     "{0|1|timeout|-1}"
    gemini_draft:    "{0|1|timeout|-1}"
  status:
    preflight:      "PENDING|COMPLETE|BLOCKED"
    draft_phase:    "PENDING|IN_PROGRESS|COMPLETE|PARTIAL|FAILED"
    critique_phase: "PENDING|IN_PROGRESS|COMPLETE|PARTIAL|FAILED"
    synthesis:      "PENDING|IN_PROGRESS|COMPLETE|FAILED"
  results:
    consensus_points: []    # Populated by orch-synthesizer
    divergence_points: []   # Populated by orch-synthesizer
    panel_gaps: []          # Models absent; populated by orchestrator
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
        │                              │
        │                         Proceed ──► Launch with 2 workers
        │
        NO
        ▼
 1 worker available? ──YES──► AskUserQuestion:
        │                       "Only {model} available.
        │                        This is no longer a consensus panel.
        │                        Options: [Proceed as single-model draft]
        │                                 [Fall back to Jerry sub-agents]
        │                                 [Cancel]"
        │
        NO
        ▼
 0 workers available ────────► AskUserQuestion:
                                "No external models available.
                                 Options: [Fall back to Jerry sub-agents]
                                          [Cancel workflow]"
```

**Jerry sub-agent fallback** (0 external models): invoke `orch-synthesizer` directly with the intent document, or use the standard Fan-Out pattern (Pattern 3) with jerry agents instead of external CLIs.

---

## P-003 Compliance Note

External CLI and API processes invoked via `Bash` are **not** Jerry sub-agents. They do not consume Claude context budget, do not have access to Jerry tools, and do not spawn further agents. P-003 (max one level of agent nesting) applies only to `Task(subagent_type=...)` invocations.

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

## Security Considerations

- **`--dangerously-skip-permissions` / `--yolo`:** These flags give CLI workers broad file system access. The intent file and output paths MUST be written by the orchestrator itself — never pass user-supplied raw text as a file path argument.
- **Path sanitization:** Always sanitize `{workflow_id}` and `{phase_id}` before constructing paths (remove `..`, `/`, special characters).
- **API keys:** Never log or write API keys to output files. Pass via environment variables only.
- **Prompt injection:** The intent document is orchestrator-authored. If any prior pipeline step produced content that feeds into the intent file, sanitize or review it before use as a CLI prompt seed.

---

*Document Version: 1.1.0*
*Skill: orchestration*
*Pattern: Consensus Panel*
*Revised: C4 adversarial review — F-001 (user gate), F-002 (auth), F-003 (variable bug), F-004 (timeout), F-005 (exit codes), F-006 (API fallback), F-007 (platform), F-008 (security note), F-009 (path sanitization)*
