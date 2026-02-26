# PROJ-006: Work Tracker Ontology - Orchestration Plan

> **Project ID:** PROJ-006-worktracker-ontology
> **Status:** IN PROGRESS
> **Version:** 2.0
> **Created:** 2026-01-13
> **Last Updated:** 2026-01-13
> **Approval Status:** APPROVED (Phase 1-3 executed; Phase 4+ pending)

---

## Executive Summary

This orchestration plan defines a multi-phase research and design effort to reverse-engineer a unified **Work Tracker Ontology** from three major project management domains: **ADO Scrum**, **SAFe**, and **JIRA**.

### End Goal

Create a **parent ontology** with:
1. Domain entities (properties and behaviors)
2. Relationships between entities
3. State transitions (workflow state machines)
4. Markdown templates for a Claude Code Skill

### Key Amendment (v2.0): Critic Loop Architecture

**Discovery:** During SYNC BARRIER 3, we identified the need for automated quality feedback loops before human approval gates. This amendment adds **critic loops** at each sync barrier to validate producer outputs before human review.

---

## Solution Epic: SE-001 - Work Tracker Domain Understanding

### Problem Statement

Work tracking systems (ADO, JIRA, SAFe implementations) have overlapping but inconsistent domain models. To build a universal Claude Code skill for work tracking, we need a **canonical ontology** that:
- Abstracts common patterns across systems
- Maps to system-specific implementations
- Provides templates for AI-assisted work management

### Success Criteria

- [x] Complete domain models for ADO Scrum, SAFe, and JIRA
- [x] Cross-domain synthesis identifying common patterns (EN-004)
- [ ] **Critic review of synthesis artifact (CL-003)** ← NEW
- [ ] Parent ontology design with mapping rules
- [ ] **Critic review of ontology design (CL-004)** ← NEW
- [ ] Markdown templates ready for skill integration
- [ ] All artifacts reviewed and approved (WI-003)

---

## Feature: FT-001 - Domain Discovery

### Enablers

| ID | Name | Dependencies | Agent(s) | Status | Critic |
|----|------|--------------|----------|--------|--------|
| EN-001 | ADO Scrum Domain Analysis | None | ps-researcher, ps-analyst | COMPLETED | SKIPPED |
| EN-002 | SAFe Domain Analysis | None | ps-researcher, ps-analyst | COMPLETED | SKIPPED |
| EN-003 | JIRA Domain Analysis | None | ps-researcher, ps-analyst | COMPLETED | SKIPPED |
| EN-004 | Cross-Domain Synthesis | EN-001, EN-002, EN-003 | ps-synthesizer | COMPLETED | **PENDING (CL-003)** |

### Work Items

| ID | Name | Dependencies | Agent(s) | Status | Critic |
|----|------|--------------|----------|--------|--------|
| WI-001 | Parent Ontology Design | EN-004, CL-003 | nse-architecture, ps-architect | BLOCKED | CL-004 |
| WI-002 | Markdown Template Generation | WI-001, CL-004 | ps-synthesizer | BLOCKED | CL-005 |
| WI-003 | Design Review & Validation | WI-002, CL-005 | nse-reviews | BLOCKED | (final gate) |

### Critic Loops (NEW)

| ID | Reviews | Critic Agent(s) | Status | Artifact |
|----|---------|-----------------|--------|----------|
| CL-003 | EN-004 (Synthesis) | ps-reviewer, nse-reviews | PENDING | `reviews/CL-003-synthesis-review.md` |
| CL-004 | WI-001 (Ontology) | ps-architect, nse-reviews | PENDING | `reviews/CL-004-ontology-review.md` |
| CL-005 | WI-002 (Templates) | ps-reviewer | PENDING | `reviews/CL-005-templates-review.md` |

---

## Critic Loop Architecture (NEW - v2.0)

### Purpose

Critic loops provide automated quality feedback before human approval gates. They:
- Pre-validate producer outputs against acceptance criteria
- Catch errors before they propagate to downstream phases
- Reduce human review burden by surfacing issues early
- Enable iterative refinement through loop-back mechanisms

