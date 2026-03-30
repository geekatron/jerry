# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Transparent BPF-to-SOCKS5 bridge with scope validation.

Accepts TCP connections that have been redirected by the BPF cgroup/connect4
program, recovers the original destination by reading from the BPF array map,
validates the destination against the configured scope, and forwards the
connection through a SOCKS5 proxy to the real target.

Full chain:
    tool -> BPF rewrite -> SocksBridge (this) -> SOCKS5 proxy -> target

Design constraints:
    H-10:     One public class per file.
    H-11:     All public methods typed.
    OPSEC-F1: Scope validation REQUIRED for raw TCP destinations.
              Raw TCP bypasses Envoy deny-by-default, so the bridge MUST
              enforce scope independently. Any destination not in the allowed
              set is dropped with a structured WARNING log entry.

References:
    src/proxy_infra/ebpf_poc/bridge.py  -- PoC implementation (reference)
    EN-023-001 OPSEC-F1  -- scope validation requirement
    TASK-023-017         -- bridge requirements
"""

from __future__ import annotations

import ipaddress
import json
import logging
import select
import socket
import struct
import subprocess
import threading

from src.proxy_infra.infrastructure.bpf.original_destination import OriginalDestination

logger = logging.getLogger(__name__)

# SOCKS5 protocol constants
_SOCKS5_VER: int = 0x05
_SOCKS5_CMD_CONNECT: int = 0x01
_SOCKS5_ATYP_IPV4: int = 0x01
_SOCKS5_AUTH_NONE: int = 0x00
_SOCKS5_SUCCESS: int = 0x00

# Relay socket buffer size
_RELAY_BUFFER: int = 65536

# Relay idle timeout seconds
_RELAY_TIMEOUT: int = 30

# Linux SO_COOKIE socket option (kernel 4.18+).
# Returns the 64-bit socket cookie that BPF uses as the key in dst_lookup.
_SO_COOKIE: int = 57

# Default pinned path for the dst_lookup LRU hash map.
# Keyed by socket cookie (__u64), value is struct orig_dst {dst_ip, dst_port}.
_DEFAULT_DST_LOOKUP_PATH: str = "/sys/fs/bpf/rainbow_maps/dst_lookup"


class SocksBridge:
    """Transparent bridge from BPF-redirected TCP to SOCKS5 proxy.

    Listens on localhost:bridge_port for connections redirected by the BPF
    program. For each connection it reads the original destination from the
    BPF array map (via bpftool), validates destination against the allowed
    scope (OPSEC-F1), then establishes a SOCKS5 tunnel to forward the data.

    OPSEC-F1 enforcement: any destination IP not in allowed_networks is
    immediately dropped with a structured WARNING log. This is critical
    because raw TCP bypasses Envoy's deny-by-default policy.

    Args:
        listen_port: TCP port to accept BPF-redirected connections on.
        socks_host: Hostname or IP of the upstream SOCKS5 proxy.
        socks_port: Port of the upstream SOCKS5 proxy.
        map_path: Pinned bpffs path to the dst_latest array map.
        allowed_networks: List of CIDR strings that raw TCP may connect to.
            If empty, ALL raw TCP destinations are allowed (not recommended
            for production; suitable for testing only).
    """

    def __init__(
        self,
        listen_port: int = 12345,
        socks_host: str = "127.0.0.1",
        socks_port: int = 1080,
        map_path: str = "/sys/fs/bpf/rainbow_maps/dst_latest",
        dst_lookup_path: str = _DEFAULT_DST_LOOKUP_PATH,
        allowed_networks: list[str] | None = None,
    ) -> None:
        """Initialise the SOCKS bridge.

        Args:
            listen_port: Port the bridge will accept connections on.
            socks_host: SOCKS5 proxy host address.
            socks_port: SOCKS5 proxy port.
            map_path: Pinned bpffs path to the BPF dst_latest array map (diagnostic fallback).
            dst_lookup_path: Pinned bpffs path to the dst_lookup LRU hash map (primary).
            allowed_networks: CIDR allowlist for raw TCP scope validation.
                None or empty list disables scope filtering.
        """
        self._listen_port = listen_port
        self._socks_host = socks_host
        self._socks_port = socks_port
        self._map_path = map_path
        self._dst_lookup_path = dst_lookup_path
        self._allowed_networks: list[ipaddress.IPv4Network] = []

        if allowed_networks:
            for cidr in allowed_networks:
                try:
                    self._allowed_networks.append(
                        ipaddress.IPv4Network(cidr, strict=False)
                    )
                except ValueError as exc:
                    raise ValueError(
                        f"Invalid CIDR in allowed_networks: {cidr!r}"
                    ) from exc

        self._server: socket.socket | None = None
        self._running = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Bind to the listen port and begin accepting connections in a background thread.

        Raises:
            OSError: If bind or listen fails.
        """
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind(("127.0.0.1", self._listen_port))
        self._server.listen(128)
        self._running = True

        logger.info(
            "SocksBridge listening on 127.0.0.1:%d -> SOCKS5 %s:%d",
            self._listen_port, self._socks_host, self._socks_port,
        )

        accept_thread = threading.Thread(target=self._accept_loop, daemon=True)
        accept_thread.start()

    def stop(self) -> None:
        """Stop the bridge and close the listening socket."""
        self._running = False
        if self._server:
            try:
                self._server.close()
            except OSError:
                pass
            self._server = None
        logger.info("SocksBridge stopped")

    def is_listening(self) -> bool:
        """Return True if the bridge server socket is bound and listening.

        Returns:
            True when the listening socket is active.
        """
        return self._server is not None and self._running

    def read_original_dst(self, map_path: str | None = None) -> OriginalDestination | None:
        """Read the latest original destination from the BPF array map.

        Calls bpftool to look up index 0 of the dst_latest array map. The BPF
        cgroup/connect4 program writes the original destination to this slot on
        every intercepted connect() call.

        Args:
            map_path: Override the instance map_path for this call (for testing).

        Returns:
            OriginalDestination with ip and port, or None if the map is empty
            or bpftool fails.
        """
        path = map_path or self._map_path
        try:
            result = subprocess.run(
                ["bpftool", "-j", "map", "lookup", "pinned", path,
                 "key", "0", "0", "0", "0"],
                capture_output=True,
                text=True,
                timeout=2,
            )
        except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
            logger.warning("bpftool map lookup failed: %s", exc)
            return None

        if result.returncode != 0:
            logger.warning("bpftool lookup error: %s", result.stderr.strip())
            return None

        try:
            data = json.loads(result.stdout)
            if isinstance(data, list):
                data = data[0] if data else {}
            formatted = data.get("formatted", data)
            value = formatted.get("value", formatted)

            dst_ip_raw: int = value.get("dst_ip", 0)
            dst_port_raw: int = value.get("dst_port", 0)

            # BPF stores values in little-endian (native) byte order
            ip_bytes = struct.pack("<I", dst_ip_raw)
            ip_str = socket.inet_ntoa(ip_bytes)

            port_bytes = struct.pack("<I", dst_port_raw)
            port = struct.unpack("!H", port_bytes[:2])[0]

            return OriginalDestination(ip=ip_str, port=port)
        except (KeyError, ValueError, json.JSONDecodeError) as exc:
            logger.warning("Failed to parse bpftool map output: %s", exc)
            return None

    def get_socket_cookie(self, sock: socket.socket) -> int | None:
        """Retrieve the kernel socket cookie for a connected socket.

        The socket cookie is a unique 64-bit identifier assigned by the kernel
        to each socket. The BPF cgroup/connect4 program uses
        ``bpf_get_socket_cookie()`` to key the ``dst_lookup`` LRU hash map,
        enabling per-connection destination lookup without the TOCTOU race
        inherent in the single-entry ``dst_latest`` array.

        Args:
            sock: A connected TCP socket to read the cookie from.

        Returns:
            The 64-bit socket cookie, or None if the getsockopt call fails
            (e.g., kernel does not support SO_COOKIE, or not running on Linux).
        """
        try:
            # SO_COOKIE returns an 8-byte (uint64) value
            cookie_bytes = sock.getsockopt(socket.SOL_SOCKET, _SO_COOKIE, 8)
            return struct.unpack("<Q", cookie_bytes)[0]
        except OSError as exc:
            logger.warning("Failed to get SO_COOKIE: %s", exc)
            return None

    def read_original_dst_by_cookie(
        self,
        cookie: int,
        lookup_path: str | None = None,
    ) -> OriginalDestination | None:
        """Read the original destination from the dst_lookup LRU hash by socket cookie.

        This is the primary destination lookup method (DC-1). Unlike
        ``read_original_dst()`` which reads the single-entry ``dst_latest[0]``
        array (subject to TOCTOU races under concurrent connections), this
        method uses the per-socket-cookie ``dst_lookup`` LRU hash map which
        provides correct per-connection isolation.

        The BPF program writes to ``dst_lookup`` keyed by
        ``bpf_get_socket_cookie(ctx)`` on every intercepted ``connect()``.
        The bridge retrieves the matching entry using the same cookie obtained
        via ``SO_COOKIE`` getsockopt on the accepted client socket.

        Args:
            cookie: The 64-bit socket cookie from ``get_socket_cookie()``.
            lookup_path: Override the dst_lookup map path (for testing).

        Returns:
            OriginalDestination with ip and port, or None if lookup fails.
        """
        path = lookup_path or self._dst_lookup_path
        # Encode cookie as 8 hex bytes (little-endian uint64)
        cookie_bytes = struct.pack("<Q", cookie)
        hex_key = " ".join(f"0x{b:02x}" for b in cookie_bytes)

        try:
            result = subprocess.run(
                ["bpftool", "-j", "map", "lookup", "pinned", path,
                 "key", "hex"] + hex_key.split(),
                capture_output=True,
                text=True,
                timeout=2,
            )
        except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
            logger.warning("bpftool dst_lookup failed: %s", exc)
            return None

        if result.returncode != 0:
            logger.debug("dst_lookup miss for cookie %d: %s", cookie, result.stderr.strip())
            return None

        try:
            data = json.loads(result.stdout)
            if isinstance(data, list):
                data = data[0] if data else {}
            formatted = data.get("formatted", data)
            value = formatted.get("value", formatted)

            dst_ip_raw: int = value.get("dst_ip", 0)
            dst_port_raw: int = value.get("dst_port", 0)

            ip_bytes = struct.pack("<I", dst_ip_raw)
            ip_str = socket.inet_ntoa(ip_bytes)

            port_bytes = struct.pack("<I", dst_port_raw)
            port = struct.unpack("!H", port_bytes[:2])[0]

            return OriginalDestination(ip=ip_str, port=port)
        except (KeyError, ValueError, json.JSONDecodeError) as exc:
            logger.warning("Failed to parse dst_lookup output: %s", exc)
            return None

    def is_destination_allowed(self, ip: str) -> bool:
        """Check whether the destination IP is within the allowed scope (OPSEC-F1).

        If no allowed_networks were configured, all destinations are permitted
        (testing mode). In production, allowed_networks MUST be configured to
        enforce the engagement scope; raw TCP bypasses Envoy deny-by-default.

        Args:
            ip: Destination IPv4 address string to validate.

        Returns:
            True if the destination is within scope or scope filtering is disabled.
        """
        if not self._allowed_networks:
            return True
        try:
            addr = ipaddress.IPv4Address(ip)
        except ValueError:
            logger.warning("Unparseable destination IP in scope check: %r", ip)
            return False
        return any(addr in net for net in self._allowed_networks)

    def handle_connection(
        self,
        client: socket.socket,
        addr: tuple[str, int],
    ) -> None:
        """Handle a single BPF-redirected TCP connection.

        Reads original destination from BPF map, validates scope, establishes
        SOCKS5 tunnel, then relays data bidirectionally until one side closes.

        Args:
            client: Accepted client socket from the BPF redirect.
            addr: Remote address tuple (ip, port) of the connecting client.
        """
        try:
            # DC-1: Use per-socket-cookie lookup (dst_lookup) as primary.
            # Falls back to dst_latest[0] if SO_COOKIE is unavailable.
            original = None
            cookie = self.get_socket_cookie(client)
            if cookie is not None:
                original = self.read_original_dst_by_cookie(cookie)

            if original is None:
                # Fallback to dst_latest[0] — racy under concurrent connections
                # but better than dropping the connection entirely.
                original = self.read_original_dst()

            if original is None:
                logger.warning(
                    "No original destination in BPF map for %s:%d; dropping",
                    addr[0], addr[1],
                )
                client.close()
                return

            if not self.is_destination_allowed(original.ip):
                logger.warning(
                    "OPSEC-F1 scope violation: %s:%d -> %s:%d blocked (not in scope)",
                    addr[0], addr[1], original.ip, original.port,
                )
                client.close()
                return

            logger.info(
                "Forwarding %s:%d -> %s:%d via SOCKS5 %s:%d",
                addr[0], addr[1], original.ip, original.port,
                self._socks_host, self._socks_port,
            )
            remote = self._socks5_connect(original.ip, original.port)
            self._relay(client, remote)

        except Exception as exc:
            logger.error("Error handling connection from %s:%d: %s", addr[0], addr[1], exc)
            client.close()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _accept_loop(self) -> None:
        """Accept connections in a loop and dispatch each to a handler thread.

        Runs until self._running is False or the server socket is closed.
        """
        assert self._server is not None
        while self._running:
            try:
                client, addr = self._server.accept()
            except OSError:
                break
            t = threading.Thread(
                target=self.handle_connection,
                args=(client, addr),
                daemon=True,
            )
            t.start()

    def _socks5_connect(self, dst_ip: str, dst_port: int) -> socket.socket:
        """Establish a SOCKS5 tunnel to dst_ip:dst_port via the configured proxy.

        Args:
            dst_ip: IPv4 address of the real destination.
            dst_port: TCP port of the real destination.

        Returns:
            Connected socket tunnelled through SOCKS5.

        Raises:
            ConnectionError: If SOCKS5 negotiation fails.
            OSError: If the TCP connection to the proxy fails.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((self._socks_host, self._socks_port))

        # Phase 1: method negotiation — request no-auth
        sock.sendall(bytes([_SOCKS5_VER, 1, _SOCKS5_AUTH_NONE]))
        resp = sock.recv(2)
        if len(resp) < 2 or resp[1] != _SOCKS5_AUTH_NONE:
            sock.close()
            raise ConnectionError(
                f"SOCKS5 method negotiation rejected: {resp!r}"
            )

        # Phase 2: CONNECT request
        ip_bytes = socket.inet_aton(dst_ip)
        port_bytes = struct.pack("!H", dst_port)
        sock.sendall(
            bytes([_SOCKS5_VER, _SOCKS5_CMD_CONNECT, 0x00, _SOCKS5_ATYP_IPV4])
            + ip_bytes
            + port_bytes
        )
        reply = sock.recv(10)
        if len(reply) < 2 or reply[1] != _SOCKS5_SUCCESS:
            sock.close()
            raise ConnectionError(
                f"SOCKS5 CONNECT failed (code {reply[1] if len(reply) > 1 else '?'}): "
                f"{reply!r}"
            )

        sock.settimeout(None)
        return sock

    def _relay(self, client: socket.socket, remote: socket.socket) -> None:
        """Bidirectional data relay between client and remote sockets.

        Uses select() with a 30-second idle timeout. Closes both sockets when
        either side closes its half of the connection.

        Args:
            client: The locally accepted client socket.
            remote: The SOCKS5 tunnel socket to the real destination.
        """
        sockets = [client, remote]
        try:
            while True:
                readable, _, errored = select.select(
                    sockets, [], sockets, _RELAY_TIMEOUT
                )
                if errored:
                    break
                if not readable:
                    break
                for sock in readable:
                    data = sock.recv(_RELAY_BUFFER)
                    if not data:
                        return
                    target = remote if sock is client else client
                    target.sendall(data)
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass
        finally:
            client.close()
            remote.close()
