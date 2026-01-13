# Configuration Item List: NASA SE Skill

> **Document ID:** CI-NSE-SKILL-001
> **Version:** 1.0
> **Date:** 2026-01-09
> **Baseline:** BL-001 (Deployment Baseline)
> **Author:** Claude Code

---

## L0: Executive Summary

**Total CIs:** 19
**Controlled:** 19 (100%)
**Pending:** 0
**Current Baseline:** BL-001 (2026-01-09)

The NASA SE Skill baseline includes 19 configuration items: 1 skill definition, 8 agent definitions, 4 documentation files, 3 knowledge base files, and 3 test/template files. All items are under configuration control for deployment.

---

## L1: Configuration Items

### CI Classification

| Type | Code | Description | Example |
|------|------|-------------|---------|
| SKILL | SKL | Skill definition | SKILL.md |
| AGENT | AGT | Agent definition | nse-requirements.md |
| DOC | DOC | Documentation | PLAYBOOK.md |
| KNOW | KNW | Knowledge base | NASA-STANDARDS-SUMMARY.md |
| TEST | TST | Test artifacts | BEHAVIOR_TESTS.md |
| TMPL | TPL | Templates | Review checklists |

### CI Registry

| CI ID | Name | Type | Description | Owner | Version | Baseline | Status |
|-------|------|------|-------------|-------|---------|----------|--------|
| CI-001 | SKILL.md | SKL | Main skill definition | Claude Code | 1.0 | BL-001 | ✅ Controlled |
| CI-002 | nse-requirements.md | AGT | Requirements Engineering Agent | Claude Code | 1.0 | BL-001 | ✅ Controlled |
| CI-003 | nse-verification.md | AGT | V&V Specialist Agent | Claude Code | 1.0 | BL-001 | ✅ Controlled |
| CI-004 | nse-risk.md | AGT | Risk Management Agent | Claude Code | 1.0 | BL-001 | ✅ Controlled |
| CI-005 | nse-architecture.md | AGT | Technical Architecture Agent | Claude Code | 1.0 | BL-001 | ✅ Controlled |
| CI-006 | nse-reviewer.md | AGT | Technical Review Gate Agent | Claude Code | 1.0 | BL-001 | ✅ Controlled |
| CI-007 | nse-integration.md | AGT | System Integration Agent | Claude Code | 1.0 | BL-001 | ✅ Controlled |
| CI-008 | nse-configuration.md | AGT | Configuration Management Agent | Claude Code | 1.0 | BL-001 | ✅ Controlled |
| CI-009 | nse-reporter.md | AGT | Status Reporter Agent | Claude Code | 1.0 | BL-001 | ✅ Controlled |
| CI-010 | PLAYBOOK.md | DOC | User guide and workflows | Claude Code | 1.0 | BL-001 | ✅ Controlled |
| CI-011 | NASA-SE-MAPPING.md | DOC | NASA process to agent mapping | Claude Code | 1.0 | BL-001 | ✅ Controlled |
| CI-012 | ORCHESTRATION.md | DOC | Agent coordination patterns | Claude Code | 1.0 | BL-001 | ✅ Controlled |
| CI-013 | NSE_AGENT_TEMPLATE.md | DOC | Agent template standard | Claude Code | 2.0 | BL-001 | ✅ Controlled |
| CI-014 | NASA-STANDARDS-SUMMARY.md | KNW | Standards reference | Claude Code | 1.0 | BL-001 | ✅ Controlled |
| CI-015 | NPR7123-PROCESSES.md | KNW | 17 processes guide | Claude Code | 1.0 | BL-001 | ✅ Controlled |
| CI-016 | EXAMPLE-REQUIREMENTS.md | KNW | Requirements exemplar | Claude Code | 1.0 | BL-001 | ✅ Controlled |
| CI-017 | EXAMPLE-RISK-REGISTER.md | KNW | Risk register exemplar | Claude Code | 1.0 | BL-001 | ✅ Controlled |
| CI-018 | BEHAVIOR_TESTS.md | TST | BDD behavioral tests | Claude Code | 2.0 | BL-001 | ✅ Controlled |
| CI-019 | review-checklists/ | TPL | Review entrance/exit checklists | Claude Code | 1.0 | BL-001 | ✅ Controlled |

### CI Status Summary

| Status | Count | % |
|--------|-------|---|
| Controlled | 19 | 100% |
| Pending | 0 | 0% |
| Obsolete | 0 | 0% |
| **Total** | **19** | **100%** |

### CI by Type

| Type | Count | % |
|------|-------|---|
| SKL (Skill) | 1 | 5% |
| AGT (Agent) | 8 | 42% |
| DOC (Documentation) | 4 | 21% |
| KNW (Knowledge) | 4 | 21% |
| TST (Test) | 1 | 5% |
| TPL (Template) | 1 | 5% |
| **Total** | **19** | **100%** |

---

## L2: CM Strategy

### Baseline Definition: BL-001 (Deployment Baseline)