### Critic Loop Pattern

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CRITIC LOOP PATTERN                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│     ┌─────────────┐         ┌─────────────┐         ┌─────────────┐        │
│     │  PRODUCER   │────────▶│   CRITIC    │────────▶│  DECISION   │        │
│     │   Agent     │         │   Agent     │         │   Gate      │        │
│     └─────────────┘         └──────┬──────┘         └──────┬──────┘        │
│                                    │                       │               │
│                                    ▼                       │               │
│                           ┌───────────────┐                │               │
│                           │ Review Artifact│                │               │
│                           │ - Criteria     │                │               │
│                           │ - Findings     │                │               │
│                           │ - Decision     │                │               │
│                           └───────────────┘                │               │
│                                                            │               │
│     ┌──────────────────────────────────────────────────────┘               │
│     │                                                                       │
│     ▼                                                                       │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────┐                      │
│  │ APPROVE  │    │  REVISE  │    │ DOCUMENT-PROCEED │                      │
│  │          │    │          │    │                  │                      │
│  │ No issues│    │ Critical │    │ Minor issues     │                      │
│  │ Proceed  │    │ Loop back│    │ Note and proceed │                      │
│  └────┬─────┘    └────┬─────┘    └────────┬─────────┘                      │
│       │               │                   │                                 │
│       │               │    ┌──────────────┘                                 │
│       │               │    │                                                │
│       │               ▼    ▼                                                │
│       │         ┌──────────────┐                                            │
│       │         │ HUMAN GATE   │                                            │
│       │         │ Final Approve│                                            │
│       │         └──────┬───────┘                                            │
│       │                │                                                    │
│       └────────────────┼─────────────────────────────────▶ NEXT PHASE      │
│                        │                                                    │
│                        └─────────────────────────────────▶ NEXT PHASE      │
│                                                                             │
│     ◄──────────────────┬───────────────────────────────────────────────    │
│                        │                                                    │
│                   LOOP BACK                                                 │
│               (max 2 iterations)                                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Critic Types

| Type | Purpose | Criteria | Used At |
|------|---------|----------|---------|
| **Lightweight** | Quick consistency check after parallel phases | consistency, completeness | SYNC-1, SYNC-2 (retroactive: skipped) |
| **Full** | Comprehensive review of synthesis/design | completeness, accuracy, consistency, coverage, traceability | SYNC-3, SYNC-4, SYNC-5 |

### Criteria Definitions

| Criterion | Weight | Description | Evidence Required |
|-----------|--------|-------------|-------------------|
| **Completeness** | High | All required elements present | Checklist against spec |
| **Accuracy** | Critical | Mappings/definitions correct | Source citations |
| **Consistency** | High | No contradictions | Cross-reference check |
| **Coverage** | Medium | All scope items addressed | Gap analysis |
| **Traceability** | Medium | Links to sources maintained | Citation audit |

### Decision Rules

| Decision | Condition | Action | Human Gate |
|----------|-----------|--------|------------|
| **APPROVE** | No critical or major findings | Proceed to next phase | Required |
| **REVISE** | Critical findings present | Loop back to producer (max 2) | After revision |
| **DOCUMENT-PROCEED** | Only minor findings | Document and proceed | Required |
| **ESCALATE** | Max iterations reached | Human decision required | Mandatory |

### Agent Assignments

| Phase | Producer Agent | Critic Primary | Critic Secondary | Escalation |
|-------|----------------|----------------|------------------|------------|
| Phase 1-2 | ps-researcher, ps-analyst | ps-reviewer | - | nse-qa |
| Phase 3 (EN-004) | ps-synthesizer | **ps-reviewer** | **nse-reviews** | Human |
| Phase 4 (WI-001) | nse-architecture | **ps-architect** | **nse-reviews** | Human |
| Phase 5 (WI-002) | ps-synthesizer | **ps-reviewer** | - | nse-qa |
| Phase 6 (WI-003) | nse-reviews | Human | - | N/A |

---

## Orchestration Architecture

