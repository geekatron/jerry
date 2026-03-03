# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for FilesystemSkillRepository.

Coverage targets:
- get() returns parsed CanonicalSkill (happy path)
- get() returns None when not found (negative)
- list_all() returns all skills (happy path)
- list_all() skips non-directories and missing yaml (edge case)
- _parse_skill_md() splits frontmatter and body (happy path)
- get_skill_md_path() returns correct path (happy path)
- Malformed YAML returns None (negative)
- Missing SKILL.md results in empty body (edge case)
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.agents.infrastructure.persistence.filesystem_skill_repository import (
    FilesystemSkillRepository,
)


@pytest.fixture()
def skills_dir(tmp_path: Path) -> Path:
    """Create a temporary skills directory structure."""
    return tmp_path / "skills"


def _create_skill(
    skills_dir: Path,
    name: str,
    yaml_content: str,
    skill_md_content: str | None = None,
) -> None:
    """Helper to create a skill directory with composition files."""
    skill_dir = skills_dir / name
    comp_dir = skill_dir / "composition"
    comp_dir.mkdir(parents=True, exist_ok=True)
    (comp_dir / "skill.jerry.yaml").write_text(yaml_content, encoding="utf-8")
    if skill_md_content is not None:
        (skill_dir / "SKILL.md").write_text(skill_md_content, encoding="utf-8")


class TestGet:
    """Tests for get() method."""

    @pytest.mark.happy_path
    def test_get_when_skill_exists_then_returns_canonical_skill(self, skills_dir: Path) -> None:
        # Arrange
        _create_skill(
            skills_dir,
            "problem-solving",
            "name: problem-solving\nversion: 1.0.0\nactivation-keywords:\n  - research\n  - analyze\nagents:\n  - ps-researcher\n",
            "---\nname: problem-solving\ndescription: Test\n---\n## Purpose\n\nSolve problems.\n",
        )
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        skill = repo.get("problem-solving")

        # Assert
        assert skill is not None
        assert skill.name == "problem-solving"
        assert skill.version == "1.0.0"
        assert skill.activation_keywords == ("research", "analyze")
        assert skill.agents == ("ps-researcher",)
        assert "Solve problems" in skill.skill_body

    @pytest.mark.negative
    def test_get_when_skill_not_found_then_returns_none(self, skills_dir: Path) -> None:
        # Arrange
        skills_dir.mkdir(parents=True, exist_ok=True)
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        skill = repo.get("nonexistent")

        # Assert
        assert skill is None

    @pytest.mark.edge_case
    def test_get_when_no_skill_md_then_empty_body(self, skills_dir: Path) -> None:
        # Arrange — no SKILL.md, only yaml
        _create_skill(
            skills_dir,
            "no-md",
            "name: no-md\nversion: 1.0.0\n",
            skill_md_content=None,
        )
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        skill = repo.get("no-md")

        # Assert
        assert skill is not None
        assert skill.skill_body == ""

    @pytest.mark.negative
    def test_get_when_malformed_yaml_then_returns_none(self, skills_dir: Path) -> None:
        # Arrange
        _create_skill(
            skills_dir,
            "bad-yaml",
            "name: [invalid yaml\n  broken: true: nope\n",
        )
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        skill = repo.get("bad-yaml")

        # Assert
        assert skill is None

    @pytest.mark.edge_case
    def test_get_when_yaml_is_not_dict_then_returns_none(self, skills_dir: Path) -> None:
        # Arrange
        _create_skill(
            skills_dir,
            "scalar-yaml",
            "just a string\n",
        )
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        skill = repo.get("scalar-yaml")

        # Assert
        assert skill is None


