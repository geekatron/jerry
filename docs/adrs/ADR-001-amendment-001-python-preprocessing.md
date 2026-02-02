# ADR-001 Amendment 1: Python Preprocessing Layer

> **PS:** FEAT-002/e-adr001-amend
> **Amendment:** 001
> **Created:** 2026-01-29
> **Status:** PROPOSED
> **Agent:** ps-architect
> **Amends:** [ADR-001: Agent Architecture for Transcript Skill](./ADR-001-agent-architecture.md)
> **Discovery Source:** [DISC-009: Agent-Only Architecture Limitation](../../projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-002-implementation/FEAT-002--DISC-009-agent-only-architecture-limitation.md)

---

## Amendment Summary

This amendment adds a **Python Preprocessing Layer** to the hybrid architecture defined in ADR-001. The original decision established custom transcript agents (parser, extractor, formatter) with ps-critic integration but did not specify an executable implementation layer. Live testing revealed that agent definitions are behavioral specifications, not executable code, causing 99.8% data loss on large files.

**Key Change:** Insert deterministic Python parsing before LLM agent processing.

---

## Executive Summary (L0: ELI5)

> **The Problem (Simple Analogy):**
>
> Imagine asking someone to count every word in a very long book by just reading it aloud.
> They'll get tired, skip pages, and make mistakes in the middle. That's what happened
> when we asked our AI to process a 9,220-line meeting transcript - it only gave us
> 5 lines back (like reading 5 pages of a 1,800-page book).
>
> **The Solution:**
>
> Instead, we use a computer program to perfectly count and organize all the words first
> (fast and 100% accurate), then ask the AI to find the interesting stuff (like decisions
> and action items). The computer handles the boring counting; the AI handles the thinking.
>
> **Why This Matters:**
>
> - Computer counting: Free and instant
> - AI counting: Expensive and slow
> - Computer + AI together: Best of both worlds

---

## Context

### What Has Changed Since ADR-001

ADR-001 was accepted on 2026-01-26 based on research and theoretical analysis. On 2026-01-28, during live skill invocation on `meeting-006-all-hands.vtt` (9,220 lines, ~90K tokens, 3,071 segments), a critical gap was discovered:

| Aspect | Expected (ADR-001) | Actual (Live Test) |
|--------|-------------------|-------------------|
| Parser Output | 3,071 segments | 5 segments |
| Data Completeness | 100% | 0.16% |
| Processing Method | Agent-based | Required ad-hoc Python script |

**Root Cause:** Agent definitions (ts-parser.md, ts-extractor.md) are behavioral specifications that describe *how* to process transcripts but lack executable implementation code. The LLM cannot deterministically process 9,220 lines without truncation.

### Evidence from DISC-009

| Finding | Evidence | Impact |
|---------|----------|--------|
| Truncation | 5/3,071 segments (99.8% loss) | CRITICAL |
| Cost Inefficiency | RAG is 1,250x cheaper than pure LLM [1] | HIGH |
| Accuracy Degradation | "Lost in the Middle" - 30%+ drop [2] | HIGH |
| Ad-hoc Workaround | Python script created to complete invocation | Violated "no hacks" principle |

### Research Supporting Amendment

| Source | Finding | Citation |
|--------|---------|----------|
| Stanford NLP | LLMs fail to utilize middle-context information; 30%+ accuracy degradation | [2] |
| Meilisearch | RAG query cost $0.00008 vs LLM $0.10 (1,250x difference) | [1] |
| byteiota | 60% of production LLM applications use RAG/hybrid (400% surge since 2024) | [3] |
| Second Talent | "Hybrid architectures win: retrieval + small models + large models" | [4] |

---

## Amendment Details

### 1. Add Python Preprocessing Layer (NEW)

**Insert before ADR-001 Appendix B Data Flow Diagram:**

The architecture now includes a **Python Preprocessing Layer** that executes before any LLM agent processing. This layer provides:

