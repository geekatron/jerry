# TASK-003: PreToolUse Hook Architecture Design

<!--
DOCUMENT-ID: FEAT-005:EN-403:TASK-003
TEMPLATE: Architecture Design
VERSION: 1.0.0
AGENT: ps-architect (Claude Opus 4.6)
DATE: 2026-02-13
PARENT: EN-403 (Hook-Based Enforcement Implementation)
FEATURE: FEAT-005 (Quality Framework Enforcement Mechanisms)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
QUALITY-TARGET: >= 0.92
CONSUMERS: TASK-006 (implementation), TASK-008 (code review), TASK-009 (adversarial review)
REQUIREMENTS-COVERED: REQ-403-030 through REQ-403-039, REQ-403-060/061, REQ-403-070-073, REQ-403-075-078, REQ-403-080-082, REQ-403-086/087, REQ-403-092/093
-->

> **Version:** 1.0.0
> **Agent:** ps-architect (Claude Opus 4.6)
> **Status:** COMPLETE
> **Created:** 2026-02-13
> **Layer:** L3 (Pre-Action Gating)
> **Primary Vectors:** V-001 (PreToolUse Blocking), V-038 (AST Import Boundary Validation)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Mission](#mission) | What this hook does and why it matters |
| [Current Implementation Analysis](#current-implementation-analysis) | What the existing PreToolUse hook already does |
| [Architecture Overview](#architecture-overview) | High-level design with hexagonal layers |
| [Detailed Design](#detailed-design) | Component specifications and interfaces |
| [AST Validation Integration](#ast-validation-integration) | V-038 boundary validation design |
| [Enforcement Decision Logic](#enforcement-decision-logic) | Block/warn/approve decision algorithm |
| [Adversarial Strategy Integration](#adversarial-strategy-integration) | S-007, S-010, S-013 touchpoint design |
| [Decision Criticality Gating](#decision-criticality-gating) | Governance file escalation |
| [Error Handling](#error-handling) | Fail-open/fail-closed behavior per context |
| [Performance Design](#performance-design) | Latency budget and optimization |
| [Platform Adaptation](#platform-adaptation) | Cross-platform considerations |
| [File Layout](#file-layout) | Where new and modified code lives |
| [Interface Contracts](#interface-contracts) | Input/output schemas |
| [Testing Strategy](#testing-strategy) | How to verify the design |
| [Requirements Coverage](#requirements-coverage) | Which requirements this design satisfies |
| [References](#references) | Source documents |

---

## Mission

The PreToolUse hook is the **L3 enforcement layer** in Jerry's 5-layer hybrid enforcement architecture. Its mission is to **deterministically block non-compliant tool operations before they execute**, providing context-rot-immune enforcement that does not depend on the LLM's context state.

**Why this matters:** L3 is the critical compensation layer for L2 failure. If the LLM ignores L2 re-injected rules (which it may under severe context rot or prompt injection), L3 blocks non-compliant operations at the tool call level regardless. L3 enforcement decisions are made by external Python code, not by the LLM.

**Defense-in-depth role:**

```
L2 (UserPromptSubmit) ──LLM ignores rules──> L3 (This Hook) blocks deterministically
L3 (This Hook) ──fail-open on error──> L4/L5 detect violations post-hoc
```

**Key properties:**
- **Zero token cost:** Enforcement logic executes externally; no context window consumption (REQ-403-033)
- **Context-rot-immune:** Decisions derived from file system state (AST analysis), not LLM context (REQ-403-087)
- **Deterministic:** Binary pass/fail based on rules encoded in Python code (REQ-403-033)

---

## Current Implementation Analysis

The existing PreToolUse hook (`scripts/pre_tool_use.py`) provides:

**Phase 1: Rule-based security checks**
- Blocked write paths (system directories, sensitive files)
- Dangerous bash command detection
- Git operation safety (force push, hard reset)

**Phase 2: Pattern-based validation**
- Extensible pattern library (`scripts/patterns/`)
- Block/warn/ask/approve decision hierarchy
- Pattern library errors fail-open

**What is missing (the gap this design fills):**
1. No AST import boundary validation (V-038)
2. No architecture rule enforcement (one-class-per-file, type hints, docstrings)
3. No governance file escalation (C3+ for constitution/rules changes)
4. No adversarial strategy integration (S-007, S-010, S-013)

**Design constraint:** The new enforcement capabilities must be **additive** to the existing implementation. The existing security guardrails (REQ-403-038) and pattern library integration (REQ-403-039) must remain fully functional.

---

## Architecture Overview

### Hexagonal Layer Mapping

```
┌──────────────────────────────────────────────────────────────┐
│                    INTERFACE LAYER                            │
│                                                              │
│  scripts/pre_tool_use.py (MODIFIED)                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Thin adapter (existing structure preserved):        │    │
│  │   Phase 1: Security checks (existing)               │    │
│  │   Phase 2: Pattern-based validation (existing)      │    │
│  │   Phase 3: AST enforcement (NEW)                    │    │
│  │   Phase 4: Governance escalation (NEW)              │    │
│  │   Phase 5: Approve if all pass (existing)           │    │
│  └─────────────────────────────────────────────────────┘    │
│                            │                                 │
│                            ▼                                 │
│                ENFORCEMENT LIBRARY (L3 core)                 │
│                                                              │
│  src/infrastructure/internal/enforcement/                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ ast_boundary_validator.py (from V-038/TASK-006)     │    │
│  │                                                     │    │
│  │   class ASTBoundaryValidator:                       │    │
│  │     validate_file(path) -> list[ImportViolation]    │    │
│  │     validate_changed_files(paths) -> [violations]   │    │
│  │                                                     │    │
│  │ boundary_rules.py (from V-038/TASK-006)             │    │
│  │                                                     │    │
│  │   get_jerry_boundary_rules() -> list[BoundaryRule]  │    │
│  │                                                     │    │
│  │ pretool_enforcement.py (NEW)                        │    │
│  │                                                     │    │
│  │   class PreToolEnforcementEngine:                   │    │
│  │     evaluate_write(file_path, content)              │    │
│  │       -> EnforcementDecision                        │    │
│  │     evaluate_edit(file_path, old, new)              │    │
│  │       -> EnforcementDecision                        │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│                    DOMAIN LAYER (Data)                        │
│                                                              │
│  src/infrastructure/internal/enforcement/                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ enforcement_rules.py (NEW)                          │    │
│  │                                                     │    │
│  │   GOVERNANCE_FILES: set[str]                        │    │
│  │   PYTHON_FILE_EXTENSIONS: set[str]                  │    │
│  │   ARCHITECTURE_CHECKS: dict[str, Callable]          │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

### Integration with Existing Code

The design follows a **phased execution** pattern within the existing `main()` function:

```
PreToolUse hook invoked (stdin JSON)
       │
       ├──► Phase 1: Security checks (EXISTING, unchanged)
       │    └── check_file_write(), check_bash_command(), check_git_operation()
       │
       ├──► Phase 2: Pattern validation (EXISTING, unchanged)
       │    └── check_patterns()
       │
       ├──► Phase 3: AST enforcement (NEW)
       │    └── For Write/Edit on .py files in src/
       │         ├── Parse content with ast.parse()
       │         ├── Extract imports
       │         ├── Validate against boundary rules
       │         ├── Check one-class-per-file (V-041)
       │         └── Block or warn based on violations
       │
       ├──► Phase 4: Governance escalation (NEW)
       │    └── For Write/Edit on governance files
       │         ├── Detect governance file paths
       │         └── Inject C3+ escalation warning
       │
       └──► Phase 5: Approve (EXISTING, renumbered)
            └── All checks passed
```

---

## Detailed Design

### Component 1: PreTool Enforcement Engine (`pretool_enforcement.py`)

**Responsibility:** Core L3 enforcement logic for file write operations. Orchestrates AST validation, architecture checks, and governance escalation.

```python
"""PreToolUse enforcement engine for L3 pre-action gating.

Provides deterministic, context-rot-immune enforcement for
tool operations. All decisions are derived from file system
state and encoded rules, never from LLM context.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class EnforcementDecision:
    """Result of an enforcement evaluation."""
    action: str  # "block", "warn", "approve"
    reason: str
    violations: list[str] = field(default_factory=list)
    criticality_escalation: str | None = None  # "C3", "C4" if escalated


class PreToolEnforcementEngine:
    """Enforcement engine for PreToolUse hook (L3 layer).

    Evaluates file write/edit operations against:
    1. AST import boundary rules (V-038)
    2. Architecture rules (V-039, V-040, V-041)
    3. Governance file escalation (REQ-403-061)

    All decisions are deterministic and context-rot-immune.
    """

    def __init__(
        self,
        project_root: Path | None = None,
    ) -> None:
        self._root = project_root or self._find_root()
        self._boundary_validator = self._create_validator()

    def evaluate_write(
        self,
        file_path: str,
        content: str,
    ) -> EnforcementDecision:
        """Evaluate a Write tool operation.

        Args:
            file_path: Target file path.
            content: Content to be written.

        Returns:
            EnforcementDecision with action and reason.
        """
        path = Path(file_path)

        # Check governance escalation first
        escalation = self._check_governance_escalation(file_path)

        # Only validate Python files in src/
        if not self._is_validatable_python(path):
            if escalation:
                return EnforcementDecision(
                    action="warn",
                    reason=f"Governance file modification detected: {escalation}",
                    criticality_escalation=escalation,
                )
            return EnforcementDecision(action="approve", reason="")

        # AST validation
        violations = self._validate_content(content, path)

        if violations:
            return EnforcementDecision(
                action="block",
                reason=self._format_violations(violations, path),
                violations=violations,
                criticality_escalation=escalation,
            )

        if escalation:
            return EnforcementDecision(
                action="warn",
                reason=f"Governance file modification -- auto-escalated to {escalation}",
                criticality_escalation=escalation,
            )

        return EnforcementDecision(action="approve", reason="")

    def evaluate_edit(
        self,
        file_path: str,
        new_content: str,
    ) -> EnforcementDecision:
        """Evaluate an Edit tool operation.

        For edits, we validate the new content that will result
        from the edit operation.

        Args:
            file_path: Target file path.
            new_content: The new string being inserted.

        Returns:
            EnforcementDecision with action and reason.
        """
        # For edits, we can only validate the new_string portion.
        # Full file validation happens at pre-commit (V-044) and CI (V-045).
        path = Path(file_path)

        # Governance escalation
        escalation = self._check_governance_escalation(file_path)
        if escalation:
            return EnforcementDecision(
                action="warn",
                reason=f"Governance file modification -- auto-escalated to {escalation}",
                criticality_escalation=escalation,
            )

        # For edits, we cannot fully parse the new content as standalone AST.
        # Import validation requires full-file context.
        # Defer to pre-commit (V-044) and CI (V-045) for edit validation.
        return EnforcementDecision(action="approve", reason="")

    def _is_validatable_python(self, path: Path) -> bool:
        """Check if a file is a validatable Python file in src/."""
        if path.suffix != ".py":
            return False
        # Only validate files under src/ (not tests/, scripts/, hooks/)
        try:
            rel = path.relative_to(self._root / "src")
            return True
        except ValueError:
            return False

    def _validate_content(
        self,
        content: str,
        file_path: Path,
    ) -> list[str]:
        """Validate Python content against architecture rules.

        Returns list of violation descriptions. Empty list = no violations.
        """
        violations = []

        # Parse AST (fail-open on SyntaxError per REQ-403-073)
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return []  # Skip files with syntax errors

        # V-038: Import boundary validation
        import_violations = self._check_imports(tree, file_path)
        violations.extend(import_violations)

        # V-041: One-class-per-file check
        class_violations = self._check_one_class_per_file(tree, file_path)
        violations.extend(class_violations)

        return violations

    def _check_imports(
        self,
        tree: ast.Module,
        file_path: Path,
    ) -> list[str]:
        """Check import boundary violations (V-038)."""
        violations = []

        # Determine source layer from file path
        source_layer = self._determine_layer(file_path)
        if source_layer is None:
            return []  # Cannot determine layer; skip validation

        # Exempt bootstrap.py (REQ-403-036)
        if file_path.name == "bootstrap.py":
            return []

        for node in ast.walk(tree):
            # Skip TYPE_CHECKING imports (REQ-403-037)
            if self._is_type_checking_import(node, tree):
                continue

            module_name = None
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_name = alias.name
                    violation = self._check_import_boundary(
                        source_layer, module_name, node.lineno
                    )
                    if violation:
                        violations.append(violation)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    module_name = node.module
                    violation = self._check_import_boundary(
                        source_layer, module_name, node.lineno
                    )
                    if violation:
                        violations.append(violation)

            # V-038 FM-038-02: Dynamic import detection (REQ-403-035)
            if isinstance(node, ast.Call):
                if self._is_dynamic_import(node):
                    violations.append(
                        f"Line {node.lineno}: Dynamic import detected "
                        f"(importlib/__import__). Use static imports."
                    )

        return violations

    def _check_import_boundary(
        self,
        source_layer: str,
        import_module: str,
        line_number: int,
    ) -> str | None:
        """Check if an import violates layer boundaries.

        Returns violation description or None if compliant.
        """
        # Define forbidden imports per layer
        forbidden = {
            "domain": ["application", "infrastructure", "interface"],
            "application": ["infrastructure", "interface"],
            "infrastructure": ["interface"],
            "shared_kernel": ["infrastructure", "interface"],
        }

        forbidden_layers = forbidden.get(source_layer, [])
        for forbidden_layer in forbidden_layers:
            if (f"src.{forbidden_layer}" in import_module or
                f".{forbidden_layer}." in import_module):
                return (
                    f"Line {line_number}: {source_layer} layer imports from "
                    f"{forbidden_layer} layer ({import_module}). "
                    f"Violates hexagonal architecture boundary."
                )

        return None

    def _determine_layer(self, file_path: Path) -> str | None:
        """Determine which hexagonal layer a file belongs to."""
        parts = file_path.parts
        layer_names = {"domain", "application", "infrastructure", "interface", "shared_kernel"}

        for part in parts:
            if part in layer_names:
                return part

        return None

    def _is_type_checking_import(
        self,
        node: ast.AST,
        tree: ast.Module,
    ) -> bool:
        """Check if an import is inside a TYPE_CHECKING block."""
        # Walk the tree to find If nodes with TYPE_CHECKING test
        for parent_node in ast.walk(tree):
            if isinstance(parent_node, ast.If):
                # Check if the test is TYPE_CHECKING
                if (isinstance(parent_node.test, ast.Name) and
                        parent_node.test.id == "TYPE_CHECKING"):
                    # Check if the import node is in the body
                    for child in ast.walk(parent_node):
                        if child is node:
                            return True
                elif (isinstance(parent_node.test, ast.Attribute) and
                      isinstance(parent_node.test.value, ast.Name)):
                    if (parent_node.test.value.id == "typing" and
                            parent_node.test.attr == "TYPE_CHECKING"):
                        for child in ast.walk(parent_node):
                            if child is node:
                                return True
        return False

    def _is_dynamic_import(self, node: ast.Call) -> bool:
        """Check if a Call node is a dynamic import."""
        # __import__("module")
        if isinstance(node.func, ast.Name) and node.func.id == "__import__":
            return True
        # importlib.import_module("module")
        if (isinstance(node.func, ast.Attribute) and
                node.func.attr == "import_module" and
                isinstance(node.func.value, ast.Name) and
                node.func.value.id == "importlib"):
            return True
        return False

    def _check_one_class_per_file(
        self,
        tree: ast.Module,
        file_path: Path,
    ) -> list[str]:
        """Check V-041: one public class per file."""
        # Only check files in domain/, application/, infrastructure/ layers
        if not self._determine_layer(file_path):
            return []

        # Exempt __init__.py files
        if file_path.name == "__init__.py":
            return []

        # Count top-level class definitions (public, not prefixed with _)
        public_classes = []
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                if not node.name.startswith("_"):
                    public_classes.append(node.name)

        if len(public_classes) > 1:
            return [
                f"File contains {len(public_classes)} public classes "
                f"({', '.join(public_classes)}). "
                f"Jerry requires one public class per file (PAT-ARCH-004)."
            ]

        return []

    def _check_governance_escalation(self, file_path: str) -> str | None:
        """Check if file targets governance/constitution files.

        Returns criticality level (C3 or C4) or None.
        """
        governance_patterns = [
            ("docs/governance/JERRY_CONSTITUTION.md", "C4"),
            ("docs/governance/", "C3"),
            (".claude/rules/", "C3"),
            (".context/rules/", "C3"),
        ]

        for pattern, level in governance_patterns:
            if pattern in file_path or file_path.endswith(pattern):
                return level

        return None

    def _format_violations(
        self,
        violations: list[str],
        file_path: Path,
    ) -> str:
        """Format violations into a human-readable block message."""
        header = f"Architecture violations in {file_path.name}:"
        items = "\n".join(f"  - {v}" for v in violations)
        return f"{header}\n{items}"

    def _find_root(self) -> Path:
        """Find project root."""
        current = Path.cwd()
        for parent in [current, *current.parents]:
            if (parent / "CLAUDE.md").exists():
                return parent
        return current

    def _create_validator(self):
        """Create ASTBoundaryValidator if available.

        Falls back to inline validation if the V-038 library
        is not yet implemented.
        """
        try:
            from src.infrastructure.internal.enforcement.ast_boundary_validator import (
                ASTBoundaryValidator,
            )
            from src.infrastructure.internal.enforcement.boundary_rules import (
                get_jerry_boundary_rules,
            )
            return ASTBoundaryValidator(get_jerry_boundary_rules())
        except ImportError:
            return None  # Use inline validation
```

### Component 2: Enforcement Rules (`enforcement_rules.py`)

**Responsibility:** Static data definitions for enforcement decisions.

```python
"""Static enforcement rule definitions for PreToolUse hook.

Contains governance file patterns, architecture check
configurations, and other rule data used by the enforcement engine.
"""
from __future__ import annotations

# Files that trigger automatic C3+ escalation (REQ-403-061)
GOVERNANCE_FILES: dict[str, str] = {
    "docs/governance/JERRY_CONSTITUTION.md": "C4",
    "docs/governance/": "C3",
    ".claude/rules/": "C3",
    ".context/rules/": "C3",
}

# File extensions eligible for AST validation
PYTHON_EXTENSIONS: set[str] = {".py"}

# Directories eligible for architecture enforcement
ENFORCED_DIRECTORIES: set[str] = {"src"}

# Directories exempt from enforcement
EXEMPT_DIRECTORIES: set[str] = {"tests", "scripts", "hooks"}

# Files exempt from import boundary checks (REQ-403-036)
EXEMPT_FILES: set[str] = {"bootstrap.py"}
```

### Component 3: Modified `pre_tool_use.py`

The existing `scripts/pre_tool_use.py` is modified to add Phase 3 and Phase 4 **after** the existing Phase 2:

```python
# Addition to main() in scripts/pre_tool_use.py, after Phase 2

        # =================================================================
        # PHASE 3: AST Architecture Enforcement (V-038, V-041) -- NEW
        # =================================================================
        if tool_name in ("Write", "Edit"):
            try:
                from src.infrastructure.internal.enforcement.pretool_enforcement import (
                    PreToolEnforcementEngine,
                )

                enforcement = PreToolEnforcementEngine()

                if tool_name == "Write":
                    decision = enforcement.evaluate_write(
                        file_path=tool_input.get("file_path", ""),
                        content=tool_input.get("content", ""),
                    )
                else:  # Edit
                    decision = enforcement.evaluate_edit(
                        file_path=tool_input.get("file_path", ""),
                        new_content=tool_input.get("new_string", ""),
                    )

                if decision.action == "block":
                    print(json.dumps({
                        "decision": "block",
                        "reason": decision.reason,
                    }))
                    return 0

                if decision.action == "warn":
                    print(json.dumps({
                        "warning": decision.reason,
                        "criticality_escalation": decision.criticality_escalation,
                    }), file=sys.stderr)
                    # Continue to approve

            except ImportError:
                # Enforcement module not yet available; fail-open
                pass
            except Exception as e:
                # Fail-open: log error, continue to approve
                print(json.dumps({
                    "warning": f"AST enforcement error: {e}",
                    "fallback": "approve",
                }), file=sys.stderr)
```

**Key design decisions:**

1. **Import inside function:** The enforcement module is imported inside the `main()` function to avoid import errors when the module is not yet deployed. This enables incremental rollout.
2. **Fail-open on ImportError:** If the enforcement library is not available, the hook silently continues. This ensures the existing security guardrails still function.
3. **Phase ordering:** Security checks (Phase 1) run before architecture enforcement (Phase 3). A security violation blocks immediately without running architecture checks. Architecture enforcement only runs for operations that pass security.

---

## AST Validation Integration

### V-038: Import Boundary Validation

**What it checks:** Python import statements against the hexagonal architecture layer dependency rules.

**Boundary rules (from `.context/rules/architecture-standards.md`):**

| Source Layer | Cannot Import From |
|-------------|-------------------|
| `domain/` | `application`, `infrastructure`, `interface` |
| `application/` | `infrastructure`, `interface` |
| `infrastructure/` | `interface` |
| `shared_kernel/` | `infrastructure`, `interface` |

**Exemptions:**
- `src/bootstrap.py` -- composition root may import all layers (REQ-403-036)
- `TYPE_CHECKING` conditional imports -- compile-time only, no runtime dependency (REQ-403-037)

**How it works:**
1. Hook receives Write tool input with `file_path` and `content`
2. Engine checks if file is a Python file in `src/`
3. If yes, parse content with `ast.parse()`
4. Walk AST tree, extract Import and ImportFrom nodes
5. Determine source layer from file path
6. Check each import against boundary rules
7. Block if violations found; approve if clean

### V-041: One-Class-Per-File

**What it checks:** Python files in `src/` layers contain at most one public (non-underscore-prefixed) class definition.

**Exemptions:** `__init__.py` files may export multiple classes.

### V-039, V-040: Type Hints and Docstrings (Future)

These checks are **designed for** but not yet implemented in this phase. The engine architecture supports adding them as additional validation steps in `_validate_content()`.

| Vector | Check | Status | Priority |
|--------|-------|--------|----------|
| V-039 | Type hint presence on public functions | DESIGNED (not implemented) | MEDIUM |
| V-040 | Docstring presence on public classes/functions | DESIGNED (not implemented) | MEDIUM |

---

## Enforcement Decision Logic

### Decision Algorithm

```
Input: tool_name, tool_input (file_path, content)
       │
       ├── Is tool_name Write or Edit?
       │   └── NO ──► APPROVE (non-file operations pass through)
       │
       ├── Is file_path a governance file?
       │   └── YES ──► WARN with C3/C4 escalation
       │
       ├── Is file_path a .py file in src/?
       │   └── NO ──► APPROVE (non-Python or non-src files pass)
       │
       ├── Is file bootstrap.py?
       │   └── YES ──► APPROVE (composition root exempt)
       │
       ├── Can AST parse the content?
       │   └── NO (SyntaxError) ──► APPROVE (fail-open per REQ-403-073)
       │
       ├── Import boundary violations found?
       │   └── YES ──► BLOCK with violation details
       │
       ├── One-class-per-file violation found?
       │   └── YES ──► BLOCK with violation details
       │
       └── All checks pass ──► APPROVE
```

### Decision Outcomes

| Decision | JSON Output | Exit Code | User Impact |
|----------|------------|-----------|-------------|
| APPROVE | `{"decision": "approve"}` | 0 | Operation proceeds |
| BLOCK | `{"decision": "block", "reason": "..."}` | 0 | Operation prevented; user sees reason |
| WARN | `{"decision": "approve"}` + stderr warning | 0 | Operation proceeds; warning logged |

**BLOCK vs WARN:**
- **BLOCK:** For deterministic architecture violations (import boundary, one-class-per-file). These are clear, objective violations of established rules.
- **WARN:** For governance escalation (C3+). The warning informs about escalated criticality but does not prevent the operation -- the user has authority (P-020) to modify any file.

---

## Adversarial Strategy Integration

### S-007 (Constitutional AI) -- File Write Operations

**Integration point:** When the PreToolUse hook detects a write to governance files (`.claude/rules/`, `docs/governance/`), it triggers a C3+ escalation warning.

**Mechanism:** The warning in stderr includes the criticality escalation level, which instructs Claude to apply S-007 constitutional compliance verification before proceeding. This is an informational trigger, not a deterministic block -- the user retains authority (P-020).

### S-010 (Self-Refine) -- Code Generation

**Integration point:** The AST validation itself serves as an external self-refine check. If the LLM-generated code contains import violations, the block message forces the LLM to revise its output.

**Mechanism:** Deterministic. The hook blocks non-compliant code and provides specific violation details that guide the LLM's revision.

### S-013 (Inversion) -- Anti-Pattern Detection

**Integration point:** The one-class-per-file check (V-041) and the dynamic import detection (REQ-403-035) are anti-pattern detection mechanisms.

**Mechanism:** Deterministic. Known anti-patterns (multiple public classes per file, dynamic imports) are detected by AST analysis and flagged/blocked.

---

## Decision Criticality Gating

### Governance File Detection (REQ-403-061)

Any Write or Edit operation targeting the following files triggers automatic C3+ escalation:

| File Pattern | Criticality Level | Rationale |
|-------------|------------------|-----------|
| `docs/governance/JERRY_CONSTITUTION.md` | C4 (Critical) | Constitution changes are irreversible governance decisions |
| `docs/governance/` | C3 (Significant) | Governance documents require deep review |
| `.claude/rules/` | C3 (Significant) | Rules changes affect all subsequent sessions |
| `.context/rules/` | C3 (Significant) | Canonical rules source |

### Escalation Behavior

Governance escalation does NOT block the operation. It:
1. Logs a warning to stderr with the escalation level
2. Includes the escalation level in the hook output for Claude to process
3. Claude is expected to apply the corresponding review depth (L3 Deep Review or L4 Tournament per SRC-002, Decision Criticality Escalation)

This design respects P-020 (User Authority): the user can always modify governance files, but the system ensures they are aware of the criticality level.

---

## Error Handling

### Fail-Open vs. Fail-Closed

The PreToolUse hook has a **mixed** error handling strategy per the requirements:

| Scenario | Behavior | Rationale |
|----------|----------|-----------|
| Non-Python files | Fail-open (approve) | REQ-403-072: AST only applies to `.py` files |
| SyntaxError in content | Fail-open (approve) | REQ-403-073: Incomplete code during development |
| ImportError (module not found) | Fail-open (approve) | Incremental deployment; existing security checks still run |
| Any unexpected exception | Fail-open (approve + log) | REQ-403-070: Never block user work due to hook errors |
| Architecture violations detected | Fail-closed (block) | REQ-403-030: Deterministic enforcement of architecture rules |

**The key distinction:** Errors in the *enforcement logic itself* fail-open. Violations detected by *correctly functioning* enforcement logic fail-closed (block). This ensures enforcement is reliable when operational but never causes collateral damage when broken.

### Error Logging

All errors and warnings are logged to stderr in JSON format (consistent with the existing implementation):

```json
{"warning": "AST enforcement error: <details>", "fallback": "approve"}
```

---

## Performance Design

### Latency Budget

Per NFR-005 (EN-403): Hook execution latency SHALL NOT noticeably degrade user experience (target: < 500ms).

| Operation | Estimated Time | Notes |
|-----------|---------------|-------|
| Read stdin JSON | < 1ms | In-memory |
| Phase 1: Security checks | < 5ms | String comparison |
| Phase 2: Pattern validation | < 10ms | Regex matching |
| Phase 3: AST parsing | < 50ms | Single file parse |
| Phase 3: Import analysis | < 20ms | AST walk |
| Phase 4: Governance check | < 1ms | String comparison |
| Total | < 87ms | Well within 500ms target |

**AST parsing is the bottleneck.** For typical Python files (< 1000 lines), `ast.parse()` completes in under 50ms. For very large files (> 5000 lines), it may take up to 200ms. This is still within the 500ms target.

### Optimization Decisions

1. **Parse only when needed:** AST parsing only runs for `.py` files in `src/`. Non-Python files and files outside `src/` skip Phase 3 entirely.
2. **No disk I/O in Phase 3:** The content to validate is already provided in the tool input (stdin JSON). No additional file reads are needed.
3. **Lazy import:** The enforcement module is imported lazily inside `main()` to avoid import overhead on non-Write/Edit operations.

---

## Platform Adaptation

### Claude Code (Primary Platform)

On Claude Code, the hook is registered in `hooks/hooks.json` with a `Write|Edit` matcher and invoked automatically before every Write/Edit tool call.

### Non-Claude-Code Platforms

Per REQ-403-077, the enforcement engine is a pure Python library importable independently:

```python
# Example: Non-Claude-Code pre-write validation
from src.infrastructure.internal.enforcement.pretool_enforcement import (
    PreToolEnforcementEngine,
)

engine = PreToolEnforcementEngine(project_root=Path("/path/to/jerry"))
decision = engine.evaluate_write(
    file_path="src/domain/entities/work_item.py",
    content=new_file_content,
)

if decision.action == "block":
    print(f"BLOCKED: {decision.reason}")
```

### Cross-Platform Considerations

| Concern | Resolution |
|---------|-----------|
| Path separators (`/` vs `\`) | Use `pathlib.Path` throughout (REQ-403-076) |
| File encoding | Specify `encoding='utf-8'` on all file reads (REQ-403-078) |
| Line endings | `ast.parse()` handles both `\n` and `\r\n` natively |
| Python stdlib only | No third-party dependencies (REQ-403-075) |

---

## File Layout

### New Files

| File | Layer | Purpose |
|------|-------|---------|
| `src/infrastructure/internal/enforcement/pretool_enforcement.py` | Infrastructure | L3 enforcement engine |
| `src/infrastructure/internal/enforcement/enforcement_rules.py` | Infrastructure | Static rule definitions |
| `tests/unit/enforcement/test_pretool_enforcement.py` | Test | Unit tests for engine |

### Modified Files

| File | Change |
|------|--------|
| `scripts/pre_tool_use.py` | Add Phase 3 (AST enforcement) and Phase 4 (governance escalation) |

### Files from V-038 (dependency, not created here)

| File | Status | Purpose |
|------|--------|---------|
| `src/infrastructure/internal/enforcement/ast_boundary_validator.py` | Future (TASK-006 / EN-402 V-038) | Reusable AST validator |
| `src/infrastructure/internal/enforcement/boundary_rules.py` | Future (TASK-006 / EN-402 V-038) | Declarative boundary rules |

The `PreToolEnforcementEngine` is designed to work both with and without the V-038 library. If V-038 is not yet deployed, the engine uses its own inline import validation logic. When V-038 is deployed, the engine delegates to `ASTBoundaryValidator` for richer validation.

---

## Interface Contracts

### Input Schema (stdin JSON -- existing)

```json
{
    "tool_name": "Write",
    "tool_input": {
        "file_path": "/absolute/path/to/file.py",
        "content": "file content string"
    }
}
```

For Edit operations:
```json
{
    "tool_name": "Edit",
    "tool_input": {
        "file_path": "/absolute/path/to/file.py",
        "old_string": "text to replace",
        "new_string": "replacement text"
    }
}
```

### Output Schema (stdout JSON -- existing, extended)

**Block:**
```json
{"decision": "block", "reason": "Architecture violations in work_item.py:\n  - Line 5: domain layer imports from infrastructure layer (src.infrastructure.adapters)"}
```

**Approve:**
```json
{"decision": "approve"}
```

**Warn (stderr):**
```json
{"warning": "Governance file modification -- auto-escalated to C3", "criticality_escalation": "C3"}
```

### Internal Interfaces

```python
# EnforcementDecision -- output from engine
@dataclass(frozen=True)
class EnforcementDecision:
    action: str           # "block", "warn", "approve"
    reason: str           # Human-readable explanation
    violations: list[str] # Individual violation descriptions
    criticality_escalation: str | None  # "C3", "C4" if escalated
```

---

## Testing Strategy

### Unit Tests

| Test | File | Validates |
|------|------|-----------|
| `test_validate_clean_domain_file` | `test_pretool_enforcement.py` | REQ-403-030 (clean file approves) |
| `test_block_domain_importing_infrastructure` | `test_pretool_enforcement.py` | REQ-403-031 (boundary violation blocks) |
| `test_block_application_importing_interface` | `test_pretool_enforcement.py` | REQ-403-031 |
| `test_exempt_bootstrap_py` | `test_pretool_enforcement.py` | REQ-403-036 |
| `test_exempt_type_checking_imports` | `test_pretool_enforcement.py` | REQ-403-037 |
| `test_approve_non_python_files` | `test_pretool_enforcement.py` | REQ-403-072 |
| `test_approve_on_syntax_error` | `test_pretool_enforcement.py` | REQ-403-073 |
| `test_detect_dynamic_imports` | `test_pretool_enforcement.py` | REQ-403-035 |
| `test_one_class_per_file_violation` | `test_pretool_enforcement.py` | REQ-403-034 (V-041) |
| `test_governance_file_c3_escalation` | `test_pretool_enforcement.py` | REQ-403-061 |
| `test_constitution_file_c4_escalation` | `test_pretool_enforcement.py` | REQ-403-061 |
| `test_engine_uses_no_external_imports` | `test_pretool_enforcement.py` | REQ-403-075 |
| `test_engine_is_deterministic` | `test_pretool_enforcement.py` | REQ-403-033 |
| `test_engine_independent_of_context` | `test_pretool_enforcement.py` | REQ-403-087 |

### Integration Tests

| Test | Validates |
|------|-----------|
| Modified `pre_tool_use.py` blocks architecture violation on Write | REQ-403-030 |
| Modified `pre_tool_use.py` preserves existing security checks | REQ-403-038 |
| Modified `pre_tool_use.py` preserves pattern library | REQ-403-039 |
| Hook fails-open when enforcement module unavailable | REQ-403-070 |

### Adversarial Tests (for TASK-009)

| Test | Attack Vector |
|------|--------------|
| Attempt to write violating code with varied import styles | Evasion techniques |
| Attempt to bypass via TYPE_CHECKING abuse | False exemption exploitation |
| Attempt to bypass via dynamic imports | V-038 FM-038-02 |
| Measure enforcement under 100K+ token context | Context rot irrelevance verification |

---

## Requirements Coverage

| Requirement | Covered By |
|-------------|-----------|
| REQ-403-030 | `evaluate_write()` triggers AST validation for .py in src/ |
| REQ-403-031 | `_check_import_boundary()` with all 4 layer rules |
| REQ-403-032 | `_check_governance_escalation()` for governance files |
| REQ-403-033 | External Python execution, no LLM dependency |
| REQ-403-034 | `_check_one_class_per_file()` (V-041); V-039/V-040 designed for future |
| REQ-403-035 | `_is_dynamic_import()` detection |
| REQ-403-036 | `bootstrap.py` exemption in `_check_imports()` |
| REQ-403-037 | `_is_type_checking_import()` exemption |
| REQ-403-038 | Existing security checks preserved (Phases 1-2 unchanged) |
| REQ-403-039 | Pattern library preserved (Phase 2 unchanged) |
| REQ-403-060 | `_check_governance_escalation()` returns C3/C4 levels |
| REQ-403-061 | Governance files auto-escalate to C3+ |
| REQ-403-070 | try/except with fail-open in Phase 3 |
| REQ-403-071 | stderr JSON logging on errors |
| REQ-403-072 | `_is_validatable_python()` checks `.py` extension |
| REQ-403-073 | SyntaxError returns empty violations |
| REQ-403-075 | Only stdlib imports (ast, pathlib, dataclasses) |
| REQ-403-076 | `pathlib.Path` throughout |
| REQ-403-077 | Engine importable as standalone library |
| REQ-403-078 | UTF-8 encoding specified where needed |
| REQ-403-080 | Enforcement logic separated from hook adapter |
| REQ-403-081 | Typed parameters and returns on engine |
| REQ-403-082 | `pre_tool_use.py` is thin adapter |
| REQ-403-086 | L3 blocks independently of LLM compliance |
| REQ-403-087 | No dependency on LLM context state |
| REQ-403-092 | Governance escalation triggers S-007 awareness |
| REQ-403-093 | One-class-per-file and dynamic import as anti-patterns (S-013) |

---

## References

| # | Citation | Used For |
|---|----------|----------|
| 1 | ADR-EPIC002-002 v1.2.0 (ACCEPTED) | L3 layer definition, V-001/V-038 properties, defense-in-depth chain |
| 2 | Barrier-1 ADV-to-ENF Handoff | PreToolUse strategy touchpoints (S-007, S-010, S-013) |
| 3 | EN-403 Enabler Definition v2.0.0 | FR-003-005, FR-009-011, NFR-003/006/008 |
| 4 | TASK-001 Hook Requirements (this enabler) | REQ-403-030 through REQ-403-093 |
| 5 | EN-402 TASK-006 Execution Plans v1.1.0 | V-038 AST validator design, boundary rules, code structure |
| 6 | `scripts/pre_tool_use.py` | Existing implementation to extend |
| 7 | `hooks/hooks.json` | Current hook registration (PreToolUse on Write/Edit) |
| 8 | `.context/rules/architecture-standards.md` | Hexagonal architecture boundary rules |
| 9 | `.context/rules/coding-standards.md` | TYPE_CHECKING pattern, one-class-per-file rule |

---

*Agent: ps-architect (Claude Opus 4.6)*
*Date: 2026-02-13*
*Parent: EN-403 Hook-Based Enforcement Implementation*
*Quality Target: >= 0.92*
*Target ACs: 3, 5, 10, 11*
