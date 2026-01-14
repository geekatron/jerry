# PROJ-005-e-007: Claude Code Plugin Script Patterns and Constraints

**PS ID:** PROJ-005
**Entry ID:** e-007
**Date:** 2025-01-13
**Author:** ps-researcher
**Topic:** Claude Code Plugin Script Patterns and Constraints

---

## L0: Executive Summary

This research documents best practices and patterns for writing standalone plugin hook scripts for Claude Code. Key findings:

1. **Exit Codes Matter**: Scripts must use specific exit codes (0=success/allow, 1=block/deny, 2=error)
2. **JSON I/O Protocol**: All input via stdin as JSON, all output via stdout as JSON
3. **Graceful Degradation**: Pattern library failures should warn, not block operations
4. **Timeout Awareness**: Default timeout is 100ms for validation; scripts must be fast
5. **Error Isolation**: Hook errors should never crash Claude Code; always return valid JSON

Three "safe" exemplar scripts demonstrate these patterns:
- `scripts/pre_tool_use.py` (308 lines) - Pre-execution security validation
- `scripts/subagent_stop.py` (202 lines) - Agent handoff orchestration
- `scripts/post_tool_use.py` (230 lines) - Output filtering and redaction

---

## L1: Technical Details

### 1. Pattern Catalog from Safe Scripts

#### Pattern P-001: Shebang and Module Docstring

```python
#!/usr/bin/env python3
"""
Hook Name - Purpose Description

Reference: https://docs.anthropic.com/en/docs/claude-code/hooks

Exit Codes:
    0 - Success/Allow operation
    1 - Block/Deny operation
    2 - Error in hook execution
"""
```

**Source:** All three exemplar scripts (lines 1-21)

#### Pattern P-002: Minimal Stdlib Imports

```python
import json
import os
import sys
from pathlib import Path
from typing import Any
```

**Rationale:** Minimize dependencies to ensure scripts work in any environment. No third-party packages required for core functionality.

**Source:** `pre_tool_use.py` lines 23-27

#### Pattern P-003: Graceful Import Fallback

```python
try:
    from patterns import PatternLibrary, load_patterns
    PATTERNS_AVAILABLE = True
except ImportError:
    # Fallback: try absolute import
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from patterns import PatternLibrary, load_patterns
        PATTERNS_AVAILABLE = True
    except ImportError:
        PATTERNS_AVAILABLE = False
        PatternLibrary = None  # type: ignore
```

**Rationale:** Pattern library is optional enhancement; script must work without it.

**Source:** `pre_tool_use.py` lines 29-44, `post_tool_use.py` lines 28-42

#### Pattern P-004: Lazy Singleton Loading

```python
_patterns: PatternLibrary | None = None

def get_patterns() -> PatternLibrary | None:
    """Get cached pattern library instance."""
    global _patterns
    if _patterns is None and PATTERNS_AVAILABLE:
        try:
            _patterns = load_patterns()
        except Exception:
            pass  # Fall back to rule-based checks only
    return _patterns
```

**Rationale:** Load patterns once at first use for performance; catch all exceptions to prevent crashes.

**Source:** `pre_tool_use.py` lines 51-62

#### Pattern P-005: Configuration as Module Constants

```python
BLOCKED_WRITE_PATHS = [
    "~/.ssh",
    "~/.gnupg",
    "~/.aws",
    "/etc",
    "/var",
]

DANGEROUS_COMMANDS = [
    "rm -rf /",
    "chmod 777",
    "curl | bash",
]
```

**Rationale:** Configuration at module level for easy auditing and modification.

**Source:** `pre_tool_use.py` lines 70-106

#### Pattern P-006: Validation Functions Return Tuples

```python
def check_file_write(tool_input: dict[str, Any]) -> tuple[bool, str]:
    """Check if a file write operation is safe."""
    file_path = tool_input.get("file_path", "")

    # Validation logic...
    if some_condition:
        return False, "Reason for blocking"

    return True, ""
```

**Rationale:** Consistent return format (allowed: bool, reason: str) enables composable validation.

