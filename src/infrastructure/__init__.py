"""
Infrastructure Layer - Adapters & Technical Concerns

This layer contains implementations of ports (secondary adapters)
and technical infrastructure.

Components:
    - persistence/sqlite/: SQLite adapter implementing IRepository
    - persistence/fs/: Filesystem adapter (Markdown-based storage)
    - messaging/protobuf/: Protocol buffer definitions for events
    - schemas/: JSON Schema contracts for validation
    - dispatcher/: Concrete event dispatcher implementation

Rules:
    1. May import from domain/ and application/
    2. NO imports from interface/
    3. Adapters MUST implement port interfaces
    4. Technical details (SQL, file formats) stay here
    5. Can use external libraries if needed (but prefer stdlib)
"""
