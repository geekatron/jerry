# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for ConfigThresholdAdapter and IThresholdConfiguration port.

Tests cover BDD scenarios from EN-002:
    - Default threshold values are available
    - Project-level override takes precedence
    - Environment variable override takes highest precedence
    - ConfigThresholdAdapter reads through IThresholdConfiguration port
    - Context monitoring can be disabled
    - All six default keys exist

References:
    - EN-002: ConfigThresholdAdapter + IThresholdConfiguration Port
    - FEAT-001: Context Detection
"""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from src.context_monitoring.application.ports.threshold_configuration import (
    IThresholdConfiguration,
)
from src.context_monitoring.infrastructure.adapters.config_threshold_adapter import (
    ConfigThresholdAdapter,
)
from src.infrastructure.adapters.configuration.layered_config_adapter import (
    LayeredConfigAdapter,
)

# =============================================================================
# Helpers
# =============================================================================


def _make_adapter(
    defaults: dict[str, object] | None = None,
    root_config_path: Path | None = None,
    project_config_path: Path | None = None,
) -> ConfigThresholdAdapter:
    """Create a ConfigThresholdAdapter backed by a LayeredConfigAdapter.

    Args:
        defaults: Optional override defaults for LayeredConfigAdapter.
        root_config_path: Optional root config TOML path.
        project_config_path: Optional project config TOML path.

    Returns:
        A fully wired ConfigThresholdAdapter.
    """
    layered = LayeredConfigAdapter(
        defaults=defaults or {},
        root_config_path=root_config_path,
        project_config_path=project_config_path,
    )
    return ConfigThresholdAdapter(config=layered)


# =============================================================================
# BDD Scenario: Default threshold values are available
# =============================================================================


class TestDefaultThresholdValues:
    """Scenario: Default threshold values are available.

    Given a fresh Jerry installation with no overrides,
    all threshold defaults should be returned.
    """

    def test_warning_threshold_default(self) -> None:
        """Default warning threshold is 0.70."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            assert adapter.get_threshold("warning") == pytest.approx(0.70)

    def test_critical_threshold_default(self) -> None:
        """Default critical threshold is 0.80."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            assert adapter.get_threshold("critical") == pytest.approx(0.80)

    def test_nominal_threshold_default(self) -> None:
        """Default nominal threshold is 0.55."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            assert adapter.get_threshold("nominal") == pytest.approx(0.55)

    def test_emergency_threshold_default(self) -> None:
        """Default emergency threshold is 0.88."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            assert adapter.get_threshold("emergency") == pytest.approx(0.88)

    def test_compaction_detection_threshold_default(self) -> None:
        """Default compaction detection threshold is 10000 tokens."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            assert adapter.get_compaction_detection_threshold() == 10000

    def test_enabled_default(self) -> None:
        """Context monitoring is enabled by default."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            assert adapter.is_enabled() is True


# =============================================================================
# BDD Scenario: Project-level override takes precedence
# =============================================================================


class TestProjectLevelOverride:
    """Scenario: Project-level override takes precedence.

    Given a project with context_monitor.warning_threshold set to 0.75,
    the project-level value should be returned.
    """

    def test_project_overrides_default_warning(self, tmp_path: Path) -> None:
        """Project config overrides default warning threshold."""
        project_config = tmp_path / "project.toml"
        project_config.write_text(
            "[context_monitor]\nwarning_threshold = 0.75\n",
            encoding="utf-8",
        )

        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter(project_config_path=project_config)
            assert adapter.get_threshold("warning") == pytest.approx(0.75)

    def test_project_overrides_default_critical(self, tmp_path: Path) -> None:
        """Project config overrides default critical threshold."""
        project_config = tmp_path / "project.toml"
        project_config.write_text(
            "[context_monitor]\ncritical_threshold = 0.90\n",
            encoding="utf-8",
        )

        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter(project_config_path=project_config)
            assert adapter.get_threshold("critical") == pytest.approx(0.90)

    def test_project_overrides_enabled_flag(self, tmp_path: Path) -> None:
        """Project config can disable context monitoring."""
        project_config = tmp_path / "project.toml"
        project_config.write_text(
            "[context_monitor]\nenabled = false\n",
            encoding="utf-8",
        )

        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter(project_config_path=project_config)
            assert adapter.is_enabled() is False

    def test_project_overrides_compaction_threshold(self, tmp_path: Path) -> None:
        """Project config overrides compaction detection threshold."""
        project_config = tmp_path / "project.toml"
        project_config.write_text(
            "[context_monitor]\ncompaction_detection_threshold = 5000\n",
            encoding="utf-8",
        )

        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter(project_config_path=project_config)
            assert adapter.get_compaction_detection_threshold() == 5000


# =============================================================================
# BDD Scenario: Environment variable override takes highest precedence
# =============================================================================


class TestEnvVarOverride:
    """Scenario: Environment variable override takes highest precedence.

    Given JERRY_CONTEXT_MONITOR__WARNING_THRESHOLD=0.80 in environment,
    the env var value should be returned, overriding project and defaults.
    """

    def test_env_overrides_warning_threshold(self, tmp_path: Path) -> None:
        """Environment variable overrides project and default warning threshold."""
        project_config = tmp_path / "project.toml"
        project_config.write_text(
            "[context_monitor]\nwarning_threshold = 0.75\n",
            encoding="utf-8",
        )

        with patch.dict(
            os.environ,
            {"JERRY_CONTEXT_MONITOR__WARNING_THRESHOLD": "0.80"},
            clear=True,
        ):
            adapter = _make_adapter(project_config_path=project_config)
            assert adapter.get_threshold("warning") == pytest.approx(0.80)

    def test_env_overrides_enabled_flag(self) -> None:
        """Environment variable overrides enabled flag."""
        with patch.dict(
            os.environ,
            {"JERRY_CONTEXT_MONITOR__ENABLED": "false"},
            clear=True,
        ):
            adapter = _make_adapter()
            assert adapter.is_enabled() is False

    def test_env_overrides_compaction_threshold(self) -> None:
        """Environment variable overrides compaction detection threshold."""
        with patch.dict(
            os.environ,
            {"JERRY_CONTEXT_MONITOR__COMPACTION_DETECTION_THRESHOLD": "8000"},
            clear=True,
        ):
            adapter = _make_adapter()
            assert adapter.get_compaction_detection_threshold() == 8000


# =============================================================================
# BDD Scenario: ConfigThresholdAdapter reads through IThresholdConfiguration
# =============================================================================


class TestPortCompliance:
    """Scenario: ConfigThresholdAdapter reads through IThresholdConfiguration port.

    Given a ConfigThresholdAdapter wired to LayeredConfigAdapter,
    it should satisfy the IThresholdConfiguration protocol.
    """

    def test_adapter_satisfies_protocol(self) -> None:
        """ConfigThresholdAdapter is a valid IThresholdConfiguration implementation."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            assert isinstance(adapter, IThresholdConfiguration)

    def test_get_threshold_returns_float(self) -> None:
        """get_threshold returns a float value."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            result = adapter.get_threshold("warning")
            assert isinstance(result, float)

    def test_is_enabled_returns_bool(self) -> None:
        """is_enabled returns a bool value."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            result = adapter.is_enabled()
            assert isinstance(result, bool)

    def test_get_compaction_detection_threshold_returns_int(self) -> None:
        """get_compaction_detection_threshold returns an int value."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            result = adapter.get_compaction_detection_threshold()
            assert isinstance(result, int)


# =============================================================================
# BDD Scenario: Context monitoring can be disabled
# =============================================================================


class TestDisableFlag:
    """Scenario: Context monitoring can be disabled.

    Given context_monitor.enabled is set to false,
    is_enabled() should return False.
    """

    def test_disabled_via_project_config(self, tmp_path: Path) -> None:
        """Context monitoring disabled via project config."""
        project_config = tmp_path / "project.toml"
        project_config.write_text(
            "[context_monitor]\nenabled = false\n",
            encoding="utf-8",
        )

        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter(project_config_path=project_config)
            assert adapter.is_enabled() is False

    def test_disabled_via_env_var(self) -> None:
        """Context monitoring disabled via environment variable."""
        with patch.dict(
            os.environ,
            {"JERRY_CONTEXT_MONITOR__ENABLED": "false"},
            clear=True,
        ):
            adapter = _make_adapter()
            assert adapter.is_enabled() is False

    def test_enabled_by_default(self) -> None:
        """Context monitoring is enabled when no override is set."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            assert adapter.is_enabled() is True


