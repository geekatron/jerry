# TASK-106: Verify ts-extractor Agent Definition Alignment

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-008 (ts-extractor Agent Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-106"
work_type: TASK
title: "Verify ts-extractor Agent Definition Alignment"
description: |
  Verify that the existing ts-extractor.md agent definition aligns with
  the TDD-ts-extractor.md specification and EN-008 requirements.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T18:30:00Z"
updated_at: "2026-01-26T18:30:00Z"

parent_id: "EN-008"

tags:
  - "alignment"
  - "ts-extractor"
  - "verification"

effort: 2
acceptance_criteria: |
  - Agent definition matches TDD-ts-extractor.md interface contracts
  - All 4 entity types (action items, decisions, questions, topics) addressed
  - PAT-001 (Tiered Extraction) referenced correctly
  - PAT-003 (Speaker Detection) referenced correctly
  - PAT-004 (Citation-Required) referenced correctly
  - Input/output schemas match TDD specification

due_date: null

activity: ANALYSIS
original_estimate: 4
remaining_work: 4
time_spent: 0
```

---

## State Machine

**Current State:** `BACKLOG`

---

## Content

### Description

Verify that the ts-extractor agent definition (`skills/transcript/agents/ts-extractor.md`) aligns with the Technical Design Document and EN-008 enabler requirements. This is a prerequisite for all subsequent implementation tasks.

### Verification Checklist

| Item | Reference | Agent Section | Status |
|------|-----------|---------------|--------|
| SpeakerIdentifier interface | TDD Section 3 | Capabilities | [ ] |
| TieredExtractor interface | TDD Section 2 | Processing | [ ] |
| CitationLinker interface | TDD Section 1.5 | Output | [ ] |
| TopicSegmenter interface | TDD Section 1.4 | Output | [ ] |
| Input schema (CanonicalTranscript) | TDD Section 5.1 | Input | [ ] |
| Output schema (ExtractionReport) | TDD Section 5.2 | Output | [ ] |
| Confidence scoring (NFR-008) | TDD Section 4 | Behavior | [ ] |
| Error handling matrix | TDD Section 8 | Error Handling | [ ] |

### TDD Reference Points

From TDD-ts-extractor.md:
- **Section 1:** Entity Extraction (FR-006, FR-007, FR-008, FR-009)
- **Section 2:** Tiered Extraction Pipeline (PAT-001)
- **Section 3:** Speaker Identification (PAT-003)
- **Section 4:** Confidence Scoring (NFR-008)
- **Section 5:** Interface Definitions

### Acceptance Criteria

- [ ] Agent reads CanonicalTranscript JSON as input
- [ ] Agent outputs ExtractionReport JSON
- [ ] SpeakerIdentifier uses 4-pattern chain (VTT → Prefix → Bracket → Context)
- [ ] TieredExtractor uses Rule → ML → LLM fallback
- [ ] CitationLinker validates all citations exist
- [ ] TopicSegmenter detects boundaries
- [ ] Confidence thresholds defined: HIGH(≥0.85), MEDIUM(0.70-0.85), LOW(<0.70)
- [ ] Processing time target: <30s for 1-hour transcript

### Related Items

- Parent: [EN-008: ts-extractor Agent Implementation](./EN-008-entity-extraction.md)
- References: [TDD-ts-extractor.md](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-extractor.md)
- Agent: [skills/transcript/agents/ts-extractor.md](../../../../../skills/transcript/agents/ts-extractor.md)
- Blocks: TASK-107, TASK-108, TASK-109, TASK-110

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ts-extractor.md reviewed | Agent | skills/transcript/agents/ts-extractor.md |
| Alignment report | Analysis | (in this file) |

### Alignment Report

```
[To be filled during task execution]

Section | TDD Reference | Agent Reference | Aligned? | Notes
--------|---------------|-----------------|----------|------
(complete verification table here)
```

### Verification

- [ ] All TDD sections mapped to agent sections
- [ ] All patterns (PAT-001, PAT-003, PAT-004) documented
- [ ] Input/output contracts match
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-008 |

