# Quality Score Report: Stream 3D — Layer 4 Statistical Comparison Engine (Iteration 5)

## L0 Executive Summary

**Score:** 0.926/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.91)
**One-line assessment:** All three iter5 targeted fixes are confirmed present and close the primary traceability gaps, but the hexagonal abstraction inconsistency (direct `ReportGenerator` concrete import in `layer4_stats.py`) and the unverifiable `baselines/protocol.md` floating reference persist, holding Internal Consistency and Evidence Quality below the 0.94 C4 threshold.

---

## Scoring Context

- **Deliverable:** `jerry/testing/types.py`, `jerry/testing/stats.py`, `jerry/testing/layer4_stats.py`, `jerry/testing/baselines/__init__.py`, `jerry/testing/baselines/store.py`, `jerry/testing/baselines/ports.py`, `jerry/testing/reports/__init__.py`, `jerry/testing/reports/generator.py`, `jerry/testing/reports/ports.py`, `jerry/testing/__init__.py`
- **Deliverable Type:** Code
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Stream Threshold:** 0.94 (C4 project mandate, above H-13 baseline of 0.92)
- **Prior Scores:** 0.874 (iter1), 0.934 (iter2), 0.892 (iter3), 0.910 (iter4)
- **Scored:** 2026-03-07T00:00:00Z

---

## Fix Verification (Mandatory for Iter5)

### Iter5 Fixes — Verification Results

| # | Fix Claimed | Status | Evidence |
|---|------------|--------|----------|
| 1 | `_emit_gha_outputs` FR-018 citation added | CONFIRMED | `layer4_stats.py` lines 419–424: docstring reads "Emit GitHub Actions workflow output variables (FR-018 CI/CD integration)" and body comment says "per FR-018 acceptance criteria (exit code + structured outputs)." FR-018 is now cited in both docstring and inline comment. |
| 2 | `_verdict_emoji` FR-018 / behavioral-contracts.md D.6 citation added | CONFIRMED | `generator.py` lines 425–429: docstring now includes "Status labels (PASS/WARN/FAIL/INFO) align with FR-018 CI/CD exit code semantics (behavioral-contracts.md Section D.6) for PR comment display." Both FR-018 and Section D.6 are cited. |
| 3 | ReportGenerator import coupling documented | CONFIRMED | `layer4_stats.py` lines 33–37: comment block above the import reads "ReportGenerator is imported directly as the convenience default for report_generator=None (line 99). This is an intentional adapter-to-adapter dependency documented in the H-07 compliance block above (line 20). Callers may inject any ReportOutputPort implementation to override." All three elements (purpose, intentionality, override path) are present. |

### Additional Incidental Fix Observed

| Item | Status | Evidence |
|------|--------|----------|
| Deprecated `::set-output` fallback eliminated | CONFIRMED | `layer4_stats.py` lines 449–452: else branch now uses `logger.info("GHA_OUTPUT %s=%s", key, value)` — plain logger output, not the deprecated GitHub Actions `::set-output` syntax. This resolves the actionability and traceability gap noted in iter4. |

### Prior Fixes — Verification Results (All Intact)

| Fix | Status | Evidence |
|-----|--------|----------|
| `Layer4Pipeline.__init__` uses port types | INTACT | `layer4_stats.py` lines 90–91: `baseline_store: BaselinePersistencePort`, `report_generator: ReportOutputPort \| None = None` |
| Module docstring uses port type names | INTACT | `layer4_stats.py` lines 11–12: "Call the report generator (via ReportOutputPort)." and "Interact with the baseline store (via BaselinePersistencePort)." |
| `MIN_FULL_SAMPLES` is public and wired as default | INTACT | `store.py` line 102: `MIN_FULL_SAMPLES: int = 30` (public). Line 113: `min_samples: int = MIN_FULL_SAMPLES` uses it as default. |
| `BONFERRONI_ALPHA_FULL = 0.004` is a literal with justification | INTACT | `stats.py` lines 76–80: `BONFERRONI_ALPHA_FULL: float = 0.004` with comment explaining conservative 3-significant-figure rounding rationale. |
| `merge_decision_from_classification` is public | INTACT | `stats.py` line 472: `def merge_decision_from_classification(cls: RegressionClass) -> MergeDecision:` — no leading underscore. |
| Both port protocols are `@runtime_checkable` | INTACT | `baselines/ports.py` line 31: `@runtime_checkable`. `reports/ports.py` line 32: `@runtime_checkable`. |
| `baselines/__init__.py` mentions `BaselinePersistencePort` in Public API | INTACT | `baselines/__init__.py` lines 9–10: "Public API: from jerry.testing.baselines import BaselinePersistencePort." |

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.926 |
| **Stream Threshold** | 0.94 (C4 project mandate) |
| **H-13 Threshold** | 0.92 |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (no adv-executor reports provided) |

