# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BDD test suite for SidecarAccessLogger and ConnectionLimiter.

Covers TASK-023-044 (sidecar JSON access logging) and TASK-023-047
(sidecar connection limits).

Scenarios:
  TASK-023-044 — SidecarAccessLogger:
    - Logger writes JSONL with all required fields
    - Logger rotation config is correct (100MB / 3 files)
    - No credentials appear in log output (APICALL-004 alignment)
    - Logger appends entries (never overwrites)
    - Default log path is /var/log/jerry-proxy/access.json
    - Timestamp is ISO 8601

  TASK-023-047 — ConnectionLimiter:
    - Limiter tracks connections per proxy node
    - Limiter accepts connections below limit
    - Limiter rejects the (max+1)th connection with 503 response
    - Rejection is logged to the sidecar access logger
    - Per-node tracking detects hotspot imbalance
    - Limit is configurable via JERRY_SIDECAR_MAX_CONNECTIONS env var
    - 60/30/10 distribution: happy path / negative / edge

Test pyramid: 60% happy path / 30% negative / 10% architecture / edge
"""

from __future__ import annotations

import inspect
import json
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.proxy_infra.infrastructure.logging.sidecar_access_logger import SidecarAccessLogger
from src.proxy_infra.infrastructure.relay.connection_limiter import ConnectionLimiter


# =============================================================================
# Shared fixtures
# =============================================================================


@pytest.fixture()
def temp_log_dir(tmp_path: Path) -> Path:
    """Return a temporary directory for sidecar log output."""
    return tmp_path


@pytest.fixture()
def access_logger(temp_log_dir: Path) -> SidecarAccessLogger:
    """Return a SidecarAccessLogger writing to a temporary directory."""
    log_path = temp_log_dir / "access.json"
    return SidecarAccessLogger(log_path=log_path)


@pytest.fixture()
def limiter(access_logger: SidecarAccessLogger) -> ConnectionLimiter:
    """Return a ConnectionLimiter with default max_connections=256."""
    return ConnectionLimiter(max_connections=256, logger=access_logger)


def _make_log_entry(**kwargs: object) -> dict[str, object]:
    """Build a minimal valid access log entry dict."""
    defaults: dict[str, object] = {
        "src_ip": "192.168.1.10",
        "dst_ip": "203.0.113.5",
        "dst_port": 443,
        "proxy_node": "node-fra-001",
        "bytes_sent": 1024,
        "bytes_received": 4096,
        "duration_ms": 350,
        "status": "success",
    }
    defaults.update(kwargs)
    return defaults


# =============================================================================
# TASK-023-044: SidecarAccessLogger — happy path (60%)
# =============================================================================


@pytest.mark.unit
class TestSidecarAccessLoggerWritesEntries:
    """
    Scenario: Sidecar produces JSON access logs for proxied connections
      Given the socks-bridge sidecar is running with logging enabled
      When a request is proxied through the sidecar to the target
      Then a JSON log entry exists at the configured log path
      And the log entry contains all required fields
    """

    def test_write_entry_creates_log_file(
        self, access_logger: SidecarAccessLogger, temp_log_dir: Path
    ) -> None:
        """SidecarAccessLogger must create the JSONL file on first write."""
        access_logger.write_entry(**_make_log_entry())
        assert access_logger.log_path.exists(), (
            "SidecarAccessLogger must create the log file on first write — "
            "TASK-023-044 AC: log file created at configured path"
        )

    def test_write_entry_produces_valid_json_per_line(
        self, access_logger: SidecarAccessLogger
    ) -> None:
        """Each access log entry must be a valid JSON object on its own line (JSONL)."""
        access_logger.write_entry(**_make_log_entry())
        lines = access_logger.log_path.read_text().strip().splitlines()
        assert len(lines) == 1, "One write_entry call must produce exactly one JSONL line"
        try:
            entry = json.loads(lines[0])
        except json.JSONDecodeError as exc:
            pytest.fail(
                f"Access log line is not valid JSON: {exc} — "
                "TASK-023-044 AC: JSONL format required"
            )
        assert isinstance(entry, dict), "Each JSONL line must parse to a dict"

    def test_write_entry_includes_all_required_fields(
        self, access_logger: SidecarAccessLogger
    ) -> None:
        """Access log entry must include all nine required fields (TASK-023-044 AC)."""
        access_logger.write_entry(**_make_log_entry())
        entry = json.loads(access_logger.log_path.read_text().strip())
        required_fields = {
            "timestamp",
            "src_ip",
            "dst_ip",
            "dst_port",
            "proxy_node",
            "bytes_sent",
            "bytes_received",
            "duration_ms",
            "status",
        }
        missing = required_fields - set(entry.keys())
        assert not missing, (
            f"Access log entry missing required fields: {missing} — "
            "TASK-023-044 AC: all nine fields required"
        )

    def test_write_entry_timestamp_is_iso_8601(
        self, access_logger: SidecarAccessLogger
    ) -> None:
        """Access log entry timestamp must be ISO 8601 format."""
        from datetime import datetime

        access_logger.write_entry(**_make_log_entry())
        entry = json.loads(access_logger.log_path.read_text().strip())
        ts = entry["timestamp"]
        try:
            datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except ValueError:
            pytest.fail(
                f"Access log timestamp '{ts}' is not ISO 8601 — "
                "TASK-023-044 AC: timestamp must be ISO 8601"
            )

    def test_write_entry_persists_all_field_values(
        self, access_logger: SidecarAccessLogger
    ) -> None:
        """Field values supplied to write_entry must appear verbatim in the log."""
        access_logger.write_entry(
            src_ip="10.0.0.5",
            dst_ip="172.16.0.1",
            dst_port=8080,
            proxy_node="node-ams-002",
            bytes_sent=512,
            bytes_received=2048,
            duration_ms=120,
            status="success",
        )
        entry = json.loads(access_logger.log_path.read_text().strip())
        assert entry["src_ip"] == "10.0.0.5"
        assert entry["dst_ip"] == "172.16.0.1"
        assert entry["dst_port"] == 8080
        assert entry["proxy_node"] == "node-ams-002"
        assert entry["bytes_sent"] == 512
        assert entry["bytes_received"] == 2048
        assert entry["duration_ms"] == 120
        assert entry["status"] == "success"

    def test_multiple_entries_are_appended_not_overwritten(
        self, access_logger: SidecarAccessLogger
    ) -> None:
        """SidecarAccessLogger must append entries — prior entries must not be lost."""
        access_logger.write_entry(**_make_log_entry(src_ip="10.0.0.1"))
        access_logger.write_entry(**_make_log_entry(src_ip="10.0.0.2"))
        access_logger.write_entry(**_make_log_entry(src_ip="10.0.0.3"))
        lines = access_logger.log_path.read_text().strip().splitlines()
        assert len(lines) == 3, (
            "SidecarAccessLogger must append entries — "
            "all three connection entries must be present"
        )

    def test_status_values_accepted(
        self, access_logger: SidecarAccessLogger
    ) -> None:
        """Logger must accept all valid status values: success, error, timeout."""
        for status_val in ("success", "error", "timeout", "rejected_max_connections"):
            access_logger.write_entry(**_make_log_entry(status=status_val))
        entries = [
            json.loads(line)
            for line in access_logger.log_path.read_text().strip().splitlines()
        ]
        recorded_statuses = {e["status"] for e in entries}
        assert "success" in recorded_statuses
        assert "error" in recorded_statuses
        assert "timeout" in recorded_statuses
        assert "rejected_max_connections" in recorded_statuses


# =============================================================================
# TASK-023-044: SidecarAccessLogger — architecture / rotation config (10%)
# =============================================================================


@pytest.mark.unit
class TestSidecarAccessLoggerRotationConfig:
    """SidecarAccessLogger must expose rotation constants per TASK-023-044 AC."""

    def test_max_file_size_is_100mb(self) -> None:
        """MAX_FILE_SIZE_BYTES must be 100MB per TASK-023-044 AC."""
        expected = 100 * 1024 * 1024
        assert SidecarAccessLogger.MAX_FILE_SIZE_BYTES == expected, (
            f"SidecarAccessLogger.MAX_FILE_SIZE_BYTES must be {expected} (100MB) — "
            "TASK-023-044 AC: max 100MB per file"
        )

    def test_max_rotated_files_is_3(self) -> None:
        """MAX_ROTATED_FILES must be 3 per TASK-023-044 AC."""
        assert SidecarAccessLogger.MAX_ROTATED_FILES == 3, (
            "SidecarAccessLogger.MAX_ROTATED_FILES must be 3 — "
            "TASK-023-044 AC: 3 rotated files retained"
        )

    def test_default_log_path_is_volume_mount(self) -> None:
        """Default log_path must be /var/log/jerry-proxy/access.json per AC."""
        logger = SidecarAccessLogger()
        assert logger.log_path == Path("/var/log/jerry-proxy/access.json"), (
            "Default log_path must be /var/log/jerry-proxy/access.json — "
            "TASK-023-044 AC: Docker volume mount path"
        )


# =============================================================================
# TASK-023-044: SidecarAccessLogger — APICALL-004 credential exclusion (30%)
# =============================================================================


@pytest.mark.unit
class TestSidecarAccessLoggerCredentialExclusion:
    """
    Scenario: Access log never contains credentials (APICALL-004 alignment)
      Given a proxied connection is logged
      When write_entry() is called
      Then no credential-like strings appear in the JSONL output
    """

    def test_write_entry_does_not_accept_password_parameter(
        self, access_logger: SidecarAccessLogger
    ) -> None:
        """write_entry() must have no password, token, or key parameters (APICALL-004)."""
        sig = inspect.signature(access_logger.write_entry)
        param_names = set(sig.parameters.keys())
        forbidden_params = {
            "password", "token", "api_key", "socks5_pass",
            "proxy_password", "credentials", "secret",
        }
        present_forbidden = forbidden_params & param_names
        assert not present_forbidden, (
            f"write_entry() must not accept credential parameters: {present_forbidden} — "
            "APICALL-004: credentials structurally excluded from log interface"
        )

    def test_log_output_contains_no_socks5_credential_fields(
        self, access_logger: SidecarAccessLogger
    ) -> None:
        """Written JSONL must not contain SOCKS5 credential field names (APICALL-004)."""
        access_logger.write_entry(**_make_log_entry())
        log_content = access_logger.log_path.read_text()
        forbidden_keys = [
            "PROXY_PASS", "PROXY_USER", "proxy_password",
            "socks5_pass", "socks5_user", "api_key", "token",
        ]
        for key in forbidden_keys:
            assert key not in log_content, (
                f"Access log must not contain credential field '{key}' — "
                "APICALL-004 alignment"
            )

    def test_log_output_contains_no_do_api_token_pattern(
        self, access_logger: SidecarAccessLogger
    ) -> None:
        """Written JSONL must not contain DigitalOcean API token prefixes."""
        access_logger.write_entry(**_make_log_entry())
        log_content = access_logger.log_path.read_text()
        assert "dop_v1_" not in log_content, (
            "Access log must not contain DigitalOcean API token prefix 'dop_v1_' — "
            "APICALL-004"
        )

    def test_log_output_contains_no_vultr_api_key_prefix(
        self, access_logger: SidecarAccessLogger
    ) -> None:
        """Written JSONL must not contain Vultr API key prefixes."""
        access_logger.write_entry(**_make_log_entry())
        log_content = access_logger.log_path.read_text()
        # Vultr API keys are UUID-like; check for explicit key field names
        assert "vultr_api_key" not in log_content, (
            "Access log must not contain Vultr API key field name — "
            "APICALL-004"
        )


# =============================================================================
# TASK-023-047: ConnectionLimiter — happy path (60%)
# =============================================================================


@pytest.mark.unit
class TestConnectionLimiterAcceptsConnections:
    """
    Scenario: Sidecar accepts connections up to the limit
      Given the socks-bridge sidecar is running with max_connections=256
      When connections are opened below the limit
      Then each connection is accepted
    """

    def test_limiter_accepts_first_connection(
        self, limiter: ConnectionLimiter
    ) -> None:
        """ConnectionLimiter must accept the first connection attempt."""
        accepted, _ = limiter.try_acquire(proxy_node="node-fra-001")
        assert accepted is True, (
            "ConnectionLimiter must accept connections below max_connections — "
            "TASK-023-047 AC"
        )

    def test_limiter_tracks_active_connection_count(
        self, limiter: ConnectionLimiter
    ) -> None:
        """ConnectionLimiter must increment count on each successful acquire."""
        limiter.try_acquire(proxy_node="node-fra-001")
        limiter.try_acquire(proxy_node="node-fra-001")
        assert limiter.active_count("node-fra-001") == 2, (
            "ConnectionLimiter must track connection count per node — "
            "TASK-023-047 AC: per-proxy-node tracking"
        )

    def test_limiter_release_decrements_count(
        self, limiter: ConnectionLimiter
    ) -> None:
        """ConnectionLimiter must decrement count on release."""
        limiter.try_acquire(proxy_node="node-fra-001")
        limiter.try_acquire(proxy_node="node-fra-001")
        limiter.release(proxy_node="node-fra-001")
        assert limiter.active_count("node-fra-001") == 1, (
            "ConnectionLimiter.release() must decrement the per-node count — "
            "TASK-023-047 AC"
        )

    def test_limiter_accepts_exactly_max_connections(
        self, limiter: ConnectionLimiter
    ) -> None:
        """ConnectionLimiter must accept exactly max_connections connections (boundary)."""
        limiter_small = ConnectionLimiter(
            max_connections=5,
            logger=MagicMock(spec=SidecarAccessLogger),
        )
        results = [
            limiter_small.try_acquire(proxy_node="node-fra-001")
            for _ in range(5)
        ]
        accepted_flags = [r[0] for r in results]
        assert all(accepted_flags), (
            "ConnectionLimiter must accept all connections up to max_connections — "
            "TASK-023-047 AC"
        )

    def test_limiter_per_node_counts_are_independent(
        self, limiter: ConnectionLimiter
    ) -> None:
        """Per-node connection counts must be tracked independently."""
        limiter.try_acquire(proxy_node="node-fra-001")
        limiter.try_acquire(proxy_node="node-fra-001")
        limiter.try_acquire(proxy_node="node-ams-002")
        assert limiter.active_count("node-fra-001") == 2
        assert limiter.active_count("node-ams-002") == 1, (
            "Per-node connection counts must be independent — "
            "TASK-023-047 AC: per-proxy-node tracking"
        )

    def test_limiter_unknown_node_returns_zero(
        self, limiter: ConnectionLimiter
    ) -> None:
        """active_count() for an unseen node must return 0."""
        assert limiter.active_count("node-not-seen") == 0, (
            "active_count() for an unseen node must return 0"
        )


# =============================================================================
# TASK-023-047: ConnectionLimiter — rejection / negative cases (30%)
# =============================================================================


@pytest.mark.unit
class TestConnectionLimiterRejectsAtLimit:
    """
    Scenario: Sidecar rejects connections beyond the limit
      Given max_connections=256 and 256 active connections
      When a 257th connection is attempted
      Then the limiter returns (False, 503_body)
      And the rejection is logged to the sidecar access logger
    """

    def _fill_limiter(
        self, limiter: ConnectionLimiter, node: str, count: int
    ) -> None:
        """Acquire *count* connections on *node* without checking results."""
        for _ in range(count):
            limiter.try_acquire(proxy_node=node)

    def test_limiter_rejects_connection_at_limit_plus_one(
        self
    ) -> None:
        """ConnectionLimiter must reject the (max+1)th connection."""
        mock_logger = MagicMock(spec=SidecarAccessLogger)
        limiter_small = ConnectionLimiter(max_connections=3, logger=mock_logger)
        self._fill_limiter(limiter_small, "node-fra-001", 3)

        accepted, body = limiter_small.try_acquire(proxy_node="node-fra-001")
        assert accepted is False, (
            "ConnectionLimiter must reject connections beyond max_connections — "
            "TASK-023-047 AC"
        )

    def test_rejection_body_is_503_json(self) -> None:
        """Rejection response body must be the 503 JSON per TASK-023-047 AC."""
        mock_logger = MagicMock(spec=SidecarAccessLogger)
        limiter_small = ConnectionLimiter(max_connections=2, logger=mock_logger)
        self._fill_limiter(limiter_small, "node-fra-001", 2)

        _, body = limiter_small.try_acquire(proxy_node="node-fra-001")
        assert body is not None, "Rejection must return a non-None response body"
        parsed = json.loads(body)
        assert parsed.get("error") == "proxy_pool_exhausted", (
            "Rejection body must contain error='proxy_pool_exhausted' — "
            "TASK-023-047 AC"
        )
        assert parsed.get("max_connections") == 2, (
            "Rejection body must contain max_connections — "
            "TASK-023-047 AC"
        )

    def test_rejection_is_logged_to_access_logger(self) -> None:
        """ConnectionLimiter must log rejection events to the sidecar access logger."""
        mock_logger = MagicMock(spec=SidecarAccessLogger)
        limiter_small = ConnectionLimiter(max_connections=2, logger=mock_logger)
        self._fill_limiter(limiter_small, "node-fra-001", 2)

        limiter_small.try_acquire(proxy_node="node-fra-001")

        mock_logger.write_entry.assert_called_once()
        call_kwargs = mock_logger.write_entry.call_args.kwargs
        assert call_kwargs.get("status") == "rejected_max_connections", (
            "Rejection event must be logged with status='rejected_max_connections' — "
            "TASK-023-047 AC: rejection events logged to sidecar access log"
        )
        assert call_kwargs.get("proxy_node") == "node-fra-001", (
            "Rejection event log must include the proxy_node — "
            "TASK-023-047 AC"
        )

    def test_count_does_not_increment_on_rejection(self) -> None:
        """Rejected connection must not increment the active count."""
        mock_logger = MagicMock(spec=SidecarAccessLogger)
        limiter_small = ConnectionLimiter(max_connections=2, logger=mock_logger)
        self._fill_limiter(limiter_small, "node-fra-001", 2)

        limiter_small.try_acquire(proxy_node="node-fra-001")
        assert limiter_small.active_count("node-fra-001") == 2, (
            "Rejected connection must not increment the per-node count — "
            "TASK-023-047 AC"
        )

    def test_after_release_slot_is_available_again(self) -> None:
        """After releasing a connection, the slot must be re-acquired."""
        mock_logger = MagicMock(spec=SidecarAccessLogger)
        limiter_small = ConnectionLimiter(max_connections=2, logger=mock_logger)
        self._fill_limiter(limiter_small, "node-fra-001", 2)
        limiter_small.release(proxy_node="node-fra-001")

        accepted, _ = limiter_small.try_acquire(proxy_node="node-fra-001")
        assert accepted is True, (
            "After releasing a slot, the next connection must be accepted — "
            "TASK-023-047 AC"
        )

    def test_release_below_zero_is_safe(self) -> None:
        """release() on a node with zero active connections must not raise."""
        mock_logger = MagicMock(spec=SidecarAccessLogger)
        limiter_small = ConnectionLimiter(max_connections=2, logger=mock_logger)
        try:
            limiter_small.release(proxy_node="node-never-seen")
        except Exception as exc:
            pytest.fail(
                f"release() on unseen node must not raise: {exc} — "
                "defensive programming for race conditions"
            )
        assert limiter_small.active_count("node-never-seen") == 0


# =============================================================================
# TASK-023-047: ConnectionLimiter — env config / architecture (10%)
# =============================================================================


@pytest.mark.unit
class TestConnectionLimiterConfiguration:
    """
    Scenario: Connection limit is configurable via environment variable
      Given JERRY_SIDECAR_MAX_CONNECTIONS is set to 64
      When ConnectionLimiter is constructed from environment
      Then max_connections is 64
    """

    def test_default_max_connections_is_256(self) -> None:
        """Default max_connections must be 256 per TASK-023-047 AC."""
        assert ConnectionLimiter.DEFAULT_MAX_CONNECTIONS == 256, (
            "ConnectionLimiter.DEFAULT_MAX_CONNECTIONS must be 256 — "
            "TASK-023-047 AC"
        )

    def test_from_env_reads_jerry_sidecar_max_connections(self) -> None:
        """from_env() must read JERRY_SIDECAR_MAX_CONNECTIONS from environment."""
        mock_logger = MagicMock(spec=SidecarAccessLogger)
        with patch.dict(os.environ, {"JERRY_SIDECAR_MAX_CONNECTIONS": "64"}):
            limiter = ConnectionLimiter.from_env(logger=mock_logger)
        assert limiter.max_connections == 64, (
            "ConnectionLimiter.from_env() must read JERRY_SIDECAR_MAX_CONNECTIONS — "
            "TASK-023-047 AC: configurable via env"
        )

    def test_from_env_falls_back_to_default_when_unset(self) -> None:
        """from_env() must fall back to DEFAULT_MAX_CONNECTIONS when env var absent."""
        mock_logger = MagicMock(spec=SidecarAccessLogger)
        env_without_var = {
            k: v for k, v in os.environ.items()
            if k != "JERRY_SIDECAR_MAX_CONNECTIONS"
        }
        with patch.dict(os.environ, env_without_var, clear=True):
            limiter = ConnectionLimiter.from_env(logger=mock_logger)
        assert limiter.max_connections == ConnectionLimiter.DEFAULT_MAX_CONNECTIONS, (
            "from_env() must fall back to DEFAULT_MAX_CONNECTIONS when env var absent — "
            "TASK-023-047 AC"
        )

    def test_60_30_10_distribution_across_nodes(self) -> None:
        """
        Simulate 60/30/10 distribution pattern across 3 proxy nodes.

        This tests that per-node tracking correctly reflects an uneven
        connection distribution (hot-spot detection use case).
        """
        mock_logger = MagicMock(spec=SidecarAccessLogger)
        limiter_test = ConnectionLimiter(max_connections=256, logger=mock_logger)
        # Simulate 60 connections to node-1, 30 to node-2, 10 to node-3
        for _ in range(60):
            limiter_test.try_acquire(proxy_node="node-1")
        for _ in range(30):
            limiter_test.try_acquire(proxy_node="node-2")
        for _ in range(10):
            limiter_test.try_acquire(proxy_node="node-3")

        assert limiter_test.active_count("node-1") == 60
        assert limiter_test.active_count("node-2") == 30
        assert limiter_test.active_count("node-3") == 10, (
            "Per-node tracking must reflect 60/30/10 distribution — "
            "TASK-023-047 AC: per-proxy-node tracking detects hotspot imbalance"
        )

    def test_all_nodes_snapshot(self) -> None:
        """all_node_counts() must return a snapshot of all per-node counts."""
        mock_logger = MagicMock(spec=SidecarAccessLogger)
        limiter_test = ConnectionLimiter(max_connections=256, logger=mock_logger)
        limiter_test.try_acquire(proxy_node="node-a")
        limiter_test.try_acquire(proxy_node="node-a")
        limiter_test.try_acquire(proxy_node="node-b")

        counts = limiter_test.all_node_counts()
        assert counts["node-a"] == 2
        assert counts["node-b"] == 1, (
            "all_node_counts() must return per-node snapshot for hotspot analysis — "
            "TASK-023-047 AC"
        )
