# {{TITLE}}

<!--
TEMPLATE: Bug (DRAFT)
SOURCE: ONTOLOGY-v1.md Section 3.4.10
VERSION: 0.1.0
STATUS: DRAFT - Pending review

DESCRIPTION:
  Defect or problem requiring fix. First-class entity present
  in all three systems. Can exist at any hierarchy level.

EXTENDS: QualityItem -> WorkItem

NOTE: "Bug" preferred over "Defect" because it is used by 2/3 systems
      and is more common in developer vernacular.
      Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.2 (Canonical Name Rationale)
-->

---

## Frontmatter

```yaml
# === IDENTITY (Auto-generated, Immutable) ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
id: "{{ID}}"                           # Format: PREFIX-NNN (e.g., BUG-001)
work_type: BUG                         # Immutable discriminator

# === CORE METADATA ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
title: "{{TITLE}}"                     # Required, 1-500 chars
description: |
  {{DESCRIPTION}}

# === CLASSIFICATION ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
classification: BUSINESS               # BUSINESS | ENABLER (default: BUSINESS)

# === LIFECYCLE STATE ===
# Source: ONTOLOGY-v1.md Section 3.4.10 (Bug.state_machine)
status: BACKLOG                        # See State Machine below
resolution: null                       # DONE | FIXED | WONT_DO | DUPLICATE | CANNOT_REPRODUCE | OBSOLETE

# === PRIORITY ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
priority: MEDIUM                       # CRITICAL | HIGH | MEDIUM | LOW

# === PEOPLE ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
assignee: "{{ASSIGNEE}}"               # User responsible
created_by: "{{CREATED_BY}}"           # Auto-set on creation (reporter)

# === TIMESTAMPS (Auto-managed) ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
created_at: "{{CREATED_AT}}"           # ISO 8601 datetime
updated_at: "{{UPDATED_AT}}"           # ISO 8601 datetime

# === HIERARCHY ===
# Source: ONTOLOGY-v1.md Section 3.4.10 (Bug.containment)
parent_id: "{{PARENT_ID}}"             # Feature, Story, or Epic ID

# === TAGS ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
tags:
  - "{{TAG_1}}"
  - "{{TAG_2}}"

# === QUALITY ITEM PROPERTIES ===
# Source: ONTOLOGY-v1.md Section 3.3.3 (QualityItem)
severity: MAJOR                        # CRITICAL | MAJOR | MINOR | TRIVIAL (default: MAJOR)
found_in_version: "{{FOUND_IN_VERSION}}"  # Version where defect was discovered
fix_version: "{{FIX_VERSION}}"         # Target version for the fix

# === BUG-SPECIFIC PROPERTIES ===
# Source: ONTOLOGY-v1.md Section 3.4.10 (Bug.specific)
reproduction_steps: |
  {{REPRODUCTION_STEPS}}               # Steps to reproduce (max: 20000 chars)
environment: |
  {{ENVIRONMENT}}                      # Environment where bug occurs (max: 5000 chars)
root_cause: |
  {{ROOT_CAUSE}}                       # Root cause analysis (max: 10000 chars)
effort: null                           # Effort estimate for fix (0-100)
acceptance_criteria: |
  {{ACCEPTANCE_CRITERIA}}              # Conditions for bug to be considered fixed
```

---

## State Machine

<!-- Source: ONTOLOGY-v1.md Section 3.4.10 (Bug.state_machine) -->

**Initial State:** `BACKLOG`

**Valid States:** `BACKLOG`, `READY`, `IN_PROGRESS`, `BLOCKED`, `IN_REVIEW`, `DONE`, `REMOVED`

```
              +-----------+
              |  BACKLOG  |
              +-----+-----+
                    |
          +---------+---------+
          |                   |
          v                   v
      +-------+          +---------+
      | READY |          | REMOVED |
      +---+---+          +---------+
          |
    +-----+-----+
    |           |
    v           v
+------------+ +---------+
| IN_PROGRESS| | BACKLOG |
+-----+------+ +---------+
      |
  +---+---+---+
  |   |   |   |
  v   v   v   v
+---+ +---+ +---+ +---+
|BLK| |REV| |DON| |REM|
+---+ +---+ +---+ +---+
  |     |     |
  v     v     v
+------------+
| IN_PROGRESS| (Reopen/Continue)
+------------+

Legend: BLK=BLOCKED, REV=IN_REVIEW, DON=DONE, REM=REMOVED
```

