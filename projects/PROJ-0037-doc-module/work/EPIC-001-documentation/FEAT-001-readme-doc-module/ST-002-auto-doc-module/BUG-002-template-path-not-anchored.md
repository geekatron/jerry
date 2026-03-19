# BUG-002: Template path not anchored to repo root

> **Type:** bug
> **Status:** completed
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-03-18T00:00:00Z
> **Due:**
> **Completed:** 2026-03-18T00:00:00Z
> **Parent:** ST-002
> **Severity:** minor
> **Owner:**

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What's broken |
| [Steps to Reproduce](#steps-to-reproduce) | How to trigger the bug |
| [Root Cause](#root-cause) | Why it's broken |
| [Acceptance Criteria](#acceptance-criteria) | How to verify the fix |
| [Related Items](#related-items) | Dependencies |
| [History](#history) | Status changes |

---

## Summary

Template directory path `".context/templates/docs"` is hardcoded as a relative path in both `bootstrap.py` and `generate_docs_command_handler.py`. This resolves against `Path.cwd()`, so if the CLI is invoked from a subdirectory (e.g., `cd src && uv run jerry docs generate`), the template directory is not found.

The `Jinja2Renderer.__init__` raises `FileNotFoundError` with a helpful message, so the failure is graceful — but the module should work regardless of CWD.

---

## Steps to Reproduce

1. Navigate to a subdirectory: `cd src/`
2. Run `uv run jerry docs generate`
3. Observe `FileNotFoundError: Template directory not found: '.context/templates/docs'. Ensure you are running from the repository root.`

### Expected Result

Docs generation works from any directory within the repository.

### Actual Result

Fails unless CWD is the repository root.

---

## Root Cause

Four locations use relative paths that resolve against CWD:

| File | Line | Path |
|------|------|------|
| `src/bootstrap.py` | 817 | `Jinja2Renderer(template_dir=".context/templates/docs")` |
| `src/docs/application/handlers/commands/generate_docs_command_handler.py` | 36 | `_TEMPLATE_DIR = ".context/templates/docs"` |
| `src/docs/application/handlers/commands/generate_docs_command_handler.py` | 131-132 | `Path(_TEMPLATE_DIR) / _SKILL_EXAMPLES_FILE` |
| `src/docs/application/services/skill_extractor.py` | 83 | `glob(str(Path(skills_dir) / "*" / "SKILL.md"))` — caller passes `"skills/"` |

The composition root (`bootstrap.py`) should resolve the template directory relative to the repo root and pass an absolute path to downstream components.

---

## Acceptance Criteria

- [ ] `uv run jerry docs generate` works when invoked from any subdirectory within the repository
- [ ] Template directory is resolved to an absolute path in the composition root (`bootstrap.py`)
- [ ] Existing tests continue to pass (59 doc tests, full suite)
- [ ] No hardcoded relative paths remain in the rendering pipeline for template or data file loading

---

## Related Items

- **Parent:** [ST-002](ST-002-auto-doc-module.md)
- **Found by:** /eng-team security-aware code review (MEDIUM-1 finding)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-18 | Claude | pending | Filed from /eng-team code review MEDIUM-1 finding |
| 2026-03-18 | Claude | completed | Fix: bootstrap.py discovers repo root via pyproject.toml walk-up; handler uses self._repo_root for all path resolution including path traversal guard. /adversary scored, revision applied. 59/59 doc tests pass. |
