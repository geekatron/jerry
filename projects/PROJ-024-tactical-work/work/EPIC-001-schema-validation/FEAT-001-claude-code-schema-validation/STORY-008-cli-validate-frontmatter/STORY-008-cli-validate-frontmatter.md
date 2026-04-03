# STORY-008: Add Frontmatter Schema Validation to Jerry CLI

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: Move frontmatter validation from throwaway script into the jerry CLI
-->

> **Type:** story
> **Status:** completed
> **Priority:** high
> **Impact:** medium
> **Created:** 2026-03-27T06:30:00Z
> **Due:**
> **Completed:** 2026-03-27T04:00:00Z
> **Parent:** FEAT-001
> **Owner:** adam.nowak
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | What needs to happen |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** Jerry framework developer

**I want** to run `jerry agents validate-frontmatter` to check all agent and skill .md files against the Anthropic frontmatter schemas

**So that** frontmatter validation is a first-class CLI capability, not a throwaway script, and can be integrated into CI/hooks

---

## Summary

The STORY-005 validation was done via `scripts/validate_all_frontmatter.py` -- a standalone script outside the CLI architecture. This should be a proper `jerry` CLI command following the hexagonal architecture (command -> handler -> adapter). The existing `jerry agents validate` command validates canonical `.agent.yaml` definitions; the new command validates Claude Code `.md` YAML frontmatter against `docs/schemas/claude-code-frontmatter-v1.schema.json` and `docs/schemas/claude-code-skill-frontmatter-v1.schema.json`.

**Options for CLI placement:**
- `jerry agents validate-frontmatter` -- extends the existing agents namespace
- `jerry agents validate --frontmatter` -- adds a flag to existing validate command

**Scope:**
- Command implementation following hexagonal architecture (H-07)
- Migrate validation logic from `scripts/validate_all_frontmatter.py`
- Support `--json` output for CI consumption
- Support `--agent <name>` and `--skill <name>` for single-file validation
- Delete `scripts/validate_all_frontmatter.py` after migration
- Update test suite to test via CLI entry point

---

## Acceptance Criteria

- [ ] `jerry agents validate-frontmatter` runs and produces pass/fail report
- [ ] Validates all agent .md files against agent frontmatter schema
- [ ] Validates all SKILL.md files against skill frontmatter schema
- [ ] `--json` flag produces machine-readable output
- [ ] `--agent <name>` validates a single agent file
- [ ] `--skill <name>` validates a single SKILL.md file
- [ ] `scripts/validate_all_frontmatter.py` deleted (functionality migrated)
- [ ] Existing test suite updated to invoke via CLI
- [ ] Command follows hexagonal architecture (H-07): command in interface/, handler in application/, schema loading in infrastructure/

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Owner |
|----|-------|--------|-------|
| TASK-001 | Add validate-frontmatter subcommand to agents namespace in parser.py | pending | -- |
| TASK-002 | Create ValidateFrontmatterCommand and handler (application layer) | pending | -- |
| TASK-003 | Create schema loading adapter (infrastructure layer) | pending | -- |
| TASK-004 | Wire into CLI adapter dispatch | pending | -- |
| TASK-005 | Update tests to use CLI entry point | pending | -- |
| TASK-006 | Delete scripts/validate_all_frontmatter.py | pending | -- |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: Claude Code Schema Validation](../FEAT-001-claude-code-schema-validation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | EN-003 | Test suite provides test cases to migrate |
| Depends On | STORY-005 | Validation script provides logic to migrate |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-27 | adam.nowak | pending | Story created -- validation logic currently in scripts/validate_all_frontmatter.py needs CLI migration |
