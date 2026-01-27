# Transcript Skill Test Data

> **Version:** 1.0.0
> **Created:** 2026-01-27
> **Source:** EN-007:DISC-002 (Test Infrastructure Dependency Gap Resolution)
> **Review Status:** PENDING_HUMAN_REVIEW

---

## Purpose

This directory contains test data and validation specifications for the transcript skill agents (ts-parser, ts-extractor, ts-formatter).

**Design Principle:** Self-contained within the skill directory per EN-007:DISC-002 decision.

---

## Directory Structure

```
test_data/
├── README.md                          ← This file
├── transcripts/                       ← Test input files
│   ├── real/                          ← Real VTT files from users (TASK-131A)
│   │   └── internal-sample-sample.vtt
│   ├── golden/                        ← Synthetic golden dataset (EN-015)
│   │   └── (placeholder for 3 meetings)
│   └── edge_cases/                    ← Edge case files (EN-015)
│       └── (placeholder for malformed, empty, large, unicode)
├── expected/                          ← Expected parser outputs
│   └── internal-sample-sample.expected.json
└── validation/                        ← Test specifications
    └── parser-tests.yaml              ← ts-parser test cases
```

---

## Current Contents (Minimal - DISC-002)

### Real Transcript Sample

| File | Source | Cues | Speakers | Purpose |
|------|--------|------|----------|---------|
| `transcripts/real/internal-sample-sample.vtt` | User VTT (first 20 cues) | 20 | 2 (Adam Nowak, Brendan Bennett) | VTT parsing verification |

### Expected Output

| File | Source | Purpose |
|------|--------|---------|
| `expected/internal-sample-sample.expected.json` | Derived from VTT (deterministic) | Golden output for comparison |

### Test Specifications

| File | Agent | Test Count | Status |
|------|-------|------------|--------|
| `validation/parser-tests.yaml` | ts-parser | 5 VTT tests + placeholders | PENDING_HUMAN_REVIEW |

---

## Review Status

**IMPORTANT:** The expected output JSON was derived deterministically from the VTT file. Human review is required before using for verification.

### Items Requiring Human Review

1. **internal-sample-sample.expected.json**
   - Verify speaker names extracted correctly
   - Verify timestamps converted to milliseconds correctly
   - Verify multi-line text joined correctly
   - Verify closing `</v>` tags stripped

2. **parser-tests.yaml**
   - Verify test assertions match acceptance criteria
   - Confirm test coverage is adequate for TASK-102

---

## Expansion Plan (EN-015 Sprint 4)

This minimal infrastructure will be expanded in EN-015 to include:

| Artifact | EN-015 Task | Description |
|----------|-------------|-------------|
| Golden Dataset (3 meetings) | TASK-131 | Synthetic meetings with known entities |
| Human Annotations | TASK-131A | Ground truth for real VTT files |
| Ground Truth JSON | TASK-132 | Expected extraction results |
| Edge Case Files | TASK-133 | malformed.vtt, empty.vtt, large.vtt, unicode.vtt |
| Full parser-tests.yaml | TASK-134 | Complete test specification |
| extractor-tests.yaml | TASK-135 | ts-extractor test cases |
| formatter-tests.yaml | TASK-136 | ts-formatter test cases |
| integration-tests.yaml | TASK-137 | End-to-end pipeline tests |

---

## Usage

### For TASK-102 (VTT Processing Verification)

1. Read `validation/parser-tests.yaml` for test cases
2. Run ts-parser against `transcripts/real/internal-sample-sample.vtt`
3. Compare output against `expected/internal-sample-sample.expected.json`
4. Verify all assertions pass

### For Future Tasks

- **TASK-103 (SRT):** Requires SRT test files (not yet created)
- **TASK-104 (Plain Text):** Requires plain text test files (not yet created)

---

## References

- [EN-007:DISC-002](../../../projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-002-implementation/EN-007-vtt-parser/EN-007--DISC-002-test-infrastructure-dependency.md) - Test Infrastructure Decision
- [EN-015](../../../projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-002-implementation/EN-015-transcript-validation/EN-015-transcript-validation.md) - Full Test Infrastructure Enabler
- [TDD-ts-parser.md](../../../projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-parser.md) - Parser Design Specification
- [ts-parser.md](../agents/ts-parser.md) - Parser Agent Definition

---

*Test Data Version: 1.0.0*
*Constitutional Compliance: P-002 (persisted), P-004 (provenance)*
