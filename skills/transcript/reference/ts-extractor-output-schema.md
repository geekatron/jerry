# ts-extractor Output Schema Reference

> Complete JSON schema, field reference, and backward compatibility rules for the extraction report produced by ts-extractor. Version 1.1 (chunked input support).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Extraction Report JSON Schema](#extraction-report-json-schema) | Full example with all fields |
| [Schema Field Reference](#schema-field-reference) | Field-by-field documentation |
| [Backward Compatibility](#backward-compatibility) | Legacy single_file format rules |

---

## Extraction Report JSON Schema

**Version:** 1.1 (updated for chunked input support)

```json
{
  "version": "1.1",
  "packet_id": "transcript-meeting-20260126-001",
  "input_format": "chunked",
  "chunk_metadata": {
    "index_path": "index.json",
    "chunks_processed": 7,
    "chunks_total": 7,
    "selection_strategy": "sequential",
    "chunks": [
      {
        "chunk_id": "chunk-001",
        "segment_range": [1, 500],
        "entities_extracted": 5
      },
      {
        "chunk_id": "chunk-002",
        "segment_range": [501, 1000],
        "entities_extracted": 3
      }
    ]
  },
  "extraction_stats": {
    "speakers_identified": 4,
    "action_items": 5,
    "decisions": 3,
    "questions": 7,
    "topics": 4,
    "confidence_summary": {
      "average": 0.87,
      "high_count": 12,
      "medium_count": 5,
      "low_count": 2,
      "high_ratio": 0.63
    }
  },
  "speakers": [
    {
      "id": "spk-alice",
      "name": "Alice",
      "detection_pattern": "vtt_voice_tag",
      "confidence": 0.95,
      "segment_count": 45
    }
  ],
  "action_items": [
    {
      "id": "act-001",
      "text": "Send the report",
      "assignee": "Bob",
      "due_date": "2026-01-31",
      "confidence": 0.92,
      "tier": 1,
      "citation": {
        "segment_id": "seg-042",
        "chunk_id": "chunk-001",
        "anchor": "#seg-042",
        "timestamp_ms": 930000,
        "text_snippet": "Bob, can you send me the report by Friday?"
      }
    }
  ],
  "decisions": [
    {
      "id": "dec-001",
      "text": "Go with Option B for the launch",
      "decided_by": "Manager",
      "confidence": 0.95,
      "citation": {
        "segment_id": "seg-078",
        "chunk_id": "chunk-002",
        "anchor": "#seg-078",
        "timestamp_ms": 1560000,
        "text_snippet": "Let's go with Option B for the launch"
      }
    }
  ],
  "questions": [
    {
      "id": "que-001",
      "text": "How are we handling authentication?",
      "asked_by": "Dev",
      "answered": false,
      "confidence": 0.95,
      "citation": {
        "segment_id": "seg-025",
        "chunk_id": "chunk-001",
        "anchor": "#seg-025",
        "timestamp_ms": 520000,
        "text_snippet": "How are we handling authentication?"
      }
    }
  ],
  "topics": [
    {
      "id": "top-001",
      "title": "Project Status Update",
      "start_ms": 0,
      "end_ms": 600000,
      "segment_ids": ["seg-001", "seg-002"],
      "chunk_ids": ["chunk-001"]
    }
  ]
}
```

**Invariant:** Every count in `extraction_stats` MUST equal the length of the corresponding array (INV-EXT-001).

---

## Schema Field Reference

### Input Format Fields (v1.1)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `input_format` | string | Yes | `"single_file"` or `"chunked"` |
| `chunk_metadata` | object | Conditional | Required when `input_format` = `"chunked"`, null/omitted for single_file |

### chunk_metadata Object

| Field | Type | Description |
|-------|------|-------------|
| `index_path` | string | Path to index.json used |
| `chunks_processed` | integer | Number of chunks actually processed |
| `chunks_total` | integer | Total chunks in index |
| `selection_strategy` | string | `"sequential"`, `"index_only"`, or `"selective"` |
| `chunks[]` | array | Per-chunk extraction details |
| `chunks[].chunk_id` | string | Chunk identifier (e.g., "chunk-001") |
| `chunks[].segment_range` | [int, int] | Segment ID range in this chunk |
| `chunks[].entities_extracted` | integer | Entity count from this chunk |

### Citation Schema (Updated)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `segment_id` | string | Yes | Source segment ID |
| `chunk_id` | string | Conditional | Chunk source (present only for chunked input) |
| `anchor` | string | Yes | Navigation anchor |
| `timestamp_ms` | integer | Yes | Timestamp in milliseconds |
| `text_snippet` | string | Yes | Relevant quote |

---

## Backward Compatibility

For **single_file** input format (legacy):

```json
{
  "version": "1.1",
  "packet_id": "transcript-small-meeting",
  "input_format": "single_file",
  "extraction_stats": { "..." : "..." },
  "action_items": [
    {
      "id": "act-001",
      "citation": {
        "segment_id": "seg-042",
        "anchor": "#seg-042",
        "timestamp_ms": 930000,
        "text_snippet": "..."
      }
    }
  ]
}
```

**Backward Compatibility Rules:**
- `chunk_metadata` is **omitted** (not null) for single_file format
- `citation.chunk_id` is **omitted** for single_file format
- All other fields remain unchanged from v1.0
- Consumers should check `input_format` before accessing chunk-specific fields
