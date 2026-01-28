# EN-016: ts-formatter Agent Implementation

<!--
CORRECTION NOTICE (2026-01-26):
This enabler was renumbered from EN-009 to EN-016 per BUG-001 resolution.
EN-009 ID was already assigned to Mind Map Generator (TASK-046..049).
See: FEAT-002--BUG-001-en009-id-conflict.md
-->

<!--
TEMPLATE: Enabler
VERSION: 2.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
CREATED: 2026-01-26 per DISC-001 alignment analysis
NOTE: This enabler absorbs EN-010 (Artifact Packaging) per ADR-002
RENUMBERED: EN-009 -> EN-016 per BUG-001 (ID conflict with Mind Map Generator)
-->

> **Type:** enabler
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Created:** 2026-01-26T16:30:00Z
> **Revised:** 2026-01-26T16:30:00Z
> **Due:** TBD
> **Completed:**
> **Parent:** FEAT-002
> **Owner:** Claude
> **Target Sprint:** Sprint 4
> **Effort Points:** 10
> **Gate:** GATE-5 (Core Implementation Review)

---

## Summary

Implement the **ts-formatter agent** that transforms parsed transcripts and extracted entities into a navigable, Claude-friendly packet structure. The agent handles token management, file splitting, bidirectional deep linking, and generates the 8-file packet structure per ADR-002.

**Implements:** [TDD-ts-formatter.md](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-formatter.md)

**Absorbs:** EN-010 (Artifact Packaging & Deep Linking) - ts-formatter handles all artifact packaging responsibilities per ADR-002.

**Technical Justification:**
- ADR-002: 8-file hierarchical packet structure (35K token limit per file)
- ADR-003: Bidirectional deep linking with anchor registry and backlinks
- ADR-004: Semantic boundary file splitting algorithm
- Final output stage of the transcript skill pipeline

---

## Design Reference (L0/L1/L2)

### L0: The Publishing House Analogy

The ts-formatter is like a **Publishing House** transforming manuscripts into organized books:

```
THE PUBLISHING HOUSE (ts-formatter)
===================================

        RAW MANUSCRIPTS                      PUBLISHED COLLECTION
        ───────────────                      ────────────────────

    ┌─────────────────────┐
    │ Parsed Transcript   │
    │ (from ts-parser)    │
    │                     │
    │ + Extracted Data    │         ┌─────────────────────────────┐
    │   (from ts-extractor)│        │   transcript-meeting-001/    │
    │                     │         │   ═══════════════════════    │
    │ - Raw segments      │   ───►  │   00-index.md               │
    │ - Action items      │         │   01-summary.md             │
    │ - Decisions         │         │   02-transcript.md          │
    │ - Questions         │         │   03-speakers.md            │
    │ - Topics            │         │   04-action-items.md        │
    │                     │         │   05-decisions.md           │
    └─────────────────────┘         │   06-questions.md           │
                                    │   07-topics.md              │
                                    └─────────────────────────────┘

    "I transform data into navigable documents."
```

