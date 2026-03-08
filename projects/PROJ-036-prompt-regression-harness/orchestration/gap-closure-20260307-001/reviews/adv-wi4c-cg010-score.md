# Quality Score Report: CG-010 — build_metric_for_mr() Adapter Method

## L0 Executive Summary

**Score:** 0.859/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.72)
**One-line assessment:** The method is correctly implemented and internally coherent, but it lacks unit tests, leaves the G-Eval-as-proxy rationale undocumented, and does not document the conceptual mismatch between the MR evaluation contract (transform + evaluate score sequences) and the G-Eval scoring contract (judge a single LLM output) — gaps that reduce evidence quality, methodological rigor, and traceability.

---

## Scoring Context

- **Deliverable:** `jerry/testing/evaluation/deepeval_adapter.py` — `build_metric_for_mr()` method (lines 225–311), added for CG-010
- **Deliverable Type:** Code (adapter method, gap closure)
- **Criticality Level:** C2 (Standard — reversible within 1 day, single file)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T00:00:00Z
- **Prior Score:** None (first scoring)
- **Strategy Findings Incorporated:** No

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.859 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.87 | 0.174 | Method present, signature correct, guards present, but no unit tests exist |
| Internal Consistency | 0.20 | 0.95 | 0.190 | Method aligns with build_metric_for_agent() pattern; attribute access consistent with MR ABC |
| Methodological Rigor | 0.20 | 0.85 | 0.170 | Follows established adapter pattern; one semantic mismatch (MR contract vs G-Eval contract) undocumented |
| Evidence Quality | 0.15 | 0.72 | 0.108 | No tests exist; criterion rubric text is plausible but its adequacy is asserted not demonstrated |
| Actionability | 0.15 | 0.88 | 0.132 | Return type is JerryGEvalDeepEvalMetric, method is callable; downstream use (conftest CG-011) is clear |
| Traceability | 0.10 | 0.85 | 0.085 | FR-010, FR-021, CG-010 cited; gap-inventory IL-4 matched; design decision (why G-Eval for MR?) not traced |
| **TOTAL** | **1.00** | | **0.859** | |

**Computed composite (verified):** 0.174 + 0.190 + 0.170 + 0.108 + 0.132 + 0.085 = **0.859**

---

## Detailed Dimension Analysis

### Completeness (0.87/1.00)

**Evidence:**

The method is present, with the correct signature `build_metric_for_mr(self, mr: MetamorphicRelation, quality_floor: float | None = None) -> JerryGEvalDeepEvalMetric` (line 225). The input validation guards are both present and correct: `if not mr.mr_id` (line 272) and `if not mr.mr_name` (line 277) each raise `ValueError` with messages that cite the class attribute contract. The `QualityCriterion` is constructed from MR attributes (lines 285–297). `JerryGEvalMetric` is built with `require_debiasing=True` (line 303), satisfying C-007/FR-021. `JerryGEvalDeepEvalMetric` is returned (line 306).

The method satisfies the literal CG-010 specification from `gap-closure-prompt.md`: "Add `build_metric_for_mr(mr: MetamorphicRelation) -> JerryGEvalDeepEvalMetric` to DeepEvalAdapter."

The docstring includes an inline usage example (lines 257–265) matching the review validation check from the gap-closure prompt: `uv run python -c "from jerry.testing.evaluation.deepeval_adapter import DeepEvalAdapter; hasattr(DeepEvalAdapter, 'build_metric_for_mr')"`.

**Gaps:**

1. No unit tests exist anywhere in the codebase for `build_metric_for_mr()`. The test file `tests/prompt-regression/unit/test_layer2_evaluation.py` does not import or test this method. `grep` across the entire `tests/` directory returns zero matches for `build_metric_for_mr` or `CG.010`. H-20 mandates 90% line coverage; lines 225–311 are entirely uncovered.

2. The `evaluate()` method (lines 313–363) on `DeepEvalAdapter` raises `NotImplementedError` by design and is noted as partially blocking FR-006. `build_metric_for_mr` adds to this partial picture — CG-011 (conftest fixture) depends on the adapter being wirable, and the new method is needed for that step. The completeness of CG-010 is therefore structural but integration-untested.

