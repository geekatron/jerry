# TASK-038: Domain Context Specifications

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 2.0.0
UPDATED: 2026-01-26 - Changed from 4 generic domains to 6 transcript analysis domains
-->

---

## Frontmatter

```yaml
# === IDENTITY (Auto-generated, Immutable) ===
id: "TASK-038"
work_type: TASK

# === CORE METADATA ===
title: "Domain Context Specifications"
description: |
  Phase 3: Create specifications/designs for 6 domain-specific context injection
  configurations targeting transcript analysis use cases. These specifications define
  entities, extraction rules, and prompt templates for each domain.

  **SCOPE:** Design artifacts only. Implementation (actual context files, test
  transcripts, validation) deferred to FEAT-002.

  **DOMAINS:**
  1. Software Engineering (standups, sprint planning, code reviews)
  2. Software Architecture (architecture review meetings, ADR discussions)
  3. Product Management (product strategy, roadmap planning)
  4. User Experience (UX research interviews, usability testing)
  5. Cloud Engineering (incident post-mortems, capacity planning)
  6. Security Engineering (security audits, threat modeling)

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: COMPLETE
resolution: DONE

# === PRIORITY ===
priority: HIGH  # All 6 domains equal priority

# === PEOPLE ===
assignee: "ps-architect + ps-validator + nse-verification"
created_by: "Claude"

# === TIMESTAMPS ===
created_at: "2026-01-26T16:00:00Z"
updated_at: "2026-01-27T00:30:00Z"

# === HIERARCHY ===
parent_id: "EN-006"

# === TAGS ===
tags:
  - "specifications"
  - "domain-context"
  - "transcript-analysis"
  - "phase-3"
  - "software-engineering"
  - "software-architecture"
  - "product-management"
  - "user-experience"
  - "cloud-engineering"
  - "security-engineering"

# === DELIVERY ITEM PROPERTIES ===
effort: 4  # Increased from 2 due to 6 domains
acceptance_criteria: |
  See Per-Domain Acceptance Criteria section below (6 sets)
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: SPECIFICATION
original_estimate: 6
remaining_work: 0
time_spent: 6

# === ORCHESTRATION ===
phase: 3
barrier: null
execution_mode: "PARALLEL_WITH_TASK_036_037"
ps_agent: "ps-architect"
validator: "ps-validator"
nse_agent: "nse-verification"
blocked_by: "BARRIER-2"

# === DOWNSTREAM IMPLEMENTATION ===
implementation_feature: "FEAT-002"
implementation_tasks_required:
  - "Create contexts/{domain}.yaml files for each domain"
  - "Provide test transcripts for each domain"
  - "Implement validation processes (manual review, schema, transcript testing)"
```

---

## Content

### Description

Create **specifications and designs** for 6 domain-specific context injection configurations targeting transcript analysis use cases. Each specification defines the entities, extraction rules, prompt templates, and expected outputs for analyzing transcripts from that domain.

> **IMPORTANT:** This task produces design artifacts only. The actual implementation
> (creating `contexts/{domain}.yaml` files, test transcripts, validation) is
> deferred to FEAT-002. See [DISC-001](./EN-006--DISC-001-feat002-implementation-scope.md).

### Target Domains

Each domain represents a professional persona whose meeting transcripts we analyze:

| # | Domain | Transcript Types | Key Use Cases |
|---|--------|------------------|---------------|
| 1 | **Software Engineering** | Standups, sprint planning, code reviews | Track commitments, blockers, decisions |
| 2 | **Software Architecture** | Architecture reviews, ADR discussions, design sessions | Extract decisions, rationale, alternatives |
| 3 | **Product Management** | Product strategy, roadmap planning, feature prioritization | Capture priorities, stakeholder needs, timelines |
| 4 | **User Experience** | UX research interviews, usability testing, design critiques | Extract user insights, pain points, recommendations |
| 5 | **Cloud Engineering** | Incident post-mortems, capacity planning, infrastructure reviews | Identify root causes, action items, metrics |
| 6 | **Security Engineering** | Security audits, threat modeling, compliance reviews | Extract vulnerabilities, mitigations, compliance gaps |

### Design vs Implementation Boundary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          FEAT-001: Analysis & Design                         │
│                                  (THIS TASK)                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ ✓ Entity definition schemas (WHAT entities to extract)                       │
│ ✓ Extraction rule patterns (WHAT patterns to look for)                       │
│ ✓ Prompt template designs (HOW to instruct the agents)                       │
│ ✓ Expected output formats (WHAT the output should look like)                 │
│ ✓ Validation criteria per domain (HOW to verify correctness)                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FEAT-002: Implementation                           │
│                             (DEFERRED - See DISC-004)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ ○ Actual contexts/{domain}.yaml files                                        │
│ ○ Test transcripts for each domain (user has transcripts)                    │
│ ○ Validation execution (manual review + schema + transcript testing)         │
│ ○ Integration with Claude Code Skills                                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Specification Directory Structure

