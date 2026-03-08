# Quality Score Report: Stream 3B — Layer 2 DeepEval Evaluation Backend

## L0 Executive Summary

**Score:** 0.845/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Completeness (0.72)

**One-line assessment:** The Layer 2 evaluation backend is architecturally coherent and methodologically sound but fails on three concrete gaps — H-10 multiple-class-per-file violations across three modules, a missing `ports.py` module required by the system design, and a stub `evaluate()` method on `DeepEvalAdapter` that returns zeros rather than real scores — pulling the composite below the stream threshold of 0.94.

---

## Scoring Context

- **Deliverable:** `jerry/testing/evaluation/` (10 files: `__init__.py`, `metrics.py`, `debiasing.py`, `deepeval_adapter.py`, `criteria/__init__.py`, `criteria/ps_researcher.py`, `criteria/ps_analyst.py`, `criteria/ps_architect.py`, `criteria/ps_critic.py`, `criteria/adv_scorer.py`)
- **Deliverable Type:** Code (Layer 2 Implementation)
- **Criticality Level:** C4 (per system-design.md: "irreversible architecture, 67 agent definitions affected")
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Stream Threshold:** >= 0.94 (C4 elevated threshold per scoring prompt)
- **Scored:** 2026-03-07

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.845 |
| **Stream Threshold** | 0.94 (PASS) |
| **Standard H-13 Threshold** | 0.92 (PASS) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (no adv-executor reports provided) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.72 | 0.144 | H-10 violated in 3 files; `ports.py` missing; FR-007 criteria storage deviation |
| Internal Consistency | 0.20 | 0.88 | 0.176 | S-014 weights correct throughout; debiasing interface consistent; weight sums verified |
| Methodological Rigor | 0.20 | 0.90 | 0.180 | H-07 domain isolation rigorously enforced; debiasing mandatory enforcement correct |
| Evidence Quality | 0.15 | 0.88 | 0.132 | FR traceability present in docstrings; contract floor values match per-agent YAML contracts |
| Actionability | 0.15 | 0.85 | 0.128 | Modules are importable and usable; stub `evaluate()` is a partial actionability gap |
| Traceability | 0.10 | 0.85 | 0.085 | FR-006/007/008/009/021 mapped in module docstrings; H-10 deviations untraceable to design intent |
| **TOTAL** | **1.00** | | **0.845** | |

**Arithmetic verification:**
(0.72 × 0.20) + (0.88 × 0.20) + (0.90 × 0.20) + (0.88 × 0.15) + (0.85 × 0.15) + (0.85 × 0.10)
= 0.144 + 0.176 + 0.180 + 0.132 + 0.1275 + 0.085
= 0.8445 ≈ **0.845**

---

## Detailed Dimension Analysis

### Completeness (0.72/1.00)

**Evidence — what is present:**
- All 10 deliverable files exist as specified in the stream scope.
- All 5 per-agent criteria files present (`ps_researcher.py`, `ps_analyst.py`, `ps_architect.py`, `ps_critic.py`, `adv_scorer.py`).
- Each criteria file contains exactly the 6 S-014 dimensions with correct SSOT weights (0.20/0.20/0.20/0.15/0.15/0.10).
- `debiasing.py` delivers `DebiasingStrategy` and `PositionRandomizationResult`.
- `metrics.py` delivers `QualityCriterion`, `ScoringResult`, `JerryGEvalMetric`.
- `deepeval_adapter.py` delivers `JerryGEvalDeepEvalMetric` and `DeepEvalAdapter`.
- `__init__.py` correctly exports `DebiasingStrategy`, `JerryGEvalMetric`, `QualityCriterion`, `ScoringResult`.

**Gaps — concrete defects:**

**G1 (H-10 violation — metrics.py):** `metrics.py` contains 3 classes: `QualityCriterion`, `ScoringResult`, and `JerryGEvalMetric`. H-10 requires one class per file. The system design's own H-10 compliance table at §1.3 lists `evaluation/metrics.py` as responsible for "QualityCriterion, ScoringResult value objects" — not `JerryGEvalMetric`. `JerryGEvalMetric` should reside in a dedicated `jerry_geval_metric.py` file.

