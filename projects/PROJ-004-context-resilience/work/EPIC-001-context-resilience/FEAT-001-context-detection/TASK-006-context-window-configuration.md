# TASK-006: Context Window Size Detection and Configuration

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-02-20
> **Due:** --
> **Completed:** --
> **Parent:** EN-008
> **Owner:** --
> **Effort:** 4h

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Description](#description) | What needs to be done |
| [Problem Analysis](#problem-analysis) | Root cause and impact |
| [Research Findings](#research-findings) | Claude Code context window landscape |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
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
1. **Fix the disconnect**: Wire the existing config key to the estimator (the plumbing is half-done)
2. **Add auto-detection**: Read the model from the transcript and infer context window size, with user config as override

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

For users with larger windows (Enterprise 500K, or `[1m]` extended context): thresholds fire **massively too early**, creating unnecessary checkpoints and wasting tokens on false warnings.

---

## Research Findings

### Context Window Sizes by Plan and Model

Source: [Claude Code Model Configuration](https://code.claude.com/docs/en/model-config), [Claude Help Center](https://support.claude.com/en/articles/8606394-how-large-is-the-context-window-on-paid-claude-plans)

| Plan / Mode | Context Window | Model Alias Example |
|---|---|---|
| Pro, Team Standard | 200K | `sonnet`, `opus` |
| Max, Team Premium | 200K | `sonnet`, `opus` |
| Enterprise | 500K | `sonnet`, `opus` |
| Extended context (API/pay-as-you-go) | 1M | `sonnet[1m]`, `opus[1m]` |
| Extended context (subscribers w/ extra usage) | 1M | `sonnet[1m]`, `opus[1m]` |

### Detection Mechanisms Available

| Mechanism | What It Provides | Accessible From Hooks? |
|---|---|---|
| `/status` command | Account info, current model, context usage | No (interactive only) |
| `ANTHROPIC_MODEL` env var | Model alias/name (may include `[1m]`) | Yes |
| Transcript file (`$TRANSCRIPT_PATH`) | Model name in API response `message.model` field | Yes (via backward scan) |
| Model alias `[1m]` suffix | Explicitly encodes 1M context window | Yes (if set via env/config) |
| User configuration | Explicit context window override | Yes (via LayeredConfigAdapter) |

### Auto-Detection Strategy

The **model name** is available in the JSONL transcript. Each API response entry contains `message.model` (e.g., `claude-opus-4-6`, `claude-sonnet-4-6`). Combined with the `[1m]` suffix detection from `ANTHROPIC_MODEL` env var, we can build a reliable model-to-window lookup:

```
Model detection priority:
1. User config override (JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS) → highest
2. ANTHROPIC_MODEL env var with [1m] suffix → 1,000,000
3. Model name from transcript → lookup table
4. Default: 200,000 → lowest
```

The lookup table cannot fully resolve subscription tier (e.g., Enterprise 500K vs Pro 200K on the same model). For these cases, user configuration is the override mechanism. But auto-detection from the model name + `[1m]` suffix handles the most common cases without user action.

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

- [ ] `JsonlTranscriptReader` (or new method) can extract the model name from the latest transcript entry
- [ ] `ANTHROPIC_MODEL` env var is checked for `[1m]` suffix → sets context window to 1,000,000
- [ ] Model-to-window lookup table maps known models to their standard context windows
- [ ] Auto-detected value is used when user has not explicitly configured a value
- [ ] Auto-detection is fail-open: if detection fails, fall back to 200K default

### Observability

- [ ] `<context-monitor>` XML tag includes `<context-window>` field showing the active window size
- [ ] `<context-monitor>` XML tag includes `<context-window-source>` field showing how it was determined (`config`, `env`, `model-detection`, `default`)
- [ ] Calibration protocol (`docs/knowledge/context-resilience/calibration-protocol.md`) updated with configuration instructions per plan

### Tests

- [ ] Unit tests for: explicit config override, env var override, `[1m]` suffix detection, model lookup, default fallback
- [ ] Unit test: XML output includes `<context-window>` and `<context-window-source>`
- [ ] Existing 229 hook tests still pass (no regression)

---

## Implementation Notes

### Step 1: Add port method

In `src/context_monitoring/application/ports/threshold_configuration.py`, add:
```python
def get_context_window_tokens(self) -> int:
    """Get the configured or detected context window size in tokens."""
    ...
```

### Step 2: Implement in ConfigThresholdAdapter

In `src/context_monitoring/infrastructure/adapters/config_threshold_adapter.py`:
```python
_DEFAULT_CONTEXT_WINDOW_TOKENS: int = 200_000

# Known model context windows (standard, without [1m] suffix)
_MODEL_CONTEXT_WINDOWS: dict[str, int] = {
    "claude-opus-4-6": 200_000,
    "claude-sonnet-4-6": 200_000,
    "claude-haiku-4-5": 200_000,
    # Add new models here as they're released
}

_EXTENDED_CONTEXT_WINDOW: int = 1_000_000

def get_context_window_tokens(self) -> int:
    """Get context window size with detection priority.

    Priority: user config > [1m] env detection > model lookup > default 200K.
    """
    # 1. Explicit user config (highest priority)
    key = f"{_CONFIG_NAMESPACE}.context_window_tokens"
    explicit = self._config.get_int_optional(key)
    if explicit is not None:
        return explicit

    # 2. Check ANTHROPIC_MODEL for [1m] suffix
    model_env = os.environ.get("ANTHROPIC_MODEL", "")
    if "[1m]" in model_env:
        return _EXTENDED_CONTEXT_WINDOW

    # 3. Model lookup (if we can determine the model)
    # Model detection from transcript happens at estimator level

    # 4. Default
    return _DEFAULT_CONTEXT_WINDOW_TOKENS
```

### Step 3: Wire into ContextFillEstimator

Remove `_DEFAULT_CONTEXT_WINDOW` constant. Change `estimate()`:
```python
def estimate(self, transcript_path: str) -> FillEstimate:
    # ...
    context_window = self._threshold_config.get_context_window_tokens()
    fill_percentage = token_count / context_window
```

### Step 4: Update XML output

```xml
<context-monitor>
  <fill-percentage>0.72</fill-percentage>
  <tier>WARNING</tier>
  <token-count>144000</token-count>
  <context-window>200000</context-window>
  <context-window-source>config</context-window-source>
  <action>Consider checkpointing...</action>
</context-monitor>
```

### Step 5: Update calibration protocol

Add a "Context Window Configuration" section to `docs/knowledge/context-resilience/calibration-protocol.md`:

| Your Plan | Recommended Setting |
|---|---|
| Pro / Team Standard | 200000 (default, no action needed) |
| Enterprise | `JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS=500000` |
| Using `sonnet[1m]` or `opus[1m]` | Auto-detected, no action needed |
| Custom/unsure | Check `/status` in Claude Code, set explicitly |

### Configuration Precedence

1. `JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS=500000` (env var, highest priority)
2. `[context_monitor] context_window_tokens = 500000` in project `.jerry/config.toml`
3. `[context_monitor] context_window_tokens = 500000` in root `.jerry/config.toml`
4. `ANTHROPIC_MODEL` env var with `[1m]` suffix → 1,000,000
5. Model name lookup table → known model defaults
6. Default: 200,000 (code default, lowest priority)

---

## Related Items

- Parent: [EN-008](./EN-008-context-resilience-hardening.md)
- Root cause: `bootstrap.py:585` defines config key but never wires to estimator
- Affects: `ContextFillEstimator`, `ConfigThresholdAdapter`, `IThresholdConfiguration`, `JsonlTranscriptReader`
- Related: Calibration protocol (`docs/knowledge/context-resilience/calibration-protocol.md`)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-20 | pending | Created. Config key exists but disconnected. |
| 2026-02-20 | pending | Revised after research. Context windows vary: 200K (standard), 500K (Enterprise), 1M (extended `[1m]`). Auto-detection possible via `ANTHROPIC_MODEL` env var `[1m]` suffix and transcript model field. `/status` exposes account info. Configuration-first with auto-detection fallback. |
