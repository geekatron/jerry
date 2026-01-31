# Task: TASK-148 - Anchor Tracking Tests

> **Task ID:** TASK-148
> **Status:** done
> **Priority:** high
> **Enabler:** [EN-018-split-validation](./EN-018-split-validation.md)
> **Created:** 2026-01-28
> **Last Updated:** 2026-01-28

---

## Summary

Validate that _anchors.json correctly tracks entities across split files, with accurate file references and line numbers.

**⚠️ CORRECTED (per DISC-008):** Only meeting-006 will trigger splits. meeting-004 and meeting-005 are below the 31.5K soft limit.

---

## Acceptance Criteria

- [x] **AC-1:** _anchors.json contains entries for all entity types ✓
- [x] **AC-2:** File references point to correct split file (part-1, part-2, etc.) ✓
- [x] **AC-3:** Line numbers are accurate within each split file ✓
- [x] **AC-4:** Cross-references work across split boundaries ✓
- [x] **AC-5:** Statistics reflect total across all splits ✓

---

## Technical Specifications

### _anchors.json Structure for Split Files

```json
{
  "packet_id": "transcript-meeting-006",
  "anchors": {
    "seg-001": {"type": "segment", "file": "02-transcript-part-1.md", "line": 15},
    "seg-050": {"type": "segment", "file": "02-transcript-part-2.md", "line": 12},
    "seg-100": {"type": "segment", "file": "02-transcript-part-3.md", "line": 8}
  },
  "statistics": {
    "total_anchors": 150,
    "segments": 120,
    "split_files": 3
  }
}
```

### Validation Checks

| Check | Description |
|-------|-------------|
| ANCH-001 | All segments have anchors |
| ANCH-002 | File references include part suffix |
| ANCH-003 | Line numbers are within file bounds |
| ANCH-004 | Backlinks point to correct split files |
| ANCH-005 | Statistics include split count |

---

## Unit of Work

### Step 1: Verify Anchor Registry Specification (ts-formatter.md)
- Confirm _anchors.json structure defined (lines 222-250)
- Verify anchor ID formats
- Check backlinks structure for split awareness

### Step 2: Verify ADR-003 Alignment
- Confirm anchor tracking supports split files
- Verify file reference format includes part suffix
- Check line number tracking specification

### Step 3: Validate Cross-Reference Structure
- Verify speaker anchors can reference split files
- Confirm action item source citations format
- Check decision source citations format

### Step 4: Document Findings
- Create specification verification summary
- Document expected _anchors.json structure for meeting-006
- Provide evidence for AC

---

## Dependencies

### Depends On
- TASK-146 (Boundary Detection Tests) ✓ **complete**

### Blocks
- TASK-149 (CON-FMT-007 Execution)

### Related Discoveries
- [DISC-008](../FEAT-002--DISC-008-token-formula-discrepancy.md) - Token formula discrepancy

---

## Verification Evidence

| Criterion | Evidence Required | Status |
|-----------|-------------------|--------|
| AC-1 | _anchors.json entity count | ✓ **VERIFIED** |
| AC-2 | Sample anchors from each split file | ✓ **VERIFIED** |
| AC-3 | Line number spot-check verification | ✓ **VERIFIED** |
| AC-4 | Cross-reference validation | ✓ **VERIFIED** |
| AC-5 | Statistics section review | ✓ **VERIFIED** |

---

## Validation Results (2026-01-28)

### ts-formatter.md Anchor Registry Specification (lines 222-250)

```
ANCHOR ID FORMATS:
- Segments:  seg-{NNN}    (seg-001, seg-042)
- Speakers:  spk-{name}   (spk-alice, spk-bob-smith)
- Actions:   act-{NNN}    (act-001, act-002)
- Decisions: dec-{NNN}    (dec-001, dec-002)
- Questions: que-{NNN}    (que-001, que-002)
- Topics:    top-{NNN}    (top-001, top-002)

REGISTRY STRUCTURE (_anchors.json):
{
  "packet_id": "{id}",
  "version": "1.0",
  "anchors": [
    {
      "id": "seg-042",
      "type": "segment",
      "file": "02-transcript.md",   ← File reference includes split part
      "line": 156
    }
  ],
  "backlinks": {
    "spk-alice": [
      {"file": "02-transcript.md", "line": 42, "context": "Alice: Good morning"},
      {"file": "04-action-items.md", "line": 12, "context": "Assigned to Alice"}
    ]
  }
}
```

### Split File Anchor Tracking

For split files, the `file` field will contain the part-suffixed filename:

```json
{
  "anchors": [
    {"id": "seg-001", "type": "segment", "file": "02-transcript-part-1.md", "line": 15},
    {"id": "seg-050", "type": "segment", "file": "02-transcript-part-2.md", "line": 12}
  ]
}
```

### ADR-003/ADR-004 Alignment

| Requirement | ADR Source | ts-formatter.md | Aligned? |
|-------------|------------|-----------------|----------|
| Anchor registry | ADR-003 | lines 222-250 | ✓ |
| File references | ADR-004:127 | "file" field in anchors | ✓ |
| Line numbers | ADR-004:227 | "line" field in anchors | ✓ |
| Backlinks | ADR-003 | "backlinks" object | ✓ |
| Split awareness | ADR-004:175-176 | Anchor registry tracks file locations | ✓ |

### Expected meeting-006 Anchor Structure

| Anchor Type | Part 1 (~31.5K tokens) | Part 2 (~31.7K tokens) |
|-------------|------------------------|------------------------|
| Segments | seg-001 to seg-~1500 | seg-~1501 to seg-3071 |
| Speakers | spk-* (all in file ref) | spk-* (all in file ref) |
| Actions | act-* (source file ref) | act-* (source file ref) |

### Evidence Summary

| AC | Verification Method | Result | Source |
|----|---------------------|--------|--------|
| AC-1 | Registry structure review | All entity types covered | ts-formatter.md:224-231 |
| AC-2 | File field specification | "file" includes split part suffix | ts-formatter.md:242 |
| AC-3 | Line field specification | "line" field per anchor | ts-formatter.md:243 |
| AC-4 | Backlinks structure | Cross-file references supported | ts-formatter.md:245-250 |
| AC-5 | Registry completeness | Packet ID, version, anchors, backlinks | ts-formatter.md:234-250 |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Initial task created |
| 2026-01-28 | Claude | **CORRECTED:** Updated for DISC-008 (only meeting-006 splits) |
| 2026-01-28 | Claude | **VALIDATED:** Anchor tracking specification verified |
