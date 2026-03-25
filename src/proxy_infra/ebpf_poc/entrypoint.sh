#!/bin/sh
# entrypoint.sh -- EN-023-001 eBPF PoC container entrypoint
#
# Steps:
#   1. Locate the container's cgroup v2 path
#   2. Load connect4.bpf.o via bpftool
#   3. Attach program to the cgroup with BPF_CGROUP_INET4_CONNECT
#   4. Start microsocks on 127.0.0.1:1080
#   5. Confirm program is loaded and print map dump instructions
#   6. Tail /dev/null (keep container running for manual tests)
set -e

BPF_OBJ=/opt/ebpf/connect4.bpf.o
PROG_NAME=connect4_redirect
SOCKS_ADDR=127.0.0.1
SOCKS_PORT=1080

echo "=== EN-023-001 eBPF cgroup/connect4 PoC ==="

# --- 1. Locate container cgroup v2 mount ---
CGROUP_PATH=$(cat /proc/self/cgroup | grep '^0::' | cut -d: -f3)
if [ -z "$CGROUP_PATH" ]; then
    # cgroup v1 fallback: use the unified hierarchy if available
    CGROUP_PATH=$(cat /proc/self/cgroup | head -1 | cut -d: -f3)
fi
CGROUP_MOUNT="/sys/fs/cgroup${CGROUP_PATH}"
echo "[INFO] Container cgroup: ${CGROUP_MOUNT}"

if [ ! -d "$CGROUP_MOUNT" ]; then
    echo "[ERROR] cgroup path not found: ${CGROUP_MOUNT}"
    echo "[HINT]  Run with --privileged and cgroup v2 enabled"
    exit 1
fi

# --- 2. Load BPF program ---
echo "[INFO] Loading BPF program from ${BPF_OBJ}"
bpftool prog load "${BPF_OBJ}" /sys/fs/bpf/connect4_poc \
    pinmaps /sys/fs/bpf/poc_maps
echo "[OK]   BPF program pinned at /sys/fs/bpf/connect4_poc"

# --- 3. Attach to cgroup ---
echo "[INFO] Attaching to cgroup ${CGROUP_MOUNT}"
bpftool cgroup attach "${CGROUP_MOUNT}" connect4 \
    pinned /sys/fs/bpf/connect4_poc
echo "[OK]   Program attached (BPF_CGROUP_INET4_CONNECT)"

# Confirm attachment
echo "[INFO] Verifying attachment:"
bpftool cgroup show "${CGROUP_MOUNT}" || true

# --- 4. Start microsocks on loopback:1080 ---
echo "[INFO] Starting microsocks on ${SOCKS_ADDR}:${SOCKS_PORT}"
microsocks -i "${SOCKS_ADDR}" -p "${SOCKS_PORT}" &
MICROSOCKS_PID=$!
echo "[OK]   microsocks PID=${MICROSOCKS_PID}"

# Brief wait for microsocks to bind
sleep 1

# --- 5. Print verification instructions ---
cat <<'EOF'
=== PoC Ready ===

To verify BPF connect() rewrite:
  curl -v http://test-target/  (in another terminal or via exec)

To inspect the original destination map:
  bpftool map show pinned /sys/fs/bpf/poc_maps/map_orig_dst
  bpftool map dump pinned /sys/fs/bpf/poc_maps/map_orig_dst

Expected: after curl, map_orig_dst contains the original {dst_ip, dst_port}
that was rewritten to 127.0.0.1:1080.

EOF

# --- 6. Keep container alive ---
echo "[INFO] Tailing /dev/null. Use 'docker exec' to run tests."
tail -f /dev/null
