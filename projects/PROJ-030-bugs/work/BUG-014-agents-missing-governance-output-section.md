# BUG-014: 12 agents produce file output but lack governance YAML output section

> **Type:** bug
> **Status:** completed
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
| [Affected Agents](#affected-agents) | Full list of 12 agents |
| [Root Cause Analysis](#root-cause-analysis) | Why governance is incomplete |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for resolution |

---

## Summary

12 agents across 4 skills produce file output (use Write tool, cite P-002 file persistence) but their `.governance.yaml` files lack a formal `output:` section with `required:`, `location:`, and `filename_pattern` fields. This means:

1. Schema validation cannot verify their output path conventions
2. They are invisible to automated output path compliance checks
3. New AD-M-011 standard cannot be enforced against them
4. The Unified Output Path Resolution Protocol (ADR-output-path-resolution-001) cannot be applied

## Steps to Reproduce

1. Read any affected agent's `.governance.yaml` (e.g., `skills/adversary/agents/adv-executor.governance.yaml`)
2. Note there is no `output:` section with `required: true` and `location:` fields
3. Read the agent's `.md` file — it references P-002 file persistence and uses the Write tool
4. The agent produces file output, but governance doesn't declare it

## Affected Agents

| Agent | Skill | Output Mechanism | Path Source |
|-------|-------|-----------------|-------------|
| adv-executor | adversary | Write tool, P-002 | Caller-provided `{output_path}` |
| adv-scorer | adversary | Write tool, P-002 | Caller-provided `{output_path}` |
| adv-selector | adversary | Write tool, P-002 | Caller-provided `{output_path}` |
| ts-parser | transcript | Write tool, P-002 | Caller-provided `{output_dir}` |
| ts-extractor | transcript | Write tool, P-002 | Caller-provided `{output_path}` |
| ts-formatter | transcript | Write tool, P-002 | Caller-provided `{output_directory}` |
| ts-mindmap-ascii | transcript | Write tool, P-002 | Caller-provided `{output_path}` |
| ts-mindmap-mermaid | transcript | Write tool, P-002 | Caller-provided `{output_path}` |
| sb-calibrator | saucer-boy-framework-voice | Write tool, P-002 | No path specification |
| sb-reviewer | saucer-boy-framework-voice | Write tool, P-002 | No path specification |
| sb-rewriter | saucer-boy-framework-voice | Write tool, P-002 | No path specification |
| wt-auditor | worktracker | Write tool, P-002 | `projects/${JERRY_PROJECT}/` in .md body |

## Root Cause Analysis

These agents were authored before or outside the governance schema conventions established by H-34 and AD-M-011. The adversary and transcript agents use a "caller-provides-path" pattern where the orchestrator supplies the output path — this works functionally but is undeclared in governance. The saucer-boy-framework-voice agents have no path specification at all.

**Related:** H-34 (agent definition standards), AD-M-011 (output path standard), ADR-output-path-resolution-001.

## Acceptance Criteria

- [x] AC-1: All 12 agents have `output:` section in `.governance.yaml` with `required: true/false`, `location:`, and `filename_pattern:` fields
- [x] AC-2: Agents that receive caller-provided paths declare `location:` using the caller-variable pattern (e.g., `{output_path}`) with documentation that the path is caller-provided
- [x] AC-3: Agents with no path specification (sb-calibrator, sb-reviewer, sb-rewriter) are evaluated — all 3 confirmed as producing persistent file output (Write tool in frontmatter, P-002 mandates in .md body), set `required: true` with caller-provided `{output_path}`
- [x] AC-4: All 12 agents pass YAML validation after updates
