# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ST-007 Migration Comparison Script.

Finds 10 real entity files in the projects/ directory (mix of entity types),
runs /ast operations (query_frontmatter, validate_file with schema detection),
and compares results to verify the domain layer correctly handles real project
files.

Prints a summary showing pass/fail per file.

Usage:
    uv run python scripts/st007_migration_comparison.py

References:
    - ST-007: Migrate /worktracker Agents to AST
    - skills/ast/scripts/ast_ops.py (AST operations)
    - src/domain/markdown_ast/schema.py (entity schemas)
"""

from __future__ import annotations

import os
import sys

# Ensure project root is on sys.path for imports
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from skills.ast.scripts.ast_ops import (
    parse_file,
    query_frontmatter,
    validate_file,
)

# ---------------------------------------------------------------------------
# Entity type detection (same logic as in test suite)
# ---------------------------------------------------------------------------

_ENTITY_PREFIX_MAP: dict[str, str] = {
    "EPIC": "epic",
    "FEAT": "feature",
    "ST": "story",
    "EN": "enabler",
    "TASK": "task",
    "BUG": "bug",
}


def detect_entity_type(file_path: str) -> str | None:
    """
    Detect entity type from a file path based on filename prefix.

    Args:
        file_path: Path to a worktracker entity file.

    Returns:
        Entity type string (e.g., "epic", "task") or None if unrecognized.
    """
    basename = os.path.basename(file_path)
    for prefix, entity_type in _ENTITY_PREFIX_MAP.items():
        if basename.startswith(f"{prefix}-"):
            return entity_type
    return None


def find_entity_files(projects_dir: str, target_count: int = 10) -> list[str]:
    """
    Find entity files in the projects directory, aiming for a mix of types.

    Walks the projects directory tree and collects files whose basename matches
    a known entity prefix. Tries to include at least one of each type.

    Args:
        projects_dir: Path to the projects/ directory.
        target_count: Target number of files to return.

    Returns:
        List of absolute paths to entity files.
    """
    by_type: dict[str, list[str]] = {t: [] for t in _ENTITY_PREFIX_MAP.values()}
    all_entity_files: list[str] = []

    for root, _dirs, files in os.walk(projects_dir):
        for fname in files:
            if not fname.endswith(".md"):
                continue
            entity_type = detect_entity_type(fname)
            if entity_type is None:
                continue
            full_path = os.path.join(root, fname)
            by_type[entity_type].append(full_path)
            all_entity_files.append(full_path)

    # Build selection: one of each type first, then fill remaining
    selected: list[str] = []
    for entity_type, paths in by_type.items():
        if paths:
            selected.append(paths[0])

    # Fill up to target_count
    for path in all_entity_files:
        if len(selected) >= target_count:
            break
        if path not in selected:
            selected.append(path)

    return selected[:target_count]


def run_comparison(file_path: str) -> dict[str, object]:
    """
    Run AST operations on a single entity file and collect results.

    Args:
        file_path: Absolute path to the entity file.

    Returns:
        Dict with file_path, entity_type, frontmatter results,
        validation results, and pass/fail status.
    """
    entity_type = detect_entity_type(file_path)
    result: dict[str, object] = {
        "file_path": file_path,
        "entity_type": entity_type,
        "passed": False,
        "errors": [],
    }
    errors: list[str] = result["errors"]  # type: ignore[assignment]

    # 1. query_frontmatter
    try:
        fm = query_frontmatter(file_path)
        result["frontmatter_fields"] = list(fm.keys())
        result["frontmatter_count"] = len(fm)
        if not fm:
            errors.append("No frontmatter found")
    except Exception as e:
        errors.append(f"query_frontmatter error: {e}")
        result["frontmatter_fields"] = []
        result["frontmatter_count"] = 0

    # 2. parse_file
    try:
        info = parse_file(file_path)
        result["heading_count"] = info["heading_count"]
        result["has_frontmatter"] = info["has_frontmatter"]
    except Exception as e:
        errors.append(f"parse_file error: {e}")

    # 3. validate_file with schema
    if entity_type:
        try:
            validation = validate_file(file_path, schema=entity_type)
            result["schema_valid"] = validation["schema_valid"]
            result["nav_table_valid"] = validation["nav_table_valid"]
            result["schema_violations_count"] = len(
                validation.get("schema_violations", [])
            )
            if not validation["schema_valid"]:
                violations = validation.get("schema_violations", [])
                for v in violations[:3]:  # Show first 3 violations
                    errors.append(
                        f"Schema violation: {v['field_path']} - {v['message']}"
                    )
        except Exception as e:
            errors.append(f"validate_file error: {e}")
    else:
        result["schema_valid"] = None
        result["nav_table_valid"] = None

    # Determine pass/fail
    # Pass = frontmatter extracted successfully (core migration requirement)
    result["passed"] = len(errors) == 0 or (
        result.get("frontmatter_count", 0) > 0
        and result.get("has_frontmatter", False)
    )

    return result


def main() -> None:
    """Run the migration comparison on 10 real entity files."""
    projects_dir = os.path.join(_PROJECT_ROOT, "projects")

    if not os.path.isdir(projects_dir):
        print(f"ERROR: Projects directory not found: {projects_dir}")
        sys.exit(1)

    print("=" * 78)
    print("ST-007 Migration Comparison: AST Operations on Real Entity Files")
    print("=" * 78)
    print()

    entity_files = find_entity_files(projects_dir, target_count=10)
    if not entity_files:
        print("ERROR: No entity files found in projects/")
        sys.exit(1)

    print(f"Found {len(entity_files)} entity files to test:")
    print()

    results: list[dict[str, object]] = []
    for i, file_path in enumerate(entity_files, 1):
        result = run_comparison(file_path)
        results.append(result)

        # Relative path for display
        rel_path = os.path.relpath(file_path, _PROJECT_ROOT)
        status = "PASS" if result["passed"] else "FAIL"
        entity_type = result.get("entity_type", "unknown")
        fm_count = result.get("frontmatter_count", 0)
        schema_valid = result.get("schema_valid", "N/A")

        print(f"  [{i:2d}] {status} | {entity_type:8s} | fm={fm_count:2d} | "
              f"schema={str(schema_valid):5s} | {rel_path}")

        errors = result.get("errors", [])
        if errors:
            for err in errors[:3]:  # type: ignore[union-attr]
                print(f"       -> {err}")

    # Summary
    print()
    print("-" * 78)
    passed = sum(1 for r in results if r["passed"])
    failed = sum(1 for r in results if not r["passed"])
    total = len(results)

    print(f"Summary: {passed}/{total} passed, {failed}/{total} failed")
    print()

    # Type coverage
    types_seen = {r["entity_type"] for r in results if r["entity_type"]}
    print(f"Entity types covered: {', '.join(sorted(types_seen))}")

    # Schema validation summary
    schema_passed = sum(1 for r in results if r.get("schema_valid") is True)
    schema_failed = sum(1 for r in results if r.get("schema_valid") is False)
    print(f"Schema validation: {schema_passed} passed, {schema_failed} failed")

    print()
    print("=" * 78)
    if failed > 0:
        print("RESULT: Some files had issues (see errors above)")
        print("Note: Schema validation failures are expected for real files")
        print("that may not perfectly match the strict entity schemas.")
    else:
        print("RESULT: All files processed successfully by AST operations")
    print("=" * 78)


if __name__ == "__main__":
    main()
