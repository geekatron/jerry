# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Jerry Framework — Quality enforcement with je ne sais quoi.

Named for a framework. Inspired by a person who demonstrated
that taking your work seriously and taking yourself seriously
are two different things.

"Up to my death I would just keep doing fun things."
— Shane McConkey, 8th grade essay

Architecture: Hexagonal (Ports & Adapters) with Domain-Driven Design.

Layers:
    - domain/: Pure business logic, no external dependencies
    - application/: Use cases, CQRS command/query handlers
    - infrastructure/: Adapters for persistence, messaging, schemas
    - interface/: Primary adapters (CLI, API)

Design Principles:
    - Zero/minimal external dependencies (stdlib-first)
    - Dependency inversion: outer layers depend on inner layers
    - Ports define contracts, adapters implement them
    - Domain events for loose coupling

References:
    - Cockburn, A. (2005). "Hexagonal Architecture"
      https://alistair.cockburn.us/hexagonal-architecture/
    - Evans, E. (2003). "Domain-Driven Design"
"""

try:
    from importlib.metadata import version

    __version__ = version("jerry")
except Exception:
    __version__ = "dev"

__author__ = "Jerry Framework Contributors"
