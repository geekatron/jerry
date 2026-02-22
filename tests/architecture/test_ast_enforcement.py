# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Architecture tests for H-33 AST-based parsing enforcement artifacts.

These tests verify that:
1. H-33 is registered in quality-enforcement.md HARD Rule Index
2. L2-REINJECT rank=10 marker exists for per-prompt reinforcement
3. All wt-* agents declare Bash in allowed_tools (tool gap closed)
4. All wt-* agents use REQUIRED/MUST language, not PREFERRED (language gap closed)
5. All wt-* agent examples use --directory ${CLAUDE_PLUGIN_ROOT} prefix
6. /ast is registered in CLAUDE.md Quick Reference (registration gap closed)
7. /ast triggers exist in mandatory-skill-usage.md (trigger gap closed)
8. AGENTS.md includes AST enforcement note for worktracker section
9. /ast skill source artifacts exist (SKILL.md, ast_ops.py)
10. No forbidden anti-patterns (regex frontmatter grep) in agent files

Test methodology: File content inspection using pathlib, validating governance
artifacts that constitute system behavior for LLM agents.

References:
    - H-33: AST-based parsing REQUIRED for worktracker entity ops
    - H-30: Register in CLAUDE.md + AGENTS.md + mandatory-skill-usage.md
    - quality-enforcement.md: HARD Rule Index, L2-REINJECT markers
    - AE-002: .context/rules/ changes auto-escalate to C3
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

# Mark as architecture tests
pytestmark = [
    pytest.mark.architecture,
]

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="session")
def project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent


@pytest.fixture(scope="session")
def rules_dir(project_root: Path) -> Path:
    """Get the .context/rules/ directory."""
    return project_root / ".context" / "rules"


@pytest.fixture(scope="session")
def quality_enforcement_content(rules_dir: Path) -> str:
    """Read quality-enforcement.md content."""
    return (rules_dir / "quality-enforcement.md").read_text()


@pytest.fixture(scope="session")
def mandatory_skill_content(rules_dir: Path) -> str:
    """Read mandatory-skill-usage.md content."""
    return (rules_dir / "mandatory-skill-usage.md").read_text()


@pytest.fixture(scope="session")
def claude_md_content(project_root: Path) -> str:
    """Read CLAUDE.md content."""
    return (project_root / "CLAUDE.md").read_text()


@pytest.fixture(scope="session")
def agents_md_content(project_root: Path) -> str:
    """Read AGENTS.md content."""
    return (project_root / "AGENTS.md").read_text()


@pytest.fixture(scope="session")
def wt_agents_dir(project_root: Path) -> Path:
    """Get the worktracker agents directory."""
    return project_root / "skills" / "worktracker" / "agents"


@pytest.fixture(scope="session")
def discovered_wt_agents(wt_agents_dir: Path) -> list[str]:
    """Dynamically discover all wt-* agent files."""
    return sorted(f.name for f in wt_agents_dir.glob("wt-*.md"))


# =============================================================================
# Test Data
# =============================================================================

# Expected worktracker agent files (validated against dynamic discovery)
EXPECTED_WT_AGENT_FILES = [
    "wt-auditor.md",
    "wt-verifier.md",
    "wt-visualizer.md",
]

# MEDIUM-tier words that must NOT appear in AST operations sections
PROHIBITED_MEDIUM_TIER_WORDS = [
    "PREFERRED",
    "SHOULD",
    "RECOMMENDED",
]

# Anti-patterns: regex-based frontmatter extraction that H-33 prohibits
FORBIDDEN_ANTI_PATTERNS = [
    # Specific known fields
    r'Grep\(pattern=["\']>\s*\*\*Status:',
    r"grep.*> \*\*Status:",
    r'Grep\(pattern=["\']>\s*\*\*Type:',
    r'Grep\(pattern=["\']>\s*\*\*Parent:',
    # Generic: any Grep targeting blockquote frontmatter pattern (> **Field:**)
    r'Grep\(pattern=["\']>\s*\\\*\\\*\w+:',
]


