# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for ComposeValidator — 7 checks (CV-001 through CV-007).

Follows Jerry testing standards: H-20 BDD, AAA pattern, 60/30/10 distribution.

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
    - P-022: No Deception (silent pass-through violates this)
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from src.agents.domain.services.compose_validator import (
    ComposeValidator,
)


def _make_composed_md(
    frontmatter: dict[str, Any] | None = None,
    body: str = "## Identity\n\nYou are test-agent.\n",
) -> str:
    """Build a composed .md string from frontmatter dict and body.

    Args:
        frontmatter: YAML frontmatter fields. Defaults to valid minimal set.
        body: Markdown body content.

    Returns:
        Composed .md file content.
    """
    import yaml

    if frontmatter is None:
        frontmatter = {
            "name": "test-agent",
            "description": "A test agent for validation",
            "model": "sonnet",
        }
    fm_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
    return f"---\n{fm_str}---\n{body}"


@pytest.fixture()
def validator() -> ComposeValidator:
    """ComposeValidator without schema (CV-007 skipped)."""
    return ComposeValidator()


@pytest.fixture()
def validator_with_schema(tmp_path: Path) -> ComposeValidator:
    """ComposeValidator with a minimal Anthropic schema for CV-007."""
    schema: dict[str, Any] = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["name", "description"],
        "$defs": {
            "kebab_case_name": {
                "type": "string",
                "pattern": "^[a-z]+-[a-z]+(-[a-z]+)*$",
            },
        },
        "properties": {
            "name": {"$ref": "#/$defs/kebab_case_name"},
            "description": {"type": "string", "maxLength": 1024},
            "model": {"type": "string", "enum": ["opus", "sonnet", "haiku"]},
            "tools": {"type": "string"},
            "maxTurns": {"type": "integer", "minimum": 1},
            "permissionMode": {
                "type": "string",
                "enum": ["default", "acceptEdits", "dontAsk", "bypassPermissions", "plan"],
            },
            "background": {"type": "boolean"},
            "mcpServers": {"type": "object"},
            "disallowedTools": {"type": "string"},
            "skills": {"type": "array", "items": {"type": "string"}},
            "hooks": {"type": "object"},
            "memory": {"type": "string", "enum": ["user", "project", "local"]},
            "isolation": {"type": "string", "enum": ["worktree"]},
        },
    }
    schema_path = tmp_path / "test-schema.json"
    schema_path.write_text(json.dumps(schema), encoding="utf-8")
    return ComposeValidator(anthropic_schema_path=schema_path)


# =============================================================================
# Happy path (60%)
# =============================================================================


@pytest.mark.unit
class TestComposeValidatorHappyPath:
    """Happy-path tests: valid content produces no findings."""

    @pytest.mark.happy_path
    def test_validate_when_valid_composed_content_then_no_errors(
        self, validator: ComposeValidator
    ) -> None:
        """GIVEN valid composed .md content
        WHEN validated
        THEN no errors or warnings are returned."""
        # Arrange
        content = _make_composed_md(
            body="## Identity\n\nYou are test-agent.\n\n## Agent Version\n\n1.0.0\n"
        )

        # Act
        result = validator.validate(content, "test-agent")

        # Assert
        assert result.is_valid
        assert len(result.errors) == 0

    @pytest.mark.happy_path
    def test_validate_when_governance_sections_present_then_no_cv003_warning(
        self, validator: ComposeValidator
    ) -> None:
        """GIVEN composed content with governance sections matching source
        WHEN validated with governance_source
        THEN no CV-003 warnings."""
        # Arrange
        body = (
            "## Identity\n\nYou are test-agent.\n\n"
            "## Agent Version\n\n2.3.1\n\n"
            "## Tool Tier\n\nT3 (External)\n"
        )
        content = _make_composed_md(body=body)
        gov_source = {"version": "2.3.1", "tool_tier": "T3"}

        # Act
        result = validator.validate(content, "test-agent", governance_source=gov_source)

        # Assert
        cv003_warnings = [w for w in result.warnings if w.check_id == "CV-003"]
        assert len(cv003_warnings) == 0

    @pytest.mark.happy_path
    def test_validate_when_frontmatter_passes_schema_then_no_cv007_error(
        self, validator_with_schema: ComposeValidator
    ) -> None:
        """GIVEN valid frontmatter matching Anthropic schema
        WHEN validated with schema
        THEN no CV-007 errors."""
        # Arrange
        content = _make_composed_md(
            frontmatter={
                "name": "test-agent",
                "description": "A valid agent",
                "model": "sonnet",
            }
        )

        # Act
        result = validator_with_schema.validate(content, "test-agent")

        # Assert
        cv007_errors = [e for e in result.errors if e.check_id == "CV-007"]
        assert len(cv007_errors) == 0


# =============================================================================
# Negative (30%)
# =============================================================================


