# EPIC-004: /red-team Skill Build

> **Type:** epic
> **Status:** pending
> **Priority:** critical
> **Impact:** critical
> **Created:** 2026-02-22
> **Due:** ---
> **Completed:** ---
> **Parent:** —
> **Owner:** Adam Nowak
> **Target Quarter:** FY26-Q1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key objectives |
| [Business Outcome Hypothesis](#business-outcome-hypothesis) | Expected business outcomes |
| [Children Features/Capabilities](#children-featurescapabilities) | Feature inventory and tracking |
| [Progress Summary](#progress-summary) | Overall epic progress |
| [Related Items](#related-items) | Dependencies and related epics |
| [History](#history) | Status changes and key events |

---

## Summary

Build the /red-team skill with 9 agents (red-lead, red-recon, red-vuln, red-exploit, red-privesc, red-lateral, red-persist, red-exfil, red-reporter). Includes SKILL.md, routing, agent definitions, methodology controls (PTES, OSSTMM, MITRE ATT&CK), authorization verification (R-020), templates, and /adversary integration.

**Key Objectives:**
- Define 9 agent definitions with real offensive techniques mapped to MITRE ATT&CK per R-018
- Implement authorization verification before any active testing per R-020
- Ensure actionable remediation guidance in all findings per R-021
- Build tool integration adapters for offensive tooling (Metasploit, Burp Suite, Nmap, etc.) per R-012
- Enforce methodology compliance with PTES and OSSTMM frameworks

---

## Business Outcome Hypothesis

**We believe that** a structured red team skill with authorization controls, methodology enforcement, and MITRE ATT&CK mapping

**Will result in** professional-grade penetration testing guidance that is safe, methodical, and produces actionable findings

**We will know we have succeeded when** all agents pass C4 /adversary review at >= 0.95, complete MITRE ATT&CK tactic coverage is achieved, authorization controls provably prevent unauthorized testing, and all findings include remediation guidance

---

## Children Features/Capabilities

### Feature Inventory

| ID | Title | Status | Priority | Progress |
|----|-------|--------|----------|----------|
| FEAT-030 | SKILL.md & Routing | pending | critical | 0% |
| FEAT-031 | Recon & Vulnerability Agents (red-lead, red-recon, red-vuln) | pending | critical | 0% |
| FEAT-032 | Exploitation Agents (red-exploit, red-privesc) | pending | critical | 0% |
| FEAT-033 | Post-Exploitation Agents (red-lateral, red-persist, red-exfil) | pending | critical | 0% |
| FEAT-034 | Reporting Agent (red-reporter) | pending | high | 0% |
| FEAT-035 | Methodology & Authorization Controls | pending | critical | 0% |
| FEAT-036 | Templates & Playbook | pending | high | 0% |
| FEAT-037 | /adversary Integration | pending | high | 0% |

### Feature Links

- [FEAT-030: SKILL.md & Routing](./FEAT-030-red-skill-routing/FEAT-030-red-skill-routing.md)
- [FEAT-031: Recon & Vulnerability Agents](./FEAT-031-recon-vulnerability-agents/FEAT-031-recon-vulnerability-agents.md)
- [FEAT-032: Exploitation Agents](./FEAT-032-exploitation-agents/FEAT-032-exploitation-agents.md)
- [FEAT-033: Post-Exploitation Agents](./FEAT-033-post-exploitation-agents/FEAT-033-post-exploitation-agents.md)
- [FEAT-034: Reporting Agent](./FEAT-034-reporting-agent/FEAT-034-reporting-agent.md)
- [FEAT-035: Methodology & Authorization Controls](./FEAT-035-methodology-authorization-controls/FEAT-035-methodology-authorization-controls.md)
- [FEAT-036: Templates & Playbook](./FEAT-036-templates-playbook/FEAT-036-templates-playbook.md)
- [FEAT-037: /adversary Integration](./FEAT-037-adversary-integration/FEAT-037-adversary-integration.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                     EPIC PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Features:  [....................] 0% (0/8 completed)              |
| Enablers:  [....................] 0% (0/33 completed)             |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                               |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Features** | 8 |
| **Completed Features** | 0 |
| **In Progress Features** | 0 |
| **Pending Features** | 8 |
| **Feature Completion %** | 0% |

---

## Related Items

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | EPIC-002 | Agent definitions and methodology controls require architectural decisions from Phase 2 |
| Blocks | EPIC-005 | Purple team validation requires completed /red-team skill |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-22 | Claude | pending | Epic created with 8 features, 33 enablers |
