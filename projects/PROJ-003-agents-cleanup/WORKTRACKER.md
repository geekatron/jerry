# PROJ-003-agents-cleanup Work Tracker

> **Project:** Agent and Skill Structure Cleanup
> **Status:** IN_PROGRESS
> **Branch:** `cc/clean-up-agents`
> **Created:** 2026-01-12
> **Last Updated:** 2026-01-12

---

## Quick Reference

| Metric | Value |
|--------|-------|
| Total Work Items | 24 |
| Completed | 23 (Phase 0-4 complete) |
| In Progress | 0 |
| Pending | 1 (wi-05-001) |
| Blocked | 0 |

---

## Phase Index

| Phase | Name | Status | Work Items | Duration Est. |
|-------|------|--------|------------|---------------|
| 0 | Research | COMPLETED | 7/7 | - |
| 1 | Plugin Infrastructure | COMPLETED | 4/4 | - |
| 2 | Skill Frontmatter | COMPLETED | 4/4 | - |
| 3 | Agent Standardization | COMPLETED | 4/4 | - |
| 4 | Hook System | COMPLETED | 4/4 | - |
| 5 | Registry Update | PENDING | 0/1 | 30 min |

---

## Phase 0: Research (COMPLETED)

| ID | Title | Status | File |
|----|-------|--------|------|
| wi-00-001 | Research Claude Code plugin best practices | DONE | [wi-00-001.md](work/wi-00-001.md) |
| wi-00-002 | Research plugins prior art | DONE | [wi-00-002.md](work/wi-00-002.md) |
| wi-00-003 | Research architecture patterns | DONE | [wi-00-003.md](work/wi-00-003.md) |
| wi-00-004 | Extract PROJ-001 knowledge | DONE | [wi-00-004.md](work/wi-00-004.md) |
| wi-00-005 | Gap analysis | DONE | [wi-00-005.md](work/wi-00-005.md) |
| wi-00-006 | Synthesis | DONE | [wi-00-006.md](work/wi-00-006.md) |
| wi-00-007 | Create ADR | DONE | [wi-00-007.md](work/wi-00-007.md) |

---

## Phase 1: Plugin Infrastructure (COMPLETED)

| ID | Title | Status | File |
|----|-------|--------|------|
| wi-01-001 | Rename manifest.json to plugin.json | DONE | [wi-01-001.md](work/wi-01-001.md) |
| wi-01-002 | Update plugin.json schema and fields | DONE | [wi-01-002.md](work/wi-01-002.md) |
| wi-01-003 | Create commands directory and move files | DONE | [wi-01-003.md](work/wi-01-003.md) |
| wi-01-004 | Cleanup and validate plugin structure | DONE | [wi-01-004.md](work/wi-01-004.md) |

---

## Phase 2: Skill Frontmatter (COMPLETED)

| ID | Title | Status | File |
|----|-------|--------|------|
| wi-02-001 | Add frontmatter to worktracker SKILL.md | DONE | [wi-02-001.md](work/wi-02-001.md) |
| wi-02-002 | Add frontmatter to architecture SKILL.md | DONE | [wi-02-002.md](work/wi-02-002.md) |
| wi-02-003 | Add frontmatter to worktracker-decomposition SKILL.md | DONE | [wi-02-003.md](work/wi-02-003.md) |
| wi-02-004 | Update problem-solving SKILL.md trigger phrases | DONE | [wi-02-004.md](work/wi-02-004.md) |

---

## Phase 3: Agent Standardization (COMPLETED)

| ID | Title | Status | File |
|----|-------|--------|------|
| wi-03-001 | Add frontmatter to orchestrator.md | DONE | [wi-03-001.md](work/wi-03-001.md) |
| wi-03-002 | Add frontmatter to qa-engineer.md | DONE | [wi-03-002.md](work/wi-03-002.md) |
| wi-03-003 | Add frontmatter to security-auditor.md | DONE | [wi-03-003.md](work/wi-03-003.md) |
| wi-03-004 | Update TEMPLATE.md and validate Phase 3 | DONE | [wi-03-004.md](work/wi-03-004.md) |

---

## Phase 4: Hook System (COMPLETED)

| ID | Title | Status | File |
|----|-------|--------|------|
| wi-04-001 | Update hooks.json paths to use CLAUDE_PLUGIN_ROOT | DONE | [wi-04-001.md](work/wi-04-001.md) |
| wi-04-002 | Add PreToolUse hook for Write/Edit validation | DONE | [wi-04-002.md](work/wi-04-002.md) |
| wi-04-003 | Migrate scripts from .claude/hooks/ | DONE | [wi-04-003.md](work/wi-04-003.md) |
| wi-04-004 | Cleanup and validate hook system | DONE | [wi-04-004.md](work/wi-04-004.md) |

---

## Phase 5: Registry Update (PENDING)

| ID | Title | Status | File |
|----|-------|--------|------|
| wi-05-001 | Update AGENTS.md with complete registry | PENDING | [wi-05-001.md](work/wi-05-001.md) |

---

## Bugs

| ID | Title | Severity | Status | Related WI |
|----|-------|----------|--------|------------|
| *None discovered yet* | | | | |

---

## Discoveries

| ID | Title | Impact | Related WI |
|----|-------|--------|------------|
| DISC-001 | Hybrid agent org is industry-aligned | Positive - no reorg needed | wi-00-003 |
| DISC-002 | ps-* agents already compliant | Positive - only framework agents need update | wi-00-005 |

---

## Technical Debt

| ID | Title | Priority | Related WI |
|----|-------|----------|------------|
| *None identified yet* | | | |

---

## References

| Document | Path | Purpose |
|----------|------|---------|
| ADR-PROJ003-001 | [decisions/ADR-PROJ003-001-agent-skill-cleanup-strategy.md](decisions/ADR-PROJ003-001-agent-skill-cleanup-strategy.md) | Migration strategy |
| Synthesis | [synthesis/proj-003-e-006-synthesis.md](synthesis/proj-003-e-006-synthesis.md) | Unified findings |
| Gap Analysis | [analysis/proj-003-e-005-gap-analysis.md](analysis/proj-003-e-005-gap-analysis.md) | 23 gaps identified |

---

## Status Legend

| Status | Meaning |
|--------|---------|
| PENDING | Not started |
| IN_PROGRESS | Currently being worked on |
| BLOCKED | Cannot proceed (see notes) |
| DONE | Completed and verified |

---

*This file is the index. See `work/wi-*.md` for detailed work items.*
