# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Contract tests for plugin manifest JSON schema validation.

These tests verify that plugin manifests conform to their JSON schemas
and that the validation script correctly validates all manifest files.

Contract Reference:
    - EN-001: Add keywords field to marketplace.schema.json (TASK-002)
    - DEC-002: Schema Validation Approach
    - schemas/marketplace.schema.json
    - schemas/plugin.schema.json
    - schemas/hooks.schema.json

Test Distribution per testing-standards.md:
    - Contract tests: 5% of total coverage
    - Focus: External interface compliance (JSON Schema validation)

References:
    - TASK-002: Add tests for plugin manifest validation
    - Phase 2: Parallel Improvements
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    pass

try:
    import jsonschema
except ImportError:
    pytest.skip("jsonschema package not installed", allow_module_level=True)


# Mark as contract tests
pytestmark = [
    pytest.mark.contract,
]


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def project_root() -> Path:
    """Get the project root directory."""
    # Navigate from tests/contract to project root
    return Path(__file__).parent.parent.parent


@pytest.fixture
def marketplace_schema_path(project_root: Path) -> Path:
    """Get the path to marketplace.schema.json."""
    return project_root / "schemas" / "marketplace.schema.json"


@pytest.fixture
def marketplace_schema(marketplace_schema_path: Path) -> dict:
    """Load the marketplace JSON schema."""
    return json.loads(marketplace_schema_path.read_text())


@pytest.fixture
def validation_script_path(project_root: Path) -> Path:
    """Get the path to the validation script."""
    return project_root / "scripts" / "validate_plugin_manifests.py"


# =============================================================================
# Test: Keywords field is accepted in marketplace plugin items
# =============================================================================


class TestMarketplaceSchemaKeywordsField:
    """Contract: marketplace.schema.json must accept keywords field in plugin items."""

    def test_marketplace_json_with_keywords_passes_validation(
        self,
        marketplace_schema: dict,
    ) -> None:
        """Test that keywords field is accepted in marketplace plugin items.

        Contract: Per TASK-001, the marketplace.schema.json MUST accept
        a keywords array in plugin items.

        Acceptance Criteria:
        - keywords field is optional
        - keywords must be an array of strings
        - Each keyword must match pattern ^[a-z0-9-]+$
        - Maximum 20 keywords allowed
        - Keywords must be unique
        """
        # Arrange - create a valid marketplace manifest with keywords
        valid_marketplace = {
            "name": "test-marketplace",
            "plugins": [
                {
                    "name": "test-plugin",
                    "source": "./test",
                    "keywords": [
                        "problem-solving",
                        "work-tracking",
                        "agents",
                        "workflows",
                    ],
                }
            ],
        }

        # Act & Assert - should validate without errors
        try:
            jsonschema.validate(valid_marketplace, marketplace_schema)
        except jsonschema.ValidationError as e:
            pytest.fail(
                f"Validation failed for manifest with keywords.\n"
                f"Error: {e.message}\n"
                f"Schema path: {list(e.absolute_schema_path)}\n"
                f"Instance path: {list(e.absolute_path)}"
            )

    def test_marketplace_json_without_keywords_passes_validation(
        self,
        marketplace_schema: dict,
    ) -> None:
        """Test that keywords field is optional.

        Contract: Plugins without keywords field should still validate.
        """
        # Arrange - valid marketplace without keywords
        valid_marketplace = {
            "name": "test-marketplace",
            "plugins": [
                {
                    "name": "test-plugin",
                    "source": "./test",
                }
            ],
        }

        # Act & Assert - should validate without errors
        try:
            jsonschema.validate(valid_marketplace, marketplace_schema)
        except jsonschema.ValidationError as e:
            pytest.fail(f"Validation failed for manifest without keywords.\nError: {e.message}")

    def test_marketplace_json_with_invalid_keyword_format_fails_validation(
        self,
        marketplace_schema: dict,
    ) -> None:
        """Test that keywords must match the required pattern.

        Contract: Keywords must be lowercase alphanumeric with hyphens only.
        Invalid patterns should be rejected.
        """
        # Arrange - invalid keyword with uppercase
        invalid_marketplace = {
            "name": "test-marketplace",
            "plugins": [
                {
                    "name": "test-plugin",
                    "source": "./test",
                    "keywords": ["Invalid-Keyword"],  # Uppercase not allowed
                }
            ],
        }

        # Act & Assert - should raise ValidationError
        with pytest.raises(jsonschema.ValidationError) as exc_info:
            jsonschema.validate(invalid_marketplace, marketplace_schema)

        # Verify the error is about the keyword pattern
        assert (
            "pattern" in str(exc_info.value).lower()
            or "does not match" in str(exc_info.value).lower()
        )

    def test_marketplace_json_with_too_many_keywords_fails_validation(
        self,
        marketplace_schema: dict,
    ) -> None:
        """Test that keywords array has maximum limit.

        Contract: Maximum 20 keywords allowed per plugin.
        """
        # Arrange - 21 keywords (exceeds limit)
        invalid_marketplace = {
            "name": "test-marketplace",
            "plugins": [
                {
                    "name": "test-plugin",
                    "source": "./test",
                    "keywords": [f"keyword-{i}" for i in range(21)],
                }
            ],
        }

        # Act & Assert - should raise ValidationError
        with pytest.raises(jsonschema.ValidationError) as exc_info:
            jsonschema.validate(invalid_marketplace, marketplace_schema)

        # Verify the error is about maxItems
        assert (
            "maxitems" in str(exc_info.value).lower() or "too long" in str(exc_info.value).lower()
        )

    def test_marketplace_json_with_duplicate_keywords_fails_validation(
        self,
        marketplace_schema: dict,
    ) -> None:
        """Test that keywords must be unique.

        Contract: uniqueItems constraint must be enforced.
        """
        # Arrange - duplicate keywords
        invalid_marketplace = {
            "name": "test-marketplace",
            "plugins": [
                {
                    "name": "test-plugin",
                    "source": "./test",
                    "keywords": ["duplicate", "keyword", "duplicate"],
                }
            ],
        }

        # Act & Assert - should raise ValidationError
        with pytest.raises(jsonschema.ValidationError) as exc_info:
            jsonschema.validate(invalid_marketplace, marketplace_schema)

        # Verify the error is about uniqueness
        assert "unique" in str(exc_info.value).lower()