1. **Deterministic VTT/SRT/TXT Parsing**
   - Library: webvtt-py (v0.5.1, MIT License)
   - Encoding detection: UTF-8, Windows-1252, ISO-8859-1
   - Voice tag extraction
   - Timestamp normalization to milliseconds

2. **Chunking Strategy**
   - Index file with metadata and chunk pointers
   - Chunk files with 500 segments each
   - Enables LLM to request specific segments

**Rationale (L1: Engineer):**

The Python layer addresses three fundamental LLM limitations:

```
Problem 1: Context Window Truncation
├─ LLMs have output limits even with large context windows
├─ Agent produced sample (5 segments) instead of full output (3,071)
└─ Solution: Python parses ALL segments deterministically

Problem 2: Lost-in-the-Middle Phenomenon
├─ Transformer attention favors start/end positions
├─ Middle-context accuracy drops 30%+
└─ Solution: Chunking allows focused processing of relevant sections

Problem 3: Cost Inefficiency
├─ Processing 90K tokens for parsing = $$$
├─ RAG/preprocessing = 1,250x cheaper
└─ Solution: Python parsing is essentially free vs token costs
```

**Technical Specification:**

```python
# Location: skills/transcript/src/parser.py
import webvtt
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Segment:
    id: int
    start_ms: int
    end_ms: int
    speaker: Optional[str]
    text: str

def parse_vtt(file_path: str) -> List[Segment]:
    """Deterministically parse VTT file to canonical segments."""
    segments = []
    for idx, caption in enumerate(webvtt.read(file_path), start=1):
        segments.append(Segment(
            id=idx,
            start_ms=timestamp_to_ms(caption.start),
            end_ms=timestamp_to_ms(caption.end),
            speaker=extract_speaker(caption.text),
            text=clean_text(caption.text)
        ))
    return segments
```

### 2. Add Chunking Layer (NEW)

**Chunking Strategy (Option D from DISC-009):**

```
canonical-output/
├── index.json           # Metadata, segment count, pointers
├── chunks/
│   ├── chunk-001.json   # Segments 1-500
│   ├── chunk-002.json   # Segments 501-1000
│   ├── chunk-003.json   # Segments 1001-1500
│   └── ...
└── extraction/
    └── extraction-report.json
```

**Index File Schema:**

```json
{
  "schema_version": "1.0",
  "source_file": "meeting-006-all-hands.vtt",
  "source_format": "vtt",
  "total_segments": 3071,
  "total_chunks": 7,
  "chunk_size": 500,
  "source_duration_ms": 18231000,
  "chunks": [
    {
      "chunk_id": "chunk-001",
      "segment_range": [1, 500],
      "timestamp_range": ["00:00:00.000", "01:15:23.500"],
      "file": "chunks/chunk-001.json"
    }
  ],
  "speakers": ["Robert Chen", "Diana Martinez", "Jennifer Adams"],
  "speaker_segment_counts": {
    "Robert Chen": 1005,
    "Diana Martinez": 491,
    "Jennifer Adams": 412
  }
}
```

**Chunk Size Rationale (L2: Architect):**

| Factor | Analysis | Decision |
|--------|----------|----------|
| LangChain Recommendation | 1000-2000 tokens with 200 overlap | Baseline guidance |
| Average Segment Size | 15-30 words = 20-40 tokens | Measured from samples |
| 500 Segments | ≈ 10,000-20,000 tokens per chunk | Conservative choice |
| ADR-004 Soft Limit | 31.5K tokens for optional split | Room for overlap |
| Lost-in-Middle Mitigation | Smaller chunks = more start/end positions | Improved accuracy |

**Tradeoff Analysis:**

