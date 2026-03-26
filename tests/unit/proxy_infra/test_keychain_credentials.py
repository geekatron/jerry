# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BDD test suite for macOS Keychain credential store + CLI + tiered resolution.

STORY-023-010: macOS Keychain Credential Store
Tasks covered:
  - TASK-023-065: BDD tests (RED)
  - TASK-023-066: KeyringCredentialStore implementation
  - TASK-023-067: CLI jerry proxy credentials set/get/delete
  - TASK-023-068: Tiered credential resolution (keychain → env → error)

RED PHASE (H-20): All tests MUST FAIL before implementation exists.

The keyring library's test backend is used to avoid touching the real
macOS Keychain during tests. Set PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
or use keyring.set_keyring() in fixtures.

Naming convention for keyring entries:
  service_name: "jerry"
  username: "{namespace}.{scope}.{type}" (e.g., "proxy.digitalocean.api-key")

Test pyramid: 60% happy path / 30% negative / 10% edge cases
Naming convention: test_{scenario}_when_{condition}_then_{expected}
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import keyring
import keyring.backend
import pytest

from src.proxy_infra.domain.exceptions.credential_not_found_error import CredentialNotFoundError


# =============================================================================
# Test keyring backend (avoids touching real macOS Keychain)
# =============================================================================


class InMemoryKeyring(keyring.backend.KeyringBackend):
    """In-memory keyring backend for testing. Never touches macOS Keychain."""

    priority = 1  # type: ignore[assignment]

    def __init__(self) -> None:
        """Initialise with empty store."""
        self._store: dict[tuple[str, str], str] = {}

    def set_password(self, service: str, username: str, password: str) -> None:
        """Store a password in memory."""
        self._store[(service, username)] = password

    def get_password(self, service: str, username: str) -> str | None:
        """Retrieve a password from memory."""
        return self._store.get((service, username))

    def delete_password(self, service: str, username: str) -> None:
        """Delete a password from memory."""
        key = (service, username)
        if key not in self._store:
            raise keyring.errors.PasswordDeleteError(f"No entry for {service}/{username}")
        del self._store[key]


@pytest.fixture()
def mock_keyring() -> InMemoryKeyring:
    """Fixture: set keyring backend to in-memory for this test."""
    backend = InMemoryKeyring()
    old_backend = keyring.get_keyring()
    keyring.set_keyring(backend)
    yield backend
    keyring.set_keyring(old_backend)


# =============================================================================
# KeyringCredentialStore tests
# =============================================================================


