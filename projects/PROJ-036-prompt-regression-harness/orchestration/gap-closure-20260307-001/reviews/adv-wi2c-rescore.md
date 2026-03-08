# Quality Score Report: CG-017/018/025/027 Input Validation Hardening (Rescore — Iteration 2)

## L0 Executive Summary

**Score:** 0.933/1.00 | **Verdict:** PASS | **Weakest Dimension:** Evidence Quality (0.88)
**One-line assessment:** The blocking CG-025 defect is resolved with the correct `is_relative_to()` idiom; the CG-018B annotation now carries injection-prevention rationale; test files provide explicit BDD coverage for all three CG areas — the deliverable clears the 0.92 threshold.

---

## Scoring Context

- **Deliverable:** Two files (focused re-review scope):
  - `/Users/evorun/workspace/jerry/jerry/testing/layer4_stats.py` (_validate_output_path, _emit_gha_outputs)
  - `/Users/evorun/workspace/jerry/jerry/testing/baselines/store.py` (VERSION_KEY_PATTERN, _validate_version_key)
- **Deliverable Type:** Code
- **Criticality Level:** C2 (reversible in 1 day, security-adjacent: path traversal and injection prevention)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Prior Score:** 0.884 REVISE (iteration 1, 2026-03-07)
- **Scored:** 2026-03-07T00:00:00Z (iteration 2)

---

## Revision Applied — Prior Finding Verification

**Prior blocking finding:** CG-025 used `str(resolved).startswith(str(cwd))` — a string-prefix collision antipattern that could produce false-negative containment results when a sibling directory shares a name prefix with CWD.

**Verification result:** CONFIRMED RESOLVED.

`layer4_stats.py` line 416 now reads:
```python
if not resolved.is_relative_to(cwd):
```

`str().startswith()` is absent from the file entirely (grep confirmed zero matches). The `Path.is_relative_to()` idiom is the correct Python 3.9+ containment check and eliminates the path-prefix collision edge case. This resolves the Priority 1 recommendation from iteration 1.

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.933 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | PASS |
| **Prior Score** | 0.884 REVISE |
| **Score Delta** | +0.049 |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.95 | 0.190 | All 4 CGs implemented and the CG-025 containment check is now correct; test files cover all three CG areas |
| Internal Consistency | 0.20 | 0.93 | 0.186 | All claims, docstrings, and comments remain mutually consistent; `import os` inline deviation unchanged but annotated |
| Methodological Rigor | 0.20 | 0.93 | 0.186 | CG-025 now uses the correct pathlib idiom; validate-early-fail-fast pattern holds across all four CGs |
| Evidence Quality | 0.15 | 0.88 | 0.132 | CG-018B comment now includes injection rationale; test citations present in test files; no test-citation comments in production source |
| Actionability | 0.15 | 0.93 | 0.140 | All guards production-integrated with actionable error messages; CG-025 false-negative risk eliminated |
| Traceability | 0.10 | 0.93 | 0.093 | CG-018B traceability gap closed by revised comment; FR/CG citations complete across both files |
| **TOTAL** | **1.00** | | **0.933** | |

---

## Detailed Dimension Analysis

### Completeness (0.95/1.00)

**Evidence:**

- **CG-025 fixed:** `_validate_output_path` at lines 396-421 of `layer4_stats.py` now uses `resolved.is_relative_to(cwd)` (line 416). The method resolves the path via `path.resolve()` (which follows symlinks and canonicalizes `..` sequences) and then applies the correct pathlib containment check. All prior completeness gaps for CG-025 are closed.

- **CG-018A:** Newline sanitization at lines 485 and 494 is unchanged and correct: `str(value).replace("\n", " ").replace("\r", " ")` applied symmetrically in both the GHA file-write path and the logger fallback path.

- **CG-018B:** Agent ID format validation at line 603 (`re.match(r"^[a-z][a-z0-9_-]*$", args.agent)`) is present and guards against log injection and filesystem path corruption from malformed agent IDs.

- **CG-027:** `VERSION_KEY_PATTERN = re.compile(r"^[0-9a-f]{7,40}:[^\n\r\0]+$")` at line 71 of `store.py`. Applied in `_validate_version_key` with two-stage validation (structural colon-split before regex). Pattern rejects newlines, carriage returns, and null bytes as required.

- **Test coverage:** Three test files exist covering all three CG areas:
  - `test_path_validation.py` — 4 tests for CG-025 (happy paths, `..` traversal, absolute outside-CWD)
  - `test_gha_output_sanitization.py` — 6 tests for CG-018A (newline, CR, clean values, dimension_driver, no-env fallback)
  - `test_version_key_validation.py` — 9 tests for CG-027 (short SHA, full SHA, newline, null byte, empty, no colon, uppercase, CR, path with slashes)

**Gaps:**

- Minor: `_MAX_OUTPUT_CHARS` (CG-017) lives in `deepeval_adapter.py`, which is not in scope for this re-review but was covered in the iteration 1 scoring. Within the two in-scope files, all requirements are addressed.

**Improvement Path:** None required. Score reflects near-complete implementation within scope.

