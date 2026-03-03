#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Pre-commit hook: Skill schema validation for Jerry Framework.

Validates SKILL.md frontmatter against the Anthropic skill schema and
skill.jerry.yaml canonical source files against the skill canonical schema.

Modes:
    - Default (pre-commit): Only validates staged files matching skill patterns.
    - --all (CI): Validates all skill files in the repository.

Exit Codes:
    0 - No violations found (or no matching files)
    1 - Schema violations found (commit should be blocked)

References:
    - PROJ-012: Skill Composition Pipeline
    - Phase 5: Pre-Commit Hook + CI Gate
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print("ERROR: jsonschema is required. Run: uv add jsonschema")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).resolve().parent.parent

_ANTHROPIC_SCHEMA_PATH = (
    _REPO_ROOT / "docs" / "schemas" / "anthropic-skill-frontmatter-v1.schema.json"
)
_CANONICAL_SCHEMA_PATH = _REPO_ROOT / "docs" / "schemas" / "skill-canonical-v1.schema.json"

_SKILL_MD_PATTERN = re.compile(r"^skills/[^/]+/SKILL\.md$")
_CANONICAL_YAML_PATTERN = re.compile(r"^skills/[^/]+/composition/skill\.jerry\.yaml$")


# ---------------------------------------------------------------------------
# Schema loading
# ---------------------------------------------------------------------------


def load_schema(schema_path: Path) -> dict | None:
    """Load a JSON Schema file.

    Args:
        schema_path: Path to the JSON Schema file.

    Returns:
        Parsed schema dict, or None if the file cannot be loaded.
    """
    if not schema_path.exists():
        print(f"WARNING: Schema not found: {schema_path}")
        return None

    try:
        return json.loads(schema_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(f"WARNING: Failed to load schema {schema_path}: {exc}")
        return None


# ---------------------------------------------------------------------------
# SKILL.md frontmatter parsing
# ---------------------------------------------------------------------------


def parse_skill_md_frontmatter(file_path: Path) -> dict | None:
    """Parse YAML frontmatter from a SKILL.md file.

    Extracts the content between the first pair of ``---`` delimiters
    and parses it as YAML.

    Args:
        file_path: Path to the SKILL.md file.

    Returns:
        Parsed frontmatter dict, or None if no valid frontmatter found.
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None

    if not content.startswith("---"):
        return None

    # Find closing delimiter
    end_idx = content.find("\n---", 3)
    if end_idx == -1:
        return None

    frontmatter_str = content[4:end_idx]
    try:
        data = yaml.safe_load(frontmatter_str)
        return data if isinstance(data, dict) else None
    except yaml.YAMLError:
        return None


# ---------------------------------------------------------------------------
# Canonical YAML loading
# ---------------------------------------------------------------------------


def load_canonical_yaml(file_path: Path) -> dict | None:
    """Load and parse a skill.jerry.yaml canonical source file.

    Args:
        file_path: Path to the skill.jerry.yaml file.

    Returns:
        Parsed YAML dict, or None if the file cannot be loaded.
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None

    try:
        data = yaml.safe_load(content)
        return data if isinstance(data, dict) else None
    except yaml.YAMLError:
        return None


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate_against_schema(
    data: dict,
    schema: dict,
    file_path: str,
) -> list[str]:
    """Validate data against a JSON Schema.

    Args:
        data: The data to validate.
        schema: The JSON Schema to validate against.
        file_path: File path for error reporting.

    Returns:
        List of formatted error strings (empty if valid).
    """
    validator = Draft202012Validator(schema)
    errors = []
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        path_str = ".".join(str(p) for p in error.path) if error.path else "(root)"
        errors.append(f"{file_path}:{path_str}: {error.message}")
    return errors


# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------


def get_staged_files() -> list[str]:
    """Get staged files from git matching skill patterns.

    Returns:
        List of relative file paths for staged skill files.
    """
    try:
        result = subprocess.run(
            [
                "git",
                "diff",
                "--cached",
                "--name-only",
                "--diff-filter=ACMR",
                "--",
                "skills/",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        if result.returncode != 0:
            return []
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []


def get_all_skill_files() -> tuple[list[Path], list[Path]]:
    """Discover all SKILL.md and skill.jerry.yaml files.

    Returns:
        Tuple of (skill_md_paths, canonical_yaml_paths).
    """
    skills_dir = _REPO_ROOT / "skills"
    if not skills_dir.is_dir():
        return [], []

    skill_mds = sorted(skills_dir.glob("*/SKILL.md"))
    canonical_yamls = sorted(skills_dir.glob("*/composition/skill.jerry.yaml"))
    return skill_mds, canonical_yamls


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def main() -> int:
    """Run skill schema validation.

    Returns:
        0 if no violations found, 1 if violations are present.
    """
    parser = argparse.ArgumentParser(
        description="Validate skill schemas (SKILL.md frontmatter + skill.jerry.yaml)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        default=False,
        help="Validate all skill files (not just staged ones)",
    )
    args = parser.parse_args()

    # Load schemas
    anthropic_schema = load_schema(_ANTHROPIC_SCHEMA_PATH)
    canonical_schema = load_schema(_CANONICAL_SCHEMA_PATH)

    if anthropic_schema is None and canonical_schema is None:
        print("WARNING: No schemas found. Skipping skill schema validation.")
        return 0

    all_errors: list[str] = []
    files_checked = 0

    if args.all:
        # CI mode: validate all files
        skill_mds, canonical_yamls = get_all_skill_files()

        if anthropic_schema:
            for skill_md in skill_mds:
                frontmatter = parse_skill_md_frontmatter(skill_md)
                if frontmatter is None:
                    continue
                files_checked += 1
                rel_path = str(skill_md.relative_to(_REPO_ROOT))
                errors = validate_against_schema(frontmatter, anthropic_schema, rel_path)
                all_errors.extend(errors)

        if canonical_schema:
            for canonical_yaml in canonical_yamls:
                data = load_canonical_yaml(canonical_yaml)
                if data is None:
                    continue
                files_checked += 1
                rel_path = str(canonical_yaml.relative_to(_REPO_ROOT))
                errors = validate_against_schema(data, canonical_schema, rel_path)
                all_errors.extend(errors)

    else:
        # Pre-commit mode: only staged files
        staged_files = get_staged_files()
        if not staged_files:
            return 0

        for file_path in staged_files:
            abs_path = _REPO_ROOT / file_path

            if _SKILL_MD_PATTERN.match(file_path) and anthropic_schema:
                frontmatter = parse_skill_md_frontmatter(abs_path)
                if frontmatter is None:
                    continue
                files_checked += 1
                errors = validate_against_schema(frontmatter, anthropic_schema, file_path)
                all_errors.extend(errors)

            elif _CANONICAL_YAML_PATTERN.match(file_path) and canonical_schema:
                data = load_canonical_yaml(abs_path)
                if data is None:
                    continue
                files_checked += 1
                errors = validate_against_schema(data, canonical_schema, file_path)
                all_errors.extend(errors)

    if files_checked == 0:
        return 0

    # Print errors
    for error in all_errors:
        print(error)

    # Print summary
    print(f"{files_checked} files checked, {len(all_errors)} violations found")

    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main())
