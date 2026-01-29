# FEAT-004: Hybrid Parsing Infrastructure

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
CREATED: 2026-01-28 (DISC-009 corrective action)
PURPOSE: Implement hybrid Python + LLM architecture for transcript processing
-->

> **Type:** feature
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-01-28T22:00:00Z
> **Due:** TBD
> **Completed:** -
> **Parent:** EPIC-001
> **Owner:** Claude
> **Target Sprint:** TBD

---

## Summary

Implement a hybrid architecture for transcript processing that combines deterministic Python parsing with semantic LLM extraction. This feature addresses the gap identified in DISC-009 where agent-only architecture cannot reliably process large transcript files (90K+ tokens).

**Value Proposition:**
- 1,250x cost reduction for parsing operations
- Sub-second parsing vs. minutes with pure LLM
- 100% parsing accuracy (deterministic vs. LLM hallucination risk)
- Testable, maintainable parsing layer

---

## Benefit Hypothesis

**We believe that** implementing a hybrid architecture with Python parsing and LLM semantic extraction

**Will result in:**
- Complete, accurate parsing of any size transcript
- Significant cost reduction (90%+ on token usage)
- Faster end-to-end processing
- Testable, reliable pipeline

**We will know we have succeeded when:**
- meeting-006-all-hands.vtt (90K tokens) processes completely without truncation
- Unit test coverage for parser reaches 90%+
- ps-critic quality score remains >= 0.90
- Processing time < 30 seconds for 5-hour transcripts

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        HYBRID TRANSCRIPT PROCESSING                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────────────────┐                                                        │
│  │  INPUT: VTT/SRT/TXT │                                                        │
│  └──────────┬──────────┘                                                        │
│             │                                                                    │
│             ▼                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                    LAYER 1: PYTHON PARSING (EN-020)                      │   │
│  │  ┌───────────────────────────────────────────────────────────────────┐  │   │
│  │  │  webvtt-py + custom logic                                          │  │   │
│  │  │  - Deterministic VTT/SRT/TXT parsing                               │  │   │
│  │  │  - Voice tag extraction                                             │  │   │
│  │  │  - Timestamp normalization                                          │  │   │
│  │  │  - Encoding detection (UTF-8, Windows-1252, ISO-8859-1)            │  │   │
│  │  └───────────────────────────────────────────────────────────────────┘  │   │
│  └──────────┬──────────────────────────────────────────────────────────────┘   │
│             │                                                                    │
│             ▼                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                    LAYER 2: CHUNKING (EN-021)                            │   │
│  │  ┌───────────────────────────────────────────────────────────────────┐  │   │
│  │  │  Index + Chunk Strategy (Option D)                                  │  │   │
│  │  │  - index.json: Metadata, speaker counts, chunk pointers            │  │   │
│  │  │  - chunks/chunk-NNN.json: 500-segment chunks                        │  │   │
│  │  │  - Enables LLM to request specific segments                         │  │   │
│  │  └───────────────────────────────────────────────────────────────────┘  │   │
│  └──────────┬──────────────────────────────────────────────────────────────┘   │
│             │                                                                    │
│             ▼                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                    LAYER 3: LLM EXTRACTION (EN-022)                      │   │
│  │  ┌───────────────────────────────────────────────────────────────────┐  │   │
│  │  │  ts-extractor agent (existing)                                      │  │   │
│  │  │  - Reads index.json for overview                                    │  │   │
│  │  │  - Requests relevant chunks based on task                           │  │   │
│  │  │  - Semantic entity extraction (actions, decisions, questions)       │  │   │
│  │  │  - Confidence scoring with citation                                  │  │   │
│  │  └───────────────────────────────────────────────────────────────────┘  │   │
│  └──────────┬──────────────────────────────────────────────────────────────┘   │
│             │                                                                    │
│             ▼                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                    OUTPUT: extraction-report.json                        │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

