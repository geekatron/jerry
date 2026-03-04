# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
SkillComposeValidator - Post-composition validation for composed SKILL.md output.

Checks composed SKILL.md files for structural issues and governance compliance.
Returns structured warnings/errors to prevent silent regressions.

Checks:
    SCV-001: No Jerry extension fields in frontmatter
    SCV-002: Required Anthropic fields present (name, description)
    SCV-003: Governance sections present when canonical source declares them
    SCV-004: Frontmatter validates against anthropic-skill-frontmatter-v1.schema.json
    SCV-005: Name matches folder name, lowercase kebab-case (H-25)
    SCV-006: Description under 1024 chars, no XML brackets (H-26)
    SCV-007: Canonical source name matches frontmatter name (cross-file consistency)
    SCV-008: All agents within a skill declare the same body_format
    SCV-009: Canonical description matches frontmatter description (cross-file consistency)

References:
    - PROJ-012: Skill Composition Pipeline
    - P-022: No Deception (silent pass-through violates this)
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from src.agents.domain.services.compose_validator import (
    ComposeValidationResult,
    ValidationFinding,
)

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None  # type: ignore[assignment]


# Jerry extension fields that must NOT appear in SKILL.md frontmatter
_JERRY_EXTENSION_FIELDS = {
    "version",
    "activation-keywords",
    "agents",
    "context_injection",
    "license",
    "compatibility",
    "metadata",
}

# H-25: Skill name must be lowercase kebab-case
_KEBAB_CASE_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")

# H-26: No XML brackets in description
_XML_BRACKET_RE = re.compile(r"<[^>]+>")


