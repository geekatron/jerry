# UoW-001: Demo Planning and Execution

> **Unit of Work ID:** UoW-001
> **Feature:** [FT-001](./FEATURE-WORKTRACKER.md) CPO Demo and Stakeholder Presentation
> **Solution Epic:** [SE-003](../SOLUTION-WORKTRACKER.md)
> **Status:** IN PROGRESS
> **Created:** 2026-01-14
> **Last Updated:** 2026-01-14

---

## Problem Statement

**Problem:** We need to demonstrate Jerry Framework's capabilities to executive and technical leadership (CPO Phil Calvin, Senior Principal SDE) to secure buy-in and showcase the framework's value proposition.

**Challenge:** Creating a demo that works for both strategic/executive audiences AND technical architects requires multi-level content (ELI5 through L2) with appropriate depth at each level.

**Constraints:**
- CPO time is limited - must be concise yet compelling
- Former Principal Architect at Salesforce - can handle technical depth but wants strategic view
- Senior Principal SDE needs technical credibility and practical applicability
- Need both elevator pitch AND deep dive formats

---

## Objectives

1. Create elevator pitch (30-60 seconds) that captures attention and conveys value
2. Develop deep dive demo (15-30 minutes) with live/recorded demonstration
3. Produce executive summary document with ROI focus
4. Create mental model guides at ELI5/L0/L1/L2 levels
5. Develop demo script/runbook for presentation delivery

---

## Acceptance Criteria

### AC-1: Elevator Pitch Script
- [ ] T-001: Draft initial elevator pitch script
- [ ] T-002: Review for jargon and clarity
- [ ] T-003: Create supporting visual (1 slide)
- [ ] T-004: Practice and refine timing (30-60 seconds)

### AC-2: Deep Dive Demo Package
- [ ] T-005: Identify key demonstration scenarios
- [ ] T-006: Create demo environment and sample project
- [ ] T-007: Write demo script/runbook
- [ ] T-008: Record demo video (or prepare live demo)
- [ ] T-009: Create supporting slides (5-10 slides)

### AC-3: Executive Summary Document
- [ ] T-010: Research competitor landscape
- [ ] T-011: Define ROI metrics and value proposition
- [ ] T-012: Write executive summary (1-2 pages)
- [ ] T-013: Include risk mitigation narrative

### AC-4: Mental Model Documentation
- [ ] T-014: Create ELI5 explanation
- [ ] T-015: Create L0 executive mental model
- [ ] T-016: Create L1 architecture mental model
- [ ] T-017: Create L2 implementation deep dive

### AC-5: Presentation Materials
- [ ] T-018: Design slide deck template
- [ ] T-019: Create final presentation deck
- [ ] T-020: Prepare speaker notes
- [ ] T-021: Create handout/leave-behind document

---

## Task Breakdown

### Phase 1: Research and Planning

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-001 | Draft elevator pitch script | PENDING | `docs/demo/elevator-pitch-v1.md` |
| T-010 | Research competitor landscape | PENDING | `docs/demo/competitor-analysis.md` |
| T-011 | Define ROI metrics | PENDING | `docs/demo/roi-analysis.md` |

### Phase 2: Content Development

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-002 | Review pitch for clarity | PENDING | Review notes |
| T-005 | Identify demo scenarios | PENDING | Scenario list |
| T-012 | Write executive summary | PENDING | `docs/demo/executive-summary.md` |
| T-014 | Create ELI5 explanation | PENDING | `docs/demo/eli5.md` |
| T-015 | Create L0 mental model | PENDING | `docs/demo/L0-executive.md` |
| T-016 | Create L1 mental model | PENDING | `docs/demo/L1-architecture.md` |
| T-017 | Create L2 deep dive | PENDING | `docs/demo/L2-implementation.md` |

### Phase 3: Demo Preparation

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-003 | Create elevator slide | PENDING | `docs/demo/slides/elevator.pptx` |
| T-006 | Create demo environment | PENDING | Demo project |
| T-007 | Write demo script | PENDING | `docs/demo/runbook.md` |
| T-013 | Write risk narrative | PENDING | In executive summary |

### Phase 4: Production

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-004 | Practice elevator pitch | PENDING | Recording |
| T-008 | Record demo video | PENDING | `docs/demo/video/` |
| T-009 | Create deep dive slides | PENDING | `docs/demo/slides/deep-dive.pptx` |
| T-018 | Design slide template | PENDING | Template file |
| T-019 | Create final deck | PENDING | `docs/demo/slides/final.pptx` |

### Phase 5: Finalization

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-020 | Prepare speaker notes | PENDING | In slides |
| T-021 | Create handout document | PENDING | `docs/demo/handout.pdf` |

---

## Key Questions to Answer in Demo

### Strategic Questions (for CPO)

1. **What problem does Jerry solve?** Context rot in AI coding assistants
2. **Why does this matter?** LLM degradation kills productivity, quality, and trust
3. **How is this different from manual coding?** Persistent memory, guardrails, quality gates
4. **What's the ROI?** (To be quantified during research)
5. **What are the risks?** (To be addressed in risk narrative)

### Technical Questions (for Principal SDE)

1. **How does it work architecturally?** Hexagonal architecture, CQRS, Event Sourcing
2. **What patterns are used?** Ports and adapters, domain-driven design
3. **How does context management work?** Filesystem as infinite memory
4. **What about quality?** Test pyramid, BDD, constitution-based governance
5. **How does orchestration work?** Multi-agent workflows, sync barriers

---

## Demo Scenarios (Initial Ideas)

| Scenario | Audience | Duration | Key Points |
|----------|----------|----------|------------|
| **Context Rot Problem** | All | 2 min | Show the problem in action |
| **Jerry Session Lifecycle** | Technical | 5 min | Start, checkpoint, resume |
| **Work Tracker Flow** | All | 5 min | Task decomposition, tracking |
| **Agent Orchestration** | Technical | 10 min | Cross-pollinated pipeline demo |
| **Quality Gates** | Technical | 5 min | BDD, testing, governance |
| **Real Bug Fix Journey** | All | 10 min | FT-002 plugin fix story |

---

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| Feature Tracker | [./FEATURE-WORKTRACKER.md](./FEATURE-WORKTRACKER.md) | FT-001 tracker |
| Solution Epic | [../SOLUTION-WORKTRACKER.md](../SOLUTION-WORKTRACKER.md) | SE-003 tracker |
| Persona Guide | `orchestration/jerry-persona-20260114/synthesis/final-synthesis.md` | Voice reference |
| Design Canon | TBD | Architecture philosophy |
| Jerry Constitution | `docs/governance/JERRY_CONSTITUTION.md` | Governance principles |

---

## Evidence Requirements

All tasks must have verifiable evidence:

| Evidence Type | Required For | Format |
|---------------|--------------|--------|
| Document | Content tasks | Markdown file |
| Slides | Presentation tasks | PowerPoint/PDF |
| Video | Demo recording | MP4 file |
| Review notes | Review tasks | Comments/notes |
| Practice recording | Timing tasks | Audio/video |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-14 | UoW-001 created with task breakdown | Claude |
| 2026-01-14 | Defined 21 tasks across 5 phases | Claude |
| 2026-01-14 | Documented key questions and demo scenarios | Claude |
