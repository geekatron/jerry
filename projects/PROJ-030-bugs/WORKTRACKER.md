# PROJ-030-bugs — Work Tracker

> Bug fixes and defect resolution for the Jerry Framework.

## Work Items

| ID | Type | Title | Status | Parent |
|----|------|-------|--------|--------|
| EN-001 | Enabler | CI pipeline security hardening | in_progress | PROJ-030-bugs |
| TASK-003 | Task | Consolidate pre_tool_use.py into CLI enforcement pipeline (#150) | in_progress | EN-001 |
| TASK-004 | Task | Claude Code permission syntax reference (#179) | in_progress | PROJ-030-bugs |
| BUG-006 | Bug | statusLine command uses python3 which fails on Windows (#113) | pending | PROJ-030-bugs |
| BUG-007 | Bug | file_repository.py uses hardcoded forward slash instead of pathlib (#117) | pending | PROJ-030-bugs |
| BUG-008 | Bug | Replace /tmp with tempfile.gettempdir() in docstring examples (#119) | pending | PROJ-030-bugs |
| BUG-009 | Bug | tspec-generator silently skips extensions with unrecognized outcome values (#195) | pending | PROJ-030-bugs |
| BUG-010 | Bug | tspec-analyst has no cross-slice aggregate coverage mechanism (#196) | pending | PROJ-030-bugs |
| BUG-011 | Bug | tspec-analyst uses live UC as coverage denominator instead of snapshot (#197) | pending | PROJ-030-bugs |
| BUG-012 | Bug | cd-generator banned-term check false positives on domain vocabulary (#198) | pending | PROJ-030-bugs |
| BUG-013 | Bug | uc-slicer append-only re-invocation lacks duplicate slice_id detection (#199) | pending | PROJ-030-bugs |

## Completed

| ID | Type | Title | Completed |
|----|------|-------|-----------|
| BUG-001 | Bug | Memory-keeper tool names mismatch across all governance files | 2026-03-02 |
| BUG-002 | Bug | Version bump regex rejects uppercase scopes like GH-NNN | 2026-03-09 |
| BUG-003 | Bug | version-bump workflow fails — uv.lock dirty after uv sync | 2026-03-09 |
| BUG-004 | Bug | settings.json uses undocumented field names (#180) | 2026-03-14 |
| BUG-005 | Bug | Skill(jerry:name) permission pattern undocumented (#181) | 2026-03-14 |
| TASK-001 | Task | Create CHANGELOG.md and establish changelog process | 2026-03-10 |
| TASK-002 | Task | Document CI pipeline hardening changes using /diataxis | 2026-03-10 |
| TASK-005 | Task | Migrate deprecated Bash(:*) syntax (#182) | 2026-03-14 |
