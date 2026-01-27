# TASK-113: Verify ts-formatter Agent Definition Alignment

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-016 (ts-formatter Agent Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-113"
work_type: TASK
title: "Verify ts-formatter Agent Definition Alignment"
description: |
  Verify that the existing ts-formatter.md agent definition aligns with
  the TDD-ts-formatter.md specification and EN-016 requirements.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T18:30:00Z"
updated_at: "2026-01-26T18:30:00Z"

parent_id: "EN-016"

tags:
  - "alignment"
  - "ts-formatter"
  - "verification"

effort: 2
acceptance_criteria: |
  - Agent definition matches TDD-ts-formatter.md interface contracts
  - 8-file packet structure (ADR-002) addressed
  - Token limits (35K) addressed
  - File splitting strategy (ADR-004) referenced
  - Bidirectional linking (ADR-003) referenced
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

Verify that the ts-formatter agent definition (`skills/transcript/agents/ts-formatter.md`) aligns with the Technical Design Document and EN-016 enabler requirements. This is a prerequisite for all subsequent implementation tasks.

### Verification Checklist

| Item | Reference | Agent Section | Status |
|------|-----------|---------------|--------|
| PacketGenerator interface | TDD Section 1 | Capabilities | [ ] |
| TokenCounter interface | TDD Section 4 | Processing | [ ] |
| FileSplitter interface | TDD Section 3 | Processing | [ ] |
| AnchorRegistry interface | TDD Section 2 | Output | [ ] |
| BacklinkInjector interface | TDD Section 5 | Output | [ ] |
| Input schema (CanonicalTranscript + ExtractionReport) | TDD Section 6 | Input | [ ] |
| Output schema (Packet directory) | TDD Section 7 | Output | [ ] |
| Error handling matrix | TDD Section 8 | Error Handling | [ ] |

### TDD Reference Points

From TDD-ts-formatter.md:
- **Section 1:** Packet Structure (FR-013, FR-015)
- **Section 2:** Deep Linking (ADR-003)
- **Section 3:** File Splitting (ADR-004)
- **Section 4:** Token Counting (NFR-009)
- **Section 5:** Backlink Generation (IR-004)

### ADR Compliance Verification

| ADR | Requirement | Agent Implementation | Status |
|-----|-------------|---------------------|--------|
| ADR-002 | 8-file packet structure | PacketGenerator | [ ] |
| ADR-002 | 35K token hard limit | TokenCounter | [ ] |
| ADR-003 | Anchor naming convention | AnchorRegistry | [ ] |
| ADR-003 | Backlinks section | BacklinkInjector | [ ] |
| ADR-004 | Semantic boundary splitting | FileSplitter | [ ] |
| ADR-005 | Phase 3 integration | Pipeline position | [ ] |

### Acceptance Criteria

- [ ] Agent reads CanonicalTranscript + ExtractionReport as input
- [ ] Agent outputs 8-file packet structure
- [ ] Token limits (35K hard, 31.5K soft) defined
- [ ] File splitting uses semantic boundaries
- [ ] Anchor naming convention (seg-, act-, dec-, etc.) defined
- [ ] Backlinks sections included in output files
- [ ] Schema version metadata included
- [ ] Processing time target: <5s for 1-hour transcript

### Related Items

- Parent: [EN-016: ts-formatter Agent Implementation](./EN-016-ts-formatter.md)
- References: [TDD-ts-formatter.md](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-formatter.md)
- Agent: [skills/transcript/agents/ts-formatter.md](../../../../../skills/transcript/agents/ts-formatter.md)
- Blocks: TASK-114, TASK-115, TASK-117

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ts-formatter.md reviewed | Agent | skills/transcript/agents/ts-formatter.md |
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
- [ ] All ADRs (ADR-002, ADR-003, ADR-004) compliance verified
- [ ] Input/output contracts match
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-016 |

