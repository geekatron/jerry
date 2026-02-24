# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for hook output schema compliance.

Validates that:
1. All JSON Schema files are valid draft 2020-12 schemas
2. Known-good hook outputs validate against their schemas
3. Known-bad hook outputs are correctly rejected
4. Live hook script outputs conform to their schemas

References:
    - BUG-002 / TASK-005: Hook schema validation pytest tests
    - schemas/hooks/: 8 JSON Schema files for hook outputs
    - scripts/validate_schemas.py: Standalone validation script (pattern reused here)
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = PROJECT_ROOT / "schemas" / "hooks"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
HOOKS_DIR = PROJECT_ROOT / "hooks"

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

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def all_schemas() -> dict[str, dict[str, Any]]:
    """Load all schema files and return as dict keyed by filename."""
    schemas: dict[str, dict[str, Any]] = {}
    for fname in SCHEMA_FILES:
        fpath = SCHEMA_DIR / fname
        with open(fpath) as f:
            schemas[fname] = json.load(f)
    return schemas


@pytest.fixture(scope="module")
def schema_registry(all_schemas: dict[str, dict[str, Any]]) -> Registry:
    """Build a referencing Registry for $ref resolution across schemas."""
    resources: list[tuple[str, Resource]] = []
    for fname, schema in all_schemas.items():
        resource = Resource.from_contents(schema, default_specification=DRAFT202012)
        schema_id = schema.get("$id", fname)
        resources.append((schema_id, resource))
        if schema_id != fname:
            resources.append((fname, resource))
    return Registry().with_resources(resources)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def validate_instance(
    instance: dict[str, Any],
    schema: dict[str, Any],
    registry: Registry,
) -> list[str]:
    """Validate an instance against a schema, returning a list of error strings."""
    validator = Draft202012Validator(schema, registry=registry)
    return [f"{err.json_path}: {err.message}" for err in validator.iter_errors(instance)]


def run_hook_script(
    script_path: Path,
    input_data: dict[str, Any],
    *,
    timeout: int = 15,
) -> tuple[int, dict[str, Any] | None, str]:
    """Run a hook script as a subprocess and return (exit_code, stdout_json, stderr).

    Args:
        script_path: Path to the hook script.
        input_data: JSON-serialisable dict to send on stdin.
        timeout: Max seconds to wait for the subprocess.

    Returns:
        Tuple of (exit_code, parsed_stdout_json_or_None, stderr_text).
    """
    result = subprocess.run(
        [sys.executable, str(script_path)],
        input=json.dumps(input_data),
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(PROJECT_ROOT),
    )

    stdout_json: dict[str, Any] | None = None
    if result.stdout.strip():
        try:
            stdout_json = json.loads(result.stdout.strip())
        except json.JSONDecodeError:
            pass

    return result.returncode, stdout_json, result.stderr


# =============================================================================
# TestSchemaSyntax
# =============================================================================


class TestSchemaSyntax:
    """Each schema file is valid JSON Schema draft 2020-12 and refs resolve."""

    @pytest.mark.parametrize("schema_file", SCHEMA_FILES)
    def test_schema_is_valid_draft_2020_12(
        self,
        schema_file: str,
        all_schemas: dict[str, dict[str, Any]],
    ) -> None:
        """Schema file must be a valid JSON Schema draft 2020-12 document."""
        schema = all_schemas[schema_file]
        Draft202012Validator.check_schema(schema)

    @pytest.mark.parametrize(
        "schema_file",
        [f for f in SCHEMA_FILES if f != "hook-output-base.schema.json"],
    )
    def test_ref_references_resolve(
        self,
        schema_file: str,
        all_schemas: dict[str, dict[str, Any]],
        schema_registry: Registry,
    ) -> None:
        """All $ref references in the schema must resolve against the registry."""
        schema = all_schemas[schema_file]
        # Creating a validator and calling iter_errors on a minimal valid-ish
        # instance exercises $ref resolution; if a $ref is broken the validator
        # raises RefResolutionError on construction or iteration.
        validator = Draft202012Validator(schema, registry=schema_registry)
        # Simply instantiate and iterate; we do not care about the validation
        # outcome here -- only that no resolution errors occur.
        list(validator.iter_errors({}))


