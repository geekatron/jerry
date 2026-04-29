# DEC-001: Hook mechanism for ts-formatter substrate enforcement (SubagentStop/PostToolUse vs prompt-discipline)

> **Type:** decision
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** FEAT-003
> **Owner:** ps-architect
> **Decision Authority:** ps-architect (with eng-reviewer concurrence)
> **Decision State:** PENDING — to be authored at FEAT-003 entry, before STORY-009 starts

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Context](#context) | Why this decision exists |
| [Question](#question) | What we are deciding |
| [Options](#options) | Alternatives under consideration |
| [Decision Criteria](#decision-criteria) | How options will be evaluated |
| [Decision](#decision) | Outcome (filled at execution) |
| [Consequences](#consequences) | Trade-offs flowing from decision (filled at execution) |
| [Affected Entities](#affected-entities) | Stories that depend on this decision |

---

## Context

This Decision is pre-created per ps-architect D-4.2 review finding so that the hook-mechanism choice is captured in worktracker rather than made implicitly during execution and lost. STORY-009 (`wire verify into ts-formatter post-render hook`) and STORY-010 (`wire update-anchors into ts-formatter write pipeline`) both depend on this decision. Both share the same underlying choice: how does `ts-formatter` *enforce* the post-write substrate-validation step?

Two mechanisms are available within the Jerry framework:

1. **Claude Code SubagentStop / PostToolUse hooks** — deterministic L4 enforcement. The hook intercepts tool-call lifecycle events and runs `verify` / `update-anchors` automatically. The agent cannot complete without the validator passing.
2. **Prompt-discipline** — soft enforcement. The agent prompt instructs the agent to invoke `verify` / `update-anchors` post-render. Compliance depends on the LLM following the instruction.

This decision is the single highest-leverage technical decision in FEAT-003 per ps-architect L2 strategic implications: SubagentStop hook = deterministic L4 enforcement (hard guarantee); prompt-discipline = soft enforcement that could recur the audit's failure pattern at a different surface.

---

## Question

For STORY-009 (post-render `verify` invocation) and STORY-010 (write-pipeline `update-anchors` invocation), should `ts-formatter` enforce these via Claude Code lifecycle hooks (deterministic) or via agent-prompt discipline (LLM-mediated)?

---

## Options

### Option A: Claude Code SubagentStop / PostToolUse hooks

**Mechanism:** Implement hooks in `hooks/` that intercept `ts-formatter` lifecycle events. SubagentStop runs `verify` before the agent reports completion. PostToolUse on Write runs `update-anchors` after each rendered .md file write. Hook failure blocks completion.

**Pros:**
- Deterministic: agent literally cannot complete without validator passing
- Aligns with the audit's diagnostic — the failure mode (substrate drift) becomes mechanically impossible
- Matches the project-wide direction "outputs need to be validated automatically"
- Hook output captured in tool-result stream, preserving evidence trail

**Cons:**
- Implementation complexity: requires understanding Claude Code hook API surface
- Hook registration must be project-scoped (per project, not global) to avoid affecting other transcript usage
- Failure mode is binary: a hook crash blocks all `ts-formatter` runs
- Performance: hook invocation adds overhead per tool call (≤500ms target)

### Option B: Prompt-discipline

**Mechanism:** Update `ts-formatter.md` and `ts-formatter.prompt.md` to instruct the agent to invoke `verify` and `update-anchors` post-render. Agent return contract requires `validation_status: PASS` field.

**Pros:**
- Simple: agent prompt edit only, no new infrastructure
- Reversible: prompt change can be tuned without code changes
- Human-readable: behavior visible in agent prompt rather than buried in hooks

**Cons:**
- LLM-mediated: compliance depends on agent following instructions correctly
- Recurrence of audit pattern: another LLM-judged surface, the exact failure mode the audit identified
- Difficult to enforce at scale: any future agent edit could regress the discipline silently
- No deterministic guarantee — same class of risk as the original audit's plateau at 0.90

---

## Decision Criteria

The decision will be evaluated against:

| Criterion | Weight | Option A | Option B |
|-----------|--------|----------|----------|
| Deterministic enforcement (matches user direction) | High | Strong | Weak |
| Resilience to future agent prompt edits | High | Strong | Weak |
| Implementation effort | Medium | Higher | Lower |
| Maintenance burden | Medium | Hook-debug | Prompt-edit |
| Performance overhead | Low | ≤500ms | None |
| Reversibility | Low | Medium | High |

---

## Decision

**(To be filled at FEAT-003 execution start by `ps-architect` after consulting `eng-reviewer`.)**

Recommended timing: pre-Phase 1 sync barrier (per ps-architect L2 strategic implications). Deferring this decision to STORY-009 execution risks ad-hoc selection.

---

## Consequences

**(To be filled when decision is made.)**

If Option A: Cleanup work to deprecate any existing prompt-discipline approaches; hook test suite needed; document hook contract for future ts-formatter agent revisions.

If Option B: Acceptance criteria on STORY-009/010 must include a regression test that the prompt-discipline holds across at least 10 simulated agent runs (per H-14 minimum 3 iterations + safety margin).

---

## Affected Entities

| Entity | Dependency on this Decision |
|--------|----------------------------|
| STORY-009 | Decides which hook (SubagentStop) implementation path to take |
| STORY-010 | Decides which hook (PostToolUse) implementation path to take |
| FEAT-003 | Quality gate cannot pass with hook approach undecided |
| EN-008 | Final adversary tournament evaluates the chosen mechanism |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-29 | adam.nowak (via Claude) | pending | Pre-created per ps-architect D-4.2 finding. Decision authoring deferred to FEAT-003 execution start. |
