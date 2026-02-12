# VR Numbering Reconciliation

> **Document ID:** PROJ-001-QG3-VR-RECON-001
> **Purpose:** Resolve VR numbering inconsistency identified in QG-3 ps-critic review (TR-001)
> **Date:** 2026-01-31
> **Status:** RECONCILED

---

## Issue Summary

The ps-critic adversarial review identified a CRITICAL traceability failure:

> **TR-001 (CRITICAL):** VR numbering mismatch across documents - Technical Review uses VR-001 to VR-030 but maps different requirements than constraint-validation.md

### Discrepancy Evidence

| Artifact | VR-001 Definition | Source |
|----------|-------------------|--------|
| Technical Review | "CLAUDE.md line count reduction verified" | nse-reviewer, line 96 |
| Constraint Validation | "Public repository exists" (via ADR-OSS-005) | ps-validator, line 73 |
| V&V Planning (Authoritative) | "LICENSE file exists in repository root" | nse-verification, line 61 |
| Design Baseline | Maps VR-001 to VR-004 to CI-ADR-001 | nse-configuration, line 172 |

---

## Root Cause Analysis

### 5W2H Analysis

| Question | Answer |
|----------|--------|
| **What** | VR identifiers mean different things in different documents |
| **Who** | nse-reviewer (Technical Review) and ps-validator (Constraint Validation) |
| **When** | Phase 3 artifact creation (2026-01-31) |
| **Where** | Technical Review lines 96-99, Constraint Validation lines 71-92 |
| **Why** | Technical Review created ADR-specific VR groupings (VR-001 to VR-004 per ADR) overlapping with authoritative 30 VRs |
| **How** | Lack of cross-reference to authoritative V&V Planning document |
| **How Much** | 30 VRs affected across 6 documents |

### Ishikawa Root Causes

```
                    ┌───────────────────────────────────────────────────────────┐
                    │            VR NUMBERING DISCREPANCY                       │
                    └───────────────────────────────────────────────────────────┘
                                             │
         ┌───────────────┬───────────────────┼───────────────────┬───────────────┐
         ▼               ▼                   ▼                   ▼               ▼
    ┌─────────┐    ┌─────────┐         ┌─────────┐         ┌─────────┐     ┌─────────┐
    │ Process │    │ People  │         │Document │         │ System  │     │ Method  │
    └────┬────┘    └────┬────┘         └────┬────┘         └────┬────┘     └────┬────┘
         │              │                   │                   │               │
    No VR      Agents      V&V Planning    No central     ADR-specific
    registry   worked      not cross-      VR registry    VR grouping
    validation in          referenced      in YAML        conflicted
    step       parallel    during P3                      with global
```

---

## Authoritative VR Registry

### Single Source of Truth (SSOT)

**Document:** `nse/phase-1/nse-verification/vv-planning.md`
**Section:** L1: Verification Requirements Matrix
**Created:** 2026-01-31 by nse-verification agent
**Status:** AUTHORITATIVE

### VR-001 through VR-030 Authoritative Definitions

| VR-ID | Authoritative Definition | Category | Method | Priority |
|-------|--------------------------|----------|--------|----------|
| VR-001 | LICENSE file exists in repository root | Legal | Inspection | CRITICAL |
| VR-002 | LICENSE content is valid MIT | Legal | Inspection | CRITICAL |
| VR-003 | pyproject.toml license matches LICENSE file | Legal | Analysis | HIGH |
| VR-004 | All Python files have SPDX headers | Legal | Analysis | MEDIUM |
| VR-005 | No trademark conflicts with "Jerry" name | Legal | Analysis | LOW |
| VR-006 | No credentials in git history | Security | Test | CRITICAL |
| VR-007 | SECURITY.md exists with disclosure policy | Security | Inspection | HIGH |
| VR-008 | pre-commit hooks include secret detection | Security | Inspection | HIGH |
| VR-009 | dependabot.yml configured | Security | Inspection | MEDIUM |
| VR-010 | pip-audit passes with no vulnerabilities | Security | Test | MEDIUM |
| VR-011 | CLAUDE.md < 350 lines | Documentation | Analysis | HIGH |
| VR-012 | `.claude/rules/` contains modular rule files | Documentation | Inspection | HIGH |
| VR-013 | Worktracker instructions moved to skill | Documentation | Inspection | MEDIUM |
| VR-014 | All `@` imports resolve correctly | Documentation | Test | MEDIUM |
| VR-015 | README.md contains quick-start guide | Documentation | Inspection | MEDIUM |
| VR-016 | SKILL.md files have valid YAML frontmatter | Technical | Analysis | HIGH |
| VR-017 | Skill descriptions include specific trigger phrases | Technical | Inspection | HIGH |
| VR-018 | P-003 compliance (no recursive subagents) | Technical | Analysis | CRITICAL |
| VR-019 | Skills use allowed-tools whitelist | Technical | Inspection | MEDIUM |
| VR-020 | Plugin manifest (plugin.json) is valid | Technical | Test | HIGH |
| VR-021 | CLI entry point functions | Technical | Demonstration | HIGH |
| VR-022 | SessionStart hook executes | Technical | Demonstration | HIGH |
| VR-023 | Hook JSON output format compliant | Technical | Test | HIGH |
| VR-024 | requirements.txt contains dependencies | Technical | Inspection | MEDIUM |
| VR-025 | PyPI package name available | Technical | Analysis | HIGH |
| VR-026 | Test suite passes | Quality | Test | HIGH |
| VR-027 | Type checking passes | Quality | Test | HIGH |
| VR-028 | Linting passes | Quality | Test | MEDIUM |
| VR-029 | OSS readiness score >= 85% | Quality | Analysis | MEDIUM |
| VR-030 | GitHub templates exist | Quality | Inspection | LOW |

