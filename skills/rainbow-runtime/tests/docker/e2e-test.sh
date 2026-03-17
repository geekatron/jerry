#!/usr/bin/env bash
# e2e-test.sh -- Build, smoke-test, and tear down rainbow-runtime containers.
# Zone 2/3 boundary: mitmproxy and frida are tested independently.
# Exit 0 on all checks passing; exit 1 on any failure.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="${SCRIPT_DIR}/docker-compose.yml"
PASS=0
FAIL=0

log()  { echo "[e2e] $*"; }
pass() { log "PASS: $*"; PASS=$((PASS + 1)); }
fail() { log "FAIL: $*"; FAIL=$((FAIL + 1)); }

cleanup() {
  log "Tearing down containers..."
  docker compose -f "${COMPOSE_FILE}" down --volumes --remove-orphans 2>/dev/null || true
}
trap cleanup EXIT

# ── Build ──────────────────────────────────────────────────────────────────────
log "Building all images..."
docker compose -f "${COMPOSE_FILE}" build --pull

# ── mitmproxy: version check ───────────────────────────────────────────────────
log "Checking mitmproxy version..."
if docker compose -f "${COMPOSE_FILE}" run --rm --no-deps --entrypoint mitmproxy \
    mitmproxy --version 2>&1 | grep -qi "mitmproxy"; then
  pass "mitmproxy --version succeeded"
else
  fail "mitmproxy --version failed"
fi

# ── frida: version check ───────────────────────────────────────────────────────
log "Checking frida version..."
if docker compose -f "${COMPOSE_FILE}" run --rm --no-deps --entrypoint frida \
    frida --version 2>&1 | grep -qE "^[0-9]+\.[0-9]+"; then
  pass "frida --version succeeded"
else
  fail "frida --version failed"
fi

# ── Summary ───────────────────────────────────────────────────────────────────
log "Results: ${PASS} passed, ${FAIL} failed"
if [ "${FAIL}" -gt 0 ]; then
  exit 1
fi
exit 0
