# Domain Specification: Cloud Engineering

<!--
DOCUMENT: SPEC-cloud-engineering.md
VERSION: 1.0.0
DOMAIN: cloud-engineering
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
| **Domain ID** | cloud-engineering |
| **Version** | 1.0.0 |
| **Status** | DESIGN COMPLETE |
| **Created** | 2026-01-27 |
| **Promoted** | 2026-01-29 (EN-014 TASK-157) |

---

## L0: Overview (ELI5)

This domain helps analyze **infrastructure and operations meetings** like:
- Incident post-mortems ("The database went down because...")
- Capacity planning ("We're at 80% CPU and growing...")
- On-call handoffs ("There's an issue with the payment service...")

It extracts **key information** like:
- Incident details and root causes
- Action items to prevent recurrence
- Capacity concerns and projections
- Key metrics and SLO status

---

## L1: Domain Details (Software Engineer)

### Target Users

| Role | Use Case |
|------|----------|
| SREs | Analyze incidents, track SLOs |
| Cloud Engineers | Capacity planning |
| Platform Engineers | Infrastructure decisions |
| DevOps Engineers | Operational improvements |

### Supported Transcript Types

| Type | Description | Typical Duration |
|------|-------------|------------------|
| Incident Post-Mortem | Blameless review | 1-2 hours |
| Capacity Planning | Resource forecasting | 1 hour |
| Infrastructure Review | Architecture discussion | 1-2 hours |
| On-Call Handoff | Shift transfer | 15-30 min |
| SLO Review | Service level review | 30-60 min |

### Incident Severity (Standard)

| Severity | Description | Response |
|----------|-------------|----------|
| SEV1 | Critical outage, customer-impacting | All hands, exec notification |
| SEV2 | Major degradation, limited impact | Team response, 1hr target |
| SEV3 | Minor degradation, workaround exists | Normal hours, 4hr target |
| SEV4 | Minimal impact, cosmetic | Backlog, best effort |

---

## L2: Technical Specification (Principal Architect)

### Entity Model

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     CLOUD ENGINEERING ENTITY MODEL                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐        caused_by     ┌─────────────────┐              │
│  │    Incident     │◄──────────────────────│   Root Cause    │              │
│  │                 │                       │                 │              │
│  │ - incident_id   │                       │ - cause         │              │
│  │ - severity      │◄─ SEV1/2/3/4          │ - category      │              │
│  │ - impact        │                       │ - contributing  │              │
│  │ - duration      │                       │ - preventable   │              │
│  │ - root_cause    │                       └─────────────────┘              │
│  └────────┬────────┘                                                        │
│           │                                                                  │
│           │ generates                                                        │
│           ▼                                                                  │
│  ┌─────────────────┐                       ┌─────────────────┐              │
│  │  Action Item    │       monitors        │     Metric      │              │
│  │                 │◄──────────────────────│                 │              │
│  │ - title         │                       │ - name          │              │
│  │ - owner         │                       │ - current_value │              │
│  │ - priority      │                       │ - target (SLO)  │              │
│  │ - due_date      │                       │ - trend         │              │
│  │ - type          │◄─ fix/prevent/detect  └─────────────────┘              │
│  └─────────────────┘                                                        │
│           │                                                                  │
│           │ addresses                                                        │
│           ▼                                                                  │
│  ┌─────────────────┐                                                        │
│  │ Capacity Concern│                                                        │
│  │                 │                                                        │
│  │ - resource      │                                                        │
│  │ - utilization   │                                                        │
│  │ - threshold     │                                                        │
│  │ - projection    │◄─ When limit reached                                   │
│  │ - mitigation    │                                                        │
│  └─────────────────┘                                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Entity Definitions

See [contexts/cloud-engineering.yaml](../../contexts/cloud-engineering.yaml) for the complete schema.

| Entity | Purpose | Key Attributes |
|--------|---------|----------------|
| `incident` | Production incident | incident_id, severity, impact, duration, root_cause |
| `root_cause` | Underlying cause | cause, category, contributing_factors, preventable |
| `action_item` | Follow-up action | title, owner, priority, due_date, type |
| `metric` | SLO/measurement | name, current_value, target_value, trend |
| `capacity_concern` | Resource issue | resource, utilization, threshold, projection, mitigation |

---

## ⚠️ IMPORTANT: Blameless Culture

This analysis MUST support a BLAMELESS post-mortem culture:
- Focus on **WHAT** happened, not WHO did it
- Identify systemic issues, not individual mistakes
- Look for process improvements, not blame
- Frame root causes around systems and processes

---

## Validation Criteria

| ID | Criterion | Status |
|----|-----------|--------|
| CE-AC-001 | Entity definitions cover 5 types | ✅ |
| CE-AC-002 | Severity aligns with SEV1-4 | ✅ |
| CE-AC-003 | Supports blameless post-mortem culture | ✅ |
| CE-AC-004 | Action items support SRE best practices | ✅ |
| CE-AC-005 | Encourages 5 Whys methodology | ✅ |
| CE-AC-006 | Supports SLO/SLA tracking | ✅ |
| CE-AC-007 | Output supports incident tracking | ✅ |
| CE-AC-008 | Validation criteria defined | ✅ |

---

## References

| Document | Relationship |
|----------|--------------|
| [DOMAIN-SELECTION-GUIDE.md](./DOMAIN-SELECTION-GUIDE.md) | Domain selection flowchart |
| [contexts/cloud-engineering.yaml](../../contexts/cloud-engineering.yaml) | Implementation schema |

---

*Document ID: SPEC-CE-001*
*Domain: cloud-engineering*
*Status: DESIGN COMPLETE*
