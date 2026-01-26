# Prompt Templates: Software Engineering Domain

<!--
DOCUMENT: prompt-templates.md
VERSION: 1.0.0
DOMAIN: software-engineering
TASK: TASK-038 (Phase 3)
STATUS: DESIGN COMPLETE

DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
standards. It is advisory only and does not constitute official NASA guidance.
-->

---

## Primary Extraction Prompt

```markdown
## Software Engineering Transcript Analysis

You are analyzing a {{$transcript_type}} transcript from a software engineering team.

### Context

- **Team**: {{$team_name}}
- **Sprint**: {{$sprint_number}}
- **Date**: {{$meeting_date}}
- **Participants**: {{$participants}}

### Extraction Instructions

Analyze the transcript and extract the following entities:

#### 1. Commitments
Identify all work items that team members commit to completing.

**Extract:**
- `assignee`: Person making the commitment
- `work_item`: Description of the work
- `sprint`: Sprint or time period
- `confidence`: high | medium | low (based on language certainty)

**Look for phrases:**
- "I will...", "I'm going to...", "I'll take..."
- "I'm picking up...", "My focus is...", "I'm committing to..."

#### 2. Blockers
Find any impediments preventing progress.

**Extract:**
- `reporter`: Person reporting the blocker
- `description`: What is blocked
- `dependency`: What/who is causing the block
- `severity`: critical | major | minor

**Look for phrases:**
- "I'm blocked on...", "Waiting for...", "Can't proceed until..."
- "Stuck on...", "Need help with...", "Dependency on..."

#### 3. Decisions
Capture all technical or process decisions made.

**Extract:**
- `topic`: What was being decided
- `outcome`: The decision made
- `rationale`: Why this decision (if mentioned)
- `participants`: Who was involved

**Look for phrases:**
- "We decided to...", "The decision is...", "Consensus is..."
- "Let's go with...", "Agreed to...", "Going forward..."

#### 4. Action Items
List all follow-up tasks assigned.

**Extract:**
- `owner`: Person responsible
- `task`: Description of the action
- `due_date`: When it's due (if mentioned)
- `context`: Related discussion

**Look for phrases:**
- "{Name} will...", "TODO:...", "Action item:..."
- "Can you...", "Please...", "Need to..."

#### 5. Risks
Identify any technical or schedule risks mentioned.

**Extract:**
- `description`: The risk
- `likelihood`: high | medium | low
- `impact`: high | medium | low
- `mitigation`: Proposed solution (if mentioned)

**Look for phrases:**
- "Risk is...", "Concern about...", "Could impact..."
- "Worried about...", "Potential issue...", "Red flag:..."

### Output Format

{{$output_schema}}

### Guidelines

1. **Preserve context**: Include enough context to understand each item
2. **Attribute correctly**: Ensure proper attribution to speakers
3. **Confidence levels**: Use language cues to assess confidence
4. **No fabrication**: Only extract what's explicitly stated
5. **Handle ambiguity**: Mark uncertain extractions with lower confidence
```

---

## Transcript Type-Specific Prompts

### Daily Standup Variant

```markdown
## Daily Standup Analysis

You are analyzing a **daily standup** from {{$team_name}}.

### Standup Focus

In standups, prioritize extracting:
1. **Yesterday's work** - What was completed
2. **Today's plan** - Commitments for today
3. **Blockers** - Any impediments

### Three Questions Framework

For each participant, identify:
- What did they accomplish yesterday?
- What will they work on today?
- What is blocking them?

### Output

Focus on:
- Commitments (high priority)
- Blockers (high priority)
- Action items related to blockers

{{$output_schema}}
```

### Sprint Planning Variant

```markdown
## Sprint Planning Analysis

You are analyzing a **sprint planning session** for {{$team_name}}, Sprint {{$sprint_number}}.

### Planning Focus

In planning sessions, prioritize extracting:
1. **Sprint commitments** - What the team is committing to
2. **Capacity concerns** - Risks to delivery
3. **Dependencies** - Cross-team dependencies
4. **Decisions** - Technical approach decisions

### Backlog Items

For each discussed item, capture:
- Who will work on it
- Story point estimate (if mentioned)
- Risks or concerns raised
- Dependencies identified

### Output

Focus on:
- Commitments (high priority)
- Risks (high priority)
- Decisions (medium priority)

{{$output_schema}}
```

### Sprint Retrospective Variant

```markdown
## Sprint Retrospective Analysis

You are analyzing a **sprint retrospective** for {{$team_name}}, Sprint {{$sprint_number}}.

### Retrospective Focus

In retrospectives, prioritize extracting:
1. **What went well** - Positive observations
2. **What could improve** - Areas for improvement
3. **Action items** - Concrete improvements to implement
4. **Decisions** - Process changes agreed upon

### Retrospective Categories

For each discussion point, identify:
- Category (went well | improve | try)
- Description
- Any resulting action items
- Who owns the action

### Output

Focus on:
- Action items (high priority)
- Decisions (high priority)
- Risks (medium priority)

{{$output_schema}}
```

---

## Template Variables Reference

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `{{$transcript_type}}` | string | Yes | Type of meeting |
| `{{$team_name}}` | string | Yes | Team identifier |
| `{{$sprint_number}}` | string | No | Current sprint |
| `{{$meeting_date}}` | date | Yes | Meeting date |
| `{{$participants}}` | array | No | List of participants |
| `{{$output_schema}}` | schema | Yes | Output format specification |

---

## Output Schema

```json
{
  "extraction_result": {
    "metadata": {
      "transcript_type": "string",
      "team": "string",
      "date": "date",
      "extraction_timestamp": "datetime"
    },
    "entities": {
      "commitments": [
        {
          "assignee": "string",
          "work_item": "string",
          "sprint": "string",
          "confidence": "high|medium|low",
          "source_quote": "string"
        }
      ],
      "blockers": [
        {
          "reporter": "string",
          "description": "string",
          "dependency": "string",
          "severity": "critical|major|minor",
          "source_quote": "string"
        }
      ],
      "decisions": [
        {
          "topic": "string",
          "outcome": "string",
          "rationale": "string",
          "participants": ["string"],
          "source_quote": "string"
        }
      ],
      "action_items": [
        {
          "owner": "string",
          "task": "string",
          "due_date": "date|null",
          "context": "string",
          "source_quote": "string"
        }
      ],
      "risks": [
        {
          "description": "string",
          "likelihood": "high|medium|low",
          "impact": "high|medium|low",
          "mitigation": "string|null",
          "source_quote": "string"
        }
      ]
    },
    "summary": {
      "total_commitments": "number",
      "active_blockers": "number",
      "decisions_made": "number",
      "action_items_assigned": "number",
      "risks_identified": "number"
    }
  }
}
```

---

*Document ID: PROMPT-SE-001*
*Domain: software-engineering*
*Task: TASK-038*
*Status: DESIGN COMPLETE*
