# ADR-150-001: Pre-Tool Enforcement Pipeline Consolidation

## Document Sections

| Section | Purpose |
|---------|---------|
| [Status](#status) | Decision status |
| [Context](#context) | Problem statement and current state |
| [Decision](#decision) | Chosen architecture |
| [Component Diagram](#component-diagram) | Text-based component topology |
| [Interface Definitions](#interface-definitions) | Port protocols and value objects |
| [File Locations](#file-locations) | New and modified files |
| [Composition Strategy](#composition-strategy) | How engines compose in the handler |
| [Output Format Specification](#output-format-specification) | Canonical hook response format |
| [Threat Model](#threat-model) | STRIDE analysis of the enforcement pipeline |
| [Consequences](#consequences) | Trade-offs and implications |

---

## Status

**Accepted and Implemented** -- 2026-03-10

**As-built deviations from original design:**
- `YamlPatternLibraryAdapter` → implemented as `PatternLibraryAdapter` (simpler name)
- `security_check_result.py`, `ipattern_library.py`, `pattern_validation_result.py` → dataclasses inlined into `pattern_library_adapter.py` and engine (fewer files, same interfaces)
- `security_engine` handler parameter → `Optional` for backward compatibility during migration
- `current_platform` field → removed (Windows enforcement out of scope; Jerry targets macOS/Linux)

---

## Context

Issue #150 requires consolidating two independent pre-tool-use enforcement
paths into a single pipeline.

### Current State: Two Divergent Paths

**Path A -- CLI Handler** (`src/interface/cli/hooks/hooks_pre_tool_use_handler.py`):
Invoked via `jerry hooks pre-tool-use`. Delegates to `PreToolEnforcementEngine`
for AST-based architecture validation (V-038 import boundaries, V-041
one-class-per-file) and `StalenessDetector` for ORCHESTRATION.yaml freshness.
Composed in `bootstrap.py`. Response format: `{"decision": "block", "reason": "..."}`.

**Path B -- Standalone Script** (`scripts/pre_tool_use.py`):
Invoked directly as a subprocess via the Claude Code hooks configuration.
Contains 18 security checks in 4 categories plus pattern-based validation
from `scripts/patterns/patterns.yaml`. Response format:
`{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", ...}}`.

### Problems

1. **Dual invocation**: Two independent entry points, only one runs depending on
   hook configuration. Currently `settings.json` has no hooks configured (they
   were in the backup), so neither security path runs.

2. **Incompatible output formats**: Path A uses `{"decision": "block"}`. Path B
   uses `{"hookSpecificOutput": {"permissionDecision": "deny"}}`. Only one can
   be correct for the Claude Code hook protocol.

3. **No domain separation**: Path B's security rules (blocked paths, dangerous
   commands, PII detection) are hardcoded in a script with no testable interfaces.

4. **Pattern library stranded**: `scripts/patterns/` uses `sys.path` hacking and
   a fallback YAML parser. Not importable from `src/`.

### Constraints

- H-07: Domain layer cannot import infrastructure.
- H-10: One class per file.
- Fail-open semantics: hook failures must never block all tool use.
- Every check must be unit-testable with injectable dependencies.
- Pattern library must accept injected patterns (for test mocking).

---

## Decision

**Create a new `SecurityEnforcementEngine` composed alongside the existing
`PreToolEnforcementEngine` in the handler. Do NOT extend the existing engine.**

Rationale for separate engines rather than extending:

1. **Single Responsibility**: The existing engine is an AST parser for
   architecture rules. Security checks are regex/string matching on tool
   inputs. Different concerns, different implementation strategies, different
   failure modes.

2. **Independent failure domains**: If AST parsing crashes, security checks
   still run. If pattern loading fails, architecture checks still run. Extending
   one engine creates a shared failure boundary.

3. **Testability**: Two focused engines with narrow interfaces are easier to
   test exhaustively than one engine with 20+ check methods.

### Domain Placement Decision

Security rules ARE domain rules -- they express "what is forbidden" independent
of how the hook protocol works or how patterns are loaded from disk. Per H-07:

- **Domain layer** (`src/domain/`): Security rule definitions (blocked paths,
  dangerous commands, sensitive patterns) as pure data and a port protocol for
  pattern loading.

- **Infrastructure layer** (`src/infrastructure/`): The `SecurityEnforcementEngine`
  that implements the check orchestration, plus the `PatternLibraryAdapter` that
  loads patterns from YAML files.

- **Interface layer** (`src/interface/`): The CLI handler that composes both
  engines and translates results into the hook response format.

This placement deviates from the existing `PreToolEnforcementEngine` which
lives entirely in `src/infrastructure/internal/enforcement/`. That engine's
rules (`enforcement_rules.py`) are also infrastructure-level constants. The
deviation is justified: the existing engine's rules are tightly coupled to
AST parsing mechanics (layer names, file extensions, directory paths for
AST enforcement). Security rules are business-domain concepts (PII must not
leak, credentials must not be written) that should survive an infrastructure
replacement.

However, pragmatism overrides purity here. Given:
- The existing engine and its rules already live in `infrastructure/internal/enforcement/`
- Moving only security rules to domain while leaving architecture rules in
  infrastructure creates inconsistency
- The `domain/` layer currently contains only `markdown_ast/` -- no enforcement concepts
- The security rules reference infrastructure concerns (file paths, OS platform checks)

**Pragmatic decision**: Place the `SecurityEnforcementEngine` and its rules
in `src/infrastructure/internal/enforcement/` alongside the existing engine.
Define a `PatternLibraryPort` protocol in `src/application/ports/secondary/`
to keep the pattern loading injectable. This matches the existing codebase
pattern where `IReadModelStore` (an application-layer port) abstracts
infrastructure storage.

---

## Component Diagram

```
                    Claude Code Hook Protocol (stdin JSON)
                                |
                                v
          +---------------------------------------------+
          |  HooksPreToolUseHandler                     |
          |  (src/interface/cli/hooks/)                 |
          |                                             |
          |  Reads stdin, dispatches to engines,        |
          |  merges results, emits canonical response   |
          +-----+----------+----------+----------------+
                |          |          |
                v          v          v
     +----------+--+ +----+------+ +-+----------------+
     | Security    | | PreTool   | | Staleness        |
     | Enforcement | | Enforce-  | | Detector         |
     | Engine      | | ment      | | (existing)       |
     | (NEW)       | | Engine    | |                  |
     |             | | (existing)| |                  |
     +------+------+ +-----+----+ +------------------+
            |               |
            v               v
     +------+------+ +-----+----+
     | security    | | enforce- |
     | rules.py    | | ment     |
     | (NEW)       | | rules.py |
     | + patterns  | | (exist.) |
     +------+------+ +----------+
            |
            v
     +------+------+
     | IPattern    |  <-- application port (Protocol)
     | Library     |
     +------+------+
            ^
            |  implements
     +------+------+
     | YamlPattern |  <-- infrastructure adapter
     | Library     |
     | Adapter     |
     +-------------+
            |
            v
     +------+------+
     | patterns    |
     | .yaml       |
     +-------------+
```

### Pipeline Execution Order

```
1. Parse stdin JSON                           (handler)
2. Security enforcement                       (SecurityEnforcementEngine)
   a. File write checks (blocked paths, sensitive files)
   b. Bash command checks (cd blocking, dangerous rm, dangerous commands)
   c. Git operation checks (force push blocking)
   d. Pattern-based validation (PII, secrets from PatternLibrary)
3. Architecture enforcement                   (PreToolEnforcementEngine)
   a. V-038 import boundary validation
   b. V-041 one-class-per-file
   c. Governance escalation detection
4. Staleness detection                        (StalenessDetector)
5. Merge results, emit canonical response     (handler)
```

**Why security first**: Security checks are cheaper (string/regex matching,
no file I/O beyond pattern loading at init) and higher priority (a write to
`~/.ssh` should be blocked before we spend time parsing AST). Early termination
on security block avoids unnecessary work.

---

## Interface Definitions

### Port: IPatternLibrary

```python
# src/application/ports/secondary/ipattern_library.py

from typing import Protocol, runtime_checkable


@runtime_checkable
class IPatternLibrary(Protocol):
    """Port for loading and validating against security patterns.

    Abstracts the pattern storage mechanism (YAML, JSON, in-memory)
    from the enforcement engine that uses patterns for validation.
    """

    def validate_tool_input(
        self,
        tool_name: str,
        tool_input: dict[str, Any],
    ) -> PatternValidationResult:
        """Validate tool input against loaded patterns.

        Args:
            tool_name: Claude Code tool name (Write, Edit, Bash, etc.)
            tool_input: Tool input parameters dict.

        Returns:
            Validation result with decision, reason, and matches.
        """
        ...
```

### Value Object: SecurityCheckResult

```python
# src/infrastructure/internal/enforcement/security_check_result.py


@dataclass(frozen=True)
class SecurityCheckResult:
    """Result of a single security check category.

    Attributes:
        passed: Whether the check passed (True) or failed (False).
        reason: Human-readable explanation when failed.
        category: Which check category produced this result.
        severity: "block", "warn", or "approve".
    """

    passed: bool
    reason: str
    category: str  # "file_write", "bash_command", "git_operation", "pattern"
    severity: str  # "block", "warn", "approve"
```

### Value Object: PatternValidationResult

```python
# src/infrastructure/internal/enforcement/pattern_validation_result.py


@dataclass(frozen=True)
class PatternValidationResult:
    """Result of pattern-based validation.

    Attributes:
        decision: "approve", "block", "warn", or "ask".
        reason: Aggregated reason string.
        matches: Individual pattern matches for logging.
    """

    decision: str
    reason: str
    matches: list[PatternMatch] = field(default_factory=list)
```

### Engine: SecurityEnforcementEngine

```python
# src/infrastructure/internal/enforcement/security_enforcement_engine.py


class SecurityEnforcementEngine:
    """Security enforcement engine for pre-tool-use validation.

    Evaluates tool inputs against security rules: blocked paths,
    dangerous commands, sensitive files, git safety, and pattern-based
    detection (PII, secrets).

    Fail-open by design: any internal error results in approval.

    Args:
        pattern_library: Injectable pattern library for PII/secrets
            detection. If None, pattern checks are skipped.
        security_rules: Injectable security rules configuration.
            If None, uses default rules from security_rules.py.
    """

    def __init__(
        self,
        pattern_library: IPatternLibrary | None = None,
        security_rules: SecurityRules | None = None,
    ) -> None: ...

    def evaluate(
        self,
        tool_name: str,
        tool_input: dict[str, Any],
    ) -> EnforcementDecision:
        """Evaluate a tool use request against security rules.

        Runs applicable checks based on tool_name. Returns the
        highest-severity result across all checks.

        Args:
            tool_name: Claude Code tool name.
            tool_input: Tool input parameters.

        Returns:
            EnforcementDecision with action, reason, violations.
        """
        ...
```

### Data: SecurityRules

```python
# src/infrastructure/internal/enforcement/security_rules.py


@dataclass(frozen=True)
class SecurityRules:
    """Static security rule definitions.

    All fields are immutable frozen collections. Injectable for testing.
    Default values match the production rules from scripts/pre_tool_use.py.
    """

    blocked_write_paths: tuple[str, ...]
    sensitive_file_patterns: tuple[str, ...]
    dangerous_commands: tuple[str, ...]
    platform: str  # "darwin", "win32", "linux"
```

---

## File Locations

### New Files

| File | Layer | Purpose |
|------|-------|---------|
| `src/application/ports/secondary/ipattern_library.py` | Application | Port protocol for pattern library |
| `src/infrastructure/internal/enforcement/security_enforcement_engine.py` | Infrastructure | Security check orchestration |
| `src/infrastructure/internal/enforcement/security_rules.py` | Infrastructure | Static security rule definitions (blocked paths, dangerous commands, sensitive files) |
| `src/infrastructure/internal/enforcement/security_check_result.py` | Infrastructure | Value object for individual check results |
| `src/infrastructure/internal/enforcement/pattern_validation_result.py` | Infrastructure | Value object for pattern validation results |
| `src/infrastructure/internal/enforcement/yaml_pattern_library_adapter.py` | Infrastructure | IPatternLibrary implementation that loads from YAML |
| `tests/unit/infrastructure/enforcement/test_security_enforcement_engine.py` | Tests | Unit tests for security engine |
| `tests/unit/infrastructure/enforcement/test_security_rules.py` | Tests | Unit tests for rule matching logic |
| `tests/unit/infrastructure/enforcement/test_yaml_pattern_library_adapter.py` | Tests | Unit tests for pattern loading |

### Modified Files

| File | Change |
|------|--------|
| `src/interface/cli/hooks/hooks_pre_tool_use_handler.py` | Add SecurityEnforcementEngine as third injected dependency. Expand `_WRITE_TOOLS` and `_EDIT_TOOLS` sets to include Bash. Add `_run_security_enforcement()` method. Merge security and architecture decisions. |
| `src/bootstrap.py` | Wire SecurityEnforcementEngine with YamlPatternLibraryAdapter into HooksPreToolUseHandler. |
| `src/infrastructure/internal/enforcement/__init__.py` | Export new classes. |
| `src/application/ports/__init__.py` | Export IPatternLibrary. |

### Files to Deprecate (Not Delete Yet)

| File | Reason |
|------|--------|
| `scripts/pre_tool_use.py` | Replaced by consolidated pipeline. Keep until hook config migration is verified. |
| `scripts/patterns/loader.py` | Replaced by `yaml_pattern_library_adapter.py`. Keep `PatternLibrary` class temporarily for backward compat. |
| `scripts/patterns/__init__.py` | Same as above. |

### Files Unchanged

| File | Reason |
|------|--------|
| `scripts/patterns/patterns.yaml` | Stays in place. The `YamlPatternLibraryAdapter` reads from a configurable path; default points here. Future migration to `src/infrastructure/` is optional. |
| `src/infrastructure/internal/enforcement/pre_tool_enforcement_engine.py` | No changes. Stays focused on AST enforcement. |
| `src/infrastructure/internal/enforcement/enforcement_decision.py` | Reused as-is by both engines. |
| `src/infrastructure/internal/enforcement/enforcement_rules.py` | No changes. Architecture rules stay separate from security rules. |

---

## Composition Strategy

### Handler Constructor Signature (After)

```python
class HooksPreToolUseHandler:
    def __init__(
        self,
        enforcement_engine: PreToolEnforcementEngine,
        security_engine: SecurityEnforcementEngine,
        staleness_detector: StalenessDetector,
    ) -> None: ...
```

### Pipeline Execution in handle()

```python
def handle(self, stdin_json: str) -> int:
    response: dict[str, Any] = {}

    # Step 0: Parse hook input (fail-open)
    hook_data = self._parse_input(stdin_json)
    tool_name = hook_data.get("tool_name", "")
    tool_input = hook_data.get("tool_input", {})

    # Step 1: Security enforcement (fail-open, runs first)
    #         Cheap checks. Early termination on block.
    try:
        security_decision = self._security_engine.evaluate(tool_name, tool_input)
        if security_decision.action == "block":
            return self._emit_block(security_decision)
    except Exception:
        pass  # fail-open

    # Step 2: Architecture enforcement (fail-open)
    #         AST parsing. Only for Write/Edit tools.
    try:
        arch_decision = self._run_enforcement(tool_name, tool_input)
        if arch_decision and arch_decision.action == "block":
            return self._emit_block(arch_decision)
    except Exception:
        pass  # fail-open

    # Step 3: Staleness detection (fail-open)
    #         Only if no block decision yet.
    try:
        self._check_staleness(tool_input, response)
    except Exception:
        pass  # fail-open

    # Step 4: Merge warnings from all steps
    #         Collect warn-level decisions from security + arch.
    self._merge_warnings(response, security_decision, arch_decision)

    # Step 5: Emit canonical response
    print(json.dumps(response))
    return 0
```

### Fail-Open Guarantees

Every engine call is independently wrapped in `try/except Exception`. The handler
guarantees:

1. **Exit code 0 always** -- Claude Code expects exit 0; non-zero kills the session.
2. **Valid JSON always** -- Even if all engines crash, `{}` is emitted (passthrough).
3. **No shared failure boundary** -- Security, architecture, and staleness are
   independent try blocks. One crash does not prevent the others from running.
4. **No cascading blocks** -- A security `warn` does not promote to `block` when
   combined with an architecture `warn`. Each engine makes its own decision
   independently; only explicit `block` decisions terminate the pipeline.

### Bootstrap Wiring

```python
# In bootstrap.py _build_hooks_handlers():

from src.infrastructure.internal.enforcement.security_enforcement_engine import (
    SecurityEnforcementEngine,
)
from src.infrastructure.internal.enforcement.yaml_pattern_library_adapter import (
    YamlPatternLibraryAdapter,
)

# Pattern library: load once, inject into engine
pattern_library = YamlPatternLibraryAdapter(
    patterns_path=project_root / "scripts" / "patterns" / "patterns.yaml"
)

security_engine = SecurityEnforcementEngine(
    pattern_library=pattern_library,
)

"pre-tool-use": HooksPreToolUseHandler(
    enforcement_engine=pre_tool_engine,
    security_engine=security_engine,
    staleness_detector=staleness_detector,
),
```

---

## Output Format Specification

### Problem: Two Incompatible Formats

**Path A (CLI handler)**: `{"decision": "block", "reason": "..."}`
**Path B (standalone script)**: `{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny"}}`

### Resolution

The Claude Code hook protocol accepts both formats, but the simpler format is
canonical per the Claude Code hooks documentation:

```json
// BLOCK
{"decision": "block", "reason": "Writing to ~/.ssh is blocked for security"}

// WARN (non-blocking)
{"decision": "warn", "reason": "Governance file modification: .context/rules/..."}

// APPROVE (passthrough)
{}
```

The `hookSpecificOutput` envelope from Path B is a legacy format from an
earlier Claude Code version. The consolidated pipeline uses the simpler format
that Path A already uses.

### Canonical Response Schema

```json
{
  "decision": "block" | "warn",           // omitted for approve
  "reason": "human-readable explanation",  // omitted for approve
  "violations": ["violation 1", "..."],    // optional, for architecture violations
  "criticality_escalation": "C3" | "C4",  // optional, for governance files
  "staleness_warning": "...",              // optional, for ORCHESTRATION.yaml
  "security_matches": [                    // optional, for pattern matches
    {"rule_id": "secret-openai", "severity": "critical", "description": "..."}
  ]
}
```

Approve is an empty object `{}`. This is the existing behavior of Path A and
the documented Claude Code protocol.

---

## Threat Model

### STRIDE Analysis (C2 -- STRIDE + DREAD scoring)

Criticality: C2 (Standard). The enforcement pipeline is a security-relevant
component (AE-005 auto-C3 candidate), but the pipeline itself is a defense
mechanism, not an attack surface exposed to external users. The threat model
covers bypass and degradation risks.

| ID | STRIDE Category | Threat | Component | DREAD Score | Mitigation |
|----|----------------|--------|-----------|-------------|------------|
| T-01 | Tampering | Attacker modifies `patterns.yaml` to weaken detection rules | YamlPatternLibraryAdapter | D:3 R:3 E:5 A:3 D:2 = 3.2 | Governance escalation (patterns.yaml under `.context/rules/` equivalent path detection; add to GOVERNANCE_FILES if moved) |
| T-02 | Tampering | Attacker modifies `security_rules.py` to remove blocked paths | SecurityRules | D:2 R:3 E:7 A:3 D:2 = 3.4 | Code review + CI. File is in `src/` under enforcement directory. Pre-commit hook catches changes. |
| T-03 | Denial of Service | Malicious regex in patterns.yaml causes ReDoS, exceeding hook timeout | PatternLibrary.validate_text | D:5 R:5 E:3 A:5 D:3 = 4.2 | Timeout enforcement (100ms per AC-015-002). Existing timeout logic in PatternLibrary.validate_text already handles this. |
| T-04 | Elevation of Privilege | Path traversal bypasses blocked path check (`../../etc/passwd`) | SecurityEnforcementEngine._check_file_write | D:7 R:5 E:5 A:7 D:5 = 5.8 | `os.path.normpath(os.path.expanduser(...))` canonicalizes before comparison. Existing code in scripts/pre_tool_use.py already does this (RT-003). Port this logic exactly. |
| T-05 | Spoofing | Tool name spoofing to bypass category-specific checks | Handler dispatch | D:1 R:1 E:1 A:1 D:1 = 1.0 | Claude Code controls `tool_name` field. Not user-controllable. Accepted risk. |
| T-06 | Information Disclosure | Pattern match details in stderr leak sensitive content (matched PII/secrets) | Handler warning output | D:3 R:3 E:7 A:3 D:2 = 3.6 | Log rule_id and description only, never the matched text. The existing `check_patterns` function in scripts/pre_tool_use.py logs `matches` which includes matched text -- fix this during port. |
| T-07 | Tampering | Fail-open semantics allow bypass if engine initialization crashes | Handler composition | D:5 R:5 E:3 A:5 D:5 = 4.6 | Intentional design trade-off: fail-open prevents hook failures from blocking all development. Mitigated by independent failure domains (three separate try blocks). Log all failures to stderr for post-hoc detection. |

### Trust Boundaries

```
+-------------------------------------------+
| Claude Code Process                       |
|  (trusted: controls tool_name, tool_input)|
|                                           |
|   stdin JSON ----+                        |
+-------------------------------------------+
                   |
                   v
+-------------------------------------------+
| Jerry Hook Process (uv run jerry hooks)   |
|  (trusted: our code)                      |
|                                           |
|  +-- SecurityEnforcementEngine            |
|  |     +-- security_rules.py (trusted)    |
|  |     +-- patterns.yaml (semi-trusted*)  |
|  +-- PreToolEnforcementEngine             |
|  |     +-- enforcement_rules.py (trusted) |
|  +-- StalenessDetector                    |
|                                           |
|   stdout JSON ---+                        |
+-------------------------------------------+
                   |
                   v
+-------------------------------------------+
| Claude Code Process                       |
|  (enforces block/warn/approve)            |
+-------------------------------------------+

* patterns.yaml is semi-trusted: it is a configuration file
  that can be modified by any contributor. Governance escalation
  should cover modifications to this file.
```

### NIST CSF 2.0 Mapping

| CSF Function | Implementation |
|-------------|---------------|
| **Identify (ID)** | SecurityRules defines the asset inventory of blocked paths and sensitive patterns |
| **Protect (PR)** | SecurityEnforcementEngine blocks writes to protected paths; PatternLibrary detects secrets before they are written |
| **Detect (DE)** | Pattern-based PII and secrets detection; governance escalation detection |
| **Respond (RS)** | Block response halts dangerous operations; warn response alerts without blocking |
| **Recover (RC)** | Fail-open design ensures development can continue even if enforcement fails; stderr logging enables post-incident analysis |

---

## Consequences

### Positive

1. **Single entry point**: All pre-tool enforcement runs through one handler,
   one pipeline, one output format.
2. **18 security checks restored**: Currently not running since hooks config
   was removed from `settings.json`. Consolidation restores them.
3. **Testable**: Every check is reachable via `SecurityEnforcementEngine.evaluate()`
   with injected `SecurityRules` and `IPatternLibrary`. No `sys.path` hacking,
   no module-level globals.
4. **Independent failure domains**: Three engines, three try blocks. One crash
   does not cascade.
5. **Pattern library injectable**: Tests can provide mock patterns without
   touching the filesystem.

### Negative

1. **Migration risk**: During the transition period, both paths exist. The
   standalone script must be deprecated carefully to avoid a window where
   neither path runs.
2. **Handler grows**: `HooksPreToolUseHandler` gains a third dependency and
   a new dispatch method. Still under 300 lines, but approaching the boundary
   where extraction to a pipeline coordinator may be warranted.
3. **Pragmatic domain violation**: Security rules in `infrastructure/` rather
   than `domain/` is a conscious trade-off for consistency with the existing
   engine. Documented as an acceptable deviation.

### Migration Sequence

1. Create new files (engine, rules, adapter, port, value objects).
2. Write unit tests for all 18 security checks.
3. Modify handler to accept and call `SecurityEnforcementEngine`.
4. Update `bootstrap.py` to wire the new engine.
5. Update `settings.json` hooks config to use `uv run jerry hooks pre-tool-use`
   instead of the standalone script.
6. Deprecate `scripts/pre_tool_use.py` (add deprecation comment, do not delete).
7. Verify end-to-end: hook fires, security blocks work, architecture blocks work,
   staleness warns work.

---

## References

| Source | Relevance |
|--------|-----------|
| #150 | Issue requiring consolidation |
| EN-703 | PreToolUse Enforcement Engine design |
| WI-SAO-015 | Guardrail Validation Hooks work item |
| AC-015-001 through AC-015-004 | Pattern library acceptance criteria |
| H-07 | Architecture layer isolation |
| H-10 | One class per file |
| RT-003 | Path traversal prevention (noted in scripts/pre_tool_use.py) |
| RT-004 | Dangerous rm flag variation detection |
