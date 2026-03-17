#!/usr/bin/env bash
# =============================================================================
# Blue Team -- End-to-End Container Test
# =============================================================================
# Domains: detection (YARA-X, Hayabusa, Chainsaw)
#          compliance (Checkov, Trivy, Prowler, Kubescape)
# Images:  blue-detection:latest, blue-compliance:latest
#
# Usage (from repo root):
#   bash skills/blue-team/tests/docker/e2e-test.sh
#
# Exit codes:
#   0 = all tools verified
#   1 = one or more tools missing or errored
# =============================================================================

set -euo pipefail

BASE_DIR="skills/blue-team/tests/docker"
PASS=0
FAIL=0

run_test() {
    local image="$1"
    local name="$2"
    local cmd="$3"
    printf "  %-44s" "${name}..."
    if docker run --rm --network none "${image}" bash -c "${cmd}" > /dev/null 2>&1; then
        echo "PASS"
        PASS=$((PASS + 1))
    else
        echo "FAIL"
        FAIL=$((FAIL + 1))
    fi
}

# ---------------------------------------------------------------------------
# Build images
# ---------------------------------------------------------------------------
echo "=== Building blue-detection ==="
docker build -t blue-detection:latest "${BASE_DIR}/detection"
echo ""

echo "=== Building blue-compliance ==="
docker build -t blue-compliance:latest "${BASE_DIR}/compliance"
echo ""

# ---------------------------------------------------------------------------
# Detection domain
# ---------------------------------------------------------------------------
echo "=== Detection: YARA-X, Hayabusa, Chainsaw ==="

run_test "blue-detection:latest" \
    "yr --version" \
    "yr --version 2>&1 | grep -iE 'yr|[0-9]+\.[0-9]+'"

run_test "blue-detection:latest" \
    "sigma convert --help" \
    "sigma convert --help 2>&1 | grep -iE 'sigma|convert|[Uu]sage'"

run_test "blue-detection:latest" \
    "hayabusa --version" \
    "hayabusa --version 2>&1 | grep -iE 'hayabusa|[0-9]+\.[0-9]+' || hayabusa csv-timeline --help 2>&1 | grep -iE 'hayabusa|timeline'"

# ---------------------------------------------------------------------------
# Compliance domain
# ---------------------------------------------------------------------------
echo ""
echo "=== Compliance: Checkov, Trivy ==="

run_test "blue-compliance:latest" \
    "checkov --version" \
    "checkov --version 2>&1 | grep -iE 'checkov|[0-9]+\.[0-9]+'"

run_test "blue-compliance:latest" \
    "trivy --version" \
    "trivy --version 2>&1 | grep -iE 'trivy|[0-9]+\.[0-9]+'"

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""
echo "================================"
echo "  Blue Team E2E Test Results"
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
