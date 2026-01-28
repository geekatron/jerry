# TASK-107: Verify Encoding Detection with Fallbacks (NFR-007)

<!--
TEMPLATE: Task
VERSION: 2.0.0
SOURCE: ps-critic GAP-002 Finding
CREATED: 2026-01-27
-->

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Created:** 2026-01-27T00:00:00Z
> **Updated:** 2026-01-27T00:00:00Z
> **Parent:** EN-007
> **Owner:** Claude
> **Effort Points:** 1
> **Blocked By:** ~~TASK-101~~ (completed)

---

## Summary

Verify that ts-parser agent correctly implements the **multi-encoding fallback chain** specified in TDD-ts-parser.md Section 5 (NFR-007). Current tests only verify UTF-8 detection; fallback behavior for Windows-1252, ISO-8859-1, and Latin-1 is untested.

**Origin:** ps-critic review GAP-002 finding - "AC-7 (Encoding detection) unchecked"

---

## Background

### Current State

1. **UTF-8 Detection**: Verified via test `vtt-ce-004` in parser-tests.yaml
2. **Schema Validation**: `source.encoding` field presence verified
3. **Error Code**: WARN-003 defined for "Fallback encoding used"

### Gap Analysis

Per TDD-ts-parser.md Section 5, the encoding detection flow is:

```
TRY UTF-8 DECODE
      │
      ├─── SUCCESS ───► Use UTF-8
      │
      └─── FAILURE ───► TRY FALLBACKS:
                              │
                              ├── Windows-1252
                              ├── ISO-8859-1
                              └── Latin-1
```

**Missing Test Coverage:**
- No test files in non-UTF-8 encoding
- No verification of fallback chain behavior
- No test for WARN-003 error code generation

---

## Acceptance Criteria

### Definition of Done

- [ ] Test file created with Windows-1252 encoding
- [ ] Test file created with ISO-8859-1 encoding
- [ ] Test specifications added to parser-tests.yaml
- [ ] Verify fallback chain triggers WARN-003
- [ ] AC-7 marked as verified in EN-007

### Technical Criteria

| # | Criterion | Source | Verified |
|---|-----------|--------|----------|
| AC-1 | Windows-1252 file decodes correctly | TDD Section 5 | [ ] |
| AC-2 | ISO-8859-1 file decodes correctly | TDD Section 5 | [ ] |
| AC-3 | Fallback triggers WARN-003 code | TDD Section 6.1 | [ ] |
| AC-4 | source.encoding reflects actual encoding used | Schema | [ ] |

---

## Test Specification

```yaml
# Addition to parser-tests.yaml

encoding_fallback:
  description: "Encoding fallback chain tests (NFR-007)"
  implements: "NFR-007"
  reference: "TDD-ts-parser.md Section 5"

  tests:
    - id: enc-001
      name: "Windows-1252 fallback"
      description: "Verify Windows-1252 encoded file triggers fallback"
      input:
        file: "transcripts/edge_cases/windows1252_sample.vtt"
        actual_encoding: "windows-1252"
      assertions:
        - type: encoding_detected
          expected: "windows-1252"
        - type: parse_warning
          expected_code: "WARN-003"
        - type: segment_count
          minimum: 1

    - id: enc-002
      name: "ISO-8859-1 fallback"
      description: "Verify ISO-8859-1 encoded file triggers fallback"
      input:
        file: "transcripts/edge_cases/iso88591_sample.vtt"
        actual_encoding: "iso-8859-1"
      assertions:
        - type: encoding_detected
          expected: "iso-8859-1"
        - type: parse_warning
          expected_code: "WARN-003"
```

---

## Deliverables

| Deliverable | Path | Description |
|-------------|------|-------------|
| Windows-1252 Test File | `test_data/transcripts/edge_cases/windows1252_sample.vtt` | VTT with Windows-1252 characters |
| ISO-8859-1 Test File | `test_data/transcripts/edge_cases/iso88591_sample.vtt` | VTT with ISO-8859-1 characters |
| Expected JSON (Windows) | `test_data/expected/windows1252_sample.expected.json` | Expected output |
| Expected JSON (ISO) | `test_data/expected/iso88591_sample.expected.json` | Expected output |
| Test Specification | `test_data/validation/parser-tests.yaml` | encoding_fallback section |

---

## Implementation Notes

### Creating Non-UTF-8 Test Files

```python
# Python snippet to create Windows-1252 test file
content = """WEBVTT

00:00:00.000 --> 00:00:05.000
<v Müller>Guten Tag, wie geht's?

00:00:05.000 --> 00:00:10.000
<v François>Très bien, merci!
"""

# Write with Windows-1252 encoding
with open('windows1252_sample.vtt', 'w', encoding='windows-1252') as f:
    f.write(content)
```

### Characters That Differ Between Encodings

| Character | UTF-8 | Windows-1252 | ISO-8859-1 |
|-----------|-------|--------------|------------|
| € (Euro) | E2 82 AC | 80 | Not present |
| „ (Low quote) | E2 80 9E | 84 | Not present |
| ö (o-umlaut) | C3 B6 | F6 | F6 |
| é (e-acute) | C3 A9 | E9 | E9 |

---

## Related Items

- **Parent Enabler:** [EN-007](./EN-007-vtt-parser.md)
- **TDD Reference:** TDD-ts-parser.md Section 5
- **Triggered By:** ps-critic GAP-002 finding
- **Risk Mitigation:** R-003 (Encoding issues) - Score 6 (GREEN)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-27 | Claude | pending | Task created per ps-critic GAP-002 finding |
