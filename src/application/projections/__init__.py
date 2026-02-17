# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Projections - Read Model Builders.

Projections are handlers that transform domain events into
read-optimized data structures (read models/materialized views).

They listen to domain events and update denormalized views
that are optimized for query operations.

Architecture:
    Domain Events → Projection Handler → IReadModelStore → Read Models

Example:
    >>> class ProjectDashboardProjection:
    ...     def __init__(self, store: IReadModelStore):
    ...         self._store = store
    ...
    ...     def on_project_created(self, event: ProjectCreated) -> None:
    ...         self._store.save("project_dashboard", str(event.project_id), {
    ...             "id": str(event.project_id),
    ...             "name": event.name,
    ...             "created_at": event.created_at.isoformat(),
    ...         })
"""

from __future__ import annotations

# Projections will be added as the event-sourcing system matures
# Currently, this module provides the infrastructure foundation

__all__: list[str] = []
