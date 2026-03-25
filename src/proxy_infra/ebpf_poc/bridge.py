#!/usr/bin/env python3
"""
bridge.py -- Transparent BPF-to-SOCKS5 bridge for EN-023-001 PoC.

Accepts connections redirected by the BPF cgroup/connect4 program,
recovers the original destination by popping from the BPF queue map,
and forwards through a SOCKS5 proxy to the real target.

Full chain: tool -> BPF rewrite -> bridge (this) -> SOCKS5 proxy -> target
"""
import argparse
import json
import select
import socket
import struct
import subprocess
import sys
import threading

SOCKS5_VER = 0x05
SOCKS5_CMD_CONNECT = 0x01
SOCKS5_ATYP_IPV4 = 0x01
SOCKS5_AUTH_NONE = 0x00
SOCKS5_SUCCESS = 0x00


def read_original_dst(map_path: str) -> tuple[str, int] | None:
    """Read the latest original destination from BPF array map[0].

    BPF writes to array index 0 on every intercepted connect().
    Bridge reads it after accepting the redirected connection.
    """
    try:
        result = subprocess.run(
            ["bpftool", "-j", "map", "lookup", "pinned", map_path,
             "key", "0", "0", "0", "0"],
            capture_output=True, text=True, timeout=2,
        )
        if result.returncode != 0:
            print(f"[bridge] bpftool lookup failed: {result.stderr.strip()}",
                  file=sys.stderr)
            return None

        data = json.loads(result.stdout)
        if data is None:
            return None

        # Navigate JSON: may be {"formatted":{"value":{...}}} or {"value":{...}}
        if isinstance(data, list):
            data = data[0] if data else {}
        formatted = data.get("formatted", data)
        value = formatted.get("value", formatted)
        dst_ip_raw = value.get("dst_ip", 0)
        dst_port_raw = value.get("dst_port", 0)

        # Convert native-endian u32 to network-order IP string
        ip_bytes = struct.pack("<I", dst_ip_raw)
        ip_str = socket.inet_ntoa(ip_bytes)

        # Convert native-endian u32 port to host port
        port_bytes = struct.pack("<I", dst_port_raw)
        port = struct.unpack("!H", port_bytes[:2])[0]

        return (ip_str, port)
    except Exception as e:
        print(f"[bridge] Queue pop failed: {e}", file=sys.stderr)
        return None


def socks5_connect(
    socks_host: str, socks_port: int, dst_ip: str, dst_port: int,
) -> socket.socket:
    """Establish a SOCKS5 connection to dst_ip:dst_port via the proxy."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((socks_host, socks_port))

    # Auth: no authentication
    sock.sendall(bytes([SOCKS5_VER, 1, SOCKS5_AUTH_NONE]))
    resp = sock.recv(2)
    if len(resp) < 2 or resp[1] != SOCKS5_AUTH_NONE:
        raise ConnectionError(f"SOCKS5 auth rejected: {resp!r}")

    # Connect request
    ip_bytes = socket.inet_aton(dst_ip)
    port_bytes = struct.pack("!H", dst_port)
    sock.sendall(
        bytes([SOCKS5_VER, SOCKS5_CMD_CONNECT, 0x00, SOCKS5_ATYP_IPV4])
        + ip_bytes + port_bytes
    )
    reply = sock.recv(10)
    if len(reply) < 2 or reply[1] != SOCKS5_SUCCESS:
        raise ConnectionError(f"SOCKS5 connect failed: {reply!r}")

    sock.settimeout(None)
    return sock


def relay(client: socket.socket, remote: socket.socket):
    """Bidirectional data relay between client and remote."""
    sockets = [client, remote]
    try:
        while True:
            readable, _, errored = select.select(sockets, [], sockets, 30)
            if errored:
                break
            for s in readable:
                data = s.recv(65536)
                if not data:
                    return
                target = remote if s is client else client
                target.sendall(data)
    except (BrokenPipeError, ConnectionResetError, OSError):
        pass
    finally:
        client.close()
        remote.close()


def handle_client(
    client: socket.socket,
    addr: tuple,
    socks_host: str,
    socks_port: int,
    map_path: str,
):
    """Handle a single redirected connection."""
    try:
        original = read_original_dst(map_path)
        if original is None:
            print(f"[bridge] No queued destination for {addr}, dropping",
                  file=sys.stderr)
            client.close()
            return

        dst_ip, dst_port = original
        print(f"[bridge] {addr} -> {dst_ip}:{dst_port} via "
              f"{socks_host}:{socks_port}")

        remote = socks5_connect(socks_host, socks_port, dst_ip, dst_port)
        print(f"[bridge] SOCKS5 tunnel established: {dst_ip}:{dst_port}")
        relay(client, remote)
        print(f"[bridge] Connection closed: {dst_ip}:{dst_port}")

    except Exception as e:
        print(f"[bridge] Error handling {addr}: {e}", file=sys.stderr)
        client.close()


def main():
    parser = argparse.ArgumentParser(
        description="BPF-to-SOCKS5 transparent bridge")
    parser.add_argument("--listen-port", type=int, default=12345)
    parser.add_argument("--socks-host", required=True)
    parser.add_argument("--socks-port", type=int, default=1080)
    parser.add_argument("--map-path",
                        default="/sys/fs/bpf/poc_maps/dst_latest")
    args = parser.parse_args()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", args.listen_port))
    server.listen(128)

    print(f"[bridge] Listening on 127.0.0.1:{args.listen_port}")
    print(f"[bridge] SOCKS5 proxy: {args.socks_host}:{args.socks_port}")
    print(f"[bridge] BPF map: {args.map_path}")

    while True:
        client, addr = server.accept()
        t = threading.Thread(
            target=handle_client,
            args=(client, addr, args.socks_host, args.socks_port,
                  args.map_path),
            daemon=True,
        )
        t.start()


if __name__ == "__main__":
    main()
