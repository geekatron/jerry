# FEAT-002:DEC-002: Jerry Returns JSON, Not Rendered Output

> **Type:** decision
> **Status:** accepted
> **Priority:** high
> **Created:** 2026-02-21
> **Completed:** 2026-02-21
> **Parent:** FEAT-002
> **Owner:** --
> **Related:** DEC-003, DEC-004

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Decision overview |
| [Decision Context](#decision-context) | Background and constraints |
| [Decision](#decision) | Choice made and rationale |
| [Decision Summary](#decision-summary) | Quick reference |
| [Related Artifacts](#related-artifacts) | Traceability |
| [Document History](#document-history) | Change log |

---

## Summary

Jerry's `context_monitoring` bounded context provides structured context data (JSON). Jerry does NOT own rendering. Consumers (jerry-statusline, other tools) render independently using the structured data.

---

## Decision Context

### Background

When designing `jerry context estimate`, two options existed: (A) Jerry renders a human-readable status line segment string, or (B) Jerry returns structured JSON and consumers render. Option A would couple Jerry's domain logic to a specific presentation format. Option B keeps the boundary clean.

### Constraints

- jerry-statusline has its own tmux/terminal rendering pipeline
- Different consumers may need different presentation formats
- Domain changes (new tier, new field) should not require changes in consumers if the JSON schema is additive

---

## Decision

**We decided:** Jerry provides structured context data (JSON). Jerry does NOT render status line output. Consumers receive the full JSON response and render independently.

**Rationale:** Clean architecture boundary. Domain provides data; consumers render. This allows multiple consumers with different rendering needs (tmux, terminal, web) without coupling Jerry to any one format. Schema changes are additive; consumers access fields by name.

**Implication:** `jerry context estimate` JSON schema is a stable API surface. Additive changes are safe. Removing or renaming fields is a breaking change.

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-002 | Jerry returns JSON, not rendered output. Consumers own rendering. | 2026-02-21 | Accepted |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-002](./FEAT-002-status-line-unification.md) | Parent feature |
| Related | [DEC-003](./DEC-003-multi-hook-rotation.md) | Multi-hook rotation architecture |
| Related | [DEC-004](./DEC-004-sub-agent-tracking.md) | Sub-agent tracking approach |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-21 | Claude | Created. JSON-not-rendering boundary decision accepted. |

---

## Metadata

```yaml
id: "FEAT-002:DEC-002"
parent_id: "FEAT-002"
work_type: DECISION
title: "Jerry Returns JSON, Not Rendered Output"
status: ACCEPTED
priority: HIGH
created_by: "Claude"
created_at: "2026-02-21"
decided_at: "2026-02-21"
```
