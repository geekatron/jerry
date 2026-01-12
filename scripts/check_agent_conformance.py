#!/usr/bin/env python3
"""
Jerry Framework - Agent Template Conformance Checker

This script validates that agent files conform to their respective templates.
It checks for required YAML frontmatter sections and reports deviations.

This script supports the Federated Template Architecture (ADR WI-SAO-009):
- Core template: skills/shared/AGENT_TEMPLATE_CORE.md
- PS extension: skills/problem-solving/agents/PS_EXTENSION.md
- NSE extension: skills/nasa-se/agents/NSE_EXTENSION.md
- Composition: scripts/compose_agent_template.py

Exit Codes:
    0: All agents conform to templates
    1: One or more agents have conformance issues
    2: Script error (file not found, parse error, etc.)

Usage:
    python scripts/check_agent_conformance.py                    # Check all agents
    python scripts/check_agent_conformance.py --family nse       # Check NSE agents only
    python scripts/check_agent_conformance.py --family ps        # Check PS agents only
    python scripts/check_agent_conformance.py --json             # Output as JSON
    python scripts/check_agent_conformance.py --verbose          # Show all checks
    python scripts/check_agent_conformance.py --validate-composition  # Validate template composition

Work Item: WI-SAO-024
Updated: WI-SAO-009 (Federated Template Architecture)
Created: 2026-01-11
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# Required YAML sections per template family
# Source: NSE_AGENT_TEMPLATE.md v1.0, PS_AGENT_TEMPLATE.md v2.0
REQUIRED_SECTIONS: dict[str, dict[str, list[str]]] = {
    "nse": {
        "top_level": [
            "name",
            "version",
            "description",
            "model",
            "identity",
            "persona",
            "capabilities",
            "guardrails",
            "output",
            "validation",
            "nasa_standards",
            "constitution",
            "enforcement",
            "session_context",
        ],
        "identity": ["role", "expertise", "cognitive_mode", "nasa_processes"],
        "persona": ["tone", "communication_style", "audience_level"],
        "capabilities": ["allowed_tools", "output_formats", "forbidden_actions"],
        "guardrails": ["input_validation", "output_filtering", "fallback_behavior"],
        "output": ["required", "location", "template", "levels"],
        "validation": ["file_must_exist", "disclaimer_required", "post_completion_checks"],
        "constitution": ["reference", "principles_applied"],
        "enforcement": ["tier", "escalation_path"],
        "session_context": [
            "schema",
            "schema_version",
            "input_validation",
            "output_validation",
            "on_receive",
            "on_send",
        ],
    },
    "ps": {
        "top_level": [
            "name",
            "version",
            "description",
            "model",
            "identity",
            "persona",
            "capabilities",
            "guardrails",
            "output",
            "validation",
            "prior_art",
            "constitution",
            "enforcement",
            "session_context",
        ],
        "identity": ["role", "expertise", "cognitive_mode"],
        "persona": ["tone", "communication_style", "audience_level"],
        "capabilities": ["allowed_tools", "output_formats", "forbidden_actions"],
        "guardrails": ["input_validation", "output_filtering", "fallback_behavior"],
        "output": ["required", "location", "template", "levels"],
        "validation": ["file_must_exist", "link_artifact_required", "post_completion_checks"],
        "constitution": ["reference", "principles_applied"],
        "enforcement": ["tier", "escalation_path"],
        "session_context": [
            "schema",
            "schema_version",
            "input_validation",
            "output_validation",
            "on_receive",
            "on_send",
        ],
    },
}

# Agent file patterns
AGENT_PATTERNS: dict[str, str] = {
    "nse": "skills/nasa-se/agents/nse-*.md",
    "ps": "skills/problem-solving/agents/ps-*.md",
}

# Files to exclude from checking (templates and extensions, not agents)
EXCLUDE_FILES: list[str] = [
    "NSE_AGENT_TEMPLATE.md",
    "PS_AGENT_TEMPLATE.md",
    "NSE_EXTENSION.md",
    "PS_EXTENSION.md",
    "AGENT_TEMPLATE_CORE.md",
]


@dataclass
class ConformanceIssue:
    """Represents a single conformance issue."""

    agent_file: str
    section: str
    issue_type: str  # "missing_section", "missing_field", "invalid_value"
    message: str
    severity: str = "error"  # "error", "warning"


@dataclass
class AgentConformanceResult:
    """Results of conformance check for a single agent."""

    agent_file: str
    family: str
    is_conformant: bool
    issues: list[ConformanceIssue] = field(default_factory=list)
    sections_checked: int = 0
    sections_passed: int = 0


def parse_yaml_frontmatter(content: str) -> dict[str, Any] | None:
    """Parse YAML frontmatter from markdown file.

    Args:
        content: Full file content

    Returns:
        Parsed YAML as dict, or None if no frontmatter found
    """
    # Match YAML frontmatter between --- delimiters
    # Must start at beginning of file
    pattern = r"^---\s*\n(.*?)\n---"
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        return None

    yaml_content = match.group(1)

    # Simple YAML parser for our specific format
    # We only need top-level keys and nested dicts/lists
    result: dict[str, Any] = {}
    current_key: str = ""

    lines = yaml_content.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]

        # Skip comments and empty lines
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue

        # Calculate indent level
        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        # Top-level key detection
        if indent == 0 and ":" in stripped:
            key_match = re.match(r"^([a-z_]+):\s*(.*)$", stripped)
            if key_match:
                current_key = key_match.group(1)
                value = key_match.group(2).strip()

                if value:
                    # Inline value
                    result[current_key] = value.strip('"\'')
                else:
                    # Start of nested structure
                    result[current_key] = {}

        # Nested key detection (under current top-level key)
        elif current_key and indent > 0:
            if isinstance(result.get(current_key), dict):
                nested_match = re.match(r"^([a-z_]+):\s*(.*)$", stripped)
                if nested_match:
                    nested_key = nested_match.group(1)
                    nested_value = nested_match.group(2).strip()
                    result[current_key][nested_key] = nested_value or True
            elif stripped.startswith("- "):
                # Array item
                if not isinstance(result.get(current_key), list):
                    result[current_key] = []
                item = stripped[2:].strip().strip('"\'')
                result[current_key].append(item)

        i += 1

    return result


def check_agent_conformance(
    agent_path: Path,
    family: str,
) -> AgentConformanceResult:
    """Check if an agent file conforms to its template.

    Args:
        agent_path: Path to agent markdown file
        family: Agent family ("nse" or "ps")

    Returns:
        AgentConformanceResult with findings
    """
    result = AgentConformanceResult(
        agent_file=str(agent_path),
        family=family,
        is_conformant=True,
    )

    # Read file
    try:
        content = agent_path.read_text()
    except Exception as e:
        result.is_conformant = False
        result.issues.append(
            ConformanceIssue(
                agent_file=str(agent_path),
                section="file",
                issue_type="read_error",
                message=f"Could not read file: {e}",
            )
        )
        return result

    # Parse YAML frontmatter
    yaml_data = parse_yaml_frontmatter(content)
    if yaml_data is None:
        result.is_conformant = False
        result.issues.append(
            ConformanceIssue(
                agent_file=str(agent_path),
                section="frontmatter",
                issue_type="missing_section",
                message="No YAML frontmatter found. Expected --- delimiters.",
            )
        )
        return result

    # Get required sections for this family
    requirements = REQUIRED_SECTIONS.get(family)
    if not requirements:
        result.issues.append(
            ConformanceIssue(
                agent_file=str(agent_path),
                section="config",
                issue_type="invalid_value",
                message=f"Unknown agent family: {family}",
                severity="warning",
            )
        )
        return result

    # Check top-level sections
    for section in requirements["top_level"]:
        result.sections_checked += 1
        if section not in yaml_data:
            result.is_conformant = False
            result.issues.append(
                ConformanceIssue(
                    agent_file=str(agent_path),
                    section=section,
                    issue_type="missing_section",
                    message=f"Missing required top-level section: {section}",
                )
            )
        else:
            result.sections_passed += 1

            # Check nested fields if section has nested requirements
            if section in requirements and section != "top_level":
                section_data = yaml_data.get(section, {})
                if isinstance(section_data, dict):
                    for nested_field in requirements[section]:
                        result.sections_checked += 1
                        if nested_field not in section_data:
                            result.is_conformant = False
                            result.issues.append(
                                ConformanceIssue(
                                    agent_file=str(agent_path),
                                    section=f"{section}.{nested_field}",
                                    issue_type="missing_field",
                                    message=f"Missing required field: {section}.{nested_field}",
                                )
                            )
                        else:
                            result.sections_passed += 1

    # Validate name format
    name = yaml_data.get("name", "")
    expected_prefix = f"{family}-"
    if not name.startswith(expected_prefix):
        result.is_conformant = False
        result.issues.append(
            ConformanceIssue(
                agent_file=str(agent_path),
                section="name",
                issue_type="invalid_value",
                message=f"Name '{name}' should start with '{expected_prefix}'",
            )
        )

    return result


def find_agent_files(project_root: Path, family: str | None = None) -> list[tuple[Path, str]]:
    """Find all agent files to check.

    Args:
        project_root: Project root directory
        family: Optional family filter ("nse", "ps", or None for all)

    Returns:
        List of (path, family) tuples
    """
    results: list[tuple[Path, str]] = []

    families_to_check = [family] if family else list(AGENT_PATTERNS.keys())

    for fam in families_to_check:
        pattern = AGENT_PATTERNS.get(fam, "")
        if not pattern:
            continue

        for agent_path in project_root.glob(pattern):
            # Skip excluded files
            if agent_path.name in EXCLUDE_FILES:
                continue
            results.append((agent_path, fam))

    return results


def format_results_text(results: list[AgentConformanceResult], verbose: bool = False) -> str:
    """Format results as human-readable text.

    Args:
        results: List of conformance results
        verbose: Include passing checks

    Returns:
        Formatted string
    """
    lines: list[str] = []
    lines.append("=" * 60)
    lines.append("Agent Template Conformance Report")
    lines.append("=" * 60)
    lines.append("")

    total_agents = len(results)
    passing_agents = sum(1 for r in results if r.is_conformant)
    failing_agents = total_agents - passing_agents

    lines.append(f"Summary: {passing_agents}/{total_agents} agents conformant")
    lines.append("")

    for result in results:
        agent_name = Path(result.agent_file).name
        status = "PASS" if result.is_conformant else "FAIL"
        icon = "✓" if result.is_conformant else "✗"

        lines.append(f"[{status}] {icon} {agent_name} ({result.family})")

        if result.issues:
            for issue in result.issues:
                severity_icon = "!" if issue.severity == "error" else "?"
                lines.append(f"       {severity_icon} {issue.section}: {issue.message}")

        if verbose and result.is_conformant:
            lines.append(f"       ✓ {result.sections_passed}/{result.sections_checked} sections passed")

        lines.append("")

    lines.append("=" * 60)

    if failing_agents > 0:
        lines.append(f"ACTION REQUIRED: Fix {failing_agents} non-conformant agent(s)")
        lines.append("See template files for required sections:")
        lines.append("  - skills/nasa-se/agents/NSE_AGENT_TEMPLATE.md")
        lines.append("  - skills/problem-solving/agents/PS_AGENT_TEMPLATE.md")
    else:
        lines.append("All agents conform to their templates.")

    return "\n".join(lines)


def format_results_json(results: list[AgentConformanceResult]) -> str:
    """Format results as JSON.

    Args:
        results: List of conformance results

    Returns:
        JSON string
    """
    data = {
        "summary": {
            "total_agents": len(results),
            "passing": sum(1 for r in results if r.is_conformant),
            "failing": sum(1 for r in results if not r.is_conformant),
        },
        "results": [
            {
                "agent_file": r.agent_file,
                "family": r.family,
                "is_conformant": r.is_conformant,
                "sections_checked": r.sections_checked,
                "sections_passed": r.sections_passed,
                "issues": [
                    {
                        "section": i.section,
                        "issue_type": i.issue_type,
                        "message": i.message,
                        "severity": i.severity,
                    }
                    for i in r.issues
                ],
            }
            for r in results
        ],
    }
    return json.dumps(data, indent=2)


def validate_composition(project_root: Path) -> tuple[bool, list[str]]:
    """Validate federated template composition.

    Runs composition script for both domains and verifies success.

    Args:
        project_root: Project root directory

    Returns:
        Tuple of (all_passed, messages)
    """
    import subprocess

    messages: list[str] = []
    all_passed = True

    compose_script = project_root / "scripts" / "compose_agent_template.py"
    if not compose_script.exists():
        messages.append(f"ERROR: Composition script not found: {compose_script}")
        return False, messages

    # Check core template exists
    core_template = project_root / "skills" / "shared" / "AGENT_TEMPLATE_CORE.md"
    if not core_template.exists():
        messages.append(f"ERROR: Core template not found: {core_template}")
        all_passed = False

    # Check extension files exist
    extensions = {
        "ps": project_root / "skills" / "problem-solving" / "agents" / "PS_EXTENSION.md",
        "nse": project_root / "skills" / "nasa-se" / "agents" / "NSE_EXTENSION.md",
    }

    for domain, path in extensions.items():
        if not path.exists():
            messages.append(f"ERROR: {domain.upper()} extension not found: {path}")
            all_passed = False

    if not all_passed:
        return False, messages

    # Validate composition for each domain
    for domain in ["ps", "nse"]:
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    str(compose_script),
                    "--domain",
                    domain,
                    "--validate",
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                messages.append(f"[PASS] {domain.upper()} composition validated")
            else:
                messages.append(f"[FAIL] {domain.upper()} composition failed")
                if result.stderr:
                    messages.append(f"       {result.stderr.strip()}")
                all_passed = False

        except subprocess.TimeoutExpired:
            messages.append(f"[FAIL] {domain.upper()} composition timed out")
            all_passed = False
        except Exception as e:
            messages.append(f"[FAIL] {domain.upper()} composition error: {e}")
            all_passed = False

    return all_passed, messages


def main() -> int:
    """Main entry point.

    Returns:
        Exit code (0 = all pass, 1 = failures, 2 = error)
    """
    parser = argparse.ArgumentParser(
        description="Check agent template conformance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/check_agent_conformance.py
  python scripts/check_agent_conformance.py --family nse
  python scripts/check_agent_conformance.py --json
  python scripts/check_agent_conformance.py --verbose
  python scripts/check_agent_conformance.py --validate-composition
        """,
    )
    parser.add_argument(
        "--family",
        choices=["nse", "ps"],
        help="Check only agents of this family",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show all checks including passing",
    )
    parser.add_argument(
        "--validate-composition",
        action="store_true",
        help="Validate template composition (federated architecture)",
    )

    args = parser.parse_args()

    # Determine project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # Handle --validate-composition mode
    if args.validate_composition:
        print("=" * 60)
        print("Federated Template Composition Validation")
        print("=" * 60)
        print()

        passed, messages = validate_composition(project_root)

        for msg in messages:
            print(msg)

        print()
        print("=" * 60)

        if passed:
            print("All composition checks passed.")
        else:
            print("Composition validation FAILED.")

        return 0 if passed else 1

    # Find agent files
    agent_files = find_agent_files(project_root, args.family)

    if not agent_files:
        print("No agent files found to check.", file=sys.stderr)
        return 2

    # Check each agent
    results: list[AgentConformanceResult] = []
    for agent_path, family in agent_files:
        result = check_agent_conformance(agent_path, family)
        results.append(result)

    # Output results
    if args.json:
        print(format_results_json(results))
    else:
        print(format_results_text(results, verbose=args.verbose))

    # Return exit code
    failing = sum(1 for r in results if not r.is_conformant)
    return 0 if failing == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
