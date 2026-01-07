"""
Domain Layer - The Innermost Hexagon

This layer contains pure business logic with NO external dependencies.
All imports must be from Python stdlib or within this package.

Components:
    - aggregates/: Consistency boundaries (e.g., WorkItem, Project)
    - value_objects/: Immutable values (e.g., Status, Priority)
    - events/: Domain events (past tense, e.g., WorkItemCompleted)
    - ports/: Secondary port interfaces (IRepository, INotifier)
    - exceptions.py: Domain-specific errors

Rules:
    1. NO imports from application/, infrastructure/, or interface/
    2. NO imports from external packages (except stdlib)
    3. Entities enforce their own invariants
    4. Value objects are immutable
    5. Domain events are facts that happened
"""
