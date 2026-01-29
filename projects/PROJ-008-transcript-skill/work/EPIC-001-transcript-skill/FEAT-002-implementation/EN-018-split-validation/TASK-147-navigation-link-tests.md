# Task: TASK-147 - Navigation Link Validation

> **Task ID:** TASK-147
> **Status:** pending
> **Priority:** high
> **Enabler:** [EN-018-split-validation](./EN-018-split-validation.md)
> **Created:** 2026-01-28
> **Last Updated:** 2026-01-28

---

## Summary

Validate that split files contain correct navigation links ("Continue in Part X") that allow readers to navigate between split segments.

---

## Acceptance Criteria

- [ ] **AC-1:** Each split file (except last) has "Continue in Part X" link
- [ ] **AC-2:** Each split file (except first) has "Continued from Part X" link
- [ ] **AC-3:** Links use correct relative paths
- [ ] **AC-4:** Links point to valid file anchors
- [ ] **AC-5:** Links are visually distinguishable (styled appropriately)

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

### Step 1: Examine meeting-005 Split Navigation
- Check Part 1 for forward link
- Check Part 2 for backward link
- Verify link paths

### Step 2: Examine meeting-006 Split Navigation
- Check all parts for appropriate links
- Verify link chain is complete
- Confirm all paths are valid

### Step 3: Test Link Functionality
- Verify target files exist
- Confirm relative paths resolve correctly
- Check link styling

### Step 4: Document Navigation
- Screenshot or copy link structures
- Document any issues found
- Create evidence summary

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
| AC-1 | Forward links in split files |
| AC-2 | Backward links in split files |
| AC-3 | Link path verification |
| AC-4 | File existence confirmation |
| AC-5 | Link format documentation |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Initial task created |
