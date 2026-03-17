#!/usr/bin/env bash
# test-tool-exec.sh -- Shell mock test for rainbow-tool-exec (no Docker required)
#
# ADR-PROJ023-001 v1.3.0 -- Behavioral Contract BC-01, BC-03, BC-05
#
# Tested behaviors (mock / no-docker mode):
#   BC-01: RAINBOW_TOOL_MODE=local + known Zone 1 tool -> exit 0
#   BC-05: RAINBOW_TOOL_MODE=local + unknown tool prefix -> exit 1
#   BC-03: RAINBOW_STRICT_MODE=true + RAINBOW_TOOL_MODE unset + Zone 3 tool -> exit 6
#
# Exit codes:
#   0  All tests passed
#   1  One or more tests failed (test harness failure, not wrapper failure)
#
# Prerequisites:
#   - rainbow-tool-exec must be on PATH or RAINBOW_TOOL_EXEC_PATH must be set
#   - skills/rainbow/config/tool-exec.yaml must be present (auto-detected)
#   - No Docker is required; all tests use RAINBOW_TOOL_MODE=local or test
#     strict-mode rejection before any execution reaches docker
#
# Usage:
#   RAINBOW_PROJECT_ROOT=/path/to/repo bash test-tool-exec.sh
#   RAINBOW_TOOL_EXEC_PATH=/path/to/rainbow-tool-exec bash test-tool-exec.sh
#
# Design: each test_* function is self-contained; failures are accumulated and
# reported at the end. The script does not exit on first failure so the full
# result picture is always visible.

set -uo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

readonly SCRIPT_NAME="test-tool-exec.sh"
readonly ADR_REF="ADR-PROJ023-001 BC-01 BC-03 BC-05"

# Locate the wrapper under test. Prefer explicit override, then sibling path.
if [[ -n "${RAINBOW_TOOL_EXEC_PATH:-}" ]]; then
    readonly WRAPPER="${RAINBOW_TOOL_EXEC_PATH}"
else
    # Resolve relative to this script's location: tests/docker/ -> ../../bin/
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    readonly WRAPPER="${SCRIPT_DIR}/../../bin/rainbow-tool-exec"
fi

# ---------------------------------------------------------------------------
# Test result tracking
# ---------------------------------------------------------------------------

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0
FAILED_TESTS=()

pass() {
    local name="$1"
    TESTS_RUN=$(( TESTS_RUN + 1 ))
    TESTS_PASSED=$(( TESTS_PASSED + 1 ))
    echo "[PASS] ${name}"
}

fail() {
    local name="$1"
    local reason="$2"
    TESTS_RUN=$(( TESTS_RUN + 1 ))
    TESTS_FAILED=$(( TESTS_FAILED + 1 ))
    FAILED_TESTS+=("${name}: ${reason}")
    echo "[FAIL] ${name}: ${reason}"
}

# ---------------------------------------------------------------------------
# Pre-flight checks
# ---------------------------------------------------------------------------

preflight_check() {
    echo "--- rainbow-tool-exec shell mock tests (${ADR_REF}) ---"
    echo ""

    if [[ ! -f "${WRAPPER}" ]]; then
        echo "[ERROR] Wrapper not found at: ${WRAPPER}"
        echo "        Set RAINBOW_TOOL_EXEC_PATH to override."
        exit 1
    fi

    if [[ ! -x "${WRAPPER}" ]]; then
        echo "[ERROR] Wrapper is not executable: ${WRAPPER}"
        echo "        Run: chmod +x ${WRAPPER}"
        exit 1
    fi

    echo "Wrapper under test : ${WRAPPER}"
    echo "Working directory  : $(pwd)"
    echo ""
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# run_wrapper: invoke the wrapper with a clean environment overlay.
# Usage: run_wrapper <var-exports> <arg1> [arg2 ...]
# Returns: exit code of the wrapper; stdout+stderr combined in WRAPPER_OUTPUT.
WRAPPER_OUTPUT=""

run_wrapper() {
    # Capture combined output; preserve exit code without set -e killing the test.
    local exit_code=0
    WRAPPER_OUTPUT="$(env "$@" "${WRAPPER}" 2>&1)" || exit_code=$?
    return "${exit_code}"
}

# ---------------------------------------------------------------------------
# BC-01: RAINBOW_TOOL_MODE=local + known Zone 1 tool -> exit 0
#
# "checkov" is a Zone 1 tool in the resolution table (supply-chain local mode).
# In local mode the wrapper attempts to run the tool directly.  On a CI host
# without checkov installed the tool itself exits non-zero (EXIT_TOOL_ERROR=2),
# but the wrapper MUST NOT exit 1 (unknown tool).  We accept exit 0 OR exit 2
# to keep the test Docker-free while still verifying the resolution path.
# ---------------------------------------------------------------------------

test_bc01_known_zone1_tool_local_exit_not_unknown() {
    local name="BC-01: known Zone 1 tool (checkov) in local mode — exit is not 1"

    local exit_code=0
    WRAPPER_OUTPUT="$(
        RAINBOW_TOOL_MODE=local \
        RAINBOW_STRICT_MODE=false \
        RAINBOW_PROJECT_ROOT="${RAINBOW_PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}" \
        "${WRAPPER}" checkov --version 2>&1
    )" || exit_code=$?

    # Exit 1 = unknown tool.  Any other code means resolution succeeded (BC-01).
    if [[ "${exit_code}" -eq 1 ]]; then
        fail "${name}" "wrapper exited 1 (unknown tool); expected tool to resolve in local mode. Output: ${WRAPPER_OUTPUT}"
    else
        pass "${name}"
    fi
}