**Improvement Path:**

Add unit tests covering: (a) happy-path metric construction with a stub MR, (b) `ValueError` on empty `mr_id`, (c) `ValueError` on empty `mr_name`, (d) `quality_floor=None` defaults to `self.default_threshold`, (e) `quality_floor` override propagates to returned metric's `threshold`. This would raise the score to 0.92+.

---

### Internal Consistency (0.95/1.00)

**Evidence:**

The implementation is internally consistent across multiple dimensions:

1. **Pattern consistency with `build_metric_for_agent()`**: Both methods follow the identical three-step pattern — (a) compute threshold from `quality_floor` or `self.default_threshold`, (b) construct `JerryGEvalMetric` with `require_debiasing=True`, (c) return `JerryGEvalDeepEvalMetric`. The parallel structure is exact.

2. **Attribute access consistency**: `mr.mr_id` and `mr.mr_name` are both declared as class attributes in `MetamorphicRelation` (base.py lines 159–160). The method accesses them via instance, which is correct Python; class attributes are accessible on instances.

3. **`agent_name` field usage**: `agent_name=mr.mr_id` (line 303) is passed to `JerryGEvalMetric`. This is a reasonable mapping — the field is used for logging and labeling per the `build_metric_for_agent()` docstring. Using `mr_id` (e.g., `"MR-001"`) as the agent name label is unconventional but not contradictory.

4. **Weight consistency**: `weight=1.0` (line 294) is documented in the docstring: "the single criterion weight is 1.0 (only one criterion, so composite == criterion score)." This is mathematically correct.

5. **`dimension` field**: `dimension=mr.mr_id` (line 296) maps the `QualityCriterion.dimension` field to the MR identifier. `QualityCriterion.dimension` is typed `str | None` and is documented as "The S-014 dimension this criterion maps to, or None for structural/agent-specific criteria." Using `mr_id` here is slightly outside the documented vocabulary but is not internally contradictory.

**Gaps:**

Minor: the docstring says "The metric name is `mr.mr_id`" (line 249) but `JerryGEvalDeepEvalMetric` takes `jerry_metric` not a `name` argument — the metric name as exposed to DeepEval is derived from `JerryGEvalDeepEvalMetric` internals, not directly from `mr_id`. This is a docstring precision gap, not a code contradiction.

**Improvement Path:**

Verify that `JerryGEvalDeepEvalMetric.name` property exposes `mr_id` as claimed, and if not, correct the docstring. This is a single-line clarification.

---

### Methodological Rigor (0.85/1.00)

**Evidence:**

The method follows the established adapter pattern documented in `base.py` (lines 37–43): "The adapter layer (jerry.testing.evaluation.deepeval_adapter) wraps each MetamorphicRelation subclass in a thin DeepEval BaseMetric adapter." The pattern is correctly implemented: domain type (`MetamorphicRelation`) is received, domain infrastructure types are constructed (`QualityCriterion`, `JerryGEvalMetric`), and the DeepEval-coupled return type is produced.

Input validation guards are appropriate: empty `mr_id` and empty `mr_name` are both rejected with informative error messages. The `require_debiasing=True` enforcement matches the C-007 mandatory debiasing requirement documented in the module-level docstring.

**Gaps:**

One significant conceptual mismatch is present but undocumented:

The `MetamorphicRelation` contract (`base.py`) involves: (1) `transform(input_text)` to produce a variant prompt, (2) running the agent N times on both original and transformed inputs, (3) `evaluate(original_scores, transformed_scores)` to compute an `MRResult`. This is a population-level statistical test requiring N >= 20 paired samples.

The `build_metric_for_mr()` method produces a `JerryGEvalDeepEvalMetric`, which invokes G-Eval on a single `LLMTestCase` — a single LLM output judged by a natural-language rubric. The produced metric asks a G-Eval judge "does this output satisfy the MR invariant?" rather than running the statistical MR evaluation protocol.

