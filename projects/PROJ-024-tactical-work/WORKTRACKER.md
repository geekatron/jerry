# PROJ-024-tactical-work -- Work Tracker

> Tactical work items -- small improvements, quick fixes, and miscellaneous tasks.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Work Items](#work-items) | Open items (pending / in_progress) with parent lineage |
| [Completed](#completed) | Terminal-state items with completion dates and parent lineage |

## Work Items

| ID | Type | Title | Status | Parent |
|----|------|-------|--------|--------|
| EPIC-001 | Epic | Claude Code Schema Validation | in_progress | PROJ-024 |
| FEAT-001 | Feature | Claude Code Schema Validation Research and Refinement | in_progress | EPIC-001 |
| EN-004 | Enabler | Memory-Keeper Collision Detection Enhancement | pending | FEAT-001 |
| EPIC-004 | Epic | Dependency Security-Scan Pipeline Hardening | in_progress | PROJ-024 |
| FEAT-002 | Feature | Security-scan pipeline hardening | in_progress | EPIC-004 |
| EN-007 | Enabler | Dependency security-scan pipeline hardening (6/7 ACs done; open solely pending STORY-028's alerting criterion) | in_progress | FEAT-002 |
| STORY-028 | Story | Add owner alerting via an auto-managed rolling GitHub issue (verified 60% — AC-4 failed, AC-2/AC-3 unproven) | in_progress | FEAT-002 |
| BUG-009 | Bug | click 8.3.1 transitive command injection — fix delivered on branch (click>=8.3.3, resolves 8.4.2); completion pending merge to main + green scan (#336) | in_progress | FEAT-002 |

## Completed

> Note: Discoveries use `validated` as their terminal state (per DISCOVERY template); they are listed here as completed-equivalent. STORY-021 closed as `wont_do` — annotated in its title, closure date in the Completed column.

| ID | Type | Title | Parent | Completed |
|----|------|-------|--------|-----------|
| STORY-001 | Story | Research Anthropic Official Agent Definition Schema | FEAT-001 | 2026-03-26 |
| STORY-002 | Story | Research Anthropic Official Skill Definition Schema | FEAT-001 | 2026-03-26 |
| STORY-003 | Story | Gap Analysis and Schema Refinement | FEAT-001 | 2026-03-26 |
| STORY-004 | Story | Schema Remediation from C4 Review Findings | FEAT-001 | 2026-03-27 |
| STORY-005 | Story | Validate All Agent and Skill Definitions Against Schemas | FEAT-001 | 2026-03-27 |
| STORY-006 | Story | GitHub Issue Scan for Frontmatter Gotchas | FEAT-001 | 2026-03-27 |
| STORY-007 | Story | Update Task->Agent Tool Rename Across Rule Files | FEAT-001 | 2026-03-27 |
| STORY-008 | Story | Add Frontmatter Schema Validation to Jerry CLI | FEAT-001 | 2026-03-27 |
| STORY-009 | Story | Add Frontmatter Schema Validation to CI Pipeline | FEAT-001 | 2026-03-27 |
| STORY-010 | Story | Sync plugin.json Agents List with Actual Agent Files | FEAT-001 | 2026-03-27 |
| STORY-012 | Story | Audit Skills and Agents for Missing Web Tool Permissions | FEAT-001 | 2026-03-27 |
| EN-001 | Enabler | Security Review of Schema Validation Pipeline | FEAT-001 | 2026-03-26 |
| EN-002 | Enabler | Developer Experience Review of Schema Validation | FEAT-001 | 2026-03-26 |
| EN-003 | Enabler | Schema Validation Test Suite | FEAT-001 | 2026-03-27 |
| STORY-015 | Story | Evaluate and Renumber Tool Security Tier Model (ADR, C4 0.953 PASS) | FEAT-001 | 2026-03-28 |
| STORY-016 | Story | Add Option E to Tier Model ADR (C4 0.950 PASS) | FEAT-001 | 2026-03-28 |
| STORY-017 | Story | Implement P0 Rule File Changes for Tier Renumbering (C4 0.954 PASS) | FEAT-001 | 2026-03-28 |
| STORY-018 | Story | Execute Governance YAML Migration (51 Files, T1=4 T2=28 T3=2 T4=54 T5=1) | FEAT-001 | 2026-03-28 |
| STORY-019 | Story | Tier Model Documentation and Migration Guide (38 ref updates + 2 new docs) | FEAT-001 | 2026-03-28 |
| STORY-020 | Story | Security and Access Control Verification (C4 0.953 PASS) | FEAT-001 | 2026-03-28 |
| STORY-011 | Story | Adversary Sub-Agents: WebSearch/WebFetch/Context7 (GH #217) | FEAT-001 | 2026-03-29 |
| STORY-013 | Story | Fix Tier/Tool Mismatches in Agent Definitions (M-007 C4 0.954 PASS) | FEAT-001 | 2026-03-29 |
| TASK-001 | Task | Fix M-001 -- nse-reporter Add WebSearch | STORY-013 | 2026-03-29 |
| TASK-002 | Task | Fix M-002 -- diataxis-explanation Upgrade to T3 | STORY-013 | 2026-03-29 |
| TASK-003 | Task | Fix M-003 -- ux-behavior-diagnostician Governance T2->T3 | STORY-013 | 2026-03-29 |
| TASK-004 | Task | Fix M-004 -- nse-requirements Tier Resolution | STORY-013 | 2026-03-29 |
| TASK-005 | Task | Fix M-005 -- orchestration Agents Add Web Tools | STORY-013 | 2026-03-29 |
| TASK-006 | Task | Fix M-006 -- pm-pmm SKILL.md Add allowed-tools | STORY-013 | 2026-03-29 |
| TASK-007 | Task | Fix M-007 -- 6 UX Worker Agents Add disallowedTools: Agent | STORY-013 | 2026-03-29 |
| TASK-008 | Task | Fix M-008 -- ux-heart-analyst + ux-kano-analyst Upgrade to T3 | STORY-013 | 2026-03-29 |
| TASK-009 | Task | Run Validation Suite After All Fixes | STORY-013 | 2026-03-29 |
| STORY-021 | Story | Add disallowedTools: [Agent] to Non-UX Worker Agents (Defense-in-Depth) (wont_do) | FEAT-001 | 2026-03-29 |
| STORY-022 | Story | Add Task->Agent CI Validation (C4 0.949 PASS) | FEAT-001 | 2026-03-29 |
| DISC-001 | Discovery | disallowedTools Redundancy When tools Explicitly Declared | STORY-013 | 2026-03-29 |
| STORY-014 | Story | Fix Documentation Drift in Tool/Agent Standards (D-001 + D-002) | FEAT-001 | 2026-03-29 |
| BUG-001 | Bug | Context Monitoring Tests Fail on 1M Context Window (GH #226) | FEAT-001 | 2026-03-30 |
| BUG-002 | Bug | Pygments CVE-2026-4539 Blocks Git Push (GH #227) | FEAT-001 | 2026-03-30 |
| BUG-003 | Bug | scripts/tests Isolation Failure (GH #228) | FEAT-001 | 2026-03-30 |
| BUG-004 | Bug | Fix Cross-Project Reference in ADR | FEAT-001 | 2026-03-30 |
| BUG-005 | Bug | Fix Hook Test Step Definitions (GH #214) | FEAT-001 | 2026-03-30 |
| BUG-006 | Bug | Fix file_repository.py Hardcoded Path Separator (GH #117) | FEAT-001 | 2026-03-30 |
| BUG-007 | Bug | Fix Broken mkdocs Anchor Links (GH #213) | FEAT-001 | 2026-03-30 |
| STORY-023 | Story | Remove Deprecated scripts/pre_tool_use.py (GH #177) | FEAT-001 | 2026-03-30 |
| STORY-024 | Story | Consolidate Dual SubagentStop Hooks (GH #178) | FEAT-001 | 2026-03-30 |
| STORY-025 | Story | Add jerry schema validate CLI Command (GH #193) | FEAT-001 | 2026-03-30 |
| EN-005 | Enabler | Add .gitattributes Cross-Platform LF (GH #116) | FEAT-001 | 2026-03-30 |
| EPIC-002 | Epic | Issue Triage Batch — UC Pipeline Bugs, Output Paths, Quick Wins | PROJ-024 | 2026-04-13 |
| EN-008 | Enabler | Issue Triage Quick Wins (retroactive container; GH #200 + #53) | EPIC-002 | 2026-03-31 |
| TASK-013 | Task | use-case SKILL.md missing Activity 5 entry (#200) | EN-008 | 2026-03-31 |
| TASK-014 | Task | Orchestration scaffold cartesian product dirs (#53) | EN-008 | 2026-03-31 |
| EPIC-003 | Epic | CI Pipeline Optimization — Remove Pip Matrix, Fix Supply Chain Gaps, Consolidate Jobs (GH #252) | PROJ-024 | 2026-04-16 |
| EN-009 | Enabler | CI Pipeline Optimization Tasks (retroactive container; GH #252) | EPIC-003 | 2026-04-15 |
| TASK-016 | Task | Remove pip test matrix (8 jobs) | EN-009 | 2026-04-13 |
| TASK-017 | Task | Migrate lint, type-check, security to uv | EN-009 | 2026-04-13 |
| TASK-018 | Task | Fix pip-audit to scan full dependency tree | EN-009 | 2026-04-13 |
| TASK-019 | Task | Consolidate 6 validation jobs into 1 | EN-009 | 2026-04-13 |
| TASK-020 | Task | Merge lint + type-check into static-analysis | EN-009 | 2026-04-13 |
| TASK-021 | Task | Scope pull-requests:write to coverage-report only | EN-009 | 2026-04-13 |
| TASK-022 | Task | Restrict push trigger to protected branches only | EN-009 | 2026-04-13 |
| EN-006 | Enabler | Supply Chain Hardening — Post-EPIC-003 Residual Risks (GH #252) | EPIC-003 | 2026-04-16 |
| TASK-023 | Task | Supply chain audit (eng-devsecops + red-recon) | EN-006 | 2026-04-16 |
| TASK-024 | Task | Pin pre-commit hooks to SHAs | EN-006 | 2026-04-16 |
| TASK-025 | Task | Add SLSA build provenance to release pipeline | EN-006 | 2026-04-16 |
| TASK-026 | Task | Fix pip-audit coverage gap in scheduled scan | EN-006 | 2026-04-16 |
| TASK-027 | Task | Evaluate replacing MishaKav coverage comment action | EN-006 | 2026-04-16 |
| TASK-028 | Task | Evaluate replacing softprops release action with gh CLI | EN-006 | 2026-04-16 |
| TASK-029 | Task | Add SBOM generation to release pipeline | EN-006 | 2026-04-16 |
| TASK-030 | Task | Track bump-my-version in Dependabot or scheduled check | EN-006 | 2026-04-16 |
| TASK-031 | Task | Remove unused security-events:write from security-scan | EN-006 | 2026-04-16 |
| TASK-032 | Task | Add CODEOWNERS for workflow files | EN-006 | 2026-04-16 |
| TASK-033 | Task | Evaluate docs.yml deploy-pages migration | EN-006 | 2026-04-16 |
| TASK-034 | Task | Add Dependabot pre-commit ecosystem entry | EN-006 | 2026-04-16 |
| BUG-008 | Bug | Scheduled security scan is false-green — audits only the local project, misses all transitive CVEs | FEAT-002 | 2026-08-05 |
| STORY-026 | Story | Unify CI + scheduled security audit into one shared composite action (DRY) | FEAT-002 | 2026-08-05 |
| STORY-027 | Story | Add owner-governed CVE accept-list with mandatory expiry/re-review | FEAT-002 | 2026-08-05 |
| STORY-029 | Story | Fix the silent-failure guard to verify a meaningful audit (not just non-empty output) | FEAT-002 | 2026-08-05 |
| STORY-030 | Story | Remediate the 9 current transitive CVEs (mako→1.3.12, urllib3→2.7.0, msgpack→1.2.1, pydantic-settings→2.14.2, pip→26.1.2) | FEAT-002 | 2026-08-05 |
| TASK-035 | Task | Confirm Dependabot security updates + vulnerability alerts enabled in repo Settings — owner enabled alerts/malware alerts/security updates; alerts API-confirmed | EN-007 | 2026-08-05 |
