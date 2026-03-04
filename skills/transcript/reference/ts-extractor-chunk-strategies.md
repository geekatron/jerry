# Chunk Selection Strategies Reference

> Detailed reference for chunk selection strategies used in Step 2 of the ts-extractor Chunked Processing Protocol. Loaded as Tier 3 supplementary content when selective or optimized chunk loading is needed.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Strategy Definitions](#strategy-definitions) | Summary table of all strategies |
| [Strategy 1: Sequential](#strategy-1-sequential-process-all-chunks) | Process all chunks in order |
| [Strategy 2: Index Only](#strategy-2-index-only-no-chunk-loading) | Extract from index metadata only |
| [Strategy 3: Selective](#strategy-3-selective-load-matching-chunks) | Load only relevant chunks |
| [Task-to-Strategy Mapping](#task-to-strategy-mapping) | Which strategy for which task |
| [Strategy Decision Flowchart](#strategy-decision-flowchart) | Visual decision aid |

---

## Strategy Definitions

| Strategy | Cost | Accuracy | When to Use |
|----------|------|----------|-------------|
| **Sequential** | High (all chunks) | Highest | Entities distributed throughout transcript |
| **Index Only** | Minimal | Full for aggregates | Data available in index metadata |
| **Selective** | Variable | High for scope | Targeted extraction with index hints |

## Strategy 1: Sequential (Process All Chunks)

**Description:** Process every chunk in order from chunk-001 to chunk-NNN.

**Cost Analysis:**
- Token usage: O(total_segments)
- API calls: O(total_chunks)
- Processing time: Linear with transcript size

**When to Use:**
```yaml
applicable_tasks:
  - action_items: "Can appear in any segment"
  - decisions: "Context-dependent, distributed"
  - questions: "May occur throughout meeting"
  - full_extraction: "Complete entity scan required"

rationale: |
  Action items, decisions, and questions have no predictable
  location in a transcript. A speaker might commit to an action
  at minute 5 or minute 55. Sequential processing ensures
  100% recall at the cost of processing all content.
```

## Strategy 2: Index Only (No Chunk Loading)

**Description:** Extract information solely from index.json metadata without loading any chunks.

**Cost Analysis:**
- Token usage: ~500 tokens (index only)
- API calls: 1
- Processing time: Constant O(1)

**When to Use:**
```yaml
applicable_tasks:
  - speakers_list: "Available in index.speakers.list"
  - speaker_counts: "Available in index.speakers.segment_counts"
  - transcript_stats: "total_segments, duration_ms, word_count"
  - chunk_overview: "chunks[].timestamp_range, speaker_counts"

rationale: |
  The index file contains pre-computed aggregates for speakers,
  segment counts, and duration. If the extraction task only
  needs this metadata, loading chunks is wasteful.

example_queries:
  - "Who were the speakers in this meeting?"
  - "How long was the transcript?"
  - "How many segments per speaker?"
```

## Strategy 3: Selective (Load Matching Chunks)

**Description:** Use index metadata to identify and load only relevant chunks.

**Cost Analysis:**
- Token usage: O(matching_chunks x chunk_size)
- API calls: O(matching_chunks)
- Processing time: Proportional to selection hit rate

**Selection Criteria:**
```yaml
by_topic:
  method: Use topics_preview from index
  example: "Extract decisions about 'Q4 Budget'"
  selection: Load chunks covering the budget topic

by_speaker:
  method: Use chunks[].speaker_counts from index
  example: "What did Alice commit to?"
  selection: Load chunks where Alice has segments

by_timeframe:
  method: Use chunks[].timestamp_range from index
  example: "Actions from the last 30 minutes"
  selection: Load chunks in time window

by_segment_range:
  method: Use chunks[].segment_range from index
  example: "Focus on segments 1000-1500"
  selection: Load chunk-003 (1001-1500)
```

**When to Use:**
```yaml
applicable_tasks:
  - topic_specific: "User asks about specific topic"
  - speaker_specific: "User asks about specific speaker"
  - timeframe_query: "User asks about specific time window"
  - follow_up: "Drill down from previous extraction"

rationale: |
  When the user's query has constraints (topic, speaker, time),
  loading all chunks is wasteful. The index provides enough
  metadata to identify which chunks are relevant.
```

## Task-to-Strategy Mapping

| Extraction Task | Recommended Strategy | Rationale |
|-----------------|---------------------|-----------|
| `extract_all` | Sequential | Complete extraction required |
| `action_items` | Sequential | Distributed throughout |
| `decisions` | Sequential | Context-dependent |
| `questions` | Sequential | May occur anywhere |
| `speakers` | Index Only | Available in index.speakers |
| `summary_stats` | Index Only | Pre-computed in index |
| `topic:{name}` | Selective | Use topics_preview |
| `speaker:{name}` | Selective | Use speaker_counts |
| `time:{start}-{end}` | Selective | Use timestamp_range |
| `segment:{start}-{end}` | Selective | Use segment_range |

## Strategy Decision Flowchart

```
                     +-------------------------+
                     |   What data is needed?  |
                     +-----------+-------------+
                                 |
              +------------------+------------------+
              |                  |                  |
              v                  v                  v
     +----------------+  +-----------------+  +-----------------+
     | Full entity    |  | Aggregate/      |  | Scoped query    |
     | extraction?    |  | metadata only?  |  | (topic/speaker/ |
     |                |  |                 |  |  timeframe)?    |
     +-------+--------+  +-------+---------+  +-------+---------+
             |                   |                    |
             v                   v                    v
      ===============     ===============     ===============
      | SEQUENTIAL  |     | INDEX ONLY  |     |  SELECTIVE  |
      ===============     ===============     ===============
```
