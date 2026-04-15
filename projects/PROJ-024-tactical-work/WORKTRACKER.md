# PROJ-024-tactical-work -- Work Tracker

> Tactical work items -- small improvements, quick fixes, and miscellaneous tasks.

## Work Items

| ID | Type | Title | Status | Parent |
|----|------|-------|--------|--------|
| EPIC-001 | Epic | Claude Code Schema Validation | in_progress | PROJ-024 |
| FEAT-001 | Feature | Claude Code Schema Validation Research and Refinement | in_progress | EPIC-001 |
| EN-004 | Enabler | Memory-Keeper Collision Detection Enhancement | pending | FEAT-001 |
| EPIC-002 | Epic | Issue Triage Batch — UC Pipeline Bugs, Output Paths, Quick Wins | in_progress | PROJ-024 |
| TASK-013 | Task | use-case SKILL.md missing Activity 5 entry (#200) | completed | EPIC-002 |
| TASK-014 | Task | Orchestration scaffold cartesian product dirs (#53) | completed | EPIC-002 |
| EPIC-003 | Epic | CI Pipeline Optimization — Remove Pip Matrix, Fix Supply Chain Gaps, Consolidate Jobs | in_progress | PROJ-024 |
| TASK-016 | Task | Remove pip test matrix (8 jobs) | completed | EPIC-003 |
| TASK-017 | Task | Migrate lint, type-check, security to uv | completed | EPIC-003 |
| TASK-018 | Task | Fix pip-audit to scan full dependency tree | completed | EPIC-003 |
| TASK-019 | Task | Consolidate 6 validation jobs into 1 | completed | EPIC-003 |
| TASK-020 | Task | Merge lint + type-check into static-analysis | completed | EPIC-003 |
| TASK-021 | Task | Scope pull-requests:write to coverage-report only | completed | EPIC-003 |
| TASK-022 | Task | Restrict push trigger to protected branches only | completed | EPIC-003 |
| EN-006 | Enabler | Supply Chain Hardening — Post-EPIC-003 Residual Risks | in_progress | EPIC-003 |
| TASK-023 | Task | Supply chain audit (eng-devsecops + red-recon) | completed | EN-006 |
| TASK-024 | Task | Pin pre-commit hooks to SHAs | pending | EN-006 |
| TASK-025 | Task | Add SLSA build provenance to release pipeline | pending | EN-006 |
| TASK-026 | Task | Fix pip-audit coverage gap in scheduled scan | pending | EN-006 |
| TASK-027 | Task | Evaluate replacing MishaKav coverage comment action | pending | EN-006 |
| TASK-028 | Task | Evaluate replacing softprops release action with gh CLI | pending | EN-006 |
| TASK-029 | Task | Add SBOM generation to release pipeline | pending | EN-006 |
| TASK-030 | Task | Track bump-my-version in Dependabot or scheduled check | pending | EN-006 |
| TASK-031 | Task | Remove unused security-events:write from security-scan | pending | EN-006 |
| TASK-032 | Task | Add CODEOWNERS for workflow files | pending | EN-006 |
| TASK-033 | Task | Evaluate docs.yml deploy-pages migration | pending | EN-006 |
| TASK-034 | Task | Add Dependabot pre-commit ecosystem entry | pending | EN-006 |

## Completed

| ID | Type | Title | Completed |
|----|------|-------|-----------|
| STORY-001 | Story | Research Anthropic Official Agent Definition Schema | 2026-03-26 |
| STORY-002 | Story | Research Anthropic Official Skill Definition Schema | 2026-03-26 |
| STORY-003 | Story | Gap Analysis and Schema Refinement | 2026-03-26 |
| STORY-004 | Story | Schema Remediation from C4 Review Findings | 2026-03-27 |
| STORY-005 | Story | Validate All Agent and Skill Definitions Against Schemas | 2026-03-27 |
| STORY-006 | Story | GitHub Issue Scan for Frontmatter Gotchas | 2026-03-27 |
| STORY-007 | Story | Update Task->Agent Tool Rename Across Rule Files | 2026-03-27 |
| STORY-008 | Story | Add Frontmatter Schema Validation to Jerry CLI | 2026-03-27 |
| STORY-009 | Story | Add Frontmatter Schema Validation to CI Pipeline | 2026-03-27 |
| STORY-010 | Story | Sync plugin.json Agents List with Actual Agent Files | 2026-03-27 |
| STORY-012 | Story | Audit Skills and Agents for Missing Web Tool Permissions | 2026-03-27 |
| EN-001 | Enabler | Security Review of Schema Validation Pipeline | 2026-03-26 |
| EN-002 | Enabler | Developer Experience Review of Schema Validation | 2026-03-26 |
| STORY-015 | Story | Evaluate and Renumber Tool Security Tier Model (ADR, C4 0.953 PASS) | 2026-03-28 |
| STORY-016 | Story | Add Option E to Tier Model ADR (C4 0.950 PASS) | 2026-03-28 |
| STORY-017 | Story | Implement P0 Rule File Changes for Tier Renumbering (C4 0.954 PASS) | 2026-03-28 |
| STORY-018 | Story | Execute Governance YAML Migration (51 Files, T1=4 T2=28 T3=2 T4=54 T5=1) | 2026-03-28 |
| STORY-019 | Story | Tier Model Documentation and Migration Guide (38 ref updates + 2 new docs) | 2026-03-28 |
| STORY-020 | Story | Security and Access Control Verification (C4 0.953 PASS) | 2026-03-28 |
| STORY-011 | Story | Adversary Sub-Agents: WebSearch/WebFetch/Context7 (GH #217) | 2026-03-29 |
| STORY-013 | Story | Fix Tier/Tool Mismatches in Agent Definitions (M-007 C4 0.954 PASS) | 2026-03-29 |
| STORY-021 | Story | Add disallowedTools: [Agent] to Non-UX Worker Agents (Defense-in-Depth) | wont_do |
| STORY-022 | Story | Add Task->Agent CI Validation (C4 0.949 PASS) | 2026-03-29 |
| DISC-001 | Discovery | disallowedTools Redundancy When tools Explicitly Declared | 2026-03-29 |
| STORY-014 | Story | Fix Documentation Drift in Tool/Agent Standards (D-001 + D-002) | 2026-03-29 |
| EN-003 | Enabler | Schema Validation Test Suite | 2026-03-27 |
| BUG-004 | Bug | Fix Cross-Project Reference in ADR (GH #228) | 2026-03-30 |
| BUG-006 | Bug | Fix file_repository.py Hardcoded Path Separator (GH #117) | 2026-03-30 |
| STORY-023 | Story | Remove Deprecated scripts/pre_tool_use.py (GH #177) | 2026-03-30 |
| STORY-024 | Story | Consolidate Dual SubagentStop Hooks (GH #178) | 2026-03-30 |
| BUG-005 | Bug | Fix Hook Test Step Definitions (GH #214) | 2026-03-30 |
| STORY-025 | Story | Add jerry schema validate CLI Command (GH #193) | 2026-03-30 |
| BUG-007 | Bug | Fix Broken mkdocs Anchor Links (GH #213) | 2026-03-30 |
| EN-005 | Enabler | Add .gitattributes Cross-Platform LF (GH #116) | 2026-03-30 |
