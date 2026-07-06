# TASK-006: Strip-Set Correction and Fail-Closed No-Duplicate-Skill-Names Gate (c-007)

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
PURPOSE: Implement the live-install-validated strip-set (skills/.graveyard/, .github/, + recommended docs/scripts/cruft) and add the fail-closed no-duplicate-skill-names generation gate (c-007) plus a CI hook-smoke check
-->

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-07-02T00:00:00Z
> **Completed:**
> **Parent:** STORY-001
> **Owner:** adam.nowak
> **Activity:** development
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Description](#description) | What this task does |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Related Items](#related-items) | Links and GitHub parity |
| [History](#history) | Status changes |

---

## Description

The 2026-07-02 live install test — skeleton force-pushed to the dedicated repo `geekatron/jerry-claude-plugin` (default branch = skeleton) and installed on Claude Web — empirically validated the dedicated-repo distribution model, but reaching a clean install took two fix cycles. Both were caused by the subtractive strip-set ("`main` minus `projects/`+`tests/`") dragging repo-internal cruft that broke Claude's plugin validator:

1. **Duplicate skill name (BLOCKER).** Archived skill `skills/.graveyard/worktracker/SKILL.md` collided by name with the live `skills/worktracker/SKILL.md`; the marketplace rejects duplicate skill names.
2. **Framework CI in the dedicated repo (loop-safety).** The retained `.github/` ran `docs.yml`, spawning a gh-pages deploy inside `jerry-claude-plugin`.

**Validated fix:** expand the strip-set to `projects/ tests/ skills/.graveyard/ .github/` — a 1,399-file tree that installs cleanly. **Recommended additional strip** (non-distribution): `docs/ scripts/ mkdocs.yml CNAME .nojekyll` plus dev/governance cruft, behind a "no retained file references a stripped path" audit (−285 files → ~1,114). **KEEP** `src/` + `pyproject.toml` + `uv.lock` (c-008; the hook -> `uv run jerry` runtime chain; fail-open hooks would silently no-op all guardrails if stripped).

This task **implements** the corrected design already folded into ADR-PROJ031-001 (c-003 retention surface, c-007, c-008), the requirements, the Phase-3 generation + CI design, and the STRIDE model. Concretely it delivers: (a) the corrected strip-set in the regeneration transformation (STORY-001); (b) the **fail-closed no-duplicate-skill-names generation gate (c-007)** inserted as an explicit step between strip and force-push — enumerate every `SKILL.md` in the tip tree, resolve each to its skill name (frontmatter `name`, falling back to the containing directory basename), and abort with a non-zero exit and NO push on any duplicate; and (c) a CI enforcement gate for c-007 plus retention assertions and a post-install hook-smoke check (Phase 5/6).

**Honesty note (P-022):** install-validated does not equal update-propagation-validated (gate G-update remains OPEN) and does not equal hook-execution-validated (fail-open residual) — the hook-smoke check is the defense-in-depth for the latter.

**Ownership (per ADR-PROJ031-001 Phase-3 Mirror Hand-Off):** nse-architecture inserts the generation step; eng-devsecops adds the CI enforcement gate and hook-smoke check.

---

## Acceptance Criteria

- [ ] Regeneration strips the validated set `projects/ tests/ skills/.graveyard/ .github/`, producing a tip tree of ~1,399 tracked files
- [ ] Recommended additional strips (`docs/ scripts/ mkdocs.yml CNAME .nojekyll` + dev/governance cruft) are applied behind a "no retained file references a stripped path" audit (~1,114-file tree)
- [ ] Retention audit confirms `skills/.graveyard/` and `.github/` are ABSENT and the canonical plugin-retention surface plus `src/` + `pyproject.toml` + `uv.lock` (c-003/c-008) are PRESENT at the branch tip
- [ ] c-007 gate enumerates every `SKILL.md` in the tip tree, resolves each to a skill name (frontmatter `name`, fallback to directory basename), and fails closed (non-zero exit, NO push) on any duplicate
- [ ] CI enforces the c-007 gate and the retention assertions on every regeneration (fail-closed, blocks the force-push)
- [ ] Post-install hook-smoke check asserts `uv run jerry hooks session-start` returns non-empty in the installed tree
- [ ] Re-running the corrected generation on the same `main` commit yields the same published result (determinism/idempotency preserved)

---

## Related Items

- **Parent:** [STORY-001: Skeleton Regeneration Script](./STORY-001-regeneration-script.md)
- **Related:** STORY-003 (validation/acceptance gate consumes the corrected output), EN-001 / TASK-002 (regenerate-and-push CI job invokes the corrected strip + c-007 gate), FEAT-002 / STORY-004 (STRIDE loop-safety mirror of the `.github/` fix)
- **Source design:** [ADR-PROJ031-001: Skeleton Derived-Branch Strategy](../../../../decisions/ADR-PROJ031-001-skeleton-distribution-strategy.md) — Phase-3 amendment (c-003 validated strip-set, c-007 no-duplicate-skill-names gate, c-008 runtime-dep retention, recommended additional strips, hook-smoke check)
- **GitHub Issue Parity (H-32):** [#314](https://github.com/geekatron/jerry/issues/314) — tracked under parent Epic [#305](https://github.com/geekatron/jerry/issues/305).

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-07-02 | pending | Task created — captures strip-set correction + c-007 gate + CI hook-smoke check surfaced by the 2026-07-02 live install test |
