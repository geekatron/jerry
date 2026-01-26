# Technical Design Document: ts-parser Agent

> **Document ID:** TDD-ts-parser
> **Version:** 1.0
> **Status:** DRAFT
> **Date:** 2026-01-26
> **Author:** ps-architect agent
> **Token Count:** ~4,800 (within 5K target per AC-005)
> **Parent:** [TDD-transcript-skill.md](./TDD-transcript-skill.md)

---

## Document Navigation

| Level | Audience | Sections |
|-------|----------|----------|
| **L0** | Executive / Stakeholders | [Executive Summary](#l0-executive-summary) |
| **L1** | Software Engineers | [Technical Design](#l1-technical-design) |
| **L2** | Principal Architects | [Strategic Considerations](#l2-strategic-considerations) |

---

# L0: Executive Summary

## The Reception Desk Analogy

The **ts-parser agent** is like a **Reception Desk** at a Translation Office:

```
THE RECEPTION DESK (ts-parser)
==============================

           INCOMING DOCUMENTS                 PROCESSED OUTPUT
           ──────────────────                 ────────────────

    ┌───────────────┐
    │ VTT File      │ ────┐
    │ (60% share)   │     │
    └───────────────┘     │
                          │     ┌─────────────────────────────┐
    ┌───────────────┐     │     │                             │
    │ SRT File      │ ────┼────►│    CANONICAL TRANSCRIPT     │
    │ (35% share)   │     │     │    ────────────────────     │
    └───────────────┘     │     │                             │
                          │     │    Unified JSON format      │
    ┌───────────────┐     │     │    Ready for extraction     │
    │ Plain Text    │ ────┘     │                             │
    │ (5% share)    │           └─────────────────────────────┘
    └───────────────┘

    "I accept any format. I output one standard format."
```

**Key Responsibilities:**
1. **Accept** - VTT, SRT, and plain text files
2. **Detect** - Auto-identify format from content
3. **Parse** - Extract timestamps, speakers, text
4. **Normalize** - Convert to canonical JSON

**Why This Matters:**
- **100% market gap** - No competitor processes text-first transcripts
- **35% user value** - VTT/SRT import is the top-valued feature

---

# L1: Technical Design

## 1. Input Format Specifications

### 1.1 WebVTT Format (FR-001)

```
WEBVTT FORMAT GRAMMAR
=====================

WEBVTT        = "WEBVTT" NEWLINE METADATA* CUE+
METADATA      = NOTE / STYLE
CUE           = CUE_ID? TIMESTAMP_LINE PAYLOAD+
TIMESTAMP_LINE = START_TIME " --> " END_TIME SETTINGS?
START_TIME    = TIMESTAMP
END_TIME      = TIMESTAMP
TIMESTAMP     = HH:MM:SS.mmm | MM:SS.mmm
PAYLOAD       = TEXT_LINE | VOICE_TAG TEXT_LINE
VOICE_TAG     = "<v " SPEAKER_NAME ">"

Example:
────────
WEBVTT

00:00:00.000 --> 00:00:05.500
<v Alice>Good morning everyone.

00:00:05.500 --> 00:00:10.200
<v Bob>Good morning Alice.
```

### 1.2 SRT Format (FR-002)

```
SRT FORMAT GRAMMAR
==================

SRT           = CUE+
CUE           = INDEX NEWLINE TIMESTAMP_LINE NEWLINE TEXT+
INDEX         = NUMBER
TIMESTAMP_LINE = START_TIME " --> " END_TIME
TIMESTAMP     = HH:MM:SS,mmm | HH:MM:SS.mmm    <- Note: comma OR period
TEXT          = TEXT_LINE | SPEAKER_PREFIX TEXT_LINE
SPEAKER_PREFIX = NAME ":"

Example:
────────
1
00:00:00,000 --> 00:00:05,500
Alice: Good morning everyone.

2
00:00:05,500 --> 00:00:10,200
Bob: Good morning Alice.
```

### 1.3 Plain Text Format (FR-003)

```
PLAIN TEXT FORMAT PATTERNS
==========================

PATTERN 1: "Speaker: text"
─────────────────────────
Alice: Good morning everyone.
Bob: Good morning Alice.

PATTERN 2: "[Speaker] text"
───────────────────────────
[Alice] Good morning everyone.
[Bob] Good morning Alice.

PATTERN 3: "SPEAKER: text"
──────────────────────────
ALICE: Good morning everyone.
BOB: Good morning Alice.
```

## 2. Format Detection Algorithm (FR-004)

```
FORMAT DETECTION FLOWCHART
==========================

            ┌─────────────────────┐
            │   Read First Line   │
            └──────────┬──────────┘
                       │
                       ▼
            ┌─────────────────────┐
            │ Starts with "WEBVTT"│
            └──────────┬──────────┘
                       │
              ┌────────┴────────┐
              │                 │
          YES ▼             NO  ▼
     ┌────────────┐    ┌─────────────────────┐
     │ Format=VTT │    │ Line matches        │
     └────────────┘    │ /^\d+$/  (index)    │
                       └──────────┬──────────┘
                                  │
                         ┌────────┴────────┐
                         │                 │
                     YES ▼             NO  ▼
                ┌────────────┐    ┌─────────────────┐
                │ Check Line │    │ Format=PLAIN    │
                │ 2 for -->  │    │ (fallback)      │
                └──────┬─────┘    └─────────────────┘
                       │
              ┌────────┴────────┐
              │                 │
          YES ▼             NO  ▼
     ┌────────────┐    ┌─────────────────┐
     │ Format=SRT │    │ Format=PLAIN    │
     └────────────┘    └─────────────────┘
```

## 3. Canonical Output Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "transcript-skill/canonical-transcript-v1.0",
  "title": "Canonical Transcript",
  "type": "object",
  "required": ["version", "source", "segments"],
  "properties": {
    "version": {
      "type": "string",
      "const": "1.0"
    },
    "source": {
      "type": "object",
      "required": ["format", "encoding"],
      "properties": {
        "format": {
          "type": "string",
          "enum": ["vtt", "srt", "plain"]
        },
        "encoding": {
          "type": "string",
          "default": "utf-8"
        },
        "file_path": {
          "type": "string"
        }
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "duration_ms": { "type": "integer", "minimum": 0 },
        "segment_count": { "type": "integer", "minimum": 0 },
        "detected_speakers": { "type": "integer", "minimum": 0 }
      }
    },
    "segments": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "start_ms", "text"],
        "properties": {
          "id": { "type": "string", "pattern": "^seg-\\d{3,}$" },
          "start_ms": { "type": "integer", "minimum": 0 },
          "end_ms": { "type": "integer", "minimum": 0 },
          "speaker": { "type": ["string", "null"] },
          "text": { "type": "string", "minLength": 1 },
          "raw_text": { "type": "string" }
        }
      }
    }
  }
}
```

## 4. Timestamp Normalization (NFR-006)

```
TIMESTAMP NORMALIZATION ALGORITHM
=================================

