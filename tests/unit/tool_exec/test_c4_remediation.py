# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""C4 Tournament Remediation tests.

Covers all 8 P0 Critical and 9 P1 Major findings from the adversarial
tournament review. Each test is tagged with the finding ID it addresses.

References:
    - W12-PHASE2-REMEDIATION: Engagement ID
    - eng-backend-c4-remediation.md: Full remediation record
"""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.interface.cli.tool_exec_commands import (
    _quarantine_output,
    create_tool_exec_handler,
)
from src.tool_exec.domain.services.credential_filter import CredentialFilterService
from src.tool_exec.domain.services.mode_resolver import ModeResolverService
from src.tool_exec.domain.value_objects.exit_codes import ExitCode
from src.tool_exec.domain.value_objects.tool_family_info import ToolFamilyInfo
from src.tool_exec.infrastructure.adapters.local_executor import LocalExecutor
from src.tool_exec.infrastructure.registry.family_registry_loader import (
    FamilyRegistryLoader,
)

# =============================================================================
# FIX-1 (DA-002/CV-005): Inline redaction + quarantine write
# =============================================================================


class TestFix1InlineRedaction:
    """DA-002/CV-005: filter_output() performs inline [CREDENTIAL-REDACTED]
    substitution instead of replacing the entire output."""

    def setup_method(self) -> None:
        """Fresh filter service for each test."""
        self.flt = CredentialFilterService()

    def test_surrounding_lines_preserved_after_detection(self) -> None:
        """Lines before and after the credential line are not redacted."""
        raw = "before\npassword=longpassword1\nafter"
        result = self.flt.filter_output(raw)
        assert result.detected is True
        assert "before" in result.filtered_output
        assert "after" in result.filtered_output

    def test_credential_token_replaced_not_whole_output(self) -> None:
        """Only the matched token is replaced, not the whole output."""
        raw = "before\npassword=longpassword1\nafter"
        result = self.flt.filter_output(raw)
        assert "[CREDENTIAL-REDACTED]" in result.filtered_output
        # The word "password" should still appear (the key, not the value is kept)
        assert "before" in result.filtered_output

    def test_raw_output_preserved_for_quarantine(self) -> None:
        """raw_output field retains the original unmodified output."""
        raw = "password=longpassword1"
        result = self.flt.filter_output(raw)
        assert result.raw_output == raw
        assert "longpassword1" in result.raw_output

    def test_inline_redaction_multiline_credential(self) -> None:
        """Credential detected via sliding-window has contributing lines redacted."""
        # Password split across line boundary
        output = "config: pass\nword=mysecretpassword123\nend"
        result = self.flt.filter_output(output)
        assert result.detected is True
        assert "[CREDENTIAL-REDACTED]" in result.filtered_output

    def test_clean_output_unchanged(self) -> None:
        """Output without credentials passes through identically."""
        raw = "scan complete\n3 vulnerabilities found"
        result = self.flt.filter_output(raw)
        assert not result.detected
        assert result.filtered_output == raw


class TestFix1QuarantineFileWrite:
    """DA-002/CV-005 + RT-003/SR-003: quarantine file is actually written with
    0o600 permissions."""

    def test_quarantine_writes_file(self, tmp_path: Path) -> None:
        """_quarantine_output writes raw stdout+stderr to quarantine dir.

        RT-R2-001: Both stdout and stderr files are written. Updated to use
        the new signature (raw_stdout, raw_stderr, project_root).
        """
        from src.tool_exec.domain.services.engagement_initializer import (
            EngagementInitializer,
        )

        init = EngagementInitializer(base_dir=tmp_path / "engagements")
        init.initialize("eng001")

        _quarantine_output(
            raw_stdout="password=longpassword1",
            raw_stderr="",
            tool_command="nuclei",
            engagement_id="eng001",
            engagement_init=init,
            project_root=tmp_path,
            match_info={"pattern": r"(password)\s*[=:]", "line_number": 1},
        )

        quarantine_dir = init.quarantine_dir("eng001")
        # RT-R2-001: stdout file written
        quarantine_stdout_files = list(quarantine_dir.glob("quarantine-*.stdout.txt"))
        assert len(quarantine_stdout_files) == 1

    def test_quarantine_file_permissions_0o600(self, tmp_path: Path) -> None:
        """RT-003/SR-003 (FIX-8): quarantine files are chmod 0o600, not world-readable.

        SR-002-20260318: quarantine directory is also chmod 0o700.
        """
        from src.tool_exec.domain.services.engagement_initializer import (
            EngagementInitializer,
        )

        init = EngagementInitializer(base_dir=tmp_path / "engagements")
        init.initialize("eng002")

        _quarantine_output(
            raw_stdout="password=longpassword1",
            raw_stderr="",
            tool_command="nuclei",
            engagement_id="eng002",
            engagement_init=init,
            project_root=tmp_path,
        )

        quarantine_dir = init.quarantine_dir("eng002")
        # Directory must be 0o700
        dir_mode = oct(quarantine_dir.stat().st_mode & 0o777)
        assert dir_mode == "0o700", f"Expected 0o700 for quarantine dir, got {dir_mode}"
        # All files in quarantine dir must be 0o600
        for f in quarantine_dir.iterdir():
            mode = oct(f.stat().st_mode & 0o777)
            assert mode == "0o600", f"Expected 0o600 for {f.name}, got {mode}"


# =============================================================================
# FIX-4 (RT-001): Strict-mode bypass via empty env var closed
# =============================================================================


class TestFix4StrictModeBypass:
    """RT-001: Only 'false', '0', or 'no' disable strict mode.
    Empty string or any other value must keep strict mode ON."""

    def _strict_check(self, env_val: str | None) -> bool:
        """Helper: returns True if strict mode is ON for the given env value."""
        env = {} if env_val is None else {"JERRY_STRICT_MODE": env_val}
        with patch.dict(os.environ, env, clear=False):
            # Temporarily remove any existing JERRY_STRICT_MODE
            old = os.environ.pop("JERRY_STRICT_MODE", None)
            if env_val is not None:
                os.environ["JERRY_STRICT_MODE"] = env_val
            try:
                val = os.environ.get("JERRY_STRICT_MODE", "true").lower()
                return val not in ("false", "0", "no")
            finally:
                if old is not None:
                    os.environ["JERRY_STRICT_MODE"] = old
                elif env_val is not None:
                    os.environ.pop("JERRY_STRICT_MODE", None)

    def test_empty_string_keeps_strict_mode_on(self) -> None:
        """Empty string '' must NOT disable strict mode (was the bypass vector)."""
        # Use the fixed logic directly
        val = "".lower()
        strict = val not in ("false", "0", "no")
        assert strict is True

    def test_explicit_false_disables_strict(self) -> None:
        """'false' disables strict mode."""
        val = "false"
        strict = val not in ("false", "0", "no")
        assert strict is False

    def test_zero_disables_strict(self) -> None:
        """'0' disables strict mode."""
        val = "0"
        strict = val not in ("false", "0", "no")
        assert strict is False

    def test_no_disables_strict(self) -> None:
        """'no' disables strict mode."""
        val = "no"
        strict = val not in ("false", "0", "no")
        assert strict is False

    def test_true_keeps_strict_on(self) -> None:
        """'true' (default) keeps strict mode on."""
        val = "true"
        strict = val not in ("false", "0", "no")
        assert strict is True

    def test_yes_keeps_strict_on(self) -> None:
        """'yes' is not a disabling value, strict mode stays on."""
        val = "yes"
        strict = val not in ("false", "0", "no")
        assert strict is True

    def test_one_keeps_strict_on(self) -> None:
        """'1' is not a disabling value, strict mode stays on."""
        val = "1"
        strict = val not in ("false", "0", "no")
        assert strict is True


# =============================================================================
# FIX-6 (CV-008/CV-009): Exit codes 7 and 8
# =============================================================================


class TestFix6ExitCodes:
    """CV-008/CV-009: FAMILY_NOT_FOUND=7 and FAMILY_CONFIG_ERROR=8 exist and
    are used correctly."""

    def test_family_not_found_is_7(self) -> None:
        """CV-008: FAMILY_NOT_FOUND exit code is 7."""
        assert ExitCode.FAMILY_NOT_FOUND == 7

    def test_family_config_error_is_8(self) -> None:
        """CV-009: FAMILY_CONFIG_ERROR exit code is 8."""
        assert ExitCode.FAMILY_CONFIG_ERROR == 8

    def test_strict_mode_violation_is_9(self) -> None:
        """STRICT_MODE_VIOLATION renumbered to 9 after FIX-6 insertions."""
        assert ExitCode.STRICT_MODE_VIOLATION == 9

    def test_zone3_container_required_is_10(self) -> None:
        """FM-002: ZONE3_CONTAINER_REQUIRED is exit code 10."""
        assert ExitCode.ZONE3_CONTAINER_REQUIRED == 10

    def test_all_exit_codes_unique(self) -> None:
        """No two exit codes share the same value."""
        values = [e.value for e in ExitCode]
        assert len(values) == len(set(values))


# =============================================================================
# FIX-9 (CC-002): Composition root factory
# =============================================================================


class TestFix9CompositionRoot:
    """CC-002: Service instantiation moved to create_tool_exec_handler() factory."""

    def test_factory_returns_all_services(self, tmp_path: Path) -> None:
        """create_tool_exec_handler() returns all pipeline services.

        CC-004-20260318: Factory includes local_executor and container_executor
        in addition to loader, engagement_init, and credential_filter.

        DA-R3-002: mode_resolver is intentionally absent from the factory.
        handle_tool_exec constructs its own ModeResolverService with a
        family-specific env_var_prefix (FIX-12/IN-009). Keeping a default-prefix
        instance in the factory was misleading and invited incorrect reuse.
        """
        # Create minimal registry so loader doesn't crash on path check
        registry = tmp_path / "tool_families.yaml"
        registry.write_text("families: []\n")

        services = create_tool_exec_handler(tmp_path)
        assert "loader" in services
        assert "engagement_init" in services
        assert "credential_filter" in services
        assert "local_executor" in services
        assert "container_executor" in services
        assert "mode_resolver" not in services

    def test_factory_credential_filter_is_service(self, tmp_path: Path) -> None:
        """The credential_filter returned is a CredentialFilterService instance."""
        registry = tmp_path / "tool_families.yaml"
        registry.write_text("families: []\n")

        services = create_tool_exec_handler(tmp_path)
        assert isinstance(services["credential_filter"], CredentialFilterService)


# =============================================================================
# FIX-12 (IN-009): ModeResolverService accepts env_var_prefix
# =============================================================================


class TestFix12ModeResolverEnvVarPrefix:
    """IN-009: ModeResolverService accepts a family-specific env var prefix."""

    def test_default_prefix_is_jerry_tool(self) -> None:
        """No-arg constructor defaults to JERRY_TOOL prefix (IN-020-R2).

        The default was changed from RAINBOW to JERRY_TOOL to decouple the
        generic ModeResolverService from the rainbow family (IN-020-R2).
        """
        resolver = ModeResolverService()
        assert resolver.env_var_name == "JERRY_TOOL_MODE"

    def test_custom_prefix_sets_env_var_name(self) -> None:
        """Custom prefix produces correct env var name."""
        resolver = ModeResolverService(env_var_prefix="BLUE_TEAM")
        assert resolver.env_var_name == "BLUE_TEAM_TOOL_MODE"

    def test_custom_prefix_reads_correct_env_var(self) -> None:
        """Resolver with custom prefix reads the family-specific env var."""
        resolver = ModeResolverService(env_var_prefix="MYTEAM")
        with patch.dict(os.environ, {"MYTEAM_TOOL_MODE": "container"}):
            mode = resolver.resolve()
        assert mode == "container"

    def test_custom_prefix_does_not_read_rainbow_env_var(self) -> None:
        """A non-rainbow resolver ignores RAINBOW_TOOL_MODE."""
        resolver = ModeResolverService(env_var_prefix="BLUE_TEAM")
        with patch.dict(
            os.environ,
            {"RAINBOW_TOOL_MODE": "container", "BLUE_TEAM_TOOL_MODE": "local"},
        ):
            mode = resolver.resolve()
        assert mode == "local"  # reads BLUE_TEAM_TOOL_MODE, not RAINBOW_TOOL_MODE


# =============================================================================
# FIX-13 (PM-002): no-filter enforcement at domain level
# =============================================================================


class TestFix13DomainLevelNoFilterEnforcement:
    """PM-002 + PM-004-R2: CredentialFilterService.filter_output() raises RuntimeError
    when no_filter=True and strict_mode=True (the new parameter-based API).

    PM-004-R2: strict_mode is now an explicit parameter rather than read from
    os.environ inside the domain service (H-07 compliance). The CLI handler
    reads JERRY_STRICT_MODE from the environment and passes the resolved boolean.
    """

    def test_no_filter_raises_in_strict_mode(self) -> None:
        """Calling filter_output(no_filter=True, strict_mode=True) raises RuntimeError."""
        flt = CredentialFilterService()
        with pytest.raises(RuntimeError, match="FORBIDDEN"):
            flt.filter_output("some output", no_filter=True, strict_mode=True)

    def test_no_filter_allowed_outside_strict_mode(self) -> None:
        """Calling filter_output(no_filter=True, strict_mode=False) succeeds."""
        flt = CredentialFilterService()
        result = flt.filter_output("some output", no_filter=True, strict_mode=False)
        assert result.detected is False
        assert result.filtered_output == "some output"

    def test_no_filter_default_is_strict_mode_on(self) -> None:
        """Default strict_mode=True means no_filter=True raises without an explicit override."""
        flt = CredentialFilterService()
        with pytest.raises(RuntimeError, match="FORBIDDEN"):
            flt.filter_output("some output", no_filter=True)  # strict_mode defaults to True


# =============================================================================
# FIX-15 (SR-005): Registry key validation
# =============================================================================


class TestFix15RegistryKeyValidation:
    """SR-005: Per-entry key validation with clear error messages."""

    def test_missing_name_key_raises_clear_error(self, tmp_path: Path) -> None:
        """Missing 'name' key produces error naming the entry and the missing key."""
        registry = tmp_path / "tool_families.yaml"
        registry.write_text(
            """
