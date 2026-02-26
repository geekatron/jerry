# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for DefaultsComposer domain service."""

from __future__ import annotations

from src.agents.domain.services.defaults_composer import DefaultsComposer

# ---------------------------------------------------------------------------
# deep_merge()
# ---------------------------------------------------------------------------


class TestDeepMerge:
    """Tests for DefaultsComposer.deep_merge()."""

    def test_scalar_override(self) -> None:
        base = {"model": "sonnet", "version": "1.0.0"}
        override = {"model": "opus"}
        result = DefaultsComposer.deep_merge(base, override)
        assert result["model"] == "opus"
        assert result["version"] == "1.0.0"

    def test_dict_recursive_merge(self) -> None:
        base = {"persona": {"tone": "professional", "style": "consultative"}}
        override = {"persona": {"tone": "technical"}}
        result = DefaultsComposer.deep_merge(base, override)
        assert result["persona"]["tone"] == "technical"
        assert result["persona"]["style"] == "consultative"

    def test_array_replacement(self) -> None:
        base = {"tools": ["Read", "Write", "Grep"]}
        override = {"tools": ["Read"]}
        result = DefaultsComposer.deep_merge(base, override)
        assert result["tools"] == ["Read"]

    def test_new_keys_added(self) -> None:
        base = {"a": 1}
        override = {"b": 2}
        result = DefaultsComposer.deep_merge(base, override)
        assert result == {"a": 1, "b": 2}

    def test_deeply_nested_merge(self) -> None:
        base = {"a": {"b": {"c": 1, "d": 2}}}
        override = {"a": {"b": {"c": 99}}}
        result = DefaultsComposer.deep_merge(base, override)
        assert result["a"]["b"]["c"] == 99
        assert result["a"]["b"]["d"] == 2

    def test_override_dict_with_scalar(self) -> None:
        base = {"persona": {"tone": "professional"}}
        override = {"persona": "none"}
        result = DefaultsComposer.deep_merge(base, override)
        assert result["persona"] == "none"

    def test_override_scalar_with_dict(self) -> None:
        base = {"persona": "none"}
        override = {"persona": {"tone": "technical"}}
        result = DefaultsComposer.deep_merge(base, override)
        assert result["persona"] == {"tone": "technical"}

    def test_empty_override_returns_base(self) -> None:
        base = {"model": "sonnet"}
        result = DefaultsComposer.deep_merge(base, {})
        assert result == {"model": "sonnet"}

    def test_empty_base_returns_override(self) -> None:
        override = {"model": "opus"}
        result = DefaultsComposer.deep_merge({}, override)
        assert result == {"model": "opus"}

    def test_modifies_base_in_place(self) -> None:
        base = {"a": 1}
        result = DefaultsComposer.deep_merge(base, {"b": 2})
        assert result is base


# ---------------------------------------------------------------------------
# substitute_config_vars()
# ---------------------------------------------------------------------------


class TestSubstituteConfigVars:
    """Tests for DefaultsComposer.substitute_config_vars()."""

    def test_string_substitution(self) -> None:
        def resolver(key: str) -> str | None:
            return "my-project" if key == "jerry.project.name" else None

        result = DefaultsComposer.substitute_config_vars(
            "Project: ${jerry.project.name}",
            resolver,
        )
        assert result == "Project: my-project"

    def test_unresolved_left_as_is(self) -> None:
        def resolver(_key: str) -> str | None:
            return None

        result = DefaultsComposer.substitute_config_vars(
            "${jerry.unknown.var}",
            resolver,
        )
        assert result == "${jerry.unknown.var}"

    def test_dict_recursive_substitution(self) -> None:
        def resolver(key: str) -> str | None:
            return "val" if key == "jerry.test" else None

        data = {"a": "${jerry.test}", "b": {"c": "${jerry.test}"}}
        result = DefaultsComposer.substitute_config_vars(data, resolver)
        assert result == {"a": "val", "b": {"c": "val"}}

    def test_list_substitution(self) -> None:
        def resolver(key: str) -> str | None:
            return "resolved" if key == "jerry.x" else None

        data = ["${jerry.x}", "literal", "${jerry.unknown}"]
        result = DefaultsComposer.substitute_config_vars(data, resolver)
        assert result == ["resolved", "literal", "${jerry.unknown}"]

    def test_non_string_passthrough(self) -> None:
        def resolver(_key: str) -> str | None:
            return None

        assert DefaultsComposer.substitute_config_vars(42, resolver) == 42
        assert DefaultsComposer.substitute_config_vars(True, resolver) is True
        assert DefaultsComposer.substitute_config_vars(None, resolver) is None

    def test_multiple_vars_in_string(self) -> None:
        def resolver(key: str) -> str | None:
            return {"jerry.a": "X", "jerry.b": "Y"}.get(key)

        result = DefaultsComposer.substitute_config_vars(
            "${jerry.a}-${jerry.b}",
            resolver,
        )
        assert result == "X-Y"


