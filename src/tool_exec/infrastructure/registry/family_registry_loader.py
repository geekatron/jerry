# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Family registry loader for dynamic plugin discovery.

Loads tool_families.yaml, dynamically imports resolver modules via importlib,
and validates that each resolver implements the ToolFamilyResolverPort interface.

References:
    - ADR-PROJ023-001: Multi-family plugin architecture
    - TASK-001D: FamilyRegistryLoader
"""

from __future__ import annotations

import importlib
import logging
from pathlib import Path

import yaml

from src.tool_exec.domain.ports.tool_family_resolver_port import (
    ToolFamilyResolverPort,
)
from src.tool_exec.domain.value_objects.tool_family_info import ToolFamilyInfo

logger = logging.getLogger(__name__)


class FamilyRegistryLoader:
    """Loads and instantiates tool family resolver plugins.

    Reads tool_families.yaml, imports each resolver module via importlib,
    validates that the resolver class implements ToolFamilyResolverPort,
    and returns a mapping of family name to resolver instance.

    The loader is designed for use at CLI startup time. It does not cache
    results; each call to load() produces fresh resolver instances.
    """

    def __init__(self, registry_path: str | Path) -> None:
        """Initialize the loader with the path to tool_families.yaml.

        Args:
            registry_path: Path to the tool families registry YAML file.
        """
        self._registry_path = Path(registry_path)

    def load(self) -> dict[str, ToolFamilyResolverPort]:
        """Load all enabled family resolvers from the registry.

        Reads tool_families.yaml, imports each enabled resolver module,
        instantiates the resolver class, and validates it implements the
        ToolFamilyResolverPort interface.

        Returns:
            Mapping of family name to resolver instance, including only
            families marked as enabled.

        Raises:
            FileNotFoundError: If tool_families.yaml does not exist.
            ValueError: If the YAML is malformed or a resolver does not
                implement ToolFamilyResolverPort.
        """
        families = self._parse_registry()
        resolvers: dict[str, ToolFamilyResolverPort] = {}

        for family_info in families:
            if not family_info.enabled:
                logger.info("Skipping disabled family: %s", family_info.name)
                continue

            try:
                resolver = self._load_resolver(family_info)
                resolvers[family_info.name] = resolver
                logger.info("Loaded family resolver: %s", family_info.name)
            except Exception:
                logger.exception("Failed to load family resolver: %s", family_info.name)
                raise

        return resolvers

    def list_families(self) -> list[ToolFamilyInfo]:
        """List all registered families without loading resolvers.

        Returns:
            List of ToolFamilyInfo for all families in the registry.

        Raises:
            FileNotFoundError: If tool_families.yaml does not exist.
        """
        return self._parse_registry()

    def _parse_registry(self) -> list[ToolFamilyInfo]:
        """Parse tool_families.yaml into ToolFamilyInfo objects.

        Returns:
            List of ToolFamilyInfo for each entry in the registry.

        Raises:
            FileNotFoundError: If the registry file does not exist.
            ValueError: If the YAML is malformed.
        """
        if not self._registry_path.exists():
            msg = f"Family registry not found: {self._registry_path}"
            raise FileNotFoundError(msg)

        with open(self._registry_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict) or "families" not in data:
            msg = (
                f"Family registry must be a YAML mapping with a 'families' key. "
                f"Got: {type(data).__name__}"
            )
            raise ValueError(msg)

        families: list[ToolFamilyInfo] = []
        for entry in data["families"]:
            families.append(
                ToolFamilyInfo(
                    name=entry["name"],
                    description=entry.get("description", ""),
                    resolver_module=entry["resolver_module"],
                    resolver_class=entry["resolver_class"],
                    config_path=entry["config_path"],
                    enabled=entry.get("enabled", True),
                )
            )

        return families

    def _load_resolver(self, family_info: ToolFamilyInfo) -> ToolFamilyResolverPort:
        """Dynamically import and instantiate a resolver.

        Args:
            family_info: Family descriptor with module and class names.

        Returns:
            Instantiated resolver implementing ToolFamilyResolverPort.

        Raises:
            ImportError: If the resolver module cannot be imported.
            AttributeError: If the resolver class is not found in the module.
            ValueError: If the resolver does not implement ToolFamilyResolverPort.
        """
        module = importlib.import_module(family_info.resolver_module)
        resolver_cls = getattr(module, family_info.resolver_class)

        if not issubclass(resolver_cls, ToolFamilyResolverPort):
            msg = (
                f"Resolver class {family_info.resolver_class} in module "
                f"{family_info.resolver_module} does not implement "
                f"ToolFamilyResolverPort"
            )
            raise ValueError(msg)

        return resolver_cls(config_path=family_info.config_path)  # type: ignore[call-arg]
