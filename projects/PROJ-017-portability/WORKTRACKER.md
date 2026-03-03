# PROJ-017 Platform Portability - Work Tracker

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Project metadata and source |
| [Hierarchy](#hierarchy) | Full decomposition tree |
| [Epic Summary](#epic-summary) | Epic-level tracking |
| [Feature Summary](#feature-summary) | Feature-level tracking |
| [Bug Inventory](#bug-inventory) | All bugs with severity and status |
| [Enabler Inventory](#enabler-inventory) | Infrastructure enablers |
| [Progress](#progress) | Completion metrics |

---

## Overview

| Field | Value |
|-------|-------|
| **Project** | PROJ-017-portability |
| **Created** | 2026-02-26 |
| **Source** | PORT-001 Portability Analysis (eng-security agent) |
| **Pattern** | Project-based placement (PROJ-009 reference) |

---

## Hierarchy

```
PROJ-017-portability
└── EPIC-017-001: Platform Portability
    ├── FEAT-017-001: Shell Command Portability
    │   ├── BUG-017-001: statusLine Uses Hardcoded python3 (Major)
    │   ├── BUG-017-002: Migration Scripts Are Bash-Only (Major)
    │   └── BUG-017-006: macOS Symlink Resolution Fallback (Major)
    ├── FEAT-017-002: File System Portability
    │   ├── BUG-017-003: Symlinks Require Elevated Privileges on Windows (Major)
    │   ├── BUG-017-004: Missing .gitattributes (Minor)
    │   └── BUG-017-005: Hardcoded Forward-Slash Path Separators (Minor)
    ├── FEAT-017-003: Documentation Portability
    │   └── BUG-017-007: /tmp References in Docstrings (Minor)
    ├── EN-017-001: Windows CI Testing Pipeline
    └── EN-017-002: Platform Portability Test Suite
```

---

## Epic Summary

| ID | Title | Priority | Status | Features | Bugs | Enablers | Completion |
|----|-------|----------|--------|----------|------|----------|------------|
| [EPIC-017-001](work/EPIC-017-001-platform-portability/EPIC-017-001.md) | Platform Portability | high | pending | 3 | 7 | 2 | 0% |

---

## Feature Summary

| ID | Title | Priority | Parent | Bugs | Status |
|----|-------|----------|--------|------|--------|
| [FEAT-017-001](work/EPIC-017-001-platform-portability/FEAT-017-001-shell-command-portability/FEAT-017-001.md) | Shell Command Portability | high | EPIC-017-001 | 3 | pending |
| [FEAT-017-002](work/EPIC-017-001-platform-portability/FEAT-017-002-file-system-portability/FEAT-017-002.md) | File System Portability | high | EPIC-017-001 | 3 | pending |
| [FEAT-017-003](work/EPIC-017-001-platform-portability/FEAT-017-003-documentation-portability/FEAT-017-003.md) | Documentation Portability | low | EPIC-017-001 | 1 | pending |

---

## Bug Inventory

| ID | Title | Severity | Parent | Platform | GitHub | Status |
|----|-------|----------|--------|----------|--------|--------|
| [BUG-017-001](work/EPIC-017-001-platform-portability/FEAT-017-001-shell-command-portability/BUG-017-001-statusline-python3/BUG-017-001.md) | statusLine Uses Hardcoded python3 | Major | FEAT-017-001 | Windows | [#113](https://github.com/geekatron/jerry/issues/113) | pending |
| [BUG-017-002](work/EPIC-017-001-platform-portability/FEAT-017-001-shell-command-portability/BUG-017-002-migration-scripts-bash/BUG-017-002.md) | Migration Scripts Are Bash-Only | Major | FEAT-017-001 | Windows | [#114](https://github.com/geekatron/jerry/issues/114) | pending |
| [BUG-017-003](work/EPIC-017-001-platform-portability/FEAT-017-002-file-system-portability/BUG-017-003-symlinks-privileges/BUG-017-003.md) | Symlinks Require Elevated Privileges | Major | FEAT-017-002 | Windows | [#115](https://github.com/geekatron/jerry/issues/115) | pending |
| [BUG-017-004](work/EPIC-017-001-platform-portability/FEAT-017-002-file-system-portability/BUG-017-004-missing-gitattributes/BUG-017-004.md) | Missing .gitattributes | Minor | FEAT-017-002 | All | [#116](https://github.com/geekatron/jerry/issues/116) | pending |
| [BUG-017-005](work/EPIC-017-001-platform-portability/FEAT-017-002-file-system-portability/BUG-017-005-hardcoded-path-separator/BUG-017-005.md) | Hardcoded Path Separators | Minor | FEAT-017-002 | Windows | [#117](https://github.com/geekatron/jerry/issues/117) | pending |
| [BUG-017-006](work/EPIC-017-001-platform-portability/FEAT-017-001-shell-command-portability/BUG-017-006-macos-symlink-resolution/BUG-017-006.md) | macOS Symlink Resolution Fallback | Major | FEAT-017-001 | macOS | [#118](https://github.com/geekatron/jerry/issues/118) | pending |
| [BUG-017-007](work/EPIC-017-001-platform-portability/FEAT-017-003-documentation-portability/BUG-017-007-tmp-in-docstrings/BUG-017-007.md) | /tmp References in Docstrings | Minor | FEAT-017-003 | All | [#119](https://github.com/geekatron/jerry/issues/119) | pending |

---

## Enabler Inventory

| ID | Title | Subtype | Parent | Priority | Status |
|----|-------|---------|--------|----------|--------|
| [EN-017-001](work/EPIC-017-001-platform-portability/EN-017-001-windows-ci-pipeline/EN-017-001.md) | Windows CI Testing Pipeline | infrastructure | EPIC-017-001 | high | pending |
| [EN-017-002](work/EPIC-017-001-platform-portability/EN-017-002-platform-portability-tests/EN-017-002.md) | Platform Portability Test Suite | infrastructure | EPIC-017-001 | high | pending |

---

## Progress

| Metric | Value |
|--------|-------|
| **Total Items** | 12 (1 Epic, 3 Features, 7 Bugs, 2 Enablers) |
| **Major Bugs** | 4 |
| **Minor Bugs** | 3 |
| **Completed** | 0 |
| **Completion %** | 0% |

### By Feature

| Feature | Total Bugs | Completed | % |
|---------|-----------|-----------|---|
| FEAT-017-001 Shell Commands | 3 | 0 | 0% |
| FEAT-017-002 File System | 3 | 0 | 0% |
| FEAT-017-003 Documentation | 1 | 0 | 0% |