INPUT FORMATS                           OUTPUT FORMAT
─────────────                           ─────────────

VTT:  "00:05:23.450"  ──┐
VTT:  "05:23.450"     ──┤
SRT:  "00:05:23,450"  ──┼──►  323450 (milliseconds)
SRT:  "0:05:23,450"   ──┤
Plain: (no timestamp) ──┘──►  null (inferred from order)

NORMALIZATION STEPS:
────────────────────
1. Replace comma with period (SRT compatibility)
2. Parse as HH:MM:SS.mmm or MM:SS.mmm
3. Convert to total milliseconds
4. Validate: end_ms > start_ms
5. Handle negative duration: log warning, swap times

PRECISION: 10 milliseconds (per NFR-006)
```

## 5. Encoding Detection (NFR-007)

```
ENCODING DETECTION FLOW
=======================

    ┌───────────────────────┐
    │  Read raw bytes       │
    └───────────┬───────────┘
                │
                ▼
    ┌───────────────────────┐
    │  Check BOM            │
    │  (Byte Order Mark)    │
    └───────────┬───────────┘
                │
       ┌────────┴────────┐
       │                 │
   BOM found         No BOM
       │                 │
       ▼                 ▼
  ┌─────────┐    ┌───────────────┐
  │ UTF-8   │    │ Try decode as │
  │ UTF-16  │    │ UTF-8         │
  │ UTF-16LE│    └───────┬───────┘
  └─────────┘            │
                ┌────────┴────────┐
                │                 │
            SUCCESS           FAILURE
                │                 │
                ▼                 ▼
         ┌─────────┐     ┌────────────────┐
         │ UTF-8   │     │ Try fallbacks: │
         └─────────┘     │ - Windows-1252 │
                         │ - ISO-8859-1   │
                         │ - Latin-1      │
                         └────────────────┘
