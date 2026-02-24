# S-004 Pre-Mortem Analysis: TASK-006 Context Window Configuration

<!-- STRATEGY: S-004 Pre-Mortem Analysis -->
<!-- CRITICALITY: C4 -->
<!-- DELIVERABLE: TASK-006 implementation (7 files, 535 insertions) -->
<!-- DATE: 2026-02-20 -->
<!-- AGENT: adv-executor v1.0.0 -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Failure scenario and critical findings |
| [Pre-Mortem Setup](#pre-mortem-setup) | Imagined failure framing |
| [Failure Mode Catalog](#failure-mode-catalog) | All identified failure modes by priority |
| [Assumption Inventory](#assumption-inventory) | Assumptions that could be wrong |
| [Environmental Conditions](#environmental-conditions) | Conditions causing unexpected behavior |
| [Edge Case Analysis](#edge-case-analysis) | Edge cases in context window detection |
| [Risk Summary](#risk-summary) | Priority-ranked risk table |
| [Mitigation Recommendations](#mitigation-recommendations) | Actionable remediation per failure mode |

---

## Executive Summary

**Pre-Mortem Scenario:** The TASK-006 implementation is deployed. Three months later, Jerry reports context monitoring failures across multiple user segments. A post-incident review is convened. This analysis works backward from that failure state to identify what went wrong.

**Critical Findings:** 5 P0 failure modes identified, 6 P1 failure modes, 4 P2 failure modes.

**Highest-risk finding (P0-001):** The `_detect_context_window()` method is called twice per `estimate()` invocation (once for tokens, once for source), performing redundant env var reads and config lookups. Under concurrent session hook invocations, ANTHROPIC_MODEL changes between calls produce a split-brain state where `get_context_window_tokens()` and `get_context_window_source()` return inconsistent values. The returned `FillEstimate` reports source="default" (200K) while fill_percentage was computed against 1M -- a silent data corruption.

**Highest-risk finding (P0-002):** The `_FAIL_OPEN_ESTIMATE` singleton is a frozen dataclass created once at module load time. It hardcodes `context_window=200_000` and `context_window_source="default"` regardless of the actual configured window. When monitoring is disabled or a reader fails, the fail-open estimate reports a 200K window even if the user configured 500K or 1M. Downstream consumers reading `estimate.context_window` will see incorrect data and may make wrong decisions (e.g., logging, telemetry, operator dashboards).

**Scope of analysis:** 7 implementation files. The analysis covers `ConfigThresholdAdapter`, `ContextFillEstimator`, `IThresholdConfiguration`, `FillEstimate`, `bootstrap.py` wiring, and both test suites.

---

## Pre-Mortem Setup

**Framing:** It is 2026-05-20. Three months have elapsed since TASK-006 was deployed in Jerry v0.3.0. The following incidents have been reported:

1. Enterprise users (500K window) intermittently receive CRITICAL-tier warnings when context is ~30% full.
2. [1m] extended-context users report EMERGENCY-tier false positives triggered at session start (< 5K tokens).
3. The `<context-monitor>` XML tag sometimes shows `<context-window-source>default</context-window-source>` while `<context-window>1000000</context-window>`, creating operator confusion.
4. A CI pipeline that runs hook tests against a corpus of real transcripts began failing after a Claude Code update changed model naming conventions.

The task: identify every plausible root cause, working backward from these observed failures.

---

## Failure Mode Catalog

### P0: Critical -- Silent data corruption or total functional failure

---

#### FM-001 (P0): Split-brain state from double-detection in _detect_context_window()

**File:** `config_threshold_adapter.py` lines 203-217

**Root cause:** `get_context_window_tokens()` and `get_context_window_source()` each independently call `_detect_context_window()`. The `ContextFillEstimator.estimate()` method calls both in sequence (lines 144-145). Between these two calls, `ANTHROPIC_MODEL` can change (extremely rare in normal usage, but possible in test environments, concurrent hook invocations, or when users run jerry CLI alongside Claude Code session). This produces a FillEstimate where:

```python
# call 1: ANTHROPIC_MODEL="sonnet[1m]" -> tokens=1_000_000, source="env-1m-detection"
context_window = self._threshold_config.get_context_window_tokens()
# call 2: ANTHROPIC_MODEL="" (env changed) -> source="default"
context_window_source = self._threshold_config.get_context_window_source()
```

Result: `FillEstimate(context_window=1_000_000, context_window_source="default")` -- internally inconsistent. The fill_percentage is computed with 1M but the source tag says "default", making the XML output misleading.

**Probability:** Low in production, moderate in test harnesses that manipulate env vars.
**Impact:** Silent data corruption in FillEstimate, misleading operator XML output (Incident #3).

---

#### FM-002 (P0): _FAIL_OPEN_ESTIMATE hardcodes 200K window regardless of configuration

**File:** `context_fill_estimator.py` lines 56-60

**Root cause:**

```python
_FAIL_OPEN_ESTIMATE = FillEstimate(
    fill_percentage=0.0,
    tier=ThresholdTier.NOMINAL,
    token_count=None,
)
```

`FillEstimate` defaults `context_window=200_000` and `context_window_source="default"`. This singleton is returned in three scenarios:
1. Monitoring disabled (`is_enabled()` returns False)
2. Reader raises any exception

For Enterprise users (500K) or [1m] users (1M) who have disabled monitoring for a session and then re-enable it, or who experience a transient reader failure, the returned estimate carries the wrong window size. Any downstream code that reads `estimate.context_window` for non-tier purposes (telemetry, calibration display, operator dashboards) will silently receive 200K regardless of configuration. This makes the fail-open path a data quality hazard, not merely a conservative fallback.

**Probability:** High for users who disable/re-enable monitoring. Moderate for any user on a transcript reader failure.
**Impact:** Incorrect context_window in fail-open FillEstimate; affects all downstream consumers of the estimate beyond tier classification.

---

#### FM-003 (P0): Division-by-zero if context_window_tokens is configured as 0

**File:** `context_fill_estimator.py` line 146

**Root cause:**

```python
fill_percentage = token_count / context_window
```

If `context_window` returns 0 (a user misconfigures `JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS=0` or `context_window_tokens = 0` in TOML), this raises `ZeroDivisionError`. The exception is NOT caught in `estimate()`. The `try/except` block only wraps the `read_latest_tokens()` call (lines 134-142); the division is outside that block (lines 144-147).

The fail-open pattern does not protect against this failure: the division occurs AFTER the reader successfully returns, in the unguarded section. This is a total failure for any user who misconfigures or is given a corrupted config.

**Probability:** Low (user misconfiguration), but the consequence is a crash in the hook execution path.
**Impact:** ZeroDivisionError propagates up through the hook, disrupting the user session. Hook may terminate abnormally.

---

#### FM-004 (P0): Negative fill_percentage if context_window_tokens is configured negative

**File:** `context_fill_estimator.py` line 146; `config_threshold_adapter.py` line 233

**Root cause:** `_detect_context_window()` applies `int(explicit)` on the user config value without range validation. A negative integer (e.g., `-1`) passes through `int()` successfully, returns a negative context window, and produces a negative `fill_percentage`. This negative fill is classified as NOMINAL (correct by accident -- `< nominal_threshold`), but the FillEstimate carries a nonsensical negative percentage. The XML tag will emit `<fill-percentage>-0.0005</fill-percentage>`, violating the documented invariant that fill_percentage is between 0.0 and 1.0.

**Probability:** Low.
**Impact:** Invalid FillEstimate with negative fill_percentage; XML output violates documented contract; downstream consumers that validate 0.0-1.0 range will error.

---

#### FM-005 (P0): Threshold ordering not validated -- inverted thresholds cause classification failure

**File:** `context_fill_estimator.py` lines 211-224; `config_threshold_adapter.py` lines 109-140

**Root cause:** The `_classify_tier()` method assumes `nominal < warning < critical < emergency`. No validation of this ordering exists. A user who configures:

```toml
[context_monitor]
warning_threshold = 0.40
critical_threshold = 0.30
```

inverts the expected ordering. The classification logic:

```python
if fill_percentage >= emergency:       # 0.88 (default)
    return EMERGENCY
if fill_percentage >= critical:        # 0.30 (misconfigured)
    return CRITICAL
if fill_percentage >= warning:         # 0.40 (misconfigured)
    return WARNING
if fill_percentage >= nominal:         # 0.55 (default)
    return LOW
return NOMINAL
```

At 0.35 fill: returns CRITICAL (correct by accident). At 0.50 fill: returns WARNING (should be LOW or NOMINAL). At 0.25 fill: returns NOMINAL (correct). At 0.60 fill: returns WARNING (correct). The overall effect is subtle misclassification, not an obvious crash, making this particularly dangerous. Users who misconfigure thresholds receive plausibly-wrong tier assignments with no error.

**Probability:** Moderate. Enterprise ops teams who tune thresholds for their environment are prime candidates for misconfiguration.
**Impact:** Silent misclassification of context fill tier; wrong action recommendations; potentially triggers compaction at wrong times.

---

### P1: Major -- Incorrect behavior in foreseeable conditions

---

#### FM-006 (P1): [1m] suffix detection based on undocumented convention that can change

**File:** `config_threshold_adapter.py` lines 57-61, 239-241

**Root cause:** The `[1m]` detection relies on a convention documented in a URL comment (`https://code.claude.com/docs/en/model-config`). This is an external interface owned by Anthropic, not a stable versioned API. The comment acknowledges "used in Claude Code model alias configuration". If Anthropic changes this suffix convention (e.g., to `[1M]`, `[ext]`, `[1000k]`, or removes it in favor of a different mechanism), the detection silently falls back to 200K default. Enterprise users on [1m] would silently receive wrong fill percentages.

The test `test_endswith_not_substring` correctly tests the endswith boundary, but there are no tests for:
- Case sensitivity: `sonnet[1M]` (uppercase M) would not be detected
- Future variants: `sonnet[2m]` (hypothetical 2M model)
- Whitespace: `sonnet[1m] ` (trailing space) would not be detected

**Probability:** Moderate (external dependency, known to change; Incident #4 describes a CI failure after a Claude Code update changing model naming).
**Impact:** Silent fallback to 200K for [1m] users; CRITICAL/EMERGENCY false positives at high token counts; user trust erosion.

---

#### FM-007 (P1): get_context_window_tokens() called N+1 times per estimate() invocation

**File:** `context_fill_estimator.py` lines 144-145; `config_threshold_adapter.py` lines 203-217

**Root cause:** `estimate()` calls both `get_context_window_tokens()` (line 144) and `get_context_window_source()` (line 145), each of which calls `_detect_context_window()`. Additionally, `_classify_tier()` calls `get_threshold()` four times (lines 211-214), each hitting the LayeredConfigAdapter. For a single `estimate()` call, the LayeredConfigAdapter is queried 4+2=6 times for threshold values plus 2 runs of the detection chain. Under high hook invocation frequency, this is inefficient. More critically, the double detection creates the split-brain risk from FM-001.

**Probability:** High (structural, not environmental).
**Impact:** Unnecessary config read overhead; FM-001 split-brain risk.

---

#### FM-008 (P1): Explicit config value type coercion bypasses LayeredConfigAdapter type safety

**File:** `config_threshold_adapter.py` lines 229-235

**Root cause:**

```python
explicit = self._config.get(key)          # returns raw Any
if explicit is not None:
    try:
        return int(explicit), "config"
    except (ValueError, TypeError):
        pass  # fall through to auto-detection
```

The implementation uses the raw `get()` method (which returns `Any`) and manually calls `int()`, rather than using the typed `get_int()` method that LayeredConfigAdapter likely provides (which is used for other config keys, e.g., `get_int(key, default=...)` on line 172). This is inconsistent with the rest of the adapter, which uses `get_float()`, `get_bool()`, and `get_int()` for typed access. The raw `get()` + manual cast silently swallows type errors and falls through to auto-detection, hiding configuration mistakes from the user.

**Note:** The task specification's Step 2 code sample used `get_int_optional(key)` (a hypothetical optional-returning variant), but the actual implementation uses `get(key)` + `int()`. This divergence from the specification is itself a finding -- the implementation uses a different method than specified, and the specified method may not exist on LayeredConfigAdapter (making the implementation a workaround, not the intended approach).

**Probability:** Moderate (any non-integer config value triggers silent fallthrough).
**Impact:** User-configured window silently ignored; falls back to 200K or 1M unexpectedly; no error surfaced to user.

---

#### FM-009 (P1): Bootstrap defaults include threshold values but comment notes context_window_tokens absent

**File:** `bootstrap.py` lines 584-594

**Root cause:**

```python
defaults={
    # NOTE: context_window_tokens is intentionally NOT in defaults.
    "context_monitor.nominal_threshold": 0.55,
    ...
}
```

The intentional absence of `context_window_tokens` from bootstrap defaults is correct per the TASK-006 design (to allow `get()` to return `None` for priority chain distinction). However, this creates a subtle bootstrap dependency: if anyone adds `"context_monitor.context_window_tokens": 200000` to the defaults dict (e.g., during a refactor or copy-paste), the priority chain breaks -- the "no explicit config" path would never be reached because `get()` would return the default value, making it indistinguishable from user-configured. This is a latent design fragility with no guard.

**Probability:** Low initially, rises over time as contributors unfamiliar with the design intent touch bootstrap.py.
**Impact:** [1m] auto-detection silently bypassed; all users locked to 200K regardless of ANTHROPIC_MODEL.

---

#### FM-010 (P1): FillEstimate context_window field defaults to 200K in dataclass -- misleading for fail-open

**File:** `fill_estimate.py` lines 56-58

**Root cause:** `FillEstimate` has `context_window: int = 200_000` as a default field value. This is correct for the normal path where context_window is always passed explicitly. However, it means that any code constructing `FillEstimate` without specifying `context_window` (e.g., the `_FAIL_OPEN_ESTIMATE` singleton, or test code) silently inherits 200K. This hardcoded default in the value object conflates "sentinel/unknown" with "200K configured". There is no way to distinguish a FillEstimate with a genuine 200K configured window from one that used the default because context_window was omitted.

**Probability:** High for test code and future developers; already manifested in `_FAIL_OPEN_ESTIMATE` (FM-002).
**Impact:** Conflated semantics for "unknown window" vs "200K window"; downstream consumers cannot distinguish.

---

#### FM-011 (P1): _classify_tier() queries IThresholdConfiguration 4 times per call -- no atomicity

**File:** `context_fill_estimator.py` lines 211-214

**Root cause:**

```python
nominal = self._threshold_config.get_threshold("nominal")
warning = self._threshold_config.get_threshold("warning")
critical = self._threshold_config.get_threshold("critical")
emergency = self._threshold_config.get_threshold("emergency")
```

Four separate calls to `get_threshold()`, each of which calls `get_float()` on the LayeredConfigAdapter. If the config is hot-reloaded (possible in some deployment patterns) or if env vars change between calls (test environments), the four threshold values may be read from different configuration states. A threshold set that is internally consistent at any single point in time may be read as an internally inconsistent set across the four calls.

**Probability:** Low in production (config is read-once from file), moderate in test environments.
**Impact:** Non-atomic threshold snapshot; potential misclassification under concurrent config mutations.

---

### P2: Minor -- Incorrect behavior under unusual but non-critical conditions

---

#### FM-012 (P2): No validation that float thresholds are in [0.0, 1.0] range

**File:** `config_threshold_adapter.py` lines 109-140

**Root cause:** `get_threshold()` reads floats from config via `get_float()` with no range check. A threshold of `1.5` is silently accepted and will cause EMERGENCY to never trigger (since fill_percentage cannot exceed approximately 1.0 in normal operation). A threshold of `-0.1` causes all fill percentages to classify as EMERGENCY. No `ValueError` is raised, no warning is logged.

**Probability:** Low (requires user misconfiguration).
**Impact:** Silent misclassification; tier never triggers or always triggers.

---

#### FM-013 (P2): generate_context_monitor_tag uses len/4 token estimate -- may exceed 200 token budget

**File:** `context_fill_estimator.py` lines 157-193; test line 372

**Root cause:** The docstring states the tag is "between 40 and 200 tokens (approximately len/4 characters)". The `len/4` approximation is a rough heuristic. For non-ASCII action text (not currently the case, but possible if action text is internationalized), or for large integer values (e.g., `context_window=1000000` adds 7 digits), the token count could exceed 200 for some tier/window combinations. The test `test_tag_within_token_budget` validates this only for the specific WARNING tier with 200K window -- not for all tiers and context window sizes. A 1M window context tag with EMERGENCY action text is not tested.

**Probability:** Low (bounded by current action text length; only at risk if action text is extended).
**Impact:** XML tag exceeds documented 200-token budget; hook injection overhead increases.

---

#### FM-014 (P2): Calibration protocol update not included in implementation

**File:** TASK-006 acceptance criteria, Step 6

**Root cause:** Acceptance criteria item "Calibration protocol updated with configuration instructions per plan" is listed as incomplete (`[ ]`) in TASK-006.md. The implementation covers Steps 1-5 (code + bootstrap) but Step 6 (calibration protocol update in `docs/knowledge/context-resilience/calibration-protocol.md`) is not part of the 7 files in scope. Enterprise users who follow the existing calibration protocol will not find the configuration instructions needed to set `JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS=500000`.

**Probability:** High (definitionally not done per AC checklist).
**Impact:** Enterprise users remain misconfigured; Incident #1 (500K users getting CRITICAL at 30% fill) persists even after TASK-006 deployment because users are never told to configure their window size.

---

#### FM-015 (P2): Context window source string is untyped -- typo-prone for downstream consumers

**File:** `config_threshold_adapter.py` lines 206-217; `fill_estimate.py` line 58; `threshold_configuration.py` lines 129-144

**Root cause:** The `context_window_source` field is typed as `str` throughout. Valid values are documented as `"config"`, `"env-1m-detection"`, `"default"` (in port docstring and TASK-006.md), but this is enforced only by convention, not by the type system. Downstream consumers who switch on `context_window_source` (e.g., `if estimate.context_window_source == "env-1m-detection"`) are vulnerable to silent breakage if the string values change (e.g., if "env-1m-detection" is renamed to "anthropic-model-1m" in a future refactor). No `Literal` type, no `enum`, no constant is defined for these values.

**Probability:** Moderate (type string values change across refactors without compiler feedback).
**Impact:** Silent breakage of switch logic in downstream consumers; difficult to find via grep.

---

## Assumption Inventory

| ID | Assumption | Location | Risk if Wrong |
|----|-----------|----------|---------------|
| A-001 | ANTHROPIC_MODEL env var is always a plain string when set | `config_threshold_adapter.py:239` | Non-string (bytes, None from OS-level anomaly) would cause AttributeError in `endswith()` despite `os.environ.get()` returning `str | None`. The `""` default prevents None, but non-string injection is possible in malformed environments. |
| A-002 | [1m] suffix convention is stable and owned by Anthropic | `config_threshold_adapter.py:57-61` | External dependency; changes silently break detection (FM-006). No version pin, no registry check. |
| A-003 | LayeredConfigAdapter.get() returns None when key is absent from all layers | `config_threshold_adapter.py:231` | If LayeredConfigAdapter raises instead of returning None for missing keys, the detection chain crashes. The implementation has no documentation of LayeredConfigAdapter's contract for missing keys. |
| A-004 | LayeredConfigAdapter is thread-safe for concurrent reads | `context_fill_estimator.py:144-145` | Claude Code may invoke hooks concurrently. If LayeredConfigAdapter is not thread-safe, the double-call pattern (FM-001, FM-007, FM-011) creates race conditions. |
| A-005 | token_count from ITranscriptReader is always a non-negative integer | `context_fill_estimator.py:146` | If reader returns a negative integer (corrupt transcript), fill_percentage is negative. FM-004 covers the config case; this covers the reader case. |
| A-006 | context_window_tokens configured value is within a reasonable range | `config_threshold_adapter.py:233` | Values of 0 (FM-003), negative (FM-004), or implausibly large (e.g., 10^18) pass through int() conversion without validation. |
| A-007 | The fail-open NOMINAL response is always safe for downstream consumers | `context_fill_estimator.py:56-60` | Downstream code that reads `estimate.context_window` from fail-open responses will receive 200K regardless of actual config. FM-002 covers this. |
| A-008 | Threshold values are always numerically ordered (nominal < warning < critical < emergency) | `context_fill_estimator.py:211-224` | No validation. FM-005 covers the misclassification consequence. |
| A-009 | The [1m] suffix check applies correctly to all Claude Code model alias formats | `config_threshold_adapter.py:240` | Model aliases are not versioned or formally specified. The test covers `claude-sonnet-4-6[1m]` but not all possible future formats. |
| A-010 | bootstrap.py defaults dict will never include context_window_tokens | `bootstrap.py:584-594` | FM-009 covers the consequence if this assumption is violated by a future contributor. No enforcement mechanism exists. |

---

## Environmental Conditions

| ID | Condition | Trigger | Failure Mode |
|----|-----------|---------|-------------|
| E-001 | Claude Code updates model naming convention | CI/CD pipeline, production upgrade | FM-006 ([1m] detection breaks silently) |
| E-002 | User runs jerry CLI alongside an active Claude Code session with different ANTHROPIC_MODEL | Concurrent processes | FM-001 (split-brain) |
| E-003 | Enterprise deployment with 500K context window and no calibration guidance | Enterprise onboarding | FM-002, FM-014 (fail-open returns 200K; calibration protocol missing) |
| E-004 | User sets context_window_tokens = 0 in TOML (typo or test) | Misconfiguration | FM-003 (ZeroDivisionError crashes hook) |
| E-005 | User configures inverted thresholds for testing or experiment | Threshold tuning | FM-005 (silent misclassification) |
| E-006 | Hook invoked at very high frequency (tight loop or streaming mode) | High-throughput agentic session | FM-007 (N+1 config reads per estimate) |
| E-007 | Config TOML has non-integer value for context_window_tokens (e.g., "500K" string) | User documentation error | FM-008 (silent fallthrough to auto-detection) |
| E-008 | Test suite manipulates os.environ between get_context_window_tokens() and get_context_window_source() calls | Test isolation failure | FM-001 (split-brain in test assertions) |
| E-009 | Future contributor adds context_window_tokens to bootstrap defaults during cleanup | Maintenance refactor | FM-009 ([1m] detection silently bypassed for all users) |
| E-010 | Downstream consumer switches on context_window_source string value after a rename refactor | Refactoring without compiler feedback | FM-015 (silent breakage of switch logic) |

---

## Edge Case Analysis

### Edge Cases in Context Window Detection

| Edge Case | Expected Behavior | Actual Behavior | Risk |
|-----------|------------------|-----------------|------|
| `ANTHROPIC_MODEL=""` (set but empty) | Return default 200K | `"".endswith("[1m]")` is False -> default. Correct. | None |
| `ANTHROPIC_MODEL="[1m]"` (suffix only, no base model) | Return 1M | `"[1m]".endswith("[1m]")` is True -> 1M. Correct. | None |
| `ANTHROPIC_MODEL="sonnet[1M]"` (uppercase M) | Return default (per current contract) | `"sonnet[1M]".endswith("[1m]")` is False -> default. Result depends on whether uppercase is a valid variant. If Anthropic uses uppercase in some contexts, silently misses detection. | P1 risk if convention allows uppercase |
| `ANTHROPIC_MODEL="sonnet[1m] "` (trailing space) | Return default (per current contract) | `"sonnet[1m] ".endswith("[1m]")` is False -> default. Trailing space in env var is unusual but possible with some shell configurations. | P2 |
| `context_window_tokens = "500000"` (string in TOML, not integer) | Return 500K | `int("500000")` succeeds -> 500K. Correct. | None |
| `context_window_tokens = "500K"` (human-readable format) | Raise/warn, fall to auto-detection | `int("500K")` raises ValueError, except catches it, falls to auto-detection. User config silently ignored. | P1 (FM-008) |
| `context_window_tokens = 1_000_000` (Python underscore syntax in TOML) | Behavior depends on TOML parser | TOML parsers do not support Python underscore syntax in integers. Parsed as string or error. `int("1_000_000")` actually succeeds in Python 3.6+, so if the TOML parser passes the raw string "1_000_000", it works. If TOML parser errors, the key may be absent. | P2 |
| `context_window_tokens = 0` | Should error or warn | `int(0)` succeeds, returns (0, "config"). Division by zero in estimator (FM-003). | P0 |
| `context_window_tokens = -1` | Should error or warn | `int(-1)` succeeds, returns (-1, "config"). Negative fill_percentage (FM-004). | P0 |
| Threshold where nominal > emergency | Should error | No validation. Proceeds to _classify_tier() with inverted ordering (FM-005). | P0 |
| fill_percentage > 1.0 (token_count > context_window) | Return EMERGENCY | EMERGENCY is classified at `>= emergency` (0.88 default). At 1.0+ fill, EMERGENCY is correctly returned. However, the condition was reached by a misconfigured context_window (too small). The underlying cause (wrong window) is masked by the correct tier. | P2 |

---

## Risk Summary

| ID | Priority | Failure Mode | File | Likelihood | Consequence |
|----|---------|-------------|------|-----------|-------------|
| FM-001 | P0 | Split-brain state from double-detection | `config_threshold_adapter.py:203-217`, `context_fill_estimator.py:144-145` | Low-prod / Med-test | Silent data corruption in FillEstimate |
| FM-002 | P0 | _FAIL_OPEN_ESTIMATE hardcodes 200K | `context_fill_estimator.py:56-60` | High | Wrong context_window in fail-open path |
| FM-003 | P0 | Division-by-zero on context_window=0 | `context_fill_estimator.py:146` | Low | Hook crash (ZeroDivisionError) |
| FM-004 | P0 | Negative fill_percentage on negative window | `config_threshold_adapter.py:233` | Low | Invalid FillEstimate, XML contract violation |
| FM-005 | P0 | Inverted thresholds cause silent misclassification | `context_fill_estimator.py:211-224` | Moderate | Wrong tier assignments, wrong action recommendations |
| FM-006 | P1 | [1m] suffix tied to undocumented external convention | `config_threshold_adapter.py:57-61` | Moderate | Silent fallback to 200K on convention change |
| FM-007 | P1 | Double-detection N+1 config reads per estimate() | `config_threshold_adapter.py:203-217` | High (structural) | Overhead + FM-001 split-brain risk |
| FM-008 | P1 | Raw get() + manual int() bypasses typed config access | `config_threshold_adapter.py:229-235` | Moderate | User config silently ignored on type mismatch |
| FM-009 | P1 | bootstrap defaults fragility (context_window_tokens absent by design, unguarded) | `bootstrap.py:584-594` | Low-initially / rising | [1m] detection bypassed if default added |
| FM-010 | P1 | FillEstimate.context_window defaults to 200K -- "unknown" conflated with "200K" | `fill_estimate.py:56-58` | High (structural) | Cannot distinguish unknown from 200K configured |
| FM-011 | P1 | Non-atomic threshold reads in _classify_tier() | `context_fill_estimator.py:211-214` | Low-prod / Mod-test | Inconsistent threshold snapshot |
| FM-012 | P2 | No validation that thresholds are in [0.0, 1.0] | `config_threshold_adapter.py:109-140` | Low | Silent misclassification |
| FM-013 | P2 | XML tag token budget validated only for WARNING+200K, not all combinations | `context_fill_estimator.py:157-193` | Low | Exceeds 200-token budget for some combinations |
| FM-014 | P2 | Calibration protocol update not in 7-file implementation scope | TASK-006 AC Step 6 | High (definitionally) | Enterprise users remain misconfigured |
| FM-015 | P2 | context_window_source untyped string -- typo-prone for downstream consumers | All files | Moderate | Silent breakage after rename refactor |

---

## Mitigation Recommendations

### For P0 Failures (Critical -- Address Before Merge)

**FM-001 and FM-007 (Split-brain / double detection):**
Refactor `ContextFillEstimator.estimate()` to call `_detect_context_window()` exactly once, storing both outputs:

```python
context_window, context_window_source = self._threshold_config.get_context_window_with_source()
```

Add `get_context_window_with_source() -> tuple[int, str]` to `IThresholdConfiguration`. Remove the separate `get_context_window_source()` method from the port to prevent independent calls. Alternatively, make `estimate()` call `get_context_window_tokens()` once and infer source from the returned value (less ideal -- loses source semantics).

**FM-002 (_FAIL_OPEN_ESTIMATE hardcodes 200K):**
Convert `_FAIL_OPEN_ESTIMATE` from a module-level singleton to a function that accepts `threshold_config` and constructs an appropriate fail-open estimate:

```python
def _make_fail_open_estimate(threshold_config: IThresholdConfiguration) -> FillEstimate:
    context_window = threshold_config.get_context_window_tokens()
    context_window_source = threshold_config.get_context_window_source()
    return FillEstimate(
        fill_percentage=0.0,
        tier=ThresholdTier.NOMINAL,
        token_count=None,
        context_window=context_window,
        context_window_source=context_window_source,
    )
```

Or: add `context_window` and `context_window_source` as `Optional` fields with a sentinel meaning "unknown" (`context_window: int | None = None`), and let downstream consumers distinguish "genuinely detected 200K" from "fail-open unknown".

**FM-003 (ZeroDivisionError):**
Add a guard in `_detect_context_window()` that rejects non-positive values:

```python
if int(explicit) <= 0:
    pass  # fall through to auto-detection
```

Add equivalent guard in `estimate()` before division:

```python
if context_window <= 0:
    logger.warning("Invalid context_window %d; returning NOMINAL (fail-open)", context_window)
    return _make_fail_open_estimate(self._threshold_config)
```

**FM-004 (Negative fill_percentage):**
Same guard as FM-003 covers the config path. Add a post-division clamp or assertion in `estimate()`:

```python
fill_percentage = max(0.0, token_count / context_window)
```

**FM-005 (Inverted thresholds):**
Add threshold ordering validation in `ConfigThresholdAdapter.get_all_thresholds()` or in a dedicated `validate()` method called at bootstrap:

```python
def _validate_threshold_ordering(self) -> None:
    n, w, c, e = self.get_threshold("nominal"), ..., ...
    if not (n < w < c < e):
        raise ConfigurationError(
            f"Threshold ordering violated: nominal={n} warning={w} critical={c} emergency={e}. "
            "Must satisfy nominal < warning < critical < emergency."
        )
```

Call at `ConfigThresholdAdapter.__init__` or at `bootstrap.py` startup.

### For P1 Failures (Major -- Address in This Sprint or Next)

**FM-006 ([1m] convention fragility):**
Add a `_KNOWN_EXTENDED_SUFFIXES: frozenset[str] = frozenset({"[1m]"})` constant with a version comment. Add a monitoring test that fetches the actual `ANTHROPIC_MODEL` from the live environment in CI (if available) and logs a warning if it does not match any known suffix patterns. Consider logging a `DEBUG` message when [1m] is detected or not detected, to provide observability.

**FM-008 (Raw get() vs typed access):**
If `LayeredConfigAdapter` has a `get_int()` method that returns a default when absent, use `get_int(key, default=None)` with a sentinel default, or check if `get_int_optional(key)` is available and preferred per the TASK-006 specification. Document the explicit choice in a comment.

**FM-009 (bootstrap fragility):**
Add a unit test that directly inspects the bootstrap defaults dict and asserts `context_window_tokens` is NOT in it. This gives a test-level guard against accidental addition.

**FM-010 (FillEstimate 200K default conflation):**
Either: (a) change `context_window: int = 200_000` to `context_window: int | None = None` and update all consumers to handle None as "unknown", or (b) add a `@classmethod` `FillEstimate.unknown()` factory that explicitly signals "fail-open" semantics. Either approach makes the distinction explicit rather than implicit.

**FM-014 (Calibration protocol missing):**
Complete TASK-006 Step 6 as a separate tracked item. The implementation is incomplete per its own acceptance criteria.

**FM-015 (Untyped source string):**
Replace `context_window_source: str` with `Literal["config", "env-1m-detection", "default"]` in `FillEstimate` and the port. This enables mypy to enforce valid values at the type level.

---

*Report generated: 2026-02-20*
*Strategy: S-004 Pre-Mortem Analysis*
*Criticality: C4*
*Agent: adv-executor v1.0.0*
