# Technical Design Document: ts-formatter Agent

> **Document ID:** TDD-ts-formatter
> **Version:** 1.0
> **Status:** DRAFT
> **Date:** 2026-01-26
> **Author:** ps-architect agent
> **Token Count:** ~5,400 (within 5K target per AC-005)
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

## The Publishing House Analogy

The **ts-formatter agent** is like a **Publishing House** that takes raw manuscripts and produces beautifully organized books:

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
    │ - Raw segments      │   ───►  │   📖 00-index.md            │
    │ - Action items      │         │   📄 01-summary.md          │
    │ - Decisions         │         │   📜 02-transcript.md       │
    │ - Questions         │         │   👥 03-speakers.md         │
    │ - Topics            │         │   ✅ 04-action-items.md     │
    │                     │         │   🎯 05-decisions.md        │
    └─────────────────────┘         │   ❓ 06-questions.md        │
                                    │   📂 07-topics.md           │
                                    └─────────────────────────────┘

    "I transform data into navigable documents."
```

**What I Do:**
1. **Organize** - Structure output into logical sections
2. **Format** - Generate clean, readable Markdown
3. **Link** - Create bidirectional navigation anchors
4. **Split** - Keep files under token limits for Claude
5. **Index** - Generate navigation hub for quick access

**Why This Matters:**
- **Claude-optimized** - All files under 35K tokens
- **Fast navigation** - Jump directly to any action item, speaker, or decision
- **Cross-references** - Click any mention to see full context

---

# L1: Technical Design

## 1. Packet Structure (ADR-002)

```
HIERARCHICAL PACKET STRUCTURE
=============================

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

### 1.1 File Templates

**00-index.md Template:**
```markdown
# {title}

> **Transcript ID:** {packet_id}
> **Date:** {date}
> **Duration:** {duration}
> **Speakers:** {speaker_count}

## Quick Stats

| Metric | Count |
|--------|-------|
| Action Items | {action_count} |
| Decisions | {decision_count} |
| Open Questions | {question_count} |
| Topics | {topic_count} |

## Navigation

- [Summary](./01-summary.md)
- [Full Transcript](./02-transcript.md)
- [Speakers](./03-speakers.md)
- [Action Items](./04-action-items.md)
- [Decisions](./05-decisions.md)
- [Questions](./06-questions.md)
- [Topics](./07-topics.md)

<backlinks>
<!-- Auto-generated backlinks -->
</backlinks>
```

**Entity File Template (04-action-items.md):**
```markdown
# Action Items

> **Extracted from:** [{packet_id}](./00-index.md)
> **Total:** {count}
> **High Confidence (>0.85):** {high_conf_count}

## Action Items

### {#action-001} {action_text}

- **Assignee:** [{assignee}](./03-speakers.md#{speaker_anchor})
- **Due Date:** {due_date}
- **Confidence:** {confidence}
- **Source:** [{source_text}](./02-transcript.md#{segment_anchor})

<backlinks>
- Referenced from: [02-transcript.md#seg-042](./02-transcript.md#seg-042)
</backlinks>

---
```

## 2. Anchor Naming Convention (ADR-003)

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

### 2.1 Anchor Registry Schema

```json
{
  "$id": "transcript-skill/anchor-registry-v1.0",
  "type": "object",
  "required": ["packet_id", "anchors"],
  "properties": {
    "packet_id": { "type": "string" },
    "version": { "const": "1.0" },
    "anchors": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "type", "file", "line"],
        "properties": {
          "id": { "type": "string", "pattern": "^(seg|spk|act|dec|que|top)-[a-z0-9-]+$" },
          "type": { "enum": ["segment", "speaker", "action", "decision", "question", "topic"] },
          "file": { "type": "string" },
          "line": { "type": "integer", "minimum": 1 }
        }
      }
    },
    "backlinks": {
      "type": "object",
      "additionalProperties": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "file": { "type": "string" },
            "line": { "type": "integer" },
            "context": { "type": "string" }
          }
        }
      }
    }
  }
}
```

## 3. File Splitting Algorithm (ADR-004)