```

## 6. Error Handling Matrix

| Error | Detection Method | Recovery Strategy | Log Level |
|-------|------------------|-------------------|-----------|
| Malformed timestamp | Regex fail | Use best-effort parse | WARNING |
| Negative duration | end < start | Swap start/end | WARNING |
| Missing speaker | No voice tag/prefix | Use null | INFO |
| Empty utterance | len(text) == 0 | Skip segment | DEBUG |
| Unknown encoding | Decode exception | Try fallbacks | WARNING |
| File not found | OS exception | Raise error | ERROR |
| File too large | Size > 50MB | Stream processing | INFO |

## 7. Component Architecture

```
TS-PARSER COMPONENT DIAGRAM
===========================

┌─────────────────────────────────────────────────────────────────────────┐
│                          ts-parser Agent                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                        FormatDetector                             │  │
│  │ ──────────────────────────────────────────────────────────────────  │  │
│  │ + detect(content: bytes) -> Format                               │  │
│  │ + _check_vtt_header(line: str) -> bool                          │  │
│  │ + _check_srt_pattern(lines: List[str]) -> bool                  │  │
│  └───────────────────────────┬──────────────────────────────────────┘  │
│                              │                                          │
│         ┌────────────────────┼────────────────────┐                    │
│         │                    │                    │                    │
│         ▼                    ▼                    ▼                    │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐            │
│  │ VTTProcessor │    │ SRTProcessor │    │ PlainParser  │            │
│  │ ────────────  │    │ ────────────  │    │ ────────────  │            │
│  │ parse()      │    │ parse()      │    │ parse()      │            │
│  │ _parse_cue() │    │ _parse_block │    │ _detect_pat  │            │
│  │ _voice_tag() │    │ _timestamp() │    │ _extract()   │            │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘            │
│         │                   │                   │                      │
│         └───────────────────┼───────────────────┘                      │
│                             │                                          │
│                             ▼                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                        Normalizer                                 │  │
│  │ ──────────────────────────────────────────────────────────────────  │  │
│  │ + normalize(segments: List[RawSegment]) -> List[Segment]        │  │
│  │ + _normalize_timestamp(ts: str) -> int                          │  │
│  │ + _detect_encoding(content: bytes) -> str                       │  │
│  └───────────────────────────┬──────────────────────────────────────┘  │
│                              │                                          │
│                              ▼                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                      SchemaValidator                              │  │
│  │ ──────────────────────────────────────────────────────────────────  │  │
│  │ + validate(transcript: dict) -> ValidationResult                │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  OUTPUT: CanonicalTranscript JSON                                       │
└─────────────────────────────────────────────────────────────────────────┘
```

---

# L2: Strategic Considerations

## 8. Design Pattern Application

### 8.1 PAT-002: Defensive Parsing

```
DEFENSIVE PARSING IMPLEMENTATION
================================

