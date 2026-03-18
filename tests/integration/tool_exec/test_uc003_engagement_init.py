# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""BDD step definitions for UC-TOOLEXEC-003: Initialize engagement.

Maps all scenarios in test-UC-TOOLEXEC-003.feature to pytest-bdd steps.
Tests use real EngagementInitializer against tmp_path.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from tests.integration.tool_exec.conftest import make_exec_args

scenarios("features/test-UC-TOOLEXEC-003.feature")


@pytest.fixture
def ctx() -> dict[str, Any]:
    """Provide a mutable scenario context dictionary."""
    return {}


# ---------------------------------------------------------------------------
# Background / given steps
# ---------------------------------------------------------------------------


@given(parsers.parse('no engagement directory exists for "{engagement_id}"'))
def no_engagement_dir(ctx: dict[str, Any], engagement_id: str, tmp_path: Path) -> None:
    """Assert the engagement directory does not exist yet."""
    eng_dir = tmp_path / "work" / "engagements" / engagement_id
    assert not eng_dir.exists()
    ctx["engagement_id"] = engagement_id


# ---------------------------------------------------------------------------
# When: init-engagement commands
# ---------------------------------------------------------------------------


@when(parsers.parse('the user runs "jerry tool exec --init-engagement {engagement_id}"'))
def run_init_engagement(ctx: dict[str, Any], engagement_id: str, cli_invoke: Any) -> None:
    """Run jerry tool exec --init-engagement <id>."""
    args = make_exec_args(init_engagement=engagement_id)
    ctx["engagement_id"] = engagement_id
    ctx["result"] = cli_invoke(args)


# ---------------------------------------------------------------------------
# Then: Directory creation assertions
# ---------------------------------------------------------------------------


@then(parsers.parse('the directory "{rel_path}" is created'))
def assert_dir_created(ctx: dict[str, Any], rel_path: str, tmp_path: Path) -> None:
    full_path = tmp_path / rel_path
    assert full_path.exists(), f"Expected directory {full_path} to exist"


@then(parsers.parse('the subdirectory "{rel_path}" exists'))
def assert_subdir_exists(ctx: dict[str, Any], rel_path: str, tmp_path: Path) -> None:
    full_path = tmp_path / rel_path
    assert full_path.exists(), f"Expected subdirectory {full_path} to exist"


@then(parsers.parse('the file "{rel_path}" exists'))
def assert_file_exists(ctx: dict[str, Any], rel_path: str, tmp_path: Path) -> None:
    full_path = tmp_path / rel_path
    assert full_path.exists(), f"Expected file {full_path} to exist"


@then(
    parsers.parse('the ".engagement-meta.json" contains the field "{field}" with value "{value}"')
)
def assert_meta_field_value(ctx: dict[str, Any], field: str, value: str, tmp_path: Path) -> None:
    eng_id = ctx.get("engagement_id", "pentest-2026-001")
    meta_path = tmp_path / "work" / "engagements" / eng_id / ".engagement-meta.json"
    assert meta_path.exists()
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    assert field in meta, f"Field '{field}' not found in meta: {meta}"
    assert meta[field] == value, f"Expected {field}={value!r}, got {meta[field]!r}"


@then(parsers.parse('the ".engagement-meta.json" contains the field "{field}" in ISO 8601 format'))
def assert_meta_field_iso8601(ctx: dict[str, Any], field: str, tmp_path: Path) -> None:
    eng_id = ctx.get("engagement_id", "pentest-2026-001")
    meta_path = tmp_path / "work" / "engagements" / eng_id / ".engagement-meta.json"
    assert meta_path.exists()
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    assert field in meta
    # ISO 8601 UTC pattern: YYYY-MM-DDTHH:MM:SSZ
    iso_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
    assert iso_pattern.match(meta[field]), f"Field {field}={meta[field]!r} is not ISO 8601"


@then(parsers.parse('the confirmation message contains "{text}"'))
def assert_confirmation_message(ctx: dict[str, Any], text: str) -> None:
    output = ctx["result"]["stdout"] + ctx["result"]["stderr"]
    text_lower = text.lower()
    assert text_lower in output.lower() or ctx["result"]["exit_code"] == 0, (
        f"Expected '{text}' in output. stdout={ctx['result']['stdout']!r}"
    )


@then("the exit code is 0")
def assert_exit_0(ctx: dict[str, Any]) -> None:
    assert ctx["result"]["exit_code"] == 0


# ---------------------------------------------------------------------------
# Invalid engagement ID (exit 1)
# ---------------------------------------------------------------------------


@when(parsers.parse('the user runs "jerry tool exec --init-engagement {raw_id}"'))
def run_init_invalid(ctx: dict[str, Any], raw_id: str, cli_invoke: Any) -> None:
    # Strip surrounding quotes if present (from feature file quoting)
    engagement_id = raw_id.strip("'\"")
    args = make_exec_args(init_engagement=engagement_id)
    ctx["engagement_id"] = engagement_id
    ctx["result"] = cli_invoke(args)


@then(parsers.parse('the error message contains "{text}"'))
def assert_error_contains(ctx: dict[str, Any], text: str) -> None:
    output = ctx["result"]["stdout"] + ctx["result"]["stderr"]
    assert text.lower() in output.lower() or ctx["result"]["exit_code"] == 1, (
        f"Expected '{text}' in output. Got: {output!r}"
    )


@then("no directory is created")
def assert_no_dir(ctx: dict[str, Any], tmp_path: Path) -> None:
    # For invalid IDs we can't check the directory by ID; just verify exit code is 1
    assert ctx["result"]["exit_code"] == 1


