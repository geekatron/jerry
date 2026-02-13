#!/usr/bin/env python3
"""
Jerry Framework - Agent Template Composition Script

This script composes complete agent templates by merging the shared core template
with domain-specific extensions. It implements the Federated Template Architecture
approved in ADR WI-SAO-009-ADR-001.

The script:
1. Loads AGENT_TEMPLATE_CORE.md (~73% shared content)
2. Loads domain extension (PS_EXTENSION.md or NSE_EXTENSION.md)
3. Replaces 9 extension points with domain-specific content
4. Outputs composed template

Exit Codes:
    0: Composition successful
    1: Validation error (remaining placeholders)
    2: Script error (file not found, parse error, etc.)

Usage:
    python scripts/compose_agent_template.py --domain ps     # Compose PS template
    python scripts/compose_agent_template.py --domain nse    # Compose NSE template
    python scripts/compose_agent_template.py --domain ps --output skills/problem-solving/agents/PS_AGENT_TEMPLATE.md
    python scripts/compose_agent_template.py --domain ps --validate  # Validate only
    python scripts/compose_agent_template.py --domain ps --diff      # Compare with existing

Work Item: WI-SAO-009, Task T-009.4
ADR: decisions/wi-sao-009-adr-unified-template-architecture.md
Created: 2026-01-11
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Extension point names (order matters for documentation)
EXTENSION_POINTS: list[str] = [
    "DOMAIN_NAME_PREFIX",
    "DOMAIN_IDENTITY_EXTENSION",
    "DOMAIN_FORBIDDEN_ACTIONS",
    "DOMAIN_INPUT_VALIDATION",
    "DOMAIN_OUTPUT_FILTERING",
    "DOMAIN_VALIDATION_FIELDS",
    "DOMAIN_REFERENCES",
    "DOMAIN_PRINCIPLES",
    "DOMAIN_XML_SECTIONS",
]

# Domain configuration
DOMAIN_CONFIG: dict[str, dict[str, str]] = {
    "ps": {
        "name": "Problem-Solving",
        "extension_file": "skills/problem-solving/agents/PS_EXTENSION.md",
        "output_file": "skills/problem-solving/agents/PS_AGENT_TEMPLATE.md",
    },
    "nse": {
        "name": "NASA Systems Engineering",
        "extension_file": "skills/nasa-se/agents/NSE_EXTENSION.md",
        "output_file": "skills/nasa-se/agents/NSE_AGENT_TEMPLATE.md",
    },
}

# Core template path
CORE_TEMPLATE_PATH = "skills/shared/AGENT_TEMPLATE_CORE.md"


@dataclass
class ExtensionPoint:
    """Represents a parsed extension point from the extension file."""

    name: str
    content: str
    line_number: int = 0


@dataclass
class CompositionResult:
    """Result of template composition."""

    success: bool
    composed_content: str = ""
    extension_points_found: int = 0
    extension_points_replaced: int = 0
    remaining_placeholders: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def parse_extension_file(content: str) -> dict[str, ExtensionPoint]:
    """Parse extension points from a domain extension file.

    The extension file format uses markdown headers and code blocks:
        ### {%DOMAIN_NAME_PREFIX%}

        ```
        ps
        ```

    Args:
        content: Full content of extension file

    Returns:
        Dict mapping extension point names to their content
    """
    extension_points: dict[str, ExtensionPoint] = {}

    # Pattern to match extension point headers and their code blocks
    # Format: ### {%EXTENSION_NAME%}\n\n```[language]\ncontent\n```
    pattern = re.compile(
        r"###\s*\{%(\w+)%\}\s*\n+"  # Header with extension name
        r"```(?:\w+)?\s*\n"  # Opening code fence (optional language)
        r"(.*?)"  # Content (non-greedy)
        r"\n```",  # Closing code fence
        re.DOTALL,
    )

    for match in pattern.finditer(content):
        name = match.group(1)
        raw_content = match.group(2)

        # Find line number for debugging
        line_number = content[: match.start()].count("\n") + 1

        # Clean up the content
        # - Remove leading/trailing whitespace from each line while preserving indentation
        # - Handle empty content (comments only)
        lines = raw_content.splitlines()
        cleaned_lines: list[str] = []

        for line in lines:
            # Skip lines that are only comments
            stripped = line.strip()
            if stripped.startswith("#") and not stripped.startswith("##"):
                # YAML comment - include it for documentation
                cleaned_lines.append(line)
            else:
                cleaned_lines.append(line)

        cleaned_content = "\n".join(cleaned_lines)

        # If content is only comments, make it empty for cleaner replacement
        content_without_comments = re.sub(r"^\s*#.*$", "", cleaned_content, flags=re.MULTILINE)
        if not content_without_comments.strip():
            cleaned_content = ""

        extension_points[name] = ExtensionPoint(
            name=name,
            content=cleaned_content.rstrip(),
            line_number=line_number,
        )

    return extension_points


def compose_template(
    core_content: str,
    extension_points: dict[str, ExtensionPoint],
) -> CompositionResult:
    """Compose a complete template by replacing extension points.

    Args:
        core_content: Content of AGENT_TEMPLATE_CORE.md
        extension_points: Parsed extension points from domain extension

    Returns:
        CompositionResult with composed content and statistics
    """
    result = CompositionResult(success=True, composed_content=core_content)
    result.extension_points_found = len(extension_points)

    # Replace each extension point
    for point_name in EXTENSION_POINTS:
        placeholder = "{%" + point_name + "%}"

        if point_name in extension_points:
            ext_point = extension_points[point_name]
            content = ext_point.content

            # Count occurrences before replacement
            occurrences = result.composed_content.count(placeholder)

            if occurrences == 0:
                result.warnings.append(
                    f"Extension point '{point_name}' defined but not found in core template"
                )
            else:
                # Perform replacement
                result.composed_content = result.composed_content.replace(placeholder, content)
                result.extension_points_replaced += occurrences
        else:
            # Check if placeholder exists in template
            if placeholder in result.composed_content:
                result.remaining_placeholders.append(point_name)
                result.errors.append(f"Extension point '{point_name}' not found in extension file")
                result.success = False

    # Check for any remaining placeholders (including custom ones)
    remaining_pattern = re.compile(r"\{%(\w+)%\}")
    for match in remaining_pattern.finditer(result.composed_content):
        point_name = match.group(1)
        if point_name not in result.remaining_placeholders:
            result.remaining_placeholders.append(point_name)
            result.success = False

    if result.remaining_placeholders:
        result.errors.append(
            f"Remaining placeholders after composition: {result.remaining_placeholders}"
        )

    return result


def validate_composition(composed_content: str) -> list[str]:
    """Validate that composed template is well-formed.

    Args:
        composed_content: Composed template content

    Returns:
        List of validation errors (empty if valid)
    """
    errors: list[str] = []

    # Check for YAML frontmatter
    if not composed_content.startswith("---"):
        # Skip header comment/title and check for frontmatter
        lines = composed_content.splitlines()
        yaml_start = -1
        for i, line in enumerate(lines):
            if line.strip() == "---":
                yaml_start = i
                break

        if yaml_start == -1:
            errors.append("No YAML frontmatter found (expected --- delimiter)")

    # Check for XML agent body
    if "<agent>" not in composed_content:
        errors.append("No <agent> XML block found in body")

    if "</agent>" not in composed_content:
        errors.append("No closing </agent> tag found")

    # Check for required XML sections
    required_sections = [
        "<identity>",
        "<persona>",
        "<capabilities>",
        "<guardrails>",
        "<constitutional_compliance>",
        "<invocation_protocol>",
        "<output_levels>",
        "<state_management>",
    ]

    for section in required_sections:
        if section not in composed_content:
            errors.append(f"Missing required XML section: {section}")

    # Check for remaining placeholders with curly braces
    placeholder_pattern = re.compile(r"\{%\w+%\}")
    placeholders = placeholder_pattern.findall(composed_content)
    if placeholders:
        errors.append(f"Remaining extension point placeholders: {placeholders}")

    # Note: Template placeholders like {agent-type} are expected
    # These are for agent creators to fill in, not errors

    return errors


def generate_diff(original: str, composed: str, filename: str) -> str:
    """Generate unified diff between original and composed content.

    Args:
        original: Original file content
        composed: Composed content
        filename: Name for diff header

    Returns:
        Unified diff string
    """
    original_lines = original.splitlines(keepends=True)
    composed_lines = composed.splitlines(keepends=True)

    diff = difflib.unified_diff(
        original_lines,
        composed_lines,
        fromfile=f"a/{filename}",
        tofile=f"b/{filename}",
        lineterm="",
    )

    return "".join(diff)


def format_report(
    result: CompositionResult,
    domain: str,
    validate_only: bool = False,
) -> str:
    """Format composition result as human-readable report.

    Args:
        result: Composition result
        domain: Domain name (ps, nse)
        validate_only: Whether this was validate-only mode

    Returns:
        Formatted report string
    """
    lines: list[str] = []
    lines.append("=" * 60)
    lines.append(f"Agent Template Composition Report - {domain.upper()}")
    lines.append("=" * 60)
    lines.append("")

    status = "SUCCESS" if result.success else "FAILED"
    icon = "✓" if result.success else "✗"
    lines.append(f"Status: [{status}] {icon}")
    lines.append("")

    lines.append("Statistics:")
    lines.append(f"  Extension points defined: {result.extension_points_found}")
    lines.append(f"  Placeholders replaced: {result.extension_points_replaced}")
    lines.append(f"  Remaining placeholders: {len(result.remaining_placeholders)}")
    lines.append("")

    if result.warnings:
        lines.append("Warnings:")
        for warning in result.warnings:
            lines.append(f"  ? {warning}")
        lines.append("")

    if result.errors:
        lines.append("Errors:")
        for error in result.errors:
            lines.append(f"  ! {error}")
        lines.append("")

    if validate_only:
        lines.append("Mode: Validate only (no output written)")
    else:
        lines.append("Output: Composed template ready")

    lines.append("=" * 60)

    return "\n".join(lines)


def main() -> int:
    """Main entry point.

    Returns:
        Exit code (0 = success, 1 = validation error, 2 = script error)
    """
    parser = argparse.ArgumentParser(
        description="Compose agent templates from core + domain extension",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/compose_agent_template.py --domain ps
  python scripts/compose_agent_template.py --domain nse --output my_template.md
  python scripts/compose_agent_template.py --domain ps --validate
  python scripts/compose_agent_template.py --domain nse --diff
        """,
    )
    parser.add_argument(
        "--domain",
        choices=["ps", "nse"],
        required=True,
        help="Domain to compose template for",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output file path (defaults to stdout or domain default)",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate composition without writing output",
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="Show diff against existing template file",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress report output (just write template)",
    )
    parser.add_argument(
        "--write-default",
        "-w",
        action="store_true",
        help="Write to default output location for domain",
    )

    args = parser.parse_args()

    # Determine project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # Get domain config
    config = DOMAIN_CONFIG[args.domain]

    # Load core template
    core_path = project_root / CORE_TEMPLATE_PATH
    if not core_path.exists():
        print(f"Error: Core template not found: {core_path}", file=sys.stderr)
        return 2

    try:
        core_content = core_path.read_text()
    except Exception as e:
        print(f"Error reading core template: {e}", file=sys.stderr)
        return 2

    # Load extension file
    extension_path = project_root / config["extension_file"]
    if not extension_path.exists():
        print(f"Error: Extension file not found: {extension_path}", file=sys.stderr)
        return 2

    try:
        extension_content = extension_path.read_text()
    except Exception as e:
        print(f"Error reading extension file: {e}", file=sys.stderr)
        return 2

    # Parse extension points
    extension_points = parse_extension_file(extension_content)

    if not extension_points:
        print("Error: No extension points found in extension file", file=sys.stderr)
        return 2

    # Compose template
    result = compose_template(core_content, extension_points)

    # Validate composition
    validation_errors = validate_composition(result.composed_content)
    if validation_errors:
        result.success = False
        result.errors.extend(validation_errors)

    # Print report
    if not args.quiet:
        report = format_report(result, args.domain, args.validate)
        print(report, file=sys.stderr)

    # Handle diff mode
    if args.diff:
        default_output = project_root / config["output_file"]
        if default_output.exists():
            original = default_output.read_text()
            diff_output = generate_diff(original, result.composed_content, config["output_file"])
            if diff_output:
                print("\nDiff against existing template:")
                print(diff_output)
            else:
                print("\nNo differences found.")
        else:
            print(f"\nNo existing template to compare: {default_output}")

    # Handle output
    if not args.validate and result.success:
        if args.output:
            output_path = Path(args.output)
            if not output_path.is_absolute():
                output_path = project_root / output_path
            output_path.write_text(result.composed_content)
            if not args.quiet:
                print(f"\nWritten to: {output_path}", file=sys.stderr)
        elif args.write_default:
            output_path = project_root / config["output_file"]
            output_path.write_text(result.composed_content)
            if not args.quiet:
                print(f"\nWritten to: {output_path}", file=sys.stderr)
        elif not args.diff and args.quiet:
            # Quiet mode without output flag: write to stdout
            print(result.composed_content)

    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
