# TASK-008: Configuration Baseline Documentation

<!--
DOCUMENT-ID: FEAT-004:EN-306:TASK-008
VERSION: 1.1.0
AGENT: ps-validator-306
DATE: 2026-02-13
STATUS: Complete
PARENT: EN-306 (Integration Testing & Validation)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
ACTIVITY: DOCUMENTATION
-->

> **Version:** 1.1.0
> **Agent:** ps-validator-306
> **Quality Target:** >= 0.92
> **Purpose:** Configuration baseline documenting version matrix, configuration parameters, and baseline snapshot for all adversarial strategy integrations

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this baseline documents |
| [Version Matrix](#version-matrix) | All agent and skill version changes |
| [Configuration Parameters](#configuration-parameters) | All configurable parameters introduced |
| [Strategy Registry](#strategy-registry) | Canonical strategy definitions baseline |
| [Quality Framework Parameters](#quality-framework-parameters) | Quality scoring and enforcement configuration |
| [Enforcement Layer Configuration](#enforcement-layer-configuration) | Per-layer configuration state |
| [SSOT Reference Points](#ssot-reference-points) | Single Source of Truth artifacts |
| [Baseline Snapshot](#baseline-snapshot) | Point-in-time configuration state |
| [Change Control](#change-control) | How to modify this baseline |
| [Traceability](#traceability) | Mapping to EN-306 AC-8 |
| [References](#references) | Source citations |

---

## Summary

This document establishes the configuration baseline for all adversarial strategy integrations delivered by FEAT-004. It captures the exact version numbers, configuration parameters, and canonical definitions that constitute the "known good state" after FEAT-004 completion. Any future modifications to adversarial strategy configuration should be tracked against this baseline.

The baseline covers: 6 agent specs (3 skills), 3 SKILL.md files, 3 PLAYBOOK.md files, 3 orchestration templates, the strategy registry (10 strategies), the quality framework parameters, and the enforcement layer configuration.

---

## Version Matrix

### Agent Specifications

| Agent | Skill | Pre-FEAT-004 Version | Post-FEAT-004 Version | Key Changes |
|-------|-------|---------------------|----------------------|-------------|
| ps-critic | /problem-solving | v2.2.0 | **v3.0.0** | 10 adversarial modes added; invocation protocol extended; anti-leniency calibration added |
| nse-verification | /nasa-se | v2.1.0 | **v3.0.0** | 4 adversarial modes + S-010 pre-step; structured finding output format; criticality-based activation |
| nse-reviewer | /nasa-se | v2.2.0 | **v3.0.0** | 6 adversarial modes; strategy-to-gate mapping; NPR finding category integration; criticality-based activation |
| nse-qa | /nasa-se | v2.1.0 | v2.1.0 (unchanged) | Adversarial modes descoped per EN-305-F002; follow-up enabler planned |
| orch-planner | /orchestration | v2.1.0 | **v3.0.0** | Auto adversarial cycle generation; strategy assignment by criticality; validation agent auto-injection |
| orch-tracker | /orchestration | v2.1.0 | **v3.0.0** | Quality score recording; score aggregation; pass/fail determination; escalation protocol; early exit logic; barrier quality gates |
| orch-synthesizer | /orchestration | v2.1.0 | **v3.0.0** | 7-step adversarial synthesis protocol; strategy effectiveness report; residual risk documentation |

### Skill Documentation

| Document | Skill | Pre-FEAT-004 Version | Post-FEAT-004 Version | Key Changes |
|----------|-------|---------------------|----------------------|-------------|
| SKILL.md | /problem-solving | v2.0.0 | **v3.0.0** | Adversarial review capabilities; available modes; criticality-based selection; enforcement layer integration |
| SKILL.md | /nasa-se | v1.1.0 | **v2.0.0** | Adversarial quality enforcement; strategy-to-gate mapping; criticality-based activation; agent adversarial capabilities |
| SKILL.md | /orchestration | v2.0.0 | **v3.0.0** | Adversarial feedback loop pattern; quality gate enforcement; adversarial configuration section |
| PLAYBOOK.md | /problem-solving | v3.3.0 | **v4.0.0** | Updated Pattern 6; new Patterns 7, 8; mode invocation guide; adversarial results interpretation; escalation procedures |
| PLAYBOOK.md | /orchestration | v3.0.0 | **v4.0.0** | L0/L1/L2 adversarial guidance; quality gate scenarios; anti-pattern catalog (AP-005 through AP-008); hard constraints (HC-006 through HC-010) |

### Orchestration Templates

| Template | Pre-FEAT-004 | Post-FEAT-004 | Key Changes |
|----------|-------------|---------------|-------------|
| ORCHESTRATION_PLAN.template.md | v1.0.0 | **v2.0.0** | Adversarial review configuration section; phase criticality; strategy assignment; enforcement layer mapping; token budget estimate |
| ORCHESTRATION.template.yaml | v1.0.0 | **v2.0.0** | Adversarial constraints; patterns list; phase quality fields; iteration tracking; barrier quality_summary; metrics.quality; resumption adversarial_feedback_status |
| ORCHESTRATION_WORKTRACKER.template.md | v1.0.0 | **v2.0.0** | Adversarial review log; quality gate status; iteration details; finding resolution tracking; escalation log |

---

## Configuration Parameters

### Quality Gate Parameters

| Parameter | Value | Source | Scope |
|-----------|-------|--------|-------|
| `quality_gate_threshold` | 0.92 | quality-enforcement.md SSOT (H-13) | All skills |
| `adversarial_iteration_min` | 3 | H-14 | All skills |
| `adversarial_validation` | true (default for new workflows) | NFR-307-003 | /orchestration |
| `anti_leniency.enabled` | true | H-16 | All skills |
| `anti_leniency.score_threshold` | 0.90 | EN-304 TASK-003 | /problem-solving |
| `anti_leniency.jump_threshold` | 0.20 | EN-304 TASK-003 | /problem-solving |
| `anti_leniency.ceiling_count` | 3 | EN-304 TASK-003 | /problem-solving |
| `anti_leniency.calibration_prompt` | "leniency-calibration" ContentBlock | Barrier-2 L2 system | All skills |

### Circuit Breaker Parameters

| Parameter | Value | Source |
|-----------|-------|--------|
| `max_iterations` | 3 (default) | EN-304-F002 terminology fix |
| `plateau_threshold` | 0.05 delta for 2 consecutive iterations | EN-304 TASK-003 |
| `accept_with_caveats_threshold` | 0.85 | EN-304 TASK-003 |

### Score Dimensions

> **Correction (F-023):** Previous version listed weights as "Equal (1/6)." The canonical weights from EN-304 TASK-003 and as used in adversarial critiques are UNEQUAL. Corrected below.

| Dimension | Weight | Source |
|-----------|--------|--------|
| completeness | 0.20 | EN-304 TASK-003 canonical dimensions |
| internal_consistency | 0.20 | EN-304 TASK-003 canonical dimensions |
| evidence_quality | 0.15 | EN-304 TASK-003 canonical dimensions |
| methodological_rigor | 0.20 | EN-304 TASK-003 canonical dimensions |
| actionability | 0.15 | EN-304 TASK-003 canonical dimensions |
| traceability | 0.10 | EN-304 TASK-003 canonical dimensions |

**Total weight:** 1.00

### Criticality Levels

| Level | Description | Strategy Count | Token Budget |
|-------|-------------|---------------|-------------|
| C1 | Routine | 1 (S-010 only) | ~2,000 |
| C2 | Significant | 3-5 Required + 2-3 Recommended | ~12,100 - ~18,000 |
| C3 | Major | 6-7 Required + 2-3 Recommended | ~23,700 - ~27,200 |
| C4 | Critical | All 10 Required | ~50,300 |

---

## Strategy Registry

### Canonical Strategy Definitions

| ID | Name | Mode Name (ps-critic) | Type | Token Cost | Source |
|----|------|-----------------------|------|------------|--------|
| S-001 | Red Team | `red-team` | Generative | ~5,000 | ADR-EPIC002-001 |
| S-002 | Devil's Advocate | `devils-advocate` | Analytical | ~4,600 | ADR-EPIC002-001 |
| S-003 | Steelman | `steelman` | Constructive | ~1,600 | ADR-EPIC002-001 |
| S-004 | Pre-Mortem | `pre-mortem` | Generative | ~5,600 | ADR-EPIC002-001 |
| S-007 | Constitutional AI | `constitutional` | Analytical | ~8,000-16,000 | ADR-EPIC002-001 |
| S-010 | Self-Refine | `self-refine` | Constructive | ~2,000 | ADR-EPIC002-001 |
| S-011 | Chain-of-Verification | `chain-of-verification` | Analytical | ~4,500 | ADR-EPIC002-001 **(Correction F-024: changed from ~6,000 to ~4,500 to match PST-008 in TASK-002 and EN-304 TASK-002 canonical token cost table)** |
| S-012 | FMEA | `fmea` | Analytical | ~9,000 | ADR-EPIC002-001 |
| S-013 | Inversion | `inversion` | Generative | ~2,100 | ADR-EPIC002-001 |
| S-014 | LLM-as-Judge | `llm-as-judge` | Evaluative | ~2,000 | ADR-EPIC002-001 |

### Rejected Strategies (Not in Registry)

| ID | Name | Rejection Rationale |
|----|------|-------------------|
| S-005 | Dialectical Inquiry | Overlaps with S-002 + S-003 |
| S-006 | Analysis of Competing Hypotheses | Narrow applicability |
| S-008 | Debate | Token-intensive; P-003 conflict |
| S-009 | Socratic Questioning | Requires interactive dialogue |
| S-015 | Adversarial NLI | Too narrow (NLI-specific) |

### Sequencing Constraints

| ID | Constraint | Effect |
|----|-----------|--------|
| SEQ-001 | steelman before devils-advocate, constitutional, red-team | Ensures critique engages strongest argument |
| SEQ-002 | inversion before constitutional, fmea, red-team; not concurrent with steelman | Anti-patterns inform subsequent evaluation |
| SEQ-003 | constitutional before llm-as-judge; llm-as-judge always last | Compliance informs final scoring |
| SEQ-004 | self-refine first | Self-improvement before external critique |
| SEQ-005 | chain-of-verification is order-independent | Factual verification is context-isolated |

### Auto-Escalation Rules

| ID | Trigger | Effect |
|----|---------|--------|
| AE-001 | Artifact modifies JERRY_CONSTITUTION.md | min(criticality, C3) |
| AE-002 | Artifact modifies .claude/rules/* | min(criticality, C3) |
| AE-003 | Artifact is new/modified ADR | min(criticality, C3) |
| AE-004 | Artifact modifies baselined ADR | criticality = C4 |
| AE-005 | Artifact modifies security-relevant code | min(criticality, C3) |
| AE-006 | C3+ at TOK-EXHAUST | Human escalation MANDATORY |

---

## Quality Framework Parameters

### Quality Gate Decision Matrix

| Condition | Verdict | Action |
|-----------|---------|--------|
| score >= 0.92 | PASS | Accept; proceed to next phase |
| score >= 0.92 at iteration 2 | PASS (early exit) | Skip iteration 3; proceed |
| 0.85 <= score < 0.92 at max iterations | CONDITIONAL PASS | User ratification required (P-020) |
| score < 0.85 at max iterations | FAIL | Blocker created; phase blocked |
| delta < 0.05 for 2 consecutive iterations | CONDITIONAL PASS (plateau) | User notified; caveats documented |

### Anti-Leniency Anomaly Detection

| Check | Threshold | Action |
|-------|-----------|--------|
| Score jump > 0.20 in one iteration | delta > 0.20 | Flag for human review |
| Scores consistently > 0.95 | 3+ artifacts at > 0.95 | Flag for rubric recalibration |
| Score improvement without artifact changes | delta > 0.05 AND no new version | Flag as leniency drift |
| First-iteration scores > 0.90 at C2+ | iteration == 1 AND score > 0.90 AND C2+ | Flag for review |

---

## Enforcement Layer Configuration

### 5-Layer Architecture State

| Layer | Status | Adversarial Integration |
|-------|--------|------------------------|
| **L1** (Constitutional Rules) | Active | Adversarial strategies referenced in constitutional principles |
| **L2** (Prompt Reinforcement) | Active | `leniency-calibration` ContentBlock; L2-REINJECT tags for quality reminders |
| **L3** (Pre-Tool Hooks) | Active | PreToolEnforcementEngine provides C1-C4 criticality assessment; governance file detection |
| **L4** (Post-Tool Hooks) | Active | PostToolEnforcementEngine validates quality scores post-review |
| **L5** (CLAUDE.md/Rules) | Active | quality-enforcement.md SSOT; mandatory-skill-usage.md |
| **Process** (Workflow) | Active | Adversarial loop patterns in PLAYBOOK.md; orchestration templates |

### Graceful Degradation Matrix

| Platform | L1 | L2 | L3 | L4 | L5 | Process | Net Impact |
|----------|----|----|----|----|----|---------|-----------|
| PLAT-CC (macOS/Linux) | Full | Full | Full | Full | Full | Full | None |
| PLAT-CC-WIN | Full | Full | Full | Full | Full | Full | None |
| PLAT-GENERIC | Full | Partial | None | None | Full | Full | Reduced auto-escalation; manual calibration |

---

## SSOT Reference Points

### Canonical SSOT Documents

| SSOT | Location | Consumers | Content |
|------|----------|-----------|---------|
| Token Cost Table | EN-304 TASK-002 | EN-305, EN-307 | Per-strategy token costs |
| FMEA Scale | EN-304 TASK-002 | EN-305, EN-307 | 1-10 scale definition |
| Quality Score Dimensions | EN-304 TASK-003 | EN-305, EN-307 | 6 canonical dimension names |
| Strategy Registry | ADR-EPIC002-001 (EN-302 TASK-005) | EN-304, EN-305, EN-307 | 10 accepted strategy IDs |
| Quality Threshold | quality-enforcement.md | All skills | 0.92 threshold |
| Criticality Levels | EN-303 TASK-001 | All enablers | C1-C4 definitions |
| Context Taxonomy | EN-303 TASK-001 | EN-304, EN-305, EN-307 | 8-dimension context vector |
| Decision Tree | EN-303 TASK-004 | EN-304 | Automatic strategy selection algorithm |

### SSOT Update Protocol

When modifying any SSOT artifact:
1. Update the canonical source document.
2. Verify all consumers still reference the canonical source.
3. Update this baseline document with the change.
4. Apply adversarial review at C3+ criticality (AE-004 for baselined ADRs).

---

## Baseline Snapshot

### Snapshot Date: 2026-02-13

### File Inventory

> **Renamed (F-025):** Previously "File Checksums (Conceptual)." Renamed to "File Inventory" because no actual checksums are computed. For baseline verification, use git commit SHA as the anchor point (more practical than file checksums for markdown content). **Baseline Git Anchor:** The git commit SHA at the time of baseline creation serves as the definitive rollback reference.

| File | Version | Status |
|------|---------|--------|
| EN-304 TASK-001 (Requirements) | v1.0.0 | Baselined |
| EN-304 TASK-002 (Mode Design -- SSOT) | v1.0.0 | Baselined |
| EN-304 TASK-003 (Invocation Protocol) | v1.0.0 | Baselined |
| EN-304 TASK-004 (ps-critic v3.0.0 spec) | v1.0.0 | Baselined |
| EN-304 TASK-005 (SKILL.md v3.0.0 content) | v1.0.0 | Baselined |
| EN-304 TASK-006 (PLAYBOOK.md v4.0.0 content) | v1.0.0 | Baselined |
| EN-304 TASK-010 (Validation Report) | v1.0.0 | Baselined |
| EN-305 TASK-001 (Requirements) | v1.0.0 | Baselined |
| EN-305 TASK-004 (Review Gate Mapping) | v1.0.0 | Baselined |
| EN-305 TASK-005 (nse-verification v3.0.0 spec) | v1.0.0 | Baselined |
| EN-305 TASK-006 (nse-reviewer v3.0.0 spec) | v1.0.0 | Baselined |
| EN-305 TASK-007 (SKILL.md v2.0.0 content) | v1.0.0 | Baselined |
| EN-307 TASK-001 (Requirements) | v1.0.0 | Baselined |
| EN-307 TASK-004 (orch-planner v3.0.0 spec) | v1.0.0 | Baselined |
| EN-307 TASK-005 (orch-tracker v3.0.0 spec) | v1.0.0 | Baselined |
| EN-307 TASK-006 (orch-synthesizer v3.0.0 spec) | v1.0.0 | Baselined |
| EN-307 TASK-007 (SKILL.md v3.0.0 content) | v1.0.0 | Baselined |
| EN-307 TASK-008 (PLAYBOOK.md v4.0.0 content) | v1.0.0 | Baselined |
| EN-307 TASK-009 (Template updates) | v1.0.0 | Baselined |
| ADR-EPIC002-001 (Strategy Selection) | ACCEPTED | Baselined |

### Baseline State Summary

| Category | Count | Status |
|----------|-------|--------|
| Agent specs at v3.0.0 | 6 | Baselined |
| SKILL.md updates | 3 | Baselined |
| PLAYBOOK.md updates | 2 | Baselined |
| Orchestration templates | 3 | Baselined |
| Formal requirements | 144 | Baselined |
| Integration test specs | 5 | Baselined |
| Strategies in registry | 10 | Baselined |
| Quality score dimensions | 6 | Baselined |

---

## Change Control

### Modification Categories

| Category | Criticality | Approval Required | Review Required |
|----------|-------------|------------------|-----------------|
| Strategy addition or removal | C4 | User + ADR amendment | Full adversarial review (all 10 strategies) |
| Quality threshold change | C4 | User + constitutional review | Full adversarial review |
| Agent spec version bump | C3 | User approval | Adversarial review at C3 |
| SSOT parameter update | C3 | User + SSOT update protocol | All consumers verified |
| SKILL.md/PLAYBOOK.md update | C2 | Standard review | Adversarial review at C2 |
| Template update | C2 | Standard review | Backward compatibility test |
| Documentation fix | C1 | None (self-refine sufficient) | S-010 Self-Refine |

### Change Request Template

For any proposed change to baselined configuration:

1. **What:** Describe the parameter or artifact being changed
2. **Why:** Rationale for the change
3. **Impact:** Which consumers are affected (trace through SSOT reference points)
4. **Criticality:** C1/C2/C3/C4 per modification categories table
5. **Review plan:** Which adversarial strategies will be applied
6. **Rollback plan:** How to revert if the change causes issues

---

## Traceability

### To EN-306 Acceptance Criteria

| EN-306 AC | Coverage |
|-----------|----------|
| AC-8 (Configuration baseline documented) | This entire document |

### To FEAT-004 Non-Functional Criteria

| FEAT-004 NFC | Coverage |
|--------------|----------|
| NFC-7 (nse-configuration tracks configuration baselines) | This entire document |

---

## References

| # | Citation | Sections Referenced |
|---|----------|-------------------|
| 1 | ADR-EPIC002-001 (Strategy Selection) -- FEAT-004:EN-302:TASK-005 | Strategy registry, accepted/rejected strategies |
| 2 | EN-304 TASK-002 (Mode Design) -- FEAT-004:EN-304:TASK-002 | Token cost table (SSOT), FMEA scale (SSOT), mode definitions |
| 3 | EN-304 TASK-003 (Invocation Protocol) -- FEAT-004:EN-304:TASK-003 | Quality score dimensions, anti-leniency config, circuit breaker, sequencing |
| 4 | EN-303 TASK-001 (Context Taxonomy) -- FEAT-004:EN-303:TASK-001 | C1-C4 criticality levels, 8-dimension context vector |
| 5 | EN-305 TASK-004 (Review Gate Mapping) -- FEAT-004:EN-305:TASK-004 | Strategy-to-gate mapping, token budget per gate |
| 6 | EN-307 TASK-001 (Requirements) -- FEAT-004:EN-307:TASK-001 | Orchestration adversarial requirements |
| 7 | EN-304 TASK-010 (Validation Report) -- FEAT-004:EN-304:TASK-010 | Quality scores, cross-enabler consistency |
| 8 | Barrier-2 ENF-to-ADV Handoff -- EPIC002-CROSSPOLL-B2-ENF-TO-ADV | Enforcement layer architecture, HARD rules |

---

*Document ID: FEAT-004:EN-306:TASK-008*
*Agent: ps-validator-306*
*Created: 2026-02-13*
*Status: Complete*