```
docs/specs/domain-contexts/
├── README.md                              # Overview and domain selection guide
├── DOMAIN-SCHEMA.json                     # JSON Schema for domain specifications
│
├── 01-software-engineering/
│   ├── SPEC-software-engineering.md       # Domain specification document
│   ├── entities/
│   │   └── entity-definitions.yaml        # Entity schema (design)
│   ├── extraction/
│   │   └── extraction-rules.yaml          # Extraction patterns (design)
│   ├── prompts/
│   │   └── prompt-templates.md            # Prompt designs
│   └── validation/
│       └── acceptance-criteria.md         # Domain-specific validation
│
├── 02-software-architecture/
│   ├── SPEC-software-architecture.md
│   ├── entities/
│   │   └── entity-definitions.yaml
│   ├── extraction/
│   │   └── extraction-rules.yaml
│   ├── prompts/
│   │   └── prompt-templates.md
│   └── validation/
│       └── acceptance-criteria.md
│
├── 03-product-management/
│   ├── SPEC-product-management.md
│   ├── entities/
│   │   └── entity-definitions.yaml
│   ├── extraction/
│   │   └── extraction-rules.yaml
│   ├── prompts/
│   │   └── prompt-templates.md
│   └── validation/
│       └── acceptance-criteria.md
│
├── 04-user-experience/
│   ├── SPEC-user-experience.md
│   ├── entities/
│   │   └── entity-definitions.yaml
│   ├── extraction/
│   │   └── extraction-rules.yaml
│   ├── prompts/
│   │   └── prompt-templates.md
│   └── validation/
│       └── acceptance-criteria.md
│
├── 05-cloud-engineering/
│   ├── SPEC-cloud-engineering.md
│   ├── entities/
│   │   └── entity-definitions.yaml
│   ├── extraction/
│   │   └── extraction-rules.yaml
│   ├── prompts/
│   │   └── prompt-templates.md
│   └── validation/
│       └── acceptance-criteria.md
│
└── 06-security-engineering/
    ├── SPEC-security-engineering.md
    ├── entities/
    │   └── entity-definitions.yaml
    ├── extraction/
    │   └── extraction-rules.yaml
    ├── prompts/
    │   └── prompt-templates.md
    └── validation/
        └── acceptance-criteria.md
```

---

## Domain 1: Software Engineering

### Overview

**Target Users:** Software Engineers, Tech Leads, Engineering Managers
**Transcript Types:** Daily standups, sprint planning, sprint retrospectives, code review sessions, pair programming sessions

### Entity Definitions (Design)

```yaml
# Design specification - actual implementation in FEAT-002
domain: software-engineering
version: "1.0.0"

entities:
  commitment:
    description: "Work item a team member commits to complete"
    attributes:
      - assignee: "Person making the commitment"
      - work_item: "Description of the work"
      - sprint: "Sprint or time period"
      - confidence: "high | medium | low"

  blocker:
    description: "Impediment preventing progress"
    attributes:
      - reporter: "Person reporting the blocker"
      - description: "What is blocked"
      - dependency: "What/who is blocking"
      - severity: "critical | major | minor"

  decision:
    description: "Technical or process decision made"
    attributes:
      - topic: "What was decided"
      - outcome: "The decision made"
      - rationale: "Why this decision"
      - participants: "Who was involved"

  action_item:
    description: "Follow-up task assigned"
    attributes:
      - owner: "Person responsible"
      - task: "Description of action"
      - due_date: "When it's due"
      - context: "Related discussion"

  risk:
    description: "Identified technical or schedule risk"
    attributes:
      - description: "Risk description"
      - likelihood: "high | medium | low"
      - impact: "high | medium | low"
      - mitigation: "Proposed mitigation"
```

### Extraction Rules (Design)

```yaml
# Design specification - actual implementation in FEAT-002
extraction_rules:
  commitment_patterns:
    - pattern: "I will {work_item}"
    - pattern: "I'm going to {work_item}"
    - pattern: "I'll take {work_item}"
    - pattern: "I'm picking up {work_item}"

  blocker_patterns:
    - pattern: "I'm blocked on {dependency}"
    - pattern: "Waiting for {dependency}"
    - pattern: "Can't proceed until {dependency}"
    - pattern: "Dependency on {dependency}"

  decision_patterns:
    - pattern: "We decided to {outcome}"
    - pattern: "The decision is {outcome}"
    - pattern: "Going forward, we will {outcome}"
    - pattern: "Consensus is {outcome}"
```

### Prompt Templates (Design)

