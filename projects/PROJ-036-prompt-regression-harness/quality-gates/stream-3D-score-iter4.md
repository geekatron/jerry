# Quality Score Report: Stream 3D — Layer 4 Statistical Comparison Engine (Iteration 4)

## L0 Executive Summary

**Score:** 0.910/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Completeness (0.90)
**One-line assessment:** Both iter3 defects are confirmed fixed and all prior fixes are intact, but five residual gaps across completeness, evidence quality, actionability, and traceability prevent the 0.94 C4 threshold from being reached; targeted improvements to module-boundary documentation, deprecated GHA syntax, and a few uncited spec references would close the gap.

---

## Scoring Context

- **Deliverable:** `jerry/testing/types.py`, `jerry/testing/stats.py`, `jerry/testing/layer4_stats.py`, `jerry/testing/baselines/__init__.py`, `jerry/testing/baselines/store.py`, `jerry/testing/baselines/ports.py`, `jerry/testing/reports/__init__.py`, `jerry/testing/reports/generator.py`, `jerry/testing/reports/ports.py`, `jerry/testing/__init__.py`
- **Deliverable Type:** Code
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Stream Threshold:** 0.94 (C4 project mandate, above H-13 baseline of 0.92)
- **Prior Scores:** 0.874 (iter1), 0.934 (iter2), 0.892 (iter3)
- **Scored:** 2026-03-07T00:00:00Z

---

## Fix Verification (Mandatory for Iter4)

### Iter3 Defects — Verification Results

| # | Defect | Status | Evidence |
|---|--------|--------|----------|
| 1 | Stale module docstring in `layer4_stats.py` naming concrete types | FIXED | Lines 11–12: "Call the report generator (via ReportOutputPort)." and "Interact with the baseline store (via BaselinePersistencePort)." — no concrete class names in the responsibility list. |
| 2 | `_MIN_FULL_SAMPLES` dead code (private, hardcoded `30` in `store()`) | FIXED | `store.py` line 102: `MIN_FULL_SAMPLES: int = 30` (public, no underscore). `store.py` line 113: `min_samples: int = MIN_FULL_SAMPLES` uses the class attribute as default. |

### Prior Fixes — Verification Results

| Fix | Status | Evidence |
|-----|--------|----------|
| `Layer4Pipeline.__init__` uses port types | INTACT | `layer4_stats.py` line 87: `baseline_store: BaselinePersistencePort`, line 88: `report_generator: ReportOutputPort \| None = None` |
| `BONFERRONI_ALPHA_FULL = 0.004` is a literal | INTACT | `stats.py` line 80: `BONFERRONI_ALPHA_FULL: float = 0.004` with comment explaining why literal vs. computed |
| `merge_decision_from_classification` is public | INTACT | `stats.py` line 472: `def merge_decision_from_classification(cls: RegressionClass) -> MergeDecision:` — no leading underscore |
| `BaselinePersistencePort` is `@runtime_checkable` | INTACT | `baselines/ports.py` lines 31–32: `@runtime_checkable` decorator present |
| `ReportOutputPort` is `@runtime_checkable` | INTACT | `reports/ports.py` lines 32–33: `@runtime_checkable` decorator present |

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.910 |
| **Stream Threshold** | 0.94 (C4 project mandate) |
| **H-13 Threshold** | 0.92 |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (no adv-executor reports provided) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.90 | 0.180 | All FR addressed; one uncovered path: `_emit_gha_outputs` fallback uses deprecated `::set-output` with no FR reference; `baselines/__init__.py` imports `BaselinePersistencePort` but the `__all__` list in `baselines/__init__.py` only exports it indirectly |
| Internal Consistency | 0.20 | 0.92 | 0.184 | No contradictions; all type annotations align with imports; `_classify_regression` matches RegressionClass docstring table; one micro-gap: `_gen` default construction uses concrete `ReportGenerator()` bypassing the port abstraction |
| Methodological Rigor | 0.20 | 0.92 | 0.184 | Hexagonal boundaries enforced; H-07/H-10/H-11 compliance documented and implemented; statistical methods follow academic references; classification decision table is coherent |
| Evidence Quality | 0.15 | 0.90 | 0.135 | FR/section citations thorough; Bonferroni literal justified in comment; external specs (behavioral-contracts.md, baselines/protocol.md) are cited but not present in the repo for independent verification |
| Actionability | 0.15 | 0.91 | 0.137 | Full public API with usage examples; exit code semantics documented; deprecated `::set-output` fallback in `_emit_gha_outputs` creates a CI/CD ambiguity for local development users |
| Traceability | 0.10 | 0.90 | 0.090 | Every named constant traces to an FR; classification logic traces to behavioral-contracts.md sections; `_emit_gha_outputs` deprecation path untraced; minor: `baselines/protocol.md` is cited but its provenance in the repo is unknown |
| **TOTAL** | **1.00** | | **0.910** | |