test_bc01_known_zone1_tool_local_no_docker_invocation() {
    local name="BC-01: local mode does not invoke docker compose exec"

    local exit_code=0
    WRAPPER_OUTPUT="$(
        RAINBOW_TOOL_MODE=local \
        RAINBOW_STRICT_MODE=false \
        RAINBOW_PROJECT_ROOT="${RAINBOW_PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}" \
        "${WRAPPER}" trivy --version 2>&1
    )" || exit_code=$?

    # "docker compose exec" must NOT appear in the wrapper's stderr/stdout
    if echo "${WRAPPER_OUTPUT}" | grep -q "docker compose exec"; then
        fail "${name}" "wrapper output contains 'docker compose exec' in local mode. Output: ${WRAPPER_OUTPUT}"
    else
        pass "${name}"
    fi
}

test_bc01_known_zone2_tool_local_mode() {
    local name="BC-01: known Zone 2 tool (subfinder) in local mode — exit is not 1"

    local exit_code=0
    WRAPPER_OUTPUT="$(
        RAINBOW_TOOL_MODE=local \
        RAINBOW_STRICT_MODE=false \
        RAINBOW_PROJECT_ROOT="${RAINBOW_PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}" \
        "${WRAPPER}" subfinder -h 2>&1
    )" || exit_code=$?

    if [[ "${exit_code}" -eq 1 ]]; then
        fail "${name}" "wrapper exited 1 (unknown tool); subfinder should resolve in local mode. Output: ${WRAPPER_OUTPUT}"
    else
        pass "${name}"
    fi
}

# ---------------------------------------------------------------------------
# BC-05: Unknown tool prefix -> exit 1
# ---------------------------------------------------------------------------

test_bc05_completely_unknown_tool_exits_1() {
    local name="BC-05: completely unknown tool prefix -> exit 1"

    local exit_code=0
    WRAPPER_OUTPUT="$(
        RAINBOW_TOOL_MODE=local \
        RAINBOW_STRICT_MODE=false \
        RAINBOW_PROJECT_ROOT="${RAINBOW_PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}" \
        "${WRAPPER}" notarealtoolxyz --help 2>&1
    )" || exit_code=$?

    if [[ "${exit_code}" -ne 1 ]]; then
        fail "${name}" "expected exit code 1, got ${exit_code}. Output: ${WRAPPER_OUTPUT}"
    else
        pass "${name}"
    fi
}

test_bc05_unknown_tool_emits_error_message() {
    local name="BC-05: unknown tool emits 'Unknown tool prefix' error message"

    local exit_code=0
    WRAPPER_OUTPUT="$(
        RAINBOW_TOOL_MODE=local \
        RAINBOW_STRICT_MODE=false \
        RAINBOW_PROJECT_ROOT="${RAINBOW_PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}" \
        "${WRAPPER}" definitelyfakecli2026 arg1 2>&1
    )" || exit_code=$?

    if ! echo "${WRAPPER_OUTPUT}" | grep -qi "Unknown tool prefix"; then
        fail "${name}" "error message missing 'Unknown tool prefix'. Output: ${WRAPPER_OUTPUT}"
    else
        pass "${name}"
    fi
}

