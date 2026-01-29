# EN-015: Transcript Validation & Test Cases

<!--
TEMPLATE: Enabler
VERSION: 2.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
CREATED: 2026-01-26 per FEAT-002 restructuring
NOTE: Provides test transcripts and validation scenarios for transcript skill
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-01-26T17:30:00Z
> **Due:** TBD
> **Completed:**
> **Parent:** FEAT-002
> **Owner:** Claude
> **Target Sprint:** Sprint 4
> **Effort Points:** 5
> **Gate:** GATE-6 (Functionality Review)

---

## Summary

Create **test transcripts, validation scenarios, and acceptance criteria tests** for the transcript skill. This enabler provides the golden dataset and test cases needed to validate ts-parser, ts-extractor, and ts-formatter agents work correctly.

**Technical Justification:**
- Test-driven validation ensures agent quality (NASA SE Process 7)
- Golden dataset provides ground truth for extraction accuracy
- Multiple transcript formats (VTT, SRT, plain) verify parser robustness
- Edge cases validate error handling and graceful degradation

---

## Design Reference (L0/L1/L2)

### L0: The Driving Test Analogy

Test validation is like a **driving test** for transcript agents:

```
THE DRIVING TEST ANALOGY (Validation)
=====================================

        TEST COURSE                           DRIVING STUDENT
        (Test Transcripts)                    (Transcript Agents)
              │                                      │
              │                                      │
              ▼                                      ▼
    ┌────────────────────┐                ┌────────────────────┐
    │                    │                │                    │
    │  PARKING TEST      │                │    ts-parser       │
    │  ─────────────     │────────────────│  Can it read VTT?  │
    │  - VTT file        │   parse test   │  Can it read SRT?  │
    │  - SRT file        │                │  Handle errors?    │
    │  - Plain text      │                │                    │
    │                    │                └────────────────────┘
    │  HIGHWAY TEST      │                ┌────────────────────┐
    │  ────────────      │                │                    │
    │  - 10+ action items│────────────────│   ts-extractor     │
    │  - 5+ decisions    │   extract test │  Find all items?   │
    │  - 3+ questions    │                │  Correct assignees?│
    │  - 4+ speakers     │                │  Confidence OK?    │
    │                    │                └────────────────────┘
    │  CITY TEST         │                ┌────────────────────┐
    │  ─────────         │                │                    │
    │  - Long transcript │────────────────│   ts-formatter     │
    │  - >35K tokens     │   format test  │  Split correctly?  │
    │  - Complex links   │                │  Links resolve?    │
    │                    │                │  Under token limit?│
    └────────────────────┘                └────────────────────┘

    "We test each skill on a standardized course with known answers."
```

### L1: Validation Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Validation Test Architecture                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  test_data/                                                                  │
│  ├── transcripts/                    ← Test input files                      │
│  │   ├── golden/                     ← Golden dataset with ground truth      │
│  │   │   ├── meeting-001.vtt         ← WebVTT format                         │
│  │   │   ├── meeting-001.srt         ← SRT format (same content)             │
│  │   │   ├── meeting-001.txt         ← Plain text format                     │
│  │   │   └── meeting-001.expected.json ← Expected extraction results         │
│  │   ├── edge_cases/                 ← Edge case transcripts                 │
│  │   │   ├── empty.vtt               ← Empty file                            │
│  │   │   ├── malformed.vtt           ← Syntax errors                         │
│  │   │   ├── large.vtt               ← >35K tokens                           │
│  │   │   └── unicode.vtt             ← Non-ASCII characters                  │
│  │   └── format_samples/             ← Format-specific samples               │
│  │       ├── teams.vtt               ← MS Teams export                       │
│  │       ├── zoom.vtt                ← Zoom export                           │
│  │       └── otter.srt               ← Otter.ai export                       │
│  │                                                                           │
│  └── validation/                     ← Validation specifications             │
│      ├── parser-tests.yaml           ← ts-parser test cases                  │
│      ├── extractor-tests.yaml        ← ts-extractor test cases               │
│      ├── formatter-tests.yaml        ← ts-formatter test cases               │
│      └── integration-tests.yaml      ← End-to-end test cases                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### L2: Strategic Considerations

