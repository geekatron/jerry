"""
Architecture tests for adversarial strategy template structure.

These tests verify that:
1. All 10 strategy template files exist in .context/templates/adversarial/
2. TEMPLATE-FORMAT.md exists as the canonical format specification
3. Each template has required sections per TEMPLATE-FORMAT.md
4. Each template references its strategy ID correctly
5. Templates are substantive (minimum 100 lines each)

Test methodology: File existence and content inspection using pathlib.

References:
    - EN-928: Test Coverage Expansion
    - quality-enforcement.md: Strategy Catalog (10 selected strategies)
    - TEMPLATE-FORMAT.md v1.1.0: Section requirements
    - ADR-EPIC002-001: Strategy selection rationale
"""

from __future__ import annotations

from pathlib import Path

import pytest

# Mark as architecture tests
pytestmark = [
    pytest.mark.architecture,
]

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def project_root() -> Path:
    """Get the project root directory."""
    # Navigate from tests/architecture to project root
    return Path(__file__).parent.parent.parent


@pytest.fixture
def templates_dir(project_root: Path) -> Path:
    """Get the adversarial templates directory."""
    return project_root / ".context" / "templates" / "adversarial"


# =============================================================================
# Test Data
# =============================================================================

# The 10 selected strategies from quality-enforcement.md Strategy Catalog
SELECTED_STRATEGIES = [
    "s-001-red-team.md",
    "s-002-devils-advocate.md",
    "s-003-steelman.md",
    "s-004-pre-mortem.md",
    "s-007-constitutional-ai.md",
    "s-010-self-refine.md",
    "s-011-cove.md",
    "s-012-fmea.md",
    "s-013-inversion.md",
    "s-014-llm-as-judge.md",
]

# Required sections per TEMPLATE-FORMAT.md v1.1.0
# Templates use direct headers, not "Section N:" format
REQUIRED_SECTIONS = [
    "## Identity",
    "## Purpose",
    "## Prerequisites",
    "## Execution Protocol",
    "## Output Format",
    "## Scoring Rubric",
    "## Examples",
    "## Integration",
]

# Strategy ID to filename mapping
STRATEGY_ID_MAP = {
    "s-001-red-team.md": "S-001",
    "s-002-devils-advocate.md": "S-002",
    "s-003-steelman.md": "S-003",
    "s-004-pre-mortem.md": "S-004",
    "s-007-constitutional-ai.md": "S-007",
    "s-010-self-refine.md": "S-010",
    "s-011-cove.md": "S-011",
    "s-012-fmea.md": "S-012",
    "s-013-inversion.md": "S-013",
    "s-014-llm-as-judge.md": "S-014",
}


# =============================================================================
# Tests
# =============================================================================


class TestAdversarialTemplateFiles:
    """Tests for template file existence and basic structure."""

    def test_templates_directory_when_checked_then_exists(self, templates_dir: Path) -> None:
        """Templates directory must exist at expected location."""
        # Arrange/Act/Assert
        assert templates_dir.exists(), f"Templates directory does not exist: {templates_dir}"
        assert templates_dir.is_dir(), f"Templates path is not a directory: {templates_dir}"

    def test_template_format_when_checked_then_exists(self, templates_dir: Path) -> None:
        """TEMPLATE-FORMAT.md must exist as canonical format specification."""
        # Arrange
        format_file = templates_dir / "TEMPLATE-FORMAT.md"

        # Act/Assert
        assert format_file.exists(), f"TEMPLATE-FORMAT.md does not exist: {format_file}"
        assert format_file.is_file(), f"TEMPLATE-FORMAT.md is not a file: {format_file}"

    @pytest.mark.parametrize("template_file", SELECTED_STRATEGIES)
    def test_strategy_template_when_checked_then_exists(
        self, templates_dir: Path, template_file: str
    ) -> None:
        """Each of the 10 selected strategy templates must exist."""
        # Arrange
        template_path = templates_dir / template_file

        # Act/Assert
        assert template_path.exists(), f"Strategy template does not exist: {template_path}"
        assert template_path.is_file(), f"Strategy template is not a file: {template_path}"


