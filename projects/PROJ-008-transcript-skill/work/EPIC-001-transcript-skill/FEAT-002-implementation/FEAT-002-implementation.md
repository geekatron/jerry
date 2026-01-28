# FEAT-002: Implementation

<!--
TEMPLATE: Feature
VERSION: 2.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
RESTRUCTURED: 2026-01-26 per DISC-001 Alignment Analysis
-->

> **Type:** feature
> **Status:** PLANNING
> **Priority:** high
> **Impact:** high
> **Created:** 2026-01-26T00:00:00Z
> **Due:** TBD
> **Completed:**
> **Parent:** EPIC-001
> **Owner:** Claude
> **Target Sprint:** Sprint 3-4

---

## Summary

Implement the Transcript Skill based on the analysis and design completed in FEAT-001. This feature covers the three-agent architecture (`ts-parser` → `ts-extractor` → `ts-formatter`), context injection mechanism, domain context files, and validation test suite. All agents are YAML/MD prompt-based per ADR-005.

**Restructuring Note (DISC-001):** This feature was restructured on 2026-01-26 to align with FEAT-001 design outputs (TDD documents, ADRs, SPEC-context-injection.md). See [DISC-001](./FEAT-002--DISC-001-enabler-alignment-analysis.md) for full analysis.

**Value Proposition:**
- Three-agent pipeline processing VTT/SRT/plain text transcripts
- Tiered entity extraction with confidence scoring (PAT-001)
- 8-file artifact packet with token management (ADR-002)
- Bidirectional deep linking with inline citations (ADR-003, PAT-004)
- YAML-only context injection per DEC-002
- Comprehensive validation with golden dataset

---

## Benefit Hypothesis

**We believe that** implementing the transcript skill based on thorough analysis and design

**Will result in** a robust, maintainable skill that meets user needs

**We will know we have succeeded when:**
- VTT files can be processed end-to-end
- Entities are extracted accurately
- Mind maps are generated
- All artifacts are properly linked
- Human approval received at each gate

---

## Acceptance Criteria

### Definition of Done

- [ ] `ts-parser` agent implemented per TDD-ts-parser.md
- [ ] `ts-extractor` agent implemented per TDD-ts-extractor.md
- [ ] `ts-formatter` agent implemented per TDD-ts-formatter.md (absorbs EN-010)
- [ ] Context injection mechanism implemented per SPEC-context-injection.md
- [ ] Domain context files created (general.yaml, transcript.yaml, meeting.yaml)
- [ ] Worktracker integration implemented
- [ ] Validation test suite with golden dataset
- ~~[ ] Skill CLI interface created (GATE-7 - Above and Beyond)~~ → Moved to FEAT-003
- [ ] All agents are prompt-based (YAML/MD per ADR-005)
- [ ] End-to-end validation tests passing
- [ ] All human approval gates passed (GATE-5, GATE-6)

### Functional Criteria

| # | Criterion | Source | Verified |
|---|-----------|--------|----------|
| AC-1 | VTT/SRT/plain text files parse correctly | TDD-ts-parser | [ ] |
| AC-2 | Timestamps normalized to ISO 8601 | TDD-ts-parser | [ ] |
| AC-3 | Speakers identified with confidence scores | PAT-003, TDD-ts-extractor | [ ] |
| AC-4 | Action items extracted with assignees | FR-006, TDD-ts-extractor | [ ] |
| AC-5 | Topics extracted with tiered confidence | PAT-001, TDD-ts-extractor | [ ] |
| AC-6 | Questions extracted with context | FR-008, TDD-ts-extractor | [ ] |
| AC-7 | All artifacts under 35K tokens | ADR-002, TDD-ts-formatter | [ ] |
| AC-8 | 8-file packet structure generated | ADR-002, TDD-ts-formatter | [ ] |
| AC-9 | Bidirectional deep links with anchors | ADR-003, PAT-004 | [ ] |
| AC-10 | Work items suggested with traceability | TDD-ts-formatter | [ ] |
| AC-11 | Context injection from domain.yaml | SPEC-context-injection | [ ] |
| AC-12 | All extractions include citations | PAT-004 | [ ] |

### Non-Functional Criteria

