# ADR-004: File Splitting Strategy

> **PS:** en004-adr-20260126-001
> **Exploration:** draft-004
> **Created:** 2026-01-26
> **Status:** ACCEPTED
> **Agent:** ps-architect
> **Supersedes:** N/A
> **Superseded By:** N/A

---

## Context

Transcript artifacts may exceed the 35K token limit established in ADR-002. When this occurs, files must be split into smaller parts while:

1. Maintaining content integrity and readability
2. Preserving cross-references and anchors
3. Enabling easy navigation between parts
4. Keeping predictable file naming

### Background

Industry research on document chunking for LLMs shows:

- The "lost in the middle" effect reduces accuracy for information buried in long documents
- Optimal chunk sizes range from 512-1024 tokens for RAG, but human-readable artifacts need larger coherent sections
- Semantic boundary splitting (at headings/sections) outperforms fixed-token splitting for comprehension
- A 10% safety margin prevents edge cases where metadata/backlinks push files over limits

**Research conducted** (see `research/adr-004-research.md`):
- Pinecone, Redis, and Firecrawl chunking strategies
- NVIDIA 2024 study on optimal chunk sizes
- Context rot research from Deepchecks

### Constraints

| ID | Constraint | Source |
|----|------------|--------|
| C-001 | Maximum 35K tokens per artifact file | ADR-002, DEC-005 |
| C-002 | Split files must maintain anchor validity | ADR-003 |
| C-003 | Users must be able to navigate between split parts | Usability |
| C-004 | Naming must be predictable and sortable | ADR-002 (-NNN suffix) |
| C-005 | Cross-references must update when files split | ADR-003 |
| C-006 | Split operation should be transparent to users | UX |

### Forces

1. **Context Preservation vs. File Size:** Larger chunks preserve context but risk exceeding limits. Smaller chunks fit limits but may lose coherence.

2. **Simplicity vs. Precision:** Fixed-token splitting is simple but may cut mid-sentence. Semantic splitting is precise but requires boundary detection.

3. **Granularity vs. File Count:** Fine-grained splitting (one topic per file) maximizes organization but creates many files. Coarse splitting creates fewer files but larger chunks.

---

## Options Considered

### Option 1: Fixed Token Split

Split at exact token count regardless of content boundaries.

**Behavior:**
```
topics.md (45K tokens)
├── topics-001.md (35K tokens - hard cut at 35,000)
└── topics-002.md (10K tokens - remainder)
```

**Pros:**
- Simplest implementation
- Predictable file sizes
- No semantic analysis needed

**Cons:**
- May split mid-sentence or mid-topic
- Loses context at boundaries
- Cross-references may break
- Poor reading experience

**Fit with Constraints:**
- C-001: PASS - Files stay under 35K
- C-002: FAIL - Anchors may split across files unpredictably
- C-003: PARTIAL - Navigation works but context lost
- C-004: PASS - Predictable naming
- C-005: FAIL - Cross-references break
- C-006: FAIL - Users see abrupt content cuts

### Option 2: Semantic Boundary Split (Recommended)

Split at natural content boundaries (section headings) when approaching the token limit.

**Behavior:**
```
topics.md (45K tokens, 23 topics at ## level)
├── topics.md (2K tokens - becomes index)
├── topics-001.md (28K tokens - Topics 1-15)
└── topics-002.md (17K tokens - Topics 16-23)
```

**Algorithm:**
1. Calculate total tokens
2. If total > 31.5K (soft limit), find split points
3. Identify all `##` heading positions
4. Group headings into parts where each part < 31.5K
5. Generate index file with navigation
6. Generate split files with prev/next navigation

**Pros:**
- Maintains topic/section integrity
- Natural reading flow preserved
- Cross-references within topics preserved
- Index provides overview and navigation
- Graceful degradation

**Cons:**
- Variable file sizes (depends on section sizes)
- Requires heading detection
- May need fallback if single section > 31.5K

**Fit with Constraints:**
- C-001: PASS - Soft limit ensures files stay under 35K
- C-002: PASS - Anchors stay with their content
- C-003: PASS - Index + navigation enables easy traversal
- C-004: PASS - `-NNN` suffix convention
- C-005: PASS - Anchor registry tracks file locations
- C-006: PASS - Transparent split with clear navigation

### Option 3: Section-Per-File Split

Create one file per major section regardless of size.

**Behavior:**
```
03-topics/
├── topics.md (index only)
├── topic-001-project-planning.md (5K tokens)
├── topic-002-budget-review.md (3K tokens)
...
└── topic-023-next-steps.md (2K tokens)
```

