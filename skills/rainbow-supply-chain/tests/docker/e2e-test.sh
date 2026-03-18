#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FAIL=0

echo "=== Building supply-chain containers ==="
docker compose -f "$SCRIPT_DIR/docker-compose.yml" build

echo "=== Testing scanner (Syft + Grype + Trivy) ==="
docker compose -f "$SCRIPT_DIR/docker-compose.yml" run --rm scanner syft version || { echo "FAIL: syft"; FAIL=1; }
docker compose -f "$SCRIPT_DIR/docker-compose.yml" run --rm scanner grype version || { echo "FAIL: grype"; FAIL=1; }
docker compose -f "$SCRIPT_DIR/docker-compose.yml" run --rm scanner trivy version || { echo "FAIL: trivy"; FAIL=1; }

echo "=== Testing verifier (Cosign) ==="
docker compose -f "$SCRIPT_DIR/docker-compose.yml" run --rm verifier cosign version || { echo "FAIL: cosign"; FAIL=1; }

echo "=== Teardown ==="
docker compose -f "$SCRIPT_DIR/docker-compose.yml" down --rmi local 2>/dev/null || true

if [ $FAIL -eq 0 ]; then
  echo "ALL PASS: supply-chain E2E"
else
  echo "FAIL: $FAIL tool(s) failed"
fi
exit $FAIL