### L1: Component Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ts-formatter Agent                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  INPUT: CanonicalTranscript + ExtractionReport (from ts-parser/ts-extractor)│
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                        PacketGenerator (ADR-002)                      │   │
│  │ + generate_packet(data) -> Packet                                     │   │
│  │ + _create_index() -> str                                              │   │
│  │ + _create_summary() -> str                                            │   │
│  │ + _create_transcript() -> str | List[str]                             │   │
│  │ + _create_entity_file(entities, template) -> str                      │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                      │                                       │
│                                      ▼                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                        TokenCounter (NFR-009)                         │   │
│  │ + count_tokens(content: str) -> int                                   │   │
│  │ + estimate_tokens(word_count: int) -> int                             │   │
│  │ + is_approaching_limit(count: int) -> bool                            │   │
│  │                                                                        │   │
│  │ LIMITS: SOFT_LIMIT=31,500 (90%), HARD_LIMIT=35,000                    │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                      │                                       │
│                                      ▼                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                        FileSplitter (ADR-004)                         │   │
│  │ + should_split(content, token_count) -> bool                          │   │
│  │ + find_split_point(content, soft_limit) -> int                        │   │
│  │ + split_file(content, base_name) -> List[SplitFile]                   │   │
│  │                                                                        │   │
│  │ Algorithm: Split at ## heading BEFORE soft limit                       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                      │                                       │
│                                      ▼                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                     AnchorRegistry (ADR-003)                          │   │
│  │ + register_anchor(id, type, file, line)                               │   │
│  │ + add_backlink(anchor_id, source_file, source_line)                   │   │
│  │ + get_backlinks(anchor_id) -> List[Backlink]                          │   │
│  │ + export_registry() -> dict                                           │   │
│  │                                                                        │   │
│  │ Anchor Format: {type}-{sequence} (seg-001, act-001, dec-001)          │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                      │                                       │
│                                      ▼                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                     BacklinkInjector (IR-004)                         │   │
│  │ + inject_backlinks(files, registry)                                   │   │
│  │ + _format_backlink_section(backlinks) -> str                          │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  OUTPUT: Packet directory with Markdown files + _anchors.json               │
└─────────────────────────────────────────────────────────────────────────────┘
```

### L2: Strategic Considerations

- **ADR-002 8-File Packet:** Standardized structure for Claude-friendly navigation
- **ADR-003 Bidirectional Linking:** Every forward link has corresponding backlink
- **ADR-004 Semantic Splitting:** Split at ## headings, not arbitrary byte boundaries
- **Token Budget:** 35K hard limit, 31.5K soft limit (90%) triggers split evaluation
- **PAT-005 Versioned Schema:** All outputs include version metadata for future compatibility

---

## Benefit Hypothesis

**We believe that** implementing ts-formatter with hierarchical packets and bidirectional linking per TDD-ts-formatter.md

**Will result in** navigable, Claude-friendly transcript artifacts under 35K tokens

**We will know we have succeeded when:**
- All files under 35K tokens (ADR-002 compliance)
- 8-file packet structure generated correctly (FR-013)
- Forward links resolve to valid anchors (ADR-003)
- Backlinks sections populated for all entities (IR-004)
- Index accurately lists all artifacts (FR-015)
- Processing time <5s for 1-hour transcript
- Human approval received at GATE-5

---

## Acceptance Criteria

### Definition of Done

- [ ] ts-formatter agent definition complete (`skills/transcript/agents/ts-formatter.md`)
- [ ] PacketGenerator creates 8-file structure (ADR-002)
- [ ] TokenCounter implements token counting with soft/hard limits
- [ ] FileSplitter implements semantic boundary splitting (ADR-004)
- [ ] AnchorRegistry implements anchor/backlink tracking (ADR-003)
- [ ] BacklinkInjector populates backlinks sections (IR-004)
- [ ] Integration with ts-parser and ts-extractor outputs verified
- [ ] ps-critic review passed
- [ ] Human approval at GATE-5

### Technical Criteria (from TDD-ts-formatter.md)

| # | Criterion | TDD Section | Verified |
|---|-----------|-------------|----------|
| AC-1 | Generates 8-file packet structure | 1 | [ ] |
| AC-2 | No artifact exceeds 35K tokens | 4, 10 | [ ] |
| AC-3 | Split files maintain context with navigation | 3.1 | [ ] |
| AC-4 | All forward links resolve to valid anchors | 2 | [ ] |
| AC-5 | Backlinks sections populated | 5 | [ ] |
| AC-6 | Index lists all artifacts with quick stats | 1.1 | [ ] |
| AC-7 | Anchor IDs follow naming convention | 2 | [ ] |
| AC-8 | Schema version metadata included | 7.1 | [ ] |
| AC-9 | Processing time <5s for 1-hour transcript | 9 | [ ] |

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Owner | Effort | Blocked By |
|----|-------|--------|-------|--------|------------|
| [TASK-113](./TASK-113-formatter-agent-alignment.md) | Verify ts-formatter agent definition alignment | pending | Claude | 2 | - |
| [TASK-114](./TASK-114-packet-generator.md) | Implement/verify PacketGenerator (ADR-002) | pending | Claude | 2 | TASK-113 |
| [TASK-115](./TASK-115-token-counter.md) | Implement/verify TokenCounter (NFR-009) | pending | Claude | 1 | TASK-113 |
| [TASK-116](./TASK-116-file-splitter.md) | Implement/verify FileSplitter (ADR-004) | pending | Claude | 2 | TASK-115 |
| [TASK-117](./TASK-117-anchor-registry.md) | Implement/verify AnchorRegistry (ADR-003) | pending | Claude | 2 | TASK-113 |
| [TASK-118](./TASK-118-backlink-injector.md) | Implement/verify BacklinkInjector (IR-004) | pending | Claude | 1 | TASK-117 |
| [TASK-119](./TASK-119-formatter-validation.md) | Create test cases and validation | pending | Claude | 2 | TASK-114..118 |
| [TASK-119A](./TASK-119A-formatter-contract-tests.md) | Create formatter contract tests (TDD/BDD) | pending | Claude | 1 | TASK-113 |
| [TASK-119B](./TASK-119B-extractor-formatter-integration-tests.md) | Create extractor-formatter integration tests | pending | Claude | 2 | TASK-112A, TASK-119A |
| [TASK-119C](./TASK-119C-e2e-pipeline-tests.md) | Create end-to-end pipeline tests | pending | Claude | 2 | TASK-137, TASK-131A |

**NOTE:** Task IDs start at TASK-113 to avoid conflicts with EN-007 (TASK-101-105) and EN-008 (TASK-106-112).
**TASK-119A/B/C added:** 2026-01-27 per TDD/BDD Testing Strategy for contract, integration, and E2E test coverage.
**Task files created:** 2026-01-26 with detailed acceptance criteria and evidence requirements.

---

## Packet Structure (ADR-002)

```
transcript-{id}/                          TOKEN BUDGET
├── 00-index.md       Navigation hub      ~2,000 tokens
├── 01-summary.md     Executive summary   ~5,000 tokens
├── 02-transcript.md  Full transcript     ~15,000 tokens*
├── 03-speakers.md    Speaker directory   ~3,000 tokens
├── 04-action-items.md Action items       ~4,000 tokens
├── 05-decisions.md   Decisions           ~3,000 tokens
├── 06-questions.md   Open questions      ~2,000 tokens
└── 07-topics.md      Topic segments      ~3,000 tokens
                      ─────────────────   ─────────────
                      Total (single file) ~37,000 tokens

