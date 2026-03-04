# Plan: Skill Composition Pipeline — Two Schemas + Governance Injection

> **Project:** PROJ-012 Agent Optimization
> **Created:** 2026-03-02
> **Status:** In Progress
> **SSOT:** This file (git-tracked). The ephemeral plan file at `~/.claude/plans/` is transient.

## Summary

Two separate schemas (Anthropic official + Jerry canonical) for skills, `.jerry.skill.yaml` canonical sources, and a composition pipeline to assemble SKILL.md files with governance sections injected into the body.

## Phases

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Plan persistence | Complete |
| 1 | Schemas (anthropic-skill-frontmatter-v1 + skill-canonical-v1) | In Progress |
| 2 | Canonical source files (.jerry.skill.yaml x14) | Pending |
| 3 | Frontmatter migration (strip Jerry fields from SKILL.md) | Pending |
| 4 | Python composition pipeline | Pending |
| 5 | Pre-commit hook + CI gate | Pending |
| 6 | Documentation updates | Pending |
| 7 | Adversarial quality review (C4 tournament) | Pending |

## Key Decisions

- SKILL.md body is human-authored docs for MAIN CONTEXT — no XML transformation needed
- Governance sections use `## Heading` format (not XML tags)
- Pipeline is lighter than agent compose (no 4-layer merge, no tool mapping)
- Canonical source: `skills/{skill}/composition/skill.jerry.yaml`
