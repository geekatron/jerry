# STORY-013:DISC-001: disallowedTools Is Redundant When tools Is Explicitly Declared

> **Type:** discovery
> **Status:** validated
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-03-29T19:00:00Z
> **Completed:** 2026-03-29T19:00:00Z
> **Parent:** STORY-013
> **Owner:** adam.nowak
> **Source:** STORY-013 M-007 investigation + Context7 Claude Code docs

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Core finding |
| [Context](#context) | How this was discovered |
| [Finding](#finding) | Technical detail |
| [Evidence](#evidence) | Sources |
| [Implications](#implications) | Impact on project |
| [Relationships](#relationships) | Related work items |

---

## Summary

`disallowedTools` provides zero additional runtime protection when an agent explicitly declares its `tools` list. All 89 Jerry agents declare `tools` explicitly. The `tools` allowlist is the sole enforcement layer for P-003 tool access control.

**Key Findings:**
- Claude Code enforces `tools` as a strict allowlist -- agents can ONLY use tools in the list
- `disallowedTools` only has runtime value when `tools` is omitted (agent inherits ALL tools)
- 89/89 Jerry agents declare `tools` explicitly -- `disallowedTools` is redundant for all of them
- STORY-021 (add disallowedTools to 79 non-UX workers) closed as wont_do based on this finding

**Validation:** Confirmed via Context7 Claude Code documentation and empirical verification (89/89 agents declare tools).

---

## Context

### Background

During STORY-013 M-007 remediation (Task->Agent rename in disallowedTools), red-vuln finding F-003 recommended adding `disallowedTools: [Agent]` to 79 non-UX worker agents as defense-in-depth. This triggered a cost-benefit analysis.

### Research Question

Does `disallowedTools` provide meaningful runtime protection beyond the `tools` allowlist?

### Investigation Approach

1. Queried Context7 Claude Code documentation for `tools` and `disallowedTools` behavior
2. Counted agents with explicit `tools` declarations via grep
3. Assessed whether any agent omits the `tools` field (which would cause ALL tool inheritance)

---

## Finding

### Claude Code Tool Access Model

From Claude Code docs (Context7, `/anthropics/claude-code`):

> The tools field is an optional configuration that restricts an agent to specific tools. **If omitted, the agent has access to all available tools.**

This means:
- `tools: [Read, Write, Grep]` -- agent can ONLY use Read, Write, Grep. Period.
- `tools` omitted -- agent inherits ALL tools. `disallowedTools` is the only deny mechanism.

### Jerry Agent Inventory

`grep -c '^tools:' skills/**/agents/*.md` = 89 matches across 89 agent files.

Zero agents omit the `tools` field. Therefore `disallowedTools` is redundant for every agent in the repository.

### When disallowedTools Would Matter

Only if someone removes the `tools` field entirely from an agent definition, causing it to inherit all tools. This scenario is better caught by CI validation (STORY-022: error if non-T5 agent has `Agent` in tools) than by a redundant deny field.

---

## Evidence

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Documentation | Claude Code agent `tools` field behavior | Context7 `/anthropics/claude-code` -- Agent Development SKILL.md | 2026-03-29 |
| E-002 | Empirical | 89/89 agents declare `tools` explicitly | `grep -c '^tools:' skills/**/agents/*.md` | 2026-03-29 |

---

## Implications

### Impact on Project

- STORY-021 (add disallowedTools to 79 agents) closed as wont_do -- zero runtime value
- STORY-022 scoped down from 2 rules to 1 -- removed disallowedTools check, kept tools check only
- Existing `disallowedTools: [Agent]` on UX workers is harmless but provides no protection beyond `tools`

### Decisions Affected

- **CI validation scope (STORY-022):** Only check `Agent` presence in non-T5 `tools` lists. Do not check `disallowedTools`.

---

## Relationships

### Informs

- [STORY-022](../STORY-022-ci-task-agent-check/STORY-022-ci-task-agent-check.md) -- Scoped down from 2 rules to 1
- [STORY-021](../STORY-021-non-ux-disallowed-tools/STORY-021-non-ux-disallowed-tools.md) -- Closed as wont_do

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [STORY-013](../STORY-013-fix-tier-tool-mismatches.md) | Parent story (co-located per REQ-D-025) |
| Security Report | [red-vuln F-003](../../../../skills/eng-team/output/STORY-013-M007/red-vuln-agent-tool-access.md) | Original finding |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-03-29 | adam.nowak | Created and validated discovery |
