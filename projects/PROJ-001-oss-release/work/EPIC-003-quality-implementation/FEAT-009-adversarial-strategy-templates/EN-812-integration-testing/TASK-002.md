# TASK-002: Write strategy ID validation tests against SSOT

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
> **Parent:** EN-812

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

Write pytest E2E tests that validate all strategy IDs used in templates, agent files, and criticality mappings match the authoritative Strategy Catalog in quality-enforcement.md. These tests form the second category of the E2E test suite in `tests/e2e/test_adversary_templates_e2e.py`.

The tests must verify consistency of strategy IDs across three sources:

1. **SSOT (quality-enforcement.md)** -- The authoritative source. Parse the Strategy Catalog table to extract the 10 selected strategy IDs: S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014. Also extract their composite scores and strategy families.

2. **Template filenames and Identity sections** -- Each template file in `.context/templates/adversarial/` uses the strategy ID in its filename (e.g., `S-002-devils-advocate.md`) and declares the ID in its Identity section. Verify that:
   - All template filenames contain valid strategy IDs from the SSOT
   - Each template's Identity section declares the correct strategy ID
   - The composite score in the Identity section matches the SSOT
   - The strategy family in the Identity section matches the SSOT

3. **Agent references** -- Agent files (adv-selector, adv-executor, adv-scorer) and updated skill agents (ps-critic, ps-reviewer, nse-reviewer, ps-architect) reference strategy IDs. Verify that all referenced IDs are valid per the SSOT.

Test implementation approach:
- Parse quality-enforcement.md to extract the Strategy Catalog as the authoritative set
- Use `pathlib.Path.glob` to find all template files
- Parse template Identity sections using regex
- Parse agent files for strategy ID references
- Compare all extracted IDs against the SSOT set
- Flag any IDs present in templates/agents but missing from SSOT (orphaned)
- Flag any IDs present in SSOT but missing from templates (gap)

### Acceptance Criteria
- [ ] Tests parse quality-enforcement.md to extract authoritative strategy ID set
- [ ] Tests validate all 10 template filenames contain valid SSOT strategy IDs
- [ ] Tests validate template Identity sections match SSOT (ID, composite score, family)
- [ ] Tests validate agent files reference only valid SSOT strategy IDs
- [ ] Tests detect orphaned IDs (in templates but not in SSOT)
- [ ] Tests detect gap IDs (in SSOT but not in templates)
- [ ] Tests use `@pytest.mark.e2e` marker
- [ ] Test file includes type hints (H-11) and docstrings (H-12)
- [ ] Quality gate: Deliverable reviewed via creator-critic-revision cycle (min 3 iterations)
- [ ] Quality gate: Score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] Quality gate: S-003 Steelman applied before S-002 Devil's Advocate critique

### Related Items
- Parent: [EN-812: Integration Testing](EN-812-integration-testing.md)
- Depends on: quality-enforcement.md (SSOT for strategy IDs)
- Depends on: EN-803 through EN-809 (strategy templates must exist)
- Depends on: EN-810 (agent files must exist for agent reference validation)

---

## Evidence
### Deliverables
| Deliverable | Type | Link |
|-------------|------|------|
| Strategy ID validation tests | Python test file | `tests/e2e/test_adversary_templates_e2e.py` (strategy ID section) |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History
| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. |