---

### Internal Consistency (0.93/1.00)

**Evidence:**

- The `_validate_output_path` docstring states the method "rejects" out-of-bounds paths and raises `ValueError`; the implementation raises `ValueError` with a message that includes both the input path and the resolved path. Documented behavior and implementation are aligned.

- The CG-025 docstring (lines 397-421) accurately describes the new `is_relative_to()` mechanism: "Resolves the path to its absolute form and verifies it is contained within the current working directory." This is internally consistent with the implementation.

- `VERSION_KEY_PATTERN`'s module-level comment description matches the regex exactly: "git_hash must be 7-40 lowercase hexadecimal characters; file path must not contain newlines (\\n, \\r) or null bytes (\\0)" matches `^[0-9a-f]{7,40}:[^\n\r\0]+$`.

- `_validate_version_key` docstring lists two stages in the order they execute: "(1) Colon-split structural check ... (2) Regex format check (CG-027)." The implementation executes them in that order (lines 440-461).

**Gaps:**

- `import os` inside `_emit_gha_outputs` (line 466) remains an inline import inconsistent with the module's top-level import style. The `# noqa: PLC0415` annotation acknowledges this. It does not affect correctness or the security properties of CG-018A. This is a minor stylistic deviation that remains from iteration 1 and was not addressed by the revision.

**Improvement Path:** Move `import os` to module level. Minor; does not affect scoring materially.

---

### Methodological Rigor (0.93/1.00)

**Evidence:**

- **CG-025 methodology correction:** The prior iteration used `str(resolved).startswith(str(cwd))`, which the Python community recognizes as an antipattern for path containment testing. The current implementation uses `resolved.is_relative_to(cwd)`, the `pathlib`-native idiom introduced in Python 3.9+ for this exact purpose. The fix uses the semantically correct method rather than a string approximation.

- **Validate-early, fail-fast:** CG-027 validation fires at the top of `store()` before any I/O (line 185). CG-025 fires in `_persist_report` before any `write_text()` call. CG-018A fires at the point of value emission. CG-017 fires before `LLMTestCase` construction (in `deepeval_adapter.py`). All four follow the correct pre-condition pattern.

- **Two-stage validation in CG-027:** Structural check (colon presence, non-empty components) precedes the regex check. This produces more actionable error messages: a missing colon yields "version_key must follow the format..." rather than the less diagnostic regex-mismatch message.

- **Test methodology:** Tests use `monkeypatch.chdir()` to control CWD, making CG-025 tests portable across environments. Tests use `pytest.raises(ValueError, match="CG-025")` and `match="CG-027"` to verify both the exception type and the CG tag in the message — a strong test practice.

**Gaps:**

- The `_validate_output_path` does not check whether the parent directory exists before returning the resolved path. This is not a security gap (`_persist_report` creates parent directories via `mkdir(parents=True, exist_ok=True)`) but is a minor documentation gap: the docstring implies the path is "safe to write to," which is not quite the same as "exists."

**Improvement Path:** The gap is minor and does not affect security. No blocking improvement needed.

---

### Evidence Quality (0.88/1.00)

**Evidence:**

- **CG-025 docstring:** The revised docstring at lines 397-421 clearly states purpose ("prevent accidental or malicious writes to arbitrary filesystem locations"), mechanism (`resolve()` then `is_relative_to()`), and the raised exception. The error message at lines 417-420 includes the input path, the resolved path, and the CWD for diagnostic completeness.

- **CG-018B annotation improved:** The comment at line 599 now reads: "This prevents injection of malformed identifiers into log messages, GHA outputs, and filesystem paths." This closes the prior traceability gap by explaining how CG-018B relates to the injection-prevention family of CG-018 (both guard injection vectors, just in different channels).

- **CG-027 module-level comment:** Lines 67-71 document the pattern format, the hash length range, and the injection-prevention rationale. The `_validate_version_key` docstring explicitly cites FR-004 and both validation stages.

- **Test files as evidence chain:** The three test files provide the evidence chain from requirement to implementation. Each test file's module docstring cites the relevant CG ID and FR number. Individual test names follow BDD conventions ("should be accepted," "should raise ValueError") that express expected behavior.

**Gaps:**

1. **No test citation comments in production source:** The production source files (`layer4_stats.py`, `store.py`) do not contain inline comments pointing to the test functions that exercise each guard. For a security-relevant set of fixes, this would complete the evidence chain. Example: `# Tested: tests/prompt-regression/unit/test_path_validation.py`. This was Priority 3 in iteration 1 and was not addressed in the revision.

2. **CG-017 evidence not in scope here:** The `_MAX_OUTPUT_CHARS` constant and its CG-017 comment are in `deepeval_adapter.py`. The task asked to focus on the two in-scope files; CG-017 is not a gap within scope.

**Improvement Path:** Add test citation comments in the production source alongside each CG guard. Low effort, meaningful for audit completeness.

---

### Actionability (0.93/1.00)

**Evidence:**

