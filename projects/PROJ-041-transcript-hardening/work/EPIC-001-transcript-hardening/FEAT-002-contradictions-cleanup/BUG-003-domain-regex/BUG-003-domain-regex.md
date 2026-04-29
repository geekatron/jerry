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
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
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

## Acceptance Criteria

- [ ] Decision recorded: `schemas/DOMAIN-SCHEMA.json` is canonical.
- [ ] `contexts/schemas/domain-schema.json` and `schemas/context-domain-schema.json` either deleted (preferred) or marked deprecated with a pointer to `DOMAIN-SCHEMA.json`.
- [ ] All references across the codebase updated to point to `DOMAIN-SCHEMA.json`.
- [ ] `grep -r 'context-domain-schema\|domain-schema' --include='*.json' --include='*.md' --include='*.py'` shows only references to the canonical schema (no orphaned references to the two losing schemas).
- [ ] Schema validation passes against a packet with each of the 6 registered domain values.
- [ ] Schema validation REJECTS a packet with a domain not in the closed list (regression test).

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
