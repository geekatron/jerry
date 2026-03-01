# {{PARENT_ID}}:DISC-{{NNN}}: {{DISCOVERY_TITLE}}

<!--
TEMPLATE: Discovery
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9, worktracker.md (Discovery File)
CREATED: 2026-01-22 (TASK-001)
UPDATED: 2026-01-23 (EN-001 Phase 2A - NSE compliance)
PURPOSE: Document research findings, technical investigations, and architectural discoveries
USAGE: For both concise findings (47-137 lines) and detailed investigations (432+ lines)
EXTENDS: KnowledgeItem -> WorkItem (worktracker-specific, not in ONTOLOGY)

REQUIREMENTS SATISFIED:
- REQ-D-001 to REQ-D-025 (nse-requirements-001-template-requirements.md)
- REQ-C-001 to REQ-C-013 (common requirements)
-->

> **Type:** discovery
> **Status:** {{STATUS}}
> **Priority:** {{PRIORITY}}
> **Impact:** {{IMPACT}}
> **Created:** {{CREATED_AT}}
> **Completed:** {{COMPLETED_AT}}
> **Parent:** {{PARENT_ID}}
> **Owner:** {{OWNER}}
> **Source:** {{SOURCE}}

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
id: "{{PARENT_ID}}:DISC-{{NNN}}"           # Required, immutable - Format: PARENT:DISC-NNN
work_type: DISCOVERY                        # Required, immutable - Discriminator
title: "{{DISCOVERY_TITLE}}"                # Required - Max 500 chars

# Classification
classification: RESEARCH                    # Optional - RESEARCH | TECHNICAL | BUSINESS

# State (see State Machine below)
status: PENDING                             # Required - PENDING | IN_PROGRESS | DOCUMENTED | VALIDATED
resolution: null                            # Optional - Resolution enum (when completed)

# Priority
priority: MEDIUM                            # Optional - CRITICAL | HIGH | MEDIUM | LOW

# Impact (REQ-D-004)
impact: MEDIUM                              # Required - CRITICAL | HIGH | MEDIUM | LOW

# People
assignee: null                              # Optional - User reference
created_by: "{{CREATED_BY}}"                # Required, auto-populated

# Timestamps (auto-managed)
created_at: "{{CREATED_AT}}"                # Required, auto, immutable (ISO 8601)
updated_at: "{{UPDATED_AT}}"                # Required, auto (ISO 8601)
completed_at: null                          # Optional - When finding was documented/validated

# Hierarchy
parent_id: "{{PARENT_ID}}"                  # Required - Parent work item (Epic, Feature, Story, Enabler)

# Tags
tags: []                                    # Optional - String array (e.g., ["architecture", "security", "performance"])

# =============================================================================
# DISCOVERY-SPECIFIC PROPERTIES
# =============================================================================

# Finding Classification
finding_type: null                          # Optional - PATTERN | GAP | RISK | OPPORTUNITY | CONSTRAINT
confidence_level: null                      # Optional - HIGH | MEDIUM | LOW

# Source Information
source: null                                # Optional - Origin of discovery (research, analysis, incident)
research_method: null                       # Optional - How discovery was made (analysis, investigation, etc.)

# Validation
validated: false                            # Boolean - Has finding been validated?
validation_date: null                       # Optional - ISO 8601 timestamp
validated_by: null                          # Optional - User reference

# Impact (REQ-D-004)
impact: MEDIUM                              # Required - CRITICAL | HIGH | MEDIUM | LOW
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

<!--
Required: Brief 1-2 sentence statement of the core finding.
Should be understandable without reading the full document.
-->

{{SUMMARY_STATEMENT}}

**Key Findings:**
- {{KEY_FINDING_1}}
- {{KEY_FINDING_2}}
- {{KEY_FINDING_3}}

**Validation:** {{VALIDATION_STATUS}}

---

## Context

<!--
Required: Background information that led to this discovery.
- What question were you trying to answer?
- What problem were you investigating?
- Why was this research necessary?
- What approach did you take?
-->

### Background

{{BACKGROUND_DESCRIPTION}}

### Research Question

{{RESEARCH_QUESTION}}

### Investigation Approach

1. {{INVESTIGATION_STEP_1}}
2. {{INVESTIGATION_STEP_2}}
3. {{INVESTIGATION_STEP_3}}

---

## Finding

<!--
Required: Core discovery with supporting details.
Use subsections to organize complex findings.
-->

### {{FINDING_CATEGORY_1}}

{{FINDING_DETAILS_1}}

**Key Observations:**
1. {{OBSERVATION_1}}
2. {{OBSERVATION_2}}
3. {{OBSERVATION_3}}

### {{FINDING_CATEGORY_2}}

{{FINDING_DETAILS_2}}

### Validation

<!--
Optional: How was the finding validated?
Include user feedback, testing results, or expert review.
-->

