# Prompt Templates: User Experience Domain

<!--
DOCUMENT: prompt-templates.md
VERSION: 1.0.0
DOMAIN: user-experience
TASK: TASK-038 (Phase 3)
STATUS: DESIGN COMPLETE

CRITICAL: This domain requires preservation of verbatim user quotes.
-->

---

## Primary Extraction Prompt

```markdown
## User Experience Transcript Analysis

You are analyzing a {{$transcript_type}} transcript from a UX research session.

### Context

- **Study**: {{$study_name}}
- **Participant**: {{$participant_id}} (anonymized)
- **Date**: {{$session_date}}
- **Research Question**: {{$research_question}}

### ⚠️ CRITICAL: Verbatim Quote Preservation

**DO NOT paraphrase, summarize, or clean up user quotes.**

User quotes must be preserved EXACTLY as spoken, including:
- Filler words ("um", "like", "you know")
- Grammatical errors
- Incomplete sentences
- Colloquialisms

This is essential for research validity.

### Extraction Instructions

#### 1. User Insights
Capture key learnings from the research.

**Extract:**
- `insight`: What was learned
- `participant`: User identifier (P01, P02, etc.)
- `context`: Research context
- `confidence`: high | medium | low
- `supporting_quotes`: Direct quotes (VERBATIM)

**Look for phrases:**
- "We learned that...", "Key insight:...", "Users consistently..."
- "Pattern:", "Theme:", "We observed..."

#### 2. Pain Points
Document user frustrations and problems.

**Extract:**
- `description`: The pain point
- `severity`: critical | major | minor | cosmetic (Nielsen Norman)
- `frequency`: always | often | sometimes | rarely
- `user_quote`: VERBATIM quote expressing the pain

**Look for phrases:**
- "Users struggle with...", "Frustration:...", "I can't figure out..."
- "This is confusing...", "I hate when..."

#### 3. Usability Issues
Note problems found during testing.

**Extract:**
- `task`: What user was trying to do
- `issue`: What went wrong
- `severity`: 0-4 (Nielsen Norman scale)
- `recommendation`: Suggested fix

**Look for phrases:**
- "User failed to...", "Gave up on...", "Error during..."
- "Completion rate:", "Task success:"

#### 4. Design Feedback
Capture critique and suggestions.

**Extract:**
- `artifact`: What was reviewed
- `feedback_type`: positive | constructive | concern
- `feedback`: The feedback
- `action`: Suggested change

**Look for phrases:**
- "I like...", "Concern about...", "Suggestion:..."
- "This would be better if..."

#### 5. User Quotes
**⚠️ PRESERVE EXACTLY AS SPOKEN**

**Extract:**
- `quote`: EXACT words - DO NOT MODIFY
- `participant`: Who said it
- `context`: When/why
- `theme`: Related theme

**Guidelines for quotes:**
- Include filler words ("um", "like")
- Keep grammatical errors
- Preserve incomplete thoughts
- Use [inaudible] for unclear speech
- Use [laughter] for non-verbal

### Output Format

{{$output_schema}}

### Quality Checklist

Before finalizing extraction:
- [ ] All quotes are verbatim (not paraphrased)
- [ ] Participant IDs are anonymized (P01, not real names)
- [ ] Severity ratings use Nielsen Norman scale
- [ ] Context is preserved for each insight
```

---

## Output Schema

```json
{
  "extraction_result": {
    "metadata": {
      "transcript_type": "string",
      "study_name": "string",
      "participant_id": "string",
      "date": "date"
    },
    "entities": {
      "user_insights": [
        {
          "insight": "string",
          "participant": "string",
          "context": "string",
          "confidence": "high|medium|low",
          "supporting_quotes": ["string (VERBATIM)"]
        }
      ],
      "pain_points": [
        {
          "description": "string",
          "severity": "critical|major|minor|cosmetic",
          "frequency": "always|often|sometimes|rarely",
          "user_quote": "string (VERBATIM)",
          "impact": "string"
        }
      ],
      "usability_issues": [
        {
          "task": "string",
          "issue": "string",
          "severity": "0|1|2|3|4",
          "recommendation": "string",
          "success_rate": "string|null"
        }
      ],
      "design_feedback": [
        {
          "artifact": "string",
          "feedback_type": "positive|constructive|concern",
          "feedback": "string",
          "action": "string|null"
        }
      ],
      "user_quotes": [
        {
          "quote": "string (VERBATIM - DO NOT MODIFY)",
          "participant": "string",
          "context": "string",
          "theme": "string"
        }
      ]
    },
    "themes": ["string"],
    "recommendations": ["string"]
  }
}
```

---

*Document ID: PROMPT-UX-001*
*Domain: user-experience*
*Task: TASK-038*
*Status: DESIGN COMPLETE*
