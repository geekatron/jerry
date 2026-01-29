# EN-022: Extractor Adaptation

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-01-28 (FEAT-004 Hybrid Infrastructure)
PURPOSE: Adapt ts-extractor agent to work with chunked input
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Enabler Type:** architecture
> **Created:** 2026-01-28T22:00:00Z
> **Due:** TBD
> **Completed:** -
> **Parent:** FEAT-004
> **Owner:** Claude
> **Effort:** 3

---

## Frontmatter

```yaml
id: "EN-022"
work_type: ENABLER
title: "Extractor Adaptation"
classification: ENABLER
status: pending
priority: medium
impact: medium
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-28T22:00:00Z"
updated_at: "2026-01-28T22:00:00Z"
parent_id: "FEAT-004"
tags: ["enabler", "ts-extractor", "chunking", "adaptation"]
effort: 3
enabler_type: architecture
nfrs: ["NFR-008"]
```

---

## Summary

Adapt the ts-extractor agent definition to work with the chunked input format from EN-021. The agent will read the index file for overview, then request specific chunks for targeted extraction, improving accuracy and reducing token usage.

**Technical Value:**
- Agent works with chunked input
- Selective chunk loading reduces costs
- Improved accuracy through focused context
- Citation preservation across chunks

---

## Problem Statement

The current ts-extractor agent expects a single canonical-transcript.json file. With the chunked format from EN-021, the agent needs to:

1. **Read index.json first** - Understand transcript overview
2. **Decide which chunks to load** - Based on extraction task
3. **Process chunks sequentially or selectively** - Depending on task type
4. **Merge results** - Combine extractions from multiple chunks

---

## Technical Approach

### Workflow Update

```
CURRENT:
ts-extractor reads canonical-transcript.json (entire file)
                    ↓
            Extract all entities

UPDATED:
ts-extractor reads index.json (small, metadata only)
                    ↓
            Identifies relevant chunks based on task
                    ↓
            Reads specific chunk files
                    ↓
            Extracts entities from focused context
                    ↓
            Merges results with citation preservation
```

### Agent Definition Updates

Update `ts-extractor.md` with new input handling:

```markdown
## Input Formats

### Format A: Single File (Legacy)
- File: `canonical-transcript.json`
- Use: Small transcripts (< 1000 segments)

### Format B: Chunked (Recommended)
- Index: `index.json` - Read first for overview
- Chunks: `chunks/chunk-NNN.json` - Load as needed

## Chunked Processing Protocol

1. **Read Index**
   - Load `index.json`
   - Note: total_segments, speaker_counts, chunk_metadata

2. **Plan Extraction**
   - For action items: Process all chunks sequentially
   - For speaker-specific: Load chunks with that speaker
   - For topic-specific: Use topics_preview to select chunks

3. **Process Chunks**
   - Load one chunk at a time
   - Extract entities with full segment context
   - Preserve segment_id for citation

4. **Merge Results**
   - Combine entities from all processed chunks
   - Deduplicate if necessary
   - Maintain citation references
```

### Chunk Selection Logic

```yaml
# Task-based chunk selection

action_items:
  strategy: sequential
  reason: "Action items can appear anywhere"

decisions:
  strategy: sequential
  reason: "Decisions can appear anywhere"

questions:
  strategy: sequential
  reason: "Questions appear throughout"

speakers:
  strategy: index_only
  reason: "Speaker counts available in index"

topics:
  strategy: selective
  selection_criteria: "Use topics_preview from index"
```

---

## NFRs Addressed

| NFR | Requirement | How Addressed |
|-----|-------------|---------------|
| NFR-008 | Confidence scoring | Maintained in chunked mode |
| PAT-004 | Citation required | Segment IDs preserved |

---

## Children (Tasks)

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| TASK-220 | Update ts-extractor.md input section | pending | high |
| TASK-221 | Add chunked processing protocol | pending | high |
| TASK-222 | Document chunk selection strategies | pending | medium |
| TASK-223 | Update extraction-report schema | pending | medium |

**Note:** Task IDs renumbered from TASK-170-173 to TASK-220-223 per DEC-010 (FEAT-004 task range allocation).

---

## Acceptance Criteria

### Definition of Done

- [ ] ts-extractor.md updated with chunked input support
- [ ] Chunk selection strategies documented
- [ ] extraction-report.json schema updated if needed
- [ ] Manual test with meeting-006 chunked output

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Agent reads index.json first | [ ] |
| AC-2 | Agent loads chunks selectively | [ ] |
| AC-3 | Citations reference segment IDs correctly | [ ] |
| AC-4 | Extraction report matches single-file quality | [ ] |

---

## Dependencies

| Type | Item | Description |
|------|------|-------------|
| Depends On | EN-021 | Requires chunked output format |
| Related | ts-extractor.md | Agent definition to update |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-28 | Claude | pending | Enabler created from DISC-009 |

---

## Metadata

```yaml
id: "EN-022"
parent_id: "FEAT-004"
work_type: ENABLER
title: "Extractor Adaptation"
status: pending
priority: medium
impact: medium
enabler_type: architecture
tags: ["ts-extractor", "chunking", "adaptation"]
```