| # | Criterion | Source | Verified |
|---|-----------|--------|----------|
| NFC-1 | Parser handles 60-min transcripts | REQ-CI-P-001 | [ ] |
| NFC-2 | Graceful error handling with fallbacks | TDD documents | [ ] |
| NFC-3 | Validation precision >= 90% | EN-015 golden dataset | [ ] |
| NFC-4 | Validation recall >= 85% | EN-015 golden dataset | [ ] |

---

## Human Approval Gates

| Gate | After Enablers | Approval Required For |
|------|----------------|----------------------|
| GATE-5 | EN-007, EN-008, EN-009, EN-013, EN-016 | Core agent implementation & context injection |
| GATE-6 | EN-011, EN-014, EN-015 | Integration, domain contexts & validation |

**Note:**
- Gate assignments restructured per DISC-001. EN-010 deprecated (absorbed into EN-016).
- **GATE-7 and EN-012 moved to FEAT-003** per DISC-002 (Above and Beyond scope).

---

## Children (Enablers/Stories)

### Enabler/Story Inventory

> **Restructured per DISC-001 (2026-01-26):** Enablers aligned with TDD documents from FEAT-001.
> **Task ID Scheme:** FEAT-002 uses TASK-101+ to avoid conflicts with FEAT-001 (TASK-001-042).

| ID | Type | Title | Status | Priority | Tasks | Gate | Notes |
|----|------|-------|--------|----------|-------|------|-------|
| [EN-007](./EN-007-vtt-parser/EN-007-vtt-parser.md) | Enabler | ts-parser Agent Implementation | pending | high | 101-105 | 5 | Per TDD-ts-parser.md |
| [EN-008](./EN-008-entity-extraction/EN-008-entity-extraction.md) | Enabler | ts-extractor Agent Implementation | pending | high | 106-112 | 5 | Per TDD-ts-extractor.md (MAJOR rewrite) |
| [EN-009](./EN-009-mindmap-generator/EN-009-mindmap-generator.md) | Enabler | Mind Map Generator (Mermaid + ASCII) | pending | high | 001-004* | 5 | **RESTORED** - Mermaid + ASCII (*enabler-scoped per DEC-003) |
| ~~EN-010~~ | ~~Enabler~~ | ~~Artifact Packaging & Deep Linking~~ | **DEPRECATED** | - | - | - | Absorbed into EN-016 per ADR-002 |
| [EN-011](./EN-011-worktracker-integration/EN-011-worktracker-integration.md) | Enabler | Worktracker Integration | pending | medium | 055-058 | 6 | Depends on EN-016 |
| ~~EN-012~~ | ~~Enabler~~ | ~~Skill CLI Interface~~ | **MOVED** | - | - | - | → **[FEAT-003](../FEAT-003-future-enhancements/EN-012-skill-interface/EN-012-skill-interface.md)** per DISC-002 |
| [EN-013](./EN-013-context-injection/EN-013-context-injection.md) | Enabler | Context Injection Implementation | pending | medium | 120-125 | 5 | YAML-only per DEC-002 |
| [EN-014](./EN-014-domain-context-files/EN-014-domain-context-files.md) | Enabler | Domain Context Files | pending | medium | 126-130 | 6 | general, transcript, meeting |
| [EN-015](./EN-015-transcript-validation/EN-015-transcript-validation.md) | Enabler | Validation & Test Cases | pending | high | 131-137 | 6 | Golden dataset, edge cases |
| [EN-016](./EN-016-ts-formatter/EN-016-ts-formatter.md) | Enabler | ts-formatter Agent Implementation | pending | high | 113-119 | 5 | **RENUMBERED** from EN-009 per BUG-001, absorbs EN-010 |

### Task Allocation Summary

