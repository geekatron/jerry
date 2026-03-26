#!/bin/sh
# entrypoint-hybrid.sh -- EN-023-001 Hybrid Envoy + BPF tool container entrypoint
#
# Architecture:
#   HTTP/HTTPS traffic:  HTTP_PROXY=envoy:3128 -> Envoy -> target (scope enforcement)
#   Raw TCP traffic:     BPF cgroup/connect4 -> bridge -> SOCKS5 -> proxy-node -> target
#   Zone 1 traffic:      NOT intercepted (loopback, Docker DNS, Envoy IP in bypass map)
#
# Bypass map population (IPs that BPF must NOT redirect):
#   - Loopback (127.0.0.0/8): already handled in BPF C code
#   - Docker DNS (127.0.0.11): loopback range, already skipped by BPF
#   - Envoy IP: HTTP_PROXY traffic goes to envoy directly -- BPF must not intercept it
#   - Proxy-node IP: bridge connects to SOCKS5 proxy -- BPF must not intercept its traffic
#
# Finding F-2 from EN-023-001: stale root cgroup BPF detach required before attaching
# to container cgroup. Without this, bpf_run() on root cgroup blocks child attach.
#
# EN-023-001 PROJ-023-exploit-framework
set -u

BPF_OBJ=/opt/ebpf/connect4.bpf.o
BRIDGE_PORT=12345
SOCKS_HOST=${SOCKS_PROXY_HOST:-proxy-node}
SOCKS_PORT=${SOCKS_PROXY_PORT:-1080}
ENVOY_HOST=${ENVOY_HOST:-envoy}
# INTERCEPT_CGROUP is set AFTER container cgroup is discovered (must be a CHILD, not sibling)
# See F-8: sibling cgroups don't inherit parent BPF programs

echo "=== EN-023-001 Hybrid Envoy + BPF entrypoint ==="
echo "[INFO] SOCKS proxy:   ${SOCKS_HOST}:${SOCKS_PORT}"
echo "[INFO] Envoy proxy:   ${ENVOY_HOST}:3128 (via HTTP_PROXY env)"
echo "[INFO] Bridge port:   127.0.0.1:${BRIDGE_PORT}"

# --- 1. Find this container's cgroup (NOT root — avoids intercepting other containers) ---
# Docker sets hostname to short container ID; cgroup is under /sys/fs/cgroup/docker/
SHORT_ID=$(hostname)
CONTAINER_CGROUP=$(find /sys/fs/cgroup/docker -maxdepth 1 -name "${SHORT_ID}*" -type d 2>/dev/null | head -1)
if [ -z "$CONTAINER_CGROUP" ]; then
    echo "[WARN] Could not find container cgroup for ${SHORT_ID}, using /sys/fs/cgroup as fallback"
    CONTAINER_CGROUP="/sys/fs/cgroup"
fi
echo "[OK]   Container cgroup: ${CONTAINER_CGROUP}"

# INTERCEPT_CGROUP must be a CHILD of CONTAINER_CGROUP so BPF inheritance works (F-8 fix)
INTERCEPT_CGROUP="${CONTAINER_CGROUP}/jerry-intercept"
mkdir -p "${INTERCEPT_CGROUP}" 2>/dev/null || true
echo "[OK]   Intercept cgroup: ${INTERCEPT_CGROUP} (child of container cgroup)"

# --- 2. Clean stale BPF pins from any previous run ---
echo "[INFO] Cleaning stale BPF pins..."
find /sys/fs/bpf -name 'connect4_poc' -exec unlink {} \; 2>/dev/null || true
find /sys/fs/bpf/poc_maps -type f -exec unlink {} \; 2>/dev/null || true
rmdir /sys/fs/bpf/poc_maps 2>/dev/null || true

# --- 3. Load BPF program and pin maps ---
echo "[INFO] Loading BPF program from ${BPF_OBJ}"
bpftool prog load "${BPF_OBJ}" /sys/fs/bpf/connect4_poc \
    pinmaps /sys/fs/bpf/poc_maps
echo "[OK]   BPF program pinned at /sys/fs/bpf/connect4_poc"

# --- 4. Detach stale root cgroup BPF (EN-023-001 finding F-2) ---
# Root cgroup BPF programs block per-container cgroup attachment.
# Must detach before attaching to child cgroup.
echo "[INFO] Detaching stale root cgroup BPF (F-2 mitigation)..."
bpftool cgroup detach /sys/fs/cgroup connect4 pinned /sys/fs/bpf/connect4_poc 2>/dev/null || true
echo "[OK]   Root cgroup detach complete (or was already clean)"

# --- 5. Attach to container-specific cgroup ---
echo "[INFO] Attaching BPF to container cgroup ${CONTAINER_CGROUP}"
if bpftool cgroup attach "${CONTAINER_CGROUP}" connect4 pinned /sys/fs/bpf/connect4_poc 2>&1; then
    echo "[OK]   BPF attached to container cgroup (only this container intercepted)"
