# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""E2E integration tests for ``jerry proxy`` CLI namespace.

These tests exercise the CLI through the real parser and handler,
hitting the real DigitalOcean API where applicable.  They require:

  - A valid DO API key in macOS Keychain as ``jerry/proxy.digitalocean.api-key``
    OR in env var ``JERRY_PROXY_DO_API_KEY``
  - Network access to the DigitalOcean API

Run with:
    uv run pytest tests/integration/proxy_infra/test_proxy_cli_e2e.py -m integration -v

References:
    - TASK-023-080: E2E live integration test (real DO API key from Keychain)
    - STORY-023-022: Jerry CLI Proxy Namespace Integration
    - NPT-013 constraint 3: NEVER claim E2E works based on mocks alone
"""

from __future__ import annotations

import json
import os

import pytest

# ---------------------------------------------------------------------------
# Skip conditions
# ---------------------------------------------------------------------------

_HAS_DO_KEY = bool(os.environ.get("JERRY_PROXY_DO_API_KEY"))


def _keychain_has_do_key() -> bool:
    """Check if DO key exists in macOS Keychain without revealing it."""
    try:
        from src.proxy_infra.infrastructure.credentials.keyring_credential_store import (
            KeyringCredentialStore,
        )

        store = KeyringCredentialStore()
        store.get_credential("digitalocean")
        return True
    except Exception:
        return False


_HAS_ANY_DO_KEY = _HAS_DO_KEY or _keychain_has_do_key()

_skip_no_do_key = pytest.mark.skipif(
    not _HAS_ANY_DO_KEY,
    reason="No DigitalOcean API key available (set JERRY_PROXY_DO_API_KEY or use jerry proxy credentials set digitalocean)",
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# E2E: credentials check (read-only, Zone 1)
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestProxyCredentialsCheckE2E:
    """E2E test: ``jerry proxy credentials check digitalocean`` against real Keychain."""

    @_skip_no_do_key
    def test_credentials_check_when_key_exists_then_exits_zero(self) -> None:
        """Verify credentials check finds the real DO key."""
        from src.interface.cli.main import _handle_proxy
        from src.interface.cli.parser import create_parser

        parser = create_parser()
        args = parser.parse_args(["proxy", "credentials", "check", "digitalocean"])
        exit_code = _handle_proxy(args, json_output=False)
        assert exit_code == 0

    @_skip_no_do_key
    def test_credentials_check_json_when_key_exists_then_returns_json(
        self,
    ) -> None:
        """Verify credentials check returns valid JSON with source info."""
        from src.interface.cli.main import _handle_proxy
        from src.interface.cli.parser import create_parser

        parser = create_parser()
        args = parser.parse_args(["proxy", "credentials", "check", "digitalocean"])

        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            exit_code = _handle_proxy(args, json_output=True)

        assert exit_code == 0
        output = json.loads(f.getvalue())
        assert output["found"] is True
        assert output["provider"] == "digitalocean"
        assert output["source"] in ("keychain", "environment")

    def test_credentials_check_when_nonexistent_provider_then_exits_one(self) -> None:
        """Verify credentials check for unknown provider exits 1."""
        from src.interface.cli.main import _handle_proxy
        from src.interface.cli.parser import create_parser

        parser = create_parser()
        args = parser.parse_args(["proxy", "credentials", "check", "nonexistent_provider_xyz"])
        exit_code = _handle_proxy(args, json_output=False)
        assert exit_code == 1


# ---------------------------------------------------------------------------
# E2E: status (read-only, Zone 1 -- hits real DO API)
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestProxyStatusE2E:
    """E2E test: ``jerry proxy status`` against real DigitalOcean API.

    Uses a non-existent engagement ID so no real nodes are returned,
    but the API call itself is real (validates authentication + connectivity).
    """

    @_skip_no_do_key
    def test_status_when_nonexistent_engagement_then_exits_zero_with_empty(
        self,
    ) -> None:
        """Status for a non-existent engagement returns 0 with empty list."""
        from src.interface.cli.main import _handle_proxy
        from src.interface.cli.parser import create_parser

        parser = create_parser()
        args = parser.parse_args(["proxy", "status", "--engagement", "NONEXISTENT-E2E-TEST"])

        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            exit_code = _handle_proxy(args, json_output=True)

        assert exit_code == 0
        output = json.loads(f.getvalue())
        assert output["engagement"] == "NONEXISTENT-E2E-TEST"
        assert output["nodes"] == []


# ---------------------------------------------------------------------------
# E2E: parser round-trip (no API key needed)
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestProxyParserRoundTrip:
    """Verify the parser handles all proxy subcommands without crashing."""

    @pytest.mark.parametrize(
        "argv",
        [
            ["proxy", "credentials", "check", "digitalocean"],
            ["proxy", "credentials", "delete", "nonexistent"],
            ["proxy", "status", "--engagement", "RED-TEST"],
            ["proxy", "gc", "--engagement", "RED-TEST", "--dry-run"],
        ],
    )
    def test_parse_round_trip_when_valid_args_then_no_exception(self, argv: list[str]) -> None:
        """Parser accepts all proxy subcommand shapes without error."""
        from src.interface.cli.parser import create_parser

        parser = create_parser()
        args = parser.parse_args(argv)
        assert args.namespace == "proxy"
