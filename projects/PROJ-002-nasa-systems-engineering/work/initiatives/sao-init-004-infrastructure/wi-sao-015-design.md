# WI-SAO-015: Guardrail Validation Hooks - Design Document

> **Work Item:** WI-SAO-015
> **Task:** T-015.1 Design guardrail hook interface
> **Date:** 2026-01-12
> **Status:** IN PROGRESS

---

## Executive Summary

This design extends the existing `pre_tool_use.py` hook with a centralized pattern library, warn mode, and configurable timeout to meet AC-015-001 through AC-015-004.

---

## Current State Analysis

### Existing Infrastructure

| Component | Location | Status |
|-----------|----------|--------|
| PreToolUse hook | `.claude/hooks/pre_tool_use.py` | ✅ Exists |
| Hook config | `.claude/settings.json` | ✅ Configured |
| SubagentStop hook | `.claude/hooks/subagent_stop.py` | ✅ Exists |
| Pattern library | - | ❌ Missing |
| Warn mode | - | ❌ Missing |

### Existing Patterns (in pre_tool_use.py)

```python
BLOCKED_WRITE_PATHS = ["~/.ssh", "~/.gnupg", "~/.aws", ...]
SENSITIVE_FILE_PATTERNS = [".env", "credentials.json", "*.pem", ...]
DANGEROUS_COMMANDS = ["rm -rf /", "chmod 777", "curl | bash", ...]
```

---

## Design Proposal

### Architecture

```
.claude/
├── hooks/
│   ├── pre_tool_use.py      # Main hook (extended)
│   ├── post_tool_use.py     # NEW: Output validation
│   └── patterns/
│       ├── schema.json      # JSON Schema for patterns.yaml
│       └── patterns.yaml    # Pattern library (NEW)
└── settings.json            # Hook configuration
```

### Pattern Library Schema (patterns.yaml)

```yaml
# .claude/hooks/patterns/patterns.yaml
schema_version: "1.0.0"

validation_modes:
  block: "Reject operation"
  warn: "Log warning, allow operation"
  ask: "Prompt user for confirmation"

patterns:
  # Input Validation Patterns
  input:
    pii_detection:
      name: "PII Detection"
      description: "Detect personally identifiable information"
      mode: warn  # AC-015-003: warn mode
      timeout_ms: 100  # AC-015-002: 100ms timeout
      rules:
        - pattern: "\\b\\d{3}-\\d{2}-\\d{4}\\b"
          type: "SSN"
          severity: high
        - pattern: "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b"
          type: "email"
          severity: medium
        - pattern: "\\b\\d{16}\\b"
          type: "credit_card"
          severity: high

    secrets_detection:
      name: "Secrets Detection"
      description: "Detect API keys, tokens, passwords"
      mode: block
      timeout_ms: 100
      rules:
        - pattern: "(sk-[a-zA-Z0-9]{48}|sk-proj-[a-zA-Z0-9-_]{100,})"
          type: "openai_api_key"
          severity: critical
        - pattern: "ghp_[a-zA-Z0-9]{36}"
          type: "github_pat"
          severity: critical
        - pattern: "AKIA[0-9A-Z]{16}"
          type: "aws_access_key"
          severity: critical

    format_validation:
      name: "Format Validation"
      description: "Validate ID formats from agent guardrails"
      mode: warn
      timeout_ms: 50
      rules:
        - pattern: "^PROJ-\\d{3}$"
          type: "project_id"
          applies_to: ["nse-*", "ps-*"]
        - pattern: "^e-\\d+$"
          type: "entry_id"
          applies_to: ["*"]
        - pattern: "^[a-z]+-\\d+(\\.\\d+)?$"
          type: "ps_id"
          applies_to: ["ps-*"]

  # Output Filtering Patterns
  output:
    no_secrets_in_output:
      name: "No Secrets in Output"
      description: "Filter secrets from agent outputs"
      mode: block
      timeout_ms: 100
      rules:
        - pattern: "(password|secret|token|api_key)\\s*[:=]\\s*['\"][^'\"]+['\"]"
          type: "inline_secret"
          action: redact
          replacement: "[REDACTED]"

    no_executable_code:
      name: "No Executable Code Without Confirmation"
      description: "Warn on executable code in outputs"
      mode: warn
      timeout_ms: 100
      rules:
        - pattern: "```(bash|sh|python).*\\n.*\\b(rm|del|chmod|chown)\\b"
          type: "destructive_command"

