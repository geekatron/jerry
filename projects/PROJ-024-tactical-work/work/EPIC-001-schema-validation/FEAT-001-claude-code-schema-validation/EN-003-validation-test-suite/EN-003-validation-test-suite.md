# EN-003: Schema Validation Test Suite

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
PURPOSE: Create positive and negative test fixtures for schema validation
-->

> **Type:** enabler
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-03-26T23:30:00Z
> **Due:**
> **Completed:**
> **Parent:** FEAT-001
> **Owner:** adam.nowak
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler covers |
| [Problem Statement](#problem-statement) | Why a test suite is needed |
| [Business Value](#business-value) | How it supports the feature |
| [Technical Approach](#technical-approach) | Test suite design |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## Summary

Create a validation test suite with positive fixtures (valid definitions that must pass) and negative fixtures (common mistakes that must fail) for both agent and skill frontmatter schemas. Without this, schema changes cannot be regression-tested.

**Technical Scope:**
- Positive fixtures: extract frontmatter from existing valid agent/skill definitions
- Negative fixtures: common mistakes from DX review (wrong model, missing required fields, wrong mcpServers format, agent-only fields in skills, etc.)
- Test runner: Python script using `jsonschema` library via `uv run`
- CI integration: run on every PR touching `docs/schemas/`

---

## Problem Statement

C4 adversarial review finding SR-003/PM-005: No validation test suite exists. Schema correctness is unverifiable, and any schema change risks silent regression. The 89 agent definitions and 30 SKILL.md files serve as implicit positive fixtures, but no negative fixtures exist to verify that invalid configurations are correctly rejected.

---

## Business Value

Prevents schema regression. Every schema change can be validated against known-good and known-bad fixtures before merge.

### Features Unlocked

- Confidence in schema changes (no regressions)
- CI gate for schema PRs
- Documentation of expected validation behavior via test fixtures

---

## Technical Approach

1. **Positive fixtures:** Extract YAML frontmatter from 5-10 representative agent definitions and 3-5 SKILL.md files
2. **Negative fixtures:** Create 10+ invalid definitions covering:
   - Missing required fields (name, description)
   - Invalid enum values (model, permissionMode, effort)
   - Wrong type (mcpServers as string, tools as object)
   - Agent-only fields in SKILL.md (tools, disallowedTools, mcpServers)
   - Skill-only fields in agent.md (context, paths, allowed-tools)
   - Name pattern violations (uppercase, underscores, consecutive hyphens)
3. **Test runner:** `uv run python tests/schemas/test_frontmatter_schemas.py`
4. **CI integration:** Add to pre-commit or GitHub Actions

---

## Acceptance Criteria

### Definition of Done

- [ ] 5+ positive fixtures for agent schema (must all pass validation)
- [ ] 3+ positive fixtures for skill schema (must all pass validation)
- [ ] 10+ negative fixtures across both schemas (must all fail validation with expected error)
- [ ] Test runner script at `tests/schemas/test_frontmatter_schemas.py`
- [ ] All tests pass via `uv run pytest tests/schemas/`
- [ ] Test fixtures document the expected error for each negative case

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: Claude Code Schema Validation](../FEAT-001-claude-code-schema-validation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | STORY-004 | Schema fixes should land before test fixtures are finalized |

### Source Findings

| Finding ID | Source | Description |
|-----------|--------|-------------|
| SR-003 | C4 adversarial | No validation test suite exists |
| PM-005 | C4 pre-mortem | Schema regression undetectable |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-26 | adam.nowak | pending | Enabler created from C4 finding SR-003 |
