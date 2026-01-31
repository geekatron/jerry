# ADR-002 Research: Artifact Structure & Token Management

> **PS ID:** en004-adr-20260126-001
> **Entry ID:** research-002
> **Agent:** ps-researcher
> **Created:** 2026-01-26
> **Status:** COMPLETE

---

## L0: Executive Summary (ELI5)

**The Question:** How should we structure the output files from transcript processing, and how do we make sure they don't get too big for Claude to read?

**Key Finding:** We should use a **packet-based structure** with numbered directories and a master index file. Each individual file should stay under **35K tokens** (~26K words) to fit within Claude's effective context window.

**Why This Matters:**
- If files are too large, Claude's performance degrades ("context rot")
- A well-organized structure helps users navigate transcript analysis results
- Proper chunking ensures reliable re-reading of outputs in future sessions

**Bottom Line:** Create a `{session-id}-transcript-output/` packet with 8 numbered subdirectories, an index file, and automatic file splitting when any artifact exceeds 35K tokens.

---

## L1: Technical Research Findings (Software Engineer)

### 1. Token Limit Constraints

#### 1.1 Source: EN-003 Requirements

| Requirement | Value | Source |
|-------------|-------|--------|
| NFR-001 | Processing < 10 seconds | Performance |
| NFR-002 | Memory < 500 MB | Resource |
| DEC-005 | 35K tokens per artifact | Architecture decision |

**35K Token Rationale:**
- Claude's effective context window shows degradation starting around 60K-120K tokens
- "Lost in the middle" effect reduces accuracy for information in central portions
- 35K provides safety margin while allowing substantial content

#### 1.2 Source: Industry Research

**Chroma Context Rot Research:**
- Performance degrades significantly as context length increases
- Models weigh beginning (first 20%) and end (last 10%) more heavily (primacy/recency bias)
- Critical data should occupy early positions

**Pinecone Chunking Best Practices:**
- Recursive chunking with 400-800 tokens for RAG retrieval
- 20% overlap between chunks for context preservation
- Document-aware chunking preserves structure (tables, code blocks, headers)

**Token Estimation:**
- 1,000 tokens = ~750 English words
- 35K tokens = ~26,250 words
- 1-hour meeting transcript = ~10,000-15,000 words

**Implication:** A 1-hour transcript fits in a single file, but extracted entities and analysis may require splitting.

### 2. Directory Structure Patterns

#### 2.1 Pattern A: Flat Structure

```
transcript-output/
├── summary.md
├── speakers.md
├── topics.md
├── action-items.md
├── questions.md
├── decisions.md
├── timeline.md
└── mindmap.mmd
```

**Pros:**
- Simple navigation
- No nesting complexity
- Easy to implement

**Cons:**
- No logical grouping
- Hard to extend
- No versioning support

#### 2.2 Pattern B: Categorized Flat

```
transcript-output/
├── 00-index.md
├── 01-summary.md
├── 02-speakers.md
├── 03-topics.md
├── 04-action-items.md
├── 05-questions.md
├── 06-decisions.md
├── 07-timeline.md
└── 08-mindmap.mmd
```

**Pros:**
- Numbered ordering for navigation
- Predictable file locations
- Index provides overview

**Cons:**
- Limited grouping
- Renumbering if inserting new files
- All files at same level

#### 2.3 Pattern C: Hierarchical Packet (Recommended)

```
{session-id}-transcript-output/
├── 00-index.md                    # Master manifest with all links
├── 01-summary.md                  # Executive summary (<5K tokens)
├── 02-speakers/
│   └── speakers.md                # Speaker profiles and stats
├── 03-topics/
│   ├── topics.md                  # Topic index
│   └── topics-detail-001.md       # Overflow if >35K tokens
├── 04-entities/
│   ├── questions.md
│   ├── action-items.md
│   ├── ideas.md
│   └── decisions.md
├── 05-timeline/
│   └── timeline.md                # Chronological view
├── 06-analysis/
│   └── sentiment.md               # If applicable
├── 07-mindmap/
│   ├── mindmap.mmd                # Mermaid source
│   └── mindmap.ascii.txt          # ASCII rendering
└── 08-workitems/
    └── suggested-tasks.md         # For worktracker integration
```

