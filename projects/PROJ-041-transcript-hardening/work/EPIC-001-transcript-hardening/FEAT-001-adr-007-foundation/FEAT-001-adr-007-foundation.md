# FEAT-001: ADR-007 Foundation & Governance

<!--
TEMPLATE: Feature
PURPOSE: Make ADR-007 governance-ready (vendored to public docs/adrs/, status promoted) so it can be a baselined source of truth for /transcript
-->

> **Type:** feature
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-04-28T00:00:00Z
> **Due:**
> **Completed:**
> **Parent:** EPIC-001
> **Owner:** adam.nowak

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this Feature delivers |
| [Children Stories/Enablers](#children-storiesenablers) | Story inventory |
| [Acceptance Criteria](#acceptance-criteria) | Feature-level acceptance |
| [Progress Summary](#progress-summary) | Overall progress |
| [Dependencies](#dependencies) | Inputs and downstream blocks |
| [Related Items](#related-items) | Hierarchy and references |
| [History](#history) | Status changes |

---

## Summary

`/transcript` SKILL.md and its agents (`ts-formatter.md`, `PLAYBOOK.md`, `ts-formatter.prompt.md`) reference ADR-007 "Output Template Specification" as authoritative for model-agnostic output rules (MUST-USE / MUST-NOT-CREATE tables, anchor format, citation format). But:

1. The ADR lives in a separate jerry-core repository under its transcript-skill project's `FEAT-006-output-consistency/docs/decisions/` directory — it does not ship in the public release. The public release packages ADR-001..ADR-006 in `docs/adrs/`. ADR-007 is missing.
2. ADR-007's frontmatter says `Status: PROPOSED` while SKILL.md, ts-formatter.md, and ADR-007 §4 itself reference its rules as MUST-USE and define validation gates. "MUST follow this PROPOSED ADR" is incoherent across all transcript packets.

This Feature closes both gaps. Stories must execute in order: STORY-001 (vendoring) before STORY-002 (status promotion), and FEAT-002 (contradictions cleanup) must complete before STORY-002 promotes to ACCEPTED.

---

## Children Stories/Enablers

| ID | Type | Title | Status | Priority |
|----|------|-------|--------|----------|
| STORY-001 | Story | Vendor ADR-007 from jerry-core to public docs/adrs/ | pending | high |
| STORY-002 | Story | Promote ADR-007 status PROPOSED → ACCEPTED | pending | high |

### Work Item Links

- [STORY-001: Vendor ADR-007 to docs/adrs/](./STORY-001-vendor-adr-007/STORY-001-vendor-adr-007.md)
- [STORY-002: Promote ADR-007 to ACCEPTED](./STORY-002-promote-adr-007-accepted/STORY-002-promote-adr-007-accepted.md)

---

## Progress Summary

```
Stories:  [....................]  0% (0/2 completed)
Overall:  [....................]  0%
```

---

## Acceptance Criteria

- [ ] `docs/adrs/ADR-007-output-template-specification.md` exists at HEAD on `feat/PROJ-041-transcript-hardening`.
- [ ] All references to ADR-007 in SKILL.md, ts-formatter.md, PLAYBOOK.md, ts-formatter.prompt.md use the new `docs/adrs/` path (no remaining old jerry-core project paths).
- [ ] ADR-007 frontmatter shows `Status: ACCEPTED`.
- [ ] All 5 contradictions in FEAT-002 are resolved before status promotion (enforced by STORY-002 acceptance criteria).
- [ ] Suggested automated check in CI: every SKILL.md cross-reference resolves in the public release.

---

## Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocks | FEAT-003 | Validators implementing PROPOSED ADR is incoherent — promotion to ACCEPTED unblocks F3 acceptance |
| Blocks | EN-008 | Final adversary tournament cannot pass while governance is incoherent |
| Blocked By | FEAT-002 | STORY-002 (promotion) requires all 5 contradictions resolved |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001](../EPIC-001-transcript-hardening.md)

### External

- Source: [#273 §C1, §C2](https://github.com/geekatron/jerry/issues/273)
- ADR-007 source: separate jerry-core repository, under its transcript-skill project's `FEAT-006-output-consistency/docs/decisions/` directory. Implementer resolves exact path against the local jerry-core checkout.

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Feature created. Stories scaffolded. Awaiting execution. |
