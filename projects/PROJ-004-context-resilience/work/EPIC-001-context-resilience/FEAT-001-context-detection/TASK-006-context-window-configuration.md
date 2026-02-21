# TASK-006: Context Window Size Detection and Configuration

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-02-20
> **Due:** --
> **Completed:** --
> **Parent:** EN-008
> **Owner:** --
> **Effort:** 6-8h

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Description](#description) | What needs to be done |
| [Problem Analysis](#problem-analysis) | Root cause and impact |
| [Research Findings](#research-findings) | Claude Code context window landscape |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Architectural Decision: Detection in ConfigThresholdAdapter](#architectural-decision-detection-in-configthresholdadapter) | Why multi-boundary detection lives in the adapter |
| [Implementation Notes](#implementation-notes) | Technical guidance |
| [Related Items](#related-items) | Links |
| [History](#history) | Status changes |

---

## Description

**Severity:** High -- the entire fill detection system produces incorrect results for any user whose context window is not exactly 200K tokens.

The `ContextFillEstimator` hardcodes `_DEFAULT_CONTEXT_WINDOW = 200_000` and all callers use this default. A config key `context_monitoring.context_window_tokens` exists in `bootstrap.py:585` but is **never wired** to the estimator. This means:

1. Users cannot configure their actual context window size
2. The fill percentages and tier classifications are wrong for any non-200K window
3. Thresholds fire too early (larger windows like 500K/1M) or too late (if smaller windows exist)

This task addresses two issues:

1. **Fix the disconnect** (primary): Wire the existing config key to the estimator through `IThresholdConfiguration`. The plumbing is half-done -- the config key exists but is never read.
2. **Add `[1m]` auto-detection** (secondary): Detect the `[1m]` model alias suffix to automatically set 1M context window for extended-context users, with user config as override.

**Backward compatibility:** The fix is additive and non-breaking. The default fallback remains 200,000, ensuring full backward compatibility for all current users on Pro/Team Standard plans. No existing behavior changes unless the user explicitly configures a different value or uses a `[1m]` model alias.

**Scope limitation:** Auto-detection handles `[1m]` extended-context users only. Enterprise users (500K) cannot be auto-detected because the same model aliases run on both Pro (200K) and Enterprise (500K) plans. Enterprise users must explicitly configure their context window size via the config key. This is documented in the calibration protocol.

---

## Problem Analysis

### The Disconnect

```
bootstrap.py:585  →  config default: "context_monitoring.context_window_tokens": 200000
                     ↓ (NEVER READ)
ContextFillEstimator._DEFAULT_CONTEXT_WINDOW = 200_000  ← hardcoded fallback
                     ↓
estimate(transcript_path)  ← callers never pass context_window parameter
                     ↓
fill_percentage = token_count / 200_000  ← ALWAYS divides by 200K
```

### Impact by Context Window Size

| Actual Window | Hardcoded 200K | At 160K tokens | Reported Fill | Actual Fill | Error |
|--------------|----------------|-----------------|---------------|-------------|-------|
| 200K | 200K | 160K | 80% (CRITICAL) | 80% (CRITICAL) | 0% |
| 500K | 200K | 160K | 80% (CRITICAL) | 32% (NOMINAL) | +48% |
| 1M   | 200K | 160K | 80% (CRITICAL) | 16% (NOMINAL) | +64% |

For Enterprise users (500K), the current bug causes a CRITICAL-tier false positive when context is only 32% full, potentially triggering unnecessary compaction and wasting tokens on false warnings. Enterprise deployments of Claude Code are a primary target for long-running agentic sessions where context management matters most -- making them the users most harmed by this bug. Enterprise users must explicitly configure their window size (see [Calibration Protocol](#step-6-update-calibration-protocol)) because auto-detection cannot distinguish Enterprise from Pro tiers.

For extended-context `[1m]` users (1M), the error is +64%. These users are auto-detected via the `[1m]` model alias suffix.

---

## Research Findings

### Context Window Sizes by Plan and Model

Source: [Claude Code Model Configuration](https://code.claude.com/docs/en/model-config), [Claude Help Center](https://support.claude.com/en/articles/8606394-how-large-is-the-context-window-on-paid-claude-plans)

| Plan / Mode | Context Window | Model Alias Example | Auto-Detectable? |
|---|---|---|---|
| Pro, Team Standard | 200K | `sonnet`, `opus` | No (default applied) |
| Max, Team Premium | 200K | `sonnet`, `opus` | No (default applied) |
| Enterprise | 500K | `sonnet`, `opus` | **No** (requires user config) |
| Extended context (API/pay-as-you-go) | 1M | `sonnet[1m]`, `opus[1m]` | **Yes** (via `[1m]` suffix) |
| Extended context (subscribers w/ extra usage) | 1M | `sonnet[1m]`, `opus[1m]` | **Yes** (via `[1m]` suffix) |

**Key constraint:** The same model alias (e.g., `claude-sonnet-4-6`) runs on both Pro (200K) and Enterprise (500K) plans. Model name alone cannot determine context window for the Enterprise case. The `[1m]` suffix is the only model-level signal that reliably indicates a non-200K window without user configuration. This justifies why user configuration is the highest priority in the detection chain and why Enterprise users are directed to the calibration protocol.

### Detection Mechanisms Available

| Mechanism | What It Provides | Accessible From Hooks? |
|---|---|---|
| `/status` command | Account info, current model, context usage | No (interactive only) |
| `ANTHROPIC_MODEL` env var | Model alias/name (may include `[1m]`) | Yes |
| Transcript file (`$TRANSCRIPT_PATH`) | Model name in API response `message.model` field | Yes (via backward scan) |
| Model alias `[1m]` suffix | Explicitly encodes 1M context window | Yes (if set via env/config) |
| User configuration | Explicit context window override | Yes (via LayeredConfigAdapter) |

### `[1m]` Suffix Convention

The `[1m]` suffix is used in Claude Code model alias configuration to select extended context. Source: [Claude Code Model Configuration](https://code.claude.com/docs/en/model-config). Examples: `sonnet[1m]`, `opus[1m]`. The `ANTHROPIC_MODEL` env var may contain this suffix when set by the user or by Claude Code's model selector.

**Detection approach:** Check if `[1m]` appears as a suffix in the model alias string (e.g., `sonnet[1m]`). Use `str.endswith("[1m]")` rather than substring `in` matching to avoid false positives on model names that might contain `[1m]` in non-suffix positions.

### Canonical Detection Priority (Authoritative)

This is the single authoritative ordering for context window detection. All implementation code and documentation must follow this ordering exactly.

```
1. Explicit user config: JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS env var
2. Explicit user config: [context_monitor] context_window_tokens in .jerry/config.toml
   (Steps 1-2 resolved by LayeredConfigAdapter — single call to get_int_optional)
3. ANTHROPIC_MODEL env var with [1m] suffix → 1,000,000
4. Transcript model name with [1m] suffix → 1,000,000
5. Default: 200,000
```

**Notes:**
- Steps 1-2 are explicit user configuration (highest priority). This is the Enterprise resolution path.
- Steps 3-4 detect `[1m]` extended-context users automatically.
- Step 5 is the fail-safe default. This is correct for Pro/Team Standard users (the majority).
- The previous draft included a model-to-window lookup table at step 5. This has been removed because all current Claude models have a 200K standard window, making the lookup functionally identical to the default. A lookup table should be added when a model ships with a non-200K standard window (see [Implementation Notes: Future Extension](#future-extension-model-lookup-table)).
- There is no separate "transcript model lookup" step because without a lookup table, transcript model detection provides no additional signal beyond `[1m]` suffix checking.

---

## Acceptance Criteria

### Configuration (fix the disconnect)

- [ ] `IThresholdConfiguration` port exposes `get_context_window_tokens() -> int` method
- [ ] `ConfigThresholdAdapter` implements `get_context_window_tokens()` reading from `context_monitor.context_window_tokens` config key
- [ ] `ContextFillEstimator` reads context window size from `IThresholdConfiguration` instead of hardcoded constant
- [ ] `bootstrap.py` wires the config value through (fix the disconnect at line 585)
- [ ] User can override via environment variable: `JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS=500000`
- [ ] User can override via `.jerry/config.toml`: `[context_monitor]\ncontext_window_tokens = 500000`
- [ ] Default remains 200,000 when not configured (backward compatible)

### Auto-Detection

- [ ] `ANTHROPIC_MODEL` env var is checked for `[1m]` suffix (using `endswith`, not substring `in`) → sets context window to 1,000,000
- [ ] Auto-detected value is used when user has not explicitly configured a value
- [ ] Auto-detection is fail-open: any exception during detection falls back to 200K default
- [ ] All detection logic lives in `ConfigThresholdAdapter` (infrastructure layer), NOT in `ContextFillEstimator` (application layer) -- see [Architectural Decision](#architectural-decision-detection-in-configthresholdadapter)

### Observability

- [ ] `<context-monitor>` XML tag includes `<context-window>` field showing the active window size in tokens
- [ ] `<context-monitor>` XML tag includes `<context-window-source>` field showing how it was determined
- [ ] Valid `<context-window-source>` values: `config`, `env-1m-detection`, `default`
- [ ] Calibration protocol (`docs/knowledge/context-resilience/calibration-protocol.md`) updated with configuration instructions per plan

### Tests

> **BDD Requirement (H-20):** Write the failing test for each acceptance criterion BEFORE implementing the corresponding step.

- [ ] Unit test: `ContextFillEstimator.estimate()` uses context window from `IThresholdConfiguration.get_context_window_tokens()` -- verified by mocking adapter to return 500,000 and asserting `fill_percentage = token_count / 500_000` (not 200,000)
- [ ] Unit tests for: explicit config override (env var), explicit config override (toml), `ANTHROPIC_MODEL` `[1m]` suffix detection via `endswith`, `ANTHROPIC_MODEL` without `[1m]` suffix (returns default), `ANTHROPIC_MODEL` not set (returns default), default fallback
- [ ] Unit test: `[1m]` detection does NOT false-positive on model names containing `[1m]` in non-suffix positions (e.g., `my-custom-[1m]-wrapper` if using substring matching)
- [ ] Unit test: XML output includes `<context-window>` and `<context-window-source>` with correct values for each detection path
- [ ] Existing 229 hook tests still pass (no regression)

---

## Architectural Decision: Detection in ConfigThresholdAdapter

**Context:** The detection logic for context window size involves reading from two external boundaries: (1) configuration files/env vars via `LayeredConfigAdapter`, and (2) the `ANTHROPIC_MODEL` environment variable directly. DA-002 raised an SRP concern about placing multi-boundary detection in `ConfigThresholdAdapter`.

**Decision:** Keep detection logic in `ConfigThresholdAdapter` rather than creating a separate `ContextWindowDetector` service.

**Rationale:**

1. **Scope is minimal after simplification.** With the model lookup table removed (DA-004) and transcript reading removed (DA-005), the adapter only accesses two boundaries: (a) the `LayeredConfigAdapter` it already holds, and (b) a single `os.environ.get("ANTHROPIC_MODEL")` call. This is comparable to other adapters that read config + a single env var.
2. **No new port needed.** A `ContextWindowDetector` service would require a new application-layer port (`IContextWindowDetector`) and a new infrastructure adapter implementing it. This adds 2 files, 2 interfaces, and additional bootstrap wiring for a method that is called once per `estimate()` invocation and returns a single integer.
3. **Testability preserved.** `ConfigThresholdAdapter.get_context_window_tokens()` is testable by: (a) providing a mock `LayeredConfigAdapter`, (b) setting/unsetting `ANTHROPIC_MODEL` env var in tests. No additional test doubles needed.
4. **The env var read is a detection fallback, not an external system integration.** `ANTHROPIC_MODEL` is a process-local environment variable, not a network call or file I/O. Reading it is a lightweight operation that does not warrant a dedicated adapter.

**Trade-off accepted:** If future detection signals require network calls, file I/O, or multiple new env vars, the detection logic should be extracted to a dedicated `ContextWindowDetector` service at that point. The current scope does not justify this.

---

## Implementation Notes

> **BDD Requirement (H-20):** Write the failing test for each acceptance criterion BEFORE implementing the corresponding step. Reference the relevant AC item when starting each step.

### Step 1: Add port method

**AC:** Configuration [line 1: `IThresholdConfiguration` port]

In `src/context_monitoring/application/ports/threshold_configuration.py`, add:
```python
def get_context_window_tokens(self) -> int:
    """Get the configured or detected context window size in tokens.

    Returns the context window size following the canonical detection priority:
    explicit user config > ANTHROPIC_MODEL [1m] suffix > default 200K.
    Always fail-open: detection failures return 200_000.
    """
    ...
```

### Step 2: Implement in ConfigThresholdAdapter

**AC:** Configuration [line 2], Auto-Detection [lines 1-4]

In `src/context_monitoring/infrastructure/adapters/config_threshold_adapter.py`:

```python
_DEFAULT_CONTEXT_WINDOW_TOKENS: int = 200_000
_EXTENDED_CONTEXT_WINDOW: int = 1_000_000

# [1m] suffix convention: used in Claude Code model alias configuration
# to select extended context (1M tokens).
# Source: https://code.claude.com/docs/en/model-config
# Examples: sonnet[1m], opus[1m]
# Detection uses endswith("[1m]") to avoid false positives.
_EXTENDED_CONTEXT_SUFFIX: str = "[1m]"


def get_context_window_tokens(self) -> int:
    """Get context window size using canonical detection priority.

    Priority (highest to lowest):
    1. Explicit user config (env var or config.toml via LayeredConfigAdapter)
    2. ANTHROPIC_MODEL env var with [1m] suffix → 1,000,000
    3. Default: 200,000

    All detection failures return the default (fail-open).
    """
    # 1. Explicit user config (highest priority, handles Enterprise 500K)
    key = f"{_CONFIG_NAMESPACE}.context_window_tokens"
    explicit = self._config.get_int_optional(key)
    if explicit is not None:
        return explicit

    try:
        # 2. Check ANTHROPIC_MODEL env var for [1m] suffix
        model_env = os.environ.get("ANTHROPIC_MODEL", "")
        if model_env.endswith(_EXTENDED_CONTEXT_SUFFIX):
            return _EXTENDED_CONTEXT_WINDOW
    except Exception:
        pass  # fail-open: any detection error returns default

    # 3. Default (correct for Pro/Team Standard 200K)
    return _DEFAULT_CONTEXT_WINDOW_TOKENS
```

> **Note:** This sample is the complete implementation. The previous draft included a model-to-window lookup table and transcript reading -- both have been removed. See [Future Extension](#future-extension-model-lookup-table) for when to add these back.

### Step 3: Wire into ContextFillEstimator

**AC:** Configuration [line 3]

`ContextFillEstimator` already receives `IThresholdConfiguration` via constructor. Remove `_DEFAULT_CONTEXT_WINDOW` constant. Change `estimate()`:

```python
def estimate(self, transcript_path: str) -> FillEstimate:
    # ...
    context_window = self._threshold_config.get_context_window_tokens()
    fill_percentage = token_count / context_window
```

`ContextFillEstimator` (application layer) calls ONLY `self._threshold_config.get_context_window_tokens()` -- zero infrastructure imports (H-08 compliant).

> **Note:** If `ContextFillEstimator.__init__` does not already accept `IThresholdConfiguration`, update the constructor:
> ```python
> def __init__(
>     self,
>     reader: ITranscriptReader,
>     threshold_config: IThresholdConfiguration,
> ) -> None:
>     self._reader = reader
>     self._threshold_config = threshold_config
> ```

### Step 4: Update XML output

**AC:** Observability [lines 1-3]

```xml
<context-monitor>
  <fill-percentage>0.72</fill-percentage>
  <tier>WARNING</tier>
  <token-count>144000</token-count>
  <context-window>200000</context-window>
  <context-window-source>default</context-window-source>
  <action>Consider checkpointing...</action>
</context-monitor>
```

Valid values for `<context-window-source>`:
- `config` -- user explicitly configured via env var or config.toml
- `env-1m-detection` -- `ANTHROPIC_MODEL` env var ends with `[1m]`
- `default` -- no configuration or detection; 200K default applied

### Step 5: Wire in bootstrap.py

**AC:** Configuration [line 4]

```python
# In bootstrap.py, where ConfigThresholdAdapter is constructed:
threshold_adapter = ConfigThresholdAdapter(config=layered_config)

# ContextFillEstimator receives the adapter through the port
estimator = ContextFillEstimator(
    reader=transcript_reader,
    threshold_config=threshold_adapter,
)
```

### Step 6: Update calibration protocol

**AC:** Observability [line 4]

Add a "Context Window Configuration" section to `docs/knowledge/context-resilience/calibration-protocol.md`:

| Your Plan | Context Window | Detection Result | Required Action |
|---|---|---|---|
| Pro / Team Standard | 200K | `<context-window-source>default</context-window-source>` | None -- default is correct |
| Max / Team Premium | 200K | `<context-window-source>default</context-window-source>` | None -- default is correct |
| Enterprise | 500K | `<context-window-source>default</context-window-source>` (INCORRECT) | **Set `JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS=500000`** |
| Using `sonnet[1m]` / `opus[1m]` | 1M | `<context-window-source>env-1m-detection</context-window-source>` | None -- auto-detected |
| Custom / unsure | Varies | Check `<context-window-source>` in output | Set explicitly if incorrect |

> **Note for Enterprise users:** Auto-detection cannot distinguish Enterprise (500K) from Pro (200K) because the same model aliases are used for both plans. You must explicitly configure your context window size. Check your plan via `/status` in Claude Code.

### Future Extension: Model Lookup Table

When a Claude model ships with a standard context window other than 200K, add a model-to-window lookup table:

```python
# TODO: Add when a model has a non-200K standard window.
# All current Claude models (opus-4-6, sonnet-4-6, haiku-4-5) are 200K standard.
# _MODEL_CONTEXT_WINDOWS: dict[str, int] = {
#     "claude-future-model": 300_000,
# }
```

This is intentionally not shipped now because all current entries would equal the 200K default, making the lookup functionally identical to the default path (YAGNI).

### Caching Behavior

`get_context_window_tokens()` is evaluated on every call to `estimate()`. The value is not cached. This means:
- If a user changes `ANTHROPIC_MODEL` mid-session (unlikely but possible), the new value is picked up on the next hook invocation
- If config changes, the new value applies on next call
- The cost is negligible: one `get_int_optional()` call + one `os.environ.get()` call per invocation

---

## Related Items

- Parent: [EN-008](./EN-008-context-resilience-hardening.md)
- Root cause: `bootstrap.py:585` defines config key but never wires to estimator
- Affects: `ContextFillEstimator`, `ConfigThresholdAdapter`, `IThresholdConfiguration`
- Related: Calibration protocol (`docs/knowledge/context-resilience/calibration-protocol.md`)
- Adversarial review: `orchestration/feat001-impl-20260220-001/impl/adversarial/task-006-review/`

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-20 | pending | Created. Config key exists but disconnected. |
| 2026-02-20 | pending | Revised after research. Context windows vary: 200K (standard), 500K (Enterprise), 1M (extended `[1m]`). Auto-detection possible via `ANTHROPIC_MODEL` env var `[1m]` suffix and transcript model field. `/status` exposes account info. Configuration-first with auto-detection fallback. |
| 2026-02-20 | pending | Revised after C2 adversarial review (S-003 Steelman, S-007 Constitutional AI, S-002 Devil's Advocate, S-014 LLM-as-Judge). Score 0.646 REJECTED. 4 Critical findings addressed: (1) SM-004 contradictory priority orderings consolidated to single canonical 5-step ordering; (2) CC-001 H-08 violation risk eliminated -- all detection in ConfigThresholdAdapter, not estimator; (3) DA-001 "most common cases" claim removed, auto-detection scoped to `[1m]` only, Enterprise requires config; (4) DA-002 SRP concern addressed with architectural decision section + scope reduction (removed lookup table and transcript reading). Major fixes: effort revised 4h→6-8h; `endswith` replaces `in` for `[1m]` detection; estimator-config wiring test added; `__init__` constructor sample added; `context-window-source` values enumerated; calibration table corrected; caching behavior documented. |
