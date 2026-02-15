# TASK-001: Write S-001-red-team.md

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** pending
> **Priority:** HIGH
> **Activity:** DEVELOPMENT
> **Agents:** ps-architect
> **Created:** 2026-02-14
> **Parent:** EN-809

---

## Document Sections
| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Parent and dependencies |
| [History](#history) | Change log |

---

## Summary

Create the Red Team Analysis execution template at `.context/templates/adversarial/S-001-red-team.md`. This template defines the adversary simulation protocol for security-sensitive work within the Jerry quality framework. Red Team Analysis (S-001, composite score 3.35) is a Role-Based Adversarialism strategy used exclusively in C4 (critical/irreversible) quality cycles where all 10 strategies must be exercised.

The template must include:
- **Threat actor emulation**: Define adversary profiles (naive user, experienced developer, malicious actor) with distinct goals, capabilities, and attack motivations relevant to Jerry's domain (framework governance, quality rules, context management).
- **Attack planning**: Structured approach to identifying attack surfaces in deliverables (documents, code, architecture decisions), including assumption inversion and boundary testing.
- **Execution documentation**: Step-by-step protocol with RT-NNN identifiers for each finding, severity classification (Critical, High, Medium, Low), and exploitation evidence.
- **Remediation validation**: Process for verifying that identified vulnerabilities are addressed in revision cycles, including regression checks.

### Acceptance Criteria
- [ ] Template file created at `.context/templates/adversarial/S-001-red-team.md`
- [ ] Template follows TEMPLATE-FORMAT.md with all 8 canonical sections (Identity, Purpose, Prerequisites, Execution Protocol, Output Format, Scoring Rubric, Examples, Integration)
- [ ] Threat actor emulation section includes >= 3 adversary profiles with distinct goals and capabilities
- [ ] Attack planning section includes attack surface identification methodology and assumption inversion protocol
- [ ] Execution documentation section defines RT-NNN identifier format with severity classification
- [ ] Remediation validation section includes regression check protocol
- [ ] Integration section maps S-001 to C4 criticality level and identifies companion strategies
- [ ] Anti-patterns section includes >= 3 common Red Team mistakes
- [ ] Strategy ID S-001 matches quality-enforcement.md SSOT entry (composite score 3.35, family: Role-Based Adversarialism)
- [ ] Quality gate: Deliverable reviewed via creator-critic-revision cycle (min 3 iterations)
- [ ] Quality gate: Score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] Quality gate: S-003 Steelman applied before S-002 Devil's Advocate critique

### Related Items
- Parent: [EN-809: Tier 4 Security Strategy Templates](EN-809-tier4-security-strategies.md)
- Depends on: EN-801 (TEMPLATE-FORMAT.md must exist)
- Parallel: TASK-002 (S-011 CoVe template)
- Blocks: TASK-003 (quality cycle review)

---

## Evidence
### Deliverables
| Deliverable | Type | Link |
|-------------|------|------|
| S-001 Red Team Analysis template | Strategy template | `.context/templates/adversarial/S-001-red-team.md` |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History
| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. |
