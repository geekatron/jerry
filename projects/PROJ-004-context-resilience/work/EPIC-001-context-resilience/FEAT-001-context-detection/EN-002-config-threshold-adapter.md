# EN-002: ConfigThresholdAdapter + IThresholdConfiguration Port

> **Type:** enabler
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-19
> **Due:** --
> **Completed:** 2026-02-21
> **Parent:** FEAT-001
> **Owner:** --
> **Effort:** 1h

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Technical scope |
| [Acceptance Criteria](#acceptance-criteria) | BDD scenarios and checklist |
| [Dependencies](#dependencies) | What this enables |
| [History](#history) | Status changes |

---

## Summary

Add context monitoring threshold defaults to the existing `LayeredConfigAdapter` configuration system and create the bounded context port + adapter bridge. Six configuration keys with defaults. Create `IThresholdConfiguration` protocol in the bounded context application layer and `ConfigThresholdAdapter` in the infrastructure layer as a bridge.

**Technical Scope:**
- 6 config keys: `context_monitor.nominal_threshold` (0.55), `context_monitor.warning_threshold` (0.70), `context_monitor.critical_threshold` (0.80), `context_monitor.emergency_threshold` (0.88), `context_monitor.compaction_detection_threshold` (10000), `context_monitor.enabled` (true)
- New port: `src/context_monitoring/application/ports/threshold_configuration.py` — `IThresholdConfiguration` Protocol
- New adapter: `src/context_monitoring/infrastructure/adapters/config_threshold_adapter.py` — `ConfigThresholdAdapter`
- Wire in `bootstrap.py`

---

## Acceptance Criteria

### BDD Scenarios (pytest-bdd)

```gherkin
Feature: Context monitoring threshold configuration

  Scenario: Default threshold values are available
    Given a fresh Jerry installation with no overrides
    When I run "jerry config get context_monitor.warning_threshold"
    Then the output should be "0.70"

  Scenario: Project-level override takes precedence
    Given a project with context_monitor.warning_threshold set to 0.75
    When I run "jerry config get context_monitor.warning_threshold"
    Then the output should be "0.75"

  Scenario: Environment variable override takes highest precedence
    Given JERRY_CONTEXT_MONITOR_WARNING_THRESHOLD=0.80 in environment
    When I run "jerry config get context_monitor.warning_threshold"
    Then the output should be "0.80"

  Scenario: ConfigThresholdAdapter reads through IThresholdConfiguration port
    Given a ConfigThresholdAdapter wired to LayeredConfigAdapter
    When I call get_threshold("warning")
    Then the result should be 0.70

  Scenario: Context monitoring can be disabled
    Given context_monitor.enabled is set to false
    When I call is_enabled() on IThresholdConfiguration
    Then the result should be False

  Scenario: All six default keys exist
    Given a fresh Jerry installation
    When I query all context_monitor.* keys
    Then nominal_threshold should be 0.55
    And warning_threshold should be 0.70
    And critical_threshold should be 0.80
    And emergency_threshold should be 0.88
    And compaction_detection_threshold should be 10000
    And enabled should be true
```

### Acceptance Checklist

- [ ] All 6 threshold keys have defaults in CLI config adapter
- [ ] `jerry config get context_monitor.warning_threshold` returns `0.70`
- [ ] `jerry config set context_monitor.warning_threshold 0.75 --scope project` persists override
- [ ] Environment variable override works
- [ ] `IThresholdConfiguration` Protocol defined with `get_threshold(tier: str) -> float` and `is_enabled() -> bool` (H-11, H-12)
- [ ] `ConfigThresholdAdapter` implements `IThresholdConfiguration`, delegates to `LayeredConfigAdapter`
- [ ] `bootstrap.py` wires `ConfigThresholdAdapter` as `IThresholdConfiguration` implementation
- [ ] One class per file (H-10)
- [ ] Unit tests: default retrieval, override precedence, `is_enabled()` flag

---

## Dependencies

**Depends On:** Nothing

**Enables:**
- EN-003 (CheckpointService reads `is_enabled()`)
- EN-004 / EN-006 (ContextFillEstimator reads thresholds via port)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-19 | Claude | pending | Enabler created from CWI-01. |
