# NASA SE Requirements Specification: Transcript Skill

> **NASA SE DISCLAIMER**: This document follows NPR 7123.1D (NASA Systems Engineering Processes and Requirements) and NASA-HDBK-1009A (Requirements Engineering Handbook) methodologies adapted for software development context. While not a flight-critical mission, we apply mission-grade rigor to ensure high-quality, traceable requirements.

---

> **Project ID**: PROJ-008-transcript-skill
> **Entry ID**: e-003
> **Document Type**: NASA SE Requirements Specification
> **Version**: 1.0
> **Date**: 2026-01-25
> **Author**: nse-requirements agent
> **Status**: Draft - Pending ps-critic Review

---

## Document Navigation

| Level | Audience | Section |
|-------|----------|---------|
| L0 | Executive / Non-Technical | [Executive Summary](#l0-executive-summary) |
| L1 | Software Engineer | [Full Requirements Specification](#l1-full-requirements-specification) |
| L2 | Principal Architect | [Traceability and Risk Analysis](#l2-traceability-and-risk-analysis) |

---

## L0: Executive Summary

### What is This Document?

This document defines **what** the Transcript Skill must do, expressed as formal requirements. Think of it as a detailed contract between what users need and what engineers will build.

### Simple Analogy

Imagine ordering a custom car:
- **Stakeholder Needs**: "I need to commute 50 miles daily in comfort"
- **Technical Requirements**: "Vehicle SHALL have 400-mile range, 5 seats, climate control"
- **Verification**: "Range tested on dynamometer; seats inspected; AC output measured"

This document does the same for our Transcript Skill - translating what people need into what the software must do, with clear ways to prove it works.

### Key Takeaways

```
STAKEHOLDER VALUE SUMMARY
=========================

Who Benefits:        3 Primary Stakeholders Identified
What They Get:       Text-first transcript analysis (first in market!)
Core Capabilities:   VTT/SRT parsing, speaker ID, action item extraction
Performance Target:  <10 seconds for 1-hour transcript
Quality Target:      80%+ accuracy for entity extraction

REQUIREMENTS AT A GLANCE
========================

Stakeholder Needs:      10 defined (STK-001 to STK-010)
Functional Requirements: 15 defined (FR-001 to FR-015)
Non-Functional Reqs:    10 defined (NFR-001 to NFR-010)
Interface Requirements:  5 defined (IR-001 to IR-005)

TOTAL: 40 traceable requirements
```

### Why NASA SE Methodology?

NASA's systems engineering approach ensures:
1. **No orphan requirements** - Everything traces back to stakeholder needs
2. **Verifiable outcomes** - Every requirement has a test method
3. **Risk-informed design** - Requirements address identified failure modes
4. **Clear priorities** - MoSCoW classification guides implementation

---

## L1: Full Requirements Specification

### 1. NPR 7123.1D Process 1: Stakeholder Expectations Definition

#### 1.1 Stakeholder Identification

```
STAKEHOLDER HIERARCHY
=====================

Primary Stakeholders (Direct Users)
├── STK-P1: Developer Dan - Software Engineer
│   ├── Usage: 5-10 meetings/week, CLI-first workflow
│   ├── Pain Point: Loses track of action items from sprint planning
│   └── Need: Quick extraction of tasks assigned to him
│
├── STK-P2: Process Manager - Engineering Manager
│   ├── Usage: Daily standups, weekly 1:1s, retrospectives
│   ├── Pain Point: Manual note-taking during meetings
│   └── Need: Automated summaries with decisions highlighted
│
└── STK-P3: Content Analyst - Business Analyst/PM
    ├── Usage: Reviews stakeholder meetings, creates requirements
    ├── Pain Point: Transcript files sit unprocessed
    └── Need: Extract requirements, decisions, questions

Secondary Stakeholders (System Integrators)
├── STK-S1: Jerry Framework - Skill Integration
│   └── Need: Compliant SKILL.md interface, hexagonal architecture
│
└── STK-S2: CI/CD Pipeline - Automation
    └── Need: Exit codes, JSON output, batch processing
```

#### 1.2 Stakeholder Needs (STK-xxx)

| ID | Need Statement | Stakeholder | Priority | Source |
|----|---------------|-------------|----------|--------|
| STK-001 | Users need to process existing VTT transcript files without recording | STK-P1, STK-P2, STK-P3 | Critical | FEATURE-MATRIX.md (100% competitor gap) |
| STK-002 | Users need to process existing SRT transcript files without recording | STK-P1, STK-P2, STK-P3 | Critical | FEATURE-MATRIX.md (100% competitor gap) |
| STK-003 | Users need to identify who said what in a meeting | STK-P1, STK-P2 | Critical | 5W2H: Speaker ID = 25% value |
| STK-004 | Users need to extract action items and commitments automatically | STK-P1, STK-P2 | Critical | Pareto: 20% value contribution |
| STK-005 | Users need to identify decisions made during meetings | STK-P2, STK-P3 | High | 8D: Core value proposition |
| STK-006 | Users need to find questions asked (answered and unanswered) | STK-P3 | High | 5W2H: Entity taxonomy |
| STK-007 | Users need results quickly without long waits | STK-P1, STK-P2 | High | 5W2H: <10s target |
| STK-008 | Users need to trust extraction results (confidence scores) | STK-P1, STK-P2, STK-P3 | High | FMEA: R-006, R-008 |
| STK-009 | System must integrate seamlessly with Jerry framework | STK-S1 | Critical | Project scope |
| STK-010 | System must support pipeline automation (CI/CD) | STK-S2 | Medium | 5W2H: Integration points |

#### 1.3 Stakeholder Context Diagram

```
                         STAKEHOLDER CONTEXT DIAGRAM
+----------------------------------------------------------------------------+
|                                                                             |
|                              EXTERNAL CONTEXT                               |
|                                                                             |
|   ┌─────────────────────────────────────────────────────────────────────┐  |
|   │                        PRIMARY STAKEHOLDERS                          │  |
|   │                                                                      │  |
|   │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐            │  |
|   │   │ Developer   │    │  Process    │    │  Content    │            │  |
|   │   │    Dan      │    │  Manager    │    │  Analyst    │            │  |
|   │   │  (STK-P1)   │    │  (STK-P2)   │    │  (STK-P3)   │            │  |
|   │   └──────┬──────┘    └──────┬──────┘    └──────┬──────┘            │  |
|   │          │                  │                  │                    │  |
|   │          │   STK-001..008   │                  │                    │  |
|   │          └──────────────────┼──────────────────┘                    │  |
|   │                             │                                       │  |
|   └─────────────────────────────┼───────────────────────────────────────┘  |
|                                 │                                          |
|                                 ▼                                          |
|   ┌─────────────────────────────────────────────────────────────────────┐  |
|   │                                                                      │  |
|   │                      TRANSCRIPT SKILL                                │  |
|   │                                                                      │  |
|   │    ┌──────────────┐   ┌──────────────┐   ┌──────────────┐          │  |
|   │    │ VTT/SRT      │   │   Entity     │   │   Output     │          │  |
|   │    │ Parsing      │──▶│  Extraction  │──▶│  Generation  │          │  |
|   │    └──────────────┘   └──────────────┘   └──────────────┘          │  |
|   │                                                                      │  |
|   └─────────────────────────────────────────────────────────────────────┘  |
|                                 │                                          |
|                                 ▼                                          |
|   ┌─────────────────────────────────────────────────────────────────────┐  |
|   │                       SECONDARY STAKEHOLDERS                         │  |
|   │                                                                      │  |
|   │   ┌─────────────────────────┐    ┌─────────────────────────┐       │  |
|   │   │    Jerry Framework      │    │    CI/CD Pipelines      │       │  |
|   │   │       (STK-S1)          │    │       (STK-S2)          │       │  |
|   │   │                         │    │                         │       │  |
|   │   │  - SKILL.md interface   │    │  - Exit codes           │       │  |
|   │   │  - Hexagonal arch       │    │  - JSON output          │       │  |
|   │   │  - Work tracker         │    │  - Batch mode           │       │  |
|   │   └─────────────────────────┘    └─────────────────────────┘       │  |
|   │                                                                      │  |
|   └─────────────────────────────────────────────────────────────────────┘  |
|                                                                             |
+----------------------------------------------------------------------------+
```

---

### 2. NPR 7123.1D Process 2: Technical Requirements Definition

#### 2.1 Functional Requirements (FR-xxx)

##### 2.1.1 Input Processing Requirements

| ID | Requirement Statement | Rationale | Parent | V-Method | Priority | Risk Link |
|----|----------------------|-----------|--------|----------|----------|-----------|
| FR-001 | The system SHALL parse WebVTT (.vtt) files conforming to W3C WebVTT specification | Primary input format with 60% market share; enables text-first processing | STK-001 | Test (T) | Must | R-001 |
| FR-002 | The system SHALL parse SubRip (.srt) files conforming to de facto standard | Secondary input format with 35% market share | STK-002 | Test (T) | Must | R-002 |
| FR-003 | The system SHALL accept plain text files with speaker prefixes (Name: text format) | Supports legacy and manual transcripts | STK-001, STK-002 | Test (T) | Should | - |
| FR-004 | The system SHALL auto-detect input file format based on content, not file extension | Handles misnamed files; improves UX | STK-001, STK-002 | Test (T) | Should | R-001 |

##### 2.1.2 Entity Extraction Requirements

| ID | Requirement Statement | Rationale | Parent | V-Method | Priority | Risk Link |
|----|----------------------|-----------|--------|----------|----------|-----------|
| FR-005 | The system SHALL extract speaker identities from VTT voice tags (`<v Speaker>`) | Native VTT speaker support; highest accuracy path | STK-003 | Test (T) | Must | R-004 |
| FR-006 | The system SHALL extract speaker identities from prefix patterns (Name:, [Name], ALLCAPS:) | Fallback when voice tags absent | STK-003 | Test (T) | Must | R-004 |
| FR-007 | The system SHALL extract action items with associated assignee (when present) and deadline (when present) | Core value proposition per Pareto analysis | STK-004 | Test (T) | Must | R-006, R-007 |
| FR-008 | The system SHALL extract explicit decisions with supporting context | Decision tracking identified as high value | STK-005 | Test (T) | Should | R-009 |
| FR-009 | The system SHALL extract questions and classify as answered or unanswered | Supports meeting follow-up workflows | STK-006 | Test (T) | Should | - |
| FR-010 | The system SHALL extract standard NER entities (PERSON, ORG, DATE) | Foundation for enriched analysis | STK-004, STK-005 | Test (T) | Must | - |
| FR-011 | The system SHALL provide confidence scores (0.0-1.0) for all extracted entities | Enables trust calibration per FMEA | STK-008 | Test (T) | Must | R-006, R-008 |

##### 2.1.3 Output Generation Requirements

| ID | Requirement Statement | Rationale | Parent | V-Method | Priority | Risk Link |
|----|----------------------|-----------|--------|----------|----------|-----------|
| FR-012 | The system SHALL generate Markdown formatted output as default | Human-readable, compatible with documentation workflows | STK-001..008 | Demonstration (D) | Must | - |
| FR-013 | The system SHALL generate JSON structured output when requested | Machine-readable for pipeline integration | STK-010 | Test (T) | Must | R-014 |
| FR-014 | The system SHALL include source transcript citations for all extracted entities | Enables verification, mitigates hallucination | STK-008 | Test (T) | Must | R-008 |
| FR-015 | The system SHALL support filtering output by entity type via command-line argument | Enables focused extraction per use case | STK-001, STK-010 | Test (T) | Should | - |

#### 2.2 Non-Functional Requirements (NFR-xxx)

##### 2.2.1 Performance Requirements

| ID | Requirement Statement | Rationale | Parent | V-Method | Priority | Risk Link |
|----|----------------------|-----------|--------|----------|----------|-----------|
| NFR-001 | The system SHALL complete processing of a 1-hour transcript (approximately 10,000 words) in less than 10 seconds on standard hardware (4-core CPU, 8GB RAM) | User experience threshold; 5W2H analysis | STK-007 | Test (T) | Must | R-017 |
| NFR-002 | The system SHALL consume less than 500 MB of RAM during peak processing | Enables operation on typical developer machines | STK-007 | Test (T) | Must | R-018 |

##### 2.2.2 Accuracy Requirements

| ID | Requirement Statement | Rationale | Parent | V-Method | Priority | Risk Link |
|----|----------------------|-----------|--------|----------|----------|-----------|
| NFR-003 | The system SHALL achieve speaker identification F1 score >= 0.95 on transcripts with voice tags | Structural extraction should be highly accurate | STK-003 | Test (T) | Must | R-004 |
| NFR-004 | The system SHALL achieve action item extraction F1 score >= 0.80 on benchmark dataset | Academic literature shows achievable with hybrid approach | STK-004, STK-008 | Test (T) | Must | R-006, R-007 |
| NFR-005 | The system SHALL achieve hallucination rate <= 2% for LLM-assisted extractions | Below GPT-4o baseline per ACADEMIC-LITERATURE-REVIEW.md | STK-008 | Test (T) | Must | R-008 |

##### 2.2.3 Robustness Requirements (FMEA-Derived)

| ID | Requirement Statement | Rationale | Parent | V-Method | Priority | Risk Link |
|----|----------------------|-----------|--------|----------|----------|-----------|
| NFR-006 | The parser SHALL handle both period (.) and comma (,) as millisecond separators in timestamps | SRT format variation per R-002 | STK-002 | Test (T) | Must | R-002 |
| NFR-007 | The system SHALL detect and convert non-UTF8 character encodings (Windows-1252, ISO-8859-1) to UTF-8 | Encoding variation per R-003 | STK-001, STK-002 | Test (T) | Must | R-003 |
| NFR-008 | The speaker extraction module SHALL support at least 4 naming patterns (voice tag, prefix, bracket, all-caps) | Multiple patterns per R-004 | STK-003 | Test (T) | Must | R-004 |
| NFR-009 | The JSON output schema SHALL include version number starting with "1.0" | Schema evolution per R-014 | STK-010 | Inspection (I) | Must | R-014 |
| NFR-010 | All LLM-based extractions SHALL include source transcript span citations | Hallucination mitigation per R-008 | STK-008 | Test (T) | Must | R-008 |

#### 2.3 Interface Requirements (IR-xxx)

| ID | Requirement Statement | Rationale | Parent | V-Method | Priority | Risk Link |
|----|----------------------|-----------|--------|----------|----------|-----------|
| IR-001 | The system SHALL provide a command-line interface (CLI) as the primary interaction method | Developer-first design per 5W2H | STK-P1 | Demonstration (D) | Must | R-011 |
| IR-002 | The CLI SHALL follow POSIX conventions and clig.dev guidelines for command structure | Industry standard CLI UX | STK-P1, STK-010 | Inspection (I) | Must | R-011 |
| IR-003 | The CLI SHALL return exit code 0 for success, 1 for errors, and 2 for invalid usage | Enables scripting and CI/CD integration | STK-010 | Test (T) | Must | R-012 |
| IR-004 | The system SHALL provide a SKILL.md interface compatible with Jerry framework | Framework integration requirement | STK-S1 | Demonstration (D) | Must | R-015 |
| IR-005 | The system architecture SHALL conform to hexagonal architecture patterns with domain isolation | Jerry framework standard | STK-S1 | Analysis (A) | Must | R-016 |

---

### 3. Requirements Quality Assessment

#### 3.1 NASA-HDBK-1009A Quality Criteria

Each requirement is assessed against NASA's requirement quality criteria:

| Criterion | Definition | Verification Method |
|-----------|------------|---------------------|
| **Necessary** | Requirement defines essential capability | Trace to stakeholder need |
| **Appropriate** | Requirement is at correct level of abstraction | No implementation details |
| **Unambiguous** | Single interpretation possible | Peer review |
| **Complete** | Contains all needed information | Checklist review |
| **Singular** | Addresses single capability | No "and" conjunctions |
| **Feasible** | Technically achievable | Engineering assessment |
| **Verifiable** | Can be proven through A/D/I/T | V-method assigned |
| **Correct** | Accurately represents stakeholder need | Stakeholder review |
| **Conforming** | Follows conventions and standards | Template compliance |

#### 3.2 ADIT Verification Method Distribution

```
VERIFICATION METHOD DISTRIBUTION
================================

              Analysis  Demonstration  Inspection  Test
              ────────  ─────────────  ──────────  ────
FR-001..015      0           2            0        13
NFR-001..010     0           0            1         9
IR-001..005      1           2            1         1
              ────────────────────────────────────────
TOTAL            1           4            2        23

Percentages:  Analysis: 3%   Demonstration: 13%
              Inspection: 7%  Test: 77%

Test-heavy distribution appropriate for software requirements.
```

#### 3.3 MoSCoW Priority Distribution

```
PRIORITY DISTRIBUTION (MoSCoW)
==============================

MUST HAVE (M):     23 requirements (77%)
├── Critical path for MVP
├── Addresses 100% competitor gap (VTT/SRT)
└── Core value proposition (speakers, actions)

SHOULD HAVE (S):    7 requirements (23%)
├── Enhances user experience
├── Enables advanced workflows
└── Addressable in Phase 2 if needed

COULD HAVE (C):     0 requirements (0%)
└── Deferred to future phases

WON'T HAVE (W):     0 requirements (0%)
└── Out of scope for MVP

Priority Breakdown:
┌─────────────────────────────────────────────────────┐
│ MUST     ████████████████████████████████████  77%  │
│ SHOULD   ██████████  23%                            │
│ COULD    (none)                                     │
│ WON'T    (none)                                     │
└─────────────────────────────────────────────────────┘
```

---

## L2: Traceability and Risk Analysis

### 4. NPR 7123.1D Process 11: Requirements Management

#### 4.1 Bidirectional Traceability Matrix

```
FULL TRACEABILITY CHAIN
=======================

                    STAKEHOLDER        TECHNICAL          DESIGN           TEST
                       NEEDS          REQUIREMENTS       ELEMENTS         CASES
                    ──────────        ────────────       ────────         ─────

                    STK-001 ─────────► FR-001 ─────────► VTT Parser ────► TC-001
                        │             FR-003 ─────────► Plain Parser ──► TC-003
                        │             FR-004 ─────────► Format Det. ───► TC-004
                        │             NFR-007 ────────► Encoding Det. ─► TC-N07
                        │
                    STK-002 ─────────► FR-002 ─────────► SRT Parser ────► TC-002
                        │             FR-003 ─────────► Plain Parser ──► TC-003
                        │             NFR-006 ────────► Timestamp Norm ► TC-N06
                        │             NFR-007 ────────► Encoding Det. ─► TC-N07
                        │
                    STK-003 ─────────► FR-005 ─────────► Voice Tag Ext. ► TC-005
                        │             FR-006 ─────────► Pattern Matcher ► TC-006
                        │             NFR-003 ────────► Speaker F1 Test ► TC-N03
                        │             NFR-008 ────────► Pattern Suite ──► TC-N08
                        │
                    STK-004 ─────────► FR-007 ─────────► Action Extractor ► TC-007
                        │             FR-010 ─────────► NER Pipeline ───► TC-010
                        │             FR-011 ─────────► Confidence Scorer ► TC-011
                        │             NFR-004 ────────► Action F1 Test ─► TC-N04
                        │
                    STK-005 ─────────► FR-008 ─────────► Decision Extract ► TC-008
                        │             FR-010 ─────────► NER Pipeline ───► TC-010
                        │
                    STK-006 ─────────► FR-009 ─────────► Question Extract ► TC-009
                        │
                    STK-007 ─────────► NFR-001 ───────► Perf Optimization ► TC-N01
                        │             NFR-002 ───────► Memory Management ► TC-N02
                        │
                    STK-008 ─────────► FR-011 ─────────► Confidence Scorer ► TC-011
                        │             FR-014 ─────────► Citation Module ──► TC-014
                        │             NFR-004 ────────► Action F1 Test ─► TC-N04
                        │             NFR-005 ────────► Hallucination Test ► TC-N05
                        │             NFR-010 ────────► Citation Valid. ─► TC-N10
                        │
                    STK-009 ─────────► IR-004 ─────────► SKILL.md ────────► TC-I04
                        │             IR-005 ─────────► Hexagonal Arch ──► TC-I05
                        │
                    STK-010 ─────────► FR-013 ─────────► JSON Formatter ──► TC-013
                        │             FR-015 ─────────► Filter Module ───► TC-015
                        │             IR-002 ─────────► CLI Structure ───► TC-I02
                        │             IR-003 ─────────► Exit Codes ──────► TC-I03
                        │             NFR-009 ────────► Schema Version ──► TC-N09
```

#### 4.2 Coverage Analysis

```
COVERAGE ANALYSIS
=================

Stakeholder Needs → Technical Requirements Coverage:
┌──────────────────────────────────────────────────────────────────┐
│ STK-001: VTT Processing       → 4 requirements  ████████ 100%   │
│ STK-002: SRT Processing       → 4 requirements  ████████ 100%   │
│ STK-003: Speaker ID           → 4 requirements  ████████ 100%   │
│ STK-004: Action Items         → 4 requirements  ████████ 100%   │
│ STK-005: Decisions            → 2 requirements  ████     100%   │
│ STK-006: Questions            → 1 requirement   ██       100%   │
│ STK-007: Performance          → 2 requirements  ████     100%   │
│ STK-008: Trust/Confidence     → 5 requirements  ██████████ 100% │
│ STK-009: Jerry Integration    → 2 requirements  ████     100%   │
│ STK-010: Pipeline/Automation  → 5 requirements  ██████████ 100% │
└──────────────────────────────────────────────────────────────────┘

TOTAL: 33 requirement allocations across 10 stakeholder needs
COVERAGE: 100% (No orphan needs)

Orphan Requirements Analysis:
┌──────────────────────────────────────────────────────────────────┐
│ Requirements without Stakeholder Need parent:  0                 │
│ Stakeholder Needs without Technical Requirements:  0             │
│                                                                  │
│ STATUS: FULLY TRACED - No orphan requirements detected           │
└──────────────────────────────────────────────────────────────────┘
```

#### 4.3 Requirements-to-Risk Linkage

| Requirement | Linked Risk(s) | Risk Level | Mitigation Reflected |
|-------------|----------------|------------|---------------------|
| FR-001 | R-001 (VTT edge cases) | GREEN | Test corpus with diverse samples |
| FR-002 | R-002 (SRT timestamps) | YELLOW | Timestamp normalization |
| FR-005, FR-006 | R-004 (Missing voice tags) | YELLOW | Multi-pattern fallback |
| FR-007 | R-006, R-007 (Precision/Recall) | YELLOW | Confidence scores, hybrid approach |
| FR-011, FR-014 | R-008 (Hallucination) | YELLOW | Citation requirement |
| FR-013 | R-014 (Schema changes) | YELLOW | Version in schema |
| NFR-001 | R-017 (Processing time) | GREEN | Performance target |
| NFR-002 | R-018 (Memory exhaustion) | GREEN | Memory limit |
| IR-003 | R-012 (Exit codes) | GREEN | Standard codes |
| IR-004, IR-005 | R-015, R-016 (Jerry integration) | GREEN | Architecture compliance |

```
RISK COVERAGE BY REQUIREMENTS
=============================

YELLOW Risks (Require Mitigation):
┌─────────────────────────────────────────────────────────────────────┐
│ R-002 (SRT timestamps)      → NFR-006            ██████████ 100%   │
│ R-004 (Voice tag missing)   → FR-005,FR-006,NFR-008 ████████ 100%  │
│ R-006 (Low precision)       → FR-007,FR-011,NFR-004 ████████ 100%  │
│ R-007 (Low recall)          → FR-007,FR-011,NFR-004 ████████ 100%  │
│ R-008 (Hallucination)       → FR-014,NFR-005,NFR-010 ███████ 100%  │
│ R-014 (Schema breaking)     → NFR-009            ██████████ 100%   │
└─────────────────────────────────────────────────────────────────────┘

ALL YELLOW RISKS HAVE REQUIREMENTS COVERAGE: YES
```

#### 4.4 Design Element Allocation

```
REQUIREMENTS → DESIGN ELEMENT ALLOCATION
========================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                           DOMAIN LAYER                                       │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ Transcript Aggregate (FR-001..004)                                     │  │
│  │ ├── TranscriptSegment (Value Object)                                   │  │
│  │ ├── Speaker (Value Object)                                             │  │
│  │ └── TranscriptMetadata (Value Object)                                  │  │
│  │                                                                         │  │
│  │ ExtractedEntity Aggregate (FR-005..011)                                │  │
│  │ ├── EntityType (Enum: SPEAKER, ACTION, DECISION, QUESTION, PERSON...)  │  │
│  │ ├── Confidence (Value Object: 0.0-1.0)                                 │  │
│  │ └── SourceCitation (Value Object) ← FR-014, NFR-010                    │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                         APPLICATION LAYER                                    │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ Commands:                                                               │  │
│  │ ├── ParseTranscriptCommand (FR-001..004)                               │  │
│  │ ├── ExtractEntitiesCommand (FR-005..011)                               │  │
│  │ └── GenerateOutputCommand (FR-012..015)                                │  │
│  │                                                                         │  │
│  │ Queries:                                                                │  │
│  │ ├── GetTranscriptSummaryQuery                                          │  │
│  │ └── FilterEntitiesByTypeQuery (FR-015)                                 │  │
│  │                                                                         │  │
│  │ Ports (Secondary):                                                      │  │
│  │ ├── ITranscriptParser                                                   │  │
│  │ ├── IEntityExtractor                                                    │  │
│  │ └── IOutputFormatter                                                    │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                       INFRASTRUCTURE LAYER                                   │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ Adapters (Persistence):                                                 │  │
│  │ ├── VTTParserAdapter (FR-001, NFR-006, NFR-007) ← webvtt-py           │  │
│  │ ├── SRTParserAdapter (FR-002, NFR-006, NFR-007) ← srt library         │  │
│  │ └── PlainTextParserAdapter (FR-003)                                    │  │
│  │                                                                         │  │
│  │ Adapters (External):                                                    │  │
│  │ ├── SpaCyNERAdapter (FR-010)                                           │  │
│  │ ├── PatternMatcherAdapter (FR-005, FR-006, NFR-008)                   │  │
│  │ ├── ActionItemExtractorAdapter (FR-007, NFR-004)                       │  │
│  │ └── LLMExtractionAdapter (NFR-005, NFR-010) ← Optional                │  │
│  │                                                                         │  │
│  │ Adapters (Output):                                                      │  │
│  │ ├── MarkdownFormatter (FR-012)                                         │  │
│  │ └── JSONFormatter (FR-013, NFR-009)                                    │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                         INTERFACE LAYER                                      │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ CLI Adapter (IR-001, IR-002, IR-003):                                  │  │
│  │ ├── transcript parse <file> [--format]                                 │  │
│  │ ├── transcript extract <file> [--entities] [--format]                  │  │
│  │ └── transcript --help | --version                                      │  │
│  │                                                                         │  │
│  │ Skill Interface (IR-004, IR-005):                                       │  │
│  │ └── SKILL.md (Jerry Framework Integration)                             │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 5. Derived Requirements from Analysis

The following requirements are derived from problem-solving analyses:

#### 5.1 Derived from 5W2H Analysis

| Derived Req | Originating Analysis | Requirement Statement |
|-------------|---------------------|----------------------|
| FR-001, FR-002 | 5W2H: WHAT (Input Formats) | VTT/SRT parsing requirements |
| STK-P1..P3 | 5W2H: WHO (Personas) | Developer/Manager/Analyst stakeholder needs |
| NFR-001 | 5W2H: HOW MUCH (Performance) | <10s processing target |
| IR-001 | 5W2H: HOW (CLI Design) | CLI-first interface |

#### 5.2 Derived from Ishikawa Analysis

| Derived Req | Root Cause Category | Requirement Statement |
|-------------|---------------------|----------------------|
| FR-001, FR-002 | MACHINE: No VTT/SRT parsers | Build parser capability (addresses root cause) |
| NFR-008 | MATERIAL: Speaker tag inconsistency | Support 4+ naming patterns |
| NFR-007 | MATERIAL: Encoding issues | Character encoding detection |

#### 5.3 Derived from 8D Analysis

| Derived Req | Corrective Action | Requirement Statement |
|-------------|-------------------|----------------------|
| FR-001, FR-002 | CA-2: Robust Format Parsing | Parser requirements with error tolerance |
| FR-005, FR-006 | CA-2: VTT/SRT Parser Reqs | Speaker extraction patterns |
| FR-007 | CA-3: NLP Stack Selection | Action item extraction with benchmarks |
| IR-001, IR-002 | CA-4: User Workflow | CLI interface requirements |

#### 5.4 Derived from Pareto Analysis

| Derived Req | Pareto Feature | Value Contribution | Priority |
|-------------|----------------|-------------------|----------|
| FR-001, FR-002 | VTT/SRT Import | 35% | Must |
| FR-005, FR-006 | Speaker Identification | 25% | Must |
| FR-007 | Action Item Extraction | 20% | Must |
| IR-001 | CLI Interface | 10% | Must |

**Cumulative**: These 4 features = 90% of value (Pareto principle validated)

#### 5.5 Derived from FMEA Analysis

| Derived Req | Originating Risk | Score | Requirement Statement |
|-------------|-----------------|-------|----------------------|
| NFR-006 | R-002 (SRT timestamps) | 8 | Handle both . and , separators |
| NFR-007 | R-003 (Encoding) | 6 | Detect/convert non-UTF8 |
| NFR-008 | R-004 (Voice tags) | 12 | Support 4+ naming patterns |
| NFR-004, FR-011 | R-006 (Low precision) | 12 | Confidence scores |
| NFR-010, FR-014 | R-008 (Hallucination) | 12 | Source citations required |
| NFR-009 | R-014 (Schema breaking) | 9 | JSON schema versioning |
| NFR-001 | R-017 (Processing time) | 6 | <10s target |

### 6. Implementation Phase Alignment

```
REQUIREMENTS → IMPLEMENTATION PHASE MAPPING
===========================================

PHASE 1: FOUNDATION (Weeks 1-2)
├── FR-001: VTT Parser                    [Must]
├── FR-002: SRT Parser                    [Must]
├── FR-003: Plain Text Parser             [Should]
├── FR-004: Auto-detect Format            [Should]
├── NFR-006: Timestamp Normalization      [Must]
├── NFR-007: Encoding Detection           [Must]
├── IR-001: CLI Interface                 [Must]
├── IR-002: POSIX Conventions             [Must]
└── IR-003: Exit Codes                    [Must]

PHASE 2: CORE EXTRACTION (Weeks 3-6)
├── FR-005: Voice Tag Extraction          [Must]
├── FR-006: Pattern-based Speaker ID      [Must]
├── FR-007: Action Item Extraction        [Must]
├── FR-010: Standard NER                  [Must]
├── FR-011: Confidence Scores             [Must]
├── NFR-003: Speaker F1 >= 0.95           [Must]
├── NFR-004: Action F1 >= 0.80            [Must]
└── NFR-008: 4+ Speaker Patterns          [Must]

PHASE 3: INTEGRATION (Weeks 7-8)
├── FR-008: Decision Extraction           [Should]
├── FR-009: Question Extraction           [Should]
├── FR-012: Markdown Output               [Must]
├── FR-013: JSON Output                   [Must]
├── FR-014: Source Citations              [Must]
├── FR-015: Entity Filtering              [Should]
├── IR-004: SKILL.md Interface            [Must]
├── IR-005: Hexagonal Architecture        [Must]
├── NFR-009: Schema Versioning            [Must]
└── NFR-010: LLM Citation Validation      [Must]

PHASE 4: VALIDATION (Weeks 9-10)
├── NFR-001: Performance Validation       [Must]
├── NFR-002: Memory Validation            [Must]
└── NFR-005: Hallucination Rate Test      [Must]

Phase Allocation Summary:
┌─────────────────────────────────────────────────────────────────┐
│ Phase 1 (Foundation):    9 requirements   ██████████ 30%       │
│ Phase 2 (Core):          8 requirements   ████████   27%       │
│ Phase 3 (Integration):  10 requirements   ██████████ 33%       │
│ Phase 4 (Validation):    3 requirements   ███        10%       │
└─────────────────────────────────────────────────────────────────┘
```

### 7. Verification and Validation Strategy

#### 7.1 Test Case Mapping

| Requirement | Test Case ID | Test Type | Description |
|-------------|--------------|-----------|-------------|
| FR-001 | TC-001 | Unit | Parse valid VTT files |
| FR-002 | TC-002 | Unit | Parse valid SRT files |
| FR-005 | TC-005 | Unit | Extract speakers from voice tags |
| FR-006 | TC-006 | Unit | Extract speakers from patterns |
| FR-007 | TC-007 | Integration | Action item extraction pipeline |
| NFR-001 | TC-N01 | Performance | Processing time benchmark |
| NFR-003 | TC-N03 | Accuracy | Speaker F1 on test corpus |
| NFR-004 | TC-N04 | Accuracy | Action item F1 on AMI subset |
| NFR-005 | TC-N05 | Accuracy | Hallucination rate on labeled data |

#### 7.2 Acceptance Test Scenarios

```
ACCEPTANCE TEST SCENARIOS
=========================

SCENARIO 1: Basic VTT Processing
Given a valid VTT file with voice tags
When the user runs "transcript extract meeting.vtt"
Then speakers are identified with F1 >= 0.95
And action items are extracted with F1 >= 0.80
And processing completes in < 10 seconds
And exit code is 0

SCENARIO 2: SRT with Timestamp Variations
Given an SRT file using period as millisecond separator
When the user runs "transcript extract meeting.srt"
Then the file is parsed successfully
And timestamps are normalized correctly
And entities are extracted

SCENARIO 3: JSON Output with Schema Version
Given any valid transcript file
When the user runs "transcript extract meeting.vtt --format json"
Then output is valid JSON
And output contains "version": "1.0"
And all entities have source citations

SCENARIO 4: Entity Filtering
Given a transcript with multiple entity types
When the user runs "transcript extract meeting.vtt --entities action-items"
Then only action items are returned
And other entity types are excluded

SCENARIO 5: Confidence Threshold
Given a transcript with varying extraction confidence
When the user examines the output
Then all entities have confidence scores (0.0-1.0)
And users can filter by confidence threshold
```

---

## Appendices

### Appendix A: Glossary of Terms

| Term | Definition |
|------|------------|
| **VTT** | WebVTT (Web Video Text Tracks) - W3C standard for timed text |
| **SRT** | SubRip Text - De facto standard subtitle format |
| **NER** | Named Entity Recognition - ML task to identify entities in text |
| **F1 Score** | Harmonic mean of precision and recall |
| **ADIT** | Analysis, Demonstration, Inspection, Test - verification methods |
| **MoSCoW** | Must, Should, Could, Won't - prioritization framework |
| **Stakeholder Need** | High-level expression of what a stakeholder requires |
| **Technical Requirement** | System capability expressed as SHALL statement |
| **Hallucination** | LLM generating content not present in source material |

### Appendix B: Reference Documents

| Document | Type | Key Contribution |
|----------|------|------------------|
| 5W2H-ANALYSIS.md | Problem-Solving | Scope definition, personas, performance targets |
| ISHIKAWA-DIAGRAM.md | Root Cause | 24 root causes identified, 6M categories |
| 8D-PROBLEM-SOLVING.md | Corrective Actions | ADR-001..003, implementation phases |
| PARETO-ANALYSIS.md | Prioritization | Vital few features (80/20) |
| FMEA-ANALYSIS.md | Risk Assessment | 20 failure modes, 5 YELLOW risks |
| FEATURE-MATRIX.md | Market Analysis | 100% competitor gap identified |
| VTT-SPECIFICATION.md | Technical Standard | W3C WebVTT compliance |
| SRT-SPECIFICATION.md | Technical Standard | De facto SRT standard |
| NLP-NER-BEST-PRACTICES.md | Technical Guide | Pipeline architecture |
| ACADEMIC-LITERATURE-REVIEW.md | Research | F1 benchmarks, hallucination rates |

### Appendix C: Standards Compliance

| Standard | Section | Compliance |
|----------|---------|------------|
| NPR 7123.1D | Process 1: Stakeholder Expectations | COMPLIANT - 10 needs defined |
| NPR 7123.1D | Process 2: Technical Requirements | COMPLIANT - 30 requirements |
| NPR 7123.1D | Process 11: Requirements Management | COMPLIANT - Full traceability |
| NASA-HDBK-1009A | Section 4: Quality Attributes | COMPLIANT - ADIT assigned |
| NASA-HDBK-1009A | Section 5: Traceability | COMPLIANT - Bidirectional |

### Appendix D: Requirement Change Control

| Field | Value |
|-------|-------|
| **Change Authority** | Human Stakeholder (User) |
| **Review Frequency** | Per sprint (2-week cycles) |
| **Change Process** | 1. Propose change, 2. Impact analysis, 3. Approval, 4. Update baseline |
| **Baseline Version** | 1.0 (this document) |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-25 | nse-requirements agent | Initial requirements specification |

---

## Review Checklist (for ps-critic)

- [ ] All requirements traceable to stakeholder needs
- [ ] All requirements have verification method (A/D/I/T)
- [ ] All FMEA YELLOW risks have requirement coverage
- [ ] No orphan requirements detected
- [ ] MoSCoW priorities assigned
- [ ] Phase allocation complete
- [ ] Design element mapping complete
- [ ] Requirements follow NASA quality criteria
- [ ] ASCII diagrams render correctly
- [ ] All citations/sources provided

---

*End of NASA SE Requirements Specification*
