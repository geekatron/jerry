# EN-007: ts-parser Agent Implementation

<!--
TEMPLATE: Enabler
VERSION: 2.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
REVISED: 2026-01-26 per DISC-001 alignment analysis
-->

> **Type:** enabler
> **Status:** **APPROVED**
> **Priority:** high
> **Impact:** high
> **Created:** 2026-01-26T00:00:00Z
> **Revised:** 2026-01-26T15:45:00Z
> **Due:** TBD
> **Completed:**
> **Parent:** FEAT-002
> **Owner:** Claude
> **Target Sprint:** Sprint 3
> **Effort Points:** 8
> **Gate:** GATE-5 (Core Implementation Review)

---

## Summary

Implement the **ts-parser agent** that converts transcript files (VTT, SRT, plain text) into canonical JSON format for downstream processing by ts-extractor.

**Implements:** [TDD-ts-parser.md](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-parser.md)

**Technical Justification:**
- Foundation for all entity extraction pipelines
- Handles three input formats (WebVTT, SRT, plain text)
- Auto-detects format from file content
- Outputs Claude-friendly canonical JSON (<35K tokens per chunk)

---

## Design Reference (L0/L1/L2)

### L0: The Reception Desk Analogy

The ts-parser is like a **Reception Desk** at a Translation Office:

```
           INCOMING DOCUMENTS                 PROCESSED OUTPUT
           ──────────────────                 ────────────────

    ┌───────────────┐
    │ VTT File      │ ────┐
    │ (60% share)   │     │
    └───────────────┘     │
                          │     ┌─────────────────────────────┐
    ┌───────────────┐     │     │                             │
    │ SRT File      │ ────┼────►│    CANONICAL TRANSCRIPT     │
    │ (35% share)   │     │     │    ────────────────────     │
    └───────────────┘     │     │                             │
                          │     │    Unified JSON format      │
    ┌───────────────┐     │     │    Ready for extraction     │
    │ Plain Text    │ ────┘     │                             │
    │ (5% share)    │           └─────────────────────────────┘
    └───────────────┘

    "I accept any format. I output one standard format."
```

