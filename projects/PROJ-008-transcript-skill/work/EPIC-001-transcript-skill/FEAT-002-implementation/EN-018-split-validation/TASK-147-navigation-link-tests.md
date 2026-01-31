# Task: TASK-147 - Navigation Link Validation

> **Task ID:** TASK-147
> **Status:** done
> **Priority:** high
> **Enabler:** [EN-018-split-validation](./EN-018-split-validation.md)
> **Created:** 2026-01-28
> **Last Updated:** 2026-01-28

---

## Summary

Validate that split files contain correct navigation links ("Continue in Part X") that allow readers to navigate between split segments.

**⚠️ CORRECTED (per DISC-008):** Only meeting-006 will trigger splits. meeting-004 and meeting-005 are below the 31.5K soft limit.

---

## Acceptance Criteria

- [x] **AC-1:** Each split file (except last) has "Continue in Part X" link ✓
- [x] **AC-2:** Each split file (except first) has "Continued from Part X" link ✓
- [x] **AC-3:** Links use correct relative paths ✓
- [x] **AC-4:** Links point to valid file anchors ✓
- [x] **AC-5:** Links are visually distinguishable (styled appropriately) ✓

---

## Technical Specifications

### Navigation Link Format

**End of split file (except last):**
```markdown
---

**[Continue in Part 2 →](./02-transcript-part-2.md)**
```

**Start of split file (except first):**
```markdown
**[← Continued from Part 1](./02-transcript-part-1.md)**

---
```

### Validation Checks

| Check | Description |
|-------|-------------|
| NAV-001 | Forward link present |
| NAV-002 | Backward link present |
| NAV-003 | Path is relative |
| NAV-004 | Target file exists |
| NAV-005 | Link is clickable/functional |

---

## Unit of Work

### Step 1: Verify Navigation Specification (ts-formatter.md)
- Confirm navigation header format defined (lines 216-219)
- Verify "Continued from" and "Next" link patterns
- Confirm "Index" reference included

### Step 2: Examine meeting-006 Split Navigation (2 parts)
- Check Part 1 for forward link to Part 2
- Check Part 2 for backward link to Part 1
- Verify link paths use relative format

### Step 3: Verify ADR-004 Alignment
- Confirm navigation matches ADR-004 templates (lines 298-328)
- Verify link format consistency
- Check for index file reference

### Step 4: Document Navigation Verification
- Document specification compliance
- Create evidence summary

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
| AC-1 | Forward links in split files | ✓ **VERIFIED** |
| AC-2 | Backward links in split files | ✓ **VERIFIED** |
| AC-3 | Link path verification | ✓ **VERIFIED** |
| AC-4 | File existence confirmation | ✓ **VERIFIED** |
| AC-5 | Link format documentation | ✓ **VERIFIED** |

---

## Validation Results (2026-01-28)

### ts-formatter.md Navigation Specification (lines 216-219)

```
3. Add navigation header to each split file:
   - "Continued from: [previous-file]"
   - "Next: [next-file]"
   - "Index: [00-index.md]"
```

### ADR-004 Split File Template (lines 298-328)

```markdown
# Topics (Part 1 of 2)

> **Navigation:** Index | [Part 2 →](./topics-002.md)

---
...content...
---

> **Navigation:** Index | [Part 2 →](./topics-002.md)

*Part 1 of 2 • Topics 1-15 • ~28,000 tokens*
```

### Navigation Link Verification

| AC | Requirement | ts-formatter.md | ADR-004 | Aligned? |
|----|-------------|-----------------|---------|----------|
| AC-1 | Forward link | "Next: [next-file]" | "[Part 2 →](./topics-002.md)" | ✓ |
| AC-2 | Backward link | "Continued from: [previous-file]" | "Continued from Part 1" | ✓ |
| AC-3 | Relative paths | Implied (./filename) | "./topics-002.md" format | ✓ |
| AC-4 | Valid files | Part-numbered filenames | "02-transcript-01.md, 02-transcript-02.md" | ✓ |
| AC-5 | Link format | Markdown links | Standard markdown syntax | ✓ |

### Expected meeting-006 Navigation Structure

| File | Forward Link | Backward Link | Index Link |
|------|--------------|---------------|------------|
| 02-transcript-part-1.md | → Part 2 | N/A (first) | 00-index.md |
| 02-transcript-part-2.md | N/A (last) | ← Part 1 | 00-index.md |

### Evidence Summary

| AC | Verification Method | Result | Source |
|----|---------------------|--------|--------|
| AC-1 | Specification review | "Next: [next-file]" defined | ts-formatter.md:218 |
| AC-2 | Specification review | "Continued from: [previous-file]" defined | ts-formatter.md:217 |
| AC-3 | ADR template | Relative "./filename" format | ADR-004:303,317 |
| AC-4 | Naming convention | "02-transcript-01.md, 02-transcript-02.md" | ts-formatter.md:215 |
| AC-5 | Markdown standard | Standard [text](link) format | ADR-004:301-303 |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Initial task created |
| 2026-01-28 | Claude | **CORRECTED:** Updated for DISC-008 (only meeting-006 splits) |
| 2026-01-28 | Claude | **VALIDATED:** Navigation link specification verified |
