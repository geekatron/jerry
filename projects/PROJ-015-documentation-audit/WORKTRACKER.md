# WORKTRACKER — PROJ-015 Documentation Audit

> **Status:** SUPERSEDED by [PROJ-040](../PROJ-040-documentation/) (2026-04-20)
>
> The 2026-03-02 audit went stale as Jerry grew from 15 skills to 30 skills. A refreshed Diataxis audit was re-run on 2026-04-20 under PROJ-040 (passed C4 adversarial review at 0.956 composite, 4 iterations). The `reports/` directory here is preserved as historical baseline; all active documentation work now routes through PROJ-040.
>
> **Authoritative successor:** `../PROJ-040-documentation/reports/diataxis-audit-20260420.md`

---

> **Project:** PROJ-015-documentation-audit
> **GitHub Issue:** [#130](https://github.com/geekatron/jerry/issues/130)
> **Created:** 2026-03-02
> **Status:** Complete (superseded 2026-04-20)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Epic](#epic) | Top-level work item |
| [Features](#features) | Feature breakdown |
| [Tasks](#tasks) | Atomic work items |

---

## Epic

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| EPIC-015-001 | User-Facing Documentation Audit & Gap Analysis | Done | high |

---

## Features

| ID | Title | Parent | Status | Priority |
|----|-------|--------|--------|----------|
| FEAT-015-001 | Diataxis Audit of Existing User-Facing Docs | EPIC-015-001 | Done | high |
| FEAT-015-002 | Skill & Agent Documentation Gap Identification | EPIC-015-001 | Done | high |
| FEAT-015-003 | Remediation Plan & Priority Ranking | EPIC-015-001 | Done | medium |

---

## Tasks

| ID | Title | Parent | Status | Priority |
|----|-------|--------|--------|----------|
| TASK-015-001 | Run diataxis-auditor on 6 user-facing docs (BOOTSTRAP, INSTALLATION, CLAUDE-MD-GUIDE, getting-started, prompt-templates, prompt-quality) | FEAT-015-001 | Done | high |
| TASK-015-002 | Run diataxis-classifier on user-facing docs to assign correct quadrant | FEAT-015-001 | Done | high |
| TASK-015-003 | Inventory all 15 skills for user-facing documentation coverage | FEAT-015-002 | Done | high |
| TASK-015-004 | Identify missing documentation categories (tutorials, how-to guides, reference, explanations) | FEAT-015-002 | Done | high |
| TASK-015-005 | Produce prioritized remediation report with gap severity rankings | FEAT-015-003 | Done | medium |
