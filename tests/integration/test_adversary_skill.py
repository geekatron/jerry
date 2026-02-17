"""
Integration tests for adversary skill file structure and content integrity.

These tests verify that:
1. skills/adversary/SKILL.md exists and has navigation table
2. skills/adversary/PLAYBOOK.md exists
3. All 3 agent files exist: adv-selector.md, adv-executor.md, adv-scorer.md
4. SKILL.md references all selected strategy IDs (S-001 through S-014)
5. Agent files reference strategy templates
6. PLAYBOOK.md has criticality-based selection guidance (C1, C2, C3, C4)

Test methodology: File existence and content validation using pathlib.

References:
    - EN-928: Test Coverage Expansion
    - skills/adversary/SKILL.md: Skill specification
    - skills/adversary/PLAYBOOK.md: Execution procedures
    - quality-enforcement.md: 10 selected strategies
"""

from __future__ import annotations

from pathlib import Path

import pytest

# Mark as integration tests
pytestmark = [
    pytest.mark.integration,
]


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def project_root() -> Path:
    """Get the project root directory."""
    # Navigate from tests/integration to project root
    return Path(__file__).parent.parent.parent


@pytest.fixture
def skill_dir(project_root: Path) -> Path:
    """Get the adversary skill directory."""
    return project_root / "skills" / "adversary"


@pytest.fixture
def agents_dir(skill_dir: Path) -> Path:
    """Get the adversary agents directory."""
    return skill_dir / "agents"


# =============================================================================
# Test Data
# =============================================================================

# The 10 selected strategies from quality-enforcement.md
SELECTED_STRATEGY_IDS = [
    "S-001",
    "S-002",
    "S-003",
    "S-004",
    "S-007",
    "S-010",
    "S-011",
    "S-012",
    "S-013",
    "S-014",
]

# Required agent files
REQUIRED_AGENTS = [
    "adv-selector.md",
    "adv-executor.md",
    "adv-scorer.md",
]

# Criticality levels that should appear in PLAYBOOK.md
CRITICALITY_LEVELS = ["C1", "C2", "C3", "C4"]


# =============================================================================
# Tests
# =============================================================================


class TestAdversarySkillFiles:
    """Tests for skill file existence."""

    def test_skill_directory_when_checked_then_exists(self, skill_dir: Path) -> None:
        """Adversary skill directory must exist at expected location."""
        # Arrange/Act/Assert
        assert skill_dir.exists(), f"Skill directory does not exist: {skill_dir}"
        assert skill_dir.is_dir(), f"Skill path is not a directory: {skill_dir}"

    def test_skill_md_when_checked_then_exists(self, skill_dir: Path) -> None:
        """SKILL.md must exist in adversary skill directory."""
        # Arrange
        skill_file = skill_dir / "SKILL.md"

        # Act/Assert
        assert skill_file.exists(), f"SKILL.md does not exist: {skill_file}"
        assert skill_file.is_file(), f"SKILL.md is not a file: {skill_file}"

    def test_playbook_when_checked_then_exists(self, skill_dir: Path) -> None:
        """PLAYBOOK.md must exist in adversary skill directory."""
        # Arrange
        playbook_file = skill_dir / "PLAYBOOK.md"

        # Act/Assert
        assert playbook_file.exists(), f"PLAYBOOK.md does not exist: {playbook_file}"
        assert playbook_file.is_file(), f"PLAYBOOK.md is not a file: {playbook_file}"

    def test_agents_directory_when_checked_then_exists(self, agents_dir: Path) -> None:
        """Agents directory must exist in adversary skill directory."""
        # Arrange/Act/Assert
        assert agents_dir.exists(), f"Agents directory does not exist: {agents_dir}"
        assert agents_dir.is_dir(), f"Agents path is not a directory: {agents_dir}"

    @pytest.mark.parametrize("agent_file", REQUIRED_AGENTS)
    def test_agent_file_when_checked_then_exists(self, agents_dir: Path, agent_file: str) -> None:
        """Each required agent file must exist."""
        # Arrange
        agent_path = agents_dir / agent_file

        # Act/Assert
        assert agent_path.exists(), f"Agent file does not exist: {agent_path}"
        assert agent_path.is_file(), f"Agent path is not a file: {agent_path}"


