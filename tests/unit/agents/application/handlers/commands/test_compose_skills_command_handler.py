# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for ComposeSkillsCommandHandler.

Coverage targets:
- Full compose single skill (happy path)
- Compose all skills (happy path)
- Dry run produces no file writes (happy path)
- Missing canonical source (negative)
- Validation errors stop composition (negative)
- Footer injection positioning (edge case)
- Skill with no agents field (edge case)
- Roundtrip compose (regression)
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src.agents.application.commands.compose_skills_command import ComposeSkillsCommand
from src.agents.application.handlers.commands.compose_skills_command_handler import (
    ComposeSkillsCommandHandler,
)
from src.agents.domain.entities.canonical_skill import CanonicalSkill
from src.agents.domain.services.compose_validator import (
    ComposeValidationResult,
    ValidationFinding,
)
from src.agents.domain.services.prompt_transformer import PromptTransformer
from src.agents.domain.services.skill_governance_builder import (
    SkillGovernanceSectionBuilder,
)


@pytest.fixture()
def mock_repository() -> MagicMock:
    """Mock ISkillRepository."""
    repo = MagicMock()
    repo.get_skill_md_path.return_value = Path("/tmp/skills/test-skill/SKILL.md")
    repo.get_agent_body_formats.return_value = {}
    return repo


@pytest.fixture()
def governance_builder() -> SkillGovernanceSectionBuilder:
    """Real governance builder."""
    return SkillGovernanceSectionBuilder()


@pytest.fixture()
def prompt_transformer() -> PromptTransformer:
    """Real prompt transformer for XML conversion."""
    return PromptTransformer()


@pytest.fixture()
def mock_validator() -> MagicMock:
    """Mock SkillComposeValidator that passes by default."""
    validator = MagicMock()
    validator.validate.return_value = ComposeValidationResult(agent_name="test-skill")
    return validator


@pytest.fixture()
def sample_skill() -> CanonicalSkill:
    """Sample canonical skill for testing."""
    return CanonicalSkill(
        name="test-skill",
        version="1.0.0",
        activation_keywords=("research", "analyze"),
        agents=("ps-researcher", "ps-analyst"),
        context_injection={},
        prompt_body="## Purpose\n\nTest skill.\n\n*Skill Version: 1.0.0*\n",
    )


@pytest.fixture()
def sample_skill_no_footer() -> CanonicalSkill:
    """Sample canonical skill without footer in body."""
    return CanonicalSkill(
        name="no-footer-skill",
        version="1.0.0",
        activation_keywords=("test",),
        agents=(),
        prompt_body="## Purpose\n\nNo footer here.\n",
    )


def _make_handler(
    repository: MagicMock,
    governance_builder: SkillGovernanceSectionBuilder,
    validator: MagicMock | None = None,
    prompt_transformer: PromptTransformer | None = None,
) -> ComposeSkillsCommandHandler:
    """Create handler with dependencies."""
    return ComposeSkillsCommandHandler(
        repository=repository,
        governance_builder=governance_builder,
        prompt_transformer=prompt_transformer,
        validator=validator,
    )


class TestHandleSingleSkill:
    """Tests for composing a single skill by name."""

    @pytest.mark.happy_path
    def test_handle_when_single_skill_exists_then_composed_count_is_one(
        self,
        mock_repository: MagicMock,
        governance_builder: SkillGovernanceSectionBuilder,
        sample_skill: CanonicalSkill,
        tmp_path: Path,
    ) -> None:
        # Arrange
        mock_repository.get.return_value = sample_skill
        skill_md_path = tmp_path / "test-skill" / "SKILL.md"
        mock_repository.get_skill_md_path.return_value = skill_md_path

        handler = _make_handler(mock_repository, governance_builder)
        command = ComposeSkillsCommand(skill_name="test-skill")

        # Act
        result = handler.handle(command)

        # Assert
        assert result.composed == 1
        assert result.failed == 0
        assert len(result.output_paths) == 1

    @pytest.mark.negative
    def test_handle_when_skill_not_found_then_error_returned(
        self,
        mock_repository: MagicMock,
        governance_builder: SkillGovernanceSectionBuilder,
    ) -> None:
        # Arrange
        mock_repository.get.return_value = None
        handler = _make_handler(mock_repository, governance_builder)
        command = ComposeSkillsCommand(skill_name="nonexistent")

        # Act
        result = handler.handle(command)

        # Assert
        assert result.failed == 1
        assert result.composed == 0
        assert any("not found" in e for e in result.errors)