class TestKeyringCredentialStore:
    """Tests for the KeyringCredentialStore CredentialStorePort implementation."""

    def test_store_when_valid_provider_then_credential_persisted(
        self, mock_keyring: InMemoryKeyring
    ) -> None:
        """Happy path: store a credential and verify it's in the keyring."""
        from src.proxy_infra.infrastructure.credentials.keyring_credential_store import (
            KeyringCredentialStore,
        )

        store = KeyringCredentialStore()
        store.store_credential("digitalocean", "dop_v1_test123")

        assert mock_keyring.get_password("jerry", "proxy.digitalocean.api-key") == "dop_v1_test123"

    def test_get_when_credential_exists_then_returns_value(
        self, mock_keyring: InMemoryKeyring
    ) -> None:
        """Happy path: retrieve a stored credential."""
        from src.proxy_infra.infrastructure.credentials.keyring_credential_store import (
            KeyringCredentialStore,
        )

        mock_keyring.set_password("jerry", "proxy.digitalocean.api-key", "dop_v1_test123")

        store = KeyringCredentialStore()
        result = store.get_credential("digitalocean")
        assert result == "dop_v1_test123"

    def test_get_when_credential_missing_then_raises_not_found(
        self, mock_keyring: InMemoryKeyring
    ) -> None:
        """Missing credential raises CredentialNotFoundError per FM-011."""
        from src.proxy_infra.infrastructure.credentials.keyring_credential_store import (
            KeyringCredentialStore,
        )

        store = KeyringCredentialStore()
        with pytest.raises(CredentialNotFoundError, match="digitalocean"):
            store.get_credential("digitalocean")

    def test_delete_when_credential_exists_then_returns_true(
        self, mock_keyring: InMemoryKeyring
    ) -> None:
        """Delete existing credential returns True."""
        from src.proxy_infra.infrastructure.credentials.keyring_credential_store import (
            KeyringCredentialStore,
        )

        mock_keyring.set_password("jerry", "proxy.digitalocean.api-key", "dop_v1_test123")

        store = KeyringCredentialStore()
        result = store.delete_credential("digitalocean")
        assert result is True
        assert mock_keyring.get_password("jerry", "proxy.digitalocean.api-key") is None

    def test_delete_when_credential_missing_then_returns_false(
        self, mock_keyring: InMemoryKeyring
    ) -> None:
        """Delete non-existent credential returns False (no raise)."""
        from src.proxy_infra.infrastructure.credentials.keyring_credential_store import (
            KeyringCredentialStore,
        )

        store = KeyringCredentialStore()
        result = store.delete_credential("nonexistent")
        assert result is False

    def test_naming_convention_uses_dot_delimited_format(
        self, mock_keyring: InMemoryKeyring
    ) -> None:
        """Credential key follows jerry/{namespace}.{scope}.{type} convention."""
        from src.proxy_infra.infrastructure.credentials.keyring_credential_store import (
            KeyringCredentialStore,
        )

        store = KeyringCredentialStore()
        store.store_credential("vultr", "v_test456")

        # Must use dot-delimited naming: proxy.vultr.api-key
        assert mock_keyring.get_password("jerry", "proxy.vultr.api-key") == "v_test456"

    def test_store_never_logs_credential_value(
        self, mock_keyring: InMemoryKeyring
    ) -> None:
        """Credential value must never appear in log output."""
        import logging

        from src.proxy_infra.infrastructure.credentials.keyring_credential_store import (
            KeyringCredentialStore,
        )

        store = KeyringCredentialStore()
        with patch("logging.Logger.debug") as mock_log:
            store.store_credential("digitalocean", "dop_v1_secret_key_do_not_log")
            for call_args in mock_log.call_args_list:
                full_msg = str(call_args)
                assert "dop_v1_secret_key_do_not_log" not in full_msg

    def test_get_credential_never_returns_none(
        self, mock_keyring: InMemoryKeyring
    ) -> None:
        """get_credential must raise, never return None (FM-011 contract)."""
        from src.proxy_infra.infrastructure.credentials.keyring_credential_store import (
            KeyringCredentialStore,
        )

        store = KeyringCredentialStore()
        # Must raise, not return None
        with pytest.raises(CredentialNotFoundError):
            store.get_credential("missing_provider")


# =============================================================================
# CLI credentials commands tests
# =============================================================================