- **NASA SE Process 7:** Verification ensures system meets requirements
- **Golden Dataset:** Ground truth enables precision/recall measurement
- **Format Coverage:** VTT (60%), SRT (35%), Plain (5%) per TDD-ts-parser.md
- **Edge Case Handling:** Malformed input, encoding issues, large files
- **Regression Prevention:** Test cases prevent quality degradation
- **Acceptance Criteria Traceability:** Each test maps to AC from enablers

---

## Benefit Hypothesis

**We believe that** creating comprehensive test transcripts and validation scenarios

**Will result in** verifiable quality for transcript skill agents

**We will know we have succeeded when:**
- All test transcripts parse without errors
- Extraction accuracy meets precision/recall targets (>85%)
- Formatter outputs stay under 35K token limit
- All acceptance criteria have corresponding test cases
- Human approval received at GATE-5

---

## Acceptance Criteria

### Definition of Done

- [ ] Golden dataset created with ground truth annotations
- [ ] Edge case transcripts created for error handling
- [ ] Parser test cases cover VTT, SRT, plain text formats
- [ ] Extractor test cases cover all entity types
- [ ] Formatter test cases cover token limits and linking
- [ ] Integration tests validate end-to-end pipeline
- [ ] ps-critic review passed
- [ ] Human approval at GATE-5

### Technical Criteria

| # | Criterion | Source | Verified |
|---|-----------|--------|----------|
| AC-1 | At least 3 golden dataset transcripts | NASA SE | [ ] |
| AC-2 | VTT, SRT, and plain text formats covered | TDD-ts-parser | [ ] |
| AC-3 | Ground truth includes 10+ action items | TDD-ts-extractor | [ ] |
| AC-4 | Ground truth includes 5+ decisions | TDD-ts-extractor | [ ] |
| AC-5 | Edge cases cover malformed, empty, large files | PAT-002 | [ ] |
| AC-6 | Formatter tests verify <35K token output | ADR-002 | [ ] |
| AC-7 | Link resolution tests verify anchors work | ADR-003 | [ ] |
| AC-8 | All enabler ACs have corresponding tests | Quality | [ ] |

### End-to-End Pipeline Validation (EN-014 + EN-024 Coverage)

| # | Criterion | Source | Verified |
|---|-----------|--------|----------|
| AC-9 | Domain context files (EN-014) validated for all 8 domains | EN-014 | [ ] |
| AC-10 | Context injection loads correct schema per --context flag | EN-013 | [ ] |
| AC-11 | Mindmap pipeline (--mindmap flag) generates Mermaid output | EN-024 | [ ] |
| AC-12 | Mindmap pipeline (--mindmap flag) generates ASCII output | EN-024 | [ ] |
| AC-13 | Mindmap pipeline validates deep links per ADR-003 | EN-024 | [ ] |
| AC-14 | Pipeline works correctly without --mindmap (backward compatible) | EN-024 | [ ] |
| AC-15 | ps-critic validates mindmap output when present | EN-024 | [ ] |
| AC-16 | Full E2E test: VTT → Parser → Extractor → Formatter → Mindmap → Critic | E2E | [ ] |

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Owner | Effort | Blocked By |
|----|-------|--------|-------|--------|------------|
| [TASK-131](./TASK-131-golden-dataset-transcripts.md) | Create golden dataset transcripts (3 meetings) | pending | Claude | 2 | - |
| [TASK-131A](./TASK-131A-human-annotation-vtt.md) | **CRITICAL:** Human annotation of user VTT files | pending | Human | 3 | User VTT files |
| [TASK-132](./TASK-132-ground-truth-json.md) | Create ground truth JSON for golden dataset | pending | Claude | 2 | TASK-131 |
| [TASK-133](./TASK-133-edge-case-transcripts.md) | Create edge case transcripts (malformed, empty, large) | pending | Claude | 1 | - |
| [TASK-134](./TASK-134-parser-tests.md) | Create parser test specification (parser-tests.yaml) | pending | Claude | 1 | TASK-131 |
| [TASK-135](./TASK-135-extractor-tests.md) | Create extractor test specification | pending | Claude | 1 | TASK-132 |
| [TASK-136](./TASK-136-formatter-tests.md) | Create formatter test specification | pending | Claude | 1 | TASK-131 |
| [TASK-137](./TASK-137-integration-tests.md) | Create integration test specification | pending | Claude | 1 | TASK-134, TASK-135, TASK-136 |
| [TASK-138](./TASK-138-en008-deferred-findings.md) | EN-008 deferred minor findings | backlog | Claude | 1 | TASK-135, TASK-137 |

