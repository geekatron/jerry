# EN-014:DISC-010: TDD Hybrid Architecture Gap - DISC-009 Not Addressed

<!--
TEMPLATE: Discovery
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9, worktracker.md (Discovery File)
CREATED: 2026-01-29 (User Review - Post TASK-178)
PURPOSE: Document missing integration of DISC-009 findings in TDD v3.0.0
TRIGGER: User feedback after TDD v3.0.0 validation
-->

> **Type:** discovery
> **Status:** RESOLVED
> **Priority:** HIGH
> **Impact:** HIGH
> **Created:** 2026-01-29T17:00:00Z
> **Completed:** 2026-01-29T18:15:00Z
> **Parent:** EN-014
> **Owner:** Claude
> **Source:** User Review (Post TASK-178)

---

## Frontmatter

```yaml
id: "EN-014:DISC-010"
work_type: DISCOVERY
title: "TDD Hybrid Architecture Gap - DISC-009 Not Addressed"

classification: TECHNICAL

status: RESOLVED
resolution: "TDD v3.1.0 revision with Section 12 and updates (ps-critic 0.97)"

priority: HIGH
impact: HIGH

assignee: "Claude"
created_by: "Claude"

created_at: "2026-01-29T17:00:00Z"
updated_at: "2026-01-29T18:15:00Z"
completed_at: "2026-01-29T18:15:00Z"

parent_id: "EN-014"

tags:
  - "tdd-gap"
  - "hybrid-architecture"
  - "disc-009"
  - "python-validation"
  - "architecture-rationale"

finding_type: GAP
confidence_level: HIGH
source: "User Review (Post TASK-178)"
research_method: "User feedback analysis"

validated: true
validation_date: "2026-01-29T17:00:00Z"
validated_by: "User"
```

---

## State Machine

**Current State:** `VALIDATED`

```
PENDING → IN_PROGRESS → DOCUMENTED → VALIDATED
                                         ↑
                                    (current)
```

---

## Summary

**Core Finding:** TDD-EN014-domain-schema-v2.md (v3.0.0) specifies Python validators (SV-001 through SV-006) but fails to incorporate the architectural findings from `FEAT-002--DISC-009-agent-only-architecture-limitation.md`. The TDD lacks the fundamental "WHY Python?" rationale and does not explain how domain validation fits within the hybrid architecture established by DISC-009.

**Key Findings:**
1. **Missing Architectural Rationale** - TDD v3.0.0 describes Python validators but doesn't explain WHY Python is required (vs. LLM-based validation)
2. **No Reference to DISC-009** - Critical research findings (Lost-in-the-Middle, 1,250x cost efficiency, hybrid architecture) are not cited
3. **FEAT-004 Not Referenced** - TDD doesn't explain how validation integrates with the Hybrid Infrastructure Initiative (FEAT-004)
4. **Missing Evidence Chain** - No connection to industry research supporting hybrid architecture decisions

**Validation:** Confirmed by User review after TASK-178 ps-critic validation passed (0.96).

---

## Context

### Background

DISC-009 established a critical architectural finding: **agent definitions are behavioral specifications, NOT executable code**. The discovery recommended a hybrid architecture where:

- **Python code** handles deterministic work (parsing, validation)
- **LLM agents** handle semantic work (entity extraction, summarization)

This finding was based on:
- Stanford "Lost-in-the-Middle" research (30%+ accuracy degradation)
- RAG vs LLM cost analysis (1,250x cheaper)
- Industry adoption data (60% of production LLM apps use RAG)

TDD v3.0.0 correctly specifies Python validators but does not reference or incorporate these findings, leaving a gap in architectural traceability.

### Research Question

**Why does the TDD specify Python validators, and how does this decision connect to the broader hybrid architecture established in DISC-009?**

### Investigation Approach

1. Review DISC-009 findings and recommendations
2. Compare against TDD v3.0.0 content
3. Identify missing connections and rationale
4. Document required TDD revisions

---

