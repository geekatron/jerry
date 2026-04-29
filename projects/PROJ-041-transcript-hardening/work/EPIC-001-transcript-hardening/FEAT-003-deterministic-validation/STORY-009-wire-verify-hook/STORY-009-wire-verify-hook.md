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

| ID | Title | Status |
|----|-------|--------|
| TASK-001 | Decide hook mechanism (SubagentStop vs prompt) | pending |
| TASK-002 | Update ts-formatter.md agent prompt | pending |
| TASK-003 | Update ts-formatter.prompt.md checklist | pending |
| TASK-004 | (If hook chosen) Implement SubagentStop hook | pending |
| TASK-005 | Update agent return contract for validation_status | pending |
| TASK-006 | Test against iter-9 audit packet | pending |
| TASK-007 | Run /eng-team eng-reviewer | pending |
| TASK-008 | Run /adversary C4 review | pending |

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