**NOTE:** Task IDs start at TASK-131 to continue from EN-014 (TASK-126-130).
**TASK-138 added:** 2026-01-28 per DEC-003:D-005 - Deferred minor findings from EN-008 GATE-5 review.
**TASK-131A added:** 2026-01-27 per TDD/BDD Testing Strategy - **Human annotation prevents "dog fooding" bias**.
**Task files created:** 2026-01-26 with detailed acceptance criteria and evidence requirements.

---

## Golden Dataset Specification

### Meeting 001: Team Standup

**Purpose:** Basic meeting with clear action items and decisions.

```
meeting-001 Golden Dataset
==========================

Duration: 15 minutes (900,000 ms)
Speakers: 4 (Alice, Bob, Carol, Dave)
Format: Available as .vtt, .srt, .txt

Expected Extractions:
─────────────────────
Action Items (5):
  - [act-001] Bob will send the report by Friday (assignee: Bob, due: Friday)
  - [act-002] Carol to review the API design (assignee: Carol)
  - [act-003] Dave needs to update the CI pipeline (assignee: Dave)
  - [act-004] Alice will schedule the planning meeting (assignee: Alice)
  - [act-005] Team to read the RFC before Thursday (assignee: Team)

Decisions (3):
  - [dec-001] Use React for the frontend (decided_by: Alice)
  - [dec-002] Deploy to AWS instead of GCP (decided_by: consensus)
  - [dec-003] Postpone the refactoring to next sprint (decided_by: Alice)

Questions (2):
  - [que-001] "How are we handling authentication?" (asked_by: Dave, answered: true)
  - [que-002] "Can we get more budget for testing?" (asked_by: Carol, answered: false)

Topics (3):
  - [top-001] Sprint Progress (00:00:30 - 00:05:00)
  - [top-002] Technical Decisions (00:05:00 - 00:10:00)
  - [top-003] Blockers and Questions (00:10:00 - 00:15:00)
```

### Meeting 002: Planning Session

**Purpose:** Longer meeting with complex discussions and multiple decision branches.

```
meeting-002 Golden Dataset
==========================

Duration: 45 minutes (2,700,000 ms)
Speakers: 6 (PM, Dev1, Dev2, QA, Designer, Stakeholder)
Format: Available as .vtt, .srt, .txt

Expected Extractions:
─────────────────────
Action Items (12):
  - [act-001] through [act-012] with various assignees

Decisions (7):
  - [dec-001] through [dec-007] including one with explicit rationale

Questions (5):
  - [que-001] through [que-005] mix of answered and unanswered

Topics (5):
  - [top-001] through [top-005] including overlapping segments
```

### Meeting 003: Edge Case Meeting

**Purpose:** Contains edge cases like mid-meeting joins, unclear speakers, overlapping speech.

```
meeting-003 Golden Dataset
==========================

Duration: 20 minutes
Speakers: Initially 3, then 5 (2 join late)
Format: Available as .vtt only (tests format-specific edge cases)

Edge Cases:
───────────
- Speaker joins at 00:07:30 (mid-meeting)
- Overlapping speech at 00:12:00-00:12:30
- Unclear speaker attribution at 00:15:00
- Correction of previous statement at 00:18:00
- Action item assigned to absent person
```

---

## Edge Case Transcripts

### empty.vtt

```vtt
WEBVTT

```

**Expected Behavior:** Parser returns empty segments array, no errors.

### malformed.vtt

```vtt
WEBVTT

00:00:01.000 --> 00:00:05
Missing end timestamp

--> 00:00:10.000
Missing start timestamp

00:00:15.000 --> 00:00:10.000
End before start

not-a-timestamp
Random text without cue
```

**Expected Behavior:** Parser logs warnings, continues with valid cues (PAT-002: Defensive Parsing).

### large.vtt

**Specifications:**
- Duration: 2 hours
- Token count: ~50,000 tokens (forces splitting)
- Segments: 500+

**Expected Behavior:** Formatter splits into multiple files per ADR-004.

