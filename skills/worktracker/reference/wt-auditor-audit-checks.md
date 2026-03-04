# WT Auditor: Audit Check Types

> Reference for audit check type definitions, example violations, and remediation guidance. Loaded by wt-auditor at Tier 3 when executing audits.

## 1. Template Compliance (severity: error)

**What it checks:**
- Required sections present (Summary, Acceptance Criteria, Status, etc.)
- Frontmatter metadata complete (id, type, status, parent_id, etc.)
- Status values valid (`pending`, `in_progress`, `completed`, `blocked`, `cancelled`)
- Template reference in HTML comment header (e.g., `<!-- Template: .context/templates/worktracker/ENABLER.md -->`)

**Example violations:**
- Missing "Acceptance Criteria" section in EN-001-example.md
- Invalid status "done" instead of "completed"
- Missing frontmatter `parent_id` field

**Remediation:**
```markdown
Compare file against template at `.context/templates/worktracker/{TYPE}.md`.
Add missing sections or fix invalid values.
```

## 2. Relationship Integrity (severity: error)

**What it checks:**
- Parent ID in child matches actual parent
- Parent references child in Children section
- No circular dependencies (A->B->A)
- Relationship references resolve to existing files

**Example violations:**
- EN-001 references parent FEAT-001, but FEAT-001 doesn't exist
- TASK-002 has `parent_id: EN-001`, but EN-001 doesn't list TASK-002 in Children section
- Circular: EN-001 -> TASK-001 -> EN-001

**Remediation:**
```markdown
Update parent file to include child in Children section.
OR remove parent_id from child if parent no longer valid.
```

## 3. Orphan Detection (severity: warning)

**What it checks:**
- All items reachable from WORKTRACKER.md
- No files in `work/` without parent linkage
- Discoveries, Bugs, Impediments linked from parent entities

**Example violations:**
- EN-005-orphan.md exists but no parent references it
- BUG-001.md not linked from any parent's Bugs section
- DISC-002.md exists but not in parent's Discoveries section

**Remediation:**
```markdown
Link orphaned item from appropriate parent entity.
OR move to archive if no longer relevant.
```

## 4. Status Consistency (severity: warning)

**What it checks:**
- Parent not DONE if children not all DONE
- Blocked items have blocker documented in Impediments section
- In-progress items have at least one child started

**Example violations:**
- EN-001 status is `completed`, but TASK-002 (child) is `in_progress`
- FEAT-001 status is `blocked`, but no IMP-* reference in Impediments section
- EN-003 status is `in_progress`, but all children are `pending`

**Remediation:**
```markdown
Update parent status to reflect actual child state.
OR complete/cancel remaining children before marking parent done.
```

## 5. ID Format (severity: info)

**What it checks:**
- Format: `{TYPE}-{NNN}-{slug}`
- IDs are unique within scope
- Type prefix matches file template (EN-*, TASK-*, BUG-*, etc.)
- Slug matches filename

**Example violations:**
- Invalid ID: "EN-1-slug" (should be EN-001-slug with leading zeros)
- Duplicate ID: Two files both using TASK-003
- Type mismatch: File is ENABLER but ID is TASK-001
- Slug mismatch: File is `EN-001-example.md` but ID is `EN-001-different-slug`

**Remediation:**
```markdown
Rename file to match canonical ID format: {TYPE}-{NNN}-{slug}.md
Update all parent references to new ID.
```
