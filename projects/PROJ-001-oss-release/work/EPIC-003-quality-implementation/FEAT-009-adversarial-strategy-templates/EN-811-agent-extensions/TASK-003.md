# TASK-003: Update nse-reviewer.md with strategy template references

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

Add a "Strategy Template References" section to `skills/nasa-se/agents/nse-reviewer.md` that points to the concrete adversarial strategy execution templates in `.context/templates/adversarial/`. The nse-reviewer agent performs NASA-SE technical reviews (requirements verification, design validation, V&V activities) and needs direct references to the 4 strategies most relevant to its review domain:

- **S-007 Constitutional AI Critique** at `.context/templates/adversarial/S-007-constitutional-ai.md` -- Compliance checking against HARD rules and governance constraints. Essential for requirements reviews ensuring compliance with the Jerry constitution and quality framework.
- **S-012 FMEA** at `.context/templates/adversarial/S-012-fmea.md` -- Failure Mode and Effects Analysis for systematic identification of potential failure modes in designs, requirements, and processes. Core NASA-SE review technique.
- **S-013 Inversion Technique** at `.context/templates/adversarial/S-013-inversion.md` -- Assumption inversion for testing design robustness. Used to challenge requirements assumptions and verify that designs handle inverted conditions.
- **S-014 LLM-as-Judge** at `.context/templates/adversarial/S-014-llm-as-judge.md` -- Quality scoring with 6-dimension rubric for formal technical review assessments.

The section must include:
- Template path for each strategy
- When to use each strategy in NASA-SE review workflows (requirements review, design review, V&V)
- Instructions to load and follow the Execution Protocol section of each template
- Mapping between NASA-SE review types and recommended strategies

### Acceptance Criteria
- [ ] nse-reviewer.md updated with "Strategy Template References" section
- [ ] References for S-007, S-012, S-013, S-014 with correct template paths
- [ ] NASA-SE review type to strategy mapping documented
- [ ] Instructions to load and follow Execution Protocol section
- [ ] Navigation table updated to include new section
- [ ] All strategy IDs match quality-enforcement.md SSOT
- [ ] Quality gate: Deliverable reviewed via creator-critic-revision cycle (min 3 iterations)
- [ ] Quality gate: Score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] Quality gate: S-003 Steelman applied before S-002 Devil's Advocate critique

### Related Items
- Parent: [EN-811: Agent Extensions](EN-811-agent-extensions.md)
- Depends on: EN-805 (S-007 template must exist)
- Depends on: EN-808 (S-012, S-013 templates must exist)
- Depends on: EN-803 (S-014 template must exist)

---

## Evidence
### Deliverables
| Deliverable | Type | Link |
|-------------|------|------|
| Updated nse-reviewer.md | Agent markdown | `skills/nasa-se/agents/nse-reviewer.md` |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History
| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. |