### unicode.vtt

```vtt
WEBVTT

00:00:01.000 --> 00:00:05.000
<v 田中さん>おはようございます。

00:00:05.000 --> 00:00:10.000
<v François>Bonjour à tous! 🎉

00:00:10.000 --> 00:00:15.000
<v Müller>Guten Morgen! ß é ü ö
```

**Expected Behavior:** Parser handles UTF-8 correctly, preserves all characters.

---

## Test Specification Format

### parser-tests.yaml Structure

```yaml
# test_data/validation/parser-tests.yaml
# Parser validation test cases
# Implements: FR-001, FR-002, FR-003, FR-004

version: "1.0.0"
agent: ts-parser

test_suites:
  vtt_parsing:
    description: "WebVTT format parsing tests"
    tests:
      - id: vtt-001
        name: "Parse basic VTT with voice tags"
        input: "transcripts/golden/meeting-001.vtt"
        assertions:
          - type: segment_count
            expected: 45
          - type: speaker_detected
            expected: ["Alice", "Bob", "Carol", "Dave"]
          - type: format_detected
            expected: "vtt"
          - type: no_errors

      - id: vtt-002
        name: "Parse VTT with missing voice tags"
        input: "transcripts/edge_cases/no-voice-tags.vtt"
        assertions:
          - type: speaker_fallback
            expected: "contextual"
          - type: warnings
            expected_count: ">0"

  srt_parsing:
    description: "SubRip format parsing tests"
    tests:
      - id: srt-001
        name: "Parse SRT with comma timestamps"
        input: "transcripts/format_samples/zoom.srt"
        assertions:
          - type: timestamp_format
            expected: "comma"
          - type: no_errors

      - id: srt-002
        name: "Parse SRT with period timestamps"
        input: "transcripts/format_samples/otter.srt"
        assertions:
          - type: timestamp_format
            expected: "period"
          - type: no_errors

  plain_text_parsing:
    description: "Plain text format parsing tests"
    tests:
      - id: txt-001
        name: "Parse plain text with speaker prefixes"
        input: "transcripts/golden/meeting-001.txt"
        assertions:
          - type: speaker_pattern
            expected: "prefix"

  error_handling:
    description: "Error handling and edge cases"
    tests:
      - id: err-001
        name: "Handle empty file gracefully"
        input: "transcripts/edge_cases/empty.vtt"
        assertions:
          - type: segments
            expected: []
          - type: no_errors

      - id: err-002
        name: "Handle malformed VTT with partial recovery"
        input: "transcripts/edge_cases/malformed.vtt"
        assertions:
          - type: partial_recovery
            expected: true
          - type: warnings
            expected_count: ">0"
```

### extractor-tests.yaml Structure

```yaml
# test_data/validation/extractor-tests.yaml
# Extractor validation test cases
# Implements: FR-005, FR-006, FR-007, FR-008, FR-009

version: "1.0.0"
agent: ts-extractor

test_suites:
  action_item_extraction:
    description: "Action item extraction tests"
    tests:
      - id: act-001
        name: "Extract action items from golden dataset"
        input: "transcripts/golden/meeting-001.vtt"
        ground_truth: "transcripts/golden/meeting-001.expected.json"
        assertions:
          - type: precision
            entity: "action_item"
            minimum: 0.85
          - type: recall
            entity: "action_item"
            minimum: 0.80
          - type: entity_count
            entity: "action_item"
            expected: 5

      - id: act-002
        name: "Extract assignee correctly"
        input: "transcripts/golden/meeting-001.vtt"
        assertions:
          - type: field_accuracy
            entity: "action_item"
            field: "assignee"
            minimum: 0.90

  decision_extraction:
    description: "Decision extraction tests"
    tests:
      - id: dec-001
        name: "Extract decisions with high confidence"
        input: "transcripts/golden/meeting-001.vtt"
        assertions:
          - type: confidence_threshold
            entity: "decision"
            minimum: 0.80
          - type: entity_count
            entity: "decision"
            expected: 3

  speaker_identification:
    description: "Speaker identification tests (PAT-003)"
    tests:
      - id: spk-001
        name: "Identify speakers from VTT voice tags"
        input: "transcripts/golden/meeting-001.vtt"
        assertions:
          - type: speaker_accuracy
            minimum: 0.95
          - type: speaker_count
            expected: 4

  citation_validation:
    description: "Citation anti-hallucination tests (PAT-004)"
    tests:
      - id: cite-001
        name: "All extractions have valid citations"
        input: "transcripts/golden/meeting-001.vtt"
        assertions:
          - type: citation_coverage
            expected: 1.0  # 100% of extractions must have citations
          - type: citation_validity
            expected: true  # All citations resolve to real segments
```

