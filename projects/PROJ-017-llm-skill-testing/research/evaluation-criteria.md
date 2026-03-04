---
DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
standards. It is advisory only and does not constitute official NASA guidance.
All SE decisions require human review and professional engineering judgment.
Not for use in mission-critical decisions without SME validation.
---

# Requirements Specification: LLM Skill Testing Framework Evaluation Criteria

> **Project:** PROJ-017
> **Entry:** e-101
> **Date:** 2026-03-03
> **Status:** Draft
> **Agent:** nse-requirements
> **Pipeline Role:** Phase 1D -- feeds Phase 2 (synthesis ranking), Phase 3A (verification scope), Phase 4 (cross-pollination), Phase 5 (trade study), and all ADV gates

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language summary for non-technical readers |
| [L1: Technical Requirements](#l1-technical-requirements) | Formal requirements with verification methods and traceability |
| [L2: Systems Perspective](#l2-systems-perspective) | Allocation, risk implications, and downstream pipeline usage |
| [Traceability Matrix](#traceability-matrix) | Forward trace from stakeholder needs to requirements to ADR-001 options |
| [Requirements Quality Checklist](#requirements-quality-checklist) | Self-assessment against NASA-HDBK-1009A criteria |
| [References](#references) | Source documents and NASA standards |

---

## L0: Executive Summary

PROJ-017 needs a formal set of evaluation criteria to select the right architecture for testing whether Jerry Framework skills (system prompts that guide Claude's behavior) reliably improve output quality. This document defines who will use the testing framework, what they need from it, and the measurable standards that any candidate architecture must meet. These criteria serve as the shared scoring standard for all downstream analysis phases -- they tell the synthesis agent how to rank findings, the verification agent what evidence to check, the trade study agent what dimensions to measure, and the adversarial reviewers what weaknesses to probe.

---

## L1: Technical Requirements

### 1. Stakeholder Needs Analysis (NPR 7123.1D Process 1)

#### 1.1 Stakeholder Identification

| ID | Stakeholder | Role | Decision Informed by Framework | Operational Context |
|----|-------------|------|-------------------------------|---------------------|
| STK-001 | Framework Developer (Jerry Team) | Primary creator and maintainer of Jerry skills and the testing framework itself | "Is this skill worth keeping, retiring, or refining?" and "What regression did this skill change introduce?" | Runs evaluations on demand and in CI/CD during pull requests; uses CLI interface; requires fast smoke results for every commit |
| STK-002 | Skill Author | Author of individual agent definition files (ps-researcher, ps-analyst, etc.) | "Does my new skill actually improve quality compared to no skill?" and "Which of my two skill variants is better?" | Runs evaluation on a specific skill before submitting a PR; needs clear before/after comparison output; not an evaluation expert |
| STK-003 | CI/CD System (GitHub Actions) | Automated evaluation executor | "Did this commit break any governance compliance checks?" | Executes smoke-mode structural checks on every push; requires binary pass/fail output, zero API cost, sub-60-second runtime |
| STK-004 | Quality Reviewer | Human reviewer of Jerry deliverables (adversarial gate operator) | "Is the evaluation result statistically credible?" and "Is the evidence quality sufficient to accept this ADR?" | Reviews evaluation reports as part of adversarial quality gates; requires confidence intervals, p-values, and explicit limitation disclosures |
| STK-005 | Governance Auditor | Oversees Jerry constitutional compliance | "Do skill outputs conform to H-rule structural requirements?" | Reviews audit trails; requires deterministic, reproducible checks with specific rule citations per finding |

#### 1.2 Stakeholder Needs (STK-NNN)

| ID | Stakeholder | Need Statement | Priority | Source |
|----|-------------|---------------|----------|--------|
| STK-001-N1 | Framework Developer | The framework shall enable comparison of skill-active vs. skill-inactive outputs to determine whether a skill improves quality | H | ADR-001 Problem Statement |
| STK-001-N2 | Framework Developer | The framework shall integrate with the existing Jerry CLI (`jerry skill-test`) with no separate toolchain installation for smoke mode | H | ADR-001 Constraint: CLI workflow |
| STK-001-N3 | Framework Developer | The framework shall produce evaluation reports in a persistent, machine-readable format (JSON) | H | ADR-001 Output Format specification |
| STK-001-N4 | Framework Developer | The framework shall display estimated API cost before executing any LLM-dependent evaluation tier | H | ADR-001 PM-001 response (cost transparency) |
| STK-002-N1 | Skill Author | The framework shall produce a clear IMPROVEMENT / REGRESSION / NO_EFFECT verdict for each evaluation dimension | H | ADR-001 Output Format, Statistical Engine |
| STK-002-N2 | Skill Author | The framework shall require no prior knowledge of statistical testing to interpret results | M | ADR-001 Adoption Friction dimension |
| STK-002-N3 | Skill Author | The framework shall execute smoke-mode structural checks in under 60 seconds | H | ADR-001 PM-001: CI/CD readiness |
| STK-003-N1 | CI/CD System | The framework shall produce a binary pass/fail exit code for smoke-mode evaluations | H | ADR-001 Smoke mode design |
| STK-003-N2 | CI/CD System | The framework shall execute smoke-mode checks with zero LLM API calls and zero external cost | H | ADR-001 PM-001 response: Smoke tier $0.00 |
| STK-003-N3 | CI/CD System | The framework shall be installable in a GitHub Actions runner environment in under 5 minutes | M | ADR-001 CI/CD integration Phase 4 |
| STK-004-N1 | Quality Reviewer | The framework shall report 95% confidence intervals alongside every statistical comparison verdict | H | ADR-001 Statistical Engine: BCa intervals |
| STK-004-N2 | Quality Reviewer | The framework shall explicitly state the number of evaluation runs (N) and classify confidence as LOW / MEDIUM / HIGH accordingly | H | ADR-001 Statistical Engine RT-003 response |
| STK-004-N3 | Quality Reviewer | The framework shall flag SINGLE-SOURCE findings and provisional results with explicit disclosures | M | ADR-001 Compliance: P-022, P-001 |
| STK-005-N1 | Governance Auditor | The framework shall map every failing structural check to the specific Jerry H-rule it violates | H | ADR-001 Governance Compliance Validator |
| STK-005-N2 | Governance Auditor | The framework shall produce identical pass/fail verdicts for identical inputs across evaluation runs (deterministic structural checks) | H | ADR-001 T1 tier definition |
| STK-005-N3 | Governance Auditor | The framework shall include a machine-readable audit trail (JSON) linking each assertion to the governance rule it enforces | M | ADR-001 Governance validator output |

---

### 2. Quality Attributes (Non-Functional Requirements)

The following quality attributes define the measurable performance envelope of the framework. These are distinct from functional evaluation dimensions (Section 3) -- they describe the framework's own operational characteristics.

**QA attribute derivation:** These attributes are selected from ISO/IEC 25010:2023 (Systems and software quality models) product quality characteristics, filtered to the subset relevant to a CLI-based evaluation framework. Determinism and Reproducibility map to ISO 25010 *Reliability > Maturity*; Latency and Cost map to *Performance Efficiency > Time Behaviour* and *Resource Utilization*; False Positive/Negative Rates map to *Functional Correctness*; Extensibility maps to *Maintainability > Modifiability*; Adoption Friction and Adoption Slope map to *Usability > Learnability*. Attributes not selected from ISO 25010 (e.g., Security, Portability, Compatibility) are excluded because the framework operates in a trusted CI/CD environment with no user-facing data exposure and targets a single platform (GitHub Actions on Ubuntu).

| ID | Attribute | Definition | Measurement | Acceptable Range | Priority | V-Method | Threshold Justification |
|----|-----------|-----------|-------------|-----------------|----------|----------|------------------------|
| QA-001 | **Determinism** | Smoke-mode (T1 structural) checks produce identical pass/fail results for identical inputs on repeated executions | Percentage of re-runs with identical verdict | 100% (binary: deterministic or not) | Must | Test | Governance checks must be deterministic by definition (REQ-011); any non-determinism undermines audit integrity. Binary threshold: either deterministic or not. |
| QA-002 | **Reproducibility** | Statistical evaluation results (T2) are statistically reproducible across environments with matched N | 95% CI overlap rate when same test is run in two environments | >= 95% CI overlap | Must | Test | 95% CI overlap is the standard statistical reproducibility criterion; a replication study producing non-overlapping CIs at the 95% level indicates a systematic difference rather than sampling variation. |
| QA-003 | **Smoke-mode Latency** | Time from CLI invocation to first result output for smoke mode | Wall-clock seconds on standard CI runner | <= 60 seconds | Must | Test | Engineering estimate based on GitHub Actions runner performance: structural checks on a typical agent definition (~5KB YAML + ~20KB markdown) should complete in <10 seconds; 60 seconds provides a 6x safety margin for larger files, slower runners, and framework initialization overhead. ADR-001 PM-001 identifies CI/CD readiness as a blocking concern. |
| QA-004 | **Zero-cost CI/CD** | Smoke mode must incur zero LLM API cost | $ per smoke evaluation run | $0.00 exactly | Must | Inspection | Binary threshold: any API cost in smoke mode defeats the purpose of zero-cost CI/CD gating (ADR-001 PM-001). |
| QA-005 | **Statistical Cost Ceiling** | Full-mode evaluation (N=30, 10 test cases) must not exceed the cost ceiling | $ per full-mode evaluation suite | <= $10.00 per 10-test-case full suite | Should | Analysis | ADR-001 revised cost calculation: N=30 x 2 conditions x 10 test cases = 600 executions. At Haiku judge pricing (~$0.005/call), judge cost is ~$3.00. Execution cost depends on model; at Haiku execution (~$0.005/call), total ~$6.00. $10.00 ceiling provides ~40% headroom for Sonnet judge or larger prompts. |
| QA-006 | **CI/CD Adoption Friction** | Time required to install and configure the framework in a fresh GitHub Actions environment | Minutes from zero to first passing smoke run | <= 30 minutes | Should | Demonstration | Analogous system comparison: promptfoo installation in GH Actions takes ~5 minutes (npm install); Jerry framework adds UV sync (~3 minutes) plus configuration (~10 minutes). 30 minutes provides 50% headroom for troubleshooting. |
| QA-007 | **Extensibility** | Adding a new skill-specific evaluation dimension requires minimal code | Lines of code required to add one new evaluation dimension | <= 50 lines of Python or YAML | Should | Inspection | Engineering estimate based on assertion provider pattern: a minimal Python assertion class requires ~20 lines (class + validate method + assertion message); YAML test case definition adds ~10 lines. 50-line ceiling accommodates moderately complex assertions with helper logic. |
| QA-008 | **False Positive Rate** | Smoke-mode structural checks should not flag correct outputs as failures | Rate of false positives on known-valid skill outputs | <= 2% false positive rate | Must | Test | Engineering estimate: 2% false positive rate means ~1 in 50 valid outputs is incorrectly flagged. At expected CI/CD volume (~10-20 smoke runs/day), this produces < 1 false alarm per day -- acceptable adoption friction. Higher rates (e.g., 5%) would produce 1+ daily false alarms, eroding trust in the framework. |
| QA-009 | **False Negative Rate** | Smoke-mode checks should not pass outputs that violate governance rules | Rate of false negatives on known-invalid outputs | <= 5% false negative rate | Must | Test | Engineering estimate: 5% false negative rate means ~1 in 20 violations escapes T1 detection. T1 is a structural pre-screen, not the only quality gate; T2/T4 tiers and manual review provide defense-in-depth. A stricter rate (e.g., 1%) would require expensive heuristics that risk increasing false positives beyond QA-008's 2% ceiling. |
| QA-010 | **Adoption Slope** | A skill author with no prior evaluation framework experience can produce a first evaluation result | Time to first successful evaluation from cold start | <= 2 hours from zero | Should | Demonstration | Engineering estimate based on analogous tool onboarding: promptfoo's getting-started tutorial takes ~30 minutes; Jerry's wrapper adds configuration complexity (~30 minutes). 2-hour ceiling provides 2x headroom for troubleshooting, reading documentation, and understanding output format. |

---

### 3. Technical Requirements (Formal SHALL Statements)

#### 3.1 Evaluation Architecture Requirements

| ID | Requirement | Rationale | Parent | V-Method | Priority | Status |
|----|-------------|-----------|--------|----------|----------|--------|
| REQ-001 | The framework shall implement a three-tier evaluation pipeline for MVP: T1 (structural/deterministic), T2 (statistical/comparative), and T4 (LLM-as-judge). The framework architecture shall reserve the T3 (hybrid-proxy) tier position in the pipeline design, but T3 implementation is deferred until concrete acceptance criteria are defined (see Section 5.4 Lifecycle Considerations for activation condition). | Hybrid evaluation is market consensus per ADR-001 Phase 1A; no single modality is sufficient. Tiered architecture ensures zero-cost CI runs at T1 and statistical rigor at T2+ on demand. T3 is architecturally reserved but not implementable without concrete "quasi-deterministic" criteria (ADR-001 PM-008); deferral avoids specifying unverifiable requirements while preserving the design slot. | STK-001-N1, STK-003-N2 | Inspection | Must | Draft |
| REQ-002 | The framework shall model skill evaluation as a paired treatment variable comparison: with-skill condition vs. without-skill condition on matched input corpora. | The skill-evaluation gap (ADR-001 CONVERGENCE-1) is precisely the absence of this modeling from existing tools. This is the primary differentiating capability. | STK-001-N1, STK-002-N1 | Test | Must | Draft |
| REQ-003 | The framework shall provide a smoke mode (T1 only) that executes with zero LLM API calls. | CI/CD cost is a blocking concern (ADR-001 PM-001); the zero-cost default ensures every commit receives structural verification without budget impact. | STK-003-N1, STK-003-N2 | Demonstration | Must | Draft |
| REQ-004 | The framework shall support configurable N (number of runs per evaluation condition) with a minimum value of 10 and a default value of 30. | N=30 is the current SINGLE-SOURCE recommendation (ADR-001 RT-003); the configurable minimum of 10 permits cost-constrained environments to use partial statistical rigor while a calibration study runs. | STK-004-N2 | Test | Must | Draft |
| REQ-005 | The framework shall compute paired bootstrap confidence intervals (BCa method) and permutation test p-values for all statistical comparisons. | No existing evaluation tool provides paired statistical testing for LLM evaluation (ADR-001 CONVERGENCE-3); this is a defensible differentiator. BCa intervals are superior to standard bootstrap for small-N and skewed distributions (Efron & Tibshirani, *An Introduction to the Bootstrap*, 1993, Ch. 14: BCa corrects for bias and skewness in the bootstrap distribution, producing more accurate coverage than percentile intervals at small sample sizes). Permutation tests are distribution-free and provide exact p-values under the null hypothesis of exchangeability (Good, *Permutation, Parametric, and Bootstrap Tests of Hypotheses*, 3rd ed., 2005). | STK-004-N1 | Test | Must | Draft |
| REQ-006 | The framework shall apply Benjamini-Hochberg FDR correction when evaluating multiple dimensions simultaneously. | Multiple comparisons inflate Type I error rate; FDR correction maintains false discovery rate at acceptable levels without the excessive conservatism of Bonferroni correction (Benjamini & Hochberg, "Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing," *Journal of the Royal Statistical Society Series B*, 57(1):289-300, 1995). FDR is preferred over FWER control (Bonferroni) when the number of simultaneous comparisons is moderate (5-10 evaluation dimensions) and individual false discoveries are recoverable rather than catastrophic. | STK-004-N1 | Analysis | Should | Draft |
| REQ-007 | The framework shall display an estimated API cost to the user before executing any tier that incurs LLM API charges, and shall require no implicit acknowledgment to proceed. | Cost transparency (ADR-001 PM-001 response) prevents unexpected billing. Users must see cost before commit. | STK-001-N4 | Demonstration | Must | Draft |
| REQ-008 | The framework shall produce evaluation output in a JSON format containing: skill name, test corpus identifier, evaluation mode, N runs, cost in USD, tier-level results, and overall verdict. | Machine-readable output enables downstream tooling integration (ADR-001 Output Format; Braintrust/LangSmith compatibility PM-005). | STK-001-N3 | Inspection | Must | Draft |

#### 3.2 Governance Compliance Requirements

| ID | Requirement | Rationale | Parent | V-Method | Priority | Status |
|----|-------------|-----------|--------|----------|----------|--------|
| REQ-009 | The framework shall implement Jerry H-rule structural checks as T1 deterministic assertions, including at minimum: H-23 navigation table presence, L0/L1/L2 section structure, citation format compliance, and heading hierarchy. | Governance validation is a Jerry-specific differentiator (ADR-001 Component 3) that no general-purpose evaluation tool provides. | STK-005-N1, STK-005-N2 | Inspection | Must | Draft |
| REQ-010 | The framework shall map each failing assertion to the specific H-rule identifier that it enforces (e.g., "H-23 VIOLATION: navigation table absent"). | Auditors need rule-specific citations, not generic failure messages, to assess compliance status (STK-005-N1). | STK-005-N1, STK-005-N3 | Inspection | Must | Draft |
| REQ-011 | The framework shall produce identical pass/fail verdicts for identical input strings on governance assertions across execution environments, language runtimes, and operating systems. | Non-deterministic governance checks would undermine audit integrity. The Jerry enforcement architecture (quality-enforcement.md L3 layer: "Deterministic gating -- Immune to context rot") requires deterministic pre-tool checks; governance validators must satisfy this same determinism property. P-022 (no deception) is also implicated: non-deterministic governance results could mislead auditors about compliance status. | STK-005-N2, QA-001 | Test | Must | Draft |

#### 3.3 Statistical Rigor Requirements

| ID | Requirement | Rationale | Parent | V-Method | Priority | Status |
|----|-------------|-----------|--------|----------|----------|--------|
| REQ-012 | The framework shall classify evaluation result confidence as LOW (N < 10), MEDIUM (10 <= N < 30), or HIGH (N >= 30) and include this classification in all evaluation reports. | ADR-001 RT-003 identifies N>=30 as a SINGLE-SOURCE finding; confidence classification makes this uncertainty explicit without blocking lower-N usage. | STK-004-N2 | Inspection | Must | Draft |
| REQ-013 | The framework shall produce a verdict of IMPROVEMENT, REGRESSION, or NO_EFFECT for each evaluation dimension, defined as: IMPROVEMENT when p < alpha AND CI entirely positive; REGRESSION when p < alpha AND CI entirely negative; NO_EFFECT otherwise. | Unambiguous verdicts at the dimension level enable non-expert skill authors to act on results without interpreting raw p-values or confidence intervals. | STK-002-N1 | Test | Must | Draft |
| REQ-014 | The framework shall use Cohen's d as the effect size measure and report it alongside the CI and p-value for each dimension. | Effect size contextualized alongside significance prevents the common error of acting on statistically significant but practically negligible improvements. | STK-004-N1 | Inspection | Should | Draft |
| REQ-015 | The framework shall accept a configurable significance level (alpha) with a default of 0.05. | Different evaluation contexts (release gating vs. experimental research) require different Type I error tolerances. | STK-004-N1 | Test | Should | Draft |

#### 3.4 Integration Requirements

| ID | Requirement | Rationale | Parent | V-Method | Priority | Status |
|----|-------------|-----------|--------|----------|----------|--------|
| REQ-016 | The framework shall provide a CLI interface compatible with the Jerry CLI pattern (`jerry skill-test <mode> <skill-file-path>`). | Integration with Jerry's existing CLI workflow (STK-001-N2) reduces adoption friction for the primary user group. | STK-001-N2, STK-002-N3 | Demonstration | Must | Draft |
| REQ-017 | The framework shall produce a binary exit code: 0 for all T1 assertions passing, 1 for any T1 assertion failing, to enable CI/CD pipeline gating. | GitHub Actions and other CI systems use exit codes as pass/fail signals. Binary output is mandatory for automated pipeline integration (STK-003-N1). | STK-003-N1 | Test | Must | Draft |
| REQ-018 | The framework shall be installable in a GitHub Actions Ubuntu runner using no more than two setup steps (e.g., `npm install promptfoo` + `uv sync`). | Installation friction directly impacts adoption (ADR-001 Adoption Friction dimension); two-step setup is a practical upper bound for CI/CD runner configuration. | STK-003-N3, QA-006 | Demonstration | Should | Draft |
| REQ-019 | The framework shall be usable with any Anthropic Claude model accessible via the Claude API, specified as a configurable parameter rather than a hardcoded model version. | Model version pinning creates maintenance debt; API pricing changes and model deprecations should not require framework code changes. | STK-001-N2 | Inspection | Should | Draft |

#### 3.5 Extensibility Requirements

| ID | Requirement | Rationale | Parent | V-Method | Priority | Status |
|----|-------------|-----------|--------|----------|----------|--------|
| REQ-020 | The framework shall support skill-specific dimension maps that define which T1 assertions are applicable to each skill type (ps-researcher, ps-analyst, ps-validator, ps-architect, ps-critic). | Different skill types produce structurally different outputs; a uniform assertion set would produce excessive false positives (QA-008) for some skill types. | STK-001-N1, QA-007 | Inspection | Must | Draft |
| REQ-021 | The framework shall define an extension interface (custom assertion provider API) that allows adding new evaluation dimensions without modifying the framework core. | Future skill types and governance rules will require new assertion types; a stable extension interface ensures the framework does not become a bottleneck. | STK-001-N2, QA-007 | Inspection | Should | Draft |

---

### 4. Acceptance Criteria for Framework Architecture Selection

These criteria define the pass/fail and scoring thresholds used in Phase 5 (Trade Study) to rank candidate architectures (ADR-001 Option A: Standalone, Option B: promptfoo Extension, Option C: Hybrid Composable).

#### 4.1 MUST-HAVE Criteria (Binary Pass/Fail)

A framework architecture that fails any MUST-HAVE criterion is eliminated from consideration.

| AC-ID | Criterion | Pass Condition | Fail Condition | Source |
|-------|-----------|---------------|----------------|--------|
| AC-M01 | Skill-as-treatment-variable modeling | Architecture can model with-skill vs. without-skill as paired evaluation conditions on matched input | Architecture requires custom pre/post processing to create paired conditions; skill and no-skill cannot be expressed as two configurations | REQ-002 |
| AC-M02 | T1 zero-cost execution | Architecture provides at least one deterministic evaluation tier that executes with zero LLM API calls | All evaluation tiers require LLM API calls | REQ-003, STK-003-N2 |
| AC-M03 | Binary CI/CD exit code | Architecture produces exit code 0 (pass) or 1 (fail) for CI/CD pipeline integration | Architecture exits with non-binary status or requires post-processing to produce a pass/fail signal | REQ-017 |
| AC-M04 | Paired statistical comparison | Architecture can compute paired comparisons (not independent samples) between with-skill and without-skill score arrays | Architecture only supports independent sample comparison or point-estimate comparison without paired structure | REQ-002, REQ-005 |
| AC-M05 | Confidence interval reporting | Architecture can produce and surface 95% confidence intervals on comparison verdicts | Architecture produces only point estimates (means, medians) without confidence bounds | REQ-005 |
| AC-M06 | Jerry governance integration | Architecture provides an extension mechanism for implementing custom H-rule assertions | Architecture has no extension mechanism; governance checks require forking or modifying core | REQ-009, REQ-021 |
| AC-M07 | Cost transparency | Architecture surfaces estimated API cost before execution of LLM-dependent tiers | Architecture executes LLM calls without pre-execution cost estimation | REQ-007 |
| AC-M08 | Determinism | T1 (structural) assertions produce identical verdicts on identical inputs across environments | T1 assertions produce different verdicts on identical inputs across OS, runtime version, or locale differences | REQ-011, QA-001 |

#### 4.2 SHOULD-HAVE Criteria (Weighted Scoring, 1-10 per dimension)

Architectures that pass all MUST-HAVEs are scored on these dimensions using the ADR-001 weighted composite formula.

| AC-ID | Criterion | Dimension | Weight | Score 10 | Score 1 | Measurement Method |
|-------|-----------|-----------|--------|----------|---------|-------------------|
| AC-S01 | Time to first value | How quickly can a skill author run the first evaluation? | 0.25 | First evaluation result in <= 1 week from zero; validation trial in <= 4 hours | First evaluation result requires >= 3 months of engineering build time | Estimate engineering days to first working smoke-mode result |
| AC-S02 | Determinism coverage | What percentage of evaluation dimensions can be made deterministic? | 0.15 | >= 90% of evaluation dimensions implemented as T1 deterministic checks; T1 assertion library extensible | < 40% of evaluation dimensions achievable deterministically; extension requires core modifications | Count of T1-implementable dimensions / total dimensions |
| AC-S03 | Statistical rigor | How completely does the architecture support paired statistical testing? | 0.15 | Native paired bootstrap (BCa) + permutation testing + FDR correction + configurable N + effect sizes, all without custom code | No statistical comparison capability; requires complete custom build of statistical engine | Count of required statistical features natively supported |
| AC-S04 | Cost per evaluation suite | What is the estimated total cost for 10 test cases at N=30 (full mode)? | 0.15 | <= $5 total for 10 test cases at N=30 using Haiku for judging | >= $50 total; cost ceiling exceeded | Calculate: (N * conditions * execution_cost) + (N * judge_calls * judge_cost) |
| AC-S05 | Extensibility | How easy is it to add new evaluation dimensions? | 0.10 | New dimension requires <= 20 lines of Python or YAML; no core modification required | New dimension requires > 200 lines, core modification, or external build step | Count lines of code to add one new assertion type |
| AC-S06 | Adoption friction | How easy is it for a new user to go from zero to first result? | 0.10 | One-command install; declarative configuration; no framework-specific DSL to learn; < 30 min to first result | Multi-tool install; custom code required before first evaluation; > 4 hours to first result | Time from zero to first passing smoke evaluation (skill author persona) |
| AC-S07 | Competitive defensibility | How resilient is the architecture's value if promptfoo adds native skill comparison? | 0.10 | Primary differentiators (statistical engine, governance validator) are independent of evaluation engine; can decouple from promptfoo without rewrite | Core value proposition is evaluation engine feature parity with promptfoo; no independent differentiator | Identify which components remain valuable if promptfoo adds native skill comparison |

#### 4.3 NICE-TO-HAVE Criteria (Bonus Points, unweighted)

These criteria represent value beyond the core selection decision. They do not affect elimination (MUST-HAVE) or primary scoring (SHOULD-HAVE) but should be noted in Phase 5 trade study findings.

| AC-ID | Criterion | Description |
|-------|-----------|-------------|
| AC-N01 | Multi-skill interaction testing | Framework can evaluate interactions between two skills active simultaneously vs. single-skill vs. no-skill conditions |
| AC-N02 | Composability with external tools | Framework output (JSON) is directly ingestible by Braintrust, LangSmith, or other observability platforms without post-processing |
| AC-N03 | Backend swappability | Architecture can swap the underlying evaluation execution engine without rewriting skill orchestration logic |
| AC-N04 | Community ecosystem | Architecture builds on a tool with an existing developer community (>5k GitHub stars, active issue tracker) |
| AC-N05 | Calibration study support | Architecture supports the N-calibration study (bootstrap interval stability at N=10, 20, 30, 50) without custom scripting |
| AC-N06 | Skill regression suite | Framework can maintain a versioned test corpus and detect regressions when a skill is updated |

---

## L2: Systems Perspective

### 5.1 Allocation to System Elements

The requirements defined in Section 3 map to three primary system elements identified in ADR-001:

| Requirement IDs | Allocated To | ADR-001 Component | Notes |
|-----------------|--------------|-------------------|-------|
| REQ-001, REQ-002, REQ-016, REQ-017, REQ-018, REQ-019, REQ-020 | Skill Comparison Orchestrator | Component 1 (YAML templates + CLI wrapper) | The orchestrator is the integration surface; adoption friction lives here |
| REQ-004, REQ-005, REQ-006, REQ-012, REQ-013, REQ-014, REQ-015 | Statistical Significance Engine | Component 2 (Python module) | This component is the primary defensible differentiator; allocate disproportionate verification effort |
| REQ-009, REQ-010, REQ-011, REQ-021 | Governance Compliance Validator | Component 3 (custom assertions) | This component is Jerry-specific; it does not need to be general-purpose at launch |
| REQ-003, REQ-007, REQ-008 | All three components | Cross-cutting | Smoke mode + cost transparency + JSON output span all components |

### 5.2 Interface Implications

| Interface | Between | Data Contract | Criticality | Realized By |
|-----------|---------|---------------|-------------|-------------|
| IF-001 | Skill Orchestrator <-> Evaluation Engine | promptfoo YAML configuration schema; with-skill/without-skill provider configs | High: format must be stable across promptfoo versions | REQ-001, REQ-002, REQ-016, REQ-020 |
| IF-002 | Evaluation Engine <-> Statistical Engine | promptfoo JSON output format; score arrays per provider per test case | High: statistical engine depends on this schema; changes require coordinated updates | REQ-004, REQ-005, REQ-006, REQ-012, REQ-013, REQ-014, REQ-015 |
| IF-003 | Statistical Engine <-> CLI Output | Python dataclass SkillComparisonResult; JSON serialization | Medium: internal interface; changes are contained within the framework | REQ-008, QA-003 |
| IF-004 | Governance Validator <-> CI/CD | Exit code 0/1; JSON report path as environment variable | High: CI/CD systems cannot adapt to API changes; this interface must be versioned and stable | REQ-009, REQ-010, REQ-011, REQ-017, QA-001 |
| IF-005 | Framework <-> Jerry Quality Gate | Evaluation report JSON mapped to 6-dimension composite (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability) | Medium: mapping is interpretive; requires documentation but not automated schema validation | REQ-008, REQ-021 |

### 5.3 Risk Implications

| Requirement | Primary Risk | Likelihood x Impact | Mitigation |
|-------------|-------------|---------------------|------------|
| REQ-002 (skill-as-treatment-variable) | promptfoo cannot express this modeling natively -- capability gap vs. configuration gap (ADR-001 RT-001, PM-002) | Medium x High | Phase 0 validation trial (4 hours) resolves this before any custom engineering; all three gap outcomes produce viable products |
| REQ-004 (configurable N, min 10) | N=30 recommendation is SINGLE-SOURCE (ADR-001 RT-003); actual required N may be higher | Low x Medium | N is configurable; Phase 3 calibration study (bootstrap stability at N=10..50) provides empirical data |
| REQ-005 (BCa bootstrap + permutation) | Statistical cost at N=30 per condition may block CI/CD adoption (ADR-001 PM-001) | Medium x High | Tiered modes (Smoke $0 / Standard $5-7 / Full $6-10 per ADR-001 revised cost calculation); statistical tier is opt-in |
| REQ-009 (H-rule assertions) | H-rule definitions may change over time; hard-coded assertion logic becomes governance debt | Low x Medium | Assertion logic maps to H-rule IDs, not literal text; updates to rules are localized to assertion implementation |
| REQ-011 (determinism across environments) | String-based structural checks may be locale-sensitive or runtime-sensitive | Low x High | Use pure byte-level string comparisons and regex; avoid locale-sensitive operations |
| QA-008 / QA-009 (false positive / negative rates) | Overly strict assertions produce adoption-blocking false positives; too lenient assertions miss real violations | Medium x Medium | Calibrate thresholds against known-valid and known-invalid skill output corpus before GA release |

### 5.4 Lifecycle Considerations

These requirements are defined for the MVP scope (Phases 0-3 per ADR-001). The following requirements are explicitly deferred to post-MVP phases:

| Deferred Item | Rationale | When to Re-visit |
|---------------|-----------|-----------------|
| T3 hybrid-proxy tier | Under-specified; "quasi-deterministic" is not implementable without concrete criteria (ADR-001 PM-008). T3 must produce identical pass/fail on > 95% reruns with identical input before implementation. REQ-001 reserves the T3 architectural slot but defers implementation to post-MVP. | When Phase 0 gap classification reveals a category of checks that are too expensive for T4 but not fully deterministic at T1, AND concrete acceptance criteria for T3 behavior are defined |
| Multi-skill interaction testing (AC-N01) | Adds combinatorial complexity; unvalidated demand (ADR-001 GAP-4) | After core skill comparison is validated against at least 3 skill types |
| Community/general-purpose release | Jerry-first scope; community size is unknown (ADR-001 RG-5: 13 stars on closest comparable tool) | After internal validation confirms skill evaluation improves Jerry quality gate scores |

### 5.5 Traceability Strategy

Phase 1D criteria must remain accessible to downstream phases. The canonical path for this artifact is:

```
projects/PROJ-017-llm-skill-testing/research/evaluation-criteria.md
```

Downstream agents MUST load this artifact and reference requirement IDs (REQ-NNN), acceptance criterion IDs (AC-M/S/N-NN), and stakeholder need IDs (STK-NNN) in their outputs. This enables Phase 4 cross-pollination to assess requirements compliance explicitly.

---

## Traceability Matrix

### Forward Trace: Stakeholder Needs to Requirements to ADR-001 Options

| STK Need | Requirement IDs | AC Criteria | Option A Score Impact | Option B Score Impact | Option C Score Impact |
|----------|----------------|-------------|----------------------|-----------------------|-----------------------|
| STK-001-N1 (skill comparison) | REQ-002 | AC-M01, AC-M04 | Positive: full design control for paired comparison | Positive: promptfoo two-provider config enables paired comparison | Neutral: depends on backend selection |
| STK-001-N2 (CLI integration) | REQ-016, REQ-019 | AC-S06 | Negative: new CLI from scratch increases adoption friction | Positive: inherits promptfoo CLI ecosystem; jerry wrapper thin | Negative: multi-tool setup increases complexity |
| STK-001-N3 (JSON output) | REQ-008 | AC-N02 | Neutral: custom JSON schema must be designed and documented | Positive: promptfoo JSON output is standard; statistical engine extends it | Neutral: abstraction layer may normalize divergent schemas |
| STK-001-N4 (cost transparency) | REQ-007 | AC-M07 | Neutral: must be custom-built | Positive: promptfoo has built-in cost tracking; display layer is thin | Neutral: depends on backend cost model normalization |
| STK-002-N1 (clear verdicts) | REQ-013 | AC-S01 | Neutral: must design verdict format | Positive: statistical engine verdict layer is independent; builds on promptfoo output | Neutral: verdict layer is independent of backend |
| STK-002-N3 (60-second smoke) | REQ-016, QA-003 | AC-M02 | Positive: no engine overhead; fully controlled | Positive: promptfoo T1 checks execute in milliseconds; native CLI integration | Negative: abstraction layer overhead may add latency |
| STK-003-N1 (binary exit code) | REQ-017 | AC-M03 | Positive: full control | Positive: promptfoo has native exit code support | Positive: exit code is at abstraction layer |
| STK-003-N2 (zero API cost smoke) | REQ-003, QA-004 | AC-M02 | Positive: full control | Positive: T1 uses promptfoo assertions; zero API cost | Positive: T1 backend can be free regardless of choice |
| STK-004-N1 (95% CI) | REQ-005, REQ-014 | AC-M05, AC-S03 | Positive: full statistical design | Positive: statistical engine is independent Python module; same capability | Positive: statistical engine is independent of backend |
| STK-004-N2 (N classification) | REQ-012 | AC-S03 | Positive: full control | Positive: N is a parameter to statistical engine; classification added in report | Positive: same as Option B |
| STK-005-N1 (H-rule mapping) | REQ-009, REQ-010 | AC-M06 | Positive: full assertion design | Positive: custom assertion provider API in promptfoo; H-rules as Python assertions | Negative: H-rule assertions must work across multiple backend extension APIs |
| STK-005-N2 (determinism) | REQ-011, QA-001 | AC-M08 | Positive: controlled | Positive: promptfoo assertion execution is deterministic for structural checks | Positive: T1 determinism does not depend on backend |

### Backward Trace: Requirements to Stakeholder Needs

| Requirement ID | Traced to STK Need(s) | Orphan? |
|----------------|----------------------|---------|
| REQ-001 | STK-001-N1, STK-003-N2 | No |
| REQ-002 | STK-001-N1, STK-002-N1 | No |
| REQ-003 | STK-003-N1, STK-003-N2 | No |
| REQ-004 | STK-004-N2 | No |
| REQ-005 | STK-004-N1 | No |
| REQ-006 | STK-004-N1 | No |
| REQ-007 | STK-001-N4 | No |
| REQ-008 | STK-001-N3 | No |
| REQ-009 | STK-005-N1, STK-005-N2 | No |
| REQ-010 | STK-005-N1 | No |
| REQ-011 | STK-005-N2 | No |
| REQ-012 | STK-004-N2 | No |
| REQ-013 | STK-002-N1 | No |
| REQ-014 | STK-004-N1 | No |
| REQ-015 | STK-004-N1 | No |
| REQ-016 | STK-001-N2, STK-002-N3 | No |
| REQ-017 | STK-003-N1 | No |
| REQ-018 | STK-003-N3 | No |
| REQ-019 | STK-001-N2 | No |
| REQ-020 | STK-001-N1 | No |
| REQ-021 | STK-001-N2 | No |

**Orphan analysis:** No orphan requirements detected. All 21 requirements trace to at least one stakeholder need.

### Stakeholder Need Coverage Analysis

| STK Need | Covered by Requirements? | Gap? |
|----------|------------------------|------|
| STK-001-N1 | REQ-001, REQ-002, REQ-020 | None |
| STK-001-N2 | REQ-016, REQ-018, REQ-019, REQ-021 | None |
| STK-001-N3 | REQ-008 | None |
| STK-001-N4 | REQ-007 | None |
| STK-002-N1 | REQ-013 | None |
| STK-002-N2 | REQ-013 (clear verdicts address this) | Partial: "no prior knowledge" is a usability constraint not fully verifiable by test; addressed by verdict format in REQ-013 |
| STK-002-N3 | REQ-016, QA-003 | None |
| STK-003-N1 | REQ-003, REQ-017 | None |
| STK-003-N2 | REQ-003, QA-004 | None |
| STK-003-N3 | REQ-018 | None |
| STK-004-N1 | REQ-005, REQ-014 | None |
| STK-004-N2 | REQ-004, REQ-012 | None |
| STK-004-N3 | REQ-012 (confidence classification addresses SINGLE-SOURCE flagging) | Partial: SINGLE-SOURCE disclosure is in REQ-012 implicitly; explicit flagging mechanism not separately required. Acceptable for MVP scope. |
| STK-005-N1 | REQ-009, REQ-010 | None |
| STK-005-N2 | REQ-011 | None |
| STK-005-N3 | REQ-008, REQ-010 | None |

**Coverage gaps noted:** STK-002-N2 (no-expertise usability) and STK-004-N3 (SINGLE-SOURCE disclosure) are partially addressed. These are low-priority coverage gaps; both are addressed as MEDIUM-priority needs by the verdict format (REQ-013) and confidence classification (REQ-012) respectively. Explicit requirements are not added to avoid requirement inflation; these should be revisited in Phase 3A verification.

---

## Requirements Quality Checklist

Per NASA-HDBK-1009A criteria:

| Criterion | Assessment | Evidence |
|-----------|-----------|---------|
| **Complete** | Pass | All 5 stakeholder groups analyzed; 21 formal requirements defined; 8 MUST-HAVE + 7 SHOULD-HAVE + 6 NICE-TO-HAVE acceptance criteria; all ADR-001 options traced |
| **Consistent** | Pass | No conflicting requirements identified. REQ-003 (zero-cost smoke) and REQ-005 (statistical comparison) are complementary, not contradictory: statistical comparison is opt-in (QA-004 applies only to smoke mode) |
| **Verifiable** | Pass | All 21 requirements have assigned verification methods (Test, Inspection, Analysis, Demonstration). Quality attributes have quantitative measurement definitions |
| **Traceable** | Pass | All requirements trace to stakeholder needs; all stakeholder needs trace to ADR-001 or orchestration plan sources; backward trace table confirms no orphan requirements |
| **Unambiguous** | Pass | Shall statements use the format "The framework shall [verb] [object] [constraint]." Terms "smoke mode," "T1," "T2," "IMPROVEMENT/REGRESSION/NO_EFFECT," "BCa," "FDR" are defined in context or reference ADR-001 |
| **Necessary** | Pass | Every requirement is traced to a stakeholder need that is documented in Section 1. No requirements are added speculatively. |

---

## Self-Review (S-010, H-15)

Pre-finalization quality assessment against the 6-dimension S-014 rubric:

**Completeness (0.20):** Five stakeholder groups analyzed with 16 stakeholder needs. 21 formal requirements across 5 subsections. 8 MUST-HAVE, 7 SHOULD-HAVE, 6 NICE-TO-HAVE acceptance criteria. 21-requirement backward trace with gap analysis. Quality attributes table (10 attributes with measurements, V-methods, and threshold justifications). Traceability matrix covers all ADR-001 options. Score: **0.94**

**Internal Consistency (0.20):** Smoke-mode zero-cost (REQ-003, QA-004) and statistical rigor (REQ-005) are explicitly reconciled as complementary through tiered architecture. Configurable N (REQ-004) is consistent with SINGLE-SOURCE disclosure (REQ-012). No conflicting shall statements detected. Acceptance criteria weights (AC-S01-07) replicate ADR-001 dimension weights exactly, maintaining lineage. T3 tier is consistently handled: REQ-001 reserves the architectural slot while explicitly deferring implementation, consistent with Section 5.4 lifecycle deferral. Score: **0.94**

**Methodological Rigor (0.20):** NPR 7123.1D Process 1 (stakeholder needs) and Process 2 (technical requirements) applied. NASA-HDBK-1009A completeness criteria explicitly assessed. Shall statement format follows "The {system} shall {verb} {object} {constraint}" pattern throughout. Three-tier acceptance criteria (MUST/SHOULD/NICE-TO-HAVE) provide structured scoring framework. V-methods assigned to both QA attributes (Section 2) and formal requirements (Section 3), using consistent vocabulary (Test, Inspection, Analysis, Demonstration). QA attribute selection derived from ISO/IEC 25010:2023 with explicit derivation note. Constitutional references validated against Jerry Constitution v1.1. Score: **0.93**

**Evidence Quality (0.15):** All requirements are grounded in ADR-001 source documents (Phase 1A, 1B, 1C findings). ADR-001 adversarial findings (RT-001, PM-001, PM-002, PM-005, PM-007, PM-008, RT-003) are explicitly cited in requirement rationale fields. Statistical method selections cite primary literature: BCa bootstrap (Efron & Tibshirani, 1993), Benjamini-Hochberg FDR (Benjamini & Hochberg, 1995), permutation tests (Good, 2005). QA attribute thresholds include explicit justification basis (engineering estimate, cost model, or analogous system comparison). SINGLE-SOURCE findings inherited and flagged. Note: WebSearch was unavailable in this environment; requirements are derived exclusively from ADR-001 and orchestration plan, which cite web-sourced Phase 1 research. Score: **0.91** (deduct for no direct web sourcing; mitigated by ADR-001 evidence chain and primary literature citations)

**Actionability (0.15):** Acceptance criteria in Section 4 are directly usable as scoring rubrics in Phase 5 trade study. Requirement IDs (REQ-NNN) are cited in traceability matrix and ready for Phase 3A verification scope definition. Quality attributes have quantitative thresholds with threshold justification basis documented (e.g., QA-001: 100%, QA-003: <= 60 seconds with 6x safety margin rationale, QA-005: <= $10.00 with cost model derivation). Deferred items are explicitly listed with re-visit conditions. Score: **0.94**

**Traceability (0.10):** All 21 requirements have parent STK need IDs. All 16 STK needs have source citations. Backward trace table confirms zero orphans. ADR-001 option traceability provided in forward trace table (all 3 options assessed per requirement). Interface table (Section 5.2) includes "Realized By" column mapping each interface to governing requirement IDs. Score: **0.93**

**Weighted composite:** (0.94 x 0.20) + (0.94 x 0.20) + (0.93 x 0.20) + (0.91 x 0.15) + (0.94 x 0.15) + (0.93 x 0.10) = 0.188 + 0.188 + 0.186 + 0.1365 + 0.141 + 0.093 = **0.933**

**Assessment:** 0.933 >= 0.92 quality target. PASS. Primary weakness is Evidence Quality (0.91) due to WebSearch being unavailable in this execution environment; requirements are derived from ADR-001 which cites web-sourced Phase 1A, 1B, 1C research. This is disclosed explicitly per P-022. Statistical method citations now reference primary literature directly.

---

## References

| Source | Type | Key Contribution |
|--------|------|-----------------|
| ADR-001-framework-architecture.md (`projects/PROJ-017-llm-skill-testing/decisions/ADR-001-framework-architecture.md`) | Internal artifact | Three options (A/B/C), 7 evaluation dimensions with weights, adversarial findings RT-001/PM-001/PM-002, cost calculations, tiered mode design |
| ORCHESTRATION_PLAN.md (`projects/PROJ-017-llm-skill-testing/orchestration/promptfoo-deep-analysis-20260303/ORCHESTRATION_PLAN.md`) | Internal artifact | Phase 1D requirements scope, cross-pollination protocol, Phase 5 trade study dimensions |
| NPR 7123.1D, Process 1 | NASA Standard | Stakeholder Expectations Definition -- identify stakeholders, elicit needs, prioritize |
| NPR 7123.1D, Process 2 | NASA Standard | Technical Requirements Definition -- formal shall statements, allocation, verification methods |
| NPR 7123.1D, Process 11 | NASA Standard | Requirements Management -- track changes, maintain traces, baseline |
| NASA-HDBK-1009A | NASA Handbook | Requirements quality criteria: necessary, unambiguous, consistent, complete, singular, achievable, verifiable |
| ISO/IEC 25010:2023 | International Standard | Systems and software quality models -- product quality characteristics used to derive QA attribute selection (Section 2) |
| Efron, B. & Tibshirani, R.J. (1993). *An Introduction to the Bootstrap*. Chapman & Hall/CRC. | Statistical literature | BCa bootstrap confidence intervals (Ch. 14): bias-corrected and accelerated intervals for small-N and skewed distributions (REQ-005) |
| Benjamini, Y. & Hochberg, Y. (1995). "Controlling the False Discovery Rate." *JRSS-B*, 57(1):289-300. | Statistical literature | FDR correction methodology for multiple comparisons (REQ-006) |
| Good, P.I. (2005). *Permutation, Parametric, and Bootstrap Tests of Hypotheses*. 3rd ed. Springer. | Statistical literature | Permutation test methodology: distribution-free exact p-values under exchangeability (REQ-005) |
| quality-enforcement.md (`.context/rules/quality-enforcement.md`) | Jerry governance | S-014 6-dimension rubric (Completeness 0.20, Internal Consistency 0.20, Methodological Rigor 0.20, Evidence Quality 0.15, Actionability 0.15, Traceability 0.10) |

---

## State Output (Agent Chaining)

```yaml
requirements_output:
  project_id: "PROJ-017"
  entry_id: "e-101"
  artifact_path: "projects/PROJ-017-llm-skill-testing/research/evaluation-criteria.md"
  summary: "21 formal requirements across 5 subsections; 5 stakeholder groups; 16 stakeholder needs; 8 MUST-HAVE + 7 SHOULD-HAVE + 6 NICE-TO-HAVE acceptance criteria; complete bidirectional traceability matrix covering ADR-001 Options A/B/C"
  requirements_count: 21
  stakeholder_needs_count: 16
  acceptance_criteria_count: 21  # 8 MUST-HAVE + 7 SHOULD-HAVE + 6 NICE-TO-HAVE
  trace_status: "complete"
  quality_score: 0.933
  quality_threshold: 0.920
  quality_verdict: "PASS"
  next_agent_hint: "Phase 2: ps-synthesizer loads this artifact for requirements alignment; Phase 3A: nse-verification loads this artifact for verification scope"
  nasa_processes_applied: ["Process 1 (Stakeholder Expectations)", "Process 2 (Technical Requirements Definition)", "Process 11 (Requirements Management)"]
  open_questions:
    - "STK-002-N2 (no-expertise usability) is partially addressed by REQ-013 verdict format; formal usability test criteria are deferred to post-MVP"
    - "T3 hybrid-proxy tier architectural slot reserved in REQ-001 but implementation deferred (ADR-001 PM-008); activation condition defined in Section 5.4"
    - "N calibration study (bootstrap stability at N=10..50) is a Phase 3 deliverable per ADR-001; REQ-004 minimum N=10 is provisional pending this study"
  blockers: []
```

---

*Generated by nse-requirements agent v2.3.0*
*NASA Standards: NPR 7123.1D, NASA-HDBK-1009A*
*Constitutional Compliance: Jerry Constitution v1.1 (P-002: file persisted, P-022: limitations disclosed, P-040: traces complete, P-041: V&V methods assigned, P-043: AI guidance disclaimer included)*
*Self-review score: 0.933 (target >= 0.92) -- PASS*
*Evidence Quality note: WebSearch unavailable in execution environment; requirements grounded in ADR-001 which cites web-sourced Phase 1A/1B/1C research*
