"""ParseTranscriptCommand - Command to parse a transcript file.

This command instructs the system to parse a transcript file (VTT/SRT)
and optionally generate chunked output.

References:
    - TDD-FEAT-004 Section 11: Jerry CLI Integration
    - TASK-251: Implement CLI Transcript Namespace
    - EN-020: Python Parser Implementation
    - EN-021: Chunking Strategy
    - TASK-420: Add CLI parameters for model selection
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.transcript.domain.value_objects.model_config import ModelConfig


@dataclass(frozen=True)
class ParseTranscriptCommand:
    """Command to parse a transcript file.

    Attributes:
        path: Path to the transcript file (VTT or SRT)
        format: Input format ('vtt', 'srt', or 'auto')
        output_dir: Output directory (None = same as input)
        chunk_size: Number of segments per chunk (default: 500, deprecated)
        target_tokens: Target tokens per chunk (default: 18000, recommended)
        generate_chunks: Whether to generate chunk files (default: True)
        model_config: Model configuration for transcript agents (default: None)

    Note:
        target_tokens takes precedence over chunk_size when both are set.
        Using chunk_size without target_tokens is deprecated per EN-026.

        model_config is optional; if None, default models will be used.
        See ModelConfig for default model selections per agent.
    """

    path: str
    format: str = "auto"
    output_dir: str | None = None
    chunk_size: int = 500
    target_tokens: int | None = 18000  # EN-026: Default to token-based chunking
    generate_chunks: bool = True
    model_config: ModelConfig | None = None  # TASK-420: Model selection capability