---

## Validation Metrics

### Precision/Recall Targets

| Entity Type | Precision Target | Recall Target | Source |
|-------------|------------------|---------------|--------|
| Action Item | >= 0.85 | >= 0.80 | TDD-ts-extractor |
| Decision | >= 0.85 | >= 0.75 | TDD-ts-extractor |
| Question | >= 0.80 | >= 0.70 | TDD-ts-extractor |
| Speaker | >= 0.90 | >= 0.95 | PAT-003 |
| Topic | >= 0.75 | >= 0.70 | FR-009 |

### Formula

```
Precision = True Positives / (True Positives + False Positives)
Recall = True Positives / (True Positives + False Negatives)
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

---

## File Location

```
projects/PROJ-008-transcript-skill/
└── test_data/
    ├── transcripts/
    │   ├── golden/
    │   │   ├── meeting-001.vtt
    │   │   ├── meeting-001.srt
    │   │   ├── meeting-001.txt
    │   │   ├── meeting-001.expected.json
    │   │   ├── meeting-002.vtt
    │   │   ├── meeting-002.expected.json
    │   │   ├── meeting-003.vtt
    │   │   └── meeting-003.expected.json
    │   ├── edge_cases/
    │   │   ├── empty.vtt
    │   │   ├── malformed.vtt
    │   │   ├── large.vtt
    │   │   └── unicode.vtt
    │   └── format_samples/
    │       ├── teams.vtt
    │       ├── zoom.vtt
    │       └── otter.srt
    └── validation/
        ├── parser-tests.yaml
        ├── extractor-tests.yaml
        ├── formatter-tests.yaml
        └── integration-tests.yaml
```

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-002: Implementation](../FEAT-002-implementation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | EN-007 | Parser tests validate ts-parser |
| Depends On | EN-008 | Extractor tests validate ts-extractor |
| Depends On | EN-009 | Mindmap agents to validate (ts-mindmap-mermaid, ts-mindmap-ascii) |
| Depends On | EN-014 | Domain schemas used in context tests |
| Depends On | EN-016 | Formatter tests validate ts-formatter |
| Depends On | EN-024 | Mindmap pipeline integration tests (--mindmap flag validation) |
| References | TDD-ts-parser.md | Parser requirements to test |
| References | TDD-ts-extractor.md | Extractor requirements to test |
| References | TDD-ts-formatter.md | Formatter requirements to test |
| References | ADR-002 | Token limits to verify |
| References | ADR-003 | Link resolution to verify |
| References | ADR-006 | Mindmap integration decision (to be created by EN-024) |
| References | PAT-002 | Defensive parsing to verify |
| References | PAT-003 | Speaker detection to verify |
| References | PAT-004 | Citation requirement to verify |

---

## TDD/BDD Testing Strategy

**See:** [TDD/BDD Testing Strategy](../docs/analysis/tdd-bdd-testing-strategy.md)

This enabler follows the TDD/BDD approach with:
- **Human-in-Loop Ground Truth Creation** - No "dog fooding"
- **Test Pyramid** - Unit (70%), Contract (10%), Integration (15%), E2E (5%)
- **Additional Testing Tasks** - Contract and integration tests for EN-007, EN-008, EN-016

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-26 | Claude | pending | Enabler created per FEAT-002 restructuring |
| 2026-01-26 | Claude | pending | TDD/BDD testing strategy document created with human-in-loop ground truth approach |
| 2026-01-27 | Claude | revised | Added TASK-131A (human annotation) per TDD/BDD Testing Strategy - prevents "dog fooding" bias |
| 2026-01-28 | Claude | revised | Added TASK-138 (EN-008 deferred findings) per DEC-003:D-005 |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Product Backlog Item (tagged Testing) |
| **SAFe** | Enabler Story |
| **JIRA** | Task |