# =============================================================================
# TestKnownGoodOutputs
# =============================================================================


class TestKnownGoodOutputs:
    """Known-good hook outputs must validate against their respective schemas."""

    def test_session_start_good(
        self,
        all_schemas: dict[str, dict[str, Any]],
        schema_registry: Registry,
    ) -> None:
        """SessionStart with systemMessage + hookSpecificOutput validates."""
        instance: dict[str, Any] = {
            "systemMessage": "Jerry Framework: PROJ-001 active. Quality gates set.",
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": "<project-context>\nProjectActive: PROJ-001\n</project-context>",
            },
        }
        errors = validate_instance(
            instance,
            all_schemas["session-start-output.schema.json"],
            schema_registry,
        )
        assert errors == [], f"Unexpected validation errors: {errors}"

    def test_user_prompt_submit_good(
        self,
        all_schemas: dict[str, dict[str, Any]],
        schema_registry: Registry,
    ) -> None:
        """UserPromptSubmit with hookEventName + additionalContext validates."""
        instance: dict[str, Any] = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": "<quality-reinforcement>\nrule content\n</quality-reinforcement>",
            },
        }
        errors = validate_instance(
            instance,
            all_schemas["user-prompt-submit-output.schema.json"],
            schema_registry,
        )
        assert errors == [], f"Unexpected validation errors: {errors}"

    def test_pre_tool_use_allow_good(
        self,
        all_schemas: dict[str, dict[str, Any]],
        schema_registry: Registry,
    ) -> None:
        """PreToolUse allow decision validates."""
        instance: dict[str, Any] = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
            },
        }
        errors = validate_instance(
            instance,
            all_schemas["pre-tool-use-output.schema.json"],
            schema_registry,
        )
        assert errors == [], f"Unexpected validation errors: {errors}"

    def test_pre_tool_use_deny_good(
        self,
        all_schemas: dict[str, dict[str, Any]],
        schema_registry: Registry,
    ) -> None:
        """PreToolUse deny decision with reason validates."""
        instance: dict[str, Any] = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "Writing to ~/.ssh is blocked for security",
            },
        }
        errors = validate_instance(
            instance,
            all_schemas["pre-tool-use-output.schema.json"],
            schema_registry,
        )
        assert errors == [], f"Unexpected validation errors: {errors}"

    def test_subagent_stop_block_good(
        self,
        all_schemas: dict[str, dict[str, Any]],
        schema_registry: Registry,
    ) -> None:
        """SubagentStop block decision with reason validates."""
        instance: dict[str, Any] = {
            "decision": "block",
            "reason": "Handoff required: route to qa-engineer.",
        }
        errors = validate_instance(
            instance,
            all_schemas["subagent-stop-output.schema.json"],
            schema_registry,
        )
        assert errors == [], f"Unexpected validation errors: {errors}"

    def test_subagent_stop_empty_good(
        self,
        all_schemas: dict[str, dict[str, Any]],
        schema_registry: Registry,
    ) -> None:
        """SubagentStop empty output (allow stop) validates."""
        instance: dict[str, Any] = {}
        errors = validate_instance(
            instance,
            all_schemas["subagent-stop-output.schema.json"],
            schema_registry,
        )
        assert errors == [], f"Unexpected validation errors: {errors}"


# =============================================================================
# TestKnownBadOutputs
# =============================================================================


