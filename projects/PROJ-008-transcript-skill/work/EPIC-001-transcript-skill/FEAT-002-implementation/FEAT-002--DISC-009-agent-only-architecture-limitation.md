# FEAT-002:DISC-009: Agent-Only Architecture Limitation Discovery

<!--
TEMPLATE: Discovery
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9, worktracker.md (Discovery File)
CREATED: 2026-01-28 (Live Skill Invocation Gap Analysis)
PURPOSE: Document the gap between agent-only design and practical large file processing
-->

> **Type:** discovery
> **Status:** DOCUMENTED
> **Priority:** HIGH
> **Impact:** HIGH
> **Created:** 2026-01-28T21:00:00Z
> **Completed:** 2026-01-28
> **Parent:** FEAT-002
> **Owner:** Claude
> **Source:** Live skill invocation on meeting-006-all-hands.vtt (90K tokens)

---

## Frontmatter

```yaml
# =============================================================================
# DISCOVERY WORK ITEM
# Source: ONTOLOGY-v1.md Section 3.4.9 (Discovery Entity Schema)
# =============================================================================

id: "FEAT-002:DISC-009"
work_type: DISCOVERY
title: "Agent-Only Architecture Limitation Discovery"

classification: TECHNICAL
status: DOCUMENTED
resolution: null
priority: HIGH
impact: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-28T21:00:00Z"
updated_at: "2026-01-28T22:00:00Z"
completed_at: "2026-01-28T22:00:00Z"
parent_id: "FEAT-002"
tags: ["architecture", "large-files", "hybrid-processing", "chunking"]

finding_type: GAP
confidence_level: HIGH
source: "Live skill invocation failure analysis"
research_method: "Multi-framework analysis (5W2H, Ishikawa, FMEA, 8D, NASA SE)"
validated: true
validation_date: "2026-01-28T22:00:00Z"
validated_by: "Claude + User"
```

---

## Summary

**Core Finding:** The transcript skill's agent definitions (ts-parser, ts-extractor, ts-formatter) are behavioral specifications that describe *how* to process transcripts, but they lack executable implementation code. For large files (9,220 lines VTT, 90K+ tokens), purely in-context LLM processing is inefficient, expensive, and unreliable due to the "Lost in the Middle" problem.

**Key Findings:**
1. **Agent definitions are prompt templates, not executable code** - ts-parser.md describes parsing rules but cannot actually parse a 9,220-line VTT file
2. **Large file processing requires deterministic preprocessing** - LLM-based parsing is 1,250x more expensive and suffers 30%+ accuracy degradation in middle sections
3. **Hybrid architecture is industry best practice** - Deterministic Python for parsing, LLM agents for semantic extraction

**Validation:** User-confirmed gap when observing ad-hoc Python script creation during live invocation.

---

## Context

### Background

During the live skill invocation on `meeting-006-all-hands.vtt` (9,220 lines, ~90K tokens), the ts-parser agent was unable to produce a complete canonical JSON representation. The agent generated a truncated 5-segment sample instead of processing all 3,071 segments.

To complete the invocation, an ad-hoc Python script was created to parse the VTT file deterministically. This shortcut violated the project's "no hacks" principle (META TODO #8, #17) and revealed a fundamental gap in the architecture.

### Research Question

**Primary:** Is pure LLM-based (agent-only) processing viable for large transcript files?

**Secondary Questions:**
1. What are industry best practices for LLM + large file processing?
2. When should RAG/chunking be used vs. long context windows?
3. What is the optimal hybrid architecture for transcript processing?

### Investigation Approach

1. **5W2H Analysis** - Who, What, When, Where, Why, How, How Much
2. **Ishikawa (Fishbone) Analysis** - Root cause identification
3. **FMEA** - Failure Mode and Effects Analysis
4. **8D Problem Solving** - Systematic corrective action
5. **NASA SE** - Requirements and verification approach
6. **Industry Research** - Context7, web search, academic sources

---

## Finding

### 5W2H Analysis

| Question | Answer |
|----------|--------|
| **WHO** | ts-parser agent (LLM-as-processor) attempting VTT parsing |
| **WHAT** | Truncated output (5 segments instead of 3,071) |
| **WHEN** | Live skill invocation on meeting-006-all-hands.vtt |
| **WHERE** | Canonical transcript JSON generation (ts-parser → canonical-transcript.json) |
| **WHY** | Agent definitions are behavioral specs, not executable code; LLM context constraints |
| **HOW** | Agent lacks deterministic parsing capability; relies on LLM to "understand" and output |
| **HOW MUCH** | 99.8% data loss (5/3,071 segments), requiring ad-hoc Python workaround |

