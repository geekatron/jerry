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
- Reads description from skill.jerry.yaml (happy path)
- Prefers skill.jerry.prompt.md over SKILL.md body (happy path)
- Falls back to SKILL.md when no prompt.md exists (edge case)
- Reads vendor overrides from skill.claude-code.yaml (happy path)
- No vendor overrides returns empty dict (edge case)
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
    prompt_md_content: str | None = None,
    vendor_yaml_content: str | None = None,
) -> None:
    """Helper to create a skill directory with composition files."""
    skill_dir = skills_dir / name
    comp_dir = skill_dir / "composition"
    comp_dir.mkdir(parents=True, exist_ok=True)
    (comp_dir / "skill.jerry.yaml").write_text(yaml_content, encoding="utf-8")
    if skill_md_content is not None:
        (skill_dir / "SKILL.md").write_text(skill_md_content, encoding="utf-8")
    if prompt_md_content is not None:
        (comp_dir / "skill.jerry.prompt.md").write_text(prompt_md_content, encoding="utf-8")
    if vendor_yaml_content is not None:
        (comp_dir / "skill.claude-code.yaml").write_text(vendor_yaml_content, encoding="utf-8")


class TestGet:
    """Tests for get() method."""

    @pytest.mark.happy_path
    def test_get_when_skill_exists_then_returns_canonical_skill(self, skills_dir: Path) -> None:
        # Arrange
        _create_skill(
            skills_dir,
            "problem-solving",
            'name: problem-solving\nversion: 1.0.0\ndescription: "Solve problems"\nactivation-keywords:\n  - research\n  - analyze\nagents:\n  - ps-researcher\n',
            "---\nname: problem-solving\ndescription: Solve problems\n---\n## Purpose\n\nSolve problems.\n",
        )
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        skill = repo.get("problem-solving")

        # Assert
        assert skill is not None
        assert skill.name == "problem-solving"
        assert skill.version == "1.0.0"
        assert skill.description == "Solve problems"
        assert skill.activation_keywords == ("research", "analyze")
        assert skill.agents == ("ps-researcher",)
        assert "Solve problems" in skill.prompt_body

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
        assert skill.prompt_body == ""

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


class TestGetDescription:
    """Tests for description field loading from skill.jerry.yaml."""

    @pytest.mark.happy_path
    def test_get_when_description_in_yaml_then_populated(self, skills_dir: Path) -> None:
        # Arrange
        _create_skill(
            skills_dir,
            "desc-skill",
            'name: desc-skill\nversion: 1.0.0\ndescription: "A test skill for validation"\n',
        )
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        skill = repo.get("desc-skill")

        # Assert
        assert skill is not None
        assert skill.description == "A test skill for validation"

    @pytest.mark.edge_case
    def test_get_when_no_description_in_yaml_then_empty_string(self, skills_dir: Path) -> None:
        # Arrange
        _create_skill(
            skills_dir,
            "no-desc",
            "name: no-desc\nversion: 1.0.0\n",
        )
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        skill = repo.get("no-desc")

        # Assert
        assert skill is not None
        assert skill.description == ""


class TestGetPromptBody:
    """Tests for prompt body loading with source preference."""

    @pytest.mark.happy_path
    def test_get_when_prompt_md_exists_then_prefers_prompt_md(self, skills_dir: Path) -> None:
        # Arrange — both prompt.md and SKILL.md exist; prompt.md should win
        _create_skill(
            skills_dir,
            "both-sources",
            "name: both-sources\nversion: 1.0.0\n",
            skill_md_content="---\nname: both-sources\ndescription: T\n---\n## From SKILL.md\n\nOld body.\n",
            prompt_md_content="## From Prompt MD\n\nNew canonical body.\n",
        )
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        skill = repo.get("both-sources")

        # Assert
        assert skill is not None
        assert "From Prompt MD" in skill.prompt_body
        assert "From SKILL.md" not in skill.prompt_body

    @pytest.mark.edge_case
    def test_get_when_no_prompt_md_then_falls_back_to_skill_md(self, skills_dir: Path) -> None:
        # Arrange — only SKILL.md, no prompt.md
        _create_skill(
            skills_dir,
            "fallback",
            "name: fallback\nversion: 1.0.0\n",
            skill_md_content="---\nname: fallback\ndescription: T\n---\n## Fallback Body\n\nFrom SKILL.md.\n",
        )
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        skill = repo.get("fallback")

        # Assert
        assert skill is not None
        assert "Fallback Body" in skill.prompt_body

    @pytest.mark.edge_case
    def test_get_when_no_prompt_md_and_no_skill_md_then_empty_body(self, skills_dir: Path) -> None:
        # Arrange — neither file exists
        _create_skill(
            skills_dir,
            "no-body",
            "name: no-body\nversion: 1.0.0\n",
        )
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        skill = repo.get("no-body")

        # Assert
        assert skill is not None
        assert skill.prompt_body == ""


