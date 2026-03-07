# PROJ-036 Execution Prompt: Four-Layer Composite Test Harness Implementation

> **Project:** PROJ-036-prompt-regression-harness
> **Template:** Template 3 (Multi-Skill Orchestration)
> **Criticality:** C4 (irreversible architecture, public API surface, 67 agent definitions affected)
> **Skills:** /orchestration + /eng-team + /nasa-se + /red-team + /adversary + /worktracker
> **Quality Gate:** >= 0.95 S-014 weighted composite at every phase boundary (C4 requirement)
> **Source ADR:** PROJ-035 ADR-001 (ACCEPTED) -- Four-Layer Composite Architecture

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [How to Execute](#how-to-execute) | Instructions for running this prompt in a fresh session |
| [Project Setup](#project-setup) | Worktracker entity creation |
| [Orchestration Configuration](#orchestration-configuration) | Pipeline structure and parallel execution plan |
| [Phase Groups](#phase-groups) | All 8 groups with agent assignments and gate specifications |
| [Baseline Generation Details](#baseline-generation-details) | Phase 1C specification |
| [Behavioral Contract Details](#behavioral-contract-details) | Phase 1D specification |
| [Code Implementation Standards](#code-implementation-standards) | Architecture and coding constraints |
| [Forbidden Actions](#forbidden-actions) | NPT-013 constraints |
| [Output Map](#output-map) | Complete artifact-to-path mapping |

---

## How to Execute

1. Open a fresh Jerry session (Claude Code CLI).
2. Set the active project: `export JERRY_PROJECT=PROJ-036`.
3. Copy the entire [Prompt](#prompt) section below into the session.
4. The orchestrator will present the ORCHESTRATION_PLAN.md for your review before proceeding (P-020). Approve or revise the plan.
5. All subsequent phases execute automatically with quality gates. You will be consulted only at the final Phase 8 acceptance gate.
6. Sessions may span multiple context windows. Each phase group produces persistent file artifacts that survive compaction.

---

## Prompt

```
Use /worktracker to create a Project titled "Prompt Regression Harness" with ID PROJ-036
and slug prompt-regression-harness.

Create an Epic titled "Four-Layer Composite Test Harness" with ID EPIC-036-001 under PROJ-036.

Create a Feature titled "Test Harness Implementation" with ID FEAT-036-001 under EPIC-036-001.

Use /worktracker with wt-verifier to validate entity hierarchy integrity after creation.
Use /worktracker with wt-auditor to verify WORKTRACKER.md reflects the new entities.

---

Use /orchestration with orch-planner to design and sequence the following 8-group
implementation pipeline for building the Four-Layer Composite Test Harness architecture
defined in PROJ-035 ADR-001.

The source architecture decision: ADR-001 (PROJ-035, Four-Layer Composite Test Harness Architecture)

This ADR is ACCEPTED and defines a Four-Layer Composite Architecture:
- Layer 1: promptfoo CI/CD regression gate (GitHub Action + YAML test cases)
- Layer 2: DeepEval pytest evaluation backend (debiased LLM-as-Judge)
- Layer 3: Metamorphic relation framework (5 universal MRs, oracle-safe assertions)
- Layer 4: Statistical comparison engine (Wilcoxon signed-rank + Wilson score intervals)

All agents MUST use jerry:{agent-name} subagent_type format.
Main context = orchestrator window. All agents run via Task tool with run_in_background: true.
Human review is REQUIRED before orchestration plan approval (P-020).
All subsequent steps are automated with quality gates.
No token limit constraint -- sessions may span multiple context windows.
Each phase group produces persistent file artifacts that survive compaction.


### Orchestration Plan Structure

Present the orchestration plan for human review at:
projects/PROJ-036-prompt-regression-harness/orchestration/harness-impl-20260306-001/ORCHESTRATION_PLAN.md

The plan must define:
- Parallel execution within groups (Group 1, Group 3, Group 5, Group 7)
- Sequential execution between groups (sync barriers at quality gates)
- Agent assignments per phase
- Artifact dependencies between phases
- Quality gate pass/fail criteria at each barrier
- Criticality level: C4 for all quality gates

After human approval of the plan, execute all phases automatically.


==========================================================================
GROUP 1 — PARALLEL: Requirements + Architecture + Baseline + Contracts
==========================================================================

Four parallel streams producing foundational artifacts.


### Phase 1A: Requirements Derivation from ADR-001

Skill: /nasa-se
Agent: jerry:nse-requirements

Derive implementation requirements from the ACCEPTED PROJ-035 ADR-001.

Input artifact: ADR-001 (PROJ-035, Four-Layer Composite Test Harness Architecture)

Requirements derivation scope:
1. Functional requirements for each of the 4 layers (promptfoo, DeepEval, MR framework,
   statistical engine)
2. Interface specifications between layers (Layer 1->2, 2->3, 2->4 data contracts)
3. Acceptance criteria derived from ADR-001's evaluation dimensions (Refactoring Safety,
   Migration Confidence, Determinism Coverage, Statistical Rigor, Integration Feasibility,
   Time to First Value)
4. Constraints carried forward from ADR-001: OSI-licensed only, UV-only Python (H-05),
   pytest backbone (H-20), CI/CD merge blocking, non-determinism-aware assertions
5. FMEA-derived requirements: each of the 10 failure modes (FM-001 through FM-010) must
   map to at least one testable requirement
6. PROJ-017 ADR-002 shared infrastructure requirements: shared statistical module at
   jerry/testing/stats.py, shared promptfoo installation, shared DeepEval metrics
7. Tiered evaluation mode requirements: Smoke (1 run, $0), Standard (10 runs, ~$2),
   Full (30 runs, ~$5-8)

Traceability: Every requirement MUST trace to a specific ADR-001 section, force, constraint,
or FMEA failure mode using the evidence IDs (E-001 through E-022).

Output: projects/PROJ-036-prompt-regression-harness/requirements/harness-requirements.md
with L0/L1/L2 sections and requirements traceability matrix.


### Phase 1B: System Design with Threat Model

Skill: /eng-team + /nasa-se
Agent: jerry:eng-architect + jerry:nse-architecture + jerry:eng-lead

jerry:eng-architect produces system design. jerry:nse-architecture validates interface
specifications against requirements. jerry:eng-lead reviews module decomposition for
engineering standards compliance.

Produce system design for the Four-Layer Composite Test Harness.

Input artifacts:
- ADR-001 (PROJ-035, Four-Layer Composite Test Harness Architecture)
- Phase 1A output (requirements) -- wait for 1A if running sequentially; proceed with
  ADR-001 directly if running in parallel

System design scope:
1. Component architecture following hexagonal pattern (H-07):
   - Domain core: statistical engine, metamorphic relations, regression classification
   - Application layer: test orchestration, baseline management, report generation
   - Infrastructure adapters: promptfoo integration, DeepEval integration, GitHub Actions
2. Module decomposition with one class per file (H-10):
   - jerry/testing/stats.py -- shared statistical module (Wilcoxon, Wilson, Bonferroni)
   - jerry/testing/metamorphic/ -- MR framework (base class + 5 universal MRs)
   - jerry/testing/regression/ -- regression detection engine
   - jerry/testing/baselines/ -- baseline management and version key logic
   - jerry/testing/evaluation/ -- DeepEval metric wrappers with debiasing
3. Interface contracts: data types flowing between layers (score arrays, regression results,
   MR violation reports)
4. STRIDE threat model on the harness itself:
   - Spoofing: can test results be forged?
   - Tampering: can YAML test cases or baselines be manipulated?
   - Repudiation: can regression results be denied or hidden?
   - Information Disclosure: can API keys leak via test fixtures?
   - Denial of Service: can cost overrun from N>=20 be exploited?
   - Elevation of Privilege: can prompt injection via test case content affect evaluation?

Output: projects/PROJ-036-prompt-regression-harness/design/system-design.md
with L0/L1/L2 sections, component diagrams, and STRIDE threat model matrix.


### Phase 1C: Baseline Generation

Skill: /eng-team
Agent: jerry:eng-qa

Generate behavioral baselines for representative Jerry agents.

Agent selection criteria: cover at minimum 3 cognitive modes from the Jerry taxonomy
(divergent, convergent, integrative, systematic, forensic). Select agents that exercise
distinct methodology patterns.

Required baseline agents (minimum set):
- ps-researcher (divergent cognitive mode, T3 tier, research methodology)
- ps-analyst (convergent cognitive mode, T2 tier, FMEA/comparative analysis)
- ps-architect (convergent cognitive mode, T3 tier, ADR production)
- ps-critic (convergent cognitive mode, T2 tier, adversarial quality scoring)
- adv-scorer (convergent cognitive mode, T1 tier, S-014 LLM-as-Judge rubric)

For each agent, define 3-5 canonical test prompts:
- Each prompt must exercise the agent's core methodology (not trivial tasks)
- Prompts must be reproducible (deterministic input, no external data dependencies)
- Prompts must be self-contained (no file reads required during evaluation)
- Each prompt must include clear success criteria for structural compliance

Baseline capture protocol:
- Run each test prompt N=30 times against claude-sonnet-4-20250514
- Capture per-run: quality score (S-014 6-dimension), structural compliance
  (L0/L1/L2 sections present, navigation table present, citation count),
  response length (token count), methodology adherence (agent-specific checklist)
- Compute per-agent: mean score, standard deviation, Wilson score interval for
  pass rate (score >= 0.92), structural compliance rate
- Store raw data as JSON, summary as Markdown

NOTE: If API access is not available in this session to run N=30 evaluations,
produce the test prompt definitions, capture protocol specification, and baseline
schema as artifacts. Mark the actual baseline data collection as a follow-up task
that requires API execution. The artifacts produced here define WHAT to measure
and HOW -- the actual measurement is execution-dependent.

Output:
- projects/PROJ-036-prompt-regression-harness/baselines/baseline-protocol.md
  (capture methodology, agent selection rationale, per-prompt specifications)
- projects/PROJ-036-prompt-regression-harness/baselines/schemas/baseline-schema.json
  (JSON schema for baseline data files)
- projects/PROJ-036-prompt-regression-harness/baselines/prompts/
  (individual test prompt files per agent: ps-researcher-prompts.yaml, etc.)


### Phase 1D: Behavioral Contract Generation

Skill: /nasa-se
Agent: jerry:nse-requirements

Define behavioral contracts specifying pass/fail criteria for each agent type.

For each baseline agent (ps-researcher, ps-analyst, ps-architect, ps-critic, adv-scorer),
define the following contract dimensions:

1. Structural invariants (binary pass/fail):
   - Required markdown sections (e.g., L0/L1/L2 for research agents, Nygard format
     for architecture agents)
   - Navigation table presence and anchor link validity (H-23)
   - YAML frontmatter fields if applicable
   - Section ordering compliance

2. Quality bounds (numeric thresholds):
   - Minimum acceptable S-014 composite score: 0.85 for routine tasks, 0.92 for C2+
   - Maximum acceptable score variance across N runs: standard deviation <= 0.08
   - Minimum dimensional scores: no single dimension below 0.70
   - Maximum quality score regression: Wilcoxon p-value < 0.05 with effect size > 0.1

3. Behavioral metamorphic relations (tolerance specifications):
   - Paraphrase invariance (MR-001): quality score delta <= 0.05 when system prompt is
     paraphrased while preserving semantic content
   - Instruction ordering invariance (MR-004): quality score delta <= 0.03 when
     non-dependent instructions are reordered
   - Context padding invariance (MR-003): quality score delta <= 0.02 when irrelevant
     context is appended to the input
   - Negation sensitivity (MR-002): quality score must decrease by >= 0.10 when a
     critical constraint is negated (validates the harness detects real changes)

4. Regression thresholds:
   - Wilcoxon signed-rank: p-value < 0.05 = REGRESSION detected
   - Wilson confidence interval: overlapping CIs at 95% level = NO REGRESSION
   - Bonferroni correction: apply when comparing across 3+ metrics simultaneously
   - Marginal zone: 0.05 <= p-value < 0.10 = MARGINAL (warn, do not block)

Output: projects/PROJ-036-prompt-regression-harness/contracts/
- behavioral-contracts.md (unified contract document with all agents)
- contracts/schemas/contract-schema.json (JSON schema for machine-readable contracts)
- contracts/per-agent/ (individual contract files: ps-researcher-contract.yaml, etc.)


==========================================================================
GROUP 2 — SEQUENTIAL: Quality Gate 1 (C4, >= 0.95)
==========================================================================

### Phase 2: C4 Adversarial Quality Gate on Group 1 Outputs

Skill: /adversary
Agent: jerry:adv-scorer + jerry:adv-executor

Score ALL Group 1 outputs (1A, 1B, 1C, 1D) against S-014 LLM-as-Judge rubric.
This is a C4 quality gate: ALL 10 adversarial strategies must be applied.

Quality threshold: >= 0.95 weighted composite per deliverable.

S-014 Dimensions and weights:
- Completeness (0.20)
- Internal Consistency (0.20)
- Methodological Rigor (0.20)
- Evidence Quality (0.15)
- Actionability (0.15)
- Traceability (0.10)

C4 Strategy Application (all 10 required):
- S-001: Red Team Analysis
- S-002: Devil's Advocate
- S-003: Steelman Technique (H-16: before S-002)
- S-004: Pre-Mortem Analysis
- S-007: Constitutional AI Critique
- S-010: Self-Refine
- S-011: Chain-of-Verification
- S-012: FMEA
- S-013: Inversion Technique
- S-014: LLM-as-Judge

Below threshold: Return to the producing agent for targeted revision.
Maximum 5 iterations per deliverable (C4 ceiling per RT-M-010).

Score reports: projects/PROJ-036-prompt-regression-harness/quality-gates/gate-1/
- 1A-requirements-score.md
- 1B-system-design-score.md
- 1C-baseline-score.md
- 1D-contracts-score.md

All 4 deliverables MUST pass before proceeding to Group 3.


==========================================================================
GROUP 3 — PARALLEL: Implementation (Layers 1-4 + CI/CD)
==========================================================================

Five parallel implementation streams. All follow Jerry coding standards.

Context for all implementers:
- Read Phase 1A requirements for acceptance criteria
- Read Phase 1B system design for module decomposition and interfaces
- Read Phase 1D contracts for test assertion specifications
- Read ADR-001 for component integration patterns and code examples


### Phase 3A: Layer 1 — promptfoo CI/CD Integration

Skill: /eng-team
Agent: jerry:eng-backend

Implement the promptfoo GitHub Action integration and YAML test case definitions.

Implementation scope:
1. GitHub Actions workflow file: .github/workflows/prompt-regression.yml
   - Trigger: on PR when files in skills/*/agents/*.md are modified
   - Three workflow modes: Smoke (every PR), Standard (agent definition PRs),
     Full (manual trigger or pre-release tag)
   - Artifact upload of regression reports
   - Status check integration (blocks merge on REGRESSION)

2. YAML test case template: tests/prompt-regression/template.yaml
   - promptfoo configuration with Jerry-specific provider settings
   - Anthropic provider configuration (claude-sonnet-4-20250514)
   - Temperature: 0 for deterministic structural checks, 0.3 for quality evaluation
   - Custom Python assertion provider bridge to Layer 2 (DeepEval metrics)

3. Per-agent test case files: tests/prompt-regression/{agent-name}.yaml
   - Generate test case YAML for each baseline agent (ps-researcher, ps-analyst,
     ps-architect, ps-critic, adv-scorer)
   - Each file references the agent's prompt file (file://skills/.../agents/{name}.md)
   - Test variables from Phase 1C baseline prompts
   - Assertion references to Layer 2 metrics and Layer 3 MR checks

4. Version key management: git commit hash + file path as composite key
   - FM-005 mitigation: version key uniquely identifies the exact prompt version
   - Baseline store lookup uses this key

5. promptfoo Docker configuration (FM-004 mitigation):
   - Dockerfile for promptfoo execution (avoids npm dependency in UV-only project)
   - GitHub Action uses Docker image, not local npm install

File paths:
- .github/workflows/prompt-regression.yml
- tests/prompt-regression/template.yaml
- tests/prompt-regression/promptfoo-config.yaml
- tests/prompt-regression/agents/ (per-agent YAML test cases)
- docker/promptfoo/Dockerfile

Output: All files above + implementation notes at
projects/PROJ-036-prompt-regression-harness/implementation/layer-1-promptfoo.md


### Phase 3B: Layer 2 — DeepEval Evaluation Backend

Skill: /eng-team
Agent: jerry:eng-backend

Implement DeepEval pytest plugin integration with debiasing.

Implementation scope:
1. DeepEval dependency: uv add deepeval (pin version in uv.lock)
   - FM-008 mitigation: pin exact version to prevent score scale drift

2. Debiased LLM-as-Judge metrics: jerry/testing/evaluation/
   - jerry/testing/evaluation/__init__.py
   - jerry/testing/evaluation/debiased_judge.py
     (position randomization + rubric shuffling per ADR-001 Phase 1D Innovation #1)
   - jerry/testing/evaluation/quality_score.py
     (S-014 6-dimension scoring adapted for harness use)
   - jerry/testing/evaluation/structural_checks.py
     (L0/L1/L2 section presence, navigation table, citation count)
   - FM-001 mitigation: position randomization as mandatory configuration

3. Custom DeepEval metrics: jerry/testing/evaluation/metrics/
   - jerry/testing/evaluation/metrics/__init__.py
   - jerry/testing/evaluation/metrics/base_metric.py (BaseMetric subclass)
   - jerry/testing/evaluation/metrics/section_compliance.py
   - jerry/testing/evaluation/metrics/navigation_table.py
   - jerry/testing/evaluation/metrics/citation_quality.py

4. pytest integration: tests/prompt-regression/conftest.py
   - DeepEval fixtures for test case creation
   - Provider configuration
   - Score collection and aggregation

File paths:
- jerry/testing/__init__.py
- jerry/testing/evaluation/ (all files above)
- tests/prompt-regression/conftest.py

Output: All files above + implementation notes at
projects/PROJ-036-prompt-regression-harness/implementation/layer-2-deepeval.md


### Phase 3C: Layer 3 — Metamorphic Relation Framework

Skill: /eng-team
Agent: jerry:eng-backend

Implement the 5 universal metamorphic relations as custom DeepEval metrics.

Implementation scope:
1. MR base class: jerry/testing/metamorphic/__init__.py
   - jerry/testing/metamorphic/base_relation.py
     (abstract base: transform(), check_consistency(), tolerance parameter)

2. Five universal MRs per ADR-001 L1 Technical Implementation:
   - jerry/testing/metamorphic/mr_001_paraphrase.py
     Paraphrase consistency: paraphrasing system prompt should not change quality
     score by more than +/- tolerance (default 0.05)
   - jerry/testing/metamorphic/mr_002_negation.py
     Negation handling: negating a critical constraint should measurably decrease
     quality (validates harness sensitivity, not prompt quality)
   - jerry/testing/metamorphic/mr_003_context_padding.py
     Irrelevant context appendation: adding irrelevant context to input should not
     change quality score by more than +/- tolerance (default 0.02)
   - jerry/testing/metamorphic/mr_004_formatting.py
     Formatting perturbation: changing markdown formatting (bold, headers, list style)
     of the system prompt should not change quality score by more than +/- tolerance
     (default 0.03)
   - jerry/testing/metamorphic/mr_005_language_roundtrip.py
     Language round-trip: translating input to another language and back should
     preserve quality score within +/- tolerance (default 0.10)

3. MR DeepEval integration: each MR is a custom DeepEval metric (BaseMetric subclass)
   that can be referenced in promptfoo YAML test cases

4. MR tolerance calibration: default tolerances from Phase 1D contracts; allow
   per-agent override via contract YAML files

File paths:
- jerry/testing/metamorphic/ (all files above)

Output: All files above + implementation notes at
projects/PROJ-036-prompt-regression-harness/implementation/layer-3-metamorphic.md


### Phase 3D: Layer 4 — Statistical Comparison Engine

Skill: /eng-team
Agent: jerry:eng-backend

Implement the statistical comparison engine as a shared module.

Implementation scope:
1. Core statistical module: jerry/testing/stats.py
   This module is SHARED with PROJ-017. Design for both use cases:
   - PROJ-035/036: Wilcoxon signed-rank for prompt version comparison (regression)
   - PROJ-017: BCa bootstrap + permutation for skill effectiveness (effect size)

   Functions:
   - compare_versions(scores_a, scores_b, alpha=0.05) -> RegressionResult
     Wilcoxon signed-rank test with N >= 20 enforcement (FM-002 mitigation)
   - wilson_interval(successes, total, confidence=0.95) -> ConfidenceInterval
     Wilson score interval for per-metric pass rate estimation
   - bonferroni_correct(p_values, alpha=0.05) -> list[CorrectedResult]
     Bonferroni correction for multi-metric simultaneous comparison
   - classify_regression(stat_result, effect_threshold=0.1) -> RegressionClass
     Enum: NO_REGRESSION | MARGINAL | REGRESSION

2. Data types: jerry/testing/types.py
   - RegressionResult (dataclass: statistic, p_value, classification, ci_a, ci_b)
   - ConfidenceInterval (dataclass: lower, upper, point_estimate)
   - CorrectedResult (dataclass: original_p, corrected_p, significant)
   - RegressionClass (enum: NO_REGRESSION, MARGINAL, REGRESSION)
   - BaselineData (dataclass: scores, metadata, version_key, timestamp)

3. Baseline management: jerry/testing/baselines/
   - jerry/testing/baselines/__init__.py
   - jerry/testing/baselines/store.py
     (load/save baseline data keyed by git_hash + file_path; FM-005 mitigation)
   - jerry/testing/baselines/validator.py
     (validate baseline quality before acceptance; FM-010 mitigation)

4. Report generation: jerry/testing/reports/
   - jerry/testing/reports/__init__.py
   - jerry/testing/reports/regression_report.py
     (Markdown report with statistical results, CI visualization, classification)
   - jerry/testing/reports/pr_comment.py
     (GitHub PR comment format for regression results)

File paths:
- jerry/testing/stats.py
- jerry/testing/types.py
- jerry/testing/baselines/ (all files above)
- jerry/testing/reports/ (all files above)

Output: All files above + implementation notes at
projects/PROJ-036-prompt-regression-harness/implementation/layer-4-statistical.md


### Phase 3E: CI/CD Pipeline Setup

Skill: /eng-team
Agent: jerry:eng-devsecops

Set up the GitHub Actions CI/CD pipeline with tiered evaluation modes.

Implementation scope:
1. Three-tier GitHub Actions workflow modes per ADR-001:
   - Smoke (every PR): 1 run, deterministic checks only, ~$0, ~2 min
     Structural compliance: L0/L1/L2 sections, navigation table, YAML validity
     Report labeled: "STRUCTURAL ONLY -- not statistically valid"
   - Standard (agent definition PRs): 10 runs, LLM-as-Judge + structural, ~$2, ~10 min
     Quality score comparison with statistical caveat for N<20
   - Full (manual trigger or release tag): 30 runs, all 4 layers, ~$5-8, ~30 min
     Full statistical analysis with Wilcoxon + Wilson + Bonferroni

2. Workflow triggers:
   - paths filter: skills/*/agents/*.md, jerry/testing/**, tests/prompt-regression/**
   - Manual dispatch: workflow_dispatch with mode selection input
   - Release tag: triggered on v*.*.* tags with Full mode

3. Secret management:
   - ANTHROPIC_API_KEY via GitHub Secrets (never in config files)
   - DEEPEVAL_API_KEY if needed for DeepEval telemetry (optional)

4. Artifact management:
   - Upload regression reports as GitHub Actions artifacts
   - Post PR comment with summary results via github-script action
   - Status check integration: required check for merge

5. Cost monitoring:
   - Log estimated cost per run in workflow output
   - FM-006 mitigation: budget alerts if monthly cost exceeds threshold

File paths:
- .github/workflows/prompt-regression.yml (primary workflow)
- .github/workflows/prompt-regression-full.yml (Full mode manual trigger)
- .github/actions/regression-report/action.yml (composite action for reporting)

Output: All files above + implementation notes at
projects/PROJ-036-prompt-regression-harness/implementation/cicd-pipeline.md


==========================================================================
GROUP 4 — SEQUENTIAL: Quality Gate 2 (C4, >= 0.95)
==========================================================================

### Phase 4: C4 Adversarial Quality Gate on Implementation

Skill: /adversary
Agent: jerry:adv-scorer + jerry:adv-executor

Score ALL Group 3 implementation outputs (3A through 3E) against S-014 rubric.
C4 quality gate: all 10 adversarial strategies applied.

Quality threshold: >= 0.95 weighted composite per deliverable.

Additional implementation-specific review criteria:
- Code compiles and passes type checking (mypy strict)
- All public functions have type hints and docstrings (H-11)
- One class per file (H-10)
- Domain core has no infrastructure imports (H-07)
- No API keys or credentials in code or config files
- N >= 20 enforcement present in statistical engine
- Debiasing configuration is mandatory (not optional) in LLM-as-Judge setup

Below threshold: Return to producing jerry:eng-backend or jerry:eng-devsecops
for targeted revision. Maximum 5 iterations per deliverable (C4 ceiling).

Score reports: projects/PROJ-036-prompt-regression-harness/quality-gates/gate-2/
- 3A-promptfoo-score.md
- 3B-deepeval-score.md
- 3C-metamorphic-score.md
- 3D-statistical-score.md
- 3E-cicd-score.md

All 5 deliverables MUST pass before proceeding to Group 5.


==========================================================================
GROUP 5 — PARALLEL: Security Assessment + V&V + Test Suite
==========================================================================

Three parallel validation streams.


### Phase 5A: Security Assessment of the Harness

Skill: /red-team
Agent: jerry:red-lead + jerry:red-vuln + jerry:red-exploit

Security assessment of the test harness itself (not the agents being tested).

Engagement scope:
1. YAML injection via test case files:
   - Can a malicious YAML test case in tests/prompt-regression/ inject arbitrary
     commands or modify evaluation behavior?
   - Can YAML anchors, aliases, or merge keys be abused?

2. Prompt injection via test case content:
   - Can test case variables (user_query field) contain prompt injection payloads
     that compromise the evaluation LLM's scoring objectivity?
   - FM-007 attack surface: test cases that appear benign but exploit LLM-as-Judge
     scoring biases

3. Statistical manipulation:
   - Can an adversary craft N=20 samples that pass Wilcoxon but mask real regression?
   - Can baseline data be tampered with to set artificially low standards?
   - FM-010 attack: injecting a known-poor baseline to make any future version "pass"

4. Credential exposure:
   - Review all config files, Docker configurations, and GitHub Actions workflows
     for potential API key leakage
   - Verify ANTHROPIC_API_KEY is exclusively in GitHub Secrets

5. FMEA attack surface review:
   - For each of FM-001 through FM-010, assess whether the failure mode can be
     deliberately triggered by a malicious contributor

Output: projects/PROJ-036-prompt-regression-harness/security/
- security-assessment.md (findings with severity: CRITICAL/HIGH/MEDIUM/LOW)
- attack-scenarios.md (detailed attack scenarios with reproduction steps)
- remediation-recommendations.md (fixes prioritized by severity)


### Phase 5B: V&V Execution Against Requirements

Skill: /nasa-se
Agent: jerry:nse-verification

Verify and validate the implementation against Phase 1A requirements.

V&V scope:
1. Requirements coverage matrix:
   - Every requirement from Phase 1A must map to at least one implemented artifact
   - Every FMEA-derived requirement must map to a specific mitigation in code

2. Interface verification:
   - Layer 1->2 data contract: verify promptfoo output format matches DeepEval input
   - Layer 2->3 data contract: verify score arrays flow correctly to MR framework
   - Layer 2->4 data contract: verify score arrays flow correctly to statistical engine

3. Constraint verification:
   - H-05 (UV-only): verify no python/pip commands in scripts or CI
   - H-07 (hexagonal): verify jerry/testing/ domain core has no infrastructure imports
   - H-10 (one class per file): verify module structure
   - H-11 (type hints + docstrings): verify all public functions
   - H-20 (pytest backbone): verify all tests use pytest

4. FMEA mitigation verification:
   - FM-002: N >= 20 assertion present in compare_versions()
   - FM-004: Docker/GHA configuration present (no local npm)
   - FM-005: git hash + file path version key implementation present
   - FM-006: tiered evaluation modes implemented
   - FM-008: DeepEval version pinned in uv.lock

Output: projects/PROJ-036-prompt-regression-harness/verification/
- requirements-coverage-matrix.md
- interface-verification.md
- constraint-verification.md
- fmea-mitigation-verification.md
- vv-summary.md (pass/fail per verification item)


### Phase 5C: Test Suite Development

Skill: /eng-team
Agent: jerry:eng-qa

Build the test suite for the harness itself.

Test suite scope:
1. BDD test-first (H-20): write tests in Red phase first, then verify against
   implementation

2. Unit tests: tests/prompt-regression/unit/
   - test_stats.py: Wilcoxon comparison with known data, Wilson intervals, Bonferroni
   - test_metamorphic.py: each MR with controlled input/output pairs
   - test_baseline_store.py: load/save/version key management
   - test_debiased_judge.py: position randomization produces different orderings
   - test_regression_report.py: report generation format compliance
   - test_types.py: data type validation and serialization

3. Property-based tests (for statistical engine): tests/prompt-regression/property/
   - test_stats_properties.py:
     Property: compare_versions with identical arrays always returns NO_REGRESSION
     Property: compare_versions with strictly dominated arrays returns REGRESSION
     Property: Wilson interval always contains the point estimate
     Property: Bonferroni-corrected p-values are always >= original p-values
     Property: compare_versions raises InsufficientSamplesError when N < 20

4. Integration tests: tests/prompt-regression/integration/
   - test_layer_integration.py: end-to-end flow from YAML -> DeepEval -> stats
   - test_baseline_roundtrip.py: save baseline, load baseline, compare versions

5. Coverage requirement: 90% line coverage (H-21) on jerry/testing/ package

File paths:
- tests/prompt-regression/unit/ (all test files)
- tests/prompt-regression/property/ (property-based tests)
- tests/prompt-regression/integration/ (integration tests)
- tests/prompt-regression/conftest.py (shared fixtures)

Output: All test files + coverage report at
projects/PROJ-036-prompt-regression-harness/verification/test-coverage-report.md


==========================================================================
GROUP 6 — SEQUENTIAL: Quality Gate 3 (C4, >= 0.95)
==========================================================================

### Phase 6: C4 Adversarial Quality Gate on Security + V&V + Tests

Skill: /adversary
Agent: jerry:adv-scorer + jerry:adv-executor

Score ALL Group 5 outputs (5A, 5B, 5C) against S-014 rubric.
C4 quality gate: all 10 adversarial strategies applied.

Quality threshold: >= 0.95 weighted composite per deliverable.

Additional validation-specific review criteria:
- Security findings are actionable (not theoretical)
- V&V coverage matrix has no uncovered requirements
- Test suite covers all FMEA failure mode mitigations
- Property-based tests cover statistical engine edge cases
- 90% line coverage demonstrated

Below threshold: Return to producing agent for revision.
Maximum 5 iterations per deliverable (C4 ceiling).

Score reports: projects/PROJ-036-prompt-regression-harness/quality-gates/gate-3/
- 5A-security-score.md
- 5B-vv-score.md
- 5C-test-suite-score.md

All 3 deliverables MUST pass before proceeding to Group 7.


==========================================================================
GROUP 7 — PARALLEL: Engineering Review + Cross-Synthesis
==========================================================================

Two parallel finalization streams.


### Phase 7A: Final Engineering Review

Skill: /eng-team
Agent: jerry:eng-reviewer

Comprehensive engineering review of the complete implementation.

Review dimensions:
1. OWASP Top 10 compliance for the CI/CD pipeline
2. ASVS (Application Security Verification Standard) level 1 check
3. Code quality: SOLID principles, clean code, naming conventions
4. Security: verify all Phase 5A remediation recommendations are addressed
5. Architecture compliance: hexagonal layers respected (H-07), no domain->infra imports
6. Testing completeness: 90% coverage, property-based tests for statistical engine
7. Documentation: all public modules have docstrings, README for tests/prompt-regression/

Output: projects/PROJ-036-prompt-regression-harness/reviews/
- engineering-review.md (findings with severity classification)


### Phase 7B: Cross-Synthesis

Skill: /problem-solving
Agent: jerry:ps-synthesizer

Synthesize findings from ALL parallel streams into a unified implementation report.

Input artifacts:
- All Phase 1 outputs (requirements, design, baselines, contracts)
- All Phase 3 outputs (5 implementation streams)
- All Phase 5 outputs (security, V&V, test suite)
- Phase 7A engineering review

Synthesis tasks:
1. Implementation completeness assessment: which ADR-001 roadmap phases are fully
   implemented? (target: Phases A-D complete)
2. Risk register update: for each FM-001 through FM-010, document current mitigation
   status (MITIGATED / PARTIALLY_MITIGATED / OPEN)
3. Residual gaps: what remains for Phase E (baseline quality) and Phase F (coverage)?
4. PROJ-017 integration readiness: is the shared jerry/testing/stats.py module ready
   for both PROJ-035 regression and PROJ-017 skill evaluation use cases?
5. Operational readiness checklist: what must happen before the harness runs on real PRs?

Output: projects/PROJ-036-prompt-regression-harness/synthesis/
- implementation-report.md (L0/L1/L2 sections)
- risk-register-update.md
- operational-readiness-checklist.md


==========================================================================
GROUP 8 — SEQUENTIAL: Final Dual Quality Gate + Human Acceptance
==========================================================================

### Phase 8: Dual Gate + Human Review

Two quality gates must BOTH pass before presenting to human.


#### Gate A: C4 Adversarial Quality Gate

Skill: /adversary
Agent: jerry:adv-scorer

Score the complete implementation package (Phase 7B synthesis + all deliverables)
against S-014 rubric.

Quality threshold: >= 0.95 weighted composite.
C4: all 10 adversarial strategies applied.

Below threshold: Return to producing agents for revision.
Maximum 5 iterations (C4 ceiling).

Score report: projects/PROJ-036-prompt-regression-harness/quality-gates/gate-final/
- gate-a-adversarial-score.md


#### Gate B: NASA SE Technical Review

Skill: /nasa-se
Agent: jerry:nse-reviewer

Technical review gate with entrance/exit criteria per NPR 7123.1D Appendix G.

Verify:
- Requirements traceability: every ADR-001 requirement has implementation evidence
- Evidence basis: all implementation decisions trace to ADR-001 evidence IDs
- Risk coverage: all 10 FMEA failure modes have documented mitigations
- Implementation feasibility: code compiles, tests pass, CI workflow is valid
- PROJ-017 compatibility: shared infrastructure is compatible

Score report: projects/PROJ-036-prompt-regression-harness/quality-gates/gate-final/
- gate-b-nse-review.md


#### Human Acceptance (P-020)

BOTH Gate A AND Gate B MUST pass before presenting to human.

Present to human:
1. Complete implementation package summary (Phase 7B synthesis)
2. All quality gate scores (Gates 1, 2, 3, Final A, Final B)
3. Security assessment summary (Phase 5A)
4. Residual risks and operational readiness checklist
5. Recommendation: ACCEPT the implementation for merge to main branch

The human decides whether to accept, request revisions, or reject.


==========================================================================
FORBIDDEN ACTIONS (NPT-013)
==========================================================================

<forbidden_actions>
  <constraint format="NPT-013">
    NEVER use `python` or `pip` directly -- Consequence: environment corruption
    breaks CI and violates H-05; UV-managed virtual environment becomes inconsistent
    with lockfile. Instead: use `uv run` for all Python execution, `uv add` for
    dependency installation.
  </constraint>

  <constraint format="NPT-013">
    NEVER skip the N >= 20 minimum sample size for statistical tests -- Consequence:
    Wilcoxon signed-rank produces unreliable p-values below N=20, per ICML 2025
    finding that "CLT-based methods perform very poorly" with small samples;
    false regression classifications propagate to merge decisions. Instead: enforce
    via runtime assertion in compare_versions() that raises InsufficientSamplesError.
  </constraint>

  <constraint format="NPT-013">
    NEVER use exact-output assertions for LLM responses -- Consequence: 100% false
    positive rate due to LLM non-determinism; every test run fails regardless of
    prompt quality, rendering the harness useless. Instead: use metamorphic relations,
    quality score thresholds, and statistical comparison across N runs.
  </constraint>

  <constraint format="NPT-013">
    NEVER merge a PR that modifies agent definitions without regression test passage --
    Consequence: silent behavioral degradation across 67 agent definitions; regressions
    compound through downstream agent handoff chains. Instead: promptfoo GitHub Action
    blocks merge on REGRESSION classification; Smoke mode runs on every PR.
  </constraint>

  <constraint format="NPT-013">
    NEVER cite LLM training knowledge as evidence in baseline or contract definitions --
    Consequence: baselines built on hallucinated data produce meaningless regression
    comparisons; the entire harness operates on fabricated ground truth. Instead:
    derive all baselines from measured runs against the live model with documented
    capture protocol.
  </constraint>

  <constraint format="NPT-013">
    NEVER store API keys, model credentials, or cost data in test fixture files --
    Consequence: credential leak via public repository; Anthropic API key exposure
    enables unauthorized usage and billing fraud. Instead: use environment variables
    and GitHub Secrets exclusively; verify via Phase 5A security assessment.
  </constraint>

  <constraint format="NPT-013">
    NEVER bypass quality gates below 0.95 for C4 deliverables -- Consequence:
    sub-threshold work propagates through the pipeline; downstream phases build on
    unvalidated foundations, compounding quality debt per error amplification patterns
    (1.3x per handoff). Instead: revise and re-score per H-14 creator-critic cycle,
    maximum 5 iterations at C4 criticality.
  </constraint>
</forbidden_actions>


==========================================================================
CODE IMPLEMENTATION STANDARDS
==========================================================================

All implementation phases MUST follow these standards:

Architecture:
- Hexagonal architecture (H-07): domain core (jerry/testing/stats.py,
  jerry/testing/metamorphic/, jerry/testing/types.py) has NO infrastructure imports
- Application layer (jerry/testing/baselines/, jerry/testing/reports/) may import
  domain but not infrastructure
- Infrastructure adapters (jerry/testing/evaluation/, CI config) contain all external
  tool integrations (DeepEval, promptfoo, GitHub Actions)
- One class per file (H-10)

Code quality:
- Type hints on all public function signatures (H-11)
- Docstrings on all public functions (H-11)
- All Python execution via uv run (H-05)
- All dependencies via uv add (H-05)

Testing:
- BDD test-first Red phase (H-20): write tests before implementation
- 90% line coverage on jerry/testing/ package (H-21)
- pytest as test runner (H-20)
- Property-based tests for statistical engine (hypothesis library)

File organization:
- Production code: jerry/testing/ (new package)
- Test code: tests/prompt-regression/ (new test directory)
- CI config: .github/workflows/ (new workflow files)
- Docker: docker/promptfoo/ (new Dockerfile)
- Baselines: projects/PROJ-036-prompt-regression-harness/baselines/
- Contracts: projects/PROJ-036-prompt-regression-harness/contracts/

Shared module (PROJ-017 compatibility):
- jerry/testing/stats.py is shared between PROJ-035 (regression) and PROJ-017 (skill eval)
- Design the module API to serve both use cases without feature flags or conditional logic
- Both projects consume paired score arrays; the statistical tests differ but the data
  format is identical


==========================================================================
OUTPUT MAP
==========================================================================

Complete artifact-to-path mapping for all phases:

| Phase | Artifact | Path |
|-------|----------|------|
| Setup | Orchestration plan | projects/PROJ-036-prompt-regression-harness/orchestration/harness-impl-20260306-001/ORCHESTRATION_PLAN.md |
| 1A | Requirements | projects/PROJ-036-prompt-regression-harness/requirements/harness-requirements.md |
| 1B | System design | projects/PROJ-036-prompt-regression-harness/design/system-design.md |
| 1C | Baseline protocol | projects/PROJ-036-prompt-regression-harness/baselines/baseline-protocol.md |
| 1C | Baseline schema | projects/PROJ-036-prompt-regression-harness/baselines/schemas/baseline-schema.json |
| 1C | Test prompts | projects/PROJ-036-prompt-regression-harness/baselines/prompts/*.yaml |
| 1D | Behavioral contracts | projects/PROJ-036-prompt-regression-harness/contracts/behavioral-contracts.md |
| 1D | Contract schema | projects/PROJ-036-prompt-regression-harness/contracts/schemas/contract-schema.json |
| 1D | Per-agent contracts | projects/PROJ-036-prompt-regression-harness/contracts/per-agent/*.yaml |
| Gate 1 | Score reports | projects/PROJ-036-prompt-regression-harness/quality-gates/gate-1/*.md |
| 3A | Layer 1 impl | .github/workflows/prompt-regression.yml + tests/prompt-regression/ + docker/promptfoo/ |
| 3A | Layer 1 notes | projects/PROJ-036-prompt-regression-harness/implementation/layer-1-promptfoo.md |
| 3B | Layer 2 impl | jerry/testing/evaluation/ |
| 3B | Layer 2 notes | projects/PROJ-036-prompt-regression-harness/implementation/layer-2-deepeval.md |
| 3C | Layer 3 impl | jerry/testing/metamorphic/ |
| 3C | Layer 3 notes | projects/PROJ-036-prompt-regression-harness/implementation/layer-3-metamorphic.md |
| 3D | Layer 4 impl | jerry/testing/stats.py + jerry/testing/types.py + jerry/testing/baselines/ + jerry/testing/reports/ |
| 3D | Layer 4 notes | projects/PROJ-036-prompt-regression-harness/implementation/layer-4-statistical.md |
| 3E | CI/CD impl | .github/workflows/ + .github/actions/ |
| 3E | CI/CD notes | projects/PROJ-036-prompt-regression-harness/implementation/cicd-pipeline.md |
| Gate 2 | Score reports | projects/PROJ-036-prompt-regression-harness/quality-gates/gate-2/*.md |
| 5A | Security assessment | projects/PROJ-036-prompt-regression-harness/security/*.md |
| 5B | V&V results | projects/PROJ-036-prompt-regression-harness/verification/*.md |
| 5C | Test suite | tests/prompt-regression/unit/ + property/ + integration/ |
| 5C | Coverage report | projects/PROJ-036-prompt-regression-harness/verification/test-coverage-report.md |
| Gate 3 | Score reports | projects/PROJ-036-prompt-regression-harness/quality-gates/gate-3/*.md |
| 7A | Engineering review | projects/PROJ-036-prompt-regression-harness/reviews/engineering-review.md |
| 7B | Implementation report | projects/PROJ-036-prompt-regression-harness/synthesis/implementation-report.md |
| 7B | Risk register | projects/PROJ-036-prompt-regression-harness/synthesis/risk-register-update.md |
| 7B | Readiness checklist | projects/PROJ-036-prompt-regression-harness/synthesis/operational-readiness-checklist.md |
| Gate Final | Adversarial score | projects/PROJ-036-prompt-regression-harness/quality-gates/gate-final/gate-a-adversarial-score.md |
| Gate Final | NSE review | projects/PROJ-036-prompt-regression-harness/quality-gates/gate-final/gate-b-nse-review.md |
```

---

## 5-Element Analysis

| Element | Present | Content |
|---------|---------|---------|
| **1. Skill Routing** | Yes | `/orchestration` with orch-planner, `/nasa-se` with nse-requirements + nse-verification + nse-architecture + nse-reviewer, `/eng-team` with eng-architect + eng-lead + eng-backend + eng-qa + eng-devsecops + eng-reviewer, `/red-team` with red-lead + red-vuln + red-exploit, `/adversary` with adv-scorer + adv-executor, `/worktracker` with wt-verifier + wt-auditor, `/problem-solving` with ps-synthesizer |
| **2. Scope** | Yes | Domain: Four-Layer Composite Test Harness (ADR-001 implementation). Source: PROJ-035 ADR-001 (ACCEPTED). Covers all 4 layers + CI/CD + baselines + contracts + security + V&V. 67 agent definitions in scope. |
| **3. Data Source** | Yes | ADR-001 as primary input. Phase 1C baselines from live model runs (claude-sonnet-4-20250514). No LLM training knowledge as evidence (NPT-013 constraint). |
| **4. Quality Gate** | Yes | >= 0.95 S-014 weighted composite at every phase boundary (C4). ALL 10 adversarial strategies. Dual gate (adv-scorer + nse-reviewer) at final phase. Maximum 5 iterations per deliverable. Human acceptance at P-020 boundary. |
| **5. Output Path** | Yes | All outputs under `projects/PROJ-036-prompt-regression-harness/` with explicit paths per phase. Production code at `jerry/testing/`. Test code at `tests/prompt-regression/`. CI at `.github/workflows/`. Complete output map provided. |

---

*Generated for PROJ-036 implementation of PROJ-035 ADR-001 (Four-Layer Composite Architecture)*
*Template: Template 3 (Multi-Skill Orchestration) from `.context/rules/prompt-templates.md`*
*Constraints: NPT-013 structured negation per PROJ-014 findings*
*Criticality: C4 (irreversible architecture, 67 agent definitions affected)*
*Source: PROJ-035 ADR-001 (ACCEPTED 2026-03-06)*