class TestKnownBadOutputs:
    """Known-bad hook outputs must be correctly rejected by their schemas."""

    def test_user_prompt_submit_missing_hook_event_name(
        self,
        all_schemas: dict[str, dict[str, Any]],
        schema_registry: Registry,
    ) -> None:
        """UserPromptSubmit missing hookEventName must fail validation."""
        instance: dict[str, Any] = {
            "hookSpecificOutput": {
                "additionalContext": "test",
            },
        }
        errors = validate_instance(
            instance,
            all_schemas["user-prompt-submit-output.schema.json"],
            schema_registry,
        )
        assert len(errors) > 0, "Expected validation errors for missing hookEventName"

    def test_pre_tool_use_deprecated_top_level_decision(
        self,
        all_schemas: dict[str, dict[str, Any]],
        schema_registry: Registry,
    ) -> None:
        """PreToolUse with deprecated top-level 'decision' field must fail."""
        instance: dict[str, Any] = {
            "decision": "approve",
        }
        errors = validate_instance(
            instance,
            all_schemas["pre-tool-use-output.schema.json"],
            schema_registry,
        )
        assert len(errors) > 0, (
            "Expected validation errors for deprecated top-level decision format"
        )

    def test_subagent_stop_with_hook_specific_output(
        self,
        all_schemas: dict[str, dict[str, Any]],
        schema_registry: Registry,
    ) -> None:
        """SubagentStop with hookSpecificOutput must fail (uses top-level only)."""
        instance: dict[str, Any] = {
            "hookSpecificOutput": {
                "hookEventName": "SubagentStop",
                "action": "handoff",
            },
        }
        errors = validate_instance(
            instance,
            all_schemas["subagent-stop-output.schema.json"],
            schema_registry,
        )
        assert len(errors) > 0, (
            "Expected validation errors for SubagentStop with hookSpecificOutput"
        )

    def test_pre_tool_use_wrong_vocabulary(
        self,
        all_schemas: dict[str, dict[str, Any]],
        schema_registry: Registry,
    ) -> None:
        """PreToolUse with wrong vocabulary (block/approve) must fail."""
        instance: dict[str, Any] = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "block",
            },
        }
        errors = validate_instance(
            instance,
            all_schemas["pre-tool-use-output.schema.json"],
            schema_registry,
        )
        assert len(errors) > 0, (
            "Expected validation errors for wrong vocabulary 'block' "
            "(valid values: allow, deny, ask)"
        )

        # Also check "approve" which is another wrong term
        instance2: dict[str, Any] = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "approve",
            },
        }
        errors2 = validate_instance(
            instance2,
            all_schemas["pre-tool-use-output.schema.json"],
            schema_registry,
        )
        assert len(errors2) > 0, (
            "Expected validation errors for wrong vocabulary 'approve' "
            "(valid values: allow, deny, ask)"
        )


# =============================================================================
# TestLiveHookOutputCompliance
# =============================================================================


