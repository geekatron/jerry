# FEAT-005: Mindmap Hardening

<!--
TEMPLATE: Feature
PURPOSE: Fix two distinct defects in ts-mindmap-mermaid surfaced by external audit. EARLY-LAND quick-win Feature per user direction.
-->

> **Type:** feature
> **Status:** pending
> **Priority:** high
> **Impact:** medium
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
| [Children Stories/Enablers](#children-storiesenablers) | Bug inventory (Bugs are children of this Feature) |
| [Acceptance Criteria](#acceptance-criteria) | Feature-level acceptance |
| [Progress Summary](#progress-summary) | Overall progress |
| [Dependencies](#dependencies) | Inputs and downstream blocks |
| [Related Items](#related-items) | Hierarchy and references |
| [Quick-Win Note](#quick-win-note) | Why this lands early |
| [History](#history) | Status changes |

---

## Summary

The audit surfaced two distinct concerns in `ts-mindmap-mermaid`:

| Bug | Concern | Severity |
|-----|---------|----------|
| BUG-006 | Agent produces non-rendering Mermaid when node labels contain bracketed canonical forms (`RFP [RDP]`, `cloud MQP [AMQP]`, etc.). The Mermaid mindmap parser interprets `[...]` as a shape construct, not literal text. Tested fix: HTML-entity escape `&#91;`/`&#93;`. | Major when packets use the convention; Minor otherwise. **Recurrence: structural** — any future packet using bracketed canonical forms hits this. |
| BUG-007 | Agent self-reports `"Mermaid syntax: Valid"` based on textual inspection of its own output, without actually rendering. The agent has only `Read, Write, Glob` tools per its definition — it cannot render. The claim misleads callers. | Minor (process integrity); aggravates BUG-006 by hiding the failure surface. |

These are independent of FEAT-001..FEAT-004 (no governance, schema, or validator dependencies). They land **early** as quick-wins per user direction: *"I want it landed early. I want us to stop generating garbage — our outputs need to be validated automatically. This should be deterministic."*

---

## Children Stories/Enablers

This Feature's children are Bugs.

| ID | Type | Title | Status | Severity |
|----|------|-------|--------|----------|
| BUG-006 | Bug | ts-mindmap-mermaid bracket-escaping fails parse | pending | major |
| BUG-007 | Bug | ts-mindmap-mermaid false self-claim of syntax validity | pending | minor |

### Work Item Links

- [BUG-006: Bracket escaping](./BUG-006-mindmap-bracket-escape/BUG-006-mindmap-bracket-escape.md)
- [BUG-007: False self-claim](./BUG-007-mindmap-false-self-claim/BUG-007-mindmap-false-self-claim.md)

---

## Progress Summary

```
Bugs:    [....................]  0% (0/2 resolved)
Overall: [....................]  0%
```

---

## Acceptance Criteria

- [ ] BUG-006: `ts-mindmap-mermaid` agent prompt updated to HTML-entity-escape `[`/`]` (and defensively `(`/`)`/`{`/`}`) at write time.
- [ ] BUG-006: Regression test — packet with bracketed canonical labels renders cleanly via `mmdc` (or chosen render adapter); local fix verified before merge.
- [ ] BUG-007: Either (a) grant `ts-mindmap-mermaid` render capability via `Bash + mmdc` and have it actually verify, OR (b) weaken the claim to "syntactic shape conforms to Mermaid mindmap directive structure" so the return summary is scope-honest. Decision recorded in BUG-007.
- [ ] Both fixes tested against the original audit packet (which exercised the failure mode).
- [ ] No regression in non-bracketed-label packets.

---

## Dependencies

| Type | Item | Description |
|------|------|-------------|
| Independent | — | Can land in parallel with FEAT-001 once branch is set up |
| Cooperates | FEAT-003 | Once validators exist, add a SCHEMA-or-CONTENT rule that detects unescaped brackets in Mermaid output |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001](../EPIC-001-transcript-hardening.md)

### External

- Source: [#273 comment 3](https://github.com/geekatron/jerry/issues/273#issuecomment-4339778594)

---

## Quick-Win Note

User direction: this Feature lands **early**. Both Bugs are scoped tightly enough to ship as a single PR (single-agent prompt fix + capability decision) without waiting for FEAT-001..FEAT-004. Treat as Phase-3 quick-win in the orchestration plan.

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Feature created. 2 Bugs scaffolded. Designated as early-land quick-win per user direction. |