# ---------------------------------------------------------------------------
# compose()
# ---------------------------------------------------------------------------


class TestCompose:
    """Tests for DefaultsComposer.compose()."""

    def test_compose_merges_defaults_and_overrides(self) -> None:
        defaults = {"permissionMode": "default", "background": False}
        agent_config = {"permissionMode": "bypassPermissions", "name": "my-agent"}
        result = DefaultsComposer.compose(defaults, agent_config)
        assert result["permissionMode"] == "bypassPermissions"
        assert result["background"] is False
        assert result["name"] == "my-agent"

    def test_compose_does_not_modify_defaults(self) -> None:
        defaults = {"persona": {"tone": "professional"}}
        agent_config = {"persona": {"tone": "technical"}}
        DefaultsComposer.compose(defaults, agent_config)
        assert defaults["persona"]["tone"] == "professional"

    def test_compose_with_resolver(self) -> None:
        defaults = {"project": "${jerry.project.name}"}
        agent_config = {}

        def resolver(key: str) -> str | None:
            return "PROJ-012" if key == "jerry.project.name" else None

        result = DefaultsComposer.compose(defaults, agent_config, resolver)
        assert result["project"] == "PROJ-012"

    def test_compose_without_resolver(self) -> None:
        defaults = {"project": "${jerry.project.name}"}
        agent_config = {}
        result = DefaultsComposer.compose(defaults, agent_config)
        assert result["project"] == "${jerry.project.name}"

    def test_compose_full_realistic_scenario(self) -> None:
        """Simulate real composition: defaults + agent config."""
        defaults = {
            "permissionMode": "default",
            "background": False,
            "version": "1.0.0",
            "persona": {
                "tone": "professional",
                "communication_style": "consultative",
                "audience_level": "adaptive",
            },
            "guardrails": {
                "output_filtering": [
                    "no_secrets_in_output",
                    "no_executable_code_without_confirmation",
                ],
                "fallback_behavior": "warn_and_retry",
            },
        }
        agent_config = {
            "name": "ps-researcher",
            "description": "Research agent",
            "model": "opus",
            "persona": {"tone": "technical"},
            "guardrails": {
                "output_filtering": [
                    "no_secrets_in_output",
                    "source_authority_tier_required",
                ],
            },
        }
        result = DefaultsComposer.compose(defaults, agent_config)

        # Scalars: agent wins
        assert result["name"] == "ps-researcher"
        assert result["model"] == "opus"
        # Deep merge: unspecified persona fields inherited
        assert result["persona"]["tone"] == "technical"
        assert result["persona"]["communication_style"] == "consultative"
        # Arrays: agent replaces entirely
        assert result["guardrails"]["output_filtering"] == [
            "no_secrets_in_output",
            "source_authority_tier_required",
        ]
        # Inherited defaults
        assert result["permissionMode"] == "default"
        assert result["background"] is False


# ---------------------------------------------------------------------------
# compose_layered()
# ---------------------------------------------------------------------------


