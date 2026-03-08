# Quality Score Report: CG-014 Unit Tests for _resolve_model()

## L0 Executive Summary

**Score:** 0.911/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Traceability (0.85)
**One-line assessment:** All five required branches are covered with sound BDD methodology, but the CG-014 work item ID is absent from the file and one docstring gap in evidence quality keeps the composite 0.009 below the 0.92 PASS threshold — a targeted two-minute fix closes the gap.

---

## Scoring Context

- **Deliverable:** `tests/prompt-regression/unit/test_resolve_model.py`
- **Deliverable Type:** Code (unit test suite)
- **Criticality Level:** C2
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.911 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.95 | 0.190 | All 5 CG-014 branches present; BDD naming on all tests; @pytest.mark.unit on all |
| Internal Consistency | 0.20 | 0.93 | 0.186 | No contradictions; pytest.raises match string confirmed in production error message |
| Methodological Rigor | 0.20 | 0.90 | 0.180 | Isolated fixtures, clean AAA structure; non-string model passthrough not covered (not required) |
| Evidence Quality | 0.15 | 0.88 | 0.132 | Per-test docstrings with CG-ID references; missing rationale for require_debiasing=False |
| Actionability | 0.15 | 0.92 | 0.138 | Immediately runnable; marker-filtered; informative assertion messages |
| Traceability | 0.10 | 0.85 | 0.085 | CG-013 and CG-024 referenced; CG-014 parent work item ID absent from file |
| **TOTAL** | **1.00** | | **0.911** | |

---

## Detailed Dimension Analysis

### Completeness (0.95/1.00)

**Evidence:**

All five branches enumerated in CG-014 requirements are covered:

1. Lowercase "claude-*" → AnthropicModel: `test_lowercase_claude_model_should_return_anthropic_model_instance` (line 83) uses "claude-sonnet-4-20250514".
2. None model → returns None: `test_none_model_should_return_none` (line 99) passes `model=None`.
3. "gpt-4" → passthrough string: `test_non_claude_model_string_should_be_returned_as_is` (line 114) uses "gpt-4" and asserts both value equality and type.
4. Mixed-case "Claude-Sonnet-*" → AnthropicModel (CG-013): `test_mixed_case_claude_model_should_return_anthropic_model_instance` (line 132) uses "Claude-Sonnet".
5. "anthropic.claude-*" → ValueError (CG-024): `test_bedrock_style_claude_model_should_raise_value_error` (line 149) uses "anthropic.claude-3-sonnet".

BDD-style `test_*_should_*` naming applied to all 5 tests (H-20 compliant). `@pytest.mark.unit` on all 5 tests. Module docstring (lines 5-16) explicitly lists all coverage goals.

**Gaps:**

The non-string passthrough branch (when `self.model` is already an `AnthropicModel` instance — production code line 404: `isinstance(self.model, str)` guard falls through to `return self.model`) is not tested. This was not listed as a CG-014 requirement, so it is not a completeness gap against the specification.

**Improvement Path:**

This dimension is essentially at ceiling for the stated requirements. Adding the non-string passthrough test would push it to 0.98+ but was not required.

---

### Internal Consistency (0.93/1.00)

**Evidence:**

No contradictions found between test claims and production behavior:

- Mixed-case test uses "Claude-Sonnet" (capital C). Production code at line 416: `self.model.lower().startswith("claude")` — this correctly matches.
- Bedrock test uses "anthropic.claude-3-sonnet". Production code at line 406: `self.model.startswith("anthropic.claude")` — this matches (lowercase input, case-sensitive check, no mismatch).
- `pytest.raises(ValueError, match="Bedrock/Vertex")` at line 158. Production error message at line 408: `"uses the Bedrock/Vertex naming convention"` — the match substring is present.
- `require_debiasing=False` in `_minimal_jerry_metric()` (line 58) is consistent with `__init__` guard at lines 111-116 which raises ValueError only when `require_debiasing is True and debiasing is None`. The fixture bypasses the guard correctly without triggering a spurious error.

**Gaps:**

The production code's `startswith("anthropic.claude")` check is case-sensitive (line 406). The test input is already lowercase, so there is no inconsistency, but there is no test for a mixed-case Bedrock identifier (e.g., "Anthropic.Claude-*"). This is a gap in consistency coverage of the production code's behavior, though not a contradiction within the test file itself.

**Improvement Path:**

Add a test for mixed-case Bedrock identifier (e.g., "Anthropic.Claude-3") to verify whether the production code correctly rejects it (it does not, since the check is case-sensitive). This would surface a latent production bug.

---

### Methodological Rigor (0.90/1.00)

**Evidence:**

- Class-based test structure (`TestResolveModel`) with clear module-level separation of helpers and tests.
- Three factory helpers (`_minimal_criterion`, `_minimal_jerry_metric`, `_make_adapter`) isolate construction complexity from test bodies. Each test constructs a fresh adapter via `_make_adapter()` — no shared mutable state.
- Pure unit testing: `_resolve_model()` is called directly; `measure()` and `a_measure()` are never invoked, so no LLM API calls are made.
- Arrange/Act/Assert structure is consistent across all 5 tests.
- Assertion error messages include actual values for debuggability.
- `@pytest.mark.unit` enables selective CI execution.

**Gaps:**

1. Non-string model passthrough not tested (not a CG-014 requirement but a methodological gap in coverage completeness of the function under test).
2. No parametrize decorator usage — five structurally similar tests could be combined via `@pytest.mark.parametrize` for the happy-path Claude variants (lowercase, mixed-case), reducing duplication while maintaining individual test visibility. This is a stylistic observation, not a rigor failure.

**Improvement Path:**

