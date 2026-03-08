# Gap Analysis Orchestration Prompt — PROJ-036 Test Harness

> **Status:** AWAITING HUMAN REVIEW — Do NOT execute until approved.
> **Built by:** pe-builder (5-element prompt anatomy)
> **Date:** 2026-03-07
> **Quality Score:** Pending pe-scorer evaluation

---

## Prompt Anatomy Breakdown

| Element | Value |
|---------|-------|
| Skill Routing | `/orchestration` + `/problem-solving` + `/nasa-se` + `/adversary` + `/eng-team` + `/red-team` + `/worktracker` |
| Domain Scope | Gap analysis: `jerry/testing/` building blocks vs FR-001–FR-030 vs validation-run outputs |
| Data Sources | Codebase (`jerry/testing/**/*.py`), validation outputs (5 agents + Phase 2-4 results), requirements (`design/harness-requirements.md`) |
| Quality Gate | C3 criticality, >= 0.92 weighted composite (S-014 LLM-as-Judge) |
| Output Path | `projects/PROJ-036-prompt-regression-harness/orchestration/gap-analysis-20260307-001/` |

---

## The Prompt

```
Use /worktracker to create a Feature titled "PROJ-036 Gap Analysis: Test Harness Integration Layer"
under PROJ-036, linked to EPIC-036-001.

Use /orchestration with orch-planner to sequence a 6-phase gap analysis pipeline.
Workflow ID: gap-analysis-20260307-001.
Pattern: Fan-Out/Fan-In with quality gates at phase boundaries.
Criticality: C3 (>= 0.92 quality gate per phase).
All phase agents MUST run in background via Task tool.
Main context is the orchestrator — do NOT spawn recursive subagents.

Output orchestration plan:
  projects/PROJ-036-prompt-regression-harness/orchestration/gap-analysis-20260307-001/ORCHESTRATION_PLAN.md

---

Phase 1 — Gap Identification (Fan-Out: 2 parallel agents)

  Phase 1A: Use /problem-solving with ps-analyst to perform a gap analysis between:
    - IMPLEMENTED building blocks in jerry/testing/:
      - jerry/testing/evaluation/deepeval_adapter.py (DeepEvalAdapter)
      - jerry/testing/evaluation/jerry_geval_deepeval_metric.py (JerryGEvalDeepEvalMetric + AnthropicModel fix)
      - jerry/testing/evaluation/ports.py (EvaluationPort protocol)
      - jerry/testing/evaluation/debiasing.py (DebiasingStrategy, C-007 criterion shuffling)
      - jerry/testing/evaluation/scoring_result.py (ScoringResult)
      - jerry/testing/evaluation/criteria/ (5 agent criteria modules: ps_researcher, ps_analyst, ps_architect, ps_critic, adv_scorer)
      - jerry/testing/metamorphic/ (MR-001 through MR-005, calibration, base)
      - jerry/testing/layer4_stats.py (Layer4Pipeline)
      - jerry/testing/stats.py (shared statistical module)
      - jerry/testing/baselines/ (BaselineStore, BaselinePersistencePort)
      - jerry/testing/reports/ (ReportOutputPort, generator)
      - jerry/testing/types.py (EvaluationMode enum)
    - VALIDATION RUN outputs at:
      - projects/PROJ-036-prompt-regression-harness/work/test-harness/validation-run/
      - 5 agent outputs: ps-researcher-output.md, ps-analyst-output.md, ps-architect-output.md, ps-critic-output.md, adv-scorer-output.md
      - Phase 2 composites: phase2-composites.json (ps-researcher 0.935 PASS, ps-analyst 0.51 FAIL, ps-architect 0.86 FAIL, ps-critic 0.575 FAIL, adv-scorer 0.785 FAIL)
      - Phase 2 per-agent reports: layer2-scores-*.md (5 files)
      - Phase 3 MR smoke: layer3-mr-results.md, phase3-costs.json (all 4 MR tests FAIL at N=5)
      - Phase 4 Layer4Pipeline: phase4-results.json (ps-researcher WARNING, 4 others BLOCK)
      - Phase 4 per-agent: layer4-*.json and layer4-*.md (5 pairs)
    - DESIGNED but MISSING integration layers (the gap):
      - No pytest conftest.py with EvaluationPort fixture (FR-006 designed this pattern but it doesn't exist)
      - No pipeline orchestrator or CLI entry point to run all 4 layers
      - No promptfoo YAML test cases or Docker integration (FR-001, FR-002, FR-025)
      - No baseline persistence workflow (FR-020 baseline store exists but no CLI to populate it)
      - No PR-triggered GitHub Action (FR-002)
      - No score array collection for Layer 4 from real evaluations (FR-009)

    Classify each gap as:
      - MISSING: No implementation exists
      - PARTIAL: Building block exists but lacks caller/integration
      - BUG: Implementation exists but is broken (e.g., the AnthropicModel fix)
      - COMPLETE: Fully implemented and validated

    Output: orchestration/gap-analysis-20260307-001/ps/phase-1/ps-analyst-001/gap-inventory.md

  Phase 1B: Use /nasa-se with nse-requirements to perform requirements traceability analysis:
    - Input: projects/PROJ-036-prompt-regression-harness/design/harness-requirements.md
    - Trace each FR against:
      (a) Existing code in jerry/testing/ (forward trace: requirement -> code)
      (b) Validation run evidence (forward trace: requirement -> test evidence)
      (c) Identified gaps from Phase 1A output (gap -> requirement coverage)
    - FR coverage scope: FR-001 through FR-030 (all 30 functional requirements)
    - NFR coverage scope: NFR-001 through NFR-015 (all 15 non-functional requirements)
    - Produce a traceability matrix with columns: FR/NFR ID, Title, Status (Implemented/Partial/Missing/Blocked), Code Location, Test Evidence, Gap Reference

    Output: orchestration/gap-analysis-20260307-001/nse/phase-1/nse-requirements-001/traceability-matrix.md

  Quality gate after Phase 1: ps-critic adversarial critique >= 0.92 on both outputs.

---

Phase 2 — Code Quality Review (Fan-Out: 2 parallel agents)

  Phase 2A: Use /eng-team with eng-security to perform secure code review of:
    - jerry/testing/evaluation/deepeval_adapter.py
    - jerry/testing/evaluation/jerry_geval_deepeval_metric.py (including the AnthropicModel fix)
    - jerry/testing/evaluation/ports.py
    - jerry/testing/evaluation/debiasing.py
    - jerry/testing/layer4_stats.py
    Review dimensions:
      - Input validation on score arrays and evaluation parameters
      - Exception handling (does it catch specific exceptions or broad Exception?)
      - API key handling pattern (AnthropicModel reads ANTHROPIC_API_KEY from env)
      - Data flow from user-provided agent outputs through DeepEval to scoring
      - Dependency security (deepeval, scipy versions)

    Output: orchestration/gap-analysis-20260307-001/eng/phase-2/eng-security-001/code-review.md

  Phase 2B: Use /red-team with red-vuln to perform security assessment of:
    - API key handling surfaces:
      - ANTHROPIC_API_KEY environment variable usage in AnthropicModel wrapper
      - DeepEval's internal API key management
      - Risk of key exposure in CI/CD logs or test output files
    - Prompt injection surfaces:
      - Agent output files (*.md) are passed as actual_output to LLM-as-Judge
      - Could a malicious agent output influence G-Eval scoring?
      - DeepEval's GEval criteria parameter accepts free-text descriptions
    - Supply chain assessment:
      - deepeval package provenance and version pinning (FR-026)
      - scipy dependency for statistical functions
    - Scope: Analysis only — no active exploitation. Read-only assessment.
    - Rules of Engagement: Assessment of code paths and configurations in jerry/testing/
      for security design review purposes. No active testing against live APIs.

    Output: orchestration/gap-analysis-20260307-001/red/phase-2/red-vuln-001/security-assessment.md

  Quality gate after Phase 2: ps-critic adversarial critique >= 0.92 on both outputs.

---

Phase 3 — Adversarial Quality Validation (Sequential)

  Use /adversary with adv-scorer to score the AnthropicModel fix and DeepEvalAdapter integration
  against the S-014 LLM-as-Judge rubric (6 dimensions):
    - Input artifacts:
      - jerry/testing/evaluation/jerry_geval_deepeval_metric.py (the fix)
      - jerry/testing/evaluation/deepeval_adapter.py (the adapter)
      - Phase 2 validation evidence: phase2-composites.json showing the fix works
        (ps-researcher scored 0.935 after fix vs 0.0 before)
    - Scoring dimensions: Completeness (0.20), Internal Consistency (0.20),
      Methodological Rigor (0.20), Evidence Quality (0.15), Actionability (0.15),
      Traceability (0.10)
    - Quality threshold: >= 0.92 (C3)
    - If below threshold: produce revision recommendations

    Output: orchestration/gap-analysis-20260307-001/adversary/phase-3/adv-scorer-001/quality-score.md

  Quality gate: Score must reach >= 0.92 or escalate to human review per AE-006.

---

Phase 4 — Gap Synthesis (Sequential, depends on Phases 1-3)

  Use /problem-solving with ps-synthesizer to cross-pollinate all Phase 1-3 outputs:
    - Input artifacts:
      - Phase 1A gap inventory
      - Phase 1B traceability matrix
      - Phase 2A code review findings
      - Phase 2B security assessment
      - Phase 3 quality score
    - Synthesis tasks:
      1. Gap priority ranking: Order gaps by (a) FR priority (Must/Should/Could), (b) downstream dependency count, (c) security risk from Phase 2B
      2. Dependency mapping: Which gaps block other gaps? What must be built first?
      3. Effort estimation: Classify each gap as S/M/L/XL based on code complexity
      4. Risk assessment: Which gaps pose the highest risk if left unaddressed?
      5. Recommendation: Propose a phased implementation sequence for closing gaps

    Output: orchestration/gap-analysis-20260307-001/synthesis/phase-4/ps-synthesizer-001/gap-synthesis.md

  Quality gate after Phase 4: ps-critic adversarial critique >= 0.92.

---

Phase 5 — Work Item Creation (Sequential, depends on Phase 4)

  Use /worktracker to create work items for each identified gap:
    - For MISSING gaps: Create Enablers linked to the relevant FR items
    - For PARTIAL gaps: Create Stories describing the integration work needed
    - For BUG gaps: Create Bugs with root cause from Phase 2A/2B findings
    - All items link to parent Feature "PROJ-036 Gap Analysis: Test Harness Integration Layer"
    - All items reference the FR/NFR IDs from Phase 1B traceability matrix
    - Priority derived from Phase 4 synthesis ranking

    Output: Work items created in WORKTRACKER.md under PROJ-036

---

Phase 6 — Final Report (Sequential, depends on Phase 5)

  Use /problem-solving with ps-reporter to produce the gap analysis summary report:
    - L0: Executive summary (1 paragraph) — how many gaps, severity distribution, top 3 priorities
    - L1: Gap inventory table with FR linkage, severity, effort, and status
    - L2: Strategic implications — should the harness be extended to all 67+ agents?
      What is the minimum viable integration path? What are the risks of proceeding
      vs. waiting for full integration?
    - Include: Phase 2-4 validation results as evidence appendix

    Output: orchestration/gap-analysis-20260307-001/GAP-ANALYSIS-REPORT.md
```