### Pipeline Visualization (Updated v2.0)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PHASE 1: PARALLEL RESEARCH                        │
│                               STATUS: COMPLETED                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐                │
│  │  Stream A   │      │  Stream B   │      │  Stream C   │                │
│  │  ADO Scrum  │      │    SAFe     │      │    JIRA     │                │
│  │             │      │             │      │             │                │
│  │ ps-research │      │ ps-research │      │ ps-research │                │
│  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘                │
│         │                    │                    │                        │
│         ▼                    ▼                    ▼                        │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐                │
│  │ ADO-RAW.md  │      │ SAFE-RAW.md │      │ JIRA-RAW.md │                │
│  │     ✓       │      │     ✓       │      │     ✓       │                │
│  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘                │
│         │                    │                    │                        │
└─────────┼────────────────────┼────────────────────┼────────────────────────┘
          │                    │                    │
          ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PHASE 2: PARALLEL ANALYSIS                        │
│                               STATUS: COMPLETED                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐                │
│  │  Stream A   │      │  Stream B   │      │  Stream C   │                │
│  │  ADO Model  │      │  SAFe Model │      │  JIRA Model │                │
│  │             │      │             │      │             │                │
│  │ ps-analyst  │      │ ps-analyst  │      │ ps-analyst  │                │
│  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘                │
│         │                    │                    │                        │
│         ▼                    ▼                    ▼                        │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐                │
│  │ADO-MODEL.md │      │SAFE-MODEL.md│      │JIRA-MODEL.md│                │
│  │     ✓       │      │     ✓       │      │     ✓       │                │
│  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘                │
│         │                    │                    │                        │
└─────────┼────────────────────┼────────────────────┼────────────────────────┘
          │                    │                    │
          └────────────────────┼────────────────────┘
                               │
                ╔══════════════╧══════════════╗
                ║      SYNC BARRIER 1         ║
                ║   All 3 models ready        ║
                ║   Critic: SKIPPED (retro)   ║
                ║   Status: ✓ PASSED          ║
                ╚══════════════╤══════════════╝
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PHASE 3: CROSS-DOMAIN SYNTHESIS                      │
│                               STATUS: COMPLETED                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                         ┌─────────────────┐                                │
│                         │  ps-synthesizer │                                │
│                         │     EN-004      │                                │
│                         │       ✓         │                                │
│                         └────────┬────────┘                                │
│                                  │                                          │
│                                  ▼                                          │
│                         ┌─────────────────┐                                │
│                         │ SYNTHESIS.md    │                                │
│                         │ - 9 entities    │                                │
│                         │ - 15 properties │                                │
│                         │ - 4 rel types   │                                │
│                         │ - 7 states      │                                │
│                         │       ✓         │                                │
│                         └────────┬────────┘                                │
│                                  │                                          │
└──────────────────────────────────┼──────────────────────────────────────────┘
                                   │
                ╔══════════════════╧══════════════════╗
                ║         SYNC BARRIER 3              ║
                ║      Synthesis complete             ║
                ╠═════════════════════════════════════╣
                ║                                     ║
                ║  ┌─────────────────────────────┐   ║
                ║  │      CRITIC LOOP CL-003     │   ║
                ║  │                             │   ║
                ║  │  Primary: ps-reviewer       │   ║
                ║  │  Secondary: nse-reviews     │   ║◄────┐
                ║  │  Status: *** PENDING ***    │   ║     │
                ║  │                             │   ║     │
                ║  │  Criteria:                  │   ║     │ Loop
                ║  │  - Completeness             │   ║     │ (max 2)
                ║  │  - Accuracy                 │   ║     │
                ║  │  - Consistency              │   ║     │
                ║  │  - Coverage                 │   ║     │
                ║  │                             │   ║     │
                ║  │  Output:                    │   ║     │
                ║  │  reviews/CL-003-synthesis-  │   ║     │
                ║  │  review.md                  │   ║     │
                ║  └──────────────┬──────────────┘   ║     │
                ║                 │                  ║     │
                ║                 ▼                  ║     │
                ║  ┌──────────────────────────────┐  ║     │
                ║  │         DECISION             │  ║     │
                ║  │  APPROVE | REVISE | DOC-PROC │──╫─────┘
                ║  └──────────────┬───────────────┘  ║
                ║                 │                  ║
                ║                 ▼                  ║
                ║  ┌──────────────────────────────┐  ║
                ║  │       HUMAN APPROVAL         │  ║
                ║  │       *** PENDING ***        │  ║
                ║  └──────────────┬───────────────┘  ║
                ║                 │                  ║
                ╚═════════════════╧══════════════════╝
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PHASE 4: ONTOLOGY DESIGN                            │
│                               STATUS: BLOCKED                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│         ┌─────────────────┐              ┌─────────────────┐               │
│         │ nse-architecture│              │   ps-architect  │               │
│         │     WI-001      │              │   (validator)   │               │
│         │                 │              │                 │               │
│         │ Entity design   │─────────────▶│ Validate design │               │
│         │ Relationships   │              │ Check patterns  │               │
│         │ State machines  │              │                 │               │
│         └────────┬────────┘              └─────────────────┘               │
│                  │                                                          │
│                  ▼                                                          │
│         ┌─────────────────┐              ┌─────────────────┐               │
│         │ ONTOLOGY-v1.md  │              │ ADR-001.md      │               │
│         │ - Entities      │              │ Design decisions│               │
│         │ - Properties    │              │                 │               │
│         │ - Behaviors     │              │                 │               │
│         │ - Relationships │              │                 │               │
│         │ - State machines│              │                 │               │
│         └────────┬────────┘              └─────────────────┘               │
│                  │                                                          │
└──────────────────┼──────────────────────────────────────────────────────────┘
                   │
                ╔══╧══════════════════════════════════╗
                ║         SYNC BARRIER 4 (NEW)        ║
                ║        Ontology approved            ║
                ╠═════════════════════════════════════╣
                ║                                     ║
                ║  ┌─────────────────────────────┐   ║
                ║  │      CRITIC LOOP CL-004     │   ║
                ║  │                             │   ║
                ║  │  Primary: ps-architect      │   ║◄────┐
                ║  │  Secondary: nse-reviews     │   ║     │
                ║  │  Status: BLOCKED            │   ║     │ Loop
                ║  │                             │   ║     │
                ║  │  Output:                    │   ║     │
                ║  │  reviews/CL-004-ontology-   │   ║     │
                ║  │  review.md                  │   ║     │
                ║  └──────────────┬──────────────┘   ║     │
                ║                 │                  ║     │
                ║                 ▼                  ║     │
                ║  ┌──────────────────────────────┐  ║     │
                ║  │         DECISION             │──╫─────┘
                ║  └──────────────┬───────────────┘  ║
                ║                 │                  ║
                ║                 ▼                  ║
                ║  ┌──────────────────────────────┐  ║
                ║  │       HUMAN APPROVAL         │  ║
                ║  └──────────────┬───────────────┘  ║
                ║                 │                  ║
                ╚═════════════════╧══════════════════╝
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PHASE 5: TEMPLATE GENERATION                          │
│                               STATUS: BLOCKED                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                         ┌─────────────────┐                                │
│                         │  ps-synthesizer │                                │
│                         │     WI-002      │                                │
│                         │                 │                                │
│                         │ Generate MD     │                                │
│                         │ templates       │                                │
│                         └────────┬────────┘                                │
│                                  │                                          │
│                                  ▼                                          │
│         ┌────────────────────────┴────────────────────────┐                │
│         │                   TEMPLATES/                     │                │
│         │  ┌──────────────┐ ┌──────────────┐ ┌──────────┐ │                │
│         │  │ EPIC.md      │ │ FEATURE.md   │ │ STORY.md │ │                │
│         │  └──────────────┘ └──────────────┘ └──────────┘ │                │
│         │  ┌──────────────┐ ┌──────────────┐ ┌──────────┐ │                │
│         │  │ TASK.md      │ │ BUG.md       │ │ SPIKE.md │ │                │
│         │  └──────────────┘ └──────────────┘ └──────────┘ │                │
│         └─────────────────────────────────────────────────┘                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                ╔══════════════════╧══════════════════╗
                ║         SYNC BARRIER 5 (NEW)        ║
                ║        Templates ready              ║
                ╠═════════════════════════════════════╣
                ║                                     ║
                ║  ┌─────────────────────────────┐   ║
                ║  │      CRITIC LOOP CL-005     │   ║
                ║  │                             │   ║
                ║  │  Primary: ps-reviewer       │   ║◄────┐
                ║  │  Status: BLOCKED            │   ║     │ Loop
                ║  │                             │   ║     │
                ║  │  Output:                    │   ║     │
                ║  │  reviews/CL-005-templates-  │   ║     │
                ║  │  review.md                  │   ║     │
                ║  └──────────────┬──────────────┘   ║     │
                ║                 │                  ║     │
                ║                 ▼                  ║     │
                ║  ┌──────────────────────────────┐  ║     │
                ║  │         DECISION             │──╫─────┘
                ║  └──────────────┬───────────────┘  ║
                ║                 │                  ║
                ╚═════════════════╧══════════════════╝
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PHASE 6: REVIEW & VALIDATION                          │
│                               STATUS: BLOCKED                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                        ┌─────────────────┐                                 │
│                        │   nse-reviews   │                                 │
│                        │     WI-003      │                                 │
│                        │                 │                                 │
│                        │ Final validation│                                 │
│                        │ Quality gate    │                                 │
│                        └────────┬────────┘                                 │
│                                 │                                           │
│                                 ▼                                           │
│                        ┌─────────────────┐                                 │
│                        │  HUMAN FINAL    │                                 │
│                        │    APPROVAL     │                                 │
│                        └────────┬────────┘                                 │
│                                 │                                           │
│                                 ▼                                           │
│                        ┌─────────────────┐                                 │
│                        │    COMPLETE     │                                 │
│                        └─────────────────┘                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Detailed Phase Breakdown

