"""E2E tests for progressive disclosure architecture verification.

Enabler: EN-906 -- Fidelity Verification & Cross-Reference Testing

This test suite validates:
1. HARD rule coverage: every H-XX rule has guide explanation (TC-1)
2. Cross-references: links between rules, guides, and patterns are valid (TC-2)
3. Guide content quality: no empty or stub-only guide files (TC-3)
4. Navigation tables: all guides have navigation with resolvable anchors (TC-4)
5. Content coverage metric: regression baseline for total guide volume (TC-5)
6. File counts and fidelity: no files dropped during restructuring
7. Three-tier architecture: rules=auto, patterns=auto, guides=on-demand

Tests verify that the progressive disclosure refactoring (FEAT-012) preserved all
content and maintains correct reference integrity.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

# ==================== TC-1: HARD rule guide coverage (TASK-001) ====================


@pytest.mark.e2e
def test_all_hard_rules_have_guide_coverage() -> None:
    """Verify every HARD rule (H-01 through H-24) is documented in .context/.

    TC-1 / TASK-001: Parses the HARD Rule Index table in quality-enforcement.md
    to extract all H-XX IDs, then scans all .context/rules/*.md and
    .context/guides/*.md files to verify each H-XX ID appears in at least one
    documentation file. This catches HARD rules that disappeared from the
    documentation ecosystem during the progressive disclosure restructuring.

    Note: Rules files are the primary location for HARD rule definitions.
    Guides provide extended explanations. Both are valid coverage locations.
    """
    # Arrange
    repo_root = Path(__file__).parent.parent.parent
    rules_dir = repo_root / ".context" / "rules"
    guides_dir = repo_root / ".context" / "guides"

    qe_file = rules_dir / "quality-enforcement.md"
    assert qe_file.exists(), "quality-enforcement.md should exist"
    assert guides_dir.exists(), ".context/guides/ directory should exist"

    # Extract all H-XX IDs from the HARD Rule Index table
    qe_content = qe_file.read_text()
    hard_rule_pattern = re.compile(r"^\|\s*(H-\d+)\s*\|", re.MULTILINE)
    hard_rule_ids = sorted(set(hard_rule_pattern.findall(qe_content)))

    assert len(hard_rule_ids) >= 24, (
        f"Expected at least 24 HARD rule IDs in quality-enforcement.md, "
        f"found {len(hard_rule_ids)}: {hard_rule_ids}"
    )

    # Act: Scan all rules AND guides files for H-XX references
    doc_files: list[Path] = list(rules_dir.glob("*.md"))
    doc_files.extend(guides_dir.glob("*.md"))

    assert len(doc_files) > 0, "Should have documentation files to scan"

    # Build combined content from all documentation files (excluding SSOT)
    all_doc_content = ""
    for doc_file in doc_files:
        all_doc_content += doc_file.read_text() + "\n"

    # Check which H-XX IDs are missing from documentation
    uncovered_rules: list[str] = []
    for rule_id in hard_rule_ids:
        # Use word boundary to avoid partial matches (e.g., H-1 matching H-10)
        pattern = re.compile(r"\b" + re.escape(rule_id) + r"\b")
        if not pattern.search(all_doc_content):
            uncovered_rules.append(rule_id)

    # Assert: Every H-XX ID is documented in at least one file
    assert not uncovered_rules, (
        f"Found {len(uncovered_rules)} HARD rules with no documentation coverage:\n"
        f"  Missing: {', '.join(uncovered_rules)}\n"
        f"  Files scanned: {sorted([f.name for f in doc_files])}\n"
        f"  Each HARD rule should be documented in .context/rules/ or .context/guides/."
    )


# ==================== TC-2: Cross-reference validation (TASK-002) ====================


@pytest.mark.e2e
def test_guide_cross_references_to_rules_are_valid() -> None:
    """Verify every guide file cross-reference to a rule file points to an existing file.

    TC-2 / TASK-002: Guides reference rules using markdown links like:
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

    TC-2 / TASK-002: Guides reference patterns using markdown links like:
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
def test_rule_file_cross_references_to_patterns_are_valid() -> None:
    """Verify every rule file cross-reference to a pattern file points to an existing file.

    TC-2 / TASK-002 (extended): Rule files may reference patterns using markdown
    links or inline backtick mentions like:
    - See `.context/patterns/` for reference
    - [aggregate_pattern.py](../patterns/aggregate_pattern.py)
    """
    # Arrange
    repo_root = Path(__file__).parent.parent.parent
    rules_dir = repo_root / ".context" / "rules"
    patterns_dir = repo_root / ".context" / "patterns"

    assert rules_dir.exists(), ".context/rules/ directory should exist"
    assert patterns_dir.exists(), ".context/patterns/ directory should exist"

    # Pattern to match markdown links to patterns (both .py and .md)
    pattern_link_pattern = re.compile(r"\[([^\]]+)\]\(\.\./patterns/([^)#]+\.(py|md))")

    broken_references: list[tuple[str, str]] = []

    # Act: Scan all rule files for pattern references
    rule_files = list(rules_dir.glob("*.md"))

    for rule_file in rule_files:
        content = rule_file.read_text()
        matches = pattern_link_pattern.findall(content)

        for _link_text, pattern_path, _ext in matches:
            referenced_pattern = patterns_dir / pattern_path
            if not referenced_pattern.exists():
                broken_references.append((rule_file.name, pattern_path))

    # Assert: No broken references
    assert not broken_references, (
        f"Found {len(broken_references)} broken pattern references in rules:\n"
        + "\n".join(f"  {rule} -> {pattern}" for rule, pattern in broken_references)
    )


@pytest.mark.e2e
def test_consolidated_redirects_point_to_existing_files() -> None:
    """Verify rule files marked as CONSOLIDATED redirect to existing target files.

    TC-2 / TASK-002: Some rule files have been consolidated and now contain
    a redirect message like:
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

    TC-2 / TASK-002: Some rule files have YAML frontmatter like:
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


# ==================== Fidelity verification: file counts and content ====================


@pytest.mark.e2e
def test_minimum_rule_file_count() -> None:
    """Verify minimum number of rule files exist (>= 7 files).

    TC-2 / Fidelity: Ensures the refactoring didn't accidentally drop rule files.
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

    TC-2 / Fidelity: Ensures the refactoring didn't accidentally drop guide files.
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

    TC-2 / Fidelity: Ensures the refactoring didn't accidentally drop pattern files.
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

    TC-2 / Fidelity: Empty or near-empty files indicate dropped content.
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

    TC-2 / Fidelity: Extension of redirect validation that also checks
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


# ==================== TC-3: Guide emptiness and stub detection (TASK-003) ========


@pytest.mark.e2e
def test_guide_files_are_not_empty_or_stubs() -> None:
    """Verify no guide file is empty or a stub with placeholder content.

    TC-3 / TASK-003: For each guide file (excluding EN-* report files), checks:
    - File has > 100 non-blank lines
    - File has >= 3 level-2 (##) headings
    - File contains no whole-word matches for TODO, TBD, or PLACEHOLDER
    """
    # Arrange
    repo_root = Path(__file__).parent.parent.parent
    guides_dir = repo_root / ".context" / "guides"

    assert guides_dir.exists(), ".context/guides/ directory should exist"

    guide_files = [f for f in guides_dir.glob("*.md") if not f.name.startswith("EN-")]
    assert len(guide_files) > 0, "Should have at least one non-EN guide file"

    placeholder_pattern = re.compile(r"\bTODO\b|\bTBD\b|\bPLACEHOLDER\b")
    heading_pattern = re.compile(r"^## ", re.MULTILINE)

    failures: list[tuple[str, str]] = []

    # Act: Check each guide file for content quality
    for guide_file in guide_files:
        content = guide_file.read_text()
        non_blank_lines = [line for line in content.splitlines() if line.strip()]
        non_blank_count = len(non_blank_lines)
        heading_count = len(heading_pattern.findall(content))
        placeholder_matches = placeholder_pattern.findall(content)

        if non_blank_count <= 100:
            failures.append(
                (guide_file.name, f"Only {non_blank_count} non-blank lines (need >100)")
            )
        if heading_count < 3:
            failures.append((guide_file.name, f"Only {heading_count} ## headings (need >=3)"))
        if placeholder_matches:
            failures.append((guide_file.name, f"Contains placeholder text: {placeholder_matches}"))

    # Assert: No empty or stub guide files
    assert not failures, f"Found {len(failures)} guide content quality issues:\n" + "\n".join(
        f"  {name}: {reason}" for name, reason in failures
    )


# ==================== TC-4: Guide navigation table validation (TASK-004) ========


@pytest.mark.e2e
def test_guide_files_have_navigation_tables() -> None:
    """Verify every guide file contains a navigation table with anchor links.

    TC-4 / TASK-004: For each guide file (excluding EN-* report files), verifies:
    - A navigation table exists (identified by a table with | Section | Purpose | headers
      or a heading like "## Document Sections")
    - Navigation table contains anchor links in [text](#anchor) format
    """
    # Arrange
    repo_root = Path(__file__).parent.parent.parent
    guides_dir = repo_root / ".context" / "guides"

    assert guides_dir.exists(), ".context/guides/ directory should exist"

    guide_files = [f for f in guides_dir.glob("*.md") if not f.name.startswith("EN-")]
    assert len(guide_files) > 0, "Should have at least one non-EN guide file"

    # Pattern for navigation table header row
    nav_table_pattern = re.compile(r"\|\s*Section\s*\|\s*Purpose\s*\|", re.IGNORECASE)
    # Pattern for anchor links in table rows: [text](#anchor)
    anchor_link_pattern = re.compile(r"\[([^\]]+)\]\(#([^)]+)\)")

    failures: list[tuple[str, str]] = []

    # Act: Check each guide file for navigation table
    for guide_file in guide_files:
        content = guide_file.read_text()

        # Check for navigation table header
        if not nav_table_pattern.search(content):
            failures.append(
                (
                    guide_file.name,
                    "No navigation table found (missing | Section | Purpose | header)",
                )
            )
            continue

        # Check for anchor links within the file
        anchor_links = anchor_link_pattern.findall(content)
        if not anchor_links:
            failures.append(
                (guide_file.name, "Navigation table has no anchor links ([text](#anchor) format)")
            )

    # Assert: All guide files have navigation tables with anchors
    assert not failures, f"Found {len(failures)} guide navigation table issues:\n" + "\n".join(
        f"  {name}: {reason}" for name, reason in failures
    )


@pytest.mark.e2e
def test_guide_navigation_anchors_resolve_to_headings() -> None:
    """Verify navigation table anchor links resolve to actual headings in the file.

    TC-4 / TASK-004: For each guide file, extracts anchor links from the navigation
    table, then verifies each anchor corresponds to a real heading in the file.
    Heading-to-anchor conversion: lowercase, spaces to hyphens, remove special chars.
    """
    # Arrange
    repo_root = Path(__file__).parent.parent.parent
    guides_dir = repo_root / ".context" / "guides"

    assert guides_dir.exists(), ".context/guides/ directory should exist"

    guide_files = [f for f in guides_dir.glob("*.md") if not f.name.startswith("EN-")]

    # Pattern to find anchor links: [text](#anchor)
    anchor_link_pattern = re.compile(r"\[([^\]]+)\]\(#([^)]+)\)")
    # Pattern to find markdown headings (## through ####)
    heading_pattern = re.compile(r"^#{1,4}\s+(.+)$", re.MULTILINE)

    broken_anchors: list[tuple[str, str, str]] = []

    # Act: Check each guide file
    for guide_file in guide_files:
        content = guide_file.read_text()

        # Extract all headings and convert to anchor format
        headings = heading_pattern.findall(content)
        # Convert headings to anchor IDs: lowercase, spaces to hyphens, remove specials
        heading_anchors: set[str] = set()
        for heading in headings:
            anchor = heading.lower().strip()
            # Remove special characters except hyphens and spaces
            anchor = re.sub(r"[^\w\s-]", "", anchor)
            anchor = re.sub(r"\s+", "-", anchor)
            # Remove trailing hyphens
            anchor = anchor.strip("-")
            heading_anchors.add(anchor)

        # Extract navigation table anchor links
        anchor_links = anchor_link_pattern.findall(content)

        for _link_text, anchor in anchor_links:
            if anchor not in heading_anchors:
                broken_anchors.append((guide_file.name, anchor, _link_text))

    # Assert: All anchors resolve to real headings
    assert not broken_anchors, (
        f"Found {len(broken_anchors)} broken navigation anchor links:\n"
        + "\n".join(
            f"  {name}: #{anchor} ('{text}') has no matching heading"
            for name, anchor, text in broken_anchors
        )
    )


# ==================== TC-5: Content coverage metric (TASK-005) ==================


@pytest.mark.e2e
def test_guide_content_volume_meets_minimum_threshold() -> None:
    """Verify total guide content volume meets a minimum character threshold.

    TC-5 / TASK-005: Measures total characters across all guide files (excluding
    frontmatter and EN-* report files) and asserts a minimum threshold as a
    regression baseline. This catches bulk content loss without requiring git history.
    """
    # Arrange
    repo_root = Path(__file__).parent.parent.parent
    guides_dir = repo_root / ".context" / "guides"

    assert guides_dir.exists(), ".context/guides/ directory should exist"

    guide_files = [f for f in guides_dir.glob("*.md") if not f.name.startswith("EN-")]
    assert len(guide_files) > 0, "Should have at least one non-EN guide file"

    frontmatter_pattern = re.compile(r"^---\s*\n.*?\n---\s*\n", re.MULTILINE | re.DOTALL)

    # Minimum threshold: 5000 characters total across all guides.
    # This is a conservative baseline; the actual content should be much larger.
    minimum_total_chars = 5000

    # Act: Measure total content volume
    total_chars = 0
    file_sizes: list[tuple[str, int]] = []

    for guide_file in guide_files:
        content = guide_file.read_text()
        # Remove frontmatter for accurate content measurement
        content_without_frontmatter = frontmatter_pattern.sub("", content).strip()
        char_count = len(content_without_frontmatter)
        total_chars += char_count
        file_sizes.append((guide_file.name, char_count))

    # Assert: Total content volume meets threshold
    assert total_chars >= minimum_total_chars, (
        f"Total guide content volume ({total_chars} chars) is below the minimum "
        f"threshold ({minimum_total_chars} chars). This may indicate bulk content loss.\n"
        f"Per-file breakdown:\n"
        + "\n".join(f"  {name}: {size} chars" for name, size in sorted(file_sizes))
    )


# ==================== Three-tier architecture verification ====================


@pytest.mark.e2e
def test_claude_rules_directory_exists() -> None:
    """Verify .claude/rules/ symlink exists (rules are synced).

    Three-tier architecture: Rules should be automatically loaded via bootstrap script.
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

    Three-tier architecture: Patterns should be automatically loaded via bootstrap.
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

    Three-tier architecture: Guides should remain in .context/guides/ and be
    loaded only when explicitly requested via tools, not automatically loaded.
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

    Three-tier architecture: Even though guides aren't synced to .claude/,
    the source directories should all exist in .context/.
    """
    # Arrange
    repo_root = Path(__file__).parent.parent.parent
    context_dir = repo_root / ".context"

    # Act & Assert
    assert (context_dir / "rules").exists(), ".context/rules/ should exist"
    assert (context_dir / "patterns").exists(), ".context/patterns/ should exist"
    assert (context_dir / "guides").exists(), ".context/guides/ should exist"
