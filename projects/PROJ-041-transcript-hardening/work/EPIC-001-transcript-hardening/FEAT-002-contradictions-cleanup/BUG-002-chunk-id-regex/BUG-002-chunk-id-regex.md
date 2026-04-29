# BUG-002: chunk_id regex divergence across 3 schemas

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
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Change log |

---

## Summary

`chunk_id` regex is specified inconsistently across three schemas. One allows 3-or-more digits (forward-compat for 1000+ chunk transcripts); two cap at exactly 3 digits.

---

## Steps to Reproduce

1. Run `grep -rn 'chunk-' --include='*.schema.json'` in the framework root.
2. Observe `extraction-report.json` schema uses `^chunk-\d{3,}$` (3-or-more digits).
3. Observe `chunk.schema.json` and `index.schema.json` use `^chunk-\d{3}$` (exactly 3 digits).
4. Construct a synthetic packet with chunk-1000+ identifiers. Validate against each schema.
5. Observe `extraction-report.json` schema accepts; `chunk.schema.json` and `index.schema.json` reject. The framework cannot consistently validate large transcripts.

---

## Affected Documents

| Document | Says |
|----------|------|
| `extraction-report.json` schema | `^chunk-\d{3,}$` |
| `chunk.schema.json` | `^chunk-\d{3}$` |
| `index.schema.json` | `^chunk-\d{3}$` |

---

## Recommended Resolution

Per audit: **converge on `^chunk-\d{3,}$`** (3-or-more digits, supports 1000+ chunk transcripts). Tightening the others to `\d{3}` would regress forward-compat, which is undesirable.

---

## Agent Assignment

| Step | Skill | Agent | Purpose |
|------|-------|-------|---------|
| 1 | `/eng-team` | `eng-lead` | Update `chunk.schema.json` and `index.schema.json` regex to `^chunk-\d{3,}$` |
| 2 | `/eng-team` | `eng-qa` | Add regression test: synthetic 1000+ chunk packet validates against all 3 schemas |
| 3 | `/problem-solving` | `ps-validator` | Grep across `**/*.schema.json` confirms no remaining `\d{3}$` (without comma) for chunk_id |
| 4 | `/adversary` | `adv-executor` + `adv-scorer` | C4 ≥0.95 review |
| 5 | `/worktracker` | `wt-verifier` | Validate AC; close |

---

## Acceptance Criteria

- [ ] `chunk.schema.json` regex updated to `^chunk-\d{3,}$`.
- [ ] `index.schema.json` regex updated to `^chunk-\d{3,}$`.
- [ ] `extraction-report.json` schema regex remains `^chunk-\d{3,}$` (no change needed).
- [ ] Regression test: schema validation passes against a synthetic 1000+ chunk packet (chunk-001 through chunk-1000+).
- [ ] FEAT-003 STORY-006 (SCHEMA-* validators) encodes consistent `chunk_id` regex across all rule paths.
- [ ] Audit grep across `**/*.schema.json` shows no remaining `\d{3}$` (without `,`) for `chunk_id`.

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-002](../FEAT-002-contradictions-cleanup.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocks | FEAT-001 STORY-002 | ADR-007 promotion blocked while contradictions remain |
| Blocks | FEAT-003 STORY-006 | SCHEMA-* validators need a single consistent regex |

### Source

- [#273 §C4.2](https://github.com/geekatron/jerry/issues/273)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Bug created from audit finding C4.2. |
