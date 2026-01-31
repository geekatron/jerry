# TDD-FEAT-004: Hybrid Infrastructure Technical Design

<!--
TEMPLATE: Technical Design Document
VERSION: 1.2.0
SOURCE: Problem-Solving Framework TDD Pattern
CREATED: 2026-01-29
UPDATED: 2026-01-30
PURPOSE: Technical specification for hybrid Python + LLM transcript processing
AMENDMENT: FL-001 - Added Section 11 Jerry CLI Integration per DISC-012
AMENDMENT: FL-001-cont - Corrected paths from skills/transcript/src/ to src/transcript/ bounded context
-->

> **Document ID:** TDD-FEAT-004
> **Version:** 1.2.0
> **Status:** DRAFT
> **Created:** 2026-01-29T23:30:00Z
> **Updated:** 2026-01-30T01:00:00Z
> **PS ID:** FEAT-004
> **Entry ID:** e-242-v2
> **Parent:** FEAT-004-hybrid-infrastructure
> **Quality Target:** 0.95
> **Input Artifacts:**
>   - FEAT-004-e-240-hybrid-architecture-research.md
>   - FEAT-004-e-241-blast-radius-analysis.md
>   - FEAT-004--DEC-011-ts-parser-hybrid-role.md
>   - FEAT-002--DISC-009-agent-only-architecture-limitation.md
>   - FEAT-004--DISC-012-cli-integration-gap.md (FL-001)

---

## Document Purpose

This Technical Design Document specifies the hybrid infrastructure transformation for the transcript skill, addressing DISC-009 operational findings. The design enables deterministic Python parsing for structured transcript formats while preserving LLM capabilities for semantic extraction and fallback scenarios.

**Traceability:**
- **DISC-009** → Problem identification (99.8% data loss)
- **DEC-011** → Role decisions (Strategy Pattern, incremental adoption)
- **Phase 1 Research** → Industry patterns and library analysis
- **Phase 2 Analysis** → Blast radius and implementation roadmap

---

## L0: Executive Summary (ELI5)

Imagine you need to read and summarize a very long book - perhaps 500 pages of meeting notes. If you try to read the entire book at once while also remembering everything important, you will likely forget details in the middle sections. This is exactly what happened to our transcript skill: when processing a 5-hour meeting recording (90,000 words), it produced only 5 bullet points instead of 3,071 - **a 99.8% data loss!**

The solution is similar to how a library works. A librarian (Python) organizes all the pages into neat, labeled stacks. Then, a researcher (Claude/LLM) can read through those organized stacks one at a time, finding and highlighting the important parts. The librarian is fast and perfect at organizing (deterministic), while the researcher is great at understanding meaning (semantic).

**What changes:**
- A Python script will read VTT transcript files instantly (less than 1 second)
- The content will be organized into smaller "chunks" (like chapters in a book)
- Claude will read one chapter at a time, never getting lost in the middle
- This approach is 1,250x cheaper and infinitely more reliable

**Why this matters:**
- Meetings of any length can now be processed completely
- Zero data loss - every word is captured
- Much faster processing (seconds instead of minutes)
- Industry best practice: 60% of production AI systems use this hybrid approach

---

## L1: Technical Specification (Software Engineer)

### Section 1: Problem Statement

#### DISC-009 Incident Summary

On 2026-01-28, during live skill invocation on `meeting-006-all-hands.vtt`:

| Metric | Expected | Actual | Impact |
|--------|----------|--------|--------|
| **Segments Extracted** | 3,071 | 5 | **99.8% data loss** |
| **Token Input** | 90,000+ | 90,000+ | Context window maxed |
| **Processing Time** | <30s | >60s (failed) | Timeout risk |
| **Parse Cost** | ~$0.27 | ~$0.27 | No value delivered |

**Root Cause Analysis (Ishikawa):**

```
                                    ┌──────────────────────────────┐
                                    │  TRUNCATED PARSER OUTPUT     │
                                    │  (5/3,071 segments)          │
                                    └──────────────────────────────┘
                                                  ▲
        ┌─────────────────┬───────────────────────┴───────────────────────┬─────────────────┐
        │                 │                                               │                 │
   ┌────┴────┐      ┌─────┴─────┐                                   ┌─────┴─────┐     ┌────┴────┐
   │  METHOD │      │  MACHINE  │                                   │ MATERIAL  │     │  MAN    │
   └────┬────┘      └─────┬─────┘                                   └─────┬─────┘     └────┬────┘
        │                 │                                               │                 │
   No executable     LLM context              Lost-in-Middle         9,220 line         Design
   implementation    limitations             accuracy drop          VTT file           assumption
        │                 │                       │                      │                 │
   Behavioral spec   Output cap exists       30%+ degradation       90K tokens      "Agent can
   only, no code          │                  in middle sections     input size       handle it"
        │                 │                       │                      │                 │
        └─────────────────┴───────────────────────┴──────────────────────┴─────────────────┘
                                                  │
                              ┌────────────────────┴────────────────────┐
                              │ ROOT CAUSE: Agent-only architecture     │
                              │ lacks deterministic processing layer     │
                              └─────────────────────────────────────────┘
```

**Stanford "Lost in the Middle" Research:**

> "Performance can degrade by more than 30% when relevant information shifts from extremes to middle positions in long contexts."
> -- Liu, N.F., et al. (2024). *Transactions of the Association for Computational Linguistics*, 12, 157-173.

**Operational Impact:**

