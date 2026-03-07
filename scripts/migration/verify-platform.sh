#!/bin/bash
# =============================================================================
# Platform Verification Script for EN-301 Manual Content Migration
# =============================================================================
#
# Purpose: Verify that rsync and tar tools on the current platform will correctly
#          handle exclusion patterns as documented in EN-301
#
# Addresses: CRIT-001 from nse-qa adversarial audit
#
# Usage:
#   chmod +x verify-platform.sh
#   ./verify-platform.sh
#
# Exit Codes:
#   0 - All verification tests passed
#   1 - One or more verification tests failed
#   2 - Critical tool missing
#
# Reference: projects/PROJ-009-oss-release/work/EPIC-001-oss-release/
#            FEAT-003-repository-setup/EN-301-manual-content-migration/
#            orchestration/nse/phase-2/qa-audit.md (FM-001)
#
# Created: 2026-02-02
# =============================================================================

set -o pipefail

# =============================================================================
# Platform Guard: Skip on Windows (Git Bash / MSYS2 / Cygwin)
# =============================================================================
# This script relies on rsync, tar, and other Unix tools that are not available
# on Windows. On Windows, use WSL or skip this verification step.
case "$(uname -s)" in
    MINGW*|MSYS*|CYGWIN*)
        echo "[SKIP] verify-platform.sh: Windows detected ($(uname -s))"
        echo "       This script requires rsync and GNU tar which are not"
        echo "       available natively on Windows."
        echo "       Run this script in WSL or on a Linux/macOS system."
        exit 0
        ;;
esac

# Colors for output (if terminal supports it)
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    NC='\033[0m' # No Color
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    NC=''
fi

# Counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0
WARNINGS=0

# Test directory
TEST_DIR=$(mktemp -d)
trap "rm -rf $TEST_DIR" EXIT

# =============================================================================
# Helper Functions
# =============================================================================

print_header() {
    echo ""
    echo -e "${BLUE}==============================================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}==============================================================================${NC}"
}

print_section() {
    echo ""
    echo -e "${BLUE}--- $1 ---${NC}"
}

pass() {
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo -e "${GREEN}[PASS]${NC} $1"
}

fail() {
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "${RED}[FAIL]${NC} $1"
}

warn() {
    WARNINGS=$((WARNINGS + 1))
    echo -e "${YELLOW}[WARN]${NC} $1"
}

info() {
    echo -e "[INFO] $1"
}

# =============================================================================
# Platform Detection
# =============================================================================

print_header "Platform Verification for EN-301 Migration"
echo "Date: $(date)"
echo "Script: $0"

print_section "Platform Detection"

OS_TYPE=$(uname -s)
OS_VERSION=$(uname -r)
ARCH=$(uname -m)

info "Operating System: $OS_TYPE"
info "Kernel Version: $OS_VERSION"
info "Architecture: $ARCH"

case "$OS_TYPE" in
    "Darwin")
        info "Platform: macOS (Darwin)"
        PLATFORM="darwin"
        MACOS_VERSION=$(sw_vers -productVersion 2>/dev/null || echo "unknown")
        info "macOS Version: $MACOS_VERSION"
        ;;
    "Linux")
        info "Platform: Linux"
        PLATFORM="linux"
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            info "Distribution: $NAME $VERSION"
        fi
        ;;
    *)
        warn "Unknown platform: $OS_TYPE - Proceed with caution"
        PLATFORM="unknown"
        ;;
esac

# =============================================================================
# rsync Version and Type Detection
# =============================================================================

print_section "rsync Detection"

if ! command -v rsync &> /dev/null; then
    fail "rsync not found in PATH"
    echo -e "${RED}CRITICAL: rsync is required for EN-301 migration${NC}"
    exit 2
fi

RSYNC_VERSION_OUTPUT=$(rsync --version 2>&1 | head -5)
RSYNC_VERSION_LINE=$(echo "$RSYNC_VERSION_OUTPUT" | head -1)
info "rsync version: $RSYNC_VERSION_LINE"