test_bc05_another_unknown_tool_exits_1() {
    local name="BC-05: another unknown tool prefix 'my-custom-scanner' -> exit 1"

    local exit_code=0
    WRAPPER_OUTPUT="$(
        RAINBOW_TOOL_MODE=local \
        RAINBOW_STRICT_MODE=false \
        RAINBOW_PROJECT_ROOT="${RAINBOW_PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}" \
        "${WRAPPER}" my-custom-scanner scan 2>&1
    )" || exit_code=$?

    if [[ "${exit_code}" -ne 1 ]]; then
        fail "${name}" "expected exit code 1, got ${exit_code}. Output: ${WRAPPER_OUTPUT}"
    else
        pass "${name}"
    fi
}

# ---------------------------------------------------------------------------
# BC-03: RAINBOW_STRICT_MODE=true + RAINBOW_TOOL_MODE unset + Zone 3 -> exit 6
# ---------------------------------------------------------------------------

test_bc03_zone3_unset_mode_strict_exits_6() {
    local name="BC-03: Zone 3 tool + unset RAINBOW_TOOL_MODE + strict mode -> exit 6"

    local exit_code=0
    WRAPPER_OUTPUT="$(
        RAINBOW_STRICT_MODE=true \
        RAINBOW_PROJECT_ROOT="${RAINBOW_PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}" \
        "${WRAPPER}" impacket-smbclient --help 2>&1
    )" || exit_code=$?
    # Unset RAINBOW_TOOL_MODE is achieved by not setting it.
    # We rely on the test environment not having RAINBOW_TOOL_MODE set externally.

    if [[ "${exit_code}" -ne 6 ]]; then
        fail "${name}" "expected exit code 6, got ${exit_code}. Output: ${WRAPPER_OUTPUT}"
    else
        pass "${name}"
    fi
}

test_bc03_zone3_unset_mode_strict_emits_error() {
    local name="BC-03: Zone 3 tool strict rejection emits 'RAINBOW_TOOL_MODE' error message"

    local exit_code=0
    WRAPPER_OUTPUT="$(
        RAINBOW_STRICT_MODE=true \
        RAINBOW_PROJECT_ROOT="${RAINBOW_PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}" \
        "${WRAPPER}" impacket-GetADUsers --help 2>&1
    )" || exit_code=$?

    if ! echo "${WRAPPER_OUTPUT}" | grep -q "RAINBOW_TOOL_MODE"; then
        fail "${name}" "error message missing 'RAINBOW_TOOL_MODE'. Output: ${WRAPPER_OUTPUT}"
    else
        pass "${name}"
    fi
}

test_bc03_zone2_unset_mode_strict_exits_6() {
    local name="BC-03: Zone 2 tool + unset RAINBOW_TOOL_MODE + strict mode -> exit 6"

    local exit_code=0
    WRAPPER_OUTPUT="$(
        RAINBOW_STRICT_MODE=true \
        RAINBOW_PROJECT_ROOT="${RAINBOW_PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}" \
        "${WRAPPER}" subfinder -h 2>&1
    )" || exit_code=$?

    if [[ "${exit_code}" -ne 6 ]]; then
        fail "${name}" "expected exit code 6, got ${exit_code}. Output: ${WRAPPER_OUTPUT}"
    else
        pass "${name}"
    fi
}

test_bc03_zone1_unset_mode_strict_does_not_exit_6() {
    local name="BC-03/BC-04: Zone 1 tool + unset RAINBOW_TOOL_MODE + strict mode -> NOT exit 6"

    # Zone 1 tools fall back safely per BC-04; exit 6 is reserved for Zone 2/3.
    local exit_code=0
    WRAPPER_OUTPUT="$(
        RAINBOW_STRICT_MODE=true \
        RAINBOW_PROJECT_ROOT="${RAINBOW_PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}" \
        "${WRAPPER}" checkov --version 2>&1
    )" || exit_code=$?

    if [[ "${exit_code}" -eq 6 ]]; then
        fail "${name}" "Zone 1 tool should NOT exit 6 in strict mode; got exit 6. Output: ${WRAPPER_OUTPUT}"
    else
        pass "${name}"
    fi
}

