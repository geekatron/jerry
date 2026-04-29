# BUG-004: seg-NNN regex — ADR-007 \d{3} vs schemas \d{3,}

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

Segment-anchor regex disagreement. Schemas use forward-compat `\d{3,}` (supports 1000+ segments). ADR-007 §3.1 specifies exactly `\d{3}` (caps at 999). This blocks any packet exceeding 999 segments — a real cap that matters for long technical sessions.

---

## Steps to Reproduce

1. Run `grep -rn 'seg-' --include='*.schema.json'` and observe schemas use `^seg-\d{3,}$`.
2. Open `docs/adrs/ADR-007-output-template-specification.md` §3.1 and observe `^seg-\d{3}$` (exactly 3 digits).
3. Construct a synthetic packet with `seg-1000` (a 4-digit segment ID).
4. Validate against schemas: passes. Validate against ADR-007 §3.1 specification: fails.
5. Observe: the framework's own canonical rule contradicts its schemas. Any transcript exceeding 999 segments cannot be both schema-valid and ADR-conformant simultaneously.

---

## Affected Documents

| Document | Says |
|----------|------|
| Schema files (segment definitions) | `^seg-\d{3,}$` |
| `docs/adrs/ADR-007-output-template-specification.md` §3.1 | `^seg-\d{3}$` |
| `skills/transcript/agents/ts-formatter.md` example | 3-digit zero-padded form (compatible with both) |

---

## Recommended Resolution

Per audit: **loosen ADR-007 §3.1 from `\d{3}` to `\d{3,}`** to match schemas and preserve forward-compat. Tightening schemas to ADR-007 would regress the 1000+ segment capability, which is undesirable.

---

## Acceptance Criteria

- [ ] ADR-007 §3.1 segment-anchor regex updated from `^seg-\d{3}$` to `^seg-\d{3,}$`.
- [ ] ADR-007 History records the amendment with date, author, and rationale.
- [ ] `ts-formatter.md` example confirms zero-padding to **at least** 3 digits (compatible with `\d{3,}`).
- [ ] FEAT-003 STORY-005 (ANCHOR-* validators) encodes `^seg-\d{3,}$` as the ANCHOR rule.
- [ ] Regression test: a synthetic packet with 1000+ segments passes all anchor validators.
- [ ] FEAT-004 STORY-015 (`discussions[]`) inherits the `\d{3,}` convention for `disc-NNN` regex.

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-002](../FEAT-002-contradictions-cleanup.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | FEAT-001 STORY-001 | ADR-007 must be readable in canonical location to amend |
| Blocks | FEAT-001 STORY-002 | ADR-007 promotion blocked while contradiction remains |
| Blocks | FEAT-003 STORY-005 | ANCHOR-* validators need consistent regex |
| Blocks | FEAT-004 STORY-015 | discussions[] disc-NNN regex inherits this convention |

### Source

- [#273 §C4.4](https://github.com/geekatron/jerry/issues/273)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Bug created from audit finding C4.4. |
