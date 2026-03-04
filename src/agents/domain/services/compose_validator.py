# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ComposeValidator - Post-composition validation for composed agent output.

Checks composed .md agent files for known regression patterns and
structural issues. Returns structured warnings/errors to prevent
silent regressions from reaching the composed output.

Checks:
    CV-001: No JERRY_PLUGIN_ROOT in composed output
    CV-002: No Python API imports in composed output
    CV-003: Governance sections present when source declares them
    CV-004: No abstract tool names leaked into composed output
    CV-005: Required frontmatter fields present
    CV-006: No governance fields in frontmatter
    CV-007: Frontmatter validates against Anthropic agent spec schema

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
    - P-022: No Deception (silent pass-through violates this)
    - H-31: Clarify when ambiguous
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from src.agents.domain.value_objects.compose_validation_result import (
    ComposeValidationResult,
)
from src.agents.domain.value_objects.validation_finding import ValidationFinding

# Re-export for backward compatibility — consuming modules may import from here
__all__ = ["ComposeValidationResult", "ComposeValidator", "ValidationFinding"]

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None  # type: ignore[assignment]


# Regex for code blocks to exclude from pattern matching
_CODE_BLOCK_RE = re.compile(r"```[\s\S]*?```", re.MULTILINE)

# CV-001: JERRY_PLUGIN_ROOT patterns (should be CLAUDE_PLUGIN_ROOT)
_JERRY_PLUGIN_ROOT_RE = re.compile(r"\$\{?JERRY_PLUGIN_ROOT\}?")

# CV-002: Python API imports (should be CLI commands or vendor tool names)
_PYTHON_API_IMPORT_RE = re.compile(r"from\s+skills\.\w+\.scripts")

# CV-004: Abstract tool names that should have been mapped to vendor names
_ABSTRACT_TOOL_NAMES = (
    "file_read",
    "file_write",
    "file_edit",
    "file_search_glob",
    "file_search_content",
    "shell_execute",
    "web_search",
    "web_fetch",
    "agent_delegate",
)

# CV-006: Governance fields that must NOT appear in YAML frontmatter
_GOVERNANCE_FRONTMATTER_FIELDS = {
    "version",
    "tool_tier",
    "identity",
    "persona",
    "capabilities",
    "guardrails",
    "constitution",
    "enforcement",
    "portability",
    "session_context",
    "prior_art",
    "validation",
    "output",
}

# CV-003: Governance sections expected in body (heading text)
_GOVERNANCE_HEADINGS = {
    "version": ("Agent Version", "agent_version"),
    "tool_tier": ("Tool Tier", "tool_tier"),
}


def _strip_code_blocks(text: str) -> str:
    """Remove fenced code blocks from text to avoid false positives.

    Args:
        text: Markdown text potentially containing code blocks.

    Returns:
        Text with code blocks removed.
    """
    return _CODE_BLOCK_RE.sub("", text)


