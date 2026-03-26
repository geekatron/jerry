# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""SOCKS relay infrastructure layer.

Manages the userspace SOCKS5 relay (socks5lb / redsocks) for the proxy pool.
"""

from src.proxy_infra.infrastructure.relay.socks_relay_manager import SocksRelayManager

__all__ = ["SocksRelayManager"]
