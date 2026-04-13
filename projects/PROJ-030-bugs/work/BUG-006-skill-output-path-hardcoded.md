# BUG-006: Agent output paths hardcoded to skill directories — breaks end-user output persistence (#230)

> **Type:** bug
> **Status:** completed
> **Priority:** high
> **Impact:** critical
> **Severity:** major
> **Created:** 2026-03-31
> **Parent:** PROJ-030-bugs
> **Owner:** unassigned
> **Found In:** 0.30.0
> **GitHub Issue:** [#230](https://github.com/geekatron/jerry/issues/230)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and scope |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the defect |
| [Root Cause Analysis](#root-cause-analysis) | Why the paths are wrong |
| [Impact Assessment](#impact-assessment) | Scope across skills, agents, and files |
| [Affected Skills Detail](#affected-skills-detail) | Per-skill audit findings |
| [Correct Reference Architecture](#correct-reference-architecture) | Pattern from /problem-solving |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for resolution |
| [Implementation Plan](#implementation-plan) | Decomposed remediation tasks |
| [Related Items](#related-items) | Hierarchy, related issues, children |
| [History](#history) | Status changes and key events |

---

## Summary

Agent definitions in 3 skill families (eng-team, red-team, user-experience) hardcode output paths to `skills/{skill-name}/output/{engagement-id}/` instead of user project directories (`projects/${JERRY_PROJECT}/`). This causes:

1. **End users writing into framework directories** — skill dirs should be read-only; outputs belong in project workspaces
2. **Committed operational state** — `skills/eng-team/output/` contains 28 files (600K) of session artifacts that don't belong in the repo
3. **Multi-tenancy collision** — multiple projects using the same skill write to the same output directory
4. **Portability failure** — porting skills to another system carries stale engagement data

**Scope:** 13 affected skills, 107 config files requiring path updates (22 eng-team + 25 red-team + 60 UX, verified via `grep -rl 'skills/(eng-team|red-team|ux-.*|user-experience).*output' skills/`), 32 agents producing output to incorrect locations. Additionally, 3 governance files require updates (agent-development-standards.md, .gitignore, diataxis SKILL.md) per TASK-010, TASK-011, TASK-012.

---

## Steps to Reproduce

1. Invoke any `/eng-team` agent (e.g., `eng-architect`) on any project
2. Observe the agent writes output to `skills/eng-team/output/{engagement-id}/`
3. Note this path is inside the framework's skill directory, not the user's project directory
4. Verify: `ls skills/eng-team/output/` shows 28 committed artifacts from prior sessions
5. Compare with `/problem-solving`: `ps-researcher` correctly writes to `projects/${JERRY_PROJECT}/research/`

**Key Details:**
- **Symptom:** Agent outputs persist in skill directories instead of user project directories
- **Frequency:** Every invocation of affected agents (32 agents across 13 skills)
- **Workaround:** None — paths are hardcoded in agent governance YAML, composition YAML, SKILL.md, templates, and rules

---

## Root Cause Analysis

**Timeline of convention divergence:**

| Date | Commit | Event | Output Pattern |
|------|--------|-------|----------------|
| 2026-01-07 | `03e12674` | `/problem-solving` SKILL.md created (initial skills release) | `projects/${JERRY_PROJECT}/{output-type}/` (correct) |
| 2026-02-22 | `cf522abb` | `/eng-team` SKILL.md created (PROJ-010) | `skills/eng-team/output/{engagement-id}/` (incorrect) |
| 2026-02-24 | `ab827f3f` | `/red-team` canonical agent format added (PROJ-010) | `skills/red-team/output/{engagement-id}/` (incorrect) |
| 2026-03-04 | `53ec37b5` | `/user-experience` parent SKILL.md created (PROJ-022) | `skills/user-experience/output/{engagement-id}/` (incorrect) |
| 2026-03-04 | `12b5148a` | UX Wave 5 sub-skills added (PROJ-022) | All 10 sub-skills copied eng-team pattern |

The `/problem-solving` skill established the correct `projects/${JERRY_PROJECT}/` convention on 2026-01-07. When `/eng-team` was built 46 days later (PROJ-010, commit `cf522abb`), it introduced a new engagement-based output pattern (`skills/eng-team/output/`) without referencing the established convention. `/red-team` (same project, 2 days later) copied the eng-team pattern. `/user-experience` (PROJ-022, 10 days after red-team) propagated the anti-pattern to all 11 sub-skills.

**Contributing factors:**
- No MEDIUM standard in `agent-development-standards.md` requiring project-relative output paths (AC-6 addresses this)
- No `.gitignore` rule preventing `skills/*/output/` accumulation (AC-7 addresses this)
- No CI gate checking for hardcoded skill-internal output paths
- The engagement-ID concept (`GH-118`, `RED-0001`, `UX-0001`) was conflated with skill-internal directory organization rather than project-scoped organization
- PROJ-010 and PROJ-022 did not include an output path review against the existing `/problem-solving` convention

**Root cause classification:** Architectural debt — convention established in initial release, never enforced as a standard, never backported to later skill implementations.

---

## Impact Assessment

| Dimension | Impact |
|-----------|--------|
| **Skills affected** | 13 (eng-team, red-team, 11 UX sub-skills) |
| **Agents affected** | 32 (10 eng, 11 red, 11 UX) |
| **Files requiring updates** | 107 config files (22 eng-team + 25 red-team + 60 UX), verified via `grep -rl 'skills/(eng-team\|red-team\|ux-.*\|user-experience).*output' skills/` |
| **Committed stale artifacts** | 28 files, 600K in `skills/eng-team/output/` |
| **End-user impact** | All users of eng-team, red-team, and UX skills get outputs in wrong location |
| **Multi-tenancy** | Multiple projects collide in shared `skills/*/output/` directories |
| **Auto-escalation** | AE-002 (touches skill directories) — auto-C3 minimum |

### Skills NOT affected (correct pattern — reference architecture)

| Skill | Agent Count | Output Pattern |
|-------|-------------|----------------|
| /problem-solving | 9 | `projects/${JERRY_PROJECT}/{output-type}/{ps-id}-{entry-id}-{slug}.md` |
| /adversary | 3 | Project-relative |
| /orchestration | 3 | Project-relative |
| /transcript | 6 | Project-relative |
| /use-case | 2 | Project-relative |
| /test-spec | 2 | Project-relative |
| /contract-design | 2 | Project-relative |
| /worktracker | 3 | Project-relative |
| /prompt-engineering | 3 | Project-relative |
| /saucer-boy | 4 | Project-relative |
| /pm-pmm | 5 | Project-relative |

### Diataxis (minor — naming inconsistency only)

Uses correct `projects/${JERRY_PROJECT}/docs/` pattern but has plural/singular naming inconsistencies between SKILL.md and governance files (e.g., `howto/` vs `how-to/`, `explanations/` vs `explanation/`). Tracked as sub-task TASK-012.

---

## Affected Skills Detail

### eng-team (10 agents, 22 config files + 28 output files)

**Hardcoded path pattern:** `skills/eng-team/output/{engagement-id}/eng-{agent}-{topic-slug}.md`
**Full line-level audit:** [`BUG-006-eng-audit-detail.md`](../research/BUG-006-eng-audit-detail.md) (verified via `grep -rn 'skills/eng-team/output' skills/eng-team/`)

| File Category | Count | Files |
|---------------|-------|-------|
| SKILL.md | 1 | Lines 119-128 (agent table), 261-273 (P-002 section) |
| Agent governance | 10 | `skills/eng-team/agents/eng-*.governance.yaml` — `output.location` field |
| Agent composition | 10 | `skills/eng-team/composition/eng-*.agent.yaml` — `output.location` field |
| Templates | 1 | `skills/eng-team/templates/engagement-playbook.md` — Line 189 |

**Committed output files (28 files, 600K — to be removed per AC-2):**

| Engagement | Files | Content |
|------------|-------|---------|
| GH-118 | 6 | Adversarial scores, backend implementation |
| PORT-001 | 3 | Portability analysis, issue drafts |
| STORY-013-M007 | 10 | C4 scorer iterations, security reviews |
| STORY-022 | 9 | C4 scorer iterations, validation sweeps |

### red-team (11 agents, 25 config files)

**Hardcoded path pattern:** `skills/red-team/output/{engagement-id}/red-{agent}-{topic-slug}.md`
**Full line-level audit:** [`BUG-006-red-audit-detail.md`](../research/BUG-006-red-audit-detail.md) (verified via `grep -rn 'skills/red-team/output' skills/red-team/`)

| File Category | Count | Files |
|---------------|-------|-------|
| SKILL.md | 1 | Lines 106-116 (agent table), 188, 274, 521-528, 535 (examples, evidence) |
| Agent governance | 11 | `skills/red-team/agents/red-*.governance.yaml` — `output.location` field |
| Agent composition | 11 | `skills/red-team/composition/red-*.agent.yaml` — `output.location` field |
| Templates | 2 | `pentest-engagement.md` (Lines 151, 189-192), `engagement-playbook.md` (Line 81) |

**No output directory on disk** — the skill has not yet been used to produce outputs.

### user-experience (11 sub-skills, 60 config files — verified via `grep -rl`)

**Hardcoded path pattern:** `skills/ux-{sub-skill}/output/{engagement-id}/ux-{agent}-{topic-slug}.md`

| Sub-Skill | SKILL.md | Agent .md | Governance | Templates | Rules | Other |
|-----------|----------|-----------|------------|-----------|-------|-------|
| user-experience (parent) | yes | yes | yes | — | routing, wave-progression, CI checks, synthesis | — |
| ux-heuristic-eval | yes | yes | yes | 1 | MCP runbook | — |
| ux-jtbd | yes | yes | yes | 2 | — | — |
| ux-lean-ux | yes | yes | yes | 2 | MCP runbook, methodology | — |
| ux-heart-metrics | yes | yes | yes | — | — | — |
| ux-kano-model | yes | yes | yes | 2 | methodology | — |
| ux-atomic-design | yes | yes | yes | 1 | MCP runbook, design | — |
| ux-inclusive-design | yes | yes | yes | 2 | MCP runbook, design | — |
| ux-behavior-design | yes | yes | yes | 1 | behavior | — |
| ux-design-sprint | yes | yes | yes | — | sprint | — |
| ux-ai-first-design | yes | yes | yes | 1 | design | — |

**No output directories on disk** — the UX skills have not yet been used to produce outputs.

**Representative line-level citations (ux-heart-metrics as sample):**

| File | Lines | Hardcoded Path |
|------|-------|----------------|
| `skills/ux-heart-metrics/SKILL.md` | 152, 488, 717 | Agent table, output spec, P-002 compliance reference |
| `skills/ux-heart-metrics/agents/ux-heart-analyst.md` | 288, 405 | Output location, artifact path in handoff |
| `skills/ux-heart-metrics/agents/ux-heart-analyst.governance.yaml` | 50 | `output.location` field |

This pattern (SKILL.md + agent .md + governance .yaml) is consistent across all 11 UX sub-skills. Full line-level audit for all 11 sub-skills persisted at [`BUG-006-ux-audit-detail.md`](../research/BUG-006-ux-audit-detail.md) with per-file, per-line citations and a sum-check verification table (7+5+5+7+3+6+6+7+5+4+5 = 60).

---

## Correct Reference Architecture

The `/problem-solving` skill (9 agents) implements the correct pattern and serves as the reference:

```yaml
# From skills/problem-solving/composition/ps-researcher.agent.yaml
output:
  location: "projects/${JERRY_PROJECT}/research/{ps-id}-{entry-id}-{topic-slug}.md"
```

**Proposed pattern for engagement-based skills:**

```
# For engagement-based skills (eng-team, red-team, UX):
projects/${JERRY_PROJECT}/engagements/{engagement-id}/{agent}-{topic-slug}.md

# For evidence/artifacts:
projects/${JERRY_PROJECT}/engagements/{engagement-id}/evidence/{category}/

# For UX wave signoff files:
projects/${JERRY_PROJECT}/engagements/{engagement-id}/wave-signoff-{wave-N}.md
```

This preserves engagement-ID scoping while placing outputs in user project directories.

---

## Acceptance Criteria

- [x] AC-1: All `skills/*/output/` path references replaced with `projects/${JERRY_PROJECT}/` or engagement-relative paths
- [x] AC-2: `skills/eng-team/output/` directory and its 28 files removed from the repository
- [x] AC-3: No `output/` directories exist under any `skills/` folder
- [x] AC-4: All affected governance YAML files pass schema validation after path updates
- [x] AC-5: Diataxis SKILL.md plural/singular inconsistencies resolved to match governance files
- [x] AC-6: Output path convention documented in `agent-development-standards.md` as a MEDIUM standard
- [x] AC-7: `.gitignore` updated to prevent future `skills/*/output/` accumulation

---

## Implementation Plan

| Task | Scope | Files | Dependency |
|------|-------|-------|------------|
| TASK-006: eng-team path remediation | Replace all `skills/eng-team/output/` with project-relative paths | 22 config files | None |
| TASK-007: red-team path remediation | Replace all `skills/red-team/output/` with project-relative paths | 25 config files | None |
| TASK-008: UX skills path remediation | Replace all `skills/ux-*/output/` across 11 sub-skills | 60 config files | None |
| TASK-009: Remove committed eng-team outputs | Delete `skills/eng-team/output/` directory and 28 files | 28 files | TASK-006 |
| TASK-010: Add output path standard to agent-development-standards.md | New MEDIUM standard AD-M-011 | 1 file | TASK-006 through TASK-008 |
| TASK-011: Update .gitignore | Add `skills/*/output/` pattern | 1 file | None |
| TASK-012: Diataxis naming consistency | Fix plural/singular mismatches in SKILL.md | 1 file | None |

**Parallelization:** TASK-006, TASK-007, TASK-008, TASK-011, and TASK-012 can execute in parallel. TASK-009 depends on TASK-006. TASK-010 depends on completion of TASK-006 through TASK-008 (to validate the chosen path convention).

---

## Related Items

| Relationship | Item | Description |
|-------------|------|-------------|
| Parent | PROJ-030-bugs | Bug project |
| Related | [#192](https://github.com/geekatron/jerry/issues/192) | enhancement: configurable output base path for skill agents |
| Related | [#144](https://github.com/geekatron/jerry/issues/144) | feat(ux): Make UX skill output paths configurable |
| GitHub Issue | [#230](https://github.com/geekatron/jerry/issues/230) | This bug's external tracking |
| Children | [TASK-006](TASK-006-eng-team-path-remediation.md) | eng-team path remediation (22 files) |
| Children | [TASK-007](TASK-007-red-team-path-remediation.md) | red-team path remediation (25 files) |
| Children | [TASK-008](TASK-008-ux-skills-path-remediation.md) | UX skills path remediation (60 files) |
| Children | [TASK-009](TASK-009-remove-eng-team-outputs.md) | Remove committed eng-team/output/ (28 files) |
| Children | [TASK-010](TASK-010-output-path-standard.md) | Add output path standard to agent-development-standards.md |
| Children | [TASK-011](TASK-011-gitignore-skill-output.md) | Update .gitignore |
| Children | [TASK-012](TASK-012-diataxis-naming-consistency.md) | Fix diataxis naming inconsistencies |
| Audit Detail | [BUG-006-eng-audit-detail.md](../research/BUG-006-eng-audit-detail.md) | eng-team line-level audit (22 files, 10 agents) |
| Audit Detail | [BUG-006-red-audit-detail.md](../research/BUG-006-red-audit-detail.md) | red-team line-level audit (25 files, 11 agents) |
| Audit Detail | [BUG-006-ux-audit-detail.md](../research/BUG-006-ux-audit-detail.md) | UX line-level audit (60 files, 11 sub-skills) |

---

## History

| Date | Event |
|------|-------|
| 2026-03-31 | Bug identified during issue triage; codebase audit confirmed scope across 13 skills, 107 verified files |
| 2026-03-31 | Filed as BUG-006 in PROJ-030-bugs; GitHub Issue #230 created |
| 2026-03-31 | C4 adversarial review iter 1: 0.891 REVISE — gaps: root cause evidence, UX file count, UX line citations |
| 2026-03-31 | Revision: added commit-level root cause timeline (5 commits), verified UX file count (60 via `grep -rl`), added ux-heart-metrics line citations |
| 2026-03-31 | C4 adversarial review iter 2: 0.886 REVISE (regression) — two stale approximations (~68, ~112) not fully replaced |
| 2026-03-31 | Revision: replaced all stale approximations with verified counts; added history entries |
| 2026-03-31 | C4 adversarial review iter 3: 0.837 REVISE — Summary said 112 (included +5 governance), Impact said 107; TASK-007 said 22+ instead of 25 |
| 2026-03-31 | Revision: reconciled all counts to 107 config files + 3 governance files (explained separately); resolved 22+ to verified 25; added exact grep command |
| 2026-03-31 | C4 adversarial review iter 4: 0.900 REVISE — UX evidence not persisted (P-002); task entity files not created |
| 2026-03-31 | Revision: persisted UX audit detail (BUG-006-ux-audit-detail.md, 60 files, 11 sub-skills with line citations and sum-check); created 7 task entity files (TASK-006 through TASK-012); linked audit detail and task files in Related Items |
| 2026-03-31 | C4 adversarial review iter 5: 0.892 REVISE — WORKTRACKER TASK-007 row still "22+"; GH issue lacks H-32 back-link; eng/red audit detail not persisted |
| 2026-03-31 | Revision: fixed WORKTRACKER.md TASK-007 row to "25"; added worktracker back-link to GH issue; created BUG-006-eng-audit-detail.md (22 files) and BUG-006-red-audit-detail.md (25 files) with full line-level citations and sum-checks |
| 2026-04-01 | Phase 2 execution: all 9 tasks completed (TASK-015 schema, TASK-011 .gitignore, TASK-009 eng-team/output/ removal, TASK-006 eng-team 22 files, TASK-007 red-team 25 files, TASK-008 UX 60 files, TASK-012 diataxis naming, TASK-010 AD-M-011 standard). Verification: `grep -r 'skills/.*/output/' skills/` returns zero matches. AC-1 through AC-7 all satisfied. |
