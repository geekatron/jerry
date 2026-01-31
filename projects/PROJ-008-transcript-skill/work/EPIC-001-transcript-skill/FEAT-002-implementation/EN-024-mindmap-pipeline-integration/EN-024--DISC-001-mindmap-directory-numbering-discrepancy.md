# EN-024:DISC-001: Mindmap Directory Numbering Discrepancy

<!--
TEMPLATE: Discovery
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9, worktracker.md (Discovery File)
CREATED: 2026-01-30
PURPOSE: Document discrepancy between ADR-002 and current implementation for mindmap output location
-->

> **Type:** discovery
> **Status:** DOCUMENTED
> **Priority:** HIGH
> **Impact:** HIGH
> **Created:** 2026-01-30T04:00:00Z
> **Completed:** 2026-01-30T04:30:00Z
> **Parent:** EN-024
> **Owner:** Claude
> **Source:** TASK-240 Pipeline State Research

---

## Summary

During TASK-240 pipeline state research, a significant discrepancy was discovered between ADR-002 (Artifact Structure) and the current ts-formatter implementation regarding file numbering. The mindmap agents reference `07-mindmap/` but this number is already used for topics in the current flat packet structure.

**Key Findings:**
- ADR-002 proposed hierarchical structure with `07-mindmap/` directory
- Current ts-formatter implementation uses flat structure where `07-topics.md` occupies the 07 slot
- Mindmap agents (ts-mindmap-mermaid, ts-mindmap-ascii) incorrectly reference `07-mindmap/`
- Resolution: Use `08-mindmap/` as the correct numbering

**Validation:** Verified by reading ADR-002, ts-formatter.md, and both mindmap agent specifications.

---

## Context

### Background

EN-024 aims to integrate mindmap generators (ts-mindmap-mermaid, ts-mindmap-ascii) from EN-009 into the default transcript skill pipeline. During research for TASK-240, the current pipeline state was analyzed to understand integration points.

### Research Question

What is the current packet structure, and where should mindmap output files be placed?

### Investigation Approach

1. Read ADR-002 (Artifact Structure & Token Management) to understand design intent
2. Read ts-formatter.md to understand current implementation
3. Read ts-mindmap-mermaid.md and ts-mindmap-ascii.md to identify referenced output paths
4. Cross-reference to identify discrepancies

---

## Finding

### F-001: ADR-002 vs Implementation Structure Mismatch

**ADR-002 Proposed Structure (Option 3: Hierarchical):**
```
{session-id}-transcript-output/
├── 00-index.md
├── 01-summary.md
├── 02-speakers/
├── 03-topics/
├── 04-entities/
├── 05-timeline/
├── 06-analysis/
├── 07-mindmap/          ← Mindmaps at position 07
│   ├── mindmap.mmd
│   └── mindmap.ascii.txt
└── 08-workitems/
```

**Current ts-formatter Implementation (Flat Structure):**
```
transcript-{id}/
├── 00-index.md
├── 01-summary.md
├── 02-transcript.md
├── 03-speakers.md
├── 04-action-items.md
├── 05-decisions.md
├── 06-questions.md
├── 07-topics.md          ← Topics at position 07 (CONFLICT!)
└── _anchors.json
```

**Evidence:**
- ADR-002 lines 136-164: Option 3 hierarchical structure with `07-mindmap/`
- ts-formatter.md lines 92-102: Flat structure with `07-topics.md`
- ts-mindmap-mermaid.md line 89: References `07-mindmap/mindmap.mmd`
- ts-mindmap-ascii.md line 89: References `07-mindmap/mindmap.ascii.txt`

### F-002: Root Cause Analysis

**Why the discrepancy exists:**

1. **ADR-002 Decision vs Implementation Drift:** ADR-002 proposed Option 3 (hierarchical) but ts-formatter implemented a simplified flat structure closer to Option 2
2. **Timing:** ts-formatter was implemented before mindmap agents were designed
3. **No Cross-Reference Check:** EN-009 mindmap agents were created based on ADR-002 without verifying against actual ts-formatter implementation

### F-003: Resolution

**Decision:** Use `08-mindmap/` as the correct output directory.

**Rationale:**
- Preserves existing ts-formatter output structure (no breaking changes to existing files)
- 08 is the next available number in the flat structure
- Minimal disruption to current implementation

