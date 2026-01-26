# DEC-001: Design Documentation Approach

<!--
TEMPLATE: Decision
VERSION: 2.0.0
SOURCE: ONTOLOGY-v1.md Section 3.5.2
UPDATED: 2026-01-26
-->

> **Type:** decision
> **Status:** accepted
> **Priority:** high
> **Impact:** high
> **Created:** 2026-01-26T09:30:00Z
> **Updated:** 2026-01-26T09:30:00Z
> **Parent:** EN-005
> **Owner:** Claude
> **Related:** DISC-001, FEAT-001, EN-003, EN-004

---

## Summary

This decision document captures the design approach decisions for EN-005 Design Documentation based on consolidated inputs from EN-003 Requirements Synthesis and EN-004 Architecture Decision Records.

---

## Decision Context

### L0: Executive Summary (ELI5)

We need to decide HOW to write the technical blueprints (design documents) for the Transcript Skill. Key questions:
- What format should documents follow?
- How do we ensure nothing is forgotten?
- How do we organize the work?
- What quality checks do we need?

### L1: Technical Context (Engineer)

EN-005 creates 10+ design artifacts. Key technical decisions:
1. Document structure and templates
2. Task sequencing and dependencies
3. Quality gate integration
4. ADR compliance verification

### L2: Strategic Context (Architect)

Design documentation bridges requirements (EN-003) and implementation (FEAT-002). Decisions here affect:
- Implementation velocity
- Maintainability
- Quality assurance
- Future extensibility

---

## Decisions Made

### DEC-001-001: TDD Structure with L0/L1/L2 Perspectives

**Question:** How should Technical Design Documents be structured?

**Decision:** All TDDs SHALL use the triple-lens approach (L0/L1/L2) as established in the Jerry Constitution and problem-solving skill.

**Rationale:**
- Consistency with existing Jerry framework patterns
- Supports multiple stakeholder audiences
- Enables efficient context loading during implementation
- ps-critic quality scoring accounts for this structure

**Structure:**
```
TDD-{component}.md
├── L0: Executive Summary (ELI5)
│   └── Simple analogy, key value, 1-page summary
├── L1: Technical Specification (Engineer)
│   ├── Component architecture
│   ├── Data contracts (JSON schemas)
│   ├── Algorithm descriptions
│   └── Interface definitions
└── L2: Strategic Design (Architect)
    ├── Performance implications
    ├── Trade-offs and alternatives
    ├── Evolution strategy
    └── Risk mitigation
```

**Evidence:** Jerry Constitution principle P-004 (explicit provenance); problem-solving skill template.

---

### DEC-001-002: ADR Compliance Checklist in Each TDD

**Question:** How do we ensure TDDs implement ADR decisions correctly?

**Decision:** Each TDD SHALL include an ADR Compliance Checklist section that explicitly verifies implementation of relevant ADR decisions.

**Rationale:**
- Prevents ADR decisions from being lost in translation
- Provides audit trail for GATE-4 review
- Enables targeted ps-critic validation

**Template:**
```markdown
## ADR Compliance Checklist

| ADR | Decision | Compliance Status | Evidence |
|-----|----------|-------------------|----------|
| ADR-001 | Hybrid Architecture | [ ] Compliant | See Section X |
| ADR-002 | 35K Token Limit | [ ] Compliant | Token count: Y |
| ...
```

**Evidence:** DISC-001 Discovery 3; ADR-001 through ADR-005.

---

### DEC-001-003: Requirements Traceability Matrix in TDDs

**Question:** How do we ensure TDDs cover all requirements?

**Decision:** TASK-001 (TDD Overview) SHALL establish the master Requirements Traceability Matrix (RTM), and each component TDD SHALL include a focused RTM for its scope.

**Rationale:**
- Ensures 100% requirement coverage
- Prevents orphan requirements
- Supports NASA SE methodology compliance from EN-003
- Enables verification planning