This is a valid design choice (using G-Eval as a proxy signal for MR quality gating at the pytest level, rather than running the full N=30 statistical protocol), but the method does not document this choice, its rationale, or its limitations. The gap-inventory (IL-4) only notes the wrapping was missing; the system-design.md reference to "wrapping MetamorphicRelation subclasses in BaseMetric adapter" does not specify that the wrapping should use G-Eval rather than executing the MR statistical protocol. Without a documented rationale, a reader cannot verify whether this is the intended design or a simplification.

**Improvement Path:**

Add a design note to the method docstring explaining: (a) this method uses G-Eval as a quality signal proxy rather than the full MR statistical evaluation protocol; (b) the full MR evaluation protocol (`mr.transform()` + `mr.evaluate()`) is used when directly computing `MRResult` for statistical purposes (Layer 3); (c) the G-Eval path is appropriate for pytest-level quality gating on individual responses. This documentation would raise methodological rigor to 0.92+.

---

### Evidence Quality (0.72/1.00)

**Evidence:**

The implementation includes an inline example demonstrating usage with `ParaphraseConsistency()` (lines 257–265). The module-level docstring traces mandatory debiasing to FR-021 and C-007. The method-level references section cites CG-010, FR-010, and FR-021.

The criterion `description` string (lines 287–296) is plausible natural language for a G-Eval rubric, but its adequacy is asserted rather than demonstrated. There is no evidence that this rubric has been validated against actual MR test cases or that the resulting G-Eval scores correlate with the statistical MR evaluation outcomes from `mr.evaluate()`.

**Gaps:**

1. **Zero test coverage.** No unit tests for `build_metric_for_mr()` exist anywhere in the codebase. This is the single largest evidence gap. For a method claiming to bridge two layers of the harness architecture, the absence of tests means there is no executable evidence of correctness.

2. **Criterion rubric is unvalidated.** The rubric text "Score 1.0 if the response would receive a similar quality assessment regardless of the transformation; score 0.0 if the transformation produces a meaningfully different output quality" (lines 291–296) is logically reasonable but untested. There is no evidence (validation run output, unit test, or design rationale) that an LLM judge would score this criterion in a way that is aligned with actual MR pass/fail outcomes.

3. **Absence of review artifacts.** Other CG closures in the same orchestration (e.g., CG-006/016 scored 0.975, CG-005 scored separately) have review artifacts in `orchestration/gap-closure-20260307-001/reviews/`. This is the first scoring for CG-010; no prior review exists to validate.

**Improvement Path:**

At minimum: add unit tests with a stub/mock `MetamorphicRelation` that confirms method behavior for both valid and invalid inputs. For stronger evidence: add an integration test or validation note documenting how the G-Eval rubric performs against a known-good MR case.

---

### Actionability (0.88/1.00)

**Evidence:**

The method returns `JerryGEvalDeepEvalMetric`, which is a `BaseMetric` subclass. It is directly usable via `deepeval.assert_test(test_case, [metric])` as shown in the docstring example. The gap-closure prompt specifies CG-011 depends on CG-010 ("conftest fixture wiring"); this method provides the specific entry point CG-011 requires.

The `quality_floor` parameter with a `None` default correctly falls back to `self.default_threshold`, matching `build_metric_for_agent()` behavior. This is the correct actionable API for callers that want to use a per-MR threshold override.

**Gaps:**

The method does not document how the returned metric connects to the `mr.transform()` / `mr.evaluate()` workflow — specifically, whether a caller should call `build_metric_for_mr()` instead of or in addition to running the full MR evaluation. A caller using this method for the first time will need to understand the distinction (G-Eval proxy vs. full statistical protocol) to use it correctly. This is a usability gap that slightly reduces actionability.

**Improvement Path:**

Add a "When to use this method vs. mr.evaluate() directly" note to the docstring, or a cross-reference to the system design section that explains the two-path MR evaluation strategy.

---

### Traceability (0.85/1.00)

**Evidence:**

The method references section cites: CG-010 (the gap closure ID), FR-010 (Five Universal Metamorphic Relations), and FR-021 (mandatory debiasing). The module-level docstring references FR-006, FR-007, FR-009, and FR-021 with design document section numbers. The comment `# CG-010` on line 225 tags the addition to the gap item.

