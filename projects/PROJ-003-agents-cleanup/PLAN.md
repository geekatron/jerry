# PROJ-003-agents-cleanup: Agent and Skill Structure Cleanup

> **Status:** PLANNING
> **Created:** 2026-01-12
> **Branch:** cc/clean-up-agents

---

## Problem Statement

The Jerry framework has accumulated legacy agent definitions in `.claude/agents/` and `.claude/commands/` that conflict with the canonical skill-based structure in `skills/{skill}/agents/`. This creates confusion about the authoritative source of agent definitions and violates the principle of single source of truth.

### 5W1H Analysis (Pending)

Research required to answer:
- **What**: What are the legacy files and what should replace them?
- **Why**: Why did this duplication occur? What patterns should we follow?
- **When**: When should cleanup happen? What's the migration path?
- **Where**: Where should agents/commands live per industry best practices?
- **Who**: Who (in terms of documentation/code) references these legacy files?
- **How**: How should we migrate without breaking existing functionality?

---

## Goals

1. Research Claude Code plugin best practices for agent/skill organization
2. Analyze current state (legacy files vs canonical structure)
3. Define migration strategy based on evidence and best practices
4. Execute cleanup with validation
5. Document decisions as ADRs

---

## Phases (TBD after research)

Phase details will be populated after ps-researcher completes industry analysis.

---

## Current Files to Evaluate

### Legacy Files (potentially to be removed/migrated)
- `.claude/agents/orchestrator.md`
- `.claude/agents/qa-engineer.md`
- `.claude/agents/security-auditor.md`
- `.claude/agents/TEMPLATE.md`
- `.claude/commands/architect.md`
- `.claude/commands/release.md`
- `AGENTS.md` (root)

### Canonical Structure (authoritative)
- `skills/problem-solving/agents/ps-*.md`
- `skills/{skill}/SKILL.md`

---

## Research Tasks

1. [ ] Research Claude Code plugin structure best practices
2. [ ] Analyze how other Claude Code plugins organize agents/skills
3. [ ] Review Anthropic documentation for recommended patterns
4. [ ] Gap analysis: current state vs best practices
5. [ ] Trade-off analysis for migration approaches

---

*Plan Version: 0.1.0*
*Last Updated: 2026-01-12*
