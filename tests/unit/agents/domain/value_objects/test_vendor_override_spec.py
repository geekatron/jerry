# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for VendorOverrideSpec value object."""

from __future__ import annotations

from src.agents.domain.value_objects.vendor_override_spec import (
    CLAUDE_CODE_OVERRIDE_SPEC,
    VendorOverrideSpec,
)


class TestVendorOverrideSpec:
    """Tests for VendorOverrideSpec.validate()."""

    def test_allowed_keys_pass(self) -> None:
        spec = VendorOverrideSpec(
            vendor="test",
            allowed_keys=frozenset({"permissionMode", "background"}),
        )
        errors = spec.validate({"permissionMode": "bypassPermissions"})
        assert errors == []

    def test_disallowed_key_returns_error(self) -> None:
        spec = VendorOverrideSpec(
            vendor="test",
            allowed_keys=frozenset({"permissionMode"}),
        )
        errors = spec.validate({"constitution": {"evil": True}})
        assert len(errors) == 1
        assert "constitution" in errors[0]

    def test_empty_overrides_pass(self) -> None:
        spec = VendorOverrideSpec(
            vendor="test",
            allowed_keys=frozenset({"permissionMode"}),
        )
        errors = spec.validate({})
        assert errors == []

    def test_multiple_disallowed_keys(self) -> None:
        spec = VendorOverrideSpec(
            vendor="test",
            allowed_keys=frozenset({"permissionMode"}),
        )
        errors = spec.validate({"constitution": {}, "guardrails": {}, "enforcement": {}})
        assert len(errors) == 3

    def test_mixed_allowed_and_disallowed(self) -> None:
        spec = VendorOverrideSpec(
            vendor="test",
            allowed_keys=frozenset({"permissionMode", "background"}),
        )
        errors = spec.validate({"permissionMode": "default", "constitution": {}})
        assert len(errors) == 1
        assert "constitution" in errors[0]

    def test_frozen_dataclass(self) -> None:
        spec = VendorOverrideSpec(vendor="test", allowed_keys=frozenset({"a"}))
        assert spec.vendor == "test"
        assert spec.allowed_keys == frozenset({"a"})

    def test_error_message_includes_vendor_name(self) -> None:
        spec = VendorOverrideSpec(
            vendor="my_vendor",
            allowed_keys=frozenset({"a"}),
        )
        errors = spec.validate({"bad_key": "value"})
        assert "my_vendor" in errors[0]

    def test_error_message_lists_allowed_keys(self) -> None:
        spec = VendorOverrideSpec(
            vendor="test",
            allowed_keys=frozenset({"alpha", "beta"}),
        )
        errors = spec.validate({"gamma": "value"})
        assert "alpha" in errors[0]
        assert "beta" in errors[0]


class TestClaudeCodeOverrideSpec:
    """Tests for the CLAUDE_CODE_OVERRIDE_SPEC constant."""

    def test_vendor_is_claude_code(self) -> None:
        assert CLAUDE_CODE_OVERRIDE_SPEC.vendor == "claude_code"

    def test_allows_permission_mode(self) -> None:
        errors = CLAUDE_CODE_OVERRIDE_SPEC.validate({"permissionMode": "bypassPermissions"})
        assert errors == []

    def test_allows_background(self) -> None:
        errors = CLAUDE_CODE_OVERRIDE_SPEC.validate({"background": True})
        assert errors == []

    def test_allows_max_turns(self) -> None:
        errors = CLAUDE_CODE_OVERRIDE_SPEC.validate({"maxTurns": 5})
        assert errors == []

    def test_allows_isolation(self) -> None:
        errors = CLAUDE_CODE_OVERRIDE_SPEC.validate({"isolation": "worktree"})
        assert errors == []

    def test_allows_skills(self) -> None:
        errors = CLAUDE_CODE_OVERRIDE_SPEC.validate({"skills": ["skill-a"]})
        assert errors == []

    def test_allows_hooks(self) -> None:
        errors = CLAUDE_CODE_OVERRIDE_SPEC.validate({"hooks": {"pre": "cmd"}})
        assert errors == []

    def test_allows_memory(self) -> None:
        errors = CLAUDE_CODE_OVERRIDE_SPEC.validate({"memory": "project"})
        assert errors == []

    def test_blocks_constitution(self) -> None:
        errors = CLAUDE_CODE_OVERRIDE_SPEC.validate({"constitution": {"evil": True}})
        assert len(errors) == 1

    def test_blocks_guardrails(self) -> None:
        errors = CLAUDE_CODE_OVERRIDE_SPEC.validate({"guardrails": {}})
        assert len(errors) == 1

    def test_blocks_enforcement(self) -> None:
        errors = CLAUDE_CODE_OVERRIDE_SPEC.validate({"enforcement": {}})
        assert len(errors) == 1

    def test_blocks_capabilities(self) -> None:
        errors = CLAUDE_CODE_OVERRIDE_SPEC.validate({"capabilities": {}})
        assert len(errors) == 1

    def test_blocks_persona(self) -> None:
        errors = CLAUDE_CODE_OVERRIDE_SPEC.validate({"persona": {}})
        assert len(errors) == 1

    def test_blocks_version(self) -> None:
        errors = CLAUDE_CODE_OVERRIDE_SPEC.validate({"version": "2.0.0"})
        assert len(errors) == 1

    def test_all_allowed_keys_at_once(self) -> None:
        overrides = {
            "permissionMode": "default",
            "background": True,
            "maxTurns": 10,
            "isolation": "worktree",
            "skills": [],
            "hooks": {},
            "memory": "user",
        }
        errors = CLAUDE_CODE_OVERRIDE_SPEC.validate(overrides)
        assert errors == []
