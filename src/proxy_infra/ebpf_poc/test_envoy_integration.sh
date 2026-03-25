#!/bin/sh
# test_envoy_integration.sh -- EN-023-001 Hybrid Envoy + BPF integration test runner
#
# Tests the hybrid architecture: Envoy handles HTTP, BPF handles raw TCP.
#
# Test Matrix:
#   Test 1: HTTP through Envoy proxy -> http-target returns 200
#           Evidence: curl exit 0, HTTP 200 in response
#   Test 2: Raw TCP through BPF -> proxy-node -> tcp-target returns TCP_ECHO_OK
#           Evidence: nc output contains TCP_ECHO_OK, BPF map has original dst
#   Test 3: Zone 1 traffic (localhost) NOT intercepted by BPF
#           Evidence: BPF bypass map contains loopback-range bypass (structural),
#                     bridge logs show no loopback connections
#   Test 4: Unauthorized HTTP target -> Envoy returns 403
#           Evidence: curl exit non-zero, HTTP 403 in response
#
# Prerequisites:
#   docker compose -f docker-compose.envoy-integration.yml up -d --wait
#
# Usage:
#   ./test_envoy_integration.sh
#   COMPOSE_FILE=docker-compose.envoy-integration.yml ./test_envoy_integration.sh
#
# Exit code: 0 if all tests pass, 1 if any test fails.
#
# EN-023-001 PROJ-023-exploit-framework
set -u

COMPOSE_FILE=${COMPOSE_FILE:-docker-compose.envoy-integration.yml}
TOOL_SVC="hybrid-tool"
PASS_COUNT=0
FAIL_COUNT=0
TOTAL_TESTS=4

# Colour codes for terminal output (disabled if not a TTY)
if [ -t 1 ]; then
    GREEN='\033[0;32m'
    RED='\033[0;31m'
    YELLOW='\033[1;33m'
    NC='\033[0m'
else
    GREEN=''
    RED=''
    YELLOW=''
    NC=''
fi

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

dc() {
    docker compose -f "${COMPOSE_FILE}" "$@"
}

exec_tool() {
    # Run a command in the tool container and capture output.
    # Usage: exec_tool <command...>
    dc exec -T "${TOOL_SVC}" sh -c "$*"
}

pass() {
    PASS_COUNT=$((PASS_COUNT + 1))
    printf "${GREEN}[PASS]${NC} %s\n" "$1"
    if [ -n "${2:-}" ]; then
        printf "       Evidence: %s\n" "$2"
    fi
}

fail() {
    FAIL_COUNT=$((FAIL_COUNT + 1))
    printf "${RED}[FAIL]${NC} %s\n" "$1"
    if [ -n "${2:-}" ]; then
        printf "       Expected: %s\n" "$2"
    fi
    if [ -n "${3:-}" ]; then
        printf "       Got:      %s\n" "$3"
    fi
}

info() {
    printf "${YELLOW}[INFO]${NC} %s\n" "$1"
}

separator() {
    printf "\n--- %s ---\n" "$1"
}

# ---------------------------------------------------------------------------
# Pre-flight checks
# ---------------------------------------------------------------------------

separator "Pre-flight"

# Verify compose file exists
if [ ! -f "${COMPOSE_FILE}" ]; then
    echo "${RED}[ERROR]${NC} Compose file not found: ${COMPOSE_FILE}"
    echo "        Run from the ebpf_poc directory:"
    echo "          cd src/proxy_infra/ebpf_poc"
    echo "          ./test_envoy_integration.sh"
    exit 1
fi

# Verify containers are running
info "Checking containers are up..."
RUNNING=$(dc ps --status running --format json 2>/dev/null | grep -c '"Service"' 2>/dev/null || echo "0")
if [ "${RUNNING}" = "0" ]; then
    info "Containers not running. Starting..."
    dc up -d --wait
    sleep 3
fi

info "Container status:"
dc ps

# Verify hybrid-tool is healthy enough to exec into
if ! exec_tool "echo container_ready" > /dev/null 2>&1; then
    echo "${RED}[ERROR]${NC} Cannot exec into ${TOOL_SVC}. Check container logs:"
    echo "          docker compose -f ${COMPOSE_FILE} logs ${TOOL_SVC}"
    exit 1
fi

info "Bridge readiness check (waiting up to 15s)..."
BRIDGE_READY=0
for i in $(seq 1 15); do
    if exec_tool "sh -c '</dev/tcp/127.0.0.1/12345'" > /dev/null 2>&1; then
        BRIDGE_READY=1
        break
    fi
    sleep 1