# =============================================================================
# Tests: Agent Discovery Integrity
# =============================================================================


class TestWorktrackerAgentDiscovery:
    """Tests for wt-* agent file discovery and expected set alignment."""

    def test_discovered_agents_when_checked_then_matches_expected_set(
        self, discovered_wt_agents: list[str]
    ) -> None:
        """Discovered wt-* agents must match the expected set exactly."""
        # Arrange
        expected = sorted(EXPECTED_WT_AGENT_FILES)

        # Act/Assert
        assert discovered_wt_agents == expected, (
            f"Agent set mismatch. Expected: {expected}, "
            f"Discovered: {discovered_wt_agents}. "
            f"Update EXPECTED_WT_AGENT_FILES if a new wt-* agent was added."
        )

    def test_discovered_agents_when_checked_then_at_least_three_exist(
        self, discovered_wt_agents: list[str]
    ) -> None:
        """There must be at least 3 wt-* agent files."""
        # Arrange/Act/Assert
        assert len(discovered_wt_agents) >= 3, (
            f"Expected at least 3 wt-* agents, found {len(discovered_wt_agents)}: "
            f"{discovered_wt_agents}"
        )


# =============================================================================
# Tests: H-33 Rule Registration (quality-enforcement.md)
# =============================================================================


class TestH31RuleRegistration:
    """Tests for H-33 registration in quality-enforcement.md HARD Rule Index."""

    def test_hard_rule_index_when_checked_then_contains_h31(
        self, quality_enforcement_content: str
    ) -> None:
        """H-33 must appear in the HARD Rule Index table."""
        # Arrange
        pattern = r"\|\s*H-33\s*\|.*AST.*\|.*ast-enforcement\s*\|"

        # Act/Assert
        assert re.search(pattern, quality_enforcement_content), (
            "H-33 not found in quality-enforcement.md HARD Rule Index table"
        )

    def test_hard_rule_index_when_checked_then_header_references_h31(
        self, quality_enforcement_content: str
    ) -> None:
        """Section header must reference H-33 range (H-01 through H-33)."""
        # Arrange/Act/Assert
        assert "H-01 through H-33" in quality_enforcement_content, (
            "quality-enforcement.md section header does not reference 'H-01 through H-33'"
        )

    def test_l2_reinject_when_checked_then_rank9_exists(
        self, quality_enforcement_content: str
    ) -> None:
        """L2-REINJECT rank=10 marker must exist for per-prompt AST reinforcement."""
        # Arrange
        pattern = r"<!--\s*L2-REINJECT:\s*rank=10.*H-33.*-->"

        # Act/Assert
        assert re.search(pattern, quality_enforcement_content, re.DOTALL), (
            "L2-REINJECT rank=10 marker for H-33 not found in quality-enforcement.md"
        )

    def test_l2_reinject_when_checked_then_rank9_prohibits_regex(
        self, quality_enforcement_content: str
    ) -> None:
        """L2-REINJECT rank=10 must include 'NEVER use regex' reinforcement."""
        # Arrange
        pattern = r"rank=10.*NEVER use regex"

        # Act/Assert
        assert re.search(pattern, quality_enforcement_content, re.DOTALL), (
            "L2-REINJECT rank=10 does not contain 'NEVER use regex' reinforcement"
        )

    def test_l2_reinject_when_checked_then_rank9_references_ast_commands(
        self, quality_enforcement_content: str
    ) -> None:
        """L2-REINJECT rank=10 must reference jerry ast CLI commands within the same directive."""
        # Arrange — match within a single HTML comment to ensure both commands
        # are in the same L2-REINJECT directive, not scattered across separate markers
        pattern = r"<!--[^>]*rank=10[^>]*jerry ast frontmatter[^>]*jerry ast validate[^>]*-->"

        # Act/Assert
        assert re.search(pattern, quality_enforcement_content, re.DOTALL), (
            "L2-REINJECT rank=10 does not reference 'jerry ast frontmatter' and "
            "'jerry ast validate' within the same HTML comment directive"
        )

    def test_l2_reinject_when_checked_then_rank9_content_is_substantive(
        self, quality_enforcement_content: str
    ) -> None:
        """L2-REINJECT rank=10 content field must be non-trivial (>= 50 chars)."""
        # Arrange
        pattern = r'rank=10.*?content="([^"]*)"'
        match = re.search(pattern, quality_enforcement_content)

        # Act/Assert
        assert match, "L2-REINJECT rank=10 missing content= field"
        content_value = match.group(1)
        assert len(content_value) >= 50, (
            f"L2-REINJECT rank=10 content is too short ({len(content_value)} chars). "
            f"Must be >= 50 chars for meaningful reinforcement."
        )

    def test_l2_reinject_when_checked_then_rank9_is_unique(
        self, quality_enforcement_content: str
    ) -> None:
        """Only one L2-REINJECT marker should use rank=10 to avoid ambiguity."""
        # Arrange
        matches = re.findall(r"rank=10", quality_enforcement_content)

        # Act/Assert
        assert len(matches) == 1, (
            f"Expected exactly 1 L2-REINJECT rank=10 marker, found {len(matches)}. "
            f"Duplicate ranks cause enforcement ambiguity."
        )