```
Smaller Chunks (250 segments)
├─ Pro: Better accuracy (more start/end positions)
├─ Pro: Parallel processing potential
├─ Con: More files to manage
└─ Con: More LLM invocations for full coverage

Larger Chunks (1000 segments)
├─ Pro: Fewer files
├─ Pro: More context per invocation
├─ Con: Approaches Lost-in-Middle threshold
└─ Con: Higher per-invocation cost

Selected: 500 segments
├─ Balanced approach
├─ ~10-20K tokens (well under limits)
└─ 7 chunks for 3,071 segments (manageable)
```

### 3. Update Data Flow Diagram (AMENDED)

**Replace ADR-001 Appendix B with:**

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                           TRANSCRIPT SKILL HYBRID ARCHITECTURE                            │
│                          (ADR-001 + Amendment 001)                                        │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                              INPUT: VTT / SRT / TXT FILE                                  │
│                           (e.g., meeting-006-all-hands.vtt)                               │
└───────────────────────────────────────┬──────────────────────────────────────────────────┘
                                        │
                    ╔═══════════════════╧═══════════════════╗
                    ║     LAYER 0: PYTHON PREPROCESSING      ║  ◄── NEW (Amendment 001)
                    ║            (Deterministic)             ║
                    ╠════════════════════════════════════════╣
                    ║  ┌──────────────────────────────────┐  ║
                    ║  │  VTT/SRT/TXT PARSER              │  ║
                    ║  │  ────────────────────────────    │  ║
                    ║  │  • webvtt-py library             │  ║
                    ║  │  • Encoding detection            │  ║
                    ║  │  • Voice tag extraction          │  ║
                    ║  │  • Timestamp normalization       │  ║
                    ║  │                                  │  ║
                    ║  │  Time: < 1 second                │  ║
                    ║  │  Cost: $0 (local execution)      │  ║
                    ║  │  Accuracy: 100% deterministic    │  ║
                    ║  └──────────────────────────────────┘  ║
                    ╚═══════════════════╤════════════════════╝
                                        │
                                        ▼  Canonical Segments
                    ╔═══════════════════╧═══════════════════╗
                    ║       LAYER 1: CHUNKING STRATEGY       ║  ◄── NEW (Amendment 001)
                    ║           (Index + Chunks)             ║
                    ╠════════════════════════════════════════╣
                    ║  ┌──────────────────────────────────┐  ║
                    ║  │  CHUNK GENERATOR                 │  ║
                    ║  │  ────────────────────────────    │  ║
                    ║  │  • index.json (metadata)         │  ║
                    ║  │  • chunks/chunk-NNN.json         │  ║
                    ║  │  • 500 segments per chunk        │  ║
                    ║  │  • Speaker segment counts        │  ║
                    ║  │                                  │  ║
                    ║  │  Output: 7 chunks for 3,071 segs │  ║
                    ║  └──────────────────────────────────┘  ║
                    ╚═══════════════════╤════════════════════╝
                                        │
                                        ▼  index.json + chunks/
                    ┌───────────────────┴───────────────────┐
                    │       LAYER 2: LLM AGENT LAYER        │  ◄── Original ADR-001
                    │           (Semantic Processing)        │
                    └───────────────────┬───────────────────┘
                                        │
        ┌───────────────────────────────┼───────────────────────────────┐
        │                               │                               │
        ▼                               ▼                               ▼
┌───────────────────┐       ┌───────────────────┐       ┌───────────────────┐
│ TS-PARSER AGENT   │       │ TS-EXTRACTOR      │       │ TS-FORMATTER      │
│ (Schema Validate) │       │ (Entity Extract)  │       │ (Output Generate) │
├───────────────────┤       ├───────────────────┤       ├───────────────────┤
│ • Validate schema │       │ • Read index.json │       │ • Markdown gen    │
│ • Enrich metadata │       │ • Request chunks  │       │ • JSON gen        │
│ • Speaker mapping │ ────► │ • Extract:        │ ────► │ • Citations       │
│                   │ Index │   - Actions       │Entity │ • Schema version  │
│ (Now: validation  │ JSON  │   - Decisions     │ List  │                   │
│  not parsing)     │       │   - Questions     │       │                   │
└───────────────────┘       └─────────┬─────────┘       └───────────────────┘
                                      │
                                      │ Quality Check
                                      ▼
                            ┌───────────────────┐
                            │     PS-CRITIC     │
                            │ (@problem-solving)│
                            ├───────────────────┤
                            │ • Template check  │
                            │ • Quality score   │
                            │ • Feedback loop   │
                            └───────────────────┘

