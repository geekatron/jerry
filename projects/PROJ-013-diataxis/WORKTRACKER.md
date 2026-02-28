# WORKTRACKER — PROJ-013 Diataxis Documentation Framework

> **Project:** PROJ-013-diataxis
> **GitHub Issue:** [#99](https://github.com/geekatron/jerry/issues/99)
> **Created:** 2026-02-27
> **Status:** Done

## Document Sections

| Section | Purpose |
|---------|---------|
| [Epic](#epic) | Top-level work item |
| [Features](#features) | Feature breakdown |
| [Enablers](#enablers) | Foundation and infrastructure work |
| [Tasks](#tasks) | Atomic work items |
| [Spikes](#spikes) | Research and exploration |

---

## Epic

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| EPIC-013-001 | Diataxis Documentation Framework Skill | Done | high |

---

## Features

| ID | Title | Parent | Status | Priority |
|----|-------|--------|--------|----------|
| FEAT-013-001 | Core Writer Agents (4 quadrants) | EPIC-013-001 | Done | high |
| FEAT-013-002 | Classifier and Auditor Agents | EPIC-013-001 | Done | high |
| FEAT-013-003 | Skill Registration and Routing | EPIC-013-001 | Done | high |
| FEAT-013-004 | Quality Validation and Dogfooding | EPIC-013-001 | Done | medium |

---

## Enablers

| ID | Title | Parent | Status | Priority |
|----|-------|--------|--------|----------|
| EN-013-001 | Diataxis Framework Research | EPIC-013-001 | Done | critical |
| EN-013-002 | Diataxis Standards Rule File | FEAT-013-001 | Done | critical |
| EN-013-003 | Per-Quadrant Templates | FEAT-013-001 | Done | high |

---

## Tasks

| ID | Title | Parent | Status | Priority |
|----|-------|--------|--------|----------|
| TASK-013-001 | Create knowledge doc `docs/knowledge/diataxis-framework.md` | EN-013-001 | Done | critical |
| TASK-013-002 | Create SKILL.md with WHAT+WHEN+triggers | FEAT-013-003 | Done | high |
| TASK-013-003 | Implement diataxis-tutorial agent (.md + .governance.yaml) | FEAT-013-001 | Done | high |
| TASK-013-004 | Implement diataxis-howto agent (.md + .governance.yaml) | FEAT-013-001 | Done | high |
| TASK-013-005 | Implement diataxis-reference agent (.md + .governance.yaml) | FEAT-013-001 | Done | high |
| TASK-013-006 | Implement diataxis-explanation agent (.md + .governance.yaml) | FEAT-013-001 | Done | high |
| TASK-013-007 | Implement diataxis-classifier agent (.md + .governance.yaml) | FEAT-013-002 | Done | high |
| TASK-013-008 | Implement diataxis-auditor agent (.md + .governance.yaml) | FEAT-013-002 | Done | high |
| TASK-013-009 | Create tutorial-template.md | EN-013-003 | Done | high |
| TASK-013-010 | Create howto-template.md | EN-013-003 | Done | high |
| TASK-013-011 | Create reference-template.md | EN-013-003 | Done | high |
| TASK-013-012 | Create explanation-template.md | EN-013-003 | Done | high |
| TASK-013-013 | Create diataxis-standards.md (5 sections) | EN-013-002 | Done | critical |
| TASK-013-014 | Register /diataxis in CLAUDE.md skill table | FEAT-013-003 | Done | high |
| TASK-013-015 | Register agents in AGENTS.md | FEAT-013-003 | Done | high |
| TASK-013-016 | Add trigger map entry to mandatory-skill-usage.md | FEAT-013-003 | Done | high |
| TASK-013-017 | Phase 2 gate: validate all .governance.yaml against schema | FEAT-013-001 | Done | high |
| TASK-013-018 | Adversarial quality review (>= 0.95, up to 5 iterations) | FEAT-013-004 | Done | high |
| TASK-013-019 | Produce sample docs across all 4 quadrants | FEAT-013-004 | Done | medium |
| TASK-013-020 | Improve 2+ existing Jerry docs using /diataxis agents | FEAT-013-004 | Done | medium |

---

## Spikes

| ID | Title | Parent | Status | Time-Box |
|----|-------|--------|--------|----------|
| SPIKE-013-001 | Diataxis Framework Deep Research | EN-013-001 | Done | 2h |
