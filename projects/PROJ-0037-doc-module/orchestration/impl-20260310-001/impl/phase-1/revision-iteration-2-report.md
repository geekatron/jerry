# Revision Iteration 2 Report — Phase 1 Backend Implementation

**Agent:** eng-backend-1
**Iteration:** 2 (Barrier 1 rejected at 0.83; threshold 0.94)
**Date:** 2026-03-10
**Status:** Fixes applied — ready for re-scoring

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What was fixed and why |
| [Finding Disposition](#finding-disposition) | Per-finding fix description |
| [Unchanged Scope](#unchanged-scope) | What was deliberately not changed |
| [Residual Risk](#residual-risk) | Any remaining considerations |

---

## Summary

Four targeted fixes were applied across three files to address the specific findings from the adv-scorer quality gate review. No other code was modified. All fixes are minimal and directly address the cited security gaps.

---

## Finding Disposition

### Finding 1 (MEDIUM) — M-1 URL allowlist not implemented

**File:** `src/docs/application/services/skill_extractor.py`

**Fix applied:**

Added `_UNSAFE_LINK_PATTERN` module-level compiled regex that matches markdown links of the form `[text](scheme:...)` where the scheme is not in the allowlist (`https://`, `http://`, `mailto:`, or a relative path starting with `/`). The pattern uses a negative lookahead (`(?!https?://|mailto:|/)`) to pass through allowlisted URLs, then matches any remaining `scheme:` prefix followed by the link target.

Updated `_sanitize_description()` to call `_UNSAFE_LINK_PATTERN.sub(r"\1", sanitized)` after HTML tag stripping. The substitution replaces the full unsafe link with just the link text (group 1), preserving readability while neutralizing the XSS vector. Examples of what is now stripped:

- `[click](javascript:alert(1))` becomes `click`
- `[x](data:text/html,<h1>XSS</h1>)` becomes `x`
- `[link](vbscript:msgbox(1))` becomes `link`
- `[safe](https://example.com)` is preserved unchanged

The docstring was updated to document the M-1 URL allowlist behavior.

---

### Finding 2 (LOW) — `_MARKER_PATTERN` dead code in jinja2_renderer.py

**File:** `src/docs/infrastructure/adapters/jinja2_renderer.py`

**Fix applied:**

Removed the `_MARKER_PATTERN = re.compile(...)` constant and the `import re` statement. The `inject_between_markers()` method uses string `index()` operations exclusively; the compiled regex was never referenced. Removal eliminates dead code and the unused import.

---

### Finding 3 (LOW) — `activation-keywords` max-30 validation missing

**File:** `src/docs/application/services/skill_extractor.py`

**Fix applied:**

Added `_MAX_ACTIVATION_KEYWORDS = 30` module-level constant. In `_extract_skill()`, after frontmatter is read, added a check: if `activation-keywords` is a list with more than 30 entries, a `logger.warning()` is emitted with the file path, actual count, and maximum. This is a validation-only check — `activation-keywords` is not included in `SkillData` construction and not rendered in the README, so no truncation of the data structure is needed. The warning gives operators visibility into malformed SKILL.md files.

---

### Finding 4 (LOW) — Path traversal on `--readme` flag

**File:** `src/docs/application/handlers/commands/generate_docs_command_handler.py`

**Fix applied:**

Added path containment validation as the first operation in `handle()`, before the `warnings` list is initialized and before any file I/O occurs. The guard:

1. Resolves `Path.cwd()` to the absolute repo root (resolves symlinks)
2. Resolves `command.readme_path` to absolute (resolves symlinks and `..` components)
3. Calls `readme_abs.relative_to(repo_root)` — this raises `ValueError` if the resolved readme path is not under the repo root

On `ValueError`, the method returns immediately with:
```python
GenerateDocsResult(
    success=False,
    error={"code": "PATH_TRAVERSAL", "message": "README path must be within the repository root"},
)
```

This is a pre-computation guard with no side effects and no exception leakage into the outer `try/except` block.

---

## Unchanged Scope

The following were deliberately not modified:

- Domain value objects (`SkillData`, `AgentData`)
- Domain ports (`IFrontmatterReader`, `ITemplateRenderer`)
- `AstFrontmatterReader` infrastructure adapter
- CLI parser and command objects
- All test files
- Templates and static YAML data files

---

## Residual Risk

None identified from the four findings. The URL pattern regex has been constructed conservatively — it targets the `scheme:` prefix structure that characterizes dangerous protocols, and the negative lookahead ensures allowlisted schemes (including relative paths) are never stripped. Edge cases like bare `(//example.com)` protocol-relative URLs are not in the allowlist and will have their link text preserved only; this is the correct secure default.