| Attribute | Value |
|-----------|-------|
| Baseline ID | BL-001 |
| Baseline Name | Deployment Baseline |
| Baseline Type | Product Baseline |
| Date Established | 2026-01-09 |
| CI Count | 19 |
| Approver | User (pending SME validation) |

### Baseline Contents

| CI ID | Name | Version | Location | Lines |
|-------|------|---------|----------|-------|
| CI-001 | SKILL.md | 1.0 | skills/nasa-se/SKILL.md | ~200 |
| CI-002 | nse-requirements.md | 1.0 | skills/nasa-se/agents/ | 504 |
| CI-003 | nse-verification.md | 1.0 | skills/nasa-se/agents/ | 544 |
| CI-004 | nse-risk.md | 1.0 | skills/nasa-se/agents/ | 581 |
| CI-005 | nse-architecture.md | 1.0 | skills/nasa-se/agents/ | 832 |
| CI-006 | nse-reviewer.md | 1.0 | skills/nasa-se/agents/ | 627 |
| CI-007 | nse-integration.md | 1.0 | skills/nasa-se/agents/ | 650 |
| CI-008 | nse-configuration.md | 1.0 | skills/nasa-se/agents/ | 673 |
| CI-009 | nse-reporter.md | 1.0 | skills/nasa-se/agents/ | 740 |
| CI-010 | PLAYBOOK.md | 1.0 | skills/nasa-se/ | 359 |
| CI-011 | NASA-SE-MAPPING.md | 1.0 | skills/nasa-se/docs/ | 540 |
| CI-012 | ORCHESTRATION.md | 1.0 | skills/nasa-se/docs/ | 590 |
| CI-013 | NSE_AGENT_TEMPLATE.md | 2.0 | skills/nasa-se/agents/ | ~300 |
| CI-014 | NASA-STANDARDS-SUMMARY.md | 1.0 | skills/nasa-se/knowledge/standards/ | 265 |
| CI-015 | NPR7123-PROCESSES.md | 1.0 | skills/nasa-se/knowledge/processes/ | 650 |
| CI-016 | EXAMPLE-REQUIREMENTS.md | 1.0 | skills/nasa-se/knowledge/exemplars/ | 334 |
| CI-017 | EXAMPLE-RISK-REGISTER.md | 1.0 | skills/nasa-se/knowledge/exemplars/ | 329 |
| CI-018 | BEHAVIOR_TESTS.md | 2.0 | skills/nasa-se/tests/ | ~600 |
| CI-019 | review-checklists/ | 1.0 | skills/nasa-se/templates/ | ~500 |

**Total Lines:** ~8,818

### Baseline Strategy

| Baseline | Phase | Contents | Purpose |
|----------|-------|----------|---------|
| BL-001 | Deployment | All 19 CIs | Product baseline for deployment |
| BL-002 | Post-SME | + SME corrections | Updated after user validation |
| BL-003 | v1.1 | + Enhancements | Feature updates |

### CI Selection Criteria Applied

Items selected for configuration control based on:
- [x] Required for skill functionality
- [x] Subject to change during maintenance
- [x] Multiple agents depend on it (knowledge base)
- [x] Impacts interfaces (agents, SKILL.md)
- [x] Has verification requirements (all agents)

### Change Control Process

| Change Type | Authority | Process |
|-------------|-----------|---------|
| Minor (typo, formatting) | Claude Code | Direct commit |
| Content update (knowledge) | Claude Code + User review | PR with review |
| Agent modification | User approval | Formal review |
| Baseline update | User | Gate approval |

### Dependencies

| CI ID | Depends On | Depended By |
|-------|------------|-------------|
| CI-001 | - | All agents |
| CI-002 to CI-009 | CI-001, CI-013 | CI-010, CI-011, CI-012 |
| CI-010 | CI-002 to CI-009 | Users |
| CI-011 | CI-002 to CI-009 | Users |
| CI-012 | CI-002 to CI-009 | Orchestration flows |
| CI-014 to CI-017 | - | CI-002 to CI-009 |
| CI-018 | CI-002 to CI-009 | QA |
| CI-019 | - | CI-006 (nse-reviewer) |

---

## Baseline Approval

| Role | Name | Date | Status |
|------|------|------|--------|
| CM Manager | Claude Code | 2026-01-09 | ✅ Recommended |
| Technical Lead | Claude Code | 2026-01-09 | ✅ Recommended |
| Project Authority | User | Pending | ⏳ Required |

---

## Change Log

| Date | Action | CI IDs | By | Notes |
|------|--------|--------|-------|-------|
| 2026-01-09 | Initial baseline | All | Claude Code | BL-001 established |

---

## References

- NPR 7123.1D Process 14 - Configuration Management
- NPR 7123.1D Process 15 - Technical Data Management
- NASA-HDBK-1009A - CM Work Products

---

*DISCLAIMER: This Configuration Item List is AI-generated based on NASA Systems Engineering standards. It is advisory only and does not constitute official NASA guidance. All configuration management decisions require human review and professional engineering judgment.*