# =============================================================================
# Test: Unknown properties are rejected
# =============================================================================


class TestMarketplaceSchemaAdditionalProperties:
    """Contract: Unknown properties in manifests must be rejected."""

    def test_marketplace_json_with_unknown_property_fails_validation(
        self,
        marketplace_schema: dict,
    ) -> None:
        """Test that unknown properties in plugin items are rejected.

        Contract: marketplace.schema.json has "additionalProperties": false
        for plugin items, so unknown fields should cause validation errors.
        """
        # Arrange - plugin with unknown field
        invalid_marketplace = {
            "name": "test-marketplace",
            "plugins": [
                {
                    "name": "test-plugin",
                    "source": "./test",
                    "unknown_field": "should-fail",  # Not in schema
                }
            ],
        }

        # Act & Assert - should raise ValidationError
        with pytest.raises(jsonschema.ValidationError) as exc_info:
            jsonschema.validate(invalid_marketplace, marketplace_schema)

        # Verify the error is about additional properties
        error_message = str(exc_info.value).lower()
        assert (
            "additional propert" in error_message
            or "not allowed" in error_message
            or "was unexpected" in error_message
        ), f"Expected additionalProperties error, got: {exc_info.value.message}"

    def test_marketplace_json_with_unknown_root_property_fails_validation(
        self,
        marketplace_schema: dict,
    ) -> None:
        """Test that unknown root-level properties are rejected.

        Contract: Root-level additionalProperties is also false.
        """
        # Arrange - unknown field at root level
        invalid_marketplace = {
            "name": "test-marketplace",
            "plugins": [{"name": "test-plugin", "source": "./test"}],
            "invalid_root_field": "should-fail",
        }

        # Act & Assert - should raise ValidationError
        with pytest.raises(jsonschema.ValidationError) as exc_info:
            jsonschema.validate(invalid_marketplace, marketplace_schema)

        # Verify the error is about additional properties
        error_message = str(exc_info.value).lower()
        assert (
            "additional propert" in error_message
            or "not allowed" in error_message
            or "was unexpected" in error_message
        )


# =============================================================================
# Test: Validation script validates all manifests
# =============================================================================


