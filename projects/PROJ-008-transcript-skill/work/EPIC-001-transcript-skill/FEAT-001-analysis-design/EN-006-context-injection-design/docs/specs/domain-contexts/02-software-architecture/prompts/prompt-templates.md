# Prompt Templates: Software Architecture Domain

<!--
DOCUMENT: prompt-templates.md
VERSION: 1.0.0
DOMAIN: software-architecture
TASK: TASK-038 (Phase 3)
STATUS: DESIGN COMPLETE
-->

---

## Primary Extraction Prompt

```markdown
## Software Architecture Transcript Analysis

You are analyzing a {{$transcript_type}} transcript from an architecture discussion.

### Context

- **System**: {{$system_name}}
- **ADR Number**: {{$adr_number}} (if applicable)
- **Date**: {{$meeting_date}}
- **Participants**: {{$participants}}

### Extraction Instructions

Analyze the transcript and extract the following entities:

#### 1. Architectural Decisions
Capture key architectural choices made during the discussion.

**Extract:**
- `title`: Decision title (suitable for ADR title)
- `context`: Why this decision is needed
- `decision`: What was decided
- `consequences`: Impact (positive and negative)
- `status`: proposed | accepted | deprecated | superseded

**Look for phrases:**
- "We're going with...", "The decision is...", "ADR:..."
- "We chose... because...", "We've decided to..."

#### 2. Alternatives Considered
Document options that were evaluated but not chosen.

**Extract:**
- `title`: Alternative name
- `description`: What it entails
- `pros`: Benefits of this option
- `cons`: Drawbacks of this option
- `rejection_reason`: Why it wasn't chosen

**Look for phrases:**
- "We considered...", "Another option was...", "We rejected... because..."
- "Alternative:", "was also on the table", "We ruled out..."

#### 3. Quality Attributes
Identify non-functional requirements discussed.

**Extract:**
- `attribute`: Category (performance | security | maintainability | reliability | etc.)
- `requirement`: Specific target or need
- `priority`: high | medium | low
- `trade_offs`: Related trade-offs

**Look for phrases:**
- "For [attribute], we need...", "[Attribute] is critical because..."
- "We're prioritizing... over...", "Trade-off between..."

#### 4. Components
Note system components or modules discussed.

**Extract:**
- `name`: Component identifier
- `responsibility`: What it does
- `interfaces`: How it connects
- `constraints`: Limitations

**Look for phrases:**
- "The [X] is responsible for...", "[X] component", "[X] service"
- "Interface between...", "[X] will handle..."

#### 5. Technical Debt
Flag any technical debt identified.

**Extract:**
- `description`: What is the debt
- `impact`: How it affects the system
- `remediation`: Proposed fix
- `priority`: high | medium | low

**Look for phrases:**
- "Technical debt:", "We're taking on debt by..."
- "This is a hack...", "We'll need to fix... later"

### Output Format

{{$output_schema}}

### Guidelines

1. **ADR Alignment**: Structure decisions for Nygard ADR format
2. **Capture Rationale**: Decision rationale is critical for ADRs
3. **Document All Options**: Record rejected alternatives with reasons
4. **ISO 25010**: Map quality attributes to standard categories
5. **No Fabrication**: Only extract what's explicitly stated
```

---

## ADR Discussion Variant

```markdown
## ADR Discussion Analysis

You are analyzing an **ADR discussion session** for {{$system_name}}.

### ADR Focus

This meeting is specifically about creating/reviewing an Architecture Decision Record.

### Nygard ADR Format

Structure extraction to support this ADR format:
1. **Title**: Short noun phrase
2. **Context**: Problem statement
3. **Decision**: Response/solution
4. **Status**: Proposed/Accepted/Deprecated/Superseded
5. **Consequences**: Results (good and bad)

### Output Priority

Focus on:
- Architectural decisions (highest priority)
- Alternatives considered (high priority)
- Quality attributes addressed (medium priority)

{{$output_schema}}
```

---

## Output Schema

```json
{
  "extraction_result": {
    "metadata": {
      "transcript_type": "string",
      "system": "string",
      "date": "date",
      "adr_number": "string|null"
    },
    "entities": {
      "architectural_decisions": [
        {
          "title": "string",
          "context": "string",
          "decision": "string",
          "consequences": {
            "positive": ["string"],
            "negative": ["string"]
          },
          "status": "proposed|accepted|deprecated|superseded",
          "source_quote": "string"
        }
      ],
      "alternatives": [
        {
          "title": "string",
          "description": "string",
          "pros": ["string"],
          "cons": ["string"],
          "rejection_reason": "string",
          "source_quote": "string"
        }
      ],
      "quality_attributes": [
        {
          "attribute": "string",
          "requirement": "string",
          "priority": "high|medium|low",
          "trade_offs": "string|null",
          "source_quote": "string"
        }
      ],
      "components": [
        {
          "name": "string",
          "responsibility": "string",
          "interfaces": ["string"],
          "constraints": "string|null",
          "source_quote": "string"
        }
      ],
      "technical_debt": [
        {
          "description": "string",
          "impact": "string",
          "remediation": "string|null",
          "priority": "high|medium|low",
          "source_quote": "string"
        }
      ]
    },
    "adr_draft": {
      "title": "string",
      "status": "string",
      "context": "string",
      "decision": "string",
      "consequences": "string"
    }
  }
}
```

---

*Document ID: PROMPT-SA-001*
*Domain: software-architecture*
*Task: TASK-038*
*Status: DESIGN COMPLETE*
