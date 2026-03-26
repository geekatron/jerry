# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""SocksVerifierPort — Protocol for verifying SOCKS5 proxy connectivity (H-10).

Design constraints:
    H-07: Application layer port — no infrastructure imports.
    H-10: One public class per file.
    H-11: All public methods have type annotations.
"""

from __future__ import annotations

from typing import Protocol


class SocksVerifierPort(Protocol):
    """Port for verifying SOCKS5 proxy connectivity.

    Implementations test that a SOCKS5 proxy is accepting authenticated
    connections (e.g., via ``curl --socks5-hostname``).
    """

    def verify(self, ip: str, port: int, username: str, password: str) -> bool:
        """Verify SOCKS5 proxy is accepting authenticated connections.

        Args:
            ip: Node IP address.
            port: SOCKS5 port.
            username: SOCKS5 username.
            password: SOCKS5 password.

        Returns:
            True if SOCKS5 is working.
        """
        ...
