# Chunked Processing Protocol -- Code Examples

> Implementation reference for the ts-extractor 4-step chunked processing protocol. Contains Python code examples and detailed YAML specifications for each step. Load as Tier 3 supplementary content when implementing chunk processing.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Step 1: Index Processing Example](#step-1-index-processing-example) | Python code for reading and parsing index.json |
| [Step 2: Strategy Selection Logic](#step-2-strategy-selection-logic) | YAML strategy specs and Python selection code |
| [Step 3: Chunk Processing Loop](#step-3-chunk-processing-loop) | YAML processing spec and Python iteration code |
| [Step 4: Merge Algorithm](#step-4-merge-algorithm) | YAML merge operations and Python merge implementation |

---

## Step 1: Index Processing Example

### Index Fields to Extract

```yaml
action: Read index.json
extracts:
  - total_segments: For progress tracking
  - total_chunks: For iteration planning
  - chunk_size: Batch size (typically 500)
  - speakers:
      list: Initial speaker registry
      segment_counts: Speaker distribution across transcript
  - chunks[]:
      chunk_id: For loading specific chunks
      segment_range: [start, end] segment IDs
      timestamp_range: For temporal correlation
      speaker_counts: Which speakers appear in chunk
      file: Relative path to chunk file
  - topics_preview: Hints for selective loading
```

### Python Example

```python
# Step 1: Read index
index = json.load(input_path / "index.json")

# Extract key metadata
total_segments = index["summary"]["total_segments"]
total_chunks = index["summary"]["total_chunks"]
speakers = index["speakers"]["list"]

print(f"Transcript: {total_segments} segments in {total_chunks} chunks")
print(f"Speakers: {len(speakers)} identified")
```

---

## Step 2: Strategy Selection Logic

### Strategy Specifications

```yaml
action: Determine chunk selection strategy
strategies:
  sequential:
    description: Process all chunks in order
    use_for: [action_items, decisions, questions]
    reason: "These entities can appear anywhere"

  index_only:
    description: Use index metadata without loading chunks
    use_for: [speakers_list, summary_stats]
    reason: "Data available in index"

  selective:
    description: Load only chunks matching criteria
    use_for: [topic_specific, speaker_specific, timeframe]
    reason: "Optimize by targeting relevant chunks"
```

### Python Selection Code

```python
def select_strategy(extraction_task: str, index: dict) -> Strategy:
    if extraction_task in ["action_items", "decisions", "questions"]:
        return Strategy.SEQUENTIAL  # Must scan all

    if extraction_task == "speakers":
        return Strategy.INDEX_ONLY  # Available in index.speakers

    if extraction_task.startswith("topic:"):
        topic = extraction_task.split(":")[1]
        # Use topics_preview to find relevant chunks
        return Strategy.SELECTIVE

    return Strategy.SEQUENTIAL  # Default: safe, complete
```

---

## Step 3: Chunk Processing Loop

### Processing Specification

```yaml
action: Iterate and extract
for_each_chunk:
  1. Load chunk file:
     - Read chunks/chunk-NNN.json
     - Validate schema_version matches

  2. Extract entities:
     - Apply tiered extraction (Tier 1 -> Tier 2 -> Tier 3)
     - Use full segment context within chunk
     - Generate citations with segment_id

  3. Preserve provenance:
     - Record chunk_id in entity metadata
     - Maintain segment_id for citation anchor
     - Track extraction tier and confidence

  4. Memory management:
     - Release chunk from context before loading next
     - Accumulate results in lightweight structures

constraints:
  - Process chunks in order (chunk-001 -> chunk-002 -> ...)
  - Never load multiple chunks simultaneously
  - Preserve navigation context (previous/next awareness)
```

### Python Iteration Code

```python
results = ExtractionResults()

for chunk_meta in index["chunks"]:
    # Load single chunk
    chunk_path = input_path / chunk_meta["file"]
    chunk = json.load(chunk_path)

    # Extract entities from this chunk
    chunk_entities = extract_from_chunk(
        chunk=chunk,
        chunk_id=chunk_meta["chunk_id"],
        speaker_registry=speakers
    )

    # Accumulate results
    results.merge(chunk_entities)

    # Release chunk (allow garbage collection)
    del chunk
```

---

## Step 4: Merge Algorithm

### Merge Operations Specification

```yaml
action: Aggregate and deduplicate
operations:
  speakers:
    - Merge speaker lists from all chunks
    - Calculate total segment_count per speaker
    - Preserve highest confidence detection_pattern

  action_items:
    - Deduplicate by text similarity (>90% match)
    - Keep version with highest confidence
    - Preserve all citations

  decisions:
    - Deduplicate by semantic similarity
    - Link related decisions (same topic)
    - Maintain decision chain context

  questions:
    - Track answered status across chunks
    - Link questions to answers if found
    - Deduplicate exact matches

  topics:
    - Merge topic segments that span chunk boundaries
    - Recalculate topic durations
    - Ensure 100% coverage (no gaps)

  confidence_summary:
    - Recalculate across all extractions
    - Update high/medium/low counts
    - Calculate weighted average

output:
  - Write unified extraction-report.json
  - Include chunk_metadata for traceability
```

### Python Merge Implementation

```python
def merge_results(chunk_results: list[ChunkResults]) -> ExtractionReport:
    merged = ExtractionReport()

    # Aggregate speakers
    speaker_map = {}
    for cr in chunk_results:
        for speaker in cr.speakers:
            if speaker.name in speaker_map:
                speaker_map[speaker.name].segment_count += speaker.segment_count
            else:
                speaker_map[speaker.name] = speaker
    merged.speakers = list(speaker_map.values())

    # Deduplicate action items
    action_map = {}
    for cr in chunk_results:
        for action in cr.action_items:
            key = normalize_text(action.text)
            if key not in action_map or action.confidence > action_map[key].confidence:
                action_map[key] = action
    merged.action_items = list(action_map.values())

    # ... similar for decisions, questions, topics

    return merged
```
