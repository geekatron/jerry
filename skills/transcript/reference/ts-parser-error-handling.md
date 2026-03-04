# ts-parser Error Handling Reference

> Defensive parsing error handling, encoding fallback chain, and enhanced error capture schema.
> Implements PAT-002: "Accept liberally, produce consistently."

---

## Error Handling Table (PAT-002: Defensive Parsing)

| Error | Detection | Recovery | Error Code |
|-------|-----------|----------|------------|
| Malformed timestamp | Regex fails | Best-effort parse, log warning | WARN-001 |
| Negative duration | end_ms < start_ms | Swap values, log warning | WARN-002 |
| Fallback encoding | UTF-8 fails | Try fallback chain, log warning | WARN-003 |
| Voice tag with class | `<v.class Name>` | Strip class, extract name | WARN-004 |
| Invalid voice syntax | Empty `<v>` | Extract as anonymous | ERR-001 |
| Empty after stripping | Tags removed, no content | Skip segment | ERR-002 |
| Malformed cue | Can't parse structure | Best effort, log error | ERR-003 |
| Empty cue text | len(text) == 0 | Skip segment | SKIP-001 |
| Whitespace-only | len(text.strip()) == 0 | Skip segment | SKIP-002 |
| Empty voice annotation | `<v></v>` | Skip segment | SKIP-003 |

## Encoding Fallback Chain (NFR-007)

```
Attempt decoding in this order:
1. UTF-8 with BOM detection (check for BOM marker first)
2. UTF-8 without BOM (try decode)
3. Windows-1252 (common Windows encoding)
4. ISO-8859-1 (Western European)
5. Latin-1 (final fallback - accepts all byte values)

If all fail: Log error with bytes preview, return empty result
```

> **NOTE (DEC-001):** UTF-16 BOM detection is **OUT OF SCOPE** for MVP. Current
> implementation only supports UTF-8 BOM. UTF-16 support deferred to EN-017.
> See [EN-007:DEC-001](../../../projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-002-implementation/EN-007-vtt-parser/EN-007--DEC-001-utf16-bom-out-of-scope.md).

## Recovery Principle

- Continue parsing despite individual segment errors
- Capture ALL issues in parse_metadata for transparency
- Never fail entirely if partial parsing is possible
- Surface errors to downstream consumers for quality assessment

## Enhanced Error Capture Schema (v1.2 - TDD-ts-parser.md Section 6.1)

All parsing issues MUST be captured in the `parse_metadata` object:

```json
{
  "parse_metadata": {
    "parse_status": "complete|partial|failed",
    "parse_warnings": [
      {
        "code": "WARN-001",
        "message": "Malformed timestamp at cue 15",
        "cue_index": 15,
        "severity": "warning",
        "raw_value": "0:05:23.abc"
      }
    ],
    "parse_errors": [
      {
        "code": "ERR-001",
        "message": "Invalid voice tag syntax",
        "cue_index": 42,
        "severity": "error",
        "raw_value": "<v>",
        "recovery_action": "extracted_as_anonymous"
      }
    ],
    "skipped_segments": [
      {
        "cue_index": 23,
        "reason": "empty_payload",
        "raw_content": ""
      }
    ]
  }
}
```

**parse_status Determination:**
- `complete` - No errors, no skipped segments
- `partial` - Has warnings OR skipped segments, but no fatal errors
- `failed` - Fatal error preventing any extraction
