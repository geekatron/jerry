---
title: "CLI Reference Fix Summary -- FM-002 Non-Existent jerry ast validate Command"
status: COMPLETE
date: "2026-03-11"
agent: eng-backend
---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Problem](#problem) | Root cause of the incorrect CLI references |
| [Scope](#scope) | All files examined and changed |
| [Changes Applied](#changes-applied) | Exact replacements made per file |
| [Verification](#verification) | Post-fix grep confirmation |
| [Security Notes](#security-notes) | OWASP / defensive coding relevance |

---

## Problem

The FM-002 implementation added references to `uv run jerry ast validate {artifact_path} --schema use_case_realization` in both `uc-slicer.md` and `uc-author.md`. This command does NOT exist. The `jerry ast validate` CLI only supports built-in worktracker entity types (epic, feature, story, task, bug, enabler, etc.) -- it does not accept an arbitrary `--schema` flag pointing to external JSON Schema files such as `use-case-realization-v1.schema.json`.

Consequence of leaving these references in place: agents executing Step 8 of the slicing methodology or the Post-Creation / Post-Update Verification steps would invoke a non-existent CLI command, receive an error, and have no actionable fallback path for validating the allOf schema constraints.

---

## Scope

Four files were examined. Three of the four required changes.

| File | Changes Required | Changes Applied |
|------|-----------------|-----------------|
| `skills/use-case/agents/uc-slicer.md` | Yes | 3 occurrences fixed |
| `skills/use-case/agents/uc-author.md` | Yes | 2 occurrences fixed |
| `skills/use-case/agents/uc-slicer.governance.yaml` | Yes | 3 occurrences fixed |
| `skills/use-case/agents/uc-author.governance.yaml` | Yes | 1 occurrence fixed |

---

## Changes Applied

### uc-slicer.md

**Occurrence 1 -- Methodology Step 8 (line 93):**

Removed:
> `run \`uv run jerry ast validate {artifact_path} --schema use_case_realization\` to verify the allOf constraint passes`

Replaced with:
> `verify the output artifact's YAML frontmatter satisfies the allOf constraints defined in \`docs/schemas/use-case-realization-v1.schema.json\`. Check: (1) goal_symbol matches goal_level, (2) if realization_level is INTERACTION_DEFINED then interactions[] must have minItems: 1, (3) if realization_level is STORY_DEFINED then slices[] must have minItems: 1, (4) if detail_level is ESSENTIAL_OUTLINE or FULLY_DESCRIBED then extensions[] must have minItems: 1, (5) INTERACTION_DEFINED is not permitted with BRIEFLY_DESCRIBED or BULLETED_OUTLINE detail_level`

**Occurrence 2 -- Post-Update Verification intro (line 145):**

Removed:
> `verify by running \`uv run jerry ast validate {artifact_path} --schema use_case_realization\` and confirming`

Replaced with:
> `verify by manually checking the YAML frontmatter satisfies the allOf constraints defined in \`docs/schemas/use-case-realization-v1.schema.json\` and confirming`

**Occurrence 3 -- Post-Update Verification item 1 (line 146):**

Removed:
> `Artifact validates against \`docs/schemas/use-case-realization-v1.schema.json\` including allOf constraints (run \`uv run jerry ast validate {artifact_path} --schema use_case_realization\`)`

Replaced with the five explicit allOf constraint checks (goal_symbol/goal_level consistency, INTERACTION_DEFINED requires interactions[], STORY_DEFINED requires slices[], ESSENTIAL_OUTLINE/FULLY_DESCRIBED require extensions[], INTERACTION_DEFINED not permitted with BRIEFLY_DESCRIBED/BULLETED_OUTLINE). The inline note about CLI validation at Step 8 was also updated to read "enforced by allOf schema constraint verified at Step 8" (removing the erroneous CLI claim).

---

### uc-author.md

**Occurrence 1 -- Post-Creation Verification intro (line 149):**

Removed:
> `verify by running \`uv run jerry ast validate {artifact_path} --schema use_case_realization\` and confirming`

Replaced with:
> `verify by manually checking the YAML frontmatter satisfies the allOf constraints defined in \`docs/schemas/use-case-realization-v1.schema.json\` and confirming`

**Occurrence 2 -- Post-Creation Verification item 2 (line 151):**

Removed:
> `YAML frontmatter validates against \`docs/schemas/use-case-realization-v1.schema.json\` (run \`uv run jerry ast validate {artifact_path} --schema use_case_realization\`)`

Replaced with the same five explicit allOf constraint checks as above, making the verification procedure actionable without any CLI dependency.

---

### uc-slicer.governance.yaml

**Occurrence 1 -- output_filtering entry (line 46):**

Removed:
> `"realization_level_must_match_populated_blocks (enforced by allOf schema constraint + jerry ast validate post-creation check)"`

Replaced with:
> `"realization_level_must_match_populated_blocks (enforced by allOf schema constraint + manual frontmatter verification against docs/schemas/use-case-realization-v1.schema.json)"`

**Occurrence 2 -- post_completion_checks entry (line 78):**

Removed:
> `"verify_detail_level_realization_level_cross_constraint_via_ast_validate"`

Replaced with:
> `"verify_frontmatter_satisfies_use_case_realization_schema_allOf_constraints"`

**Occurrence 3 -- post_completion_checks entry (line 79):**

Removed:
> `"verify_realization_level_allOf_constraint_via_jerry_ast_validate"`

Replaced with:
> `"verify_frontmatter_realization_level_allOf_constraint_satisfied_before_state_transition"`

Note: The two post_completion_checks were semantically distinct (cross-constraint vs. allOf specifically), so distinct replacement strings were chosen to preserve their individual intent rather than deduplicating them.

---

### uc-author.governance.yaml

**Occurrence 1 -- post_completion_checks entry (line 71):**

Removed:
> `"verify_yaml_frontmatter_validates_against_schema_via_jerry_ast_validate"`

Replaced with:
> `"verify_frontmatter_satisfies_use_case_realization_schema_allOf_constraints"`

---

## Verification

After all edits, a grep scan of `skills/use-case/agents/` for both `jerry ast validate` and `--schema use_case_realization` returned zero matches, confirming complete removal of the non-existent CLI references.

---

## Security Notes

This fix is a defensive coding correctness issue rather than a security vulnerability. However, it is aligned with OWASP ASVS 5.0 V14.2 (Dependency verification -- ensuring agents do not depend on non-existent runtime commands that would silently fail or produce unexpected behavior). Failing to validate schema constraints at the correct trust boundary (artifact creation time) could allow malformed use case artifacts to pass into downstream /contract-design and /test-spec pipelines, producing invalid API contracts or test specifications.

The correct mitigation -- manual inspection of YAML frontmatter against the five enumerated allOf constraints in `docs/schemas/use-case-realization-v1.schema.json` -- provides equivalent enforcement without a runtime CLI dependency.

---

*Generated by eng-backend on 2026-03-11*
