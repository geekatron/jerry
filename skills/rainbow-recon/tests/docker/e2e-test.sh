#!/usr/bin/env sh
# =============================================================================
# Rainbow Recon -- End-to-End Container Test
# =============================================================================
# Tests: Subfinder, httpx, Nuclei CLI availability in recon-pipeline image
# Image: rainbow-recon-pipeline:latest
#
# Usage (from repo root):
#   sh skills/rainbow-recon/tests/docker/e2e-test.sh
#
# Exit codes:
#   0 = all tools verified
#   1 = one or more tools missing or errored
# =============================================================================

set -eu

IMAGE="rainbow-recon-pipeline:latest"
BUILD_CTX="skills/rainbow-recon/tests/docker/recon-pipeline"

PASS=0
FAIL=0

run_test() {
    name="$1"
    cmd="$2"
    printf "  %-40s" "${name}..."
    if docker run --rm --entrypoint "" "${IMAGE}" sh -c "${cmd}" > /dev/null 2>&1; then
        echo "PASS"
        PASS=$((PASS + 1))
    else
        echo "FAIL"
        FAIL=$((FAIL + 1))
    fi
}

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
echo "=== Building ${IMAGE} ==="
docker build -t "${IMAGE}" "${BUILD_CTX}"
echo ""

# ---------------------------------------------------------------------------
# Version checks
# ---------------------------------------------------------------------------
echo "=== Tool availability ==="

run_test "subfinder -version" \
    "subfinder -version 2>&1 | grep -iE 'subfinder|v[0-9]|[0-9]+\.[0-9]+'"

run_test "httpx -version" \
    "httpx -version 2>&1 | grep -iE 'httpx|v[0-9]|[0-9]+\.[0-9]+'"

run_test "dnsx -version" \
    "dnsx -version 2>&1 | grep -iE 'dnsx|v[0-9]|[0-9]+\.[0-9]+'"

run_test "naabu -version" \
    "naabu -version 2>&1 | grep -iE 'naabu|v[0-9]|[0-9]+\.[0-9]+'"

run_test "katana -version" \
    "katana -version 2>&1 | grep -iE 'katana|v[0-9]|[0-9]+\.[0-9]+'"

run_test "nuclei -version" \
    "nuclei -version 2>&1 | grep -iE 'nuclei|v[0-9]|[0-9]+\.[0-9]+'"

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""
echo "================================"
echo "  Recon E2E Test Results"
echo "================================"
echo "  PASS: ${PASS}"
echo "  FAIL: ${FAIL}"
echo "================================"

if [ "${FAIL}" -gt 0 ]; then
    echo "  STATUS: FAIL"
    exit 1
fi

echo "  STATUS: PASS"
exit 0