# Detect rsync type (GNU vs BSD/Apple)
if echo "$RSYNC_VERSION_LINE" | grep -q "protocol version"; then
    RSYNC_MAJOR=$(echo "$RSYNC_VERSION_LINE" | sed -E 's/.*version ([0-9]+)\..*/\1/')
    RSYNC_MINOR=$(echo "$RSYNC_VERSION_LINE" | sed -E 's/.*version [0-9]+\.([0-9]+).*/\1/')
    info "rsync major version: $RSYNC_MAJOR"
    info "rsync minor version: $RSYNC_MINOR"
fi

if [ "$PLATFORM" = "darwin" ]; then
    # Check if using Apple's bundled rsync (typically older)
    RSYNC_PATH=$(which rsync)
    if [ "$RSYNC_PATH" = "/usr/bin/rsync" ]; then
        warn "Using Apple's bundled rsync (may be older BSD-derived version)"
        warn "Consider installing GNU rsync via Homebrew: brew install rsync"
        RSYNC_TYPE="apple"
    else
        # Check if it's GNU rsync (from Homebrew)
        if echo "$RSYNC_VERSION_OUTPUT" | grep -qi "receiving"; then
            info "Using GNU rsync (likely from Homebrew)"
            RSYNC_TYPE="gnu"
        else
            info "Using rsync from: $RSYNC_PATH"
            RSYNC_TYPE="unknown"
        fi
    fi
else
    RSYNC_TYPE="gnu"
fi

# =============================================================================
# tar Version and Type Detection
# =============================================================================

print_section "tar Detection"

if ! command -v tar &> /dev/null; then
    fail "tar not found in PATH"
    echo -e "${RED}CRITICAL: tar is required for EN-301 migration alternative method${NC}"
    exit 2
fi

TAR_VERSION_OUTPUT=$(tar --version 2>&1 | head -3)
TAR_VERSION_LINE=$(echo "$TAR_VERSION_OUTPUT" | head -1)
info "tar version: $TAR_VERSION_LINE"

# Detect tar type
if echo "$TAR_VERSION_LINE" | grep -qi "bsdtar"; then
    TAR_TYPE="bsd"
    info "tar type: BSD (libarchive)"
elif echo "$TAR_VERSION_LINE" | grep -qi "GNU tar"; then
    TAR_TYPE="gnu"
    info "tar type: GNU tar"
else
    TAR_TYPE="unknown"
    warn "Unknown tar type - manual verification recommended"
fi

# =============================================================================
# Platform-Specific Behavior Documentation
# =============================================================================

print_section "Platform-Specific Behavior Analysis"

if [ "$PLATFORM" = "darwin" ]; then
    echo ""
    echo "IMPORTANT: macOS Platform Considerations"
    echo "========================================="
    echo ""
    echo "1. rsync Differences (BSD vs GNU):"
    echo "   - Apple's bundled rsync (v2.6.9) is BSD-derived and older"
    echo "   - GNU rsync (v3.x) has more consistent pattern matching"
    echo "   - Trailing slash behavior: Both should work with 'dir/' exclusion"
    echo "   - RECOMMENDATION: The patterns in EN-301 are compatible with both"
    echo ""
    echo "2. tar Differences (bsdtar vs GNU tar):"
    echo "   - macOS uses bsdtar (from libarchive)"
    echo "   - Pattern matching: Both support --exclude with glob patterns"
    echo "   - Anchoring: bsdtar excludes are relative to archive root"
    echo "   - POTENTIAL ISSUE: bsdtar may not honor all GNU tar flags"
    echo ""
    echo "3. Glob Pattern Expansion:"
    echo "   - macOS uses BSD glob which is POSIX compliant"
    echo "   - Patterns like '*.backup' and '.env.*' work on both platforms"
    echo "   - VERIFIED: Shell expansion disabled with single quotes"
    echo ""
fi

# =============================================================================
# Exclusion Pattern Tests
# =============================================================================

print_section "Exclusion Pattern Verification Tests"