def _parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter from SKILL.md content.

    Args:
        content: Full SKILL.md file content.

    Returns:
        Tuple of (frontmatter_dict, body_string). Empty dict if
        frontmatter is missing or invalid.
    """
    if not content.startswith("---"):
        return {}, content

    end = content.find("\n---", 3)
    if end == -1:
        return {}, content

    fm_text = content[4:end]
    body = content[end + 4 :].lstrip("\n")

    try:
        fm_data = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        fm_data = {}

    return fm_data, body


class SkillComposeValidator:
    """Post-composition validator for composed SKILL.md files.

    Runs deterministic checks against composed output to catch
    known regression patterns before they ship.

    Attributes:
        _anthropic_schema: Loaded JSON Schema for frontmatter validation.
    """

    def __init__(self, anthropic_schema_path: Path | None = None) -> None:
        """Initialize with optional Anthropic skill schema for SCV-004.

        Args:
            anthropic_schema_path: Path to anthropic-skill-frontmatter-v1.schema.json.
                If None, SCV-004 is skipped.
        """
        self._anthropic_schema: dict[str, Any] | None = None
        if anthropic_schema_path and anthropic_schema_path.exists():
            import json

            schema_text = anthropic_schema_path.read_text(encoding="utf-8")
            self._anthropic_schema = json.loads(schema_text)

    def validate(
        self,
        composed_content: str,
        skill_name: str = "",
        folder_name: str = "",
        governance_source: dict[str, Any] | None = None,
        canonical_name: str = "",
        agent_body_formats: dict[str, str] | None = None,
        canonical_description: str = "",
    ) -> ComposeValidationResult:
        """Validate composed SKILL.md content.

        Args:
            composed_content: Full composed SKILL.md file content.
            skill_name: Skill name for error reporting.
            folder_name: Skill folder name for SCV-005 cross-check.
            governance_source: Optional canonical source data from skill.jerry.yaml
                for SCV-003 cross-reference.
            canonical_name: Name from the canonical skill.jerry.yaml source for
                SCV-007 cross-file consistency check.
            agent_body_formats: Optional dict of agent_name -> body_format for
                SCV-008 cross-agent consistency check.
            canonical_description: Description from the canonical skill.jerry.yaml
                source for SCV-009 cross-file consistency check.

        Returns:
            ComposeValidationResult with errors and warnings.
        """
        result = ComposeValidationResult(agent_name=skill_name)
        frontmatter, body = _parse_frontmatter(composed_content)

        self._check_scv001(frontmatter, skill_name, result)
        self._check_scv002(frontmatter, skill_name, result)
        self._check_scv003(body, skill_name, governance_source, result)
        self._check_scv004(frontmatter, skill_name, result)
        self._check_scv005(frontmatter, skill_name, folder_name, result)
        self._check_scv006(frontmatter, skill_name, result)
        self._check_scv007(frontmatter, skill_name, canonical_name, result)
        self._check_scv008(skill_name, agent_body_formats, result)
        self._check_scv009(frontmatter, skill_name, canonical_description, result)

        return result

    def _check_scv001(
        self,
        frontmatter: dict[str, Any],
        skill_name: str,
        result: ComposeValidationResult,
    ) -> None:
        """SCV-001: No Jerry extension fields in frontmatter.

        Args:
            frontmatter: Parsed YAML frontmatter.
            skill_name: Skill name for reporting.
            result: Result to append findings to.
        """
        leaked = {k for k in frontmatter if k.lower() in _JERRY_EXTENSION_FIELDS}
        for leaked_field in sorted(leaked):
            result.errors.append(
                ValidationFinding(
                    check_id="SCV-001",
                    severity="error",
                    message=f"Jerry extension field '{leaked_field}' found in SKILL.md frontmatter (should be in canonical source only)",
                    agent_name=skill_name,
                )
            )

    def _check_scv002(
        self,
        frontmatter: dict[str, Any],
        skill_name: str,
        result: ComposeValidationResult,
    ) -> None:
        """SCV-002: Required Anthropic fields present (name, description).

        Args:
            frontmatter: Parsed YAML frontmatter.
            skill_name: Skill name for reporting.
            result: Result to append findings to.
        """
        for required_field in ("name", "description"):
            if required_field not in frontmatter or not frontmatter[required_field]:
                result.errors.append(
                    ValidationFinding(
                        check_id="SCV-002",
                        severity="error",
                        message=f"Required Anthropic field '{required_field}' is missing or empty",
                        agent_name=skill_name,
                    )
                )

    # Mapping from governance field key to (heading_text, xml_tag) for dual detection
    _GOVERNANCE_SECTION_MAP: list[tuple[str, str, str]] = [
        ("version", "Skill Version", "skill_version"),
        ("activation-keywords", "Activation Keywords", "activation_keywords"),
        ("agents", "Agent Registry", "agent_registry"),
        ("context_injection", "Context Injection", "context_injection"),
    ]

    def _check_scv003(
        self,
        body: str,
        skill_name: str,
        governance_source: dict[str, Any] | None,
        result: ComposeValidationResult,
    ) -> None:
        """SCV-003: Governance sections present when canonical source declares them.

        Detects both ## Heading format and <xml_tag> format to support
        composed output in either format.

        Args:
            body: SKILL.md body content.
            skill_name: Skill name for reporting.
            governance_source: Canonical source data from skill.jerry.yaml.
            result: Result to append findings to.
        """
        if not governance_source:
            return

        # Required governance fields escalate to error; optional remain warning
        required_fields = {"version", "activation-keywords"}

        for field_key, heading_text, xml_tag in self._GOVERNANCE_SECTION_MAP:
            value = governance_source.get(field_key)
            if value:
                # Check for ## Heading format
                heading_pattern = re.compile(
                    rf"^##\s+{re.escape(heading_text)}\s*$",
                    re.MULTILINE | re.IGNORECASE,
                )
                # Check for <xml_tag> format
                xml_pattern = re.compile(rf"<{xml_tag}[\s/>]")

                if not heading_pattern.search(body) and not xml_pattern.search(body):
                    is_required = field_key in required_fields
                    severity = "error" if is_required else "warning"
                    finding = ValidationFinding(
                        check_id="SCV-003",
                        severity=severity,
                        message=(
                            f"Governance field '{field_key}' declared in canonical source "
                            f"but neither '## {heading_text}' heading nor '<{xml_tag}>' "
                            f"tag found in body"
                        ),
                        agent_name=skill_name,
                    )
                    if is_required:
                        result.errors.append(finding)
                    else:
                        result.warnings.append(finding)

    def _check_scv004(
        self,
        frontmatter: dict[str, Any],
        skill_name: str,
        result: ComposeValidationResult,
    ) -> None:
        """SCV-004: Frontmatter validates against anthropic-skill-frontmatter-v1.schema.json.

        Args:
            frontmatter: Parsed YAML frontmatter.
            skill_name: Skill name for reporting.
            result: Result to append findings to.
        """
        if self._anthropic_schema is None:
            return

        if jsonschema is None:  # FM-08: Warn instead of silent skip when jsonschema missing
            result.warnings.append(
                ValidationFinding(
                    check_id="SCV-004",
                    severity="warning",
                    message="jsonschema package not installed — schema validation skipped",
                    agent_name=skill_name,
                )
            )
            return

        try:
            jsonschema.validate(instance=frontmatter, schema=self._anthropic_schema)
        except jsonschema.ValidationError as e:
            result.errors.append(
                ValidationFinding(
                    check_id="SCV-004",
                    severity="error",
                    message=f"Frontmatter schema validation failed: {e.message}",
                    agent_name=skill_name,
                )
            )

    def _check_scv005(
        self,
        frontmatter: dict[str, Any],
        skill_name: str,
        folder_name: str,
        result: ComposeValidationResult,
    ) -> None:
        """SCV-005: Name matches folder name, lowercase kebab-case (H-25).

        Args:
            frontmatter: Parsed YAML frontmatter.
            skill_name: Skill name for reporting.
            folder_name: Skill folder name for cross-check.
            result: Result to append findings to.
        """
        name = frontmatter.get("name", "")
        if not name:
            return  # SCV-002 will catch missing name

        if not _KEBAB_CASE_RE.match(name):
            result.errors.append(
                ValidationFinding(
                    check_id="SCV-005",
                    severity="error",
                    message=f"Skill name '{name}' is not lowercase kebab-case",
                    agent_name=skill_name,
                )
            )

        if folder_name and name != folder_name:
            result.errors.append(
                ValidationFinding(
                    check_id="SCV-005",
                    severity="error",
                    message=f"Skill name '{name}' does not match folder name '{folder_name}'",
                    agent_name=skill_name,
                )
            )

    def _check_scv006(
        self,
        frontmatter: dict[str, Any],
        skill_name: str,
        result: ComposeValidationResult,
    ) -> None:
        """SCV-006: Description under 1024 chars, no XML brackets (H-26).

        Args:
            frontmatter: Parsed YAML frontmatter.
            skill_name: Skill name for reporting.
            result: Result to append findings to.
        """
        description = frontmatter.get("description", "")
        if not description:
            return  # SCV-002 will catch missing description

        if len(description) > 1024:
            result.errors.append(
                ValidationFinding(
                    check_id="SCV-006",
                    severity="error",
                    message=f"Description exceeds 1024 characters ({len(description)} chars)",
                    agent_name=skill_name,
                )
            )

        if _XML_BRACKET_RE.search(description):
            result.errors.append(
                ValidationFinding(
                    check_id="SCV-006",
                    severity="error",
                    message="Description contains XML brackets (<>)",
                    agent_name=skill_name,
                )
            )

    def _check_scv008(
        self,
        skill_name: str,
        agent_body_formats: dict[str, str] | None,
        result: ComposeValidationResult,
    ) -> None:
        """SCV-008: All agents within a skill must declare the same body_format.

        Args:
            skill_name: Skill name for reporting.
            agent_body_formats: Dict of agent_name -> body_format string.
            result: Result to append findings to.
        """
        if not agent_body_formats or len(agent_body_formats) < 2:
            return  # Nothing to check with 0-1 agents

        unique_formats = set(agent_body_formats.values())
        if len(unique_formats) <= 1:
            return  # All consistent

        # Build a readable breakdown: format -> [agent names]
        format_groups: dict[str, list[str]] = {}
        for agent, fmt in sorted(agent_body_formats.items()):
            format_groups.setdefault(fmt, []).append(agent)

        parts = [f"{fmt} ({', '.join(agents)})" for fmt, agents in sorted(format_groups.items())]
        result.errors.append(
            ValidationFinding(
                check_id="SCV-008",
                severity="error",
                message=(f"Inconsistent body_format within skill: {'; '.join(parts)}"),
                agent_name=skill_name,
            )
        )

    def _check_scv009(
        self,
        frontmatter: dict[str, Any],
        skill_name: str,
        canonical_description: str,
        result: ComposeValidationResult,
    ) -> None:
        """SCV-009: Canonical description matches frontmatter description.

        Catches drift if someone edits the composed SKILL.md directly
        instead of the canonical skill.jerry.yaml source.

        Args:
            frontmatter: Parsed YAML frontmatter.
            skill_name: Skill name for reporting.
            canonical_description: Description from skill.jerry.yaml.
            result: Result to append findings to.
        """
        if not canonical_description:
            return  # No canonical description provided — skip cross-check

        fm_description = frontmatter.get("description", "")
        if not fm_description:
            return  # SCV-002 will catch missing description

        if fm_description != canonical_description:
            result.warnings.append(
                ValidationFinding(
                    check_id="SCV-009",
                    severity="warning",
                    message=(
                        "Canonical description does not match frontmatter description. "
                        "Edit skill.jerry.yaml instead of SKILL.md directly."
                    ),
                    agent_name=skill_name,
                )
            )

    # FM-03: Cross-file name consistency check (canonical name vs frontmatter name)
    def _check_scv007(
        self,
        frontmatter: dict[str, Any],
        skill_name: str,
        canonical_name: str,
        result: ComposeValidationResult,
    ) -> None:
        """SCV-007: Canonical name matches frontmatter name (cross-file consistency).

        Args:
            frontmatter: Parsed YAML frontmatter.
            skill_name: Skill name for reporting.
            canonical_name: Name from the canonical skill.jerry.yaml source.
            result: Result to append findings to.
        """
        if not canonical_name:
            return  # No canonical source provided — skip cross-check

        fm_name = frontmatter.get("name", "")
        if not fm_name:
            return  # SCV-002 will catch missing name

        if fm_name != canonical_name:
            result.errors.append(
                ValidationFinding(
                    check_id="SCV-007",
                    severity="error",
                    message=(
                        f"Canonical source name '{canonical_name}' does not match "
                        f"frontmatter name '{fm_name}'"
                    ),
                    agent_name=skill_name,
                )
            )
