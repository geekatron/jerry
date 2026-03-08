# PROJ-036 Gap Closure: Orchestration Plan

> **Document ID:** PROJ-036-ORCH-PLAN
> **Workflow ID:** gap-closure-20260307-001
> **Date:** 2026-03-07
> **Status:** IN-PROGRESS
> **Criticality:** C2 (Standard — reversible in 1 day, < 10 files per work item, internal harness)

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Workflow Overview](#l0-workflow-overview) | Plain-language summary of what this workflow does |
| [L1: Technical Plan](#l1-technical-plan) | Diagram, phase definitions, sync barriers |
| [L2: Implementation Details](#l2-implementation-details) | State schema, path configuration, recovery |
| [Phase Status Table](#phase-status-table) | Current execution state of all phases |
| [Disclaimer](#disclaimer) | P-043 mandatory disclaimer |

---

## L0: Workflow Overview

This workflow closes the 31 gap items (CGs) identified in the gap analysis for the PROJ-036 prompt regression test harness. The gap analysis found the harness could not run end-to-end: Python modules lacked command-line entry points, security exceptions were untyped, Docker images were pinned to mutable tags, and the integration pipeline had missing components.

Five work items address these gaps in dependency order. Each work item has one or more creator agents writing code, followed by adversarial quality reviews (S-014 scoring, threshold >= 0.92). Work that scores below threshold is revised and re-reviewed, up to three iterations. After all five work items pass, a final gate runs a security re-assessment and produces the GAP-CLOSURE-SYNTHESIS-REPORT.md documenting what was fixed, the quality delta from the 0.737 baseline, and what remains deferred.

Most of the implementation is complete. The current state is: all creators have finished, most reviews have passed, and five reviews need a second pass before the final gate can open.

---

## L1: Technical Plan

### Workflow Diagram (ASCII)

```
DEPENDENCY CHAIN
BUG-036-001 (P0 Blocker)
     |
     v
STORY-036-001 (P1 Security)  <--parallel-->  STORY-036-003 (P2 Model Resolution)
     |                                              |
     +--------------------+--------------------------+
                          |
                          v
               STORY-036-002 (P2 Integration Pipeline)
                          |
                          v
               STORY-036-004 (P3 Quality Verification)
                          |
                          v
              ╔═══════════════════════════╗
              ║       FINAL GATE          ║
              ║  red-vuln + eng-reviewer  ║
              ║  Quality Gate >= 0.92     ║
              ╚═════════════╦═════════════╝
                            |
                            v
              ps-synthesizer -> GAP-CLOSURE-SYNTHESIS-REPORT.md


PHASE DETAIL (creator -> adversary -> gate -> re-review if REVISE)

Phase 1: WI1 — BUG-036-001
  Creator A (CG-001 layer4_stats): COMPLETE
  Creator B (CG-002 baselines/store): COMPLETE
  Review A: 0.883 REVISE --> revision applied --> RE-REVIEW NEEDED
  Review B: 0.975 PASS

        ╔══════════════════════════════╗
        ║  BARRIER-WI1                 ║
        ║  Both reviews >= 0.92        ║
        ║  Status: BLOCKED (Review A)  ║
        ╚══════════════════════════════╝

Phase 2: WI2 — STORY-036-001 (parallel with Phase 3)
  Creator A (CG-005 exceptions):              COMPLETE
  Creator B (CG-006/016 API key+telemetry):   COMPLETE
  Creator C (CG-017/018/025/027 validation):  COMPLETE
  Creator D (CG-007 Docker SHA):              COMPLETE
  Review A: 0.891 REVISE --> revision applied --> RE-REVIEW NEEDED
  Review B: 0.975 PASS
  Review C: 0.884 REVISE --> revision applied --> RE-REVIEW NEEDED
  Review D: 0.695 REVISE --> revision applied --> RE-REVIEW NEEDED

        ╔══════════════════════════════════╗
        ║  BARRIER-WI2                     ║
        ║  All 4 reviews >= 0.92           ║
        ║  Status: BLOCKED (A, C, D)       ║
        ╚══════════════════════════════════╝

Phase 3: WI3 — STORY-036-003 (parallel with Phase 2)
  Creator A (CG-013/023/024 model resolution): COMPLETE
  Creator B (CG-014 tests):                    COMPLETE
  Review A: 0.897 REVISE --> revision applied --> RE-REVIEW NEEDED
  Review B: 0.911 REVISE --> revision applied --> RE-REVIEW NEEDED

        ╔══════════════════════════════════╗
        ║  BARRIER-WI3                     ║
        ║  Both reviews >= 0.92            ║
        ║  Status: BLOCKED (A, B)          ║
        ╚══════════════════════════════════╝

Phase 4: WI4 — STORY-036-002
  Creator A (CG-011 conftest):          COMPLETE
  Creator B (CG-008 promptfoo extract): COMPLETE
  Creator C (CG-010 build_metric_for_mr): COMPLETE
  Creator D (CG-012 composite actions): COMPLETE
  Review A: 0.944 PASS
  Review B: 0.801 REVISE --> WI5-A unit tests close test gap
  Review C: 0.859 REVISE --> WI5-A unit tests close test gap
  Review D: 0.797 REVISE --> revision applied (outputs block, header, date) --> RE-REVIEW NEEDED

        ╔══════════════════════════════════════════╗
        ║  BARRIER-WI4                             ║
        ║  All 4 reviews >= 0.92                   ║
        ║  B, C: gate on WI5-A unit test evidence  ║
        ║  Status: BLOCKED (B, C, D)               ║
        ╚══════════════════════════════════════════╝

Phase 5: WI5 — STORY-036-004
  Creator A (unit tests):            COMPLETE (53 tests, all pass)
  Creator B (integration tests):     COMPLETE (6 new tests, all pass)
  Creator C (dependency governance): COMPLETE (deepeval narrowed, scipy added, pip-audit added)
  Review A: NEEDS ADVERSARY REVIEW
  Review B: NEEDS ADVERSARY REVIEW
  Review C: NEEDS ADVERSARY REVIEW

        ╔══════════════════════════════════╗
        ║  BARRIER-WI5                     ║
        ║  All 3 reviews >= 0.92           ║
        ║  Status: BLOCKED (all 3 pending) ║
        ╚══════════════════════════════════╝

Phase 6: FINAL GATE
  red-vuln security re-assessment: NOT STARTED
  eng-reviewer final review:        NOT STARTED
  pe-builder + ps-synthesizer:      NOT STARTED

        ╔══════════════════════════════════╗
        ║  BARRIER-FINAL                   ║
        ║  red-vuln + eng-reviewer done    ║
        ║  pe-scorer >= 90 on synth prompt ║
        ║  Status: NOT STARTED             ║
        ╚══════════════════════════════════╝

        --> GAP-CLOSURE-SYNTHESIS-REPORT.md
```

### Pipeline Definitions

| Phase | Work Item | Priority | Creator Agents | CG Items | Barrier Status |
|-------|-----------|----------|----------------|----------|----------------|
| 1 | BUG-036-001 | P0 Blocker | eng-backend (A, B) | CG-001, CG-002 | BLOCKED — Review A re-review pending |
| 2 | STORY-036-001 | P1 Critical | eng-security (A), eng-backend (B, C), eng-infra (D) | CG-005, CG-006, CG-007, CG-016, CG-017, CG-018, CG-025, CG-027 | BLOCKED — Reviews A, C, D re-review pending |
| 3 | STORY-036-003 | P2 High | eng-backend (A, B) | CG-013, CG-014, CG-023, CG-024 | BLOCKED — Reviews A, B re-review pending |
| 4 | STORY-036-002 | P2 High | eng-backend (A, B, C, D) | CG-008, CG-010, CG-011, CG-012 | BLOCKED — Reviews B, C (WI5 evidence), D re-review pending |
| 5 | STORY-036-004 | P3 Medium | eng-qa (A, B), eng-backend (C) | CG-019–CG-022, CG-026, CG-028–CG-030 | BLOCKED — All 3 adversary reviews not started |
| 6 | FINAL GATE | — | red-vuln, eng-reviewer, ps-synthesizer | — | NOT STARTED |

### Sync Barriers

| Barrier ID | Phase Gate | Triggering Condition | Quality Threshold | Status |
|------------|------------|----------------------|-------------------|--------|
| BARRIER-WI1 | Phase 1 complete | Both Review A and Review B >= 0.92 | 0.92 | BLOCKED |
| BARRIER-WI2 | Phase 2 complete | All 4 reviews (A, B, C, D) >= 0.92 | 0.92 | BLOCKED |
| BARRIER-WI3 | Phase 3 complete | Both Review A and Review B >= 0.92 | 0.92 | BLOCKED |
| BARRIER-WI4 | Phase 4 complete | All 4 reviews (A, B, C, D) >= 0.92; B and C gate on WI5-A unit test evidence | 0.92 | BLOCKED |
| BARRIER-WI5 | Phase 5 complete | All 3 reviews (A, B, C) >= 0.92 AND all tests pass | 0.92 | BLOCKED |
| BARRIER-FINAL | Final gate complete | red-vuln done; eng-reviewer done; pe-scorer >= 90 | 0.92 / 90 | NOT STARTED |

---

## L2: Implementation Details

### State Schema (ORCHESTRATION.yaml)

```yaml
workflow:
  id: "gap-closure-20260307-001"
  name: "PROJ-036 Gap Closure Execution"
  status: "IN_PROGRESS"
  date: "2026-03-07"
  project: "PROJ-036-prompt-regression-harness"

paths:
  base: "orchestration/gap-closure-20260307-001/"
  reviews: "{base}reviews/"
  adversary_wi1: "{base}adversary/bug-036-001/"
  adversary_wi2: "{base}adversary/story-036-001/"
  adversary_wi3: "{base}adversary/story-036-003/"
  adversary_wi4: "{base}adversary/story-036-002/"
  adversary_wi5: "{base}adversary/story-036-004/"
  red_final: "{base}red/final/red-vuln-001/"
  eng_final: "{base}eng/final/eng-reviewer-001/"
  synthesis: "{base}GAP-CLOSURE-SYNTHESIS-REPORT.md"

pipelines:
  wi1:
    id: "bug-036-001"
    label: "BUG-036-001 Missing __main__ entry points"
    priority: "P0 Blocker"
    dependency: none
    creators:
      A: { cg: "CG-001", file: "jerry/testing/layer4_stats.py", agent: "eng-backend", status: "complete" }
      B: { cg: "CG-002", file: "jerry/testing/baselines/store.py", agent: "eng-backend", status: "complete" }
    reviews:
      A: { creator: "A", score: 0.883, verdict: "REVISE", iteration: 1, status: "revision-applied-re-review-needed" }
      B: { creator: "B", score: 0.975, verdict: "PASS", iteration: 1, status: "passed" }

  wi2:
    id: "story-036-001"
    label: "STORY-036-001 Security hardening"
    priority: "P1 Critical"
    dependency: wi1
    creators:
      A: { cg: "CG-005", file: "jerry/testing/evaluation/exceptions.py + deepeval_adapter.py + jerry_geval_deepeval_metric.py", agent: "eng-security", status: "complete" }
      B: { cg: "CG-006, CG-016", file: "jerry/testing/evaluation/deepeval_adapter.py + .env.example + 3 workflow files", agent: "eng-backend", status: "complete" }
      C: { cg: "CG-017, CG-018, CG-025, CG-027", file: "jerry/testing/evaluation/deepeval_adapter.py + layer4_stats.py + baselines/store.py", agent: "eng-backend", status: "complete" }
      D: { cg: "CG-007", file: ".github/workflows/prompt-regression-*.yml (3 files)", agent: "eng-infra", status: "complete" }
    reviews:
      A: { creator: "A", score: 0.891, verdict: "REVISE", iteration: 1, status: "revision-applied-re-review-needed", fix: "EvaluationConfigError replaces EnvironmentError in __post_init__" }
      B: { creator: "B", score: 0.975, verdict: "PASS", iteration: 1, status: "passed" }
      C: { creator: "C", score: 0.884, verdict: "REVISE", iteration: 1, status: "revision-applied-re-review-needed", fix: "is_relative_to() replaces startswith() for CG-025 path check" }
      D: { creator: "D", score: 0.695, verdict: "REVISE", iteration: 1, status: "revision-applied-re-review-needed", fix: "Version-pinned tags applied; placeholder digest acknowledged as blocked on Docker env" }

  wi3:
    id: "story-036-003"
    label: "STORY-036-003 Model resolution quality gate compliance (RFA)"
    priority: "P2 High"
    dependency: wi1
    parallel_with: wi2
    creators:
      A: { cg: "CG-013, CG-023, CG-024", file: "jerry/testing/evaluation/jerry_geval_deepeval_metric.py", agent: "eng-backend", status: "complete" }
      B: { cg: "CG-014", file: "tests/prompt-regression/unit/test_resolve_model.py", agent: "eng-backend", status: "complete" }
    reviews:
      A: { creator: "A", score: 0.897, verdict: "REVISE", iteration: 1, status: "revision-applied-re-review-needed", fix: "Case-insensitive Bedrock check documented; Bedrock guard comment added" }
      B: { creator: "B", score: 0.911, verdict: "REVISE", iteration: 1, status: "revision-applied-re-review-needed", fix: "CG-014 ref added to module docstring; require_debiasing=False comment added" }

  wi4:
    id: "story-036-002"
    label: "STORY-036-002 Integration pipeline"
    priority: "P2 High"
    dependency: wi1
    creators:
      A: { cg: "CG-011", file: "tests/prompt-regression/conftest.py", agent: "eng-backend", status: "complete" }
      B: { cg: "CG-008", file: "jerry/testing/extraction/promptfoo_extractor.py + __init__.py", agent: "eng-backend", status: "complete" }
      C: { cg: "CG-010", file: "jerry/testing/evaluation/deepeval_adapter.py (build_metric_for_mr)", agent: "eng-backend", status: "complete" }
      D: { cg: "CG-012", file: ".github/actions/cost-monitor/action.yml + .github/actions/artifact-publish/action.yml", agent: "eng-backend", status: "complete" }
    reviews:
      A: { creator: "A", score: 0.944, verdict: "PASS", iteration: 1, status: "passed" }
      B: { creator: "B", score: 0.801, verdict: "REVISE", iteration: 1, status: "test-gap-closed-by-wi5a", note: "Unit tests in WI5-A cover the evidence gap; re-score after WI5 completes" }
      C: { creator: "C", score: 0.859, verdict: "REVISE", iteration: 1, status: "test-gap-closed-by-wi5a", note: "Unit tests in WI5-A cover the evidence gap; re-score after WI5 completes" }
      D: { creator: "D", score: 0.797, verdict: "REVISE", iteration: 1, status: "revision-applied-re-review-needed", fix: "outputs block added, header corrected, date flag fixed to POSIX, halting behavior corrected" }

  wi5:
    id: "story-036-004"
    label: "STORY-036-004 Quality verification + dependency governance"
    priority: "P3 Medium"
    dependency: "wi1, wi2, wi3, wi4"
    creators:
      A: { cg: "CG-019–CG-022, CG-026", file: "tests/prompt-regression/unit/", agent: "eng-qa", status: "complete", evidence: "53 tests, all pass" }
      B: { cg: "CG-026", file: "tests/prompt-regression/integration/", agent: "eng-qa", status: "complete", evidence: "6 new tests, all pass; 3 pre-existing fixed" }
      C: { cg: "CG-028, CG-029, CG-030", file: "pyproject.toml + .github/workflows/prompt-regression-smoke.yml", agent: "eng-backend", status: "complete", evidence: "deepeval narrowed to >=3.8.0,<4.0.0; scipy added; pip-audit step added" }
    reviews:
      A: { creator: "A", score: null, verdict: "PENDING", status: "adversary-review-not-started" }
      B: { creator: "B", score: null, verdict: "PENDING", status: "adversary-review-not-started" }
      C: { creator: "C", score: null, verdict: "PENDING", status: "adversary-review-not-started" }

  final_gate:
    id: "final-gate"
    label: "Final Gate: Security Re-Assessment + Cross-Synthesis"
    dependency: "wi1, wi2, wi3, wi4, wi5"
    steps:
      red_vuln: { agent: "red-vuln", output: "{paths.red_final}security-reassessment.md", status: "NOT_STARTED" }
      eng_reviewer: { agent: "eng-reviewer", output: "{paths.eng_final}final-review.md", status: "NOT_STARTED" }
      pe_builder: { agent: "pe-builder", purpose: "construct synthesis prompt; pe-scorer >= 90", status: "NOT_STARTED" }
      ps_synthesizer: { agent: "ps-synthesizer", output: "{paths.synthesis}", status: "NOT_STARTED" }

quality:
  threshold: 0.92
  criticality: "C2"
  scoring_mechanism: "S-014"
  required_strategies:
    - "S-007 Constitutional AI Critique"
    - "S-002 Devil's Advocate"
    - "S-014 LLM-as-Judge"
  optional_strategies:
    - "S-003 Steelman Technique"
    - "S-010 Self-Refine"
  phase_scores:
    wi1:
      review_a: 0.883
      review_b: 0.975
    wi2:
      review_a: 0.891
      review_b: 0.975
      review_c: 0.884
      review_d: 0.695
    wi3:
      review_a: 0.897
      review_b: 0.911
    wi4:
      review_a: 0.944
      review_b: 0.801
      review_c: 0.859
      review_d: 0.797
    wi5:
      review_a: null
      review_b: null
      review_c: null
  barrier_scores: {}
  workflow_quality: {}

metrics:
  phases_total: 6
  agents_total: 9
  barriers_total: 6
  work_items_active: 5
  work_items_deferred: 3
  cg_items_active: 27
  cg_items_deferred: 7
  cg_items_pre_complete: 1
```

### Phase Status Table

| Work Item | Phase | Creators Done | Reviews | Barrier | Next Action |
|-----------|-------|---------------|---------|---------|-------------|
| BUG-036-001 | 1 | A: done, B: done | A: 0.883 REVISE (rev1 applied), B: 0.975 PASS | BLOCKED | Re-review A (layer4_stats) |
| STORY-036-001 | 2 | A-D: all done | A: 0.891 REVISE (rev1 applied), B: 0.975 PASS, C: 0.884 REVISE (rev1 applied), D: 0.695 REVISE (rev1 applied) | BLOCKED | Re-review A (exceptions), C (input validation), D (Docker) |
| STORY-036-003 | 3 | A-B: all done | A: 0.897 REVISE (rev1 applied), B: 0.911 REVISE (rev1 applied) | BLOCKED | Re-review A (model resolution), B (test_resolve_model) |
| STORY-036-002 | 4 | A-D: all done | A: 0.944 PASS, B: 0.801 REVISE (WI5 coverage), C: 0.859 REVISE (WI5 coverage), D: 0.797 REVISE (rev1 applied) | BLOCKED | Re-review D (CI actions); B+C gate on WI5-A evidence |
| STORY-036-004 | 5 | A-C: all done | A: PENDING, B: PENDING, C: PENDING | BLOCKED | Launch all 3 adversary reviews |
| FINAL GATE | 6 | — | — | NOT STARTED | Wait for all WIs to pass >= 0.92 |

**Legend:** rev1 = revision applied after first REVISE verdict; PASS = score >= 0.92; REVISE = score < 0.92.

### Re-Review Action Queue (Current Blockers)

The following adversary re-reviews are needed before the final gate can open. Launch in the order shown; items within the same group may run in parallel.

#### Group A — Can start now (revisions already applied)

| Re-Review ID | Work Item | Creator | CGs | Previous Score | Revision Applied | Validation Command |
|---|---|---|---|---|---|---|
| RE-WI1-A | BUG-036-001 | Creator A (layer4_stats) | CG-001 | 0.883 | Traceability citations added to main() | `uv run python -m jerry.testing.layer4_stats --help` |
| RE-WI2-A | STORY-036-001 | Creator A (exceptions) | CG-005 | 0.891 | EvaluationConfigError replaces EnvironmentError in __post_init__ | `uv run python -c "from jerry.testing.evaluation.exceptions import EvaluationConfigError, EvaluationAPIError, EvaluationScoringError"` |
| RE-WI2-C | STORY-036-001 | Creator C (validation) | CG-017/018/025/027 | 0.884 | is_relative_to() fix applied for CG-025 | `uv run python -c "from jerry.testing.evaluation.deepeval_adapter import DeepEvalAdapter"` |
| RE-WI2-D | STORY-036-001 | Creator D (Docker) | CG-007 | 0.695 | Version-pinned tags in place; placeholder digest documented as pending Docker env | Review SHA format in workflow files |
| RE-WI3-A | STORY-036-003 | Creator A (model resolution) | CG-013/023/024 | 0.897 | Case-insensitive Bedrock check documented | `uv run python -c "from jerry.testing.evaluation.jerry_geval_deepeval_metric import JerryGEvalDeepEvalMetric"` |
| RE-WI3-B | STORY-036-003 | Creator B (test_resolve_model) | CG-014 | 0.911 | CG-014 ref + debiasing comment added | `uv run pytest tests/prompt-regression/unit/test_resolve_model.py -v` |
| RE-WI4-D | STORY-036-002 | Creator D (CI actions) | CG-012 | 0.797 | outputs block added, header corrected, date format fixed | Check action.yml files parse as valid YAML |

#### Group B — Can start now (WI5 creators complete)

| Re-Review ID | Work Item | Creator | CGs | Previous Score | Gate Condition | Validation Command |
|---|---|---|---|---|---|---|
| ADV-WI5-A | STORY-036-004 | Creator A (unit tests) | CG-019–022, CG-026 | N/A (first review) | All 53 unit tests pass | `uv run pytest tests/prompt-regression/unit/ -v --tb=short` |
| ADV-WI5-B | STORY-036-004 | Creator B (integration tests) | CG-026 | N/A (first review) | All 9 integration tests pass | `uv run pytest tests/prompt-regression/integration/ -v --tb=short` |
| ADV-WI5-C | STORY-036-004 | Creator C (dependency governance) | CG-028/029/030 | N/A (first review) | `uv sync` succeeds | `uv sync` |

#### Group C — Gate on WI5-A passing (unit test evidence closes the test gap)

| Re-Review ID | Work Item | Creator | CGs | Previous Score | Gate Condition |
|---|---|---|---|---|---|
| RE-WI4-B | STORY-036-002 | Creator B (promptfoo extractor) | CG-008 | 0.801 | WI5-A adversary review PASS (unit tests cover evidence gap) |
| RE-WI4-C | STORY-036-002 | Creator C (build_metric_for_mr) | CG-010 | 0.859 | WI5-A adversary review PASS (unit tests cover evidence gap) |

### Quality Gate Definitions

| Gate | At Barrier | Criticality | Threshold | Strategy | Max Iterations |
|------|------------|-------------|-----------|----------|----------------|
| Per-creator adversary review | Each creator exit | C2 | >= 0.92 | S-014 LLM-as-Judge (6 dimensions) | 3 per H-14 |
| Synthesis prompt quality | Before ps-synthesizer | C2 | pe-scorer >= 90 | 7-criterion rubric | 3 iterations with pe-builder |
| Security re-assessment | BARRIER-FINAL | C2 | Pass/fail delta vs Phase 2B baseline | S-001 Red Team Analysis | 1 |
| Final architecture review | BARRIER-FINAL | C2 | H-07, H-20 compliance | eng-reviewer checklist | 1 |

**S-014 Scoring Dimensions (per quality-enforcement.md SSOT):**

| Dimension | Weight |
|-----------|--------|
| Completeness | 0.20 |
| Internal Consistency | 0.20 |
| Methodological Rigor | 0.20 |
| Evidence Quality | 0.15 |
| Actionability | 0.15 |
| Traceability | 0.10 |

### Dynamic Path Configuration

All artifact paths use dynamic identifiers derived from the workflow ID. No hardcoded pipeline names.

| Path Type | Pattern | Example |
|-----------|---------|---------|
| Base | `orchestration/{workflow.id}/` | `orchestration/gap-closure-20260307-001/` |
| Reviews | `{base}reviews/adv-{wi-id}-{cg-slug}-score.md` | `orchestration/gap-closure-20260307-001/reviews/adv-wi2a-cg005-score.md` |
| Adversary (per WI) | `{base}adversary/{work-item-id}/` | `orchestration/gap-closure-20260307-001/adversary/story-036-001/` |
| Red team final | `{base}red/final/red-vuln-001/security-reassessment.md` | |
| Eng review final | `{base}eng/final/eng-reviewer-001/final-review.md` | |
| Synthesis | `{base}GAP-CLOSURE-SYNTHESIS-REPORT.md` | |

### Deferred and Out-of-Scope Items

| Item | Status | Reason |
|------|--------|--------|
| STORY-036-005 (P4 docs): CG-015, CG-031–CG-034 | Deferred | Out of scope for this execution; follow-up prompt required |
| BUG-036-002 / CG-004 (API key on disk) | Deferred | User decision: deferred until key manager available |
| CG-009 (baseline population) | Deferred | Deferred until pipeline validated end-to-end |
| CG-003 (field name mismatch) | Pre-complete | Already fixed in .github/workflows/ prior to this execution |

### Recovery Strategies

| Failure Mode | Recovery Action |
|---|---|
| Re-review scores below 0.92 after revision (iteration 2) | Creator applies targeted fix from adv-scorer findings; launch iteration 3 adversary review. At iteration 3 with no improvement: escalate to user per H-14. |
| WI5-A unit tests fail | eng-qa Creator A revises failing tests; re-run uv run pytest; relaunch ADV-WI5-A. |
| WI5-B integration tests fail | eng-qa Creator B investigates failure against conftest evaluator fixture; revise tests or underlying adapter; relaunch ADV-WI5-B. |
| WI2-D Docker placeholder digest blocked | Document final scoring state; note CG-007 remains structurally complete but operationally blocked; include in synthesis report remaining-risk register. Consider conditional PASS at reviewer discretion per blocker justification. |
| red-vuln finds new high-severity finding | Escalate to user; create new work item before synthesis; update FEAT-036-003. |
| ps-synthesizer synthesis prompt pe-scorer < 90 | pe-builder iterates with pe-scorer until threshold reached (max 3 iterations). |
| pe-scorer cannot reach 90 after 3 iterations | Escalate to user per H-31 before executing synthesis. |

---

## Disclaimer

This orchestration plan was generated by orch-planner agent (v2.2.0) on 2026-03-07. It reflects the current execution state of workflow `gap-closure-20260307-001` as of the document date. Phase status is accurate as of session authoring and must be updated by orch-tracker as re-reviews complete. Human review of re-review outcomes and final gate results is required before marking FEAT-036-003 as complete.

All adversarial quality scores are produced by adv-scorer using the S-014 LLM-as-Judge rubric with the quality threshold established in `.context/rules/quality-enforcement.md` (H-13: >= 0.92 for C2+ deliverables). Score records are persisted to the orchestration review paths above for audit traceability.

**P-043 Notice:** This document is an internal Jerry Framework orchestration artifact. It does not constitute official project approval or release authorization. Execution of the remaining re-reviews and final gate requires human orchestrator oversight.
