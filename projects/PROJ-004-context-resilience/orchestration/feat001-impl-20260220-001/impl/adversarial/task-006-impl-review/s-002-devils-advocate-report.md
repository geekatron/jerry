# S-002 Devil's Advocate Report — TASK-006 Implementation Review

<!-- VERSION: 1.0.0 | DATE: 2026-02-20 | STRATEGY: S-002 Devil's Advocate -->
<!-- PRECONDITION: S-003 Steelman completed (10 HIGH-robustness strengths identified) -->
<!-- H-16 SATISFIED: Steelman executed before Devil's Advocate -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Scope, preconditions, methodology |
| [Challenge 1: 3-Step vs 5-Step Detection](#challenge-1-3-step-vs-5-step-detection) | Premature simplification argument |
| [Challenge 2: Fail-Open Default](#challenge-2-fail-open-default) | Safety case for fail-closed |
| [Challenge 3: No Caching of Detection Results](#challenge-3-no-caching-of-detection-results) | Double invocation waste |
| [Challenge 4: 200K Default Assumption](#challenge-4-200k-default-assumption) | Future-model fragility |
| [Challenge 5: ANTHROPIC_MODEL Dependency](#challenge-5-anthropic_model-dependency) | Undocumented convention brittleness |
| [Challenge 6: Absent Bootstrap Default](#challenge-6-absent-bootstrap-default) | Invisible footgun |
| [Challenge 7: Double Zero Guard](#challenge-7-double-zero-guard) | Redundancy as code smell |
| [Consolidated Risk Register](#consolidated-risk-register) | All 7 challenges ranked |
| [Required Actions](#required-actions) | STRONG-rated items only |

---

## Overview

**Deliverable under review:** TASK-006 Context Window Size Detection and Configuration
**Strategy applied:** S-002 Devil's Advocate — challenge every design decision with the strongest possible counterargument
**Precondition:** S-003 Steelman completed; 10 HIGH-robustness strengths identified
**H-16 compliance:** Steelman-before-critique ordering satisfied

**Core files reviewed:**
- `src/context_monitoring/infrastructure/adapters/config_threshold_adapter.py` (lines 222-261)
- `src/context_monitoring/application/services/context_fill_estimator.py` (lines 130-165)
- `src/context_monitoring/application/ports/threshold_configuration.py`
- `src/context_monitoring/domain/value_objects/fill_estimate.py`
- `src/bootstrap.py` (lines 575-600)
- `tests/unit/context_monitoring/test_config_threshold_adapter.py`
- `tests/unit/context_monitoring/application/test_context_fill_estimator.py`

**Challenge rating scale:**
- **STRONG** — Genuine concern that, if valid, would require design change
- **MODERATE** — Valid concern, manageable with documentation or minor mitigation
- **WEAK** — Theoretically valid but practically irrelevant in this context

---

## Challenge 1: 3-Step vs 5-Step Detection

**Design decision:** The TASK-006 spec originally proposed 5 detection steps (including Anthropic API capability query and /proc filesystem inspection). The implementation simplifies to 3 steps: explicit config > `ANTHROPIC_MODEL [1m]` suffix > 200K default.

**Devil's Advocate Counterargument:**

The two dropped steps — API-based capability detection and /proc filesystem inspection — were dropped for reasons unstated in the implementation. This is a silent scope reduction masquerading as a simplification. The implementation comments justify only the kept steps; there is no audit trail explaining *why* API detection was removed. The consequences of this omission are non-trivial:

*Step 4 (API detection):* If a Claude model exposes its context window size via an API endpoint (e.g., via the Anthropic model metadata endpoint), that source is authoritative and cannot be spoofed by a misconfigured environment variable. An operator could set `ANTHROPIC_MODEL=claude-sonnet[1m]` even when running against a standard 200K model — the `[1m]` suffix check would then silently return 1,000,000 tokens when the true window is 200,000. An API-sourced detection step would catch this misconfiguration. By not implementing it, the code makes an incorrect detection indistinguishable from a correct one.

*Step 5 (/proc inspection):* On Linux-hosted Claude Code deployments (container or server environments), the process environment may carry Claude-specific context configuration in ways not reflected by `ANTHROPIC_MODEL`. The /proc-based step would provide a fallback for non-standard deployment topographies. Dropping it means the 3-step chain has no path for Linux server deployments with atypical env var configurations.

Furthermore, the decision to stop at 3 steps is recorded only in a comment on line 63 (`# [1m] suffix convention: used in Claude Code model alias configuration`), which explains the detection method but not the decision to exclude the other two steps. This violates documentation standards for architectural decisions — the simplification should be captured in an ADR, not left as an implicit design choice.

**Evidence from code:**
```python
# config_threshold_adapter.py lines 59-64
# [1m] suffix convention: used in Claude Code model alias configuration
# to select extended context (1M tokens).
# Source: https://code.claude.com/docs/en/model-config
# Examples: sonnet[1m], opus[1m]
# Detection uses endswith("[1m]") to avoid false positives.
_EXTENDED_CONTEXT_SUFFIX: str = "[1m]"
```
No comment or ADR explains why steps 4 and 5 were dropped.

**What would change if this concern is valid:** An ADR should be written recording the decision to exclude API-based and /proc-based detection, with explicit rationale (complexity, test surface area, API availability uncertainty). Without this ADR, future contributors may re-implement one of the dropped steps inconsistently.

**Rating: MODERATE**

The 3-step simplification is defensible on complexity grounds. API detection introduces a network dependency (fragile for offline/air-gapped deployments). /proc inspection introduces a platform dependency (non-portable to macOS/Windows). The practical risk of environment misconfiguration with `[1m]` suffix is bounded by the fact that it requires user action to set incorrectly. However, the *absence of a recorded decision* is a genuine traceability gap, which keeps this from being WEAK.

---

## Challenge 2: Fail-Open Default

**Design decision:** `_detect_context_window()` returns `(_DEFAULT_CONTEXT_WINDOW_TOKENS, "default")` (200K) on any detection failure. The estimator's catch-all handler returns `_FAIL_OPEN_ESTIMATE` (NOMINAL, fill=0.0) on any exception. Both layers choose fail-open over fail-closed.

**Devil's Advocate Counterargument:**

Fail-open is the wrong default for a context resilience system. The entire purpose of PROJ-004 is to prevent context exhaustion from causing unrecoverable failures. A fail-open policy in the detection layer creates an insidious failure mode: if detection silently falls back to 200K when the actual window is 1M, the monitoring system will produce false-positive EMERGENCY alerts at 88% of 200K (176K tokens), which is only 17.6% of the actual 1M window. This is annoying but manageable — the user gets warnings too early.

However, the inverse is more dangerous: if detection silently falls back to 200K when the actual window is 100K (e.g., a budget model or constrained deployment), the monitoring system will never reach EMERGENCY threshold until 176K tokens, which is 76K tokens *beyond* the actual context limit. The system would silently allow context exhaustion to occur, producing exactly the failure PROJ-004 is designed to prevent.

The estimator's fail-open logic compounds this. In `context_fill_estimator.py` lines 159-165:
```python
except Exception as exc:  # noqa: BLE001
    logger.warning(
        "Context estimation failed for %s: %s (fail-open -> NOMINAL)",
        transcript_path,
        exc,
    )
    return _FAIL_OPEN_ESTIMATE
```
A NOMINAL estimate when the system has failed is a lie. The returned `FillEstimate` has `fill_percentage=0.0` and `tier=NOMINAL`, suggesting context is healthy when in fact monitoring has completely broken down. Any downstream system consuming this estimate — for example, a hook that suppresses checkpoint warnings at NOMINAL — will behave as if everything is fine.

A fail-closed alternative would return an EMERGENCY-tier sentinel with `token_count=None` and a distinct source label (e.g., `"monitoring-failure"`), so callers can distinguish a genuine NOMINAL reading from a monitoring failure. This is especially important for C3/C4 sessions where context exhaustion risk is highest.

**Evidence from code:**
```python
# config_threshold_adapter.py lines 257-258
except Exception:  # noqa: BLE001
    pass  # fail-open: any detection error returns default
```

```python
# context_fill_estimator.py line 56-60
_FAIL_OPEN_ESTIMATE = FillEstimate(
    fill_percentage=0.0,
    tier=ThresholdTier.NOMINAL,
    token_count=None,
)
```

**What would change if this concern is valid:** The `_FAIL_OPEN_ESTIMATE` sentinel should use a dedicated tier (e.g., `ThresholdTier.UNKNOWN`) or a flag field to distinguish "monitoring failed" from "context is genuinely nominal." Alternatively, a third option between fail-open and fail-closed: return a CRITICAL sentinel on monitoring failure, triggering a checkpoint as a safe default.

**Rating: STRONG**

This is a genuine architectural concern. The fail-open policy is appropriate for detection failures where the fallback (200K default) is *probably* correct. But the estimator-level fail-open — returning NOMINAL when monitoring has broken — is distinguishable from "context is healthy." The current implementation makes these two states indistinguishable to callers, which could suppress correct checkpoint behavior in production.

---

## Challenge 3: No Caching of Detection Results

**Design decision:** `_detect_context_window()` is a private method called by both `get_context_window_tokens()` and `get_context_window_source()`. The `estimate()` method in `ContextFillEstimator` calls both methods sequentially (lines 137-138).

**Devil's Advocate Counterargument:**

The `estimate()` method calls the detection chain twice per invocation:
```python
# context_fill_estimator.py lines 137-138
context_window = self._threshold_config.get_context_window_tokens()
context_window_source = self._threshold_config.get_context_window_source()
```
Each call invokes `_detect_context_window()` on the adapter, which reads from `LayeredConfigAdapter` and calls `os.environ.get()`. While the actual cost per call is negligible (microseconds), the design has three subtler problems:

*Problem 1 — Consistency gap:* If `ANTHROPIC_MODEL` changes between the two calls — which is theoretically possible in a multithreaded environment or if another thread modifies env vars — the returned `(tokens, source)` pair would be inconsistent: tokens from one detection run, source from another. The current implementation has no atomicity guarantee between the two public methods.

*Problem 2 — Contract violation:* The `IThresholdConfiguration` port does not document that `get_context_window_tokens()` and `get_context_window_source()` are guaranteed to be consistent when called sequentially. A naive implementer could return different detection results from each method without violating the protocol specification. The estimator silently assumes consistency.

*Problem 3 — Repeated I/O in hot paths:* Context monitoring runs on every prompt submission (via the `HooksPromptSubmitHandler`). In a long session, `estimate()` is called hundreds of times. While env-var reads are fast, TOML config reads (`LayeredConfigAdapter.get()`) may involve file I/O or parsing on each call if the adapter does not cache internally. If `LayeredConfigAdapter` does not cache, this is redundant I/O on every estimation.

**Evidence from code:**
```python
# config_threshold_adapter.py lines 206-219
def get_context_window_tokens(self) -> int:
    tokens, _ = self._detect_context_window()
    return tokens

def get_context_window_source(self) -> str:
    _, source = self._detect_context_window()
    return source
```

The `_detect_context_window` internal DRY comment acknowledges the design:
```python
"""Single detection method to prevent DRY violations between
get_context_window_tokens() and get_context_window_source()."""
```
But DRY compliance does not address the consistency or caching concerns.

**What would change if this concern is valid:** Cache the `(tokens, source)` tuple in `__init__` or on first call. Alternatively, expose `get_context_window()` as a single method returning both values, forcing consumers to call once and unpack. This would also require updating the `IThresholdConfiguration` port.

**Rating: MODERATE**

The consistency gap is real but bounded — env var modification between two consecutive calls in the same thread is unlikely. The lack of caching is a performance concern only if `LayeredConfigAdapter` does not cache internally (which should be verified). The contract documentation gap is a genuine MEDIUM concern.

---

## Challenge 4: 200K Default Assumption

**Design decision:** `_DEFAULT_CONTEXT_WINDOW_TOKENS: int = 200_000` is hardcoded as the fallback when no config and no `[1m]` detection applies.

**Devil's Advocate Counterargument:**

The 200K default encodes an assumption about Anthropic's Pro/Team product tier that has already changed once (Claude was originally 100K). It will change again. More critically, the default is wrong for multiple active deployment scenarios today:

1. **Haiku models:** Claude 3 Haiku has a 200K context window, but Claude 3.5 Haiku variants on some API plans have different limits. Hardcoding 200K may be wrong for a specific model version.

2. **Batch API deployments:** The Anthropic Batch API has different effective context limits per request slot. A Jerry deployment running batch mode would get incorrect fill estimates.

3. **Enterprise custom limits:** Enterprise customers with custom context window allocations (e.g., 500K as mentioned in the code comments) will not have the `[1m]` suffix — they use explicit config. But if they forget to set `JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS`, they silently get 200K math applied to a 500K actual window.

4. **Future model tiers:** If Anthropic introduces a "2M" tier or a "512K" tier, this detection chain cannot express those values without code changes. The `[1m]` detection is hard-coded to exactly 1,000,000; there is no `[2m]` path, no `[512k]` path, and no runtime extensibility mechanism.

The 200K default is not documented as "correct for Pro/Team Standard" in the constant definition — it appears as a bare magic number:
```python
_DEFAULT_CONTEXT_WINDOW_TOKENS: int = 200_000
```
A future maintainer editing this constant has no documentation indicating what deployment profile it represents.

**Evidence from code:**
```python
# config_threshold_adapter.py lines 56-57
_DEFAULT_CONTEXT_WINDOW_TOKENS: int = 200_000
_EXTENDED_CONTEXT_WINDOW: int = 1_000_000
```

**What would change if this concern is valid:** The constant should be documented with its deployment context ("Pro/Team Standard 200K context window as of 2026-02"). An ADR should record the decision to use 200K as the default, with a note to revisit when Anthropic changes model families. The detection chain should ideally be designed to accommodate future suffixes (e.g., `[2m]`) without code changes, perhaps via a configurable suffix-to-tokens map.

**Rating: MODERATE**

The concern is real but the escape hatch (explicit config via `JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS`) already exists. Any user on a non-standard model can set the exact value. The default being "wrong" for edge cases is self-correcting through the explicit config path. The absence of documentation on the constant and the absence of an extensibility mechanism for future suffixes keep this from being WEAK.

---

## Challenge 5: ANTHROPIC_MODEL Dependency

**Design decision:** The `[1m]` suffix detection reads `os.environ.get("ANTHROPIC_MODEL", "")` and checks `endswith("[1m]")`.

**Devil's Advocate Counterargument:**

`ANTHROPIC_MODEL` is a Claude Code internal environment variable, not part of the Anthropic public API specification. The code comments reference `https://code.claude.com/docs/en/model-config` as the source, but:

1. **Undocumented contract:** The `[1m]` suffix convention is a Claude Code implementation detail, not a guaranteed stable interface. Anthropic could change the suffix format (e.g., to `[-1m]`, `[1M]`, or drop it entirely in favor of a separate env var) in any Claude Code update. There is no public SLA on `ANTHROPIC_MODEL` format stability.

2. **Case sensitivity footgun:** The check `endswith("[1m]")` is case-sensitive. If Claude Code ever produces `ANTHROPIC_MODEL=claude-sonnet-4-6[1M]` (uppercase M), detection would silently fail and fall back to 200K. The test `test_endswith_not_substring` verifies the suffix must be exact — but it does not test case sensitivity. A user who manually sets `ANTHROPIC_MODEL=sonnet[1M]` would get the wrong result with no error or warning.

3. **Embedding ambiguity:** The `endswith("[1m]")` check correctly rejects `my-custom-[1m]-wrapper` (proven by `test_endswith_not_substring`). But what about `claude-[1m]-extended[1m]`? This would be detected as 1M. The exact format of a valid `[1m]` suffix model alias is never validated — only the suffix is checked. Any string ending in `[1m]` will be detected as 1M context.

4. **No fallback on env var absence:** If `ANTHROPIC_MODEL` is absent (step 2 skipped silently), the code falls directly to the 200K default. For a Claude Code session running with an extended context model but without `ANTHROPIC_MODEL` set (e.g., a subprocess or non-standard launcher), detection silently yields the wrong default.

**Evidence from code:**
```python
# config_threshold_adapter.py lines 252-258
try:
    # 2. Check ANTHROPIC_MODEL env var for [1m] suffix
    model_env = os.environ.get("ANTHROPIC_MODEL", "")
    if model_env.endswith(_EXTENDED_CONTEXT_SUFFIX):
        return _EXTENDED_CONTEXT_WINDOW, "env-1m-detection"
except Exception:  # noqa: BLE001
    pass  # fail-open: any detection error returns default
```

The `try/except Exception` block wrapping `os.environ.get()` is also suspicious: `os.environ.get()` cannot raise `Exception` under normal Python execution. The try/except is dead code that provides false safety theatre.

**What would change if this concern is valid:** The detection should be documented as "best-effort; depends on Claude Code internal convention." The case sensitivity issue should be addressed with `.lower()` normalization. The `try/except` around `os.environ.get()` should be removed as dead code (or the comment should explain a hypothetical exception scenario). A log message should be emitted when `ANTHROPIC_MODEL` is set but does not end with `[1m]`, so users can diagnose misconfiguration.

**Rating: STRONG**

The case sensitivity issue is a real defect: `endswith("[1m]")` will silently fail for uppercase `[1M]`. This is not a hypothetical; users who manually set `ANTHROPIC_MODEL` may use any capitalization. The `try/except` around `os.environ.get()` is dead code that creates a false impression of defensive programming. Both are actionable defects.

---

## Challenge 6: Absent Bootstrap Default

**Design decision:** `context_window_tokens` is intentionally excluded from the `defaults` dict in `bootstrap.py` (lines 584-594), with a comment explaining why.

**Devil's Advocate Counterargument:**

The detection chain in `_detect_context_window()` works by checking `self._config.get(key)` for `context_monitor.context_window_tokens` first. If this key returns `None` (absent from config), detection falls through to the `[1m]` check. This requires that the `LayeredConfigAdapter` returns `None` when the key is absent from all layers, and that `context_window_tokens` is not present in the `defaults` dict.

This is a **hidden constraint on the bootstrap configuration**: if any future maintainer adds `"context_monitor.context_window_tokens": 200000` to the defaults dict (as a "helpful" default alongside the other five threshold keys), the detection chain silently breaks. The `[1m]` detection step and explicit-config-takes-priority behavior would both become unreachable. The 200K default would always be used, and monitoring would never auto-detect 1M model aliases.

The bootstrap comment warns about this:
```python
# NOTE: context_window_tokens is intentionally NOT in defaults.
# The adapter must distinguish "user explicitly configured" from
# "default" to support auto-detection priority chain (TASK-006).
```
But the comment is co-located with the bootstrap instantiation, not with the adapter or the port. A contributor modifying `config_threshold_adapter.py` or `IThresholdConfiguration` would not see this constraint unless they also read `bootstrap.py`.

Furthermore, the architecture relies on the semantic distinction between "key absent" (None return) and "key present with value 200000" to encode "use auto-detection" vs. "user explicitly set this." This is a non-obvious convention that is not expressed in the type system. The port interface says `get_context_window_tokens() -> int` with no way to signal "use auto-detection."

**Evidence from code:**
```python
# bootstrap.py lines 584-594
defaults={
    # NOTE: context_window_tokens is intentionally NOT in defaults.
    # The adapter must distinguish "user explicitly configured" from
    # "default" to support auto-detection priority chain (TASK-006).
    "context_monitor.nominal_threshold": 0.55,
    "context_monitor.warning_threshold": 0.70,
    "context_monitor.critical_threshold": 0.80,
    "context_monitor.emergency_threshold": 0.88,
    "context_monitor.compaction_detection_threshold": 10000,
    "context_monitor.enabled": True,
}
```

```python
# config_threshold_adapter.py lines 232-234
key = f"{_CONFIG_NAMESPACE}.context_window_tokens"
explicit = self._config.get(key)
if explicit is not None:
```

**What would change if this concern is valid:** The constraint "context_window_tokens MUST NOT be in bootstrap defaults" should be enforced by a test that directly inspects the bootstrap defaults dict, or by a startup assertion in the adapter itself that fails loudly if the key is pre-populated. Additionally, the design decision should be captured in an ADR, not only in a comment. The adapter could also move the default-exclusion logic internally (e.g., using a sentinel value for "auto-detect") rather than relying on absent-vs-present semantics in the config system.

**Rating: STRONG**

This is the most significant architectural concern in the review. The correct functioning of the entire detection chain depends on an invisible invariant: a specific key must be absent from one specific dict in one specific file. There is no test, assertion, or type-system mechanism enforcing this invariant. It is a silent footgun that will be triggered by any maintainer who adds the "missing" default key as a cleanup action.

---

## Challenge 7: Double Zero Guard

**Design decision:** Zero/negative context window values are guarded in *two* separate places: once in `_detect_context_window()` (adapter, lines 237-242) and once in `estimate()` (estimator, lines 141-147).

**Devil's Advocate Counterargument:**

The adapter already validates that `context_window_tokens > 0` before returning a value from explicit config. The adapter cannot return zero or negative from the `[1m]` path (1,000,000 is always positive) or from the default path (200,000 is always positive). Therefore, the estimator's guard at lines 141-147 is logically unreachable code when using `ConfigThresholdAdapter`:

```python
# context_fill_estimator.py lines 141-147
if context_window <= 0:
    logger.warning(
        "Invalid context window %d; falling back to 200K default.",
        context_window,
    )
    context_window = 200_000
    context_window_source = "default"
```

This unreachable guard has two negative effects:

*Effect 1 — Port contract looseness:* The existence of the guard in the estimator implies that `IThresholdConfiguration.get_context_window_tokens()` may legally return zero or negative values. This is a looser contract than necessary. The port's docstring says it returns `The context window size in tokens` but does not state `Returns a positive integer.` A type annotation of `int` permits any integer. The estimator's defensive guard compensates for a port contract that is underspecified.

*Effect 2 — Testing theater:* `TestEstimatorContextWindowGuard` in the estimator tests exercises the estimator's fallback for zero/negative context windows. But these tests use `FakeThresholdConfiguration(context_window_tokens=0)`, which bypasses the adapter's own guard. In production, a zero value would be caught and rejected at the adapter layer before reaching the estimator. The estimator tests are testing a scenario that the adapter guard already prevents — adding test coverage for a path that cannot occur in the real wiring.

The correct solution is to tighten the port contract (`get_context_window_tokens() -> int` with a documented invariant `value > 0`), trust the adapter to enforce it, and remove the defensive estimator guard. The estimator's catch-all `except Exception` block already handles cases where `get_context_window_tokens()` throws entirely, which is the actual failure mode to guard against.

**Evidence from code:**
```python
# config_threshold_adapter.py lines 237-242 (adapter guard)
if value <= 0:
    logger.warning(
        "Invalid context_window_tokens=%d (must be > 0); "
        "falling through to auto-detection.",
        value,
    )

# context_fill_estimator.py lines 141-147 (estimator guard)
if context_window <= 0:
    logger.warning(
        "Invalid context window %d; falling back to 200K default.",
        context_window,
    )
    context_window = 200_000
    context_window_source = "default"
```

**What would change if this concern is valid:** The port contract should be tightened with a documented postcondition (`value > 0`). The estimator guard should be removed or reduced to an assertion (`assert context_window > 0`). The estimator test class `TestEstimatorContextWindowGuard` should be revised — the zero/negative cases are adapter-layer concerns and should only be tested there.

**Rating: MODERATE**

The double guard is redundant rather than harmful — having defense in depth at two layers is generally better than having it at one. The concern is a code quality/contract precision issue, not a safety issue. However, it does reveal a genuine underspecification in the port contract and creates misleading test coverage that implies the estimator handles invalid adapter output that the real adapter cannot produce.

---

## Consolidated Risk Register

| # | Challenge | Rating | Evidence Location | If Valid: Change Required |
|---|-----------|--------|-------------------|--------------------------|
| 1 | 3-step vs 5-step: missing ADR for dropped steps | MODERATE | No ADR exists; comment on line 63 only | Write ADR for detection simplification decision |
| 2 | Fail-open: NOMINAL sentinel indistinguishable from genuine health | STRONG | `_FAIL_OPEN_ESTIMATE` line 56-60; `except` block line 159-165 | Add `monitoring_failed` flag to `FillEstimate` or use distinct tier |
| 3 | No caching: double invocation, consistency gap, undocumented contract | MODERATE | Lines 206-219 adapter; lines 137-138 estimator | Cache detection result; document port consistency contract |
| 4 | 200K default: undocumented model profile assumption, no extensibility | MODERATE | `_DEFAULT_CONTEXT_WINDOW_TOKENS` line 56 | Document constant; add suffix-to-tokens config map |
| 5 | ANTHROPIC_MODEL: case sensitivity defect, dead try/except | STRONG | Lines 252-258; `endswith("[1m]")` | Add `.lower()` normalization; remove dead try/except |
| 6 | Bootstrap absent-key invariant: no enforcement, invisible footgun | STRONG | `bootstrap.py` lines 584-594; adapter lines 232-234 | Add test or assertion to enforce invariant; write ADR |
| 7 | Double zero guard: redundant, underspecified port contract | MODERATE | Adapter lines 237-242; estimator lines 141-147 | Tighten port postcondition; remove estimator guard |

---

## Required Actions

Only STRONG-rated items require immediate action per quality enforcement standards.

### Action 1 — Fix case sensitivity in `[1m]` detection (Challenge 5)

**File:** `src/context_monitoring/infrastructure/adapters/config_threshold_adapter.py`
**Line:** 255
**Change:** Replace `model_env.endswith(_EXTENDED_CONTEXT_SUFFIX)` with `model_env.lower().endswith(_EXTENDED_CONTEXT_SUFFIX.lower())` or normalize the input before comparison.
**Also:** Remove or justify the `try/except Exception` block wrapping `os.environ.get()` (line 252-258). Document why the block exists if it must remain.

### Action 2 — Enforce bootstrap absent-key invariant (Challenge 6)

**File:** `tests/unit/context_monitoring/test_config_threshold_adapter.py` (or a new integration test)
**Change:** Add a test that inspects the defaults dict passed to `LayeredConfigAdapter` in bootstrap and asserts `"context_monitor.context_window_tokens"` is absent. This prevents silent regression if the default is added later.
**Also:** Write ADR documenting the absent-key design decision and its consequences.

### Action 3 — Distinguish monitoring failure from genuine NOMINAL (Challenge 2)

**File:** `src/context_monitoring/domain/value_objects/fill_estimate.py` and `src/context_monitoring/application/services/context_fill_estimator.py`
**Change:** Add a `monitoring_ok: bool = True` field to `FillEstimate`. Set `monitoring_ok=False` on `_FAIL_OPEN_ESTIMATE`. Allow callers to check `estimate.monitoring_ok` to distinguish "context is genuinely nominal" from "monitoring failed and fell back to safe default."
**Note:** This is a behavior change requiring new tests and a port update. It could be deferred to TASK-007 with an issue filed, if TASK-006 scope is to be preserved.

---

*S-002 Devil's Advocate execution complete. 3 STRONG challenges identified, 4 MODERATE challenges identified, 0 WEAK challenges identified.*
*Per H-14 creator-critic-revision cycle: these findings feed into the revision phase.*