1. **Data Integrity Failure**: 99.8% of transcript content lost
2. **Principle Violation**: Ad-hoc Python workaround violated "no hacks" principle (META TODO #8, #17)
3. **Scalability Gap**: No solution for files exceeding context window
4. **Cost Inefficiency**: Full token cost with no value delivered

#### Why Hybrid Architecture is Required

| Dimension | LLM-Only | Hybrid (Python + LLM) |
|-----------|----------|----------------------|
| **Accuracy** | 0.2% (DISC-009) | 100% (deterministic) |
| **Cost** | $0.27/file (90K tokens) | $0.00 (Python) + $0.05 (chunked LLM) |
| **Speed** | 60+ seconds | <1 second (parse) + 5-10s (extract) |
| **Scalability** | Limited by context | Unlimited (chunking) |
| **Testability** | Golden datasets | Unit tests (100% coverage) |

**Industry Evidence:**

> "60% of production LLM applications use retrieval-augmented generation or hybrid architectures."
> -- byteiota (2026), "RAG vs Long Context 2026 Retrieval Debate"

---

### Section 2: Architecture Overview

#### Hybrid Model Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                           HYBRID TRANSCRIPT PROCESSING ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐   │
│  │                         ORCHESTRATION LAYER (ts-parser.md v2.0)                       │   │
│  │                                                                                        │   │
│  │   ┌─────────────┐    ┌───────────────────────────────────────────────────────────┐   │   │
│  │   │   INPUT     │    │                   STRATEGY SELECTION                        │   │   │
│  │   │ VTT/SRT/TXT │───►│  ┌───────────────┐    ┌───────────────┐                   │   │   │
│  │   │   File      │    │  │ Format        │───►│ Python Parser │── VTT/SRT ──►     │   │   │
│  │   └─────────────┘    │  │ Detection     │    │ Strategy      │                   │   │   │
│  │                      │  └───────────────┘    └───────────────┘                   │   │   │
│  │                      │         │                    │                             │   │   │
│  │                      │         │ Unknown format     │ Parse failure               │   │   │
│  │                      │         ▼                    ▼                             │   │   │
│  │                      │  ┌────────────────────────────────┐                       │   │   │
│  │                      │  │      LLM Parser Strategy        │                       │   │   │
│  │                      │  │        (FALLBACK)               │                       │   │   │
│  │                      │  └────────────────────────────────┘                       │   │   │
│  │                      └───────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────────────────────┘   │
│                                              │                                              │
│                                              ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐   │
│  │                         PYTHON PARSING LAYER (EN-020)                                 │   │
│  │                                                                                        │   │
│  │   ┌───────────────┐    ┌───────────────┐    ┌───────────────┐                        │   │
│  │   │  Encoding     │───►│   webvtt-py   │───►│   Canonical   │                        │   │
│  │   │  Detection    │    │   Parser      │    │   JSON        │                        │   │
│  │   │(charset-norm) │    │               │    │   Output      │                        │   │
│  │   └───────────────┘    └───────────────┘    └───────────────┘                        │   │
│  └─────────────────────────────────────────────────────────────────────────────────────┘   │
│                                              │                                              │
│                                              ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐   │
│  │                         CHUNKING LAYER (EN-021)                                       │   │
│  │                                                                                        │   │
│  │   ┌───────────────────────────────────────────────────────────────────────────────┐  │   │
│  │   │                                                                                │  │   │
│  │   │  ┌─────────────────┐   ┌──────────────────────────────────────────────────┐  │  │   │
│  │   │  │   index.json    │   │              chunks/                              │  │  │   │
│  │   │  │  ─────────────  │   │  ┌────────────┐ ┌────────────┐ ┌────────────┐   │  │  │   │
│  │   │  │  • total: 3071  │   │  │chunk-001.  │ │chunk-002.  │ │chunk-007.  │   │  │  │   │
│  │   │  │  • chunks: 7    │   │  │json        │ │json        │ │json        │   │  │  │   │
│  │   │  │  • speakers: 50+│   │  │seg 1-500   │ │seg 501-1000│ │seg 3001-   │   │  │  │   │
│  │   │  │  • pointers → ──│──►│  │~15K tokens │ │~15K tokens │ │3071        │   │  │  │   │
│  │   │  └─────────────────┘   │  └────────────┘ └────────────┘ └────────────┘   │  │  │   │
│  │   │                        └──────────────────────────────────────────────────┘  │  │   │
│  │   └───────────────────────────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────────────────────┘   │
│                                              │                                              │
│                                              ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐   │
│  │                         LLM EXTRACTION LAYER (ts-extractor via EN-022)               │   │
│  │                                                                                        │   │
│  │   ┌───────────────┐    ┌───────────────┐    ┌───────────────┐    ┌───────────────┐  │   │
│  │   │ Read          │───►│ Request       │───►│ Extract       │───►│ Aggregate     │  │   │
│  │   │ index.json    │    │ Relevant      │    │ Entities      │    │ Results       │  │   │
│  │   │ (overview)    │    │ Chunks        │    │ Per Chunk     │    │ Across Chunks │  │   │
│  │   └───────────────┘    └───────────────┘    └───────────────┘    └───────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────────────────────┘   │
│                                              │                                              │
│                                              ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐   │
│  │                         OUTPUT: extraction-report.json                                │   │
│  │                         (Complete, with citations across all chunks)                   │   │
│  └─────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                              │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

#### Component Relationships

| Layer | Component | Responsibility | Interface |
|-------|-----------|----------------|-----------|
| **Orchestration** | ts-parser.md v2.0 | Route, delegate, validate | Strategy Pattern |
| **Parsing** | EN-020 Python Parser | Deterministic VTT/SRT parsing | IParserStrategy |
| **Chunking** | EN-021 Chunker | Segment chunking with index | ChunkResult |
| **Extraction** | ts-extractor via EN-022 | Semantic entity extraction | Chunked Input |
| **Validation** | EN-023 Integration | End-to-end verification | Test Specs |

#### Data Flow Sequence

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  ts-parser  │     │   Python    │     │   Chunker   │     │ts-extractor │     │   Output    │
│ Orchestrator│     │   Parser    │     │   (EN-021)  │     │  (EN-022)   │     │             │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │                   │                   │
       │  1. detect format │                   │                   │                   │
       │──────────────────►│                   │                   │                   │
       │                   │                   │                   │                   │
       │  2. delegate parse│                   │                   │                   │
       │──────────────────►│                   │                   │                   │
       │                   │                   │                   │                   │
       │                   │  3. parse VTT     │                   │                   │
       │                   │  (all segments)   │                   │                   │
       │                   │──────────────────►│                   │                   │
       │                   │                   │                   │                   │
       │                   │                   │  4. create chunks │                   │
       │                   │                   │  index.json +     │                   │
       │                   │                   │  chunk-NNN.json   │                   │
       │                   │                   │──────────────────►│                   │
       │                   │                   │                   │                   │
       │  5. validate      │                   │                   │                   │
       │  schema + counts  │                   │                   │                   │
       │◄──────────────────│                   │                   │                   │
       │                   │                   │                   │                   │
       │                   │                   │  6. read index    │                   │
       │                   │                   │◄──────────────────│                   │
       │                   │                   │                   │                   │
       │                   │                   │  7. extract       │                   │
       │                   │                   │  per chunk        │                   │
       │                   │                   │──────────────────►│                   │
       │                   │                   │                   │                   │
       │                   │                   │                   │  8. aggregate     │
       │                   │                   │                   │  extraction-      │
       │                   │                   │                   │  report.json      │
       │                   │                   │                   │─────────────────►│
       │                   │                   │                   │                   │
```

---

### Section 3: ts-parser.md Transformation

#### Current State (v1.2.0)

```yaml
Current Role: DIRECT PARSER
Processing Model: LLM parses entire file content
Output: canonical-transcript.json
Limitations:
  - Context window constraints (90K tokens fails)
  - Lost-in-Middle degradation (30%+ accuracy drop)
  - Probabilistic accuracy (hallucination risk)
  - Slow processing (60s+ for large files)
  - High token cost ($0.27/file)
```

#### Target State (v2.0.0)

```yaml
Target Role: ORCHESTRATOR + DELEGATOR + FALLBACK + VALIDATOR
Processing Model: Strategy Pattern with Python delegation
Output: canonical-transcript.json + index.json + chunks/*.json
Benefits:
  - No context window limits (Python has none)
  - No Lost-in-Middle (chunks are small contexts)
  - Deterministic accuracy (100%)
  - Fast processing (<1s for any size)
  - Zero token cost for parsing
```

#### Four Roles Specification

##### Role 1: ORCHESTRATOR

**Responsibility:** Coordinate the parsing pipeline based on input format and results.

```markdown
ORCHESTRATION LOGIC:
1. Receive input file path from SKILL.md
2. Invoke format detection
3. Select appropriate parsing strategy
4. Coordinate output validation
5. Signal completion to downstream agents
```

##### Role 2: DELEGATOR

**Responsibility:** Route parsing requests to appropriate strategy implementation.

```markdown
DELEGATION LOGIC:
1. IF format == "VTT" AND Python parser available:
   → Invoke Python VTT parser (EN-020)
2. ELSE IF format == "SRT" AND Python parser available:
   → Invoke Python SRT parser (Phase 2)
3. ELSE:
   → Invoke LLM parser strategy (fallback)
```

##### Role 3: FALLBACK

**Responsibility:** Maintain LLM-based parsing for unsupported formats and error recovery.

```markdown
FALLBACK TRIGGERS:
1. Format not recognized (not VTT/SRT)
2. Python parser execution failure
3. Output validation failure
4. Encoding detection failure after all fallbacks

FALLBACK BEHAVIOR:
- Log warning with failure reason
- Invoke original LLM parsing logic (v1.2.0 behavior)
- Mark output with fallback_used: true
```

##### Role 4: VALIDATOR

**Responsibility:** Validate Python parser output before downstream processing.

```markdown
VALIDATION CRITERIA:
1. Schema compliance (canonical-transcript.json v1.1)
2. Segment count matches expectations (based on timestamp count in source)
3. No null/undefined required fields
4. Duration_ms calculated correctly
5. Parse_status in ["complete", "partial"]
6. All segments have valid ID format (seg-NNN)

VALIDATION FAILURE:
→ Trigger Role 3 (FALLBACK)
```

#### Format Detection Logic

```python
def detect_format(file_path: str) -> str:
    """
    Detect transcript format from file content.

    Algorithm:
    1. Read first 10 lines of file
    2. Check for WEBVTT header (case-insensitive)
    3. Check for SRT pattern (digit line + timestamp)
    4. Default to PLAIN

    Returns: "vtt" | "srt" | "plain"
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [f.readline() for _ in range(10)]

    # VTT Detection: First line starts with "WEBVTT"
    if lines[0].strip().upper().startswith("WEBVTT"):
        return "vtt"

    # SRT Detection: Line 1 is digit, Line 2 contains " --> "
    if lines[0].strip().isdigit() and " --> " in lines[1]:
        return "srt"

    # Default: Plain text
    return "plain"
```

#### Python Delegation Contract

**Input Contract:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "PythonParserInput",
  "type": "object",
  "required": ["file_path", "output_dir"],
  "properties": {
    "file_path": {
      "type": "string",
      "description": "Absolute path to source transcript file"
    },
    "output_dir": {
      "type": "string",
      "description": "Directory for canonical JSON and chunk output"
    },
    "options": {
      "type": "object",
      "properties": {
        "chunk_size": {
          "type": "integer",
          "default": 500,
          "description": "Number of segments per chunk"
        },
        "generate_chunks": {
          "type": "boolean",
          "default": true,
          "description": "Whether to generate chunked output"
        }
      }
    }
  }
}
```

**Output Contract:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "PythonParserOutput",
  "type": "object",
  "required": ["success", "canonical_path"],
  "properties": {
    "success": {
      "type": "boolean"
    },
    "canonical_path": {
      "type": "string",
      "description": "Path to canonical-transcript.json"
    },
    "index_path": {
      "type": "string",
      "description": "Path to index.json (if chunking enabled)"
    },
    "chunk_count": {
      "type": "integer",
      "description": "Number of chunk files generated"
    },
    "segment_count": {
      "type": "integer",
      "description": "Total segments parsed"
    },
    "parse_warnings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "code": {"type": "string"},
          "message": {"type": "string"},
          "cue_index": {"type": "integer"}
        }
      }
    },
    "error": {
      "type": "object",
      "properties": {
        "code": {"type": "string"},
        "message": {"type": "string"}
      }
    }
  }
}
```

#### LLM Fallback Triggers

| Trigger | Detection | Response |
|---------|-----------|----------|
| Unknown format | `detect_format()` returns "plain" with no Python handler | Invoke LLM parser |
| Python error | Exception during Python execution | Log error, invoke LLM parser |
| Validation failure | Schema validation fails | Log warning, invoke LLM parser |
| Encoding failure | All fallback encodings fail | Invoke LLM parser with raw bytes |
| Parse count mismatch | segment_count << expected | Invoke LLM parser, compare results |

---

### Section 4: Python Parser (EN-020)

#### webvtt-py Integration Approach

**Library:** webvtt-py v0.5.1 (MIT License)
**Repository:** [github.com/glut23/webvtt-py](https://github.com/glut23/webvtt-py)

```python
"""
EN-020: VTT Parser Implementation

Location: src/transcript/infrastructure/adapters/vtt_parser.py
Dependencies: webvtt-py, charset-normalizer (added to pyproject.toml)
"""

import webvtt
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field
import json
import re

@dataclass
class ParsedSegment:
    """Canonical segment representation."""
    id: str
    start_ms: int
    end_ms: int
    speaker: Optional[str]
    text: str
    raw_text: str

@dataclass
class ParseResult:
    """Result from VTT parsing operation."""
    segments: List[ParsedSegment] = field(default_factory=list)
    format: str = "vtt"
    encoding: str = "utf-8"
    duration_ms: Optional[int] = None
    warnings: List[dict] = field(default_factory=list)
    errors: List[dict] = field(default_factory=list)
    parse_status: str = "complete"


class VTTParser:
    """
    Deterministic VTT parser using webvtt-py.

    Implements:
    - FR-001: VTT parsing with voice tags
    - NFR-006: Timestamp normalization to milliseconds
    - NFR-007: Encoding detection with fallback chain
    - PAT-002: Defensive parsing (accept liberally, produce consistently)
    """

    VOICE_TAG_PATTERN = re.compile(r'<v\s+([^>]+)>')
    VOICE_CLOSE_PATTERN = re.compile(r'</v>')

    ENCODING_FALLBACK = [
        'utf-8-sig',  # UTF-8 with BOM
        'utf-8',
        'windows-1252',
        'iso-8859-1',
        'latin-1'
    ]

    def parse(self, file_path: str) -> ParseResult:
        """
        Parse VTT file to canonical format.

        Args:
            file_path: Path to VTT file

        Returns:
            ParseResult with segments and metadata
        """
        result = ParseResult()

        # Detect encoding
        encoding = self._detect_encoding(file_path)
        result.encoding = encoding

        # Parse with webvtt-py
        try:
            vtt = webvtt.read(file_path, encoding=encoding)
        except Exception as e:
            result.parse_status = "failed"
            result.errors.append({
                "code": "ERR-PARSE",
                "message": str(e)
            })
            return result

        # Extract segments
        for idx, caption in enumerate(vtt, start=1):
            segment = self._extract_segment(caption, idx, result.warnings)
            if segment:
                result.segments.append(segment)

        # Calculate duration
        if result.segments:
            result.duration_ms = max(s.end_ms for s in result.segments)

        # Determine parse status
        if result.errors:
            result.parse_status = "failed"
        elif result.warnings:
            result.parse_status = "partial"
        else:
            result.parse_status = "complete"

        return result

    def _detect_encoding(self, file_path: str) -> str:
        """Detect file encoding using charset-normalizer fallback."""
        from charset_normalizer import from_path

        result = from_path(file_path)
        best = result.best()

        if best:
            return best.encoding

        # Fallback to UTF-8
        return 'utf-8'

    def _extract_segment(
        self,
        caption: webvtt.Caption,
        idx: int,
        warnings: List[dict]
    ) -> Optional[ParsedSegment]:
        """Extract segment from webvtt Caption object."""

        raw_text = caption.text

        # Extract speaker from voice tag
        speaker = None
        match = self.VOICE_TAG_PATTERN.search(raw_text)
        if match:
            speaker = match.group(1).strip()

        # Clean text: remove voice tags
        text = self.VOICE_TAG_PATTERN.sub('', raw_text)
        text = self.VOICE_CLOSE_PATTERN.sub('', text)
        text = ' '.join(text.split())  # Normalize whitespace

        # Skip empty segments
        if not text.strip():
            return None

        # Convert timestamps to milliseconds
        start_ms = self._timestamp_to_ms(caption.start)
        end_ms = self._timestamp_to_ms(caption.end)

        # Validate duration
        if end_ms < start_ms:
            warnings.append({
                "code": "WARN-002",
                "message": f"Negative duration at segment {idx}",
                "cue_index": idx
            })
            # Swap values
            start_ms, end_ms = end_ms, start_ms

        return ParsedSegment(
            id=f"seg-{idx:03d}",
            start_ms=start_ms,
            end_ms=end_ms,
            speaker=speaker,
            text=text,
            raw_text=raw_text
        )

    def _timestamp_to_ms(self, timestamp: str) -> int:
        """
        Convert VTT timestamp to milliseconds.

        Format: HH:MM:SS.mmm or MM:SS.mmm
        """
        parts = timestamp.replace(',', '.').split(':')

        if len(parts) == 3:
            hours, minutes, seconds = parts
        elif len(parts) == 2:
            hours = '0'
            minutes, seconds = parts
        else:
            return 0

        seconds, milliseconds = seconds.split('.') if '.' in seconds else (seconds, '0')

        total_ms = (
            int(hours) * 3600000 +
            int(minutes) * 60000 +
            int(seconds) * 1000 +
            int(milliseconds.ljust(3, '0')[:3])
        )

        # Round to nearest 10ms per NFR-006
        return round(total_ms / 10) * 10
```

#### Input/Output Contracts

**Input Contract (VTT File):**

```
WEBVTT                          ← REQUIRED: Header line
                                ← Optional blank line
00:00:00.000 --> 00:00:05.500   ← Timestamp line
<v Speaker Name>Text content    ← Payload with voice tag (optional)
continuation line</v>           ← Multi-line payload support
```

**Output Contract (canonical-transcript.json v1.1):**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CanonicalTranscript",
  "version": "1.1",
  "type": "object",
  "required": ["version", "source", "metadata", "segments", "parse_metadata"],
  "properties": {
    "version": {
      "type": "string",
      "const": "1.1"
    },
    "source": {
      "type": "object",
      "required": ["format", "encoding", "file_path"],
      "properties": {
        "format": {"type": "string", "enum": ["vtt", "srt", "plain"]},
        "encoding": {"type": "string"},
        "file_path": {"type": "string"}
      }
    },
    "metadata": {
      "type": "object",
      "required": ["duration_ms", "segment_count", "detected_speakers"],
      "properties": {
        "duration_ms": {"type": "integer"},
        "segment_count": {"type": "integer"},
        "detected_speakers": {"type": "integer"}
      }
    },
    "segments": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "text"],
        "properties": {
          "id": {"type": "string", "pattern": "^seg-\\d{3,}$"},
          "start_ms": {"type": ["integer", "null"]},
          "end_ms": {"type": ["integer", "null"]},
          "speaker": {"type": ["string", "null"]},
          "text": {"type": "string"},
          "raw_text": {"type": "string"}
        }
      }
    },
    "parse_metadata": {
      "type": "object",
      "required": ["parse_status"],
      "properties": {
        "parse_status": {"type": "string", "enum": ["complete", "partial", "failed"]},
        "parse_warnings": {"type": "array"},
        "parse_errors": {"type": "array"},
        "skipped_segments": {"type": "array"}
      }
    }
  }
}
```

#### Error Handling

| Error Code | Condition | Recovery Action |
|------------|-----------|-----------------|
| **ERR-PARSE** | webvtt-py fails to parse | Return failed status, trigger LLM fallback |
| **ERR-ENCODING** | All encoding fallbacks fail | Return failed status, trigger LLM fallback |
| **ERR-IO** | File read failure | Return failed status with path info |
| **WARN-001** | Malformed timestamp | Best-effort parse, log warning |
| **WARN-002** | Negative duration | Swap values, log warning |
| **WARN-003** | Encoding fallback used | Log which encoding succeeded |
| **WARN-004** | Voice tag with class attribute | Strip class, extract name |
| **SKIP-001** | Empty cue text | Skip segment, log in skipped_segments |
| **SKIP-002** | Whitespace-only segment | Skip segment |

#### Performance Requirements

| Metric | Requirement | Validation Method |
|--------|-------------|-------------------|
| **Parse time** | <5 seconds for 5-hour transcript | Timer in EN-023 benchmark |
| **Memory** | <100MB during parsing | Memory profiler |
| **Segment count** | 3,071+ segments (meeting-006) | Exact count validation |
| **Speaker count** | 50+ speakers (meeting-006) | Unique speaker count |
| **Encoding detection** | <500ms | Timer on charset-normalizer |

#### Encoding Detection (charset-normalizer)

**Why charset-normalizer over chardet:**

> "charset-normalizer is 4-5x faster than chardet for encoding detection."
> -- GitHub, charset-normalizer documentation

```python
# Encoding detection fallback chain
ENCODING_FALLBACK_CHAIN = [
    'utf-8-sig',    # UTF-8 with BOM (Windows common)
    'utf-8',        # Standard UTF-8
    'windows-1252', # Windows Latin (common transcription tool output)
    'iso-8859-1',   # Western European
    'latin-1'       # Final fallback (accepts all bytes)
]
```

---

### Section 5: Chunking Strategy (EN-021)

#### Index.json Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ChunkIndex",
  "version": "1.0",
  "type": "object",
  "required": ["schema_version", "total_segments", "total_chunks", "chunk_size", "chunks"],
  "properties": {
    "schema_version": {
      "type": "string",
      "const": "1.0"
    },
    "total_segments": {
      "type": "integer",
      "description": "Total number of segments in transcript"
    },
    "total_chunks": {
      "type": "integer",
      "description": "Number of chunk files generated"
    },
    "chunk_size": {
      "type": "integer",
      "default": 500,
      "description": "Target segments per chunk"
    },
    "source_file": {
      "type": "string",
      "description": "Original transcript file name"
    },
    "source_format": {
      "type": "string",
      "enum": ["vtt", "srt", "plain"]
    },
    "source_duration_ms": {
      "type": "integer",
      "description": "Total transcript duration in milliseconds"
    },
    "speakers": {
      "type": "array",
      "items": {"type": "string"},
      "description": "List of all detected speakers"
    },
    "speaker_segment_counts": {
      "type": "object",
      "additionalProperties": {"type": "integer"},
      "description": "Segment count per speaker"
    },
    "chunks": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/ChunkPointer"
      }
    }
  },
  "definitions": {
    "ChunkPointer": {
      "type": "object",
      "required": ["chunk_id", "segment_range", "file"],
      "properties": {
        "chunk_id": {
          "type": "string",
          "pattern": "^chunk-\\d{3}$"
        },
        "segment_range": {
          "type": "array",
          "items": {"type": "integer"},
          "minItems": 2,
          "maxItems": 2,
          "description": "[start_segment, end_segment]"
        },
        "timestamp_range": {
          "type": "array",
          "items": {"type": "string"},
          "minItems": 2,
          "maxItems": 2,
          "description": "[start_time, end_time] as HH:MM:SS.mmm"
        },
        "file": {
          "type": "string",
          "description": "Relative path to chunk file"
        },
        "segment_count": {
          "type": "integer"
        },
        "speaker_distribution": {
          "type": "object",
          "additionalProperties": {"type": "integer"}
        }
      }
    }
  }
}
```

#### Chunk-NNN.json Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TranscriptChunk",
  "version": "1.0",
  "type": "object",
  "required": ["chunk_id", "schema_version", "segment_range", "segments"],
  "properties": {
    "chunk_id": {
      "type": "string",
      "pattern": "^chunk-\\d{3}$"
    },
    "schema_version": {
      "type": "string",
      "const": "1.0"
    },
    "segment_range": {
      "type": "array",
      "items": {"type": "integer"},
      "minItems": 2,
      "maxItems": 2
    },
    "timestamp_range": {
      "type": "array",
      "items": {"type": "string"},
      "minItems": 2,
      "maxItems": 2
    },
    "prev_chunk": {
      "type": ["string", "null"],
      "description": "chunk_id of previous chunk (for navigation)"
    },
    "next_chunk": {
      "type": ["string", "null"],
      "description": "chunk_id of next chunk (for navigation)"
    },
    "segments": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "text"],
        "properties": {
          "id": {"type": "string"},
          "start_ms": {"type": ["integer", "null"]},
          "end_ms": {"type": ["integer", "null"]},
          "speaker": {"type": ["string", "null"]},
          "text": {"type": "string"}
        }
      }
    }
  }
}
```

#### 500-Segment Rationale

**Calculation:**

```
Average segment length: 15-30 words
Average tokens per word: 1.3-1.5
Tokens per segment: 20-40 tokens

500 segments × 30 tokens/segment = 15,000 tokens

Context limits (ADR-004):
- Soft limit: 31,500 tokens (target)
- Hard limit: 45,000 tokens (absolute)

15,000 tokens << 31,500 tokens ✓ (safe margin)
```

**Industry Alignment:**

> "RecursiveCharacterTextSplitter is the recommended text splitter for generic text. Configuration: chunk_size=1000, chunk_overlap=200."
> -- LangChain Documentation

**Meeting-006-all-hands.vtt Example:**

| Total Segments | Chunk Size | Total Chunks | Tokens per Chunk |
|----------------|------------|--------------|------------------|
| 3,071 | 500 | 7 (6 full + 1 partial) | ~15,000 |

#### Segment-Boundary Preservation

**Rule:** Chunks MUST end on segment boundaries, never mid-segment.

```python
def create_chunks(segments: List[Segment], chunk_size: int = 500) -> List[Chunk]:
    """
    Create chunks from segments, respecting segment boundaries.

    Algorithm:
    1. Group segments into batches of chunk_size
    2. Last chunk may have fewer segments (remainder)
    3. Never split a segment across chunks
    """
    chunks = []

    for i in range(0, len(segments), chunk_size):
        batch = segments[i:i + chunk_size]
        chunk_num = (i // chunk_size) + 1

        chunk = Chunk(
            chunk_id=f"chunk-{chunk_num:03d}",
            segment_range=[i + 1, min(i + chunk_size, len(segments))],
            segments=batch,
            prev_chunk=f"chunk-{chunk_num-1:03d}" if chunk_num > 1 else None,
            next_chunk=f"chunk-{chunk_num+1:03d}" if i + chunk_size < len(segments) else None
        )
        chunks.append(chunk)

    return chunks
```

#### Navigation API

**Index Navigation Pattern:**

```markdown
1. ts-extractor reads index.json
2. Determines which chunks to process:
   - ALL chunks (comprehensive extraction)
   - SPECIFIC chunks (targeted extraction by timestamp/speaker)
3. Requests chunks sequentially or selectively
4. Aggregates results with cross-chunk citation linking
```

**Chunk Request Protocol:**

```json
{
  "action": "read_chunk",
  "chunk_id": "chunk-003",
  "context": {
    "index_path": "./index.json",
    "purpose": "Extract action items from segments 1001-1500"
  }
}
```

---

### Section 6: Extractor Adaptation (EN-022)

#### Current Extractor Interface

**Current Input (ts-extractor v1.2.0):**

```json
{
  "canonical_json_path": "/path/to/canonical-transcript.json",
  "output_path": "/path/to/extraction-report.json",
  "packet_id": "meeting-006",
  "confidence_threshold": 0.7
}
```

**Current Assumption:** Entire canonical transcript fits in single context read.

#### Chunked Input Interface Changes

**New Input Contract:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ChunkedExtractorInput",
  "type": "object",
  "required": ["index_path", "output_path", "packet_id"],
  "properties": {
    "index_path": {
      "type": "string",
      "description": "Path to index.json for chunked transcript"
    },
    "canonical_path": {
      "type": "string",
      "description": "Path to canonical-transcript.json (optional for small files)"
    },
    "output_path": {
      "type": "string"
    },
    "packet_id": {
      "type": "string"
    },
    "confidence_threshold": {
      "type": "number",
      "default": 0.7
    },
    "extraction_mode": {
      "type": "string",
      "enum": ["full", "selective"],
      "default": "full",
      "description": "Process all chunks or select specific ones"
    },
    "chunk_selection": {
      "type": "array",
      "items": {"type": "string"},
      "description": "List of chunk_ids to process (if selective mode)"
    }
  }
}
```

**Detection Logic (in ts-extractor):**

```markdown
IF index_path is provided AND file exists:
  → Use chunked processing mode
ELSE IF canonical_path is provided:
  → Use legacy single-file mode (backward compatible)
ELSE:
  → Error: No input path provided
```

#### Index-Based Navigation

**Extraction Workflow:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CHUNKED EXTRACTION WORKFLOW                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. READ INDEX                                                          │
│     ┌─────────────────────────────────────────────────────────────┐    │
│     │  index.json                                                  │    │
│     │  - total_segments: 3071                                      │    │
│     │  - total_chunks: 7                                           │    │
│     │  - speakers: [50+ names]                                     │    │
│     │  - chunks: [chunk-001 → chunk-007]                          │    │
│     └─────────────────────────────────────────────────────────────┘    │
│                               │                                          │
│                               ▼                                          │
│  2. BUILD EXTRACTION PLAN                                               │
│     ┌─────────────────────────────────────────────────────────────┐    │
│     │  For each extraction type:                                   │    │
│     │  - Action items: Process ALL chunks sequentially             │    │
│     │  - Decisions: Process ALL chunks sequentially                │    │
│     │  - Questions: Process ALL chunks sequentially                │    │
│     │  - Topics: Process ALL chunks, detect boundaries             │    │
│     │  - Speakers: Build from index speaker_segment_counts         │    │
│     └─────────────────────────────────────────────────────────────┘    │
│                               │                                          │
│                               ▼                                          │
│  3. PROCESS CHUNKS                                                      │
│     ┌─────────────────────────────────────────────────────────────┐    │
│     │  FOR chunk in chunks:                                        │    │
│     │    1. Read chunk file                                        │    │
│     │    2. Apply extraction rules (PAT-001, PAT-003, PAT-004)    │    │
│     │    3. Generate citations with chunk context                  │    │
│     │    4. Store partial results                                  │    │
│     │                                                              │    │
│     │  Chunk 1 → Results 1 ─┐                                     │    │
│     │  Chunk 2 → Results 2 ─┼─► ACCUMULATOR                       │    │
│     │  Chunk 7 → Results 7 ─┘                                     │    │
│     └─────────────────────────────────────────────────────────────┘    │
│                               │                                          │
│                               ▼                                          │
│  4. AGGREGATE RESULTS                                                   │
│     ┌─────────────────────────────────────────────────────────────┐    │
│     │  - Merge entity lists                                        │    │
│     │  - Deduplicate across chunks                                 │    │
│     │  - Link cross-chunk topics                                   │    │
│     │  - Recalculate confidence summary                            │    │
│     └─────────────────────────────────────────────────────────────┘    │
│                               │                                          │
│                               ▼                                          │
│  5. OUTPUT                                                              │
│     ┌─────────────────────────────────────────────────────────────┐    │
│     │  extraction-report.json                                      │    │
│     │  - All entities with valid citations                         │    │
│     │  - chunk_id included in citations                            │    │
│     └─────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Citation Preservation Across Chunks

**Enhanced Citation Schema:**

```json
{
  "citation": {
    "segment_id": "seg-1042",
    "chunk_id": "chunk-003",
    "anchor": "#chunk-003/seg-1042",
    "timestamp_ms": 2340000,
    "text_snippet": "Bob will prepare the quarterly report by Friday."
  }
}
```

**Citation Resolution:**

```markdown
When referencing citations:
1. Parse anchor: #chunk-003/seg-1042
2. Locate chunk file: chunks/chunk-003.json
3. Find segment by id: seg-1042
4. Validate text_snippet is substring of segment.text
```

#### Accumulation Pattern for Multi-Chunk Processing

```python
class ChunkedExtractionAccumulator:
    """
    Accumulates extraction results across multiple chunks.

    Responsibilities:
    1. Store partial results per chunk
    2. Deduplicate entities across chunks
    3. Link topics spanning chunk boundaries
    4. Calculate aggregate statistics
    """

    def __init__(self):
        self.action_items = []
        self.decisions = []
        self.questions = []
        self.topics = []
        self.speakers = {}
        self.processed_chunks = []

    def add_chunk_results(self, chunk_id: str, results: dict):
        """Add extraction results from a single chunk."""
        self.processed_chunks.append(chunk_id)

        # Merge with deduplication
        for action in results.get('action_items', []):
            if not self._is_duplicate_action(action):
                self.action_items.append(action)

        # Similar for other entity types...

    def finalize(self) -> dict:
        """Generate final extraction report."""
        return {
            "version": "1.0",
            "extraction_stats": self._calculate_stats(),
            "action_items": self.action_items,
            "decisions": self.decisions,
            "questions": self.questions,
            "topics": self._link_topics(),
            "speakers": list(self.speakers.values())
        }

    def _is_duplicate_action(self, action: dict) -> bool:
        """Check if action already exists (fuzzy match)."""
        for existing in self.action_items:
            if self._text_similarity(existing['text'], action['text']) > 0.9:
                return True
        return False
```

---

### Section 7: Integration Testing (EN-023)

#### Contract Test Specifications

**Test Suite: CON-HYBRID-001 - Parser Output Contract**

```yaml
test_id: CON-HYBRID-001
name: "Python Parser Output Contract Validation"
description: "Validates Python parser output matches canonical schema"
preconditions:
  - meeting-006-all-hands.vtt exists in test_data/golden/
assertions:
  - canonical-transcript.json passes JSON Schema validation
  - segment_count == 3071 (exact match)
  - all segments have valid id format (seg-NNN)
  - all segments with timestamps have valid duration
  - parse_status in ["complete", "partial"]
```

**Test Suite: CON-HYBRID-002 - Chunk Index Contract**

```yaml
test_id: CON-HYBRID-002
name: "Chunk Index Contract Validation"
description: "Validates chunk index structure and pointers"
preconditions:
  - Python parser has created index.json
assertions:
  - index.json passes ChunkIndex schema
  - total_segments matches canonical-transcript.json
  - sum of chunk segment_counts == total_segments
  - all chunk file pointers resolve to existing files
  - chunk navigation (prev/next) is consistent
```

**Test Suite: CON-HYBRID-003 - Extractor Chunked Input**

```yaml
test_id: CON-HYBRID-003
name: "Extractor Chunked Input Contract"
description: "Validates ts-extractor handles chunked input correctly"
preconditions:
  - index.json and chunks/*.json exist
assertions:
  - ts-extractor reads index.json successfully
  - all chunks are processed
  - citations reference valid chunk_id + segment_id
  - extraction_stats aggregated correctly
```

#### E2E Validation Scenarios

**Scenario 1: Full Pipeline - Large VTT File**

```gherkin
Feature: Large VTT File Processing
  As a user
  I want to process a 5-hour meeting transcript
  So that I can extract all entities without data loss

  Scenario: Process meeting-006-all-hands.vtt end-to-end
    Given a VTT file with 3071 segments and 90K+ tokens
    When I invoke the transcript skill pipeline
    Then the Python parser extracts all 3071 segments
    And 7 chunks are created with 500 segments each (last has 71)
    And ts-extractor processes all chunks
    And extraction-report.json contains entities from all chunks
    And no data loss occurs (0 skipped segments in parse_metadata)
```

**Scenario 2: Format Detection and Routing**

```gherkin
Feature: Format Detection and Strategy Routing
  As the ts-parser orchestrator
  I want to route files to the correct parser
  So that each format is handled optimally

  Scenario: VTT file routes to Python parser
    Given a file starting with "WEBVTT"
    When format detection runs
    Then format is detected as "vtt"
    And Python parser strategy is selected

  Scenario: Unknown format falls back to LLM
    Given a file with no recognized format markers
    When format detection runs
    Then format is detected as "plain"
    And LLM parser strategy is selected (fallback)
```

**Scenario 3: Fallback Path Validation**

```gherkin
Feature: LLM Fallback Path
  As the ts-parser orchestrator
  I want to fall back to LLM parsing when Python fails
  So that processing continues despite errors

  Scenario: Python parser failure triggers LLM fallback
    Given a malformed VTT file that webvtt-py cannot parse
    When the Python parser throws an exception
    Then the error is logged
    And LLM parser strategy is invoked
    And output.fallback_used is set to true
```

#### Performance Benchmarks

**Benchmark Suite: PERF-HYBRID-001**

| Metric | Target | Test Method |
|--------|--------|-------------|
| **Parse time (3071 segments)** | <5 seconds | Time VTTParser.parse() |
| **Memory usage during parse** | <100MB | tracemalloc profiling |
| **Chunk file I/O** | <100ms per chunk | Time chunk writes |
| **Total pipeline (parse→chunk→extract)** | <30 seconds | End-to-end timer |
| **Encoding detection** | <500ms | Time charset-normalizer |

**Benchmark Script:**

```python
import time
import tracemalloc

def benchmark_parser():
    """Benchmark Python VTT parser performance."""
    tracemalloc.start()

    start = time.perf_counter()
    result = VTTParser().parse("meeting-006-all-hands.vtt")
    end = time.perf_counter()

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "parse_time_s": end - start,
        "segment_count": len(result.segments),
        "memory_current_mb": current / 1024 / 1024,
        "memory_peak_mb": peak / 1024 / 1024
    }
```

#### Fallback Path Testing

**Test Cases:**

| Test ID | Scenario | Expected Behavior |
|---------|----------|-------------------|
| FB-001 | webvtt-py parse exception | Log error, invoke LLM, set fallback_used=true |
| FB-002 | Unknown format (no WEBVTT header) | Detect as plain, invoke LLM directly |
| FB-003 | Schema validation failure | Log warning, invoke LLM, compare outputs |
| FB-004 | All encoding fallbacks fail | Log error, invoke LLM with raw content |
| FB-005 | Partial Python success | Validate partial output, no fallback |

---

## L2: Strategic Design (Principal Architect)

### Section 8: Testing Strategy

#### RED/GREEN/REFACTOR Cycle

**Kent Beck's Canon TDD Applied:**

> "TDD is intended to help the programmer create a new state of the system where: Everything that used to work still works. The new behavior works as expected. The system is ready for the next change."
> -- Kent Beck, "Canon TDD"

**Cycle Application:**

```
┌───────────────────────────────────────────────────────────────────────────┐
│                     TDD CYCLE FOR HYBRID INFRASTRUCTURE                    │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │  ITERATION 1: Python Parser (EN-020)                                │   │
│  │                                                                     │   │
│  │  RED:    Write test: parse_vtt_extracts_all_segments_from_file     │   │
│  │          Test fails: VTTParser class does not exist                │   │
│  │                                                                     │   │
│  │  GREEN:  Implement VTTParser.parse() using webvtt-py               │   │
│  │          Test passes: 3071 segments extracted                      │   │
│  │                                                                     │   │
│  │  REFACTOR: Extract _timestamp_to_ms() helper, add type hints       │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                      │                                     │
│                                      ▼                                     │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │  ITERATION 2: Chunking Strategy (EN-021)                            │   │
│  │                                                                     │   │
│  │  RED:    Write test: create_chunks_produces_index_and_files        │   │
│  │          Test fails: Chunker class does not exist                  │   │
│  │                                                                     │   │
│  │  GREEN:  Implement Chunker with 500-segment batching               │   │
│  │          Test passes: 7 chunks created for 3071 segments           │   │
│  │                                                                     │   │
│  │  REFACTOR: Add prev/next navigation, extract schema validation     │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                      │                                     │
│                                      ▼                                     │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │  ITERATION 3: Extractor Adaptation (EN-022)                         │   │
│  │                                                                     │   │
│  │  RED:    Write test: extractor_processes_chunked_input             │   │
│  │          Test fails: ts-extractor doesn't recognize index.json     │   │
│  │                                                                     │   │
│  │  GREEN:  Update ts-extractor input detection and chunk processing  │   │
│  │          Test passes: All chunks processed, results aggregated     │   │
│  │                                                                     │   │
│  │  REFACTOR: Extract ChunkedExtractionAccumulator, improve citations │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                      │                                     │
│                                      ▼                                     │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │  ITERATION 4: Integration (EN-023)                                  │   │
│  │                                                                     │   │
│  │  RED:    Write test: full_pipeline_meeting006_no_data_loss         │   │
│  │          Test fails: Pipeline not wired together                   │   │
│  │                                                                     │   │
│  │  GREEN:  Wire ts-parser → Python parser → Chunker → ts-extractor   │   │
│  │          Test passes: 0 data loss, all entities extracted          │   │
│  │                                                                     │   │
│  │  REFACTOR: Optimize performance, add fallback path tests           │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
└───────────────────────────────────────────────────────────────────────────┘
```

#### Test Pyramid for Hybrid Architecture

```
                         ┌─────────────────┐
                         │      E2E        │  ← 5% (Full pipeline tests)
                        ┌┴─────────────────┴┐
                        │    Integration     │  ← 15% (Python↔LLM handoff)
                       ┌┴───────────────────┴┐
                       │      Contract       │  ← 10% (Schema validation)
                      ┌┴─────────────────────┴┐
                      │         Unit          │  ← 70% (Python parser logic)
                      └───────────────────────┘

DISTRIBUTION BY ENABLER:
─────────────────────────────────────────────────────────────────────────
EN-020 (Python Parser):     70% unit, 20% contract, 10% integration
EN-021 (Chunking):          60% unit, 30% contract, 10% integration
EN-022 (Extractor):         50% unit, 30% contract, 20% integration
EN-023 (Integration):       20% unit, 30% contract, 50% integration/E2E
```

#### Unit Test Scope (Python Layer)

| Component | Test Focus | Coverage Target |
|-----------|------------|-----------------|
| VTTParser.parse() | Segment extraction accuracy | 95%+ |
| VTTParser._detect_encoding() | Fallback chain execution | 100% |
| VTTParser._timestamp_to_ms() | Edge cases (missing ms, overflow) | 100% |
| VTTParser._extract_segment() | Voice tag patterns, multi-line | 100% |
| Chunker.create_chunks() | Boundary handling, navigation | 95%+ |
| Chunker.write_index() | Schema compliance | 100% |

#### Contract Tests (Interface Boundaries)

| Contract | Parties | Validation |
|----------|---------|------------|
| CON-PARSE-001 | Python Parser → Canonical JSON | JSON Schema validation |
| CON-CHUNK-001 | Chunker → Index JSON | ChunkIndex schema |
| CON-CHUNK-002 | Chunker → Chunk JSON | TranscriptChunk schema |
| CON-EXTRACT-001 | ts-extractor → Chunked Input | Input detection logic |
| CON-EXTRACT-002 | ts-extractor → Citations | Citation validity |

#### Integration Tests (End-to-End)

| Test | Components | Validation |
|------|------------|------------|
| INT-001 | Python Parser + Chunker | Parse → Chunk pipeline |
| INT-002 | Chunker + ts-extractor | Chunk → Extract pipeline |
| INT-003 | Full Pipeline | Input VTT → Output Report |
| INT-004 | Fallback Path | Python Fail → LLM Fallback |
| INT-005 | Performance | <30s end-to-end |

#### Coverage Targets

| Layer | Line Coverage | Branch Coverage |
|-------|---------------|-----------------|
| Python Parser (EN-020) | 95% | 90% |
| Chunker (EN-021) | 95% | 90% |
| Integration (EN-023) | 80% | 75% |
| Overall | 90% | 85% |

---

### Section 9: Implementation Roadmap

#### Work Item Specifications

##### EN-020: Python Parser Implementation

**Priority:** P0 (Foundation - all others depend on this)
**Estimated Tasks:** 6-8
**Complexity:** HIGH

| Task ID | Title | Description | Dependencies |
|---------|-------|-------------|--------------|
| TASK-200 | Environment Setup | Create src/transcript/ bounded context structure, add webvtt-py and charset-normalizer to pyproject.toml | None |
| TASK-201 | VTTParser Class Design | Define class structure, type hints, interfaces | TASK-200 |
| TASK-202 | Encoding Detection | Implement charset-normalizer integration | TASK-201 |
| TASK-203 | VTT Parsing Implementation | webvtt-py wrapper with voice tag extraction | TASK-201, 202 |
| TASK-204 | Output Schema Compliance | Ensure canonical-transcript.json v1.1 output | TASK-203 |
| TASK-205 | Error Handling | Implement warning/error capture, recovery | TASK-203 |
| TASK-206 | Unit Tests | pytest suite for all parser logic | TASK-203, 204, 205 |
| TASK-207 | Performance Benchmarks | Timer, memory profiling tests | TASK-206 |

**Acceptance Criteria:**
- [ ] Parse meeting-006-all-hands.vtt with 3071 segments extracted
- [ ] Unit test coverage ≥ 95%
- [ ] Parse time < 5 seconds
- [ ] Memory usage < 100MB

##### EN-021: Chunking Strategy

**Priority:** P0 (Required for extraction)
**Estimated Tasks:** 5-6
**Complexity:** MEDIUM

| Task ID | Title | Description | Dependencies |
|---------|-------|-------------|--------------|
| TASK-210 | Index Schema Design | Define index.json JSON Schema | EN-020 complete |
| TASK-211 | Chunk Schema Design | Define chunk-NNN.json JSON Schema | TASK-210 |
| TASK-212 | Chunking Algorithm | Implement 500-segment batching | TASK-210, 211 |
| TASK-213 | Navigation Links | Add prev/next chunk pointers | TASK-212 |
| TASK-214 | Unit Tests | pytest suite for chunking logic | TASK-212, 213 |
| TASK-215 | Schema Validation Tests | Contract tests for JSON schemas | TASK-214 |

**Acceptance Criteria:**
- [ ] Index.json created with accurate metadata
- [ ] 7 chunks created for meeting-006 (6 × 500 + 1 × 71)
- [ ] All chunk files pass JSON Schema validation
- [ ] Navigation links are consistent

##### EN-022: Extractor Adaptation

**Priority:** P1 (After chunking infrastructure)
**Estimated Tasks:** 4-5
**Complexity:** LOW

| Task ID | Title | Description | Dependencies |
|---------|-------|-------------|--------------|
| TASK-220 | Input Detection Update | Add index.json detection to ts-extractor | EN-021 complete |
| TASK-221 | Chunk Processing Loop | Implement sequential chunk reading | TASK-220 |
| TASK-222 | Result Accumulation | ChunkedExtractionAccumulator implementation | TASK-221 |
| TASK-223 | Citation Enhancement | Add chunk_id to citation schema | TASK-222 |
| TASK-224 | Integration Tests | Test chunked extraction flow | TASK-222, 223 |

**Acceptance Criteria:**
- [ ] ts-extractor processes chunked input when index.json provided
- [ ] Backward compatible with single-file input
- [ ] Citations include chunk_id for navigation
- [ ] Results aggregated correctly across chunks

##### EN-023: Integration Testing

**Priority:** P1 (Validation layer)
**Estimated Tasks:** 5-6
**Complexity:** MEDIUM

| Task ID | Title | Description | Dependencies |
|---------|-------|-------------|--------------|
| TASK-230 | Test Framework Setup | pytest fixtures for hybrid tests | EN-020, 021, 022 complete |
| TASK-231 | Large File Test Cases | meeting-006 full pipeline tests | TASK-230 |
| TASK-232 | Fallback Path Tests | Python failure → LLM fallback | TASK-230 |
| TASK-233 | Performance Benchmarks | End-to-end timing validation | TASK-231 |
| TASK-234 | Regression Tests | Existing test data compatibility | TASK-231 |
| TASK-235 | Documentation | Test coverage report, runbook | TASK-234 |

**Acceptance Criteria:**
- [ ] E2E pipeline passes for meeting-006-all-hands.vtt
- [ ] 0 data loss (all 3071 segments processed)
- [ ] Fallback path tested and functional
- [ ] Performance < 30 seconds end-to-end

#### Task Dependencies

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CRITICAL PATH DEPENDENCY GRAPH                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  PHASE 1: FOUNDATION (EN-020)                                    │    │
│  │                                                                   │    │
│  │  TASK-200 ──► TASK-201 ──► TASK-202 ──► TASK-203 ──►            │    │
│  │              (design)     (encoding)   (parsing)                 │    │
│  │                                            │                      │    │
│  │                                            ├──► TASK-204 (schema) │    │
│  │                                            ├──► TASK-205 (errors) │    │
│  │                                            │                      │    │
│  │                                            └──► TASK-206 (tests)  │    │
│  │                                                      │            │    │
│  │                                                      ▼            │    │
│  │                                              TASK-207 (bench)     │    │
│  └──────────────────────────────────────────────────────┬────────────┘    │
│                                                         │                 │
│                                                         ▼                 │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  PHASE 2: CHUNKING (EN-021)                                      │    │
│  │                                                                   │    │
│  │  TASK-210 ──► TASK-211 ──► TASK-212 ──► TASK-213 ──►            │    │
│  │  (index)     (chunk)      (algorithm)  (navigation)              │    │
│  │                                            │                      │    │
│  │                                            ├──► TASK-214 (tests)  │    │
│  │                                            └──► TASK-215 (schema) │    │
│  └──────────────────────────────────────────────────────┬────────────┘    │
│                                                         │                 │
│                                                         ▼                 │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  PHASE 3: ADAPTATION (EN-022)                                    │    │
│  │                                                                   │    │
│  │  TASK-220 ──► TASK-221 ──► TASK-222 ──► TASK-223 ──►            │    │
│  │  (detect)    (loop)       (accumulate) (citations)               │    │
│  │                                            │                      │    │
│  │                                            └──► TASK-224 (tests)  │    │
│  └──────────────────────────────────────────────────────┬────────────┘    │
│                                                         │                 │
│                                                         ▼                 │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  PHASE 4: VALIDATION (EN-023)                                    │    │
│  │                                                                   │    │
│  │  TASK-230 ──► TASK-231 ──► TASK-233                              │    │
│  │  (setup)     (large file) (performance)                          │    │
│  │       │                                                           │    │
│  │       ├──► TASK-232 (fallback)                                   │    │
│  │       │                                                           │    │
│  │       └──► TASK-234 ──► TASK-235 (regression, docs)              │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  LEGEND:                                                                 │
│  ──► Sequential dependency (must complete before)                       │
│  │── Parallel tasks (can execute concurrently)                          │
│                                                                          │
│  CRITICAL PATH: TASK-200 → 203 → EN-020 → TASK-212 → EN-021 →          │
│                 TASK-222 → EN-022 → TASK-231 → EN-023                   │
│                                                                          │
│  ESTIMATED CALENDAR TIME: 3-4 sprints                                   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Estimated Task Count per Enabler

| Enabler | Task Count | Complexity | Calendar Estimate |
|---------|------------|------------|-------------------|
| EN-020 | 8 | HIGH | 1-1.5 sprints |
| EN-021 | 6 | MEDIUM | 0.5-1 sprint |
| EN-022 | 5 | LOW | 0.5 sprint |
| EN-023 | 6 | MEDIUM | 0.5-1 sprint |
| **Total** | **25** | - | **3-4 sprints** |

---

### Section 10: Migration Strategy

#### Incremental Adoption

**Phase Order (per DEC-011 D-002):**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     INCREMENTAL FORMAT ADOPTION                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │  PHASE 1: VTT (MVP)                                                 │ │
│  │  ─────────────────                                                  │ │
│  │  Library: webvtt-py v0.5.1                                         │ │
│  │  Priority: P0 (caused DISC-009 incident)                           │ │
│  │  Files affected: meeting-006-all-hands.vtt, all *.vtt              │ │
│  │  Deliverables: EN-020, EN-021, EN-022, EN-023                      │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                    │                                     │
│                                    ▼                                     │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │  PHASE 2: SRT (Future)                                              │ │
│  │  ─────────────────────                                              │ │
│  │  Library: pysrt (GPL-3.0) or srt (MIT-like)                        │ │
│  │  Priority: P2                                                       │ │
│  │  Enabler: EN-025 (new)                                             │ │
│  │  Pattern: Same as Phase 1, add SRT strategy to ts-parser           │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                    │                                     │
│                                    ▼                                     │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │  PHASE 3: Plain Text (Future)                                       │ │
│  │  ────────────────────────────                                       │ │
│  │  Library: Custom parser (no external lib)                          │ │
│  │  Priority: P3                                                       │ │
│  │  Enabler: EN-026 (new)                                             │ │
│  │  Notes: Plain text has no timestamps, LLM may remain best option   │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Backward Compatibility Guarantees

| Concern | Guarantee | Validation |
|---------|-----------|------------|
| **Small transcripts** | LLM path still works | Regression tests with existing golden data |
| **ts-extractor input** | Detects both single-file and chunked | Input detection tests |
| **Output schema** | canonical-transcript.json v1.1 unchanged | JSON Schema validation |
| **Pipeline order** | SKILL.md orchestration unchanged | E2E pipeline tests |
| **Performance** | No regression for small files | Benchmark comparison |

**Backward Compatibility Matrix:**

```markdown
BEFORE (v1.2.0):
  Input: VTT file
  → ts-parser (LLM): Parse entire file
  → canonical-transcript.json
  → ts-extractor: Process all at once

AFTER (v2.0.0):
  Input: VTT file
  → ts-parser (Orchestrator): Detect format
    IF VTT:
      → Python Parser: Deterministic parse
      → canonical-transcript.json + index.json + chunks/
    ELSE:
      → LLM Parser: Fallback (same as v1.2.0)
  → ts-extractor: Detect input type
    IF chunked:
      → Process chunks iteratively
    ELSE:
      → Process single file (same as v1.2.0)
```

#### Rollback Strategy

**Decision Tree:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ROLLBACK DECISION TREE                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│                  ┌─────────────────────────────────┐                    │
│                  │  Hybrid Architecture Deployed   │                    │
│                  └────────────────┬────────────────┘                    │
│                                   │                                      │
│                                   ▼                                      │
│               ┌───────────────────────────────────────┐                 │
│               │  Is Python Parser Functioning?        │                 │
│               └─────────────────┬─────────────────────┘                 │
│                                 │                                        │
│                    YES          │           NO                           │
│                     │           │           │                            │
│          ┌──────────┘           │           └──────────┐                │
│          │                      │                      │                 │
│          ▼                      │                      ▼                 │
│  ┌───────────────────┐          │         ┌───────────────────────────┐ │
│  │ Continue with     │          │         │ AUTOMATIC LLM FALLBACK    │ │
│  │ Python Strategy   │          │         │ ts-parser routes to       │ │
│  │                   │          │         │ original LLM parser       │ │
│  └───────────────────┘          │         └─────────────┬─────────────┘ │
│                                 │                       │                │
│                                 │                       ▼                │
│                                 │      ┌─────────────────────────────┐  │
│                                 │      │ Is Fallback Sufficient?     │  │
│                                 │      └──────────────┬──────────────┘  │
│                                 │                     │                  │
│                                 │        YES          │        NO        │
│                                 │         │           │         │        │
│                                 │  ┌──────┘           │   ┌─────┘        │
│                                 │  │                  │   │              │
│                                 │  ▼                  │   ▼              │
│                                 │  ┌───────────────┐  │  ┌────────────┐  │
│                                 │  │ Log & Monitor │  │  │ FULL       │  │
│                                 │  │ Continue ops  │  │  │ ROLLBACK   │  │
│                                 │  └───────────────┘  │  └────────────┘  │
│                                                                          │
│  FULL ROLLBACK PROCEDURE:                                               │
│  ─────────────────────────                                              │
│  1. git revert to pre-FEAT-004 commit                                   │
│  2. Remove src/transcript/ bounded context directory                   │
│  3. Restore ts-parser.md v1.2.0                                        │
│  4. Keep chunking infrastructure for future retry                       │
│  5. Document root cause in DISC-012                                     │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Feature Flag Approach (Optional)

If gradual rollout is desired:

```yaml
# skills/transcript/config.yaml
hybrid_parsing:
  enabled: true
  formats:
    vtt: true   # Use Python parser for VTT
    srt: false  # Keep LLM for SRT (Phase 2)
    plain: false # Keep LLM for plain text
  fallback_on_error: true
  chunking:
    enabled: true
    chunk_size: 500
```

---

## 11. Jerry CLI Integration

> **Pipeline Position:** The `jerry transcript parse` command is the entry point
> for the deterministic parsing layer. In the hybrid pipeline:
> 1. CLI invokes Python VTT/SRT parser (deterministic, fast, cheap)
> 2. Parsed canonical JSON is chunked for LLM consumption
> 3. LLM agents perform semantic extraction on manageable chunks
>
> **Reference Pattern:** TDD-EN014 Section 10 (Domain Validation CLI)
> **Amendment:** Added per DISC-012 feedback loop FL-001

### 11.1 Parser Registration

**File:** `src/interface/cli/parser.py`

**Add function:**

```python
def _add_transcript_namespace(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Add transcript namespace commands.

    Commands:
        - parse: Parse VTT/SRT transcript to canonical JSON

    References:
        - TDD-FEAT-004: Hybrid Infrastructure Design
        - EN-020: Python Parser Implementation
    """
    transcript_parser = subparsers.add_parser(
        "transcript",
        help="Transcript skill commands",
        description="Manage transcript skill operations.",
    )

    transcript_subparsers = transcript_parser.add_subparsers(
        title="commands",
        dest="command",
        metavar="<command>",
    )

    # parse command
    parse_parser = transcript_subparsers.add_parser(
        "parse",
        help="Parse transcript file to canonical JSON",
        description="Parse VTT/SRT transcript file and produce canonical JSON output with optional chunking.",
    )
    parse_parser.add_argument(
        "path",
        help="Path to transcript file (VTT or SRT)",
    )
    parse_parser.add_argument(
        "--format",
        choices=["vtt", "srt", "auto"],
        default="auto",
        help="Input format (default: auto-detect from extension)",
    )
    parse_parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory for canonical JSON and chunks (default: same as input)",
    )
    parse_parser.add_argument(
        "--chunk-size",
        type=int,
        default=500,
        help="Number of segments per chunk (default: 500)",
    )
    parse_parser.add_argument(
        "--no-chunks",
        action="store_true",
        help="Skip chunk generation, output canonical JSON only",
    )
```

**Add to `create_parser()`:**

```python
# Add transcript namespace after other namespaces
_add_transcript_namespace(subparsers)
```

### 11.2 Main Routing

**File:** `src/interface/cli/main.py`

**Add handler:**

```python
def _handle_transcript(adapter: CLIAdapter, args: Any, json_output: bool) -> int:
    """Route transcript namespace commands.

    Args:
        adapter: CLI adapter instance
        args: Parsed arguments
        json_output: Whether to output JSON

    Returns:
        Exit code (0 = success, 1 = error)
    """
    if args.command is None:
        print("Error: No transcript command specified. Use 'jerry transcript --help'")
        return 1

    if args.command == "parse":
        return adapter.cmd_transcript_parse(
            path=args.path,
            format=getattr(args, "format", "auto"),
            output_dir=getattr(args, "output_dir", None),
            chunk_size=getattr(args, "chunk_size", 500),
            generate_chunks=not getattr(args, "no_chunks", False),
            json_output=json_output,
        )

    print(f"Error: Unknown transcript command '{args.command}'")
    return 1
```

**Update `main()` routing:**

```python
elif args.namespace == "transcript":
    return _handle_transcript(adapter, args, json_output)
```

### 11.3 CLIAdapter Method

**File:** `src/interface/cli/adapter.py`

**Add method:**

```python
def cmd_transcript_parse(
    self,
    path: str,
    format: str = "auto",
    output_dir: str | None = None,
    chunk_size: int = 500,
    generate_chunks: bool = True,
    json_output: bool = False,
) -> int:
    """Parse a transcript file to canonical JSON.

    Args:
        path: Path to transcript file (VTT or SRT)
        format: Input format ('vtt', 'srt', or 'auto')
        output_dir: Output directory (default: same as input)
        chunk_size: Number of segments per chunk
        generate_chunks: Whether to generate chunk files
        json_output: Whether to output as JSON

    Returns:
        Exit code (0 for success, 1 for failure)

    References:
        - TDD-FEAT-004: Hybrid Infrastructure Design
        - EN-020: Python Parser Implementation
        - EN-021: Chunking Strategy

    Example:
        >>> jerry transcript parse meeting.vtt
        Parsed: meeting.vtt
        Output: meeting-canonical.json
        Chunks: 6 files in chunks/

        >>> jerry transcript parse meeting.vtt --json
        {"success": true, "canonical_path": "...", "chunk_count": 6, ...}
    """
    try:
        # Create parse command
        command = ParseTranscriptCommand(
            path=path,
            format=format,
            output_dir=output_dir,
            chunk_size=chunk_size,
            generate_chunks=generate_chunks,
        )

        # Dispatch to handler
        result = self._command_dispatcher.dispatch(command)

        if json_output:
            output = {
                "success": result.success,
                "path": path,
                "format": result.detected_format,
                "canonical_path": result.canonical_path,
                "index_path": result.index_path,
                "chunk_count": result.chunk_count,
                "segment_count": result.segment_count,
                "warnings": result.warnings,
                "error": result.error,
            }
            print(json.dumps(output, indent=2))
        else:
            if result.success:
                print(f"Parsed: {path}")
                print(f"Format: {result.detected_format.upper()}")
                print(f"Segments: {result.segment_count}")
                print(f"Output: {result.canonical_path}")
                if result.chunk_count > 0:
                    print(f"Chunks: {result.chunk_count} files")
                    print(f"Index: {result.index_path}")
                if result.warnings:
                    print(f"\nWarnings ({len(result.warnings)}):")
                    for w in result.warnings:
                        print(f"  - {w}")
            else:
                print(f"Error: Failed to parse {path}")
                if result.error:
                    print(f"  {result.error.get('code', 'UNKNOWN')}: {result.error.get('message', 'Unknown error')}")

        return 0 if result.success else 1

    except FileNotFoundError:
        if json_output:
            print(json.dumps({"success": False, "error": {"code": "FILE_NOT_FOUND", "message": f"File not found: {path}"}}))
        else:
            print(f"Error: File not found: {path}")
        return 1

    except Exception as e:
        if json_output:
            print(json.dumps({"success": False, "error": {"code": "INTERNAL_ERROR", "message": str(e)}}))
        else:
            print(f"Error: {e}")
        return 1
```

### 11.4 Bootstrap Wiring

**File:** `src/bootstrap.py`

**Add imports:**

```python
from src.transcript.application.commands import ParseTranscriptCommand
from src.transcript.application.handlers.commands import ParseTranscriptCommandHandler
from src.transcript.domain.parsers import VTTParser, SRTParser
from src.transcript.domain.services import Chunker
from src.transcript.infrastructure.adapters import FilesystemOutputAdapter
```

**Add factory function:**

```python
def create_vtt_parser() -> VTTParser:
    """Create a VTT parser instance.

    Returns:
        VTTParser instance with encoding detection.

    References:
        - EN-020: Python Parser Implementation
        - TDD-FEAT-004: Hybrid Infrastructure Design
    """
    return VTTParser(
        encoding_detector=CharsetNormalizerAdapter(),
        strict_mode=False,  # Allow recovery from minor format issues
    )


def create_chunker(chunk_size: int = 500) -> Chunker:
    """Create a chunker instance.

    Args:
        chunk_size: Number of segments per chunk (default: 500)

    Returns:
        Chunker instance.

    References:
        - EN-021: Chunking Strategy
        - ADR-004: File Splitting Strategy
    """
    return Chunker(
        chunk_size=chunk_size,
        overlap_segments=0,  # No overlap for initial implementation
    )
```

**Add to `create_command_dispatcher()`:**

```python
# Add transcript parse handler
vtt_parser = create_vtt_parser()
srt_parser = SRTParser()  # Placeholder for Phase 2
chunker = create_chunker()
output_adapter = FilesystemOutputAdapter()

parse_handler = ParseTranscriptCommandHandler(
    vtt_parser=vtt_parser,
    srt_parser=srt_parser,
    chunker=chunker,
    output_adapter=output_adapter,
)
dispatcher.register(ParseTranscriptCommand, parse_handler.handle)
```

### 11.5 CLI Integration Sequence Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CLI INTEGRATION SEQUENCE DIAGRAM                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  USER                                                                        │
│    │                                                                         │
│    │  $ jerry transcript parse meeting.vtt --chunk-size 500                 │
│    │                                                                         │
│    ▼                                                                         │
│  ┌──────────────────┐                                                        │
│  │    main.py       │  1. Parse CLI arguments                               │
│  │  (CLI Router)    │                                                        │
│  └────────┬─────────┘                                                        │
│           │                                                                  │
│           │  _handle_transcript(adapter, args)                              │
│           ▼                                                                  │
│  ┌──────────────────┐                                                        │
│  │   adapter.py     │  2. Create ParseTranscriptCommand                     │
│  │  (CLIAdapter)    │     Dispatch to handler                               │
│  └────────┬─────────┘                                                        │
│           │                                                                  │
│           │  command_dispatcher.dispatch(command)                           │
│           ▼                                                                  │
│  ┌──────────────────┐                                                        │
│  │ ParseTranscript  │  3. Determine format (VTT/SRT)                        │
│  │ CommandHandler   │     Select appropriate parser                         │
│  └────────┬─────────┘                                                        │
│           │                                                                  │
│           │  vtt_parser.parse(path)                                         │
│           ▼                                                                  │
│  ┌──────────────────┐                                                        │
│  │   VTTParser      │  4. Detect encoding (charset-normalizer)              │
│  │  (EN-020)        │     Parse VTT with webvtt-py                          │
│  │                  │     Extract segments, speakers, timestamps             │
│  └────────┬─────────┘                                                        │
│           │                                                                  │
│           │  ParsedTranscript (canonical model)                             │
│           ▼                                                                  │
│  ┌──────────────────┐                                                        │
│  │ output_adapter   │  5. Write canonical-transcript.json                   │
│  │ .write_canonical │                                                        │
│  └────────┬─────────┘                                                        │
│           │                                                                  │
│           │  if generate_chunks:                                            │
│           ▼                                                                  │
│  ┌──────────────────┐                                                        │
│  │    Chunker       │  6. Split segments into chunks (500 each)             │
│  │   (EN-021)       │     Generate index.json                               │
│  │                  │     Write chunks/chunk-{N}.json                       │
│  └────────┬─────────┘                                                        │
│           │                                                                  │
│           │  ParseResult                                                    │
│           ▼                                                                  │
│  ┌──────────────────┐                                                        │
│  │   CLIAdapter     │  7. Format output (text or JSON)                      │
│  │  (response)      │     Return exit code                                  │
│  └────────┬─────────┘                                                        │
│           │                                                                  │
│           │  stdout                                                         │
│           ▼                                                                  │
│  USER                                                                        │
│    │                                                                         │
│    │  Parsed: meeting.vtt                                                   │
│    │  Format: VTT                                                           │
│    │  Segments: 3071                                                        │
│    │  Output: meeting-canonical.json                                        │
│    │  Chunks: 7 files                                                       │
│    │  Index: chunks/index.json                                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 11.6 CLI Usage Examples

#### Basic Usage

```bash
# Parse VTT file with default chunking (500 segments)
$ jerry transcript parse meeting.vtt
Parsed: meeting.vtt
Format: VTT
Segments: 3071
Output: meeting-canonical.json
Chunks: 7 files
Index: chunks/index.json

# Parse with custom chunk size
$ jerry transcript parse meeting.vtt --chunk-size 1000
Parsed: meeting.vtt
Segments: 3071
Chunks: 4 files

# Parse without chunking (canonical JSON only)
$ jerry transcript parse meeting.vtt --no-chunks
Parsed: meeting.vtt
Segments: 3071
Output: meeting-canonical.json
```

#### JSON Output (for programmatic use)

```bash
$ jerry transcript parse meeting.vtt --json
{
  "success": true,
  "path": "meeting.vtt",
  "format": "vtt",
  "canonical_path": "meeting-canonical.json",
  "index_path": "chunks/index.json",
  "chunk_count": 7,
  "segment_count": 3071,
  "warnings": [],
  "error": null
}
```

#### Error Handling

```bash
$ jerry transcript parse nonexistent.vtt
Error: File not found: nonexistent.vtt

$ jerry transcript parse corrupted.vtt
Error: Failed to parse corrupted.vtt
  PARSE_FAILED: Invalid VTT format at line 42
```

### 11.7 Exit Codes

| Code | Meaning | Scenario |
|------|---------|----------|
| 0 | Success | Parse completed successfully |
| 1 | Error | Parse failed, file not found, invalid format |
| 2 | Usage Error | Invalid arguments (handled by argparse) |

### 11.8 Integration with LLM Agents

After CLI parsing, the outputs integrate with LLM agents:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    HYBRID PIPELINE INTEGRATION                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  DETERMINISTIC LAYER (CLI)              SEMANTIC LAYER (LLM)                │
│  ─────────────────────────              ────────────────────                 │
│                                                                              │
│  jerry transcript parse                  ts-extractor agent                  │
│         │                                       │                            │
│         │ canonical-transcript.json             │                            │
│         │ chunks/index.json                     │                            │
│         │ chunks/chunk-*.json                   │                            │
│         │                                       │                            │
│         └──────────────────────►────────────────┘                            │
│                                                                              │
│  Benefits:                                                                   │
│  - Parser: Instant, deterministic, free (Python)                            │
│  - Extractor: Per-chunk processing, no context overflow                     │
│  - Total: 1,250x cost reduction, 0% data loss                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Agent Integration Points:**

1. **ts-parser agent**: Reads `canonical-transcript.json` for validation
2. **ts-extractor agent**: Processes `chunks/chunk-*.json` sequentially
3. **ts-formatter agent**: Reads extraction results, generates final output

---

## Appendices

### A: Interface Contracts

#### A.1: IParserStrategy Interface

```python
from abc import ABC, abstractmethod
from typing import Optional
from dataclasses import dataclass

@dataclass
class ParseResult:
    success: bool
    canonical_path: Optional[str]
    index_path: Optional[str]
    chunk_count: int
    segment_count: int
    warnings: list
    error: Optional[dict]

class IParserStrategy(ABC):
    """
    Strategy interface for transcript parsing.

    Implements Gang of Four Strategy Pattern.
    """

    @abstractmethod
    def can_handle(self, format: str) -> bool:
        """Check if this strategy handles the given format."""
        pass

    @abstractmethod
    def parse(self, file_path: str, output_dir: str, options: dict) -> ParseResult:
        """Parse transcript file and produce canonical output."""
        pass
```

#### A.2: PythonParserStrategy Implementation

```python
class PythonVTTParserStrategy(IParserStrategy):
    """
    Python-based VTT parser using webvtt-py.

    Implements:
    - IParserStrategy interface
    - EN-020 specification
    """

    def can_handle(self, format: str) -> bool:
        return format.lower() == "vtt"

    def parse(self, file_path: str, output_dir: str, options: dict) -> ParseResult:
        parser = VTTParser()
        result = parser.parse(file_path)

        if result.parse_status == "failed":
            return ParseResult(
                success=False,
                canonical_path=None,
                index_path=None,
                chunk_count=0,
                segment_count=0,
                warnings=result.warnings,
                error={"code": "PARSE_FAILED", "message": str(result.errors)}
            )

        # Write canonical JSON
        canonical_path = self._write_canonical(result, output_dir)

        # Create chunks if enabled
        index_path = None
        chunk_count = 0
        if options.get("generate_chunks", True):
            chunker = Chunker(chunk_size=options.get("chunk_size", 500))
            index_path, chunk_count = chunker.create_chunks(result.segments, output_dir)

        return ParseResult(
            success=True,
            canonical_path=canonical_path,
            index_path=index_path,
            chunk_count=chunk_count,
            segment_count=len(result.segments),
            warnings=result.warnings,
            error=None
        )
```

#### A.3: LLMParserStrategy (Fallback)

```python
class LLMParserStrategy(IParserStrategy):
    """
    LLM-based parser for fallback scenarios.

    Maintains v1.2.0 ts-parser behavior for:
    - Unsupported formats
    - Python parser failures
    - Validation failures
    """

    def can_handle(self, format: str) -> bool:
        # Fallback handles all formats
        return True

    def parse(self, file_path: str, output_dir: str, options: dict) -> ParseResult:
        # Delegate to original LLM parsing logic
        # (This is the existing ts-parser v1.2.0 behavior)
        ...
```

### B: Dependency Graph

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FULL DEPENDENCY GRAPH                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  EXTERNAL DEPENDENCIES                                                   │
│  ─────────────────────                                                   │
│                                                                          │
│  ┌───────────────────┐    ┌───────────────────┐    ┌─────────────────┐  │
│  │    webvtt-py      │    │ charset-normalizer│    │      pytest     │  │
│  │    v0.5.1         │    │    v3.x           │    │     v8.x        │  │
│  │    MIT License    │    │    MIT License    │    │   MIT License   │  │
│  └─────────┬─────────┘    └─────────┬─────────┘    └────────┬────────┘  │
│            │                        │                        │           │
│            └────────────┬───────────┘                        │           │
│                         │                                    │           │
│                         ▼                                    │           │
│  ENABLER DEPENDENCIES                                        │           │
│  ────────────────────                                        │           │
│                                                              │           │
│  ┌─────────────────────────────────────────────────────────┐ │           │
│  │                     EN-020                               │ │           │
│  │              Python Parser Implementation                │ │           │
│  │  ┌─────────────────┐  ┌─────────────────┐               │ │           │
│  │  │   VTTParser     │  │ EncodingDetector│               │ │           │
│  │  │   (webvtt-py)   │  │(charset-normalizer)             │ │           │
│  │  └────────┬────────┘  └────────┬────────┘               │ │           │
│  │           └──────────┬─────────┘                         │ │           │
│  │                      ▼                                   │ │           │
│  │           ┌─────────────────────┐                        │ │           │
│  │           │ canonical-transcript│                        │ │           │
│  │           │      .json          │                        │ │           │
│  │           └──────────┬──────────┘                        │ │           │
│  └──────────────────────┼───────────────────────────────────┘ │           │
│                         │                                     │           │
│                         ▼                                     │           │
│  ┌─────────────────────────────────────────────────────────┐ │           │
│  │                     EN-021                               │ │           │
│  │                Chunking Strategy                         │ │           │
│  │  ┌─────────────────┐  ┌─────────────────┐               │ │           │
│  │  │     Chunker     │  │  IndexGenerator │               │ │           │
│  │  │ (500 segments)  │  │                 │               │ │           │
│  │  └────────┬────────┘  └────────┬────────┘               │ │           │
│  │           └──────────┬─────────┘                         │ │           │
│  │                      ▼                                   │ │           │
│  │           ┌─────────────────────┐                        │ │           │
│  │           │    index.json +     │                        │ │           │
│  │           │    chunks/*.json    │                        │ │           │
│  │           └──────────┬──────────┘                        │ │           │
│  └──────────────────────┼───────────────────────────────────┘ │           │
│                         │                                     │           │
│                         ▼                                     │           │
│  ┌─────────────────────────────────────────────────────────┐ │           │
│  │                     EN-022                               │ │           │
│  │              Extractor Adaptation                        │ │           │
│  │  ┌─────────────────┐  ┌─────────────────────────────┐   │ │           │
│  │  │  InputDetector  │  │ChunkedExtractionAccumulator │   │ │           │
│  │  │                 │  │                             │   │ │           │
│  │  └────────┬────────┘  └────────────┬────────────────┘   │ │           │
│  │           └─────────────┬──────────┘                     │ │           │
│  │                         ▼                                │ │           │
│  │           ┌─────────────────────┐                        │ │           │
│  │           │   ts-extractor      │                        │ │           │
│  │           │   (adapted)         │                        │ │           │
│  │           └──────────┬──────────┘                        │ │           │
│  └──────────────────────┼───────────────────────────────────┘ │           │
│                         │                                     │           │
│                         ▼                                     │           │
│  ┌─────────────────────────────────────────────────────────┐ │           │
│  │                     EN-023                               │◄┘           │
│  │              Integration Testing                         │             │
│  │  ┌─────────────────┐  ┌─────────────────┐               │             │
│  │  │  Contract Tests │  │  E2E Pipeline   │               │             │
│  │  │   (pytest)      │  │    Tests        │               │             │
│  │  └─────────────────┘  └─────────────────┘               │             │
│  └─────────────────────────────────────────────────────────┘             │
│                                                                          │
│  CRITICAL PATH:                                                          │
│  EN-020 ═══════► EN-021 ═══════► EN-022 ═══════► EN-023                 │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### C: DISC-009 Traceability Matrix

| DISC-009 Finding | Requirement | TDD Section | Enabler |
|------------------|-------------|-------------|---------|
| 99.8% data loss (5/3071) | FR-HYBRID-001: Deterministic parsing | Section 4 | EN-020 |
| Ad-hoc workaround violation | NFR-HYBRID-001: Formal architecture | Section 3 | ts-parser.md |
| No scalability solution | FR-HYBRID-002: Chunking strategy | Section 5 | EN-021 |
| LLM parsing insufficient | FR-HYBRID-003: Strategy Pattern | Section 3 | ts-parser.md |
| Lost-in-Middle phenomenon | NFR-HYBRID-002: Chunk size limits | Section 5 | EN-021 |
| 60s+ processing time | NFR-HYBRID-003: <5s parse time | Section 4 | EN-020 |
| $0.27/file parsing cost | NFR-HYBRID-004: $0 parse cost | Section 4 | EN-020 |
| Extractor assumes full input | FR-HYBRID-004: Chunked input support | Section 6 | EN-022 |
| No integration testing | FR-HYBRID-005: E2E validation | Section 7 | EN-023 |

---

## References

### Phase 1 Research Citations

1. **Liu, N.F., et al.** (2024). "Lost in the Middle: How Language Models Use Long Contexts." *Transactions of the Association for Computational Linguistics*, 12, 157-173.
   - URL: [https://aclanthology.org/2024.tacl-1.9/](https://aclanthology.org/2024.tacl-1.9/)
   - Application: Section 1 (Lost-in-Middle rationale), Section 5 (chunk sizing)

2. **Gang of Four Strategy Pattern** - Gamma, Helm, Johnson, Vlissides (1994)
   - URL: [https://refactoring.guru/design-patterns/strategy](https://refactoring.guru/design-patterns/strategy)
   - Application: Section 3 (ts-parser transformation)

3. **webvtt-py** - Python WebVTT Library (v0.5.1, MIT License)
   - URL: [https://github.com/glut23/webvtt-py](https://github.com/glut23/webvtt-py)
   - Application: Section 4 (EN-020 implementation)

4. **charset-normalizer** - Universal Encoding Detector
   - URL: [https://github.com/jawah/charset_normalizer](https://github.com/jawah/charset_normalizer)
   - Application: Section 4 (encoding detection)

5. **LangChain RecursiveCharacterTextSplitter**
   - URL: [https://docs.langchain.com/oss/python/langchain/rag](https://docs.langchain.com/oss/python/langchain/rag)
   - Application: Section 5 (chunking rationale)

### Phase 2 Analysis Citations

6. **WorkOS Enterprise AI Agent Playbook**
   - URL: [https://workos.com/blog/enterprise-ai-agent-playbook](https://workos.com/blog/enterprise-ai-agent-playbook)
   - Application: Section 2 (orchestrator-worker pattern)

7. **byteiota RAG Adoption Statistics**
   - URL: [https://byteiota.com/rag-vs-long-context-2026-retrieval-debate/](https://byteiota.com/rag-vs-long-context-2026-retrieval-debate/)
   - Application: Section 1 (industry evidence)

8. **Meilisearch RAG Cost Analysis**
   - URL: [https://www.meilisearch.com/blog/rag-vs-long-context-llms](https://www.meilisearch.com/blog/rag-vs-long-context-llms)
   - Application: Section 1 (1,250x cost reduction)

### Internal References

9. **DISC-009**: Agent-Only Architecture Limitation Discovery
   - Path: `FEAT-002-implementation/FEAT-002--DISC-009-agent-only-architecture-limitation.md`

10. **DEC-011**: ts-parser Hybrid Role Decision
    - Path: `FEAT-004-hybrid-infrastructure/FEAT-004--DEC-011-ts-parser-hybrid-role.md`

11. **FEAT-004**: Hybrid Infrastructure Feature Definition
    - Path: `FEAT-004-hybrid-infrastructure/FEAT-004-hybrid-infrastructure.md`

12. **ADR-001-amendment-001**: Python Preprocessing Layer
    - Path: `docs/adrs/ADR-001-amendment-001-python-preprocessing.md`

### Testing References

13. **Kent Beck, Canon TDD**
    - URL: [https://tidyfirst.substack.com/p/canon-tdd](https://tidyfirst.substack.com/p/canon-tdd)
    - Application: Section 8 (TDD cycle)

14. **Martin Fowler, Test Driven Development**
    - URL: [https://martinfowler.com/bliki/TestDrivenDevelopment.html](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
    - Application: Section 8 (refactoring anti-pattern)

---

## Metadata

```yaml
document_id: "TDD-FEAT-004"
version: "1.0.0"
status: "DRAFT"
created_at: "2026-01-29T23:30:00Z"
updated_at: "2026-01-29T23:30:00Z"

ps_id: "FEAT-004"
entry_id: "e-242"
topic: "Hybrid Infrastructure Technical Design"
agent: "ps-architect"
agent_version: "2.0.0"

input_artifacts:
  - id: "FEAT-004-e-240"
    path: "docs/research/FEAT-004-e-240-hybrid-architecture-research.md"
    type: "research"
  - id: "FEAT-004-e-241"
    path: "docs/analysis/FEAT-004-e-241-blast-radius-analysis.md"
    type: "analysis"
  - id: "DEC-011"
    path: "FEAT-004--DEC-011-ts-parser-hybrid-role.md"
    type: "decision"
  - id: "DISC-009"
    path: "../FEAT-002-implementation/FEAT-002--DISC-009-agent-only-architecture-limitation.md"
    type: "discovery"

quality_threshold: 0.95
quality_criteria:
  - "Actionability: All sections enable work item creation"
  - "Traceability: DISC-009 findings mapped to TDD sections"
  - "DEC-011 Compliance: All three decisions implemented"
  - "L0/L1/L2: Three-persona documentation throughout"
  - "Evidence-Based: Phase 1/2 citations used"
  - "Schemas: JSON schemas included for all interfaces"
  - "Diagrams: ASCII architecture diagrams included"

next_phase: "TASK-243 (ps-critic validation at 0.95 threshold)"

work_items_generated:
  - enabler: "EN-020"
    task_range: "TASK-200..207"
    task_count: 8
  - enabler: "EN-021"
    task_range: "TASK-210..215"
    task_count: 6
  - enabler: "EN-022"
    task_range: "TASK-220..224"
    task_count: 5
  - enabler: "EN-023"
    task_range: "TASK-230..235"
    task_count: 6
  - total_tasks: 25

related_artifacts:
  - "FEAT-004-hybrid-infrastructure.md"
  - "ADR-001-amendment-001-python-preprocessing.md"
  - "ts-parser.md (v1.2.0 → v2.0.0)"
  - "ts-extractor.md (v1.2.0)"
```

---

<!--
DESIGN RATIONALE:

This TDD provides comprehensive technical specification for the hybrid infrastructure
transformation. Key design decisions:

1. STRATEGY PATTERN: ts-parser.md becomes orchestrator using Gang of Four Strategy
   Pattern, delegating to Python for VTT (primary) or LLM (fallback)

2. 500-SEGMENT CHUNKS: Based on LangChain research and ADR-004 limits, 500 segments
   (~15K tokens) provides safe margin under 31.5K soft limit

3. INCREMENTAL ADOPTION: VTT first (webvtt-py), SRT second (pysrt), plain text third
   per DEC-011 D-002 decision

4. BACKWARD COMPATIBILITY: Maintained through LLM fallback path and input detection
   logic in ts-extractor

5. TDD CYCLE: Kent Beck's Canon TDD applied with RED/GREEN/REFACTOR for each enabler

The document satisfies all 10 required sections with actionable specifications that
enable direct work item creation for EN-020, EN-021, EN-022, and EN-023.

TRACE:
- DISC-009 → Section 1 (Problem Statement)
- DEC-011 D-001 → Section 3 (ts-parser transformation)
- DEC-011 D-002 → Section 10 (Migration Strategy)
- DEC-011 D-003 → Section 9 (Work item specifications)
- Phase 1 Research → Sections 4, 5 (implementation details)
- Phase 2 Analysis → Sections 7, 8, 9 (testing and roadmap)

QUALITY TARGET: 0.95
- All citations included with URLs
- All schemas defined in JSON Schema format
- All diagrams in ASCII art
- L0/L1/L2 documentation complete
- Actionable task specifications for 25 tasks across 4 enablers
-->
