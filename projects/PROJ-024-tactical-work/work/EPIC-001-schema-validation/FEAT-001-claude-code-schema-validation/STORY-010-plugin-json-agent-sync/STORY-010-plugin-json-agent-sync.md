# STORY-010: Sync plugin.json Agents List with Actual Agent Files

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: Register all 20 missing agents in plugin.json and add CI drift detection
-->

> **Type:** story
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-27T08:00:00Z
> **Due:**
> **Completed:** 2026-03-27T06:00:00Z
> **Parent:** FEAT-001
> **Owner:** adam.nowak
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | What needs to happen |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Missing Agents](#missing-agents) | The 20 agents not in plugin.json |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** Claude Code user installing Jerry as a plugin

**I want** all 89 agents to be registered in `.claude-plugin/plugin.json`

**So that** agents from newer skills (contract-design, prompt-engineering, test-spec, use-case, user-experience, and all UX sub-skills) are discoverable and invocable

---

## Summary

`.claude-plugin/plugin.json` lists 69 agents. There are 89 agent `.md` files on disk. 20 agents from 15 skills are missing from the registry. These agents exist and work when invoked by name, but are not formally registered in the plugin manifest -- meaning plugin-based installations may not discover them.

Additionally, there is no CI check to prevent this drift. When a new agent is added to `skills/*/agents/`, nothing enforces that it gets added to `plugin.json`.

**Scope:**
- Add all 20 missing agents to `.claude-plugin/plugin.json`
- Add a CI validation step that detects agent-file-to-plugin.json drift
- The CI check should compare `skills/*/agents/*.md` on disk against the `agents` array in `plugin.json` and fail if any are missing

---

## Missing Agents

20 agents across 15 skills not registered in `.claude-plugin/plugin.json`:

| Skill | Agent File | Agent Name |
|-------|-----------|------------|
| contract-design | `skills/contract-design/agents/cd-generator.md` | cd-generator |
| contract-design | `skills/contract-design/agents/cd-validator.md` | cd-validator |
| prompt-engineering | `skills/prompt-engineering/agents/pe-builder.md` | pe-builder |
| prompt-engineering | `skills/prompt-engineering/agents/pe-constraint-gen.md` | pe-constraint-gen |
| prompt-engineering | `skills/prompt-engineering/agents/pe-scorer.md` | pe-scorer |
| test-spec | `skills/test-spec/agents/tspec-analyst.md` | tspec-analyst |
| test-spec | `skills/test-spec/agents/tspec-generator.md` | tspec-generator |
| use-case | `skills/use-case/agents/uc-author.md` | uc-author |
| use-case | `skills/use-case/agents/uc-slicer.md` | uc-slicer |
| user-experience | `skills/user-experience/agents/ux-orchestrator.md` | ux-orchestrator |
| ux-ai-first-design | `skills/ux-ai-first-design/agents/ux-ai-design-guide.md` | ux-ai-design-guide |
| ux-atomic-design | `skills/ux-atomic-design/agents/ux-atomic-architect.md` | ux-atomic-architect |
| ux-behavior-design | `skills/ux-behavior-design/agents/ux-behavior-diagnostician.md` | ux-behavior-diagnostician |
| ux-design-sprint | `skills/ux-design-sprint/agents/ux-sprint-facilitator.md` | ux-sprint-facilitator |
| ux-heart-metrics | `skills/ux-heart-metrics/agents/ux-heart-analyst.md` | ux-heart-analyst |
| ux-heuristic-eval | `skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.md` | ux-heuristic-evaluator |
| ux-inclusive-design | `skills/ux-inclusive-design/agents/ux-inclusive-evaluator.md` | ux-inclusive-evaluator |
| ux-jtbd | `skills/ux-jtbd/agents/ux-jtbd-analyst.md` | ux-jtbd-analyst |
| ux-kano-model | `skills/ux-kano-model/agents/ux-kano-analyst.md` | ux-kano-analyst |
| ux-lean-ux | `skills/ux-lean-ux/agents/ux-lean-ux-facilitator.md` | ux-lean-ux-facilitator |

---

## Acceptance Criteria

- [ ] All 20 missing agents added to `.claude-plugin/plugin.json` `agents` array
- [ ] Agents sorted alphabetically by path within the array
- [ ] `plugin.json` remains valid JSON after additions
- [ ] `jerry agents validate-frontmatter` passes for all 89 agents after changes
- [ ] CI drift detection script added (compares disk files to plugin.json)
- [ ] CI job fails if any agent file on disk is not in plugin.json
- [ ] CI job fails if any agent in plugin.json does not exist on disk (stale reference)

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Owner |
|----|-------|--------|-------|
| TASK-001 | Add 20 missing agents to plugin.json | pending | -- |
| TASK-002 | Verify plugin.json is valid JSON and agents are sorted | pending | -- |
| TASK-003 | Create drift detection script (scripts/check_plugin_agent_sync.py) | pending | -- |
| TASK-004 | Add plugin-agent-sync check to CI pipeline | pending | -- |
| TASK-005 | Run jerry agents validate-frontmatter to confirm all 89 pass | pending | -- |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: Claude Code Schema Validation](../FEAT-001-claude-code-schema-validation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Related | STORY-008 | Frontmatter validation confirms agents are valid |
| Related | STORY-009 | CI pipeline integration |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-27 | adam.nowak | pending | Story created -- 20/89 agents not in plugin.json |