class TestHandleAllSkills:
    """Tests for composing all skills."""

    @pytest.mark.happy_path
    def test_handle_when_all_skills_then_each_composed(
        self,
        mock_repository: MagicMock,
        governance_builder: SkillGovernanceSectionBuilder,
        tmp_path: Path,
    ) -> None:
        # Arrange
        skills = []
        for name in ["skill-a", "skill-b"]:
            skills.append(
                CanonicalSkill(
                    name=name,
                    version="1.0.0",
                    activation_keywords=("test",),
                    prompt_body="## Purpose\n\nPurpose.\n",
                )
            )

        mock_repository.list_all_with_diagnostics.return_value = (skills, [])
        mock_repository.get_skill_md_path.side_effect = [
            tmp_path / "skill-a" / "SKILL.md",
            tmp_path / "skill-b" / "SKILL.md",
        ]

        handler = _make_handler(mock_repository, governance_builder)
        command = ComposeSkillsCommand()  # No skill_name = all

        # Act
        result = handler.handle(command)

        # Assert
        assert result.composed == 2
        assert result.failed == 0


class TestDryRun:
    """Tests for dry run mode."""

    @pytest.mark.happy_path
    def test_handle_when_dry_run_then_no_file_written(
        self,
        mock_repository: MagicMock,
        governance_builder: SkillGovernanceSectionBuilder,
        sample_skill: CanonicalSkill,
        tmp_path: Path,
    ) -> None:
        # Arrange
        mock_repository.get.return_value = sample_skill
        skill_md = tmp_path / "test-skill" / "SKILL.md"
        skill_md.parent.mkdir(parents=True, exist_ok=True)
        skill_md.write_text("original content", encoding="utf-8")
        mock_repository.get_skill_md_path.return_value = skill_md

        handler = _make_handler(mock_repository, governance_builder)
        command = ComposeSkillsCommand(skill_name="test-skill", dry_run=True)

        # Act
        result = handler.handle(command)

        # Assert
        assert result.composed == 1
        assert result.dry_run is True
        # File should NOT be modified in dry run
        assert skill_md.read_text() == "original content"


class TestValidation:
    """Tests for post-composition validation."""

    @pytest.mark.negative
    def test_handle_when_validation_errors_then_skill_marked_failed(
        self,
        mock_repository: MagicMock,
        governance_builder: SkillGovernanceSectionBuilder,
        mock_validator: MagicMock,
        sample_skill: CanonicalSkill,
        tmp_path: Path,
    ) -> None:
        # Arrange
        mock_repository.get.return_value = sample_skill
        skill_md = tmp_path / "test-skill" / "SKILL.md"
        mock_repository.get_skill_md_path.return_value = skill_md

        # Configure validator to return errors
        error_result = ComposeValidationResult(agent_name="test-skill")
        error_result.errors.append(
            ValidationFinding(
                check_id="SCV-001",
                severity="error",
                message="Jerry field found",
                agent_name="test-skill",
            )
        )
        mock_validator.validate.return_value = error_result

        handler = _make_handler(mock_repository, governance_builder, mock_validator)
        command = ComposeSkillsCommand(skill_name="test-skill")

        # Act
        result = handler.handle(command)

        # Assert
        assert result.failed == 1
        assert result.composed == 0
        assert any("SCV-001" in e for e in result.errors)

    @pytest.mark.happy_path
    def test_handle_when_validation_warnings_then_skill_still_composed(
        self,
        mock_repository: MagicMock,
        governance_builder: SkillGovernanceSectionBuilder,
        mock_validator: MagicMock,
        sample_skill: CanonicalSkill,
        tmp_path: Path,
    ) -> None:
        # Arrange
        mock_repository.get.return_value = sample_skill
        skill_md = tmp_path / "test-skill" / "SKILL.md"
        mock_repository.get_skill_md_path.return_value = skill_md

        # Configure validator to return only warnings
        warn_result = ComposeValidationResult(agent_name="test-skill")
        warn_result.warnings.append(
            ValidationFinding(
                check_id="SCV-003",
                severity="warning",
                message="Section missing",
                agent_name="test-skill",
            )
        )
        mock_validator.validate.return_value = warn_result

        handler = _make_handler(mock_repository, governance_builder, mock_validator)
        command = ComposeSkillsCommand(skill_name="test-skill")

        # Act
        result = handler.handle(command)

        # Assert
        assert result.composed == 1
        assert result.failed == 0
        assert len(result.warnings) == 1