```markdown
## Software Engineering Transcript Analysis

You are analyzing a {{$transcript_type}} transcript from a software engineering team.

### Context
- Team: {{$team_name}}
- Sprint: {{$sprint_number}}
- Date: {{$meeting_date}}

### Extraction Instructions

1. **Commitments**: Identify all work items team members commit to
   - Extract: assignee, work_item, confidence level
   - Look for phrases: "I will", "I'm going to", "I'll take"

2. **Blockers**: Find any impediments or dependencies
   - Extract: reporter, description, blocking dependency, severity
   - Look for phrases: "blocked on", "waiting for", "can't proceed"

3. **Decisions**: Capture all decisions made
   - Extract: topic, outcome, rationale, participants
   - Look for phrases: "we decided", "the decision is", "consensus"

4. **Action Items**: List follow-up tasks
   - Extract: owner, task description, due date if mentioned
   - Look for: assignments, "TODO", "action item"

### Output Format
{{$output_schema}}
```

### Per-Domain Acceptance Criteria: Software Engineering

| ID | Criterion | Verification Method |
|----|-----------|---------------------|
| **SE-AC-001** | Entity definitions cover: commitment, blocker, decision, action_item, risk | Schema validation |
| **SE-AC-002** | Each entity has ≥3 meaningful attributes | Manual review |
| **SE-AC-003** | Extraction rules include ≥4 patterns per entity type | Pattern count |
| **SE-AC-004** | Patterns cover common standup/planning terminology | Domain expert review |
| **SE-AC-005** | Prompt template includes all {{$variable}} placeholders | Template validation |
| **SE-AC-006** | Prompt template provides clear extraction instructions | Manual review |
| **SE-AC-007** | Output format aligns with SPEC-context-injection.md schema | Schema validation |
| **SE-AC-008** | Validation criteria defined for transcript testing | Checklist review |

---

## Domain 2: Software Architecture

### Overview

**Target Users:** Software Architects, Principal Engineers, Tech Leads
**Transcript Types:** Architecture review meetings, ADR discussion sessions, design reviews, technical deep-dives

### Entity Definitions (Design)

```yaml
# Design specification - actual implementation in FEAT-002
domain: software-architecture
version: "1.0.0"

entities:
  architectural_decision:
    description: "A significant architectural choice"
    attributes:
      - title: "Decision title/summary"
      - context: "Why this decision is needed"
      - decision: "What was decided"
      - consequences: "Impact of the decision"
      - status: "proposed | accepted | deprecated | superseded"

  alternative:
    description: "Option considered but not chosen"
    attributes:
      - title: "Alternative name"
      - description: "What was the alternative"
      - pros: "Benefits of this option"
      - cons: "Drawbacks of this option"
      - rejection_reason: "Why not chosen"

  quality_attribute:
    description: "Non-functional requirement discussed"
    attributes:
      - attribute: "scalability | security | maintainability | performance | etc."
      - requirement: "Specific requirement"
      - priority: "high | medium | low"
      - trade_offs: "Related trade-offs"

  component:
    description: "System component discussed"
    attributes:
      - name: "Component name"
      - responsibility: "What it does"
      - interfaces: "How it connects"
      - constraints: "Limitations"

  technical_debt:
    description: "Identified technical debt or concern"
    attributes:
      - description: "What is the debt"
      - impact: "How it affects the system"
      - remediation: "Proposed fix"
      - priority: "high | medium | low"
```

### Extraction Rules (Design)

```yaml
# Design specification - actual implementation in FEAT-002
extraction_rules:
  decision_patterns:
    - pattern: "We're going with {decision}"
    - pattern: "The architecture decision is {decision}"
    - pattern: "ADR: {decision}"
    - pattern: "We chose {decision} because {rationale}"

  alternative_patterns:
    - pattern: "We considered {alternative}"
    - pattern: "Another option was {alternative}"
    - pattern: "We rejected {alternative} because {reason}"
    - pattern: "Alternative: {alternative}"

  quality_attribute_patterns:
    - pattern: "For {attribute}, we need {requirement}"
    - pattern: "{attribute} is critical because {reason}"
    - pattern: "We're prioritizing {attribute} over {other}"
```

### Prompt Templates (Design)

```markdown
## Software Architecture Transcript Analysis

You are analyzing a {{$transcript_type}} transcript from an architecture discussion.

### Context
- System: {{$system_name}}
- ADR Number: {{$adr_number}} (if applicable)
- Date: {{$meeting_date}}

### Extraction Instructions

1. **Architectural Decisions**: Capture key decisions made
   - Extract: title, context, decision, consequences, status
   - Look for: "we decided", "the architecture is", "ADR"

2. **Alternatives Considered**: Document rejected options
   - Extract: title, description, pros, cons, rejection reason
   - Look for: "we considered", "another option", "we rejected"

3. **Quality Attributes**: Identify NFR discussions
   - Extract: attribute, requirement, priority, trade-offs
   - Look for: scalability, security, performance, maintainability

4. **Components**: Note system components discussed
   - Extract: name, responsibility, interfaces, constraints

5. **Technical Debt**: Flag any tech debt identified
   - Extract: description, impact, remediation, priority

### Output Format
{{$output_schema}}
```