**Pros:**
- Logical grouping by category
- Room for overflow files
- Session ID provides uniqueness
- Index enables navigation
- Numbered ordering maintains structure

**Cons:**
- More complex implementation
- Deeper paths
- Directory creation overhead

### 3. Token Budget Allocation

Based on 35K token limit per file:

| Artifact | Budget | Rationale |
|----------|--------|-----------|
| 00-index.md | 2K | Links and metadata only |
| 01-summary.md | 5K | Executive summary |
| 02-speakers.md | 8K | ~20 speakers max with profiles |
| 03-topics.md | 15K | Topic hierarchy and summaries |
| 04-questions.md | 10K | Q&A pairs with context |
| 04-action-items.md | 10K | Tasks with assignees and dates |
| 04-ideas.md | 8K | Ideas and suggestions |
| 04-decisions.md | 10K | Decisions with rationale |
| 05-timeline.md | 15K | Chronological summary |
| 06-sentiment.md | 8K | Sentiment analysis |
| 07-mindmap.mmd | 5K | Mermaid source |
| 08-workitems.md | 8K | Suggested tasks |

**Total Theoretical:** 104K tokens (but distributed across 12+ files)

**Overflow Strategy:**
When any file exceeds 35K tokens, split using `-001`, `-002` suffix:
```
03-topics/
├── topics.md           # Index pointing to splits
├── topics-001.md       # First 35K tokens
└── topics-002.md       # Remainder
```

### 4. Naming Conventions

#### 4.1 Session ID Format

```
{YYYY-MM-DD}-{HH-MM}-{slug}

Examples:
- 2026-01-26-09-30-project-kickoff
- 2026-01-26-14-00-sprint-planning
- 2026-01-26-16-30-1-on-1-alice
```

**Rationale:**
- ISO date prefix enables chronological sorting
- Time component distinguishes same-day meetings
- Human-readable slug provides context

#### 4.2 File Naming Rules

| Rule | Pattern | Example |
|------|---------|---------|
| Index files | `00-index.md` | `00-index.md` |
| Summary | `01-summary.md` | `01-summary.md` |
| Category index | `{NN}-{category}.md` | `03-topics.md` |
| Detail files | `{category}-{NNN}.md` | `topics-001.md` |
| Overflow splits | `{name}-{NNN}.md` | `action-items-002.md` |
| Mermaid source | `*.mmd` | `mindmap.mmd` |
| ASCII art | `*.ascii.txt` | `mindmap.ascii.txt` |

### 5. Index/Manifest Structure

```markdown
# Transcript Analysis: {Meeting Title}

> **Session:** {session-id}
> **Date:** {YYYY-MM-DD}
> **Duration:** {HH:MM}
> **Speakers:** {count}
> **Token Count:** {total} (across {file_count} files)

## Quick Navigation

| Section | File | Tokens | Status |
|---------|------|--------|--------|
| Summary | [01-summary.md](./01-summary.md) | 4,200 | COMPLETE |
| Speakers | [02-speakers/speakers.md](./02-speakers/speakers.md) | 7,800 | COMPLETE |
| Topics | [03-topics/topics.md](./03-topics/topics.md) | 14,200 | COMPLETE |
| Questions | [04-entities/questions.md](./04-entities/questions.md) | 8,100 | COMPLETE |
| Action Items | [04-entities/action-items.md](./04-entities/action-items.md) | 9,500 | COMPLETE |
| Decisions | [04-entities/decisions.md](./04-entities/decisions.md) | 6,200 | COMPLETE |
| Timeline | [05-timeline/timeline.md](./05-timeline/timeline.md) | 12,000 | COMPLETE |
| Mind Map | [07-mindmap/mindmap.mmd](./07-mindmap/mindmap.mmd) | 3,100 | COMPLETE |

## Extraction Statistics

- **Speakers Identified:** 5
- **Topics Detected:** 12
- **Questions Found:** 8 (6 answered, 2 open)
- **Action Items:** 14
- **Decisions Made:** 4

## Processing Metadata

- **Processed At:** {timestamp}
- **Processing Time:** {seconds}s
- **Model:** Claude Sonnet
- **Skill Version:** 1.0.0
```

---

## L2: Architectural Implications (Principal Architect)