| Enabler | Task Range | Total Tasks | Notes |
|---------|------------|-------------|-------|
| EN-007 | TASK-101..105 | 5 | ts-parser |
| EN-008 | TASK-106..112 | 7 | ts-extractor |
| EN-009 | TASK-001..004* | 4 | Mind Map Generator (*enabler-scoped per DEC-003) |
| EN-011 | TASK-055..058 | 4 | Worktracker Integration |
| ~~EN-012~~ | ~~TASK-059..062~~ | ~~4~~ | ~~Skill CLI Interface~~ → FEAT-003 |
| EN-013 | TASK-120..125 | 6 | Context Injection |
| EN-014 | TASK-126..130 | 5 | Domain Context Files |
| EN-015 | TASK-131..137 | 7 | Validation & Test Cases |
| EN-016 | TASK-113..119 | 7 | ts-formatter (renumbered from EN-009) |
| **Total** | | **45** | Excludes EN-012 (moved to FEAT-003) |

### Work Item Links

**Active Enablers:**
- [EN-007: ts-parser Agent Implementation](./EN-007-vtt-parser/EN-007-vtt-parser.md)
- [EN-008: ts-extractor Agent Implementation](./EN-008-entity-extraction/EN-008-entity-extraction.md)
- [EN-009: Mind Map Generator (Mermaid + ASCII)](./EN-009-mindmap-generator/EN-009-mindmap-generator.md)
- [EN-011: Worktracker Integration](./EN-011-worktracker-integration/EN-011-worktracker-integration.md)
- [EN-013: Context Injection Implementation](./EN-013-context-injection/EN-013-context-injection.md)
- [EN-014: Domain Context Files](./EN-014-domain-context-files/EN-014-domain-context-files.md)
- [EN-015: Validation & Test Cases](./EN-015-transcript-validation/EN-015-transcript-validation.md)
- [EN-016: ts-formatter Agent Implementation](./EN-016-ts-formatter/EN-016-ts-formatter.md)

**Deprecated/Moved Enablers:**
- ~~EN-010: Artifact Packaging & Deep Linking~~ → Absorbed into EN-016
- ~~EN-012: Skill CLI Interface~~ → [Moved to FEAT-003](../FEAT-003-future-enhancements/EN-012-skill-interface/EN-012-skill-interface.md) per DISC-002

**Bug Resolutions:**
- [BUG-001: EN-009 ID Conflict](./FEAT-002--BUG-001-en009-id-conflict.md) - Resolved by renumbering ts-formatter to EN-016

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
|      (Restructured per DISC-001, BUG-001, DISC-002)              |
+------------------------------------------------------------------+
| Enablers:  [....................] 0% (0/8 completed)             |
| Deprecated: EN-010 (absorbed into EN-016)                        |
| Moved:     EN-012 → FEAT-003 (Above and Beyond)                  |
| Tasks:     [....................] 0% (0/45 completed)            |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                             |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| **Active Enablers** | 8 | EN-007,008,009,011,013,014,015,016 |
| **Deprecated Enablers** | 1 | EN-010 absorbed into EN-016 |
| **Moved Enablers** | 1 | EN-012 → FEAT-003 per DISC-002 |
| **Completed Enablers** | 0 | |
| **Total Tasks** | 45 | EN-009:TASK-001..004*, 055..058, 101-137 (*enabler-scoped, excludes EN-012) |
| **Completed Tasks** | 0 | |
| **Gates Total** | 2 | GATE-5, GATE-6 (GATE-7 moved to FEAT-003) |
| **Gates Passed** | 0 | |
| **Completion %** | 0% | |
| **Bug Resolutions** | 1 | BUG-001 (EN-009 ID conflict resolved) |

### Orchestration Artifacts

| Artifact | Purpose | Location |
|----------|---------|----------|
| [ORCHESTRATION_PLAN.md](./ORCHESTRATION_PLAN.md) | Strategic workflow (L0/L1/L2) | This folder |
| [ORCHESTRATION.yaml](./ORCHESTRATION.yaml) | Machine-readable SSOT | This folder |

---

## Orchestration Pipeline

> **See [ORCHESTRATION_PLAN.md](./ORCHESTRATION_PLAN.md)** for detailed L0/L1/L2 diagrams.
> **See [ORCHESTRATION.yaml](./ORCHESTRATION.yaml)** for machine-readable SSOT.

