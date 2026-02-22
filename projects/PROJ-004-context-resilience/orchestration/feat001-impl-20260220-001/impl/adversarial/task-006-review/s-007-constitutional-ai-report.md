# Constitutional Compliance Report: TASK-006 Context Window Size Detection and Configuration

**Strategy:** S-007 Constitutional AI Critique
**Deliverable:** `projects/PROJ-004-context-resilience/work/EPIC-001-context-resilience/FEAT-001-context-detection/TASK-006-context-window-configuration.md`
**Criticality:** C2 (Standard — reversible in 1 day, affects 3–10 files, no public API change)
**Date:** 2026-02-20
**Reviewer:** adv-executor agent (v1.0.0)
**Execution ID:** 20260220T1200
**Constitutional Context:** JERRY_CONSTITUTION.md v1.1, quality-enforcement.md v1.3.0, architecture-standards.md, coding-standards.md, testing-standards.md, markdown-navigation-standards.md

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall compliance assessment |
| [Findings Table](#findings-table) | All CC-NNN findings |
| [Finding Details](#finding-details) | Expanded Critical and Major findings |
| [Recommendations](#recommendations) | Prioritized remediation plan |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping and compliance score |
| [Appendix: Applicable Principles Index](#appendix-applicable-principles-index) | Constitutional context loaded |

---

## Summary

PARTIAL compliance: 1 Critical (H-08 architectural ambiguity), 2 Major (H-21 coverage gap, H-11/H-12 incomplete implementation path), 3 Minor (P-011 evidence gap, P-022 code sample incompleteness, H-20 ordering notation). Constitutional compliance score: **0.74** (REJECTED; H-13 applies, revision required).

The task specification is well-structured, clearly identifies the root cause, and correctly designs the user-authority-preserving configuration hierarchy. The primary failure is an architectural ambiguity in Step 2's implementation comment that could cause an H-08 layer boundary violation if followed literally by an implementer: the comment "Model detection from transcript happens at estimator level" implies that `ContextFillEstimator` (application layer) would call `JsonlTranscriptReader` (infrastructure layer) directly, violating H-08. A secondary Major finding is the test acceptance criteria do not include an explicit test for the wiring between `ContextFillEstimator.estimate()` and `IThresholdConfiguration.get_context_window_tokens()`, risking undetected regressions in the critical data path.

**Recommendation:** REJECT. Revision required per H-13 before implementation begins.

---

## Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| CC-001-20260220T1200 | H-08: Application layer MUST NOT import infrastructure | HARD | Critical | Step 2 comment: "Model detection from transcript happens at estimator level" — ambiguously instructs application-layer ContextFillEstimator to access transcript (infrastructure), violating layer boundary | Methodological Rigor |
| CC-002-20260220T1200 | H-21: 90% line coverage REQUIRED | HARD | Major | Acceptance criteria Tests section (lines 138–141) lists unit tests for adapter logic but omits test for the critical wiring path: `ContextFillEstimator.estimate()` → `IThresholdConfiguration.get_context_window_tokens()` integration | Completeness |
| CC-003-20260220T1200 | H-11: Type hints REQUIRED on public functions | HARD | Major | Step 3 code sample shows modified `estimate()` body without a complete function signature, making type-hint compliance of the modified method unverifiable from the specification | Internal Consistency |
| CC-004-20260220T1200 | P-011: Evidence-Based Decisions | MEDIUM | Minor | `_MODEL_CONTEXT_WINDOWS` lookup table in Step 2 includes `claude-haiku-4-5: 200_000` but Research Findings table (lines 78–82) only validates sonnet and opus window sizes; haiku's 200K assignment lacks a cited source | Evidence Quality |
| CC-005-20260220T1200 | P-022: No Deception (misleading code sample) | MEDIUM | Minor | Step 2 code sample presents `get_context_window_tokens()` as near-complete but omits model-from-transcript detection required by AC line 125 and 128, with no caveat that the sample is illustrative only | Completeness |
| CC-006-20260220T1200 | H-20: BDD Red phase — test ordering notation | HARD | Minor | Implementation Notes (Steps 1–5) use imperative construction without explicitly marking each step as post-test; no cross-reference from implementation steps back to the corresponding acceptance criterion tests | Methodological Rigor |

---

## Finding Details

### CC-001-20260220T1200: H-08 Application Layer Import Ambiguity [CRITICAL]

**Principle:** H-08 — `src/application/` MUST NOT import from `infrastructure/` or `interface/`. Violation causes architecture test failure and CI block.

**Location:** TASK-006 Implementation Notes, Step 2, lines 188–190

**Evidence:**
```python
# 3. Model lookup (if we can determine the model)
# Model detection from transcript happens at estimator level
```

**Impact:** `ContextFillEstimator` resides in the application layer (`src/context_monitoring/application/`). `JsonlTranscriptReader` resides in the infrastructure layer (`src/context_monitoring/infrastructure/`). If an implementer follows the comment literally and adds transcript-reading logic directly in `ContextFillEstimator.estimate()`, this introduces an infrastructure import into the application layer, violating H-08 and failing the architecture test gate.

The acceptance criterion at line 125 requires "`JsonlTranscriptReader` (or new method) can extract the model name" — but does not specify which layer calls it. The comment in Step 2 resolves this ambiguity in the wrong direction.

**Dimension:** Methodological Rigor

**Remediation (P0):** Revise Step 2 and Step 3 to explicitly specify that model-from-transcript detection MUST occur inside `ConfigThresholdAdapter.get_context_window_tokens()` (infrastructure layer), not in `ContextFillEstimator` (application layer). `ConfigThresholdAdapter` already holds the transcript reader reference (or must receive it via constructor injection from bootstrap.py). Remove the comment "Model detection from transcript happens at estimator level" entirely.

**Corrected Design:**
```python
# In ConfigThresholdAdapter (infrastructure) — CORRECT design:
def get_context_window_tokens(self) -> int:
    """Get context window size with detection priority.

    Priority: user config > [1m] env detection > model lookup > default 200K.
    """
    # 1. Explicit user config (highest priority)
    explicit = self._config.get_int_optional(f"{_CONFIG_NAMESPACE}.context_window_tokens")
    if explicit is not None:
        return explicit

    # 2. Check ANTHROPIC_MODEL for [1m] suffix
    model_env = os.environ.get("ANTHROPIC_MODEL", "")
    if "[1m]" in model_env:
        return _EXTENDED_CONTEXT_WINDOW

    # 3. Model lookup from transcript (infrastructure concern — stays here)
    model_name = self._transcript_reader.get_latest_model_name(self._transcript_path)
    if model_name and model_name in _MODEL_CONTEXT_WINDOWS:
        return _MODEL_CONTEXT_WINDOWS[model_name]

    # 4. Default
    return _DEFAULT_CONTEXT_WINDOW_TOKENS
```

`ContextFillEstimator` (application layer) ONLY calls `self._threshold_config.get_context_window_tokens()` — zero infrastructure imports.

---

### CC-002-20260220T1200: H-21 Missing Test for Estimator-Config Wiring [MAJOR]

**Principle:** H-21 — Test suite MUST maintain >= 90% line coverage. CI blocks merge on failure.

**Location:** Acceptance Criteria, Tests section, lines 138–141

**Evidence:**
```markdown
- [ ] Unit tests for: explicit config override, env var override, `[1m]` suffix detection,
      model lookup, default fallback
- [ ] Unit test: XML output includes `<context-window>` and `<context-window-source>`
- [ ] Existing 229 hook tests still pass (no regression)
```

**Impact:** Step 3 removes `_DEFAULT_CONTEXT_WINDOW` from `ContextFillEstimator` and changes `estimate()` to call `self._threshold_config.get_context_window_tokens()`. This is the highest-risk code change — it alters the core division operation that produces all fill percentages. No acceptance criterion test verifies that `ContextFillEstimator.estimate()` correctly uses the context window from `IThresholdConfiguration`. Without this test, the wiring could be broken (e.g., method not called, wrong parameter used) and no test would catch it. The existing 229 hook tests may not exercise this specific code path with a mocked or varied context window.

**Dimension:** Completeness

**Remediation (P1):** Add the following explicit test to the acceptance criteria Tests section:
```markdown
- [ ] Unit test: ContextFillEstimator.estimate() uses context_window from
      IThresholdConfiguration.get_context_window_tokens() — verify with mock returning 500_000
      that fill_percentage = token_count / 500_000 (not 200_000)
```

This test should be added at line 139 (before XML output test) and covers the integration between `ContextFillEstimator` and `IThresholdConfiguration`.

---

### CC-003-20260220T1200: H-11 Incomplete Type Signature in Step 3 Sample [MAJOR]

**Principle:** H-11 — All public functions and methods MUST have type annotations. mypy fails without them.

**Location:** Implementation Notes, Step 3, lines 196–202

**Evidence:**
```python
def estimate(self, transcript_path: str) -> FillEstimate:
    # ...
    context_window = self._threshold_config.get_context_window_tokens()
    fill_percentage = token_count / context_window
```

**Impact:** The `estimate()` signature fragment is shown, and does include type hints in the abbreviated snippet. However, the existing `estimate()` method signature may already have full type annotations, and the task does not confirm this. More critically, if `ContextFillEstimator` receives a new dependency (`IThresholdConfiguration`) via constructor injection (which is implied by Step 3's `self._threshold_config` reference), the `__init__` constructor must also be updated with type hints. The task does not show the modified `__init__` signature. An implementer may omit type hints on the constructor update.

**Dimension:** Internal Consistency

**Remediation (P1):** Add an explicit code sample showing the updated `ContextFillEstimator.__init__` with type hints:
```python
def __init__(self, threshold_config: IThresholdConfiguration) -> None:
    """Initialize estimator with threshold configuration.

    Args:
        threshold_config: Port providing context window and tier thresholds.
    """
    self._threshold_config = threshold_config
```

Alternatively, if `ContextFillEstimator` already receives `IThresholdConfiguration` (and only the method call is being added), document this explicitly to prevent implementer confusion.

---

### CC-004-20260220T1200: P-011 Unsubstantiated Model Entry in Lookup Table [MINOR]

**Principle:** P-011 (Evidence-Based Decisions) — Decisions SHALL be based on evidence with citations.

**Location:** Implementation Notes, Step 2, lines 163–168

**Evidence:**
```python
_MODEL_CONTEXT_WINDOWS: dict[str, int] = {
    "claude-opus-4-6": 200_000,
    "claude-sonnet-4-6": 200_000,
    "claude-haiku-4-5": 200_000,
    # Add new models here as they're released
}
```

**Impact:** The Research Findings table (lines 78–82) cites two sources validating `sonnet` and `opus` window sizes. `claude-haiku-4-5` does not appear in the cited research table. Its assignment of 200K is plausible but unverified in the task.

**Dimension:** Evidence Quality

**Remediation (P2):** Either add `claude-haiku-4-5` to the Research Findings table with a citation, or add a code comment referencing the source for haiku's 200K window size. Example:
```python
"claude-haiku-4-5": 200_000,  # https://www.anthropic.com/models/claude-haiku
```

---

### CC-005-20260220T1200: P-022 Misleading Incomplete Code Sample [MINOR]

**Principle:** P-022 (No Deception) — agents SHALL NOT deceive about actions, capabilities, or confidence levels.

**Location:** Implementation Notes, Step 2, lines 172–193

**Evidence:**
The `get_context_window_tokens()` sample in Step 2 implements detection steps 1 and 2 (config override and `[1m]` suffix) but leaves step 3 (model lookup) as a comment placeholder: "Model detection from transcript happens at estimator level." This placeholder contradicts the acceptance criterion at line 128 ("Model-to-window lookup table maps known models to their standard context windows") which implies the lookup happens in the adapter, not the estimator. The sample appears complete but omits a required detection branch.

**Dimension:** Completeness

**Remediation (P2):** Add an explicit note below the Step 2 code sample:
```
> **Note:** This sample is illustrative. Step 3 (model-from-transcript detection) is
> intentionally omitted pending resolution of the layer architecture question (see CC-001).
> Final implementation must complete steps 1–4 entirely within `ConfigThresholdAdapter`.
```

---

### CC-006-20260220T1200: H-20 Missing Back-Reference from Implementation Steps to Tests [MINOR]

**Principle:** H-20 — NEVER write implementation before the test fails (BDD Red phase).

**Location:** Implementation Notes, Steps 1–5, lines 146–227

**Evidence:** The document structure correctly places Acceptance Criteria (lines 111–141) before Implementation Notes (lines 145–227). However, none of the five implementation steps cross-reference the specific acceptance criterion test that must be written first. An implementer could execute the implementation steps sequentially without first writing the failing tests.

**Dimension:** Methodological Rigor

**Remediation (P2):** Add a header note at the top of the Implementation Notes section:
```markdown
> **BDD Requirement (H-20):** Write the failing test for each acceptance criterion BEFORE
> implementing the corresponding step. Reference the relevant AC item (e.g., "AC: Config [line 115]")
> when starting each step.
```

---

## Recommendations

### Remediation Plan

**P0 (Critical — blocks acceptance):**
- **CC-001:** Revise Step 2 implementation comment to unambiguously specify that model-from-transcript detection occurs inside `ConfigThresholdAdapter` (infrastructure layer), NOT in `ContextFillEstimator` (application layer). Remove the comment "Model detection from transcript happens at estimator level." Add corrected code sample showing `ConfigThresholdAdapter` calling `self._transcript_reader.get_latest_model_name()`. Also update bootstrap.py wiring note to show `ConfigThresholdAdapter` receives a `JsonlTranscriptReader` reference.

**P1 (Major — revision required):**
- **CC-002:** Add explicit acceptance criterion test: "`ContextFillEstimator.estimate()` uses context window from `IThresholdConfiguration.get_context_window_tokens()` — verified by mocking adapter to return 500,000 and asserting `fill_percentage = token_count / 500_000`."
- **CC-003:** Add `ContextFillEstimator.__init__` type-annotated constructor sample to Step 3 showing `threshold_config: IThresholdConfiguration` injection. Clarify whether this is a new dependency or already present.

**P2 (Minor — consider fixing):**
- **CC-004:** Add citation or inline source comment for `claude-haiku-4-5: 200_000` in the lookup table.
- **CC-005:** Add explicit "Note: illustrative sample" caveat below Step 2 code block.
- **CC-006:** Add BDD header note at top of Implementation Notes section cross-referencing the required test-first discipline.

---

## Scoring Impact

### Constitutional Compliance Score Calculation

| Violation Type | Count | Penalty Each | Total Penalty |
|---------------|-------|-------------|---------------|
| Critical | 1 | -0.10 | -0.10 |
| Major | 2 | -0.05 | -0.10 |
| Minor | 3 | -0.02 | -0.06 |
| **Total Penalty** | | | **-0.26** |

**Constitutional Compliance Score:** `1.00 - 0.26 = 0.74`

**Threshold Determination:** REJECTED (< 0.85; H-13 applies; revision required)

### S-014 Dimension Impact Table

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | CC-002 (Major): Missing test for estimator-config wiring; CC-005 (Minor): Incomplete code sample without caveat |
| Internal Consistency | 0.20 | Negative | CC-003 (Major): Incomplete `__init__` constructor signature leaves implementation compliance unverifiable; CC-001 (Critical): Comment contradicts correct architectural design |
| Methodological Rigor | 0.20 | Negative | CC-001 (Critical): Ambiguous layer guidance could cause H-08 violation at implementation; CC-006 (Minor): No test-first cross-reference in implementation steps |
| Evidence Quality | 0.15 | Negative | CC-004 (Minor): `claude-haiku-4-5` window size lacks citation |
| Actionability | 0.15 | Positive | Implementation notes are detailed and specific; configuration precedence table is clear; XML output example is concrete |
| Traceability | 0.10 | Positive | Sources cited for research findings; bootstrap.py line 585 identified precisely; related items section maps affected components |

**Positive dimensions note:** Actionability and Traceability are not affected by constitutional findings; they remain strong aspects of the deliverable that reduce rework burden once Critical/Major issues are resolved.

---

## Appendix: Applicable Principles Index

### Constitutional Principles Evaluated

| Principle | Tier | Source | Applicable | Result |
|-----------|------|--------|-----------|--------|
| H-07: Domain no external imports | HARD | architecture-standards.md | Yes — task touches arch layers | COMPLIANT |
| H-08: App no infra imports | HARD | architecture-standards.md | Yes — task specifies app/infra interaction | VIOLATED (ambiguous → Critical) |
| H-09: Composition root | HARD | architecture-standards.md | Yes — bootstrap.py wiring specified | COMPLIANT |
| H-10: One class per file | HARD | architecture-standards.md | Yes — task adds methods, no new classes | COMPLIANT |
| H-11: Type hints required | HARD | coding-standards.md | Yes — task contains public function samples | PARTIAL (Major) |
| H-12: Docstrings required | HARD | coding-standards.md | Yes — task contains public function samples | COMPLIANT |
| H-20: Test before implement | HARD | testing-standards.md | Yes — task is implementation spec | MINOR gap |
| H-21: 90% coverage | HARD | testing-standards.md | Yes — new code paths specified | MAJOR gap |
| H-23: Navigation table | HARD | markdown-navigation-standards.md | Yes — >30 line markdown | COMPLIANT |
| H-24: Anchor links in nav | HARD | markdown-navigation-standards.md | Yes — navigation table present | COMPLIANT |
| P-001: Truth and Accuracy | SOFT | JERRY_CONSTITUTION.md | Yes — factual claims about windows | COMPLIANT |
| P-002: File Persistence | MEDIUM | JERRY_CONSTITUTION.md | No — applies to agent execution | N/A |
| P-004: Explicit Provenance | SOFT | JERRY_CONSTITUTION.md | Yes — research citations present | COMPLIANT |
| P-011: Evidence-Based | SOFT | JERRY_CONSTITUTION.md | Yes — lookup table values | MINOR gap |
| P-020: User Authority | HARD | JERRY_CONSTITUTION.md | Yes — user config override design | COMPLIANT |
| P-022: No Deception | HARD | JERRY_CONSTITUTION.md | Yes — code sample completeness | MINOR gap |

### Not-Applicable Principles

| Principle | Rationale |
|-----------|-----------|
| P-002 (Persistence) | Applies to agent behavior; this is a deliverable review, not agent output |
| P-003 (No Recursion) | Applies to agent spawn control; not relevant to task spec |
| P-010 (Task Tracking) | Applies to WORKTRACKER updates during session; task spec itself is the artifact |
| P-012 (Scope Discipline) | Task is scoped to a specific bug fix; no scope creep detected |
| P-021 (Transparency) | No capabilities claimed by the task spec |
| P-030–P-031 (Collaboration) | Applies to agent handoffs, not task specification content |
| P-040–P-043 (NASA SE) | NASA SE principles apply to NSE skill agents; not applicable to framework task specs |

---

<!-- VERSION: 1.0.0 | CREATED: 2026-02-20 | EXECUTION_ID: 20260220T1200 | STRATEGY: S-007 | DELIVERABLE: TASK-006 -->