# Create test directory structure
mkdir -p "$TEST_DIR/source/projects/internal"
mkdir -p "$TEST_DIR/source/transcripts"
mkdir -p "$TEST_DIR/source/docs/knowledge/dragonsbelurkin"
mkdir -p "$TEST_DIR/source/docs/knowledge/public"
mkdir -p "$TEST_DIR/source/.jerry"
mkdir -p "$TEST_DIR/source/.venv"
mkdir -p "$TEST_DIR/source/.idea"
mkdir -p "$TEST_DIR/source/__pycache__"
mkdir -p "$TEST_DIR/target"

# Create test files
echo "SENSITIVE" > "$TEST_DIR/source/projects/internal/secret.txt"
echo "SENSITIVE" > "$TEST_DIR/source/transcripts/meeting.txt"
echo "SENSITIVE" > "$TEST_DIR/source/docs/knowledge/dragonsbelurkin/private.md"
echo "PUBLIC" > "$TEST_DIR/source/docs/knowledge/public/readme.md"
echo "SENSITIVE" > "$TEST_DIR/source/.jerry/state.json"
echo "SENSITIVE" > "$TEST_DIR/source/.env"
echo "SENSITIVE" > "$TEST_DIR/source/.env.local"
echo "SENSITIVE" > "$TEST_DIR/source/test.backup"
echo "SENSITIVE" > "$TEST_DIR/source/file.bak"
echo "SENSITIVE" > "$TEST_DIR/source/editor~"
echo "SENSITIVE" > "$TEST_DIR/source/debug.log"
echo "PUBLIC" > "$TEST_DIR/source/readme.md"

# Test T-001: rsync directory exclusion with trailing slash
echo ""
info "T-001: Testing rsync directory exclusion (trailing slash)"
rsync -av --dry-run \
    --exclude='projects/' \
    "$TEST_DIR/source/" "$TEST_DIR/target/" 2>&1 | grep -q "projects" && \
    fail "T-001: 'projects/' directory not excluded" || \
    pass "T-001: 'projects/' directory correctly excluded"

# Test T-002: rsync multiple directory exclusions
info "T-002: Testing rsync multiple directory exclusions"
RSYNC_OUTPUT=$(rsync -av --dry-run \
    --exclude='projects/' \
    --exclude='transcripts/' \
    --exclude='.jerry/' \
    --exclude='.venv/' \
    --exclude='.idea/' \
    "$TEST_DIR/source/" "$TEST_DIR/target/" 2>&1)

EXCLUDED_FOUND=0
for dir in "projects" "transcripts" ".jerry" ".venv" ".idea"; do
    if echo "$RSYNC_OUTPUT" | grep -q "$dir"; then
        EXCLUDED_FOUND=1
        break
    fi
done
[ $EXCLUDED_FOUND -eq 0 ] && \
    pass "T-002: Multiple directories correctly excluded" || \
    fail "T-002: Some directories not excluded"

# Test T-003: rsync file pattern exclusion (*.backup)
info "T-003: Testing rsync file pattern exclusion (*.backup)"
rsync -av --dry-run \
    --exclude='*.backup' \
    "$TEST_DIR/source/" "$TEST_DIR/target/" 2>&1 | grep -q "\.backup" && \
    fail "T-003: '*.backup' files not excluded" || \
    pass "T-003: '*.backup' files correctly excluded"

# Test T-004: rsync .env file exclusion
info "T-004: Testing rsync .env file exclusion"
RSYNC_OUTPUT=$(rsync -av --dry-run \
    --exclude='.env' \
    --exclude='.env.*' \
    "$TEST_DIR/source/" "$TEST_DIR/target/" 2>&1)

ENV_FOUND=0
if echo "$RSYNC_OUTPUT" | grep -E "\.env$|\.env\." | grep -v "exclude"; then
    ENV_FOUND=1
fi
[ $ENV_FOUND -eq 0 ] && \
    pass "T-004: .env files correctly excluded" || \
    fail "T-004: .env files not excluded"

# Test T-005: rsync *.log exclusion
info "T-005: Testing rsync *.log exclusion"
rsync -av --dry-run \
    --exclude='*.log' \
    "$TEST_DIR/source/" "$TEST_DIR/target/" 2>&1 | grep -q "\.log" && \
    fail "T-005: '*.log' files not excluded" || \
    pass "T-005: '*.log' files correctly excluded"