| From State    | Allowed Transitions                              |
|---------------|--------------------------------------------------|
| BACKLOG       | READY, REMOVED                                   |
| READY         | IN_PROGRESS, BACKLOG, REMOVED                    |
| IN_PROGRESS   | BLOCKED, IN_REVIEW, DONE, REMOVED                |
| BLOCKED       | IN_PROGRESS, REMOVED                             |
| IN_REVIEW     | DONE, IN_PROGRESS                                |
| DONE          | IN_PROGRESS (Reopen - regression found)          |
| REMOVED       | (Terminal - no transitions)                      |

---

## Containment Rules

<!-- Source: ONTOLOGY-v1.md Section 3.4.10 (Bug.containment) -->

| Rule             | Value                           |
|------------------|---------------------------------|
| Allowed Children | Task                            |
| Allowed Parents  | Feature, Story, Epic            |
| Max Depth        | 1                               |

---

## Invariants

<!-- Source: ONTOLOGY-v1.md Section 3.4.10 (Bug.invariants) -->

- **INV-Q01:** CRITICAL severity bugs must have assignee (inherited from QualityItem)
- **INV-Q02:** fix_version should be set before DONE (inherited from QualityItem)
- **INV-BG01:** Bug can have Feature, Story, or Epic as parent
- **INV-BG02:** reproduction_steps should be provided for non-TRIVIAL severity
- **INV-BG03:** root_cause should be documented when DONE

---

## System Mapping

<!-- Source: ONTOLOGY-v1.md Section 3.4.10 (Bug.system_mapping) -->

| System | Mapping                          |
|--------|----------------------------------|
| ADO    | Bug                              |
| SAFe   | Defect (uses 'Defect' terminology) |
| JIRA   | Bug                              |

---

## Content

### Summary

{{BUG_SUMMARY}}

### Reproduction Steps

1. {{STEP_1}}
2. {{STEP_2}}
3. {{STEP_3}}

**Expected Result:** {{EXPECTED_RESULT}}

**Actual Result:** {{ACTUAL_RESULT}}

### Environment

- **OS:** {{OS}}
- **Browser/Runtime:** {{BROWSER_RUNTIME}}
- **Version:** {{APP_VERSION}}
- **Configuration:** {{CONFIGURATION}}

### Screenshots/Evidence

{{SCREENSHOTS_EVIDENCE}}

### Root Cause Analysis

<!-- Document when status transitions to DONE (INV-BG03) -->

{{ROOT_CAUSE_ANALYSIS}}

### Fix Description

{{FIX_DESCRIPTION}}

### Acceptance Criteria

<!-- Conditions for bug to be considered fixed -->

- [ ] {{FIX_CRITERION_1}}
- [ ] {{FIX_CRITERION_2}}
- [ ] Regression tests added
- [ ] No new issues introduced

### Related Items

- Parent: [{{PARENT_TITLE}}]({{PARENT_LINK}})
- Related Bug: [{{RELATED_BUG}}]({{RELATED_BUG_LINK}})
- Causing Change: [{{CAUSING_CHANGE}}]({{CAUSING_CHANGE_LINK}})

---

## Severity Guide

| Severity | Description                                                   |
|----------|---------------------------------------------------------------|
| CRITICAL | System crash, data loss, security vulnerability, no workaround |
| MAJOR    | Major functionality broken, significant impact, workaround exists |
| MINOR    | Minor functionality issue, low impact, easy workaround        |
| TRIVIAL  | Cosmetic issue, typo, no functional impact                    |

---

## History

| Date       | Status       | Notes                          |
|------------|--------------|--------------------------------|
| {{DATE}}   | Created      | Initial report                 |
| {{DATE}}   | READY        | Triage complete                |
| {{DATE}}   | IN_PROGRESS  | Fix in progress                |
| {{DATE}}   | IN_REVIEW    | Fix ready for verification     |
| {{DATE}}   | DONE         | Verified and closed            |

---

<!--
JERRY ALIGNMENT:
  existing_type: "WorkType.BUG"
  changes_needed: "None - already exists"

DESIGN RATIONALE:
  "Bug" preferred over "Defect" because it is used by 2/3 systems
  and is more common in developer vernacular.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.2 (Canonical Name Rationale)
-->
