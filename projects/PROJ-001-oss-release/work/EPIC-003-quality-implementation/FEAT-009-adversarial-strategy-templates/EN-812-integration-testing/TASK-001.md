# TASK-001: Write template format compliance tests

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

Write pytest E2E tests that validate all 10 strategy templates in `.context/templates/adversarial/` contain the 8 required sections defined in TEMPLATE-FORMAT.md. These tests form the first category of the E2E test suite in `tests/e2e/test_adversary_templates_e2e.py`.

The tests must verify that each strategy template file contains the following 8 canonical sections as markdown headings:
1. **Identity** -- Strategy ID, name, composite score, strategy family
2. **Purpose** -- When and why to use the strategy
3. **Prerequisites** -- Required inputs, context, and preconditions
4. **Execution Protocol** -- Step-by-step instructions for applying the strategy
5. **Output Format** -- Structure and format of the strategy's deliverable
6. **Scoring Rubric** -- Dimension-level scoring criteria aligned with quality-enforcement.md
7. **Examples** -- Calibration examples at multiple score levels
8. **Integration** -- How the strategy connects to criticality levels, quality cycle, and other strategies

The 10 strategy template files to test:
- `S-001-red-team.md`
- `S-002-devils-advocate.md`
- `S-003-steelman.md`
- `S-004-pre-mortem.md`
- `S-007-constitutional-ai.md`
- `S-010-self-refine.md`
- `S-011-cove.md`
- `S-012-fmea.md`
- `S-013-inversion.md`
- `S-014-llm-as-judge.md`

Test implementation approach:
- Use `pathlib.Path` to locate template files in `.context/templates/adversarial/`
- Read each template file content
- Use regex to find section headings (e.g., `## Identity`, `## Purpose`, etc.)
- Assert all 8 required sections are present
- Use `pytest.mark.parametrize` to test each template individually for clear failure reporting
- Mark tests with `@pytest.mark.e2e`

### Acceptance Criteria
- [ ] Tests check all 10 strategy template files for existence
- [ ] Tests verify all 8 required sections are present in each template
- [ ] Tests use `pytest.mark.parametrize` for individual template testing
- [ ] Tests use `@pytest.mark.e2e` marker
- [ ] Tests use `pathlib.Path` for file access
- [ ] Test functions follow naming convention: `test_{scenario}_when_{condition}_then_{expected}`
- [ ] Tests follow AAA pattern (Arrange, Act, Assert)
- [ ] Test file includes type hints (H-11) and docstrings (H-12)
- [ ] Quality gate: Deliverable reviewed via creator-critic-revision cycle (min 3 iterations)
- [ ] Quality gate: Score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] Quality gate: S-003 Steelman applied before S-002 Devil's Advocate critique

### Related Items
- Parent: [EN-812: Integration Testing](EN-812-integration-testing.md)
- Depends on: EN-801 (TEMPLATE-FORMAT.md defines the 8 required sections)
- Depends on: EN-803 through EN-809 (strategy templates must exist to be tested)

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
| Template format compliance tests | Python test file | `tests/e2e/test_adversary_templates_e2e.py` (format compliance section) |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History
| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. |
