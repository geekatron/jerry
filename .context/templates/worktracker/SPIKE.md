# {{TITLE}}

<!--
TEMPLATE: Spike (DRAFT)
SOURCE: ONTOLOGY-v1.md Section 3.4.8
VERSION: 0.1.0
STATUS: DRAFT - Pending review

DESCRIPTION:
  Timeboxed research or exploration activity.
  Does NOT require quality gates (unlike other work types).
  Outputs knowledge/decisions, not production code.

EXTENDS: DeliveryItem -> WorkItem

IMPORTANT: Spikes are LEAF NODES - they cannot have children.
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Frontmatter](#frontmatter) | YAML metadata schema for spikes |
| [State Machine](#state-machine) | Spike status transitions |
| [Containment Rules](#containment-rules) | Parent/child constraints |
| [Invariants](#invariants) | Business rules and constraints |
| [System Mapping](#system-mapping) | ADO, SAFe, JIRA mappings |
| [Content](#content) | Research question, hypothesis, scope |
| [Findings](#findings) | Summary and detailed findings |
| [Recommendation](#recommendation) | Decision and recommended actions |
| [Related Items](#related-items) | Hierarchy and related work |
| [History](#history) | Status changes and key events |

---

## Frontmatter

```yaml
# === IDENTITY (Auto-generated, Immutable) ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
id: "{{ID}}"                           # Format: PREFIX-NNN (e.g., SPIKE-001)
work_type: SPIKE                       # Immutable discriminator

# === CORE METADATA ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
title: "{{TITLE}}"                     # Required, 1-500 chars
description: |
  {{DESCRIPTION}}

# === CLASSIFICATION ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
classification: ENABLER                # Spikes are typically ENABLER work

# === LIFECYCLE STATE ===
# Source: ONTOLOGY-v1.md Section 3.4.8 (Spike.state_machine)
status: BACKLOG                        # See State Machine below
resolution: null                       # Set when status is DONE or REMOVED

# === PRIORITY ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
priority: MEDIUM                       # CRITICAL | HIGH | MEDIUM | LOW

# === PEOPLE ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
assignee: "{{ASSIGNEE}}"               # Researcher responsible
created_by: "{{CREATED_BY}}"           # Auto-set on creation

# === TIMESTAMPS (Auto-managed) ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
created_at: "{{CREATED_AT}}"           # ISO 8601 datetime
updated_at: "{{UPDATED_AT}}"           # ISO 8601 datetime

# === HIERARCHY ===
# Source: ONTOLOGY-v1.md Section 3.4.8 (Spike.containment)
parent_id: "{{PARENT_ID}}"             # Feature or Story ID

# === TAGS ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
tags:
  - spike
  - "{{TAG_1}}"
  - "{{TAG_2}}"

# === DELIVERY ITEM PROPERTIES ===
# Source: ONTOLOGY-v1.md Section 3.3.2 (DeliveryItem)
effort: null                           # Story points or effort estimate (0-100)
acceptance_criteria: |
  {{ACCEPTANCE_CRITERIA}}              # What question needs to be answered?
due_date: null                         # ISO 8601 date (timebox end)

# === SPIKE-SPECIFIC PROPERTIES ===
# Source: ONTOLOGY-v1.md Section 3.4.8 (Spike.specific)
timebox: {{TIMEBOX}}                   # REQUIRED: Maximum duration in hours (1-336, i.e., max 2 weeks)
research_question: |
  {{RESEARCH_QUESTION}}                # The question the spike aims to answer (max: 500 chars)
findings: |
  {{FINDINGS}}                         # Research findings and conclusions (max: 20000 chars)
recommendation: |
  {{RECOMMENDATION}}                   # Recommended next steps based on findings (max: 10000 chars)

# === QUALITY GATES ===
# Source: ONTOLOGY-v1.md Section 3.4.8 (Spike.invariants INV-SP04)
requires_quality_gates: false          # Spikes do NOT require quality gates
```

---

## State Machine

<!-- Source: ONTOLOGY-v1.md Section 3.4.8 (Spike.state_machine) -->

**Initial State:** `BACKLOG`

**Valid States:** `BACKLOG`, `IN_PROGRESS`, `DONE`, `REMOVED`

**Note:** Spikes have a simplified state machine - no `READY`, `BLOCKED`, or `IN_REVIEW` states.
Once DONE, a spike CANNOT be reopened (research is complete).

```
              +-----------+
              |  BACKLOG  |
              +-----+-----+
                    |
          +---------+---------+
          |                   |
          v                   v
    +------------+       +---------+
    | IN_PROGRESS|------>| REMOVED |
    +-----+------+       +---------+
          |
          v
      +------+
      | DONE |  <-- Terminal (cannot reopen)
      +------+
```

| From State    | Allowed Transitions                    |
|---------------|----------------------------------------|
| BACKLOG       | IN_PROGRESS, REMOVED                   |
| IN_PROGRESS   | DONE, REMOVED                          |
| DONE          | (Terminal - cannot reopen)             |
| REMOVED       | (Terminal - no transitions)            |

---

## Containment Rules

<!-- Source: ONTOLOGY-v1.md Section 3.4.8 (Spike.containment) -->

| Rule             | Value                           |
|------------------|---------------------------------|
| Allowed Children | (None - Spike is a leaf node)   |
| Allowed Parents  | Feature, Story                  |
| Max Depth        | 0                               |

**Note:** INV-SP03 - Spike cannot have children. Spikes output research/decisions, not work breakdown.

---

## Invariants

<!-- Source: ONTOLOGY-v1.md Section 3.4.8 (Spike.invariants) -->

- **INV-D01:** effort must be non-negative (inherited from DeliveryItem)
- **INV-SP01:** timebox is REQUIRED and must be set (1-336 hours)
- **INV-SP02:** findings should be documented when DONE
- **INV-SP03:** Spike cannot have children
- **INV-SP04:** Spike does NOT require quality gates

---

## System Mapping

<!-- Source: ONTOLOGY-v1.md Section 3.4.8 (Spike.system_mapping) -->

| System | Mapping                                |
|--------|----------------------------------------|
| ADO    | Task (with 'spike' tag)                |
| SAFe   | Enabler Story (Exploration type)       |
| JIRA   | Task (with 'spike' label)              |

---

## Content

### Research Question

<!-- INV-SP01: Clearly define what question this spike aims to answer -->

**Question:** {{RESEARCH_QUESTION}}

### Hypothesis

<!-- Optional: State your hypothesis before research begins -->

{{HYPOTHESIS}}

### Timebox

| Aspect              | Value                           |
|---------------------|---------------------------------|
| Timebox Duration    | {{TIMEBOX}} hours               |
| Start Date          | {{START_DATE}}                  |
| Target End Date     | {{END_DATE}}                    |

**Warning:** Do not exceed the timebox. If more research is needed, create a follow-up spike.

### Scope

**In Scope:**
- {{IN_SCOPE_1}}
- {{IN_SCOPE_2}}

**Out of Scope:**
- {{OUT_OF_SCOPE_1}}
- {{OUT_OF_SCOPE_2}}

### Research Approach

1. {{APPROACH_STEP_1}}
2. {{APPROACH_STEP_2}}
3. {{APPROACH_STEP_3}}

---

## Findings

<!-- INV-SP02: Document findings when DONE -->

### Summary

{{FINDINGS_SUMMARY}}

### Detailed Findings

#### {{FINDING_1_TITLE}}

{{FINDING_1_DETAILS}}

#### {{FINDING_2_TITLE}}

{{FINDING_2_DETAILS}}

### Evidence/References

- {{REFERENCE_1}}
- {{REFERENCE_2}}
- {{REFERENCE_3}}

### Proof of Concept (if applicable)

{{POC_DESCRIPTION}}

**Location:** {{POC_LOCATION}}

---

## Recommendation

<!-- Recommended next steps based on findings -->

### Decision

{{DECISION}}

### Recommended Actions

1. {{ACTION_1}}
2. {{ACTION_2}}
3. {{ACTION_3}}

### Follow-up Work Items

<!-- Work items that should be created based on spike findings -->

| Type    | Title                        | Priority |
|---------|------------------------------|----------|
| {{TYPE}}| {{FOLLOW_UP_TITLE}}          | {{PRIO}} |

### Risks/Considerations

- {{RISK_1}}
- {{RISK_2}}

---

## Related Items

- Parent: [{{PARENT_TITLE}}]({{PARENT_LINK}})
- Related Feature: [{{RELATED_FEATURE}}]({{RELATED_FEATURE_LINK}})
- Follow-up Story: [{{FOLLOW_UP_STORY}}]({{FOLLOW_UP_STORY_LINK}})

---

## History

| Date       | Status       | Notes                          |
|------------|--------------|--------------------------------|
| {{DATE}}   | Created      | Spike defined                  |
| {{DATE}}   | IN_PROGRESS  | Research started               |
| {{DATE}}   | DONE         | Research complete              |

---

## Compaction Resilience (T-004)

| Constraint | Failure Mode if Lost | Compensating Control | Detection |
|-----------|---------------------|---------------------|-----------|
| INV-SP01: timebox is REQUIRED (1-336 hours) | Spike created without timebox, research runs unbounded | L3 AST validation (H-33) | `jerry ast validate` rejects missing timebox |
| INV-SP03: Spike cannot have children | Tasks created under Spike | /worktracker skill enforcement (WTI rules) | Worktracker audit detects children under Spike |
| INV-SP04: Spike does NOT require quality gates | Quality gates incorrectly applied to Spike | Template body states exception | Manual review |
| INV-SP02: findings documented when DONE | Spike closed without documenting findings | /worktracker skill enforcement | Manual review at completion |

<!--
JERRY ALIGNMENT:
  existing_type: "WorkType.SPIKE"
  existing_property: "requires_quality_gates = False"
  changes_needed: "None - already exists with correct semantics"

DESIGN RATIONALE:
  Spike modeled as first-class entity because it has distinct
  behavior: no quality gates required. SAFe formalizes this;
  other systems use labeling conventions.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.1 (Spike row)
-->
