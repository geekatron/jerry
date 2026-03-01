# TASK-021: Phase 1: Baseline capture — identify all NPT-014 instances + quality metrics

> **Type:** task
> **Status:** completed
> **Priority:** high
> **Created:** 2026-02-28
> **Completed:** 2026-02-28
> **Parent:** FEAT-001
> **Owner:** Claude
> **Activity:** RESEARCH

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description |
| [Content](#content) | Description and acceptance criteria |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes |

---

## Summary

Scan the Jerry codebase to identify and catalog all 47 NPT-014 (Bare Prohibition) instances across rule files, agent definitions, and SKILL.md files. Produce an inventory with file paths, line numbers, and recommended upgrade patterns.

---

## Content

### Description

Scan the entire Jerry codebase to identify all NPT-014 (Bare Prohibition) instances — standalone NEVER/MUST NOT/DO NOT statements without consequence or alternative text. Catalog each instance with file path, line number, current text, and recommended upgrade pattern (NPT-009 or NPT-013).

### Acceptance Criteria

- [x] All rule files (.context/rules/) scanned for NPT-014 instances
- [x] All agent definitions (skills/*/agents/) scanned for NPT-014 instances
- [x] All SKILL.md files scanned for NPT-014 instances
- [x] Inventory document produced with file, line, current text, and target pattern
- [x] Baseline metrics captured: 47 NPT-014, 28 NPT-009, 36 NPT-013

### Related Items

- Parent: [FEAT-001: Implement ADR-001](./FEAT-001-implement-adr-001-npt-014-elimination.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Phase 1 inventory | Research artifact | `orchestration/adr001-implementation/phase-1-npt014-inventory.md` |

### Verification

- [x] Acceptance criteria verified
- [x] 47 NPT-014 instances catalogued across rule files, agent definitions, and SKILL.md files
- [x] 28 NPT-009 and 36 NPT-013 baseline instances documented

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-28 | Created | Initial creation |
| 2026-02-28 | completed | 47 NPT-014, 28 NPT-009, 36 NPT-013 identified |
