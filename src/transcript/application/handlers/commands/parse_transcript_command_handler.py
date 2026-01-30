"""ParseTranscriptCommandHandler - Command handler for transcript parsing.

Orchestrates VTTParser and TranscriptChunker to process transcript files.

References:
    - TDD-FEAT-004 Section 11.4: Bootstrap Wiring
    - TASK-251: Implement CLI Transcript Namespace
    - EN-020: Python Parser Implementation
    - EN-021: Chunking Strategy
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from src.transcript.application.commands import ParseTranscriptCommand
from src.transcript.application.results import ParseTranscriptResult

if TYPE_CHECKING:
    from src.transcript.application.services.chunker import TranscriptChunker
    from src.transcript.infrastructure.adapters.vtt_parser import VTTParser


class ParseTranscriptCommandHandler:
    """Handler for ParseTranscriptCommand.

    Orchestrates the parsing and chunking of transcript files:
    1. Parses the transcript using the appropriate parser
    2. Optionally generates chunked output with index

    Attributes:
        _vtt_parser: Parser for VTT format files
        _chunker: Chunker service for creating index + chunk files

    References:
        - TDD-FEAT-004 Section 11.4: Bootstrap Wiring
        - EN-020: Python Parser Implementation
        - EN-021: Chunking Strategy
    """

    def __init__(
        self,
        vtt_parser: VTTParser,
        chunker: TranscriptChunker,
    ) -> None:
        """Initialize handler with parser and chunker.

        Args:
            vtt_parser: VTT format parser
            chunker: Transcript chunker service
        """
        self._vtt_parser = vtt_parser
        self._chunker = chunker

    def handle(self, command: ParseTranscriptCommand) -> ParseTranscriptResult:
        """Execute the parse transcript command.

        Args:
            command: The parse command with file path and options

        Returns:
            ParseTranscriptResult with success/failure and output paths
        """
        try:
            # Determine output directory
            if command.output_dir:
                output_dir = Path(command.output_dir)
            else:
                output_dir = Path(command.path).parent / "output"

            output_dir.mkdir(parents=True, exist_ok=True)

            # Detect format and parse
            detected_format = self._detect_format(command.path, command.format)

            if detected_format != "vtt":
                return ParseTranscriptResult(
                    success=False,
                    detected_format=detected_format,
                    error={
                        "code": "UNSUPPORTED_FORMAT",
                        "message": f"Format '{detected_format}' not yet supported. Only VTT is currently implemented.",
                    },
                )

            # Parse the VTT file
            parse_result = self._vtt_parser.parse(command.path)

            if parse_result.parse_status == "failed":
                return ParseTranscriptResult(
                    success=False,
                    detected_format=detected_format,
                    error={
                        "code": "PARSE_ERROR",
                        "message": parse_result.errors[0]["message"] if parse_result.errors else "Unknown parse error",
                    },
                )

            # Save canonical JSON
            canonical_path = output_dir / "canonical-transcript.json"
            canonical_data = {
                "format": parse_result.format,
                "encoding": parse_result.encoding,
                "duration_ms": parse_result.duration_ms,
                "segment_count": len(parse_result.segments),
                "segments": [
                    {
                        "id": seg.id,
                        "start_ms": seg.start_ms,
                        "end_ms": seg.end_ms,
                        "speaker": seg.speaker,
                        "text": seg.text,
                        "raw_text": seg.raw_text,
                    }
                    for seg in parse_result.segments
                ],
            }
            canonical_path.write_text(json.dumps(canonical_data, indent=2))

            # Generate chunks if requested
            index_path = None
            chunk_count = 0

            if command.generate_chunks and parse_result.segments:
                # EN-026: Use token-based chunking by default (BUG-001 fix)
                from src.transcript.application.services.chunker import TranscriptChunker

                chunker = TranscriptChunker(
                    chunk_size=command.chunk_size,
                    target_tokens=command.target_tokens,
                )
                index_path = chunker.chunk(parse_result.segments, str(output_dir))

                # Count chunks from index
                index_data = json.loads(Path(index_path).read_text())
                chunk_count = index_data.get("total_chunks", 0)

            # Collect warnings
            warnings = []
            if parse_result.warnings:
                warnings.extend([w.get("message", str(w)) for w in parse_result.warnings])
            if parse_result.parse_status == "partial":
                warnings.append("Partial parse: some segments may be missing")

            return ParseTranscriptResult(
                success=True,
                detected_format=detected_format,
                canonical_path=str(canonical_path),
                index_path=index_path,
                segment_count=len(parse_result.segments),
                chunk_count=chunk_count,
                warnings=warnings,
            )

        except FileNotFoundError as e:
            return ParseTranscriptResult(
                success=False,
                error={
                    "code": "FILE_NOT_FOUND",
                    "message": str(e),
                },
            )
        except Exception as e:
            return ParseTranscriptResult(
                success=False,
                error={
                    "code": "INTERNAL_ERROR",
                    "message": str(e),
                },
            )

    def _detect_format(self, file_path: str, format_hint: str) -> str:
        """Detect the transcript format.

        Args:
            file_path: Path to the transcript file
            format_hint: Format hint from command ('auto', 'vtt', 'srt', 'txt')

        Returns:
            Detected format string
        """
        if format_hint != "auto":
            return format_hint

        # Auto-detect from extension
        path = Path(file_path)
        ext = path.suffix.lower()

        format_map = {
            ".vtt": "vtt",
            ".srt": "srt",
            ".txt": "txt",
        }

        return format_map.get(ext, "txt")