```
ADR-004: SEMANTIC BOUNDARY SPLITTING
====================================

                    INPUT: File content + token count
                              │
                              ▼
              ┌───────────────────────────────┐
              │  Token count < 31,500?        │
              │  (SOFT_LIMIT = 90% of 35K)    │
              └───────────────┬───────────────┘
                              │
                 ┌────────────┴────────────┐
                 │                         │
             YES ▼                     NO  ▼
         ┌───────────┐         ┌────────────────────┐
         │ NO SPLIT  │         │ Find nearest ##    │
         │ Output    │         │ heading BEFORE     │
         │ single    │         │ soft limit         │
         │ file      │         └──────────┬─────────┘
         └───────────┘                    │
                              ┌───────────┴───────────┐
                              │                       │
                          FOUND ▼               NOT FOUND ▼
                     ┌────────────────┐     ┌─────────────────┐
                     │ Split at ##    │     │ Force split at  │
                     │ heading        │     │ HARD_LIMIT      │
                     └───────┬────────┘     │ (35K tokens)    │
                             │              └────────┬────────┘
                             │                       │
                             ├───────────────────────┘
                             ▼
              ┌───────────────────────────────┐
              │ Create continuation files:    │
              │ - 02-transcript-01.md         │
              │ - 02-transcript-02.md         │
              │ - etc.                        │
              │                               │
              │ Each file includes:           │
              │ - Navigation header           │
              │ - Previous/Next links         │
              │ - Shared anchor registry ref  │
              └───────────────────────────────┘

SPLIT DECISION TREE:
────────────────────
tokens < 31,500        → No split needed
31,500 ≤ tokens < 35K  → Split at semantic boundary (##)
tokens ≥ 35,000        → Force split at hard limit
```

### 3.1 Split File Template

```markdown
# {title} (Part {n} of {total})

> **Continued from:** [{prev_file}](./{prev_file})
> **Next part:** [{next_file}](./{next_file})
> **Anchor Registry:** [_anchors.json](./_anchors.json)

---

{content}

---

## Navigation

- ← Previous: [{prev_file}](./{prev_file})
- → Next: [{next_file}](./{next_file})
- ↑ Index: [00-index.md](./00-index.md)
```

## 4. Token Counting Implementation

```
TOKEN COUNTING ALGORITHM
========================

METHOD: tiktoken-compatible (cl100k_base encoding)

APPROXIMATION (when tiktoken unavailable):
──────────────────────────────────────────
1. Word count: split on whitespace
2. Multiply by 1.3 (average tokens per word for English)
3. Add 10% buffer for Markdown formatting

FORMULA:
────────
token_estimate = (word_count × 1.3) × 1.1

VALIDATION:
───────────
actual_tokens = tiktoken.encode(content)
if abs(estimate - actual) / actual > 0.15:
    log.warning("Token estimation drift detected")


COUNTING POINTS:
────────────────
┌─────────────────────────────────────────────────────────────┐
│  After each file section is generated:                      │
│    1. Count tokens in section                               │
│    2. Add to running total                                  │
│    3. Check against soft limit                              │
│    4. If approaching limit, trigger split evaluation        │
└─────────────────────────────────────────────────────────────┘
```

## 5. Backlinks Generation

```
BACKLINK GENERATION ALGORITHM
=============================

STEP 1: Build anchor registry during formatting
───────────────────────────────────────────────
for each entity in (actions, decisions, questions, speakers, topics):
    anchor = generate_anchor(entity)
    register_anchor(anchor, file, line)

STEP 2: Scan for references during transcript formatting
─────────────────────────────────────────────────────────
for each segment in transcript:
    for each registered_anchor in anchor_registry:
        if segment.text contains reference_to(anchor):
            add_backlink(anchor, current_file, current_line)

STEP 3: Inject backlinks sections
─────────────────────────────────
for each file with <backlinks> placeholder:
    backlinks = get_backlinks_for_file(file)
    replace_placeholder(file, format_backlinks(backlinks))

BACKLINK FORMAT:
────────────────
<backlinks>
Referenced from:
- [02-transcript.md#seg-042](./02-transcript.md#seg-042) - "Alice mentioned..."
- [05-decisions.md#dec-001](./05-decisions.md#dec-001) - "This action supports..."
</backlinks>
```

## 6. Component Architecture

