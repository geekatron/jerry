# {{PARENT_ID}}:DEC-{{NNN}}: {{DECISION_TITLE}}

<!--
TEMPLATE: Decision
VERSION: 1.0.0
SOURCE: worktracker.md (Decision File), ADR/MADR best practices
CREATED: 2026-01-23 (EN-001 Phase 2A)
PURPOSE: Document architectural/technical decisions with Q&A context
USAGE: For capturing decisions made during work, including user-agent discussions
EXTENDS: KnowledgeItem -> WorkItem (worktracker-specific, not in ONTOLOGY)

REQUIREMENTS SATISFIED:
- REQ-DEC-001 to REQ-DEC-023 (nse-requirements-001-template-requirements.md)
- REQ-C-001 to REQ-C-013 (common requirements)
-->

> **Type:** decision
> **Status:** {{STATUS}}
> **Priority:** {{PRIORITY}}
> **Created:** {{CREATED_AT}}
> **Parent:** {{PARENT_ID}}
> **Owner:** {{OWNER}}
> **Related:** {{RELATED_ITEMS}}

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Frontmatter](#frontmatter) | YAML metadata schema for decisions |
| [State Machine](#state-machine) | Decision status transitions |
| [Containment Rules](#containment-rules) | Parent/child constraints |
| [Summary](#summary) | Brief description of decisions captured |
| [Decision Context](#decision-context) | Background and constraints |
| [Decisions](#decisions) | Structured D-NNN decision entries |
| [Decision Summary](#decision-summary) | Quick reference table of all decisions |
| [Related Artifacts](#related-artifacts) | Traceability to parent and related items |
| [Document History](#document-history) | Track changes to this document |
| [Metadata](#metadata) | Machine-readable metadata |

---

## Frontmatter

```yaml
# =============================================================================
# DECISION WORK ITEM
# Source: worktracker.md (Decision File), ADR/MADR best practices
# Purpose: Document decisions made during work with Q&A context
# =============================================================================

# Identity (inherited from WorkItem)
id: "{{PARENT_ID}}:DEC-{{NNN}}"           # Required, immutable - Format: PARENT:DEC-NNN
work_type: DECISION                        # Required, immutable - Discriminator
title: "{{DECISION_TITLE}}"                # Required - Max 500 chars

# State (see State Machine below)
status: PENDING                            # Required - PENDING | DOCUMENTED | SUPERSEDED | ACCEPTED

# Priority
priority: MEDIUM                           # Optional - CRITICAL | HIGH | MEDIUM | LOW

# People
created_by: "{{CREATED_BY}}"               # Required, auto-populated
participants:                              # Required - Array of decision participants
  - "{{PARTICIPANT_1}}"
  - "{{PARTICIPANT_2}}"

# Timestamps (auto-managed)
created_at: "{{CREATED_AT}}"               # Required, auto, immutable (ISO 8601)
updated_at: "{{UPDATED_AT}}"               # Required, auto (ISO 8601)
decided_at: null                           # Optional - When decisions were accepted (ISO 8601)

# Hierarchy
parent_id: "{{PARENT_ID}}"                 # Required - Parent work item (Epic, Feature, Story, Enabler)

# Tags
tags: []                                   # Optional - String array (e.g., ["architecture", "api-design"])

# =============================================================================
# DECISION-SPECIFIC PROPERTIES
# =============================================================================

# Supersession (for ADR pattern)
superseded_by: null                        # Optional - ADR/DEC ID that replaces this decision
supersedes: null                           # Optional - ADR/DEC ID this decision replaces

# Decision Count
decision_count: 0                          # Auto-calculated from D-NNN entries
```

---

## State Machine

<!--
Source: nse-architecture-001-template-architecture.md Section 5.2
INV-SM-002: DECISION Status Transitions
-->

```
              +----------+
              |  PENDING |  <-- Initial state (awaiting input)
              +----+-----+
                   |
                   v
            +------------+
            | DOCUMENTED |  <-- Decisions captured
            +------+-----+
                   |
         +---------+---------+
         |                   |
         v                   v
   +------------+      +----------+
   | SUPERSEDED |      | ACCEPTED |
   +------------+      +----------+
   (Terminal)          (Terminal)
```

| Status | Description | Entry Criteria | Exit Criteria |
|--------|-------------|----------------|---------------|
| `PENDING` | Awaiting decisions | Decision document created | First decision captured |
| `DOCUMENTED` | Decisions recorded | Q&A completed, decisions documented | Formal acceptance or supersession |
| `SUPERSEDED` | Replaced by ADR/new DEC | ADR created or new decision | Terminal (no exit) |
| `ACCEPTED` | Decisions finalized | Stakeholder approval | Terminal (no exit) |

**Allowed Transitions:**
- PENDING -> DOCUMENTED (decisions captured)
- DOCUMENTED -> ACCEPTED (stakeholder approval)
- DOCUMENTED -> SUPERSEDED (replaced by ADR or new decision)

**Forbidden:**
- ACCEPTED -> any (terminal state)
- SUPERSEDED -> any (terminal state)

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
| **Co-Location** | MUST be in parent's folder |

---

## Summary

<!--
Required (REQ-DEC-009): Brief description of decision(s) captured.
Should be understandable without reading the full document.
-->

{{SUMMARY_STATEMENT}}

**Decisions Captured:** {{DECISION_COUNT}}

**Key Outcomes:**
- {{KEY_OUTCOME_1}}
- {{KEY_OUTCOME_2}}

---

## Decision Context

<!--
Optional (REQ-DEC-010): Background leading to these decisions.
- What situation prompted these decisions?
- Why did these decisions need to be made?
- What constraints or requirements existed?
-->

### Background

{{BACKGROUND_DESCRIPTION}}

### Constraints

- {{CONSTRAINT_1}}
- {{CONSTRAINT_2}}

### Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| {{STAKEHOLDER_1}} | {{ROLE_1}} | {{INTEREST_1}} |

---

## Decisions

<!--
Required (REQ-DEC-011): Structured decision entries.
Each decision follows the D-{NNN} format with required subsections.

STRUCTURE PER DECISION:
- Question/Context [REQUIRED] - REQ-DEC-012
- Options Considered [SHOULD] - REQ-DEC-013
- Decision [REQUIRED] - REQ-DEC-014
- Rationale [REQUIRED] - REQ-DEC-015
- Date and Participants [REQUIRED] - REQ-DEC-016
- Implications [SHOULD] - optional
-->

### D-001: {{DECISION_1_TITLE}}

**Date:** {{DECISION_1_DATE}}
**Participants:** {{DECISION_1_PARTICIPANTS}}

#### Question/Context

<!--
Required (REQ-DEC-012): What question was asked or what context prompted this decision?
Captures Q&A context when Claude asks for clarification (REQ-DEC-020).
-->

{{QUESTION_1}}

#### Options Considered

<!--
Should (REQ-DEC-013): Alternative approaches evaluated.
-->

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | {{OPTION_A_DESC}} | {{OPTION_A_PROS}} | {{OPTION_A_CONS}} |
| **B** | {{OPTION_B_DESC}} | {{OPTION_B_PROS}} | {{OPTION_B_CONS}} |

#### Decision

<!--
Required (REQ-DEC-014): The choice made - clear, unambiguous statement.
-->

**We decided:** {{DECISION_1_STATEMENT}}

#### Rationale

<!--
Required (REQ-DEC-015): Why this decision was made.
-->

{{RATIONALE_1}}

#### Implications

<!--
Optional: Impact of this decision.
-->

- **Positive:** {{POSITIVE_1}}
- **Negative:** {{NEGATIVE_1}}
- **Follow-up required:** {{FOLLOWUP_1}}

---

### D-002: {{DECISION_2_TITLE}}

**Date:** {{DECISION_2_DATE}}
**Participants:** {{DECISION_2_PARTICIPANTS}}

#### Question/Context

{{QUESTION_2}}

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | {{OPTION_A_DESC}} | {{OPTION_A_PROS}} | {{OPTION_A_CONS}} |
| **B** | {{OPTION_B_DESC}} | {{OPTION_B_PROS}} | {{OPTION_B_CONS}} |

#### Decision

**We decided:** {{DECISION_2_STATEMENT}}

#### Rationale

{{RATIONALE_2}}

---

<!--
Add additional D-NNN sections as needed following the same structure.
-->

## Decision Summary

<!--
Should (REQ-DEC-017): Quick reference table of all decisions.
-->

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-001 | {{DECISION_1_SUMMARY}} | {{DECISION_1_DATE}} | {{DECISION_1_STATUS}} |
| D-002 | {{DECISION_2_SUMMARY}} | {{DECISION_2_DATE}} | {{DECISION_2_STATUS}} |

---

## Related Artifacts

<!--
Required (REQ-DEC-018, REQ-C-005): Traceability to parent and related items.
-->

| Type | Path | Description |
|------|------|-------------|
| Parent | [{{PARENT_ID}}]({{PARENT_PATH}}) | Parent work item |
| Reference | {{REFERENCE_PATH}} | {{REFERENCE_DESCRIPTION}} |
| Supersedes | {{SUPERSEDED_ID}} | Decision this replaces (if applicable) |
| Superseded By | {{SUPERSEDING_ID}} | Decision that replaces this (if applicable) |
| Related | {{RELATED_PATH}} | {{RELATED_DESCRIPTION}} |
| Convention | [docs/conventions/worktracker.md](../../../conventions/worktracker.md) | Worktracker conventions |

---

## Document History

<!--
Should (REQ-DEC-022): Track changes to this decision document.
-->

| Date | Author | Change |
|------|--------|--------|
| {{UPDATED_AT}} | {{AUTHOR}} | {{CHANGE_DESCRIPTION}} |
| {{CREATED_AT}} | {{CREATED_BY}} | Created decision document |

---

## Metadata

<!--
Required (REQ-DEC-019): Machine-readable metadata for tooling and automation.
Keep in sync with frontmatter above.
-->

```yaml
id: "{{PARENT_ID}}:DEC-{{NNN}}"
parent_id: "{{PARENT_ID}}"
work_type: DECISION
title: "{{DECISION_TITLE}}"
status: {{STATUS}}
priority: {{PRIORITY}}
created_by: "{{CREATED_BY}}"
created_at: "{{CREATED_AT}}"
updated_at: "{{UPDATED_AT}}"
decided_at: {{DECIDED_AT}}
participants: [{{PARTICIPANT_1}}, {{PARTICIPANT_2}}]
tags: [{{TAG_1}}, {{TAG_2}}]
decision_count: {{DECISION_COUNT}}
superseded_by: {{SUPERSEDED_BY}}
supersedes: {{SUPERSEDES}}
```

---

<!--
DESIGN RATIONALE:

This template captures decisions made during work, focusing on the Q&A context
between user and Claude. It follows ADR (Architecture Decision Record) and MADR
(Markdown Any Decision Record) best practices while integrating with the
worktracker hierarchy.

KEY DESIGN CHOICES:

1. Q&A Context Capture (REQ-DEC-020): The D-NNN structure with Question/Context
   preserves the conversation flow when decisions arise from clarification questions.

2. Options Considered: Following AWS ADR best practices, we document alternatives
   evaluated to provide context for future reviewers.

3. Supersession Pattern (REQ-DEC-023): Decisions can be superseded by ADRs for
   architectural decisions, or by new decisions for tactical choices.

4. Status State Machine: Four states (PENDING, DOCUMENTED, SUPERSEDED, ACCEPTED)
   with SUPERSEDED and ACCEPTED as terminal states - once finalized or replaced,
   decisions cannot be reopened.

5. Participants Array (REQ-DEC-008): Captures who participated in the decision
   for accountability and future reference.

SOURCES:
- MADR Template: https://adr.github.io/madr/
- AWS ADR Best Practices: Status patterns, options format
- Nygard 2011: Context-Decision-Consequences structure
- worktracker.md: Decision File specification
- nse-requirements-001-template-requirements.md: REQ-DEC-001 to REQ-DEC-023

TRACE:
- EN-001: Hierarchical Worktracker Conventions (parent enabler)
- nse-architecture-001-template-architecture.md: Section 1.2, 5.2
- ps-analyst-001-pattern-analysis.md: Section 3.2 DECISION Blueprint
-->