@pytest.mark.unit
class TestComposeValidatorNegative:
    """Negative tests: invalid content is caught."""

    @pytest.mark.negative
    def test_validate_when_jerry_plugin_root_in_body_then_cv001_error(
        self, validator: ComposeValidator
    ) -> None:
        """GIVEN body containing ${JERRY_PLUGIN_ROOT}
        WHEN validated
        THEN CV-001 error is returned."""
        # Arrange
        body = "Use ${JERRY_PLUGIN_ROOT}/scripts/run.sh to execute."
        content = _make_composed_md(body=body)

        # Act
        result = validator.validate(content, "bad-agent")

        # Assert
        assert not result.is_valid
        cv001 = [e for e in result.errors if e.check_id == "CV-001"]
        assert len(cv001) == 1
        assert "JERRY_PLUGIN_ROOT" in cv001[0].message

    @pytest.mark.negative
    def test_validate_when_jerry_plugin_root_no_braces_then_cv001_error(
        self, validator: ComposeValidator
    ) -> None:
        """GIVEN body containing $JERRY_PLUGIN_ROOT (no braces)
        WHEN validated
        THEN CV-001 error is returned."""
        # Arrange
        body = "Run $JERRY_PLUGIN_ROOT/scripts/run.sh to execute."
        content = _make_composed_md(body=body)

        # Act
        result = validator.validate(content, "bad-agent")

        # Assert
        cv001 = [e for e in result.errors if e.check_id == "CV-001"]
        assert len(cv001) == 1

    @pytest.mark.negative
    def test_validate_when_python_api_import_in_body_then_cv002_error(
        self, validator: ComposeValidator
    ) -> None:
        """GIVEN body containing 'from skills.worktracker.scripts'
        WHEN validated
        THEN CV-002 error is returned."""
        # Arrange
        body = "You can use from skills.worktracker.scripts import validate to check."
        content = _make_composed_md(body=body)

        # Act
        result = validator.validate(content, "bad-agent")

        # Assert
        assert not result.is_valid
        cv002 = [e for e in result.errors if e.check_id == "CV-002"]
        assert len(cv002) == 1

    @pytest.mark.negative
    def test_validate_when_abstract_tool_name_leaked_then_cv004_warning(
        self, validator: ComposeValidator
    ) -> None:
        """GIVEN body containing abstract tool name 'file_read'
        WHEN validated
        THEN CV-004 warning is returned."""
        # Arrange
        body = "Use file_read to read files in the workspace."
        content = _make_composed_md(body=body)

        # Act
        result = validator.validate(content, "leaky-agent")

        # Assert
        cv004 = [w for w in result.warnings if w.check_id == "CV-004"]
        assert len(cv004) >= 1
        assert "file_read" in cv004[0].message

    @pytest.mark.negative
    def test_validate_when_governance_in_frontmatter_then_cv006_error(
        self, validator: ComposeValidator
    ) -> None:
        """GIVEN frontmatter containing governance field 'version'
        WHEN validated
        THEN CV-006 error is returned."""
        # Arrange
        content = _make_composed_md(
            frontmatter={
                "name": "leaked-agent",
                "description": "An agent with leaked governance",
                "version": "2.0.0",
            }
        )

        # Act
        result = validator.validate(content, "leaked-agent")

        # Assert
        assert not result.is_valid
        cv006 = [e for e in result.errors if e.check_id == "CV-006"]
        assert len(cv006) >= 1
        assert "version" in cv006[0].message

    @pytest.mark.negative
    def test_validate_when_frontmatter_invalid_model_enum_then_cv007_error(
        self, validator_with_schema: ComposeValidator
    ) -> None:
        """GIVEN frontmatter with invalid model value 'gpt-4'
        WHEN validated with schema
        THEN CV-007 error is returned."""
        # Arrange
        content = _make_composed_md(
            frontmatter={
                "name": "bad-model-agent",
                "description": "Agent with invalid model",
                "model": "gpt-4",
            }
        )

        # Act
        result = validator_with_schema.validate(content, "bad-model-agent")

        # Assert
        cv007 = [e for e in result.errors if e.check_id == "CV-007"]
        assert len(cv007) == 1

    @pytest.mark.negative
    def test_validate_when_name_missing_then_cv005_error(self, validator: ComposeValidator) -> None:
        """GIVEN frontmatter without 'name' field
        WHEN validated
        THEN CV-005 error is returned."""
        # Arrange
        content = _make_composed_md(frontmatter={"description": "Agent without name"})

        # Act
        result = validator.validate(content, "nameless-agent")

        # Assert
        assert not result.is_valid
        cv005 = [e for e in result.errors if e.check_id == "CV-005"]
        assert len(cv005) >= 1
        assert "name" in cv005[0].message

    @pytest.mark.negative
    def test_validate_when_governance_section_missing_then_cv003_warning(
        self, validator: ComposeValidator
    ) -> None:
        """GIVEN body missing governance sections that source declares
        WHEN validated with governance_source
        THEN CV-003 warnings are returned."""
        # Arrange
        body = "## Identity\n\nYou are test-agent.\n"
        content = _make_composed_md(body=body)
        gov_source = {"version": "2.3.1", "tool_tier": "T3"}

        # Act
        result = validator.validate(content, "test-agent", governance_source=gov_source)

        # Assert
        cv003 = [w for w in result.warnings if w.check_id == "CV-003"]
        assert len(cv003) == 2  # Both version and tool_tier missing


