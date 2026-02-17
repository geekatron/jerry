#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Pattern Library Loader

Loads and validates the guardrail pattern library for hook validation.

Work Item: WI-SAO-015
Task: T-015.2.3

Usage:
    from patterns.loader import PatternLibrary, load_patterns

    patterns = load_patterns()
    result = patterns.validate_input(tool_name="Write", text="content...")
"""

from __future__ import annotations

import json
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore


def _simple_yaml_parse(content: str) -> dict:
    """
    Simple YAML parser for pattern library format.

    This parser handles the subset of YAML used in patterns.yaml:
    - Key-value pairs
    - Nested dictionaries
    - Lists with - prefix
    - Strings (quoted and unquoted)
    - Comments (#)

    Note: This is NOT a full YAML parser. It's a fallback for
    environments without PyYAML installed.
    """

    result: dict = {}
    stack: list[tuple[int, dict | list, str | None]] = [(0, result, None)]
    lines = content.split("\n")

    for line in lines:
        # Skip empty lines and comments
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Calculate indentation
        indent = len(line) - len(line.lstrip())

        # Pop stack until we find the right level
        while stack and indent <= stack[-1][0] and len(stack) > 1:
            stack.pop()

        current_indent, current_container, current_key = stack[-1]

        # Handle list item
        if stripped.startswith("- "):
            value_str = stripped[2:].strip()
            if isinstance(current_container, list):
                # Parse the value
                value = _parse_yaml_value(value_str)
                if isinstance(value, dict):
                    current_container.append(value)
                    stack.append((indent + 2, value, None))
                else:
                    current_container.append(value)
            elif isinstance(current_container, dict) and current_key:
                # Create new list for this key
                new_list: list = []
                current_container[current_key] = new_list
                value = _parse_yaml_value(value_str)
                if isinstance(value, dict):
                    new_list.append(value)
                    stack.append((indent + 2, value, None))
                else:
                    new_list.append(value)
                stack.append((indent, new_list, None))
            continue

        # Handle key: value
        if ":" in stripped:
            colon_pos = stripped.find(":")
            key = stripped[:colon_pos].strip()
            value_str = stripped[colon_pos + 1 :].strip()

            if isinstance(current_container, dict):
                if value_str:
                    # Inline value
                    current_container[key] = _parse_yaml_value(value_str)
                else:
                    # Nested structure coming
                    current_container[key] = {}
                    stack.append((indent + 2, current_container[key], key))

    return result


def _parse_yaml_value(s: str) -> str | int | float | bool | dict | list:
    """Parse a YAML value string."""
    s = s.strip()

    # Remove comments
    if " #" in s:
        s = s[: s.find(" #")].strip()

    # Handle quoted strings
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]

    # Handle booleans
    if s.lower() in ("true", "yes"):
        return True
    if s.lower() in ("false", "no"):
        return False

    # Handle null
    if s.lower() in ("null", "~", ""):
        return ""

    # Handle numbers
    try:
        if "." in s:
            return float(s)
        return int(s)
    except ValueError:
        pass

    # Return as string
    return s


# =============================================================================
# DATA STRUCTURES
# =============================================================================


@dataclass
class PatternMatch:
    """Result of a pattern match."""

    rule_id: str
    pattern_group: str
    description: str
    severity: str
    matched_text: str
    start_pos: int
    end_pos: int


@dataclass
class ValidationResult:
    """Result of pattern validation."""

    decision: Literal["approve", "block", "warn", "ask"]
    reason: str
    matches: list[PatternMatch] = field(default_factory=list)
    elapsed_ms: float = 0.0

    def to_json(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict for hook output."""
        result: dict[str, Any] = {"decision": self.decision}
        if self.reason:
            result["reason"] = self.reason
        if self.matches:
            result["matches"] = [
                {
                    "rule_id": m.rule_id,
                    "severity": m.severity,
                    "description": m.description,
                }
                for m in self.matches
            ]
        return result


@dataclass
class PatternRule:
    """A single pattern rule."""

    id: str
    pattern: str
    description: str
    severity: str = "medium"
    mode: str | None = None
    applies_to: list[str] = field(default_factory=list)

    _compiled: re.Pattern | None = field(default=None, repr=False)

    def compile(self) -> re.Pattern:
        """Compile and cache the regex pattern."""
        if self._compiled is None:
            self._compiled = re.compile(self.pattern)
        return self._compiled


@dataclass
class PatternGroup:
    """A group of related patterns."""

    name: str
    description: str
    mode: str
    timeout_ms: int
    enabled: bool
    rules: list[PatternRule]
    action: str = "detect"
    replacement: str = "[REDACTED]"


# =============================================================================
# PATTERN LIBRARY
# =============================================================================


class PatternLibrary:
    """
    Guardrail pattern library for tool validation.

    Implements:
        - AC-015-001: Async validation (via subprocess hook model)
        - AC-015-002: timeout_ms: 100
        - AC-015-003: mode: warn
        - AC-015-004: Pattern library for common checks
    """

    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize from parsed YAML data."""
        self.schema_version = data.get("schema_version", "1.0.0")
        self.validation_modes = data.get("validation_modes", {})
        self.input_patterns = self._parse_pattern_groups(data.get("input_patterns", {}))
        self.output_patterns = self._parse_pattern_groups(data.get("output_patterns", {}))
        self.tool_rules = data.get("tool_rules", {})

    def _parse_pattern_groups(self, groups_data: dict[str, Any]) -> dict[str, PatternGroup]:
        """Parse pattern groups from YAML data."""
        groups = {}
        for name, group_data in groups_data.items():
            rules = [
                PatternRule(
                    id=r["id"],
                    pattern=r["pattern"],
                    description=r["description"],
                    severity=r.get("severity", "medium"),
                    mode=r.get("mode"),
                    applies_to=r.get("applies_to", []),
                )
                for r in group_data.get("rules", [])
            ]
            groups[name] = PatternGroup(
                name=group_data["name"],
                description=group_data["description"],
                mode=group_data["mode"],
                timeout_ms=group_data.get("timeout_ms", 100),
                enabled=group_data.get("enabled", True),
                rules=rules,
                action=group_data.get("action", "detect"),
                replacement=group_data.get("replacement", "[REDACTED]"),
            )
        return groups

    def get_patterns_for_tool(
        self, tool_name: str, pattern_type: str = "input"
    ) -> list[PatternGroup]:
        """Get pattern groups applicable to a specific tool."""
        tool_config = self.tool_rules.get(tool_name, {})
        pattern_key = f"{pattern_type}_patterns"
        pattern_names = tool_config.get(pattern_key, [])

        patterns = self.input_patterns if pattern_type == "input" else self.output_patterns
        return [patterns[name] for name in pattern_names if name in patterns]

    def validate_text(
        self,
        text: str,
        pattern_groups: list[PatternGroup],
        default_mode: str = "warn",
        timeout_ms: int = 100,
    ) -> ValidationResult:
        """
        Validate text against pattern groups.

        Args:
            text: Text to validate
            pattern_groups: Pattern groups to check
            default_mode: Default mode if group doesn't specify
            timeout_ms: Maximum time for validation (AC-015-002)

        Returns:
            ValidationResult with decision and matches
        """
        start_time = time.time()
        matches: list[PatternMatch] = []
        highest_severity_mode = "approve"
        severity_order = {"approve": 0, "warn": 1, "ask": 2, "block": 3}

        for group in pattern_groups:
            if not group.enabled:
                continue

            # Check timeout
            elapsed = (time.time() - start_time) * 1000
            if elapsed >= timeout_ms:
                break

            for rule in group.rules:
                try:
                    compiled = rule.compile()
                    for match in compiled.finditer(text):
                        pattern_match = PatternMatch(
                            rule_id=rule.id,
                            pattern_group=group.name,
                            description=rule.description,
                            severity=rule.severity,
                            matched_text=match.group(),
                            start_pos=match.start(),
                            end_pos=match.end(),
                        )
                        matches.append(pattern_match)

                        # Determine mode for this match
                        mode = rule.mode or group.mode or default_mode
                        if severity_order.get(mode, 0) > severity_order.get(
                            highest_severity_mode, 0
                        ):
                            highest_severity_mode = mode
                except re.error:
                    # Invalid regex - skip this rule
                    continue

        elapsed_ms = (time.time() - start_time) * 1000

        if not matches:
            return ValidationResult(
                decision="approve", reason="", matches=[], elapsed_ms=elapsed_ms
            )

        # Build reason from matches
        reasons = [f"{m.rule_id}: {m.description}" for m in matches[:3]]
        if len(matches) > 3:
            reasons.append(f"... and {len(matches) - 3} more")
        reason = "; ".join(reasons)

        return ValidationResult(
            decision=highest_severity_mode,  # type: ignore
            reason=reason,
            matches=matches,
            elapsed_ms=elapsed_ms,
        )

    def validate_input(self, tool_name: str, tool_input: dict[str, Any]) -> ValidationResult:
        """
        Validate tool input against applicable patterns.

        Args:
            tool_name: Name of the tool being called
            tool_input: Tool input parameters

        Returns:
            ValidationResult with decision and matches
        """
        # Get applicable patterns
        pattern_groups = self.get_patterns_for_tool(tool_name, "input")

        if not pattern_groups:
            # No patterns configured for this tool - apply all input patterns
            pattern_groups = list(self.input_patterns.values())

        # Get tool fallback mode
        fallback_mode = self.tool_rules.get(tool_name, {}).get("fallback_mode", "warn")

        # Convert input to searchable text
        text = json.dumps(tool_input, default=str)

        return self.validate_text(
            text=text,
            pattern_groups=pattern_groups,
            default_mode=fallback_mode,
            timeout_ms=100,  # AC-015-002
        )

    def validate_output(self, tool_name: str, output: str) -> ValidationResult:
        """
        Validate tool output against applicable patterns.

        Args:
            tool_name: Name of the tool
            output: Tool output text

        Returns:
            ValidationResult with decision and matches
        """
        pattern_groups = self.get_patterns_for_tool(tool_name, "output")

        if not pattern_groups:
            pattern_groups = list(self.output_patterns.values())

        return self.validate_text(
            text=output,
            pattern_groups=pattern_groups,
            default_mode="warn",
            timeout_ms=100,
        )


# =============================================================================
# LOADING FUNCTIONS
# =============================================================================


def load_patterns(
    patterns_path: Path | str | None = None,
) -> PatternLibrary:
    """
    Load pattern library from YAML or JSON file.

    Priority:
        1. If PyYAML is available, use patterns.yaml
        2. If PyYAML not available, use patterns.json
        3. Fall back to empty library

    Args:
        patterns_path: Path to patterns file (default: auto-detect)

    Returns:
        PatternLibrary instance
    """
    base_dir = Path(__file__).parent

    # Determine which file to use
    if patterns_path is None:
        if yaml is not None:
            patterns_path = base_dir / "patterns.yaml"
        else:
            # Prefer JSON when YAML not available
            json_path = base_dir / "patterns.json"
            yaml_path = base_dir / "patterns.yaml"
            patterns_path = json_path if json_path.exists() else yaml_path
    else:
        patterns_path = Path(patterns_path)

    if not patterns_path.exists():
        # Return empty library if file doesn't exist
        return PatternLibrary(
            {
                "schema_version": "1.0.0",
                "validation_modes": {},
                "input_patterns": {},
                "output_patterns": {},
                "tool_rules": {},
            }
        )

    content = patterns_path.read_text()

    # Parse based on file extension and available libraries
    if patterns_path.suffix == ".json":
        data = json.loads(content)
    elif yaml is not None:
        data = yaml.safe_load(content)
    else:
        # Fallback: try JSON parsing
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            # Cannot parse YAML without library
            return PatternLibrary(
                {
                    "schema_version": "1.0.0",
                    "validation_modes": {},
                    "input_patterns": {},
                    "output_patterns": {},
                    "tool_rules": {},
                }
            )

    return PatternLibrary(data)


# =============================================================================
# CLI INTERFACE
# =============================================================================


def main() -> int:
    """CLI interface for testing pattern loading."""
    patterns = load_patterns()
    print(f"Loaded pattern library v{patterns.schema_version}")
    print(f"Input pattern groups: {len(patterns.input_patterns)}")
    print(f"Output pattern groups: {len(patterns.output_patterns)}")
    print(f"Tool rules: {len(patterns.tool_rules)}")

    # Test validation
    test_input = {"command": "echo password='secret123'"}
    result = patterns.validate_input("Bash", test_input)
    print(f"\nTest validation: {result.decision}")
    if result.matches:
        print(f"Matches: {len(result.matches)}")
        for m in result.matches:
            print(f"  - {m.rule_id}: {m.description}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
