# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for SkillComposeValidator domain service.

Coverage targets:
- SCV-001: No Jerry extension fields in frontmatter
- SCV-002: Required Anthropic fields present
- SCV-003: Governance sections present when canonical source declares them
- SCV-004: Frontmatter validates against Anthropic schema
- SCV-005: Name matches folder, lowercase kebab-case
- SCV-006: Description under 1024 chars, no XML brackets
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.agents.domain.services.skill_compose_validator import SkillComposeValidator

_REPO_ROOT = Path(__file__).resolve().parents[5]
_ANTHROPIC_SCHEMA = _REPO_ROOT / "docs" / "schemas" / "anthropic-skill-frontmatter-v1.schema.json"


@pytest.fixture()
def validator() -> SkillComposeValidator:
    """Validator without schema for SCV-004 (skips schema validation)."""
    return SkillComposeValidator(anthropic_schema_path=None)


@pytest.fixture()
def validator_with_schema() -> SkillComposeValidator:
    """Validator with Anthropic schema for SCV-004 tests."""
    return SkillComposeValidator(anthropic_schema_path=_ANTHROPIC_SCHEMA)


def _make_skill_md(
    name: str = "test-skill",
    description: str = "A test skill for validation",
    extra_frontmatter: str = "",
    body: str = "## Purpose\n\nTest purpose.\n",
) -> str:
    """Helper to build SKILL.md content."""
    fm = f"name: {name}\ndescription: {description}\n"
    if extra_frontmatter:
        fm += extra_frontmatter
    return f"---\n{fm}---\n{body}"


