# PROJ-012: Agent Definition Optimization — Work Tracker

## Summary

| Metric | Value |
|--------|-------|
| Total Items | 5 |
| Completed | 2 |
| In Progress | 3 |
| Blocked | 0 |

## Work Items

| ID | Type | Title | Status | Parent |
|----|------|-------|--------|--------|
| EN-006 | Enabler | `jerry agents compose` CLI and doc alignment | Done | PROJ-012 |
| EN-007 | Enabler | Skill composition pipeline FMEA hardening | Done | PROJ-012 |
| BUG-001 | Bug | Broken XML tag nesting in composed agent files | In Progress | PROJ-012 |
| BUG-002 | Bug | SKILL.md governance sections missing XML tags per spec | In Progress | PROJ-012 |
| BUG-003 | Bug | Inconsistent body_format (XML vs markdown) across agents in same skill | In Progress | PROJ-012 |

### EN-006: `jerry agents compose` CLI and Doc Alignment

**Status:** Done
**Criticality:** C2 (Standard)
**GitHub Issue:** [#93](https://github.com/geekatron/jerry/issues/93)
**Quality Gate:** PASS — 0.935 (C3 adversarial review on doc alignment subset)

**Scope:**
- `jerry agents compose all` / `jerry agents compose <name>` CLI command
- Defaults-then-override composition pipeline (`jerry-claude-agent-defaults.yaml`)
- Schema path alignment across rule files, CLAUDE.md, AGENTS.md, knowledge docs
- 58 composed `.claude/agents/*.md` files generated and committed
- `--clean` and `--output-dir` flags
- JSON output mode (`--json`)

**Files Changed:**
- Infrastructure: `agent_config_resolver.py` (ComposeResult, compose_agent_to_file, compose_all_to_dir)
- Application: `agent_config_queries.py`, `agent_config_query_handlers.py`, `bootstrap.py`
- Interface: `parser.py`, `adapter.py`, `main.py`
- Docs: `agent-development-standards.md` v1.3.0, `CLAUDE.md`, `AGENTS.md`, `SCHEMA_VERSIONING.md`, `jerry-vs-anthropic-best-practices.md`
- Tests: 22 new tests (14 resolver, 3 handler, 5 integration)
- Generated: 58 `.claude/agents/*.md` composed agent files

**Adversarial Review:**
- Strategies executed: S-003, S-007, S-004, S-012, S-013, S-002, S-014
- Findings resolved: F-01 (L3 claim corrected), F-02 (historical exclusion documented), F-03 (AGENTS.md provenance)
- False findings dismissed: DA-001, DA-004 (pre-existing content, not in diff)
- Score progression: 0.861 → 0.935 → ~0.95 (3 iterations)

### EN-007: Skill Composition Pipeline FMEA Hardening

**Status:** Done
**Criticality:** C2 (Standard)
**Quality Gate:** PASS — 0.925 (S-014 iteration 4, C2 adversarial review)
**FMEA Source:** `projects/PROJ-012-agent-optimization/reviews/s-012-fmea-skill-pipeline.md`

**Problem:** S-012 FMEA identified 9 open failure modes in the skill composition pipeline. These are defense-in-depth gaps that must be addressed before shipping.

**Tasks:**

| # | FM-ID | RPN | Task | Status |
|---|-------|-----|------|--------|
| 1 | FM-03 | 224 | Add SCV-007: canonical name == frontmatter name cross-file check | Done |
| 2 | FM-02 | 192 | Surface parse errors from `list_all()` instead of silent skip | Done |
| 3 | FM-05 | 189 | Add CI sync check for `$defs/skill_name` between schemas | Done |
| 4 | FM-12 | 150 | Document compose workflow; add compose-then-validate pre-commit hook | Done |
| 5 | FM-08 | 128 | Emit warning when SCV-004 skips due to missing `jsonschema` | Done |
| 6 | FM-01 | 126 | Document branch protection recommendation for CI gating | Done |
| 7 | FM-06 | 108 | Add regression test for heading dedup with HTML comment spacing | Done |
| 8 | FM-13 | 108 | Use `sort_keys=True` for `context_injection` YAML output | Done |
| 9 | FM-07 | 100 | Broaden footer regex to handle bold/alternative formats | Done |

**Acceptance Criteria:**
- [x] All 9 FMEA findings addressed with code changes or documented recommendations
- [x] New SCV-007 check validates canonical name vs frontmatter name
- [x] `list_all()` surfaces parse errors to caller
- [x] Schema `$def` duplication detected by CI sync check in `check_skill_schemas.py`
- [x] All existing tests pass + new tests for each fix (14423 passed, 0 failed)
- [x] Adversarial review (C2+) scores >= 0.92 — PASS 0.925 (4 iterations)

**Quality Gate Revisions (iteration 2):**
- S-014 iteration 1: 0.879 REVISE — 4 targeted revision actions identified
- Rev-1: Added FM-13 determinism test (dict insertion order independence) — 2 new tests
- Rev-2: Documented `list_all()` diagnostic discard in ISkillRepository + implementation docstrings
- Rev-3: Added FM-ID traceability comments at 5 fix sites (FM-03, FM-06, FM-07, FM-08, FM-13)
- Rev-4: Elevated FM-01 branch protection to `docs/knowledge/ci-gate-configuration.md`
- S-014 iteration 2: 0.880 REVISE — 3 Methodological Rigor gaps identified
- Rev-5: Clarified FM-01 D-score rationale (D=2 pre-existing CI detection vs FM-12 D=3 documentation-only)
- Rev-6: Added below-threshold disposition table for FM-09, FM-10, FM-14 (accepted risk)
- Rev-7: Added CI job name verification guidance to `ci-gate-configuration.md`
- S-014 iteration 4: 0.925 PASS — quality gate cleared

### BUG-001: Broken XML Tag Nesting in Composed Agent Files

**Status:** In Progress
**Criticality:** C2 (Standard)
**Discovered:** Post-EN-007 regression analysis (compose output diff vs main)

**Problem:** The compose pipeline produces structurally broken XML in several composed agent `.md` files. Defects include:
- Duplicate opening/closing XML tags (e.g., `<execution_process>` nested inside itself in `adv-executor.md`)
- Misplaced closing tags — closer for previous section emitted at start of next section
- Governance sections placed outside `<agent>` wrapper element (~6 diataxis agent files)

**Affected Files:**
- `skills/adversary/agents/adv-executor.md` — duplicate `<execution_process>` open/close, misplaced `</output_format>` and `</constitutional_compliance>`
- `skills/diataxis/agents/diataxis-auditor.md` — governance sections outside `</agent>` wrapper
- ~4-5 additional diataxis agent files with same `</agent>` wrapper issue

**Root Cause:** The compose pipeline's body assembly logic does not correctly handle XML tag boundaries when injecting governance sections. The governance section injector appends after the last content section but does not account for the `</agent>` closing wrapper tag.

**Acceptance Criteria:**
- [ ] All 67 composed agent files pass XML structural validation (no duplicate tags, no misplaced closers)
- [ ] Governance sections are inside `<agent>` wrapper in all files
- [ ] Re-compose all agents and diff confirms clean output
- [ ] No content regression vs main (same prompt body content preserved)
- [ ] Automated XML structural integrity check added (post-compose assertion or pre-commit hook) — prevents broken XML from shipping undetected
- [ ] XML validation runs on all 67 agent files AND all 15 SKILL.md files in CI (or compose pipeline) with zero tolerance for nesting errors

### BUG-002: SKILL.md Governance Sections Missing XML Tags Per Spec

**Status:** In Progress
**Criticality:** C2 (Standard)
**Discovered:** Post-EN-007 regression analysis

**Problem:** The `agent-development-standards.md` v1.3.0 spec (H-34) states governance metadata is "injected into the prompt body as XML sections." For agents, this is partially implemented (XML tags present but with nesting bugs per BUG-001). For SKILL.md files, the `SkillGovernanceSectionBuilder` emits **markdown `##` headings** (`## Skill Version`, `## Activation Keywords`, `## Agent Registry`, `## Context Injection`) — not XML tags.

The builder source code explicitly comments: "Unlike agents, no XML transformation is needed — SKILL.md body is human-authored documentation consumed by the MAIN CONTEXT."

**Investigation Findings:**
- 15/15 SKILL.md files modified on this branch
- All governance sections use `## Heading` format, zero use XML tags
- Governance fields successfully moved from frontmatter YAML to body sections (non-regressive data migration)
- The `SkillGovernanceSectionBuilder` was intentionally coded for markdown headings

**Decision Required:** The spec says XML sections. The implementation says markdown headings with an explicit design comment justifying the deviation. Either:
- (A) Update `SkillGovernanceSectionBuilder` to emit XML tags for SKILL.md governance sections (align code to spec)
- (B) Update spec to document that SKILL.md uses `##` headings while agents use XML tags (align spec to code with rationale)

**Rationale for (B):** SKILL.md files are human-authored documentation loaded into MAIN CONTEXT. XML tags add parsing overhead for content that isn't consumed by a subagent. Agent `.md` files are system prompts consumed by subagents where XML tag delineation aids section parsing.

**Acceptance Criteria:**
- [ ] Decision documented (A or B)
- [ ] Implementation matches spec (whichever direction chosen)
- [ ] All 15 SKILL.md files consistent with chosen format

### BUG-003: Inconsistent body_format Across Agents in Same Skill

**Status:** In Progress
**Criticality:** C2 (Standard)
**Discovered:** Post-EN-007 regression analysis (compose output diff vs main)

**Problem:** Composed agent files use mixed governance section formats within the same skill:

| Skill Group | Format | Example Agents |
|-------------|--------|----------------|
| adversary | Mixed — `adv-executor` uses XML tags; `adv-scorer`, `adv-selector` use `##` headings | adv-executor, adv-scorer, adv-selector |
| diataxis | Mixed — classifier/writers use XML; auditor uses markdown | diataxis-classifier, diataxis-auditor |
| problem-solving, nasa-se, orchestration, transcript | XML tags | ps-researcher, nse-explorer, etc. |
| eng-team, red-team, saucer-boy, worktracker | Markdown headings | eng-architect, red-lead, sb-voice, etc. |

The `portability.body_format` field in `.jerry.yaml` sources declares `xml` or `markdown`, so this may be intentional per-agent configuration. However, agents within the same skill having different formats creates inconsistency.

**Root Cause:** The compose pipeline reads `body_format` from each agent's canonical `.jerry.yaml` and emits governance sections in the declared format. Some `.jerry.yaml` files declare `xml`, others `markdown`. No skill-level consistency constraint exists.

**Investigation Required:**
- [ ] Audit all `.jerry.yaml` `portability.body_format` values
- [ ] Determine if mixed formats within a skill are intentional or accidental
- [ ] If accidental: standardize to one format per skill (or globally)
- [ ] If intentional: document the rationale

**Acceptance Criteria:**
- [ ] All agents within each skill use consistent governance section format
- [ ] `body_format` values in `.jerry.yaml` sources are intentional and documented
- [ ] Re-compose and verify consistency
