# S-012 FMEA + S-013 Inversion: TASK-006 Implementation Review

> **Agent:** adv-executor v1.0.0
> **Date:** 2026-02-20
> **Criticality:** C4
> **Deliverable:** TASK-006 context window configuration implementation (7 files, 535 insertions)
> **Strategies:** S-012 FMEA (Failure Mode and Effects Analysis) + S-013 Inversion Technique

## Document Sections

| Section | Purpose |
|---------|---------|
| [Scope and Subject](#scope-and-subject) | What was analysed |
| [S-012 FMEA Results](#s-012-fmea-results) | Component-level failure modes with RPN scoring |
| [S-013 Inversion Results](#s-013-inversion-results) | Inverted design claims with harm pathways |
| [Consolidated Findings](#consolidated-findings) | Ranked defects across both strategies |
| [Recommended Actions](#recommended-actions) | Per-finding remediation |

---

## Scope and Subject

Files analysed:

| File | Role |
|------|------|
| `src/context_monitoring/infrastructure/adapters/config_threshold_adapter.py` | Detection logic + threshold reads |
| `src/context_monitoring/application/services/context_fill_estimator.py` | Fill computation + tier classification |
| `src/context_monitoring/application/ports/threshold_configuration.py` | Port contract (IThresholdConfiguration) |
| `src/context_monitoring/domain/value_objects/fill_estimate.py` | Value object |
| `src/bootstrap.py` lines 579-600 | Wiring / composition root |
| `tests/unit/context_monitoring/test_config_threshold_adapter.py` | Adapter unit tests |
| `tests/unit/context_monitoring/application/test_context_fill_estimator.py` | Estimator unit tests |

---

## S-012 FMEA Results

FMEA notation: **Severity (S)**, **Occurrence (O)**, **Detection (D)** each on a 1-10 scale.
**RPN = S x O x D**. RPN >= 100 is a critical risk zone.

---

### Component 1: `ConfigThresholdAdapter._detect_context_window()`

#### FM-001: `self._config.get()` returns a non-numeric string from config

**Mechanism:** `_detect_context_window()` calls `self._config.get(key)` for the explicit config path. If the TOML or env var value is a non-numeric string (e.g., `context_window_tokens = "large"`), the code enters `try: return int(explicit), "config"`. This raises `ValueError` or `TypeError`, which is silently caught by `except (ValueError, TypeError): pass`. Execution falls through to env-var detection.

**Effect on system:** The user's explicit configuration is silently discarded. The system falls through to `[1m]` detection or the 200K default. An Enterprise user who misconfigures the value (e.g., `"500000"` as a string that the TOML parser passes as a string, not an integer) receives wrong fill calculations with no error feedback. The `context_window_source` will report `"default"` or `"env-1m-detection"` even though the user intended to configure an explicit value.

**Observability gap:** There is no log.warning() call in the except branch. The misconfiguration is completely silent.

| S | O | D | RPN |
|---|---|---|-----|
| 7 | 4 | 9 | 252 |

**S=7:** Wrong fill calculations for Enterprise users, potentially causing missed CRITICAL/EMERGENCY states.
**O=4:** TOML parsers typically coerce integer literals to int, but env var values are always strings. `LayeredConfigAdapter.get()` vs `get_int()` may differ in coercion behaviour — if `get()` returns the raw string, this fires for env-var users.
**D=9:** Completely silent failure. No log. `context_window_source` misreports. User has no feedback that their config was ignored.

**Classification: P0 (Critical)**

---

#### FM-002: `_detect_context_window()` called twice per `estimate()` invocation — race condition on env var mutation

**Mechanism:** `get_context_window_tokens()` and `get_context_window_source()` both call `_detect_context_window()` independently. In `ContextFillEstimator.estimate()`:
```python
context_window = self._threshold_config.get_context_window_tokens()
context_window_source = self._threshold_config.get_context_window_source()
```
These are two separate calls to `_detect_context_window()`. Between the two calls, `os.environ["ANTHROPIC_MODEL"]` could be mutated by another thread or by a subprocess that inherits the environment.

**Effect on system:** `context_window` and `context_window_source` become inconsistent: e.g., `context_window=200000` with `context_window_source="env-1m-detection"`, or vice versa. The `FillEstimate` value object captures internally inconsistent state. Downstream code (e.g., XML tag generation) would display contradictory information.

| S | O | D | RPN |
|---|---|---|-----|
| 5 | 2 | 7 | 70 |

**S=5:** Inconsistent observability data; incorrect tier classification is unlikely (fill is computed from `context_window`, not `context_window_source`), but the reported source label would be wrong.
**O=2:** Rare in practice — env var mutation during a single hook invocation is unlikely but possible in test harnesses or concurrent tool use.
**D=7:** No test covers the race; the inconsistency is only visible if both values are inspected together.

**Classification: P1 (Major)**

---

#### FM-003: `endswith("[1m]")` is case-sensitive — `ANTHROPIC_MODEL=sonnet[1M]` goes undetected

**Mechanism:** The detection check `model_env.endswith(_EXTENDED_CONTEXT_SUFFIX)` where `_EXTENDED_CONTEXT_SUFFIX = "[1m]"` is case-sensitive. Python `str.endswith()` does not perform case folding.

**Effect on system:** A user who sets `ANTHROPIC_MODEL=claude-sonnet-4-6[1M]` (uppercase M, which may result from shell variable expansion or documentation copy-paste) receives the 200K default instead of 1M. The `context_window_source` reports `"default"` rather than `"env-1m-detection"`.

| S | O | D | RPN |
|---|---|---|-----|
| 6 | 2 | 8 | 96 |

**S=6:** 1M-window user treated as 200K — fills reported at 5x the correct value; EMERGENCY fires at 176K tokens when actual fill is only 17.6%.
**O=2:** The documented suffix is `[1m]` (lowercase); uppercase is unlikely from official tooling but plausible from user error.
**D=8:** No test covers the uppercase variant. The test suite only tests `sonnet[1m]`, `opus[1m]`, and `claude-sonnet-4-6[1m]`.

**Classification: P1 (Major)**

---

#### FM-004: Negative or zero `context_window_tokens` config bypasses validation and causes ZeroDivisionError

**Mechanism:** If a user sets `context_monitor.context_window_tokens = 0` or `-1`, `_detect_context_window()` calls `int(explicit)` which succeeds and returns `(0, "config")` or `(-1, "config")`. This value is then used in `ContextFillEstimator.estimate()`:
```python
fill_percentage = token_count / context_window  # ZeroDivisionError if 0
```
For zero: Python raises `ZeroDivisionError`. The fail-open catch in `estimate()` only wraps the `self._reader.read_latest_tokens()` call, not the division. The `ZeroDivisionError` propagates up from `estimate()`, violating the fail-open contract.

For a negative value: `fill_percentage` becomes negative, which maps to `ThresholdTier.NOMINAL` (since no threshold is <= 0), silently producing a wrong result.

| S | O | D | RPN |
|---|---|---|-----|
| 8 | 3 | 8 | 192 |

**S=8:** ZeroDivisionError propagates from `estimate()`, breaking the hook entirely. The fail-open contract is violated.
**O=3:** User misconfiguration is uncommon but plausible (typo, testing with 0).
**D=8:** No test covers zero or negative config values. The division is outside the try/except in `estimate()`.

**Classification: P0 (Critical)**

---

#### FM-005: `get_threshold()` returns a float outside [0.0, 1.0] with no validation

**Mechanism:** `get_threshold()` reads a float from config and returns it directly. If a user configures `warning_threshold = 1.5` or `critical_threshold = -0.1`, the adapter returns those values without validation.

**Effect on system:** The `_classify_tier()` method in `ContextFillEstimator` compares `fill_percentage` against these thresholds. With `warning_threshold = 1.5`, WARNING is never reached (fill is capped at ~1.0 for any realistic window). With `critical_threshold = -0.1`, CRITICAL fires for any fill including 0.0. Threshold ordering violations (e.g., `warning > critical`) cause tier mis-classification that may be subtle.

| S | O | D | RPN |
|---|---|---|-----|
| 6 | 3 | 7 | 126 |

**S=6:** Systematic tier mis-classification across all estimates. EMERGENCY may never fire or fire immediately.
**O=3:** Misconfiguration is plausible, especially for users experimenting with thresholds.
**D=7:** No validation in `get_threshold()` or `_classify_tier()`. No test asserts out-of-range values are rejected.

**Classification: P1 (Major)**

---

#### FM-006: `get_all_thresholds()` iterates `_TIER_KEY_MAP` with N calls to `get_threshold()` — inconsistency window

**Mechanism:** `get_all_thresholds()` is implemented as:
```python
return {tier: self.get_threshold(tier) for tier in _TIER_KEY_MAP}
```
Each `get_threshold()` call makes a separate `self._config.get_float()` call. If the configuration system is dynamic (e.g., file-watching or mutable in tests), the values may differ between calls.

**Effect:** The returned dict may have internally inconsistent thresholds (e.g., `warning` read before a config reload and `critical` read after). In the current implementation this is a minor concern since `LayeredConfigAdapter` is not dynamic, but the design creates an unnecessary inconsistency window.

| S | O | D | RPN |
|---|---|---|-----|
| 3 | 2 | 8 | 48 |

**S=3:** Minor inconsistency; would only matter if config is dynamic.
**O=2:** `LayeredConfigAdapter` is currently static post-construction.
**D=8:** No test covers mid-call config mutation.

**Classification: P2 (Minor)**

---

### Component 2: `ContextFillEstimator.estimate()`

#### FM-007: `_FAIL_OPEN_ESTIMATE` is a module-level singleton shared across all estimator instances

**Mechanism:** `_FAIL_OPEN_ESTIMATE` is defined at module level:
```python
_FAIL_OPEN_ESTIMATE = FillEstimate(
    fill_percentage=0.0,
    tier=ThresholdTier.NOMINAL,
    token_count=None,
)
```
`FillEstimate` is a frozen dataclass, so mutation is prevented. However, `_FAIL_OPEN_ESTIMATE.context_window` defaults to `200_000` and `context_window_source` defaults to `"default"`.

**Effect:** When monitoring is disabled or a reader error occurs, the returned `FillEstimate` reports `context_window=200000` and `context_window_source="default"` regardless of what the adapter would actually detect. A user with a 1M window who disables monitoring, or whose reader fails, gets a misleading sentinel that implies the default 200K window was used. If downstream code inspects `context_window_source` to infer plan type, it will read `"default"` even when `env-1m-detection` would have been the real source.

| S | O | D | RPN |
|---|---|---|-----|
| 4 | 5 | 7 | 140 |

**S=4:** Misleading observability; no functional harm to tier classification since fill=0.0 always maps to NOMINAL.
**O=5:** Reader failures and monitoring-disabled states are both plausible in real use.
**D=7:** No test checks the `context_window` or `context_window_source` fields of the fail-open result; the existing tests only check `tier`, `fill_percentage`, and `token_count`.

**Classification: P1 (Major)**

---

#### FM-008: `_classify_tier()` makes 4 separate `get_threshold()` calls — thresholds may be inconsistent within a single classification

**Mechanism:** `_classify_tier()` calls `get_threshold()` four times in sequence:
```python
nominal = self._threshold_config.get_threshold("nominal")
warning = self._threshold_config.get_threshold("warning")
critical = self._threshold_config.get_threshold("critical")
emergency = self._threshold_config.get_threshold("emergency")
```
If config changes between calls (e.g., a test that patches the environment mid-call, or a hypothetical dynamic config), `nominal`, `warning`, `critical`, and `emergency` are read at different instants.

**Effect:** Threshold ordering invariant (`nominal < warning < critical < emergency`) may be violated within a single classification call, producing an incorrect tier. For example, if `warning` increases between reads and lands above `critical`, a fill percentage between the old `warning` and old `critical` would be classified as NOMINAL instead of WARNING.

| S | O | D | RPN |
|---|---|---|-----|
| 5 | 2 | 7 | 70 |

**S=5:** Wrong tier for a fill percentage that sits between two thresholds that flipped ordering.
**O=2:** Config is static in production; dynamic in some test scenarios.
**D=7:** No test covers threshold ordering invariant within a single call.

**Classification: P1 (Major)**

---

#### FM-009: Division `token_count / context_window` is outside the fail-open try/except block

**Mechanism:** The try/except in `estimate()` only wraps the reader call:
```python
try:
    token_count = self._reader.read_latest_tokens(transcript_path)
except Exception as exc:
    ...
    return _FAIL_OPEN_ESTIMATE

context_window = self._threshold_config.get_context_window_tokens()
context_window_source = self._threshold_config.get_context_window_source()
fill_percentage = token_count / context_window  # <- NOT inside try/except
tier = self._classify_tier(fill_percentage)
```
Any exception after the try/except block (ZeroDivisionError, TypeError from config, AttributeError from a broken threshold_config) propagates uncaught from `estimate()`.

**Effect:** The fail-open contract documented in the docstring and in EN-004 is only partially implemented. The method promises "Any exception from the ITranscriptReader results in a NOMINAL FillEstimate", but this only covers reader exceptions. Config-layer exceptions propagate.

| S | O | D | RPN |
|---|---|---|-----|
| 7 | 3 | 6 | 126 |

**S=7:** Uncaught exception breaks the hook entirely; context monitoring disrupts the main workflow, which is the exact outcome the fail-open design was built to prevent.
**O=3:** Triggered by FM-004 (zero config) or a broken `threshold_config` implementation.
**D=6:** Docstring says "Any exception" is caught; tests only exercise reader exceptions; this gap is testable but untested.

**Classification: P0 (Critical)**

---

### Component 3: `FillEstimate` value object

#### FM-010: `FillEstimate.context_window` defaults to `200_000` — sentinel is domain-value-polluting

**Mechanism:** `FillEstimate` has:
```python
context_window: int = 200_000
context_window_source: str = "default"
```
These defaults mean any code constructing `FillEstimate` without supplying `context_window` silently gets 200K. The fail-open sentinel `_FAIL_OPEN_ESTIMATE` is one such instance (see FM-007). More broadly, test code that constructs `FillEstimate` for XML testing without supplying these fields will get 200K, masking test coverage gaps.

**Effect:** The hardcoded 200K value (the original bug TASK-006 was created to fix) survives as a default in the value object itself. Future callers constructing `FillEstimate` without passing `context_window` will silently resurrect the original bug.

| S | O | D | RPN |
|---|---|---|-----|
| 5 | 4 | 8 | 160 |

**S=5:** Silent wrong context_window in any FillEstimate constructed without the field.
**O=4:** Test code already constructs FillEstimate without context_window (visible in test_context_fill_estimator.py lines 318-319, 329-331, etc.).
**D=8:** No test asserts that code-constructed FillEstimate without context_window is rejected or warned about; static analysis cannot detect this.

**Classification: P1 (Major)**

---

### Component 4: `bootstrap.py` wiring

#### FM-011: `bootstrap.py` defaults do not include `context_window_tokens` — the comment creates a false sense of security

**Mechanism:** The bootstrap comment reads:
```python
# NOTE: context_window_tokens is intentionally NOT in defaults.
# The adapter must distinguish "user explicitly configured" from
# "default" to support auto-detection priority chain (TASK-006).
```
This is correct design intent: `_detect_context_window()` checks `self._config.get(key)` returning `None` to distinguish "not set" from "set to something". However, if `LayeredConfigAdapter.get()` falls back to a hardcoded internal default for this key (e.g., if someone accidentally adds the key to `LayeredConfigAdapter`'s own defaults), the priority chain breaks silently.

**Effect:** If `context_window_tokens` ever appears in `LayeredConfigAdapter`'s defaults layer, `explicit` in `_detect_context_window()` will never be `None`, and the `[1m]` auto-detection branch will never execute. All users get `context_window_source="config"` with value 200K (or whatever the erroneous default is).

| S | O | D | RPN |
|---|---|---|-----|
| 6 | 2 | 9 | 108 |

**S=6:** Silent bypass of `[1m]` auto-detection for all users; 1M-window users receive 200K.
**O=2:** Requires a future change to `LayeredConfigAdapter` defaults; low probability but high impact.
**D=9:** Completely silent; no assertion in bootstrap.py that `layered_config.get("context_monitor.context_window_tokens")` returns None at startup; no test guards this invariant.

**Classification: P1 (Major)**

---

### Component 5: Test suite

#### FM-012: `TestContextWindowFailOpen` tests only the trivially-passing case

**Mechanism:** The class `TestContextWindowFailOpen` contains one test:
```python
def test_fail_open_returns_default(self) -> None:
    """Detection error falls back to 200K default."""
    with patch.dict(os.environ, {}, clear=True):
        adapter = _make_adapter()
        assert adapter.get_context_window_tokens() == 200_000
```
This test does not simulate an actual detection error — it tests the normal no-config path. No test raises an exception inside `_detect_context_window()` to verify the `except Exception` branch actually catches it.

**Effect:** The fail-open exception handler (`except Exception: pass`) in `_detect_context_window()` has no test coverage. If this block has a bug (e.g., the exception is re-raised by accident), no test would catch it.

| S | O | D | RPN |
|---|---|---|-----|
| 5 | 6 | 9 | 270 |

**S=5:** Undetected bug in exception handler could let detection errors propagate.
**O=6:** The test gap is definite (the scenario exists but is not covered).
**D=9:** No test exercises the exception path; code review alone is the only detection mechanism.

**Classification: P0 (Critical)**

---

#### FM-013: `FakeThresholdConfiguration.get_threshold()` uses dict lookup without ValueError on unknown tier — masks contract violation

**Mechanism:** In the test fake:
```python
def get_threshold(self, tier: str) -> float:
    return self._thresholds[tier.lower()]
```
A `KeyError` is raised if an invalid tier is passed, not `ValueError`. The real `ConfigThresholdAdapter.get_threshold()` raises `ValueError` with a descriptive message. If code under test passes an invalid tier, the fake raises `KeyError` which is a different exception type.

**Effect:** Tests that exercise error handling for invalid tiers against the fake receive `KeyError`, not `ValueError`. If `ContextFillEstimator._classify_tier()` ever passes a bad tier name, the test would observe a `KeyError`, which might be caught generically or cause a confusing test failure rather than the expected `ValueError`.

| S | O | D | RPN |
|---|---|---|-----|
| 3 | 3 | 7 | 63 |

**S=3:** Minor contract fidelity gap in test doubles.
**O=3:** Only triggered if `_classify_tier` ever calls `get_threshold` with an invalid tier name.
**D=7:** Test would fail with an unexpected exception type rather than the expected contract.

**Classification: P2 (Minor)**

---

#### FM-014: No test covers `_classify_tier()` threshold ordering invariant violation

**Mechanism:** No test exists that configures thresholds in an invalid order (e.g., `warning > critical`) and asserts that tier classification either: (a) raises, or (b) degrades gracefully. The TASK-006 acceptance criteria mention threshold configuration but do not specify invariant enforcement.

**Effect:** A user who misconfigures thresholds in inverted order (e.g., `warning=0.85, critical=0.75`) receives silent mis-classification. The `_classify_tier()` logic does not validate ordering.

| S | O | D | RPN |
|---|---|---|-----|
| 5 | 3 | 9 | 135 |

**S=5:** Fill percentage classified into wrong tier, producing incorrect action text and wrong alerts.
**O=3:** Threshold misconfiguration is plausible for power users experimenting with thresholds.
**D=9:** No validation, no test. Pure config path — static analysis cannot detect at runtime.

**Classification: P1 (Major)**

---

### FMEA RPN Summary

| ID | Failure Mode | RPN | Classification |
|----|-------------|-----|----------------|
| FM-012 | No actual fail-open exception test | 270 | P0 Critical |
| FM-001 | Silent discard of non-numeric config value | 252 | P0 Critical |
| FM-004 | Zero/negative config window causes ZeroDivisionError | 192 | P0 Critical |
| FM-009 | Division outside try/except — partial fail-open | 192 (same) | P0 Critical |
| FM-010 | FillEstimate.context_window=200K default resurfaces bug | 160 | P1 Major |
| FM-014 | No threshold ordering invariant test | 135 | P1 Major |
| FM-007 | _FAIL_OPEN_ESTIMATE misleads on context_window_source | 140 | P1 Major |
| FM-005 | No validation for out-of-range threshold floats | 126 | P1 Major |
| FM-009 | Config-layer exceptions propagate from estimate() | 126 | P0 Critical |
| FM-011 | LayeredConfigAdapter default would silently break detection | 108 | P1 Major |
| FM-003 | Case-sensitive [1m] suffix detection | 96 | P1 Major |
| FM-002 | Double _detect_context_window() call creates race | 70 | P1 Major |
| FM-008 | 4 separate get_threshold() calls in _classify_tier | 70 | P1 Major |
| FM-013 | Fake raises KeyError not ValueError for unknown tier | 63 | P2 Minor |
| FM-006 | get_all_thresholds() inconsistency window | 48 | P2 Minor |

---

## S-013 Inversion Results

The Inversion Technique inverts the design's stated claims to identify how they could be false, harmful, or fragile.

---

### Inversion 1: "The detection priority is correct"

**Claim:** Explicit user config > `ANTHROPIC_MODEL [1m]` detection > default 200K is the correct canonical ordering.

**Inverted: How could this priority ordering produce wrong results?**

**INV-001: The priority ordering correctly handles exactly ONE non-standard window size per user**

An Enterprise user who has `ANTHROPIC_MODEL=opus[1m]` set for API usage but is running Claude Code on an Enterprise 500K plan receives wrong results. The detection chain fires `[1m]` detection (step 2) and returns 1M before reaching the default. If the user's actual working window is 500K, their fills are reported at half the correct value (1M denominator instead of 500K). The user's only correct path is to set the explicit config override — but the `<context-window-source>env-1m-detection</context-window-source>` output does not indicate this is potentially wrong, and the calibration protocol does not document this edge case.

**Effect:** Enterprise + `[1m]` env var users receive fill percentages at 50% of the correct value. CRITICAL fires at 440K tokens instead of 400K. No warning is given.

**Classification: P1 (Major)**

---

**INV-002: `endswith("[1m]")` is not specific to Claude Code context windows**

`ANTHROPIC_MODEL` is an environment variable that users may set for reasons unrelated to Jerry context monitoring. A user who sets `ANTHROPIC_MODEL=my-app-model[1m]` (where `[1m]` means something else entirely in their naming convention — perhaps "version 1 minor") would trigger 1M detection. There is no documentation or runtime feedback that the `[1m]` suffix has been interpreted as a context window signal.

**Effect:** False positive 1M detection; fills reported at ~5x too low; EMERGENCY fires far later than it should.

**Classification: P1 (Major)**

---

**INV-003: The canonical ordering in TASK-006 spec (5 steps) diverges from implementation (3 steps)**

TASK-006 specifies a 5-step canonical priority:
1. Explicit user config via env var (`JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS`)
2. Explicit user config via config.toml
3. `ANTHROPIC_MODEL` env var with `[1m]` suffix
4. Transcript model name with `[1m]` suffix
5. Default 200K

The implementation combines steps 1-2 into a single `LayeredConfigAdapter.get()` call (correct) but step 4 (transcript model name detection) is explicitly absent. The implementation comment says "removed per DA-005" and TASK-006 notes this removal. However:

- The port method `get_context_window_tokens()` docstring says "explicit user config > ANTHROPIC_MODEL [1m] suffix > default 200K" — 3 steps, correct.
- The `IThresholdConfiguration` port docstring says the same — 3 steps, correct.
- But TASK-006 itself still lists step 4 in the canonical ordering with a note that it was removed.

If a future developer reads the TASK-006 spec (the authoritative design document), they see a 5-step ordering. If they re-implement step 4 (transcript model detection), they are not in violation of the spec as written. This creates a divergence risk between the living spec and the implemented design.

**Effect:** Design doc inconsistency that could cause incorrect re-implementation. Not a current runtime bug.

**Classification: P2 (Minor)**

---

### Inversion 2: "The fail-open design is safe"

**Claim:** Any exception from the reader or detection logic results in a NOMINAL FillEstimate, ensuring context monitoring never disrupts the main workflow.

**Inverted: How could fail-open cause harm?**

**INV-004: Fail-open on EMERGENCY state means context exhaustion is invisible during the worst-case scenario**

If the transcript reader fails at a moment when the context is at 95% fill (EMERGENCY tier), the fail-open mechanism returns `NOMINAL (0.0)`. The user sees no warning. The next hook invocation will also fail if the reader is broken (e.g., `$TRANSCRIPT_PATH` is stale or unset). The fail-open design means that during the most critical period — when the user most needs a warning — the monitoring system silently lies by saying the context is healthy.

The fail-open is correct for startup failures (when context is genuinely low), but becomes actively harmful when it masks a real EMERGENCY condition. There is no mechanism to distinguish "reader failed when context was low" from "reader failed when context was critically high."

**Effect:** Context exhaustion occurs without warning. The user's session compacts unexpectedly. The entire purpose of the context monitoring system — to warn before compaction — is defeated at the worst possible moment.

**Classification: P0 (Critical)**

---

**INV-005: Fail-open on config errors uses the wrong context window silently**

If `self._threshold_config.get_context_window_tokens()` raises (e.g., broken port implementation, import error, constructor failure), the exception propagates from `estimate()` rather than returning NOMINAL (FM-009 root cause). But even if a hypothetical wrapper were added, the fail-open would return `_FAIL_OPEN_ESTIMATE` with `context_window=200_000`. If the user's actual window is 1M, all NOMINAL fail-open returns are technically correct (context is low) but the returned `context_window=200_000` is wrong metadata.

**Effect:** Metadata inconsistency; if the context ever recovers and the reader starts working, the transition from `context_window=200000` to `context_window=1000000` looks like a context window change event, not a monitoring recovery. Downstream analytics would misread this as a model switch.

**Classification: P1 (Major)**

---

**INV-006: Fail-open cannot be disabled for development/testing scenarios**

The fail-open behaviour is hardcoded. There is no way to configure the estimator to propagate exceptions (e.g., for strict test environments or developer debugging mode). A developer writing an integration test that intentionally passes a broken reader to verify their tool chain cannot distinguish "the reader is broken as expected" from "the estimator silently swallowed the error."

The `is_enabled()` flag controls whether monitoring runs at all, but cannot be used to switch between fail-open and fail-strict modes.

**Effect:** Test coverage of the reader layer is harder to write precisely; tests that should verify reader failures must inspect side effects (log messages) rather than exception propagation.

**Classification: P2 (Minor)**

---

### Inversion 3: "The DRY refactoring is clean"

**Claim:** Extracting both `get_context_window_tokens()` and `get_context_window_source()` to call `_detect_context_window()` eliminates code duplication and is a clean refactoring.

**Inverted: How could the shared `_detect_context_window()` method cause issues?**

**INV-007: `_detect_context_window()` is called twice per `estimate()` — the DRY fix creates a double-execution cost**

The DRY refactoring correctly eliminates code duplication, but the calling pattern in `estimate()` invokes `_detect_context_window()` twice per hook invocation. Each call performs:
1. A `LayeredConfigAdapter.get()` call (file I/O or dict lookup depending on adapter implementation)
2. An `os.environ.get("ANTHROPIC_MODEL")` syscall

For a system called on every Claude Code hook invocation (potentially hundreds of times per session), this doubles the detection work per estimate. The TASK-006 spec notes this in "Caching Behavior" and argues "the cost is negligible." This is correct for a single call, but the claim that "one `get_int_optional()` call + one `os.environ.get()` call per invocation" is correct only for the single-method case. With two calls to `_detect_context_window()` per `estimate()`, the actual cost is two of each.

**Effect:** Minor performance regression relative to stated cost. Not harmful in isolation, but the spec's cost characterisation is inaccurate.

**Classification: P2 (Minor)**

---

**INV-008: `_detect_context_window()` returning a tuple couples the two return values — callers cannot independently cache them**

The method returns `(tokens, source)` as a tuple. If `ContextFillEstimator` were ever refactored to call `get_context_window_tokens()` and `get_context_window_source()` in different methods or at different times, the double-invocation problem (FM-002) becomes harder to fix without restructuring the adapter. The current design provides no way for the estimator to atomically capture both values from a single detection run.

The correct fix would be for `estimate()` to call `_detect_context_window()` once (directly or via a combined method), but this would require the estimator to receive the tuple directly — which breaks the port abstraction (the port only exposes `get_context_window_tokens()` and `get_context_window_source()` separately).

**Effect:** Architectural tension: the DRY fix at the adapter level is correct, but the port interface design forces the double-call at the estimator level. Fixing the double-call requires either: (a) adding a `get_context_window()` method returning a named tuple to the port, or (b) having the estimator call the adapter directly (H-07/H-08 violation). Neither option is clean.

**Classification: P1 (Major)**

---

### Inversion 4: "Enterprise users can configure"

**Claim:** Enterprise users (500K context window) can set `JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS=500000` to correctly configure their context window.

**Inverted: How could configuration fail for Enterprise users?**

**INV-009: The env var name convention is undiscoverable without documentation**

`JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS` uses double-underscore (`__`) as the namespace separator (a `LayeredConfigAdapter` convention). Enterprise users familiar with environment variables would reasonably try:
- `JERRY_CONTEXT_MONITOR_CONTEXT_WINDOW_TOKENS` (single underscore — wrong)
- `JERRY__CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS` (double prefix — wrong)
- `JERRY_CONTEXT_MONITORING_CONTEXT_WINDOW_TOKENS` (wrong key name from old bootstrap comment that says `context_monitoring.context_window_tokens`)

The bootstrap.py comment at line 587 says the namespace is `context_monitor.*`, but an old bootstrap comment referenced `context_monitoring.context_window_tokens`. If any documentation uses the old `context_monitoring` namespace, Enterprise users silently fail to configure their window.

**Effect:** Enterprise users who mistype the env var receive no error, fall back to 200K, and get 150% overreported fill percentages. The `context_window_source="default"` in the output is the only signal, but without calibration protocol documentation, users may not check it.

**Classification: P1 (Major)**

---

**INV-010: The calibration protocol referenced in TASK-006 is listed as an acceptance criterion but its update status is unverified**

TASK-006 AC line: "Calibration protocol updated with configuration instructions per plan." The calibration protocol is at `docs/knowledge/context-resilience/calibration-protocol.md`. The TASK-006 document provides the table content for step 6, but the implementation files reviewed do not confirm that this file was actually updated.

If the calibration protocol was not updated, Enterprise users have no documented path to correct configuration. The `<context-window-source>default</context-window-source>` output is the only indicator of misconfiguration, but its meaning is not explained without documentation.

**Effect:** Enterprise users cannot self-serve configure their context window. The code is correct, but the user-facing guidance is missing.

**Classification: P1 (Major)**

---

**INV-011: Invalid `context_window_tokens` values are silently ignored, not reported as misconfiguration**

If an Enterprise user sets `JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS=abc` (a typo), the `try: int(explicit)` block in `_detect_context_window()` catches `ValueError` silently and falls through to `[1m]` detection or the 200K default. The user sees `context_window_source="default"` and has no indication their configuration was rejected.

The fix is FM-001's recommended action: add a `logger.warning()` in the except branch. Without it, Enterprise users who misconfigure the key spend significant debugging time.

**Effect:** Silent configuration rejection. User gets wrong window size with no feedback. This is the same failure mode as FM-001 — included here to complete the Inversion analysis from the user perspective.

**Classification: P0 (Critical)** (same root as FM-001, elevated here because it directly impacts the primary user group — Enterprise users — who the feature is designed to serve)

---

## Consolidated Findings

Priority classification across both strategies:

### P0 Critical (must fix before release)

| ID | Source | Finding |
|----|--------|---------|
| FM-001 / INV-011 | FMEA + Inversion | Non-numeric config value silently discarded; no warning logged |
| FM-004 | FMEA | Zero/negative `context_window_tokens` config causes `ZeroDivisionError` in `estimate()` |
| FM-009 | FMEA | Division and config calls outside try/except — partial fail-open contract violation |
| FM-012 | FMEA | `TestContextWindowFailOpen` tests only the trivially-passing path; exception handler has no test coverage |
| INV-004 | Inversion | Fail-open masks EMERGENCY conditions — context exhaustion is invisible when monitoring most needed |

### P1 Major (fix before or shortly after release)

| ID | Source | Finding |
|----|--------|---------|
| FM-002 | FMEA | Double `_detect_context_window()` call per `estimate()` — race condition on env var mutation |
| FM-003 | FMEA | Case-sensitive `[1m]` detection — `[1M]` suffix goes undetected |
| FM-005 | FMEA | No validation of threshold float range; out-of-range values accepted silently |
| FM-007 | FMEA | `_FAIL_OPEN_ESTIMATE` reports `context_window=200000` regardless of actual configuration |
| FM-008 | FMEA | 4 separate `get_threshold()` calls in `_classify_tier()` — inconsistency window |
| FM-010 | FMEA | `FillEstimate.context_window=200_000` default resurrects original TASK-006 bug for future callers |
| FM-011 | FMEA | No assertion guards `LayeredConfigAdapter` not having `context_window_tokens` as a default |
| FM-014 | FMEA | No test for threshold ordering invariant violation |
| INV-001 | Inversion | Enterprise + `[1m]` env var: detection returns 1M instead of 500K with no warning |
| INV-002 | Inversion | `[1m]` suffix in unrelated model name causes false-positive 1M detection |
| INV-005 | Inversion | Fail-open returns misleading `context_window=200000` metadata |
| INV-008 | Inversion | Port interface forces double-call; no atomic `get_context_window()` method available |
| INV-009 | Inversion | Env var name is undiscoverable; old `context_monitoring` namespace references risk misdirection |
| INV-010 | Inversion | Calibration protocol update not confirmed as complete |

### P2 Minor (fix in follow-up)

| ID | Source | Finding |
|----|--------|---------|
| FM-006 | FMEA | `get_all_thresholds()` inconsistency window |
| FM-013 | FMEA | Test fake raises `KeyError` not `ValueError` for unknown tier |
| INV-003 | Inversion | TASK-006 spec still lists 5-step ordering; implementation uses 3-step |
| INV-006 | Inversion | No fail-strict mode for testing/debugging |
| INV-007 | Inversion | Spec's cost characterisation understates double-call overhead |

---

## Recommended Actions

### P0 Actions (blocking release)

**A-001 (FM-001 / INV-011):** Add `logger.warning()` in the `except (ValueError, TypeError)` block of `_detect_context_window()`. Include the key, the raw value, and the fallback source in the message.

```python
except (ValueError, TypeError):
    logger.warning(
        "context_monitor.context_window_tokens value %r cannot be converted to int; "
        "falling through to auto-detection. Check your configuration.",
        explicit,
    )
    # fall through to auto-detection
```

**A-002 (FM-004):** Add validation in `_detect_context_window()` after `int(explicit)`: if the result is <= 0, log a warning and fall through rather than returning the invalid value.

```python
tokens = int(explicit)
if tokens <= 0:
    logger.warning(
        "context_monitor.context_window_tokens value %d is not positive; "
        "falling through to auto-detection.",
        tokens,
    )
    # fall through
else:
    return tokens, "config"
```

**A-003 (FM-009):** Wrap the post-reader block in `estimate()` in a broad try/except, or extend the existing try/except to cover the full computation:

```python
try:
    token_count = self._reader.read_latest_tokens(transcript_path)
    context_window = self._threshold_config.get_context_window_tokens()
    context_window_source = self._threshold_config.get_context_window_source()
    fill_percentage = token_count / context_window
    tier = self._classify_tier(fill_percentage)
except Exception as exc:
    logger.warning("Context monitoring error: %s (fail-open -> NOMINAL)", exc)
    return _FAIL_OPEN_ESTIMATE
```

**A-004 (FM-012):** Add a test that patches `os.environ.get` to raise `RuntimeError` during `_detect_context_window()` and asserts that `get_context_window_tokens()` returns 200K:

```python
def test_fail_open_on_environ_exception(self) -> None:
    with patch("os.environ.get", side_effect=RuntimeError("env error")):
        adapter = _make_adapter()
        assert adapter.get_context_window_tokens() == 200_000
```

**A-005 (INV-004):** Document the fail-open limitation explicitly in the module docstring and in the calibration protocol: "If the transcript reader fails during an active EMERGENCY condition, monitoring will report NOMINAL. Check `<context-window-source>` and `<token-count>N/A</token-count>` as signals of monitoring failure."

### P1 Actions (fix before or shortly after release)

**A-006 (FM-002 / INV-008):** Capture both detection values atomically in `estimate()`. The cleanest option without breaking port abstraction is to add a `get_context_window() -> tuple[int, str]` method to `IThresholdConfiguration` and call it once. Alternatively, call `_detect_context_window()` once and extract both values (requires adapter-level access, acceptable if done in bootstrap wiring). Minimum fix: document the double-call as a known limitation in the code comment.

**A-007 (FM-003):** Change detection to `model_env.lower().endswith("[1m]")` and add a test for `ANTHROPIC_MODEL=sonnet[1M]`.

**A-008 (FM-005):** Add validation in `get_threshold()`: if the returned float is not in `[0.0, 1.0]`, raise `ValueError` or log a warning and clamp.

**A-009 (FM-007 / INV-005):** Update `_FAIL_OPEN_ESTIMATE` to not include a `context_window` value, or make it clear it is a sentinel. One option: set `context_window=0` and `context_window_source="monitoring-error"` so downstream code can distinguish a genuine NOMINAL from a fail-open NOMINAL. This would require updating the `FillEstimate` sentinel and any callers that inspect `context_window`.

**A-010 (FM-010):** Remove the `context_window: int = 200_000` default from `FillEstimate`. Make it a required field. This forces all callers to explicitly supply the value, preventing silent resurrection of the original bug. Update `_FAIL_OPEN_ESTIMATE` to supply `context_window=0` or a sentinel value.

**A-011 (FM-011):** Add an assertion in bootstrap.py after constructing `config_adapter` that the key is absent from the adapter's defaults:

```python
assert config_adapter.get("context_monitor.context_window_tokens") is None, (
    "context_monitor.context_window_tokens must not be in LayeredConfigAdapter defaults "
    "(required for TASK-006 detection priority chain)"
)
```

**A-012 (FM-014):** Add a test for inverted threshold ordering (e.g., `warning=0.90, critical=0.75`) and document the expected behaviour.

**A-013 (INV-001):** Add a note to the calibration protocol: "If you have both an Enterprise (500K) account and use `[1m]` model aliases, set `JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS=500000` explicitly. The env var takes priority over `[1m]` auto-detection."

**A-014 (INV-009 / INV-010):** Confirm calibration protocol has been updated (step 6 from TASK-006 implementation notes). Verify the env var name `JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS` is the only name documented (no `JERRY_CONTEXT_MONITORING__` variant).

### P2 Actions (follow-up)

**A-015 (INV-003):** Update TASK-006 spec to remove step 4 from the canonical detection ordering, making the spec match the implementation.

**A-016 (FM-013):** Update `FakeThresholdConfiguration.get_threshold()` to raise `ValueError` (not `KeyError`) for unknown tiers, matching the real adapter's contract.

**A-017 (INV-007):** Update the "Caching Behavior" note in TASK-006 to accurately state that `_detect_context_window()` is called twice per `estimate()` invocation (two `get()` calls and two `os.environ.get()` calls, not one of each).

---

*Report generated by adv-executor v1.0.0 — S-012 FMEA + S-013 Inversion combined analysis.*
*Findings are independent assessments; traceability to acceptance criteria is the responsibility of the adv-scorer.*
