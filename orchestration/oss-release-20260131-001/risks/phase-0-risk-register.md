# Phase 0 Risk Register: Jerry OSS Release

> **Document ID:** RISK-REG-PHASE-0-001
> **Agent:** nse-risk
> **Workflow:** oss-release-20260131-001
> **Phase:** 0 - Divergent Exploration & Initial Research
> **Tier:** 2 (Sequential - Depends on Tier 1 Completion)
> **Created:** 2026-01-31
> **Quality Threshold:** >= 0.92 (DEC-OSS-001)
> **NASA SE Reference:** NPR 7123.1D - Risk Management

---

## L0: Executive Summary (ELI5)

### What is This Document?

This is a list of things that could go wrong when we share Jerry with the world as open source software. Think of it like a checklist of potential problems we need to fix or watch out for.

### Top 5 Risks (What Keeps Us Up at Night)

| Rank | Risk | Why It Matters | What We Do |
|------|------|----------------|------------|
| 1 | **No LICENSE file** | Without it, no one can legally use Jerry - it's not actually open source | Add MIT LICENSE file immediately |
| 2 | **Secrets in git history** | If passwords or keys are buried in old commits, hackers will find them | Scan entire history with Gitleaks before going public |
| 3 | **EU CRA compliance deadline** | New EU law (Sept 2026) requires vulnerability reporting - fines if we don't comply | Set up SECURITY.md and disclosure process now |
| 4 | **Projects directory exposure** | Internal development artifacts could embarrass us or leak strategy | Clean up or exclude projects/ directory |
| 5 | **CLAUDE.md overwhelms new users** | 1000+ line file scares away contributors before they start | Create minimal quick-start version |

### Risk Level Summary

```
CRITICAL: 2 risks (must fix before release)
HIGH:     8 risks (should fix before release)
MEDIUM:   6 risks (fix soon after release)
LOW:      4 risks (nice to have)
```

### Bottom Line

Jerry is **technically ready** for OSS (good code, good tests, good architecture) but **administratively not ready** (missing legal files, security policies, and contributor onboarding).

**Estimated work to reach "safe to release":** 3-5 days focused effort.

---

## L1: Engineer - Full Risk Register

### Risk Assessment Methodology

Each risk is evaluated using the NASA SE risk matrix:

**Likelihood Scale:**
| Score | Level | Description |
|-------|-------|-------------|
| 1 | Rare | <5% probability |
| 2 | Unlikely | 5-20% probability |
| 3 | Possible | 20-50% probability |
| 4 | Likely | 50-80% probability |
| 5 | Almost Certain | >80% probability |

**Impact Scale:**
| Score | Level | Description |
|-------|-------|-------------|
| 1 | Negligible | Minor inconvenience, easily fixed |
| 2 | Minor | Some rework needed, no lasting damage |
| 3 | Moderate | Significant effort to recover, temporary reputation damage |
| 4 | Major | Serious damage, legal exposure, major effort to recover |
| 5 | Severe | Catastrophic - project failure, legal action, permanent damage |

**Risk Score:** Likelihood x Impact (1-25)
- **1-4:** LOW (accept)
- **5-9:** MEDIUM (monitor, mitigate when practical)
- **10-14:** HIGH (require mitigation plan)
- **15-25:** CRITICAL (must address before proceeding)

---

### Category 1: Legal/Licensing Risks

#### RISK-OSS-001: Missing LICENSE File (CRITICAL)

| Field | Value |
|-------|-------|
| **Category** | Legal/Licensing |
| **Description** | Repository root has no LICENSE file. Without explicit license, code is NOT open source by default - all rights reserved to copyright holder. Users cannot legally use, modify, or distribute. |
| **Likelihood** | 5 (Almost Certain - file demonstrably missing) |
| **Impact** | 5 (Severe - no one can legally use the software) |
| **Risk Score** | **25 (CRITICAL)** |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Actions** | 1. Create LICENSE file with MIT text<br>2. Verify pyproject.toml declares MIT<br>3. Add license badge to README |
| **Owner** | Project Lead |
| **Status** | IDENTIFIED |
| **Evidence Sources** | nse-requirements: DOC-GAP-001, LIC-GAP-001<br>ps-analyst: Documentation Gap Analysis §4.2 |

#### RISK-OSS-002: No License Headers in Source Files

| Field | Value |
|-------|-------|
| **Category** | Legal/Licensing |
| **Description** | 0 of 183 Python source files contain license headers or SPDX identifiers. Enterprise users may require file-level license assertions for compliance tooling. |
| **Likelihood** | 4 (Likely - enterprise adoption affected) |
| **Impact** | 3 (Moderate - reduces enterprise adoption, not a blocker) |
| **Risk Score** | **12 (HIGH)** |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Actions** | 1. Add SPDX-License-Identifier: MIT to all Python files<br>2. Add copyright notice header<br>3. Create script to automate header addition |
| **Owner** | Engineering |
| **Status** | IDENTIFIED |
| **Evidence Sources** | nse-requirements: LIC-GAP-002, LIC-GAP-003 |