- **CG-025 false-negative risk eliminated:** With `is_relative_to(cwd)` replacing the string prefix check, the containment guard is now reliable. There are no known inputs for which the guard can produce a false negative (i.e., pass a path that is actually outside CWD).

- **Error messages are actionable:** All four guards produce error messages that include the failed value, the constraint that was violated, and the CG tag:
  - CG-025: `"Output path {path} resolves to {resolved} which is outside the working directory {cwd}. Path traversal rejected (CG-025)."`
  - CG-027: `"version_key does not match required pattern '^[0-9a-f]{7,40}:[^\n\r\0]+$' (CG-027)..."` with explicit description of the hash length, allowed characters, and forbidden characters.

- **Test actions are actionable:** The `pytest.raises(ValueError, match="CG-025")` pattern in the path validation tests makes failure mode explicit to future maintainers: when the guard breaks, tests produce a clear failure message that identifies the CG and the expected exception type.

- **All guards are integrated into production code paths.** None are stubs or conditionally disabled.

**Gaps:**

- The `test_path_traversal_outside_cwd_should_raise_value_error` test uses `work_dir / ".." / "secret.json"` as the escaping path. This is a relative-style `..` path. The test for an absolute path outside CWD covers the complementary case. Both cases are exercised. No actionability gap.

**Improvement Path:** None required within scope.

---

### Traceability (0.93/1.00)

**Evidence:**

- **CG-018B traceability gap closed:** The revised comment at line 599-602 now explains that the CG-018B agent ID validation "prevents injection of malformed identifiers into log messages, GHA outputs, and filesystem paths." This links the implementation to the injection-prevention family that CG-018 belongs to, resolving the traceability ambiguity identified in iteration 1.

- **CG cross-references present at implementation sites:** CG tags appear inline at every guard: `CG-025` in `_validate_output_path` docstring and `_persist_report` docstring; `CG-027` at line 67 (module comment) and line 451 (docstring); `CG-018A` at lines 482 and 493; `CG-018B` at line 599.

- **FR references:** FR-004 cited in `_validate_version_key` docstring; FR-018 cited in `_emit_gha_outputs` docstring; FR-020 cited in `store.py` module docstring.

- **Test-to-requirement traceability:** Each test file's module docstring lists the CG IDs and FR numbers it exercises. Individual tests include the CG ID in the docstring ("CG-025," "CG-027," "CG-018A"). The `VERSION_KEY_PATTERN` constant is module-level and independently importable, making it directly testable by name (confirmed: `test_version_key_validation.py` imports `VERSION_KEY_PATTERN` directly at line 23).

**Gaps:**

1. **No bidirectional link to requirements document:** Production source files do not link back to the gap analysis document that originated the CGs. This remains from iteration 1. The CG numbers alone are sufficient for traceability within the project's gap-closure workflow, but a path reference to the gap analysis would make the chain unambiguous for external reviewers.

**Improvement Path:** Add a reference to the gap analysis path in module-level docstrings for security-relevant guards. Minor; does not affect scoring materially.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.88 | 0.92 | Add test citation comments in production source alongside each CG guard (e.g., `# Tested: tests/prompt-regression/unit/test_path_validation.py`). Completes the evidence chain from requirement to implementation to test within the source file itself. |
| 2 | Internal Consistency | 0.93 | 0.95 | Move `import os` in `_emit_gha_outputs` to module level; remove the `# noqa: PLC0415` suppressor. Removes a stylistic inconsistency that is currently annotated but not resolved. |
| 3 | Traceability | 0.93 | 0.95 | Add a reference to the gap analysis document path (e.g., `gap-analysis-20260307-001/`) in the module-level docstrings of `layer4_stats.py` and `store.py` for the security-relevant CG implementations. |

---

## Leniency Bias Check

- [x] Each dimension scored independently
- [x] Evidence documented for each score (specific line numbers cited throughout)
- [x] Uncertain scores resolved downward — Evidence Quality held at 0.88 (not 0.90) because test citation comments in production source remain absent; Completeness held at 0.95 (not 1.00) because CG-017 is not in scope
- [x] First-draft calibration considered — this is a revised deliverable; 0.933 is appropriate for "good implementation with one known minor gap remaining"
- [x] No dimension scored above 0.95 without exceptional evidence — Completeness at 0.95 is justified by four CGs implemented plus three test files with full BDD coverage

---

## Session Context Handoff

```yaml
verdict: PASS
composite_score: 0.933
threshold: 0.92
weakest_dimension: Evidence Quality
weakest_score: 0.88
critical_findings_count: 0
blocking_findings: []
iteration: 2
prior_score: 0.884
score_delta: +0.049
improvement_recommendations:
  - "Add test citation comments in production source alongside each CG guard"
  - "Move import os to module level in layer4_stats.py"
  - "Add gap analysis document path reference in module-level docstrings"
resolved_findings:
  - "CG-025: resolved.is_relative_to(cwd) confirmed at layer4_stats.py:416 (was str.startswith)"
  - "CG-018B: injection-prevention rationale now present in comment at line 599-602"
  - "Test coverage: three BDD test files with CG-tagged tests added"
```