### 6. Strategic Considerations

#### 6.1 File System as Memory

**Principle:** The Transcript Skill uses the filesystem as extended memory, surviving context compaction.

**Implications:**
- Every output must persist to disk (P-002)
- Files must be self-contained (can be read in isolation)
- Index files enable navigation without reading all content
- Token counts in index allow Claude to plan reads

#### 6.2 Cross-Session Compatibility

**Requirement:** Output packets must be readable by future Claude sessions without original context.

**Design Decisions:**
- Session ID in folder name for identification
- Metadata in 00-index.md for context
- All links relative (portable)
- No external dependencies in artifacts

#### 6.3 Token-Aware Agent Design

**Integration with ADR-001:**

| Agent | Token Concern |
|-------|---------------|
| transcript-parser | Count tokens in canonical model |
| entity-extractor | Track token counts per entity type |
| output-formatter | Enforce 35K limit, trigger splits |

**Output Formatter Responsibilities:**
1. Calculate token count before writing
2. If > 35K, split into numbered files
3. Update index with actual counts
4. Create index entries for all splits

### 7. Trade-Off Analysis

| Factor | Flat | Categorized | Hierarchical |
|--------|------|-------------|--------------|
| Simplicity | HIGH | MEDIUM | LOW |
| Extensibility | LOW | MEDIUM | HIGH |
| Navigation | MEDIUM | HIGH | HIGH |
| Token Tracking | MEDIUM | MEDIUM | HIGH |
| Split Support | LOW | LOW | HIGH |
| Agent Complexity | LOW | LOW | MEDIUM |

**Recommendation:** Hierarchical Packet (Pattern C)

### 8. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Token count estimation error | MEDIUM | LOW | Add 10% safety margin |
| Deep nesting confusion | LOW | LOW | Max 2 levels deep |
| File split orphans | LOW | MEDIUM | Index always lists all files |
| Session ID collision | LOW | LOW | Include timestamp to second |

---

## 7. Recommendations for ADR-002

### Primary Recommendation: Hierarchical Packet with Token Tracking

**Decision Elements:**
1. **Structure:** 8-directory hierarchical packet with numbered ordering
2. **Token Limit:** 35K per file (strict), 31.5K soft limit (10% margin)
3. **Naming:** ISO date + time + slug session ID
4. **Index:** 00-index.md with token counts and status
5. **Overflow:** `-NNN` suffix for split files

### Alternative Options

1. **Option A: Flat** - All files in single directory (simple but limited)
2. **Option B: Categorized Flat** - Numbered files, no subdirectories
3. **Option C: Hierarchical** (recommended) - Numbered subdirectories with index

---

## 8. References

### 8.1 Primary Sources

| # | Reference | Type | Citation |
|---|-----------|------|----------|
| 1 | EN-003 REQUIREMENTS-SPECIFICATION.md | Project | NFR-001, DEC-005 |
| 2 | Pinecone Chunking Strategies | Industry | https://www.pinecone.io/learn/chunking-strategies/ |
| 3 | Deepchecks Token Limits | Industry | https://www.deepchecks.com/5-approaches-to-solve-llm-token-limits/ |
| 4 | Context Length Guide 2025 | Industry | https://local-ai-zone.github.io/guides/context-length-optimization-ultimate-guide-2025.html |

### 8.2 Secondary Sources

| # | Reference | Type | Citation |
|---|-----------|------|----------|
| 5 | Chroma Context Rot Research | Research | https://research.trychroma.com/context-rot |
| 6 | Weaviate Chunking Strategies | Industry | https://weaviate.io/blog/chunking-strategies-for-rag |
| 7 | Agenta Context Management | Industry | https://agenta.ai/blog/top-6-techniques-to-manage-context-length-in-llms |

---

## Document Metadata

| Field | Value |
|-------|-------|
| Document ID | ADR-002-RESEARCH |
| Created | 2026-01-26 |
| Author | ps-researcher agent |
| Status | COMPLETE |
| Word Count | ~1,800 |
| Next Step | ps-architect drafts ADR-002 |

---

*Generated by ps-researcher agent v2.2.0*
*Constitutional Compliance: P-002 (persisted), P-004 (provenance), P-011 (evidence-based)*
