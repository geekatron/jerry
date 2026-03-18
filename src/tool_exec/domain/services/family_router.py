# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Family router service for dispatching tool commands to resolvers.

Routes tool commands to the appropriate family resolver, supporting both
explicit family selection via --family flag and auto-detection via the
can_resolve() probe on each registered resolver.

References:
    - ADR-PROJ023-001: Multi-family plugin architecture
    - TASK-002: FamilyRouterService
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from src.shared_kernel.exceptions import NotFoundError

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from src.tool_exec.domain.ports.tool_family_resolver_port import (
        ToolFamilyResolverPort,
    )
    from src.tool_exec.domain.value_objects.tool_resolution_entry import (
        ToolResolutionEntry,
    )


class FamilyRouterService:
    """Routes tool commands to the appropriate family resolver.

    Supports two dispatch modes:
    1. Explicit: When --family is specified, routes directly to that resolver.
    2. Auto-detect: Probes each registered resolver via can_resolve() and
       uses the first match.

    The router does not depend on any specific family implementation,
    operating purely through the ToolFamilyResolverPort interface.
    """

    def __init__(self, resolvers: dict[str, ToolFamilyResolverPort]) -> None:
        """Initialize the family router with registered resolvers.

        Args:
            resolvers: Mapping of family name to resolver instance.
                Keys are family identifiers (e.g., 'rainbow'), values are
                concrete implementations of ToolFamilyResolverPort.
        """
        self._resolvers = resolvers

    def resolve(
        self,
        tool_command: str,
        family: str | None = None,
    ) -> ToolResolutionEntry:
        """Resolve a tool command through the appropriate family.

        Dispatch precedence:
        1. Explicit --family flag: route directly to named resolver.
        2. Auto-detect: probe each resolver via can_resolve(); use first match.

        Args:
            tool_command: The tool command to resolve (e.g., 'nuclei', 'trivy').
            family: Optional explicit family name to route to.

        Returns:
            ToolResolutionEntry with execution metadata.

        Raises:
            NotFoundError: If no resolver can handle the tool command,
                or if the specified family is not registered.
        """
        if family is not None:
            return self._resolve_explicit(tool_command, family)
        return self._resolve_auto(tool_command)

    def list_families(self) -> list[str]:
        """List all registered family names.

        Returns:
            Sorted list of registered family identifiers.
        """
        return sorted(self._resolvers.keys())

    def _resolve_explicit(
        self,
        tool_command: str,
        family: str,
    ) -> ToolResolutionEntry:
        """Resolve via explicitly specified family.

        Args:
            tool_command: The tool command to resolve.
            family: The family name to use.

        Returns:
            ToolResolutionEntry from the specified family's resolver.

        Raises:
            NotFoundError: If the family is not registered or cannot resolve
                the tool command.
        """
        resolver = self._resolvers.get(family)
        if resolver is None:
            registered = ", ".join(sorted(self._resolvers.keys()))
            raise NotFoundError(
                entity_type="ToolFamily",
                entity_id=f"{family} (registered: {registered})",
            )
        return resolver.resolve(tool_command)

    def _resolve_auto(self, tool_command: str) -> ToolResolutionEntry:
        """Auto-detect the family by probing each resolver.

        Iterates through registered resolvers and returns the first match.

        Args:
            tool_command: The tool command to resolve.

        Returns:
            ToolResolutionEntry from the first matching resolver.

        Raises:
            NotFoundError: If no registered resolver can handle the tool command.
        """
        for resolver in self._resolvers.values():
            if resolver.can_resolve(tool_command):
                # FM-006: Log auto-detection decision so operators can trace
                # which family claimed the tool without reading source code.
                # Traceability requirement: CLI invocation -> family selection
                # must produce an observable signal (OWASP A09:2021).
                logger.info(
                    "Auto-detected '%s' -> family '%s'",
                    tool_command,
                    resolver.FAMILY_NAME,
                )
                return resolver.resolve(tool_command)

        families = ", ".join(sorted(self._resolvers.keys()))
        raise NotFoundError(
            entity_type="Tool",
            entity_id=f"{tool_command} (searched families: {families})",
        )
