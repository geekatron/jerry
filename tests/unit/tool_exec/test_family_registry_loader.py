# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for FamilyRegistryLoader.

Security tests include M-01 (T-01, DREAD 38): module path allowlist enforcement.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.tool_exec.infrastructure.registry.family_registry_loader import (
    _ALLOWED_MODULE_PREFIXES,
    _CLASS_NAME_PATTERN,
    FamilyRegistryLoader,
)


class TestFamilyRegistryLoaderParsing:
    """Tests for registry YAML parsing."""

    def test_parse_valid_registry(self, tmp_path: Path) -> None:
        """Valid registry YAML is parsed into ToolFamilyInfo objects."""
        registry = tmp_path / "tool_families.yaml"
        registry.write_text(
            """
families:
  - name: test-family
    description: A test family
    resolver_module: src.tool_exec.infrastructure.adapters.rainbow_tool_resolver
    resolver_class: RainbowToolResolver
    config_path: skills/rainbow/config/tool-exec.yaml
    enabled: true
"""
        )

        loader = FamilyRegistryLoader(registry)
        families = loader.list_families()

        assert len(families) == 1
        assert families[0].name == "test-family"
        assert families[0].description == "A test family"
        assert families[0].enabled is True

    def test_parse_disabled_family(self, tmp_path: Path) -> None:
        """Disabled families are parsed but not loaded."""
        registry = tmp_path / "tool_families.yaml"
        registry.write_text(
            """
families:
  - name: disabled-family
    description: A disabled family
    resolver_module: nonexistent.module
    resolver_class: NonexistentClass
    config_path: nonexistent.yaml
    enabled: false
"""
        )

        loader = FamilyRegistryLoader(registry)
        families = loader.list_families()

        assert len(families) == 1
        assert families[0].enabled is False

    def test_missing_registry_raises(self) -> None:
        """Missing registry file raises FileNotFoundError."""
        loader = FamilyRegistryLoader("/nonexistent/path.yaml")
        with pytest.raises(FileNotFoundError):
            loader.list_families()

    def test_malformed_registry_raises(self, tmp_path: Path) -> None:
        """Registry without 'families' key raises ValueError."""
        registry = tmp_path / "tool_families.yaml"
        registry.write_text("some_key: some_value\n")

        loader = FamilyRegistryLoader(registry)
        with pytest.raises(ValueError, match="families"):
            loader.list_families()


class TestFamilyRegistryLoaderLoading:
    """Tests for dynamic resolver loading."""

    def test_load_real_rainbow_resolver(self) -> None:
        """Load the real rainbow resolver from tool_families.yaml."""
        # Find the repo root
        repo_root = Path(__file__).resolve().parents[3]
        registry_path = repo_root / "tool_families.yaml"
        config_path = repo_root / "skills" / "rainbow" / "config" / "tool-exec.yaml"

        if not registry_path.exists():
            pytest.skip("tool_families.yaml not found")
        if not config_path.exists():
            pytest.skip("tool-exec.yaml not found")

        loader = FamilyRegistryLoader(registry_path)
        resolvers = loader.load()

        assert "rainbow" in resolvers
        assert resolvers["rainbow"].can_resolve("nuclei")

    def test_load_skips_disabled_families(self, tmp_path: Path) -> None:
        """Disabled families are not loaded."""
        registry = tmp_path / "tool_families.yaml"
        registry.write_text(
            """
families:
  - name: disabled-family
    description: Should be skipped
    resolver_module: nonexistent.module
    resolver_class: NonexistentClass
    config_path: nonexistent.yaml
    enabled: false
"""
        )

        loader = FamilyRegistryLoader(registry)
        resolvers = loader.load()

        assert len(resolvers) == 0


