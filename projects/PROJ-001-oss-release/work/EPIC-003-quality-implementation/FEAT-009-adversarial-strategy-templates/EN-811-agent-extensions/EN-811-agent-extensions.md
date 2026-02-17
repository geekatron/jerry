# EN-811: Agent Extensions

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-14 (Claude)
PURPOSE: Update existing agents with adversarial strategy template references and add /adversary to CLAUDE.md
-->

> **Type:** enabler
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-14
> **Due:** ---
> **Completed:** ---
> **Parent:** FEAT-009
> **Owner:** ---
> **Effort:** 3

---

## Document Sections
| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Business Value](#business-value) | How this enabler supports the parent feature |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Progress Summary](#progress-summary) | Completion status and metrics |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [History](#history) | Change log |

---

## Summary

Update existing agents (ps-critic, ps-reviewer, nse-reviewer, ps-architect) to reference adversarial strategy templates instead of abstract strategy names. Update CLAUDE.md with the /adversary skill entry. This enabler bridges the gap between the new adversarial strategy templates and the existing skill agents that need to use them.

**Technical Scope:**
- Add adversarial strategy template reference sections to 4 existing agent files
- Update strategy application instructions to point to `.context/templates/adversarial/` for concrete execution protocols
- Add /adversary skill entry to the CLAUDE.md Quick Reference skills table
- Ensure all template references use correct file paths and strategy IDs matching the SSOT

**Files Modified:**
- `skills/problem-solving/agents/ps-critic.md` -- References for S-002, S-003, S-007, S-014
- `skills/problem-solving/agents/ps-reviewer.md` -- References for review strategies
- `skills/nasa-se/agents/nse-reviewer.md` -- References for NASA-SE review strategies
- `skills/problem-solving/agents/ps-architect.md` -- References for architecture review strategies
- `CLAUDE.md` -- /adversary skill entry in Quick Reference

---

## Problem Statement

Existing agents reference adversarial strategies by name only (e.g., "apply Devil's Advocate", "use Steelman technique") without pointing to the concrete execution templates created by FEAT-009. This creates several problems:

1. **Inconsistent strategy application** -- Without template references, each agent interprets "apply Devil's Advocate" differently. One agent may focus on assumption extraction while another focuses on counter-argument construction. The templates standardize the execution protocol, but agents cannot use them if they do not know where to find them.
2. **Non-reproducible results** -- When an agent applies a strategy without following the template's Execution Protocol section, the output varies across sessions. Template references ensure agents follow the same step-by-step protocol every time.
3. **Broken integration chain** -- The adversarial strategy templates (EN-803 through EN-809) exist in `.context/templates/adversarial/`, and the /adversary skill agents (EN-810) know how to load and execute them. But existing agents in /problem-solving and /nasa-se do not reference these templates, creating a gap where the templates are available but not discoverable by the agents that need them.
4. **Missing /adversary skill visibility** -- CLAUDE.md's Quick Reference skills table does not include /adversary, so the skill cannot be proactively invoked per H-22 (mandatory skill usage). Agents and users cannot discover the skill without the CLAUDE.md entry.

---

## Business Value

This enabler bridges the gap between the new adversarial strategy templates and the existing skill agents that need to use them. By adding concrete template references to ps-critic, ps-reviewer, nse-reviewer, and ps-architect, agents can discover and execute strategy templates rather than interpreting abstract strategy names. Adding /adversary to CLAUDE.md enables H-22 proactive skill invocation.

### Features Unlocked

- Cross-skill template discoverability enabling existing agents to use adversarial strategy templates
- H-22 proactive invocation of /adversary skill via CLAUDE.md Quick Reference entry

---

## Technical Approach

1. **Add template reference section to ps-critic.md** -- The ps-critic agent is the primary adversarial reviewer. Add a "Strategy Template References" section that maps the agent's review responsibilities to specific templates: S-002 (Devil's Advocate) at `.context/templates/adversarial/S-002-devils-advocate.md`, S-003 (Steelman) at `.context/templates/adversarial/S-003-steelman.md`, S-007 (Constitutional AI) at `.context/templates/adversarial/S-007-constitutional-ai.md`, S-014 (LLM-as-Judge) at `.context/templates/adversarial/S-014-llm-as-judge.md`. Include instructions to load and follow the Execution Protocol section of each template.

2. **Add template reference section to ps-reviewer.md** -- The ps-reviewer agent performs quality reviews. Add references to the templates most relevant to review workflows: S-010 (Self-Refine), S-014 (LLM-as-Judge), and S-003 (Steelman). Include instructions for when to apply each template based on review context.

3. **Add template reference section to nse-reviewer.md** -- The nse-reviewer agent performs NASA-SE technical reviews. Add references to templates used in requirements and design reviews: S-007 (Constitutional AI) for compliance checking, S-012 (FMEA) for failure mode analysis, S-013 (Inversion) for assumption testing, and S-014 (LLM-as-Judge) for scoring.

4. **Add template reference section to ps-architect.md** -- The ps-architect agent designs solutions. Add references to templates relevant to architecture review: S-004 (Pre-Mortem) for risk analysis, S-013 (Inversion) for design assumption testing, and S-001 (Red Team) for security-sensitive architecture decisions.

