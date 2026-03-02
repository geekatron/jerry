# WORKTRACKER — PROJ-015 Documentation Audit

> **Project:** PROJ-015-documentation-audit
> **GitHub Issue:** [#130](https://github.com/geekatron/jerry/issues/130)
> **Created:** 2026-03-02
> **Status:** Complete

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