### Per-Domain Acceptance Criteria: Software Architecture

| ID | Criterion | Verification Method |
|----|-----------|---------------------|
| **SA-AC-001** | Entity definitions cover: architectural_decision, alternative, quality_attribute, component, technical_debt | Schema validation |
| **SA-AC-002** | Each entity has ≥4 meaningful attributes | Manual review |
| **SA-AC-003** | Extraction rules align with ADR terminology (Nygard format) | Domain expert review |
| **SA-AC-004** | Patterns capture decision rationale and alternatives | Pattern analysis |
| **SA-AC-005** | Prompt template supports ADR generation workflow | Workflow review |
| **SA-AC-006** | Quality attributes list covers ISO 25010 categories | Standard compliance |
| **SA-AC-007** | Output format supports downstream ADR document generation | Schema validation |
| **SA-AC-008** | Validation criteria test against architecture review transcripts | Checklist review |

---

## Domain 3: Product Management

### Overview

**Target Users:** Product Managers, Product Owners, Business Analysts
**Transcript Types:** Product strategy sessions, roadmap planning, feature prioritization, stakeholder interviews

### Entity Definitions (Design)

```yaml
# Design specification - actual implementation in FEAT-002
domain: product-management
version: "1.0.0"

entities:
  feature_request:
    description: "Requested product capability"
    attributes:
      - title: "Feature name"
      - description: "What it does"
      - requester: "Who requested"
      - business_value: "Why it's valuable"
      - priority: "P0 | P1 | P2 | P3"

  user_need:
    description: "Identified user requirement"
    attributes:
      - persona: "User type"
      - need: "What they need"
      - pain_point: "Current problem"
      - frequency: "How often encountered"

  roadmap_item:
    description: "Planned product work"
    attributes:
      - title: "Item name"
      - quarter: "Target quarter"
      - dependencies: "What it depends on"
      - success_metric: "How to measure success"

  stakeholder_feedback:
    description: "Input from stakeholders"
    attributes:
      - stakeholder: "Who provided feedback"
      - topic: "What about"
      - sentiment: "positive | neutral | negative"
      - key_points: "Main points"

  competitive_insight:
    description: "Competitive intelligence discussed"
    attributes:
      - competitor: "Which competitor"
      - feature: "What they have/do"
      - our_position: "How we compare"
      - action: "Suggested response"
```

### Extraction Rules (Design)

```yaml
# Design specification - actual implementation in FEAT-002
extraction_rules:
  feature_patterns:
    - pattern: "We need {feature} to {benefit}"
    - pattern: "Customers are asking for {feature}"
    - pattern: "Feature request: {feature}"
    - pattern: "{requester} wants {feature}"

  priority_patterns:
    - pattern: "This is P0|P1|P2|P3"
    - pattern: "Priority: {level}"
    - pattern: "Must have for {milestone}"
    - pattern: "This is critical|important|nice-to-have"

  roadmap_patterns:
    - pattern: "Targeting Q{quarter} for {item}"
    - pattern: "On the roadmap for {timeframe}"
    - pattern: "Planning to ship {item} in {quarter}"
```

### Prompt Templates (Design)

```markdown
## Product Management Transcript Analysis

You are analyzing a {{$transcript_type}} transcript from a product planning session.

### Context
- Product: {{$product_name}}
- Planning Horizon: {{$planning_quarter}}
- Date: {{$meeting_date}}

### Extraction Instructions

1. **Feature Requests**: Capture requested capabilities
   - Extract: title, description, requester, business value, priority
   - Look for: "we need", "customers want", "feature request"

2. **User Needs**: Document identified requirements
   - Extract: persona, need, pain point, frequency
   - Look for: "users need", "pain point", "problem is"

3. **Roadmap Items**: Note planned work
   - Extract: title, target quarter, dependencies, success metric
   - Look for: "roadmap", "targeting Q", "planning to ship"

4. **Stakeholder Feedback**: Capture input
   - Extract: stakeholder, topic, sentiment, key points
   - Look for: direct quotes, feedback references

5. **Competitive Insights**: Note competitor discussion
   - Extract: competitor, feature, our position, suggested action

### Output Format
{{$output_schema}}
```

### Per-Domain Acceptance Criteria: Product Management

