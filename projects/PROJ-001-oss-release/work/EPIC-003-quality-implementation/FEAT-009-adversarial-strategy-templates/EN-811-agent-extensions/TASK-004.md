# TASK-004: Update ps-architect.md with strategy template references

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
> **Parent:** EN-811

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

Add a "Strategy Template References" section to `skills/problem-solving/agents/ps-architect.md` that points to the concrete adversarial strategy execution templates in `.context/templates/adversarial/`. The ps-architect agent designs solutions, creates architecture decisions, and builds implementations. It needs direct references to the 3 strategies most relevant to architecture and design review:

- **S-004 Pre-Mortem Analysis** at `.context/templates/adversarial/S-004-pre-mortem.md` -- Prospective failure analysis for architecture decisions. Used to identify potential failure modes before they occur by imagining the design has already failed and working backwards to identify causes.
- **S-013 Inversion Technique** at `.context/templates/adversarial/S-013-inversion.md` -- Design assumption testing through systematic inversion of key assumptions. Used to stress-test architecture decisions by exploring what happens when foundational assumptions are violated.
- **S-001 Red Team Analysis** at `.context/templates/adversarial/S-001-red-team.md` -- Adversary simulation for security-sensitive architecture decisions. Used in C4 reviews when architecture decisions affect security, governance, or public-facing systems.

The section must include:
- Template path for each strategy
- When to use each strategy in architecture workflows (design phase, ADR creation, security review)
- Instructions to load and follow the Execution Protocol section of each template
- Guidance on when to escalate to C3/C4 review levels for architecture decisions

### Acceptance Criteria
- [ ] ps-architect.md updated with "Strategy Template References" section
- [ ] References for S-004, S-013, S-001 with correct template paths
- [ ] Architecture workflow integration documented (design phase, ADR creation, security review)
- [ ] Instructions to load and follow Execution Protocol section
- [ ] C3/C4 escalation guidance for architecture decisions included
- [ ] Navigation table updated to include new section
- [ ] All strategy IDs match quality-enforcement.md SSOT
- [ ] Quality gate: Deliverable reviewed via creator-critic-revision cycle (min 3 iterations)
- [ ] Quality gate: Score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] Quality gate: S-003 Steelman applied before S-002 Devil's Advocate critique

### Related Items
- Parent: [EN-811: Agent Extensions](EN-811-agent-extensions.md)
- Depends on: EN-808 (S-004, S-013 templates must exist)
- Depends on: EN-809 (S-001 template must exist)

---

## Evidence
### Deliverables
| Deliverable | Type | Link |
|-------------|------|------|
| Updated ps-architect.md | Agent markdown | `skills/problem-solving/agents/ps-architect.md` |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History
| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. |