else
    echo "[WARN] Container cgroup attach failed, falling back to root cgroup"
    bpftool cgroup attach "/sys/fs/cgroup" connect4 pinned /sys/fs/bpf/connect4_poc
    echo "[OK]   BPF attached to root cgroup"
fi
bpftool cgroup show "${CONTAINER_CGROUP}" 2>/dev/null || true

# --- 6. Populate bypass map ---
# BPF must NOT redirect connections to: Envoy, proxy-node.
# Loopback (127.x) and Docker DNS (127.0.0.11) are skipped by the BPF C code.
#
# Helper: add IP to bypass map using Python to construct the hex key
add_bypass_ip() {
    local HOST="$1"
    local LABEL="$2"
    local IP
    IP=$(getent hosts "${HOST}" 2>/dev/null | awk '{print $1}' | head -1)
    if [ -z "$IP" ]; then
        echo "[WARN] Could not resolve ${HOST} for bypass map — traffic to ${LABEL} may be intercepted"
        return
    fi
    python3 -c "
import socket, subprocess, sys
try:
    ip_bytes = socket.inet_aton('${IP}')
    hex_args = ' '.join(f'0x{b:02x}' for b in ip_bytes)
    subprocess.run(
        ['bpftool', 'map', 'update', 'pinned',
         '/sys/fs/bpf/poc_maps/bypass_ips',
         'key', 'hex'] + hex_args.split() +
        ['value', 'hex', '0x01'],
        check=True
    )
    print(f'[OK]   Bypass: ${LABEL} (${IP})')
except Exception as e:
    print(f'[WARN] Bypass map update failed for ${LABEL}: {e}', file=sys.stderr)
"
}

echo "[INFO] Populating BPF bypass map..."

# Envoy: HTTP_PROXY traffic goes directly to envoy — BPF must not intercept it.
# Without this, the tool container's HTTP_PROXY=envoy:3128 connections would be
# BPF-redirected to the bridge instead of going to Envoy.
add_bypass_ip "${ENVOY_HOST}" "envoy (HTTP proxy)"

# Proxy-node: the bridge connects to SOCKS5 proxy-node directly.
# BPF must not intercept bridge -> proxy-node connections (would cause a loop).
add_bypass_ip "${SOCKS_HOST}" "proxy-node (SOCKS5)"

echo "[OK]   Bypass map populated"

# --- 7. Start transparent bridge (in default cgroup — NOT intercepted by BPF) ---
# Bridge receives BPF-redirected raw TCP connections on 127.0.0.1:BRIDGE_PORT,
# reads the original destination from BPF map, and forwards via SOCKS5 to proxy-node.
echo "[INFO] Starting bridge on 127.0.0.1:${BRIDGE_PORT} -> ${SOCKS_HOST}:${SOCKS_PORT}"
python3 /opt/ebpf/bridge.py \
    --listen-port "${BRIDGE_PORT}" \
    --socks-host "${SOCKS_HOST}" \
    --socks-port "${SOCKS_PORT}" \
    --map-path /sys/fs/bpf/poc_maps/dst_latest &
BRIDGE_PID=$!
echo "[OK]   Bridge PID=${BRIDGE_PID} (default cgroup, not intercepted)"

sleep 1

# --- 8. Create intercept wrapper for running commands in the BPF cgroup ---
# Commands run WITHOUT intercept go through HTTP_PROXY (Envoy) if they use HTTP,
# or bypass entirely for non-TCP/non-proxy-aware protocols.
# Commands run WITH intercept have their raw TCP connect() calls redirected by BPF.
cat > /usr/local/bin/intercept <<WRAPPER
#!/bin/sh
# Run a command inside the jerry-intercept cgroup (BPF will intercept connect())
# Usage: intercept <command> [args...]
echo \$\$ > "${INTERCEPT_CGROUP}/cgroup.procs"
exec "\$@"
WRAPPER
chmod +x /usr/local/bin/intercept

# Intercept cgroup already created above (child of container cgroup)

# --- Ready ---
cat <<'EOF'
=== Hybrid Envoy + BPF Tool Container Ready ===

Traffic paths:
  HTTP/HTTPS:  curl http://...             -> HTTP_PROXY -> Envoy:3128 -> target
  Raw TCP:     intercept nc tcp-target 4444 -> BPF -> bridge -> SOCKS5 -> proxy-node -> target
  Zone 1:      curl http://localhost/       -> direct (loopback, not intercepted)

Test commands:
  HTTP (Envoy):      curl -v http://http-target/
  HTTP deny:         curl -v http://unauthorized-host/
  Raw TCP (BPF):     intercept nc -w3 tcp-target 4444

Inspect BPF maps:
  bpftool map dump pinned /sys/fs/bpf/poc_maps/dst_latest
  bpftool map dump pinned /sys/fs/bpf/poc_maps/bypass_ips
  bpftool cgroup show \${CONTAINER_CGROUP}/jerry-intercept

EOF

echo "[INFO] Container ready."
wait $BRIDGE_PID