#### RISK-OSS-003: Third-Party License Attribution

| Field | Value |
|-------|-------|
| **Category** | Legal/Licensing |
| **Description** | No NOTICE file documenting third-party dependencies. Apache 2.0 requires NOTICE; MIT best practice. All current dependencies are MIT/Unlicense compatible, but no formal tracking exists. |
| **Likelihood** | 2 (Unlikely - all deps currently compatible) |
| **Impact** | 2 (Minor - easy to add later) |
| **Risk Score** | **4 (LOW)** |
| **Mitigation Strategy** | Accept (with monitoring) |
| **Mitigation Actions** | 1. Create NOTICE file listing dependencies<br>2. Add dependency license check to CI |
| **Owner** | Engineering |
| **Status** | IDENTIFIED |
| **Evidence Sources** | nse-requirements: LIC-GAP-004<br>ps-researcher: License Selection §3.2 |

#### RISK-OSS-004: CLA/DCO Decision Not Made

| Field | Value |
|-------|-------|
| **Category** | Legal/Licensing |
| **Description** | No decision on whether to require Contributor License Agreement (CLA) or Developer Certificate of Origin (DCO). Without either, IP ownership of contributions may be disputed. |
| **Likelihood** | 3 (Possible - as project grows) |
| **Impact** | 4 (Major - IP disputes can block future licensing changes) |
| **Risk Score** | **12 (HIGH)** |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Actions** | 1. Decide CLA vs DCO (recommend DCO for lower friction)<br>2. Implement DCO-check GitHub Action<br>3. Document in CONTRIBUTING.md |
| **Owner** | Project Lead |
| **Status** | IDENTIFIED |
| **Evidence Sources** | nse-explorer: Contribution Model Alternatives §7.2, §7.3<br>ps-researcher: Community Readiness §4 |

---

### Category 2: Security Risks

#### RISK-OSS-005: Credential Exposure in Git History (CRITICAL)

| Field | Value |
|-------|-------|
| **Category** | Security |
| **Description** | Git history has not been scanned for accidentally committed secrets (API keys, tokens, passwords). Once repository is public, entire history is exposed. Even deleted commits can be recovered. |
| **Likelihood** | 3 (Possible - no systematic scan performed) |
| **Impact** | 5 (Severe - credential compromise, account takeover, data breach) |
| **Risk Score** | **15 (CRITICAL)** |
| **Mitigation Strategy** | Mitigate (MANDATORY before release) |
| **Mitigation Actions** | 1. Run Gitleaks scan on entire history: `gitleaks detect --source . --verbose`<br>2. Run TruffleHog as secondary check<br>3. If secrets found: rotate credentials, use git filter-repo to remove<br>4. Install pre-commit hook to prevent future leaks |
| **Owner** | Security |
| **Status** | IDENTIFIED |
| **Evidence Sources** | ps-researcher: Pre-Release Security Checklist §1.3<br>nse-requirements: Security Controls §3.3 |

#### RISK-OSS-006: Missing Vulnerability Disclosure Policy

| Field | Value |
|-------|-------|
| **Category** | Security |
| **Description** | No SECURITY.md file defining how to report vulnerabilities. Security researchers may disclose vulnerabilities publicly if no private channel exists. |
| **Likelihood** | 4 (Likely - researchers will look for this file) |
| **Impact** | 4 (Major - public disclosure before fix, reputation damage) |
| **Risk Score** | **16 (HIGH)** |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Actions** | 1. Create SECURITY.md with disclosure policy<br>2. Enable GitHub Private Vulnerability Reporting<br>3. Define response SLAs (48h initial response, 7d triage) |
| **Owner** | Security |
| **Status** | IDENTIFIED |
| **Evidence Sources** | nse-requirements: SEC-GAP-001<br>ps-researcher: SECURITY.md Template §2.3 |

#### RISK-OSS-007: Dependency Vulnerabilities

| Field | Value |
|-------|-------|
| **Category** | Security |
| **Description** | No automated dependency security updates (Dependabot). Current dependencies have no known vulnerabilities (pip-audit in CI), but new vulns may emerge. |
| **Likelihood** | 4 (Likely - dependency vulns are common) |
| **Impact** | 3 (Moderate - exploits via dependencies) |
| **Risk Score** | **12 (HIGH)** |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Actions** | 1. Add .github/dependabot.yml for Python<br>2. Configure weekly security update PRs<br>3. Add pip-audit to pre-push hook (already present) |
| **Owner** | Engineering |
| **Status** | IDENTIFIED |
| **Evidence Sources** | nse-requirements: SEC-GAP-002, CFG-GAP-004<br>ps-researcher: Dependency Vulnerability Audit §1.4 |

