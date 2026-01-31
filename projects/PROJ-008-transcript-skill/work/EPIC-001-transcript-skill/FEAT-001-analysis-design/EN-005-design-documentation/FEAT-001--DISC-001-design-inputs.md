# DISC-001: Design Documentation Inputs Discovery

<!--
TEMPLATE: Discovery
VERSION: 2.0.0
SOURCE: ONTOLOGY-v1.md Section 3.5.1
UPDATED: 2026-01-26
-->

> **Type:** discovery
> **Status:** documented
> **Priority:** high
> **Impact:** high
> **Created:** 2026-01-26T09:30:00Z
> **Updated:** 2026-01-26T09:30:00Z
> **Parent:** EN-005
> **Owner:** Claude
> **Related:** FEAT-001, EN-003, EN-004

---

## Summary

This discovery documents the consolidation of inputs from EN-003 (Requirements Synthesis) and EN-004 (Architecture Decision Records) that inform EN-005 Design Documentation. The synthesis of 40 requirements from EN-003 and 5 ADRs from EN-004 provides a complete foundation for technical design.

---

## Discovery Context

### L0: Executive Summary (ELI5)

Think of building a house. Before writing the detailed blueprints (EN-005), we need two things:
1. **What the house needs to do** (EN-003 Requirements) - 40 detailed requirements like "needs 3 bedrooms, 2 bathrooms, can handle 4 people"
2. **Key building decisions** (EN-004 ADRs) - 5 architectural decisions like "use brick not wood, single-story not two"

This discovery captures what we learned from analyzing these inputs so we can write complete technical designs.

### L1: Technical Context (Engineer)

EN-005 Design Documentation receives inputs from two predecessor enablers:

```
EN-003 Requirements          EN-004 ADRs                EN-005 Design
==================          ===========                ==============

40 Requirements             5 Architecture             TDD Documents
├── 10 STK (Needs)          Decisions                  AGENT.md Files
├── 15 FR (Functional)      ├── ADR-001: Agents        SKILL.md
├── 10 NFR (Non-Func)       ├── ADR-002: Artifacts     PLAYBOOK
└── 5 IR (Interface)        ├── ADR-003: Linking       RUNBOOK
                            ├── ADR-004: Splitting
6 Design Patterns           └── ADR-005: Phasing
20 FMEA Risks
8 Assumptions
```

### L2: Strategic Implications (Architect)

The combination of requirements and ADRs provides:
1. **Complete scope** - Every TDD can trace to specific requirements
2. **Clear architecture** - Agent boundaries and responsibilities defined
3. **Risk coverage** - Design addresses all YELLOW risks from FMEA
4. **Quality targets** - Measurable criteria for validation

---

## Key Discoveries

### Discovery 1: Requirements-to-Agent Mapping

The 40 requirements map to the 3 custom agents defined in ADR-001:

| Agent | Requirements Covered | Primary Focus |
|-------|---------------------|---------------|
| ts-parser | FR-001..004, NFR-006, NFR-007 | Input parsing, format detection |
| ts-extractor | FR-005..011, NFR-003, NFR-004, NFR-008 | Entity extraction, confidence scoring |
| ts-formatter | FR-012..015, NFR-009, NFR-010, IR-004, IR-005 | Output generation, linking, splitting |

**Implication**: Each TDD must show requirement traceability matrix.

### Discovery 2: Design Pattern Implementation

Six design patterns from EN-003 REQUIREMENTS-SPECIFICATION.md must be documented in TDDs:

| Pattern ID | Pattern Name | TDD Location |
|------------|--------------|--------------|
| PAT-001 | Tiered Extraction Pipeline | TDD-ts-extractor |
| PAT-002 | Defensive Parsing | TDD-ts-parser |
| PAT-003 | Multi-Pattern Speaker Detection | TDD-ts-extractor |
| PAT-004 | Citation-Required Extraction | TDD-ts-formatter |
| PAT-005 | Versioned Schema Evolution | TDD-ts-formatter |
| PAT-006 | Hexagonal Skill Architecture | TDD-transcript-skill |

**Implication**: TDDs must show how patterns are implemented, not just referenced.

### Discovery 3: ADR Implementation Specifications

Each ADR provides specific implementation guidance:

| ADR | Key Specifications for TDDs |
|-----|----------------------------|
| ADR-001 | Agent boundaries, ps-critic quality gates, single nesting |
| ADR-002 | 35K token limit, hierarchical packet (00-index.md, 01-summary.md, etc.) |
| ADR-003 | Anchor naming `{type}-{nnn}`, backlinks section template |
| ADR-004 | 31.5K soft limit (90% of 35K), split at `##` headings |
| ADR-005 | AGENT.md template from PS_AGENT_TEMPLATE.md, Phase 2 migration triggers |

**Implication**: TDDs must include ADR compliance checklist.

### Discovery 4: Risk Mitigation Through Design

Five YELLOW risks from FMEA require explicit design coverage:

| Risk | Score | Design Mitigation |
|------|-------|-------------------|
| R-002 (SRT timestamps) | 8 | ts-parser: timestamp normalization logic |
| R-004 (Missing voice tags) | 12 | ts-extractor: 4-pattern fallback chain |
| R-006/R-007 (Precision/Recall) | 12 | ts-extractor: confidence thresholds |
| R-008 (Hallucination) | 12 | ts-formatter: citation validation |
| R-014 (Schema breaking) | 9 | ts-formatter: version in JSON schema |

**Implication**: TDDs must show risk mitigation design, not just reference.

### Discovery 5: Quality Gate Integration

