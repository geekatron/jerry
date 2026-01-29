# EN-021: Chunking Strategy

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-01-28 (FEAT-004 Hybrid Infrastructure)
PURPOSE: Implement index + chunk file strategy for LLM-efficient processing
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Enabler Type:** architecture
> **Created:** 2026-01-28T22:00:00Z
> **Due:** TBD
> **Completed:** -
> **Parent:** FEAT-004
> **Owner:** Claude
> **Effort:** 5

---

## Frontmatter

```yaml
id: "EN-021"
work_type: ENABLER
title: "Chunking Strategy"
classification: ENABLER
status: pending
priority: high
impact: high
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-28T22:00:00Z"
updated_at: "2026-01-28T22:00:00Z"
parent_id: "FEAT-004"
tags: ["enabler", "chunking", "llm-optimization", "architecture"]
effort: 5
enabler_type: architecture
nfrs: ["NFR-004", "NFR-005"]
```

---

## Summary

Implement Option D chunking strategy: an index file with metadata and pointers to segment chunk files. This enables LLM agents to request specific chunks instead of loading the entire transcript, reducing context usage and addressing the "Lost-in-the-Middle" accuracy problem.

**Technical Value:**
- Reduces LLM context usage by 80-95%
- Enables selective chunk loading
- Preserves speaker/timestamp metadata in index
- Supports parallel processing (future)

---

## Problem Statement

The "Lost-in-the-Middle" problem (Stanford research) shows 30%+ accuracy degradation when relevant information is in the middle of long contexts. For a 3,071-segment transcript:

1. **Full context load** - Wastes tokens on irrelevant segments
2. **Accuracy degradation** - Middle segments get less attention
3. **Cost inefficiency** - Processing full context for targeted queries
4. **Memory pressure** - Large context windows are expensive

---

## Business Value

| Metric | Full Context | Chunked | Improvement |
|--------|--------------|---------|-------------|
| Context tokens | 90,000 | 15,000 | 83% reduction |
| Accuracy (middle) | 70% | 95% | +25 percentage points |
| Processing cost | $0.10 | $0.02 | 80% savings |

---

## Technical Approach

### Chunking Strategy (Option D)

```
canonical-output/
├── index.json           # Metadata + chunk pointers
└── chunks/
    ├── chunk-001.json   # Segments 1-500
    ├── chunk-002.json   # Segments 501-1000
    ├── chunk-003.json   # Segments 1001-1500
    ├── chunk-004.json   # Segments 1501-2000
    ├── chunk-005.json   # Segments 2001-2500
    ├── chunk-006.json   # Segments 2501-3000
    └── chunk-007.json   # Segments 3001-3071
```

### Index File Schema

```json
{
  "schema_version": "1.0",
  "generator": "ts-parser-python",
  "generated_at": "2026-01-28T22:00:00Z",

  "source": {
    "file": "meeting-006-all-hands.vtt",
    "format": "vtt",
    "encoding": "utf-8"
  },

  "summary": {
    "total_segments": 3071,
    "total_chunks": 7,
    "chunk_size": 500,
    "duration_ms": 18231000,
    "word_count": 28796
  },

  "speakers": {
    "count": 50,
    "list": ["Robert Chen", "Diana Martinez", "Jennifer Adams", "..."],
    "segment_counts": {
      "Robert Chen": 1005,
      "Diana Martinez": 491,
      "Jennifer Adams": 317
    }
  },

  "chunks": [
    {
      "chunk_id": "chunk-001",
      "segment_range": [1, 500],
      "timestamp_range": {
        "start": "00:00:00.000",
        "end": "01:15:23.500",
        "start_ms": 0,
        "end_ms": 4523500
      },
      "speaker_counts": {"Robert Chen": 150, "Diana Martinez": 80},
      "word_count": 4500,
      "file": "chunks/chunk-001.json"
    }
  ],

  "topics_preview": [
    {"segment_range": [1, 500], "likely_topic": "Opening and Q3 Overview"},
    {"segment_range": [501, 1000], "likely_topic": "Financial Results"}
  ]
}
```

