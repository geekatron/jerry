# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Transcript Domain Ports.

Exports:
- ITranscriptParser: Port interface for transcript parsing

Reference: TDD-FEAT-004-hybrid-infrastructure.md v1.2.0, Section 4
"""

from src.transcript.domain.ports.transcript_parser import ITranscriptParser

__all__ = ["ITranscriptParser"]