class TestSCV001NoJerryFieldsInFrontmatter:
    """SCV-001: No Jerry extension fields in frontmatter."""

    @pytest.mark.happy_path
    def test_validate_when_clean_frontmatter_then_no_scv001_errors(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = _make_skill_md()

        # Act
        result = validator.validate(content, skill_name="test-skill")

        # Assert
        scv001_errors = [f for f in result.errors if f.check_id == "SCV-001"]
        assert len(scv001_errors) == 0

    @pytest.mark.negative
    def test_validate_when_version_in_frontmatter_then_scv001_error(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = _make_skill_md(extra_frontmatter="version: 1.0.0\n")

        # Act
        result = validator.validate(content, skill_name="test-skill")

        # Assert
        scv001_errors = [f for f in result.errors if f.check_id == "SCV-001"]
        assert len(scv001_errors) == 1
        assert "version" in scv001_errors[0].message

    @pytest.mark.negative
    def test_validate_when_multiple_jerry_fields_then_multiple_scv001_errors(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = _make_skill_md(
            extra_frontmatter="version: 1.0.0\nactivation-keywords:\n  - test\nagents:\n  - agent-1\n"
        )

        # Act
        result = validator.validate(content, skill_name="test-skill")

        # Assert
        scv001_errors = [f for f in result.errors if f.check_id == "SCV-001"]
        assert len(scv001_errors) == 3

    @pytest.mark.negative
    def test_validate_when_metadata_in_frontmatter_then_scv001_error(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = _make_skill_md(extra_frontmatter="metadata:\n  key: value\n")

        # Act
        result = validator.validate(content, skill_name="test-skill")

        # Assert
        scv001_errors = [f for f in result.errors if f.check_id == "SCV-001"]
        assert len(scv001_errors) == 1
        assert "metadata" in scv001_errors[0].message


class TestSCV002RequiredFields:
    """SCV-002: Required Anthropic fields present (name, description)."""

    @pytest.mark.happy_path
    def test_validate_when_name_and_description_present_then_no_scv002_errors(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = _make_skill_md()

        # Act
        result = validator.validate(content, skill_name="test-skill")

        # Assert
        scv002_errors = [f for f in result.errors if f.check_id == "SCV-002"]
        assert len(scv002_errors) == 0

    @pytest.mark.negative
    def test_validate_when_name_missing_then_scv002_error(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = "---\ndescription: A test skill\n---\n## Body\n"

        # Act
        result = validator.validate(content, skill_name="test-skill")

        # Assert
        scv002_errors = [f for f in result.errors if f.check_id == "SCV-002"]
        assert any("name" in f.message for f in scv002_errors)

    @pytest.mark.negative
    def test_validate_when_description_missing_then_scv002_error(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = "---\nname: test-skill\n---\n## Body\n"

        # Act
        result = validator.validate(content, skill_name="test-skill")

        # Assert
        scv002_errors = [f for f in result.errors if f.check_id == "SCV-002"]
        assert any("description" in f.message for f in scv002_errors)

    @pytest.mark.negative
    def test_validate_when_both_missing_then_two_scv002_errors(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = "---\nallowed-tools: Read\n---\n## Body\n"

        # Act
        result = validator.validate(content, skill_name="test-skill")

        # Assert
        scv002_errors = [f for f in result.errors if f.check_id == "SCV-002"]
        assert len(scv002_errors) == 2


class TestSCV003GovernanceSections:
    """SCV-003: Governance sections present when canonical source declares them."""

    @pytest.mark.happy_path
    def test_validate_when_governance_sections_present_then_no_scv003_warnings(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        body = "## Skill Version\n\n1.0.0\n\n## Activation Keywords\n\n- test\n"
        content = _make_skill_md(body=body)
        governance_source = {"version": "1.0.0", "activation-keywords": ["test"]}

        # Act
        result = validator.validate(
            content, skill_name="test-skill", governance_source=governance_source
        )

        # Assert
        scv003_warnings = [f for f in result.warnings if f.check_id == "SCV-003"]
        assert len(scv003_warnings) == 0

    @pytest.mark.negative
    def test_validate_when_version_declared_but_section_missing_then_scv003_warning(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = _make_skill_md(body="## Purpose\n\nNo governance sections.\n")
        governance_source = {"version": "1.0.0"}

        # Act
        result = validator.validate(
            content, skill_name="test-skill", governance_source=governance_source
        )

        # Assert
        scv003_warnings = [f for f in result.warnings if f.check_id == "SCV-003"]
        assert len(scv003_warnings) == 1
        assert "version" in scv003_warnings[0].message

    @pytest.mark.edge_case
    def test_validate_when_no_governance_source_then_scv003_skipped(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = _make_skill_md()

        # Act
        result = validator.validate(content, skill_name="test-skill")

        # Assert
        scv003_warnings = [f for f in result.warnings if f.check_id == "SCV-003"]
        assert len(scv003_warnings) == 0

    @pytest.mark.negative
    def test_validate_when_agents_declared_but_section_missing_then_scv003_warning(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = _make_skill_md(body="## Purpose\n\nNo governance sections here.\n")
        governance_source = {"agents": ["ps-researcher"]}

        # Act
        result = validator.validate(
            content, skill_name="test-skill", governance_source=governance_source
        )

        # Assert
        scv003_warnings = [f for f in result.warnings if f.check_id == "SCV-003"]
        assert any("agents" in w.message for w in scv003_warnings)


class TestSCV005NameMatching:
    """SCV-005: Name matches folder name, lowercase kebab-case."""

    @pytest.mark.happy_path
    def test_validate_when_name_matches_folder_then_no_scv005_errors(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = _make_skill_md(name="problem-solving")

        # Act
        result = validator.validate(
            content, skill_name="problem-solving", folder_name="problem-solving"
        )

        # Assert
        scv005_errors = [f for f in result.errors if f.check_id == "SCV-005"]
        assert len(scv005_errors) == 0

    @pytest.mark.negative
    def test_validate_when_name_not_kebab_case_then_scv005_error(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = _make_skill_md(name="ProblemSolving")

        # Act
        result = validator.validate(
            content, skill_name="ProblemSolving", folder_name="problem-solving"
        )

        # Assert
        scv005_errors = [f for f in result.errors if f.check_id == "SCV-005"]
        assert any("kebab-case" in e.message for e in scv005_errors)

    @pytest.mark.negative
    def test_validate_when_name_differs_from_folder_then_scv005_error(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = _make_skill_md(name="wrong-name")

        # Act
        result = validator.validate(content, skill_name="wrong-name", folder_name="correct-name")

        # Assert
        scv005_errors = [f for f in result.errors if f.check_id == "SCV-005"]
        assert any("folder" in e.message for e in scv005_errors)

    @pytest.mark.regression
    def test_validate_when_uppercase_name_then_scv005_error(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange — regression: Bootstrap name was uppercase
        content = _make_skill_md(name="Bootstrap")

        # Act
        result = validator.validate(content, skill_name="Bootstrap", folder_name="bootstrap")

        # Assert
        scv005_errors = [f for f in result.errors if f.check_id == "SCV-005"]
        assert len(scv005_errors) >= 1


class TestSCV006Description:
    """SCV-006: Description under 1024 chars, no XML brackets."""

    @pytest.mark.happy_path
    def test_validate_when_short_description_no_xml_then_no_scv006_errors(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = _make_skill_md(description="A clean short description")

        # Act
        result = validator.validate(content, skill_name="test-skill")

        # Assert
        scv006_errors = [f for f in result.errors if f.check_id == "SCV-006"]
        assert len(scv006_errors) == 0

    @pytest.mark.negative
    def test_validate_when_description_exceeds_1024_then_scv006_error(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        long_desc = "x" * 1025
        content = _make_skill_md(description=long_desc)

        # Act
        result = validator.validate(content, skill_name="test-skill")

        # Assert
        scv006_errors = [f for f in result.errors if f.check_id == "SCV-006"]
        assert any("1024" in e.message for e in scv006_errors)

    @pytest.mark.security
    def test_validate_when_description_has_xml_tags_then_scv006_error(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange — security: no XML injection in description
        content = _make_skill_md(description="A skill with <script>alert(1)</script> tag")

        # Act
        result = validator.validate(content, skill_name="test-skill")

        # Assert
        scv006_errors = [f for f in result.errors if f.check_id == "SCV-006"]
        assert any("XML" in e.message for e in scv006_errors)

    @pytest.mark.security
    def test_validate_when_description_has_system_tag_then_scv006_error(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = _make_skill_md(description="A skill with <system> injection attempt")

        # Act
        result = validator.validate(content, skill_name="test-skill")

        # Assert
        scv006_errors = [f for f in result.errors if f.check_id == "SCV-006"]
        assert any("XML" in e.message for e in scv006_errors)

    @pytest.mark.boundary
    def test_validate_when_description_exactly_1024_then_no_scv006_error(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        exact_desc = "x" * 1024
        content = _make_skill_md(description=exact_desc)

        # Act
        result = validator.validate(content, skill_name="test-skill")

        # Assert
        scv006_errors = [f for f in result.errors if f.check_id == "SCV-006"]
        assert len(scv006_errors) == 0


class TestValidateCleanSkill:
    """Integration-style tests for a fully valid composed SKILL.md."""

    @pytest.mark.happy_path
    def test_validate_when_clean_skill_then_is_valid(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        body = (
            "## Purpose\n\nTest purpose.\n\n"
            "## Skill Version\n\n1.0.0\n\n"
            "## Activation Keywords\n\n- research\n"
        )
        content = _make_skill_md(name="test-skill", body=body)
        governance = {"version": "1.0.0", "activation-keywords": ["research"]}

        # Act
        result = validator.validate(
            content,
            skill_name="test-skill",
            folder_name="test-skill",
            governance_source=governance,
        )

        # Assert
        assert result.is_valid

    @pytest.mark.edge_case
    def test_validate_when_no_frontmatter_then_scv002_errors(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange — no frontmatter at all
        content = "# Just a heading\n\nBody content.\n"

        # Act
        result = validator.validate(content, skill_name="test-skill")

        # Assert
        assert not result.is_valid
        scv002_errors = [f for f in result.errors if f.check_id == "SCV-002"]
        assert len(scv002_errors) == 2  # name + description missing


class TestSCV001CaseInsensitive:
    """SCV-001: Case-insensitive detection of Jerry extension fields."""

    @pytest.mark.regression
    def test_validate_when_version_uppercase_then_scv001_error(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange — case-variant bypass attempt
        content = _make_skill_md(extra_frontmatter="Version: 1.0.0\n")

        # Act
        result = validator.validate(content, skill_name="test-skill")

        # Assert
        scv001_errors = [f for f in result.errors if f.check_id == "SCV-001"]
        assert len(scv001_errors) == 1

    @pytest.mark.regression
    def test_validate_when_metadata_mixed_case_then_scv001_error(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = _make_skill_md(extra_frontmatter="Metadata:\n  key: val\n")

        # Act
        result = validator.validate(content, skill_name="test-skill")

        # Assert
        scv001_errors = [f for f in result.errors if f.check_id == "SCV-001"]
        assert len(scv001_errors) == 1

    @pytest.mark.regression
    def test_validate_when_agents_all_caps_then_scv001_error(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = _make_skill_md(extra_frontmatter="AGENTS:\n  - agent-1\n")

        # Act
        result = validator.validate(content, skill_name="test-skill")

        # Assert
        scv001_errors = [f for f in result.errors if f.check_id == "SCV-001"]
        assert len(scv001_errors) == 1


class TestSCV003StructuralHeadingMatch:
    """SCV-003: Structural heading match (not substring)."""

    @pytest.mark.regression
    def test_validate_when_heading_text_in_paragraph_then_no_false_match(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange — "skill version" appears in prose, not as heading
        body = "## Purpose\n\nThe skill version was updated recently.\n"
        content = _make_skill_md(body=body)
        governance_source = {"version": "1.0.0"}

        # Act
        result = validator.validate(
            content, skill_name="test-skill", governance_source=governance_source
        )

        # Assert — should warn because no ## Skill Version heading exists
        scv003_warnings = [f for f in result.warnings if f.check_id == "SCV-003"]
        assert len(scv003_warnings) == 1

    @pytest.mark.happy_path
    def test_validate_when_proper_heading_then_no_warning(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        body = "## Purpose\n\nContent.\n\n## Skill Version\n\n1.0.0\n"
        content = _make_skill_md(body=body)
        governance_source = {"version": "1.0.0"}

        # Act
        result = validator.validate(
            content, skill_name="test-skill", governance_source=governance_source
        )

        # Assert
        scv003_warnings = [f for f in result.warnings if f.check_id == "SCV-003"]
        assert len(scv003_warnings) == 0


class TestSCV004SchemaValidation:
    """SCV-004: Frontmatter validates against Anthropic skill schema."""

    @pytest.mark.happy_path
    def test_validate_when_valid_frontmatter_with_schema_then_no_scv004_errors(
        self, validator_with_schema: SkillComposeValidator
    ) -> None:
        # Arrange
        content = _make_skill_md(name="test-skill", description="A valid test skill")

        # Act
        result = validator_with_schema.validate(content, skill_name="test-skill")

        # Assert
        scv004_errors = [f for f in result.errors if f.check_id == "SCV-004"]
        assert len(scv004_errors) == 0

    @pytest.mark.negative
    def test_validate_when_invalid_name_with_schema_then_scv004_error(
        self, validator_with_schema: SkillComposeValidator
    ) -> None:
        # Arrange — name with spaces violates kebab-case pattern
        content = _make_skill_md(name="Invalid Name With Spaces")

        # Act
        result = validator_with_schema.validate(content, skill_name="Invalid Name With Spaces")

        # Assert
        scv004_errors = [f for f in result.errors if f.check_id == "SCV-004"]
        assert len(scv004_errors) >= 1

    @pytest.mark.edge_case
    def test_validate_when_no_schema_then_scv004_skipped(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange — validator without schema
        content = _make_skill_md(name="Invalid Name")

        # Act
        result = validator.validate(content, skill_name="Invalid Name")

        # Assert — SCV-004 should not fire
        scv004_errors = [f for f in result.errors if f.check_id == "SCV-004"]
        assert len(scv004_errors) == 0

    @pytest.mark.negative
    def test_validate_when_extra_field_in_frontmatter_then_scv004_error(
        self, validator_with_schema: SkillComposeValidator
    ) -> None:
        # Arrange — unknown field should fail additionalProperties: false
        content = _make_skill_md(extra_frontmatter="unknown-field: true\n")

        # Act
        result = validator_with_schema.validate(content, skill_name="test-skill")

        # Assert
        scv004_errors = [f for f in result.errors if f.check_id == "SCV-004"]
        assert len(scv004_errors) >= 1
