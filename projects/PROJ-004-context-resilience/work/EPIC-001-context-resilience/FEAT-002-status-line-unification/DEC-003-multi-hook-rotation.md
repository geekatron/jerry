# FEAT-002:DEC-003: Multi-Hook Rotation Architecture

> **Type:** decision
> **Status:** accepted
> **Priority:** high
> **Created:** 2026-02-21
> **Completed:** 2026-02-21
> **Parent:** FEAT-002
> **Owner:** --
> **Related:** DEC-002, DEC-004

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

Hooks cannot trigger /compact directly. Automatic session rotation is orchestrated via: `UserPromptSubmit` escalation messages → `Stop` hook gate → `PreCompact` state checkpoint → `SessionStart` resumption context injection. The only manual step is the user pressing Enter to run /compact or /clear.

---

## Decision Context

### Background

The original FEAT-001 design assumed a single hook could trigger session rotation. Claude Code's hook API does not support invoking /compact programmatically from within a hook. Rotation must be orchestrated across the hook lifecycle.

### Constraints

- Hooks cannot invoke Claude Code commands (/compact, /clear)
- Hook events fire at defined lifecycle points (prompt submit, stop, pre-compact, session start)
- Hooks can inject messages into `additionalContext` (UserPromptSubmit, SessionStart)
- Stop hook can block Claude from stopping (`decision: block`)
- PreCompact hook fires before compaction, cannot prevent it

---

## Decision

**We decided:** Multi-hook orchestration across 4 hook types implements graduated session rotation:
1. `UserPromptSubmit` — inject escalation notices at WARNING/CRITICAL tiers
2. `Stop` hook — block stop at EMERGENCY, prompt user to /compact first
3. `PreCompact` — checkpoint state before compaction fires
4. `SessionStart` — detect compaction vs /clear, inject resumption context

**Rationale:** This is the only viable architecture given Claude Code's hook API constraints. Each hook handles the rotation aspect it can control. The user's manual /compact or /clear is the bridge between hook layers.

**Implication:** Full rotation cycle requires user action at EMERGENCY tier. This is a constraint of the Claude Code API, not a design limitation.

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-003 | Multi-hook rotation via UserPromptSubmit + Stop + PreCompact + SessionStart hooks | 2026-02-21 | Accepted |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-002](./FEAT-002-status-line-unification.md) | Parent feature |
| Related | [ST-006](./ST-006-automatic-session-rotation.md) | Rotation story implementing this decision |
| Related | [EN-014](./EN-014-stop-hook-gate.md) | Stop hook gate |
| Related | [EN-015](./EN-015-pre-compact-checkpoint.md) | PreCompact checkpoint |
| Related | [EN-016](./EN-016-session-start-resumption.md) | SessionStart resumption |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-21 | Claude | Created. Multi-hook rotation architecture accepted. |

---

## Metadata

```yaml
id: "FEAT-002:DEC-003"
parent_id: "FEAT-002"
work_type: DECISION
title: "Multi-Hook Rotation Architecture"
status: ACCEPTED
priority: HIGH
created_by: "Claude"
created_at: "2026-02-21"
decided_at: "2026-02-21"
```