class TestGetVendorOverrides:
    """Tests for vendor overrides loading from skill.claude-code.yaml."""

    @pytest.mark.happy_path
    def test_get_when_vendor_yaml_exists_then_overrides_populated(self, skills_dir: Path) -> None:
        # Arrange
        _create_skill(
            skills_dir,
            "vendor-skill",
            "name: vendor-skill\nversion: 1.0.0\n",
            vendor_yaml_content="allowed-tools:\n  - Read\n  - Write\n  - Grep\n",
        )
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        skill = repo.get("vendor-skill")

        # Assert
        assert skill is not None
        assert skill.vendor_overrides == {"allowed-tools": ["Read", "Write", "Grep"]}

    @pytest.mark.edge_case
    def test_get_when_no_vendor_yaml_then_empty_overrides(self, skills_dir: Path) -> None:
        # Arrange — no skill.claude-code.yaml
        _create_skill(
            skills_dir,
            "no-vendor",
            "name: no-vendor\nversion: 1.0.0\n",
        )
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        skill = repo.get("no-vendor")

        # Assert
        assert skill is not None
        assert skill.vendor_overrides == {}

    @pytest.mark.negative
    def test_get_when_malformed_vendor_yaml_then_empty_overrides(self, skills_dir: Path) -> None:
        # Arrange
        _create_skill(
            skills_dir,
            "bad-vendor",
            "name: bad-vendor\nversion: 1.0.0\n",
            vendor_yaml_content="[broken yaml: nope\n",
        )
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        skill = repo.get("bad-vendor")

        # Assert
        assert skill is not None
        assert skill.vendor_overrides == {}


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


class TestListAllWithDiagnostics:
    """Tests for list_all_with_diagnostics() method (FM-02)."""

    @pytest.mark.happy_path
    def test_list_all_with_diagnostics_when_all_valid_then_no_errors(
        self, skills_dir: Path
    ) -> None:
        # Arrange
        _create_skill(skills_dir, "alpha", "name: alpha\nversion: 1.0.0\n")
        _create_skill(skills_dir, "beta", "name: beta\nversion: 2.0.0\n")
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        skills, errors = repo.list_all_with_diagnostics()

        # Assert
        assert len(skills) == 2
        assert len(errors) == 0

    @pytest.mark.negative
    def test_list_all_with_diagnostics_when_malformed_yaml_then_error_reported(
        self, skills_dir: Path
    ) -> None:
        # Arrange
        _create_skill(skills_dir, "good", "name: good\nversion: 1.0.0\n")
        _create_skill(skills_dir, "bad", "name: [broken yaml\n  bad: true: nope\n")
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        skills, errors = repo.list_all_with_diagnostics()

        # Assert
        assert len(skills) == 1
        assert skills[0].name == "good"
        assert len(errors) == 1
        assert "bad" in errors[0]

    @pytest.mark.edge_case
    def test_list_all_with_diagnostics_when_no_skills_then_both_empty(
        self, skills_dir: Path
    ) -> None:
        # Arrange
        skills_dir.mkdir(parents=True, exist_ok=True)
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        skills, errors = repo.list_all_with_diagnostics()

        # Assert
        assert skills == []
        assert errors == []

    @pytest.mark.negative
    def test_list_all_with_diagnostics_when_scalar_yaml_then_error_reported(
        self, skills_dir: Path
    ) -> None:
        # Arrange — YAML that parses to a scalar, not a dict
        _create_skill(skills_dir, "scalar-skill", "just a string\n")
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        skills, errors = repo.list_all_with_diagnostics()

        # Assert
        assert len(skills) == 0
        assert len(errors) == 1
        assert "scalar-skill" in errors[0]


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


