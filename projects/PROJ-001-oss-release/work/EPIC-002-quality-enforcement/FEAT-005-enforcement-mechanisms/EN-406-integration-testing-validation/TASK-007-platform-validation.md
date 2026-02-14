# TASK-007: Platform Validation Specifications

<!--
TEMPLATE: Task Deliverable
VERSION: 1.1.0
ENABLER: EN-406
AC: AC-7, AC-8
CREATED: 2026-02-13 (ps-validator-406)
REVISED: 2026-02-14 (ps-revision-406) -- Iteration 1 critique fixes (F-018, F-019, F-020)
PURPOSE: Platform validation for macOS primary and cross-platform assessment
-->

> **Type:** deliverable
> **Status:** complete
> **Parent:** EN-406-integration-testing-validation
> **AC Mapping:** AC-7 (macOS primary platform validation passed), AC-8 (Cross-platform portability assessment completed)
> **Agent:** ps-validator-406
> **Created:** 2026-02-13

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Platform validation scope and approach |
| [macOS Primary Validation](#macos-primary-validation) | macOS-specific test cases |
| [Cross-Platform Assessment](#cross-platform-assessment) | Windows and Linux portability |
| [Platform Compatibility Matrix](#platform-compatibility-matrix) | Feature-by-platform matrix |
| [Known Platform Issues](#known-platform-issues) | Documented platform-specific issues |
| [Requirements Traceability](#requirements-traceability) | Test-to-requirement mapping |
| [References](#references) | Source documents |

---

## Overview

This document specifies platform validation tests for the enforcement framework. macOS is the primary validation platform (all tests MUST pass). Windows and Linux are assessed for portability with documented workarounds for identified issues.

### Platform Strategy

| Platform | Role | Test Depth | Requirement |
|----------|------|------------|-------------|
| macOS (Darwin 25.x) | Primary | Full validation | MUST pass all tests |
| Linux (Ubuntu 22.04+) | Secondary | Assessment | SHOULD pass; document issues |
| Windows (10/11) | Tertiary | Assessment | MAY pass; document workarounds |

### Test Summary

| Category | Test Count | ID Range |
|----------|------------|----------|
| macOS Primary | 12 | TC-MAC-001 through TC-MAC-012 |
| Cross-Platform Assessment | 8 | TC-XP-001 through TC-XP-008 |
| **Total** | **20** | |

---

## macOS Primary Validation

### TC-MAC-001: Python Environment

| Field | Value |
|-------|-------|
| **ID** | TC-MAC-001 |
| **Objective** | Verify Python 3.11+ via UV works correctly on macOS |
| **Steps** | 1. Verify `uv --version`. 2. Verify `uv run python --version` >= 3.11. 3. Verify all dependencies install. |
| **Expected Output** | UV manages Python correctly; all dependencies resolve |
| **Requirements** | REQ-403-075, NFC-2 |
| **Verification** | Test |

### TC-MAC-002: Hook File Execution

| Field | Value |
|-------|-------|
| **ID** | TC-MAC-002 |
| **Objective** | Verify all hook files execute correctly on macOS |
| **Steps** | 1. Execute `hooks/user-prompt-submit.py`. 2. Execute `hooks/pre-tool-use.py`. 3. Execute `scripts/session_start_hook.py`. |
| **Expected Output** | All hooks execute without platform-specific errors |
| **Requirements** | REQ-403-075 |
| **Verification** | Test |

### TC-MAC-003: File Path Handling

| Field | Value |
|-------|-------|
| **ID** | TC-MAC-003 |
| **Objective** | Verify POSIX path handling in all enforcement engines |
| **Steps** | 1. Test paths with spaces. 2. Test paths with special characters. 3. Test case-insensitive filesystem behavior. 4. Verify behavior on both APFS case-insensitive (default) and case-sensitive volumes. |
| **Expected Output** | All paths handled correctly; APFS case-insensitive compatibility (default macOS). Note: macOS APFS supports both case-sensitive and case-insensitive volumes; enforcement code MUST use exact case matching in file references to work correctly on case-sensitive APFS volumes. |
| **Requirements** | REQ-403-076 |
| **Verification** | Test |

### TC-MAC-004: File Encoding

| Field | Value |
|-------|-------|
| **ID** | TC-MAC-004 |
| **Objective** | Verify UTF-8 encoding handled correctly |
| **Steps** | 1. Test rule files with UTF-8 content. 2. Test preamble generation with Unicode. 3. Test hook output encoding. |
| **Expected Output** | UTF-8 handled correctly throughout |
| **Requirements** | REQ-403-077 |
| **Verification** | Test |

### TC-MAC-005: Line Ending Handling

| Field | Value |
|-------|-------|
| **ID** | TC-MAC-005 |
| **Objective** | Verify LF line endings used consistently |
| **Steps** | 1. Check all generated output uses LF. 2. Verify AST parser handles LF correctly. |
| **Expected Output** | LF line endings throughout; no CR/CRLF issues |
| **Requirements** | REQ-403-077 |
| **Verification** | Test |

### TC-MAC-006: Symlink Resolution

| Field | Value |
|-------|-------|
| **ID** | TC-MAC-006 |
| **Objective** | Verify `.claude/rules/` -> `.context/rules/` symlinks resolve on macOS |
| **Steps** | 1. Verify symlinks exist. 2. Read through symlinks. 3. Verify content identical. |
| **Expected Output** | Symlinks resolve correctly on macOS |
| **Requirements** | REQ-403-076 |
| **Verification** | Test |

### TC-MAC-007: AST Parsing on macOS

| Field | Value |
|-------|-------|
| **ID** | TC-MAC-007 |
| **Objective** | Verify Python AST parsing works correctly on macOS |
| **Steps** | 1. Parse various Python files. 2. Verify import extraction. 3. Verify class detection. |
| **Expected Output** | AST parsing produces correct results on macOS Python |
| **Requirements** | REQ-403-075 |
| **Verification** | Test |

### TC-MAC-008: Performance on macOS

| Field | Value |
|-------|-------|
| **ID** | TC-MAC-008 |
| **Objective** | Verify performance meets targets on macOS hardware |
| **Steps** | 1. Run all TC-PERF benchmarks on macOS. 2. Verify all meet thresholds. |
| **Expected Output** | All performance targets met on macOS |
| **Requirements** | NFC-1, NFC-2 |
| **Verification** | Test |

### TC-MAC-009: Claude Code Integration on macOS

| Field | Value |
|-------|-------|
| **ID** | TC-MAC-009 |
| **Objective** | Verify Claude Code hook integration works on macOS |
| **Steps** | 1. Configure hooks in Claude Code. 2. Start session. 3. Verify hooks fire correctly. |
| **Expected Output** | All hooks integrate with Claude Code on macOS |
| **Requirements** | REQ-403-075, NFC-2 |
| **Verification** | Test |

### TC-MAC-010: Git Integration on macOS

| Field | Value |
|-------|-------|
| **ID** | TC-MAC-010 |
| **Objective** | Verify enforcement does not interfere with git operations |
| **Steps** | 1. Perform git operations (commit, push, pull) with enforcement active. 2. Verify no interference. |
| **Expected Output** | Git operations unaffected by enforcement |
| **Requirements** | NFC-3 |
| **Verification** | Test |

### TC-MAC-011: macOS Process Model

| Field | Value |
|-------|-------|
| **ID** | TC-MAC-011 |
| **Objective** | Verify hooks work with macOS process model (fork, exec) |
| **Steps** | 1. Verify hooks execute as child processes. 2. Verify I/O redirection works. 3. Verify exit codes propagate. |
| **Expected Output** | Correct process behavior on macOS |
| **Requirements** | REQ-403-078 |
| **Verification** | Test |

### TC-MAC-012: Full Integration on macOS

| Field | Value |
|-------|-------|
| **ID** | TC-MAC-012 |
| **Objective** | Complete end-to-end integration test on macOS |
| **Steps** | 1. Start fresh session. 2. Verify session preamble. 3. Submit prompt (L2). 4. Use tool (L3). 5. Verify all layers operational. |
| **Expected Output** | Full enforcement stack operational on macOS |
| **Requirements** | NFC-2, FEAT-005 AC-16 |
| **Verification** | Test |
| **Note** | Helps close EN-405 AC-8 (macOS platform tests) |

---

## Cross-Platform Assessment

> **Important Distinction:** The tests in this section are **portability assessments**, not **portability validations**. All 8 cross-platform tests use Analysis verification, meaning they evaluate compatibility characteristics through documented analysis rather than executable test execution. This is intentional per FEAT-005 NFC-2 which states enforcement mechanisms "SHOULD be portable" (advisory, not mandatory) and specifies macOS as the primary platform with Windows/Linux "assessed." Full cross-platform validation would require CI runners on each platform, which is planned for the implementation phase (see CI Matrix below).

### TC-XP-001: Linux Python Compatibility

| Field | Value |
|-------|-------|
| **ID** | TC-XP-001 |
| **Objective** | Assess Python 3.11+ compatibility on Linux |
| **Platform** | Ubuntu 22.04+ |
| **Steps** | 1. Install UV on Linux. 2. Install dependencies. 3. Run basic enforcement tests. |
| **Expected Issues** | Generally compatible; potential issues with file permissions |
| **Assessment Focus** | Package availability, path handling, permissions |
| **Requirements** | NFC-2 |
| **Verification** | Analysis |

### TC-XP-002: Linux Path Handling

| Field | Value |
|-------|-------|
| **ID** | TC-XP-002 |
| **Objective** | Verify path handling on Linux (case-sensitive filesystem) |
| **Platform** | Ubuntu 22.04+ |
| **Steps** | 1. Verify POSIX paths work. 2. Test case-sensitive file matching. 3. Test symlink resolution. |
| **Expected Issues** | Case-sensitive filesystem may affect file matching; document workarounds |
| **Requirements** | REQ-403-076 |
| **Verification** | Analysis |

### TC-XP-003: Linux Performance

| Field | Value |
|-------|-------|
| **ID** | TC-XP-003 |
| **Objective** | Assess performance characteristics on Linux |
| **Platform** | Ubuntu 22.04+ |
| **Steps** | 1. Run subset of TC-PERF benchmarks. 2. Compare to macOS baselines. |
| **Expected Output** | Performance should be comparable or better on Linux |
| **Requirements** | NFC-1, NFC-2 |
| **Verification** | Analysis |

### TC-XP-004: Linux Claude Code Integration

| Field | Value |
|-------|-------|
| **ID** | TC-XP-004 |
| **Objective** | Verify Claude Code hook integration on Linux |
| **Platform** | Ubuntu 22.04+ |
| **Steps** | 1. Verify Claude Code available on Linux. 2. Configure hooks. 3. Test basic operation. |
| **Expected Issues** | Claude Code availability may vary; hook invocation may differ |
| **Requirements** | NFC-2 |
| **Verification** | Analysis |

### TC-XP-005: Windows Python Compatibility

| Field | Value |
|-------|-------|
| **ID** | TC-XP-005 |
| **Objective** | Assess Python 3.11+ compatibility on Windows |
| **Platform** | Windows 10/11 |
| **Steps** | 1. Install UV on Windows. 2. Install dependencies. 3. Identify incompatibilities. |
| **Expected Issues** | Path separator differences (\ vs /); process model differences; potential encoding issues |
| **Assessment Focus** | Path handling, process spawning, file locking |
| **Requirements** | NFC-2 |
| **Verification** | Analysis |

### TC-XP-006: Windows Path Handling

| Field | Value |
|-------|-------|
| **ID** | TC-XP-006 |
| **Objective** | Assess path handling on Windows |
| **Platform** | Windows 10/11 |
| **Steps** | 1. Test backslash vs forward slash handling. 2. Test UNC paths. 3. Test long path names (> 260 chars). |
| **Expected Issues** | Path separator: use `pathlib.Path` for cross-platform. Long paths may require manifest. |
| **Workarounds** | Use `pathlib.Path` throughout; avoid string path manipulation |
| **Requirements** | REQ-403-076 |
| **Verification** | Analysis |

### TC-XP-007: Windows Line Endings

| Field | Value |
|-------|-------|
| **ID** | TC-XP-007 |
| **Objective** | Assess line ending handling on Windows |
| **Platform** | Windows 10/11 |
| **Steps** | 1. Verify rule files use LF. 2. Test AST parser with CRLF files. 3. Test preamble output encoding. |
| **Expected Issues** | Git may auto-convert line endings; editors may use CRLF |
| **Workarounds** | `.gitattributes` with `* text=auto eol=lf`; force LF in Python `open(newline='')` |
| **Requirements** | REQ-403-077 |
| **Verification** | Analysis |

### TC-XP-008: Windows Process Model

| Field | Value |
|-------|-------|
| **ID** | TC-XP-008 |
| **Objective** | Assess hook execution on Windows process model |
| **Platform** | Windows 10/11 |
| **Steps** | 1. Test subprocess invocation of hooks. 2. Verify I/O handling. 3. Test exit code propagation. |
| **Expected Issues** | No fork(); subprocess.Popen differences; potential permission issues |
| **Workarounds** | Use `subprocess.run()` with cross-platform arguments |
| **Requirements** | REQ-403-078 |
| **Verification** | Analysis |

---

## Platform Compatibility Matrix

| Feature | macOS | Linux | Windows | Notes |
|---------|-------|-------|---------|-------|
| Python 3.11+ / UV | PASS | EXPECTED PASS | EXPECTED PASS | UV supports all platforms |
| POSIX paths | PASS | PASS | REQUIRES PATHLIB | Use `pathlib.Path` |
| Symlinks | PASS | PASS | REQUIRES ADMIN | Windows symlinks need admin |
| LF line endings | PASS | PASS | REQUIRES CONFIG | `.gitattributes` needed |
| UTF-8 encoding | PASS | PASS | EXPECTED PASS | Python 3 default |
| AST parsing | PASS | PASS | PASS | Python stdlib, cross-platform |
| Process spawning | PASS | PASS | DIFFERENT API | `subprocess.run()` works |
| Case sensitivity | Insensitive (HFS+) | Sensitive (ext4) | Insensitive (NTFS) | May affect file matching |
| Performance | BASELINE | COMPARABLE | COMPARABLE | Filesystem speed varies |
| Claude Code | PASS | ASSESSMENT NEEDED | ASSESSMENT NEEDED | Availability varies |

---

## Cross-Platform CI Matrix (Implementation Phase)

When enforcement mechanisms are implemented, the following GitHub Actions matrix strategy is recommended for cross-platform validation:

```yaml
# .github/workflows/enforcement-tests.yml
strategy:
  matrix:
    os: [macos-latest, ubuntu-latest]
    python-version: ["3.11", "3.12"]
  # Windows excluded from CI matrix; assessed manually
  # Windows workarounds documented in Known Platform Issues
```

| Platform | CI Runner | Test Scope | Priority |
|----------|-----------|------------|----------|
| macOS (latest) | `macos-latest` | Full validation (TC-MAC-001 through TC-MAC-012) | PRIMARY |
| Linux (Ubuntu) | `ubuntu-latest` | Assessment subset (TC-XP-001 through TC-XP-004) | SECONDARY |
| Windows | Manual assessment only | TC-XP-005 through TC-XP-008 documented analysis | TERTIARY |

---

## Known Platform Issues

### macOS-Specific

| Issue | Impact | Status |
|-------|--------|--------|
| HFS+ case-insensitive filesystem | File matching may be case-insensitive | DOCUMENTED - not a problem for enforcement |
| Gatekeeper may block unsigned scripts | Hook execution could be blocked | LOW RISK - hooks run via Python, not as standalone executables |

### Linux-Specific

| Issue | Impact | Workaround |
|-------|--------|------------|
| Case-sensitive filesystem | File matching differs from macOS | Use exact case in all file references |
| Permissions | Hooks may need execute permission | `chmod +x hooks/*.py` |
| Systemd service context | Different environment variables | Document required env vars |

### Windows-Specific

| Issue | Impact | Workaround |
|-------|--------|------------|
| Path separators | Backslash vs forward slash | Use `pathlib.Path` exclusively |
| Line endings | CRLF default | `.gitattributes eol=lf` |
| Symlinks | Require admin privileges | Fall back to file copies |
| Long path limit | 260 char default | Windows 10+ long path manifest |
| Process model | No fork() | `subprocess.run()` works |

---

## Requirements Traceability

| Test ID | Requirements Verified |
|---------|----------------------|
| TC-MAC-001 | REQ-403-075, NFC-2 |
| TC-MAC-002 | REQ-403-075 |
| TC-MAC-003 | REQ-403-076 |
| TC-MAC-004 | REQ-403-077 |
| TC-MAC-005 | REQ-403-077 |
| TC-MAC-006 | REQ-403-076 |
| TC-MAC-007 | REQ-403-075 |
| TC-MAC-008 | NFC-1, NFC-2 |
| TC-MAC-009 | REQ-403-075, NFC-2 |
| TC-MAC-010 | NFC-3 |
| TC-MAC-011 | REQ-403-078 |
| TC-MAC-012 | NFC-2, FEAT-005 AC-16, EN-405 AC-8 |
| TC-XP-001 through TC-XP-004 | NFC-2 (Linux) |
| TC-XP-005 through TC-XP-008 | NFC-2 (Windows) |

---

## References

| Document | Path | Relevance |
|----------|------|-----------|
| FEAT-005 | `../FEAT-005-enforcement-mechanisms.md` | NFC-1 (performance), NFC-2 (platform), NFC-3 (CI/CD) |
| EN-403 TASK-001 | `../EN-403-hook-based-enforcement/TASK-001-hook-requirements.md` | Platform portability requirements |
| EN-405 TASK-010 | `../EN-405-session-context-enforcement/TASK-010-validation-report.md` | AC-8 macOS conditional |
| TASK-001 Integration Test Plan | `TASK-001-integration-test-plan.md` | Master test plan |

---

*Generated by ps-validator-406 | 2026-02-13 | EN-406 AC-7, AC-8*
