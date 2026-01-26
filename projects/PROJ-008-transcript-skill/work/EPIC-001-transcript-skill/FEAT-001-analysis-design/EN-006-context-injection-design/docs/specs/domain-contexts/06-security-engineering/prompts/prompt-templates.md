# Prompt Templates: Security Engineering Domain

<!--
DOCUMENT: prompt-templates.md
VERSION: 1.0.0
DOMAIN: security-engineering
TASK: TASK-038 (Phase 3)
STATUS: DESIGN COMPLETE
-->

---

## Primary Extraction Prompt

```markdown
## Security Engineering Transcript Analysis

You are analyzing a {{$transcript_type}} transcript from a security session.

### Context

- **System**: {{$system_name}}
- **Compliance Framework**: {{$framework}} (if applicable)
- **Date**: {{$meeting_date}}
- **Participants**: {{$participants}}

### Extraction Instructions

#### 1. Vulnerabilities
Capture security weaknesses identified.

**Extract:**
- `title`: Vulnerability name
- `cve`: CVE identifier (CVE-YYYY-NNNNN) if mentioned
- `severity`: critical | high | medium | low | informational
- `cvss_score`: Numeric CVSS v3.1 score (0.0-10.0)
- `affected_systems`: Impacted systems
- `status`: open | in_progress | mitigated | accepted

**Look for phrases:**
- "CVE-...", "Vulnerability:", "CVSS score:"
- "Critical/High/Medium/Low severity", "CWE-..."

#### 2. Threats
Document threat model findings.

**Extract:**
- `threat_id`: STRIDE category or ID
- `description`: Threat description
- `threat_actor`: Who could exploit (external attacker, insider)
- `attack_vector`: How they'd attack
- `likelihood`: high | medium | low
- `impact`: high | medium | low

**Apply STRIDE Framework:**
- **S**poofing - Identity impersonation
- **T**ampering - Data modification
- **R**epudiation - Denying actions
- **I**nformation Disclosure - Data exposure
- **D**enial of Service - Availability
- **E**levation of Privilege - Unauthorized access

**Look for phrases:**
- "Threat:", "STRIDE:", "Attack vector:"
- "Attacker could...", "Threat actor:"

#### 3. Mitigations
Note security controls proposed or implemented.

**Extract:**
- `title`: Mitigation name
- `type`: preventive | detective | corrective
- `implementation`: How to implement
- `effectiveness`: high | medium | low
- `status`: proposed | approved | implemented | verified

**Control types:**
- **Preventive**: Stop attack before it happens
- **Detective**: Identify attack in progress
- **Corrective**: Respond and recover

**Look for phrases:**
- "Mitigation:", "Control:", "Remediation:"
- "We should... to prevent...", "Fix:"

#### 4. Compliance Gaps
Identify compliance issues.

**Extract:**
- `framework`: SOC2 | PCI-DSS | HIPAA | GDPR | ISO27001
- `requirement`: Specific control/requirement
- `current_state`: What we have
- `gap`: What's missing
- `remediation`: How to fix

**Look for phrases:**
- "SOC2/PCI/HIPAA/GDPR requirement"
- "Compliance gap:", "Audit finding:"
- "We're not compliant with..."

#### 5. Security Decisions
Capture risk decisions (especially risk acceptance).

**Extract:**
- `topic`: What was decided
- `decision`: The decision
- `risk_accepted`: Any accepted risk (CRITICAL to capture)
- `rationale`: Why this decision
- `approver`: Who approved

**⚠️ Flag risk acceptance explicitly - auditors need this.**

**Look for phrases:**
- "Security decision:", "Risk accepted:"
- "Approved by...", "Accept the risk of..."

### Output Format

{{$output_schema}}

### ⚠️ Important Notes

1. **CVE Format**: Extract exact CVE identifiers (CVE-YYYY-NNNNN)
2. **CVSS Scores**: Use numeric scores where mentioned
3. **Risk Acceptance**: Always flag with approver
4. **Compliance**: Map to specific framework controls
```

---

## Output Schema

```json
{
  "extraction_result": {
    "metadata": {
      "transcript_type": "string",
      "system": "string",
      "framework": "string|null",
      "date": "date"
    },
    "entities": {
      "vulnerabilities": [
        {
          "title": "string",
          "cve": "string|null",
          "severity": "critical|high|medium|low|informational",
          "cvss_score": "number|null",
          "affected_systems": ["string"],
          "status": "open|in_progress|mitigated|accepted",
          "cwe": "string|null",
          "source_quote": "string"
        }
      ],
      "threats": [
        {
          "threat_id": "string",
          "description": "string",
          "threat_actor": "string",
          "attack_vector": "string",
          "likelihood": "high|medium|low",
          "impact": "high|medium|low",
          "stride_category": "S|T|R|I|D|E",
          "source_quote": "string"
        }
      ],
      "mitigations": [
        {
          "title": "string",
          "type": "preventive|detective|corrective",
          "implementation": "string",
          "effectiveness": "high|medium|low",
          "status": "proposed|approved|implemented|verified",
          "source_quote": "string"
        }
      ],
      "compliance_gaps": [
        {
          "framework": "SOC2|PCI-DSS|HIPAA|GDPR|ISO27001",
          "requirement": "string",
          "current_state": "string",
          "gap": "string",
          "remediation": "string",
          "source_quote": "string"
        }
      ],
      "security_decisions": [
        {
          "topic": "string",
          "decision": "string",
          "risk_accepted": "string|null",
          "rationale": "string",
          "approver": "string|null",
          "source_quote": "string"
        }
      ]
    },
    "summary": {
      "critical_vulnerabilities": "number",
      "high_vulnerabilities": "number",
      "risks_accepted": "number",
      "compliance_gaps_by_framework": {
        "SOC2": "number",
        "PCI": "number"
      }
    }
  }
}
```

---

*Document ID: PROMPT-SEC-001*
*Domain: security-engineering*
*Task: TASK-038*
*Status: DESIGN COMPLETE*