---

## pe-builder Element Verification

| Element | Present | Details |
|---------|---------|---------|
| 1. Skill Routing | Yes | `/orchestration` (orch-planner), `/problem-solving` (ps-analyst, ps-synthesizer, ps-reporter), `/nasa-se` (nse-requirements), `/adversary` (adv-scorer), `/eng-team` (eng-security), `/red-team` (red-vuln), `/worktracker` |
| 2. Domain Scope | Yes | Gap between `jerry/testing/` building blocks, FR-001–FR-030, and validation-run evidence |
| 3. Data Sources | Yes | Codebase files (34 Python modules), validation outputs (29 files), requirements doc (45 FRs + NFRs) |
| 4. Quality Gate | Yes | C3 criticality, >= 0.92 per phase via ps-critic adversarial critique, S-014 rubric |
| 5. Output Path | Yes | `projects/PROJ-036-prompt-regression-harness/orchestration/gap-analysis-20260307-001/` with per-agent subdirectories |

## Orchestration Constraints

| Constraint | Value |
|------------|-------|
| Pattern | Fan-Out/Fan-In (Phases 1-2 parallel, Phases 3-6 sequential) |
| Agent execution | Background via Task tool |
| Orchestrator | Main context window |
| P-003 compliance | Single level: main context -> worker agents |
| Quality gates | After Phases 1, 2, 3, 4 |
| Criticality | C3 (auto-escalation: touches code in jerry/testing/ per AE-005) |
| Circuit breaker | Max 3 hops per H-36 |