class TestInjectBeforeFooter:
    """Tests for static _inject_before_footer method."""

    @pytest.mark.happy_path
    def test_inject_when_footer_present_then_sections_before_footer(self) -> None:
        # Arrange
        body = "## Purpose\n\nContent.\n\n*Skill Version: 1.0.0*\n"
        sections = "## Activation Keywords\n\n- test\n"

        # Act
        result = ComposeSkillsCommandHandler._inject_before_footer(body, sections)

        # Assert
        footer_idx = result.index("*Skill Version:")
        section_idx = result.index("## Activation Keywords")
        assert section_idx < footer_idx

    @pytest.mark.edge_case
    def test_inject_when_no_footer_then_sections_appended(self) -> None:
        # Arrange
        body = "## Purpose\n\nContent with no footer.\n"
        sections = "## Skill Version\n\n1.0.0\n"

        # Act
        result = ComposeSkillsCommandHandler._inject_before_footer(body, sections)

        # Assert
        assert result.endswith("## Skill Version\n\n1.0.0\n\n")
        assert "## Purpose" in result


class TestBuildFrontmatter:
    """Tests for static _build_frontmatter method."""

    @pytest.mark.happy_path
    def test_build_frontmatter_when_canonical_sources_then_name_and_description(
        self,
    ) -> None:
        # Arrange
        skill = CanonicalSkill(
            name="test-skill",
            version="1.0.0",
            description="A test skill for testing",
        )

        # Act
        fm = ComposeSkillsCommandHandler._build_frontmatter(skill)

        # Assert
        assert fm["name"] == "test-skill"
        assert fm["description"] == "A test skill for testing"
        assert "version" not in fm  # version is governance, not frontmatter

    @pytest.mark.happy_path
    def test_build_frontmatter_when_vendor_overrides_then_merged(self) -> None:
        # Arrange
        skill = CanonicalSkill(
            name="test-skill",
            version="1.0.0",
            description="A test skill",
            vendor_overrides={"allowed-tools": "Read, Write, Edit"},
        )

        # Act
        fm = ComposeSkillsCommandHandler._build_frontmatter(skill)

        # Assert
        assert fm["name"] == "test-skill"
        assert fm["description"] == "A test skill"
        assert fm["allowed-tools"] == "Read, Write, Edit"

    @pytest.mark.edge_case
    def test_build_frontmatter_when_vendor_overrides_name_then_name_not_overridden(
        self,
    ) -> None:
        # Arrange — vendor override tries to set name (should be ignored)
        skill = CanonicalSkill(
            name="canonical-name",
            version="1.0.0",
            description="A test skill",
            vendor_overrides={"name": "vendor-name", "allowed-tools": "Read"},
        )

        # Act
        fm = ComposeSkillsCommandHandler._build_frontmatter(skill)

        # Assert — name always from jerry.yaml, never vendor
        assert fm["name"] == "canonical-name"
        assert fm["allowed-tools"] == "Read"

    @pytest.mark.edge_case
    def test_build_frontmatter_when_no_description_then_description_absent(
        self,
    ) -> None:
        # Arrange
        skill = CanonicalSkill(
            name="test-skill",
            version="1.0.0",
        )

        # Act
        fm = ComposeSkillsCommandHandler._build_frontmatter(skill)

        # Assert
        assert fm["name"] == "test-skill"
        assert "description" not in fm


