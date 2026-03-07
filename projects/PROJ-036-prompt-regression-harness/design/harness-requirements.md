---
DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
standards. It is advisory only and does not constitute official NASA guidance.
All SE decisions require human review and professional engineering judgment.
Not for use in mission-critical decisions without SME validation.
---

# Requirements Specification: Four-Layer Composite Test Harness

> **Project:** PROJ-036 (Prompt Regression Harness)
> **Entry:** Stream 1A
> **Date:** 2026-03-07
> **Status:** Draft (Iteration 3)
> **ADR Source:** PROJ-035/decisions/ADR-001-test-harness-architecture.md (ACCEPTED 2026-03-06)
> **Agent:** nse-requirements v2.3.0
> **Revision:** Iteration 3 — adds G/W/T acceptance criteria for NFR-005 and NFR-007; adds Appendix B Verification Artifact Map

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | What the system must do, in plain language |
| [L1: Stakeholder Needs](#l1-stakeholder-needs) | Elicited needs from ADR-001 stakeholder analysis |
| [L1: Functional Requirements](#l1-functional-requirements) | FR-001 through FR-030 with acceptance criteria |
| [L1: Non-Functional Requirements](#l1-non-functional-requirements) | NFR-001 through NFR-015 performance, reliability, maintainability, security, usability |
| [L1: Interface Specifications](#l1-interface-specifications) | Layer-to-layer and external interface contracts |
| [L1: FMEA-Derived Requirements](#l1-fmea-derived-requirements) | Requirements derived from FM-001 through FM-010 failure modes |
| [L1: Requirements Quality Checklist](#l1-requirements-quality-checklist) | Completeness, consistency, verifiability, traceability |
| [L2: Systems Perspective](#l2-systems-perspective) | Allocation matrix, risk implications, traceability strategy |
| [Traceability Matrix](#traceability-matrix) | Bidirectional traces: ADR-001 evidence to requirements |
| [Appendix A: Phase-to-Requirements Map](#appendix-a-phase-to-requirements-map) | FR and NFR delivery phase alignment with ADR-001 roadmap |
| [Appendix B: Verification Artifact Map](#appendix-b-verification-artifact-map) | Forward trace from each FR/NFR to planned test file location |
| [Self-Review (S-010)](#self-review-s-010) | Pre-finalization quality assessment |
| [References](#references) | NASA standards and source documents |

---

## L0: Executive Summary

The Four-Layer Composite Test Harness must automatically detect when a change to a Jerry agent definition (a system prompt file) causes a statistically significant regression in that agent's output quality. It does this by running the changed prompt against a collection of test cases, evaluating the outputs with multiple complementary quality metrics, and comparing the results to stored baseline measurements using proper statistical hypothesis testing — not simple threshold comparisons that cannot distinguish real quality degradation from random variation. Engineers who modify agent prompt files get an automated, evidence-based answer to the question "did I break anything?" before their change can be merged.

---

## L1: Stakeholder Needs

### Identified Stakeholders (NPR 7123.1D Process 1)

| ID | Stakeholder | Role | Primary Concern |
|----|-------------|------|-----------------|
| STK-001 | Jerry Framework Engineers | Prompt authors and refactoring engineers | Confident, safe prompt modification without manual testing |
| STK-002 | Framework Maintainers | Maintainers of 67+ agent definitions across 12 skills | Automated validation during model migration events |
| STK-003 | CI/CD System Operators | GitHub Actions workflow operators | Automated merge blocking when regressions are detected |
| STK-004 | Quality Reviewers | Engineers reviewing PRs that modify agent definitions | Evidence-based, statistically valid regression reports |
| STK-005 | Future Extension Engineers | Engineers adding PPI calibration and perturbation testing (Phases E-F) | Extensible architecture that accommodates future layers |

### Stakeholder Needs Table

| ID | Stakeholder | Need | Priority | Coverage | ADR Source |
|----|-------------|------|----------|----------|------------|
| STK-N-001 | STK-001 | Know whether a prompt change caused a behavioral regression before merge | H | Primary: FR-003, FR-015, FR-018; Secondary: all Layer 1-4 FRs | ADR-001 L1 Problem Statement #1 |
| STK-N-002 | STK-002 | Systematically validate all 67 agent definitions against new model versions with statistical confidence | H | Primary: FR-028 | ADR-001 L1 Problem Statement #2 |
| STK-N-003 | STK-003 | Block pull request merges when statistically significant regressions are detected | H | Primary: FR-002, FR-018; Secondary: NFR-005 | ADR-001 L1 Constraints M-003 |
| STK-N-004 | STK-004 | Receive regression reports with confidence intervals, not just binary pass/fail | H | Primary: FR-016, FR-018; Secondary: FR-013, FR-017 | ADR-001 L1 Forces F-2 |
| STK-N-005 | STK-001 | Assert behavioral consistency without needing exact expected outputs (oracle problem) | H | Primary: FR-010, FR-011, FR-012; Secondary: FR-013 | ADR-001 L1 Forces F-1 |
| STK-N-006 | STK-001 | Evaluate prompts without false alarms caused by normal LLM output variance | H | Primary: FR-014, FR-015, FR-021; Secondary: FR-003, FR-008, NFR-006, NFR-007, NFR-010 | ADR-001 L1 Forces F-2 |
| STK-N-007 | STK-003 | Trigger regression testing automatically on every PR that modifies agent definition files | H | Primary: FR-002 | ADR-001 L1 Forces F-4 |
| STK-N-008 | STK-001 | Evaluate at different cost/thoroughness trade-offs (fast smoke check vs. full statistical analysis) | M | Primary: FR-005; Secondary: NFR-001, NFR-002, NFR-004 | ADR-001 L1 Technical Implementation, Tiered Evaluation Modes |
| STK-N-009 | STK-002 | Track regression trends across prompt versions over time | M | Primary: FR-029; Secondary: FR-024 | ADR-001 L2 Architectural Implications |
| STK-N-010 | STK-005 | Add new evaluation layers without refactoring existing layers | M | Primary: FR-030; Secondary: NFR-012 | ADR-001 L2 Long-Term Evolution Path |

> **Note on STK-N-001 coverage:** STK-N-001 is the most general stakeholder need and is incidentally addressed by most functional requirements. The Coverage column distinguishes Primary requirements (directly and primarily implement the need) from Secondary requirements (contribute to the need as a side effect of implementing other concerns). Primary requirements for STK-N-001 are FR-003 (before/after comparison execution), FR-015 (Wilcoxon comparison), and FR-018 (regression report with PR integration).

---

## L1: Functional Requirements

### Layer 1: CI/CD Regression Gate (promptfoo)

---

**FR-001**

**Title:** Declarative YAML Test Case Definitions

**Description:** The system shall define regression test cases in declarative YAML files stored under `tests/prompt-regression/`, referencing agent definition files by path and specifying assertion types per test variable.

**Acceptance Criteria:**
- Given a Jerry agent definition file at `skills/{skill}/agents/{agent}.md`, When a test case YAML file is created for that agent, Then the YAML file shall reference the agent definition using a `file://` path prefix and define at least one test variable with at least one assertion.
- Given a YAML test case file, When parsed by promptfoo, Then the file shall validate against the promptfoo YAML schema without error.
- The YAML format shall support at minimum: `description`, `prompts` (file references), `providers` (LLM model identifiers), `tests` (variables and assertions).

**Rationale:** Declarative configuration is required to support PR-triggered automation and to separate test authorship from harness implementation. promptfoo's YAML schema was selected as the format per Phase 1B survey (E-004: "Purpose-built for this exact use case"). [ADR-001 L1 Decision, Layer 1; ADR-001 Test Case Definition Format section]

**Parent:** STK-N-001, STK-N-007

**Verification Method:** Inspection (review YAML schema conformance), Demonstration (execute `promptfoo eval` against sample YAML)

**Priority:** Must

**Layer:** Layer 1 (promptfoo CI/CD gate)

**Status:** Draft

---

**FR-002**

**Title:** PR-Triggered GitHub Action Regression Gate

**Description:** The system shall include a GitHub Actions workflow that automatically triggers promptfoo evaluation when pull request file changes include any file matching the pattern `skills/*/agents/*.md`.

**Acceptance Criteria:**
- Given a pull request that modifies one or more files matching `skills/*/agents/*.md`, When the PR is created or updated, Then the GitHub Actions workflow shall automatically execute the promptfoo regression evaluation for the affected agent(s).
- Given a pull request that does not modify any agent definition file, When the PR is created, Then the GitHub Actions workflow shall not execute the regression evaluation (to avoid unnecessary cost).
- The GitHub Actions workflow step shall produce a non-zero exit code when a statistically significant regression is detected, causing the CI check to fail and blocking merge per STK-N-003.

**Rationale:** Automated PR-triggered gating is required to intercept regressions before they reach the main branch. This directly addresses Phase 1C Gap #4: "No evaluated SDK provides a PR-triggered regression gate." [ADR-001 L1 Forces F-4; E-008; ADR-001 Constraints M-003]

**Parent:** STK-N-003, STK-N-007

**Verification Method:** Demonstration (open a test PR modifying an agent definition file and observe automated workflow execution)

**Priority:** Must

**Layer:** Layer 1 (promptfoo CI/CD gate)

**Status:** Draft

---

**FR-003**

**Title:** Before/After Prompt Version Comparison Execution

**Description:** The system shall execute both the baseline prompt version (Version A, from the target branch) and the modified prompt version (Version B, from the PR branch) against the configured LLM provider, collecting raw outputs for downstream evaluation.

**Acceptance Criteria:**
- Given two prompt versions (A and B) and a configured LLM provider, When a regression evaluation is triggered, Then the system shall execute both versions against the same set of test case inputs.
- Raw outputs from both Version A and Version B runs shall be preserved and passed to Layer 2 (DeepEval) for metric evaluation.
- The number of runs per version shall be configurable per evaluation mode: Smoke=1, Standard=10, Full=30.

**Rationale:** Regression detection requires a before/after comparison. This is the novel contribution identified in ADR-001: "The comparison logic between prompt versions is the novel contribution this harness must make." [ADR-001 L0 Key Rationale #1; ADR-001 L1 Forces F-6; E-007]

**Parent:** STK-N-001, STK-N-006

**Verification Method:** Test (execute evaluation in each mode and verify output count matches configured N)

**Priority:** Must

**Layer:** Layer 1 (promptfoo CI/CD gate)

**Status:** Draft

---

**FR-004**

**Title:** Version Key Management via Git Commit Hash

**Description:** The system shall identify each prompt version using a composite key consisting of the git commit hash and the agent definition file path, stored in a baseline artifact store. The system shall validate that the baseline version key matches the current main branch commit hash before accepting a baseline for comparison.

**Acceptance Criteria:**
- Given a prompt evaluation result, When the result is stored as a baseline, Then the baseline record shall include the git commit hash of the agent definition file and the file path as a composite key.
- Given a baseline retrieval operation, When the stored commit hash does not match the target branch commit hash for the same file, Then the system shall reject the baseline with an explicit error message identifying the mismatch.
- The composite key format shall be `{git_commit_hash}:{file_path}` (e.g., `abc1234:skills/problem-solving/agents/ps-researcher.md`).

**Rationale:** Prompt version mismatch is FMEA failure mode FM-005 (S=9, O=4, D=4, RPN=144). Using git commit hash as the version identifier eliminates ambiguity between prompt versions and prevents comparison against a stale baseline. [ADR-001 L1 Risks FM-005; ADR-001 L1 Implementation Roadmap Phase A]

**Parent:** STK-N-001

**Verification Method:** Test (verify baseline store rejects mismatched commit hash; verify composite key format in stored artifact)

**Priority:** Must

**Layer:** Layer 1 (promptfoo CI/CD gate)

**Status:** Draft

---

**FR-005**

**Title:** Tiered Evaluation Mode Selection

**Description:** The system shall support three tiered evaluation modes — Smoke, Standard, and Full — selectable per evaluation invocation. Each tier defines the number of LLM runs per version, the set of active metrics, and whether statistical analysis is performed.

**Acceptance Criteria:**
- Smoke mode: N=1 run per version; deterministic metrics only (structural checks, format compliance); no statistical comparison; report labeled "STRUCTURAL ONLY — not statistically valid".
- Standard mode: N=10 runs per version; deterministic plus debiased LLM-as-Judge metrics; statistical comparison performed only if N >= 20 is met by aggregating runs over time, otherwise the mode produces a warning that statistical analysis requires more runs.
- Full mode: N=30 runs per version; all active layers (Layers 1-4) including metamorphic relation checks and full Wilcoxon statistical analysis; N >= 20 enforced at runtime.
- The evaluation mode shall be specifiable as a CLI argument, GitHub Action input parameter, and environment variable.

**Rationale:** Cost control is required to make the harness viable for routine use. FM-006 (LLM cost overrun, RPN=140) is mitigated by tiered modes. Smoke mode explicitly labels its output as non-statistical to prevent the false confidence documented in FM-002. [ADR-001 L1 Technical Implementation, Tiered Evaluation Modes; ADR-001 L1 Risks FM-006, FM-002]

**Parent:** STK-N-008

**Verification Method:** Test (execute each mode and verify: run counts, active metric sets, report label in Smoke mode, runtime N enforcement in Full mode)

**Priority:** Must

**Layer:** Layer 1 (promptfoo CI/CD gate), Layer 4 (statistical engine)

**Status:** Draft

---

### Layer 2: Evaluation Backend (DeepEval)

---

**FR-006**

**Title:** DeepEval pytest Plugin Integration

**Description:** The system shall integrate DeepEval as a pytest plugin, enabling all Layer 2 evaluation metrics to be executed via `uv run pytest tests/prompt-regression/` without requiring a separate evaluation runtime.

**Acceptance Criteria:**
- Given a pytest invocation with `uv run pytest tests/prompt-regression/`, When the DeepEval plugin is installed and configured, Then all DeepEval metric evaluations shall execute within the pytest test run.
- The DeepEval package version shall be pinned in `uv.lock` and shall not be updated without a re-baseline operation.
- DeepEval shall be installable via `uv add deepeval` with no system Python invocations required.

**Rationale:** pytest is the mandated test runner per H-20 ("pytest as test runner backbone"). DeepEval is a pytest plugin, making it the natural integration point. This alignment was the primary selection criterion: PAT-002 identified pytest as the convergence point across all evaluated frameworks. [ADR-001 L1 Forces F-3; ADR-001 L1 Decision Layer 2; E-005; E-015 PAT-002]

**Parent:** STK-N-001

**Verification Method:** Demonstration (execute `uv run pytest tests/prompt-regression/` and observe DeepEval metrics evaluated)

**Priority:** Must

**Layer:** Layer 2 (DeepEval evaluation backend)

**Status:** Draft

---

**FR-007**

**Title:** G-Eval Custom Criteria Evaluation

**Description:** The system shall implement G-Eval evaluation criteria using DeepEval's G-Eval metric, allowing Jerry-specific quality criteria to be defined in natural language and evaluated by a debiased LLM-as-Judge.

**Acceptance Criteria:**
- Given a set of Jerry-specific quality criteria expressed in natural language (e.g., "The output provides an L0 executive summary"), When G-Eval is invoked, Then the metric shall return a numeric score between 0.0 and 1.0 for each criterion.
- At minimum, the following criteria shall be defined as G-Eval metrics: L0/L1/L2 section presence, stakeholder-appropriate tone, actionable findings, and requirement traceability presence.
- G-Eval criteria definitions shall be stored as YAML or JSON files under `tests/prompt-regression/criteria/` for maintainability and version control.

**Rationale:** Jerry agents produce structured outputs with specific quality properties. G-Eval's natural language criteria approach allows these properties to be verified without exact-output matching, directly addressing the oracle problem (F-1). [ADR-001 L1 Technical Implementation Layer 2; E-009; ADR-001 L0 Key Rationale #1]

**Parent:** STK-N-005

**Verification Method:** Test (evaluate a known-good agent output against defined criteria and verify score >= 0.85; evaluate a deliberately degraded output and verify score <= 0.50)

**Priority:** Must

**Layer:** Layer 2 (DeepEval evaluation backend)

**Status:** Draft

---

**FR-008**

**Title:** Deterministic Property Assertions

**Description:** The system shall implement deterministic property assertions that verify structural and format properties of agent outputs without invoking an LLM evaluator, producing binary pass/fail results.

**Acceptance Criteria:**
- Given an agent output, When deterministic assertions are evaluated, Then the system shall check at minimum: presence of required section markers (e.g., `## L0`, `## L1`, `## L2`), absence of prohibited content patterns (secrets, API keys), and output length within configured bounds.
- Deterministic assertions shall execute in < 100ms per test case.
- Deterministic assertions shall produce the same result on every invocation given the same input (zero stochasticity).

**Rationale:** Deterministic assertions provide the structural safety net that is valid even in Smoke mode (N=1). They address the subset of requirements that do not require statistical aggregation. [ADR-001 L1 Technical Implementation, Tiered Evaluation Modes; ADR-001 Test Case Definition Format; E-008]

**Parent:** STK-N-001, STK-N-006

**Verification Method:** Test (execute deterministic assertions against outputs with and without required sections; verify execution time < 100ms; verify identical results across 10 consecutive invocations)

**Priority:** Must

**Layer:** Layer 2 (DeepEval evaluation backend)

**Status:** Draft

---

**FR-009**

**Title:** Score Array Collection and Export

**Description:** The system shall collect all metric scores produced by Layer 2 evaluation as ordered numeric arrays, one array per metric per prompt version, and export these arrays in a structured format consumable by Layer 3 (metamorphic relations) and Layer 4 (statistical engine).

**Acceptance Criteria:**
- Given N evaluation runs for a prompt version, When Layer 2 evaluation completes, Then the system shall produce one array of N scores per metric, where each score is a float in [0.0, 1.0].
- Score arrays shall be serialized to JSON with the following structure: `{"metric_id": str, "version_key": str, "scores": list[float], "run_count": int, "evaluation_mode": str}`.
- Score arrays shall be written to a deterministic output path: `tests/prompt-regression/results/{agent_id}/{version_key}/{metric_id}.json`.

**Rationale:** The statistical engine (Layer 4) and metamorphic relation framework (Layer 3) both consume arrays of quality scores. A common score array format enables both layers to operate on the same data structure without requiring a transformation layer. [ADR-001 L2 Long-Term Evolution Path; ADR-001 L1 Technical Implementation Layer 2 + Layer 4 integration; E-016]

**Parent:** STK-N-001

**Verification Method:** Inspection (verify JSON schema of output files); Test (verify array length matches N for each mode)

**Priority:** Must

**Layer:** Layer 2 (DeepEval evaluation backend)

**Status:** Draft

---

### Layer 3: Metamorphic Relation Framework

---

**FR-010**

**Title:** Five Universal Metamorphic Relations Implementation

**Description:** The system shall implement the following five universal metamorphic relations (MRs) as custom DeepEval metrics: MR-001 Paraphrase Consistency, MR-002 Negation Handling, MR-003 Irrelevant Context Appendation, MR-004 Formatting Perturbation, MR-005 Language Round-Trip.

**Acceptance Criteria:**
- MR-001 (Paraphrase Consistency): Given a system prompt and a paraphrased variant, the quality score difference shall not exceed a configurable tolerance (default: ±0.05).
- MR-002 (Negation Handling): Given a user query and a negated variant, the output response type (factual vs. refusal) shall be consistent with the semantic intent of the negation.
- MR-003 (Irrelevant Context Appendation): Given a user query with an appended irrelevant sentence, the quality score shall not decrease by more than a configurable tolerance (default: ±0.10) compared to the unmodified query.
- MR-004 (Formatting Perturbation): Given a system prompt with varied whitespace, capitalization, or line-break formatting (without semantic change), the quality score shall not change by more than a configurable tolerance (default: ±0.05).
- MR-005 (Language Round-Trip): Given a user query translated to a second language and back to the original, the quality score shall not decrease by more than a configurable tolerance (default: ±0.15).
- Each MR shall be implemented as a class inheriting from DeepEval's `BaseMetric` with a `measure(test_case: LLMTestCase) -> float` method returning 0.0 (violation) or 1.0 (pass).

**Rationale:** Metamorphic relations are the academically validated solution to the LLM oracle problem identified as the central challenge in ADR-001 Forces F-1 and PAT-001. The LLMORPH study (ASE 2025, 560,000 tests, 8.6% false positive rate) validated this approach's effectiveness. The five MRs selected cover the most universal behavioral consistency properties applicable across all Jerry agent types. [ADR-001 L0 Executive Summary #3; ADR-001 L1 Technical Implementation Layer 3; ADR-001 Architecture Diagram; E-010; E-002]

**Parent:** STK-N-005, STK-N-006

**Verification Method:** Test (calibrate each MR against 100+ real Jerry agent output pairs and verify false positive rate <= 15%; verify pass/fail output for constructed violation cases)

**Priority:** Must

**Layer:** Layer 3 (Metamorphic Relation Framework)

**Status:** Draft

---

**FR-011**

**Title:** MR Tolerance Calibration from Real Output Pairs

**Description:** The system shall provide a calibration utility that accepts a dataset of real Jerry agent output pairs and computes appropriate tolerance values for each metamorphic relation, storing calibrated tolerances in a configuration file.

**Acceptance Criteria:**
- Given a dataset of at least 100 real agent output pairs, When the calibration utility is executed, Then the system shall compute the empirical distribution of score deltas for each MR type and set the tolerance at the 95th percentile of observed deltas.
- Calibrated tolerances shall be stored in `tests/prompt-regression/mr-config.yaml` with the format `{mr_id}: {tolerance}`.
- The calibration utility shall warn when fewer than 100 pairs are provided, as this reduces calibration accuracy.
- Until calibrated, MR violations shall be reported as warnings (not failures) to prevent false regression blocks.

**Rationale:** FM-009 (MR violation is ambiguous, RPN=125) is mitigated by calibrating MR tolerances against real output pairs rather than using arbitrary defaults. The "use MR violations as warnings until validated" mitigation from FM-009 is captured here as a requirement. [ADR-001 L1 Risks FM-009; ADR-001 Implementation Roadmap Phase D]

**Parent:** STK-N-005, STK-N-006

**Verification Method:** Test (execute calibration with synthetic dataset; verify output config file format; verify warning threshold behavior when N < 100)

**Priority:** Must

**Layer:** Layer 3 (Metamorphic Relation Framework)

**Status:** Draft

---

**FR-012**

**Title:** Jerry-Specific Metamorphic Relation Definitions

**Description:** The system shall provide a mechanism for defining agent-specific metamorphic relations beyond the five universal MRs, allowing engineers to encode Jerry-specific behavioral expectations for individual agent types.

**Acceptance Criteria:**
- Given a Jerry agent type (e.g., ps-researcher, nse-requirements), When an agent-specific MR is defined, Then the system shall execute that MR only for test cases associated with that agent type.
- Agent-specific MRs shall be defined using the same `BaseMetric` interface as the universal MRs.
- A minimum of two agent-specific MRs per agent class shall be defined during Phase D (one structural consistency MR and one behavioral consistency MR).

**Rationale:** Universal MRs cover cross-cutting behavioral properties, but individual Jerry agents have specific behavioral expectations (e.g., nse-requirements must always produce a traceability matrix; ps-researcher must include L0/L1/L2 sections). Agent-specific MRs encode these expectations without requiring exact-output comparison. FM-003 (incomplete MR coverage, RPN=240) is the third-highest-priority failure mode; agent-specific MRs are the primary mechanism for narrowing that coverage gap. [ADR-001 L1 Technical Implementation Layer 3; ADR-001 L1 Negative Consequences #3; ADR-001 L1 Risks FM-003; E-016]

**Parent:** STK-N-005

**Verification Method:** Inspection (verify at least two agent-specific MRs defined per agent class after Phase D); Demonstration (show an agent-specific MR executing only for its target agent type)

> **Phase dependency note:** The Inspection verification criterion is a Phase D acceptance criterion. Prior to Phase D, this requirement is verified by demonstrating the mechanism exists (per-agent MR definition capability is present) even if minimum MR count has not yet been reached.

**Priority:** Should

**Layer:** Layer 3 (Metamorphic Relation Framework)

**Status:** Draft

---

**FR-013**

**Title:** MR Coverage Tracking Metric

**Description:** The system shall compute and report a metamorphic relation coverage percentage for each agent definition — the fraction of the agent's known behavioral properties that are covered by at least one MR assertion — and include this metric in the CI/CD regression report.

**Acceptance Criteria:**
- Given a set of MR definitions and a list of documented behavioral properties for an agent (defined in the behavioral property registry per the registry specification below), When the coverage report is generated, Then the coverage percentage shall equal (number of properties covered by at least one MR) / (total documented behavioral properties) * 100.
- Coverage below 50% for any agent shall produce a warning in the CI/CD report.
- The coverage metric shall be included in the regression test summary report visible in the GitHub PR check output.

**Behavioral Property Registry Specification:** The behavioral property registry shall consist of per-agent YAML files stored at `contracts/per-agent/{agent-name}.contract.yaml`. Each file shall list the agent's documented behavioral properties as an array of named properties with description fields (e.g., `- name: "produces_l0_section" description: "Output always contains an L0 executive summary section"`). The registry format and content will be fully specified in `contracts/behavioral-contracts.md` as part of Stream 1D deliverables. Until Stream 1D is complete, FR-013 implementation shall use a stub registry file for testing purposes.

> **Path note:** `contracts/per-agent/` is the authoritative location for behavioral contract files (Stream 1D deliverable). The `tests/prompt-regression/` directory contains test execution artifacts (YAML test cases, benchmark scripts, result files) but not the contracts themselves. FR-013 coverage computation reads contract files from `contracts/per-agent/` and writes coverage results to the test execution report.

**Rationale:** FM-003 (incomplete MR coverage, RPN=240) is the third-highest-priority failure mode. Tracking coverage makes the gap visible and enables prioritization of new MR definitions. This requirement directly implements the "track MR coverage metric" mitigation from FM-003. [ADR-001 L1 Risks FM-003; ADR-001 Implementation Roadmap Phase D]

**Parent:** STK-N-004

**Verification Method:** Test (create a test agent with 4 documented behavioral properties and 2 MR assertions; verify coverage report shows 50% and triggers warning)

**Priority:** Should

**Layer:** Layer 3 (Metamorphic Relation Framework)

**Status:** Draft

---

### Layer 4: Statistical Comparison Engine

---

**FR-014**

**Title:** Minimum Sample Size Enforcement (N >= 20)

**Description:** The system shall enforce a minimum sample size of N=20 runs per prompt version before executing Wilcoxon signed-rank comparison. When N < 20, the system shall raise an `InsufficientSamplesError` with a message identifying the actual sample counts and directing the user to use Smoke mode for single-run structural checks.

**Acceptance Criteria:**
- Given score arrays with len(scores_a) < 20 or len(scores_b) < 20, When `compare_versions()` is called, Then the system shall raise `InsufficientSamplesError` with message format: "Wilcoxon requires N >= 20 per version (got {N_a}, {N_b}). Use Smoke mode for single-run structural checks only."
- Given score arrays with len(scores_a) >= 20 and len(scores_b) >= 20, When `compare_versions()` is called, Then the function shall execute without raising this error.
- The N=20 threshold shall be a named constant `MIN_STATISTICAL_SAMPLE_SIZE = 20` in `jerry/testing/stats.py`.

**Rationale:** Wilcoxon signed-rank tests require adequate sample sizes for reliable results. The ICML 2025 consensus identifies CLT-based methods as performing "very poorly" for small N, "usually dramatically underestimating uncertainty." The N=20 threshold is the minimum enforced by the ADR code example. This requirement is a direct formalization of the FM-002 mitigation. [ADR-001 L1 Technical Implementation, code example; ADR-001 L1 Risks FM-002; E-011; ADR-001 L1 Negative Consequences #4]

**Parent:** STK-N-006

**Verification Method:** Test (execute `compare_versions()` with N=19 and N=20 inputs; verify exception raised for N=19 and not raised for N=20)

**Priority:** Must

**Layer:** Layer 4 (Statistical comparison engine)

**Status:** Draft

---

**FR-015**

**Title:** Wilcoxon Signed-Rank Version Comparison

**Description:** The system shall compare two prompt versions using the Wilcoxon signed-rank test (two-sided, alpha=0.05) applied to the paired score arrays from Layer 2, producing a p-value and a regression classification.

**Acceptance Criteria:**
- Given score arrays `scores_a` (baseline) and `scores_b` (candidate), both with N >= 20, When `compare_versions()` is called, Then `scipy.stats.wilcoxon` shall be invoked on the paired arrays.
- The regression classification shall follow: `p < 0.05 AND mean(scores_b) < mean(scores_a)` → `REGRESSION`; `p < 0.10` → `MARGINAL`; otherwise → `NO_REGRESSION`.
- The function shall return a `RegressionResult` object containing: `classification` (enum), `p_value` (float), `statistic` (float), `mean_a` (float), `mean_b` (float), `ci_a` (tuple[float, float]), `ci_b` (tuple[float, float])`.
- The default alpha shall be 0.05 and shall be a configurable parameter with valid range (0.01, 0.10).

**Rationale:** Wilcoxon signed-rank is the correct non-parametric test for paired score comparison when the score distribution is not guaranteed to be normal — which it is not for LLM evaluation scores. This resolves the universal statistical rigor gap identified across all 7 evaluated frameworks (Force F-2, PAT-006). [ADR-001 L1 Technical Implementation, compare_versions() code; ADR-001 L1 Forces F-2; E-003; E-011; E-018]

**Parent:** STK-N-004, STK-N-006

**Verification Method:** Test (verify p-value computation against known statistical test cases; verify classification thresholds produce correct enum values; verify RegressionResult fields are populated)

**Priority:** Must

**Layer:** Layer 4 (Statistical comparison engine)

**Status:** Draft

---

**FR-016**

**Title:** Wilson Score Confidence Intervals per Metric

**Description:** The system shall compute Wilson score confidence intervals for each metric's pass rate (proportion of scores >= 0.92) for both prompt versions, using `statsmodels.stats.proportion.proportion_confint` with method="wilson".

**Acceptance Criteria:**
- Given a score array for one metric and one version, When Wilson score intervals are computed, Then the system shall compute the proportion of scores >= 0.92 and compute the 95% Wilson score confidence interval for that proportion.
- The 0.92 pass-rate threshold shall be the named constant `QUALITY_PASS_THRESHOLD = 0.92` in `jerry/testing/stats.py`, consistent with the Jerry quality gate threshold (H-13).
- Confidence intervals shall be reported in the regression summary as: "Version A: [{ci_lower:.3f}, {ci_upper:.3f}]; Version B: [{ci_lower:.3f}, {ci_upper:.3f}]".

**Rationale:** Wilson score intervals quantify uncertainty around each version's quality estimate, enabling stakeholders to understand both the point estimate and its uncertainty. This is required per STK-N-004 (evidence-based reports with confidence intervals). The 0.92 threshold aligns with H-13 (Jerry quality gate). [ADR-001 L1 Technical Implementation, compare_versions() code; ADR-001 L0 Executive Summary #4; E-011]

**Parent:** STK-N-004

**Verification Method:** Test (compute Wilson intervals for known proportions and verify against analytically expected bounds; verify interval format in report output)

**Priority:** Must

**Layer:** Layer 4 (Statistical comparison engine)

**Status:** Draft

---

**FR-017**

**Title:** Bonferroni Correction for Multi-Metric Comparison

**Description:** The system shall apply Bonferroni correction when performing Wilcoxon signed-rank tests across multiple metrics simultaneously, dividing the alpha threshold by the number of metrics tested to control the family-wise error rate.

**Acceptance Criteria:**
- Given K metrics evaluated simultaneously, When multi-metric comparison is performed, Then the effective alpha per test shall be `alpha / K` (e.g., for K=5 metrics and alpha=0.05, the per-test threshold is 0.01).
- The corrected alpha shall be applied to the Wilcoxon p-value for each metric's regression classification.
- The regression report shall disclose the Bonferroni correction applied: "Bonferroni correction applied: alpha={alpha}, K={K}, per-metric threshold={alpha/K:.4f}".

**Rationale:** Testing multiple metrics simultaneously inflates the family-wise Type I error rate. Without correction, the probability of at least one false regression alarm increases linearly with the number of metrics. Bonferroni correction was specified in ADR-001 as the correction method alongside Wilcoxon. [ADR-001 L1 Decision Layer 4 description; ADR-001 Options Evaluation Dimension 4: "Full statistical rigor: Wilson score intervals, Wilcoxon signed-rank, Bonferroni correction"]

**Parent:** STK-N-004, STK-N-006

**Verification Method:** Test (verify corrected alpha calculation for K=3 and K=7 metrics; verify correction disclosed in report output)

**Priority:** Must

**Layer:** Layer 4 (Statistical comparison engine)

**Status:** Draft

---

**FR-018**

**Title:** Regression Classification Report with PR Integration

**Description:** The system shall produce a structured regression classification report for each evaluation and post it as a comment or status check to the associated GitHub pull request. The report shall include the regression verdict, p-value, confidence intervals, and per-metric results. Report generation and GitHub status API integration are implemented in `jerry/testing/layer4_stats.py` (see FR-030 and the module architecture note in FR-019).

**Acceptance Criteria:**
- Given a completed evaluation, When the regression report is generated, Then the report shall include at minimum: overall verdict (NO_REGRESSION / MARGINAL / REGRESSION / STRUCTURAL ONLY), per-metric Wilcoxon results (p-value, classification), Wilson confidence intervals per version per metric, and Bonferroni correction disclosure.
- A REGRESSION verdict shall set the GitHub commit status to "failure", blocking merge.
- A MARGINAL verdict shall set the GitHub commit status to "success" with a warning annotation.
- A NO_REGRESSION verdict shall set the GitHub commit status to "success".
- A STRUCTURAL ONLY verdict (Smoke mode) shall be labeled explicitly and shall not set a blocking status.

**Rationale:** The regression report is the primary artifact delivered to STK-N-004 (quality reviewers). CI/CD merge blocking on REGRESSION verdict is required per STK-N-003 and ADR-001 Constraints M-003. [ADR-001 Architecture Diagram, CI/CD Gate Decision; ADR-001 L1 Constraints M-003]

**Parent:** STK-N-003, STK-N-004

**Verification Method:** Demonstration (run evaluation producing REGRESSION verdict and verify GitHub PR status set to failure; run NO_REGRESSION and verify pass status)

**Priority:** Must

**Layer:** Layer 4 (Statistical comparison engine), Layer 1 (promptfoo CI/CD gate)

**Status:** Draft

---

**FR-019**

**Title:** Shared Statistical Module (jerry/testing/stats.py)

**Description:** The system shall implement the core statistical comparison functions in a shared Python module at `jerry/testing/stats.py` that is usable by both PROJ-036 (prompt regression) and PROJ-017 (skill evaluation framework).

**Module Architecture Note:** The harness uses two distinct Layer 4 modules with a clear dependency relationship:
- `jerry/testing/stats.py` — The shared statistical function library. Contains `compare_versions()`, `wilson_score_intervals()`, `InsufficientSamplesError`, `RegressionResult`, `MIN_STATISTICAL_SAMPLE_SIZE`, and `QUALITY_PASS_THRESHOLD`. This module operates on generic `list[float]` inputs and has no project-specific imports.
- `jerry/testing/layer4_stats.py` — The Layer 4 pipeline orchestration module. Imports and coordinates functions from `jerry/testing/stats.py`, handles report formatting, and manages GitHub Actions status API integration. `layer4_stats.py` depends on `stats.py`; they are distinct modules with different responsibilities.

**Acceptance Criteria:**
- The module at `jerry/testing/stats.py` shall export at minimum: `compare_versions()` (Wilcoxon signed-rank), `wilson_score_intervals()`, `InsufficientSamplesError`, `RegressionResult` (enum), `MIN_STATISTICAL_SAMPLE_SIZE`, `QUALITY_PASS_THRESHOLD`.
- The module shall not import any PROJ-036-specific or PROJ-017-specific code; it shall operate on generic `list[float]` inputs.
- The module shall include full type annotations and docstrings per H-11.
- The module shall be importable via `from jerry.testing.stats import compare_versions`.
- The `jerry/testing/layer4_stats.py` orchestration module shall import statistical functions exclusively from `jerry.testing.stats`; it shall not reimplement statistical logic.

**Rationale:** ADR-001 explicitly identifies shared statistical infrastructure as a positive consequence: "A shared Python statistical module (`jerry/testing/stats.py`) serves both PROJ-017 and PROJ-035 without infrastructure duplication." This requirement operationalizes that architectural intent. The separation between `stats.py` (pure computation) and `layer4_stats.py` (pipeline orchestration) enforces the single-responsibility principle and keeps the shared module free of project-specific concerns. [ADR-001 L1 Consequences Positive #2; ADR-001 L1 PROJ-017 ADR-002 Relationship, Shared Infrastructure #2]

**Parent:** STK-N-001

**Verification Method:** Inspection (verify module exports match specification; verify type annotations and docstrings present per H-11; verify `layer4_stats.py` imports from `stats.py` not vice versa); Test (import module from both PROJ-036 and PROJ-017 test contexts)

**Priority:** Must

**Layer:** Layer 4 (Statistical comparison engine)

**Status:** Draft

---

**FR-020**

**Title:** Baseline Store with Quality Gate Acceptance Criteria

**Description:** The system shall maintain a baseline artifact store that records score arrays for prompt version A. Before a baseline is accepted into the store, the system shall verify that the candidate baseline's quality score passes the quality gate (>= 0.92 average score across all metrics).

**Acceptance Criteria:**
- Given a candidate baseline score array, When the baseline acceptance check runs, Then the system shall compute the mean score across all metrics and reject the baseline if mean < 0.92, logging the rejection with the actual score.
- Given an accepted baseline, When stored, Then the baseline record shall include: version key (git hash + file path), mean quality score, per-metric score arrays, and ISO-8601 timestamp.
- A baseline audit CLI command (`jerry test baseline audit`) shall list all stored baselines with their version keys, acceptance scores, and ages.

**Rationale:** FM-010 (stale baseline captures known-poor prompt version, RPN=144) is mitigated by the baseline quality gate. Comparing a candidate against a known-bad baseline produces meaningless regression results. [ADR-001 L1 Risks FM-010; ADR-001 Implementation Roadmap Phase E]

**Parent:** STK-N-001

**Verification Method:** Test (attempt to store a baseline with mean score 0.85; verify rejection and log message; attempt to store with mean score 0.93; verify acceptance and stored fields)

**Priority:** Must

**Layer:** Layer 1 (promptfoo CI/CD gate), Layer 4 (Statistical comparison engine)

**Status:** Draft

---

### Cross-Cutting Functional Requirements

---

**FR-021**

**Title:** LLM-as-Judge Debiasing via Position Randomization and Rubric Shuffling

**Description:** The system shall implement position randomization and rubric shuffling for all LLM-as-Judge evaluations, randomizing the order in which evaluated outputs are presented to the judge and the order in which rubric criteria are listed.

**Acceptance Criteria:**
- Given two outputs presented to an LLM judge for comparison, When position randomization is active, Then the system shall randomize whether Version A or Version B appears first in the judge prompt, and adjust score assignment accordingly.
- Given a rubric with K criteria, When rubric shuffling is active, Then the criteria shall appear in a random order different from their definition order on each judge invocation.
- Both debiasing techniques shall be enabled by default and disableable only via explicit configuration with a logged warning.
- The debiasing configuration shall be documented in a `debiasing-config.yaml` file under `tests/prompt-regression/`.

**Rationale:** LLM-as-Judge without debiasing achieves 80-87% human correlation, but vanilla usage "cannot replace human expert verification for high-stakes evaluation" (Phase 1D Innovation #1). FM-001 (vanilla LLM-as-Judge bias, RPN=280) is the second-highest-priority failure mode. Debiasing is the direct mitigation. [ADR-001 L1 Forces F-5; ADR-001 L1 Risks FM-001; ADR-001 Implementation Roadmap Phase C; E-009]

**Parent:** STK-N-006

**Verification Method:** Test (run 20 evaluations of the same output pair; verify position order varies across runs; verify rubric criterion order varies across runs)

**Priority:** Must

**Layer:** Layer 2 (DeepEval evaluation backend)

**Status:** Draft

---

**FR-022**

**Title:** OSI-Approved License Verification for All Dependencies

**Description:** The system shall use only dependencies with OSI-approved open-source licenses. All production and development dependencies shall have their licenses verified and documented in a `LICENSES.md` file in the repository root.

**Acceptance Criteria:**
- All direct production dependencies shall have an OSI-approved license: promptfoo (MIT), DeepEval (Apache 2.0), scipy (BSD), statsmodels (BSD).
- No dependency with a proprietary, copyleft (GPL), or non-OSI-approved license shall be added without explicit engineering review and documentation of the license risk.
- A license verification check shall run in CI and fail if any dependency has an unverified or non-OSI license.

**Rationale:** OSI-approved licenses are a hard constraint per ADR-001 Constraints M-001 and ADR-002 Constraints. All four primary components have been verified as OSI-licensed. [ADR-001 L1 Constraints; E-013; ADR-001 L1 Consequences Neutral #2]

**Parent:** STK-N-001

**Verification Method:** Inspection (review LICENSES.md and dependency manifests); Test (CI license check passes)

**Priority:** Must

**Layer:** Cross-cutting (all layers)

**Status:** Draft

---

**FR-023**

**Title:** UV-Only Python Execution

**Description:** All Python code in the harness shall execute via `uv run` and all Python dependencies shall be managed via `uv add`. No direct invocations of `python`, `pip`, or `pip3` shall appear in any script, Makefile, GitHub Actions workflow, or documentation.

**Acceptance Criteria:**
- All GitHub Actions workflow steps that invoke Python shall use `uv run pytest` or `uv run python`.
- The `pyproject.toml` shall define all Python dependencies; no `requirements.txt` shall be used as the primary dependency file.
- The CI workflow shall fail if any Python invocation pattern matching `\bpython\b` or `\bpip\b` (not preceded by `uv run `) is detected in workflow YAML files.

**Rationale:** H-05 mandates UV-only Python execution. This is a Jerry framework-wide hard constraint that applies to all sub-projects including PROJ-036. [ADR-001 L1 Constraints; CLAUDE.md H-05; Jerry quality-enforcement.md]

**Parent:** STK-N-001

**Verification Method:** Inspection (grep all workflow YAML files and scripts for bare `python` or `pip` invocations; verify none found); Test (CI UV-check step passes)

**Priority:** Must

**Layer:** Cross-cutting (all layers)

**Status:** Draft

---

**FR-024**

**Title:** Langfuse Observability Integration (Optional)

**Description:** The system shall support optional integration with Langfuse for logging prompt versions, evaluation scores, and regression comparison results as trace data, enabling trend tracking across prompt versions over time.

**Acceptance Criteria:**
- Given Langfuse credentials configured as environment variables (`LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`), When an evaluation completes, Then the system shall log a trace to Langfuse containing: agent identifier, prompt version key, per-metric scores, and regression classification.
- When Langfuse credentials are not configured, the system shall continue evaluation without logging and shall not raise an error.
- Langfuse integration shall be documented as optional in the harness README and shall not be required for any core functional requirement.

**Rationale:** ADR-001 Architecture Diagram includes "Optional: Langfuse observability layer" for trend tracking. This addresses STK-N-009 (track regression trends over time) as a should-requirement consistent with its optional designation in the ADR. [ADR-001 L1 Technical Implementation, Architecture Diagram; ADR-001 L2 Architectural Implications]

**Parent:** STK-N-009

**Verification Method:** Demonstration (configure Langfuse credentials, execute evaluation, verify trace visible in Langfuse dashboard); Test (execute without credentials and verify no error raised)

**Priority:** Should

**Layer:** Cross-cutting (all layers)

**Status:** Draft

---

**FR-025**

**Title:** promptfoo Docker/GitHub Action Isolation from UV Environment

**Description:** The system shall run promptfoo via Docker image or GitHub Action, isolating the Node.js/TypeScript promptfoo runtime from the UV-only Python environment. No local `npm install` shall be required for CI execution.

**Acceptance Criteria:**
- The GitHub Actions workflow shall invoke promptfoo via the official `promptfoo/action` GitHub Action or a pinned Docker image, not via a locally installed npm package.
- The Python environment shall have no npm or Node.js dependencies in `pyproject.toml` or `uv.lock`.
- If Docker-based execution is used, the Docker image version shall be pinned in the workflow YAML.
- A fallback configuration using promptfoo's Python API client shall be documented for environments where Docker/GHA is not available, with explicit notation that this fallback does not include native PR status integration.

**Rationale:** FM-004 (promptfoo npm dependency conflicts with UV-only, RPN=90) requires mitigation via Docker/GitHub Action isolation. The fallback to the Python API client is documented in ADR-001 as compliant with M-003 via pytest exit code. [ADR-001 L1 Consequences Negative #2; ADR-001 L1 Risks FM-004; ADR-001 L1 Constraints H-05 impact]

**Parent:** STK-N-001

**Verification Method:** Inspection (verify no npm/Node.js entries in pyproject.toml or uv.lock); Demonstration (execute CI workflow and verify promptfoo runs via Action/Docker, not local npm)

**Priority:** Must

**Layer:** Layer 1 (promptfoo CI/CD gate)

**Status:** Draft

---

**FR-026**

**Title:** DeepEval Version Pinning with Re-Baseline Protocol

**Description:** The system shall pin the DeepEval package version in `uv.lock` and shall define a documented re-baseline protocol that is executed whenever the DeepEval version is updated.

**Acceptance Criteria:**
- The DeepEval version in `uv.lock` shall be a pinned exact version (e.g., `deepeval==1.5.2`), not a range constraint.
- A re-baseline runbook shall be documented at `tests/prompt-regression/runbooks/re-baseline-after-upgrade.md` specifying: (1) update DeepEval version, (2) run Full evaluation on all agents, (3) review score distribution shift, (4) update all baselines if shift is within expected bounds, (5) flag for human review if shift exceeds 0.05 per metric.
- The CI pipeline shall detect if DeepEval has been updated without a re-baseline and produce a warning annotation.

**Rationale:** FM-008 (DeepEval metric version drift changes score scale, RPN=60) is mitigated by version pinning and re-baseline protocol. A metric scale shift makes all prior baselines incomparable, producing false regressions or missed regressions. [ADR-001 L1 Risks FM-008; ADR-001 Implementation Roadmap Phase A]

**Parent:** STK-N-001

**Verification Method:** Inspection (verify deepeval version pinned in uv.lock; verify runbook document exists); Test (update DeepEval version without re-baseline and verify CI warning)

**Priority:** Must

**Layer:** Layer 2 (DeepEval evaluation backend)

**Status:** Draft

---

**FR-027**

**Title:** Test Case Authorship Requirement for Agent Definition PRs

**Description:** The system shall enforce, via PR checklist, that every pull request modifying an agent definition file includes corresponding test case authorship (new or updated test cases in `tests/prompt-regression/`) or provides an explicit documented justification for why no new test cases are needed.

**Acceptance Criteria:**
- The GitHub pull request template shall include a required checklist item: "[ ] I have added or updated regression test cases in `tests/prompt-regression/` for all modified agent definitions, OR documented why no new test cases are required."
- A CI check shall detect PRs that modify `skills/*/agents/*.md` without modifying `tests/prompt-regression/` and produce a warning annotation (not a blocking failure, to avoid over-enforcement for trivial changes).
- The CI warning shall link to the test case authorship guide.

**Rationale:** FM-007 (false confidence from incomplete test suite coverage, RPN=432) is the highest-priority failure mode and is structurally irreducible. The primary mitigation is requiring test case authorship alongside prompt authorship. This is a process requirement, not a technical one. [ADR-001 L1 Risks FM-007; ADR-001 Implementation Roadmap Phase F; ADR-001 L2 Systemic Consequences Pattern C]

**Parent:** STK-N-001

**Verification Method:** Demonstration (create a PR modifying an agent definition without updating test cases; verify CI warning annotation appears and links to guide)

**Priority:** Must

**Layer:** Cross-cutting (governance / process)

**Status:** Draft

---

**FR-028**

**Title:** Model Migration Comparison Mode

**Description:** The system shall support a model migration evaluation mode that runs the same prompt version against two different LLM providers (e.g., `claude-sonnet-4-20250514` vs. a new model version) and applies the same statistical comparison logic to detect behavioral differences between model versions.

**Acceptance Criteria:**
- Given two LLM provider identifiers and a prompt version, When model migration mode is invoked, Then the system shall run N=30 evaluations of the same prompt against both providers and apply Wilcoxon signed-rank comparison.
- The regression report in migration mode shall label the comparison as "MODEL MIGRATION COMPARISON: {provider_a} vs. {provider_b}" to distinguish it from prompt version regression.
- promptfoo's multi-provider support (100+ integrations) shall be used as the execution layer for model migration mode.

> **Consistency note:** FR-028 specifies N=30 runs for model migration mode. This matches Full mode (FR-005, N=30) because migration analysis requires the same statistical rigor as full regression testing. FR-028 is "Should" priority (migration mode is not required for the core PR regression gate) while Full mode (FR-005) is "Must" priority; the N=30 run count is not derived from FR-005 but independently specified for FR-028 based on the same statistical adequacy rationale. The N=30 run count for FR-028 and FR-005 are independently specified and may diverge if migration analysis requirements change independently of Full mode requirements.

**Rationale:** ADR-001 identifies model migration as the secondary use case: "When Anthropic releases new Claude model versions, all 67 agent definitions must be validated against the new model." Migration Confidence scored 5/5 for the Four-Layer Composite specifically because of multi-provider support. [ADR-001 L0 Why This Decision Matters; ADR-001 L1 Problem Statement #2; ADR-001 Options Evaluation Dimension Migration Confidence; E-004]

**Parent:** STK-N-002

**Verification Method:** Demonstration (run migration mode comparing two mock providers and verify labeled report output); Test (verify Wilcoxon comparison applied to cross-provider score arrays)

**Priority:** Should

**Layer:** Layer 1 (promptfoo CI/CD gate), Layer 4 (Statistical comparison engine)

**Status:** Draft

---

**FR-029**

**Title:** Regression Trend Persistence

**Description:** The system shall persist all evaluation results (version key, evaluation mode, per-metric scores, regression classification, timestamp) to a local artifact store in a format that enables trend analysis across prompt version history.

**Acceptance Criteria:**
- Each evaluation run shall produce a result record persisted to `tests/prompt-regression/history/{agent_id}/{YYYYMMDD-HHMMSS}-{version_key_short}.json`.
- Result records shall be committed to git as part of the evaluation workflow, creating a queryable history in the repository.
- A trend summary command (`jerry test trend {agent_id}`) shall display the last 10 regression classifications for an agent in chronological order.

**Rationale:** Trend tracking addresses STK-N-009 and ADR-001 L2 positive consequence: "Agent definition quality can be tracked over time via regression trend data." Persistent history also enables retrospective analysis of regression-introducing changes. [ADR-001 L2 Architectural Implications; ADR-001 L2 Future Flexibility]

**Parent:** STK-N-009

**Verification Method:** Inspection (verify result files created after evaluation with correct schema); Demonstration (run trend command and verify chronological display)

**Priority:** Should

**Layer:** Cross-cutting (all layers)

**Status:** Draft

---

**FR-030**

**Title:** Extensible Layer Architecture

**Description:** The system shall implement each layer as an independently deployable, independently testable module with a defined input/output contract, enabling new layers (e.g., PPI calibration as Phase E, perturbation testing as Phase F) to be added without modifying existing layers.

**Acceptance Criteria:**
- Each layer shall be implemented in a distinct Python module or package: `jerry/testing/layer1_promptfoo.py` (or configuration files), `jerry/testing/layer2_deepeval.py`, `jerry/testing/layer3_metamorphic.py`, `jerry/testing/layer4_stats.py` (orchestration), and `jerry/testing/stats.py` (shared statistical functions imported by `layer4_stats.py`).
- The inter-layer contract shall be the score array JSON format defined in FR-009; no layer shall pass raw LLM outputs directly to Layer 4.
- Adding a new layer shall require: (1) creating a new module implementing the layer contract, (2) registering the layer in the evaluation pipeline configuration, and (3) updating the regression report to include the new layer's output.
- No modification to existing layer modules shall be required to add a new layer.

**Rationale:** ADR-001 L2 Long-Term Evolution Path requires that the architecture accommodates Phases E-F (PPI calibration, perturbation testing) "without refactoring." The common score array interface is the mechanism enabling this extensibility. [ADR-001 L2 Long-Term Evolution Path; ADR-001 L1 Consequences Neutral #1; E-016; E-017]

**Parent:** STK-N-010

**Verification Method:** Inspection (verify layer modules exist at specified paths; verify no cross-layer raw output sharing); Demonstration (describe addition of a hypothetical Layer 5 and confirm no modifications to Layers 1-4 are needed)

**Priority:** Must

**Layer:** Cross-cutting (architecture)

**Status:** Draft

---

## L1: Non-Functional Requirements

---

**NFR-001**

**Title:** Evaluation Execution Latency — Smoke Mode

**Description:** The system shall complete Smoke mode evaluation (N=1, deterministic metrics only) for a single agent in under 60 seconds from trigger to CI status posted.

**Acceptance Criteria:**
- Given a Smoke mode evaluation trigger for a single agent, When the evaluation executes end-to-end from workflow trigger to CI status posted, Then the total elapsed wall-clock time shall be less than 60 seconds for P95 across 10 measured runs.

**Rationale:** Smoke mode is designed for "every PR; fast feedback" per the tiered evaluation table. A 60-second target allows Smoke to complete well within the GitHub Actions 6-minute standard job timeout, providing fast feedback without incurring LLM API cost. [ADR-001 L1 Technical Implementation, Tiered Evaluation Modes]

**Parent:** STK-N-008

**Verification Method:** Test (measure wall-clock time for Smoke evaluation on a representative agent; verify < 60 seconds for P95 across 10 runs)

**Priority:** Must

**Status:** Draft

---

**NFR-002**

**Title:** Evaluation Execution Latency — Standard Mode

**Description:** The system shall complete Standard mode evaluation (N=10, LLM-as-Judge metrics) for a single agent in under 15 minutes from trigger to CI status posted.

**Acceptance Criteria:**
- Given a Standard mode evaluation trigger for a single agent, When the evaluation executes end-to-end from workflow trigger to CI status posted, Then the total elapsed wall-clock time shall be less than 15 minutes for P95 across 5 measured runs.

**Rationale:** Standard mode runs on "PRs modifying agent definitions" and governs the Must-priority CI gate (FR-002). A Must-priority PR-blocking gate requires a Must-priority latency bound to be operationally viable; a "Should" latency bound would permit the gate to block indefinitely without a defined SLA, making the CI gate unfit for engineering practice. A 15-minute target keeps regression testing within acceptable PR feedback loop bounds without imposing excessive wait on engineers. [ADR-001 L1 Technical Implementation, Tiered Evaluation Modes; FR-002 CI gate latency dependency]

**Parent:** STK-N-008

**Verification Method:** Test (measure wall-clock time for Standard evaluation on a representative agent with LLM-as-Judge metrics; verify < 15 minutes for P95 across 5 runs)

**Priority:** Must

**Status:** Draft

---

**NFR-003**

**Title:** Statistical Engine Computation Time

**Description:** The `jerry/testing/stats.py` module shall complete Wilcoxon signed-rank computation, Wilson score interval computation, and Bonferroni correction for K=10 metrics and N=30 scores per metric in under 1 second.

**Acceptance Criteria:**
- Given K=10 metrics and N=30 score pairs per metric as input to `stats.py`, When the full computation pipeline (Wilcoxon + Wilson + Bonferroni) executes, Then the total wall-clock time shall be less than 1.0 second for each of 100 consecutive benchmark invocations.

**Rationale:** The statistical computation layer adds no LLM latency; it operates on pre-computed score arrays. Sub-second computation ensures the statistical layer adds negligible overhead to the overall evaluation time. [ADR-001 L1 Technical Implementation Layer 4]

> **Bonferroni k cross-reference:** The K=10 value used here is specific to this NFR's performance benchmark scope (Standard mode computation ceiling). This mode-specific k value applies only within this NFR's scope. The full evaluation suite uses k=13 per the behavioral contracts (contracts/behavioral-contracts.md Section D.3).

**Parent:** STK-N-001

**Verification Method:** Test (benchmark stats.py execution with K=10, N=30 inputs; assert execution time < 1.0 seconds for 100 iterations)

**Priority:** Must

**Status:** Draft

---

**NFR-004**

**Title:** Evaluation Cost Ceiling — Full Mode

**Description:** The cost of Full mode evaluation for a single agent (N=30 per version, all layers) shall not exceed USD $10.

**Acceptance Criteria:**
- Given Full mode evaluation parameters (N=30 per version, all active layers including LLM-as-Judge and metamorphic relation checks), When the expected cost is computed from the LLM provider's current pricing for a representative agent, Then the computed cost estimate shall be less than $10.

**Rationale:** FM-006 (LLM cost overrun, RPN=140) requires cost controls. ADR-001 estimates Full mode at "$5-8" for one agent. The $10 ceiling provides a 25% buffer above the upper estimate. [ADR-001 L1 Technical Implementation, Tiered Evaluation Modes; ADR-001 L1 Risks FM-006]

**Parent:** STK-N-008

**Verification Method:** Analysis (compute expected cost from LLM provider pricing for N=30 invocations of representative agents using G-Eval and metamorphic checks; verify estimate < $10)

**Priority:** Must

**Status:** Draft

---

**NFR-005**

**Title:** Harness Availability in CI Environment

**Description:** The harness shall be available for execution in the GitHub Actions environment without requiring any manual setup steps beyond what is defined in the GitHub Actions workflow file.

**Acceptance Criteria:**
- Given a pull request triggering the regression workflow on a GitHub Actions runner with no prior harness setup, When the workflow executes, Then the harness shall complete initialization and begin evaluation without any manual intervention or pre-configuration steps outside the workflow YAML file.
- Given a freshly provisioned GitHub Actions runner (ubuntu-latest), When the workflow executes the harness setup steps defined in the workflow YAML, Then all required dependencies (UV, Python packages, promptfoo via Action) shall be installed and the harness shall reach a ready state within the GitHub Actions job without requiring external manual steps.
- Given any contributor (not just the original harness author) submitting a PR that modifies agent definition files, When the regression workflow triggers on their PR, Then the harness shall execute successfully without requiring that contributor to perform any one-time manual configuration.

**Rationale:** A harness requiring manual setup steps would fail to execute on PRs from contributors who have not performed the setup, breaking the regression gate. This supports STK-N-003 (automated, reliable merge blocking). [ADR-001 L1 Constraints M-003]

**Parent:** STK-N-003

**Verification Method:** Demonstration (create a fresh GitHub Actions runner and execute the workflow without manual pre-configuration; verify harness executes successfully)

**Priority:** Must

**Status:** Draft

---

**NFR-006**

**Title:** False Positive Rate — Metamorphic Relations

**Description:** After calibration per FR-011, the five universal metamorphic relations (MR-001 through MR-005) shall produce a false positive rate (MR violation on an output that is actually correct) of no more than 15% when evaluated against a reference dataset of 100+ known-good agent outputs.

**Rationale:** The LLMORPH study (ASE 2025) validated metamorphic testing across 560,000 tests with an 8.6% false positive rate. The 15% ceiling allows for less-optimal calibration in practice while still making MR violations meaningful signals. ADR-001 FM-009 mitigation specifies "Calibrate MR tolerance against 100+ real output pairs." [ADR-001 L1 Technical Implementation Layer 3; E-010; ADR-001 L1 Risks FM-009]

**Parent:** STK-N-006

**Verification Method:** Test (execute all five MRs against a reference dataset of 100+ known-good outputs; compute false positive rate; verify <= 15%)

**Priority:** Must

**Status:** Draft

---

**NFR-007**

**Title:** Statistical Rigor — Type I Error Rate

**Description:** The Wilcoxon signed-rank comparison shall produce a Type I error rate (false regression alarm) not exceeding the configured alpha value when evaluated against N=30 pairs drawn from the same distribution.

**Acceptance Criteria:**
- Given 1000 independently drawn paired samples of N=30 scores per version, both samples drawn from the identical distribution (simulating a prompt change with no actual quality difference), When the `compare_versions()` function in `jerry/testing/stats.py` is invoked on each sample pair using the default alpha=0.05, Then the fraction of invocations returning classification `REGRESSION` (i.e., p < 0.05 AND mean_b < mean_a) shall be no greater than 0.05 ± 0.01 (i.e., <= 0.06).
- Given the same Monte Carlo simulation executed with alpha=0.01 (Bonferroni-corrected threshold for K=5 metrics), When the simulation runs 1000 trials with N=30 pairs from the same distribution, Then the fraction of REGRESSION classifications shall be no greater than 0.01 ± 0.005 (i.e., <= 0.015).
- The Monte Carlo validation shall be implemented as a parameterized pytest benchmark in `tests/prompt-regression/unit/test_stats_type1_error.py` and shall run as part of the harness validation suite prior to production deployment.

> **Bonferroni k cross-reference:** The K=5 value in the second acceptance criterion above applies only within this NFR's Type I error validation scope (a representative subset of metrics for Monte Carlo simulation). This mode-specific k value applies only within this NFR's scope. The full evaluation suite uses k=13 per the behavioral contracts (contracts/behavioral-contracts.md Section D.3).

**Rationale:** Statistical validity of the regression detection is the central value proposition of Layer 4. A harness that produces more false alarms than its alpha parameter promises is not trustworthy for merge blocking decisions. [ADR-001 L1 Forces F-2; E-011; ADR-001 Options Evaluation Dimension Statistical Rigor]

**Parent:** STK-N-006

**Verification Method:** Analysis (Monte Carlo simulation: draw 1000 paired samples of N=30 from same distribution; compute fraction of Wilcoxon tests returning p < 0.05; verify fraction <= 0.05 ± 0.01)

**Priority:** Must

**Status:** Draft

---

**NFR-008**

**Title:** Maintainability — Test Case File Naming Convention

**Description:** All test case YAML files shall follow the naming convention `{agent-id}-regression.yaml` (e.g., `ps-researcher-regression.yaml`) and shall be stored under `tests/prompt-regression/` with one file per agent.

**Rationale:** Consistent naming enables automated test case discovery, CI tooling to associate YAML files with agent definition files for coverage tracking (FR-013), and engineers to find test cases without directory enumeration. This naming convention aligns with the promptfoo test case definition format established in ADR-001 and with the behavioral property registry naming scheme (per-agent files at `tests/prompt-regression/contracts/{agent-id}.yaml`) to ensure consistent agent identifier usage across all test artifacts. [ADR-001 L1 Technical Implementation, Test Case Definition Format; ADR-001 L1 Decision Layer 1]

**Parent:** STK-N-001

**Verification Method:** Inspection (verify all test case files match naming convention; verify one-file-per-agent structure)

**Priority:** Should

**Status:** Draft

---

**NFR-009**

**Title:** Security — No Secrets in Test Case Definitions or Evaluation Logs

**Description:** The harness shall not persist API keys, authentication tokens, or other secrets in test case YAML files, evaluation result JSON files, or CI workflow logs. LLM provider credentials shall be referenced exclusively via environment variables or GitHub Actions secrets.

**Rationale:** Test case files and evaluation logs are committed to the git repository. Secrets in these artifacts constitute a critical security exposure. This implements the harness's contribution to P-022 (no deception about actions, including logging sensitive data). [Jerry P-022; Jerry quality-enforcement.md]

**Parent:** STK-N-001

**Verification Method:** Inspection (grep test YAML and result JSON files for patterns matching API key formats; verify all LLM credentials referenced via environment variable names, not values)

**Priority:** Must

**Status:** Draft

---

**NFR-010**

**Title:** Reproducibility — Deterministic Structural Assertions

**Description:** Deterministic structural assertions (FR-008) shall produce identical results on every invocation given the same input, with no dependence on random number generation, time, or external API calls.

**Rationale:** Deterministic assertions are the foundation of Smoke mode. If structural assertions produce non-deterministic results, they provide no reliable safety signal. This is required for the Smoke mode label "STRUCTURAL ONLY" to be meaningful. [ADR-001 L1 Technical Implementation, Tiered Evaluation Modes]

**Parent:** STK-N-006

**Verification Method:** Test (execute structural assertions on the same input 50 times; verify all results are identical)

**Priority:** Must

**Status:** Draft

---

**NFR-011**

**Title:** Test Coverage — Harness Implementation Code

**Description:** The harness's own Python implementation code (all modules under `jerry/testing/`) shall maintain >= 90% line coverage as measured by pytest-cov, consistent with Jerry's H-20 testing standard.

**Rationale:** H-20 mandates 90% line coverage for all Jerry code. The statistical engine and metamorphic relation framework are production-critical components; test coverage ensures their correctness is maintained during refactoring. [Jerry quality-enforcement.md H-20; CLAUDE.md]

**Parent:** STK-N-001

**Verification Method:** Test (run `uv run pytest --cov=jerry/testing --cov-report=term-missing tests/` and verify line coverage >= 90%)

**Priority:** Must

**Status:** Draft

---

**NFR-012**

**Title:** Extensibility — Layer Contract Stability

**Description:** The score array JSON schema defined in FR-009 shall not change in a breaking way (removing or renaming required fields) after the harness reaches production status (Phase B completion). Non-breaking additions (new optional fields) are permitted.

**Rationale:** ADR-001's layered architecture depends on stable inter-layer contracts. A breaking change to the score array format would require simultaneous updates to Layers 2, 3, and 4, violating the independent-deployability principle in FR-030. [ADR-001 L2 Long-Term Evolution Path; FR-030]

**Parent:** STK-N-010

**Verification Method:** Inspection (review any schema changes against the original FR-009 schema; verify no required fields removed or renamed)

**Priority:** Should

**Status:** Draft

---

**NFR-013**

**Title:** Usability — Baseline CLI Commands

**Description:** The harness shall expose CLI commands via the `jerry test` subcommand group for the following operations: `jerry test run {agent_id} --mode {smoke|standard|full}`, `jerry test baseline list`, `jerry test baseline audit`, `jerry test trend {agent_id}`.

**Rationale:** CLI access enables engineers to run evaluations locally for development and debugging without constructing GitHub Action invocations. This supports confident prompt iteration (STK-N-001) outside of the PR workflow. [ADR-001 L1 Consequences Positive #1; ADR-001 Implementation Roadmap Phase E]

**Parent:** STK-N-001

**Verification Method:** Demonstration (execute each CLI command and verify expected output; verify `--help` output for each command)

**Priority:** Should

**Status:** Draft

---

**NFR-014**

**Title:** Documentation — Inline Code Documentation

**Description:** All public functions and classes in `jerry/testing/` shall include type annotations and docstrings conforming to H-11 ("Public function signatures: type hints + docstrings REQUIRED"). Docstrings shall include: summary line, parameter descriptions, return value description, and raised exceptions.

**Rationale:** H-11 is a Jerry framework hard rule. The statistical engine and metamorphic relation framework will be shared across projects (FR-019); complete documentation is essential for correct use by engineers unfamiliar with the implementation. [Jerry quality-enforcement.md H-11; CLAUDE.md]

**Parent:** STK-N-001

**Verification Method:** Inspection (verify all public functions and classes in `jerry/testing/` have type annotations and docstrings meeting H-11 criteria)

**Priority:** Must

**Status:** Draft

---

**NFR-015**

**Title:** Portability — Local Development Without GitHub Actions

**Description:** The harness shall be executable in a local development environment (macOS, Linux) using only `uv run pytest` without requiring Docker or GitHub Actions. Local execution shall support Smoke and Standard modes; Full mode local execution is desirable but not required.

> **Windows exclusion:** Windows is explicitly excluded from this portability requirement. ADR-001 does not include a Windows constraint, and Windows is excluded here because: (1) the Jerry framework's primary development environment is macOS/Linux, (2) promptfoo's Docker/GHA isolation (FR-025) provides a Windows-compatible path for CI execution, and (3) adding Windows support would require cross-platform testing infrastructure not currently planned.

**Rationale:** Engineers need to run regression tests locally during prompt development, before pushing a PR. If local execution requires Docker or GHA, the feedback loop is too slow for iterative prompt work. [ADR-001 L1 Consequences Positive #1; STK-N-001]

**Parent:** STK-N-001

**Verification Method:** Demonstration (execute `uv run pytest tests/prompt-regression/ --mode smoke` on a developer macOS machine with no Docker installed; verify evaluation completes successfully)

**Priority:** Should

**Status:** Draft

---

## L1: Interface Specifications

### IF-001: Layer 1 → Layer 2 Interface (promptfoo → DeepEval)

**Contract Type:** Python assertion provider

**Protocol:** promptfoo calls a custom Python file specified in the `assert` block of the test YAML. The Python file implements a function that receives the raw LLM output as a string and returns a score.

**Data Format:**
```
Input:  { "output": str, "prompt": str, "vars": dict[str, str], "test_case_id": str }
Output: { "pass": bool, "score": float, "reason": str }
```

**Constraints:**
- The Python assertion provider shall be invokable via `uv run python tests/prompt-regression/metrics/{metric_name}.py`.
- Score shall be in [0.0, 1.0].
- The provider shall not maintain state between invocations (stateless per test case).

**ADR Source:** ADR-001 L1 Technical Implementation "Layer 1 + Layer 2 integration"; ADR-001 L1 Decision Layer 1 "custom Python assertion provider"

---

### IF-002: Layer 2 → Layer 3 Interface (DeepEval → Metamorphic Relations)

**Contract Type:** DeepEval `BaseMetric` plugin

**Protocol:** Metamorphic relations are implemented as classes inheriting from `deepeval.metrics.BaseMetric`. DeepEval invokes the `measure(test_case: LLMTestCase) -> float` method during metric evaluation. The MR class receives the original and transformed inputs from the `LLMTestCase`.

**Data Format:**
```python
class MRMetric(BaseMetric):
    def measure(self, test_case: LLMTestCase) -> float:
        # test_case.input: original user input
        # test_case.actual_output: LLM output for original input
        # test_case.additional_metadata["transformed_input"]: MR-transformed input
        # test_case.additional_metadata["transformed_output"]: LLM output for transformed input
        ...
        return 0.0 | 1.0  # violation | pass
```

**Constraints:**
- Transformed input and output shall be passed via `test_case.additional_metadata` to avoid modifying the LLMTestCase contract.
- The `measure()` method shall return 1.0 for pass and 0.0 for violation (inverted from "score" semantics to make violations explicit).

**ADR Source:** ADR-001 L1 Technical Implementation "Layer 2 + Layer 3 integration"; ADR-001 ParaphraseConsistencyMetric code example

---

### IF-003: Layer 2 → Layer 4 Interface (DeepEval Scores → Statistical Engine)

**Contract Type:** Score array JSON files

**Protocol:** After N evaluation runs, Layer 2 writes one JSON file per metric per prompt version to the results directory. Layer 4 reads these files for statistical comparison.

**Data Format:**
```json
{
  "schema_version": "1.0",
  "metric_id": "string (e.g., g_eval_l0_presence)",
  "version_key": "string (git_hash:file_path)",
  "evaluation_mode": "smoke | standard | full",
  "scores": [0.87, 0.92, 0.81, ...],
  "run_count": 30,
  "timestamp_utc": "ISO-8601",
  "agent_id": "string (e.g., ps-researcher)"
}
```

**Constraints:**
- The `scores` array length shall equal `run_count`.
- All score values shall be in [0.0, 1.0].
- The file path shall follow: `tests/prompt-regression/results/{agent_id}/{version_key_short}/{metric_id}.json`

**ADR Source:** ADR-001 L2 Long-Term Evolution Path "common data format: arrays of quality scores"; ADR-001 L1 Technical Implementation Layer 2 + Layer 4 integration

---

### IF-004: Layer 3 → Layer 4 Interface (MR Results → Statistical Engine)

**Contract Type:** MR result JSON (same schema as IF-003, score values are 0.0 or 1.0)

**Protocol:** MR results are represented as binary score arrays (0.0 = violation, 1.0 = pass) using the same JSON schema as IF-003. Layer 4 computes the Wilcoxon signed-rank test on MR pass rates between version A and version B.

**Data Format:** Same as IF-003, with `metric_id` prefixed with `mr_` (e.g., `mr_paraphrase_consistency`).

**Constraints:**
- MR score values shall be exactly 0.0 or 1.0 (binary, not continuous).
- MR result files shall be stored alongside DeepEval result files in the same results directory.

**ADR Source:** ADR-001 L1 Technical Implementation "Layer 2 + Layer 3 integration"; ADR-001 L2 Long-Term Evolution Path

---

### IF-005: Layer 1 ↔ Layer 4 Interface (CI/CD Gate → Regression Verdict)

**Contract Type:** Process exit code and structured report file

**Protocol:** Layer 4 produces a regression verdict that controls the CI/CD gate behavior. The verdict is communicated via (a) process exit code of the pytest run and (b) a structured report JSON.

**Data Format:**
```json
{
  "schema_version": "1.0",
  "agent_id": "string",
  "evaluation_mode": "smoke | standard | full",
  "version_a_key": "string",
  "version_b_key": "string",
  "overall_verdict": "NO_REGRESSION | MARGINAL | REGRESSION | STRUCTURAL_ONLY",
  "per_metric_results": [
    {
      "metric_id": "string",
      "wilcoxon_p_value": 0.032,
      "wilcoxon_statistic": 45.0,
      "classification": "NO_REGRESSION | MARGINAL | REGRESSION",
      "ci_a": [0.81, 0.95],
      "ci_b": [0.78, 0.93],
      "bonferroni_corrected_alpha": 0.01
    }
  ],
  "bonferroni_k": 5,
  "timestamp_utc": "ISO-8601"
}
```

**Exit Code Mapping:**
- `NO_REGRESSION` or `STRUCTURAL_ONLY`: exit 0 (CI passes)
- `MARGINAL`: exit 0 with warning annotation
- `REGRESSION`: exit 1 (CI fails, blocks merge)

**ADR Source:** ADR-001 Architecture Diagram "CI/CD Gate Decision"; ADR-001 L1 Constraints M-003

---

### IF-006: External Interface — GitHub Actions

**Contract:** The harness shall expose a GitHub Action invocable as follows in workflow YAML:

```yaml
- uses: promptfoo/action@v1
  with:
    config: tests/prompt-regression/promptfooconfig.yaml
    output-path: tests/prompt-regression/results/
```

Followed by a Python evaluation step:

```yaml
- name: Run statistical regression evaluation
  run: uv run pytest tests/prompt-regression/ --mode ${{ inputs.mode }}
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

**ADR Source:** ADR-001 L1 Decision Layer 1 "GitHub Action for PR-triggered regression testing"; E-004

---

### IF-007: External Interface — LLM Provider API

**Contract:** The harness shall invoke LLM providers exclusively via promptfoo's provider abstraction layer (for Layer 1) and DeepEval's evaluator abstraction layer (for Layer 2). Direct Anthropic API invocations in harness code are prohibited.

**Credentials:** Provider API keys shall be passed exclusively via environment variables (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`). No credentials shall appear in test YAML, Python code, or result JSON files.

**ADR Source:** ADR-001 L1 Decision provider table; ADR-001 Constraints OSI licenses; NFR-009

---

## L1: FMEA-Derived Requirements

The following table maps each failure mode from ADR-001 Phase 5 FMEA to the requirements that mitigate it.

| Failure Mode | S | O | D | RPN | Mitigating Requirements | Gap Remaining |
|---|---|---|---|---|---|---|
| FM-007: False confidence from incomplete test suite coverage | 9 | 6 | 8 | **432** | FR-027 (test case authorship PR checklist), FR-013 (MR coverage tracking) | Structurally irreducible per ADR-001; Phase F perturbation testing deferred |
| FM-001: Vanilla LLM-as-Judge bias invalidates comparison | 8 | 7 | 5 | **280** | FR-021 (position randomization + rubric shuffling, mandatory by default) | None; fully mitigated |
| FM-003: Incomplete metamorphic relation coverage | 8 | 5 | 6 | **240** | FR-012 (agent-specific MRs), FR-013 (MR coverage metric), FR-011 (calibration) | Coverage gap persists until all agent types have specific MRs; ongoing process |
| FM-002: Statistical false alarm from small evaluation sets | 7 | 6 | 4 | **168** | FR-014 (N >= 20 enforcement), FR-005 (Smoke mode labeled non-statistical), NFR-007 (Type I error rate) | None; fully mitigated |
| FM-005: Prompt version mismatch in baseline store | 9 | 4 | 4 | **144** | FR-004 (git commit hash composite key), FR-020 (baseline acceptance check) | None; fully mitigated |
| FM-010: Stale baseline captures known-poor prompt version | 8 | 3 | 6 | **144** | FR-020 (baseline quality gate >= 0.92 before acceptance) | None; fully mitigated |
| FM-006: LLM cost overrun from multi-sample statistical engine | 7 | 5 | 4 | **140** | FR-005 (tiered evaluation modes), NFR-004 (cost ceiling $10/Full) | None; fully mitigated |
| FM-009: Metamorphic relation violation is ambiguous | 5 | 5 | 5 | **125** | FR-011 (calibration against 100+ pairs), FR-010 (MRs as warnings until calibrated) | None; mitigated post-calibration |
| FM-004: promptfoo npm dependency conflicts with UV-only | 6 | 5 | 3 | **90** | FR-025 (Docker/GHA isolation; Python API fallback documented), FR-023 (UV-only enforcement) | Fallback path lacks native PR status integration; acceptable per ADR |
| FM-008: DeepEval metric version drift changes score scale | 5 | 4 | 3 | **60** | FR-026 (version pinning + re-baseline runbook) | None; fully mitigated |

---

## L1: Requirements Quality Checklist

| Quality Criterion | Status | Evidence |
|---|---|---|
| **Complete:** All 4 architectural layers have functional requirements | PASS | FR-001 through FR-005 (L1), FR-006 through FR-009 (L2), FR-010 through FR-013 (L3), FR-014 through FR-020 (L4) |
| **Complete:** All 10 FMEA failure modes addressed by at least one requirement | PASS | FMEA-Derived Requirements table above |
| **Complete:** All 10 stakeholder needs (STK-N-001 through STK-N-010) addressed | PASS | Each STK-N maps to at least one FR or NFR via Parent field |
| **Complete:** Interface specifications for all 7 interfaces | PASS | IF-001 through IF-007 defined |
| **Complete:** Behavioral property registry format specified for FR-013 | PASS | FR-013 includes registry specification block with file format, path, and content structure |
| **Consistent:** Module naming resolved — `stats.py` vs `layer4_stats.py` | PASS | FR-019 Module Architecture Note explicitly defines both modules and their dependency relationship; FR-030 and allocation table updated accordingly |
| **Consistent:** NFR-002 priority consistent with FR-002 CI gate | PASS | NFR-002 escalated to Must; rationale updated to reference FR-002 dependency |
| **Consistent:** No conflicting requirements identified | PASS | FR-005 (tiered modes) resolves potential conflict between FR-014 (N >= 20) and practical use; Smoke mode explicitly carved out; FR-028 N=30 documented as independent specification |
| **Consistent:** FR-023 (UV-only) consistent with H-05; FR-011 consistent with H-20 | PASS | All H-rule citations verified against quality-enforcement.md |
| **Verifiable:** All requirements have assigned verification methods (A/D/I/T) | PASS | Each FR and NFR has Verification Method field |
| **Verifiable:** All NFRs have quantitative thresholds where applicable | PASS | NFR-001 (60s), NFR-002 (15min), NFR-003 (1s), NFR-004 ($10), NFR-006 (15%), NFR-007 (alpha), NFR-011 (90%) |
| **Verifiable:** Must-priority NFRs use Given/When/Then acceptance criteria | PASS | NFR-001, NFR-002, NFR-003, NFR-004 have G/W/T acceptance criteria (Iteration 2); NFR-005, NFR-007 have G/W/T acceptance criteria (Iteration 3) |
| **Traceable:** All requirements trace to ADR-001 sections or evidence entries | PASS | Each requirement Rationale cites specific ADR-001 section or E-XXX evidence entry |
| **Traceable:** FR-012 present in FMEA reverse trace table | PASS | FR-012 row added to reverse trace table under FM-003 in Iteration 2 |
| **Traceable:** IF-005 ADR Source references external ADR-001 section | PASS | IF-005 ADR Source updated from self-referential to ADR-001 L1 Constraints M-003 |
| **Unambiguous:** "Shall" statements use concrete verbs and measurable constraints | PASS | Reviewed for passive constructions and vague descriptors |
| **Necessary:** All requirements serve a purpose derivable from ADR-001 | PASS | FM-007 requirements retained despite irreducibility; structural necessity confirmed |
| **FMEA coverage:** All failure modes addressed | PASS | See FMEA table above; FM-007 gap explicitly documented |

---

## L2: Systems Perspective

### Allocation Matrix

| Requirement | Allocated To | Interface | Notes |
|---|---|---|---|
| FR-001 | promptfoo YAML + tests/prompt-regression/ | IF-006 (GHA) | Test case authorship is engineer responsibility |
| FR-002 | GitHub Actions workflow | IF-006 (GHA) | Workflow triggers on `skills/*/agents/*.md` path filter |
| FR-003 | promptfoo + LLM provider | IF-007 (LLM API) | promptfoo manages provider invocation |
| FR-004 | Baseline artifact store module | IF-003 (score arrays) | Store at `tests/prompt-regression/baselines/` |
| FR-005 | Layer 1 CLI + GitHub Action input | IF-005 (CI verdict) | Mode propagated through all layers |
| FR-006 | DeepEval + pyproject.toml | IF-001 (promptfoo→DeepEval) | `uv add deepeval` integration |
| FR-007 | `tests/prompt-regression/criteria/` + DeepEval | IF-001 | Criteria stored as YAML per agent |
| FR-008 | `jerry/testing/layer2_deepeval.py` | IF-001 | Stateless assertion functions |
| FR-009 | `jerry/testing/layer2_deepeval.py` | IF-003 (score arrays) | JSON schema versioned |
| FR-010 | `jerry/testing/layer3_metamorphic.py` | IF-002 (DeepEval→MR) | Five MR classes |
| FR-011 | `jerry/testing/layer3_metamorphic.py` + `tests/prompt-regression/mr-config.yaml` | IF-002 | Calibration utility separate from MR execution |
| FR-012 | `tests/prompt-regression/mr/` (per-agent definitions) | IF-002 | One subdirectory per agent type |
| FR-013 | `jerry/testing/layer3_metamorphic.py` | IF-004 (MR→stats) | Coverage computed against behavioral property registry at `tests/prompt-regression/contracts/` |
| FR-014 | `jerry/testing/stats.py` | IF-003 | `InsufficientSamplesError` in shared module |
| FR-015 | `jerry/testing/stats.py` | IF-003, IF-005 | `compare_versions()` primary function |
| FR-016 | `jerry/testing/stats.py` | IF-003, IF-005 | `wilson_score_intervals()` function |
| FR-017 | `jerry/testing/stats.py` | IF-005 | Bonferroni applied within `compare_versions()` |
| FR-018 | `jerry/testing/layer4_stats.py` + GHA integration | IF-005 | Report format and GitHub status API calls; imports statistical functions from `jerry/testing/stats.py` |
| FR-019 | `jerry/testing/stats.py` (shared functions) + `jerry/testing/layer4_stats.py` (orchestration) | IF-003 | `stats.py` is the shared module with no project-specific imports; `layer4_stats.py` orchestrates the pipeline |
| FR-020 | Baseline store module | IF-003, IF-005 | Baseline acceptance separate from regression comparison |
| FR-021 | `jerry/testing/layer2_deepeval.py` | IF-001 | Debiasing wrapper around DeepEval G-Eval |
| FR-022 | `pyproject.toml` + CI license check | IF-006 | `uv` lock file verification |
| FR-023 | All workflow YAML + CI UV-check | IF-006 | Grep-based CI enforcement |
| FR-024 | Optional Langfuse SDK integration | External | Environment-variable gated |
| FR-025 | GitHub Actions workflow YAML | IF-006 | promptfoo/action version pinned |
| FR-026 | `pyproject.toml` + `uv.lock` + runbook | IF-006 | Version constraint and documentation |
| FR-027 | PR template + CI path check | IF-006 | Warning annotation, not block |
| FR-028 | `jerry/testing/layer1_promptfoo.py` + `jerry/testing/stats.py` | IF-007, IF-003 | Two-provider promptfoo config; Wilcoxon comparison via stats.py |
| FR-029 | `tests/prompt-regression/history/` | IF-005 | Git-committed result history |
| FR-030 | Package structure in `jerry/testing/` | All IFs | One module per layer; `stats.py` is shared; `layer4_stats.py` imports from `stats.py` |

### Risk Implications

| Requirement | Risk | Likelihood x Impact | Mitigation |
|---|---|---|---|
| FR-010 (5 universal MRs) | MR calibration takes longer than planned | L(3) x I(3) = 9 | Start with warnings-only mode per FR-010; production block deferred until calibrated |
| FR-027 (test case authorship) | Process compliance not enforced by engineers | L(4) x I(4) = 16 | Warning annotation is visible; consider adding to merge protection rules in Phase D |
| FR-019 (shared stats module) | PROJ-017 and PROJ-036 evolve incompatible requirements for stats.py | L(2) x I(4) = 8 | Define stable public API per FR-030; coordinate with PROJ-017 team before breaking changes |
| FM-007 residual | Test suite coverage gap leaves undetected regressions | L(5) x I(4) = 20 | Structurally irreducible; accepted risk per ADR-001; Phase F perturbation testing partially mitigates |
| NFR-004 (cost ceiling) | Full mode cost exceeds $10 for complex agents | L(2) x I(3) = 6 | Monitor per-agent cost in Phase B; apply per-metric run caps if needed |

### Traceability Strategy

The traceability chain for this harness is:

```
Stakeholder Needs (STK-N-001 through STK-N-010)
    └── ADR-001 Forces and Evidence (E-001 through E-022)
        └── Functional Requirements (FR-001 through FR-030)
        └── Non-Functional Requirements (NFR-001 through NFR-015)
        └── Interface Specifications (IF-001 through IF-007)
            └── Implementation Phases (Phase A through F)
                └── Verification Evidence (Test/Demo/Inspection results)
```

Bidirectional traceability is maintained via:
- Forward: Each FR cites its Parent (STK-N) and ADR Source
- Backward: The Traceability Matrix below maps ADR evidence entries to requirements
- FMEA: Each failure mode maps to at least one mitigating requirement

---

## Traceability Matrix

### ADR-001 Evidence to Requirements

| Evidence ID | ADR Source | Content Summary | Requirements Derived |
|---|---|---|---|
| E-001 | Phase 1A: Oracle Problem + Non-Determinism Gap | LLM outputs are non-deterministic; no ground truth oracle exists for evaluating them | FR-010, FR-011, FR-014, NFR-007 |
| E-002 | Phase 1A: Metamorphic Testing HIGHEST applicability | Metamorphic testing rated highest applicability for oracle-free LLM evaluation across 5 techniques studied | FR-010, FR-012 |
| E-003 | Phase 1B: Statistical rigor row: all LOW | All 7 evaluated SDKs scored LOW on statistical rigor — none apply hypothesis testing to regression detection | FR-015, FR-017, NFR-007 |
| E-004 | Phase 1B: promptfoo purpose-built for regression | promptfoo is "purpose-built for this exact use case" among 7 SDKs; only one with native YAML test case format | FR-001, FR-002, FR-003, FR-025, FR-028 |
| E-005 | Phase 1B: DeepEval pytest-native, 14+ metrics | DeepEval integrates natively with pytest and provides 14+ evaluation metrics out of the box | FR-006, FR-007, FR-008 |
| E-006 | Phase 1B: hybrid approach architecturally viable | Research validated that combining promptfoo + DeepEval + custom statistical layer is architecturally viable | FR-030 |
| E-007 | Phase 1C: No SDK provides prompt regression testing | Gap analysis: zero of 7 SDKs provide before/after prompt version comparison; this is the novel harness contribution | FR-003, FR-018 |
| E-008 | Phase 1C: Five gaps the harness addresses | The five identified gaps in existing SDKs that justify building a custom harness | FR-001, FR-004, FR-010, FR-021, FR-027 |
| E-009 | Phase 1D: Innovation #1 — debiasing, 80-87% correlation | Debiased LLM-as-Judge achieves 80-87% human correlation; position bias and rubric order bias are primary sources of error | FR-021 |
| E-010 | Phase 1D: Innovation #2 — LLMORPH 8.6% false positive | LLMORPH study (ASE 2025): 560,000 metamorphic tests, 8.6% false positive rate; validates practical viability | FR-010, NFR-006 |
| E-011 | Phase 1D: Innovation #6 — CLT very poorly, ICML 2025 | ICML 2025 consensus: CLT-based methods perform "very poorly" for small N; non-parametric tests required | FR-014, FR-015, FR-016, NFR-007 |
| E-012 | Phase 1D: Innovation #3 — PPI valid intervals | Prediction-Powered Inference (PPI) provides valid confidence intervals using LLM annotations + small human-labeled set; deferred to Phase E because Phase A-D can achieve statistical validity with Wilcoxon alone and PPI requires a human-labeled calibration dataset not yet available | (Phase E; deferred; architecture extensibility via FR-030) |
| E-013 | Phase 1D: Innovation #8 — License verification | All four primary components (promptfoo MIT, DeepEval Apache 2.0, scipy BSD, statsmodels BSD) have verified OSI-approved licenses | FR-022 |
| E-014 | Phase 1D: Innovation #11 — Perturbation testing | Perturbation testing is a complementary technique to metamorphic testing; deferred to Phase F as it requires additional infrastructure not needed for core regression detection | FR-027 (process mitigation); FR-013 (coverage tracking) |
| E-015 | Phase 3: PAT-001 through PAT-006 convergence | Six cross-framework patterns identified: PAT-001 oracle-free testing, PAT-002 pytest convergence point, PAT-003 debiasing, PAT-004 PR automation | FR-006 (PAT-002), FR-021 (PAT-003), FR-002 (PAT-004) |
| E-016 | Phase 3: Four-Layer Architecture derivation | The four-layer composite architecture was derived from convergence of PAT-001 through PAT-006; each layer addresses one or more identified patterns | FR-030, IF-001 through IF-004 |
| E-017 | Phase 3: Component Selection Justification | Justification for promptfoo, DeepEval, scipy/statsmodels, and shared stats module as the four components implementing the four layers | FR-001, FR-006, FR-010, FR-015, FR-019 |
| E-018 | Phase 5: Comparative Matrix scoring | The comparative evaluation matrix scored the Four-Layer Composite highest across all dimensions (Statistical Rigor 5/5, Refactoring Safety 5/5, Migration Confidence 5/5) | FR-015, FR-017, NFR-007 |
| E-019 | Phase 5: FMEA 10 failure modes | Ten failure modes identified with RPN scores; FM-007 highest (432), FM-001 second (280), FM-003 third (240) | FR-004 (FM-005), FR-005 (FM-002,FM-006), FR-010 (FM-009), FR-011 (FM-009), FR-013 (FM-003), FR-014 (FM-002), FR-020 (FM-010), FR-021 (FM-001), FR-025 (FM-004), FR-026 (FM-008), FR-027 (FM-007) |
| E-020 | Phase 5: PROJ-017 ADR-002 relationship | PROJ-017 (skill evaluation framework) shares the same statistical infrastructure need; `jerry/testing/stats.py` serves both projects | FR-019, IF-003 |
| E-021 | PROJ-017 ADR-002: Shared infrastructure | ADR-002 explicitly identifies the shared statistical module as a positive architectural consequence of the composite approach | FR-019 |
| E-022 | ADR-001 Weight Justification | Evaluation dimension weights: Statistical Rigor 0.20, Refactoring Safety 0.25, Migration Confidence 0.15; justification for weight assignments | FR-015 (Statistical Rigor 0.20), FR-010 (Refactoring Safety 0.25), FR-028 (Migration Confidence 0.15) |

### Stakeholder Needs to Requirements

| STK-N | Stakeholder Need | Primary Requirements | Secondary Requirements |
|---|---|---|---|
| STK-N-001 | Know whether a prompt change caused regression | Primary: FR-003, FR-015, FR-018 | Secondary: FR-001, FR-002, FR-006, FR-007, FR-008, FR-009, FR-019, FR-020, FR-022, FR-023, FR-026, NFR-005, NFR-009, NFR-011, NFR-013, NFR-014, NFR-015 |
| STK-N-002 | Validate all 67 agents against new model versions | FR-028 | — |
| STK-N-003 | Block merge on statistically significant regression | FR-002, FR-018 | NFR-005 |
| STK-N-004 | Receive regression reports with confidence intervals | FR-016, FR-018 | FR-013, FR-017 |
| STK-N-005 | Assert behavioral consistency without oracle | FR-010, FR-011, FR-012 | FR-013 |
| STK-N-006 | Evaluate without false alarms from LLM variance | FR-014, FR-015, FR-021 | FR-003, FR-008, NFR-006, NFR-007, NFR-010 |
| STK-N-007 | Trigger testing automatically on agent definition PRs | FR-002 | — |
| STK-N-008 | Evaluate at different cost/thoroughness trade-offs | FR-005 | NFR-001, NFR-002, NFR-004 |
| STK-N-009 | Track regression trends over time | FR-029 | FR-024 |
| STK-N-010 | Add new evaluation layers without refactoring existing | FR-030 | NFR-012 |

### ADR-001 Architectural Layers to Requirements

| Layer | Layer Name | Functional Requirements |
|---|---|---|
| Layer 1 | promptfoo CI/CD gate | FR-001, FR-002, FR-003, FR-004, FR-005, FR-018, FR-025 |
| Layer 2 | DeepEval evaluation backend | FR-006, FR-007, FR-008, FR-009, FR-021, FR-026 |
| Layer 3 | Metamorphic Relation Framework | FR-010, FR-011, FR-012, FR-013 |
| Layer 4 | Statistical comparison engine | FR-014, FR-015, FR-016, FR-017, FR-018, FR-019, FR-020 |
| Cross-cutting | Architecture, governance, observability | FR-022, FR-023, FR-024, FR-027, FR-028, FR-029, FR-030 |

### FMEA Failure Modes to Requirements (Reverse Trace)

| Requirement | Mitigates Failure Mode(s) |
|---|---|
| FR-004 | FM-005 (version mismatch) |
| FR-005 | FM-002 (small N false alarms); FM-006 (cost overrun) |
| FR-010 | FM-009 (MR violations warnings-only until calibrated) |
| FR-011 | FM-009 (MR calibration) |
| FR-012 | FM-003 (incomplete MR coverage — agent-specific MRs narrow the coverage gap) |
| FR-013 | FM-003 (MR coverage gap visibility) |
| FR-014 | FM-002 (N >= 20 enforcement) |
| FR-020 | FM-010 (baseline quality gate) |
| FR-021 | FM-001 (LLM-as-Judge debiasing) |
| FR-025 | FM-004 (promptfoo npm isolation) |
| FR-026 | FM-008 (DeepEval version drift) |
| FR-027 | FM-007 (test coverage process enforcement) |

---

## Appendix A: Phase-to-Requirements Map

The following table maps each functional and non-functional requirement to its target delivery phase from the ADR-001 six-phase implementation roadmap. Engineers picking up a specific phase can use this table to identify in-scope requirements without scanning all 45+ requirements.

| Phase | Description | Functional Requirements | Non-Functional Requirements |
|-------|-------------|------------------------|-----------------------------|
| **Phase A** | Core Layer 1 + Layer 4 (CI gate + statistical engine) | FR-001, FR-002, FR-003, FR-004, FR-005, FR-014, FR-015, FR-016, FR-017, FR-018, FR-019, FR-022, FR-023, FR-025, FR-026 | NFR-001, NFR-002, NFR-003, NFR-004, NFR-005, NFR-009, NFR-011, NFR-014 |
| **Phase B** | Layer 2 integration (DeepEval + G-Eval + deterministic assertions) | FR-006, FR-007, FR-008, FR-009, FR-020, FR-021 | NFR-006, NFR-010, NFR-012 |
| **Phase C** | LLM-as-Judge debiasing (position randomization + rubric shuffling) | FR-021 (if not completed in Phase B) | NFR-006 |
| **Phase D** | Layer 3 (metamorphic relations + agent-specific MRs + coverage tracking) | FR-010, FR-011, FR-012, FR-013 | NFR-006, NFR-007 |
| **Phase E** | Baseline management + CLI + trend persistence | FR-020 (if deferred), FR-024, FR-029 | NFR-013 |
| **Phase F** | Process governance + perturbation testing (process requirement) | FR-027, FR-028 | NFR-015 |
| **Cross-phase** | Architecture requirements applicable throughout | FR-030 | NFR-008, NFR-011 |

> **Phase scope notes:**
> - FR-021 (LLM debiasing) is listed in both Phase B and Phase C per ADR-001; it should be completed no later than Phase C when G-Eval is production-ready.
> - NFR-002 (Standard mode latency, Must-priority) becomes measurable once Phase A + Phase B are complete and LLM-as-Judge metrics are active.
> - NFR-011 (90% test coverage) applies throughout all phases; it should be maintained from Phase A onward, not deferred to a later phase.

---

## Appendix B: Verification Artifact Map

The following table provides a forward trace from each functional and non-functional requirement to its planned verification artifact location in the `tests/prompt-regression/` directory structure. Engineers implementing a requirement can use this table to locate or create the appropriate test file without consulting ADR-001.

> **Conventions:** `unit/` contains isolated unit tests with no LLM API calls. `integration/` contains tests requiring GitHub Actions or live LLM providers. `benchmark/` contains performance and statistical validation tests. `validation/` contains inspection and demonstration scripts for CI-stage verification.

### Functional Requirements — Verification Artifact Map

| Requirement ID | Verification Method | Planned Test / Verification Location |
|---------------|--------------------|------------------------------------|
| FR-001 | Inspection, Demonstration | `tests/prompt-regression/validation/test_yaml_schema_conformance.py` |
| FR-002 | Demonstration | `tests/prompt-regression/integration/test_github_actions_trigger.py` |
| FR-003 | Test | `tests/prompt-regression/unit/test_version_comparison_execution.py` |
| FR-004 | Test | `tests/prompt-regression/unit/test_version_keys.py` |
| FR-005 | Test | `tests/prompt-regression/unit/test_evaluation_modes.py` |
| FR-006 | Demonstration | `tests/prompt-regression/integration/test_deepeval_pytest_plugin.py` |
| FR-007 | Test | `tests/prompt-regression/unit/test_geval_criteria.py` |
| FR-008 | Test | `tests/prompt-regression/unit/test_deterministic_assertions.py` |
| FR-009 | Inspection, Test | `tests/prompt-regression/unit/test_score_array_schema.py` |
| FR-010 | Test | `tests/prompt-regression/unit/test_metamorphic_relations.py` |
| FR-011 | Test | `tests/prompt-regression/unit/test_mr_calibration.py` |
| FR-012 | Inspection, Demonstration | `tests/prompt-regression/unit/test_agent_specific_mr.py` |
| FR-013 | Test | `tests/prompt-regression/unit/test_mr_coverage_metric.py` |
| FR-014 | Test | `tests/prompt-regression/unit/test_stats_sample_enforcement.py` |
| FR-015 | Test | `tests/prompt-regression/unit/test_stats_wilcoxon.py` |
| FR-016 | Test | `tests/prompt-regression/unit/test_stats_wilson_intervals.py` |
| FR-017 | Test | `tests/prompt-regression/unit/test_stats_bonferroni.py` |
| FR-018 | Demonstration | `tests/prompt-regression/integration/test_ci_gate.py` |
| FR-019 | Inspection, Test | `tests/prompt-regression/unit/test_stats_module_exports.py` |
| FR-020 | Test | `tests/prompt-regression/unit/test_baseline_store.py` |
| FR-021 | Test | `tests/prompt-regression/unit/test_debiasing.py` |
| FR-022 | Inspection, Test | `tests/prompt-regression/validation/test_license_check.py` |
| FR-023 | Inspection, Test | `tests/prompt-regression/validation/test_uv_only_enforcement.py` |
| FR-024 | Demonstration, Test | `tests/prompt-regression/integration/test_langfuse_optional.py` |
| FR-025 | Inspection, Demonstration | `tests/prompt-regression/integration/test_promptfoo_isolation.py` |
| FR-026 | Inspection, Test | `tests/prompt-regression/validation/test_deepeval_version_pin.py` |
| FR-027 | Demonstration | `tests/prompt-regression/integration/test_pr_checklist_warning.py` |
| FR-028 | Demonstration, Test | `tests/prompt-regression/integration/test_model_migration_mode.py` |
| FR-029 | Inspection, Demonstration | `tests/prompt-regression/unit/test_regression_trend_persistence.py` |
| FR-030 | Inspection, Demonstration | `tests/prompt-regression/validation/test_layer_architecture.py` |

### Non-Functional Requirements — Verification Artifact Map

| Requirement ID | Verification Method | Planned Test / Verification Location |
|---------------|--------------------|------------------------------------|
| NFR-001 | Test | `tests/prompt-regression/benchmark/test_smoke_mode_latency.py` |
| NFR-002 | Test | `tests/prompt-regression/benchmark/test_standard_mode_latency.py` |
| NFR-003 | Test | `tests/prompt-regression/benchmark/test_stats_computation_time.py` |
| NFR-004 | Analysis | `tests/prompt-regression/validation/cost_estimate_full_mode.py` |
| NFR-005 | Demonstration | `tests/prompt-regression/integration/test_ci_availability.py` |
| NFR-006 | Test | `tests/prompt-regression/benchmark/test_mr_false_positive_rate.py` |
| NFR-007 | Analysis | `tests/prompt-regression/unit/test_stats_type1_error.py` |
| NFR-008 | Inspection | `tests/prompt-regression/validation/test_naming_convention.py` |
| NFR-009 | Inspection | `tests/prompt-regression/validation/test_secrets_scan.py` |
| NFR-010 | Test | `tests/prompt-regression/unit/test_deterministic_reproducibility.py` |
| NFR-011 | Test | `tests/prompt-regression/unit/` (coverage collected via `--cov=jerry/testing`) |
| NFR-012 | Inspection | `tests/prompt-regression/validation/test_layer_contract_stability.py` |
| NFR-013 | Demonstration | `tests/prompt-regression/integration/test_cli_commands.py` |
| NFR-014 | Inspection | `tests/prompt-regression/validation/test_docstring_coverage.py` |
| NFR-015 | Demonstration | `tests/prompt-regression/integration/test_local_execution.py` |

---

## Self-Review (S-010)

Applied per H-15 before finalization. Iteration 3 review — addresses two targeted findings from iter2 adv-scorer report (NFR-005/NFR-007 G/W/T gap and missing Appendix B).

**Iteration 3 Fixes Verified:**

- [x] NFR-005 G/W/T RESOLVED: NFR-005 ("Harness Availability in CI Environment") now includes three Given/When/Then acceptance criteria covering: (1) fresh runner execution without manual intervention, (2) dependency installation within workflow YAML scope, and (3) any contributor (not just harness author) triggering successful execution. The criteria are consistent with the Demonstration verification method and the NFR description.

- [x] NFR-007 G/W/T RESOLVED: NFR-007 ("Statistical Rigor — Type I Error Rate") now includes three Given/When/Then acceptance criteria: (1) Monte Carlo simulation at alpha=0.05 with <= 0.06 REGRESSION fraction, (2) Monte Carlo at Bonferroni-corrected alpha=0.01 with <= 0.015 REGRESSION fraction, and (3) a planned test artifact location (`tests/prompt-regression/unit/test_stats_type1_error.py`) enabling implementation without external reference. The prior acceptance criteria block embedded the Monte Carlo description without G/W/T structure; it is now fully structured.

- [x] APPENDIX B RESOLVED: "Appendix B: Verification Artifact Map" added after Appendix A. The map provides a forward trace from all 30 FRs and all 15 NFRs to planned test file locations in the `tests/prompt-regression/` directory structure. Directory conventions (unit/, integration/, benchmark/, validation/) are documented in the Appendix B preamble. Document Sections navigation table updated to include the Appendix B anchor link.

**Iteration 2 Fixes Verified (all carry forward from iter2):**

- [x] FINDING-1 RESOLVED: FR-019 now includes explicit Module Architecture Note distinguishing `jerry/testing/stats.py` (shared statistical functions) from `jerry/testing/layer4_stats.py` (pipeline orchestration). FR-030 updated to list both modules. Allocation table rows FR-018 and FR-019 updated with consistent, non-conflicting descriptions. The dependency direction (`layer4_stats.py` imports from `stats.py`) is explicitly stated in three locations: FR-019 acceptance criteria, FR-019 rationale, and the FR-030 allocation table row.

- [x] FINDING-2 RESOLVED: NFR-002 priority escalated from "Should" to "Must". Rationale updated to explicitly reference the FR-002 dependency: "A Must-priority PR-blocking gate requires a Must-priority latency bound to be operationally viable." Acceptance criteria updated with Given/When/Then structure consistent with Must-priority NFRs.

- [x] FINDING-3 RESOLVED: FR-012 row added to FMEA Reverse Trace table with description "FM-003 (incomplete MR coverage — agent-specific MRs narrow the coverage gap)". FR-012 now has complete bidirectional traceability: forward (FMEA table maps FM-003 to FR-012), backward (reverse trace maps FR-012 to FM-003).

- [x] FINDING-4 RESOLVED: FR-013 now includes a "Behavioral Property Registry Specification" block defining the registry location (`tests/prompt-regression/contracts/{agent-id}.yaml`), file format (YAML array of named properties with descriptions), and the relationship to Stream 1D deliverables (`contracts/behavioral-contracts.md`). FR-013 is now implementable without consulting external documents.

- [x] FINDING-5 RESOLVED: IF-005 ADR Source updated from self-referential "ADR-001 FR-018 (from this document)" to "ADR-001 Architecture Diagram 'CI/CD Gate Decision'; ADR-001 L1 Constraints M-003". The ADR source now references two authoritative external sections, not a requirement from this document.

**Completeness:**
- [x] All four ADR-001 architectural layers covered: Layer 1 (FR-001 through FR-005, FR-025), Layer 2 (FR-006 through FR-009, FR-021, FR-026), Layer 3 (FR-010 through FR-013), Layer 4 (FR-014 through FR-020)
- [x] All 10 FMEA failure modes (FM-001 through FM-010) addressed by at least one requirement
- [x] All 10 stakeholder needs (STK-N-001 through STK-N-010) traced to at least one FR or NFR
- [x] All 7 interface specifications (IF-001 through IF-007) defined
- [x] 30 functional requirements (FR-001 through FR-030) defined
- [x] 15 non-functional requirements (NFR-001 through NFR-015) defined
- [x] Behavioral property registry format specified (FR-013 specification block)
- [x] Windows exclusion documented with explicit rationale (NFR-015)
- [x] NFR-008 rationale updated to include ADR-001 citation

**Traceability:**
- [x] Every functional requirement cites a specific ADR-001 section or E-XXX evidence entry in its Rationale
- [x] Every NFR is derived from an ADR-001 constraint, force, or FMEA failure mode
- [x] Bidirectional traceability matrix provided (ADR evidence → requirements; STK-N → requirements; layers → requirements; FMEA → requirements)
- [x] P-040 compliance: every requirement has a Parent trace to a stakeholder need
- [x] FR-012 present in FMEA reverse trace (added in Iteration 2)
- [x] IF-005 ADR source no longer self-referential (fixed in Iteration 2)
- [x] STK-N-001 table now distinguishes Primary from Secondary coverage (added in Iteration 2)
- [x] Evidence descriptions added to traceability matrix for all 22 E-XXX entries (added in Iteration 2)
- [x] E-012 deferral rationale documented (added in Iteration 2)
- [x] Appendix A Phase-to-Requirements Map added (added in Iteration 2)

**Testability:**
- [x] Every functional requirement has an assigned verification method (Analysis/Demonstration/Inspection/Test)
- [x] Every NFR with a numeric threshold specifies how the threshold is measured
- [x] No requirement uses unmeasurable qualifiers ("good", "appropriate", "satisfactory") without quantitative criteria
- [x] Given/When/Then acceptance criteria provided for all Must-priority FRs
- [x] Must-priority NFRs (NFR-001, NFR-002, NFR-003, NFR-004) include Given/When/Then acceptance criteria (added in Iteration 2)
- [x] Must-priority NFRs (NFR-005, NFR-007) now include Given/When/Then acceptance criteria (added in Iteration 3)
- [x] FR-012 Phase D verification dependency explicitly labeled as a phase acceptance criterion (added in Iteration 2)

**Consistency:**
- [x] FR-005 (tiered modes with N=1 Smoke) is consistent with FR-014 (N >= 20 enforcement): Smoke mode is explicitly excluded from statistical analysis
- [x] FR-023 (UV-only) is consistent with H-05 (Jerry hard rule)
- [x] FR-006 (DeepEval pytest integration) is consistent with H-20 (pytest mandate)
- [x] FR-016 uses QUALITY_PASS_THRESHOLD = 0.92, consistent with H-13 (Jerry quality gate)
- [x] NFR-002 "Must" priority is now consistent with FR-002 "Must" CI gate (fixed in Iteration 2)
- [x] FR-028 N=30 documented as independent specification, not derived from FR-005 (clarified in Iteration 2)
- [x] `stats.py` vs `layer4_stats.py` module naming fully resolved (fixed in Iteration 2)

**FMEA Coverage:**
- [x] All 10 failure modes addressed
- [x] FM-007 (RPN=432, highest priority) correctly documented as structurally irreducible per ADR-001; FR-027 provides maximum feasible mitigation
- [x] Phase F perturbation testing (partial FM-007 mitigation) noted as deferred future work

**P-043 Disclaimer:**
- [x] Mandatory disclaimer present at top of document

---

## References

| Source | Content |
|--------|---------|
| PROJ-035/decisions/ADR-001-test-harness-architecture.md | Primary source: Four-Layer Composite Architecture decision, all evidence entries E-001 through E-022, FMEA FM-001 through FM-010, implementation roadmap Phases A-F |
| NPR 7123.1D, Process 1 (Stakeholder Expectations) | Stakeholder identification and needs elicitation methodology |
| NPR 7123.1D, Process 2 (Technical Requirements) | Shall statement formulation, requirement quality criteria |
| NPR 7123.1D, Process 11 (Requirements Management) | Traceability matrix structure, bidirectional traces |
| NASA-HDBK-1009A | Requirements quality criteria (complete, consistent, verifiable, traceable, unambiguous, necessary, achievable) |
| Jerry quality-enforcement.md | H-05, H-11, H-13, H-20, H-23 constraints applied throughout |
| Jerry CLAUDE.md | P-002, P-003, P-020, P-022, P-040, P-043 constitutional compliance |

---

*Generated by nse-requirements agent v2.3.0*
*Source ADR: PROJ-035/decisions/ADR-001-test-harness-architecture.md (ACCEPTED 2026-03-06)*
*Criticality: C4 (architecture/governance deliverable — all tiers applied)*
*Iteration: 3 of adversarial scoring cycle*
*Evidence entries cited: 22 (E-001 through E-022)*
*Requirements count: FR-030, NFR-015, IF-007, STK-N-010*
*FMEA failure modes mitigated: 10/10 (FM-007 gap documented as structurally irreducible)*
*Findings resolved: FINDING-1 (module naming), FINDING-2 (NFR-002 priority), FINDING-3 (FR-012 reverse trace), FINDING-4 (FR-013 registry), FINDING-5 (IF-005 citation)*
*Iteration 3 fixes: NFR-005 G/W/T acceptance criteria added; NFR-007 G/W/T acceptance criteria added; Appendix B Verification Artifact Map added (FR-001 through FR-030 and NFR-001 through NFR-015)*
