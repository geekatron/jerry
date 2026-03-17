#!/usr/bin/env bash
# consensus-panel.sh — Consensus Panel pattern implementation template
# Skill: orchestration | Pattern: Consensus Panel (Pattern 6 in PATTERNS.md)
# Version: 1.3.0
#
# Usage: source or copy-adapt this file. Set WORKFLOW_ID, PHASE_ID, and
# transport variables before calling the functions.
#
# See docs/MULTI_CLI_INTEGRATION.md for pre-flight resolution steps (Phase 0)
# that must run before using these functions.

# ---------------------------------------------------------------------------
# PATH SANITIZATION (run before any file construction)
# ---------------------------------------------------------------------------
# WORKFLOW_ID=$(echo "$WORKFLOW_ID" | tr -cd 'a-zA-Z0-9_-')
# PHASE_ID=$(echo "$PHASE_ID"       | tr -cd 'a-zA-Z0-9_-')
# CONSENSUS_DIR="orchestration/${WORKFLOW_ID}/consensus"
# mkdir -p "$CONSENSUS_DIR"

# ---------------------------------------------------------------------------
# API WRAPPERS (used when transport = "api")
# ---------------------------------------------------------------------------

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

invoke_gemini_api() {
  local prompt_file="$1" output_file="$2"
  local api_key="${GEMINI_API_KEY:-$GOOGLE_API_KEY}"
  curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key=$api_key" \
    -H "Content-Type: application/json" \
    -d "{
      \"contents\": [{\"parts\": [{\"text\": $(cat "$prompt_file" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')}]}]
    }" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['candidates'][0]['content']['parts'][0]['text'])" > "$output_file"
}

# ---------------------------------------------------------------------------
# LAUNCH HELPER
# Dispatches to CLI or API transport, backgrounds the process, echoes PID.
# ---------------------------------------------------------------------------
# Arguments:
#   $1  model      "claude" | "codex" | "gemini"
#   $2  transport  "cli" | "api"
#   $3  prompt_file  path to prompt file
#   $4  output_file  path for model output
# Returns: PID of background process, or "" if not launched
# ---------------------------------------------------------------------------

launch_worker() {
  local model="$1"
  local transport="$2"
  local prompt_file="$3"
  local output_file="$4"

  case "$model:$transport" in
    claude:cli)
      # T-002: never use claude CLI when CLAUDECODE=1 (nested session hang).
      # Pre-flight (Step 0b) must have already downgraded transport to "" or "api".
      claude --dangerously-skip-permissions --model claude-opus-4-6 \
        --thinking-budget high -p "$(cat "$prompt_file")" > "$output_file" 2>&1 &
      echo $!
      ;;
    codex:cli)
      # T-004: codex v0.115.0+ — use `exec --full-auto`, not `--yolo`.
      # --full-auto and --dangerously-bypass-approvals-and-sandbox are mutually exclusive.
      codex exec --full-auto -m gpt-4o "$(cat "$prompt_file")" > "$output_file" 2>&1 &
      echo $!
      ;;
    gemini:cli)
      # T-003: GEMINI_API_KEY or GOOGLE_API_KEY must be set; gemini exits 41 without it.
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
      echo ""  # not launched
      ;;
  esac
}

# ---------------------------------------------------------------------------
# WAIT WITH TIMEOUT
# Waits for a PID with a watchdog kill after $timeout seconds.
# Returns the process exit code (or 0 if pid was empty).
# ---------------------------------------------------------------------------
# Arguments:
#   $1  pid      process ID (may be empty — safely no-ops)
#   $2  model    label for warning messages
#   $3  timeout  seconds before kill
# ---------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------
# OUTPUT VERIFICATION
# Checks that output files are non-empty after a phase completes.
# Reports missing outputs; does NOT abort (gaps noted in synthesis).
# ---------------------------------------------------------------------------
# Arguments: phase_label, then pairs of: label path label path ...
# Example:
#   verify_outputs "draft" \
#     "claude" "$CLAUDE_OUT" \
#     "codex"  "$CODEX_OUT"  \
#     "gemini" "$GEMINI_OUT"
# ---------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------
# EXAMPLE: DRAFT PHASE
# Copy-adapt this block — replace path variables with your actual values.
# ---------------------------------------------------------------------------
# TIMEOUT=${CONSENSUS_TIMEOUT:-300}
#
# CLAUDE_PID=$([ -n "$CLAUDE_TRANSPORT" ] && \
#   launch_worker claude "$CLAUDE_TRANSPORT" "$CLAUDE_PROMPT" "$CLAUDE_OUT" || echo "")
# CODEX_PID=$([ -n "$CODEX_TRANSPORT" ] && \
#   launch_worker codex  "$CODEX_TRANSPORT"  "$CODEX_PROMPT"  "$CODEX_OUT"  || echo "")
# GEMINI_PID=$([ -n "$GEMINI_TRANSPORT" ] && \
#   launch_worker gemini "$GEMINI_TRANSPORT" "$GEMINI_PROMPT" "$GEMINI_OUT" || echo "")
#
# wait_with_timeout "$CLAUDE_PID" "claude" "$TIMEOUT"; CLAUDE_EXIT=$?
# wait_with_timeout "$CODEX_PID"  "codex"  "$TIMEOUT"; CODEX_EXIT=$?
# wait_with_timeout "$GEMINI_PID" "gemini" "$TIMEOUT"; GEMINI_EXIT=$?
#
# echo "Draft exits: claude=$CLAUDE_EXIT codex=$CODEX_EXIT gemini=$GEMINI_EXIT"
# verify_outputs "draft" "claude" "$CLAUDE_OUT" "codex" "$CODEX_OUT" "gemini" "$GEMINI_OUT"

# ---------------------------------------------------------------------------
# EXAMPLE: CRITIQUE PHASE
# Only launch critique for models whose peers' draft files exist.
# ---------------------------------------------------------------------------
# CLAUDE_CRIT_PID=$([ -f "$CODEX_OUT" ] && [ -f "$GEMINI_OUT" ] && [ -n "$CLAUDE_TRANSPORT" ] && \
#   launch_worker claude "$CLAUDE_TRANSPORT" "$CLAUDE_CRIT_PROMPT" "$CLAUDE_CRIT" || echo "")
# CODEX_CRIT_PID=$([ -f "$CLAUDE_OUT" ] && [ -f "$GEMINI_OUT" ] && [ -n "$CODEX_TRANSPORT" ] && \
#   launch_worker codex  "$CODEX_TRANSPORT"  "$CODEX_CRIT_PROMPT"  "$CODEX_CRIT"  || echo "")
# GEMINI_CRIT_PID=$([ -f "$CLAUDE_OUT" ] && [ -f "$CODEX_OUT" ] && [ -n "$GEMINI_TRANSPORT" ] && \
#   launch_worker gemini "$GEMINI_TRANSPORT" "$GEMINI_CRIT_PROMPT" "$GEMINI_CRIT" || echo "")
#
# wait_with_timeout "$CLAUDE_CRIT_PID" "claude-critique" "$TIMEOUT"
# wait_with_timeout "$CODEX_CRIT_PID"  "codex-critique"  "$TIMEOUT"
# wait_with_timeout "$GEMINI_CRIT_PID" "gemini-critique" "$TIMEOUT"
#
# verify_outputs "critique" \
#   "claude-critique" "$CLAUDE_CRIT" \
#   "codex-critique"  "$CODEX_CRIT"  \
#   "gemini-critique" "$GEMINI_CRIT"
