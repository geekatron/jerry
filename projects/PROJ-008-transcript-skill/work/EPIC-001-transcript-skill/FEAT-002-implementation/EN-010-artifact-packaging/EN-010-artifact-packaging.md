# EN-010: Artifact Packaging & Deep Linking [DEPRECATED]

<!--
TEMPLATE: Enabler
VERSION: 2.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
STATUS: DEPRECATED - Absorbed into EN-016 (ts-formatter) per DISC-001 and BUG-001
-->

> **Type:** enabler
> **Status:** DEPRECATED
> **Priority:** N/A
> **Impact:** N/A
> **Created:** 2026-01-26T00:00:00Z
> **Deprecated:** 2026-01-26T16:30:00Z
> **Due:** N/A
> **Completed:** N/A
> **Parent:** FEAT-002
> **Owner:** Claude
> **Target Sprint:** N/A
> **Effort Points:** 0 (absorbed into EN-009)
> **Gate:** N/A

---

## DEPRECATION NOTICE

**This enabler has been deprecated and absorbed into [EN-016: ts-formatter Agent Implementation](../EN-016-ts-formatter/EN-016-ts-formatter.md).**

> **Note:** EN-016 was originally created as EN-009 but was renumbered per BUG-001 to resolve an ID conflict with EN-009 Mind Map Generator.

### Rationale

Per [DISC-001 Enabler Alignment Analysis](../FEAT-002--DISC-001-enabler-alignment-analysis.md):

1. **TDD-ts-formatter.md** defines ts-formatter as the artifact packaging agent
2. **ADR-002** assigns the 8-file hierarchical packet structure to ts-formatter
3. Separating formatting from packaging creates unnecessary complexity
4. Single ts-formatter agent handles: PacketGenerator, TokenCounter, FileSplitter, AnchorRegistry, BacklinkInjector

### Task Migration

| Original Task | Status | Migrated To |
|---------------|--------|-------------|
| TASK-050 (Token Counter) | Deprecated | TASK-115 |
| TASK-051 (File Splitter) | Deprecated | TASK-116 |
| TASK-052 (Forward Link Generator) | Deprecated | TASK-117 |
| TASK-053 (Backlinks Generator) | Deprecated | TASK-118 |
| TASK-054 (Index/Manifest Generator) | Deprecated | TASK-114 |

### Acceptance Criteria Migration

All EN-010 acceptance criteria are covered by EN-016 (ts-formatter):
- AC-1 (Token limit) → EN-016 AC-2
- AC-2 (Split context) → EN-016 AC-3
- AC-3 (Forward links) → EN-016 AC-4
- AC-4 (Backlinks) → EN-016 AC-5
- AC-5 (Index complete) → EN-016 AC-6
- AC-6 (Anchor unique) → EN-016 AC-7
- AC-7 (Cross-references) → EN-016 AC-4, AC-5
- AC-8 (Numbered prefixes) → EN-016 AC-1

---

## Original Content (Archived)

The following content is preserved for reference only. All work should reference EN-009

---

## Summary

Implement the artifact packager that assembles all extracted entities and generated outputs into a structured transcript packet. Enforces the 35K token limit per artifact, implements bidirectional deep linking with backlinks sections, and generates the packet index/manifest.

**Technical Justification:**
- 35K token limit ensures Claude-friendliness
- Bidirectional linking enables navigation
- Backlinks sections provide reverse navigation
- Index/manifest enables packet discovery

---

## Benefit Hypothesis

**We believe that** packaging artifacts with token management and deep linking

**Will result in** navigable, Claude-friendly transcript packets

**We will know we have succeeded when:**
- All artifacts are under 35K tokens
- Forward links resolve correctly
- Backlinks sections are populated
- Index accurately lists all artifacts
- Human approval received at GATE-6

---

## Acceptance Criteria

### Definition of Done