### Ishikawa (Fishbone) Root Cause Analysis

```
                                    ┌──────────────────────────────┐
                                    │  TRUNCATED PARSER OUTPUT     │
                                    │  (5/3,071 segments)          │
                                    └──────────────────────────────┘
                                                  ▲
        ┌─────────────────┬───────────────────────┴───────────────────────┬─────────────────┐
        │                 │                                               │                 │
   ┌────┴────┐      ┌─────┴─────┐                                   ┌─────┴─────┐     ┌────┴────┐
   │  METHOD │      │  MACHINE  │                                   │ MATERIAL  │     │  MAN    │
   └────┬────┘      └─────┬─────┘                                   └─────┬─────┘     └────┬────┘
        │                 │                                               │                 │
        │                 │                                               │                 │
   No executable     LLM context              Lost-in-Middle         9,220 line         Design
   implementation    limitations             accuracy drop          VTT file           assumption
        │                 │                       │                      │                 │
   Behavioral spec   200K window but         30%+ degradation       90K tokens      "Agent can
   only, no code     output cap exists       in middle sections     input size       handle it"
        │                 │                       │                      │                 │
        └─────────────────┴───────────────────────┴──────────────────────┴─────────────────┘
                                                  │
                              ┌────────────────────┴────────────────────┐
                              │ ROOT CAUSE: Agent-only architecture     │
                              │ lacks deterministic processing layer     │
                              └─────────────────────────────────────────┘
```

**Top 3 Root Causes (5 Whys):**

1. **No Executable Implementation**
   - Why truncated? → Agent produced sample, not full output
   - Why sample? → Agent has no parsing code, only instructions
   - Why no code? → Design treated agents as self-sufficient processors
   - Why self-sufficient? → Assumption that LLM can do everything
   - **Root:** Conflation of behavioral specification with execution capability

2. **Lost-in-the-Middle Problem**
   - Why inaccurate? → LLM fails to utilize middle-context information
   - Why middle fails? → Attention mechanism favors start/end positions
   - Why attention bias? → Fundamental transformer architecture limitation
   - Why not addressed? → No chunking strategy implemented
   - **Root:** Stanford research shows 30%+ accuracy drop for mid-context info

3. **Cost/Latency Inefficiency**
   - Why use Python script? → LLM approach too slow/expensive
   - Why expensive? → Each token costs money, 90K tokens = significant cost
   - Why all tokens? → No preprocessing to reduce context
   - Why no preprocessing? → Agent-only design excluded Python
   - **Root:** RAG is 1,250x cheaper than pure LLM for document queries

### FMEA (Failure Mode and Effects Analysis)

| Failure Mode | Effect | Severity (1-10) | Occurrence (1-10) | Detection (1-10) | RPN | Recommended Action |
|--------------|--------|-----------------|-------------------|------------------|-----|-------------------|
| Truncated output | Data loss, incomplete transcript | 9 | 8 | 3 | 216 | Add Python parser preprocessing |
| Lost-in-middle accuracy | Missed entities mid-transcript | 7 | 7 | 5 | 245 | Implement chunking with overlap |
| Cost overrun | Budget exhaustion | 6 | 9 | 2 | 108 | Preprocess to reduce token count |
| Latency spike | Poor UX, timeouts | 5 | 8 | 4 | 160 | Deterministic parsing (instant) |
| Schema drift | Invalid JSON output | 8 | 4 | 6 | 192 | Python enforces schema |

**RPN > 200 = Critical Action Required**

### 8D Problem Solving

| D | Step | Analysis |
|---|------|----------|
| **D1** | Team | Claude (AI), User (Oversight), ps-architect (Design) |
| **D2** | Problem Description | Agent-only architecture cannot reliably process large transcript files (90K+ tokens) |
| **D3** | Containment | Ad-hoc Python script created to complete invocation (temporary workaround) |
| **D4** | Root Cause | Agent definitions are behavioral specs without execution code; LLM limitations for large deterministic tasks |
| **D5** | Corrective Actions | 1) Create Python parsing layer 2) Implement chunking strategy 3) Reserve LLM for semantic extraction |
| **D6** | Validation | Execute pipeline with new architecture, verify complete output |
| **D7** | Prevention | Document hybrid architecture pattern in ADRs; update skill design guidelines |
| **D8** | Congratulate Team | Pending successful FEAT-004 implementation |