**G2 (H-10 violation — deepeval_adapter.py):** `deepeval_adapter.py` contains 2 classes: `JerryGEvalDeepEvalMetric` (line 81) and `DeepEvalAdapter` (line 407). The system design's H-10 compliance table lists `evaluation/deepeval_adapter.py` as responsible for "DeepEvalAdapter class" (singular). `JerryGEvalDeepEvalMetric` is a distinct class that should be in its own file (e.g., `jerry_geval_deepeval_metric.py`). The docstring on line 97 even acknowledges the tension: "H-10: One class per file — this class is the primary export of this module. But DeepEvalAdapter (below) is the public API."

**G3 (H-10 violation — debiasing.py):** `debiasing.py` contains 2 classes: `PositionRandomizationResult` (line 40) and `DebiasingStrategy` (line 73). While `PositionRandomizationResult` is a data-only dataclass that serves as a return type for `DebiasingStrategy`, H-10 is absolute — one class per file. The system design's H-10 table does not list `PositionRandomizationResult` as a separate file, suggesting this dataclass was added without updating the compliance table.

**G4 (Missing ports.py):** The system design module decomposition at §1.3 explicitly lists `evaluation/ports.py` as a `[PORT] EvaluationPort protocol` file. The dependency graph at §1.4 shows `pytest_adapter --> [evaluation/ports.py] --> DOMAIN CORE`. This file does not exist in the deliverable. The `deepeval_adapter.py` docstring references it: "The DeepEvalAdapter class implements the EvaluationPort protocol defined in jerry/testing/evaluation/ports.py." This is a documented planned module that was not implemented.

**G5 (FR-007 criteria storage deviation):** FR-007 acceptance criterion states: "G-Eval criteria definitions shall be stored as YAML or JSON files under `tests/prompt-regression/criteria/` for maintainability and version control." The implementation stores criteria as Python module constants in `criteria/*.py` files. This is an architectural deviation from the requirement — Python constants are not easily editable without code changes, which is the exact maintainability concern FR-007 is addressing. The deviation may be intentional (Python constants are type-safe and importable), but it is not documented as an accepted deviation.

**Improvement Path:**
Split `metrics.py` into `quality_criterion.py`, `scoring_result.py`, and `jerry_geval_metric.py`. Split `deepeval_adapter.py` into `jerry_geval_deepeval_metric.py` and `deep_eval_adapter.py`. Extract `PositionRandomizationResult` from `debiasing.py` into `position_randomization_result.py`. Implement `ports.py` with the `EvaluationPort` protocol. Document or resolve the FR-007 criteria storage deviation.

---

### Internal Consistency (0.88/1.00)

**Evidence — what is consistent:**
- S-014 dimension weights in `DIMENSION_WEIGHTS` constant in `metrics.py` exactly match `quality-enforcement.md` SSOT: 0.20/0.20/0.20/0.15/0.15/0.10.
- All 5 criteria files verify their own weight sums with `assert abs(_weight_sum - 1.0) < 1e-9` at module load time — this is a runtime consistency invariant.
- The `__init__.py` import `from jerry.testing.evaluation.debiasing import DebiasingStrategy` matches the class exported in `debiasing.py`.
- `JerryGEvalMetric.classify_composite()` uses thresholds >= 0.92 (PASS), >= 0.85 (REVISE), else REJECTED — consistent with `quality-enforcement.md` H-13 and all contract files (`band_thresholds.pass_minimum: 0.92`).
- `DeepEvalAdapter.default_threshold = 0.82` is consistent with the comment in `deepeval_adapter.py` ("the lowest agent floor across all five target agents") and the per-agent contracts (ps-researcher overall_floor: 0.82).
- `criteria/__init__.py` floor annotations match per-agent contract YAML: ps-researcher 0.82, ps-analyst 0.85, ps-architect 0.88, ps-critic 0.83, adv-scorer 0.90 — all verified against the contract files.
- `DebiasingStrategy.shuffle_criteria()` returns a new list (pure function), consistent with `JerryGEvalMetric.get_criteria_for_debiasing()` which calls it without mutation concerns.

**Gaps:**
- Minor: `JerryGEvalMetric.__post_init__` logs a warning when weight sum != 1.0 but uses `pass` — the comment says "Normalization applied in score_composite()" but there is a dead code path where the comment block (`if abs(weight_sum - 1.0) > 0.01: pass`) does nothing. The normalization is correctly applied in `score_composite()` by dividing by `total_weight`, so the behavior is correct, but the code structure is misleading.
- Minor: `deepeval_adapter.py` line 97 contains the acknowledgment "H-10: One class per file — this class is the primary export of this module. But DeepEvalAdapter (below) is the public API." This acknowledges the H-10 tension without resolving it, which is an internal inconsistency between the stated constraint and the implementation.

