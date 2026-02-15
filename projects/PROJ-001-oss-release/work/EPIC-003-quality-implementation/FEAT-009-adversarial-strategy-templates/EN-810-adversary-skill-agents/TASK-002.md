# TASK-002: Write adv-executor.md agent

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

Create the strategy execution agent at `skills/adversary/agents/adv-executor.md`. This agent is the workhorse of the /adversary skill, responsible for loading the appropriate strategy template from `.context/templates/adversarial/` and executing the Execution Protocol section step-by-step against a deliverable under review.

The agent must implement the following operational phases:

1. **Template loading**: Accept a strategy ID (e.g., S-002) from adv-selector's execution plan. Resolve the template path using the naming convention `.context/templates/adversarial/S-{NNN}-{name}.md`. Validate that the template file exists and contains the required Execution Protocol section.

2. **Context gathering**: Read the deliverable under review and extract relevant context for the strategy. This includes the deliverable's content, its parent work item metadata (enabler/task), the criticality level, and any prior strategy execution results from the current quality cycle.

3. **Protocol execution**: Execute each step in the template's Execution Protocol section sequentially. For each step, apply the protocol instruction to the deliverable, document findings using the strategy-specific identifier format (e.g., RT-NNN for Red Team, DA-NNN for Devil's Advocate, CV-NNN for CoVe), and record the evidence supporting each finding.

4. **Output formatting**: Format the execution results according to the template's Output Format section. Include the strategy ID, execution timestamp, deliverable reference, all findings with identifiers, severity classifications where applicable, and a summary of key issues discovered.

### Acceptance Criteria
- [ ] Agent file created at `skills/adversary/agents/adv-executor.md`
- [ ] Template loading mechanism defined with path resolution using `.context/templates/adversarial/S-{NNN}-{name}.md` convention
- [ ] Template validation checks for required Execution Protocol section
- [ ] Context gathering protocol defined for reading deliverable and extracting metadata
- [ ] Protocol execution defined as sequential step-by-step processing
- [ ] Strategy-specific identifier formats documented for all 10 strategies
- [ ] Output formatting follows each template's Output Format section
- [ ] Error handling defined for missing templates, malformed protocols, and execution failures
- [ ] Agent follows markdown navigation standards (H-23, H-24)
- [ ] P-003 compliance: agent does not spawn sub-agents
- [ ] Quality gate: Deliverable reviewed via creator-critic-revision cycle (min 3 iterations)
- [ ] Quality gate: Score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] Quality gate: S-003 Steelman applied before S-002 Devil's Advocate critique

### Related Items
- Parent: [EN-810: Adversary Skill Agents](EN-810-adversary-skill-agents.md)
- Depends on: EN-801 (TEMPLATE-FORMAT.md defines Execution Protocol section structure)
- Depends on: EN-803 through EN-809 (strategy templates must exist)
- Parallel: TASK-001 (adv-selector), TASK-003 (adv-scorer)
- Blocks: TASK-004 (quality cycle review)

---

## Evidence
### Deliverables
| Deliverable | Type | Link |
|-------------|------|------|
| adv-executor agent definition | Agent markdown | `skills/adversary/agents/adv-executor.md` |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History
| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. |
