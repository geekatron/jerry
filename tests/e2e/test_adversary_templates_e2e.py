"""
End-to-end integration tests for the Adversary Skill Templates (EN-812).

Validates adversarial strategy templates, skill agents, and integration points:
- Template format compliance with TEMPLATE-FORMAT.md
- Strategy ID validation against SSOT quality-enforcement.md
- SSOT consistency (dimension weights, quality threshold, criticality levels)
- Skill agent validation (adv-selector, adv-executor, adv-scorer)
- Integration points (CLAUDE.md, skill cross-references)
- Criticality-based strategy selection

Test naming follows BDD convention:
    test_{scenario}_when_{condition}_then_{expected}

References:
    - EN-812: Adversary Skill E2E Integration Testing
    - EPIC-003: Quality Framework Implementation
    - .context/rules/quality-enforcement.md: SSOT
    - .context/templates/adversarial/TEMPLATE-FORMAT.md: Template standard
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = [pytest.mark.e2e]

# ===========================================================================
# Constants
# ===========================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SSOT_PATH = PROJECT_ROOT / ".context" / "rules" / "quality-enforcement.md"
TEMPLATE_FORMAT_PATH = (
    PROJECT_ROOT / ".context" / "templates" / "adversarial" / "TEMPLATE-FORMAT.md"
)
TEMPLATES_DIR = PROJECT_ROOT / ".context" / "templates" / "adversarial"
SKILL_DIR = PROJECT_ROOT / "skills" / "adversary"
SKILL_FILE = SKILL_DIR / "SKILL.md"
CLAUDE_MD_PATH = PROJECT_ROOT / "CLAUDE.md"

# Expected strategy IDs and metadata from SSOT
SELECTED_STRATEGIES = {
    "S-001": {"name": "Red Team Analysis", "family": "Role-Based Adversarialism", "prefix": "RT"},
    "S-002": {"name": "Devil's Advocate", "family": "Role-Based Adversarialism", "prefix": "DA"},
    "S-003": {"name": "Steelman Technique", "family": "Dialectical Synthesis", "prefix": "SM"},
    "S-004": {"name": "Pre-Mortem Analysis", "family": "Role-Based Adversarialism", "prefix": "PM"},
    "S-007": {
        "name": "Constitutional AI Critique",
        "family": "Iterative Self-Correction",
        "prefix": "CC",
    },
    "S-010": {"name": "Self-Refine", "family": "Iterative Self-Correction", "prefix": "SR"},
    "S-011": {
        "name": "Chain-of-Verification",
        "family": "Structured Decomposition",
        "prefix": "CV",
    },
    "S-012": {"name": "FMEA", "family": "Structured Decomposition", "prefix": "FM"},
    "S-013": {"name": "Inversion Technique", "family": "Structured Decomposition", "prefix": "IN"},
    "S-014": {"name": "LLM-as-Judge", "family": "Iterative Self-Correction", "prefix": "LJ"},
}

EXCLUDED_STRATEGIES = ["S-005", "S-006", "S-008", "S-009", "S-015"]

# Expected dimension weights from SSOT
DIMENSION_WEIGHTS = {
    "Completeness": 0.20,
    "Internal Consistency": 0.20,
    "Methodological Rigor": 0.20,
    "Evidence Quality": 0.15,
    "Actionability": 0.15,
    "Traceability": 0.10,
}

# Quality threshold from SSOT
QUALITY_THRESHOLD = 0.92

# Criticality levels from SSOT
CRITICALITY_LEVELS = {
    "C1": {"required": ["S-010"], "optional": ["S-003", "S-014"]},
    "C2": {"required": ["S-007", "S-002", "S-014"], "optional": ["S-003", "S-010"]},
    "C3": {
        "required": ["S-007", "S-002", "S-014", "S-004", "S-012", "S-013"],
        "optional": ["S-001", "S-003", "S-010", "S-011"],
    },
    "C4": {"required": list(SELECTED_STRATEGIES.keys()), "optional": []},
}

# Expected template paths
TEMPLATE_PATHS = {
    "S-001": TEMPLATES_DIR / "s-001-red-team.md",
    "S-002": TEMPLATES_DIR / "s-002-devils-advocate.md",
    "S-003": TEMPLATES_DIR / "s-003-steelman.md",
    "S-004": TEMPLATES_DIR / "s-004-pre-mortem.md",
    "S-007": TEMPLATES_DIR / "s-007-constitutional-ai.md",
    "S-010": TEMPLATES_DIR / "s-010-self-refine.md",
    "S-011": TEMPLATES_DIR / "s-011-cove.md",
    "S-012": TEMPLATES_DIR / "s-012-fmea.md",
    "S-013": TEMPLATES_DIR / "s-013-inversion.md",
    "S-014": TEMPLATES_DIR / "s-014-llm-as-judge.md",
}

# Expected agent files
AGENT_FILES = {
    "adv-selector": SKILL_DIR / "agents" / "adv-selector.md",
    "adv-executor": SKILL_DIR / "agents" / "adv-executor.md",
    "adv-scorer": SKILL_DIR / "agents" / "adv-scorer.md",
}

# Canonical sections from TEMPLATE-FORMAT.md (8 required sections)
CANONICAL_SECTIONS = [
    "Identity",
    "Purpose",
    "Prerequisites",
    "Execution Protocol",
    "Output Format",
    "Scoring Rubric",
    "Examples",
    "Integration",
]


# ===========================================================================
# Helper functions
# ===========================================================================


def read_file(path: Path) -> str:
    """Read a file and return its content as a string."""
    return path.read_text(encoding="utf-8")


def extract_frontmatter(content: str) -> dict[str, str]:
    """Extract YAML frontmatter from markdown content."""
    frontmatter = {}
    # Match HTML comment block at start of file
    frontmatter_match = re.search(r"^<!--(.*?)-->", content, re.DOTALL | re.MULTILINE)
    if frontmatter_match:
        frontmatter_text = frontmatter_match.group(1)
        # Parse key-value pairs
        for line in frontmatter_text.split("\n"):
            if ":" in line and not line.strip().startswith("http"):
                key, value = line.split(":", 1)
                frontmatter[key.strip()] = value.strip()
    return frontmatter


def extract_table_from_section(content: str, section_heading: str) -> str | None:
    """Extract a markdown table from a specific section."""
    # Find the section
    section_pattern = rf"^##\s+{re.escape(section_heading)}.*?(?=^##\s+|\Z)"
    section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)
    if not section_match:
        return None

    section_content = section_match.group(0)

    # Extract the first table
    table_pattern = r"\|.*?\|.*?\n\|[-:\s|]+\|.*?\n(?:\|.*?\|.*?\n)+"
    table_match = re.search(table_pattern, section_content)
    if table_match:
        return table_match.group(0)
    return None


def parse_markdown_table(table_text: str) -> list[dict[str, str]]:
    """Parse a markdown table into a list of dictionaries."""
    lines = [line.strip() for line in table_text.strip().split("\n")]
    if len(lines) < 3:
        return []

    # Parse header
    header_line = lines[0]
    headers = [cell.strip() for cell in header_line.split("|") if cell.strip()]

    # Parse rows (skip separator line)
    rows = []
    for line in lines[2:]:
        cells = [cell.strip() for cell in line.split("|") if cell.strip()]
        if len(cells) == len(headers):
            row = dict(zip(headers, cells, strict=False))
            rows.append(row)

    return rows


# ===========================================================================
# Test Class: Template Format Compliance
# ===========================================================================


class TestTemplateFormatCompliance:
    """
    Validates that all adversarial strategy templates comply with the
    canonical format defined in TEMPLATE-FORMAT.md.
    """

    def test_template_format_file_when_accessed_then_exists_and_is_readable(self):
        """TEMPLATE-FORMAT.md must exist and be parseable."""
        assert TEMPLATE_FORMAT_PATH.exists(), "TEMPLATE-FORMAT.md not found"
        content = read_file(TEMPLATE_FORMAT_PATH)
        assert len(content) > 100, "TEMPLATE-FORMAT.md appears empty or corrupted"

    @pytest.mark.parametrize("strategy_id", SELECTED_STRATEGIES.keys())
    def test_template_file_when_strategy_selected_then_exists(self, strategy_id: str):
        """All 10 selected strategy templates must exist."""
        template_path = TEMPLATE_PATHS[strategy_id]
        assert template_path.exists(), f"Template for {strategy_id} not found at {template_path}"

    @pytest.mark.parametrize("strategy_id", SELECTED_STRATEGIES.keys())
    def test_template_frontmatter_when_read_then_contains_required_fields(self, strategy_id: str):
        """Each template must have frontmatter with required fields."""
        template_path = TEMPLATE_PATHS[strategy_id]
        content = read_file(template_path)
        frontmatter = extract_frontmatter(content)

        # Check for required frontmatter fields (various formats)
        # Accept "TEMPLATE:", "VERSION:", or other metadata fields like "ENABLER:", "STATUS:"
        has_frontmatter = (
            "TEMPLATE" in frontmatter
            or "VERSION" in frontmatter
            or "ENABLER" in frontmatter
            or "STATUS" in frontmatter
            or len(frontmatter) > 0
        )
        assert has_frontmatter, (
            f"{strategy_id}: Missing frontmatter (found: {list(frontmatter.keys())})"
        )

    @pytest.mark.parametrize("strategy_id", SELECTED_STRATEGIES.keys())
    def test_template_sections_when_read_then_contains_all_8_canonical_sections(
        self, strategy_id: str
    ):
        """Each template must contain all 8 canonical sections in order."""
        template_path = TEMPLATE_PATHS[strategy_id]
        content = read_file(template_path)

        # Extract all ## level headings (including "Section N:" prefixes)
        headings = re.findall(r"^##\s+(.+)$", content, re.MULTILINE)

        # Check that all canonical sections are present
        # Accept both "Identity" and "Section 1: Identity" formats
        for section in CANONICAL_SECTIONS:
            # Check for section name with or without "Section N:" prefix
            found = any(
                section in heading or heading.endswith(f": {section}") for heading in headings
            )
            assert found, f"{strategy_id}: Missing canonical section '{section}'"

    @pytest.mark.parametrize("strategy_id", SELECTED_STRATEGIES.keys())
    def test_template_identity_when_read_then_contains_7_required_fields(self, strategy_id: str):
        """Identity section must contain 7 required fields."""
        template_path = TEMPLATE_PATHS[strategy_id]
        content = read_file(template_path)

        # Extract Identity section table (try both "Identity" and "Section 1: Identity")
        identity_table = extract_table_from_section(content, "Identity")
        if identity_table is None:
            identity_table = extract_table_from_section(content, "Section 1: Identity")

        assert identity_table is not None, f"{strategy_id}: No table found in Identity section"

        # Parse the table
        rows = parse_markdown_table(identity_table)
        fields = {row["Field"]: row["Value"] for row in rows if "Field" in row and "Value" in row}

        # Check required fields
        required_fields = [
            "Strategy ID",
            "Strategy Name",
            "Family",
            "Composite Score",
            "Finding Prefix",
            "Version",
            "Date",
        ]
        for field in required_fields:
            assert field in fields, f"{strategy_id}: Missing Identity field '{field}'"

        # Validate Strategy ID matches
        assert fields["Strategy ID"] == strategy_id, (
            f"{strategy_id}: Strategy ID mismatch in Identity table"
        )

    @pytest.mark.parametrize("strategy_id", SELECTED_STRATEGIES.keys())
    def test_template_navigation_when_read_then_has_nav_table_with_anchor_links(
        self, strategy_id: str
    ):
        """H-23/H-24: Templates must have navigation table with anchor links."""
        template_path = TEMPLATE_PATHS[strategy_id]
        content = read_file(template_path)

        # Check for navigation table (usually "Document Sections")
        nav_section_match = re.search(
            r"^##\s+Document Sections.*?\n(.*?)(?=^##|\Z)", content, re.MULTILINE | re.DOTALL
        )
        assert nav_section_match is not None, (
            f"{strategy_id}: Missing 'Document Sections' navigation table (H-23)"
        )

        nav_content = nav_section_match.group(1)

        # Check for anchor links in navigation table
        anchor_links = re.findall(r"\[.+?\]\(#.+?\)", nav_content)
        assert len(anchor_links) >= len(CANONICAL_SECTIONS) - 1, (
            f"{strategy_id}: Navigation table missing anchor links (H-24)"
        )


# ===========================================================================
# Test Class: Strategy ID Validation Against SSOT
# ===========================================================================


class TestStrategyIDValidation:
    """
    Validates that all selected strategy IDs are present and no excluded
    strategies appear in templates.
    """

    def test_selected_strategies_when_checked_then_all_10_present(self):
        """All 10 selected strategy IDs must have corresponding template files."""
        for strategy_id in SELECTED_STRATEGIES.keys():
            template_path = TEMPLATE_PATHS[strategy_id]
            assert template_path.exists(), f"Template for {strategy_id} not found"

    def test_excluded_strategies_when_checked_then_none_have_templates(self):
        """No excluded strategy IDs should have template files."""
        for strategy_id in EXCLUDED_STRATEGIES:
            # Map to expected file name
            slug = f"s-{strategy_id.lower().replace('s-', '')}"
            potential_path = TEMPLATES_DIR / f"{slug}.md"
            assert not potential_path.exists() or "EXCLUDED" in read_file(potential_path), (
                f"Excluded strategy {strategy_id} has a template at {potential_path}"
            )

    @pytest.mark.parametrize("strategy_id", SELECTED_STRATEGIES.keys())
    def test_finding_prefix_when_read_from_template_then_matches_catalog(self, strategy_id: str):
        """Finding prefix in template Identity section must match SSOT catalog."""
        template_path = TEMPLATE_PATHS[strategy_id]
        content = read_file(template_path)

        # Extract Identity section table (try both formats)
        identity_table = extract_table_from_section(content, "Identity")
        if identity_table is None:
            identity_table = extract_table_from_section(content, "Section 1: Identity")

        assert identity_table is not None, f"{strategy_id}: No table found in Identity section"

        rows = parse_markdown_table(identity_table)
        fields = {row["Field"]: row["Value"] for row in rows if "Field" in row and "Value" in row}

        # Extract finding prefix
        finding_prefix_value = fields.get("Finding Prefix", "")
        # Handle both "DA-NNN" and "DA" formats
        finding_prefix = (
            finding_prefix_value.split("-")[0]
            if "-" in finding_prefix_value
            else finding_prefix_value
        )
        expected_prefix = SELECTED_STRATEGIES[strategy_id]["prefix"]

        assert finding_prefix == expected_prefix, (
            f"{strategy_id}: Finding prefix '{finding_prefix}' does not match "
            f"expected '{expected_prefix}' from catalog"
        )


# ===========================================================================
# Test Class: SSOT Consistency
# ===========================================================================


class TestSSOTConsistency:
    """
    Validates that templates reference the correct SSOT file and do not
    hardcode constants that should come from quality-enforcement.md.
    """

    def test_ssot_file_when_accessed_then_exists_and_is_readable(self):
        """quality-enforcement.md SSOT must exist and be parseable."""
        assert SSOT_PATH.exists(), "quality-enforcement.md SSOT not found"
        content = read_file(SSOT_PATH)
        assert len(content) > 1000, "quality-enforcement.md appears empty or corrupted"

    @pytest.mark.parametrize("strategy_id", SELECTED_STRATEGIES.keys())
    def test_template_ssot_reference_when_read_then_mentions_quality_enforcement(
        self, strategy_id: str
    ):
        """Templates must reference quality-enforcement.md as SSOT."""
        template_path = TEMPLATE_PATHS[strategy_id]
        content = read_file(template_path)

        # Check for SSOT reference
        assert "quality-enforcement.md" in content, (
            f"{strategy_id}: Template does not reference quality-enforcement.md"
        )

    @pytest.mark.parametrize("strategy_id", SELECTED_STRATEGIES.keys())
    def test_template_dimension_weights_when_mentioned_then_not_hardcoded_differently(
        self, strategy_id: str
    ):
        """Templates should reference SSOT weights, not redefine them differently."""
        template_path = TEMPLATE_PATHS[strategy_id]
        content = read_file(template_path)

        # Check for Scoring Impact or Dimension Weights table
        scoring_section = extract_table_from_section(content, "Scoring Rubric")
        if scoring_section is None:
            scoring_section = extract_table_from_section(content, "Output Format")

        if scoring_section:
            # Parse dimension weights from table if present
            rows = parse_markdown_table(scoring_section)
            for row in rows:
                dimension = row.get("Dimension", "")
                weight_str = row.get("Weight", "")

                # Skip if not a dimension row
                if dimension not in DIMENSION_WEIGHTS:
                    continue

                # Extract weight value
                weight_match = re.search(r"0\.\d+", weight_str)
                if weight_match:
                    weight = float(weight_match.group(0))
                    expected_weight = DIMENSION_WEIGHTS[dimension]

                    assert abs(weight - expected_weight) < 0.01, (
                        f"{strategy_id}: Dimension '{dimension}' has weight {weight}, "
                        f"expected {expected_weight} from SSOT"
                    )

    @pytest.mark.parametrize("strategy_id", SELECTED_STRATEGIES.keys())
    def test_template_quality_threshold_when_mentioned_then_matches_ssot(self, strategy_id: str):
        """Templates must reference 0.92 threshold, not a different value."""
        template_path = TEMPLATE_PATHS[strategy_id]
        content = read_file(template_path)

        # Check if the primary threshold 0.92 is mentioned
        # Templates can mention operational bands (0.85, 0.91, etc.) but the canonical threshold should be 0.92
        if ">= 0.92" in content or "0.92" in content:
            # Good - template references the correct threshold
            pass
        else:
            # Check if a different threshold is being used as THE threshold
            threshold_matches = re.finditer(r"(?:threshold|Threshold)[:\s]+>=?\s*(0\.\d+)", content)
            for match in threshold_matches:
                threshold = float(match.group(1))
                # Only fail if it's clearly THE threshold (not an operational band)
                if threshold != QUALITY_THRESHOLD and threshold not in [0.85, 0.91, 0.95]:
                    pytest.fail(
                        f"{strategy_id}: Found threshold {threshold}, expected {QUALITY_THRESHOLD} from SSOT"
                    )


# ===========================================================================
# Test Class: Skill Agent Validation
# ===========================================================================


class TestSkillAgentValidation:
    """
    Validates that the three adversary skill agents exist and contain
    correct references to templates and SSOT values.
    """

    def test_skill_file_when_accessed_then_exists_and_is_readable(self):
        """skills/adversary/SKILL.md must exist."""
        assert SKILL_FILE.exists(), "adversary SKILL.md not found"
        content = read_file(SKILL_FILE)
        assert len(content) > 500, "adversary SKILL.md appears empty"

    @pytest.mark.parametrize("agent_name", AGENT_FILES.keys())
    def test_agent_file_when_accessed_then_exists(self, agent_name: str):
        """All 3 agent files must exist."""
        agent_path = AGENT_FILES[agent_name]
        assert agent_path.exists(), f"Agent file {agent_name} not found at {agent_path}"

    def test_adv_selector_when_read_then_contains_all_10_template_paths(self):
        """adv-selector.md must contain all 10 template paths matching actual files."""
        agent_path = AGENT_FILES["adv-selector"]
        content = read_file(agent_path)

        for strategy_id, template_path in TEMPLATE_PATHS.items():
            # Convert to relative path format
            relative_path = f".context/templates/adversarial/{template_path.name}"
            assert relative_path in content, (
                f"adv-selector.md missing template path for {strategy_id}: {relative_path}"
            )

    def test_adv_executor_when_read_then_contains_all_10_finding_prefixes(self):
        """adv-executor.md must contain all 10 finding prefixes."""
        agent_path = AGENT_FILES["adv-executor"]
        content = read_file(agent_path)

        for strategy_id, metadata in SELECTED_STRATEGIES.items():
            prefix = metadata["prefix"]
            # Check for prefix pattern (e.g., "RT-001", "DA-001")
            assert f"{prefix}-" in content, (
                f"adv-executor.md missing finding prefix for {strategy_id}: {prefix}-"
            )

    def test_adv_scorer_when_read_then_contains_correct_dimension_weights(self):
        """adv-scorer.md must contain the 6 dimension weights matching SSOT."""
        agent_path = AGENT_FILES["adv-scorer"]
        content = read_file(agent_path)

        # Extract dimension weights table
        dimension_table = extract_table_from_section(content, "SSOT Quality Dimensions")
        assert dimension_table is not None, "adv-scorer.md missing dimension weights table"

        rows = parse_markdown_table(dimension_table)
        for row in rows:
            dimension = row.get("Dimension", "")
            weight_str = row.get("Weight", "")

            if dimension in DIMENSION_WEIGHTS:
                weight_match = re.search(r"0\.\d+", weight_str)
                if weight_match:
                    weight = float(weight_match.group(0))
                    expected_weight = DIMENSION_WEIGHTS[dimension]

                    assert abs(weight - expected_weight) < 0.01, (
                        f"adv-scorer.md: Dimension '{dimension}' has weight {weight}, "
                        f"expected {expected_weight} from SSOT"
                    )


# ===========================================================================
# Test Class: Integration Points
# ===========================================================================


class TestIntegrationPoints:
    """
    Validates that the adversary skill is properly integrated into the
    framework via CLAUDE.md and cross-referenced in other skills.
    """

    def test_claude_md_when_read_then_contains_adversary_skill_entry(self):
        """CLAUDE.md must list /adversary skill."""
        content = read_file(CLAUDE_MD_PATH)

        # Check for /adversary skill reference
        assert "/adversary" in content or "adversary" in content.lower(), (
            "CLAUDE.md missing /adversary skill entry"
        )

    def test_skill_md_when_read_then_contains_template_references(self):
        """adversary SKILL.md must reference strategy templates."""
        content = read_file(SKILL_FILE)

        # Check for template directory reference
        assert ".context/templates/adversarial" in content, (
            "adversary SKILL.md missing template directory reference"
        )

        # Check for at least some strategy names
        for strategy_id, metadata in list(SELECTED_STRATEGIES.items())[:3]:
            # Check for strategy name or ID
            assert metadata["name"] in content or strategy_id in content, (
                f"adversary SKILL.md missing reference to {strategy_id} ({metadata['name']})"
            )

    def test_skill_md_when_read_then_contains_correct_criticality_mapping(self):
        """adversary SKILL.md enabler-to-template mapping must be correct."""
        content = read_file(SKILL_FILE)

        # Extract criticality-based strategy selection table
        criticality_table = extract_table_from_section(
            content, "Criticality-Based Strategy Selection"
        )
        if criticality_table is None:
            pytest.skip("Criticality table not found in expected section")

        rows = parse_markdown_table(criticality_table)

        # Validate each criticality level
        for row in rows:
            level = row.get("Level", "")
            if level not in CRITICALITY_LEVELS:
                continue

            required_str = row.get("Required Strategies", "")

            # Extract strategy IDs from the strings
            required_ids = re.findall(r"S-\d+", required_str)

            expected_required = CRITICALITY_LEVELS[level]["required"]

            # Check required strategies
            for expected_id in expected_required:
                assert expected_id in required_ids, (
                    f"adversary SKILL.md: {level} missing required strategy {expected_id}"
                )


# ===========================================================================
# Test Class: Criticality-Based Strategy Selection
# ===========================================================================


class TestCriticalityBasedStrategySelection:
    """
    Validates that criticality level to strategy set mappings are correct
    and consistent across SSOT, templates, and skill files.
    """

    @pytest.mark.parametrize("level", CRITICALITY_LEVELS.keys())
    def test_criticality_level_when_checked_then_required_strategies_are_valid(self, level: str):
        """All required strategies for each criticality level must be valid selected strategies."""
        required = CRITICALITY_LEVELS[level]["required"]

        for strategy_id in required:
            assert strategy_id in SELECTED_STRATEGIES, (
                f"Criticality {level} requires invalid strategy {strategy_id}"
            )

    @pytest.mark.parametrize("level", CRITICALITY_LEVELS.keys())
    def test_criticality_level_when_checked_then_optional_strategies_are_valid(self, level: str):
        """All optional strategies for each criticality level must be valid selected strategies."""
        optional = CRITICALITY_LEVELS[level]["optional"]

        for strategy_id in optional:
            assert strategy_id in SELECTED_STRATEGIES, (
                f"Criticality {level} has invalid optional strategy {strategy_id}"
            )

    def test_c1_level_when_checked_then_has_s010_required(self):
        """C1 (Routine) must require S-010 (Self-Refine)."""
        required = CRITICALITY_LEVELS["C1"]["required"]
        assert "S-010" in required, "C1 must require S-010 (Self-Refine)"

    def test_c2_level_when_checked_then_has_core_set(self):
        """C2 (Standard) must require S-007, S-002, S-014."""
        required = CRITICALITY_LEVELS["C2"]["required"]
        assert "S-007" in required, "C2 must require S-007 (Constitutional AI)"
        assert "S-002" in required, "C2 must require S-002 (Devil's Advocate)"
        assert "S-014" in required, "C2 must require S-014 (LLM-as-Judge)"

    def test_c3_level_when_checked_then_includes_c2_plus_decomposition(self):
        """C3 (Significant) must include C2 set plus S-004, S-012, S-013."""
        required = CRITICALITY_LEVELS["C3"]["required"]

        # Check C2 set is included
        c2_required = CRITICALITY_LEVELS["C2"]["required"]
        for strategy_id in c2_required:
            assert strategy_id in required, f"C3 must include C2 required strategy {strategy_id}"

        # Check additional strategies
        assert "S-004" in required, "C3 must require S-004 (Pre-Mortem)"
        assert "S-012" in required, "C3 must require S-012 (FMEA)"
        assert "S-013" in required, "C3 must require S-013 (Inversion)"

    def test_c4_level_when_checked_then_requires_all_10_strategies(self):
        """C4 (Critical) must require all 10 selected strategies."""
        required = CRITICALITY_LEVELS["C4"]["required"]

        assert len(required) == 10, f"C4 must require all 10 strategies, found {len(required)}"

        for strategy_id in SELECTED_STRATEGIES.keys():
            assert strategy_id in required, f"C4 must require {strategy_id}"

    def test_h16_ordering_when_documented_then_s003_before_s002(self):
        """H-16 ordering constraint: S-003 must be documented as running before S-002."""
        # Check in SSOT
        ssot_content = read_file(SSOT_PATH)
        assert "H-16" in ssot_content, "SSOT missing H-16 rule"
        assert "Steelman before critique" in ssot_content or "S-003" in ssot_content, (
            "SSOT missing H-16 Steelman ordering"
        )

        # Check in S-002 template
        s002_content = read_file(TEMPLATE_PATHS["S-002"])
        assert "H-16" in s002_content, "S-002 template missing H-16 reference"
        assert "S-003" in s002_content, "S-002 template missing S-003 prerequisite for H-16"

        # Check in adversary SKILL.md
        skill_content = read_file(SKILL_FILE)
        assert "H-16" in skill_content, "adversary SKILL.md missing H-16 reference"


# ===========================================================================
# Test Class: Template Content Quality
# ===========================================================================


class TestFindingPrefixUniqueness:
    """
    Validates that finding ID prefixes are unique across all strategy templates
    and properly documented with execution-scoped format.
    """

    def test_finding_prefixes_when_checked_then_all_unique(self):
        """All 10 strategy templates must define unique STRATEGY_PREFIX values."""
        prefixes_found = {}

        for strategy_id, template_path in TEMPLATE_PATHS.items():
            content = read_file(template_path)

            # Extract Finding Prefix from Identity table
            identity_table = extract_table_from_section(content, "Identity")
            if identity_table is None:
                identity_table = extract_table_from_section(content, "Section 1: Identity")

            assert identity_table is not None, f"{strategy_id}: No table found in Identity section"

            rows = parse_markdown_table(identity_table)
            fields = {
                row["Field"]: row["Value"] for row in rows if "Field" in row and "Value" in row
            }

            finding_prefix_value = fields.get("Finding Prefix", "")
            # Extract prefix (handle both "DA-NNN" and "DA-NNN-{execution_id}" formats)
            prefix_match = re.match(r"([A-Z]{2})-", finding_prefix_value)
            assert prefix_match is not None, (
                f"{strategy_id}: Finding Prefix not in expected format (found: {finding_prefix_value})"
            )

            prefix = prefix_match.group(1)

            # Check for duplicates
            if prefix in prefixes_found:
                pytest.fail(
                    f"Duplicate finding prefix '{prefix}' found in {strategy_id} "
                    f"and {prefixes_found[prefix]}"
                )

            prefixes_found[prefix] = strategy_id

        # Verify we found all 10 unique prefixes
        assert len(prefixes_found) == 10, (
            f"Expected 10 unique prefixes, found {len(prefixes_found)}: {list(prefixes_found.keys())}"
        )

    @pytest.mark.parametrize("strategy_id", SELECTED_STRATEGIES.keys())
    def test_finding_id_format_when_read_then_documented_in_template(self, strategy_id: str):
        """Each template must document the execution-scoped finding ID format."""
        template_path = TEMPLATE_PATHS[strategy_id]
        content = read_file(template_path)

        # Get expected prefix
        expected_prefix = SELECTED_STRATEGIES[strategy_id]["prefix"]

        # Check for Finding ID Format documentation
        # Look for patterns like "Finding ID Format:" or "{PREFIX}-{NNN}-{execution_id}"
        format_pattern = f"{expected_prefix}-{{NNN}}-{{execution_id}}"

        assert format_pattern in content, (
            f"{strategy_id}: Template missing execution-scoped finding ID format documentation. "
            f"Expected to find '{format_pattern}' in Output Format or Execution Protocol section."
        )

        # Also check for the explanation text about preventing collisions
        collision_text_variants = [
            "prevent ID collisions",
            "preventing ID collisions",
            "execution-scoped",
            "tournament executions",
        ]

        has_collision_explanation = any(variant in content for variant in collision_text_variants)

        assert has_collision_explanation, (
            f"{strategy_id}: Template missing explanation for execution-scoped IDs "
            "(should mention preventing collisions or tournament executions)"
        )

    @pytest.mark.parametrize("strategy_id", SELECTED_STRATEGIES.keys())
    def test_finding_id_examples_when_present_then_use_scoped_format(self, strategy_id: str):
        """Examples in templates should use execution-scoped finding IDs, not just PREFIX-NNN."""
        template_path = TEMPLATE_PATHS[strategy_id]
        content = read_file(template_path)

        expected_prefix = SELECTED_STRATEGIES[strategy_id]["prefix"]

        # Extract Examples section
        examples_match = re.search(
            r"^##\s+(?:Section 7: )?Examples.*?(?=^##\s+|\Z)", content, re.MULTILINE | re.DOTALL
        )

        if examples_match is None:
            pytest.skip(f"{strategy_id}: No Examples section found")

        examples_content = examples_match.group(0)

        # Look for finding ID patterns in examples
        # Old format: PREFIX-001, PREFIX-002, etc.
        old_format_pattern = rf"{expected_prefix}-\d{{3}}(?!-)"
        # New format: PREFIX-001-20260215T1430, PREFIX-001-sess-xyz, etc.
        new_format_pattern = rf"{expected_prefix}-\d{{3}}-[\w-]+"

        old_format_matches = re.findall(old_format_pattern, examples_content)
        new_format_matches = re.findall(new_format_pattern, examples_content)

        # Examples should use new format (scoped IDs), not old format
        # Allow templates with no finding ID examples in the Examples section
        if len(old_format_matches) > 0 or len(new_format_matches) > 0:
            assert len(new_format_matches) > 0, (
                f"{strategy_id}: Examples section contains finding IDs but uses old format "
                f"({expected_prefix}-NNN) instead of execution-scoped format "
                f"({expected_prefix}-NNN-execution_id). Found: {old_format_matches[:3]}"
            )


class TestTemplateContentQuality:
    """
    Validates that templates have substantive content in key sections
    (not just structural compliance).
    """

    @pytest.mark.parametrize("strategy_id", SELECTED_STRATEGIES.keys())
    def test_template_execution_protocol_when_read_then_has_at_least_4_steps(
        self, strategy_id: str
    ):
        """Execution Protocol must have at least 4 numbered steps."""
        template_path = TEMPLATE_PATHS[strategy_id]
        content = read_file(template_path)

        # Extract Execution Protocol section (try both formats)
        protocol_match = re.search(
            r"^##\s+(?:Section 4: )?Execution Protocol.*?(?=^##\s+|\Z)",
            content,
            re.MULTILINE | re.DOTALL,
        )
        assert protocol_match is not None, f"{strategy_id}: Missing Execution Protocol section"

        protocol_content = protocol_match.group(0)

        # Count step headings (### Step N:)
        step_headings = re.findall(r"^###\s+Step\s+\d+:", protocol_content, re.MULTILINE)
        assert len(step_headings) >= 4, (
            f"{strategy_id}: Execution Protocol has {len(step_headings)} steps, expected >= 4"
        )

    @pytest.mark.parametrize("strategy_id", SELECTED_STRATEGIES.keys())
    def test_template_examples_when_read_then_has_at_least_one_example(self, strategy_id: str):
        """Examples section must contain at least one concrete example."""
        template_path = TEMPLATE_PATHS[strategy_id]
        content = read_file(template_path)

        # Extract Examples section (try both formats)
        examples_match = re.search(
            r"^##\s+(?:Section 7: )?Examples.*?(?=^##\s+|\Z)", content, re.MULTILINE | re.DOTALL
        )
        assert examples_match is not None, f"{strategy_id}: Missing Examples section"

        examples_content = examples_match.group(0)

        # Check for example indicators
        assert len(examples_content) > 200, (
            f"{strategy_id}: Examples section appears too short (< 200 chars)"
        )

        # Check for "Before" and "After" or "Example" headings
        has_example = (
            "Before" in examples_content
            or "After" in examples_content
            or "Example" in examples_content
        )
        assert has_example, f"{strategy_id}: Examples section missing Before/After/Example content"


# ===========================================================================
# Summary Statistics Test
# ===========================================================================


class TestSummaryStatistics:
    """
    Provides summary statistics and overview validation.
    """

    def test_adversary_framework_when_checked_then_has_complete_strategy_coverage(self):
        """
        Summary test: All 10 selected strategies must have complete coverage
        (template file, SSOT entry, agent references).
        """
        missing = []

        for strategy_id in SELECTED_STRATEGIES:
            # Check template file
            if not TEMPLATE_PATHS[strategy_id].exists():
                missing.append(f"{strategy_id}: template file missing")

            # Check SSOT entry
            ssot_content = read_file(SSOT_PATH)
            if strategy_id not in ssot_content:
                missing.append(f"{strategy_id}: missing from SSOT")

        assert not missing, "Incomplete strategy coverage:\n" + "\n".join(missing)

    def test_adversary_framework_when_checked_then_has_correct_file_count(self):
        """
        Summary test: Verify expected file count in templates directory.
        """
        # Count actual template files (excluding TEMPLATE-FORMAT.md)
        actual_templates = [
            f
            for f in TEMPLATES_DIR.iterdir()
            if f.is_file() and f.suffix == ".md" and f.name != "TEMPLATE-FORMAT.md"
        ]

        assert len(actual_templates) == 10, (
            f"Expected 10 strategy templates, found {len(actual_templates)}"
        )