class TestCliCredentialsCommands:
    """Tests for jerry proxy credentials set/check/delete CLI commands."""

    def test_set_when_input_provided_then_stores_in_keyring(
        self, mock_keyring: InMemoryKeyring
    ) -> None:
        """Set command stores the credential via KeyringCredentialStore."""
        from src.proxy_infra.interface.cli.proxy_commands import credentials_set_command

        credentials_set_command(provider="digitalocean", api_key="dop_v1_test")

        assert mock_keyring.get_password("jerry", "proxy.digitalocean.api-key") == "dop_v1_test"

    def test_check_when_credential_exists_then_returns_found(
        self, mock_keyring: InMemoryKeyring
    ) -> None:
        """Check command reports credential presence without revealing value."""
        from src.proxy_infra.interface.cli.proxy_commands import credentials_check_command

        mock_keyring.set_password("jerry", "proxy.digitalocean.api-key", "secret")

        result = credentials_check_command(provider="digitalocean")
        assert result.found is True
        assert "dop_v1" not in str(result)  # value not exposed

    def test_check_when_credential_missing_then_returns_not_found(
        self, mock_keyring: InMemoryKeyring
    ) -> None:
        """Check command reports not found when no credential stored."""
        from src.proxy_infra.interface.cli.proxy_commands import credentials_check_command

        result = credentials_check_command(provider="nonexistent")
        assert result.found is False

    def test_delete_when_credential_exists_then_removes(
        self, mock_keyring: InMemoryKeyring
    ) -> None:
        """Delete command removes credential from keyring."""
        from src.proxy_infra.interface.cli.proxy_commands import credentials_delete_command

        mock_keyring.set_password("jerry", "proxy.digitalocean.api-key", "secret")

        result = credentials_delete_command(provider="digitalocean")
        assert result is True
        assert mock_keyring.get_password("jerry", "proxy.digitalocean.api-key") is None


# =============================================================================
# Tiered credential resolution tests
# =============================================================================


class TestTieredCredentialResolver:
    """Tests for tiered resolution: keychain → env var → error."""

    def _make_resolver(self, mock_keyring: InMemoryKeyring) -> object:
        """Helper: create a TieredCredentialResolver with injected stores."""
        from src.proxy_infra.application.handlers.tiered_credential_resolver import (
            TieredCredentialResolver,
        )
        from src.proxy_infra.infrastructure.adapters.env_credential_store import EnvCredentialStore
        from src.proxy_infra.infrastructure.credentials.keyring_credential_store import (
            KeyringCredentialStore,
        )

        return TieredCredentialResolver(
            primary=KeyringCredentialStore(),
            fallback=EnvCredentialStore(),
        )

    def test_resolve_when_keyring_has_credential_then_returns_it(
        self, mock_keyring: InMemoryKeyring
    ) -> None:
        """Tier 1: Keychain has the credential — use it."""
        mock_keyring.set_password("jerry", "proxy.digitalocean.api-key", "from_keychain")

        resolver = self._make_resolver(mock_keyring)
        result = resolver.get_credential("digitalocean")
        assert result == "from_keychain"

    def test_resolve_when_keyring_empty_but_env_set_then_uses_env(
        self, mock_keyring: InMemoryKeyring, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Tier 2: Keychain empty, env var set — use env var."""
        monkeypatch.setenv("JERRY_PROXY_DIGITALOCEAN_API_KEY", "from_env")

        resolver = self._make_resolver(mock_keyring)
        result = resolver.get_credential("digitalocean")
        assert result == "from_env"

    def test_resolve_when_both_available_then_keyring_wins(
        self, mock_keyring: InMemoryKeyring, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Keychain takes precedence over env var."""
        mock_keyring.set_password("jerry", "proxy.digitalocean.api-key", "from_keychain")
        monkeypatch.setenv("JERRY_PROXY_DIGITALOCEAN_API_KEY", "from_env")

        resolver = self._make_resolver(mock_keyring)
        result = resolver.get_credential("digitalocean")
        assert result == "from_keychain"

    def test_resolve_when_neither_available_then_raises_with_both_paths(
        self, mock_keyring: InMemoryKeyring
    ) -> None:
        """Neither tier has credential — error message lists both resolution methods."""
        resolver = self._make_resolver(mock_keyring)
        with pytest.raises(CredentialNotFoundError, match="(?is)keychain.*environment"):
            resolver.get_credential("digitalocean")

    def test_resolve_implements_credential_store_port(self, mock_keyring: InMemoryKeyring) -> None:
        """TieredCredentialResolver must implement CredentialStorePort."""
        from src.proxy_infra.domain.ports.credential_store_port import CredentialStorePort

        resolver = self._make_resolver(mock_keyring)
        assert isinstance(resolver, CredentialStorePort)
