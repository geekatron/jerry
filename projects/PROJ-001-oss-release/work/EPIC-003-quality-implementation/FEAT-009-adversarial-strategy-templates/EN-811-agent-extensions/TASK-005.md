# TASK-005: Update CLAUDE.md with /adversary skill entry

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

Add the `/adversary` skill entry to the Skills table in the CLAUDE.md Quick Reference section. This is required for H-22 (proactive skill invocation) to apply to the /adversary skill. Without the CLAUDE.md entry, the skill is not discoverable by agents or users through the primary navigation document.

The entry must be added to the existing Skills table in the Quick Reference section of CLAUDE.md, following the established format:

```markdown
| `/adversary` | Adversarial quality review |
```

Additionally, the mandatory-skill-usage.md trigger map should be updated to include /adversary triggers:

```markdown
| adversarial, quality review, red team, devil's advocate, steelman, critique | `/adversary` |
```

This task also involves verifying that AE-002 auto-escalation applies since CLAUDE.md is in the `.context/rules/` governance scope (it is the root-level configuration file). However, since CLAUDE.md is not in `.context/rules/`, AE-002 does not apply directly. The modification is a C2 (Standard) change -- adding a single table row to an existing file, reversible within 1 day.

### Acceptance Criteria
- [ ] CLAUDE.md Skills table includes `/adversary` entry with purpose "Adversarial quality review"
- [ ] Entry follows the existing table format (pipe-delimited, skill name with slash, purpose description)
- [ ] Entry is positioned alphabetically or logically within the existing skills list
- [ ] No other CLAUDE.md content is modified beyond the Skills table addition
- [ ] Quality gate: Deliverable reviewed via creator-critic-revision cycle (min 3 iterations)
- [ ] Quality gate: Score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] Quality gate: S-003 Steelman applied before S-002 Devil's Advocate critique

### Related Items
- Parent: [EN-811: Agent Extensions](EN-811-agent-extensions.md)
- Depends on: EN-802 (/adversary skill skeleton must exist with SKILL.md)
- Depends on: EN-810 (/adversary skill agents must exist for skill to be functional)
- Related: mandatory-skill-usage.md (trigger map may also be updated)

---

## Evidence
### Deliverables
| Deliverable | Type | Link |
|-------------|------|------|
| Updated CLAUDE.md | Configuration | `CLAUDE.md` |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History
| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. |
