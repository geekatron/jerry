# TASK-131A: Human-Annotate User VTT Files for Ground Truth

<!--
TEMPLATE: Task
VERSION: 2.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
CREATED: 2026-01-27 per TDD/BDD Testing Strategy
-->

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-01-27T00:00:00Z
> **Parent:** EN-015
> **Owner:** Human Expert
> **Effort Points:** 3
> **Blocked By:** User VTT Files

---

## Summary

Create **ground truth expected.json files** from user-provided VTT files via **human expert annotation**. This is a critical TDD/BDD prerequisite that ensures we do NOT "dog food" (test with agent output).

**Why Human-in-Loop?**

| Approach | Problem | Risk |
|----------|---------|------|
| Agent-Generated Ground Truth | Circular validation | 100% false positive rate |
| Automated Extraction | No external oracle | Same as agent |
| **Human-in-Loop** | Expert validates/creates | Gold standard accuracy |

---

## Acceptance Criteria

### Definition of Done

- [ ] User provides 2-3 real VTT files from actual meetings
- [ ] Human expert manually reads each VTT file
- [ ] For each VTT file, human annotates:
  - [ ] Action Items (who, what, when, source timestamp)
  - [ ] Decisions (what, decided by, rationale, source timestamp)
  - [ ] Questions (asked by, answered?, answer reference, source timestamp)
  - [ ] Speakers (names, speaking segments)
  - [ ] Topics (boundaries, hierarchy)
- [ ] expected.json files created for each VTT file
- [ ] expected.json follows the ExtractionReport schema
- [ ] All annotated entities have citations per PAT-004

### Technical Criteria

| # | Criterion | Source | Verified |
|---|-----------|--------|----------|
| AC-1 | Minimum 2 VTT files annotated | TDD/BDD Strategy | [ ] |
| AC-2 | Each annotation has source timestamp citation | PAT-004 | [ ] |
| AC-3 | expected.json validates against ExtractionReport schema | TDD-ts-extractor | [ ] |
| AC-4 | Annotation follows confidence guidelines | TDD/BDD Strategy | [ ] |

---

## Annotation Guidelines

### Action Item Signals

| Signal | Confidence | Example |
|--------|------------|---------|
| "I will...", "I'll..." | HIGH (0.95) | "I'll send the report by Friday" |
| "Can you...", "Would you..." | HIGH (0.90) | "Can you review the PR?" |
| "Need to...", "Should..." | MEDIUM (0.75) | "We need to fix the bug" |
| "TODO:", "ACTION:" | HIGH (0.95) | "ACTION: Update docs" |

### Decision Signals

| Signal | Confidence | Example |
|--------|------------|---------|
| "We've decided...", "Decision:" | HIGH (0.95) | "We've decided to use React" |
| "Let's go with...", "Agreed:" | HIGH (0.90) | "Let's go with option B" |
| "So we'll..." (consensus) | MEDIUM (0.80) | "So we'll deploy Monday" |

### Citation Format

Every entity MUST have a citation:

```json
{
  "id": "act-001",
  "text": "Send report by Friday",
  "assignee": "Bob",
  "citation": {
    "segment_id": "seg-042",
    "timestamp_ms": 930000,
    "text_snippet": "Bob, can you send me the report by Friday?"
  }
}
```

---

## Deliverables

| Deliverable | Path | Description |
|-------------|------|-------------|
| User VTT Files | `test_data/transcripts/user/` | User-provided meeting recordings |
| expected.json | `test_data/transcripts/user/meeting-*.expected.json` | Human-annotated ground truth |
| Annotation Notes | `test_data/transcripts/user/README.md` | Documentation of annotation decisions |

---

## Evidence Requirements

To close this task, provide:

1. **User VTT Files:** Screenshots or file listings showing user-provided VTT files
2. **Annotation Process:** Documentation of human annotation process
3. **expected.json Validation:** Schema validation output showing compliance
4. **Citation Coverage:** Report showing all entities have citations

---

## Related Items

- **Parent Enabler:** [EN-015](./EN-015-transcript-validation.md)
- **Strategy Document:** [TDD/BDD Testing Strategy](../docs/analysis/tdd-bdd-testing-strategy.md)
- **Depends On:** User provides VTT files
- **Blocks:** TASK-132 (ground truth JSON), E2E tests

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-27 | Claude | pending | Task created per TDD/BDD Testing Strategy |
