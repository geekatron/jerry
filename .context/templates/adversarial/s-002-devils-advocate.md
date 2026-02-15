# S-002 Devil's Advocate -- Adversarial Strategy Execution Template

<!--
TEMPLATE: S-002 Devil's Advocate Strategy Execution
VERSION: 1.0.0 | DATE: 2026-02-15
SOURCE: quality-enforcement.md SSOT, ADR-EPIC002-001, TEMPLATE-FORMAT.md v1.1.0
ENABLER: EN-806
STATUS: ACTIVE
CONFORMANCE: TEMPLATE-FORMAT.md v1.1.0

Academic Foundation:
- Nemeth (2018): "In Defense of Troublemakers" -- genuine vs. assigned dissent effectiveness
- Janis (1982): "Groupthink" -- catastrophic consensus failures
- Schwenk (1984): Devil's Advocate in strategic decision-making
- CIA Tradecraft Primer (2009): Structured analytic techniques for intelligence analysis

Origin: Catholic Church, 1587 (Pope Sixtus V). Advocatus diaboli argued against canonization.
Domain: Decision Science, Organizational Behavior, Group Decision-Making, Argumentation.
-->

> **Type:** adversarial-strategy-template
> **Status:** ACTIVE
> **Version:** 1.0.0
> **Date:** 2026-02-15
> **Source:** quality-enforcement.md, ADR-EPIC002-001, ADR-EPIC002-002
> **Format Conformance:** TEMPLATE-FORMAT.md v1.1.0
> **Enabler:** EN-806

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Identity](#identity) | Strategy classification and metadata |
| [Purpose](#purpose) | When and why to apply Devil's Advocate |
| [Prerequisites](#prerequisites) | Required inputs and ordering constraints (H-16) |
| [Execution Protocol](#execution-protocol) | Step-by-step counter-argument construction |
| [Output Format](#output-format) | Required structure for Devil's Advocate report |
| [Scoring Rubric](#scoring-rubric) | Meta-evaluation of strategy execution quality |
| [Examples](#examples) | Concrete C2 demonstration with findings |
| [Integration](#integration) | Cross-strategy pairing, H-16 compliance, criticality mapping |

---

## Identity

| Field | Value |
|-------|-------|
| Strategy ID | S-002 |
| Strategy Name | Devil's Advocate |
| Family | Role-Based Adversarialism |
| Composite Score | 4.10 |
| Finding Prefix | DA-NNN-{execution_id} |
| Version | 1.0.0 |
| Date | 2026-02-15 |

### Criticality Tier Table

| Level | Name | Status | Notes |
|-------|------|--------|-------|
| C1 | Routine | OPTIONAL | C1 enforces HARD rules only; adversarial critique not required |
| C2 | Standard | REQUIRED | Part of C2 required set (S-007, S-002, S-014) |
| C3 | Significant | REQUIRED | Inherited from C2 set |
| C4 | Critical | REQUIRED | All 10 strategies required; tournament mode |

**Foundation:** Nemeth (2018) demonstrates that assigned dissent, while less effective than genuine disagreement, systematically improves decision quality by surfacing hidden assumptions and forcing argument strengthening. Janis (1982) documents catastrophic groupthink failures (Bay of Pigs, Challenger) that Devil's Advocate prevents.

**Jerry Implementation:** Explicitly assigns the adversarial role of arguing against the deliverable's positions, assumptions, and claims. Constructs the strongest possible counter-arguments, forcing the creator to respond substantively. Implements H-16 ordering (S-003 Steelman MUST run before S-002).

---

## Purpose

### When to Use

1. **C2+ Deliverable Review:** ALL Standard+ deliverables MUST undergo Devil's Advocate critique (required at C2). Apply after Steelman (S-003) has strengthened the deliverable to ensure critique targets a robust version.

2. **Quick Consensus or Groupthink Risk:** When a decision was reached rapidly without significant debate, or when all participants agree without visible tension, Devil's Advocate surfaces the arguments that were not made.

3. **Architecture and Design Reviews:** For design decisions (ADRs, architecture proposals, API designs) where the cost of a wrong decision is high. Counter-arguments reveal unstated assumptions about scalability, maintainability, or coupling.

4. **Requirements Reviews:** When requirements appear complete but may contain hidden assumptions, missing edge cases, or unstated dependencies. Devil's Advocate challenges each requirement's necessity, sufficiency, and feasibility.

5. **Pre-Commit Quality Gate:** Before merging deliverables that affect shared infrastructure, APIs, or framework behavior. Catching logical flaws pre-merge is orders of magnitude cheaper than post-merge remediation.

### When NOT to Use

1. **Genuine Disagreement Already Exists:** If stakeholders already hold opposing views and debate is active, Devil's Advocate adds redundant conflict without new insight. Redirect to S-003 (Steelman) to strengthen both positions, then S-013 (Inversion) to find the resolution.

2. **Trivial or C1 Routine Decisions:** For reversible single-session work affecting fewer than 3 files, the overhead of formal adversarial critique exceeds its value. Redirect to S-010 (Self-Refine) as the sole required C1 strategy.

3. **Creative Ideation or Brainstorming Phase:** Devil's Advocate prematurely constrains idea generation. Use S-003 (Steelman) to strengthen nascent ideas before subjecting them to critique.

### Expected Outcome

A Devil's Advocate report containing:
- Enumeration of all explicit and implicit assumptions in the deliverable
- At least 3 counter-arguments with DA-NNN identifiers, each targeting a distinct claim or assumption
- Severity classification (Critical/Major/Minor) with evidence for each finding
- Mapping of findings to the 6 S-014 scoring dimensions
- Prioritized list of counter-arguments requiring substantive creator response
- Measurable quality improvement when findings are addressed (target: 0.05+ composite score increase)

### Pairing Recommendations

**H-16 Compliance (MANDATORY):** Run S-003 Steelman BEFORE S-002 Devil's Advocate. H-16 requires the deliverable to be strengthened before adversarial critique. This prevents premature attack on weak first drafts and ensures critique targets a robust version.

| Pairing | Order | Rationale |
|---------|-------|-----------|
| **S-003 + S-002** | S-003 -> S-002 | H-16: Steelman strengthens before critique attacks |
| **S-002 + S-014** | S-002 -> S-014 | Findings feed dimension scoring; S-014 validates post-revision quality |
| **S-002 + S-007** | S-007 -> S-002 | Constitutional check identifies rule violations; S-002 attacks logical coherence |
| **S-002 + S-004** | S-002 + S-004 (parallel or sequential) | Complementary: S-002 attacks current claims; S-004 imagines future failures |

**Optimal sequence:** S-003 -> S-007 -> S-002 -> S-014

---

## Prerequisites

### Required Inputs

- [ ] Deliverable artifact (document, design, ADR, analysis, plan, etc.)
- [ ] Criticality level classification (C2, C3, or C4)
- [ ] S-003 Steelman output (H-16 compliance: Steelman MUST have been applied first)
- [ ] Quality framework SSOT (`quality-enforcement.md`) for dimension weights and threshold
- [ ] Domain context sufficient to construct informed counter-arguments

### Context Requirements

The advocate must have domain expertise sufficient to construct credible counter-arguments, familiarity with the deliverable's claims and recommendations, and access to the S-003 Steelman output. The deliverable must be in a complete, reviewable state (not partial or placeholder) and have been strengthened by S-003 (H-16 compliance verified).

### Ordering Constraints

**H-16 (MANDATORY):** S-003 Steelman MUST be applied before S-002 Devil's Advocate. The deliverable MUST be strengthened before adversarial critique begins. Executing S-002 without prior S-003 is an H-16 violation.

**Recommended sequence:**
1. S-010 Self-Refine (creator self-review)
2. S-003 Steelman (strengthen the deliverable)
3. S-007 Constitutional AI Critique (HARD rule compliance)
4. **S-002 Devil's Advocate (this strategy)**
5. S-014 LLM-as-Judge (score the revised deliverable)

**Minimum:** S-003 before S-002. S-014 after S-002 for dimensional scoring.

---

## Execution Protocol

### Step 1: Assume the Advocate Role

**Action:** Explicitly adopt the Devil's Advocate role with a clear mandate to argue against the deliverable's positions.

**Procedure:**
1. Read the deliverable in full, noting its central thesis, key claims, and recommendations
2. Read the S-003 Steelman output to understand how the deliverable was strengthened (H-16 compliance check: if no S-003 output exists, STOP and flag H-16 violation)
3. Adopt the adversarial mindset: your goal is to find the strongest possible reasons why the deliverable is wrong, incomplete, or flawed
4. Document the role assumption: state the deliverable being challenged, the scope of the critique, and the criticality level

**Decision Point:**
- If S-003 Steelman output is missing: STOP. Flag H-16 violation. Do not proceed until S-003 is applied.
- If S-003 output exists: Proceed to Step 2.

**Output:** Role assumption statement with deliverable ID, criticality level, and H-16 compliance confirmation.

### Step 2: Document and Challenge Assumptions

**Action:** Extract all explicit and implicit assumptions from the deliverable, then challenge each one.

**Procedure:**
1. Identify **explicit assumptions** stated in the deliverable (e.g., "We assume Redis can handle 10K requests/second")
2. Identify **implicit assumptions** not stated but relied upon (e.g., the deliverable assumes the team has Redis operational expertise)
3. For each assumption, ask:
   - What if this assumption is wrong?
   - What evidence supports this assumption? Is it sufficient?
   - Under what conditions would this assumption fail?
   - What are the consequences if this assumption fails?
4. Document each challenged assumption with its counter-position

**Decision Point:**
- If zero assumptions identified: the deliverable may lack explicit reasoning. Flag as a Completeness concern and proceed with claim-level analysis in Step 3.
- If 5+ assumptions identified: prioritize by impact (which failures would be most damaging?) before proceeding.

**Output:** Assumption inventory with challenge notes, prioritized by failure impact.

### Step 3: Construct Counter-Arguments

**Action:** For each significant claim, decision, or recommendation in the deliverable, construct the strongest possible counter-argument.

**Procedure:**
For each claim or decision in the deliverable:

1. **Identify the claim:** Quote or paraphrase the specific position being challenged
2. **Apply the 6 counter-argument lenses:**
   1. **Logical flaws:** Does the argument contain fallacies, non sequiturs, or circular reasoning?
   2. **Unstated assumptions:** What must be true for this claim to hold? Are those conditions guaranteed?
   3. **Contradicting evidence:** Is there evidence (from the deliverable itself or domain knowledge) that contradicts this claim?
   4. **Alternative interpretations:** Could the same evidence support a different conclusion?
   5. **Unaddressed risks:** What could go wrong that the deliverable does not consider?
   6. **Historical precedents of failure:** Have similar approaches failed before? Under what conditions?
3. **Construct the counter-argument:** State the strongest possible case against the claim
4. **Assign severity:**
   - **Critical:** Counter-argument invalidates a core claim or reveals a HARD rule violation. Blocks acceptance.
   - **Major:** Counter-argument reveals a significant gap, unstated risk, or weak justification. Requires revision.
   - **Minor:** Counter-argument identifies an improvement opportunity or minor weakness. Does not block acceptance.
5. **Map to affected dimension:** Identify which of the 6 scoring dimensions the finding impacts
6. **Assign finding identifier:** Use DA-NNN prefix (DA-001, DA-002, etc.)

**Decision Point:**
- If fewer than 3 counter-arguments generated: apply leniency bias counteraction. Force deeper analysis. Even strong deliverables have weaknesses; the advocate role requires finding them.
- If Critical counter-arguments found: the deliverable has fundamental issues requiring substantial revision.

**Output:** Findings table with DA-NNN identifiers, severity, evidence, and affected dimensions.

**Finding Documentation Format:** Use the Findings Table format from [Output Format: Findings Table](#3-findings-table) with DA-NNN identifiers and severity per definitions above.

### Step 4: Require Substantive Responses

**Action:** For each Critical and Major finding, specify what constitutes a substantive response from the creator.

**Procedure:**
1. For each Critical and Major finding:
   - State what the creator must demonstrate to resolve the finding
   - Define acceptance criteria: what evidence, analysis, or revision would satisfy the counter-argument?
   - Specify whether the finding requires content revision, additional evidence, explicit acknowledgment of the risk, or fundamental rethinking
2. For Minor findings:
   - State the improvement opportunity
   - Note that acknowledgment (with or without revision) is sufficient
3. Prioritize response requirements:
   - **P0:** Critical findings -- MUST be resolved before acceptance
   - **P1:** Major findings -- SHOULD be resolved; require justification if not
   - **P2:** Minor findings -- MAY be resolved; acknowledgment sufficient

**Decision Point:**
- If P0 findings exist: deliverable MUST be revised before proceeding to S-014 scoring
- If only P1/P2 findings: deliverable may proceed to S-014 scoring with documented responses

**Output:** Response requirements table with acceptance criteria for each Critical and Major finding.

### Step 5: Synthesize and Score Impact

**Action:** Produce a consolidated assessment of the Devil's Advocate findings and their impact on quality dimensions.

**Procedure:**
1. Aggregate findings by severity: count Critical, Major, and Minor
2. Map findings to the 6 scoring dimensions and assess net impact (Positive/Negative/Neutral) per dimension
3. Estimate composite score impact: Critical findings typically reduce affected dimensions by 0.10-0.20; Major by 0.05-0.10; Minor by 0.01-0.03
4. Determine overall assessment: major revision required (arguments undermine deliverable), targeted revision (addressable gaps), or proceed with minor revisions (deliverable withstands scrutiny)
5. Document the synthesis in the Scoring Impact table

**Output:** Scoring Impact table, overall assessment, and revision guidance.

---

## Output Format

Every S-002 execution MUST produce a Devil's Advocate report with these sections:

### 1. Header

```markdown
# Devil's Advocate Report: {{DELIVERABLE_NAME}}

**Strategy:** S-002 Devil's Advocate
**Deliverable:** {{Artifact name, file path, or work item ID}}
**Criticality:** {{C2/C3/C4}}
**Date:** {{ISO 8601 date}}
**Reviewer:** {{Agent ID or human name}}
**H-16 Compliance:** S-003 Steelman applied on {{date}} (confirmed)
```

### 2. Summary

2-3 sentence overall assessment covering: number and severity of counter-arguments, overall deliverable resilience, and recommendation (ACCEPT with revisions / REVISE / REJECT).

_Example: "6 counter-arguments identified (1 Critical, 3 Major, 2 Minor). The deliverable's core decision is sound but relies on an unstated scalability assumption (DA-001, Critical) that could invalidate the approach. Recommend REVISE to address Critical and Major findings."_

### 3. Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-{execution_id} | {{Counter-argument}} | Critical | {{Quote or reference from deliverable}} | {{Dimension}} |
| DA-002-{execution_id} | {{Counter-argument}} | Major | {{Quote or reference from deliverable}} | {{Dimension}} |

**Finding ID Format:** `DA-{NNN}-{execution_id}` where execution_id is a short timestamp or session identifier (e.g., `DA-001-20260215T1430`) to prevent ID collisions across tournament executions.

Severity definitions: see [Step 3: Construct Counter-Arguments](#step-3-construct-counter-arguments).

### 4. Finding Details

Expanded description for each Critical and Major finding:

```markdown
### DA-001: {{Finding Title}} [CRITICAL]

**Claim Challenged:** {{Quote the specific claim or decision from the deliverable}}
**Counter-Argument:** {{The strongest case against this claim}}
**Evidence:** {{Specific references, contradicting data, or logical analysis}}
**Impact:** {{What happens if this counter-argument is valid}}
**Dimension:** {{Affected scoring dimension}}
**Response Required:** {{What the creator must demonstrate to resolve this finding}}
**Acceptance Criteria:** {{Specific criteria that would satisfy this counter-argument}}
```

### 5. Recommendations

Prioritized action list grouped by: **P0** (Critical -- MUST resolve before acceptance), **P1** (Major -- SHOULD resolve; require justification if not), **P2** (Minor -- MAY resolve; acknowledgment sufficient). Each entry: DA-NNN identifier, specific action, and acceptance criteria.

### 6. Scoring Impact

Map Devil's Advocate findings to S-014 scoring dimensions (Completeness 0.20, Internal Consistency 0.20, Methodological Rigor 0.20, Evidence Quality 0.15, Actionability 0.15, Traceability 0.10). For each dimension, assess Impact (Positive/Negative/Neutral) with rationale referencing specific DA-NNN findings. See [Example Scoring Impact](#example-1-c2-architecture-decision----event-sourcing-adoption) for a completed table.

### Evidence Requirements

Each finding MUST include: specific reference to the location in the deliverable (section, line, heading), quotation or paraphrase of the challenged content, and explanation of why the counter-argument is valid.

---

## Scoring Rubric

This rubric evaluates the **quality of the S-002 Devil's Advocate execution itself** (meta-evaluation), not the deliverable being reviewed.

### Threshold Bands

**SSOT threshold (from quality-enforcement.md, MUST NOT be redefined):** >= 0.92 weighted composite score. Below threshold = REJECTED; revision required per H-13.

**Operational bands for S-002 execution quality:**

| Band | Score Range | Outcome |
|------|------------|---------|
| PASS | >= 0.92 | Strategy execution accepted; counter-arguments are rigorous and evidence-based |
| REVISE | 0.85 - 0.91 | Strategy execution requires targeted revision; close to threshold |
| REJECTED | < 0.85 | Strategy execution inadequate; significant rework required (H-13) |

> **Note:** The SSOT defines only the 0.92 threshold with REJECTED as the below-threshold outcome. The REVISE band (0.85-0.91) is a template-specific operational category (not sourced from quality-enforcement.md) to distinguish near-threshold executions requiring targeted improvements from those requiring significant rework. Both REVISE and REJECTED trigger the revision cycle per H-13.

### Dimension Weights

From quality-enforcement.md (MUST NOT be redefined):

| Dimension | Weight | Measures (for S-002 execution quality) |
|-----------|--------|----------------------------------------|
| Completeness | 0.20 | All claims examined; all assumptions extracted; minimum 3 counter-arguments |
| Internal Consistency | 0.20 | No contradictory findings; severity consistent with evidence; no self-defeating arguments |
| Methodological Rigor | 0.20 | All 5 steps executed; H-16 verified; counter-argument lenses applied systematically |
| Evidence Quality | 0.15 | Each counter-argument backed by specific deliverable references and logical analysis |
| Actionability | 0.15 | Response requirements concrete; acceptance criteria specific and verifiable |
| Traceability | 0.10 | Findings linked to deliverable claims; dimensions mapped; H-16 compliance documented |

### Strategy-Specific Rubric

| Dimension (Weight) | 0.95+ | 0.90-0.94 | 0.85-0.89 | <0.85 |
|--------------------|-------|-----------|-----------|-------|
| **Completeness (0.20)** | ALL claims and assumptions examined; 5+ counter-arguments; all 6 lenses applied per claim; no deliverable section unexamined | Most claims examined; 3-4 counter-arguments; most lenses applied; minor coverage gaps | Key claims examined; 2-3 counter-arguments; some lenses applied; notable coverage gaps | Few claims examined; <2 counter-arguments; lenses not systematically applied; major sections unexamined |
| **Internal Consistency (0.20)** | Zero contradictions; severity rigorously justified by evidence; counter-arguments do not contradict each other | No contradictions; severity mostly justified; minor alignment gaps between findings | One minor inconsistency; severity broadly reasonable; some counter-arguments overlap without acknowledgment | Multiple contradictions; severity arbitrary; counter-arguments self-defeating or redundant |
| **Methodological Rigor (0.20)** | ALL 5 steps executed in order; H-16 verified with evidence; all 6 counter-argument lenses applied; leniency bias counteracted (minimum 3 findings) | All 5 steps executed; H-16 verified; most lenses applied; leniency bias addressed | 4 steps executed; H-16 noted but not verified; some lenses applied; limited leniency counteraction | <4 steps executed; H-16 not checked; counter-arguments ad hoc; no systematic method |
| **Evidence Quality (0.15)** | Every counter-argument quotes deliverable content and provides logical analysis; counter-arguments are credible and domain-informed | Most counter-arguments have specific evidence; logical analysis present; minor vagueness | Some counter-arguments have evidence; others rely on general assertions; logical analysis incomplete | Counter-arguments lack evidence; vague assertions dominate; not credible |
| **Actionability (0.15)** | ALL P0/P1 findings have specific response requirements and verifiable acceptance criteria; creator can act without guessing | Most findings have specific response requirements; acceptance criteria present for Critical findings | Some response requirements present; acceptance criteria vague; creator must interpret | No response requirements; findings are observations without actionable guidance |
| **Traceability (0.10)** | Every finding traces to specific deliverable claim (with quote); all findings mapped to dimensions; H-16 compliance documented with S-003 reference | Most findings traceable; dimension mapping present; H-16 documented | Some findings traceable; dimension mapping partial; H-16 mentioned | Findings not traceable; no dimension mapping; H-16 status unknown |

---

## Examples

### Example 1: C2 Architecture Decision -- Event Sourcing Adoption

**Context:** A developer proposed adopting event sourcing for the Jerry work item aggregate (C2 Standard: reversible in 1 day, affects 6 files). S-003 Steelman was applied first (H-16 compliance). Devil's Advocate now critiques the strengthened proposal.

#### Before (Key Claims from ADR after S-003 Steelman)

ADR-PROJ001-007 proposes event sourcing for the WorkItem aggregate. Key claims: (1) "storing domain events as the primary source of truth," (2) "WorkItem has clear state transitions (Created -> InProgress -> Done) that map naturally to domain events," (3) benefits include "complete audit trail" and "natural fit with existing CQRS," (4) acknowledged trade-off: "additional complexity in event store implementation."

#### Strategy Execution

**Step 1: Assume the Advocate Role**
- Deliverable: ADR-PROJ001-007 (Event Sourcing for WorkItem)
- Criticality: C2 Standard
- H-16 compliance: S-003 Steelman applied 2026-02-15 (confirmed; Steelman strengthened rationale and added consequences section)
- Role assumed: Argue against event sourcing adoption for WorkItem aggregate

**Step 2: Document and Challenge Assumptions**
- Explicit assumption: "WorkItem has clear state transitions" -- What if transitions become complex with sub-states or parallel workflows?
- Implicit assumption: Team has event sourcing operational experience -- No evidence of prior event sourcing implementations
- Implicit assumption: Read model projections will be simple -- Complexity scales with query variety
- Implicit assumption: Event schema will remain stable -- No versioning strategy documented

**Step 3: Construct Counter-Arguments**

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-20260215T1515 | No event schema versioning strategy | Major | ADR mentions "storing domain events" but does not address event schema evolution. When event shapes change (e.g., adding fields to WorkItemCreated), existing events become incompatible without an explicit upcasting or versioning strategy. | Completeness |
| DA-002-20260215T1515 | Operational complexity understated | Major | "Additional complexity in event store implementation" is acknowledged but not quantified. Event sourcing requires: event store, snapshot strategy, read model projection, eventual consistency handling, and replay tooling. This is a 5x complexity multiplier over simple CRUD, not a minor addition. | Evidence Quality |
| DA-003-20260215T1515 | "Clear state transitions" assumption is fragile | Major | ADR states "Created -> InProgress -> Done" but WorkItem domain model may evolve to include Blocked, InReview, Cancelled, or parallel sub-item states. Event sourcing with complex state machines requires saga/process manager patterns not addressed in the ADR. | Methodological Rigor |
| DA-004-20260215T1515 | No rollback or migration path defined | Minor | If event sourcing proves too complex, no strategy exists for reverting to a simpler persistence model. C2 classification assumes reversibility in 1 day, but event store migration is not a 1-day operation. | Actionability |
| DA-005-20260215T1515 | Audit trail benefit overstated for current scope | Minor | "Complete audit trail" is listed as a primary benefit, but Jerry's current WorkItem aggregate is used by a single developer in a CLI tool. The audit trail benefit is relevant for multi-user systems, not the current single-user scope. | Evidence Quality |

**Step 4: Require Substantive Responses**

**P1 (Major -- SHOULD resolve):**
- DA-001: Add an "Event Versioning Strategy" section documenting how schema changes will be handled (upcasting, weak schema, or versioned events). Acceptance criteria: strategy must handle at least one concrete example of event shape change.
- DA-002: Quantify the implementation complexity by listing all required components (event store, snapshots, projections, etc.) with estimated effort. Acceptance criteria: effort estimate per component with total hours.
- DA-003: Document which state transitions are supported in v1 and explicitly defer complex transitions (Blocked, parallel sub-items) with a decision on when to revisit. Acceptance criteria: explicit scope boundary for v1.

**P2 (Minor -- MAY resolve):**
- DA-004: Add a "Reversibility" section noting the migration path if event sourcing is abandoned. Acknowledgment sufficient.
- DA-005: Clarify whether audit trail is a current need or future-proofing. Acknowledgment sufficient.

**Step 5: Synthesize and Score Impact**

#### After (ADR Revised Based on DA Findings)

The creator addressed findings by adding:
- Event Versioning Strategy section with upcasting example (resolves DA-001)
- Implementation Complexity breakdown with 5 components and effort estimates (resolves DA-002)
- Explicit v1 scope boundary: "Created -> InProgress -> Done only; Blocked and parallel states deferred to ADR-PROJ001-008" (resolves DA-003)
- Reversibility note: "Event store can be migrated to CRUD by replaying to final state" (resolves DA-004)
- Acknowledged DA-005: "Audit trail is future-proofing for multi-user support planned in FEAT-015"

**Scoring Impact:**

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-001: Missing event versioning strategy leaves a significant gap |
| Internal Consistency | 0.20 | Neutral | No contradictions detected in the deliverable |
| Methodological Rigor | 0.20 | Negative | DA-003: Fragile assumption about state transition simplicity undermines design rigor |
| Evidence Quality | 0.15 | Negative | DA-002, DA-005: Complexity understated and audit benefit overstated without evidence |
| Actionability | 0.15 | Negative | DA-004: No rollback path defined for a supposedly reversible (C2) decision |
| Traceability | 0.10 | Neutral | ADR traces to CQRS architecture decision and domain model |

**Result:** 3 Major and 2 Minor findings identified. After revision addressing all Major findings, the ADR's quality improved across 4 of 6 dimensions (Completeness, Methodological Rigor, Evidence Quality, and Actionability), moving the deliverable closer to the 0.92 threshold.

---

## Integration

### Canonical Pairings

See [Pairing Recommendations](#pairing-recommendations) for the full pairing table (S-003, S-014, S-007, S-004) with rationale and optimal sequence.

### H-16 Compliance

**H-16 Rule:** Steelman before critique. S-003 MUST execute before S-002. Full ordering constraints, compliant/non-compliant orderings, and recommended sequences are documented in [Prerequisites: Ordering Constraints](#ordering-constraints) and [Purpose: Pairing Recommendations](#pairing-recommendations).

### Criticality-Based Selection Table

From quality-enforcement.md (MUST NOT modify):

| Level | Required Strategies | Optional Strategies | S-002 Status |
|-------|---------------------|---------------------|--------------|
| C1 | S-010 | S-003, S-014 | OPTIONAL |
| C2 | S-007, S-002, S-014 | S-003, S-010 | **REQUIRED** |
| C3 | C2 + S-004, S-012, S-013 | S-001, S-003, S-010, S-011 | **REQUIRED** |
| C4 | All 10 selected | None | **REQUIRED** |

**Source:** quality-enforcement.md Criticality Levels table (SSOT). Values MUST match exactly. See [Criticality Tier Table](#criticality-tier-table) for S-002-specific usage notes per level.

### Cross-References

**SSOT and Source Documents:**
- `.context/rules/quality-enforcement.md` -- Authoritative source for H-13 threshold, dimension weights, criticality levels, strategy catalog
- `ADR-EPIC002-001` -- Strategy selection methodology, composite score 4.10, exclusion rationale
- `ADR-EPIC002-002` -- 5-layer enforcement architecture, token budgets
- `.context/templates/adversarial/TEMPLATE-FORMAT.md` -- Canonical format this template conforms to (v1.1.0)

**Related Strategy Templates:**
- `s-003-steelman.md` -- MUST run before S-002 (H-16 compliance)
- `s-007-constitutional-ai.md` -- Complementary: rule compliance check before logical critique
- `s-014-llm-as-judge.md` -- Scoring mechanism for post-S-002 revised deliverables
- `s-010-self-refine.md` -- Optional self-review before or after S-002
- `s-004-pre-mortem.md` -- Complementary Role-Based Adversarialism (future failure vs. current flaw)
- `s-001-red-team.md` -- Complementary Role-Based Adversarialism (systematic attack scenarios)

**Academic Sources:** See file header comment for Nemeth (2018), Janis (1982), Schwenk (1984), CIA Tradecraft Primer (2009).

**HARD Rules Referenced:** H-13 (threshold), H-14 (creator-critic cycle), H-15 (self-review), H-16 (steelman before critique), H-17 (quality scoring). See `quality-enforcement.md` for definitions.

---

<!-- VALIDATION CHECKLIST (per TEMPLATE-FORMAT.md):
- [x] All 8 canonical sections present in order (Identity, Purpose, Prerequisites, Execution Protocol, Output Format, Scoring Rubric, Examples, Integration)
- [x] H-23: Navigation table present
- [x] H-24: Navigation table uses anchor links
- [x] Metadata blockquote header present
- [x] File length under 500 lines (TEMPLATE-FORMAT.md structural limit)
- [x] Identity: 7 required fields + criticality tier table; values match SSOT
- [x] Purpose: 5 "When to Use", 3 "When NOT to Use", measurable outcome, pairing recommendations with H-16
- [x] Prerequisites: Input checklist (5 items), context requirements, ordering constraints (H-16 MANDATORY)
- [x] Execution Protocol: 5 steps with step format, decision points, DA-NNN finding prefix, severity definitions
- [x] Output Format: 6 output sections, scoring impact table with correct weights (0.20/0.20/0.20/0.15/0.15/0.10), evidence requirements
- [x] Scoring Rubric: Threshold bands match SSOT (>=0.92), REVISE note included, weights match SSOT, strategy-specific 4-band rubric for all 6 dimensions
- [x] Examples: 1 C2 example with Before/After, findings with DA-NNN identifiers (DA-001 through DA-005), 3 Major findings
- [x] Integration: Pairings, H-16 compliance explicitly documented, criticality table matches SSOT, cross-references
- [x] H-16 referenced in: Purpose (Pairing Recommendations), Prerequisites (Ordering Constraints), Execution Protocol (Step 1), Integration (H-16 Compliance)
- [x] Finding prefix DA-NNN used consistently throughout
- [x] No absolute paths; all references use relative paths
-->

<!-- VERSION: 1.0.0 | CREATED: 2026-02-15 | ENABLER: EN-806 | FORMAT: TEMPLATE-FORMAT.md v1.1.0 -->