class TestFamilyRegistryLoaderModuleAllowlist:
    """Tests for M-01: module path allowlist enforcement (T-01, DREAD 38).

    Verifies that _validate_module_path() rejects arbitrary module paths
    and only accepts paths within the approved src.tool_exec.infrastructure.adapters.
    prefix. This prevents arbitrary code execution if tool_families.yaml is
    compromised (malicious PR, git config injection, developer workstation compromise).
    """

    def setup_method(self, tmp_path: Path | None = None) -> None:
        """Create a loader with a dummy path for unit testing."""
        self.loader = FamilyRegistryLoader("/tmp/dummy.yaml")

    def test_allowed_prefix_passes(self) -> None:
        """Module path within allowed prefix is accepted without error."""
        # Should not raise
        self.loader._validate_module_path(
            "src.tool_exec.infrastructure.adapters.rainbow_tool_resolver"
        )

    def test_allowed_prefix_any_submodule(self) -> None:
        """Any submodule within the allowed prefix passes validation."""
        self.loader._validate_module_path(
            "src.tool_exec.infrastructure.adapters.future_family_resolver"
        )

    def test_disallowed_arbitrary_module_raises(self) -> None:
        """Arbitrary module path outside allowlist raises ValueError (T-01 block)."""
        with pytest.raises(ValueError, match="not in the allowed prefix list"):
            self.loader._validate_module_path("malicious.module.with.exploit_code")

    def test_disallowed_os_module_raises(self) -> None:
        """os module cannot be imported via the registry (supply chain attack prevention)."""
        with pytest.raises(ValueError, match="not in the allowed prefix list"):
            self.loader._validate_module_path("os")

    def test_disallowed_sys_module_raises(self) -> None:
        """sys module cannot be imported via the registry."""
        with pytest.raises(ValueError, match="not in the allowed prefix list"):
            self.loader._validate_module_path("sys")

    def test_disallowed_plausible_typosquat_raises(self) -> None:
        """A plausible typosquat module path (e.g., missing adapters prefix) is rejected."""
        # Attacker might use: src.tool_exec.infrastructure.rainbow_tool_resolver_v2
        # (missing 'adapters.' in path -- looks legitimate but lands outside the gate)
        with pytest.raises(ValueError, match="not in the allowed prefix list"):
            self.loader._validate_module_path(
                "src.tool_exec.infrastructure.rainbow_tool_resolver_v2"
            )

    def test_disallowed_partial_prefix_prefix_match_raises(self) -> None:
        """Prefix match must be exact dotted path, not a substring match."""
        # 'src.tool_exec.infrastructure.adapters' without trailing dot should fail
        # if the module_path itself starts that way but doesn't have the full prefix.
        # The actual allowed prefix includes the trailing dot, so this module path
        # (which equals the prefix without the trailing dot) should be rejected.
        with pytest.raises(ValueError, match="not in the allowed prefix list"):
            self.loader._validate_module_path("src.tool_exec.infrastructure.adapters")

    def test_disallowed_site_packages_module_raises(self) -> None:
        """Installed packages from site-packages cannot be loaded via the registry."""
        with pytest.raises(ValueError, match="not in the allowed prefix list"):
            self.loader._validate_module_path("requests.sessions")

    def test_load_with_disallowed_module_raises_on_enabled_family(self, tmp_path: Path) -> None:
        """load() raises ValueError when an enabled family has a disallowed module path.

        NEW-002 (FM-005): The per-family error is now caught and the family
        is skipped. With only one enabled family and it failing, the loader
        raises 'No family resolvers could be loaded' (the aggregate error).
        The security invariant is preserved: the disallowed module is never
        imported.
        """
        registry = tmp_path / "tool_families.yaml"
        registry.write_text(
            """
families:
  - name: malicious-family
    description: Should be rejected before import
    resolver_module: os.path
    resolver_class: join
    config_path: nonexistent.yaml
    enabled: true
"""
        )
        loader = FamilyRegistryLoader(registry)
        with pytest.raises(ValueError, match="No family resolvers could be loaded"):
            loader.load()

    def test_allowed_module_prefixes_constant_is_correct(self) -> None:
        """The allowlist constant contains only the infrastructure.adapters prefix."""
        assert len(_ALLOWED_MODULE_PREFIXES) >= 1
        assert all("infrastructure.adapters" in prefix for prefix in _ALLOWED_MODULE_PREFIXES)


