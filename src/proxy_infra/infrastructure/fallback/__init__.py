# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""iptables fallback infrastructure layer.

Transparent TCP redirect using iptables REDIRECT rules + redsocks
for environments where BPF is unavailable (kernel < 5.7 or no CAP_BPF).
"""

from src.proxy_infra.infrastructure.fallback.iptables_redirect import IptablesRedirect

__all__ = ["IptablesRedirect"]