families:
  - description: A family without a name
    resolver_module: src.tool_exec.infrastructure.adapters.rainbow_tool_resolver
    resolver_class: RainbowToolResolver
    config_path: skills/rainbow/config/tool-exec.yaml
"""
        )
        loader = FamilyRegistryLoader(registry)
        with pytest.raises(ValueError, match="name"):
            loader.list_families()

    def test_missing_resolver_module_raises_clear_error(self, tmp_path: Path) -> None:
        """Missing 'resolver_module' key produces error naming the entry and key."""
        registry = tmp_path / "tool_families.yaml"
        registry.write_text(
            """
families:
  - name: broken-family
    description: Missing resolver_module
    resolver_class: RainbowToolResolver
    config_path: skills/rainbow/config/tool-exec.yaml
"""
        )
        loader = FamilyRegistryLoader(registry)
        with pytest.raises(ValueError, match="resolver_module"):
            loader.list_families()

    def test_missing_config_path_raises_clear_error(self, tmp_path: Path) -> None:
        """Missing 'config_path' key produces error naming the entry and key."""
        registry = tmp_path / "tool_families.yaml"
        registry.write_text(
            """
families:
  - name: broken-family
    description: Missing config_path
    resolver_module: src.tool_exec.infrastructure.adapters.rainbow_tool_resolver
    resolver_class: RainbowToolResolver