Consider parametrizing the two Claude → AnthropicModel tests (lowercase and mixed-case) into one parametrized test with two cases. Add a test for the non-string passthrough branch to maximize coverage of the function under test.

---

### Evidence Quality (0.88/1.00)

**Evidence:**

- Module-level docstring (lines 5-16) explains what each coverage target verifies and states no API key is required.
- References section in docstring lists CG-013, CG-024, H-20 by ID — enabling traceback to source requirements.
- Per-test docstrings explain the behavioral contract being verified, the before/after state (especially for CG-013), and why the behavior matters (e.g., "DeepEval falls back to its own default" for the None case).
- Assertion failure messages include actual received values (`f"... got {type(result)}"`, `f"... got {result!r}"`).
- SPDX license header and copyright line present.

**Gaps:**

`_minimal_jerry_metric()` uses `require_debiasing=False` and `debiasing=None`. No comment or docstring explains why `require_debiasing=False` is used rather than providing a real debiasing strategy. A reader unfamiliar with the `__init__` guard (production code lines 111-116) must infer that `True` would cause a ValueError. Adding one inline comment `# require_debiasing=False prevents the debiasing guard in __init__ from raising ValueError in unit test context` would fully close this gap.

**Improvement Path:**

Add one inline comment in `_minimal_jerry_metric()` explaining the `require_debiasing=False` choice. This is a two-line change that raises Evidence Quality to 0.93+.

---

### Actionability (0.92/1.00)

**Evidence:**

- Tests are immediately runnable: `uv run pytest tests/prompt-regression/unit/test_resolve_model.py -m unit`.
- No environment variables or API keys required (confirmed by module docstring and the fact that `_resolve_model()` does not make network calls — it only constructs an `AnthropicModel` object, which does not require a key at construction time).
- `_make_adapter()` factory is reusable for future CG-014 extension tests.
- Test file is self-contained: imports only from the production module, pytest, and deepeval.
- Assertion messages produce immediately actionable failure output.

**Gaps:**

`AnthropicModel(model=self.model)` construction (production line 417) may raise an exception if deepeval's `AnthropicModel.__init__` performs early validation that requires `ANTHROPIC_API_KEY` to be set. This is an external dependency on the deepeval library's behavior. The module docstring asserts "no API key is required" but this claim depends on deepeval's implementation, which is not mocked in the tests. If deepeval changes `AnthropicModel.__init__` to eagerly validate credentials, the tests would fail in CI without the key.

**Improvement Path:**

If CI does not have `ANTHROPIC_API_KEY` set, verify that `AnthropicModel("claude-sonnet-4-20250514")` construction succeeds without it (test it in dry run). Alternatively, mock `AnthropicModel.__init__` to eliminate the external library dependency entirely.

---

### Traceability (0.85/1.00)

**Evidence:**

- CG-013 referenced in module docstring (line 21) and in the mixed-case test docstring (line 134-138).
- CG-024 referenced in module docstring (line 22) and in the Bedrock test docstring (line 150-155).
- H-20 referenced in module docstring (line 23) and class docstring (line 79).
- SPDX-License-Identifier and Copyright header provide file provenance.
- `@pytest.mark.unit` connects to pytest marker taxonomy.

**Gaps:**

The CG-014 work item ID itself — the parent that scopes all five tests — does not appear anywhere in the file. Someone browsing the codebase searching for "CG-014" would not find this file. The references section lists CG-013 and CG-024 (sub-items) but not the parent work item that required them to be tested together. Adding `- CG-014: Unit tests for _resolve_model() (this file)` to the References section would close this gap.

**Improvement Path:**

Add one line to the References section: `- CG-014: Unit tests for _resolve_model() (this file covers all CG-014 required branches)`. This is a one-line change that raises Traceability to 0.93+.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Traceability | 0.85 | 0.93 | Add `- CG-014: Unit tests for _resolve_model()` to the References section in the module docstring. One-line change, closes the parent work item traceability gap. |
| 2 | Evidence Quality | 0.88 | 0.93 | Add inline comment in `_minimal_jerry_metric()` explaining why `require_debiasing=False` is used: prevents the debiasing guard in `__init__` from raising ValueError in unit test context. One-line change. |
| 3 | Methodological Rigor | 0.90 | 0.94 | Add a test for the non-string passthrough branch (model already an AnthropicModel instance). Also consider whether a mixed-case Bedrock identifier test ("Anthropic.Claude-*") is warranted to document the case-sensitive production behavior. |
| 4 | Internal Consistency | 0.93 | 0.95 | Add a test for mixed-case Bedrock identifier ("Anthropic.Claude-3-sonnet") to verify and document the case-sensitive behavior of the production `startswith("anthropic.claude")` check. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing the composite
- [x] Evidence documented for each score with specific line number references
- [x] Uncertain scores resolved downward (Traceability: 0.85 not 0.88; Evidence Quality: 0.88 not 0.90)
- [x] First-draft calibration considered — this is production-quality test code, not a rough draft, so scores above 0.85 are warranted; the 0.92+ range was reached only for dimensions with no meaningful gaps
- [x] No dimension scored above 0.95 without exceptional evidence (Completeness at 0.95 is justified by literal 5/5 branch coverage against specification)

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.911
threshold: 0.92
weakest_dimension: Traceability
weakest_score: 0.85
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Add CG-014 work item reference to module docstring References section (one-line)"
  - "Add inline comment in _minimal_jerry_metric() explaining require_debiasing=False choice"
  - "Add test for non-string model passthrough branch (AnthropicModel instance as model)"
  - "Add test for mixed-case Bedrock identifier to document case-sensitive production behavior"
```