class TestFamilyRegistryLoaderClassNameValidation:
    """Tests for FINDING-003 (CWE-94): resolver_class name validation.

    Verifies that _validate_class_name() rejects non-CamelCase strings before
    getattr() is called. This closes the gap where the module path allowlist (M-01)
    guarded the import but left the class attribute access unconstrained -- allowing
    a tampered tool_families.yaml to access __builtins__, imported submodules, or
    any other module-level attribute via getattr().
    """

    def setup_method(self, tmp_path: Path | None = None) -> None:
        """Create a loader with a dummy path for unit testing."""
        self.loader = FamilyRegistryLoader("/tmp/dummy.yaml")

    def test_valid_camelcase_name_passes(self) -> None:
        """CamelCase class name within the 2-64 char range is accepted."""
        self.loader._validate_class_name("RainbowToolResolver")

    def test_valid_two_char_name_passes(self) -> None:
        """Minimum-length (2-char) class name is accepted."""
        self.loader._validate_class_name("Ab")

    def test_valid_64_char_name_passes(self) -> None:
        """Maximum-length (64-char) class name is accepted."""
        name = "A" + "b" * 63
        self.loader._validate_class_name(name)

    def test_lowercase_start_rejected(self) -> None:
        """Class name starting with lowercase letter is rejected (FINDING-003)."""
        with pytest.raises(ValueError, match="invalid"):
            self.loader._validate_class_name("rainbowToolResolver")

    def test_dunder_attribute_rejected(self) -> None:
        """Dunder attribute name is rejected (FINDING-003 -- prevents __builtins__ access)."""
        with pytest.raises(ValueError, match="invalid"):
            self.loader._validate_class_name("__builtins__")

    def test_module_level_import_name_rejected(self) -> None:
        """Lowercase module import name (subprocess) is rejected (FINDING-003)."""
        with pytest.raises(ValueError, match="invalid"):
            self.loader._validate_class_name("subprocess")

    def test_dotted_name_rejected(self) -> None:
        """Dotted attribute path is rejected -- only simple identifiers allowed."""
        with pytest.raises(ValueError, match="invalid"):
            self.loader._validate_class_name("os.system")

    def test_empty_name_rejected(self) -> None:
        """Empty class name is rejected."""
        with pytest.raises(ValueError, match="invalid"):
            self.loader._validate_class_name("")

    def test_single_char_name_rejected(self) -> None:
        """Single-character class name (below 2-char minimum) is rejected."""
        with pytest.raises(ValueError, match="invalid"):
            self.loader._validate_class_name("A")

    def test_65_char_name_rejected(self) -> None:
        """65-character class name (above 64-char maximum) is rejected."""
        name = "A" + "b" * 64  # 65 chars total
        with pytest.raises(ValueError, match="invalid"):
            self.loader._validate_class_name(name)

    def test_name_with_underscore_rejected(self) -> None:
        """Class name containing underscore is rejected (pattern requires alphanum only)."""
        with pytest.raises(ValueError, match="invalid"):
            self.loader._validate_class_name("Rainbow_Resolver")

    def test_class_name_pattern_constant_is_correct(self) -> None:
        """The class name pattern constant enforces CamelCase 2-64 char constraint."""
        assert _CLASS_NAME_PATTERN.match("RainbowToolResolver") is not None
        assert _CLASS_NAME_PATTERN.match("__builtins__") is None
        assert _CLASS_NAME_PATTERN.match("subprocess") is None
        assert _CLASS_NAME_PATTERN.match("A") is None

    def test_load_with_invalid_class_name_raises(self, tmp_path: Path) -> None:
        """load() raises ValueError when resolver_class is not a valid CamelCase name.

        NEW-002 (FM-005): Per-family errors are caught and the family is skipped.
        With only one enabled family failing, the aggregate 'No family resolvers
        could be loaded' error is raised. The security invariant (no getattr on
        invalid names) is preserved.
        """
        registry = tmp_path / "tool_families.yaml"
        registry.write_text(
            """
families:
  - name: bad-class-family
    description: Should be rejected by class name validation
    resolver_module: src.tool_exec.infrastructure.adapters.rainbow_tool_resolver
    resolver_class: __builtins__
    config_path: skills/rainbow/config/tool-exec.yaml
    enabled: true
"""
        )
        loader = FamilyRegistryLoader(registry)
        with pytest.raises(ValueError, match="No family resolvers could be loaded"):
            loader.load()

    def test_load_with_lowercase_class_name_raises(self, tmp_path: Path) -> None:
        """load() raises ValueError when resolver_class starts with lowercase.

        NEW-002 (FM-005): Per-family errors are caught and the family is skipped.
        With only one enabled family failing, the aggregate error is raised.
        """
        registry = tmp_path / "tool_families.yaml"
        registry.write_text(
            """
families:
  - name: lowercase-class-family
    description: Should be rejected by class name validation
    resolver_module: src.tool_exec.infrastructure.adapters.rainbow_tool_resolver
    resolver_class: subprocess
    config_path: skills/rainbow/config/tool-exec.yaml
    enabled: true
"""
        )
        loader = FamilyRegistryLoader(registry)
        with pytest.raises(ValueError, match="No family resolvers could be loaded"):
            loader.load()
