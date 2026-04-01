# Constructed Prompt: EPIC-002 Phase 2 Output Path Remediation

> **Type:** session-entry-prompt
> **Created:** 2026-03-31
> **Target Branch:** `feat/PROJ-024-tactical-work-2`
> **Criticality:** C4 (irreversible changes across 107 config files in 13 skills; touches governance schema and rule files; AE-002 auto-C3 minimum)

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Quick-Start Version](#l0-quick-start-version) | Minimal copy-paste prompt for immediate session use |
| [L1 Full Version](#l1-full-version) | Complete prompt with all constraints, quality gates, and verification steps |
| [Construction Notes](#construction-notes) | 5-element mapping and source traceability |
| [Self-Review Score](#self-review-score) | 7-criterion rubric assessment |

---

## L0 Quick-Start Version

Copy everything inside the fence below into a fresh Claude Code session on branch `feat/PROJ-024-tactical-work-2`.

~~~
Resume EPIC-002 Phase 2 (Output Path Remediation). This session executes the full phase.

Read these context files first:
1. docs/design/ADR-EPIC002-001-unified-output-path-resolution.md — sections: Migration Guide (Steps 0-5), Agent Integration Specification
2. projects/PROJ-024-tactical-work/work/EPIC-002-issue-triage-batch/EPIC-002-issue-triage-batch.md — sections: Work Items, Dependency Graph, Execution Phases
3. projects/PROJ-030-bugs/work/BUG-006-skill-output-path-hardcoded.md — sections: Acceptance Criteria (AC-1 through AC-7)
4. projects/PROJ-030-bugs/research/BUG-006-eng-audit-detail.md — 22 files with line numbers
5. projects/PROJ-030-bugs/research/BUG-006-red-audit-detail.md — 25 files with line numbers
6. projects/PROJ-030-bugs/research/BUG-006-ux-audit-detail.md — 60 files with line numbers per sub-skill

Execute 9 tasks in dependency order per the EPIC-002 dependency graph:
  Phase 2-pre: TASK-015 (governance schema)
  Phase 2a:    TASK-011 (.gitignore) + TASK-009 (delete eng-team/output/)
  Phase 2b:    TASK-006 (eng, 22 files) + TASK-007 (red, 25 files) + TASK-008 (UX, 60 files) + TASK-012 (diataxis)
  Phase 2c:    TASK-010 (AD-M-011 standard)

Read each task's worktracker entity (projects/PROJ-030-bugs/work/TASK-{NNN}-*.md) for acceptance criteria before starting it.

Use /worktracker to update EPIC-002 Work Items table and PROJ-030 WORKTRACKER.md as each task completes.
Use /eng-team domain knowledge when editing eng-team skill files.
Use /user-experience domain knowledge when editing UX skill files.
Quality threshold: >= 0.95
Run /adversary C4 tournament (all 10 strategies) on the completed migration before marking BUG-006 resolved.

Final verification: `grep -r 'skills/.*/output/' skills/` returns zero matches after all tasks complete.
Output format: in-place file edits across skills/ directories; markdown table status updates in EPIC-002 and PROJ-030 WORKTRACKER.md; one commit per task for atomicity.
~~~

---

## L1 Full Version

Copy everything inside the fence below into a fresh Claude Code session on branch `feat/PROJ-024-tactical-work-2`.

~~~
## SESSION OBJECTIVE

Execute EPIC-002 Phase 2 (Output Path Remediation) — implement ADR-EPIC002-001 Unified Output Path Resolution Protocol across 107 config files in 13 skills. This session handles all 9 Phase 2 tasks in dependency order.

## CONTEXT LOADING (read all before starting work)

Read the following files in order. These provide the migration specification, coordination state, and line-level audit citations:

1. **ADR (migration spec):** `docs/design/ADR-EPIC002-001-unified-output-path-resolution.md`
   - Sections needed: Migration Guide (Steps 0-5), Agent Integration Specification, Verification
2. **Coordination epic:** `projects/PROJ-024-tactical-work/work/EPIC-002-issue-triage-batch/EPIC-002-issue-triage-batch.md`
   - Sections needed: Work Items table, Dependency Graph, Execution Phases (Phase 2)
3. **Parent bug:** `projects/PROJ-030-bugs/work/BUG-006-skill-output-path-hardcoded.md`
   - Sections needed: Acceptance Criteria (AC-1 through AC-7), Implementation Plan
4. **eng-team audit:** `projects/PROJ-030-bugs/research/BUG-006-eng-audit-detail.md`
   - Contains: 22 file paths with line numbers for every `skills/eng-team/output/` reference
5. **red-team audit:** `projects/PROJ-030-bugs/research/BUG-006-red-audit-detail.md`
   - Contains: 25 file paths with line numbers for every `skills/red-team/output/` reference
6. **UX audit:** `projects/PROJ-030-bugs/research/BUG-006-ux-audit-detail.md`
   - Contains: 60 file paths organized by sub-skill with line numbers for every `skills/ux-*/output/` reference

## SKILL ROUTING

- Use `/worktracker` for status tracking: update EPIC-002 Work Items table and PROJ-030 WORKTRACKER.md as each task transitions to `in_progress` then `completed`
- Use `/eng-team` domain knowledge when editing `skills/eng-team/` files (TASK-006) — understand the engagement playbook structure, agent roles, and composition YAML format
- Use `/user-experience` domain knowledge when editing `skills/user-experience/` and `skills/ux-*/` files (TASK-008) — understand wave progression, routing rules, CI checks, and sub-skill orchestration
- Direct file editing (Read, Grep, Edit, Write, Bash) for the migration work itself

## EXECUTION PLAN — DEPENDENCY ORDER

Execute tasks strictly in this order. Within a phase, tasks can be done in any order.

### Phase 2-pre: Schema Update (MUST complete first)

**TASK-015: Add `filename_pattern` to governance schema**
- Worktracker entity: `projects/PROJ-030-bugs/work/TASK-015-governance-schema-filename-pattern.md`
- File: `docs/schemas/agent-governance-v1.schema.json`
- Action: Add `filename_pattern` as optional string field to the `output` object properties (see ADR Step 6 diff)
- Verify: Field is type `string` with description; field is NOT in `required` array; schema is valid JSON Schema Draft 2020-12
- After: Run `uv run jerry schema validate` to confirm existing agents still pass

### Phase 2a: Prep (parallel within phase; both must complete before Phase 2b)

**TASK-011: Update .gitignore**
- Worktracker entity: `projects/PROJ-030-bugs/work/TASK-011-gitignore-skill-output.md`
- File: `.gitignore`
- Action: Add `skills/*/output/` pattern with explanatory comment
- Verify: `git check-ignore skills/eng-team/output/test.md` confirms pattern works

**TASK-009: Remove committed eng-team/output/ directory**
- Worktracker entity: `projects/PROJ-030-bugs/work/TASK-009-remove-eng-team-outputs.md`
- Action: `git rm -r skills/eng-team/output/` to remove 28 files (600K)
- Verify: `git ls-files skills/eng-team/output/` returns empty; no remaining references to these specific files in other documents

### Phase 2b: Path Remediation (parallel within phase; all must complete before Phase 2c)

For each skill family, follow ADR-EPIC002-001 Migration Guide Steps 1-4 in order:
- Step 1: Governance YAML — replace `output.location`, add `output.filename_pattern`
- Step 2: Agent .md definitions — add Output Path Resolution section to `<output>` block
- Step 3: SKILL.md and rules files — update agent tables, examples, P-002 sections
- Step 4: Templates — update engagement playbooks and template files

**TASK-006: eng-team (22 files)**
- Worktracker entity: `projects/PROJ-030-bugs/work/TASK-006-eng-team-path-remediation.md`
- Audit reference: `projects/PROJ-030-bugs/research/BUG-006-eng-audit-detail.md`
- Scope: 10 governance YAML + 10 composition YAML + 1 SKILL.md + 1 template
- Pattern: `skills/eng-team/output/{engagement-id}/` becomes `projects/${JERRY_PROJECT}/engagements/{engagement-id}/`
- Verify: `grep -r 'skills/eng-team/output' skills/eng-team/` returns zero matches; all 10 governance YAML have `output.filename_pattern`; all 10 agent .md have Output Path Resolution section

**TASK-007: red-team (25 files)**
- Worktracker entity: `projects/PROJ-030-bugs/work/TASK-007-red-team-path-remediation.md`
- Audit reference: `projects/PROJ-030-bugs/research/BUG-006-red-audit-detail.md`
- Scope: 11 governance YAML + 11 composition YAML + 1 SKILL.md + 2 templates
- Pattern: `skills/red-team/output/{engagement-id}/` becomes `projects/${JERRY_PROJECT}/engagements/{engagement-id}/`
- Verify: `grep -r 'skills/red-team/output' skills/red-team/` returns zero matches; all 11 governance YAML have `output.filename_pattern`; all 11 agent .md have Output Path Resolution section; both template files updated

**TASK-008: UX skills (60 files across 11 sub-skills)**
- Worktracker entity: `projects/PROJ-030-bugs/work/TASK-008-ux-skills-path-remediation.md`
- Audit reference: `projects/PROJ-030-bugs/research/BUG-006-ux-audit-detail.md`
- Scope: 11 governance YAML + 11 agent .md + 11 SKILL.md + 12 templates + 15 rules files
- Pattern: `skills/ux-*/output/{engagement-id}/` and `skills/user-experience/output/{engagement-id}/` become `projects/${JERRY_PROJECT}/engagements/{engagement-id}/`
- UX-specific concerns: wave signoff paths in `ux-routing-rules.md` and `wave-progression.md`; CI check rules in `ci-checks.md`; synthesis report paths in `synthesis-validation.md`; engagement ID pattern `UX-{NNNN}` preserved
- Verify: `grep -rl 'skills/ux-.*output\|skills/user-experience.*output' skills/ux-*/ skills/user-experience/` returns zero matches; all 11 governance YAML have `output.filename_pattern`; all 11 agent .md have Output Path Resolution section

**TASK-012: Diataxis naming consistency**
- Worktracker entity: `projects/PROJ-030-bugs/work/TASK-012-diataxis-naming-consistency.md`
- File: `skills/diataxis/SKILL.md`
- Action: Fix `docs/howto/` to `docs/how-to/` and `docs/explanations/` to `docs/explanation/` (governance files are canonical)
- Verify: SKILL.md output paths match governance YAML `output.location` fields exactly

### Phase 2c: Standards Codification (after Phase 2b complete)

**TASK-010: Add AD-M-011 standard**
- Worktracker entity: `projects/PROJ-030-bugs/work/TASK-010-output-path-standard.md`
- File: `.context/rules/agent-development-standards.md`
- Action: Insert AD-M-011 into Agent Structure Standards table after AD-M-010 (text provided in task entity)
- AE-002 auto-escalation applies (touches `.context/rules/`)
- Verify: AD-M-011 exists with SHOULD/SHOULD NOT language; references ADR-EPIC002-001 and `/problem-solving`

## TASK ACCEPTANCE CRITERIA (SUMMARY)

| Task | Key AC | Verification Command |
|------|--------|---------------------|
| TASK-015 | `filename_pattern` exists as optional string in schema `output` properties | `uv run jerry schema validate` (existing agents still pass) |
| TASK-011 | `.gitignore` contains `skills/*/output/` with comment | `git check-ignore skills/eng-team/output/test.md` |
| TASK-009 | `skills/eng-team/output/` dir and 28 files removed from repo | `git ls-files skills/eng-team/output/` returns empty |
| TASK-006 | 10 governance YAML have `filename_pattern`; 10 agent .md have Output Path Resolution section; SKILL.md + template updated | `grep -r 'skills/eng-team/output' skills/eng-team/` returns 0 |
| TASK-007 | 11 governance YAML have `filename_pattern`; 11 agent .md have Output Path Resolution section; SKILL.md + 2 templates updated | `grep -r 'skills/red-team/output' skills/red-team/` returns 0 |
| TASK-008 | 11 governance YAML have `filename_pattern`; 11 agent .md have Output Path Resolution section; 11 SKILL.md + 12 templates + 15 rules updated; wave signoff paths updated | `grep -rl 'skills/ux-.*output\|skills/user-experience.*output' skills/ux-*/ skills/user-experience/` returns 0 |
| TASK-012 | SKILL.md `howto/` → `how-to/`; `explanations/` → `explanation/` | SKILL.md paths match governance YAML `output.location` |
| TASK-010 | AD-M-011 in agent-development-standards.md with SHOULD language; refs ADR + /problem-solving | Read `.context/rules/agent-development-standards.md` |

## STATUS TRACKING PROTOCOL

For each task:
1. Read the task's worktracker entity file for acceptance criteria
2. Update EPIC-002 Work Items table: set task status to `in_progress`
3. Execute the task following the ADR migration guide
4. Verify against all acceptance criteria listed in the task entity
5. Update EPIC-002 Work Items table: set task status to `completed`
6. Update PROJ-030 WORKTRACKER.md to reflect the status change
7. After all tasks: update BUG-006 status to `completed` when AC-1 through AC-7 are satisfied; update EPIC-002 Phase 2 status in Progress Summary to `completed`

## QUALITY GATE

After completing all 9 tasks and before marking BUG-006 resolved:

1. Run comprehensive verification:
   - `grep -r 'skills/.*/output/' skills/` — MUST return zero matches
   - `uv run jerry schema validate` — all governance YAML files pass
   - `git ls-files skills/eng-team/output/` — empty
   - `git check-ignore skills/eng-team/output/test.md` — confirmed
2. Run `/adversary` C4 tournament review on the completed migration:
   - Quality threshold: >= 0.95
   - Review scope: ADR compliance across all 3 skill families
   - Verification dimensions: path correctness, schema compliance, Output Path Resolution section completeness, template accuracy, rules file consistency
   - All 10 adversarial strategies applied per C4 criticality level

## CONSTRAINTS

NEVER edit agent `.md` frontmatter fields that are not `output`-related -- Consequence: unrelated frontmatter changes create review noise and risk breaking Claude Code agent discovery. Instead: restrict edits to `<output>` sections in agent `.md` body and `output.*` fields in governance/composition YAML.

NEVER modify `/problem-solving` agent files -- Consequence: these agents already implement the correct pattern and serve as reference architecture; changes break backward compatibility (DC-7). Instead: use `/problem-solving` agents as the reference for how the Output Path Resolution section should read.

NEVER proceed to Phase 2b before TASK-015 schema update is complete and validated -- Consequence: governance YAML files with `filename_pattern` will fail schema validation if the schema has not been updated first. Instead: complete and validate TASK-015, then proceed.

NEVER proceed to TASK-010 (AD-M-011 standard) before TASK-006, TASK-007, and TASK-008 are all complete -- Consequence: codifying the standard before validating the implementation pattern across all 3 skill families risks encoding an untested convention. Instead: complete all path remediations first, verify the pattern works, then codify.

NEVER create new output directories under `skills/` -- Consequence: recreates the anti-pattern being fixed (BUG-006). Instead: all agent output paths resolve to `projects/${JERRY_PROJECT}/` per the ADR resolution protocol.

## COMMIT STRATEGY

Commit per-skill for atomicity and rollback safety per ADR Migration Risk Assessment:
1. `fix(schema): add filename_pattern to agent-governance-v1.schema.json` (TASK-015)
2. `chore: add skills/*/output/ to .gitignore` (TASK-011)
3. `chore: remove committed eng-team/output/ directory (28 files)` (TASK-009)
4. `fix(eng-team): migrate output paths to project-relative per ADR-EPIC002-001` (TASK-006)
5. `fix(red-team): migrate output paths to project-relative per ADR-EPIC002-001` (TASK-007)
6. `fix(ux): migrate output paths to project-relative per ADR-EPIC002-001` (TASK-008)
7. `fix(diataxis): resolve plural/singular naming inconsistencies` (TASK-012)
8. `docs: add AD-M-011 output path resolution standard` (TASK-010)
~~~

---

## Construction Notes

| Element | Value | Source |
|---------|-------|--------|
| Skill Routing | `/worktracker` (status tracking) + `/eng-team` (domain knowledge for eng files) + `/user-experience` (domain knowledge for UX files) + `/adversary` C4 (quality gate) + direct file editing | Trigger map: "status tracking" -> `/worktracker`; eng-team/UX file editing benefits from skill domain knowledge; C4 quality gate requires `/adversary` |
| Domain Scope | 107 config files across 13 skills (22 eng + 25 red + 60 UX), 9 tasks (TASK-015, TASK-011, TASK-009, TASK-006, TASK-007, TASK-008, TASK-012, TASK-010), BUG-006 parent bug, ADR-EPIC002-001 protocol | EPIC-002 Work Items table + BUG-006 Impact Assessment (verified file counts) |
| Data Source | ADR-EPIC002-001 Migration Guide (Steps 0-5), 3 line-level audit files (eng/red/UX with per-file line numbers), 9 task entity files with acceptance criteria | All artifacts persisted in `docs/design/` and `projects/PROJ-030-bugs/` |
| Quality Gate | `/adversary` C4 tournament, threshold >= 0.95, all 10 strategies, verification dimensions named | C4 criticality: irreversible changes across 107 files, touches governance schema and rule files; threshold 0.95 per security-level quality (AE-002 auto-C3, elevated to C4 given scope) |
| Output Path | In-place edits across `skills/` directories; worktracker updates in `projects/PROJ-024-tactical-work/` and `projects/PROJ-030-bugs/`; AD-M-011 in `.context/rules/agent-development-standards.md` | Output is migration-in-place, not a new artifact; locations determined by source file locations |

---

## Self-Review Score

| Criterion | Weight | Score | Notes |
|-----------|--------|-------|-------|
| C1 Task Specificity | 20% | 3/3 | All 9 tasks named with specific file counts, dependency order, and per-task acceptance criteria. Zero undefined terms. All clauses complete. |
| C2 Skill Routing | 18% | 3/3 | `/worktracker`, `/eng-team`, `/user-experience`, `/adversary` all invoked with specific purposes. Direct file editing tools named. |
| C3 Context Provision | 15% | 3/3 | 6 context files listed with repo-relative paths and section-level specificity. 3 audit detail files provide line-level citations. Task entity files referenced for acceptance criteria. |
| C4 Quality Specification | 15% | 3/3 | Numeric threshold (0.95) + named mechanism (`/adversary` C4 tournament) + verification dimensions + comprehensive grep-based verification commands. |
| C5 Decomposition | 12% | 3/3 | 4 sub-phases (2-pre, 2a, 2b, 2c) with dependency barriers. 9 named tasks with explicit ordering. Commit strategy per-task. Status tracking protocol. |
| C6 Output Specification | 12% | 3/3 | All output locations specified (in-place edits across `skills/`, worktracker updates in `projects/`, AD-M-011 in `.context/rules/`). Per-task verification commands. Commit message formats. |
| C7 Positive Framing | 8% | 3/3 | All 5 constraints use NPT-013 format (NEVER + consequence + Instead). Main body uses positive directives throughout. |
| **Weighted Composite** | | **100/100** | |

**Scoring formula applied:**
- C1: (3/3) x 20 = 20.0
- C2: (3/3) x 18 = 18.0
- C3: (3/3) x 15 = 15.0
- C4: (3/3) x 15 = 15.0
- C5: (3/3) x 12 = 12.0
- C6: (3/3) x 12 = 12.0
- C7: (3/3) x 8 = 8.0
- **Total: 100.0/100 (Exemplary)**

---

*Constructed by pe-builder v1.0.0 | Template: adapted Multi-Skill Orchestration (Template 3) for migration-in-place work | Criticality: C4 | Date: 2026-03-31*
