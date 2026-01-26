# Prompt Templates: Product Management Domain

<!--
DOCUMENT: prompt-templates.md
VERSION: 1.0.0
DOMAIN: product-management
TASK: TASK-038 (Phase 3)
STATUS: DESIGN COMPLETE
-->

---

## Primary Extraction Prompt

```markdown
## Product Management Transcript Analysis

You are analyzing a {{$transcript_type}} transcript from a product planning session.

### Context

- **Product**: {{$product_name}}
- **Planning Horizon**: {{$planning_quarter}}
- **Date**: {{$meeting_date}}
- **Participants**: {{$participants}}

### Extraction Instructions

#### 1. Feature Requests
Capture requested capabilities.

**Extract:**
- `title`: Feature name
- `description`: What it does
- `requester`: Who requested (customer, sales, exec)
- `business_value`: Why it's valuable
- `priority`: P0 | P1 | P2 | P3

**Look for phrases:**
- "We need...", "Customers are asking for...", "Feature request:..."

#### 2. User Needs
Document identified requirements.

**Extract:**
- `persona`: User type
- `need`: What they need
- `pain_point`: Current problem
- `frequency`: always | often | sometimes | rarely

**Look for phrases:**
- "Users need...", "Pain point:...", "The problem is..."

#### 3. Roadmap Items
Note planned work.

**Extract:**
- `title`: Item name
- `quarter`: Target quarter
- `dependencies`: What it depends on
- `success_metric`: How to measure success

**Look for phrases:**
- "Targeting Q...", "On the roadmap for...", "Planning to ship..."

#### 4. Stakeholder Feedback
Capture input from stakeholders.

**Extract:**
- `stakeholder`: Who (name, role, company)
- `topic`: What about
- `sentiment`: positive | neutral | negative
- `key_points`: Main points

**Look for phrases:**
- "{Name} said...", "Feedback from...", "{Customer} mentioned..."

#### 5. Competitive Insights
Note competitor discussion.

**Extract:**
- `competitor`: Which competitor
- `feature`: What they have/do
- `our_position`: ahead | parity | behind
- `action`: Suggested response

**Look for phrases:**
- "{Competitor} has...", "Competitive gap:...", "We're behind on..."

### Output Format

{{$output_schema}}
```

---

## Output Schema

```json
{
  "extraction_result": {
    "metadata": {
      "transcript_type": "string",
      "product": "string",
      "date": "date",
      "planning_quarter": "string"
    },
    "entities": {
      "feature_requests": [
        {
          "title": "string",
          "description": "string",
          "requester": "string",
          "business_value": "string",
          "priority": "P0|P1|P2|P3",
          "source_quote": "string"
        }
      ],
      "user_needs": [
        {
          "persona": "string",
          "need": "string",
          "pain_point": "string",
          "frequency": "always|often|sometimes|rarely",
          "source_quote": "string"
        }
      ],
      "roadmap_items": [
        {
          "title": "string",
          "quarter": "string",
          "dependencies": ["string"],
          "success_metric": "string",
          "confidence": "high|medium|low",
          "source_quote": "string"
        }
      ],
      "stakeholder_feedback": [
        {
          "stakeholder": "string",
          "topic": "string",
          "sentiment": "positive|neutral|negative",
          "key_points": ["string"],
          "source_quote": "string"
        }
      ],
      "competitive_insights": [
        {
          "competitor": "string",
          "feature": "string",
          "our_position": "ahead|parity|behind",
          "action": "string",
          "source_quote": "string"
        }
      ]
    },
    "summary": {
      "high_priority_features": "number",
      "roadmap_items_by_quarter": {"Q1": "number", "Q2": "number"},
      "competitive_gaps": "number"
    }
  }
}
```

---

*Document ID: PROMPT-PM-001*
*Domain: product-management*
*Task: TASK-038*
*Status: DESIGN COMPLETE*
