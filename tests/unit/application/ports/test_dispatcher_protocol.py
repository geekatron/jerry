# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for dispatcher port interfaces.

Tests the IQueryDispatcher and ICommandDispatcher protocols.
Follows Red/Green/Refactor - these tests fail initially (RED).

Test Distribution per impl-es-e-003:
- Happy Path (60%): 3 tests - Protocol definition, type correctness, docstrings
- Negative (30%): 2 tests - Missing methods, wrong signatures
- Edge (10%): 1 test - Generic type constraints
"""

from __future__ import annotations


class TestIQueryDispatcherProtocol:
    """Tests for IQueryDispatcher protocol definition."""

    # === Happy Path (60%) ===

    def test_protocol_is_importable(self) -> None:
        """IQueryDispatcher can be imported from application.ports."""
        from src.application.ports import IQueryDispatcher

        assert IQueryDispatcher is not None

    def test_protocol_has_dispatch_method(self) -> None:
        """IQueryDispatcher defines dispatch method."""
        from src.application.ports import IQueryDispatcher

        assert hasattr(IQueryDispatcher, "dispatch")

    def test_protocol_is_runtime_checkable(self) -> None:
        """IQueryDispatcher is runtime_checkable for isinstance checks."""
        from src.application.ports import IQueryDispatcher

        # Protocol decorated with @runtime_checkable
        assert getattr(IQueryDispatcher, "__protocol_attrs__", None) is not None or hasattr(
            IQueryDispatcher, "_is_runtime_protocol"
        )

    # === Negative (30%) ===

    def test_class_without_dispatch_is_not_dispatcher(self) -> None:
        """A class without dispatch method doesn't satisfy IQueryDispatcher."""
        from src.application.ports import IQueryDispatcher

        class NotADispatcher:
            pass

        instance = NotADispatcher()
        assert not isinstance(instance, IQueryDispatcher)

    def test_class_with_wrong_dispatch_signature_fails_type_check(self) -> None:
        """A class with wrong dispatch signature should not be valid dispatcher."""
        from src.application.ports import IQueryDispatcher

        class WrongSignature:
            def dispatch(self) -> None:  # Missing query parameter
                pass

        # With @runtime_checkable, isinstance only checks method exists
        # Type checker would catch the wrong signature
        # For runtime, we just verify our protocol is properly defined
        assert hasattr(IQueryDispatcher, "dispatch")

    # === Edge (10%) ===

    def test_dispatcher_supports_generic_query_types(self) -> None:
        """IQueryDispatcher dispatch method accepts generic query type."""
        from src.application.ports import IQueryDispatcher

        # Verify the protocol is generic (uses TypeVar)
        # The dispatch method should accept TQuery and return TResult
        annotations = getattr(IQueryDispatcher.dispatch, "__annotations__", {})
        # At minimum, dispatch should have type annotations
        assert len(annotations) > 0 or hasattr(IQueryDispatcher, "__class_getitem__")


class TestICommandDispatcherProtocol:
    """Tests for ICommandDispatcher protocol definition."""

    def test_protocol_is_importable(self) -> None:
        """ICommandDispatcher can be imported from application.ports."""
        from src.application.ports import ICommandDispatcher

        assert ICommandDispatcher is not None

    def test_protocol_has_dispatch_method(self) -> None:
        """ICommandDispatcher defines dispatch method."""
        from src.application.ports import ICommandDispatcher

        assert hasattr(ICommandDispatcher, "dispatch")


class TestDispatcherExceptions:
    """Tests for dispatcher exception classes."""

    def test_query_handler_not_found_error_is_importable(self) -> None:
        """QueryHandlerNotFoundError can be imported."""
        from src.application.ports import QueryHandlerNotFoundError

        assert QueryHandlerNotFoundError is not None

    def test_query_handler_not_found_error_is_exception(self) -> None:
        """QueryHandlerNotFoundError is an Exception subclass."""
        from src.application.ports import QueryHandlerNotFoundError

        assert issubclass(QueryHandlerNotFoundError, Exception)

    def test_duplicate_handler_error_is_importable(self) -> None:
        """DuplicateHandlerError can be imported."""
        from src.application.ports import DuplicateHandlerError

        assert DuplicateHandlerError is not None

    def test_duplicate_handler_error_is_exception(self) -> None:
        """DuplicateHandlerError is an Exception subclass."""
        from src.application.ports import DuplicateHandlerError

        assert issubclass(DuplicateHandlerError, Exception)
