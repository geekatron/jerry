# TASK-001: Implement DocsGenerator handler + SkillExtractor service + infrastructure adapters

> **Type:** task
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-10T00:00:00Z
> **Due:**
> **Completed:** 2026-03-10T00:00:00Z
> **Parent:** ST-002
> **Owner:** eng-backend-1
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable criteria |
| [Related Items](#related-items) | Dependencies |

---

## Summary

Phase 1 of the implementation pipeline. Build the 4 core bounded context files:
- `GenerateDocsCommandHandler` (application handler)
- `SkillExtractor` (application service)
- `Jinja2Renderer` (infrastructure adapter)
- `AstFrontmatterReader` (infrastructure adapter)

Plus all required `__init__.py` package files.

---

## Acceptance Criteria

- [ ] `GenerateDocsCommandHandler` accepts `SkillExtractor`, `ITemplateRenderer`, `IFrontmatterReader` via constructor injection
- [ ] `SkillExtractor.extract_all()` validates name regex, strips HTML, enforces length limits (M-1, M-5)
- [ ] `Jinja2Renderer` uses `SandboxedEnvironment` + `StrictUndefined` (M-2)
- [ ] `AstFrontmatterReader` calls `uv run jerry ast frontmatter` via subprocess (H-05, H-33)
- [ ] Atomic write uses `tempfile.NamedTemporaryFile` + `os.replace()` (M-3)
- [ ] No domain layer file imports from infrastructure (H-07)
- [ ] One class per file throughout `src/docs/` (H-10)
- [ ] Type hints + docstrings on all public functions (H-11)

---

## Related Items

### Hierarchy

- **Parent Story:** [ST-002](../ST-002-auto-doc-module.md)
- **Orchestration Phase:** impl-20260310-001 / phase-1 / eng-backend-1

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-10 | Claude | in_progress | Task created; Phase 1 agent launched |
| 2026-03-10 | Claude | completed | Barrier 1 PASSED (0.9410 >= 0.94, 10 iterations) |
