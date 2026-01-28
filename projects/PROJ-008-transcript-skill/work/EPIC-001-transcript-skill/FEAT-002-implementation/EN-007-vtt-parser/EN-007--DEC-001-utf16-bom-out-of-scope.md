# EN-007:DEC-001: UTF-16 BOM Support Out of Scope

<!--
TEMPLATE: Decision
VERSION: 1.0.0
SOURCE: TASK-107 Documentation Audit
CREATED: 2026-01-27
PURPOSE: Document discrepancy between TDD and agent regarding UTF-16 BOM support
-->

> **Type:** decision
> **Status:** ACCEPTED
> **Priority:** MEDIUM
> **Created:** 2026-01-27T00:00:00Z
> **Parent:** EN-007
> **Owner:** Claude
> **Related:** TDD-ts-parser.md, ts-parser.md, NFR-007

---

## Frontmatter

```yaml
id: "EN-007:DEC-001"
work_type: DECISION
title: "UTF-16 BOM Support Out of Scope"
status: ACCEPTED
priority: MEDIUM
created_by: "Claude"
participants:
  - "Claude"
  - "User"
created_at: "2026-01-27T00:00:00Z"
updated_at: "2026-01-27T00:00:00Z"
decided_at: "2026-01-27T00:00:00Z"
parent_id: "EN-007"
tags: ["encoding", "utf-16", "bom", "scope-reduction"]
decision_count: 1
superseded_by: null
supersedes: null
```

---

## Summary

During TASK-107 (Encoding Fallback Verification) documentation audit, a **discrepancy** was discovered between the Technical Design Document (TDD-ts-parser.md) and the Agent Definition (ts-parser.md) regarding UTF-16 BOM support.

**Decisions Captured:** 1

**Key Outcomes:**
- UTF-16/UTF-16LE BOM support is **out of scope** for MVP
- TDD and Agent will be updated to document this limitation
- Tech debt enabler EN-017 created in FEAT-003 for future UTF-16 support

---

## Decision Context

### Background

During TASK-107 Step 1 (Documentation Audit), the following discrepancy was identified:

**TDD-ts-parser.md (Section 5, lines 365-368):**
```
  BOM found         No BOM
      │                 │
      ▼                 ▼
 ┌─────────┐    ┌───────────────┐
 │ UTF-8   │    │ Try decode as │
 │ UTF-16  │    │ UTF-8         │
 │ UTF-16LE│    └───────┬───────┘
```

**ts-parser.md (Agent Definition, Section 2.5 - Encoding Fallback Chain):**
```
1. UTF-8 with BOM detection (check for BOM marker first)
2. UTF-8 without BOM (try decode)
3. Windows-1252 (common Windows encoding)
4. ISO-8859-1 (Western European)
5. Latin-1 (final fallback - accepts all byte values)
```

**Finding:** The TDD specifies UTF-16 and UTF-16LE BOM detection, but the agent implementation only mentions UTF-8 BOM detection. The agent's encoding fallback chain does NOT include UTF-16.

### Constraints

- **MVP Timeline:** Adding UTF-16 support requires additional implementation and testing effort
- **Market Analysis (EN-001):** 99%+ of transcripts use UTF-8 encoding
- **Effort vs. Value:** UTF-16 is rare in transcript files; VTT/SRT standards primarily use UTF-8
- **WebVTT Specification:** W3C WebVTT recommends UTF-8 encoding

### Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| User | Product Owner | Scope management, MVP delivery |
| Claude | Implementer | Technical accuracy, honest documentation |

---

## Decisions

### D-001: UTF-16 BOM Support Deferred to Tech Debt

**Date:** 2026-01-27
**Participants:** Claude, User

#### Question/Context

During documentation audit, Claude identified the discrepancy and asked:

> "The TDD mentions UTF-16/UTF-16LE in the BOM detection flow diagram (lines 365-368), but the agent definition only mentions UTF-8 BOM. How should we handle this discrepancy?"

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Implement UTF-16 support now | Full TDD compliance | Delays MVP, low ROI (rare format) |
| **B** | Document as known limitation, defer to tech debt | Honest documentation, unblocks MVP | TDD-Agent misalignment until fixed |
| **C** | Remove UTF-16 from TDD entirely | Clean documentation | Loses design intent for future |

#### Decision

**We decided:** Option B - Document UTF-16 BOM support as a known limitation and create a tech debt enabler (EN-017) in FEAT-003 for future implementation.

#### Rationale

1. **Market Reality:** Per EN-001 Market Analysis, UTF-8 is the dominant encoding (99%+) for transcript files
2. **W3C WebVTT Standard:** Explicitly recommends UTF-8 encoding (`WEBVTT` signature is UTF-8)
3. **SRT Standard:** De facto standard uses UTF-8 or Latin-1, not UTF-16
4. **MVP Focus:** UTF-16 adds complexity without significant user benefit
5. **Honest Documentation:** Better to document the limitation than silently ignore it

#### Implications

- **Positive:** Unblocks TASK-107 and MVP delivery
- **Positive:** Honest documentation of current capabilities
- **Negative:** TDD shows capability not yet implemented (until tech debt resolved)
- **Follow-up required:** Create EN-017 in FEAT-003 for UTF-16 tech debt

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-001 | UTF-16 BOM support deferred to tech debt (EN-017) | 2026-01-27 | ACCEPTED |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [EN-007-vtt-parser.md](./EN-007-vtt-parser.md) | Parent enabler |
| TDD | [TDD-ts-parser.md](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-parser.md) | Technical design (contains UTF-16 mention) |
| Agent | [ts-parser.md](../../../../../skills/transcript/agents/ts-parser.md) | Agent definition (UTF-8 only) |
| Tech Debt | [EN-017](../../FEAT-003-future-enhancements/EN-017-utf16-support/EN-017-utf16-support.md) | Future UTF-16 implementation |
| Task | [TASK-107](./TASK-107-encoding-fallback-verification.md) | Source of discovery |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-27 | Claude | Created decision document per TASK-107 documentation audit |

---

## Metadata

```yaml
id: "EN-007:DEC-001"
parent_id: "EN-007"
work_type: DECISION
title: "UTF-16 BOM Support Out of Scope"
status: ACCEPTED
priority: MEDIUM
created_by: "Claude"
created_at: "2026-01-27T00:00:00Z"
updated_at: "2026-01-27T00:00:00Z"
decided_at: "2026-01-27T00:00:00Z"
participants: ["Claude", "User"]
tags: ["encoding", "utf-16", "bom", "scope-reduction"]
decision_count: 1
superseded_by: null
supersedes: null
```
