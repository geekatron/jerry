# PROJ-008: Transcript Skill - Project Plan

> **Project ID:** PROJ-008-transcript-skill
> **Status:** PLANNING
> **Created:** 2026-01-25
> **Last Updated:** 2026-01-25
> **Branch:** feat/008-transcript-skill

---

## Executive Summary

### L0: ELI5 (Big Picture)

Imagine you have a recording of a meeting and you want to remember everything important that was said. This skill is like having a super-smart assistant that:
- Listens to the meeting transcript (the written version of what everyone said)
- Figures out who was talking about what
- Picks out the important stuff: questions asked, ideas shared, things people need to do
- Creates a colorful map showing how all the ideas connect together
- Helps you turn conversations into actual work tasks

### L1: Engineer (Technical Summary)

The Transcript Skill is a Jerry framework capability that:
1. **Ingests** VTT files (with future support for SRT, TXT, JSON from providers like Otter.ai, Rev, Fireflies)
2. **Extracts** structured entities: speakers, topics, questions, ideas, action items, work items
3. **Generates** mind maps (Mermaid + ASCII, with future D3.js support)
4. **Integrates** with Jerry's worktracker for task creation
5. **Provides** three documentation levels (ELI5, Engineer, Architect)

### L2: Architect (Strategic Context)

**One-Way Door Decisions:**
- Transcript format parser architecture (extensible vs. monolithic)
- Entity extraction model (rule-based vs. LLM-based vs. hybrid)
- Mind map data model (determines future visualization options)

**Trade-offs:**
- Accuracy vs. Speed: LLM extraction is more accurate but slower
- Complexity vs. Maintainability: Multiple format support adds complexity
- Integration depth: Auto-create tasks vs. suggest for review

**Performance Implications:**
- Large transcript processing (1+ hour meetings)
- Real-time vs. batch processing modes
- Memory footprint for mind map generation

---

## Project Objectives

### Primary Goals

1. **Research Phase**: Deep competitive analysis and industry best practices
2. **Design Phase**: Architecture and API design with evidence-based decisions
3. **Implementation Phase**: Phased development starting with MVP (VTT support)
4. **Documentation Phase**: Three-tier documentation for all components

### Success Criteria

- [ ] Comprehensive competitive analysis of 5 products (Pocket + 4 others)
- [ ] Entity extraction accuracy > 90% for key entities (speakers, action items)
- [ ] Mind map generation from transcripts
- [ ] Worktracker integration for suggested task creation
- [ ] Documentation at all three levels (ELI5, Engineer, Architect)

---

## Research Strategy

### Phase 1: Competitive Analysis

**Primary Research Targets:**

| Product | URL | Focus Areas |
|---------|-----|-------------|
| **Pocket** | https://heypocket.com/ | Meeting intelligence, action items |
| **Otter.ai** | https://otter.ai/ | Transcription, collaboration |
| **Fireflies.ai** | https://fireflies.ai/ | Meeting notes, CRM integration |
| **Grain** | https://grain.com/ | Video highlights, sharing |
| **tl;dv** | https://tldv.io/ | Meeting recorder, AI summaries |

**Research Questions (5W2H Framework):**

| Question | Focus |
|----------|-------|
| **What** | What features do competitors offer? What entities do they extract? |
| **Why** | Why do users choose these tools? What problems do they solve? |
| **Who** | Who are the target users? What personas do they serve? |
| **When** | When in the workflow are these tools used? |
| **Where** | Where does the tool integrate (Slack, CRM, Calendar)? |
| **How** | How do they extract entities? How do they visualize? |
| **How much** | How much do they cost? What's the accuracy? |

### Phase 2: Problem-Solving Framework Application

**Frameworks to Apply:**

```
+------------------------------------------------------------------+
|                    FRAMEWORK APPLICATION PLAN                      |
+------------------------------------------------------------------+
| 5W2H          | Requirements gathering, feature scoping           |
| Ishikawa      | Root cause analysis for transcript challenges     |
| Pareto (80/20)| Prioritize 20% features delivering 80% value      |
| FMEA          | Identify failure modes in entity extraction       |
| 8D            | Structured problem resolution approach            |
| NASA SE       | Systems engineering process for architecture      |
+------------------------------------------------------------------+
```

### Phase 3: Industry Best Practices Research

**Research Topics:**
- NLP/NER for meeting transcripts
- Speaker diarization techniques
- Action item extraction algorithms
- Mind mapping data structures
- VTT/SRT format specifications
- Transcript processing pipelines

**Sources:**
- Academic papers (ACL, EMNLP)
- Industry blogs (Hugging Face, OpenAI)
- Open source projects (AssemblyAI, Deepgram)
- Standards bodies (W3C for VTT)

---

## Phased Implementation Strategy

### Phase 0: Research & Discovery (Current)
**Status:** IN_PROGRESS
**Duration:** 1-2 weeks