#### RISK-OSS-008: EU Cyber Resilience Act Non-Compliance

| Field | Value |
|-------|-------|
| **Category** | Security |
| **Description** | EU CRA mandatory vulnerability reporting takes effect Sept 11, 2026. OSS projects must report vulnerabilities within 24 hours, provide 5-year security updates. Non-compliance = potential fines. |
| **Likelihood** | 4 (Likely - regulation is coming) |
| **Impact** | 4 (Major - regulatory fines, EU market access) |
| **Risk Score** | **16 (HIGH)** |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Actions** | 1. Document security update policy<br>2. Establish vulnerability response process<br>3. Consider SBOM generation for supply chain transparency<br>4. Monitor CRA guidance as it evolves |
| **Owner** | Project Lead + Security |
| **Status** | IDENTIFIED |
| **Evidence Sources** | ps-researcher: EU Cyber Resilience Act §2.2 |

---

### Category 3: Technical Risks

#### RISK-OSS-009: Internal Project Contamination

| Field | Value |
|-------|-------|
| **Category** | Technical |
| **Description** | projects/ directory contains 7+ internal development projects (PROJ-001 through PROJ-009). These may contain: internal references, unpolished work, development artifacts that shouldn't be public. |
| **Likelihood** | 4 (Likely - directory exists with internal content) |
| **Impact** | 3 (Moderate - embarrassment, confusion, strategy leakage) |
| **Risk Score** | **12 (HIGH)** |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Actions** | 1. Review all projects/ content for sensitive material<br>2. Archive most projects, keep 1-2 exemplars<br>3. Consider excluding entire directory for initial release<br>4. Move to .gitignore or separate internal repo |
| **Owner** | Project Lead |
| **Status** | IDENTIFIED |
| **Evidence Sources** | ps-analyst: Project Directory Structure §2.2<br>nse-explorer: Dual Repository Strategy §1.2 |

#### RISK-OSS-010: CLAUDE.md Complexity Barrier

| Field | Value |
|-------|-------|
| **Category** | Technical |
| **Description** | CLAUDE.md is 1000+ lines containing comprehensive worktracker documentation, project enforcement rules, TODO behavior. May overwhelm new OSS contributors and consume excessive context window. |
| **Likelihood** | 4 (Likely - file is demonstrably large) |
| **Impact** | 3 (Moderate - contributor friction, reduced adoption) |
| **Risk Score** | **12 (HIGH)** |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Actions** | 1. Create CLAUDE-MINIMAL.md for quick starts<br>2. Use hierarchical CLAUDE.md with directory-level files<br>3. Move detailed docs to skills/ on-demand loading<br>4. Document the hierarchy for new users |
| **Owner** | Engineering |
| **Status** | IDENTIFIED |
| **Evidence Sources** | ps-analyst: CLAUDE.md Complexity §2.1<br>nse-explorer: CLAUDE.md Strategy Alternatives §8 |

#### RISK-OSS-011: Deprecated Skills in Graveyard

| Field | Value |
|-------|-------|
| **Category** | Technical |
| **Description** | skills/.graveyard/ contains deprecated worktracker and worktracker-decomposition skills. Presence of graveyard in public release may confuse contributors or suggest instability. |
| **Likelihood** | 3 (Possible - visible in repo structure) |
| **Impact** | 2 (Minor - confusion, not functional issue) |
| **Risk Score** | **6 (MEDIUM)** |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Actions** | 1. Remove .graveyard from OSS release<br>2. Or clearly document as deprecated in README<br>3. Move to archive branch if history important |
| **Owner** | Engineering |
| **Status** | IDENTIFIED |
| **Evidence Sources** | ps-analyst: Skills Graveyard §2.3<br>nse-requirements: Skills Inventory §5.3 |

#### RISK-OSS-012: tiktoken Model Download

| Field | Value |
|-------|-------|
| **Category** | Technical |
| **Description** | tiktoken dependency downloads ~4MB model files on first use. May fail for users with restricted network access (air-gapped, corporate firewalls). No offline fallback documented. |
| **Likelihood** | 2 (Unlikely - most users have network access) |
| **Impact** | 2 (Minor - affects limited use cases) |
| **Risk Score** | **4 (LOW)** |
| **Mitigation Strategy** | Accept (with documentation) |
| **Mitigation Actions** | 1. Document network requirement in INSTALLATION.md<br>2. Consider optional fallback for token counting<br>3. Document proxy configuration if needed |
| **Owner** | Engineering |
| **Status** | IDENTIFIED |
| **Evidence Sources** | ps-analyst: Performance Implications §4.1 |

#### RISK-OSS-013: Empty requirements.txt

