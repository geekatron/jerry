# TASK-003: Adversarial Integration Design for nse-reviewer

<!--
DOCUMENT-ID: FEAT-004:EN-305:TASK-003
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
> **Purpose:** Design adversarial integration for the nse-reviewer agent, defining adversarial critique modes for technical reviews, strategy enhancement of review rigor, quality gate enforcement integration, and per-gate adversarial behavior

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this design delivers |
| [Design Philosophy](#design-philosophy) | How adversarial modes enhance SE reviews |
| [Adversarial Mode Definitions](#adversarial-mode-definitions) | The 6 adversarial modes for nse-reviewer |
| [Criticality-Based Mode Activation](#criticality-based-mode-activation) | C1-C4 mapping to mode selection |
| [Per-Gate Adversarial Behavior](#per-gate-adversarial-behavior) | Strategy selection at SRR, PDR, CDR, TRR, FRR |
| [Output Format for Adversarial Review Findings](#output-format-for-adversarial-review-findings) | Structured finding schema using RFA/RFI/Comment |
| [Quality Gate Enforcement Integration](#quality-gate-enforcement-integration) | How adversarial scoring drives review outcomes |
| [Enforcement Integration](#enforcement-integration) | Consuming enforcement layer data |
| [Session Context Extensions](#session-context-extensions) | Additions to the v1.0.0 session context schema |
| [Backward Compatibility](#backward-compatibility) | Preserving existing nse-reviewer behavior |
| [Traceability](#traceability) | Mapping to TASK-001 requirements |
| [References](#references) | Source citations |

---

## Summary

This document designs the adversarial integration for the nse-reviewer agent (v2.2.0). The design introduces 6 adversarial modes that enhance the agent's technical review capabilities across all 5 SE review gates (SRR, PDR, CDR, TRR, FRR). Each mode maps one or more of the 10 selected adversarial strategies to specific review activities per NPR 7123.1D Appendix G.

The design satisfies requirements FR-305-010 through FR-305-022 from TASK-001. Adversarial findings are produced in the existing RFA/RFI/Comment finding categories (FR-305-017), ensuring compatibility with the current review process.

---

## Design Philosophy

### Review Rigor Enhancement

The nse-reviewer currently evaluates entrance/exit criteria and produces readiness assessments. Adversarial modes add a layer of challenge: instead of merely checking "are criteria met?", they actively probe "how could this review fail to catch critical issues?"

### SYN Pair Protocol: S-003 then S-002

The canonical Jerry review protocol is the Steelman-then-Devil's-Advocate (SYN pair #1 from EN-303 TASK-003). The nse-reviewer design makes this the default adversarial behavior for all reviews at C2+ criticality: first reconstruct the strongest version of the review readiness argument (S-003), then systematically challenge that strongest version (S-002).

### Per-Gate Strategy Selection

Different review gates have different concerns. The design maps strategies to gates based on the EN-303 TASK-001 Phase-Strategy Interaction Matrix and TASK-003 per-strategy Decision Criticality Mapping:

| Gate | Phase Code | Primary Concern | Primary Strategies |
|------|-----------|----------------|-------------------|
| SRR | PH-DESIGN | Requirements completeness | S-013 (anti-requirements), S-007 (compliance) |
| PDR | PH-DESIGN | Design viability | S-002 (DA), S-004 (Pre-Mortem) |
| CDR | PH-DESIGN→PH-IMPL | Design completeness | S-007 (compliance), S-012 (FMEA) |
| TRR | PH-IMPL→PH-VALID | Test readiness | S-011 (CoVe), S-014 (scoring) |
| FRR | PH-VALID | Flight/mission readiness | All 10 (C4 intensity) |

---

## Adversarial Mode Definitions

### Mode 1: `adversarial-critique` (S-002 Devil's Advocate)

**Requirement:** FR-305-010

**Purpose:** Challenge the rationale behind review readiness determinations (PASS/CONDITIONAL/FAIL) by applying Devil's Advocate to the readiness argument.

**Activation:**
- Explicit flag: `--mode adversarial-critique`
- Auto-activation: C2+ criticality

**Workflow:**
1. After standard entrance criteria evaluation, extract the readiness determination and its rationale
2. Apply S-002 (Devil's Advocate) to challenge:
   - Each "GREEN" criterion: What evidence would make this YELLOW or RED?
   - The overall readiness determination: What are the strongest arguments against proceeding?
   - Assumptions in the rationale: What unstated assumptions are being relied upon?
3. Produce counter-arguments as RFA findings

**Token Cost:** ~4,600 tokens per invocation (Low tier)

**Preconditions:**
- Entrance criteria evaluation is complete (standard assessment first, then challenge)
- TEAM-MULTI or TEAM-HIL composition (self-DA is weaker per EN-303 TASK-003 S-002 profile)
- S-003 (Steelman) should precede S-002 (SYN pair #1 protocol)

---

### Mode 2: `steelman-critique` (S-003 then S-002)

**Requirement:** FR-305-011

**Purpose:** Apply the canonical Steelman-then-DA protocol to review readiness assessment. First reconstruct the readiness argument in its strongest form, then challenge that strongest form.

**Activation:**
- Explicit flag: `--mode steelman-critique`
- Auto-activation: C3+ criticality (Required at C3 per EN-303 TASK-003 S-003 profile)

**Workflow:**
1. After standard criteria evaluation, apply S-003 (Steelman) to the readiness argument:
   - Identify the strongest evidence for each GREEN criterion
   - Reconstruct the rationale in its most defensible form
   - Make assumptions explicit and charitable
2. Apply S-002 (Devil's Advocate) to the steelmanned argument:
   - Challenge even the strongest formulation
   - Identify weaknesses that survive steelmanning
   - Produce counter-arguments that address the core of the argument, not strawman versions
3. Findings that survive steelmanning are higher-signal and receive MAJOR severity

**Token Cost:** ~6,200 tokens per invocation (1,600 for S-003 + 4,600 for S-002)

**Sequencing:** S-003 MUST execute before S-002 (SYN pair #1 canonical protocol per EN-303 TASK-003)

---

### Mode 3: `adversarial-premortem` (S-004 Pre-Mortem)

**Requirement:** FR-305-012

**Purpose:** Imagine how the review could fail to catch critical issues, producing a failure cause inventory for review preparation.

**Activation:**
- Explicit flag: `--mode adversarial-premortem`
- Auto-activation: C3+ criticality at PDR and CDR gates

**Workflow:**
1. Adopt the temporal reframing: "The review has been completed. It was a disaster -- critical issues were missed, and the project suffered significant setbacks."
2. Generate a failure cause inventory:
   - What entrance criteria appeared GREEN but concealed underlying issues?
   - What categories of defects passed through the review undetected?
   - What blind spots in the review scope allowed issues to escape?
   - What review board biases contributed to the failure?
3. For each failure cause, produce a mitigation recommendation
4. Convert the most critical failure causes into additional review preparation tasks (RFA findings)

**Token Cost:** ~5,600 tokens per invocation (Low tier)

**Preconditions:**
- Review is in preparation or early execution phase (PH-DESIGN phase per EN-303 TASK-003 S-004 profile)
- Artifact describes a plan or design with a future success/failure horizon

---

### Mode 4: `adversarial-fmea` (S-012 FMEA)

**Requirement:** FR-305-013

**Purpose:** Systematically enumerate failure modes in the review entrance criteria evaluation process.

**Activation:**
- Explicit flag: `--mode adversarial-fmea`
- Auto-activation: C3+ criticality at CDR gate

**Workflow:**
1. Enumerate each entrance criterion as a "component" of the review process
2. For each criterion, identify failure modes:
   - **Incorrect evaluation:** Criterion marked GREEN when evidence is insufficient
   - **Missing evidence:** Criterion evaluated without supporting artifact
   - **Stale evidence:** Evidence references outdated or superseded documents
   - **Ambiguous criterion:** Criterion language allows multiple interpretations
3. Score each failure mode: Severity (1-5) x Occurrence (1-5) x Detection (1-5) = RPN
4. Produce risk-prioritized failure inventory sorted by RPN

**Token Cost:** ~9,000 tokens per invocation (Medium tier)

**Preconditions:**
- Entrance criteria are defined for the review type
- TOK-FULL or TOK-CONST budget state (9,000 tokens required)

---

### Mode 5: `adversarial-redteam` (S-001 Red Team)

**Requirement:** FR-305-014

**Purpose:** Simulate an adversary attempting to pass a review gate with non-compliant artifacts.

**Activation:**
- Explicit flag: `--mode adversarial-redteam`
- Auto-activation: C4 criticality (Required at C4; Recommended at C3 for architecture reviews)

**Workflow:**
1. Adopt the adversary persona: "I am attempting to pass this review gate with artifacts that appear compliant but contain hidden non-compliance."
2. For each entrance criterion, identify:
   - How could compliant-appearing evidence be fabricated or misleading?
   - What are the minimum viable artifacts that would technically satisfy the criterion?
   - Where are the detection gaps in the reviewer's evaluation process?
3. Produce a vulnerability report documenting attack vectors against the review process
4. For each vulnerability, recommend detection improvements

**Token Cost:** ~7,000 tokens per invocation (Medium tier)

**Preconditions:**
- TEAM-MULTI composition (needs separate critic with adversary persona per EN-303 TASK-003 S-001 profile)
- C3+ criticality (token cost unjustified below C3)

---

### Mode 6: `adversarial-scoring` (S-014 LLM-as-Judge)

**Requirement:** FR-305-015

**Purpose:** Produce a numerical quality score (0.00-1.00) on the overall review readiness assessment.

**Activation:**
- Explicit flag: `--mode adversarial-scoring`
- Auto-activation: C2+ criticality

**Workflow:**
1. Define the review readiness rubric:
   - **Criteria Coverage** (0.00-1.00): Percentage of entrance criteria evaluated with evidence
   - **Evidence Strength** (0.00-1.00): Quality and recency of evidence per criterion
   - **Gap Analysis Completeness** (0.00-1.00): Are all gaps identified with mitigation plans?
   - **Risk Assessment** (0.00-1.00): Are risks to the review documented with impacts?
   - **Action Item Quality** (0.00-1.00): Are pre-review actions specific, owned, and dated?
   - **Readiness Rationale** (0.00-1.00): Is the readiness determination well-supported?
2. Score each dimension with rationale
3. Calculate composite score and determine PASS/FAIL against >= 0.92 threshold (H-13)

**Token Cost:** ~2,000 tokens per invocation (Ultra-Low tier)

---

## Criticality-Based Mode Activation

**Requirement:** FR-305-016

| Criticality | Auto-Activated Modes | Required Strategies | Total Token Budget |
|-------------|---------------------|--------------------|--------------------|
| **C1** | None (standard review only) | S-010 (self-review) | 2,000 |
| **C2** | adversarial-critique + adversarial-scoring | S-003, S-002, S-014 | 8,200 |
| **C3** | steelman-critique + adversarial-premortem + adversarial-fmea + adversarial-scoring | S-003, S-002, S-014, S-004, S-012, S-013 | 22,800 |
| **C4** | All 6 modes | All 10 strategies (via steelman-critique + adversarial-premortem + adversarial-fmea + adversarial-redteam + adversarial-scoring + adversarial-compliance via S-007) | 34,400+ |

**Note:** At C4, S-007 (Constitutional AI) and S-011 (CoVe) are invoked as part of the comprehensive review but are not standalone modes for nse-reviewer; they are consumed via nse-verification's adversarial modes when the agents are orchestrated together.

---

## Per-Gate Adversarial Behavior

### SRR (System Requirements Review)

**Requirement:** FR-305-018

| Strategy | Application at SRR | Finding Type |
|----------|--------------------|-------------|
| S-013 (Inversion) | Generate anti-requirements that test completeness of the requirements baseline | RFA: "Anti-requirement {X} is not covered by any requirement" |
| S-007 (Constitutional AI) | Evaluate requirements against NPR 7123.1D Process 2 and P-040 traceability | RFA: "P-040 violation: requirement {X} has no parent traceability" |
| S-003 + S-002 (Steelman-DA) | Challenge the requirements completeness argument | RFI: "What evidence supports {requirement set} completeness?" |
| S-014 (LLM-as-Judge) | Score SRR readiness | Comment: "SRR readiness score: {X}/1.00" |

### PDR (Preliminary Design Review)

**Requirement:** FR-305-019

| Strategy | Application at PDR | Finding Type |
|----------|--------------------|-------------|
| S-002 (Devil's Advocate) | Challenge preliminary design decisions and interface definitions | RFA: "Design decision {X} has unexamined alternative {Y}" |
| S-004 (Pre-Mortem) | Imagine how the preliminary design could fail in implementation | RFA: "Pre-Mortem scenario: {failure cause} leads to {consequence}" |
| S-003 (Steelman) | Reconstruct design rationale in strongest form before challenge | Comment: "Design rationale steelmanned to: {strongest formulation}" |
| S-014 (LLM-as-Judge) | Score PDR readiness | Comment: "PDR readiness score: {X}/1.00" |

### CDR (Critical Design Review)

**Requirement:** FR-305-020

| Strategy | Application at CDR | Finding Type |
|----------|--------------------|-------------|
| S-007 (Constitutional AI) | Evaluate detailed design against architecture standards and coding standards | RFA: "Architecture standard violation: {specific standard} at {location}" |
| S-012 (FMEA) | Enumerate design failure modes with severity, occurrence, detection | RFA: "Failure mode: {mode}, RPN={value}, mitigation required" |
| S-013 (Inversion) | Generate design anti-patterns | RFI: "Does design address anti-pattern {X}?" |
| S-003 + S-002 (Steelman-DA) | Challenge the detailed design readiness | RFA: "Design completeness challenged: {counter-argument}" |
| S-014 (LLM-as-Judge) | Score CDR readiness | Comment: "CDR readiness score: {X}/1.00" |

### TRR (Test Readiness Review)

**Requirement:** FR-305-021

| Strategy | Application at TRR | Finding Type |
|----------|--------------------|-------------|
| S-011 (CoVe) | Verify test procedure claims and evidence references | RFA: "Claim '{claim}' in test procedure {proc} is UNVERIFIED" |
| S-014 (LLM-as-Judge) | Score test readiness | Comment: "TRR readiness score: {X}/1.00" |
| S-007 (Constitutional AI) | Evaluate test artifacts against NPR 7123.1D Process 7 | RFA: "Process 7 compliance gap: {gap}" |
| S-003 + S-002 (Steelman-DA) | Challenge the test readiness argument | RFI: "Test coverage for {requirement} claimed at {X}% -- supporting evidence?" |

### FRR (Flight/Final Readiness Review)

**Requirement:** FR-305-022

| Activation | Description |
|-----------|-------------|
| **Criticality** | C4 (all 10 strategies activated) |
| **All 6 modes** | Active simultaneously |
| **Comprehensive package** | Steelman-critique + adversarial-premortem + adversarial-fmea + adversarial-redteam + adversarial-scoring |
| **Additional invocations** | nse-verification adversarial modes also invoked via orchestration |
| **Token budget** | 35,000-55,000 tokens (C4 allocation per EN-303 TASK-001) |
| **Human-in-the-loop** | P-020 requires human authority for FRR determination |

---

## Output Format for Adversarial Review Findings

**Requirement:** FR-305-017

Adversarial findings are produced in the existing RFA/RFI/Comment finding categories per NPR 7123.1D Appendix G:

```markdown
### Adversarial Review Finding: {Finding ID}

| Attribute | Value |
|-----------|-------|
| **Finding ID** | ARF-{gate}-{NNN} |
| **Category** | RFA / RFI / Comment |
| **Mode** | adversarial-critique / steelman-critique / adversarial-premortem / adversarial-fmea / adversarial-redteam / adversarial-scoring |
| **Strategy** | S-{NNN} ({Strategy Name}) |
| **Severity** | CRITICAL / MAJOR / MINOR / INFO |
| **Criterion** | {entrance/exit criterion being evaluated} |
| **Evidence** | {citation to specific evidence or gap} |
| **Remediation** | {specific recommendation} |
| **Owner** | {suggested owner for RFA/RFI} |
| **Due** | {suggested resolution date} |
| **Traceability** | {FR-305-XXX, NPR 7123.1D section, HARD rule ID} |
```

**Category Assignment Rules:**
- **RFA (Request for Action):** Finding identifies an issue that MUST be addressed before review can pass. Used for CRITICAL and MAJOR severity findings.
- **RFI (Request for Information):** Finding identifies a gap where additional information is needed. Used for information gaps where the issue may or may not be significant.
- **Comment:** Observation that does not require action. Used for INFO findings, positive observations, and quality scores.

---

## Quality Gate Enforcement Integration

Adversarial scoring (S-014) drives the quality gate enforcement for review readiness:

| Score Range | Review Outcome | Enforcement Action |
|-------------|---------------|-------------------|
| >= 0.92 | PASS (all findings resolved or accepted) | Review may proceed |
| 0.85 - 0.91 | CONDITIONAL (minor findings outstanding) | Review may proceed with conditions; RFAs tracked |
| 0.70 - 0.84 | FAIL (significant findings outstanding) | Review blocked; remediation required |
| < 0.70 | FAIL (critical findings) | Review blocked; fundamental rework required |

**Enforcement integration with H-13 (Quality gate score >= 0.92 REQUIRED):** When adversarial-scoring produces a composite score below 0.92, the finding is automatically classified as CRITICAL and blocks the review's PASS determination.

---

## Enforcement Integration

**Requirements:** FR-305-030, FR-305-031, FR-305-032, FR-305-033, FR-305-034

| Integration Point | Source | How nse-reviewer Consumes It |
|-------------------|--------|------------------------------|
| C1-C4 criticality | PromptReinforcementEngine (L2) | Determines which adversarial modes to auto-activate |
| EnforcementDecision | PreToolEnforcementEngine (L3) | Adversarial findings mapped to action/reason/violations/criticality_escalation |
| 24 HARD rules | quality-enforcement.md SSOT (L1) | adversarial-critique evaluates review readiness against applicable HARD rules |
| 6 effective patterns | barrier-2 handoff | Finding reports use Forbidden/Required Binary and Quality Gate Declaration patterns |
| Governance escalation | PreToolEnforcementEngine (L3) | Reviews of governance artifacts auto-escalate to C3+ |

---

## Session Context Extensions

**Requirement:** NFR-305-008

```yaml
review_output:
  # Existing fields (preserved)
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

  # NEW: Adversarial extension fields
  adversarial:
    modes_applied: ["steelman-critique", "adversarial-scoring"]
    strategies_applied: ["S-003", "S-002", "S-014"]
    criticality_level: "C2"
    composite_quality_score: 0.93
    quality_gate_result: "PASS"
    finding_counts:
      rfa: 2
      rfi: 1
      comment: 5
    adversarial_findings:
      critical: 0
      major: 1
      minor: 3
      info: 4
    premortem_failure_causes: 0
    fmea_failure_modes: 0
    redteam_vulnerabilities: 0
```

---

## Backward Compatibility

**Requirement:** BC-305-002

| Aspect | Guarantee |
|--------|-----------|
| Default invocation | nse-reviewer invoked without `--mode` flags produces identical output to v2.2.0 |
| Finding categories | Adversarial findings use existing RFA/RFI/Comment categories (no new categories) |
| Review type validation | FIX-NEG-003 Levenshtein distance typo detection unchanged |
| Session context schema | All existing fields preserved; adversarial fields are additive |
| L0/L1/L2 output levels | Adversarial findings integrated into existing levels (not new levels) |
| Entrance criteria templates | Existing SRR/PDR/CDR templates preserved; adversarial sections appended |

---

## Traceability

| TASK-001 Requirement | How Addressed |
|---------------------|--------------|
| FR-305-010 | adversarial-critique mode defined (S-002 DA challenging readiness) |
| FR-305-011 | steelman-critique mode defined (S-003 then S-002 canonical protocol) |
| FR-305-012 | adversarial-premortem mode defined (S-004 failure cause inventory) |
| FR-305-013 | adversarial-fmea mode defined (S-012 systematic failure enumeration) |
| FR-305-014 | adversarial-redteam mode defined (S-001 adversary simulation) |
| FR-305-015 | adversarial-scoring mode defined (S-014 quality score 0.00-1.00) |
| FR-305-016 | Criticality-based mode activation (C2: S-003+S-002+S-014; C3: adds S-004+S-012+S-013; C4: all) |
| FR-305-017 | Findings use RFA/RFI/Comment categories per NPR 7123.1D Appendix G |
| FR-305-018 | SRR adversarial behavior defined (S-013 anti-requirements) |
| FR-305-019 | PDR adversarial behavior defined (S-002 DA + S-004 Pre-Mortem) |
| FR-305-020 | CDR adversarial behavior defined (S-007 compliance + S-012 FMEA) |
| FR-305-021 | TRR adversarial behavior defined (S-011 CoVe + S-014 scoring) |
| FR-305-022 | FRR adversarial behavior defined (C4, all 10 strategies) |
| FR-305-030-035 | Enforcement integration section addresses all enforcement requirements |
| BC-305-002 | Backward compatibility guarantees defined |

---

## References

| # | Citation | Sections Referenced |
|---|----------|-------------------|
| 1 | TASK-001 (Requirements) -- FEAT-004:EN-305:TASK-001 | FR-305-010 through FR-305-022, FR-305-030 through FR-305-035, BC-305-002 |
| 2 | ADR-EPIC002-001 (ACCEPTED) -- FEAT-004:EN-302:TASK-005 | 10 selected strategies, SYN pair #1 (S-003 + S-002), quality layers |
| 3 | EN-303 TASK-001 -- FEAT-004:EN-303:TASK-001 | Phase-Strategy Interaction Matrix, C1-C4 strategy allocation |
| 4 | EN-303 TASK-003 -- FEAT-004:EN-303:TASK-003 | S-002/S-003/S-004/S-012/S-001 profiles, SYN pairs, decision criticality mapping |
| 5 | Barrier-2 ENF-to-ADV Handoff -- EPIC002-CROSSPOLL-B2-ENF-TO-ADV | EnforcementDecision, HARD rules, effective patterns, governance escalation |
| 6 | nse-reviewer agent spec -- `skills/nasa-se/agents/nse-reviewer.md` v2.2.0 | Review gate methodology, finding categories, entrance criteria templates |

---

*Document ID: FEAT-004:EN-305:TASK-003*
*Agent: nse-architecture-305*
*Created: 2026-02-13*
*Status: Complete*