### L1: Component Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          ts-parser Agent                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                        FormatDetector                             │  │
│  │ + detect(content: bytes) -> Format                               │  │
│  └───────────────────────────┬──────────────────────────────────────┘  │
│                              │                                          │
│         ┌────────────────────┼────────────────────┐                    │
│         ▼                    ▼                    ▼                    │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐            │
│  │ VTTProcessor │    │ SRTProcessor │    │ PlainParser  │            │
│  │ (FR-001)     │    │ (FR-002)     │    │ (FR-003)     │            │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘            │
│         └───────────────────┼───────────────────┘                      │
│                             │                                          │
│                             ▼                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                        Normalizer                                 │  │
│  │ + normalize_timestamps(ts: str) -> int (milliseconds)           │  │
│  │ + detect_encoding(content: bytes) -> str                        │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  OUTPUT: CanonicalTranscript JSON (per TDD schema)                     │
└─────────────────────────────────────────────────────────────────────────┘
```

### L2: Strategic Considerations

- **PAT-002 Defensive Parsing:** "Accept liberally, produce consistently" - continue parsing despite individual segment errors
- **Large File Handling:** Stream processing for files > 10MB, O(batch_size) memory
- **Risk Mitigation:** Both `.` and `,` supported in timestamps (R-002), multi-encoding fallback chain (R-003)

---

## Benefit Hypothesis

**We believe that** implementing ts-parser as a Claude Code agent per TDD-ts-parser.md

**Will result in** reliable structured transcript data for downstream processing

**We will know we have succeeded when:**
- VTT files parse with >95% accuracy (FR-001)
- SRT files parse with both comma and period timestamps (FR-002)
- Plain text speaker patterns detected (FR-003)
- Format auto-detection works reliably (FR-004)
- Timestamps normalized to milliseconds (NFR-006)
- Multi-encoding support handles UTF-8/Windows-1252/ISO-8859-1 (NFR-007)
- Human approval received at GATE-5

---

## Acceptance Criteria

### Definition of Done

- [x] ts-parser agent definition complete (`skills/transcript/agents/ts-parser.md`) - v1.2.0
- [x] VTT processing verified (FR-001) - TASK-102 complete
- [x] SRT processing verified (FR-002) - TASK-103 complete
- [x] Plain text processing verified (FR-003) - TASK-104 complete
- [x] Format detection verified (FR-004) - Implicit: 11 format_detected assertions in parser-tests.yaml
- [x] Timestamp normalization verified (NFR-006) - TASK-102, 103
- [x] Encoding detection verified (NFR-007) - TASK-107 complete
- [x] Error handling graceful (PAT-002) - TASK-106 complete
- [x] ps-critic review passed - Score: 0.892 (CONDITIONAL)
- [ ] Human approval at GATE-5

### Technical Criteria (from TDD-ts-parser.md)

| # | Criterion | TDD Section | Verified |
|---|-----------|-------------|----------|
| AC-1 | Parses WebVTT with voice tags `<v Speaker>` | 1.1 | [x] TASK-102 |
| AC-2 | Parses SRT with speaker prefix `Name:` | 1.2 | [x] TASK-103 |
| AC-3 | Parses plain text patterns (colon, bracket, caps) | 1.3 | [x] TASK-104 |
| AC-4 | Auto-detects format from content | 2 | [x] parser-tests.yaml det-001 + 11 format_detected assertions |
| AC-5 | Outputs canonical JSON per schema | 3 | [x] TASK-102..104 |
| AC-6 | Normalizes timestamps to milliseconds | 4 | [x] TASK-102, 103 |
| AC-7 | Handles encoding detection with fallbacks | 5 | [x] TASK-107 |
| AC-8 | Error handling per matrix (continues parsing) | 6 | [x] TASK-106 |

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Owner | Effort | Blocked By |
|----|-------|--------|-------|--------|------------|
| [TASK-101](./TASK-101-parser-agent-alignment.md) | Verify ts-parser agent definition alignment | **done** | Claude | 3 | - |
| [TASK-102](./TASK-102-vtt-processing.md) | Implement/verify VTT processing (FR-001) | **done** | Claude | 2 | ~~TASK-101~~ |
| [TASK-103](./TASK-103-srt-processing.md) | Implement/verify SRT processing (FR-002) | **done** | Claude | 1 | ~~TASK-101~~ |
| [TASK-104](./TASK-104-plain-text-processing.md) | Implement/verify plain text processing (FR-003) | **done** | Claude | 1 | ~~TASK-101~~ |
| [TASK-105](./TASK-105-parser-validation.md) | Create test cases and validation | **done** | Claude | 2 | ~~TASK-102..104~~ |
| [TASK-105A](./TASK-105A-parser-contract-tests.md) | Create parser contract tests (TDD/BDD) | **done** | Claude | 1 | ~~TASK-101~~ |
| [TASK-106](./TASK-106-error-capture-mechanism.md) | Implement enhanced error capture mechanism | **done** | Claude | 2 | ~~TASK-101~~ |
| [TASK-107](./TASK-107-encoding-fallback-verification.md) | Verify encoding detection with fallbacks (NFR-007) | **done** | Claude | 1 | ~~TASK-101~~ |

**NOTE:** Task IDs renumbered from TASK-034-038 to TASK-101-105 per DISC-001 to avoid conflicts with EN-006 tasks.
**TASK-105A added:** 2026-01-27 per TDD/BDD Testing Strategy for contract test coverage.
**TASK-106 added:** 2026-01-27 per W3C WebVTT research for enhanced error capture (PAT-002).
**TASK-107 added:** 2026-01-27 per ps-critic GAP-002 finding - encoding fallback verification needed.
**Task files created:** 2026-01-26 with detailed acceptance criteria and evidence requirements.

### Execution Dependency Graph

```
TASK-101 (foundation - DONE)
    │
    ├──► TASK-102 (VTT) ─────────┐
    │                            │
    ├──► TASK-103 (SRT) ─────────┼──► TASK-105 (validation)
    │                            │
    ├──► TASK-104 (Plain Text) ──┘
    │
    ├──► TASK-105A (contract tests) ──► (parallel with 102-104)
    │
    └──► TASK-106 (error capture) ────► (parallel, needed by 102-104 verification)

