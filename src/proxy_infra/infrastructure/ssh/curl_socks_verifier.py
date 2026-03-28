# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""CurlSocksVerifier — concrete SocksVerifierPort adapter using curl subprocess.

Verifies SOCKS5 proxy connectivity by routing a request through the proxy
to an IP echo service. Returns True when the egress IP matches the proxy
node (not the operator's IP).

Security properties:
    - Credentials passed as --proxy-user argument (acceptable for ephemeral nodes)
    - curl process is local to the operator machine
    - Response validated as a valid IP address before returning True

Design constraints:
    H-07: Infrastructure layer adapter implementing application port.
    H-10: One public class per file.
    H-11: All public methods have type annotations.

References:
    - TASK-023-074: CurlSocksVerifier concrete adapter
    - TASK-023-055: SSH credential injection handler (consumer at step 6)
"""

from __future__ import annotations

import logging
import re
import subprocess

logger = logging.getLogger(__name__)

#: Default curl timeout in seconds.
_DEFAULT_TIMEOUT: int = 10

#: IP echo service URL.
_IP_ECHO_URL: str = "https://ifconfig.me"

#: Regex for a valid IPv4 address.
_IPV4_PATTERN: re.Pattern[str] = re.compile(
    r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
)


class CurlSocksVerifier:
    """Verifies SOCKS5 proxy connectivity via curl subprocess.

    Implements the ``SocksVerifierPort`` protocol. Routes a request
    through the SOCKS5 proxy to an IP echo service and validates
    the response.

    Args:
        timeout: Maximum seconds for the curl request.
        echo_url: URL of the IP echo service.
    """

    def __init__(
        self,
        timeout: int = _DEFAULT_TIMEOUT,
        echo_url: str = _IP_ECHO_URL,
    ) -> None:
        """Initialise the SOCKS verifier.

        Args:
            timeout: Curl request timeout in seconds.
            echo_url: IP echo service URL.
        """
        self._timeout = timeout
        self._echo_url = echo_url

    def verify(self, ip: str, port: int, username: str, password: str) -> bool:
        """Verify SOCKS5 proxy is accepting authenticated connections.

        Routes a request through the proxy to an IP echo service.
        Returns True if the response is a valid IP address (proving
        traffic egresses through the proxy, not directly).

        Args:
            ip: Proxy node IPv4 address.
            port: SOCKS5 listening port.
            username: SOCKS5 username.
            password: SOCKS5 password.

        Returns:
            True if SOCKS5 proxy is working (curl exits 0, response is valid IP).
        """
        curl_cmd = [
            "curl",
            "--socks5-hostname", f"{ip}:{port}",
            "--proxy-user", f"{username}:{password}",
            "-s",
            "--max-time", str(self._timeout),
            self._echo_url,
        ]

        logger.debug("SOCKS5 verify: %s:%d via %s", ip, port, self._echo_url)

        try:
            result = subprocess.run(
                curl_cmd,
                capture_output=True,
                text=True,
                timeout=self._timeout + 5,  # subprocess timeout slightly longer than curl's
            )

            if result.returncode != 0:
                logger.warning(
                    "SOCKS5 verification failed: curl exit %d for %s:%d — %s",
                    result.returncode, ip, port, result.stderr.strip(),
                )
                return False

            egress_ip = result.stdout.strip()

            if not _IPV4_PATTERN.match(egress_ip):
                logger.warning(
                    "SOCKS5 verification: unexpected response from %s — %r",
                    self._echo_url, egress_ip[:100],
                )
                return False

            logger.info(
                "SOCKS5 verified: %s:%d egress IP is %s",
                ip, port, egress_ip,
            )
            return True

        except subprocess.TimeoutExpired:
            logger.warning("SOCKS5 verification timed out after %ds: %s:%d", self._timeout, ip, port)
            return False
        except FileNotFoundError:
            logger.error("curl binary not found in PATH")
            return False
