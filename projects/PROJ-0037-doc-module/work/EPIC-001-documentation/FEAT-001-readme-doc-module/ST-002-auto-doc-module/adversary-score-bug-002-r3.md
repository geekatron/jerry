# Quality Score Report: BUG-002 Fix — Template Path Not Anchored to Repo Root (Iteration 3)

## L0 Executive Summary

**Score:** 0.932/1.00 | **Verdict:** PASS | **Weakest Dimension:** Evidence Quality (0.87)
**One-line assessment:** Three dedicated BUG-002 tests directly exercise the subdirectory-invocation scenario, the repo_root-based skills_dir resolution, and the pyproject.toml walk-up discovery, closing the binding Evidence Quality constraint and pushing the weighted composite to 0.932 — above the 0.93 threshold; quality gate is met.

---

## Scoring Context

- **Deliverable:** BUG-002 fix spanning `src/bootstrap.py` (lines 792-860) and `src/docs/application/handlers/commands/generate_docs_command_handler.py`
- **Deliverable Type:** Code (Bug Fix)
- **Criticality Level:** C2 (Standard — 3 files in scope, reversible within 1 day)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Prior Score:** 0.899 (Iteration 2, REVISE)
- **Strategy Findings Incorporated:** No — scored from deliverable artifacts directly
- **Scored:** 2026-03-18T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.932 |
| **Threshold** | 0.93 (project-specified) |
| **Verdict** | PASS |
| **Strategy Findings Incorporated** | No |
| **Delta from Iteration 2** | +0.033 (0.899 → 0.932) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.93 | 0.186 | All four ACs now have executable evidence; AC-1 directly tested via CWD-divergence test |
| Internal Consistency | 0.20 | 0.95 | 0.190 | Unchanged from R2 — all four path-sensitive operations use `self._repo_root`; no contradictions |
| Methodological Rigor | 0.20 | 0.92 | 0.184 | Unchanged from R2 — pyproject.toml walk-up + `logger.warning()` fallback; composition root pattern intact |
| Evidence Quality | 0.15 | 0.87 | 0.1305 | Three dedicated BUG-002 tests now exercise the exact scenario; fallback path (pyproject.toml not found) remains untested |
| Actionability | 0.15 | 0.96 | 0.144 | Unchanged from R2 — test confirmation adds marginal confidence; production-ready across all documented paths |
| Traceability | 0.10 | 0.97 | 0.097 | Unchanged from R2 — entity closed, five code-level references, tests add BUG-002 traceability chain |
| **TOTAL** | **1.00** | | **0.932** | |

---

## Detailed Dimension Analysis

### Completeness (0.93/1.00)

**Evidence:**

AC-1 ("works from any subdirectory") — NOW DIRECTLY TESTED. `test_bug002_path_traversal_uses_repo_root_not_cwd` (line 1248) sets CWD to `/` via `monkeypatch.chdir("/")`, constructs the handler with `repo_root=tmp_path`, and asserts that `/etc/passwd` is rejected with `error["code"] == "PATH_TRAVERSAL"`. This is the definitive executable proof that the traversal guard uses `self._repo_root` (not CWD): if CWD were being used as root, `/` would contain `/etc/passwd` and the guard would pass — but it fails as expected, confirming `repo_root=tmp_path` is the operative boundary.

AC-2 (template directory resolved to absolute path in composition root) — SATISFIED. `bootstrap.py` line 849: `template_dir = str(_repo_root / ".context" / "templates" / "docs")`. Tested indirectly by `test_bug002_bootstrap_repo_root_discovery` which asserts `handler._repo_root` contains `pyproject.toml` (i.e., the handler received a correctly-resolved root from `create_docs_generator()`).

AC-3 (existing tests continue to pass) — SATISFIED. 62/62 doc tests pass (59 original + 3 new BUG-002 tests).

AC-4 (no hardcoded relative paths in rendering pipeline) — SATISFIED. Handler lines 142 (`self._repo_root / _DEFAULT_SKILLS_SUBDIR`) and 147 (`self._repo_root / _DEFAULT_TEMPLATE_SUBDIR`) confirmed unchanged. Tested by `test_bug002_handler_resolves_paths_against_repo_root` which asserts the `called_skills_dir` contains `str(repo_root)`.