```
TS-FORMATTER COMPONENT DIAGRAM
==============================

┌─────────────────────────────────────────────────────────────────────────────┐
│                          ts-formatter Agent                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  INPUT: CanonicalTranscript + ExtractionReport (from ts-parser/ts-extractor)│
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                        PacketGenerator (ADR-002)                      │   │
│  │ ──────────────────────────────────────────────────────────────────────│   │
│  │ + generate_packet(data: ProcessedData) -> Packet                     │   │
│  │ + _create_index() -> str                                             │   │
│  │ + _create_summary() -> str                                           │   │
│  │ + _create_transcript() -> str | List[str]                            │   │
│  │ + _create_entity_file(entities, template) -> str                     │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                      │                                       │
│                                      ▼                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                        TokenCounter (NFR-009)                         │   │
│  │ ──────────────────────────────────────────────────────────────────────│   │
│  │ + count_tokens(content: str) -> int                                  │   │
│  │ + estimate_tokens(word_count: int) -> int                            │   │
│  │ + is_approaching_limit(count: int) -> bool                           │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                      │                                       │
│                                      ▼                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                        FileSplitter (ADR-004)                         │   │
│  │ ──────────────────────────────────────────────────────────────────────│   │
│  │ + should_split(content: str, token_count: int) -> bool               │   │
│  │ + find_split_point(content: str, soft_limit: int) -> int             │   │
│  │ + split_file(content: str, base_name: str) -> List[SplitFile]        │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                      │                                       │
│                                      ▼                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                     AnchorRegistry (ADR-003)                          │   │
│  │ ──────────────────────────────────────────────────────────────────────│   │
│  │ + register_anchor(id: str, type: str, file: str, line: int)          │   │
│  │ + add_backlink(anchor_id: str, source_file: str, source_line: int)   │   │
│  │ + get_backlinks(anchor_id: str) -> List[Backlink]                    │   │
│  │ + export_registry() -> dict                                          │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                      │                                       │
│                                      ▼                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                     BacklinkInjector (IR-004)                         │   │
│  │ ──────────────────────────────────────────────────────────────────────│   │
│  │ + inject_backlinks(files: List[File], registry: AnchorRegistry)      │   │
│  │ + _format_backlink_section(backlinks: List[Backlink]) -> str         │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                      │                                       │
│                                      ▼                                       │
│  OUTPUT: Packet directory with Markdown files + _anchors.json               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# L2: Strategic Considerations

## 7. Design Pattern Application

### 7.1 PAT-005: Versioned Schema Evolution

```
VERSIONED OUTPUT SCHEMA
=======================

PRINCIPLE: All output files include version metadata for future compatibility.

VERSION HEADER (in each file):
──────────────────────────────
---
schema_version: "1.0"
generator: "ts-formatter"
generated_at: "2026-01-26T15:30:00Z"
---

EVOLUTION STRATEGY:
───────────────────
v1.0 → v1.1: Additive changes only (new optional fields)
v1.x → v2.0: Breaking changes require migration tool

MIGRATION PATH:
───────────────
1. Read schema_version from existing files
2. Apply transformer chain: v1.0 → v1.1 → ... → current
3. Re-generate affected sections
4. Preserve anchor IDs for link stability
```

### 7.2 PAT-006: Hexagonal Skill Architecture

```
HEXAGONAL BOUNDARIES
====================

PRIMARY PORTS (Inbound):
────────────────────────
┌────────────────────────────────────────────────────────────┐
│ IFormatter                                                  │
│ + format(data: ProcessedData) -> FormattedPacket           │
└────────────────────────────────────────────────────────────┘

SECONDARY PORTS (Outbound):
───────────────────────────
┌────────────────────────────────────────────────────────────┐
│ IFileWriter                                                 │
│ + write_file(path: str, content: str) -> None              │
│ + create_directory(path: str) -> None                      │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│ ITokenizer                                                  │
│ + count_tokens(text: str) -> int                           │
│ + encoding_name: str                                       │
└────────────────────────────────────────────────────────────┘