# =============================================================================
# Tests: Worktracker Agent Tool Gap (Bash in allowed_tools)
# =============================================================================


class TestWorktrackerAgentToolAccess:
    """Tests for Bash tool declaration in wt-* agent YAML frontmatter."""

    @pytest.mark.parametrize("agent_file", EXPECTED_WT_AGENT_FILES)
    def test_agent_yaml_when_checked_then_declares_bash(
        self, wt_agents_dir: Path, agent_file: str
    ) -> None:
        """Each wt-* agent must declare Bash in allowed_tools YAML."""
        # Arrange
        content = (wt_agents_dir / agent_file).read_text()
        pattern = r"allowed_tools:.*?- Bash"

        # Act/Assert
        assert re.search(pattern, content, re.DOTALL), (
            f"{agent_file} does not declare '- Bash' in allowed_tools YAML"
        )

    @pytest.mark.parametrize("agent_file", EXPECTED_WT_AGENT_FILES)
    def test_agent_capabilities_when_checked_then_has_bash_row(
        self, wt_agents_dir: Path, agent_file: str
    ) -> None:
        """Each wt-* agent must have a Bash row in the capabilities table."""
        # Arrange
        content = (wt_agents_dir / agent_file).read_text()
        pattern = r"\|\s*Bash\s*\|.*AST.*\|.*REQUIRED.*H-33.*\|"

        # Act/Assert
        assert re.search(pattern, content), (
            f"{agent_file} missing Bash row in capabilities table with H-33 reference"
        )


# =============================================================================
# Tests: Worktracker Agent Language Enforcement (MUST, not PREFERRED)
# =============================================================================