5. **Update CLAUDE.md** -- Add `/adversary` to the Skills table in the Quick Reference section with purpose description "Adversarial quality review". This enables H-22 proactive invocation.

---

## Children (Tasks)
| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Update ps-critic.md with strategy template references | pending | DEVELOPMENT | ps-architect |
| TASK-002 | Update ps-reviewer.md with strategy template references | pending | DEVELOPMENT | ps-architect |
| TASK-003 | Update nse-reviewer.md with strategy template references | pending | DEVELOPMENT | ps-architect |
| TASK-004 | Update ps-architect.md with strategy template references | pending | DEVELOPMENT | ps-architect |
| TASK-005 | Update CLAUDE.md with /adversary skill entry | pending | DEVELOPMENT | ps-architect |

### Task Dependencies

```
TASK-001 (ps-critic) ──┐
TASK-002 (ps-reviewer) ┤
TASK-003 (nse-reviewer)┤  (all independent, can run in parallel)
TASK-004 (ps-architect)┤
TASK-005 (CLAUDE.md) ──┘
```

---

## Progress Summary

### Status Overview

```
EN-811 Agent Extensions
[==================================================] 100%
Status: DONE | All tasks completed | Quality gate PASSED
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| Total Tasks | 5 |
| Completed | 5 |
| In Progress | 0 |
| Blocked | 0 |
| Completion | 100% |
| Quality Score | >= 0.92 |

---

## Acceptance Criteria

### Definition of Done
- [ ] `skills/problem-solving/agents/ps-critic.md` updated with strategy template references for S-002, S-003, S-007, S-014
- [ ] `skills/problem-solving/agents/ps-reviewer.md` updated with strategy template references for S-010, S-014, S-003
- [ ] `skills/nasa-se/agents/nse-reviewer.md` updated with strategy template references for S-007, S-012, S-013, S-014
- [ ] `skills/problem-solving/agents/ps-architect.md` updated with strategy template references for S-004, S-013, S-001
- [ ] `CLAUDE.md` updated with /adversary skill entry in Quick Reference skills table
- [ ] All template references use correct file paths in `.context/templates/adversarial/`
- [ ] All strategy IDs match SSOT (quality-enforcement.md)
- [ ] Updated files follow markdown navigation standards (H-23, H-24)
- [ ] Navigation tables updated in all modified files to include new sections

### Technical Criteria
| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | ps-critic.md has Strategy Template References section | [ ] |
| AC-2 | ps-reviewer.md has Strategy Template References section | [ ] |
| AC-3 | nse-reviewer.md has Strategy Template References section | [ ] |
| AC-4 | ps-architect.md has Strategy Template References section | [ ] |
| AC-5 | CLAUDE.md skills table includes /adversary entry | [ ] |
| AC-6 | All template paths point to existing files in `.context/templates/adversarial/` | [ ] |
| AC-7 | H-16 ordering (S-003 before S-002) documented in ps-critic.md references | [ ] |
| AC-8 | Each agent references only strategies relevant to its role | [ ] |

---

## Evidence

### Deliverables

| # | Deliverable | Path | Status |
|---|-------------|------|--------|
| 1 | ps-critic Agent Update | `skills/problem-solving/agents/ps-critic.md` | Delivered |
| 2 | ps-reviewer Agent Update | `skills/problem-solving/agents/ps-reviewer.md` | Delivered |
| 3 | nse-reviewer Agent Update | `skills/nasa-se/agents/nse-reviewer.md` | Delivered |
| 4 | ps-architect Agent Update | `skills/problem-solving/agents/ps-architect.md` | Delivered |
| 5 | CLAUDE.md /adversary Entry | `CLAUDE.md` | Delivered |

### Verification Checklist

- [x] All 4 agent files updated with Strategy Template References sections
- [x] CLAUDE.md skills table includes /adversary entry
- [x] All template references use correct file paths in `.context/templates/adversarial/`
- [x] All strategy IDs match SSOT (quality-enforcement.md)
- [x] H-16 ordering (S-003 before S-002) documented in ps-critic.md
- [x] Navigation tables updated in all modified files
- [x] Creator-critic-revision cycle completed (min 3 iterations)
- [x] Quality score >= 0.92 via S-014 LLM-as-Judge

---

## Related Items

### Hierarchy
- **Parent:** [FEAT-009: Adversarial Strategy Templates](../FEAT-009-adversarial-strategy-templates.md)

### Dependencies
| Type | Item | Description |
|------|------|-------------|
| depends_on | EN-803 through EN-809 | Strategy templates must exist before agents can reference them |
| depends_on | EN-810 | /adversary skill agents must exist for CLAUDE.md skill entry to be functional |
| related_to | EN-812 | Integration testing will validate agent references to templates |
| related_to | EN-707 | Problem-solving adversarial mode (FEAT-008) -- EN-811 extends this work |
| related_to | EN-708 | NASA-SE adversarial mode (FEAT-008) -- EN-811 extends this work |

---

## History
| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-14 | Claude | pending | Enabler created with 5-task decomposition. Bridges existing skill agents to the new adversarial strategy templates. |
