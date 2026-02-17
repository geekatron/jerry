# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Serialization Adapters - Infrastructure Layer.

Provides serialization implementations for LLM context formatting:
- ToonSerializer: Token-Oriented Object Notation (30-60% token reduction)
- JsonSerializer: Standard JSON fallback

These adapters implement the ILlmContextSerializer port.

References:
    - impl-es-e-002-toon-serialization.md: TOON research
    - DISC-012: TOON Format Required as Primary Output
"""

from __future__ import annotations

from src.infrastructure.adapters.serialization.toon_serializer import ToonSerializer

__all__ = [
    "ToonSerializer",
]