### NASA SE Analysis

**NPR 7123.1D Process Assessment:**

| Process | Gap Identified |
|---------|---------------|
| **4.1 System Design** | Agent architecture lacks execution layer |
| **4.2 Verification** | No unit tests for parsing (requires code) |
| **4.3 Validation** | Live invocation revealed functional gap |
| **6.1 Requirements** | FR-001 (parse VTT) not implementable without code |

**Requirements Traceability:**

| Requirement | Status | Gap |
|-------------|--------|-----|
| FR-001: Parse VTT/SRT/TXT | UNMET | No executable parser |
| NFR-001: Process 5h meetings | UNMET | 90K tokens exceeds practical limit |
| NFR-002: < 30s parse time | UNMET | LLM parsing takes minutes |

---

## Option Analysis

### Option A: Implement Python Code in Repository

**Description:** Add full Python parsing implementation to `skills/transcript/src/`

| Aspect | Assessment |
|--------|------------|
| Pros | Full control, testable, deterministic, fast |
| Cons | Maintenance burden, dependency management |
| Effort | Medium (8-16 hours) |
| Risk | Low - established patterns |

### Option B: Agent-Only with Advanced Chunking

**Description:** Keep agent-only design but implement sophisticated chunking protocol

| Aspect | Assessment |
|--------|------------|
| Pros | Stays within agent paradigm |
| Cons | Still expensive, accuracy issues, complex orchestration |
| Effort | High (20+ hours) |
| Risk | High - fighting fundamental LLM limitations |

**Research Verdict on Option B:**

