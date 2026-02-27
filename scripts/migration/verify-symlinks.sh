#!/usr/bin/env bash
#
# verify-symlinks.sh - Symlink Verification Script for EN-301 Migration
#
# PURPOSE:
#   Verifies that no symbolic links in the source repository point to
#   excluded content, which could bypass migration exclusions.
#
# FINDING ADDRESSED:
#   CRIT-004 from nse-qa adversarial audit: "No Symlink Verification"
#   IR-002 says "preserve all symbolic links" but no verification exists
#   to ensure symlinks don't point to excluded content.
#
# USAGE:
#   ./scripts/migration/verify-symlinks.sh [OPTIONS] [SOURCE_DIR]
#
# OPTIONS:
#   -h, --help        Show this help message
#   -v, --verbose     Show detailed output for each symlink
#   -q, --quiet       Only show errors (exit code indicates result)
#   --pre-migration   Run pre-migration checks (source directory)
#   --post-migration  Run post-migration checks (target directory)
#
# EXAMPLES:
#   # Pre-migration check (default)
#   ./scripts/migration/verify-symlinks.sh /path/to/source-repo
#
#   # Post-migration check on target
#   ./scripts/migration/verify-symlinks.sh --post-migration /path/to/target-repo
#
#   # Verbose output
#   ./scripts/migration/verify-symlinks.sh -v /path/to/source-repo
#
# EXIT CODES:
#   0 - All symlinks are safe (or no symlinks found)
#   1 - Dangerous symlinks found pointing to excluded content
#   2 - Broken symlinks found (warning, not blocking)
#   3 - Invalid arguments or usage error
#
# AUTHOR: Claude (CRIT-004 remediation)
# DATE: 2026-02-02
# VERSION: 1.0.0

set -euo pipefail

# ============================================================================
# CONFIGURATION
# ============================================================================

# Excluded directories - symlinks pointing to these are DANGEROUS
readonly EXCLUDED_DIRS=(
    "projects"
    "transcripts"
    "docs/knowledge/dragonsbelurkin"
    "docs/internal"
    ".jerry"
    ".venv"
    ".git"
)

# Excluded patterns for post-migration check
readonly EXCLUDED_PATTERNS=(
    "projects/"
    "transcripts/"
    "dragonsbelurkin/"
    ".jerry/"
    ".env"
)

# Default source directory (relative to script or absolute)
DEFAULT_SOURCE_DIR="."

# ============================================================================
# GLOBALS
# ============================================================================

VERBOSE=false
QUIET=false
MODE="pre-migration"
SOURCE_DIR=""
DANGEROUS_COUNT=0
BROKEN_COUNT=0
SAFE_COUNT=0
TOTAL_COUNT=0

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

usage() {
    head -52 "$0" | tail -50 | sed 's/^#//' | sed 's/^ //'
    exit 3
}

log_info() {
    if [[ "$QUIET" != true ]]; then
        echo "[INFO] $*"
    fi
}

log_warn() {
    echo "[WARN] $*" >&2
}

log_error() {
    echo "[ERROR] $*" >&2
}

log_danger() {
    echo "[DANGER] $*" >&2
}

log_verbose() {
    if [[ "$VERBOSE" == true ]]; then
        echo "[DEBUG] $*"
    fi
}