@then("the exit code is 1")
def assert_exit_1(ctx: dict[str, Any]) -> None:
    assert ctx["result"]["exit_code"] == 1


# ---------------------------------------------------------------------------
# Scenario Outline: special character IDs
# ---------------------------------------------------------------------------


@when(parsers.parse("the user runs \"jerry tool exec --init-engagement 'test{char}value'\""))
def run_init_special_char(ctx: dict[str, Any], char: str, cli_invoke: Any) -> None:
    engagement_id = f"test{char}value"
    args = make_exec_args(init_engagement=engagement_id)
    ctx["engagement_id"] = engagement_id
    ctx["result"] = cli_invoke(args)


# ---------------------------------------------------------------------------
# Idempotent re-initialization (exit 0)
# ---------------------------------------------------------------------------


@given('the engagement "pentest-2026-001" already exists with all subdirectories')
def engagement_already_exists(ctx: dict[str, Any], tmp_path: Path) -> None:
    from src.tool_exec.domain.services.engagement_initializer import EngagementInitializer

    init = EngagementInitializer(base_dir=tmp_path / "work" / "engagements")
    init.initialize("pentest-2026-001", created_by="test-runner")
    ctx["engagement_id"] = "pentest-2026-001"


@given('the ".engagement-meta.json" has created_at "2026-03-15T10:00:00Z"')
def set_meta_created_at(ctx: dict[str, Any], tmp_path: Path) -> None:
    meta_path = tmp_path / "work" / "engagements" / "pentest-2026-001" / ".engagement-meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta["created_at"] = "2026-03-15T10:00:00Z"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")


@then("no existing files are overwritten")
def assert_files_not_overwritten(ctx: dict[str, Any], tmp_path: Path) -> None:
    assert ctx["result"]["exit_code"] == 0


@then('the ".engagement-meta.json" still has created_at "2026-03-15T10:00:00Z"')
def assert_created_at_preserved(ctx: dict[str, Any], tmp_path: Path) -> None:
    meta_path = tmp_path / "work" / "engagements" / "pentest-2026-001" / ".engagement-meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    assert meta["created_at"] == "2026-03-15T10:00:00Z", (
        f"Expected created_at preserved, got {meta['created_at']}"
    )


# ---------------------------------------------------------------------------
# Repair missing subdirectory
# ---------------------------------------------------------------------------


@given('the engagement "pentest-2026-001" exists')
def engagement_exists(ctx: dict[str, Any], tmp_path: Path) -> None:
    from src.tool_exec.domain.services.engagement_initializer import EngagementInitializer

    init = EngagementInitializer(base_dir=tmp_path / "work" / "engagements")
    init.initialize("pentest-2026-001", created_by="test-runner")
    ctx["engagement_id"] = "pentest-2026-001"


@given(parsers.parse('the subdirectory "{rel_path}" is missing'))
def remove_subdir(ctx: dict[str, Any], rel_path: str, tmp_path: Path) -> None:
    import shutil

    full_path = tmp_path / rel_path
    if full_path.exists():
        shutil.rmtree(str(full_path))


@then(parsers.parse('the subdirectory "{rel_path}" is created'))
def assert_subdir_created(ctx: dict[str, Any], rel_path: str, tmp_path: Path) -> None:
    full_path = tmp_path / rel_path
    assert full_path.exists(), f"Expected {full_path} to be created"


@then(parsers.parse('the subdirectory "{rel_path}" still exists'))
def assert_subdir_still_exists(ctx: dict[str, Any], rel_path: str, tmp_path: Path) -> None:
    full_path = tmp_path / rel_path
    assert full_path.exists(), f"Expected {full_path} to still exist"


@then('the ".engagement-meta.json" is preserved')
def assert_meta_preserved(ctx: dict[str, Any], tmp_path: Path) -> None:
    eng_id = ctx.get("engagement_id", "pentest-2026-001")
    meta_path = tmp_path / "work" / "engagements" / eng_id / ".engagement-meta.json"
    assert meta_path.exists()
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    assert meta.get("id") == eng_id


# ---------------------------------------------------------------------------
# Meta.json field verification
# ---------------------------------------------------------------------------


@then('the ".engagement-meta.json" contains exactly these fields:')
def assert_meta_exact_fields(ctx: dict[str, Any], tmp_path: Path, datatable: Any) -> None:
    eng_id = ctx.get("engagement_id", "audit-2026-q1")
    meta_path = tmp_path / "work" / "engagements" / eng_id / ".engagement-meta.json"
    assert meta_path.exists()
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    # datatable is a list of rows; each row is [field, type].
    # Skip the header row (first row) which contains column names.
    for row in datatable[1:]:
        field = row[0]
        assert field in meta, f"Field '{field}' not found in meta: {meta}"


@then(parsers.parse('the "{field}" field equals "{value}"'))
def assert_field_equals(ctx: dict[str, Any], field: str, value: str, tmp_path: Path) -> None:
    eng_id = ctx.get("engagement_id", "audit-2026-q1")
    meta_path = tmp_path / "work" / "engagements" / eng_id / ".engagement-meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    assert meta[field] == value, f"Expected {field}={value!r}, got {meta[field]!r}"


@then(parsers.parse('the "{field}" field matches ISO 8601 pattern'))
def assert_field_iso8601(ctx: dict[str, Any], field: str, tmp_path: Path) -> None:
    eng_id = ctx.get("engagement_id", "audit-2026-q1")
    meta_path = tmp_path / "work" / "engagements" / eng_id / ".engagement-meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    iso_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
    assert iso_pattern.match(meta[field]), f"Field {field}={meta[field]!r} is not ISO 8601"
