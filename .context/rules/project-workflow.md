# Project Workflow Rules

> Operational guidance for Jerry project-based work sessions.
> **SSOT:** `/worktracker` skill rules are the authoritative source for project structure, entity hierarchy, and worktracker integrity. This file provides session-start orientation and H-04 enforcement.

## Document Sections

| Section | Purpose |
|---------|---------|
| [HARD Rule Reference](#hard-rule-reference) | H-04 active project requirement |
| [GitHub Issue Parity](#github-issue-parity) | H-31 dual-tracking requirement |
| [Workflow Phases](#workflow-phases) | Before, during, after work |
| [Workflow Methodology (MEDIUM)](#workflow-methodology-medium) | Plan mode and structured workflow for C2+ work |
| [Project Orientation](#project-orientation) | Minimal structural context for session start |
| [Project Resolution](#project-resolution) | How to handle missing project context |

---

## HARD Rule Reference

> H-04: Active project REQUIRED. MUST NOT proceed without `JERRY_PROJECT` set -- doing so causes session work to be untracked, artifacts to land in incorrect paths, and worktracker integrity violations. Instead: set `JERRY_PROJECT` via the SessionStart hook or select a project using `jerry projects list`. See CLAUDE.md.

---

## GitHub Issue Parity

> **H-31:** When working in the Jerry repository (`geekatron/jerry`), all worktracker bugs, stories, enablers, and tasks MUST have a corresponding GitHub Issue. Worktracker is the internal SSOT; GitHub Issues are the external collaboration surface. Both MUST be kept in sync.

| Action | Worktracker | GitHub Issue |
|--------|------------|--------------|
| Create work item | Create entity file + update WORKTRACKER.md | `gh issue create` with matching title, link worktracker ID in body |
| Update status | Update entity file status field | Update issue labels or close issue |
| Close/Complete | Mark completed in entity file | `gh issue close` |
| Link | Add `GitHub Issue: [#N](url)` to Related Items | Add worktracker ID in issue body |

**Scope:** This rule applies only when the active repository is `geekatron/jerry` (the Jerry framework itself). Projects hosted in other repositories are not subject to this rule.

---

## Workflow Phases

| Phase | Actions |
|-------|---------|
| **Before** | Set `JERRY_PROJECT` env var. Check `PLAN.md`. Review `WORKTRACKER.md`. Read relevant `docs/knowledge/`. Invoke `/worktracker` for structural guidance. |
| **During** | Persist state to `WORKTRACKER.md` per WTI-001 through WTI-009. Update `PLAN.md`. Document decisions in `docs/design/`. |
| **After** | Update completion status. Capture learnings in `docs/experience/`. Commit with semantic messages. |

> **Integrity enforcement (HARD):** All worktracker operations MUST follow WTI-001 through WTI-009. See `skills/worktracker/rules/worktracker-behavior-rules.md` for full definitions.

---

## Workflow Methodology (MEDIUM)

> Override requires documented justification.

| ID | Standard | Guidance | Source |
|----|----------|----------|--------|
| PM-M-001 | For C2+ work, SHOULD follow the explore-plan-approve-implement-verify sequence. Plan mode SHOULD be used when: (a) 3+ files will be affected, (b) multiple valid implementation approaches exist, or (c) no explicit user plan has been provided. Plan mode is NOT needed for: single-file changes, obvious bug fixes, or when the user provides detailed implementation instructions. | This formalizes the structured workflow pattern recommended by Anthropic's Claude Code best practices. For multi-agent workflows, `/orchestration` provides the equivalent coordination; PM-M-001 covers the single-agent case where the main context manages the work directly. Plan mode enables the user to review and approve the approach before implementation begins, reducing wrong-direction work (H-31 alignment). | Anthropic Claude Code best practices, H-31 (ambiguity resolution) |

### PM-M-001 Decision Guide

| Condition | Use Plan Mode? | Rationale |
|-----------|---------------|-----------|
| C1 task, single file, clear instructions | No | Overhead exceeds benefit |
| C2 task, 3+ files, clear approach | Recommended | Confirms scope alignment |
| C2 task, multiple valid approaches | Yes | User selects preferred approach |
| C3+ task, any scope | Yes | High-impact work warrants explicit approval |
| User provided detailed step-by-step | No | User's plan serves as the approved plan |
| `/orchestration` is being invoked | No | Orchestration provides its own planning phase |

---

## Project Orientation

Projects follow `projects/PROJ-{NNN}-{slug}/` with `PLAN.md`, `WORKTRACKER.md`, and `work/` decomposition into Epics, Features, Enablers, Stories, and Tasks. This is the project-based placement pattern; a repository-based pattern also exists (see `skills/worktracker/rules/worktracker-directory-structure.md` for both).

> **Authoritative source:** `skills/worktracker/rules/worktracker-directory-structure.md` defines both placement patterns, the full directory hierarchy, naming conventions (`{EntityId}-{slug}`), and entity containment rules. `skills/worktracker/rules/worktracker-entity-hierarchy.md` defines entity types, classification, and parent-child constraints. Invoke `/worktracker` for full structural guidance.

---

## Project Resolution

When `<project-required>` or `<project-error>` is received from SessionStart hook:

1. Parse available projects from hook output.
2. Present options via AskUserQuestion (list projects + "Create new" option).
3. If existing: instruct user to set `JERRY_PROJECT`. Invoke `/worktracker` for structural guidance if needed.
4. If new: invoke `/worktracker` for structural guidance, then auto-generate ID using `PROJ-{NNN}-{slug}` format (next available number from `projects/README.md`), create directory structure per `skills/worktracker/rules/worktracker-directory-structure.md`, and update `projects/README.md`.

See `quality-enforcement.md` for decision criticality levels (C1-C4).