**Improvement Path:**
Replace the dead `pass` in `__post_init__` with a log warning call. Resolve the H-10 acknowledgment by splitting the classes.

---

### Methodological Rigor (0.90/1.00)

**Evidence — what is rigorous:**
- H-07 domain isolation is consistently enforced across all modules. `metrics.py`, `debiasing.py`, and all `criteria/*.py` files contain zero imports from `deepeval`, `promptfoo`, `scipy`, or `statsmodels`. The `if TYPE_CHECKING:` guard in `debiasing.py` correctly avoids circular imports while maintaining type annotations.
- C-007 mandatory debiasing enforcement is implemented at two layers: (1) `JerryGEvalMetric.__post_init__` raises `ValueError` if `require_debiasing=True` and `debiasing=None`; (2) `JerryGEvalDeepEvalMetric.__init__` re-validates the same constraint. This double-enforcement prevents debiasing bypass.
- The debiasing implementation is methodologically sound: `PositionRandomizationResult.swapped` enables correct result re-attribution after position swap; `shuffle_criteria()` returns a new list without mutating the original.
- `_evaluate_criteria()` evaluates each criterion as a separate GEval call (one criterion per GEval invocation), which prevents the LLM judge from conflating criteria in a multi-criterion prompt — this is a methodologically sound approach to per-criterion scoring.
- Weight sum assertions in all 5 criteria files (`assert abs(_weight_sum - 1.0) < 1e-9`) enforce a runtime invariant that prevents silent weight drift.
- `score_composite()` normalizes by total_weight rather than assuming sum=1.0, which handles partial criterion evaluation gracefully.
- `ScoringResult.weighted_score` is computed as an immutable derived field in `__post_init__`, preventing stale cached values.

**Gaps:**
- `evaluate()` on `DeepEvalAdapter` (lines 522-572) is a stub that logs a warning and returns `{name: 0.0 for name in criteria}`. The system design §2.2 describes `EvaluationPort.evaluate()` as the protocol method the adapter should implement. The stub means the `EvaluationPort` protocol conformance is nominal, not functional, for this method path. The comment acknowledges this: "Return stub dictionary matching the protocol signature. Callers that need real scores must use build_metric_for_agent()." This is a methodological gap: the EvaluationPort contract is not fully implemented.
- `a_measure()` uses `asyncio.get_event_loop().run_in_executor()` — `get_event_loop()` is deprecated in Python 3.10+ in favor of `asyncio.get_running_loop()`. This is a minor methodological concern for Python version compatibility.

**Improvement Path:**
Implement `evaluate()` as a real evaluation call rather than a stub, or formally deprecate it and route callers to `build_metric_for_agent()`. Replace `asyncio.get_event_loop()` with `asyncio.get_running_loop()`.

---

### Evidence Quality (0.88/1.00)

**Evidence — what is well-cited:**
- Module docstrings in all 10 files cite specific FR numbers (FR-006, FR-007, FR-008, FR-009, FR-021) and contract section references (behavioral-contracts.md §B.3, §B.4, §A.2 through §A.6).
- Per-dimension bounds in all 5 criteria files exactly match the per-agent contract YAML files. Spot checks confirmed:
  - `ps_researcher.py`: Actionability floor 0.65 matches `ps-researcher.contract.yaml` `actionability.min: 0.65`.
  - `adv_scorer.py`: Internal Consistency floor 0.90 matches `adv-scorer.contract.yaml` `internal_consistency.min: 0.90`.
  - `ps_architect.py`: Traceability floor 0.88 matches `ps-architect.contract.yaml` `traceability.min: 0.88`.
- ADR-001 references are present (`ADR-001 Forces F-5` appears in `__init__.py`, `metrics.py`, and `debiasing.py`).
- The `criteria/__init__.py` docstring cites behavioral-contracts.md §B.3 and §B.4 for per-agent floor values.
- `adv_scorer.py` cites SI-SCOR-001 through SI-SCOR-011 structural invariants that map directly to `adv-scorer.contract.yaml` structural_invariants section.