# Tool-specific overrides
tool_rules:
  Write:
    patterns: ["secrets_detection", "format_validation"]
    fallback: block
  Edit:
    patterns: ["secrets_detection"]
    fallback: block
  Bash:
    patterns: ["secrets_detection", "pii_detection"]
    fallback: warn
  Task:
    patterns: ["format_validation"]
    fallback: warn
```

### Hook Interface

```python
# Updated pre_tool_use.py interface
class GuardrailResult:
    decision: Literal["approve", "block", "warn", "ask"]
    reason: str
    pattern_matches: list[PatternMatch]
    elapsed_ms: float

def validate_tool_input(
    tool_name: str,
    tool_input: dict,
    patterns: PatternLibrary,
    timeout_ms: int = 100,
    mode: str = "warn"
) -> GuardrailResult:
    """
    Validate tool input against pattern library.

    Args:
        tool_name: Name of the tool being called
        tool_input: Tool input parameters
        patterns: Loaded pattern library
        timeout_ms: Validation timeout (AC-015-002)
        mode: Default mode if not specified in pattern (AC-015-003)

    Returns:
        GuardrailResult with decision and matches
    """
```

### Async Validation (AC-015-001)

The hook subprocess model already provides async validation:
- Claude Code spawns hook as subprocess
- Hook has configurable timeout (settings.json)
- Non-blocking to main context

**Timeout Configuration:**
```json
// .claude/settings.json
{
  "hooks": {
    "PreToolUse": [{
      "timeout": 100  // AC-015-002: 100ms
    }]
  }
}
```

### Warn Mode (AC-015-003)

```python
def handle_match(match: PatternMatch, mode: str) -> GuardrailResult:
    if mode == "warn":
        # Log warning to stderr (visible in hook output)
        log_warning(match)
        return GuardrailResult(decision="approve", ...)
    elif mode == "block":
        return GuardrailResult(decision="block", ...)
    elif mode == "ask":
        return GuardrailResult(decision="ask", ...)
```

---

## Implementation Plan

### Phase 1: Pattern Library (T-015.2, T-015.3)

1. Create `patterns.yaml` with initial patterns
2. Create `schema.json` for validation
3. Implement pattern loader in Python

### Phase 2: Hook Extension (T-015.4)

1. Extend `pre_tool_use.py` to load patterns
2. Implement async validation with timeout
3. Implement warn mode (log but approve)
4. Create `post_tool_use.py` for output filtering

### Phase 3: Testing (T-015.5)

1. Unit tests for pattern matching
2. Integration tests for hook execution
3. BDD scenarios for guardrail behavior

---

## Acceptance Criteria Mapping

| AC | Criterion | Design Solution |
|----|-----------|-----------------|
| AC-015-001 | Async validation (non-blocking) | Subprocess model (inherent) |
| AC-015-002 | timeout_ms: 100 | Hook config + pattern config |
| AC-015-003 | mode: warn (don't block, just log) | GuardrailResult with warn decision |
| AC-015-004 | Pattern library for common checks | patterns.yaml with PII, secrets, formats |

---

## File Changes

| File | Action | Purpose |
|------|--------|---------|
| `.claude/hooks/patterns/patterns.yaml` | CREATE | Pattern library |
| `.claude/hooks/patterns/schema.json` | CREATE | JSON Schema |
| `.claude/hooks/pre_tool_use.py` | MODIFY | Add pattern loading |
| `.claude/hooks/post_tool_use.py` | CREATE | Output filtering |
| `.claude/settings.json` | MODIFY | Add PostToolUse hook |

---

## References

- **Source:** `.claude/hooks/pre_tool_use.py` (existing implementation)
- **Source:** `.claude/settings.json` (hook configuration)
- **Research:** Explore agent output on Claude Code hook types
- **Prior Art:** DISC-015-001 (22 agent files have guardrails sections)

---

*Design Document v1.0.0*
*Task: T-015.1*
