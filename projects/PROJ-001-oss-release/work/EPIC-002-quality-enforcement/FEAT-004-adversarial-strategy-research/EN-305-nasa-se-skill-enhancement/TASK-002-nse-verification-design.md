# TASK-002: Adversarial Integration Design for nse-verification

<!--
DOCUMENT-ID: FEAT-004:EN-305:TASK-002
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
> **Purpose:** Design adversarial integration for the nse-verification agent, defining adversarial challenge modes for V&V processes, strategy application to verification activities, integration with C1-C4 criticality, and output format for adversarial V&V findings

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this design delivers |
| [Design Philosophy](#design-philosophy) | How adversarial modes integrate with existing V&V |
| [Adversarial Mode Definitions](#adversarial-mode-definitions) | The 4 adversarial modes + 1 pre-step for nse-verification |
| [Criticality-Based Mode Activation](#criticality-based-mode-activation) | C1-C4 mapping to mode selection |
| [Mode Application to Verification Activities](#mode-application-to-verification-activities) | How each mode maps to NPR 7123.1D Process 7/8 activities |
| [Output Format for Adversarial V&V Findings](#output-format-for-adversarial-v&v-findings) | Structured finding schema |
| [Review Gate Integration](#review-gate-integration) | Per-gate adversarial behavior at TRR and CDR |
| [Enforcement Integration](#enforcement-integration) | How modes consume enforcement layer data |
| [Session Context Extensions](#session-context-extensions) | Additions to the v1.0.0 session context schema |
| [Backward Compatibility](#backward-compatibility) | How existing nse-verification behavior is preserved |
| [Traceability](#traceability) | Mapping to TASK-001 requirements |
| [References](#references) | Source citations |

---

## Summary

This document designs the adversarial integration for the nse-verification agent (v2.1.0). The design introduces 4 adversarial modes and 1 always-on pre-step that enhance the agent's V&V capabilities without modifying its existing behavior. Each mode maps one or more of the 10 selected adversarial strategies (ADR-EPIC002-001) to specific verification activities in NPR 7123.1D Processes 7 and 8.

The design satisfies requirements FR-305-001 through FR-305-009 from TASK-001 and is structured as an additive layer: existing nse-verification invocations without adversarial mode flags produce identical output to v2.1.0 (BC-305-001).

---

## Design Philosophy

### Additive, Not Replacement

Adversarial modes are **opt-in capabilities** activated by explicit mode flags or by criticality-based auto-selection. The existing nse-verification workflows (VCRM creation, verification planning, evidence collection) remain the primary path. Adversarial modes provide additional rigor when activated.

### Strategy-to-V&V Mapping Principle

Each adversarial mode applies one or more strategies to a specific V&V activity:

| V&V Activity (NPR 7123.1D) | Adversarial Challenge | Strategy |
|----|----|----|
| Requirements baseline analysis (Process 7, Step 1) | Generate anti-requirements to test baseline completeness | S-013 (Inversion) |
| Evidence evaluation (Process 7, Step 6) | Independently verify factual claims in evidence | S-011 (CoVe) |
| Quality scoring (Process 7/8) | Produce numerical quality score on V&V artifacts | S-014 (LLM-as-Judge) |
| Compliance evaluation (Process 7/8) | Evaluate V&V artifacts against NPR 7123.1D and Jerry constitution | S-007 (Constitutional AI) |
| Self-improvement (all activities) | Self-correct V&V artifacts before external critique | S-010 (Self-Refine) |

---

## Adversarial Mode Definitions

### Mode 1: `adversarial-challenge` (S-013 Inversion)

**Requirement:** FR-305-001

**Purpose:** Generate anti-requirement checklists from the requirements baseline before verification planning. This mode produces "how to guarantee this verification fails" scenarios that become additional verification criteria.

**Activation:**
- Explicit flag: `--mode adversarial-challenge`
- Auto-activation: C3+ criticality when TGT-REQ is the review target type

**Workflow:**
1. Read the requirements baseline from `projects/${JERRY_PROJECT}/requirements/`
2. For each requirement, apply S-013 (Inversion) to generate:
   - The anti-requirement (what would make this requirement impossible to verify)
   - Verification blind spots (what standard verification methods would miss)
   - Edge conditions not covered by the requirement's acceptance criteria
3. Produce an anti-requirement checklist as a structured output
4. Feed the checklist into standard VCRM creation as additional verification criteria

**Token Cost:** ~2,100 tokens per invocation (Ultra-Low tier)

**Preconditions:**
- Requirements baseline exists and is readable
- Artifact maturity is MAT-DRAFT or MAT-REVIEW (anti-requirement generation is inappropriate for approved/baselined artifacts per EN-303 TASK-003 S-013 profile)

**Output:**
```markdown
### Anti-Requirement Checklist (S-013 Inversion)

| Req ID | Anti-Requirement | Verification Blind Spot | Additional Criteria |
|--------|-----------------|------------------------|---------------------|
| REQ-001 | {inverted requirement} | {what standard V-method misses} | {new criterion} |
```

---

### Mode 2: `adversarial-verification` (S-011 CoVe)

**Requirement:** FR-305-002

**Purpose:** Independently verify factual claims in verification evidence before accepting PASS status. This mode applies Chain-of-Verification to ensure evidence actually supports the claimed verification result.

**Activation:**
- Explicit flag: `--mode adversarial-verification`
- Auto-activation: C3+ criticality during PH-VALID phase

**Workflow:**
1. Extract all factual claims from the verification evidence (test reports, analysis reports, inspection reports, demonstration reports)
2. For each claim, generate independent verification questions (per S-011 CoVe protocol)
3. Answer verification questions in a separate context pass (context isolation per S-011 preconditions)
4. Compare independent answers against the original claims
5. Mark claims as VERIFIED, UNVERIFIED, or CONTRADICTED

**Token Cost:** ~6,000 tokens per invocation (Medium tier)

**Preconditions:**
- Verification evidence exists (evidence documents referenced in VCRM)
- TEAM-MULTI or TEAM-HIL composition (context isolation is harder in TEAM-SINGLE per EN-303 TASK-003 S-011 profile)
- TOK-FULL or TOK-CONST budget state (6,000 tokens required)

**Output:**
```markdown
### Factual Verification Report (S-011 CoVe)

| Claim ID | Claim | Verification Question | Independent Answer | Status | Confidence |
|----------|-------|----------------------|-------------------|--------|------------|
| CLM-001 | {factual claim from evidence} | {verification question} | {independent answer} | VERIFIED/UNVERIFIED/CONTRADICTED | HIGH/MEDIUM/LOW |
```

---

### Mode 3: `adversarial-scoring` (S-014 LLM-as-Judge)

**Requirement:** FR-305-003

**Purpose:** Produce a 0.00-1.00 quality score on VCRM completeness, evidence quality, and coverage metrics. This mode applies the S-014 LLM-as-Judge rubric to V&V artifacts.

**Activation:**
- Explicit flag: `--mode adversarial-scoring`
- Auto-activation: C2+ criticality (S-014 is Required at C2+)

**Workflow:**
1. Define the scoring rubric dimensions:
   - **Completeness** (0.00-1.00): Are all requirements in the VCRM? Are all verification methods assigned?
   - **Evidence Quality** (0.00-1.00): Does evidence directly demonstrate requirement satisfaction? Is evidence traceable?
   - **Coverage** (0.00-1.00): What percentage of requirements have PASS status with evidence?
   - **Consistency** (0.00-1.00): Are verification methods appropriate for the requirement type (ADIT)?
   - **Traceability** (0.00-1.00): Bidirectional traceability between requirements and verification evidence?
   - **Rigor** (0.00-1.00): Are verification procedures sufficiently detailed and repeatable?
2. Score each dimension independently with rationale
3. Calculate composite score (weighted average; all dimensions equally weighted)
4. Determine PASS/FAIL against >= 0.92 threshold (per H-13, barrier-2 handoff)

**Token Cost:** ~2,000 tokens per invocation (Ultra-Low tier)

**Preconditions:**
- VCRM artifact exists
- Scoring rubric is calibrated (default rubric provided; custom rubric accepted)

**Output:**
```markdown
### V&V Quality Score (S-014 LLM-as-Judge)

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Completeness | 0.XX | {specific evidence for score} |
| Evidence Quality | 0.XX | {specific evidence for score} |
| Coverage | 0.XX | {specific evidence for score} |
| Consistency | 0.XX | {specific evidence for score} |
| Traceability | 0.XX | {specific evidence for score} |
| Rigor | 0.XX | {specific evidence for score} |
| **Composite** | **0.XX** | **PASS/FAIL (threshold: 0.92)** |
```

---

### Mode 4: `adversarial-compliance` (S-007 Constitutional AI)

**Requirement:** FR-305-004

**Purpose:** Evaluate V&V artifacts against NPR 7123.1D Process 7/8 requirements and Jerry constitutional principles (P-040, P-041).

**Activation:**
- Explicit flag: `--mode adversarial-compliance`
- Auto-activation: C2+ criticality

**Workflow:**
1. Load the constitutional principles applicable to V&V:
   - NPR 7123.1D Process 7: Product Verification (7 steps)
   - NPR 7123.1D Process 8: Product Validation
   - P-040 (Traceability): Bidirectional requirement-verification traceability
   - P-041 (V&V Coverage): All requirements have verification methods
   - P-043 (Disclaimer): Mandatory AI disclaimer on all outputs
   - H-17 (Evidence-Based Closure): Evidence required for PASS status
   - H-18 (Acceptance Criteria Verification): AC verified before closure
2. Evaluate the V&V artifact against each principle
3. Produce a principle-by-principle compliance report (PASS/FAIL/PARTIAL)
4. If S-007 detects violations against HARD rules (H-01 through H-24), flag them with CRITICAL severity

**Token Cost:** ~8,000-16,000 tokens per invocation (Medium tier; varies with principle count and multi-pass depth)

**Preconditions:**
- Constitutional principles are loaded (`.claude/rules/` accessible)
- V&V artifact is sufficiently complete to evaluate

**Output:**
```markdown
### V&V Compliance Report (S-007 Constitutional AI)

| Principle | Requirement | Status | Evidence | Severity |
|-----------|-------------|--------|----------|----------|
| NPR 7123.1D P7 Step 1 | Requirements identified | PASS/FAIL/PARTIAL | {citation} | {severity} |
| P-040 | Bidirectional traceability | PASS/FAIL/PARTIAL | {citation} | {severity} |
| P-041 | V&V coverage | PASS/FAIL/PARTIAL | {citation} | {severity} |
| H-17 | Evidence-based closure | PASS/FAIL/PARTIAL | {citation} | {severity} |
```

---

### Pre-Step: Self-Refine (S-010)

**Requirement:** FR-305-005

**Purpose:** Apply S-010 (Self-Refine) as a pre-step before any adversarial mode invocation, producing a self-corrected V&V artifact before external critique.

**Activation:**
- Always-on when any adversarial mode is invoked (unless explicitly skipped)
- Standalone at C1 criticality (S-010 is the only Required strategy at C1)

**Workflow:**
1. Before invoking any adversarial mode, the agent performs a self-review pass on its V&V output
2. Self-identifies obvious issues: missing evidence references, incomplete VCRM entries, formatting errors, orphan references
3. Self-corrects the artifact
4. Passes the self-corrected version to the requested adversarial mode

**Token Cost:** ~2,000 tokens per invocation (Ultra-Low tier)

**Iteration Limit:** Maximum 3 self-refine iterations (diminishing returns per EN-303 TASK-003 S-010 profile)

---

## Criticality-Based Mode Activation

**Requirement:** FR-305-007

| Criticality | Auto-Activated Modes | Required Strategies | Optional Strategies | Total Token Budget |
|-------------|---------------------|--------------------|--------------------|-------------------|
| **C1** | Self-Refine only | S-010 | S-014 (adversarial-scoring) | 2,000-4,000 |
| **C2** | adversarial-scoring + adversarial-compliance + Self-Refine | S-007, S-014, S-010 | S-003 (Steelman, via separate invocation) | 12,000-20,000 |
| **C3** | adversarial-challenge + adversarial-verification + adversarial-scoring + adversarial-compliance + Self-Refine | S-007, S-014, S-010, S-013, S-011 | S-003, S-002 (via nse-reviewer) | 20,100-28,100 |
| **C4** | All modes active + full strategy complement | All 10 strategies | None -- all deployed | 35,000-55,000 |

**Auto-selection algorithm:**
1. Determine criticality level from PromptReinforcementEngine C1-C4 assessment (FR-305-030)
2. Activate Required strategies for that criticality level
3. If token budget (TOK-CONST or TOK-EXHAUST) prevents full activation, degrade gracefully:
   - Drop Medium-tier strategies first (S-007, S-011)
   - Retain Ultra-Low strategies (S-010, S-014, S-013)
   - At C3+ with TOK-EXHAUST, escalate to human review (P-020)

---

## Mode Application to Verification Activities

### NPR 7123.1D Process 7: Product Verification

| Process 7 Step | Standard Activity | Adversarial Enhancement | Mode | Strategy |
|----------------|------------------|-----------------------|------|----------|
| Step 1: Identify requirements | Read requirements baseline | Generate anti-requirements | adversarial-challenge | S-013 |
| Step 2: Select verification method | Assign A/D/I/T | Validate method appropriateness via compliance check | adversarial-compliance | S-007 |
| Step 3: Determine verification level | Assign Unit/Integration/System | Score level assignment completeness | adversarial-scoring | S-014 |
| Step 4: Develop procedures | Write test/analysis procedures | Self-improve procedure clarity | Self-Refine | S-010 |
| Step 5: Execute activities | Run tests, perform analyses | N/A (execution is not enhanced by adversarial modes) | -- | -- |
| Step 6: Collect evidence | Gather test reports, evidence | Verify factual claims in evidence | adversarial-verification | S-011 |
| Step 7: Analyze results | Evaluate pass/fail | Score results quality and completeness | adversarial-scoring | S-014 |

### NPR 7123.1D Process 8: Product Validation

| Validation Activity | Standard Activity | Adversarial Enhancement | Mode | Strategy |
|---------------------|------------------|-----------------------|------|----------|
| Stakeholder needs mapping | Map needs to validation criteria | Generate anti-needs (what would invalidate the system) | adversarial-challenge | S-013 |
| Validation planning | Define validation approach | Compliance check against NPR 7123.1D | adversarial-compliance | S-007 |
| Validation execution | Perform user acceptance | N/A (execution is human-driven) | -- | -- |
| Results evaluation | Evaluate satisfaction | Score validation completeness | adversarial-scoring | S-014 |

---

## Output Format for Adversarial V&V Findings

**Requirement:** FR-305-006

All adversarial modes produce findings in the following structured format, designed to integrate with the EnforcementDecision dataclass pattern from the barrier-2 handoff:

```markdown
### Adversarial V&V Finding: {Finding ID}

| Attribute | Value |
|-----------|-------|
| **Finding ID** | AVF-{mode_prefix}-{NNN} |
| **Mode** | adversarial-challenge / adversarial-verification / adversarial-scoring / adversarial-compliance |
| **Strategy** | S-{NNN} ({Strategy Name}) |
| **Severity** | CRITICAL / MAJOR / MINOR / INFO |
| **Requirement** | {requirement being verified, e.g., REQ-001} |
| **Evidence** | {citation to specific evidence supporting the finding} |
| **Remediation** | {specific recommendation for addressing the finding} |
| **Traceability** | {traces to FR-305-XXX, NPR 7123.1D section, HARD rule ID} |
```

**Finding ID Prefixes:**
- `AVF-CHG-` for adversarial-challenge findings
- `AVF-VER-` for adversarial-verification findings
- `AVF-SCR-` for adversarial-scoring findings
- `AVF-CMP-` for adversarial-compliance findings

**Severity Classification (aligned with nse-qa severity levels):**
- **CRITICAL:** Blocks V&V completion; HARD rule violation; evidence contradicts claim
- **MAJOR:** Significant quality gap; requirement without verification method; missing evidence
- **MINOR:** Quality enhancement opportunity; incomplete traceability; formatting issue
- **INFO:** Observation; suggestion for improvement; positive finding

---

## Review Gate Integration

### TRR (Test Readiness Review) Gate

**Requirement:** FR-305-008

At TRR, nse-verification adversarial findings SHALL include:

| TRR Deliverable | Adversarial Mode | Metrics Produced |
|-----------------|-----------------|------------------|
| Verification procedure completeness score | adversarial-scoring (S-014) | 0.00-1.00 score on procedure completeness dimension |
| Evidence quality score | adversarial-scoring (S-014) | 0.00-1.00 score on evidence quality dimension |
| Coverage gap enumeration | adversarial-challenge (S-013) | List of requirements without verification coverage, with risk assessment per gap |
| Factual verification of test claims | adversarial-verification (S-011) | VERIFIED/UNVERIFIED/CONTRADICTED per evidence claim |

**TRR Adversarial Package:**
```markdown
## Adversarial V&V Assessment for TRR

### Procedure Completeness: {score}/1.00
### Evidence Quality: {score}/1.00
### Coverage Gaps: {count} requirements without verification
### Factual Verification: {verified_count}/{total_claims} claims verified

### Findings
{Structured findings per output format above}

### TRR Readiness Determination
**Adversarial Assessment:** Ready / Not Ready / Conditional
**Rationale:** {Based on composite score vs. 0.92 threshold and critical findings}
```

### CDR (Critical Design Review) Gate

**Requirement:** FR-305-009

At CDR, nse-verification adversarial findings SHALL include:

| CDR Deliverable | Adversarial Mode | Metrics Produced |
|-----------------|-----------------|------------------|
| Verification approach maturity | adversarial-compliance (S-007) | Compliance score against NPR 7123.1D Process 7 steps 1-4 |
| Procedure readiness score | adversarial-scoring (S-014) | 0.00-1.00 score on procedure readiness |
| Requirements-to-verification traceability completeness | adversarial-challenge (S-013) | Anti-requirement coverage analysis identifying traceability gaps |

---

## Enforcement Integration

**Requirements:** FR-305-030, FR-305-031, FR-305-032, FR-305-033

### Consuming Enforcement Layer Data

| Integration Point | Source | How nse-verification Consumes It |
|-------------------|--------|----------------------------------|
| C1-C4 criticality assessment | PromptReinforcementEngine (L2) | Determines which adversarial modes to auto-activate (see criticality table above) |
| EnforcementDecision dataclass | PreToolEnforcementEngine (L3) | Adversarial findings are structured to match the `action/reason/violations/criticality_escalation` schema for downstream consumption |
| 24 HARD rules (H-01 through H-24) | quality-enforcement.md SSOT (L1) | When adversarial-compliance mode (S-007) is active, it validates V&V artifacts against all applicable HARD rules |
| 6 effective HARD language patterns | barrier-2 handoff | Adversarial finding reports use effective patterns (Constitutional Constraint, Forbidden/Required Binary, Quality Gate Declaration) |
| Governance file escalation | PreToolEnforcementEngine (L3) | If nse-verification reviews artifacts that modify governance files (`.claude/rules/`, `JERRY_CONSTITUTION.md`), auto-escalate to C3+ (FR-305-034) |

### Producing Enforcement-Compatible Output

Adversarial findings are structured so that downstream consumers (quality gates, orchestrators, nse-reviewer) can process them as enforcement decisions:

```yaml
adversarial_finding:
  action: "block"  # or "warn" or "pass"
  reason: "VCRM entry for REQ-001 claims PASS but evidence TR-001 contradicts claimed response time"
  violations:
    - "FR-305-002: Factual claim verification failure"
    - "H-17: Evidence-based closure violated"
  criticality_escalation: null  # or "C3" / "C4" if governance file affected
```

---

## Session Context Extensions

**Requirement:** NFR-305-008

The existing nse-verification session context schema (v1.0.0) is extended with adversarial-specific fields. Existing fields are preserved (BC-305-004).

```yaml
verification_output:
  # Existing fields (preserved)
  project_id: "{project_id}"
  entry_id: "{entry_id}"
  artifact_path: "projects/{project}/verification/{filename}.md"
  summary: "{verification status summary}"
  coverage_percent: {percent}
  pass_count: {count}
  fail_count: {count}
  gap_count: {count}
  review_ready: "{PDR|CDR|TRR|None}"
  next_agent_hint: "nse-reviewer"
  nasa_processes_applied: ["Process 7", "Process 8"]

  # NEW: Adversarial extension fields
  adversarial:
    modes_applied: ["adversarial-scoring", "adversarial-compliance"]
    strategies_applied: ["S-014", "S-007", "S-010"]
    criticality_level: "C2"
    composite_quality_score: 0.94
    quality_gate_result: "PASS"
    finding_counts:
      critical: 0
      major: 1
      minor: 3
      info: 2
    anti_requirements_generated: 0  # Count from adversarial-challenge
    claims_verified: 0              # Count from adversarial-verification
    claims_contradicted: 0          # Count from adversarial-verification
```

---

## Backward Compatibility

**Requirement:** BC-305-001

| Aspect | Guarantee |
|--------|-----------|
| Default invocation | nse-verification invoked without `--mode` flags produces identical output to v2.1.0 |
| Session context schema | All existing fields preserved; adversarial fields are additive (default to `null` if no adversarial modes applied) |
| VCRM template | Existing VCRM template and output structure unchanged; adversarial findings appear as additional sections appended after L2 output |
| Cross-reference validation | FIX-NEG-005 cross-reference validation behavior unchanged |
| L0/L1/L2 output levels | Adversarial findings integrated into existing output levels (L1 for findings, L2 for quality scores); no L3 or L4 levels added (BC-305-005) |

---

## Traceability

| TASK-001 Requirement | How Addressed |
|---------------------|--------------|
| FR-305-001 | adversarial-challenge mode defined (S-013 Inversion anti-requirement checklists) |
| FR-305-002 | adversarial-verification mode defined (S-011 CoVe factual claim verification) |
| FR-305-003 | adversarial-scoring mode defined (S-014 LLM-as-Judge 0.00-1.00 quality score) |
| FR-305-004 | adversarial-compliance mode defined (S-007 Constitutional AI against NPR 7123.1D and P-040/P-041) |
| FR-305-005 | Self-Refine pre-step defined (S-010 always-on before adversarial modes) |
| FR-305-006 | Output format defined with finding ID, severity, evidence, remediation, traceability |
| FR-305-007 | Criticality-based mode activation table (C1-C4) with graceful degradation |
| FR-305-008 | TRR gate integration defined with procedure completeness, evidence quality, coverage gaps |
| FR-305-009 | CDR gate integration defined with verification approach maturity, procedure readiness, traceability completeness |
| FR-305-030 | Enforcement integration: C1-C4 assessment consumed from PromptReinforcementEngine |
| FR-305-031 | Finding output structured to match EnforcementDecision dataclass |
| FR-305-032 | adversarial-compliance mode validates against 24 HARD rules |
| FR-305-033 | Findings use 6 effective HARD language patterns |
| FR-305-034 | Governance file escalation triggers C3+ auto-escalation |
| NFR-305-008 | Session context extended with adversarial fields preserving v1.0.0 schema |
| BC-305-001 | Default invocation produces identical v2.1.0 output |

---

## References

| # | Citation | Sections Referenced |
|---|----------|-------------------|
| 1 | TASK-001 (Requirements) -- FEAT-004:EN-305:TASK-001 | FR-305-001 through FR-305-009, FR-305-030 through FR-305-035, NFR-305-008, BC-305-001 |
| 2 | ADR-EPIC002-001 (ACCEPTED) -- FEAT-004:EN-302:TASK-005 | 10 selected strategies, quality layers, token tiers |
| 3 | EN-303 TASK-001 -- FEAT-004:EN-303:TASK-001 | C1-C4 criticality levels, dimension codes |
| 4 | EN-303 TASK-003 -- FEAT-004:EN-303:TASK-003 | Per-strategy profiles (S-013, S-011, S-014, S-007, S-010) |
| 5 | Barrier-2 ENF-to-ADV Handoff -- EPIC002-CROSSPOLL-B2-ENF-TO-ADV | EnforcementDecision dataclass, 24 HARD rules, 6 effective patterns, governance escalation |
| 6 | nse-verification agent spec -- `skills/nasa-se/agents/nse-verification.md` v2.1.0 | Current capabilities, session context schema, VCRM template |

---

*Document ID: FEAT-004:EN-305:TASK-002*
*Agent: nse-architecture-305*
*Created: 2026-02-13*
*Status: Complete*