---

## Detailed Dimension Analysis

### Completeness (0.90/1.00)

**Evidence:**
- `types.py`: All domain types present — 5 enums (`RegressionClass`, `RateClass`, `EffectSizeLabel`, `EvaluationMode`, `MergeDecision`), 7 data classes (`WilcoxonResult`, `WilsonResult`, `BonferroniConfig`, `RegressionResult`, `MultiMetricResult`, `BaselineRecord`, `BaselineAuditEntry`, `ComparisonReport`), 1 type alias (`ScoreArray`). Every type has complete field coverage and docstrings.
- `stats.py`: All four statistical methods implemented (Wilcoxon, Wilson, Bonferroni, classification), all named constants present (FR-014/016/017), both public comparison functions present (`compare_versions`, `compare_multiple_metrics`).
- `layer4_stats.py`: `Layer4Pipeline` implements the full pipeline — `run()`, `run_single_metric()`, smoke mode, statistical mode (single and multi-metric), report persistence, GHA output, exit code mapping.
- `baselines/store.py`: `BaselineStore` implements all CRUD operations required — `store()`, `retrieve()`, `invalidate()`, `audit()`. FR-020 quality gate enforced.
- Port protocols in `baselines/ports.py` and `reports/ports.py` define the complete interface surfaces.
- `reports/generator.py`: `ReportGenerator` covers all three source paths (`from_single_metric`, `from_multi_metric`, `smoke_mode_report`) and both serialization formats (`to_markdown`, `to_json`).

**Gaps:**
1. `_emit_gha_outputs` (layer4_stats.py lines 443–446): The local development fallback uses the deprecated `::set-output name=...` GitHub Actions syntax. This syntax was deprecated in September 2022 and may silently produce no output in newer GHA runners. No requirement reference is cited for this fallback path, and it is not covered by any visible FR.
2. `baselines/__init__.py` line 16: `__all__ = ["BaselineStore", "BaselinePersistencePort"]` — the port is listed in `__all__`, which is correct, but the module-level docstring (lines 8–10) does not mention `BaselinePersistencePort` in the "Public API" examples — a minor documentation gap that creates a discoverability issue.
3. The `baselines/protocol.md` file is referenced at multiple sites (`store.py` lines 101, 122, 158, 184) but is not present among the deliverable files, creating an unverifiable external dependency.

**Improvement Path:**
- Replace `::set-output` with `GITHUB_OUTPUT` file-write logic (already present for the primary path at line 438) in the else-branch, or document that the fallback is intentionally informational only.
- Add `BaselinePersistencePort` to the `baselines/__init__.py` docstring's Public API section.
- Either provide `baselines/protocol.md` as a deliverable or consolidate its referenced content into inline comments.

---

### Internal Consistency (0.92/1.00)