**Source:** `pre_tool_use.py` lines 114-136

#### Pattern P-007: Main Function with JSON Protocol

```python
def main() -> int:
    """Main hook entry point."""
    try:
        # Read hook input from stdin
        input_data = json.loads(sys.stdin.read())

        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        # Validation logic...

        # Output decision as JSON
        print(json.dumps({"decision": "approve"}))
        return 0

    except json.JSONDecodeError as e:
        print(json.dumps({"decision": "block", "reason": f"Invalid JSON - {e}"}))
        return 2
    except Exception as e:
        print(json.dumps({"decision": "block", "reason": f"Hook error: {e}"}))
        return 2
```

**Rationale:** All errors must produce valid JSON output; never crash without output.

**Source:** `pre_tool_use.py` lines 236-305

#### Pattern P-008: Entry Point Guard

```python
if __name__ == "__main__":
    sys.exit(main())
```

**Rationale:** Enables both direct execution and module import; returns exit code to shell.

**Source:** All scripts

#### Pattern P-009: Stderr for Warnings, Stdout for Decisions

```python
# Warning (doesn't affect decision)
print(
    json.dumps({"warning": "Piping to shell detected"}),
    file=sys.stderr,
)

# Decision (Claude reads this)
print(json.dumps({"decision": "approve"}))
```

**Rationale:** Claude reads stdout for decisions; stderr is for logging/debugging.

**Source:** `pre_tool_use.py` lines 163-166, 278-282

#### Pattern P-010: Phase-Based Validation Architecture

```python
def main() -> int:
    # PHASE 1: Rule-based security checks (fast, hardcoded)
    allowed, reason = check_file_write(tool_input)
    if not allowed:
        print(json.dumps({"decision": "block", "reason": reason}))
        return 0

    # PHASE 2: Pattern-based validation (extensible)
    pattern_decision, pattern_reason, matches = check_patterns(tool_name, tool_input)
    if pattern_decision == "block":
        print(json.dumps({"decision": "block", "reason": pattern_reason}))
        return 0

    # PHASE 3: Approve if all checks pass
    print(json.dumps({"decision": "approve"}))
    return 0
```

**Rationale:** Fast hardcoded rules first, then extensible patterns; fail-fast on block.

**Source:** `pre_tool_use.py` lines 245-298

---

### 2. Claude Code Hook Requirements (from Context7)

#### Input Format (stdin JSON)

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.txt",
  "cwd": "/current/working/dir",
  "permission_mode": "ask|allow",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {"file_path": "/path/to/file", "content": "..."}
}
```

**Source:** Context7 `/anthropics/claude-code` - Hook Input Format

#### Output Format (stdout JSON)

```json
{
  "continue": true,
  "suppressOutput": false,
  "systemMessage": "Message for Claude",
  "decision": "approve|block|warn|ask"
}
```

**Source:** Context7 `/anthropics/claude-code` - Standard Hook Output Format

#### Exit Codes

| Code | Meaning | Claude Behavior |
|------|---------|-----------------|
| 0 | Success | Read stdout JSON for decision |
| 1 | Block/Deny | Operation blocked |
| 2 | Error | Hook error, may continue or abort |

**Source:** Context7 `/anthropics/claude-code` - Validate Hook Input

#### Timeout Configuration

```json
{
  "type": "command",
  "command": "python3 script.py",
  "timeout": 10
}
```

- Default: 60s for command hooks, 30s for prompt hooks
- Jerry uses: 5000ms (5s) for PreToolUse, 10000ms (10s) for SessionStart

**Source:** Context7, `hooks/hooks.json`

---

### 3. Pattern Library Architecture

#### Directory Structure

```
scripts/patterns/
├── __init__.py        # Public API exports
├── loader.py          # PatternLibrary class (517 lines)
├── patterns.json      # JSON format patterns
├── patterns.yaml      # YAML format patterns (primary)
└── schema.json        # JSON Schema for validation
```

#### Key Classes

```python
@dataclass
class PatternMatch:
    rule_id: str
    pattern_group: str
    description: str
    severity: str
    matched_text: str
    start_pos: int
    end_pos: int

