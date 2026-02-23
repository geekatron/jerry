# {{BUG_ID}}: {{BUG_TITLE}}

<!--
TEMPLATE: Bug
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.10
CREATED: 2026-01-23 (ps-architect-002)
PURPOSE: Document defects or problems requiring fix

DESCRIPTION:
  Defect or problem requiring fix. First-class entity present
  in all three systems. Can exist at any hierarchy level.

EXTENDS: QualityItem -> WorkItem

NOTE: "Bug" preferred over "Defect" because it is used by 2/3 systems
      and is more common in developer vernacular.
      Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.2 (Canonical Name Rationale)
-->

> **Type:** bug
> **Status:** {{STATUS}}
> **Priority:** {{PRIORITY}}
> **Impact:** {{IMPACT}}
> **Severity:** {{SEVERITY}}
> **Created:** {{CREATED_AT}}
> **Due:** {{DUE_DATE}}
> **Completed:** {{COMPLETED_AT}}
> **Parent:** {{PARENT_ID}}
> **Owner:** {{ASSIGNEE}}
> **Found In:** {{FOUND_IN_VERSION}}
> **Fix Version:** {{FIX_VERSION}}

<!--
STATUS VALUES: pending | in_progress | completed
PRIORITY VALUES: critical | high | medium | low
IMPACT VALUES: critical | high | medium | low
SEVERITY VALUES: critical | major | minor | trivial
TIMESTAMPS: Use ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
-->

---

## Quick Creation Guide

<!-- READ THIS FIRST when creating a new Bug. Rules: WTI-007, WTI-008. -->

### Steps

1. **Summary:** 1-2 sentences describing the **symptom** from the user's perspective. Do not describe root cause here.
2. **Repro Steps:** 4-6 numbered steps to reproduce the issue. Include expected vs actual behavior.
3. **AC:** Max **3 bullets**. Start each with actor/system. Focus on what "fixed" looks like.
4. **Sections to skip at creation:** Root Cause Analysis, Fix Description, Evidence (populate these during/after fix).

### BAD vs GOOD AC (Bugs)

```markdown
# BAD (violates WTI-007a, WTI-007b):
- [ ] Fix the null reference in AssetHandler.cs line 42
- [ ] All unit tests pass
- [ ] Code reviewed

# GOOD (compliant):
- [ ] Asset list page loads without error when asset type filter is empty
- [ ] System returns 200 OK with empty array (not 500) when no assets match
- [ ] Error is logged at WARN level with correlation ID for debugging
```

### Quality Check

Before creating: Can an engineer verify the fix without asking questions? If not, add more detail.