---

## Arithmetic Verification

```
Completeness:         0.93 × 0.20 = 0.1860
Internal Consistency: 0.91 × 0.20 = 0.1820
Methodological Rigor: 0.93 × 0.20 = 0.1860
Evidence Quality:     0.92 × 0.15 = 0.1380
Actionability:        0.94 × 0.15 = 0.1410
Traceability:         0.93 × 0.10 = 0.0930
                                   --------
Running sum:
  0.1860 + 0.1820 = 0.3680
  0.3680 + 0.1860 = 0.5540
  0.5540 + 0.1380 = 0.6920
  0.6920 + 0.1410 = 0.8330
  0.8330 + 0.0930 = 0.9260

Weighted Composite: 0.926
Gap to threshold:   0.94 − 0.926 = −0.014
```

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.93 | 0.186 | All FR addressed; deprecated GHA fallback removed; FR-018 citation added; floating `baselines/protocol.md` reference still unresolved across six `store.py` citations |
| Internal Consistency | 0.20 | 0.91 | 0.182 | Direct `ReportGenerator` concrete import persists — documented but not removed; no logical contradictions elsewhere; abstraction gap disclosed but architecturally present |
| Methodological Rigor | 0.20 | 0.93 | 0.186 | Hexagonal boundaries enforced; coupling now has explicit H-07 compliance note; statistical methodology rigorous; note documents the gap but gap remains |
| Evidence Quality | 0.15 | 0.92 | 0.138 | FR-018 and D.6 citations added to `_emit_gha_outputs` and `_verdict_emoji`; `baselines/protocol.md` still unverifiable; academic refs complete |
| Actionability | 0.15 | 0.94 | 0.141 | Deprecated `::set-output` eliminated; full usage examples present; override path for ReportGenerator documented; minor gap: `invalidate()` usage example absent |
| Traceability | 0.10 | 0.93 | 0.093 | `_emit_gha_outputs` and `_verdict_emoji` now trace to FR-018/D.6; `baselines/protocol.md` remains a floating citation without FR equivalence |
| **TOTAL** | **1.00** | | **0.926** | |

---

## Detailed Dimension Analysis

### Completeness (0.93/1.00)

**Evidence:**
- All 10 modules are present and complete. The type contract (`types.py`) covers all domain entities: 5 enums, 8+ data classes, 1 type alias.
- `stats.py` implements all four statistical primitives (Wilcoxon, Wilson, Bonferroni, classification) with correct signatures. Named constants cover FR-014, FR-016, FR-017.
- `layer4_stats.py` implements the full pipeline: `run()`, `run_single_metric()`, smoke mode, statistical mode (single and multi-metric), report persistence, GHA output, exit code mapping.
- `baselines/store.py` covers all CRUD operations: `store()`, `retrieve()`, `invalidate()`, `audit()`. FR-020 quality gate enforced.
- Both port protocols define complete interface surfaces with `@runtime_checkable`.
- `reports/generator.py` covers all three report-construction paths and both serialization formats.
- **Iter5 fix confirmed:** `_emit_gha_outputs` now references FR-018 in its docstring. The deprecated `::set-output` syntax is gone from the fallback path (now uses `logger.info`).

