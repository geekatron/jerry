# Domain Specification: Software Engineering

<!--
DOCUMENT: SPEC-software-engineering.md
VERSION: 1.0.0
DOMAIN: software-engineering
SOURCE: EN-006 Context Injection Design (TASK-038)
PROMOTED: EN-014 Domain Context Files (TASK-157)
STATUS: COMPLETE
-->

---

> **DISCLAIMER:** This guidance is AI-generated based on NASA Systems Engineering
> standards. It is advisory only and does not constitute official NASA guidance.
> All SE decisions require human review and professional engineering judgment.

---

## Document Control

| Attribute | Value |
|-----------|-------|
| **Domain ID** | software-engineering |
| **Version** | 1.0.0 |
| **Status** | DESIGN COMPLETE |
| **Created** | 2026-01-27 |
| **Promoted** | 2026-01-29 (EN-014 TASK-157) |

---

## L0: Overview (ELI5)

This domain helps analyze **software team meetings** like:
- Daily standups ("What did you do? What will you do? Any blockers?")
- Sprint planning ("What can we commit to this sprint?")
- Code reviews ("The approach looks good, but consider...")

It extracts **key information** like:
- What work people committed to
- What's blocking progress
- What decisions were made
- What follow-up actions are needed

---

## L1: Domain Details (Software Engineer)

### Target Users

| Role | Use Case |
|------|----------|
| Software Engineers | Track personal commitments, blockers |
| Tech Leads | Monitor team progress, decisions |
| Engineering Managers | Understand team health, risks |
| Scrum Masters | Capture action items, impediments |

### Supported Transcript Types

| Type | Description | Typical Duration |
|------|-------------|------------------|
| Daily Standup | Quick status sync | 15 min |
| Sprint Planning | Commitment setting | 1-2 hours |
| Sprint Retrospective | Team improvement | 1 hour |
| Code Review | Technical discussion | 30-60 min |
| Pair Programming | Collaborative coding | Variable |

### Key Use Cases

1. **Track Commitments** - Who committed to what for this sprint
2. **Surface Blockers** - Identify what's preventing progress
3. **Capture Decisions** - Document technical choices made
4. **Extract Action Items** - List follow-up tasks with owners
5. **Identify Risks** - Flag potential issues early

---

## L2: Technical Specification (Principal Architect)

### Entity Model

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SOFTWARE ENGINEERING ENTITY MODEL                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────┐     blocks      ┌─────────────┐                           │
│  │ Commitment  │◄───────────────►│   Blocker   │                           │
│  │             │                 │             │                           │
│  │ - assignee  │                 │ - reporter  │                           │
│  │ - work_item │                 │ - issue     │                           │
│  │ - sprint    │                 │ - dependency│                           │
│  │ - confidence│                 │ - severity  │                           │
│  └──────┬──────┘                 └──────┬──────┘                           │
│         │                               │                                   │
│         │ relates_to                    │ resolves                          │
│         ▼                               ▼                                   │
│  ┌─────────────┐     triggers    ┌─────────────┐                           │
│  │  Decision   │────────────────►│ Action Item │                           │
│  │             │                 │             │                           │
│  │ - topic     │                 │ - owner     │                           │
│  │ - outcome   │                 │ - task      │                           │
│  │ - rationale │                 │ - due_date  │                           │
│  │ - parties   │                 │ - context   │                           │
│  └─────────────┘                 └──────┬──────┘                           │
│                                         │                                   │
│                                         │ mitigates                         │
│                                         ▼                                   │
│                                  ┌─────────────┐                           │
│                                  │    Risk     │                           │
│                                  │             │                           │
│                                  │ - desc      │                           │
│                                  │ - likelihood│                           │
│                                  │ - impact    │                           │
│                                  │ - mitigation│                           │
│                                  └─────────────┘                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Entity Definitions

See [contexts/software-engineering.yaml](../../contexts/software-engineering.yaml) for the complete schema.

| Entity | Purpose | Key Attributes |
|--------|---------|----------------|
| `commitment` | Work someone commits to | assignee, work_item, sprint, confidence |
| `blocker` | What's preventing progress | reporter, description, dependency, severity |
| `decision` | Technical/process decisions | topic, outcome, rationale, participants |
| `action_item` | Follow-up tasks | owner, task, due_date, context |
| `risk` | Identified risks | description, likelihood, impact, mitigation |

### Extraction Patterns

| Pattern Category | Example Phrases |
|------------------|-----------------|
| Commitment | "I will...", "I'm going to...", "I'll take..." |
| Blocker | "I'm blocked on...", "Waiting for...", "Can't proceed until..." |
| Decision | "We decided to...", "The decision is...", "Consensus is..." |
| Action Item | "TODO:", "Action item:", "{name} will..." |
| Risk | "Risk is...", "Concern about...", "Could impact..." |

### Prompt Template

**Key Template Variables:**

| Variable | Description | Example |
|----------|-------------|---------|
| `{{$transcript_type}}` | Type of meeting | "daily standup" |
| `{{$team_name}}` | Team identifier | "Platform Team" |
| `{{$sprint_number}}` | Current sprint | "Sprint 42" |
| `{{$meeting_date}}` | Meeting date | "2026-01-27" |
| `{{$output_schema}}` | Output format spec | JSON schema |

---

## Validation Criteria

| ID | Criterion | Status |
|----|-----------|--------|
| SE-AC-001 | Entity definitions cover 5 types | ✅ |
| SE-AC-002 | Each entity has ≥3 attributes | ✅ |
| SE-AC-003 | ≥4 extraction patterns per entity | ✅ |
| SE-AC-004 | Covers standup/planning terminology | ✅ |
| SE-AC-005 | Prompt template has {{$variable}} syntax | ✅ |
| SE-AC-006 | Clear extraction instructions | ✅ |
| SE-AC-007 | Output format aligns with SPEC schema | ✅ |
| SE-AC-008 | Validation criteria defined | ✅ |

---

## Implementation

1. **Context File**: `contexts/software-engineering.yaml`
2. **Test Transcripts**: Standup recordings, sprint planning notes
3. **Integration**: Jerry transcript skill activation

---

## References

| Document | Relationship |
|----------|--------------|
| [DOMAIN-SELECTION-GUIDE.md](./DOMAIN-SELECTION-GUIDE.md) | Domain selection flowchart |
| [contexts/software-engineering.yaml](../../contexts/software-engineering.yaml) | Implementation schema |

---

*Document ID: SPEC-SE-001*
*Domain: software-engineering*
*Status: DESIGN COMPLETE*
