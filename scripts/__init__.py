"""
Jerry Framework - Session Start Hook Scripts

This package implements the project enforcement mechanism for Jerry Framework.
It follows Hexagonal Architecture (Ports & Adapters) with DDD principles.

Architecture:
    - domain/: Pure domain models (no external dependencies)
    - application/: Use cases and port interfaces (CQRS pattern)
    - infrastructure/: Adapter implementations
    - session_start.py: Entry point (Interface layer)
"""
