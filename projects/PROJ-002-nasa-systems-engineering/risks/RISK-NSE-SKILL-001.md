# Risk Register: NASA SE Skill

> **Document ID:** RISK-NSE-SKILL-001
> **Version:** 1.0
> **Date:** 2026-01-09
> **Status:** ACTIVE
> **Risk Manager:** User (SME Proxy)

---

## Risk Summary Dashboard

| Level | Count | Change | Status |
|-------|-------|--------|--------|
| 🔴 RED (16-25) | 2 | — | Mitigations implemented |
| 🟡 YELLOW (8-15) | 3 | — | Monitoring |
| 🟢 GREEN (1-7) | 2 | — | Accepted |
| **Total Active** | **7** | | |

---

## 5x5 Risk Matrix (Current State)

|  | **Consequence** |||||
|---|:---:|:---:|:---:|:---:|:---:|
| **Likelihood** | 1 (Min) | 2 (Low) | 3 (Mod) | 4 (High) | 5 (Max) |
| 5 (Very High) | | | | | |
| 4 (High) | | | | **R-001** | **R-002** |
| 3 (Moderate) | | | R-004 | R-003 | |
| 2 (Low) | | R-007 | R-005 | | |
| 1 (Very Low) | R-006 | | | | |

---

## Active Risks

### R-001: AI Hallucination of NASA Standards

| Attribute | Value |
|-----------|-------|
| **ID** | R-001 |
| **Status** | 🔴 RED - Mitigated |
| **Category** | Technical |
| **Owner** | User (SME) |
| **Identified** | 2026-01-09 |
| **Last Updated** | 2026-01-09 |

**Risk Statement:**
> IF the AI generates inaccurate interpretations of NASA standards (NPR 7123.1D, NPR 8000.4C),
> THEN users may apply incorrect SE practices,
> resulting in non-compliant SE artifacts and potential mission risk.

**Context:**
LLMs can confidently generate plausible-sounding but incorrect information. NASA SE requires precise interpretation of standards.

| Factor | Score | Rationale |
|--------|-------|-----------|
| Likelihood | 4 (High) | LLMs are prone to hallucination |
| Consequence | 5 (Maximum) | Could lead to mission-critical errors |
| **Risk Score** | **20** | 4 × 5 = 20 (RED) |

**Mitigations Implemented:**

| # | Action | Status | Evidence |
|---|--------|--------|----------|
| 1 | P-043 mandatory disclaimer on all outputs | ✅ Complete | All agents include disclaimer |
| 2 | User designated as SME proxy for validation | ✅ Complete | Plan Section 10.1 RACI |
| 3 | Citations to authoritative sources | ✅ Complete | Standards summaries with URLs |
| 4 | Human-in-loop gate checkpoints | ✅ Complete | 6 phase gates with user approval |

**Residual Risk (post-mitigation):** Score 8 (L=2, C=4) - YELLOW
- Mitigations reduce likelihood through human review
- Consequence remains high if hallucination undetected

**Escalation:** User must validate all NASA standard interpretations.

---

### R-002: Over-Reliance on AI Guidance

| Attribute | Value |
|-----------|-------|
| **ID** | R-002 |
| **Status** | 🔴 RED - Mitigated |
| **Category** | Safety |
| **Owner** | User |
| **Identified** | 2026-01-09 |
| **Last Updated** | 2026-01-09 |

**Risk Statement:**
> IF users treat AI-generated SE guidance as authoritative without human review,
> THEN critical engineering decisions may be made without proper professional judgment,
> resulting in system failures or safety issues.

**Context:**
Users may become complacent with AI outputs, especially when they appear professional and well-formatted.

| Factor | Score | Rationale |
|--------|-------|-----------|
| Likelihood | 4 (High) | Natural human tendency |
| Consequence | 5 (Maximum) | Could lead to safety-critical failures |
| **Risk Score** | **20** | 4 × 5 = 20 (RED) |

**Mitigations Implemented:**

