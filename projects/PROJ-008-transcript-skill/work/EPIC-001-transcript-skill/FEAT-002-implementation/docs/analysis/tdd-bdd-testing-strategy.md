# TDD/BDD Testing Strategy for Transcript Skill

> **Created:** 2026-01-26
> **Author:** Claude
> **Status:** APPROVED
> **Parent:** FEAT-002
> **Related:** EN-015 (Validation & Test Cases)

---

## Purpose

This document defines the TDD/BDD testing strategy for FEAT-002 Transcript Skill implementation, specifically addressing:

1. **Golden Dataset Creation** - How to create ground truth without "dog fooding" (using agent output)
2. **Human-in-Loop Workflow** - Process for creating expected outputs from user's VTT files
3. **Test Pyramid Coverage** - Unit, Integration, E2E, and Contract testing
4. **Task Recommendations** - Additional testing tasks for enablers

---

## L0: The Problem (ELI5)

Imagine you're creating an answer key for a math test. You can't:
- Have students answer the test first, then use their answers as the key (dog fooding)
- Guess what the answers should be

You need a **teacher** (human expert) to work through the problems and create the answer key **before** giving the test to students.

For our transcript skill:
- **VTT Files** = The test questions (user has these)
- **Expected Output** = The answer key (needs to be created)
- **Agent** = The student taking the test (can't create its own answer key)
- **Human Expert** = The teacher creating ground truth

---

## L1: Human-in-Loop Ground Truth Creation

### Why Human-in-Loop?

| Approach | Problem | Risk |
|----------|---------|------|
| **Agent-Generated Ground Truth** | Circular validation - testing with own output | 100% false positive rate possible |
| **Automated Extraction** | No external oracle exists | Same problem as agent |
| **Human-in-Loop** | Human expert validates/creates | Gold standard accuracy |

### Ground Truth Creation Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    HUMAN-IN-LOOP GROUND TRUTH WORKFLOW                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  STEP 1: USER PROVIDES VTT FILES                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  User's Real VTT Files                                               │    │
│  │  - meeting-alpha.vtt (User's actual meeting)                         │    │
│  │  - meeting-beta.vtt  (User's actual meeting)                         │    │
│  │  - meeting-gamma.vtt (User's actual meeting)                         │    │
│  └────────────────────────────────┬────────────────────────────────────┘    │
│                                   │                                          │
│                                   ▼                                          │
│  STEP 2: HUMAN EXPERT ANNOTATION                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Human reads VTT and manually identifies:                            │    │
│  │                                                                       │    │
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐            │    │
│  │  │ Action Items  │  │  Decisions    │  │  Questions    │            │    │
│  │  │ - Who         │  │ - What        │  │ - Asked by    │            │    │
│  │  │ - What        │  │ - Decided by  │  │ - Answered?   │            │    │
│  │  │ - When        │  │ - Rationale   │  │ - Answer ref  │            │    │
│  │  │ - Source cue  │  │ - Source cue  │  │ - Source cue  │            │    │
│  │  └───────────────┘  └───────────────┘  └───────────────┘            │    │
│  │                                                                       │    │
│  │  ┌───────────────┐  ┌───────────────┐                                │    │
│  │  │   Speakers    │  │    Topics     │                                │    │
│  │  │ - Names       │  │ - Boundaries  │                                │    │
│  │  │ - Confidence  │  │ - Hierarchy   │                                │    │
│  │  └───────────────┘  └───────────────┘                                │    │
│  └────────────────────────────────┬────────────────────────────────────┘    │
│                                   │                                          │
│                                   ▼                                          │
│  STEP 3: CREATE EXPECTED.JSON                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  meeting-alpha.expected.json                                         │    │
│  │  {                                                                   │    │
│  │    "version": "1.0",                                                 │    │
│  │    "source": "meeting-alpha.vtt",                                    │    │
│  │    "annotated_by": "human_expert",                                   │    │
│  │    "annotation_date": "2026-01-27",                                  │    │
│  │    "action_items": [...],                                            │    │
│  │    "decisions": [...],                                               │    │
│  │    "questions": [...],                                               │    │
│  │    "speakers": [...],                                                │    │
│  │    "topics": [...]                                                   │    │
│  │  }                                                                   │    │
│  └────────────────────────────────┬────────────────────────────────────┘    │
│                                   │                                          │
│                                   ▼                                          │
│  STEP 4: VALIDATION (Tests can now run)                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                                                                       │    │
│  │  Agent Output         vs.        Expected.json (Ground Truth)        │    │
│  │  ─────────────                   ─────────────────────────────       │    │
│  │  {                               {                                   │    │
│  │    "action_items": [...]           "action_items": [...] ←── COMPARE │    │
│  │  }                               }                                   │    │
│  │                                                                       │    │
│  │  Calculate: Precision, Recall, F1 Score                              │    │
│  │                                                                       │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Annotation Guidelines for Human Expert

#### Action Item Identification Rules

| Signal | Confidence | Example |
|--------|------------|---------|
| "I will...", "I'll..." | HIGH (0.95) | "I'll send the report by Friday" |
| "Can you...", "Would you..." | HIGH (0.90) | "Can you review the PR?" |
| "Need to...", "Should..." | MEDIUM (0.75) | "We need to fix the bug" |
| "TODO:", "ACTION:" | HIGH (0.95) | "ACTION: Update docs" |

#### Decision Identification Rules

| Signal | Confidence | Example |
|--------|------------|---------|
| "We've decided...", "Decision:" | HIGH (0.95) | "We've decided to use React" |
| "Let's go with...", "Agreed:" | HIGH (0.90) | "Let's go with option B" |
| "So we'll..." (consensus) | MEDIUM (0.80) | "So we'll deploy Monday" |

#### Citation Requirements (PAT-004)

Every entity MUST have a citation linking to the source cue:
```json
{
  "id": "act-001",
  "text": "Send report by Friday",
  "citation": {
    "segment_id": "seg-042",
    "timestamp_ms": 930000,
    "text_snippet": "Bob, can you send me the report by Friday?"
  }
}
```

---

## L2: Test Pyramid Architecture

### Test Pyramid Overview

```
                    ┌─────────────────┐
                    │      E2E        │  ← Full pipeline (5%)
                    │   VTT → 8-file  │
                   ┌┴─────────────────┴┐
                   │    Integration    │  ← Agent-to-agent (15%)
                   │  Parser→Extractor │
                  ┌┴───────────────────┴┐
                  │      Contract       │  ← Schema validation (10%)
                  │  Input/Output JSON  │
                 ┌┴─────────────────────┴┐
                 │         Unit          │  ← Component logic (70%)
                 │ Patterns, Rules, Fns  │
                 └───────────────────────┘
```

### Test Level Definitions

#### Unit Tests (70%)

**What:** Test individual parsing rules, extraction patterns, and formatting functions.

**Examples:**
- Does `parse_vtt_timestamp()` handle all timestamp formats?
- Does `extract_action_items()` catch "I'll send..."?
- Does `count_tokens()` accurately estimate token count?

**Files:** Inline validation within agent prompts, test assertions in YAML specs.

#### Contract Tests (10%)

**What:** Verify that agent inputs and outputs match TDD-specified JSON schemas.

**Examples:**
- ts-parser output matches `CanonicalTranscript` schema
- ts-extractor output matches `ExtractionReport` schema
- ts-formatter output matches `8-file packet` structure

**Files:** `contract-tests.yaml` with JSON Schema validation

#### Integration Tests (15%)

**What:** Test data flow between agents.

**Examples:**
- ts-parser output → ts-extractor input (data compatibility)
- ts-extractor output → ts-formatter input (entity preservation)
- Context injection → All agents (context availability)

**Files:** `integration-tests.yaml`

#### End-to-End Tests (5%)

**What:** Complete pipeline from VTT input to 8-file packet output.

**Examples:**
- VTT file → All agents → 8-file packet with correct structure
- Large VTT → File splitting happens correctly
- Malformed VTT → Graceful degradation, partial results

**Files:** `e2e-tests.yaml`

---

## Test Specifications

### Contract Test Specification

```yaml
# test_data/validation/contract-tests.yaml
# Contract validation for agent input/output schemas
# Implements: Schema compliance per TDD documents

version: "1.0.0"
type: contract

contracts:
  ts-parser-output:
    description: "ts-parser output matches CanonicalTranscript schema"
    schema_ref: "schemas/canonical-transcript.json"
    tests:
      - id: con-par-001
        name: "Parser output has required fields"
        input: "golden/meeting-001.vtt"
        assertions:
          - type: json_schema_valid
            schema: "canonical-transcript.json"
          - type: required_fields
            expected: ["version", "source", "metadata", "segments"]

      - id: con-par-002
        name: "Segment structure is valid"
        assertions:
          - type: array_item_schema
            path: "$.segments"
            schema: "segment.json"

  ts-extractor-output:
    description: "ts-extractor output matches ExtractionReport schema"
    schema_ref: "schemas/extraction-report.json"
    tests:
      - id: con-ext-001
        name: "Extractor output has required fields"
        assertions:
          - type: json_schema_valid
            schema: "extraction-report.json"
          - type: required_fields
            expected: ["version", "source_transcript_id", "speakers", "action_items", "decisions", "questions", "topics"]

      - id: con-ext-002
        name: "All entities have citations (PAT-004)"
        assertions:
          - type: citation_present
            paths:
              - "$.action_items[*].citation"
              - "$.decisions[*].citation"
              - "$.questions[*].citation"

  ts-formatter-output:
    description: "ts-formatter output matches 8-file packet structure"
    tests:
      - id: con-fmt-001
        name: "8-file packet has all required files"
        assertions:
          - type: files_exist
            expected:
              - "00-index.md"
              - "01-summary.md"
              - "02-speakers.md"
              - "03-topics.md"
              - "04-entities.md"
              - "05-timeline.md"
              - "06-insights.md"
              - "07-visualization.md"

      - id: con-fmt-002
        name: "All files under 35K token limit"
        assertions:
          - type: token_count
            max: 35000
            apply_to: "all_files"
```

### Integration Test Specification

```yaml
# test_data/validation/integration-tests.yaml
# Integration tests for agent-to-agent data flow
# Implements: Pipeline continuity

version: "1.0.0"
type: integration

test_suites:
  parser-to-extractor:
    description: "ts-parser output compatible with ts-extractor input"
    tests:
      - id: int-001
        name: "Parser segments flow to extractor"
        pipeline:
          - agent: ts-parser
            input: "golden/meeting-001.vtt"
            capture: parser_output
          - agent: ts-extractor
            input: "${parser_output}"
            capture: extractor_output
        assertions:
          - type: no_data_loss
            description: "All segments from parser available to extractor"
          - type: speaker_preservation
            description: "Speaker names preserved through pipeline"

      - id: int-002
        name: "Timestamps preserved through pipeline"
        assertions:
          - type: timestamp_integrity
            description: "All timestamps match between parser and extractor output"

  extractor-to-formatter:
    description: "ts-extractor output compatible with ts-formatter input"
    tests:
      - id: int-003
        name: "All entity types flow to formatter"
        pipeline:
          - agent: ts-extractor
            input: "precalculated/canonical-001.json"
            capture: extractor_output
          - agent: ts-formatter
            input: "${extractor_output}"
            capture: formatter_output
        assertions:
          - type: entity_count_preserved
            entities: ["action_items", "decisions", "questions"]
          - type: citation_links_valid
            description: "All citations resolve in formatted output"

  context-injection:
    description: "Context injection available to all agents"
    tests:
      - id: int-004
        name: "Domain context loaded by agents"
        context:
          files:
            - "contexts/general.yaml"
            - "contexts/transcript.yaml"
        assertions:
          - type: context_available
            agents: ["ts-parser", "ts-extractor", "ts-formatter"]
```

### End-to-End Test Specification

```yaml
# test_data/validation/e2e-tests.yaml
# End-to-end tests for complete pipeline
# Implements: Full workflow validation

version: "1.0.0"
type: e2e

test_suites:
  happy_path:
    description: "Standard VTT processing workflows"
    tests:
      - id: e2e-001
        name: "Basic meeting VTT to 8-file packet"
        input: "golden/meeting-001.vtt"
        expected_output_structure:
          folder: "${session_id}-transcript-output/"
          files: 8
          index_valid: true
        ground_truth: "golden/meeting-001.expected.json"
        assertions:
          - type: precision
            entity: "action_items"
            minimum: 0.85
          - type: recall
            entity: "action_items"
            minimum: 0.80
          - type: files_created
            count: 8

      - id: e2e-002
        name: "Complex planning session"
        input: "golden/meeting-002.vtt"
        assertions:
          - type: handles_complexity
            speakers_min: 5
            topics_min: 4
          - type: all_entities_have_citations

  edge_cases:
    description: "Edge case handling"
    tests:
      - id: e2e-003
        name: "Large file triggers splitting"
        input: "edge_cases/large.vtt"
        assertions:
          - type: file_split_triggered
            reason: "token_limit"
          - type: all_splits_under_limit
            max_tokens: 35000

      - id: e2e-004
        name: "Malformed VTT graceful degradation"
        input: "edge_cases/malformed.vtt"
        assertions:
          - type: partial_success
            description: "Valid cues extracted despite errors"
          - type: error_logged
            level: "warning"
          - type: no_crash

      - id: e2e-005
        name: "Unicode content preserved"
        input: "edge_cases/unicode.vtt"
        assertions:
          - type: unicode_preserved
            characters: ["田中", "François", "Müller", "ß", "é"]
```

---

## Additional Tasks for Enablers

Based on the TDD/BDD strategy, the following tasks should be added to existing enablers:

### EN-007 (ts-parser): Add Contract Test Task

| Task ID | Title | Description | Blocked By |
|---------|-------|-------------|------------|
| TASK-105A | Create parser contract tests | Contract tests validating CanonicalTranscript schema compliance | TASK-101 |

### EN-008 (ts-extractor): Add Contract and Integration Test Tasks

| Task ID | Title | Description | Blocked By |
|---------|-------|-------------|------------|
| TASK-112A | Create extractor contract tests | Contract tests validating ExtractionReport schema compliance | TASK-106 |
| TASK-112B | Create parser-extractor integration tests | Integration tests for ts-parser → ts-extractor data flow | TASK-105A, TASK-112A |

### EN-016 (ts-formatter): Add Contract and E2E Test Tasks

| Task ID | Title | Description | Blocked By |
|---------|-------|-------------|------------|
| TASK-119A | Create formatter contract tests | Contract tests validating 8-file packet structure | TASK-113 |
| TASK-119B | Create extractor-formatter integration tests | Integration tests for ts-extractor → ts-formatter data flow | TASK-112A, TASK-119A |
| TASK-119C | Create end-to-end pipeline tests | E2E tests for complete VTT → 8-file packet workflow | TASK-137 |

### EN-015 (Validation): Add Human Ground Truth Task

| Task ID | Title | Description | Blocked By |
|---------|-------|-------------|------------|
| TASK-130A | Human-annotate user VTT files for ground truth | Create expected.json from user-provided VTT files via human annotation | User VTT files |

---

## Test Execution Sequence (TDD)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        TDD EXECUTION SEQUENCE                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PHASE 0: GROUND TRUTH CREATION (BEFORE ANY IMPLEMENTATION)                 │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  1. User provides VTT files                                          │    │
│  │  2. Human expert annotates entities                                  │    │
│  │  3. Create meeting-*.expected.json                                   │    │
│  │  4. Test specifications written (parser-tests.yaml, etc.)            │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                      │                                       │
│                                      ▼                                       │
│  PHASE 1: CONTRACT TESTS (RED)                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Write contract tests FIRST → They will FAIL (no implementation)     │    │
│  │  - Parser schema tests: FAIL                                         │    │
│  │  - Extractor schema tests: FAIL                                      │    │
│  │  - Formatter structure tests: FAIL                                   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                      │                                       │
│                                      ▼                                       │
│  PHASE 2: UNIT TESTS (RED → GREEN)                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  For each agent:                                                     │    │
│  │  1. Write unit tests → FAIL                                          │    │
│  │  2. Implement minimal code → PASS                                    │    │
│  │  3. Refactor → Still PASS                                            │    │
│  │  4. Contract tests → Start PASSING                                   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                      │                                       │
│                                      ▼                                       │
│  PHASE 3: INTEGRATION TESTS (RED → GREEN)                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  1. Write integration tests → FAIL                                   │    │
│  │  2. Fix data flow issues → PASS                                      │    │
│  │  3. Verify agent compatibility                                       │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                      │                                       │
│                                      ▼                                       │
│  PHASE 4: E2E TESTS (RED → GREEN)                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  1. Write E2E tests → FAIL                                           │    │
│  │  2. Fix pipeline issues → PASS                                       │    │
│  │  3. Measure precision/recall vs. ground truth                        │    │
│  │  4. Iterate until targets met                                        │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                      │                                       │
│                                      ▼                                       │
│  PHASE 5: GATE REVIEW                                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Present evidence:                                                   │    │
│  │  - All unit tests PASS                                               │    │
│  │  - All contract tests PASS                                           │    │
│  │  - All integration tests PASS                                        │    │
│  │  - E2E precision >= 85%, recall >= 80%                               │    │
│  │  - Human approves at GATE-5/GATE-6                                   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## User's VTT Files: Next Steps

To proceed with TDD/BDD:

1. **User Action:** Provide 2-3 real VTT files from actual meetings
2. **Human Annotation:** Work together to identify and annotate:
   - Action items (who, what, when, source timestamp)
   - Decisions (what, decided by, rationale, source timestamp)
   - Questions (asked by, answered?, answer reference, source timestamp)
   - Speakers (names, speaking segments)
   - Topics (boundaries, hierarchy)
3. **Create Ground Truth:** Generate `meeting-*.expected.json` files
4. **Write Tests First:** Create test specifications before implementation
5. **Implement to Pass:** Build agents to pass the tests

---

## References

- **NASA SE Process 7:** Verification ensures system meets requirements
- **BDD (Behavior-Driven Development):** [cucumber.io/docs/bdd](https://cucumber.io/docs/bdd/)
- **TDD (Test-Driven Development):** Kent Beck, "Test-Driven Development by Example"
- **Precision/Recall:** Information Retrieval evaluation metrics
- **PAT-004:** Citation-Required extraction pattern (anti-hallucination)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-26 | Claude | CREATED | Initial TDD/BDD strategy addressing user's dog fooding concern |
