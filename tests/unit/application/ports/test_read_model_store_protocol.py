"""
Unit tests for IReadModelStore protocol.

Test Distribution per impl-es-e-003:
- Happy Path (60%): 3 tests - Protocol definition, runtime checkable, adapter conforms
- Negative (30%): 2 tests - Missing methods, wrong signature
- Edge (10%): 1 test - Protocol documentation
"""

from __future__ import annotations

from typing import Any

import pytest

from src.application.ports.secondary import IReadModelStore
from src.infrastructure.read_models import InMemoryReadModelStore


# === Happy Path Tests (60%) ===


class TestIReadModelStoreProtocolHappyPath:
    """Happy path tests for IReadModelStore protocol."""

    def test_protocol_is_importable(self) -> None:
        """IReadModelStore can be imported."""
        from src.application.ports.secondary import IReadModelStore

        assert IReadModelStore is not None

    def test_protocol_is_runtime_checkable(self) -> None:
        """IReadModelStore is decorated with @runtime_checkable."""
        store = InMemoryReadModelStore()
        assert isinstance(store, IReadModelStore)

    def test_inmemory_adapter_conforms_to_protocol(self) -> None:
        """InMemoryReadModelStore implements all protocol methods."""
        store = InMemoryReadModelStore()

        # Verify all protocol methods exist and are callable
        assert hasattr(store, "save")
        assert hasattr(store, "load")
        assert hasattr(store, "load_all")
        assert hasattr(store, "delete")
        assert hasattr(store, "exists")
        assert callable(store.save)
        assert callable(store.load)


# === Negative Tests (30%) ===


class TestIReadModelStoreProtocolNegative:
    """Negative tests for IReadModelStore protocol."""

    def test_class_without_methods_is_not_store(self) -> None:
        """Class missing methods doesn't satisfy protocol."""

        class NotAStore:
            pass

        store = NotAStore()
        assert not isinstance(store, IReadModelStore)

    def test_class_with_partial_methods_is_not_store(self) -> None:
        """Class with only some methods doesn't satisfy protocol."""

        class PartialStore:
            def save(self, model_type: str, key: str, data: dict) -> None:
                pass

            # Missing: load, load_all, delete, exists

        store = PartialStore()
        assert not isinstance(store, IReadModelStore)


# === Edge Case Tests (10%) ===


class TestIReadModelStoreProtocolEdgeCases:
    """Edge case tests for IReadModelStore protocol."""

    def test_protocol_has_docstring(self) -> None:
        """Protocol has documentation."""
        assert IReadModelStore.__doc__ is not None
        assert "read model" in IReadModelStore.__doc__.lower()
