#!/usr/bin/env bash
# Test script for blue-team compliance container tooling
# Tests: Checkov, Trivy, Prowler, Kubescape, kube-bench, OpenSCAP, Cosign
# Container: skills/blue-team/tests/docker/compliance/Dockerfile
# Exit on first failure for CI integration
set -euo pipefail

PASS=0
FAIL=0
SKIP=0

log_pass() { echo "[PASS] $1"; ((PASS++)); }
log_fail() { echo "[FAIL] $1"; ((FAIL++)); }
log_skip() { echo "[SKIP] $1"; ((SKIP++)); }

echo "========================================"
echo "Blue Team Compliance Container Test Suite"
echo "========================================"
echo ""

# --- T1: Checkov CLI availability ---
echo "--- Checkov ---"
if command -v checkov &>/dev/null; then
    CHECKOV_VERSION=$(checkov --version 2>&1 | head -1)
    log_pass "Checkov found: ${CHECKOV_VERSION}"
else
    log_fail "Checkov not found in PATH"
fi

# T2: Checkov can scan a minimal Terraform file
CHECKOV_TMP=$(mktemp -d)
cat > "${CHECKOV_TMP}/main.tf" <<'EOF'
resource "aws_s3_bucket" "test" {
  bucket = "test-bucket"
}
EOF
if checkov -f "${CHECKOV_TMP}/main.tf" --output json --quiet 2>/dev/null | head -1 | grep -q '{'; then
    log_pass "Checkov can scan Terraform and produce JSON"
else
    log_fail "Checkov JSON scan failed"
fi
rm -rf "${CHECKOV_TMP}"

# --- T3: Trivy CLI availability ---
echo ""
echo "--- Trivy ---"
if command -v trivy &>/dev/null; then
    TRIVY_VERSION=$(trivy --version 2>&1 | head -1)
    log_pass "Trivy found: ${TRIVY_VERSION}"
else
    log_fail "Trivy not found in PATH"
fi

# T4: Trivy config scan mode
TRIVY_TMP=$(mktemp -d)
cat > "${TRIVY_TMP}/Dockerfile" <<'EOF'
FROM ubuntu:latest
RUN apt-get update
EOF
if trivy config "${TRIVY_TMP}" -f json --quiet 2>/dev/null | head -1 | grep -q '{'; then
    log_pass "Trivy config scan produces JSON output"
else
    log_skip "Trivy config scan (may require DB download)"
fi
rm -rf "${TRIVY_TMP}"

# --- T5: Prowler CLI availability ---
echo ""
echo "--- Prowler ---"
if command -v prowler &>/dev/null; then
    PROWLER_VERSION=$(prowler --version 2>&1 | head -1)
    log_pass "Prowler found: ${PROWLER_VERSION}"
elif python3 -c "import prowler" 2>/dev/null; then
    log_pass "Prowler importable as Python module"
else
    log_fail "Prowler not found in PATH or as Python module"
fi

# T6: Prowler help (does not require cloud credentials)
if prowler --help &>/dev/null; then
    log_pass "Prowler --help executes successfully"
else
    log_skip "Prowler --help (may not be installed as CLI)"
fi

# --- T7: Kubescape CLI availability ---
echo ""
echo "--- Kubescape ---"
if command -v kubescape &>/dev/null; then
    KUBESCAPE_VERSION=$(kubescape version 2>&1 | head -1)
    log_pass "Kubescape found: ${KUBESCAPE_VERSION}"
else
    log_fail "Kubescape not found in PATH"
fi

# T8: Kubescape can list frameworks
if kubescape list frameworks 2>/dev/null | grep -qi "nsa\|mitre\|cis"; then
    log_pass "Kubescape can list frameworks (NSA/MITRE/CIS present)"
else
    log_skip "Kubescape framework listing (may require download)"
fi

# --- T9: kube-bench CLI availability ---
echo ""
echo "--- kube-bench ---"
if command -v kube-bench &>/dev/null; then
    KUBEBENCH_VERSION=$(kube-bench version 2>&1 | head -1)
    log_pass "kube-bench found: ${KUBEBENCH_VERSION}"
else
    log_fail "kube-bench not found in PATH"
fi

# T10: kube-bench help
if kube-bench --help &>/dev/null; then
    log_pass "kube-bench --help executes successfully"
else
    log_fail "kube-bench --help failed"
fi

# --- T11: OpenSCAP CLI availability ---
echo ""
echo "--- OpenSCAP ---"
if command -v oscap &>/dev/null; then
    OSCAP_VERSION=$(oscap --version 2>&1 | head -1)
    log_pass "oscap found: ${OSCAP_VERSION}"
else
    log_fail "oscap not found in PATH"
fi

# T12: OpenSCAP can show version info
if oscap --version &>/dev/null; then
    log_pass "oscap --version executes successfully"
else
    log_fail "oscap --version failed"
fi

# --- T13: Cosign CLI availability ---
echo ""
echo "--- Cosign ---"
if command -v cosign &>/dev/null; then
    COSIGN_VERSION=$(cosign version 2>&1 | grep -i "version" | head -1)
    log_pass "Cosign found: ${COSIGN_VERSION}"
else
    log_fail "Cosign not found in PATH"
fi

# T14: Cosign verify subcommand exists (does not require image)
if cosign verify --help &>/dev/null; then
    log_pass "Cosign verify subcommand available"
else
    log_fail "Cosign verify subcommand not available"
fi

# T15: Cosign tree subcommand exists
if cosign tree --help &>/dev/null; then
    log_pass "Cosign tree subcommand available"
else
    log_skip "Cosign tree subcommand (may not be available in all versions)"
fi

# --- Summary ---
echo ""
echo "========================================"
echo "Test Summary"
echo "========================================"
echo "PASS: ${PASS}"
echo "FAIL: ${FAIL}"
echo "SKIP: ${SKIP}"
echo "TOTAL: $((PASS + FAIL + SKIP))"
echo ""

if [ "${FAIL}" -gt 0 ]; then
    echo "STATUS: FAILED (${FAIL} failures)"
    exit 1
else
    echo "STATUS: PASSED"
    exit 0
fi
