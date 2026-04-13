# BUG-012: pm-pmm agents write output to repo-root docs/pm-pmm/ instead of project-relative paths

> **Type:** bug
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Severity:** minor
> **Created:** 2026-04-13
> **Parent:** PROJ-030-bugs
> **Owner:** unassigned
> **Found In:** 0.30.0

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and scope |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the defect |
| [Root Cause Analysis](#root-cause-analysis) | Why the paths are wrong |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for resolution |

---

## Summary

All 5 pm-pmm agents (pm-business-analyst, pm-competitive-analyst, pm-customer-insight, pm-market-strategist, pm-product-strategist) hardcode output paths to `docs/pm-pmm/{artifact-type}/{slug}.md` — a repo-root location, not a project-relative `projects/${JERRY_PROJECT}/` path.

This is the same class of defect as BUG-006 (skill-internal output paths). The pm-pmm skill was contributed by another author and did not follow the established convention used by `/problem-solving` and the 32 agents remediated under BUG-006.

**Scope:** 5 agents, governance YAML + agent .md + SKILL.md files.

## Steps to Reproduce

1. Invoke any `/pm-pmm` agent (e.g., `pm-product-strategist`) on any project
2. Observe the agent writes output to `docs/pm-pmm/` at the repo root
3. Note this path is shared across all projects — multi-tenancy collision risk
4. Compare with `/problem-solving` or `/eng-team`: outputs go to `projects/${JERRY_PROJECT}/`

## Root Cause Analysis

The `/pm-pmm` skill was contributed separately and did not reference the `projects/${JERRY_PROJECT}/` convention established by `/problem-solving`. AD-M-011 (codified during BUG-006 remediation) now documents this as a MEDIUM standard, but the pm-pmm agents predate it.

**Related:** BUG-006 (same pattern, different skill family), ADR-output-path-resolution-001 (the protocol these agents should follow).

## Acceptance Criteria

- [ ] AC-1: All 5 pm-pmm governance YAML `output.location` fields use `projects/${JERRY_PROJECT}/` prefix
- [ ] AC-2: All 5 pm-pmm governance YAML files have `filename_pattern` field
- [ ] AC-3: All 5 pm-pmm agent .md files have Output Path Resolution section per ADR-output-path-resolution-001
- [ ] AC-4: pm-pmm SKILL.md agent table uses project-relative paths
- [ ] AC-5: Zero `grep -r 'docs/pm-pmm/' skills/pm-pmm/` matches in path-specifying contexts