class TestListAll:
    """Tests for list_all() method."""

    @pytest.mark.happy_path
    def test_list_all_when_multiple_skills_then_all_returned(self, skills_dir: Path) -> None:
        # Arrange
        _create_skill(skills_dir, "alpha", "name: alpha\nversion: 1.0.0\n")
        _create_skill(skills_dir, "beta", "name: beta\nversion: 2.0.0\n")
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        skills = repo.list_all()

        # Assert
        assert len(skills) == 2
        names = {s.name for s in skills}
        assert names == {"alpha", "beta"}

    @pytest.mark.edge_case
    def test_list_all_when_no_skills_then_empty_list(self, skills_dir: Path) -> None:
        # Arrange
        skills_dir.mkdir(parents=True, exist_ok=True)
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        skills = repo.list_all()

        # Assert
        assert skills == []

    @pytest.mark.edge_case
    def test_list_all_when_dir_has_files_not_dirs_then_skipped(self, skills_dir: Path) -> None:
        # Arrange
        skills_dir.mkdir(parents=True, exist_ok=True)
        (skills_dir / "README.md").write_text("# Skills\n", encoding="utf-8")
        _create_skill(skills_dir, "real-skill", "name: real-skill\nversion: 1.0.0\n")
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        skills = repo.list_all()

        # Assert
        assert len(skills) == 1
        assert skills[0].name == "real-skill"

    @pytest.mark.edge_case
    def test_list_all_when_skill_dir_has_no_composition_then_skipped(
        self, skills_dir: Path
    ) -> None:
        # Arrange
        (skills_dir / "no-comp").mkdir(parents=True, exist_ok=True)
        _create_skill(skills_dir, "has-comp", "name: has-comp\nversion: 1.0.0\n")
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        skills = repo.list_all()

        # Assert
        assert len(skills) == 1
        assert skills[0].name == "has-comp"

    @pytest.mark.happy_path
    def test_list_all_returns_skills_sorted_by_directory_name(self, skills_dir: Path) -> None:
        # Arrange — create in reverse order
        _create_skill(skills_dir, "zeta", "name: zeta\nversion: 1.0.0\n")
        _create_skill(skills_dir, "alpha", "name: alpha\nversion: 1.0.0\n")
        _create_skill(skills_dir, "mid", "name: mid\nversion: 1.0.0\n")
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        skills = repo.list_all()

        # Assert
        names = [s.name for s in skills]
        assert names == ["alpha", "mid", "zeta"]


class TestGetSkillMdPath:
    """Tests for get_skill_md_path() method."""

    @pytest.mark.happy_path
    def test_get_skill_md_path_returns_correct_path(self, skills_dir: Path) -> None:
        # Arrange
        skills_dir.mkdir(parents=True, exist_ok=True)
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        result = repo.get_skill_md_path("problem-solving")

        # Assert
        assert result == skills_dir / "problem-solving" / "SKILL.md"


class TestParseSkillMd:
    """Tests for static _parse_skill_md() method."""

    @pytest.mark.happy_path
    def test_parse_when_valid_frontmatter_then_dict_and_body(self) -> None:
        # Arrange
        content = "---\nname: test\ndescription: Test\n---\n## Body\n\nContent.\n"

        # Act
        fm, body = FilesystemSkillRepository._parse_skill_md(content)

        # Assert
        assert fm["name"] == "test"
        assert "## Body" in body

    @pytest.mark.edge_case
    def test_parse_when_no_frontmatter_then_empty_dict_full_body(self) -> None:
        # Arrange
        content = "# No frontmatter\n\nJust body.\n"

        # Act
        fm, body = FilesystemSkillRepository._parse_skill_md(content)

        # Assert
        assert fm == {}
        assert "No frontmatter" in body

    @pytest.mark.edge_case
    def test_parse_when_unclosed_frontmatter_then_empty_dict_full_body(self) -> None:
        # Arrange
        content = "---\nname: test\nno closing delimiter\n"

        # Act
        fm, body = FilesystemSkillRepository._parse_skill_md(content)

        # Assert
        assert fm == {}

    @pytest.mark.negative
    def test_parse_when_invalid_yaml_frontmatter_then_empty_dict(self) -> None:
        # Arrange
        content = "---\n: [broken yaml\n---\nBody.\n"

        # Act
        fm, body = FilesystemSkillRepository._parse_skill_md(content)

        # Assert
        assert fm == {}
        assert "Body" in body


class TestSecurityChecks:
    """Security-focused tests."""

    @pytest.mark.security
    def test_get_when_path_traversal_in_name_then_not_found(self, skills_dir: Path) -> None:
        # Arrange
        skills_dir.mkdir(parents=True, exist_ok=True)
        repo = FilesystemSkillRepository(skills_dir)

        # Act — path traversal attempt
        skill = repo.get("../../../etc/passwd")

        # Assert
        assert skill is None

    @pytest.mark.security
    def test_get_when_absolute_path_in_name_then_not_found(self, skills_dir: Path) -> None:
        # Arrange
        skills_dir.mkdir(parents=True, exist_ok=True)
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        skill = repo.get("/etc/passwd")

        # Assert
        assert skill is None