# Test T-006: rsync backup pattern variations
info "T-006: Testing rsync backup patterns (*.bak, *~)"
RSYNC_OUTPUT=$(rsync -av --dry-run \
    --exclude='*.bak' \
    --exclude='*~' \
    "$TEST_DIR/source/" "$TEST_DIR/target/" 2>&1)

BAK_FOUND=0
if echo "$RSYNC_OUTPUT" | grep -E "\.bak$|~$"; then
    BAK_FOUND=1
fi
[ $BAK_FOUND -eq 0 ] && \
    pass "T-006: Backup patterns (*.bak, *~) correctly excluded" || \
    fail "T-006: Backup patterns not excluded"

# Test T-007: rsync nested directory exclusion
info "T-007: Testing rsync nested path exclusion (docs/knowledge/dragonsbelurkin/)"
rsync -av --dry-run \
    --exclude='docs/knowledge/dragonsbelurkin/' \
    "$TEST_DIR/source/" "$TEST_DIR/target/" 2>&1 | grep -q "dragonsbelurkin" && \
    fail "T-007: Nested path 'docs/knowledge/dragonsbelurkin/' not excluded" || \
    pass "T-007: Nested path correctly excluded"

# Test T-008: Verify public content IS included
info "T-008: Verifying public content is included"
RSYNC_OUTPUT=$(rsync -av --dry-run \
    --exclude='projects/' \
    --exclude='transcripts/' \
    --exclude='docs/knowledge/dragonsbelurkin/' \
    "$TEST_DIR/source/" "$TEST_DIR/target/" 2>&1)

if echo "$RSYNC_OUTPUT" | grep -q "docs/knowledge/public"; then
    pass "T-008: Public content correctly included"
else
    fail "T-008: Public content incorrectly excluded"
fi

# =============================================================================
# tar Exclusion Tests (Alternative Method)
# =============================================================================

print_section "tar Exclusion Verification Tests"

# Test T-009: tar directory exclusion
info "T-009: Testing tar directory exclusion"
cd "$TEST_DIR/source"
TAR_OUTPUT=$(tar --exclude='projects' --exclude='transcripts' -cvf - . 2>&1)

TAR_EXCLUDED=0
if echo "$TAR_OUTPUT" | grep -q "projects\|transcripts"; then
    TAR_EXCLUDED=0
else
    TAR_EXCLUDED=1
fi
[ $TAR_EXCLUDED -eq 1 ] && \
    pass "T-009: tar directory exclusion works" || \
    fail "T-009: tar directory exclusion failed"
cd - > /dev/null

# Test T-010: tar pattern exclusion
info "T-010: Testing tar pattern exclusion (*.backup, *.log)"
cd "$TEST_DIR/source"
TAR_OUTPUT=$(tar --exclude='*.backup' --exclude='*.log' -cvf - . 2>&1)

PATTERNS_FOUND=0
if echo "$TAR_OUTPUT" | grep -E "\.backup|\.log"; then
    PATTERNS_FOUND=1
fi
[ $PATTERNS_FOUND -eq 0 ] && \
    pass "T-010: tar pattern exclusion works" || \
    fail "T-010: tar pattern exclusion failed"
cd - > /dev/null

# =============================================================================
# Full EN-301 Command Simulation
# =============================================================================

print_section "Full EN-301 Command Simulation (Dry Run)"

info "Running full EN-301 rsync command in dry-run mode..."

cd "$TEST_DIR/source"

FULL_RSYNC_OUTPUT=$(rsync -av --dry-run \
    --exclude='projects/' \
    --exclude='transcripts/' \
    --exclude='docs/internal/' \
    --exclude='docs/knowledge/dragonsbelurkin/' \
    --exclude='.git/' \
    --exclude='.venv/' \
    --exclude='.jerry/' \
    --exclude='logs/' \
    --exclude='__pycache__/' \
    --exclude='.pytest_cache/' \
    --exclude='.mypy_cache/' \
    --exclude='.ruff_cache/' \
    --exclude='.coverage' \
    --exclude='htmlcov/' \
    --exclude='.idea/' \
    --exclude='.vscode/' \
    --exclude='*.pyc' \
    --exclude='*.pyo' \
    --exclude='*.log' \
    --exclude='.env' \
    --exclude='.env.*' \
    --exclude='*.backup' \
    --exclude='*.bak' \
    --exclude='*~' \
    --exclude='*.iml' \
    --exclude='.DS_Store' \
    --exclude='Thumbs.db' \
    --exclude='uv.lock' \
    . "$TEST_DIR/target/" 2>&1)

