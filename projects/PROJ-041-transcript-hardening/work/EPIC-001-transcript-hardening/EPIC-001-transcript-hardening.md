# EPIC-001: `/transcript` Skill Hardening from External Packet Audit

<!--
TEMPLATE: Epic
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.2
PURPOSE: Top-level container for all hardening work driven by issue #273 audit findings
-->

> **Type:** epic
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-04-28T00:00:00Z
> **Due:**
> **Completed:**
> **Parent:** PROJ-041
> **Owner:** adam.nowak

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this Epic covers |
| [Business Outcome Hypothesis](#business-outcome-hypothesis) | Expected outcome |
| [Children Features/Capabilities](#children-featurescapabilities) | Decomposition |
| [Progress Summary](#progress-summary) | Overall progress |
| [Acceptance Criteria](#acceptance-criteria) | Epic-level acceptance |
| [Related Items](#related-items) | Hierarchy and external links |
| [History](#history) | Status changes |

---

## Summary

Harden the `/transcript` skill so its output is **deterministically validated** at every write — no LLM-judged spec compliance, no declared counts that drift silently from walked truth. Driven by an external audit (issue #273) where 9 iterations of `/adversary` C4 review on a real packet plateaued at composite 0.900 (below 0.95 target). Each fix wave introduced small new defects in the same surface because the framework had no mechanically enforceable validators for the rules ADR-007 §4 already specifies.

This Epic delivers (1) governance closure for ADR-007, (2) resolution of 5 framework-internal contradictions, (3) implementation of all 17 ADR-007 §4 rule IDs as runnable validators wired into the `ts-formatter` write pipeline, (4) four schema extensions, and (5) two mindmap rendering bug fixes. All work is gated by `/adversary` C4 ≥0.95 between phases and a final tournament at acceptance.

---

## Business Outcome Hypothesis

**For** Jerry framework users who run `/transcript` against real meeting recordings,
**who currently** receive packets that pass LLM-judged review but contain machine-detectable substrate drift (declared counts not matching walked grep results, ASR convention inconsistencies, schema gaps),
**this Epic** delivers automated deterministic validation at every write,
**unlike** the current LLM-judged review that catches issues 30 minutes later and at composite ceilings of 0.90,
**so that** transcript packets are trustworthy out of the box, `/adversary` reviews focus on substantive content quality rather than mechanical defects, and downstream consumers (knowledge graphs, search indexes, audits) operate on substrate that is machine-derived rather than hand-attested.

---

## Children Features/Capabilities

| ID | Type | Title | Status | Priority |
|----|------|-------|--------|----------|
| FEAT-001 | Feature | ADR-007 Foundation & Governance | pending | high |
| FEAT-002 | Feature | Framework-Internal Contradictions Cleanup | pending | high |
| FEAT-003 | Feature | Deterministic Substrate Validation | pending | high |
| FEAT-004 | Feature | Schema Extensions | pending | medium |
| FEAT-005 | Feature | Mindmap Hardening | pending | high |
| EN-004 | Enabler | `/red-team` threat model on entire `/transcript` skill | pending | high |
| EN-005 | Enabler | `/user-experience` JTBD + feedback exploration | pending | medium |
| EN-006 | Enabler | `/diataxis` documentation pass | pending | medium |
| EN-008 | Enabler | Final `/adversary` C4 tournament | pending | high |

### Work Item Links

- [FEAT-001: ADR-007 Foundation & Governance](./FEAT-001-adr-007-foundation/FEAT-001-adr-007-foundation.md)
- [FEAT-002: Framework-Internal Contradictions Cleanup](./FEAT-002-contradictions-cleanup/FEAT-002-contradictions-cleanup.md)
- [FEAT-003: Deterministic Substrate Validation](./FEAT-003-deterministic-validation/FEAT-003-deterministic-validation.md)
- [FEAT-004: Schema Extensions](./FEAT-004-schema-extensions/FEAT-004-schema-extensions.md)
- [FEAT-005: Mindmap Hardening](./FEAT-005-mindmap-hardening/FEAT-005-mindmap-hardening.md)
- [EN-004: /red-team threat model](./EN-004-red-team-threat-model/EN-004-red-team-threat-model.md)
- [EN-005: /user-experience JTBD + feedback](./EN-005-user-experience-exploration/EN-005-user-experience-exploration.md)
- [EN-006: /diataxis documentation pass](./EN-006-diataxis-docs/EN-006-diataxis-docs.md)
- [EN-008: Final /adversary C4 tournament](./EN-008-final-adversary-tournament/EN-008-final-adversary-tournament.md)

---

## Progress Summary

```
+------------------------------------------------------------------+
|                   EPIC PROGRESS TRACKER                           |
+------------------------------------------------------------------+
| Features:  [....................]  0% (0/5 completed)             |
| Enablers:  [....................]  0% (0/4 cross-cutting)         |
| Bugs:      [....................]  0% (0/7 — F2: 5, F5: 2)        |
| Stories:   [....................]  0% (0/16 across F1, F3, F4)    |
+------------------------------------------------------------------+
| Overall:   [....................]  0%                              |
+------------------------------------------------------------------+
```

Total entity count: 1 Epic + 5 Features + 4 cross-cutting Enablers + 3 in-feature Enablers + 16 Stories + 7 Bugs = **36 work items**.

---

## Acceptance Criteria

The Epic closes only when ALL of the following hold:

- [ ] All 5 Features completed with delivery evidence in their History sections.
- [ ] All 5 cross-cutting Enablers completed with deliverables (threat model report, UX findings, documentation set, orchestration plan, final tournament report).
- [ ] All 7 Bugs verified fixed with regression tests in CI.
- [ ] All 16 Stories closed with concrete evidence (commits, validator runs, adversary scores).
- [ ] Final `/adversary` C4 tournament against the merged Epic deliverable scores ≥0.95 weighted composite (S-014 LLM-as-Judge with 6-dimension rubric).
- [ ] `/eng-team` `eng-reviewer` final-gate review passes (architecture compliance, security standards, test coverage).
- [ ] CI gate: validators run against golden packets in `test_data/` on every PR.
- [ ] `ts-formatter` post-render hook executes `verify` before reporting completion.
- [ ] `update-anchors` is wired into `ts-formatter` write pipeline; declared counts are now a cache of walked truth.
- [ ] No remaining cross-document disagreement on canonical `/transcript` rules.
- [ ] ADR-007 status is `ACCEPTED` and lives at `docs/adrs/ADR-007-output-template-specification.md`.
- [ ] Issue #273 closed with comment linking to this Epic's completion summary.

---

## Related Items

### Hierarchy

- **Parent Project:** [PROJ-041: transcript hardening](../../PLAN.md)

### External

- **GitHub Issue:** [#273](https://github.com/geekatron/jerry/issues/273) — meta tracker for the 5 audit findings + 3 comment findings.
- **Author's prototype CLI:** [public gist](https://gist.github.com/anowak-delinea/f6748192a6e32bb65c874cd0e5dde924) — reference, not literal port.

### Related

- ADR-007 source location (jerry-core): the canonical ADR lives in a separate jerry-core repository under its transcript-skill project's `FEAT-006-output-consistency/docs/decisions/` directory. STORY-001 implementer resolves exact path against the local jerry-core checkout.
- `/transcript` skill: `skills/transcript/SKILL.md`
- Quality SSOT: `.context/rules/quality-enforcement.md`

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Epic created from #273 audit findings. 5 Features + 5 cross-cutting Enablers scaffolded. |
| 2026-04-29 | adam.nowak (via Claude) | pending | EN-007 (`/orchestration` plan) removed — `/orchestration` skill identified as overkill. Execution order handled by worktracker dependency chain. Cross-cutting enablers count: 4 (was 5). |