**Gaps:**

The handler tests mock `extractor` and `renderer`, so no test exercises the full end-to-end execution path from a subdirectory CWD through to actual Jinja2 rendering and README writing. This is a minor gap — the mocking isolates the path resolution logic correctly, which is exactly what needs testing for BUG-002. A full integration test would close this residual gap but is not required for AC satisfaction.

**Improvement Path:**

Score would reach 0.96+ with a full integration test (real renderer, real template directory, synthetic subdirectory CWD) and a test covering the `pyproject.toml`-not-found fallback path. Neither is required for the quality gate at this threshold.

---

### Internal Consistency (0.95/1.00)

**Evidence:**

Unchanged from Iteration 2. All four path-sensitive operations in `handle()` use `self._repo_root`:
- Line 112: `readme_abs.relative_to(self._repo_root)` — traversal guard
- Line 142: `skills_dir = str(self._repo_root / _DEFAULT_SKILLS_SUBDIR)` — skill discovery
- Line 147: `template_data_dir = self._repo_root / _DEFAULT_TEMPLATE_SUBDIR` — template data

The class docstring at line 62-63 accurately describes `_repo_root` as "used to resolve skills_dir and template data paths independent of CWD (BUG-002)". `bootstrap.py` always supplies an explicit `_repo_root` from the pyproject.toml walk-up (lines 823-847). The handler `__init__` default `Path.cwd()` is a backward-compatibility provision for test callers only, not a production path.

No contradictions are present. The Iteration 1 binding constraint (path traversal guard using `Path.cwd()` directly) was resolved in Iteration 2 and remains resolved.

**Gaps:**

The 0.05 residual gap reflects the intentional `repo_root: Path | None = None` default in `__init__`, which makes CWD the fallback for callers not supplying an explicit root. This is an intentional design choice for backward-compatible test callers — it is not an inconsistency in the post-revision state. The absence of an `assert repo_root.is_absolute()` guard in `__init__` is a minor defensive-programming gap.

**Improvement Path:**

Adding `assert repo_root is None or repo_root.is_absolute()` to `__init__` would close the defensive gap. Score would reach 0.97+ with this addition.

---

### Methodological Rigor (0.92/1.00)

**Evidence:**

Unchanged from Iteration 2. The pyproject.toml walk-up in `bootstrap.py` (lines 830-847) is a standard Python ecosystem pattern for anchor-independent repo root discovery. The composition root pattern (H-07) is maintained: `bootstrap.py` performs all path resolution and passes absolute paths to downstream components. The fallback uses `Path.cwd().resolve()` with `logger.warning()`, making the exceptional case (no pyproject.toml in ancestry) observable rather than silently misconfigured.

**Gaps:**

The fallback to `Path.cwd()` still produces a CWD-dependent result in the edge case the fix was designed to eliminate CWD dependency for. The `logger.warning()` mitigates this by making the fallback observable, but a `RuntimeError` would provide a clearer failure signal. This is a methodological preference, not a defect.

**Improvement Path:**

Converting the fallback to a `RuntimeError("Cannot locate pyproject.toml above {_here}")` would push this dimension to 0.95+. Adding a test for the fallback path would also improve Evidence Quality simultaneously.

---

### Evidence Quality (0.87/1.00)

**Evidence:**

Three new dedicated BUG-002 tests are confirmed present at lines 1248-1351 of `tests/unit/docs/test_phase1_evidence.py`:

**Test 1 — `test_bug002_path_traversal_uses_repo_root_not_cwd` (line 1248):**
Sets CWD to `/` (filesystem root) via `monkeypatch.chdir("/")`. Constructs handler with `repo_root=tmp_path`. Attempts to `handle()` with `readme_path="/etc/passwd"`. Asserts `result.success is False` and `result.error["code"] == "PATH_TRAVERSAL"`. This is the strongest possible form of BUG-002 evidence: it would produce a false `success=True` if the guard used CWD (since `/etc/passwd` is within CWD=`/`), but correctly produces `success=False` because the guard uses `self._repo_root=tmp_path` instead. The CWD/repo_root divergence is maximal (`/` vs. `tmp_path`), eliminating any coincidence.

