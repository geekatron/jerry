# FEAT-031: Recon & Vulnerability Agents (red-lead, red-recon, red-vuln)

> **Type:** feature
> **Status:** pending
> **Priority:** critical
> **Impact:** critical
> **Created:** 2026-02-22
> **Due:** ---
> **Completed:** ---
> **Parent:** EPIC-004
> **Owner:** ---
> **Target Sprint:** ---

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Feature description and scope |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Children Stories/Enablers](#children-storiesenablers) | Enabler inventory |
| [Progress Summary](#progress-summary) | Completion tracking |
| [Dependencies](#dependencies) | Upstream and downstream links |
| [History](#history) | Status changes and key events |

---

## Summary

Build red-lead, red-recon, and red-vuln agent definitions. red-lead handles scope definition, rules of engagement, methodology selection, and authorization verification. red-recon covers OSINT, network enumeration, service discovery, and attack surface mapping. red-vuln performs CVE research, exploit availability assessment, attack path analysis, and CVSS scoring.

---

## Acceptance Criteria

- [ ] red-lead agent definition with authorization verification (R-020)
- [ ] red-recon agent definition with real reconnaissance techniques (R-018)
- [ ] red-vuln agent definition with CVSS scoring and attack path analysis
- [ ] All agents mapped to MITRE ATT&CK tactics (R-018)
- [ ] All agents follow agent-development-standards (R-022)
- [ ] All agents portable across LLMs (R-010)
- [ ] Passes C4 /adversary review >= 0.95

---

## Children Stories/Enablers

| ID | Title | Status | Priority | Category |
|----|-------|--------|----------|----------|
| EN-304 | red-lead Agent Definition | pending | critical | architecture |
| EN-305 | red-recon Agent Definition | pending | critical | architecture |
| EN-306 | red-vuln Agent Definition | pending | critical | architecture |
| EN-307 | MITRE ATT&CK Mapping (Recon/Discovery) | pending | high | compliance |
| EN-308 | Quality Gate: Recon/Vuln Agents Review | pending | critical | compliance |

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Total Enablers** | 5 |
| **Completed Enablers** | 0 |
| **Completion %** | 0% |

---

## Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | FEAT-030 | Requires SKILL.md routing table for agent registration |
| Depends On | FEAT-015 | Authorization architecture for scope verification |
| Blocks | FEAT-032 | Recon findings feed exploitation agents |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-22 | --- | pending | Feature created during EPIC-004 decomposition |
