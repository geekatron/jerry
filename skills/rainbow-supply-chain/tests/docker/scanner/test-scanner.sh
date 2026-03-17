#!/usr/bin/env bash
# Rainbow Supply Chain Scanner - CLI Validation Test
# Purpose: Verify all scanner tools are installed and functional
# Usage: ./test-scanner.sh
# Exit: 0 = all tools pass, 1 = one or more tools failed

set -euo pipefail

PASS=0
FAIL=0
TOTAL=0

check_tool() {
    local tool_name="$1"
    local version_cmd="$2"
    local help_cmd="$3"
    TOTAL=$((TOTAL + 1))

    echo "--- Testing: ${tool_name} ---"

    # Version check
    echo "  Version:"
    if eval "${version_cmd}" 2>&1; then
        echo "  [PASS] ${tool_name} --version"
    else
        echo "  [FAIL] ${tool_name} --version"
        FAIL=$((FAIL + 1))
        return
    fi

    # Help check
    echo "  Help:"
    if eval "${help_cmd}" >/dev/null 2>&1; then
        echo "  [PASS] ${tool_name} --help"
    else
        echo "  [FAIL] ${tool_name} --help"
        FAIL=$((FAIL + 1))
        return
    fi

    PASS=$((PASS + 1))
}

echo "========================================="
echo "Rainbow SC Scanner - CLI Validation"
echo "========================================="
echo ""

check_tool "Syft" "syft version" "syft --help"
echo ""

check_tool "Grype" "grype version" "grype --help"
echo ""

check_tool "Trivy" "trivy --version" "trivy --help"
echo ""

check_tool "OSV-Scanner" "osv-scanner --version" "osv-scanner --help"
echo ""

check_tool "Checkov" "checkov --version" "checkov --help"
echo ""

echo "========================================="
echo "Results: ${PASS}/${TOTAL} passed, ${FAIL}/${TOTAL} failed"
echo "========================================="

if [ "${FAIL}" -gt 0 ]; then
    echo "FAIL: One or more tools did not pass validation."
    exit 1
else
    echo "PASS: All scanner tools validated successfully."
    exit 0
fi