```
+==============================================================================+
|            FEAT-002 IMPLEMENTATION PIPELINE (RESTRUCTURED per DISC-001)       |
+==============================================================================+
|                                                                               |
|  PREREQUISITE: FEAT-001 Complete (All 4 Gates Passed)                        |
|                                                                               |
|  EXECUTION GROUP 1: CORE AGENTS (SEQUENTIAL)                                 |
|  ┌─────────────────────────────────────────────────────────────────────────┐ |
|  │  ┌─────────────────────┐          ┌─────────────────────┐              │ |
|  │  │      EN-007         │          │      EN-008         │              │ |
|  │  │   ts-parser Agent   │─────────▶│  ts-extractor Agent │              │ |
|  │  │  (TASK-101..105)    │          │   (TASK-106..112)   │              │ |
|  │  │   Per TDD-ts-parser │          │   Per TDD-ts-extractor             │ |
|  │  └─────────────────────┘          └─────────────────────┘              │ |
|  └─────────────────────────────────────────────────────────────────────────┘ |
|                                 │                                            |
|                                 ▼                                            |
|  EXECUTION GROUP 2: CONTEXT & FORMATTING (PARALLEL)                          |
|  ┌─────────────────────────────────────────────────────────────────────────┐ |
|  │  ┌─────────────────────┐                         ┌─────────────────┐   │ |
|  │  │      EN-016         │                         │    EN-013       │   │ |
|  │  │ ts-formatter Agent  │                         │Context Injection│   │ |
|  │  │  (TASK-113..119)    │                         │ (TASK-120..125) │   │ |
|  │  │ Absorbs EN-010      │                         │ YAML-only       │   │ |
|  │  └─────────┬───────────┘                         └─────────────────┘   │ |
|  └────────────│───────────────────────────────────────────────────────────┘ |
|               │                                                              |
|               ▼                                                              |
|  EXECUTION GROUP 3: MIND MAP GENERATION (SEQUENTIAL) ◄── NEW per DEC-003    |
|  ┌─────────────────────────────────────────────────────────────────────────┐ |
|  │  ┌─────────────────────┐                                               │ |
|  │  │      EN-009         │                                               │ |
|  │  │   Mind Map Gen      │  Blocked By: EN-016                           │ |
|  │  │  (TASK-001..004*)   │  *enabler-scoped numbering per DEC-003        │ |
|  │  │ Mermaid + ASCII     │                                               │ |
|  │  └─────────────────────┘                                               │ |
|  └─────────────────────────────────────────────────────────────────────────┘ |
|                                 │                                            |
|                   ╔═════════════╧═════════════╗                              |
|                   ║  ★ GATE-5: Core Review ★  ║                              |
|                   ║   Human Approval Required  ║                              |
|                   ╚═════════════╤═════════════╝                              |
|                                 │                                            |
|                                 ▼                                            |
|  EXECUTION GROUP 4: INTEGRATION & VALIDATION (PARALLEL) ◄── Renumbered      |
|  ┌─────────────────────────────────────────────────────────────────────────┐ |
|  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │ |
|  │  │     EN-011      │  │     EN-014      │  │     EN-015      │        │ |
|  │  │   Worktracker   │  │ Domain Context  │  │  Validation &   │        │ |
|  │  │   Integration   │  │     Files       │  │   Test Cases    │        │ |
|  │  │    (legacy)     │  │ (TASK-126..130) │  │ (TASK-131..137) │        │ |
|  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │ |
|  └─────────────────────────────────────────────────────────────────────────┘ |
|                                 │                                            |
|                   ╔═════════════╧═════════════╗                              |
|                   ║ ★ GATE-6: Func. Review ★  ║                              |
|                   ║  Human Approval Required   ║                              |
|                   ╚═════════════╤═════════════╝                              |
|                                 │                                            |
|                                 ▼                                            |
|                   ┌─────────────────────────────┐                            |
|                   │   FEAT-002 MVP COMPLETE     │                            |
|                   │   Ready for Release/Testing  │                            |
|                   └─────────────────────────────┘                            |
|                                                                              |
|   [EN-012 CLI Interface moved to FEAT-003 per DISC-002 - Above and Beyond]  |
+==============================================================================+
```

---

## Implementation Approach

> **Per ADR-005:** All agents are prompt-based (YAML/MD), no Python code.
> **Per DEC-002:** Context injection is YAML-only using Claude Code Skills constructs.

### Three-Agent Pipeline Architecture