{{VALIDATION_APPROACH}}

**Validation Results:**
- {{VALIDATION_RESULT_1}}
- {{VALIDATION_RESULT_2}}

---

## Evidence

<!--
Required: Sources, dates, citations, and validation evidence.
All claims must be traceable to sources.
-->

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | {{TYPE}} | {{DESCRIPTION}} | {{SOURCE_URL}} | {{VERIFICATION_DATE}} |
| E-002 | {{TYPE}} | {{DESCRIPTION}} | {{SOURCE_URL}} | {{VERIFICATION_DATE}} |

### Reference Material

- **Source:** {{SOURCE_NAME}}
- **URL:** {{SOURCE_URL}}
- **Date Accessed:** {{ACCESS_DATE}}
- **Relevance:** {{WHY_RELEVANT}}

### Expert Review

<!--
Optional: If findings were reviewed by subject matter experts
-->

- **Reviewer:** {{REVIEWER_NAME}}
- **Date:** {{REVIEW_DATE}}
- **Feedback:** {{REVIEW_FEEDBACK}}

---

## Implications

<!--
Required: Impact of this discovery on the project.
- What work items does this create or inform?
- What design decisions are affected?
- What risks or opportunities exist?
-->

### Impact on Project

{{IMPACT_DESCRIPTION}}

### Design Decisions Affected

- **Decision:** {{DECISION_ITEM_1}}
  - **Impact:** {{IMPACT_1}}
  - **Rationale:** {{RATIONALE_1}}

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| {{RISK_1}} | {{SEVERITY}} | {{MITIGATION_1}} |

### Opportunities Created

- {{OPPORTUNITY_1}}
- {{OPPORTUNITY_2}}

---

## Relationships

<!--
Required: How this discovery relates to other work.
-->

### Creates

<!--
Work items created as a result of this discovery
-->

- [{{WORK_ITEM_ID}}]({{WORK_ITEM_PATH}}) - {{WORK_ITEM_DESCRIPTION}}

### Informs

<!--
Work items informed or influenced by this discovery
-->

- [{{WORK_ITEM_ID}}]({{WORK_ITEM_PATH}}) - {{WORK_ITEM_DESCRIPTION}}

### Related Discoveries

<!--
Other discoveries that relate to this finding
-->

- [{{DISC_ID}}]({{DISC_PATH}}) - {{DISC_DESCRIPTION}}

### Related Artifacts

<!--
Source materials, references, documentation
-->

| Type | Path | Description |
|------|------|-------------|
| Parent | [{{PARENT_LINK}}] | Parent work item |
| Reference | {{REFERENCE_PATH}} | {{REFERENCE_DESCRIPTION}} |
| Convention | [docs/conventions/worktracker.md](../../docs/conventions/worktracker.md) | Worktracker conventions |

---

## Recommendations

<!--
Optional: Actionable recommendations based on findings.
Remove this section if no recommendations.
-->

### Immediate Actions

1. {{RECOMMENDATION_1}}
2. {{RECOMMENDATION_2}}

### Long-term Considerations

- {{LONG_TERM_1}}
- {{LONG_TERM_2}}

---

## Open Questions

<!--
Optional: Unanswered questions or areas for future investigation.
Remove this section if no open questions.
-->

### Questions for Follow-up

1. **Q:** {{QUESTION_1}}
   - **Investigation Method:** {{METHOD_1}}
   - **Priority:** {{PRIORITY_1}}

2. **Q:** {{QUESTION_2}}
   - **Investigation Method:** {{METHOD_2}}
   - **Priority:** {{PRIORITY_2}}

---

## Detailed Investigation

<!--
========================================
OPTIONAL FREEFORM SECTION
========================================

This section is for detailed investigation documentation in the style of
Jerry project disc-001 (432+ lines with Q&A, hypothesis testing, etc.).

Use this section when you need to document:
- Interactive Q&A sessions (Question → Answer → Follow-up → Resolution)
- Hypothesis testing (Hypothesis → Test → Result → Conclusion)
- Detailed validation results with user verification quotes
- Complex analysis with multiple iterations
- Evidence IDs and detailed source analysis

STRUCTURE SUGGESTIONS:
1. Q&A Session Documentation
2. Hypothesis Testing
3. Detailed Validation Results
4. Evidence Analysis
5. Synthesis and Conclusions

Remove this entire section if not needed for concise discoveries.
========================================
-->

### Q&A Session

<!--
Example format for documenting interactive problem-solving:

**Q1:** {{QUESTION}}
**A1:** {{ANSWER}}
**Follow-up:** {{FOLLOW_UP_QUESTION}}
**Resolution:** {{FINAL_ANSWER}}
-->

### Hypothesis Testing

<!--
Example format for testing hypotheses:

**Hypothesis:** {{HYPOTHESIS_STATEMENT}}
**Test:** {{TEST_APPROACH}}
**Result:** {{TEST_RESULT}}
**Conclusion:** {{CONCLUSION}}
-->

### Detailed Evidence Analysis

<!--
Example format for evidence with IDs:

**E-001: {{EVIDENCE_TITLE}}**
- **Source:** {{SOURCE}}
- **Finding:** {{FINDING}}
- **Validation:** {{VALIDATION}}
- **Significance:** {{SIGNIFICANCE}}
-->

---

## Document History

<!--
Required: Track changes to this discovery document.
-->

| Date | Author | Change |
|------|--------|--------|
| {{UPDATED_AT}} | {{AUTHOR}} | {{CHANGE_DESCRIPTION}} |
| {{CREATED_AT}} | {{CREATED_BY}} | Created discovery |

---

## Metadata

<!--
Required: Machine-readable metadata for tooling and automation.
Keep in sync with frontmatter above.
-->

```yaml
id: "{{PARENT_ID}}:DISC-{{NNN}}"
parent_id: "{{PARENT_ID}}"
work_type: DISCOVERY
title: "{{DISCOVERY_TITLE}}"
status: {{STATUS}}
priority: {{PRIORITY}}
impact: {{IMPACT}}
created_by: "{{CREATED_BY}}"
created_at: "{{CREATED_AT}}"
updated_at: "{{UPDATED_AT}}"
completed_at: {{COMPLETED_AT}}
tags: [{{TAG_1}}, {{TAG_2}}, {{TAG_3}}]
source: "{{SOURCE}}"
finding_type: {{FINDING_TYPE}}
confidence_level: {{CONFIDENCE_LEVEL}}
validated: {{VALIDATED}}
```

---

## Compaction Resilience (T-004)

| Constraint | Failure Mode if Lost | Compensating Control | Detection |
|-----------|---------------------|---------------------|-----------|
| Co-location (REQ-D-025): MUST be in parent's folder | Discovery placed in wrong directory | /worktracker skill enforcement (WTI rules) | Worktracker audit detects misplaced discovery |
| Status values: PENDING, IN_PROGRESS, DOCUMENTED, VALIDATED | Invalid status transition | L3 AST validation (H-33) | `jerry ast validate` rejects invalid status |
| Impact field REQUIRED (REQ-D-004) | Discovery created without impact assessment | L3 AST validation (H-33) | `jerry ast validate` rejects missing impact |
| ID format: PARENT:DISC-NNN | Incorrect ID format breaks traceability | /worktracker skill enforcement | Worktracker audit detects format violation |

<!--
DESIGN RATIONALE:

This template supports both concise discoveries (PROJ-001 style, 47-137 lines)
and detailed investigation documentation (Jerry disc-001 style, 432+ lines).

Mandatory sections (Summary, Context, Finding, Evidence, Implications, Relationships)
provide consistent structure across all discoveries. Optional sections
(Recommendations, Open Questions, Detailed Investigation) can be removed when
not needed.

The freeform "Detailed Investigation" section enables documenting complex
problem-solving sessions with Q&A, hypothesis testing, and detailed validation
while maintaining template consistency.

KEY DESIGN CHOICES:

1. Status State Machine (INV-SM-001): Four states (PENDING, IN_PROGRESS, DOCUMENTED,
   VALIDATED) with VALIDATED as the final validation stage but not strictly terminal.

2. Impact Field (REQ-D-004): Required field indicating criticality/severity of the
   discovery (CRITICAL, HIGH, MEDIUM, LOW).

3. Evidence Tiering: Supports inline (simple), table (standard), and academic
   (rigorous) evidence formats based on finding importance.

4. Co-location (REQ-D-025): Discoveries MUST be in parent's folder to maintain
   traceability hierarchy.

5. Dual-Mode Support: Concise mode (~100 lines) for quick findings, Investigation
   mode (400+ lines) for deep analysis with Q&A and hypothesis testing.

REQUIREMENTS SATISFIED:
- REQ-D-001 to REQ-D-025 (Discovery requirements)
- REQ-C-001 to REQ-C-013 (Common requirements)

SOURCES:
- ONTOLOGY-v1.md Section 3.4.9: Discovery entity schema
- worktracker.md: Discovery co-location and numbering conventions
- PROJ-001 DISC-001, DISC-022, DISC-033: Concise discovery examples
- Jerry project disc-001: Detailed investigation gold standard
- nse-requirements-001-template-requirements.md: REQ-D-001 to REQ-D-025
- nse-architecture-001-template-architecture.md: Section 1.1, 5.1
- ps-analyst-001-pattern-analysis.md: Section 3.1 DISCOVERY Blueprint

TRACE:
- EN-001: Hierarchical Worktracker Conventions (parent enabler)
- en-001-v1-template-validation: Phase 2A template creation
-->