**Structure:**
```markdown
## Requirements Traceability

| Requirement | Description | Section | Verification |
|-------------|-------------|---------|--------------|
| FR-001 | VTT Parsing | 3.2.1 | Unit Test |
| NFR-006 | Timestamp Normalization | 3.2.2 | Unit Test |
```

**Evidence:** EN-003 REQUIREMENTS-SPECIFICATION.md Section 4.1; NASA-HDBK-1009A.

---

### DEC-001-004: Sequential TDD Development with Dependencies

**Question:** In what order should TDDs be developed?

**Decision:** TDDs SHALL be developed in dependency order:

```
TASK-001 (Overview)
     │
     ├──▶ TASK-002 (ts-parser)  ──┐
     │                             │
     └──▶ TASK-003 (ts-extractor) ─┼──▶ TASK-004 (ts-formatter)
                                   │
                                   ▼
```

**Rationale:**
- TASK-001 establishes architecture context for component TDDs
- ts-parser and ts-extractor can run in parallel (no dependency)
- ts-formatter depends on both (needs input/output contracts)

**Evidence:** ORCHESTRATION_EN005.yaml execution_queue; ADR-001 agent boundaries.

---

### DEC-001-005: AGENT.md Template from ADR-005

**Question:** What template should AGENT.md files follow?

**Decision:** All AGENT.md files SHALL follow the PS_AGENT_TEMPLATE.md structure defined in ADR-005.

**Template Sections:**
```markdown
# {agent-name} Agent

> Version, role, constitutional compliance

## Purpose
## Capabilities
## Tool Access
## Input/Output Contracts
## Quality Gates
## Integration Points
## Examples
```

**Rationale:**
- Consistency with problem-solving skill agents
- Enables potential migration to Python (Phase 2 per ADR-005)
- Supports ps-critic quality scoring

**Evidence:** ADR-005 Section 5.1 (Agent Definition Structure).

---

### DEC-001-006: ps-critic Review Strategy

**Question:** How should ps-critic reviews be integrated?

**Decision:** ps-critic reviews SHALL occur at two levels:

1. **Component-Level Reviews (TASK-011, TASK-012)**
   - TASK-011: Review all TDD documents (TASK-001 through TASK-004)
   - TASK-012: Review all AGENT.md files (TASK-005 through TASK-008)

2. **Aggregate Review (TASK-013)**
   - Aggregate quality score from TASK-011 + TASK-012
   - Final gate check before GATE-4

**Quality Thresholds:**
- Individual document: >= 0.85
- Aggregate score: >= 0.90
- Maximum iterations: 3 per document

**Rationale:**
- Matches EN-004 review strategy (successful at 0.924)
- Prevents scope creep from endless revisions
- Provides clear GATE-4 criteria

**Evidence:** EN-004 ORCHESTRATION_EN004.yaml quality section; ADR-001.

---

### DEC-001-007: PLAYBOOK Phase Alignment

**Question:** How should the PLAYBOOK be structured?

**Decision:** PLAYBOOK-en005.md SHALL align with the 4 implementation phases from EN-003:

```
PLAYBOOK Phases:
├── Phase 1: Foundation (FR-001..004, NFR-006, NFR-007, IR-001..003)
├── Phase 2: Core Extraction (FR-005..011, NFR-003, NFR-004, NFR-008)
├── Phase 3: Integration (FR-008..015, NFR-009, NFR-010, IR-004, IR-005)
└── Phase 4: Validation (NFR-001, NFR-002, NFR-005)
```

**Rationale:**
- Direct traceability to requirements
- Aligns with stakeholder expectations
- Supports incremental delivery

**Evidence:** EN-003 REQUIREMENTS-SPECIFICATION.md Section 4.1 (Implementation Phase Mapping).

---

### DEC-001-008: RUNBOOK Risk-Based Structure

**Question:** How should the RUNBOOK be organized?

**Decision:** RUNBOOK-en005.md SHALL include troubleshooting sections for each YELLOW risk from FMEA:

```
RUNBOOK Troubleshooting Sections:
├── R-002: SRT Timestamp Issues
├── R-004: Missing Speaker Identification
├── R-006: Low Action Item Precision
├── R-007: Low Action Item Recall
├── R-008: Hallucination Detection
└── R-014: JSON Schema Compatibility
```

