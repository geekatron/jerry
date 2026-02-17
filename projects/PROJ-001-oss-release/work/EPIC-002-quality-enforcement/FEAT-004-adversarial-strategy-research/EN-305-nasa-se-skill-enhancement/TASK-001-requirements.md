# TASK-001: Requirements for NSE Skill Adversarial Enhancements

<!--
DOCUMENT-ID: FEAT-004:EN-305:TASK-001
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
> **Purpose:** Define formal requirements for integrating adversarial strategies into the /nasa-se skill agents (nse-verification, nse-reviewer, nse-qa) and SE review gates

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this requirements document defines |
| [Functional Requirements: nse-verification](#functional-requirements-nse-verification) | Adversarial capabilities for V&V |
| [Functional Requirements: nse-reviewer](#functional-requirements-nse-reviewer) | Adversarial capabilities for technical reviews |
| [Functional Requirements: nse-qa](#functional-requirements-nse-qa) | Adversarial capabilities for QA |
| [Functional Requirements: Review Gate Mapping](#functional-requirements-review-gate-mapping) | Strategy-to-gate requirements |
| [Functional Requirements: Enforcement Integration](#functional-requirements-enforcement-integration) | Hook and enforcement layer integration |
| [Non-Functional Requirements](#non-functional-requirements) | Quality, performance, compatibility constraints |
| [Backward Compatibility Requirements](#backward-compatibility-requirements) | Existing capability preservation |
| [Traceability](#traceability) | Mapping to EN-302, EN-303, barrier-2 handoff |
| [References](#references) | Source citations |

---

## Summary

This document defines 50 formal requirements: 35 functional (FR-305-001 through FR-305-035), 10 non-functional (NFR-305-001 through NFR-305-010), and 5 backward compatibility (BC-305-001 through BC-305-005) for enhancing the /nasa-se skill with adversarial strategy integration. The requirements are derived from three authoritative sources:

1. **ADR-EPIC002-001** (ACCEPTED): The 10 selected adversarial strategies (S-001 through S-014) and their quality layer composition (L0-L4).
2. **EN-303 TASK-001/TASK-003**: The 8-dimension context taxonomy, per-strategy applicability profiles, and decision criticality mapping (C1-C4).
3. **Barrier-2 ENF-to-ADV handoff**: Hook-based enforcement architecture (L2/L3), rule-based enforcement (L1), and adversarial strategy integration points for EN-305.

The requirements target three NSE agents: nse-verification (V&V specialist), nse-reviewer (technical review gate), and nse-qa (quality assurance specialist). Each agent receives adversarial modes mapped to specific SE review gates (SRR, PDR, CDR, TRR, FRR).

---

## Functional Requirements: nse-verification

### Adversarial V&V Capabilities

| ID | Requirement | Priority | Verification Method | Traces To |
|----|-------------|----------|-------------------|-----------|
| FR-305-001 | nse-verification SHALL support an `adversarial-challenge` mode that applies S-013 (Inversion) to generate anti-requirement checklists from the requirements baseline before verification planning. | HARD | Inspection of agent spec | EN-303 TASK-003 S-013 profile (TGT-REQ: High affinity) |
| FR-305-002 | nse-verification SHALL support an `adversarial-verification` mode that applies S-011 (CoVe) to independently verify factual claims in verification evidence before accepting PASS status. | HARD | Test | EN-303 TASK-003 S-011 profile (PH-VALID: primary) |
| FR-305-003 | nse-verification SHALL support an `adversarial-scoring` mode that applies S-014 (LLM-as-Judge) to produce a 0.00-1.00 quality score on VCRM completeness, evidence quality, and coverage metrics. | HARD | Test | EN-303 TASK-003 S-014 profile (universal evaluation) |
| FR-305-004 | nse-verification SHALL support an `adversarial-compliance` mode that applies S-007 (Constitutional AI) to evaluate V&V artifacts against NPR 7123.1D Process 7/8 requirements and Jerry constitutional principles (P-040, P-041). | HARD | Inspection | EN-303 TASK-003 S-007 profile (TGT-CODE: High affinity) |
| FR-305-005 | nse-verification SHALL apply S-010 (Self-Refine) as a pre-step before any adversarial mode invocation, producing a self-corrected artifact before external critique. | MEDIUM | Inspection | EN-303 TASK-003 S-010 profile (always-on baseline) |
| FR-305-006 | nse-verification adversarial modes SHALL produce structured output including: finding ID, severity (CRITICAL/MAJOR/MINOR/INFO), evidence citation, remediation recommendation, and traceability to the requirement being verified. | HARD | Inspection | Barrier-2 handoff: EnforcementDecision dataclass pattern |
| FR-305-007 | nse-verification SHALL support criticality-based mode selection: C1 uses S-010 only; C2 adds S-007 + S-014; C3 adds S-013 + S-011; C4 activates all adversarial modes. | HARD | Test | EN-303 TASK-001 Dimension 3 (C1-C4 strategy allocation) |

### Review Gate Integration for nse-verification

| ID | Requirement | Priority | Verification Method | Traces To |
|----|-------------|----------|-------------------|-----------|
| FR-305-008 | nse-verification adversarial findings at TRR gate SHALL include: verification procedure completeness score, evidence quality score, and coverage gap enumeration with risk assessment. | HARD | Inspection | EN-305 enabler AC-2; SKILL.md TRR gate |
| FR-305-009 | nse-verification adversarial findings at CDR gate SHALL include: verification approach maturity assessment, procedure readiness score, and requirements-to-verification traceability completeness. | MEDIUM | Inspection | EN-305 enabler AC-4; SKILL.md CDR gate |

---

## Functional Requirements: nse-reviewer

### Adversarial Review Capabilities

| ID | Requirement | Priority | Verification Method | Traces To |
|----|-------------|----------|-------------------|-----------|
| FR-305-010 | nse-reviewer SHALL support an `adversarial-critique` mode that applies S-002 (Devil's Advocate) to challenge the rationale behind review readiness determinations (PASS/CONDITIONAL/FAIL). | HARD | Test | EN-303 TASK-003 S-002 profile (TGT-DEC: High affinity) |
| FR-305-011 | nse-reviewer SHALL support a `steelman-critique` mode that applies S-003 (Steelman) before S-002 (DA), ensuring the review readiness argument is reconstructed in its strongest form before adversarial challenge. | HARD | Inspection | EN-303 TASK-003 SYN pair #1: S-003 + S-002 canonical protocol |
| FR-305-012 | nse-reviewer SHALL support an `adversarial-premortem` mode that applies S-004 (Pre-Mortem) to imagine how the review could fail to catch critical issues, producing a failure cause inventory for review preparation. | HARD | Inspection | EN-303 TASK-003 S-004 profile (PH-DESIGN: primary) |
| FR-305-013 | nse-reviewer SHALL support an `adversarial-fmea` mode that applies S-012 (FMEA) to systematically enumerate failure modes in the review entrance criteria evaluation process. | MEDIUM | Test | EN-303 TASK-003 S-012 profile (TGT-PROC: High affinity) |
| FR-305-014 | nse-reviewer SHALL support an `adversarial-redteam` mode that applies S-001 (Red Team) to simulate an adversary attempting to pass a review gate with non-compliant artifacts. | MEDIUM | Inspection | EN-303 TASK-003 S-001 profile (TGT-ARCH: primary) |
| FR-305-015 | nse-reviewer SHALL apply S-014 (LLM-as-Judge) to produce a numerical quality score (0.00-1.00) on the overall review readiness assessment. | HARD | Test | EN-303 TASK-003 S-014 profile; Barrier-2 H-13 (>= 0.92 threshold) |
| FR-305-016 | nse-reviewer SHALL support criticality-based mode activation: C2 activates S-003 + S-002 + S-014; C3 adds S-004 + S-012 + S-013; C4 adds S-001 + S-011. | HARD | Test | EN-303 TASK-001 Dimension 3 (C1-C4 strategy allocation) |
| FR-305-017 | nse-reviewer adversarial modes SHALL produce findings in the existing RFA (Request for Action) / RFI (Request for Information) / Comment finding categories per NPR 7123.1D Appendix G. | HARD | Inspection | nse-reviewer.md `<nasa_methodology>` finding categories |

### Per-Gate Adversarial Requirements

| ID | Requirement | Priority | Verification Method | Traces To |
|----|-------------|----------|-------------------|-----------|
| FR-305-018 | At SRR gate, nse-reviewer SHALL apply S-013 (Inversion) to generate anti-requirements that test completeness of the requirements baseline. | HARD | Inspection | EN-303 TASK-003 S-013 (TGT-REQ: High affinity) |
| FR-305-019 | At PDR gate, nse-reviewer SHALL apply S-002 (DA) to challenge preliminary design decisions and S-004 (Pre-Mortem) to imagine design failure scenarios. | HARD | Inspection | EN-303 TASK-003 S-002 (TGT-ARCH), S-004 (PH-DESIGN) |
| FR-305-020 | At CDR gate, nse-reviewer SHALL apply S-007 (Constitutional AI) to evaluate detailed design against architecture standards and S-012 (FMEA) to enumerate design failure modes. | HARD | Inspection | EN-303 TASK-003 S-007 (TGT-CODE: High), S-012 (PH-DESIGN) |
| FR-305-021 | At TRR gate, nse-reviewer SHALL apply S-011 (CoVe) to verify test procedure claims and S-014 (Judge) to score test readiness. | HARD | Inspection | EN-303 TASK-003 S-011 (PH-VALID: primary), S-014 |
| FR-305-022 | At FRR gate, nse-reviewer SHALL activate all 10 adversarial strategies at C4 intensity, producing a comprehensive adversarial review package. | HARD | Inspection | EN-303 TASK-001 Dimension 3 (C4: all 10 strategies) |

---

## Functional Requirements: nse-qa

### Adversarial QA Capabilities

| ID | Requirement | Priority | Verification Method | Traces To |
|----|-------------|----------|-------------------|-----------|
| FR-305-023 | nse-qa SHALL support an `adversarial-audit` mode that applies S-007 (Constitutional AI) to evaluate SE artifacts against both NPR 7123.1D and Jerry constitutional principles simultaneously. | HARD | Inspection | EN-303 TASK-003 S-007 profile; nse-qa.md `<qa_checklists>` |
| FR-305-024 | nse-qa SHALL support an `adversarial-scoring` mode that applies S-014 (LLM-as-Judge) to produce compliance scores calibrated against the >= 0.92 quality gate threshold. | HARD | Test | Barrier-2 handoff H-13; EN-303 TASK-003 S-014 |
| FR-305-025 | nse-qa SHALL support an `adversarial-verification` mode that applies S-011 (CoVe) to verify factual claims and citations in QA audit reports themselves (meta-QA). | MEDIUM | Inspection | EN-303 TASK-003 S-011 (TGT-RES: High affinity) |

---

## Functional Requirements: Review Gate Mapping

| ID | Requirement | Priority | Verification Method | Traces To |
|----|-------------|----------|-------------------|-----------|
| FR-305-026 | The /nasa-se skill SHALL define a strategy-to-gate mapping table that specifies which adversarial strategies are applicable at each SE review gate (SRR, PDR, CDR, TRR, FRR) with applicability scores. | HARD | Inspection | EN-305 enabler AC-4 |
| FR-305-027 | The strategy-to-gate mapping SHALL include rationale for each strategy-gate combination, traceable to EN-303 TASK-003 per-strategy applicability profiles. | MEDIUM | Inspection | EN-303 TASK-003 decision criticality mapping |
| FR-305-028 | The strategy-to-gate mapping SHALL classify each strategy-gate combination as Required, Recommended, or Optional based on criticality level and review phase. | HARD | Inspection | EN-303 TASK-001 Dimension 3 |
| FR-305-029 | FRR (Flight/Final Readiness Review) SHALL be classified as C4 criticality, requiring activation of all 10 adversarial strategies. | HARD | Inspection | EN-303 TASK-001 (C4 = all 10 strategies) |

---

## Functional Requirements: Enforcement Integration

| ID | Requirement | Priority | Verification Method | Traces To |
|----|-------------|----------|-------------------|-----------|
| FR-305-030 | NSE adversarial modes SHALL consume the C1-C4 criticality assessment from the PromptReinforcementEngine to determine which strategies to activate. | MEDIUM | Inspection | Barrier-2 handoff: C1-C4 keyword matching in PromptReinforcementEngine |
| FR-305-031 | NSE adversarial findings SHALL be structured to integrate with the EnforcementDecision dataclass (action, reason, violations, criticality_escalation). | MEDIUM | Inspection | Barrier-2 handoff: EnforcementDecision API contract |
| FR-305-032 | NSE adversarial modes SHALL validate compliance against the 24 HARD rules (H-01 through H-24) when S-007 (Constitutional AI) is active. | HARD | Test | Barrier-2 handoff: HARD rule inventory |
| FR-305-033 | NSE adversarial modes SHALL use the 6 effective HARD language patterns (Constitutional Constraint, Forbidden/Required Binary, Layer Boundary Declaration, Quality Gate Declaration, Mandatory Skill Invocation, Escalation Trigger) in their finding reports. | MEDIUM | Inspection | Barrier-2 handoff: 6 effective patterns |
| FR-305-034 | NSE adversarial modes SHALL apply governance file escalation (C3/C4 criticality) when reviewing artifacts that modify `.claude/rules/`, `JERRY_CONSTITUTION.md`, or `CLAUDE.md`. | HARD | Test | Barrier-2 handoff: PreToolEnforcementEngine governance escalation |
| FR-305-035 | NSE adversarial mode output SHALL be consumable by the quality-enforcement.md SSOT file for shared enforcement constants (0.92 threshold, C1-C4 definitions, strategy encodings). | MEDIUM | Inspection | Barrier-2 handoff: quality-enforcement.md SSOT |

---

## Non-Functional Requirements

| ID | Requirement | Priority | Verification Method | Traces To |
|----|-------------|----------|-------------------|-----------|
| NFR-305-001 | Adversarial mode invocation SHALL NOT increase the token cost of a standard (non-adversarial) NSE agent invocation. Adversarial modes are additive and opt-in. | HARD | Test | Backward compatibility |
| NFR-305-002 | Each adversarial mode SHALL document its token cost per invocation, using the token tiers from ADR-EPIC002-001 (Ultra-Low: 1,600-2,100; Low: 4,600-5,600; Medium: 6,000-16,000). | MEDIUM | Inspection | EN-303 TASK-003 token budget per strategy |
| NFR-305-003 | Adversarial modes SHALL be deliverable via the portable enforcement stack (L1 + L5 + Process) without requiring Claude Code hooks. | HARD | Test | Barrier-2 handoff: Graceful Degradation Matrix; EN-303 TASK-003 platform portability |
| NFR-305-004 | Adversarial modes SHALL respect the token budget state dimension (TOK-FULL, TOK-CONST, TOK-EXHAUST) and degrade gracefully under constrained budgets per EN-303 TASK-003 token guidance. | MEDIUM | Test | EN-303 TASK-001 Dimension 8 |
| NFR-305-005 | All adversarial mode outputs SHALL include the P-043 mandatory disclaimer. | HARD | Inspection | nse-verification.md, nse-reviewer.md, nse-qa.md P-043 requirement |
| NFR-305-006 | Adversarial modes SHALL comply with P-003 (No Recursive Subagents) by operating within the orchestrator-worker pattern. | HARD | Architecture test | ADR-EPIC002-001 P-003 compliance table |
| NFR-305-007 | Adversarial mode configurations SHALL be defined at the specification level (markdown agent specs) and NOT require Python code changes for Phase 3 scope. | HARD | Inspection | EN-305 enabler scope |
| NFR-305-008 | Adversarial mode findings SHALL use the existing NSE session context schema (v1.0.0) for agent handoff, extending `key_findings` with adversarial-specific fields. | MEDIUM | Inspection | nse-verification.md `<session_context_validation>` |
| NFR-305-009 | The quality score produced by S-014 (LLM-as-Judge) in NSE agents SHALL use the same rubric dimensions and >= 0.92 threshold as the Jerry quality framework. | HARD | Test | Barrier-2 handoff H-13, H-15 |
| NFR-305-010 | Adversarial enhancements SHALL be documented with navigation tables and anchor links per the markdown navigation standard (NAV-001 through NAV-006). | MEDIUM | Inspection | `.context/rules/markdown-navigation-standards.md` |

---

## Backward Compatibility Requirements

| ID | Requirement | Priority | Rationale |
|----|-------------|----------|-----------|
| BC-305-001 | Existing nse-verification invocations without adversarial mode flags SHALL produce identical output to the current v2.1.0 behavior. | HARD | Zero regression on existing workflows |
| BC-305-002 | Existing nse-reviewer invocations without adversarial mode flags SHALL produce identical output to the current v2.2.0 behavior. | HARD | Zero regression on existing workflows |
| BC-305-003 | Existing nse-qa invocations without adversarial mode flags SHALL produce identical output to the current v2.1.0 behavior. | HARD | Zero regression on existing workflows |
| BC-305-004 | The existing YAML frontmatter, `<agent>` tags, and session context schema in NSE agent specs SHALL be preserved. New adversarial sections SHALL be additive. | HARD | Schema backward compatibility |
| BC-305-005 | The existing L0/L1/L2 output level structure SHALL be preserved. Adversarial findings SHALL be integrated into the existing output levels, not added as separate levels. | MEDIUM | Output format consistency |

---

## Traceability

### To EN-302 (Strategy Selection)

| EN-302 Artifact | EN-305 Requirement | Relationship |
|-----------------|-------------------|--------------|
| ADR-EPIC002-001: 10 selected strategies | FR-305-001 through FR-305-025 | Each functional requirement maps to one or more of the 10 strategies |
| ADR-EPIC002-001: P-003 compliance table | NFR-305-006 | All adversarial modes comply with P-003 |
| ADR-EPIC002-001: Token budget tiers | NFR-305-002 | Token costs documented per tier |

### To EN-303 (Situational Applicability)

| EN-303 Artifact | EN-305 Requirement | Relationship |
|-----------------|-------------------|--------------|
| TASK-001: C1-C4 criticality levels | FR-305-007, FR-305-016 | Criticality-based mode activation |
| TASK-001: Token Budget State (D8) | NFR-305-004 | Graceful degradation under budget constraints |
| TASK-003: Per-strategy profiles | FR-305-001 through FR-305-025 | Strategy affinity and when-to-use guidance |
| TASK-003: SYN pair #1 (S-003 + S-002) | FR-305-011 | Steelman-then-DA canonical protocol |

### To Barrier-2 ENF-to-ADV Handoff

| Barrier-2 Section | EN-305 Requirement | Relationship |
|-------------------|-------------------|--------------|
| EN-305 Integration Points | FR-305-030 through FR-305-035 | Enforcement layer integration |
| PreToolEnforcementEngine API | FR-305-031 | EnforcementDecision integration |
| 24 HARD rules (H-01 through H-24) | FR-305-032 | Constitutional AI validates against HARD rules |
| 6 effective HARD language patterns | FR-305-033 | Finding reports use effective patterns |
| C1-C4 criticality assessment | FR-305-030 | Criticality drives mode selection |
| Governance file escalation | FR-305-034 | C3/C4 auto-escalation for governance files |

---

## References

| # | Citation | Sections Referenced |
|---|----------|-------------------|
| 1 | ADR-EPIC002-001 (ACCEPTED) -- FEAT-004:EN-302:TASK-005 | Strategy IDs, quality layers, P-003 compliance, token tiers |
| 2 | EN-303 TASK-001 -- FEAT-004:EN-303:TASK-001 | 8-dimension context taxonomy, C1-C4 strategy allocation |
| 3 | EN-303 TASK-003 -- FEAT-004:EN-303:TASK-003 | Per-strategy applicability profiles, SYN/TEN pairs, enforcement layer mapping |
| 4 | Barrier-2 ENF-to-ADV Handoff -- EPIC002-CROSSPOLL-B2-ENF-TO-ADV | Hook API contracts, HARD rule inventory, enforcement capabilities, integration points |
| 5 | nse-verification agent spec -- `skills/nasa-se/agents/nse-verification.md` v2.1.0 | Current agent capabilities, session context schema |
| 6 | nse-reviewer agent spec -- `skills/nasa-se/agents/nse-reviewer.md` v2.2.0 | Current agent capabilities, review gate methodology |
| 7 | nse-qa agent spec -- `skills/nasa-se/agents/nse-qa.md` v2.1.0 | Current agent capabilities, QA checklists |
| 8 | NASA SE SKILL.md -- `skills/nasa-se/SKILL.md` v1.1.0 | Available agents, orchestration flow, review sequence |

---

*Document ID: FEAT-004:EN-305:TASK-001*
*Agent: nse-architecture-305*
*Created: 2026-02-13*
*Status: Complete*
