# TASK-002: Adversarial Mode Architecture Design for ps-critic

<!--
DOCUMENT-ID: FEAT-004:EN-304:TASK-002
VERSION: 1.0.0
AGENT: ps-architect-304 (creator)
DATE: 2026-02-13
STATUS: Draft
PARENT: EN-304 (Problem-Solving Skill Enhancement)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
ACTIVITY: DESIGN
INPUT: TASK-001 (requirements), ADR-EPIC002-001, EN-303 TASK-003 (strategy profiles), EN-303 TASK-004 (decision tree), Barrier-2 ENF-to-ADV handoff
-->

> **Version:** 1.0.0
> **Agent:** ps-architect-304
> **Quality Target:** >= 0.92
> **Purpose:** Design the adversarial mode architecture for the ps-critic agent -- 10 named modes with prompt templates, evaluation criteria, output formats, applicability metadata, mode switching protocol, multi-mode composition, C1-C4 integration, and ContentBlock priority integration

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this design delivers |
| [Architecture Overview](#architecture-overview) | How adversarial modes integrate into ps-critic |
| [Mode Definition Schema](#mode-definition-schema) | Canonical schema for each adversarial mode |
| [Mode Definitions](#mode-definitions) | All 10 adversarial mode specifications |
| [Mode Switching Protocol](#mode-switching-protocol) | How ps-critic transitions between modes |
| [Multi-Mode Composition](#multi-mode-composition) | How multiple modes execute in sequence |
| [C1-C4 Integration](#c1-c4-integration) | Criticality-to-mode mapping and activation |
| [ContentBlock Priority Integration](#contentblock-priority-integration) | Alignment with L2 reinforcement system |
| [Traceability](#traceability) | Mapping to TASK-001 requirements and source artifacts |
| [References](#references) | Source citations |

---

## Summary

This document defines the adversarial mode architecture for the ps-critic agent. Each of the 10 selected adversarial strategies from ADR-EPIC002-001 becomes a named mode within ps-critic, with its own prompt template, evaluation criteria, output format, and applicability metadata derived from EN-303 TASK-003. The architecture preserves backward compatibility with ps-critic v2.2.0's default behavior while enabling strategy-specific adversarial review through explicit or automatic mode selection.

**Key design decisions:**
- Modes are additive extensions to ps-critic, not replacements for existing behavior
- The default mode (`standard`) maps to current v2.2.0 behavior (BC-304-001)
- Each mode is self-contained: one mode, one prompt template, one output schema
- Multi-mode composition is orchestrator-managed (P-003 compliant)
- Mode activation is driven by C1-C4 criticality (FR-304-006)

---

## Architecture Overview

### Mode Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      ps-critic Agent                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐   ┌──────────────────────────────────────┐   │
│  │ Mode Router  │──>│ Mode Registry                        │   │
│  │              │   │                                      │   │
│  │ Input:       │   │  standard (default, v2.2.0 compat)  │   │
│  │  --mode arg  │   │  self-refine     (S-010)             │   │
│  │  OR          │   │  steelman        (S-003)             │   │
│  │  auto-select │   │  inversion       (S-013)             │   │
│  │  via C1-C4   │   │  constitutional  (S-007)             │   │
│  └──────────────┘   │  devils-advocate (S-002)             │   │
│                     │  pre-mortem      (S-004)             │   │
│                     │  fmea            (S-012)             │   │
│                     │  chain-of-verification (S-011)       │   │
│                     │  llm-as-judge    (S-014)             │   │
│                     │  red-team        (S-001)             │   │
│                     └──────────────────────────────────────┘   │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Shared Infrastructure                                     │  │
│  │  - Quality score calculation (weighted dimensions)        │  │
│  │  - L0/L1/L2 output level generation                      │  │
│  │  - Critique file persistence (P-002)                      │  │
│  │  - Session context validation (WI-SAO-002)                │  │
│  │  - Constitutional compliance checks (P-003, P-020, P-022)│  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Design Principles

| Principle | Implementation | Source |
|-----------|---------------|--------|
| **P-003 Compliance** | Modes execute within ps-critic as a single worker agent; no subagent spawning | NFR-304-001 |
| **Backward Compatibility** | Default `standard` mode preserves v2.2.0 behavior | BC-304-001 |
| **Deterministic Selection** | Mode selection is O(1) fixed-depth lookup on C1-C4 + modifiers | NFR-304-003 |
| **Token Efficiency** | Each mode has a declared token budget; multi-mode pipelines sum budgets | NFR-304-002 |
| **Self-Contained Modes** | Each mode includes its own prompt, criteria, and output schema | FR-304-002 |

---

## Mode Definition Schema

Each adversarial mode follows this canonical schema:

```yaml
mode:
  name: "<kebab-case identifier>"
  strategy_id: "<S-NNN from ADR-EPIC002-001>"
  strategy_name: "<human-readable name>"
  adr_rank: <1-10>
  mechanistic_family: "<from ADR-EPIC002-001>"

  prompt_template: |
    <strategy-specific prompt injected into ps-critic context>

  evaluation_criteria:
    - name: "<dimension name>"
      weight: <0.0-1.0>
      description: "<what to evaluate>"
      scoring_rubric:
        excellent: "<0.9-1.0>"
        good: "<0.7-0.89>"
        acceptable: "<0.5-0.69>"
        needs_work: "<0.3-0.49>"
        poor: "<0.0-0.29>"

  output_format:
    sections:
      - name: "<section name>"
        required: <true|false>
        description: "<what this section contains>"

  applicability:
    target_type_affinity:
      high: [<TGT-xxx codes>]
      medium: [<TGT-xxx codes>]
      low: [<TGT-xxx codes>]
    phase_applicability:
      recommended: [<PH-xxx codes>]
      cautionary: [<PH-xxx codes>]
    criticality_mapping:
      C1: "<required|optional|not_recommended>"
      C2: "<required|optional|not_recommended>"
      C3: "<required|optional|not_recommended>"
      C4: "<required|optional|not_recommended>"
    token_budget: <tokens>
    token_tier: "<Ultra-Low|Low|Low-Medium|Medium>"

  pairing:
    synergistic: [<mode names>]
    compatible: [<mode names>]
    tension: [<mode names>]
    sequencing_notes: "<when this mode should execute relative to others>"
```

---

## Mode Definitions

### Mode 1: `self-refine` (S-010)

**Strategy:** Self-Refine | **Rank:** 7 | **Family:** Iterative Self-Correction

**Prompt Template:**

```
You are operating in SELF-REFINE mode.

Review the artifact below and identify areas where quality can be improved.
Apply iterative self-improvement: read the artifact, identify weaknesses,
and produce specific revision recommendations.

Focus on:
1. Completeness gaps -- what is missing that should be present?
2. Logical inconsistencies -- where does the reasoning break down?
3. Clarity issues -- where is the writing unclear or ambiguous?
4. Evidence gaps -- where are claims unsupported?

For each issue found, provide:
- Location in the artifact
- Specific problem description
- Concrete revision recommendation
- Expected quality improvement

Do NOT provide a quality score in this mode. Scoring is the
responsibility of the llm-as-judge mode (S-014).
```

**Evaluation Criteria:**

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Completeness of Issue Identification | 0.30 | Did the self-refine pass find all significant quality gaps? |
| Specificity of Recommendations | 0.30 | Are revision recommendations concrete and actionable? |
| Logical Coherence | 0.20 | Are the identified issues logically valid? |
| Improvement Potential | 0.20 | Would implementing the recommendations improve quality? |

**Output Format:**

| Section | Required | Description |
|---------|----------|-------------|
| Issue Summary | Yes | Count and severity of issues found |
| Issue Details | Yes | Per-issue: location, description, recommendation, expected impact |
| Revision Priority | Yes | Ordered list of which issues to address first |
| Self-Assessment Confidence | Yes | How confident the agent is in the completeness of its review |

**Applicability:**

| Attribute | Value |
|-----------|-------|
| Target Type Affinity (High) | TGT-CODE, TGT-ARCH, TGT-REQ, TGT-RES, TGT-DEC, TGT-PROC |
| Phase (Recommended) | PH-DESIGN, PH-IMPL, PH-MAINT |
| Phase (Cautionary) | PH-EXPLORE (premature), PH-VALID (scoring preferred) |
| Criticality | C1: required; C2: recommended; C3: recommended; C4: required |
| Token Budget | ~2,000 |
| Token Tier | Ultra-Low |
| Pairing (SYN) | llm-as-judge (S-010 then S-014 scores improvement) |
| Pairing (TEN) | steelman (both improve before critique; scope separate) |

---

### Mode 2: `steelman` (S-003)

**Strategy:** Steelman Technique | **Rank:** 2 | **Family:** Dialectical Synthesis

**Prompt Template:**

```
You are operating in STEELMAN mode.

Before any adversarial critique occurs, reconstruct the artifact's argument
in its STRONGEST possible form. Your job is to:

1. Identify the core thesis or design decision being made
2. Enumerate all assumptions the argument depends on (make implicit
   assumptions explicit)
3. Reconstruct the reasoning chain in its most compelling form
4. Identify the strongest evidence supporting the argument
5. Note any additional arguments that COULD support the position
   but are not stated

Output the steelmanned argument as a structured document. This output
will be consumed by subsequent adversarial modes (devils-advocate,
constitutional, red-team) to ensure they engage with the STRONGEST
version of the argument, not a strawman.

Do NOT critique the argument. Your role is charitable reconstruction only.
```

**Evaluation Criteria:**

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Argument Fidelity | 0.35 | Does the steelman faithfully represent the original argument? |
| Assumption Explicitation | 0.25 | Are implicit assumptions made explicit? |
| Reasoning Completeness | 0.25 | Is the logical chain complete and sound? |
| Charitable Strength | 0.15 | Is the reconstruction genuinely the strongest version? |

**Output Format:**

| Section | Required | Description |
|---------|----------|-------------|
| Core Thesis | Yes | The artifact's central argument in one statement |
| Explicit Assumptions | Yes | All assumptions (stated and implicit) |
| Strongest Reasoning Chain | Yes | The argument reconstructed at maximum strength |
| Supporting Evidence | Yes | Evidence supporting the argument |
| Unstated Supporting Arguments | No | Additional arguments that could strengthen the position |

**Applicability:**

| Attribute | Value |
|-----------|-------|
| Target Type Affinity (High) | TGT-ARCH, TGT-DEC, TGT-RES, TGT-REQ |
| Target Type Affinity (Low) | TGT-CODE (no arguments to steelman) |
| Phase (Recommended) | PH-DESIGN, PH-IMPL |
| Phase (Cautionary) | PH-EXPLORE (no argument formed yet) |
| Criticality | C1: optional; C2: recommended; C3: required; C4: required |
| Token Budget | ~1,600 |
| Token Tier | Ultra-Low |
| Pairing (SYN) | devils-advocate, constitutional, red-team (steelman BEFORE all three) |
| Pairing (TEN) | self-refine (both improve before critique; scope separate) |
| Sequencing | MUST execute before devils-advocate, constitutional, and red-team |

---

### Mode 3: `inversion` (S-013)

**Strategy:** Inversion Technique | **Rank:** 3 | **Family:** Structured Decomposition

**Prompt Template:**

```
You are operating in INVERSION mode.

Instead of asking "how to make this succeed," ask "how to GUARANTEE this fails."
Generate a comprehensive anti-pattern checklist for the artifact:

1. Invert each success criterion into a failure criterion
2. For each design decision, describe what the WORST possible version
   would look like
3. Generate "how to guarantee failure" scenarios
4. Produce an anti-pattern checklist that subsequent review modes
   can evaluate the artifact against
5. Identify blind spots -- failure modes NOT covered by any stated
   success criterion

Output format: structured anti-pattern checklist with severity ratings.
Each anti-pattern should be specific enough to serve as a verification
criterion for other adversarial modes (constitutional, fmea, red-team).
```

**Evaluation Criteria:**

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Anti-Pattern Coverage | 0.30 | Are all plausible failure modes enumerated? |
| Specificity | 0.25 | Are anti-patterns specific enough to serve as verification criteria? |
| Creativity | 0.25 | Did the inversion reveal non-obvious failure modes? |
| Actionability | 0.20 | Can the anti-patterns be checked against the artifact? |

**Output Format:**

| Section | Required | Description |
|---------|----------|-------------|
| Inverted Success Criteria | Yes | Each success criterion expressed as failure condition |
| Anti-Pattern Checklist | Yes | Per-pattern: description, severity, verification method |
| Blind Spot Analysis | Yes | Failure modes not covered by any stated requirement |
| Reusable Verification Criteria | No | Anti-patterns formatted for consumption by other modes |

**Applicability:**

| Attribute | Value |
|-----------|-------|
| Target Type Affinity (High) | TGT-ARCH, TGT-PROC, TGT-DEC, TGT-REQ |
| Phase (Recommended) | PH-EXPLORE, PH-DESIGN |
| Phase (Cautionary) | PH-VALID (generative noise during validation), PH-MAINT |
| Criticality | C1: not recommended; C2: optional; C3: required; C4: required |
| Token Budget | ~2,100 |
| Token Tier | Ultra-Low |
| Pairing (SYN) | constitutional (S-013 first, then S-007 verifies against anti-patterns); fmea (parallel -- different failure analysis angles); pre-mortem (complementary failure framing); red-team (S-013 generates attack surface, S-001 exploits) |

---

### Mode 4: `constitutional` (S-007)

**Strategy:** Constitutional AI Critique | **Rank:** 4 | **Family:** Iterative Self-Correction

**Prompt Template:**

```
You are operating in CONSTITUTIONAL mode.

Evaluate the artifact against Jerry's codified constitutional principles
and standards. Your constitution consists of:

1. HARD rules from quality-enforcement.md (H-01 through H-24)
2. Architecture standards (.context/rules/architecture-standards.md)
3. Coding standards (.context/rules/coding-standards.md)
4. Testing standards (.context/rules/testing-standards.md)
5. Any domain-specific standards relevant to the artifact type

For each applicable principle:
- Evaluate COMPLIANCE: Does the artifact meet this principle?
- Rate as: PASS / PARTIAL / FAIL
- For PARTIAL and FAIL: cite the specific violation with location
- Provide remediation guidance for each violation

Prioritize HARD rules first (H-01 through H-24), then MEDIUM, then SOFT.
A single HARD rule FAIL means the artifact cannot pass the quality gate.
```

**Evaluation Criteria:**

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Principle Coverage | 0.30 | Were all applicable constitutional principles evaluated? |
| Violation Detection Accuracy | 0.30 | Are identified violations genuine (low false positive rate)? |
| Remediation Quality | 0.20 | Are remediation suggestions specific and implementable? |
| Severity Classification | 0.20 | Are HARD/MEDIUM/SOFT violations correctly classified? |

**Output Format:**

| Section | Required | Description |
|---------|----------|-------------|
| Constitutional Compliance Summary | Yes | Overall PASS/PARTIAL/FAIL with counts |
| HARD Rule Evaluation | Yes | H-01 through H-24 evaluation (applicable rules only) |
| MEDIUM Rule Evaluation | Yes | MEDIUM-tier principle evaluation |
| SOFT Rule Evaluation | No | SOFT-tier evaluation (advisory) |
| Violation Details | Yes | Per-violation: principle, location, severity, remediation |
| Compliance Score | Yes | Percentage of applicable principles in PASS status |

**Applicability:**

| Attribute | Value |
|-----------|-------|
| Target Type Affinity (High) | TGT-CODE, TGT-ARCH, TGT-REQ, TGT-DEC, TGT-PROC |
| Phase (Recommended) | PH-IMPL, PH-VALID, PH-MAINT |
| Phase (Cautionary) | PH-EXPLORE (no constitution yet) |
| Criticality | C1: not required; C2: required; C3: required; C4: required |
| Token Budget | ~8,000-16,000 |
| Token Tier | Medium |
| Pairing (SYN) | steelman (S-003 first); inversion (S-013 generates additional criteria); llm-as-judge (S-007 evaluates, S-014 scores); devils-advocate (S-007 compliance, S-002 reasoning) |

---

### Mode 5: `devils-advocate` (S-002)

**Strategy:** Devil's Advocate | **Rank:** 5 | **Family:** Role-Based Adversarialism

**Prompt Template:**

```
You are operating in DEVIL'S ADVOCATE mode.

Assume the role of a skilled adversarial challenger. Your job is to
systematically challenge every assumption, conclusion, and design decision
in the artifact. You are NOT trying to be fair -- you are trying to find
every weakness.

For each major claim or decision in the artifact:
1. Challenge the underlying assumption -- what if this assumption is wrong?
2. Present the strongest counterargument
3. Identify the evidence that would disprove the claim
4. Assess the robustness of the decision under challenge

Ground rules:
- Challenge substance, not style
- Every challenge must be specific and falsifiable
- You must propose at least one concrete alternative for each challenged decision
- If a claim survives your challenge, acknowledge it as robust

NOTE: If steelman mode was run first, challenge the STEELMANNED version,
not the original. This ensures you attack the strongest formulation.
```

**Evaluation Criteria:**

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Challenge Depth | 0.30 | How deeply do challenges probe the artifact's assumptions? |
| Alternative Generation | 0.25 | Are concrete alternatives proposed for challenged decisions? |
| Specificity | 0.25 | Are challenges specific and falsifiable? |
| Fairness | 0.20 | Are challenges substantive (not nitpicking or stylistic)? |

**Output Format:**

| Section | Required | Description |
|---------|----------|-------------|
| Challenged Assumptions | Yes | Each assumption challenged with counterargument |
| Challenged Decisions | Yes | Each major decision challenged with alternatives |
| Robustness Assessment | Yes | Which claims survived challenge (and why) |
| Critical Vulnerabilities | Yes | The most serious weaknesses found |
| Recommended Actions | Yes | Priority-ordered response actions |

**Applicability:**

| Attribute | Value |
|-----------|-------|
| Target Type Affinity (High) | TGT-ARCH, TGT-DEC |
| Target Type Affinity (Medium) | TGT-RES, TGT-REQ, TGT-CODE |
| Phase (Recommended) | PH-DESIGN (highest value), PH-IMPL |
| Criticality | C1: not recommended; C2: required; C3: required; C4: required |
| Token Budget | ~4,600 |
| Token Tier | Low |
| Pairing (SYN) | steelman (S-003 first ensures strongest formulation challenged) |
| Sequencing | MUST execute AFTER steelman when both are in the pipeline |
| Team Note | TEAM-SINGLE: replace with self-refine (self-DA is weak) |

---

### Mode 6: `pre-mortem` (S-004)

**Strategy:** Pre-Mortem Analysis | **Rank:** 6 | **Family:** Role-Based Adversarialism

**Prompt Template:**

```
You are operating in PRE-MORTEM mode.

Imagine it is 6 months from now. The artifact's design/decision has been
implemented and has CATASTROPHICALLY FAILED. Your job is to write the
post-mortem explaining WHY it failed.

For each failure scenario:
1. Describe the failure in narrative form (what happened, who was affected)
2. Trace the root cause back to a specific aspect of the current artifact
3. Identify the warning signs that were visible NOW but were ignored
4. Assess the probability and severity of this failure mode
5. Propose preventive measures that could be added NOW

Focus on:
- Planning fallacy (underestimated effort/complexity)
- Optimism bias (assumed best-case outcomes)
- Missing edge cases (what was not considered)
- Integration failures (what happens at boundaries)
- Temporal risks (what changes over time that invalidates assumptions)
```

**Evaluation Criteria:**

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Failure Scenario Plausibility | 0.30 | Are failure scenarios realistic and probable? |
| Root Cause Tracing | 0.25 | Are root causes traced to specific artifact elements? |
| Preventive Measure Quality | 0.25 | Are proposed preventions concrete and actionable? |
| Bias Coverage | 0.20 | Are planning fallacy, optimism bias, and temporal risks covered? |

**Output Format:**

| Section | Required | Description |
|---------|----------|-------------|
| Failure Narratives | Yes | 3-5 failure scenarios in narrative form |
| Root Cause Analysis | Yes | Per-scenario: specific artifact element causing failure |
| Warning Signs | Yes | Signs visible now that predict each failure |
| Risk Matrix | Yes | Probability x Severity for each scenario |
| Preventive Measures | Yes | Concrete actions to mitigate each scenario |

**Applicability:**

| Attribute | Value |
|-----------|-------|
| Target Type Affinity (High) | TGT-ARCH, TGT-DEC, TGT-PROC |
| Target Type Affinity (Low) | TGT-CODE (too late for concrete code) |
| Phase (Recommended) | PH-EXPLORE, PH-DESIGN |
| Phase (Cautionary) | PH-IMPL (too late), PH-VALID (too late) |
| Criticality | C1: not recommended; C2: not recommended; C3: required; C4: required |
| Token Budget | ~5,600 |
| Token Tier | Low |
| Pairing (SYN) | inversion (complementary -- S-013 structural anti-patterns, S-004 narrative failures); fmea (complementary -- S-004 creative scenarios, S-012 systematic enumeration) |

---

### Mode 7: `fmea` (S-012)

**Strategy:** FMEA (Failure Mode and Effects Analysis) | **Rank:** 8 | **Family:** Structured Decomposition

**Prompt Template:**

```
You are operating in FMEA mode.

Perform a systematic Failure Mode and Effects Analysis on the artifact.
Decompose the artifact into components and for each component:

1. FAILURE MODE: What could go wrong? (one failure mode per row)
2. EFFECT: What is the consequence if this failure occurs?
3. CAUSE: What is the root cause of this failure mode?
4. SEVERITY (S): Rate 1-10 (10 = catastrophic)
5. OCCURRENCE (O): Rate 1-10 (10 = certain to occur)
6. DETECTION (D): Rate 1-10 (10 = undetectable)
7. RPN: Calculate S x O x D (Risk Priority Number)
8. RECOMMENDED ACTION: Mitigation for high-RPN items

Sort the output by RPN descending. Flag any item with RPN > 200 as
requiring immediate attention. Flag any item with Severity >= 8 as
requiring design review regardless of RPN.
```

**Evaluation Criteria:**

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Component Coverage | 0.25 | Are all artifact components analyzed? |
| Failure Mode Completeness | 0.25 | Are plausible failure modes enumerated for each component? |
| Rating Calibration | 0.25 | Are S/O/D ratings internally consistent and well-justified? |
| Action Quality | 0.25 | Are recommended actions concrete and proportionate to RPN? |

**Output Format:**

| Section | Required | Description |
|---------|----------|-------------|
| Component Decomposition | Yes | List of artifact components analyzed |
| FMEA Table | Yes | Full S/O/D/RPN table sorted by RPN descending |
| Critical Items (RPN > 200) | Yes | Items requiring immediate attention |
| High-Severity Items (S >= 8) | Yes | Items requiring design review |
| Recommended Actions | Yes | Per-item mitigation actions |
| Risk Summary | Yes | Aggregate risk assessment |

**Applicability:**

| Attribute | Value |
|-----------|-------|
| Target Type Affinity (High) | TGT-CODE, TGT-ARCH, TGT-PROC |
| Phase (Recommended) | PH-DESIGN, PH-IMPL, PH-MAINT |
| Phase (Cautionary) | PH-EXPLORE (insufficient detail for FMEA) |
| Criticality | C1: not recommended; C2: not recommended; C3: required; C4: required |
| Token Budget | ~9,000 |
| Token Tier | Medium |
| Pairing (SYN) | inversion (parallel -- different failure analysis angles); pre-mortem (S-004 creative, S-012 systematic) |

---

### Mode 8: `chain-of-verification` (S-011)

**Strategy:** Chain-of-Verification (CoVe) | **Rank:** 9 | **Family:** Structured Decomposition

**Prompt Template:**

```
You are operating in CHAIN-OF-VERIFICATION mode.

Systematically verify every factual claim in the artifact. For each claim:

1. EXTRACT the factual claim (quote it exactly)
2. CLASSIFY the claim type:
   - EMPIRICAL: Can be verified against external evidence
   - LOGICAL: Can be verified by reasoning
   - REFERENCE: Cites a specific source
   - QUANTITATIVE: Makes a numerical claim
3. VERIFY the claim independently (without assuming the artifact is correct)
4. Rate verification status: VERIFIED / PARTIALLY VERIFIED / UNVERIFIED / CONTRADICTED
5. For UNVERIFIED and CONTRADICTED: provide the correct information or
   flag as needing external verification

IMPORTANT: Verify in isolation. Do not let one claim's context influence
verification of another claim. Each claim should be checked independently
to avoid correlated false negatives from shared context.
```

**Evaluation Criteria:**

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Claim Extraction Completeness | 0.30 | Were all factual claims in the artifact identified? |
| Verification Rigor | 0.30 | Was each claim independently verified (not assumed correct)? |
| Classification Accuracy | 0.20 | Are claims correctly classified by type? |
| Correction Quality | 0.20 | For contradicted claims, is the correct information provided? |

**Output Format:**

| Section | Required | Description |
|---------|----------|-------------|
| Claim Inventory | Yes | All extracted claims with classification |
| Verification Results | Yes | Per-claim: status, evidence, confidence |
| Contradicted Claims | Yes | Claims found to be incorrect with corrections |
| Unverified Claims | Yes | Claims that could not be verified (flagged for human review) |
| Verification Summary | Yes | Counts by status category |

**Applicability:**

| Attribute | Value |
|-----------|-------|
| Target Type Affinity (High) | TGT-RES, TGT-REQ |
| Target Type Affinity (Medium) | TGT-DEC, TGT-CODE (docstrings) |
| Target Type Affinity (Low) | TGT-ARCH (fewer factual claims), TGT-PROC |
| Phase (Recommended) | PH-IMPL, PH-VALID, PH-MAINT |
| Criticality | C1: not recommended; C2: not recommended; C3: optional; C4: required |
| Token Budget | ~4,500 |
| Token Tier | Low |
| Pairing (COM) | llm-as-judge (S-011 verifies facts, S-014 scores overall quality) |

---

### Mode 9: `llm-as-judge` (S-014)

**Strategy:** LLM-as-Judge | **Rank:** 1 | **Family:** Iterative Self-Correction

**Prompt Template:**

```
You are operating in LLM-AS-JUDGE mode.

Evaluate the artifact against a structured quality rubric and produce
a numerical quality score. You are the SCORING mechanism for the quality
gate (>= 0.92 per H-13).

Evaluation rubric dimensions (adjust weights by artifact type):

For artifact types with default weights:
| Dimension | Weight | Description |
|-----------|--------|-------------|
| Completeness | 0.20 | Does the artifact address all requirements? |
| Accuracy | 0.20 | Is information correct and internally consistent? |
| Rigor | 0.20 | Is the analysis thorough and well-reasoned? |
| Actionability | 0.15 | Can the artifact be acted upon by downstream consumers? |
| Traceability | 0.15 | Are claims traceable to evidence and source requirements? |
| Clarity | 0.10 | Is the artifact clear, well-structured, and unambiguous? |

CRITICAL: ANTI-LENIENCY CALIBRATION (H-16)
You have a known bias toward leniency (R-014-FN from EN-302 TASK-002).
Actively counteract this:
- A score of 0.92+ means the artifact is genuinely excellent
- A score of 0.80-0.91 means good but with real improvement opportunities
- If you find yourself giving 0.95+ easily, you are likely being lenient
- Reference the rubric descriptors explicitly for each score assignment

Calculate: quality_score = SUM(dimension_score x dimension_weight)

Threshold: >= 0.92 PASS | < 0.92 REVISE
```

**Evaluation Criteria:**

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Scoring Calibration | 0.30 | Are scores well-calibrated against rubric descriptors? |
| Dimension Coverage | 0.25 | Were all rubric dimensions evaluated? |
| Rationale Quality | 0.25 | Is each score justified with specific evidence? |
| Anti-Leniency Compliance | 0.20 | Does scoring demonstrate active leniency bias countermeasure? |

**Output Format:**

| Section | Required | Description |
|---------|----------|-------------|
| Quality Score | Yes | Overall 0.00-1.00 score |
| Dimension Breakdown | Yes | Per-dimension: score, weight, evidence, rationale |
| Pass/Fail Determination | Yes | PASS (>= 0.92) or REVISE (< 0.92) |
| Strengths | Yes | Top 3 strengths with evidence |
| Improvement Areas | Yes | Per-area: gap description, recommendation, expected impact |
| Score Trend | No | If previous iteration scores available, show trend |
| Anti-Leniency Check | Yes | Self-assessment of leniency calibration |

**Applicability:**

| Attribute | Value |
|-----------|-------|
| Target Type Affinity (High) | All target types |
| Phase (Recommended) | PH-DESIGN, PH-IMPL, PH-VALID, PH-MAINT |
| Phase (Cautionary) | PH-EXPLORE (no rubric yet) |
| Criticality | C1: optional; C2: required; C3: required; C4: required |
| Token Budget | ~2,000 |
| Token Tier | Ultra-Low |
| Pairing (SYN) | constitutional (S-007 evaluates, S-014 scores); self-refine (S-010 improves, S-014 measures) |
| Sequencing | Typically LAST in multi-mode pipeline (provides final score) |

---

### Mode 10: `red-team` (S-001)

**Strategy:** Red Team Analysis | **Rank:** 10 | **Family:** Role-Based Adversarialism

**Prompt Template:**

```
You are operating in RED-TEAM mode.

Assume the persona of a skilled adversary attempting to exploit, subvert,
or cause failure in the system described by this artifact. Your objective
is to find vulnerabilities that a motivated attacker could exploit.

Attack vectors to consider:
1. SECURITY: Authentication bypass, privilege escalation, data exposure
2. ARCHITECTURE: Boundary violations, dependency attacks, composition failures
3. GOVERNANCE: Rule circumvention, constraint bypass, policy evasion
4. OPERATIONAL: Denial of service, resource exhaustion, state corruption
5. SOCIAL: Misleading documentation, deceptive naming, unclear interfaces

For each vulnerability found:
- Describe the attack scenario (how an adversary would exploit it)
- Assess exploitability (how easy is it to exploit?)
- Assess impact (what damage could be done?)
- Propose defensive measures

NOTE: This is the highest-intensity adversarial mode. It is appropriate
for C3-C4 criticality only. For C1-C2, use lighter strategies
(self-refine, constitutional, devils-advocate).
```

**Evaluation Criteria:**

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Attack Surface Coverage | 0.30 | Are all relevant attack vectors considered? |
| Vulnerability Realism | 0.25 | Are identified vulnerabilities exploitable in practice? |
| Impact Assessment | 0.25 | Is the damage potential correctly assessed? |
| Defensive Measure Quality | 0.20 | Are proposed defenses concrete and effective? |

**Output Format:**

| Section | Required | Description |
|---------|----------|-------------|
| Attack Surface Analysis | Yes | Enumeration of attack vectors relevant to the artifact |
| Vulnerability Report | Yes | Per-vulnerability: scenario, exploitability, impact, defense |
| Critical Vulnerabilities | Yes | High-exploitability + high-impact findings |
| Defense Recommendations | Yes | Priority-ordered defensive measures |
| Residual Risk Assessment | Yes | What risks remain after recommended defenses |

**Applicability:**

| Attribute | Value |
|-----------|-------|
| Target Type Affinity (High) | TGT-ARCH, TGT-CODE (security-relevant) |
| Target Type Affinity (Medium) | TGT-DEC, TGT-PROC |
| Phase (Recommended) | PH-DESIGN |
| Phase (Cautionary) | PH-EXPLORE (premature adversarial pressure) |
| Criticality | C1: not recommended; C2: not recommended; C3: optional; C4: required |
| Token Budget | ~6,500 |
| Token Tier | Low-Medium |
| Pairing (SYN) | steelman (S-003 first); inversion (S-013 generates attack surface) |
| Sequencing | Execute AFTER steelman and inversion when all are in the pipeline |

---

## Mode Switching Protocol

### Mode Selection Flow

```
1. RECEIVE invocation (from orchestrator)
   |
   +-- Explicit mode specified (--mode)?
   |     YES -> Validate mode name(s) -> Execute mode(s)
   |     NO  -> Continue to automatic selection
   |
   +-- Context vector available?
   |     YES -> Apply auto-escalation rules (AE-001 through AE-006)
   |          -> Traverse decision tree (EN-303 TASK-004)
   |          -> Determine mode set by criticality
   |     NO  -> Use default mode (standard v2.2.0 behavior)
   |
   +-- Execute selected mode(s) -> Return results to orchestrator
```

### Mode Validation Rules

| Rule | Description |
|------|-------------|
| Unknown mode name | Reject with error listing all valid mode names |
| Empty mode list | Fall back to default `standard` mode |
| Contradictory modes | Warn but execute (e.g., `steelman,devils-advocate` is valid and recommended) |
| TEN pair warning | If tension pair detected, emit guidance note but proceed |

---

## Multi-Mode Composition

### Sequencing Rules

Multi-mode pipelines follow these ordering constraints:

| Constraint | Rule | Source |
|-----------|------|--------|
| **SEQ-001** | `steelman` MUST execute before `devils-advocate`, `constitutional`, and `red-team` | EN-303 TASK-003 S-003 SYN pairings |
| **SEQ-002** | `inversion` SHOULD execute before `constitutional`, `fmea`, and `red-team` | EN-303 TASK-003 S-013 SYN pairings |
| **SEQ-003** | `llm-as-judge` SHOULD execute LAST in the pipeline (provides final score) | EN-303 TASK-003 S-014 role as evaluation infrastructure |
| **SEQ-004** | `self-refine` SHOULD execute FIRST (creator self-improvement before critique) | EN-303 TASK-004 Creator-Critic-Revision cycle |
| **SEQ-005** | `chain-of-verification` is order-independent (verifies facts in isolation) | EN-303 TASK-003 S-011 isolation requirement |

### Canonical Pipeline Examples

**C2 Pipeline (Standard Critic):**
```
steelman -> constitutional -> devils-advocate -> llm-as-judge
```

**C3 Pipeline (Deep Review):**
```
steelman -> inversion -> constitutional -> devils-advocate -> pre-mortem -> fmea -> llm-as-judge
```

**C4 Pipeline (Tournament):**
```
self-refine -> steelman -> inversion -> constitutional -> devils-advocate ->
pre-mortem -> fmea -> chain-of-verification -> red-team -> llm-as-judge
```

### Output Chaining

Each mode's output is appended to the pipeline context, making it available to subsequent modes:

- `steelman` output becomes input for `devils-advocate` (challenge the strongest version)
- `inversion` output (anti-pattern checklist) becomes input for `constitutional` (verify against anti-patterns)
- All mode outputs become context for `llm-as-judge` (final comprehensive scoring)

---

## C1-C4 Integration

### Mode Activation Matrix

| Mode | C1 | C2 | C3 | C4 |
|------|----|----|----|----|
| `self-refine` | **Required** | Recommended | Recommended | **Required** |
| `steelman` | Optional | Recommended | **Required** | **Required** |
| `inversion` | -- | Optional | **Required** | **Required** |
| `constitutional` | -- | **Required** | **Required** | **Required** |
| `devils-advocate` | -- | **Required** | **Required** | **Required** |
| `pre-mortem` | -- | -- | **Required** | **Required** |
| `fmea` | -- | -- | **Required** | **Required** |
| `chain-of-verification` | -- | -- | Optional | **Required** |
| `llm-as-judge` | Optional | **Required** | **Required** | **Required** |
| `red-team` | -- | -- | Optional | **Required** |

**Legend:** Required = always included; Recommended = included if budget allows; Optional = user/orchestrator choice; -- = not recommended at this level.

---

## ContentBlock Priority Integration

The adversarial modes align with the L2 PromptReinforcementEngine ContentBlocks from the barrier-2 handoff:

| ContentBlock | Priority | Token | Mode Alignment | Integration |
|-------------|----------|-------|----------------|-------------|
| `quality-gate` | 1 | ~30 | `llm-as-judge` | Reinforces >= 0.92 threshold and S-014 scoring requirement |
| `constitutional-principles` | 2 | ~65 | `constitutional` | Reinforces P-003, P-020, P-022 for S-007 evaluation |
| `self-review` | 3 | ~30 | `self-refine` | Reinforces S-010 self-review before submission |
| `scoring-requirement` | 4 | ~35 | `llm-as-judge` | Reinforces S-014 scoring as mandatory |
| `steelman` | 5 | ~30 | `steelman` | Reinforces S-003 steelman-before-critique protocol |
| `leniency-calibration` | 6 | ~25 | `llm-as-judge` | Reinforces anti-leniency bias for S-014 |
| `deep-review` | 7 | ~40 | Multi-mode pipeline | Triggers full adversarial pipeline at C3+ |

**Key insight:** The ContentBlock system already encodes the most critical adversarial modes as per-prompt reinforcement. The mode architecture leverages this by ensuring that mode behavior matches the reinforced expectations.

---

## Traceability

### Requirements Coverage

| Requirement | Coverage |
|-------------|----------|
| FR-304-001 (10 modes) | All 10 modes defined with complete specifications |
| FR-304-002 (mode components) | Each mode includes all 7 required components |
| FR-304-005 (multi-mode pipeline) | Multi-mode composition section with sequencing rules |
| FR-304-006 (C1-C4 mapping) | C1-C4 Integration section with activation matrix |
| FR-304-008 (quality scoring) | llm-as-judge mode with anti-leniency calibration |
| IR-304-005 (ContentBlock integration) | ContentBlock Priority Integration section |
| BC-304-001 (backward compatibility) | Default `standard` mode preserves v2.2.0 behavior |

---

## References

| # | Citation | Relevance |
|---|----------|-----------|
| 1 | ADR-EPIC002-001 | 10 selected strategies, composite scores, mechanistic families |
| 2 | EN-303 TASK-001 | Context taxonomy, strategy affinity tables, phase-strategy matrix |
| 3 | EN-303 TASK-003 | Per-strategy profiles, token budgets, pairing reference, enforcement mapping |
| 4 | EN-303 TASK-004 | Decision tree, auto-escalation rules, cycle mapping, pipeline examples |
| 5 | Barrier-2 ENF-to-ADV | ContentBlock system, L2-REINJECT tags, HARD rules, defense-in-depth |
| 6 | TASK-001 (this enabler) | Formal requirements (FR-304-xxx, NFR-304-xxx, IR-304-xxx, BC-304-xxx) |
| 7 | ps-critic.md v2.2.0 | Current agent specification (baseline for mode architecture) |

---

*Document ID: FEAT-004:EN-304:TASK-002*
*Agent: ps-architect-304*
*Created: 2026-02-13*
*Status: Draft*