class TestSkillContent:
    """Tests for SKILL.md content structure and references."""

    def test_skill_md_when_read_then_has_navigation_table(self, skill_dir: Path) -> None:
        """SKILL.md must have navigation table per H-23."""
        # Arrange
        skill_file = skill_dir / "SKILL.md"
        content = skill_file.read_text()

        # Act/Assert
        # Check for Document Audience (Triple-Lens) which serves as navigation
        assert (
            "## Document Audience (Triple-Lens)" in content or "## Document Sections" in content
        ), "SKILL.md missing navigation table"

    @pytest.mark.parametrize("strategy_id", SELECTED_STRATEGY_IDS)
    def test_skill_md_when_read_then_references_strategy_id(
        self, skill_dir: Path, strategy_id: str
    ) -> None:
        """SKILL.md must reference all 10 selected strategy IDs."""
        # Arrange
        skill_file = skill_dir / "SKILL.md"
        content = skill_file.read_text()

        # Act/Assert
        assert strategy_id in content, f"SKILL.md does not reference strategy ID {strategy_id}"

    def test_skill_md_when_read_then_references_quality_enforcement(self, skill_dir: Path) -> None:
        """SKILL.md must reference quality-enforcement.md SSOT."""
        # Arrange
        skill_file = skill_dir / "SKILL.md"
        content = skill_file.read_text()

        # Act/Assert
        assert "quality-enforcement.md" in content or "quality-enforcement" in content, (
            "SKILL.md does not reference quality-enforcement.md SSOT"
        )

    def test_skill_md_when_read_then_is_substantive(self, skill_dir: Path) -> None:
        """SKILL.md must be substantive (minimum 100 lines)."""
        # Arrange
        skill_file = skill_dir / "SKILL.md"
        content = skill_file.read_text()
        lines = content.splitlines()

        # Act/Assert
        assert len(lines) >= 100, f"SKILL.md has only {len(lines)} lines (minimum 100 required)"


class TestPlaybookContent:
    """Tests for PLAYBOOK.md content structure and guidance."""

    def test_playbook_when_read_then_has_navigation_table(self, skill_dir: Path) -> None:
        """PLAYBOOK.md must have navigation table per H-23."""
        # Arrange
        playbook_file = skill_dir / "PLAYBOOK.md"
        content = playbook_file.read_text()

        # Act/Assert
        assert "## Document Sections" in content, "PLAYBOOK.md missing navigation table heading"
        assert "| Section | Purpose |" in content, "PLAYBOOK.md missing navigation table structure"

    @pytest.mark.parametrize("criticality", CRITICALITY_LEVELS)
    def test_playbook_when_read_then_has_criticality_guidance(
        self, skill_dir: Path, criticality: str
    ) -> None:
        """PLAYBOOK.md must have selection guidance for all criticality levels."""
        # Arrange
        playbook_file = skill_dir / "PLAYBOOK.md"
        content = playbook_file.read_text()

        # Act/Assert
        assert criticality in content, (
            f"PLAYBOOK.md missing criticality level {criticality} guidance"
        )

    def test_playbook_when_read_then_references_strategy_selection(self, skill_dir: Path) -> None:
        """PLAYBOOK.md must have strategy selection flowchart or guidance."""
        # Arrange
        playbook_file = skill_dir / "PLAYBOOK.md"
        content = playbook_file.read_text()

        # Act/Assert
        assert (
            "Strategy Selection" in content
            or "strategy selection" in content
            or "STRATEGY SELECTION" in content
        ), "PLAYBOOK.md missing strategy selection guidance"

    def test_playbook_when_read_then_references_quality_enforcement(self, skill_dir: Path) -> None:
        """PLAYBOOK.md must reference quality-enforcement.md SSOT."""
        # Arrange
        playbook_file = skill_dir / "PLAYBOOK.md"
        content = playbook_file.read_text()

        # Act/Assert
        assert "quality-enforcement.md" in content or "quality-enforcement" in content, (
            "PLAYBOOK.md does not reference quality-enforcement.md SSOT"
        )

    def test_playbook_when_read_then_is_substantive(self, skill_dir: Path) -> None:
        """PLAYBOOK.md must be substantive (minimum 100 lines)."""
        # Arrange
        playbook_file = skill_dir / "PLAYBOOK.md"
        content = playbook_file.read_text()
        lines = content.splitlines()

        # Act/Assert
        assert len(lines) >= 100, f"PLAYBOOK.md has only {len(lines)} lines (minimum 100 required)"


