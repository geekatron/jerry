"""
Jerry Framework

A framework for behavior and workflow guardrails with knowledge accrual.
Implements Hexagonal Architecture (Ports & Adapters) with Domain-Driven Design.

Architecture Layers:
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