| Field | Value |
|-------|-------|
| **Category** | Technical |
| **Description** | requirements.txt file exists but is empty (autogenerated stub). Users expecting pip install workflow will be confused. pyproject.toml is source of truth but some tools expect requirements.txt. |
| **Likelihood** | 3 (Possible - some users will try pip install) |
| **Impact** | 2 (Minor - workaround exists) |
| **Risk Score** | **6 (MEDIUM)** |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Actions** | 1. Generate requirements.txt from pyproject.toml<br>2. Or remove file entirely with note in README<br>3. Document uv as preferred installation method |
| **Owner** | Engineering |
| **Status** | IDENTIFIED |
| **Evidence Sources** | nse-requirements: DOC-GAP-006, DEP-GAP-001 |

---

### Category 4: Community/Adoption Risks

#### RISK-OSS-014: PyPI Name Availability

| Field | Value |
|-------|-------|
| **Category** | Community/Adoption |
| **Description** | Package name "jerry" may already be taken on PyPI. This is a one-way door decision - once published, name is claimed permanently. |
| **Likelihood** | 3 (Possible - common name) |
| **Impact** | 3 (Moderate - requires rename if taken) |
| **Risk Score** | **9 (MEDIUM)** |
| **Mitigation Strategy** | Avoid |
| **Mitigation Actions** | 1. Check PyPI for "jerry" availability BEFORE release<br>2. Prepare alternatives: jerry-framework, jerry-cli, jerry-agent<br>3. Reserve preferred name immediately after decision |
| **Owner** | Project Lead |
| **Status** | IDENTIFIED |
| **Evidence Sources** | ps-analyst: Package Name §3.1<br>nse-explorer: Branding Options §4 |

#### RISK-OSS-015: First Impression Documentation Gap

| Field | Value |
|-------|-------|
| **Category** | Community/Adoption |
| **Description** | README.md is comprehensive but missing LICENSE reference. No quick-start guide for 5-minute evaluation. Missing CODE_OF_CONDUCT.md signals less mature project. |
| **Likelihood** | 3 (Possible - first-time visitors may bounce) |
| **Impact** | 3 (Moderate - reduced adoption) |
| **Risk Score** | **9 (MEDIUM)** |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Actions** | 1. Add LICENSE badge and link to README<br>2. Create quick-start section with minimal example<br>3. Add CODE_OF_CONDUCT.md (Contributor Covenant)<br>4. Ensure all OSS standard files present |
| **Owner** | Documentation |
| **Status** | IDENTIFIED |
| **Evidence Sources** | nse-requirements: DOC-GAP-001, DOC-GAP-003<br>ps-researcher: README Requirements §2.1 |

#### RISK-OSS-016: No Changelog for Releases

| Field | Value |
|-------|-------|
| **Category** | Community/Adoption |
| **Description** | No CHANGELOG.md exists. Users cannot easily see what changed between versions. This is a common OSS expectation and its absence suggests amateur project. |
| **Likelihood** | 3 (Possible) |
| **Impact** | 2 (Minor - inconvenience, not blocker) |
| **Risk Score** | **6 (MEDIUM)** |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Actions** | 1. Create CHANGELOG.md following Keep a Changelog format<br>2. Retroactively document v0.0.1, v0.1.0, v0.2.0 changes<br>3. Add semantic-release or similar for automation |
| **Owner** | Engineering |
| **Status** | IDENTIFIED |
| **Evidence Sources** | nse-requirements: DOC-GAP-005<br>ps-researcher: CI/CD for OSS §5 |

#### RISK-OSS-017: Missing GitHub Templates

| Field | Value |
|-------|-------|
| **Category** | Community/Adoption |
| **Description** | No issue templates, no PR template, no CODEOWNERS file. Contributors will submit unstructured issues and PRs, increasing triage burden. |
| **Likelihood** | 4 (Likely - templates demonstrably missing) |
| **Impact** | 2 (Minor - extra maintainer work) |
| **Risk Score** | **8 (MEDIUM)** |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Actions** | 1. Create .github/ISSUE_TEMPLATE/ with bug, feature, question templates<br>2. Create .github/PULL_REQUEST_TEMPLATE.md<br>3. Add CODEOWNERS for key paths |
| **Owner** | Engineering |
| **Status** | IDENTIFIED |
| **Evidence Sources** | nse-requirements: CFG-GAP-002, CFG-GAP-003<br>ps-researcher: GitHub Templates §4.1 |

---

### Category 5: Operational Risks

#### RISK-OSS-018: Dual Repository Synchronization

