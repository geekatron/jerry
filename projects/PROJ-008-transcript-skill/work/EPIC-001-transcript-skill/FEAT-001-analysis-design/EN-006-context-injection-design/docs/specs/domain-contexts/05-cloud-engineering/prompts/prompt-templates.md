# Prompt Templates: Cloud Engineering Domain

<!--
DOCUMENT: prompt-templates.md
VERSION: 1.0.0
DOMAIN: cloud-engineering
TASK: TASK-038 (Phase 3)
STATUS: DESIGN COMPLETE
-->

---

## Primary Extraction Prompt

```markdown
## Cloud Engineering Transcript Analysis

You are analyzing a {{$transcript_type}} transcript from a cloud engineering session.

### Context

- **Team**: {{$team_name}}
- **Incident ID**: {{$incident_id}} (if applicable)
- **Date**: {{$meeting_date}}
- **Services**: {{$services_affected}}

### ⚠️ IMPORTANT: Blameless Culture

This analysis should support a BLAMELESS post-mortem culture:
- Focus on WHAT happened, not WHO did it
- Identify systemic issues, not individual mistakes
- Look for process improvements, not blame

### Extraction Instructions

#### 1. Incidents
Capture incident details discussed.

**Extract:**
- `incident_id`: Incident identifier
- `severity`: SEV1 | SEV2 | SEV3 | SEV4
- `impact`: Customer/business impact
- `duration`: Time to resolution
- `services_affected`: Impacted services

**Look for phrases:**
- "Incident...", "SEV...", "outage", "degradation"
- "Impact:", "Duration:", "affected"

#### 2. Root Causes
Identify underlying causes (blameless).

**Extract:**
- `cause`: What caused it (not who)
- `category`: human | process | system | external
- `contributing_factors`: Other factors
- `preventable`: yes | no | partially

**Apply 5 Whys methodology:**
- Why did X happen? → Because Y
- Why did Y happen? → Because Z
- Continue until root cause

**Look for phrases:**
- "Root cause:", "Because...", "5 Whys"
- "Contributing factor:", "System failure:"

#### 3. Action Items
Note follow-up actions.

**Extract:**
- `title`: Action description
- `owner`: Person/team responsible
- `priority`: P0 | P1 | P2
- `due_date`: Target completion
- `type`: fix | prevention | detection | process

**Categorize by SRE best practices:**
- **Fix**: Immediate remediation
- **Prevention**: Stop future occurrence
- **Detection**: Improve monitoring
- **Process**: Update runbooks

**Look for phrases:**
- "Action item:", "{name} will...", "TODO:"
- "Prevention:", "Follow-up:", "P1:"

#### 4. Metrics
Document SLO/SLA measurements.

**Extract:**
- `name`: Metric name
- `current_value`: Current measurement
- `target_value`: SLO target
- `trend`: improving | stable | degrading

**Look for phrases:**
- "SLO:", "Error rate:", "Latency p99:"
- "Target:", "Availability:"

#### 5. Capacity Concerns
Flag resource issues.

**Extract:**
- `resource`: What resource
- `current_utilization`: Current usage
- `threshold`: Warning level
- `projection`: When limit reached
- `mitigation`: Proposed solution

**Look for phrases:**
- "at X% utilization", "capacity", "scale"
- "headroom:", "We'll hit capacity..."

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
      "team": "string",
      "incident_id": "string|null",
      "date": "date"
    },
    "entities": {
      "incidents": [
        {
          "incident_id": "string",
          "severity": "SEV1|SEV2|SEV3|SEV4",
          "impact": "string",
          "duration": "string",
          "services_affected": ["string"],
          "source_quote": "string"
        }
      ],
      "root_causes": [
        {
          "cause": "string",
          "category": "human|process|system|external",
          "contributing_factors": ["string"],
          "preventable": "yes|no|partially",
          "five_whys": ["string"],
          "source_quote": "string"
        }
      ],
      "action_items": [
        {
          "title": "string",
          "owner": "string",
          "priority": "P0|P1|P2",
          "due_date": "date|null",
          "type": "fix|prevention|detection|process",
          "source_quote": "string"
        }
      ],
      "metrics": [
        {
          "name": "string",
          "current_value": "string",
          "target_value": "string",
          "trend": "improving|stable|degrading",
          "breach": "yes|no|at_risk"
        }
      ],
      "capacity_concerns": [
        {
          "resource": "string",
          "current_utilization": "string",
          "threshold": "string",
          "projection": "string",
          "mitigation": "string"
        }
      ]
    },
    "summary": {
      "incident_severity": "string",
      "action_items_by_type": {
        "fix": "number",
        "prevention": "number",
        "detection": "number",
        "process": "number"
      },
      "slo_status": "healthy|at_risk|breached"
    }
  }
}
```

---

*Document ID: PROMPT-CE-001*
*Domain: cloud-engineering*
*Task: TASK-038*
*Status: DESIGN COMPLETE*