**Reference:** `skills/worktracker/rules/worktracker-content-standards.md`

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Quick Creation Guide](#quick-creation-guide) | How to create a bug quickly with quality AC |
| [Template Structure](#template-structure) | Visual structure reference for bug template |
| [Frontmatter](#frontmatter) | YAML metadata schema for bug work items |
| [Summary](#summary) | Brief description and key details |
| [Reproduction Steps](#reproduction-steps) | Steps to reproduce the issue |
| [Environment](#environment) | Environment where bug occurs |
| [Evidence](#evidence) | Bug documentation and fix verification |
| [Root Cause Analysis](#root-cause-analysis) | Investigation and root cause details |
| [Fix Description](#fix-description) | Solution approach and changes made |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for bug to be fixed |
| [Related Items](#related-items) | Hierarchy and related work items |
| [State Machine Reference](#state-machine-reference) | Bug status transitions |
| [Containment Rules](#containment-rules) | Parent/child constraints |
| [Invariants](#invariants) | Business rules and constraints |
| [Severity Guide](#severity-guide) | Severity levels and response times |
| [History](#history) | Status changes and key events |
| [System Mapping](#system-mapping) | ADO, SAFe, JIRA mappings |

---

## Template Structure

```
+---------------------------------------------------------------------+
|                          BUG TEMPLATE                                |
|                    Version 1.0.0 (ONTOLOGY-aligned)                  |
+---------------------------------------------------------------------+
| Header Block (blockquote)                                            |
|   |-- type: "bug"                              [REQUIRED]            |
|   |-- status: pending|in_progress|completed    [REQUIRED]            |
|   |-- priority: critical|high|medium|low       [REQUIRED]            |
|   |-- impact: critical|high|medium|low         [REQUIRED]            |
|   |-- severity: critical|major|minor|trivial   [REQUIRED]            |
|   |-- created: ISO-8601                        [REQUIRED]            |
|   |-- due: ISO-8601                            [OPTIONAL]            |
|   |-- completed: ISO-8601                      [OPTIONAL]            |
|   |-- parent: {ID}                             [REQUIRED]            |
|   |-- owner: {USER}                            [OPTIONAL]            |
|   |-- found_in: version                        [RECOMMENDED]         |
|   +-- fix_version: version                     [OPTIONAL]            |
+---------------------------------------------------------------------+
| Summary Section                                 [REQUIRED]           |
| Reproduction Steps                              [REQUIRED]           |
| Environment                                     [REQUIRED]           |
| Root Cause Analysis                             [RECOMMENDED]        |
| Fix Description                                 [REQUIRED when done] |
| Acceptance Criteria                             [REQUIRED]           |
| Related Items                                   [RECOMMENDED]        |
| History                                         [RECOMMENDED]        |
+---------------------------------------------------------------------+
```

---

## Frontmatter

```yaml
# =============================================================================
# BUG WORK ITEM
# Source: ONTOLOGY-v1.md Section 3.4.10 (Bug Entity Schema)
# =============================================================================

# Identity (inherited from WorkItem - Section 2.1)
id: "{{BUG_ID}}"                           # Required, immutable - Format: BUG-NNN
work_type: BUG                             # Required, immutable - Discriminator
title: "{{BUG_TITLE}}"                     # Required, 1-500 chars

# Classification
classification: BUSINESS                   # Optional - BUSINESS | ENABLER (default: BUSINESS)

# State (see State Machine below)
status: pending                            # Required - pending | in_progress | completed
resolution: null                           # Optional - FIXED | WONT_DO | DUPLICATE | CANNOT_REPRODUCE | OBSOLETE

# Priority & Impact
priority: medium                           # Required - critical | high | medium | low
impact: medium                             # Required - critical | high | medium | low

# People
assignee: "{{ASSIGNEE}}"                   # Optional - User responsible
created_by: "{{CREATED_BY}}"               # Required, auto-populated (reporter)

# Timestamps (auto-managed)
created_at: "{{CREATED_AT}}"               # Required, auto, immutable (ISO 8601)
updated_at: "{{UPDATED_AT}}"               # Required, auto (ISO 8601)
completed_at: null                         # Optional - When bug was fixed (ISO 8601)

# Hierarchy
parent_id: "{{PARENT_ID}}"                 # Required - Feature, Story, Epic, or Enabler ID

# Tags
tags: []                                   # Optional - String array

# =============================================================================
# QUALITY ITEM PROPERTIES (Section 3.3.3)
# =============================================================================
severity: major                            # Required - critical | major | minor | trivial
found_in_version: "{{FOUND_IN_VERSION}}"   # Optional - Version where defect was discovered
fix_version: "{{FIX_VERSION}}"             # Optional - Target version for the fix

# =============================================================================
# BUG-SPECIFIC PROPERTIES (Section 3.4.10)
# =============================================================================
reproduction_steps: |
  {{REPRODUCTION_STEPS}}                   # Required for non-trivial - Steps to reproduce (max: 20000 chars)
environment: |
  {{ENVIRONMENT}}                          # Required - Environment where bug occurs (max: 5000 chars)
root_cause: |
  {{ROOT_CAUSE}}                           # Required when completed - Root cause analysis (max: 10000 chars)
acceptance_criteria: |
  {{ACCEPTANCE_CRITERIA}}                  # Required - Conditions for bug to be considered fixed
```

---

## Summary

<!--
REQUIRED: Brief 1-2 sentence description of the bug.
Should be understandable without reading the full document.
-->

{{BUG_SUMMARY}}

**Key Details:**
- **Symptom:** {{SYMPTOM_DESCRIPTION}}
- **Frequency:** {{BUG_FREQUENCY}}
- **Workaround:** {{WORKAROUND_IF_ANY}}

---

## Reproduction Steps

<!--
REQUIRED for non-trivial severity (INV-BG02).
Provide clear, numbered steps to reproduce the issue.
-->

### Prerequisites

{{PREREQUISITES}}

### Steps to Reproduce

1. {{STEP_1}}
2. {{STEP_2}}
3. {{STEP_3}}

### Expected Result

{{EXPECTED_RESULT}}

### Actual Result

{{ACTUAL_RESULT}}

---

## Environment

<!--
REQUIRED: Document the environment where the bug occurs.
-->

| Attribute | Value |
|-----------|-------|
| **Operating System** | {{OS}} |
| **Browser/Runtime** | {{BROWSER_RUNTIME}} |
| **Application Version** | {{APP_VERSION}} |
| **Configuration** | {{CONFIGURATION}} |
| **Deployment** | {{DEPLOYMENT_ENVIRONMENT}} |

### Additional Environment Details

{{ADDITIONAL_ENVIRONMENT_DETAILS}}

---

## Evidence

<!--
COMPLETION EVIDENCE: Documentation supporting the bug report and verifying the fix.
- Pre-fix: Screenshots, logs, reproduction evidence
- Post-fix: Verification that bug is resolved and regression tests pass
This is audit trail evidence (proving work was done), not knowledge evidence (research citations).
-->

### Bug Documentation

| Evidence | Type | Description | Date |
|----------|------|-------------|------|
| {{EVIDENCE_1}} | Screenshot | {{DESC_1}} | {{DATE_1}} |
| {{EVIDENCE_2}} | Log | {{DESC_2}} | {{DATE_2}} |
| {{EVIDENCE_3}} | Recording | {{DESC_3}} | {{DATE_3}} |

### Fix Verification

<!--
Complete this section when status changes to completed.
-->

| Verification | Method | Result | Verified By | Date |
|--------------|--------|--------|-------------|------|
| Bug no longer reproducible | Manual test | {{RESULT_1}} | {{VERIFIER_1}} | {{DATE_1}} |
| Regression test added | Automated test | {{RESULT_2}} | {{VERIFIER_2}} | {{DATE_2}} |
| Related areas tested | {{METHOD_3}} | {{RESULT_3}} | {{VERIFIER_3}} | {{DATE_3}} |

### Verification Checklist

- [ ] Bug no longer reproducible with original steps
- [ ] Regression test added and passing
- [ ] No new issues introduced
- [ ] Code review approved

---

## Root Cause Analysis

<!--
REQUIRED when status is completed (INV-BG03).
Document the root cause once identified.
-->

### Investigation Summary

{{ROOT_CAUSE_INVESTIGATION}}

### Root Cause

{{ROOT_CAUSE_DESCRIPTION}}

### Contributing Factors

- {{CONTRIBUTING_FACTOR_1}}
- {{CONTRIBUTING_FACTOR_2}}

---

## Fix Description

<!--
REQUIRED when status is completed.
Document the fix that was applied.
-->

### Solution Approach

{{SOLUTION_APPROACH}}

### Changes Made

- {{CHANGE_1}}
- {{CHANGE_2}}

### Code References

| File | Change Description |
|------|-------------------|
| {{FILE_PATH_1}} | {{CHANGE_DESC_1}} |
| {{FILE_PATH_2}} | {{CHANGE_DESC_2}} |

---

## Acceptance Criteria

<!--
REQUIRED: Conditions for bug to be considered fixed.
All criteria must be verified before marking as completed.
-->

### Fix Verification

- [ ] {{FIX_CRITERION_1}}
- [ ] {{FIX_CRITERION_2}}
- [ ] Bug no longer reproducible with original steps

### Quality Checklist

- [ ] Regression tests added
- [ ] Existing tests still passing
- [ ] No new issues introduced
- [ ] Documentation updated (if applicable)

---

## Related Items

<!--
RECOMMENDED: Link to related work items, bugs, or changes.
-->

### Hierarchy

- **Parent:** [{{PARENT_TITLE}}]({{PARENT_LINK}})

### Related Items

- **Related Bug:** [{{RELATED_BUG}}]({{RELATED_BUG_LINK}})
- **Causing Change:** [{{CAUSING_CHANGE}}]({{CAUSING_CHANGE_LINK}})
- **Fix Commit:** [{{FIX_COMMIT}}]({{FIX_COMMIT_LINK}})

---

## State Machine Reference

<!--
Source: ONTOLOGY-v1.md Section 3.4.10 (Bug.state_machine)
Simplified to match worktracker conventions.
-->

```
+-------------------------------------------------------------------+
|                     BUG STATE MACHINE                              |
+-------------------------------------------------------------------+
|                                                                    |
|   +---------+     +-------------+     +-----------+               |
|   | PENDING |---->| IN_PROGRESS |---->| COMPLETED |               |
|   +---------+     +-------------+     +-----------+               |
|        |               |                   |                       |
|        |               |                   |                       |
|        v               v                   v                       |
|   (Triage)        (Working)           (Verified)                  |
|                                                                    |
+-------------------------------------------------------------------+

Allowed Transitions:
- pending -> in_progress: Start working on fix
- in_progress -> completed: Fix verified and closed
- in_progress -> pending: Deprioritized or blocked
- completed -> in_progress: Reopened (regression found)
```

---

## Containment Rules

<!--
Source: ONTOLOGY-v1.md Section 3.4.10 (Bug.containment)
-->

| Rule | Value |
|------|-------|
| **Allowed Children** | Task |
| **Allowed Parents** | Feature, Story, Epic, Enabler |
| **Max Depth** | 1 |

---

## Invariants

<!--
Source: ONTOLOGY-v1.md Section 3.4.10 (Bug.invariants)
-->

- **INV-Q01:** CRITICAL severity bugs must have assignee (inherited from QualityItem)
- **INV-Q02:** fix_version should be set before completed (inherited from QualityItem)
- **INV-BG01:** Bug can have Feature, Story, Epic, or Enabler as parent
- **INV-BG02:** reproduction_steps should be provided for non-TRIVIAL severity
- **INV-BG03:** root_cause should be documented when completed

---

## Severity Guide

| Severity | Description | Response Time |
|----------|-------------|---------------|
| **CRITICAL** | System crash, data loss, security vulnerability, no workaround | Immediate |
| **MAJOR** | Major functionality broken, significant impact, workaround exists | Same sprint |
| **MINOR** | Minor functionality issue, low impact, easy workaround | Backlog |
| **TRIVIAL** | Cosmetic issue, typo, no functional impact | Low priority |

---

## History

<!--
RECOMMENDED: Track status changes and key events.
Use ISO 8601 timestamps.
-->

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| {{CREATED_AT}} | {{CREATED_BY}} | pending | Initial report |
| {{DATE_2}} | {{AUTHOR_2}} | in_progress | Triage complete, fix started |
| {{DATE_3}} | {{AUTHOR_3}} | completed | Verified and closed |

---

## System Mapping

<!--
Source: ONTOLOGY-v1.md Section 3.4.10 (Bug.system_mapping)
-->

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Bug |
| **SAFe** | Defect (uses 'Defect' terminology) |
| **JIRA** | Bug |

---

<!--
DESIGN RATIONALE:
"Bug" preferred over "Defect" because it is used by 2/3 systems
and is more common in developer vernacular.
Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.2 (Canonical Name Rationale)

PATTERN COMPLIANCE:
- P-001: Blockquote Header [COMPLIANT]
- P-002: Summary Section [COMPLIANT]
- P-005: History/Changelog [COMPLIANT]
- P-006: ISO 8601 Timestamps [COMPLIANT]
- P-007: Horizontal Rule Separators [COMPLIANT]
- P-019: Parent Reference [COMPLIANT]

WORKTRACKER ALIGNMENT:
- Status values: pending, in_progress, completed (per work-items.md)
- Priority/Impact: critical, high, medium, low (per work-items.md)
-->
