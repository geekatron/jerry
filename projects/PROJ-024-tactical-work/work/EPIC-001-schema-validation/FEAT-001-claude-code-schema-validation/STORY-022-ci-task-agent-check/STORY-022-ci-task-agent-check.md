# STORY-022: Add Agent-in-Tools CI Validation to validate-agent-frontmatter.py

> **Type:** story
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-29T18:00:00Z
> **Due:**
> **Completed:** 2026-03-29T20:00:00Z
> **Parent:** FEAT-001
> **Owner:** adam.nowak
> **Effort:** 1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | What and why |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Implementation Details](#implementation-details) | Files changed and evidence |
| [Related Items](#related-items) | Links and dependencies |

---

## User Story

**As a** Jerry framework developer

**I want** the CI pipeline to error if any non-T5 agent has `Agent` in its `tools` list

**So that** accidental P-003 violations are caught at PR time

---

## Summary

Red-vuln finding F-006 (STORY-013-M007) identified no CI check exists to verify `Agent` is absent from non-T5 agents' `tools` lists. The `tools` allowlist is the enforcement layer for P-003 (all 89 agents declare it explicitly). A single check is sufficient: error if any non-T5 agent includes `Agent` in `tools`.

Note: `disallowedTools` validation is explicitly out of scope per DISC-001 finding that `disallowedTools` is redundant when `tools` is explicitly declared.

---

## Acceptance Criteria

- [x] `validate-agent-frontmatter.py` errors if `Agent` appears in any non-T5 agent's `tools` field
- [x] CI pipeline runs the check on every PR touching `skills/*/agents/*.md`
- [x] All 89 existing agents pass the new check

---

## Implementation Details

- `scripts/validate-agent-frontmatter.py`: P-003 check in `validate_agent()` with string-format normalization and type-hardened T5 detection via companion `.governance.yaml`
- `scripts/tests/test_validate_agent_frontmatter.py`: 6 tests covering list format, string format, T5 exception, no-agent, missing governance (fail-closed)
- `.github/workflows/ci.yml`: Added script as second validation step (line 213)
- `pytest.ini` + `pyproject.toml`: Added `scripts/tests` to testpaths
- eng-security review: 3 HIGH/MEDIUM findings remediated (string bypass, test gap, type guard)

---

## Related Items

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Informed By | STORY-013 M-007 | UX agents fix revealed CI gap |
| Informed By | red-vuln F-006 | Finding that identified CI enforcement gap |
| Informed By | DISC-001 | disallowedTools redundancy finding scoped out rule 1 |
