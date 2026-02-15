# TASK-002: Write S-007-constitutional-ai.md Following TEMPLATE-FORMAT

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
> **Parent:** EN-805

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

Create the S-007 Constitutional AI Critique template at `.context/templates/adversarial/S-007-constitutional-ai.md` with all 8 required sections from TEMPLATE-FORMAT.md. Include the principle-by-principle review checklist covering all HARD rules (H-01 through H-24) and auto-escalation rules (AE-001 through AE-006), violation severity classification (blocking, warning, informational), remediation guidance, and integration with the C2+ quality cycle.

### Acceptance Criteria

- [ ] File created at `.context/templates/adversarial/S-007-constitutional-ai.md`
- [ ] Identity section: S-007, Constitutional AI Critique, score 4.15, Iterative Self-Correction family
- [ ] Purpose section: when and why to use, C2+ mandatory trigger (H-18)
- [ ] Prerequisites section: required inputs (deliverable, principle inventory, context)
- [ ] Execution Protocol section: principle-by-principle review with numbered steps
- [ ] Output Format section: compliance report structure with violation details
- [ ] Scoring Rubric section: compliance assessment criteria per principle category
- [ ] Examples section: compliant deliverable, deliverable with blocking violation, deliverable with warning
- [ ] Integration section: C2+ quality cycle placement, interaction with S-014 scoring
- [ ] Principle checklist covers H-01 through H-24 grouped by source file
- [ ] Auto-escalation rules AE-001 through AE-006 included in checklist
- [ ] Violation classification defined: blocking (must fix), warning (should fix), informational
- [ ] File follows markdown navigation standards (H-23, H-24)
- [ ] Quality gate: Deliverable reviewed via creator-critic-revision cycle (min 3 iterations)
- [ ] Quality gate: Score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] Quality gate: S-003 Steelman applied before S-002 Devil's Advocate critique

### Related Items

- Parent: [EN-805: S-007 Constitutional AI Template](EN-805-s007-constitutional-ai.md)
- Depends on: TASK-001 (methodology extraction and principle inventory)
- Blocks: TASK-003 (quality cycle)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| `.context/templates/adversarial/S-007-constitutional-ai.md` | Strategy template | --- |

### Verification

- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. Core deliverable -- S-007 template operationalizes constitutional compliance review for C2+ deliverables. |