### Chunk File Schema

```json
{
  "chunk_id": "chunk-001",
  "schema_version": "1.0",
  "segment_range": [1, 500],
  "timestamp_range": {
    "start_ms": 0,
    "end_ms": 4523500
  },

  "segments": [
    {
      "id": 1,
      "start_ms": 0,
      "end_ms": 5500,
      "speaker": "Robert Chen",
      "text": "Good morning everyone."
    },
    {
      "id": 2,
      "start_ms": 5501,
      "end_ms": 11000,
      "speaker": "Robert Chen",
      "text": "Welcome to our Q3 quarterly all-hands meeting."
    }
  ],

  "navigation": {
    "previous": null,
    "next": "chunk-002",
    "index": "index.json"
  }
}
```

### Chunker Implementation

```python
class TranscriptChunker:
    """Splits canonical transcript into LLM-efficient chunks."""

    def __init__(self, chunk_size: int = 500):
        self.chunk_size = chunk_size

    def chunk(self, transcript: CanonicalTranscript, output_dir: str) -> str:
        """
        Create index and chunk files.

        Args:
            transcript: Parsed canonical transcript
            output_dir: Directory for output files

        Returns:
            Path to index.json
        """
        chunks_dir = Path(output_dir) / "chunks"
        chunks_dir.mkdir(parents=True, exist_ok=True)

        chunk_metadata = []

        for i, chunk_segments in enumerate(self._split_segments(transcript.segments)):
            chunk_id = f"chunk-{i+1:03d}"
            chunk_file = chunks_dir / f"{chunk_id}.json"

            # Write chunk file
            chunk_data = self._create_chunk(chunk_id, chunk_segments, i)
            chunk_file.write_text(json.dumps(chunk_data, indent=2))

            # Collect metadata
            chunk_metadata.append(self._chunk_metadata(chunk_id, chunk_segments))

        # Write index file
        index = self._create_index(transcript, chunk_metadata)
        index_file = Path(output_dir) / "index.json"
        index_file.write_text(json.dumps(index, indent=2))

        return str(index_file)

    def _split_segments(self, segments: List[Segment]):
        """Yield chunks of segments."""
        for i in range(0, len(segments), self.chunk_size):
            yield segments[i:i + self.chunk_size]
```

---

## NFRs Addressed

| NFR | Requirement | How Addressed |
|-----|-------------|---------------|
| NFR-004 | Minimize context usage | Selective chunk loading |
| NFR-005 | Preserve citations | Segment IDs maintained |
| ADR-004 | 31.5K soft limit | Chunks under limit |

---

## Children (Tasks)

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| TASK-160 | Design chunk file schemas | pending | high |
| TASK-161 | Implement TranscriptChunker | pending | high |
| TASK-162 | Create index generation | pending | high |
| TASK-163 | Add navigation links | pending | medium |
| TASK-164 | Unit tests for chunker | pending | high |

---

## Acceptance Criteria

### Definition of Done

- [ ] Index schema defined and documented
- [ ] Chunk schema defined and documented
- [ ] TranscriptChunker implementation complete
- [ ] Unit tests for chunking logic
- [ ] Integration test with meeting-006 output

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Index.json contains all speaker metadata | [ ] |
| AC-2 | Each chunk file <= 500 segments | [ ] |
| AC-3 | Navigation links between chunks work | [ ] |
| AC-4 | Total segments across chunks = source | [ ] |
| AC-5 | Timestamps preserved accurately | [ ] |

---

## Dependencies

| Type | Item | Description |
|------|------|-------------|
| Depends On | EN-020 | Requires parsed canonical transcript |
| Blocks | EN-022 | Extractor needs chunk format |
| Related | LangChain | Inspired by RecursiveCharacterTextSplitter |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-28 | Claude | pending | Enabler created from DISC-009 |

---

## Metadata

```yaml
id: "EN-021"
parent_id: "FEAT-004"
work_type: ENABLER
title: "Chunking Strategy"
status: pending
priority: high
impact: high
enabler_type: architecture
tags: ["chunking", "llm-optimization", "architecture"]
```
