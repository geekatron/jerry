# DEC-001: Create PROJ-002 for Future-Facing R&D

> **Type:** decision
> **Status:** accepted
> **Priority:** medium
> **Impact:** strategic
> **Created:** 2026-02-17
> **Owner:** Adam Nowak

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Context](#context) | Why this decision was needed |
| [Decision](#decision) | What was decided |
| [Alternatives](#alternatives) | Options considered |
| [Consequences](#consequences) | Impact of this decision |

---

## Context

PROJ-001 (OSS Release) is nearing completion with EPICs 001-003 done and only bug fixes remaining. EPIC-004 (Advanced Adversarial Capabilities) was created as a deferred, future-facing epic within PROJ-001 but doesn't align with the OSS release scope. Future discoveries and research-heavy features need a dedicated home.

## Decision

Create PROJ-002-roadmap-next as a dedicated project for future-facing R&D. Migrate EPIC-004 from PROJ-001 to PROJ-002. Future discoveries from any project can feed into PROJ-002 as new EPICs.

## Alternatives

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| **New PROJ-002** (chosen) | Clean separation, PROJ-001 can close cleanly, dedicated planning space | Migration overhead | Selected |
| Keep in PROJ-001 | No migration needed | Muddies scope, prevents clean closure | Rejected |
| Lightweight backlog | Low ceremony | Loses hierarchy and tracking benefits | Rejected |

## Consequences

- PROJ-001 can be closed once remaining bugs are resolved
- EPIC-004 retains its full work decomposition (FEAT-007, EN-601-605)
- Future research items have a proper home with worktracker support
- Cross-project references maintained for traceability
