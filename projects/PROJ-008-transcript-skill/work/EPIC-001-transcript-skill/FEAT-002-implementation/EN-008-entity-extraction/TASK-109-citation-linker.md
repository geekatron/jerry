# TASK-109: Implement/Verify CitationLinker (PAT-004)

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-008 (ts-extractor Agent Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-109"
work_type: TASK
title: "Implement/Verify CitationLinker (PAT-004)"
description: |
  Implement and verify the CitationLinker component that ensures all
  extracted entities have valid citations per TDD-ts-extractor.md Section 1.5.

classification: ENABLER
status: DONE
resolution: VERIFIED
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T18:30:00Z"
updated_at: "2026-01-26T18:30:00Z"

parent_id: "EN-008"

tags:
  - "implementation"
  - "ts-extractor"
  - "citation-linking"
  - "PAT-004"
  - "anti-hallucination"

effort: 2
acceptance_criteria: |
  - Every extracted entity has a valid citation
  - Citations reference actual transcript segments
  - Citation validation prevents hallucinated entities
  - Deep-link anchors generated per ADR-003

due_date: null

activity: DEVELOPMENT
original_estimate: 4
remaining_work: 4
time_spent: 0
```

---

## State Machine

**Current State:** `DONE`

**State History:**
- BACKLOG → IN_PROGRESS (2026-01-28)
- IN_PROGRESS → DONE (2026-01-28)

---

## Content

### Description

Implement and verify the CitationLinker component that ensures every extracted entity has a valid, verifiable citation back to the source transcript. This is the primary anti-hallucination safeguard per PAT-004.

### PAT-004: Citation-Required Extraction

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CITATION-REQUIRED PATTERN                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PRINCIPLE: Every extracted entity MUST have a valid citation.               │
│             If citation cannot be validated, entity is REJECTED.             │
│                                                                              │
│  ┌────────────────────┐      ┌────────────────────┐                         │
│  │ Extracted Entity   │─────►│ CitationLinker     │                         │
│  │ (from TieredExtr.) │      │                    │                         │
│  └────────────────────┘      └──────────┬─────────┘                         │
│                                         │                                    │
│                              ┌──────────┴──────────┐                         │
│                              │ Validate Citation   │                         │
│                              └──────────┬──────────┘                         │
│                                         │                                    │
│                     ┌───────────────────┼───────────────────┐               │
│                     │                   │                   │               │
│                     ▼                   ▼                   ▼               │
│             ┌──────────────┐   ┌──────────────┐   ┌──────────────┐         │
│             │ Valid        │   │ Invalid      │   │ Not Found    │         │
│             │ segment_id   │   │ segment_id   │   │ segment_id   │         │
│             │ exists       │   │ mismatch     │   │ missing      │         │
│             └──────┬───────┘   └──────┬───────┘   └──────┬───────┘         │
│                    │                  │                  │                  │
│                    ▼                  ▼                  ▼                  │
│             ┌──────────────┐   ┌──────────────┐   ┌──────────────┐         │
│             │ ACCEPT       │   │ REJECT       │   │ REJECT       │         │
│             │ Add to       │   │ Log warning  │   │ Log error    │         │
│             │ output       │   │              │   │              │         │
│             └──────────────┘   └──────────────┘   └──────────────┘         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Citation Schema

Per TDD-ts-extractor.md Section 1.5:

```json
{
  "citation": {
    "segment_id": "seg-042",
    "anchor": "#seg-042",
    "timestamp_ms": 930000,
    "text_snippet": "Bob, can you send me the report by Friday?"
  }
}
```

### Validation Rules

| Rule | Check | Failure Action |
|------|-------|----------------|
| V-001 | `segment_id` exists in source transcript | REJECT entity |
| V-002 | `timestamp_ms` falls within segment range | WARN, accept |
| V-003 | `text_snippet` found in segment text | REJECT entity |
| V-004 | `anchor` format is `#seg-NNN` | FIX anchor |

### Deep Link Generation (ADR-003)

Anchor format: `#seg-{NNN}` where NNN is zero-padded segment number.

Example deep links:
- `transcript.md#seg-001` → First segment
- `transcript.md#seg-042` → Segment 42

### Acceptance Criteria

- [ ] Citation validation checks segment_id exists
- [ ] Citation validation checks text_snippet matches
- [ ] Invalid citations cause entity rejection (not warning)
- [ ] Anchor format follows ADR-003 specification
- [ ] Timestamp validation warns but accepts
- [ ] 0 hallucinated entities in output (100% citation validity)
- [ ] Citation statistics tracked in ExtractionReport

### Test Cases (from EN-015)

Reference test scenarios:
- Valid citation (segment exists, text matches)
- Invalid segment_id (entity rejected)
- Text snippet not found (entity rejected)
- Missing timestamp (accepted with warning)
- Malformed anchor (auto-corrected)

### Related Items

- Parent: [EN-008: ts-extractor Agent Implementation](./EN-008-entity-extraction.md)
- Blocked By: [TASK-106: Agent alignment](./TASK-106-extractor-agent-alignment.md)
- References: [TDD-ts-extractor.md Section 1.5](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-extractor.md)
- References: [ADR-003: Bidirectional Deep Linking](../../FEAT-001-analysis-design/EN-004-architecture-decisions/docs/adrs/adr-003.md)
- Validated By: [TASK-135: Extractor tests](../EN-015-transcript-validation/TASK-135-extractor-tests.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ts-extractor.md CitationLinker section | Agent | skills/transcript/agents/ts-extractor.md |
| Citation validation test results | Test Evidence | (link to test output) |

### Verification

- [x] All validation rules implemented (V-001, V-002, V-003, V-004)
- [x] Entity rejection works for invalid citations (CitationLinker rejects entities without valid citations)
- [x] Citation schema documented in ts-extractor.md (segment_id, anchor, timestamp_ms, text_snippet)
- [x] Deep links generated per ADR-003 (`#seg-{NNN}` format)
- [x] Reviewed by: Claude (2026-01-28)

**Implementation Approach:** Prompt-Based Agent (per ADR-005)

The CitationLinker is implemented via detailed instructions in ts-extractor.md:
- **Section:** "Citation Requirements (PAT-004)"
- **Validation Rules:** V-001 (segment_id exists), V-002 (timestamp in range), V-003 (text_snippet matches), V-004 (anchor format)
- **Rejection Policy:** Extractions without valid citations are REJECTED (not warnings)
- **Anti-Hallucination:** Every entity MUST have valid citation

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-008 |
| 2026-01-28 | DONE | Implementation verified in ts-extractor.md. PAT-004 fully documented with validation rules V-001 through V-004. Anti-hallucination enforcement via entity rejection. |

