# EN-007: VTT Parser Implementation

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-01-26T00:00:00Z
> **Due:** TBD
> **Completed:**
> **Parent:** FEAT-002
> **Owner:** Claude
> **Target Sprint:** Sprint 3
> **Effort Points:** 8
> **Gate:** GATE-5 (Core Implementation Review)

---

## Summary

Implement the VTT parser agent that converts WebVTT transcript files into structured data suitable for downstream entity extraction. The parser handles cue parsing, speaker identification heuristics, timestamp normalization, and outputs a clean intermediate format.

**Technical Justification:**
- Foundation for all entity extraction pipelines
- WebVTT is the primary input format (MVP decision)
- Parser must handle speaker identification edge cases
- Output format must be Claude-friendly (<35K tokens per chunk)

---

## Benefit Hypothesis

**We believe that** implementing a robust VTT parser as a prompt-based agent

**Will result in** reliable structured transcript data for downstream processing

**We will know we have succeeded when:**
- Valid VTT files parse without errors
- Speaker turns are correctly identified
- Timestamps are normalized to standard format
- Output chunks respect 35K token limit
- Human approval received at GATE-5

---

## Acceptance Criteria

### Definition of Done

- [ ] VTT parser agent prompt created
- [ ] Speaker identification heuristics implemented
- [ ] Timestamp normalization working
- [ ] Chunking strategy for large files implemented
- [ ] Error handling for malformed VTT
- [ ] Unit tests passing
- [ ] Integration tests with sample VTT files
- [ ] ps-critic review passed
- [ ] Human approval at GATE-5

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Parses standard WebVTT format | [ ] |
| AC-2 | Handles speaker prefixes (e.g., "John:") | [ ] |
| AC-3 | Handles speaker tags (e.g., "<v John>") | [ ] |
| AC-4 | Normalizes timestamps to ISO format | [ ] |
| AC-5 | Handles overlapping cues | [ ] |
| AC-6 | Outputs JSON intermediate format | [ ] |
| AC-7 | Chunks large files at natural boundaries | [ ] |
| AC-8 | Graceful error handling for malformed input | [ ] |

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Owner | Effort | Blocked By |
|----|-------|--------|-------|--------|------------|
| TASK-034 | Create VTT Parser Agent Prompt | pending | Claude | 2 | EN-005 |
| TASK-035 | Implement Speaker Identification Logic | pending | Claude | 2 | TASK-034 |
| TASK-036 | Implement Timestamp Normalization | pending | Claude | 1 | TASK-034 |
| TASK-037 | Implement Chunking Strategy | pending | Claude | 2 | TASK-034 |
| TASK-038 | Create Unit Tests | pending | Claude | 1 | TASK-035..037 |

---

## Technical Design

### Input Format (WebVTT)

```
WEBVTT

00:00:00.000 --> 00:00:05.000
<v John>Hello everyone, welcome to the meeting.

00:00:05.500 --> 00:00:10.000
<v Sarah>Thanks John. Let's get started.
```

### Output Format (JSON)

```json
{
  "metadata": {
    "source_file": "meeting-2026-01-25.vtt",
    "duration_seconds": 3600,
    "speaker_count": 4,
    "cue_count": 245,
    "chunk_index": 0,
    "total_chunks": 3
  },
  "speakers": [
    {"id": "speaker-001", "name": "John", "first_appearance": "00:00:00"},
    {"id": "speaker-002", "name": "Sarah", "first_appearance": "00:00:05"}
  ],
  "cues": [
    {
      "id": "cue-001",
      "start": "00:00:00.000",
      "end": "00:00:05.000",
      "speaker_id": "speaker-001",
      "text": "Hello everyone, welcome to the meeting."
    }
  ]
}
```

### Chunking Strategy

- Target: <30K tokens per chunk (with 5K buffer)
- Split at natural boundaries: silence gaps > 2s, topic changes
- Maintain speaker context across chunks
- Include overlap context (last 3 cues from previous chunk)

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-002: Implementation](../FEAT-002-implementation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | EN-005 | Design documentation required |
| Depends On | ADR-002 | Artifact structure decision |
| Blocks | EN-008 | Entity extraction needs parsed output |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-26 | Claude | pending | Enabler created |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Product Backlog Item (tagged Technical) |
| **SAFe** | Enabler Story |
| **JIRA** | Task |