**Files Requiring Update:**
| File | Current | Corrected |
|------|---------|-----------|
| `ts-mindmap-mermaid.md` | `07-mindmap/` | `08-mindmap/` |
| `ts-mindmap-ascii.md` | `07-mindmap/` | `08-mindmap/` |
| `EN-024-mindmap-pipeline-integration.md` | `07-mindmap/` | `08-mindmap/` |

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | ADR | Hierarchical structure with 07-mindmap/ | ADR-002 lines 136-164 | 2026-01-26 |
| E-002 | Agent Spec | Flat structure with 07-topics.md | ts-formatter.md lines 92-102 | 2026-01-28 |
| E-003 | Agent Spec | References 07-mindmap/mindmap.mmd | ts-mindmap-mermaid.md line 89 | 2026-01-28 |
| E-004 | Agent Spec | References 07-mindmap/mindmap.ascii.txt | ts-mindmap-ascii.md line 89 | 2026-01-28 |

### Reference Material

- **Source:** ADR-002: Artifact Structure & Token Management
- **Path:** `docs/adrs/ADR-002-artifact-structure.md`
- **Relevance:** Defines original packet structure design

- **Source:** ts-formatter Agent Definition
- **Path:** `skills/transcript/agents/ts-formatter.md`
- **Relevance:** Defines actual implemented packet structure

---

## Implications

### Impact on Project

This discovery impacts:
1. **EN-024 Implementation** - Must use 08-mindmap/ for integration
2. **Mindmap Agent Specs** - Both agents need path corrections
3. **ADR-002** - May benefit from amendment noting implementation deviation

### Design Decisions Affected

- **Decision:** EN-024 Pipeline Integration
  - **Impact:** Output path must be corrected before integration
  - **Rationale:** Prevents overwriting 07-topics.md with mindmap content

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Existing mindmap files at wrong location | LOW | No production use yet; fix now before deployment |
| ADR-002/Implementation confusion | MEDIUM | Document deviation, consider ADR amendment |
| Future file number conflicts | LOW | Reserve 09+ for future extensions |

---

## Relationships

### Creates

- Updated ts-mindmap-mermaid.md (path correction)
- Updated ts-mindmap-ascii.md (path correction)
- Updated EN-024-mindmap-pipeline-integration.md (numbering correction)

### Informs

- [EN-024](./EN-024-mindmap-pipeline-integration.md) - Pipeline integration design
- [TASK-240](./TASK-240-research-pipeline-state.md) - Research task captures this finding

### Related Discoveries

- [FEAT-002:DISC-012](../FEAT-002--DISC-012-agent-environment-context-issues.md) - Agent file consumption rules (related context)

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [EN-024](./EN-024-mindmap-pipeline-integration.md) | Parent enabler |
| ADR | [ADR-002](../../../../../docs/adrs/ADR-002-artifact-structure.md) | Original structure design |
| Agent | [ts-formatter.md](../../../../../skills/transcript/agents/ts-formatter.md) | Implemented structure |

---

## Recommendations

### Immediate Actions

1. **REQUIRED:** Update ts-mindmap-mermaid.md to use `08-mindmap/`
2. **REQUIRED:** Update ts-mindmap-ascii.md to use `08-mindmap/`
3. **REQUIRED:** Update EN-024 enabler and diagrams to reflect `08-mindmap/`
4. **OPTIONAL:** Consider ADR-002 amendment documenting implementation deviation

### Long-term Considerations

- **Packet Structure Standardization:** Consider creating a definitive packet structure document that supersedes ADR-002 and reflects actual implementation
- **Schema Validation:** Add validation that ensures output paths don't conflict

---

## Open Questions

### Questions for Follow-up

1. **Q:** Should ADR-002 be formally amended to reflect the flat structure implementation?
   - **Investigation Method:** Review ADR amendment process, assess impact
   - **Priority:** LOW (documentation improvement, not blocking)

2. **Q:** Should we reserve specific numbers for future extensions (09-xxx, 10-xxx)?
   - **Investigation Method:** Survey potential future output types
   - **Priority:** LOW

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-30 | Claude | Created discovery documenting 07 vs 08 numbering discrepancy |

---

## Metadata

```yaml
id: "EN-024:DISC-001"
parent_id: "EN-024"
work_type: DISCOVERY
title: "Mindmap Directory Numbering Discrepancy"
status: DOCUMENTED
priority: HIGH
impact: HIGH
created_by: "Claude"
created_at: "2026-01-30T04:00:00Z"
updated_at: "2026-01-30T04:30:00Z"
completed_at: "2026-01-30T04:30:00Z"
tags: [packet-structure, file-numbering, adr-deviation, mindmap]
source: "TASK-240 Pipeline State Research"
finding_type: GAP
confidence_level: HIGH
validated: true
```