| ID | Criterion | Verification Method |
|----|-----------|---------------------|
| **PM-AC-001** | Entity definitions cover: feature_request, user_need, roadmap_item, stakeholder_feedback, competitive_insight | Schema validation |
| **PM-AC-002** | Priority levels align with standard frameworks (P0-P3, MoSCoW) | Standard compliance |
| **PM-AC-003** | Extraction rules capture common PM terminology | Domain expert review |
| **PM-AC-004** | Patterns support quarterly roadmap planning | Workflow review |
| **PM-AC-005** | Prompt template addresses stakeholder management | Manual review |
| **PM-AC-006** | User need extraction supports persona development | Persona checklist |
| **PM-AC-007** | Output format supports backlog item creation | Schema validation |
| **PM-AC-008** | Validation criteria test against roadmap planning transcripts | Checklist review |

---

## Domain 4: User Experience

### Overview

**Target Users:** UX Researchers, UX Designers, Product Designers
**Transcript Types:** User research interviews, usability testing sessions, design critique meetings, stakeholder feedback sessions

### Entity Definitions (Design)

```yaml
# Design specification - actual implementation in FEAT-002
domain: user-experience
version: "1.0.0"

entities:
  user_insight:
    description: "Key insight from user research"
    attributes:
      - insight: "What was learned"
      - participant: "User identifier (anonymized)"
      - context: "Research context"
      - confidence: "high | medium | low"
      - supporting_quotes: "Direct quotes"

  pain_point:
    description: "User frustration or problem"
    attributes:
      - description: "The pain point"
      - severity: "critical | major | minor"
      - frequency: "always | often | sometimes | rarely"
      - user_quote: "Verbatim user feedback"

  usability_issue:
    description: "Problem found during testing"
    attributes:
      - task: "What user was trying to do"
      - issue: "What went wrong"
      - severity: "critical | major | minor | cosmetic"
      - recommendation: "Suggested fix"

  design_feedback:
    description: "Feedback on design artifacts"
    attributes:
      - artifact: "What was reviewed"
      - feedback_type: "positive | constructive | concern"
      - feedback: "The feedback"
      - action: "Suggested action"

  user_quote:
    description: "Verbatim user statement"
    attributes:
      - quote: "Exact words"
      - participant: "Who said it"
      - context: "When/why they said it"
      - theme: "Related theme"
```

### Extraction Rules (Design)

```yaml
# Design specification - actual implementation in FEAT-002
extraction_rules:
  insight_patterns:
    - pattern: "We learned that {insight}"
    - pattern: "Key insight: {insight}"
    - pattern: "Users consistently {behavior}"
    - pattern: "Pattern: {insight}"

  pain_point_patterns:
    - pattern: "Users struggle with {issue}"
    - pattern: "Frustration: {description}"
    - pattern: "I can't figure out how to {task}"
    - pattern: "This is confusing because {reason}"

  usability_patterns:
    - pattern: "User failed to {task}"
    - pattern: "Completion rate: {percentage}"
    - pattern: "User gave up on {task}"
    - pattern: "Error during {task}"
```

### Prompt Templates (Design)

```markdown
## User Experience Transcript Analysis

You are analyzing a {{$transcript_type}} transcript from a UX research session.

### Context
- Study: {{$study_name}}
- Participant: {{$participant_id}} (anonymized)
- Date: {{$session_date}}

### Extraction Instructions

1. **User Insights**: Capture key learnings
   - Extract: insight, participant, context, confidence, supporting quotes
   - Look for: "we learned", "key insight", "pattern"
   - PRESERVE exact user quotes verbatim

2. **Pain Points**: Document user frustrations
   - Extract: description, severity, frequency, user quote
   - Look for: "struggle with", "frustration", "confusing"

3. **Usability Issues**: Note testing problems
   - Extract: task, issue, severity, recommendation
   - Look for: "failed to", "error", "gave up"

4. **Design Feedback**: Capture critique
   - Extract: artifact, feedback type, feedback, suggested action
   - Look for: "I like", "concern about", "suggestion"

5. **User Quotes**: Preserve verbatim statements
   - Extract: exact quote, participant, context, theme
   - CRITICAL: Do not paraphrase user quotes

### Output Format
{{$output_schema}}
```

### Per-Domain Acceptance Criteria: User Experience

| ID | Criterion | Verification Method |
|----|-----------|---------------------|
| **UX-AC-001** | Entity definitions cover: user_insight, pain_point, usability_issue, design_feedback, user_quote | Schema validation |
| **UX-AC-002** | Severity scales align with Nielsen Norman severity ratings | Standard compliance |
| **UX-AC-003** | Extraction preserves verbatim user quotes | Quote fidelity test |
| **UX-AC-004** | Patterns support affinity diagramming workflow | Workflow review |
| **UX-AC-005** | Prompt template emphasizes quote preservation | Manual review |
| **UX-AC-006** | Participant anonymization handled properly | Privacy review |
| **UX-AC-007** | Output format supports research repository integration | Schema validation |
| **UX-AC-008** | Validation criteria test against usability testing transcripts | Checklist review |

