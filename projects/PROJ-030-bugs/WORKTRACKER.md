# PROJ-030-bugs — Work Tracker

> Bug fixes and defect resolution for the Jerry Framework.

## Work Items

| ID | Type | Title | Status | Parent |
|----|------|-------|--------|--------|
| BUG-001 | Bug | Memory-keeper tool names mismatch across all governance files | completed | PROJ-030-bugs |
| BUG-002 | Bug | Version bump regex rejects uppercase scopes like GH-NNN | completed | PROJ-030-bugs |
| BUG-003 | Bug | version-bump workflow fails — uv.lock dirty after uv sync | completed | PROJ-030-bugs |
| EN-001 | Enabler | CI pipeline security hardening | in_progress | PROJ-030-bugs |
| TASK-003 | Task | Consolidate pre_tool_use.py into CLI enforcement pipeline (#150) | in_progress | EN-001 |
| TASK-004 | Task | Claude Code permission syntax reference (#179) | in_progress | PROJ-030-bugs |
| BUG-004 | Bug | settings.json uses undocumented field names (#180) | completed | PROJ-030-bugs |
| BUG-005 | Bug | Skill(jerry:name) permission pattern undocumented (#181) | completed | PROJ-030-bugs |
| TASK-005 | Task | Migrate deprecated Bash(:*) syntax (#182) | completed | PROJ-030-bugs |
| TASK-001 | Task | Create CHANGELOG.md and establish changelog process | completed | EN-001 |
| TASK-002 | Task | Document CI pipeline hardening changes using /diataxis | completed | EN-001 |
| BUG-006 | Bug | Agent output paths hardcoded to skill directories (#230) | pending | PROJ-030-bugs |
| TASK-006 | Task | eng-team path remediation (22 config files) | pending | BUG-006 |
| TASK-007 | Task | red-team path remediation (25 config files) | pending | BUG-006 |
| TASK-008 | Task | UX skills path remediation — 11 sub-skills (60 files) | pending | BUG-006 |
| TASK-009 | Task | Remove committed eng-team/output/ (28 files, 600K) | pending | BUG-006 |
| TASK-010 | Task | Add output path MEDIUM standard to agent-development-standards.md | pending | BUG-006 |
| TASK-011 | Task | Update .gitignore to prevent skills/*/output/ accumulation | pending | BUG-006 |
| TASK-012 | Task | Fix diataxis SKILL.md plural/singular naming inconsistencies | pending | BUG-006 |
| TASK-015 | Task | Add filename_pattern to agent-governance-v1.schema.json | pending | BUG-006 |
| BUG-007 | Bug | tspec-generator silently skips unrecognized extensions (#195) | completed | PROJ-030-bugs |
| BUG-008 | Bug | tspec-analyst uses live UC as coverage denominator (#197) | completed | PROJ-030-bugs |
| BUG-009 | Bug | tspec-analyst has no cross-slice aggregate coverage (#196) | completed | PROJ-030-bugs |
| BUG-010 | Bug | uc-slicer lacks duplicate slice_id conflict detection (#199) | completed | PROJ-030-bugs |
| BUG-011 | Bug | cd-generator banned-term false positives under 60 chars (#198) | completed | PROJ-030-bugs |

## Completed

| ID | Type | Title | Completed |
|----|------|-------|-----------|