def _parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter from composed .md content.

    Args:
        content: Full .md file content.

    Returns:
        Tuple of (frontmatter_dict, body_string). Empty dict if
        frontmatter is missing or invalid.
    """
    if not content.startswith("---"):
        return {}, content

    end = content.find("---", 3)
    if end == -1:
        return {}, content

    fm_text = content[3:end].strip()
    body = content[end + 3 :].lstrip("\n")

    try:
        fm_data = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        fm_data = {}

    return fm_data, body


class ComposeValidator:
    """Post-composition validator for composed agent .md files.

    Runs deterministic checks against composed output to catch
    known regression patterns before they ship.

    Attributes:
        _anthropic_schema: Loaded JSON Schema for frontmatter validation.
    """

    # Claude Code's 12 official frontmatter fields
    _VENDOR_FIELDS: frozenset[str] = frozenset(
        {
            "name",
            "description",
            "model",
            "tools",
            "disallowedTools",
            "mcpServers",
            "permissionMode",
            "maxTurns",
            "skills",
            "hooks",
            "memory",
            "background",
            "isolation",
        }
    )

    def __init__(self, anthropic_schema_path: Path | None = None) -> None:
        """Initialize with optional Anthropic schema for CV-007.

        Args:
            anthropic_schema_path: Path to jerry-claude-agent-definition-v1.schema.json.
                If None, CV-007 is skipped.
        """
        self._anthropic_schema: dict[str, Any] | None = None
        if anthropic_schema_path and anthropic_schema_path.exists():
            import json

            schema_text = anthropic_schema_path.read_text(encoding="utf-8")
            self._anthropic_schema = json.loads(schema_text)

    def validate(
        self,
        composed_content: str,
        agent_name: str = "",
        governance_source: dict[str, Any] | None = None,
    ) -> ComposeValidationResult:
        """Validate composed agent .md content.

        Args:
            composed_content: Full composed .md file content.
            agent_name: Agent name for error reporting.
            governance_source: Optional governance data from .jerry.yaml
                for CV-003 cross-reference.

        Returns:
            ComposeValidationResult with errors and warnings.
        """
        result = ComposeValidationResult(agent_name=agent_name)
        frontmatter, body = _parse_frontmatter(composed_content)

        self._check_cv001(body, agent_name, result)
        self._check_cv002(body, agent_name, result)
        self._check_cv003(body, agent_name, governance_source, result)
        self._check_cv004(body, agent_name, result)
        self._check_cv005(frontmatter, agent_name, result)
        self._check_cv006(frontmatter, agent_name, result)
        self._check_cv007(frontmatter, agent_name, result)

        return result

    def _check_cv001(
        self,
        body: str,
        agent_name: str,
        result: ComposeValidationResult,
    ) -> None:
        """CV-001: No JERRY_PLUGIN_ROOT in composed output.

        Args:
            body: Prompt body content.
            agent_name: Agent name for reporting.
            result: Result to append findings to.
        """
        body_no_code = _strip_code_blocks(body)
        if _JERRY_PLUGIN_ROOT_RE.search(body_no_code):
            result.errors.append(
                ValidationFinding(
                    check_id="CV-001",
                    severity="error",
                    message="JERRY_PLUGIN_ROOT found in composed output; should be CLAUDE_PLUGIN_ROOT",
                    agent_name=agent_name,
                )
            )

    def _check_cv002(
        self,
        body: str,
        agent_name: str,
        result: ComposeValidationResult,
    ) -> None:
        """CV-002: No Python API imports in composed output.

        Args:
            body: Prompt body content.
            agent_name: Agent name for reporting.
            result: Result to append findings to.
        """
        body_no_code = _strip_code_blocks(body)
        if _PYTHON_API_IMPORT_RE.search(body_no_code):
            result.errors.append(
                ValidationFinding(
                    check_id="CV-002",
                    severity="error",
                    message="Python API import (from skills.*.scripts) found in composed output",
                    agent_name=agent_name,
                )
            )

    def _check_cv003(
        self,
        body: str,
        agent_name: str,
        governance_source: dict[str, Any] | None,
        result: ComposeValidationResult,
    ) -> None:
        """CV-003: Governance sections present when source declares them.

        Args:
            body: Prompt body content.
            agent_name: Agent name for reporting.
            governance_source: Governance data from .jerry.yaml.
            result: Result to append findings to.
        """
        if not governance_source:
            return

        for field_key, (md_heading, xml_tag) in _GOVERNANCE_HEADINGS.items():
            if field_key in governance_source and governance_source[field_key]:
                # Check for structural markdown heading (not substring in paragraph)
                heading_pattern = re.compile(
                    rf"^##\s+{re.escape(md_heading)}\s*$",
                    re.MULTILINE | re.IGNORECASE,
                )
                has_md = bool(heading_pattern.search(body))
                has_xml = f"<{xml_tag}>" in body.lower()
                if not has_md and not has_xml:
                    result.warnings.append(
                        ValidationFinding(
                            check_id="CV-003",
                            severity="warning",
                            message=(
                                f"Governance field '{field_key}' declared in source "
                                f"but '## {md_heading}' / '<{xml_tag}>' not found in body"
                            ),
                            agent_name=agent_name,
                        )
                    )

    def _check_cv004(
        self,
        body: str,
        agent_name: str,
        result: ComposeValidationResult,
    ) -> None:
        """CV-004: No abstract tool names leaked into composed output.

        Args:
            body: Prompt body content.
            agent_name: Agent name for reporting.
            result: Result to append findings to.
        """
        body_no_code = _strip_code_blocks(body)

        for tool_name in _ABSTRACT_TOOL_NAMES:
            # Match as whole word to avoid false positives in natural text
            pattern = re.compile(rf"\b{re.escape(tool_name)}\b")
            if pattern.search(body_no_code):
                result.warnings.append(
                    ValidationFinding(
                        check_id="CV-004",
                        severity="warning",
                        message=f"Abstract tool name '{tool_name}' found in composed output (outside code blocks)",
                        agent_name=agent_name,
                    )
                )

    def _check_cv005(
        self,
        frontmatter: dict[str, Any],
        agent_name: str,
        result: ComposeValidationResult,
    ) -> None:
        """CV-005: Required frontmatter fields present.

        Args:
            frontmatter: Parsed YAML frontmatter.
            agent_name: Agent name for reporting.
            result: Result to append findings to.
        """
        for required_field in ("name", "description"):
            if required_field not in frontmatter or not frontmatter[required_field]:
                result.errors.append(
                    ValidationFinding(
                        check_id="CV-005",
                        severity="error",
                        message=f"Required frontmatter field '{required_field}' is missing or empty",
                        agent_name=agent_name,
                    )
                )

    def _check_cv006(
        self,
        frontmatter: dict[str, Any],
        agent_name: str,
        result: ComposeValidationResult,
    ) -> None:
        """CV-006: No governance fields in frontmatter.

        Args:
            frontmatter: Parsed YAML frontmatter.
            agent_name: Agent name for reporting.
            result: Result to append findings to.
        """
        leaked = {k for k in frontmatter if k.lower() in _GOVERNANCE_FRONTMATTER_FIELDS}
        for leaked_field in sorted(leaked):
            result.errors.append(
                ValidationFinding(
                    check_id="CV-006",
                    severity="error",
                    message=f"Governance field '{leaked_field}' found in YAML frontmatter (should be in body only)",
                    agent_name=agent_name,
                )
            )

    def _check_cv007(
        self,
        frontmatter: dict[str, Any],
        agent_name: str,
        result: ComposeValidationResult,
    ) -> None:
        """CV-007: Frontmatter validates against Anthropic agent spec schema.

        Only validates the subset of the schema that applies to
        Claude Code's 12 official frontmatter fields.

        Args:
            frontmatter: Parsed YAML frontmatter.
            agent_name: Agent name for reporting.
            result: Result to append findings to.
        """
        if self._anthropic_schema is None:
            return

        if jsonschema is None:
            return  # pragma: no cover

        # Build a frontmatter-only schema from the full schema
        fm_schema = self._build_frontmatter_schema()
        if not fm_schema:
            return

        try:
            jsonschema.validate(instance=frontmatter, schema=fm_schema)
        except jsonschema.ValidationError as e:
            result.errors.append(
                ValidationFinding(
                    check_id="CV-007",
                    severity="error",
                    message=f"Frontmatter schema validation failed: {e.message}",
                    agent_name=agent_name,
                )
            )

    def _build_frontmatter_schema(self) -> dict[str, Any]:
        """Build a JSON Schema for frontmatter-only validation.

        Extracts only the Claude Code official fields from the full
        Anthropic schema and makes only 'name' and 'description' required.

        Claude Code accepts both string and array for 'tools' and
        'disallowedTools' (e.g. ``tools: Read, Write`` or ``tools: [Read, Write]``).
        The canonical schema defines array-only; this method widens those
        fields to accept both formats for composed output validation.

        Returns:
            JSON Schema dict for frontmatter validation.
        """
        if self._anthropic_schema is None:
            return {}

        full_props = self._anthropic_schema.get("properties", {})
        fm_props: dict[str, Any] = {}
        for field_name in self._VENDOR_FIELDS:
            if field_name in full_props:
                fm_props[field_name] = full_props[field_name]

        # Claude Code accepts both string and array for tools fields.
        # The compose pipeline produces comma-separated string format.
        # Widen the schema to accept both.
        for tools_field in ("tools", "disallowedTools"):
            if tools_field in fm_props:
                original = fm_props[tools_field]
                items_schema = original.get("items", {"type": "string"})
                fm_props[tools_field] = {
                    "oneOf": [
                        {"type": "string"},
                        {"type": "array", "items": items_schema},
                    ],
                    "description": original.get("description", ""),
                }

        # Claude Code accepts mcpServers as object (name -> config) or array.
        # The compose pipeline produces object format: {context7: true}.
        if "mcpServers" in fm_props:
            original = fm_props["mcpServers"]
            fm_props["mcpServers"] = {
                "oneOf": [
                    {"type": "object"},
                    {"type": "array", "items": {"type": "object"}},
                ],
                "description": original.get("description", ""),
            }

        # Copy $defs for references
        defs = self._anthropic_schema.get("$defs", {})

        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "properties": fm_props,
            "required": ["name", "description"],
            "additionalProperties": False,
            "$defs": defs,
        }