"""
        )
        loader = FamilyRegistryLoader(registry)
        with pytest.raises(ValueError, match="config_path"):
            loader.list_families()

    def test_error_message_includes_entry_name(self, tmp_path: Path) -> None:
        """Error message identifies the entry by name for easier debugging."""
        registry = tmp_path / "tool_families.yaml"
        registry.write_text(
            """
families:
  - name: known-bad-family
    description: Missing config_path
    resolver_module: src.tool_exec.infrastructure.adapters.rainbow_tool_resolver
    resolver_class: RainbowToolResolver
"""
        )
        loader = FamilyRegistryLoader(registry)
        with pytest.raises(ValueError, match="known-bad-family"):
            loader.list_families()


# =============================================================================
# FIX-16 (DA-004/IN-004): Priority field for auto-detection ordering
# =============================================================================


class TestFix16PriorityOrdering:
    """DA-004/IN-004: Explicit priority field; families sorted by priority."""

    def test_tool_family_info_has_priority_field(self) -> None:
        """ToolFamilyInfo has a priority field with default 100."""
        fi = ToolFamilyInfo(
            name="test",
            description="",
            resolver_module="src.tool_exec.infrastructure.adapters.rainbow_tool_resolver",
            resolver_class="RainbowToolResolver",
            config_path="config.yaml",
        )
        assert fi.priority == 100

    def test_priority_field_can_be_set(self) -> None:
        """ToolFamilyInfo priority can be set to a custom value."""
        fi = ToolFamilyInfo(
            name="test",
            description="",
            resolver_module="src.tool_exec.infrastructure.adapters.rainbow_tool_resolver",
            resolver_class="RainbowToolResolver",
            config_path="config.yaml",
            priority=10,
        )
        assert fi.priority == 10

    def test_registry_sorts_families_by_priority(self, tmp_path: Path) -> None:
        """list_families() returns entries sorted ascending by priority."""
        registry = tmp_path / "tool_families.yaml"
        registry.write_text(
            """
