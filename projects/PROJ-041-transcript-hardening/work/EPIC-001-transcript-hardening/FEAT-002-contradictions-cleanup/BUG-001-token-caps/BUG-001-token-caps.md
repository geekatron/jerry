# BUG-001: Token caps disambiguation: 2K/5K (authoring) vs 5K/8K (validator)

> **Type:** bug
> **Status:** pending
> **Priority:** high
> **Impact:** medium
> **Severity:** minor
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

`agents/ts-formatter.md` and ADR-007 §1.1 both specify per-file token caps for `00-index.md` and `01-summary.md` as **2K / 5K**. SKILL.md L2665-L2666 specifies **5K / 8K** — but in a section about post-completion validator thresholds, not authoring budgets. This is likely an unintended-divergence-OR-undocumented-disambiguation problem.

---

## Steps to Reproduce

1. Open `skills/transcript/agents/ts-formatter.md` and locate per-file token cap declarations for `00-index.md` / `01-summary.md`.
2. Open `docs/adrs/ADR-007-output-template-specification.md` §1.1 and locate the same declarations.
3. Observe both say **2K / 5K**.
4. Open `skills/transcript/SKILL.md` lines 2665-2666 and observe **5K / 8K** in a section about validator thresholds.
5. Conclude: it is unclear whether the 5K/8K is intentionally a different value (validator soft-cap vs authoring budget) or an unintended divergence — neither side is labeled to disambiguate.

---

## Affected Documents

| Document | Says | Context |
|----------|------|---------|
| `skills/transcript/agents/ts-formatter.md` | 2K / 5K | Authoring budget |
| `docs/adrs/ADR-007-output-template-specification.md` §1.1 | 2K / 5K | Authoring budget |
| `skills/transcript/SKILL.md` L2665-L2666 | 5K / 8K | Validator threshold context (likely) |

---

## Recommended Resolution

Per audit: **clarify the disambiguation**. If 2K/5K is the authoring budget (input to ts-formatter) and 5K/8K is the validator soft-cap (post-completion check), label both clearly. If unintended divergence, converge on 2K/5K everywhere.

Recommended path: confirm intent with author/maintainer of SKILL.md L2665-L2666; if disambiguation is intended, label both sides ("authoring budget: 2K/5K", "validator soft-cap: 5K/8K") and add a cross-reference. If unintended, converge on 2K/5K.

---

## Acceptance Criteria

- [ ] Decision recorded in ADR-007 amendment or SKILL.md (which side is canonical, if both, why and how they differ).
- [ ] If labels added: SKILL.md L2665-L2666 explicitly says "validator soft-cap" or equivalent disambiguation language.
- [ ] If converged: only 2K/5K appears across all four references; SKILL.md updated.
- [ ] FEAT-003 STORY-003 (FILE-* validators) encodes the resolved values as test expectations.
- [ ] Regression check: `grep -rE '(2,?000|5,?000|2K|5K|8K)' skills/transcript/` shows only labeled references.

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-002](../FEAT-002-contradictions-cleanup.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | FEAT-001 STORY-001 | ADR-007 must be in canonical location to amend |
| Blocks | FEAT-001 STORY-002 | Promotion to ACCEPTED requires this resolved |

### Source

- [#273 §C4.1](https://github.com/geekatron/jerry/issues/273)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Bug created from audit finding C4.1. |