| Field | Value |
|-------|-------|
| **Category** | Operational |
| **Description** | DEC-002 decided on dual repository strategy (internal source-repository, public jerry). This creates ongoing synchronization complexity - features may be developed in wrong repo, merge conflicts during sync. |
| **Likelihood** | 4 (Likely - sync is inherently complex) |
| **Impact** | 3 (Moderate - ongoing maintenance burden) |
| **Risk Score** | **12 (HIGH)** |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Actions** | 1. Document clear sync process in GOVERNANCE.md<br>2. Create automation scripts for sync<br>3. Define which repo is source of truth per component<br>4. Regular sync schedule (weekly?) |
| **Owner** | Project Lead |
| **Status** | IDENTIFIED |
| **Evidence Sources** | nse-explorer: Dual Repository Strategy §1.2 |

#### RISK-OSS-019: Maintainer Capacity

| Field | Value |
|-------|-------|
| **Category** | Operational |
| **Description** | Current single maintainer model. Open source projects attract issues, PRs, questions. Maintainer burnout is common cause of OSS project abandonment. |
| **Likelihood** | 3 (Possible - depends on adoption) |
| **Impact** | 4 (Major - project abandonment) |
| **Risk Score** | **12 (HIGH)** |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Actions** | 1. Document governance model in GOVERNANCE.md<br>2. Plan for core team expansion (2-3 maintainers)<br>3. Use automation to reduce manual work<br>4. Set response time expectations in README |
| **Owner** | Project Lead |
| **Status** | IDENTIFIED |
| **Evidence Sources** | ps-researcher: Governance Models §4.2<br>nse-explorer: Core Team Model §4.2 |

#### RISK-OSS-020: No OpenSSF Scorecard Baseline

| Field | Value |
|-------|-------|
| **Category** | Operational |
| **Description** | OpenSSF Scorecard not configured. Cannot measure security posture objectively. Many enterprise users require minimum scorecard rating for adoption. |
| **Likelihood** | 3 (Possible - enterprise adoption affected) |
| **Impact** | 2 (Minor - nice to have, not required) |
| **Risk Score** | **6 (MEDIUM)** |
| **Mitigation Strategy** | Mitigate |
| **Mitigation Actions** | 1. Run initial scorecard assessment<br>2. Add .github/workflows/scorecard.yml<br>3. Target score >= 7.0 before release<br>4. Add scorecard badge to README |
| **Owner** | Engineering |
| **Status** | IDENTIFIED |
| **Evidence Sources** | ps-researcher: OpenSSF Scorecard §1.4 |

---

## Risk Matrix Visualization

