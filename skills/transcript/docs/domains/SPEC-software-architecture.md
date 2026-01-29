# Domain Specification: Software Architecture

<!--
DOCUMENT: SPEC-software-architecture.md
VERSION: 1.0.0
DOMAIN: software-architecture
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
| **Domain ID** | software-architecture |
| **Version** | 1.0.0 |
| **Status** | DESIGN COMPLETE |
| **Created** | 2026-01-27 |
| **Promoted** | 2026-01-29 (EN-014 TASK-157) |

---

## L0: Overview (ELI5)

This domain helps analyze **architecture discussion meetings** like:
- Architecture review boards ("Let's discuss the microservices approach...")
- ADR discussions ("We need to decide on the caching strategy...")
- Design sessions ("How should we structure the API layer?")

It extracts **key information** like:
- What architectural decisions were made
- What alternatives were considered
- What quality attributes (performance, security, etc.) matter most
- What technical debt was identified

---

## L1: Domain Details (Software Engineer)

### Target Users

| Role | Use Case |
|------|----------|
| Software Architects | Document decisions, alternatives |
| Principal Engineers | Track design rationale |
| Tech Leads | Understand architectural direction |
| Engineering Directors | Review strategic technical choices |

### Supported Transcript Types

| Type | Description | Typical Duration |
|------|-------------|------------------|
| Architecture Review | Formal design review | 1-2 hours |
| ADR Discussion | Decision record creation | 30-60 min |
| Design Session | Collaborative design work | 1-3 hours |
| Technical Deep Dive | Detailed exploration | 1-2 hours |
| Trade-off Analysis | Options evaluation | 1 hour |

### Key Use Cases

1. **Document ADRs** - Capture decisions in Nygard format
2. **Record Alternatives** - Document options considered but rejected
3. **Track Quality Attributes** - Identify NFR priorities
4. **Map Components** - Understand system structure
5. **Flag Technical Debt** - Identify debt and remediation plans

---

## L2: Technical Specification (Principal Architect)

### Entity Model

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   SOFTWARE ARCHITECTURE ENTITY MODEL                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌───────────────────┐         ┌───────────────────┐                       │
│  │   Architectural   │ rejected│    Alternative    │                       │
│  │     Decision      │◄────────│                   │                       │
│  │                   │         │ - title           │                       │
│  │ - title           │         │ - description     │                       │
│  │ - context         │         │ - pros            │                       │
│  │ - decision        │         │ - cons            │                       │
│  │ - consequences    │         │ - rejection_reason│                       │
│  │ - status          │         └───────────────────┘                       │
│  └─────────┬─────────┘                                                     │
│            │ addresses                                                      │
│            ▼                                                                │
│  ┌───────────────────┐                                                     │
│  │ Quality Attribute │                                                     │
│  │                   │                                                     │
│  │ - attribute       │◄──────── ISO 25010 Categories                       │
│  │ - requirement     │          (Performance, Security,                    │
│  │ - priority        │           Maintainability, etc.)                    │
│  │ - trade_offs      │                                                     │
│  └─────────┬─────────┘                                                     │
│            │ influences                                                     │
│            ▼                                                                │
│  ┌───────────────────┐         ┌───────────────────┐                       │
│  │    Component      │ incurs  │  Technical Debt   │                       │
│  │                   │────────►│                   │                       │
│  │ - name            │         │ - description     │                       │
│  │ - responsibility  │         │ - impact          │                       │
│  │ - interfaces      │         │ - remediation     │                       │
│  │ - constraints     │         │ - priority        │                       │
│  └───────────────────┘         └───────────────────┘                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Entity Definitions

See [contexts/software-architecture.yaml](../../contexts/software-architecture.yaml) for the complete schema.

| Entity | Purpose | Key Attributes |
|--------|---------|----------------|
| `architectural_decision` | Significant design choice | title, context, decision, consequences, status |
| `alternative` | Rejected option | title, description, pros, cons, rejection_reason |
| `quality_attribute` | Non-functional requirement | attribute, requirement, priority, trade_offs |
| `component` | System component | name, responsibility, interfaces, constraints |
| `technical_debt` | Design debt identified | description, impact, remediation, priority |

### Quality Attributes (ISO 25010)

| Category | Examples |
|----------|----------|
| Performance Efficiency | Response time, throughput, resource utilization |
| Security | Confidentiality, integrity, authentication |
| Maintainability | Modularity, reusability, analyzability |
| Reliability | Availability, fault tolerance, recoverability |
| Compatibility | Interoperability, co-existence |
| Usability | Learnability, operability, accessibility |
| Portability | Adaptability, installability |
| Functional Suitability | Completeness, correctness, appropriateness |

---

## Validation Criteria

| ID | Criterion | Status |
|----|-----------|--------|
| SA-AC-001 | Entity definitions cover 5 types | ✅ |
| SA-AC-002 | Each entity has ≥4 attributes | ✅ |
| SA-AC-003 | Aligns with ADR terminology (Nygard format) | ✅ |
| SA-AC-004 | Captures decision rationale and alternatives | ✅ |
| SA-AC-005 | Supports ADR generation workflow | ✅ |
| SA-AC-006 | Quality attributes cover ISO 25010 | ✅ |
| SA-AC-007 | Output supports ADR document generation | ✅ |
| SA-AC-008 | Validation criteria defined | ✅ |

---

## References

| Document | Relationship |
|----------|--------------|
| [DOMAIN-SELECTION-GUIDE.md](./DOMAIN-SELECTION-GUIDE.md) | Domain selection flowchart |
| [contexts/software-architecture.yaml](../../contexts/software-architecture.yaml) | Implementation schema |
| [Nygard ADR Format](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) | ADR standard |
| [ISO 25010](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010) | Quality model |

---

*Document ID: SPEC-SA-001*
*Domain: software-architecture*
*Status: DESIGN COMPLETE*
