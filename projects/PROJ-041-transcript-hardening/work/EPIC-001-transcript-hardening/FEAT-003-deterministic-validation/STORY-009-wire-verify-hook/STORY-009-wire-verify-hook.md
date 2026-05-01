# STORY-009: Wire `verify` into `ts-formatter` post-render hook

> **Type:** story
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-04-28T00:00:00Z
> **Parent:** FEAT-003
> **Owner:** adam.nowak
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | What this story delivers |
| [Integration Point](#integration-point) | Where verify runs in the agent lifecycle |
| [Agent Assignment](#agent-assignment) | Specific skill+agent mappings |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** consumer of `ts-formatter` agent output,
**I want** the agent to run `verify` before reporting completion,
**So that** any rule violations the agent introduced are caught at agent exit (not 30 minutes later in adversary review).

---

## Summary

Wire the `verify` CLI into the `ts-formatter` agent post-render hook so the agent cannot report completion without validators passing. Catches drift at agent exit, not 30 minutes later in adversary review. Hook mechanism (SubagentStop vs prompt-discipline) decided in FEAT-003 DEC-001.

---

## Integration Point

`ts-formatter` agent's completion checkpoint runs `jerry transcript verify <packet>` before declaring success. If `verify` exit code != 0, the agent reports the failure and does NOT mark the work complete. This catches the iter-9 audit regression class at the agent's boundary.

| Hook surface | Mechanism |
|--------------|-----------|
| `skills/transcript/agents/ts-formatter.md` | Agent prompt updated to require post-render `verify` invocation as part of acceptance |
| `skills/transcript/agents/ts-formatter.prompt.md` | Detailed checklist updated |
| Agent return contract | Adds `validation_status: PASS|FAIL` field; FAIL prevents completion claim |

If we're using a Claude Code SubagentStop hook for stronger enforcement, that's a deterministic L4-layer enforcement option. STORY-009 evaluates and either uses it OR enforces by prompt + agent self-discipline. Decision recorded in DEC.

---

## Agent Assignment

| Step | Skill | Agent | Purpose |
|------|-------|-------|---------|
| 1 | `/problem-solving` | `ps-architect` | Decision: SubagentStop hook vs prompt-discipline approach (DEC for hook mechanism) |
| 2 | `/eng-team` | `eng-backend` | Update `ts-formatter.md` agent prompt + `ts-formatter.prompt.md` checklist; add `validation_status: PASS\|FAIL` to return contract |
| 3 | `/eng-team` | `eng-backend` | If hook mechanism chosen: implement SubagentStop hook |
| 4 | `/eng-team` | `eng-reviewer` | Final-gate review: agent prompt changes preserve agent's primary purpose; no regression in non-bracketed packets |
| 5 | `/eng-team` | `eng-qa` | Test against iter-9 audit packet — agent correctly catches at exit |
| 6 | `/adversary` | `adv-executor` + `adv-scorer` | C4 ≥0.95 review |
| 7 | `/worktracker` | `wt-verifier` | Validate AC; close |

---

## Acceptance Criteria

- [ ] `ts-formatter` agent prompt updated to require post-render `verify` invocation; agent cannot report `completed` if `verify` exit code != 0.
- [ ] `ts-formatter.prompt.md` checklist updated.
- [ ] Decision recorded: SubagentStop hook vs prompt-discipline approach (DEC).
- [ ] If SubagentStop hook chosen: hook exists, runs `verify`, blocks completion on failure.
- [ ] Reproduces audit's iter-9 catch at agent exit (not at adversary review 30 min later).
- [ ] Existing `ts-formatter` test suite continues to pass; tests updated to include verify step.
- [ ] Performance: post-render verify adds <1s to agent execution time on standard packets.
- [ ] `/eng-team` `eng-reviewer` confirms agent prompt changes do not break agent's primary purpose.
- [ ] `/adversary` C4 ≥0.95 phase gate.

---

## Children Tasks

| ID | Title | Owner | Status |
|----|-------|-------|--------|
| [TASK-114](./TASK-114-decide-hook-mechanism-via-dec-001.md) | Decide hook mechanism (SubagentStop vs prompt-discipline) via FEAT-003 DEC-001 | `ps-architect` | pending |
| [TASK-115](./TASK-115-update-ts-formatter-prompt.md) | Update ts-formatter.md agent prompt + ts-formatter.prompt.md checklist | `eng-backend` | pending |
| [TASK-116](./TASK-116-implement-subagentstop-hook-if-chosen.md) | If hook chosen (per DEC-001): implement SubagentStop hook | `eng-backend` | pending |
| [TASK-117](./TASK-117-final-gate-review-prompt-changes.md) | Final-gate review: agent prompt changes preserve agent's primary purpose | `eng-reviewer` | pending |
| [TASK-118](./TASK-118-test-iter-9-catch-at-agent-exit.md) | Test against iter-9 audit packet — agent correctly catches at exit | `eng-qa` | pending |
| [TASK-119](./TASK-119-run-adversary-c4-review.md) | Run /adversary C4 review | `adv-executor` | pending |
| [TASK-120](./TASK-120-validate-ac-and-close-story-009.md) | Validate STORY-009 AC and close | `wt-verifier` | pending |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-003](../FEAT-003-deterministic-validation.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | STORY-007 | verify CLI must exist |
| Blocked By | STORY-003..STORY-006 | All validators must be implemented |
| Blocks | EN-008 | Final adversary needs hook in place |

### Source

- [#273 comment 1](https://github.com/geekatron/jerry/issues/273#issuecomment-4339264545) — gist proposal item 2

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Story created. |
