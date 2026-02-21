# S-001 Red Team Analysis — TASK-006 Implementation

<!-- VERSION: 1.0.0 | DATE: 2026-02-20 | STRATEGY: S-001 Red Team Analysis -->
<!-- DELIVERABLE: TASK-006 Context Window Size Detection and Configuration -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Scope](#scope) | Attack surface and files analyzed |
| [AV-001: Integer Overflow / Memory Allocation](#av-001-integer-overflow--memory-allocation) | Malicious large integer via env var |
| [AV-002: Monitoring Suppression via Config Poisoning](#av-002-monitoring-suppression-via-config-poisoning) | Disabling alerts by inflating window or thresholds |
| [AV-003: Race Condition (Double Detection)](#av-003-race-condition-double-detection) | TOCTOU between tokens and source calls |
| [AV-004: Fail-Open Abuse](#av-004-fail-open-abuse) | Deliberate error injection to suppress alerts |
| [AV-005: Log Injection via Config Values](#av-005-log-injection-via-config-values) | Crafted values injected into warning logs |
| [AV-006: ANTHROPIC_MODEL Env Var Spoofing](#av-006-anthropic_model-env-var-spoofing) | Forcing 1M window by injecting [1m] suffix |
| [AV-007: Threshold Inversion Attack](#av-007-threshold-inversion-attack) | Setting thresholds so EMERGENCY is unreachable |
| [AV-008: Disabled Flag Stealth Suppression](#av-008-disabled-flag-stealth-suppression) | Silently zeroing monitoring output |
| [AV-009: XML Injection via context_window_source](#av-009-xml-injection-via-context_window_source) | Injecting tags into XML output field |
| [Summary Table](#summary-table) | All findings at a glance |
| [Recommended Mitigations](#recommended-mitigations) | Priority-ordered remediation actions |

---

## Scope

**Files analyzed:**

| File | Role |
|------|------|
| `src/context_monitoring/infrastructure/adapters/config_threshold_adapter.py` | Detection logic, `_detect_context_window()` |
| `src/context_monitoring/application/services/context_fill_estimator.py` | Consumer of context window, fail-open path |
| `src/context_monitoring/application/ports/threshold_configuration.py` | Protocol definition |
| `src/context_monitoring/domain/value_objects/fill_estimate.py` | Output value object |
| `src/bootstrap.py` (L575-600) | Wiring and defaults |
| `tests/unit/context_monitoring/test_config_threshold_adapter.py` | Test coverage audit |
| `tests/unit/context_monitoring/application/test_context_fill_estimator.py` | Test coverage audit |

**Attack surface summary:** Two externally controllable inputs reach the detection chain:
1. `JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS` (env var, or config.toml)
2. `ANTHROPIC_MODEL` (env var, read directly via `os.environ.get`)

Both are read at runtime on every `estimate()` call (detection is not cached). All other inputs (thresholds, enabled flag) are also controllable via the same env var / TOML mechanism.

---

## AV-001: Integer Overflow / Memory Allocation

**Classification: MITIGATED (P2)**

**Attack description:**

An attacker sets `JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS=9999999999999999999` (or Python's `sys.maxsize` value). The goal is to cause integer overflow, extremely large memory allocation, or a division-by-near-zero producing a fill of ~0.0, permanently suppressing all alerts.

**Attack path:**

1. `os.environ["JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS"] = "9999999999999999999"`
2. `_detect_context_window()` calls `int(explicit)` — succeeds with the Python arbitrary-precision integer.
3. `value > 0` check passes.
4. `context_window` is returned as 9,999,999,999,999,999,999.
5. `fill_percentage = token_count / context_window` = 190,000 / 9.99e18 ≈ 0.0000000000000019.
6. Tier classifies as NOMINAL. All alerts permanently suppressed.

**Evidence:**

- `config_threshold_adapter.py:237` — `value = int(explicit)` — Python int has no overflow.
- `config_threshold_adapter.py:237-244` — Only guard is `value <= 0`. No upper bound.
- `context_fill_estimator.py:141` — Secondary guard only checks `<= 0`. No upper bound.
- `fill_estimate.py:54` — `fill_percentage: float` — a near-zero float is valid.

**Why only P2 (Mitigated):** Python's `int` does not overflow (arbitrary precision). There is no memory allocation proportional to the integer value. The only real consequence is alert suppression — which is already covered by AV-002 as the primary concern. The implementation is not broken by the value itself; the _security consequence_ is alert suppression addressed in AV-002.

**Residual risk:** The alert suppression outcome is real (fill -> 0.0). The defense that exists is: the integer is accepted without error. The _effect_ is classified separately under AV-002.

**Recommended mitigation:** Add an upper bound check. A reasonable ceiling is `1_000_000` (1M tokens, the maximum known Claude context). Values above this should trigger the same warning and fall-through as non-positive values.

---

## AV-002: Monitoring Suppression via Config Poisoning

**Classification: EXPLOITABLE (P0)**

**Attack description:**

An attacker (with environment variable or config.toml write access) sets `context_window_tokens` to an astronomically large value. The result: `fill_percentage` approaches zero for any realistic token count, all alerts are permanently silenced, and `is_enabled()` still returns `True`. The user has no indication that monitoring is degraded — the XML tag will output `<tier>NOMINAL</tier>` and `<fill-percentage>0.0000</fill-percentage>` indefinitely.

This is the highest-severity finding because:
- It silently degrades a safety mechanism without triggering any error.
- The fail-open design (NOMINAL on error) amplifies this: the attack outcome is _indistinguishable_ from the expected fail-safe outcome.
- `is_enabled()` returns `True`, so operators believe monitoring is active.

**Attack path (concrete):**

```
JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS=999999999999
```

With 190,000 actual tokens: fill = 190,000 / 999,999,999,999 ≈ 0. Tier = NOMINAL. EMERGENCY never fires.

**Evidence:**

- `config_threshold_adapter.py:237-244` — `int(explicit)` accepted, `value > 0` check passes, no upper bound.
- `context_fill_estimator.py:141` — `if context_window <= 0:` — only catches zero/negative, not astronomically large.
- `context_fill_estimator.py:149` — `fill_percentage = token_count / context_window` — produces near-zero silently.
- `context_fill_estimator.py:130-132` — When disabled, returns NOMINAL. When poisoned, also returns NOMINAL. Outputs are identical.

**Variant: Threshold poisoning (secondary attack surface):**

An attacker sets all thresholds to their maximum:

```
JERRY_CONTEXT_MONITOR__EMERGENCY_THRESHOLD=0.9999999
```

Result: EMERGENCY requires fill > 99.99%, which is unreachable in practice. CRITICAL and WARNING similarly blocked. This requires four separate env vars (one per threshold), but the attack surface exists.

**Evidence:** `config_threshold_adapter.py:143` — `return self._config.get_float(key, default=default)` — no upper or lower bound validation on threshold values. A value of `2.0` for emergency_threshold means EMERGENCY can _never_ trigger (fill is always < 200%).

**Test gap:** No test verifies that a large context_window_tokens value is rejected or flagged. Tests only cover zero and negative values. No test covers thresholds outside [0.0, 1.0].

**Recommended mitigations:**
1. Add upper bound to `_detect_context_window()`: reject values above `2_000_000` (2x the largest known context) with a warning and fall-through.
2. Add threshold range validation in `get_threshold()`: reject values outside `(0.0, 1.0)` with a warning and return the default.
3. Add log output indicating the active context window value at session start, so operators can detect poisoned values from logs.

---

## AV-003: Race Condition (Double Detection)

**Classification: THEORETICAL (P1)**

**Attack description:**

`get_context_window_tokens()` and `get_context_window_source()` are two separate public methods, each calling `_detect_context_window()` independently. If `ANTHROPIC_MODEL` or `JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS` changes between the two calls, the returned (tokens, source) pair is inconsistent: the source label does not match the token value.

**Attack path:**

1. `context_fill_estimator.py:137` — `context_window = self._threshold_config.get_context_window_tokens()` — calls `_detect_context_window()` once. At this moment, `ANTHROPIC_MODEL` is absent. Returns `(200_000, "default")`.
2. An external process modifies `ANTHROPIC_MODEL=sonnet[1m]` between the two calls.
3. `context_fill_estimator.py:138` — `context_window_source = self._threshold_config.get_context_window_source()` — calls `_detect_context_window()` again. `ANTHROPIC_MODEL` is now present. Returns `(1_000_000, "env-1m-detection")`.
4. `FillEstimate` is constructed with `context_window=200_000` (from step 1) but `context_window_source="env-1m-detection"` (from step 3).
5. The XML tag reports `<context-window>200000</context-window>` and `<context-window-source>env-1m-detection</context-window-source>` — contradictory data.

**Why P1 (Theoretical):** Requires modifying the process environment mid-execution. In typical deployments (single Claude Code session), `ANTHROPIC_MODEL` is set once at process start and does not change. In containerized or adversarial test environments, it is conceivable. The consequence is misleading diagnostics, not a safety failure (the token count is what actually drives the fill calculation; the source is metadata).

**Evidence:**

- `context_fill_estimator.py:137-138` — Two separate calls to `_detect_context_window()` via port methods.
- `config_threshold_adapter.py:222` — `_detect_context_window()` reads `os.environ.get("ANTHROPIC_MODEL", "")` live on each call.
- The DRY comment at `config_threshold_adapter.py:223-228` acknowledges the split but does not address the TOCTOU.

**Recommended mitigation:** In `ContextFillEstimator.estimate()`, call a single method that returns the `(tokens, source)` tuple atomically, or add a `get_context_window()` method to `IThresholdConfiguration` that returns both values. Alternatively, cache detection results for the lifetime of the `ConfigThresholdAdapter` instance (environment changes are extremely rare in production).

---

## AV-004: Fail-Open Abuse

**Classification: THEORETICAL (P1)**

**Attack description:**

The fail-open design causes `estimate()` to return NOMINAL on _any_ exception from the reader or threshold config. An attacker who can cause a controlled exception in the reader path (e.g., by deleting the transcript file, corrupting the JSONL, or causing a permissions error) will cause monitoring to silently return NOMINAL — identical to the legitimate fail-safe outcome.

**Attack path (transcript deletion):**

1. Attacker deletes or chmod 000's the transcript file.
2. `JsonlTranscriptReader.read_latest_tokens()` raises `FileNotFoundError`.
3. `context_fill_estimator.py:159` — `except Exception as exc:` catches it.
4. `context_fill_estimator.py:165` — Returns `_FAIL_OPEN_ESTIMATE` with tier NOMINAL.
5. EMERGENCY is never triggered even if the context is genuinely at 99%.

**Why P1 (Theoretical):** File deletion requires local system access, which implies broader compromise. An attacker with filesystem write access has more impactful vectors. The fail-open design is an intentional, documented architectural choice that protects against infrastructure failures. The tradeoff is acknowledged in the docstring.

**Evidence:**

- `context_fill_estimator.py:55-60` — `_FAIL_OPEN_ESTIMATE` singleton with `tier=NOMINAL`.
- `context_fill_estimator.py:159-165` — Broad `except Exception` returning that sentinel.
- The sentinel shares the same output format as legitimate NOMINAL (fill=0.0, token_count=None).

**Recommended mitigation (low priority):**

Add a `monitoring_degraded` field to `FillEstimate` (bool, default False) that is set to True when the fail-open path is taken. The XML output would include `<monitoring-degraded>true</monitoring-degraded>`, allowing downstream consumers to distinguish genuine NOMINAL from a suppressed error state. This preserves fail-open semantics while providing observability.

---

## AV-005: Log Injection via Config Values

**Classification: MITIGATED (P2)**

**Attack description:**

An attacker sets `JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS` to a value containing newlines or log formatting characters, attempting to inject false log entries via the `logger.warning()` calls.

**Example payload:**

```
JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS="0\nERROR fake_module - SECURITY BREACH DETECTED"
```

**Attack path:**

1. `_detect_context_window()` reads the value.
2. `int("0\nERROR...")` raises `ValueError` (cannot parse).
3. The `except (ValueError, TypeError)` branch logs: `logger.warning("Cannot parse context_window_tokens=%r as integer; ...", explicit)`.
4. `%r` (repr) is used in the format string, which would produce `"'0\\nERROR fake_module - SECURITY BREACH DETECTED'"` — the newline is escaped by repr.

**Why P2 (Mitigated):**

- `config_threshold_adapter.py:247` — `%r` (repr format) is used for the invalid value. `repr()` escapes newlines, null bytes, and control characters. A `\n` in the value becomes `\\n` in the log output, preventing log line injection.
- `config_threshold_adapter.py:239` — The negative/zero branch uses `%d` (integer format), which cannot carry injection payloads since the value has already been successfully cast to `int`.

**Evidence:**

- `config_threshold_adapter.py:247` — `logger.warning("Cannot parse context_window_tokens=%r as integer; ...", explicit)` — `%r` is safe.
- `config_threshold_adapter.py:239` — `logger.warning("Invalid context_window_tokens=%d ...", value)` — integer format is safe.

**Note:** This is correctly mitigated. No action required. The use of `%r` for repr-formatting untrusted input in log messages is the correct pattern.

---

## AV-006: ANTHROPIC_MODEL Env Var Spoofing

**Classification: THEORETICAL (P1)**

**Attack description:**

An attacker sets `ANTHROPIC_MODEL=any-string[1m]` to force the 1M context window detection, causing the system to underestimate fill percentage. With 1M context window and a 200K actual window, fill percentage is reported at 20% when the actual fill is 100%. EMERGENCY is never triggered.

**Attack path:**

1. `ANTHROPIC_MODEL=fake-model[1m]`
2. `_detect_context_window()` at `config_threshold_adapter.py:255` — `model_env.endswith("[1m]")` is True.
3. Returns `(1_000_000, "env-1m-detection")`.
4. `fill_percentage = token_count / 1_000_000` — 5x underestimate for a standard 200K window.
5. At actual 190K tokens (95% fill), reported fill = 0.19 = NOMINAL.

**Why P1 (Theoretical):** Requires the ability to set process environment variables, which implies pre-existing system access. `ANTHROPIC_MODEL` is a legitimate system variable that an attacker with local access could manipulate. In a shared environment, this is more plausible.

**Evidence:**

- `config_threshold_adapter.py:254-256` — `model_env = os.environ.get("ANTHROPIC_MODEL", ""); if model_env.endswith("[1m]"): return _EXTENDED_CONTEXT_WINDOW, "env-1m-detection"` — any value ending in `[1m]` is accepted.
- No validation that `ANTHROPIC_MODEL` matches a known-valid Claude model pattern.
- `config_threshold_adapter.py:63` — The `endswith` check was deliberately chosen to avoid false positives from substrings, but it does not validate the model name itself.

**Recommended mitigation:** Optionally validate that the model name before `[1m]` matches a known Claude model prefix pattern (e.g., `claude-`, `sonnet`, `opus`, `haiku`). This is SOFT — the benefit is marginal and adds coupling to a vendor-specific model naming scheme that may change. A pragmatic alternative is to log the detected model value at DEBUG level so operators can audit what model was detected.

---

## AV-007: Threshold Inversion Attack

**Classification: EXPLOITABLE (P0)**

**Attack description:**

An attacker sets threshold values to logically invalid states:

- **Zero/negative thresholds:** `JERRY_CONTEXT_MONITOR__EMERGENCY_THRESHOLD=0` causes EMERGENCY to trigger immediately at any fill level, flooding operators with false alerts (denial-of-utility).
- **Inverted thresholds:** `JERRY_CONTEXT_MONITOR__EMERGENCY_THRESHOLD=2.0` causes EMERGENCY to never trigger (fill is always < 200%).
- **Out-of-order thresholds:** `JERRY_CONTEXT_MONITOR__WARNING_THRESHOLD=0.95`, `JERRY_CONTEXT_MONITOR__CRITICAL_THRESHOLD=0.10` inverts the meaning of WARNING and CRITICAL.

The `_classify_tier()` method evaluates thresholds in fixed order (emergency -> critical -> warning -> nominal) with no validation of relative ordering. Inverted thresholds cause tier misclassification without errors.

**Attack path (EMERGENCY suppression):**

1. `JERRY_CONTEXT_MONITOR__EMERGENCY_THRESHOLD=2.0`
2. `_classify_tier()` at `context_fill_estimator.py:226` — `if fill_percentage >= 2.0:` is never True.
3. Falls through to `fill_percentage >= critical` — with default 0.80, CRITICAL fires at 80% fill.
4. But attacker also sets `JERRY_CONTEXT_MONITOR__CRITICAL_THRESHOLD=2.0`, `JERRY_CONTEXT_MONITOR__WARNING_THRESHOLD=2.0`.
5. All tiers above nominal are unreachable. Only NOMINAL and LOW are ever returned.

**Evidence:**

- `config_threshold_adapter.py:143` — `return self._config.get_float(key, default=default)` — no bounds validation.
- `context_fill_estimator.py:221-234` — `_classify_tier()` uses raw threshold values with no range validation.
- Tests in `test_config_threshold_adapter.py` validate only correct values (0.75, 0.90, etc.); no test verifies rejection of values outside (0.0, 1.0).
- No test verifies threshold ordering invariant (nominal < warning < critical < emergency).

**Why P0 (Exploitable):** Unlike AV-002 which requires a very large integer, threshold inversion only requires setting a float to `2.0` — a plausible accidental misconfiguration as well as an intentional attack. The consequence (EMERGENCY never fires) is identical to AV-002 but via a different mechanism with no existing guard.

**Recommended mitigations:**
1. In `get_threshold()`, validate that the returned float is in `(0.0, 1.0)`. Values outside this range should log a warning and return the hardcoded default.
2. Add a `_validate_threshold_ordering()` check called at `ConfigThresholdAdapter.__init__()` or on first use, verifying `nominal < warning < critical < emergency`. Log a warning (do not crash) if the invariant is violated.

---

## AV-008: Disabled Flag Stealth Suppression

**Classification: MITIGATED (P2)**

**Attack description:**

An attacker sets `JERRY_CONTEXT_MONITOR__ENABLED=false` to disable monitoring silently. The service returns NOMINAL regardless of actual fill. There is no operator alert that monitoring is disabled.

**Why P2 (Mitigated):** Disabling monitoring via `enabled=false` is an _intentional, documented_ design feature. It is explicitly tested and expected behavior. The `is_enabled()` check at `context_fill_estimator.py:130` is clear and its result is logged at DEBUG level. This is not a vulnerability — it is a designed administrative control.

**Evidence:**

- `context_fill_estimator.py:130-132` — `if not self._threshold_config.is_enabled(): logger.debug("Context monitoring disabled; returning NOMINAL.")` — explicit log message exists.

**Residual concern (SOFT):** The log level is DEBUG, not WARNING or INFO. In production deployments with INFO-level logging, a disabled monitoring state would not appear in logs. Consider upgrading to INFO to aid operational visibility.

---

## AV-009: XML Injection via context_window_source

**Classification: THEORETICAL (P1)**

**Attack description:**

`FillEstimate.context_window_source` is a free-form string written directly into the XML output at `context_fill_estimator.py:200`:

```python
f"  <context-window-source>{estimate.context_window_source}</context-window-source>\n"
```

If an attacker can control `context_window_source` to contain XML special characters or closing tags, they can inject arbitrary XML into the `<context-monitor>` output.

**Attack path:**

1. An attacker sets `JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS=999` and also contrives a situation where `context_window_source` is derived from a user-controlled string.
2. In the current implementation, `context_window_source` is only ever one of: `"config"`, `"env-1m-detection"`, or `"default"`. These are hardcoded string constants in `_detect_context_window()`.
3. However, `FillEstimate.context_window_source: str = "default"` is a bare string field with no validation. A test, mock, or future code path could set it to `"</context-window-source><injected>payload</injected><context-window-source>"`.

**Why P1 (Theoretical):** In the current implementation, `context_window_source` can only take one of three hardcoded values from `_detect_context_window()`. The injection path does not exist in production code. It exists as a latent risk if the field is ever populated from an external source or if the adapter is extended.

**Evidence:**

- `context_fill_estimator.py:200` — Unescaped f-string interpolation: `f"  <context-window-source>{estimate.context_window_source}</context-window-source>\n"`.
- `fill_estimate.py:58` — `context_window_source: str = "default"` — unconstrained string type.
- `config_threshold_adapter.py:244,256,261` — Only three literals returned; currently safe.

**Recommended mitigation (low priority):** Either constrain `context_window_source` to a `Literal["config", "env-1m-detection", "default"]` type (catches violations at type-check time), or XML-escape the field value before interpolation. The `Literal` type is the most principled defense.

---

## Summary Table

| ID | Attack Vector | Classification | Severity | File:Line |
|----|--------------|----------------|----------|-----------|
| AV-001 | Large integer via env var (integer overflow attempt) | MITIGATED (P2) | Low | `config_threshold_adapter.py:237` |
| AV-002 | Context window poisoning to suppress all alerts | **EXPLOITABLE (P0)** | **Critical** | `config_threshold_adapter.py:237-244`, `context_fill_estimator.py:141` |
| AV-003 | Race condition: tokens/source TOCTOU inconsistency | THEORETICAL (P1) | Medium | `context_fill_estimator.py:137-138` |
| AV-004 | Fail-open abuse via transcript deletion | THEORETICAL (P1) | Medium | `context_fill_estimator.py:159-165` |
| AV-005 | Log injection via crafted config values | MITIGATED (P2) | None | `config_threshold_adapter.py:247` |
| AV-006 | ANTHROPIC_MODEL spoofing to force 1M window | THEORETICAL (P1) | Medium | `config_threshold_adapter.py:254-256` |
| AV-007 | Threshold inversion to suppress EMERGENCY tier | **EXPLOITABLE (P0)** | **Critical** | `config_threshold_adapter.py:143`, `context_fill_estimator.py:221-234` |
| AV-008 | Enabled flag stealth suppression | MITIGATED (P2) | Low | `context_fill_estimator.py:130-132` |
| AV-009 | XML injection via context_window_source field | THEORETICAL (P1) | Low | `context_fill_estimator.py:200`, `fill_estimate.py:58` |

**P0 count: 2 | P1 count: 4 | P2 count: 3**

---

## Recommended Mitigations

Ordered by priority (P0 first):

### P0-A: Add upper bound to context_window_tokens (AV-002)

**Location:** `config_threshold_adapter.py:_detect_context_window()` after line 237

```python
_MAX_CONTEXT_WINDOW_TOKENS: int = 2_000_000  # 2x known maximum

# In _detect_context_window():
value = int(explicit)
if value <= 0 or value > _MAX_CONTEXT_WINDOW_TOKENS:
    logger.warning(
        "Invalid context_window_tokens=%d (must be 1 to %d); "
        "falling through to auto-detection.",
        value, _MAX_CONTEXT_WINDOW_TOKENS,
    )
else:
    return value, "config"
```

**Also add** the same guard in `context_fill_estimator.py:141`:

```python
if context_window <= 0 or context_window > _MAX_CONTEXT_WINDOW_TOKENS:
    ...fallback to 200_000
```

### P0-B: Add threshold range validation (AV-007)

**Location:** `config_threshold_adapter.py:get_threshold()` after line 143

```python
value = self._config.get_float(key, default=default)
if not (0.0 < value <= 1.0):
    logger.warning(
        "Threshold %r=%r is outside valid range (0.0, 1.0]; "
        "using default %r.",
        tier, value, default,
    )
    return default
return value
```

### P1-A: Eliminate TOCTOU in ContextFillEstimator (AV-003)

**Location:** `context_fill_estimator.py:137-138` and `IThresholdConfiguration` port

Add `get_context_window() -> tuple[int, str]` to the port and adapter that returns both values atomically from a single `_detect_context_window()` call. Change `estimate()` to use this single call.

### P1-B: Constrain context_window_source type (AV-009)

**Location:** `fill_estimate.py:58`

```python
from typing import Literal
context_window_source: Literal["config", "env-1m-detection", "default"] = "default"
```

This provides static type-checking enforcement at zero runtime cost.

### SOFT-A: Upgrade disabled-state log level (AV-008)

Change `logger.debug("Context monitoring disabled; returning NOMINAL.")` to `logger.info(...)` to ensure disabled monitoring state is visible in production INFO-level logs.

### SOFT-B: Log active context window at session start (AV-002 observability)

In `bootstrap.py`, after constructing `threshold_config`, log the detected context window at INFO level:

```python
logger.info(
    "Context monitoring: window=%d tokens (source=%s)",
    threshold_config.get_context_window_tokens(),
    threshold_config.get_context_window_source(),
)
```

This allows operators to detect poisoned configurations from startup logs without code changes.

---

*Red Team Analysis completed by adv-executor agent (S-001). Strategy: Adversarial attack simulation with concrete exploit paths. Date: 2026-02-20.*