class TestComposeLayered:
    """Tests for DefaultsComposer.compose_layered()."""

    def test_four_layer_precedence(self) -> None:
        governance = {"permissionMode": "default", "persona": {"tone": "professional"}}
        vendor = {"permissionMode": "default", "background": False}
        agent = {"name": "test-agent", "persona": {"tone": "technical"}}
        overrides = {"permissionMode": "bypassPermissions"}

        result = DefaultsComposer.compose_layered(governance, vendor, agent, overrides)

        assert result["permissionMode"] == "bypassPermissions"
        assert result["name"] == "test-agent"
        assert result["persona"]["tone"] == "technical"
        assert result["background"] is False

    def test_deep_merge_across_layers(self) -> None:
        governance = {"persona": {"tone": "professional", "style": "consultative"}}
        vendor = {"persona": {"vendor_field": "vendor_val"}}
        agent = {"persona": {"tone": "technical"}}

        result = DefaultsComposer.compose_layered(governance, vendor, agent)

        assert result["persona"]["tone"] == "technical"
        assert result["persona"]["style"] == "consultative"
        assert result["persona"]["vendor_field"] == "vendor_val"

    def test_empty_overrides_omitted(self) -> None:
        governance = {"a": 1}
        vendor = {"b": 2}
        agent = {"c": 3}

        result = DefaultsComposer.compose_layered(governance, vendor, agent)

        assert result == {"a": 1, "b": 2, "c": 3}

    def test_none_overrides_omitted(self) -> None:
        governance = {"a": 1}
        vendor = {"b": 2}
        agent = {"c": 3}

        result = DefaultsComposer.compose_layered(governance, vendor, agent, None)

        assert result == {"a": 1, "b": 2, "c": 3}

    def test_array_replacement_across_layers(self) -> None:
        governance = {"tools": ["Read", "Write", "Grep"]}
        vendor = {}
        agent = {"tools": ["Read"]}

        result = DefaultsComposer.compose_layered(governance, vendor, agent)

        assert result["tools"] == ["Read"]

    def test_does_not_modify_governance_defaults(self) -> None:
        governance = {"persona": {"tone": "professional"}}
        vendor = {"background": False}
        agent = {"persona": {"tone": "technical"}}
        overrides = {"background": True}

        DefaultsComposer.compose_layered(governance, vendor, agent, overrides)

        assert governance["persona"]["tone"] == "professional"

    def test_with_resolver(self) -> None:
        governance = {"project": "${jerry.project.name}"}
        vendor = {}
        agent = {}

        def resolver(key: str) -> str | None:
            return "PROJ-012" if key == "jerry.project.name" else None

        result = DefaultsComposer.compose_layered(governance, vendor, agent, resolver=resolver)

        assert result["project"] == "PROJ-012"

    def test_vendor_overrides_win_over_agent(self) -> None:
        governance = {}
        vendor = {}
        agent = {"maxTurns": 10}
        overrides = {"maxTurns": 5}

        result = DefaultsComposer.compose_layered(governance, vendor, agent, overrides)

        assert result["maxTurns"] == 5

    def test_realistic_four_layer_scenario(self) -> None:
        governance = {
            "version": "1.0.0",
            "persona": {"tone": "professional", "communication_style": "consultative"},
            "guardrails": {
                "output_filtering": ["no_secrets", "no_exec"],
                "fallback_behavior": "warn_and_retry",
            },
            "constitution": {"principles_applied": ["P-003", "P-020", "P-022"]},
        }
        vendor = {"permissionMode": "default", "background": False}
        agent = {
            "name": "ps-architect",
            "model": "opus",
            "persona": {"tone": "analytical"},
        }
        overrides = {"maxTurns": 5, "background": True}

        result = DefaultsComposer.compose_layered(governance, vendor, agent, overrides)

        assert result["name"] == "ps-architect"
        assert result["model"] == "opus"
        assert result["permissionMode"] == "default"
        assert result["background"] is True
        assert result["maxTurns"] == 5
        assert result["persona"]["tone"] == "analytical"
        assert result["persona"]["communication_style"] == "consultative"
        assert result["constitution"]["principles_applied"] == ["P-003", "P-020", "P-022"]