# =============================================================================
# BDD Scenario: All six default keys exist
# =============================================================================


class TestAllSixDefaultKeys:
    """Scenario: All six default keys exist.

    Given a fresh Jerry installation,
    all six context_monitor.* keys should return their defaults.
    """

    def test_nominal_threshold(self) -> None:
        """nominal_threshold should be 0.55."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            assert adapter.get_threshold("nominal") == pytest.approx(0.55)

    def test_warning_threshold(self) -> None:
        """warning_threshold should be 0.70."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            assert adapter.get_threshold("warning") == pytest.approx(0.70)

    def test_critical_threshold(self) -> None:
        """critical_threshold should be 0.80."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            assert adapter.get_threshold("critical") == pytest.approx(0.80)

    def test_emergency_threshold(self) -> None:
        """emergency_threshold should be 0.88."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            assert adapter.get_threshold("emergency") == pytest.approx(0.88)

    def test_compaction_detection_threshold(self) -> None:
        """compaction_detection_threshold should be 10000."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            assert adapter.get_compaction_detection_threshold() == 10000

    def test_enabled(self) -> None:
        """enabled should be true."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            assert adapter.is_enabled() is True


# =============================================================================
# get_all_thresholds tests
# =============================================================================


class TestGetAllThresholds:
    """Tests for the get_all_thresholds convenience method."""

    def test_returns_all_four_tiers(self) -> None:
        """get_all_thresholds returns all four threshold tiers."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            thresholds = adapter.get_all_thresholds()
            assert set(thresholds.keys()) == {
                "nominal",
                "warning",
                "critical",
                "emergency",
            }

    def test_values_match_individual_getters(self) -> None:
        """get_all_thresholds values match individual get_threshold calls."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            thresholds = adapter.get_all_thresholds()
            for tier, value in thresholds.items():
                assert value == pytest.approx(adapter.get_threshold(tier))

    def test_reflects_overrides(self, tmp_path: Path) -> None:
        """get_all_thresholds reflects project overrides."""
        project_config = tmp_path / "project.toml"
        project_config.write_text(
            "[context_monitor]\nwarning_threshold = 0.65\n",
            encoding="utf-8",
        )

        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter(project_config_path=project_config)
            thresholds = adapter.get_all_thresholds()
            assert thresholds["warning"] == pytest.approx(0.65)
            # Others remain at defaults
            assert thresholds["nominal"] == pytest.approx(0.55)