---

## Domain 5: Cloud Engineering

### Overview

**Target Users:** Cloud Engineers, SREs, Platform Engineers, DevOps Engineers
**Transcript Types:** Incident post-mortems, capacity planning sessions, infrastructure reviews, on-call handoffs

### Entity Definitions (Design)

```yaml
# Design specification - actual implementation in FEAT-002
domain: cloud-engineering
version: "1.0.0"

entities:
  incident:
    description: "Production incident discussed"
    attributes:
      - incident_id: "Incident identifier"
      - severity: "SEV1 | SEV2 | SEV3 | SEV4"
      - impact: "Customer/business impact"
      - duration: "Time to resolution"
      - root_cause: "Why it happened"

  root_cause:
    description: "Underlying cause identified"
    attributes:
      - cause: "What caused the issue"
      - category: "human | process | system | external"
      - contributing_factors: "Other factors"
      - preventable: "yes | no | partially"

  action_item:
    description: "Follow-up action from review"
    attributes:
      - title: "Action title"
      - owner: "Person responsible"
      - priority: "P0 | P1 | P2"
      - due_date: "Target completion"
      - type: "fix | prevention | detection | process"

  metric:
    description: "Metric or measurement discussed"
    attributes:
      - name: "Metric name"
      - current_value: "Current measurement"
      - target_value: "Target/SLA"
      - trend: "improving | stable | degrading"

  capacity_concern:
    description: "Resource capacity issue"
    attributes:
      - resource: "What resource"
      - current_utilization: "Current usage"
      - threshold: "Warning threshold"
      - projection: "When limit reached"
      - mitigation: "Proposed solution"
```

### Extraction Rules (Design)

```yaml
# Design specification - actual implementation in FEAT-002
extraction_rules:
  incident_patterns:
    - pattern: "Incident {id} was caused by {cause}"
    - pattern: "SEV{level} incident"
    - pattern: "Root cause: {cause}"
    - pattern: "Impact: {impact}"

  action_patterns:
    - pattern: "Action item: {title}"
    - pattern: "{owner} will {action}"
    - pattern: "TODO: {action}"
    - pattern: "Follow-up: {action}"

  capacity_patterns:
    - pattern: "{resource} is at {percentage}% utilization"
    - pattern: "We'll hit capacity in {timeframe}"
    - pattern: "Need to scale {resource}"
    - pattern: "Capacity warning for {resource}"
```

### Prompt Templates (Design)

```markdown
## Cloud Engineering Transcript Analysis

You are analyzing a {{$transcript_type}} transcript from a cloud engineering session.

### Context
- Team: {{$team_name}}
- Incident ID: {{$incident_id}} (if applicable)
- Date: {{$meeting_date}}

### Extraction Instructions

1. **Incidents**: Capture incident details
   - Extract: incident_id, severity, impact, duration, root_cause
   - Look for: "incident", "SEV", "outage", "degradation"

2. **Root Causes**: Identify underlying causes
   - Extract: cause, category, contributing factors, preventability
   - Look for: "root cause", "caused by", "because"
   - Apply 5 Whys methodology

3. **Action Items**: Note follow-ups
   - Extract: title, owner, priority, due date, type
   - Categorize: fix, prevention, detection, process

4. **Metrics**: Document measurements
   - Extract: name, current value, target, trend
   - Look for: SLO, SLA, latency, error rate, availability

5. **Capacity Concerns**: Flag resource issues
   - Extract: resource, utilization, threshold, projection, mitigation
   - Look for: "at X% utilization", "capacity", "scale"

### Output Format
{{$output_schema}}
```

### Per-Domain Acceptance Criteria: Cloud Engineering

| ID | Criterion | Verification Method |
|----|-----------|---------------------|
| **CE-AC-001** | Entity definitions cover: incident, root_cause, action_item, metric, capacity_concern | Schema validation |
| **CE-AC-002** | Severity levels align with standard incident classification (SEV1-4) | Standard compliance |
| **CE-AC-003** | Root cause categories support blameless post-mortem culture | Culture review |
| **CE-AC-004** | Action items support SRE best practices (fix/prevent/detect) | SRE checklist |
| **CE-AC-005** | Prompt template encourages 5 Whys methodology | Methodology review |
| **CE-AC-006** | Metrics extraction supports SLO/SLA tracking | SLO alignment |
| **CE-AC-007** | Output format supports incident tracking system integration | Schema validation |
| **CE-AC-008** | Validation criteria test against post-mortem transcripts | Checklist review |

---

## Domain 6: Security Engineering

### Overview

**Target Users:** Security Engineers, Security Architects, AppSec Engineers, Compliance Officers
**Transcript Types:** Security audit discussions, threat modeling sessions, compliance reviews, vulnerability triage meetings

### Entity Definitions (Design)

