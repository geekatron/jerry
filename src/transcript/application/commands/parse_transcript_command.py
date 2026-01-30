"""ParseTranscriptCommand - Command to parse a transcript file.

This command instructs the system to parse a transcript file (VTT/SRT)
and optionally generate chunked output.

References:
    - TDD-FEAT-004 Section 11: Jerry CLI Integration
    - TASK-251: Implement CLI Transcript Namespace
    - EN-020: Python Parser Implementation
    - EN-021: Chunking Strategy
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ParseTranscriptCommand:
    """Command to parse a transcript file.

    Attributes:
        path: Path to the transcript file (VTT or SRT)
        format: Input format ('vtt', 'srt', or 'auto')
        output_dir: Output directory (None = same as input)
        chunk_size: Number of segments per chunk (default: 500)
        generate_chunks: Whether to generate chunk files (default: True)
    """

    path: str
    format: str = "auto"
    output_dir: str | None = None
    chunk_size: int = 500
    generate_chunks: bool = True
