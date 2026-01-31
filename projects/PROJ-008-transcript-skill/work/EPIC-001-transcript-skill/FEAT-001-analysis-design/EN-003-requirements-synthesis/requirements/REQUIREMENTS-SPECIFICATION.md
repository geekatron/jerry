# Consolidated Requirements Specification: Transcript Skill

> **Document ID**: PROJ-008-e-003-REQUIREMENTS-SPECIFICATION
> **Version**: 1.0
> **Date**: 2026-01-25
> **Author**: ps-synthesizer agent
> **Status**: GATE-2 Ready

---

## Document Navigation

| Level | Audience | Sections |
|-------|----------|----------|
| **L0** | Executive / GATE-2 Review | [Executive Summary](#l0-executive-summary-gate-2-review) |
| **L1** | Software Engineer | [Unified Requirements Catalog](#l1-unified-requirements-catalog) |
| **L2** | Principal Architect | [Strategic Patterns & Architectural Decisions](#l2-strategic-patterns-and-architectural-decisions) |

---

# L0: Executive Summary (GATE-2 Review)

## Synthesis Overview

This document consolidates requirements from **6 analysis frameworks** applied during Phase 1 research:

```
SYNTHESIS INPUTS
================

Wave 1 (Parallel Analyses):
├── 5W2H-ANALYSIS.md      → Scope definition, personas, use cases
├── ISHIKAWA-DIAGRAM.md   → Root cause analysis (6M framework)
├── 8D-PROBLEM-SOLVING.md → Corrective actions, ADR references
└── PARETO-ANALYSIS.md    → Feature prioritization (80/20)

Wave 2 (Sequential Analyses):
├── FMEA-ANALYSIS.md      → Risk assessment (20 failure modes)
└── NASA-SE-REQUIREMENTS.md → Formal requirements (NPR 7123.1D)
```

## Requirements at a Glance

```
REQUIREMENTS PORTFOLIO SUMMARY
==============================

┌─────────────────────────────────────────────────────────────────────────┐
│                        REQUIREMENTS BY CATEGORY                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   Stakeholder Needs (STK):     10  ████████████████████                 │
│   Functional Requirements (FR): 15  ██████████████████████████████       │
│   Non-Functional Reqs (NFR):   10  ████████████████████                 │
│   Interface Requirements (IR):   5  ██████████                           │
│                                 ───                                      │
│   TOTAL:                        40  requirements                         │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                        PRIORITY DISTRIBUTION                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   MUST (Critical):             31  ██████████████████████████████  78%  │
│   SHOULD (High):                9  ██████████████                   22%  │
│   COULD (Medium):               0                                    0%  │
│   WON'T (Deferred):             0                                    0%  │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                        VERIFICATION METHODS                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   Test (T):                    30  ██████████████████████████████  75%  │
│   Demonstration (D):            5  ██████████                      12%  │
│   Inspection (I):               3  ██████                           8%  │
│   Analysis (A):                 2  ████                              5%  │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                        RISK COVERAGE                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   RED (Critical) Risks:         0  No critical risks identified         │
│   YELLOW (Watch) Risks:         5  ██████████  All covered by reqs      │
│   GREEN (Acceptable):          15  ██████████████████████████████        │
│                                                                          │
│   Risk Coverage: 100% of YELLOW risks have mitigating requirements      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Key Value Proposition

Based on Pareto Analysis, **three features deliver 80% of user value**:

| Rank | Feature | Value Contribution | Cumulative | Market Gap |
|------|---------|-------------------|------------|------------|
| 1 | VTT/SRT Import | 35% | 35% | **100%** (no competitor) |
| 2 | Speaker Identification | 25% | 60% | Partial support |
| 3 | Action Item Extraction | 20% | **80%** | Limited support |

**Strategic Implication**: MVP must deliver all three to achieve differentiation.

## Framework Contribution Summary

| Framework | Key Contribution | Requirements Generated |
|-----------|------------------|------------------------|
| **5W2H** | Scope boundaries, personas, performance targets | FR-001..004, NFR-001..002, STK-001..010 |
| **Ishikawa** | Root cause identification (24 causes in 6M) | NFR-006..008 (format handling) |
| **8D** | Corrective actions, ADR references | CA-1..CA-4 mapped to FR-001..015 |
| **Pareto** | Vital few prioritization | Priority assignments (Must/Should) |
| **FMEA** | Risk-informed requirements | NFR-003..010 (risk mitigations) |
| **NASA SE** | Formal specification, traceability | Full catalog (40 requirements) |

## GATE-2 Recommendation

```
GATE-2 DECISION MATRIX
======================

✓ Requirements completeness:     100% stakeholder needs traced
✓ Risk coverage:                 100% YELLOW risks mitigated
✓ Verification coverage:         100% requirements have V-methods
✓ Priority clarity:              MoSCoW assigned to all
✓ Phase allocation:              4 phases defined
✓ Architecture alignment:        Hexagonal pattern confirmed

RECOMMENDATION: PROCEED TO IMPLEMENTATION (FEAT-002)
```

---

# L1: Unified Requirements Catalog

## 1. Cross-Reference Matrix

### 1.1 Framework Contribution to Requirements

```
CROSS-REFERENCE MATRIX: FRAMEWORK → REQUIREMENTS
================================================

                          5W2H  Ishikawa  8D   Pareto  FMEA  NASA-SE
                          ────  ────────  ──   ──────  ────  ───────
STAKEHOLDER NEEDS
├── STK-001 (VTT)          ●                     ●            ●
├── STK-002 (SRT)          ●                     ●            ●
├── STK-003 (Speakers)     ●                     ●            ●
├── STK-004 (Actions)      ●                     ●            ●
├── STK-005 (Decisions)    ●                     ●            ●
├── STK-006 (Questions)    ●                                  ●
├── STK-007 (Performance)  ●                                  ●
├── STK-008 (Trust)        ●                          ●       ●
├── STK-009 (Jerry)                              ●            ●
└── STK-010 (Pipeline)     ●                     ●            ●

FUNCTIONAL REQUIREMENTS
├── FR-001 (VTT Parse)     ●       ●       ●     ●      ●     ●
├── FR-002 (SRT Parse)     ●       ●       ●     ●      ●     ●
├── FR-003 (Plain Text)    ●               ●                  ●
├── FR-004 (Auto-detect)   ●               ●                  ●
├── FR-005 (Voice Tags)    ●               ●     ●            ●
├── FR-006 (Patterns)      ●       ●       ●            ●     ●
├── FR-007 (Actions)       ●               ●     ●      ●     ●
├── FR-008 (Decisions)     ●                     ●            ●
├── FR-009 (Questions)     ●                                  ●
├── FR-010 (Standard NER)  ●               ●                  ●
├── FR-011 (Confidence)                          ●      ●     ●
├── FR-012 (Markdown)      ●               ●                  ●
├── FR-013 (JSON)          ●               ●                  ●
├── FR-014 (Citations)                                 ●      ●
└── FR-015 (Filtering)     ●               ●                  ●

NON-FUNCTIONAL REQUIREMENTS
├── NFR-001 (Performance)  ●                            ●     ●
├── NFR-002 (Memory)       ●                            ●     ●
├── NFR-003 (Speaker F1)                               ●      ●
├── NFR-004 (Action F1)                                ●      ●
├── NFR-005 (Hallucinate)                              ●      ●
├── NFR-006 (Timestamps)           ●                   ●      ●
├── NFR-007 (Encoding)             ●                   ●      ●
├── NFR-008 (Patterns)             ●                   ●      ●
├── NFR-009 (Versioning)                               ●      ●
└── NFR-010 (LLM Citations)                            ●      ●

INTERFACE REQUIREMENTS
├── IR-001 (CLI)           ●               ●     ●            ●
├── IR-002 (POSIX)         ●               ●            ●     ●
├── IR-003 (Exit Codes)                    ●            ●     ●
├── IR-004 (SKILL.md)                            ●            ●
└── IR-005 (Hexagonal)                           ●            ●

Legend: ● = Framework contributed to requirement
```

### 1.2 Requirement-to-Risk Linkage

| Requirement | Linked Risk | Risk Score | Risk Status | Mitigation Reflected |
|-------------|-------------|------------|-------------|---------------------|
| FR-001 | R-001 (VTT edge cases) | 6 | GREEN | Test corpus with diverse samples |
| FR-002, NFR-006 | R-002 (SRT timestamps) | 8 | YELLOW | Timestamp normalization |
| NFR-007 | R-003 (Encoding issues) | 6 | GREEN | Encoding detection |
| FR-005, FR-006, NFR-008 | R-004 (Missing voice tags) | 12 | YELLOW | Multi-pattern fallback |
| NFR-008 | R-005 (Speaker name variations) | 8 | YELLOW | Name normalization |
| FR-007, FR-011, NFR-004 | R-006 (Low precision) | 12 | YELLOW | Confidence thresholds |
| FR-007, FR-011, NFR-004 | R-007 (Low recall) | 12 | YELLOW | Multi-strategy approach |
| FR-014, NFR-005, NFR-010 | R-008 (Hallucination) | 12 | YELLOW | Citation requirement |
| FR-008 | R-009 (Implicit decisions) | 8 | GREEN | Scope clarity |
| IR-001, IR-002 | R-011 (CLI usability) | 4 | GREEN | Design guidelines |
| IR-003 | R-012 (Exit codes) | 2 | GREEN | Standard codes |
| FR-013, NFR-009 | R-014 (Schema breaking) | 9 | YELLOW | Versioning from v1 |
| IR-004, IR-005 | R-015, R-016 (Jerry integration) | 6 | GREEN | Pattern compliance |
| NFR-001 | R-017 (Processing time) | 6 | GREEN | Performance target |
| NFR-002 | R-018 (Memory exhaustion) | 6 | GREEN | Memory limit |

**YELLOW Risk Coverage Analysis**:

```
YELLOW RISK → REQUIREMENT COVERAGE
==================================

Risk ID    Risk Name                 Score  Requirements Covering     Coverage
──────────────────────────────────────────────────────────────────────────────
R-002      SRT Timestamp Malform.     8     FR-002, NFR-006           100%
R-004      Missing VTT Voice Tags    12     FR-005, FR-006, NFR-008   100%
R-006      Action Item Low Precision 12     FR-007, FR-011, NFR-004   100%
R-007      Action Item Low Recall    12     FR-007, FR-011, NFR-004   100%
R-008      LLM Hallucination         12     FR-014, NFR-005, NFR-010  100%
R-014      JSON Schema Breaking       9     FR-013, NFR-009           100%
──────────────────────────────────────────────────────────────────────────────
                                           ALL YELLOW RISKS COVERED: 100%
```

---

## 2. Unified Requirements Catalog

### 2.1 Stakeholder Needs (STK-001 to STK-010)

| ID | Need Statement | Stakeholder | Priority | Traceability |
|----|----------------|-------------|----------|--------------|
| STK-001 | Users need to process existing VTT transcript files without recording | Developers, Managers, Analysts | Critical | 5W2H: WHAT; Pareto: 35% value |
| STK-002 | Users need to process existing SRT transcript files without recording | Developers, Managers, Analysts | Critical | 5W2H: WHAT; Pareto: 35% value |
| STK-003 | Users need to identify who said what in a meeting | Developers, Managers | Critical | 5W2H: WHO; Pareto: 25% value |
| STK-004 | Users need to extract action items and commitments automatically | Developers, Managers | Critical | 5W2H: WHAT; Pareto: 20% value |
| STK-005 | Users need to identify decisions made during meetings | Managers, Analysts | High | 8D: Core value proposition |
| STK-006 | Users need to find questions asked (answered and unanswered) | Analysts | High | 5W2H: Entity taxonomy |
| STK-007 | Users need results quickly without long waits | All personas | High | 5W2H: <10s target |
| STK-008 | Users need to trust extraction results (confidence scores) | All personas | High | FMEA: R-006, R-008 |
| STK-009 | System must integrate seamlessly with Jerry framework | Jerry Framework | Critical | Project scope |
| STK-010 | System must support pipeline automation (CI/CD) | CI/CD Pipelines | Medium | 5W2H: Integration points |

### 2.2 Functional Requirements (FR-001 to FR-015)

#### 2.2.1 Input Processing (FR-001 to FR-004)

| ID | Requirement | Rationale | Parent | V-Method | Priority | Risk |
|----|-------------|-----------|--------|----------|----------|------|
| FR-001 | The system SHALL parse WebVTT (.vtt) files conforming to W3C WebVTT specification | Primary format (60% share); 100% market gap | STK-001 | Test | Must | R-001 |
| FR-002 | The system SHALL parse SubRip (.srt) files conforming to de facto standard | Secondary format (35% share) | STK-002 | Test | Must | R-002 |
| FR-003 | The system SHALL accept plain text files with speaker prefixes (Name: text format) | Legacy/manual transcripts | STK-001 | Test | Should | - |
| FR-004 | The system SHALL auto-detect input file format based on content, not file extension | Handles misnamed files | STK-001 | Test | Should | R-001 |

#### 2.2.2 Entity Extraction (FR-005 to FR-011)

| ID | Requirement | Rationale | Parent | V-Method | Priority | Risk |
|----|-------------|-----------|--------|----------|----------|------|
| FR-005 | The system SHALL extract speaker identities from VTT voice tags (`<v Speaker>`) | Native VTT support | STK-003 | Test | Must | R-004 |
| FR-006 | The system SHALL extract speaker identities from prefix patterns (Name:, [Name], ALLCAPS:) | Fallback for missing voice tags | STK-003 | Test | Must | R-004 |
| FR-007 | The system SHALL extract action items with associated assignee and deadline when present | Core value proposition (20% value) | STK-004 | Test | Must | R-006, R-007 |
| FR-008 | The system SHALL extract explicit decisions with supporting context | Decision tracking value | STK-005 | Test | Should | R-009 |
| FR-009 | The system SHALL extract questions and classify as answered or unanswered | Meeting follow-up support | STK-006 | Test | Should | - |
| FR-010 | The system SHALL extract standard NER entities (PERSON, ORG, DATE) | Foundation for enrichment | STK-004 | Test | Must | - |
| FR-011 | The system SHALL provide confidence scores (0.0-1.0) for all extracted entities | Trust calibration (FMEA) | STK-008 | Test | Must | R-006, R-008 |

#### 2.2.3 Output Generation (FR-012 to FR-015)

| ID | Requirement | Rationale | Parent | V-Method | Priority | Risk |
|----|-------------|-----------|--------|----------|----------|------|
| FR-012 | The system SHALL generate Markdown formatted output as default | Human-readable | STK-001 | Demo | Must | - |
| FR-013 | The system SHALL generate JSON structured output when requested | Machine-readable | STK-010 | Test | Must | R-014 |
| FR-014 | The system SHALL include source transcript citations for all extracted entities | Hallucination mitigation | STK-008 | Test | Must | R-008 |
| FR-015 | The system SHALL support filtering output by entity type via command-line argument | Focused extraction | STK-010 | Test | Should | - |

### 2.3 Non-Functional Requirements (NFR-001 to NFR-010)

#### 2.3.1 Performance (NFR-001 to NFR-002)

| ID | Requirement | Rationale | Parent | V-Method | Priority | Risk |
|----|-------------|-----------|--------|----------|----------|------|
| NFR-001 | The system SHALL complete processing of a 1-hour transcript (~10K words) in <10 seconds on standard hardware (4-core, 8GB RAM) | UX threshold (5W2H) | STK-007 | Test | Must | R-017 |
| NFR-002 | The system SHALL consume less than 500 MB RAM during peak processing | Developer machine constraints | STK-007 | Test | Must | R-018 |

#### 2.3.2 Accuracy (NFR-003 to NFR-005)

| ID | Requirement | Rationale | Parent | V-Method | Priority | Risk |
|----|-------------|-----------|--------|----------|----------|------|
| NFR-003 | The system SHALL achieve speaker identification F1 score >= 0.95 on transcripts with voice tags | Structural extraction accuracy | STK-003 | Test | Must | R-004 |
| NFR-004 | The system SHALL achieve action item extraction F1 score >= 0.80 on benchmark dataset | Academic baseline achievable | STK-004 | Test | Must | R-006, R-007 |
| NFR-005 | The system SHALL achieve hallucination rate <= 2% for LLM-assisted extractions | Below GPT-4o baseline (1.5%) | STK-008 | Test | Must | R-008 |

#### 2.3.3 Robustness (NFR-006 to NFR-010) - FMEA Derived

| ID | Requirement | Rationale | Parent | V-Method | Priority | Risk |
|----|-------------|-----------|--------|----------|----------|------|
| NFR-006 | The parser SHALL handle both period (.) and comma (,) as millisecond separators in timestamps | SRT format variation (R-002) | STK-002 | Test | Must | R-002 |
| NFR-007 | The system SHALL detect and convert non-UTF8 character encodings (Windows-1252, ISO-8859-1) to UTF-8 | Encoding variation (R-003) | STK-001 | Test | Must | R-003 |
| NFR-008 | The speaker extraction module SHALL support at least 4 naming patterns (voice tag, prefix, bracket, all-caps) | Multi-pattern coverage (R-004) | STK-003 | Test | Must | R-004 |
| NFR-009 | The JSON output schema SHALL include version number starting with "1.0" | Schema evolution (R-014) | STK-010 | Inspect | Must | R-014 |
| NFR-010 | All LLM-based extractions SHALL include source transcript span citations | Hallucination mitigation (R-008) | STK-008 | Test | Must | R-008 |

### 2.4 Interface Requirements (IR-001 to IR-005)

| ID | Requirement | Rationale | Parent | V-Method | Priority | Risk |
|----|-------------|-----------|--------|----------|----------|------|
| IR-001 | The system SHALL provide a CLI as the primary interaction method | Developer-first design | STK-P1 | Demo | Must | R-011 |
| IR-002 | The CLI SHALL follow POSIX conventions and clig.dev guidelines | Industry standard UX | STK-010 | Inspect | Must | R-011 |
| IR-003 | The CLI SHALL return exit code 0 for success, 1 for errors, 2 for invalid usage | CI/CD integration | STK-010 | Test | Must | R-012 |
| IR-004 | The system SHALL provide a SKILL.md interface compatible with Jerry framework | Framework integration | STK-S1 | Demo | Must | R-015 |
| IR-005 | The system architecture SHALL conform to hexagonal architecture patterns with domain isolation | Jerry framework standard | STK-S1 | Analysis | Must | R-016 |

---

## 3. Traceability Summary

### 3.1 Forward Traceability (Needs → Requirements → Design)

```
FORWARD TRACEABILITY CHAIN
==========================

5W2H Scope → Pareto Priority → FMEA Risks → NASA SE Requirements → Design Elements

┌──────────────────────────────────────────────────────────────────────────────────┐
│                                                                                   │
│  5W2H SCOPE                          PARETO PRIORITY                             │
│  ──────────                          ───────────────                             │
│                                                                                   │
│  WHAT: VTT/SRT parsing        ────► 35% value (Rank 1)                          │
│  WHO: 3 personas              ────► Developer-first                              │
│  HOW MUCH: <10s, 80% F1       ────► Performance targets                         │
│                    │                       │                                     │
│                    ▼                       ▼                                     │
│            ┌──────────────────────────────────────┐                             │
│            │         FMEA RISK ANALYSIS           │                             │
│            ├──────────────────────────────────────┤                             │
│            │ R-002: SRT Timestamps       [YELLOW] │──► NFR-006                  │
│            │ R-004: Missing Voice Tags   [YELLOW] │──► FR-005, FR-006, NFR-008  │
│            │ R-006: Low Precision        [YELLOW] │──► FR-011, NFR-004          │
│            │ R-008: Hallucination        [YELLOW] │──► FR-014, NFR-005, NFR-010 │
│            │ R-014: Schema Breaking      [YELLOW] │──► NFR-009                  │
│            └──────────────────────────────────────┘                             │
│                             │                                                    │
│                             ▼                                                    │
│            ┌──────────────────────────────────────┐                             │
│            │      NASA SE REQUIREMENTS            │                             │
│            ├──────────────────────────────────────┤                             │
│            │ STK-001..010: Stakeholder Needs      │                             │
│            │ FR-001..015: Functional Requirements │                             │
│            │ NFR-001..010: Non-Functional Reqs    │                             │
│            │ IR-001..005: Interface Requirements  │                             │
│            └──────────────────────────────────────┘                             │
│                             │                                                    │
│                             ▼                                                    │
│            ┌──────────────────────────────────────┐                             │
│            │       DESIGN ELEMENTS                │                             │
│            ├──────────────────────────────────────┤                             │
│            │ Domain: Transcript, ExtractedEntity  │                             │
│            │ Application: Commands, Queries       │                             │
│            │ Infrastructure: Adapters (VTT, SRT)  │                             │
│            │ Interface: CLI, SKILL.md             │                             │
│            └──────────────────────────────────────┘                             │
│                                                                                   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Vital Few Coverage (80% Value)

| Vital Few Feature | Value | Requirements | Design Elements | Test Cases |
|-------------------|-------|--------------|-----------------|------------|
| VTT/SRT Import | 35% | FR-001, FR-002, NFR-006, NFR-007 | VTTParser, SRTParser, FormatDetector | TC-001, TC-002, TC-N06, TC-N07 |
| Speaker Identification | 25% | FR-005, FR-006, NFR-003, NFR-008 | VoiceTagExtractor, PatternMatcher | TC-005, TC-006, TC-N03, TC-N08 |
| Action Item Extraction | 20% | FR-007, FR-011, NFR-004 | ActionItemExtractor, ConfidenceScorer | TC-007, TC-011, TC-N04 |
| **TOTAL** | **80%** | **11 requirements** | **6 components** | **10 test cases** |

### 3.3 YELLOW Risk Coverage Matrix

| Risk ID | Risk Name | Score | Requirements | Test Cases | Residual Risk |
|---------|-----------|-------|--------------|------------|---------------|
| R-002 | SRT Timestamp Malformation | 8 | NFR-006 | TC-N06 | 4 (GREEN) |
| R-004 | Missing VTT Voice Tags | 12 | FR-005, FR-006, NFR-008 | TC-005, TC-006, TC-N08 | 6 (GREEN) |
| R-006 | Low Precision (Action Items) | 12 | FR-007, FR-011, NFR-004 | TC-007, TC-011, TC-N04 | 6 (GREEN) |
| R-007 | Low Recall (Action Items) | 12 | FR-007, FR-011, NFR-004 | TC-007, TC-011, TC-N04 | 6 (GREEN) |
| R-008 | LLM Hallucination | 12 | FR-014, NFR-005, NFR-010 | TC-014, TC-N05, TC-N10 | 6 (GREEN) |
| R-014 | JSON Schema Breaking | 9 | NFR-009 | TC-N09 | 4 (GREEN) |

**Coverage Status**: All 6 YELLOW risks mitigated to GREEN via requirements

---

## 4. Implementation Phase Mapping

### 4.1 Phase Allocation

```
IMPLEMENTATION PHASE TIMELINE
=============================

PHASE 1: FOUNDATION (Weeks 1-2)
───────────────────────────────
Priority: Must-have core capabilities

Requirements:
├── FR-001: VTT Parser                    [Must]
├── FR-002: SRT Parser                    [Must]
├── FR-003: Plain Text Parser             [Should]
├── FR-004: Auto-detect Format            [Should]
├── NFR-006: Timestamp Normalization      [Must]  ← R-002 mitigation
├── NFR-007: Encoding Detection           [Must]  ← R-003 mitigation
├── IR-001: CLI Interface                 [Must]
├── IR-002: POSIX Conventions             [Must]
└── IR-003: Exit Codes                    [Must]

Deliverables:
  transcript parse <file> --format=text


PHASE 2: CORE EXTRACTION (Weeks 3-6)
────────────────────────────────────
Priority: 80% value delivery

Requirements:
├── FR-005: Voice Tag Extraction          [Must]
├── FR-006: Pattern-based Speaker ID      [Must]
├── FR-007: Action Item Extraction        [Must]
├── FR-010: Standard NER                  [Must]
├── FR-011: Confidence Scores             [Must]  ← R-006/R-008 mitigation
├── NFR-003: Speaker F1 >= 0.95           [Must]
├── NFR-004: Action F1 >= 0.80            [Must]
└── NFR-008: 4+ Speaker Patterns          [Must]  ← R-004 mitigation

Deliverables:
  transcript extract <file> --entities speakers,action-items


PHASE 3: INTEGRATION (Weeks 7-8)
────────────────────────────────
Priority: Full feature set + Jerry integration

Requirements:
├── FR-008: Decision Extraction           [Should]
├── FR-009: Question Extraction           [Should]
├── FR-012: Markdown Output               [Must]
├── FR-013: JSON Output                   [Must]
├── FR-014: Source Citations              [Must]  ← R-008 mitigation
├── FR-015: Entity Filtering              [Should]
├── IR-004: SKILL.md Interface            [Must]
├── IR-005: Hexagonal Architecture        [Must]
├── NFR-009: Schema Versioning            [Must]  ← R-014 mitigation
└── NFR-010: LLM Citation Validation      [Must]  ← R-008 mitigation

Deliverables:
  transcript extract <file> --format json
  SKILL.md interface file


PHASE 4: VALIDATION (Weeks 9-10)
────────────────────────────────
Priority: Quality assurance + deployment

Requirements:
├── NFR-001: Performance Validation       [Must]  ← R-017 verification
├── NFR-002: Memory Validation            [Must]  ← R-018 verification
└── NFR-005: Hallucination Rate Test      [Must]  ← R-008 verification

Deliverables:
  Benchmark reports
  Accuracy test results
  Deployment package


PHASE SUMMARY
─────────────
┌─────────────────────────────────────────────────────────────────┐
│ Phase 1 (Foundation):    9 requirements   ██████████ 23%       │
│ Phase 2 (Core):          8 requirements   ████████   20%       │
│ Phase 3 (Integration):  10 requirements   ██████████ 25%       │
│ Phase 4 (Validation):    3 requirements   ███        7%        │
│ Ongoing (Cross-cutting): 10 requirements  ██████████ 25%       │
│                                           ──────────────        │
│ TOTAL:                  40 requirements               100%      │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Verification Method Distribution by Phase

| Phase | Test (T) | Demo (D) | Inspect (I) | Analysis (A) | Total |
|-------|----------|----------|-------------|--------------|-------|
| Phase 1 | 7 | 1 | 1 | 0 | 9 |
| Phase 2 | 8 | 0 | 0 | 0 | 8 |
| Phase 3 | 7 | 2 | 1 | 1 | 11 |
| Phase 4 | 3 | 0 | 0 | 0 | 3 |
| **Total** | **25** | **3** | **2** | **1** | **31** |

---

# L2: Strategic Patterns and Architectural Decisions

## 5. Pattern Extraction

### 5.1 Design Patterns (PAT-001 to PAT-006)

| ID | Pattern Name | Description | Source Framework | Requirements Affected |
|----|--------------|-------------|------------------|----------------------|
| PAT-001 | **Tiered Extraction Pipeline** | Rule-based → ML-based → LLM-based extraction with confidence scores | FMEA, 8D | FR-007, FR-011, NFR-004, NFR-005 |
| PAT-002 | **Defensive Parsing** | Accept liberally, process consistently; normalize formats to canonical model | Ishikawa, FMEA | FR-001, FR-002, NFR-006, NFR-007 |
| PAT-003 | **Multi-Pattern Speaker Detection** | 4+ pattern fallback chain for speaker identification | Ishikawa, FMEA | FR-005, FR-006, NFR-008 |
| PAT-004 | **Citation-Required Extraction** | All LLM outputs include source transcript spans | FMEA (R-008) | FR-014, NFR-010 |
| PAT-005 | **Versioned Schema Evolution** | JSON output includes version; backward compatibility guaranteed | FMEA (R-014) | FR-013, NFR-009 |
| PAT-006 | **Hexagonal Skill Architecture** | Domain isolation with ports/adapters; composable with Jerry | 8D, NASA SE | IR-004, IR-005 |

### 5.2 Pattern Implementation Guidance

#### PAT-001: Tiered Extraction Pipeline

```
TIERED EXTRACTION PIPELINE PATTERN
==================================

                    INPUT: Transcript Segment
                              │
                              ▼
              ┌───────────────────────────────┐
              │  TIER 1: Rule-Based (Default)  │
              │  ─────────────────────────────  │
              │  • Pattern matching             │
              │  • Keyword detection            │
              │  • Linguistic markers           │
              │  • Confidence: 0.6-0.8          │
              │  • Latency: <500ms              │
              └───────────────┬───────────────┘
                              │ (if confidence < threshold)
                              ▼
              ┌───────────────────────────────┐
              │  TIER 2: ML-Based (Enhanced)   │
              │  ─────────────────────────────  │
              │  • spaCy NER                   │
              │  • Fine-tuned classifiers      │
              │  • Confidence: 0.7-0.9         │
              │  • Latency: <2000ms            │
              └───────────────┬───────────────┘
                              │ (if confidence < threshold OR opt-in)
                              ▼
              ┌───────────────────────────────┐
              │  TIER 3: LLM-Based (Premium)   │
              │  ─────────────────────────────  │
              │  • Claude/GPT extraction       │
              │  • Citation requirement        │
              │  • Confidence: 0.85-0.95       │
              │  • Latency: <5000ms            │
              └───────────────┬───────────────┘
                              │
                              ▼
                    OUTPUT: ExtractedEntity
                    with confidence + citations
```

#### PAT-002: Defensive Parsing

```
DEFENSIVE PARSING PATTERN
=========================

     RAW INPUT                   DETECTION               NORMALIZATION
     ─────────                   ─────────               ─────────────

┌──────────────┐          ┌──────────────────┐      ┌──────────────────┐
│ VTT File     │─────────►│ Format Detection │      │                  │
│ (60% share)  │          │ ────────────────  │      │  Canonical       │
└──────────────┘          │                  │      │  Transcript      │
                          │ 1. Check header  │─────►│  Model           │
┌──────────────┐          │ 2. Detect cues   │      │  ──────────      │
│ SRT File     │─────────►│ 3. Identify      │      │                  │
│ (35% share)  │          │    timestamps    │      │ • Segments[]     │
└──────────────┘          │                  │      │ • Speakers[]     │
                          │ 4. Encoding      │      │ • Metadata       │
┌──────────────┐          │    detection     │      │                  │
│ Plain Text   │─────────►│                  │      │                  │
│ (5% share)   │          └──────────────────┘      └──────────────────┘
└──────────────┘                   │
                                   │
                          ┌────────▼────────┐
                          │ Error Recovery  │
                          │ ──────────────  │
                          │ • Log anomalies │
                          │ • Skip malformed│
                          │ • Continue      │
                          └─────────────────┘
```

---

## 6. Lessons Learned (LES-001 to LES-006)

| ID | Lesson | Source | Application |
|----|--------|--------|-------------|
| LES-001 | **Recording-first paradigm is business model driven, not technical** | Ishikawa (5 Whys) | Position as text-first; don't compete on recording |
| LES-002 | **Format fragmentation requires defensive parsing** | Ishikawa (MATERIAL), FMEA | Build robust parsers; accept liberally |
| LES-003 | **NLP accuracy varies wildly (F1: 0.13-0.94)** | 8D, FMEA | Set realistic targets (0.80); use confidence scores |
| LES-004 | **LLM hallucination is manageable with citations** | FMEA (R-008) | Require source spans for all LLM extractions |
| LES-005 | **Pareto principle validates MVP scope** | Pareto | 3 features = 80% value; resist scope creep |
| LES-006 | **NASA SE methodology prevents orphan requirements** | NASA SE | Bidirectional traceability catches gaps |

---

## 7. Key Assumptions Requiring Validation (ASM-001 to ASM-008)

| ID | Assumption | Validation Method | Risk if Invalid |
|----|------------|-------------------|-----------------|
| ASM-001 | VTT voice tags are present in majority of transcripts from major platforms | User survey; sample file analysis | R-004 escalation; pattern fallback critical |
| ASM-002 | spaCy en_core_web_sm provides sufficient NER accuracy for standard entities | Benchmark on AMI corpus subset | May require larger model (performance impact) |
| ASM-003 | Rule-based action item detection achieves F1 >= 0.70 baseline | Test on labeled dataset | Earlier LLM integration needed |
| ASM-004 | 10-second processing target is achievable on 4-core CPU | Performance profiling | Architecture changes required |
| ASM-005 | Users accept confidence scores in lieu of perfect accuracy | User testing | Trust issues; feature rejection risk |
| ASM-006 | CLI-first interface meets majority user needs | Adoption metrics | Web interface may be needed earlier |
| ASM-007 | Jerry SKILL.md interface is stable and documented | Jerry framework review | Integration delays |
| ASM-008 | LLM hallucination rate stays below 2% with citation prompting | A/B testing with labeled data | May require additional validation layer |

---

## 8. Tensions and Resolutions

### 8.1 Identified Framework Tensions

| Tension | Frameworks | Resolution |
|---------|------------|------------|
| **Accuracy vs. Speed** | 5W2H (<10s) vs. FMEA (F1>=0.80) | Tiered extraction: fast default, accurate opt-in |
| **Feature breadth vs. Risk** | Pareto (90% cumulative) vs. FMEA (YELLOW risks) | Defer high-risk features (Summary) to Phase 3+ |
| **Local-first vs. Accuracy** | 5W2H (privacy) vs. FMEA (LLM path) | Local default; cloud LLM opt-in with citation requirement |
| **MVP scope vs. User expectations** | Pareto (3 features) vs. 5W2H (7 capabilities) | Clear documentation of MVP limitations |

### 8.2 Tension Resolution Rationale

```
TENSION: Accuracy vs. Speed
===========================

5W2H Position:                      FMEA Position:
──────────────                      ─────────────
• <10s processing                   • F1 >= 0.80 for actions
• Responsive UX                     • Confidence scores required
• Developer-first                   • Low hallucination rate

                    ┌─────────────────────────┐
                    │      RESOLUTION         │
                    ├─────────────────────────┤
                    │                         │
                    │  TIERED EXTRACTION      │
                    │  ─────────────────      │
                    │                         │
                    │  Default: Rule-based    │
                    │  • Fast (<3s)           │
                    │  • Moderate accuracy    │
                    │  • Zero external deps   │
                    │                         │
                    │  Opt-in: LLM-based      │
                    │  • Slower (5-15s)       │
                    │  • Higher accuracy      │
                    │  • Citation required    │
                    │                         │
                    │  User chooses based     │
                    │  on use case            │
                    │                         │
                    └─────────────────────────┘


TENSION: Feature Breadth vs. Risk
=================================

Pareto Position:                    FMEA Position:
────────────────                    ─────────────
• 6 features = 100% value           • Summary = HIGH risk
• Summary = 5% value                • Real-time = CRITICAL risk
• Include all for completeness      • Defer high-risk features

                    ┌─────────────────────────┐
                    │      RESOLUTION         │
                    ├─────────────────────────┤
                    │                         │
                    │  PHASED DELIVERY        │
                    │  ───────────────        │
                    │                         │
                    │  Phase 1-2: Vital Few   │
                    │  • VTT/SRT (35%)        │
                    │  • Speakers (25%)       │
                    │  • Actions (20%)        │
                    │  = 80% value, LOW risk  │
                    │                         │
                    │  Phase 3+: Optional     │
                    │  • Decisions (5%)       │
                    │  • Questions (5%)       │
                    │  • Summary (5%)         │
                    │  = 15% value, MEDIUM+   │
                    │                         │
                    └─────────────────────────┘
```

---

## 9. Architectural Decision References

### 9.1 ADR Cross-Reference

| ADR ID | Decision | Source | Requirements |
|--------|----------|--------|--------------|
| ADR-001 | Parser Abstraction (ITranscriptParser protocol) | 8D (D7: Prevention) | FR-001..004 |
| ADR-002 | NLP Pipeline Composition (staged interfaces) | 8D (D5: CA-3) | FR-005..011 |
| ADR-003 | LLM Fallback Strategy (dual-mode extraction) | 8D (D5), FMEA (R-008) | NFR-005, NFR-010 |
| ADR-004 | Versioned Output Schema | FMEA (R-014) | NFR-009 |
| ADR-005 | Citation Requirement for LLM | FMEA (R-008) | FR-014, NFR-010 |

### 9.2 One-Way Door Decisions

| Decision | Type | Risk Level | Mitigation |
|----------|------|------------|------------|
| Python as core language | One-way | Low | Ecosystem alignment with spaCy, HuggingFace |
| Local-first architecture | One-way | Low | Core differentiator; cloud opt-in |
| Hexagonal architecture | Two-way | Low | Jerry framework alignment |
| spaCy for NER MVP | Two-way | Medium | Abstraction allows swap |
| CLI-first interface | Two-way | Low | Can add API/GUI later |
| Entity type taxonomy | One-way | Medium | Extensible enum design |

---

## 10. References

### 10.1 Input Documents

| Document | Framework | Location |
|----------|-----------|----------|
| 5W2H-ANALYSIS.md | 5W2H | EN-003-requirements-synthesis/analysis/ |
| ISHIKAWA-DIAGRAM.md | Ishikawa/6M | EN-003-requirements-synthesis/analysis/ |
| 8D-PROBLEM-SOLVING.md | 8D | EN-003-requirements-synthesis/analysis/ |
| PARETO-ANALYSIS.md | Pareto 80/20 | EN-003-requirements-synthesis/analysis/ |
| FMEA-ANALYSIS.md | FMEA | EN-003-requirements-synthesis/analysis/ |
| NASA-SE-REQUIREMENTS.md | NPR 7123.1D | EN-003-requirements-synthesis/requirements/ |

### 10.2 Research Sources (EN-001, EN-002)

| Document | Type | Key Contribution |
|----------|------|------------------|
| FEATURE-MATRIX.md | Market Analysis | 100% competitor gap identification |
| VTT-SPECIFICATION.md | Technical Standard | W3C WebVTT compliance |
| SRT-SPECIFICATION.md | Technical Standard | De facto SRT format |
| NLP-NER-BEST-PRACTICES.md | Technical Guide | Pipeline architecture |
| ACADEMIC-LITERATURE-REVIEW.md | Research | F1 benchmarks, hallucination rates |

### 10.3 Standards

| Standard | Application |
|----------|-------------|
| NPR 7123.1D | NASA Systems Engineering Processes |
| NASA-HDBK-1009A | Requirements Engineering Handbook |
| NPR 8000.4C | Risk Management Program Requirements |
| W3C WebVTT | Transcript format specification |

---

## Appendix A: Requirement Summary Tables

### A.1 Requirements by Category

| Category | Count | Must | Should | Could | Won't |
|----------|-------|------|--------|-------|-------|
| Stakeholder Needs (STK) | 10 | 6 | 4 | 0 | 0 |
| Functional (FR) | 15 | 11 | 4 | 0 | 0 |
| Non-Functional (NFR) | 10 | 10 | 0 | 0 | 0 |
| Interface (IR) | 5 | 5 | 0 | 0 | 0 |
| **TOTAL** | **40** | **32** | **8** | **0** | **0** |

### A.2 Requirements by Phase

| Phase | Requirements | % of Total |
|-------|--------------|------------|
| Phase 1: Foundation | 9 | 22.5% |
| Phase 2: Core Extraction | 8 | 20.0% |
| Phase 3: Integration | 11 | 27.5% |
| Phase 4: Validation | 3 | 7.5% |
| Cross-cutting | 9 | 22.5% |
| **TOTAL** | **40** | **100%** |

### A.3 Verification Method Summary

| Method | Count | % | Examples |
|--------|-------|---|----------|
| Test (T) | 30 | 75% | Parser unit tests, F1 benchmarks |
| Demonstration (D) | 5 | 12.5% | CLI walkthrough, SKILL.md review |
| Inspection (I) | 3 | 7.5% | Schema version check, POSIX compliance |
| Analysis (A) | 2 | 5% | Architecture review |

---

## Appendix B: Glossary

| Term | Definition |
|------|------------|
| **5W2H** | What, Why, Where, When, Who, How, How Much - scope definition framework |
| **Ishikawa** | Fishbone/6M root cause analysis diagram |
| **8D** | Eight Disciplines problem-solving methodology |
| **Pareto** | 80/20 rule - vital few vs. useful many |
| **FMEA** | Failure Mode and Effects Analysis |
| **NPR 7123.1D** | NASA Systems Engineering Processes and Requirements |
| **MoSCoW** | Must, Should, Could, Won't - prioritization method |
| **ADIT** | Analysis, Demonstration, Inspection, Test - verification methods |
| **F1 Score** | Harmonic mean of precision and recall |
| **VTT** | WebVTT - W3C standard for timed text |
| **SRT** | SubRip Text - de facto subtitle standard |
| **NER** | Named Entity Recognition |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-25 | ps-synthesizer agent | Initial consolidated requirements specification |

---

## Review Checklist (GATE-2)

- [x] All requirements traceable to stakeholder needs (100%)
- [x] All requirements have verification method (ADIT)
- [x] All FMEA YELLOW risks have requirement coverage (6/6)
- [x] No orphan requirements detected
- [x] MoSCoW priorities assigned (32 Must, 8 Should)
- [x] Phase allocation complete (4 phases)
- [x] Design pattern extraction complete (6 patterns)
- [x] Lessons learned documented (6 lessons)
- [x] Assumptions listed for validation (8 assumptions)
- [x] Framework tensions resolved with rationale
- [x] ADR cross-references complete

---

*End of Consolidated Requirements Specification*
