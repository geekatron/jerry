"""
Unit tests for ConfigSource enum value object.

Tests cover:
    - 5-level configuration precedence per ADR-PROJ004-004
    - Priority comparisons
    - Source properties (file-based, volatile)

Test Categories:
    - Happy path: Valid enum values, comparisons
    - Edge cases: Sorting, from_string parsing
"""

from __future__ import annotations

import pytest

from src.configuration.domain.value_objects.config_source import ConfigSource


class TestConfigSourceValues:
    """Tests for ConfigSource enum values."""

    def test_env_has_highest_precedence(self) -> None:
        """ENV has value 1 (highest precedence)."""
        assert ConfigSource.ENV.value == 1

    def test_session_local_has_second_precedence(self) -> None:
        """SESSION_LOCAL has value 2."""
        assert ConfigSource.SESSION_LOCAL.value == 2

    def test_project_has_third_precedence(self) -> None:
        """PROJECT has value 3."""
        assert ConfigSource.PROJECT.value == 3

    def test_framework_has_fourth_precedence(self) -> None:
        """FRAMEWORK has value 4."""
        assert ConfigSource.FRAMEWORK.value == 4

    def test_default_has_lowest_precedence(self) -> None:
        """DEFAULT has value 5 (lowest precedence)."""
        assert ConfigSource.DEFAULT.value == 5

    def test_all_five_sources_exist(self) -> None:
        """Exactly 5 configuration sources exist."""
        assert len(ConfigSource) == 5


class TestConfigSourcePrecedence:
    """Tests for precedence comparison."""

    def test_env_has_priority_over_session_local(self) -> None:
        """ENV wins over SESSION_LOCAL."""
        assert ConfigSource.ENV.has_priority_over(ConfigSource.SESSION_LOCAL) is True

    def test_env_has_priority_over_default(self) -> None:
        """ENV wins over DEFAULT."""
        assert ConfigSource.ENV.has_priority_over(ConfigSource.DEFAULT) is True

    def test_default_does_not_have_priority_over_framework(self) -> None:
        """DEFAULT loses to FRAMEWORK."""
        assert ConfigSource.DEFAULT.has_priority_over(ConfigSource.FRAMEWORK) is False

    def test_same_source_no_priority(self) -> None:
        """Same source has no priority over itself."""
        assert ConfigSource.PROJECT.has_priority_over(ConfigSource.PROJECT) is False

    def test_project_has_priority_over_framework(self) -> None:
        """PROJECT wins over FRAMEWORK."""
        assert ConfigSource.PROJECT.has_priority_over(ConfigSource.FRAMEWORK) is True

    def test_precedence_matches_value(self) -> None:
        """Precedence property returns the value."""
        assert ConfigSource.ENV.precedence == 1
        assert ConfigSource.DEFAULT.precedence == 5


class TestConfigSourceComparison:
    """Tests for numeric comparison (IntEnum)."""

    def test_env_less_than_project(self) -> None:
        """Lower value = higher precedence."""
        assert ConfigSource.ENV < ConfigSource.PROJECT

    def test_default_greater_than_framework(self) -> None:
        """Higher value = lower precedence."""
        assert ConfigSource.DEFAULT > ConfigSource.FRAMEWORK

    def test_sort_by_precedence(self) -> None:
        """Sources sort by precedence (highest first)."""
        sources = [ConfigSource.DEFAULT, ConfigSource.ENV, ConfigSource.PROJECT]
        sorted_sources = sorted(sources)
        assert sorted_sources == [ConfigSource.ENV, ConfigSource.PROJECT, ConfigSource.DEFAULT]


