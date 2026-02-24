# PR #52 Comprehensive Forensic Diff Report

> Forensic analysis of PR #52 merge damage. Compares pre-PR#52 state (`1234e0a`) against current `origin/main` (`f363f34`, post-repair PRs #70-#73).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Verdict and key findings |
| [Methodology](#methodology) | How the analysis was conducted |
| [File Count Summary](#file-count-summary) | Totals at each analysis step |
| [Repair PR Coverage](#repair-pr-coverage) | What each repair PR fixed |
| [Remaining Damage](#remaining-damage) | Files with unrepaired regressions |
| [Classification Table](#classification-table) | All modified-by-PR#52 files still different from baseline |
| [Evidence](#evidence) | Git diff excerpts for each damage finding |
| [Recommendations](#recommendations) | Prioritized repair actions |

---

## Executive Summary

**Verdict: REMAINING DAMAGE FOUND -- 8 files with unrepaired EN-002 regressions.**

PR #52 (feat/proj-004-context-resilience, +12K/-42K lines) merged to main at commit `4895410` and silently reverted changes from PRs #55, #58, and #60 (EN-002 HARD Rule Budget Enforcement, PROJ-007 agent patterns, BUG-002 AST CLI fix).

Four repair PRs (#70, #71, #72, #73) have been applied. They successfully restored:
- All 105 deleted PROJ-007 files (PR #70)
- Critical governance files: quality-enforcement.md, project-workflow.md, skill-standards.md (PR #71)
- Agent development and routing standards rule files (PR #71)
- BUG-002 AST CLI commands (PR #72)
- EN-002 prompt reinforcement engine with C-06 injection protection (PR #73)

However, **8 files** retain unrepaired EN-002 regressions. These fall into two categories:
1. **L2-REINJECT marker format regressions** (7 files) -- Markers use deprecated `tokens=` parameter and pre-consolidation H-rule references
2. **E2E test regressions** (1 file) -- Test references 600-token budget and lacks consolidated H-rule awareness

**Functional impact: LOW.** The prompt reinforcement engine on origin/main correctly handles both old and new marker formats (optional `tokens=` regex). The L2 system works. The damage is governance/specification inconsistency, not functional breakage.

---

## Methodology

1. Identified ALL 293 files PR #52 changed: `git diff --name-status 1234e0a..4895410`
2. Compared pre-PR#52 state vs current `origin/main`: `git diff --name-status 1234e0a..origin/main`
3. Computed intersection: files PR #52 touched AND still different on origin/main (204 files on local HEAD, 119 on origin/main after PRs #72/#73)
4. Filtered out: `projects/PROJ-*` work artifacts, `.jerry/checkpoints/`, `uv.lock`
5. For each remaining file, compared `git show 1234e0a:<file>` vs `git show origin/main:<file>` and classified as:
   - **Legitimate** -- New PROJ-004/PROJ-010 code, version bumps, new features
   - **Repaired** -- Damage from PR #52 that was fixed by repair PRs
   - **Damage** -- EN-002 changes reverted by PR #52 and NOT repaired

**Reference commits:**
- `1234e0a` -- Last clean main state BEFORE PR #52 merged (post-EN-002)
- `4895410` -- The PR #52 merge commit
- `f363f34` -- Current `origin/main` HEAD (post-repair PRs #70-#73)

---

## File Count Summary

| Step | Count | Description |
|------|-------|-------------|
| PR #52 total files changed | 293 | M=93, A=57, D=142, R=1 |
| Files different: 1234e0a vs origin/main | 334 | Includes post-PR#52 new work |
| Intersection (PR #52 touched AND still different) | 119 | After filtering PROJ-*, .jerry/, uv.lock |
| Of those: Added by PR #52 (new code) | 55 | Legitimate PROJ-004 additions |
| Of those: Modified by PR #52 (potential reverts) | 47 | Analyzed individually below |
| Fully restored to pre-PR#52 state | 89+31=120 | 89 by PRs #70/#71, 31 more by PRs #72/#73 |
| Classified as legitimate changes | 39 | PROJ-004 code, version bumps, PROJ-010 additions |
| **Classified as REMAINING DAMAGE** | **8** | EN-002 regressions (see below) |

---

## Repair PR Coverage

| PR | Scope | Files Fixed | Status |
|----|-------|------------|--------|
| #70 | Restore 105 deleted PROJ-007 files, check_hard_rule_ceiling.py, CI workflow | 107 | COMPLETE |
| #71 | EN-002 governance changes in quality-enforcement.md, project-workflow.md, skill-standards.md, agent-dev-standards.md, agent-routing-standards.md | 5 rule files + PROJ-007 worktracker entities | COMPLETE |
| #72 | BUG-002 AST CLI fix (ast_commands.py, ast_ops.py removal, test coverage) | 6 files | COMPLETE |
| #73 | EN-002 prompt reinforcement engine (multi-file scanning, 850-token budget, C-06 injection protection, unit test coverage) | 2 src + 1 test | COMPLETE |

---

## Remaining Damage

### Category 1: L2-REINJECT Marker Format Regressions (7 files)

**Root cause:** EN-002 (TASK-022) updated L2-REINJECT markers across all rule files to:
- Remove deprecated `tokens=` parameter
- Use compound H-rule references (e.g., "H-11" covering both type hints and docstrings)

PR #52 reverted these markers to pre-EN-002 format. Repair PRs fixed quality-enforcement.md and other critical governance files but did NOT fix the L2-REINJECT markers in the following files:

| # | File | Damage | Severity |
|---|------|--------|----------|
| 1 | `.context/rules/architecture-standards.md` | L2-REINJECT uses `tokens=60` and old content. H-07/H-08/H-09 listed as 3 separate rules instead of compound H-07. Section header says "H-07 to H-10" instead of "H-07 (compound), H-10". | MEDIUM |
| 2 | `.context/rules/coding-standards.md` | L2-REINJECT uses `tokens=60` and references "H-11" + "H-12" separately instead of compound "H-11". | LOW |
| 3 | `.context/rules/markdown-navigation-standards.md` | L2-REINJECT uses `tokens=25` and references "H-23" + "H-24" separately instead of compound "H-23". | LOW |
| 4 | `.context/rules/python-environment.md` | L2-REINJECT uses `tokens=50`. Content unchanged but format inconsistent. | LOW |
| 5 | `.context/rules/testing-standards.md` | L2-REINJECT uses `tokens=40` and references "H-20" + "H-21" separately instead of compound "H-20". | LOW |
| 6 | `.context/rules/mcp-tool-standards.md` | L2-REINJECT uses `tokens=70`. Content unchanged but format inconsistent. | LOW |
| 7 | `CLAUDE.md` | L2-REINJECT uses `tokens=80`. | LOW |

### Category 2: E2E Test Regression (1 file)

| # | File | Damage | Severity |
|---|------|--------|----------|
| 8 | `tests/e2e/test_quality_framework_e2e.py` | Three regressions: (a) L2 reinforcement test uses 600-token budget + single-file path instead of 850 + directory; (b) H-rule range tests lack `consolidated_ids` skip sets for retired IDs; (c) Test docstrings reference pre-consolidation rule ranges. | MEDIUM |

### Category 3: Cosmetic Comment Regression (1 file, informational)

| # | File | Damage | Severity |
|---|------|--------|----------|
| -- | `src/infrastructure/internal/enforcement/enforcement_rules.py` | Comments reference "H-07, H-08" instead of compound "H-07". No functional impact. | COSMETIC |

---

## Classification Table

All 47 modified-by-PR#52 files that are still different from pre-PR#52 state on origin/main:

### Configuration Files

| File | Classification | Notes |
|------|---------------|-------|
| `.claude-plugin/marketplace.json` | Legitimate | Version bump 0.11.0 -> 0.12.4 |
| `.claude-plugin/plugin.json` | Legitimate | Version bump |
| `.gitignore` | Legitimate | Intentional: `.jerry/local/` -> `.jerry/` for checkpoint coverage |
| `.pre-commit-config.yaml` | Legitimate | Hook ordering change only; same hooks present |
| `pyproject.toml` | Legitimate | Version bump + expected config |
| `hooks/hooks.json` | Legitimate | PROJ-004 SubagentStop + Stop hooks added |
| `projects/README.md` | Legitimate | PROJ-010 added |

### Rule Files

| File | Classification | Notes |
|------|---------------|-------|
| `.context/rules/architecture-standards.md` | **DAMAGE** | H-07/H-08/H-09 split + L2-REINJECT `tokens=` |
| `.context/rules/coding-standards.md` | **DAMAGE** | L2-REINJECT `tokens=` + split H-11/H-12 |
| `.context/rules/mandatory-skill-usage.md` | Legitimate | /eng-team + /red-team added (PROJ-010) + L2-REINJECT `tokens=` |
| `.context/rules/markdown-navigation-standards.md` | **DAMAGE** | L2-REINJECT `tokens=` + split H-23/H-24 |
| `.context/rules/mcp-tool-standards.md` | Mixed | Legitimate eng/red-team agents + **DAMAGE** L2-REINJECT `tokens=` |
| `.context/rules/python-environment.md` | **DAMAGE** | L2-REINJECT `tokens=` |
| `.context/rules/testing-standards.md` | **DAMAGE** | L2-REINJECT `tokens=` + split H-20/H-21 |

### Top-Level Docs

| File | Classification | Notes |
|------|---------------|-------|
| `AGENTS.md` | Legitimate | eng-team + red-team agents added (PROJ-010) |
| `CLAUDE.md` | **DAMAGE** | L2-REINJECT `tokens=80` (plus legitimate PROJ-010 skill additions) |

### Source Code (src/)

| File | Classification | Notes |
|------|---------------|-------|
| `src/bootstrap.py` | Legitimate | PROJ-004 context monitoring wiring |
| `src/context_monitoring/application/services/checkpoint_service.py` | Legitimate | PROJ-004 expansion |
| `src/context_monitoring/application/services/resumption_context_generator.py` | Legitimate | PROJ-004 expansion |
| `src/infrastructure/internal/enforcement/enforcement_rules.py` | Cosmetic | Comment references "H-07, H-08" vs compound "H-07" |
| `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py` | Legitimate | Repaired by PR #73 + enhanced C-06 |
| `src/interface/cli/adapter.py` | Legitimate | PROJ-004 additions |
| `src/interface/cli/hooks/hooks_pre_compact_handler.py` | Legitimate | PROJ-004 expansion |
| `src/interface/cli/hooks/hooks_prompt_submit_handler.py` | Legitimate | PROJ-004 expansion |
| `src/interface/cli/hooks/hooks_session_start_handler.py` | Legitimate | PROJ-004 expansion |
| `src/interface/cli/main.py` | Legitimate | PROJ-004 CLI commands |
| `src/interface/cli/parser.py` | Legitimate | PROJ-004 CLI arguments |
| `src/session_management/application/handlers/commands/abandon_session_command_handler.py` | Legitimate | PROJ-004 refactor |
| `src/session_management/application/handlers/commands/create_session_command_handler.py` | Legitimate | PROJ-004 refactor |
| `src/session_management/application/handlers/commands/end_session_command_handler.py` | Legitimate | PROJ-004 refactor |
| `src/session_management/application/ports/session_repository.py` | Legitimate | PROJ-004 expansion |
| `src/session_management/domain/aggregates/session.py` | Legitimate | PROJ-004 expansion |
| `src/session_management/infrastructure/adapters/event_sourced_session_repository.py` | Legitimate | PROJ-004 expansion |
| `src/session_management/infrastructure/adapters/in_memory_session_repository.py` | Legitimate | PROJ-004 expansion |

### Test Files

| File | Classification | Notes |
|------|---------------|-------|
| `tests/architecture/test_ast_enforcement.py` | Legitimate | H-30->H-26 reference update (correct post-consolidation) |
| `tests/e2e/test_quality_framework_e2e.py` | **DAMAGE** | 600-token budget, missing consolidated_ids, pre-consolidation docstrings |
| `tests/integration/cli/test_jerry_cli_subprocess.py` | Legitimate | PROJ-004 test updates |
| `tests/integration/test_event_sourcing_wiring.py` | Legitimate | PROJ-004 test updates |
| `tests/session_management/unit/application/test_session_handlers.py` | Legitimate | PROJ-004 test updates |
| `tests/system/test_context_monitoring_system.py` | Legitimate | PROJ-004 test updates |
| `tests/unit/context_monitoring/application/test_checkpoint_service.py` | Legitimate | PROJ-004 test expansion |
| `tests/unit/context_monitoring/application/test_resumption_context_generator.py` | Legitimate | PROJ-004 test expansion |
| `tests/unit/enforcement/test_prompt_reinforcement_engine.py` | Legitimate | Repaired by PR #73 (850-token, directory, C-06 tests) |
| `tests/unit/interface/cli/hooks/test_hooks_pre_compact_handler.py` | Legitimate | PROJ-004 test expansion |
| `tests/unit/interface/cli/hooks/test_hooks_prompt_submit_handler.py` | Legitimate | PROJ-004 test expansion |
| `tests/unit/interface/cli/hooks/test_hooks_session_start_handler.py` | Legitimate | PROJ-004 test expansion |
| `tests/unit/interface/cli/test_ast_commands.py` | Legitimate | PR #72 repair + new coverage |

---

## Evidence

### Evidence 1: architecture-standards.md H-07/H-08/H-09 Split

**Pre-PR#52 (1234e0a) -- EN-002 consolidated:**
```markdown
| H-07 | **Architecture layer isolation:** (a) `src/domain/` MUST NOT import from `application/`, `infrastructure/`, or `interface/` (stdlib and `shared_kernel/` only); (b) `src/application/` MUST NOT import from `infrastructure/` or `interface/`; (c) Only `src/bootstrap.py` SHALL instantiate infrastructure adapters. | Architecture test fails. CI blocks merge. |
```

**Current origin/main -- REVERTED to pre-EN-002:**
```markdown
| H-07 | `src/domain/` MUST NOT import from `application/`, `infrastructure/`, or `interface/`. Stdlib and `shared_kernel/` only. | Architecture test fails. CI blocks merge. |
| H-08 | `src/application/` MUST NOT import from `infrastructure/` or `interface/`. | Architecture test fails. CI blocks merge. |
| H-09 | Only `src/bootstrap.py` SHALL instantiate infrastructure adapters. | Architecture test fails. |
```

**Impact:** Inconsistent with quality-enforcement.md which lists H-08 and H-09 as RETIRED (consolidated into H-07). Three separate rules where there should be one compound rule.

### Evidence 2: L2-REINJECT Marker Format (all affected files)

**Pre-PR#52 (EN-002 format):**
```html
<!-- L2-REINJECT: rank=7, content="Public function signatures REQUIRED (H-11): (a) type hints on all public functions, (b) docstrings on all public functions/classes/modules. Google-style format." -->
```

**Current origin/main (reverted to pre-EN-002):**
```html
<!-- L2-REINJECT: rank=7, tokens=60, content="Type hints REQUIRED on all public functions (H-11). Docstrings REQUIRED on all public functions/classes/modules (H-12). Google-style format." -->
```

**Differences:**
1. `tokens=60` present (deprecated per EN-002 R4)
2. References "H-11" and "H-12" separately instead of compound "H-11"
3. Content uses flat list instead of (a)/(b) compound structure

### Evidence 3: test_quality_framework_e2e.py Regressions

**Pre-PR#52 (1234e0a):**
```python
def test_l2_reinforcement_when_generated_then_under_850_token_budget(self) -> None:
    """L2 prompt reinforcement preamble is under the 850-token budget (EN-002)."""
    engine = PromptReinforcementEngine(
        rules_path=rules_dir,
        token_budget=850,
    )
```

**Current origin/main (REVERTED):**
```python
def test_l2_reinforcement_when_generated_then_under_600_token_budget(self) -> None:
    """L2 prompt reinforcement preamble is under the 600-token budget."""
    engine = PromptReinforcementEngine(
        rules_path=SSOT_PATH,
        token_budget=600,
    )
```

**Pre-PR#52 (1234e0a):**
```python
def test_ssot_when_read_then_h_rules_h01_through_h16_defined(self) -> None:
    """SSOT defines H-rules H-01 through H-16 (post-consolidation: H-08, H-09 absorbed into H-07)."""
    content = read_file(SSOT_PATH)
    consolidated_ids = {"H-08", "H-09"}
    for i in range(1, 17):
        rule_id = f"H-{i:02d}"
        if rule_id in consolidated_ids:
            continue
        assert rule_id in content
```

**Current origin/main (REVERTED):**
```python
def test_ssot_when_read_then_h_rules_h01_through_h16_defined(self) -> None:
    """SSOT defines H-rules H-01 through H-16 (minimum original set)."""
    content = read_file(SSOT_PATH)
    for i in range(1, 17):
        rule_id = f"H-{i:02d}"
        assert rule_id in content
```

---

## Recommendations

### Priority 1: Fix architecture-standards.md (MEDIUM severity)

Restore the EN-002 compound H-07 rule. This file is auto-loaded via `.claude/rules/` and directly affects LLM rule comprehension. Having three rules (H-07, H-08, H-09) when quality-enforcement.md says H-08 and H-09 are RETIRED creates a contradiction.

**Action:** Restore to pre-PR#52 version: `git show 1234e0a:.context/rules/architecture-standards.md`

### Priority 2: Fix test_quality_framework_e2e.py (MEDIUM severity)

The E2E test for L2 reinforcement uses the wrong budget (600 vs 850) and tests single-file mode. The H-rule range tests lack consolidated ID awareness.

**Action:** Restore EN-002 changes:
- Change token budget test to 850 with directory path
- Add `consolidated_ids` skip sets to H-rule range tests
- Update docstrings to reference post-consolidation state

### Priority 3: Fix L2-REINJECT markers in 6 rule files + CLAUDE.md (LOW severity)

Remove deprecated `tokens=` parameter and update to compound H-rule references. NOT functionally breaking (engine handles both formats) but inconsistent with EN-002 specification.

**Action for each file:** Remove `tokens=N, ` from L2-REINJECT markers and update content to use compound rule references per EN-002.

Files:
1. `.context/rules/coding-standards.md`
2. `.context/rules/markdown-navigation-standards.md`
3. `.context/rules/python-environment.md`
4. `.context/rules/testing-standards.md`
5. `.context/rules/mcp-tool-standards.md`
6. `CLAUDE.md`

### Priority 4: Fix enforcement_rules.py comment (COSMETIC)

Update comment from "H-07, H-08" to "H-07" (compound). No functional impact.

---

## Analysis Metadata

- **Analyst:** Claude Code (forensic investigation)
- **Date:** 2026-02-22
- **Criticality:** C3 (touches .context/rules/, >10 files affected)
- **Base commit:** `1234e0a` (pre-PR#52, post-EN-002)
- **Merge commit:** `4895410` (PR #52)
- **Current HEAD:** `f363f34` (origin/main, post-repair PRs #70-#73)
- **Total files analyzed:** 293 (PR #52 changeset) + 334 (origin/main delta) = full coverage
- **Damage files found:** 8 (+ 1 cosmetic)
- **Functional impact:** LOW (L2 engine handles both marker formats)
- **Governance impact:** MEDIUM (specification inconsistency with quality-enforcement.md)
