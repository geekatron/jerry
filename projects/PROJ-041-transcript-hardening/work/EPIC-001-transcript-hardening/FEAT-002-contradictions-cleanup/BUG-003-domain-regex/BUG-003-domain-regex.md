# BUG-003: domain regex — 3 disagreeing schemas

> **Type:** bug
> **Status:** pending
> **Priority:** high
> **Impact:** medium
> **Severity:** major
> **Created:** 2026-04-28T00:00:00Z
> **Parent:** FEAT-002
> **Owner:** adam.nowak
> **Effort:** 1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What's contradicted |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the disagreement |
| [Affected Documents](#affected-documents) | Where the disagreement lives |
| [Recommended Resolution](#recommended-resolution) | Audit's stated fix |
| [Agent Assignment](#agent-assignment) | Specific skill+agent mappings |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Change log |

---

## Summary

Three domain schemas exist and disagree. Two are regex-based; one is the closed-list enum form aligned with the registered 6-domain list.

---

## Steps to Reproduce

1. Run `find . -name 'domain*schema*.json' -o -name 'DOMAIN-SCHEMA.json'` in the framework root.
2. Observe three schema files exist: `contexts/schemas/domain-schema.json`, `schemas/context-domain-schema.json`, and `schemas/DOMAIN-SCHEMA.json`.
3. Open each and compare validation rules: two are regex-based with different floors; one is closed-list enum aligned with the registered 6-domain list.
4. Construct a packet whose domain field uses a value passing the loosest schema. Validate against each.
5. Observe inconsistent pass/reject results across the three schemas — the framework cannot consistently validate domain values.

---

## Affected Documents

| Document | Says |
|----------|------|
| `contexts/schemas/domain-schema.json` | Regex-based (looser) |
| `schemas/context-domain-schema.json` | Regex-based (different floor) |
| `schemas/DOMAIN-SCHEMA.json` | Closed-list enum (stronger validation, aligns with 6-domain list) |

---

## Recommended Resolution

Per audit: **pick the closed-list `DOMAIN-SCHEMA.json` form** (enum-based, stronger validation; aligns with the registered 6-domain list). Delete or deprecate the two regex schemas. Update all references to point to `DOMAIN-SCHEMA.json`.

---

## Agent Assignment

| Step | Skill | Agent | Purpose |
|------|-------|-------|---------|
| 1 | `/problem-solving` | `ps-architect` | Author ADR recording the canonical-schema choice (`DOMAIN-SCHEMA.json` enum form) and rationale |
| 2 | `/eng-team` | `eng-lead` | Delete or deprecate `contexts/schemas/domain-schema.json` and `schemas/context-domain-schema.json`; update all references |
| 3 | `/eng-team` | `eng-qa` | Regression: 6 registered domain values pass; out-of-list value rejected |
| 4 | `/problem-solving` | `ps-validator` | Grep for orphaned references to losing schemas; verify zero matches |
| 5 | `/eng-team` | `eng-reviewer` | Final-gate review on schema deletion + canonical-choice ADR (governance-class change) per ps-architect D-4.4 |
| 6 | `/adversary` | `adv-executor` + `adv-scorer` | C4 ≥0.95 review (governance change) |
| 7 | `/worktracker` | `wt-verifier` | Validate AC; close |

---

## Acceptance Criteria

- [ ] Decision recorded: `schemas/DOMAIN-SCHEMA.json` is canonical.
- [ ] `contexts/schemas/domain-schema.json` and `schemas/context-domain-schema.json` either deleted (preferred) or marked deprecated with a pointer to `DOMAIN-SCHEMA.json`.
- [ ] All references across the codebase updated to point to `DOMAIN-SCHEMA.json`.
- [ ] `grep -r 'context-domain-schema\|domain-schema' --include='*.json' --include='*.md' --include='*.py'` shows only references to the canonical schema (no orphaned references to the two losing schemas).
- [ ] Schema validation passes against a packet with each of the 6 registered domain values.
- [ ] Schema validation REJECTS a packet with a domain not in the closed list (regression test).

---

## Children Tasks

| ID | Title | Owner | Status |
|----|-------|-------|--------|
| [TASK-029](./TASK-029-author-canonical-domain-schema-adr.md) | Author ADR recording canonical-schema choice (DOMAIN-SCHEMA.json) | `ps-architect` | pending |
| [TASK-030](./TASK-030-delete-losing-domain-schemas.md) | Delete or deprecate contexts/schemas/domain-schema.json and schemas/context-domain-schema.json | `eng-lead` | pending |
| [TASK-031](./TASK-031-regression-test-domain-enum.md) | Regression: 6 registered domain values pass; out-of-list value rejected | `eng-qa` | pending |
| [TASK-032](./TASK-032-grep-orphaned-references.md) | Grep for orphaned references to losing schemas; verify zero matches | `ps-validator` | pending |
| [TASK-033](./TASK-033-final-gate-review-canonical-choice.md) | Final-gate review on schema deletion + canonical-choice ADR (per ps-architect D-4.4) | `eng-reviewer` | pending |
| [TASK-034](./TASK-034-run-adversary-c4-review.md) | Run /adversary C4 review | `adv-executor` | pending |
| [TASK-035](./TASK-035-validate-ac-and-close-bug-003.md) | Validate BUG-003 AC and close | `wt-verifier` | pending |


---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-002](../FEAT-002-contradictions-cleanup.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocks | FEAT-001 STORY-002 | ADR-007 promotion blocked while contradictions remain |
| Blocks | FEAT-003 STORY-006 | SCHEMA-* validators need a single canonical domain schema |

### Source

- [#273 §C4.3](https://github.com/geekatron/jerry/issues/273)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Bug created from audit finding C4.3. |