# =============================================================================
# Edge cases (10%)
# =============================================================================


@pytest.mark.unit
class TestComposeValidatorEdgeCases:
    """Edge-case tests: boundary conditions and false-positive prevention."""

    @pytest.mark.edge_case
    def test_validate_when_pattern_inside_code_block_then_no_false_positive(
        self, validator: ComposeValidator
    ) -> None:
        """GIVEN JERRY_PLUGIN_ROOT inside a code block
        WHEN validated
        THEN no CV-001 error (code blocks are excluded)."""
        # Arrange
        body = "## Example\n\n```bash\nexport JERRY_PLUGIN_ROOT=/path/to/plugins\n```\n"
        content = _make_composed_md(body=body)

        # Act
        result = validator.validate(content, "code-block-agent")

        # Assert
        cv001 = [e for e in result.errors if e.check_id == "CV-001"]
        assert len(cv001) == 0

    @pytest.mark.edge_case
    def test_validate_when_python_import_inside_code_block_then_no_false_positive(
        self, validator: ComposeValidator
    ) -> None:
        """GIVEN Python import inside a code block
        WHEN validated
        THEN no CV-002 error (code blocks are excluded)."""
        # Arrange
        body = "## Example\n\n```python\nfrom skills.worktracker.scripts import validate\n```\n"
        content = _make_composed_md(body=body)

        # Act
        result = validator.validate(content, "code-block-agent")

        # Assert
        cv002 = [e for e in result.errors if e.check_id == "CV-002"]
        assert len(cv002) == 0

    @pytest.mark.edge_case
    def test_validate_when_abstract_tool_inside_code_block_then_no_false_positive(
        self, validator: ComposeValidator
    ) -> None:
        """GIVEN abstract tool name inside a code block
        WHEN validated
        THEN no CV-004 warning."""
        # Arrange
        body = "## Tools\n\n```yaml\ntools:\n  - file_read\n  - file_write\n```\n"
        content = _make_composed_md(body=body)

        # Act
        result = validator.validate(content, "code-block-agent")

        # Assert
        cv004 = [w for w in result.warnings if w.check_id == "CV-004"]
        assert len(cv004) == 0

    @pytest.mark.edge_case
    def test_validate_when_empty_body_then_governance_warning(
        self, validator: ComposeValidator
    ) -> None:
        """GIVEN empty body with governance_source
        WHEN validated
        THEN CV-003 warnings for missing governance sections."""
        # Arrange
        content = _make_composed_md(body="")
        gov_source = {"version": "1.0.0"}

        # Act
        result = validator.validate(content, "empty-agent", governance_source=gov_source)

        # Assert
        cv003 = [w for w in result.warnings if w.check_id == "CV-003"]
        assert len(cv003) >= 1

    @pytest.mark.edge_case
    def test_validate_when_no_frontmatter_then_cv005_errors(
        self, validator: ComposeValidator
    ) -> None:
        """GIVEN content with no YAML frontmatter
        WHEN validated
        THEN CV-005 errors for missing required fields."""
        # Arrange
        content = "## Identity\n\nYou are test-agent.\n"

        # Act
        result = validator.validate(content, "no-fm-agent")

        # Assert
        cv005 = [e for e in result.errors if e.check_id == "CV-005"]
        assert len(cv005) >= 2  # name and description both missing

    @pytest.mark.edge_case
    def test_validate_when_xml_governance_tags_then_cv003_passes(
        self, validator: ComposeValidator
    ) -> None:
        """GIVEN body with XML governance tags instead of markdown headings
        WHEN validated with governance_source
        THEN no CV-003 warnings (both formats are accepted)."""
        # Arrange
        body = (
            "<agent>\n"
            "<identity>You are test-agent.</identity>\n"
            "<agent_version>2.3.1</agent_version>\n"
            "<tool_tier>T3 (External)</tool_tier>\n"
            "</agent>\n"
        )
        content = _make_composed_md(body=body)
        gov_source = {"version": "2.3.1", "tool_tier": "T3"}

        # Act
        result = validator.validate(content, "xml-agent", governance_source=gov_source)

        # Assert
        cv003 = [w for w in result.warnings if w.check_id == "CV-003"]
        assert len(cv003) == 0