ADAPTERS:
─────────
- FileSystemWriter: Implements IFileWriter for local filesystem
- TiktokenAdapter: Implements ITokenizer using tiktoken library
- EstimationTokenizer: Implements ITokenizer using word-count estimation
```

## 8. Risk Mitigation Implementation

| Risk | RPN | Mitigation in ts-formatter | Verification |
|------|-----|----------------------------|--------------|
| R-014: Schema breaking | 10 (YELLOW) | Versioned schema (PAT-005) | Version header check |
| R-015: Token overflow | 8 (YELLOW) | Soft/hard limits with split | Token count validation |
| R-016: Broken links | 6 (GREEN) | Anchor registry validation | Link checker test |

## 9. Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Formatting time (1-hr transcript) | < 5 seconds | End-to-end timing |
| Token count accuracy | ± 5% of actual | tiktoken comparison |
| Backlink completeness | 100% | Cross-reference check |
| File size compliance | 100% < 35K tokens | Token counter validation |

## 10. Token Budget Compliance (ADR-002)

```
TOKEN BUDGET ENFORCEMENT
========================

                    DOCUMENT GENERATION FLOW
                    ────────────────────────

    Generate Section           Check Budget              Decision
    ────────────────           ────────────              ────────

    [01-summary.md]  ───►  5,200 tokens  ───►  ✓ Continue
           │
           ▼
    [02-transcript.md]
           │
    ┌──────┴──────┐
    │ Segment 1-50│ ───►  15,000 tokens ───►  ✓ Continue
    │ Segment 51-100│ ──► 29,500 tokens ───►  ⚠ Approaching soft limit
    │ Segment 101+ │ ──►  32,100 tokens ───►  🔀 SPLIT at ## heading
    └─────────────┘
           │
           ▼
    [02-transcript-01.md]  28,500 tokens
    [02-transcript-02.md]  18,600 tokens

LIMITS:
───────
SOFT_LIMIT: 31,500 tokens (90% of 35K) → Trigger semantic split
HARD_LIMIT: 35,000 tokens              → Force split
BUFFER:      3,500 tokens              → Safety margin for headers/navigation
```

---

## 11. Requirements Traceability

| Requirement | Implementation | Section |
|-------------|----------------|---------|
| FR-012 (Markdown Output) | PacketGenerator | 1 |
| FR-013 (Packet Structure) | Hierarchical packet | 1 |
| FR-014 (File Splitting) | FileSplitter + ADR-004 | 3 |
| FR-015 (Index Generation) | PacketGenerator._create_index | 1.1 |
| NFR-009 (Token Budget) | TokenCounter | 4, 10 |
| NFR-010 (Navigation) | AnchorRegistry + BacklinkInjector | 2, 5 |
| IR-004 (Backlink Format) | BacklinkInjector | 5 |
| IR-005 (Anchor Naming) | ADR-003 naming scheme | 2 |

---

## 12. ADR Compliance Checklist

| ADR | Decision | Compliance | Evidence |
|-----|----------|------------|----------|
| ADR-001 | Hybrid Architecture | [x] | ts-formatter is single-purpose formatting agent |
| ADR-002 | Hierarchical Packet | [x] | 8-file packet structure defined |
| ADR-003 | Bidirectional Linking | [x] | Anchor registry + backlinks implementation |
| ADR-004 | Semantic Boundary Split | [x] | Split algorithm with ## heading detection |
| ADR-005 | Phased Implementation | [x] | Prompt-based agent design |

---

## 13. Related Documents

### Backlinks
- [TDD-transcript-skill.md](./TDD-transcript-skill.md) - Parent architecture
- [TDD-ts-parser.md](./TDD-ts-parser.md) - Upstream agent (provides CanonicalTranscript)
- [TDD-ts-extractor.md](./TDD-ts-extractor.md) - Upstream agent (provides ExtractionReport)
- [TASK-004-tdd-ts-formatter.md](../TASK-004-tdd-ts-formatter.md) - Task definition

### Forward Links
- [ts-formatter AGENT.md](../agents/ts-formatter/AGENT.md) - Implementation (TASK-007)
- [SKILL.md](../SKILL.md) - Skill definition (TASK-008)

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-26 | ps-architect | Initial design with ADR-002/003/004 implementation |

---

*Document ID: TDD-ts-formatter*
*Workflow ID: en005-tdd-20260126-001*
*Constitutional Compliance: P-002 (persisted), P-004 (provenance)*
