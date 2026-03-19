# Quality Score Report: BUG-002 Fix — Template Path Not Anchored to Repo Root (Iteration 2)

## L0 Executive Summary

**Score:** 0.899/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.72)
**One-line assessment:** The Internal Consistency binding constraint is fully resolved (path traversal guard now uses `self._repo_root`), the fallback diagnostic was improved to `Path.cwd()` with `logger.warning()`, and the BUG-002 entity is closed — but no automated test exercises the subdirectory invocation scenario or the pyproject.toml walk-up logic, keeping Evidence Quality at 0.72 and the composite at 0.899, below the 0.93 threshold.

---

## Scoring Context

- **Deliverable:** BUG-002 fix spanning `src/bootstrap.py` (lines 792-860) and `src/docs/application/handlers/commands/generate_docs_command_handler.py`
- **Deliverable Type:** Code (Bug Fix)
- **Criticality Level:** C2 (Standard — 3 files in scope, reversible within 1 day)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Prior Score:** 0.882 (Iteration 1, REVISE)
- **Strategy Findings Incorporated:** No — scored from deliverable artifacts directly
- **Scored:** 2026-03-18T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.899 |
| **Threshold** | 0.93 (project-specified) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |
| **Delta from Iteration 1** | +0.017 (0.882 → 0.899) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.88 | 0.176 | BUG-002 entity now closed; three of four ACs satisfied; AC-1 (subdirectory invocation) still has no automated test |
| Internal Consistency | 0.20 | 0.95 | 0.190 | **Fixed:** path traversal guard now uses `self._repo_root` (line 112); all four path-sensitive operations consistent |
| Methodological Rigor | 0.20 | 0.92 | 0.184 | **Improved:** fallback now uses `Path.cwd().resolve()` with `logger.warning()` instead of silent `_here`; composition root pattern maintained |
| Evidence Quality | 0.15 | 0.72 | 0.108 | No new tests for subdirectory invocation, pyproject.toml walk, or `create_docs_generator()` path; 59/59 doc tests pass but BUG-002-specific scenario unexercised |
| Actionability | 0.15 | 0.96 | 0.144 | **Improved:** fix is now coherent across all code paths; traversal guard gap closed; production-ready for all documented use cases |
| Traceability | 0.10 | 0.97 | 0.097 | **Improved:** BUG-002 entity `completed` with Completed timestamp and history entry; five code-level references intact |
| **TOTAL** | **1.00** | | **0.899** | |

---

## Detailed Dimension Analysis

### Completeness (0.88/1.00)

**Evidence:**

AC-2 (template directory resolved to absolute path in composition root) — SATISFIED. `bootstrap.py` line 849: `template_dir = str(_repo_root / ".context" / "templates" / "docs")`. The `_repo_root` is computed by walking up from `Path(__file__).resolve().parent` until `pyproject.toml` is found.

AC-3 (existing tests continue to pass) — SATISFIED. The task context confirms 59/59 doc tests pass. The `repo_root` parameter addition is backward-compatible (default `None` preserved) and does not break existing callers.

AC-4 (no hardcoded relative paths in rendering pipeline) — SATISFIED. Handler line 142 uses `self._repo_root / _DEFAULT_SKILLS_SUBDIR`; line 147 uses `self._repo_root / _DEFAULT_TEMPLATE_SUBDIR`. No CWD-relative path remains in the operational pipeline.

AC-1 (works from any subdirectory) — NOT INDEPENDENTLY VERIFIED BY TEST. The code correctness is structural: `bootstrap.py` anchors `_repo_root` to `__file__` ancestry, not CWD. But no automated test invokes `create_docs_generator()` or `GenerateDocsCommandHandler.handle()` from a synthetic subdirectory CWD and asserts success. The grep of `tests/unit/docs/test_phase1_evidence.py` finds zero matches for `repo_root`, `BUG-002`, `subdirectory`, or `pyproject`, confirming no new tests were added addressing the specific BUG-002 scenario.

BUG-002 entity closure — SATISFIED. History entry added: "Fix: bootstrap.py discovers repo root via pyproject.toml walk-up; handler uses self._repo_root for all path resolution including path traversal guard. /adversary scored, revision applied. 59/59 doc tests pass." `Status: completed`, `Completed: 2026-03-18T00:00:00Z`. This addresses the entity-level gap from Iteration 1.

**Gaps:**

No test exercises AC-1 directly. The pyproject.toml-not-found fallback path in `bootstrap.py` (lines 835-845) remains untested. The entity closure gap from Iteration 1 is resolved but the test gap remains.