### Phase 1: Parallel Research (EN-001, EN-002, EN-003) - COMPLETED

**Status:** ✓ COMPLETED
**Agent:** ps-researcher (3 instances)
**Critic:** SKIPPED (retroactive - infrastructure added after execution)

#### Stream A: ADO Scrum Research (EN-001-T1)

**Research Questions:**
1. What work item types exist in ADO Scrum? (Epic, Feature, User Story, Task, Bug, etc.)
2. What properties does each work item type have?
3. What are the default states and transitions?
4. How are work items related (parent-child, links)?
5. What behaviors/operations are supported?

**Sources to Consult:**
- Microsoft Azure DevOps documentation
- ADO REST API reference
- Scrum process template documentation

**Output:** `research/ADO-SCRUM-RAW.md` ✓

#### Stream B: SAFe Research (EN-002-T1)

**Research Questions:**
1. What are the SAFe hierarchy levels? (Portfolio, Program, Team)
2. What work item types exist at each level?
3. What properties are defined for each type?
4. How do items relate across levels?
5. What are the PI (Program Increment) concepts?

**Sources to Consult:**
- Scaled Agile Framework official documentation
- SAFe Big Picture
- SAFe Glossary

**Output:** `research/SAFE-RAW.md` ✓

#### Stream C: JIRA Research (EN-003-T1)