@dataclass
class ValidationResult:
    decision: Literal["approve", "block", "warn", "ask"]
    reason: str
    matches: list[PatternMatch]
    elapsed_ms: float

class PatternLibrary:
    def validate_input(tool_name, tool_input) -> ValidationResult
    def validate_output(tool_name, output) -> ValidationResult
```

**Source:** `scripts/patterns/loader.py`

#### Pattern Types

| Type | Purpose | Default Mode |
|------|---------|--------------|
| `pii_detection` | PII in inputs (SSN, email, phone) | warn |
| `secrets_detection` | API keys, tokens, passwords | block |
| `format_validation` | ID format validation | warn |
| `no_secrets_in_output` | Secrets in outputs | block (redact) |
| `executable_code_warning` | Destructive commands in outputs | warn |

**Source:** `scripts/patterns/patterns.yaml`

---

### 4. Constraint Checklist

#### MUST Do

- [x] Use `#!/usr/bin/env python3` shebang
- [x] Read all input from stdin as JSON
- [x] Write decision to stdout as JSON
- [x] Return exit code 0 for success, 2 for errors
- [x] Handle `json.JSONDecodeError` explicitly
- [x] Handle all exceptions with valid JSON output
- [x] Use `sys.exit(main())` pattern
- [x] Provide module docstring with exit codes
- [x] Use type hints on public functions

#### MUST NOT Do

- [x] Crash without producing JSON output
- [x] Use print() for non-JSON output to stdout
- [x] Import heavy dependencies unconditionally
- [x] Block indefinitely (respect timeouts)
- [x] Modify global state that affects other hooks
- [x] Write to files without error handling

#### SHOULD Do

- [x] Use lazy loading for optional dependencies
- [x] Log warnings to stderr, not stdout
- [x] Implement phase-based validation (fast rules first)
- [x] Cache expensive computations (pattern library)
- [x] Use configuration constants at module level
- [x] Return tuple (allowed, reason) from validation functions
- [x] Use `tool_input.get("key", default)` for safe access

#### SHOULD NOT Do

- [x] Perform network I/O in validation hooks
- [x] Run subprocesses unless necessary
- [x] Use global variables for state
- [x] Hard-code paths that vary by environment

---

### 5. Error Handling Strategy

#### Principle: Graceful Degradation

All errors should degrade to a safe state (usually "approve" or "warn"), not crash:

```python
try:
    result = patterns.validate_input(tool_name, tool_input)
except Exception as e:
    # Pattern validation failure should not block operations
    print(
        json.dumps({"warning": f"Pattern validation error: {e}", "fallback": "approve"}),
        file=sys.stderr,
    )
    return "approve", "", []
```

**Source:** `pre_tool_use.py` lines 226-233

#### Fallback Safety Net

Even when pattern library fails, inline patterns provide baseline protection:

```python
INLINE_REDACTION_PATTERNS = [
    (re.compile(r"Bearer\s+[A-Za-z0-9-_.]+", re.IGNORECASE), "[BEARER_TOKEN_REDACTED]"),
    (re.compile(r"sk-[a-zA-Z0-9]{20,}"), "[API_KEY_REDACTED]"),
    (re.compile(r"ghp_[a-zA-Z0-9]{36}"), "[GITHUB_TOKEN_REDACTED]"),
]
```

**Source:** `post_tool_use.py` lines 140-147

---

### 6. Code Structure Template

