#!/bin/sh
# entrypoint-unified-bpf.sh -- EN-023-010 Unified 3-program BPF entrypoint
#
# Architecture: ALL traffic (HTTP + raw TCP) intercepted by 3 BPF programs
# and routed through Envoy's transparent_tcp listener on port 15001.
#
# NO bypass_ips map. NO SocksBridge. NO HTTP_PROXY.
# Loop prevention via SO_MARK=100 (C2).
#
# Programs loaded:
#   connect4    -- cgroup/connect4: redirect connect() to 127.0.0.1:15001
#   sockops     -- cgroup/sock_ops: map port -> cookie on ACTIVE_ESTABLISHED
#   getsockopt  -- cgroup/getsockopt: chain-lookup SO_ORIGINAL_DST
#
# EN-023-009 + EN-023-010 PROJ-023-exploit-framework
set -eu

BPF_DIR=/opt/ebpf
PIN_ROOT=/sys/fs/bpf
MAP_DIR=${PIN_ROOT}/rainbow_maps
CGROUP_ROOT=/sys/fs/cgroup/docker

echo "=== EN-023-010 Unified 3-Program BPF Entrypoint ==="

# --- 1. Find this container's cgroup ---
SHORT_ID=$(hostname)
CONTAINER_CGROUP=$(find ${CGROUP_ROOT} -maxdepth 1 -name "${SHORT_ID}*" -type d 2>/dev/null | head -1)
if [ -z "$CONTAINER_CGROUP" ]; then
    echo "[WARN] Container cgroup not found for ${SHORT_ID}, using /sys/fs/cgroup"
    CONTAINER_CGROUP="/sys/fs/cgroup"
fi
echo "[OK]   Container cgroup: ${CONTAINER_CGROUP}"

# --- 2. Create jerry-intercept child cgroup (F-8) ---
INTERCEPT_CGROUP="${CONTAINER_CGROUP}/jerry-intercept"
mkdir -p "${INTERCEPT_CGROUP}" 2>/dev/null || true
echo "[OK]   Intercept cgroup: ${INTERCEPT_CGROUP}"

# --- 3. Clean stale pins from any previous run ---
echo "[INFO] Cleaning stale BPF pins..."
for PIN in rainbow_connect4 rainbow_sockops rainbow_getsockopt; do
    if [ -d "${PIN_ROOT}/${PIN}" ]; then
        # loadall creates directories; remove recursively
        find "${PIN_ROOT}/${PIN}" -type f -exec unlink {} \; 2>/dev/null || true
        rmdir "${PIN_ROOT}/${PIN}" 2>/dev/null || true
    elif [ -e "${PIN_ROOT}/${PIN}" ]; then
        unlink "${PIN_ROOT}/${PIN}" 2>/dev/null || true
    fi
done
if [ -d "${MAP_DIR}" ]; then
    find "${MAP_DIR}" -type f -exec unlink {} \; 2>/dev/null || true
    rmdir "${MAP_DIR}" 2>/dev/null || true
fi

# --- 4. Load all 3 BPF programs atomically (C5: all or nothing) ---
echo "[INFO] Loading 3 BPF programs..."

# connect4 first — creates and pins the shared maps (dst_lookup, port_cookie)
bpftool prog load "${BPF_DIR}/connect4.bpf.o" "${PIN_ROOT}/rainbow_connect4" \
    pinmaps "${MAP_DIR}"
echo "[OK]   connect4 loaded and pinned (maps created)"

# sockops — reuse BOTH already-pinned maps (all programs include maps.h)
bpftool prog load "${BPF_DIR}/sockops.bpf.o" "${PIN_ROOT}/rainbow_sockops" \
    map name dst_lookup pinned "${MAP_DIR}/dst_lookup" \
    map name port_cookie pinned "${MAP_DIR}/port_cookie"
echo "[OK]   sockops loaded and pinned (reusing pinned maps)"

