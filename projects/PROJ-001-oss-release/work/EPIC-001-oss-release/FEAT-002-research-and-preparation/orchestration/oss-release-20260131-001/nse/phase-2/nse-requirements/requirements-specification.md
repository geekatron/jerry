# Requirements Specification: Jerry OSS Release

> **Document ID:** PROJ-001-REQ-SPEC-001
> **NPR 7123.1D Compliance:** Section 5.2 (Requirements Analysis)
> **Phase:** 2
> **Tier:** 1 (Foundation)
> **Agent:** nse-requirements
> **Created:** 2026-01-31
> **Status:** DRAFT
> **Quality Threshold:** >= 0.92 (DEC-OSS-001)

---

## Document Navigation

| Level | Audience | Sections |
|-------|----------|----------|
| **L0** | Executives, Stakeholders | Executive Summary, Requirements Overview |
| **L1** | Engineers, Developers | Detailed Shall-Statements by Category |
| **L2** | Architects, Decision Makers | Traceability, Verification Strategy, Risk Linkage |

---

## L0: Executive Summary (ELI5)

### What Are Requirements?

Think of requirements like a recipe for baking a cake:
- **The recipe** tells you exactly what ingredients you need and what steps to follow
- **Requirements** tell us exactly what Jerry needs to have before going public

Without clear requirements:
- Bakers forget ingredients = We might release without a LICENSE
- Steps are unclear = Users can't install Jerry
- No quality check = The cake might taste terrible = Jerry might have security holes

### Why Do We Need This Document?

Before Jerry can be released as open source, we need to:

1. **Check 18 boxes** - Items we discovered are missing (from Gap Analysis)
2. **Reduce 22 risks** - Things that could go wrong (from FMEA Analysis)
3. **Pass 30 tests** - Verification requirements (from V&V Planning)

This document converts all those findings into clear, actionable requirements.

### The Bottom Line

| Category | Requirements | CRITICAL | HIGH | MEDIUM | LOW |
|----------|-------------|----------|------|--------|-----|
| Legal/Licensing | 7 | 2 | 2 | 2 | 1 |
| Security | 6 | 2 | 2 | 1 | 1 |
| Documentation | 8 | 1 | 4 | 2 | 1 |
| Technical | 9 | 1 | 5 | 2 | 1 |
| Quality | 6 | 0 | 3 | 2 | 1 |
| **TOTAL** | **36** | **6** | **16** | **9** | **5** |

**Key Insight:** 6 CRITICAL requirements must be completed before ANY public release.

---

## L1: Technical Requirements (Engineer)

### 1. Legal/Licensing Requirements (REQ-LIC-xxx)

---

#### REQ-LIC-001: LICENSE File Existence

| Field | Value |
|-------|-------|
| **ID** | REQ-LIC-001 |
| **Statement** | The system SHALL include a LICENSE file in the repository root containing a valid MIT license. |
| **Priority** | CRITICAL |
| **Rationale** | Without a LICENSE file, users have no legal right to use, modify, or distribute Jerry. This is an absolute legal blocker for any OSS release. |
| **Gap Source** | GAP-001 (LIC-GAP-001 / DOC-GAP-001) |
| **Risk Linkage** | RSK-P0-001 (RPN: 60) |
| **Verification Method** | Inspection |
| **VR Linkage** | VR-001, VR-002 |
| **Acceptance Criteria** | `ls -la LICENSE` returns file; content matches MIT template |
| **Effort** | S (30 minutes) |

---

#### REQ-LIC-002: LICENSE Content Validity

| Field | Value |
|-------|-------|
| **ID** | REQ-LIC-002 |
| **Statement** | The LICENSE file SHALL contain the official MIT license text with correct copyright year (2026) and copyright holder (Jerry Framework Contributors). |
| **Priority** | CRITICAL |
| **Rationale** | Invalid license text could create legal ambiguity. Enterprise users require exact license matching for compliance. |
| **Gap Source** | GAP-001 (LIC-GAP-001) |
| **Risk Linkage** | RSK-P0-001 (RPN: 60) |
| **Verification Method** | Inspection |
| **VR Linkage** | VR-002 |
| **Acceptance Criteria** | LICENSE text matches SPDX MIT template; year is 2026 |
| **Effort** | S (included in REQ-LIC-001) |

---

#### REQ-LIC-003: pyproject.toml License Consistency

| Field | Value |
|-------|-------|
| **ID** | REQ-LIC-003 |
| **Statement** | The pyproject.toml license field SHALL match the LICENSE file content (MIT). |
| **Priority** | HIGH |
| **Rationale** | Inconsistency between declared and actual license creates confusion and compliance issues for automated license scanners. |
| **Gap Source** | GAP-001 (LIC-GAP-001) |
| **Risk Linkage** | RSK-P0-001 (RPN: 60) |
| **Verification Method** | Analysis |
| **VR Linkage** | VR-003 |
| **Acceptance Criteria** | `license = { text = "MIT" }` in pyproject.toml; matches LICENSE file |
| **Effort** | S (15 minutes) |

---

#### REQ-LIC-004: SPDX License Headers

| Field | Value |
|-------|-------|
| **ID** | REQ-LIC-004 |
| **Statement** | All Python source files (183 files) SHALL contain an SPDX license header as the first comment block. |
| **Priority** | HIGH |
| **Rationale** | Enterprise users require per-file licensing for compliance. SPDX identifiers enable automated license scanning and SBOM generation. |
| **Gap Source** | GAP-003 (LIC-GAP-002), GAP-009 (LIC-GAP-003) |
| **Risk Linkage** | RSK-P0-007 (RPN: 105) |
| **Verification Method** | Analysis |
| **VR Linkage** | VR-004 |
| **Acceptance Criteria** | `grep -r "SPDX-License-Identifier: MIT" src/ | wc -l` = 183 |
| **Effort** | M (2-3 hours for script + execution) |

**Header Format:**
```python
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jerry Framework Contributors
```

---

#### REQ-LIC-005: Third-Party NOTICE File

