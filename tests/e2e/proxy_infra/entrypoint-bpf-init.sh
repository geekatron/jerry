#!/bin/bash
# entrypoint-bpf-init.sh -- Production-aligned BPF init sidecar
#
# Split-cgroup attachment (BUG-023-004, DEC-023-001):
#   connect4 + sockops → tool container cgroup
#   getsockopt → Envoy container cgroup
#
# Discovers cgroups via Docker socket. Loads all 3 BPF programs from
# compiled .bpf.o files. Maps shared via pinned bpffs.
#
# EN-023-009 + EN-023-010 + BUG-023-004 PROJ-023-exploit-framework
set -eu

BPF_DIR=/opt/ebpf
PIN_ROOT=/sys/fs/bpf
MAP_DIR=${PIN_ROOT}/rainbow_maps

# Container names passed via environment (from docker-compose)
TOOL_CONTAINER=${TOOL_CONTAINER:?TOOL_CONTAINER env var required}
ENVOY_CONTAINER=${ENVOY_CONTAINER:?ENVOY_CONTAINER env var required}

echo "=== BPF Init Sidecar (Split-Cgroup, DEC-023-001) ==="
echo "[INFO] Tool container:  ${TOOL_CONTAINER}"
echo "[INFO] Envoy container: ${ENVOY_CONTAINER}"

# --- 1. Discover container cgroups via Docker socket ---
get_cgroup() {
    local container_name="$1"
    local container_id
    container_id=$(docker inspect --format '{{.Id}}' "${container_name}" 2>/dev/null)
    if [ -z "$container_id" ]; then
        echo ""
        return
    fi

    # Try direct path first (standard Docker cgroup v1/v2)
    local cgroup_path="/sys/fs/cgroup/docker/${container_id}"
    if [ -d "$cgroup_path" ]; then
        echo "$cgroup_path"
        return
    fi

    # Fallback: find container's cgroup via its PID (works for network_mode: service:X
    # containers whose cgroup may not be at the standard docker/ path)
    local pid
    pid=$(docker inspect --format '{{.State.Pid}}' "${container_name}" 2>/dev/null)
    if [ -n "$pid" ] && [ "$pid" != "0" ]; then
        # Read the cgroup path from /proc/PID/cgroup (host PID namespace, privileged)
        local proc_cgroup
        proc_cgroup=$(cat "/proc/${pid}/cgroup" 2>/dev/null | head -1 | cut -d: -f3)
        if [ -n "$proc_cgroup" ] && [ -d "/sys/fs/cgroup${proc_cgroup}" ]; then
            echo "/sys/fs/cgroup${proc_cgroup}"
            return
        fi
    fi

    # Last resort: search by short ID
    local short_id="${container_id:0:12}"
    find /sys/fs/cgroup -maxdepth 4 -name "${short_id}*" -type d 2>/dev/null | head -1
}

echo "[INFO] Discovering cgroups..."
TOOL_CGROUP=$(get_cgroup "${TOOL_CONTAINER}")
ENVOY_CGROUP=$(get_cgroup "${ENVOY_CONTAINER}")

if [ -z "$TOOL_CGROUP" ]; then
    echo "[FATAL] Cannot find cgroup for tool container ${TOOL_CONTAINER}"
    exit 1
fi
if [ -z "$ENVOY_CGROUP" ]; then
    echo "[FATAL] Cannot find cgroup for Envoy container ${ENVOY_CONTAINER}"
    exit 1
fi

echo "[OK]   Tool cgroup:  ${TOOL_CGROUP}"
echo "[OK]   Envoy cgroup: ${ENVOY_CGROUP}"

# --- 2. Create jerry-intercept child cgroup (F-8) ---
INTERCEPT_CGROUP="${TOOL_CGROUP}/jerry-intercept"
mkdir -p "${INTERCEPT_CGROUP}" 2>/dev/null || true
echo "[OK]   Intercept cgroup: ${INTERCEPT_CGROUP}"

# --- 3. Clean stale pins ---
echo "[INFO] Cleaning stale BPF pins..."
for PIN in rainbow_connect4 rainbow_sockops rainbow_getsockopt; do
    if [ -d "${PIN_ROOT}/${PIN}" ]; then
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

# --- 4. Load all 3 BPF programs (C5: all or nothing) ---
echo "[INFO] Loading 3 BPF programs..."

bpftool prog load "${BPF_DIR}/connect4.bpf.o" "${PIN_ROOT}/rainbow_connect4" \
    pinmaps "${MAP_DIR}"
echo "[OK]   connect4 loaded (maps created)"

bpftool prog load "${BPF_DIR}/sockops.bpf.o" "${PIN_ROOT}/rainbow_sockops" \
    map name dst_lookup pinned "${MAP_DIR}/dst_lookup" \
    map name port_cookie pinned "${MAP_DIR}/port_cookie"
echo "[OK]   sockops loaded (reusing maps)"

bpftool prog load "${BPF_DIR}/getsockopt.bpf.o" "${PIN_ROOT}/rainbow_getsockopt" \
    map name dst_lookup pinned "${MAP_DIR}/dst_lookup" \
    map name port_cookie pinned "${MAP_DIR}/port_cookie"
echo "[OK]   getsockopt loaded (reusing maps)"

# --- 5. Detach stale root cgroup BPF (F-2) ---
echo "[INFO] Detaching stale root cgroup BPF..."
bpftool cgroup detach /sys/fs/cgroup connect4 pinned "${PIN_ROOT}/rainbow_connect4" 2>/dev/null || true
bpftool cgroup detach /sys/fs/cgroup sock_ops pinned "${PIN_ROOT}/rainbow_sockops" 2>/dev/null || true
bpftool cgroup detach /sys/fs/cgroup getsockopt pinned "${PIN_ROOT}/rainbow_getsockopt" 2>/dev/null || true

# --- 6. Split-cgroup attachment (BUG-023-004, DEC-023-001) ---
# connect4 + sockops → tool cgroup (intercept tool process syscalls)
echo "[INFO] Attaching connect4 + sockops to tool cgroup"
bpftool cgroup attach "${TOOL_CGROUP}" connect4 pinned "${PIN_ROOT}/rainbow_connect4"
echo "[OK]   connect4 → tool cgroup"
bpftool cgroup attach "${TOOL_CGROUP}" sock_ops pinned "${PIN_ROOT}/rainbow_sockops"
echo "[OK]   sockops → tool cgroup"

# getsockopt → Envoy cgroup (intercept Envoy's getsockopt(SO_ORIGINAL_DST))
echo "[INFO] Attaching getsockopt to Envoy cgroup"
bpftool cgroup attach "${ENVOY_CGROUP}" getsockopt pinned "${PIN_ROOT}/rainbow_getsockopt"
echo "[OK]   getsockopt → Envoy cgroup"

# --- Verify ---
echo "[INFO] Tool cgroup programs:"
bpftool cgroup show "${TOOL_CGROUP}" 2>/dev/null || true
echo "[INFO] Envoy cgroup programs:"
bpftool cgroup show "${ENVOY_CGROUP}" 2>/dev/null || true

echo "[OK]   BPF init complete. All 3 programs loaded and attached (split-cgroup)."
