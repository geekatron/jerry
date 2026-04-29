# BUG-005: Backlinks format direct contradiction (ADR-003 vs ADR-007)

> **Type:** bug
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-04-28T00:00:00Z
> **Parent:** FEAT-002
> **Owner:** adam.nowak
> **Effort:** 2

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

**Direct contradiction.** ADR-003 "Backlinks Section Template" (under Implementation, ~line 270) specifies a `## Backlinks` H2 heading. ADR-007 §3.3 explicitly says `<backlinks>` tag (not `## Backlinks` heading). Existing packets use one or the other inconsistently.

---

## Steps to Reproduce

1. Open `docs/adrs/ADR-003-*.md` and locate the "Backlinks Section Template" (Implementation section, ~line 270). Observe it specifies a `## Backlinks` H2 heading.
2. Open `docs/adrs/ADR-007-output-template-specification.md` §3.3. Observe it specifies a `<backlinks>` tag (NOT a `## Backlinks` heading).
3. Inspect existing transcript packets — observe inconsistent application of the two formats.
4. Conclude: ADR-003 and ADR-007 directly contradict each other on the same surface. There is no canonical answer for which format is correct.

---

## Affected Documents

| Document | Says |
|----------|------|
| `docs/adrs/ADR-003-*.md` (Backlinks Section Template, ~line 270) | `## Backlinks` H2 heading |
| `docs/adrs/ADR-007-output-template-specification.md` §3.3 | `<backlinks>` tag |

---

## Recommended Resolution

Per audit: **ADR-007 is newer; pick `<backlinks>` tag and amend ADR-003.** ADR-003 backlinks section gets a "superseded by ADR-007 §3.3" notice or is updated inline.

---

## Acceptance Criteria

- [ ] ADR-003 amended: backlinks section either deleted (with pointer to ADR-007 §3.3) OR updated inline to use `<backlinks>` tag.
- [ ] ADR-003 History records the amendment with date, author, and rationale.
- [ ] ADR-007 §3.3 remains canonical with no contradicting language.
- [ ] All existing packets (including golden test packets in `test_data/`) regenerated to use `<backlinks>` tag where they used `## Backlinks`.
- [ ] FEAT-003 STORY-004 (CONTENT-* validators) encodes `<backlinks>` as the canonical CONTENT rule; rejects packets using `## Backlinks` H2.
- [ ] Migration note: if any external user packets exist with `## Backlinks`, document a one-time migration path.

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-002](../FEAT-002-contradictions-cleanup.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | FEAT-001 STORY-001 | ADR-007 must be readable in canonical location |
| Blocks | FEAT-001 STORY-002 | ADR-007 promotion blocked while contradiction remains |
| Blocks | FEAT-003 STORY-004 | CONTENT-* validators need consistent backlinks format |

### Source

- [#273 §C4.5](https://github.com/geekatron/jerry/issues/273)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Bug created from audit finding C4.5. Direct contradiction between ADR-003 and ADR-007. |