## Finding

### Gap Analysis: TDD v3.0.0 vs. DISC-009

| DISC-009 Finding | TDD v3.0.0 Status | Gap |
|------------------|-------------------|-----|
| Agent definitions are behavioral specs, not code | ❌ NOT ADDRESSED | No mention of agent vs. code distinction |
| Python for deterministic work, LLM for semantic | ❌ NOT ADDRESSED | Validators use Python but no rationale provided |
| Lost-in-the-Middle accuracy problem | ❌ NOT ADDRESSED | No reference to Stanford research |
| RAG 1,250x cost efficiency | ❌ NOT ADDRESSED | No cost analysis for validation approach |
| Hybrid architecture recommendation | ❌ NOT ADDRESSED | No mention of FEAT-004 integration |
| webvtt-py and Python libraries | ❌ NOT ADDRESSED | No library specifications for validation |
| Chunking strategy for large files | ❌ NOT ADDRESSED | No chunking considerations |

### Missing TDD Sections

The TDD v3.0.0 needs the following additions:

**Section 12: Hybrid Architecture Rationale**
- Why Python validators (not LLM-based)
- Connection to DISC-009 findings
- Evidence chain (Stanford research, cost analysis)
- Integration with FEAT-004 (Hybrid Infrastructure Initiative)

**Updates to Existing Sections:**
- Section 5.2: Reference DISC-009 for Python implementation decision
- Section 7: Reference hybrid architecture for runtime environment
- Section 10: Explain CLI integration in context of hybrid pipeline

### Evidence from DISC-009

The following DISC-009 evidence must be incorporated into TDD:

| Evidence ID | Finding | Implication for TDD |
|-------------|---------|---------------------|
| E-001 | Stanford "Lost in the Middle" - 30%+ accuracy drop | LLM-only validation unreliable for large schemas |
| E-002 | RAG 1,250x cost efficiency | Python validation is cost-effective |
| E-003 | 60% of LLM apps use hybrid/RAG | Industry standard supports hybrid approach |
| E-004 | webvtt-py library | Python ecosystem has mature tooling |

### User Feedback (Verbatim)

> "I reviewed the TDD and it doesn't look like any of the feedback from the following discovery `FEAT-002--DISC-009-agent-only-architecture-limitation.md` was addressed. We are talking about the Python code and this is a significant oversight that has to be addressed as well."

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | User Feedback | Direct user review of TDD v3.0.0 | Session transcript | 2026-01-29 |
| E-002 | Discovery | DISC-009 Agent-Only Architecture Limitation | FEAT-002--DISC-009 | 2026-01-28 |
| E-003 | TDD | TDD-EN014-domain-schema-v2.md v3.0.0 | docs/design/ | 2026-01-29 |
| E-004 | Validation | TASK-178 ps-critic validation (0.96) | critiques/EN-014-e-178 | 2026-01-29 |

### DISC-009 Key Citations (To Be Incorporated)

1. **Stanford NLP**: Lost-in-the-Middle research - 30%+ accuracy degradation in middle context
2. **Meilisearch**: RAG vs LLM cost analysis - $0.00008 vs $0.10 (1,250x difference)
3. **byteiota**: RAG adoption surge - 60% of production LLM apps use RAG (2024-2026)
4. **Elasticsearch Labs**: Hybrid architecture best practices

---

## Implications

### Impact on Project

1. **TASK-169 (Human Approval Gate)** - Cannot proceed until TDD addresses DISC-009
2. **Implementation Tasks (TASK-126..159)** - Implementers need architectural rationale
3. **Traceability** - Missing link between validation design and hybrid architecture decision

### Design Decisions Affected

| Decision | Impact | Required Update |
|----------|--------|-----------------|
| TDD-EN014-domain-schema-v2.md | Needs Section 12 | Add hybrid architecture rationale |
| Section 5.2 Python Validators | Missing context | Reference DISC-009 |
| Section 10 CLI Integration | Missing context | Reference hybrid pipeline |

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Implementers lack context for Python choice | HIGH | Add Section 12 with rationale |
| No traceability to DISC-009 | MEDIUM | Add explicit references |
| Validation approach not connected to FEAT-004 | MEDIUM | Add integration explanation |

