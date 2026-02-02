"""
Transcript Infrastructure Adapters.

Exports:
- VTTParser: WebVTT format parser using webvtt-py

Reference: TDD-FEAT-004-hybrid-infrastructure.md v1.2.0, Section 4
"""

from src.transcript.infrastructure.adapters.vtt_parser import VTTParser

__all__ = ["VTTParser"]
