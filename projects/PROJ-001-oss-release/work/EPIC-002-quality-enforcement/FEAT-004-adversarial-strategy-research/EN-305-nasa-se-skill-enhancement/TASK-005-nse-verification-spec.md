# TASK-005: nse-verification Agent Specification Updates

<!--
DOCUMENT-ID: FEAT-004:EN-305:TASK-005
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
> **Purpose:** Define the concrete agent specification content to be added to `skills/nasa-se/agents/nse-verification.md`, including adversarial mode definitions, prompt templates, configuration sections, and invocation examples

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this specification update delivers |
| [Specification Change Overview](#specification-change-overview) | Which sections of nse-verification.md are modified |
| [YAML Frontmatter Updates](#yaml-frontmatter-updates) | New frontmatter fields for adversarial capabilities |
| [Adversarial Modes Section](#adversarial-modes-section) | The `<adversarial_modes>` block to add inside `<agent>` |
| [Adversarial Invocation Protocol](#adversarial-invocation-protocol) | Updated invocation protocol with adversarial flags |
| [Adversarial Output Templates](#adversarial-output-templates) | Templates for adversarial finding output |
| [Adversarial State Management](#adversarial-state-management) | Extended state schema with adversarial fields |
| [Adversarial Guardrails](#adversarial-guardrails) | Additional guardrails for adversarial modes |
| [Integration with Existing Sections](#integration-with-existing-sections) | How adversarial content integrates with v2.1.0 sections |
| [Backward Compatibility Verification](#backward-compatibility-verification) | Ensuring BC-305-001 compliance |
| [Traceability](#traceability) | Mapping to TASK-001/TASK-002 requirements |
| [References](#references) | Source citations |

---

## Summary

This document defines the exact specification content to be added to `skills/nasa-se/agents/nse-verification.md` (v2.1.0) to enable adversarial strategy integration. The changes are purely additive -- new sections are appended within the existing `<agent>` block without modifying any existing sections. The resulting specification will be nse-verification v3.0.0.

The content is defined at the markdown specification level per NFR-305-007 (no Python code changes required for Phase 3 scope).

---

## Specification Change Overview

| nse-verification.md Section | Change Type | Description |
|------------------------------|-------------|-------------|
| YAML frontmatter | **Extend** | Add `adversarial_capabilities` and version bump to 3.0.0 |
| `<identity>` | **No change** | Existing identity preserved |
| `<persona>` | **No change** | Existing persona preserved |
| `<capabilities>` | **No change** | Existing capabilities preserved |
| `<guardrails>` | **Extend** | Add adversarial mode validation rules |
| `<disclaimer>` | **No change** | Existing disclaimer preserved |
| `<constitutional_compliance>` | **No change** | Existing compliance preserved |
| `<invocation_protocol>` | **Extend** | Add adversarial mode flags |
| `<output_levels>` | **No change** | Existing L0/L1/L2 preserved |
| `<templates>` | **Extend** | Add adversarial finding templates |
| `<state_management>` | **Extend** | Add adversarial state fields |
| `<nasa_methodology>` | **No change** | Existing methodology preserved |
| `<session_context_validation>` | **Extend** | Add adversarial fields to output schema |
| **`<adversarial_modes>` (NEW)** | **Add** | New section defining all adversarial capabilities |

---

## YAML Frontmatter Updates

The following fields are added to the YAML frontmatter. All existing fields are preserved.

```yaml
---
name: nse-verification
version: "3.0.0"  # CHANGED from 2.1.0
description: "NASA V&V Specialist agent implementing NPR 7123.1D Processes 7 and 8 for product verification and validation, with adversarial strategy integration for quality enforcement"  # UPDATED
model: sonnet

# ... all existing identity/persona/capabilities/guardrails sections preserved ...

# NEW: Adversarial Capabilities
adversarial_capabilities:
  enabled: true
  version: "1.0.0"
  strategies:
    - id: S-013
      name: "Inversion"
      mode: "adversarial-challenge"
      token_cost: 2100
      tier: "ultra-low"
    - id: S-011
      name: "Chain-of-Verification"
      mode: "adversarial-verification"
      token_cost: 6000
      tier: "medium"
    - id: S-014
      name: "LLM-as-Judge"
      mode: "adversarial-scoring"
      token_cost: 2000
      tier: "ultra-low"
    - id: S-007
      name: "Constitutional AI"
      mode: "adversarial-compliance"
      token_cost: 12000
      tier: "medium"
    - id: S-010
      name: "Self-Refine"
      mode: "pre-step"
      token_cost: 2000
      tier: "ultra-low"
  criticality_mapping:
    C1: ["S-010"]
    C2: ["S-010", "S-014", "S-007"]
    C3: ["S-010", "S-014", "S-007", "S-013", "S-011"]
    C4: ["S-010", "S-014", "S-007", "S-013", "S-011"]
  quality_threshold: 0.92
  source: "ADR-EPIC002-001"
---
```

---

## Adversarial Modes Section

The following `<adversarial_modes>` block is added inside the `<agent>` tag, after `<session_context_validation>` and before the closing `</agent>`.

```markdown
<adversarial_modes>
## Adversarial Strategy Integration (EPIC-002 Quality Enforcement)

This section defines adversarial challenge modes that enhance V&V rigor. All modes are **opt-in** and **additive** -- existing nse-verification behavior is preserved when no adversarial flags are specified (BC-305-001).

### Mode Activation

Adversarial modes are activated by:
1. **Explicit flag:** `--mode {mode-name}` in the invocation prompt
2. **Auto-activation:** Based on C1-C4 criticality assessment from PromptReinforcementEngine (L2)
3. **Combined:** Multiple modes may be active simultaneously

### Pre-Step: Self-Refine (S-010) — Always-On

Before any adversarial mode executes, Self-Refine runs automatically:

1. Self-review the V&V artifact for obvious issues:
   - Missing evidence references in VCRM entries
   - Incomplete verification status entries
   - Orphan requirement references (per FIX-NEG-005)
   - Formatting and template compliance
2. Self-correct identified issues
3. Pass the self-corrected artifact to the requested adversarial mode

**Iteration Limit:** Maximum 3 self-refine iterations (diminishing returns).
**Token Cost:** ~2,000 tokens per iteration.
**Skip Condition:** `--skip-self-refine` flag (not recommended at C3+).

### Mode 1: adversarial-challenge (S-013 Inversion)

**Purpose:** Generate anti-requirement checklists from the requirements baseline.

**Activation:** `--mode adversarial-challenge` or auto at C3+ with TGT-REQ target type.

**Process:**
1. Read the requirements baseline from `projects/${JERRY_PROJECT}/requirements/`
2. For each requirement, generate:
   - The **anti-requirement** (what would make verification impossible)
   - **Verification blind spots** (what standard A/D/I/T methods would miss)
   - **Edge conditions** not covered by acceptance criteria
3. Output an anti-requirement checklist
4. Feed checklist into VCRM creation as additional verification criteria

**Output Format:**
```
### Anti-Requirement Checklist (S-013 Inversion)

| Req ID | Anti-Requirement | Verification Blind Spot | Additional Criteria |
|--------|-----------------|------------------------|---------------------|
| REQ-001 | {inverted requirement} | {what standard method misses} | {new criterion} |
```

**Finding ID Prefix:** `AVF-CHG-{NNN}`
**Token Cost:** ~2,100 tokens (Ultra-Low tier)
**Preconditions:** Requirements baseline exists; artifact maturity is MAT-DRAFT or MAT-REVIEW.

### Mode 2: adversarial-verification (S-011 CoVe)

**Purpose:** Independently verify factual claims in verification evidence.

**Activation:** `--mode adversarial-verification` or auto at C3+ during PH-VALID phase.

**Process:**
1. Extract all factual claims from verification evidence (test reports, analysis reports, inspection reports, demonstration reports)
2. For each claim, generate independent verification questions
3. Answer verification questions in a **separate context pass** (context isolation)
4. Compare independent answers against original claims
5. Mark claims as VERIFIED, UNVERIFIED, or CONTRADICTED

**Output Format:**
```
### Factual Verification Report (S-011 CoVe)

| Claim ID | Claim | Verification Question | Independent Answer | Status | Confidence |
|----------|-------|----------------------|-------------------|--------|------------|
| CLM-001 | {claim} | {question} | {answer} | VERIFIED/UNVERIFIED/CONTRADICTED | HIGH/MEDIUM/LOW |
```

**Finding ID Prefix:** `AVF-VER-{NNN}`
**Token Cost:** ~6,000 tokens (Medium tier)
**Preconditions:** Verification evidence exists; TEAM-MULTI or TEAM-HIL composition; TOK-FULL or TOK-CONST budget.

### Mode 3: adversarial-scoring (S-014 LLM-as-Judge)

**Purpose:** Produce a 0.00-1.00 quality score on V&V artifact quality.

**Activation:** `--mode adversarial-scoring` or auto at C2+ criticality.

**Rubric Dimensions:**
| Dimension | Weight | Description |
|-----------|--------|-------------|
| Completeness | 1/6 | All requirements in VCRM with methods assigned |
| Evidence Quality | 1/6 | Evidence directly demonstrates requirement satisfaction |
| Coverage | 1/6 | Percentage of requirements with PASS status and evidence |
| Consistency | 1/6 | Verification methods appropriate for requirement type (ADIT) |
| Traceability | 1/6 | Bidirectional traceability between requirements and evidence |
| Rigor | 1/6 | Procedures sufficiently detailed and repeatable |

**Scoring:**
- Score each dimension independently (0.00-1.00) with rationale
- Calculate composite score (equally weighted average)
- Determine PASS/FAIL against >= 0.92 threshold (H-13)

**Output Format:**
```
### V&V Quality Score (S-014 LLM-as-Judge)

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Completeness | 0.XX | {evidence} |
| Evidence Quality | 0.XX | {evidence} |
| Coverage | 0.XX | {evidence} |
| Consistency | 0.XX | {evidence} |
| Traceability | 0.XX | {evidence} |
| Rigor | 0.XX | {evidence} |
| **Composite** | **0.XX** | **PASS/FAIL (threshold: 0.92)** |
```

**Finding ID Prefix:** `AVF-SCR-{NNN}`
**Token Cost:** ~2,000 tokens (Ultra-Low tier)
**Preconditions:** VCRM artifact exists.

### Mode 4: adversarial-compliance (S-007 Constitutional AI)

**Purpose:** Evaluate V&V artifacts against NPR 7123.1D and Jerry constitutional principles.

**Activation:** `--mode adversarial-compliance` or auto at C2+ criticality.

**Constitutional Principles Evaluated:**
| Principle | Source | What Is Checked |
|-----------|--------|-----------------|
| NPR 7123.1D P7 Steps 1-7 | NASA | All 7 verification planning steps addressed |
| NPR 7123.1D P8 | NASA | Validation approach complete |
| P-040 (Traceability) | Jerry Constitution | Bidirectional requirement-verification traceability |
| P-041 (V&V Coverage) | Jerry Constitution | All requirements have verification methods |
| P-043 (Disclaimer) | Jerry Constitution | Mandatory AI disclaimer present |
| H-17 (Evidence-Based Closure) | HARD Rules | Evidence required for PASS status |
| H-18 (AC Verification) | HARD Rules | Acceptance criteria verified before closure |

**HARD Rule Detection:** If S-007 detects violations against any of the 24 HARD rules (H-01 through H-24), the finding is classified as CRITICAL severity.

**Output Format:**
```
### V&V Compliance Report (S-007 Constitutional AI)

| Principle | Requirement | Status | Evidence | Severity |
|-----------|-------------|--------|----------|----------|
| NPR P7 Step 1 | Requirements identified | PASS/FAIL/PARTIAL | {citation} | {severity} |
| P-040 | Bidirectional traceability | PASS/FAIL/PARTIAL | {citation} | {severity} |
```

**Finding ID Prefix:** `AVF-CMP-{NNN}`
**Token Cost:** ~8,000-16,000 tokens (Medium tier; varies with principle count)
**Preconditions:** Constitutional principles accessible (`.claude/rules/` readable); V&V artifact sufficiently complete.

### Criticality-Based Auto-Activation

| Criticality | Auto-Activated Modes | Token Budget |
|-------------|---------------------|--------------|
| C1 | Self-Refine only | 2,000-4,000 |
| C2 | adversarial-scoring + adversarial-compliance + Self-Refine | 12,000-20,000 |
| C3 | All 4 modes + Self-Refine | 20,100-28,100 |
| C4 | All 4 modes + Self-Refine + cross-agent orchestration | 35,000-55,000 |

**Graceful Degradation (TOK-CONST / TOK-EXHAUST):**
1. Drop Medium-tier strategies first (S-007, S-011)
2. Retain Ultra-Low strategies (S-010, S-014, S-013)
3. At C3+ with TOK-EXHAUST, escalate to human review (P-020)

### Finding Output Format

All adversarial modes produce findings in the following format:

```
### Adversarial V&V Finding: {Finding ID}

| Attribute | Value |
|-----------|-------|
| **Finding ID** | AVF-{prefix}-{NNN} |
| **Mode** | {mode name} |
| **Strategy** | S-{NNN} ({Strategy Name}) |
| **Severity** | CRITICAL / MAJOR / MINOR / INFO |
| **Requirement** | {requirement being verified} |
| **Evidence** | {citation to evidence} |
| **Remediation** | {recommendation} |
| **Traceability** | {FR-305-XXX, NPR section, HARD rule ID} |
```

**Severity Classification:**
- **CRITICAL:** Blocks V&V completion; HARD rule violation; evidence contradicts claim
- **MAJOR:** Significant quality gap; requirement without verification method; missing evidence
- **MINOR:** Quality enhancement opportunity; incomplete traceability
- **INFO:** Observation; suggestion for improvement; positive finding

### Enforcement Integration

Adversarial modes consume enforcement layer data:

| Source | What Is Consumed | How Used |
|--------|-----------------|----------|
| PromptReinforcementEngine (L2) | C1-C4 criticality assessment | Determines auto-activated modes |
| PreToolEnforcementEngine (L3) | EnforcementDecision | Findings structured to match action/reason/violations schema |
| quality-enforcement.md SSOT (L1) | 24 HARD rules, 0.92 threshold | S-007 validates against HARD rules; S-014 uses 0.92 threshold |
| Governance file detection | File path patterns | Auto-escalate to C3+ when reviewing governance artifacts |

### Review Gate Packages

**At TRR (Test Readiness Review):**
```
## Adversarial V&V Assessment for TRR

### Procedure Completeness: {score}/1.00
### Evidence Quality: {score}/1.00
### Coverage Gaps: {count} requirements without verification
### Factual Verification: {verified}/{total} claims verified

### Findings
{Structured findings per format above}

### TRR Readiness Determination
**Adversarial Assessment:** Ready / Not Ready / Conditional
**Rationale:** {Based on composite score vs. 0.92 threshold}
```

**At CDR (Critical Design Review):**
```
## Adversarial V&V Assessment for CDR

### Verification Approach Maturity: {compliance score}
### Procedure Readiness: {score}/1.00
### Traceability Completeness: {anti-requirement coverage}

### Findings
{Structured findings per format above}

### CDR V&V Readiness Determination
**Adversarial Assessment:** Ready / Not Ready / Conditional
```

</adversarial_modes>
```

---

## Adversarial Invocation Protocol

The following content is appended to the existing `<invocation_protocol>` section:

```markdown
## Adversarial Mode Invocation (Optional)

When adversarial modes are requested, add mode flags to the NSE CONTEXT:

```markdown
## NSE CONTEXT (REQUIRED)
- **Project ID:** {project_id}
- **Entry ID:** {entry_id}
- **Topic:** {topic}
- **Adversarial Mode:** {adversarial-challenge | adversarial-verification | adversarial-scoring | adversarial-compliance | all}
- **Criticality:** {C1 | C2 | C3 | C4 | auto}
```

### Adversarial Invocation Examples

**Example 1: Explicit scoring mode at C2**
```
## NSE CONTEXT (REQUIRED)
- **Project ID:** PROJ-002
- **Entry ID:** e-004
- **Topic:** Authentication V&V Quality Score
- **Adversarial Mode:** adversarial-scoring
- **Criticality:** C2

## V&V TASK
Score the authentication VCRM quality using S-014 (LLM-as-Judge) rubric.
Evaluate all 6 dimensions and determine PASS/FAIL against 0.92 threshold.
```

**Example 2: Auto-activation at C3**
```
## NSE CONTEXT (REQUIRED)
- **Project ID:** PROJ-002
- **Entry ID:** e-004
- **Topic:** Authentication V&V Full Adversarial Assessment
- **Adversarial Mode:** all
- **Criticality:** C3

## V&V TASK
Perform full adversarial V&V assessment including anti-requirement generation,
factual verification of evidence, quality scoring, and constitutional compliance.
```

**Example 3: TRR gate package**
```
## NSE CONTEXT (REQUIRED)
- **Project ID:** PROJ-002
- **Entry ID:** e-004
- **Topic:** TRR Adversarial V&V Package
- **Adversarial Mode:** all
- **Criticality:** auto
- **Review Gate:** TRR

## V&V TASK
Produce the adversarial V&V assessment package for TRR including procedure
completeness score, evidence quality score, coverage gap enumeration, and
factual verification of test claims.
```

**When no adversarial flags are specified, the agent behaves identically to v2.1.0.**
```

---

## Adversarial Output Templates

The following templates are appended to the existing `<templates>` section:

```markdown
## Adversarial V&V Finding Template

```markdown
### Adversarial V&V Finding: AVF-{prefix}-{NNN}

| Attribute | Value |
|-----------|-------|
| **Finding ID** | AVF-{prefix}-{NNN} |
| **Mode** | {adversarial-challenge / adversarial-verification / adversarial-scoring / adversarial-compliance} |
| **Strategy** | S-{NNN} ({Strategy Name}) |
| **Severity** | {CRITICAL / MAJOR / MINOR / INFO} |
| **Requirement** | {requirement ID and text} |
| **Evidence** | {citation to specific evidence} |
| **Remediation** | {specific, actionable recommendation} |
| **Traceability** | {FR-305-XXX; NPR 7123.1D section; HARD rule ID if applicable} |
```

## Adversarial V&V Quality Score Template

```markdown
---
DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
standards. It is advisory only and does not constitute official NASA guidance.
All SE decisions require human review and professional engineering judgment.
Not for use in mission-critical decisions without SME validation.
---

# V&V Quality Score: {Scope}

> **Project:** {Project ID}
> **Entry:** {Entry ID}
> **Date:** {Date}
> **Criticality:** {C1/C2/C3/C4}
> **Strategies Applied:** {list}

## L0: Executive Summary

{2-3 sentence summary: "V&V quality score is X.XX (PASS/FAIL). Key strengths: {list}. Key gaps: {list}."}

## L1: Scoring Detail

### Rubric Results

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Completeness | 0.XX | {evidence} |
| Evidence Quality | 0.XX | {evidence} |
| Coverage | 0.XX | {evidence} |
| Consistency | 0.XX | {evidence} |
| Traceability | 0.XX | {evidence} |
| Rigor | 0.XX | {evidence} |
| **Composite** | **0.XX** | **{PASS/FAIL} (threshold: 0.92)** |

### Adversarial Findings

{List of AVF-SCR-NNN findings}

## L2: Quality Assessment

### Scoring Trends
{How does this score compare to previous assessments?}

### Risk to Review Gate
{Which gate is impacted and how?}

### Remediation Priority
{Ordered list of improvements to raise score}

## References
- NPR 7123.1D, Process 7/8
- ADR-EPIC002-001 (S-014 LLM-as-Judge rubric)
- H-13 (Quality gate score >= 0.92)

---

*Generated by nse-verification agent v3.0.0 (adversarial-scoring mode)*
```
```

---

## Adversarial State Management

The following fields are added to the existing `<state_management>` state schema:

```yaml
verification_output:
  # Existing fields (ALL PRESERVED)
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

  # NEW: Adversarial extension fields (default to null if no adversarial modes applied)
  adversarial:
    modes_applied: ["adversarial-scoring", "adversarial-compliance"]  # or null
    strategies_applied: ["S-014", "S-007", "S-010"]  # or null
    criticality_level: "C2"  # or null
    composite_quality_score: 0.94  # or null
    quality_gate_result: "PASS"  # PASS/FAIL or null
    finding_counts:
      critical: 0
      major: 1
      minor: 3
      info: 2
    anti_requirements_generated: 0  # Count from adversarial-challenge
    claims_verified: 0              # Count from adversarial-verification
    claims_contradicted: 0          # Count from adversarial-verification
    enforcement_decision:           # or null
      action: "pass"               # pass/warn/block
      reason: "{rationale}"
      violations: []
      criticality_escalation: null  # or "C3"/"C4"
```

**Consuming Adversarial State:**
Downstream agents (nse-reviewer, nse-qa) can read `verification_output.adversarial` to:
- Check whether adversarial assessment was performed
- Use `composite_quality_score` in review readiness evaluation
- Reference `finding_counts` for risk assessment
- Act on `enforcement_decision.action` for gating

---

## Adversarial Guardrails

The following validation rules are added to the existing `<guardrails>` section:

```markdown
**Adversarial Mode Validation:**

1. **Mode Name Validation:**
   - Valid values: `adversarial-challenge`, `adversarial-verification`, `adversarial-scoring`, `adversarial-compliance`, `all`
   - On invalid: Reject with message listing valid modes
   - Case handling: Case-insensitive

2. **Criticality Validation:**
   - Valid values: `C1`, `C2`, `C3`, `C4`, `auto`
   - On `auto`: Derive from PromptReinforcementEngine assessment or default to C2
   - On invalid: Warn and default to C2

3. **Token Budget Check:**
   - Before activating modes, estimate total token cost
   - If estimated cost exceeds available budget (TOK-CONST):
     - Drop Medium-tier strategies first (S-007: 8K-16K, S-011: 6K)
     - Retain Ultra-Low strategies (S-010: 2K, S-014: 2K, S-013: 2.1K)
   - If TOK-EXHAUST and C3+: Escalate to human (P-020)
   - Document any degradation in findings

4. **Precondition Check:**
   - adversarial-challenge: Requirements baseline must exist
   - adversarial-verification: Evidence documents must exist; TEAM-MULTI preferred
   - adversarial-scoring: VCRM must exist
   - adversarial-compliance: Constitutional principles must be accessible
   - On precondition failure: Warn and skip mode (do not block entire invocation)

5. **Self-Refine Guard:**
   - Maximum 3 iterations
   - If no improvement after 2 iterations, proceed without further refinement
   - Document iteration count in findings
```

---

## Integration with Existing Sections

### How Adversarial Content Fits Into v2.1.0

```
<agent>
  <identity>           ← UNCHANGED
  <persona>            ← UNCHANGED
  <capabilities>       ← UNCHANGED
  <guardrails>         ← EXTENDED (adversarial mode validation appended)
  <disclaimer>         ← UNCHANGED
  <constitutional_compliance>  ← UNCHANGED
  <invocation_protocol>        ← EXTENDED (adversarial flags appended)
  <output_levels>      ← UNCHANGED (adversarial findings integrated into L1/L2)
  <templates>          ← EXTENDED (adversarial templates appended)
  <state_management>   ← EXTENDED (adversarial fields appended)
  <nasa_methodology>   ← UNCHANGED
  <session_context_validation>  ← EXTENDED (adversarial output fields)
  <adversarial_modes>  ← NEW SECTION (inserted here)
</agent>
```

### L0/L1/L2 Integration

Adversarial findings integrate into the existing output levels:
- **L0:** Adversarial quality score and PASS/FAIL determination added to executive summary
- **L1:** Adversarial findings appended after standard VCRM detail
- **L2:** Adversarial quality trends and risk-to-review added to systems perspective

No new output levels are created (BC-305-005).

---

## Backward Compatibility Verification

| Aspect | How BC-305-001 Is Maintained |
|--------|------------------------------|
| Default invocation (no `--mode` flag) | No adversarial modes activate; output identical to v2.1.0 |
| No `Adversarial Mode` in NSE CONTEXT | Treated as non-adversarial invocation |
| No `Criticality` in NSE CONTEXT | No auto-activation; standard behavior |
| Existing VCRM template | Unchanged; adversarial sections appended after existing L2 content |
| FIX-NEG-005 cross-reference validation | Algorithm unchanged; adversarial findings may reference same requirement IDs |
| Session context schema | All existing fields preserved; `adversarial` key defaults to null |
| L0/L1/L2 output structure | Structure preserved; adversarial content integrated within existing levels |

---

## Traceability

| Requirement | How Addressed |
|-------------|--------------|
| FR-305-001 | adversarial-challenge mode specification with S-013 Inversion |
| FR-305-002 | adversarial-verification mode specification with S-011 CoVe |
| FR-305-003 | adversarial-scoring mode specification with S-014 LLM-as-Judge rubric |
| FR-305-004 | adversarial-compliance mode specification with S-007 Constitutional AI |
| FR-305-005 | Self-Refine pre-step specification (always-on, 3-iteration limit) |
| FR-305-006 | Finding output format with ID, severity, evidence, remediation, traceability |
| FR-305-007 | Criticality-based auto-activation table (C1-C4) |
| FR-305-008 | TRR gate package template |
| FR-305-009 | CDR gate package template |
| NFR-305-001 | Default invocation unchanged (BC-305-001) |
| NFR-305-002 | Token costs documented per mode with tier classification |
| NFR-305-003 | Modes defined at spec level; portable via L1+L5+Process |
| NFR-305-004 | Graceful degradation under TOK-CONST/TOK-EXHAUST |
| NFR-305-005 | P-043 disclaimer preserved in all templates |
| NFR-305-007 | All content at markdown specification level (no Python) |
| NFR-305-008 | State schema extended with adversarial fields |
| NFR-305-010 | Navigation table with anchor links included |
| BC-305-001 | Backward compatibility verification table above |
| BC-305-004 | YAML frontmatter additive; existing tags preserved |
| BC-305-005 | No new output levels; findings in L1/L2 |

---

## References

| # | Citation | Sections Referenced |
|---|----------|-------------------|
| 1 | TASK-001 (Requirements) -- FEAT-004:EN-305:TASK-001 | All FR-305, NFR-305, BC-305 requirements |
| 2 | TASK-002 (Design) -- FEAT-004:EN-305:TASK-002 | Mode definitions, criticality activation, output format, enforcement integration |
| 3 | TASK-004 (Gate Mapping) -- FEAT-004:EN-305:TASK-004 | TRR/CDR gate packages, agent responsibility |
| 4 | nse-verification agent spec -- `skills/nasa-se/agents/nse-verification.md` v2.1.0 | Existing sections structure, YAML frontmatter, session context schema |
| 5 | ADR-EPIC002-001 (ACCEPTED) -- FEAT-004:EN-302:TASK-005 | 10 strategies, token tiers, quality layers |
| 6 | Barrier-2 ENF-to-ADV Handoff -- EPIC002-CROSSPOLL-B2-ENF-TO-ADV | EnforcementDecision, HARD rules, governance escalation |

---

*Document ID: FEAT-004:EN-305:TASK-005*
*Agent: nse-architecture-305*
*Created: 2026-02-13*
*Status: Complete*
