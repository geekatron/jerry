# EN-006: `/diataxis` documentation pass

> **Type:** enabler
> **Enabler Type:** infrastructure
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-04-28T00:00:00Z
> **Parent:** EPIC-001
> **Owner:** adam.nowak
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this Enabler delivers |
| [Technical Approach](#technical-approach) | /diataxis four-quadrant approach |
| [Documentation Plan](#documentation-plan) | Per-quadrant deliverables |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Change log |

---

## Summary

After FEAT-001..FEAT-005 land, write the documentation set using `/diataxis` four-quadrant methodology. Each new capability (validators, CLI subcommands, schema extensions, hook integrations) gets the right quadrant of doc — no quadrant mixing, no orphan capabilities.

This Enabler runs in Phase 7 (after implementation, before final adversary tournament).

---

## Technical Approach

Apply `/diataxis` four-quadrant methodology: every doc fits exactly one of {Tutorial, How-to, Reference, Explanation}. `diataxis-classifier` validates each doc's claimed quadrant; `diataxis-auditor` finds zero quadrant mixing across the doc set. Each writer agent (`diataxis-tutorial`, `diataxis-howto`, `diataxis-reference`, `diataxis-explanation`) produces its quadrant; cross-references use repo-relative paths per H-23. Doc set surfaces from `skills/transcript/SKILL.md` References section.

---

## Documentation Plan

| Quadrant | Audience | Topic | Writer Agent | Output Location |
|----------|----------|-------|--------------|-----------------|
| **Tutorial** (learning by doing) | New `/transcript` user | "Run your first transcript validation" — guided walkthrough from raw VTT to validated packet | `diataxis-tutorial` | `docs/transcript/tutorials/first-validation.md` |
| **How-to guide** (goal-oriented) | Practitioner with packet drift | "How to detect and repair declared-derived drift in a transcript packet" | `diataxis-howto` | `docs/transcript/how-to/repair-drift.md` |
| **How-to guide** (goal-oriented) | Practitioner integrating CI | "How to gate PRs on transcript validator results" | `diataxis-howto` | `docs/transcript/how-to/ci-integration.md` |
| **Reference** (information-oriented) | Developer / agent author | "Catalog of all 17 ADR-007 §4 validation rules" — rule_id, pre-conditions, evidence shape, severity | `diataxis-reference` | `docs/transcript/reference/validation-rules.md` |
| **Reference** | Developer / agent author | "CLI: `jerry transcript verify` and `update-anchors`" — exhaustive command reference | `diataxis-reference` | `docs/transcript/reference/cli.md` |
| **Reference** | Schema consumer | "extraction-report.json schema v1.2" — including new editorial_conventions, arithmetic_invariants, discussions[], audit_basis fields | `diataxis-reference` | `docs/transcript/reference/extraction-report-schema.md` |
| **Explanation** (understanding-oriented) | Curious reader / contributor | "Why declared substrate is mechanically derived, not hand-attested" — design rationale connecting audit findings to validator architecture | `diataxis-explanation` | `docs/transcript/explanation/substrate-coupling.md` |
| **Explanation** | Curious reader / contributor | "Why `/transcript` validation is an operation within the bounded context, not a separate BC" — DDD framing rationale | `diataxis-explanation` | `docs/transcript/explanation/bounded-context.md` |

---

## Acceptance Criteria

- [ ] All 8 docs written with `/diataxis` writer agents.
- [ ] `diataxis-classifier` confirms each doc fits its claimed quadrant.
- [ ] `diataxis-auditor` finds zero quadrant mixing across the doc set.
- [ ] All ADR-007 §4 rule IDs documented in the reference catalog with correct evidence shapes.
- [ ] Tutorial validated by following it end-to-end on a fresh checkout.
- [ ] Cross-references between docs use proper repo-relative paths (NAV-001 / H-23).
- [ ] Documentation set surfaced from `skills/transcript/SKILL.md` "References" section.
- [ ] `/eng-team` `eng-reviewer` confirms documentation matches implementation reality.
- [ ] `/adversary` C4 ≥0.95 review on the doc set.

---

## Children Tasks

| ID | Title | Status |
|----|-------|--------|
| TASK-001 | diataxis-tutorial: first-validation tutorial | pending |
| TASK-002 | diataxis-howto: repair-drift how-to | pending |
| TASK-003 | diataxis-howto: ci-integration how-to | pending |
| TASK-004 | diataxis-reference: validation rules catalog | pending |
| TASK-005 | diataxis-reference: CLI reference | pending |
| TASK-006 | diataxis-reference: schema reference | pending |
| TASK-007 | diataxis-explanation: substrate coupling | pending |
| TASK-008 | diataxis-explanation: bounded context | pending |
| TASK-009 | Run diataxis-classifier on each doc | pending |
| TASK-010 | Run diataxis-auditor on full doc set | pending |
| TASK-011 | Update SKILL.md References section | pending |
| TASK-012 | Run /adversary C4 review | pending |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001](../EPIC-001-transcript-hardening.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | FEAT-001..FEAT-005 | Documentation describes shipped capabilities; cannot precede implementation |
| Blocks | EN-008 | Final tournament expects complete documentation |

### Source

- Standard /diataxis post-build documentation pattern

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Cross-cutting Enabler created. 8 docs across 4 quadrants planned. |
