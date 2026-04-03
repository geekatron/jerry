# EPIC-001: Claude Code Schema Validation

<!--
TEMPLATE: Epic
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.3
PURPOSE: Research and create authoritative JSON schemas for Claude Code skill and agent definitions
-->

> **Type:** epic
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-26T22:10:00Z
> **Due:**
> **Completed:**
> **Parent:** PROJ-024
> **Owner:** adam.nowak

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this Epic covers |
| [Children Features/Capabilities](#children-featurescapabilities) | Feature inventory |
| [Progress Summary](#progress-summary) | Overall progress |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## Summary

Research, validate, and create authoritative JSON schemas for Anthropic Claude Code skill (SKILL.md) and agent (.md) definitions. Existing schemas in `docs/schemas/` were created from early documentation and may be incomplete or inaccurate. This epic ensures we have validated, up-to-date schemas that can be used for CI validation, agent governance, and developer tooling.

**Value Proposition:**
- Authoritative schemas prevent silent misconfiguration of skills and agents
- CI validation catches definition errors before they reach runtime
- Developer tooling (autocomplete, linting) improves agent development velocity

---

## Children Features/Capabilities

| ID | Type | Title | Status | Priority |
|----|------|-------|--------|----------|
| FEAT-001 | Feature | Claude Code Schema Validation Research and Refinement | in_progress | high |

### Work Item Links

- [FEAT-001: Claude Code Schema Validation Research and Refinement](./FEAT-001-claude-code-schema-validation/FEAT-001-claude-code-schema-validation.md)

---

## Progress Summary

```
+------------------------------------------------------------------+
|                   EPIC PROGRESS TRACKER                           |
+------------------------------------------------------------------+
| Features:  [##..................] 10% (0/1 completed)             |
+------------------------------------------------------------------+
| Overall:   [##..................] 10%                              |
+------------------------------------------------------------------+
```

---

## Related Items

### Hierarchy

- **Parent Project:** [PROJ-024: Tactical Work](../../PLAN.md)

### Related

- Existing schemas: `docs/schemas/claude-code-frontmatter-v1.schema.json`, `docs/schemas/claude-code-skill-frontmatter-v1.schema.json`, `docs/schemas/agent-governance-v1.schema.json`
- Agent development standards: `.context/rules/agent-development-standards.md` (H-34)
- Skill standards: `.context/rules/skill-standards.md` (H-25, H-26)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-26 | adam.nowak | in_progress | Epic created; research agents launched |