═══════════════════════════════════════════════════════════════════════════════
                              PROCESSING COMPARISON
═══════════════════════════════════════════════════════════════════════════════

                    BEFORE (ADR-001)              AFTER (Amendment 001)
                    ────────────────              ─────────────────────
  Parsing:          LLM-based (~90K tokens)       Python (0 tokens)
  Cost:             ~$0.10 per transcript         ~$0.00 for parsing
  Time:             Minutes                       < 1 second
  Accuracy:         Truncation risk (99.8% loss)  100% deterministic
  Extraction:       Full context required         Chunked (focused)
  Lost-in-Middle:   High risk (30%+ degradation)  Mitigated (chunking)

═══════════════════════════════════════════════════════════════════════════════
```

### 4. Update Agent Responsibilities (AMENDED)

**Amend ADR-001 Appendix A - Agent Responsibilities Matrix:**

| Agent | Original Responsibility | Amended Responsibility |
|-------|------------------------|----------------------|
| transcript-parser | Parse VTT/SRT/TXT to canonical model | **Validate** Python-generated canonical JSON; enrich with metadata |
| entity-extractor | Extract speakers, actions, decisions, questions | **Unchanged** - but now processes chunked input via index.json |
| output-formatter | Generate MD/JSON output with citations | **Unchanged** |
| ps-critic | Review extraction quality | **Unchanged** |
| **Python Parser** (NEW) | N/A | **NEW:** Deterministic VTT/SRT/TXT parsing to canonical JSON |
| **Chunker** (NEW) | N/A | **NEW:** Generate index.json + chunk files |

### 5. Update Risk Table (AMENDED)

**Amend ADR-001 Risks section - add row:**

| Risk | Probability | Impact | Mitigation | **Status** |
|------|-------------|--------|------------|-----------|
| ps-critic integration issues | LOW | MEDIUM | Test cross-skill invocation in isolation first | Unchanged |
| Custom agent drift from Jerry patterns | LOW | LOW | Use PS_AGENT_TEMPLATE.md as base | Unchanged |
| Performance regression with ps-critic loop | MEDIUM | LOW | Make critic review optional; threshold-based | Unchanged |
| **Context rot in long transcripts** | **MEDIUM** | **HIGH** | ~~Implement chunking in transcript-parser~~ **RESOLVED: Python preprocessing + chunking (Amendment 001)** | **MITIGATED** |
| **webvtt-py dependency** (NEW) | LOW | MEDIUM | Pin version, comprehensive test coverage | NEW |
| **Two-stack maintenance** (NEW) | LOW | LOW | Clear separation: Python=parsing, LLM=semantic | NEW |

### 6. Add Scalability Section (NEW)

**Insert after ADR-001 Implementation section:**

#### Scalability Design

The hybrid architecture is designed to handle transcripts of any size without truncation:

| Metric | Design Target | Rationale |
|--------|---------------|-----------|
| Segment Count | Unlimited | Python parsing is O(n) linear |
| File Size | No limit | Streaming parser possible |
| Processing Time | < 1s per 10K segments (parsing) | webvtt-py benchmark |
| Memory | < 100MB | Chunked output prevents memory bloat |

**Anti-Hack Guarantee:**

The design explicitly prevents future ad-hoc workarounds by:

1. **Complete Coverage:** Python parser processes 100% of segments (not samples)
2. **Deterministic Output:** No LLM truncation, hallucination, or sampling
3. **Testable:** Unit tests verify complete parsing
4. **Monitored:** Segment count validation in index.json

```
Future-Proofing Matrix:
────────────────────────────────────────────────────────────
Scenario                  │ Without Amendment │ With Amendment
────────────────────────────────────────────────────────────
5-hour meeting (10K segs) │ Truncation risk   │ ✓ Full parsing
All-day event (50K segs)  │ Certain failure   │ ✓ Chunked processing
Conference (100K segs)    │ Ad-hoc scripts    │ ✓ Same architecture
────────────────────────────────────────────────────────────
```

---

## Implementation Impact

### New Components Required

| Component | Type | Location | Owner |
|-----------|------|----------|-------|
| Python VTT Parser | Python module | `skills/transcript/src/parser.py` | EN-020 |
| Chunking Module | Python module | `skills/transcript/src/chunker.py` | EN-021 |
| Index Schema | JSON Schema | `skills/transcript/schemas/index.schema.json` | EN-021 |
| Chunk Schema | JSON Schema | `skills/transcript/schemas/chunk.schema.json` | EN-021 |

### Modified Components

| Component | Change | Rationale |
|-----------|--------|-----------|
| ts-parser agent | Responsibility shift: parsing → validation | Python does parsing |
| ts-extractor agent | Input format change: full transcript → index + chunks | Chunked processing |
| SKILL.md | Orchestration update: add Python preprocessing step | Pipeline ordering |

### Dependency Additions

| Dependency | Version | License | Purpose |
|------------|---------|---------|---------|
| webvtt-py | 0.5.1 | MIT | VTT parsing |
| chardet | 5.x | LGPL-2.1 | Encoding detection |

### Feature Implementation Reference

This amendment is implemented by **FEAT-004: Hybrid Parsing Infrastructure**:

- [EN-020: Python Parser Implementation](../../projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-004-hybrid-infrastructure/EN-020-python-parser/EN-020-python-parser.md)
- [EN-021: Chunking Strategy](../../projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-004-hybrid-infrastructure/EN-021-chunking-strategy/EN-021-chunking-strategy.md)
- [EN-022: Extractor Adaptation](../../projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-004-hybrid-infrastructure/EN-022-extractor-adaptation/EN-022-extractor-adaptation.md)

---

## Validation Criteria

### Amendment Acceptance

| # | Criterion | Verification Method |
|---|-----------|---------------------|
| 1 | Python parser processes meeting-006-all-hands.vtt completely (3,071 segments) | Unit test |
| 2 | No truncation or data loss | Segment count assertion |
| 3 | Chunking produces valid index.json | Schema validation |
| 4 | ts-extractor can process chunked input | Integration test |
| 5 | End-to-end quality score >= 0.90 | ps-critic review |
| 6 | Processing time < 30s for 5-hour transcript | Performance test |

### Regression Tests

| Test | Purpose | Expected |
|------|---------|----------|
| Small file (100 segments) | Baseline functionality | Same output as before |
| Medium file (1000 segments) | Chunking trigger | Multiple chunks created |
| Large file (3071 segments) | Full pipeline | Complete extraction-report.json |
| Unicode content | Encoding handling | Correct character preservation |
| Missing speakers | Robustness | Graceful handling |

---

## References

### Primary Sources

| # | Reference | Type | URL |
|---|-----------|------|-----|
| [1] | "RAG vs Long Context LLMs: Cost Analysis" | Research | [Meilisearch Blog](https://www.meilisearch.com/blog/rag-vs-long-context-llms) |
| [2] | "Lost in the Middle: How Language Models Use Long Contexts" | Academic | [Stanford NLP via SuperAnnotate](https://www.superannotate.com/blog/rag-vs-long-context-llms) |
| [3] | "RAG vs Long Context 2026: The Retrieval Debate" | Industry Analysis | [byteiota](https://byteiota.com/rag-vs-long-context-2026-retrieval-debate/) |
| [4] | "Top LLM Frameworks for Building AI Agents" | Industry | [Second Talent](https://www.secondtalent.com/resources/top-llm-frameworks-for-building-ai-agents/) |
| [5] | "webvtt-py Documentation" | Library | [GitHub webvtt-py](https://github.com/glut23/webvtt-py) |
| [6] | "LangChain Text Splitters" | Library | [LangChain Docs](https://docs.langchain.com/oss/python/integrations/splitters) |

### Jerry Sources

| Document | Relevance |
|----------|-----------|
| [ADR-001: Agent Architecture](./ADR-001-agent-architecture.md) | Document being amended |
| [DISC-009: Agent-Only Architecture Limitation](../../projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-002-implementation/FEAT-002--DISC-009-agent-only-architecture-limitation.md) | Discovery documenting the gap |
| [FEAT-004: Hybrid Infrastructure](../../projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-004-hybrid-infrastructure/FEAT-004-hybrid-infrastructure.md) | Implementation feature |

---

## Decision Record

| Aspect | Detail |
|--------|--------|
| **Decision** | Add Python Preprocessing Layer to ADR-001 hybrid architecture |
| **Status** | PROPOSED |
| **Deciders** | ps-architect, User |
| **Date** | 2026-01-29 |
| **Approval Required** | User confirmation |

### Approval Criteria

- [ ] User reviews and accepts amendment rationale
- [ ] Technical approach validated (Python + webvtt-py)
- [ ] FEAT-004 implementation plan accepted
- [ ] No blocking concerns raised

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-29 | ps-architect | Created amendment based on DISC-009 findings |

---

## Appendix: LLM Cost Comparison

**Per DISC-009 Evidence (Meilisearch Research):**

```
┌────────────────────────────────────────────────────────────────────┐
│                    COST COMPARISON: PARSING                         │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Pure LLM Approach (Before Amendment)                              │
│  ─────────────────────────────────────                             │
│  • Input: 90,000 tokens                                            │
│  • Cost per query: ~$0.10                                          │
│  • Risk: Truncation, Lost-in-Middle                                │
│  • Latency: Minutes                                                │
│                                                                     │
│  Hybrid Approach (After Amendment)                                 │
│  ─────────────────────────────────                                 │
│  • Python parsing: 0 tokens, ~$0.00                                │
│  • Chunked extraction: 10-20K tokens per chunk                     │
│  • Cost per query: ~$0.00008 (for RAG-style)                       │
│  • Latency: Sub-second parsing + focused extraction                │
│                                                                     │
│  SAVINGS: 1,250x cost reduction for parsing                        │
│                                                                     │
│  Source: Meilisearch RAG vs Long Context Analysis [1]              │
└────────────────────────────────────────────────────────────────────┘
```

---

<!--
DESIGN RATIONALE:

This amendment addresses a critical architectural gap discovered during live testing.
The evidence is overwhelming:

1. EMPIRICAL: 99.8% data loss during live invocation (5/3071 segments)
2. ACADEMIC: Stanford "Lost in the Middle" research (30%+ accuracy drop)
3. ECONOMIC: 1,250x cost efficiency of preprocessing (Meilisearch)
4. INDUSTRY: 60% of production LLM apps use hybrid/RAG (byteiota)

The amendment follows the principle of "no hacks" by providing a systematic,
testable, and maintainable solution rather than ad-hoc scripts.

Key architectural principles preserved:
- Hexagonal architecture (Python = infrastructure adapter)
- Single responsibility (Python = parsing, LLM = semantics)
- Testability (Python layer is fully unit-testable)
- Cost efficiency (minimize token usage)

TRACE:
- DISC-009: Root cause analysis and recommendation source
- FEAT-004: Implementation feature (EN-020, EN-021, EN-022)
- ADR-001: Original decision (this amends Appendix A, B, and Risks)

APPROVAL REQUIRED: User must accept this amendment before merging to ACCEPTED.
-->

**Generated by:** ps-architect agent
**Template Version:** Nygard ADR Amendment Format
**Quality Review:** Pending ps-critic review
