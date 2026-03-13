# PROJ-0037-doc-module Bugfix: Orchestration Plan

> **Document ID:** PROJ-0037-ORCH-PLAN-003
> **Workflow ID:** bugfix-20260312-001
> **Date:** 2026-03-12
> **Status:** PLANNED
> **Criticality:** C2 (Standard — 3-5 files, reversible within 1 day, no new public API surface)
> **Quality Threshold:** >= 0.93
> **Prior Workflow:** impl-20260310-001

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Workflow Overview](#l0-workflow-overview) | What we're fixing and why |
| [L1: Technical Plan](#l1-technical-plan) | Phases, agents, barriers, diagram |
| [L2: Implementation Details](#l2-implementation-details) | File changes, execution validation, recovery |
| [Quality Gates](#quality-gates) | C2 gate definitions |

---

## L0: Workflow Overview

The implementation pipeline (impl-20260310-001) completed all 4 barriers but discovered BUG-001 at the CLI smoke test: `AstFrontmatterReader` reads blockquote metadata (`> **Key:** Value`) instead of YAML frontmatter (`---` delimited). All 30 SKILL.md files are skipped because the `name` field lives in YAML frontmatter.

This workflow fixes BUG-001, validates that `YamlFrontmatterReader` is the **only** blocker, updates stale data files (13 -> 30 skills), and runs `jerry docs generate --write` to produce the actual README output. Every claim is verified by **code execution**, not inspection.

**Scope:**
- Create `YamlFrontmatterReader` adapter
- Swap wiring in `bootstrap.py`
- Update `skill-examples.yaml` (17 missing skills)
- Add integration tests against real SKILL.md and agent files
- Execute `jerry docs generate --write` and verify exit 0
- Verify existing tests still pass

**Note:** `features.yaml` does NOT require modification — skill/agent counts are computed dynamically at generation time (see features.yaml header comment). The `AstFrontmatterReader` bug affects both SKILL.md and `agents/*.md` files equally since both use `---`-delimited YAML frontmatter. `YamlFrontmatterReader` fixes both paths.

---

## L1: Technical Plan

### Workflow Diagram

```
BUGFIX-20260312-001: BUG-001 Fix + End-to-End Validation
========================================================

Input Artifacts (from impl-20260310-001)
  ├── BUG-001-frontmatter-reader-mismatch.md (root cause + fix plan)
  ├── src/docs/ bounded context (all existing code)
  └── .context/templates/docs/ (templates + stale data files)

══════════════════════════════════════════════════════════════
PHASE 1 — FIX (Sequential)
══════════════════════════════════════════════════════════════

  ┌──────────────────────────────────────────────┐
  │              eng-backend                      │
  │  1a. Create YamlFrontmatterReader adapter     │
  │      src/docs/infrastructure/adapters/        │
  │      yaml_frontmatter_reader.py               │
  │  1b. Swap wiring in src/bootstrap.py          │
  │      AstFrontmatterReader -> YamlFrontmatter  │
  │  1c. Update IFrontmatterReader docstring      │
  │  1d. Update skill-examples.yaml (+17 skills)  │
  │                                               │
  │  EXECUTION VALIDATION:                        │
  │  ✓ SKILL.md: read adversary/SKILL.md → name  │
  │  ✓ Agent: read agents/adv-executor.md → name  │
  │    (DA-001: validates agent extraction path)  │
  │  ✓ Complex YAML: read contract-design/        │
  │    SKILL.md (>- block scalar) → name          │
  │    (DA-003: validates complex frontmatter)    │
  │  ✓ Bulk: 30/30 SKILL.md files have name      │
  └──────────────────┬───────────────────────────┘
                     │
                     ▼
         ╔═══════════════════════╗
         ║      BARRIER 1        ║
         ║    Fix Validation     ║
         ║   /adversary C2       ║
         ║   S-007, S-002, S-014 ║
         ║   >= 0.93             ║
         ╚═══════════════════════╝
                     │
                     ▼

══════════════════════════════════════════════════════════════
PHASE 2 — INTEGRATION TEST (Sequential)
══════════════════════════════════════════════════════════════

  ┌──────────────────────────────────────────────┐
  │               eng-qa                          │
  │  2a. Integration test: YamlFrontmatterReader  │
  │      reads name from real SKILL.md            │
  │  2b. Integration test: SkillExtractor with    │
  │      YamlFrontmatterReader extracts 30 skills │
  │  2c. Verify existing unit tests still pass    │
  │      (they mock IFrontmatterReader)           │
  │  2d. Verify architecture tests pass           │
  │      (bootstrap.py swap safety — DA-007)      │
  │                                               │
  │  EXECUTION VALIDATION:                        │
  │  ✓ uv run pytest tests/unit/docs/ -v          │
  │  ✓ uv run pytest tests/architecture/ -v       │
  │  ✓ uv run pytest tests/integration/docs/ -v   │
  │  ✓ All tests pass (exit 0)                    │
  └──────────────────┬───────────────────────────┘
                     │
                     ▼
         ╔═══════════════════════╗
         ║      BARRIER 2        ║
         ║   Test Validation     ║
         ║   /adversary C2       ║
         ║   S-007, S-002, S-014 ║
         ║   >= 0.93             ║
         ╚═══════════════════════╝
                     │
                     ▼

══════════════════════════════════════════════════════════════
PHASE 3 — END-TO-END EXECUTION (Sequential)
══════════════════════════════════════════════════════════════

  ┌──────────────────────────────────────────────┐
  │              eng-backend                      │
  │  3a. Run: uv run jerry docs generate          │
  │      → Verify stdout shows 30 skills,         │
  │        89 agents, populated table             │
  │  3b. Run: uv run jerry docs generate --write  │
  │      → Verify README.md updated between       │
  │        markers                                │
  │  3c. Run: uv run jerry docs generate --check  │
  │      → Verify exit 0 (no drift)               │
  │  3d. Run: uv run pytest tests/ -v --tb=short  │
  │      → Full test suite green                  │
  │                                               │
  │  EXECUTION VALIDATION:                        │
  │  ✓ jerry docs generate --check exits 0        │
  │  ✓ README.md contains populated skills table  │
  │  ✓ README.md contains 30 skills, 89 agents    │
  │  ✓ Full pytest suite passes                   │
  └──────────────────┬───────────────────────────┘
                     │
                     ▼
         ╔═══════════════════════╗
         ║      BARRIER 3        ║
         ║   Final Gate          ║
         ║   /adversary C2       ║
         ║   S-007, S-002, S-014 ║
         ║   >= 0.93             ║
         ╚═══════════════════════╝
                     │
                     ▼
         ┌─────────────────────────┐
         │   HUMAN REVIEW          │
         │   Present results +     │
         │   README diff to user   │
         └─────────────────────────┘
```

### Phase Breakdown

| Phase | ID | Pattern | Agent | Trigger | Deliverables |
|-------|----|---------|-------|---------|--------------|
| 1 — Fix | phase-1 | Sequential | eng-backend | Workflow start | `yaml_frontmatter_reader.py`, `bootstrap.py` mod, `skill-examples.yaml` update |
| 2 — Test | phase-2 | Sequential | eng-qa | Barrier 1 PASS | Integration tests, existing test verification |
| 3 — E2E | phase-3 | Sequential | eng-backend | Barrier 2 PASS | `jerry docs generate --write` executed, README updated, `--check` exit 0 |

---

## L2: Implementation Details

### Files to Create

| File | Purpose |
|------|---------|
| `src/docs/infrastructure/adapters/yaml_frontmatter_reader.py` | New adapter: `IFrontmatterReader` via `yaml.safe_load` |
| `tests/integration/docs/test_yaml_frontmatter_reader.py` | Integration test against real SKILL.md |
| `tests/integration/docs/test_end_to_end.py` | E2E test: extractor with YamlFrontmatterReader → 30 skills |

### Files to Modify

| File | Change |
|------|--------|
| `src/bootstrap.py` | `create_docs_generator()`: swap `AstFrontmatterReader` → `YamlFrontmatterReader` |
| `src/docs/domain/ports/frontmatter_reader.py` | Update docstring to list `YamlFrontmatterReader` as primary implementation |
| `.context/templates/docs/skill-examples.yaml` | Add 17 missing skill examples (30 total) |

### Files NOT Modified (With Justification)

| File | Why |
|------|-----|
| `.context/templates/docs/features.yaml` | **DA-002/DA-005 resolution:** File header states "agent count headline rendered dynamically from `total_agents` (computed at generation time); this file does not need updating for agent count changes." Skill/agent counts are computed by `GenerateDocsCommandHandler` from live extraction — no static counts to update. Feature descriptions (e.g., "9 agents" in Structured Problem-Solving entry) are accurate summaries of per-skill agent counts and do not represent totals. |

### Files NOT Modified (Validation Only)

| File | Why |
|------|-----|
| `src/docs/application/services/skill_extractor.py` | No changes needed — uses `IFrontmatterReader` port correctly. Note: `_extract_agents()` calls `self._reader.read_frontmatter(agent_file)` — this path is ALSO fixed by `YamlFrontmatterReader` since agent files use the same `---`-delimited YAML format. Validated by DA-001 remediation command. |
| `src/docs/application/handlers/commands/generate_docs_command_handler.py` | No changes needed — orchestration logic is correct |
| `src/interface/cli/main.py` | No changes needed — CLI dispatch works |
| `src/interface/cli/parser.py` | No changes needed — args defined correctly |
| `tests/architecture/test_composition_root.py` | **DA-007 resolution:** Verified via `grep -c 'AstFrontmatterReader\|create_docs_generator\|frontmatter' tests/architecture/test_composition_root.py` → 0 matches. File does NOT reference `AstFrontmatterReader`, `create_docs_generator`, or `frontmatter`. Safe from bootstrap.py swap. |
| `tests/unit/docs/test_phase1_evidence.py` | Tests `AstFrontmatterReader` class directly (not via DI). Class file is NOT being deleted — only bootstrap wiring changes. Tests continue to pass because `AstFrontmatterReader` remains importable. |

### skill-examples.yaml: 17 Missing Entries

Existing (13): adversary, architecture, ast, bootstrap, eng-team, nasa-se, orchestration, problem-solving, red-team, saucer-boy, saucer-boy-framework-voice, transcript, worktracker.

Missing (17 — must be added by Phase 1):

| Skill Name | Example (format: `skill-name: '"Example invocation"'`) |
|------------|---------|
| `contract-design` | `'"Generate OpenAPI contract from use case"'` |
| `diataxis` | `'"Write a tutorial for the CLI"'` |
| `pm-pmm` | `'"Create product strategy PRD"'` |
| `prompt-engineering` | `'"Build structured prompt for analysis"'` |
| `test-spec` | `'"Generate test specification"'` |
| `use-case` | `'"Create use case for login flow"'` |
| `user-experience` | `'"Run UX audit on dashboard"'` |
| `ux-ai-first-design` | `'"Evaluate AI-first design patterns"'` |
| `ux-atomic-design` | `'"Build component taxonomy"'` |
| `ux-behavior-design` | `'"Map user behavior triggers"'` |
| `ux-design-sprint` | `'"Plan 5-day design sprint"'` |
| `ux-heart-metrics` | `'"Define HEART metrics for feature"'` |
| `ux-heuristic-eval` | `'"Run heuristic evaluation"'` |
| `ux-inclusive-design` | `'"Audit for accessibility compliance"'` |
| `ux-jtbd` | `'"Map jobs to be done"'` |
| `ux-kano-model` | `'"Classify features with Kano model"'` |
| `ux-lean-ux` | `'"Define lean UX hypothesis"'` |

### Verified Counts (Reproducible Evidence)

| Metric | Command | Result |
|--------|---------|--------|
| Skill count | `ls -d skills/*/SKILL.md \| wc -l` | 30 |
| Agent count | `grep -rh "^name:" skills/*/agents/*.md \| wc -l` | 89 (one `name:` per agent file) |
| One-name-per-file | `for f in skills/*/agents/*.md; do c=$(grep -c "^name:" "$f"); [ "$c" -ne 1 ] && echo "FAIL: $f has $c"; done` | No output (all 89 files have exactly 1 `name:` line) |
| Existing skill-examples | `grep -c '^[a-z]' .context/templates/docs/skill-examples.yaml` | 13 entries |
| DA-007 safety | `grep -c 'AstFrontmatterReader\|create_docs_generator\|frontmatter' tests/architecture/test_composition_root.py` | 0 matches |
| README markers | `grep -c 'BEGIN:GENERATED' README.md` | 2 |

### H-33 Scope Justification

`H-33`: "AST-based parsing REQUIRED for **worktracker entity operations**."

SKILL.md files are NOT worktracker entities. They are Claude Code skill definitions consumed by the runtime. Using `yaml.safe_load` for YAML frontmatter extraction is the correct tool — it's a stdlib YAML parser for YAML content. `jerry ast frontmatter` is designed for blockquote metadata in worktracker entities.

### Execution Validation Requirements

Every phase includes mandatory code execution. "Validated by inspection" is not accepted.

| Phase | Execution Command | Expected Result | DA Reference |
|-------|-------------------|-----------------|--------------|
| 1 | `uv run python -c "from src.docs.infrastructure.adapters.yaml_frontmatter_reader import YamlFrontmatterReader; r = YamlFrontmatterReader(); fm = r.read_frontmatter('skills/adversary/SKILL.md'); assert 'name' in fm, f'Missing name: {fm}'; print(f'OK: name={fm[\"name\"]}')"` | `OK: name=adversary` | — |
| 1 | `uv run python -c "from src.docs.infrastructure.adapters.yaml_frontmatter_reader import YamlFrontmatterReader; r = YamlFrontmatterReader(); fm = r.read_frontmatter('skills/adversary/agents/adv-executor.md'); assert 'name' in fm, f'Missing name: {fm}'; print(f'OK: agent name={fm[\"name\"]}')"` | `OK: agent name=adv-executor` | DA-001 |
| 1 | `uv run python -c "from src.docs.infrastructure.adapters.yaml_frontmatter_reader import YamlFrontmatterReader; r = YamlFrontmatterReader(); fm = r.read_frontmatter('skills/contract-design/SKILL.md'); assert 'name' in fm, f'Missing name: {fm}'; assert len(fm.get('description',''))>50, f'Description too short: {fm.get(\"description\",\"\")}'; print(f'OK: name={fm[\"name\"]}, desc_len={len(fm[\"description\"])}')"` | `OK: name=contract-design, desc_len=...` (>50 chars) | DA-003 |
| 1 | `uv run python -c "from src.docs.infrastructure.adapters.yaml_frontmatter_reader import YamlFrontmatterReader; r = YamlFrontmatterReader(); count = sum(1 for s in __import__('pathlib').Path('skills').glob('*/SKILL.md') if 'name' in r.read_frontmatter(str(s))); print(f'{count}/30 skills have name')"` | `30/30 skills have name` | — |
| 2 | `uv run pytest tests/unit/docs/ -v` | All pass | — |
| 2 | `uv run pytest tests/architecture/ -v` | All pass (bootstrap.py swap safe) | DA-007 |
| 2 | `uv run pytest tests/integration/docs/ -v` | All pass | DA-004 |
| 3 | `grep -c 'BEGIN:GENERATED' README.md` | `2` (markers exist) | DA-006 |
| 3 | `uv run jerry docs generate` | Outputs populated skills table to stdout | — |
| 3 | `uv run jerry docs generate --write` | README.md updated, exit 0 | — |
| 3 | `uv run jerry docs generate --check` | Exit 0 (no drift) | — |
| 3 | `uv run pytest tests/ -v --tb=short` | Full suite passes | — |

### Recovery Strategies

| Failure Mode | Recovery |
|-------------|----------|
| `yaml.safe_load` fails on any SKILL.md | Investigate that specific file; likely non-standard frontmatter delimiter. Check `---` boundary detection logic. |
| `bootstrap.py` swap breaks tests | Revert: `git checkout HEAD -- src/bootstrap.py` to restore `AstFrontmatterReader` wiring. Re-investigate fix approach. |
| Existing unit tests break | Unit tests in `test_phase1_evidence.py` test `AstFrontmatterReader` directly — class is NOT deleted, so these pass. Unit tests that mock `IFrontmatterReader` pass because port contract is unchanged. |
| `--check` exits 1 after `--write` | Marker mismatch in README.md; verify `BEGIN:GENERATED` / `END:GENERATED` markers present (pre-verified: `grep -c 'BEGIN:GENERATED' README.md` → 2) |
| Agent count mismatch | Re-count agents with exclusion filters (TEMPLATE, EXTENSION files). Verify: `grep -rh "^name:" skills/*/agents/*.md \| wc -l` |
| skill-examples.yaml missing key | `jerry docs generate` still works — skill renders with empty example column |

---

## Quality Gates

### Criticality Assessment

**Level:** C2 (Standard)

| Factor | Assessment |
|--------|-----------|
| Reversibility | Reversible within 1 day — new adapter is additive, old adapter remains |
| File scope | 3-5 files modified, 2-3 created (within C2 range) |
| Impact | No new public API surface — same CLI flags, same output format |
| Auto-escalation | AE-005 does NOT apply (no security-relevant code changes; yaml.safe_load is stdlib) |

### Required Strategies (C2)

| ID | Strategy | Application |
|----|----------|-------------|
| S-007 | Constitutional AI Critique | H-07 layer isolation, H-33 scope compliance |
| S-002 | Devil's Advocate | Challenge: is YamlFrontmatterReader the ONLY fix needed? |
| S-014 | LLM-as-Judge | Quality scoring with 6-dimension rubric |

### Optional Strategies

| ID | Strategy | Application |
|----|----------|-------------|
| S-003 | Steelman | Strengthen the fix rationale before critique |
| S-010 | Self-Refine | Agent self-review before presenting |

### Per-Barrier Gate Definitions

| Barrier | Threshold | Creator | Critic | Max Iter |
|---------|-----------|---------|--------|----------|
| Barrier 1 (Fix) | >= 0.93 | eng-backend | adv-scorer | 5 |
| Barrier 2 (Test) | >= 0.93 | eng-qa | adv-scorer | 5 |
| Barrier 3 (E2E) | >= 0.93 | eng-backend | adv-scorer | 5 |

### Operational Score Bands

| Band | Score Range | Action |
|------|------------|--------|
| PASS | >= 0.93 | Advance to next phase |
| REVISE | 0.86 - 0.92 | Targeted revision |
| REJECTED | < 0.86 | Significant rework |

---

## Worktracker Updates Required

After each phase, update the following:

| Entity | Update |
|--------|--------|
| BUG-001 | Status: `in_progress` → `completed` (after Phase 3 PASS) |
| ST-002 | Status: `in_progress` → `completed` (after BUG-001 closed) |
| ST-001 | Status: `in_progress` → `completed` (after README written) |
| FEAT-001 | Verify AC-1 through AC-5 |
| WORKTRACKER.md | Update Discoveries D-002 (stale counts resolved: 30 skills, 89 agents) |

---

## Adversarial Findings Resolution (S-002 Devil's Advocate)

**Source document:** `orchestration/bugfix-20260312-001/impl/adversary-devils-advocate.md`

All 7 findings from the Devil's Advocate review have been addressed:

| ID | Severity | Finding | Resolution |
|----|----------|---------|------------|
| DA-001 | Critical | Agent frontmatter extraction path not validated | Added Phase 1 validation command reading `skills/adversary/agents/adv-executor.md` and asserting `name` present |
| DA-002 | Major | features.yaml doesn't have count fields | Removed features.yaml from Files to Modify; added justification note (counts are dynamic) |
| DA-003 | Major | Complex YAML (>- block scalar) not validated | Added Phase 1 validation command reading `skills/contract-design/SKILL.md` with description length assertion |
| DA-004 | Major | Integration test needs dynamic count assertion | Strengthened Phase 2 constraint: "MUST assert count == len(glob('skills/*/SKILL.md')), NOT hardcoded integer" |
| DA-005 | Major | features.yaml mischaracterized | Same as DA-002; corrected in Files to Modify and scope section |
| DA-006 | Minor | README markers not pre-verified | Added Phase 3 pre-check: `grep -c 'BEGIN:GENERATED' README.md` → 2 |
| DA-007 | Minor | test_composition_root.py may reference AstFrontmatterReader | Verified via grep: file has NO AstFrontmatterReader references. Added to Files NOT Modified with evidence. |

---

## Disclaimer

This orchestration plan was generated on 2026-03-12 for PROJ-0037-doc-module bugfix workflow. It addresses BUG-001 from the prior implementation pipeline (impl-20260310-001). Human review is required before merge.

All paths are relative to `projects/PROJ-0037-doc-module/` unless otherwise stated.
