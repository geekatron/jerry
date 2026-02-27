# PROJ-017: Platform Portability

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Project scope and objectives |
| [Status](#status) | Current project state |
| [Decomposition](#decomposition) | Epic/Feature/Bug/Enabler hierarchy |
| [Phased Execution](#phased-execution) | Implementation phases and ordering |
| [Dependencies](#dependencies) | Cross-item dependencies |
| [Analysis Artifacts](#analysis-artifacts) | Source analysis references |

---

## Overview

Cross-platform compatibility fixes to ensure Jerry works on Windows, macOS, and Linux. Derived from PORT-001 portability analysis (eng-security agent) which identified 14 findings (5 Major, 9 Minor). Seven actionable bugs extracted, grouped into 3 features by category, supported by 2 infrastructure enablers.

---

## Status

| Field | Value |
|-------|-------|
| **Created** | 2026-02-26 |
| **Status** | Active |
| **Source** | PORT-001 Portability Analysis |
| **Total Items** | 12 (1 Epic, 3 Features, 7 Bugs, 2 Enablers) |
| **Completion** | 0% |

---

## Decomposition

```
EPIC-017-001: Platform Portability
├── FEAT-017-001: Shell Command Portability (3 bugs)
├── FEAT-017-002: File System Portability (3 bugs)
├── FEAT-017-003: Documentation Portability (1 bug)
├── EN-017-001: Windows CI Testing Pipeline
└── EN-017-002: Platform Portability Test Suite
```

See [WORKTRACKER.md](WORKTRACKER.md) for full item details and links.

---

## Phased Execution

### Phase 0: Infrastructure (Enablers)

Set up CI and test infrastructure before fixing bugs, so fixes can be verified.

| Item | Title | Rationale |
|------|-------|-----------|
| EN-017-001 | Windows CI Testing Pipeline | Must exist before Windows bug fixes can be CI-verified |
| EN-017-002 | Platform Portability Test Suite | Test harness for regression prevention |

### Phase 1: Major Bugs (High Impact)

Fix major bugs that block Windows/macOS usage. Order: least-dependent first.

| Item | Title | Priority | Dependency |
|------|-------|----------|------------|
| BUG-017-001 | statusLine Uses Hardcoded python3 | high | None |
| BUG-017-002 | Migration Scripts Are Bash-Only | high | None |
| BUG-017-006 | macOS Symlink Resolution Fallback | high | None |
| BUG-017-003 | Symlinks Require Elevated Privileges | high | None |

### Phase 2: Minor Bugs (Low Impact)

Fix minor bugs that improve cross-platform quality.

| Item | Title | Priority | Dependency |
|------|-------|----------|------------|
| BUG-017-004 | Missing .gitattributes | medium | None |
| BUG-017-005 | Hardcoded Path Separators | medium | None |
| BUG-017-007 | /tmp References in Docstrings | low | None |

---

## Dependencies

| From | To | Relationship |
|------|----|-------------|
| EN-017-001 | All BUG-017-* | CI pipeline enables verification of all bug fixes |
| EN-017-002 | All BUG-017-* | Test suite provides regression tests for each fix |
| EN-017-002 | EN-017-001 | Test suite runs on Windows CI pipeline |

**Recommended order:** EN-017-001 -> EN-017-002 -> Phase 1 bugs (parallel) -> Phase 2 bugs (parallel)

---

## Analysis Artifacts

| Artifact | Location |
|----------|----------|
| Full portability analysis | `skills/eng-team/output/PORT-001/eng-security-portability-analysis.md` |
| Issue draft templates | `skills/eng-team/output/PORT-001/issue-drafts.md` |
| Quality gate results | `skills/eng-team/output/PORT-001/adv-scorer-quality-report.md` |