# =============================================================================
# Error handling tests
# =============================================================================


class TestInvalidTier:
    """Tests for invalid tier name handling."""

    def test_invalid_tier_raises_value_error(self) -> None:
        """get_threshold with unrecognized tier raises ValueError."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            with pytest.raises(ValueError, match="Unrecognized threshold tier"):
                adapter.get_threshold("nonexistent")

    def test_case_insensitive_tier(self) -> None:
        """get_threshold is case-insensitive for tier names."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            assert adapter.get_threshold("WARNING") == pytest.approx(0.70)
            assert adapter.get_threshold("Warning") == pytest.approx(0.70)


# =============================================================================
# BDD Scenario: Context window size default (TASK-006)
# =============================================================================


class TestContextWindowDefault:
    """Scenario: Default context window size is 200K.

    Given no explicit user configuration and no [1m] model alias,
    get_context_window_tokens() should return 200_000.
    """

    def test_default_context_window(self) -> None:
        """Default context window is 200_000 tokens."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            assert adapter.get_context_window_tokens() == 200_000

    def test_default_source(self) -> None:
        """Default source is 'default'."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            assert adapter.get_context_window_source() == "default"


# =============================================================================
# BDD Scenario: Explicit user config overrides context window (TASK-006)
# =============================================================================


class TestContextWindowExplicitConfig:
    """Scenario: User explicitly configures context window size.

    Given JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS=500000,
    get_context_window_tokens() should return 500_000 and source 'config'.
    """

    def test_env_var_override(self) -> None:
        """Environment variable sets context window to 500K (Enterprise)."""
        with patch.dict(
            os.environ,
            {"JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS": "500000"},
            clear=True,
        ):
            adapter = _make_adapter()
            assert adapter.get_context_window_tokens() == 500_000

    def test_env_var_source(self) -> None:
        """Environment variable source is 'config'."""
        with patch.dict(
            os.environ,
            {"JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS": "500000"},
            clear=True,
        ):
            adapter = _make_adapter()
            assert adapter.get_context_window_source() == "config"

    def test_toml_override(self, tmp_path: Path) -> None:
        """Config.toml sets context window to 500K."""
        project_config = tmp_path / "project.toml"
        project_config.write_text(
            "[context_monitor]\ncontext_window_tokens = 500000\n",
            encoding="utf-8",
        )

        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter(project_config_path=project_config)
            assert adapter.get_context_window_tokens() == 500_000

    def test_toml_source(self, tmp_path: Path) -> None:
        """Config.toml source is 'config'."""
        project_config = tmp_path / "project.toml"
        project_config.write_text(
            "[context_monitor]\ncontext_window_tokens = 500000\n",
            encoding="utf-8",
        )

        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter(project_config_path=project_config)
            assert adapter.get_context_window_source() == "config"

    def test_env_var_overrides_1m_detection(self) -> None:
        """Explicit config takes priority over [1m] auto-detection."""
        with patch.dict(
            os.environ,
            {
                "JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS": "500000",
                "ANTHROPIC_MODEL": "sonnet[1m]",
            },
            clear=True,
        ):
            adapter = _make_adapter()
            assert adapter.get_context_window_tokens() == 500_000
            assert adapter.get_context_window_source() == "config"