@pytest.mark.skipif(
    shutil.which("uv") is None,
    reason="uv not available in this environment",
)
class TestValidationScriptIntegration:
    """Contract: validate_plugin_manifests.py must validate all three manifests."""

    def test_all_manifests_pass_validation(
        self,
        validation_script_path: Path,
        project_root: Path,
    ) -> None:
        """Test that all three manifests pass the validation script.

        Contract: The validation script MUST validate:
        - .claude-plugin/plugin.json
        - .claude-plugin/marketplace.json
        - hooks/hooks.json

        And all must pass for the script to return exit code 0.

        Acceptance Criteria:
        - Script exits with code 0
        - Output contains "All validations passed!"
        - Each manifest shows [PASS] status
        """
        # Act - run the validation script with uv
        result = subprocess.run(
            ["uv", "run", "python", str(validation_script_path)],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=30,
        )

        # Assert - exit code is 0
        assert result.returncode == 0, (
            f"Validation script failed with exit code {result.returncode}.\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )

        # Assert - success message present
        assert "All validations passed!" in result.stdout, (
            f"Expected success message not found in output.\nstdout:\n{result.stdout}"
        )

        # Assert - each manifest shows [PASS]
        required_manifests = [
            "plugin.json",
            "marketplace.json",
            "hooks.json",
        ]

        for manifest in required_manifests:
            assert "[PASS]" in result.stdout and manifest in result.stdout, (
                f"Expected [PASS] for {manifest} in output.\nstdout:\n{result.stdout}"
            )

    def test_validation_script_uses_uv_run(
        self,
        validation_script_path: Path,
        project_root: Path,
    ) -> None:
        """Test that validation script can be run with uv run.

        Contract: Per python-environment.md, all Python scripts should
        work with 'uv run' for proper dependency isolation.

        Note: This test verifies the script is compatible with uv run,
        even if we use python3 directly in other tests.
        """
        # Act - run with uv run
        result = subprocess.run(
            ["uv", "run", "python", str(validation_script_path)],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=30,
        )

        # Assert - should succeed (or gracefully handle missing uv)
        if "uv: command not found" in result.stderr or "uv: not found" in result.stderr:
            pytest.skip("uv not available in environment")

        assert result.returncode == 0, (
            f"Validation script failed with uv run.\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )


# =============================================================================
# Test: Actual marketplace.json validates with keywords
# =============================================================================


class TestActualMarketplaceManifest:
    """Contract: The actual .claude-plugin/marketplace.json must validate."""

    def test_actual_marketplace_json_validates(
        self,
        project_root: Path,
        marketplace_schema: dict,
    ) -> None:
        """Test that the actual marketplace.json validates against schema.

        Contract: The real marketplace.json file (with keywords field)
        must pass validation.
        """
        # Arrange
        marketplace_path = project_root / ".claude-plugin" / "marketplace.json"

        assert marketplace_path.exists(), f"marketplace.json not found at {marketplace_path}"

        marketplace_data = json.loads(marketplace_path.read_text())

        # Act & Assert - should validate without errors
        try:
            jsonschema.validate(marketplace_data, marketplace_schema)
        except jsonschema.ValidationError as e:
            pytest.fail(
                f"Actual marketplace.json failed validation.\n"
                f"Error: {e.message}\n"
                f"Schema path: {list(e.absolute_schema_path)}\n"
                f"Instance path: {list(e.absolute_path)}"
            )

    def test_actual_marketplace_json_has_keywords(
        self,
        project_root: Path,
    ) -> None:
        """Test that the actual marketplace.json uses the keywords field.

        Contract: Per TASK-001, the marketplace.json should include
        keywords for the jerry plugin.
        """
        # Arrange
        marketplace_path = project_root / ".claude-plugin" / "marketplace.json"
        marketplace_data = json.loads(marketplace_path.read_text())

        # Act
        plugins = marketplace_data.get("plugins", [])
        assert len(plugins) > 0, "marketplace.json has no plugins"

        jerry_plugin = next((p for p in plugins if p.get("name") == "jerry"), None)

        # Assert
        assert jerry_plugin is not None, "jerry plugin not found"
        assert "keywords" in jerry_plugin, "jerry plugin missing keywords"
        assert isinstance(jerry_plugin["keywords"], list), "keywords must be an array"
        assert len(jerry_plugin["keywords"]) > 0, "keywords array is empty"
