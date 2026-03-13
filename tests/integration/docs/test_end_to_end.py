# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""End-to-end integration tests for SkillExtractor with YamlFrontmatterReader.

Tests verify that the full extraction pipeline — SkillExtractor wired with
YamlFrontmatterReader — produces correct results against the real skills/
directory.  No mocks are used; all assertions run against live files.

Test methodology:
    - DA-004: skill count MUST equal len(list(Path('skills').glob('*/SKILL.md')));
      hardcoded integers are forbidden so that the test does not drift as new
      skills are added.
    - Verifies agent extraction works by asserting at least one skill has
      agent_count > 0 (skills with an agents/ directory).
    - Verifies that every extracted skill has a non-empty name field, proving
      M-5 schema validation gates out unnamed skills without crashing.

References:
    - DA-004: Dynamic skill count assertion (no hardcoded integers)
    - BUG-001: YamlFrontmatterReader wired into bootstrap / SkillExtractor
    - PROJ-0037-doc-module: Phase 2 end-to-end integration tests
"""

from __future__ import annotations

from pathlib import Path

import pytest

# Mark all tests in this module as integration tests.
pytestmark = [
    pytest.mark.integration,
]

# ---------------------------------------------------------------------------
# Project root discovery (same pattern as test_adversary_skill.py)
# ---------------------------------------------------------------------------

_PROJECT_ROOT = Path(__file__).parent.parent.parent.parent


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_extractor():
    """Return a SkillExtractor wired with YamlFrontmatterReader."""
    from src.docs.application.services.skill_extractor import SkillExtractor
    from src.docs.infrastructure.adapters.yaml_frontmatter_reader import (
        YamlFrontmatterReader,
    )

    return SkillExtractor(YamlFrontmatterReader())


# ---------------------------------------------------------------------------
# End-to-end extraction tests
# ---------------------------------------------------------------------------


class TestSkillExtractorEndToEnd:
    """End-to-end tests for SkillExtractor using YamlFrontmatterReader."""

    @pytest.mark.happy_path
    def test_extract_all_when_run_then_skill_count_matches_glob(self) -> None:
        """Extracted skill count equals the number of SKILL.md files on disk.

        DA-004: The count assertion uses a dynamic glob, NOT a hardcoded
        integer, so the test remains correct when new skills are added or
        removed without touching the test file.
        """
        skills_dir = str(_PROJECT_ROOT / "skills")

        # DA-004: dynamic count — never a hardcoded integer.
        expected_count = len(list(Path(skills_dir).glob("*/SKILL.md")))
        assert expected_count > 0, (
            "Sanity check: glob found zero SKILL.md files; "
            "skills/ directory may be missing or empty"
        )

        extractor = _make_extractor()
        skills = extractor.extract_all(skills_dir)

        assert len(skills) == expected_count, (
            f"SkillExtractor returned {len(skills)} skills but "
            f"glob found {expected_count} SKILL.md files. "
            "A skill may have failed extraction (check logs for warnings)."
        )

    @pytest.mark.happy_path
    def test_extract_all_when_run_then_at_least_one_skill_has_agents(self) -> None:
        """At least one extracted skill has agent_count > 0.

        Verifies that the agent extraction path (SkillExtractor._extract_agents)
        is exercised end-to-end and returns results.  Skills with an agents/
        subdirectory (e.g., adversary, problem-solving) must have agent_count > 0.
        """
        skills_dir = str(_PROJECT_ROOT / "skills")

        extractor = _make_extractor()
        skills = extractor.extract_all(skills_dir)

        skills_with_agents = [s for s in skills if s.agent_count > 0]
        assert len(skills_with_agents) > 0, (
            "Expected at least one skill with agent_count > 0 but found none. "
            "Agent extraction may be broken."
        )

    @pytest.mark.happy_path
    def test_extract_all_when_run_then_all_skills_have_non_empty_name(self) -> None:
        """Every extracted SkillData has a non-empty name field.

        M-5 validation in SkillExtractor skips skills with a missing or empty
        'name' field.  This test confirms that all returned SkillData objects
        passed validation — i.e., that no unnamed skills slipped through.
        """
        skills_dir = str(_PROJECT_ROOT / "skills")

        extractor = _make_extractor()
        skills = extractor.extract_all(skills_dir)

        for skill in skills:
            assert skill.name, (
                f"Extracted skill at {skill.file_path!r} has an empty name field. "
                "M-5 validation should have excluded this skill."
            )
            assert len(skill.name) > 0, f"skill.name is non-None but empty for {skill.file_path!r}"
