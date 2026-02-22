# EN-013: Bootstrap Wiring + Config Integration

> **Type:** enabler
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-21
> **Due:** --
> **Completed:** 2026-02-21
> **Parent:** FEAT-002
> **Owner:** --
> **Effort:** 1-2h

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Technical scope |
| [Acceptance Criteria](#acceptance-criteria) | Checklist |
| [Dependencies](#dependencies) | Relationships |
| [Technical Approach](#technical-approach) | Implementation strategy |
| [History](#history) | Status changes |

---

## Summary

Wires the `jerry context estimate` pipeline in the composition root (`bootstrap.py`) and registers the CLI subcommand in the parser:

- `create_context_estimate_handler()` factory in `bootstrap.py` — instantiates `FilesystemContextStateStore`, `TranscriptSubAgentReader`, `ContextEstimateComputer`, `ContextEstimateService`, `ContextEstimateHandler` in dependency order
- CLI parser registers `context estimate` as a subcommand under the `context` subparser group
- `adapter.py` routes `context estimate` to the handler
- `main.py` wires the new subcommand group

---

## Acceptance Criteria

- [x] `create_context_estimate_handler()` factory in `bootstrap.py` with full DI chain
- [x] `jerry context estimate` callable after wiring
- [x] `context` subparser group registered in `parser.py`
- [x] `adapter.py` routes `context estimate` to `ContextEstimateHandler.handle()`
- [x] No ad-hoc instantiation in handler (all deps injected)
- [x] `jerry context --help` lists `estimate` subcommand
- [x] `jerry --json context estimate` returns valid JSON

---

## Dependencies

**Depends On:**
- EN-009 (ContextEstimateComputer)
- EN-010 (ContextEstimateService)
- EN-011 (FilesystemContextStateStore)
- EN-012 (ContextEstimateHandler)
- EN-018 (TranscriptSubAgentReader)

**Files:**
- `src/bootstrap.py`
- `src/interface/cli/parser.py`
- `src/interface/cli/main.py`
- `src/interface/cli/adapter.py`

---

## Technical Approach

The composition root factory create_context_estimate_handler() in bootstrap.py wires domain service, application service, infrastructure adapter, and sub-agent reader in dependency order, with all dependencies injected rather than instantiated ad-hoc. The CLI parser registers context estimate as a subcommand, adapter.py routes the command to the handler, and config integration reads context_monitor.* settings from .jerry/config.toml for threshold overrides and rotation aggressiveness.

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-21 | Claude | completed | Bootstrap wiring complete. `jerry context estimate` callable end-to-end. |