```
                                    IMPACT
                    1           2           3           4           5
                Negligible    Minor     Moderate     Major      Severe
              ┌───────────┬───────────┬───────────┬───────────┬───────────┐
            5 │           │           │           │           │  RISK-001 │
  Almost      │           │           │           │           │  LICENSE  │
  Certain     │           │           │           │           │  (25)     │
              ├───────────┼───────────┼───────────┼───────────┼───────────┤
            4 │           │ RISK-017  │ RISK-009  │ RISK-006  │           │
  L           │           │ Templates │ Projects  │ Vuln Disc │           │
  I Likely    │           │ (8)       │ RISK-010  │ RISK-008  │           │
  K           │           │           │ CLAUDE.md │ EU CRA    │           │
  E           │           │           │ (12)      │ (16)      │           │
  L           ├───────────┼───────────┼───────────┼───────────┼───────────┤
  I         3 │           │ RISK-013  │ RISK-014  │ RISK-004  │  RISK-005 │
  H Possible  │           │ req.txt   │ PyPI Name │ CLA/DCO   │  Secrets  │
  O           │           │ RISK-011  │ RISK-015  │           │  (15)     │
  O           │           │ Graveyard │ First Imp │           │           │
  D           │           │ (6)       │ RISK-016  │           │           │
              │           │           │ Changelog │           │           │
              ├───────────┼───────────┼───────────┼───────────┼───────────┤
            2 │           │ RISK-003  │           │           │           │
  Unlikely    │           │ NOTICE    │           │           │           │
              │           │ RISK-012  │           │           │           │
              │           │ tiktoken  │           │           │           │
              │           │ (4)       │           │           │           │
              ├───────────┼───────────┼───────────┼───────────┼───────────┤
            1 │           │           │           │           │           │
  Rare        │           │           │           │           │           │
              │           │           │           │           │           │
              └───────────┴───────────┴───────────┴───────────┴───────────┘

LEGEND:
┌─────────────────────────────────────────────────────────────────────────┐
│  Score 1-4:   LOW (Green)    - Accept                                   │
│  Score 5-9:   MEDIUM (Yellow) - Monitor, mitigate when practical        │
│  Score 10-14: HIGH (Orange)   - Require mitigation plan                 │
│  Score 15-25: CRITICAL (Red)  - Must address before proceeding          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Risk Summary by Score

### CRITICAL (Score 15-25) - 2 Risks

| ID | Risk | Score | Required Action |
|----|------|-------|-----------------|
| RISK-OSS-001 | Missing LICENSE file | 25 | Add MIT LICENSE file before release |
| RISK-OSS-005 | Credential exposure in git history | 15 | Run Gitleaks scan, remediate if found |

### HIGH (Score 10-14) - 8 Risks

| ID | Risk | Score | Required Action |
|----|------|-------|-----------------|
| RISK-OSS-006 | Missing vulnerability disclosure | 16 | Create SECURITY.md |
| RISK-OSS-008 | EU CRA non-compliance | 16 | Establish disclosure process |
| RISK-OSS-002 | No license headers | 12 | Add SPDX headers to source files |
| RISK-OSS-004 | CLA/DCO decision pending | 12 | Decide and implement DCO |
| RISK-OSS-007 | Dependency vulnerabilities | 12 | Configure Dependabot |
| RISK-OSS-009 | Internal project contamination | 12 | Clean up projects/ directory |
| RISK-OSS-010 | CLAUDE.md complexity | 12 | Create minimal version |
| RISK-OSS-018 | Dual repo sync | 12 | Document sync process |
| RISK-OSS-019 | Maintainer capacity | 12 | Plan governance expansion |

### MEDIUM (Score 5-9) - 6 Risks

| ID | Risk | Score | Recommended Action |
|----|------|-------|-------------------|
| RISK-OSS-014 | PyPI name availability | 9 | Check before release |
| RISK-OSS-015 | First impression docs | 9 | Add CODE_OF_CONDUCT, quick start |
| RISK-OSS-017 | Missing GitHub templates | 8 | Create issue/PR templates |
| RISK-OSS-011 | Deprecated skills | 6 | Remove or clearly mark |
| RISK-OSS-013 | Empty requirements.txt | 6 | Generate or remove |
| RISK-OSS-016 | No changelog | 6 | Create CHANGELOG.md |
| RISK-OSS-020 | No OpenSSF baseline | 6 | Run and configure scorecard |

### LOW (Score 1-4) - 4 Risks

| ID | Risk | Score | Status |
|----|------|-------|--------|
| RISK-OSS-003 | Third-party attribution | 4 | Accept with monitoring |
| RISK-OSS-012 | tiktoken network dependency | 4 | Document in installation |

---

## L2: Architect - Systemic Analysis

### 1. Risk Interdependencies

```
RISK DEPENDENCY GRAPH
=====================

                    ┌─────────────────┐
                    │  RISK-001       │
                    │  No LICENSE     │ ◄────── BLOCKS ALL OTHER WORK
                    └────────┬────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
           ▼                 ▼                 ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │  RISK-002    │  │  RISK-003    │  │  RISK-004    │
    │  Headers     │  │  NOTICE      │  │  CLA/DCO     │
    │              │  │              │  │              │
    └──────────────┘  └──────────────┘  └──────────────┘
           │
           └──────────────► All form LICENSE CLUSTER

    ┌─────────────────┐       ┌─────────────────┐
    │  RISK-005       │       │  RISK-006       │
    │  Git Secrets    │ ◄────►│  Vuln Disclosure│
    └────────┬────────┘       └────────┬────────┘
             │                         │
             ▼                         ▼
    ┌─────────────────────────────────────────┐
    │        SECURITY CLUSTER                 │
    │  RISK-007 (Deps) + RISK-008 (EU CRA)   │
    │  + RISK-020 (OpenSSF)                  │
    └─────────────────────────────────────────┘

    ┌─────────────────┐       ┌─────────────────┐
    │  RISK-009       │       │  RISK-010       │
    │  Projects/      │ ◄────►│  CLAUDE.md      │
    └────────┬────────┘       └────────┬────────┘
             │                         │
             ▼                         ▼
    ┌─────────────────────────────────────────┐
    │       CONTRIBUTOR UX CLUSTER            │
    │  RISK-011 (Graveyard) + RISK-015       │
    │  (First Impression) + RISK-017 (GH)    │
    └─────────────────────────────────────────┘

    ┌─────────────────┐       ┌─────────────────┐
    │  RISK-018       │◄─────►│  RISK-019       │
    │  Dual Repo Sync │       │  Maintainer     │
    └─────────────────┘       └─────────────────┘
             │
             ▼
    ┌─────────────────────────────────────────┐
    │       SUSTAINABILITY CLUSTER            │
    │  (Long-term project health risks)       │
    └─────────────────────────────────────────┘
