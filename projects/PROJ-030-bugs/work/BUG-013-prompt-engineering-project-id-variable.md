# BUG-013: prompt-engineering agents use {PROJECT_ID} instead of ${JERRY_PROJECT} env var

> **Type:** bug
> **Status:** completed
> **Priority:** medium
> **Impact:** low
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
| [Root Cause Analysis](#root-cause-analysis) | Why the variable name differs |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for resolution |

---

## Summary

Two prompt-engineering agents (pe-builder, pe-constraint-gen) use `projects/{PROJECT_ID}/` in their governance YAML `output.location` instead of `projects/${JERRY_PROJECT}/`. The `{PROJECT_ID}` is a template placeholder that requires the caller to supply the project ID, whereas `${JERRY_PROJECT}` is the environment variable used by all other 68 output-producing agents.

This inconsistency means these agents cannot resolve their default output path (Priority 3) from the environment alone — they always require explicit caller input, breaking the P3 fallback that every other agent supports.

**Scope:** 2 agents (pe-builder, pe-constraint-gen), governance YAML + agent .md files.

## Steps to Reproduce

1. Set `JERRY_PROJECT=PROJ-030`
2. Invoke `pe-builder` without specifying an output path
3. Observe the agent cannot resolve `{PROJECT_ID}` from the environment — it's not `${JERRY_PROJECT}`
4. Compare with any `/problem-solving` agent: P3 default resolution works automatically

## Root Cause Analysis

The prompt-engineering agents were authored using a different variable naming convention (`{PROJECT_ID}`) instead of the established `${JERRY_PROJECT}` env var. This predates AD-M-011 which codifies the convention.

**Related:** ADR-output-path-resolution-001 (defines `${JERRY_PROJECT}` as the standard), AD-M-011 (MEDIUM standard requiring project-relative paths).

## Acceptance Criteria

- [x] AC-1: Both agents' governance YAML `output.location` use `projects/${JERRY_PROJECT}/` prefix
- [x] AC-2: Both agents' governance YAML files have `filename_pattern` field
- [x] AC-3: Both agents' .md files have Output Path Resolution section per ADR-output-path-resolution-001
- [x] AC-4: Zero `{PROJECT_ID}` references remain in prompt-engineering governance/agent files (replaced with `${JERRY_PROJECT}`)