| Field | Value |
|-------|-------|
| **ID** | REQ-LIC-005 |
| **Statement** | The system SHALL include a NOTICE file listing third-party dependencies and their respective licenses. |
| **Priority** | MEDIUM |
| **Rationale** | Provides transparency about third-party components. Required by some licenses (Apache 2.0 dependencies) and expected by enterprise users. |
| **Gap Source** | GAP-015 (LIC-GAP-004) |
| **Risk Linkage** | N/A |
| **Verification Method** | Inspection |
| **VR Linkage** | N/A |
| **Acceptance Criteria** | NOTICE file exists; lists all dependencies with licenses |
| **Effort** | S (1 hour) |

---

#### REQ-LIC-006: Trademark Conflict Verification

| Field | Value |
|-------|-------|
| **ID** | REQ-LIC-006 |
| **Statement** | The system SHALL verify that the "Jerry" name does not conflict with existing trademarks in the software/developer tools category. |
| **Priority** | MEDIUM |
| **Rationale** | Trademark conflicts could force expensive rebranding and legal issues. |
| **Gap Source** | RSK-P0-021 |
| **Risk Linkage** | RSK-P0-021 (RPN: 50) |
| **Verification Method** | Analysis |
| **VR Linkage** | VR-005 |
| **Acceptance Criteria** | USPTO/EUIPO search completed; no blocking conflicts found |
| **Effort** | S (1 hour) |

---

#### REQ-LIC-007: PyPI Package Name Availability

| Field | Value |
|-------|-------|
| **ID** | REQ-LIC-007 |
| **Statement** | The system SHALL verify that the intended PyPI package name is available before release. |
| **Priority** | LOW |
| **Rationale** | Package name conflicts require documentation updates and user confusion. Early verification prevents last-minute issues. |
| **Gap Source** | RSK-P0-010 |
| **Risk Linkage** | RSK-P0-010 (RPN: 36) |
| **Verification Method** | Analysis |
| **VR Linkage** | VR-025 |
| **Acceptance Criteria** | pypi.org search confirms availability or alternative documented |
| **Effort** | S (15 minutes) |

---

### 2. Security Requirements (REQ-SEC-xxx)

---

#### REQ-SEC-001: Credential Exposure Prevention

| Field | Value |
|-------|-------|
| **ID** | REQ-SEC-001 |
| **Statement** | The git repository history SHALL contain zero exposed credentials, API keys, or secrets as verified by automated scanning. |
| **Priority** | CRITICAL |
| **Rationale** | Credential exposure in public repositories leads to security breaches, account compromises, and reputational damage. |
| **Gap Source** | RSK-P0-002 |
| **Risk Linkage** | RSK-P0-002 (RPN: 120) |
| **Verification Method** | Test |
| **VR Linkage** | VR-006 |
| **Acceptance Criteria** | Gitleaks full-history scan: 0 findings |
| **Effort** | M (2 hours for scan + remediation if needed) |

---

#### REQ-SEC-002: Security Policy Documentation

| Field | Value |
|-------|-------|
| **ID** | REQ-SEC-002 |
| **Statement** | The system SHALL include a SECURITY.md file documenting the vulnerability disclosure process, response timeline, and security contact. |
| **Priority** | CRITICAL |
| **Rationale** | Security researchers need a clear path to report vulnerabilities responsibly. Without this, vulnerabilities may be disclosed publicly without coordination. EU CRA requires this by September 2026. |
| **Gap Source** | GAP-002 (SEC-GAP-001 / DOC-GAP-004) |
| **Risk Linkage** | RSK-P0-003 (RPN: 144) |
| **Verification Method** | Inspection |
| **VR Linkage** | VR-007 |
| **Acceptance Criteria** | SECURITY.md exists with: Supported Versions, Reporting Process, Response Timeline (48h acknowledgment), Security Update Process |
| **Effort** | S (2 hours) |

**Required Sections:**
```markdown
# Security Policy
## Supported Versions
## Reporting a Vulnerability
## Response Timeline
## Security Update Process
```

---

#### REQ-SEC-003: Pre-commit Secret Detection

| Field | Value |
|-------|-------|
| **ID** | REQ-SEC-003 |
| **Statement** | The pre-commit configuration SHALL include secret detection hooks to prevent credential commits. |
| **Priority** | HIGH |
| **Rationale** | Preventive control is more effective than detective control. Catching secrets before commit prevents exposure entirely. |
| **Gap Source** | Security best practices |
| **Risk Linkage** | RSK-P0-002 (RPN: 120) |
| **Verification Method** | Inspection |
| **VR Linkage** | VR-008 |
| **Acceptance Criteria** | `.pre-commit-config.yaml` contains `detect-private-key` or equivalent hook |
| **Effort** | S (30 minutes) |

---

#### REQ-SEC-004: Automated Dependency Updates

| Field | Value |
|-------|-------|
| **ID** | REQ-SEC-004 |
| **Statement** | The system SHALL have Dependabot configured for automated security updates of Python dependencies and GitHub Actions. |
| **Priority** | HIGH |
| **Rationale** | Manual dependency updates lead to delayed security patches. Automated updates ensure timely remediation of vulnerabilities. |
| **Gap Source** | GAP-007 (SEC-GAP-002 / CFG-GAP-004) |
| **Risk Linkage** | RSK-P0-017 (RPN: 80) |
| **Verification Method** | Inspection |
| **VR Linkage** | VR-009 |
| **Acceptance Criteria** | `.github/dependabot.yml` exists with Python and GitHub Actions configuration |
| **Effort** | S (30 minutes) |