class TestWorktrackerAgentLanguage:
    """Tests for HARD-tier language in wt-* agent AST sections."""

    @staticmethod
    def _extract_ast_section(content: str) -> str | None:
        """Extract the AST-Based Operations section from agent content.

        Uses section boundary detection: from '**AST-Based Operations' to the
        next bold heading (any '**' starting with a capital letter) or EOF.
        """
        ast_start = content.find("**AST-Based Operations")
        if ast_start == -1:
            return None
        # Find the end: next bold heading or ## section after the AST heading line
        rest = content[ast_start + len("**AST-Based Operations") :]
        # Skip past the first line (the heading itself)
        first_newline = rest.find("\n")
        if first_newline == -1:
            return content[ast_start:]
        rest_after_heading = rest[first_newline:]
        # Find the next bold heading starting with a capital letter
        end_match = re.search(r"\n\*\*[A-Z][a-z]", rest_after_heading)
        if end_match:
            return content[
                ast_start : ast_start
                + len("**AST-Based Operations")
                + first_newline
                + end_match.start()
            ]
        return content[ast_start:]

    @pytest.mark.parametrize("agent_file", EXPECTED_WT_AGENT_FILES)
    def test_agent_ast_section_when_checked_then_uses_required_heading(
        self, wt_agents_dir: Path, agent_file: str
    ) -> None:
        """AST operations section must use 'REQUIRED — H-33' heading."""
        # Arrange
        content = (wt_agents_dir / agent_file).read_text()

        # Act/Assert
        assert "REQUIRED — H-33" in content, (
            f"{agent_file} AST section heading does not contain 'REQUIRED — H-33'"
        )

    @pytest.mark.parametrize("agent_file", EXPECTED_WT_AGENT_FILES)
    def test_agent_ast_section_when_checked_then_no_preferred_language(
        self, wt_agents_dir: Path, agent_file: str
    ) -> None:
        """AST operations section must not use MEDIUM-tier language (PREFERRED/SHOULD)."""
        # Arrange
        content = (wt_agents_dir / agent_file).read_text()
        ast_section = self._extract_ast_section(content)

        # Act/Assert
        assert ast_section is not None, f"{agent_file} missing AST-Based Operations section"
        for word in PROHIBITED_MEDIUM_TIER_WORDS:
            assert word not in ast_section, (
                f"{agent_file} AST section contains MEDIUM-tier word '{word}' "
                f"— must use HARD-tier language (MUST/REQUIRED)"
            )

    @pytest.mark.parametrize("agent_file", EXPECTED_WT_AGENT_FILES)
    def test_agent_enforcement_note_when_checked_then_references_h31(
        self, wt_agents_dir: Path, agent_file: str
    ) -> None:
        """Enforcement note must reference H-33 (not 'Migration Note')."""
        # Arrange
        content = (wt_agents_dir / agent_file).read_text()

        # Act/Assert
        assert "**Enforcement (H-33):**" in content, (
            f"{agent_file} missing '**Enforcement (H-33):**' note"
        )

    @pytest.mark.parametrize("agent_file", EXPECTED_WT_AGENT_FILES)
    def test_agent_when_checked_then_no_migration_note(
        self, wt_agents_dir: Path, agent_file: str
    ) -> None:
        """Migration Note (ST-007) must have been replaced by Enforcement (H-33)."""
        # Arrange
        content = (wt_agents_dir / agent_file).read_text()

        # Act/Assert
        assert "Migration Note" not in content, (
            f"{agent_file} still contains 'Migration Note' — should be 'Enforcement (H-33)'"
        )


# =============================================================================
# Tests: Plugin Root Path Prefix (--directory ${CLAUDE_PLUGIN_ROOT})
# =============================================================================


class TestWorktrackerAgentPluginRoot:
    """Tests for jerry ast CLI pattern in wt-* agent invocations."""

    @pytest.mark.parametrize("agent_file", EXPECTED_WT_AGENT_FILES)
    def test_agent_when_checked_then_no_python_c_pattern(
        self, wt_agents_dir: Path, agent_file: str
    ) -> None:
        """No 'python -c' invocations (old ast_ops pattern replaced by CLI)."""
        # Arrange
        content = (wt_agents_dir / agent_file).read_text()

        # Act/Assert
        assert "python -c" not in content, (
            f"{agent_file} still contains 'python -c' invocations — "
            f"should use 'jerry ast' CLI commands instead"
        )

    @pytest.mark.parametrize("agent_file", EXPECTED_WT_AGENT_FILES)
    def test_agent_when_checked_then_uses_jerry_ast_pattern(
        self, wt_agents_dir: Path, agent_file: str
    ) -> None:
        """Each agent must use 'jerry ast' CLI commands."""
        # Arrange
        content = (wt_agents_dir / agent_file).read_text()

        # Act/Assert
        assert "jerry ast" in content, (
            f"{agent_file} does not contain 'jerry ast' CLI command invocations"
        )

    @pytest.mark.parametrize("agent_file", EXPECTED_WT_AGENT_FILES)
    def test_agent_when_checked_then_all_uv_run_prefixed(
        self, wt_agents_dir: Path, agent_file: str
    ) -> None:
        """All uv run invocations must use --directory ${CLAUDE_PLUGIN_ROOT}."""
        # Arrange
        content = (wt_agents_dir / agent_file).read_text()
        all_uv_run = re.findall(r"uv run\b", content)
        prefixed_uv_run = re.findall(r"uv run --directory", content)

        # Act/Assert
        assert len(all_uv_run) == len(prefixed_uv_run), (
            f"{agent_file}: {len(all_uv_run)} 'uv run' calls but only "
            f"{len(prefixed_uv_run)} have --directory prefix"
        )


