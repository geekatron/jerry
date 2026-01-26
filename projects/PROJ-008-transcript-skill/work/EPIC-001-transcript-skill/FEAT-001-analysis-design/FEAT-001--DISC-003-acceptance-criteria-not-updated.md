# DISC-003: Acceptance Criteria Checkboxes Not Updated

<!--
TEMPLATE: Discovery
SOURCE: ONTOLOGY-v1.md Section 3.4.8
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "DISC-003"
work_type: DISCOVERY
title: "Acceptance Criteria Checkboxes Not Updated in Work Tracker Items"

# === LIFECYCLE ===
status: OPEN
severity: MEDIUM
impact: PROCESS

# === TIMESTAMPS ===
discovered_at: "2026-01-26T12:00:00Z"
discovered_by: "User"

# === HIERARCHY ===
parent_id: "FEAT-001"

# === TAGS ===
tags:
  - "process"
  - "worktracker"
  - "acceptance-criteria"
```

---

## Discovery Summary

When marking work tracker items as DONE, Claude did not update the acceptance criteria checkboxes (`- [ ]` to `- [x]`) in the work tracker files. This reduces traceability and evidence of completion.

---

## L0: What Happened (ELI5)

Imagine a checklist where you're supposed to check off each item as you complete it. Instead, Claude just wrote "DONE" at the top without checking any boxes. Now we can't see which specific items were actually verified.

---

## L1: Technical Analysis

### Example of Issue

**TASK-011-review-tdd.md** shows:

```markdown
### Acceptance Criteria

- [ ] **AC-001:** All 4 TDD documents reviewed
- [ ] **AC-002:** Quality score >= 0.85 for each document
- [ ] **AC-003:** Aggregate TDD quality >= 0.90
...
```

Despite task being marked `status: DONE`, all checkboxes remain unchecked.

### Pattern Observed

| Task File | Status | Checkboxes Updated |
|-----------|--------|-------------------|
| TASK-001-tdd-overview.md | DONE | No |
| TASK-002-tdd-ts-parser.md | DONE | No |
| TASK-003-tdd-ts-extractor.md | DONE | No |
| ... | ... | ... |
| TASK-013-final-review.md | DONE | No |

**None of the 13 task files have updated acceptance criteria checkboxes.**

### Root Cause Analysis

1. Why? → Claude marked status: DONE without updating checkboxes
2. Why? → The workflow focused on creating deliverables, not updating checklists
3. Why? → No explicit step in Claude's process to "verify and check ACs"
4. Why? → Task completion was defined by "deliverable exists" not "all ACs verified"

---

## L2: Process Implications

### Missing Traceability

Without checked acceptance criteria:
- Cannot verify WHICH criteria were actually met
- Cannot audit completion evidence
- Cannot identify partial completions

### Correct Behavior

When completing a task, Claude SHOULD:

1. Review each acceptance criterion
2. Verify it is met with evidence
3. Update checkbox: `- [ ]` → `- [x]`
4. Only THEN mark status: DONE

```markdown
### Acceptance Criteria

- [x] **AC-001:** All 4 TDD documents reviewed
      Evidence: review/tdd-review.md documents all 4
- [x] **AC-002:** Quality score >= 0.85 for each document
      Evidence: Scores 0.92, 0.89, 0.91, 0.90 (all >= 0.85)
- [x] **AC-003:** Aggregate TDD quality >= 0.90
      Evidence: Aggregate 0.905 >= 0.90
```

---

## Impact Assessment

| Dimension | Impact | Notes |
|-----------|--------|-------|
| Schedule | NONE | Work is done |
| Quality | LOW | Deliverables exist |
| Process | MEDIUM | Audit trail incomplete |
| Trust | LOW | Minor but sloppy |

---

## Remediation

### Immediate Action

Update all 13 TASK-*.md files in EN-005 to check completed acceptance criteria.

### Process Improvement

Add to Claude's task completion checklist:
1. Create deliverable
2. Verify each acceptance criterion
3. Check checkbox with evidence
4. Update status to DONE

---

## Related Items

- **Parent:** FEAT-001 Analysis & Design
- **Affected Files:** All TASK-*.md files in EN-005

---

*Discovery ID: DISC-003*
*Severity: MEDIUM*
*Status: OPEN*