# Portable realpath implementation for macOS/BSD
# Priority: greadlink (GNU coreutils) > uv run python > basic readlink
realpath_portable() {
    local path="$1"
    local resolved

    # Priority 1: GNU readlink (fastest, most reliable)
    # Available via: brew install coreutils
    if command -v greadlink &>/dev/null; then
        resolved=$(greadlink -f "$path" 2>/dev/null) && {
            echo "$resolved"
            return 0
        }
    fi

    # Priority 2: uv-managed Python (project-consistent)
    # Uses the project's managed Python via uv
    if command -v uv &>/dev/null; then
        resolved=$(uv run python -c "import os,sys; print(os.path.realpath(sys.argv[1]))" "$path" 2>/dev/null) && {
            echo "$resolved"
            return 0
        }
    fi

    # Priority 3: Basic readlink (may not fully resolve nested symlinks)
    # This is a degraded fallback - works for simple cases
    if command -v readlink &>/dev/null; then
        resolved=$(readlink "$path" 2>/dev/null)
        if [[ -n "$resolved" ]]; then
            # If relative, make absolute
            if [[ "$resolved" != /* ]]; then
                resolved="$(cd "$(dirname "$path")" && pwd)/$resolved"
            fi
            echo "$resolved"
            return 0
        fi
    fi

    # Fallback: return original path if it exists, otherwise fail
    if [[ -e "$path" ]]; then
        # Use pwd to get canonical path if possible
        if [[ -d "$path" ]]; then
            (cd "$path" && pwd)
        else
            echo "$path"
        fi
        return 0
    fi

    log_error "Cannot resolve path: $path"
    log_error "Install GNU coreutils (brew install coreutils) or ensure uv is available"
    return 1
}

log_result() {
    local status="$1"
    local symlink="$2"
    local target="$3"

    if [[ "$QUIET" == true ]] && [[ "$status" == "SAFE" ]]; then
        return
    fi

    case "$status" in
        SAFE)
            [[ "$VERBOSE" == true ]] && echo "[SAFE] $symlink -> $target"
            ;;
        DANGEROUS)
            echo "[DANGEROUS] $symlink -> $target"
            ;;
        BROKEN)
            echo "[BROKEN] $symlink -> $target (target does not exist)"
            ;;
        EXTERNAL)
            echo "[EXTERNAL] $symlink -> $target (points outside source tree)"
            ;;
    esac
}

# ============================================================================
# SYMLINK ANALYSIS FUNCTIONS
# ============================================================================

# Check if a path matches any excluded directory
is_excluded_path() {
    local path="$1"
    local excluded

    for excluded in "${EXCLUDED_DIRS[@]}"; do
        # Check if path starts with excluded directory or contains it
        if [[ "$path" == "$excluded"* ]] || [[ "$path" == *"/$excluded"* ]]; then
            return 0  # Is excluded
        fi
    done

    return 1  # Not excluded
}

# Get the real (resolved) path of a symlink target
resolve_symlink() {
    local symlink="$1"
    local target

    # Try to resolve the symlink using portable method
    if command -v readlink &>/dev/null; then
        if [[ "$(uname)" == "Darwin" ]]; then
            # Use portable realpath for macOS (greadlink > uv > basic readlink)
            target=$(realpath_portable "$symlink" 2>/dev/null) || true
        else
            # GNU readlink available on Linux
            target=$(readlink -f "$symlink" 2>/dev/null) || true
        fi
    fi

    # Fallback: just read the link
    if [[ -z "$target" ]]; then
        target=$(readlink "$symlink" 2>/dev/null) || true
    fi

    echo "$target"
}

# Check if target is within the source directory tree
is_within_tree() {
    local symlink_dir="$1"
    local target="$2"
    local source_real

    # Get real path of source directory using portable method
    if [[ "$(uname)" == "Darwin" ]]; then
        source_real=$(realpath_portable "$SOURCE_DIR" 2>/dev/null) || source_real="$SOURCE_DIR"
    else
        source_real=$(readlink -f "$SOURCE_DIR" 2>/dev/null) || source_real="$SOURCE_DIR"
    fi

    # Check if target starts with source directory
    if [[ "$target" == "$source_real"* ]]; then
        return 0  # Within tree
    fi

    return 1  # Outside tree
}

# Analyze a single symlink
analyze_symlink() {
    local symlink="$1"
    local resolved_target
    local relative_target

    ((TOTAL_COUNT++))

    log_verbose "Analyzing: $symlink"

    # Resolve the symlink target
    resolved_target=$(resolve_symlink "$symlink")

    if [[ -z "$resolved_target" ]]; then
        log_verbose "  Could not resolve target"
        ((BROKEN_COUNT++))
        log_result "BROKEN" "$symlink" "(unresolvable)"
        return 2
    fi

    log_verbose "  Resolved to: $resolved_target"

    # Check if target exists
    if [[ ! -e "$resolved_target" ]]; then
        ((BROKEN_COUNT++))
        log_result "BROKEN" "$symlink" "$resolved_target"
        return 2
    fi

    # Get relative path from source directory
    relative_target="${resolved_target#$SOURCE_DIR/}"
    log_verbose "  Relative path: $relative_target"

    # Check if target is outside the source tree (post-migration concern)
    if ! is_within_tree "$(dirname "$symlink")" "$resolved_target"; then
        if [[ "$MODE" == "post-migration" ]]; then
            # In post-migration mode, external symlinks are dangerous
            ((DANGEROUS_COUNT++))
            log_result "EXTERNAL" "$symlink" "$resolved_target"
            return 1
        else
            # In pre-migration mode, external symlinks are a warning
            log_verbose "  External symlink (outside source tree)"
        fi
    fi

    # Check if target points to excluded content
    if is_excluded_path "$relative_target"; then
        ((DANGEROUS_COUNT++))
        log_result "DANGEROUS" "$symlink" "$resolved_target"
        log_danger "  REASON: Points to excluded content ($relative_target)"
        return 1
    fi

    # Check raw symlink target (in case it's a relative path to excluded content)
    local raw_target
    raw_target=$(readlink "$symlink" 2>/dev/null) || raw_target=""
    if [[ -n "$raw_target" ]] && is_excluded_path "$raw_target"; then
        ((DANGEROUS_COUNT++))
        log_result "DANGEROUS" "$symlink" "$raw_target"
        log_danger "  REASON: Relative link to excluded content ($raw_target)"
        return 1
    fi

    # Symlink is safe
    ((SAFE_COUNT++))
    log_result "SAFE" "$symlink" "$resolved_target"
    return 0
}

# ============================================================================
# MAIN SCAN FUNCTIONS
# ============================================================================

# Find all symlinks in the source directory (excluding .venv and .git)
find_symlinks() {
    local dir="$1"

    find "$dir" -type l \
        -not -path "*/.venv/*" \
        -not -path "*/.git/*" \
        -not -path "*/__pycache__/*" \
        -not -path "*/.pytest_cache/*" \
        -not -path "*/.mypy_cache/*" \
        -not -path "*/.ruff_cache/*" \
        2>/dev/null || true
}

# Run pre-migration verification
run_pre_migration() {
    log_info "Running PRE-MIGRATION symlink verification..."
    log_info "Source directory: $SOURCE_DIR"
    log_info ""

    local symlinks
    symlinks=$(find_symlinks "$SOURCE_DIR")

    if [[ -z "$symlinks" ]]; then
        log_info "No symbolic links found outside of excluded directories."
        log_info ""
        log_info "RESULT: PASS - No symlinks to verify"
        return 0
    fi

    log_info "Analyzing symlinks..."
    log_info ""

    while IFS= read -r symlink; do
        analyze_symlink "$symlink" || true
    done <<< "$symlinks"

    print_summary
}

# Run post-migration verification
run_post_migration() {
    log_info "Running POST-MIGRATION symlink verification..."
    log_info "Target directory: $SOURCE_DIR"
    log_info ""

    local symlinks
    symlinks=$(find_symlinks "$SOURCE_DIR")

    if [[ -z "$symlinks" ]]; then
        log_info "No symbolic links found in target repository."
        log_info ""
        log_info "RESULT: PASS - No symlinks present"
        return 0
    fi

    log_info "Analyzing symlinks..."
    log_info ""

    while IFS= read -r symlink; do
        analyze_symlink "$symlink" || true
    done <<< "$symlinks"

    # Additional post-migration checks
    log_info ""
    log_info "Additional post-migration checks..."

    # Check if any symlink target contains excluded patterns
    for pattern in "${EXCLUDED_PATTERNS[@]}"; do
        local matches
        matches=$(find "$SOURCE_DIR" -type l -exec readlink {} \; 2>/dev/null | grep -c "$pattern" || echo "0")
        if [[ "$matches" -gt 0 ]]; then
            log_danger "Found $matches symlink(s) referencing excluded pattern: $pattern"
            ((DANGEROUS_COUNT+=$matches))
        fi
    done

    print_summary
}

# Print summary report
print_summary() {
    log_info ""
    log_info "============================================================"
    log_info "                    SYMLINK VERIFICATION SUMMARY            "
    log_info "============================================================"
    log_info ""
    log_info "Total symlinks analyzed:  $TOTAL_COUNT"
    log_info "Safe symlinks:            $SAFE_COUNT"
    log_info "Broken symlinks:          $BROKEN_COUNT"
    log_info "DANGEROUS symlinks:       $DANGEROUS_COUNT"
    log_info ""

    if [[ $DANGEROUS_COUNT -gt 0 ]]; then
        log_error "============================================================"
        log_error "RESULT: FAIL - $DANGEROUS_COUNT dangerous symlink(s) found"
        log_error "============================================================"
        log_error ""
        log_error "ACTION REQUIRED:"
        log_error "  1. Remove or redirect dangerous symlinks before migration"
        log_error "  2. Review each DANGEROUS symlink above"
        log_error "  3. Re-run this verification after fixes"
        log_error ""
        return 1
    elif [[ $BROKEN_COUNT -gt 0 ]]; then
        log_warn "============================================================"
        log_warn "RESULT: WARN - $BROKEN_COUNT broken symlink(s) found"
        log_warn "============================================================"
        log_warn ""
        log_warn "Broken symlinks will copy as-is (pointing to non-existent paths)."
        log_warn "Consider removing or fixing broken symlinks before migration."
        log_warn ""
        return 2
    else
        log_info "============================================================"
        log_info "RESULT: PASS - All symlinks are safe"
        log_info "============================================================"
        log_info ""
        return 0
    fi
}

# ============================================================================
# ARGUMENT PARSING
# ============================================================================

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)
                usage
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -q|--quiet)
                QUIET=true
                shift
                ;;
            --pre-migration)
                MODE="pre-migration"
                shift
                ;;
            --post-migration)
                MODE="post-migration"
                shift
                ;;
            -*)
                log_error "Unknown option: $1"
                usage
                ;;
            *)
                SOURCE_DIR="$1"
                shift
                ;;
        esac
    done

    # Set default source directory if not provided
    if [[ -z "$SOURCE_DIR" ]]; then
        SOURCE_DIR="$DEFAULT_SOURCE_DIR"
    fi

    # Validate source directory exists
    if [[ ! -d "$SOURCE_DIR" ]]; then
        log_error "Directory does not exist: $SOURCE_DIR"
        exit 3
    fi

    # Get absolute path using portable method
    if [[ "$(uname)" == "Darwin" ]]; then
        SOURCE_DIR=$(realpath_portable "$SOURCE_DIR" 2>/dev/null) || true
    else
        SOURCE_DIR=$(readlink -f "$SOURCE_DIR" 2>/dev/null) || true
    fi
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    parse_args "$@"

    case "$MODE" in
        pre-migration)
            run_pre_migration
            ;;
        post-migration)
            run_post_migration
            ;;
        *)
            log_error "Unknown mode: $MODE"
            exit 3
            ;;
    esac
}

# Run main function
main "$@"