class TestAdversarialTemplateContent:
    """Tests for template content structure and completeness."""

    @pytest.mark.parametrize("template_file", SELECTED_STRATEGIES)
    def test_template_when_read_then_has_required_sections(
        self, templates_dir: Path, template_file: str
    ) -> None:
        """Each template must have all 8 required sections per TEMPLATE-FORMAT.md."""
        # Arrange
        template_path = templates_dir / template_file
        content = template_path.read_text()

        # Section names (without "##" prefix)
        section_names = [
            "Identity",
            "Purpose",
            "Prerequisites",
            "Execution Protocol",
            "Output Format",
            "Scoring Rubric",
            "Examples",
            "Integration",
        ]

        # Act/Assert
        # Check for each section - accept either "## Identity" or "## Section 1: Identity" format
        for section_name in section_names:
            has_direct_format = f"## {section_name}" in content
            has_numbered_format = f": {section_name}" in content
            assert has_direct_format or has_numbered_format, (
                f"{template_file} missing required section: {section_name}"
            )

    @pytest.mark.parametrize("template_file", SELECTED_STRATEGIES)
    def test_template_when_read_then_references_correct_strategy_id(
        self, templates_dir: Path, template_file: str
    ) -> None:
        """Each template must reference its correct strategy ID."""
        # Arrange
        template_path = templates_dir / template_file
        content = template_path.read_text()
        expected_id = STRATEGY_ID_MAP[template_file]

        # Act/Assert
        assert expected_id in content, (
            f"{template_file} does not reference strategy ID {expected_id}"
        )

    @pytest.mark.parametrize("template_file", SELECTED_STRATEGIES)
    def test_template_when_read_then_is_substantive(
        self, templates_dir: Path, template_file: str
    ) -> None:
        """Each template must be substantive (minimum 100 lines)."""
        # Arrange
        template_path = templates_dir / template_file
        content = template_path.read_text()
        lines = content.splitlines()

        # Act/Assert
        assert len(lines) >= 100, (
            f"{template_file} has only {len(lines)} lines (minimum 100 required)"
        )

    @pytest.mark.parametrize("template_file", SELECTED_STRATEGIES)
    def test_template_when_read_then_is_not_empty(
        self, templates_dir: Path, template_file: str
    ) -> None:
        """Each template must not be empty."""
        # Arrange
        template_path = templates_dir / template_file
        content = template_path.read_text()

        # Act/Assert
        assert content.strip(), f"{template_file} is empty or contains only whitespace"


class TestTemplateFormatSpecification:
    """Tests for TEMPLATE-FORMAT.md content and structure."""

    def test_template_format_when_read_then_defines_required_sections(
        self, templates_dir: Path
    ) -> None:
        """TEMPLATE-FORMAT.md must define all 8 required sections."""
        # Arrange
        format_file = templates_dir / "TEMPLATE-FORMAT.md"
        content = format_file.read_text()

        # Section names (TEMPLATE-FORMAT.md uses "Section N: Name" format)
        section_names = [
            "Section 1: Identity",
            "Section 2: Purpose",
            "Section 3: Prerequisites",
            "Section 4: Execution Protocol",
            "Section 5: Output Format",
            "Section 6: Scoring Rubric",
            "Section 7: Examples",
            "Section 8: Integration",
        ]

        # Act/Assert
        for section_name in section_names:
            assert section_name in content, (
                f"TEMPLATE-FORMAT.md does not define required section: {section_name}"
            )

    def test_template_format_when_read_then_has_navigation_table(self, templates_dir: Path) -> None:
        """TEMPLATE-FORMAT.md must have navigation table per H-23."""
        # Arrange
        format_file = templates_dir / "TEMPLATE-FORMAT.md"
        content = format_file.read_text()

        # Act/Assert
        assert "## Document Sections" in content, (
            "TEMPLATE-FORMAT.md missing navigation table heading"
        )
        assert "| Section | Purpose |" in content, (
            "TEMPLATE-FORMAT.md missing navigation table structure"
        )

    def test_template_format_when_read_then_is_substantive(self, templates_dir: Path) -> None:
        """TEMPLATE-FORMAT.md must be substantive (minimum 100 lines)."""
        # Arrange
        format_file = templates_dir / "TEMPLATE-FORMAT.md"
        content = format_file.read_text()
        lines = content.splitlines()

        # Act/Assert
        assert len(lines) >= 100, (
            f"TEMPLATE-FORMAT.md has only {len(lines)} lines (minimum 100 required)"
        )


class TestTemplateCompleteness:
    """Tests for overall template coverage."""

    def test_templates_when_counted_then_all_10_selected_strategies_present(
        self, templates_dir: Path
    ) -> None:
        """All 10 selected strategies from quality-enforcement.md must have templates."""
        # Arrange
        existing_templates = [f.name for f in templates_dir.glob("s-*.md")]

        # Act/Assert
        for expected_template in SELECTED_STRATEGIES:
            assert expected_template in existing_templates, (
                f"Missing strategy template: {expected_template}"
            )

    def test_templates_when_counted_then_exactly_10_strategy_files(
        self, templates_dir: Path
    ) -> None:
        """There should be exactly 10 strategy templates (no extras)."""
        # Arrange
        strategy_templates = list(templates_dir.glob("s-*.md"))

        # Act/Assert
        assert len(strategy_templates) == 10, (
            f"Expected exactly 10 strategy templates, found {len(strategy_templates)}"
        )

    def test_templates_when_scanned_then_no_excluded_strategies(self, templates_dir: Path) -> None:
        """No excluded strategies should have templates."""
        # Arrange
        # Excluded strategies from quality-enforcement.md
        excluded_ids = ["s-005", "s-006", "s-008", "s-009", "s-015"]
        existing_templates = [f.name for f in templates_dir.glob("s-*.md")]

        # Act/Assert
        for excluded_id in excluded_ids:
            excluded_templates = [t for t in existing_templates if t.startswith(excluded_id)]
            assert not excluded_templates, (
                f"Found template for excluded strategy {excluded_id}: {excluded_templates}"
            )
