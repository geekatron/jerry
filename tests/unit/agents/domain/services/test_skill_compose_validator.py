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
- SCV-007: Canonical name matches frontmatter name (FM-03)
- SCV-008: All agents within a skill declare the same body_format
- FM-08: Warning when jsonschema missing for SCV-004
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
    def test_validate_when_version_declared_but_section_missing_then_scv003_error(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange — version is a required governance field, so missing section is an error
        content = _make_skill_md(body="## Purpose\n\nNo governance sections.\n")
        governance_source = {"version": "1.0.0"}

        # Act
        result = validator.validate(
            content, skill_name="test-skill", governance_source=governance_source
        )

        # Assert — required field escalates to error
        scv003_errors = [f for f in result.errors if f.check_id == "SCV-003"]
        assert len(scv003_errors) == 1
        assert "version" in scv003_errors[0].message

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


class TestSCV003XmlTagDetection:
    """SCV-003: XML governance tags satisfy governance section checks.

    After BUG-002, composed SKILL.md files use <xml_tag> format for
    governance sections. SCV-003 must detect both ## Heading and <xml_tag>
    patterns to avoid false positives during validation.
    """

    @pytest.mark.happy_path
    def test_validate_when_xml_skill_version_tag_then_no_scv003_error(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange — XML tag format instead of ## heading
        body = "## Purpose\n\nContent.\n\n<skill_version>\n1.0.0\n</skill_version>\n"
        content = _make_skill_md(body=body)
        governance_source = {"version": "1.0.0"}

        # Act
        result = validator.validate(
            content, skill_name="test-skill", governance_source=governance_source
        )

        # Assert
        scv003_errors = [f for f in result.errors if f.check_id == "SCV-003"]
        assert len(scv003_errors) == 0

    @pytest.mark.happy_path
    def test_validate_when_xml_activation_keywords_tag_then_no_scv003_error(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        body = (
            "## Purpose\n\nContent.\n\n"
            "<activation_keywords>\n- research\n- analyze\n</activation_keywords>\n"
        )
        content = _make_skill_md(body=body)
        governance_source = {"activation-keywords": ["research", "analyze"]}

        # Act
        result = validator.validate(
            content, skill_name="test-skill", governance_source=governance_source
        )

        # Assert
        scv003_errors = [f for f in result.errors if f.check_id == "SCV-003"]
        assert len(scv003_errors) == 0

    @pytest.mark.happy_path
    def test_validate_when_xml_agent_registry_tag_then_no_scv003_warning(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        body = "## Purpose\n\nContent.\n\n<agent_registry>\n- ps-researcher\n</agent_registry>\n"
        content = _make_skill_md(body=body)
        governance_source = {"agents": ["ps-researcher"]}

        # Act
        result = validator.validate(
            content, skill_name="test-skill", governance_source=governance_source
        )

        # Assert
        scv003_warnings = [f for f in result.warnings if f.check_id == "SCV-003"]
        assert len(scv003_warnings) == 0

    @pytest.mark.happy_path
    def test_validate_when_xml_context_injection_tag_then_no_scv003_warning(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        body = "## Purpose\n\nContent.\n\n<context_injection>\nrules:\n- test.md\n</context_injection>\n"
        content = _make_skill_md(body=body)
        governance_source = {"context_injection": {"rules": ["test.md"]}}

        # Act
        result = validator.validate(
            content, skill_name="test-skill", governance_source=governance_source
        )

        # Assert
        scv003_warnings = [f for f in result.warnings if f.check_id == "SCV-003"]
        assert len(scv003_warnings) == 0

    @pytest.mark.edge_case
    def test_validate_when_all_four_xml_tags_present_then_no_scv003_findings(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange — all governance sections in XML format
        body = (
            "## Purpose\n\nContent.\n\n"
            "<skill_version>\n1.0.0\n</skill_version>\n\n"
            "<activation_keywords>\n- test\n</activation_keywords>\n\n"
            "<agent_registry>\n- ps-researcher\n</agent_registry>\n\n"
            "<context_injection>\nrules:\n- test.md\n</context_injection>\n"
        )
        content = _make_skill_md(body=body)
        governance_source = {
            "version": "1.0.0",
            "activation-keywords": ["test"],
            "agents": ["ps-researcher"],
            "context_injection": {"rules": ["test.md"]},
        }

        # Act
        result = validator.validate(
            content, skill_name="test-skill", governance_source=governance_source
        )

        # Assert
        scv003_errors = [f for f in result.errors if f.check_id == "SCV-003"]
        scv003_warnings = [f for f in result.warnings if f.check_id == "SCV-003"]
        assert len(scv003_errors) == 0
        assert len(scv003_warnings) == 0

    @pytest.mark.edge_case
    def test_validate_when_mixed_xml_and_heading_format_then_no_scv003_findings(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange — mix of XML tags and ## headings
        body = (
            "## Purpose\n\nContent.\n\n"
            "<skill_version>\n1.0.0\n</skill_version>\n\n"
            "## Activation Keywords\n\n- test\n"
        )
        content = _make_skill_md(body=body)
        governance_source = {
            "version": "1.0.0",
            "activation-keywords": ["test"],
        }

        # Act
        result = validator.validate(
            content, skill_name="test-skill", governance_source=governance_source
        )

        # Assert
        scv003_errors = [f for f in result.errors if f.check_id == "SCV-003"]
        assert len(scv003_errors) == 0


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

        # Assert — should error because no ## Skill Version heading exists (version is required)
        scv003_errors = [f for f in result.errors if f.check_id == "SCV-003"]
        assert len(scv003_errors) == 1

    @pytest.mark.happy_path
    def test_validate_when_proper_heading_then_no_error(
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
        scv003_errors = [f for f in result.errors if f.check_id == "SCV-003"]
        assert len(scv003_errors) == 0
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

    @pytest.mark.edge_case
    def test_validate_when_extra_field_in_frontmatter_then_no_scv004_error(
        self, validator_with_schema: SkillComposeValidator
    ) -> None:
        # Arrange — unknown fields are allowed (additionalProperties: true)
        # so Anthropic can add new official fields without breaking CI.
        # Jerry extension field enforcement is handled by SCV-001, not schema.
        content = _make_skill_md(extra_frontmatter="unknown-field: true\n")

        # Act
        result = validator_with_schema.validate(content, skill_name="test-skill")

        # Assert — SCV-004 should not fire for unknown fields
        scv004_errors = [f for f in result.errors if f.check_id == "SCV-004"]
        assert len(scv004_errors) == 0

    @pytest.mark.negative
    def test_validate_when_jsonschema_unavailable_then_scv004_warning(
        self, validator_with_schema: SkillComposeValidator
    ) -> None:
        """FM-08: SCV-004 emits warning when jsonschema is None (not silent skip)."""
        # Arrange — temporarily set _anthropic_schema to trigger the check
        # but patch jsonschema to None
        import src.agents.domain.services.skill_compose_validator as mod

        original = mod.jsonschema
        mod.jsonschema = None  # type: ignore[assignment]
        try:
            content = _make_skill_md()

            # Act
            result = validator_with_schema.validate(content, skill_name="test-skill")

            # Assert — should produce a warning, not silently skip
            scv004_warnings = [f for f in result.warnings if f.check_id == "SCV-004"]
            assert len(scv004_warnings) == 1
            assert "jsonschema" in scv004_warnings[0].message
        finally:
            mod.jsonschema = original


class TestSCV007CanonicalNameConsistency:
    """SCV-007: Canonical source name matches frontmatter name (FM-03)."""

    @pytest.mark.happy_path
    def test_validate_when_names_match_then_no_scv007_errors(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = _make_skill_md(name="problem-solving")

        # Act
        result = validator.validate(
            content,
            skill_name="problem-solving",
            canonical_name="problem-solving",
        )

        # Assert
        scv007_errors = [f for f in result.errors if f.check_id == "SCV-007"]
        assert len(scv007_errors) == 0

    @pytest.mark.negative
    def test_validate_when_names_differ_then_scv007_error(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange — canonical source says "problem-solving" but frontmatter says "wrong-name"
        content = _make_skill_md(name="wrong-name")

        # Act
        result = validator.validate(
            content,
            skill_name="wrong-name",
            canonical_name="problem-solving",
        )

        # Assert
        scv007_errors = [f for f in result.errors if f.check_id == "SCV-007"]
        assert len(scv007_errors) == 1
        assert "problem-solving" in scv007_errors[0].message
        assert "wrong-name" in scv007_errors[0].message

    @pytest.mark.edge_case
    def test_validate_when_no_canonical_name_then_scv007_skipped(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = _make_skill_md(name="test-skill")

        # Act
        result = validator.validate(content, skill_name="test-skill", canonical_name="")

        # Assert
        scv007_errors = [f for f in result.errors if f.check_id == "SCV-007"]
        assert len(scv007_errors) == 0

    @pytest.mark.edge_case
    def test_validate_when_frontmatter_name_missing_then_scv007_skipped(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange — no name in frontmatter (SCV-002 catches this)
        content = "---\ndescription: Test\n---\n## Body\n"

        # Act
        result = validator.validate(content, skill_name="test-skill", canonical_name="test-skill")

        # Assert — SCV-007 should not fire when name is missing (SCV-002 handles that)
        scv007_errors = [f for f in result.errors if f.check_id == "SCV-007"]
        assert len(scv007_errors) == 0


class TestSCV008BodyFormatConsistency:
    """SCV-008: All agents within a skill must declare the same body_format."""

    @pytest.mark.happy_path
    def test_validate_when_all_agents_same_format_then_no_scv008_errors(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = _make_skill_md()
        formats = {"agent-a": "xml", "agent-b": "xml", "agent-c": "xml"}

        # Act
        result = validator.validate(content, skill_name="test-skill", agent_body_formats=formats)

        # Assert
        scv008_errors = [f for f in result.errors if f.check_id == "SCV-008"]
        assert len(scv008_errors) == 0

    @pytest.mark.negative
    def test_validate_when_mixed_formats_then_scv008_error(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = _make_skill_md()
        formats = {"agent-a": "xml", "agent-b": "markdown", "agent-c": "xml"}

        # Act
        result = validator.validate(content, skill_name="test-skill", agent_body_formats=formats)

        # Assert
        scv008_errors = [f for f in result.errors if f.check_id == "SCV-008"]
        assert len(scv008_errors) == 1
        assert "Inconsistent body_format" in scv008_errors[0].message
        assert "markdown" in scv008_errors[0].message
        assert "xml" in scv008_errors[0].message

    @pytest.mark.edge_case
    def test_validate_when_single_agent_then_scv008_skipped(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange — only one agent, nothing to compare
        content = _make_skill_md()
        formats = {"agent-a": "xml"}

        # Act
        result = validator.validate(content, skill_name="test-skill", agent_body_formats=formats)

        # Assert
        scv008_errors = [f for f in result.errors if f.check_id == "SCV-008"]
        assert len(scv008_errors) == 0

    @pytest.mark.edge_case
    def test_validate_when_no_agent_formats_then_scv008_skipped(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange — None passed (no agent data available)
        content = _make_skill_md()

        # Act
        result = validator.validate(content, skill_name="test-skill", agent_body_formats=None)

        # Assert
        scv008_errors = [f for f in result.errors if f.check_id == "SCV-008"]
        assert len(scv008_errors) == 0

    @pytest.mark.edge_case
    def test_validate_when_empty_formats_dict_then_scv008_skipped(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = _make_skill_md()

        # Act
        result = validator.validate(content, skill_name="test-skill", agent_body_formats={})

        # Assert
        scv008_errors = [f for f in result.errors if f.check_id == "SCV-008"]
        assert len(scv008_errors) == 0

    @pytest.mark.negative
    def test_validate_when_two_agents_different_formats_then_error_shows_both(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = _make_skill_md()
        formats = {"agent-x": "markdown", "agent-y": "xml"}

        # Act
        result = validator.validate(content, skill_name="test-skill", agent_body_formats=formats)

        # Assert
        scv008_errors = [f for f in result.errors if f.check_id == "SCV-008"]
        assert len(scv008_errors) == 1
        msg = scv008_errors[0].message
        assert "agent-x" in msg
        assert "agent-y" in msg


class TestSCV009DescriptionConsistency:
    """SCV-009: Canonical description matches frontmatter description."""

    @pytest.mark.happy_path
    def test_validate_when_descriptions_match_then_no_scv009_warnings(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = _make_skill_md(description="A test skill for validation")

        # Act
        result = validator.validate(
            content,
            skill_name="test-skill",
            canonical_description="A test skill for validation",
        )

        # Assert
        scv009_warnings = [f for f in result.warnings if f.check_id == "SCV-009"]
        assert len(scv009_warnings) == 0

    @pytest.mark.negative
    def test_validate_when_descriptions_differ_then_scv009_warning(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange — canonical says one thing, frontmatter says another (drift)
        content = _make_skill_md(description="Edited description in SKILL.md")

        # Act
        result = validator.validate(
            content,
            skill_name="test-skill",
            canonical_description="Original description from skill.jerry.yaml",
        )

        # Assert
        scv009_warnings = [f for f in result.warnings if f.check_id == "SCV-009"]
        assert len(scv009_warnings) == 1
        assert "skill.jerry.yaml" in scv009_warnings[0].message

    @pytest.mark.edge_case
    def test_validate_when_no_canonical_description_then_scv009_skipped(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange
        content = _make_skill_md(description="Some description")

        # Act
        result = validator.validate(content, skill_name="test-skill", canonical_description="")

        # Assert
        scv009_warnings = [f for f in result.warnings if f.check_id == "SCV-009"]
        assert len(scv009_warnings) == 0

    @pytest.mark.edge_case
    def test_validate_when_frontmatter_description_missing_then_scv009_skipped(
        self, validator: SkillComposeValidator
    ) -> None:
        # Arrange — no description in frontmatter (SCV-002 catches this)
        content = "---\nname: test-skill\n---\n## Body\n"

        # Act
        result = validator.validate(
            content,
            skill_name="test-skill",
            canonical_description="Some canonical description",
        )

        # Assert — SCV-009 should not fire when description is missing
        scv009_warnings = [f for f in result.warnings if f.check_id == "SCV-009"]
        assert len(scv009_warnings) == 0
