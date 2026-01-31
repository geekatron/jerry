# Domain Specification: User Experience

<!--
DOCUMENT: SPEC-user-experience.md
VERSION: 1.0.0
DOMAIN: user-experience
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
| **Domain ID** | user-experience |
| **Version** | 1.0.0 |
| **Status** | DESIGN COMPLETE |
| **Created** | 2026-01-27 |
| **Promoted** | 2026-01-29 (EN-014 TASK-157) |

---

## L0: Overview (ELI5)

This domain helps analyze **UX research sessions** like:
- User interviews ("Tell me about the last time you...")
- Usability tests ("Try to find the settings page...")
- Design critiques ("The button placement feels off...")

It extracts **key information** like:
- User insights and patterns
- Pain points and frustrations
- Usability issues found during testing
- Verbatim user quotes (preserved exactly)

**CRITICAL:** This domain emphasizes preserving exact user quotes - never paraphrase!

---

## L1: Domain Details (Software Engineer)

### Target Users

| Role | Use Case |
|------|----------|
| UX Researchers | Analyze interview data |
| UX Designers | Track design feedback |
| Product Designers | Understand user needs |
| Research Ops | Build research repository |

### Supported Transcript Types

| Type | Description | Typical Duration |
|------|-------------|------------------|
| User Interview | Research conversation | 30-60 min |
| Usability Test | Task completion testing | 30-60 min |
| Design Critique | Feedback session | 30-60 min |
| Focus Group | Group discussion | 1-2 hours |
| Stakeholder Feedback | Internal design review | 30 min |

### Severity Ratings (Nielsen Norman)

| Severity | Description |
|----------|-------------|
| 0 - Cosmetic | Not a usability problem |
| 1 - Minor | Cosmetic problem only |
| 2 - Minor | Minor usability problem |
| 3 - Major | Major usability problem |
| 4 - Critical | Catastrophic - must fix |

---

## L2: Technical Specification (Principal Architect)

### Entity Model

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      USER EXPERIENCE ENTITY MODEL                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐       supports      ┌─────────────────┐               │
│  │  User Insight   │◄────────────────────│   User Quote    │               │
│  │                 │                     │                 │               │
│  │ - insight       │    ◄─VERBATIM───►   │ - quote         │               │
│  │ - participant   │                     │ - participant   │               │
│  │ - context       │                     │ - context       │               │
│  │ - confidence    │                     │ - theme         │               │
│  │ - quotes        │                     └─────────────────┘               │
│  └────────┬────────┘                                                       │
│           │                                                                 │
│           │ reveals                                                         │
│           ▼                                                                 │
│  ┌─────────────────┐                                                       │
│  │   Pain Point    │                                                       │
│  │                 │                                                       │
│  │ - description   │                                                       │
│  │ - severity      │◄──────── Nielsen Norman Scale                         │
│  │ - frequency     │                                                       │
│  │ - user_quote    │                                                       │
│  └────────┬────────┘                                                       │
│           │                                                                 │
│           │ manifests_as                                                    │
│           ▼                                                                 │
│  ┌─────────────────┐      triggers      ┌─────────────────┐               │
│  │ Usability Issue │────────────────────►│ Design Feedback │               │
│  │                 │                     │                 │               │
│  │ - task          │                     │ - artifact      │               │
│  │ - issue         │                     │ - feedback_type │               │
│  │ - severity      │                     │ - feedback      │               │
│  │ - recommendation│                     │ - action        │               │
│  └─────────────────┘                     └─────────────────┘               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Entity Definitions

See [contexts/user-experience.yaml](../../contexts/user-experience.yaml) for the complete schema.

| Entity | Purpose | Key Attributes |
|--------|---------|----------------|
| `user_insight` | Key research learning | insight, participant, context, confidence, supporting_quotes |
| `pain_point` | User frustration | description, severity, frequency, user_quote |
| `usability_issue` | Testing problem | task, issue, severity, recommendation |
| `design_feedback` | Critique input | artifact, feedback_type, feedback, action |
| `user_quote` | Verbatim statement | quote, participant, context, theme |

---

## ⚠️ CRITICAL: Verbatim Quote Preservation

**DO NOT paraphrase, summarize, or clean up user quotes.**

User quotes must be preserved EXACTLY as spoken, including:
- Filler words ("um", "like", "you know")
- Grammatical errors
- Incomplete sentences
- Colloquialisms
- [inaudible] for unclear speech
- [laughter] for non-verbal cues

This is ESSENTIAL for research validity.

---

## Validation Criteria

| ID | Criterion | Status |
|----|-----------|--------|
| UX-AC-001 | Entity definitions cover 5 types | ✅ |
| UX-AC-002 | Severity aligns with Nielsen Norman ratings | ✅ |
| UX-AC-003 | Extraction preserves verbatim quotes | ✅ |
| UX-AC-004 | Supports affinity diagramming workflow | ✅ |
| UX-AC-005 | Emphasizes quote preservation | ✅ |
| UX-AC-006 | Handles participant anonymization | ✅ |
| UX-AC-007 | Output supports research repository | ✅ |
| UX-AC-008 | Validation criteria defined | ✅ |

---

## References

| Document | Relationship |
|----------|--------------|
| [DOMAIN-SELECTION-GUIDE.md](./DOMAIN-SELECTION-GUIDE.md) | Domain selection flowchart |
| [contexts/user-experience.yaml](../../contexts/user-experience.yaml) | Implementation schema |

---

*Document ID: SPEC-UX-001*
*Domain: user-experience*
*Status: DESIGN COMPLETE*