**Pros:**
- Maximum granularity
- Each section completely standalone
- Simple cross-referencing
- Perfect for large knowledge bases

**Cons:**
- Many small files (23 files for 23 topics)
- Directory navigation overhead
- May exceed reasonable file count
- Inconsistent with ADR-002 flat structure within subdirectory

**Fit with Constraints:**
- C-001: PASS - Small files easily under limit
- C-002: PASS - Each anchor in dedicated file
- C-003: PARTIAL - Many files to navigate
- C-004: PARTIAL - Long filenames with slugs
- C-005: PASS - Stable anchor locations
- C-006: FAIL - Noticeable change in structure

---

## Decision

**We will use Option 2: Semantic Boundary Split.**

### Rationale

1. **Context Preservation (C-002, C-006):** Splitting at section headings keeps topics intact. Readers never encounter a topic split mid-way through.

2. **Navigation (C-003):** The index file pattern provides a navigation hub. Users can see all topics at a glance and jump to specific parts.

3. **Anchor Integrity (C-005):** When a file splits, anchors move predictably with their content. The anchor registry (ADR-003) tracks which file contains each anchor.

4. **Soft Limit Safety (C-001):** Using 31.5K (90% of 35K) provides buffer for:
   - Backlinks section (~500 tokens)
   - Navigation header/footer (~300 tokens)
   - Post-processing additions

5. **Consistency with ADR-002:** Split files use the established `-NNN` suffix convention and remain in the same directory as the original file.

### Alignment

| Criterion | Score | Notes |
|-----------|-------|-------|
| Constraint Satisfaction | HIGH | All 6 constraints met |
| Risk Level | LOW | Fallback to fixed split available |
| Implementation Effort | MEDIUM | Heading detection + anchor tracking |
| Reversibility | HIGH | Can switch to fixed split easily |

---

## Consequences

### Positive Consequences

1. **Readable Split Files:** Each part contains complete topics, maintaining reading flow.

2. **Clear Navigation:** Index file shows document structure; prev/next links enable sequential reading.

3. **Stable Cross-References:** Anchors stay with content; links remain valid through anchor registry.

4. **Graceful Handling:** Large transcripts split transparently without user intervention.

5. **Token Budget Safety:** 10% margin prevents edge case overflows.

### Negative Consequences

1. **Variable File Sizes:** Split files may vary significantly (e.g., 15K vs 28K) depending on section sizes.

2. **Fallback Complexity:** If a single section exceeds 31.5K, secondary split logic needed.

### Neutral Consequences

