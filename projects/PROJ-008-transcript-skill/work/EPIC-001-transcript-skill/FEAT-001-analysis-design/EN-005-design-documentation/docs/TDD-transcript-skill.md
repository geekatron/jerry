# Technical Design Document: Transcript Skill Overview

> **Document ID:** TDD-transcript-skill
> **Version:** 1.0
> **Status:** DRAFT
> **Date:** 2026-01-26
> **Author:** ps-architect agent
> **Token Count:** ~14,500 (within 15K target per ADR-002)
> **Parent:** EN-005 Design Documentation

---

## Document Navigation

| Level | Audience | Sections |
|-------|----------|----------|
| **L0** | Executive / Stakeholders | [Executive Summary](#l0-executive-summary) |
| **L1** | Software Engineers | [Technical Architecture](#l1-technical-architecture) |
| **L2** | Principal Architects | [Strategic Design](#l2-strategic-design) |

---

# L0: Executive Summary

## The Translation Office Analogy

Imagine a **Translation Office** that receives meeting recordings in different languages (file formats) and produces organized reports with who said what, action items, and key decisions.

```
THE TRANSCRIPT SKILL AS A TRANSLATION OFFICE
=============================================

                   ┌───────────────────────────────────────────────────┐
                   │              TRANSCRIPT SKILL                      │
                   │          "The Translation Office"                  │
                   └───────────────────────────────────────────────────┘
                                        │
        ┌───────────────────────────────┼───────────────────────────────┐
        │                               │                               │
        ▼                               ▼                               ▼
┌───────────────┐             ┌───────────────┐              ┌───────────────┐
│   RECEPTION   │             │  TRANSLATORS  │              │   REPORTERS   │
│   DESK        │             │  (Extractors) │              │   (Formatters)│
│ ─────────────  │             │ ─────────────  │              │ ─────────────  │
│               │             │               │              │               │
│ • Accepts any │────────────►│ • Identify    │─────────────►│ • Write       │
│   format      │             │   speakers    │              │   reports     │
│ • Detects     │             │ • Find action │              │ • Create      │
│   language    │             │   items       │              │   summaries   │
│ • Prepares    │             │ • Mark        │              │ • Add         │
│   documents   │             │   decisions   │              │   citations   │
│               │             │               │              │               │
└───────────────┘             └───────────────┘              └───────────────┘
    ts-parser                   ts-extractor                  ts-formatter
```

**Key Value Proposition:**
- **VTT/SRT Import** (35% value): No competitor supports text-first transcripts
- **Speaker Identification** (25% value): Know who said what
- **Action Item Extraction** (20% value): Never miss a follow-up

**Total:** These three features deliver **80% of user value** (Pareto Principle).

## Business Justification

| Metric | Target | Source |
|--------|--------|--------|
| Processing Time | < 10 seconds (1-hour transcript) | 5W2H Analysis |
| Speaker ID Accuracy | F1 >= 0.95 | FMEA R-004 |
| Action Item F1 | >= 0.80 | FMEA R-006/R-007 |
| Hallucination Rate | <= 2% | FMEA R-008 |
| Market Gap Addressed | 100% (no competitor) | EN-001 |

## What This Document Covers

This TDD establishes:
1. **System Architecture** - Three-agent design (parser, extractor, formatter)
2. **Data Flow** - How transcripts become structured output
3. **Requirements Traceability** - All 40 requirements mapped
4. **ADR Compliance** - All 5 architectural decisions implemented

---

# L1: Technical Architecture

## 1. System Context (C4 Level 1)

```
C4 SYSTEM CONTEXT DIAGRAM
=========================

┌─────────────────────────────────────────────────────────────────────────────┐
│                           EXTERNAL ENVIRONMENT                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌──────────────┐                              ┌──────────────┐            │
│   │  Developer   │                              │   Manager    │            │
│   │  Persona     │                              │   Persona    │            │
│   └──────┬───────┘                              └──────┬───────┘            │
│          │                                             │                     │
│          │  /transcript <file>                         │  Reviews output     │
│          │                                             │                     │
│          ▼                                             ▼                     │
│   ┌─────────────────────────────────────────────────────────────────┐       │
│   │                                                                  │       │
│   │                    TRANSCRIPT SKILL                              │       │
│   │                                                                  │       │
│   │  "Processes VTT/SRT transcripts to extract speakers,           │       │
│   │   action items, decisions, and questions with citations"        │       │
│   │                                                                  │       │
│   └───────────────────────────┬─────────────────────────────────────┘       │
│                               │                                              │
│          ┌────────────────────┼────────────────────┐                        │
│          │                    │                    │                        │
│          ▼                    ▼                    ▼                        │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│   │ File System  │    │    spaCy     │    │   Claude     │                  │
│   │  (Input)     │    │   (NLP)      │    │   (LLM)      │                  │
│   └──────────────┘    └──────────────┘    └──────────────┘                  │
│     VTT, SRT,          en_core_web_sm      Optional path                    │
│     Plain Text         NER processing      for accuracy                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 2. Container Diagram (C4 Level 2)

```
C4 CONTAINER DIAGRAM
====================

┌─────────────────────────────────────────────────────────────────────────────┐
│                         TRANSCRIPT SKILL                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                          INTERFACE LAYER                               │ │
│  │ ──────────────────────────────────────────────────────────────────────  │ │
│  │                                                                        │ │
│  │   ┌──────────────────┐        ┌──────────────────┐                    │ │
│  │   │    SKILL.md      │        │   CLI Adapter    │                    │ │
│  │   │ ────────────────  │        │ ────────────────  │                    │ │
│  │   │ Jerry interface  │        │ /transcript cmd  │                    │ │
│  │   │ Natural language │        │ POSIX compliant  │                    │ │
│  │   └────────┬─────────┘        └────────┬─────────┘                    │ │
│  │            │                           │                              │ │
│  └────────────┼───────────────────────────┼──────────────────────────────┘ │
│               │                           │                                │
│               ▼                           ▼                                │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                        APPLICATION LAYER                               │ │
│  │ ──────────────────────────────────────────────────────────────────────  │ │
│  │                                                                        │ │
│  │   ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐  │ │
│  │   │   ts-parser      │   │   ts-extractor   │   │   ts-formatter   │  │ │
│  │   │ ────────────────  │   │ ────────────────  │   │ ────────────────  │  │ │
│  │   │ Agent            │   │ Agent            │   │ Agent            │  │ │
│  │   │ VTT/SRT parsing  │──►│ Entity extraction│──►│ Output generation│  │ │
│  │   │ Format detection │   │ Speaker ID       │   │ Markdown/JSON    │  │ │
│  │   │ Normalization    │   │ Action items     │   │ Citations        │  │ │
│  │   └──────────────────┘   └──────────────────┘   └──────────────────┘  │ │
│  │                                                                        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                          DOMAIN LAYER                                  │ │
│  │ ──────────────────────────────────────────────────────────────────────  │ │
│  │                                                                        │ │
│  │   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │ │
│  │   │  Transcript  │  │ Utterance    │  │ Extracted    │               │ │
│  │   │  Aggregate   │  │ Value Object │  │ Entity       │               │ │
│  │   └──────────────┘  └──────────────┘  └──────────────┘               │ │
│  │                                                                        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                      INFRASTRUCTURE LAYER                              │ │
│  │ ──────────────────────────────────────────────────────────────────────  │ │
│  │                                                                        │ │
│  │   ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐  │ │
│  │   │  VTT Parser      │   │  SRT Parser      │   │  spaCy Adapter   │  │ │
│  │   │  Adapter         │   │  Adapter         │   │                  │  │ │
│  │   └──────────────────┘   └──────────────────┘   └──────────────────┘  │ │
│  │                                                                        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

LEGEND:
───────
[ Agent ]  = Prompt-based worker (per ADR-005)
[ Adapter ] = Infrastructure port implementation
──►        = Data flow direction
```

## 3. Component Diagram (C4 Level 3)

```
C4 COMPONENT DIAGRAM: THREE-AGENT ARCHITECTURE
==============================================

                         INPUT
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TS-PARSER AGENT                                      │
│ ────────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐        │
│  │  FormatDetector  │   │  VTTProcessor    │   │  Normalizer      │        │
│  │ ────────────────  │   │ ────────────────  │   │ ────────────────  │        │
│  │ • Magic bytes    │──►│ • WEBVTT header  │──►│ • Timestamps     │        │
│  │ • Header check   │   │ • Cue parsing    │   │ • Encoding       │        │
│  │ • Extension      │   │ • Voice tags     │   │ • Segments       │        │
│  └──────────────────┘   └──────────────────┘   └──────────────────┘        │
│           │                                            │                     │
│           │             ┌──────────────────┐           │                     │
│           └────────────►│  SRTProcessor    │───────────┘                     │
│                         │ ────────────────  │                                 │
│                         │ • Index numbers  │                                 │
│                         │ • Timestamp      │                                 │
│                         │ • Text block     │                                 │
│                         └──────────────────┘                                 │
│                                                                              │
│  OUTPUT: CanonicalTranscript (JSON)                                         │
│  ─────────────────────────────────                                          │
│  {                                                                           │
│    "format": "vtt|srt|plain",                                               │
│    "segments": [ { "speaker": "?", "text": "...", "start": 0.0 } ]          │
│  }                                                                           │
└──────────────────────────────────────────────────┬──────────────────────────┘
                                                   │
                                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       TS-EXTRACTOR AGENT                                     │
│ ────────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐        │
│  │  SpeakerDetector │   │  ActionExtractor │   │  DecisionFinder  │        │
│  │ ────────────────  │   │ ────────────────  │   │ ────────────────  │        │
│  │ • Voice tags     │   │ • TIER 1: Rules  │   │ • Explicit       │        │
│  │ • Prefix pattern │   │ • TIER 2: ML     │   │   keywords       │        │
│  │ • Bracket        │   │ • TIER 3: LLM    │   │ • Context        │        │
│  │ • ALL CAPS       │   │ • Confidence     │   │   analysis       │        │
│  └──────────────────┘   └──────────────────┘   └──────────────────┘        │
│           │                     │                      │                     │
│           └─────────────────────┴──────────────────────┘                     │
│                                 │                                            │
│                                 ▼                                            │
│                    ┌──────────────────────┐                                 │
│                    │  ConfidenceScorer    │                                 │
│                    │ ──────────────────    │                                 │
│                    │ • Score 0.0-1.0      │                                 │
│                    │ • Source citations   │                                 │
│                    └──────────────────────┘                                 │
│                                                                              │
│  OUTPUT: ExtractedEntities (JSON)                                           │
│  ───────────────────────────────                                            │
│  {                                                                           │
│    "speakers": [ { "id": "S001", "name": "Alice", "utterances": [...] } ],  │
│    "action_items": [ { "text": "...", "assignee": "...", "conf": 0.85 } ],  │
│    "decisions": [ { "text": "...", "context": "...", "conf": 0.90 } ]       │
│  }                                                                           │
└──────────────────────────────────────────────────┬──────────────────────────┘
                                                   │
                                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       TS-FORMATTER AGENT                                     │
│ ────────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐        │
│  │  MarkdownWriter  │   │  JSONWriter      │   │  CitationLinker  │        │
│  │ ────────────────  │   │ ────────────────  │   │ ────────────────  │        │
│  │ • Human readable │   │ • Schema v1.0    │   │ • Source spans   │        │
│  │ • Tables         │   │ • Machine parse  │   │ • Anchor links   │        │
│  │ • Sections       │   │ • Validation     │   │ • Backlinks      │        │
│  └──────────────────┘   └──────────────────┘   └──────────────────┘        │
│                                                                              │
│  OUTPUT: Formatted Report (Markdown or JSON)                                │
│  ──────────────────────────────────────────                                 │
│  # Meeting Summary                                                           │
│  ## Speakers                                                                 │
│  - Alice (15 utterances)                                                    │
│  ## Action Items                                                             │
│  - [ ] Alice to review PR [00:05:23](#ts-323)                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 4. Data Flow Sequence

```
SEQUENCE DIAGRAM: TRANSCRIPT PROCESSING
=======================================

User          SKILL.md      ts-parser     ts-extractor   ts-formatter    Output
 │               │              │               │              │            │
 │ /transcript   │              │               │              │            │
 │ analyze       │              │               │              │            │
 │ <file>        │              │               │              │            │
 │──────────────►│              │               │              │            │
 │               │ invoke       │               │              │            │
 │               │──────────────►              │              │            │
 │               │              │               │              │            │
 │               │              │ detect format │              │            │
 │               │              │───────────┐   │              │            │
 │               │              │           │   │              │            │
 │               │              │◄──────────┘   │              │            │
 │               │              │               │              │            │
 │               │              │ parse         │              │            │
 │               │              │───────────┐   │              │            │
 │               │              │           │   │              │            │
 │               │              │◄──────────┘   │              │            │
 │               │              │               │              │            │
 │               │              │ Canonical     │              │            │
 │               │              │ Transcript    │              │            │
 │               │              │──────────────►│              │            │
 │               │              │               │              │            │
 │               │              │               │ extract      │            │
 │               │              │               │ speakers     │            │
 │               │              │               │──────┐       │            │
 │               │              │               │      │       │            │
 │               │              │               │◄─────┘       │            │
 │               │              │               │              │            │
 │               │              │               │ extract      │            │
 │               │              │               │ actions      │            │
 │               │              │               │──────┐       │            │
 │               │              │               │      │       │            │
 │               │              │               │◄─────┘       │            │
 │               │              │               │              │            │
 │               │              │               │ Extracted    │            │
 │               │              │               │ Entities     │            │
 │               │              │               │─────────────►│            │
 │               │              │               │              │            │
 │               │              │               │              │ format     │
 │               │              │               │              │ output     │
 │               │              │               │              │────┐       │
 │               │              │               │              │    │       │
 │               │              │               │              │◄───┘       │
 │               │              │               │              │            │
 │               │              │               │              │ Formatted  │
 │               │              │               │              │ Report     │
 │               │              │               │              │───────────►│
 │               │              │               │              │            │
 │◄─────────────────────────────────────────────────────────────────────────│
 │  Output file created                                                      │
 │                                                                           │
```

## 5. Domain Model

```
DOMAIN MODEL: TRANSCRIPT SKILL
==============================

┌──────────────────────────────────────────────────────────────────────────┐
│                           AGGREGATES                                      │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│   ┌────────────────────────────────┐                                     │
│   │        Transcript              │                                     │
│   │ ──────────────────────────────  │                                     │
│   │ + id: TranscriptId             │                                     │
│   │ + source_format: Format        │                                     │
│   │ + segments: List[Segment]      │                                     │
│   │ + metadata: TranscriptMetadata │                                     │
│   │ ──────────────────────────────  │                                     │
│   │ + parse(file): Transcript      │                                     │
│   │ + normalize(): Transcript      │                                     │
│   └────────────────┬───────────────┘                                     │
│                    │ contains                                             │
│                    ▼                                                      │
│   ┌────────────────────────────────┐                                     │
│   │        ExtractionResult        │                                     │
│   │ ──────────────────────────────  │                                     │
│   │ + speakers: List[Speaker]      │                                     │
│   │ + action_items: List[Action]   │                                     │
│   │ + decisions: List[Decision]    │                                     │
│   │ + questions: List[Question]    │                                     │
│   │ ──────────────────────────────  │                                     │
│   │ + filter_by_type(): Result     │                                     │
│   │ + to_markdown(): str           │                                     │
│   │ + to_json(): dict              │                                     │
│   └────────────────────────────────┘                                     │
│                                                                           │
├──────────────────────────────────────────────────────────────────────────┤
│                         VALUE OBJECTS                                     │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│   ┌───────────────┐  ┌───────────────┐  ┌───────────────┐               │
│   │    Segment    │  │   Timestamp   │  │  Confidence   │               │
│   │ ─────────────  │  │ ─────────────  │  │ ─────────────  │               │
│   │ + speaker: ?  │  │ + start: f64  │  │ + score: f64  │               │
│   │ + text: str   │  │ + end: f64    │  │ + tier: int   │               │
│   │ + start: TS   │  │ + duration    │  │ + source: str │               │
│   │ + end: TS     │  └───────────────┘  └───────────────┘               │
│   └───────────────┘                                                      │
│                                                                           │
│   ┌───────────────┐  ┌───────────────┐  ┌───────────────┐               │
│   │   Speaker     │  │  ActionItem   │  │   Decision    │               │
│   │ ─────────────  │  │ ─────────────  │  │ ─────────────  │               │
│   │ + id: str     │  │ + text: str   │  │ + text: str   │               │
│   │ + name: str   │  │ + assignee: ? │  │ + context: str│               │
│   │ + utterances  │  │ + deadline: ? │  │ + participants│               │
│   │ + confidence  │  │ + confidence  │  │ + confidence  │               │
│   │ + citations   │  │ + citations   │  │ + citations   │               │
│   └───────────────┘  └───────────────┘  └───────────────┘               │
│                                                                           │
├──────────────────────────────────────────────────────────────────────────┤
│                          ENUMERATIONS                                     │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│   ┌───────────────┐  ┌───────────────┐  ┌───────────────┐               │
│   │    Format     │  │  EntityType   │  │ ExtractionTier│               │
│   │ ─────────────  │  │ ─────────────  │  │ ─────────────  │               │
│   │ VTT           │  │ SPEAKER       │  │ RULE_BASED    │               │
│   │ SRT           │  │ ACTION_ITEM   │  │ ML_BASED      │               │
│   │ PLAIN_TEXT    │  │ DECISION      │  │ LLM_BASED     │               │
│   │               │  │ QUESTION      │  │               │               │
│   │               │  │ PERSON        │  │               │               │
│   │               │  │ ORG           │  │               │               │
│   │               │  │ DATE          │  │               │               │
│   └───────────────┘  └───────────────┘  └───────────────┘               │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

## 6. Interface Contracts

### 6.1 ts-parser Input/Output

**Input:**
```
File path to transcript (VTT, SRT, or plain text)
```

**Output (Canonical Transcript JSON):**
```json
{
  "$schema": "transcript-skill/canonical-transcript-v1.0",
  "version": "1.0",
  "source": {
    "format": "vtt",
    "encoding": "utf-8",
    "file_path": "/path/to/file.vtt"
  },
  "metadata": {
    "duration_seconds": 3600,
    "segment_count": 150,
    "detected_speakers": 3
  },
  "segments": [
    {
      "id": "seg-001",
      "start": 0.0,
      "end": 5.5,
      "speaker": "Alice",
      "text": "Good morning everyone.",
      "raw_text": "<v Alice>Good morning everyone.</v>"
    }
  ]
}
```

### 6.2 ts-extractor Input/Output

**Input:** Canonical Transcript JSON from ts-parser

**Output (Extracted Entities JSON):**
```json
{
  "$schema": "transcript-skill/extracted-entities-v1.0",
  "version": "1.0",
  "speakers": [
    {
      "id": "S001",
      "name": "Alice",
      "detection_method": "voice_tag",
      "confidence": 0.99,
      "utterance_count": 45,
      "first_appearance": "seg-001"
    }
  ],
  "action_items": [
    {
      "id": "AI-001",
      "text": "Review the PR by Friday",
      "assignee": "Alice",
      "deadline": "2026-01-31",
      "confidence": 0.85,
      "extraction_tier": "rule_based",
      "citation": {
        "segment_id": "seg-042",
        "timestamp": "00:15:23",
        "span": "I'll review the PR by Friday"
      }
    }
  ],
  "decisions": [],
  "questions": []
}
```

### 6.3 ts-formatter Input/Output

**Input:** Extracted Entities JSON from ts-extractor

**Output Options:**

**Markdown (default):**
```markdown
# Meeting Analysis Report

## Speakers (3 identified)

| Speaker | Utterances | Confidence |
|---------|------------|------------|
| Alice   | 45         | 0.99       |
| Bob     | 32         | 0.95       |
| Carol   | 28         | 0.92       |

## Action Items (5 found)

- [ ] **Alice**: Review the PR by Friday [00:15:23](#seg-042) (confidence: 0.85)
- [ ] **Bob**: Update documentation [00:22:10](#seg-067) (confidence: 0.82)

## Citations

<a id="seg-042">00:15:23</a>: "I'll review the PR by Friday"
```

**JSON:**
```json
{
  "$schema": "transcript-skill/report-v1.0",
  "version": "1.0",
  "generated_at": "2026-01-26T10:00:00Z",
  "source_file": "/path/to/file.vtt",
  "speakers": [...],
  "action_items": [...],
  "decisions": [...],
  "questions": []
}
```

---

# L2: Strategic Design

## 7. Architectural Decisions Summary

| ADR | Decision | Impact | Implementation |
|-----|----------|--------|----------------|
| ADR-001 | Hybrid Architecture | Three specialized agents | ts-parser, ts-extractor, ts-formatter |
| ADR-002 | 35K Token Limit | File splitting strategy | ~15K per TDD, semantic boundaries |
| ADR-003 | Bidirectional Linking | Custom anchors | `<a id="req-001">` format |
| ADR-004 | Semantic Split | 31.5K soft limit | Split at section boundaries |
| ADR-005 | Phased Implementation | Prompt-first, Python later | AGENT.md files for Phase 1 |

## 8. Trade-offs Analysis

### 8.1 Accuracy vs. Speed

```
TRADE-OFF: ACCURACY VS. SPEED
=============================

                         SPEED-OPTIMIZED                 ACCURACY-OPTIMIZED
                         ──────────────                 ─────────────────

Processing Time          <3 seconds                      5-15 seconds
                              │                              │
                              ▼                              ▼
                    ┌─────────────────┐            ┌─────────────────┐
                    │   TIER 1 ONLY   │            │  TIER 1 + 2 + 3 │
                    │   Rule-based    │            │  Full pipeline  │
                    │                 │            │                 │
                    │ • Pattern match │            │ • Rules + ML    │
                    │ • Keywords      │            │ • + LLM verify  │
                    │ • F1 ~ 0.70     │            │ • F1 ~ 0.90+    │
                    └─────────────────┘            └─────────────────┘

                           │                              │
                           ▼                              ▼
                    ┌─────────────────┐            ┌─────────────────┐
                    │   USE CASE      │            │   USE CASE      │
                    │                 │            │                 │
                    │ Quick review    │            │ Formal minutes  │
                    │ Draft analysis  │            │ Compliance      │
                    │ Large batches   │            │ Critical docs   │
                    └─────────────────┘            └─────────────────┘

RESOLUTION: User selects via --mode=fast|accurate flag
            Default: fast (TIER 1 only)
            Opt-in:  accurate (TIER 1 + 2 + 3 with LLM)
```

### 8.2 Local-First vs. Cloud Accuracy

```
TRADE-OFF: LOCAL-FIRST VS. CLOUD ACCURACY
=========================================

LOCAL-FIRST (Default)              CLOUD-ENHANCED (Opt-in)
─────────────────────              ───────────────────────

Privacy:    Data stays local       Privacy:    Sent to LLM provider
Latency:    <3 seconds             Latency:    5-15 seconds
Cost:       Free                   Cost:       API charges
Accuracy:   F1 ~ 0.80              Accuracy:   F1 ~ 0.95
Offline:    Works offline          Offline:    Requires internet
Dependencies: spaCy only           Dependencies: Claude/GPT API

RESOLUTION:
- Default: Local-only processing
- Flag: --use-llm enables TIER 3
- All LLM extractions require citations (ADR-003)
- Hallucination rate monitored (NFR-005: <= 2%)
```

## 9. Risk Mitigations

### 9.1 YELLOW Risk Coverage

| Risk ID | Risk | Score | Mitigation Approach |
|---------|------|-------|---------------------|
| R-002 | SRT Timestamp Malformation | 8 | NFR-006: Support both `.` and `,` separators |
| R-004 | Missing VTT Voice Tags | 12 | FR-005, FR-006: 4+ pattern fallback chain |
| R-006 | Low Action Item Precision | 12 | FR-011: Confidence scores with thresholds |
| R-007 | Low Action Item Recall | 12 | Tiered extraction (PAT-001) |
| R-008 | LLM Hallucination | 12 | FR-014, NFR-010: Citation requirement |
| R-014 | JSON Schema Breaking | 9 | NFR-009: Version number from v1.0 |

### 9.2 Design Pattern Applications

| Pattern | Application | Risks Mitigated |
|---------|-------------|-----------------|
| PAT-001 Tiered Extraction | ts-extractor TIER 1/2/3 | R-006, R-007 |
| PAT-002 Defensive Parsing | ts-parser format detection | R-002, R-003 |
| PAT-003 Multi-Pattern Speaker | ts-extractor speaker ID | R-004 |
| PAT-004 Citation-Required | ts-formatter citations | R-008 |
| PAT-005 Versioned Schema | JSON output v1.0 | R-014 |
| PAT-006 Hexagonal Architecture | Domain isolation | IR-005 |

## 10. Evolution Strategy

### 10.1 Phase 1 → Phase 2 Migration Triggers

Per ADR-005, agents migrate from prompt-based to Python when:

| Trigger | Threshold | Measurement |
|---------|-----------|-------------|
| Performance | Response time > 5s consistently | Monitoring |
| Complexity | > 50 tool calls per invocation | Logs |
| Accuracy | Prompt instructions insufficient | Testing |
| Maintenance | > 3 bug fixes per month | Issue tracking |
| Integration | External API required | Requirements |

### 10.2 Extensibility Points

```
EXTENSIBILITY ARCHITECTURE
==========================

                         EXTENSION POINTS
                         ────────────────

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│  1. NEW FORMAT SUPPORT                                                  │
│     ───────────────────                                                 │
│     • Add new parser adapter implementing ITranscriptParser             │
│     • Register in FormatDetector                                        │
│     • Example: .ass subtitles, .sbv YouTube format                      │
│                                                                          │
│  2. NEW ENTITY TYPES                                                    │
│     ─────────────────                                                   │
│     • Extend EntityType enum                                            │
│     • Add extraction rules/patterns                                     │
│     • Example: RISK_ITEM, DEADLINE, REFERENCE                           │
│                                                                          │
│  3. NEW OUTPUT FORMATS                                                  │
│     ──────────────────                                                  │
│     • Add new formatter implementing IOutputFormatter                   │
│     • Register in output factory                                        │
│     • Example: HTML, PDF, JIRA ticket format                            │
│                                                                          │
│  4. CUSTOM EXTRACTION STRATEGIES                                        │
│     ────────────────────────────                                        │
│     • Add new tier to tiered extraction                                 │
│     • Implement IExtractionStrategy                                     │
│     • Example: Domain-specific models                                   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 11. Requirements Traceability Matrix (RTM)

### 11.1 Stakeholder Needs to Design Elements

| STK | Need | Design Element | TDD Section |
|-----|------|----------------|-------------|
| STK-001 | VTT processing | ts-parser VTTProcessor | TDD-ts-parser 3.1 |
| STK-002 | SRT processing | ts-parser SRTProcessor | TDD-ts-parser 3.2 |
| STK-003 | Speaker identification | ts-extractor SpeakerDetector | TDD-ts-extractor 3.1 |
| STK-004 | Action item extraction | ts-extractor ActionExtractor | TDD-ts-extractor 3.2 |
| STK-005 | Decision extraction | ts-extractor DecisionFinder | TDD-ts-extractor 3.3 |
| STK-006 | Question extraction | ts-extractor QuestionFinder | TDD-ts-extractor 3.4 |
| STK-007 | Performance | All agents, <10s target | This TDD 8.1 |
| STK-008 | Trust (confidence) | ts-extractor ConfidenceScorer | TDD-ts-extractor 3.5 |
| STK-009 | Jerry integration | SKILL.md interface | TDD-ts-formatter 4.1 |
| STK-010 | Pipeline automation | CLI adapter, exit codes | This TDD 6.3 |

### 11.2 Functional Requirements to Components

| FR | Requirement | Component | Agent |
|----|-------------|-----------|-------|
| FR-001 | VTT parsing | VTTProcessor | ts-parser |
| FR-002 | SRT parsing | SRTProcessor | ts-parser |
| FR-003 | Plain text | PlainTextProcessor | ts-parser |
| FR-004 | Format auto-detect | FormatDetector | ts-parser |
| FR-005 | Voice tag extraction | VoiceTagExtractor | ts-extractor |
| FR-006 | Pattern-based speaker | PatternMatcher | ts-extractor |
| FR-007 | Action item extraction | ActionExtractor | ts-extractor |
| FR-008 | Decision extraction | DecisionFinder | ts-extractor |
| FR-009 | Question extraction | QuestionFinder | ts-extractor |
| FR-010 | Standard NER | SpaCyAdapter | ts-extractor |
| FR-011 | Confidence scores | ConfidenceScorer | ts-extractor |
| FR-012 | Markdown output | MarkdownWriter | ts-formatter |
| FR-013 | JSON output | JSONWriter | ts-formatter |
| FR-014 | Source citations | CitationLinker | ts-formatter |
| FR-015 | Entity filtering | FilterEngine | ts-formatter |

### 11.3 Non-Functional Requirements to Design

| NFR | Requirement | Design Element | Verification |
|-----|-------------|----------------|--------------|
| NFR-001 | <10s for 1hr transcript | Tiered extraction default | Performance test |
| NFR-002 | <500 MB RAM | Streaming parser | Memory profiler |
| NFR-003 | Speaker F1 >= 0.95 | Multi-pattern detection | Benchmark test |
| NFR-004 | Action F1 >= 0.80 | Tiered extraction | Benchmark test |
| NFR-005 | Hallucination <= 2% | Citation requirement | A/B testing |
| NFR-006 | Timestamp normalization | Normalizer component | Unit test |
| NFR-007 | Encoding detection | EncodingDetector | Unit test |
| NFR-008 | 4+ speaker patterns | PatternMatcher registry | Unit test |
| NFR-009 | Schema versioning | JSON schema v1.0 | Schema validation |
| NFR-010 | LLM citation validation | CitationLinker verify | Integration test |

### 11.4 Interface Requirements to Implementation

| IR | Requirement | Implementation | Verification |
|----|-------------|----------------|--------------|
| IR-001 | CLI interface | cli_adapter.py | Demo |
| IR-002 | POSIX conventions | Argparse + conventions | Inspection |
| IR-003 | Exit codes | ExitCode enum | Unit test |
| IR-004 | SKILL.md interface | SKILL.md file | Demo |
| IR-005 | Hexagonal architecture | Domain isolation | Architecture test |

---

## 12. ADR Compliance Checklist

| ADR | Decision | Compliance Status | Evidence |
|-----|----------|-------------------|----------|
| ADR-001 | Hybrid Architecture (3 agents) | [x] Compliant | Section 3: ts-parser, ts-extractor, ts-formatter |
| ADR-002 | 35K Token Limit | [x] Compliant | Token count: ~14,500 (within 15K target) |
| ADR-003 | Bidirectional Linking | [x] Compliant | Section 11: RTM with anchor references |
| ADR-004 | Semantic Split (31.5K soft) | [x] Compliant | Single file, no split needed |
| ADR-005 | Phased Implementation | [x] Compliant | Agents defined as prompt-based AGENT.md |

---

## 13. Related Documents

### 13.1 Backlinks

This document is referenced by:
- [EN-005-design-documentation.md](../EN-005-design-documentation.md)
- [TASK-001-tdd-overview.md](../TASK-001-tdd-overview.md)
- [ORCHESTRATION_EN005.yaml](../ORCHESTRATION_EN005.yaml)

### 13.2 Forward Links

This document references:
- [TDD-ts-parser.md](./TDD-ts-parser.md) (TASK-002)
- [TDD-ts-extractor.md](./TDD-ts-extractor.md) (TASK-003)
- [TDD-ts-formatter.md](./TDD-ts-formatter.md) (TASK-004)
- [REQUIREMENTS-SPECIFICATION.md](../../EN-003-requirements-synthesis/requirements/REQUIREMENTS-SPECIFICATION.md)
- [ADR-001 through ADR-005](../../EN-004-architecture-decisions/research/)

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-26 | ps-architect agent | Initial TDD with C4 diagrams, RTM, ADR compliance |

---

*Document ID: TDD-transcript-skill*
*Workflow ID: en005-tdd-20260126-001*
*Constitutional Compliance: P-002 (persisted), P-004 (provenance), P-011 (evidence-based)*
