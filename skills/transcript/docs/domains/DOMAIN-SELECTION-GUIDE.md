# Domain Selection Guide

<!--
DOCUMENT: DOMAIN-SELECTION-GUIDE.md
VERSION: 1.0.0
SOURCE: EN-006 Context Injection Design (TASK-038)
PROMOTED: EN-014 Domain Context Files (TASK-157)
STATUS: COMPLETE
-->

---

## Overview

This guide helps you select the appropriate domain context for transcript analysis. Each domain provides specialized entity extraction, pattern recognition, and prompt guidance tailored to specific professional contexts.

---

## Domain Selection Flowchart

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DOMAIN SELECTION FLOWCHART                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  What type of meeting are you analyzing?                                     │
│                                                                              │
│  ┌─────────────────────────┐                                                │
│  │ Daily standup?          │─────────────────────► software-engineering     │
│  │ Sprint planning?        │                                                │
│  │ Code review?            │                                                │
│  └─────────────────────────┘                                                │
│                                                                              │
│  ┌─────────────────────────┐                                                │
│  │ Architecture review?    │─────────────────────► software-architecture    │
│  │ ADR discussion?         │                                                │
│  │ Design session?         │                                                │
│  └─────────────────────────┘                                                │
│                                                                              │
│  ┌─────────────────────────┐                                                │
│  │ Product strategy?       │─────────────────────► product-management       │
│  │ Roadmap planning?       │                                                │
│  │ Stakeholder meeting?    │                                                │
│  └─────────────────────────┘                                                │
│                                                                              │
│  ┌─────────────────────────┐                                                │
│  │ User interview?         │─────────────────────► user-experience          │
│  │ Usability testing?      │                                                │
│  │ Design critique?        │                                                │
│  └─────────────────────────┘                                                │
│                                                                              │
│  ┌─────────────────────────┐                                                │
│  │ Incident post-mortem?   │─────────────────────► cloud-engineering        │
│  │ Capacity planning?      │                                                │
│  │ Infrastructure review?  │                                                │
│  └─────────────────────────┘                                                │
│                                                                              │
│  ┌─────────────────────────┐                                                │
│  │ Security audit?         │─────────────────────► security-engineering     │
│  │ Threat modeling?        │                                                │
│  │ Compliance review?      │                                                │
│  └─────────────────────────┘                                                │
│                                                                              │
│  ┌─────────────────────────┐                                                │
│  │ General meeting?        │─────────────────────► meeting (or general)     │
│  │ Unknown context?        │                                                │
│  └─────────────────────────┘                                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Available Domains

| # | Domain | Context File | Target Users | Key Use Cases |
|---|--------|--------------|--------------|---------------|
| 1 | [general](SPEC-general.md) | `contexts/general.yaml` | All users | Baseline extraction |
| 2 | [transcript](../../contexts/transcript.yaml) | `contexts/transcript.yaml` | All users | Base transcript entities |
| 3 | [meeting](../../contexts/meeting.yaml) | `contexts/meeting.yaml` | All users | Generic meetings |
| 4 | [software-engineering](SPEC-software-engineering.md) | `contexts/software-engineering.yaml` | Engineers, Tech Leads | Standups, sprint planning |
| 5 | [software-architecture](SPEC-software-architecture.md) | `contexts/software-architecture.yaml` | Architects | ADR discussions, design |
| 6 | [product-management](SPEC-product-management.md) | `contexts/product-management.yaml` | PMs, Product Owners | Roadmap, prioritization |
| 7 | [user-experience](SPEC-user-experience.md) | `contexts/user-experience.yaml` | UX Researchers | Research interviews |
| 8 | [cloud-engineering](SPEC-cloud-engineering.md) | `contexts/cloud-engineering.yaml` | SREs, DevOps | Post-mortems, capacity |
| 9 | [security-engineering](SPEC-security-engineering.md) | `contexts/security-engineering.yaml` | Security Engineers | Audits, threat modeling |

---

## Domain Comparison Matrix

| Feature | general | meeting | sw-eng | sw-arch | pm | ux | cloud | security |
|---------|---------|---------|--------|---------|----|----|-------|----------|
| Speakers | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Topics | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Questions | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Action Items | - | ✅ | ✅ | - | - | - | ✅ | - |
| Decisions | - | ✅ | ✅ | ✅ | - | - | - | ✅ |
| Commitments | - | - | ✅ | - | - | - | - | - |
| Blockers | - | - | ✅ | - | - | - | - | - |
| ADRs | - | - | - | ✅ | - | - | - | - |
| Quality Attributes | - | - | - | ✅ | - | - | - | - |
| Feature Requests | - | - | - | - | ✅ | - | - | - |
| User Needs | - | - | - | - | ✅ | ✅ | - | - |
| Verbatim Quotes | - | - | - | - | - | ✅ | - | - |
| Pain Points | - | - | - | - | - | ✅ | - | - |
| Incidents | - | - | - | - | - | - | ✅ | - |
| Root Causes | - | - | - | - | - | - | ✅ | - |
| Vulnerabilities | - | - | - | - | - | - | - | ✅ |
| Threats (STRIDE) | - | - | - | - | - | - | - | ✅ |

---

## Special Considerations

### User Experience Domain

**CRITICAL: Verbatim Quote Preservation**

The UX domain requires that user quotes be preserved **exactly as spoken**, including:
- Filler words ("um", "like", "you know")
- Grammatical errors
- Incomplete sentences
- [inaudible] and [laughter] markers

This is essential for research validity.

### Cloud Engineering Domain

**CRITICAL: Blameless Culture**

The cloud-engineering domain enforces **blameless post-mortem culture**:
- Focus on WHAT happened, not WHO
- Identify systemic issues, not individual mistakes
- Frame root causes around systems and processes

### Security Engineering Domain

**CRITICAL: Risk Acceptance Documentation**

Risk acceptance decisions must include:
- Topic being accepted
- Approver name and role
- Expiry date for re-review

This is required for audit compliance.

---

## Usage Example

```yaml
# In SKILL.md invocation or agent configuration
context_injection:
  domain: "software-engineering"
  context_file: "contexts/software-engineering.yaml"
  transcript_type: "daily_standup"
```

---

## References

| Document | Description |
|----------|-------------|
| [SKILL.md](../../SKILL.md) | Transcript skill orchestrator |
| [TDD-EN014](../../../projects/.../EN-014-domain-context-files/docs/TDD-EN014-domain-context-files.md) | Technical design document |

---

*Document ID: DOMAIN-SELECTION-GUIDE*
*Version: 1.0.0*
*Promoted: 2026-01-29 (EN-014 TASK-157)*
