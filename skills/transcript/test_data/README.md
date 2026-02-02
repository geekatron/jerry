# Transcript Skill Test Data

> **Version:** 1.3.0
> **Created:** 2026-01-27
> **Updated:** 2026-01-28 (Added large transcript golden dataset - EN-017)
> **Source:** EN-007:DISC-002 (Test Infrastructure Dependency Gap Resolution)
> **Research:** EN-007 webvtt-test-suite-research.md
> **Review Status:** PENDING_HUMAN_REVIEW

---

## Purpose

This directory contains test data and validation specifications for the transcript skill agents (ts-parser, ts-extractor, ts-formatter).

**Design Principle:** Self-contained within the skill directory per EN-007:DISC-002 decision.

---

## Directory Structure

```
test_data/
├── README.md                              ← This file
├── transcripts/                           ← Test input files
│   ├── real/                              ← Real VTT files from users
│   │   └── internal-sample-sample.vtt
│   ├── golden/                            ← Synthetic golden dataset (EN-017)
│   │   ├── meeting-001.vtt                ← 8 min, ~1.6K tokens (no splits)
│   │   ├── meeting-004-sprint-planning.vtt ← 126 min, ~23K tokens (no splits)
│   │   ├── meeting-005-roadmap-review.vtt  ← 160 min, ~37K tokens (1 split)
│   │   └── meeting-006-all-hands.vtt       ← 304 min, ~94K tokens (2-3 splits)
│   └── edge_cases/                        ← Edge case VTT files (W3C research)
│       ├── voice_tag_basic.vtt            ← VT-001, VT-002
│       ├── voice_tag_no_close.vtt         ← VT-004
│       ├── voice_tag_with_class.vtt       ← VT-006, VT-007
│       ├── multi_speaker_cue.vtt          ← VT-009
│       ├── nested_formatting.vtt          ← VT-008, TT-008
│       ├── multiline_payload.vtt          ← ML-001 through ML-005
│       ├── unicode_speakers.vtt           ← CE-003, CE-004
│       ├── entity_escapes.vtt             ← CE-005, CE-006, CE-007
│       ├── timestamp_edge_cases.vtt       ← TS-001 through TS-005
│       ├── empty_and_malformed.vtt        ← PAT-002 defensive parsing
│       ├── combined_edge_cases.vtt        ← All edge cases combined
│       ├── windows1252_sample.vtt         ← ⚠️ BINARY: Windows-1252 encoding test
│       ├── windows1252_sample.srt         ← ⚠️ BINARY: Windows-1252 SRT test
│       ├── iso88591_sample.vtt            ← ⚠️ BINARY: ISO-8859-1 encoding test
│       └── iso88591_sample.srt            ← ⚠️ BINARY: ISO-8859-1 SRT test
├── expected/                              ← Expected parser outputs
│   ├── internal-sample-sample.expected.json
│   ├── windows1252_sample.expected.json   ← Encoding fallback expected output
│   ├── windows1252_sample_srt.expected.json
│   ├── iso88591_sample.expected.json
│   └── iso88591_sample_srt.expected.json
└── validation/                            ← Test specifications
    └── parser-tests.yaml                  ← ts-parser test cases (v1.1.0)
```

---

## Current Contents

### Real Transcript Sample

| File | Source | Cues | Speakers | Purpose |
|------|--------|------|----------|---------|
| `transcripts/real/internal-sample-sample.vtt` | User VTT (first 20 cues) | 20 | 2 (Adam Nowak, Brendan Bennett) | VTT parsing verification |

### Large Transcript Golden Dataset (EN-017)

Created for testing file splitting behavior in ts-formatter. Token calculation uses formula from DISC-006:
`actual_tokens = (word_count × 1.3) + (cue_count × 12)`

| File | Duration | Words | Cues | Tokens | Splits | Topic |
|------|----------|-------|------|--------|--------|-------|
| `meeting-004-sprint-planning.vtt` | 02:05:45 | 13,030 | 536 | ~23,371 | 0 | Engineering sprint |
| `meeting-005-roadmap-review.vtt` | 02:40:02 | 20,202 | 899 | ~37,051 | 1 | Product roadmap |
| `meeting-006-all-hands.vtt` | 05:03:46 | 44,225 | 3,071 | ~94,345 | 2-3 | Quarterly all-hands |

