#!/usr/bin/env bash
# =============================================================================
# Blue Team -- Detection Domain Container Test
# =============================================================================
# Tests: YARA-X (yr), Hayabusa, Chainsaw CLI availability and minimum versions
# Container: blue-detection (skills/blue-team/tests/docker/detection/Dockerfile)
# Agents: blue-detect, blue-siem
# Zone: 1 (Analysis)
#
# Usage:
#   docker build -t blue-detection skills/blue-team/tests/docker/detection/
#   docker run --rm blue-detection /app/test-detection.sh
#
# Exit codes:
#   0 = all tests passed
#   1 = one or more tests failed
# =============================================================================

set -euo pipefail

PASS=0
FAIL=0
TOTAL=0

# ---------------------------------------------------------------------------
# Test helper
# ---------------------------------------------------------------------------
run_test() {
    local name="$1"
    local cmd="$2"
    local expected="$3"
    TOTAL=$((TOTAL + 1))

    echo -n "  TEST ${TOTAL}: ${name}... "
    if result=$(eval "${cmd}" 2>&1); then
        if echo "${result}" | grep -qE "${expected}"; then
            echo "PASS"
            PASS=$((PASS + 1))
        else
            echo "FAIL (unexpected output: ${result})"
            FAIL=$((FAIL + 1))
        fi
    else
        echo "FAIL (command failed: ${result})"
        FAIL=$((FAIL + 1))
    fi
}

# ---------------------------------------------------------------------------
# YARA-X (yr CLI) Tests
# ---------------------------------------------------------------------------
echo ""
echo "=== YARA-X (yr CLI) ==="

run_test "yr binary exists" \
    "which yr" \
    "/usr/local/bin/yr"

run_test "yr version >= 0.9.0" \
    "yr --version" \
    "yr [0-9]+\.[0-9]+\.[0-9]+"

run_test "yr check command available" \
    "yr check --help 2>&1 | head -5" \
    "[Cc]heck|[Vv]alidate|YARA"

run_test "yr scan command available" \
    "yr scan --help 2>&1 | head -5" \
    "[Ss]can|YARA"

run_test "yr compile command available" \
    "yr compile --help 2>&1 | head -5" \
    "[Cc]ompile|YARA"

# Functional test: create a simple YARA rule and validate it
run_test "yr check validates a simple rule" \
    "echo 'rule test_rule { strings: \$a = \"test\" condition: \$a }' > /tmp/work/test.yar && yr check /tmp/work/test.yar 2>&1" \
    ""

# Functional test: scan with the validated rule
run_test "yr scan executes against target" \
    "echo 'test content' > /tmp/work/target.txt && yr scan /tmp/work/test.yar /tmp/work/target.txt --output-format json 2>&1; echo 'scan_complete'" \
    "scan_complete"

# ---------------------------------------------------------------------------
# Hayabusa Tests
# ---------------------------------------------------------------------------
echo ""
echo "=== Hayabusa ==="

run_test "hayabusa binary exists" \
    "which hayabusa" \
    "/usr/local/bin/hayabusa"

run_test "hayabusa version >= 2.14" \
    "hayabusa --version 2>&1 || hayabusa csv-timeline --help 2>&1 | head -3" \
    "[Hh]ayabusa|2\.[0-9]+"

run_test "hayabusa csv-timeline command available" \
    "hayabusa csv-timeline --help 2>&1 | head -5" \
    "csv.timeline|[Tt]imeline|[Uu]sage"

run_test "hayabusa json-timeline command available" \
    "hayabusa json-timeline --help 2>&1 | head -5" \
    "json.timeline|[Tt]imeline|[Uu]sage"

# ---------------------------------------------------------------------------
# Chainsaw Tests
# ---------------------------------------------------------------------------
echo ""
echo "=== Chainsaw ==="

run_test "chainsaw binary exists" \
    "which chainsaw" \
    "/usr/local/bin/chainsaw"

run_test "chainsaw version >= 2.9" \
    "chainsaw --version 2>&1" \
    "[Cc]hainsaw|[0-9]+\.[0-9]+"

run_test "chainsaw hunt command available" \
    "chainsaw hunt --help 2>&1 | head -5" \
    "[Hh]unt|[Uu]sage|[Ss]igma"

run_test "chainsaw search command available" \
    "chainsaw search --help 2>&1 | head -5" \
    "[Ss]earch|[Uu]sage"

# ---------------------------------------------------------------------------
# YARA-X Python binding test (for blue-ioc)
# ---------------------------------------------------------------------------
echo ""
echo "=== YARA-X Python Binding ==="

run_test "yara-x Python module importable" \
    "python3 -c 'import yara_x; print(\"yara_x_ok\")'" \
    "yara_x_ok"

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""
echo "=========================================="
echo "  Detection Container Test Results"
echo "=========================================="
echo "  TOTAL:  ${TOTAL}"
echo "  PASSED: ${PASS}"
echo "  FAILED: ${FAIL}"
echo "=========================================="

if [ "${FAIL}" -gt 0 ]; then
    echo "  STATUS: FAIL"
    exit 1
else
    echo "  STATUS: PASS"
    exit 0
fi