**Gaps:**
1. `baselines/protocol.md` is cited at `store.py` lines 101, 122, 158, 184 (and in multiple comments) but is not a deliverable file and has no FR equivalence stated. Independent verification of the N=30 requirement's provenance is impossible from the code alone. This is a non-trivial completeness gap because callers using `store()` must trust the N=30 mandate is grounded, but the document that grounds it is absent.
2. `baselines/__init__.py` line 56 in the implementation spec (the design artifact) listed `jerry.testing.reports.generator` as importing from `jerry.testing.stats (Bonferroni only)` — but reviewing `generator.py`, it imports only from `jerry.testing.types`, not `jerry.testing.stats`. This is a minor deviation between the spec and implementation (not a code defect, but the spec's H-07 table is slightly inaccurate).

**Improvement Path:**
- Provide `baselines/protocol.md` as a committed artifact, or inline the N=30 specification into a named constant comment with an FR citation.
- (Minor) Correct the implementation spec's H-07 table for `generator.py`.

---

### Internal Consistency (0.91/1.00)

**Evidence:**
- All type annotations in `layer4_stats.py` match imports: `BaselinePersistencePort` (line 32), `ReportOutputPort` (line 38), `ScoreArray` (line 53), `MultiMetricResult` (line 50).
- `_classify_regression` boundary logic is consistent with the `RegressionClass` docstring table in `types.py`. The alpha-scaling logic (`alpha_marginal = alpha * (_ALPHA_MARGINAL / _ALPHA_REGRESSION)`) preserves the 0.05/0.10 ratio under corrected alpha.
- `merge_decision_from_classification` in `stats.py` is imported by both `layer4_stats.py` (line 43) and `__init__.py` (line 37). Mapping is consistent with `MergeDecision` enum.
- Module docstring uses port type names (not concrete classes) — confirmed from iter3 fix.
- `MIN_FULL_SAMPLES = 30` class attribute is referenced as default `min_samples: int = MIN_FULL_SAMPLES` — valid Python class body evaluation.
- Classification table in `types.py` RegressionClass docstring matches the implementation in `_classify_regression` in `stats.py` exactly.

**Gaps:**
- `layer4_stats.py` lines 33–37: `from jerry.testing.reports.generator import ReportGenerator` is a direct import of the concrete adapter. The iter5 fix documents this as "intentional" with a comment, but the architectural inconsistency is not removed — only disclosed. The `Layer4Pipeline.__init__` constructor accepts `ReportOutputPort | None` as the typed parameter, but internally falls back to `ReportGenerator()` (concrete), creating a hidden hard dependency on the concrete adapter. Documentation acknowledges this but does not eliminate the tension.
- The iter5 comment states "Callers may inject any ReportOutputPort implementation to override" — this is accurate, but the default path still bypasses dependency inversion, which is the architectural pattern the module claims to follow. The disclosure reduces the severity compared to an undocumented gap, but the inconsistency between stated principle and implementation remains.

**Improvement Path:**
- The only full resolution is to remove the direct `ReportGenerator` import and require callers to supply a `ReportOutputPort` implementation explicitly (or use a factory module). The current documentation-only mitigation reduces impact but does not close the architectural gap.

---

### Methodological Rigor (0.93/1.00)

**Evidence:**
- Hexagonal boundaries are correctly implemented: `types.py` and `stats.py` import only stdlib + each other; both `ports.py` files import only stdlib + `types.py`; adapter modules import domain modules only; `layer4_stats.py` imports from ports (for type annotations) and from the concrete generator (documented as intentional adapter-to-adapter).
- H-10 (one class per file): met in all files.
- H-11 (type hints + docstrings): All public and private functions have complete annotations and docstrings across all 10 files.
- Statistical methodology: Wilcoxon uses `alternative="two-sided"` per D.1. Effect size is derived via normal approximation as documented. Wilson CIs use `method="wilson"` (statsmodels). Bonferroni division is standard.
- FR-019 one-way dependency: `stats.py` imports only stdlib, scipy, statsmodels, and `types.py` — verified. `layer4_stats.py` is not imported by `stats.py`.
- The iter5 fix adds an explicit H-07 compliance note for the `ReportGenerator` import, which strengthens the documentation of the methodological decision even though the underlying coupling persists.

**Gaps:**
- The `ReportGenerator` direct import in `layer4_stats.py` remains methodologically inconsistent with full hexagonal pattern compliance. The H-07 compliance block documents it as "adapter → adapter (allowed)" — while adapter-to-adapter dependencies are less severe than adapter-to-domain reverse flow, the port abstraction exists precisely to avoid hard-coding which adapter is used. The gap is now disclosed and rationalized, but not eliminated.
- `baselines/protocol.md` is cited as a methodological source document (N=30 requirement) but is not a verifiable deliverable.

**Improvement Path:**
- Remove the concrete `ReportGenerator` import; provide a factory or require explicit injection. This is the methodologically clean path.

---

### Evidence Quality (0.92/1.00)

**Evidence:**
- Every named constant cites its requirement: `MIN_STATISTICAL_SAMPLE_SIZE` cites FR-014 (including verbatim acceptance criterion language), `QUALITY_PASS_THRESHOLD` cites FR-016, `BONFERRONI_K_FULL_SUITE` cites FR-017 with the decomposition (6+1+5+1=13) explained, `BONFERRONI_ALPHA_FULL` cites FR-017 and explains the rounding rationale at length.
- Classification rules cite behavioral-contracts.md sections D.1 and D.4 by name with table entries reproduced inline.
- Academic references [1]–[8] are cited in `stats.py` module docstring (Wilcoxon 1945, Wilson 1927, Cohen 1988, scipy docs, statsmodels docs).
- **Iter5 fix confirmed:** `_emit_gha_outputs` now cites FR-018 in the docstring. `_verdict_emoji` now cites FR-018 and behavioral-contracts.md Section D.6. These were the two uncited functions identified in iter4.
- `store.py` cites FR-004, FR-020, and `baselines/protocol.md` for the N=30 requirement.

**Gaps:**
- `behavioral-contracts.md` is referenced throughout but is not in the deliverable set. The cited sections (D.1, D.2, D.3, D.4, D.5, D.6, E.3) drive critical classification, CI/CD, and invalidation behavior. Without the document, reviewers must trust that the code accurately implements the cited spec. This is an inherent limitation of the split-spec approach.
- `baselines/protocol.md` is cited at least six times in `store.py` but is not a deliverable. The N=30 minimum and "adequate statistical power" justification are grounded in this external document with no in-repo verification path.

**Improvement Path:**
- Include `behavioral-contracts.md` (minimum Sections D.1–D.6) and `baselines/protocol.md` in the deliverable set, or create a `REFERENCES.md` that quotes the exact acceptance criteria text for each cited section.

---

### Actionability (0.94/1.00)

**Evidence:**
- `Layer4Pipeline` class has a complete usage docstring (lines 62–83) showing an end-to-end example with `metric_scores` dict, `EvaluationMode`, and `sys.exit(exit_code)` handling.
- `BaselineStore` usage example shows `store()` and `retrieve()` calls with realistic parameters.
- `ReportGenerator` usage example shows chained `from_single_metric() → to_markdown() → to_json()` calls.
- All public methods have concrete return types and documented exceptions.
- The FR-019 public API exports are listed with clear intent in `__init__.py`.
- Exit codes are documented (0=ALLOW, 1=BLOCK, 2=MARGINAL) in the `_exit_code` docstring.
- **Iter5 incidental fix confirmed:** The deprecated `::set-output` syntax is eliminated from `_emit_gha_outputs`. The local fallback now uses `logger.info("GHA_OUTPUT %s=%s", key, value)` — explicit, non-deprecated, and consistent with the documented local development intent.
- **Iter5 fix 3 confirmed:** The comment block above the `ReportGenerator` import explains the override pattern explicitly, making it actionable for callers who need to inject a different implementation.

**Gaps:**
- `BaselineStore.invalidate()` lacks a usage example. The behavioral-contracts.md Section E.3 baseline invalidation protocol is referenced in the docstring, but no code example shows how to call `invalidate()` in an operational workflow. This is a minor operational documentation gap.

**Improvement Path:**
- Add a usage example to the `BaselineStore` class docstring showing the `invalidate()` call pattern with a contract version string.

---

### Traceability (0.93/1.00)

**Evidence:**
- Every named constant has an explicit `#: FR-NNN:` comment with the acceptance criterion language quoted.
- Module docstrings list all relevant FR numbers.
- Classification rules trace to behavioral-contracts.md D.1/D.4 with table entries reproduced.
- The dependency direction diagram in `layer4_stats.py` (lines 17–22) provides explicit layer traceability, including the documented adapter-to-adapter dependency.
- **Iter5 fixes 1 and 2 confirmed:** `_emit_gha_outputs` now traces to FR-018 in the docstring ("FR-018 CI/CD integration" and "per FR-018 acceptance criteria"). `_verdict_emoji` now traces to FR-018 and behavioral-contracts.md Section D.6. These were the two untraced functions identified in iter4 — both are now traceable.
- `store.py` `store()` method traces to FR-020 in its docstring.
- `baselines/ports.py` traces FR-020 for the `audit()` method requirement.

**Gaps:**
- `baselines/protocol.md` is cited six times in `store.py` (lines 101, 122, 123, 158, 184, 209 area) but this file is not a deliverable and has no FR equivalence stated. The traceability chain for the N=30 requirement terminates at an external document that cannot be independently verified within the deliverable set. This is the same floating reference that has persisted across all iterations.
- The `QUALITY_FLOOR_BREACH` enum value in `RegressionClass` (types.py line 57) is in the classification table with a docstring but is never produced by `_classify_regression()` in `stats.py`. The implementation spec (stream-3d-layer4-stats.md) notes this is "reserved for external callers." However, the docstring for `RegressionClass` does not include a note explaining this value is externally injected, not produced by the statistical engine. A reviewer reading `types.py` alone cannot determine where `QUALITY_FLOOR_BREACH` originates — it is not untraceable, but the traceability requires reading the implementation spec document, not the code.

**Improvement Path:**
- Resolve the `baselines/protocol.md` floating reference by either committing the document or mapping its content to named FRs with inline comments.
- Add a comment to the `QUALITY_FLOOR_BREACH` enum value noting it is injected by Layer 2 callers (not produced by `_classify_regression()`), with a reference to where in the calling code this injection occurs.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.91 | 0.95 | Remove direct `ReportGenerator` import from `layer4_stats.py`; require callers to inject a concrete `ReportOutputPort`; move default construction to a factory function or CLI entrypoint. The documentation-only mitigation (iter5 fix 3) discloses but does not close the hexagonal abstraction gap. |
| 2 | Completeness / Evidence / Traceability | 0.93/0.92/0.93 | 0.95 | Commit `baselines/protocol.md` as a deliverable artifact, OR inline the N=30 specification into `store.py` with a named constant comment and an FR equivalence reference. This single change closes the floating reference gap that persists across all three dimensions. |
| 3 | Traceability | 0.93 | 0.95 | Add a comment to `RegressionClass.QUALITY_FLOOR_BREACH` in `types.py` explaining it is injected by Layer 2 callers and not produced by `_classify_regression()`, with a reference to the injection site. |
| 4 | Actionability | 0.94 | 0.96 | Add a `BaselineStore` class docstring usage example for the `invalidate()` method showing a contract-version invalidation workflow. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific line references
- [x] Uncertain scores resolved downward — Internal Consistency held at 0.91 (not 0.92) despite iter5 documentation fix, because the underlying architectural inconsistency is not removed
- [x] Prior iteration calibration considered — iter4 was 0.910; iter5 raises to 0.926 reflecting three genuine fixes (FR-018 citations on two functions, coupling documentation, deprecated syntax removed), which is a proportionate improvement
- [x] No dimension scored above 0.95 — highest is Actionability at 0.94, supported by elimination of deprecated syntax and complete usage examples
- [x] Score 0.926 is below the 0.94 C4 threshold by −0.014, reflecting the genuine residual defects (hexagonal abstraction gap, floating `baselines/protocol.md` reference) that have not been closed across five iterations

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.926
threshold: 0.94
weakest_dimension: Internal Consistency
weakest_score: 0.91
critical_findings_count: 0
iteration: 5
improvement_recommendations:
  - "Remove direct ReportGenerator import from layer4_stats.py; require explicit ReportOutputPort injection; documentation-only mitigation (iter5 fix 3) does not close the hexagonal abstraction gap"
  - "Commit baselines/protocol.md as a deliverable artifact OR inline the N=30 specification into store.py with FR equivalence — this resolves the floating reference across Completeness, Evidence Quality, and Traceability simultaneously"
  - "Add QUALITY_FLOOR_BREACH comment in types.py RegressionClass noting it is injected by Layer 2 callers (not produced by _classify_regression), with reference to injection site"
  - "Add invalidate() usage example to BaselineStore class docstring"
```
