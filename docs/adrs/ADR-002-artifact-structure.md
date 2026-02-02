# ADR-002: Artifact Structure & Token Management

> **PS:** en004-adr-20260126-001
> **Exploration:** draft-002
> **Created:** 2026-01-26
> **Status:** ACCEPTED
> **Agent:** ps-architect
> **Supersedes:** N/A
> **Superseded By:** N/A

---

## Context

The Transcript Skill produces multiple output artifacts (summaries, speaker lists, action items, mindmaps, etc.). These artifacts must:

1. Stay within Claude's effective context window for reliable re-reading
2. Be organized for easy navigation by both humans and future Claude sessions
3. Support splitting when content exceeds token limits
4. Persist as the filesystem-based memory for the Transcript Skill

### Background

Industry research (Chroma, Pinecone, Agenta) shows that LLM performance degrades with large context windows:
- "Lost in the middle" effect reduces accuracy for centrally-placed information
- Models weigh first 20% and last 10% of context more heavily (primacy/recency bias)
- Effective context varies: Claude Sonnet optimal at 60K-120K tokens

A 1-hour meeting transcript contains ~10,000-15,000 words (~13K-20K tokens), but extracted entities and analysis can easily exceed a single file's capacity.

**Research conducted** (see `research/adr-002-research.md`):
- EN-003 requirements (NFR-001, DEC-005: 35K token limit)
- Industry chunking best practices (Pinecone, Weaviate)
- Context rot research (Chroma)

### Constraints

| ID | Constraint | Source |
|----|------------|--------|
| C-001 | Maximum 35K tokens per artifact file | DEC-005, NFR-001 |
| C-002 | All outputs must persist to filesystem | P-002 Constitution |
| C-003 | Files must be self-contained (readable in isolation) | Session independence |
| C-004 | Directory structure must support future extensions | Extensibility |
| C-005 | Navigation must work without reading all content | Efficiency |
| C-006 | Output must be compatible with Jerry worktracker | IR-004, IR-005 |

### Forces

1. **Simplicity vs. Organization:** Flat structures are simpler but harder to navigate. Hierarchical structures organize well but add complexity.

2. **Token Efficiency vs. Context Preservation:** Smaller files fit context better but may lose cross-file context. Larger files preserve context but risk degradation.

3. **Fixed vs. Dynamic Structure:** Static directories are predictable but may have empty folders. Dynamic creation is flexible but unpredictable.

4. **Human vs. Machine Readability:** Deep nesting aids organization but complicates manual navigation. Flat structures are easy to browse but hard to extend.

---

## Options Considered

### Option 1: Flat File Structure

All output files in a single directory with descriptive names.

**Structure:**
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
- Simplest to implement
- Easy to list all files
- No nesting complexity
- Minimal agent logic

**Cons:**
- No logical grouping
- Hard to extend (where do new artifacts go?)
- No support for file splitting
- No versioning or session tracking

**Fit with Constraints:**
- C-001: PARTIAL - No split support for >35K files
- C-002: PASS - Files persist
- C-003: PASS - Files are self-contained
- C-004: FAIL - No extension mechanism
- C-005: PARTIAL - Must read file list to navigate
- C-006: FAIL - No integration structure

### Option 2: Numbered Flat Structure

Files numbered for ordering, with a master index.

**Structure:**
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
- Predictable ordering
- Index provides navigation
- Simple implementation
- Easy file discovery

**Cons:**
- Limited grouping
- Renumbering pain when inserting
- Split files awkward (04-action-items-split-1.md?)
- Single level limits organization

**Fit with Constraints:**
- C-001: PARTIAL - Split naming unclear
- C-002: PASS - Files persist
- C-003: PASS - Files self-contained
- C-004: PARTIAL - Can add numbered files
- C-005: PASS - Index enables navigation
- C-006: PARTIAL - No dedicated integration area

### Option 3: Hierarchical Packet Structure (Recommended)

Session-identified directory with numbered subdirectories and master index.

