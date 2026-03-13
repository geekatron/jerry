# BUG-001: AstFrontmatterReader parses blockquote metadata, not YAML frontmatter

> **Type:** bug
> **Status:** completed
> **Priority:** critical
> **Impact:** high
> **Created:** 2026-03-11T00:00:00Z
> **Due:**
> **Completed:** 2026-03-12T00:00:00Z
> **Parent:** ST-002
> **Severity:** critical
> **Owner:**

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Steps to Reproduce](#steps-to-reproduce) | How to trigger the bug |
| [Summary](#summary) | What's broken |
| [Root Cause](#root-cause) | Why it's broken |
| [Evidence](#evidence) | Execution-verified proof |
| [Impact](#impact) | What this blocks |
| [Fix](#fix) | Required changes |
| [Acceptance Criteria](#acceptance-criteria) | How to verify the fix |
| [Related Items](#related-items) | Dependencies |
| [History](#history) | Status changes |

---

## Steps to Reproduce

1. Run `uv run jerry ast frontmatter skills/adversary/SKILL.md`
2. Observe output contains `Version`, `Framework`, `Constitutional Compliance` (blockquote keys) but no `name`
3. Run `uv run jerry docs generate --check`
4. Observe all 27 SKILL.md files skipped with "missing required 'name' field"

---

## Summary

`jerry docs generate` produces empty output. All 27 SKILL.md files are skipped with "missing required 'name' field" because `AstFrontmatterReader` delegates to `jerry ast frontmatter`, which parses blockquote metadata (`> **Key:** Value`) instead of `---`-delimited YAML frontmatter where the `name` field lives.

---

## Root Cause

SKILL.md files contain two metadata formats:

- **Format A** (lines 1-28): `---`-delimited YAML frontmatter with `name`, `description`, `version`, `activation-keywords`. Consumed by Claude Code.
- **Format B** (lines 32+): Blockquote `> **Key:** Value` with `Version`, `Framework`, `Constitutional Compliance`. Consumed by Jerry worktracker.

`jerry ast frontmatter` (`src/domain/markdown_ast/frontmatter.py:46`) uses regex `^>\s*\*\*(?P<key>[^*:]+):\*\*\s*(?P<value>.+)$` which only matches Format B. There is no code path for `---`-delimited YAML.

The research (`doc-module-patterns.md` line 30) incorrectly assumed "`jerry ast` CLI parses YAML frontmatter." This assumption was never verified by execution before implementation.

**Source citations:**
- `frontmatter.py:5` — Module named `BlockquoteFrontmatter`
- `frontmatter.py:46` — Regex only matches `> **Key:** Value`
- `ast_commands.py:454` — Docstring says "Extract **blockquote** frontmatter fields"
- `ast_frontmatter_reader.py:28` — Docstring incorrectly says "parse YAML frontmatter" (documentation error)

---

## Evidence

Verified by code execution on 2026-03-11 post-rebase:

**`jerry ast frontmatter` output (Format B — no `name` key):**
```json
{
  "Version": "1.0.0",
  "Framework": "Jerry Adversarial Quality (ADV)",
  "Constitutional Compliance": "Jerry Constitution v1.0"
}
```

**`yaml.safe_load` output (Format A — has `name` key):**
```
Keys: ['name', 'description', 'version', 'allowed-tools', 'activation-keywords']
name: "adversary"
```

**Result:** 27/27 skills return `has 'name': NO` via `jerry ast frontmatter`. 27/27 return `has 'name': YES` via `yaml.safe_load`.

**`jerry docs generate --check` output:** Exits 1. All 27 skills skipped.

---

## Impact

- **ST-002 (auto-doc module):** BLOCKED. Module produces empty skills table.
- **ST-001 (README update):** BLOCKED. Depends on working doc generation.
- **FEAT-001:** BLOCKED. Both child stories blocked.
- **AC-1 (skills table lists all skills):** FAILS.
- **TASK-006 AC-3 (`jerry docs generate --check` exits 0):** FAILS.

---

## Fix

Create `YamlFrontmatterReader` adapter using `yaml.safe_load` for `---`-delimited YAML:

### Files to create

| File | Purpose |
|------|---------|
| `src/docs/infrastructure/adapters/yaml_frontmatter_reader.py` | New adapter implementing `IFrontmatterReader` using `yaml.safe_load` |

### Files to modify

| File | Change |
|------|--------|
| `src/bootstrap.py` | `create_docs_generator()`: replace `AstFrontmatterReader()` with `YamlFrontmatterReader()` |
| `tests/integration/docs/test_docs_generate.py` | Add integration test using `YamlFrontmatterReader` against real SKILL.md |

### Why a new adapter, not fixing AstFrontmatterReader

- `jerry ast frontmatter` is the correct tool for blockquote metadata — that's what worktracker entities use (H-33).
- SKILL.md files are NOT worktracker entities. H-33 scope: "AST-based parsing REQUIRED for **worktracker entity operations**."
- Mixing YAML and blockquote parsing in one adapter creates semantic ambiguity.
- The `IFrontmatterReader` port allows multiple implementations — this is hexagonal architecture working as designed.

### Expected output after fix

`jerry docs generate --check` will:
1. Read 27 SKILL.md files via `YamlFrontmatterReader`
2. Extract `name`, `description`, `version` from YAML frontmatter
3. Render skills table and features section via Jinja2
4. Compare against README.md markers
5. Exit 0 if current, exit 1 if drift detected

---

## Acceptance Criteria

- [x] `YamlFrontmatterReader` implements `IFrontmatterReader` protocol
- [x] `yaml.safe_load` extracts `name` from all 30 SKILL.md files
- [x] `bootstrap.py` wires `YamlFrontmatterReader` (not `AstFrontmatterReader`) in `create_docs_generator()`
- [x] `uv run jerry docs generate` outputs a populated skills table (30 skills)
- [x] `uv run jerry docs generate --check` exits 0 after `--write`
- [x] Integration test verifies `YamlFrontmatterReader` against a real SKILL.md file
- [x] Existing unit tests still pass (16,062 passed, 0 failed)

---

## Related Items

### Hierarchy

- **Parent Story:** [ST-002](ST-002-auto-doc-module.md)
- **Blocks:** ST-001, FEAT-001, AC-1, TASK-006/AC-3
- **Research:** `projects/PROJ-0037-doc-module/research/doc-module-patterns.md` (incorrect assumption at line 30)
- **Explanation:** `projects/PROJ-0037-doc-module/orchestration/impl-20260310-001/impl/phase-4/frontmatter-issue-explanation.md`
- **Validation:** `projects/PROJ-0037-doc-module/research/extraction-layer-validation.md` (pending creation)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-11 | Claude | open | Bug filed. Discovered during Phase 4 CLI smoke test. Verified post-rebase: 27/27 skills skipped. Root cause: research assumed `jerry ast frontmatter` parses YAML; it parses blockquotes only. |
| 2026-03-12 | Claude | completed | YamlFrontmatterReader created and wired via bugfix-20260312-001 orchestration. 30/30 skills extracted. `jerry docs generate --check` exits 0. 16,062 tests pass. |
