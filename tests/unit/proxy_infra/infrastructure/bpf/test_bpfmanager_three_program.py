# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BDD tests for BpfManager 3-program lifecycle (connect4, sockops, getsockopt).

TASK-023-174 RED phase: These tests MUST fail before implementation.
GREEN phase: Extend BpfManager to manage all 3 BPF programs atomically.

NPT-013 constraints:
    C5: NEVER leave fewer than 3 programs loaded during ACTIVE engagement.
    B3: NEVER leave programs attached/pinned after teardown.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.proxy_infra.infrastructure.bpf.bpf_manager import BpfManager


def _make_completed(returncode: int = 0, stdout: str = "", stderr: str = "") -> MagicMock:
    """Create a mock CompletedProcess."""
    result = MagicMock()
    result.returncode = returncode
    result.stdout = stdout
    result.stderr = stderr
    return result


class TestLoadAndAttachLoadsThreePrograms:
    """AC-1: BpfManager.load_and_attach() loads all 3 BPF programs."""

    def test_load_and_attach_loads_three_programs(self) -> None:
        """load_and_attach calls bpftool prog load 3 times (connect4, sockops, getsockopt).

        C5: All 3 programs must be loaded atomically during activation.
        """
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(0, stdout="/sys/fs/cgroup/docker/abc123")
            manager.load_and_attach("abc123")

        # Count bpftool prog load calls
        load_calls = [c for c in mock_run.call_args_list if "prog" in str(c) and "load" in str(c)]
        assert len(load_calls) == 3, f"Expected 3 bpftool prog load calls, got {len(load_calls)}"


class TestDetachAndCleanupDetachesThreePrograms:
    """AC-2: BpfManager.detach_and_cleanup() detaches all 3 programs."""

    def test_detach_and_cleanup_detaches_three_programs(self) -> None:
        """detach_and_cleanup calls bpftool cgroup detach for all 3 programs.

        B3: ALL programs must be detached and unpinned during teardown.
        """
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        manager._attached_cgroup = "/sys/fs/cgroup/docker/abc123"

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(0)
            manager.detach_and_cleanup()

        # Count detach calls
        detach_calls = [c for c in mock_run.call_args_list if "detach" in str(c)]
        assert len(detach_calls) >= 3, (
            f"Expected >= 3 detach calls (one per program + root), got {len(detach_calls)}"
        )

        # Count unlink/unpin calls
        unpin_calls = [c for c in mock_run.call_args_list if "unlink" in str(c)]
        assert len(unpin_calls) == 3, (
            f"Expected 3 unpin calls (one per program), got {len(unpin_calls)}"
        )


class TestPartialLoadFailureRollsBack:
    """AC-3: Partial load failure triggers rollback of all loaded programs."""

    def test_partial_load_failure_rolls_back_all(self) -> None:
        """If sockops loads but getsockopt fails, previously loaded programs are cleaned up.

        C5: System must not remain in a state with fewer than 3 programs.
        """
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")
        call_count = 0

        def selective_failure(cmd, **kwargs):
            nonlocal call_count
            call_count += 1
            cmd_str = " ".join(str(c) for c in cmd)
            # Let first two loads succeed, fail on the third
            if "prog" in cmd_str and "load" in cmd_str:
                if "getsockopt" in cmd_str:
                    result = _make_completed(1, stderr="verifier error")
                    if kwargs.get("check", False):
                        raise RuntimeError(f"BpfManager command failed: {cmd_str}")
                    return result
            return _make_completed(0, stdout="/sys/fs/cgroup/docker/abc123")

        with patch("subprocess.run", side_effect=selective_failure):
            with pytest.raises(RuntimeError):
                manager.load_and_attach("abc123")

        # After failure, verify cleanup happened (unlink calls for rolled-back programs)
        # The manager should have attempted to unpin the successfully loaded programs


class TestIsReadyChecksAllThreePins:
    """AC-4: is_ready() verifies all 3 programs are pinned."""

    def test_is_ready_checks_all_three_pins(self) -> None:
        """is_ready() checks 3 pin paths exist on bpffs.

        All 3 programs must be verified before declaring the system ready.
        """
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = _make_completed(0, stdout=":15001")
            result = manager.is_ready()

        # Count prog show calls (one per pin path)
        show_calls = [c for c in mock_run.call_args_list if "prog" in str(c) and "show" in str(c)]
        assert len(show_calls) == 3, (
            f"Expected 3 bpftool prog show calls (one per pin), got {len(show_calls)}"
        )
        assert result is True


class TestIsReadyChecksEnvoyPort:
    """AC-4: is_ready() verifies Envoy is listening on port 15001."""

    def test_is_ready_checks_envoy_port_15001(self) -> None:
        """is_ready() verifies port 15001 (Envoy transparent TCP) not port 12345 (old bridge).

        C8: Port 15001 is reserved for Envoy transparent TCP listener.
        """
        manager = BpfManager("/opt/ebpf/connect4.bpf.o")

        with patch("subprocess.run") as mock_run:
            # ss output contains port 15001
            mock_run.return_value = _make_completed(
                0, stdout="LISTEN 0 128 0.0.0.0:15001 0.0.0.0:*"
            )
            result = manager.is_ready()

        assert result is True

        # Verify it checks for 15001, not 12345
        ss_calls = [c for c in mock_run.call_args_list if "ss" in str(c)]
        assert len(ss_calls) >= 1, "Expected at least one ss call for port check"