> "Stanford's 'Lost in the Middle' research revealed that LLMs fail to utilize information in the middle of long contexts. Performance degrades by 30% or more when relevant information shifts from the start or end positions to the middle." - [Elasticsearch Labs](https://www.elastic.co/search-labs/blog/rag-vs-long-context-model-llm)

> "The average cost of a RAG query ($0.00008) was 1,250 times lower than the pure LLM approach ($0.10)." - [Meilisearch](https://www.meilisearch.com/blog/rag-vs-long-context-llms)

**Conclusion:** Option B is not recommended due to fundamental LLM architecture limitations.

### Option C: Hybrid Architecture (RECOMMENDED)

**Description:** Python for deterministic parsing, LLM agents for semantic extraction

| Aspect | Assessment |
|--------|------------|
| Pros | Best of both worlds, cost-effective, accurate, testable |
| Cons | Two tech stacks to maintain |
| Effort | Medium (10-14 hours) |
| Risk | Low - industry best practice |

**Industry Evidence:**

> "Hybrid architectures win: Combining retrieval systems, small fine-tuned models and large general models yields higher performance and lower cost." - [Second Talent](https://www.secondtalent.com/resources/top-llm-frameworks-for-building-ai-agents/)

> "RAG framework usage surged 400% since 2024. Sixty percent of production LLM applications now use retrieval-augmented generation." - [byteiota](https://byteiota.com/rag-vs-long-context-2026-retrieval-debate/)

### Option D: Chunking Strategy Enhancement (Complements Option C)

**Description:** Index file + segment chunk files for LLM-efficient access

**Implementation:**
```
canonical-output/
├── index.json           # Metadata, segment count, pointers
├── chunks/
│   ├── chunk-001.json   # Segments 1-500
│   ├── chunk-002.json   # Segments 501-1000
│   └── ...
└── extraction/
    └── extraction-report.json
```

**Benefits:**
- LLM requests specific chunks as needed
- Reduces context window usage
- Enables parallel processing
- Preserves semantic boundaries

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Research | RAG vs Long Context performance | [Elasticsearch Labs](https://www.elastic.co/search-labs/blog/rag-vs-long-context-model-llm) | 2026-01-28 |
| E-002 | Research | RAG 1,250x cost efficiency | [Meilisearch](https://www.meilisearch.com/blog/rag-vs-long-context-llms) | 2026-01-28 |
| E-003 | Research | Lost-in-Middle accuracy drop | [Stanford NLP](https://www.superannotate.com/blog/rag-vs-long-context-llms) | 2026-01-28 |
| E-004 | Research | Hybrid architecture patterns | [Second Talent](https://www.secondtalent.com/resources/top-llm-frameworks-for-building-ai-agents/) | 2026-01-28 |
| E-005 | Library | webvtt-py VTT parsing | [GitHub webvtt-py](https://github.com/glut23/webvtt-py) | 2026-01-28 |
| E-006 | Research | LangChain chunking patterns | [LangChain Docs](https://docs.langchain.com/oss/python/integrations/splitters) | 2026-01-28 |
| E-007 | Research | RAG 400% adoption surge | [byteiota](https://byteiota.com/rag-vs-long-context-2026-retrieval-debate/) | 2026-01-28 |
| E-008 | Observation | Live invocation failure | LIVE-INVOCATION-RESULTS.md | 2026-01-28 |

### LangChain Chunking Best Practices

From Context7 research:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True
)
all_splits = text_splitter.split_documents(docs)
```

**Key Patterns:**
- **RecursiveCharacterTextSplitter**: Prioritizes semantic boundaries (paragraphs → sentences → words)
- **chunk_overlap**: Preserves context across chunk boundaries (typically 10-20% overlap)
- **add_start_index**: Enables citation back to source

### webvtt-py Library Analysis

**Library:** webvtt-py v0.5.1 (MIT License)
**Source:** [PyPI](https://pypi.org/project/webvtt-py/), [GitHub](https://github.com/glut23/webvtt-py)

**Capabilities:**
- Read, write, convert WebVTT caption files
- Parse SRT format with conversion
- HLS video segmentation support
- Clean Python API

**Usage Pattern:**
```python
import webvtt

# Parse VTT
for caption in webvtt.read('captions.vtt'):
    print(caption.start, caption.end, caption.text)

# Convert from SRT
vtt = webvtt.from_srt('captions.srt')
vtt.save()
```

---

## Implications

### Impact on Project

1. **FEAT-002 Scope Change**: Implementation enablers need Python parsing layer
2. **ADR Update Required**: Document hybrid architecture decision
3. **Test Strategy Change**: Unit tests now possible for parsing layer
4. **Cost Reduction**: Significant reduction in LLM token usage

### Design Decisions Affected

| Decision | Impact | Rationale |
|----------|--------|-----------|
| ADR-001 (Agent Architecture) | Amendment Required | Add Python preprocessing layer |
| ADR-005 (Agent Implementation) | Clarification | Agents for semantic work only |
| TDD-ts-parser | Major Update | Add Python implementation specs |

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Dependency on webvtt-py | Medium | Pin version, test edge cases |
| Two-stack maintenance | Low | Clear separation of concerns |
| Migration complexity | Low | Incremental adoption |

### Opportunities Created

1. **Testable Parsing**: Unit tests with 100% coverage possible
2. **Performance**: Sub-second parsing vs. minutes with LLM
3. **Reliability**: Deterministic output, no hallucination risk
4. **Cost Efficiency**: 1,250x reduction in parsing costs

---

## Relationships

### Creates

- [FEAT-004](./FEAT-004-hybrid-infrastructure/FEAT-004-hybrid-infrastructure.md) - Hybrid Infrastructure Initiative
- [EN-020: Python Parser Implementation](./FEAT-004-hybrid-infrastructure/EN-020-python-parser/EN-020-python-parser.md)
- [EN-021: Chunking Strategy](./FEAT-004-hybrid-infrastructure/EN-021-chunking-strategy/EN-021-chunking-strategy.md)

### Informs

- [ADR-001](../../docs/adrs/adr-001.md) - Agent Architecture (amendment)
- [ADR-005](../../docs/adrs/adr-005.md) - Agent Implementation Approach
- [TDD-ts-parser](../../skills/transcript/docs/TDD-ts-parser.md) - Parser technical design

### Related Discoveries

- [DISC-004: Agent Instruction Compliance Failure](./FEAT-002--DISC-004-agent-instruction-compliance-failure.md)
- [DISC-008: Token Formula Discrepancy](./FEAT-002--DISC-008-token-formula-discrepancy.md)

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-002](./FEAT-002-implementation.md) | Parent feature |
| Evidence | [LIVE-INVOCATION-RESULTS.md](../../skills/transcript/test_data/validation/live-output-meeting-006/LIVE-INVOCATION-RESULTS.md) | Live test results |
| Agent | [ts-parser.md](../../skills/transcript/agents/ts-parser.md) | Parser agent definition |

---

## Recommendations

### Immediate Actions

1. **Create FEAT-004**: Hybrid Infrastructure Initiative with Option C architecture
2. **Create EN-020**: Python Parser Implementation using webvtt-py
3. **Create EN-021**: Chunking Strategy with Option D (index + chunks)
4. **Update ADR-001**: Amendment documenting hybrid architecture decision

### Long-term Considerations

1. **Jerry CLI Integration**: Parser should migrate to Jerry CLI (north star)
2. **Multi-Format Support**: Extend Python parser for SRT, plain text
3. **Parallel Processing**: Leverage chunking for concurrent extraction
4. **Caching Layer**: Cache parsed canonical JSON for repeated processing

---

## Chunking Strategy Design (Option D)

### Index File Structure

```json
{
  "schema_version": "1.0",
  "total_segments": 3071,
  "total_chunks": 7,
  "chunk_size": 500,
  "source_file": "meeting-006-all-hands.vtt",
  "source_format": "vtt",
  "source_duration_ms": 18231000,
  "chunks": [
    {
      "chunk_id": "chunk-001",
      "segment_range": [1, 500],
      "timestamp_range": ["00:00:00.000", "01:15:23.500"],
      "file": "chunks/chunk-001.json"
    },
    {
      "chunk_id": "chunk-002",
      "segment_range": [501, 1000],
      "timestamp_range": ["01:15:23.501", "02:35:04.999"],
      "file": "chunks/chunk-002.json"
    }
  ],
  "speakers": ["Robert Chen", "Diana Martinez", "Jennifer Adams", "..."],
  "speaker_segment_counts": {
    "Robert Chen": 1005,
    "Diana Martinez": 491
  }
}
```

### Chunk File Structure

```json
{
  "chunk_id": "chunk-001",
  "schema_version": "1.0",
  "segment_range": [1, 500],
  "segments": [
    {
      "id": 1,
      "start_ms": 0,
      "end_ms": 5500,
      "speaker": "Robert Chen",
      "text": "Good morning everyone."
    }
  ]
}
```

### LLM Agent Workflow

```
1. ts-extractor reads index.json
2. Identifies relevant chunks based on task (e.g., "find action items")
3. Requests specific chunks: chunk-003.json, chunk-005.json
4. Processes chunks with focused context (500 segments vs 3071)
5. Merges results with citation preservation
```

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28T22:00:00Z | Claude | Created discovery with multi-framework analysis |
| 2026-01-28T21:00:00Z | Claude | Initial gap identification during live invocation |

---

## Metadata

```yaml
id: "FEAT-002:DISC-009"
parent_id: "FEAT-002"
work_type: DISCOVERY
title: "Agent-Only Architecture Limitation Discovery"
status: DOCUMENTED
priority: HIGH
impact: HIGH
created_by: "Claude"
created_at: "2026-01-28T21:00:00Z"
updated_at: "2026-01-28T22:00:00Z"
completed_at: "2026-01-28T22:00:00Z"
tags: ["architecture", "large-files", "hybrid-processing", "chunking", "5W2H", "ishikawa", "fmea", "8d", "nasa-se"]
source: "Live skill invocation failure analysis"
finding_type: GAP
confidence_level: HIGH
validated: true
```

---

<!--
DESIGN RATIONALE:

This discovery documents a fundamental architectural gap revealed during live skill
invocation. The multi-framework analysis (5W2H, Ishikawa, FMEA, 8D, NASA SE) provides
rigorous evidence-based support for the hybrid architecture recommendation.

Key evidence:
- Stanford "Lost in the Middle" research: 30%+ accuracy degradation
- RAG vs LLM cost: 1,250x cheaper ($0.00008 vs $0.10)
- Industry adoption: 60% of production LLM apps use RAG (2024-2026)

The recommended Option C (hybrid architecture) aligns with industry best practices
while maintaining the semantic extraction capabilities of LLM agents.

SOURCES:
- LIVE-INVOCATION-RESULTS.md: Direct observation of failure
- LangChain Documentation: Chunking patterns via Context7
- Elasticsearch Labs, Meilisearch, byteiota: RAG research
- webvtt-py documentation: Python library assessment

TRACE:
- FEAT-002: Parent feature (implementation)
- FEAT-004: Child feature (hybrid infrastructure)
- ADR-001: Affected architecture decision
-->