**Split Thresholds (ADR-004):**
- **Soft Limit:** 31,500 tokens (prefer split at semantic ## boundaries)
- **Hard Limit:** 35,000 tokens (force split regardless)

**Speaker Rosters:**
- **meeting-004:** Sarah Chen (SM), Mike Johnson, Emma Williams, David Kim, Lisa Martinez, Raj Patel
- **meeting-005:** Jennifer Adams (VP Product), Marcus Thompson, Anna Kowalski, Chris Wong, Steve Roberts, Priya Sharma, Olivia Foster
- **meeting-006:** Robert Chen (CEO), Diana Martinez (CTO), James Wilson, Jennifer Adams, Michelle Taylor, Kevin O'Brien, 30+ employees

**Entity Distribution:**

| Entity Type | meeting-004 | meeting-005 | meeting-006 |
|-------------|-------------|-------------|-------------|
| Topics | 4 | 5+ | 8+ |
| Action Items | 10+ | 14+ | 17+ |
| Decisions | 2-3 | 6+ | 7+ |
| Questions | 5+ | 10+ | 14+ |

**W3C Compliance:** All files validated with `validate_vtt.py` (monotonic timestamps, valid seconds < 60)

**Source:** EN-017 TASK-141 through TASK-143

---

### Edge Case Files (from W3C WebVTT Research)

| File | Test IDs | Description |
|------|----------|-------------|
| `voice_tag_basic.vtt` | VT-001, VT-002 | Basic voice tags with/without spaces in names |
| `voice_tag_no_close.vtt` | VT-004 | Voice tags without closing `</v>` |
| `voice_tag_with_class.vtt` | VT-006, VT-007 | Voice tags with CSS classes (`.loud`, `.whisper`) |
| `multi_speaker_cue.vtt` | VT-009 | Multiple speakers in single cue |
| `nested_formatting.vtt` | VT-008, TT-008 | Nested `<b>`, `<i>`, `<u>` within voice tags |
| `multiline_payload.vtt` | ML-001–ML-005 | Multi-line cue payloads, whitespace handling |
| `unicode_speakers.vtt` | CE-003, CE-004 | Unicode: Chinese, Arabic, Greek, Japanese, Emoji |
| `entity_escapes.vtt` | CE-005–CE-007 | HTML entities: `&amp;`, `&lt;`, `&gt;`, `&nbsp;` |
| `timestamp_edge_cases.vtt` | TS-001–TS-005 | Timestamp formats: no hours, extended hours, boundaries |
| `empty_and_malformed.vtt` | PAT-002 | Empty cues, whitespace-only, empty voice annotations |
| `combined_edge_cases.vtt` | All | All edge cases in single file |
| `windows1252_sample.vtt` | ENC-001 | ⚠️ **BINARY** - Windows-1252 encoding (€, smart quotes) |
| `windows1252_sample.srt` | ENC-003 | ⚠️ **BINARY** - Windows-1252 SRT encoding test |
| `iso88591_sample.vtt` | ENC-002 | ⚠️ **BINARY** - ISO-8859-1 encoding (German, French chars) |
| `iso88591_sample.srt` | ENC-004 | ⚠️ **BINARY** - ISO-8859-1 SRT encoding test |

### Expected Output

| File | Source | Purpose |
|------|--------|---------|
| `expected/internal-sample-sample.expected.json` | Derived from VTT (deterministic) | Golden output for comparison |
| `expected/windows1252_sample.expected.json` | TASK-107 encoding tests | Windows-1252 VTT expected output |
| `expected/windows1252_sample_srt.expected.json` | TASK-107 encoding tests | Windows-1252 SRT expected output |
| `expected/iso88591_sample.expected.json` | TASK-107 encoding tests | ISO-8859-1 VTT expected output |
| `expected/iso88591_sample_srt.expected.json` | TASK-107 encoding tests | ISO-8859-1 SRT expected output |

### Test Specifications

| File | Agent | Test Count | Status |
|------|-------|------------|--------|
| `validation/parser-tests.yaml` | ts-parser | 18 VTT + 4 encoding + SRT + TXT tests | PENDING_HUMAN_REVIEW |

---

## ⚠️ ENCODING TEST FILES - IMPORTANT WARNING

The following files are **BINARY files** with specific byte sequences designed to test encoding fallback (NFR-007):

| File | Encoding | Special Bytes |
|------|----------|---------------|
| `windows1252_sample.vtt` | Windows-1252 | `0x80` (€), `0x93/0x94` (smart quotes), `0x92` (') |
| `windows1252_sample.srt` | Windows-1252 | Same as above |
| `iso88591_sample.vtt` | ISO-8859-1 | `0xF6` (ö), `0xE9` (é), `0xE8` (è), `0xE0` (à) |
| `iso88591_sample.srt` | ISO-8859-1 | Same as above |

### DO NOT EDIT WITH TEXT EDITORS

**WARNING:** These files contain bytes that are INVALID UTF-8. Opening them in a text editor may:
- Corrupt the byte sequences (making tests invalid)
- Transcode characters incorrectly
- Add/remove BOM markers

### Regeneration

If files become corrupted, regenerate them using the Python script:
```python
# Example regeneration (see test_data/scripts/generate_encoding_tests.py for full script)
windows1252_content = b'WEBVTT\n\n...\n<v M\xfcller>The price is \x8050...'
with open('windows1252_sample.vtt', 'wb') as f:
    f.write(windows1252_content)
```

### Purpose

These files verify the encoding fallback chain per NFR-007:
1. UTF-8 decode attempt FAILS (invalid byte sequences)
2. Parser falls back to Windows-1252 or ISO-8859-1
3. WARN-003 is emitted in `parse_metadata.parse_warnings`

**Reference:** EN-007:DEC-001 (UTF-16 BOM out of scope), TDD-ts-parser.md Section 5

---

## Test Case Summary

### Core VTT Tests (5 - from DISC-002)

| Test ID | Name | Input | Coverage |
|---------|------|-------|----------|
| vtt-001 | Voice tags with closing tags | internal-sample-sample.vtt | FR-001.3 |
| vtt-002 | Multi-line cue payloads | internal-sample-sample.vtt | FR-001.4 |
| vtt-003 | Timestamp normalization | internal-sample-sample.vtt | NFR-006 |
| vtt-004 | Speaker extraction | internal-sample-sample.vtt | FR-001.3 |
| vtt-005 | Canonical JSON schema | internal-sample-sample.vtt | TDD Section 3 |

### Edge Case Tests (9 - from W3C Research)

| Test ID | Name | Input | Research ID |
|---------|------|-------|-------------|
| vtt-006 | Voice tags without closing | voice_tag_no_close.vtt | VT-004 |
| vtt-007 | Voice tags with classes | voice_tag_with_class.vtt | VT-006, VT-007 |
| vtt-008 | Multiple speakers per cue | multi_speaker_cue.vtt | VT-009 |
| vtt-009 | Nested formatting tags | nested_formatting.vtt | VT-008, TT-008 |
| vtt-010 | Unicode speakers/content | unicode_speakers.vtt | CE-003, CE-004 |
| vtt-011 | HTML entity decoding | entity_escapes.vtt | CE-005–CE-007 |
| vtt-012 | Timestamp edge cases | timestamp_edge_cases.vtt | TS-001–TS-005 |
| vtt-013 | Empty/malformed (PAT-002) | empty_and_malformed.vtt | Error handling |
| vtt-014 | Combined edge cases | combined_edge_cases.vtt | Comprehensive |

### Encoding Fallback Tests (4 - from TASK-107)

| Test ID | Name | Input | Requirement |
|---------|------|-------|-------------|
| enc-001 | Windows-1252 VTT fallback | windows1252_sample.vtt | NFR-007.1, NFR-007.2 |
| enc-002 | ISO-8859-1 VTT fallback | iso88591_sample.vtt | NFR-007.1, NFR-007.4 |
| enc-003 | Windows-1252 SRT fallback | windows1252_sample.srt | NFR-007.2 |
| enc-004 | ISO-8859-1 SRT fallback | iso88591_sample.srt | NFR-007.4 |

---

## Review Status

**IMPORTANT:** The expected output JSON was derived deterministically from the VTT file. Human review is required before using for verification.

### Items Requiring Human Review

1. **internal-sample-sample.expected.json**
   - Verify speaker names extracted correctly
   - Verify timestamps converted to milliseconds correctly
   - Verify multi-line text joined correctly
   - Verify closing `</v>` tags stripped

2. **parser-tests.yaml (v1.1.0)**
   - Verify test assertions match acceptance criteria
   - Confirm edge case test coverage is adequate
   - Review W3C-derived test cases for applicability

3. **Edge case VTT files**
   - Verify files match W3C specification requirements
   - Confirm Unicode test data covers required scripts

---

## Research Reference

Edge case files were created based on comprehensive W3C WebVTT research:

- **Research Document:** `EN-007/research/webvtt-test-suite-research.md`
- **Sources:**
  - [W3C WebVTT Specification](https://www.w3.org/TR/webvtt1/)
  - [web-platform-tests/wpt](https://github.com/web-platform-tests/wpt/tree/master/webvtt)
  - [MDN WebVTT Format](https://developer.mozilla.org/en-US/docs/Web/API/WebVTT_API/Web_Video_Text_Tracks_Format)
  - [w3c/webvtt.js](https://github.com/w3c/webvtt.js)
  - [mozilla/vtt.js](https://github.com/mozilla/vtt.js)

### Gap Analysis from Research

| Category | WPT Coverage | Our Coverage | Gap Status |
|----------|-------------|--------------|------------|
| Header/Signature | Excellent | Not tested (low priority) | Deferred to EN-015 |
| Timestamps | Good | 7 tests | Covered |
| Voice Tags | **Poor** | 5 tests | **Addressed** |
| Tag Stripping | Limited | 3 tests | Covered |
| Multiline | Limited | 3 tests | Covered |
| Encoding | Good | 9 tests (5 UTF-8 + 4 fallback) | **Covered (TASK-107)** |

---

## Expansion Plan (EN-015 Sprint 4)

This infrastructure will be expanded in EN-015 to include:

| Artifact | EN-015 Task | Description |
|----------|-------------|-------------|
| Golden Dataset (3 meetings) | TASK-131 | Synthetic meetings with known entities |
| Human Annotations | TASK-131A | Ground truth for real VTT files |
| Ground Truth JSON | TASK-132 | Expected extraction results |
| Additional Edge Cases | TASK-133 | Header validation, SRT compatibility |
| Full parser-tests.yaml | TASK-134 | Complete test specification |
| extractor-tests.yaml | TASK-135 | ts-extractor test cases |
| formatter-tests.yaml | TASK-136 | ts-formatter test cases |
| integration-tests.yaml | TASK-137 | End-to-end pipeline tests |

---

## Usage

### For TASK-102 (VTT Processing Verification)

1. Read `validation/parser-tests.yaml` for test cases (vtt-001 through vtt-005)
2. Run ts-parser against `transcripts/real/internal-sample-sample.vtt`
3. Compare output against `expected/internal-sample-sample.expected.json`
4. Verify all assertions pass

### For Edge Case Testing

1. Review test cases vtt-006 through vtt-014 in `parser-tests.yaml`
2. Run ts-parser against files in `transcripts/edge_cases/`
3. Verify edge case handling per assertions

### For Future Tasks

- **TASK-103 (SRT):** Requires SRT test files (not yet created)
- **TASK-104 (Plain Text):** Requires plain text test files (not yet created)

---

## References

- [EN-007:DISC-002](../../../projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-002-implementation/EN-007-vtt-parser/EN-007--DISC-002-test-infrastructure-dependency.md) - Test Infrastructure Decision
- [EN-007:webvtt-research](../../../projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-002-implementation/EN-007-vtt-parser/research/webvtt-test-suite-research.md) - W3C WebVTT Test Suite Research
- [EN-015](../../../projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-002-implementation/EN-015-transcript-validation/EN-015-transcript-validation.md) - Full Test Infrastructure Enabler
- [TDD-ts-parser.md](../../../projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-parser.md) - Parser Design Specification
- [ts-parser.md](../agents/ts-parser.md) - Parser Agent Definition

---

*Test Data Version: 1.3.0*
*Constitutional Compliance: P-002 (persisted), P-004 (provenance)*
*EN-017: Large transcript golden dataset added 2026-01-28*