ps-critic integration from ADR-001 requires:
- Each TDD reviewed with quality score >= 0.90
- Aggregate quality for EN-005 >= 0.90
- Review criteria aligned with Jerry Constitution P-001, P-002, P-004

**Implication**: TASK-011, TASK-012, TASK-013 define ps-critic review scope.

### Discovery 6: Token Budget Allocation

From ADR-002 (35K limit) and ADR-004 (31.5K soft):

| Deliverable | Estimated Tokens | Within Budget |
|-------------|------------------|---------------|
| TDD-transcript-skill.md | ~15K | YES |
| TDD-ts-parser.md | ~10K | YES |
| TDD-ts-extractor.md | ~12K | YES |
| TDD-ts-formatter.md | ~15K | YES |
| ts-parser AGENT.md | ~3K | YES |
| ts-extractor AGENT.md | ~5K | YES |
| ts-formatter AGENT.md | ~4K | YES |
| SKILL.md | ~3K | YES |

**Implication**: All deliverables fit within single-file budget.

---

## Consolidated Input Summary

### Requirements Input (EN-003)

```
REQUIREMENTS SUMMARY FROM EN-003
================================

Total Requirements:     40
├── Stakeholder Needs:  10 (STK-001..010)
├── Functional:         15 (FR-001..015)
├── Non-Functional:     10 (NFR-001..010)
└── Interface:           5 (IR-001..005)

Priority Distribution:
├── MUST:               31 (78%)
└── SHOULD:              9 (22%)

Risk Coverage:
├── YELLOW Risks:        5 (all covered by requirements)
└── GREEN Risks:        15

Phase Allocation:
├── Phase 1 (Foundation):   9 requirements
├── Phase 2 (Core):         8 requirements
├── Phase 3 (Integration): 10 requirements
└── Phase 4 (Validation):   3 requirements
```

### ADR Input (EN-004)

```
ADR SUMMARY FROM EN-004
=======================

Total ADRs:              5
Aggregate Quality:       0.924 (exceeds 0.90 threshold)

ADR Decisions:
├── ADR-001: Hybrid Architecture (3 custom agents + ps-critic)
├── ADR-002: Hierarchical Packet Structure (35K limit)
├── ADR-003: Custom Anchors (bidirectional linking)
├── ADR-004: Semantic Boundary Split (31.5K soft limit)
└── ADR-005: Phased Implementation (prompt-based first)

All ADRs: APPROVED at GATE-3
```

---

## Traceability Matrix

### EN-005 Tasks → EN-003 Requirements

| Task | Requirements Covered |
|------|---------------------|
| TASK-001 (TDD Overview) | All FR, NFR, IR |
| TASK-002 (TDD ts-parser) | FR-001..004, NFR-006, NFR-007 |
| TASK-003 (TDD ts-extractor) | FR-005..011, NFR-003, NFR-004, NFR-008 |
| TASK-004 (TDD ts-formatter) | FR-012..015, NFR-009, NFR-010, IR-004, IR-005 |
| TASK-005 (ts-parser AGENT.md) | FR-001..004 |
| TASK-006 (ts-extractor AGENT.md) | FR-005..011 |
| TASK-007 (ts-formatter AGENT.md) | FR-012..015 |
| TASK-008 (SKILL.md) | IR-004, IR-005 |

### EN-005 Tasks → EN-004 ADRs

| Task | ADRs Referenced |
|------|-----------------|
| TASK-001 (TDD Overview) | ADR-001, ADR-002, ADR-005 |
| TASK-002 (TDD ts-parser) | ADR-001, ADR-002 |
| TASK-003 (TDD ts-extractor) | ADR-001, ADR-002 |
| TASK-004 (TDD ts-formatter) | ADR-001, ADR-002, ADR-003, ADR-004 |
| TASK-005..007 (AGENT.md) | ADR-005 (template) |
| TASK-008 (SKILL.md) | ADR-001, ADR-005 |

---

## Impact Assessment

| Impact Area | Severity | Description |
|-------------|----------|-------------|
| TDD Completeness | HIGH | All TDDs must trace to requirements |
| ADR Compliance | HIGH | Design must implement ADR decisions |
| Risk Coverage | HIGH | Design must address YELLOW risks |
| Quality Gates | MEDIUM | ps-critic reviews at 0.90 threshold |
| Token Budgets | LOW | All files within 35K limit |

---

## Recommendations

1. **TASK-001 (TDD Overview)** should establish the requirements traceability baseline
2. **Each TDD** should include ADR Compliance Checklist section
3. **TASK-004 (ts-formatter TDD)** is most complex - covers linking, splitting, formatting
4. **PLAYBOOK** should reference specific requirements for each phase
5. **RUNBOOK** should include troubleshooting for each YELLOW risk

---

## Related Artifacts

| Artifact | Relationship | Path |
|----------|--------------|------|
| REQUIREMENTS-SPECIFICATION.md | Source | EN-003-requirements-synthesis/requirements/ |
| NASA-SE-REQUIREMENTS.md | Source | EN-003-requirements-synthesis/requirements/ |
| ADR-001..005 | Source | docs/adrs/ |
| EN-004-final-review.md | Source | EN-004-architecture-decisions/review/ |
| EN-005-design-documentation.md | Target | EN-005-design-documentation/ |
| ORCHESTRATION_EN005.yaml | Target | EN-005-design-documentation/ |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-26 | Claude | documented | Initial discovery documenting EN-003 and EN-004 inputs |

---

*Discovery ID: DISC-001*
*Constitutional Compliance: P-002 (persisted), P-004 (provenance), P-011 (evidence-based)*