**Research Questions:**
1. What issue types exist in JIRA? (Epic, Story, Task, Bug, Sub-task, etc.)
2. What are the standard and custom fields?
3. What workflow states and transitions exist?
4. How are issues linked (blocks, is blocked by, relates to)?
5. What is the hierarchy (Epic → Story → Sub-task)?

**Sources to Consult:**
- Atlassian JIRA documentation
- JIRA REST API reference
- JIRA Cloud vs Server differences

**Output:** `research/JIRA-RAW.md` ✓

---

### Phase 2: Parallel Analysis (EN-001, EN-002, EN-003) - COMPLETED

**Status:** ✓ COMPLETED
**Agent:** ps-analyst (3 instances)
**Critic:** SKIPPED (retroactive)

#### Analysis Template (Applied to Each Domain)

For each domain, extract:

```markdown
## Domain Model: {SYSTEM}

### 1. Entity Catalog

| Entity | Description | Level |
|--------|-------------|-------|
| Epic | Large body of work | Portfolio |
| ... | ... | ... |

### 2. Entity Properties

#### {Entity Name}
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| id | string | yes | Unique identifier |
| title | string | yes | Display name |
| ... | ... | ... | ... |

### 3. Entity Behaviors

| Entity | Behavior | Description | Preconditions |
|--------|----------|-------------|---------------|
| Story | create | Create new story | Valid parent |
| Story | transition | Change state | Valid transition |
| ... | ... | ... | ... |

### 4. Relationships

| From | Relationship | To | Cardinality |
|------|--------------|----|-----------:|
| Epic | contains | Feature | 1:N |
| Feature | contains | Story | 1:N |
| ... | ... | ... | ... |

### 5. State Machine

#### {Entity Name} States

```
[New] → [Active] → [Resolved] → [Closed]
         ↓    ↑
       [Blocked]
