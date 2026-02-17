# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
PreToolUse Enforcement Engine for AST-based architecture validation.

Implements L3 Pre-Action Gating by analyzing Python source code via AST
to enforce import boundary rules (V-038) and one-class-per-file (V-041).
Also detects governance file modifications requiring criticality escalation.

The engine is fail-open by design: any internal error results in approval
rather than blocking legitimate work. Architecture violations detected by
correctly-functioning code result in blocking.

References:
    - EN-703: PreToolUse Enforcement Engine
    - EPIC-002 EN-403/TASK-003: PreToolUse hook design
    - EN-402: Enforcement priority analysis (V-038 scored 4.92 WCS)
"""

from __future__ import annotations

import ast
from pathlib import Path

from src.infrastructure.internal.enforcement.enforcement_decision import (
    EnforcementDecision,
)
from src.infrastructure.internal.enforcement.enforcement_rules import (
    ENFORCED_DIRECTORIES,
    EXEMPT_FILES,
    GOVERNANCE_FILES,
    LAYER_IMPORT_RULES,
    PYTHON_EXTENSIONS,
    RECOGNIZED_LAYERS,
)


class PreToolEnforcementEngine:
    """AST-based enforcement engine for pre-tool-use validation.

    Evaluates Python file writes and edits against architectural
    constraints. Enforces import boundaries (V-038) and
    one-class-per-file (V-041). Detects governance file modifications
    requiring escalation.

    The engine is fail-open: internal errors produce approval decisions
    rather than blocking legitimate work.

    Design deviation note (M-3):
        The EPIC-002 design (TASK-003, REQ-403-035) specifies that dynamic
        imports should be flagged as warnings.  This implementation
        intentionally blocks them instead.  The stricter behavior is safer:
        a dynamic ``__import__("src.infrastructure.adapters")`` in a domain
        file is just as much a boundary violation as a static import and
        should be blocked.  Warnings would allow the violation to enter the
        codebase.  This deviation is documented as design decision DD-7 in
        the creator report.

    Args:
        project_root: Path to the project root directory. If None,
            auto-detected by searching for CLAUDE.md.
    """

    def __init__(self, project_root: Path | None = None) -> None:
        """Initialize the enforcement engine.

        Args:
            project_root: Path to the project root directory. If None,
                auto-detected by searching for CLAUDE.md upward from CWD.
        """
        self._project_root = project_root or self._find_root()

    def evaluate_write(self, file_path: str, content: str) -> EnforcementDecision:
        """Evaluate a file write operation for architectural compliance.

        Checks governance escalation, then validates Python content
        against import boundary and one-class-per-file rules.

        Args:
            file_path: Absolute or relative path to the file being written.
            content: The complete file content to be written.

        Returns:
            EnforcementDecision with action, reason, violations, and
            optional criticality escalation.
        """
        try:
            # Check governance escalation first
            escalation = self._check_governance_escalation(file_path)

            path = Path(file_path)

            # Only validate Python files under enforced directories
            if not self._is_validatable_python(path):
                if escalation:
                    return EnforcementDecision(
                        action="warn",
                        reason=f"Governance file modification: {file_path}",
                        criticality_escalation=escalation,
                    )
                return EnforcementDecision(action="approve", reason="Not a validatable file")

            # Validate content
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
                    reason=f"Governance file modification: {file_path}",
                    criticality_escalation=escalation,
                )

            return EnforcementDecision(action="approve", reason="All checks passed")

        except Exception:
            # Fail-open: any unexpected error results in approval
            return EnforcementDecision(
                action="approve",
                reason="Enforcement error (fail-open)",
            )

    def evaluate_edit(
        self, file_path: str, old_string: str, new_string: str
    ) -> EnforcementDecision:
        """Evaluate a file edit operation for architectural compliance.

        Reads the existing file, applies the edit in-memory, then validates
        the resulting content against architectural rules.

        Args:
            file_path: Absolute or relative path to the file being edited.
            old_string: The text being replaced.
            new_string: The replacement text.

        Returns:
            EnforcementDecision with action, reason, violations, and
            optional criticality escalation.
        """
        try:
            target = Path(file_path)

            # If the file doesn't exist, fail-open
            if not target.is_file():
                return EnforcementDecision(
                    action="approve",
                    reason="File not found (fail-open)",
                )

            # Read existing content
            existing_content = target.read_text(encoding="utf-8")

            # Apply edit in-memory
            if old_string not in existing_content:
                # Edit target not found in file; fail-open
                return EnforcementDecision(
                    action="approve",
                    reason="Edit target not found in file (fail-open)",
                )

            resulting_content = existing_content.replace(old_string, new_string, 1)

            # Validate the resulting content
            return self.evaluate_write(file_path, resulting_content)

        except Exception:
            # Fail-open: any unexpected error results in approval
            return EnforcementDecision(
                action="approve",
                reason="Enforcement error (fail-open)",
            )

    def _is_validatable_python(self, path: Path) -> bool:
        """Check if a file is a Python file under an enforced directory.

        Only .py files under src/ are subject to enforcement.
        Files under tests/, scripts/, hooks/ are exempt.

        Args:
            path: Path to the file to check.

        Returns:
            True if the file should be validated.
        """
        if path.suffix not in PYTHON_EXTENSIONS:
            return False

        # Resolve relative to project root for reliable checks
        try:
            if path.is_absolute():
                rel_path = path.relative_to(self._project_root)
            else:
                rel_path = path
        except ValueError:
            # Path is not under project root
            return False

        parts = rel_path.parts
        if not parts:
            return False

        # Check if under an enforced directory
        return parts[0] in ENFORCED_DIRECTORIES

    def _validate_content(self, content: str, file_path: Path) -> list[str]:
        """Orchestrate all AST-based validation checks.

        Parses the content as a Python AST and runs import boundary
        and one-class-per-file checks.

        Args:
            content: Python source code to validate.
            file_path: Path to the file (for layer detection).

        Returns:
            List of violation description strings. Empty if compliant.
        """
        try:
            tree = ast.parse(content, filename=str(file_path))
        except SyntaxError:
            # Fail-open on syntax errors
            return []

        violations: list[str] = []

        # V-038: Import boundary validation
        violations.extend(self._check_imports(tree, file_path))

        # V-041: One-class-per-file
        violations.extend(self._check_one_class_per_file(tree, file_path))

        return violations

    def _check_imports(self, tree: ast.Module, file_path: Path) -> list[str]:
        """Check import statements against layer boundary rules (V-038).

        Validates that imports respect the hexagonal architecture
        dependency rules: domain cannot import application/infrastructure/
        interface, etc.

        Note on dynamic imports (design deviation DD-7):
            Dynamic imports that resolve to a boundary violation are
            **blocked** rather than warned.  The EPIC-002 design
            (REQ-403-035) specifies warnings, but blocking is the safer
            choice -- a dynamic import of a forbidden module is just as
            much a violation as a static import.

        Args:
            tree: Parsed AST module.
            file_path: Path to the file being checked.

        Returns:
            List of import boundary violation descriptions.
        """
        violations: list[str] = []

        # Check if file is exempt (bootstrap.py)
        if file_path.name in EXEMPT_FILES:
            return violations

        # Determine source layer
        source_layer = self._determine_layer(file_path)
        if source_layer is None:
            return violations

        # Check if this layer has import restrictions
        if source_layer not in LAYER_IMPORT_RULES:
            return violations

        for node in ast.walk(tree):
            # Skip TYPE_CHECKING conditional imports
            if self._is_type_checking_import(node, tree):
                continue

            if isinstance(node, ast.Import):
                for alias in node.names:
                    violation = self._check_import_boundary(source_layer, alias.name, node.lineno)
                    if violation:
                        violations.append(violation)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    violation = self._check_import_boundary(source_layer, node.module, node.lineno)
                    if violation:
                        violations.append(violation)

            elif isinstance(node, ast.Call):
                # Check for dynamic imports: __import__() and importlib.import_module()
                # Design deviation DD-7: blocks (not warns) to prevent
                # boundary violations from entering the codebase.
                if self._is_dynamic_import(node):
                    # Try to extract the module name from arguments
                    if node.args and isinstance(node.args[0], ast.Constant):
                        module_name = str(node.args[0].value)
                        violation = self._check_import_boundary(
                            source_layer, module_name, node.lineno
                        )
                        if violation:
                            violations.append(f"Dynamic import violation: {violation}")

        return violations

    def _check_import_boundary(
        self, source_layer: str, import_module: str, line_number: int
    ) -> str | None:
        """Check if a single import violates layer boundaries.

        Only checks imports that are project-internal (starting with ``src.``
        or beginning directly with a recognized layer name).  Third-party
        packages whose module path happens to include layer keywords
        (e.g. ``some_lib.domain.utils``) are ignored to avoid false positives.

        Args:
            source_layer: The layer of the file containing the import.
            import_module: The fully qualified module being imported.
            line_number: Line number of the import statement.

        Returns:
            Violation description string, or None if compliant.
        """
        forbidden_layers = LAYER_IMPORT_RULES.get(source_layer, set())

        # Only enforce boundary rules on project-internal imports.
        # Project imports start with "src." or begin directly with a
        # recognized layer name (e.g., "domain.entities").
        module_parts = import_module.split(".")
        if not self._is_project_import(module_parts):
            return None

        for part in module_parts:
            if part in RECOGNIZED_LAYERS and part in forbidden_layers:
                return (
                    f"Line {line_number}: {source_layer} layer cannot import "
                    f"from {part} (module: {import_module})"
                )

        return None

    @staticmethod
    def _is_project_import(module_parts: list[str]) -> bool:
        """Determine if an import is a project-internal import.

        Project-internal imports either start with ``src`` or begin with a
        recognized layer name.  Everything else is assumed to be a
        third-party or stdlib import and is exempt from boundary checking.

        Args:
            module_parts: The dotted module name split into parts.

        Returns:
            True if this looks like a project-internal import.
        """
        if not module_parts:
            return False

        # Imports starting with "src" are always project-internal
        if module_parts[0] == "src":
            return True

        # Imports starting directly with a recognized layer name
        # (e.g., "domain.entities") are also project-internal
        if module_parts[0] in RECOGNIZED_LAYERS:
            return True

        return False

    def _determine_layer(self, file_path: Path) -> str | None:
        """Determine which architectural layer a file belongs to.

        Maps file paths to layer names: domain, application,
        infrastructure, interface, shared_kernel.

        Args:
            file_path: Path to the file.

        Returns:
            Layer name string, or None if not in a recognized layer.
        """
        try:
            if file_path.is_absolute():
                rel_path = file_path.relative_to(self._project_root)
            else:
                rel_path = file_path
        except ValueError:
            return None

        parts = rel_path.parts

        # Look for layer directory in the path
        for part in parts:
            if part in RECOGNIZED_LAYERS:
                return part

        return None

    def _is_type_checking_import(self, node: ast.AST, tree: ast.Module) -> bool:
        """Check if an import is inside a TYPE_CHECKING conditional block.

        Imports guarded by ``if TYPE_CHECKING:`` are exempt from boundary
        checks because they are not executed at runtime.

        Args:
            node: The AST node to check.
            tree: The full AST module for context.

        Returns:
            True if the import is inside a TYPE_CHECKING block.
        """
        if not isinstance(node, ast.Import | ast.ImportFrom):
            return False

        # Walk the tree looking for If nodes that test TYPE_CHECKING
        for top_node in ast.walk(tree):
            if not isinstance(top_node, ast.If):
                continue

            # Check if the test is TYPE_CHECKING
            is_type_checking = False
            test = top_node.test

            if isinstance(test, ast.Name) and test.id == "TYPE_CHECKING":
                is_type_checking = True
            elif isinstance(test, ast.Attribute) and test.attr == "TYPE_CHECKING":
                is_type_checking = True

            if not is_type_checking:
                continue

            # Check if the import node is in the body of this If
            for child in ast.walk(top_node):
                if child is node:
                    return True

        return False

    def _is_dynamic_import(self, node: ast.Call) -> bool:
        """Check if a call node is a dynamic import.

        Detects ``__import__("module")`` and ``importlib.import_module("module")``.

        Args:
            node: The AST Call node to check.

        Returns:
            True if the call is a dynamic import.
        """
        # __import__("module")
        if isinstance(node.func, ast.Name) and node.func.id == "__import__":
            return True

        # importlib.import_module("module")
        if isinstance(node.func, ast.Attribute) and node.func.attr == "import_module":
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "importlib":
                return True

        return False

    def _check_one_class_per_file(self, tree: ast.Module, file_path: Path) -> list[str]:
        """Check one-class-per-file rule (V-041).

        Each Python file should contain at most one public class.
        Private classes (prefixed with underscore) are exempt.
        __init__.py files are exempt.

        Args:
            tree: Parsed AST module.
            file_path: Path to the file being checked.

        Returns:
            List of violation descriptions. Empty if compliant.
        """
        # __init__.py files are exempt
        if file_path.name == "__init__.py":
            return []

        public_classes: list[str] = []

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                # Skip private classes (underscore prefix)
                if not node.name.startswith("_"):
                    public_classes.append(node.name)

        if len(public_classes) > 1:
            return [
                f"One-class-per-file violation: found {len(public_classes)} "
                f"public classes ({', '.join(public_classes)}). "
                f"Each file should contain at most one public class."
            ]

        return []

    def _check_governance_escalation(self, file_path: str) -> str | None:
        """Check if a file requires governance criticality escalation.

        Governance files (constitution, rules) require elevated review
        when modified.

        Args:
            file_path: Path to the file being modified.

        Returns:
            Criticality level string ("C3" or "C4"), or None if no
            escalation is required.
        """
        # Normalize to relative path for matching
        try:
            path = Path(file_path)
            if path.is_absolute():
                rel_path = str(path.relative_to(self._project_root))
            else:
                rel_path = file_path
        except (ValueError, RuntimeError):
            rel_path = file_path

        # Normalize separators
        rel_path = rel_path.replace("\\", "/")

        # Check against governance patterns (most specific first)
        # Sort by length descending so specific patterns match before prefixes
        for pattern, criticality in sorted(
            GOVERNANCE_FILES.items(), key=lambda x: len(x[0]), reverse=True
        ):
            normalized_pattern = pattern.replace("\\", "/")
            if rel_path == normalized_pattern or rel_path.startswith(normalized_pattern):
                return criticality

        return None

    def _format_violations(self, violations: list[str], file_path: Path) -> str:
        """Format violation list into a human-readable reason string.

        Args:
            violations: List of violation description strings.
            file_path: Path to the file with violations.

        Returns:
            Formatted multi-line string describing all violations.
        """
        header = f"Architecture violations in {file_path.name}:"
        items = "\n".join(f"  - {v}" for v in violations)
        return f"{header}\n{items}"

    def _find_root(self) -> Path:
        """Find the project root by searching for CLAUDE.md.

        Walks upward from the current working directory looking for
        a CLAUDE.md file, which indicates the project root.

        Returns:
            Path to the project root directory.
        """
        current = Path.cwd()
        for parent in [current, *current.parents]:
            if (parent / "CLAUDE.md").exists():
                return parent
        # Fallback to CWD if no CLAUDE.md found
        return current
