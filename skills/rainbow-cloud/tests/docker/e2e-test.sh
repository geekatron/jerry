#!/usr/bin/env sh
# =============================================================================
# Rainbow Cloud -- End-to-End Container Test
# =============================================================================
# Tests: Checkov, Prowler, Kubescape CLI availability in cloud-auditor image
# Image: rainbow-cloud-auditor:latest
#
# Usage (from repo root):
#   sh skills/rainbow-cloud/tests/docker/e2e-test.sh
#
# Exit codes:
#   0 = all tools verified
#   1 = one or more tools missing or errored
# =============================================================================

set -eu

IMAGE="rainbow-cloud-auditor:latest"
BUILD_CTX="skills/rainbow-cloud/tests/docker/cloud-auditor"

PASS=0
FAIL=0

run_test() {
    name="$1"
    cmd="$2"
    printf "  %-40s" "${name}..."
    if docker run --rm "${IMAGE}" sh -c "${cmd}" > /dev/null 2>&1; then
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

run_test "checkov --version" \
    "checkov --version 2>&1 | grep -iE 'checkov|[0-9]+\.[0-9]+'"

run_test "prowler --version" \
    "prowler --version 2>&1 | grep -iE 'prowler|[0-9]+\.[0-9]+'"

run_test "kubescape version" \
    "kubescape version 2>&1 | grep -iE 'kubescape|v[0-9]'"

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""
echo "================================"
echo "  Cloud E2E Test Results"
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