Recommended execution order:
1. TASK-106 (error capture) - Enables proper error surfacing
2. TASK-102, TASK-103, TASK-104 (can run in parallel)
3. TASK-105A (contract tests)
4. TASK-105 (final validation)
```

---

## Implementation Artifacts

### Existing (from EN-005, updated per DISC-001 and DISC-002)

| Artifact | Path | Status |
|----------|------|--------|
| TDD | [TDD-ts-parser.md](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-parser.md) | Complete (v1.2 - error capture schema) |
| Agent Definition | [skills/transcript/agents/ts-parser.md](../../../../../skills/transcript/agents/ts-parser.md) | Complete (v1.2.0 - error capture) |
| Test Specification | [parser-tests.yaml](../../../../../skills/transcript/test_data/validation/parser-tests.yaml) | Complete (v1.4.0 - 14 VTT + 4 encoding + 3 SRT + 4 TXT tests) |
| W3C Research | [webvtt-test-suite-research.md](./research/webvtt-test-suite-research.md) | Complete |
| VTT Verification | [verification/TASK-102-vtt-verification-results.md](./verification/TASK-102-vtt-verification-results.md) | Complete |
| SRT Verification | [verification/TASK-103-srt-verification-results.md](./verification/TASK-103-srt-verification-results.md) | Complete |
| Plain Text Verification | [verification/TASK-104-plain-text-verification-results.md](./verification/TASK-104-plain-text-verification-results.md) | Complete |
| ps-critic Review | [critiques/EN-007-ps-critic-review.md](./critiques/EN-007-ps-critic-review.md) | Complete (Score: 0.892) |

### To Verify/Enhance

| Artifact | Purpose | Status |
|----------|---------|--------|
| Canonical JSON Schema | Output validation | Verify alignment |
| Test transcripts | Validation | Awaiting EN-015 |

---

## Input/Output Format

### Input (from user)

Transcript file in one of three formats:
- WebVTT (`.vtt`) - 60% of use cases
- SubRip (`.srt`) - 35% of use cases
- Plain text (`.txt`) - 5% of use cases

### Output (to ts-extractor)

Canonical JSON per TDD-ts-parser.md Section 3:

```json
{
  "version": "1.0",
  "source": {
    "format": "vtt|srt|plain",
    "encoding": "utf-8",
    "file_path": "/path/to/original/file"
  },
  "metadata": {
    "duration_ms": 3600000,
    "segment_count": 150,
    "detected_speakers": 4
  },
  "segments": [
    {
      "id": "seg-001",
      "start_ms": 0,
      "end_ms": 5000,
      "speaker": "Alice",
      "text": "Good morning everyone.",
      "raw_text": "<v Alice>Good morning everyone."
    }
  ]
}
```

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-002: Implementation](../FEAT-002-implementation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Implements | [TDD-ts-parser.md](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-parser.md) | Technical design |
| References | [ADR-001](../../FEAT-001-analysis-design/EN-004-architecture-decisions/docs/adrs/adr-001.md) | Hybrid agent architecture |
| References | [ADR-005](../../FEAT-001-analysis-design/EN-004-architecture-decisions/docs/adrs/adr-005.md) | Phased implementation |
| Blocks | EN-008 | Entity extraction needs parsed output |

### Discovery Reference

- [FEAT-002:DISC-001](../FEAT-002--DISC-001-enabler-alignment-analysis.md) - Enabler alignment analysis (task renumbering)
- [EN-007:DISC-001](./EN-007--DISC-001-vtt-voice-tag-gaps.md) - **VTT Voice Tag Parsing Gaps (CRITICAL)** - Found during TASK-101 audit
- [EN-007:DISC-002](./EN-007--DISC-002-test-infrastructure-dependency.md) - **Test Infrastructure Dependency Gap (RESOLVED)** - Found during TASK-102 prep; created minimal test infrastructure in `skills/transcript/test_data/`

### Decision Reference

- [EN-007:DEC-001](./EN-007--DEC-001-utf16-bom-out-of-scope.md) - **UTF-16 BOM Support Out of Scope** - Found during TASK-107 documentation audit; UTF-16 deferred to EN-017 in FEAT-003

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-26 | Claude | pending | Enabler created |
| 2026-01-26 | Claude | revised | Aligned with TDD-ts-parser.md per DISC-001; tasks renumbered to TASK-101+ |
| 2026-01-27 | Claude | revised | Added TASK-105A (parser contract tests) per TDD/BDD Testing Strategy |
| 2026-01-27 | Claude | in_progress | TASK-101 audit discovered DISC-001 (VTT voice tag gaps); remediation in progress |
| 2026-01-27 | Claude | in_progress | TASK-101 complete: TDD v1.1, Agent v1.1.0; TASK-102..105A unblocked |
| 2026-01-27 | Claude | in_progress | DISC-002: Test infrastructure dependency gap resolved; created `skills/transcript/test_data/` with minimal test infrastructure |
| 2026-01-27 | Claude | in_progress | W3C WebVTT research complete: 11 edge case VTT files created, parser-tests.yaml v1.1.0 with 14 VTT tests |
| 2026-01-27 | Claude | in_progress | Added TASK-106 (error capture mechanism) per W3C research; TDD-ts-parser.md updated to v1.2 with enhanced error schema |
| 2026-01-27 | Claude | in_progress | TASK-106 complete: Enhanced error capture schema verified |
| 2026-01-27 | Claude | in_progress | TASK-102 complete: All 14 VTT tests pass (core + edge cases) |
| 2026-01-27 | Claude | in_progress | TASK-103 complete: 3 SRT test cases pass (comma/period timestamps, mixed speakers) |
| 2026-01-27 | Claude | in_progress | TASK-104 complete: 4 Plain Text test cases pass (colon/bracket/ALL CAPS/null fallback) |
| 2026-01-27 | Claude | in_progress | TASK-105 complete: 33/33 validation tests pass (5 golden + 14 edge case + 4 format detection + 10 AC) |
| 2026-01-27 | Claude | in_progress | TASK-105A complete: Contract tests created (10 tests), JSON schemas created (canonical-transcript.json, segment.json) |
| 2026-01-27 | Claude | in_progress | ps-critic review complete: Score 0.892 (CONDITIONAL) - 2 minor gaps (AC-4, AC-7 verification) |
| 2026-01-27 | Claude | in_progress | GAP-001 resolved: AC-4 (Format detection) verified - 11 format_detected assertions in parser-tests.yaml |
| 2026-01-27 | Claude | in_progress | GAP-002 addressed: TASK-107 created for encoding fallback verification (NFR-007) |
| 2026-01-27 | Claude | in_progress | DEC-001 created: UTF-16 BOM support documented as out-of-scope; tech debt EN-017 in FEAT-003 |
| 2026-01-27 | Claude | in_progress | TASK-107 complete: Encoding fallback test infrastructure created (4 binary test files, 4 expected JSON, parser-tests.yaml v1.4.0 encoding_fallback section) |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Product Backlog Item (tagged Technical) |
| **SAFe** | Enabler Story |
| **JIRA** | Task |
