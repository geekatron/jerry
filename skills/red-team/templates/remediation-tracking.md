# Remediation Tracking Template

> **Version:** 1.0.0
> **Skill:** /red-team
> **Agent:** red-reporter
> **Configurable Rule Set:** R-011
> **SSOT:** FEAT-040 Finding Lifecycle

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Template scope and finding lifecycle |
| [L0: Remediation Dashboard](#l0-remediation-dashboard) | Stakeholder-accessible status overview |
| [L1: Finding Tracker](#l1-finding-tracker) | Detailed finding lifecycle tracking |
| [L2: Trend Analysis](#l2-trend-analysis) | Strategic remediation metrics |
| [Configuration](#configuration) | Configurable rule set parameters |

---

## Overview

This template tracks the remediation lifecycle of findings from discovery through verification. It implements the finding lifecycle defined in FEAT-040: Open -> Confirmed -> Remediation In Progress -> Remediation Complete -> Verified -> Closed.

**When to use:** After the initial engagement report is delivered, to track remediation progress across findings. Updated periodically (recommended: weekly).

**Agent:** red-reporter (tracks and reports remediation status).

### Finding Lifecycle

```
Open -> Confirmed -> Remediation In Progress -> Remediation Complete -> Verified -> Closed
                 \                                                         /
                  +---> Accepted (risk acceptance with justification) -----+
                  \
                   +---> False Positive (with evidence) -> Closed
```

---

## L0: Remediation Dashboard

| Field | Value |
|-------|-------|
| **Engagement ID** | RED-{NNNN} |
| **Report Date** | {YYYY-MM-DD} |
| **Total Findings** | {count} |
| **Remediated** | {count} ({%}) |
| **In Progress** | {count} ({%}) |
| **Open** | {count} ({%}) |
| **Overdue** | {count} |

### Status by Severity

| Severity | Total | Closed | Verified | In Progress | Open | Overdue |
|----------|-------|--------|----------|-------------|------|---------|
| Critical | {n} | {n} | {n} | {n} | {n} | {n} |
| High | {n} | {n} | {n} | {n} | {n} | {n} |
| Medium | {n} | {n} | {n} | {n} | {n} | {n} |
| Low | {n} | {n} | {n} | {n} | {n} | {n} |

### SLA Compliance

| Severity | SLA (days) | Within SLA | Overdue | Compliance % |
|----------|-----------|------------|---------|-------------|
| Critical | 7 | {n} | {n} | {%} |
| High | 30 | {n} | {n} | {%} |
| Medium | 90 | {n} | {n} | {%} |
| Low | 180 | {n} | {n} | {%} |

---

## L1: Finding Tracker

### Active Findings

| Finding ID | Title | Severity | Status | Owner | Due Date | Days Open |
|------------|-------|----------|--------|-------|----------|-----------|
| {ID} | {title} | {severity} | {status} | {owner} | {date} | {days} |

### Finding Detail

#### {Finding ID}: {Title}

| Field | Value |
|-------|-------|
| **Severity** | {severity} |
| **CVSS** | {score} |
| **Status** | {lifecycle status} |
| **Owner** | {remediation owner} |
| **Discovered** | {date} |
| **SLA Due** | {date} |
| **Last Updated** | {date} |

**Remediation Plan:**

{Description of planned remediation action.}

**Progress Notes:**

| Date | Note | Author |
|------|------|--------|
| {date} | {progress note} | {author} |

**Verification:**

| Verification Type | Date | Result | Verified By |
|-------------------|------|--------|-------------|
| {Retest / Scan / Code Review} | {date} | {Pass / Fail} | {verifier} |

---

## L2: Trend Analysis

### Remediation Velocity

| Period | Findings Opened | Findings Closed | Net Change | Avg Days to Close |
|--------|----------------|----------------|------------|-------------------|
| {week/month} | {n} | {n} | {+/-n} | {days} |

### Risk Reduction Over Time

| Date | Total Risk Score | Critical Open | High Open | Trend |
|------|-----------------|---------------|-----------|-------|
| {date} | {cumulative CVSS} | {n} | {n} | {Improving / Stable / Degrading} |

### Systemic Issues

| Pattern | Findings Affected | Root Cause | Recommended Systemic Fix |
|---------|------------------|-----------|------------------------|
| {pattern} | {finding IDs} | {root cause} | {fix} |

---

## Configuration

### Configurable Rule Set (R-011)

| Parameter | Default | Override | Description |
|-----------|---------|----------|-------------|
| `sla_critical_days` | 7 | 1-30 | SLA for critical findings |
| `sla_high_days` | 30 | 7-90 | SLA for high findings |
| `sla_medium_days` | 90 | 30-180 | SLA for medium findings |
| `sla_low_days` | 180 | 90-365 | SLA for low findings |
| `tracking_frequency` | weekly | daily, weekly, biweekly | Update cadence |
| `auto_escalate_overdue` | true | false | Escalate overdue findings |

---

*Template Version: 1.0.0 | /red-team Skill | PROJ-010 Cyber Ops*