```python
#!/usr/bin/env python3
"""
{Hook Name} - {Purpose}

Reference: https://docs.anthropic.com/en/docs/claude-code/hooks

Exit Codes:
    0 - {Success behavior}
    1 - {Block behavior}
    2 - Error in hook execution
"""

import json
import sys
from pathlib import Path
from typing import Any

# =============================================================================
# OPTIONAL IMPORTS (Graceful fallback)
# =============================================================================

try:
    from patterns import PatternLibrary, load_patterns
    PATTERNS_AVAILABLE = True
except ImportError:
    PATTERNS_AVAILABLE = False
    PatternLibrary = None  # type: ignore

# =============================================================================
# CONFIGURATION
# =============================================================================

BLOCKED_ITEMS = [
    # Configuration constants
]

# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_something(tool_input: dict[str, Any]) -> tuple[bool, str]:
    """Validate {what}. Returns (allowed, reason)."""
    # Implementation
    return True, ""

# =============================================================================
# MAIN HOOK LOGIC
# =============================================================================

def main() -> int:
    """Main hook entry point."""
    try:
        # Read input
        input_data = json.loads(sys.stdin.read())
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        # Phase 1: Fast rule-based checks
        allowed, reason = validate_something(tool_input)
        if not allowed:
            print(json.dumps({"decision": "block", "reason": reason}))
            return 0

        # Phase 2: Pattern-based checks (if available)
        # ...

        # Success
        print(json.dumps({"decision": "approve"}))
        return 0

    except json.JSONDecodeError as e:
        print(json.dumps({"decision": "block", "reason": f"Invalid JSON: {e}"}))
        return 2
    except Exception as e:
        print(json.dumps({"decision": "block", "reason": f"Hook error: {e}"}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
```

---

## L2: Strategic Implications

### 1. Plugin Reliability

The pattern library approach (with fallback to inline patterns) ensures hooks remain functional even when:
- PyYAML is not installed
- Pattern files are missing or corrupted
- Pattern validation times out

This aligns with the Jerry principle of **graceful degradation**.

### 2. Security Posture

The two-phase validation (hardcoded rules + extensible patterns) provides:
- **Defense in depth**: Multiple layers of security checks
- **Auditability**: Hardcoded rules are easy to review
- **Extensibility**: Pattern library can be updated without code changes

### 3. Performance Considerations

Key performance patterns:
- Lazy loading of pattern library (only when needed)
- Singleton caching (load once, use many times)
- 100ms timeout for pattern validation
- Fast rule-based checks before expensive pattern matching

### 4. Recommended Improvements

Based on this research, consider:

1. **Add health check endpoint**: Allow hooks to report their status
2. **Structured logging**: Use structured JSON logs for better debugging
3. **Metrics collection**: Track validation times and match counts
4. **Unit tests**: Add pytest tests for each validation function

---

## References

### Primary Sources (Codebase)

| File | Lines | Purpose |
|------|-------|---------|
| `scripts/pre_tool_use.py` | 308 | Pre-tool security validation |
| `scripts/subagent_stop.py` | 202 | Subagent handoff orchestration |
| `scripts/post_tool_use.py` | 230 | Output filtering and redaction |
| `scripts/patterns/loader.py` | 517 | Pattern library implementation |
| `scripts/patterns/patterns.yaml` | 279 | Pattern definitions |
| `scripts/patterns/schema.json` | 212 | Pattern schema |
| `hooks/hooks.json` | 41 | Hook configuration |

### External Sources (Context7)

| Library ID | Topic |
|------------|-------|
| `/anthropics/claude-code` | Official Claude Code documentation |
| `/davila7/claude-code-templates` | Community hook examples |

### Related Documents

- Anthropic Hooks Documentation: https://docs.anthropic.com/en/docs/claude-code/hooks
- OWASP Validation Regex Repository: https://owasp.org/www-community/OWASP_Validation_Regex_Repository
- TruffleHog Regex Patterns: https://github.com/dxa4481/truffleHogRegexes

---

## Appendix: Quick Reference Card

### Hook Types

| Hook | When | Input Fields |
|------|------|--------------|
| `SessionStart` | Session begins | `session_id`, `cwd` |
| `PreToolUse` | Before tool | `tool_name`, `tool_input` |
| `PostToolUse` | After tool | `tool_name`, `tool_output` |
| `Stop` | Claude stops | `reason` |
| `SubagentStop` | Subagent stops | `agent_name`, `output` |

### Decision Values

| Value | Effect |
|-------|--------|
| `approve` | Allow operation |
| `block` | Deny operation |
| `warn` | Log warning, allow |
| `ask` | Prompt user |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Block/Deny |
| 2 | Error |
