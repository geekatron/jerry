#!/bin/sh
# entrypoint.sh -- EN-023-001 eBPF PoC (Full Chain)
#
# Architecture:
#   1. Create a dedicated cgroup "jerry-intercept" for tool processes
#   2. Load BPF program and attach to jerry-intercept cgroup ONLY
#   3. Bridge + microsocks stay in the default cgroup (NOT intercepted)
#   4. Tool commands (curl, etc.) run inside jerry-intercept cgroup
#
# This ensures BPF only intercepts tool traffic, not bridge/proxy traffic.
set -u

BPF_OBJ=/opt/ebpf/connect4.bpf.o
BRIDGE_PORT=12345
SOCKS_HOST=${SOCKS_PROXY_HOST:-proxy-node}
SOCKS_PORT=${SOCKS_PROXY_PORT:-1080}
INTERCEPT_CGROUP="/sys/fs/cgroup/jerry-intercept"

echo "=== EN-023-001 eBPF cgroup/connect4 PoC (Full Chain) ==="

# --- 1. Find this container's cgroup (NOT root — avoids intercepting other containers) ---
# Docker sets hostname to short container ID; full ID is in /sys/fs/cgroup/docker/
SHORT_ID=$(hostname)
CONTAINER_CGROUP=$(find /sys/fs/cgroup/docker -maxdepth 1 -name "${SHORT_ID}*" -type d 2>/dev/null | head -1)
if [ -z "$CONTAINER_CGROUP" ]; then
    echo "[WARN] Could not find container cgroup for ${SHORT_ID}, using jerry-intercept"
    CONTAINER_CGROUP="${INTERCEPT_CGROUP}"
    mkdir -p "${CONTAINER_CGROUP}"
fi
echo "[OK]   Container cgroup: ${CONTAINER_CGROUP}"

# --- 2. Clean stale pins and load BPF program ---
find /sys/fs/bpf -name 'connect4_poc' -exec unlink {} \; 2>/dev/null || true
find /sys/fs/bpf/poc_maps -type f -exec unlink {} \; 2>/dev/null || true
rmdir /sys/fs/bpf/poc_maps 2>/dev/null || true

echo "[INFO] Loading BPF program from ${BPF_OBJ}"
bpftool prog load "${BPF_OBJ}" /sys/fs/bpf/connect4_poc \
    pinmaps /sys/fs/bpf/poc_maps
echo "[OK]   BPF program pinned at /sys/fs/bpf/connect4_poc"

# --- 3. Attach to jerry-intercept cgroup ---
# Detach any stale BPF from root cgroup (blocks child cgroup attachment)
bpftool cgroup detach /sys/fs/cgroup connect4 pinned /sys/fs/bpf/connect4_poc 2>/dev/null || true

echo "[INFO] Attaching to container cgroup ${CONTAINER_CGROUP}"
if bpftool cgroup attach "${CONTAINER_CGROUP}" connect4 pinned /sys/fs/bpf/connect4_poc 2>&1; then
    echo "[OK]   Program attached to container cgroup (only this container intercepted)"
else
    echo "[WARN] Container cgroup attach failed, falling back to root"
    bpftool cgroup attach "/sys/fs/cgroup" connect4 pinned /sys/fs/bpf/connect4_poc
    echo "[OK]   Program attached to root cgroup"
fi
bpftool cgroup show "${CONTAINER_CGROUP}" || true

# --- 4. Populate bypass map with proxy IPs (for root cgroup fallback) ---
for HOST in "${SOCKS_HOST}"; do
    IP=$(getent hosts "${HOST}" 2>/dev/null | awk '{print $1}')
    if [ -n "$IP" ]; then
        python3 -c "
import socket, subprocess
ip_bytes = socket.inet_aton('${IP}')
hex_args = ' '.join(f'0x{b:02x}' for b in ip_bytes)
subprocess.run(['bpftool', 'map', 'update', 'pinned',
    '/sys/fs/bpf/poc_maps/bypass_ips',
    'key', 'hex'] + hex_args.split() +
    ['value', 'hex', '0x01'], check=True)
" && echo "[OK]   Bypass: ${HOST} (${IP})"
    fi
done

# --- 5. Start transparent bridge (in default cgroup - NOT intercepted) ---
echo "[INFO] Starting bridge on 127.0.0.1:${BRIDGE_PORT} -> ${SOCKS_HOST}:${SOCKS_PORT}"
python3 /opt/ebpf/bridge.py \
    --listen-port "${BRIDGE_PORT}" \
    --socks-host "${SOCKS_HOST}" \
    --socks-port "${SOCKS_PORT}" \
    --map-path /sys/fs/bpf/poc_maps/dst_latest &
BRIDGE_PID=$!
echo "[OK]   Bridge PID=${BRIDGE_PID} (default cgroup, not intercepted)"

sleep 1

# --- 5. Create wrapper to run commands in the intercepted cgroup ---
cat > /usr/local/bin/intercept <<'WRAPPER'
#!/bin/sh
# Run a command inside the jerry-intercept cgroup (BPF will intercept connect())
echo $$ > /sys/fs/cgroup/jerry-intercept/cgroup.procs
exec "$@"
WRAPPER
chmod +x /usr/local/bin/intercept

# --- 6. Verification instructions ---
cat <<'EOF'
=== Full Chain PoC Ready ===

Architecture:
  intercept curl -> BPF cgroup/connect4 -> bridge (127.0.0.1:12345) -> SOCKS5 -> proxy-node:1080 -> target

IMPORTANT: Use 'intercept' wrapper to run commands through the BPF chain:
  docker compose exec ebpf-test intercept curl -v http://test-target/

Without 'intercept', commands bypass BPF (useful for debugging):
  docker compose exec ebpf-test curl -v http://test-target/  (direct, no BPF)

To inspect BPF map:
  docker compose exec ebpf-test bpftool map dump pinned /sys/fs/bpf/poc_maps/dst_latest
  docker compose exec ebpf-test bpftool map dump pinned /sys/fs/bpf/poc_maps/dst_lookup

EOF

echo "[INFO] Container ready. Use 'intercept <command>' for BPF-proxied execution."
wait $BRIDGE_PID
