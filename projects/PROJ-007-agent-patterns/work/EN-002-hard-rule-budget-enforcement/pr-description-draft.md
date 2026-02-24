# PR Description Draft: EN-002 HARD Rule Budget Enforcement

> **Deliverable Type:** Pull Request Description
> **Worktracker Entity:** EN-002 (part of PROJ-007 Agent Patterns)
> **Base Branch:** main
> **Head Branch:** feat/proj-007-agent-patterns

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Title](#title) | PR title |
| [Body](#body) | Full PR description |

---

## Title

feat(proj-007): implement EN-002 HARD rule budget enforcement

## Body

### Summary

- Expand L2 prompt reinforcement engine from 1 file to 9 files, increasing HARD rule coverage from 32% to 84% (21/25 rules context-rot protected via combined engine expansion + rule consolidation)
- Consolidate HARD rules from 31 to 25 via compound rules (H-25..H-30: 6->2, H-07..H-09: 3->1) with principled ceiling derived from cognitive load, token budget, and governance constraints
- Add L5 CI enforcement gate (pre-commit hook + GitHub Actions job) preventing silent ceiling breaches with absolute maximum safety valve (`_ABSOLUTE_MAX_CEILING = 28`)
- Introduce Two-Tier enforcement model: Tier A (21 rules, L2-protected) and Tier B (4 rules with per-rule compensating controls: H-04 SessionStart hook, H-16 skill workflow, H-17 quality gate infrastructure, H-18 S-007 strategy)
- Remove deprecated `tokens` field from all 17 L2-REINJECT markers; update parser regex for backward compatibility
- Create worktracker entities for EN-001 (install deliverables, 10 tasks PENDING) and EN-002 (budget enforcement, 7 tasks DONE + 1 PENDING follow-up)

### Motivation

The C4 adversary tournament on the HARD rule budget upper boundary derivation revealed two critical enforcement gaps:

1. **DISC-001:** The 35-rule ceiling had no principled derivation. Three independent constraint families (cognitive load @ 7+/-2, enforcement coverage @ L2 token budget, governance burden @ review cost) converge on a 25-rule ceiling.
2. **DISC-002:** The L2 engine only read `quality-enforcement.md`, leaving 21 of 31 H-rules vulnerable to context rot — the exact problem the enforcement architecture was built to prevent.

These gaps were identified during PROJ-007 Agent Patterns research and codified as DISC-001 and DISC-002. DEC-001 captures the 5-decision implementation plan.

### Changes

#### Engine (`src/infrastructure/internal/enforcement/`)

| File | Change |
|------|--------|
| `prompt_reinforcement_engine.py` | `_read_rules_file` handles directories via `sorted(glob("*.md"))`; `_find_rules_path` returns `.claude/rules/` directory; `tokens` field made optional in regex (non-capturing group); `tokens` removed from output dict; budget documented as 850; C-06 content sanitization added |
| `enforcement_rules.py` | Comment update: H-07/H-08 -> H-07 compound |

#### CI Gate (`scripts/`)

| File | Change |
|------|--------|
| `check_hard_rule_ceiling.py` (new) | Counts H-rules in quality-enforcement.md, reads ceiling, fails if exceeded. Independent `_ABSOLUTE_MAX_CEILING = 28` prevents self-referential bypass. Exits non-zero on violation. |

#### Governance (`.context/rules/`, `CLAUDE.md`)

| File | Change |
|------|--------|
| `quality-enforcement.md` | Version 1.3.0->1.5.0. Ceiling 35->25; two-tier model; exception mechanism (max N=3, C4 ADR required, 3-month reversion); auto-escalation rules AE-001..AE-006; operational score bands (PASS/REVISE/REJECTED); H-31 ambiguity rule; skill routing decision table; `tokens` removed from 8 L2-REINJECT markers |
| `skill-standards.md` | H-25..H-30 consolidated to H-25 (skill file naming/location) + H-26 (skill registration); `tokens` removed from marker |
| `architecture-standards.md` | H-07..H-09 consolidated to H-07 (hexagonal layer boundaries as compound rule with sub-items a/b/c); `tokens` removed from marker |
| `coding-standards.md` | `tokens` removed from L2-REINJECT marker |
| `testing-standards.md` | `tokens` removed from L2-REINJECT marker |
| `python-environment.md` | `tokens` removed from L2-REINJECT marker |
| `mandatory-skill-usage.md` | `tokens` removed from L2-REINJECT marker |
| `markdown-navigation-standards.md` | `tokens` removed from L2-REINJECT marker |
| `mcp-tool-standards.md` | `tokens` removed from L2-REINJECT marker |
| `CLAUDE.md` | `tokens` removed from L2-REINJECT marker; H-31 added to critical constraints table |

#### CI/CD

| File | Change |
|------|--------|
| `.pre-commit-config.yaml` | Added `hard-rule-ceiling` hook (runs `scripts/check_hard_rule_ceiling.py`) |
| `.github/workflows/ci.yml` | Added `hard-rule-ceiling` job validating both SSOT ceiling and `_ABSOLUTE_MAX_CEILING` |

#### Tests

| File | Tests | Change |
|------|-------|--------|
| `test_prompt_reinforcement_engine.py` | 41 | +4 `TestMultiFileReading` tests; replaced `test_parse_markers_when_valid_content_then_extracts_tokens` with `test_parse_markers_when_no_tokens_field_then_still_parses`; removed stale `tokens` assertion; `TestBudgetEnforcement` updated 600->850; +4 C-06 sanitization tests |
| `test_hard_rule_ceiling.py` (new) | 12 | Full coverage of ceiling enforcement script including absolute max, edge cases, malformed input |
| `test_quality_framework_e2e.py` | 51 | Updated L2 budget test (600->850, directory path); updated H-rule assertions for consolidated IDs (H-08/H-09 retired) |

#### Worktracker Entities (30+ files)

| Entity Set | Path Pattern | Status |
|------------|-------------|--------|
| EN-001 + TASK-012..021 | `work/EN-001-install-agent-pattern-deliverables/` | PENDING |
| EN-002 + TASK-022..029 | `work/EN-002-hard-rule-budget-enforcement/` | DONE (7/8 tasks, 1 follow-up) |
| DISC-001, DISC-002 | `work/EN-002-.../DISC-00{1,2}-*/` | VALIDATED |
| DEC-001 | `work/EN-002-.../DEC-001-*/` | ACCEPTED |
| BUG-001 | `work/BUG-001-scaffold-cartesian-product/` | PENDING |
| C4 Tournament | `work/EN-002-.../c4-tournament/` | 4 score rounds + strategy reports |

### Quality Evidence

| Evidence | Value |
|----------|-------|
| C4 adversary tournament | 10/10 strategies applied |
| S-014 quality score | 0.953 PASS (threshold: >= 0.95 elevated) |
| Score trajectory | 0.620 -> 0.868 -> 0.924 -> 0.953 (4 rounds) |
| Test suite | 3,382 passed, 66 skipped, 0 failed |
| L5 ceiling gate | 25/25 PASS, headroom 0 |
| Pre-commit hooks | 19/19 PASS (including new `hard-rule-ceiling`) |
| Implementation summary | `work/EN-002-.../en-002-implementation-summary.md` |
| Tournament final score | `work/EN-002-.../c4-tournament/s014-score-r4.md` |

### Test Plan

- [x] Unit tests: `test_prompt_reinforcement_engine.py` (41/41 PASS) — multi-file reading, marker parsing, budget enforcement, C-06 sanitization
- [x] Unit tests: `test_hard_rule_ceiling.py` (12/12 PASS) — ceiling count, absolute max, edge cases
- [x] E2E tests: `test_quality_framework_e2e.py` (51/51 PASS) — full quality framework integration
- [x] Full suite: `uv run pytest tests/` (3,382 pass, 66 skip, 0 fail)
- [x] Pre-commit: all 19 hooks pass (including new `hard-rule-ceiling` hook)
- [x] L5 gate: `uv run python scripts/check_hard_rule_ceiling.py` reports PASS (25/25, headroom 0)
- [ ] CI pipeline: verify GitHub Actions `hard-rule-ceiling` job passes on push (check Actions tab after merge)

### Reviewer Guidance

**Key areas to verify:**

1. **Engine changes** (`prompt_reinforcement_engine.py`): Backward-compatible directory handling, `tokens` field removal with optional regex group, match group index shift (content moved from group 3 to group 2)
2. **Governance SSOT** (`quality-enforcement.md`): Two-tier model, exception mechanism constraints, H-31 rule definition
3. **CI gate** (`check_hard_rule_ceiling.py`): Absolute max ceiling (`_ABSOLUTE_MAX_CEILING = 28`) independence from SSOT value, fail-closed design
4. **Test coverage**: Multi-file reading tests, no-tokens-field parsing test, budget assertion update

**Safe to skim:** Worktracker entity files (30+ files following standard templates), tournament artifacts (scoring reports from C4 process)

### Worktracker Cross-Reference

| Entity | Relationship | Path |
|--------|-------------|------|
| PROJ-007 | Parent project | `projects/PROJ-007-agent-patterns/` |
| EN-002 | This PR implements EN-002 | `work/EN-002-.../EN-002.md` |
| EN-001 | Unblocked by EN-002 (TASK-016 depends on ceiling headroom) | `work/EN-001-.../EN-001.md` |
| DISC-001 | Discovery: unprincipled ceiling | `work/EN-002-.../DISC-001-*/DISC-001.md` |
| DISC-002 | Discovery: L2 engine coverage gap | `work/EN-002-.../DISC-002-*/DISC-002.md` |
| DEC-001 | Decision: 5 implementation decisions | `work/EN-002-.../DEC-001-*/DEC-001.md` |
| BUG-001 | Scaffold bug (separate, included for tracking) | `work/BUG-001-*/BUG-001.md` |

### Breaking Changes

None. The L2 engine changes are backward-compatible:
- Directory path handling falls back to single-file reading (`is_file()` check before `is_dir()`)
- `tokens` field in markers is optional (old markers with `tokens` still parse via non-capturing group)
- Consolidated H-rules retain their original IDs (retired IDs H-08, H-09, H-27..H-30 not reassigned)

---

Generated with [Claude Code](https://claude.com/claude-code)