**Rationale:**
- Risk-informed documentation
- Proactive troubleshooting guidance
- Supports operational excellence

**Evidence:** EN-003 FMEA-ANALYSIS.md; REQUIREMENTS-SPECIFICATION.md Section 1.2 (YELLOW Risk Coverage).

---

### DEC-001-009: Token Budget Monitoring

**Question:** How do we ensure documents stay within token budgets?

**Decision:** Each document SHALL track token count against ADR-002/ADR-004 limits:

| Budget Type | Limit | Source |
|-------------|-------|--------|
| Hard Limit | 35,000 tokens | ADR-002 |
| Soft Limit | 31,500 tokens (90%) | ADR-004 |
| Warning Threshold | 28,000 tokens (80%) | Convention |

**Monitoring:** TDD authors SHALL include token count estimate in document metadata.

**Rationale:**
- Prevents context window overflow
- Ensures single-file readability
- Supports Claude Code integration

**Evidence:** ADR-002, ADR-004.

---

### DEC-001-010: Bidirectional Linking Implementation

**Question:** How should TDDs implement ADR-003 bidirectional linking?

**Decision:** TDDs SHALL use the anchor format from ADR-003:

```html
<!-- Forward link anchor -->
<a id="req-001">FR-001: VTT Parsing</a>

<!-- Backlink in source -->
See [FR-001](#req-001) for details.
```

**Backlinks Section:** Each TDD SHALL include a "Backlinks" section listing all incoming references.

**Rationale:**
- Consistent with ADR-003 decision
- Enables navigation in rendered Markdown
- Supports Claude Code file reading

**Evidence:** ADR-003 Section 5.1 (Anchor Naming Convention).

---

## Decision Summary Matrix

| ID | Decision | Applies To | ADR/Source |
|----|----------|-----------|------------|
| DEC-001-001 | L0/L1/L2 Structure | All TDDs | Jerry Constitution |
| DEC-001-002 | ADR Compliance Checklist | All TDDs | ADR-001..005 |
| DEC-001-003 | Requirements Traceability | All TDDs | EN-003 |
| DEC-001-004 | Sequential Development | Task ordering | ORCHESTRATION_EN005 |
| DEC-001-005 | AGENT.md Template | TASK-005..007 | ADR-005 |
| DEC-001-006 | ps-critic Review Strategy | TASK-011..013 | ADR-001 |
| DEC-001-007 | PLAYBOOK Phase Alignment | TASK-009 | EN-003 |
| DEC-001-008 | RUNBOOK Risk Structure | TASK-010 | EN-003 FMEA |
| DEC-001-009 | Token Budget Monitoring | All documents | ADR-002, ADR-004 |
| DEC-001-010 | Bidirectional Linking | All TDDs | ADR-003 |

---

## Acceptance Criteria

- [ ] All TDDs follow L0/L1/L2 structure
- [ ] All TDDs include ADR Compliance Checklist
- [ ] All TDDs include Requirements Traceability section
- [ ] Task dependencies enforced in execution
- [ ] AGENT.md files follow PS_AGENT_TEMPLATE.md
- [ ] ps-critic reviews achieve >= 0.90 aggregate
- [ ] PLAYBOOK aligns with 4 implementation phases
- [ ] RUNBOOK covers all 5 YELLOW risks
- [ ] All documents within token budget
- [ ] Bidirectional links use ADR-003 anchor format

---

## Related Items

| Document | Relationship |
|----------|--------------|
| DISC-001 | Informs decisions |
| REQUIREMENTS-SPECIFICATION.md | Source for traceability |
| ADR-001..005 | Source for compliance |
| ORCHESTRATION_EN005.yaml | Execution context |
| EN-005-design-documentation.md | Target enabler |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-26 | Claude | accepted | Initial design approach decisions |

---

*Decision ID: DEC-001*
*Constitutional Compliance: P-002 (persisted), P-004 (provenance), P-011 (evidence-based)*