**Improvement Path:**

Add a unit test that: (1) creates a temp tree with `tmp_path/pyproject.toml` and `tmp_path/src/bootstrap_equivalent.py`; (2) instantiates `GenerateDocsCommandHandler` with `repo_root=tmp_path`; (3) monkeypatches CWD to `tmp_path/src`; (4) calls `handle()` with a `readme_path` at `tmp_path/README.md` and asserts `success=True` on the path traversal check. This directly validates AC-1 with executable evidence. Score moves toward 0.93+ when AC-1 has test coverage.

---

### Internal Consistency (0.95/1.00)

**Evidence:**

The binding constraint from Iteration 1 is fully resolved. The path traversal guard at handler lines 107-112 now reads:

```
readme_abs = Path(command.readme_path).resolve()
readme_abs.relative_to(self._repo_root)
```

The inline comment at lines 101-109 was updated to explain the BUG-002 consistency: "The path traversal guard uses `self._repo_root` (resolved at construction time via the composition root) rather than CWD, ensuring consistency with all other path resolution in this handler (BUG-002)."

All four path-sensitive operations in `handle()` are now consistent:
- Line 112: `readme_abs.relative_to(self._repo_root)` — traversal guard
- Line 142: `skills_dir = str(self._repo_root / _DEFAULT_SKILLS_SUBDIR)` — skill discovery
- Line 147: `template_data_dir = self._repo_root / _DEFAULT_TEMPLATE_SUBDIR` — template data

The class docstring at line 62-63 accurately describes `_repo_root` as "used to resolve skills_dir and template data paths independent of CWD (BUG-002)".

**Gaps:**

The `repo_root: Path | None = None` default in `__init__` (line 88) means that callers who do not supply `repo_root` get `Path.cwd().resolve()` as the root. This is documented and intentional (backward compatibility for tests), not an inconsistency. The `bootstrap.py` composition root always supplies an explicit `_repo_root`, so production callers are not affected.

No contradictions remain. The 0.05 gap from 1.00 reflects the minor conceptual distinction between the handler's `__init__` default (CWD-based, for backward-compatible test callers) and the production path (explicit `_repo_root` from composition root). This is a deliberate design choice, not an inconsistency in the post-revision state.

**Improvement Path:**

This dimension is essentially resolved. The residual 0.05 gap reflects the intentional backward-compatibility default and the absence of a guard assertion in `__init__` that `repo_root` is absolute (i.e., no `assert repo_root.is_absolute()` guard to catch misuse). Adding such a guard would push this dimension to 0.97+.

---

### Methodological Rigor (0.92/1.00)

**Evidence:**

The Iteration 1 gap was the fallback: `_repo_root = _here` (the `src/` directory containing `bootstrap.py`), which silently produced a non-functional `src/.context/templates/docs` path. The revision replaces this with:

```python
_repo_root = _Path.cwd().resolve()
_logger.warning(
    "Could not locate pyproject.toml walking up from %s; "
    "falling back to CWD for repo root: %s",
    _here,
    _repo_root,
)
```

This is methodologically improved on two counts: (1) the fallback is now transparent (warning logged with both the start path and the fallback resolution), and (2) `Path.cwd()` is a more reasonable fallback than `_here` for the edge case where the CLI is invoked without a `pyproject.toml` ancestry — at least CWD is likely to be the repo root in common invocations.

The composition root pattern (H-07) remains intact. The pyproject.toml walk-up is a standard Python ecosystem pattern for repo root discovery. Backward compatibility via `repo_root: Path | None = None` default is maintained.

**Gaps:**

The fallback to `Path.cwd()` still produces a CWD-dependent result in a scenario (no `pyproject.toml` in ancestry) that the fix was designed to eliminate CWD dependency for. The warning makes this visible, but the fallback does not prevent template resolution failure. A more rigorous approach would raise a `RuntimeError` with the diagnostic message so the failure is immediate and clear, rather than deferring to `Jinja2Renderer.__init__`'s `FileNotFoundError`. The current approach is methodologically adequate but not maximally rigorous.

**Improvement Path:**

Consider converting the fallback to a `RuntimeError("Cannot locate pyproject.toml above {_here}; cannot anchor repo root. Ensure CLI is run within the repository.")`. This eliminates the deferred failure mode. If the `Path.cwd()` fallback is intentionally retained for some edge case, add a docstring comment naming that use case.

---

### Evidence Quality (0.72/1.00)

**Evidence:**

