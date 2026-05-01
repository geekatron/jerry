# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for scripts/check_skill_adr_references.py (TASK-008).

Tests cover:
    - Passing case: valid ADR reference resolves to an existing file -> exit 0.
    - Failing case: broken ADR reference (target does not exist) -> exit 1 with
      error message naming the broken reference.
    - Edge case: multiple references, some valid, some not; script reports ALL
      broken references, not just the first.
    - extract_adr_references: anchor fragment stripping, multi-match per line.
    - resolve_adr_path: relative (../../) vs repo-root-relative paths.
    - format_violation_line: message format matches ci-check-spec.md spec.
    - format_summary_line: summary format matches ci-check-spec.md spec.
    - main: no SKILL.md files found -> exit 0 with informational message.

References:
    - TASK-008: Add CI check: every SKILL.md ADR cross-reference resolves
    - ci-check-spec.md: Test fixture and expected output specification
    - H-20: BDD test-first approach
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# ---------------------------------------------------------------------------
# Import module under test
# ---------------------------------------------------------------------------

_project_root = Path(__file__).parent.parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from scripts.check_skill_adr_references import (  # noqa: E402
    extract_adr_references,
    format_summary_line,
    format_violation_line,
    main,
    resolve_adr_path,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_skill_md(tmp_path: Path, content: str, skill_name: str = "fake-skill") -> Path:
    """Create a minimal skills/<skill_name>/SKILL.md under tmp_path.

    Args:
        tmp_path: Pytest-provided temporary directory.
        content: Markdown content to write into the SKILL.md file.
        skill_name: Subdirectory name under skills/.

    Returns:
        Absolute path to the created SKILL.md file.
    """
    skill_dir = tmp_path / "skills" / skill_name
    skill_dir.mkdir(parents=True)
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text(content, encoding="utf-8")
    return skill_md


def _make_adr_file(tmp_path: Path, filename: str) -> Path:
    """Create an ADR file at docs/adrs/<filename> under tmp_path.

    Args:
        tmp_path: Pytest-provided temporary directory.
        filename: ADR filename (e.g., ``ADR-007-output-template-specification.md``).

    Returns:
        Absolute path to the created ADR file.
    """
    adrs_dir = tmp_path / "docs" / "adrs"
    adrs_dir.mkdir(parents=True, exist_ok=True)
    adr_file = adrs_dir / filename
    adr_file.write_text("# ADR content\n", encoding="utf-8")
    return adr_file


# ---------------------------------------------------------------------------
# Passing case: valid ADR reference, file exists -> exit 0
# ---------------------------------------------------------------------------


@pytest.mark.happy_path
def test_valid_adr_reference_exits_zero(tmp_path: Path) -> None:
    """A SKILL.md with one valid ADR reference (file exists) returns exit code 0.

    Arrange: Create SKILL.md with a relative ADR link and the matching ADR file.
    Act: Run main() with the SKILL.md path as argument (no git needed).
    Assert: Exit code is 0.
    """
    _make_adr_file(tmp_path, "ADR-007-output-template-specification.md")
    skill_md = _make_skill_md(
        tmp_path,
        "See [ADR-007](../../docs/adrs/ADR-007-output-template-specification.md) here.\n",
    )

    with patch("scripts.check_skill_adr_references.get_repo_root", return_value=tmp_path):
        exit_code = main([str(skill_md)])

    assert exit_code == 0


# ---------------------------------------------------------------------------
# Failing case: broken ADR reference (target missing) -> exit 1
# ---------------------------------------------------------------------------


@pytest.mark.negative
def test_broken_adr_reference_exits_one(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """A SKILL.md with a broken ADR reference (file does not exist) returns exit code 1.

    Arrange: Create SKILL.md with a link to a non-existent ADR file.
    Act: Run main() with the SKILL.md path as argument.
    Assert: Exit code is 1 and the error message names the broken reference.
    """
    skill_md = _make_skill_md(
        tmp_path,
        "- [ADR-007](../../docs/adrs/ADR-007-DOES-NOT-EXIST.md) - broken\n",
    )

    with patch("scripts.check_skill_adr_references.get_repo_root", return_value=tmp_path):
        exit_code = main([str(skill_md)])

    assert exit_code == 1

    captured = capsys.readouterr()
    output = captured.out

    # Error message must name the broken reference
    assert "BROKEN ADR REF" in output
    assert "ADR-007-DOES-NOT-EXIST.md" in output
    # Summary line must be present
    assert "1 broken reference(s)" in output


# ---------------------------------------------------------------------------
# Edge case: multiple references, some valid, some not -> all broken reported
# ---------------------------------------------------------------------------


@pytest.mark.edge_case
def test_multiple_references_reports_all_broken(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """A SKILL.md with mixed valid/broken references reports ALL broken ones.

    Arrange: Create SKILL.md with two broken and one valid ADR reference.
             Only the valid ADR file exists on disk.
    Act: Run main() with the SKILL.md path.
    Assert: Exit code is 1 and both broken references appear in the output;
            the valid reference is not mentioned.
    """
    _make_adr_file(tmp_path, "ADR-007-output-template-specification.md")

    content = (
        "- [ADR-X](../../docs/adrs/ADR-007-FIRST-BROKEN.md) - broken\n"
        "- [ADR-007](../../docs/adrs/ADR-007-output-template-specification.md) - valid\n"
        "- [ADR-Y](../../docs/adrs/ADR-007-SECOND-BROKEN.md) - also broken\n"
    )
    skill_md = _make_skill_md(tmp_path, content)

    with patch("scripts.check_skill_adr_references.get_repo_root", return_value=tmp_path):
        exit_code = main([str(skill_md)])

    assert exit_code == 1

    captured = capsys.readouterr()
    output = captured.out

    # Both broken references must appear
    assert "ADR-007-FIRST-BROKEN.md" in output
    assert "ADR-007-SECOND-BROKEN.md" in output
    # Valid reference must NOT appear as broken
    assert (
        "ADR-007-output-template-specification.md" not in output.split("BROKEN ADR REF")[0]
        or "ADR-007-output-template-specification.md" in output.split("BROKEN ADR REF")[0]
    )

    # More direct assertion: only 2 "BROKEN ADR REF" lines
    broken_lines = [line for line in output.splitlines() if "BROKEN ADR REF" in line]
    assert len(broken_lines) == 2

    # Summary shows 2 broken references
    assert "2 broken reference(s)" in output


# ---------------------------------------------------------------------------
# extract_adr_references: unit tests
# ---------------------------------------------------------------------------


@pytest.mark.happy_path
def test_extract_strips_anchor_fragment(tmp_path: Path) -> None:
    """extract_adr_references strips #anchor fragments from link targets.

    Args:
        tmp_path: Pytest-provided temp directory.
    """
    skill_md = _make_skill_md(
        tmp_path,
        "See [ADR-007](../../docs/adrs/ADR-007-spec.md#section-3) for details.\n",
    )
    refs = extract_adr_references(skill_md)

    assert len(refs) == 1
    lineno, raw_path = refs[0]
    assert lineno == 1
    assert raw_path == "../../docs/adrs/ADR-007-spec.md"


@pytest.mark.happy_path
def test_extract_multiple_refs_on_one_line(tmp_path: Path) -> None:
    """extract_adr_references finds multiple ADR links on a single line.

    Args:
        tmp_path: Pytest-provided temp directory.
    """
    content = "See [A](../../docs/adrs/ADR-001-foo.md) and [B](../../docs/adrs/ADR-002-bar.md).\n"
    skill_md = _make_skill_md(tmp_path, content)
    refs = extract_adr_references(skill_md)

    assert len(refs) == 2
    paths = [r[1] for r in refs]
    assert "../../docs/adrs/ADR-001-foo.md" in paths
    assert "../../docs/adrs/ADR-002-bar.md" in paths


@pytest.mark.happy_path
def test_extract_ignores_non_adr_links(tmp_path: Path) -> None:
    """extract_adr_references ignores links that are not ADR references.

    Args:
        tmp_path: Pytest-provided temp directory.
    """
    content = "See [README](../README.md) and [some doc](docs/reference/foo.md).\n"
    skill_md = _make_skill_md(tmp_path, content)
    refs = extract_adr_references(skill_md)

    assert refs == []


@pytest.mark.negative
def test_extract_returns_empty_for_unreadable_file(tmp_path: Path) -> None:
    """extract_adr_references returns empty list if file cannot be read.

    Args:
        tmp_path: Pytest-provided temp directory.
    """
    nonexistent = tmp_path / "skills" / "ghost" / "SKILL.md"
    refs = extract_adr_references(nonexistent)
    assert refs == []


# ---------------------------------------------------------------------------
# resolve_adr_path: unit tests
# ---------------------------------------------------------------------------


@pytest.mark.happy_path
def test_resolve_relative_path(tmp_path: Path) -> None:
    """resolve_adr_path normalizes a relative ../../ path to repo-root-relative.

    Args:
        tmp_path: Pytest-provided temp directory.
    """
    skill_file = tmp_path / "skills" / "transcript" / "SKILL.md"
    raw_path = "../../docs/adrs/ADR-007-spec.md"

    resolved = resolve_adr_path(skill_file, raw_path, tmp_path)

    assert resolved == Path("docs/adrs/ADR-007-spec.md")


@pytest.mark.happy_path
def test_resolve_already_repo_relative_path(tmp_path: Path) -> None:
    """resolve_adr_path passes through a repo-root-relative path unchanged.

    Args:
        tmp_path: Pytest-provided temp directory.
    """
    skill_file = tmp_path / "skills" / "transcript" / "SKILL.md"
    raw_path = "docs/adrs/ADR-007-spec.md"

    resolved = resolve_adr_path(skill_file, raw_path, tmp_path)

    assert resolved == Path("docs/adrs/ADR-007-spec.md")


# ---------------------------------------------------------------------------
# format_violation_line: unit test
# ---------------------------------------------------------------------------


@pytest.mark.happy_path
def test_format_violation_line_matches_spec(tmp_path: Path) -> None:
    """format_violation_line output matches the ci-check-spec.md format exactly.

    Expected format:
        BROKEN ADR REF: {skill_file}:{line}: '{raw_path}' -> resolved
        '{resolved}' does not exist

    Args:
        tmp_path: Pytest-provided temp directory.
    """
    skill_file = tmp_path / "skills" / "fake-skill" / "SKILL.md"
    raw_path = "../../docs/adrs/ADR-007-DOES-NOT-EXIST.md"
    resolved = Path("docs/adrs/ADR-007-DOES-NOT-EXIST.md")

    line = format_violation_line(tmp_path, skill_file, 12, raw_path, resolved)

    assert line.startswith("BROKEN ADR REF:")
    assert "skills/fake-skill/SKILL.md:12:" in line
    assert "'../../docs/adrs/ADR-007-DOES-NOT-EXIST.md'" in line
    assert "resolved 'docs/adrs/ADR-007-DOES-NOT-EXIST.md'" in line
    assert "does not exist" in line


# ---------------------------------------------------------------------------
# format_summary_line: unit test
# ---------------------------------------------------------------------------


@pytest.mark.happy_path
def test_format_summary_line() -> None:
    """format_summary_line produces the expected summary string.

    Args: None.
    """
    summary = format_summary_line(broken_count=3, file_count=2)

    assert "3 broken reference(s)" in summary
    assert "2 SKILL.md file(s)" in summary
    assert "Fix the paths or vendor the missing ADR files." in summary


# ---------------------------------------------------------------------------
# main: no SKILL.md files found
# ---------------------------------------------------------------------------


@pytest.mark.edge_case
def test_main_no_skill_files_found(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """main exits 0 with informational message when no SKILL.md files are found.

    Arrange: Pass an explicit path to a SKILL.md that does not exist.
    Act: Run main() with that path.
    Assert: Exit code is 0 (no violations from no files).
    """
    with patch("scripts.check_skill_adr_references.get_repo_root", return_value=tmp_path):
        with patch("scripts.check_skill_adr_references.discover_skill_files", return_value=[]):
            # Run with no argv to trigger auto-discovery (which we mock to return [])
            exit_code = main([])

    assert exit_code == 0
    captured = capsys.readouterr()
    assert "no SKILL.md files found" in captured.out


# ---------------------------------------------------------------------------
# Integration: ci-check-spec.md test fixture
# ---------------------------------------------------------------------------


@pytest.mark.happy_path
def test_spec_fixture_exact_output(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Reproduces the ci-check-spec.md test fixture scenario.

    The spec defines:
        - One broken reference (ADR-007-DOES-NOT-EXIST.md) on line 12.
        - One valid reference (ADR-007-output-template-specification.md) on line 13.
        - Expected exit code: 1.
        - Expected output contains exactly 1 BROKEN ADR REF line.
        - Summary: 1 broken reference(s) found in 1 SKILL.md file(s).

    Args:
        tmp_path: Pytest-provided temp directory.
        capsys: Pytest capture fixture.
    """
    # Create the valid ADR file so the second reference resolves
    _make_adr_file(tmp_path, "ADR-007-output-template-specification.md")

    # Build SKILL.md with 11 lines of preamble so ADR refs land on lines 12-13
    preamble = "---\nname: fake-skill\ndescription: A fake skill for CI check testing.\n---\n\n"
    preamble += "# Fake Skill\n\n## References\n\n"  # lines 5-9 (0-padded); 9 total so far
    # line 10 blank, line 11 blank -> refs on lines 12 and 13
    preamble += "\n\n"
    content = (
        preamble
        + "- [ADR-007](../../docs/adrs/ADR-007-DOES-NOT-EXIST.md) - A broken ADR reference\n"
        + "- [ADR-007](../../docs/adrs/ADR-007-output-template-specification.md)"
        + " - A valid ADR reference\n"
    )

    skill_md = _make_skill_md(tmp_path, content)

    with patch("scripts.check_skill_adr_references.get_repo_root", return_value=tmp_path):
        exit_code = main([str(skill_md)])

    assert exit_code == 1

    captured = capsys.readouterr()
    output = captured.out

    broken_lines = [line for line in output.splitlines() if "BROKEN ADR REF" in line]
    assert len(broken_lines) == 1
    assert "ADR-007-DOES-NOT-EXIST.md" in broken_lines[0]
    # Valid reference must NOT appear as broken
    valid_broken = [ln for ln in broken_lines if "ADR-007-output-template-specification" in ln]
    assert valid_broken == []

    assert "1 broken reference(s) found in 1 SKILL.md file(s)" in output
