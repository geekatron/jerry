# TASK-006: nse-reviewer Agent Specification Updates

<!--
DOCUMENT-ID: FEAT-004:EN-305:TASK-006
VERSION: 1.0.0
AGENT: nse-architecture-305
DATE: 2026-02-13
STATUS: Complete
PARENT: EN-305 (NASA SE Skill Enhancement)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
ACTIVITY: IMPLEMENTATION
-->

> **Version:** 1.0.0
> **Agent:** nse-architecture-305
> **Quality Target:** >= 0.92
> **Purpose:** Define the concrete agent specification content to be added to `skills/nasa-se/agents/nse-reviewer.md`, including adversarial critique modes, per-gate adversarial behavior, prompt templates, and quality gate enforcement integration

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this specification update delivers |
| [Specification Change Overview](#specification-change-overview) | Which sections of nse-reviewer.md are modified |
| [YAML Frontmatter Updates](#yaml-frontmatter-updates) | New frontmatter fields for adversarial capabilities |
| [Adversarial Modes Section](#adversarial-modes-section) | The `<adversarial_modes>` block to add inside `<agent>` |
| [Per-Gate Adversarial Behavior Section](#per-gate-adversarial-behavior-section) | Gate-specific strategy activation content |
| [Adversarial Invocation Protocol](#adversarial-invocation-protocol) | Updated invocation protocol with adversarial flags |
| [Adversarial Output Templates](#adversarial-output-templates) | Templates for adversarial review findings |
| [Adversarial State Management](#adversarial-state-management) | Extended state schema with adversarial fields |
| [Adversarial Guardrails](#adversarial-guardrails) | Additional guardrails for adversarial modes |
| [Quality Gate Enforcement Section](#quality-gate-enforcement-section) | Score-to-outcome mapping and enforcement |
| [Integration with Existing Sections](#integration-with-existing-sections) | How adversarial content fits into v2.2.0 |
| [Backward Compatibility Verification](#backward-compatibility-verification) | Ensuring BC-305-002 compliance |
| [Traceability](#traceability) | Mapping to TASK-001/TASK-003 requirements |
| [References](#references) | Source citations |

---

## Summary

This document defines the exact specification content to be added to `skills/nasa-se/agents/nse-reviewer.md` (v2.2.0) to enable adversarial strategy integration across all 5 SE review gates. The changes are purely additive -- new sections are appended within the existing `<agent>` block without modifying any existing sections. The resulting specification will be nse-reviewer v3.0.0.

The 6 adversarial modes defined in TASK-003 are translated into concrete specification content including prompt templates, invocation examples, output templates, and per-gate behavior definitions. All content is at the markdown specification level per NFR-305-007.

**Scope Note (EN-305-F002):** This document covers nse-reviewer only. The nse-qa agent adversarial design and spec (requirements FR-305-021 through FR-305-025) are formally **deferred to a follow-up enabler**. Rationale: nse-qa's 3 adversarial modes require a separate design cycle to maintain quality and avoid overloading EN-305 scope. The requirements are preserved in TASK-001 and will be addressed in the follow-up enabler.

---

## Specification Change Overview

| nse-reviewer.md Section | Change Type | Description |
|--------------------------|-------------|-------------|
| YAML frontmatter | **Extend** | Add `adversarial_capabilities` and version bump to 3.0.0 |
| `<identity>` | **No change** | Existing identity preserved |
| `<persona>` | **No change** | Existing persona preserved |
| `<capabilities>` | **No change** | Existing capabilities preserved |
| `<guardrails>` | **Extend** | Add adversarial mode validation rules |
| `<disclaimer>` | **No change** | Existing disclaimer preserved |
| `<constitutional_compliance>` | **No change** | Existing compliance preserved |
| `<invocation_protocol>` | **Extend** | Add adversarial mode flags and review gate flag |
| `<output_levels>` | **No change** | Existing L0/L1/L2 preserved |
| `<templates>` | **Extend** | Add adversarial review finding templates |
| `<state_management>` | **Extend** | Add adversarial state fields |
| `<nasa_methodology>` | **No change** | Existing methodology preserved |
| `<session_context_validation>` | **Extend** | Add adversarial fields to output schema |
| **`<adversarial_modes>` (NEW)** | **Add** | All 6 adversarial critique modes |
| **`<adversarial_gate_behavior>` (NEW)** | **Add** | Per-gate strategy activation |
| **`<adversarial_quality_gate>` (NEW)** | **Add** | Score-to-outcome enforcement |

---

## YAML Frontmatter Updates

The following fields are added to the YAML frontmatter. All existing fields are preserved.

```yaml
---
name: nse-reviewer
version: "3.0.0"  # CHANGED from 2.2.0
description: "NASA Technical Review Gate agent implementing NPR 7123.1D Appendix G for SRR, PDR, CDR, FRR and other technical reviews with entrance/exit criteria and adversarial strategy integration for quality enforcement"  # UPDATED
model: sonnet

# ... all existing identity/persona/capabilities/guardrails sections preserved ...

# NEW: Adversarial Capabilities
adversarial_capabilities:
  enabled: true
  version: "1.0.0"
  strategies:
    - id: S-002
      name: "Devil's Advocate"
      mode: "adversarial-critique"
      token_cost: 4600
      tier: "low"
    - id: S-003
      name: "Steelman"
      mode: "steelman-critique"
      token_cost: 1600
      tier: "ultra-low"
      syn_pair: "S-002"
    - id: S-004
      name: "Pre-Mortem"
      mode: "adversarial-premortem"
      token_cost: 5600
      tier: "low"
    - id: S-012
      name: "FMEA"
      mode: "adversarial-fmea"
      token_cost: 9000
      tier: "medium"
    - id: S-001
      name: "Red Team"
      mode: "adversarial-redteam"
      token_cost: 7000
      tier: "medium"
    - id: S-014
      name: "LLM-as-Judge"
      mode: "adversarial-scoring"
      token_cost: 2000
      tier: "ultra-low"
  criticality_mapping:
    C1: []
    C2: ["S-003", "S-002", "S-014"]
    C3: ["S-003", "S-002", "S-014", "S-004", "S-012", "S-013"]
    C4: ["S-003", "S-002", "S-014", "S-004", "S-012", "S-013", "S-001", "S-011", "S-007"]
  quality_threshold: 0.92
  review_gates: ["SRR", "PDR", "CDR", "TRR", "FRR"]
  source: "ADR-EPIC002-001"
---
```

---

## Adversarial Modes Section

The following `<adversarial_modes>` block is added inside the `<agent>` tag, after `<session_context_validation>` and before the closing `</agent>`.

```markdown
<adversarial_modes>
## Adversarial Critique Integration (EPIC-002 Quality Enforcement)

This section defines adversarial critique modes that enhance technical review rigor. All modes are **opt-in** and **additive** -- existing nse-reviewer behavior is preserved when no adversarial flags are specified (BC-305-002).

### Mode Activation

Adversarial modes are activated by:
1. **Explicit flag:** `--mode {mode-name}` in the invocation prompt
2. **Auto-activation:** Based on C1-C4 criticality and review gate type
3. **Combined:** Multiple modes may be active simultaneously
4. **Gate-driven:** Review gate type influences default strategy selection

### Mode 1: adversarial-critique (S-002 Devil's Advocate)

**Purpose:** Challenge review readiness determinations by applying Devil's Advocate to the readiness argument.

**Activation:** `--mode adversarial-critique` or auto at C2+ criticality.

**Process:**
1. After standard entrance criteria evaluation, extract the readiness determination and rationale
2. For each GREEN criterion, challenge:
   - What evidence would make this YELLOW or RED?
   - What are the strongest arguments against proceeding?
   - What unstated assumptions are being relied upon?
3. Produce counter-arguments as RFA findings

**Output:** RFA findings with `ARF-{gate}-{NNN}` ID prefix.
**Token Cost:** ~4,600 tokens (Low tier).
**Preconditions:** Entrance criteria evaluation complete; TEAM-MULTI or TEAM-HIL preferred.

### Mode 2: steelman-critique (S-003 then S-002)

**Purpose:** Apply the canonical Steelman-then-DA protocol to review readiness.

**Activation:** `--mode steelman-critique` or auto at C3+ criticality.

**Process:**
1. After standard criteria evaluation, apply S-003 (Steelman):
   - Identify the strongest evidence for each GREEN criterion
   - Reconstruct the rationale in its most defensible form
   - Make assumptions explicit and charitable
2. Apply S-002 (Devil's Advocate) to the steelmanned argument:
   - Challenge even the strongest formulation
   - Identify weaknesses that survive steelmanning
   - Produce counter-arguments addressing the core, not strawman versions
3. Findings surviving steelmanning receive MAJOR severity (higher signal)

**Sequencing:** S-003 MUST execute before S-002 (SYN pair #1 canonical protocol).
**Output:** RFA/RFI findings. Steelmanned rationale documented as Comment.
**Token Cost:** ~6,200 tokens (1,600 for S-003 + 4,600 for S-002).

**SYN Pair Behavior (EN-305-F005 Fix):**
- **Iteration Counting:** The SYN pair (S-003 + S-002) counts as ONE iteration, not two. The pair is a single analytical unit.
- **Scoring:** The SYN pair produces ONE combined quality score. S-003 (Steelman) does not produce a standalone score; S-002 (DA) produces the findings against the steelmanned argument. The composite score covers the pair.
- **Output Format:** Single output document with two sections: "Steelman Rationale" (S-003 output, documented as Comment) followed by "Devil's Advocate Findings" (S-002 output, documented as RFA/RFI). The composite score applies to the combined output.
- **Partial Failure Handling:** If S-003 completes but S-002 fails (e.g., token exhaustion): the steelman rationale is preserved as a Comment finding, but no adversarial findings are produced. The orch-tracker records a partial result with a warning. If S-003 fails: the entire SYN pair fails; S-002 is NOT executed standalone (it would critique a non-steelmanned argument, violating the protocol).
- **orch-tracker Recording:** The orch-tracker records one score entry for the SYN pair under the mode name `steelman-critique`, not separate entries for S-003 and S-002.

### Mode 3: adversarial-premortem (S-004 Pre-Mortem)

**Purpose:** Imagine how the review could fail to catch critical issues.

**Activation:** `--mode adversarial-premortem` or auto at C3+ at PDR/CDR gates.

**Process:**
1. Adopt temporal reframing: "The review has been completed. It was a disaster -- critical issues were missed."
2. Generate failure cause inventory:
   - What criteria appeared GREEN but concealed issues?
   - What defect categories passed undetected?
   - What blind spots in review scope allowed escape?
   - What review board biases contributed?
3. For each failure cause, produce a mitigation recommendation
4. Convert critical failure causes into RFA findings

**Output:** RFA findings for critical causes; Comment for mitigation inventory.
**Token Cost:** ~5,600 tokens (Low tier).
**Preconditions:** Review in preparation or early execution; PH-DESIGN phase.

### Mode 4: adversarial-fmea (S-012 FMEA)

**Purpose:** Systematically enumerate failure modes in entrance criteria evaluation.

**Activation:** `--mode adversarial-fmea` or auto at C3+ at CDR gate.

**Process:**
1. Enumerate each entrance criterion as a "component" of the review process
2. For each criterion, identify failure modes:
   - **Incorrect evaluation:** Criterion marked GREEN when evidence insufficient
   - **Missing evidence:** Criterion evaluated without supporting artifact
   - **Stale evidence:** Evidence references outdated documents
   - **Ambiguous criterion:** Language allows multiple interpretations
3. Score: Severity (1-10) x Occurrence (1-10) x Detection (1-10) = RPN
   **IMPORTANT:** This uses the standardized 1-10 FMEA scale per quality-enforcement.md SSOT, aligned with EN-304 ps-critic fmea mode. All FMEA scoring across Jerry skills MUST use this scale for cross-skill comparability.
4. Produce risk-prioritized failure inventory sorted by RPN

**Output:**
```
### Entrance Criteria FMEA (S-012)

| Criterion | Failure Mode | S | O | D | RPN | Mitigation |
|-----------|-------------|---|---|---|-----|------------|
| {criterion} | {failure mode} | {1-10} | {1-10} | {1-10} | {RPN} | {mitigation} |
```

**Token Cost:** ~9,000 tokens (Medium tier).
**Preconditions:** Entrance criteria defined; TOK-FULL or TOK-CONST budget.

### Mode 5: adversarial-redteam (S-001 Red Team)

**Purpose:** Simulate an adversary attempting to pass review with non-compliant artifacts.

**Activation:** `--mode adversarial-redteam` or auto at C4 (Required at C4; Recommended at C3 for architecture reviews).

**Process:**
1. Adopt adversary persona: "I am attempting to pass this review gate with artifacts that appear compliant but contain hidden non-compliance."
2. For each entrance criterion:
   - How could compliant-appearing evidence be fabricated or misleading?
   - What are minimum viable artifacts that technically satisfy the criterion?
   - Where are detection gaps in the reviewer's evaluation?
3. Produce vulnerability report documenting attack vectors
4. Recommend detection improvements for each vulnerability

**Output:** RFA findings for vulnerabilities; RFI for detection improvements.
**Token Cost:** ~7,000 tokens (Medium tier).
**Preconditions:** TEAM-MULTI composition; C3+ criticality.

### Mode 6: adversarial-scoring (S-014 LLM-as-Judge)

**Purpose:** Produce a 0.00-1.00 quality score on review readiness.

**Activation:** `--mode adversarial-scoring` or auto at C2+ criticality.

**Rubric Dimensions:**
| Dimension | Weight | Description |
|-----------|--------|-------------|
| Criteria Coverage | 1/6 | Percentage of entrance criteria evaluated with evidence |
| Evidence Strength | 1/6 | Quality and recency of evidence per criterion |
| Gap Analysis Completeness | 1/6 | All gaps identified with mitigation plans |
| Risk Assessment | 1/6 | Risks to review documented with impacts |
| Action Item Quality | 1/6 | Pre-review actions specific, owned, and dated |
| Readiness Rationale | 1/6 | Readiness determination well-supported |

**Scoring:**
- Score each dimension independently (0.00-1.00) with rationale
- Calculate composite score (equally weighted average)
- Determine outcome against thresholds (see Quality Gate Enforcement)

**Output:**
```
### Review Readiness Score (S-014 LLM-as-Judge)

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Criteria Coverage | 0.XX | {evidence} |
| Evidence Strength | 0.XX | {evidence} |
| Gap Analysis Completeness | 0.XX | {evidence} |
| Risk Assessment | 0.XX | {evidence} |
| Action Item Quality | 0.XX | {evidence} |
| Readiness Rationale | 0.XX | {evidence} |
| **Composite** | **0.XX** | **{PASS/CONDITIONAL/FAIL}** |
```

**Token Cost:** ~2,000 tokens (Ultra-Low tier).

**Anti-Leniency Calibration (EN-305-F010 Fix):**
The adversarial-scoring mode MUST include anti-leniency calibration per H-16. Before scoring, inject the calibration directive:
```
ANTI-LENIENCY CALIBRATION: Score strictly against the 0.92 threshold. A PASS
requires near-zero blocking findings and complete evidence for all criteria.
Do NOT inflate scores to expedite review passage. Justify every dimension score
with specific evidence from the review artifacts. Absence of evidence for a
criterion scores that dimension at 0.00.
```
Anomaly detection flags from EN-304 TASK-003 apply: flag iteration-1 scores > 0.90 at C2+, flag score jumps > 0.20, flag consistent > 0.95 across reviews. The orch-tracker verifies anti-leniency indicators are present in scoring output.

### Criticality-Based Auto-Activation

| Criticality | Auto-Activated Modes | Token Budget |
|-------------|---------------------|--------------|
| C1 | None (standard review only; S-010 self-review) | 2,000 |
| C2 | adversarial-critique + adversarial-scoring | 8,200 |
| C3 | steelman-critique + adversarial-premortem + adversarial-fmea + adversarial-scoring | 22,800 |
| C4 | All 6 modes | 34,400+ |

**Note:** At C4, S-007 (Constitutional AI) and S-011 (CoVe) are consumed via nse-verification's adversarial modes when agents are orchestrated together.

### Adversarial Finding Format

All adversarial review findings use the existing RFA/RFI/Comment categories:

```
### Adversarial Review Finding: ARF-{gate}-{NNN}

| Attribute | Value |
|-----------|-------|
| **Finding ID** | ARF-{gate}-{NNN} |
| **Category** | RFA / RFI / Comment |
| **Mode** | {mode name} |
| **Strategy** | S-{NNN} ({Strategy Name}) |
| **Severity** | CRITICAL / MAJOR / MINOR / INFO |
| **Criterion** | {entrance/exit criterion being evaluated} |
| **Evidence** | {citation to specific evidence or gap} |
| **Remediation** | {specific recommendation} |
| **Owner** | {suggested owner for RFA/RFI} |
| **Due** | {suggested resolution date} |
| **Traceability** | {FR-305-XXX; NPR 7123.1D Appendix G section; HARD rule ID} |
```

**Category Assignment:**
- **RFA:** Issue that MUST be addressed before review can pass. CRITICAL and MAJOR findings.
- **RFI:** Gap where additional information is needed. Significance uncertain.
- **Comment:** Observation not requiring action. INFO findings, positive observations, scores.

</adversarial_modes>
```

---

## Per-Gate Adversarial Behavior Section

The following `<adversarial_gate_behavior>` block is added inside `<agent>`, after `<adversarial_modes>`.

```markdown
<adversarial_gate_behavior>
## Per-Gate Adversarial Behavior

Each review gate has a default adversarial strategy profile based on the gate's primary concerns and the EN-303 Phase-Strategy Interaction Matrix.

### SRR (System Requirements Review)

**Default Criticality:** C2 | **Primary Concern:** Requirements completeness

| Strategy | Application | Finding Type |
|----------|------------|-------------|
| S-013 (Inversion) | Generate anti-requirements testing baseline completeness | RFA |
| S-007 (Constitutional AI) | Evaluate requirements against NPR 7123.1D P2 and P-040 | RFA |
| S-003 + S-002 (Steelman-DA) | Challenge requirements completeness argument | RFI |
| S-014 (LLM-as-Judge) | Score SRR readiness | Comment |

**SRR Adversarial Package:**
After standard SRR entrance criteria evaluation, append:
1. Anti-requirement checklist (S-013) -- identifies requirements gaps
2. Compliance report (S-007) -- validates against NPR 7123.1D Process 2
3. Steelman-DA assessment (S-003/S-002) -- challenges completeness claim
4. Readiness score (S-014) -- composite quality score

### PDR (Preliminary Design Review)

**Default Criticality:** C2 | **Primary Concern:** Design viability

| Strategy | Application | Finding Type |
|----------|------------|-------------|
| S-002 (Devil's Advocate) | Challenge preliminary design decisions | RFA |
| S-004 (Pre-Mortem) | Imagine design failure scenarios | RFA |
| S-003 (Steelman) | Reconstruct design rationale before DA | Comment |
| S-014 (LLM-as-Judge) | Score PDR readiness | Comment |

**PDR Adversarial Package:**
1. Pre-Mortem failure inventory (S-004) -- failure scenarios for the design
2. Steelman-DA assessment (S-003/S-002) -- challenge design decisions
3. Readiness score (S-014) -- composite quality score

### CDR (Critical Design Review)

**Default Criticality:** C3 | **Primary Concern:** Design completeness, build readiness

| Strategy | Application | Finding Type |
|----------|------------|-------------|
| S-007 (Constitutional AI) | Evaluate design against architecture/coding standards | RFA |
| S-012 (FMEA) | Enumerate design failure modes with RPN | RFA |
| S-013 (Inversion) | Generate design anti-patterns | RFI |
| S-003 + S-002 (Steelman-DA) | Challenge design completeness | RFA |
| S-014 (LLM-as-Judge) | Score CDR readiness | Comment |

**CDR Adversarial Package:**
1. FMEA failure mode inventory (S-012) -- systematic enumeration with RPN
2. Compliance report (S-007) -- validate against architecture standards
3. Anti-pattern checklist (S-013) -- design anti-patterns
4. Steelman-DA assessment (S-003/S-002) -- challenge readiness to build
5. Readiness score (S-014) -- composite quality score

### TRR (Test Readiness Review)

**Default Criticality:** C2 | **Primary Concern:** Test readiness

| Strategy | Application | Finding Type |
|----------|------------|-------------|
| S-011 (CoVe) | Verify test procedure claims and evidence | RFA |
| S-014 (LLM-as-Judge) | Score test readiness | Comment |
| S-007 (Constitutional AI) | Evaluate test artifacts against NPR P7 | RFA |
| S-003 + S-002 (Steelman-DA) | Challenge test readiness argument | RFI |

**TRR Adversarial Package:**
1. Factual verification of test claims (S-011) -- via nse-verification orchestration
2. Compliance report (S-007) -- validate against NPR 7123.1D Process 7
3. Steelman-DA assessment (S-003/S-002) -- challenge test readiness
4. Readiness score (S-014) -- composite quality score

### FRR (Flight/Final Readiness Review)

**Default Criticality:** C4 | **Primary Concern:** Complete readiness

**Requirement:** FR-305-029 -- FRR SHALL be C4 with all 10 strategies Required.

| Activation | Description |
|-----------|-------------|
| All 6 modes | Active simultaneously |
| Cross-agent | nse-verification adversarial modes also invoked |
| Token budget | 35,000-55,000 tokens (C4 allocation) |
| Human-in-the-loop | P-020 requires human authority for FRR determination |

**FRR Adversarial Package:**
1. Full Steelman-DA assessment (S-003/S-002)
2. Pre-Mortem failure inventory (S-004)
3. Comprehensive FMEA (S-012)
4. Red Team vulnerability assessment (S-001)
5. Readiness score (S-014)
6. nse-verification: anti-requirements (S-013), factual verification (S-011), compliance (S-007), self-refine (S-010)

</adversarial_gate_behavior>
```

---

## Adversarial Invocation Protocol

The following content is appended to the existing `<invocation_protocol>` section:

```markdown
## Adversarial Mode Invocation (Optional)

When adversarial modes are requested, add mode and gate flags to the NSE CONTEXT:

```markdown
## NSE CONTEXT (REQUIRED)
- **Project ID:** {project_id}
- **Entry ID:** {entry_id}
- **Review Type:** {MCR|SRR|MDR|SDR|PDR|CDR|SIR|TRR|SAR|ORR|FRR}
- **Topic:** {topic}
- **Adversarial Mode:** {adversarial-critique | steelman-critique | adversarial-premortem | adversarial-fmea | adversarial-redteam | adversarial-scoring | all | gate-default}
- **Criticality:** {C1 | C2 | C3 | C4 | auto}
```

### Adversarial Invocation Examples

**Example 1: CDR with gate-default adversarial behavior**
```
## NSE CONTEXT (REQUIRED)
- **Project ID:** PROJ-002
- **Entry ID:** e-005
- **Review Type:** CDR
- **Topic:** API Service CDR Entrance Evaluation
- **Adversarial Mode:** gate-default
- **Criticality:** auto

## REVIEW TASK
Evaluate CDR entrance criteria for the API service with adversarial assessment.
Apply gate-default adversarial strategies (S-007 + S-012 + S-013 + S-003/S-002 + S-014).
Produce readiness score and FMEA of entrance criteria.
```

**Example 2: Explicit steelman-critique at PDR**
```
## NSE CONTEXT (REQUIRED)
- **Project ID:** PROJ-002
- **Entry ID:** e-005
- **Review Type:** PDR
- **Topic:** Authentication Design PDR Steelman Challenge
- **Adversarial Mode:** steelman-critique
- **Criticality:** C2

## REVIEW TASK
Apply Steelman-then-DA protocol to the PDR readiness assessment.
First reconstruct the strongest design readiness argument, then challenge it.
```

**Example 3: FRR full adversarial package**
```
## NSE CONTEXT (REQUIRED)
- **Project ID:** PROJ-002
- **Entry ID:** e-005
- **Review Type:** FRR
- **Topic:** Release Readiness FRR Full Assessment
- **Adversarial Mode:** all
- **Criticality:** C4

## REVIEW TASK
Execute the complete FRR adversarial assessment package at C4 intensity.
All 6 adversarial modes active. Coordinate with nse-verification for V&V
adversarial assessment. Produce comprehensive adversarial readiness package.
Human authority required for final FRR determination (P-020).
```

**When no adversarial flags are specified, the agent behaves identically to v2.2.0.**

**Gate-default mode:** When `--mode gate-default` is specified, the agent automatically selects the adversarial strategies defined in the Per-Gate Adversarial Behavior section for the specified review type.
```

---

## Adversarial Output Templates

The following templates are appended to the existing `<templates>` section:

```markdown
## Adversarial Review Finding Template

```markdown
### Adversarial Review Finding: ARF-{gate}-{NNN}

| Attribute | Value |
|-----------|-------|
| **Finding ID** | ARF-{gate}-{NNN} |
| **Category** | {RFA / RFI / Comment} |
| **Mode** | {mode name} |
| **Strategy** | S-{NNN} ({Strategy Name}) |
| **Severity** | {CRITICAL / MAJOR / MINOR / INFO} |
| **Criterion** | {entrance/exit criterion} |
| **Evidence** | {citation or gap reference} |
| **Remediation** | {actionable recommendation} |
| **Owner** | {suggested owner} |
| **Due** | {suggested date} |
| **Traceability** | {FR-305-XXX; NPR 7123.1D Appendix G; HARD rule} |
```

## Adversarial Review Readiness Score Template

```markdown
---
DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
standards. It is advisory only and does not constitute official NASA guidance.
All SE decisions require human review and professional engineering judgment.
Not for use in mission-critical decisions without SME validation.
---

# {Review Type} Adversarial Readiness Assessment

> **Project:** {Project ID}
> **Entry:** {Entry ID}
> **Review:** {Review Type}
> **Date:** {Date}
> **Criticality:** {C1/C2/C3/C4}
> **Strategies Applied:** {list}

## L0: Executive Summary

**Standard Readiness:** {Ready/Not Ready/Conditional}
**Adversarial Readiness Score:** {X.XX}/1.00 ({PASS/CONDITIONAL/FAIL})
**Critical Adversarial Findings:** {count}

{2-3 sentence adversarial assessment summary}

## L1: Adversarial Assessment Detail

### Readiness Score

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Criteria Coverage | 0.XX | {evidence} |
| Evidence Strength | 0.XX | {evidence} |
| Gap Analysis Completeness | 0.XX | {evidence} |
| Risk Assessment | 0.XX | {evidence} |
| Action Item Quality | 0.XX | {evidence} |
| Readiness Rationale | 0.XX | {evidence} |
| **Composite** | **0.XX** | **{PASS/CONDITIONAL/FAIL}** |

### Adversarial Findings

{Ordered list of ARF-{gate}-NNN findings}

### {Mode-Specific Sections}

{Pre-Mortem failure inventory, FMEA table, Red Team vulnerabilities, etc.}

## L2: Strategic Assessment

### Adversarial Quality Trends
{How does adversarial assessment compare to standard assessment?}

### Risk from Adversarial Findings
{What program risks do the adversarial findings reveal?}

### Remediation Priority
{Ordered improvements ranked by impact on readiness score}

## References
- NPR 7123.1D Appendix G, Table G-{X}
- ADR-EPIC002-001 (adversarial strategy framework)
- H-13 (Quality gate score >= 0.92)

---

*Generated by nse-reviewer agent v3.0.0 (adversarial mode: {modes})*
```

## FMEA Report Template (S-012)

```markdown
### Entrance Criteria FMEA Report

| # | Criterion | Failure Mode | Severity | Occurrence | Detection | RPN | Risk Level | Mitigation |
|---|-----------|-------------|----------|-----------|-----------|-----|------------|------------|
| 1 | {criterion} | {failure mode} | {1-10} | {1-10} | {1-10} | {S*O*D} | {H/M/L} | {action} |

**FMEA Scale:** Standardized 1-10 scale per quality-enforcement.md SSOT (max RPN = 1,000). This aligns with EN-304 ps-critic fmea mode for cross-skill RPN comparability.

**RPN Thresholds (1-10 scale):**
- RPN > 200: CRITICAL risk -- RFA finding, requires immediate attention and design review
- RPN 100-200: HIGH risk -- RFA finding, must address before review
- RPN 50-99: MEDIUM risk -- RFI finding, investigate
- RPN < 50: LOW risk -- Comment, monitor

**Risk Level:**
- CRITICAL: S >= 8 OR RPN > 200
- HIGH: S >= 6 AND RPN >= 100
- MEDIUM: S >= 4 OR RPN >= 50
- LOW: All others
```
```

---

## Adversarial State Management

The following fields are added to the existing `<state_management>` state schema:

```yaml
review_output:
  # Existing fields (ALL PRESERVED)
  project_id: "{project_id}"
  entry_id: "{entry_id}"
  review_type: "{review_type}"
  artifact_path: "projects/{project}/reviews/{filename}.md"
  summary: "{readiness summary}"
  readiness: "{Ready|Not Ready|Conditional}"
  criteria_met: {count}
  criteria_total: {count}
  blockers: ["{blocker1}", ...]
  action_items: [{action, owner, due}, ...]
  next_agent_hint: "nse-reporter"
  nasa_processes_applied: ["Process 16", "Appendix G"]

  # NEW: Adversarial extension fields (default to null if no adversarial modes applied)
  adversarial:
    modes_applied: ["steelman-critique", "adversarial-scoring"]  # or null
    strategies_applied: ["S-003", "S-002", "S-014"]  # or null
    criticality_level: "C2"  # or null
    composite_quality_score: 0.93  # or null
    quality_gate_result: "PASS"  # PASS/CONDITIONAL/FAIL or null
    finding_counts:
      rfa: 2
      rfi: 1
      comment: 5
    adversarial_findings:
      critical: 0
      major: 1
      minor: 3
      info: 4
    premortem_failure_causes: 0  # Count from adversarial-premortem
    fmea_failure_modes: 0        # Count from adversarial-fmea
    fmea_high_rpn_count: 0       # RPN >= 64 count
    redteam_vulnerabilities: 0   # Count from adversarial-redteam
    enforcement_decision:        # or null
      action: "pass"
      reason: "{rationale}"
      violations: []
      criticality_escalation: null
```

---

## Adversarial Guardrails

The following validation rules are added to the existing `<guardrails>` section:

```markdown
**Adversarial Mode Validation:**

1. **Mode Name Validation:**
   - Valid values: `adversarial-critique`, `steelman-critique`, `adversarial-premortem`, `adversarial-fmea`, `adversarial-redteam`, `adversarial-scoring`, `all`, `gate-default`
   - On invalid: Reject with message listing valid modes
   - Case handling: Case-insensitive

2. **Gate-Mode Compatibility Check:**
   - `adversarial-premortem`: Most effective at PDR/CDR (warn if used at TRR/FRR)
   - `adversarial-fmea`: Most effective at CDR (warn if used at SRR)
   - `adversarial-redteam`: Requires C3+ (reject at C1/C2 unless explicitly overridden)
   - `gate-default`: Automatically selects per-gate strategy profile

3. **SYN Pair Enforcement:**
   - If `adversarial-critique` (S-002) is activated without `steelman-critique`:
     Warn: "S-002 is more effective when preceded by S-003 (SYN pair #1). Consider using steelman-critique mode."
   - `steelman-critique` always executes S-003 before S-002 (enforced)

4. **Token Budget Check:**
   - Before activating modes, estimate total token cost
   - If estimated cost exceeds available budget:
     - Drop Medium-tier modes first (adversarial-fmea: 9K, adversarial-redteam: 7K)
     - Retain scoring (adversarial-scoring: 2K)
   - Document degradation in findings

5. **FRR Special Handling:**
   - FRR ALWAYS activates at C4 (FR-305-029)
   - Override any lower criticality specification with C4
   - Warn: "FRR is classified as C4 criticality per FR-305-029. All adversarial strategies activated."
```

---

## Quality Gate Enforcement Section

The following `<adversarial_quality_gate>` block is added inside `<agent>`.

```markdown
<adversarial_quality_gate>
## Quality Gate Enforcement

Adversarial scoring (S-014) drives quality gate enforcement for review readiness:

| Score Range | Outcome | Enforcement Action |
|-------------|---------|-------------------|
| >= 0.92 | **PASS** | Review may proceed; all findings resolved or accepted |
| 0.85 - 0.91 | **CONDITIONAL** | Review may proceed with conditions; RFAs tracked to closure |
| 0.70 - 0.84 | **FAIL** | Review blocked; remediation required before re-assessment |
| < 0.70 | **FAIL** | Review blocked; fundamental rework required |

**H-13 Integration:** When adversarial-scoring produces a composite score below 0.92, the finding is automatically classified as CRITICAL and blocks the review's PASS determination.

**Enforcement Decision Output:**
```yaml
enforcement_decision:
  action: "block"      # pass / warn / block
  reason: "CDR readiness score 0.87 below 0.92 threshold (H-13)"
  violations:
    - "H-13: Quality gate score below threshold"
    - "FR-305-015: Readiness score FAIL"
  criticality_escalation: null  # or "C3" / "C4"
```

**Escalation Rules:**
- Score < 0.70: Auto-escalate criticality by one level
- CRITICAL adversarial findings present: Block regardless of composite score
- Governance artifacts under review: Auto-escalate to C3+ (FR-305-034)

</adversarial_quality_gate>
```

---

## Integration with Existing Sections

### How Adversarial Content Fits Into v2.2.0

```
<agent>
  <identity>              ← UNCHANGED
  <persona>               ← UNCHANGED
  <capabilities>          ← UNCHANGED
  <guardrails>            ← EXTENDED (adversarial mode + gate validation appended)
  <disclaimer>            ← UNCHANGED
  <constitutional_compliance>  ← UNCHANGED
  <invocation_protocol>   ← EXTENDED (adversarial + gate flags appended)
  <output_levels>         ← UNCHANGED (adversarial findings in L1/L2)
  <templates>             ← EXTENDED (adversarial templates appended)
  <state_management>      ← EXTENDED (adversarial fields appended)
  <nasa_methodology>      ← UNCHANGED
  <session_context_validation>  ← EXTENDED (adversarial output fields)
  <adversarial_modes>     ← NEW SECTION
  <adversarial_gate_behavior>   ← NEW SECTION
  <adversarial_quality_gate>    ← NEW SECTION
</agent>
```

### L0/L1/L2 Integration

- **L0:** Adversarial readiness score and PASS/CONDITIONAL/FAIL added to executive summary
- **L1:** Adversarial findings (ARF-{gate}-NNN) appended after standard criteria evaluation
- **L2:** Adversarial quality trends and risk-to-program in strategic assessment

No new output levels are created (BC-305-005).

### Finding Category Integration

Adversarial findings use the existing RFA/RFI/Comment categories per NPR 7123.1D Appendix G. No new finding categories are introduced (FR-305-017).

---

## Backward Compatibility Verification

| Aspect | How BC-305-002 Is Maintained |
|--------|------------------------------|
| Default invocation (no `--mode` flag) | No adversarial modes activate; output identical to v2.2.0 |
| No `Adversarial Mode` in NSE CONTEXT | Treated as non-adversarial invocation |
| No `Criticality` in NSE CONTEXT | No auto-activation; standard behavior |
| FIX-NEG-003 Levenshtein typo detection | Algorithm unchanged; adversarial mode names use separate validation |
| Finding categories | Adversarial findings use existing RFA/RFI/Comment (no new categories) |
| Entrance criteria templates | SRR/PDR/CDR templates preserved; adversarial sections appended |
| Session context schema | All existing fields preserved; `adversarial` key defaults to null |
| L0/L1/L2 structure | Structure preserved; adversarial content within existing levels |
| Review type enum | Existing valid values unchanged; no new review types |

---

## Traceability

| Requirement | How Addressed |
|-------------|--------------|
| FR-305-010 | adversarial-critique mode specification (S-002 DA) |
| FR-305-011 | steelman-critique mode specification (S-003 then S-002 canonical protocol) |
| FR-305-012 | adversarial-premortem mode specification (S-004 failure inventory) |
| FR-305-013 | adversarial-fmea mode specification (S-012 with RPN scoring) |
| FR-305-014 | adversarial-redteam mode specification (S-001 adversary simulation) |
| FR-305-015 | adversarial-scoring mode specification (S-014 quality score) |
| FR-305-016 | Criticality-based auto-activation table (C2/C3/C4) |
| FR-305-017 | Findings use RFA/RFI/Comment categories |
| FR-305-018 | SRR gate adversarial behavior defined |
| FR-305-019 | PDR gate adversarial behavior defined |
| FR-305-020 | CDR gate adversarial behavior defined |
| FR-305-021 | TRR gate adversarial behavior defined |
| FR-305-022 | FRR gate adversarial behavior defined (C4, all strategies) |
| FR-305-030 | Enforcement integration: criticality consumed from PromptReinforcementEngine |
| FR-305-031 | EnforcementDecision in adversarial state management |
| FR-305-032 | S-007 validates HARD rules (via nse-verification orchestration at C4) |
| FR-305-033 | Finding reports use effective HARD language patterns |
| FR-305-034 | Governance escalation in quality gate enforcement |
| NFR-305-001 | Default invocation unchanged (BC-305-002) |
| NFR-305-002 | Token costs documented per mode with tier |
| NFR-305-003 | Modes defined at spec level; portable via L1+L5+Process |
| NFR-305-005 | P-043 disclaimer in all templates |
| NFR-305-007 | All content at markdown specification level |
| NFR-305-008 | State schema extended with adversarial fields |
| NFR-305-009 | S-014 rubric uses >= 0.92 threshold |
| NFR-305-010 | Navigation table with anchor links included |
| BC-305-002 | Backward compatibility verification table |
| BC-305-004 | YAML frontmatter additive; existing tags preserved |
| BC-305-005 | No new output levels |

---

## References

| # | Citation | Sections Referenced |
|---|----------|-------------------|
| 1 | TASK-001 (Requirements) -- FEAT-004:EN-305:TASK-001 | All FR-305, NFR-305, BC-305 requirements |
| 2 | TASK-003 (Design) -- FEAT-004:EN-305:TASK-003 | 6 mode definitions, criticality activation, per-gate behavior, finding format, quality gate |
| 3 | TASK-004 (Gate Mapping) -- FEAT-004:EN-305:TASK-004 | Strategy-to-gate mapping, token budgets, agent responsibility |
| 4 | nse-reviewer agent spec -- `skills/nasa-se/agents/nse-reviewer.md` v2.2.0 | Existing sections, YAML frontmatter, templates, session context |
| 5 | ADR-EPIC002-001 (ACCEPTED) -- FEAT-004:EN-302:TASK-005 | 10 strategies, SYN pair #1, token tiers |
| 6 | EN-303 TASK-003 -- FEAT-004:EN-303:TASK-003 | Per-strategy profiles, SYN pairs, decision criticality |
| 7 | Barrier-2 ENF-to-ADV Handoff -- EPIC002-CROSSPOLL-B2-ENF-TO-ADV | EnforcementDecision, HARD rules, governance escalation |

---

*Document ID: FEAT-004:EN-305:TASK-006*
*Agent: nse-architecture-305*
*Created: 2026-02-13*
*Status: Complete*