@pytest.mark.subprocess
class TestLiveHookOutputCompliance:
    """Run each hook script and validate its stdout JSON against the correct schema."""

    # ----- pre_tool_use.py -----

    def test_pre_tool_use_allow_output(
        self,
        all_schemas: dict[str, dict[str, Any]],
        schema_registry: Registry,
    ) -> None:
        """pre_tool_use.py allow path output conforms to PreToolUse schema."""
        script = SCRIPTS_DIR / "pre_tool_use.py"
        exit_code, stdout_json, _stderr = run_hook_script(
            script,
            {"tool_name": "Read", "tool_input": {"file_path": "/tmp/test.txt"}},
        )

        assert exit_code == 0, f"Hook exited with code {exit_code}"
        assert stdout_json is not None, "Hook produced no JSON output"

        errors = validate_instance(
            stdout_json,
            all_schemas["pre-tool-use-output.schema.json"],
            schema_registry,
        )
        assert errors == [], f"Schema validation errors: {errors}"

    def test_pre_tool_use_deny_output(
        self,
        all_schemas: dict[str, dict[str, Any]],
        schema_registry: Registry,
    ) -> None:
        """pre_tool_use.py deny path output conforms to PreToolUse schema."""
        script = SCRIPTS_DIR / "pre_tool_use.py"
        exit_code, stdout_json, _stderr = run_hook_script(
            script,
            {
                "tool_name": "Write",
                "tool_input": {
                    "file_path": "~/.ssh/authorized_keys",
                    "content": "malicious",
                },
            },
        )

        assert exit_code == 0, f"Hook exited with code {exit_code}"
        assert stdout_json is not None, "Hook produced no JSON output"

        errors = validate_instance(
            stdout_json,
            all_schemas["pre-tool-use-output.schema.json"],
            schema_registry,
        )
        assert errors == [], f"Schema validation errors: {errors}"

    # ----- subagent_stop.py -----

    def test_subagent_stop_block_output(
        self,
        all_schemas: dict[str, dict[str, Any]],
        schema_registry: Registry,
    ) -> None:
        """subagent_stop.py block path output conforms to SubagentStop schema."""
        script = SCRIPTS_DIR / "subagent_stop.py"
        # Provide input that triggers a handoff (orchestrator + implementation_complete)
        exit_code, stdout_json, _stderr = run_hook_script(
            script,
            {
                "agent_name": "orchestrator",
                "output": "Work done.\n##HANDOFF:implementation_complete##\nAll tasks finished.",
            },
        )

        assert exit_code == 0, f"Hook exited with code {exit_code}"
        assert stdout_json is not None, "Hook produced no JSON output"

        errors = validate_instance(
            stdout_json,
            all_schemas["subagent-stop-output.schema.json"],
            schema_registry,
        )
        assert errors == [], f"Schema validation errors: {errors}"

    def test_subagent_stop_allow_output(
        self,
        all_schemas: dict[str, dict[str, Any]],
        schema_registry: Registry,
    ) -> None:
        """subagent_stop.py allow-stop path output conforms to SubagentStop schema."""
        script = SCRIPTS_DIR / "subagent_stop.py"
        # Provide input with no handoff signal -> empty output (allow stop)
        exit_code, stdout_json, _stderr = run_hook_script(
            script,
            {
                "agent_name": "unknown-agent",
                "output": "Just finished my work, nothing special.",
            },
        )

        assert exit_code == 0, f"Hook exited with code {exit_code}"
        assert stdout_json is not None, "Hook produced no JSON output"

        errors = validate_instance(
            stdout_json,
            all_schemas["subagent-stop-output.schema.json"],
            schema_registry,
        )
        assert errors == [], f"Schema validation errors: {errors}"

    # ----- prompt-submit (via CLI) -----

    def test_user_prompt_submit_output(
        self,
        all_schemas: dict[str, dict[str, Any]],
        schema_registry: Registry,
    ) -> None:
        """prompt-submit hook via CLI produces valid JSON with additionalContext.

        EN-007: Hooks now run via jerry CLI. The CLI output format uses
        top-level additionalContext rather than the nested hookSpecificOutput
        format defined in the original schemas.
        """
        result = subprocess.run(
            ["uv", "run", "jerry", "--json", "hooks", "prompt-submit"],
            input=json.dumps({"prompt": "Hello, how are you?"}),
            capture_output=True,
            text=True,
            timeout=15,
            cwd=str(PROJECT_ROOT),
        )

        assert result.returncode == 0, f"Hook exited with code {result.returncode}"
        stdout_json = json.loads(result.stdout.strip())
        assert isinstance(stdout_json, dict), "Hook output must be a JSON object"
        assert "additionalContext" in stdout_json, (
            f"Hook output must contain additionalContext. Got keys: {list(stdout_json.keys())}"
        )
        assert isinstance(stdout_json["additionalContext"], str)

    # ----- session-start (via CLI) -----

    def test_session_start_output(
        self,
        all_schemas: dict[str, dict[str, Any]],
        schema_registry: Registry,
    ) -> None:
        """session-start hook via CLI produces valid JSON with additionalContext.

        EN-007: Hooks now run via jerry CLI. The CLI output format uses
        top-level additionalContext rather than the nested hookSpecificOutput
        format defined in the original schemas.
        """
        result = subprocess.run(
            ["uv", "run", "jerry", "--json", "hooks", "session-start"],
            input=json.dumps({}),
            capture_output=True,
            text=True,
            timeout=45,
            cwd=str(PROJECT_ROOT),
        )

        assert result.returncode == 0, f"Hook exited with code {result.returncode}"
        stdout_json = json.loads(result.stdout.strip())
        assert isinstance(stdout_json, dict), "Hook output must be a JSON object"
        assert "additionalContext" in stdout_json, (
            f"Hook output must contain additionalContext. Got keys: {list(stdout_json.keys())}"
        )
        assert isinstance(stdout_json["additionalContext"], str)
        assert len(stdout_json["additionalContext"]) > 0, "additionalContext must not be empty"
