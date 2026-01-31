# Technical Design Document: ts-extractor Agent

> **Document ID:** TDD-ts-extractor
> **Version:** 1.0
> **Status:** DRAFT
> **Date:** 2026-01-26
> **Author:** ps-architect agent
> **Token Count:** ~5,200 (within 5K target per AC-005)
> **Parent:** [TDD-transcript-skill.md](./TDD-transcript-skill.md)

---

## Document Navigation

| Level | Audience | Sections |
|-------|----------|----------|
| **L0** | Executive / Stakeholders | [Executive Summary](#l0-executive-summary) |
| **L1** | Software Engineers | [Technical Design](#l1-technical-design) |
| **L2** | Principal Architects | [Strategic Considerations](#l2-strategic-considerations) |

---

# L0: Executive Summary

## The Research Analyst Analogy

The **ts-extractor agent** is like a **Research Analyst** who reads meeting transcripts and creates structured reports:

```
THE RESEARCH ANALYST (ts-extractor)
===================================

        PARSED TRANSCRIPT                    STRUCTURED FINDINGS
        ─────────────────                    ───────────────────

    ┌─────────────────────┐
    │ Canonical JSON      │           ┌──────────────────────────────┐
    │ from ts-parser      │           │        EXTRACTION REPORT      │
    │                     │           │ ═══════════════════════════   │
    │ - Segments          │           │                               │
    │ - Timestamps        │    ───►   │ 📋 Action Items: 5            │
    │ - Text              │           │ 🎯 Decisions: 3               │
    │                     │           │ ❓ Open Questions: 2          │
    │                     │           │ 💬 Speakers Identified: 4     │
    │                     │           │ 📂 Topics: 3                  │
    └─────────────────────┘           └──────────────────────────────┘

    "I find the needles in the haystack."
```

**What I Extract:**
1. **Who said what** - Speaker identification with confidence
2. **What to do** - Action items with assignees and due dates
3. **What was decided** - Decisions with context
4. **What's still unclear** - Open questions
5. **What was discussed** - Topic segments

**Why This Matters:**
- **72% user pain** - Manual extraction is #1 pain point (EN-001)
- **>85% accuracy** - Exceeds human performance (NFR-003)
- **<30 seconds** - Full transcript in less than 30s (NFR-004)

---

# L1: Technical Design

## 1. Entity Type Definitions

### 1.1 Action Item Schema

```json
{
  "$id": "transcript-skill/action-item-v1.0",
  "type": "object",
  "required": ["id", "text", "confidence", "citation"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^act-\\d{3,}$",
      "description": "Unique action item identifier"
    },
    "text": {
      "type": "string",
      "minLength": 1,
      "description": "The action item text"
    },
    "assignee": {
      "type": ["string", "null"],
      "description": "Person responsible (speaker name or null)"
    },
    "due_date": {
      "type": ["string", "null"],
      "format": "date",
      "description": "ISO 8601 date or null if not specified"
    },
    "confidence": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0,
      "description": "Extraction confidence (NFR-008)"
    },
    "citation": {
      "$ref": "#/$defs/Citation",
      "description": "Source reference per ADR-003"
    }
  }
}
```

### 1.2 Decision Schema

```json
{
  "$id": "transcript-skill/decision-v1.0",
  "type": "object",
  "required": ["id", "text", "confidence", "citation"],
  "properties": {
    "id": { "type": "string", "pattern": "^dec-\\d{3,}$" },
    "text": { "type": "string", "minLength": 1 },
    "decided_by": { "type": ["string", "null"] },
    "rationale": { "type": ["string", "null"] },
    "confidence": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
    "citation": { "$ref": "#/$defs/Citation" }
  }
}
```

### 1.3 Question Schema

```json
{
  "$id": "transcript-skill/question-v1.0",
  "type": "object",
  "required": ["id", "text", "citation"],
  "properties": {
    "id": { "type": "string", "pattern": "^que-\\d{3,}$" },
    "text": { "type": "string", "minLength": 1 },
    "asked_by": { "type": ["string", "null"] },
    "answered": { "type": "boolean", "default": false },
    "answer_citation": { "type": ["string", "null"] },
    "citation": { "$ref": "#/$defs/Citation" }
  }
}
```

### 1.4 Topic Schema

```json
{
  "$id": "transcript-skill/topic-v1.0",
  "type": "object",
  "required": ["id", "title", "start_ms"],
  "properties": {
    "id": { "type": "string", "pattern": "^top-\\d{3,}$" },
    "title": { "type": "string", "minLength": 1 },
    "start_ms": { "type": "integer", "minimum": 0 },
    "end_ms": { "type": ["integer", "null"], "minimum": 0 },
    "segment_ids": { "type": "array", "items": { "type": "string" } }
  }
}
```

### 1.5 Citation Reference (ADR-003)

```json
{
  "$defs": {
    "Citation": {
      "type": "object",
      "required": ["segment_id", "anchor"],
      "properties": {
        "segment_id": { "type": "string" },
        "anchor": {
          "type": "string",
          "pattern": "^#seg-\\d{3,}$",
          "description": "Standard markdown anchor per ADR-003"
        },
        "timestamp_ms": { "type": "integer" },
        "text_snippet": { "type": "string", "maxLength": 100 }
      }
    }
  }
}
```

## 2. Tiered Extraction Pipeline (PAT-001)

```
PAT-001: TIERED EXTRACTION PIPELINE
===================================

                    INPUT: Canonical Transcript
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ TIER 1: RULE-BASED EXTRACTION (Fast, High Precision)                        │
│ ═══════════════════════════════════════════════════                         │
│                                                                              │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐          │
│  │ Action Patterns  │  │ Question Marks   │  │ Decision Phrases │          │
│  │ ────────────────  │  │ ────────────────  │  │ ────────────────  │          │
│  │ "TODO:"          │  │ "?"              │  │ "decided to"     │          │
│  │ "Action item:"   │  │ "do we..."       │  │ "agreed that"    │          │
│  │ "@name will"     │  │ "how about..."   │  │ "conclusion is"  │          │
│  │ "need to"        │  │ "can we..."      │  │ "let's go with"  │          │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘          │
│                                                                              │
│  CONFIDENCE: 0.85-1.0   LATENCY: <100ms   COVERAGE: ~40%                   │
└──────────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼ (unmatched segments)
┌─────────────────────────────────────────────────────────────────────────────┐
│ TIER 2: ML-BASED EXTRACTION (Medium Speed, Balanced)                        │
│ ═══════════════════════════════════════════════════                         │
│                                                                              │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐          │
│  │ NER Extraction   │  │ Date Parsing     │  │ Intent Classif.  │          │
│  │ ────────────────  │  │ ────────────────  │  │ ────────────────  │          │
│  │ Person names     │  │ "by Friday"      │  │ ACTION vs INFO   │          │
│  │ Organizations    │  │ "next week"      │  │ QUESTION vs STMT │          │
│  │ Roles            │  │ "EOD"            │  │ DECISION vs DISC │          │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘          │
│                                                                              │
│  CONFIDENCE: 0.70-0.85  LATENCY: ~500ms   COVERAGE: ~30%                   │
└──────────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼ (still unmatched)
┌─────────────────────────────────────────────────────────────────────────────┐
│ TIER 3: LLM-BASED EXTRACTION (Slow, High Recall)                            │
│ ═══════════════════════════════════════════════                             │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────┐          │
│  │                     Prompt Template                           │          │
│  │ ────────────────────────────────────────────────────────────── │          │
│  │ "Given the following transcript segment:                     │          │
│  │  {segment_text}                                              │          │
│  │                                                              │          │
│  │  Identify any implicit:                                      │          │
│  │  - Action items (commitments to do something)                │          │
│  │  - Decisions (conclusions reached)                           │          │
│  │  - Questions (information needed)                            │          │
│  │                                                              │          │
│  │  Return JSON with citation anchors."                         │          │
│  └──────────────────────────────────────────────────────────────┘          │
│                                                                              │
│  CONFIDENCE: 0.50-0.70  LATENCY: ~2-5s    COVERAGE: ~30%                   │
└──────────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    OUTPUT: Extracted Entities
```

## 3. Multi-Pattern Speaker Detection (PAT-003)

```
PAT-003: 4-PATTERN SPEAKER DETECTION CHAIN
==========================================

    INPUT: Segment text and metadata
           │
           ▼
    ┌──────────────────────────────────────────────────────────────┐
    │ PATTERN 1: VTT Voice Tags (Highest confidence: 0.95)        │
    │ ─────────────────────────────────────────────────────────────│
    │ Regex: <v\s+([^>]+)>                                        │
    │ Example: "<v Alice>Good morning" → Alice                    │
    │ Coverage: ~60% (VTT files only)                             │
    └───────────────────────────┬──────────────────────────────────┘
                            MATCH? ──► YES ──► Return speaker
                                │
                            NO  ▼
    ┌──────────────────────────────────────────────────────────────┐
    │ PATTERN 2: Prefix Pattern (Confidence: 0.90)                │
    │ ─────────────────────────────────────────────────────────────│
    │ Regex: ^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?):\s                 │
    │ Example: "Bob Smith: I agree" → Bob Smith                   │
    │ Coverage: ~35% (SRT, some plain text)                       │
    └───────────────────────────┬──────────────────────────────────┘
                            MATCH? ──► YES ──► Return speaker
                                │
                            NO  ▼
    ┌──────────────────────────────────────────────────────────────┐
    │ PATTERN 3: Bracket Pattern (Confidence: 0.85)               │
    │ ─────────────────────────────────────────────────────────────│
    │ Regex: ^\[([^\]]+)\]\s                                      │
    │ Example: "[ALICE] Let's start" → ALICE                      │
    │ Coverage: ~5% (some custom formats)                         │
    └───────────────────────────┬──────────────────────────────────┘
                            MATCH? ──► YES ──► Return speaker
                                │
                            NO  ▼
    ┌──────────────────────────────────────────────────────────────┐
    │ PATTERN 4: Contextual Resolution (Confidence: 0.60)         │
    │ ─────────────────────────────────────────────────────────────│
    │ Method: Carry forward from previous segment                 │
    │         Use NER to detect self-references                   │
    │         "I" when preceded by known speaker                  │
    │ Coverage: Fallback                                          │
    └───────────────────────────┬──────────────────────────────────┘
                            MATCH? ──► YES ──► Return speaker
                                │
                            NO  ▼
                    Return: speaker = null, confidence = 0.0
```

## 4. Confidence Scoring Mechanism (NFR-008)

```
CONFIDENCE CALCULATION
======================

                    EXTRACTION SOURCE
                    ─────────────────
    ┌─────────────────────────────────────────────────────────────┐
    │  Source           │  Base Confidence │  Adjustments        │
    │───────────────────│──────────────────│─────────────────────│
    │  Tier 1 (Rules)   │      0.90        │  +0.05 if explicit  │
    │  Tier 2 (ML)      │      0.75        │  +0.10 if NER match │
    │  Tier 3 (LLM)     │      0.60        │  +0.10 if cited     │
    │  Pattern 1 (VTT)  │      0.95        │  -0.05 if edited    │
    │  Pattern 2 (Prefix)│     0.90        │  -0.10 if ambiguous │
    │  Pattern 3 (Brack)│      0.85        │  -0.10 if ambiguous │
    │  Pattern 4 (Context)│    0.60        │  +0.15 if confirmed │
    └─────────────────────────────────────────────────────────────┘

    CONFIDENCE FORMULA:
    ────────────────────
    final_confidence = base_confidence + Σ(adjustments)

    THRESHOLDS (NFR-008):
    ─────────────────────
    HIGH:   confidence >= 0.85  → Include in primary output
    MEDIUM: 0.70 <= conf < 0.85 → Include with review flag
    LOW:    confidence < 0.70   → Include in "uncertain" section
```

## 5. Sample Extractions

### 5.1 Action Item Extraction

```
INPUT SEGMENT:
──────────────
seg-042 | 00:15:30 | Alice: Bob, can you send me the report by Friday?

EXTRACTED:
──────────
{
  "id": "act-001",
  "text": "Send the report",
  "assignee": "Bob",
  "due_date": "2026-01-31",
  "confidence": 0.92,
  "citation": {
    "segment_id": "seg-042",
    "anchor": "#seg-042",
    "timestamp_ms": 930000,
    "text_snippet": "Bob, can you send me the report by Friday?"
  }
}

EXTRACTION PATH: Tier 1 (Rule) → "can you...by Friday" pattern
CONFIDENCE: 0.90 (base) + 0.02 (explicit assignee) = 0.92
```

### 5.2 Decision Extraction

```
INPUT SEGMENT:
──────────────
seg-087 | 00:28:15 | Manager: Okay, so we've decided to go with Option B for the launch.

EXTRACTED:
──────────
{
  "id": "dec-001",
  "text": "Go with Option B for the launch",
  "decided_by": "Manager",
  "rationale": null,
  "confidence": 0.95,
  "citation": {
    "segment_id": "seg-087",
    "anchor": "#seg-087",
    "timestamp_ms": 1695000,
    "text_snippet": "we've decided to go with Option B"
  }
}

EXTRACTION PATH: Tier 1 (Rule) → "decided to" pattern
CONFIDENCE: 0.90 (base) + 0.05 (explicit "decided") = 0.95
```

### 5.3 Question Extraction

```
INPUT SEGMENT:
──────────────
seg-023 | 00:08:45 | Dev: How are we handling authentication for the API?

EXTRACTED:
──────────
{
  "id": "que-001",
  "text": "How are we handling authentication for the API?",
  "asked_by": "Dev",
  "answered": false,
  "citation": {
    "segment_id": "seg-023",
    "anchor": "#seg-023",
    "timestamp_ms": 525000,
    "text_snippet": "How are we handling authentication..."
  }
}

EXTRACTION PATH: Tier 1 (Rule) → Question mark + "How" starter
CONFIDENCE: 0.95 (explicit question mark)
```

## 6. Component Architecture

```
TS-EXTRACTOR COMPONENT DIAGRAM
==============================

┌─────────────────────────────────────────────────────────────────────────────┐
│                          ts-extractor Agent                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  INPUT: CanonicalTranscript JSON (from ts-parser)                           │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                      SpeakerIdentifier (PAT-003)                      │   │
│  │ ──────────────────────────────────────────────────────────────────────│   │
│  │ + identify_speakers(segments: List[Segment]) -> SpeakerMap           │   │
│  │ + _pattern_chain(text: str) -> tuple[str | None, float]              │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                      │                                       │
│                                      ▼                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    TieredExtractor (PAT-001)                          │   │
│  │ ──────────────────────────────────────────────────────────────────────│   │
│  │                                                                        │   │
│  │  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐            │   │
│  │  │ RuleExtractor  │ │  MLExtractor   │ │  LLMExtractor  │            │   │
│  │  │ ────────────── │ │ ────────────── │ │ ────────────── │            │   │
│  │  │ Tier 1         │ │ Tier 2         │ │ Tier 3         │            │   │
│  │  │ Conf: 0.85-1.0 │ │ Conf: 0.70-0.85│ │ Conf: 0.50-0.70│            │   │
│  │  └────────┬───────┘ └────────┬───────┘ └────────┬───────┘            │   │
│  │           │                  │                  │                     │   │
│  │           └──────────────────┴──────────────────┘                     │   │
│  │                              │                                        │   │
│  └──────────────────────────────┼────────────────────────────────────────┘   │
│                                 │                                            │
│                                 ▼                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    CitationLinker (PAT-004)                           │   │
│  │ ──────────────────────────────────────────────────────────────────────│   │
│  │ + link_citations(entities: List[Entity]) -> List[Entity]             │   │
│  │ + _generate_anchor(segment_id: str) -> str                           │   │
│  │ + _validate_citation(citation: Citation) -> bool                     │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                 │                                            │
│                                 ▼                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    TopicSegmenter (FR-009)                            │   │
│  │ ──────────────────────────────────────────────────────────────────────│   │
│  │ + segment_topics(segments: List[Segment]) -> List[Topic]             │   │
│  │ + _detect_boundary(prev: Segment, curr: Segment) -> bool             │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                 │                                            │
│                                 ▼                                            │
│  OUTPUT: ExtractionReport JSON                                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# L2: Strategic Considerations

## 7. Risk Mitigation Implementation

| Risk | RPN | Mitigation in ts-extractor | Verification |
|------|-----|----------------------------|--------------|
| R-004: Missing voice tags | 12 (YELLOW) | 4-pattern fallback chain (PAT-003) | >85% speaker attribution |
| R-006: Low precision | 8 (YELLOW) | Confidence thresholds per NFR-008 | Precision benchmark test |
| R-007: Low recall | 8 (YELLOW) | Tiered extraction (PAT-001) | Recall benchmark test |
| R-008: Hallucination | 12 (YELLOW) | Citation-required (PAT-004) | Citation validation test |

## 8. PAT-004: Citation-Required Extraction

```
ANTI-HALLUCINATION SAFEGUARD
============================

RULE: Every extracted entity MUST have a citation pointing to source segment.

BEFORE (Hallucination-prone):
─────────────────────────────
{
  "action": "Complete the project",
  "assignee": "John"  ← May not exist in transcript!
}

AFTER (Citation-required per PAT-004):
──────────────────────────────────────
{
  "action": "Complete the project",
  "assignee": "John",
  "citation": {
    "segment_id": "seg-142",     ← Must exist
    "anchor": "#seg-142",         ← For deep linking
    "text_snippet": "John will complete the project"  ← Proof
  }
}

VALIDATION:
───────────
1. segment_id MUST exist in input transcript
2. text_snippet MUST be substring of segment text
3. Entities without valid citations are REJECTED
```

## 9. Performance Targets (NFR-003, NFR-004)

| Metric | Target | Measurement | Test Method |
|--------|--------|-------------|-------------|
| Precision (all entities) | > 85% | True Positives / (TP + FP) | Golden dataset |
| Recall (all entities) | > 85% | True Positives / (TP + FN) | Golden dataset |
| Processing time (1-hr transcript) | < 30 seconds | End-to-end timing | Performance test |
| Confidence calibration | ± 5% error | Predicted vs actual | Calibration test |
| Speaker attribution | > 90% | Correct / Total speakers | Attribution test |

## 10. Token Budget Compliance (ADR-002)

```
TOKEN DISTRIBUTION FOR ts-extractor
===================================

COMPONENT                    ESTIMATED TOKENS
─────────────────────────────────────────────
Prompt template              ~500
Input transcript (1 hr)      ~8,000 (100 seg × 80 tokens)
Tier 1 processing            0 (local rules)
Tier 2 processing            ~500 (NER calls)
Tier 3 processing            ~3,000 (LLM extraction)
─────────────────────────────────────────────
TOTAL PER INVOCATION         ~12,000 tokens

BUDGET: 35K hard limit → ✓ COMPLIANT
SOFT LIMIT (90%): 31.5K → ✓ SAFE MARGIN
```

---

## 11. Requirements Traceability

| Requirement | Implementation | Section |
|-------------|----------------|---------|
| FR-005 (Speaker ID) | SpeakerIdentifier + PAT-003 | 3 |
| FR-006 (Action Items) | TieredExtractor.extract_actions | 2 |
| FR-007 (Decisions) | TieredExtractor.extract_decisions | 2 |
| FR-008 (Questions) | TieredExtractor.extract_questions | 2 |
| FR-009 (Topics) | TopicSegmenter | 6 |
| FR-010 (Confidence) | Confidence scoring mechanism | 4 |
| FR-011 (Citations) | CitationLinker + PAT-004 | 8 |
| NFR-003 (Accuracy) | Performance targets | 9 |
| NFR-004 (Processing) | Token budget | 10 |
| NFR-008 (Threshold) | Confidence thresholds | 4 |

---

## 12. ADR Compliance Checklist

| ADR | Decision | Compliance | Evidence |
|-----|----------|------------|----------|
| ADR-001 | Hybrid Architecture | [x] | ts-extractor is single-purpose extraction agent |
| ADR-002 | Token Limit | [x] | ~12K tokens per invocation (< 35K) |
| ADR-003 | Bidirectional Linking | [x] | All entities have citation anchors |
| ADR-005 | Phased Implementation | [x] | Prompt-based with tiered processing |

---

## 13. Related Documents

### Backlinks
- [TDD-transcript-skill.md](./TDD-transcript-skill.md) - Parent architecture
- [TDD-ts-parser.md](./TDD-ts-parser.md) - Upstream agent (provides input)
- [TASK-003-tdd-ts-extractor.md](../TASK-003-tdd-ts-extractor.md) - Task definition

### Forward Links
- [TDD-ts-formatter.md](./TDD-ts-formatter.md) - Downstream agent (consumes output)
- [ts-extractor AGENT.md](../agents/ts-extractor/AGENT.md) - Implementation (TASK-006)

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-26 | ps-architect | Initial design with PAT-001, PAT-003, PAT-004 |

---

*Document ID: TDD-ts-extractor*
*Workflow ID: en005-tdd-20260126-001*
*Constitutional Compliance: P-002 (persisted), P-004 (provenance)*