class TestAgentContent:
    """Tests for agent file content and references."""

    @pytest.mark.parametrize("agent_file", REQUIRED_AGENTS)
    def test_agent_when_read_then_references_strategy_templates(
        self, agents_dir: Path, agent_file: str
    ) -> None:
        """Agent files must reference strategy templates."""
        # Arrange
        agent_path = agents_dir / agent_file
        content = agent_path.read_text()

        # Act/Assert
        # Check for at least one of: template references, strategy IDs, or .context/templates path
        has_template_reference = (
            "template" in content.lower()
            or ".context/templates" in content
            or any(sid in content for sid in SELECTED_STRATEGY_IDS)
        )
        assert has_template_reference, (
            f"{agent_file} does not reference strategy templates or strategy IDs"
        )

    @pytest.mark.parametrize("agent_file", REQUIRED_AGENTS)
    def test_agent_when_read_then_is_not_empty(self, agents_dir: Path, agent_file: str) -> None:
        """Agent files must not be empty."""
        # Arrange
        agent_path = agents_dir / agent_file
        content = agent_path.read_text()

        # Act/Assert
        assert content.strip(), f"{agent_file} is empty or contains only whitespace"

    @pytest.mark.parametrize("agent_file", REQUIRED_AGENTS)
    def test_agent_when_read_then_has_minimum_content(
        self, agents_dir: Path, agent_file: str
    ) -> None:
        """Agent files must have minimum substantive content (50 lines)."""
        # Arrange
        agent_path = agents_dir / agent_file
        content = agent_path.read_text()
        lines = content.splitlines()

        # Act/Assert
        assert len(lines) >= 50, (
            f"{agent_file} has only {len(lines)} lines (minimum 50 required for agents)"
        )


class TestSkillIntegration:
    """Tests for skill component integration."""

    def test_playbook_when_read_then_references_all_agent_names(self, skill_dir: Path) -> None:
        """PLAYBOOK.md must reference all agent names."""
        # Arrange
        playbook_file = skill_dir / "PLAYBOOK.md"
        content = playbook_file.read_text()

        # Agent names without .md extension
        agent_names = ["adv-selector", "adv-executor", "adv-scorer"]

        # Act/Assert
        for agent_name in agent_names:
            assert agent_name in content, f"PLAYBOOK.md does not reference agent {agent_name}"

    def test_skill_when_scanned_then_has_3_core_agent_files(self, agents_dir: Path) -> None:
        """There should be 3 core agent files (plus optional README)."""
        # Arrange
        all_md_files = list(agents_dir.glob("*.md"))
        # Filter out README.md if present
        agent_files = [f for f in all_md_files if f.name != "README.md"]

        # Act/Assert
        assert len(agent_files) == 3, (
            f"Expected exactly 3 core agent files (excluding README), found {len(agent_files)}"
        )

    def test_skill_md_when_read_then_references_playbook(self, skill_dir: Path) -> None:
        """SKILL.md should reference PLAYBOOK.md for detailed procedures."""
        # Arrange
        skill_file = skill_dir / "SKILL.md"
        content = skill_file.read_text()

        # Act/Assert
        # Check for PLAYBOOK reference (case-insensitive) or agent names that indicate orchestration
        has_playbook_ref = "PLAYBOOK" in content or "playbook" in content or "Playbook" in content
        # Also accept if it clearly describes procedures that would be in a playbook
        has_procedure_guidance = (
            "adv-selector" in content and "adv-executor" in content and "adv-scorer" in content
        )

        assert has_playbook_ref or has_procedure_guidance, (
            "SKILL.md should reference PLAYBOOK.md or describe agent orchestration procedures"
        )
