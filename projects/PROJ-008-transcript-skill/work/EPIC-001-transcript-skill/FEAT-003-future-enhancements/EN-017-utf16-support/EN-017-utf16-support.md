# EN-017: UTF-16 BOM Support

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: EN-007:DEC-001 (UTF-16 BOM Out of Scope)
CREATED: 2026-01-27
PURPOSE: Tech debt enabler for UTF-16 encoding support
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** low
> **Impact:** low
> **Enabler Type:** infrastructure
> **Created:** 2026-01-27T00:00:00Z
> **Due:** TBD
> **Completed:**
> **Parent:** FEAT-003
> **Owner:** Claude
> **Effort:** 3

---

## Summary

Implement **UTF-16 BOM detection and decoding** for the ts-parser agent as specified in the original TDD-ts-parser.md Section 5 encoding detection flow. This was deferred from MVP scope per [EN-007:DEC-001](../../FEAT-002-implementation/EN-007-vtt-parser/EN-007--DEC-001-utf16-bom-out-of-scope.md).

**Tech Debt Origin:** TASK-107 Documentation Audit (2026-01-27)

---

## Problem Statement

The TDD-ts-parser.md Section 5 specifies UTF-16 and UTF-16LE BOM detection:

```
BOM found         No BOM
    │                 │
    ▼                 ▼
┌─────────┐    ┌───────────────┐
│ UTF-8   │    │ Try decode as │
│ UTF-16  │    │ UTF-8         │
│ UTF-16LE│    └───────┬───────┘
└─────────┘
```

However, the current ts-parser agent implementation only supports UTF-8 BOM detection. UTF-16 encoded transcripts (rare but possible) will fail to parse.

---

## Business Value

| Benefit | Value |
|---------|-------|
| **Completeness** | Full TDD compliance for encoding detection |
| **Edge Case Coverage** | Support for legacy Windows-generated transcripts |
| **Risk Reduction** | Prevent silent parsing failures |

**ROI Assessment:** LOW - UTF-16 transcripts are extremely rare (<0.1% of use cases per EN-001 Market Analysis)

---

## Technical Approach

### L0: Simple Analogy

Like a door that recognizes three different key types (UTF-8, UTF-16, UTF-16LE) based on the shape at the start of the key.

### L1: Technical Implementation

1. **BOM Detection Enhancement:**
   - UTF-8 BOM: `EF BB BF`
   - UTF-16 BE BOM: `FE FF`
   - UTF-16 LE BOM: `FF FE`

2. **Encoding Flow Update:**
   ```python
   def detect_encoding(content: bytes) -> str:
       if content.startswith(b'\xef\xbb\xbf'):
           return 'utf-8-sig'
       elif content.startswith(b'\xfe\xff'):
           return 'utf-16-be'
       elif content.startswith(b'\xff\xfe'):
           return 'utf-16-le'
       else:
           # Fallback chain as before
           ...
   ```

3. **Update Artifacts:**
   - Remove "OUT OF SCOPE" note from TDD-ts-parser.md
   - Remove "OUT OF SCOPE" note from ts-parser.md
   - Add UTF-16 test cases to parser-tests.yaml

### L2: Architectural Considerations

- **Backward Compatibility:** No breaking changes - existing UTF-8 files continue to work
- **Performance:** BOM check is O(1), no impact on parse performance
- **Testing:** Requires creating UTF-16 encoded test files

---

## Acceptance Criteria

### Definition of Done

- [ ] UTF-16 BE BOM detection implemented
- [ ] UTF-16 LE BOM detection implemented
- [ ] Test cases created for both UTF-16 variants
- [ ] TDD-ts-parser.md note removed
- [ ] ts-parser.md note removed
- [ ] EN-007:DEC-001 marked as superseded

---

## Children (Tasks)

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| TASK-001 | Implement UTF-16 BOM detection | pending | 1 |
| TASK-002 | Create UTF-16 test files | pending | 1 |
| TASK-003 | Update documentation | pending | 1 |

**NOTE:** Tasks use enabler-scoped numbering (TASK-001, TASK-002, TASK-003) per worktracker conventions.

---

## Related Items

| Type | Item | Description |
|------|------|-------------|
| Origin | [EN-007:DEC-001](../../FEAT-002-implementation/EN-007-vtt-parser/EN-007--DEC-001-utf16-bom-out-of-scope.md) | Decision that deferred this work |
| Specification | [TDD-ts-parser.md](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-parser.md) | Original specification (Section 5) |
| Agent | [ts-parser.md](../../../../../skills/transcript/agents/ts-parser.md) | Agent to be updated |
| Prerequisite | FEAT-002 | Core implementation must be complete first |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-27 | Claude | pending | Enabler created per EN-007:DEC-001 |
