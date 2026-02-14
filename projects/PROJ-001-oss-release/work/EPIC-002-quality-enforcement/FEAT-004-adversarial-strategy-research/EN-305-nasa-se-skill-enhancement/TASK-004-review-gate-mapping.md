# TASK-004: Strategy-to-Review-Gate Mapping

<!--
DOCUMENT-ID: FEAT-004:EN-305:TASK-004
VERSION: 1.0.0
AGENT: nse-architecture-305
DATE: 2026-02-13
STATUS: Complete
PARENT: EN-305 (NASA SE Skill Enhancement)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
ACTIVITY: DESIGN
-->

> **Version:** 1.0.0
> **Agent:** nse-architecture-305
> **Quality Target:** >= 0.92
> **Purpose:** Map all 10 adversarial strategies to the 5 SE review gates (SRR, PDR, CDR, TRR, FRR) with applicability scores, classifications (Required/Recommended/Optional), and rationale traceable to EN-303

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this mapping delivers |
| [Mapping Methodology](#mapping-methodology) | How applicability was determined |
| [Master Strategy-to-Gate Mapping Table](#master-strategy-to-gate-mapping-table) | Complete 10x5 mapping matrix |
| [Per-Gate Detail: SRR](#per-gate-detail-srr) | Strategy application at System Requirements Review |
| [Per-Gate Detail: PDR](#per-gate-detail-pdr) | Strategy application at Preliminary Design Review |
| [Per-Gate Detail: CDR](#per-gate-detail-cdr) | Strategy application at Critical Design Review |
| [Per-Gate Detail: TRR](#per-gate-detail-trr) | Strategy application at Test Readiness Review |
| [Per-Gate Detail: FRR](#per-gate-detail-frr) | Strategy application at Flight/Final Readiness Review |
| [Criticality Overlay](#criticality-overlay) | How C1-C4 modifies the mapping |
| [Token Budget by Gate](#token-budget-by-gate) | Cumulative token costs per gate at each criticality |
| [Agent Responsibility Matrix](#agent-responsibility-matrix) | Which NSE agent executes each strategy at each gate |
| [Traceability](#traceability) | Mapping to TASK-001 requirements and EN-303 |
| [References](#references) | Source citations |

---

## Summary

This document provides the definitive mapping of all 10 adversarial strategies to the 5 NASA SE review gates (SRR, PDR, CDR, TRR, FRR). The mapping classifies each strategy-gate combination as Required, Recommended, or Optional based on the review gate's primary concerns, the strategy's affinity profile (EN-303 TASK-003), and the decision criticality framework (EN-303 TASK-001 Dimension 3).

The mapping satisfies requirements FR-305-026 through FR-305-029 from TASK-001.

---

## Mapping Methodology

Each strategy-gate combination is scored on a 3-level classification:

| Classification | Definition | Activation |
|---------------|-----------|-----------|
| **Required** | Strategy MUST be applied at this gate. Non-application constitutes a review gap. Corresponds to C2+ criticality for the gate's primary concern area. | Auto-activated at the gate's default criticality |
| **Recommended** | Strategy SHOULD be applied. Provides significant value but may be omitted under token budget constraints (TOK-CONST). | Auto-activated at C3+; manual activation at C2 |
| **Optional** | Strategy MAY be applied. Provides incremental value; justified only at elevated criticality or specific circumstances. | Manual activation only; auto-activated at C4 |

**Classification criteria (derived from EN-303 TASK-003):**
1. **Target Type Affinity:** Does the strategy have High affinity for the artifacts reviewed at this gate? (EN-303 TASK-001, Strategy Affinity by Target Type table)
2. **Phase Alignment:** Is the strategy's favorable phase (from its "When to Use" profile) aligned with the gate's lifecycle phase?
3. **Defect Coverage:** Does the strategy detect defect categories that are critical at this gate?

---

## Master Strategy-to-Gate Mapping Table

| Strategy | SRR | PDR | CDR | TRR | FRR |
|----------|-----|-----|-----|-----|-----|
| **S-014** LLM-as-Judge | Required | Required | Required | Required | Required |
| **S-003** Steelman | Recommended | Required | Required | Recommended | Required |
| **S-013** Inversion | **Required** | Recommended | Recommended | Optional | Required |
| **S-007** Constitutional AI | **Required** | Recommended | **Required** | Required | Required |
| **S-002** Devil's Advocate | Recommended | **Required** | Required | Recommended | Required |
| **S-004** Pre-Mortem | Optional | **Required** | Recommended | Optional | Required |
| **S-010** Self-Refine | Required | Required | Required | Required | Required |
| **S-012** FMEA | Optional | Recommended | **Required** | Recommended | Required |
| **S-011** CoVe | Optional | Optional | Optional | **Required** | Required |
| **S-001** Red Team | Optional | Optional | Recommended | Optional | Required |

**Legend:**
- **Bold** = Primary strategy for that gate (strongest alignment)
- Regular = Supporting strategy
- FRR = All Required (C4 intensity per FR-305-029)

---

## Per-Gate Detail: SRR

**System Requirements Review** | NPR 7123.1D Appendix G, Table G-4

**Primary Concern:** Requirements completeness, traceability to stakeholder needs, verification approach defined.

**Target Type:** TGT-REQ (requirements artifacts)

**Phase:** PH-DESIGN (requirements are being established)

**Default Criticality:** C2 (significant -- new system requirements)

| Strategy | Classification | Rationale | EN-303 Reference |
|----------|---------------|-----------|-------------------|
| S-014 LLM-as-Judge | Required | Score requirements baseline quality; universal evaluation at all gates | TASK-003 S-014: universal, C2 Required |
| S-013 Inversion | **Required** | Generate anti-requirements to test requirements completeness; TGT-REQ High affinity | TASK-003 S-013: TGT-REQ anti-pattern generation; TASK-001 TGT-REQ High affinity |
| S-007 Constitutional AI | **Required** | Evaluate requirements against NPR 7123.1D Process 2 and P-040 traceability | TASK-003 S-007: TGT-REQ High affinity; compliance evaluation |
| S-003 Steelman | Recommended | Reconstruct requirements rationale before adversarial challenge | TASK-003 S-003: C2 Recommended; SYN pair #1 enabler |
| S-002 Devil's Advocate | Recommended | Challenge requirements completeness argument after steelmanning | TASK-003 S-002: TGT-REQ Medium affinity; C2 Required but secondary at SRR |
| S-010 Self-Refine | Required | Baseline self-improvement for requirements artifacts | TASK-003 S-010: always-on at all levels |
| S-004 Pre-Mortem | Optional | Imagine requirements failure scenarios (valuable but secondary to S-013 at SRR) | TASK-003 S-004: PH-DESIGN favorable but not primary for requirements |
| S-012 FMEA | Optional | Enumerate requirement failure modes (secondary to S-013 at SRR) | TASK-003 S-012: TGT-REQ applicability but medium token cost |
| S-011 CoVe | Optional | Verify factual claims in requirements (valuable for empirical requirements) | TASK-003 S-011: TGT-REQ applicable but not primary |
| S-001 Red Team | Optional | Simulate adversary exploiting requirements gaps (only at C4) | TASK-003 S-001: TGT-REQ Low affinity; C4 only |

---

## Per-Gate Detail: PDR

**Preliminary Design Review** | NPR 7123.1D Appendix G, Table G-6

**Primary Concern:** Design viability, interface identification, SRR action items closed.

**Target Type:** TGT-ARCH (architecture/design artifacts)

**Phase:** PH-DESIGN (design phase)

**Default Criticality:** C2 (significant -- design decisions)

| Strategy | Classification | Rationale | EN-303 Reference |
|----------|---------------|-----------|-------------------|
| S-014 LLM-as-Judge | Required | Score PDR readiness | TASK-003 S-014: universal |
| S-002 Devil's Advocate | **Required** | Challenge preliminary design decisions and assumptions | TASK-003 S-002: TGT-ARCH High affinity; PH-DESIGN peak value |
| S-004 Pre-Mortem | **Required** | Imagine design failure scenarios; PH-DESIGN primary phase | TASK-003 S-004: TGT-ARCH favorable; PH-DESIGN primary |
| S-003 Steelman | Required | Steelman design rationale before DA challenge (SYN pair #1) | TASK-003 S-003: SYN pair #1 mandatory before S-002 |
| S-010 Self-Refine | Required | Baseline self-improvement | TASK-003 S-010: always-on |
| S-013 Inversion | Recommended | Generate design anti-patterns | TASK-003 S-013: TGT-ARCH High affinity; PH-DESIGN favorable |
| S-007 Constitutional AI | Recommended | Evaluate design against architecture standards | TASK-003 S-007: TGT-ARCH Medium affinity |
| S-012 FMEA | Recommended | Enumerate design failure modes | TASK-003 S-012: TGT-ARCH High affinity; PH-DESIGN favorable |
| S-011 CoVe | Optional | Verify factual claims in design rationale | TASK-003 S-011: TGT-ARCH Low affinity |
| S-001 Red Team | Optional | Simulate adversary exploiting design vulnerabilities (C3+ for security) | TASK-003 S-001: TGT-ARCH primary but C3+ only |

---

## Per-Gate Detail: CDR

**Critical Design Review** | NPR 7123.1D Appendix G, Table G-7

**Primary Concern:** Design completeness, TBD resolution, verification readiness, manufacturing/coding readiness.

**Target Type:** TGT-ARCH + TGT-CODE (detailed design transitioning to implementation)

**Phase:** PH-DESIGN transitioning to PH-IMPL

**Default Criticality:** C3 (major -- detailed design freeze)

| Strategy | Classification | Rationale | EN-303 Reference |
|----------|---------------|-----------|-------------------|
| S-014 LLM-as-Judge | Required | Score CDR readiness | TASK-003 S-014: universal |
| S-007 Constitutional AI | **Required** | Evaluate detailed design against architecture and coding standards | TASK-003 S-007: TGT-CODE High affinity; compliance at CDR critical |
| S-012 FMEA | **Required** | Systematically enumerate design failure modes before build | TASK-003 S-012: PH-DESIGN favorable; C3 Required |
| S-002 Devil's Advocate | Required | Challenge design completeness and readiness to build | TASK-003 S-002: C3 Required |
| S-003 Steelman | Required | Steelman before DA (SYN pair #1) | TASK-003 S-003: C3 Required |
| S-010 Self-Refine | Required | Baseline self-improvement | TASK-003 S-010: always-on |
| S-013 Inversion | Recommended | Generate design anti-patterns for build phase | TASK-003 S-013: C3 Required but secondary to S-012 at CDR |
| S-004 Pre-Mortem | Recommended | Imagine how the build could fail (transition to implementation) | TASK-003 S-004: C3 Required; PH-DESIGN primary |
| S-001 Red Team | Recommended | Simulate adversary exploiting detailed design (architecture reviews) | TASK-003 S-001: C3 Recommended for security/architecture |
| S-011 CoVe | Optional | Verify factual claims in design documentation | TASK-003 S-011: C3 Recommended; secondary at CDR |

---

## Per-Gate Detail: TRR

**Test Readiness Review** | NPR 7123.1D

**Primary Concern:** Test procedures ready, prerequisites complete, verification approach validated.

**Target Type:** TGT-REQ + TGT-CODE (verification artifacts)

**Phase:** PH-IMPL transitioning to PH-VALID

**Default Criticality:** C2 (significant -- test readiness)

| Strategy | Classification | Rationale | EN-303 Reference |
|----------|---------------|-----------|-------------------|
| S-014 LLM-as-Judge | Required | Score test readiness | TASK-003 S-014: universal |
| S-011 CoVe | **Required** | Verify factual claims in test procedures and evidence | TASK-003 S-011: PH-VALID primary; evidence verification |
| S-007 Constitutional AI | Required | Evaluate test artifacts against NPR 7123.1D Process 7 | TASK-003 S-007: PH-IMPL/VALID favorable |
| S-010 Self-Refine | Required | Baseline self-improvement | TASK-003 S-010: always-on |
| S-003 Steelman | Recommended | Steelman test readiness argument | TASK-003 S-003: C2 Recommended |
| S-002 Devil's Advocate | Recommended | Challenge test readiness determination | TASK-003 S-002: C2 Required but secondary at TRR to S-011 |
| S-012 FMEA | Recommended | Enumerate test process failure modes | TASK-003 S-012: TGT-PROC Medium affinity |
| S-004 Pre-Mortem | Optional | Imagine how testing could fail (limited value at TRR stage) | TASK-003 S-004: PH-IMPL/VALID cautionary |
| S-013 Inversion | Optional | Generate anti-test-criteria (limited value at validation phase) | TASK-003 S-013: PH-VALID cautionary per "When to Avoid" |
| S-001 Red Team | Optional | Simulate adversary bypassing test procedures (only at C4) | TASK-003 S-001: C4 only for testing |

---

## Per-Gate Detail: FRR

**Flight/Final Readiness Review** | NPR 7123.1D

**Primary Concern:** Complete readiness for flight/mission/release. Everything must be verified.

**Target Type:** All target types (comprehensive review)

**Phase:** PH-VALID (final validation)

**Default Criticality:** C4 (critical -- irreversible decision)

**Requirement:** FR-305-029 -- FRR SHALL be classified as C4 criticality, requiring activation of all 10 adversarial strategies.

| Strategy | Classification | Rationale |
|----------|---------------|-----------|
| S-014 LLM-as-Judge | Required | Final quality gate scoring |
| S-003 Steelman | Required | Fair evaluation of readiness argument |
| S-013 Inversion | Required | Comprehensive anti-pattern coverage |
| S-007 Constitutional AI | Required | Full compliance verification |
| S-002 Devil's Advocate | Required | Maximum adversarial challenge to readiness |
| S-004 Pre-Mortem | Required | Final failure imagination before commitment |
| S-010 Self-Refine | Required | Baseline self-improvement |
| S-012 FMEA | Required | Comprehensive failure mode enumeration |
| S-011 CoVe | Required | Verify all evidence claims |
| S-001 Red Team | Required | Adversary simulation against readiness package |

**Token Budget:** 35,000-55,000 tokens (C4 allocation per EN-303 TASK-001)

---

## Criticality Overlay

The master mapping table shows the default classification. Criticality level modifies the classification:

| Gate Default Criticality | Override to C3 | Override to C4 |
|-------------------------|---------------|---------------|
| SRR (C2 default) | All Recommended become Required; Optional become Recommended | All strategies Required |
| PDR (C2 default) | All Recommended become Required; Optional become Recommended | All strategies Required |
| CDR (C3 default) | Already at C3 | All strategies Required |
| TRR (C2 default) | All Recommended become Required; Optional become Recommended | All strategies Required |
| FRR (C4 default) | N/A (already C4) | Already all Required |

**Criticality escalation triggers (per EN-303 TASK-001):**
- Artifact modifies governance files -> Auto-C3+
- Artifact introduces new architectural pattern -> C3 minimum
- Artifact modifies security-relevant code -> C3 minimum
- Artifact modifies existing baselined ADR -> C4

---

## Token Budget by Gate

| Gate | C2 Required Tokens | C3 Required Tokens | C4 Required Tokens |
|------|-------------------|--------------------|-------------------|
| SRR | ~12,100 (S-014: 2K + S-013: 2.1K + S-007: 8K + S-010: 2K) | ~23,700 (+ S-003: 1.6K + S-002: 4.6K + S-004: 5.6K) | ~50,300 (all 10) |
| PDR | ~15,200 (S-014: 2K + S-002: 4.6K + S-004: 5.6K + S-003: 1.6K + S-010: 2K) | ~26,300 (+ S-013: 2.1K + S-007: 8K + S-012: 9K) | ~50,300 (all 10) |
| CDR | ~27,200 (S-014: 2K + S-007: 8K + S-012: 9K + S-002: 4.6K + S-003: 1.6K + S-010: 2K) | ~35,100 (+ S-013: 2.1K + S-004: 5.6K) | ~50,300 (all 10) |
| TRR | ~18,000 (S-014: 2K + S-011: 6K + S-007: 8K + S-010: 2K) | ~25,800 (+ S-003: 1.6K + S-002: 4.6K + S-012: 9K) | ~50,300 (all 10) |
| FRR | N/A (FRR is always C4) | N/A | ~50,300 (all 10) |

---

## Agent Responsibility Matrix

| Strategy | Primary Agent | Secondary Agent | Gate Context |
|----------|--------------|----------------|-------------|
| S-014 LLM-as-Judge | nse-reviewer (review scoring) | nse-verification (V&V scoring) | All gates |
| S-003 Steelman | nse-reviewer | -- | All gates (before S-002) |
| S-013 Inversion | nse-reviewer (review anti-patterns) | nse-verification (anti-requirements) | SRR (nse-verification); PDR-FRR (nse-reviewer) |
| S-007 Constitutional AI | nse-reviewer (review compliance) | nse-verification (V&V compliance), nse-qa (artifact compliance) | All gates |
| S-002 Devil's Advocate | nse-reviewer | -- | All gates (after S-003) |
| S-004 Pre-Mortem | nse-reviewer | -- | PDR, CDR, FRR |
| S-010 Self-Refine | nse-reviewer (self-review) | nse-verification (self-review) | All gates (pre-step) |
| S-012 FMEA | nse-reviewer (review FMEA) | nse-verification (V&V FMEA) | CDR, TRR, FRR |
| S-011 CoVe | nse-verification (evidence verification) | nse-reviewer (claim verification) | TRR, FRR |
| S-001 Red Team | nse-reviewer | -- | CDR (recommended), FRR (required) |

---

## Traceability

| TASK-001 Requirement | How Addressed |
|---------------------|--------------|
| FR-305-026 | Master mapping table defines strategy-to-gate mapping with applicability classifications |
| FR-305-027 | Per-gate detail sections include rationale traceable to EN-303 TASK-003 profiles |
| FR-305-028 | Each combination classified as Required/Recommended/Optional based on criticality and phase |
| FR-305-029 | FRR classified as C4 with all 10 strategies Required |

---

## References

| # | Citation | Sections Referenced |
|---|----------|-------------------|
| 1 | TASK-001 (Requirements) -- FEAT-004:EN-305:TASK-001 | FR-305-026 through FR-305-029 |
| 2 | ADR-EPIC002-001 (ACCEPTED) -- FEAT-004:EN-302:TASK-005 | 10 selected strategies, quality layers, token tiers |
| 3 | EN-303 TASK-001 -- FEAT-004:EN-303:TASK-001 | Strategy Affinity by Target Type table, Phase-Strategy Interaction Matrix, C1-C4 strategy allocation, token budget tiers |
| 4 | EN-303 TASK-003 -- FEAT-004:EN-303:TASK-003 | Per-strategy profiles: When to Use, When to Avoid, Decision Criticality Mapping, token costs |
| 5 | Barrier-2 ENF-to-ADV Handoff -- EPIC002-CROSSPOLL-B2-ENF-TO-ADV | Criticality assessment, enforcement layer mapping |
| 6 | nse-reviewer agent spec -- `skills/nasa-se/agents/nse-reviewer.md` v2.2.0 | Review gate methodology, NPR 7123.1D Appendix G tables |
| 7 | nse-verification agent spec -- `skills/nasa-se/agents/nse-verification.md` v2.1.0 | V&V methodology, VCRM process |

---

*Document ID: FEAT-004:EN-305:TASK-004*
*Agent: nse-architecture-305*
*Created: 2026-02-13*
*Status: Complete*