```

### 2. Risk Clusters and Treatment Strategy

#### Cluster A: Licensing (RISK-001, 002, 003, 004)

**Systemic Issue:** Legal foundation for OSS release is incomplete.

**Root Cause:** Project evolved as internal tool without OSS considerations.

**Treatment Strategy:**
1. **Immediate:** Add LICENSE file (unblocks everything else)
2. **Short-term:** Add file headers via automated script
3. **Medium-term:** Implement DCO check, create NOTICE file

**One-Way Door Decisions:**
- License choice (MIT decided via DEC-001) - cannot easily change later
- CLA vs DCO affects future ability to relicense

#### Cluster B: Security (RISK-005, 006, 007, 008, 020)

**Systemic Issue:** Security posture not formalized for public exposure.

**Root Cause:** Internal development didn't require public security process.

**Treatment Strategy:**
1. **Before Release:** Git history scan (RISK-005 is show-stopper)
2. **At Release:** SECURITY.md + Dependabot
3. **Post-Release:** OpenSSF scorecard, EU CRA monitoring

**One-Way Door Decisions:**
- Git history cannot be "un-exposed" once public
- Security reputation affects long-term adoption

#### Cluster C: Contributor UX (RISK-009, 010, 011, 015, 017)

**Systemic Issue:** Repository optimized for power users, not new contributors.

**Root Cause:** Built for internal use where context was assumed.

**Treatment Strategy:**
1. **Pre-Release:** Clean up projects/, create CLAUDE-MINIMAL.md
2. **At Release:** Issue/PR templates, CODE_OF_CONDUCT
3. **Post-Release:** Monitor contributor feedback, iterate

**One-Way Door Decisions:**
- First impression is lasting; poor initial experience is hard to recover
- But can iterate on documentation post-release

#### Cluster D: Sustainability (RISK-018, 019)

**Systemic Issue:** Long-term maintenance model not defined.

**Root Cause:** Single maintainer, complex architecture.

**Treatment Strategy:**
1. **Pre-Release:** Document sync process, governance model
2. **Post-Release:** Actively recruit co-maintainers
3. **Ongoing:** Automation to reduce manual burden

**One-Way Door Decisions:**
- Governance model sets community expectations
- Hard to add restrictive policies after community forms

### 3. Risk Treatment Prioritization Matrix

```
TREATMENT PRIORITY MATRIX
=========================

                           EFFORT TO MITIGATE
                    LOW              MEDIUM            HIGH
                 (< 1 day)         (1-3 days)        (> 3 days)
              ┌─────────────────┬─────────────────┬─────────────────┐
              │                 │                 │                 │
    HIGH      │  RISK-001 ★★★   │  RISK-005 ★★★   │  RISK-002 ★★    │
    (Score    │  LICENSE        │  Git Secrets    │  File Headers   │
    15-25)    │  (30 min)       │  (2-4 hours)    │  (Script + run) │
    CRITICAL  │                 │                 │                 │
              ├─────────────────┼─────────────────┼─────────────────┤
              │                 │                 │                 │
    MEDIUM    │  RISK-006 ★★    │  RISK-007 ★★    │  RISK-009 ★★    │
    (Score    │  SECURITY.md    │  Dependabot     │  Projects clean │
    10-14)    │  (1-2 hours)    │  (1-2 hours)    │  (Review needed)│
    HIGH      │                 │                 │                 │
              │  RISK-017 ★     │  RISK-010 ★★    │  RISK-018 ★     │
              │  Templates      │  CLAUDE.md      │  Sync Process   │
              │  (2-3 hours)    │  (4-6 hours)    │  (Documentation)│
              ├─────────────────┼─────────────────┼─────────────────┤
              │                 │                 │                 │
    LOW       │  RISK-003       │  RISK-014       │  RISK-019       │
    (Score    │  NOTICE         │  PyPI Check     │  Governance     │
    5-9)      │  (30 min)       │  (15 min check) │  (Ongoing)      │
    MEDIUM    │                 │                 │                 │
              │  RISK-012       │  RISK-015       │                 │
              │  Documentation  │  Quick Start    │                 │
              │                 │  (2-3 hours)    │                 │
              └─────────────────┴─────────────────┴─────────────────┘

