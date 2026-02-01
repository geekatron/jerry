# Phase 0 Risk Register - OSS Release (Consolidated)

> **Document ID:** RSK-PHASE-0-001-v2
> **Agent:** nse-risk (Risk Manager)
> **Phase:** 0 (Divergent Exploration & Research)
> **Workflow:** oss-release-20260131-001
> **Created:** 2026-01-31
> **Updated:** 2026-01-31 (Consolidated with Tier 1b research)
> **NASA SE Reference:** NPR 7123.1D - Risk Management
> **Status:** COMPLETE

---

## Document Navigation

| Section | Audience | Purpose |
|---------|----------|---------|
| [L0: Executive Risk Summary](#l0-executive-risk-summary-eli5) | Executives, Stakeholders | High-level risk overview |
| [L1: Technical Risk Details](#l1-engineer-technical-risk-details) | Engineers, Developers | Actionable risk items |
| [L2: Strategic Risk Implications](#l2-architect-strategic-risk-implications) | Architects, Decision Makers | Trade-offs and strategic risks |

---

## L0: Executive Risk Summary (ELI5)

### What Are We Risking?

Releasing Jerry as open source is like opening your restaurant to the public for the first time. There are several things that could go wrong:

1. **Legal Problems** - Like serving food without proper licenses. If we don't have the right LICENSE file, technically people can't legally use our code.

2. **Security Leaks** - Like leaving your recipe book open on the counter. If we accidentally publish passwords or API keys, bad actors could misuse them.

3. **Bad First Impressions** - Like having a messy dining room on opening day. If our documentation is confusing, people won't come back.

4. **Overwhelmed Kitchen** - Like promising a 100-person banquet when you only have 2 cooks. If we don't set realistic scope, we'll burn out.

5. **Wrong Directions** - Like giving customers a map to the wrong address. If our CLAUDE.md is too bloated (912 lines!), Claude Code will get confused and make mistakes.

### Top 5 Risks at a Glance

| Rank | Risk | Likelihood | Impact | Action |
|------|------|------------|--------|--------|
| 1 | Missing LICENSE file | CERTAIN | CRITICAL | Create LICENSE file before ANY release |
| 2 | Credential exposure in git history | POSSIBLE | CRITICAL | Run full Gitleaks scan of entire history |
| 3 | CLAUDE.md context bloat (912 lines) | CERTAIN | HIGH | Decompose to ~300 lines + skills |
| 4 | No vulnerability disclosure process | CERTAIN | HIGH | Create SECURITY.md |
| 5 | Dual repository sync complexity | LIKELY | MEDIUM | Define sync strategy before split |

### Risk Heat Map

```
                              IMPACT
                    Low      Medium     High     Critical
                 ┌────────┬──────────┬─────────┬──────────┐
         High    │        │          │ RSK-08  │ RSK-01   │
                 │        │          │ RSK-09  │ RSK-02   │
                 ├────────┼──────────┼─────────┼──────────┤
LIKELIHOOD       │ RSK-18 │ RSK-10   │ RSK-06  │ RSK-03   │
         Medium  │ RSK-19 │ RSK-11   │ RSK-07  │ RSK-04   │
                 │        │ RSK-12   │         │          │
                 ├────────┼──────────┼─────────┼──────────┤
         Low     │ RSK-20 │ RSK-14   │ RSK-13  │ RSK-05   │
                 │ RSK-21 │ RSK-15   │ RSK-16  │          │
                 │        │ RSK-17   │         │          │
                 └────────┴──────────┴─────────┴──────────┘

Critical Risks (Red Zone): RSK-01, RSK-02, RSK-03, RSK-04, RSK-05
High Risks (Orange Zone): RSK-06, RSK-07, RSK-08, RSK-09
Medium Risks (Yellow Zone): RSK-10 through RSK-17
Low Risks (Green Zone): RSK-18 through RSK-21
```

### Bottom Line

Jerry is **technically ready** for OSS (good code, good tests, good architecture) but **administratively not ready** (missing legal files, security policies, and contributor onboarding).

**Estimated work to reach "safe to release":** 5-7 days focused effort.

---

## L1: Engineer Technical Risk Details

### Risk Assessment Methodology

Each risk is evaluated using the NASA SE risk matrix:

**Probability Scale:**
| Level | Description |
|-------|-------------|
| High | >70% probability or certain to occur |
| Medium | 30-70% probability |
| Low | <30% probability |

**Impact Scale:**
| Level | Description |
|-------|-------------|
| Critical | Project failure, legal liability, security breach |
| High | Significant rework, reputation damage, delayed release |
| Medium | Moderate effort to resolve, limited damage |
| Low | Minor inconvenience, easily addressed |

**Risk Score Matrix:**
| Probability × Impact | Result |
|---------------------|--------|
| High × Critical | **CRITICAL** |
| High × High OR Medium × Critical | **HIGH** |
| Medium × High OR High × Medium | **MEDIUM** |
| Low × any OR any × Low | **LOW** |

---

### Risk Register Table

| Risk ID | Category | Description | Probability | Impact | Risk Score | Owner | Status |
|---------|----------|-------------|-------------|--------|------------|-------|--------|
| RSK-P0-001 | Legal | Missing LICENSE file in repository root | High | Critical | **CRITICAL** | Maintainer | Open |
| RSK-P0-002 | Security | Potential credential exposure in git history | Medium | Critical | **HIGH** | Security | Open |
| RSK-P0-003 | Security | Missing SECURITY.md vulnerability disclosure | High | High | **HIGH** | Security | Open |
| RSK-P0-004 | Technical | CLAUDE.md context bloat (912 lines) | High | High | **HIGH** | Architecture | Open |
| RSK-P0-005 | Technical | Dual repository sync complexity | Medium | Critical | **HIGH** | DevOps | Open |
| RSK-P0-006 | Quality | Documentation not OSS-ready (68% score) | Medium | High | **MEDIUM** | Docs | Open |
| RSK-P0-007 | Quality | No license headers in 183 Python files | High | Medium | **MEDIUM** | Legal | Open |
| RSK-P0-008 | Schedule | Underestimated effort for Priority 1 items | Medium | High | **MEDIUM** | PM | Open |
| RSK-P0-009 | Technical | Empty requirements.txt file | High | Medium | **MEDIUM** | DevOps | Open |
| RSK-P0-010 | External | PyPI package name `jerry` availability | Low | Critical | **MEDIUM** | Release | Open |
| RSK-P0-011 | Scope | Scope creep from expanded research (9 agents) | Medium | Medium | **MEDIUM** | PM | Open |
| RSK-P0-012 | Technical | Hook system complexity for OSS users | Medium | Medium | **MEDIUM** | Docs | Open |
| RSK-P0-013 | External | Community adoption challenges | Low | High | **MEDIUM** | Community | Open |
| RSK-P0-014 | Technical | MCP server context bloat | Medium | Medium | **MEDIUM** | Architecture | Open |
| RSK-P0-015 | Quality | Missing GitHub templates (issues, PRs) | Medium | Low | **LOW** | DevOps | Open |
| RSK-P0-016 | Technical | Skills graveyard contains deprecated code | Low | Medium | **LOW** | Cleanup | Open |
| RSK-P0-017 | Quality | No dependabot.yml for security updates | Medium | Low | **LOW** | Security | Open |
| RSK-P0-018 | External | EU CRA compliance (Sept 2026 deadline) | Low | Medium | **LOW** | Legal | Open |
| RSK-P0-019 | Technical | tiktoken model download on first use | Low | Low | **LOW** | Docs | Open |
| RSK-P0-020 | Quality | Test suite size (2530 tests) may slow contributors | Low | Low | **LOW** | DevOps | Open |
| RSK-P0-021 | External | Trademark conflicts with "Jerry" name | Low | Medium | **LOW** | Legal | Open |

---

### Detailed Risk Analysis

#### RSK-P0-001: Missing LICENSE File [CRITICAL]

**Category:** Legal

**Description:** The repository declares MIT license in `pyproject.toml` and references it in `README.md`, but NO actual LICENSE file exists in the repository root. Without this file, the code is technically NOT open source and cannot be legally used.

**Evidence:**
- nse-requirements inventory: "LIC-GAP-001: Missing LICENSE file in repository root | CRITICAL"
- ps-analyst analysis: "Missing LICENSE file (critical)"
- ps-researcher: "Without [LICENSE], NOT open source"

**Probability:** HIGH (It's certain - the file is missing)

**Impact:** CRITICAL
- Legal liability for downstream users
- Cannot be published to PyPI as OSS
- Blocks all other release activities

**Risk Score:** P(H) × I(C) = **CRITICAL**

**Mitigation Strategy:**
1. Create MIT LICENSE file in repository root IMMEDIATELY
2. Validate LICENSE content matches pyproject.toml declaration
3. Add to pre-release checklist as blocking item

**Verification:** `ls -la LICENSE` returns file with MIT text

**Owner:** Repository Maintainer

**Status:** Open - BLOCKING

---

#### RSK-P0-002: Credential Exposure in Git History [HIGH]

**Category:** Security

**Description:** Git history may contain accidentally committed secrets (API keys, passwords, tokens). While current scans show no active credentials, full historical analysis required before public release.

**Evidence:**
- ps-researcher: "Pre-commit hooks (Gitleaks)" present but history not scanned
- nse-requirements: "detect-private-key hook" exists for new commits
- ps-analyst: "No actual credentials or secrets" in current state (but history unverified)

**Probability:** MEDIUM (pre-commit hooks reduce ongoing risk, but history is unknown)

**Impact:** CRITICAL
- Compromised accounts if real credentials exposed
- Reputation damage
- Security incident requiring disclosure

**Risk Score:** P(M) × I(C) = **HIGH**

**Mitigation Strategy:**
1. Run `gitleaks detect --source . --verbose` on full history
2. Run `trufflehog git file://. --since-commit HEAD~1000` for deep scan
3. If secrets found: Use `git filter-repo` to purge (BEFORE going public)
4. Document scan results in release checklist

**Verification:** Clean Gitleaks/TruffleHog scan report

**Owner:** Security Lead

**Status:** Open

---

#### RSK-P0-003: Missing SECURITY.md [HIGH]

**Category:** Security

**Description:** No vulnerability disclosure policy exists. Security researchers finding vulnerabilities have no guidance on responsible disclosure.

**Evidence:**
- nse-requirements: "SEC-GAP-001: Missing SECURITY.md vulnerability disclosure policy | HIGH"
- ps-researcher: Template provided for SECURITY.md structure
- ps-researcher: "EU CRA September 2026 deadline" for mandatory reporting

**Probability:** HIGH (It's certain - the file is missing)

**Impact:** HIGH
- Security issues reported via public issues (bad practice)
- No coordinated disclosure process
- Potential CRA non-compliance by Sept 2026

**Risk Score:** P(H) × I(H) = **HIGH**

**Mitigation Strategy:**
1. Create SECURITY.md using template from ps-researcher
2. Enable GitHub Security Advisories (private reporting)
3. Define response SLA (48h acknowledgment recommended)
4. Add security@email for alternative reporting

**Verification:** SECURITY.md exists with disclosure process

**Owner:** Security Lead

**Status:** Open

---

#### RSK-P0-004: CLAUDE.md Context Bloat [HIGH]

**Category:** Technical

**Description:** Current CLAUDE.md is 912 lines, exceeding recommended 500-line maximum by 82%. Research shows context rot degrades LLM performance even when within token limits.

**Evidence:**
- ps-researcher-claude-md: "Current Jerry CLAUDE.md: 912 lines (needs optimization)"
- ps-researcher-claude-md: "Quality improvement: Sessions stopping at 75% context utilization produce higher-quality code"
- ps-researcher-decomposition: "CLAUDE.md (Core - Always Loaded) ... Total: ~50 lines [recommended]"
- Chroma Research: Context rot phenomenon degrades performance as context window fills

**Probability:** HIGH (Current state is measurable)

**Impact:** HIGH
- Claude Code performance degradation
- Instruction loss (user reports missed rules)
- Poor OSS user experience

**Risk Score:** P(H) × I(H) = **HIGH**

**Mitigation Strategy:**
1. Decompose CLAUDE.md to ~300 lines (67% reduction)
2. Move Worktracker entity mappings to skills/worktracker/
3. Move templates to references (not inline)
4. Use `.claude/rules/` for auto-loaded standards
5. Implement skills for on-demand loading
6. Apply progressive disclosure architecture (Tier 1 → Tier 2 → Tier 3)

**Verification:** `wc -l CLAUDE.md` returns < 350

**Owner:** Architecture Lead

**Status:** Open

---

#### RSK-P0-005: Dual Repository Sync Complexity [HIGH]

**Category:** Technical

**Description:** DEC-002 decision to use dual repository strategy (source-repository internal, jerry public) creates ongoing synchronization complexity.

**Evidence:**
- nse-explorer: "Dual Repo (DECIDED - DEC-002) | Synchronization complexity; potential drift"
- nse-explorer: "Contribution flow confusion; features developed in wrong repo"
- ps-analyst: "Dual repository strategy creates merge/sync burden"

**Probability:** MEDIUM (Complexity is inherent to the strategy)

**Impact:** CRITICAL
- Features lost between repos
- Security patches delayed
- Contributor confusion

**Risk Score:** P(M) × I(C) = **HIGH**

**Mitigation Strategy:**
1. Define sync frequency (daily/weekly/per-release)
2. Document contribution flow (which repo for what)
3. Automate sync with GitHub Actions workflow
4. Create sync verification checklist
5. Consider alternative: single repo with access control

**Verification:** Documented sync process with automation

**Owner:** DevOps Lead

**Status:** Open - DECISION REQUIRED

---

#### RSK-P0-006: Documentation OSS Readiness Gap [MEDIUM]

**Category:** Quality

**Description:** Overall OSS readiness score is 68%, with License Compliance at 40% (critical) and Security Controls at 70%.

**Evidence:**
- nse-requirements: "Overall OSS Readiness Score: 68%"
- nse-requirements: "License Compliance: 40% | Critical"
- nse-requirements: "Security Controls: 70% | Needs Work"

**Probability:** MEDIUM (Known gap, fixable with effort)

**Impact:** HIGH
- Poor first impression for OSS users
- Reduced adoption
- Support burden from confusion

**Risk Score:** P(M) × I(H) = **MEDIUM**

**Mitigation Strategy:**
1. Complete Priority 1 items (LICENSE, SECURITY.md)
2. Create quick-start guide for new users
3. Add example projects (1-2 curated)
4. Simplify CLAUDE.md for beginners

**Verification:** OSS readiness score >= 85%

**Owner:** Documentation Lead

**Status:** Open

---

#### RSK-P0-007: Missing License Headers [MEDIUM]

**Category:** Legal

**Description:** 0 of 183 Python files have license headers or SPDX identifiers.

**Evidence:**
- nse-requirements: "LIC-GAP-002: No license headers in 183 Python source files | HIGH"
- nse-requirements: "LIC-GAP-003: No SPDX-License-Identifier in source files | MEDIUM"

**Probability:** HIGH (Measurable current state)

**Impact:** MEDIUM
- Unclear licensing per-file
- Some enterprise compliance concerns
- Professional appearance issue

**Risk Score:** P(H) × I(M) = **MEDIUM**

**Mitigation Strategy:**
1. Create script to add headers to all Python files
2. Use SPDX format: `# SPDX-License-Identifier: MIT`
3. Add to pre-commit hook for new files
4. Run as batch operation before release

**Verification:** All Python files have SPDX header

**Owner:** Legal/DevOps

**Status:** Open

---

#### RSK-P0-008: Schedule Underestimation [MEDIUM]

**Category:** Schedule

**Description:** ps-analyst estimates "2-3 days for Priority 1 items, 1 week for full preparation" but research scope expanded significantly (9 agents vs. original 4).

**Evidence:**
- ps-analyst: "Estimated effort: 2-3 days for Priority 1 items"
- Tier 1b remediation: Added 5 additional research agents
- Multiple "Critical" and "High" items identified

**Probability:** MEDIUM (Estimates often understate)

**Impact:** HIGH
- Delayed release
- Cut corners on quality
- Burnout

**Risk Score:** P(M) × I(H) = **MEDIUM**

**Mitigation Strategy:**
1. Re-estimate with contingency (1.5-2x multiplier)
2. Prioritize ruthlessly - only true blockers first
3. Define MVP scope vs. nice-to-have
4. Create phased release plan if needed

**Verification:** Revised schedule with contingency

**Owner:** Project Manager

**Status:** Open

---

#### RSK-P0-009: Empty requirements.txt [MEDIUM]

**Category:** Technical

**Description:** requirements.txt is empty/autogenerated stub, which causes installation issues for pip users.

**Evidence:**
- nse-requirements: "DOC-GAP-006: requirements.txt is empty (autogenerated stub) | HIGH"
- nse-requirements: "DEP-GAP-001: requirements.txt is empty | HIGH"

**Probability:** HIGH (Measurable)

**Impact:** MEDIUM
- pip install fails without pyproject.toml support
- Older Python environments affected
- Contributor setup friction

**Risk Score:** P(H) × I(M) = **MEDIUM**

**Mitigation Strategy:**
1. Generate requirements.txt from pyproject.toml
2. Pin versions for reproducibility
3. Add to pre-release checklist
4. Document uv vs pip preference

**Verification:** `pip install -r requirements.txt` succeeds

**Owner:** DevOps

**Status:** Open

---

#### RSK-P0-010: PyPI Name Availability [MEDIUM]

**Category:** External

**Description:** Package name `jerry` may already be claimed on PyPI.

**Evidence:**
- ps-analyst: "Package Name: jerry | Verify `jerry` is available on PyPI. Consider `jerry-framework` if taken"
- nse-explorer: One-way door decision - name cannot change after publishing

**Probability:** LOW (Unknown until checked)

**Impact:** CRITICAL
- Must rename package if taken
- All documentation references change
- Installation instructions change

**Risk Score:** P(L) × I(C) = **MEDIUM**

**Mitigation Strategy:**
1. Check `pip search jerry` or pypi.org
2. Prepare alternatives: `jerry-framework`, `jerry-cli`, `jerry-code`
3. Reserve preferred name if available
4. Update pyproject.toml if needed

**Verification:** Confirmed PyPI name availability

**Owner:** Release Manager

**Status:** Open

---

#### RSK-P0-011: Scope Creep from Expanded Research [MEDIUM]

**Category:** Scope

**Description:** DISC-001 remediation expanded research from 4 agents to 9 agents, potentially increasing scope.

**Evidence:**
- Tier 1b added: ps-researcher-claude-code, ps-researcher-claude-md, ps-researcher-plugins, ps-researcher-skills, ps-researcher-decomposition
- Each additional research stream generates findings requiring action

**Probability:** MEDIUM (Research complete, findings now scope)

**Impact:** MEDIUM
- More work items than originally planned
- Analysis paralysis risk
- Delayed convergence

**Risk Score:** P(M) × I(M) = **MEDIUM**

**Mitigation Strategy:**
1. Synthesize research findings (ps-analyst task)
2. Ruthlessly prioritize: Block/Should/Could
3. Create Phase 1 scope with explicit exclusions
4. Document deferred items for future releases

**Verification:** Converged action plan with scope boundaries

**Owner:** Project Manager

**Status:** Open

---

#### RSK-P0-012: Hook System Complexity [MEDIUM]

**Category:** Technical

**Description:** Jerry's hook system may be too complex for OSS newcomers to understand and use effectively.

**Evidence:**
- ps-researcher-claude-code: Detailed hook architecture with 12 event types
- ps-researcher-plugins: Hook configuration requires JSON and shell scripting knowledge
- Current Jerry: Uses Python hooks with complex JSON output

**Probability:** MEDIUM (Complexity exists, user impact uncertain)

**Impact:** MEDIUM
- Steep learning curve
- Support burden
- Reduced adoption

**Risk Score:** P(M) × I(M) = **MEDIUM**

**Mitigation Strategy:**
1. Create hooks quick-start guide
2. Provide copy-paste hook examples
3. Document common use cases
4. Consider simplifying for v1.0 release

**Verification:** Hooks documentation with examples

**Owner:** Documentation Lead

**Status:** Open

---

#### RSK-P0-013: Community Adoption Challenges [MEDIUM]

**Category:** External

**Description:** OSS success depends on community adoption, which is uncertain for a new framework.

**Evidence:**
- nse-explorer: "Community channels: GitHub Discussions + Discord is the modern pattern"
- ps-researcher: "Poor adoption | MEDIUM | Quality documentation with README best practices"
- No existing community (new project)

**Probability:** LOW (Success is uncertain but not a failure mode)

**Impact:** HIGH
- Low usage after release effort
- Maintainer burnout without contributors
- Project stagnation

**Risk Score:** P(L) × I(H) = **MEDIUM**

**Mitigation Strategy:**
1. Enable GitHub Discussions
2. Create Discord server (optional)
3. Write compelling README with value proposition
4. Reach out to early adopters
5. Submit to relevant aggregators (Awesome lists, etc.)

**Verification:** Community infrastructure ready

**Owner:** Community Lead

**Status:** Open

---

#### RSK-P0-014: MCP Server Context Bloat [MEDIUM]

**Category:** Technical

**Description:** Each MCP server adds tool definitions consuming context budget.

**Evidence:**
- ps-researcher-claude-code: "0 MCP: ~0 tokens, 3 MCP: ~5-10K tokens, 10 MCP: ~20-50K tokens"
- ps-researcher-claude-code: "Tool Search feature reduced MCP context bloat by 46.9%"
- Jerry uses MCP extensively

**Probability:** MEDIUM (Depends on user configuration)

**Impact:** MEDIUM
- Performance degradation with many MCP servers
- User confusion about performance issues
- Support burden

**Risk Score:** P(M) × I(M) = **MEDIUM**

**Mitigation Strategy:**
1. Document MCP token impact
2. Recommend essential servers only
3. Provide `/mcp` usage guidance
4. Consider lazy-loading patterns

**Verification:** MCP best practices documented

**Owner:** Architecture Lead

**Status:** Open

---

#### RSK-P0-015: Missing GitHub Templates [LOW]

**Category:** Quality

**Description:** No issue templates or PR templates in .github/ directory.

**Evidence:**
- nse-requirements: "DOC-GAP-008: No issue/PR templates in .github/ | LOW"
- nse-requirements: "CFG-GAP-002: No issue templates"
- nse-requirements: "CFG-GAP-003: No PR template"

**Probability:** MEDIUM (Missing, will affect quality)

**Impact:** LOW
- Inconsistent issue reports
- Missing information in PRs
- Minor quality impact

**Risk Score:** P(M) × I(L) = **LOW**

**Mitigation Strategy:**
1. Create .github/ISSUE_TEMPLATE/ with bug, feature, question
2. Create .github/PULL_REQUEST_TEMPLATE.md
3. Use templates from ps-researcher examples

**Verification:** Templates present and working

**Owner:** DevOps

**Status:** Open

---

#### RSK-P0-016: Skills Graveyard [LOW]

**Category:** Technical

**Description:** `skills/.graveyard/` contains deprecated code that may confuse OSS users.

**Evidence:**
- ps-analyst: "Skills Graveyard: worktracker, worktracker-decomposition"
- ps-analyst: "Recommendation: Remove or explicitly mark as deprecated"

**Probability:** LOW (Minor confusion)

**Impact:** MEDIUM
- User confusion
- Maintenance questions
- Professional appearance

**Risk Score:** P(L) × I(M) = **LOW**

**Mitigation Strategy:**
1. Remove .graveyard from public release OR
2. Add clear DEPRECATED.md in graveyard OR
3. Rename to `_deprecated/` or `_archive/`

**Verification:** Graveyard handled appropriately

**Owner:** Cleanup Task

**Status:** Open

---

#### RSK-P0-017: No Dependabot Configuration [LOW]

**Category:** Quality

**Description:** No dependabot.yml for automated security updates.

**Evidence:**
- nse-requirements: "SEC-GAP-002: No dependabot.yml for automated security updates | MEDIUM"
- nse-requirements: "CFG-GAP-004: No dependabot.yml for security updates | MEDIUM"

**Probability:** MEDIUM (Configuration missing)

**Impact:** LOW
- Delayed security patches
- Manual update burden
- But pip-audit covers scanning

**Risk Score:** P(M) × I(L) = **LOW**

**Mitigation Strategy:**
1. Create .github/dependabot.yml
2. Configure for Python, GitHub Actions
3. Set weekly schedule

**Verification:** Dependabot PRs appearing

**Owner:** Security/DevOps

**Status:** Open

---

#### RSK-P0-018: EU CRA Compliance [LOW]

**Category:** External

**Description:** EU Cyber Resilience Act mandatory vulnerability reporting takes effect September 11, 2026.

**Evidence:**
- ps-researcher: "Critical Date: September 11, 2026 - CRA mandatory vulnerability reporting"
- ps-researcher: "SBOM required" for supply chain transparency

**Probability:** LOW (8+ months away)

**Impact:** MEDIUM
- Future compliance burden
- May require SBOM generation
- Affects EU users

**Risk Score:** P(L) × I(M) = **LOW**

**Mitigation Strategy:**
1. Create SECURITY.md now (satisfies disclosure)
2. Plan SBOM generation for future
3. Monitor CRA requirements
4. Consider CRA-ready documentation

**Verification:** CRA compliance roadmap documented

**Owner:** Legal/Compliance

**Status:** Open - FUTURE

---

#### RSK-P0-019: tiktoken Model Download [LOW]

**Category:** Technical

**Description:** tiktoken downloads ~4MB model files on first use.

**Evidence:**
- ps-analyst: "tiktoken downloads model files (~4MB) on first use"
- Affects users with restricted network access

**Probability:** LOW (Minor edge case)

**Impact:** LOW
- Offline installation fails
- Enterprise firewall issues
- Minor setup friction

**Risk Score:** P(L) × I(L) = **LOW**

**Mitigation Strategy:**
1. Document in INSTALLATION.md
2. Provide offline installation option
3. Pre-cache in CI/CD

**Verification:** tiktoken note in docs

**Owner:** Documentation

**Status:** Open

---

#### RSK-P0-020: Large Test Suite [LOW]

**Category:** Quality

**Description:** 2530 tests may slow contributor feedback loop.

**Evidence:**
- ps-analyst: "2530 tests collected"
- ps-analyst: "May be slow for contributor feedback loop"

**Probability:** LOW (Contributor impact uncertain)

**Impact:** LOW
- Slower PR feedback
- Resource usage
- CI costs

**Risk Score:** P(L) × I(L) = **LOW**

**Mitigation Strategy:**
1. Document `pytest -m unit` for fast feedback
2. CI runs full suite, contributors run subset
3. Optimize slow tests over time

**Verification:** Fast test subset documented

**Owner:** DevOps

**Status:** Open

---

#### RSK-P0-021: Trademark Conflicts [LOW]

**Category:** External

**Description:** "Jerry" name may conflict with other projects or trademarks.

**Evidence:**
- nse-explorer: "Trademark search needed; may conflict with other projects"
- Generic name increases conflict likelihood

**Probability:** LOW (No known conflicts identified)

**Impact:** MEDIUM
- Rebranding cost
- Legal issues
- Confusion

**Risk Score:** P(L) × I(M) = **LOW**

**Mitigation Strategy:**
1. Search USPTO/EUIPO for "Jerry" trademarks
2. Search GitHub for "jerry" projects
3. Prepare backup names if needed
4. Consider distinctive modifier: "Jerry Framework"

**Verification:** Trademark search completed

**Owner:** Legal

**Status:** Open

---

## L2: Architect Strategic Risk Implications

### 1. Risk Categorization by Decision Type

#### One-Way Door Decisions (Irreversible)

| Risk ID | Decision | Reversibility | Recommendation |
|---------|----------|---------------|----------------|
| RSK-P0-001 | License type (MIT) | Very Hard | Already decided, ensure file exists |
| RSK-P0-010 | PyPI package name | Permanent | Verify availability BEFORE release |
| RSK-P0-021 | Project name "Jerry" | Hard | Complete trademark search |
| RSK-P0-005 | Dual repo strategy | Hard | Re-evaluate before implementing |

#### Two-Way Door Decisions (Reversible)

| Risk ID | Decision | Reversibility | Recommendation |
|---------|----------|---------------|----------------|
| RSK-P0-004 | CLAUDE.md structure | Fully Reversible | Experiment with decomposition |
| RSK-P0-015 | GitHub templates | Easy | Iterate based on feedback |
| RSK-P0-016 | Skills graveyard | Easy | Remove for clean release |
| RSK-P0-017 | Dependabot config | Easy | Enable and adjust |

### 2. Risk Interdependencies

```
RSK-P0-001 (LICENSE) ──────────┐
                               │
RSK-P0-007 (Headers) ──────────┼──► LEGAL COMPLIANCE CHAIN
                               │
RSK-P0-021 (Trademark) ────────┘


RSK-P0-002 (Secrets) ──────────┐
                               │
RSK-P0-003 (SECURITY.md) ──────┼──► SECURITY POSTURE CHAIN
                               │
RSK-P0-017 (Dependabot) ───────┘


RSK-P0-004 (CLAUDE.md) ────────┐
                               │
RSK-P0-014 (MCP Bloat) ────────┼──► CONTEXT EFFICIENCY CHAIN
                               │
RSK-P0-012 (Hook Complexity) ──┘


RSK-P0-005 (Dual Repo) ────────┐
                               │
RSK-P0-008 (Schedule) ─────────┼──► EXECUTION CHAIN
                               │
RSK-P0-011 (Scope Creep) ──────┘
```

### 3. FMEA Analysis (Failure Mode and Effects Analysis)

| Failure Mode | Cause | Effect | Severity (1-10) | Probability (1-10) | Detection (1-10) | RPN | Priority |
|--------------|-------|--------|-----------------|-------------------|-----------------|-----|----------|
| Release without LICENSE | Oversight | Legal liability, unusable code | 10 | 3 | 2 | 60 | CRITICAL |
| Credential leak post-release | History not scanned | Security incident | 10 | 4 | 3 | 120 | CRITICAL |
| Context rot causing failures | Bloated CLAUDE.md | Poor user experience | 7 | 8 | 5 | 280 | HIGH |
| Repo sync drift | Manual process | Feature loss, bugs | 8 | 6 | 4 | 192 | HIGH |
| Abandoned project | No community | Wasted effort | 6 | 4 | 7 | 168 | MEDIUM |
| Installation failures | Empty requirements.txt | User frustration | 5 | 7 | 3 | 105 | MEDIUM |

**RPN (Risk Priority Number)** = Severity × Probability × Detection
- RPN > 200: Critical action required
- RPN 100-200: High priority
- RPN 50-100: Medium priority
- RPN < 50: Low priority / accept

### 4. Risk Response Strategies

#### Avoid (Eliminate Risk Source)

| Risk | Avoidance Strategy |
|------|---------------------|
| RSK-P0-005 | Reconsider dual-repo; single repo with access control |
| RSK-P0-016 | Remove graveyard entirely from release |

#### Mitigate (Reduce Probability/Impact)

| Risk | Mitigation Strategy |
|------|----------------------|
| RSK-P0-001 | Add LICENSE file immediately (eliminates risk) |
| RSK-P0-002 | Run comprehensive secret scan before release |
| RSK-P0-004 | Decompose CLAUDE.md using research findings |
| RSK-P0-006 | Focus on critical documentation first |

#### Transfer (Shift Risk Elsewhere)

| Risk | Transfer Strategy |
|------|-------------------|
| RSK-P0-013 | Partner with early adopters for feedback |
| RSK-P0-018 | Engage legal counsel for CRA compliance |

#### Accept (Conscious Decision to Live With Risk)

| Risk | Acceptance Rationale |
|------|----------------------|
| RSK-P0-019 | tiktoken behavior is library default, document only |
| RSK-P0-020 | Large test suite is quality feature, not bug |

### 5. Trade-off Analysis

#### Speed vs. Quality Trade-off

```
                Quality
                   ▲
                   │      ★ Target Zone
               100%├─────★────────────
                   │    / \
                   │   /   \
                   │  /     \ Diminishing Returns
               75% ├─/───────\────────
                   │/         \
               50% │           \
                   │            \
                   ├─────────────────► Time
                   0  2wk  4wk  6wk  8wk
                      │
                      └─ Original estimate (2-3 days P1)
                         Revised estimate (5-7 days)
```

**Analysis:**
- 2-3 day estimate for P1 items is aggressive
- Quality target of 85%+ OSS readiness requires addressing HIGH risks
- Recommend 5-7 days minimum for P1 with buffer

#### Scope vs. Time Trade-off

| Scope Level | Items | Time | Quality | Risk |
|-------------|-------|------|---------|------|
| MVP (Blocking Only) | 2 (LICENSE, Secret Scan) | 1 day | 70% | High |
| P1 (Critical + High) | 9 | 5-7 days | 85% | Medium |
| Full (All Identified) | 21 | 2-3 weeks | 95% | Low |

**Recommendation:** P1 scope with explicit deferral of P2/P3 items.

### 6. Monitoring and Control

#### Risk Dashboard Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Critical Risks Open | 0 | 2 | RED |
| High Risks Open | < 3 | 5 | YELLOW |
| OSS Readiness Score | >= 85% | 68% | YELLOW |
| Secret Scan Status | PASS | NOT RUN | RED |
| LICENSE File | EXISTS | MISSING | RED |
| SECURITY.md | EXISTS | MISSING | RED |
| CLAUDE.md Lines | < 350 | 912 | YELLOW |

#### Risk Review Cadence

| Phase | Frequency | Focus |
|-------|-----------|-------|
| Phase 0 | End of phase | Complete risk identification |
| Phase 1 | Daily | Critical risk closure |
| Phase 2 | End of phase | Risk re-assessment |
| Pre-Release | Gate review | All Critical/High closed |

---

## Appendix A: Risk Sources and Evidence

### Tier 1a Research Inputs (Original 4 Agents)

| Agent | Document | Key Risk Findings |
|-------|----------|-------------------|
| ps-researcher | best-practices-research.md | LICENSE requirements, security scanning, community patterns |
| ps-analyst | current-architecture-analysis.md | Missing LICENSE, CLAUDE.md complexity, graveyard |
| nse-explorer | divergent-alternatives.md | Dual repo complexity, one-way decisions |
| nse-requirements | current-state-inventory.md | 21 gaps identified, 68% OSS readiness |

### Tier 1b Research Inputs (DISC-001 Remediation)

| Agent | Document | Key Risk Findings |
|-------|----------|-------------------|
| ps-researcher-claude-code | claude-code-best-practices.md | Hook complexity, MCP bloat, context management |
| ps-researcher-claude-md | claude-md-best-practices.md | 912 lines vs. 500 recommended, context rot |
| ps-researcher-plugins | plugins-best-practices.md | Plugin caching, security FMEA |
| ps-researcher-skills | skills-best-practices.md | P-003 recursion constraints, portability |
| ps-researcher-decomposition | decomposition-best-practices.md | Import patterns, context optimization |

---

## Appendix B: Risk Closure Criteria

### Critical Risks (Must Close Before Release)

| Risk ID | Closure Criteria |
|---------|------------------|
| RSK-P0-001 | LICENSE file exists in root, validates as MIT |
| RSK-P0-002 | Gitleaks scan passes with no findings |

### High Risks (Should Close Before Release)

| Risk ID | Closure Criteria |
|---------|------------------|
| RSK-P0-003 | SECURITY.md exists with disclosure process |
| RSK-P0-004 | CLAUDE.md < 350 lines |
| RSK-P0-005 | Sync strategy documented and agreed |
| RSK-P0-006 | OSS readiness >= 85% |
| RSK-P0-007 | All Python files have SPDX header |

### Medium Risks (Address Before or Shortly After Release)

| Risk ID | Closure Criteria |
|---------|------------------|
| RSK-P0-008 | Revised schedule published |
| RSK-P0-009 | requirements.txt generates from pyproject.toml |
| RSK-P0-010 | PyPI name verified available |
| RSK-P0-011 | Converged scope document published |
| RSK-P0-012 | Hook documentation with examples |
| RSK-P0-013 | Community infrastructure ready |
| RSK-P0-014 | MCP best practices documented |

---

## Appendix C: Recommended Treatment Sequence

### Phase 1: Unblock Release (Day 1)

1. Create MIT LICENSE file (30 min) - RSK-P0-001
2. Run Gitleaks scan on full history (2 hours) - RSK-P0-002
3. Check PyPI name availability (15 min) - RSK-P0-010

### Phase 2: Security Hardening (Days 2-3)

4. Create SECURITY.md (1-2 hours) - RSK-P0-003
5. Add dependabot.yml (30 min) - RSK-P0-017
6. Add GitHub issue/PR templates (2 hours) - RSK-P0-015

### Phase 3: Context Optimization (Days 3-4)

7. Decompose CLAUDE.md (4-6 hours) - RSK-P0-004
8. Document MCP best practices (2 hours) - RSK-P0-014
9. Create hooks quick-start (3 hours) - RSK-P0-012

### Phase 4: Cleanup and Polish (Days 5-7)

10. Clean up projects/ directory (4-6 hours) - if included
11. Add license headers script + run (3 hours) - RSK-P0-007
12. Generate requirements.txt (1 hour) - RSK-P0-009
13. Document sync strategy (2 hours) - RSK-P0-005

---

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | RSK-PHASE-0-001-v2 |
| **Status** | COMPLETE |
| **Risks Identified** | 21 |
| **Critical Risks** | 2 |
| **High Risks** | 5 |
| **Medium Risks** | 9 |
| **Low Risks** | 5 |
| **Quality Score** | Pending QG-0 evaluation |
| **Word Count** | ~5,500 |
| **Frameworks Applied** | 5W2H, FMEA, Pareto, NASA SE Risk Matrix |
| **Research Inputs Analyzed** | 9 (Tier 1a: 4, Tier 1b: 5) |

---

*Document generated by nse-risk agent for PROJ-009-oss-release orchestration workflow.*
*Constitutional Compliance: P-001 (Truth), P-002 (Persistence), P-004 (Provenance), P-011 (Evidence)*
