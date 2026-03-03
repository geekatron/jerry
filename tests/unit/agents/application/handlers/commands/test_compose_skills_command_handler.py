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
from src.agents.domain.services.skill_governance_builder import (
    SkillGovernanceSectionBuilder,
)


@pytest.fixture()
def mock_repository() -> MagicMock:
    """Mock ISkillRepository."""
    repo = MagicMock()
    repo.get_skill_md_path.return_value = Path("/tmp/skills/test-skill/SKILL.md")
    return repo


@pytest.fixture()
def governance_builder() -> SkillGovernanceSectionBuilder:
    """Real governance builder."""
    return SkillGovernanceSectionBuilder()


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
        skill_body="## Purpose\n\nTest skill.\n\n*Skill Version: 1.0.0*\n",
    )


@pytest.fixture()
def sample_skill_no_footer() -> CanonicalSkill:
    """Sample canonical skill without footer in body."""
    return CanonicalSkill(
        name="no-footer-skill",
        version="1.0.0",
        activation_keywords=("test",),
        agents=(),
        skill_body="## Purpose\n\nNo footer here.\n",
    )


def _make_handler(
    repository: MagicMock,
    governance_builder: SkillGovernanceSectionBuilder,
    validator: MagicMock | None = None,
) -> ComposeSkillsCommandHandler:
    """Create handler with dependencies."""
    return ComposeSkillsCommandHandler(
        repository=repository,
        governance_builder=governance_builder,
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
    ) -> None:
        # Arrange
        mock_repository.get.return_value = sample_skill
        skill_md_path = Path("/tmp/skills/test-skill/SKILL.md")
        mock_repository.get_skill_md_path.return_value = skill_md_path
        skill_md_path.parent.mkdir(parents=True, exist_ok=True)

        # Write existing SKILL.md
        skill_md_path.write_text(
            "---\nname: test-skill\ndescription: A test skill\n---\n"
            "## Purpose\n\nTest skill.\n\n*Skill Version: 1.0.0*\n",
            encoding="utf-8",
        )

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
            skill_dir = tmp_path / name
            skill_dir.mkdir()
            skill_md = skill_dir / "SKILL.md"
            skill_md.write_text(
                f"---\nname: {name}\ndescription: Skill {name}\n---\n## Purpose\n\nPurpose.\n",
                encoding="utf-8",
            )
            skills.append(
                CanonicalSkill(
                    name=name,
                    version="1.0.0",
                    activation_keywords=("test",),
                    skill_body="## Purpose\n\nPurpose.\n",
                )
            )

        mock_repository.list_all.return_value = skills
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
        skill_md.write_text(
            "---\nname: test-skill\ndescription: Test\n---\n"
            "## Purpose\n\nTest.\n\n*Skill Version: 1.0.0*\n",
            encoding="utf-8",
        )
        original_content = skill_md.read_text()
        mock_repository.get_skill_md_path.return_value = skill_md

        handler = _make_handler(mock_repository, governance_builder)
        command = ComposeSkillsCommand(skill_name="test-skill", dry_run=True)

        # Act
        result = handler.handle(command)

        # Assert
        assert result.composed == 1
        assert result.dry_run is True
        # File should NOT be modified in dry run
        assert skill_md.read_text() == original_content


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
        skill_md.parent.mkdir(parents=True, exist_ok=True)
        skill_md.write_text(
            "---\nname: test-skill\ndescription: Test\n---\n"
            "## Purpose\n\nTest.\n\n*Skill Version: 1.0.0*\n",
            encoding="utf-8",
        )
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
        skill_md.parent.mkdir(parents=True, exist_ok=True)
        skill_md.write_text(
            "---\nname: test-skill\ndescription: Test\n---\n"
            "## Purpose\n\nTest.\n\n*Skill Version: 1.0.0*\n",
            encoding="utf-8",
        )
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


class TestParseMd:
    """Tests for static _parse_md method."""

    @pytest.mark.happy_path
    def test_parse_md_when_valid_frontmatter_then_dict_and_body(self) -> None:
        # Arrange
        content = "---\nname: test\ndescription: Test\n---\n## Body\n\nContent.\n"

        # Act
        fm, body = ComposeSkillsCommandHandler._parse_md(content)

        # Assert
        assert fm["name"] == "test"
        assert "## Body" in body

    @pytest.mark.edge_case
    def test_parse_md_when_no_frontmatter_then_empty_dict(self) -> None:
        # Arrange
        content = "# Just a heading\n\nBody content.\n"

        # Act
        fm, body = ComposeSkillsCommandHandler._parse_md(content)

        # Assert
        assert fm == {}
        assert "Just a heading" in body


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


class TestComposedOutputRoundtrip:
    """Regression tests for compose output stability."""

    @pytest.mark.regression
    def test_compose_roundtrip_when_recomposed_then_identical_structure(
        self,
        mock_repository: MagicMock,
        governance_builder: SkillGovernanceSectionBuilder,
        tmp_path: Path,
    ) -> None:
        # Arrange — first compose
        skill = CanonicalSkill(
            name="roundtrip",
            version="1.0.0",
            activation_keywords=("test",),
            agents=("agent-1",),
            skill_body="## Purpose\n\nRoundtrip test.\n\n*Skill Version: 1.0.0*\n",
        )
        mock_repository.get.return_value = skill
        skill_md = tmp_path / "roundtrip" / "SKILL.md"
        skill_md.parent.mkdir(parents=True, exist_ok=True)
        skill_md.write_text(
            "---\nname: roundtrip\ndescription: Roundtrip test\n---\n"
            "## Purpose\n\nRoundtrip test.\n\n*Skill Version: 1.0.0*\n",
            encoding="utf-8",
        )
        mock_repository.get_skill_md_path.return_value = skill_md

        handler = _make_handler(mock_repository, governance_builder)
        command = ComposeSkillsCommand(skill_name="roundtrip")

        # Act — compose twice
        handler.handle(command)
        first_output = skill_md.read_text()

        # Update skill_body with the composed content for second pass
        mock_repository.get_skill_md_path.return_value = skill_md
        handler.handle(command)
        second_output = skill_md.read_text()

        # Assert — second compose produces same output
        assert first_output == second_output