**Test 2 — `test_bug002_handler_resolves_paths_against_repo_root` (line 1281):**
Creates a fake repo structure at `tmp_path / "fake-repo"`. Passes `repo_root=repo_root` to the handler. Calls `handle()`. Asserts that `mock_extractor.extract_all` was called with a `skills_dir` argument containing `str(repo_root)`. This directly verifies the core BUG-002 scenario: skills discovery uses the injected `repo_root`, not CWD.

**Test 3 — `test_bug002_bootstrap_repo_root_discovery` (line 1338):**
Calls `create_docs_generator()` directly. Asserts `hasattr(handler, "_repo_root")` and `(handler._repo_root / "pyproject.toml").exists()`. This tests the composition root's walk-up logic: the handler's `_repo_root` attribute points to a directory that actually contains `pyproject.toml`, confirming the walk-up terminates at the correct anchor.

Together, these three tests provide executable evidence for:
- The traversal guard uses `repo_root` not CWD (Test 1)
- Path resolution for discovery uses `repo_root` not CWD (Test 2)
- The composition root discovers the correct anchor via pyproject.toml walk-up (Test 3)

**Gaps:**

The fallback path in `bootstrap.py` (lines 835-845: pyproject.toml not found, fallback to `Path.cwd()`, `logger.warning()`) remains untested. No test exercises the `mode="write"` or atomic write path in a repo_root-anchored context. These are secondary and tertiary gaps relative to the primary BUG-002 claim.

**Improvement Path:**

Add a test that mocks the `pyproject.toml` walk to always miss and asserts that `logger.warning()` is called with the diagnostic message. This closes the fallback coverage gap. Score would reach 0.92+ with this addition.

---

### Actionability (0.96/1.00)

**Evidence:**

Unchanged from Iteration 2. The fix is production-ready across all documented paths:
- Path traversal guard: `readme_abs.relative_to(self._repo_root)` — anchored to injected root
- Skills discovery: `self._repo_root / _DEFAULT_SKILLS_SUBDIR` — absolute, CWD-independent
- Template data: `self._repo_root / _DEFAULT_TEMPLATE_SUBDIR` — absolute, CWD-independent
- Composition root: `bootstrap.py` always supplies explicit `_repo_root` from pyproject.toml walk-up

Test 1 now provides executable confirmation that the fix is correctly deployed: a developer can invoke `jerry docs generate` from any subdirectory and the handler will use the composition root's `_repo_root` for all path operations.

**Gaps:**

The 0.04 gap reflects that no test exercises the full `mode="write"` atomic write path with a repo_root-anchored handler from a subdirectory CWD. This is a minor actionability gap; the write path is covered by other tests, just not in the CWD-divergence scenario.

**Improvement Path:**

Adding a CWD-divergence test for the write mode path would push this dimension to 0.98+. Not required for the quality gate.

---

### Traceability (0.97/1.00)

**Evidence:**

Unchanged from Iteration 2. BUG-002 entity status is `completed` with `Completed: 2026-03-18T00:00:00Z`. History entry documents the fix and scoring provenance. Five code-level BUG-002 references are present:
- `bootstrap.py` function docstring: "BUG-002: Template path anchored to repo root, not CWD"
- Handler class docstring: "_repo_root: Absolute path ... (BUG-002)"
- Handler `__init__` docstring: "BUG-002 fix" in `repo_root` parameter description
- Handler `handle()` inline comment (line 104): "BUG-002" reference in path traversal note
- Handler `handle()` inline comment (lines 108-109): "BUG-002" reference in consistency note

The three new tests each carry a `"""BUG-002 evidence: ..."""` docstring, extending the traceability chain into the test layer. An auditor following the chain from code comment → entity → test now finds a complete, closed, traceable fix.

**Gaps:**

The 0.03 residual gap reflects the absence of a commit hash in the BUG-002 history entry. The history entry documents the fix description and test evidence but does not cite a specific commit reference for long-term audit.

**Improvement Path:**