**Gaps:**
- The FR-007 deviation (criteria in Python vs. YAML/JSON) is not documented as an accepted deviation with a rationale. An evidence trail justifying the architectural deviation is absent.
- `deepeval_adapter.py` references `jerry/testing/evaluation/ports.py` in its docstring but that file does not exist — the evidence chain breaks at this reference.
- The `debiasing.py` reference to "contracts/behavioral-contracts.md §B.5" (Score stability bounds) in its module docstring is correct, but the implementation does not expose any mechanism to capture or report score stability — the reference is aspirational rather than implemented.

**Improvement Path:**
Add a design note documenting the FR-007 deviation (Python constants vs. YAML files) with explicit rationale. Implement `ports.py` so the reference in `deepeval_adapter.py` resolves. Add score stability measurement hooks or update the §B.5 reference to note it is a future concern.

---

### Actionability (0.85/1.00)

**Evidence — what is usable:**
- The core usage pattern documented in `__init__.py` is fully functional: `DebiasingStrategy()`, `JerryGEvalMetric(criteria=..., debiasing=..., agent_name=...)` are all constructable and usable.
- `DeepEvalAdapter.build_metric_for_agent()` produces a `JerryGEvalDeepEvalMetric` ready for `deepeval.assert_test()` — the primary integration path for FR-006 pytest plugin usage.
- `evaluate_batch()` implements FR-009 score array collection, returning `dict[str, list[float]]` per criterion — directly consumable by Layer 4.
- All 5 criteria constants are importable from `jerry.testing.evaluation.criteria` and are immediately usable with `JerryGEvalMetric`.
- Constructor-time validation (empty criteria, missing debiasing, invalid weights, invalid score ranges) provides actionable error messages with FR references and remediation guidance.

**Gaps:**
- `DeepEvalAdapter.evaluate()` returns stub scores (all 0.0) with a warning log. Any caller following the `EvaluationPort` protocol by invoking `evaluate()` for programmatic single-shot evaluation receives non-functional results. This reduces actionability for that usage path.
- `evaluate_batch()` only collects composite scores, not per-criterion scores, despite the method signature suggesting per-criterion collection (`dict[str, list[float]]` with criterion names as keys). The "composite" key is dynamically added, but the per-criterion score accumulator initialized at line 617 (`score_lists: dict[str, list[float]] = {c.name: [] for c in criteria}`) is never populated with per-criterion scores. The `score_lists` entries for individual criterion names remain empty lists. This is a functional gap: FR-009 requires "one array of N scores per metric" and the batch collection only produces one array total (composite).
- `ports.py` absence means the `EvaluationPort` protocol that `conftest.py` is supposed to inject is not implemented — blocking the FR-006 pytest fixture injection path until `ports.py` is created.

**Improvement Path:**
Implement `evaluate()` or route to `build_metric_for_agent()`. Fix `evaluate_batch()` to collect per-criterion scores from individual `GEval.measure()` calls in addition to the composite. Implement `ports.py`.

---

### Traceability (0.85/1.00)

**Evidence — what is traceable:**
- FR-006, FR-007, FR-008, FR-009, FR-021 are cited in module docstrings with FR ID cross-references. The mapping is consistent across the package.
- The `DIMENSION_WEIGHTS` constant is labeled "SSOT: quality-enforcement.md" with explicit weight values — traceable to the governing document.
- All 5 criteria files cite behavioral-contracts.md section references (§A.2 through §A.6 for structural invariants; §B.3 for floors; §B.4 for per-dimension bounds).
- `adv_scorer.py` criterion descriptions reference SI-SCOR-002 (all 6 dimensions must be scored), SI-SCOR-003 (arithmetic consistency), SI-SCOR-005/006/007 (classification thresholds) — these trace directly to the contract invariants.
- `JerryGEvalMetric.classify_composite()` states the thresholds explicitly in its docstring: "PASS >= 0.92, REVISE 0.85-0.91, REJECTED < 0.85" — traceable to quality-enforcement.md H-13.

**Gaps:**
- The H-10 violations in `metrics.py`, `deepeval_adapter.py`, and `debiasing.py` cannot be traced to any documented exception or approved deviation. The system design's H-10 compliance table does not reflect the actual class distribution. This breaks the traceability chain from design to implementation for that constraint.
- `deepeval_adapter.py` docstring references `system-design.md §2.2: EvaluationPort protocol` but `ports.py` does not exist — the reference is a broken trace.
- FR-007 acceptance criterion specifying YAML/JSON storage at `tests/prompt-regression/criteria/` is not implemented. No documented deviation trace exists.
- The `evaluate_batch()` per-criterion score accumulation gap (empty lists for non-composite criteria names) cannot be traced to any intentional design decision — it appears to be an implementation oversight.