---

## Relationships

### Creates

- TASK-179 - ps-analyst Gap Analysis for DISC-009 TDD Integration
- TASK-180 - nse-architect TDD v3.1.0 Revision (DISC-009 Integration)
- TASK-181 - ps-critic TDD v3.1.0 Validation

### Blocks

- [TASK-169](./TASK-169-human-gate.md) - Human Approval Gate (cannot proceed until TDD revised)

### Related Discoveries

- [FEAT-002:DISC-009](../FEAT-002--DISC-009-agent-only-architecture-limitation.md) - Agent-Only Architecture Limitation (SOURCE)
- [EN-014:DISC-008](./EN-014--DISC-008-comprehensive-tdd-implementation-gap.md) - Prior TDD gaps (RESOLVED)

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [EN-014-domain-context-files.md](./EN-014-domain-context-files.md) | Parent enabler |
| TDD | [TDD-EN014-domain-schema-v2.md](./docs/design/TDD-EN014-domain-schema-v2.md) | Document with gap |
| DISC-009 | [FEAT-002--DISC-009](../FEAT-002--DISC-009-agent-only-architecture-limitation.md) | Source architecture finding |
| FEAT-004 | [FEAT-004-hybrid-infrastructure](../FEAT-004-hybrid-infrastructure/) | Hybrid Infrastructure Initiative |

---

## Recommendations

### Immediate Actions

1. **TASK-179**: ps-analyst deep analysis to map DISC-009 findings to TDD sections
2. **TASK-180**: nse-architect TDD revision to v3.1.0 with Section 12 and updates
3. **TASK-181**: ps-critic validation at 0.95 threshold
4. Ensure agents use Context7 and WebSearch for additional research

### TDD Revision Requirements

The revised TDD v3.1.0 must include:

1. **New Section 12: Hybrid Architecture Rationale**
   - Why Python for validation (not LLM-based)
   - Reference to DISC-009 findings with citations
   - Evidence chain (Stanford, Meilisearch, byteiota)
   - Integration with FEAT-004

2. **Updated Section 5.2: Semantic Validators**
   - Add rationale paragraph referencing DISC-009
   - Explain why deterministic Python is required

3. **Updated Section 7: Runtime Environment**
   - Connect Python environment to hybrid architecture

4. **Updated Section 10: CLI Integration**
   - Explain how CLI validation fits hybrid pipeline

---

## Open Questions

### Questions for Gap Analysis (TASK-179)

1. **Q:** What additional sections of TDD need DISC-009 references?
   - **Investigation Method:** ps-analyst systematic section review
   - **Priority:** HIGH

2. **Q:** Should FEAT-004 integration details be included in TDD or separate document?
   - **Investigation Method:** Research existing integration patterns
   - **Priority:** MEDIUM

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-29T17:00:00Z | Claude | Created discovery from user review feedback |

---

## Metadata

```yaml
id: "EN-014:DISC-010"
parent_id: "EN-014"
work_type: DISCOVERY
title: "TDD Hybrid Architecture Gap - DISC-009 Not Addressed"
status: RESOLVED
priority: HIGH
impact: HIGH
created_by: "Claude"
created_at: "2026-01-29T17:00:00Z"
updated_at: "2026-01-29T18:15:00Z"
completed_at: "2026-01-29T18:15:00Z"
tags: ["tdd-gap", "hybrid-architecture", "disc-009", "python-validation", "architecture-rationale"]
source: "User Review (Post TASK-178)"
finding_type: GAP
confidence_level: HIGH
validated: true
extends: "FEAT-002:DISC-009"
creates:
  - "TASK-179"
  - "TASK-180"
  - "TASK-181"
blocks:
  - "TASK-169"
```
