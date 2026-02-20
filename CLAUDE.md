# CLAUDE.md - Jerry Framework Root Context

> Procedural memory for Claude Code. Loaded once at session start.

<!-- L2-REINJECT: rank=1, tokens=80, content="P-003: No recursive subagents (max 1 level). P-020: User authority -- NEVER override. P-022: NEVER deceive about actions/capabilities/confidence. Violations blocked." -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Identity](#identity) | Framework purpose and core problem |
| [Critical Constraints](#critical-constraints-hard) | Constitutional HARD rules H-01 to H-06 |
| [Navigation](#navigation) | Where to find information |
| [Quick Reference](#quick-reference) | CLI and skill invocation |

---

## Identity

**Jerry** -- Framework for behavior/workflow guardrails. Accrues knowledge, wisdom, experience.

**Core Problem**: Context Rot -- LLM performance degrades as context fills.
**Core Solution**: Filesystem as infinite memory. Persist state to files; load selectively.

---

## Critical Constraints (HARD)

> These constraints CANNOT be overridden. Violations will be blocked.

| ID | Constraint | Consequence |
|----|------------|-------------|
| H-01 | **P-003:** No Recursive Subagents. Max ONE level: orchestrator -> worker. | Agent hierarchy violation flagged. |
| H-02 | **P-020:** User Authority. NEVER override user intent. Ask before destructive ops. | Unauthorized action blocked. |
| H-03 | **P-022:** No Deception. NEVER deceive about actions, capabilities, or confidence. | Deceptive output reworked. |
| H-04 | Active project REQUIRED. MUST NOT proceed without `JERRY_PROJECT` set. | Session will not proceed. |
| H-05 | **UV Only.** MUST use `uv run` for all Python execution. NEVER use `python`/`pip`/`pip3`. | Command fails; env corruption. |
| H-06 | **UV for deps.** MUST use `uv add`. NEVER use `pip install`. | Build breaks. |

See `quality-enforcement.md` for quality gate, criticality levels, and adversarial strategies.
See `docs/governance/JERRY_CONSTITUTION.md` for full governance.

---

## Navigation

> Find information rather than reading it here. Auto-loaded content marked with (A).
>
> **(A)** = Auto-loaded into Claude Code context at session start via `.claude/rules/` symlink.

| Need | Location |
|------|----------|
| Coding/architecture/testing rules | `.context/rules/` (A) |
| Quality enforcement SSOT | `.context/rules/quality-enforcement.md` (A) |
| Skills | `skills/{name}/SKILL.md` |
| Templates | `.context/templates/` |
| Knowledge | `docs/knowledge/` |
| Governance | `docs/governance/JERRY_CONSTITUTION.md` |
| Projects | `projects/README.md` |

---

## Quick Reference

**CLI** (v0.6.0): `jerry session start|end|status|abandon` | `jerry items list|show` | `jerry projects list|context|validate`

**Skills** (invoke proactively per H-22):

| Skill | Purpose |
|-------|---------|
| `/worktracker` | Task/issue management |
| `/problem-solving` | Research, analysis, root cause |
| `/nasa-se` | Requirements, V&V, reviews |
| `/orchestration` | Multi-phase workflows |
| `/architecture` | Design decisions |
| `/adversary` | Adversarial quality reviews, strategy templates, tournament execution, multi-strategy orchestration |
| `/saucer-boy` | Session conversational voice, McConkey personality |
| `/saucer-boy-framework-voice` | Internal: framework output voice quality gate, persona compliance |
| `/transcript` | Transcription parsing |

**SessionStart Hook Tags:**

| Tag | Action |
|-----|--------|
| `<project-context>` | Proceed with work |
| `<project-required>` | Use AskUserQuestion to select/create project |
| `<project-error>` | Help user fix or select valid project |
