# ADR-004 Research: File Splitting Strategy

> **PS ID:** en004-adr-20260126-001
> **Entry ID:** research-004
> **Agent:** ps-researcher
> **Created:** 2026-01-26
> **Status:** COMPLETE

---

## L0: Executive Summary (ELI5)

**The Question:** When a transcript artifact gets too big (>35K tokens), how should we split it into smaller files?

**Key Finding:** Use **semantic boundary splitting** with a **soft limit trigger** at 31.5K tokens (10% safety margin). Split files at natural boundaries (topic transitions, speaker changes) and use an **index file pattern** where the original filename becomes a navigation hub.

**Why This Matters:**
- Large files degrade Claude's performance ("lost in the middle" effect)
- Splitting at arbitrary token counts loses context
- Users need predictable navigation between split parts
- Cross-references must remain valid after splitting

**Bottom Line:** Split at 31.5K tokens using semantic boundaries. Original file becomes index. Split files use `-001`, `-002` suffix. Include prev/next navigation in each split.

---

## L1: Technical Research Findings (Software Engineer)

### 1. Industry Chunking Research

#### 1.1 Optimal Chunk Sizes

**Source:** [Pinecone Chunking Strategies](https://www.pinecone.io/learn/chunking-strategies/), [Firecrawl Best Chunking 2025](https://www.firecrawl.dev/blog/best-chunking-strategies-rag-2025)

| Research | Optimal Range | Context |
|----------|---------------|---------|
| Pinecone 2024 | 400-512 tokens | RAG retrieval |
| NVIDIA 2024 | 512-1024 tokens | QA tasks |
| Academic studies | 1024+ tokens | Analytical queries |

**Key Insight:** These sizes are for RAG embedding, not for human-readable artifacts. Our 35K limit is for Claude's effective context window, not embedding chunking.

#### 1.2 Context Rot Research

**Source:** [Deepchecks Token Limits](https://www.deepchecks.com/5-approaches-to-solve-llm-token-limits/)

- LLMs weigh beginning (first 20%) and end (last 10%) more heavily
- Information in the middle of long documents is often "lost"
- Claude Sonnet optimal at 60K-120K tokens but degrades with longer contexts
- Our 35K limit provides safety margin for multi-file sessions

#### 1.3 The Lost-in-the-Middle Problem

**Source:** [Redis LLM Chunking](https://redis.io/blog/llm-chunking/)

- Long context models (100K+) still suffer from reduced accuracy in middle sections
- Smaller, focused documents outperform single large documents
- 35K per file + multi-file approach aligns with best practices

### 2. Splitting Strategy Analysis

#### 2.1 Strategy A: Fixed Token Count

Split at exact token count regardless of content.

```
topics.md (45K tokens)
├── topics-001.md (35K tokens - hard cut)
└── topics-002.md (10K tokens)
```

**Pros:**
- Simple implementation
- Predictable file sizes
- No semantic analysis needed

**Cons:**
- May split mid-sentence
- May split mid-topic
- Loses context at boundaries
- Cross-references may break

#### 2.2 Strategy B: Semantic Boundary (Recommended)

Split at natural boundaries (section headings, topic transitions) below threshold.

```
topics.md (45K tokens, 23 topics)
├── topics-001.md (28K tokens, Topics 1-15)
└── topics-002.md (17K tokens, Topics 16-23)
```

**Pros:**
- Maintains topic integrity
- Natural reading flow
- Cross-references within topic preserved
- Better for human readers

**Cons:**
- Variable file sizes
- Requires boundary detection
- May exceed threshold if topic is huge

#### 2.3 Strategy C: Page/Section Level

Split at document sections regardless of token count.

```
topics.md becomes directory:
topics/
├── index.md
├── topic-001.md (5K tokens)
├── topic-002.md (3K tokens)
...
└── topic-023.md (2K tokens)
```

**Pros:**
- Maximum granularity
- Each section standalone
- Easy cross-referencing

**Cons:**
- Many small files
- Directory overhead
- May exceed reasonable file count

### 3. Split Trigger Analysis

#### 3.1 Hard Limit vs. Soft Limit

| Approach | Trigger Point | Behavior |
|----------|---------------|----------|
| Hard Limit | 35K tokens | Error if exceeded |
| Soft Limit | 31.5K tokens | Split when exceeded, 10% margin |
| Proactive | 28K tokens | Split early, more room |

**Recommendation:** Soft limit at 31.5K (90% of 35K) provides:
- Buffer for metadata/backlinks section
- Room for post-processing additions
- Consistent split behavior

#### 3.2 Token Counting Considerations

**Estimation Methods:**
1. **Character-based:** ~4 chars = 1 token (rough)
2. **Word-based:** ~0.75 words = 1 token (English)
3. **Tokenizer-based:** Use `tiktoken` or Claude's tokenizer (accurate)

**For Transcript Skill:** Use word-based estimation (0.75 words/token) during generation, validate with tokenizer before write.

### 4. Naming Convention Analysis

#### 4.1 Suffix Patterns

| Pattern | Example | Pros | Cons |
|---------|---------|------|------|
| `-NNN` | `topics-001.md` | Sortable, predictable | Requires padding |
| `-part-N` | `topics-part-1.md` | Human readable | Less compact |
| `_N` | `topics_1.md` | Simple | Underscore in markdown |
| `/N.md` | `topics/1.md` | Directory isolation | More nesting |

**Recommendation:** `-NNN` suffix (zero-padded 3 digits) per ADR-002 decision.

#### 4.2 Index File Pattern

When `topics.md` exceeds limit:

```markdown
# Topics Index

This section contains 23 topics extracted from the transcript.
Due to size, content is split across multiple files.

## Navigation

| Part | Topics | Token Count | Link |
|------|--------|-------------|------|
| 1 | Topics 1-15 | 28,000 | [→ Part 1](./topics-001.md) |
| 2 | Topics 16-23 | 17,000 | [→ Part 2](./topics-002.md) |

## Quick Links

- [Topic 001: Project Planning](./topics-001.md#topic-001)
- [Topic 008: Budget Review](./topics-001.md#topic-008)
- [Topic 016: Q&A Session](./topics-002.md#topic-016)
```

### 5. Cross-Reference Handling

#### 5.1 Problem Statement

When a file splits, anchors move to different files. Cross-references must update.

**Before Split:**
```markdown
See [Topic 020](./topics.md#topic-020)
```

**After Split (Topic 020 in Part 2):**
```markdown
See [Topic 020](./topics-002.md#topic-020)
```

#### 5.2 Solutions

| Solution | Approach | Complexity |
|----------|----------|------------|
| Pre-split links | Always use split paths | LOW |
| Index redirection | Link to index, index redirects | MEDIUM |
| Post-split update | Scan/replace after split | HIGH |
| Anchor registry | Track anchor→file mapping | MEDIUM |

**Recommendation:** Anchor registry approach
- Output-formatter maintains anchor→file mapping
- All links generated from registry
- After split, registry updated
- Links always valid

### 6. Navigation Between Splits

#### 6.1 Prev/Next Pattern

Each split file includes navigation header and footer:

```markdown
# Topics (Part 2 of 2)

> **Navigation:** [← Part 1](./topics-001.md) | [Index](./topics.md) | Part 2

---

## Topic 016: Q&A Session
...

---

> **Navigation:** [← Part 1](./topics-001.md) | [Index](./topics.md) | Part 2

*File 2 of 2 • Topics 16-23 • 17,000 tokens*
```

#### 6.2 Breadcrumb Pattern

```markdown
**Location:** [00-index.md](../00-index.md) → [03-topics](./topics.md) → Part 2
```

---

## L2: Architectural Implications (Principal Architect)

### 7. Strategic Considerations

#### 7.1 Splitting Responsibility

**Agent:** `output-formatter`

**Workflow:**
1. Generate full content in memory
2. Calculate token count
3. If > 31.5K, identify split boundaries
4. Generate index file + split files
5. Update anchor registry
6. Write files with navigation

#### 7.2 Integration with ADR-002 and ADR-003

| ADR | Integration Point |
|-----|-------------------|
| ADR-002 | Split files live in same directory as original |
| ADR-003 | Anchors must include file path after split |

#### 7.3 Token Budget Impact

From ADR-002 token budgets:

| Artifact | Budget | Split Likely? |
|----------|--------|---------------|
| 00-index.md | 2K | NO |
| 01-summary.md | 5K | NO |
| 02-speakers.md | 8K | RARE |
| 03-topics.md | 35K | **YES** |
| 04-questions.md | 10K | RARE |
| 04-action-items.md | 10K | RARE |
| 04-decisions.md | 10K | RARE |
| 05-timeline.md | 15K | POSSIBLE |
| 07-mindmap.mmd | 5K | NO |
| 08-workitems.md | 8K | RARE |

**Primary Split Candidates:** Topics (03) and Timeline (05)

### 8. Trade-Off Analysis

| Factor | Fixed Token | Semantic Boundary | Section Level |
|--------|-------------|-------------------|---------------|
| Implementation | SIMPLE | MEDIUM | COMPLEX |
| Context Preservation | LOW | HIGH | HIGHEST |
| File Count | PREDICTABLE | VARIABLE | MANY |
| Navigation | EASY | MODERATE | COMPLEX |
| Cross-References | BROKEN | MAINTAINED | MAINTAINED |

**Recommendation:** Semantic Boundary splitting

### 9. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Topic too large for single file | LOW | HIGH | Further split by sub-topic |
| Split boundary detection fails | MEDIUM | MEDIUM | Fallback to fixed split |
| Index becomes stale | LOW | LOW | Regenerate with content |
| Token count estimation drift | MEDIUM | LOW | Validate before write |
| Deep nesting confusion | LOW | MEDIUM | Max 2 levels (index + parts) |

---

## 7. Recommendations for ADR-004

### Primary Recommendation: Semantic Boundary with Soft Limit

**Decision Elements:**
1. **Trigger:** Soft limit at 31.5K tokens (90% of 35K)
2. **Boundaries:** Split at section headings (## level)
3. **Naming:** `-NNN` suffix (topics-001.md, topics-002.md)
4. **Index:** Original filename becomes navigation hub
5. **Navigation:** Prev/Next links in header/footer
6. **Cross-References:** Anchor registry tracks file locations

### Alternative Options

1. **Option A: Fixed Token Split** - Simple but loses context
2. **Option B: Semantic Boundary Split** (recommended) - Balanced
3. **Option C: Section-Per-File Split** - Maximum granularity but many files

---

## 8. References

### 8.1 Primary Sources

| # | Reference | Type | Citation |
|---|-----------|------|----------|
| 1 | Pinecone Chunking Strategies | Industry | https://www.pinecone.io/learn/chunking-strategies/ |
| 2 | Deepchecks Token Limits | Industry | https://www.deepchecks.com/5-approaches-to-solve-llm-token-limits/ |
| 3 | Firecrawl Best Chunking 2025 | Industry | https://www.firecrawl.dev/blog/best-chunking-strategies-rag-2025 |
| 4 | EN-003 REQUIREMENTS-SPECIFICATION.md | Project | NFR-001, DEC-005 |
| 5 | ADR-002 Artifact Structure | Project | Token budgets, naming conventions |

### 8.2 Secondary Sources

| # | Reference | Type | Citation |
|---|-----------|------|----------|
| 6 | Redis LLM Chunking | Industry | https://redis.io/blog/llm-chunking/ |
| 7 | Azure AI Chunk Documents | Industry | https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents |
| 8 | Eden AI Document Processing | Industry | https://www.edenai.co/post/how-to-process-huge-documents-with-llms |
| 9 | ADR-003 Bidirectional Linking | Project | Anchor handling after split |

---

## Document Metadata

| Field | Value |
|-------|-------|
| Document ID | ADR-004-RESEARCH |
| Created | 2026-01-26 |
| Author | ps-researcher agent |
| Status | COMPLETE |
| Word Count | ~1,900 |
| Next Step | ps-architect drafts ADR-004 |

---

*Generated by ps-researcher agent v2.2.0*
*Constitutional Compliance: P-002 (persisted), P-004 (provenance), P-011 (evidence-based)*