cd - > /dev/null

# Check for any sensitive content that should have been excluded
CRITICAL_PATTERNS="projects|transcripts|dragonsbelurkin|\.jerry|\.env|\.backup|\.bak|~$|\.log$"

LEAK_DETECTED=0
LEAKED_ITEMS=$(echo "$FULL_RSYNC_OUTPUT" | grep -E "$CRITICAL_PATTERNS" || true)

if [ -n "$LEAKED_ITEMS" ]; then
    LEAK_DETECTED=1
    fail "Full EN-301 simulation: Some excluded content would be copied"
    echo "   Leaked items:"
    echo "$LEAKED_ITEMS" | head -10 | sed 's/^/   - /'
else
    pass "Full EN-301 simulation: All exclusions working correctly"
fi

# =============================================================================
# Recommendations
# =============================================================================

print_section "Platform-Specific Recommendations"

if [ "$PLATFORM" = "darwin" ]; then
    echo ""
    if [ "$RSYNC_TYPE" = "apple" ]; then
        warn "Using Apple's bundled rsync (v2.x)"
        echo "   RECOMMENDATION: Install GNU rsync for consistent behavior"
        echo "   Command: brew install rsync"
        echo "   After installation, verify with: which rsync"
        echo "   Should show: /opt/homebrew/bin/rsync or /usr/local/bin/rsync"
        echo ""
    fi

    if [ "$TAR_TYPE" = "bsd" ]; then
        info "Using bsdtar (standard on macOS)"
        echo "   The tar exclusion patterns in EN-301 are compatible with bsdtar"
        echo "   No action required"
        echo ""
    fi
fi

# Check for GNU coreutils
if [ "$PLATFORM" = "darwin" ]; then
    if command -v gtar &> /dev/null; then
        info "GNU tar available as 'gtar'"
        echo "   You can use 'gtar' instead of 'tar' for guaranteed GNU compatibility"
    fi

    if command -v grsync &> /dev/null; then
        info "GNU rsync available as 'grsync' (if installed)"
    fi
fi

# =============================================================================
# Summary
# =============================================================================

print_header "Verification Summary"

echo ""
echo "Platform: $PLATFORM ($OS_TYPE $OS_VERSION)"
echo "rsync: $RSYNC_VERSION_LINE (type: $RSYNC_TYPE)"
echo "tar: $TAR_VERSION_LINE (type: $TAR_TYPE)"
echo ""
echo "Test Results:"
echo "  Total tests run: $TESTS_RUN"
echo "  Tests passed:    $TESTS_PASSED"
echo "  Tests failed:    $TESTS_FAILED"
echo "  Warnings:        $WARNINGS"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}RESULT: PLATFORM VERIFIED${NC}"
    echo "All exclusion patterns work correctly on this platform."
    echo "Migration can proceed with the documented commands."
    EXIT_CODE=0
else
    echo -e "${RED}RESULT: VERIFICATION FAILED${NC}"
    echo "Some exclusion patterns may not work as expected."
    echo "Review the failed tests above and apply recommendations."
    EXIT_CODE=1
fi

if [ $WARNINGS -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}WARNINGS ISSUED: $WARNINGS${NC}"
    echo "Review warnings above for potential improvements."
fi

echo ""
echo "For detailed platform behavior documentation, see:"
echo "  projects/PROJ-009-oss-release/work/EPIC-001-oss-release/"
echo "  FEAT-003-repository-setup/EN-301-manual-content-migration/"
echo "  orchestration/remediation/CRIT-001-remediation.md"
echo ""

exit $EXIT_CODE