1. **Two File Types:** Original files may be either content (< 31.5K) or index (> 31.5K with splits).

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Single section > 31.5K | LOW | MEDIUM | Split at sub-headings (###) or fixed fallback |
| Section detection fails | LOW | LOW | Treat as single section, fixed split fallback |
| Token estimation drift | MEDIUM | LOW | Validate with tokenizer before write |
| Index file too large | LOW | LOW | Index contains links only, ~2K tokens max |
| Anchor collision after split | LOW | MEDIUM | Prefix anchors with file part number |

---

## Implementation

### Split Trigger

| Condition | Action |
|-----------|--------|
| Token count <= 31,500 | No split, write single file |
| Token count > 31,500 | Trigger semantic split |

**Soft Limit Calculation:**
```
HARD_LIMIT = 35,000 tokens
SAFETY_MARGIN = 0.10 (10%)
SOFT_LIMIT = HARD_LIMIT * (1 - SAFETY_MARGIN) = 31,500 tokens
```

### Split Boundary Detection

**Primary:** `##` level headings (Markdown H2)
**Secondary:** `###` level headings (if H2 section too large)
**Fallback:** Fixed token split at 31,500

### Naming Convention

| Scenario | Original | Index | Split 1 | Split 2 |
|----------|----------|-------|---------|---------|
| Topics split | topics.md | topics.md | topics-001.md | topics-002.md |
| Timeline split | timeline.md | timeline.md | timeline-001.md | timeline-002.md |

**Pattern:** `{name}-{NNN}.md` where NNN is zero-padded 3 digits.

### Index File Template

```markdown
# Topics

> **Note:** This section is split into 2 parts due to size.

## Overview

This document contains 23 topics extracted from the transcript.
Total content: ~45,000 tokens across 2 files.

## Navigation

| Part | Content | Tokens | Link |
|------|---------|--------|------|
| 1 | Topics 1-15 | ~28,000 | [→ Part 1](./topics-001.md) |
| 2 | Topics 16-23 | ~17,000 | [→ Part 2](./topics-002.md) |

## All Topics

### Part 1
- [Topic 001: Project Planning](./topics-001.md#topic-001)
- [Topic 002: Team Introductions](./topics-001.md#topic-002)
...
- [Topic 015: Timeline Review](./topics-001.md#topic-015)

### Part 2
- [Topic 016: Q&A Session](./topics-002.md#topic-016)
...
- [Topic 023: Next Steps](./topics-002.md#topic-023)

---
*Split by output-formatter agent*
```

### Split File Template

```markdown
# Topics (Part 1 of 2)

> **Navigation:** Index | [Part 2 →](./topics-002.md)

---

<a id="topic-001"></a>
## Topic 001: Project Planning
...

<a id="topic-015"></a>
## Topic 015: Timeline Review
...

---

> **Navigation:** Index | [Part 2 →](./topics-002.md)

*Part 1 of 2 • Topics 1-15 • ~28,000 tokens*

---

## Backlinks

| Source | Context | Link |
|--------|---------|------|
| action-items.md | "Assigned during Project Planning" | [→ Action 001](../04-entities/action-items.md#action-001) |
```

### Action Items

| # | Action | Owner | Status |
|---|--------|-------|--------|
| 1 | Implement token counting in output-formatter | ps-architect | Pending |
| 2 | Add heading detection for split boundaries | ps-architect | Pending |
| 3 | Create index file generator | ps-architect | Pending |
| 4 | Implement navigation header/footer injection | ps-architect | Pending |
| 5 | Update anchor registry for split awareness | ps-architect | Pending |
| 6 | Add fixed-split fallback | ps-architect | Pending |

### Validation Criteria

1. **Split Trigger:** Files > 31.5K tokens trigger split
2. **Boundary Respect:** No topic split across files
3. **Navigation Valid:** All prev/next links work
4. **Anchors Valid:** All cross-references resolve
5. **Index Complete:** All topics listed in index
6. **Total Preserved:** Sum of split tokens ≈ original tokens

---

## Related Decisions

| ADR | Relationship | Notes |
|-----|--------------|-------|
| ADR-001 | RELATED_TO | Output-formatter agent handles splitting |
| ADR-002 | DEPENDS_ON | Token limits, naming conventions |
| ADR-003 | DEPENDS_ON | Anchor handling after split |
| ADR-005 | RELATED_TO | Agent implementation includes split logic |

---

## References

| # | Reference | Type | Relevance |
|---|-----------|------|-----------|
| 1 | research/adr-004-research.md | Research | Primary research input |
| 2 | ADR-002 Artifact Structure | Decision | Token limits, naming |
| 3 | ADR-003 Bidirectional Linking | Decision | Anchor handling |
| 4 | Pinecone Chunking Strategies | Industry | Chunk size guidance |
| 5 | Deepchecks Token Limits | Industry | Context rot evidence |
| 6 | EN-003 REQUIREMENTS-SPECIFICATION.md | Requirements | NFR-001, DEC-005 |

---

## Appendix A: Split Decision Flowchart

```
                    ┌─────────────────────────┐
                    │  Calculate Token Count  │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │   Tokens > 31,500?      │
                    └───────────┬─────────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │ NO              │                 │ YES
              ▼                 │                 ▼
    ┌─────────────────┐         │       ┌─────────────────────┐
    │  Write Single   │         │       │ Find ## Headings    │
    │     File        │         │       └──────────┬──────────┘
    └─────────────────┘         │                  │
                                │       ┌──────────▼──────────┐
                                │       │ Group by Token Limit│
                                │       └──────────┬──────────┘
                                │                  │
                                │       ┌──────────▼──────────┐
                                │       │ Any Section > 31.5K?│
                                │       └──────────┬──────────┘
                                │                  │
                                │    ┌─────────────┼─────────────┐
                                │    │ NO          │             │ YES
                                │    ▼             │             ▼
                                │  ┌───────────────┐   ┌─────────────────┐
                                │  │ Write Index + │   │ Try ### Headings│
                                │  │  Split Files  │   │ or Fixed Split  │
                                │  └───────────────┘   └─────────────────┘
```

---

**Generated by:** ps-architect agent
**Template Version:** 1.0 (Nygard ADR Format)
**Quality Review:** PASSED (0.94) - ps-critic review 2026-01-26