class TestConfigSourceProperties:
    """Tests for source property accessors."""

    def test_env_not_file_based(self) -> None:
        """ENV is not file-based."""
        assert ConfigSource.ENV.is_file_based is False

    def test_default_not_file_based(self) -> None:
        """DEFAULT is not file-based."""
        assert ConfigSource.DEFAULT.is_file_based is False

    def test_session_local_is_file_based(self) -> None:
        """SESSION_LOCAL is file-based."""
        assert ConfigSource.SESSION_LOCAL.is_file_based is True

    def test_project_is_file_based(self) -> None:
        """PROJECT is file-based."""
        assert ConfigSource.PROJECT.is_file_based is True

    def test_framework_is_file_based(self) -> None:
        """FRAMEWORK is file-based."""
        assert ConfigSource.FRAMEWORK.is_file_based is True

    def test_env_is_volatile(self) -> None:
        """ENV is volatile (can change at runtime)."""
        assert ConfigSource.ENV.is_volatile is True

    def test_session_local_is_volatile(self) -> None:
        """SESSION_LOCAL is volatile."""
        assert ConfigSource.SESSION_LOCAL.is_volatile is True

    def test_project_not_volatile(self) -> None:
        """PROJECT is not volatile."""
        assert ConfigSource.PROJECT.is_volatile is False

    def test_framework_not_volatile(self) -> None:
        """FRAMEWORK is not volatile."""
        assert ConfigSource.FRAMEWORK.is_volatile is False

    def test_default_not_volatile(self) -> None:
        """DEFAULT is not volatile (hardcoded)."""
        assert ConfigSource.DEFAULT.is_volatile is False


class TestConfigSourceDisplayName:
    """Tests for display_name property."""

    def test_env_display_name(self) -> None:
        """ENV displays as 'Env'."""
        assert ConfigSource.ENV.display_name == "Env"

    def test_session_local_display_name(self) -> None:
        """SESSION_LOCAL displays with spaces."""
        assert ConfigSource.SESSION_LOCAL.display_name == "Session Local"

    def test_default_display_name(self) -> None:
        """DEFAULT displays as 'Default'."""
        assert ConfigSource.DEFAULT.display_name == "Default"


class TestConfigSourceDescription:
    """Tests for description property."""

    def test_env_description_mentions_jerry(self) -> None:
        """ENV description mentions JERRY_ prefix."""
        assert "JERRY_" in ConfigSource.ENV.description

    def test_session_local_description_mentions_path(self) -> None:
        """SESSION_LOCAL description mentions file path."""
        assert "local" in ConfigSource.SESSION_LOCAL.description.lower()
        assert "toml" in ConfigSource.SESSION_LOCAL.description

    def test_project_description_mentions_proj(self) -> None:
        """PROJECT description mentions project path."""
        assert "PROJ" in ConfigSource.PROJECT.description

    def test_framework_description_mentions_config(self) -> None:
        """FRAMEWORK description mentions config file."""
        assert "config" in ConfigSource.FRAMEWORK.description.lower()

    def test_default_description_mentions_code(self) -> None:
        """DEFAULT description mentions code defaults."""
        assert "default" in ConfigSource.DEFAULT.description.lower()


class TestConfigSourceFromString:
    """Tests for from_string class method."""

    def test_from_string_lowercase(self) -> None:
        """Parse lowercase string."""
        assert ConfigSource.from_string("env") == ConfigSource.ENV

    def test_from_string_uppercase(self) -> None:
        """Parse uppercase string."""
        assert ConfigSource.from_string("PROJECT") == ConfigSource.PROJECT

    def test_from_string_mixed_case(self) -> None:
        """Parse mixed case string."""
        assert ConfigSource.from_string("Default") == ConfigSource.DEFAULT

    def test_from_string_with_spaces(self) -> None:
        """Parse string with whitespace."""
        assert ConfigSource.from_string("  env  ") == ConfigSource.ENV

    def test_from_string_with_hyphens(self) -> None:
        """Parse string with hyphens."""
        assert ConfigSource.from_string("session-local") == ConfigSource.SESSION_LOCAL

    def test_from_string_with_spaces_in_name(self) -> None:
        """Parse string with spaces instead of underscores."""
        assert ConfigSource.from_string("session local") == ConfigSource.SESSION_LOCAL

    def test_from_string_invalid_raises(self) -> None:
        """Invalid string raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            ConfigSource.from_string("invalid")
        assert "Invalid configuration source" in str(exc_info.value)

    def test_from_string_empty_raises(self) -> None:
        """Empty string raises ValueError (KeyError on empty name)."""
        with pytest.raises(ValueError):
            ConfigSource.from_string("")


class TestConfigSourceStringRepresentation:
    """Tests for string representations."""

    def test_str_returns_lowercase_name(self) -> None:
        """str() returns lowercase name."""
        assert str(ConfigSource.ENV) == "env"
        assert str(ConfigSource.SESSION_LOCAL) == "session_local"

    def test_repr_includes_class_name(self) -> None:
        """repr() includes class name."""
        assert repr(ConfigSource.ENV) == "ConfigSource.ENV"
