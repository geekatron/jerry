"""ParseTranscriptResult - Result from parsing a transcript file.

This result contains the outcome of a transcript parse operation,
including success/failure status, output paths, and statistics.

References:
    - TDD-FEAT-004 Section 11.3: CLIAdapter Method
    - TASK-251: Implement CLI Transcript Namespace
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ParseTranscriptResult:
    """Result from parsing a transcript file.

    Attributes:
        success: Whether the parse operation succeeded
        detected_format: The detected format (vtt, srt, txt)
        canonical_path: Path to the canonical JSON output (if generated)
        index_path: Path to the index.json (if chunking was enabled)
        segment_count: Number of segments parsed
        chunk_count: Number of chunks generated
        warnings: List of warning messages
        error: Error details if success=False
    """

    success: bool
    detected_format: str | None = None
    canonical_path: str | None = None
    index_path: str | None = None
    segment_count: int = 0
    chunk_count: int = 0
    warnings: list[str] = field(default_factory=list)
    error: dict[str, str] | None = None