**Structure:**
```
{session-id}-transcript-output/
├── 00-index.md                    # Master manifest with all links
├── 01-summary.md                  # Executive summary (<5K tokens)
├── 02-speakers/
│   └── speakers.md                # Speaker profiles and stats
├── 03-topics/
│   ├── topics.md                  # Topic index
│   └── topics-001.md              # Overflow if >35K tokens
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
- Clear overflow mechanism (`-001`, `-002` suffixes)
- Session ID provides uniqueness
- Index enables efficient navigation
- Numbered ordering maintains structure
- Dedicated workitems directory for Jerry integration
- Room for future categories

**Cons:**
- More complex implementation
- Deeper paths to navigate
- Directory creation overhead
- Two levels of numbering to track

**Fit with Constraints:**
- C-001: PASS - Clear split pattern with `-NNN` suffix
- C-002: PASS - Persistent file structure
- C-003: PASS - Each file self-contained with context
- C-004: PASS - Categories can be added (09-xxx/)
- C-005: PASS - 00-index.md provides navigation without reading content
- C-006: PASS - 08-workitems/ dedicated for integration

---

## Decision

**We will use Option 3: Hierarchical Packet Structure.**

### Rationale

1. **Token Limit Compliance (C-001):** The `-NNN` suffix pattern provides clear, unambiguous file splitting when content exceeds 35K tokens. The index tracks all splits.

2. **Organized Navigation (C-005):** The 00-index.md file provides a manifest with token counts, allowing Claude to plan which files to read without loading all content.

3. **Jerry Integration (C-006):** The dedicated 08-workitems/ directory provides a clear location for suggested tasks that can be imported into worktracker.

4. **Future Extensibility (C-004):** New categories can be added as 09-xxx/, 10-xxx/ without disrupting existing structure.

5. **Session Independence (C-003):** Session ID in folder name + metadata in index enables re-reading by future Claude sessions without original context.

### Alignment

| Criterion | Score | Notes |
|-----------|-------|-------|
| Constraint Satisfaction | HIGH | All 6 constraints met |
| Risk Level | LOW | Proven patterns from file systems |
| Implementation Effort | MEDIUM | Directory creation + index generation |
| Reversibility | HIGH | Can flatten later if needed |

---

## Consequences

### Positive Consequences

1. **Clear Token Management:** Each file has a 35K token limit with explicit overflow handling.

2. **Self-Documenting Structure:** The numbered directories and index make the output packet understandable without external documentation.

3. **Session Portability:** Complete packet can be moved/copied; all paths are relative.

4. **Integration Ready:** 08-workitems/ provides ready-made location for Jerry worktracker import.

5. **Scalable:** Can handle transcripts of any length through file splitting.

### Negative Consequences

1. **Implementation Complexity:** Output formatter agent must track token counts and manage splits.

2. **Path Depth:** Files are 2-3 levels deep, slightly longer paths.

### Neutral Consequences

1. **Directory Overhead:** Empty subdirectories may exist for short transcripts (e.g., no sentiment analysis run).

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Token count estimation error | MEDIUM | LOW | Use 31.5K soft limit (10% margin) |
| Index out of sync with files | LOW | MEDIUM | Generate index last, after all files |
| Session ID collision | LOW | LOW | Include timestamp to second precision |
| Split file orphans | LOW | LOW | Index always regenerated with all files |

---

## Implementation

### Token Budget Allocation

| Artifact | Token Budget | Soft Limit | Notes |
|----------|--------------|------------|-------|
| 00-index.md | 2,000 | 1,800 | Metadata only |
| 01-summary.md | 5,000 | 4,500 | Executive summary |
| 02-speakers.md | 8,000 | 7,200 | ~20 speakers max |
| 03-topics.md | 35,000 | 31,500 | May split |
| 04-questions.md | 10,000 | 9,000 | Q&A pairs |
| 04-action-items.md | 10,000 | 9,000 | Tasks with assignees |
| 04-decisions.md | 10,000 | 9,000 | Decisions with rationale |
| 05-timeline.md | 15,000 | 13,500 | Chronological summary |
| 07-mindmap.mmd | 5,000 | 4,500 | Mermaid source |
| 08-workitems.md | 8,000 | 7,200 | Suggested tasks |

### Session ID Format

```
{YYYY-MM-DD}-{HH-MM}-{slug}

