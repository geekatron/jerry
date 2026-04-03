# STORY-013: Fix Tier/Tool Mismatches in Agent Definitions

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: Fix governance YAML tier declarations that don't match actual tools in frontmatter
-->

> **Type:** story
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-27T10:00:00Z
> **Due:**
> **Completed:** 2026-03-29T21:00:00Z
> **Parent:** FEAT-001
> **Owner:** adam.nowak
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | What needs to happen |
| [Mismatches](#mismatches) | All identified tier/tool inconsistencies |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** Jerry framework developer reviewing agent definitions

**I want** governance YAML `tool_tier` to accurately reflect the actual tools in the .md frontmatter

**So that** the T1-T5 tier model is trustworthy and CI cross-validation can enforce consistency

---

## Summary

STORY-012 audit found 8 inconsistencies where the governance YAML tier declaration doesn't match the actual tools in the .md frontmatter, or where skill-level allowed-tools don't align with agent-level tools. Each mismatch erodes trust in the tier model and could mislead developers creating new agents based on these examples.

---

## Mismatches

### M-001: nse-reporter -- Incomplete T3 (WebFetch without WebSearch)

| Attribute         | Value                                                   |
|-------------------|---------------------------------------------------------|
| **File**          | `skills/nasa-se/agents/nse-reporter.md`                 |
| **Governance**    | `tool_tier: T3` (should have both WebSearch + WebFetch) |
| **Frontmatter**   | Has `WebFetch` but NOT `WebSearch`                      |
| **Fix**           | Add `WebSearch` to tools in frontmatter                 |
| **Source**        | ps-analyst P2                                           |
| **User Feedback** | Correct                                                 |

### M-002: diataxis-explanation -- Divergent Mode at T2

| Attribute | Value                                                                                                             |
|-----------|-------------------------------------------------------------------------------------------------------------------|
| **File** | `skills/diataxis/agents/diataxis-explanation.md` + `.governance.yaml`                                             |
| **Governance** | `tool_tier: T2`, `cognitive_mode: divergent`                                                                      |
| **Issue** | agent-development-standards.md maps divergent mode to T3+ ("Needs breadth; premature convergence misses sources") |
| **Fix** | Either upgrade to T3 (add WebSearch/WebFetch) OR document justification for T2 exception                          |
| **Source** | ps-analyst P2                                                                                                     |
| **User Feedback** | Upgrade to T3                                                                                                     |

### M-003: ux-behavior-diagnostician -- T2 Declared, T3 Tools

| Attribute | Value |
|-----------|-------|
| **File** | `skills/ux-behavior-design/agents/ux-behavior-diagnostician.md` + `.governance.yaml` |
| **Governance** | `tool_tier: T2` |
| **Frontmatter** | Has `WebSearch`, `WebFetch` (T3-level tools) |
| **Fix** | Update governance to `tool_tier: T3` |
| **Source** | eng-security |
| **User Feedback** | Correct                                                 |

### M-004: nse-requirements -- T4 Declared, Has T3+T4 Tools

| Attribute | Value                                                                                                                                                                                                                                                                                                                                                                              |
|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **File** | `skills/nasa-se/agents/nse-requirements.md` + `.governance.yaml`                                                                                                                                                                                                                                                                                                                   |
| **Governance** | `tool_tier: T4`                                                                                                                                                                                                                                                                                                                                                                    |
| **Frontmatter** | Has `WebSearch`, `WebFetch` (T3) + `mcpServers: memory-keeper` (T4) = effectively T5 capability                                                                                                                                                                                                                                                                                    |
| **Fix** | Either restrict to T4 (remove WebSearch/WebFetch) OR declare as T5 with justification                                                                                                                                                                                                                                                                                              |
| **Source** | eng-security                                                                                                                                                                                                                                                                                                                                                                       |
| **User Feedback** | I think we are missing a Tier or Two. Why is it that only Orchestration with Delegation agents have access to Memory-Keeper? Why wouldn't we want other agents to be able to leverage Memory-Keeper? Why wouldn't we want the agents to be use Memeory-Keeper. I am asking - not telling. Is this to keep them stateless and only have the orchestration skills use Memory Keeper? |

### M-005: orchestration SKILL.md -- Authorizes Web Tools Agents Don't Have

| Attribute | Value                                                                                                                |
|-----------|----------------------------------------------------------------------------------------------------------------------|
| **File** | `skills/orchestration/SKILL.md`                                                                                      |
| **Issue** | `allowed-tools` includes `WebSearch`, `WebFetch` but orch-planner, orch-synthesizer, orch-tracker don't declare them |
| **Fix** | Either remove from SKILL.md allowed-tools OR add to agent frontmatter (decide intent)                                |
| **Source** | ps-analyst                                                                                                           |
| **User Feedback** | Add them to the agent frontmatter.                                                                                   |

### M-006: pm-pmm SKILL.md -- Missing allowed-tools Entirely

| Attribute | Value |
|-----------|-------|
| **File** | `skills/pm-pmm/SKILL.md` |
| **Issue** | No `allowed-tools` field at all. All 5 pm agents have WebSearch/WebFetch in their frontmatter but the skill doesn't grant auto-approval. |
| **Fix** | Add `allowed-tools` matching the agents' tool union |
| **Source** | ps-analyst |
| **User Feedback** | Correct                                                 |

### M-007: 6 UX Worker Agents Missing disallowedTools: [Agent]

| Attribute | Value                                                                                                                                                                              |
|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Agents** | ux-ai-design-guide, ux-atomic-architect, ux-sprint-facilitator, ux-heuristic-evaluator, ux-inclusive-evaluator, ux-lean-ux-facilitator                                             |
| **Issue** | H-35 says worker agents must not have the Agent tool. These agents don't explicitly disallow it. They inherit all tools from parent by not declaring `tools` or `disallowedTools`. |
| **Fix** | Add `disallowedTools: Agent` to each, or add explicit `tools` list without Agent                                                                                                   |
| **Source** | eng-security                                                                                                                                                                       |
| **User Feedback** | Add `disallowedTools`                                                                                                                                                               |

### M-008: ux-heart-analyst, ux-kano-analyst -- Assess T2 vs T3

| Attribute | Value                                                                                                           |
|-----------|-----------------------------------------------------------------------------------------------------------------|
| **Agents** | `skills/ux-heart-metrics/agents/ux-heart-analyst.md`, `skills/ux-kano-model/agents/ux-kano-analyst.md`          |
| **Issue** | 7 of 10 UX sub-skill agents are T3. These 2 are T2. Their methodologies may or may not require external data.   |
| **Fix** | Assess whether HEART GSM process and Kano survey methodology need web access for benchmarks. Document decision. |
| **Source** | ps-analyst                                                                                                      |
| **User Feedback** | Why wouldn't they require access to external data? Help me understand.                                          |

---

## Acceptance Criteria

- [x] M-001: nse-reporter has both WebSearch and WebFetch
- [x] M-002: diataxis-explanation upgraded to T3 (now T4 after tier renumbering)
- [x] M-003: ux-behavior-diagnostician governance corrected to T2 (frontmatter has T2 tools only; original STORY-012 audit incorrectly reported T3 tools in frontmatter)
- [x] M-004: nse-requirements tier resolved -- T4 (External) under new Persistent-First Linear model is exact fit for Web+MK. Resolved by STORY-017/018 tier renumbering.
- [x] M-005: orchestration agents have WebSearch/WebFetch added to frontmatter
- [x] M-006: pm-pmm SKILL.md has allowed-tools field
- [x] M-007: 6 UX worker agents have Agent tool explicitly disallowed (via disallowedTools)
- [x] M-008: ux-heart-analyst and ux-kano-analyst upgraded to T3 (now T4 after tier renumbering)
- [x] 611 schema tests pass, 320 architecture/contract tests pass
- [x] 62 pm-pmm security tests pass (tier values updated T3→T4)

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Blocked By | Owner |
|----|-------|--------|-----------|-------|
| TASK-001 | Fix M-001: nse-reporter add WebSearch | completed | eng-backend | -- |
| TASK-002 | Fix M-002: diataxis-explanation upgrade to T3 | completed | eng-backend | -- |
| TASK-003 | Fix M-003: ux-behavior-diagnostician governance corrected to T2 | completed | eng-security | -- |
| TASK-004 | Fix M-004: nse-requirements tier resolution | completed | Resolved by STORY-017/018 | -- |
| TASK-005 | Fix M-005: orchestration agents add WebSearch/WebFetch | completed | eng-backend | -- |
| TASK-006 | Fix M-006: pm-pmm SKILL.md add allowed-tools | completed | eng-backend | -- |
| TASK-007 | Fix M-007: 6 UX worker agents already have disallowedTools: Task | completed | eng-backend (verified) | -- |
| TASK-008 | Fix M-008: ux-heart-analyst + ux-kano-analyst upgrade to T3 | completed | eng-backend | -- |
| TASK-009 | Run validation suite to confirm all fixes | completed | -- | -- |

### Task Links

- [TASK-001: nse-reporter add WebSearch](./TASK-001/TASK-001-nse-reporter-add-websearch.md)
- [TASK-002: diataxis-explanation upgrade to T3](./TASK-002/TASK-002-diataxis-explanation-upgrade-t3.md)
- [TASK-003: ux-behavior-diagnostician governance T2->T3](./TASK-003/TASK-003-ux-behavior-diagnostician-governance-t3.md)
- [TASK-004: nse-requirements tier resolution](./TASK-004/TASK-004-nse-requirements-tier-resolution.md) **(BLOCKED by STORY-015)**
- [TASK-005: orchestration agents add web tools](./TASK-005/TASK-005-orchestration-agents-add-web-tools.md)
- [TASK-006: pm-pmm SKILL.md add allowed-tools](./TASK-006/TASK-006-pm-pmm-add-allowed-tools.md)
- [TASK-007: 6 UX worker agents add disallowedTools](./TASK-007/TASK-007-ux-workers-add-disallowed-tools.md)
- [TASK-008: ux-heart-analyst + ux-kano-analyst upgrade to T3](./TASK-008/TASK-008-ux-heart-kano-upgrade-t3.md)
- [TASK-009: Run validation suite](./TASK-009/TASK-009-run-validation-suite.md)

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: Claude Code Schema Validation](../FEAT-001-claude-code-schema-validation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Informed By | STORY-012 | Audit identified all mismatches |
| Related | STORY-011 | adv-executor T2->T3 is a related tier change |
| Blocked By (TASK-004 only) | STORY-015 | nse-requirements tier fix depends on new tier model |
| Blocks | STORY-014 | Doc drift fixes depend on tier fixes landing |
| Produced | STORY-021 | Defense-in-depth analysis (wont_do per DISC-001) |
| Produced | STORY-022 | CI validation for P-003 Agent tool check |
| Produced | DISC-001 | disallowedTools redundancy finding |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-27 | adam.nowak | pending | Story created from STORY-012 audit findings |
| 2026-03-28 | adam.nowak | in_progress | Wave 1: 7 tasks implemented (TASK-004 blocked). Wave 2: eng-security (9 findings), red-vuln (6 findings), ps-reviewer (5 findings). SEC-001/004/005/006 + DX-HIGH-1/2/3 fixed. M-003 corrected (T2 not T3). Citation guardrails added to nse-reporter + orch agents. |
| 2026-03-28 | adam.nowak | in_progress | Iteration 2: 5 scorer findings fixed. Score 0.82 -> 0.895. |
| 2026-03-28 | adam.nowak | in_progress | Iteration 3: 4 hygiene fixes. Score 0.895 -> 0.942. |
| 2026-03-29 | claude | completed | TASK-004 resolved by tier renumbering (STORY-017/018): T4=External is exact fit for nse-requirements (Web+MK). TASK-009 validation passed: 611 schema, 320 architecture, 62 pm-pmm tests. All 10 ACs verified. |
| 2026-03-29 | adam.nowak | in_progress | Re-opened: M-007 Task->Agent rename across 11 UX agents + ~100 doc edits across 30 files. C4 /adversary 0.954 PASS (5 iterations). eng-security (5 findings) + red-vuln (6 findings). Produced STORY-021 (wont_do), STORY-022 (completed, C4 0.949 PASS), DISC-001 (disallowedTools redundancy). Worktracker audit: 16 findings fixed. |
