# ts-parser Output Schema Reference

> Canonical Transcript JSON Schema (v1.1) and output directory structure.
> Defines the contract between ts-parser and downstream agents (ts-extractor).

---

## Canonical Transcript JSON Schema (v1.1)

```json
{
  "version": "1.1",
  "source": {
    "format": "vtt|srt|plain",
    "encoding": "utf-8",
    "file_path": "/path/to/original/file"
  },
  "metadata": {
    "duration_ms": 3600000,
    "segment_count": 150,
    "detected_speakers": 4
  },
  "segments": [
    {
      "id": "seg-001",
      "start_ms": 0,
      "end_ms": 5000,
      "speaker": "Alice",
      "text": "Good morning everyone.",
      "raw_text": "<v Alice>Good morning everyone."
    }
  ],
  "parse_metadata": {
    "parse_status": "complete",
    "parse_warnings": [],
    "parse_errors": [],
    "skipped_segments": []
  }
}
```

**Segment ID Format:** `seg-{NNN}` where NNN is zero-padded sequence number

**Mandatory Fields:**
- `id`: Always generated
- `text`: Always present (may be empty string)

**Optional Fields:**
- `start_ms`, `end_ms`: null for plain text
- `speaker`: null if not detected
- `raw_text`: Original unparsed line (for debugging)

## Output Directory Structure (v2.0)

```
{output_path}/
├── canonical-transcript.json  # Full parsed transcript (legacy compatibility)
├── index.json                 # Chunk index with metadata (NEW)
│   ├── total_segments: 3071
│   ├── chunk_count: 7
│   ├── chunk_size: 500
│   └── chunks: [{file, start_seg, end_seg, speaker_summary}]
└── chunks/                    # Chunked segments (NEW)
    ├── chunk-000.json         # Segments 0-499
    ├── chunk-001.json         # Segments 500-999
    └── ...
```

## Validation Checks

```yaml
Required Fields:
  - version: string (e.g., "1.1")
  - source:
      format: "vtt" | "srt" | "plain"
      file_path: string
  - metadata:
      segment_count: integer > 0
  - segments: array (length > 0)
      - each segment must have:
          - id: string (seg-NNN)
          - text: string

Validation Checks:
  - [ ] segments array is non-empty
  - [ ] segment_count matches len(segments)
  - [ ] all segments have required fields
  - [ ] no duplicate segment IDs
```

## State Management Key

**Output Key:** `ts_parser_output`

```yaml
ts_parser_output:
  packet_id: "{packet_id}"
  canonical_json_path: "{output_path}/canonical-transcript.json"
  index_json_path: "{output_path}/index.json"
  chunks_dir: "{output_path}/chunks/"
  chunk_count: {integer}
  format_detected: "vtt|srt|plain"
  parsing_method: "python|llm"
  segment_count: {integer}
  speaker_count: {integer}
  duration_ms: {integer|null}
  warnings: []
  validation_passed: {boolean}
  next_agent: "ts-extractor"
```
