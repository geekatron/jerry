#!/usr/bin/env python3
"""Validate plugin manifest files against JSON Schema.

This script validates the following plugin artifacts:
- .claude-plugin/plugin.json
- .claude-plugin/marketplace.json
- hooks/hooks.json

Schemas are stored in schemas/ directory and versioned with the repo.
Uses official Claude Code schemas where available, custom schemas (via Context7) otherwise.

All validation calls explicitly specify Draft202012Validator to ensure consistent
interpretation of JSON Schema Draft 2020-12 features regardless of jsonschema library defaults.

References:
    - EN-005: Pre-commit/CI hooks for plugin validation
    - DEC-001: JSON Schema Validator Class Selection
    - DEC-002: Schema Validation Approach

Exit Codes:
    0: All validations passed
    1: One or more validations failed
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import NamedTuple

try:
    import jsonschema
except ImportError:
    print("ERROR: jsonschema package not installed")
    print("Run: uv sync --all-extras")
    sys.exit(1)


class ValidationResult(NamedTuple):
    """Result of a single validation."""

    file_path: str
    passed: bool
    error: str | None = None


def get_project_root() -> Path:
    """Get the project root directory."""
    # Script is in scripts/, so go up one level
    return Path(__file__).parent.parent


def load_json(file_path: Path) -> dict | list | None:
    """Load and parse a JSON file."""
    try:
        return json.loads(file_path.read_text())
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {file_path}: {e}") from e


def validate_plugin_json(project_root: Path) -> ValidationResult:
    """Validate .claude-plugin/plugin.json against schema."""
    manifest_path = project_root / ".claude-plugin" / "plugin.json"
    schema_path = project_root / "schemas" / "plugin.schema.json"

    if not manifest_path.exists():
        return ValidationResult(
            file_path=str(manifest_path),
            passed=False,
            error="File not found",
        )

    if not schema_path.exists():
        return ValidationResult(
            file_path=str(manifest_path),
            passed=False,
            error=f"Schema not found: {schema_path}",
        )

    try:
        manifest = load_json(manifest_path)
        schema = load_json(schema_path)

        if manifest is None:
            return ValidationResult(
                file_path=str(manifest_path),
                passed=False,
                error="Failed to load manifest",
            )

        jsonschema.validate(manifest, schema, cls=jsonschema.Draft202012Validator)
        return ValidationResult(file_path=str(manifest_path), passed=True)

    except jsonschema.ValidationError as e:
        return ValidationResult(
            file_path=str(manifest_path),
            passed=False,
            error=f"Schema validation failed: {e.message}",
        )
    except ValueError as e:
        return ValidationResult(
            file_path=str(manifest_path),
            passed=False,
            error=str(e),
        )


def validate_marketplace_json(project_root: Path) -> ValidationResult:
    """Validate .claude-plugin/marketplace.json against schema."""
    manifest_path = project_root / ".claude-plugin" / "marketplace.json"
    schema_path = project_root / "schemas" / "marketplace.schema.json"

    if not manifest_path.exists():
        return ValidationResult(
            file_path=str(manifest_path),
            passed=False,
            error="File not found",
        )

    if not schema_path.exists():
        return ValidationResult(
            file_path=str(manifest_path),
            passed=False,
            error=f"Schema not found: {schema_path}",
        )

    try:
        manifest = load_json(manifest_path)
        schema = load_json(schema_path)

        if manifest is None:
            return ValidationResult(
                file_path=str(manifest_path),
                passed=False,
                error="Failed to load manifest",
            )

        jsonschema.validate(manifest, schema, cls=jsonschema.Draft202012Validator)
        return ValidationResult(file_path=str(manifest_path), passed=True)

    except jsonschema.ValidationError as e:
        return ValidationResult(
            file_path=str(manifest_path),
            passed=False,
            error=f"Schema validation failed: {e.message}",
        )
    except ValueError as e:
        return ValidationResult(
            file_path=str(manifest_path),
            passed=False,
            error=str(e),
        )


def validate_hooks_json(project_root: Path) -> ValidationResult:
    """Validate hooks/hooks.json against schema."""
    manifest_path = project_root / "hooks" / "hooks.json"
    schema_path = project_root / "schemas" / "hooks.schema.json"

    if not manifest_path.exists():
        return ValidationResult(
            file_path=str(manifest_path),
            passed=False,
            error="File not found",
        )

    if not schema_path.exists():
        return ValidationResult(
            file_path=str(manifest_path),
            passed=False,
            error=f"Schema not found: {schema_path}",
        )

    try:
        manifest = load_json(manifest_path)
        schema = load_json(schema_path)

        if manifest is None:
            return ValidationResult(
                file_path=str(manifest_path),
                passed=False,
                error="Failed to load manifest",
            )

        jsonschema.validate(manifest, schema, cls=jsonschema.Draft202012Validator)
        return ValidationResult(file_path=str(manifest_path), passed=True)

    except jsonschema.ValidationError as e:
        return ValidationResult(
            file_path=str(manifest_path),
            passed=False,
            error=f"Schema validation failed: {e.message}",
        )
    except ValueError as e:
        return ValidationResult(
            file_path=str(manifest_path),
            passed=False,
            error=str(e),
        )


def main() -> int:
    """Run all validations, return 0 on success, 1 on failure."""
    project_root = get_project_root()

    print("Validating plugin manifests...")
    print(f"Project root: {project_root}")
    print()

    results = [
        validate_plugin_json(project_root),
        validate_marketplace_json(project_root),
        validate_hooks_json(project_root),
    ]

    all_passed = True

    for result in results:
        if result.passed:
            print(f"[PASS] {result.file_path}")
        else:
            print(f"[FAIL] {result.file_path}")
            print(f"       Error: {result.error}")
            all_passed = False

    print()
    if all_passed:
        print("All validations passed!")
        return 0
    else:
        print("Some validations failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