class TestBuildGovernanceDict:
    """Tests for static _build_governance_dict method."""

    @pytest.mark.happy_path
    def test_build_when_all_fields_then_dict_populated(self) -> None:
        # Arrange
        skill = CanonicalSkill(
            name="test",
            version="1.0.0",
            activation_keywords=("a", "b"),
            agents=("agent-1",),
            context_injection={"key": "value"},
        )

        # Act
        result = ComposeSkillsCommandHandler._build_governance_dict(skill)

        # Assert
        assert result["version"] == "1.0.0"
        assert result["activation-keywords"] == ["a", "b"]
        assert result["agents"] == ["agent-1"]
        assert result["context_injection"] == {"key": "value"}

    @pytest.mark.edge_case
    def test_build_when_empty_fields_then_dict_empty(self) -> None:
        # Arrange
        skill = CanonicalSkill(
            name="test",
            version="",
            activation_keywords=(),
            agents=(),
            context_injection={},
        )

        # Act
        result = ComposeSkillsCommandHandler._build_governance_dict(skill)

        # Assert
        assert result == {}


class TestParseErrorSurfacing:
    """Tests for FM-02: parse error surfacing from list_all_with_diagnostics."""

    @pytest.mark.negative
    def test_handle_when_parse_errors_then_warnings_populated(
        self,
        mock_repository: MagicMock,
        governance_builder: SkillGovernanceSectionBuilder,
        tmp_path: Path,
    ) -> None:
        # Arrange — list_all_with_diagnostics returns one good skill + parse errors
        skill = CanonicalSkill(
            name="good-skill",
            version="1.0.0",
            activation_keywords=("test",),
            prompt_body="## Purpose\n\nPurpose.\n",
        )
        mock_repository.list_all_with_diagnostics.return_value = (
            [skill],
            ["bad-skill: failed to parse /path/to/bad.yaml"],
        )
        skill_md = tmp_path / "good-skill" / "SKILL.md"
        mock_repository.get_skill_md_path.return_value = skill_md

        handler = _make_handler(mock_repository, governance_builder)
        command = ComposeSkillsCommand()

        # Act
        result = handler.handle(command)

        # Assert
        assert result.composed == 1
        assert any("Parse error" in w for w in result.warnings)
        assert any("bad-skill" in w for w in result.warnings)


class TestBoldFooterHandling:
    """Tests for FM-07: broadened footer regex handles bold markers."""

    @pytest.mark.regression
    def test_inject_when_bold_footer_then_sections_before_footer(self) -> None:
        # Arrange — bold footer: **Skill Version:**
        body = "## Purpose\n\nContent.\n\n**Skill Version: 1.0.0**\n"
        sections = "## Activation Keywords\n\n- test\n"

        # Act
        result = ComposeSkillsCommandHandler._inject_before_footer(body, sections)

        # Assert
        footer_idx = result.index("**Skill Version:")
        section_idx = result.index("## Activation Keywords")
        assert section_idx < footer_idx

    @pytest.mark.regression
    def test_inject_when_single_star_footer_then_sections_before_footer(self) -> None:
        # Arrange — original format: *Skill Version:*
        body = "## Purpose\n\nContent.\n\n*Skill Version: 1.0.0*\n"
        sections = "## Skill Version\n\n2.0.0\n"

        # Act
        result = ComposeSkillsCommandHandler._inject_before_footer(body, sections)

        # Assert
        footer_idx = result.index("*Skill Version:")
        section_idx = result.index("## Skill Version")
        assert section_idx < footer_idx

    @pytest.mark.regression
    def test_inject_when_no_star_footer_then_sections_before_footer(self) -> None:
        # Arrange — plain footer: Skill Version:
        body = "## Purpose\n\nContent.\n\nSkill Version: 1.0.0\n"
        sections = "## Activation Keywords\n\n- test\n"

        # Act
        result = ComposeSkillsCommandHandler._inject_before_footer(body, sections)

        # Assert
        footer_idx = result.index("Skill Version:")
        section_idx = result.index("## Activation Keywords")
        assert section_idx < footer_idx