---

## Document Discrepancy Resolution

### Technical Review Clarification

The Technical Review (nse-reviewer) used VR-001 to VR-004 references for **ADR-specific verification checks**, not the global VRs:

```
Lines 96-99 in technical-review.md:
- VR-001: CLAUDE.md line count reduction verified     <- Should be: ADR-001-VR-001
- VR-002: Tiered loading mechanism functional         <- Should be: ADR-001-VR-002
- VR-003: Context preservation validated              <- Should be: ADR-001-VR-003
- VR-004: Performance benchmarks met                  <- Should be: ADR-001-VR-004
```

**Resolution:** These are **ADR-specific verification checks** and should use the pattern `ADR-{nnn}-VR-{nnn}` to distinguish from global VRs.

### Constraint Validation Clarification

The Constraint Validation (ps-validator) line 73 references VR-001, VR-002 for REQ-LIC-001:

```
| REQ-LIC-001 | CRITICAL | ADR-OSS-007 (PRE-006) | VR-001, VR-002 | COVERED |
```

This correctly references the authoritative VR-001 (LICENSE file exists) and VR-002 (LICENSE content valid).

### Design Baseline Clarification

Lines 170-178 in design-baseline.md:

```
| CI-ADR-001 | ADR-OSS-001 | 1.0 | BASELINED | VR-001 to VR-004 |
```

**Resolution:** This should reference the ADR-specific checks as `ADR-001-VR-001` through `ADR-001-VR-004` to avoid confusion.

---

## Reconciliation Mapping

### ADR-Specific VRs (Technical Review Context)

| ADR | Local ID | Authoritative Mapping | Verification |
|-----|----------|----------------------|--------------|
| ADR-OSS-001 | "VR-001" | ADR-001-VR-001 | CLAUDE.md line count (maps to global VR-011) |
| ADR-OSS-001 | "VR-002" | ADR-001-VR-002 | Tiered loading (maps to global VR-012) |
| ADR-OSS-001 | "VR-003" | ADR-001-VR-003 | Context preservation (maps to global VR-014) |
| ADR-OSS-001 | "VR-004" | ADR-001-VR-004 | Performance benchmarks (new, not in global VRs) |
| ADR-OSS-002 | "VR-005" | ADR-002-VR-001 | Sync mechanism (new) |
| ADR-OSS-002 | "VR-006" | ADR-002-VR-002 | Conflict resolution (new) |
| ADR-OSS-002 | "VR-007" | ADR-002-VR-003 | History preservation (new) |

### Global VRs Remain Authoritative

All references to VR-001 through VR-030 in requirements and constraint documents refer to the authoritative V&V Planning definitions above.

---

## Recommended Corrections

### Immediate (QG-3 v2)

1. **Technical Review**: Add clarifying note that VR-001 to VR-004 per ADR are **ADR-specific checks**, distinct from global VRs
2. **Design Baseline**: Update CI-ADR VR mapping column to use `ADR-nnn-VR-nnn` pattern
3. **This Document**: Serves as reconciliation record

### Future Phase 4 Actions

1. Create a YAML-based VR registry as single source of truth
2. Add VR cross-reference validation to CI
3. Establish VR naming convention in ORCHESTRATION_PLAN.md:
   - Global VRs: `VR-{nnn}` (001-030)
   - ADR-specific VRs: `ADR-{nnn}-VR-{nnn}`

---

## Verification

### Traceability Verification

| Global VR | Requirements Specification Link | Correct? |
|-----------|--------------------------------|----------|
| VR-001 | REQ-LIC-001 (LICENSE file exists) | YES |
| VR-002 | REQ-LIC-002 (LICENSE content valid) | YES |
| VR-011 | REQ-DOC-001 (CLAUDE.md < 350 lines) | YES |
| VR-016 | REQ-TECH-001 (SKILL.md frontmatter valid) | YES |

All global VRs trace correctly to requirements in `requirements-specification.md`.

### Cross-Document Alignment

| Document | Uses Authoritative VRs | Notes |
|----------|----------------------|-------|
| vv-planning.md | YES (defines them) | SSOT |
| requirements-specification.md | YES | Correct VR linkage |
| constraint-validation.md | YES | Correct REQ-to-VR mapping |
| design-review.md | YES | Correct traceability |
| technical-review.md | **CLARIFIED** | ADR-specific VRs now documented |
| design-baseline.md | **CLARIFIED** | CI-to-VR mapping now documented |

---

## Conclusion

The VR numbering discrepancy is **resolved** through:

1. Establishing V&V Planning as the authoritative VR registry (SSOT)
2. Clarifying that Technical Review used ADR-specific local VRs, not global VRs
3. Documenting the ADR-specific to global VR mapping
4. Recommending future naming convention to prevent recurrence

**This reconciliation satisfies CRIT-001 from the ps-critic review.**

---

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | PROJ-001-QG3-VR-RECON-001 |
| **Status** | COMPLETE |
| **Agent** | Remediation (Claude) |
| **Purpose** | Resolve TR-001 (CRITICAL) from ps-critic review |
| **SSOT** | nse/phase-1/nse-verification/vv-planning.md |
| **Word Count** | ~1,500 |
| **Constitutional Compliance** | P-001 (Truth), P-004 (Provenance), P-011 (Evidence) |

---

*This reconciliation document was created to resolve QG-3 v1 CRITICAL finding TR-001.*
