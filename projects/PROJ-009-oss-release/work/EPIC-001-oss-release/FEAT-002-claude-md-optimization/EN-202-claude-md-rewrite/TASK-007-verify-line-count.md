# TASK-007: Verify Line Count Target (60-80 lines)

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Frontmatter](#frontmatter) | Task metadata |
| [Content](#content) | Description, verification steps, metrics |
| [Time Tracking](#time-tracking) | Effort metrics |
| [Evidence](#evidence) | Deliverables, metrics, verification |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-007"
work_type: TASK
title: "Verify Line Count Target (60-80 lines)"
description: |
  Verify that the final CLAUDE.md meets the target line count of 60-80 lines
  and estimate token count reduction.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: null
created_by: "Claude"
created_at: "2026-02-01T00:00:00Z"
updated_at: "2026-02-01T00:00:00Z"
parent_id: "EN-202"
tags:
  - enabler
  - claude-md
  - verification

effort: 1
acceptance_criteria: |
  - Line count between 60-80 lines
  - Token count estimated at ~3,300-3,500
  - Original backed up
  - Reduction metrics documented
due_date: null

activity: TESTING
original_estimate: 1
remaining_work: 1
time_spent: null
```

---

## Content

### Description

Final verification that the new CLAUDE.md meets all quantitative targets and document the improvement metrics.

### Dependencies

This task depends on completion of:
- TASK-006: Validate all pointers resolve correctly

### Verification Steps

1. **Create backup of original**
   ```bash
   cp CLAUDE.md CLAUDE.md.backup
   ```

2. **Verify line count**
   ```bash
   wc -l CLAUDE.md
   # Target: 60-80 lines
   ```

3. **Estimate token count**
   - Use Claude Code `/context` command
   - Target: ~3,300-3,500 tokens

4. **Document metrics**

### Target Metrics

| Metric | Current | Target | Achieved |
|--------|---------|--------|----------|
| Lines | 914 | 60-80 | [ ] |
| Tokens | ~10,000 | ~3,300-3,500 | [ ] |
| Reduction % | - | 91-93% | [ ] |

### Acceptance Criteria

- [ ] CLAUDE.md line count is 60-80
- [ ] Token count approximately 3,300-3,500
- [ ] Backup created (CLAUDE.md.backup)
- [ ] Metrics documented
- [ ] Reduction percentage calculated

### Contingency

If line count exceeds 80 lines:
1. Review each section for verbosity
2. Remove any redundant information
3. Consider moving additional content to skills

If line count below 60 lines:
1. Verify all critical information included
2. Consider if any essential context is missing

### Related Items

- Parent: [EN-202: CLAUDE.md Rewrite](./EN-202-claude-md-rewrite.md)
- Dependencies: TASK-001 through TASK-006

---

## Time Tracking

| Metric | Value |
|---------|-------|
| Original Estimate | 1 hour |
| Remaining Work | 1 hour |
| Time Spent | 0 hours |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| CLAUDE.md | Documentation | CLAUDE.md |
| CLAUDE.md.backup | Backup | CLAUDE.md.backup |
| Metrics | Documentation | (inline in this file) |

### Final Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Lines | 914 | - | - |
| Tokens | ~10,000 | - | - |
| Reduction | - | - | - |

### Verification

- [ ] All metrics documented
- [ ] Backup created
- [ ] Reviewed by: -

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Created | Initial creation |