class TestComposedOutputRoundtrip:
    """Regression tests for compose output stability."""

    @pytest.mark.regression
    def test_compose_roundtrip_when_recomposed_then_identical_structure(
        self,
        mock_repository: MagicMock,
        governance_builder: SkillGovernanceSectionBuilder,
        prompt_transformer: PromptTransformer,
        tmp_path: Path,
    ) -> None:
        # Arrange — canonical sources are stable inputs; compose should be idempotent
        skill = CanonicalSkill(
            name="roundtrip",
            version="1.0.0",
            activation_keywords=("test",),
            agents=("agent-1",),
            prompt_body="## Purpose\n\nRoundtrip test.\n\n*Skill Version: 1.0.0*\n",
        )
        mock_repository.get.return_value = skill
        skill_md = tmp_path / "roundtrip" / "SKILL.md"
        mock_repository.get_skill_md_path.return_value = skill_md

        handler = _make_handler(
            mock_repository, governance_builder, prompt_transformer=prompt_transformer
        )
        command = ComposeSkillsCommand(skill_name="roundtrip")

        # Act — compose twice (canonical sources unchanged between runs)
        handler.handle(command)
        first_output = skill_md.read_text()

        handler.handle(command)
        second_output = skill_md.read_text()

        # Assert — second compose produces same output
        assert first_output == second_output


class TestXmlGovernanceOutput:
    """Tests for BUG-002: governance sections wrapped in XML tags when transformer is provided."""

    @pytest.mark.happy_path
    def test_compose_when_transformer_provided_then_xml_governance_tags_in_output(
        self,
        mock_repository: MagicMock,
        governance_builder: SkillGovernanceSectionBuilder,
        prompt_transformer: PromptTransformer,
        tmp_path: Path,
    ) -> None:
        # Arrange
        skill = CanonicalSkill(
            name="xml-test",
            version="2.0.0",
            activation_keywords=("research", "analyze"),
            agents=("ps-researcher",),
            prompt_body="## Purpose\n\nTest skill.\n\n*Skill Version: 1.0.0*\n",
        )
        mock_repository.get.return_value = skill
        skill_md = tmp_path / "xml-test" / "SKILL.md"
        mock_repository.get_skill_md_path.return_value = skill_md

        handler = _make_handler(
            mock_repository, governance_builder, prompt_transformer=prompt_transformer
        )
        command = ComposeSkillsCommand(skill_name="xml-test")

        # Act
        handler.handle(command)
        output = skill_md.read_text()

        # Assert — governance sections wrapped in XML tags
        assert "<skill_version>" in output
        assert "</skill_version>" in output
        assert "<activation_keywords>" in output
        assert "</activation_keywords>" in output
        assert "<agent_registry>" in output
        assert "</agent_registry>" in output
        # Original ## headings should NOT appear for governance sections
        assert "## Skill Version" not in output
        assert "## Activation Keywords" not in output
        assert "## Agent Registry" not in output

    @pytest.mark.happy_path
    def test_compose_when_no_transformer_then_markdown_governance_headings_in_output(
        self,
        mock_repository: MagicMock,
        governance_builder: SkillGovernanceSectionBuilder,
        tmp_path: Path,
    ) -> None:
        # Arrange
        skill = CanonicalSkill(
            name="md-test",
            version="1.0.0",
            activation_keywords=("test",),
            prompt_body="## Purpose\n\nTest skill.\n\n*Skill Version: 1.0.0*\n",
        )
        mock_repository.get.return_value = skill
        skill_md = tmp_path / "md-test" / "SKILL.md"
        mock_repository.get_skill_md_path.return_value = skill_md

        # No prompt_transformer — fallback to markdown headings
        handler = _make_handler(mock_repository, governance_builder)
        command = ComposeSkillsCommand(skill_name="md-test")

        # Act
        handler.handle(command)
        output = skill_md.read_text()

        # Assert — governance sections use ## headings (no XML)
        assert "## Skill Version" in output
        assert "<skill_version>" not in output


