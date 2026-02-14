# TASK-004: Strategy Selection Decision Tree

<!--
DOCUMENT-ID: FEAT-004:EN-303:TASK-004
VERSION: 1.1.0
AGENT: ps-architect
DATE: 2026-02-13
STATUS: Complete
PARENT: EN-303 (Situational Applicability Mapping)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
ACTIVITY: DESIGN
REQUIREMENTS: FR-010, FR-011, NFR-006, NFR-007
TARGET-ACS: 4, 5, 6, 13
INPUT: TASK-001 (context taxonomy), TASK-003 (strategy profiles), ADR-EPIC002-001, Barrier-1 ENF-to-ADV
-->

> **Version:** 1.1.0
> **Agent:** ps-architect
> **Quality Target:** >= 0.92
> **Purpose:** Build a deterministic decision tree that takes context inputs (from TASK-001 taxonomy) and recommends adversarial strategy sets, with enforcement layer integration, token budget optimization, platform adaptation, and escalation paths

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What the decision tree delivers and its design properties |
| [Design Properties](#design-properties) | Determinism, completeness, minimality, traceability guarantees |
| [Input Schema](#input-schema) | Context dimensions consumed by the decision tree |
| [Auto-Escalation Rules](#auto-escalation-rules) | Rules that override criticality determination before tree traversal, including PR-001 precedence rule and ENF-MIN override rules |
| [Decision Tree: Primary Path](#decision-tree-primary-path) | The main decision tree branching on criticality (C1-C4) |
| [Decision Tree: Token Budget Adaptation](#decision-tree-token-budget-adaptation) | Budget-constrained alternatives for each criticality level |
| [Decision Tree: Platform Adaptation](#decision-tree-platform-adaptation) | Portable fallback paths for non-Claude-Code environments |
| [Creator-Critic-Revision Cycle Mapping](#creator-critic-revision-cycle-mapping) | Strategy assignments per iteration of the review cycle |
| [Escalation Decision Logic](#escalation-decision-logic) | When and how to escalate to human review |
| [Fallback for Ambiguous Contexts](#fallback-for-ambiguous-contexts) | Handling uncertain or unlisted dimension values |
| [Enforcement Layer Integration](#enforcement-layer-integration) | How the tree maps to the 5-layer architecture |
| [Worked Examples](#worked-examples) | 5 representative scenarios spanning C1-C4 |
| [Determinism Verification](#determinism-verification) | Proof that identical inputs produce identical outputs |
| [Completeness Verification](#completeness-verification) | Proof that every context combination has a recommendation |
| [Traceability](#traceability) | Requirements and acceptance criteria coverage |
| [References](#references) | Source citations |

---

## Summary

This document defines a deterministic decision tree that accepts context inputs (8 dimensions from TASK-001) and produces strategy set recommendations grounded in the per-strategy applicability profiles (TASK-003). The tree is designed for O(1) traversal -- fixed-depth lookup through the primary branching dimension (criticality C1-C4) with secondary modifiers for token budget, platform, and phase.

The tree produces:
1. **A base strategy set** -- the strategies to apply for the given criticality level
2. **A delivery mechanism** -- how each strategy is enforced (enforcement layer mapping)
3. **Token-budget-adapted variants** -- reduced strategy sets for constrained budgets
4. **Platform-adapted variants** -- portable fallback delivery for non-Claude-Code environments
5. **Iteration-specific assignments** -- which strategies apply at each step of the creator-critic-revision cycle
6. **Escalation triggers** -- conditions requiring human review

---

## Design Properties

| Property | Guarantee | Verification |
|----------|-----------|-------------|
| **Deterministic** | Same inputs always produce same outputs. No randomness, no iteration, no model-dependent branching. | [Determinism Verification](#determinism-verification) |
| **Complete** | Every valid context combination produces a recommendation. No dead-end branches. | [Completeness Verification](#completeness-verification) |
| **Minimal** | No redundant branches. Secondary dimensions modify the base recommendation, not replicate it. | Tree structure inspection |
| **Traceable** | Every recommendation traces to TASK-003 profiles and ADR-EPIC002-001 quality layers. | [Traceability](#traceability) |
| **O(1)** | Fixed-depth traversal: 1 primary branch (criticality) + up to 3 modifier lookups (budget, platform, phase). No iteration. | Tree depth = 4 maximum |

---

## Input Schema

The decision tree consumes the following inputs from the TASK-001 context taxonomy:

| Input | Code | Values | Role in Tree |
|-------|------|--------|-------------|
| **Decision Criticality** | CRIT | C1, C2, C3, C4 | **Primary branch** (root dimension) |
| **Token Budget State** | TOK | FULL, CONST, EXHAUST | **Modifier 1** -- adapts strategy set for budget |
| **Platform Context** | PLAT | CC, CC-WIN, GENERIC | **Modifier 2** -- adapts delivery mechanism |
| **Review Phase** | PH | EXPLORE, DESIGN, IMPL, VALID, MAINT | **Modifier 3** -- adjusts strategy emphasis |
| **Review Target Type** | TGT | CODE, ARCH, REQ, RES, DEC, PROC | **Context for guidance notes** -- does not change strategy set but adds context-specific guidance |
| **Artifact Maturity** | MAT | DRAFT, REVIEW, APPR, BASE | **Gate check** -- restricts review scope for approved/baselined artifacts |
| **Team Composition** | TEAM | SINGLE, MULTI, HIL | **Capability check** -- restricts strategies requiring multi-agent for single-agent contexts |
| **Enforcement Layer Availability** | ENF | FULL, PORT, MIN | **Derived from PLAT with ENF-MIN override** -- Default: PLAT-CC/PLAT-CC-WIN -> ENF-FULL; PLAT-GENERIC -> ENF-PORT. **Override:** ENF-MIN may be explicitly specified on any platform when the environment is degraded (CI broken, hooks disabled, emergency session). See ENF-MIN Override Rules below. |

---

## Auto-Escalation Rules

These rules fire BEFORE tree traversal and may override the initial criticality determination:

| Rule | Condition | Effect | Source |
|------|-----------|--------|--------|
| **AE-001** | Artifact modifies `docs/governance/JERRY_CONSTITUTION.md` | Escalate to C3 minimum (if initially C1 or C2) | FR-011 |
| **AE-002** | Artifact modifies any file in `.claude/rules/` | Escalate to C3 minimum (if initially C1 or C2) | FR-011 |
| **AE-003** | Artifact is a new or modified ADR | Escalate to C3 minimum | TASK-001 Criticality Determination Guidelines |
| **AE-004** | Artifact modifies existing baselined ADR | Escalate to C4 | TASK-001 Criticality Determination Guidelines |
| **AE-005** | Artifact modifies security-relevant code (auth, crypto, access control) | Escalate to C3 minimum | TASK-001 Criticality Determination Guidelines |
| **AE-006** | Token budget is EXHAUST and criticality is C3+ | Add mandatory human escalation flag | Escalation Decision Logic |

**Processing order:** Apply AE-001 through AE-005 first (criticality overrides), then AE-006 (human escalation).

**Precedence Rule (PR-001): Auto-escalation overrides phase downgrade.** If criticality was elevated by AE-001 through AE-005, phase modifiers SHALL NOT reduce the criticality below the auto-escalated level. For example: if AE-002 escalates a C1 artifact to C3 (because it modifies `.claude/rules/`), and the phase is PH-EXPLORE, the PH-EXPLORE downgrade rule ("downgrade to C2") does NOT apply. The artifact remains at C3 minimum. This ensures that governance protection provided by auto-escalation is never undermined by phase-based convenience downgrades. The rationale is that auto-escalation rules encode hard governance constraints (FR-011, JERRY_CONSTITUTION), while phase modifiers encode soft workflow optimization preferences.

### ENF-MIN Override Rules

When ENF-MIN is explicitly specified (degraded environment on any platform):

| Rule | Condition | Effect |
|------|-----------|--------|
| **ENF-MIN-001** | ENF = MIN on any platform | Override default ENF derivation from PLAT. Treat delivery mechanisms as L1 only. |
| **ENF-MIN-002** | ENF = MIN AND CRIT >= C3 | Add mandatory human escalation flag (same as AE-006). |
| **ENF-MIN-003** | ENF = MIN | Apply PLAT-GENERIC portable stack treatment for all delivery mechanism lookups (L1, L5 if available, Process if available). |
| **ENF-MIN-004** | ENF = MIN | Flag strategies infeasible under ENF-MIN per TASK-003 ENF-MIN handling notes: S-004, S-012, S-001 are infeasible; S-002 and S-011 are marginally feasible. |

**Design Decision:** ENF is treated as derived from PLAT for the primary 7-dimensional decision space (4 x 3 x 3 x 5 x 6 x 4 x 3 = 12,960 combinations). ENF-MIN is handled as an explicit override that applies the ENF-MIN rules above, adding a bounded set of additional scenarios. This preserves the O(1) traversal property while ensuring ENF-MIN coverage. See TASK-001 "Design Decision -- ENF = f(PLAT)" for full rationale. The 8-dimensional total space (19,440 from TASK-001) represents the theoretical maximum; the practical decision space is 12,960 base combinations + ENF-MIN override handling.

---

## Decision Tree: Primary Path

The primary decision tree branches on criticality level, producing a base strategy set for each level. This is the path followed when TOK = FULL and PLAT = CC (full capability).

### C1: Routine (Quality Layer L0/L1)

```
CRITICALITY = C1
  |
  +-- BASE STRATEGY SET:
  |     Required: S-010 (Self-Refine)
  |     Optional: S-003 (Steelman), S-014 (LLM-as-Judge)
  |
  +-- TOKEN BUDGET: 2,000 required; 5,600 with all optional
  |
  +-- QUALITY TARGET: ~0.60 to ~0.80
  |     NOTE: Artifacts scoring 0.75-0.80 are in the C1/C2 transition zone.
  |           If quality is critical, escalate to C2 review.
  |
  +-- PHASE MODIFIER:
  |     PH-EXPLORE: S-010 only (no scoring yet)
  |     PH-DESIGN: S-010 + S-014
  |     PH-IMPL: S-010 + S-014
  |     PH-VALID: S-014 only (scoring, not refinement)
  |     PH-MAINT: S-010 + S-014
  |
  +-- MATURITY GATE:
  |     MAT-APPR / MAT-BASE: S-014 confirmation only
  |
  +-- TEAM CHECK:
        TEAM-SINGLE: Full capability (all C1 strategies are single-agent)
        TEAM-MULTI: Full capability
        TEAM-HIL: Full capability
```

### C2: Significant (Quality Layer L2 -- Target Operating Layer)

```
CRITICALITY = C2
  |
  +-- BASE STRATEGY SET:
  |     Required: S-007 (Constitutional AI), S-002 (Devil's Advocate), S-014 (LLM-as-Judge)
  |     Recommended: S-003 (Steelman), S-010 (Self-Refine)
  |
  +-- TOKEN BUDGET: 14,600 required; 18,200 with recommended
  |
  +-- QUALITY TARGET: ~0.80 to ~0.92+
  |     NOTE: The C1/C2 boundary overlaps at ~0.80 to ensure no gap.
  |           Artifacts in the 0.75-0.85 range should receive C2 review.
  |
  +-- PHASE MODIFIER:
  |     PH-EXPLORE: Downgrade to C1 (adversarial critique premature; BUT see PR-001 -- if auto-escalated, do not downgrade below escalated level)
  |     PH-DESIGN: Full C2 set + consider S-013 (Inversion)
  |     PH-IMPL: Full C2 set
  |     PH-VALID: S-007 + S-014 (compliance + scoring)
  |     PH-MAINT: S-007 + S-014 (compliance + regression)
  |
  +-- MATURITY GATE:
  |     MAT-APPR: S-007 + S-014 only (compliance confirmation)
  |     MAT-BASE: S-014 only (regression scoring)
  |
  +-- TEAM CHECK:
        TEAM-SINGLE: Replace S-002 with S-010 (self-DA is weak; use self-refine + S-007)
        TEAM-MULTI: Full capability
        TEAM-HIL: Full capability
```

### C3: Major (Quality Layer L3 -- Deep Review)

```
CRITICALITY = C3
  |
  +-- BASE STRATEGY SET:
  |     Required: S-007, S-002, S-014, S-004 (Pre-Mortem), S-012 (FMEA), S-013 (Inversion)
  |     Recommended: S-003, S-010, S-011 (CoVe)
  |
  +-- TOKEN BUDGET: 31,300 required; 38,900 with recommended
  |
  +-- QUALITY TARGET: ~0.92 to ~0.96
  |
  +-- PHASE MODIFIER:
  |     PH-EXPLORE: Downgrade to C2 (deep review premature; apply full C3 when design begins; BUT see PR-001 -- if auto-escalated, do not downgrade below escalated level)
  |     PH-DESIGN: Full C3 set (maximum value phase for deep review)
  |     PH-IMPL: Full C3 set minus S-004 (Pre-Mortem less applicable to implementation)
  |     PH-VALID: S-007 + S-014 + S-011 + S-012 (verification-heavy)
  |     PH-MAINT: S-007 + S-014 + S-012 + S-011 (regression + impact analysis)
  |
  +-- MATURITY GATE:
  |     MAT-APPR: Full C3 only if formal revision is underway; otherwise S-014 + S-007 confirmation
  |     MAT-BASE: Full review only if formally reopened; otherwise regression-only
  |
  +-- TEAM CHECK:
  |     TEAM-SINGLE: Not recommended for C3. Escalate to TEAM-MULTI or TEAM-HIL.
  |                   If forced: S-010 + S-007 + S-013 + S-014 (single-agent-capable strategies only)
  |     TEAM-MULTI: Full capability
  |     TEAM-HIL: Full capability + human domain expertise enhances S-004, S-012
  |
  +-- ESCALATION: Consider human review involvement for all C3 decisions (P-020)
```

### C4: Critical (Quality Layer L4 -- Tournament)

```
CRITICALITY = C4
  |
  +-- BASE STRATEGY SET:
  |     Required: ALL 10 strategies
  |     S-010 (Self-Refine) + S-003 (Steelman) + S-013 (Inversion) +
  |     S-007 (Constitutional AI) + S-002 (Devil's Advocate) + S-004 (Pre-Mortem) +
  |     S-012 (FMEA) + S-011 (CoVe) + S-014 (LLM-as-Judge) + S-001 (Red Team)
  |
  +-- TOKEN BUDGET: ~50,300 total
  |
  +-- QUALITY TARGET: ~0.96+
  |
  +-- PHASE MODIFIER:
  |     PH-EXPLORE: Downgrade to C3 (tournament premature for exploration; BUT see PR-001 -- if auto-escalated, do not downgrade below escalated level)
  |     PH-DESIGN: Full C4 set (primary application phase)
  |     PH-IMPL: Full C4 set (for security-critical implementation)
  |     PH-VALID: Full C4 set (all strategies for final validation)
  |     PH-MAINT: Full C4 only if change scope warrants; otherwise C3
  |
  +-- MATURITY GATE:
  |     MAT-APPR / MAT-BASE: Full C4 only if formal revision underway
  |
  +-- TEAM CHECK:
  |     TEAM-SINGLE: NOT PERMITTED for C4. MUST escalate to TEAM-MULTI + TEAM-HIL.
  |     TEAM-MULTI: Full capability
  |     TEAM-HIL: REQUIRED. Human must be involved in C4 decisions per P-020.
  |
  +-- ESCALATION: MANDATORY human involvement (P-020). Human reviews and ratifies findings.
```

---

## Decision Tree: Token Budget Adaptation

When token budget is constrained (TOK-CONST or TOK-EXHAUST), the base strategy sets are adapted:

### TOK-CONST (5,000-20,000 tokens remaining)

| Criticality | Adapted Strategy Set | Token Cost | Adaptation Rationale |
|-------------|---------------------|------------|---------------------|
| C1 | S-010 only | 2,000 | Drop optional S-003, S-014 |
| C2 | S-003 + S-014 + S-010 | 5,600 | Replace S-007 (8,000-16,000) and S-002 (4,600) with ultra-low alternatives. Sacrifice depth for budget. |
| C3 | S-003 + S-002 + S-014 + S-013 | 10,300 | Drop S-004 (5,600), S-012 (9,000), S-007 (8,000-16,000). Retain core adversarial challenge + generative criteria. **Flag: quality target may not reach 0.92.** |
| C4 | S-003 + S-002 + S-013 + S-014 + S-007 (single-pass) | ~18,300 | Drop S-004, S-012, S-011, S-001. Simplify S-007 to single-pass. **MANDATORY: escalate to human review per AE-006.** |

### TOK-EXHAUST (< 5,000 tokens remaining)

| Criticality | Adapted Strategy Set | Token Cost | Adaptation Rationale |
|-------------|---------------------|------------|---------------------|
| C1 | S-010 only (or skip review entirely) | 2,000 | Minimal self-check |
| C2 | S-003 + S-014 | 3,600 | Steelman + scoring only. **Flag: below target quality.** |
| C3 | S-014 scoring only | 2,000 | **MANDATORY: escalate to human review (AE-006). Agent review quality severely degraded.** |
| C4 | **End session. Start fresh.** | 0 | **MANDATORY: cannot perform C4 review with exhausted budget. End session to reset context window. Human review mandatory.** |

### Context Rot Warning

Per NFR-001 and R-SYS-001: when session token count exceeds 20K, add warning to all strategy recommendations:

> **CONTEXT ROT WARNING:** Session has exceeded 20K tokens. L1-dependent strategy delivery (rules encoded in `.claude/rules/`) may have 40-60% effectiveness degradation at 50K+ tokens. Prefer L2/L3/L5/Process delivery mechanisms. Consider ending session and starting fresh for high-criticality reviews.

---

## Decision Tree: Platform Adaptation

When platform context is PLAT-GENERIC (no Claude Code hooks available), delivery mechanisms shift:

### Delivery Mechanism Adaptation

| Strategy | Full Stack (PLAT-CC) | Portable Stack (PLAT-GENERIC) |
|----------|---------------------|-------------------------------|
| S-010 | L1 rule + L2 reinforcement + L4 hook | L1 rule only (subject to context rot) |
| S-003 | L1 rule + L2 reinforcement | L1 rule only |
| S-013 | L1 rule + Process | L1 rule + Process (no change) |
| S-007 | L1 rules + L3 hook + L5 tests | L1 rules + L5 tests + Process gate |
| S-002 | Process gate | Process gate (no change) |
| S-004 | Process gate | Process gate (no change) |
| S-012 | Process + L5 CI | Process + L5 CI (no change) |
| S-011 | Process + L4 hook | Process only |
| S-014 | Process + L3/L4 hooks | Process only |
| S-001 | Process + L3 hook | Process only |

### Enforcement Level Summary

| Platform | Enforcement Level | Layers Available | Key Loss |
|----------|------------------|-----------------|----------|
| PLAT-CC | HIGH | L1, L2, L3, L4, L5, Process | None |
| PLAT-CC-WIN | HIGH (with WSL caveats) | L1, L2, L3, L4, L5, Process | Potential WSL friction |
| PLAT-GENERIC | MODERATE | L1, L5, Process | L3 real-time blocking, L4 auto-validation, L2 per-prompt reinforcement |

**Key constraint:** Portable delivery at MODERATE level is sufficient for all 10 strategies. No strategy is inoperable on PLAT-GENERIC. The loss is in enforcement automation, not strategy capability.

### ENF-MIN Adaptation (Degraded Environment)

When ENF-MIN is explicitly specified (regardless of platform), delivery is restricted to L1 only:

| Strategy | ENF-MIN Delivery | Feasibility | Substitute |
|----------|------------------|-------------|-----------|
| S-010 | L1 rule (self-review instruction) | **Feasible** -- most resilient strategy under ENF-MIN | N/A |
| S-003 | L1 rule (steelman instruction) | **Feasible** -- single-pass, ultra-low cost | N/A |
| S-013 | L1 rule (inversion prompt) | **Feasible** -- single-pass generative | N/A |
| S-014 | L1 rule (rubric-based scoring) | **Feasible** -- advisory only, no Process gate | N/A |
| S-007 | L1 rule (constitutional principles) | **Feasible** -- advisory only, no enforcement gating | N/A |
| S-002 | L1 rule (critic role assignment) | **Marginally feasible** -- requires TEAM-MULTI; advisory only | S-010 (self-review) |
| S-011 | L1 rule (verification prompt) | **Marginally feasible** -- no context isolation guarantee | Human-directed verification |
| S-004 | None | **Infeasible** -- requires Process orchestration | S-013 (Inversion) as partial substitute |
| S-012 | None | **Infeasible** -- requires Process/L5 | S-013 (Inversion) as partial substitute |
| S-001 | None | **Infeasible** -- requires Process/L3 | Human-directed security review |

**ENF-MIN Adapted Strategy Sets by Criticality:**

| Criticality | ENF-MIN Strategy Set | Token Cost | Human Required? |
|-------------|---------------------|------------|-----------------|
| C1 | S-010 | 2,000 | No |
| C2 | S-010 + S-007 (advisory) + S-014 (advisory) | 12,000 | Recommended |
| C3 | S-010 + S-003 + S-013 + S-007 (advisory) + S-014 (advisory) | 15,700 | **Mandatory** (ENF-MIN-002) |
| C4 | **End session. Human review mandatory.** | 0 | **Mandatory** |

---

## Creator-Critic-Revision Cycle Mapping

Per FR-009, the decision tree supports the creator-critic-revision cycle with strategy assignments per iteration:

### 3-Iteration Cycle (Standard)

| Iteration | Role | C1 Strategies | C2 Strategies | C3 Strategies | C4 Strategies |
|-----------|------|--------------|--------------|--------------|--------------|
| **1: Create** | Creator produces artifact with self-review | S-010 | S-010 | S-010 | S-010 |
| **2: Critique** | Critic reviews artifact adversarially | S-014 (score only) | S-003 + S-002 + S-007 + S-014 | S-003 + S-002 + S-007 + S-004 + S-012 + S-013 + S-014 | All 10 strategies |
| **3: Revise** | Creator revises based on critique; Judge scores | S-010 + S-014 | S-010 + S-014 | S-010 + S-014 + S-011 (verify corrections) | S-010 + S-014 + S-011 (verify all claims) |

### Extended Cycle (C3-C4, if quality gate not met after iteration 3)

| Iteration | Role | Strategies | Trigger |
|-----------|------|-----------|---------|
| **4: Re-Critique** | Fresh critic reviews revised artifact | Repeat iteration 2 strategies | S-014 score < 0.92 after iteration 3 |
| **5: Final Revision** | Creator addresses remaining issues | S-010 + S-014 | Score still < 0.92 after iteration 4 |
| **6: Human Escalation** | Human reviews if quality gate still not met | Human review per P-020 | Score < 0.92 after iteration 5 |

### Strategy Assignment Rationale

- **Iteration 1 (Create):** Only S-010 (Self-Refine). Creator should produce the best initial version without external adversarial pressure.
- **Iteration 2 (Critique):** Full adversarial battery appropriate to criticality level. This is where most defects are identified.
- **Iteration 3 (Revise):** Creator revises + S-014 scores to verify quality improvement. S-011 (CoVe) at C3+ verifies factual corrections.
- **Iterations 4-6 (Extended):** Diminishing returns expected. If quality gate not met by iteration 5, the artifact likely needs fundamental rework, not iterative refinement.

---

## Escalation Decision Logic

### Mandatory Escalation Triggers

| Trigger | Condition | Action | Source |
|---------|-----------|--------|--------|
| **ESC-001** | Criticality = C4 | Human must review and ratify findings | P-020 (User Authority) |
| **ESC-002** | TOK = EXHAUST and CRIT >= C3 | Human must review; agent review quality severely degraded | AE-006, NFR-001 |
| **ESC-003** | Quality gate (>= 0.92) not met after 5 iterations | Human must review; iterative refinement has failed | Quality framework design |
| **ESC-004** | Artifact touches governance/constitution AND CRIT = C4 | Human must review and explicitly ratify any governance change | P-020, FR-011 |

### Recommended (Non-Mandatory) Escalation

| Trigger | Condition | Recommendation | Source |
|---------|-----------|---------------|--------|
| **ESC-005** | CRIT = C3 | Recommend human involvement; not mandatory | P-020 best practice |
| **ESC-006** | Context rot warning active (> 20K tokens) AND CRIT >= C3 | Recommend ending session and starting fresh | R-SYS-001, R-SYS-004 |
| **ESC-007** | TEAM-SINGLE AND CRIT >= C3 | Recommend escalating to TEAM-MULTI or TEAM-HIL | Team capability constraint |

---

## Fallback for Ambiguous Contexts

When context dimension values are uncertain or unlisted:

### General Fallback Rule

**When in doubt, escalate to the next higher criticality level.** Conservative escalation is always preferred over under-review.

| Ambiguity | Fallback |
|-----------|----------|
| Criticality uncertain between C1 and C2 | Apply C2 |
| Criticality uncertain between C2 and C3 | Apply C3 |
| Criticality uncertain between C3 and C4 | Apply C4 + human escalation |
| Target type unknown | Treat as TGT-DEC (broadest strategy affinity) |
| Phase unknown | Treat as PH-DESIGN (fullest strategy palette) |
| Token budget unknown | Treat as TOK-CONST (conservative budget assumption) |
| Platform unknown | Treat as PLAT-GENERIC (portable stack only) |
| Maturity unknown | Treat as MAT-DRAFT (no scope restrictions) |
| Team unknown | Treat as TEAM-MULTI (full strategy palette) |

### Novel Context Handling

If a review context has dimension values not listed in the TASK-001 taxonomy:

1. Map the novel value to the closest existing value by definition
2. Apply the fallback rule for the appropriate dimension
3. Document the novel value and recommended mapping for future taxonomy updates
4. Escalate one criticality level as a safety margin

---

## Enforcement Layer Integration

The decision tree integrates with the 5-layer enforcement architecture by specifying which layer delivers each strategy recommendation:

### Layer Firing Order per Review

```
SESSION START
  |
  L1: Load rules (constitutional principles, self-review instructions, steelman guidance)
  |
  v
EACH PROMPT
  |
  L2: Reinforce critical rules (quality target >= 0.92, self-review reminder)
  |
  v
TOOL CALL (write operation)
  |
  L3: Pre-Action Gate -- trigger S-007 constitutional check, S-014 pre-commit scoring
  |                       (Claude Code only; PLAT-GENERIC skips to L5)
  v
TOOL CALL COMPLETES
  |
  L4: Post-Action Validation -- trigger S-010 self-review, S-011 factual verification
  |                             (Claude Code only; PLAT-GENERIC relies on Process)
  v
COMMIT
  |
  L5: Pre-commit hooks + CI -- architecture tests, ruff, mypy, pytest
  |
  v
TASK CLOSURE
  |
  Process: Quality gate (V-057) requires S-014 score >= 0.92
           Evidence-based closure (V-060) requires review artifacts
           Acceptance criteria verification (V-061)
```

### Adversarial Strategy Integration Points

| Strategy | Layer Integration | Trigger Mechanism |
|----------|------------------|-------------------|
| S-010 | L0 (always-on), L4 (post-output) | L1 rule instruction + L4 hook |
| S-003 | L1 (pre-critic phase), L2 (reinforcement) | L1 rule + L2 per-prompt |
| S-013 | Process (design review phase) | Orchestrator invokes during design review |
| S-007 | L1 (principles), L3 (pre-write gate) | L1 rules loaded at session; L3 hook triggers before writes |
| S-002 | Process (critic step) | Orchestrator invokes during creator-critic-revision cycle |
| S-004 | Process (design review phase) | Orchestrator invokes during design review for C3+ |
| S-012 | Process (risk analysis phase), L5 (CI checklist) | Orchestrator invokes; CI verifies checklist |
| S-011 | Process (verification phase), L4 (post-output) | Orchestrator invokes; L4 hook triggers for research artifacts |
| S-014 | Process (quality gate), L3/L4 (hooks) | Process gate requires score; hooks enable automation |
| S-001 | Process (security review gate), L3 (security-tagged) | Orchestrator invokes for C3+ architecture/security; L3 hook for tagged files |

---

## Worked Examples

### Example 1: C1 Routine -- Code Change Following Established Pattern

**Context:**
- CRIT: C1 (routine), TGT: CODE, PH: IMPL, MAT: DRAFT, TEAM: SINGLE, PLAT: CC, TOK: FULL

**Auto-escalation check:** No governance files modified. No security code. No ADR. -> C1 stands.

**Tree traversal:**
1. CRIT = C1 -> Base set: S-010 (required), S-003 + S-014 (optional)
2. TOK = FULL -> No budget adaptation needed
3. PLAT = CC -> Full enforcement stack
4. PH = IMPL -> S-010 + S-014

**Recommendation:** S-010 (Self-Refine) + S-014 (LLM-as-Judge)
**Token cost:** ~4,000
**Delivery:** L1 rule (self-review instruction) + L4 hook (post-output quality check)
**Cycle:** Iteration 1: S-010 self-review. Iteration 2: S-014 scoring. If >= 0.75, done.

### Example 2: C2 Standard -- New Feature Implementation

**Context:**
- CRIT: C2 (significant), TGT: CODE, PH: IMPL, MAT: DRAFT, TEAM: MULTI, PLAT: CC, TOK: FULL

**Auto-escalation check:** No governance files. -> C2 stands.

**Tree traversal:**
1. CRIT = C2 -> Base set: S-007, S-002, S-014 (required) + S-003, S-010 (recommended)
2. TOK = FULL -> No budget adaptation
3. PLAT = CC -> Full enforcement stack
4. PH = IMPL -> Full C2 set

**Recommendation:** S-010 + S-003 + S-007 + S-002 + S-014
**Token cost:** ~18,200
**Delivery:** L1 rules + L2 reinforcement + L3 pre-write constitutional check + Process quality gate
**Cycle:** Iteration 1: Creator + S-010. Iteration 2: S-003 + S-002 + S-007 + S-014. Iteration 3: S-010 + S-014. Target: >= 0.92.

### Example 3: C3 Deep Review -- Architecture Decision with Governance Impact

**Context:**
- CRIT: C2 initially, TGT: DEC, PH: DESIGN, MAT: DRAFT, TEAM: MULTI, PLAT: CC, TOK: FULL
- Artifact modifies `.claude/rules/architecture-standards.md`

**Auto-escalation check:** AE-002 fires -- artifact modifies `.claude/rules/`. Escalate to C3 minimum.

**Tree traversal:**
1. CRIT = C3 (escalated) -> Base set: S-007, S-002, S-014, S-004, S-012, S-013 (required) + S-003, S-010, S-011 (recommended)
2. TOK = FULL -> No budget adaptation
3. PLAT = CC -> Full enforcement stack
4. PH = DESIGN -> Full C3 set

**Recommendation:** All 9 strategies (S-010, S-003, S-013, S-007, S-002, S-004, S-012, S-011, S-014)
**Token cost:** ~38,900
**Delivery:** Full enforcement stack. L3 hooks gate writes. Process gates require evidence.
**Cycle:** Iteration 1: Creator + S-010. Iteration 2: S-003 steelman, then S-002 DA + S-007 constitutional + S-004 pre-mortem + S-012 FMEA + S-013 inversion + S-014 scoring. Iteration 3: Creator revision + S-010 + S-014 + S-011 verification.
**Escalation:** ESC-005 (recommended human involvement for C3).

### Example 4: C4 Critical on Non-Claude-Code Platform with Constrained Budget

**Context:**
- CRIT: C4 (constitutional amendment), TGT: DEC, PH: DESIGN, MAT: DRAFT, TEAM: HIL, PLAT: GENERIC, TOK: CONST

**Auto-escalation check:** AE-004 fires (modifying baselined ADR -> C4). AE-001 fires (governance modification). Already C4.

**Tree traversal:**
1. CRIT = C4 -> Base set: All 10 strategies
2. TOK = CONST -> Adapted set: S-003 + S-002 + S-013 + S-014 + S-007 (single-pass) = ~18,300 tokens. **ESC-002 fires: MANDATORY human escalation.**
3. PLAT = GENERIC -> Portable delivery only (L1, L5, Process)
4. PH = DESIGN -> Full available set

**Recommendation:** S-003 + S-002 + S-013 + S-014 + S-007 (single-pass). **MANDATORY HUMAN REVIEW (ESC-001, ESC-002).**
**Token cost:** ~18,300
**Delivery:** L1 rules + L5 CI + Process gates only. No hooks available.
**Cycle:** Standard 3-iteration with human review of all findings. Human ratifies final decision.
**Warning:** Budget-constrained C4 review. Quality target (0.96+) may not be achievable with reduced strategy set. Human review compensates for reduced agent review depth.

### Example 5: C2 Standard with Exhausted Budget on Claude Code

**Context:**
- CRIT: C2, TGT: CODE, PH: IMPL, MAT: REVIEW, TEAM: MULTI, PLAT: CC, TOK: EXHAUST

**Auto-escalation check:** No governance files. -> C2 stands. AE-006 does not fire (CRIT < C3).

**Tree traversal:**
1. CRIT = C2 -> Base set: S-007, S-002, S-014 (required)
2. TOK = EXHAUST -> Adapted set: S-003 + S-014 = 3,600 tokens. **Flag: below target quality.**
3. PLAT = CC -> Full enforcement stack
4. PH = IMPL -> Adapted set applies
5. MAT = REVIEW -> Adapted set compatible (incremental review)

**Recommendation:** S-003 (Steelman) + S-014 (LLM-as-Judge). **WARNING: Below target quality due to budget exhaustion.**
**Token cost:** ~3,600
**Delivery:** L1 rule + L2 reinforcement + L3/L4 hooks
**Action recommendation:** Complete this review with reduced strategy set. Consider ending session and starting fresh for remaining work to reset context window.

---

## Determinism Verification

The decision tree is deterministic because:

1. **All branches are determined by enumerated input values.** There are no probabilistic branches, no model-dependent decisions, no subjective assessments.
2. **Auto-escalation rules are deterministic.** Each rule has a binary condition (file path match or criticality threshold) and a deterministic action.
3. **Token budget adaptation is deterministic.** Each (criticality, budget-state) pair maps to exactly one strategy set.
4. **Platform adaptation is deterministic.** Each (strategy, platform) pair maps to exactly one delivery mechanism.
5. **Phase modifiers are deterministic.** Each (criticality, phase) pair maps to exactly one strategy set adjustment.

**Proof:** Given identical values for (CRIT, TOK, PLAT, PH, TGT, MAT, TEAM, ENF), the tree traversal follows the same path through the same branches and produces the same output. No randomness, no LLM-dependent branching, no iteration.

---

## Completeness Verification

The decision tree is complete because:

1. **Criticality covers all values:** C1, C2, C3, C4 all have defined base strategy sets. No criticality level is unhandled.
2. **Token budget covers all values:** FULL, CONST, EXHAUST all have defined adaptations for each criticality level.
3. **Platform covers all values:** CC, CC-WIN, GENERIC all have defined delivery mechanisms for each strategy.
4. **Phase covers all values:** EXPLORE, DESIGN, IMPL, VALID, MAINT all have defined modifiers for each criticality level.
5. **Maturity covers all values:** DRAFT, REVIEW, APPR, BASE all have defined gate checks.
6. **Team covers all values:** SINGLE, MULTI, HIL all have defined capability checks.
7. **Fallback paths exist:** Every ambiguous or unknown input maps to a conservative default.

**Proof of completeness:** The practical decision space is 4 (CRIT) x 3 (TOK) x 3 (PLAT) x 5 (PH) x 6 (TGT) x 4 (MAT) x 3 (TEAM) = **12,960 base combinations** (ENF is derived from PLAT by default; see Design Decision in Auto-Escalation Rules section). The theoretical 8-dimension space from TASK-001 is **19,440 combinations** (6 x 5 x 4 x 4 x 3 x 3 x 3 x 3). The difference (6,480) represents ENF-MIN and ENF-PORT override scenarios on platforms where the default derivation would assign a different ENF value. These are handled by the ENF-MIN Override Rules (ENF-MIN-001 through ENF-MIN-004) which modify the base recommendation without requiring additional tree branches, preserving O(1) traversal.

Each of the 12,960 base combinations resolves through:
- Primary branch on CRIT (4 paths, all defined)
- Modifier 1 on TOK (3 states per CRIT, all defined)
- Modifier 2 on PLAT (3 states per strategy, all defined)
- Modifier 3 on PH (5 states per CRIT, all defined)
- Gate check on MAT (4 states, all defined)
- Capability check on TEAM (3 states, all defined)
- ENF-MIN override (if applicable): applies ENF-MIN-001 through ENF-MIN-004

No dead-end paths exist. Every terminal node produces a strategy recommendation (possibly "end session and escalate to human" for the most constrained C4 scenarios).

---

## Traceability

### Requirements Coverage

| Requirement | How Addressed |
|-------------|--------------|
| FR-010 | Every strategy recommendation includes portable delivery mechanism in Platform Adaptation section |
| FR-011 | Auto-escalation rules AE-001 through AE-005 enforce governance artifact escalation |
| NFR-006 | Tree is documented in both human-readable tables and structured traversal algorithms suitable for agent parsing |
| NFR-007 | All recommendations trace to ADR-EPIC002-001 strategy IDs; all enforcement references cite Barrier-1 sections |

### Acceptance Criteria Coverage

| AC | How Addressed |
|----|--------------|
| AC-4 | Decision tree is complete, covering all context combinations including C1-C4 (verified in Completeness Verification) |
| AC-5 | Multi-strategy recommendations with quality layer composition demonstrated for C2 (3 strategies), C3 (6-9 strategies), C4 (all 10) |
| AC-6 | Fallback paths for ambiguous contexts (Fallback section) and platform portability fallbacks (Platform Adaptation section) both defined |
| AC-7 | Token budget awareness with adapted strategy sets for CONST and EXHAUST states; no recommendations exceed available budget |
| AC-13 | All FR/NFR requirements traced; tree properties verified for determinism and completeness |

---

## References

| # | Citation | Sections Referenced |
|---|----------|-------------------|
| 1 | ADR-EPIC002-001 (ACCEPTED) -- FEAT-004:EN-302:TASK-005 | Quality Layer Composition (L0-L4), Decision Criticality Escalation (C1-C4), token budgets, P-020 governance |
| 2 | EN-303 TASK-001 -- FEAT-004:EN-303:TASK-001 | Context taxonomy: 8 dimensions with codes and values |
| 3 | EN-303 TASK-003 -- FEAT-004:EN-303:TASK-003 | Per-strategy applicability profiles: when to use, when to avoid, enforcement mapping, criticality mapping |
| 4 | Barrier-1 ENF-to-ADV Handoff -- EPIC002-CROSSPOLL-B1-ENF-TO-ADV | 5-Layer enforcement architecture, platform constraints, defense-in-depth compensation chain, 4 RED systemic risks |
| 5 | Jerry Constitution -- docs/governance/JERRY_CONSTITUTION.md | P-003 (No Recursive Subagents), P-020 (User Authority), P-022 (No Deception) |

---

*Document ID: FEAT-004:EN-303:TASK-004*
*Agent: ps-architect*
*Created: 2026-02-13*
*Revised: 2026-02-13 (v1.1.0 -- ps-analyst-303 revision addressing critique iteration 1)*
*Status: Complete*
