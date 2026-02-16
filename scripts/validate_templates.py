#!/usr/bin/env python3
"""Validate adversarial strategy templates against TEMPLATE-FORMAT.md conformance.

This script validates all 10 adversarial strategy templates in .context/templates/adversarial/
against the canonical format defined in TEMPLATE-FORMAT.md.

Validation checks:
- All 8 canonical sections present in correct order (Identity, Purpose, Prerequisites,
  Execution Protocol, Output Format, Scoring Rubric, Examples, Integration)
- Navigation table present (H-23) with anchor links (H-24)
- Identity section has 7 required fields with valid Strategy ID from SSOT
- Identity section has Criticality Tier table
- Metadata blockquote present with Type or Status fields
- Purpose section has When to Use and When NOT to Use subheadings
- Execution Protocol has >= 4 steps
- Finding prefix matches expected format (2-letter uppercase + -NNN-{execution_id})
- Scoring Rubric has threshold bands table and dimension weights table
- Examples section has >= 200 chars of content
- Examples section has Before/After/Example structure
- Integration section has Criticality table with C1-C4 rows

Exit Codes:
    0: All templates pass validation
    1: One or more templates failed validation

References:
    - EN-818: Template Validation CI Gate
    - TEMPLATE-FORMAT.md: Canonical template format
    - quality-enforcement.md: SSOT for constants

Notes:
    - This script uses stdlib-only imports (argparse, re, sys, pathlib, typing) to avoid
      external dependencies and ensure it can run in CI without additional package installs.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

# ===========================================================================
# Constants
# ===========================================================================

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

IDENTITY_REQUIRED_FIELDS = [
    "Strategy ID",
    "Strategy Name",
    "Family",
    "Composite Score",
    "Finding Prefix",
    "Version",
    "Date",
]

# Valid Strategy IDs from quality-enforcement.md SSOT (10 selected strategies)
VALID_STRATEGY_IDS = {
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
}


# ===========================================================================
# Data Structures
# ===========================================================================


class ValidationResult(NamedTuple):
    """Result of a single validation check."""

    check_name: str
    passed: bool
    message: str | None = None


class TemplateValidation(NamedTuple):
    """Result of validating a single template."""

    template_path: Path
    passed: bool
    results: list[ValidationResult]


# ===========================================================================
# Helper Functions
# ===========================================================================


def get_project_root() -> Path:
    """Get the project root directory."""
    # Script is in scripts/, so go up one level
    return Path(__file__).parent.parent


def read_file(path: Path) -> str:
    """Read a file and return its content as a string."""
    return path.read_text(encoding="utf-8")


def extract_table_from_section(content: str, section_heading: str) -> str | None:
    """Extract a markdown table from a specific section.

    Args:
        content: Full markdown document content
        section_heading: Section name to search for (e.g., "Identity")

    Returns:
        First markdown table found in the section, or None if not found
    """
    # Find the section (try both "Section N: Name" and just "Name" formats)
    section_pattern = rf"^##\s+(?:Section \d+:\s+)?{re.escape(section_heading)}.*?(?=^##\s+|\Z)"
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
    """Parse a markdown table into a list of dictionaries.

    Args:
        table_text: Markdown table text

    Returns:
        List of dictionaries mapping header names to cell values
    """
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
# Validation Checks
# ===========================================================================


def check_all_sections_present(content: str) -> ValidationResult:
    """Check that all 8 canonical sections are present.

    Accepts both "Section N: Name" and "Name" heading formats.
    """
    # Extract all ## level headings
    headings = re.findall(r"^##\s+(.+)$", content, re.MULTILINE)

    missing_sections = []
    section_positions = {}
    for section in CANONICAL_SECTIONS:
        # Check for section name with or without "Section N:" prefix
        position = None
        for idx, heading in enumerate(headings):
            if section in heading or heading.endswith(f": {section}"):
                position = idx
                break

        if position is None:
            missing_sections.append(section)
        else:
            section_positions[section] = position

    if missing_sections:
        return ValidationResult(
            check_name="All 8 canonical sections",
            passed=False,
            message=f"Missing sections: {', '.join(missing_sections)}",
        )

    # Check section ordering (positions should be monotonically increasing)
    positions = [section_positions[section] for section in CANONICAL_SECTIONS]
    if positions != sorted(positions):
        return ValidationResult(
            check_name="All 8 canonical sections",
            passed=False,
            message="Sections are not in canonical order",
        )

    return ValidationResult(
        check_name="All 8 canonical sections",
        passed=True,
        message="All sections present and in order",
    )


def check_navigation_table(content: str) -> ValidationResult:
    """Check for navigation table with anchor links (H-23, H-24)."""
    # Check for navigation table (usually "Document Sections")
    nav_section_match = re.search(
        r"^##\s+Document Sections.*?\n(.*?)(?=^##|\Z)", content, re.MULTILINE | re.DOTALL
    )

    if nav_section_match is None:
        return ValidationResult(
            check_name="Navigation table (H-23)",
            passed=False,
            message="Missing 'Document Sections' navigation table",
        )

    nav_content = nav_section_match.group(1)

    # Check for anchor links in navigation table
    anchor_links = re.findall(r"\[.+?\]\(#.+?\)", nav_content)

    if len(anchor_links) < len(CANONICAL_SECTIONS) - 1:
        return ValidationResult(
            check_name="Navigation anchor links (H-24)",
            passed=False,
            message=f"Navigation table has {len(anchor_links)} anchor links, "
            f"expected >= {len(CANONICAL_SECTIONS) - 1}",
        )

    return ValidationResult(
        check_name="Navigation table (H-23/H-24)",
        passed=True,
        message=f"Navigation table with {len(anchor_links)} anchor links",
    )


def check_identity_fields(content: str) -> ValidationResult:
    """Check that Identity section has 7 required fields and valid Strategy ID."""
    # Extract Identity section table (try both formats)
    identity_table = extract_table_from_section(content, "Identity")
    if identity_table is None:
        identity_table = extract_table_from_section(content, "Section 1: Identity")

    if identity_table is None:
        return ValidationResult(
            check_name="Identity section fields",
            passed=False,
            message="No table found in Identity section",
        )

    # Parse the table
    rows = parse_markdown_table(identity_table)
    fields = {row.get("Field", ""): row.get("Value", "") for row in rows}

    # Check required fields
    missing_fields = [field for field in IDENTITY_REQUIRED_FIELDS if field not in fields]

    if missing_fields:
        return ValidationResult(
            check_name="Identity section fields",
            passed=False,
            message=f"Missing Identity fields: {', '.join(missing_fields)}",
        )

    # Validate Strategy ID against SSOT
    strategy_id = fields.get("Strategy ID", "")
    if strategy_id not in VALID_STRATEGY_IDS:
        return ValidationResult(
            check_name="Identity section fields",
            passed=False,
            message=f"Strategy ID '{strategy_id}' not in SSOT (expected one of {sorted(VALID_STRATEGY_IDS)})",
        )

    return ValidationResult(
        check_name="Identity section fields",
        passed=True,
        message="All 7 required fields present with valid Strategy ID",
    )


def check_criticality_tier_table(content: str) -> ValidationResult:
    """Check that Identity section has Criticality Tier table."""
    # Extract Identity section
    identity_section_match = re.search(
        r"^##\s+(?:Section 1:\s+)?Identity.*?(?=^##\s+|\Z)", content, re.MULTILINE | re.DOTALL
    )

    if identity_section_match is None:
        return ValidationResult(
            check_name="Criticality Tier table",
            passed=False,
            message="Identity section not found",
        )

    identity_content = identity_section_match.group(0)

    # Look for Criticality Tier table or heading
    has_criticality = (
        "Criticality Tier" in identity_content or "criticality tier" in identity_content
    )

    if not has_criticality:
        return ValidationResult(
            check_name="Criticality Tier table",
            passed=False,
            message="Criticality Tier table not found in Identity section",
        )

    return ValidationResult(
        check_name="Criticality Tier table",
        passed=True,
        message="Criticality Tier table present",
    )


def check_execution_protocol_steps(content: str) -> ValidationResult:
    """Check that Execution Protocol has >= 4 steps."""
    # Extract Execution Protocol section (try both formats)
    protocol_match = re.search(
        r"^##\s+(?:Section 4:\s+)?Execution Protocol.*?(?=^##\s+|\Z)",
        content,
        re.MULTILINE | re.DOTALL,
    )

    if protocol_match is None:
        return ValidationResult(
            check_name="Execution Protocol steps",
            passed=False,
            message="Execution Protocol section not found",
        )

    protocol_content = protocol_match.group(0)

    # Count step headings (### Step N:)
    step_headings = re.findall(r"^###\s+Step\s+\d+:", protocol_content, re.MULTILINE)

    if len(step_headings) < 4:
        return ValidationResult(
            check_name="Execution Protocol steps",
            passed=False,
            message=f"Found {len(step_headings)} steps, expected >= 4",
        )

    return ValidationResult(
        check_name="Execution Protocol steps",
        passed=True,
        message=f"{len(step_headings)} steps present",
    )


def check_finding_prefix_format(content: str) -> ValidationResult:
    """Check that Finding Prefix matches expected format (XX-NNN-{execution_id})."""
    # Extract Identity section table
    identity_table = extract_table_from_section(content, "Identity")
    if identity_table is None:
        identity_table = extract_table_from_section(content, "Section 1: Identity")

    if identity_table is None:
        return ValidationResult(
            check_name="Finding Prefix format",
            passed=False,
            message="No Identity table found",
        )

    rows = parse_markdown_table(identity_table)
    fields = {row.get("Field", ""): row.get("Value", "") for row in rows}

    finding_prefix = fields.get("Finding Prefix", "")

    # Check format: XX-NNN-{execution_id} where XX is 2 uppercase letters
    pattern = r"^[A-Z]{2}-NNN-\{execution_id\}$"
    if not re.match(pattern, finding_prefix):
        return ValidationResult(
            check_name="Finding Prefix format",
            passed=False,
            message=f"Finding Prefix '{finding_prefix}' does not match expected format "
            f"'XX-NNN-{{execution_id}}'",
        )

    return ValidationResult(
        check_name="Finding Prefix format",
        passed=True,
        message=f"Valid format: {finding_prefix}",
    )


def check_scoring_rubric_tables(content: str) -> ValidationResult:
    """Check that Scoring Rubric has threshold bands and dimension weights tables."""
    # Extract Scoring Rubric section
    rubric_match = re.search(
        r"^##\s+(?:Section 6:\s+)?Scoring Rubric.*?(?=^##\s+|\Z)",
        content,
        re.MULTILINE | re.DOTALL,
    )

    if rubric_match is None:
        return ValidationResult(
            check_name="Scoring Rubric tables",
            passed=False,
            message="Scoring Rubric section not found",
        )

    rubric_content = rubric_match.group(0)

    # Check for threshold bands
    has_threshold_bands = "Threshold Bands" in rubric_content or "threshold bands" in rubric_content

    # Check for dimension weights
    has_dimension_weights = (
        "Dimension Weights" in rubric_content
        or "dimension weights" in rubric_content
        or ("Dimension" in rubric_content and "Weight" in rubric_content)
    )

    missing = []
    if not has_threshold_bands:
        missing.append("Threshold Bands")
    if not has_dimension_weights:
        missing.append("Dimension Weights")

    if missing:
        return ValidationResult(
            check_name="Scoring Rubric tables",
            passed=False,
            message=f"Missing tables: {', '.join(missing)}",
        )

    return ValidationResult(
        check_name="Scoring Rubric tables",
        passed=True,
        message="Threshold bands and dimension weights present",
    )


def check_examples_content(content: str) -> ValidationResult:
    """Check that Examples section has >= 200 chars of content."""
    # Extract Examples section (try both formats)
    examples_match = re.search(
        r"^##\s+(?:Section 7:\s+)?Examples.*?(?=^##\s+|\Z)", content, re.MULTILINE | re.DOTALL
    )

    if examples_match is None:
        return ValidationResult(
            check_name="Examples section content",
            passed=False,
            message="Examples section not found",
        )

    examples_content = examples_match.group(0)

    # Remove the section heading for character count
    examples_text = re.sub(r"^##\s+.*?\n", "", examples_content, count=1)

    if len(examples_text) < 200:
        return ValidationResult(
            check_name="Examples section content",
            passed=False,
            message=f"Examples section has {len(examples_text)} chars, expected >= 200",
        )

    return ValidationResult(
        check_name="Examples section content",
        passed=True,
        message=f"{len(examples_text)} chars of content",
    )


def check_metadata_blockquote(content: str) -> ValidationResult:
    """Check that template contains a metadata blockquote with required fields."""
    # Look for blockquote pattern with Type or Status metadata
    has_type_metadata = re.search(r"^>\s+\*\*Type:\*\*", content, re.MULTILINE)
    has_status_metadata = re.search(r"^>\s+\*\*Status:\*\*", content, re.MULTILINE)

    if not (has_type_metadata or has_status_metadata):
        return ValidationResult(
            check_name="Metadata blockquote",
            passed=False,
            message="No metadata blockquote found with Type or Status fields",
        )

    return ValidationResult(
        check_name="Metadata blockquote",
        passed=True,
        message="Metadata blockquote present",
    )


def check_purpose_section_content(content: str) -> ValidationResult:
    """Check that Purpose section has 'When to Use' and 'When NOT to Use' subheadings."""
    # Extract Purpose section
    purpose_match = re.search(
        r"^##\s+(?:Section 2:\s+)?Purpose.*?(?=^##\s+|\Z)", content, re.MULTILINE | re.DOTALL
    )

    if purpose_match is None:
        return ValidationResult(
            check_name="Purpose section content",
            passed=False,
            message="Purpose section not found",
        )

    purpose_content = purpose_match.group(0)

    # Check for "When to Use" and "When NOT to Use" subheadings
    has_when_to_use = re.search(r"^###\s+When to Use", purpose_content, re.MULTILINE)
    has_when_not_to_use = re.search(r"^###\s+When NOT to Use", purpose_content, re.MULTILINE)

    missing = []
    if not has_when_to_use:
        missing.append("When to Use")
    if not has_when_not_to_use:
        missing.append("When NOT to Use")

    if missing:
        return ValidationResult(
            check_name="Purpose section content",
            passed=False,
            message=f"Missing subheadings: {', '.join(missing)}",
        )

    return ValidationResult(
        check_name="Purpose section content",
        passed=True,
        message="When to Use and When NOT to Use present",
    )


def check_integration_section_content(content: str) -> ValidationResult:
    """Check that Integration section has a Criticality table with C1-C4 rows."""
    # Extract Integration section
    integration_match = re.search(
        r"^##\s+(?:Section 8:\s+)?Integration.*?(?=^##\s+|\Z)", content, re.MULTILINE | re.DOTALL
    )

    if integration_match is None:
        return ValidationResult(
            check_name="Integration section content",
            passed=False,
            message="Integration section not found",
        )

    integration_content = integration_match.group(0)

    # Check for Criticality table with C1-C4 rows
    has_c1 = "C1" in integration_content
    has_c2 = "C2" in integration_content
    has_c3 = "C3" in integration_content
    has_c4 = "C4" in integration_content

    if not (has_c1 and has_c2 and has_c3 and has_c4):
        return ValidationResult(
            check_name="Integration section content",
            passed=False,
            message="Criticality table missing C1-C4 rows",
        )

    return ValidationResult(
        check_name="Integration section content",
        passed=True,
        message="Criticality table with C1-C4 present",
    )


def check_examples_section_structure(content: str) -> ValidationResult:
    """Check that Examples section has Before/After/Example structure."""
    # Extract Examples section
    examples_match = re.search(
        r"^##\s+(?:Section 7:\s+)?Examples.*?(?=^##\s+|\Z)", content, re.MULTILINE | re.DOTALL
    )

    if examples_match is None:
        return ValidationResult(
            check_name="Examples section structure",
            passed=False,
            message="Examples section not found",
        )

    examples_content = examples_match.group(0)

    # Check for Before/After/Example indicators
    has_before = "Before" in examples_content or "before" in examples_content
    has_after = "After" in examples_content or "after" in examples_content
    has_example = "Example" in examples_content or "example" in examples_content

    if not (has_before or has_after or has_example):
        return ValidationResult(
            check_name="Examples section structure",
            passed=False,
            message="No Before/After/Example content found",
        )

    return ValidationResult(
        check_name="Examples section structure",
        passed=True,
        message="Before/After/Example content present",
    )


# ===========================================================================
# Template Validation
# ===========================================================================


def validate_template(template_path: Path) -> TemplateValidation:
    """Validate a single template file.

    Args:
        template_path: Path to template file

    Returns:
        TemplateValidation result
    """
    if not template_path.exists():
        return TemplateValidation(
            template_path=template_path,
            passed=False,
            results=[
                ValidationResult(
                    check_name="File exists",
                    passed=False,
                    message="Template file not found",
                )
            ],
        )

    content = read_file(template_path)

    # Run all validation checks
    checks = [
        check_all_sections_present(content),
        check_navigation_table(content),
        check_identity_fields(content),
        check_criticality_tier_table(content),
        check_execution_protocol_steps(content),
        check_finding_prefix_format(content),
        check_scoring_rubric_tables(content),
        check_examples_content(content),
        check_metadata_blockquote(content),
        check_purpose_section_content(content),
        check_integration_section_content(content),
        check_examples_section_structure(content),
    ]

    all_passed = all(check.passed for check in checks)

    return TemplateValidation(
        template_path=template_path,
        passed=all_passed,
        results=checks,
    )


def find_template_files(templates_dir: Path) -> list[Path]:
    """Find all template files in the adversarial templates directory.

    Excludes TEMPLATE-FORMAT.md.

    Args:
        templates_dir: Path to templates directory

    Returns:
        List of template file paths
    """
    if not templates_dir.exists():
        return []

    return [f for f in sorted(templates_dir.glob("*.md")) if f.name != "TEMPLATE-FORMAT.md"]


# ===========================================================================
# Main
# ===========================================================================


def main() -> int:
    """Main entry point for template validation."""
    parser = argparse.ArgumentParser(
        description="Validate adversarial strategy templates against TEMPLATE-FORMAT.md"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed validation results for each template",
    )

    args = parser.parse_args()

    project_root = get_project_root()
    templates_dir = project_root / ".context" / "templates" / "adversarial"

    # Find all template files
    template_files = find_template_files(templates_dir)

    if not template_files:
        print(f"ERROR: No template files found in {templates_dir}")
        return 1

    print(f"Validating {len(template_files)} template files...")
    print()

    # Validate each template
    all_passed = True
    validations = []
    for template_path in template_files:
        validation = validate_template(template_path)
        validations.append(validation)

        # Print template status
        status = "PASS" if validation.passed else "FAIL"
        print(f"[{status}] {template_path.name}")

        if args.verbose or not validation.passed:
            for result in validation.results:
                status_symbol = "✓" if result.passed else "✗"
                message = f" - {result.message}" if result.message else ""
                print(f"  {status_symbol} {result.check_name}{message}")

        if not validation.passed:
            all_passed = False

        if args.verbose or not validation.passed:
            print()

    # Print summary
    passed_count = sum(1 for v in validations if v.passed)
    failed_count = len(template_files) - passed_count

    print("=" * 60)
    print(f"Summary: {passed_count} passed, {failed_count} failed")
    print("=" * 60)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
