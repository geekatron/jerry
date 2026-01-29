# EN-014: Domain Context Files Implementation

<!--
TEMPLATE: Enabler
VERSION: 2.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
CREATED: 2026-01-26 per FEAT-002 restructuring
NOTE: Creates actual contexts/*.yaml domain schema files per SPEC-context-injection.md Section 3.3
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-01-26T17:00:00Z
> **Due:** TBD
> **Completed:**
> **Parent:** FEAT-002
> **Owner:** Claude
> **Target Sprint:** Sprint 4
> **Effort Points:** 5
> **Gate:** GATE-5 (Core Implementation Review)

---

## Summary

Create the **domain context YAML files** that provide domain-specific knowledge to transcript analysis agents. These files define entity types, extraction rules, and prompt guidance for different transcript domains (general, meeting, interview, etc.).

**Implements:** [SPEC-context-injection.md Section 3.3](../../FEAT-001-analysis-design/EN-006-context-injection-design/docs/specs/SPEC-context-injection.md#33-contextsyaml-domain-files)

**Scope Expansion (2026-01-28):** Per [DISC-005](../FEAT-002--DISC-005-en006-artifact-promotion-gap.md), this enabler now includes promoting the 6 domain specifications from EN-006 TASK-038. Original scope was 3 domains (general, transcript, meeting); expanded scope adds 6 more domains from EN-006 design phase (software-engineering, software-architecture, product-management, user-experience, cloud-engineering, security-engineering).

**Technical Justification:**
- Domain schemas enable agent specialization without code changes
- YAML configuration separates domain knowledge from agent logic
- Extraction rules provide per-domain confidence thresholds
- Prompt guidance gives expert knowledge to agents

---

## Design Reference (L0/L1/L2)

### L0: The Recipe Book Analogy

Domain context files are like **specialized recipe books** for different cuisines:

```
THE RECIPE BOOK ANALOGY (Domain Context Files)
==============================================

SAME CHEF (ts-extractor)          DIFFERENT RECIPE BOOKS

                                  ┌────────────────────────────┐
    ┌───────────────┐             │  GENERAL COOKBOOK          │
    │               │             │  ────────────────          │
    │    CHEF       │             │  - Basic ingredients       │
    │    (Agent)    │◄──── uses ──│  - Standard techniques     │
    │               │             │  - Generic recipes         │
    │   "I can      │             └────────────────────────────┘
    │    cook any   │
    │    cuisine"   │             ┌────────────────────────────┐
    │               │             │  MEETING COOKBOOK          │
    │               │◄──── uses ──│  ────────────────          │
    │               │             │  - Action items = tasks    │
    │               │             │  - Decisions = agreements  │
    └───────────────┘             │  - Questions = open items  │
                                  └────────────────────────────┘

                                  ┌────────────────────────────┐
                                  │  INTERVIEW COOKBOOK        │
                        ◄──── uses──│  ────────────────          │
                                  │  - Q&A pairs = exchanges   │
                                  │  - Skills = qualifications │
                                  │  - Red flags = concerns    │
                                  └────────────────────────────┘

    "I use the recipe book that matches what I'm cooking."
```

### L1: Domain Schema Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Domain Context Files Architecture                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  skills/transcript/contexts/                                                 │
│  ├── general.yaml          ← Default domain (no specialized entities)       │
│  ├── transcript.yaml       ← Core transcript entities (action, decision)    │
│  ├── meeting.yaml          ← Meeting-specific extensions                    │
│  └── interview.yaml        ← Interview-specific extensions                  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                        DOMAIN SCHEMA STRUCTURE                        │   │
│  │ ────────────────────────────────────────────────────────────────────│   │
│  │                                                                       │   │
│  │  schema_version: "1.0.0"                                              │   │
│  │  domain: "meeting"                                                    │   │
│  │  display_name: "Meeting Transcript Analysis"                          │   │
│  │  extends: "transcript"    ← Inheritance from base domain              │   │
│  │                                                                       │   │
│  │  entity_definitions:      ← What to extract                           │   │
│  │    attendee:              ← Meeting-specific entity                   │   │
│  │      description: "Person present in meeting"                         │   │
│  │      attributes:                                                      │   │
│  │        - name: "name"                                                 │   │
│  │          type: "string"                                               │   │
│  │        - name: "role"                                                 │   │
│  │          type: "enum"                                                 │   │
│  │          values: ["organizer", "presenter", "participant"]            │   │
│  │                                                                       │   │
│  │  extraction_rules:        ← How to find entities                      │   │
│  │    - id: "attendees"                                                  │   │
│  │      entity_type: "attendee"                                          │   │
│  │      confidence_threshold: 0.85                                       │   │
│  │      priority: 1                                                      │   │
│  │                                                                       │   │
│  │  prompt_guidance: |       ← Expert knowledge for agent                │   │
│  │    When analyzing meeting transcripts:                                │   │
│  │    1. Identify all attendees from introductions...                    │   │
│  │                                                                       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### L2: Strategic Considerations

- **Domain Inheritance:** Extended domains can inherit from base domains (meeting extends transcript)
- **Entity Reuse:** Common entities (action_item, decision) defined once in transcript.yaml
- **Confidence Tuning:** Per-domain confidence thresholds optimize precision/recall tradeoffs
- **Prompt Guidance:** Domain experts encode knowledge in prompt_guidance field
- **Validation:** All schemas validated against JSON Schema before use (REQ-CI-F-009)

---

## Benefit Hypothesis

**We believe that** creating specialized domain context files per SPEC Section 3.3

**Will result in** improved extraction accuracy for different transcript types

**We will know we have succeeded when:**
- general.yaml provides baseline extraction for any transcript
- transcript.yaml covers core action/decision/question extraction
- meeting.yaml adds meeting-specific entities (attendees, agenda)
- All schemas validate against JSON Schema
- Human approval received at GATE-5

---

## Acceptance Criteria

### Definition of Done

- [ ] general.yaml created with minimal entity set
- [ ] transcript.yaml created with core entities (REQ-CI-F-001)
- [ ] meeting.yaml created with meeting extensions
- [ ] All schemas pass JSON Schema validation (REQ-CI-F-009)
- [ ] prompt_guidance provides domain-specific expert knowledge
- [ ] Integration with EN-013 context injection verified
- [ ] ps-critic review passed
- [ ] Human approval at GATE-5

### Technical Criteria (from SPEC-context-injection.md Section 3.3)

| # | Criterion | SPEC Section | Verified |
|---|-----------|--------------|----------|
| AC-1 | Each schema has schema_version field | 3.3.2 | [ ] |
| AC-2 | Each schema has domain identifier | 3.3.2 | [ ] |
| AC-3 | entity_definitions has at least 1 entity | 2.3 | [ ] |
| AC-4 | extraction_rules has at least 1 rule | 2.3 | [ ] |
| AC-5 | Confidence thresholds in 0.0-1.0 range | 2.3 | [ ] |
| AC-6 | Extraction rule IDs are unique | 2.3 | [ ] |
| AC-7 | prompt_guidance provides actionable guidance | 3.3.2 | [ ] |
| AC-8 | Schemas load correctly by SKILL.md | 3.1 | [ ] |

---

## Children (Tasks)

### Task Inventory - Original Scope (3 Domains)

| ID | Title | Status | Owner | Effort | Blocked By |
|----|-------|--------|-------|--------|------------|
| [TASK-126](./TASK-126-general-domain-schema.md) | Create general.yaml baseline domain schema | pending | Claude | 1 | EN-013 |
| [TASK-127](./TASK-127-transcript-domain-schema.md) | Create transcript.yaml core domain schema | pending | Claude | 2 | TASK-126 |
| [TASK-128](./TASK-128-meeting-domain-schema.md) | Create meeting.yaml extended domain schema | pending | Claude | 1 | TASK-127 |
| [TASK-129](./TASK-129-domain-json-schema.md) | Create JSON Schema validator for domain files | pending | Claude | 1 | TASK-126 |
| [TASK-130](./TASK-130-schema-validation.md) | Validate all schemas against JSON Schema | pending | Claude | 1 | TASK-129, TASK-128 |

### Task Inventory - EN-006 Artifact Promotion (6 Additional Domains)

> **Source:** [DISC-005](../FEAT-002--DISC-005-en006-artifact-promotion-gap.md) - EN-006 Context Injection Artifact Promotion Gap Analysis
>
> **Rationale:** EN-006 TASK-038 produced 34 files across 6 domain specifications during the design phase.
> These artifacts contain runtime-necessary entity definitions, extraction rules, and prompt guidance
> that must be transformed and promoted to the skill for self-containment.
>
> **Transformation:** EN-006 decomposed files (4 files per domain) → Consolidated YAML (1 file per domain)
> per SPEC-context-injection.md Section 3.3 design.

| ID | Title | Status | Owner | Effort | Blocked By |
|----|-------|--------|-------|--------|------------|
| [TASK-150](./TASK-150-software-engineering-domain.md) | Transform & create software-engineering.yaml | pending | Claude | 1 | TASK-129 |
| [TASK-151](./TASK-151-software-architecture-domain.md) | Transform & create software-architecture.yaml | pending | Claude | 1 | TASK-129 |
| [TASK-152](./TASK-152-product-management-domain.md) | Transform & create product-management.yaml | pending | Claude | 1 | TASK-129 |
| [TASK-153](./TASK-153-user-experience-domain.md) | Transform & create user-experience.yaml | pending | Claude | 1 | TASK-129 |
| [TASK-154](./TASK-154-cloud-engineering-domain.md) | Transform & create cloud-engineering.yaml | pending | Claude | 1 | TASK-129 |
| [TASK-155](./TASK-155-security-engineering-domain.md) | Transform & create security-engineering.yaml | pending | Claude | 1 | TASK-129 |
| [TASK-156](./TASK-156-domain-schema-promotion.md) | Promote DOMAIN-SCHEMA.json to skill schemas | pending | Claude | 0.5 | TASK-129 |
| [TASK-157](./TASK-157-spec-files-promotion.md) | Promote SPEC-*.md files to skill docs | pending | Claude | 1 | TASK-150..155 |
| [TASK-158](./TASK-158-skill-md-domain-update.md) | Update SKILL.md with 6 new domains | pending | Claude | 0.5 | TASK-150..155 |
| [TASK-159](./TASK-159-domain-load-validation.md) | Validation: All 8 domains load correctly | pending | Claude | 1 | TASK-158, TASK-130 |

**NOTE:** Task IDs start at TASK-126 to continue from EN-013 (TASK-120-125).
**Task files created:** 2026-01-26 with detailed acceptance criteria and evidence requirements.
**Scope expanded:** 2026-01-28 per DISC-005. Added TASK-150..159 for EN-006 artifact promotion.

### Task Inventory - Schema Extension Workflow (DISC-006)

> **Source:** [DISC-006](./EN-014--DISC-006-schema-gap-analysis.md) - Schema Gap Analysis: EN-006 Features vs domain-schema.json
>
> **Rationale:** EN-006 artifacts contain 4 feature categories (relationships, metadata, context_rules, validation) not supported by current domain-schema.json. These tasks research, analyze, and design schema V2 before domain YAML promotion.
>
> **Workflow:** [EN-014--WORKFLOW-schema-extension.md](./EN-014--WORKFLOW-schema-extension.md)
>
> **Quality Strategy:** Dual-reviewer (ps-critic + nse-qa) with Logical AND; ADR uses nse-reviewer; Final review elevated to 0.90 threshold.

| ID | Title | Status | Owner | Effort | Blocked By | Reviewers |
|----|-------|--------|-------|--------|------------|-----------|
| [TASK-164](./TASK-164-research-schema-extensibility.md) | Research: Schema Extensibility Patterns | BACKLOG | Claude | 2 | - | ps-critic + nse-qa |
| [TASK-165](./TASK-165-analysis-gap-impact.md) | Analysis: Gap Impact Assessment | BACKLOG | Claude | 2 | TASK-164 | ps-critic + nse-qa |
| [TASK-166](./TASK-166-adr-schema-extension.md) | ADR: Schema Extension Strategy | BACKLOG | Claude | 2 | TASK-164, 165 | ps-critic + nse-reviewer |
| [TASK-167](./TASK-167-tdd-schema-v2.md) | TDD: Schema V2 Design | BACKLOG | Claude | 3 | TASK-166 | ps-critic + nse-qa |
| [TASK-168](./TASK-168-final-adversarial-review.md) | Final Adversarial Review | BACKLOG | Claude | 2 | TASK-164..167 | TRIPLE (0.90) |
| [TASK-169](./TASK-169-human-gate.md) | GATE: Human Approval | BACKLOG | Human | 1 | TASK-168 | Human |

**NOTE:** TASK-150..159 (EN-006 Artifact Promotion) are BLOCKED by TASK-169 Human Approval Gate.
This ensures schema extension is complete before domain YAML creation begins.

### Task Inventory - TDD Minor Issue Fixes (ps-critic + nse-qa Findings)

> **Source:** [DISC-007](./EN-014--DISC-007-tdd-validation-implementation-gap.md) - TDD Validation Implementation Gap
>
> **Rationale:** TASK-167 dual-reviewer quality reviews (ps-critic 0.93, nse-qa 0.91) identified 5 minor issues
> that must be addressed before TDD adversarial review (TASK-170). These are documentation improvements,
> not architectural changes.
>
> **Execution Order:** TASK-171..175 (parallel) → TASK-170 (TDD Adversarial Review) → TASK-168 (Final Review)

| ID | Title | Status | Owner | Effort | Blocked By | Source |
|----|-------|--------|-------|--------|------------|--------|
| [TASK-170](./TASK-170-tdd-adversarial-review.md) | TDD Adversarial Review (nse-reviewer) | BACKLOG | Claude | 2 | TASK-171..175 | User request |
| [TASK-171](./TASK-171-containment-cardinality-docs.md) | Add containment cardinality documentation | BACKLOG | Claude | 1 | - | ps-critic MINOR-001 |
| [TASK-172](./TASK-172-section-numbering-fix.md) | Fix section numbering inconsistency | BACKLOG | Claude | 1 | - | ps-critic MINOR-002 |
| [TASK-173](./TASK-173-semantic-validator-reference.md) | Add semantic validator implementation reference | BACKLOG | Claude | 2 | - | ps-critic MINOR-003, DISC-007 |
| [TASK-174](./TASK-174-performance-benchmarks.md) | Replace performance estimates with benchmarks | BACKLOG | Claude | 1 | - | nse-qa NC-m-001 |
| [TASK-175](./TASK-175-sv006-implementation-details.md) | Add SV-006 circular detection implementation details | BACKLOG | Claude | 2 | - | nse-qa NC-m-002, DISC-007 |

**Quality Gate:** TASK-170 targets **nse-reviewer score ≥ 0.95** (elevated from ADR's 0.93). If < 0.85 after 2 iterations, escalate to user.

### Effort Summary

| Scope | Tasks | Story Points |
|-------|-------|--------------|
| Original (3 domains) | TASK-126..130 | 6 |
| Schema Extension | TASK-164..169 | 12 |
| TDD Minor Issue Fixes | TASK-170..175 | 9 |
| EN-006 Promotion (6 domains) | TASK-150..159 | 9 |
| **Total** | **27 tasks** | **36 SP** |

---

## Domain Schema Specifications

### 1. general.yaml - Baseline Domain

**Purpose:** Minimal entity extraction when no domain specified.

```yaml
# contexts/general.yaml
# Baseline domain schema for general transcript analysis
# Implements: REQ-CI-F-001

schema_version: "1.0.0"
domain: "general"
display_name: "General Transcript Analysis"

entity_definitions:
  statement:
    description: "General statement or assertion"
    attributes:
      - name: "text"
        type: "string"
        required: true
      - name: "speaker"
        type: "string"
      - name: "timestamp_ms"
        type: "integer"

  reference:
    description: "Reference to external entity (person, document, etc.)"
    attributes:
      - name: "text"
        type: "string"
        required: true
      - name: "reference_type"
        type: "enum"
        values: ["person", "document", "organization", "other"]

extraction_rules:
  - id: "statements"
    entity_type: "statement"
    confidence_threshold: 0.5
    priority: 1
  - id: "references"
    entity_type: "reference"
    confidence_threshold: 0.6
    priority: 2

prompt_guidance: |
  When analyzing general transcripts:

  1. Extract significant statements that convey information
  2. Identify references to external entities
  3. Use low confidence thresholds - this is the baseline

  This is the fallback domain when no specific domain matches.
```

### 2. transcript.yaml - Core Domain

**Purpose:** Core transcript entities used across all domains.

```yaml
# contexts/transcript.yaml
# Core domain schema for transcript analysis
# Implements: REQ-CI-F-001, REQ-CI-F-007, PAT-001

schema_version: "1.0.0"
domain: "transcript"
display_name: "Transcript Analysis"

entity_definitions:
  action_item:
    description: "Task or commitment made during conversation"
    attributes:
      - name: "text"
        type: "string"
        required: true
      - name: "assignee"
        type: "string"
      - name: "due_date"
        type: "date"
      - name: "confidence"
        type: "float"
    extraction_patterns:
      - "{{assignee}} will {{text}}"
      - "{{assignee}}, can you {{text}}"
      - "action item: {{text}}"
      - "TODO: {{text}}"

  decision:
    description: "Decision made during conversation"
    attributes:
      - name: "text"
        type: "string"
        required: true
      - name: "decided_by"
        type: "string"
      - name: "rationale"
        type: "string"
    extraction_patterns:
      - "we've decided to {{text}}"
      - "the decision is {{text}}"
      - "let's go with {{text}}"
      - "agreed: {{text}}"

  question:
    description: "Question raised during conversation"
    attributes:
      - name: "text"
        type: "string"
        required: true
      - name: "asked_by"
        type: "string"
      - name: "answered"
        type: "boolean"
        default: false

  speaker:
    description: "Person speaking in the transcript"
    attributes:
      - name: "name"
        type: "string"
        required: true
      - name: "role"
        type: "string"
      - name: "segment_count"
        type: "integer"
      - name: "speaking_time_ms"
        type: "integer"

  topic:
    description: "Topic or subject discussed"
    attributes:
      - name: "title"
        type: "string"
        required: true
      - name: "start_ms"
        type: "integer"
      - name: "end_ms"
        type: "integer"
      - name: "segment_ids"
        type: "array"
        items: "string"

extraction_rules:
  - id: "action_items"
    entity_type: "action_item"
    confidence_threshold: 0.7
    priority: 1
    tier: "rule"  # PAT-001: Try rule patterns first

  - id: "decisions"
    entity_type: "decision"
    confidence_threshold: 0.8
    priority: 2
    tier: "rule"

  - id: "questions"
    entity_type: "question"
    confidence_threshold: 0.75
    priority: 3
    tier: "ml"  # PAT-001: Use ML patterns

  - id: "speakers"
    entity_type: "speaker"
    confidence_threshold: 0.9
    priority: 4
    tier: "rule"  # PAT-003: Speaker detection

  - id: "topics"
    entity_type: "topic"
    confidence_threshold: 0.7
    priority: 5
    tier: "llm"  # PAT-001: LLM inference for topics

prompt_guidance: |
  When analyzing transcripts for entity extraction:

  ## Action Items (FR-006)
  Look for commitments with specific owners and deadlines.
  - Phrases: "will do", "by Friday", "I'll handle", "assigned to"
  - Must have: text describing action, optional assignee and due date
  - Cite source segment for anti-hallucination (PAT-004)

  ## Decisions (FR-007)
  Identify explicit decisions with consensus language.
  - Phrases: "we've decided", "let's go with", "agreed", "final answer"
  - Include rationale when provided
  - Higher confidence threshold (0.8) to reduce false positives

  ## Questions (FR-008)
  Track open questions and whether they were answered.
  - Mark as answered if response follows within transcript
  - Track who asked for attribution

  ## Speakers (FR-005)
  Apply 4-pattern detection chain (PAT-003):
  1. VTT voice tags: <v Speaker>
  2. Prefix pattern: "Speaker Name:"
  3. Bracket pattern: "[Speaker Name]"
  4. Contextual resolution (fallback)

  ## Topics (FR-009)
  Segment by topic changes using boundary detection:
  - Time gaps > 5 minutes
  - Explicit transitions: "moving on", "next topic"
  - Semantic shifts in discussion

  ## Confidence Scoring (NFR-008)
  - 0.9+: Explicit indicator present ("action item:", "decision:")
  - 0.7-0.9: Strong implicit signal with context
  - 0.5-0.7: Ambiguous, flag for human review
  - <0.5: Do not extract
```

### 3. meeting.yaml - Meeting Extension

**Purpose:** Meeting-specific entities extending transcript.yaml.

```yaml
# contexts/meeting.yaml
# Meeting-specific domain schema
# Implements: REQ-CI-F-001

schema_version: "1.0.0"
domain: "meeting"
display_name: "Meeting Transcript Analysis"
extends: "transcript"  # Inherits all transcript entities

entity_definitions:
  # Inherits: action_item, decision, question, speaker, topic

  attendee:
    description: "Person present in the meeting"
    attributes:
      - name: "name"
        type: "string"
        required: true
      - name: "role"
        type: "enum"
        values: ["organizer", "presenter", "participant", "guest"]
      - name: "department"
        type: "string"
      - name: "present_from_ms"
        type: "integer"
      - name: "present_to_ms"
        type: "integer"

  agenda_item:
    description: "Item from meeting agenda"
    attributes:
      - name: "title"
        type: "string"
        required: true
      - name: "presenter"
        type: "string"
      - name: "allocated_time_min"
        type: "integer"
      - name: "actual_time_min"
        type: "integer"
      - name: "status"
        type: "enum"
        values: ["covered", "deferred", "skipped"]

  follow_up:
    description: "Post-meeting follow-up item"
    attributes:
      - name: "text"
        type: "string"
        required: true
      - name: "owner"
        type: "string"
      - name: "target_meeting"
        type: "string"
      - name: "priority"
        type: "enum"
        values: ["high", "medium", "low"]

extraction_rules:
  # Inherits: action_items, decisions, questions, speakers, topics

  - id: "attendees"
    entity_type: "attendee"
    confidence_threshold: 0.85
    priority: 0  # Highest priority for meetings
    tier: "rule"

  - id: "agenda_items"
    entity_type: "agenda_item"
    confidence_threshold: 0.75
    priority: 6
    tier: "llm"

  - id: "follow_ups"
    entity_type: "follow_up"
    confidence_threshold: 0.7
    priority: 7
    tier: "ml"

prompt_guidance: |
  When analyzing meeting transcripts:

  ## Attendees
  Identify all meeting participants from:
  - Roll call or introductions
  - Speaker labels in transcript
  - References to "everyone", "all present"
  Track when people join/leave ("X had to drop off")

  ## Agenda Items
  Recognize meeting structure:
  - Explicit agenda references: "Item 3 is..."
  - Topic transitions: "Moving to the next item"
  - Time checks: "We have 10 minutes left for this"

  ## Follow-ups
  Distinct from action items - specifically for future meetings:
  - "Let's revisit this next time"
  - "We'll need to discuss with absent parties"
  - "Parking lot" items

  This schema extends transcript.yaml, so all base extraction
  rules and entities are also available.
```

---

## Entity Inheritance Model

```
DOMAIN INHERITANCE HIERARCHY
============================

general.yaml                    ← Baseline (no specialized entities)
     │
     │ does NOT inherit
     ▼
transcript.yaml                 ← Core entities (action, decision, question)
     │
     │ extends
     ├─────────────────┐
     ▼                 ▼
meeting.yaml      interview.yaml
(+ attendee)      (+ qa_pair)
(+ agenda_item)   (+ qualification)
(+ follow_up)     (+ concern)

MERGE BEHAVIOR:
──────────────
When domain="meeting":
  1. Load meeting.yaml
  2. See extends="transcript"
  3. Load transcript.yaml
  4. Merge (meeting overrides transcript if conflict)
```

---

## File Location

### Target Skill Structure After EN-014 Completion

```
skills/transcript/
├── SKILL.md                          ← TASK-158: Updated with 8 domains
├── agents/
│   ├── ts-parser.md
│   ├── ts-extractor.md
│   └── ts-formatter.md
├── contexts/                         ← Domain schema files (this enabler)
│   ├── general.yaml                  ← TASK-126 (Original)
│   ├── transcript.yaml               ← TASK-127 (Original)
│   ├── meeting.yaml                  ← TASK-128 (Original)
│   ├── software-engineering.yaml     ← TASK-150 (EN-006 Promotion)
│   ├── software-architecture.yaml    ← TASK-151 (EN-006 Promotion)
│   ├── product-management.yaml       ← TASK-152 (EN-006 Promotion)
│   ├── user-experience.yaml          ← TASK-153 (EN-006 Promotion)
│   ├── cloud-engineering.yaml        ← TASK-154 (EN-006 Promotion)
│   └── security-engineering.yaml     ← TASK-155 (EN-006 Promotion)
├── schemas/
│   ├── domain-schema.json            ← TASK-129 (Original)
│   └── DOMAIN-SCHEMA.json            ← TASK-156 (EN-006 Promotion - validation schema)
└── docs/
    ├── PLAYBOOK.md                   ← Existing
    ├── RUNBOOK.md                    ← Existing
    └── domains/                      ← TASK-157: NEW folder for domain documentation
        ├── SPEC-software-engineering.md
        ├── SPEC-software-architecture.md
        ├── SPEC-product-management.md
        ├── SPEC-user-experience.md
        ├── SPEC-cloud-engineering.md
        ├── SPEC-security-engineering.md
        └── DOMAIN-SELECTION-GUIDE.md ← From EN-006 README flowchart
```

### EN-006 Source Artifacts (for transformation)

```
EN-006/docs/specs/domain-contexts/
├── DOMAIN-SCHEMA.json              ← To: schemas/DOMAIN-SCHEMA.json (TASK-156)
├── README.md                       ← To: docs/domains/DOMAIN-SELECTION-GUIDE.md (TASK-157)
├── 01-software-engineering/
│   ├── SPEC-software-engineering.md   ← To: docs/domains/ (TASK-157)
│   ├── entities/entity-definitions.yaml  ─┐
│   ├── extraction/extraction-rules.yaml  ─┼→ contexts/software-engineering.yaml (TASK-150)
│   └── prompts/prompt-templates.md       ─┘
├── 02-software-architecture/          ← Same transform (TASK-151)
├── 03-product-management/             ← Same transform (TASK-152)
├── 04-user-experience/                ← Same transform (TASK-153)
├── 05-cloud-engineering/              ← Same transform (TASK-154)
└── 06-security-engineering/           ← Same transform (TASK-155)
```

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-002: Implementation](../FEAT-002-implementation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Implements | [SPEC-context-injection.md Section 3.3](../../FEAT-001-analysis-design/EN-006-context-injection-design/docs/specs/SPEC-context-injection.md) | Domain schema specification |
| Depends On | EN-013 | Context injection mechanism must be in place |
| Depends On | EN-008 | Entity extraction patterns inform domain schemas |
| References | TDD-ts-extractor.md | Entity schemas for extraction |
| References | ADR-002 | Token limits apply to combined context |
| Blocks | EN-015 | Validation needs domain schemas |

### Discovery Reference

- [DISC-001](../FEAT-002--DISC-001-enabler-alignment-analysis.md) - Alignment analysis
- [DISC-005](../FEAT-002--DISC-005-en006-artifact-promotion-gap.md) - EN-006 artifact promotion gap (scope expansion source)
- [DISC-006](./EN-014--DISC-006-schema-gap-analysis.md) - Schema gap analysis: EN-006 features vs domain-schema.json
- [DISC-007](./EN-014--DISC-007-tdd-validation-implementation-gap.md) - TDD validation implementation gap (triggers TASK-170-175)

### Workflow Reference

- [EN-014--WORKFLOW-schema-extension.md](./EN-014--WORKFLOW-schema-extension.md) - Schema extension workflow with dual-reviewer quality gates

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-26 | Claude | pending | Enabler created per FEAT-002 restructuring |
| 2026-01-28 | Claude | pending | **SCOPE EXPANDED** per DISC-005: Added TASK-150..159 to promote 6 EN-006 domain specifications. Original scope (3 domains, 5 tasks, 6 SP) expanded to 8 domains total (15 tasks, 15 SP). Human decisions: (1) SPEC files promoted as documentation, (2) Consolidated YAML per SPEC design, (3) Work blocked by EN-016 completion. |
| 2026-01-29 | Claude | pending | **SCHEMA EXTENSION WORKFLOW** per DISC-006: Created TASK-164..169 for schema gap analysis and V2 design. TASK-150..159 now BLOCKED by TASK-169 human approval gate. Added dual-reviewer (ps-critic + nse-qa) quality strategy. Total scope: 21 tasks, 27 SP. |
| 2026-01-29 | Claude | pending | **TDD IMPROVEMENTS** per DISC-007: Created TASK-170..175 to address ps-critic (3 MINOR) and nse-qa (2 NC-m) findings from TASK-167 quality reviews. TASK-170 adds nse-reviewer adversarial review of TDD (target 0.95). TASK-171..175 fix minor documentation issues (containment cardinality, section numbering, validator reference, performance benchmarks, SV-006 algorithm). Execution order: TASK-171..175 (parallel) → TASK-170 → TASK-168. Total scope: 27 tasks, 36 SP. |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Product Backlog Item (tagged Technical) |
| **SAFe** | Enabler Story |
| **JIRA** | Task |