Add the implementing commit hash to the BUG-002 history entry after the fix is committed. Score would reach 0.99 with this addition.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.87 | 0.92 | Add a test that simulates pyproject.toml-not-found (mock the walk loop to always reach filesystem root) and asserts `logger.warning()` is called with the diagnostic message |
| 2 | Completeness | 0.93 | 0.96 | The fallback test (Priority 1) also satisfies the remaining coverage gap for AC-1's edge case |
| 3 | Methodological Rigor | 0.92 | 0.95 | Consider converting the `Path.cwd()` fallback to `RuntimeError("Cannot locate pyproject.toml above {_here}")` for clearer failure semantics, or add an explicit docstring justification for why the CWD fallback is intentionally retained |
| 4 | Internal Consistency | 0.95 | 0.97 | Add `assert repo_root is None or repo_root.is_absolute()` to `__init__` to defensively guard against callers passing a relative path as `repo_root` |
| 5 | Traceability | 0.97 | 0.99 | Add implementing commit hash to BUG-002 history entry after the fix is committed |

---

## Score Delta Summary (Iteration 2 → Iteration 3)

| Dimension | R2 Score | R3 Score | Delta | Driver |
|-----------|----------|----------|-------|--------|
| Completeness | 0.88 | 0.93 | +0.05 | AC-1 now has executable test evidence via CWD-divergence test |
| Internal Consistency | 0.95 | 0.95 | 0.00 | No change; R2 fix remains in place |
| Methodological Rigor | 0.92 | 0.92 | 0.00 | No change; fallback diagnostic unchanged |
| Evidence Quality | 0.72 | 0.87 | +0.15 | Three dedicated BUG-002 tests added; fallback path still uncovered |
| Actionability | 0.96 | 0.96 | 0.00 | No change; test confirmation provides marginal confidence boost |
| Traceability | 0.97 | 0.97 | 0.00 | No change; test docstrings extend chain but no new entity updates |
| **Composite** | **0.899** | **0.932** | **+0.033** | — |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence Quality at 0.87 — three tests directly exercise BUG-002 scenario; uncertain whether 0.87 or 0.88 was appropriate for the remaining fallback gap; resolved downward to 0.87 per bias rule
- [x] Completeness moved to 0.93 — justified by AC-1 having direct executable evidence (CWD-divergence test); not rounded up to 0.95+ because the tests mock the extractor/renderer rather than running full end-to-end through real rendering infrastructure
- [x] Internal Consistency held at 0.95 — no changes in Iteration 3 code; the intentional `repo_root=None` default justifies the 0.05 residual
- [x] Methodological Rigor held at 0.92 — no changes in Iteration 3 code; the fallback deferred-failure mode justifies the 0.08 residual
- [x] Composite at 0.932 clears the 0.93 threshold by 0.002; calibration re-check: if Evidence Quality were scored 0.85 (one tick lower), composite would be 0.929 (REVISE). The 0.87 score is justified by three directly targeted tests with strong specificity (Test 1 uses maximal CWD/root divergence, not a mild scenario); 0.87 rather than 0.85 is appropriate
- [x] No dimension scored above 0.97 without exceptional evidence — Traceability at 0.97 is justified by full entity closure plus five code-level references plus three test docstrings
- [x] Calibration: this is iteration 3 of a focused bug fix; the 0.87 Evidence Quality reflects genuine improvement from 0.72 (three targeted tests added) but acknowledges the fallback path remains unexercised

---

## Session Context (Handoff Schema)

```yaml
verdict: PASS
composite_score: 0.932
threshold: 0.93
weakest_dimension: Evidence Quality
weakest_score: 0.87
critical_findings_count: 0
iteration: 3
improvement_recommendations:
  - "Add test: pyproject.toml-not-found fallback — mock walk to always reach filesystem root, assert logger.warning() called with diagnostic message"
  - "Consider converting Path.cwd() fallback in bootstrap.py to RuntimeError for clearer failure semantics"
  - "Add assert repo_root is None or repo_root.is_absolute() defensive guard in __init__"
  - "Add implementing commit hash to BUG-002 history entry after commit"
```
