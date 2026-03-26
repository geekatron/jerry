# BDD RED PHASE — All tests expected to FAIL (ImportError). Implementation in TASK-023-027+.
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
BDD test suite for EnvCredentialStore and KeyringCredentialStore adapters.

TASK-023-027: Design ProxyProvisionerPort Interface (Hexagonal Port)

Covers:
  - DA-001: env var is the primary credential source
  - EnvCredentialStore resolves JERRY_PROXY_{PROVIDER}_API_KEY
  - EnvCredentialStore raises CredentialNotFoundError when env var is absent
  - EnvCredentialStore.get_credential() never returns None (FM-011)
  - KeyringCredentialStore uses SERVICE_NAME "jerry-proxy"
  - CompositeCredentialStore: env checked first, keyring second (DA-001)
  - API key must not appear in any log output (APIKEY-002)

Test pyramid: 60% happy path / 30% negative / 10% architecture
"""

from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import pytest

from src.proxy_infra.domain.ports.credential_store_port import (
    CredentialStorePort,
    CredentialNotFoundError,
)
from src.proxy_infra.infrastructure.adapters.env_credential_store import (
    EnvCredentialStore,
)
from src.proxy_infra.infrastructure.adapters.keyring_credential_store import (
    KeyringCredentialStore,
)


# =============================================================================
# Happy path: EnvCredentialStore — DA-001 primary path
# =============================================================================


@pytest.mark.unit
class TestEnvCredentialStoreHappyPath:
    """
    Scenario: Operator has JERRY_PROXY_DIGITALOCEAN_API_KEY set in environment
      Given JERRY_PROXY_DIGITALOCEAN_API_KEY is set to a valid API key
      When get_credential("digitalocean") is called
      Then the API key string is returned without modification
      And no exception is raised
    """

    def test_get_credential_returns_api_key_from_env(self) -> None:
        """DA-001: EnvCredentialStore retrieves key from environment variable."""
        test_key = "dop_v1_abc123def456"
        with patch.dict(
            os.environ, {"JERRY_PROXY_DIGITALOCEAN_API_KEY": test_key}, clear=False
        ):
            store = EnvCredentialStore()
            result = store.get_credential("digitalocean")
        assert result == test_key, (
            "EnvCredentialStore.get_credential('digitalocean') must return the "
            "value of JERRY_PROXY_DIGITALOCEAN_API_KEY — DA-001: env is primary"
        )

    def test_env_var_name_follows_jerry_proxy_convention(self) -> None:
        """EnvCredentialStore must use JERRY_PROXY_{PROVIDER}_API_KEY naming convention.

        CV-009 fix: the canonical env var name is documented in
        ~/.jerry/providers.yaml as 'api_key_env'.  The adapter must follow this
        naming so operators can predict which env var to set for each provider.
        """
        test_key = "v_abc123"
        with patch.dict(
            os.environ, {"JERRY_PROXY_VULTR_API_KEY": test_key}, clear=False
        ):
            store = EnvCredentialStore()
            result = store.get_credential("vultr")
        assert result == test_key, (
            "EnvCredentialStore must read JERRY_PROXY_VULTR_API_KEY for 'vultr' — "
            "CV-009: provider name is uppercased in the env var name"
        )

    def test_provider_name_is_uppercased_in_env_var_key(self) -> None:
        """Provider name must be uppercased when constructing the env var name."""
        test_key = "hcloud_token_xyz"
        with patch.dict(
            os.environ, {"JERRY_PROXY_HETZNER_API_KEY": test_key}, clear=False
        ):
            store = EnvCredentialStore()
            result = store.get_credential("hetzner")
        assert result == test_key, (
            "EnvCredentialStore must uppercase provider name in env var lookup — "
            "JERRY_PROXY_HETZNER_API_KEY, not jerry_proxy_hetzner_api_key"
        )

    def test_store_and_retrieve_roundtrip(self) -> None:
        """EnvCredentialStore.store_credential() must set the env var for retrieval."""
        test_key = "dop_v1_stored_key"
        store = EnvCredentialStore()
        try:
            store.store_credential("digitalocean", test_key)
            result = store.get_credential("digitalocean")
            assert result == test_key, (
                "store_credential() must persist key so get_credential() retrieves it"
            )
        finally:
            # Clean up: remove the env var after the test
            os.environ.pop("JERRY_PROXY_DIGITALOCEAN_API_KEY", None)

    def test_env_credential_store_satisfies_credential_store_port_protocol(
        self,
    ) -> None:
        """EnvCredentialStore must structurally implement CredentialStorePort."""
        store = EnvCredentialStore()
        assert hasattr(store, "get_credential"), (
            "EnvCredentialStore must implement get_credential() — CredentialStorePort"
        )
        assert hasattr(store, "store_credential"), (
            "EnvCredentialStore must implement store_credential() — CredentialStorePort"
        )
        assert hasattr(store, "delete_credential"), (
            "EnvCredentialStore must implement delete_credential() — CredentialStorePort"
        )


# =============================================================================
# Negative path: EnvCredentialStore — missing env var raises CredentialNotFoundError
# =============================================================================


@pytest.mark.unit
class TestEnvCredentialStoreNegativePath:
    """
    Scenario: Operator has NOT set JERRY_PROXY_DIGITALOCEAN_API_KEY
      Given JERRY_PROXY_DIGITALOCEAN_API_KEY is absent from the environment
      When get_credential("digitalocean") is called
      Then CredentialNotFoundError is raised (FM-011)
      And the error message includes actionable guidance
    """

    def test_get_credential_raises_when_env_var_absent(self) -> None:
        """FM-011: CredentialNotFoundError raised when env var is not set."""
        env_without_key = {
            k: v for k, v in os.environ.items()
            if k != "JERRY_PROXY_DIGITALOCEAN_API_KEY"
        }
        with patch.dict(os.environ, env_without_key, clear=True):
            store = EnvCredentialStore()
            with pytest.raises(CredentialNotFoundError) as exc_info:
                store.get_credential("digitalocean")
        assert "digitalocean" in str(exc_info.value).lower() or "DIGITALOCEAN" in str(
            exc_info.value
        ), (
            "CredentialNotFoundError must identify which provider credential is missing — "
            "FM-011: operator must know what to configure"
        )

    def test_get_credential_never_returns_none(self) -> None:
        """FM-011 / DA-001: get_credential() MUST raise, never return None."""
        env_without_key = {
            k: v for k, v in os.environ.items()
            if k != "JERRY_PROXY_DIGITALOCEAN_API_KEY"
        }
        with patch.dict(os.environ, env_without_key, clear=True):
            store = EnvCredentialStore()
            try:
                result = store.get_credential("digitalocean")
                # If no exception raised, result must not be None
                assert result is not None, (
                    "get_credential() must never return None — "
                    "FM-011: CredentialNotFoundError must be raised on miss"
                )
            except CredentialNotFoundError:
                pass  # This is the correct behaviour

    def test_error_message_includes_env_var_name(self) -> None:
        """CredentialNotFoundError message must name the env var to set.

        Actionable guidance: operator must know EXACTLY which env var is missing.
        """
        env_without_key = {
            k: v for k, v in os.environ.items()
            if k != "JERRY_PROXY_DIGITALOCEAN_API_KEY"
        }
        with patch.dict(os.environ, env_without_key, clear=True):
            store = EnvCredentialStore()
            with pytest.raises(CredentialNotFoundError) as exc_info:
                store.get_credential("digitalocean")
        error_msg = str(exc_info.value)
        assert "JERRY_PROXY_DIGITALOCEAN_API_KEY" in error_msg or "jerry proxy" in error_msg.lower(), (
            "CredentialNotFoundError must include the env var name or remediation hint — "
            "operator needs to know exactly what to set"
        )

    def test_delete_credential_returns_false_when_not_found(self) -> None:
        """delete_credential() returns False when credential does not exist."""
        env_without_key = {
            k: v for k, v in os.environ.items()
            if k != "JERRY_PROXY_DIGITALOCEAN_API_KEY"
        }
        with patch.dict(os.environ, env_without_key, clear=True):
            store = EnvCredentialStore()
            result = store.delete_credential("digitalocean")
        assert result is False, (
            "delete_credential() must return False when credential not found — "
            "consistent with CredentialStorePort contract"
        )


# =============================================================================
# Happy path: KeyringCredentialStore
# =============================================================================


@pytest.mark.unit
class TestKeyringCredentialStoreHappyPath:
    """
    Scenario: Operator has stored a credential in OS keyring
      Given the OS keyring contains "jerry-proxy" / "digitalocean" entry
      When get_credential("digitalocean") is called
      Then the stored API key is returned
    """

    def test_keyring_uses_jerry_proxy_service_name(self) -> None:
        """KeyringCredentialStore.SERVICE_NAME must be 'jerry-proxy'.

        The service name is the namespace in the OS keychain.  Using a stable,
        predictable service name allows operators to inspect stored credentials
        via the OS keychain UI.
        """
        assert KeyringCredentialStore.SERVICE_NAME == "jerry-proxy", (
            "KeyringCredentialStore.SERVICE_NAME must be 'jerry-proxy' — "
            "this is the keychain namespace for all Jerry proxy credentials"
        )

    def test_keyring_get_credential_returns_stored_key(self) -> None:
        """DA-001 secondary: KeyringCredentialStore returns key stored in keyring."""
        test_key = "dop_v1_keyring_key"
        with patch("keyring.get_password", return_value=test_key) as mock_get:
            store = KeyringCredentialStore()
            result = store.get_credential("digitalocean")
        mock_get.assert_called_once_with("jerry-proxy", "digitalocean")
        assert result == test_key, (
            "KeyringCredentialStore.get_credential() must return the keyring-stored key"
        )

    def test_keyring_store_credential_calls_keyring_set(self) -> None:
        """KeyringCredentialStore.store_credential() must call keyring.set_password()."""
        test_key = "dop_v1_to_store"
        with patch("keyring.set_password") as mock_set:
            store = KeyringCredentialStore()
            store.store_credential("digitalocean", test_key)
        mock_set.assert_called_once_with("jerry-proxy", "digitalocean", test_key)


# =============================================================================
# Negative path: KeyringCredentialStore
# =============================================================================


@pytest.mark.unit
class TestKeyringCredentialStoreNegativePath:
    """
    Scenario: Keyring has no entry for "digitalocean"
      Given the OS keyring returns None for "jerry-proxy" / "digitalocean"
      When get_credential("digitalocean") is called
      Then CredentialNotFoundError is raised (FM-011, never returns None)
    """

    def test_keyring_raises_when_keyring_returns_none(self) -> None:
        """FM-011: CredentialNotFoundError raised when keyring returns None."""
        with patch("keyring.get_password", return_value=None):
            store = KeyringCredentialStore()
            with pytest.raises(CredentialNotFoundError):
                store.get_credential("digitalocean")

    def test_keyring_delete_returns_true_when_key_existed(self) -> None:
        """KeyringCredentialStore.delete_credential() returns True on successful delete."""
        with patch("keyring.delete_password"), patch(
            "keyring.get_password", return_value="existing_key"
        ):
            store = KeyringCredentialStore()
            result = store.delete_credential("digitalocean")
        assert result is True, (
            "delete_credential() must return True when credential was found and deleted"
        )


# =============================================================================
# Architecture: API key must not appear in log output (APIKEY-002)
# =============================================================================


@pytest.mark.unit
class TestCredentialRedactionInLogs:
    """
    Scenario: API key must never appear in log output (APIKEY-002)
      Given a CredentialNotFoundError is logged
      When the error is formatted for output
      Then no API key value appears in the log string
    """

    def test_credential_not_found_error_does_not_expose_key_value(self) -> None:
        """APIKEY-002: CredentialNotFoundError message must not contain key values."""
        # Simulate an accidental key value being passed to the error
        err = CredentialNotFoundError("digitalocean")
        error_str = str(err)
        # The error should describe the missing credential, not expose a key value
        assert "dop_v1_" not in error_str, (
            "CredentialNotFoundError must not expose API key values — APIKEY-002"
        )

    def test_env_store_get_credential_result_not_logged_on_success(self) -> None:
        """APIKEY-002: The returned API key string must not be logged by the store.

        This is a structural test: the EnvCredentialStore source must not call
        any logging function with the actual key value.
        """
        import inspect
        import src.proxy_infra.infrastructure.adapters.env_credential_store as module

        source = inspect.getsource(module)
        # Heuristic: look for logger.debug/info/warning calls that include the
        # credential variable in a non-redacted context
        suspicious_patterns = [
            "log.debug(credential",
            "log.info(credential",
            "logger.debug(api_key",
            "logger.info(api_key",
            "print(api_key",
            "print(credential",
        ]
        for pattern in suspicious_patterns:
            assert pattern not in source, (
                f"EnvCredentialStore source contains suspicious log pattern '{pattern}' — "
                f"APIKEY-002: API key values must never be logged"
            )