PRINCIPLE: "Accept liberally, produce consistently"

BEFORE (Brittle):
─────────────────
if timestamp != "HH:MM:SS.mmm":
    raise ParseError("Invalid timestamp")

AFTER (Defensive):
──────────────────
def parse_timestamp(ts: str) -> int | None:
    patterns = [
        r"(\d{1,2}):(\d{2}):(\d{2})[.,](\d{3})",  # HH:MM:SS.mmm
        r"(\d{1,2}):(\d{2})[.,](\d{3})",           # MM:SS.mmm
        r"(\d+)",                                   # raw milliseconds
    ]
    for pattern in patterns:
        match = re.match(pattern, ts)
        if match:
            return convert_to_ms(match)
    log.warning(f"Unparseable timestamp: {ts}")
    return None  # Continue with null timestamp
```

### 8.2 Large File Handling (NFR-007)

**Strategy:** Stream processing for files > 10MB

```
STREAMING PARSER APPROACH
=========================

     ┌────────────────┐
     │  File Input    │
     │  (60+ min)     │
     └───────┬────────┘
             │
             ▼
     ┌────────────────┐       ┌─────────────┐
     │  Line Iterator │──────►│ Process in  │
     │  (lazy read)   │       │ 100-segment │
     └────────────────┘       │ batches     │
                              └──────┬──────┘
                                     │
                                     ▼
                              ┌─────────────┐
                              │ Yield to    │
                              │ output      │
                              │ stream      │
                              └─────────────┘

MEMORY: O(batch_size) not O(file_size)
TARGET: <500 MB RAM (NFR-002)
```

## 9. Risk Mitigation

| Risk | Score | Mitigation in ts-parser |
|------|-------|-------------------------|
| R-002: SRT timestamp malformation | 8 (YELLOW) | Both `.` and `,` supported in regex |
| R-003: Encoding issues | 6 (GREEN) | Multi-encoding fallback chain |

## 10. Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| 1-hour transcript parse time | < 2 seconds | Benchmark test |
| Memory usage (peak) | < 100 MB | Profiler |
| Segment throughput | > 500 seg/sec | Unit test |

---

## 11. Requirements Traceability

| Requirement | Implementation | Section |
|-------------|----------------|---------|
| FR-001 (VTT) | VTTProcessor | 1.1, 7 |
| FR-002 (SRT) | SRTProcessor | 1.2, 7 |
| FR-003 (Plain) | PlainParser | 1.3, 7 |
| FR-004 (Auto-detect) | FormatDetector | 2 |
| NFR-006 (Timestamps) | Normalizer | 4 |
| NFR-007 (Encoding) | Normalizer._detect_encoding | 5 |

---

## 12. ADR Compliance Checklist

| ADR | Decision | Compliance | Evidence |
|-----|----------|------------|----------|
| ADR-001 | Hybrid Architecture | [x] | ts-parser is single-purpose agent |
| ADR-002 | Token Limit | [x] | ~4,800 tokens (within 5K) |
| ADR-005 | Phased Impl. | [x] | Prompt-based agent design |

---

## 13. Related Documents

### Backlinks
- [TDD-transcript-skill.md](./TDD-transcript-skill.md) - Parent architecture
- [TASK-002-tdd-ts-parser.md](../TASK-002-tdd-ts-parser.md) - Task definition

### Forward Links
- [TDD-ts-extractor.md](./TDD-ts-extractor.md) - Consumes this output
- [ts-parser AGENT.md](../agents/ts-parser/AGENT.md) - Implementation (TASK-005)

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-26 | ps-architect | Initial design with schemas and algorithms |

---

*Document ID: TDD-ts-parser*
*Workflow ID: en005-tdd-20260126-001*
*Constitutional Compliance: P-002 (persisted), P-004 (provenance)*
