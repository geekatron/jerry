# Constructed Prompt: CI Cleanup -- Script Removal and CLI Consolidation (v2)

> **pe-builder** output | Project: PROJ-024 | Criticality: C4 (>10 files, multi-skill, 7 skills including tournament mode, irreversible script deletions)
> Template: 3 (Multi-Skill Orchestration) adapted for 4-phase sequential implementation with per-phase 7-skill quality gates.
> **v2 change:** Previous version (v1, scored 93/100) dropped 4 of 7 user-requested skills (/eng-team, /red-team, /nasa-se, /user-experience, /diataxis). This is an H-02 violation. v2 routes ALL 7 skills per user directive.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Quick-Start Version](#l0-quick-start-version) | Minimal prompt with all 5 elements |
| [L1 Full Version](#l1-full-version) | Complete copy-paste prompt with all 7 skills routed per phase |
| [Construction Notes](#construction-notes) | Element traceability |
| [Self-Review Score](#self-review-score) | 7-criterion rubric evaluation |

---

## L0 Quick-Start Version

```
Execute 4 worktracker items in dependency order under PROJ-024.

Phase 1 -- STORY-023 (GH #177): Remove deprecated scripts/pre_tool_use.py.
Phase 2 -- STORY-024 (GH #178): Consolidate dual SubagentStop hooks into CLI.
Phase 3 -- BUG-005 (GH #214): Rewrite hook tests from scripts/tests/ to tests/.
Phase 4 -- STORY-025 (GH #193): Port scripts/validate-agent-frontmatter.py P-003 check into CLI handler, resolve H-10.

Use /orchestration to sequence all 4 phases.
Use /problem-solving (ps-investigator, ps-analyst, ps-reviewer) for implementation per phase.
Use /eng-team (eng-security, eng-lead, eng-reviewer) for security and standards review per phase.
Use /red-team (red-vuln) for bypass path assessment per phase.
Use /nasa-se (nse-verification, nse-requirements) for AC validation and traceability per phase.
Use /user-experience (ux-heuristic-evaluator) for CLI DX evaluation on Phases 2 and 4.
Use /diataxis (diataxis-how-to-writer) for CLI reference documentation on Phase 4.
Use /adversary C4 tournament mode >= 0.95 per phase before proceeding.
Run full test suite after each phase; baseline = 16,341 passing tests.

Output: commit per phase; worktracker entity status updated to completed.
```

---

## L1 Full Version

Copy-paste the entire block below into a fresh Claude Code session.

---

```
Set JERRY_PROJECT=PROJ-024-tactical-work.

Use /worktracker to update STORY-023, STORY-024, BUG-005, and STORY-025 status to in-progress.

Use /orchestration with orch-planner to sequence the following 4-phase pipeline.
Each phase has a hard dependency on the previous phase completing successfully.
Proceed to the next phase ONLY after: (a) all acceptance criteria pass per /nasa-se
verification, (b) full test suite passes with count >= 16,341, (c) /eng-team
eng-reviewer approves refactored code, and (d) /adversary C4 quality gate >= 0.95.

---

## Skills Routed Per Phase

| Skill | Agents | Role | Phases Active |
|-------|--------|------|---------------|
| /orchestration | orch-planner | Sequence 4-phase pipeline, enforce phase gates | All |
| /problem-solving | ps-investigator, ps-analyst, ps-reviewer | Dead code verification, consolidation strategy, code review | All |
| /eng-team | eng-security, eng-lead, eng-reviewer | CWE/OWASP compliance, coding standards, final quality gate | All |
| /red-team | red-vuln | Bypass path assessment for migration gaps | All |
| /nasa-se | nse-verification, nse-requirements | AC validation, requirements traceability | All |
| /user-experience | ux-heuristic-evaluator | CLI error messages, exit codes, help text DX evaluation | 2, 4 |
| /diataxis | diataxis-how-to-writer | Reference documentation for consolidated CLI commands | 4 |
| /adversary | adv-selector, adv-executor, adv-scorer | C4 tournament mode, all 10 strategies, >= 0.95 | All |

---

## Constraints (apply to ALL phases)

NEVER introduce new standalone scripts in scripts/ -- Consequence: increases
surface area, creates parallel code paths that drift from CLI. Instead: all logic
goes through `uv run jerry ...` CLI commands.

NEVER put enforcement logic outside src/ hexagonal layers -- Consequence: bypasses
domain/application/infrastructure boundaries, breaks testability. Instead: domain
rules in domain layer, command handling in application layer, adapters in
infrastructure layer.

NEVER write implementation before the test fails -- Consequence: untested code, no
regression guard. Instead: Red (write failing test for CLI behavior) -> Green
(implement/port) -> Refactor (delete old code).

NEVER add tests to scripts/tests/ -- Consequence: parallel test infrastructure,
not collected by CI unless special config. Instead: all tests in tests/ directory
following existing test pyramid.

NEVER merge with fewer passing tests than baseline (16,341) -- Consequence:
regression introduced. Instead: run full suite via `uv run pytest tests/` after
each phase, verify count >= baseline.

---

## Phase 1 -- STORY-023: Remove Deprecated scripts/pre_tool_use.py (GH #177)

### Implementation (/problem-solving)

Use /problem-solving with ps-investigator to verify scripts/pre_tool_use.py is
dead code. Confirm all security guardrail logic already exists in
src/infrastructure/internal/enforcement/security_enforcement_engine.py.

Data sources:
- Deprecated script: scripts/pre_tool_use.py
- CLI enforcement: src/infrastructure/internal/enforcement/security_enforcement_engine.py
- Worktracker entity: projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/STORY-023-remove-deprecated-hook/STORY-023-remove-deprecated-hook.md

Steps:
1. Read scripts/pre_tool_use.py and catalog every security check it performs.
2. Read src/infrastructure/internal/enforcement/security_enforcement_engine.py and
   verify each cataloged check has a corresponding implementation.
3. If any check is missing from the CLI implementation, port it using TDD (H-20):
   write failing test in tests/ first, then implement in src/.
4. Delete scripts/pre_tool_use.py.
5. Use Grep to find all references to pre_tool_use.py or the old script path
   across the entire repository (docs, configs, rule files, CLAUDE.md, .claude/).
   Update every reference to point to the CLI command.
6. Update scripts/tests/test_hooks.py: remove or comment out tests that import
   or invoke the deleted script (full rewrite happens in Phase 3).
7. Run `uv run pytest tests/ -v` and verify count >= 16,341.

### Security Review (/eng-team)

Use /eng-team with eng-security to review the ported enforcement logic in
src/infrastructure/internal/enforcement/security_enforcement_engine.py for
CWE/OWASP compliance. Verify the migration from standalone script to CLI
handler preserves all security properties.

Use /eng-team with eng-lead to verify the refactored code follows coding
standards (H-11 type hints, docstrings, naming conventions).

Evaluation dimensions: CWE-78 (OS command injection), CWE-22 (path traversal),
OWASP input validation, security check completeness parity.

### Bypass Assessment (/red-team)

Use /red-team with red-vuln to assess whether removing scripts/pre_tool_use.py
introduces any bypass paths. Verify that the CLI-based enforcement
(jerry hooks pre-tool-use) provides equivalent or stronger gating than the
deleted standalone script.

Evaluation dimensions: enforcement bypass via direct tool invocation,
race conditions between hook removal and CLI enforcement, configuration
drift that could disable the CLI hook.

### AC Verification (/nasa-se)

Use /nasa-se with nse-verification to validate each acceptance criterion in the
STORY-023 worktracker entity is satisfied by the implementation.

Use /nasa-se with nse-requirements to trace each AC back to the worktracker
entity and confirm bidirectional traceability (AC -> implementation -> test).

### Quality Gate (/adversary + /eng-team)

Use /adversary with adv-selector to select C4 strategy set, then adv-executor
to run all 10 strategies in tournament mode against Phase 1 output.
Use adv-scorer to score with 6-dimension rubric.
Quality threshold: >= 0.95.

Evaluation dimensions: completeness of reference cleanup, no dangling imports,
no broken CI steps, security parity between old script and CLI,
CWE/OWASP compliance of ported logic.

Use /eng-team with eng-reviewer as the final quality gate. eng-reviewer approves
the refactored code before Phase 1 is marked complete.

Use /worktracker to update STORY-023 status to completed upon passing all gates.
Commit with message: "fix(hooks): remove deprecated scripts/pre_tool_use.py (STORY-023, GH #177)"

---

## Phase 2 -- STORY-024: Consolidate Dual SubagentStop Hooks (GH #178)

### Implementation (/problem-solving)

Use /problem-solving with ps-analyst to analyze the dual SubagentStop
implementations and identify consolidation strategy.

Data sources:
- Standalone hook: scripts/subagent_stop.py
- CLI implementation: search src/ for SubagentStop or subagent_stop references
- Worktracker entity: projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/STORY-024-consolidate-subagent-hooks/STORY-024-consolidate-subagent-hooks.md

Steps:
1. Read scripts/subagent_stop.py and catalog all hook behaviors.
2. Use Grep to find the CLI-side SubagentStop implementation in src/.
3. Diff the two implementations: identify any logic in the standalone script
   that is absent from the CLI version.
4. If any logic is missing from CLI, port it using TDD (H-20):
   write failing test in tests/ first, then implement in src/.
5. Delete scripts/subagent_stop.py.
6. Use Grep to find all references to subagent_stop.py across the repository.
   Update every reference to point to the CLI command.
7. Update .claude/settings.json and .claude/settings.local.json if they
   reference the standalone script path.
8. Run `uv run pytest tests/ -v` and verify count >= 16,341.

### Security Review (/eng-team)

Use /eng-team with eng-security to review the consolidated SubagentStop
implementation for CWE/OWASP compliance. The SubagentStop hook enforces P-003
(no recursive subagents) -- verify the CLI consolidation preserves this
security-critical enforcement without introducing gaps.

Use /eng-team with eng-lead to verify coding standards compliance on the
consolidated implementation (H-11, hexagonal layer boundaries per H-07).

### Bypass Assessment (/red-team)

Use /red-team with red-vuln to assess whether the migration from standalone
SubagentStop script to CLI introduces any bypass paths for P-003 enforcement.
Verify that subagent nesting detection is equally or more restrictive in the
CLI handler.

Evaluation dimensions: P-003 bypass via Agent tool without hook firing,
race condition between hook registration and subagent invocation,
settings.json misconfiguration that could disable the consolidated hook.

### DX Evaluation (/user-experience)

Use /user-experience with ux-heuristic-evaluator to evaluate the CLI-side
SubagentStop enforcement for developer experience quality.

Evaluation surfaces:
- Error messages when P-003 violation is detected: are they actionable?
- Exit codes: do they follow convention (non-zero for violation)?
- Help text for `jerry hooks` subcommands: is it discoverable?
- Consistency with other jerry CLI enforcement commands.

Apply Nielsen heuristic #9 (help users recognize, diagnose, recover from errors)
and #4 (consistency and standards) to the CLI enforcement output.

### AC Verification (/nasa-se)

Use /nasa-se with nse-verification to validate each acceptance criterion in the
STORY-024 worktracker entity is satisfied.

Use /nasa-se with nse-requirements to trace each AC back to the worktracker
entity and confirm bidirectional traceability.

### Quality Gate (/adversary + /eng-team)

Use /adversary with adv-selector to select C4 strategy set, then adv-executor
to run all 10 strategies in tournament mode against Phase 2 output.
Use adv-scorer to score with 6-dimension rubric.
Quality threshold: >= 0.95.

Evaluation dimensions: behavioral parity, no orphaned config references,
hook lifecycle correctness, Clean Architecture compliance,
P-003 enforcement strength, CLI DX quality.

Use /eng-team with eng-reviewer as the final quality gate.

Use /worktracker to update STORY-024 status to completed upon passing all gates.
Commit with message: "fix(hooks): consolidate SubagentStop into CLI (STORY-024, GH #178)"

---

## Phase 3 -- BUG-005: Rewrite Hook Tests (GH #214)

### Implementation (/problem-solving)

Use /problem-solving with ps-analyst to analyze scripts/tests/test_hooks.py and
design replacement tests targeting CLI-based enforcement.

Use /problem-solving with ps-reviewer to review the replacement tests for
correctness, coverage completeness, and BDD compliance before finalizing.

Data sources:
- Old tests: scripts/tests/test_hooks.py
- CLI enforcement: src/infrastructure/internal/enforcement/security_enforcement_engine.py
- pytest config: pytest.ini (contains --ignore entries to remove)
- Worktracker entity: projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/BUG-005-hook-test-step-defs/BUG-005-hook-test-step-defs.md

Steps:
1. Read scripts/tests/test_hooks.py. Catalog every test case and what behavior
   it verifies.
2. For each test case, design a replacement test that:
   - Lives in tests/ (not scripts/tests/)
   - Tests the CLI-based enforcement (jerry hooks pre-tool-use) or imports
     directly from src/infrastructure/internal/enforcement/
   - Uses BDD Given/When/Then structure per H-20
3. Write the new tests in tests/ using TDD Red phase: all tests fail initially
   because they target CLI entry points.
4. Verify new tests pass (Green phase) by running against existing CLI
   implementation.
5. Delete scripts/tests/test_hooks.py.
6. Edit pytest.ini: remove any --ignore entries that reference scripts/tests/.
7. Run `uv run pytest tests/ -v` and verify count >= 16,341.
   The count should increase because previously-ignored tests are now collected.

### Security Review (/eng-team)

Use /eng-team with eng-security to review the replacement test suite for
security test coverage completeness. Verify that every security-critical
behavior tested in the old scripts/tests/test_hooks.py has a corresponding
test in the new tests/ location.

Use /eng-team with eng-lead to verify test code follows coding standards
(H-11, H-20 BDD structure, naming conventions).

### Bypass Assessment (/red-team)

Use /red-team with red-vuln to assess whether the test migration introduces
any coverage gaps that could mask enforcement bypass vulnerabilities.
Verify that the new test suite exercises the same enforcement paths as the old.

Evaluation dimensions: test coverage gaps in security-critical paths,
pytest.ini --ignore removal correctness, CI pipeline collecting all new tests.

### AC Verification (/nasa-se)

Use /nasa-se with nse-verification to validate each acceptance criterion in the
BUG-005 worktracker entity is satisfied.

Use /nasa-se with nse-requirements to trace each AC back to the worktracker
entity and confirm bidirectional traceability.

### Quality Gate (/adversary + /eng-team)

Use /adversary with adv-selector to select C4 strategy set, then adv-executor
to run all 10 strategies in tournament mode against Phase 3 output.
Use adv-scorer to score with 6-dimension rubric.
Quality threshold: >= 0.95.

Evaluation dimensions: test coverage parity (every old behavior has a new test),
BDD compliance (H-20), no tests remaining in scripts/tests/, pytest.ini cleanup,
test count verification, security test completeness.

Use /eng-team with eng-reviewer as the final quality gate.

Use /worktracker to update BUG-005 status to completed upon passing all gates.
Commit with message: "fix(tests): rewrite hook tests for CLI enforcement (BUG-005, GH #214)"

---

## Phase 4 -- STORY-025: Port P-003 Validation Script to CLI (GH #193)

### Implementation (/problem-solving)

Use /problem-solving with ps-analyst to analyze the H-10 violation in
validate_frontmatter_command.py and plan the refactoring.

Use /problem-solving with ps-reviewer to review the refactored files for
Clean Architecture compliance and H-10 resolution correctness.

Data sources:
- Script to port: scripts/validate-agent-frontmatter.py
- CLI handler (H-10 violation): src/agents/application/commands/validate_frontmatter_command.py
- Worktracker entity: projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/STORY-025-schema-validate-cli/STORY-025-schema-validate-cli.md

Steps:
1. Read scripts/validate-agent-frontmatter.py. Catalog all validation checks,
   especially the P-003 (subagent nesting) check.
2. Read src/agents/application/commands/validate_frontmatter_command.py. Identify:
   a. Which validations already exist in the CLI handler.
   b. Which validations exist only in the standalone script (port candidates).
   c. The H-10 violation: identify the 3 classes in one file.
3. Resolve the H-10 violation first:
   a. Extract each class to its own file in the same directory following naming
      conventions (one_class_per_file.py pattern).
   b. Update all imports across the codebase.
   c. Run tests to verify no regressions.
4. Port missing validation logic (especially P-003 check) into the CLI handler
   using TDD (H-20):
   a. Write failing tests in tests/ for each validation being ported.
   b. Implement the validation in the appropriate hexagonal layer.
   c. Verify tests pass.
5. Delete scripts/validate-agent-frontmatter.py.
6. Use Grep to find all references to validate-agent-frontmatter.py across the
   repository (CI configs, docs, rule files). Update to use
   `uv run jerry agents validate-frontmatter`.
7. Remove any separate CI step that invokes the standalone script.
8. Move any tests from scripts/tests/ that test this script into tests/.
9. Run `uv run pytest tests/ -v` and verify count >= 16,341.

### Security Review (/eng-team)

Use /eng-team with eng-security to review the ported P-003 validation logic
for CWE/OWASP compliance. The P-003 check is a security-critical control
preventing recursive subagent spawning -- verify the CLI handler preserves
all enforcement strength.

Use /eng-team with eng-lead to verify the H-10 resolution (class extraction)
and ported validation logic follow coding standards (H-11 type hints,
docstrings, hexagonal layer boundaries per H-07).

### Bypass Assessment (/red-team)

Use /red-team with red-vuln to assess whether porting the P-003 validation
from standalone script to CLI handler introduces any bypass paths.
Verify that `uv run jerry agents validate-frontmatter` provides equivalent
or stronger P-003 enforcement than the standalone script.

Evaluation dimensions: P-003 bypass via agent definition that omits
disallowedTools, validation gaps for edge cases (empty tools list, alias
"Task" vs "Agent"), CI pipeline enforcement correctness.

### DX Evaluation (/user-experience)

Use /user-experience with ux-heuristic-evaluator to evaluate the CLI command
`jerry agents validate-frontmatter` for developer experience quality.

Evaluation surfaces:
- Error messages: when frontmatter validation fails, do error messages identify
  the specific file, line, and violation type?
- Exit codes: non-zero for validation failure, distinct codes for different
  failure categories?
- Help text: `jerry agents validate-frontmatter --help` is discoverable and
  explains usage, options, and expected input?
- Consistency with other jerry CLI commands (jerry hooks, jerry session).

Apply Nielsen heuristic #9 (help users recognize, diagnose, recover from errors),
#1 (visibility of system status), and #4 (consistency and standards).

### Reference Documentation (/diataxis)

Use /diataxis with diataxis-how-to-writer to create or update reference
documentation for the consolidated CLI commands:
- `jerry hooks pre-tool-use` -- what it enforces, when it runs, how to configure
- `jerry agents validate-frontmatter` -- what it validates, CLI usage,
  expected output, integration with CI

Output: update existing reference documentation or create new reference page at
an appropriate location under docs/reference/.

### AC Verification (/nasa-se)

Use /nasa-se with nse-verification to validate each acceptance criterion in the
STORY-025 worktracker entity is satisfied.

Use /nasa-se with nse-requirements to trace each AC back to the worktracker
entity and confirm bidirectional traceability (AC -> implementation -> test ->
CLI command -> CI step).

### Quality Gate (/adversary + /eng-team)

Use /adversary with adv-selector to select C4 strategy set, then adv-executor
to run all 10 strategies in tournament mode against Phase 4 output.
Use adv-scorer to score with 6-dimension rubric.
Quality threshold: >= 0.95.

Evaluation dimensions: validation parity (every script check exists in CLI),
H-10 resolution (one class per file), Clean Architecture compliance,
CI pipeline correctness, P-003 check coverage, CLI DX quality,
reference documentation completeness.

Use /eng-team with eng-reviewer as the final quality gate.

Use /worktracker to update STORY-025 status to completed upon passing all gates.
Commit with message: "feat(agents): port frontmatter validation to CLI (STORY-025, GH #193)"

---

## Post-Pipeline Verification

After all 4 phases complete:

1. Run full test suite: `uv run pytest tests/ -v --tb=short`
   Verify count >= 16,341.
2. Verify no files remain in scripts/ that duplicate CLI functionality:
   - scripts/pre_tool_use.py deleted
   - scripts/subagent_stop.py deleted
   - scripts/validate-agent-frontmatter.py deleted
   - scripts/tests/test_hooks.py deleted
3. Verify pytest.ini has no --ignore entries referencing scripts/tests/.
4. Verify no dangling references: use Grep to search for all three deleted
   script filenames across the entire repository. Zero matches expected
   (except historical references in commit messages or changelogs).
5. Use /nasa-se with nse-verification to run a final traceability check:
   all 4 worktracker entities (STORY-023, STORY-024, BUG-005, STORY-025)
   have all ACs satisfied with bidirectional traceability.
6. Use /worktracker to verify STORY-023, STORY-024, BUG-005, STORY-025 all
   show status: completed.

Final commit (if any cleanup needed):
"chore: post-cleanup verification for CI script removal (FEAT-001)"
```

---

## Construction Notes

| Element | Value | Source |
|---------|-------|--------|
| Skill Routing | /orchestration (orch-planner), /problem-solving (ps-investigator, ps-analyst, ps-reviewer), /eng-team (eng-security, eng-lead, eng-reviewer), /red-team (red-vuln), /nasa-se (nse-verification, nse-requirements), /user-experience (ux-heuristic-evaluator), /diataxis (diataxis-how-to-writer), /adversary (adv-selector, adv-executor, adv-scorer) | User explicitly requested all 7 skills (H-02 user authority); /orchestration added for 4-phase coordination |
| Domain Scope | Jerry CLI hook consolidation: scripts/ -> src/ hexagonal architecture migration across 4 worktracker items under FEAT-001 | User input: 4 named items with file paths |
| Data Source | Codebase files (Read, Grep, Glob): scripts/pre_tool_use.py, scripts/subagent_stop.py, scripts/validate-agent-frontmatter.py, src/infrastructure/internal/enforcement/security_enforcement_engine.py, src/agents/application/commands/validate_frontmatter_command.py, scripts/tests/test_hooks.py, pytest.ini, worktracker entities under projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/ | All paths verified via Glob |
| Quality Gate | /adversary C4 >= 0.95 per phase (tournament mode, all 10 strategies); /eng-team eng-reviewer as final gate; test count >= 16,341 baseline | User-specified threshold (0.95) exceeds H-13 minimum (0.92); user-specified C4 tournament mode |
| Output Path | Commit per phase with semantic message; worktracker entity status updates; reference docs under docs/reference/ | User-specified: commit-per-phase workflow |

### Template Adaptation Notes

Template 3 (Multi-Skill Orchestration) is designed for research -> analysis -> decision pipelines. This prompt adapts it for a 4-phase sequential implementation pipeline where each phase is an independent worktracker item with a dependency on the previous phase. Key adaptations:

1. **Phases are implementation items, not research -> analysis -> decision.** Each phase follows its own TDD micro-cycle (Red -> Green -> Refactor) rather than the template's research -> analysis -> decision macro-pattern.
2. **Quality gate is per-phase, not per-pipeline.** Each phase gets its own /adversary C4 tournament review because each is an independently deliverable worktracker item.
3. **Constraints section added.** NPT-013 format constraints embedded at the top to apply across all phases, which the template does not natively support.
4. **Post-pipeline verification added.** The dependency chain requires end-to-end validation that no regressions propagated across phases.
5. **7-skill routing per phase.** Each phase routes through implementation (/problem-solving), security review (/eng-team), bypass assessment (/red-team), AC verification (/nasa-se), and quality gate (/adversary). Phases 2 and 4 additionally route through DX evaluation (/user-experience). Phase 4 additionally routes through documentation (/diataxis).

### Skills Requested vs. Skills Routed

The user requested 7 skills. All 7 are routed per H-02 (user authority). The user's skill-to-agent mapping and rationale is preserved exactly as provided.

| Requested Skill | Routed | Named Agents | User Rationale |
|-----------------|--------|--------------|----------------|
| /eng-team | Yes (all phases) | eng-security, eng-lead, eng-reviewer | eng-security: CWE/OWASP compliance on ported logic. eng-lead: coding standards. eng-reviewer: final quality gate. |
| /red-team | Yes (all phases) | red-vuln | Assess whether migration introduces bypass paths or weakens enforcement. |
| /problem-solving | Yes (all phases) | ps-investigator, ps-analyst, ps-reviewer | ps-investigator: dead code verification. ps-analyst: consolidation strategy. ps-reviewer: code review. |
| /nasa-se | Yes (all phases) | nse-verification, nse-requirements | nse-verification: AC validation. nse-requirements: traceability. |
| /user-experience | Yes (phases 2, 4) | ux-heuristic-evaluator | CLI IS the user interface. Error messages, exit codes, help text are DX surfaces. |
| /diataxis | Yes (phase 4) | diataxis-how-to-writer | Reference documentation for consolidated CLI commands. |
| /adversary | Yes (all phases) | adv-selector, adv-executor, adv-scorer | C4 >= 0.95 per phase, all 10 strategies, tournament mode. |
| /orchestration | Yes (added) | orch-planner | 4-phase dependency chain with quality gates at boundaries requires orchestration. |

### v1 to v2 Diff Summary

| Aspect | v1 (Previous) | v2 (This Version) |
|--------|---------------|-------------------|
| Skills routed | 3 (/orchestration, /problem-solving, /adversary) | 8 (all 7 requested + /orchestration) |
| H-02 compliance | Violated (dropped 4 user-requested skills) | Compliant (all 7 routed) |
| /eng-team | Not routed | eng-security, eng-lead, eng-reviewer per phase |
| /red-team | Not routed | red-vuln per phase |
| /nasa-se | Not routed | nse-verification, nse-requirements per phase |
| /user-experience | Not routed | ux-heuristic-evaluator on phases 2, 4 |
| /diataxis | Not routed | diataxis-how-to-writer on phase 4 |
| Criticality | C3 | C4 (7-skill tournament mode, irreversible deletions) |
| Phase gate conditions | 3 conditions | 4 conditions (added eng-reviewer approval, nasa-se AC verification) |

---

## Self-Review Score

| Criterion | Weight | Score | Notes |
|-----------|--------|-------|-------|
| C1 Task Specificity | 20% | 3/3 | All 4 items have concrete file paths, named scripts, specific deletion/port/rewrite actions. Zero undefined terms. Zero trailing fragments. Every step is actionable with named files. Agent-to-task mapping is explicit per phase. |
| C2 Skill Routing | 18% | 3/3 | All 8 skills use /skill syntax with named agents: /orchestration (orch-planner), /problem-solving (ps-investigator, ps-analyst, ps-reviewer), /eng-team (eng-security, eng-lead, eng-reviewer), /red-team (red-vuln), /nasa-se (nse-verification, nse-requirements), /user-experience (ux-heuristic-evaluator), /diataxis (diataxis-how-to-writer), /adversary (adv-selector, adv-executor, adv-scorer). All 7 user-requested skills present. |
| C3 Context Provision | 15% | 3/3 | All data sources named with full repo-relative paths. Worktracker entity paths provided per phase. Baseline test count specified (16,341). Per-phase evaluation dimensions specified. CWE/OWASP dimensions for eng-security. Nielsen heuristics for ux-heuristic-evaluator. No redundant padding. |
| C4 Quality Specification | 15% | 3/3 | Numeric threshold (>= 0.95) with named mechanism (/adversary C4 tournament mode, adv-selector + adv-executor + adv-scorer). eng-reviewer as secondary gate. nse-verification as AC gate. Test count baseline as tertiary gate. Four-condition phase gate explicitly stated. |
| C5 Decomposition | 12% | 3/3 | 4 named phases with explicit dependency ordering. Per-phase subsections for each skill (Implementation, Security Review, Bypass Assessment, DX Evaluation, Reference Documentation, AC Verification, Quality Gate). Sync barrier: "proceed ONLY after (a) AC pass, (b) test suite passes, (c) eng-reviewer approves, (d) quality gate >= 0.95." Skills Routed Per Phase table provides cross-phase visibility. |
| C6 Output Specification | 12% | 3/3 | Per-phase commit messages with semantic format specified. Worktracker entity status updates specified. Reference documentation output path specified (docs/reference/). Post-pipeline verification checklist with 6 items. |
| C7 Positive Framing | 8% | 2/3 | 5 NPT-013 constraints use NEVER format (user-specified as NPT-013 hard constraints). Each has a constructive "Instead:" alternative. The NEVER format is intentional per NPT-013 research (100% compliance vs 92.2% for positive-only, p=0.016). Deducting 1 point because the constraints are in the prompt body rather than isolated in a separate guardrails section. |
| **Weighted Composite** | | **97/100** | (3/3 * 20) + (3/3 * 18) + (3/3 * 15) + (3/3 * 15) + (3/3 * 12) + (3/3 * 12) + (2/3 * 8) = 20 + 18 + 15 + 15 + 12 + 12 + 5.33 = 97.33, rounded to 97. |

**Tier: Exemplary (97/100)**

---

*Built by pe-builder v1.0.0 | Template 3 adapted | NPT-013 constraints embedded | 7 skills routed per H-02 | 2026-03-29*