LEGEND:
├─ Python Layer: Deterministic, testable, fast
├─ Chunking Layer: Optimizes LLM context usage
└─ LLM Layer: Semantic understanding, entity extraction
```

---

## Acceptance Criteria

### Definition of Done

- [ ] Python parser successfully parses all test VTT files
- [ ] Chunking strategy produces index + chunk files
- [ ] LLM extractor can request and process specific chunks
- [ ] Unit test coverage >= 90% for Python layer
- [ ] Integration tests pass for full pipeline
- [ ] ps-critic quality score >= 0.90

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Python parser parses meeting-006-all-hands.vtt (3,071 segments) completely | [ ] |
| AC-2 | Chunking produces index.json with correct metadata | [ ] |
| AC-3 | Chunk files contain <= 500 segments each | [ ] |
| AC-4 | ts-extractor can process chunked input | [ ] |
| AC-5 | End-to-end pipeline produces complete extraction-report.json | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Parse time < 5 seconds for 5-hour transcript | [ ] |
| NFC-2 | Memory usage < 100MB during parsing | [ ] |
| NFC-3 | No external network dependencies (offline capable) | [ ] |
| NFC-4 | Works with Python 3.10+ | [ ] |

---

## MVP Definition

### In Scope (MVP)

- VTT format parsing with webvtt-py
- Basic chunking strategy (fixed 500-segment chunks)
- Index file generation
- ts-extractor adaptation for chunked input

### Out of Scope (Future)

- SRT format parsing (Phase 2)
- Plain text parsing (Phase 2)
- Semantic boundary chunking (Phase 2)
- Parallel chunk processing (Phase 3)
- Jerry CLI integration (North star)

---

## Children (Stories/Enablers)

### Story/Enabler Inventory

| ID | Type | Title | Status | Priority | Dependencies |
|----|------|-------|--------|----------|--------------|
| EN-020 | Enabler | Python Parser Implementation | pending | high | - |
| EN-021 | Enabler | Chunking Strategy | pending | high | EN-020 |
| EN-022 | Enabler | Extractor Adaptation | pending | medium | EN-021 |
| EN-023 | Enabler | Integration Testing | pending | medium | EN-020, EN-021, EN-022 |

### Work Item Links

- [EN-020: Python Parser Implementation](./EN-020-python-parser/EN-020-python-parser.md)
- [EN-021: Chunking Strategy](./EN-021-chunking-strategy/EN-021-chunking-strategy.md)
- [EN-022: Extractor Adaptation](./EN-022-extractor-adaptation/EN-022-extractor-adaptation.md)
- [EN-023: Integration Testing](./EN-023-integration-testing/EN-023-integration-testing.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Enablers:  [....................] 0% (0/4 completed)              |
| Tasks:     [....................] 0% (0/TBD completed)            |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                              |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Enablers** | 4 |
| **Completed Enablers** | 0 |
| **Total Tasks** | TBD |
| **Completed Tasks** | 0 |
| **Completion %** | 0% |

---

## Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | DISC-009 | Architecture gap analysis (COMPLETE) |
| Informs | FEAT-002 | Implementation feature (amends agent-only design) |
| Informs | ADR-001 | Agent architecture (requires amendment) |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001: Transcript Skill](../EPIC-001-transcript-skill.md)

### Related Features

- [FEAT-002: Implementation](../FEAT-002-implementation/FEAT-002-implementation.md) - Original implementation feature

### Related Discoveries

- [DISC-009: Agent-Only Architecture Limitation](../FEAT-002-implementation/FEAT-002--DISC-009-agent-only-architecture-limitation.md) - Root cause analysis

### Related ADRs

- [ADR-001: Agent Architecture](../../../docs/adrs/adr-001.md) - Requires amendment

---

## Technical Notes

### Python Library Selection

**webvtt-py** selected based on DISC-009 research:
- MIT License
- Active maintenance (v0.5.1)
- VTT and SRT support
- Clean Python API
- HLS segmentation capability

```python
import webvtt

for caption in webvtt.read('captions.vtt'):
    print(caption.start, caption.end, caption.text)
```

### File Location

**Short-term:** `skills/transcript/src/`
**North star:** Jerry CLI integration

### Chunk Size Rationale

500 segments per chunk based on:
- LangChain recommendation: 1000-2000 tokens with 200 overlap
- Average segment: 15-30 words = 20-40 tokens
- 500 segments ≈ 10,000-20,000 tokens
- Well under 31.5K soft limit from ADR-004

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-28 | Claude | pending | Feature created from DISC-009 findings |

---

## Metadata

```yaml
id: "FEAT-004"
parent_id: "EPIC-001"
work_type: FEATURE
title: "Hybrid Parsing Infrastructure"
status: pending
priority: high
impact: high
created_by: "Claude"
created_at: "2026-01-28T22:00:00Z"
updated_at: "2026-01-28T22:00:00Z"
tags: ["hybrid-architecture", "python-parsing", "chunking", "webvtt-py"]
```

---

<!--
DESIGN RATIONALE:

This feature implements the hybrid architecture recommended in DISC-009.
The design separates deterministic parsing (Python) from semantic extraction (LLM)
following industry best practices.

Key decisions:
1. webvtt-py for VTT parsing - established library, MIT license
2. 500-segment chunks - balanced for context efficiency
3. Index + chunks pattern - enables selective LLM access
4. Short-term in skills/transcript/src/ - eventual Jerry CLI migration

Evidence base:
- RAG 1,250x cost efficiency (Meilisearch)
- 60% production LLM apps use hybrid/RAG (byteiota)
- Lost-in-Middle accuracy degradation (Stanford)

TRACE:
- DISC-009: Root cause analysis and recommendation
- FEAT-002: Original implementation (amended)
- ADR-001: Agent architecture (requires amendment)
-->
