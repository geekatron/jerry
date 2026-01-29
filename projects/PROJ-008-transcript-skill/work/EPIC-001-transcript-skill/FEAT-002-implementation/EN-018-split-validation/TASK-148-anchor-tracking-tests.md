# Task: TASK-148 - Anchor Tracking Tests

> **Task ID:** TASK-148
> **Status:** pending
> **Priority:** high
> **Enabler:** [EN-018-split-validation](./EN-018-split-validation.md)
> **Created:** 2026-01-28
> **Last Updated:** 2026-01-28

---

## Summary

Validate that _anchors.json correctly tracks entities across split files, with accurate file references and line numbers.

---

## Acceptance Criteria

- [ ] **AC-1:** _anchors.json contains entries for all entity types
- [ ] **AC-2:** File references point to correct split file (part-1, part-2, etc.)
- [ ] **AC-3:** Line numbers are accurate within each split file
- [ ] **AC-4:** Cross-references work across split boundaries
- [ ] **AC-5:** Statistics reflect total across all splits

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

### Step 1: Examine meeting-005 Anchors
- Parse _anchors.json
- Verify segment anchors span both parts
- Check line number accuracy

### Step 2: Examine meeting-006 Anchors
- Parse _anchors.json
- Verify segment anchors span all parts
- Check line number accuracy for each part

### Step 3: Validate Cross-References
- Check speaker anchors reference correct file
- Verify action item source citations
- Confirm decision source citations

### Step 4: Verify Statistics
- Confirm total segment count
- Verify split file count
- Check entity totals

### Step 5: Document Findings
- Create anchor verification summary
- Document any discrepancies
- Provide evidence for AC

---

## Dependencies

### Depends On
- TASK-146 (Boundary Detection Tests)

### Blocks
- TASK-149 (CON-FMT-007 Execution)

---

## Verification Evidence

| Criterion | Evidence Required |
|-----------|-------------------|
| AC-1 | _anchors.json entity count |
| AC-2 | Sample anchors from each split file |
| AC-3 | Line number spot-check verification |
| AC-4 | Cross-reference validation |
| AC-5 | Statistics section review |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Initial task created |
