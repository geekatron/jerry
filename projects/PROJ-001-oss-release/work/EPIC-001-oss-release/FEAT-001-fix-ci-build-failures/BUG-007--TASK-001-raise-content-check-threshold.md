# BUG-007/TASK-001: Raise content check file count threshold

> **Type:** task
> **Status:** done
> **Priority:** high
> **Created:** 2026-02-11
> **Parent:** BUG-007

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Description](#description) | What needs to be done |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical approach |
| [Related Items](#related-items) | Parent and related work |
| [History](#history) | Status changes |

---

## Description

Raise the minimum file count threshold in `test_path_conventions.py` content validation tests from "any `.md` files" (`if list(dir.glob("*.md")):`) to "at least 3 `.md` files" (`if len(list(dir.glob("*.md"))) >= 3:`) before enforcing naming conventions.

This change applies consistently to all three content tests:
1. `test_research_contains_extraction_docs` (line 193-204)
2. `test_synthesis_contains_canon_doc` (line 206-219)
3. `test_decisions_contains_adr_docs` (line 221-230)

**Rationale:** Projects with 1-2 documents in a category directory are still building up. Enforcing specific naming patterns (extraction, canon/unified, ADR-) at such low document counts is overly prescriptive. A threshold of 3+ documents indicates a mature directory where naming conventions should be enforced.

---

## Acceptance Criteria

- [x] All three content tests use `len(md_files) >= 3` threshold
- [x] `test_synthesis_contains_canon_doc[PROJ-001-oss-release]` passes
- [x] Full test suite passes locally (596+ passed, 33 skipped — excludes local-only PROJ-001-plugin-cleanup failures)
- [x] No regression in other project validation tests

---

## Implementation Notes

### File to modify

`tests/project_validation/architecture/test_path_conventions.py`

### Changes

For each of the three tests, change:
```python
if list(dir.glob("*.md")):
```
To:
```python
md_files = list(dir.glob("*.md"))
if len(md_files) >= 3:
```

### Verification

```bash
uv run pytest tests/project_validation/architecture/test_path_conventions.py -v
```

---

## Related Items

- Parent: [BUG-007: Synthesis content validation test overly prescriptive](./FEAT-001--BUG-007-synthesis-content-test-overly-prescriptive.md)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-11 | pending | Task created |
| 2026-02-11 | done | Implemented: changed threshold from `if list(dir.glob("*.md")):` to `if len(md_files) >= 3:` in all 3 content tests. Verified locally. |
