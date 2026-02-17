# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Application Layer - Use Cases & Orchestration

This layer orchestrates domain objects to perform use cases.
Implements CQRS (Command Query Responsibility Segregation).

Components:
    - use_cases/commands/: Write operations (imperative, change state)
    - use_cases/queries/: Read operations (return DTOs, no side effects)
    - dtos/: Data Transfer Objects for query results
    - dispatcher/: Event dispatcher interface

Rules:
    1. May import from domain/ only
    2. NO imports from infrastructure/ or interface/
    3. Commands return None or domain events
    4. Queries return DTOs, never domain entities
    5. Use cases depend on ports, not concrete adapters
"""
