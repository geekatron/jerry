# STORY-012: Audit Skills and Agent Definitions for Missing WebFetch/WebSearch Permissions

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: Identify agents/skills that should have WebSearch/WebFetch but don't, and vice versa
-->

> **Type:** story
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-27T09:30:00Z
> **Due:**
> **Completed:** 2026-03-27T09:00:00Z
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
| [Audit Dimensions](#audit-dimensions) | What to check |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** Jerry framework maintainer

**I want** a complete audit of which agents and skills have (or are missing) WebSearch, WebFetch, and Context7 MCP permissions

**So that** agents that need web research capability have it, agents that shouldn't have it don't, and the rationale for each decision is documented

---

## Summary

Issue #217 exposed that `adv-executor` lacked web tools and hallucinated facts. This is likely not an isolated case -- other agents may also be missing tools they need, or conversely, may have web access they don't need (violating principle of least privilege).

This story audits ALL 89 agent definitions and 30 SKILL.md files to produce a complete inventory of web tool permissions, identify gaps, and recommend changes.

**Scope:**
- Inventory: which agents/skills currently have WebSearch, WebFetch, Context7 MCP
- Gap analysis: which agents SHOULD have web access based on their cognitive mode, role, and methodology
- Over-privilege analysis: which agents have web access but don't need it
- Cross-reference against `mcp-tool-standards.md` Agent Integration Matrix
- Cross-reference against `agent-development-standards.md` T1-T5 tier assignments in governance YAML
- Produce a recommendation table with rationale per agent

---

## Acceptance Criteria

- [ ] Complete inventory of WebSearch/WebFetch/Context7 permissions across all 89 agents
- [ ] Complete inventory of allowed-tools web permissions across all 30 SKILL.md files
- [ ] Gap analysis: agents that SHOULD have web access but don't (like adv-executor per #217)
- [ ] Over-privilege analysis: agents that HAVE web access but don't need it
- [ ] Cross-reference against `mcp-tool-standards.md` Agent Integration Matrix (is it current?)
- [ ] Cross-reference against governance YAML tool_tier (T1/T2 agents shouldn't have web tools; T3+ should)
- [ ] Recommendation table: per-agent add/remove/keep decision with rationale
- [ ] Identified changes tracked as follow-up tasks or linked to existing issues
- [ ] Audit report persisted to project research directory

---

## Audit Dimensions

### 1. Agent-Level Tool Inventory

For each of the 89 agents, check `.md` frontmatter `tools` field for:
- `WebSearch` presence/absence
- `WebFetch` presence/absence
- `mcp__context7__resolve-library-id` presence/absence
- `mcp__context7__query-docs` presence/absence

### 2. Skill-Level Tool Inventory

For each of the 30 SKILL.md files, check `allowed-tools` field for:
- `WebSearch` presence/absence
- `WebFetch` presence/absence
- Context7 MCP tools presence/absence
- Memory-Keeper MCP tools presence/absence

### 3. Governance YAML Cross-Reference

For each agent with a `.governance.yaml`, check:
- `tool_tier` matches actual tools (T1 should NOT have web tools; T3+ should)
- `capabilities.allowed_tools` matches `.md` frontmatter `tools`

### 4. mcp-tool-standards.md Alignment

Compare the Agent Integration Matrix in `.context/rules/mcp-tool-standards.md` against actual agent tool declarations. Identify drift.

### 5. Cognitive Mode Relevance

Agents with these cognitive modes typically NEED web access:
- `divergent` (research, exploration) -- YES (WebSearch, WebFetch, Context7)
- `forensic` (investigation, debugging) -- MAYBE (WebSearch for CVE/issue lookup)
- `convergent` (analysis, evaluation) -- MAYBE (Context7 for library docs)
- `systematic` (validation, auditing) -- UNLIKELY
- `integrative` (synthesis) -- MAYBE (Context7 for cross-referencing)

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Owner |
|----|-------|--------|-------|
| TASK-001 | Extract web tool inventory from all 89 agent .md frontmatter | pending | -- |
| TASK-002 | Extract web tool inventory from all 30 SKILL.md allowed-tools | pending | -- |
| TASK-003 | Cross-reference against governance YAML tool_tier | pending | -- |
| TASK-004 | Cross-reference against mcp-tool-standards.md Agent Integration Matrix | pending | -- |
| TASK-005 | Gap analysis: agents that need web tools but don't have them | pending | ps-analyst |
| TASK-006 | Over-privilege analysis: agents with web tools that don't need them | pending | ps-analyst |
| TASK-007 | Produce recommendation table with per-agent rationale | pending | ps-analyst |
| TASK-008 | Security review of recommended changes | pending | eng-security |
| TASK-009 | Create follow-up tasks for identified changes | pending | -- |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: Claude Code Schema Validation](../FEAT-001-claude-code-schema-validation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Related | STORY-011 | adv-executor tool access is one instance of this broader audit |
| Related | GitHub #217 | The incident that triggered this audit |
| Reference | mcp-tool-standards.md | Agent Integration Matrix is the current baseline |
| Reference | agent-development-standards.md | T1-T5 tier model defines tool access expectations |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-27 | adam.nowak | pending | Story created -- broad audit of web tool permissions across all agents/skills |
