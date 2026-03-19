# The YamlFrontmatterReader Issue — Explained

## The One-Sentence Version

`jerry ast frontmatter` is the wrong tool for SKILL.md files — it extracts blockquote metadata instead of YAML frontmatter, so the doc module sees zero skills.

---

## The Two Formats

SKILL.md files contain **two** different metadata formats in the same file. Here's what the top of `skills/adversary/SKILL.md` looks like:

```markdown
---                                          ← FORMAT A: YAML frontmatter
name: adversary                              ← (this is what we need)
description: On-demand adversarial quality...
version: "1.0.0"
activation-keywords:
  - "adversarial review"
  - "adversary"
---                                          ← end of YAML frontmatter

# Adversary Skill

> **Version:** 1.0.0                         ← FORMAT B: Blockquote metadata
> **Framework:** Jerry Adversarial Quality    ← (this is what jerry ast reads)
> **Constitutional Compliance:** Jerry...
```

**Format A** (`---`-delimited YAML) is what Claude Code and the doc module need — it has `name`, `description`, `version`, `activation-keywords`.

**Format B** (blockquote `> **Key:** Value`) is what worktracker entities use, and what `jerry ast frontmatter` was built to parse.

---

## What Goes Wrong

The doc module's `AstFrontmatterReader` calls `jerry ast frontmatter` on each SKILL.md file. Here's the actual output:

```
$ uv run jerry ast frontmatter skills/adversary/SKILL.md
{
  "Version": "1.0.0",
  "Framework": "Jerry Adversarial Quality (ADV)",
  "Constitutional Compliance": "Jerry Constitution v1.0",
  "SSOT Reference": "`.context/rules/quality-enforcement.md`..."
}
```

Notice: the returned JSON has `"Version"` (from the blockquote) but **no `"name"` key**. The YAML frontmatter's `name: adversary` is completely ignored.

**Confusing detail:** the `AstFrontmatterReader` adapter's own docstring (`ast_frontmatter_reader.py:28`) says it "parses YAML frontmatter" — but that's a documentation error in the adapter. The underlying `jerry ast frontmatter` command is explicitly a blockquote parser. You can confirm this in the source:

- `ast_commands.py:454` — the function's docstring says "Extract **blockquote** frontmatter fields from a markdown file as JSON"
- `frontmatter.py:46` — the sole extraction regex is `^>\s*\*\*(?P<key>[^*:]+):\*\*\s*(?P<value>.+)$` — this only matches `> **Key:** Value` lines
- `frontmatter.py:5` — the module is named `BlockquoteFrontmatter`

There is no code path in the parser for `---`-delimited YAML. When `jerry ast frontmatter` is pointed at a SKILL.md file, it scans the entire file with that blockquote regex, finds the `> **Version:** 1.0.0` lines (Format B), and returns them. It skips right over the YAML frontmatter (Format A) because `---` delimiters don't match the regex.

Back in the `SkillExtractor`, the code does:

```python
# skill_extractor.py:110-115
raw_name = frontmatter.get("name")    # Returns None — no "name" in blockquote data
if not raw_name:
    logger.warning(
        "Skipping %s: missing required 'name' field", skill_file
    )
    return None                        # ← Every skill hits this path
```

Result: all skills are skipped (currently 13 — one per `skills/*/SKILL.md` directory). Each of these 13 files has a `---` YAML block containing a `name` field at line 2, so all 13 would be successfully extracted by a reader that parses Format A. The doc module generates an empty skills table.

---

## Why Tests Didn't Catch It

All 51 unit tests mock `IFrontmatterReader`:

```python
mock_reader.read_frontmatter.return_value = {
    "name": "test-skill",
    "description": "A test skill",
    "version": "1.0.0",
}
```

These mocks always return a dict with `"name"` in it — exactly what Format A (YAML frontmatter) would produce. No test ever calls the real `AstFrontmatterReader` against a real SKILL.md file. The mismatch is invisible at the unit level.

The defect was only caught by the Phase 4 CLI smoke test: `uv run jerry docs generate --check`.

---

## The Fix: YamlFrontmatterReader

The recommended fix is to create a second adapter — `YamlFrontmatterReader` — that reads Format A directly:

```
IFrontmatterReader (port/interface)
    ├── AstFrontmatterReader   → uses jerry ast frontmatter → reads Format B (blockquotes)
    └── YamlFrontmatterReader  → uses yaml.safe_load        → reads Format A (--- delimited)
```

**Why not just fix `AstFrontmatterReader`?** Because `jerry ast frontmatter` is the right tool for blockquote parsing — that's what worktracker entities use. Mixing YAML frontmatter parsing into an adapter designed for blockquote extraction creates semantic ambiguity: the same reader would behave differently depending on which metadata format it encounters first. Keeping them separate means each adapter does one thing, and changing one can't break the other.

**Why a new adapter instead of inlining `yaml.safe_load` in the extractor?** The `SkillExtractor` is in the application layer. It talks to the domain port `IFrontmatterReader`, not to infrastructure directly. Adding `yaml.safe_load` inside the extractor would violate the hexagonal layer boundary (H-07) — the extractor shouldn't know *how* frontmatter is parsed, only that it gets a dict back. A new adapter preserves this separation. (The port's docstring would also be updated to list `YamlFrontmatterReader` as a second implementation.)

**Does this violate H-33?** No. H-33 says "AST-based parsing REQUIRED for worktracker entity operations." SKILL.md and agent `.md` files are not worktracker entities. They're skill definitions consumed by Claude Code. Using `yaml.safe_load` on them is perfectly valid.

The composition root (`bootstrap.py`) would wire the correct reader:

```python
def create_docs_generator(...):
    reader = YamlFrontmatterReader()   # reads --- YAML frontmatter
    extractor = SkillExtractor(reader)
    # ...
```

**After the fix:** `jerry docs generate` would correctly extract all 13 skills and produce a populated skills table in the README. An integration test exercising `YamlFrontmatterReader` against a real SKILL.md would also be added to prevent this class of defect from recurring.
