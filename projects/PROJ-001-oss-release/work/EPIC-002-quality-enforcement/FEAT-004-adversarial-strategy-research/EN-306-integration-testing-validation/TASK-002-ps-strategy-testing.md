# TASK-002: /problem-solving Strategy Testing Specifications

<!--
DOCUMENT-ID: FEAT-004:EN-306:TASK-002
VERSION: 1.0.0
AGENT: ps-validator-306
DATE: 2026-02-13
STATUS: Complete
PARENT: EN-306 (Integration Testing & Validation)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
ACTIVITY: TESTING
-->

> **Version:** 1.0.0
> **Agent:** ps-validator-306
> **Quality Target:** >= 0.92
> **Purpose:** Detailed test specifications for all 10 adversarial strategies in the /problem-solving skill (ps-critic agent v3.0.0)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this test specification covers |
| [Test Design Basis](#test-design-basis) | Source artifacts driving test design |
| [Strategy Test Specifications](#strategy-test-specifications) | Per-strategy test cases (10 strategies) |
| [Pipeline Test Specifications](#pipeline-test-specifications) | Multi-mode pipeline tests (C1-C4) |
| [Invocation Protocol Tests](#invocation-protocol-tests) | Mode selection and validation tests |
| [Quality Score Tracking Tests](#quality-score-tracking-tests) | S-014 scoring and anti-leniency tests |
| [Backward Compatibility Tests](#backward-compatibility-tests) | BC-T-001 through BC-T-007 |
| [Traceability](#traceability) | Mapping to EN-306 AC-2 |
| [References](#references) | Source citations |

---

## Summary

This document provides detailed test specifications for all 10 adversarial strategies as implemented in the /problem-solving skill's ps-critic agent (v3.0.0). For each strategy, the specification defines: test case ID, input conditions, expected output structure, pass criteria, and traceability to the source design (EN-304 TASK-002 mode definitions and EN-304 TASK-003 invocation protocol).

---

## Test Design Basis

| Source | What It Provides | Test Impact |
|--------|-----------------|-------------|
| EN-304 TASK-002 | 10 adversarial mode definitions with prompt templates, evaluation criteria, output formats | Per-mode output validation |
| EN-304 TASK-003 | Invocation protocol, selection algorithm, pipeline model, BC test specs | Invocation and pipeline tests |
| EN-304 TASK-004 | ps-critic v3.0.0 agent spec with mode registry and configuration schema | Configuration validation |
| EN-304 TASK-001 | 50 formal requirements (FR/NFR/IR/BC) | Requirements traceability |

---

## Strategy Test Specifications

### PST-001: Self-Refine (S-010)

| Field | Value |
|-------|-------|
| **Strategy:** | S-010 Self-Refine |
| **Mode Name:** | `self-refine` |
| **Source:** | EN-304 TASK-002, Mode 1 |

**Input:**
- Artifact: Any design document (e.g., `work/EN-304/TASK-002.md`)
- Mode: `--mode self-refine`
- Criticality: C1 (minimum -- self-refine is always available)

**Expected Output Structure:**
- Issue Summary: Count and severity of issues found
- Issue Details: Per-issue location, description, recommendation, expected impact
- Revision Priority: Ordered list of issues to address first
- Self-Assessment Confidence: Confidence level in review completeness

**Pass Criteria:**
- [ ] Output contains all 4 required sections
- [ ] Issues are specific with locations cited
- [ ] Recommendations are concrete and actionable
- [ ] No quality score produced (scoring is llm-as-judge responsibility)
- [ ] Token cost within ~2,000 template budget

**Evaluation Criteria Verification:**
- Issue Identification Completeness (0.30): Issues cover the artifact comprehensively
- Recommendation Specificity (0.30): Each recommendation is actionable
- Logical Coherence (0.20): Identified issues are logically valid
- Improvement Potential (0.20): Implementing recommendations would improve quality

---

### PST-002: Steelman (S-003)

| Field | Value |
|-------|-------|
| **Strategy:** | S-003 Steelman Technique |
| **Mode Name:** | `steelman` |
| **Source:** | EN-304 TASK-002, Mode 2 |

**Input:**
- Artifact: Architecture decision document (TGT-ARCH or TGT-DEC)
- Mode: `--mode steelman`
- Criticality: C2+ (recommended at C2, required at C3+)

**Expected Output Structure:**
- Core Thesis: Central argument in one statement
- Explicit Assumptions: All assumptions (stated and implicit)
- Strongest Reasoning Chain: Argument at maximum strength
- Supporting Evidence: Evidence supporting the argument
- Unstated Supporting Arguments (optional): Additional strengthening arguments

**Pass Criteria:**
- [ ] Core thesis accurately represents the artifact's central argument
- [ ] Implicit assumptions are made explicit (not just stated assumptions repeated)
- [ ] Reasoning chain is genuinely the strongest reconstruction (not a paraphrase)
- [ ] No critique is present (steelman does charitable reconstruction only)
- [ ] Token cost within ~1,600 template budget
- [ ] Sequencing: When in pipeline, executes BEFORE devils-advocate, constitutional, red-team (SEQ-001)

---

### PST-003: Inversion (S-013)

| Field | Value |
|-------|-------|
| **Strategy:** | S-013 Inversion Technique |
| **Mode Name:** | `inversion` |
| **Source:** | EN-304 TASK-002, Mode 3 |

**Input:**
- Artifact: Process definition or requirements document (TGT-PROC, TGT-REQ)
- Mode: `--mode inversion`
- Criticality: C3+ (required at C3+)

**Expected Output Structure:**
- Inverted Success Criteria: Each success criterion as failure condition
- Anti-Pattern Checklist: Per-pattern description, severity, verification method
- Blind Spot Analysis: Failure modes not covered by stated requirements
- Reusable Verification Criteria (optional): Anti-patterns for other modes

**Pass Criteria:**
- [ ] Each stated success criterion has a corresponding failure inversion
- [ ] Anti-patterns are specific enough to serve as verification criteria
- [ ] Blind spot analysis identifies non-obvious failure modes
- [ ] Token cost within ~2,100 template budget
- [ ] Sequencing: Executes before constitutional, fmea, red-team (SEQ-002)

---

### PST-004: Constitutional AI (S-007)

| Field | Value |
|-------|-------|
| **Strategy:** | S-007 Constitutional AI Critique |
| **Mode Name:** | `constitutional` |
| **Source:** | EN-304 TASK-002, Mode 4 |

**Input:**
- Artifact: Code, architecture, or requirements document
- Mode: `--mode constitutional`
- Criticality: C2+ (required at C2+)

**Expected Output Structure:**
- Constitutional Compliance Summary: Overall PASS/PARTIAL/FAIL with counts
- HARD Rule Evaluation: H-01 through H-24 (applicable rules)
- MEDIUM Rule Evaluation: MEDIUM-tier principles
- SOFT Rule Evaluation (optional): Advisory items
- Violation Details: Per-violation principle, location, severity, remediation
- Compliance Score: Percentage of applicable principles in PASS

**Pass Criteria:**
- [ ] All applicable HARD rules (H-01 through H-24) are evaluated
- [ ] Each violation includes specific location in artifact
- [ ] Severity classification follows HARD/MEDIUM/SOFT vocabulary
- [ ] A single HARD FAIL means overall FAIL (documented)
- [ ] Remediation suggestions are implementable
- [ ] Token cost within ~8,000-16,000 budget range

---

### PST-005: Devil's Advocate (S-002)

| Field | Value |
|-------|-------|
| **Strategy:** | S-002 Devil's Advocate |
| **Mode Name:** | `devils-advocate` |
| **Source:** | EN-304 TASK-002, Mode 5 |

**Input:**
- Artifact: Architecture decision or design document (TGT-ARCH, TGT-DEC)
- Mode: `--mode devils-advocate`
- Criticality: C2+ (required at C2+)
- Precondition: Steelman output available (if steelman was in pipeline)

**Expected Output Structure:**
- Challenged Assumptions: Each assumption with counterargument
- Challenged Decisions: Major decisions challenged with alternatives
- Robustness Assessment: Claims that survived challenge
- Critical Vulnerabilities: Most serious weaknesses
- Recommended Actions: Priority-ordered responses

**Pass Criteria:**
- [ ] Challenges are substantive (not stylistic or nitpicking)
- [ ] Each challenged decision has at least one concrete alternative
- [ ] Challenges are falsifiable
- [ ] If steelman preceded, DA challenges the steelmanned version
- [ ] Robust claims are acknowledged (not everything fails challenge)
- [ ] Token cost within ~4,600 template budget
- [ ] TEAM-SINGLE note: When TEAM-SINGLE, replace with self-refine per mode spec

---

### PST-006: Pre-Mortem (S-004)

| Field | Value |
|-------|-------|
| **Strategy:** | S-004 Pre-Mortem Analysis |
| **Mode Name:** | `pre-mortem` |
| **Source:** | EN-304 TASK-002, Mode 6 |

**Input:**
- Artifact: Architecture or process decision (TGT-ARCH, TGT-DEC, TGT-PROC)
- Mode: `--mode pre-mortem`
- Criticality: C3+ (required at C3+)

**Expected Output Structure:**
- Failure Narratives: 3-5 failure scenarios in narrative form
- Root Cause Analysis: Per-scenario artifact element causing failure
- Warning Signs: Signs visible now predicting each failure
- Risk Matrix: Probability x Severity for each scenario
- Preventive Measures: Concrete actions to mitigate

**Pass Criteria:**
- [ ] At least 3 failure scenarios with narrative form
- [ ] Root causes trace to specific elements in the artifact
- [ ] Risk matrix includes both probability and severity ratings
- [ ] Preventive measures are concrete and actionable
- [ ] Covers planning fallacy, optimism bias, and temporal risks
- [ ] Token cost within ~5,600 template budget

---

### PST-007: FMEA (S-012)

| Field | Value |
|-------|-------|
| **Strategy:** | S-012 FMEA |
| **Mode Name:** | `fmea` |
| **Source:** | EN-304 TASK-002, Mode 7 |

**Input:**
- Artifact: System design or process definition (TGT-CODE, TGT-ARCH, TGT-PROC)
- Mode: `--mode fmea`
- Criticality: C3+ (required at C3+)

**Expected Output Structure:**
- Component Decomposition: Artifact components analyzed
- FMEA Table: S/O/D/RPN sorted by RPN descending
- Critical Items (RPN > 200): Immediate attention required
- High-Severity Items (S >= 8): Design review required
- Recommended Actions: Per-item mitigation
- Risk Summary: Aggregate assessment

**Pass Criteria:**
- [ ] Uses 1-10 scale (canonical FMEA scale per EN-304 TASK-002 SSOT)
- [ ] RPN calculated as S x O x D (max 1,000)
- [ ] Items with RPN > 200 flagged as critical
- [ ] Items with S >= 8 flagged regardless of RPN
- [ ] FMEA table sorted by RPN descending
- [ ] Scale consistent with nse-reviewer adversarial-fmea (cross-skill SSOT)
- [ ] Token cost within ~9,000 template budget

---

### PST-008: Chain-of-Verification (S-011)

| Field | Value |
|-------|-------|
| **Strategy:** | S-011 Chain-of-Verification |
| **Mode Name:** | `chain-of-verification` |
| **Source:** | EN-304 TASK-002, Mode 8 |

**Input:**
- Artifact: Research document or requirements with factual claims (TGT-RES, TGT-REQ)
- Mode: `--mode chain-of-verification`
- Criticality: C4 required; C3 optional

**Expected Output Structure:**
- Claim Inventory: All extracted claims with classification
- Verification Results: Per-claim status, evidence, confidence
- Contradicted Claims: Incorrect claims with corrections
- Unverified Claims: Claims requiring human verification
- Verification Summary: Counts by status category

**Pass Criteria:**
- [ ] Claims classified by type: EMPIRICAL, LOGICAL, REFERENCE, QUANTITATIVE
- [ ] Each claim verified independently (isolation requirement)
- [ ] Verification status: VERIFIED / PARTIALLY VERIFIED / UNVERIFIED / CONTRADICTED
- [ ] Contradicted claims include corrections
- [ ] Order-independent in pipeline (SEQ-005)
- [ ] Token cost within ~4,500 template budget

---

### PST-009: LLM-as-Judge (S-014)

| Field | Value |
|-------|-------|
| **Strategy:** | S-014 LLM-as-Judge |
| **Mode Name:** | `llm-as-judge` |
| **Source:** | EN-304 TASK-002, Mode 9 |

**Input:**
- Artifact: Any artifact type (universal applicability)
- Mode: `--mode llm-as-judge`
- Criticality: C2+ (required at C2+); C1 optional
- Anti-leniency calibration: REQUIRED per H-16

**Expected Output Structure:**
- Quality Score: 0.00-1.00 numeric
- Dimension Breakdown: Per-dimension score, weight, evidence, rationale
- Pass/Fail Determination: PASS (>= 0.92) or REVISE (< 0.92)
- Strengths: Top 3 with evidence
- Improvement Areas: Per-area gap, recommendation, expected impact
- Score Trend (optional): If previous scores available
- Anti-Leniency Check: Self-assessment of calibration

**Pass Criteria:**
- [ ] Score uses 6 dimensions: Completeness (0.20), Accuracy (0.20), Rigor (0.20), Actionability (0.15), Traceability (0.15), Clarity (0.10)
- [ ] Anti-leniency calibration text present in scoring prompt
- [ ] Score of 0.92+ requires "genuinely excellent" evidence
- [ ] Anomaly flags: jump > 0.20, consistent > 0.95, improvement without changes
- [ ] Typically LAST in multi-mode pipeline (SEQ-003)
- [ ] Token cost within ~2,000 template budget

---

### PST-010: Red Team (S-001)

| Field | Value |
|-------|-------|
| **Strategy:** | S-001 Red Team Analysis |
| **Mode Name:** | `red-team` |
| **Source:** | EN-304 TASK-002, Mode 10 |

**Input:**
- Artifact: Architecture or security-relevant code (TGT-ARCH, TGT-CODE)
- Mode: `--mode red-team`
- Criticality: C3 optional; C4 required

**Expected Output Structure:**
- Attack Surface Analysis: Relevant attack vectors
- Vulnerability Report: Per-vulnerability scenario, exploitability, impact, defense
- Critical Vulnerabilities: High-exploitability + high-impact
- Defense Recommendations: Priority-ordered
- Residual Risk Assessment: Remaining risks after defenses

**Pass Criteria:**
- [ ] 5 attack vector categories covered: security, architecture, governance, operational, social
- [ ] Vulnerabilities are exploitable in practice (not theoretical)
- [ ] Each vulnerability has a defense recommendation
- [ ] Executes AFTER steelman and inversion when all in pipeline
- [ ] Token cost within ~6,500 template budget

---

## Pipeline Test Specifications

### PLN-001: C1 Pipeline (Routine)

| Field | Value |
|-------|-------|
| Pipeline: | `self-refine` |
| Total tokens: | ~2,000 |
| Threshold: | 0.85 (standard) or 0.92 (if adversarial context present) |

**Pass Criteria:** Only S-010 executes. No scoring unless explicitly requested.

### PLN-002: C2 Pipeline (Standard Critic)

| Field | Value |
|-------|-------|
| Pipeline: | `steelman` -> `constitutional` -> `devils-advocate` -> `llm-as-judge` |
| Total tokens: | ~14,800 |
| Sequencing: | SEQ-001 (steelman before DA), SEQ-003 (judge last) |

**Pass Criteria:** 4 modes execute in correct order. S-014 produces final score. Score against 0.92 threshold.

### PLN-003: C3 Pipeline (Deep Review)

| Field | Value |
|-------|-------|
| Pipeline: | `steelman` -> `inversion` -> `constitutional` -> `devils-advocate` -> `pre-mortem` -> `fmea` -> `llm-as-judge` |
| Total tokens: | ~33,500 |
| Sequencing: | SEQ-001, SEQ-002, SEQ-003 all satisfied |

**Pass Criteria:** 7 modes execute. Inversion output consumed by constitutional. All findings aggregated. Final score from S-014.

### PLN-004: C4 Pipeline (Tournament)

| Field | Value |
|-------|-------|
| Pipeline: | `self-refine` -> `steelman` -> `inversion` -> `constitutional` -> `devils-advocate` -> `pre-mortem` -> `fmea` -> `chain-of-verification` -> `red-team` -> `llm-as-judge` |
| Total tokens: | ~50,300 |
| Sequencing: | All 5 constraints (SEQ-001 through SEQ-005) satisfied |

**Pass Criteria:** All 10 modes execute. Output chaining works. MANDATORY human involvement flagged (P-020).

---

## Invocation Protocol Tests

### INV-001: Explicit Mode -- Valid Mode

- Input: `--mode steelman`
- Expected: Steelman mode executes
- Pass: Mode produces correct output structure

### INV-002: Explicit Mode -- Unknown Mode

- Input: `--mode unknown-mode`
- Expected: REJECT with error listing available modes
- Pass: Error message includes all 10 valid mode names

### INV-003: Explicit Mode -- Multiple Modes

- Input: `--mode steelman,devils-advocate,llm-as-judge`
- Expected: Pipeline executes in specified order with SEQ enforcement
- Pass: Steelman executes before DA; judge executes last

### INV-004: Automatic Mode Selection

- Input: Context vector with criticality=C2, phase=PH-DESIGN, target_type=TGT-ARCH
- Expected: C2 strategy set selected via decision tree
- Pass: constitutional, devils-advocate, llm-as-judge in result set

### INV-005: Empty Mode Parameter

- Input: `--mode ""`
- Expected: Fall back to standard mode (v2.2.0 behavior)
- Pass: Default 5 quality dimensions, threshold 0.85

### INV-006: Tension Pair Warning

- Input: `--mode steelman,self-refine`
- Expected: Warning about tension pair; both execute
- Pass: Warning emitted; execution proceeds

---

## Quality Score Tracking Tests

### QST-001: Score Tracking Across Iterations

- Input: 3 iterations with scores [null, 0.78, 0.93]
- Expected: Improvement delta calculated (+0.15), threshold met at iteration 3
- Pass: `threshold_met: true`, `improvement_delta: +0.15`

### QST-002: Anti-Leniency Flag -- Score Jump

- Input: Score jumps from 0.65 to 0.92 in one iteration
- Expected: Anomaly flag "Unusual improvement"
- Pass: Flag triggers human review recommendation

### QST-003: Anti-Leniency Flag -- Consistent High

- Input: 3 consecutive artifacts scored > 0.95
- Expected: Anomaly flag "Possible ceiling effect"
- Pass: Rubric recalibration recommended

### QST-004: Plateau Detection

- Input: Iterations [0.78, 0.81, 0.83] with delta < 0.05 for iterations 2 and 3
- Expected: Plateau detected
- Pass: ACCEPT_WITH_CAVEATS or ESCALATE triggered

---

## Backward Compatibility Tests

Per EN-304 TASK-003 backward compatibility test specifications:

| Test ID | Scenario | Expected | Requirement |
|---------|----------|----------|-------------|
| BC-T-001 | ps-critic invoked with v2.2.0 PS CONTEXT (no ADVERSARIAL CONTEXT) | Standard mode. Default 5 dimensions. Threshold 0.85. | BC-304-001 |
| BC-T-002 | ps-critic invoked with `--mode standard` | Same as BC-T-001 | BC-304-001 |
| BC-T-003 | Existing orchestration workflow invokes ps-critic without changes | Workflow completes. No errors. | BC-304-002 |
| BC-T-004 | ps-critic invoked with empty `--mode` | Falls back to standard. No error. | BC-304-001 |
| BC-T-005 | ps-critic invoked with ADVERSARIAL CONTEXT present | Threshold 0.92. Adversarial protocol active. | BC-304-003 |
| BC-T-006 | ADVERSARIAL CONTEXT removed after adversarial run | Returns to standard. No residual state. | BC-304-002 |
| BC-T-007 | v2.2.0 caller sends context to v3.0.0 ps-critic | Accepted. Missing adversarial fields default gracefully. | BC-304-001 |

---

## Traceability

| EN-306 AC | Coverage |
|-----------|----------|
| AC-2 | This document -- all 10 adversarial strategies tested in /problem-solving |

| EN-304 Requirement | Test Cases |
|-------------------|------------|
| FR-304-001 (10 modes) | PST-001 through PST-010 |
| FR-304-002 (mode components) | All PST tests verify 7 components |
| FR-304-003 (explicit selection) | INV-001 through INV-006 |
| FR-304-005 (multi-mode pipeline) | PLN-001 through PLN-004 |
| FR-304-008 (quality scoring) | QST-001 through QST-004 |
| BC-304-001 through BC-304-003 | BC-T-001 through BC-T-007 |

---

## References

| # | Citation | Relevance |
|---|----------|-----------|
| 1 | EN-304 TASK-002 | 10 mode definitions with prompt templates and evaluation criteria |
| 2 | EN-304 TASK-003 | Invocation protocol, selection algorithm, BC test specs |
| 3 | EN-304 TASK-004 | ps-critic v3.0.0 spec with mode registry |
| 4 | EN-304 TASK-001 | Formal requirements (FR/NFR/IR/BC) |

---

*Document ID: FEAT-004:EN-306:TASK-002*
*Agent: ps-validator-306*
*Created: 2026-02-13*
*Status: Complete*