```

| From State | To State | Trigger | Guards |
|------------|----------|---------|--------|
| New | Active | Start work | Assigned |
| ... | ... | ... | ... |
```

**Outputs:**
- `analysis/ADO-SCRUM-MODEL.md` ✓
- `analysis/SAFE-MODEL.md` ✓
- `analysis/JIRA-MODEL.md` ✓

---

### Phase 3: Cross-Domain Synthesis (EN-004) - COMPLETED, PENDING CRITIC

**Status:** ✓ COMPLETED (awaiting CL-003 critic review)
**Agent:** ps-synthesizer
**Critic:** CL-003 - **PENDING**

#### Synthesis Tasks (All Completed)

1. **Entity Alignment Matrix** ✓
   - Map equivalent entities across systems
   - Identify system-specific entities
   - Propose canonical names
   - **Result:** 9 canonical entities identified

2. **Property Alignment Matrix** ✓
   - Map equivalent properties
   - Identify required vs optional
   - Propose canonical property names
   - **Result:** 9 core + 6 extended properties

3. **Relationship Pattern Analysis** ✓
   - Identify common relationship types
   - Abstract to canonical relationships
   - Document semantic differences
   - **Result:** 4 relationship categories

4. **State Machine Comparison** ✓
   - Compare workflow states
   - Identify common transitions
   - Propose canonical state machine
   - **Result:** 7 canonical states

**Output:** `synthesis/CROSS-DOMAIN-SYNTHESIS.md` ✓

#### Critic Review (CL-003) - PENDING

**Artifact to Review:** `synthesis/CROSS-DOMAIN-SYNTHESIS.md`

**Validation Sources:**
- `analysis/ADO-SCRUM-MODEL.md`
- `analysis/SAFE-MODEL.md`
- `analysis/JIRA-MODEL.md`

**Criteria:**
| Criterion | Weight | Check |
|-----------|--------|-------|
| Completeness | High | All entities from source models mapped |
| Accuracy | Critical | Mappings reflect source semantics |
| Consistency | High | No contradictions in canonical definitions |
| Coverage | Medium | All properties, relationships, states addressed |

**Output:** `reviews/CL-003-synthesis-review.md`

**Decision Options:**
- APPROVE → Proceed to Phase 4
- REVISE → Loop back to EN-004 (max 2 iterations)
- DOCUMENT-PROCEED → Note minor issues and proceed

---

### Phase 4: Ontology Design (WI-001) - BLOCKED

**Status:** BLOCKED (awaiting CL-003 approval)
**Agents:** nse-architecture, ps-architect
**Critic:** CL-004

#### Design Tasks

1. **Entity Schema Design**
   - Define canonical entity types
   - Define inheritance hierarchy
   - Define required/optional properties

2. **Relationship Schema Design**
   - Define relationship types
   - Define cardinality rules
   - Define constraint rules

3. **State Machine Design**
   - Define canonical states
   - Define valid transitions
   - Define guard conditions

4. **Mapping Rules Design**
   - Define ADO → Canonical mappings
   - Define SAFe → Canonical mappings
   - Define JIRA → Canonical mappings

**Outputs:**
- `synthesis/ONTOLOGY-v1.md`
- `decisions/ADR-001-ontology-design.md`

---

### Phase 5: Template Generation (WI-002) - BLOCKED

**Status:** BLOCKED (awaiting Phase 4 + CL-004)
**Agent:** ps-synthesizer
**Critic:** CL-005

#### Template Requirements

Each template must include:
1. YAML frontmatter (machine-readable metadata)
2. Human-readable sections
3. Placeholders for dynamic content
4. Relationship references
5. State indicators

#### Template List

| Template | Entity Type | Priority |
|----------|-------------|----------|
| EPIC.md | Epic | P1 |
| FEATURE.md | Feature | P1 |
| STORY.md | Story | P1 |
| TASK.md | Task | P1 |
| BUG.md | Bug | P1 |
| SPIKE.md | Spike | P2 |
| ENABLER.md | Enabler | P2 |