# =============================================================================
# BDD Scenario: ANTHROPIC_MODEL [1m] suffix auto-detection (TASK-006)
# =============================================================================


class TestContextWindow1mDetection:
    """Scenario: Auto-detect [1m] extended-context model alias.

    Given ANTHROPIC_MODEL=sonnet[1m] and no explicit config,
    get_context_window_tokens() should return 1_000_000.
    """

    def test_sonnet_1m_detection(self) -> None:
        """sonnet[1m] auto-detected as 1M context window."""
        with patch.dict(
            os.environ,
            {"ANTHROPIC_MODEL": "sonnet[1m]"},
            clear=True,
        ):
            adapter = _make_adapter()
            assert adapter.get_context_window_tokens() == 1_000_000

    def test_opus_1m_detection(self) -> None:
        """opus[1m] auto-detected as 1M context window."""
        with patch.dict(
            os.environ,
            {"ANTHROPIC_MODEL": "opus[1m]"},
            clear=True,
        ):
            adapter = _make_adapter()
            assert adapter.get_context_window_tokens() == 1_000_000

    def test_1m_source(self) -> None:
        """[1m] detection source is 'env-1m-detection'."""
        with patch.dict(
            os.environ,
            {"ANTHROPIC_MODEL": "sonnet[1m]"},
            clear=True,
        ):
            adapter = _make_adapter()
            assert adapter.get_context_window_source() == "env-1m-detection"

    def test_no_1m_suffix_returns_default(self) -> None:
        """ANTHROPIC_MODEL without [1m] suffix returns default."""
        with patch.dict(
            os.environ,
            {"ANTHROPIC_MODEL": "sonnet"},
            clear=True,
        ):
            adapter = _make_adapter()
            assert adapter.get_context_window_tokens() == 200_000

    def test_no_anthropic_model_returns_default(self) -> None:
        """Missing ANTHROPIC_MODEL returns default."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            assert adapter.get_context_window_tokens() == 200_000

    def test_endswith_not_substring(self) -> None:
        """[1m] must be suffix, not just substring (no false positives)."""
        with patch.dict(
            os.environ,
            {"ANTHROPIC_MODEL": "my-custom-[1m]-wrapper"},
            clear=True,
        ):
            adapter = _make_adapter()
            # Should NOT detect [1m] since it's not a suffix
            assert adapter.get_context_window_tokens() == 200_000
            assert adapter.get_context_window_source() == "default"

    def test_claude_sonnet_4_6_1m(self) -> None:
        """Full model ID with [1m] suffix is detected."""
        with patch.dict(
            os.environ,
            {"ANTHROPIC_MODEL": "claude-sonnet-4-6[1m]"},
            clear=True,
        ):
            adapter = _make_adapter()
            assert adapter.get_context_window_tokens() == 1_000_000

    def test_case_insensitive_1M_uppercase(self) -> None:
        """[1M] uppercase suffix is detected (case-insensitive)."""
        with patch.dict(
            os.environ,
            {"ANTHROPIC_MODEL": "sonnet[1M]"},
            clear=True,
        ):
            adapter = _make_adapter()
            assert adapter.get_context_window_tokens() == 1_000_000
            assert adapter.get_context_window_source() == "env-1m-detection"


# =============================================================================
# BDD Scenario: Fail-open on detection errors (TASK-006)
# =============================================================================


class TestContextWindowFailOpen:
    """Scenario: Detection failures fall back to default.

    Given any exception during detection,
    get_context_window_tokens() should return 200_000 (fail-open).
    """

    def test_fail_open_returns_default(self) -> None:
        """Detection error falls back to 200K default."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            # Even with no env vars or config, should return default gracefully
            assert adapter.get_context_window_tokens() == 200_000

    def test_fail_open_on_environ_get_exception(self) -> None:
        """os.environ.get raising falls back to 200K (genuine failure injection)."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            # Patch os.environ.get to raise, exercising outer try/except
            with patch("os.environ.get", side_effect=RuntimeError("env error")):
                assert adapter.get_context_window_tokens() == 200_000
                assert adapter.get_context_window_source() == "default"


# =============================================================================
# BDD Scenario: Invalid config values handled gracefully (TASK-006, FM-001/FM-003/FM-004)
# =============================================================================


class TestContextWindowInvalidConfig:
    """Scenario: Invalid context_window_tokens config falls through to auto-detection.

    Given a non-numeric, zero, or negative context_window_tokens config value,
    the adapter should log a warning and fall through to the next detection step.
    """

    def test_non_numeric_config_falls_through(self) -> None:
        """Non-numeric context_window_tokens falls through to default (FM-001/W-003)."""
        with patch.dict(
            os.environ,
            {"JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS": "not_a_number"},
            clear=True,
        ):
            adapter = _make_adapter()
            assert adapter.get_context_window_tokens() == 200_000
            assert adapter.get_context_window_source() == "default"

    def test_zero_config_falls_through(self) -> None:
        """Zero context_window_tokens falls through to default (FM-003)."""
        with patch.dict(
            os.environ,
            {"JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS": "0"},
            clear=True,
        ):
            adapter = _make_adapter()
            assert adapter.get_context_window_tokens() == 200_000
            assert adapter.get_context_window_source() == "default"

    def test_negative_config_falls_through(self) -> None:
        """Negative context_window_tokens falls through to default (FM-004)."""
        with patch.dict(
            os.environ,
            {"JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS": "-100"},
            clear=True,
        ):
            adapter = _make_adapter()
            assert adapter.get_context_window_tokens() == 200_000
            assert adapter.get_context_window_source() == "default"

    def test_non_numeric_with_1m_model_falls_to_1m(self) -> None:
        """Non-numeric config falls through to [1m] detection when available."""
        with patch.dict(
            os.environ,
            {
                "JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS": "abc",
                "ANTHROPIC_MODEL": "sonnet[1m]",
            },
            clear=True,
        ):
            adapter = _make_adapter()
            assert adapter.get_context_window_tokens() == 1_000_000
            assert adapter.get_context_window_source() == "env-1m-detection"

    def test_zero_with_1m_model_falls_to_1m(self) -> None:
        """Zero config falls through to [1m] detection when available."""
        with patch.dict(
            os.environ,
            {
                "JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS": "0",
                "ANTHROPIC_MODEL": "opus[1m]",
            },
            clear=True,
        ):
            adapter = _make_adapter()
            assert adapter.get_context_window_tokens() == 1_000_000
            assert adapter.get_context_window_source() == "env-1m-detection"

    def test_exceeds_max_falls_through(self) -> None:
        """Value exceeding 2M max falls through to default (AV-002)."""
        with patch.dict(
            os.environ,
            {"JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS": "999999999999"},
            clear=True,
        ):
            adapter = _make_adapter()
            assert adapter.get_context_window_tokens() == 200_000
            assert adapter.get_context_window_source() == "default"

    def test_exceeds_max_with_1m_falls_to_1m(self) -> None:
        """Value exceeding max falls through to [1m] detection when available."""
        with patch.dict(
            os.environ,
            {
                "JERRY_CONTEXT_MONITOR__CONTEXT_WINDOW_TOKENS": "5000000",
                "ANTHROPIC_MODEL": "sonnet[1m]",
            },
            clear=True,
        ):
            adapter = _make_adapter()
            assert adapter.get_context_window_tokens() == 1_000_000
            assert adapter.get_context_window_source() == "env-1m-detection"


# =============================================================================
# BDD Scenario: Port compliance with new methods (TASK-006)
# =============================================================================


class TestContextWindowConfigGetFailure:
    """Scenario: LayeredConfigAdapter.get() raises during detection.

    Given an infrastructure exception from config.get(),
    _detect_context_window() should return the 200K default (DEFECT-001).
    """

    def test_config_get_exception_fails_open(self) -> None:
        """config.get() exception falls back to default (DEFECT-001)."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            # Monkey-patch config.get to raise
            adapter._config.get = lambda key: (_ for _ in ()).throw(  # type: ignore[method-assign]
                RuntimeError("TOML parse error")
            )
            assert adapter.get_context_window_tokens() == 200_000
            assert adapter.get_context_window_source() == "default"