**Configuration Template:**
```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

---

#### REQ-SEC-005: Vulnerability-Free Dependencies

| Field | Value |
|-------|-------|
| **ID** | REQ-SEC-005 |
| **Statement** | The system SHALL pass pip-audit scans with zero known vulnerabilities at release time. |
| **Priority** | MEDIUM |
| **Rationale** | Known vulnerabilities in dependencies create immediate security exposure for users. |
| **Gap Source** | Security best practices |
| **Risk Linkage** | N/A |
| **Verification Method** | Test |
| **VR Linkage** | VR-010 |
| **Acceptance Criteria** | `uv run pip-audit` returns clean with 0 vulnerabilities |
| **Effort** | S (30 minutes, may require dependency updates) |

---

#### REQ-SEC-006: Code Ownership Protection

| Field | Value |
|-------|-------|
| **ID** | REQ-SEC-006 |
| **Statement** | The system SHALL have a CODEOWNERS file designating reviewers for security-sensitive paths. |
| **Priority** | LOW |
| **Rationale** | Ensures security-sensitive changes receive appropriate review. Protects against supply chain attacks on critical paths. |
| **Gap Source** | GAP-008 (SEC-GAP-003) |
| **Risk Linkage** | N/A |
| **Verification Method** | Inspection |
| **VR Linkage** | N/A |
| **Acceptance Criteria** | `.github/CODEOWNERS` exists with coverage for `.github/`, `.claude/`, `src/` |
| **Effort** | S (30 minutes) |

---

### 3. Documentation Requirements (REQ-DOC-xxx)

---

#### REQ-DOC-001: CLAUDE.md Size Compliance

| Field | Value |
|-------|-------|
| **ID** | REQ-DOC-001 |
| **Statement** | The CLAUDE.md file SHALL be decomposed to less than 350 lines while maintaining all essential context. |
| **Priority** | CRITICAL |
| **Rationale** | Current 912 lines causes context rot, degraded Claude performance, and missed instructions. Research shows optimal performance at 75% context utilization. |
| **Gap Source** | ps-researcher-claude-md, ps-investigator INV-002 |
| **Risk Linkage** | RSK-P0-004 (RPN: 280) - HIGHEST PRIORITY |
| **Verification Method** | Analysis |
| **VR Linkage** | VR-011 |
| **Acceptance Criteria** | `wc -l CLAUDE.md` < 350 |
| **Effort** | L (4-6 hours for full decomposition) |

---

#### REQ-DOC-002: Modular Rules Structure

| Field | Value |
|-------|-------|
| **ID** | REQ-DOC-002 |
| **Statement** | The system SHALL organize Claude Code rules into modular files under `.claude/rules/` directory. |
| **Priority** | HIGH |
| **Rationale** | Enables progressive loading, reduces context window usage, and improves maintainability. Supports CLAUDE.md decomposition strategy. |
| **Gap Source** | ps-researcher-decomposition |
| **Risk Linkage** | RSK-P0-004 (RPN: 280) |
| **Verification Method** | Inspection |
| **VR Linkage** | VR-012 |
| **Acceptance Criteria** | `.claude/rules/` directory exists with domain-specific `.md` files |
| **Effort** | M (included in REQ-DOC-001) |

---

#### REQ-DOC-003: Worktracker Skill Extraction

| Field | Value |
|-------|-------|
| **ID** | REQ-DOC-003 |
| **Statement** | The worktracker entity mappings and behavior rules SHALL be moved from CLAUDE.md to the worktracker skill. |
| **Priority** | HIGH |
| **Rationale** | Worktracker content is ~370 lines (40%) of CLAUDE.md. Moving to skill reduces root context while maintaining functionality. |
| **Gap Source** | ps-investigator INV-002 |
| **Risk Linkage** | RSK-P0-004 (RPN: 280) |
| **Verification Method** | Inspection |
| **VR Linkage** | VR-013 |
| **Acceptance Criteria** | `skills/worktracker/SKILL.md` contains entity mappings; CLAUDE.md references skill |
| **Effort** | M (2 hours) |

---

#### REQ-DOC-004: Import Reference Integrity

| Field | Value |
|-------|-------|
| **ID** | REQ-DOC-004 |
| **Statement** | All `@import` or reference directives in CLAUDE.md and skill files SHALL resolve correctly (max 5 hops). |
| **Priority** | HIGH |
| **Rationale** | Broken references cause Claude to miss important context, leading to errors and poor user experience. |
| **Gap Source** | ps-researcher-decomposition |
| **Risk Linkage** | RSK-P0-004 (RPN: 280) |
| **Verification Method** | Test |
| **VR Linkage** | VR-014 |
| **Acceptance Criteria** | All referenced files exist; no circular imports; max 5 hop depth |
| **Effort** | S (1 hour for validation) |

---

#### REQ-DOC-005: Quick-Start Guide

| Field | Value |
|-------|-------|
| **ID** | REQ-DOC-005 |
| **Statement** | The README.md SHALL contain a quick-start guide enabling new users to install and run their first command in under 5 minutes. |
| **Priority** | HIGH |
| **Rationale** | First impressions are critical for OSS adoption. Users who struggle with installation often abandon projects. |
| **Gap Source** | RSK-P0-006 |
| **Risk Linkage** | RSK-P0-013 (RPN: 168) |
| **Verification Method** | Inspection |
| **VR Linkage** | VR-015 |
| **Acceptance Criteria** | README has Installation section + first command example; VAL-005 passes |
| **Effort** | M (2 hours) |

---

#### REQ-DOC-006: Code of Conduct

| Field | Value |
|-------|-------|
| **ID** | REQ-DOC-006 |
| **Statement** | The system SHALL include a CODE_OF_CONDUCT.md file establishing community behavior expectations. |
| **Priority** | MEDIUM |
| **Rationale** | Sets expectations for community interaction. Required for many corporate contribution policies. |
| **Gap Source** | GAP-005 (DOC-GAP-003) |
| **Risk Linkage** | N/A |
| **Verification Method** | Inspection |
| **VR Linkage** | N/A |
| **Acceptance Criteria** | CODE_OF_CONDUCT.md exists; based on Contributor Covenant |
| **Effort** | S (30 minutes) |

---

#### REQ-DOC-007: Change History Documentation

| Field | Value |
|-------|-------|
| **ID** | REQ-DOC-007 |
| **Statement** | The system SHALL include a CHANGELOG.md file documenting version history in Keep a Changelog format. |
| **Priority** | MEDIUM |
| **Rationale** | Users need to understand what changed between versions for upgrade decisions. Package managers reference changelogs. |
| **Gap Source** | GAP-006 (DOC-GAP-005) |
| **Risk Linkage** | N/A |
| **Verification Method** | Inspection |
| **VR Linkage** | N/A |
| **Acceptance Criteria** | CHANGELOG.md exists with v0.1.0 entry; follows Keep a Changelog format |
| **Effort** | M (2-3 hours to compile history) |

---

#### REQ-DOC-008: API Reference Documentation

| Field | Value |
|-------|-------|
| **ID** | REQ-DOC-008 |
| **Statement** | The system SHALL provide generated API reference documentation from docstrings. |
| **Priority** | LOW |
| **Rationale** | Advanced users and integrators need API documentation. Docstrings exist but aren't compiled. |
| **Gap Source** | GAP-011 (DOC-GAP-007) |
| **Risk Linkage** | RSK-P0-006 (RPN: 150) |
| **Verification Method** | Inspection |
| **VR Linkage** | N/A |
| **Acceptance Criteria** | API documentation generated via Sphinx/mkdocstrings; hosted on ReadTheDocs or GitHub Pages |
| **Effort** | L (4-6 hours initial setup) |

---

### 4. Technical Requirements (REQ-TECH-xxx)

---

#### REQ-TECH-001: SKILL.md Frontmatter Validity

| Field | Value |
|-------|-------|
| **ID** | REQ-TECH-001 |
| **Statement** | All SKILL.md files SHALL have valid YAML frontmatter containing `name`, `description`, and `version` fields. |
| **Priority** | CRITICAL |
| **Rationale** | Claude Code requires valid frontmatter to register and invoke skills. Invalid frontmatter causes skill discovery failures. |
| **Gap Source** | ps-researcher-skills |
| **Risk Linkage** | RSK-P1-001 (RPN: 80) |
| **Verification Method** | Analysis |
| **VR Linkage** | VR-016 |
| **Acceptance Criteria** | All 5 active skills have valid YAML frontmatter; no parsing errors |
| **Effort** | S (1 hour) |

---

#### REQ-TECH-002: Skill Trigger Phrases

| Field | Value |
|-------|-------|
| **ID** | REQ-TECH-002 |
| **Statement** | All SKILL.md descriptions SHALL include specific trigger phrases using "when the user asks to..." pattern. |
| **Priority** | HIGH |
| **Rationale** | Clear trigger phrases enable Claude Code to correctly identify when to invoke skills. |
| **Gap Source** | ps-researcher-skills |
| **Risk Linkage** | RSK-P1-001 (RPN: 80) |
| **Verification Method** | Inspection |
| **VR Linkage** | VR-017 |
| **Acceptance Criteria** | All skill descriptions contain activation context |
| **Effort** | S (30 minutes) |

---

#### REQ-TECH-003: P-003 Compliance (No Recursive Subagents)

| Field | Value |
|-------|-------|
| **ID** | REQ-TECH-003 |
| **Statement** | All agent files SHALL comply with Jerry Constitution P-003 (maximum ONE level of agent nesting). |
| **Priority** | HIGH |
| **Rationale** | Recursive subagents cause context explosion and violate Jerry's architectural constraints. Constitutional compliance is mandatory. |
| **Gap Source** | ps-researcher-skills, Jerry Constitution |
| **Risk Linkage** | N/A (Constitution) |
| **Verification Method** | Analysis |
| **VR Linkage** | VR-018 |
| **Acceptance Criteria** | No agent files invoke Task tool spawning further agents |
| **Effort** | S (1 hour for audit) |

---

#### REQ-TECH-004: Skill Tool Whitelisting

| Field | Value |
|-------|-------|
| **ID** | REQ-TECH-004 |
| **Statement** | All SKILL.md files SHALL specify an allowed-tools whitelist. |
| **Priority** | MEDIUM |
| **Rationale** | Tool whitelisting provides security and predictability by constraining skill capabilities. |
| **Gap Source** | ps-researcher-skills |
| **Risk Linkage** | N/A |
| **Verification Method** | Inspection |
| **VR Linkage** | VR-019 |
| **Acceptance Criteria** | SKILL.md files contain `allowed_tools` or equivalent section |
| **Effort** | S (30 minutes) |

---

#### REQ-TECH-005: Plugin Manifest Validity

| Field | Value |
|-------|-------|
| **ID** | REQ-TECH-005 |
| **Statement** | The plugin manifest (plugin.json) SHALL be valid against the Claude Code plugin schema. |
| **Priority** | HIGH |
| **Rationale** | Invalid plugin manifest prevents Jerry from being installed as a Claude Code plugin. |
| **Gap Source** | ps-researcher-plugins |
| **Risk Linkage** | N/A |
| **Verification Method** | Test |
| **VR Linkage** | VR-020 |
| **Acceptance Criteria** | JSON validates against Claude Code schema; plugin loads successfully |
| **Effort** | S (30 minutes) |

---

#### REQ-TECH-006: CLI Entry Point Functionality

| Field | Value |
|-------|-------|
| **ID** | REQ-TECH-006 |
| **Statement** | The jerry CLI entry point SHALL function correctly and display usage information. |
| **Priority** | HIGH |
| **Rationale** | CLI is the primary user interface. Non-functional CLI prevents all user interaction. |
| **Gap Source** | ps-analyst |
| **Risk Linkage** | RSK-P0-012 (RPN: 125) |
| **Verification Method** | Demonstration |
| **VR Linkage** | VR-021 |
| **Acceptance Criteria** | `uv run jerry --help` returns usage without error |
| **Effort** | S (verification only) |

---

#### REQ-TECH-007: Session Hook Execution

| Field | Value |
|-------|-------|
| **ID** | REQ-TECH-007 |
| **Statement** | The SessionStart hook SHALL execute successfully and produce valid JSON output. |
| **Priority** | HIGH |
| **Rationale** | Session hooks provide critical project context to Claude. Hook failures degrade user experience. |
| **Gap Source** | ps-researcher-claude-code |
| **Risk Linkage** | RSK-P0-012 (RPN: 125) |
| **Verification Method** | Demonstration |
| **VR Linkage** | VR-022 |
| **Acceptance Criteria** | Hook executes without error; output is valid JSON |
| **Effort** | S (verification only) |

---

#### REQ-TECH-008: Hook Output Compliance

| Field | Value |
|-------|-------|
| **ID** | REQ-TECH-008 |
| **Statement** | The hook JSON output SHALL contain both `systemMessage` and `additionalContext` fields. |
| **Priority** | HIGH |
| **Rationale** | Claude Code requires specific output format. Non-compliant output causes session initialization failures. |
| **Gap Source** | ps-researcher-claude-code |
| **Risk Linkage** | RSK-P0-012 (RPN: 125) |
| **Verification Method** | Test |
| **VR Linkage** | VR-023 |
| **Acceptance Criteria** | Output contains required fields; format matches documented specification |
| **Effort** | S (verification only) |

---

#### REQ-TECH-009: Requirements.txt Population

| Field | Value |
|-------|-------|
| **ID** | REQ-TECH-009 |
| **Statement** | The requirements.txt file SHALL contain pinned dependencies generated from pyproject.toml. |
| **Priority** | MEDIUM |
| **Rationale** | Empty requirements.txt causes pip install failures for users without uv. Pinned versions ensure reproducibility. |
| **Gap Source** | GAP-004 (DOC-GAP-006 / DEP-GAP-001), GAP-010 (DEP-GAP-002) |
| **Risk Linkage** | RSK-P0-009 (RPN: 105) |
| **Verification Method** | Inspection |
| **VR Linkage** | VR-024 |
| **Acceptance Criteria** | File non-empty; `pip install -r requirements.txt` succeeds in clean environment |
| **Effort** | S (1 hour) |

**Generation Command:**
```bash
uv pip compile pyproject.toml -o requirements.txt
```

---

### 5. Quality Requirements (REQ-QA-xxx)

---

#### REQ-QA-001: Test Suite Passing

| Field | Value |
|-------|-------|
| **ID** | REQ-QA-001 |
| **Statement** | The complete test suite SHALL pass with zero failures before release. |
| **Priority** | HIGH |
| **Rationale** | Failing tests indicate broken functionality. Releasing with failing tests damages credibility. |
| **Gap Source** | ps-analyst |
| **Risk Linkage** | RSK-P0-020 (RPN: 48) - ACCEPTED |
| **Verification Method** | Test |
| **VR Linkage** | VR-026 |
| **Acceptance Criteria** | `uv run pytest` returns exit code 0 |
| **Effort** | S (verification + fixes if needed) |

---

#### REQ-QA-002: Type Checking Compliance

| Field | Value |
|-------|-------|
| **ID** | REQ-QA-002 |
| **Statement** | The source code SHALL pass mypy type checking with zero errors. |
| **Priority** | HIGH |
| **Rationale** | Type errors indicate potential runtime bugs. Type safety improves code quality and maintainability. |
| **Gap Source** | Coding standards |
| **Risk Linkage** | N/A |
| **Verification Method** | Test |
| **VR Linkage** | VR-027 |
| **Acceptance Criteria** | `uv run mypy src/` returns 0 errors |
| **Effort** | S (verification + fixes if needed) |

---

#### REQ-QA-003: Linting Compliance

| Field | Value |
|-------|-------|
| **ID** | REQ-QA-003 |
| **Statement** | The source code SHALL pass ruff linting with zero errors. |
| **Priority** | HIGH |
| **Rationale** | Linting errors indicate code quality issues. Clean linting is expected for professional OSS projects. |
| **Gap Source** | Coding standards |
| **Risk Linkage** | N/A |
| **Verification Method** | Test |
| **VR Linkage** | VR-028 |
| **Acceptance Criteria** | `uv run ruff check src/` returns clean |
| **Effort** | S (verification + fixes if needed) |

---

#### REQ-QA-004: OSS Readiness Score

| Field | Value |
|-------|-------|
| **ID** | REQ-QA-004 |
| **Statement** | The OSS readiness score SHALL be at least 85% as measured by the requirements scoring formula. |
| **Priority** | MEDIUM |
| **Rationale** | Aggregate score ensures comprehensive readiness. 85% threshold allows minor gaps while ensuring overall quality. |
| **Gap Source** | RSK-P0-006 |
| **Risk Linkage** | RSK-P0-006 (RPN: 150) |
| **Verification Method** | Analysis |
| **VR Linkage** | VR-029 |
| **Acceptance Criteria** | Scoring formula returns >= 0.85; all CRITICAL items completed |
| **Effort** | M (aggregation of all requirements) |

---

#### REQ-QA-005: GitHub Templates

| Field | Value |
|-------|-------|
| **ID** | REQ-QA-005 |
| **Statement** | The system SHALL include GitHub issue and pull request templates. |
| **Priority** | MEDIUM |
| **Rationale** | Templates ensure consistent issue reporting and PR structure. Improves triage efficiency and contributor experience. |
| **Gap Source** | GAP-013 (DOC-GAP-008 / CFG-GAP-002), GAP-014 (CFG-GAP-003) |
| **Risk Linkage** | RSK-P0-015 (RPN: 72) |
| **Verification Method** | Inspection |
| **VR Linkage** | VR-030 |
| **Acceptance Criteria** | `.github/ISSUE_TEMPLATE/` contains bug_report.md, feature_request.md; `PULL_REQUEST_TEMPLATE.md` exists |
| **Effort** | S (1 hour) |

---

#### REQ-QA-006: Editor Configuration

| Field | Value |
|-------|-------|
| **ID** | REQ-QA-006 |
| **Statement** | The system SHALL include an .editorconfig file for consistent formatting across editors. |
| **Priority** | LOW |
| **Rationale** | Ensures consistent formatting for contributors using different editors. Reduces formatting-related PR noise. |
| **Gap Source** | GAP-012 (CFG-GAP-001) |
| **Risk Linkage** | N/A |
| **Verification Method** | Inspection |
| **VR Linkage** | N/A |
| **Acceptance Criteria** | `.editorconfig` exists with Python and Markdown settings |
| **Effort** | S (15 minutes) |

---

## L2: Requirements Strategy (Architect)

### 2.1 Traceability Matrix: Gap to Requirement

| Gap ID | Gap Description | Requirement ID | Priority |
|--------|-----------------|----------------|----------|
| GAP-001 (LIC-GAP-001) | Missing LICENSE file | REQ-LIC-001, REQ-LIC-002 | CRITICAL |
| GAP-002 (SEC-GAP-001) | Missing SECURITY.md | REQ-SEC-002 | CRITICAL |
| GAP-003 (LIC-GAP-002) | No license headers (183 files) | REQ-LIC-004 | HIGH |
| GAP-004 (DOC-GAP-006) | Empty requirements.txt | REQ-TECH-009 | MEDIUM |
| GAP-005 (DOC-GAP-003) | Missing CODE_OF_CONDUCT.md | REQ-DOC-006 | MEDIUM |
| GAP-006 (DOC-GAP-005) | Missing CHANGELOG.md | REQ-DOC-007 | MEDIUM |
| GAP-007 (SEC-GAP-002) | No Dependabot | REQ-SEC-004 | HIGH |
| GAP-008 (SEC-GAP-003) | No CODEOWNERS | REQ-SEC-006 | LOW |
| GAP-009 (LIC-GAP-003) | No SPDX identifiers | REQ-LIC-004 | HIGH |
| GAP-010 (DEP-GAP-002) | No dependency pinning | REQ-TECH-009 | MEDIUM |
| GAP-011 (DOC-GAP-007) | Missing API docs | REQ-DOC-008 | LOW |
| GAP-012 (CFG-GAP-001) | Missing .editorconfig | REQ-QA-006 | LOW |
| GAP-013 (DOC-GAP-008) | No issue templates | REQ-QA-005 | MEDIUM |
| GAP-014 (CFG-GAP-003) | No PR template | REQ-QA-005 | MEDIUM |
| GAP-015 (LIC-GAP-004) | No NOTICE file | REQ-LIC-005 | MEDIUM |
| GAP-016 (DEP-GAP-003) | No SBOM | (Deferred - CRA deadline Sept 2026) | LOW |

**Notes:**
- GAP-016 (SBOM) deferred to post-release as not blocking for initial OSS release
- 9 gaps consolidated into fewer requirements due to overlap

---

### 2.2 Traceability Matrix: Requirement to Verification

| Requirement ID | Verification ID(s) | Method | Phase |
|----------------|-------------------|--------|-------|
| REQ-LIC-001 | VR-001 | Inspection | 2 |
| REQ-LIC-002 | VR-002 | Inspection | 2 |
| REQ-LIC-003 | VR-003 | Analysis | 2 |
| REQ-LIC-004 | VR-004 | Analysis | 3 |
| REQ-LIC-006 | VR-005 | Analysis | 4 |
| REQ-LIC-007 | VR-025 | Analysis | 2 |
| REQ-SEC-001 | VR-006 | Test | 2 |
| REQ-SEC-002 | VR-007 | Inspection | 2 |
| REQ-SEC-003 | VR-008 | Inspection | 3 |
| REQ-SEC-004 | VR-009 | Inspection | 3 |
| REQ-SEC-005 | VR-010 | Test | 3 |
| REQ-DOC-001 | VR-011 | Analysis | 3 |
| REQ-DOC-002 | VR-012 | Inspection | 3 |
| REQ-DOC-003 | VR-013 | Inspection | 3 |
| REQ-DOC-004 | VR-014 | Test | 3 |
| REQ-DOC-005 | VR-015 | Inspection | 4 |
| REQ-TECH-001 | VR-016 | Analysis | 3 |
| REQ-TECH-002 | VR-017 | Inspection | 3 |
| REQ-TECH-003 | VR-018 | Analysis | 3 |
| REQ-TECH-004 | VR-019 | Inspection | 3 |
| REQ-TECH-005 | VR-020 | Test | 3 |
| REQ-TECH-006 | VR-021 | Demonstration | 3 |
| REQ-TECH-007 | VR-022 | Demonstration | 3 |
| REQ-TECH-008 | VR-023 | Test | 3 |
| REQ-TECH-009 | VR-024 | Inspection | 3 |
| REQ-QA-001 | VR-026 | Test | 3 |
| REQ-QA-002 | VR-027 | Test | 3 |
| REQ-QA-003 | VR-028 | Test | 3 |
| REQ-QA-004 | VR-029 | Analysis | 4 |
| REQ-QA-005 | VR-030 | Inspection | 4 |

---

### 2.3 Traceability Matrix: Requirement to Risk

| Requirement ID | Risk ID | RPN | Risk Reduction |
|----------------|---------|-----|----------------|
| REQ-LIC-001 | RSK-P0-001 | 60 | Eliminates release blocker |
| REQ-LIC-002 | RSK-P0-001 | 60 | Ensures legal validity |
| REQ-LIC-003 | RSK-P0-001 | 60 | Ensures consistency |
| REQ-LIC-004 | RSK-P0-007 | 105 | Enables enterprise compliance |
| REQ-LIC-006 | RSK-P0-021 | 50 | Prevents trademark conflict |
| REQ-LIC-007 | RSK-P0-010 | 36 | Validates package name |
| REQ-SEC-001 | RSK-P0-002 | 120 | Prevents security breach |
| REQ-SEC-002 | RSK-P0-003 | 144 | Enables responsible disclosure |
| REQ-SEC-004 | RSK-P0-017 | 80 | Automates security updates |
| REQ-DOC-001 | RSK-P0-004 | **280** | **Highest RPN - Critical** |
| REQ-DOC-002 | RSK-P0-004 | 280 | Supports decomposition |
| REQ-DOC-003 | RSK-P0-004 | 280 | Reduces CLAUDE.md size |
| REQ-DOC-004 | RSK-P0-004 | 280 | Ensures reference integrity |
| REQ-DOC-005 | RSK-P0-013 | 168 | Improves adoption |
| REQ-TECH-001 | RSK-P1-001 | 80 | Fixes skill metadata |
| REQ-TECH-002 | RSK-P1-001 | 80 | Improves skill activation |
| REQ-TECH-006 | RSK-P0-012 | 125 | Ensures CLI works |
| REQ-TECH-007 | RSK-P0-012 | 125 | Ensures hooks work |
| REQ-TECH-008 | RSK-P0-012 | 125 | Ensures hook compliance |
| REQ-TECH-009 | RSK-P0-009 | 105 | Enables pip install |
| REQ-QA-004 | RSK-P0-006 | 150 | Validates overall readiness |
| REQ-QA-005 | RSK-P0-015 | 72 | Improves contributor experience |

---

### 2.4 Requirements Priority Analysis

#### CRITICAL Requirements (6) - Must Complete Before Release

| ID | Description | Risk RPN | Effort |
|----|-------------|----------|--------|
| REQ-LIC-001 | LICENSE file existence | 60 | S |
| REQ-LIC-002 | LICENSE content validity | 60 | S |
| REQ-SEC-001 | Credential exposure prevention | 120 | M |
| REQ-SEC-002 | Security policy documentation | 144 | S |
| REQ-DOC-001 | CLAUDE.md size compliance | **280** | L |
| REQ-TECH-001 | SKILL.md frontmatter validity | 80 | S |

#### HIGH Requirements (16) - Should Complete Before Release

| ID | Description | Risk RPN | Effort |
|----|-------------|----------|--------|
| REQ-LIC-003 | pyproject.toml license consistency | 60 | S |
| REQ-LIC-004 | SPDX license headers | 105 | M |
| REQ-SEC-003 | Pre-commit secret detection | 120 | S |
| REQ-SEC-004 | Automated dependency updates | 80 | S |
| REQ-DOC-002 | Modular rules structure | 280 | M |
| REQ-DOC-003 | Worktracker skill extraction | 280 | M |
| REQ-DOC-004 | Import reference integrity | 280 | S |
| REQ-DOC-005 | Quick-start guide | 168 | M |
| REQ-TECH-002 | Skill trigger phrases | 80 | S |
| REQ-TECH-003 | P-003 compliance | N/A | S |
| REQ-TECH-005 | Plugin manifest validity | N/A | S |
| REQ-TECH-006 | CLI entry point functionality | 125 | S |
| REQ-TECH-007 | Session hook execution | 125 | S |
| REQ-TECH-008 | Hook output compliance | 125 | S |
| REQ-QA-001 | Test suite passing | 48 | S |
| REQ-QA-002 | Type checking compliance | N/A | S |
| REQ-QA-003 | Linting compliance | N/A | S |

---

### 2.5 Effort Summary

| T-Shirt Size | Count | Total Effort | Requirements |
|--------------|-------|--------------|--------------|
| **S** (Small) | 25 | ~12 hours | Most legal, security, verification |
| **M** (Medium) | 9 | ~18 hours | Headers, decomposition parts, docs |
| **L** (Large) | 2 | ~10 hours | CLAUDE.md decomposition, API docs |
| **Total** | **36** | **~40 hours** | ~5 person-days |

---

### 2.6 Implementation Sequence

#### Phase 2A: Blockers (Day 1) - 4 hours

| Seq | Requirement | Action | Duration |
|-----|-------------|--------|----------|
| 1 | REQ-LIC-001, REQ-LIC-002 | Create MIT LICENSE file | 30 min |
| 2 | REQ-SEC-001 | Run Gitleaks full history scan | 2 hours |
| 3 | REQ-LIC-007 | Verify PyPI name availability | 15 min |
| 4 | REQ-TECH-001 | Fix worktracker SKILL.md metadata | 15 min |
| 5 | REQ-SEC-002 | Create SECURITY.md | 1 hour |

#### Phase 2B: Core Decomposition (Days 2-3) - 8 hours

| Seq | Requirement | Action | Duration |
|-----|-------------|--------|----------|
| 6 | REQ-DOC-001 | Begin CLAUDE.md decomposition | 4 hours |
| 7 | REQ-DOC-002 | Create modular rules structure | (included) |
| 8 | REQ-DOC-003 | Extract worktracker to skill | 2 hours |
| 9 | REQ-DOC-004 | Validate import references | 1 hour |
| 10 | REQ-TECH-009 | Generate requirements.txt | 1 hour |

#### Phase 3: Quality Gates (Days 4-5) - 10 hours

| Seq | Requirement | Action | Duration |
|-----|-------------|--------|----------|
| 11 | REQ-LIC-004 | Add SPDX headers to 183 files | 3 hours |
| 12 | REQ-SEC-003 | Configure pre-commit secret detection | 30 min |
| 13 | REQ-SEC-004 | Configure dependabot.yml | 30 min |
| 14 | REQ-DOC-005 | Complete quick-start guide | 2 hours |
| 15 | REQ-QA-001-003 | Verify tests, types, linting | 2 hours |
| 16 | REQ-TECH-006-008 | Verify CLI and hooks | 1 hour |
| 17 | REQ-TECH-002-005 | Verify skill structure | 1 hour |

#### Phase 4: Polish (Days 5-7) - 6 hours

| Seq | Requirement | Action | Duration |
|-----|-------------|--------|----------|
| 18 | REQ-LIC-005 | Create NOTICE file | 1 hour |
| 19 | REQ-DOC-006 | Add CODE_OF_CONDUCT.md | 30 min |
| 20 | REQ-DOC-007 | Create CHANGELOG.md | 2 hours |
| 21 | REQ-QA-005 | Create GitHub templates | 1 hour |
| 22 | REQ-QA-006 | Add .editorconfig | 15 min |
| 23 | REQ-LIC-006 | Conduct trademark search | 1 hour |
| 24 | REQ-QA-004 | Validate OSS readiness >= 85% | 30 min |

---

### 2.7 NPR 7123.1D Compliance Statement

This requirements specification complies with NASA NPR 7123.1D Section 5.2 (Requirements Analysis):

| NPR Requirement | Compliance | Evidence |
|-----------------|------------|----------|
| 5.2.1 Requirements shall be necessary | Each requirement traces to gap or risk | Traceability matrices |
| 5.2.2 Requirements shall be verifiable | All have verification method and criteria | VR linkage column |
| 5.2.3 Requirements shall be achievable | Effort estimates provided; all S/M/L | Effort column |
| 5.2.4 Requirements shall be traceable | Forward (to VR) and backward (to gap/risk) | Section 2.1-2.3 |
| 5.2.5 Requirements shall be unambiguous | SHALL statements with measurable criteria | Acceptance criteria |
| 5.2.6 Requirements shall be prioritized | CRITICAL/HIGH/MEDIUM/LOW | Priority column |

---

## Appendix A: Requirements Summary Table

| ID | Statement Summary | Priority | Risk | VR | Effort |
|----|-------------------|----------|------|----|----|
| REQ-LIC-001 | LICENSE file exists | CRITICAL | RSK-P0-001 | VR-001 | S |
| REQ-LIC-002 | LICENSE content valid | CRITICAL | RSK-P0-001 | VR-002 | S |
| REQ-LIC-003 | pyproject.toml matches | HIGH | RSK-P0-001 | VR-003 | S |
| REQ-LIC-004 | SPDX headers 183 files | HIGH | RSK-P0-007 | VR-004 | M |
| REQ-LIC-005 | NOTICE file exists | MEDIUM | - | - | S |
| REQ-LIC-006 | Trademark verified | MEDIUM | RSK-P0-021 | VR-005 | S |
| REQ-LIC-007 | PyPI name available | LOW | RSK-P0-010 | VR-025 | S |
| REQ-SEC-001 | Zero credentials in history | CRITICAL | RSK-P0-002 | VR-006 | M |
| REQ-SEC-002 | SECURITY.md exists | CRITICAL | RSK-P0-003 | VR-007 | S |
| REQ-SEC-003 | Pre-commit secrets hook | HIGH | RSK-P0-002 | VR-008 | S |
| REQ-SEC-004 | Dependabot configured | HIGH | RSK-P0-017 | VR-009 | S |
| REQ-SEC-005 | Zero vulnerabilities | MEDIUM | - | VR-010 | S |
| REQ-SEC-006 | CODEOWNERS exists | LOW | - | - | S |
| REQ-DOC-001 | CLAUDE.md < 350 lines | CRITICAL | RSK-P0-004 | VR-011 | L |
| REQ-DOC-002 | Modular rules structure | HIGH | RSK-P0-004 | VR-012 | M |
| REQ-DOC-003 | Worktracker in skill | HIGH | RSK-P0-004 | VR-013 | M |
| REQ-DOC-004 | Imports resolve | HIGH | RSK-P0-004 | VR-014 | S |
| REQ-DOC-005 | Quick-start guide | HIGH | RSK-P0-013 | VR-015 | M |
| REQ-DOC-006 | CODE_OF_CONDUCT.md | MEDIUM | - | - | S |
| REQ-DOC-007 | CHANGELOG.md | MEDIUM | - | - | M |
| REQ-DOC-008 | API reference docs | LOW | RSK-P0-006 | - | L |
| REQ-TECH-001 | SKILL.md frontmatter valid | CRITICAL | RSK-P1-001 | VR-016 | S |
| REQ-TECH-002 | Skill trigger phrases | HIGH | RSK-P1-001 | VR-017 | S |
| REQ-TECH-003 | P-003 compliance | HIGH | - | VR-018 | S |
| REQ-TECH-004 | Tool whitelisting | MEDIUM | - | VR-019 | S |
| REQ-TECH-005 | Plugin manifest valid | HIGH | - | VR-020 | S |
| REQ-TECH-006 | CLI works | HIGH | RSK-P0-012 | VR-021 | S |
| REQ-TECH-007 | Hooks execute | HIGH | RSK-P0-012 | VR-022 | S |
| REQ-TECH-008 | Hook output compliant | HIGH | RSK-P0-012 | VR-023 | S |
| REQ-TECH-009 | requirements.txt valid | MEDIUM | RSK-P0-009 | VR-024 | S |
| REQ-QA-001 | Tests pass | HIGH | RSK-P0-020 | VR-026 | S |
| REQ-QA-002 | Type check passes | HIGH | - | VR-027 | S |
| REQ-QA-003 | Linting passes | HIGH | - | VR-028 | S |
| REQ-QA-004 | OSS readiness >= 85% | MEDIUM | RSK-P0-006 | VR-029 | M |
| REQ-QA-005 | GitHub templates | MEDIUM | RSK-P0-015 | VR-030 | S |
| REQ-QA-006 | .editorconfig | LOW | - | - | S |

---

## Appendix B: Deferred Requirements

The following items were identified but deferred:

| Item | Reason | Target |
|------|--------|--------|
| SBOM Generation (GAP-016) | EU CRA deadline Sept 2026; not blocking | Post-release |
| API Documentation Hosting | Nice-to-have; not blocking | Post-release |
| Trademark Registration | Verification sufficient; registration if needed | If conflicts found |

---

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | PROJ-001-REQ-SPEC-001 |
| **Status** | DRAFT |
| **Agent** | nse-requirements |
| **Total Requirements** | 36 |
| **CRITICAL Requirements** | 6 |
| **HIGH Requirements** | 16 |
| **MEDIUM Requirements** | 9 |
| **LOW Requirements** | 5 |
| **Gaps Converted** | 16 of 18 unique gaps |
| **Risks Linked** | 15 of 22 risks |
| **VRs Linked** | 30 of 30 VRs |
| **Estimated Effort** | ~40 hours (~5 person-days) |
| **NPR 7123.1D Compliance** | Section 5.2 (Requirements Analysis) |
| **Word Count** | ~7,500 |

---

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-31 | nse-requirements | Initial requirements specification |

---

*This document was produced by nse-requirements agent as part of Phase 2 Tier 1 for PROJ-001-oss-release.*
*Constitutional Compliance: P-001 (Truth), P-002 (Persistence), P-004 (Provenance), P-011 (Evidence)*
