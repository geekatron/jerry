# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Validation script for version_keys.py — run by CI and S-010 self-review.

This script verifies that the version_keys module is importable, classes
construct correctly, validation rules reject invalid input, and the registry
covers the expected set of agents.

Usage: uv run python tests/prompt-regression/validate_keys_check.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add the test directory to path so version_keys is importable
sys.path.insert(0, str(Path(__file__).parent))

from version_keys import (
    BaselineMismatchError,
    BaselineVersionRecord,
    EvaluationMode,
    VersionKey,
    VersionKeyError,
    VersionKeyRegistry,
    validate_baseline_version_key,
)

PASS = 0
FAIL = 0


def check(label: str, condition: bool) -> None:
    """Record a check result."""
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  PASS: {label}")
    else:
        FAIL += 1
        print(f"  FAIL: {label}")


def expect_error(label: str, error_type: type, fn: object) -> None:
    """Assert that calling fn() raises error_type."""
    global PASS, FAIL
    try:
        fn()  # type: ignore[operator]
        FAIL += 1
        print(f"  FAIL: {label} (expected {error_type.__name__}, got no exception)")
    except error_type:
        PASS += 1
        print(f"  PASS: {label}")
    except Exception as exc:
        FAIL += 1
        print(f"  FAIL: {label} (wrong exception type: {type(exc).__name__}: {exc})")


print("=== version_keys.py validation ===")
print()

# --- VersionKey construction ---
print("Section: VersionKey construction and string representation")
valid_hash = "a" * 40
valid_path = "skills/problem-solving/agents/ps-researcher.md"

key = VersionKey(commit_hash=valid_hash, file_path=valid_path)
check("VersionKey constructs without error", key is not None)
check(
    "str() returns composite key format",
    str(key) == f"{valid_hash}:{valid_path}",
)

# --- VersionKey validation: commit hash ---
print()
print("Section: Commit hash validation")
expect_error(
    "Rejects short hash (7 chars)",
    VersionKeyError,
    lambda: VersionKey(commit_hash="abc1234", file_path=valid_path),
)
expect_error(
    "Rejects empty hash",
    VersionKeyError,
    lambda: VersionKey(commit_hash="", file_path=valid_path),
)
expect_error(
    "Rejects 39-char hash (one short)",
    VersionKeyError,
    lambda: VersionKey(commit_hash="a" * 39, file_path=valid_path),
)
expect_error(
    "Rejects non-hex characters in hash",
    VersionKeyError,
    lambda: VersionKey(commit_hash="z" * 40, file_path=valid_path),
)

# --- VersionKey validation: file path ---
print()
print("Section: File path validation (security — OWASP A03 path traversal)")
expect_error(
    "Rejects path traversal (../)",
    VersionKeyError,
    lambda: VersionKey(commit_hash=valid_hash, file_path="../../../etc/passwd"),
)
expect_error(
    "Rejects absolute path",
    VersionKeyError,
    lambda: VersionKey(commit_hash=valid_hash, file_path="/etc/hosts"),
)
expect_error(
    "Rejects path outside skills/*/agents/*.md",
    VersionKeyError,
    lambda: VersionKey(commit_hash=valid_hash, file_path="docs/governance/JERRY_CONSTITUTION.md"),
)
expect_error(
    "Rejects empty file path",
    VersionKeyError,
    lambda: VersionKey(commit_hash=valid_hash, file_path=""),
)

# All 5 covered agent paths must be valid
print()
print("Section: All covered agent file paths are valid")
valid_paths = list(VersionKeyRegistry.AGENT_FILE_PATHS.values())
for fpath in valid_paths:
    key = VersionKey(commit_hash=valid_hash, file_path=fpath)
    check(f"Valid path: {fpath}", str(key).endswith(fpath))

# --- VersionKey.from_string ---
print()
print("Section: VersionKey.from_string round-trip")
key2 = VersionKey.from_string(f"{valid_hash}:{valid_path}")
check("from_string parses commit_hash", key2.commit_hash == valid_hash)
check("from_string parses file_path", key2.file_path == valid_path)
expect_error(
    "from_string rejects missing colon separator",
    VersionKeyError,
    lambda: VersionKey.from_string(valid_hash + valid_path),
)