**Output:** `templates/` directory with all templates

---

### Phase 6: Review & Validation (WI-003) - BLOCKED

**Status:** BLOCKED (awaiting Phase 5 + CL-005)
**Agent:** nse-reviews
**Final Gate:** Human approval required

This phase serves as the final quality gate. WI-003 is itself a comprehensive review, so no additional critic loop is needed.

---

## Execution Schedule (Updated v2.0)

| Phase | Parallelism | Dependencies | Status | Critic |
|-------|-------------|--------------|--------|--------|
| Phase 1 | 3 parallel | None | ✓ COMPLETED | SKIPPED |
| Phase 2 | 3 parallel | Phase 1 | ✓ COMPLETED | SKIPPED |
| Phase 3 | Sequential | SYNC-1 | ✓ COMPLETED | **CL-003 PENDING** |
| Phase 4 | Sequential | SYNC-3 + CL-003 | BLOCKED | CL-004 |
| Phase 5 | Sequential | SYNC-4 + CL-004 | BLOCKED | CL-005 |
| Phase 6 | Sequential | SYNC-5 + CL-005 | BLOCKED | (final gate) |

**Total Steps:** 10 major tasks + 3 critic reviews

---

## Review Artifact Template

All critic reviews produce a standardized artifact:

```markdown
# Review: {CL-ID} {Artifact Name}

> **Review ID:** {CL-ID}
> **Artifact:** {path/to/artifact.md}
> **Critic:** {primary agent} (primary), {secondary agent} (secondary)
> **Date:** {date}
> **Iteration:** {n}/{max}
> **Status:** PENDING | APPROVED | REVISE | DOCUMENT-PROCEED

---

## Criteria Assessment

| Criterion | Weight | Score | Evidence |
|-----------|--------|-------|----------|
| Completeness | High | PASS/WARN/FAIL | {evidence} |
| Accuracy | Critical | PASS/WARN/FAIL | {evidence} |
| Consistency | High | PASS/WARN/FAIL | {evidence} |
| Coverage | Medium | PASS/WARN/FAIL | {evidence} |

---

## Findings

### Critical (blocks approval)
{numbered list or "none"}

### Major (require revision before proceed)
{numbered list or "none"}

### Minor (document and proceed)
{numbered list or "none"}

---

## Decision

**{APPROVE | REVISE | DOCUMENT-PROCEED}**

Rationale: {explanation}

---

## Traceability

| Source | Section | Verified |
|--------|---------|----------|
| {source} | {section} | ✓/✗ |

---

## Sign-off

- **Critic (primary):** {decision}
- **Critic (secondary):** {decision}
- **Human:** PENDING
```

---

## Risk Assessment (Updated v2.0)

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Incomplete documentation | High | Medium | Use multiple sources |
| Domain ambiguity | Medium | High | Document assumptions |
| Scope creep | High | Medium | Strict phase gates |
| Template complexity | Medium | Low | Iterative refinement |
| **Critic loop delays** | Medium | Medium | **Time-box reviews (30m)** |
| **Infinite revision loops** | High | Low | **Max 2 iterations + escalation** |

---

## Approval Checklist (Updated v2.0)

Before execution, confirm:

- [x] Solution Epic scope is correct
- [x] Feature breakdown is appropriate
- [x] Agent assignments are optimal
- [x] Sync barriers are well-placed
- [x] Output formats are acceptable
- [x] Risk mitigations are adequate
- [x] **Critic loop architecture defined** ← NEW
- [x] **Review artifact template defined** ← NEW
- [x] **Escalation rules defined** ← NEW

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-01-13 | Initial plan | Claude |
| 2.0 | 2026-01-13 | Added critic loop architecture; Updated pipeline; Added SYNC-4, SYNC-5; Added review template | Claude |

---

## Approval Status

**Version 1.0:** APPROVED (2026-01-13) - Phases 1-3 executed
**Version 2.0:** APPROVED (2026-01-13) - Critic loops added; CL-003 pending execution

---

*Plan Version: 2.0*
*Last Updated: 2026-01-13*
*Status: IN PROGRESS - Awaiting CL-003 critic review*
