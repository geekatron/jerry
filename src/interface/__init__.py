"""
Interface Layer - Primary Adapters (Driving)

This layer contains adapters that DRIVE the application.
These are entry points from the outside world.

Components:
    - cli/: Command-line interface adapter
    - api/: HTTP API adapter (FastAPI/Flask if needed)

Rules:
    1. May import from all inner layers
    2. Translates external input to application commands
    3. Translates application DTOs to external output format
    4. Handles authentication, rate limiting, etc.
    5. NO business logic - delegate to application layer
"""