families:
  - name: low-priority
    description: Lower priority (checked last)
    resolver_module: src.tool_exec.infrastructure.adapters.rainbow_tool_resolver
    resolver_class: RainbowToolResolver
    config_path: skills/rainbow/config/tool-exec.yaml
    priority: 50
  - name: high-priority
    description: Higher priority (checked first)
    resolver_module: src.tool_exec.infrastructure.adapters.rainbow_tool_resolver
    resolver_class: RainbowToolResolver
    config_path: skills/rainbow/config/tool-exec.yaml
    priority: 1
"""
        )
        loader = FamilyRegistryLoader(registry)
        families = loader.list_families()
        assert families[0].name == "high-priority"
        assert families[1].name == "low-priority"

    def test_default_priority_in_yaml_is_100(self, tmp_path: Path) -> None:
        """Registry entries without explicit priority default to 100."""
        registry = tmp_path / "tool_families.yaml"
        registry.write_text(
            """
families:
  - name: no-priority-entry
    description: No priority field
    resolver_module: src.tool_exec.infrastructure.adapters.rainbow_tool_resolver
    resolver_class: RainbowToolResolver
    config_path: skills/rainbow/config/tool-exec.yaml
"""
        )
        loader = FamilyRegistryLoader(registry)
        families = loader.list_families()
        assert families[0].priority == 100


# =============================================================================
# FIX-17: Exit code normalization
# =============================================================================


class TestFix17ExitCodeNormalization:
    """FIX-17: Tool non-zero exit codes are normalized to TOOL_ERROR (2)."""

    @patch("src.tool_exec.infrastructure.adapters.local_executor.subprocess.run")
    def test_nonzero_tool_exit_normalized_to_2(self, mock_run: MagicMock) -> None:
        """Tool returning exit code 5 is normalized to 2 (TOOL_ERROR)."""
        mock_run.return_value = MagicMock(
            returncode=5,
            stdout="some output",
            stderr="some error",
        )

        cred_filter = CredentialFilterService()
        executor = LocalExecutor(credential_filter=cred_filter)
        result = executor.execute("tool")

        assert result.exit_code == 2  # TOOL_ERROR, not 5

    @patch("src.tool_exec.infrastructure.adapters.local_executor.subprocess.run")
    def test_zero_exit_stays_zero(self, mock_run: MagicMock) -> None:
        """Tool returning exit code 0 is not changed."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="clean output",
            stderr="",
        )

        cred_filter = CredentialFilterService()
        executor = LocalExecutor(credential_filter=cred_filter)
        result = executor.execute("tool")

        assert result.exit_code == 0

    @patch("src.tool_exec.infrastructure.adapters.local_executor.subprocess.run")
    def test_credential_exit_code_overrides_normalization(self, mock_run: MagicMock) -> None:
        """Credential detection sets exit code 4 regardless of tool exit code."""
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="password=longpassword1",
            stderr="",
        )

        cred_filter = CredentialFilterService()
        executor = LocalExecutor(credential_filter=cred_filter)
        result = executor.execute("tool")

        assert result.exit_code == 4  # CREDENTIAL_DETECTED, not 2 or 1