The gap-inventory (gap-inventory.md, item 34, IL-4) identifies the specific missing adapter: "DeepEvalAdapter has no `build_metric_for_mr()` method; MR classes cannot be passed to `deepeval.assert_test()` without a wrapping adapter." This implementation directly addresses that inventory item.

**Gaps:**

1. The gap-synthesis (gap-synthesis.md, line 128) also cross-references `GAP-L3-BASECLASS` as an identifier for this gap. This identifier does not appear in the implementation or its docstring — a minor traceability chain break.

2. The system-design.md reference cited in `base.py` ("The adapter layer...wraps each MetamorphicRelation subclass in a thin DeepEval BaseMetric adapter" — system-design.md Section 4 and §1.4) is not cited in `build_metric_for_mr()`. The method cites FR-010 but not the system design section that mandated the adapter pattern.

3. The design decision to use G-Eval (a single-output quality signal) rather than the MR statistical evaluation protocol has no traceable design record. There is no ADR, no comment, and no design document reference explaining why G-Eval was chosen for this bridge.

**Improvement Path:**

Add a `system-design.md §1.4` reference to the method docstring. Add a comment or docstring note explaining the design choice to use G-Eval as the MR proxy evaluation mechanism, with a reference to the relevant system design section or an inline justification.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.72 | 0.90 | Add unit tests for `build_metric_for_mr()`: happy path with stub MR, ValueError on empty `mr_id`, ValueError on empty `mr_name`, `quality_floor=None` defaults to `default_threshold`, `quality_floor` override propagates. Add to `tests/prompt-regression/unit/test_layer2_evaluation.py`. |
| 2 | Methodological Rigor | 0.85 | 0.92 | Document the G-Eval-as-proxy design decision in the method docstring: explain that `build_metric_for_mr()` uses G-Eval for pytest-level quality gating on individual responses (not the full statistical MR protocol), and when each path is appropriate. |
| 3 | Traceability | 0.85 | 0.92 | Add `system-design.md §1.4` citation to the method's References block. Add `GAP-L3-BASECLASS` to the gap reference comment or tracing note. Add an inline rationale for the G-Eval proxy approach (can be brief — one sentence citing the design intent). |
| 4 | Completeness | 0.87 | 0.92 | The test gap (Priority 1) is the primary completeness gap. Additionally verify that `JerryGEvalDeepEvalMetric.name` exposes `mr_id` as the docstring claims. |
| 5 | Actionability | 0.88 | 0.92 | Add a brief note distinguishing `build_metric_for_mr()` (G-Eval single-output quality gate) from `mr.evaluate()` (full statistical MR protocol), so callers know which path to use. |
| 6 | Internal Consistency | 0.95 | 0.97 | Verify and tighten the docstring claim "The metric name is `mr.mr_id`" against the actual `JerryGEvalDeepEvalMetric` interface. |

---

## Leniency Bias Check

- [x] Each dimension scored independently
- [x] Evidence documented for each score — specific line numbers cited where applicable
- [x] Uncertain scores resolved downward (Evidence Quality: chose 0.72 over 0.75 given total absence of tests; Methodological Rigor: chose 0.85 over 0.88 given the undocumented conceptual mismatch)
- [x] First-draft calibration considered — this is a fresh implementation with no revision history
- [x] No dimension scored above 0.95 without exceptional evidence (Internal Consistency at 0.95 is justified by exact parallel to `build_metric_for_agent()` and consistent attribute access)

**Calibration note:** The composite of 0.859 sits in the REVISE band (0.70-0.84 range in the agent spec, 0.85-0.91 range for "near threshold" per quality-enforcement.md operational bands). The primary blocker to PASS is the complete absence of unit tests (Evidence Quality), which is not a minor gap — H-20 mandates 90% line coverage and the method spans 87 executable lines with zero coverage. The implementation quality itself (structure, guards, debiasing compliance) is strong; targeted test addition and documentation improvements would close the gap.
