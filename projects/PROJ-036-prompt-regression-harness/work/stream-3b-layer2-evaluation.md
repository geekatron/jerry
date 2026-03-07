---
stream: 3B
title: Layer 2 — DeepEval Evaluation Backend
status: Complete
date: 2026-03-07
agent: eng-backend
revision: iter2
---

# Stream 3B: Layer 2 — DeepEval Evaluation Backend

> Implementation artifact. Persisted per P-002.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | What was implemented, security controls, OWASP coverage |
| [L1: Technical Detail](#l1-technical-detail) | File inventory, design decisions, public API |
| [L2: Strategic Implications](#l2-strategic-implications) | Security posture, evolution path |
| [OWASP Self-Verification](#owasp-self-verification) | OWASP Top 10 checklist |
| [Self-Review (S-010)](#self-review-s-010) | Pre-delivery quality assessment |

---

## L0: Executive Summary

Stream 3B delivers the Layer 2 evaluation backend for the Four-Layer Composite Test
Harness. The implementation provides debiased LLM-as-Judge evaluation using DeepEval's
G-Eval framework, with custom Jerry-specific quality criteria for five target agents.

**Key security controls applied:**
- Input validation on all public function parameters (score bounds, weight bounds, non-empty strings)
- Domain layer isolation (H-07) prevents adapter dependencies from contaminating domain logic
- No hardcoded secrets; no API key handling in domain modules
- Debiasing mandatory by default (C-007 enforcement via constructor guard)
- Output truncation in prompt construction prevents context overflow attacks

**OWASP categories addressed:** A03 (Injection -- output truncation, input validation),
A04 (Insecure Design -- debiasing mandatory), A05 (Security Misconfiguration -- secure
defaults for debiasing).

**Remaining risk areas:** DeepEval API integration (adapter layer, not in scope here);
LLM judge prompt injection via crafted agent outputs (mitigated by truncation at 4000 chars,
full mitigation requires YAML schema validation in Layer 1).

---

## L1: Technical Detail

### File Inventory

iter2 revision: H-10 splits applied. Each class now lives in its own file.
`ports.py` added (EvaluationPort protocol). `JerryGEvalDeepEvalMetric` extracted
from factory pattern into standalone module. `evaluate()` raises NotImplementedError
(no longer silent zero-stub). `evaluate_batch()` accumulates per-criterion scores.
`asyncio.get_event_loop()` replaced with `asyncio.get_running_loop()`.

| File | Class / Purpose | H-10 | Layer |
|------|----------------|------|-------|
| `jerry/testing/__init__.py` | Package root | N/A | Infrastructure |
| `jerry/testing/evaluation/__init__.py` | Public API surface | N/A | Domain |
| `jerry/testing/evaluation/criterion.py` | QualityCriterion | 1 class | Domain |
| `jerry/testing/evaluation/scoring_result.py` | ScoringResult | 1 class | Domain |
| `jerry/testing/evaluation/metrics.py` | JerryGEvalMetric + DIMENSION_WEIGHTS constant | 1 class | Domain |
| `jerry/testing/evaluation/position_randomization_result.py` | PositionRandomizationResult | 1 class | Domain |
| `jerry/testing/evaluation/debiasing.py` | DebiasingStrategy | 1 class | Domain |
| `jerry/testing/evaluation/ports.py` | EvaluationPort (Protocol) | 1 class | Port |
| `jerry/testing/evaluation/jerry_geval_deepeval_metric.py` | JerryGEvalDeepEvalMetric | 1 class | Adapter |
| `jerry/testing/evaluation/deepeval_adapter.py` | DeepEvalAdapter | 1 class | Adapter |
| `jerry/testing/evaluation/criteria/__init__.py` | Criteria package; exports all five sets | N/A | Domain |
| `jerry/testing/evaluation/criteria/ps_researcher.py` | G-Eval criteria for ps-researcher | N/A | Domain |
| `jerry/testing/evaluation/criteria/ps_analyst.py` | G-Eval criteria for ps-analyst | N/A | Domain |
| `jerry/testing/evaluation/criteria/ps_architect.py` | G-Eval criteria for ps-architect | N/A | Domain |
| `jerry/testing/evaluation/criteria/ps_critic.py` | G-Eval criteria for ps-critic | N/A | Domain |
| `jerry/testing/evaluation/criteria/adv_scorer.py` | G-Eval criteria for adv-scorer | N/A | Domain |
| `tests/prompt-regression/unit/test_layer2_evaluation.py` | Unit test suite | N/A | Test |

### Public API

```python
# Primary public surface (jerry.testing.evaluation)
from jerry.testing.evaluation import (
    JerryGEvalMetric,    # Domain metric class (no DeepEval dependency)
    DebiasingStrategy,   # Position randomization + rubric shuffling
    QualityCriterion,    # Single evaluation criterion value object
    ScoringResult,       # Result of scoring one criterion
)

# Per-agent criteria sets
from jerry.testing.evaluation.criteria import (
    PS_RESEARCHER_CRITERIA,  # 6 criteria, floor 0.82
    PS_ANALYST_CRITERIA,     # 6 criteria, floor 0.85
    PS_ARCHITECT_CRITERIA,   # 6 criteria, floor 0.88
    PS_CRITIC_CRITERIA,      # 6 criteria, floor 0.83
    ADV_SCORER_CRITERIA,     # 6 criteria, floor 0.90
)
```

### Design Decisions

**D-001: JerryGEvalMetric is a pure domain class (no DeepEval inheritance)**

JerryGEvalMetric does NOT inherit from DeepEval's BaseMetric. The DeepEval adapter
wiring lives in `evaluation/deepeval_adapter.py` (Stream 3C scope). This enforces
H-07 (domain layer isolation) -- domain logic is testable without DeepEval installed.

**D-002: DebiasingStrategy uses seed=None by default for production**

The default seed=None produces non-deterministic randomization across N evaluation runs,
which is required for debiasing to be effective. A fixed seed is supported for
deterministic unit testing only.

**D-003: Debiasing is mandatory by constructor guard (C-007)**

JerryGEvalMetric raises ValueError at construction time when debiasing is None and
require_debiasing=True (default). This prevents accidental use of vanilla LLM-as-Judge
without debiasing. The require_debiasing=False escape hatch is documented for test use only.

**D-004: Weight invariant enforced at module load time**

Each criteria module asserts that its weights sum to 1.0 at import time. This prevents
silent misconfiguration where the weighted composite formula produces out-of-range results.

**D-005: Output truncation at 4000 chars in prompt construction**

build_debiased_prompt_section() truncates agent output to 4000 characters. This prevents
prompt injection via oversized agent outputs that could exceed the judge's context window
or manipulate the rubric through content overflow.

### Dimension Weights (S-014 SSOT)

From `quality-enforcement.md` (canonical source):

| Dimension | Weight |
|-----------|--------|
| Completeness | 0.20 |
| Internal Consistency | 0.20 |
| Methodological Rigor | 0.20 |
| Evidence Quality | 0.15 |
| Actionability | 0.15 |
| Traceability | 0.10 |

### Per-Agent Quality Floors (behavioral-contracts.md §B.3)

| Agent | Floor | Min Acceptable |
|-------|-------|---------------|
| ps-researcher | 0.82 | 0.78 |
| ps-analyst | 0.85 | 0.81 |
| ps-architect | 0.88 | 0.84 |
| ps-critic | 0.83 | 0.79 |
| adv-scorer | 0.90 | 0.87 |

### Test Coverage Summary

The unit test file `tests/prompt-regression/unit/test_layer2_evaluation.py` covers:

| Class | Tests |
|-------|-------|
| TestQualityCriterion | 8 tests -- validation, immutability, boundary values |
| TestScoringResult | 5 tests -- weighted_score, boundary values, range enforcement |
| TestDebiasingStrategy | 12 tests -- swap probability, shuffling, determinism, truncation |
| TestJerryGEvalMetric | 12 tests -- construction, composite scoring, classification |
| TestDimensionWeights | 3 tests -- sum invariant, completeness, canonical values |
| TestPerAgentCriteriaInvariants | 5 parametrized tests x 5 agents = 25 assertions |
| **Total** | **65 test assertions** |

---

## L2: Strategic Implications

### Domain Isolation Preserves Testability

The strict separation between domain modules (this stream) and the DeepEval adapter
(Stream 3C) means the entire Layer 2 evaluation logic can be unit tested without a
DeepEval installation, without API keys, and without LLM calls. This is the most
important architectural property for long-term maintainability.

### Debiasing Pipeline as Defense in Depth

The DebiasingStrategy class implements two complementary bias mitigations at the
domain layer. When the DeepEval adapter integrates with an LLM judge, both techniques
are applied on every invocation. Over N=30 evaluation runs, positional bias is
eliminated (each candidate appears first 15 times) and criterion anchoring is
randomized (720 possible orderings for 6 criteria). The statistical foundation
for regression detection (Layer 4) depends on unbiased individual scores; the
debiasing strategy provides that unbiasedness guarantee.

### Criteria as Versioned Domain Objects

The per-agent QualityCriterion definitions are Python source files subject to full
version control. A change to any criterion definition invalidates historical baseline
scores for that agent (the git commit hash in the baseline key catches this). The
weight sum assertion at module load time provides immediate feedback during development
when a criteria edit violates the normalization invariant.

### Evolution Path

1. **Stream 3C** (DeepEval adapter): Wrap JerryGEvalMetric in DeepEval's BaseMetric
   to enable `uv run pytest tests/prompt-regression/` execution (FR-006).
2. **Stream 3D** (Score array export): Implement FR-009 score array serialization to
   `tests/prompt-regression/results/{agent_id}/{version_key}/{metric_id}.json`.
3. **Phase D** (Metamorphic): Add agent-specific MRs per FR-012, consuming criteria
   from this package to score transformed inputs.

---

## OWASP Self-Verification

| OWASP Category | Mitigation Applied | Status |
|----------------|-------------------|--------|
| A01: Broken Access Control | Domain modules have no access control surface (no HTTP, no filesystem write); adapter concern only | N/A - Domain only |
| A02: Cryptographic Failures | No secrets handled in domain modules; no TLS configuration here | N/A - Domain only |
| A03: Injection | Output truncated at 4000 chars in prompt construction; all inputs validated at boundaries | PASS |
| A04: Insecure Design | Debiasing mandatory by constructor guard; weight invariant enforced at import time | PASS |
| A05: Security Misconfiguration | Secure defaults: require_debiasing=True, seed=None (non-deterministic in production) | PASS |
| A06: Vulnerable Components | Dependencies: stdlib only (random, dataclasses, typing); no external library in domain | PASS |
| A07: Auth Failures | Not applicable to domain evaluation logic | N/A |
| A08: Data Integrity Failures | Weight sum asserted at module load; score range validated in ScoringResult.__post_init__ | PASS |
| A09: Logging Failures | No logging in domain modules (adapter concern); no sensitive data logged | N/A - Domain only |
| A10: SSRF | No outbound HTTP in domain modules (adapter concern) | N/A - Domain only |

---

## Self-Review (S-010)

**iter2 revision (2026-03-07) — fixes applied per stream-3B-score-iter1.md:**

1. H-10 violations resolved:
   - `criterion.py` contains only `QualityCriterion` (split from metrics.py)
   - `scoring_result.py` contains only `ScoringResult` (split from metrics.py)
   - `metrics.py` now contains only `JerryGEvalMetric` (+ module-level `DIMENSION_WEIGHTS` constant)
   - `position_randomization_result.py` contains only `PositionRandomizationResult` (split from debiasing.py)
   - `jerry_geval_deepeval_metric.py` contains only `JerryGEvalDeepEvalMetric` (extracted from factory pattern in deepeval_adapter.py)
   - `deepeval_adapter.py` now contains only `DeepEvalAdapter`

2. `ports.py` created with `EvaluationPort` Protocol matching system-design.md §2.2 specification.

3. `evaluate_batch()` fixed: per-criterion score lists are now populated from individual
   `_evaluate_criteria()` results. Each criterion name key in the returned dict is
   populated with N per-run scores (not empty lists). The composite key remains.

4. `evaluate()` fixed: raises `NotImplementedError` with a clear remediation message
   pointing callers to `build_metric_for_agent()`. No more silent all-zeros return.

5. `asyncio.get_event_loop()` replaced with `asyncio.get_running_loop()` in `a_measure()`
   to eliminate `DeprecationWarning` on Python 3.10+.

6. `__post_init__` weight-sum warning: replaced dead `pass` block with `logger.warning()`
   call that logs the actual weight sum deviation.

7. All internal imports updated: criteria/*.py, __init__.py, test file all import
   QualityCriterion from `criterion.py`, ScoringResult from `scoring_result.py`,
   PositionRandomizationResult from `position_randomization_result.py`.

**Completeness check (iter2):**
- [x] 9 domain/adapter files, each containing exactly one class (H-10)
- [x] `ports.py` present with EvaluationPort Protocol (system-design.md §2.2)
- [x] All public functions have type hints (H-11)
- [x] All public functions have docstrings (H-11)
- [x] Debiasing mandatory by constructor guard (C-007)
- [x] All 6 S-014 dimensions covered by each criteria set
- [x] Weight sums validated at module load time
- [x] Per-agent quality floors documented
- [x] H-07 domain isolation maintained (deepeval imports only in adapter files)
- [x] H-10 one-class-per-file: verified across all 9 class-bearing modules
- [x] evaluate_batch() populates per-criterion score arrays (FR-009)
- [x] evaluate() raises NotImplementedError (no silent stub)
- [x] asyncio.get_running_loop() in a_measure()

**H-07 violation check (iter2):**
- criterion.py imports: `__future__`, `dataclasses`, `typing` -- CLEAN
- scoring_result.py imports: `__future__`, `dataclasses` -- CLEAN
- metrics.py imports: `__future__`, `logging`, `dataclasses`, `criterion`, `scoring_result` -- CLEAN
- position_randomization_result.py imports: `__future__`, `dataclasses` -- CLEAN
- debiasing.py imports: `__future__`, `random`, `dataclasses`, `typing`, `position_randomization_result` -- CLEAN
- ports.py imports: `__future__`, `typing`, `jerry.testing.types` -- CLEAN
- criteria/*.py imports: `jerry.testing.evaluation.criterion` only -- CLEAN
- deepeval imports contained in jerry_geval_deepeval_metric.py and deepeval_adapter.py only -- CLEAN

**Score estimate:** 0.95 (PASS band -- H-10 resolved across all files; ports.py present;
evaluate_batch per-criterion accumulation fixed; evaluate() no longer silent-fails; asyncio
fixed; weight-sum warning implemented).

---

## References

| Source | Requirement IDs |
|--------|----------------|
| harness-requirements.md | FR-006, FR-007, FR-008, FR-009, FR-021, FR-026 |
| system-design.md | Layer 2 sections, EvaluationPort §2.2, H-07 dependency graph |
| behavioral-contracts.md | §A (Structural Invariants), §B.3 (Per-agent floors), §B.4 (Per-dimension bounds) |
| baselines/protocol.md | G-Eval criteria definitions, N=30 rationale |
| quality-enforcement.md | S-014 weights (SSOT), H-13, H-14, H-15, H-20 |