# =============================================================================
# Tests: /ast Skill Registration (CLAUDE.md, mandatory-skill-usage.md)
# =============================================================================


class TestAstSkillRegistration:
    """/ast skill must be registered per H-30 and source artifacts must exist."""

    def test_claude_md_when_checked_then_ast_in_quick_reference(
        self, claude_md_content: str
    ) -> None:
        """/ast must appear in CLAUDE.md Quick Reference skills table."""
        # Arrange
        pattern = r"\|\s*`/ast`\s*\|"

        # Act/Assert
        assert re.search(pattern, claude_md_content), (
            "/ast not found in CLAUDE.md Quick Reference skills table"
        )

    def test_mandatory_skill_when_checked_then_ast_in_trigger_map(
        self, mandatory_skill_content: str
    ) -> None:
        """/ast must have entries in mandatory-skill-usage.md trigger map."""
        # Arrange/Act/Assert
        assert "`/ast`" in mandatory_skill_content, (
            "/ast not found in mandatory-skill-usage.md trigger map"
        )

    def test_mandatory_skill_when_checked_then_h22_includes_ast(
        self, mandatory_skill_content: str
    ) -> None:
        """H-22 rule text must include /ast invocation clause within the same row."""
        # Arrange — single-line match ensures /ast is in the H-22 row, not a later row
        pattern = r"H-22\s*\|[^\n]*/ast"

        # Act/Assert
        assert re.search(pattern, mandatory_skill_content), (
            "H-22 rule text in mandatory-skill-usage.md does not mention /ast"
        )

    def test_mandatory_skill_when_checked_then_l2_reinject_includes_ast(
        self, mandatory_skill_content: str
    ) -> None:
        """L2-REINJECT in mandatory-skill-usage.md must reference /ast."""
        # Arrange
        pattern = r"L2-REINJECT.*?/ast"

        # Act/Assert
        assert re.search(pattern, mandatory_skill_content, re.DOTALL), (
            "L2-REINJECT in mandatory-skill-usage.md does not reference /ast"
        )

    def test_mandatory_skill_when_checked_then_trigger_map_has_frontmatter_keyword(
        self, mandatory_skill_content: str
    ) -> None:
        """Trigger map must include 'frontmatter' keyword mapping to /ast."""
        # Arrange
        pattern = r"frontmatter.*\|\s*`/ast`\s*\|"

        # Act/Assert
        assert re.search(pattern, mandatory_skill_content, re.DOTALL), (
            "mandatory-skill-usage.md trigger map missing 'frontmatter' -> /ast mapping"
        )

    def test_ast_skill_when_checked_then_skill_md_exists(self, project_root: Path) -> None:
        """/ast skill must have a SKILL.md file (H-25)."""
        # Arrange
        skill_file = project_root / "skills" / "ast" / "SKILL.md"

        # Act/Assert
        assert skill_file.exists(), (
            "skills/ast/SKILL.md does not exist — /ast skill registered but source missing"
        )

    def test_ast_skill_when_checked_then_ast_ops_does_not_exist(self, project_root: Path) -> None:
        """ast_ops.py must NOT exist (BUG-002: CLI is the single adapter)."""
        # Arrange
        ast_ops = project_root / "skills" / "ast" / "scripts" / "ast_ops.py"

        # Act/Assert
        assert not ast_ops.exists(), (
            "skills/ast/scripts/ast_ops.py still exists — BUG-002 requires deletion; "
            "agents should use 'jerry ast' CLI commands instead"
        )


# =============================================================================
# Tests: AGENTS.md Enforcement Note
# =============================================================================


