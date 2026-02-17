"""E2E tests for progressive disclosure architecture verification.

This test suite validates:
1. Cross-references between rules, guides, and patterns are valid
2. No rules content was dropped (fidelity check)
3. Three-tier architecture is enforced (rules=auto, patterns=auto, guides=on-demand)

Tests verify that the progressive disclosure refactoring (FEAT-012) preserved all
content and maintains correct reference integrity.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

# ==================== TASK-001: Cross-reference E2E tests ====================


@pytest.mark.e2e
def test_guide_cross_references_to_rules_are_valid() -> None:
    """Verify every guide file cross-reference to a rule file points to an existing file.

    Guides reference rules using markdown links like:
    - [architecture-standards.md](../rules/architecture-standards.md)
    - See [coding-standards.md](../rules/coding-standards.md)
    """
    # Arrange
    repo_root = Path(__file__).parent.parent.parent
    guides_dir = repo_root / ".context" / "guides"
    rules_dir = repo_root / ".context" / "rules"

    assert guides_dir.exists(), ".context/guides/ directory should exist"
    assert rules_dir.exists(), ".context/rules/ directory should exist"

    # Pattern to match markdown links to rules
    # Matches: [text](../rules/filename.md) or [text](../rules/filename.md#anchor)
    rule_link_pattern = re.compile(r"\[([^\]]+)\]\(\.\./rules/([^)#]+\.md)")

    broken_references: list[tuple[str, str]] = []

    # Act: Scan all guide files for rule references
    guide_files = list(guides_dir.glob("*.md"))
    assert len(guide_files) > 0, "Should have at least one guide file"

    for guide_file in guide_files:
        content = guide_file.read_text()
        matches = rule_link_pattern.findall(content)

        for _, rule_filename in matches:
            referenced_rule = rules_dir / rule_filename
            if not referenced_rule.exists():
                broken_references.append((guide_file.name, rule_filename))

    # Assert: No broken references
    assert not broken_references, (
        f"Found {len(broken_references)} broken rule references in guides:\n"
        + "\n".join(f"  {guide} -> {rule}" for guide, rule in broken_references)
    )


@pytest.mark.e2e
def test_guide_cross_references_to_patterns_are_valid() -> None:
    """Verify every guide file cross-reference to a pattern file points to an existing file.

    Guides reference patterns using markdown links or inline mentions like:
    - [aggregate_pattern.py](../patterns/aggregate_pattern.py)
    - See `aggregate_pattern.py`
    """
    # Arrange
    repo_root = Path(__file__).parent.parent.parent
    guides_dir = repo_root / ".context" / "guides"
    patterns_dir = repo_root / ".context" / "patterns"

    assert guides_dir.exists(), ".context/guides/ directory should exist"
    assert patterns_dir.exists(), ".context/patterns/ directory should exist"

    # Pattern to match markdown links to patterns (both .py and .md)
    pattern_link_pattern = re.compile(r"\[([^\]]+)\]\(\.\./patterns/([^)#]+\.(py|md))")

    broken_references: list[tuple[str, str]] = []

    # Act: Scan all guide files for pattern references
    guide_files = list(guides_dir.glob("*.md"))

    for guide_file in guide_files:
        content = guide_file.read_text()
        matches = pattern_link_pattern.findall(content)

        for _link_text, pattern_path, _ext in matches:
            # Handle both flat and nested pattern paths
            referenced_pattern = patterns_dir / pattern_path
            if not referenced_pattern.exists():
                broken_references.append((guide_file.name, pattern_path))

    # Assert: No broken references
    assert not broken_references, (
        f"Found {len(broken_references)} broken pattern references in guides:\n"
        + "\n".join(f"  {guide} -> {pattern}" for guide, pattern in broken_references)
    )


@pytest.mark.e2e
def test_consolidated_redirects_point_to_existing_files() -> None:
    """Verify rule files marked as CONSOLIDATED redirect to existing target files.

    Some rule files have been consolidated and now contain a redirect message like:
    > **CONSOLIDATED:** Error handling rules are now in `coding-standards.md`.
    """
    # Arrange
    repo_root = Path(__file__).parent.parent.parent
    rules_dir = repo_root / ".context" / "rules"

    assert rules_dir.exists(), ".context/rules/ directory should exist"

    # Pattern to match CONSOLIDATED redirect messages
    # Matches: "rules are now in `target.md`" or "now in [target.md](target.md)"
    consolidated_pattern = re.compile(
        r"(?:now in|see)\s+(?:`([^`]+\.md)`|\[([^\]]+\.md)\])", re.IGNORECASE
    )

    broken_redirects: list[tuple[str, str]] = []

    # Act: Scan all rule files for CONSOLIDATED redirects
    rule_files = list(rules_dir.glob("*.md"))

    for rule_file in rule_files:
        content = rule_file.read_text()

        # Only check files that have CONSOLIDATED marker
        if "CONSOLIDATED" not in content:
            continue

        matches = consolidated_pattern.findall(content)

        for backtick_match, bracket_match in matches:
            target = backtick_match or bracket_match
            # Remove any anchor fragments
            target = target.split("#")[0]
            target_file = rules_dir / target

            if not target_file.exists():
                broken_redirects.append((rule_file.name, target))

    # Assert: No broken redirects
    assert not broken_redirects, (
        f"Found {len(broken_redirects)} broken CONSOLIDATED redirects:\n"
        + "\n".join(f"  {source} -> {target}" for source, target in broken_redirects)
    )


@pytest.mark.e2e
def test_rule_files_with_paths_frontmatter_have_valid_yaml() -> None:
    """Verify rule files with 'paths:' frontmatter have valid YAML format.

    Some rule files have YAML frontmatter like:
    ---
    paths:
      - .context/rules/
      - .claude/rules/
    ---
    """
    # Arrange
    repo_root = Path(__file__).parent.parent.parent
    rules_dir = repo_root / ".context" / "rules"

    assert rules_dir.exists(), ".context/rules/ directory should exist"

    # Pattern to detect YAML frontmatter
    frontmatter_pattern = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.MULTILINE | re.DOTALL)

    invalid_yaml_files: list[tuple[str, str]] = []

    # Act: Scan all rule files for frontmatter
    rule_files = list(rules_dir.glob("*.md"))

    for rule_file in rule_files:
        content = rule_file.read_text()
        match = frontmatter_pattern.match(content)

        if not match:
            continue  # No frontmatter

        yaml_content = match.group(1)

        # Basic validation: check for 'paths:' and proper indentation
        if "paths:" in yaml_content:
            # Verify paths are in a list format (starts with -)
            path_lines = [
                line.strip() for line in yaml_content.split("\n") if line.strip().startswith("-")
            ]

            if not path_lines:
                invalid_yaml_files.append(
                    (rule_file.name, "paths: keyword found but no list items")
                )

    # Assert: No invalid YAML
    assert not invalid_yaml_files, (
        f"Found {len(invalid_yaml_files)} rule files with invalid YAML frontmatter:\n"
        + "\n".join(f"  {file}: {reason}" for file, reason in invalid_yaml_files)
    )


# ==================== TASK-002: Fidelity verification ====================


@pytest.mark.e2e
def test_minimum_rule_file_count() -> None:
    """Verify minimum number of rule files exist (>= 7 files).

    This ensures the refactoring didn't accidentally drop rule files.
    Expected files include:
    - architecture-standards.md
    - coding-standards.md
    - quality-enforcement.md
    - testing-standards.md
    - project-workflow.md
    - python-environment.md
    - mandatory-skill-usage.md
    - markdown-navigation-standards.md
    Plus consolidated redirects.
    """
    # Arrange
    repo_root = Path(__file__).parent.parent.parent
    rules_dir = repo_root / ".context" / "rules"

    # Act
    rule_files = list(rules_dir.glob("*.md"))
    actual_count = len(rule_files)

    # Assert
    assert actual_count >= 7, (
        f"Expected at least 7 rule files, found {actual_count}. "
        f"Files: {sorted([f.name for f in rule_files])}"
    )


@pytest.mark.e2e
def test_minimum_guide_file_count() -> None:
    """Verify minimum number of guide files exist (>= 5 files).

    This ensures the refactoring didn't accidentally drop guide files.
    Expected files include:
    - architecture-patterns.md
    - architecture-layers.md
    - coding-practices.md
    - error-handling.md
    - testing-practices.md
    """
    # Arrange
    repo_root = Path(__file__).parent.parent.parent
    guides_dir = repo_root / ".context" / "guides"

    # Act
    guide_files = [f for f in guides_dir.glob("*.md") if not f.name.startswith("EN-")]
    actual_count = len(guide_files)

    # Assert
    assert actual_count >= 5, (
        f"Expected at least 5 guide files, found {actual_count}. "
        f"Files: {sorted([f.name for f in guide_files])}"
    )


@pytest.mark.e2e
def test_minimum_pattern_file_count() -> None:
    """Verify minimum number of Python pattern files exist (>= 4 .py files).

    This ensures the refactoring didn't accidentally drop pattern files.
    Expected files include:
    - aggregate_pattern.py
    - repository_pattern.py
    - value_object_pattern.py
    - domain_event_pattern.py
    - command_handler_pattern.py
    - exception_hierarchy_pattern.py
    """
    # Arrange
    repo_root = Path(__file__).parent.parent.parent
    patterns_dir = repo_root / ".context" / "patterns"

    # Act
    pattern_files = list(patterns_dir.glob("*.py"))
    actual_count = len(pattern_files)

    # Assert
    assert actual_count >= 4, (
        f"Expected at least 4 Python pattern files, found {actual_count}. "
        f"Files: {sorted([f.name for f in pattern_files])}"
    )


@pytest.mark.e2e
def test_no_rule_files_are_empty() -> None:
    """Verify all rule files have content beyond frontmatter.

    Empty or near-empty files indicate dropped content.
    Minimum expected content: > 100 characters (beyond YAML frontmatter).
    """
    # Arrange
    repo_root = Path(__file__).parent.parent.parent
    rules_dir = repo_root / ".context" / "rules"

    frontmatter_pattern = re.compile(r"^---\s*\n.*?\n---\s*\n", re.MULTILINE | re.DOTALL)

    empty_files: list[tuple[str, int]] = []

    # Act: Check each rule file for substantial content
    rule_files = list(rules_dir.glob("*.md"))

    for rule_file in rule_files:
        content = rule_file.read_text()

        # Remove frontmatter
        content_without_frontmatter = frontmatter_pattern.sub("", content).strip()

        # Check content length
        if len(content_without_frontmatter) < 100:
            empty_files.append((rule_file.name, len(content_without_frontmatter)))

    # Assert: No empty files
    assert not empty_files, (
        f"Found {len(empty_files)} rule files with insufficient content (<100 chars):\n"
        + "\n".join(f"  {file}: {length} chars" for file, length in empty_files)
    )


@pytest.mark.e2e
def test_consolidated_redirects_have_valid_targets() -> None:
    """Verify consolidated redirect files point to existing, non-empty targets.

    This is an extension of the redirect validation test that also checks
    the target file exists and has content.
    """
    # Arrange
    repo_root = Path(__file__).parent.parent.parent
    rules_dir = repo_root / ".context" / "rules"

    consolidated_pattern = re.compile(
        r"(?:now in|see)\s+(?:`([^`]+\.md)`|\[([^\]]+\.md)\])", re.IGNORECASE
    )

    invalid_targets: list[tuple[str, str, str]] = []

    # Act: Scan consolidated files
    rule_files = list(rules_dir.glob("*.md"))

    for rule_file in rule_files:
        content = rule_file.read_text()

        if "CONSOLIDATED" not in content:
            continue

        matches = consolidated_pattern.findall(content)

        for backtick_match, bracket_match in matches:
            target = backtick_match or bracket_match
            target = target.split("#")[0]
            target_file = rules_dir / target

            if not target_file.exists():
                invalid_targets.append((rule_file.name, target, "File does not exist"))
            elif len(target_file.read_text().strip()) < 100:
                invalid_targets.append((rule_file.name, target, "Target file is empty"))

    # Assert: All targets are valid and non-empty
    assert not invalid_targets, (
        f"Found {len(invalid_targets)} invalid redirect targets:\n"
        + "\n".join(
            f"  {source} -> {target}: {reason}" for source, target, reason in invalid_targets
        )
    )


# ==================== TASK-003: Three-tier architecture test ====================


@pytest.mark.e2e
def test_claude_rules_directory_exists() -> None:
    """Verify .claude/rules/ symlink exists (rules are synced).

    Rules should be automatically loaded via bootstrap script.
    """
    # Arrange
    repo_root = Path(__file__).parent.parent.parent
    claude_rules = repo_root / ".claude" / "rules"

    # Act & Assert
    assert claude_rules.exists(), (
        ".claude/rules/ should exist. Rules must be synced from .context/rules/ "
        "for automatic loading."
    )
    assert claude_rules.is_symlink(), ".claude/rules/ should be a symlink"


@pytest.mark.e2e
def test_claude_patterns_directory_exists() -> None:
    """Verify .claude/patterns/ symlink exists (patterns are synced).

    Patterns should be automatically loaded via bootstrap script.
    """
    # Arrange
    repo_root = Path(__file__).parent.parent.parent
    claude_patterns = repo_root / ".claude" / "patterns"

    # Act & Assert
    assert claude_patterns.exists(), (
        ".claude/patterns/ should exist. Patterns must be synced from .context/patterns/ "
        "for automatic loading."
    )
    assert claude_patterns.is_symlink(), ".claude/patterns/ should be a symlink"


@pytest.mark.e2e
def test_claude_guides_directory_does_not_exist() -> None:
    """Verify .claude/guides/ does NOT exist (guides are on-demand only).

    Guides should remain in .context/guides/ and be loaded only when explicitly
    requested via tools, not automatically loaded into context.
    """
    # Arrange
    repo_root = Path(__file__).parent.parent.parent
    claude_guides = repo_root / ".claude" / "guides"

    # Act & Assert
    assert not claude_guides.exists(), (
        ".claude/guides/ should NOT exist. Guides must remain on-demand only "
        "to prevent context pollution. They should be loaded explicitly via "
        "tools when needed, not automatically included in every session."
    )


@pytest.mark.e2e
def test_context_source_directories_exist() -> None:
    """Verify all three .context/ source directories exist.

    Even though guides aren't synced to .claude/, the source directories
    should all exist in .context/.
    """
    # Arrange
    repo_root = Path(__file__).parent.parent.parent
    context_dir = repo_root / ".context"

    # Act & Assert
    assert (context_dir / "rules").exists(), ".context/rules/ should exist"
    assert (context_dir / "patterns").exists(), ".context/patterns/ should exist"
    assert (context_dir / "guides").exists(), ".context/guides/ should exist"
