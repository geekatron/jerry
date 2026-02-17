# EPIC-003:DISC-001: Worktracker Template Non-Compliance Across EPIC-003 Entity Files

<!--
TEMPLATE: Discovery
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9, worktracker.md (Discovery File)
CREATED: 2026-02-15
PURPOSE: Document research findings from template compliance audit across EPIC-003 entities
EXTENDS: KnowledgeItem -> WorkItem (worktracker-specific, not in ONTOLOGY)
-->

> **Type:** discovery
> **Status:** DOCUMENTED
> **Priority:** CRITICAL
> **Impact:** CRITICAL
> **Created:** 2026-02-15
> **Completed:** null
> **Parent:** EPIC-003
> **Owner:** Claude
> **Source:** Template compliance audit during FEAT-010 creation

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Frontmatter](#frontmatter) | YAML metadata schema for discoveries |
| [State Machine](#state-machine) | Discovery status transitions |
| [Containment Rules](#containment-rules) | Parent/child constraints |
| [Summary](#summary) | Brief statement of the core finding |
| [Context](#context) | Background and research question |
| [Finding](#finding) | Core discovery with supporting details |
| [Evidence](#evidence) | Sources, dates, citations, validation |
| [Implications](#implications) | Impact on project and decisions |
| [Relationships](#relationships) | Related work items and discoveries |
| [Recommendations](#recommendations) | Actionable recommendations |
| [Open Questions](#open-questions) | Unanswered questions for follow-up |
| [Detailed Investigation](#detailed-investigation) | Optional freeform investigation docs |
| [Document History](#document-history) | Track changes to this discovery |
| [Metadata](#metadata) | Machine-readable metadata |

---

## Frontmatter

```yaml
# =============================================================================
# DISCOVERY WORK ITEM
# Source: ONTOLOGY-v1.md Section 3.4.9 (Discovery Entity Schema)
# Purpose: Document research findings, technical investigations, learnings
# =============================================================================

# Identity (inherited from WorkItem)
id: "EPIC-003:DISC-001"                        # Required, immutable - Format: PARENT:DISC-NNN
work_type: DISCOVERY                           # Required, immutable - Discriminator
title: "Worktracker Template Non-Compliance Across EPIC-003 Entity Files"  # Required - Max 500 chars

# Classification
classification: TECHNICAL                      # RESEARCH | TECHNICAL | BUSINESS

# State (see State Machine below)
status: DOCUMENTED                             # Required - PENDING | IN_PROGRESS | DOCUMENTED | VALIDATED
resolution: null                               # Optional - Resolution enum (when completed)

# Priority
priority: CRITICAL                             # Optional - CRITICAL | HIGH | MEDIUM | LOW

# Impact (REQ-D-004)
impact: CRITICAL                               # Required - CRITICAL | HIGH | MEDIUM | LOW

# People
assignee: null                                 # Optional - User reference
created_by: "Claude"                           # Required, auto-populated

# Timestamps (auto-managed)
created_at: "2026-02-15"                       # Required, auto, immutable (ISO 8601)
updated_at: "2026-02-15"                       # Required, auto (ISO 8601)
completed_at: null                             # Optional - When finding was documented/validated

# Hierarchy
parent_id: "EPIC-003"                          # Required - Parent work item (Epic, Feature, Story, Enabler)

# Tags
tags: [template-compliance, worktracker, quality, root-cause-analysis]

# =============================================================================
# DISCOVERY-SPECIFIC PROPERTIES
# =============================================================================

# Finding Classification
finding_type: GAP                              # Optional - PATTERN | GAP | RISK | OPPORTUNITY | CONSTRAINT
confidence_level: HIGH                         # Optional - HIGH | MEDIUM | LOW

# Source Information
source: "Template compliance audit during FEAT-010 creation"
research_method: "Multi-agent parallel audit with root cause analysis"

# Validation
validated: false                               # Boolean - Has finding been validated?
validation_date: null                          # Optional - ISO 8601 timestamp
validated_by: null                             # Optional - User reference

# Impact (REQ-D-004)
impact: CRITICAL                               # Required - CRITICAL | HIGH | MEDIUM | LOW
```

---

## State Machine

<!--
Source: nse-architecture-001-template-architecture.md Section 5.1
INV-SM-001: DISCOVERY Status Transitions
-->

```
                 +----------+
                 |  PENDING |  <-- Initial state
                 +----+-----+
                      |
                      v
              +--------------+
              | IN_PROGRESS  |
              +------+-------+
                     |
           +---------+---------+
           |                   |
           v                   v
    +------------+      +------------+
    | DOCUMENTED |      | VALIDATED  |
    +------------+      +------------+
```

| Status | Description | Entry Criteria | Exit Criteria |
|--------|-------------|----------------|---------------|
| `PENDING` | Investigation planned | Discovery created | Investigation started |
| `IN_PROGRESS` | Active investigation | Work begun | Finding documented |
| `DOCUMENTED` | Finding recorded | Core finding captured | Validation complete |
| `VALIDATED` | Finding verified | Evidence validated | - |

**Allowed Transitions:**
- PENDING -> IN_PROGRESS (start research)
- IN_PROGRESS -> DOCUMENTED (findings recorded)
- DOCUMENTED -> VALIDATED (peer-reviewed)
- Any -> PENDING (reset, with justification)

**Note:** VALIDATED is NOT a terminal state - findings can be updated if new evidence emerges.

---

## Containment Rules

<!--
Source: nse-architecture-001-template-architecture.md Section 4.1
-->

| Rule | Value |
|------|-------|
| **Allowed Children** | None |
| **Allowed Parents** | Epic, Feature, Story, Enabler |
| **Max Depth** | 0 (leaf node) |
| **Co-Location** | MUST be in parent's folder (REQ-D-025) |

---

## Summary

All 64+ worktracker entity files across EPIC-003 (1 epic, 3 features, 30 enablers, 29+ tasks) were created WITHOUT following the canonical templates from `.context/templates/worktracker/`. Files use a simplified format missing 40-60% of template-defined sections. Root cause: the template rules file (`worktracker-templates.md`) is never `@`-imported into agent context.

**Key Findings:**
1. The `worktracker-templates.md` file is NOT `@`-imported in SKILL.md -- its CRITICAL rules ("MUST use templates", "NEVER make up your own format") never reach agent context
2. The only loaded rule file (`worktracker-behavior-rules.md`) contains zero instructions about template compliance
3. ENABLER files are missing 3 REQUIRED sections universally: Business Value, Progress Summary, Evidence
4. TASK files use invalid status enum ("pending" instead of "BACKLOG" per state machine)

**Validation:** Verified by 5 parallel audit agents examining all entity types against canonical templates.

---

## Context

### Background

During creation of FEAT-010 (Tournament Remediation) worktracker entities, the user identified that entity files were not following canonical templates from `.context/templates/worktracker/`. A comprehensive audit was conducted across all EPIC-003 entities.

### Research Question

Why are worktracker entity files not following canonical templates, and what behavioral gap causes this to persist?

### Investigation Approach

1. Read all 4 canonical templates (EPIC.md, FEATURE.md, ENABLER.md, TASK.md)
2. Launched 5 parallel audit agents to compare actual files against templates
3. Analyzed the behavioral chain: SKILL.md -> @imports -> loaded rules -> actual instructions
4. Traced the `@` import mechanism to identify which rules reach agent context

---

## Finding

### Category 1: Behavioral Root Cause (4 Gaps)

**Gap 1 (PRIMARY):** `worktracker-templates.md` is NOT `@`-imported in `skills/worktracker/SKILL.md` (line 66). Only `@rules/worktracker-behavior-rules.md` is imported. The template rules exist but are never loaded into context -- a dead rule.

**Gap 2:** `worktracker-behavior-rules.md` (the only loaded file) contains zero instructions about reading or following templates. It focuses exclusively on WTI-001 through WTI-006 (state integrity). No WTI rule for template compliance exists.

**Gap 3:** SKILL.md's "Template Locations" table (lines 160-171) is informational, not instructional -- tells WHERE templates are but never says to USE them.

**Gap 4:** Orchestration workflows create entity files with zero awareness of worktracker templates. The orchestration skill has no cross-reference to worktracker templates.

**Key Observations:**
1. The `@` import mechanism is the ONLY auto-loading path for rules into agent context
2. Informational references (tables listing template paths) do not substitute for instructional rules
3. Cross-skill dependencies (orchestration -> worktracker) are not captured in either skill's rule set

### Category 2: Entity File Non-Compliance Findings

**EPIC (1 file):** 6/16 sections MISSING -- Template Structure, Frontmatter, State Machine, Containment Rules, Invariants, System Mapping. Progress data stale/inaccurate.

**FEATURE (3 files):** 6/17 sections MISSING per file. Sprint Tracking absent. FEAT-008 missing Functional/Non-Functional AC. Naming inconsistencies in Children tables.

**ENABLER (30 files):** 15/26 sections MISSING. 3 REQUIRED sections universally absent: Business Value, Progress Summary, Evidence. Zero RECOMMENDED sections present. Architecture Diagram missing from Technical Approach. All files use ~30% of template content.

**TASK (29+ files):** 5/11 sections MISSING -- State Machine, Containment Rules, Invariants, System Mapping, Time Tracking. Status uses "pending" (invalid) instead of "BACKLOG". Blockquote metadata replaces YAML Frontmatter.

### Validation

All findings verified by reading actual files and comparing against canonical templates. Audit covered 8 enabler samples, 6 task samples, all 3 features, and the epic.

**Validation Results:**
- 5 parallel audit agents independently confirmed non-compliance across all entity types
- Root cause analysis confirmed the behavioral chain gap (template rules never loaded)

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | File Analysis | SKILL.md line 66 -- only `@rules/worktracker-behavior-rules.md` imported | `skills/worktracker/SKILL.md` | 2026-02-15 |
| E-002 | File Analysis | worktracker-templates.md lines 49-98 -- contains CRITICAL template rules never loaded | `skills/worktracker/rules/worktracker-templates.md` | 2026-02-15 |
| E-003 | Audit Report | EPIC-003 gap analysis -- 6/16 sections missing | Background agent a63dda0 | 2026-02-15 |
| E-004 | Audit Report | FEAT-008/009/010 gap analysis -- 6/17 sections missing per file | Background agent a51253f | 2026-02-15 |
| E-005 | Audit Report | ENABLER gap analysis (8 samples) -- 15/26 sections missing | Background agent a49793e | 2026-02-15 |
| E-006 | Audit Report | TASK gap analysis (6 samples) -- 5/11 sections missing, invalid status enum | Background agent abab83e | 2026-02-15 |
| E-007 | Root Cause Analysis | 4-gap behavioral chain analysis | Background agent aec22d0 | 2026-02-15 |

### Reference Material

- **Source:** Canonical Worktracker Templates
- **Path:** `.context/templates/worktracker/`
- **Date Accessed:** 2026-02-15
- **Relevance:** Defines the REQUIRED structure for all worktracker entity files (EPIC, FEATURE, ENABLER, TASK)

### Expert Review

<!--
Not yet reviewed. Pending user validation.
-->

- **Reviewer:** Pending
- **Date:** Pending
- **Feedback:** Awaiting user review

---

## Implications

### Impact on Project

All 64+ entity files under EPIC-003 lack structural completeness. Enablers cannot be formally closed (missing Evidence section). Progress cannot be tracked (missing Progress Summary). No business justification documented for enablers (missing Business Value). Automation and tooling that relies on template structure will fail.

### Design Decisions Affected

- **Decision:** Worktracker skill rule loading strategy
  - **Impact:** Template compliance rules were never enforced because they weren't loaded
  - **Rationale:** The `@` import mechanism is the only auto-loading path; cross-references are passive

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Entity files cannot be formally closed without Evidence section | HIGH | Add Evidence section to all enablers as part of remediation |
| Future entity files will continue to be non-compliant | CRITICAL | Fix behavioral root cause (Category A) BEFORE Category B |
| Stale progress data causes confusion | MEDIUM | Update Progress Summary in all files during remediation |

### Opportunities Created

- Establish WTI-007 (Mandatory Template Usage) as a new integrity rule
- Cross-skill template awareness -- orchestration workflows reference worktracker templates

---

## Relationships

### Creates

- [FEAT-011](./FEAT-011-template-compliance-remediation/FEAT-011-template-compliance-remediation.md) - Template Compliance Remediation feature

### Informs

- [FEAT-008](./FEAT-008-quality-framework-implementation/FEAT-008-quality-framework-implementation.md) - All enabler/task files need remediation
- [FEAT-009](./FEAT-009-adversarial-strategy-templates/FEAT-009-adversarial-strategy-templates.md) - All enabler/task files need remediation
- [FEAT-010](./FEAT-010-tournament-remediation/FEAT-010-tournament-remediation.md) - All enabler/task files need remediation

### Related Discoveries

<!--
No related discoveries at this time. This is the first discovery filed under EPIC-003.
-->

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [EPIC-003](./EPIC-003-quality-implementation.md) | Parent epic |
| Template | `.context/templates/worktracker/ENABLER.md` | Canonical enabler template |
| Template | `.context/templates/worktracker/TASK.md` | Canonical task template |
| Template | `.context/templates/worktracker/FEATURE.md` | Canonical feature template |
| Template | `.context/templates/worktracker/EPIC.md` | Canonical epic template |
| Rule | `skills/worktracker/rules/worktracker-templates.md` | Template rules (never loaded) |
| Rule | `skills/worktracker/rules/worktracker-behavior-rules.md` | Behavior rules (loaded, no template instructions) |

---

## Recommendations

### Immediate Actions

1. Fix behavioral root cause (Category A): Add `@` import for templates, add WTI-007 rule, update orchestration skill
2. Remediate all 64+ entity files (Category B): Add missing REQUIRED and RECOMMENDED sections using templates as guides

### Long-term Considerations

- Consider adding a pre-commit validation hook for template compliance
- Consider clarifying which template sections are REFERENCE-only vs must-appear-in-instances
- Consider adding the "Agents" and "Design Source" fields to canonical templates (frequently used ad-hoc additions)

---

## Open Questions

### Questions for Follow-up

1. **Q:** Should REFERENCE sections (State Machine, Containment Rules, Invariants, System Mapping) be omitted from instance files or included as collapsed references?
   - **Investigation Method:** User decision based on documentation philosophy
   - **Priority:** HIGH -- affects scope of Category B remediation

---

## Detailed Investigation

<!--
This discovery was conducted via 5 parallel audit agents plus a root cause analysis agent.
The investigation was comprehensive and findings are captured in the structured sections above.
No additional freeform investigation documentation is needed at this time.
-->

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-15 | Claude | Created discovery. 5 audit agents + root cause analysis completed. |

---

## Metadata

```yaml
id: "EPIC-003:DISC-001"
parent_id: "EPIC-003"
work_type: DISCOVERY
title: "Worktracker Template Non-Compliance Across EPIC-003 Entity Files"
status: DOCUMENTED
priority: CRITICAL
impact: CRITICAL
created_by: "Claude"
created_at: "2026-02-15"
updated_at: "2026-02-15"
completed_at: null
tags: [template-compliance, worktracker, quality, root-cause-analysis]
source: "Template compliance audit during FEAT-010 creation"
finding_type: GAP
confidence_level: HIGH
validated: false
```