| # | Action | Status | Evidence |
|---|--------|--------|----------|
| 1 | P-043 explicit "advisory only" disclaimer | ✅ Complete | All agent outputs |
| 2 | "Not for mission-critical decisions" warning | ✅ Complete | Disclaimer text |
| 3 | SME validation requirement documented | ✅ Complete | Plan Section 10 |
| 4 | Constitutional principle P-043 | ✅ Complete | JERRY_CONSTITUTION.md |

**Residual Risk (post-mitigation):** Score 10 (L=2, C=5) - YELLOW
- Likelihood reduced through explicit warnings
- Consequence remains maximum (cannot be reduced)

**Escalation:** Skill outputs must never be used for mission-critical decisions without SME validation.

---

### R-003: Process Misrepresentation

| Attribute | Value |
|-----------|-------|
| **ID** | R-003 |
| **Status** | 🟡 YELLOW - Monitoring |
| **Category** | Technical |
| **Owner** | User (SME) |
| **Identified** | 2026-01-09 |
| **Last Updated** | 2026-01-09 |

**Risk Statement:**
> IF the skill incorrectly maps NPR 7123.1D processes to agent capabilities,
> THEN users may receive guidance for the wrong process,
> resulting in SE artifacts that don't meet intended purpose.

**Context:**
17 processes are complex and interrelated. Incorrect mapping could cause confusion.

| Factor | Score | Rationale |
|--------|-------|-----------|
| Likelihood | 3 (Moderate) | Mapping verified against NPR 7123.1D |
| Consequence | 4 (High) | Wrong process could cause significant rework |
| **Risk Score** | **12** | 3 × 4 = 12 (YELLOW) |

**Mitigations Implemented:**

| # | Action | Status | Evidence |
|---|--------|--------|----------|
| 1 | NASA-SE-MAPPING.md with explicit mappings | ✅ Complete | 540 lines |
| 2 | Each agent specifies covered processes | ✅ Complete | YAML frontmatter |
| 3 | NPR7123-PROCESSES.md process guide | ✅ Complete | 650 lines |

**Residual Risk:** Score 6 (L=2, C=3) - GREEN with monitoring

---

### R-004: Template Format Non-Compliance

| Attribute | Value |
|-----------|-------|
| **ID** | R-004 |
| **Status** | 🟡 YELLOW - Monitoring |
| **Category** | Technical |
| **Owner** | Claude Code |
| **Identified** | 2026-01-09 |
| **Last Updated** | 2026-01-09 |

**Risk Statement:**
> IF templates don't match NASA-HDBK-1009A work product formats,
> THEN generated artifacts may not meet organizational standards,
> resulting in rework or rejection at reviews.

**Context:**
NASA has specific format expectations for SE work products.

| Factor | Score | Rationale |
|--------|-------|-----------|
| Likelihood | 3 (Moderate) | Templates based on handbook, not exact copies |
| Consequence | 3 (Moderate) | Formatting issues are correctable |
| **Risk Score** | **9** | 3 × 3 = 9 (YELLOW) |

**Mitigations Implemented:**

| # | Action | Status | Evidence |
|---|--------|--------|----------|
| 1 | Templates based on NASA-HDBK-1009A | ✅ Complete | Standards summary |
| 2 | Exemplar artifacts provided | ✅ Complete | EXAMPLE-REQUIREMENTS.md, EXAMPLE-RISK-REGISTER.md |
| 3 | User can customize templates | ✅ Complete | Markdown is editable |

**Residual Risk:** Score 4 (L=2, C=2) - GREEN

---

### R-005: Agent Coordination Failures

| Attribute | Value |
|-----------|-------|
| **ID** | R-005 |
| **Status** | 🟡 YELLOW - Monitoring |
| **Category** | Technical |
| **Owner** | Claude Code |
| **Identified** | 2026-01-09 |
| **Last Updated** | 2026-01-09 |

**Risk Statement:**
> IF agents fail to properly hand off state during multi-agent workflows,
> THEN orchestrated workflows may produce inconsistent outputs,
> resulting in gaps in SE coverage.

**Context:**
8 agents must coordinate for complex workflows like CDR preparation.