What exists (unchanged from Iteration 1):
- 59/59 doc tests pass (task context assertion).
- Full suite (16,126+ tests) passes. Provides broad regression evidence.
- `test_phase1_evidence.py` tests: path traversal rejection (using `monkeypatch.chdir(tmp_path)` + `repo_root=None` default), malformed YAML handling, mode dispatch, atomic write, marker validation, sandbox environment, strict undefined, XSS sanitization, drift detection variants, and end-to-end pipeline with mocked extractor.

What is absent (unchanged from Iteration 1):
- **No test directly asserts `self._repo_root` is set correctly** when `create_docs_generator()` is called in any context.
- **No test verifies the pyproject.toml walk** resolves to the expected directory from a known anchor.
- **No test invokes `handle()` from a subdirectory CWD** and asserts that path operations use `_repo_root`, not CWD.
- **No test covers the fallback path** (`pyproject.toml` not found, fallback to `Path.cwd()`).
- AC-1 ("works when invoked from any subdirectory") has zero corresponding automated test evidence.

The grep of `tests/unit/docs/test_phase1_evidence.py` for `repo_root`, `BUG-002`, `subdirectory`, `pyproject`, and `_repo_root` returns zero matches. The revision did not add any new tests.

The binding constraint on this dimension is factual: the specific scenario BUG-002 claims to fix (subdirectory invocation) has no executable test evidence. The fix is plausible from code inspection, but plausibility is not proof.

**Gaps:**

The gap is identical to Iteration 1. No new test evidence was added in the revision cycle.

**Improvement Path:**

Add a parametrized test using `monkeypatch.chdir(tmp_path / "subdirectory")` that:
1. Creates `tmp_path / "pyproject.toml"` (empty file sufficient).
2. Creates `tmp_path / ".context" / "templates" / "docs"` (or patches the renderer).
3. Instantiates `GenerateDocsCommandHandler` with `repo_root=tmp_path`.
4. Creates `tmp_path / "README.md"` with section markers.
5. Calls `handle(GenerateDocsCommand(readme_path="README.md", mode="check"))`.
6. Asserts `result.success is True` — confirming path traversal guard passes with `self._repo_root` (not CWD subdirectory).

Add a second test that patches `Path(__file__).resolve()` to a controlled location and asserts the pyproject.toml walk stops at the correct directory. These two tests would provide direct executable evidence for the BUG-002 fix and push this dimension to 0.88-0.90.

---

### Actionability (0.96/1.00)

**Evidence:**

The Iteration 1 gap (path traversal guard using `Path.cwd()`) is closed. The handler is now coherent across all documented paths:

- Path traversal guard: `readme_abs.relative_to(self._repo_root)` — uses the injected root
- Skills discovery: `self._repo_root / _DEFAULT_SKILLS_SUBDIR` — absolute, CWD-independent
- Template data: `self._repo_root / _DEFAULT_TEMPLATE_SUBDIR` — absolute, CWD-independent

The fix is production-ready. A developer can invoke `jerry docs generate` from any subdirectory of the repository and the handler will use the composition root's `_repo_root` for all path operations. The `repo_root: Path | None = None` default preserves backward compatibility for test callers.

The fallback improvement (`Path.cwd()` + `logger.warning()` instead of silent `_here`) means that the exceptional case (no `pyproject.toml` in ancestry) is observable rather than silently misconfigured.

**Gaps:**

The 0.04 gap reflects the absence of executable verification for the subdirectory scenario. The code is correct by inspection, but "correct by inspection" is a weaker form of actionability evidence than "correct by test execution." The production behavior is reliable for the normal case; the gap is only in the evidence layer.

**Improvement Path:**

Adding the AC-1 test (described in Evidence Quality) closes this gap as a side-effect by providing executable confirmation of production-ready behavior.

---

### Traceability (0.97/1.00)

**Evidence:**

The Iteration 1 gap (BUG-002 entity `pending`, no `Completed` timestamp) is fully resolved.

BUG-002 entity now shows:
- `Status: completed`
- `Completed: 2026-03-18T00:00:00Z`
- History entry: "Fix: bootstrap.py discovers repo root via pyproject.toml walk-up; handler uses self._repo_root for all path resolution including path traversal guard. /adversary scored, revision applied. 59/59 doc tests pass."

Code-level references unchanged from Iteration 1 (all five present):
- `bootstrap.py` function docstring: "BUG-002: Template path anchored to repo root, not CWD"
- Handler class docstring: "_repo_root: Absolute path ... (BUG-002)"
- Handler `__init__` docstring: "BUG-002 fix" in parameter description
- Handler `handle()` inline comments: two BUG-002 references at lines 104 and 108