Examples:
- 2026-01-26-09-30-project-kickoff
- 2026-01-26-14-00-sprint-planning
```

### File Split Naming

When `topics.md` exceeds 35K tokens:
```
03-topics/
├── topics.md           # Becomes index to splits
├── topics-001.md       # First 35K tokens
├── topics-002.md       # Next 35K tokens
└── topics-003.md       # Remainder
```

### Action Items

| # | Action | Owner | Status |
|---|--------|-------|--------|
| 1 | Implement token counting in output-formatter | ps-architect | Pending |
| 2 | Create index template with token counts | ps-architect | Pending |
| 3 | Implement file splitting logic | ps-architect | Pending |
| 4 | Define 08-workitems schema for Jerry | ps-architect | Pending |
| 5 | Create session ID generator | ps-architect | Pending |

### Validation Criteria

1. **Token Limit Test:** No file exceeds 35K tokens
2. **Index Completeness:** All files listed in 00-index.md
3. **Split Correctness:** Split files maintain content continuity
4. **Navigation Test:** Can navigate to any file from index
5. **Isolation Test:** Each file readable without others

---

## Related Decisions

| ADR | Relationship | Notes |
|-----|--------------|-------|
| ADR-001 | DEPENDS_ON | Agents defined in ADR-001 produce these artifacts |
| ADR-003 | RELATED_TO | Bidirectional linking uses this structure |
| ADR-004 | RELATED_TO | File splitting strategy for large transcripts |
| ADR-005 | DEPENDS_ON | Implementation approach affects formatter agent |

---

## References

| # | Reference | Type | Relevance |
|---|-----------|------|-----------|
| 1 | research/adr-002-research.md | Research | Primary research input |
| 2 | EN-003 REQUIREMENTS-SPECIFICATION.md | Requirements | NFR-001, DEC-005 |
| 3 | Pinecone Chunking Strategies | Industry | Token management patterns |
| 4 | Chroma Context Rot Research | Research | Performance degradation evidence |
| 5 | Jerry Constitution P-002 | Governance | File persistence requirement |
| 6 | ADR-001 Agent Architecture | Decision | Agent responsibilities |

---

## Appendix A: Index Template

```markdown
# Transcript Analysis: {Meeting Title}

> **Session:** {session-id}
> **Date:** {YYYY-MM-DD}
> **Duration:** {HH:MM}
> **Speakers:** {count}
> **Total Tokens:** {total} (across {file_count} files)
> **Processed:** {timestamp}

## Quick Navigation

| # | Section | File | Tokens | Status |
|---|---------|------|--------|--------|
| 1 | Summary | [01-summary.md](./01-summary.md) | 4,200 | COMPLETE |
| 2 | Speakers | [speakers.md](./02-speakers/speakers.md) | 7,800 | COMPLETE |
| 3 | Topics | [topics.md](./03-topics/topics.md) | 14,200 | COMPLETE |
| 4 | Questions | [questions.md](./04-entities/questions.md) | 8,100 | COMPLETE |
| 5 | Action Items | [action-items.md](./04-entities/action-items.md) | 9,500 | COMPLETE |
| 6 | Decisions | [decisions.md](./04-entities/decisions.md) | 6,200 | COMPLETE |
| 7 | Timeline | [timeline.md](./05-timeline/timeline.md) | 12,000 | COMPLETE |
| 8 | Mind Map | [mindmap.mmd](./07-mindmap/mindmap.mmd) | 3,100 | COMPLETE |
| 9 | Work Items | [suggested-tasks.md](./08-workitems/suggested-tasks.md) | 2,400 | COMPLETE |

## Extraction Statistics

| Metric | Count |
|--------|-------|
| Speakers Identified | 5 |
| Topics Detected | 12 |
| Questions (Answered/Open) | 8 (6/2) |
| Action Items | 14 |
| Decisions Made | 4 |
| Suggested Work Items | 7 |
```

---

**Generated by:** ps-architect agent
**Template Version:** 1.0 (Nygard ADR Format)
**Quality Review:** PASSED (0.91) - ps-critic review 2026-01-26