- [ ] Token counting implemented
- [ ] File splitting strategy implemented
- [ ] Forward link generation working
- [ ] Backlinks section generation working
- [ ] Index/manifest generator implemented
- [ ] Packet structure validated
- [ ] Integration tests passing
- [ ] ps-critic review passed
- [ ] Human approval at GATE-6

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | No artifact exceeds 35K tokens | [ ] |
| AC-2 | Split files maintain context | [ ] |
| AC-3 | All forward links resolve | [ ] |
| AC-4 | All backlinks are accurate | [ ] |
| AC-5 | Index lists all artifacts | [ ] |
| AC-6 | Anchor IDs are unique | [ ] |
| AC-7 | Cross-references validated | [ ] |
| AC-8 | Numbered prefixes correct | [ ] |

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Owner | Effort | Blocked By |
|----|-------|--------|-------|--------|------------|
| TASK-050 | Implement Token Counter | pending | Claude | 1 | EN-008 |
| TASK-051 | Implement File Splitter | pending | Claude | 2 | TASK-050 |
| TASK-052 | Implement Forward Link Generator | pending | Claude | 2 | TASK-050 |
| TASK-053 | Implement Backlinks Generator | pending | Claude | 2 | TASK-052 |
| TASK-054 | Implement Index/Manifest Generator | pending | Claude | 1 | TASK-051..053 |

---

## Packet Structure

```
{session-id}-transcript-output/
├── 00-index.md                    # Manifest with all links
├── 01-summary.md                  # Executive summary (<5K tokens)
│   <!-- BACKLINKS -->
│   - Referenced by: 02-speakers/speakers.md
│   - Referenced by: 03-topics/topics.md
├── 02-speakers/
│   └── speakers.md                # Speaker profiles
│       <!-- BACKLINKS -->
│       - Referenced by: 03-topics/topics.md#topic-001
│       - Referenced by: 04-entities/action-items.md#action-001
├── 03-topics/
│   ├── topics.md                  # Topic index (<35K tokens)
│   │   <!-- BACKLINKS -->
│   │   - Referenced by: 04-entities/questions.md
│   └── topics-detail-001.md       # Split if topics.md > 35K
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

---

## Deep Linking Specification

### Forward Link Format

```markdown
See [Speaker Profile: John Smith](../02-speakers/speakers.md#speaker-001)
Related topic: [Q4 Budget Review](../03-topics/topics.md#topic-001)
Source: [Transcript 00:05:30](../transcript-chunks/chunk-001.md#cue-045)
```

### Anchor ID Generation

```
{entity-type}-{sequential-number}

Examples:
- speaker-001, speaker-002
- topic-001, topic-002
- action-001, action-002
- cue-001, cue-002
```

### Backlinks Section Format

```markdown
---

## Backlinks

<!-- AUTO-GENERATED: Do not edit manually -->

This artifact is referenced by:
- [03-topics/topics.md](../03-topics/topics.md) - Line 45: "Led by [John Smith](#speaker-001)"
- [04-entities/action-items.md](../04-entities/action-items.md) - Line 12: "Assigned to [John Smith](#speaker-001)"

Last updated: 2026-01-26T10:30:00Z
```

---

## Token Management

### Counting Strategy

- Use tiktoken (cl100k_base encoding) for accurate counts
- Include markdown formatting overhead
- Buffer 2K tokens for backlinks section growth

### Splitting Strategy

1. **Natural Split Points**:
   - Topic boundaries
   - Time gaps (>5 minutes)
   - Speaker changes

2. **Split Naming**:
   - `topics.md` → `topics-001.md`, `topics-002.md`
   - Include continuation markers

3. **Context Preservation**:
   - Include header with split context
   - Reference previous/next parts
   - Maintain consistent anchor IDs

### Split Header Template

```markdown
# Topics (Part 2 of 3)

> **Continued from:** [topics-001.md](./topics-001.md)
> **Continues in:** [topics-003.md](./topics-003.md)
> **Time Range:** 00:45:00 - 01:30:00

---
```

---

## Validation Rules

| Rule | Description | Error Level |
|------|-------------|-------------|
| TOKEN_LIMIT | File < 35K tokens | ERROR |
| LINK_RESOLVES | All links point to existing anchors | ERROR |
| ANCHOR_UNIQUE | No duplicate anchor IDs | ERROR |
| BACKLINKS_COMPLETE | All forward links have backlinks | WARNING |
| INDEX_COMPLETE | All files listed in index | ERROR |
| NUMBERED_PREFIX | Files use correct prefix | WARNING |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-002: Implementation](../FEAT-002-implementation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | EN-008 | Requires entities to package |
| Depends On | EN-009 | Includes mind map artifacts |
| Depends On | ADR-002 | Artifact structure decision |
| Depends On | ADR-003 | Deep linking decision |
| Depends On | ADR-004 | File splitting decision |
| Blocks | EN-011 | Worktracker integration uses packaged artifacts |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-26 | Claude | pending | Enabler created |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Product Backlog Item (tagged Technical) |
| **SAFe** | Enabler Story |
| **JIRA** | Task |