class TestStripGovernanceSections:
    """Tests for _strip_governance_sections method."""

    @pytest.mark.happy_path
    def test_strip_when_heading_governance_then_removed(self) -> None:
        body = (
            "## Purpose\n\nContent.\n\n"
            "## Skill Version\n\n1.0.0\n\n"
            "## Activation Keywords\n\n- test\n"
        )
        result = ComposeSkillsCommandHandler._strip_governance_sections(body)
        assert "## Skill Version" not in result
        assert "## Activation Keywords" not in result
        assert "## Purpose" in result
        assert "Content." in result

    @pytest.mark.happy_path
    def test_strip_when_xml_governance_then_removed(self) -> None:
        body = (
            "## Purpose\n\nContent.\n\n"
            "<skill_version>\n1.0.0\n</skill_version>\n\n"
            "<activation_keywords>\n- test\n</activation_keywords>\n"
        )
        result = ComposeSkillsCommandHandler._strip_governance_sections(body)
        assert "<skill_version>" not in result
        assert "</skill_version>" not in result
        assert "<activation_keywords>" not in result
        assert "## Purpose" in result

    @pytest.mark.regression
    def test_strip_when_footer_after_last_governance_then_footer_preserved(self) -> None:
        """BUG-002 regression: footer lines after last governance heading must be preserved."""
        body = (
            "## Purpose\n\nContent.\n\n"
            "## Skill Version\n\n1.0.0\n\n"
            "## Activation Keywords\n\n- test\n\n"
            "## Agent Registry\n\n- agent-1\n\n"
            "*Skill Version: 1.0.0*\n"
            "*Constitutional Compliance: Jerry Constitution v1.0*\n"
        )
        result = ComposeSkillsCommandHandler._strip_governance_sections(body)
        assert "## Skill Version" not in result
        assert "## Agent Registry" not in result
        assert "*Skill Version: 1.0.0*" in result
        assert "*Constitutional Compliance:" in result
        assert "## Purpose" in result

    @pytest.mark.edge_case
    def test_strip_when_code_block_contains_governance_heading_then_preserved(self) -> None:
        body = (
            "## Purpose\n\nContent.\n\n"
            "```markdown\n## Skill Version\n\nInside code block.\n```\n\n"
            "## Skill Version\n\n1.0.0\n"
        )
        result = ComposeSkillsCommandHandler._strip_governance_sections(body)
        # The code block content should be preserved
        assert "Inside code block." in result
        # The actual governance section should be stripped
        assert result.count("## Skill Version") == 1  # only the one inside code block

    @pytest.mark.edge_case
    def test_strip_when_no_governance_sections_then_body_unchanged(self) -> None:
        body = "## Purpose\n\nContent only.\n\n## References\n\nLinks.\n"
        result = ComposeSkillsCommandHandler._strip_governance_sections(body)
        assert result == body

    @pytest.mark.regression
    def test_strip_idempotent_on_xml_then_heading_cycle(self) -> None:
        """Stripping XML-formatted governance enables rebuild as headings."""
        body = (
            "## Purpose\n\nContent.\n\n"
            "<skill_version>\n1.0.0\n</skill_version>\n\n"
            "<agent_registry>\n- agent-1\n</agent_registry>\n\n"
            "*Skill Version: 1.0.0*\n"
        )
        result = ComposeSkillsCommandHandler._strip_governance_sections(body)
        assert "<skill_version>" not in result
        assert "<agent_registry>" not in result
        assert "*Skill Version: 1.0.0*" in result
        assert "## Purpose" in result