class TestAgentsMdEnforcement:
    """Tests for AST enforcement note in AGENTS.md worktracker section."""

    def test_agents_md_when_checked_then_has_h31_enforcement_note(
        self, agents_md_content: str
    ) -> None:
        """AGENTS.md must contain AST Enforcement (H-33) note."""
        # Arrange/Act/Assert
        assert "AST Enforcement (H-33)" in agents_md_content, (
            "AGENTS.md missing 'AST Enforcement (H-33)' note in worktracker section"
        )

    def test_agents_md_when_checked_then_enforcement_prohibits_regex(
        self, agents_md_content: str
    ) -> None:
        """AGENTS.md enforcement note must explicitly prohibit regex-based parsing."""
        # Arrange
        wt_match = re.search(
            r"## Worktracker Skill Agents.*?(?=\n## |\Z)",
            agents_md_content,
            re.DOTALL,
        )

        # Act/Assert
        assert wt_match, "AGENTS.md missing 'Worktracker Skill Agents' section"
        wt_section = wt_match.group(0).lower()
        assert "regex" in wt_section and "prohibited" in wt_section, (
            "AGENTS.md Worktracker section does not explicitly prohibit "
            "regex-based frontmatter parsing (must contain both 'regex' and 'prohibited')"
        )

    def test_agents_md_when_checked_then_enforcement_references_plugin_root(
        self, agents_md_content: str
    ) -> None:
        """AGENTS.md enforcement note must reference ${CLAUDE_PLUGIN_ROOT} invocation."""
        # Arrange/Act/Assert
        assert "${CLAUDE_PLUGIN_ROOT}" in agents_md_content, (
            "AGENTS.md enforcement note missing ${CLAUDE_PLUGIN_ROOT} reference"
        )

    def test_agents_md_when_checked_then_enforcement_in_worktracker_section(
        self, agents_md_content: str
    ) -> None:
        """Enforcement note must be in the Worktracker Skill Agents section."""
        # Arrange
        wt_match = re.search(
            r"## Worktracker Skill Agents.*?(?=\n## |\Z)",
            agents_md_content,
            re.DOTALL,
        )

        # Act/Assert
        assert wt_match, "AGENTS.md missing 'Worktracker Skill Agents' section"
        wt_section = wt_match.group(0)
        assert "AST Enforcement (H-33)" in wt_section, (
            "H-33 enforcement note not in Worktracker Skill Agents section"
        )


# =============================================================================
# Tests: AST Function Coverage in Agent Examples
# =============================================================================


class TestWorktrackerAgentAstExamples:
    """Tests for jerry ast CLI command references in agent code examples."""

    @pytest.mark.parametrize("agent_file", EXPECTED_WT_AGENT_FILES)
    def test_agent_when_checked_then_references_jerry_ast_frontmatter(
        self, wt_agents_dir: Path, agent_file: str
    ) -> None:
        """Each agent must reference 'jerry ast frontmatter' in AST examples."""
        # Arrange
        content = (wt_agents_dir / agent_file).read_text()

        # Act/Assert
        assert "jerry ast frontmatter" in content, (
            f"{agent_file} does not reference 'jerry ast frontmatter' in AST examples"
        )

    @pytest.mark.parametrize("agent_file", EXPECTED_WT_AGENT_FILES)
    def test_agent_when_checked_then_no_ast_ops_import(
        self, wt_agents_dir: Path, agent_file: str
    ) -> None:
        """No agent should import from skills.ast.scripts.ast_ops (BUG-002)."""
        # Arrange
        content = (wt_agents_dir / agent_file).read_text()

        # Act/Assert
        assert "from skills.ast.scripts.ast_ops import" not in content, (
            f"{agent_file} still contains 'from skills.ast.scripts.ast_ops import' — "
            f"should use 'jerry ast' CLI commands instead (BUG-002)"
        )

    @pytest.mark.parametrize("agent_file", ["wt-auditor.md", "wt-verifier.md"])
    def test_agent_when_checked_then_references_jerry_ast_validate(
        self, wt_agents_dir: Path, agent_file: str
    ) -> None:
        """Agents that perform schema validation must reference 'jerry ast validate'."""
        # Arrange
        content = (wt_agents_dir / agent_file).read_text()

        # Act/Assert
        assert "jerry ast validate" in content, (
            f"{agent_file} does not reference 'jerry ast validate' in AST examples"
        )


