# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Architecture tests verifying bypass_ips map and SocksBridge TCP path removal.

TASK-023-173 RED phase: These tests MUST fail before implementation.
GREEN phase: Remove bypass_ips map, populate_bypass, and SocksBridge BPF map reading.

EN-023-010: The unified Envoy + SO_MARK architecture eliminates the need for
bypass exemption maps entirely. These tests enforce that removal at the
architecture level, preventing re-introduction.

NPT-013 constraints:
    C3: NEVER use, reference, or recreate a bypass_ips BPF hash map.
    C4: NEVER call or implement populate_bypass().
"""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SRC_DIR = _PROJECT_ROOT / "src"
_BPF_SOURCE_DIR = _SRC_DIR / "proxy_infra" / "ebpf_poc"
_BPF_MANAGER_PATH = _SRC_DIR / "proxy_infra" / "infrastructure" / "bpf" / "bpf_manager.py"
_SOCKS_BRIDGE_PATH = _SRC_DIR / "proxy_infra" / "infrastructure" / "bpf" / "socks_bridge.py"


class TestNoBypassIpsInBpfSource:
    """C3: bypass_ips map must not exist in BPF C source files."""

    def test_no_bypass_ips_in_bpf_source(self) -> None:
        """grep bypass_ips across BPF .c and .h files returns zero matches.

        The unified SO_MARK architecture replaces bypass_ips. Any reference
        to bypass_ips in BPF source code indicates the old dual-path
        architecture has not been fully removed.
        """
        bpf_files = list(_BPF_SOURCE_DIR.glob("*.bpf.c")) + list(_BPF_SOURCE_DIR.glob("*.h"))
        assert len(bpf_files) > 0, f"No BPF source files found in {_BPF_SOURCE_DIR}"

        violations: list[str] = []
        for bpf_file in bpf_files:
            content = bpf_file.read_text()
            for i, line in enumerate(content.splitlines(), start=1):
                if "bypass_ips" in line:
                    violations.append(f"{bpf_file.name}:{i}: {line.strip()}")

        assert violations == [], "bypass_ips found in BPF source (C3 violation):\n" + "\n".join(
            violations
        )


class TestNoPopulateBypassInBpfManager:
    """C4: BpfManager must not have a populate_bypass method."""

    def test_no_populate_bypass_in_bpfmanager(self) -> None:
        """BpfManager class has no method named populate_bypass.

        The unified SO_MARK architecture eliminates the need for bypass
        map population. Any populate_bypass method is an attack surface
        re-introduction (C4).
        """
        from src.proxy_infra.infrastructure.bpf.bpf_manager import BpfManager

        methods = [name for name, _ in inspect.getmembers(BpfManager, predicate=inspect.isfunction)]
        assert "populate_bypass" not in methods, (
            "BpfManager still has populate_bypass method (C4 violation)"
        )


class TestNoBypassIpsInSrcDirectory:
    """C3: No production code in src/ may reference bypass_ips."""

    def test_no_bypass_ips_in_src_directory(self) -> None:
        """grep -r bypass_ips src/ returns only test files and archives.

        Production source code must not reference bypass_ips. References
        in test files (this file) and documentation/archives are permitted.
        """
        violations: list[str] = []
        for py_file in _SRC_DIR.rglob("*.py"):
            # Skip __pycache__ and test directories
            if "__pycache__" in str(py_file):
                continue
            content = py_file.read_text()
            for i, line in enumerate(content.splitlines(), start=1):
                if "bypass_ips" in line:
                    rel = py_file.relative_to(_PROJECT_ROOT)
                    violations.append(f"{rel}:{i}: {line.strip()}")

        assert violations == [], (
            "bypass_ips found in src/ Python files (C3 violation):\n" + "\n".join(violations)
        )


class TestSocksBridgeNoBpfMapRead:
    """SocksBridge.handle_connection must not read BPF maps directly."""

    def test_socks_bridge_no_bpf_map_read(self) -> None:
        """SocksBridge.handle_connection does not call BPF map read methods.

        With the unified Envoy architecture, raw TCP flows through Envoy,
        not SocksBridge. The bridge's handle_connection must not read
        BPF maps (read_original_dst, read_original_dst_by_cookie) for
        forwarding purposes.
        """
        source = _SOCKS_BRIDGE_PATH.read_text()
        tree = ast.parse(source)

        bpf_map_calls = {"read_original_dst", "read_original_dst_by_cookie", "get_socket_cookie"}
        violations: list[str] = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "handle_connection":
                for child in ast.walk(node):
                    if isinstance(child, ast.Attribute) and child.attr in bpf_map_calls:
                        violations.append(
                            f"Line {child.lineno}: handle_connection calls self.{child.attr}"
                        )

        assert violations == [], (
            "SocksBridge.handle_connection still reads BPF maps:\n" + "\n".join(violations)
        )