```
┌────────────────┐     ┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│   ts-parser    │────▶│  ts-extractor  │────▶│  ts-formatter  │────▶│   mind-map     │
│   (EN-007)     │     │    (EN-008)    │     │    (EN-016)    │     │   (EN-009)     │
│                │     │                │     │                │     │                │
│ - VTT parsing  │     │ - Action items │     │ - 8-file packet│     │ - Mermaid gen  │
│ - SRT parsing  │     │ - Decisions    │     │ - Token mgmt   │     │ - ASCII render │
│ - Plain text   │     │ - Questions    │     │ - Deep links   │     │ - Visualization│
│ - Timestamps   │     │ - Topics       │     │ - Backlinks    │     │                │
│ - Speakers     │     │ - Speakers     │     │                │     │                │
└────────────────┘     └────────────────┘     └────────────────┘     └────────────────┘
```

### Agent File Structure (Per TDD Documents)

```
skills/transcript/
├── SKILL.md                    # Orchestrator with context_injection section
├── contexts/
│   ├── general.yaml            # General extraction rules
│   ├── transcript.yaml         # Transcript-specific context
│   └── meeting.yaml            # Meeting extends transcript
├── agents/
│   ├── ts-parser.md            # Parser agent definition
│   ├── ts-extractor.md         # Extractor agent definition
│   └── ts-formatter.md         # Formatter agent definition
├── PLAYBOOK.md                 # Step-by-step user guide
└── RUNBOOK.md                  # Operator procedures
```

### Key Design Documents

| Document | Location | Implements |
|----------|----------|------------|
| TDD-ts-parser.md | EN-005/docs/ | EN-007 |
| TDD-ts-extractor.md | EN-005/docs/ | EN-008 |
| TDD-ts-formatter.md | EN-005/docs/ | EN-016 (renumbered from EN-009) |
| SPEC-context-injection.md | EN-006/docs/specs/ | EN-013, EN-014 |
| ADR-002 (8-file packet) | docs/adrs/ | EN-016 |
| ADR-003 (Deep linking) | docs/adrs/ | EN-016 |
| ADR-004 (File splitting) | docs/adrs/ | EN-016 |
| ADR-005 (Prompt-based) | docs/adrs/ | All agents |

---

## Transcript Packet Output Structure (ADR-002)

> **8-File Packet Structure** per ADR-002. Each file <35K tokens max.
> **Deep Linking** per ADR-003 with inline anchors and backlinks sections.

```
{session-id}-transcript-output/
├── 00-index.md                    # Manifest (<5K) - links to all files
│   - File inventory with token counts
│   - Quick navigation anchors
│
├── 01-summary.md                  # Executive summary (<10K)
│   - Key takeaways
│   - Speaker highlights
│   - Confidence scores
│   <!-- BACKLINKS -->
│
├── 02-speakers.md                 # Speaker profiles (<35K)
│   - Speaking time analysis
│   - Contribution summary
│   - Inline anchors: #speaker-{name}
│   <!-- BACKLINKS -->
│
├── 03-topics.md                   # Topics (<35K, split if needed)
│   - Topic hierarchy with confidence
│   - Tiered extraction (PAT-001)
│   - Inline anchors: #topic-{id}
│   <!-- BACKLINKS -->
│
├── 04-entities.md                 # Entities (<35K)
│   - Action items with assignees
│   - Decisions with rationale
│   - Questions with context
│   - All with citations (PAT-004)
│   <!-- BACKLINKS -->
│
├── 05-timeline.md                 # Chronological view (<35K)
│   - Timestamp-ordered events
│   - Cross-references to entities
│   <!-- BACKLINKS -->
│
├── 06-insights.md                 # Analysis (<35K)
│   - Sentiment (if applicable)
│   - Key themes
│   - Risk areas
│   <!-- BACKLINKS -->
│
├── 07-visualization.md            # Visual representations
│   - Mermaid mindmap source
│   - ASCII art rendering
│   <!-- BACKLINKS -->
│
└── 08-workitems.md                # Work item suggestions
    - Tasks for worktracker
    - Traceability to source
    <!-- BACKLINKS -->
```

### File Splitting Strategy (ADR-004)