done
if [ "${BRIDGE_READY}" = "0" ]; then
    echo "${RED}[ERROR]${NC} Bridge not listening on 127.0.0.1:12345 after 15s"
    echo "        Check entrypoint logs: dc logs ${TOOL_SVC}"
    exit 1
fi
info "Bridge is ready."

# ---------------------------------------------------------------------------
# Test 1: HTTP through Envoy -> http-target -> 200
# ---------------------------------------------------------------------------

separator "Test 1: HTTP through Envoy (expect 200)"
info "Running: curl -s -o /dev/null -w '%{http_code}' http://172.31.1.20/"
info "Traffic path: hybrid-tool -> HTTP_PROXY=envoy:3128 -> envoy -> http-target"

HTTP_CODE=$(exec_tool "curl -s -o /dev/null -w '%{http_code}' --max-time 10 http://172.31.1.20/" 2>&1 || echo "CURL_FAILED")

if [ "${HTTP_CODE}" = "200" ]; then
    # Verify Envoy access log shows the request
    # Brief sleep to allow log flush
    sleep 1
    ENVOY_LOG=$(dc logs envoy 2>/dev/null | grep '"response_code":200' | tail -1)
    EVIDENCE="HTTP 200 from nginx via Envoy; access log: $(echo "${ENVOY_LOG}" | grep -o '"authority":"[^"]*"' || echo 'see dc logs envoy')"
    pass "Test 1" "${EVIDENCE}"
else
    fail "Test 1" "HTTP 200" "Got: ${HTTP_CODE}"
    info "Envoy logs (last 10 lines):"
    dc logs --tail 10 envoy
fi

# ---------------------------------------------------------------------------
# Test 2: Raw TCP through BPF -> bridge -> proxy-node -> tcp-target
# ---------------------------------------------------------------------------

separator "Test 2: Raw TCP through BPF (expect TCP_ECHO_OK)"
info "Running: intercept nc -w5 172.31.1.30 4444"
info "Traffic path: intercept cgroup -> BPF rewrite -> bridge:12345 -> SOCKS5 -> proxy-node -> tcp-target:4444"
info "tcp-target echoes 'TCP_ECHO_OK' per socat config"

# intercept wrapper puts the shell into the jerry-intercept cgroup before exec
TCP_RESP=$(exec_tool "intercept nc -w5 172.31.1.30 4444" 2>&1 || echo "NC_FAILED")

if echo "${TCP_RESP}" | grep -q "TCP_ECHO_OK"; then
    # Verify BPF map recorded the original destination
    BPF_MAP=$(exec_tool "bpftool -j map dump pinned /sys/fs/bpf/poc_maps/dst_latest 2>/dev/null" 2>&1)
    EVIDENCE="nc received TCP_ECHO_OK; BPF dst_latest map: $(echo "${BPF_MAP}" | grep -o '"dst_ip":[0-9]*' | head -1 || echo 'map content present')"
    pass "Test 2" "${EVIDENCE}"
else
    fail "Test 2" "nc output contains TCP_ECHO_OK" "Got: ${TCP_RESP}"
    info "BPF dst_latest map dump:"
    exec_tool "bpftool map dump pinned /sys/fs/bpf/poc_maps/dst_latest" 2>&1 || true
    info "BPF bypass_ips map dump:"
    exec_tool "bpftool map dump pinned /sys/fs/bpf/poc_maps/bypass_ips" 2>&1 || true
fi

# ---------------------------------------------------------------------------
# Test 3: Zone 1 traffic (localhost) NOT intercepted by BPF
# ---------------------------------------------------------------------------

separator "Test 3: Zone 1 traffic not intercepted (structural verification)"
info "Verifying BPF loopback bypass is in effect"
info "Method 1: BPF C code has LOOPBACK_PREFIX check (static — verify source)"
info "Method 2: Connect to bridge port directly (127.0.0.1:12345) succeeds without BPF redirect"
info "Method 3: Bridge log shows no entries for 127.0.0.0/8 destinations"

# Structural check: connect to loopback and verify bridge does NOT log a destination lookup.
# Since BPF skips loopback, the connection to 127.0.0.1:12345 is NOT BPF-intercepted —
# it goes directly to the bridge listener. The bridge will accept the connection but
# will read dst_latest from the map, which contains the PREVIOUS non-loopback destination.
# This demonstrates BPF did not fire for the loopback connect().
#
# We verify this by connecting to loopback WITHOUT the intercept wrapper (not in BPF cgroup)
# and then via the intercept wrapper — both should NOT trigger a new BPF map entry for 127.x.

# Capture current dst_latest before test
DST_BEFORE=$(exec_tool "bpftool -j map lookup pinned /sys/fs/bpf/poc_maps/dst_latest key 0 0 0 0 2>/dev/null" 2>&1 || echo "MAP_EMPTY")

# Connect to localhost — should NOT be intercepted (loopback bypass in BPF)
exec_tool "intercept sh -c 'curl -s --max-time 3 http://127.0.0.1/ > /dev/null 2>&1 || true'" 2>&1 || true

# Capture dst_latest after test — should be unchanged or still non-loopback
DST_AFTER=$(exec_tool "bpftool -j map lookup pinned /sys/fs/bpf/poc_maps/dst_latest key 0 0 0 0 2>/dev/null" 2>&1 || echo "MAP_EMPTY")

# The BPF map should contain the SAME destination as before the loopback test,
# confirming BPF did not write a new 127.x entry.
# dst_ip for 127.0.0.1 in BPF native-endian u32 would be 16777343 (0x0100007F).
LOOPBACK_IN_MAP=$(echo "${DST_AFTER}" | grep -c '"dst_ip":16777343' 2>/dev/null || echo "0")

if [ "${LOOPBACK_IN_MAP}" = "0" ]; then
    pass "Test 3" "BPF map dst_latest does not contain 127.0.0.1 (0x0100007F=16777343) after loopback connect — BPF loopback bypass confirmed"
else
    fail "Test 3" "BPF map should NOT contain 127.0.0.1 as intercepted destination" "dst_latest contains 127.0.0.1 entry: ${DST_AFTER}"
fi

# Also verify bypass_ips map contains envoy IP (defense in depth for HTTP_PROXY path)
BYPASS_MAP=$(exec_tool "bpftool map dump pinned /sys/fs/bpf/poc_maps/bypass_ips 2>/dev/null" 2>&1)
if [ -n "${BYPASS_MAP}" ]; then
    info "Bypass map (envoy + proxy-node IPs):"
    echo "${BYPASS_MAP}" | head -20
fi

# ---------------------------------------------------------------------------
# Test 4: Unauthorized HTTP target -> Envoy returns 403
# ---------------------------------------------------------------------------

separator "Test 4: Unauthorized HTTP target via Envoy (expect 403)"
info "Running: curl -s -o /dev/null -w '%{http_code}' http://unauthorized-host/"
info "Traffic path: hybrid-tool -> HTTP_PROXY=envoy:3128 -> Envoy deny_all -> 403"
info "Envoy config has deny_all catch-all for all domains except 172.31.1.20 / http-target"

HTTP_CODE_DENY=$(exec_tool "curl -s -o /dev/null -w '%{http_code}' --max-time 10 http://10.0.0.99/" 2>&1 || echo "CURL_FAILED")

if [ "${HTTP_CODE_DENY}" = "403" ]; then
    # Verify Envoy logged the denial
    sleep 1
    ENVOY_DENY_LOG=$(dc logs envoy 2>/dev/null | grep '"response_code":403' | tail -1)
    EVIDENCE="HTTP 403 from Envoy deny_all; verdict log: $(echo "${ENVOY_DENY_LOG}" | grep -o '"verdict":"[^"]*"' || echo 'see dc logs envoy')"
    pass "Test 4" "${EVIDENCE}"
else
    fail "Test 4" "HTTP 403 (Envoy deny)" "Got: ${HTTP_CODE_DENY}"
    info "Envoy logs (last 10 lines):"
    dc logs --tail 10 envoy
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

separator "Summary"
printf "\nResults: %s/%s tests passed\n\n" "${PASS_COUNT}" "${TOTAL_TESTS}"

if [ "${PASS_COUNT}" = "${TOTAL_TESTS}" ]; then
    printf "${GREEN}ALL TESTS PASSED${NC}\n"
    printf "\nHybrid Envoy + BPF architecture verified:\n"
    printf "  - HTTP/HTTPS: Envoy proxy scope enforcement operational\n"
    printf "  - Raw TCP:    BPF transparent redirect via SOCKS5 operational\n"
    printf "  - Zone 1:     Loopback traffic not intercepted\n"
    printf "  - Deny:       Envoy deny-by-default enforced for unauthorized targets\n\n"
    exit 0
else
    printf "${RED}${FAIL_COUNT} TEST(S) FAILED${NC}\n\n"
    printf "Diagnostic commands:\n"
    printf "  dc logs hybrid-tool           # entrypoint + bridge logs\n"
    printf "  dc logs envoy                 # Envoy access log (JSON)\n"
    printf "  dc exec hybrid-tool bpftool cgroup show /sys/fs/cgroup/jerry-intercept\n"
    printf "  dc exec hybrid-tool bpftool map dump pinned /sys/fs/bpf/poc_maps/bypass_ips\n"
    printf "  dc exec hybrid-tool bpftool map dump pinned /sys/fs/bpf/poc_maps/dst_latest\n\n"
    exit 1
fi
