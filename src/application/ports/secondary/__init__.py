"""
Secondary Ports - Application Layer.

Secondary ports define contracts for outbound dependencies
that handlers need to fulfill their responsibilities.

These are "driven" ports that the application layer uses to:
- Persist data (repositories)
- Read materialized views (read model stores)
- Send notifications
- Access external services
"""

from __future__ import annotations

from src.application.ports.secondary.illm_context_serializer import (
    ILlmContextSerializer,
    OutputFormat,
)
from src.application.ports.secondary.iread_model_store import IReadModelStore

__all__ = [
    "ILlmContextSerializer",
    "IReadModelStore",
    "OutputFormat",
]