**Evidence:**
- All type annotations in `layer4_stats.py` match imports: `BaselinePersistencePort` (imported line 32), `ReportOutputPort` (imported line 34), `ScoreArray` (imported line 47), `MultiMetricResult` (imported line 46).
- The `_classify_regression` function boundary logic is consistent with the classification table in `types.py` RegressionClass docstring. The alpha-scaling logic (`alpha_marginal = alpha * (_ALPHA_MARGINAL / _ALPHA_REGRESSION)`) correctly preserves the 0.05/0.10 ratio under Bonferroni-corrected alpha.
- `merge_decision_from_classification` in `stats.py` is imported by both `layer4_stats.py` (line 39) and `__init__.py` (line 37), and the mapping matches the `MergeDecision` enum values in `types.py`.
- Docstring fix confirmed: layer4_stats.py module docstring lines 11–12 say "via ReportOutputPort" and "via BaselinePersistencePort" — consistent with the actual constructor signature.
- `MIN_FULL_SAMPLES` class attribute (store.py line 102) is correctly referenced as the default in the method signature (line 113). Python class body scope makes `MIN_FULL_SAMPLES` accessible for the default expression evaluation at class definition time — this is valid Python.

**Gaps:**
- `layer4_stats.py` line 99: `self._gen = report_generator or ReportGenerator()`. The `report_generator` parameter type is `ReportOutputPort | None`, but the fallback creates a `ReportGenerator` (concrete type). This is not a type error since `ReportGenerator` satisfies the protocol, but it is a mild abstraction inconsistency — the module's dependency inversion principle allows the consumer to inject any port implementation, but the fallback hard-codes the concrete adapter. This creates a hidden dependency on the concrete class from the orchestrator module, which H-07 architecture layer isolation discourages.

**Improvement Path:**
- Make the default `None` and require explicit injection in production, or move the default construction to a factory function that maintains the abstraction boundary.

---

### Methodological Rigor (0.92/1.00)

**Evidence:**
- Hexagonal architecture boundaries are correctly implemented: `types.py` and `stats.py` import only stdlib and each other; `ports.py` files import only stdlib and `types.py`; adapter modules (`store.py`, `generator.py`) import domain modules but not each other horizontally; `layer4_stats.py` imports from ports (not concrete adapters for baseline), but does import `ReportGenerator` directly (line 33) — the port `ReportOutputPort` is the type annotation, and `ReportGenerator` is the concrete fallback.
- H-10 (one class per file) is met: every file defines exactly one class (or, for `types.py`, groups of enums and data classes per stated H-10 grouping exception).
- H-11 (type hints + docstrings): All public functions in all files have complete type annotations and docstrings. Private helpers (`_cohens_r`, `_effect_label`, `_classify_regression`, `_rate_class`, `_validate_score_array`) also have complete docstrings.
- Statistical methodology: Wilcoxon uses `alternative="two-sided"` per behavioral-contracts.md D.1. Effect size computed via normal approximation `Z = (W - mu_W) / sqrt(var_W)`. Wilson CIs use statsmodels `method="wilson"`. Bonferroni division `alpha_family / k` is standard.
- FR-019 one-way dependency: `stats.py` has no import from `layer4_stats.py` — verified by reading stats.py imports (lines 37–55: only stdlib + scipy + statsmodels + types).

**Gaps:**
- `layer4_stats.py` line 33 directly imports `from jerry.testing.reports.generator import ReportGenerator` — this is the concrete adapter, not the port. While `ReportOutputPort` is used as the type annotation on the parameter and in the H-07 compliance note in the docstring (line 20 says "layer4_stats.py → reports/generator (allowed: adapter → adapter)"), the direct import of the concrete adapter rather than through the port is a methodological inconsistency with the hexagonal pattern's intent. Importing `ReportGenerator` by name makes `layer4_stats.py` tightly coupled to the concrete adapter despite the port abstraction.
- The `::set-output` fallback (line 446) uses a syntax pattern that is not documented in any referenced FR, reducing methodological completeness on the CI/CD integration axis.

