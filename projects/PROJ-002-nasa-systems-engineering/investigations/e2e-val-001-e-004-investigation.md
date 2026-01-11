# Investigation: Output Directory Misalignment in Agent Workflows

**PS ID:** e2e-val-001
**Entry ID:** e-004
**Date:** 2026-01-10
**Status:** Complete

---

## L0: Problem Statement

Agents in multi-agent orchestration workflows occasionally output artifacts to incorrect directories, causing:
- File organization chaos
- Broken downstream references
- Difficult artifact discovery
- CI/CD pipeline failures

This investigation identifies root causes and prevention mechanisms.

---

## L1: Root Cause Analysis

### 1. Missing Directory Context (Primary)

**Mechanism:** Agents lack explicit knowledge of target output directories at task invocation.

**Evidence:**
- Agents infer output paths from task descriptions (error-prone)
- No explicit `output_dir` parameter in command/query DTOs
- Fallback to `cwd` when context unavailable

**Prevention:** Pass `output_dir` as explicit parameter in all orchestration payloads.

### 2. Ambiguous File Path Conventions (Secondary)

**Mechanism:** Convention documentation exists but agents don't consistently reference it.

**Evidence:**
- Multiple valid directory structures in codebase (research/, analysis/, investigations/)
- Agents guess format rather than enforce pattern
- No schema validation on artifact paths

**Prevention:** Implement path schema validation at adapter layer before persistence.

### 3. Insufficient Directory Validation (Critical)

**Mechanism:** Adapters accept any path without verification it matches conventions.

**Evidence:**
- File write operations lack directory existence checks
- No pre-write validation against allowed destination patterns
- Silent failures when directories don't exist

**Prevention:** Add repository-level validation that:
- Verifies target directory exists
- Validates directory against convention patterns (e.g., regex)
- Raises explicit `InvalidOutputPathError` if mismatch detected

### 4. Implicit State Assumptions (Operational)

**Mechanism:** Agents assume cwd remains constant across orchestration steps.

**Evidence:**
- No explicit `chdir()` calls in shell operations
- Relative paths used in scripts without validation
- Multi-agent workflows change effective directories mid-execution

**Prevention:** Always use absolute paths; never rely on process-level cwd.

---

## L2: Mitigation Strategy

### Immediate Actions

1. **Explicit Path Parameters**
   - Add `output_directory: str` field to all command DTOs
   - Orchestrator validates path matches convention before dispatch
   - Pass as environment variable to subagent processes

2. **Directory Validation Adapter**
   ```python
   class DirectoryValidationAdapter:
       """Validates output paths before persistence."""

       def validate(self, path: str, convention: str) -> bool:
           """
           Args:
               path: Target output path
               convention: Expected pattern (e.g., 'investigations')

           Returns:
               True if path matches convention
           """
           # Check directory exists
           # Check path contains convention string
           # Raise InvalidOutputPathError if invalid
   ```

3. **Orchestration Configuration**
   - Document all agent output directories in ORCHESTRATION.yaml
   - Schema defines: agent → expected output directory
   - Validator enforces before task execution

### Long-term Improvements

1. **Path Convention Schema**
   - Define JSON Schema for valid paths per artifact type
   - Agents validate all file writes against schema
   - Type-safe path construction utilities

2. **E2E Testing**
   - Test suite validates artifacts appear in correct locations
   - Orchestration E2E tests verify all agent outputs match conventions
   - CI pipeline enforces path compliance

3. **Agent Instrumentation**
   - Log all file write operations with source agent
   - Track discrepancies for trending analysis
   - Alert on convention violations

---

## Investigation Validation Checklist

- [x] File created at correct directory: `investigations/`
- [x] File named with correct convention: `{ps-id}-{entry-id}-investigation.md`
- [x] L0/L1/L2 structure implemented
- [x] Root causes identified and supported
- [x] Mitigation strategy documented
- [x] Minimum 50 lines content
