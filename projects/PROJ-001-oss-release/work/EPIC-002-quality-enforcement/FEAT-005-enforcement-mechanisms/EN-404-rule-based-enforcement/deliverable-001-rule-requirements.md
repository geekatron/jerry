# TASK-001: Requirements for Rule-Based Enforcement

<!--
DOCUMENT-ID: FEAT-005:EN-404:TASK-001
TEMPLATE: Task
VERSION: 1.1.0
AGENT: nse-requirements (Claude Opus 4.6)
DATE: 2026-02-13
PARENT: EN-404 (Rule-Based Enforcement Enhancement)
FEATURE: FEAT-005 (Quality Framework Enforcement Mechanisms)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
QUALITY-TARGET: >= 0.92
ACTIVITY: DESIGN
-->

> **Type:** task
> **Status:** complete
> **Agent:** nse-requirements
> **Activity:** DESIGN
> **Created:** 2026-02-13
> **Parent:** EN-404

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Purpose](#purpose) | Why these requirements exist |
| [Scope](#scope) | What these requirements cover |
| [Requirements Overview](#requirements-overview) | Category summary and traceability matrix |
| [Token Budget Requirements](#token-budget-requirements) | REQ-404-001 through REQ-404-006 |
| [Enforcement Tier Requirements](#enforcement-tier-requirements) | REQ-404-010 through REQ-404-017 |
| [Adversarial Strategy Encoding Requirements](#adversarial-strategy-encoding-requirements) | REQ-404-020 through REQ-404-027 |
| [Decision Criticality Requirements](#decision-criticality-requirements) | REQ-404-030 through REQ-404-035 |
| [Quality Gate Requirements](#quality-gate-requirements) | REQ-404-040 through REQ-404-045 |
| [L2 Re-Injection Support Requirements](#l2-re-injection-support-requirements) | REQ-404-050 through REQ-404-054 |
| [Context Rot Mitigation Requirements](#context-rot-mitigation-requirements) | REQ-404-060 through REQ-404-064 |
| [Traceability Matrix](#traceability-matrix) | Full requirement-to-source traceability |
| [Verification Methods](#verification-methods) | How each requirement is verified |
| [References](#references) | Source documents |

---

## Purpose

This document defines the formal "shall" requirements for EN-404 (Rule-Based Enforcement Enhancement). These requirements govern the redesign of Jerry's `.context/rules/` files and `CLAUDE.md` to implement tiered enforcement language, adversarial strategy encoding, token budget optimization, and L2 re-injection support.

Requirements are derived from three authoritative sources:

1. **ADR-EPIC002-002** (ACCEPTED) -- 5-layer hybrid enforcement architecture, L1 layer specification, token budget targets
2. **Barrier-1 ADV-to-ENF Handoff** -- Adversarial strategy encoding requirements, quality gate integration, decision criticality escalation
3. **EN-404 Enabler** -- Functional requirements FR-001 through FR-014 and non-functional requirements NFR-001 through NFR-008

All requirements follow NASA NPR 7123.1D requirements engineering standards: each is uniquely identified, traceable, verifiable, necessary, and unambiguous.

---

## Scope

These requirements apply to:

- All files in `.context/rules/` (currently 10 files)
- `CLAUDE.md` (root context file)
- Any new rule files created as part of EN-404

These requirements do NOT apply to:

- Skill files (`skills/*/SKILL.md`)
- Hook scripts (`hooks/`, `scripts/`)
- Source code (`src/`)
- Test files (`tests/`)

---

## Requirements Overview

| Category | Count | IDs | Priority |
|----------|-------|-----|----------|
| Token Budget | 6 | REQ-404-001 to REQ-404-006 | HARD |
| Enforcement Tiers | 8 | REQ-404-010 to REQ-404-017 | HARD |
| Adversarial Strategy Encoding | 8 | REQ-404-020 to REQ-404-027 | HARD/MEDIUM |
| Decision Criticality | 6 | REQ-404-030 to REQ-404-035 | HARD |
| Quality Gates | 6 | REQ-404-040 to REQ-404-045 | HARD |
| L2 Re-Injection Support | 5 | REQ-404-050 to REQ-404-054 | HARD |
| Context Rot Mitigation | 5 | REQ-404-060 to REQ-404-064 | HARD/MEDIUM |
| **Total** | **44** | | |

---

## Token Budget Requirements

These requirements derive from ADR-EPIC002-002 L1 layer specification and R-SYS-002 (token budget exhaustion, score 16 RED).

| ID | Requirement | Source | Priority | Verification |
|----|-------------|--------|----------|--------------|
| REQ-404-001 | The total token count of all L1 content (CLAUDE.md + all `.context/rules/` files) SHALL NOT exceed 12,476 tokens (7.6% of the 200K context window). | ADR-EPIC002-002 Token Budget; NFR-001 | HARD | Measurement: word count * 1.3 for each file, summed |
| REQ-404-002 | CLAUDE.md SHALL NOT exceed 2,000 tokens (reduced from current ~3,200). | ADR-EPIC002-002 Token Budget Optimization Target | HARD | Measurement: word count * 1.3 |
| REQ-404-003 | The combined token count of all `.context/rules/` files SHALL NOT exceed 10,476 tokens (reduced from current ~22,500). | ADR-EPIC002-002 Token Budget Optimization Target | HARD | Measurement: word count * 1.3, summed |
| REQ-404-004 | Token reduction SHALL NOT reduce enforcement effectiveness; enforcement effectiveness SHALL be maintained or improved compared to the pre-optimization baseline. | ADR-EPIC002-002; NFR-002 | HARD | Analysis: pre/post enforcement coverage comparison |
| REQ-404-005 | Each rule file SHALL have a documented token budget allocation that sums to the REQ-404-003 total. | ADR-EPIC002-002 | HARD | Inspection: per-file budget in TASK-002 audit |
| REQ-404-006 | Adversarial strategy encoding (REQ-404-020 through REQ-404-027) SHALL fit within the token budgets allocated per REQ-404-005, not as additional token expenditure. | Barrier-1 ADV-to-ENF Token Budget Awareness | HARD | Measurement: post-encoding token counts vs. allocations |

---

## Enforcement Tier Requirements

These requirements derive from ADR-EPIC002-002 V-026 (Rule File Enforcement Language) and Barrier-1 ADV-to-ENF Enforcement Tier Language.

| ID | Requirement | Source | Priority | Verification |
|----|-------------|--------|----------|--------------|
| REQ-404-010 | All `.context/rules/` files SHALL classify every directive into exactly one enforcement tier: HARD, MEDIUM, or SOFT. | ADR-EPIC002-002 V-026; FR-001 | HARD | Inspection: every rule has a tier label |
| REQ-404-011 | HARD tier directives SHALL use exclusively the vocabulary: "MUST", "SHALL", "NEVER", "FORBIDDEN", "REQUIRED", "CRITICAL". | ADR-EPIC002-002 Enforcement Tier Language; Barrier-1 ADV-to-ENF | HARD | Inspection: no HARD rules use hedging language |
| REQ-404-012 | MEDIUM tier directives SHALL use exclusively the vocabulary: "SHOULD", "RECOMMENDED", "PREFERRED", "EXPECTED". | ADR-EPIC002-002 Enforcement Tier Language | HARD | Inspection: consistent MEDIUM vocabulary |
| REQ-404-013 | SOFT tier directives SHALL use exclusively the vocabulary: "MAY", "CONSIDER", "OPTIONAL", "SUGGESTED". | ADR-EPIC002-002 Enforcement Tier Language | HARD | Inspection: consistent SOFT vocabulary |
| REQ-404-014 | HARD tier directives SHALL be visually distinguishable from MEDIUM and SOFT directives through formatting conventions (bold labels, table format, or blockquote callouts). | NFR-007; FR-001 | MEDIUM | Inspection: visual distinction is apparent |
| REQ-404-015 | No rule file SHALL contain enforcement language that mixes tier vocabularies within a single directive (e.g., "SHOULD NEVER" or "MAY be REQUIRED"). | NFR-004 | HARD | Inspection: no mixed-tier language |
| REQ-404-016 | HARD tier directives SHALL state the consequence of violation (e.g., "Violations will be blocked", "Build will fail"). | NFR-004 | HARD | Inspection: every HARD rule has a consequence |
| REQ-404-017 | The number of HARD tier directives across all rule files SHALL NOT exceed 30, to prevent enforcement fatigue and preserve signal-to-noise ratio. | ADR-EPIC002-002 NFR-005 (context rot feedback loop) | MEDIUM | Count: total HARD directives <= 30 |

---

## Adversarial Strategy Encoding Requirements

These requirements derive from Barrier-1 ADV-to-ENF Section "Rules (Static Context) -- EN-404". Six strategies must be encoded as rule-based enforcement.

| ID | Requirement | Source | Priority | Verification |
|----|-------------|--------|----------|--------------|
| REQ-404-020 | Rules SHALL encode S-007 (Constitutional AI) as HARD enforcement: existing rules serve as the constitution, and Claude SHALL evaluate its outputs against constitutional principles before presenting them. | Barrier-1 ADV-to-ENF; FR-003 | HARD | Inspection: S-007 language present in rule files |
| REQ-404-021 | Rules SHALL encode S-003 (Steelman) as a HARD directive: "Before criticizing any proposal, MUST first present the strongest version of the argument." | Barrier-1 ADV-to-ENF; FR-004 | HARD | Inspection: S-003 language present |
| REQ-404-022 | Rules SHALL encode S-010 (Self-Refine) as a HARD directive: "MUST review own output for completeness, accuracy, and quality before presenting it." | Barrier-1 ADV-to-ENF; FR-005 | HARD | Inspection: S-010 language present |
| REQ-404-023 | Rules SHALL encode S-014 (LLM-as-Judge) as a HARD directive: "All deliverables for C2+ decisions MUST include a quality score against defined rubrics. Target: >= 0.92." | Barrier-1 ADV-to-ENF; FR-006 | HARD | Inspection: S-014 language with 0.92 threshold present |
| REQ-404-024 | Rules SHALL encode S-002 (Devil's Advocate) as a MEDIUM directive: "Before finalizing any decision, SHOULD explicitly consider and document the strongest counterargument." | Barrier-1 ADV-to-ENF; FR-007 | MEDIUM | Inspection: S-002 language present |
| REQ-404-025 | Rules SHALL encode S-013 (Inversion) as a MEDIUM directive: "Before proposing any solution, SHOULD identify at least 3 ways it could fail." | Barrier-1 ADV-to-ENF; FR-008 | MEDIUM | Inspection: S-013 language present |
| REQ-404-026 | All six adversarial strategy encodings SHALL fit within the existing token budget (REQ-404-003) without exceeding the 10,476 token allocation for rule files. | Barrier-1 ADV-to-ENF Token Budget Awareness; FR-002 | HARD | Measurement: post-encoding token count |
| REQ-404-027 | Adversarial strategy encoding SHALL be additive to existing rule content semantically but NOT duplicative -- no strategy shall be encoded in more than one rule file. | Barrier-1 ADV-to-ENF Token Budget Awareness | HARD | Inspection: no duplicate strategy encodings across files |

---

## Decision Criticality Requirements

These requirements derive from Barrier-1 ADV-to-ENF Section "Decision Criticality Escalation" and ADR-EPIC002-001.

| ID | Requirement | Source | Priority | Verification |
|----|-------------|--------|----------|--------------|
| REQ-404-030 | Rules SHALL define four decision criticality levels: C1 (Routine), C2 (Standard), C3 (Significant), C4 (Critical). | Barrier-1 ADV-to-ENF Decision Criticality Escalation; FR-009 | HARD | Inspection: all four levels defined with criteria |
| REQ-404-031 | Each criticality level SHALL specify: classification criteria, default review layer (L0-L4), applicable adversarial strategies (mandatory vs. optional), and enforcement vectors. | Barrier-1 ADV-to-ENF Decision Criticality Escalation; FR-009 | HARD | Inspection: all four attributes per level |
| REQ-404-032 | C1 (Routine) criteria SHALL be: reversible within 1 session, fewer than 3 files changed, no external dependencies. Default review: L1 (Self-Check). | Barrier-1 ADV-to-ENF | HARD | Inspection: C1 definition matches |
| REQ-404-033 | C2 (Standard) criteria SHALL be: reversible within 1 day, 3-10 files changed, no API changes. Default review: L2 (Standard Critic). | Barrier-1 ADV-to-ENF | HARD | Inspection: C2 definition matches |
| REQ-404-034 | C3 (Significant) criteria SHALL be: more than 1 day to reverse, more than 10 files, API/interface changes. Default review: L3 (Deep Review). | Barrier-1 ADV-to-ENF | HARD | Inspection: C3 definition matches |
| REQ-404-035 | Any artifact touching `docs/governance/JERRY_CONSTITUTION.md` or `.context/rules/` SHALL be automatically classified as C3 or higher. This rule CANNOT be overridden. | Barrier-1 ADV-to-ENF; FR-011 | HARD | Inspection: mandatory escalation rule present |

---

## Quality Gate Requirements

These requirements derive from Barrier-1 ADV-to-ENF Section "Quality Gate Integration" and the 0.92 threshold.

| ID | Requirement | Source | Priority | Verification |
|----|-------------|--------|----------|--------------|
| REQ-404-040 | Rules SHALL define the quality gate threshold as >= 0.92 for all deliverables at C2+ criticality. | Barrier-1 ADV-to-ENF; FR-006; FR-010 | HARD | Inspection: 0.92 threshold stated as HARD rule |
| REQ-404-041 | Rules SHALL define the creator-critic-revision cycle as a minimum of 3 iterations for C2+ decisions. | Barrier-1 ADV-to-ENF; FR-010 | HARD | Inspection: 3-iteration minimum stated as HARD rule |
| REQ-404-042 | Rules SHALL define the strategy composition per quality layer: L0 (S-010), L1 (S-003 + S-010 + S-014), L2 (S-007 + S-002 + S-014), L3 (L2 + S-004 + S-012 + S-013), L4 (L3 + S-001 + S-011). | Barrier-1 ADV-to-ENF Quality Gate Integration | HARD | Inspection: layer-strategy mapping present |
| REQ-404-043 | Rules SHALL require that if a deliverable scores below 0.92 after 3 iterations, additional iterations are triggered until either the threshold is met or escalation to the next criticality level occurs. | Barrier-1 ADV-to-ENF Quality Gate Integration | HARD | Inspection: iteration escalation rule present |
| REQ-404-044 | The quality gate definition SHALL be the single authoritative source -- defined in exactly one rule file, referenced from others. | FR-013; NFR-005 | HARD | Inspection: no duplicate definitions |
| REQ-404-045 | A new `quality-enforcement.md` rule file SHALL be created as the authoritative source for enforcement framework definitions including: tier definitions, quality thresholds, decision criticality levels, and adversarial strategy trigger conditions. | FR-013 | HARD | Inspection: file exists with required content |

---

## L2 Re-Injection Support Requirements

These requirements derive from ADR-EPIC002-002 Section "Defense-in-Depth Context for L1" and FR-012.

| ID | Requirement | Source | Priority | Verification |
|----|-------------|--------|----------|--------------|
| REQ-404-050 | Rules SHALL tag the highest-priority content for L2 re-injection via V-024 (Context Reinforcement via Repetition). | ADR-EPIC002-002 L2 dependency on L1; FR-012 | HARD | Inspection: tagged content exists |
| REQ-404-051 | The tagging mechanism SHALL use a consistent marker (e.g., `<!-- L2-REINJECT: priority=HIGH -->`) that V-024 implementation (EN-403) can programmatically extract. | ADR-EPIC002-002 | HARD | Inspection: consistent tag format |
| REQ-404-052 | Tagged L2 re-injection content SHALL NOT exceed 600 tokens total (the V-024 per-session budget from ADR-EPIC002-002). | ADR-EPIC002-002 Token Budget Feasibility | HARD | Measurement: tagged content token count <= 600 |
| REQ-404-053 | The following rule categories SHALL be prioritized for L2 re-injection: (a) Constitutional constraints (P-003, P-020, P-022), (b) Python environment (UV only), (c) Quality gate threshold (0.92), (d) HARD enforcement tier definitions. | ADR-EPIC002-002 V-024 synergy analysis | HARD | Inspection: priority categories tagged |
| REQ-404-054 | L2 re-injection tags SHALL include a priority rank (1-N) enabling V-024 to select the most critical content when the 600-token budget must be further constrained. | ADR-EPIC002-002 | MEDIUM | Inspection: ranked tags present |

---

## Context Rot Mitigation Requirements

These requirements derive from ADR-EPIC002-002 R-SYS-001 (context rot cascade, score 20 RED) and R-SYS-004 (context rot + token exhaustion feedback loop, score 16 RED).

| ID | Requirement | Source | Priority | Verification |
|----|-------------|--------|----------|--------------|
| REQ-404-060 | Within each rule file, the most critical HARD directives SHALL be placed in the first 25% of the file content, exploiting recency and primacy bias in LLM attention. | ADR-EPIC002-002 R-SYS-001; NFR-003 | HARD | Inspection: HARD rules appear early in each file |
| REQ-404-061 | Rule files SHALL prefer concise imperative statements over verbose explanatory prose. Verbose examples and rationale SHALL be placed after the enforcement directives, not before. | NFR-005; ADR-EPIC002-002 R-SYS-004 | HARD | Inspection: enforcement-first, explanation-second structure |
| REQ-404-062 | Redundant content that appears in multiple rule files SHALL be consolidated into a single authoritative file and referenced from others. | NFR-005 | MEDIUM | Inspection: no significant content duplication |
| REQ-404-063 | Rule files SHALL NOT contain content that does not contribute to enforcement (e.g., aspirational roadmaps, historical context, implementation details that belong in source code). | NFR-005; ADR-EPIC002-002 R-SYS-004 | MEDIUM | Inspection: no non-enforcement content |
| REQ-404-064 | All rule files SHALL maintain the navigation table standard (NAV-001 through NAV-006) to support efficient Claude navigation even under context pressure. | NFR-008 | MEDIUM | Inspection: NAV compliance per markdown-navigation-standards.md |

---

## Traceability Matrix

### Requirements to Functional Requirements (FR)

| Requirement | FR-001 | FR-002 | FR-003 | FR-004 | FR-005 | FR-006 | FR-007 | FR-008 | FR-009 | FR-010 | FR-011 | FR-012 | FR-013 | FR-014 |
|-------------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| REQ-404-001 | | X | | | | | | | | | | | | |
| REQ-404-003 | | X | | | | | | | | | | | | |
| REQ-404-004 | | X | | | | | | | | | | | | |
| REQ-404-010 | X | | | | | | | | | | | | | |
| REQ-404-011 | X | | | | | | | | | | | | | |
| REQ-404-020 | | | X | | | | | | | | | | | |
| REQ-404-021 | | | | X | | | | | | | | | | |
| REQ-404-022 | | | | | X | | | | | | | | | |
| REQ-404-023 | | | | | | X | | | | | | | | |
| REQ-404-024 | | | | | | | X | | | | | | | |
| REQ-404-025 | | | | | | | | X | | | | | | |
| REQ-404-030 | | | | | | | | | X | | | | | |
| REQ-404-040 | | | | | | X | | | | X | | | | |
| REQ-404-041 | | | | | | | | | | X | | | | |
| REQ-404-035 | | | | | | | | | | | X | | | |
| REQ-404-050 | | | | | | | | | | | | X | | |
| REQ-404-045 | | | | | | | | | | | | | X | |

### Requirements to Non-Functional Requirements (NFR)

| Requirement | NFR-001 | NFR-002 | NFR-003 | NFR-004 | NFR-005 | NFR-006 | NFR-007 | NFR-008 |
|-------------|---------|---------|---------|---------|---------|---------|---------|---------|
| REQ-404-001 | X | | | | | | | |
| REQ-404-004 | | X | | | | | | |
| REQ-404-060 | | | X | | | | | |
| REQ-404-015 | | | | X | | | | |
| REQ-404-016 | | | | X | | | | |
| REQ-404-061 | | | | | X | | | |
| REQ-404-014 | | | | | | | X | |
| REQ-404-064 | | | | | | | | X |

### Requirements to ADR-EPIC002-002 Vectors

| Requirement | V-008 | V-009 | V-010 | V-015 | V-016 | V-017 | V-026 |
|-------------|-------|-------|-------|-------|-------|-------|-------|
| REQ-404-002 | X | | | | | | |
| REQ-404-020 | | X | X | | | | |
| REQ-404-011 | | | | | | | X |
| REQ-404-010 | | | | X | X | X | X |

### Requirements to Acceptance Criteria

| Requirement | AC-1 | AC-2 | AC-3 | AC-4 | AC-5 | AC-8 | AC-9 | AC-10 | AC-12 | AC-13 |
|-------------|------|------|------|------|------|------|------|-------|-------|-------|
| REQ-404-001 | | | | | | X | | | X | |
| REQ-404-010 | | | X | | | | | | | |
| REQ-404-030 | | X | | | | | | | | |
| REQ-404-040 | | | | | X | | | | | |
| REQ-404-050 | | | | | | | X | | | |
| REQ-404-020 | | | | | | | | X | | |
| REQ-404-035 | | | | | | | | | | X |

---

## Verification Methods

| Method | Description | Applicable Requirements |
|--------|-------------|------------------------|
| **Measurement** | Quantitative token count using word count * 1.3 conversion factor as a design-time approximation. **Note (v1.1.0 -- M-001):** Production verification MUST use an actual tokenizer (tiktoken cl100k_base or Claude's tokenizer) to validate budget compliance. The word count * 1.3 ratio is unreliable for XML-tagged content, structured tables, and code snippets (observed variance up to +/-20%). | REQ-404-001, 002, 003, 005, 006, 026, 052 |
| **Inspection** | Manual review of rule file content against requirement specification | REQ-404-010-017, 020-025, 027, 030-035, 040-045, 050-054, 060-064 |
| **Analysis** | Comparative analysis of enforcement coverage before and after optimization | REQ-404-004 |
| **Count** | Enumeration of specific elements (HARD directives, duplicate encodings) | REQ-404-017, 027 |

### Verification Responsibility

| Phase | Verification Owner | Scope |
|-------|-------------------|-------|
| TASK-002 (Audit) | ps-investigator | Baseline measurements for REQ-404-001 through REQ-404-003 |
| TASK-005/006/007 (Implementation) | ps-architect | Implementation compliance with all REQs |
| TASK-008 (Adversarial Review) | ps-critic | Bypass vector identification against REQs |
| TASK-010 (Verification) | nse-verification | Final verification of all 44 requirements |

---

## References

| # | Document | Location | Content Used |
|---|----------|----------|--------------|
| 1 | ADR-EPIC002-002 (ACCEPTED) | `EN-402-enforcement-priority-analysis/TASK-005-enforcement-ADR.md` | L1 layer specification, token budget targets, enforcement tier language, 5-layer architecture, V-008/V-009/V-010/V-015-V-017/V-026, R-SYS-001 through R-SYS-004 |
| 2 | Barrier-1 ADV-to-ENF Handoff | `orchestration/epic002-crosspoll-20260213-001/cross-pollination/barrier-1/adv-to-enf/barrier-1-adv-to-enf-handoff.md` | 6 adversarial strategies, quality gate integration, decision criticality escalation, enforcement tier language, token budget awareness |
| 3 | EN-404 Enabler (Enriched) | `EN-404-rule-based-enforcement/EN-404-rule-based-enforcement.md` | FR-001 through FR-014, NFR-001 through NFR-008, acceptance criteria |
| 4 | NASA NPR 7123.1D | Systems Engineering Processes and Requirements | Requirements engineering methodology |

---

*Agent: nse-requirements (Claude Opus 4.6)*
*Date: 2026-02-13*
*Parent: EN-404 Rule-Based Enforcement Enhancement*
*Quality Target: >= 0.92*
*Total Requirements: 44 (33 HARD, 11 MEDIUM)*
*Note (v1.1.0 -- m-004): The EN-404 enabler states ~25,700 tokens for current L1 content. The TASK-002 audit, which reads all files individually, reports ~30,160. The TASK-002 audit figure (~30,160) is the authoritative baseline as it is derived from direct file content analysis. The enabler estimate was made prior to the detailed audit.*
