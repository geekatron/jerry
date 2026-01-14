# SOLUTION-WORKTRACKER: SE-001 Performance and Plugin Bug Fixes

> **Solution Epic ID:** SE-001
> **Project:** PROJ-007-jerry-bugs
> **Status:** IN PROGRESS
> **Created:** 2026-01-14
> **Last Updated:** 2026-01-14

---

## Overview

This Solution Epic addresses two critical bugs affecting Jerry Framework usability:

1. **Lock file accumulation** causing performance degradation
2. **Plugin not loading** preventing Jerry from initializing

---

## Features

| ID | Name | Status | Progress | Tracker |
|----|------|--------|----------|---------|
| [FT-001](./FT-001-lock-file-cleanup/FEATURE-WORKTRACKER.md) | Lock File Cleanup | IN PROGRESS | 0/1 Enablers | [FEATURE-WORKTRACKER.md](./FT-001-lock-file-cleanup/FEATURE-WORKTRACKER.md) |
| [FT-002](./FT-002-plugin-loading-fix/FEATURE-WORKTRACKER.md) | Plugin Loading Fix | PENDING | 0/1 Enablers | [FEATURE-WORKTRACKER.md](./FT-002-plugin-loading-fix/FEATURE-WORKTRACKER.md) |

---

## Work Items Summary

| Feature | Enablers | Units of Work | Tasks | Status |
|---------|----------|---------------|-------|--------|
| FT-001 | EN-001 | 0 | TBD | IN PROGRESS |
| FT-002 | EN-002 | 0 | TBD | PENDING |

---

## Bugs Addressed

| ID | Description | Feature | Status |
|----|-------------|---------|--------|
| BUG-001 | Lock files accumulating in .jerry/local/locks/ | FT-001 | INVESTIGATING |
| BUG-002 | Jerry plugin not loading when started via --plugin-dir | FT-002 | PENDING |

---

## Technical Debt

| ID | Description | Feature | Status |
|----|-------------|---------|--------|
| TD-001 | Lock file cleanup never implemented per ADR-006 | FT-001 | DOCUMENTED |

---

## Key Decisions

| ADR | Decision | Status |
|-----|----------|--------|
| *(pending investigation)* | Lock file cleanup strategy | PENDING |
| *(pending investigation)* | Plugin loading fix approach | PENDING |

---

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| Global Manifest | [../../WORKTRACKER.md](../../WORKTRACKER.md) | Project work tracker |
| Investigation | [../../investigations/](../../investigations/) | ps-investigator reports |
| Plans | [./plans/](./plans/) | Implementation plans |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-14 | SE-001 created | Claude |
| 2026-01-14 | FT-001, FT-002 features created | Claude |
