# FEAT-001: Claude Code Schema Validation Research and Refinement

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
PURPOSE: Significant deliverable containing Stories and Enablers for schema validation work
-->

> **Type:** feature
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-26T22:10:00Z
> **Due:**
> **Completed:**
> **Parent:** EPIC-001
> **Owner:** adam.nowak
> **Target Sprint:**

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Feature overview and value proposition |
| [Benefit Hypothesis](#benefit-hypothesis) | Expected benefits |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [MVP Definition](#mvp-definition) | Minimum viable scope |
| [Children Stories/Enablers](#children-storiesenablers) | Work decomposition |
| [Progress Summary](#progress-summary) | Overall progress |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## Summary

Research Anthropic's official Claude Code documentation, GitHub source, and community resources to discover the authoritative set of YAML frontmatter fields for both agent definitions (.md files) and skill definitions (SKILL.md files). Compare findings against existing Jerry schemas, identify gaps and inaccuracies, and produce refined JSON schemas validated through multi-skill review (security, UX, adversarial C4).

**Value Proposition:**
- Prevents agent/skill misconfiguration that causes silent runtime failures
- Enables CI-time validation of all 50+ agent definitions and 15+ skills
- Creates authoritative reference for agent developers (reduces onboarding friction)
- Security review ensures schema validation cannot be bypassed or exploited

---

## Benefit Hypothesis

**We believe that** creating authoritative, research-validated JSON schemas for Claude Code skill and agent definitions

**Will result in** reduced agent misconfiguration, faster developer onboarding, and CI-enforced definition quality

**We will know we have succeeded when** all existing agent and skill definitions validate against the refined schemas with zero false positives, and new definitions are caught by CI before reaching runtime

---

## Acceptance Criteria

### Definition of Done

- [x] Agent frontmatter schema validated against Anthropic's official documentation (STORY-001, STORY-003)
- [x] Skill frontmatter schema validated against Anthropic's official documentation (STORY-002, STORY-003)
- [x] Gap analysis completed documenting all differences between existing and official schemas (STORY-003)
- [x] Refined schemas pass security review (EN-001, STORY-020)
- [x] Developer experience reviewed (EN-002, STORY-019 DX review)
- [x] C4 adversarial review completed (STORY-004, STORY-015 ADR 0.950, STORY-017 0.954, STORY-020 0.953)
- [x] All existing agent definitions validate against refined schema (STORY-005, STORY-013 TASK-009: 611 tests pass)
- [x] All existing SKILL.md files validate against refined schema (STORY-005)

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Refined agent schema includes all fields documented by Anthropic as of March 2026 | [x] STORY-001 |
| AC-2 | Refined skill schema includes all fields documented by Anthropic as of March 2026 | [x] STORY-002 |
| AC-3 | Schema correctly rejects invalid field values (wrong enum, bad pattern, missing required) | [x] EN-003 |
| AC-4 | Schema correctly accepts all valid field combinations used in existing Jerry definitions | [x] STORY-005, STORY-013 |
| AC-5 | Research artifacts document sources with URLs and access dates | [x] STORY-001, STORY-002 |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Schema validation completes in < 1 second per file | [x] 611 tests in 11.24s = ~0.018s/file |
| NFC-2 | Error messages identify the specific field and constraint violated | [x] jsonschema.ValidationError includes path + message |
| NFC-3 | Schema uses JSON Schema Draft 2020-12 for consistency with existing schemas | [x] `$schema: https://json-schema.org/draft/2020-12/schema` |

---

## MVP Definition

### In Scope (MVP)

- Agent frontmatter schema (claude-code-frontmatter-v1.schema.json) refinement
- Skill frontmatter schema (claude-code-skill-frontmatter-v1.schema.json) refinement
- Research artifacts with source citations
- Security review findings
- C4 adversarial review

### Out of Scope (Future)

- Agent governance schema (agent-governance-v1.schema.json) — Jerry-specific, not Anthropic-sourced
- Automated CI validation pipeline (separate enabler)
- VS Code / IDE schema integration (separate feature)
- settings.json schema refinement (separate effort)

---

## Children Stories/Enablers

### Story/Enabler Inventory

| ID | Type | Title | Status | Priority | Effort |
|----|------|-------|--------|----------|--------|
| STORY-001 | Story | Research Anthropic Official Agent Definition Schema | completed | high | 5 |
| STORY-002 | Story | Research Anthropic Official Skill Definition Schema | completed | high | 5 |
| STORY-003 | Story | Gap Analysis and Schema Refinement | completed | high | 8 |
| STORY-004 | Story | Schema Remediation from C4 Review Findings | completed | high | 3 |
| STORY-005 | Story | Validate All Agent and Skill Definitions Against Schemas | completed | high | 3 |
| STORY-006 | Story | GitHub Issue Scan for Frontmatter Gotchas | completed | high | 3 |
| STORY-007 | Story | Update Task->Agent Tool Rename Across Rule Files | completed | high | 3 |
| STORY-008 | Story | Add Frontmatter Schema Validation to Jerry CLI | completed | high | 5 |
| STORY-009 | Story | Add Frontmatter Schema Validation to CI Pipeline | completed | high | 3 |
| STORY-010 | Story | Sync plugin.json Agents List with Actual Agent Files | completed | high | 5 |
| STORY-011 | Story | Adversary Sub-Agents: Add WebSearch/WebFetch/Context7 (GH #217) | completed | high | 5 |
| STORY-012 | Story | Audit Skills and Agents for Missing Web Tool Permissions | completed | high | 5 |
| STORY-013 | Story | Fix Tier/Tool Mismatches in Agent Definitions | completed | high | 5 |
| STORY-021 | Story | Add disallowedTools to Non-UX Workers (Defense-in-Depth) | wont_do | medium | 3 |
| STORY-022 | Story | Add Task->Agent CI Validation | completed | high | 1 |
| STORY-014 | Story | Fix Documentation Drift in Tool/Agent Standards | completed | medium | 3 |
| STORY-015 | Story | Evaluate and Renumber Tool Security Tier Model (ADR) | completed | high | 8 |
| STORY-016 | Story | Add Option E to Tier Model ADR | completed | high | 3 |
| STORY-017 | Story | Implement P0 Rule File Changes for Tier Renumbering | completed | high | 5 |
| STORY-018 | Story | Execute Governance YAML Migration (51 Files) | completed | high | 3 |
| STORY-019 | Story | Tier Model Documentation and Migration Guide | completed | medium | 5 |
| STORY-020 | Story | Security and Access Control Verification | completed | high | 3 |
| EN-001 | Enabler | Security Review of Schema Validation Pipeline | completed | high | 5 |
| EN-002 | Enabler | Developer Experience Review of Schema Validation | completed | medium | 3 |
| EN-003 | Enabler | Schema Validation Test Suite | completed | high | 5 |
| STORY-023 | Story | Remove Deprecated scripts/pre_tool_use.py (GH #177) | completed | medium | 1 |
| STORY-024 | Story | Consolidate Dual SubagentStop Hooks (GH #178) | completed | medium | 2 |
| STORY-025 | Story | Add jerry schema validate CLI Command (GH #193) | completed | medium | 2 |
| BUG-001 | Bug | Context Monitoring Tests Fail on 1M Context Window (GH #226) | completed | critical | 3 |
| BUG-002 | Bug | Pygments CVE-2026-4539 Blocks Git Push (GH #227) | completed | critical | 1 |
| BUG-003 | Bug | scripts/tests Isolation Failure (GH #228) | completed | high | 2 |
| BUG-004 | Bug | Fix Cross-Project Reference in ADR (GH #228) | completed | high | 1 |
| BUG-005 | Bug | Fix Hook Test Step Definitions (GH #214) | completed | high | 3 |
| BUG-006 | Bug | Fix file_repository.py Hardcoded Path Separator (GH #117) | completed | medium | 1 |
| BUG-007 | Bug | Fix Broken mkdocs Anchor Links (GH #213) | completed | high | 1 |
| EN-004 | Enabler | Memory-Keeper Collision Detection Enhancement | pending | medium | 5 |
| EN-005 | Enabler | Add .gitattributes Cross-Platform LF (GH #116) | completed | medium | 1 |

### Work Item Links

- [STORY-001: Research Anthropic Official Agent Definition Schema](./STORY-001-research-agent-schema/STORY-001-research-agent-schema.md)
- [STORY-002: Research Anthropic Official Skill Definition Schema](./STORY-002-research-skill-schema/STORY-002-research-skill-schema.md)
- [STORY-003: Gap Analysis and Schema Refinement](./STORY-003-gap-analysis-refinement/STORY-003-gap-analysis-refinement.md)
- [STORY-004: Schema Remediation from C4 Review Findings](./STORY-004-schema-remediation/STORY-004-schema-remediation.md)
- [STORY-005: Validate All Agent and Skill Definitions Against Schemas](./STORY-005-validate-all-definitions/STORY-005-validate-all-definitions.md)
- [STORY-006: GitHub Issue Scan for Frontmatter Gotchas](./STORY-006-github-issue-scan/STORY-006-github-issue-scan.md)
- [STORY-007: Update Task->Agent Tool Rename Across Rule Files](./STORY-007-task-to-agent-rename/STORY-007-task-to-agent-rename.md)
- [STORY-008: Add Frontmatter Schema Validation to Jerry CLI](./STORY-008-cli-validate-frontmatter/STORY-008-cli-validate-frontmatter.md)
- [STORY-009: Add Frontmatter Schema Validation to CI Pipeline](./STORY-009-ci-frontmatter-validation/STORY-009-ci-frontmatter-validation.md)
- [STORY-010: Sync plugin.json Agents List with Actual Agent Files](./STORY-010-plugin-json-agent-sync/STORY-010-plugin-json-agent-sync.md)
- [STORY-011: Adversary Sub-Agents WebSearch/WebFetch/Context7](./STORY-011-adversary-tool-access/STORY-011-adversary-tool-access.md)
- [STORY-012: Audit Skills and Agents for Missing Web Tool Permissions](./STORY-012-audit-web-tool-permissions/STORY-012-audit-web-tool-permissions.md)
- [STORY-013: Fix Tier/Tool Mismatches in Agent Definitions](./STORY-013-fix-tier-tool-mismatches/STORY-013-fix-tier-tool-mismatches.md)
- [STORY-021: Add disallowedTools to Non-UX Workers](./STORY-021-non-ux-disallowed-tools/STORY-021-non-ux-disallowed-tools.md)
- [STORY-022: Add Task->Agent CI Validation](./STORY-022-ci-task-agent-check/STORY-022-ci-task-agent-check.md)
- [STORY-014: Fix Documentation Drift in Tool/Agent Standards](./STORY-014-fix-documentation-drift/STORY-014-fix-documentation-drift.md)
- [STORY-015: Evaluate and Renumber Tool Security Tier Model](./STORY-015-tier-model-renumbering/STORY-015-tier-model-renumbering.md)
- [STORY-016: Add Option E to Tier Model ADR](./STORY-016-adr-option-e/STORY-016-adr-option-e.md)
- [STORY-017: Implement P0 Rule File Changes for Tier Renumbering](./STORY-017-rule-file-updates/STORY-017-rule-file-updates.md)
- [STORY-018: Execute Governance YAML Migration (51 Files)](./STORY-018-governance-yaml-migration/STORY-018-governance-yaml-migration.md)
- [STORY-019: Tier Model Documentation and Migration Guide](./STORY-019-documentation-migration-guide/STORY-019-documentation-migration-guide.md)
- [STORY-020: Security and Access Control Verification](./STORY-020-security-verification/STORY-020-security-verification.md)
- [EN-001: Security Review of Schema Validation Pipeline](./EN-001-security-review/EN-001-security-review.md)
- [EN-002: Developer Experience Review of Schema Validation](./EN-002-developer-experience-review/EN-002-developer-experience-review.md)
- [EN-003: Schema Validation Test Suite](./EN-003-validation-test-suite/EN-003-validation-test-suite.md)
- [BUG-001: Context Monitoring Tests Fail on 1M Context Window](./BUG-001-context-monitoring-1m/BUG-001-context-monitoring-1m.md)
- [BUG-002: Pygments CVE-2026-4539 Blocks Git Push](./BUG-002-pygments-cve/BUG-002-pygments-cve.md)
- [BUG-003: scripts/tests Isolation Failure](./BUG-003-scripts-tests-isolation/BUG-003-scripts-tests-isolation.md)
- [EN-004: Memory-Keeper Collision Detection Enhancement](./EN-004-mk-collision-detection/EN-004-mk-collision-detection.md)
- [EN-005: Add .gitattributes Cross-Platform LF (GH #116)](./EN-005-gitattributes/EN-005-gitattributes.md)
- [STORY-023: Remove Deprecated scripts/pre_tool_use.py (GH #177)](./STORY-023-remove-deprecated-hook/STORY-023-remove-deprecated-hook.md)
- [STORY-024: Consolidate Dual SubagentStop Hooks (GH #178)](./STORY-024-consolidate-subagent-hooks/STORY-024-consolidate-subagent-hooks.md)
- [STORY-025: Add jerry schema validate CLI Command (GH #193)](./STORY-025-schema-validate-cli/STORY-025-schema-validate-cli.md)
- [BUG-004: Fix Cross-Project Reference in ADR (GH #228)](./BUG-004-cross-project-ref/BUG-004-cross-project-ref.md)
- [BUG-005: Fix Hook Test Step Definitions (GH #214)](./BUG-005-hook-test-step-defs/BUG-005-hook-test-step-defs.md)
- [BUG-006: Fix file_repository.py Hardcoded Path Separator (GH #117)](./BUG-006-file-repo-path-sep/BUG-006-file-repo-path-sep.md)
- [BUG-007: Fix Broken mkdocs Anchor Links (GH #213)](./BUG-007-broken-mkdocs-anchors/BUG-007-broken-mkdocs-anchors.md)

---

## Progress Summary

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Stories:   [####################] 100% (23/23 completed)          |
| Enablers:  [################....] 80% (4/5 completed)             |
| Bugs:      [####################] 100% (7/7 completed)            |
+------------------------------------------------------------------+
| Overall:   [###################.] 97% (34/35 items)               |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Stories** | 23 |
| **Completed Stories** | 23 |
| **In Progress Stories** | 0 |
| **Pending Stories** | 0 |
| **Total Enablers** | 5 |
| **Completed Enablers** | 4 |
| **Pending Enablers** | 1 (EN-004) |
| **Total Bugs** | 7 |
| **Completed Bugs** | 7 |
| **Pending Bugs** | 0 |
| **Total Effort (points)** | 123 |
| **Completed Effort** | 118 |
| **Completion %** | 97% |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001: Claude Code Schema Validation](../EPIC-001-schema-validation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | Anthropic docs | Official Claude Code documentation must be accessible |
| Blocks | H-34 enforcement | Refined schemas needed for CI validation pipeline |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-26 | adam.nowak | in_progress | Feature created; STORY-001 and STORY-002 research launched in parallel |
| 2026-03-28 | claude | in_progress | STORY-015 through STORY-020 completed (tier model renumbering). EN-004 created (pending). 83% complete. |
| 2026-03-29 | claude | in_progress | STORY-011, STORY-013, STORY-014 closed out with delivery evidence. All 20 stories complete. All DoD + functional + non-functional criteria verified. 96% (23/24). Status remains in_progress: EN-004 (MK collision detection, non-blocking, FMEA RPN=105) is the sole remaining item. |
| 2026-03-30 | claude | in_progress | CI cleanup sprint: STORY-023/024/025 + BUG-001-007 + EN-005 completed with delivery evidence. All stories and bugs done. GH #117, #177, #178, #193, #213, #214, #226, #227, #228 closed. Sole remaining: EN-004 (MK collision detection). 97% (34/35). |
