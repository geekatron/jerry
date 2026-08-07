# TASK-033: Evaluate docs.yml deploy-pages Migration

> **Type:** task
> **Status:** completed
> **Priority:** low
> **Created:** 2026-04-15
> **Completed:** 2026-04-16
> **Parent:** EN-006
> **GitHub Issue:** [#252](https://github.com/geekatron/jerry/issues/252)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |
| [Evidence](#evidence) | Verification record |

---

## Summary

`docs.yml` uses `contents: write` to push to gh-pages via `mkdocs gh-deploy --force`. This is broader than needed — `contents: write` also grants ability to push to main or create tags. Evaluate migrating to `actions/deploy-pages` which uses the more targeted `pages: write` + `id-token: write` permissions.

**Finding:** eng-devsecops Finding 10 (LOW), `docs.yml:21-22`

---

## Acceptance Criteria

- [x] Migration feasibility evaluated: deploy-pages requires repo settings change, 2 new actions, MkDocs Material compatibility unverified
- [x] Decision: **KEEP** current approach — risk mitigated by main-only trigger, path filters, no custom secrets
- [x] Rationale documented: `contents: write` blast radius bounded by ephemeral token; `id-token: write` from deploy-pages has its own attack surface; net permission reduction narrower than it appears

## Evidence

| Verification | Agent | Result |
|-------------|-------|--------|
| Decision | eng-infra | KEEP — migration cost exceeds security benefit at current scale |
| Revisit triggers | eng-infra | Revisit if: (a) other jobs need workflow-level contents:write removed, or (b) workflow gains source-branch steps |