# getsockopt — reuse BOTH already-pinned maps
bpftool prog load "${BPF_DIR}/getsockopt.bpf.o" "${PIN_ROOT}/rainbow_getsockopt" \
    map name dst_lookup pinned "${MAP_DIR}/dst_lookup" \
    map name port_cookie pinned "${MAP_DIR}/port_cookie"
echo "[OK]   getsockopt loaded and pinned (reusing pinned maps)"

# --- 5. Detach stale root cgroup BPF (F-2) ---
echo "[INFO] Detaching stale root cgroup BPF..."
bpftool cgroup detach /sys/fs/cgroup connect4 pinned "${PIN_ROOT}/rainbow_connect4" 2>/dev/null || true
bpftool cgroup detach /sys/fs/cgroup sock_ops pinned "${PIN_ROOT}/rainbow_sockops" 2>/dev/null || true
bpftool cgroup detach /sys/fs/cgroup getsockopt pinned "${PIN_ROOT}/rainbow_getsockopt" 2>/dev/null || true

# --- 6. Attach ALL 3 programs to container cgroup ---
echo "[INFO] Attaching 3 programs to ${CONTAINER_CGROUP}"
bpftool cgroup attach "${CONTAINER_CGROUP}" connect4 pinned "${PIN_ROOT}/rainbow_connect4"
echo "[OK]   connect4 attached"
bpftool cgroup attach "${CONTAINER_CGROUP}" sock_ops pinned "${PIN_ROOT}/rainbow_sockops"
echo "[OK]   sockops attached"
bpftool cgroup attach "${CONTAINER_CGROUP}" getsockopt pinned "${PIN_ROOT}/rainbow_getsockopt"
echo "[OK]   getsockopt attached"

# Verify
echo "[INFO] Cgroup BPF programs:"
bpftool cgroup show "${CONTAINER_CGROUP}" 2>/dev/null || true

# --- 7. Create intercept wrapper ---
cat > /usr/local/bin/intercept <<WRAPPER
#!/bin/sh
# Run a command inside the jerry-intercept cgroup (BPF will intercept connect())
echo \$\$ > "${INTERCEPT_CGROUP}/cgroup.procs"
exec "\$@"
WRAPPER
chmod +x /usr/local/bin/intercept

# --- Ready ---
cat <<'EOF'
=== Unified 3-Program BPF + Envoy Ready ===

Traffic flow:
  ALL TCP: connect() -> BPF connect4 -> 127.0.0.1:15001 -> Envoy transparent_tcp
           -> original_dst (recovered via getsockopt BPF chain)
           -> scope filter: allow (original_dst_cluster) or deny (deny_all_tcp)
           -> upstream with SO_MARK=100 (not re-intercepted by BPF)

Test:
  intercept curl -v http://tcp-target/        # HTTP through BPF+Envoy
  intercept sh -c 'echo hi | nc tcp-target 80' # raw TCP through BPF+Envoy

Inspect:
  bpftool cgroup show <cgroup>
  bpftool map dump pinned /sys/fs/bpf/rainbow_maps/dst_lookup
  bpftool map dump pinned /sys/fs/bpf/rainbow_maps/port_cookie

EOF

# --- 8. Start Envoy in the background (same cgroup as tool processes) ---
# BPF getsockopt is cgroup-scoped: Envoy MUST run in the same cgroup as tool
# processes for getsockopt(SO_ORIGINAL_DST) interception to work. Running Envoy
# in a separate container shares the network namespace but NOT the cgroup.
echo "[INFO] Starting Envoy (transparent_tcp :15001 + HTTP :3128)..."
envoy -c /etc/envoy/envoy.yaml --log-level warn &
ENVOY_PID=$!

# Wait for Envoy transparent TCP listener
for i in $(seq 1 30); do
    if bash -c "</dev/tcp/127.0.0.1/15001" 2>/dev/null; then
        echo "[OK]   Envoy listening on :15001 (transparent TCP)"
        break
    fi
    sleep 1
done

echo "[INFO] Container ready. Waiting for test commands."
# Keep container alive for test exec commands
wait $ENVOY_PID
