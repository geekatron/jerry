#!/usr/bin/env bash
# Test script for blue-team threat intelligence container tooling
# Tests: PyMISP import, python-stix2 import, taxii2-client import
# Container: skills/blue-team/tests/docker/intel/Dockerfile
# Exit on first failure for CI integration
set -euo pipefail

PASS=0
FAIL=0
SKIP=0

log_pass() { echo "[PASS] $1"; ((PASS++)); }
log_fail() { echo "[FAIL] $1"; ((FAIL++)); }
log_skip() { echo "[SKIP] $1"; ((SKIP++)); }

echo "========================================"
echo "Blue Team Threat Intel Container Test Suite"
echo "========================================"
echo ""

# Detect Python command (uv run preferred, fallback to python3)
if command -v uv &>/dev/null; then
    PY="uv run python"
elif command -v python3 &>/dev/null; then
    PY="python3"
else
    echo "[FATAL] No Python runtime found"
    exit 1
fi

echo "Using Python: ${PY}"
echo ""

# --- T1: PyMISP import ---
echo "--- PyMISP ---"
if ${PY} -c "import pymisp; print(f'PyMISP version: {pymisp.__version__}')" 2>/dev/null; then
    log_pass "PyMISP importable"
else
    log_fail "PyMISP import failed"
fi

# T2: PyMISP core classes available
if ${PY} -c "from pymisp import PyMISP, MISPEvent, MISPAttribute, MISPObject; print('Core classes: PyMISP, MISPEvent, MISPAttribute, MISPObject')" 2>/dev/null; then
    log_pass "PyMISP core classes available (PyMISP, MISPEvent, MISPAttribute, MISPObject)"
else
    log_fail "PyMISP core classes not available"
fi

# --- T3: python-stix2 import ---
echo ""
echo "--- python-stix2 ---"
if ${PY} -c "import stix2; print(f'stix2 version: {stix2.__version__}')" 2>/dev/null; then
    log_pass "stix2 importable"
else
    log_fail "stix2 import failed"
fi

# T4: STIX 2.1 SDO/SRO creation
if ${PY} -c "
from stix2 import Indicator, Bundle, ThreatActor, Malware, Relationship
ind = Indicator(
    name='Test Indicator',
    pattern=\"[ipv4-addr:value = '198.51.100.1']\",
    pattern_type='stix',
    valid_from='2026-01-01T00:00:00Z'
)
ta = ThreatActor(name='Test Actor')
mal = Malware(name='Test Malware', is_family=False)
rel = Relationship(source_ref=ta.id, relationship_type='uses', target_ref=mal.id)
bundle = Bundle(objects=[ind, ta, mal, rel])
assert bundle.type == 'bundle'
assert len(bundle.objects) == 4
print(f'STIX 2.1 bundle created: {len(bundle.objects)} objects')
" 2>/dev/null; then
    log_pass "STIX 2.1 SDO/SRO/Bundle creation works"
else
    log_fail "STIX 2.1 object creation failed"
fi

# T5: STIX 2.1 serialization
if ${PY} -c "
from stix2 import Indicator
import json
ind = Indicator(
    name='Serialize Test',
    pattern=\"[domain-name:value = 'example.com']\",
    pattern_type='stix',
    valid_from='2026-01-01T00:00:00Z'
)
serialized = ind.serialize()
parsed = json.loads(serialized)
assert parsed['type'] == 'indicator'
assert parsed['spec_version'] == '2.1'
print(f'Serialization OK: type={parsed[\"type\"]}, spec={parsed[\"spec_version\"]}')
" 2>/dev/null; then
    log_pass "STIX 2.1 serialization to JSON works"
else
    log_fail "STIX 2.1 serialization failed"
fi

# --- T6: taxii2-client import ---
echo ""
echo "--- taxii2-client ---"
if ${PY} -c "import taxii2client; print('taxii2client importable')" 2>/dev/null; then
    log_pass "taxii2client importable"
else
    log_fail "taxii2client import failed"
fi

# T7: TAXII v20 and v21 module availability
if ${PY} -c "
from taxii2client.v20 import Server as Server20
from taxii2client.v21 import Server as Server21
print('TAXII v20 and v21 modules available')
" 2>/dev/null; then
    log_pass "TAXII v20 and v21 client modules available"
else
    log_fail "TAXII v20/v21 modules not available"
fi

# T8: TAXII Collection class available
if ${PY} -c "
from taxii2client.v21 import Collection
print('Collection class available for TAXII feed consumption')
" 2>/dev/null; then
    log_pass "TAXII Collection class available"
else
    log_fail "TAXII Collection class not available"
fi

# --- T9: Cross-library integration ---
echo ""
echo "--- Cross-Library Integration ---"
if ${PY} -c "
from stix2 import Indicator, Bundle
from pymisp import MISPEvent, MISPAttribute
# Verify both libraries can coexist and produce compatible data
ind = Indicator(
    name='Cross-lib Test',
    pattern=\"[file:hashes.md5 = 'd41d8cd98f00b204e9800998ecf8427e']\",
    pattern_type='stix',
    valid_from='2026-01-01T00:00:00Z'
)
event = MISPEvent()
event.info = 'Cross-library integration test'
attr = MISPAttribute()
attr.type = 'md5'
attr.value = 'd41d8cd98f00b204e9800998ecf8427e'
print('Cross-library integration: stix2 + pymisp coexist')
" 2>/dev/null; then
    log_pass "stix2 and PyMISP cross-library integration works"
else
    log_fail "Cross-library integration failed"
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