* May be split into 02-transcript-01.md, 02-transcript-02.md, etc.

PACKET ID FORMAT:
─────────────────
transcript-{type}-{date}-{seq}
Example: transcript-meeting-20260126-001
```

---

## Anchor Naming Convention (ADR-003)

```
ANCHOR NAMING SCHEME
====================

FORMAT: {type}-{sequence_number}

TYPE PREFIXES:
──────────────
seg-    → Transcript segments     (seg-001, seg-042)
spk-    → Speakers                (spk-001, spk-alice)
act-    → Action items            (act-001, act-002)
dec-    → Decisions               (dec-001, dec-002)
que-    → Questions               (que-001, que-002)
top-    → Topics                  (top-001, top-002)

EXAMPLES:
─────────
#seg-042     → Link to transcript segment 42
#spk-alice   → Link to speaker "Alice" entry
#act-001     → Link to first action item
#dec-003     → Link to decision 3
```

---

## Token Management

### Soft and Hard Limits

| Limit | Value | Trigger |
|-------|-------|---------|
| SOFT_LIMIT | 31,500 tokens (90%) | Trigger semantic split evaluation |
| HARD_LIMIT | 35,000 tokens | Force split at nearest boundary |
| BUFFER | 3,500 tokens | Safety margin for headers/navigation |

### Splitting Algorithm (ADR-004)

```
tokens < 31,500        → No split needed
31,500 ≤ tokens < 35K  → Split at semantic boundary (##)
tokens ≥ 35,000        → Force split at hard limit
```

---

## Implementation Artifacts

### Existing (from EN-005)

| Artifact | Path | Status |
|----------|------|--------|
| TDD | [TDD-ts-formatter.md](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-formatter.md) | Complete |
| Agent Definition | [skills/transcript/agents/ts-formatter.md](../../../../../skills/transcript/agents/ts-formatter.md) | Complete |

### Absorbed from EN-010

| Artifact | Purpose | Status |
|----------|---------|--------|
| Token Counter | Token counting implementation | Absorbed |
| File Splitter | File splitting strategy | Absorbed |
| Anchor Registry | Deep linking registry | Absorbed |
| Backlinks Generator | Backlinks section generation | Absorbed |

---

## Input/Output Format

### Input (from ts-parser and ts-extractor)

Combined inputs:
1. **CanonicalTranscript** (from ts-parser) - Parsed segments with timestamps
2. **ExtractionReport** (from ts-extractor) - Action items, decisions, questions, topics

### Output

Packet directory structure:
```
transcript-meeting-20260126-001/
├── 00-index.md
├── 01-summary.md
├── 02-transcript.md  (or 02-transcript-01.md, 02-transcript-02.md if split)
├── 03-speakers.md
├── 04-action-items.md
├── 05-decisions.md
├── 06-questions.md
├── 07-topics.md
└── _anchors.json     (anchor registry for tooling)
```

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-002: Implementation](../FEAT-002-implementation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Implements | [TDD-ts-formatter.md](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-formatter.md) | Technical design |
| Depends On | EN-007 | Requires parsed transcript from ts-parser |
| Depends On | EN-008 | Requires extraction report from ts-extractor |
| References | [ADR-002](../../FEAT-001-analysis-design/EN-004-architecture-decisions/docs/adrs/adr-002.md) | 8-file packet structure |
| References | [ADR-003](../../FEAT-001-analysis-design/EN-004-architecture-decisions/docs/adrs/adr-003.md) | Bidirectional deep linking |
| References | [ADR-004](../../FEAT-001-analysis-design/EN-004-architecture-decisions/docs/adrs/adr-004.md) | Semantic boundary splitting |
| References | [ADR-005](../../FEAT-001-analysis-design/EN-004-architecture-decisions/docs/adrs/adr-005.md) | Phased implementation |
| Absorbs | EN-010 | Artifact Packaging & Deep Linking (deprecated) |
| Blocks | EN-011 | Worktracker integration uses formatted packets |

### Discovery Reference

- [DISC-001](../FEAT-002--DISC-001-enabler-alignment-analysis.md) - Alignment analysis (EN-010 absorption)

---

## EN-010 Deprecation Notice

**EN-010 (Artifact Packaging & Deep Linking)** is deprecated and absorbed into EN-016 (ts-formatter) per DISC-001 alignment analysis.

**Rationale:**
- TDD-ts-formatter.md defines ts-formatter as the artifact packaging agent
- ADR-002 assigns 8-file packet structure to ts-formatter
- Separating formatting from packaging creates unnecessary complexity
- Single ts-formatter agent handles: PacketGenerator, TokenCounter, FileSplitter, AnchorRegistry, BacklinkInjector

**Migration:**
- EN-010 tasks (TASK-050-054) are now absorbed into EN-016 tasks (TASK-113-119)
- EN-010 acceptance criteria are covered by EN-016 AC-1 through AC-9

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-26 | Claude | pending | Created per DISC-001: ts-formatter implementation absorbing EN-010 |
| 2026-01-27 | Claude | revised | Added TASK-119A (contract tests), TASK-119B (integration tests), TASK-119C (E2E tests) per TDD/BDD Testing Strategy |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Product Backlog Item (tagged Technical) |
| **SAFe** | Enabler Story |
| **JIRA** | Task |
