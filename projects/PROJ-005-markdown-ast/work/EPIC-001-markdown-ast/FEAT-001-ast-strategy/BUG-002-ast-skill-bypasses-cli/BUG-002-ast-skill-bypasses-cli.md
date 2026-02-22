# BUG-002: /ast Skill Bypasses CLI Primary Adapter

> **Type:** bug
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-02-22
> **Due:** --
> **Completed:** --
> **Parent:** FEAT-001
> **Owner:** Claude
> **Found In:** 1.0.0
> **Fix Version:** --

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key details |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the defect |
| [Environment](#environment) | Where the bug occurs |
| [Root Cause Analysis](#root-cause-analysis) | Why this happened |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for fix |
| [Related Items](#related-items) | Hierarchy and related work |
| [History](#history) | Status changes |

---

## Summary

The `/ast` skill (`skills/ast/scripts/ast_ops.py`) imports directly from the domain layer (`src.domain.markdown_ast`) instead of routing through the `jerry ast` CLI, which is the primary adapter for AST operations. This creates two parallel wrappers around the same domain code -- a maintainability and testability defect that violates the primary adapter pattern.

**Key Details:**
- **Symptom:** `ast_ops.py` has 7 functions that each import from `src.domain.markdown_ast` and call domain code directly. The `jerry ast` CLI (`src/interface/cli/ast_commands.py`) does the same thing independently. Two adapters, zero reuse.
- **Frequency:** Permanent architectural defect -- every skill invocation bypasses the CLI.
- **Workaround:** None needed for functionality (both paths work). The defect is structural, not behavioral.

---

## Steps to Reproduce

### Prerequisites

- Jerry framework with PROJ-005 AST infrastructure on `feat/proj-005-markdown-ast` branch

### Reproduction Steps

1. Open `skills/ast/scripts/ast_ops.py` line 39
2. Observe: `from src.domain.markdown_ast import (JerryDocument, extract_frontmatter, ...)`
3. Open `src/interface/cli/ast_commands.py` line 36
4. Observe: `from src.domain.markdown_ast import JerryDocument, get_entity_schema, validate_document`
5. Both files import the same domain layer independently
6. The skill never calls `jerry ast parse`, `jerry ast validate`, or any CLI command

### Expected Result

The `/ast` skill should delegate to the `jerry ast` CLI as the primary adapter. One canonical path to the domain.

### Actual Result

Two parallel adapters exist. The skill bypasses the CLI entirely. 7 functions in `ast_ops.py` duplicate adapter logic that should be in the CLI.

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | macOS / Linux / Windows |
| **Runtime** | Python 3.12+ with UV |
| **Application Version** | Jerry Framework v0.5.0, PROJ-005 branch |
| **Configuration** | Standard Jerry project layout |
| **Deployment** | Local development |

---

## Root Cause Analysis

### Investigation Summary

The defect originates from ST-005's user story definition, which explicitly stated: "So that I can perform structured markdown manipulation during interactive sessions **without shelling out to CLI commands**." This framing led to `ast_ops.py` being designed as a parallel wrapper that imports the domain directly, rather than delegating to the CLI.

### Root Cause

Bad design decision in ST-005. The user story steered implementation away from the CLI, creating a second adapter to the same domain layer. The Pattern D ("Hybrid") architecture in SPIKE-002 described "dual-audience interfaces" but did not specify that the skill should route through the CLI.

### Contributing Factors

- ST-005 user story explicitly discouraged CLI delegation ("without shelling out")
- No architecture review caught the parallel adapter anti-pattern before implementation
- The CLI (ST-004) and skill (ST-005) were developed as siblings, not as a chain
- `ast_ops.py` (424 LOC) grew to 7 operations while the CLI has only 4 commands -- the CLI was never extended to cover all operations

### Gap Analysis

The CLI currently has 4 commands. The skill has 7 operations. Missing from CLI:

| Skill Operation | CLI Equivalent | Status |
|----------------|----------------|--------|
| `parse_file()` | `jerry ast parse` | Exists |
| `query_frontmatter()` | -- | **Missing** |
| `modify_frontmatter()` | -- | **Missing** |
| `validate_file()` | `jerry ast validate` | Exists |
| `render_file()` | `jerry ast render` | Exists |
| `extract_reinject()` | -- | **Missing** |
| `validate_nav_table_file()` | `jerry ast query` (partial) | **Missing (dedicated)** |

4 operations are missing from the CLI. The skill cannot delegate to the CLI until these are added.

---

## Acceptance Criteria

### Fix Verification

- [ ] All 7 `/ast` skill operations route through the `jerry ast` CLI
- [ ] `ast_ops.py` does NOT import from `src.domain.markdown_ast` directly
- [ ] CLI has commands for all 7 operations (4 existing + 3 new)
- [ ] All existing tests pass without modification (or with justified updates)
- [ ] Architecture tests verify no direct domain imports in skill scripts

### Quality Checklist

- [ ] Regression tests added for new CLI commands
- [ ] Existing tests still passing
- [ ] No new issues introduced
- [ ] ST-005 history updated with design correction note

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-001: AST Strategy Evaluation & Library Selection](../FEAT-001-ast-strategy.md)

### Related Items

- **Root Cause Story:** [ST-005: Create /ast Claude Skill](../ST-005-ast-skill/ST-005-ast-skill.md) -- user story steered away from CLI delegation
- **CLI Story:** [ST-004: Add jerry ast CLI Commands](../ST-004-cli-commands/ST-004-cli-commands.md) -- only 4 of 7 operations implemented
- **Architecture:** Pattern D Hybrid from SPIKE-002 feasibility assessment

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-22 | Claude | pending | BUG filed. /ast skill bypasses CLI primary adapter. Root cause: ST-005 user story explicitly discouraged CLI delegation. 4 CLI commands missing to enable full delegation. |
