# S-014 LLM-as-Judge Quality Score: C-06 Injection Protection Hardening

> Scorer: adv-scorer | Strategy: S-014 LLM-as-Judge | Criticality: C2
> Anti-leniency statement: Scores below reflect strict rubric application. Leniency bias has been actively counteracted by searching for deficiencies before strengths in each dimension.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Assessment Target](#assessment-target) | Files under review |
| [Dimension Scores](#dimension-scores) | Per-dimension scoring with justification |
| [Deficiencies Found](#deficiencies-found) | Specific weaknesses identified |
| [Weighted Composite](#weighted-composite) | Final score computation |
| [Verdict](#verdict) | PASS/REVISE/REJECTED determination |

---

## Assessment Target

| Artifact | Path | Lines |
|----------|------|-------|
| Implementation | `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py` | 321 |
| Tests | `tests/unit/enforcement/test_prompt_reinforcement_engine.py` | 619 |
| Supporting dataclass | `src/infrastructure/internal/enforcement/reinforcement_content.py` | 36 |

**Scope:** Three C-06 security hardening observations applied to the L2 Prompt Reinforcement Engine:
1. Case-insensitive regex matching for injection patterns
2. Forensic WARNING-level logging on C-06 rejections
3. Expanded injection pattern coverage (iframe, object, embed, javascript:, data:text/html)

**Test execution:** 49/49 tests passed (0 failures, 0 errors, 0.13s).

---

## Dimension Scores

### 1. Completeness (Weight: 0.20)

**Score: 0.91**

**Strengths:**
- All three observations from the C-06 review are addressed: case-insensitive matching (line 134 `re.IGNORECASE`), forensic logging (lines 185-190, 196-200), expanded patterns (lines 132-135).
- Boundary test at exact max length (500 chars) is present (line 168-173).
- Both rejection paths (oversized and injection pattern) have dedicated log-verification tests (lines 211-226).
- 8 new C-06-specific tests cover the main injection vectors.

**Deficiencies:**
- No test for a marker that passes length validation but contains a closing HTML comment delimiter (`<!--`) in isolation. The existing test on line 156-160 tests `-->` within a broader scenario but does not isolate `<!--` as a standalone injection vector.
- No test for `data:text/html` with mixed case (e.g., `Data:Text/Html`), although `re.IGNORECASE` covers it. The mixed-case test exists only for `<script>` (line 175-179). This is a minor gap -- the regex handles it, but there is no explicit test proving it for every pattern variant.
- No parametrized test consolidating the injection pattern variants. Each injection vector (script, iframe, object, embed, javascript:, data:text/html) has its own test method. While this is explicit, parametrization would reduce duplication and make it trivial to add new patterns.

### 2. Internal Consistency (Weight: 0.20)

**Score: 0.96**

**Strengths:**
- Docstring on `_parse_reinject_markers` (lines 139-167) accurately describes all three C-06 protections (length check, injection pattern check, warning logging).
- Class-level comment on `_MAX_MARKER_CONTENT_LENGTH` (line 125-126) correctly references C-06 and its purpose.
- Class-level comment on `_INJECTION_PATTERNS` (lines 128-135) accurately describes the patterns and the case-insensitivity rationale.
- Variable naming is consistent: `_MAX_MARKER_CONTENT_LENGTH`, `_INJECTION_PATTERNS` follow the established private class attribute convention.
- Test docstrings consistently prefix with "C-06:" for all hardening-related tests.
- The module-level docstring (lines 4-26) references EN-002 and the engine's purpose.

**Deficiencies:**
- Line 157 docstring says "Note: The engine does NOT use declared token counts..." but uses "computes" without a subject ("It computes" would be correct). This is a minor grammatical error in the docstring, not a logic inconsistency.
- The `_INJECTION_PATTERNS` comment says "Covers: HTML comments, script/iframe/object/embed tags, JS URI schemes" but does not mention `data:text/html` explicitly in the summary comment, though it is in the regex. Minor documentation gap.

### 3. Methodological Rigor (Weight: 0.20)

**Score: 0.93**

**Strengths:**
- Defense-in-depth approach is sound: length check first (cheap), then pattern matching (more expensive). Rejection happens before the marker enters the output list.
- Compiled regex (`re.compile`) with `re.IGNORECASE` is the correct approach for case-insensitive matching -- avoids per-invocation flag passing.
- Fail-open design is maintained: C-06 rejections skip individual markers but do not fail the entire engine.
- Tests follow BDD naming convention consistently: `test_{scenario}_when_{condition}_then_{expected}`.
- Test classes are well-organized by concern: `TestParseReinjectMarkers`, `TestEstimateTokens`, `TestGenerateReinforcement`, `TestBudgetEnforcement`, `TestErrorHandling`, `TestMultiFileReading`, `TestReinforcementContent`.
- Logging uses structured format with rank identification, enabling forensic correlation.

**Deficiencies:**
- The regex pattern does not anchor the dangerous tokens within word boundaries. For example, the pattern would reject a legitimate marker containing the word "javascript:" even as part of a description like "prevents javascript: URI injection". In practice this is unlikely in L2-REINJECT content, but it is a methodological choice that trades precision for safety without documenting the false-positive risk.
- No integration test verifying that the logger output is structured in a way that forensic tooling could parse. The warning log tests check for substring presence (`"C-06"`, `"content length"`, `"injection pattern"`) but not log level or structured fields.

### 4. Evidence Quality (Weight: 0.15)

**Score: 0.94**

**Strengths:**
- 49/49 tests pass with zero failures, providing strong evidence of correctness.
- Boundary conditions are tested: exact max length (500 chars, accepted), one over (501 chars, rejected), zero budget, large budget, tiny budget.
- Each injection pattern type has a dedicated test with a meaningful assertion (`assert len(markers) == 0`).
- Log verification tests use `caplog` fixture correctly and assert on specific C-06 identifiers.
- Determinism test (line 313-321) verifies reproducibility.

**Deficiencies:**
- Assertions in some tests could be more specific. For example, `test_budget_enforcement_when_exact_budget_for_first_item_then_includes_one` asserts `>= 1` instead of `== 1` (line 378), which is weaker than the test name implies.
- No assertion on the specific log level (WARNING) in the log verification tests. The `caplog.at_level("WARNING")` context manager filters the level for capture but the assertion only checks text content, not that the log record's level is `WARNING`.

### 5. Actionability (Weight: 0.15)

**Score: 0.95**

**Strengths:**
- Code is production-ready: no TODOs, no incomplete items, no placeholder implementations.
- The compiled regex pattern is efficient for repeated invocation.
- The `_MAX_MARKER_CONTENT_LENGTH = 500` constant is clearly defined and easily adjustable.
- Fail-open behavior is maintained throughout -- no risk of blocking user prompts due to C-06 validation.
- All injection rejection paths continue processing remaining markers (using `continue` in the loop), so one malicious marker does not affect legitimate ones.

**Deficiencies:**
- The `_INJECTION_PATTERNS` regex is a class-level attribute but `_MAX_MARKER_CONTENT_LENGTH` is also class-level. Both are used only in `_parse_reinject_markers` which is a `@staticmethod`. This is consistent but means extending the pattern list requires modifying the class definition. A configuration-driven approach would be more extensible, but this is a design preference, not a deficiency per se.

### 6. Traceability (Weight: 0.10)

**Score: 0.90**

**Strengths:**
- Module docstring references EN-705, EN-002, ADR-EPIC002-002 (lines 21-25).
- C-06 is explicitly referenced in code comments (lines 125, 128-129, 182, 193), docstrings (lines 149-153), and test docstrings (every C-06 test).
- Test module docstring references EN-705 and ADR-EPIC002-002.

**Deficiencies:**
- No explicit reference to PROJ-005 in either the implementation or test files. The C-06 hardening is part of the PROJ-005 scope, and this traceability link is absent from the source code.
- The EN-002 reference in the module docstring is for the token budget update, not specifically for the C-06 injection hardening. There is no dedicated enabler/story ID for the C-06 work itself referenced in the code.
- Test file docstring (lines 4-17) does not reference C-06 or the injection hardening scope; it was not updated to reflect the new test categories.

---

## Deficiencies Found

| ID | Dimension | Severity | Description |
|----|-----------|----------|-------------|
| D-01 | Completeness | Minor | No parametrized test for injection pattern variants; each pattern tested individually |
| D-02 | Completeness | Minor | No mixed-case test for `data:text/html` or `javascript:` (only `<script>` has mixed-case test) |
| D-03 | Consistency | Trivial | Docstring line 157 missing subject ("computes" should be "It computes") |
| D-04 | Consistency | Trivial | Comment on `_INJECTION_PATTERNS` omits `data:text/html` from summary |
| D-05 | Rigor | Minor | No documentation of false-positive risk from non-word-boundary pattern matching |
| D-06 | Evidence | Minor | `test_budget_enforcement_when_exact_budget_for_first_item_then_includes_one` asserts `>= 1` not `== 1` |
| D-07 | Evidence | Minor | Log level (WARNING) not explicitly asserted in log verification tests |
| D-08 | Traceability | Minor | No PROJ-005 reference in implementation or test source files |
| D-09 | Traceability | Minor | Test file module docstring not updated for C-06 scope |

---

## Weighted Composite

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Completeness | 0.20 | 0.91 | 0.182 |
| Internal Consistency | 0.20 | 0.96 | 0.192 |
| Methodological Rigor | 0.20 | 0.93 | 0.186 |
| Evidence Quality | 0.15 | 0.94 | 0.141 |
| Actionability | 0.15 | 0.95 | 0.1425 |
| Traceability | 0.10 | 0.90 | 0.090 |
| **COMPOSITE** | **1.00** | | **0.9335** |

---

## Verdict

**PASS** (0.9335 >= 0.92 threshold)

The C-06 injection protection hardening meets the quality gate. All three security observations are addressed with sound implementation and comprehensive test coverage. The 9 deficiencies identified are all Minor or Trivial severity and do not compromise the security posture or functional correctness of the hardening.

**Recommended improvements (non-blocking):**
1. Add parametrized test for injection pattern variants to reduce duplication (D-01).
2. Add PROJ-005 traceability reference to module docstrings (D-08).
3. Strengthen the budget boundary assertion from `>= 1` to `== 1` (D-06).
4. Assert explicit WARNING log level in forensic logging tests (D-07).

---

*Scored by: adv-scorer | Strategy: S-014 LLM-as-Judge*
*Date: 2026-02-22*
*Source: EN-002 C-06 hardening, PROJ-005*
