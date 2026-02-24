# /red-team Adversary Integration

> **Version:** 1.0.0
> **Skill:** /red-team
> **Feature:** FEAT-037 (/adversary Integration)
> **SSOT:** `.context/rules/quality-enforcement.md`, ADR-PROJ010-006

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Integration scope and rationale |
| [Integration Point Mapping](#integration-point-mapping) | Which red-team outputs go through /adversary |
| [Finding Quality Review](#finding-quality-review) | How /adversary validates red-team findings |
| [Engagement Report Scoring](#engagement-report-scoring) | Completeness criteria for red-reporter output |
| [Remediation Guidance Quality](#remediation-guidance-quality) | How remediation recommendations are reviewed |
| [End-to-End Quality Workflow](#end-to-end-quality-workflow) | From agent output to accepted deliverable |

---

## Overview

The /red-team skill integrates with the /adversary skill to enforce quality gates on engagement deliverables. Unlike /eng-team's centralized eng-reviewer quality gate, /red-team's quality integration is distributed across different deliverable types with varying criticality levels.

**Key Principle:** Scope documents are always C4. Engagement reports are C2+. Individual findings scale from C1 (informational) to C3 (critical findings).

**Governing Rules:**
- H-13: Quality threshold >= 0.92 for C2+ deliverables
- H-14: Creator-critic-revision cycle (minimum 3 iterations)
- H-15: Self-review (S-010) before presenting any deliverable
- H-17: Quality scoring via S-014 LLM-as-Judge REQUIRED

---

## Integration Point Mapping

| Deliverable Type | Source Agent | Criticality | /adversary Integration |
|-----------------|-------------|-------------|----------------------|
| Scope document | red-lead | C4 (always) | Full tournament -- all 10 strategies |
| Engagement report | red-reporter | C2+ | Standard /adversary scoring |
| Executive summary | red-reporter | C2+ | S-007, S-002, S-014 minimum |
| Vulnerability findings (Critical) | red-vuln, red-exploit | C3 | C2 + S-004, S-012, S-013 |
| Vulnerability findings (High) | red-vuln, red-exploit | C2 | S-007, S-002, S-014 |
| Vulnerability findings (Medium/Low) | red-vuln | C1 | S-010 (self-review only) |
| Exploitation methodology | red-exploit | C2 | S-007, S-002, S-014 |
| Remediation guidance | red-reporter | C2 | S-007, S-003, S-014 |
| Reconnaissance report | red-recon | C1 | S-010 (self-review only) |
| Infrastructure methodology | red-infra | C1 | S-010 (self-review only) |

### Criticality Assignment Rules

| Condition | Criticality | Rationale |
|-----------|-------------|-----------|
| Scope document (any engagement) | C4 | Irreversible authorization decision |
| Final engagement report | C3 minimum | Drives remediation decisions with business impact |
| Critical/High vulnerability finding | C2+ | Findings that drive immediate remediation |
| Exploitation methodology for novel chains | C3 | Complex attack paths require rigorous validation |
| Executive summary for board/C-suite | C3 | Reputational risk from inaccurate reporting |
| Standard findings and methodology | C1 | Routine operational output |

---

## Finding Quality Review

### What /adversary Validates on Findings

| Quality Dimension | Validation Criteria | Weight |
|-------------------|-------------------|--------|
| Completeness | All CVSS metrics justified, reproduction steps complete, evidence attached | 0.20 |
| Internal Consistency | CVSS score matches described impact, severity aligns with technical detail | 0.20 |
| Methodological Rigor | ATT&CK mapping correct, CWE classification accurate, PTES phase appropriate | 0.20 |
| Evidence Quality | Screenshots/tool output present, reproduction verified, scope compliance confirmed | 0.15 |
| Actionability | Remediation guidance specific, effort estimates realistic, priority justified | 0.15 |
| Traceability | Finding linked to scope targets, technique in allowlist, evidence chain intact | 0.10 |

### Finding Validation Protocol

1. red-vuln or red-exploit produces finding using [Vulnerability Report Template](templates/vulnerability-report.md)
2. Agent performs self-review (S-010, H-15)
3. For C2+ findings:
   a. Submit to /adversary (adv-scorer) for S-014 scoring
   b. adv-scorer evaluates against 6 dimensions
   c. If score < 0.92: return findings for revision
   d. If score >= 0.92: finding accepted
4. Accepted findings feed into red-reporter for engagement report

---

## Engagement Report Scoring

### Completeness Criteria for red-reporter Output

| Section | Required | Completeness Check |
|---------|----------|-------------------|
| Executive Summary | Yes | Business risk communicated, key metrics present |
| Methodology | Yes | PTES phases documented, scope referenced |
| Findings (all) | Yes | Every finding documented with full detail |
| Risk Matrix | Yes | All findings plotted by likelihood x impact |
| Remediation Roadmap | Yes | Priority-ordered with timelines and effort |
| Kill Chain Progress | Yes | ATT&CK tactics coverage documented |
| Evidence Appendix | Yes | All evidence artifacts referenced and accessible |
| Scope Compliance | Yes | Attestation that all activities were within scope |

### Report Scoring Protocol

1. red-reporter produces engagement report
2. Self-review (S-010, H-15)
3. Submit to /adversary for scoring:
   - C3+ engagements: Full strategy set (S-007, S-002, S-004, S-012, S-013, S-014)
   - C2 engagements: Standard set (S-007, S-002, S-014)
4. Quality threshold: >= 0.92 (H-13)
5. Below threshold: revision cycle (H-14, minimum 3 iterations)

---

## Remediation Guidance Quality

### What Makes Good Remediation Guidance

| Attribute | Poor | Acceptable | Good |
|-----------|------|-----------|------|
| Specificity | "Fix the vulnerability" | "Update the library" | "Update library X from v2.1 to v2.3.1 which patches CVE-2026-XXXX" |
| Effort | No estimate | "Medium effort" | "~4 hours for backend team; requires regression testing of auth flow" |
| Priority | No priority | "High priority" | "P1: Exploit publicly available, CVSS 9.1, 72h SLA" |
| Verification | No verification plan | "Rescan after fix" | "Rerun DAST scan targeting endpoint X; verify SAST rule Y no longer triggers" |

### Remediation /adversary Review

/adversary applies S-003 (Steelman) before S-002 (Devil's Advocate) per H-16:

1. **Steelman (S-003):** Strengthen the remediation recommendation -- is there a more complete fix? Are there additional mitigations that would increase defense-in-depth?
2. **Devil's Advocate (S-002):** Challenge the recommendation -- could this fix introduce new issues? Is the effort estimate realistic? Are there edge cases not covered?
3. **S-014 Scoring:** Score the remediation guidance against the 6 quality dimensions

---

## End-to-End Quality Workflow

### Scope Documents (C4 -- Always)

```
red-lead produces scope document
    |
    v
Self-review (S-010)
    |
    v
Submit to /adversary (FULL TOURNAMENT -- all 10 strategies)
    |
    v
Score >= 0.92? --YES--> APPROVED (proceed with engagement)
    |
    NO
    |
    v
Revision cycle (H-14, min 3 iterations)
```

### Engagement Reports (C2+)

```
red-reporter produces engagement report
    |
    v
Self-review (S-010)
    |
    v
Submit to /adversary (strategy set per criticality)
    |
    v
Score >= 0.92? --YES--> APPROVED (deliver to stakeholders)
    |
    NO
    |
    v
Return findings to red-reporter for revision
    |
    v
Re-score (H-14 cycle)
```

### Individual Findings (C1+)

```
red-vuln/red-exploit produces finding
    |
    v
Self-review (S-010) -- ALL findings regardless of criticality
    |
    +-- C1: Self-review sufficient, finding accepted
    |
    +-- C2+: Submit to /adversary for scoring
            |
            v
        Score >= 0.92? --YES--> Finding accepted
            |
            NO
            |
            v
        Return to originating agent for revision
```

### Quality Score Dimensions (S-014)

| Dimension | Weight | red-team Focus |
|-----------|--------|---------------|
| Completeness | 0.20 | All fields populated, evidence attached, scope reference present |
| Internal Consistency | 0.20 | CVSS matches description, severity consistent, ATT&CK mapping accurate |
| Methodological Rigor | 0.20 | PTES phases followed, methodology standards cited, technique IDs valid |
| Evidence Quality | 0.15 | Tool output present, reproduction verified, evidence properly stored |
| Actionability | 0.15 | Remediation specific and implementable, effort realistic, priority justified |
| Traceability | 0.10 | Scope -> finding -> evidence -> remediation chain intact |

---

*Version: 1.0.0 | /red-team Skill | FEAT-037 | PROJ-010 Cyber Ops*