| Factor | Score | Rationale |
|--------|-------|-----------|
| Likelihood | 2 (Low) | State schema defined, patterns documented |
| Consequence | 3 (Moderate) | Would require manual coordination |
| **Risk Score** | **6** | 2 × 3 = 6 (GREEN, borderline) |

**Mitigations Implemented:**

| # | Action | Status | Evidence |
|---|--------|--------|----------|
| 1 | ORCHESTRATION.md with patterns | ✅ Complete | 590 lines |
| 2 | State schema defined per agent | ✅ Complete | JSON schema in each agent |
| 3 | Integration chain tests | ✅ Complete | BHV-CHAIN-001 to 004 |

**Residual Risk:** Score 4 (L=2, C=2) - GREEN

---

### R-006: Knowledge Base Staleness

| Attribute | Value |
|-----------|-------|
| **ID** | R-006 |
| **Status** | 🟢 GREEN - Accepted |
| **Category** | Technical |
| **Owner** | User |
| **Identified** | 2026-01-09 |
| **Last Updated** | 2026-01-09 |

**Risk Statement:**
> IF NASA standards are updated (e.g., NPR 7123.1E released),
> THEN skill guidance may become outdated,
> resulting in non-compliant recommendations.

**Context:**
Standards evolve. NPR 7123.1D superseded 7123.1C. Future updates possible.

| Factor | Score | Rationale |
|--------|-------|-----------|
| Likelihood | 1 (Very Low) | Major updates infrequent (years) |
| Consequence | 3 (Moderate) | Would require knowledge base update |
| **Risk Score** | **3** | 1 × 3 = 3 (GREEN) |

**Mitigations:**

| # | Action | Status | Evidence |
|---|--------|--------|----------|
| 1 | Version numbers in citations | ✅ Complete | "NPR 7123.1D" explicit |
| 2 | User monitors NASA standards | Ongoing | Plan Section 12.3 |

**Residual Risk:** Accepted at GREEN level.

---

### R-007: Insufficient Test Coverage

| Attribute | Value |
|-----------|-------|
| **ID** | R-007 |
| **Status** | 🟢 GREEN - Accepted |
| **Category** | Quality |
| **Owner** | Claude Code |
| **Identified** | 2026-01-09 |
| **Last Updated** | 2026-01-09 |

**Risk Statement:**
> IF behavioral tests don't cover all edge cases,
> THEN agents may behave unexpectedly in untested scenarios,
> resulting in poor user experience.

**Context:**
30 tests cover happy paths, edge cases, and adversarial scenarios, but not exhaustively.

| Factor | Score | Rationale |
|--------|-------|-----------|
| Likelihood | 2 (Low) | 30 tests with good coverage |
| Consequence | 2 (Low) | Edge cases are handleable |
| **Risk Score** | **4** | 2 × 2 = 4 (GREEN) |

**Mitigations:**

| # | Action | Status | Evidence |
|---|--------|--------|----------|
| 1 | 30 BDD tests covering all agents | ✅ Complete | BEHAVIOR_TESTS.md |
| 2 | Happy/Edge/Adversarial coverage | ✅ Complete | Test categories |
| 3 | Dog-fooding validation | ✅ In Progress | This document |

**Residual Risk:** Accepted at GREEN level.

---

## Risk Trends

| Metric | Current | Target |
|--------|---------|--------|
| Total Risks | 7 | - |
| RED Risks | 2 (mitigated) | 0 unmitigated |
| Total Exposure | 74 | <50 |
| Residual Exposure | 44 | <40 |

**Trend:** Mitigations have reduced exposure from 74 to 44 (residual).

---

## Risk Matrix Legend

| Score | Level | Action |
|-------|-------|--------|
| 16-25 | 🔴 RED | Immediate mitigation required |
| 8-15 | 🟡 YELLOW | Active mitigation/monitoring |
| 1-7 | 🟢 GREEN | Accept and monitor |

---

*DISCLAIMER: This risk register is AI-generated based on NASA Systems Engineering standards (NPR 8000.4C). It is advisory only and does not constitute official NASA guidance. All risk decisions require human review and professional engineering judgment.*
