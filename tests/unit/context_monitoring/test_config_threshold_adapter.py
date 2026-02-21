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
