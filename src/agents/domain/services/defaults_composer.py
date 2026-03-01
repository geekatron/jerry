# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
DefaultsComposer - Pure business logic for defaults composition.

Merges base defaults with per-agent configuration overrides and
substitutes ${jerry.*} config variables. No I/O — pure functions.

Merge semantics (from jerry-claude-agent-defaults.yaml):
  - Scalars: agent overrides base
  - Objects: deep merge (agent keys override base keys; unspecified inherited)
  - Arrays: agent replaces base entirely (no append)

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
    - ADR-PROJ010-003: LLM Portability Architecture
"""

from __future__ import annotations

import copy
import re
from collections.abc import Callable
from typing import Any

# Pattern for ${jerry.*} config variable references
_CONFIG_VAR_RE = re.compile(r"\$\{(jerry\.[a-zA-Z0-9_.]+)\}")


class DefaultsComposer:
    """Composes agent configurations by merging defaults with overrides.

    Pure domain service with no I/O dependencies. All data is passed
    in as arguments.
    """

    @staticmethod
    def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
        """Deep merge two dicts. Override wins for scalars. Arrays replace entirely.

        Args:
            base: Base dictionary (modified in place).
            override: Override dictionary.

        Returns:
            Merged dictionary (same reference as base).
        """
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                DefaultsComposer.deep_merge(base[key], value)
            else:
                base[key] = value
        return base

    @staticmethod
    def substitute_config_vars(
        data: Any,
        resolver: Callable[[str], str | None],
    ) -> Any:
        """Recursively substitute ${jerry.*} config variables.

        Args:
            data: Data structure to process (dict, list, str, or scalar).
            resolver: Callable that takes a config key (e.g., 'jerry.project.name')
                and returns the resolved value, or None if unresolved.

        Returns:
            Data with config variables substituted. Unresolved tokens left as-is.
        """
        if isinstance(data, str):
            return DefaultsComposer._replace_vars_in_string(data, resolver)
        if isinstance(data, dict):
            return {
                k: DefaultsComposer.substitute_config_vars(v, resolver) for k, v in data.items()
            }
        if isinstance(data, list):
            return [DefaultsComposer.substitute_config_vars(item, resolver) for item in data]
        return data

    @staticmethod
    def compose(
        defaults: dict[str, Any],
        agent_config: dict[str, Any],
        resolver: Callable[[str], str | None] | None = None,
    ) -> dict[str, Any]:
        """Compose a full agent config from defaults and per-agent overrides.

        Args:
            defaults: Base defaults dictionary (not modified).
            agent_config: Per-agent override dictionary.
            resolver: Optional config variable resolver.

        Returns:
            Fully composed configuration dictionary.
        """
        composed = DefaultsComposer.deep_merge(copy.deepcopy(defaults), agent_config)

        if resolver is not None:
            composed = DefaultsComposer.substitute_config_vars(composed, resolver)

        return composed

    @staticmethod
    def compose_layered(
        governance_defaults: dict[str, Any],
        vendor_defaults: dict[str, Any],
        agent_config: dict[str, Any],
        vendor_overrides: dict[str, Any] | None = None,
        resolver: Callable[[str], str | None] | None = None,
    ) -> dict[str, Any]:
        """Compose a full agent config from 4 layers.

        Merge order:
          1. governance_defaults (Jerry governance)
          2. vendor_defaults (vendor-specific, e.g. Claude Code)
          3. agent_config (per-agent from adapter + governance + extra_yaml)
          4. vendor_overrides (per-agent vendor overrides)

        Each layer overrides the previous via deep_merge.

        Args:
            governance_defaults: Layer 1 - Jerry governance defaults (not modified).
            vendor_defaults: Layer 2 - Vendor-specific defaults (not modified).
            agent_config: Layer 3 - Per-agent configuration.
            vendor_overrides: Layer 4 - Per-agent vendor overrides (optional).
            resolver: Optional config variable resolver for ${jerry.*} substitution.

        Returns:
            Fully composed configuration dictionary.
        """
        composed = copy.deepcopy(governance_defaults)
        DefaultsComposer.deep_merge(composed, vendor_defaults)
        DefaultsComposer.deep_merge(composed, agent_config)

        if vendor_overrides:
            DefaultsComposer.deep_merge(composed, vendor_overrides)

        if resolver is not None:
            composed = DefaultsComposer.substitute_config_vars(composed, resolver)

        return composed

    @staticmethod
    def _replace_vars_in_string(
        value: str,
        resolver: Callable[[str], str | None],
    ) -> str:
        """Replace ${jerry.*} tokens in a string with resolved values.

        Args:
            value: String potentially containing ${jerry.*} tokens.
            resolver: Callable to resolve config keys.

        Returns:
            String with tokens replaced. Unresolved tokens left as-is.
        """

        def replacer(match: re.Match[str]) -> str:
            config_key = match.group(1)
            resolved = resolver(config_key)
            if resolved is not None:
                return str(resolved)
            return match.group(0)

        return _CONFIG_VAR_RE.sub(replacer, value)