# =============================================================================
# Tests: Anti-Pattern Detection (Forbidden regex frontmatter patterns)
# =============================================================================


class TestWorktrackerAgentAntiPatterns:
    """Tests that wt-* agents do not contain forbidden regex-based frontmatter patterns.

    Anti-pattern detection must distinguish between:
    - Instructional usage (agent tells LLM to use Grep for frontmatter) — FORBIDDEN
    - Prohibition context (enforcement note says 'DO NOT use Grep(...)') — ALLOWED
    """

    @staticmethod
    def _is_prohibition_context(lines: list[str], match_line_idx: int) -> bool:
        """Check if a match is within prohibition/enforcement context.

        Looks at the match line and surrounding lines (up to 3 lines before)
        for prohibition keywords like 'DO NOT', 'NEVER', 'prohibited', 'forbidden'.
        """
        prohibition_keywords = [
            "DO NOT",
            "NEVER",
            "prohibited",
            "forbidden",
            "replaces",
            "replaced",
        ]
        # Check the match line itself and up to 3 preceding lines
        start = max(0, match_line_idx - 3)
        context_lines = lines[start : match_line_idx + 1]
        context_text = " ".join(context_lines)
        return any(kw in context_text for kw in prohibition_keywords)

    @pytest.mark.parametrize("agent_file", EXPECTED_WT_AGENT_FILES)
    def test_agent_when_checked_then_no_grep_status_pattern(
        self, wt_agents_dir: Path, agent_file: str
    ) -> None:
        """Agents must not contain Grep patterns for blockquote frontmatter fields.

        Matches within prohibition/enforcement context (e.g., 'DO NOT use Grep(...)')
        are excluded — only instructional usage is flagged.
        """
        # Arrange
        content = (wt_agents_dir / agent_file).read_text()
        lines = content.splitlines()

        # Act: check each anti-pattern, excluding prohibition context
        violations = []
        for anti_pattern in FORBIDDEN_ANTI_PATTERNS:
            for line_idx, line in enumerate(lines):
                if re.search(anti_pattern, line):
                    if not self._is_prohibition_context(lines, line_idx):
                        violations.append(
                            f"  Line {line_idx + 1}: {line.strip()} (pattern: {anti_pattern})"
                        )

        # Assert
        assert len(violations) == 0, (
            f"{agent_file} contains forbidden anti-patterns outside prohibition context. "
            f"H-33 requires AST-based extraction, not regex:\n" + "\n".join(violations)
        )

    @pytest.mark.parametrize("agent_file", EXPECTED_WT_AGENT_FILES)
    def test_agent_when_checked_then_no_grep_for_frontmatter_outside_prohibition(
        self, wt_agents_dir: Path, agent_file: str
    ) -> None:
        """Agents must not instruct Grep usage for frontmatter extraction.

        Grep references in enforcement/prohibition notes are allowed;
        instructional Grep usage for frontmatter is not.
        Context window: checks up to 3 lines before the match for prohibition keywords.
        """
        # Arrange
        content = (wt_agents_dir / agent_file).read_text()
        lines = content.splitlines()

        # Act: find lines mentioning both Grep and Status/frontmatter
        violations = []
        for line_idx, line in enumerate(lines):
            if "Grep" in line and "Status" in line:
                # Allow lines within prohibition/enforcement context
                if self._is_prohibition_context(lines, line_idx):
                    continue
                violations.append(f"  Line {line_idx + 1}: {line.strip()}")

        # Assert
        assert len(violations) == 0, (
            f"{agent_file} has Grep+Status references that appear instructional "
            f"(not prohibition text):\n" + "\n".join(violations)
        )