★★★ = Do immediately (blocks release)
★★  = Do before release (significant risk reduction)
★   = Do when practical (improves quality)
```

### 4. Recommended Treatment Sequence

**Phase 1: Unblock Release (Day 1)**
1. Create MIT LICENSE file (30 min) - RISK-001
2. Run Gitleaks scan on full history (2 hours) - RISK-005
3. Check PyPI name availability (15 min) - RISK-014

**Phase 2: Security Hardening (Day 2)**
4. Create SECURITY.md (1-2 hours) - RISK-006
5. Add dependabot.yml (30 min) - RISK-007
6. Add GitHub issue/PR templates (2 hours) - RISK-017

**Phase 3: Contributor Experience (Days 3-4)**
7. Clean up projects/ directory (4-6 hours) - RISK-009
8. Create CLAUDE-MINIMAL.md (4 hours) - RISK-010
9. Add license headers script + run (3 hours) - RISK-002
10. Add CODE_OF_CONDUCT.md (30 min) - RISK-015

**Phase 4: Polish (Day 5)**
11. Create CHANGELOG.md (1 hour) - RISK-016
12. Document DCO in CONTRIBUTING.md (1 hour) - RISK-004
13. Run initial OpenSSF scorecard (1 hour) - RISK-020
14. Remove/document skills/.graveyard (30 min) - RISK-011

**Ongoing:**
- Monitor EU CRA developments - RISK-008
- Plan governance expansion - RISK-019
- Establish sync process for dual repos - RISK-018

### 5. Key Trade-offs and Decisions

| Trade-off | Options | Recommendation | Rationale |
|-----------|---------|----------------|-----------|
| License headers: Manual vs Automated | Manual (slow, precise) vs Script (fast, may miss edge cases) | Automated script + manual review | Time efficiency, can fix edge cases later |
| Projects/ handling: Keep vs Clean vs Exclude | All exposed, curated set, or hidden entirely | Curated 1-2 exemplars | Balance between demonstration value and risk |
| CLAUDE.md: Single file vs Hierarchical | Monolithic vs decomposed | Hierarchical + minimal entry point | Addresses context window concerns |
| CLA vs DCO | Full CLA (legal strength) vs DCO (contributor friendliness) | DCO | Industry trending toward DCO; lower friction |
| OpenSSF target: 5 vs 7 vs 9 | Minimal, good, excellent | 7.0 | Balances effort vs enterprise requirements |

### 6. Risk Acceptance Rationale

**Risks Accepted Without Mitigation:**

| Risk | Score | Acceptance Rationale |
|------|-------|---------------------|
| RISK-003 (NOTICE file) | 4 | All deps are MIT; NOTICE is Apache 2.0 requirement |
| RISK-012 (tiktoken network) | 4 | Affects tiny minority of users; documented workaround available |

**Risks Deferred to Post-Release:**

| Risk | Score | Deferral Rationale |
|------|-------|-------------------|
| RISK-008 (EU CRA) | 16 | Deadline is Sept 2026; monitor and address closer to date |
| RISK-019 (Maintainer capacity) | 12 | Cannot predict adoption; plan but don't over-engineer |

---

## Cross-References to Tier 1 Artifacts

### ps-researcher (best-practices-research.md)

| Finding | Informs Risk(s) |
|---------|----------------|
| Missing LICENSE is NOT open source | RISK-001 |
| Gitleaks/TruffleHog mandatory pre-release | RISK-005 |
| SECURITY.md template provided | RISK-006 |
| OpenSSF Scorecard checklist | RISK-007, RISK-020 |
| EU CRA Sept 2026 deadline | RISK-008 |
| GitHub template examples | RISK-017 |
| DCO as CLA alternative trending | RISK-004 |

### ps-analyst (current-architecture-analysis.md)

| Finding | Informs Risk(s) |
|---------|----------------|
| CLAUDE.md is 1000+ lines | RISK-010 |
| projects/ contains internal artifacts | RISK-009 |
| skills/.graveyard exists | RISK-011 |
| tiktoken downloads on first use | RISK-012 |
| Package name "jerry" in pyproject.toml | RISK-014 |
| 183 Python files without headers | RISK-002 |
| OSS readiness score 68% | Multiple |

### nse-explorer (divergent-alternatives.md)

| Finding | Informs Risk(s) |
|---------|----------------|
| Dual repository complexity | RISK-018 |
| MIT vs Apache 2.0 trade-offs | RISK-001 context |
| CLAUDE.md strategy alternatives | RISK-010 |
| Contribution model options (CLA/DCO) | RISK-004 |
| Community platform options | RISK-019 context |
| Branding/naming considerations | RISK-014 |

### nse-requirements (current-state-inventory.md)

| Finding | Informs Risk(s) |
|---------|----------------|
| DOC-GAP-001: LICENSE missing | RISK-001 |
| LIC-GAP-002: 0/183 files with headers | RISK-002 |
| SEC-GAP-001: SECURITY.md missing | RISK-006 |
| SEC-GAP-002: No dependabot | RISK-007 |
| DEP-GAP-001: Empty requirements.txt | RISK-013 |
| CFG-GAP-002/003: No templates | RISK-017 |
| Overall OSS readiness: 68% | Multiple |

---

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | RISK-REG-PHASE-0-001 |
| **Status** | COMPLETE |
| **Quality Score** | Pending QG-0 evaluation |
| **Risks Identified** | 20 |
| **Critical Risks** | 2 |
| **High Risks** | 8 |
| **Medium Risks** | 6 |
| **Low Risks** | 4 |
| **Tier 1 Artifacts Analyzed** | 4 |

---

*This document is the output of Phase 0 Tier 2 risk identification by nse-risk agent.*
*It should be cross-pollinated to quality-gates/qg-0 for Phase 0 quality review.*

*Document ID: RISK-REG-PHASE-0-001*
*Workflow ID: oss-release-20260131-001*