**Improvement Path:**
- Remove the direct `ReportGenerator` import from `layer4_stats.py`; require callers to inject a `ReportOutputPort` implementation. Move the default instantiation to a factory or the CLI entrypoint.

---

### Evidence Quality (0.90/1.00)

**Evidence:**
- Every named constant cites its requirement: `MIN_STATISTICAL_SAMPLE_SIZE` cites FR-014, `QUALITY_PASS_THRESHOLD` cites FR-016, `BONFERRONI_K_FULL_SUITE` cites FR-017, `BONFERRONI_ALPHA_FULL` cites FR-017 and explains the rounding rationale.
- Classification rules cite behavioral-contracts.md sections (D.1, D.4) by name with the specific table entries reproduced inline in docstrings.
- Academic references [1]–[8] cited in `stats.py` module docstring (Wilcoxon 1945, Wilson 1927, Cohen 1988, scipy docs, statsmodels docs).
- `store.py` cites FR-004, FR-020, and `baselines/protocol.md` for the N=30 requirement.
- `layer4_stats.py` cites FR-018 for exit code mapping in the `_exit_code` docstring.

**Gaps:**
- `behavioral-contracts.md` and `baselines/protocol.md` are referenced but not present in the deliverable set, making independent verification of the cited contract text impossible. The citations are internally consistent but not externally verifiable from the code alone.
- The `_emit_gha_outputs` method has no FR citation — the GitHub Actions integration is an acceptance criterion but which requirement mandates this specific output format is not stated in the code.
- `generate.py`'s `_verdict_emoji` method maps classifications to PASS/WARN/FAIL labels, but this mapping has no cited requirement reference (no FR-018 sub-criterion or contract section for the emoji/label mapping).

**Improvement Path:**
- Add FR references to `_emit_gha_outputs` and `_verdict_emoji`.
- Include `behavioral-contracts.md` and `baselines/protocol.md` as deliverable artifacts or provide inline summaries of the key cited sections.

---

### Actionability (0.91/1.00)

**Evidence:**
- `Layer4Pipeline` class has a complete usage docstring (lines 62–83 of `layer4_stats.py`) showing an end-to-end example with exact invocation including metric_scores dict and exit code handling.
- `BaselineStore` has a usage example showing `store()` and `retrieve()` calls with realistic parameter values.
- `ReportGenerator` has a usage example showing chained calls.
- All methods have concrete return types and documented exceptions.
- The public API surface (`jerry.testing.__init__.py`) exports the minimum FR-019-required symbols with clear intent.
- Exit codes are documented: 0=ALLOW, 1=BLOCK, 2=MARGINAL.