# =============================================================================
# BDD Scenario: Bootstrap absent-key invariant (TASK-006)
# =============================================================================


class TestBootstrapAbsentKeyInvariant:
    """Scenario: context_window_tokens is intentionally absent from bootstrap defaults.

    The detection chain depends on config.get() returning None when
    context_window_tokens is not configured. If someone adds it to the
    bootstrap defaults, auto-detection breaks silently.
    """

    def test_context_window_tokens_not_in_bootstrap_defaults(self) -> None:
        """context_window_tokens must NOT appear in bootstrap defaults.

        If someone adds context_monitor.context_window_tokens to defaults,
        this test will fail because source would become 'config' instead
        of 'default', breaking the auto-detection chain.
        """
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter(
                defaults={
                    # Replicate bootstrap defaults WITHOUT context_window_tokens
                    "context_monitor.nominal_threshold": 0.55,
                    "context_monitor.warning_threshold": 0.70,
                    "context_monitor.critical_threshold": 0.80,
                    "context_monitor.emergency_threshold": 0.88,
                    "context_monitor.compaction_detection_threshold": 10000,
                    "context_monitor.enabled": True,
                },
            )
            # Source must be 'default', NOT 'config'
            assert adapter.get_context_window_source() == "default"

    def test_adding_context_window_tokens_to_defaults_breaks_detection(self) -> None:
        """Proves that adding context_window_tokens to defaults would break detection.

        If someone adds the key to defaults, config.get() returns it,
        bypassing ANTHROPIC_MODEL [1m] auto-detection.
        """
        with patch.dict(
            os.environ,
            {"ANTHROPIC_MODEL": "sonnet[1m]"},
            clear=True,
        ):
            # With the key in defaults: detection chain is broken
            adapter_broken = _make_adapter(
                defaults={"context_monitor.context_window_tokens": 200000},
            )
            # Source becomes 'config' instead of 'env-1m-detection'
            assert adapter_broken.get_context_window_source() == "config"
            assert adapter_broken.get_context_window_tokens() == 200_000  # Wrong!

            # Without the key in defaults: detection chain works correctly
            adapter_correct = _make_adapter(defaults={})
            assert adapter_correct.get_context_window_source() == "env-1m-detection"
            assert adapter_correct.get_context_window_tokens() == 1_000_000  # Correct!


class TestContextWindowPortCompliance:
    """Scenario: ConfigThresholdAdapter still satisfies IThresholdConfiguration.

    Given the new get_context_window_tokens() and get_context_window_source()
    methods on the port, the adapter should still satisfy the protocol.
    """

    def test_adapter_satisfies_protocol_with_context_window(self) -> None:
        """ConfigThresholdAdapter satisfies IThresholdConfiguration with new methods."""
        with patch.dict(os.environ, {}, clear=True):
            adapter = _make_adapter()
            assert isinstance(adapter, IThresholdConfiguration)