# Additional boundary check: RAINBOW_TOOL_MODE explicitly set for Zone 3
# should not trigger exit 6 even in strict mode.
test_bc03_zone3_explicit_mode_not_exit_6() {
    local name="BC-03: Zone 3 tool with RAINBOW_TOOL_MODE=local set -> NOT exit 6"

    local exit_code=0
    WRAPPER_OUTPUT="$(
        RAINBOW_TOOL_MODE=local \
        RAINBOW_STRICT_MODE=true \
        RAINBOW_PROJECT_ROOT="${RAINBOW_PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}" \
        "${WRAPPER}" impacket-smbclient --help 2>&1
    )" || exit_code=$?

    if [[ "${exit_code}" -eq 6 ]]; then
        fail "${name}" "explicit RAINBOW_TOOL_MODE=local should not trigger exit 6. Output: ${WRAPPER_OUTPUT}"
    else
        pass "${name}"
    fi
}

# ---------------------------------------------------------------------------
# Strict mode: --no-filter forbidden when RAINBOW_STRICT_MODE=true
# ---------------------------------------------------------------------------

test_strict_mode_no_filter_rejected() {
    local name="Strict mode: --no-filter rejected when RAINBOW_STRICT_MODE=true"

    local exit_code=0
    WRAPPER_OUTPUT="$(
        RAINBOW_TOOL_MODE=local \
        RAINBOW_STRICT_MODE=true \
        RAINBOW_PROJECT_ROOT="${RAINBOW_PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}" \
        "${WRAPPER}" --no-filter checkov --version 2>&1
    )" || exit_code=$?

    if [[ "${exit_code}" -eq 0 ]]; then
        fail "${name}" "expected non-zero exit when --no-filter used in strict mode; got 0. Output: ${WRAPPER_OUTPUT}"
    else
        pass "${name}"
    fi
}

test_strict_mode_no_filter_rejection_message() {
    local name="Strict mode: --no-filter rejection includes 'FORBIDDEN' in message"

    local exit_code=0
    WRAPPER_OUTPUT="$(
        RAINBOW_TOOL_MODE=local \
        RAINBOW_STRICT_MODE=true \
        RAINBOW_PROJECT_ROOT="${RAINBOW_PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}" \
        "${WRAPPER}" --no-filter checkov --version 2>&1
    )" || exit_code=$?

    if ! echo "${WRAPPER_OUTPUT}" | grep -qi "FORBIDDEN"; then
        fail "${name}" "error message missing 'FORBIDDEN'. Output: ${WRAPPER_OUTPUT}"
    else
        pass "${name}"
    fi
}

# ---------------------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------------------

run_all_tests() {
    echo "=== BC-01: local mode resolves known tools ==="
    test_bc01_known_zone1_tool_local_exit_not_unknown
    test_bc01_known_zone1_tool_local_no_docker_invocation
    test_bc01_known_zone2_tool_local_mode
    echo ""

    echo "=== BC-05: unknown tool prefix exits 1 ==="
    test_bc05_completely_unknown_tool_exits_1
    test_bc05_unknown_tool_emits_error_message
    test_bc05_another_unknown_tool_exits_1
    echo ""

    echo "=== BC-03: strict mode rejects Zone 2/3 without explicit RAINBOW_TOOL_MODE ==="
    test_bc03_zone3_unset_mode_strict_exits_6
    test_bc03_zone3_unset_mode_strict_emits_error
    test_bc03_zone2_unset_mode_strict_exits_6
    test_bc03_zone1_unset_mode_strict_does_not_exit_6
    test_bc03_zone3_explicit_mode_not_exit_6
    echo ""

    echo "=== Strict mode: --no-filter prevention ==="
    test_strict_mode_no_filter_rejected
    test_strict_mode_no_filter_rejection_message
    echo ""
}

print_summary() {
    echo "========================================"
    echo " Results: ${TESTS_PASSED}/${TESTS_RUN} passed"
    echo "========================================"

    if [[ "${TESTS_FAILED}" -gt 0 ]]; then
        echo ""
        echo "Failed tests:"
        for t in "${FAILED_TESTS[@]}"; do
            echo "  - ${t}"
        done
        echo ""
        echo "Exit: FAIL (${TESTS_FAILED} test(s) failed)"
        return 1
    else
        echo ""
        echo "Exit: PASS"
        return 0
    fi
}

main() {
    preflight_check

    # RAINBOW_TOOL_MODE must NOT be exported into the BC-03 tests, which rely on
    # it being absent.  Save and unset it so the individual tests control it.
    local saved_mode="${RAINBOW_TOOL_MODE:-}"
    unset RAINBOW_TOOL_MODE 2>/dev/null || true

    run_all_tests

    # Restore original value if it was set before this script ran
    [[ -n "${saved_mode}" ]] && export RAINBOW_TOOL_MODE="${saved_mode}"

    print_summary
}

main "$@"