```yaml
# Design specification - actual implementation in FEAT-002
domain: security-engineering
version: "1.0.0"

entities:
  vulnerability:
    description: "Security vulnerability identified"
    attributes:
      - title: "Vulnerability name"
      - cve: "CVE identifier (if applicable)"
      - severity: "critical | high | medium | low | informational"
      - cvss_score: "CVSS score"
      - affected_systems: "Systems impacted"
      - status: "open | in_progress | mitigated | accepted"

  threat:
    description: "Threat identified in modeling"
    attributes:
      - threat_id: "STRIDE category or custom ID"
      - description: "Threat description"
      - threat_actor: "Who could exploit"
      - attack_vector: "How they'd attack"
      - likelihood: "high | medium | low"
      - impact: "high | medium | low"

  mitigation:
    description: "Security control or fix"
    attributes:
      - title: "Mitigation name"
      - type: "preventive | detective | corrective"
      - implementation: "How to implement"
      - effectiveness: "high | medium | low"
      - status: "proposed | approved | implemented"

  compliance_gap:
    description: "Compliance requirement not met"
    attributes:
      - framework: "SOC2 | PCI | HIPAA | GDPR | etc."
      - requirement: "Specific requirement"
      - current_state: "Current compliance"
      - gap: "What's missing"
      - remediation: "How to fix"

  security_decision:
    description: "Security architecture decision"
    attributes:
      - topic: "What was decided"
      - decision: "The decision"
      - risk_accepted: "Any accepted risk"
      - rationale: "Why this decision"
      - approver: "Who approved"
```

### Extraction Rules (Design)

```yaml
# Design specification - actual implementation in FEAT-002
extraction_rules:
  vulnerability_patterns:
    - pattern: "CVE-{year}-{id}"
    - pattern: "Vulnerability: {title}"
    - pattern: "CVSS score: {score}"
    - pattern: "Critical|High|Medium|Low severity"

  threat_patterns:
    - pattern: "Threat: {description}"
    - pattern: "STRIDE: {category}"
    - pattern: "Attack vector: {vector}"
    - pattern: "Attacker could {action}"

  mitigation_patterns:
    - pattern: "Mitigation: {title}"
    - pattern: "We should {action} to prevent {threat}"
    - pattern: "Control: {control}"
    - pattern: "Remediation: {action}"

  compliance_patterns:
    - pattern: "SOC2|PCI|HIPAA|GDPR requirement"
    - pattern: "Compliance gap: {gap}"
    - pattern: "We're not compliant with {requirement}"
    - pattern: "Audit finding: {finding}"
```

### Prompt Templates (Design)

```markdown
## Security Engineering Transcript Analysis

You are analyzing a {{$transcript_type}} transcript from a security session.

### Context
- System: {{$system_name}}
- Compliance Framework: {{$framework}} (if applicable)
- Date: {{$meeting_date}}

### Extraction Instructions

1. **Vulnerabilities**: Capture security weaknesses
   - Extract: title, CVE, severity, CVSS score, affected systems, status
   - Look for: CVE references, severity ratings, CVSS scores

2. **Threats**: Document threat model findings
   - Extract: threat ID, description, actor, vector, likelihood, impact
   - Apply STRIDE framework where applicable

3. **Mitigations**: Note security controls
   - Extract: title, type, implementation, effectiveness, status
   - Categorize: preventive, detective, corrective

4. **Compliance Gaps**: Identify compliance issues
   - Extract: framework, requirement, current state, gap, remediation
   - Link to specific control requirements

5. **Security Decisions**: Capture risk decisions
   - Extract: topic, decision, accepted risk, rationale, approver
   - Flag any risk acceptance decisions

### Output Format
{{$output_schema}}
```

### Per-Domain Acceptance Criteria: Security Engineering

| ID | Criterion | Verification Method |
|----|-----------|---------------------|
| **SEC-AC-001** | Entity definitions cover: vulnerability, threat, mitigation, compliance_gap, security_decision | Schema validation |
| **SEC-AC-002** | Severity levels align with CVSS v3.1 qualitative ratings | Standard compliance |
| **SEC-AC-003** | Threat modeling supports STRIDE methodology | STRIDE checklist |
| **SEC-AC-004** | Compliance frameworks cover major standards (SOC2, PCI, HIPAA, GDPR) | Framework coverage |
| **SEC-AC-005** | Prompt template handles CVE extraction | CVE pattern test |
| **SEC-AC-006** | Risk acceptance decisions are explicitly captured | Decision audit |
| **SEC-AC-007** | Output format supports vulnerability tracking system integration | Schema validation |
| **SEC-AC-008** | Validation criteria test against security audit transcripts | Checklist review |

---

## Cross-Domain Validation Criteria

These criteria apply across all 6 domains:

| ID | Criterion | Verification Method |
|----|-----------|---------------------|
| **XD-AC-001** | All domains use consistent entity_definitions schema structure | Schema validation |
| **XD-AC-002** | All domains use consistent extraction_rules schema structure | Schema validation |
| **XD-AC-003** | All prompt templates use {{$variable}} syntax | Template validation |
| **XD-AC-004** | All domains have README.md with domain overview | File existence |
| **XD-AC-005** | All domains validate against context-injection-schema.json | JSON Schema validation |
| **XD-AC-006** | VCRM links domains to requirements from SPEC-context-injection.md | Traceability matrix |

---

## Validation Approach

### Validation Pipeline

```
┌────────────────────────────────────────────────────────────────────────────┐
│                       TASK-038 Validation Pipeline                          │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  1. SCHEMA VALIDATION (ps-validator)                                       │
│     ├── Validate entity_definitions.yaml against schema                    │
│     ├── Validate extraction_rules.yaml against schema                      │
│     └── Validate prompt templates have required sections                   │
│                                                                            │
│  2. MANUAL REVIEW (Domain Expert)                                          │
│     ├── Review entity attributes for domain completeness                   │
│     ├── Review extraction patterns for coverage                            │
│     └── Review prompt templates for clarity                                │
│                                                                            │
│  3. VCRM TRACEABILITY (nse-verification)                                   │
│     ├── Link each domain to supported requirements                         │
│     ├── Verify NASA SE Process 7, 8 compliance                             │
│     └── Document verification approach                                     │
│                                                                            │
│  4. TRANSCRIPT TESTING (FEAT-002 - Implementation)                         │
│     ├── Test against real transcripts (user has transcripts)               │
│     ├── Measure extraction accuracy                                        │
│     └── Refine based on results                                            │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### Verification Cross Reference Matrix (VCRM) Template

| Requirement | SE | SA | PM | UX | CE | SEC | Verification Method |
|-------------|:--:|:--:|:--:|:--:|:--:|:---:|---------------------|
| REQ-CI-F-001 (Entity Recognition) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Schema validation |
| REQ-CI-F-002 (Extraction Rules) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Pattern testing |
| REQ-CI-F-003 (Prompt Templates) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Template validation |
| REQ-CI-F-004 (Domain Selection) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Selector testing |
| ... | | | | | | | |

---

## Deliverables

| Deliverable | Type | Link | Status |
|-------------|------|------|--------|
| Domain Specifications Directory | Documentation | docs/specs/domain-contexts/ | ✅ COMPLETE |
| README | Documentation | docs/specs/domain-contexts/README.md | ✅ COMPLETE |
| Domain JSON Schema | Schema | docs/specs/domain-contexts/DOMAIN-SCHEMA.json | ✅ COMPLETE |
| Software Engineering Spec | Specification | docs/specs/domain-contexts/01-software-engineering/ | ✅ COMPLETE |
| Software Architecture Spec | Specification | docs/specs/domain-contexts/02-software-architecture/ | ✅ COMPLETE |
| Product Management Spec | Specification | docs/specs/domain-contexts/03-product-management/ | ✅ COMPLETE |
| User Experience Spec | Specification | docs/specs/domain-contexts/04-user-experience/ | ✅ COMPLETE |
| Cloud Engineering Spec | Specification | docs/specs/domain-contexts/05-cloud-engineering/ | ✅ COMPLETE |
| Security Engineering Spec | Specification | docs/specs/domain-contexts/06-security-engineering/ | ✅ COMPLETE |
| VCRM Document | Verification | docs/specs/domain-contexts/VCRM-domains.md | ✅ COMPLETE |

---

## Implementation Notes (FEAT-002)

> **See:** [DISC-001](./EN-006--DISC-001-feat002-implementation-scope.md) for full details.

The following implementation tasks are required in FEAT-002:

1. **Create Actual Context Files**
   - `contexts/software-engineering.yaml`
   - `contexts/software-architecture.yaml`
   - `contexts/product-management.yaml`
   - `contexts/user-experience.yaml`
   - `contexts/cloud-engineering.yaml`
   - `contexts/security-engineering.yaml`

2. **Provide Test Transcripts**
   - User has transcripts to test against
   - One or more transcripts per domain
   - Used for validation and refinement

3. **Implement Validation Process**
   - Manual review process
   - Schema validation tooling
   - Transcript-based testing workflow

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-26 | Created     | Task created with 4 generic domains |
| 2026-01-27 | Updated     | Major revision: 6 transcript analysis domains with per-domain AC |
| 2026-01-27 | COMPLETE    | All 34 specification files created (6 domains × 5 files + 4 base files) |

---

*Task ID: TASK-038*
*Workflow ID: en006-ctxinj-20260126-001*
*Phase: 3 (Integration, Risk & Examples)*
*NASA SE: Process 7, 8 (Verification)*
