#!/usr/bin/env -S uv run python

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Validate JSON Schema files for Claude Code hook outputs.

Runs 8 validation tests:
1. Schema syntax validation (all 8 schemas)
2. Known-good SessionStart output
3. Known-bad UserPromptSubmit (missing hookEventName)
4. Known-bad PreToolUse (deprecated top-level decision format)
5. Known-bad SubagentStop (has hookSpecificOutput which it shouldn't)
6. Known-good PreToolUse (correct hookSpecificOutput format)
7. Known-good SubagentStop (correct top-level decision format)
8. Known-good UserPromptSubmit (correct format with hookEventName)
"""

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

SCHEMA_DIR = Path(__file__).parent.parent / "schemas" / "hooks"

SCHEMA_FILES = [
    "hook-output-base.schema.json",
    "session-start-output.schema.json",
    "user-prompt-submit-output.schema.json",
    "pre-tool-use-output.schema.json",
    "post-tool-use-output.schema.json",
    "stop-output.schema.json",
    "subagent-stop-output.schema.json",
    "permission-request-output.schema.json",
]

# Track results
results: list[dict] = []


def record(test_id: str, name: str, passed: bool, detail: str = "") -> None:
    """Record a test result."""
    status = "PASS" if passed else "FAIL"
    results.append({"id": test_id, "name": name, "passed": passed, "detail": detail})
    print(f"  [{status}] {test_id}: {name}")
    if detail:
        for line in detail.splitlines():
            print(f"         {line}")


def load_schemas() -> dict[str, dict]:
    """Load all schema files and return as dict keyed by filename."""
    schemas = {}
    for fname in SCHEMA_FILES:
        fpath = SCHEMA_DIR / fname
        with open(fpath) as f:
            schemas[fname] = json.load(f)
    return schemas


def build_registry(schemas: dict[str, dict]) -> Registry:
    """Build a referencing Registry so $ref resolution works."""
    resources = []
    for fname, schema in schemas.items():
        resource = Resource.from_contents(schema, default_specification=DRAFT202012)
        # Use the $id from the schema as the URI, and also the filename
        schema_id = schema.get("$id", fname)
        resources.append((schema_id, resource))
        # Also register by filename for relative $ref resolution
        if schema_id != fname:
            resources.append((fname, resource))
    return Registry().with_resources(resources)


def make_validator(schema: dict, registry: Registry) -> Draft202012Validator:
    """Create a validator with $ref resolution."""
    return Draft202012Validator(schema, registry=registry)


def validate_instance(instance: dict, schema: dict, registry: Registry) -> list[str]:
    """Validate an instance against a schema, return list of errors."""
    validator = make_validator(schema, registry)
    errors = []
    for error in validator.iter_errors(instance):
        errors.append(f"{error.json_path}: {error.message}")
    return errors


def main() -> None:
    print("=" * 70)
    print("Claude Code Hook Schema Validation Report")
    print("=" * 70)

    # Load all schemas
    print("\nLoading schemas...")
    try:
        schemas = load_schemas()
        print(f"  Loaded {len(schemas)} schema files")
    except Exception as e:
        print(f"  FATAL: Failed to load schemas: {e}")
        sys.exit(1)

    # Build registry for $ref resolution
    try:
        registry = build_registry(schemas)
        print("  Registry built for $ref resolution")
    except Exception as e:
        print(f"  FATAL: Failed to build registry: {e}")
        sys.exit(1)

    # ===== TEST 1: Schema Syntax Validation =====
    print("\n--- Test 1: Schema Syntax Validation ---")
    all_valid = True
    syntax_details = []
    for fname in SCHEMA_FILES:
        schema = schemas[fname]
        try:
            Draft202012Validator.check_schema(schema)
            syntax_details.append(f"{fname}: valid")
        except Exception as e:
            all_valid = False
            syntax_details.append(f"{fname}: INVALID - {e}")

    record(
        "T1",
        "All 8 schemas are valid JSON Schema draft 2020-12",
        all_valid,
        "\n".join(syntax_details),
    )

    # ===== TEST 2: Known-Good SessionStart =====
    print("\n--- Test 2: Known-Good SessionStart ---")
    good_session_start = {
        "systemMessage": "test message",
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "test context",
        },
    }
    errors = validate_instance(
        good_session_start,
        schemas["session-start-output.schema.json"],
        registry,
    )
    record(
        "T2",
        "Known-good SessionStart output validates successfully",
        len(errors) == 0,
        "\n".join(errors) if errors else "No validation errors",
    )

    # ===== TEST 3: Known-Bad UserPromptSubmit (missing hookEventName) =====
    print("\n--- Test 3: Known-Bad UserPromptSubmit (missing hookEventName) ---")
    bad_ups_no_event = {
        "hookSpecificOutput": {
            "additionalContext": "test",
        },
    }
    errors = validate_instance(
        bad_ups_no_event,
        schemas["user-prompt-submit-output.schema.json"],
        registry,
    )
    record(
        "T3",
        "Known-bad UserPromptSubmit (missing hookEventName) correctly rejected",
        len(errors) > 0,
        "\n".join(errors) if errors else "ERROR: No validation errors raised (should have failed)",
    )

    # ===== TEST 4: Known-Bad PreToolUse (deprecated top-level decision) =====
    print("\n--- Test 4: Known-Bad PreToolUse (deprecated format) ---")
    bad_ptu_deprecated = {
        "decision": "approve",
    }
    errors = validate_instance(
        bad_ptu_deprecated,
        schemas["pre-tool-use-output.schema.json"],
        registry,
    )
    record(
        "T4",
        "Known-bad PreToolUse (deprecated top-level decision) correctly rejected",
        len(errors) > 0,
        "\n".join(errors) if errors else "ERROR: No validation errors raised (should have failed)",
    )

    # ===== TEST 5: Known-Bad SubagentStop (has hookSpecificOutput) =====
    print("\n--- Test 5: Known-Bad SubagentStop (has hookSpecificOutput) ---")
    bad_sas_with_hso = {
        "hookSpecificOutput": {
            "hookEventName": "SubagentStop",
            "action": "handoff",
        },
    }
    errors = validate_instance(
        bad_sas_with_hso,
        schemas["subagent-stop-output.schema.json"],
        registry,
    )
    record(
        "T5",
        "Known-bad SubagentStop (has hookSpecificOutput) correctly rejected",
        len(errors) > 0,
        "\n".join(errors) if errors else "ERROR: No validation errors raised (should have failed)",
    )

    # ===== TEST 6: Known-Good PreToolUse =====
    print("\n--- Test 6: Known-Good PreToolUse ---")
    good_ptu = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
        },
    }
    errors = validate_instance(
        good_ptu,
        schemas["pre-tool-use-output.schema.json"],
        registry,
    )
    record(
        "T6",
        "Known-good PreToolUse output validates successfully",
        len(errors) == 0,
        "\n".join(errors) if errors else "No validation errors",
    )

    # ===== TEST 7: Known-Good SubagentStop =====
    print("\n--- Test 7: Known-Good SubagentStop ---")
    good_sas = {
        "decision": "block",
        "reason": "Must complete handoff first",
    }
    errors = validate_instance(
        good_sas,
        schemas["subagent-stop-output.schema.json"],
        registry,
    )
    record(
        "T7",
        "Known-good SubagentStop output validates successfully",
        len(errors) == 0,
        "\n".join(errors) if errors else "No validation errors",
    )

    # ===== TEST 8: Known-Good UserPromptSubmit =====
    print("\n--- Test 8: Known-Good UserPromptSubmit ---")
    good_ups = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": "quality reinforcement content",
        },
    }
    errors = validate_instance(
        good_ups,
        schemas["user-prompt-submit-output.schema.json"],
        registry,
    )
    record(
        "T8",
        "Known-good UserPromptSubmit output validates successfully",
        len(errors) == 0,
        "\n".join(errors) if errors else "No validation errors",
    )

    # ===== Summary =====
    print("\n" + "=" * 70)
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed
    verdict = "VALIDATED" if failed == 0 else "FAILED"

    print(f"Results: {passed}/{total} passed, {failed} failed")
    print(f"Verdict: {verdict}")
    print("=" * 70)

    if failed > 0:
        print("\nFailed tests:")
        for r in results:
            if not r["passed"]:
                print(f"  - {r['id']}: {r['name']}")
                if r["detail"]:
                    for line in r["detail"].splitlines():
                        print(f"    {line}")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