# --- validate_baseline_version_key ---
print()
print("Section: Baseline version key validation (FR-004 AC-2)")

hash_a = "a" * 40
hash_b = "b" * 40

key_a = VersionKey(commit_hash=hash_a, file_path=valid_path)
key_b = VersionKey(commit_hash=hash_b, file_path=valid_path)

# Matching keys should not raise
try:
    validate_baseline_version_key(baseline_key=key_a, current_branch_key=key_a)
    check("Matching keys pass validation", True)
except Exception:
    check("Matching keys pass validation", False)

# Mismatched hash should raise BaselineMismatchError
expect_error(
    "Mismatched commit hash raises BaselineMismatchError",
    BaselineMismatchError,
    lambda: validate_baseline_version_key(baseline_key=key_a, current_branch_key=key_b),
)

# Mismatched file path should raise BaselineMismatchError
adv_path = "skills/adversary/agents/adv-scorer.md"
key_adv = VersionKey(commit_hash=hash_a, file_path=adv_path)
expect_error(
    "Mismatched file path raises BaselineMismatchError",
    BaselineMismatchError,
    lambda: validate_baseline_version_key(baseline_key=key_a, current_branch_key=key_adv),
)

# --- BaselineVersionRecord.validate_minimum_runs ---
print()
print("Section: BaselineVersionRecord minimum run validation (FR-003)")


def make_record(mode: EvaluationMode, run_count: int) -> BaselineVersionRecord:
    """Create a test baseline record."""
    return BaselineVersionRecord(
        version_key=key_a,
        evaluation_mode=mode,
        run_count=run_count,
        captured_at_iso="2026-03-07T00:00:00Z",
        model_id="claude-sonnet-4-20250514",
    )


# Smoke: N=1 minimum
try:
    make_record(EvaluationMode.SMOKE, 1).validate_minimum_runs()
    check("Smoke N=1 passes minimum validation", True)
except VersionKeyError:
    check("Smoke N=1 passes minimum validation", False)

# Standard: N=10 minimum
expect_error(
    "Standard N=9 fails minimum validation",
    VersionKeyError,
    lambda: make_record(EvaluationMode.STANDARD, 9).validate_minimum_runs(),
)

try:
    make_record(EvaluationMode.STANDARD, 10).validate_minimum_runs()
    check("Standard N=10 passes minimum validation", True)
except VersionKeyError:
    check("Standard N=10 passes minimum validation", False)

# Full: N=30 minimum
expect_error(
    "Full N=29 fails minimum validation",
    VersionKeyError,
    lambda: make_record(EvaluationMode.FULL, 29).validate_minimum_runs(),
)

try:
    make_record(EvaluationMode.FULL, 30).validate_minimum_runs()
    check("Full N=30 passes minimum validation", True)
except VersionKeyError:
    check("Full N=30 passes minimum validation", False)

# --- VersionKeyRegistry ---
print()
print("Section: VersionKeyRegistry coverage and rejection")

registry = VersionKeyRegistry()
check(
    "Registry covers exactly 5 agents",
    len(registry.COVERED_AGENTS) == 5,
)

expected_agents = {"ps-researcher", "ps-analyst", "ps-architect", "ps-critic", "adv-scorer"}
check(
    "Registry covers all 5 expected agent IDs",
    registry.COVERED_AGENTS == expected_agents,
)

expect_error(
    "Registry rejects unknown agent ID",
    VersionKeyError,
    lambda: registry.get_version_key("ps-unknown"),
)

# AGENT_FILE_PATHS has exactly the covered agents as keys
check(
    "AGENT_FILE_PATHS keys match COVERED_AGENTS",
    set(registry.AGENT_FILE_PATHS.keys()) == registry.COVERED_AGENTS,
)

# --- EvaluationMode ---
print()
print("Section: EvaluationMode enum values")
check("SMOKE value is 'smoke'", EvaluationMode.SMOKE.value == "smoke")
check("STANDARD value is 'standard'", EvaluationMode.STANDARD.value == "standard")
check("FULL value is 'full'", EvaluationMode.FULL.value == "full")

# --- Summary ---
print()
print(f"=== Results: {PASS} passed, {FAIL} failed ===")

if FAIL > 0:
    sys.exit(1)