class TestGetAgentBodyFormats:
    """Tests for get_agent_body_formats() method (SCV-008 support)."""

    @pytest.mark.happy_path
    def test_get_agent_body_formats_when_agents_have_body_format_then_dict_returned(
        self, skills_dir: Path
    ) -> None:
        # Arrange
        _create_skill(skills_dir, "my-skill", "name: my-skill\nversion: 1.0.0\n")
        comp_dir = skills_dir / "my-skill" / "composition"
        (comp_dir / "agent-a.jerry.yaml").write_text(
            "name: agent-a\nportability:\n  body_format: xml\n", encoding="utf-8"
        )
        (comp_dir / "agent-b.jerry.yaml").write_text(
            "name: agent-b\nportability:\n  body_format: markdown\n", encoding="utf-8"
        )
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        result = repo.get_agent_body_formats("my-skill")

        # Assert
        assert result == {"agent-a": "xml", "agent-b": "markdown"}

    @pytest.mark.happy_path
    def test_get_agent_body_formats_when_all_same_then_consistent(self, skills_dir: Path) -> None:
        # Arrange
        _create_skill(skills_dir, "consistent", "name: consistent\nversion: 1.0.0\n")
        comp_dir = skills_dir / "consistent" / "composition"
        (comp_dir / "agent-x.jerry.yaml").write_text(
            "name: agent-x\nportability:\n  body_format: xml\n", encoding="utf-8"
        )
        (comp_dir / "agent-y.jerry.yaml").write_text(
            "name: agent-y\nportability:\n  body_format: xml\n", encoding="utf-8"
        )
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        result = repo.get_agent_body_formats("consistent")

        # Assert
        assert result == {"agent-x": "xml", "agent-y": "xml"}

    @pytest.mark.edge_case
    def test_get_agent_body_formats_when_no_composition_dir_then_empty(
        self, skills_dir: Path
    ) -> None:
        # Arrange — skill dir exists but no composition subdir
        (skills_dir / "empty-skill").mkdir(parents=True, exist_ok=True)
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        result = repo.get_agent_body_formats("empty-skill")

        # Assert
        assert result == {}

    @pytest.mark.edge_case
    def test_get_agent_body_formats_when_no_portability_field_then_skipped(
        self, skills_dir: Path
    ) -> None:
        # Arrange — agent yaml without portability section
        _create_skill(skills_dir, "no-port", "name: no-port\nversion: 1.0.0\n")
        comp_dir = skills_dir / "no-port" / "composition"
        (comp_dir / "agent-c.jerry.yaml").write_text(
            "name: agent-c\nversion: 1.0.0\n", encoding="utf-8"
        )
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        result = repo.get_agent_body_formats("no-port")

        # Assert
        assert result == {}

    @pytest.mark.edge_case
    def test_get_agent_body_formats_skips_skill_jerry_yaml(self, skills_dir: Path) -> None:
        # Arrange — skill.jerry.yaml should be excluded (it's the skill-level source)
        _create_skill(skills_dir, "with-skill", "name: with-skill\nversion: 1.0.0\n")
        comp_dir = skills_dir / "with-skill" / "composition"
        (comp_dir / "agent-d.jerry.yaml").write_text(
            "name: agent-d\nportability:\n  body_format: xml\n", encoding="utf-8"
        )
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        result = repo.get_agent_body_formats("with-skill")

        # Assert — only agent-d, not "skill"
        assert "skill" not in result
        assert result == {"agent-d": "xml"}

    @pytest.mark.negative
    def test_get_agent_body_formats_when_malformed_yaml_then_skipped(
        self, skills_dir: Path
    ) -> None:
        # Arrange
        _create_skill(skills_dir, "bad-agent", "name: bad-agent\nversion: 1.0.0\n")
        comp_dir = skills_dir / "bad-agent" / "composition"
        (comp_dir / "agent-e.jerry.yaml").write_text("name: [broken yaml\n", encoding="utf-8")
        (comp_dir / "agent-f.jerry.yaml").write_text(
            "name: agent-f\nportability:\n  body_format: markdown\n", encoding="utf-8"
        )
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        result = repo.get_agent_body_formats("bad-agent")

        # Assert — malformed agent skipped, good agent included
        assert result == {"agent-f": "markdown"}

    @pytest.mark.edge_case
    def test_get_agent_body_formats_when_empty_body_format_then_skipped(
        self, skills_dir: Path
    ) -> None:
        # Arrange — body_format is empty string
        _create_skill(skills_dir, "empty-bf", "name: empty-bf\nversion: 1.0.0\n")
        comp_dir = skills_dir / "empty-bf" / "composition"
        (comp_dir / "agent-g.jerry.yaml").write_text(
            "name: agent-g\nportability:\n  body_format: ''\n", encoding="utf-8"
        )
        repo = FilesystemSkillRepository(skills_dir)

        # Act
        result = repo.get_agent_body_formats("empty-bf")

        # Assert
        assert result == {}


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