```
+------------------------------------------------------------------+
|                      PHASE 0: RESEARCH                            |
+------------------------------------------------------------------+
|                                                                    |
|  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐         |
|  │ Competitive │     │  Technical  │     │  Standards  │         |
|  │  Analysis   │     │  Research   │     │  Research   │         |
|  └──────┬──────┘     └──────┬──────┘     └──────┬──────┘         |
|         │                   │                   │                  |
|         └───────────────────┼───────────────────┘                  |
|                             │                                      |
|                             ▼                                      |
|                    ┌─────────────────┐                            |
|                    │   SYNTHESIS     │                            |
|                    │  Requirements   │                            |
|                    └────────┬────────┘                            |
|                             │                                      |
|                             ▼                                      |
|                    ┌─────────────────┐                            |
|                    │  CRITIC REVIEW  │                            |
|                    └─────────────────┘                            |
+------------------------------------------------------------------+
```

**Deliverables:**
- Competitive analysis report (5 products)
- Technical research document
- Requirements specification
- Architecture decision records (ADRs)

### Phase 1: MVP Foundation
**Status:** PENDING
**Duration:** 2-3 weeks

**Scope:**
- VTT parser implementation
- Basic entity extraction (speakers, timestamps)
- Simple mind map generation (Mermaid)
- CLI integration

### Phase 2: Entity Enhancement
**Status:** PENDING
**Duration:** 2-3 weeks

**Scope:**
- Advanced entity extraction (topics, questions, action items)
- Confidence scoring
- Multi-speaker handling
- ASCII art diagram generation

### Phase 3: Worktracker Integration
**Status:** PENDING
**Duration:** 1-2 weeks

**Scope:**
- Suggested task generation
- Review workflow
- Auto-creation option (configurable)

### Phase 4: Visualization & Polish
**Status:** PENDING
**Duration:** 2-3 weeks

**Scope:**
- D3.js mind map export
- Obsidian integration
- Additional format support (SRT, JSON)
- Performance optimization

---

## Multi-Agent Orchestration Plan

### Agent Roster

**Problem-Solving Agents:**
| Agent | Role | Phase |
|-------|------|-------|
| ps-researcher | Competitive analysis, industry research | 0 |
| ps-analyst | Framework analysis (5W2H, FMEA, etc.) | 0 |
| ps-architect | ADR creation, system design | 0, 1 |
| ps-critic | Quality review, adversarial feedback | All |
| ps-validator | Constraint verification | All |
| ps-synthesizer | Pattern extraction, synthesis | 0 |

**NASA SE Agents:**
| Agent | Role | Phase |
|-------|------|-------|
| nse-requirements | Requirements engineering | 0 |
| nse-architecture | System architecture decisions | 1 |
| nse-verification | Verification planning | 1+ |
| nse-reviewer | Technical reviews | All |

### Orchestration Workflow

```
+------------------------------------------------------------------+
|                 ORCHESTRATION PIPELINE                            |
+------------------------------------------------------------------+
|                                                                    |
|  PHASE 0: PARALLEL RESEARCH (Fan-Out)                             |
|  ┌─────────────────────────────────────────────────────────┐      |
|  │                                                          │      |
|  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │      |
|  │  │ps-researcher│  │ps-researcher│  │ps-researcher│     │      |
|  │  │ (Pocket)    │  │ (Otter.ai)  │  │ (Fireflies) │     │      |
|  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │      |
|  │         │                │                │             │      |
|  │  ┌──────┴────────────────┴────────────────┴──────┐     │      |
|  │  │              SYNC BARRIER 1                    │     │      |
|  │  └────────────────────────────────────────────────┘     │      |
|  └─────────────────────────────────────────────────────────┘      |
|                              │                                     |
|                              ▼                                     |
|  PHASE 0B: FRAMEWORK ANALYSIS (Fan-Out)                           |
|  ┌─────────────────────────────────────────────────────────┐      |
|  │  ┌───────────┐  ┌───────────┐  ┌───────────┐           │      |
|  │  │ps-analyst │  │ps-analyst │  │ps-analyst │           │      |
|  │  │ (5W2H)    │  │ (FMEA)    │  │ (Ishikawa)│           │      |
|  │  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘           │      |
|  │        └──────────────┼──────────────┘                  │      |
|  │                       │                                 │      |
|  │  ┌────────────────────┴────────────────────┐           │      |
|  │  │           SYNC BARRIER 2                 │           │      |
|  │  └──────────────────────────────────────────┘           │      |
|  └─────────────────────────────────────────────────────────┘      |
|                              │                                     |
|                              ▼                                     |
|  PHASE 0C: SYNTHESIS (Fan-In)                                     |
|  ┌─────────────────────────────────────────────────────────┐      |
|  │  ┌───────────────┐      ┌───────────────┐              │      |
|  │  │ ps-synthesizer│ ───▶ │  ps-critic    │              │      |
|  │  │ (Combine)     │      │ (Adversarial) │              │      |
|  │  └───────────────┘      └───────┬───────┘              │      |
|  │                                 │                       │      |
|  │  ┌──────────────────────────────┴───────────────────┐  │      |
|  │  │              SYNC BARRIER 3 (Human Review)        │  │      |
|  │  └───────────────────────────────────────────────────┘  │      |
|  └─────────────────────────────────────────────────────────┘      |
|                              │                                     |
|                              ▼                                     |
|  PHASE 1: ARCHITECTURE (Sequential)                               |
|  ┌─────────────────────────────────────────────────────────┐      |
|  │  ┌────────────────┐    ┌────────────────┐              │      |
|  │  │ nse-requirements│───▶│ nse-architecture│             │      |
|  │  └────────────────┘    └────────┬───────┘              │      |
|  │                                 │                       │      |
|  │                                 ▼                       │      |
|  │                    ┌────────────────────┐              │      |
|  │                    │   ps-architect     │              │      |
|  │                    │   (ADR Creation)   │              │      |
|  │                    └────────────────────┘              │      |
|  └─────────────────────────────────────────────────────────┘      |
+------------------------------------------------------------------+
```

