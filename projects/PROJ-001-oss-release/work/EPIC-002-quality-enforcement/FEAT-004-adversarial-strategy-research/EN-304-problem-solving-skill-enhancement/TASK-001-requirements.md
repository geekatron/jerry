# TASK-001: Requirements for /problem-solving Skill Enhancement

<!--
DOCUMENT-ID: FEAT-004:EN-304:TASK-001
VERSION: 1.0.0
AGENT: ps-architect-304 (creator)
DATE: 2026-02-13
STATUS: Draft
PARENT: EN-304 (Problem-Solving Skill Enhancement)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
ACTIVITY: DESIGN
-->

> **Version:** 1.0.0
> **Agent:** ps-architect-304
> **Quality Target:** >= 0.92
> **Purpose:** Define formal requirements for enhancing the /problem-solving skill with adversarial strategy capabilities, covering functional, non-functional, and integration requirements with full traceability to EN-302 (ADR-EPIC002-001) and EN-303 (situational mapping)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this requirements document delivers |
| [Functional Requirements](#functional-requirements) | What the enhanced skill MUST do |
| [Non-Functional Requirements](#non-functional-requirements) | Quality attributes and constraints |
| [Integration Requirements](#integration-requirements) | How the enhanced skill integrates with EN-403/EN-404 enforcement hooks |
| [Backward Compatibility Requirements](#backward-compatibility-requirements) | What MUST NOT break |
| [Traceability Matrix](#traceability-matrix) | Mapping to EN-302, EN-303, and barrier-2 handoff |
| [References](#references) | Source citations |

---

## Summary

This document formalizes the requirements for enhancing Jerry's /problem-solving skill to integrate the 10 selected adversarial strategies (ADR-EPIC002-001) into the ps-critic agent architecture. The requirements are organized into four categories:

1. **Functional Requirements (FR-304-xxx):** What the enhanced ps-critic agent and skill MUST do -- adversarial modes, invocation protocol, mode selection, multi-mode composition, quality scoring integration.
2. **Non-Functional Requirements (NFR-304-xxx):** Quality attributes -- token efficiency, backward compatibility, determinism, P-003 compliance, context rot resilience.
3. **Integration Requirements (IR-304-xxx):** How the enhanced skill connects to the EN-403/EN-404 enforcement architecture -- hook trigger points, L2-REINJECT tags, quality-enforcement.md SSOT, ContentBlock priority system.
4. **Backward Compatibility Requirements (BC-304-xxx):** What existing behavior MUST be preserved.

All requirements trace to source artifacts: ADR-EPIC002-001 (strategy selection), EN-303 TASK-001 (context taxonomy), EN-303 TASK-003 (strategy profiles), EN-303 TASK-004 (decision tree), and the barrier-2 ENF-to-ADV handoff.

---

## Functional Requirements

### FR-304-001: Adversarial Mode Support

The ps-critic agent specification SHALL support 10 named adversarial modes, one per selected strategy from ADR-EPIC002-001:

| Mode Name | Strategy | ADR Rank | Requirement |
|-----------|----------|----------|-------------|
| `self-refine` | S-010 Self-Refine | 7 | ps-critic SHALL support a self-refine mode that performs iterative self-improvement on the creator's output |
| `steelman` | S-003 Steelman Technique | 2 | ps-critic SHALL support a steelman mode that reconstructs the artifact's argument in its strongest form before critique |
| `inversion` | S-013 Inversion Technique | 3 | ps-critic SHALL support an inversion mode that generates anti-pattern checklists and failure criteria |
| `constitutional` | S-007 Constitutional AI Critique | 4 | ps-critic SHALL support a constitutional mode that evaluates the artifact against Jerry's codified rules and principles |
| `devils-advocate` | S-002 Devil's Advocate | 5 | ps-critic SHALL support a devils-advocate mode that systematically challenges assumptions and conclusions |
| `pre-mortem` | S-004 Pre-Mortem Analysis | 6 | ps-critic SHALL support a pre-mortem mode that imagines future failure scenarios through temporal reframing |
| `fmea` | S-012 FMEA | 8 | ps-critic SHALL support an fmea mode that performs systematic failure mode and effects analysis |
| `chain-of-verification` | S-011 Chain-of-Verification | 9 | ps-critic SHALL support a chain-of-verification mode that isolates and verifies factual claims |
| `llm-as-judge` | S-014 LLM-as-Judge | 1 | ps-critic SHALL support an llm-as-judge mode that performs rubric-based quality scoring |
| `red-team` | S-001 Red Team Analysis | 10 | ps-critic SHALL support a red-team mode that simulates adversary behavior to identify vulnerabilities |

**Source:** ADR-EPIC002-001 Section "The 10 Selected Strategies"; EN-304 AC-2, AC-3.

### FR-304-002: Mode Components

Each adversarial mode SHALL include the following components:

| Component | Description | Requirement Level |
|-----------|-------------|-------------------|
| **Name** | Unique kebab-case identifier (e.g., `red-team`) | REQUIRED |
| **Prompt Template** | Strategy-specific prompt that configures ps-critic behavior for that mode | REQUIRED |
| **Evaluation Criteria** | Mode-specific quality dimensions and weights | REQUIRED |
| **Output Format** | Structured output schema specific to the mode's analysis type | REQUIRED |
| **Applicability Metadata** | Context dimensions from EN-303 TASK-001 (target type affinity, phase applicability, criticality mapping) | REQUIRED |
| **Token Budget** | Per-invocation token cost estimate from EN-303 TASK-003 | REQUIRED |
| **Pairing Guidance** | SYN/COM/TEN relationships with other modes from EN-303 TASK-003 | REQUIRED |

**Source:** EN-304 AC-3; EN-303 TASK-003 profile template.

### FR-304-003: Explicit Mode Selection

The invocation protocol SHALL support explicit mode selection by the user or orchestrator:

- **Syntax:** `ps-critic --mode <mode-name>` (e.g., `ps-critic --mode red-team`)
- **Validation:** If a mode name is not recognized, the invocation SHALL fail with a clear error listing available modes
- **Multiple modes:** `ps-critic --mode steelman,devils-advocate,llm-as-judge` SHALL execute modes in the specified order

**Source:** EN-304 AC-4.

### FR-304-004: Automatic Mode Selection

The invocation protocol SHALL support automatic mode selection using the EN-303 TASK-004 decision tree:

- **Input:** The 8-dimension context vector (criticality, phase, target type, maturity, team composition, enforcement layer availability, platform context, token budget state)
- **Process:** Apply auto-escalation rules (AE-001 through AE-006) per EN-303 TASK-004, then traverse the decision tree to determine the strategy set
- **Output:** An ordered list of modes to execute, with delivery mechanism annotations
- **Determinism:** Given identical context inputs, automatic selection SHALL always produce the identical mode set (EN-303 TASK-004 Design Properties: deterministic, O(1) traversal)

**Source:** EN-304 AC-5; EN-303 TASK-004 Input Schema and Auto-Escalation Rules.

### FR-304-005: Multi-Mode Pipeline

The invocation protocol SHALL support multi-mode pipelines where multiple adversarial modes execute in sequence:

- **Sequencing:** Modes SHALL execute in the order specified by the decision tree or explicit invocation, respecting SYN pairing guidance from EN-303 TASK-003 (e.g., S-003 steelman BEFORE S-002 devils-advocate)
- **Output chaining:** The output of one mode SHALL be available as context input to the next mode in the pipeline
- **Score aggregation:** When S-014 llm-as-judge is included in the pipeline, its score SHALL be the authoritative quality score for the cycle
- **Pipeline abort:** If any mode produces a BLOCK-level finding (criticality escalation), the pipeline SHALL halt and escalate per FR-304-011

**Source:** EN-304 AC-6; EN-303 TASK-003 consolidated pairing reference (14 SYN + 29 COM + 2 TEN = 45 pairs).

### FR-304-006: Criticality-Strategy Mapping

The ps-critic agent SHALL implement the criticality-to-strategy mapping from EN-303 TASK-001:

| Criticality | Required Strategies | Optional Strategies |
|-------------|--------------------|--------------------|
| C1 | S-010 | S-003, S-014 |
| C2 | S-007, S-002, S-014 | S-003, S-010 |
| C3 | S-007, S-002, S-014, S-004, S-012, S-013 | S-003, S-010, S-011 |
| C4 | All 10 strategies | None -- all deployed |

**Source:** EN-303 TASK-001 "Strategy Allocation by Criticality"; EN-303 TASK-004 Decision Tree: Primary Path.

### FR-304-007: Auto-Escalation Integration

The mode selection logic SHALL implement the 6 auto-escalation rules from EN-303 TASK-004:

| Rule | Condition | Effect |
|------|-----------|--------|
| AE-001 | Artifact modifies `docs/governance/JERRY_CONSTITUTION.md` | Escalate to C3 minimum |
| AE-002 | Artifact modifies any file in `.claude/rules/` | Escalate to C3 minimum |
| AE-003 | Artifact is a new or modified ADR | Escalate to C3 minimum |
| AE-004 | Artifact modifies existing baselined ADR | Escalate to C4 |
| AE-005 | Artifact modifies security-relevant code | Escalate to C3 minimum |
| AE-006 | Token budget is EXHAUST and criticality is C3+ | Mandatory human escalation flag |

**Precedence Rule (PR-001):** Auto-escalation overrides phase downgrade. If criticality was elevated by AE-001 through AE-005, phase modifiers SHALL NOT reduce the criticality below the auto-escalated level.

**Source:** EN-303 TASK-004 Auto-Escalation Rules.

### FR-304-008: Quality Score Tracking

The ps-critic agent SHALL track quality scores across iterations using S-014 LLM-as-Judge:

- **Score format:** 0.00-1.00 numeric score with dimension-level breakdown
- **Quality threshold:** >= 0.92 (HARD rule H-13 from EN-404)
- **Iteration tracking:** Scores from each iteration SHALL be recorded to enable quality trend analysis
- **Anti-leniency calibration:** S-014 scoring SHALL include anti-leniency bias instructions (HARD rule H-16 from EN-404; ContentBlock `leniency-calibration`)

**Source:** EN-404 HARD rules H-13, H-15, H-16; barrier-2 handoff ContentBlock system.

### FR-304-009: Creator-Critic-Revision Cycle

The ps-critic agent SHALL support the 3-iteration minimum creator-critic-revision cycle (HARD rule H-14):

| Iteration | Creator Role | Critic Role | Strategy Application |
|-----------|-------------|-------------|---------------------|
| 1 (Create) | Produce initial artifact | N/A | Creator applies S-010 self-refine during creation |
| 2 (Critique) | N/A | Execute strategy battery per criticality | Full mode pipeline per C1-C4 allocation |
| 3 (Revise) | Revise based on critique | Score revised output | Creator uses S-010; Critic applies S-014 scoring + S-011 CoVe for verification |

**Extended cycle:** If quality threshold is not met after 3 iterations, the orchestrator MAY invoke additional iterations, subject to the circuit breaker (max iterations configurable, default 3 per current ps-critic spec).

**Source:** EN-303 TASK-004 Creator-Critic-Revision Cycle Mapping; EN-404 H-14.

### FR-304-010: Phase-Strategy Interaction

The mode selection logic SHALL respect phase-strategy interaction guidance from EN-303 TASK-001:

| Phase | Recommended Strategies | Cautionary Strategies |
|-------|----------------------|----------------------|
| PH-EXPLORE | S-013, S-004, S-003 | S-001 (premature pressure), S-007 (no constitution yet), S-014 (no rubric yet) |
| PH-DESIGN | S-003, S-002, S-012, S-013, S-004, S-001 | None -- full palette appropriate |
| PH-IMPL | S-007, S-011, S-010, S-014, S-012 | S-004 (too late), S-003 (less value for concrete code) |
| PH-VALID | S-014, S-007, S-011 | S-013 (generative output adds noise), S-004 (too late) |
| PH-MAINT | S-012, S-011, S-007, S-014 | S-001 (full red team expensive for maintenance) |

**Source:** EN-303 TASK-001 Phase-Strategy Interaction Matrix.

### FR-304-011: Escalation Protocol

The ps-critic agent SHALL support escalation to human review under the following conditions:

| Condition | Action |
|-----------|--------|
| C4 criticality detected | MANDATORY human involvement (P-020) |
| AE-006 triggered (EXHAUST + C3+) | MANDATORY human escalation flag |
| ENF-MIN-002 triggered (ENF-MIN + C3+) | MANDATORY human escalation flag |
| TEAM-SINGLE + C3 | Escalate to TEAM-MULTI or TEAM-HIL |
| TEAM-SINGLE + C4 | NOT PERMITTED. MUST escalate. |
| Quality score < 0.80 after 3 iterations | ESCALATE to user for decision |

**Source:** EN-303 TASK-004 Escalation Decision Logic (ESC-001 through ESC-007).

### FR-304-012: Token Budget Adaptation

The mode selection logic SHALL adapt strategy sets based on token budget state per EN-303 TASK-004:

| Budget State | Definition | Adaptation |
|-------------|-----------|------------|
| TOK-FULL | > 20,000 tokens remaining | Full strategy set per criticality |
| TOK-CONST | 5,000-20,000 tokens remaining | Reduced set per EN-303 TASK-004 TOK-CONST table |
| TOK-EXHAUST | < 5,000 tokens remaining | Minimal set; mandatory human escalation at C3+; session end at C4 |

**Context rot warning:** When session token count exceeds 20K, a context rot warning SHALL be appended to strategy recommendations.

**Source:** EN-303 TASK-004 Decision Tree: Token Budget Adaptation.

---

## Non-Functional Requirements

### NFR-304-001: P-003 Compliance

All adversarial modes SHALL operate within the orchestrator-worker pattern (max ONE level: orchestrator -> worker). No mode SHALL spawn recursive subagents. The ps-critic agent is invoked by the orchestrator (main context) and returns results; it does not invoke other agents.

**Source:** Jerry Constitution P-003 (HARD); ADR-EPIC002-001 Compliance section.

### NFR-304-002: Token Efficiency

Each adversarial mode SHALL conform to the token budget established in EN-303 TASK-003:

| Mode | Token Budget | Tier |
|------|-------------|------|
| `self-refine` (S-010) | ~2,000 | Ultra-Low |
| `steelman` (S-003) | ~1,600 | Ultra-Low |
| `inversion` (S-013) | ~2,100 | Ultra-Low |
| `constitutional` (S-007) | ~8,000-16,000 | Medium |
| `devils-advocate` (S-002) | ~4,600 | Low |
| `pre-mortem` (S-004) | ~5,600 | Low |
| `fmea` (S-012) | ~9,000 | Medium |
| `chain-of-verification` (S-011) | ~4,500 | Low |
| `llm-as-judge` (S-014) | ~2,000 | Ultra-Low |
| `red-team` (S-001) | ~6,500 | Low-Medium |

**Cumulative budgets per criticality:**
- C1: 2,000-5,600 tokens
- C2: 14,600-18,200 tokens
- C3: 31,300-38,900 tokens
- C4: ~50,300 tokens

**Source:** EN-303 TASK-003 per-profile Token Budget sections; EN-303 TASK-004 token budget adaptation.

### NFR-304-003: Deterministic Selection

Given identical context inputs (8-dimension vector), the automatic mode selection SHALL always produce the identical mode set. The selection algorithm SHALL have O(1) traversal complexity (fixed-depth lookup, no iteration).

**Source:** EN-303 TASK-004 Design Properties.

### NFR-304-004: Context Rot Resilience

The adversarial mode architecture SHALL degrade gracefully under context rot:

- Modes with L2/L3 enforcement delivery SHALL remain effective beyond 50K tokens
- Modes with L1-only delivery SHALL include context rot warnings when session exceeds 20K tokens
- The ContentBlock system (barrier-2 handoff) provides 600 tokens/prompt reinforcement for critical strategies

**Source:** Barrier-2 ENF-to-ADV handoff, defense-in-depth compensation chain.

### NFR-304-005: Platform Portability

The adversarial mode architecture SHALL support graceful degradation across platforms:

| Platform | Available Layers | Enforcement Level |
|----------|-----------------|-------------------|
| Claude Code (full) | L1 + L2 + L3 + L4 + L5 + Process | HIGH |
| Claude Code (hooks disabled) | L1 + L5 + Process | MODERATE |
| Non-Claude Code LLM | L1 + L5 + Process | MODERATE |
| No CI/pre-commit | L1 only | LOW |

No adversarial strategy SHALL be inoperable on any platform. Capability degrades; availability does not.

**Source:** Barrier-2 ENF-to-ADV handoff, Graceful Degradation Matrix.

### NFR-304-006: Quality Gate Integration

The quality threshold for all adversarial review cycles SHALL be >= 0.92 (HARD rule H-13). This threshold SHALL be sourced from the `quality-enforcement.md` SSOT file, not hardcoded in the ps-critic specification.

**Source:** EN-404 HARD rule H-13; barrier-2 handoff quality-enforcement.md SSOT.

### NFR-304-007: Documentation Requirements

All mode specifications SHALL include navigation tables with anchor links per Jerry markdown navigation standards (NAV-001 through NAV-006). All mode documentation SHALL include traceability to source requirements and ADR references.

**Source:** `.context/rules/markdown-navigation-standards.md`.

---

## Integration Requirements

### IR-304-001: C1-C4 Criticality Trigger Integration

The ps-critic adversarial modes SHALL integrate with the PromptReinforcementEngine (EN-403) criticality assessment:

- C1-C4 criticality levels from the UserPromptSubmit hook SHALL inform automatic mode selection
- The `_assess_criticality()` method output SHALL be consumable by the decision tree (FR-304-004)
- Strategy activation sets per criticality level SHALL match the ContentBlock selection in the PromptReinforcementEngine

**Source:** Barrier-2 handoff, "For EN-304 (Strategy-Skill Integration)" integration point table.

### IR-304-002: L2-REINJECT Tag Authoring

The /problem-solving skill documentation SHALL define L2-REINJECT tags for adversarial strategy reinforcement content:

- **Tag format:** `<!-- L2-REINJECT: rank=N, tokens=NN, content="..." -->`
- **Location:** Tags SHALL be placed in `.context/rules/quality-enforcement.md` or appropriate rule files
- **Content:** Strategy-specific reinforcement (e.g., "S-014 LLM-as-Judge scoring REQUIRED for all C2+ artifacts")
- **Budget:** Content SHALL fit within the 90-token buffer remaining in the 600-token L2 budget (510 of 600 currently allocated)

**Source:** Barrier-2 handoff, L2-REINJECT Tag Format; EN-403 TASK-002 ContentBlock system.

### IR-304-003: SSOT File Consumption

The ps-critic agent SHALL source the following values from `quality-enforcement.md` (SSOT):

| Value | SSOT Key | Used By |
|-------|----------|---------|
| Quality threshold | 0.92 | Quality gate determination in S-014 scoring |
| C1-C4 definitions | Criticality framework | Automatic mode selection |
| Strategy encodings | 6 adversarial strategy encodings (~119 tokens) | SessionStart context, L1 encoding |
| Iteration cycle count | Minimum 3 | Creator-critic-revision cycle |
| Tier vocabulary | HARD/MEDIUM/SOFT word lists | Mode output categorization |

**Source:** Barrier-2 handoff, quality-enforcement.md SSOT description.

### IR-304-004: SessionStart Strategy Listing

The /problem-solving skill SHALL ensure all 10 adversarial strategies are correctly listed in the SessionQualityContextGenerator output:

- The `<adversarial-strategies>` XML section in SessionStart (~120 tokens) SHALL enumerate all 10 strategies with their mode names
- Strategy listing SHALL use the canonical names from ADR-EPIC002-001

**Source:** Barrier-2 handoff, EN-403 TASK-004 SessionStart Hook design.

### IR-304-005: ContentBlock Priority Integration

The ps-critic mode definitions SHALL align with the ContentBlock priority system in the PromptReinforcementEngine:

| ContentBlock | Priority | Relevant Mode |
|-------------|----------|---------------|
| `quality-gate` | 1 | `llm-as-judge` (S-014) |
| `constitutional-principles` | 2 | `constitutional` (S-007) |
| `self-review` | 3 | `self-refine` (S-010) |
| `scoring-requirement` | 4 | `llm-as-judge` (S-014) |
| `steelman` | 5 | `steelman` (S-003) |
| `leniency-calibration` | 6 | `llm-as-judge` (S-014) |
| `deep-review` | 7 | Multi-mode pipeline activation |

**Source:** Barrier-2 handoff, ContentBlock System table.

### IR-304-006: PreToolEnforcementEngine Coordination

The ps-critic adversarial modes SHALL coordinate with the PreToolEnforcementEngine (L3 gating):

- Governance file escalation (C3/C4 triggers) from `PreToolEnforcementEngine.evaluate_write()` and `evaluate_edit()` SHALL feed into the auto-escalation rules (FR-304-007)
- The `EnforcementDecision.criticality_escalation` field SHALL be consumed by the mode selection logic

**Source:** Barrier-2 handoff, EN-403 TASK-003 PreToolUse Hook design.

---

## Backward Compatibility Requirements

### BC-304-001: Default Behavior Preservation

When invoked without an explicit `--mode` parameter and without context for automatic selection, ps-critic SHALL behave identically to the current v2.2.0 specification:

- Default quality dimensions: Completeness (0.25), Accuracy (0.25), Clarity (0.20), Actionability (0.15), Alignment (0.15)
- Default circuit breaker: max 3 iterations, improvement threshold 0.10, acceptance threshold 0.85
- Default output format: L0/L1/L2 levels with quality score

**Source:** Current ps-critic.md v2.2.0 specification.

### BC-304-002: Existing Workflow Compatibility

All existing /problem-solving workflows that invoke ps-critic SHALL continue to function without modification:

- The Generator-Critic Loop (Pattern 6 in PLAYBOOK.md v3.3.0) SHALL work with the default mode
- Session context validation (WI-SAO-002) schema SHALL remain backward-compatible
- Critique output file path convention SHALL be preserved

**Source:** Current PLAYBOOK.md v3.3.0 Pattern 6; current ps-critic.md session context validation.

### BC-304-003: Quality Threshold Migration

The acceptance threshold SHALL migrate from 0.85 (current default) to 0.92 (HARD rule H-13) when adversarial modes are active:

- **Default mode (no explicit adversarial invocation):** Threshold remains 0.85 for backward compatibility
- **Adversarial mode (explicit or automatic selection):** Threshold becomes 0.92 per quality-enforcement.md SSOT
- **Transition:** Documentation SHALL clearly communicate this distinction

**Source:** Current ps-critic.md circuit breaker (0.85); EN-404 H-13 (0.92).

---

## Traceability Matrix

### Requirements to Source Artifacts

| Requirement | ADR-EPIC002-001 | EN-303 TASK-001 | EN-303 TASK-003 | EN-303 TASK-004 | Barrier-2 Handoff | EN-304 AC |
|-------------|-----------------|-----------------|-----------------|-----------------|-------------------|-----------|
| FR-304-001 | Selected strategies | -- | Strategy profiles | -- | -- | AC-2, AC-3 |
| FR-304-002 | -- | -- | Profile template | -- | -- | AC-3 |
| FR-304-003 | -- | -- | -- | -- | -- | AC-4 |
| FR-304-004 | -- | Context taxonomy | -- | Decision tree | -- | AC-5 |
| FR-304-005 | -- | -- | Pairing reference | -- | -- | AC-6 |
| FR-304-006 | Quality layers | Strategy allocation | -- | Primary path | -- | AC-2 |
| FR-304-007 | -- | -- | -- | Auto-escalation rules | -- | AC-5 |
| FR-304-008 | S-014 role | -- | S-014 profile | -- | ContentBlock system | AC-3 |
| FR-304-009 | 3-iteration cycle | -- | -- | Cycle mapping | H-14 | AC-8 |
| FR-304-010 | -- | Phase-strategy matrix | Phase guidance | Phase modifiers | -- | AC-5 |
| FR-304-011 | P-020 | -- | -- | Escalation logic | -- | AC-5 |
| FR-304-012 | -- | -- | Token budgets | Budget adaptation | -- | AC-5 |
| NFR-304-001 | P-003 compliance | -- | -- | -- | -- | AC-9 |
| NFR-304-002 | Token budgets | -- | Token budgets | -- | Token budget summary | AC-9 |
| NFR-304-003 | -- | -- | -- | Design properties | -- | AC-5 |
| NFR-304-004 | -- | -- | -- | Context rot warning | Defense-in-depth chain | AC-9 |
| NFR-304-005 | -- | -- | Platform portability | Platform adaptation | Graceful degradation | AC-9 |
| NFR-304-006 | >= 0.92 threshold | -- | -- | -- | H-13, SSOT | AC-9 |
| IR-304-001 | -- | C1-C4 framework | -- | -- | C1-C4 triggers | AC-5 |
| IR-304-002 | -- | -- | -- | -- | L2-REINJECT tags | AC-7 |
| IR-304-003 | -- | -- | -- | -- | SSOT description | AC-7 |
| IR-304-004 | Strategy list | -- | -- | -- | SessionStart design | AC-7 |
| IR-304-005 | -- | -- | -- | -- | ContentBlock system | AC-7 |
| IR-304-006 | -- | -- | -- | -- | PreToolUse design | AC-7 |
| BC-304-001 | -- | -- | -- | -- | -- | AC-9 |
| BC-304-002 | -- | -- | -- | -- | -- | AC-9 |
| BC-304-003 | -- | -- | -- | -- | H-13 | AC-9 |

### Requirements to EN-304 Acceptance Criteria

| AC | Requirement Coverage |
|----|---------------------|
| AC-1 (Requirements document) | This document (TASK-001) |
| AC-2 (10 adversarial modes) | FR-304-001, FR-304-006 |
| AC-3 (Mode components) | FR-304-002, FR-304-008 |
| AC-4 (Explicit mode selection) | FR-304-003 |
| AC-5 (Automatic mode selection) | FR-304-004, FR-304-007, FR-304-010, FR-304-011, FR-304-012 |
| AC-6 (Multi-mode pipelines) | FR-304-005 |
| AC-7 (SKILL.md documentation) | IR-304-002, IR-304-003, IR-304-004, IR-304-005 |
| AC-8 (PLAYBOOK.md procedures) | FR-304-009 |
| AC-9 (Backward compatibility) | NFR-304-001 through NFR-304-006, BC-304-001 through BC-304-003 |
| AC-10 (Code review) | -- (TASK-007 scope) |
| AC-11 (Adversarial review) | -- (TASK-008 scope) |
| AC-12 (Requirements verification) | -- (TASK-009 scope) |
| AC-13 (Final validation) | -- (TASK-010 scope) |

---

## References

| # | Citation | Relevance |
|---|----------|-----------|
| 1 | ADR-EPIC002-001 (EN-302 TASK-005) | Authoritative selection of 10 adversarial strategies, composite scores, P-003 compliance |
| 2 | EN-303 TASK-001 (Context Taxonomy) | 8-dimension taxonomy, strategy affinity tables, criticality allocation |
| 3 | EN-303 TASK-003 (Strategy Profiles) | Per-strategy applicability profiles, token budgets, pairing reference, enforcement layer mapping |
| 4 | EN-303 TASK-004 (Decision Tree) | Deterministic selection algorithm, auto-escalation rules, budget adaptation, cycle mapping |
| 5 | Barrier-2 ENF-to-ADV Handoff | Hook designs, ContentBlock system, L2-REINJECT tags, SSOT, HARD rules H-01 through H-24 |
| 6 | EN-304 Enabler Entity | Acceptance criteria, task decomposition, agent assignments |
| 7 | ps-critic.md v2.2.0 | Current agent specification (baseline for backward compatibility) |
| 8 | SKILL.md v2.1.0 | Current /problem-solving skill documentation |
| 9 | PLAYBOOK.md v3.3.0 | Current /problem-solving playbook (Pattern 6: Generator-Critic Loop) |

---

*Document ID: FEAT-004:EN-304:TASK-001*
*Agent: ps-architect-304*
*Created: 2026-02-13*
*Status: Draft*
