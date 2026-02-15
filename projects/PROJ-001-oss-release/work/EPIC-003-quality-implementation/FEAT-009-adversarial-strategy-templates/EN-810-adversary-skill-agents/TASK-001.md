# TASK-001: Write adv-selector.md agent

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
> **Parent:** EN-810

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

Create the strategy selection agent at `skills/adversary/agents/adv-selector.md`. This agent is the entry point for the /adversary skill, responsible for mapping criticality levels to the correct strategy sets as defined in quality-enforcement.md. It accepts a criticality level (C1-C4) and optional strategy overrides, then returns an ordered list of strategies to execute with their template paths.

The agent must implement the canonical criticality-to-strategy mapping:
- **C1 (Routine)**: {S-010} -- Reversible in 1 session, <3 files. Self-Refine only.
- **C2 (Standard)**: {S-007, S-002, S-014} -- Reversible in 1 day, 3-10 files. Constitutional AI Critique + Devil's Advocate + LLM-as-Judge.
- **C3 (Significant)**: C2 + {S-004, S-012, S-013} -- >1 day to reverse, >10 files, API changes. Adds Pre-Mortem + FMEA + Inversion.
- **C4 (Critical)**: All 10 selected strategies -- Irreversible, architecture/governance/public. Adds S-001 Red Team + S-003 Steelman + S-010 Self-Refine + S-011 CoVe.

The agent must also support:
- **Optional strategy overrides**: Allow adding or removing specific strategies from the default set for a criticality level, with justification logging.
- **Input format**: Criticality level (required), deliverable type (optional), override list (optional).
- **Output format**: Ordered strategy execution plan with strategy ID, name, template path, and execution sequence number.

### Acceptance Criteria
- [ ] Agent file created at `skills/adversary/agents/adv-selector.md`
- [ ] Criticality-to-strategy mapping matches quality-enforcement.md exactly
- [ ] C1 maps to {S-010}
- [ ] C2 maps to {S-007, S-002, S-014}
- [ ] C3 maps to C2 + {S-004, S-012, S-013}
- [ ] C4 maps to all 10 strategies {S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014}
- [ ] Optional strategy override mechanism defined with justification logging
- [ ] Input/output formats clearly specified
- [ ] Execution sequence ordering logic defined (e.g., S-003 Steelman before S-002 Devil's Advocate per H-16)
- [ ] Auto-escalation rules (AE-001 through AE-006) referenced for automatic criticality determination
- [ ] Agent follows markdown navigation standards (H-23, H-24)
- [ ] P-003 compliance: agent does not spawn sub-agents
- [ ] Quality gate: Deliverable reviewed via creator-critic-revision cycle (min 3 iterations)
- [ ] Quality gate: Score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] Quality gate: S-003 Steelman applied before S-002 Devil's Advocate critique

### Related Items
- Parent: [EN-810: Adversary Skill Agents](EN-810-adversary-skill-agents.md)
- Depends on: quality-enforcement.md (criticality-to-strategy mappings)
- Depends on: EN-802 (/adversary skill skeleton)
- Parallel: TASK-002 (adv-executor), TASK-003 (adv-scorer)
- Blocks: TASK-004 (quality cycle review)

---

## Evidence
### Deliverables
| Deliverable | Type | Link |
|-------------|------|------|
| adv-selector agent definition | Agent markdown | `skills/adversary/agents/adv-selector.md` |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History
| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. |
