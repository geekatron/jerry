# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Canonicalize .jerry.prompt.md files from XML to markdown heading format.

Scans all skills/*/composition/*.jerry.prompt.md files and converts any that
contain XML-tagged sections (<identity>, <methodology>, etc.) to canonical
markdown ## Heading format using PromptTransformer.from_xml().

This is a one-time migration script for BUG-001: 21 of 68 canonical prompt
sources contain pre-existing XML tags that cause double-transform corruption
when the compose pipeline converts them to XML again.

Usage:
    uv run python scripts/canonicalize_prompt_sources.py [--dry-run]

References:
    - BUG-001: Broken XML nesting in composed agent files
    - agent-development-standards.md: Canonical source format
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Add project root to path for imports
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

from src.agents.domain.services.prompt_transformer import PromptTransformer  # noqa: E402

# XML section tags used in agent definitions (outside code blocks)
_KNOWN_XML_TAGS = {
    "identity",
    "purpose",
    "capabilities",
    "methodology",
    "guardrails",
    "output",
    "constitutional_compliance",
    "agent_version",
    "tool_tier",
    "enforcement",
    "portability",
    "prior_art",
    "session_context",
}

# Pattern to detect XML section tags outside code blocks
_XML_TAG_RE = re.compile(r"<(" + "|".join(_KNOWN_XML_TAGS) + r")(?:\s*/)?>\s*$", re.MULTILINE)


def _has_xml_sections(content: str) -> bool:
    """Detect if content has XML section tags outside code blocks.

    Args:
        content: File content to check.

    Returns:
        True if XML section tags found outside code blocks.
    """
    in_code_block = False
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if _XML_TAG_RE.match(stripped):
            return True
    return False


def canonicalize(skills_dir: Path, *, dry_run: bool = False) -> tuple[int, int, list[str]]:
    """Canonicalize all XML-format .jerry.prompt.md files to markdown headings.

    Args:
        skills_dir: Path to the skills/ directory.
        dry_run: If True, report but do not write.

    Returns:
        Tuple of (converted_count, already_canonical_count, converted_paths).
    """
    transformer = PromptTransformer()
    converted = 0
    already_canonical = 0
    converted_paths: list[str] = []

    prompt_files = sorted(skills_dir.glob("*/composition/*.jerry.prompt.md"))

    for prompt_file in prompt_files:
        content = prompt_file.read_text(encoding="utf-8")

        if _has_xml_sections(content):
            canonical = transformer.from_xml(content)

            if not dry_run:
                prompt_file.write_text(canonical, encoding="utf-8")

            converted += 1
            converted_paths.append(str(prompt_file.relative_to(skills_dir.parent)))
        else:
            already_canonical += 1

    return converted, already_canonical, converted_paths


def main() -> None:
    """Entry point for canonicalization script."""
    parser = argparse.ArgumentParser(
        description="Canonicalize .jerry.prompt.md files from XML to markdown heading format."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would be converted without writing.",
    )
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=_PROJECT_ROOT / "skills",
        help="Path to skills/ directory.",
    )
    args = parser.parse_args()

    if not args.skills_dir.is_dir():
        print(f"ERROR: Skills directory not found: {args.skills_dir}")
        sys.exit(1)

    prefix = "[DRY RUN] " if args.dry_run else ""
    print(f"{prefix}Scanning {args.skills_dir} for XML-format .jerry.prompt.md files...")

    converted, already_canonical, paths = canonicalize(args.skills_dir, dry_run=args.dry_run)

    if paths:
        print(f"\n{prefix}Converted {converted} files:")
        for path in paths:
            print(f"  - {path}")
    else:
        print(f"\n{prefix}No XML-format files found.")

    print(f"\nSummary: {converted} converted, {already_canonical} already canonical")

    if args.dry_run and converted > 0:
        print("\nRe-run without --dry-run to apply changes.")


if __name__ == "__main__":
    main()