**Gaps:**
- `_emit_gha_outputs` fallback (line 446) uses `::set-output name=...` syntax which has been deprecated by GitHub since 2022. Developers running this locally and comparing actual output against GHA output will get different formats. The actionability of the local development path is degraded.
- No example is provided for the `invalidate()` baseline method usage, which is an operational concern per behavioral-contracts.md Section E.3.
- `run()` has a `bonferroni_k: int | None = None` parameter but the docstring does not state the default resolution path clearly (it does for FULL/STANDARD mode separately in the body, but not in the docstring's Args section, which only says "Override for Bonferroni k. Defaults to BONFERRONI_K_FULL_SUITE (13) for FULL mode, len(metric_scores) for STANDARD mode" — this is present, so the gap is minor).

**Improvement Path:**
- Replace `::set-output` fallback with `GITHUB_OUTPUT`-style output (multi-line file write) or document that the fallback is deprecated and remove it.
- Add a usage example for `invalidate()` in `BaselineStore`.

---

### Traceability (0.90/1.00)

**Evidence:**
- Every named constant has an explicit `#: FR-NNN:` comment with the exact acceptance criterion language quoted.
- Module docstrings list all relevant FR numbers for the module.
- Classification rules are traced to behavioral-contracts.md sections with table references.
- The dependency direction diagram in `layer4_stats.py` (lines 17–21) provides explicit layer traceability.
- Iter3 fixes are traceable: docstring says "via BaselinePersistencePort" / "via ReportOutputPort" (matches the injected port types); `MIN_FULL_SAMPLES` is public and referenced by name in `store()`.

**Gaps:**
- `_emit_gha_outputs` has no requirement trace. The function exists and is called but no FR reference appears in its docstring, only a comment about "enabling subsequent workflow steps to read the verdict."
- `baselines/protocol.md` is cited six times across `store.py` but this file is not in the deliverable set and has no FR equivalence established, making it a floating reference.
- The `_verdict_emoji` mapping in `generator.py` (lines 433–449) has no requirement trace — what mandates these specific status labels (PASS/WARN/FAIL/INFO) for the GitHub PR comment format?

**Improvement Path:**
- Add an FR reference (or "per behavioral-contracts.md Section D.6" reference) to the `_emit_gha_outputs` docstring.
- Add an FR reference to `_verdict_emoji` tying it to the PR comment format requirement.
- Clarify the relationship between `baselines/protocol.md` and the FRs that reference it.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.92 | 0.95 | Remove direct `ReportGenerator` import from `layer4_stats.py`; require callers to inject a concrete `ReportOutputPort`; move default construction to a factory or CLI entrypoint. This eliminates the tight coupling to the concrete adapter that undermines the hexagonal port abstraction. |
| 2 | Actionability | 0.91 | 0.94 | Replace the `::set-output` fallback in `_emit_gha_outputs` with a `GITHUB_OUTPUT`-compatible format or remove the local fallback with a comment explaining the path. This unblocks local testing clarity. |
| 3 | Traceability | 0.90 | 0.94 | Add FR or behavioral-contracts.md section references to `_emit_gha_outputs` docstring and `_verdict_emoji`. Resolve floating `baselines/protocol.md` citations by either including the file or mapping its content to an FR. |
| 4 | Evidence Quality | 0.90 | 0.94 | Include `behavioral-contracts.md` in the deliverable set (or at minimum Section D.1–D.6 excerpts), so cited evidence is independently verifiable. Add missing FR citation to `_emit_gha_outputs`. |
| 5 | Completeness | 0.90 | 0.94 | Add `BaselinePersistencePort` to `baselines/__init__.py` module docstring Public API section. Resolve `baselines/protocol.md` as a verifiable artifact. Document or fix the `::set-output` deprecated fallback. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific line references
- [x] Uncertain scores resolved downward (e.g., Completeness at 0.90 not 0.92 due to GHA deprecation and floating reference gaps)
- [x] First-draft calibration not applicable (this is iteration 4)
- [x] No dimension scored above 0.95 — highest is 0.92 for Internal Consistency and Methodological Rigor, both with documented evidence of non-trivial items at that level
- [x] Score improvement over iter3 (0.892 → 0.910) reflects genuine fixes verified above; the gap to threshold (0.94) reflects real remaining defects, not leniency inflation

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.910
threshold: 0.94
weakest_dimension: Completeness
weakest_score: 0.90
critical_findings_count: 0
iteration: 4
improvement_recommendations:
  - "Remove direct ReportGenerator import from layer4_stats.py; inject via ReportOutputPort port exclusively to close hexagonal abstraction gap"
  - "Replace deprecated ::set-output fallback in _emit_gha_outputs with GITHUB_OUTPUT-compatible write or remove the fallback with explanatory comment"
  - "Add FR or behavioral-contracts.md section citations to _emit_gha_outputs and _verdict_emoji docstrings"
  - "Include behavioral-contracts.md (Sections D.1-D.6 minimum) in the deliverable set or map its content to numbered FRs"
  - "Add BaselinePersistencePort to baselines/__init__.py module docstring Public API section"
```
