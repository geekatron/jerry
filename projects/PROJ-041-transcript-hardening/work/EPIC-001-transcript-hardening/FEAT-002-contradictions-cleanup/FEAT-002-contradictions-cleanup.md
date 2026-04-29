# FEAT-002: Framework-Internal Contradictions Cleanup

<!--
TEMPLATE: Feature
PURPOSE: Resolve 5 framework-internal contradictions across ADR-002/003/004/006/007 + schemas before ADR-007 is baselined
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
| [Children Stories/Enablers](#children-storiesenablers) | Bug inventory (Bugs are tracked as children of this Feature) |
| [Acceptance Criteria](#acceptance-criteria) | Feature-level acceptance |
| [Progress Summary](#progress-summary) | Overall progress |
| [Dependencies](#dependencies) | Inputs and downstream blocks |
| [Related Items](#related-items) | Hierarchy and references |
| [History](#history) | Status changes |

---

## Summary

The audit identified five direct or partial contradictions across `/transcript` framework documents (ADRs and schemas). These must be resolved as a precondition for ADR-007 baselining (FEAT-001 STORY-002). Each contradiction is filed as its own Bug with a stated recommended resolution from the audit. Each Bug must close with the resolution recorded in the affected document(s) and no remaining cross-document disagreement on that item.

| Bug | Disagreement Surface | Recommended Resolution |
|-----|---------------------|------------------------|
| BUG-001 | Per-file token caps for `00-index.md` / `01-summary.md`: ts-formatter + ADR-007 §1.1 say 2K/5K; SKILL.md L2665-L2666 says 5K/8K (in validator-thresholds context) | Clarify disambiguation: 2K/5K is authoring budget, 5K/8K is post-completion validator soft-cap. Label both explicitly. If unintended divergence, converge on 2K/5K. |
| BUG-002 | `chunk_id` regex: `extraction-report.json` schema `^chunk-\d{3,}$` vs `chunk.schema.json` `^chunk-\d{3}$` vs `index.schema.json` `^chunk-\d{3}$` | Converge on `^chunk-\d{3,}$` (forward-compat past 999 chunks). |
| BUG-003 | `domain` regex: `contexts/schemas/domain-schema.json` vs `schemas/context-domain-schema.json` vs `schemas/DOMAIN-SCHEMA.json` (closed-list enum) | Pick closed-list `DOMAIN-SCHEMA.json` (enum-based, stronger validation). |
| BUG-004 | Segment-anchor regex: schemas use `^seg-\d{3,}$`; ADR-007 §3.1 says `^seg-\d{3}$`; ts-formatter example uses 3-digit zero-padded form | **Loosen ADR-007 §3.1 to `\d{3,}`** to match schemas (preserves forward-compat past 999 segments). |
| BUG-005 | Backlinks format **direct contradiction**: ADR-003 "Backlinks Section Template" specifies `## Backlinks` H2 heading; ADR-007 §3.3 specifies `<backlinks>` tag | ADR-007 is newer; recommend `<backlinks>` tag and amend ADR-003. |

---

## Children Stories/Enablers

This Feature's children are Bugs (per worktracker entity hierarchy: Features may contain Bugs alongside Stories/Enablers when the Feature scope is bug-cleanup).

| ID | Type | Title | Status | Severity |
|----|------|-------|--------|----------|
| BUG-001 | Bug | Token caps disambiguation: 2K/5K vs 5K/8K | pending | minor |
| BUG-002 | Bug | chunk_id regex divergence (3 schemas) | pending | major |
| BUG-003 | Bug | domain regex: 3 disagreeing schemas | pending | major |
| BUG-004 | Bug | seg-NNN regex: ADR-007 \d{3} vs schemas \d{3,} | pending | major |
| BUG-005 | Bug | Backlinks format direct contradiction (ADR-003 vs ADR-007) | pending | major |

### Work Item Links

- [BUG-001: Token caps disambiguation](./BUG-001-token-caps/BUG-001-token-caps.md)
- [BUG-002: chunk_id regex divergence](./BUG-002-chunk-id-regex/BUG-002-chunk-id-regex.md)
- [BUG-003: domain regex schemas disagree](./BUG-003-domain-regex/BUG-003-domain-regex.md)
- [BUG-004: seg-NNN regex contradiction](./BUG-004-seg-nnn-regex/BUG-004-seg-nnn-regex.md)
- [BUG-005: Backlinks format contradiction](./BUG-005-backlinks-format/BUG-005-backlinks-format.md)

---

## Progress Summary

```
Bugs:    [....................]  0% (0/5 resolved)
Overall: [....................]  0%
```

---

## Acceptance Criteria

- [ ] All 5 Bugs closed with resolution recorded in the affected document(s).
- [ ] No remaining cross-document disagreement on the 5 items (verified by grep across schemas + ADRs + SKILL.md + agents).
- [ ] Where ADR amendments are required (BUG-004, BUG-005), the source ADR's History records the change.
- [ ] BUG-003 (domain regex) deletes the two losing schemas and updates references to point to `DOMAIN-SCHEMA.json`.
- [ ] CI test added: regex/string consistency check across schemas + ADRs + agent definitions for the 5 affected fields.

---

## Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocks | FEAT-001 STORY-002 | ADR-007 promotion to ACCEPTED requires no contradictions to inherit |
| Blocks | FEAT-003 | Validators implementing rules that contradict each other are incoherent |
| Blocked By | FEAT-001 STORY-001 | ADR-007 must be readable in the new docs/adrs/ location before BUG-004/BUG-005 amendments |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001](../EPIC-001-transcript-hardening.md)

### External

- Source: [#273 §C4](https://github.com/geekatron/jerry/issues/273) (5 sub-conflicts table)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Feature created. 5 Bugs scaffolded with recommended resolutions from audit. |
