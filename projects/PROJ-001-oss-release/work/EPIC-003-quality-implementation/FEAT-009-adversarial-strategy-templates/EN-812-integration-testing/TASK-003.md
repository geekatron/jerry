# TASK-003: Write skill invocation and agent reference tests

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** DONE
> **Priority:** HIGH
> **Activity:** DEVELOPMENT
> **Agents:** ps-architect
> **Created:** 2026-02-14
> **Parent:** EN-812

---

## Document Sections
| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Time Tracking](#time-tracking) | Effort estimates and actuals |
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Parent and dependencies |
| [History](#history) | Change log |

---

## Summary

Write pytest E2E tests that verify the /adversary skill's structural integrity: SKILL.md and PLAYBOOK.md exist with required sections, all 3 agent files exist with required sections, and agents reference correct template paths. These tests form the third category of the E2E test suite in `tests/e2e/test_adversary_templates_e2e.py`.

The tests must verify:

1. **Skill file existence and structure**:
   - `skills/adversary/SKILL.md` exists and contains required sections (at minimum: a navigation table per H-23, purpose description, usage instructions)
   - `skills/adversary/PLAYBOOK.md` exists and contains required sections (workflow phases, strategy execution ordering, quality cycle integration)

2. **Agent file existence and structure**:
   - `skills/adversary/agents/adv-selector.md` exists and contains: criticality-to-strategy mapping, input/output format, override mechanism
   - `skills/adversary/agents/adv-executor.md` exists and contains: template loading protocol, execution steps, output formatting
   - `skills/adversary/agents/adv-scorer.md` exists and contains: 6-dimension rubric, weighted composite calculation, threshold comparison

3. **Agent template path references**:
   - Parse each agent file for references to `.context/templates/adversarial/` paths
   - Verify each referenced path corresponds to an existing template file
   - Verify adv-executor references all 10 strategy template paths
   - Verify adv-selector references all strategy IDs in its criticality mapping

Test implementation approach:
- Use `pathlib.Path` to check file existence
- Read file contents and use regex to find required section headings
- Extract template path references using regex (e.g., patterns matching `.context/templates/adversarial/S-NNN-*.md`)
- Cross-reference extracted paths against actual files in the template directory
- Mark tests with `@pytest.mark.e2e`

### Acceptance Criteria
- [ ] Tests verify SKILL.md exists with navigation table and required sections
- [ ] Tests verify PLAYBOOK.md exists with required sections
- [ ] Tests verify all 3 agent files exist (adv-selector, adv-executor, adv-scorer)
- [ ] Tests verify each agent file contains its required sections
- [ ] Tests extract template path references from agent files
- [ ] Tests verify extracted paths correspond to existing template files
- [ ] Tests verify adv-executor references all 10 strategy templates
- [ ] Tests use `@pytest.mark.e2e` marker
- [ ] Test file includes type hints (H-11) and docstrings (H-12)
- [ ] Quality gate: Deliverable reviewed via creator-critic-revision cycle (min 3 iterations)
- [ ] Quality gate: Score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] Quality gate: S-003 Steelman applied before S-002 Devil's Advocate critique

### Related Items
- Parent: [EN-812: Integration Testing](EN-812-integration-testing.md)
- Depends on: EN-802 (/adversary skill skeleton -- SKILL.md, PLAYBOOK.md)
- Depends on: EN-810 (agent files -- adv-selector, adv-executor, adv-scorer)
- Depends on: EN-803 through EN-809 (templates that agents reference)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | — |
| Remaining Work | 0 hours |
| Time Spent | — |

---

## Evidence
### Deliverables
| Deliverable | Type | Link |
|-------------|------|------|
| Skill invocation and agent reference tests | Python test file | `tests/e2e/test_adversary_templates_e2e.py` (skill/agent section) |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History
| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. |