**Improvement Path:**
Document H-10 deviations as accepted deviations with rationale, or resolve them by splitting files. Create `ports.py`. Document the FR-007 storage format deviation.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Completeness | 0.72 | 0.88 | Split `metrics.py` into `quality_criterion.py`, `scoring_result.py`, `jerry_geval_metric.py`; split `deepeval_adapter.py` into `jerry_geval_deepeval_metric.py` and `deep_eval_adapter.py`; extract `PositionRandomizationResult` from `debiasing.py`. This resolves H-10 for all 3 files simultaneously. |
| 2 | Completeness | 0.72 | 0.88 | Implement `jerry/testing/evaluation/ports.py` with the `EvaluationPort` protocol (as referenced in `deepeval_adapter.py` docstring and system design §2.2). Minimum: define `EvaluationPort` as a `typing.Protocol` with `evaluate()` and `evaluate_batch()` signatures. |
| 3 | Actionability | 0.85 | 0.93 | Fix `evaluate_batch()` to populate per-criterion score lists from individual `GEval.measure()` calls — the `score_lists` dict initialized with criterion names is currently left empty; only the "composite" key accumulates values. FR-009 requires one array per metric. |
| 4 | Actionability | 0.85 | 0.93 | Either implement `DeepEvalAdapter.evaluate()` as a real single-shot evaluation path, or annotate it as deprecated and provide a migration guide pointing to `build_metric_for_agent()`. The current stub returning all-zeros without raising is a silent failure mode. |
| 5 | Completeness | 0.72 | 0.88 | Document the FR-007 deviation (criteria stored as Python constants rather than YAML/JSON files at `tests/prompt-regression/criteria/`). If the Python approach is accepted, add a `Deviations` section to the design document with rationale. If YAML storage is required, implement a YAML-based criteria loader. |
| 6 | Methodological Rigor | 0.90 | 0.94 | Replace `asyncio.get_event_loop()` with `asyncio.get_running_loop()` in `a_measure()` to prevent `DeprecationWarning` on Python 3.10+. |
| 7 | Internal Consistency | 0.88 | 0.93 | Replace the dead `pass` block in `JerryGEvalMetric.__post_init__` with an actual `logging.warning()` call when weight sum deviates by > 0.01, so the intention is implemented rather than only commented. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific file/line references
- [x] Uncertain scores resolved downward (Completeness held at 0.72 despite strong criteria content, due to 3 concrete H-10 violations + missing ports.py + FR-007 deviation)
- [x] First-draft calibration considered (this is iter1; multiple structural gaps in a C4 deliverable are expected to score below 0.90 on Completeness)
- [x] No dimension scored above 0.95 without exceptional evidence
- [x] Anti-leniency check on Methodological Rigor: held at 0.90 (not 0.95) specifically because the `evaluate()` stub and `asyncio.get_event_loop()` deprecation are real gaps, and because the H-10 violations represent methodological process failures even though the domain logic itself is sound

**Score calibration note:** Composite of 0.845 is in the 0.84-0.86 range, appropriate for a C4 first-draft implementation that is architecturally strong (H-07 isolation, debiasing pipeline, weight verification) but has concrete structural compliance failures (H-10 x3, missing ports.py) and functional gaps (evaluate() stub, evaluate_batch() per-criterion accumulation). The deliverable is well above 0.70 (good work with clear improvement areas) and close to but not at 0.85 (strong work with minor refinements).

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.845
threshold: 0.94
weakest_dimension: completeness
weakest_score: 0.72
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Split metrics.py (3 classes), deepeval_adapter.py (2 classes), debiasing.py (2 classes) to comply with H-10"
  - "Implement jerry/testing/evaluation/ports.py with EvaluationPort protocol"
  - "Fix evaluate_batch() per-criterion score accumulation (non-composite criterion lists are empty)"
  - "Implement or formally deprecate DeepEvalAdapter.evaluate() stub returning all-zeros"
  - "Document or resolve FR-007 criteria storage deviation (Python vs YAML/JSON)"
  - "Replace asyncio.get_event_loop() with asyncio.get_running_loop() in a_measure()"
  - "Add logging.warning() call in JerryGEvalMetric.__post_init__ for weight-sum deviation"
```