The discovery provenance ("Found by: /eng-team security-aware code review (MEDIUM-1 finding)") and resolution provenance (history entry) are both present. An auditor following the chain from code comment → entity → status now finds a closed, traceable fix.

**Gaps:**

The 0.03 gap reflects the absence of a commit reference in the history entry. The history entry documents the fix description and test evidence but does not cite a specific commit hash or PR number. This is a minor traceability gap for long-term audit.

**Improvement Path:**

Add the implementing commit hash to the BUG-002 history entry once the fix is committed. This closes the final traceability gap.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.72 | 0.88 | Add a unit test that monkeypatches CWD to a subdirectory, creates `tmp_path/pyproject.toml`, passes `repo_root=tmp_path` to handler, and asserts `handle()` succeeds (path traversal passes against `_repo_root`, not CWD) |
| 2 | Evidence Quality | 0.72 | 0.88 | Add a second unit test covering the pyproject.toml-walk discovery path in `create_docs_generator()`, asserting `_repo_root` resolves to the directory containing `pyproject.toml` |
| 3 | Evidence Quality | 0.72 | 0.88 | Add a third unit test covering the fallback path (mock `pyproject.toml` not found) and asserting `logger.warning()` is called with the expected message |
| 4 | Completeness | 0.88 | 0.93 | The above Evidence Quality tests directly satisfy AC-1; no additional completeness work needed beyond those tests |
| 5 | Methodological Rigor | 0.92 | 0.95 | Consider converting the `Path.cwd()` fallback to a `RuntimeError` for clearer failure semantics, or add an explicit docstring justification for why the fallback is intentionally silent rather than immediately fatal |
| 6 | Traceability | 0.97 | 0.99 | Add implementing commit hash to BUG-002 history entry after the fix is committed |

---

## Score Delta Summary (Iteration 1 → Iteration 2)

| Dimension | R1 Score | R2 Score | Delta | Driver |
|-----------|----------|----------|-------|--------|
| Completeness | 0.88 | 0.88 | 0.00 | Entity closure satisfied; AC-1 test gap persists |
| Internal Consistency | 0.82 | 0.95 | +0.13 | Path traversal guard fixed to use `self._repo_root` |
| Methodological Rigor | 0.90 | 0.92 | +0.02 | Fallback improved to `Path.cwd()` + `logger.warning()` |
| Evidence Quality | 0.72 | 0.72 | 0.00 | No new tests added for BUG-002 scenario |
| Actionability | 0.94 | 0.96 | +0.02 | Traversal guard gap closed; fix coherent across all paths |
| Traceability | 0.93 | 0.97 | +0.04 | Entity closed with `completed` status and history entry |
| **Composite** | **0.882** | **0.899** | **+0.017** | — |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence Quality held at 0.72 — identical to Iteration 1 because no new test evidence was added; applying leniency bias check: uncertain whether the structural fix is sufficient without execution evidence; resolved downward (stay at 0.72)
- [x] Internal Consistency moved to 0.95 — justified by concrete code-level evidence that the binding constraint (`Path.cwd()` in traversal guard) is eliminated; not rounded up to 1.00 because the CWD-based default in `__init__` is an intentional design choice that warrants documentation of the distinction
- [x] Methodological Rigor at 0.92 — improved from 0.90 due to the fallback diagnostic improvement; not scored above 0.92 because the fallback still produces a deferred failure mode rather than an immediate explicit error
- [x] No dimension scored above 0.97 without exceptional evidence — Traceability at 0.97 is justified by full entity closure plus five code-level references; the 0.03 gap reflects the absence of a commit reference
- [x] First-draft calibration considered — this is iteration 2 of a focused bug fix; the expectation for Evidence Quality remains high relative to a complex first-draft document; the 0.72 score reflects a genuine factual gap, not a lenient impression

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.899
threshold: 0.93
weakest_dimension: Evidence Quality
weakest_score: 0.72
critical_findings_count: 0
iteration: 2
improvement_recommendations:
  - "Add unit test: monkeypatch CWD to subdirectory + repo_root=tmp_path, assert handle() path traversal succeeds (AC-1 executable evidence)"
  - "Add unit test: pyproject.toml walk-up discovery — assert _repo_root resolves to pyproject.toml parent directory"
  - "Add unit test: pyproject.toml-not-found fallback — assert logger.warning() is called with diagnostic message"
  - "Consider converting Path.cwd() fallback in bootstrap.py to RuntimeError for clearer failure semantics"
  - "Add implementing commit hash to BUG-002 history entry after commit"
```