## Validation Run Evidence Summary (for agent context)

| Agent | Phase 2 Composite | Phase 2 Verdict | Phase 4 Status | Notes |
|-------|-------------------|-----------------|----------------|-------|
| ps-researcher | 0.935 | PASS | WARNING | Above floor (0.82); synthetic baseline comparison |
| ps-analyst | 0.510 | FAIL | BLOCK | Below floor (0.85); low traceability (0.2), completeness (0.0) |
| ps-architect | 0.860 | FAIL | BLOCK | Below floor (0.88); low traceability (0.1) |
| ps-critic | 0.575 | FAIL | BLOCK | Below floor (0.83); low methodological_rigor (0.3), evidence_quality (0.0) |
| adv-scorer | 0.785 | FAIL | BLOCK | Below floor (0.90); low internal_consistency (0.2) |

Phase 3 MR smoke tests: All 4 FAIL (N=5, underpowered per ADR-001 N>=20 requirement).

## Critical Bug Fix Context

The `AnthropicModel` fix in `jerry_geval_deepeval_metric.py` resolved a root cause where DeepEval
wrapped Claude model strings in `GPTModel` (OpenAI), causing all Phase 2 scores to return 0.0.
The fix adds `_resolve_model()` that detects `"claude*"` strings and wraps them in
`from deepeval.models import AnthropicModel`. This fix is a candidate for `/adversary` C3 review
(Phase 3 of this orchestration).