### Critic Feedback Loops

```
+------------------------------------------------------------------+
|                    CRITIC LOOP PATTERN                            |
+------------------------------------------------------------------+
|                                                                    |
|    ┌──────────────┐                                               |
|    │   Producer   │                                               |
|    │   Agent      │                                               |
|    └──────┬───────┘                                               |
|           │                                                        |
|           ▼                                                        |
|    ┌──────────────┐         ┌──────────────┐                      |
|    │   Artifact   │ ──────▶ │  ps-critic   │                      |
|    │   Output     │         │  (Review)    │                      |
|    └──────────────┘         └──────┬───────┘                      |
|                                    │                               |
|                    ┌───────────────┼───────────────┐              |
|                    │               │               │              |
|                    ▼               ▼               ▼              |
|               ┌────────┐    ┌──────────┐    ┌─────────────┐      |
|               │APPROVED│    │  REVISE  │    │DOC_PROCEED  │      |
|               └────────┘    └────┬─────┘    └─────────────┘      |
|                                  │                                 |
|                                  │ (max 2 iterations)             |
|                                  ▼                                 |
|                           Back to Producer                         |
+------------------------------------------------------------------+
```

---

## Work Breakdown Structure

### Epic: EPIC-001 - Transcript Skill Foundation

**Features:**
1. **FEAT-001**: Competitive Research & Analysis
2. **FEAT-002**: VTT Parser & Entity Extraction
3. **FEAT-003**: Mind Map Generation
4. **FEAT-004**: Worktracker Integration

**Enablers:**
- EN-001: Market Analysis & Competitive Research
- EN-002: Technical Standards Research (VTT, SRT)
- EN-003: Entity Extraction Architecture
- EN-004: Visualization Architecture

---

## Risk Assessment (FMEA Preview)

| Risk | Severity | Likelihood | Detection | RPN | Mitigation |
|------|----------|------------|-----------|-----|------------|
| Entity extraction accuracy low | High | Medium | Medium | 12 | Use LLM + rules hybrid |
| Large transcript performance | Medium | Medium | High | 6 | Streaming/chunking |
| Mind map complexity overflow | Medium | Low | Medium | 3 | Hierarchical clustering |
| Format parsing edge cases | Low | High | High | 3 | Comprehensive test suite |

---

## Quality Gates

### Research Phase Exit Criteria
- [ ] 5 competitive products analyzed with feature matrices
- [ ] 5W2H analysis complete for problem domain
- [ ] FMEA analysis complete for key failure modes
- [ ] Requirements specification reviewed by ps-critic
- [ ] All findings documented at ELI5/Engineer/Architect levels

### Design Phase Exit Criteria
- [ ] Architecture ADRs approved
- [ ] API contracts defined
- [ ] Entity model finalized
- [ ] Test strategy documented

### Implementation Phase Exit Criteria
- [ ] Unit test coverage > 90%
- [ ] Integration tests passing
- [ ] Documentation complete (all 3 levels)
- [ ] Performance benchmarks met

---

## Related Artifacts

| Artifact | Location | Status |
|----------|----------|--------|
| WORKTRACKER.md | `./WORKTRACKER.md` | PENDING |
| Epic | `./work/EPIC-001-transcript-skill/` | PENDING |
| Competitive Research | `./research/` | PENDING |
| ADRs | `./decisions/` | PENDING |

---

## References

### Industry Sources
- [W3C WebVTT Specification](https://www.w3.org/TR/webvtt1/)
- [Anthropic Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Chroma Context Rot Research](https://research.trychroma.com/context-rot)

### Jerry Framework
- [Problem-Solving Skill](../skills/problem-solving/SKILL.md)
- [NASA SE Skill](../skills/nasa-se/SKILL.md)
- [Orchestration Skill](../skills/orchestration/SKILL.md)
- [Worktracker Templates](../.context/templates/worktracker/)

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-25 | Claude | Initial plan created |