If any file exceeds 35K tokens:
- Split semantically at logical boundaries
- Use suffix: `03-topics-01.md`, `03-topics-02.md`
- Update index with split file manifest

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001: Transcript Skill Foundation](../EPIC-001-transcript-skill.md)

### Related Features

- FEAT-001: Analysis & Design (prerequisite - COMPLETE pending GATE-4)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | FEAT-001 | Analysis & design must be complete |
| Depends On | FEAT-001 GATE-4 | Consolidated Design Review approval |
| Implements | TDD-ts-parser.md | Parser agent design |
| Implements | TDD-ts-extractor.md | Extractor agent design |
| Implements | TDD-ts-formatter.md | Formatter agent design |
| Implements | SPEC-context-injection.md | Context injection mechanism |
| Implements | ADR-001 through ADR-005 | Architecture decisions |

---

## Artifacts

### Orchestration Artifacts

| Artifact | Purpose |
|----------|---------|
| [ORCHESTRATION_PLAN.md](./ORCHESTRATION_PLAN.md) | Strategic workflow with L0/L1/L2 diagrams |
| [ORCHESTRATION.yaml](./ORCHESTRATION.yaml) | Machine-readable SSOT |

### Decisions
- Inherited from FEAT-001 ADRs (ADR-001 through ADR-005)
- DEC-002: YAML-only implementation approach
- [DEC-003: Orchestration Execution Order Correction](./FEAT-002--DEC-003-orchestration-execution-order.md) - EN-009/EN-016 dependency fix, TASK-138

### Discoveries
- [DISC-001: Enabler Alignment Analysis](./FEAT-002--DISC-001-enabler-alignment-analysis.md) - Major restructuring trigger
- [DISC-002: Future Scope Analysis](./FEAT-002--DISC-002-future-scope-analysis.md) - EN-011/EN-012 scope evaluation
- [DISC-003: Quality Artifact Folder Structure](./FEAT-002--DISC-003-quality-artifact-folder-structure.md) - Critiques/QA folder requirements
- [DISC-004: Agent Instruction Compliance Failure](./FEAT-002--DISC-004-agent-instruction-compliance-failure.md) - Background task context isolation

### Bugs
- [BUG-001: EN-009 ID Conflict](./FEAT-002--BUG-001-en009-id-conflict.md) - **RESOLVED** - Two enablers shared EN-009 ID. ts-formatter renumbered to EN-016.

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-26 | Claude | pending | Feature created |
| 2026-01-26 | Claude | PLANNING | **RESTRUCTURED per DISC-001:** EN-007/008/009/013 revised, EN-010 deprecated, EN-014/EN-015 created. Task IDs renumbered to TASK-101+. ORCHESTRATION artifacts created. |
| 2026-01-26 | Claude | PLANNING | **BUG-001 RESOLVED:** EN-009 ID conflict fixed. EN-009-ts-formatter renumbered to EN-016. EN-009-mindmap-generator retained as original. All dependencies updated. |
| 2026-01-26 | Claude | PLANNING | **DISC-002 CREATED:** Future scope analysis for EN-011/EN-012. EN-011 (Worktracker) stays in FEAT-002 (core). EN-012 (CLI) recommended for FEAT-003 (Above and Beyond). |
| 2026-01-26 | Claude | PLANNING | **DISC-002 EXECUTED:** EN-012 moved to FEAT-003. GATE-7 removed from FEAT-002. Task count reduced from 49→45. Enabler count reduced from 9→8. |
| 2026-01-28 | Claude | PLANNING | **DEC-003 CREATED:** Orchestration execution order correction. EN-009 cannot be parallel with EN-016 (dependency). TASK-138 created in EN-015 for EN-008 deferred findings. |
| 2026-01-28 | Claude | PLANNING | **DEC-003 AI-003/AI-004 EXECUTED:** (1) ORCHESTRATION.yaml group renumbering (Group 2→EN-013+EN-016, Group 3→EN-009, Group 4→rest). (2) EN-009 task files created with enabler-scoped numbering (TASK-001..004). |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Feature |
| **SAFe** | Feature (Program Backlog) |
| **JIRA** | Epic (or custom issue type) |
