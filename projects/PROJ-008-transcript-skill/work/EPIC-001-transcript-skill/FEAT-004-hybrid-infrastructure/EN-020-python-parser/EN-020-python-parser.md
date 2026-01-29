# EN-020: Python Parser Implementation

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-01-28 (FEAT-004 Hybrid Infrastructure)
PURPOSE: Implement Python-based transcript parsing using webvtt-py
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-01-28T22:00:00Z
> **Due:** TBD
> **Completed:** -
> **Parent:** FEAT-004
> **Owner:** Claude
> **Effort:** 8

---

## Frontmatter

```yaml
id: "EN-020"
work_type: ENABLER
title: "Python Parser Implementation"
classification: ENABLER
status: pending
priority: high
impact: high
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-28T22:00:00Z"
updated_at: "2026-01-28T22:00:00Z"
parent_id: "FEAT-004"
tags: ["enabler", "python", "webvtt-py", "parsing"]
effort: 8
enabler_type: infrastructure
nfrs: ["NFR-001", "NFR-002"]
technical_debt_category: "architecture"
```

---

## Summary

Implement a Python-based transcript parser using the webvtt-py library that provides deterministic, testable, and fast parsing of VTT transcript files. This replaces the agent-only approach that proved unreliable for large files (90K+ tokens).

**Technical Value:**
- Sub-second parsing (vs. minutes with LLM)
- 100% deterministic output
- Unit testable with 90%+ coverage
- Foundation for chunking strategy (EN-021)

---

## Problem Statement

The ts-parser agent definition describes parsing behavior but lacks executable code. When processing large files like meeting-006-all-hands.vtt (9,220 lines, 3,071 segments), the LLM-based approach:

1. **Truncates output** - Produced 5 segments instead of 3,071
2. **Is expensive** - 90K tokens input costs significantly more than Python processing
3. **Is slow** - LLM inference takes minutes vs. milliseconds
4. **Is unreliable** - No guarantee of schema compliance

---

## Business Value

| Metric | Before (LLM) | After (Python) | Improvement |
|--------|--------------|----------------|-------------|
| Parse time | ~60 seconds | < 1 second | 60x faster |
| Cost per parse | ~$0.10 | ~$0.00 | 100% savings |
| Accuracy | Truncated | 100% complete | Reliable |
| Testability | Manual | Automated | CI/CD ready |

---

## Technical Approach

### Library Selection

**webvtt-py v0.5.1** selected based on:
- MIT License (permissive)
- Active maintenance
- VTT and SRT support
- Clean Python API
- Well-documented

### Implementation Architecture

```
skills/transcript/src/
├── __init__.py
├── parser/
│   ├── __init__.py
│   ├── base.py           # Abstract base parser
│   ├── vtt_parser.py     # WebVTT implementation
│   ├── srt_parser.py     # SRT implementation (Phase 2)
│   └── models.py         # Canonical data models
├── schema/
│   ├── __init__.py
│   └── canonical.py      # JSON schema definitions
└── utils/
    ├── __init__.py
    └── encoding.py       # Encoding detection
```

### Core Interface

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Segment:
    """Canonical transcript segment."""
    id: int
    start_ms: int
    end_ms: int
    speaker: Optional[str]
    text: str

@dataclass
class CanonicalTranscript:
    """Canonical transcript representation."""
    segments: List[Segment]
    speakers: List[str]
    duration_ms: int
    source_format: str
    source_file: str

class BaseParser(ABC):
    """Abstract base class for transcript parsers."""

    @abstractmethod
    def parse(self, file_path: str) -> CanonicalTranscript:
        """Parse transcript file to canonical format."""
        pass

class VTTParser(BaseParser):
    """WebVTT format parser using webvtt-py."""

    def parse(self, file_path: str) -> CanonicalTranscript:
        import webvtt

        segments = []
        speakers = set()

        for i, caption in enumerate(webvtt.read(file_path), start=1):
            speaker = self._extract_speaker(caption.text)
            text = self._clean_text(caption.text)

            segments.append(Segment(
                id=i,
                start_ms=self._timestamp_to_ms(caption.start),
                end_ms=self._timestamp_to_ms(caption.end),
                speaker=speaker,
                text=text
            ))

            if speaker:
                speakers.add(speaker)

        return CanonicalTranscript(
            segments=segments,
            speakers=sorted(speakers),
            duration_ms=segments[-1].end_ms if segments else 0,
            source_format="vtt",
            source_file=file_path
        )
```

### Voice Tag Extraction

Handle `<v Speaker Name>text</v>` format:

```python
import re

def _extract_speaker(self, text: str) -> Optional[str]:
    """Extract speaker from VTT voice tag."""
    match = re.match(r'<v\s+([^>]+)>', text)
    return match.group(1) if match else None

def _clean_text(self, text: str) -> str:
    """Remove voice tags from text."""
    return re.sub(r'<v\s+[^>]+>', '', text).replace('</v>', '').strip()
```

---

## NFRs Addressed

| NFR | Requirement | How Addressed |
|-----|-------------|---------------|
| NFR-001 | Process 5h transcripts | Python handles any size |
| NFR-002 | < 30s parse time | Sub-second parsing |
| NFR-007 | Encoding detection | chardet + fallback chain |

---

## Children (Tasks)

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| TASK-200 | Create parser module structure | pending | high |
| TASK-201 | Implement VTT parser with webvtt-py | pending | high |
| TASK-202 | Implement voice tag extraction | pending | high |
| TASK-203 | Add encoding detection fallback | pending | medium |
| TASK-204 | Create unit tests (90%+ coverage) | pending | high |
| TASK-205 | Integration test with meeting-006 | pending | high |

**Note:** Task IDs renumbered from TASK-150-155 to TASK-200-205 per DEC-010 (FEAT-004 task range allocation).

---

## Acceptance Criteria

### Definition of Done

- [ ] Parser module created at `skills/transcript/src/parser/`
- [ ] VTT parser implementation complete
- [ ] Voice tag extraction working
- [ ] Encoding detection with fallback chain
- [ ] Unit test coverage >= 90%
- [ ] Integration test passes with meeting-006-all-hands.vtt

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Parse meeting-006-all-hands.vtt producing exactly 3,071 segments | [ ] |
| AC-2 | Extract all 50 speakers from voice tags | [ ] |
| AC-3 | Timestamps normalized to milliseconds | [ ] |
| AC-4 | Output matches canonical JSON schema | [ ] |
| AC-5 | Handle UTF-8, Windows-1252, ISO-8859-1 encodings | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Parse time < 1 second for 5h transcript | [ ] |
| NFC-2 | Memory usage < 50MB | [ ] |
| NFC-3 | No network dependencies | [ ] |

---

## Risks and Mitigations

| Risk | Severity | Probability | Mitigation |
|------|----------|-------------|------------|
| webvtt-py edge cases | Medium | Low | Comprehensive unit tests |
| Encoding detection failures | Low | Medium | 3-stage fallback chain |
| Voice tag format variations | Medium | Medium | Regex pattern library |

---

## Dependencies

| Type | Item | Description |
|------|------|-------------|
| Depends On | webvtt-py | External Python library |
| Blocks | EN-021 | Chunking requires parsed output |
| Related | DISC-009 | Architecture recommendation |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-28 | Claude | pending | Enabler created from DISC-009 |

---

## Metadata

```yaml
id: "EN-020"
parent_id: "FEAT-004"
work_type: ENABLER
title: "Python Parser Implementation"
status: pending
priority: high
impact: high
enabler_type: infrastructure
tags: ["python", "webvtt-py", "parsing", "infrastructure"]
```
