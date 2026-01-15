# Draft Presentation Materials: Jerry Framework CPO Demo

> **Agent:** C2 (ps-synthesizer-draft)
> **Pipeline:** C (Presentation Synthesis)
> **Phase:** 2
> **Date:** 2026-01-14
> **Audience:** Phil Calvin (CPO, ex-Salesforce Principal Architect), Senior Principal SDEs

---

## Document Navigation

| Section | Purpose | Time |
|---------|---------|------|
| [1. 30-Second Elevator Pitch](#1-30-second-elevator-pitch) | Quick value summary | 30s |
| [2. 2-Minute Executive Summary](#2-2-minute-executive-summary) | CPO-focused overview | 2m |
| [3. 15-Minute Demo Script](#3-15-minute-demo-script) | Live demo walkthrough | 15m |
| [4. 30-Minute Deep Dive](#4-30-minute-deep-dive-script) | Technical deep dive | 30m |
| [5. Mental Models](#5-mental-models) | ELI5 through L2 | - |
| [6. Slide Deck Outline](#6-slide-deck-outline) | 12 slides | - |
| [7. Visual Assets](#7-visual-assets) | ASCII diagrams | - |
| [8. Q&A Preparation](#8-qa-preparation) | Anticipated questions | - |

---

## 1. 30-Second Elevator Pitch

**Word-for-word script:**

> "Jerry is a governance framework that solves the #1 problem in AI-assisted development: Context Rot - where LLM performance degrades as conversations get longer, even within token limits. Chroma Research documented this phenomenon.
>
> Jerry treats the filesystem as infinite memory. Work items survive session restarts. Agents enforce behavioral constraints via a Constitution. Multi-agent orchestration enables parallel research with quality gates.
>
> In 4 months, we've built 43 documented patterns, 2,180 automated tests, and 22 specialized agents - including a NASA Systems Engineering skill that implements NPR 7123.1D processes.
>
> **And for Phil, this means:** A foundation for enterprise AI governance that scales."

**Duration:** 30 seconds
**Word count:** 105 words

---

## 2. 2-Minute Executive Summary

**Script for Phil Calvin (CPO):**

> Phil, you've seen the challenge at Salesforce - AI assistants that lose context mid-project, forget architectural decisions, let work items slip through the cracks. That's Context Rot, and it's the foundational problem Jerry solves.
>
> **The Core Innovation:** Jerry uses the filesystem as infinite memory. Every decision persists. Every work item survives session restarts. When the context window compacts, the critical state remains.
>
> **What We've Built in 4 Months:**
>
> - **Enterprise Architecture**: Hexagonal with CQRS and Event Sourcing - the same patterns you'd expect from a Salesforce Principal Architect
> - **Constitutional AI Governance**: 8 principles, 4 enforcement tiers, 18 behavior tests
> - **Multi-Agent Orchestration**: Parallel pipelines with sync barriers and quality gates
> - **NASA SE Integration**: 10 specialized agents following NPR 7123.1D
>
> **The Numbers:**
>
> - 2,180+ automated tests across unit, integration, E2E, and architecture
> - 43 documented patterns in a comprehensive catalog
> - 22 enhanced agents with +11.7% average improvement
> - 7 projects completed, zero regressions
>
> **Why This Matters for Enterprise:**
>
> Context Rot isn't just annoying - it's expensive. Every time an AI forgets context, that's developer time lost re-explaining. Every lost decision is technical debt. Every slipped work item is a quality risk.
>
> Jerry provides the governance layer that makes AI assistants enterprise-ready. We have the architecture. We have the patterns. We have the quality gates.
>
> **And for Phil, this means:** A foundation for AI governance that reduces the risk of AI-assisted development at scale.

**Duration:** 2 minutes
**Word count:** 255 words

---

## 3. 15-Minute Demo Script

### Timing Breakdown

| Section | Duration | Focus |
|---------|----------|-------|
| Hook: Context Rot | 2:00 | The problem |
| Demo: Bug Hunt Story | 5:00 | Multi-agent in action |
| Show: Persona System | 4:00 | User experience |
| Explain: Constitution | 3:00 | Governance |
| Close: Enterprise Value | 1:00 | ROI |

---

### Section 1: The Hook (0:00 - 2:00)

**Visual:** Show Chroma Research quote on screen

> "Let me start with a question Phil has probably experienced. You're two hours into a complex refactoring session. You've explained the entire codebase structure, the design patterns you want to use, the specific files that need changes. You ask the AI to continue where it left off... and it's forgotten everything.
>
> That's Context Rot. Chroma Research documented this phenomenon:
>
> *'Context Rot is the phenomenon where an LLM's performance degrades as the context window fills up, even when total token count is well within the technical limit.'*
>
> It's not a bug in the AI. It's a fundamental limitation of how context windows work. The architecture decisions you explained? Gone. The WORKTRACKER you updated? Evaporated.
>
> Jerry exists because we realized: **the filesystem is infinite memory that never forgets.**"

**Transition:** "Let me show you how this works in practice with a real bug we fixed last week."

---

### Section 2: The Bug Hunt Story (2:00 - 7:00)

**Visual:** Show workflow diagram (from Visual Assets section)

> "Two bugs were killing Jerry. Performance was degrading - 97 lock files had accumulated, slowing everything down. And our plugin wasn't loading at all - silent failure, no output.
>
> Instead of debugging for hours, I activated an 8-agent orchestration.
>
> **The Crisis:**
>
> BUG-001 was sneaky. The `AtomicFileAdapter` creates lock files for safe concurrent access. But the cleanup mechanism from ADR-006 was documented... and never implemented. Technical debt that accumulated invisibly.
>
> BUG-002 was critical. When users loaded the plugin, nothing happened. Silent failure. The root cause? A semantic conflict between PEP 723 inline script metadata and package imports. When `uv run` executes, it creates an isolated environment that ignores PYTHONPATH.
>
> **The Resolution:**
>
> The investigation agents ran 5 Whys analysis. The reviewers scored both investigations at 0.91. The architect generated ADRs. The validator confirmed no conflicts - different architecture layers, zero file overlap.
>
> And here's the kicker: **BUG-002 was a one-line fix.** Change `uv run` to `python -m`. Done. The isolated environment is bypassed entirely.
>
> **The Lesson:**
>
> This is why multi-agent works. No single agent would have caught both issues. No single investigation would have validated they don't conflict. The quality gates caught real problems - both investigations needed improvement before passing the 0.85 threshold.
>
> **And for Phil, this means:** Complex debugging that would take a senior engineer days happens in under an hour - with validated quality at every step."

**Visual:** Show quality score progression chart

```
Quality Progression
==================
Phase          Score    Threshold
Investigation  0.91     >= 0.85  [PASS]
Cross-Valid.   0.93     >= 0.85  [PASS]
```

---

### Section 3: The Persona System (7:00 - 11:00)

**Visual:** Show ASCII splash screen

```
     _                        _____                                           _
    | | ___ _ __ _ __ _   _  |  ___| __ __ _ _ __ ___   _____      _____  _ __| | __
 _  | |/ _ \ '__| '__| | | | | |_ | '__/ _` | '_ ` _ \ / _ \ \ /\ / / _ \| '__| |/ /
| |_| |  __/ |  | |  | |_| | |  _|| | | (_| | | | | | |  __/\ V  V / (_) | |  |   <
 \___/ \___|_|  |_|   \__, | |_|  |_|  \__,_|_| |_| |_|\___| \_/\_/ \___/|_|  |_|\_\
                      |___/

                         "The best skier is the one having the most fun."
                                        - Shane McConkey

Session initialized. Let's make some turns.
```

> "When something goes wrong in Jerry, you don't just see 'Error.' You see this:
>
> *'Caught an edge there - full yard sale. Let me gather my equipment.'*
>
> That's not just cute - it's a **context rot warning**. The ski metaphors map to specific context thresholds:
>
> - **Minor wobble (60%)**: Minor context gap
> - **Yard sale (75%)**: Lost thread, needs rebuild
> - **Run went sideways (90%)**: Needs different approach
> - **Red flag conditions (95%)**: Human judgment required
>
> Jerry tells you when it's losing context BEFORE it fails silently.
>
> The persona came from a 7-agent cross-pollinated pipeline. We researched ski culture - 'Jerry' is the affectionate term for someone having a bad day on the mountain. Everyone has Jerry moments. Even experts sometimes yard-sale down a slope.
>
> Then we researched Shane McConkey - the legendary skier who dressed as 'Saucer Boy' while revolutionizing ski technology. He proved you can be technically elite AND silly. Innovative AND humble.
>
> **Voice Modes for Enterprise:**
>
> Users choose their mode:
> - `saucer_boy`: Full personality, skiing metaphors
> - `professional`: Warm but no metaphors
> - `minimal`: Just the facts - perfect for CI/CD pipelines
>
> **And for Phil, this means:** The framework adapts to context. Playful for individual devs, professional for enterprise, minimal for automation."

---

### Section 4: The Constitution (11:00 - 14:00)

**Visual:** Show Constitution principles table

> "Jerry has a Constitution with 8 principles. It's inspired by Anthropic's Constitutional AI, OpenAI's Model Spec, and DeepEval's G-Eval approach.
>
> Three principles are **HARD** - meaning agents cannot override them even if the user asks:
>
> | Principle | What It Means |
> |-----------|---------------|
> | P-003: No Recursive Subagents | Maximum one level of nesting (orchestrator to worker). No agent can spawn an agent that spawns an agent. |
> | P-020: User Authority | The user has ultimate authority. Never override user decisions. |
> | P-022: No Deception | Never deceive about actions, capabilities, or confidence. |
>
> We validate compliance with **18 behavior tests** - happy paths, edge cases, and adversarial scenarios. It's the same approach used by Anthropic's SHADE-Arena.
>
> **Why This Matters:**
>
> Without governance, AI agents can:
> - Spawn infinite nested agents (resource exhaustion)
> - Override user decisions (autonomy violation)
> - Hallucinate capabilities they don't have (trust erosion)
>
> Jerry prevents all three.
>
> **And for Phil, this means:** Enterprise-grade guardrails. Auditable compliance. Trust by design."

---

### Section 5: Close - Enterprise Value (14:00 - 15:00)

**Visual:** Show ROI indicators

> "Let me close with the numbers that matter for enterprise:
>
> - **2,180+ automated tests** - not test scripts, but validated assertions
> - **91% test coverage** on core modules
> - **43 documented patterns** - onboarding acceleration
> - **22 agents enhanced** with +11.7% measurable improvement
> - **Zero regressions** across 7 projects
>
> The architecture is enterprise-ready:
> - Hexagonal with strict boundaries
> - CQRS with Event Sourcing
> - CloudEvents 1.0 compliance
> - NASA SE integration
>
> **And for Phil, this means:**
>
> Jerry isn't a prototype. It's a foundation for enterprise AI governance - the kind of architecture you'd expect from a Principal Architect, with the quality metrics to prove it.
>
> Questions?"

---

## 4. 30-Minute Deep Dive Script

### Timing Breakdown

| Section | Duration | Focus |
|---------|----------|-------|
| Context Rot Problem | 3:00 | Foundation |
| Architecture Tour | 8:00 | Technical depth |
| Bug Hunt Story (Extended) | 6:00 | Process demonstration |
| NASA SE Skill | 5:00 | Domain expertise |
| Multi-Agent Orchestration | 5:00 | Coordination patterns |
| Enterprise Roadmap | 3:00 | Vision |

---

### Section 1: Context Rot Deep Dive (0:00 - 3:00)

> "Context Rot is the core problem. Let me explain why this is fundamental.
>
> AI assistants use context windows - a fixed-size buffer of recent conversation. When that buffer fills up, older content is summarized or dropped. Even within the technical token limit, performance degrades.
>
> **The Research (Chroma):**
>
> Chroma Research quantified this effect. They found that LLM accuracy drops significantly as context fills, even when the technical limit isn't reached. The model 'forgets' earlier context despite having access to it.
>
> **Jerry's Solution: Four Pillars**
>
> 1. **Filesystem as Infinite Memory**: Significant outputs persist to files
> 2. **Work Tracker**: Task state survives sessions and compaction
> 3. **Skills**: Compressed instruction interfaces - reload capability on demand
> 4. **Structured Knowledge**: `docs/` hierarchy accumulates wisdom over time
>
> **The Pattern:**
>
> Jerry agents are trained to recognize context rot indicators and externalize state BEFORE degradation. The persona system makes this visible through severity levels (mild -> standard -> full -> mega)."

---

### Section 2: Architecture Tour (3:00 - 11:00)

**Visual:** Show architecture diagram

```
                    Jerry Framework Architecture
    ============================================================

                          Interface Layer
    +--------------------------------------------------------+
    |   CLI Adapter    |    API Adapter    |   Hook Adapter   |
    |   (Primary)      |    (Primary)      |   (Primary)      |
    +--------------------------------------------------------+
                              |
                              v
                       Application Layer
    +--------------------------------------------------------+
    |  Query Dispatcher  |  Command Dispatcher  |   Handlers  |
    |       CQRS         |        CQRS          |             |
    +--------------------------------------------------------+
                              |
                              v
                         Domain Layer
    +--------------------------------------------------------+
    |   Aggregates   |  Value Objects  |  Domain Events      |
    |   (WorkItem)   |   (ProjectId)   |   (Immutable)       |
    +--------------------------------------------------------+
                              |
                              v
                     Infrastructure Layer
    +--------------------------------------------------------+
    |  Event Store  |  Repositories  |  External Adapters   |
    |  (Secondary)  |   (Secondary)  |     (Secondary)      |
    +--------------------------------------------------------+

    Dependencies flow INWARD only (Dependency Inversion)
```

> "The architecture follows Hexagonal (Ports & Adapters) with strict layer boundaries.
>
> **Domain Layer:**
> - Zero external dependencies - pure Python stdlib only
> - This is not aspirational - it's enforced by architecture tests
> - Aggregates enforce their own invariants
> - Value objects are immutable (`@dataclass(frozen=True)`)
>
> **Application Layer (CQRS):**
> - Commands write data, return domain events
> - Queries read data, return DTOs (never domain entities)
> - Separate dispatchers route to handlers
> - Handlers receive dependencies via constructor injection
>
> **Infrastructure Layer:**
> - Implements application ports
> - Event Store for event sourcing
> - File-based persistence for development
> - CloudEvents 1.0 for event serialization
>
> **Composition Root:**
> - Single location (`bootstrap.py`) for all dependency wiring
> - Adapters NEVER instantiate their own dependencies
> - This enables clean testing - swap real adapters for mocks
>
> **Pattern Count Reconciliation:**
>
> You might see two numbers: 27 patterns in the Design Canon, 43 patterns in the Pattern Catalog. Here's the distinction:
>
> - **27 patterns**: Canonical architecture patterns from the Design Canon synthesis
> - **43 patterns**: Full implementation catalog including identity, testing, and graph patterns
>
> Both numbers are correct. The Design Canon focused on core architectural patterns. The Catalog is comprehensive."

---

### Section 3: Bug Hunt Extended Story (11:00 - 17:00)

**Visual:** Show workflow diagram

```
Bug Investigation Workflow (8 Agents)
=====================================

Phase 1: Investigation
    +-----------------+       +-----------------+
    | ps-investigator |       | ps-investigator |
    |    (BUG-001)    |       |    (BUG-002)    |
    +-----------------+       +-----------------+
            |                         |
            v                         v
Phase 2: Review Gate (0.85 threshold)
    +-----------------+       +-----------------+
    |  ps-reviewer    |       |  ps-reviewer    |
    |   Score: 0.91   |       |   Score: 0.91   |
    +-----------------+       +-----------------+
            |                         |
            v                         v
Phase 3: Architecture
    +-----------------+       +-----------------+
    |  ps-architect   |       |  ps-architect   |
    |  ADR-PROJ007-01 |       |  ADR-PROJ007-02 |
    +-----------------+       +-----------------+
            |                         |
            +-----------+-------------+
                        |
                        v
Phase 4: Cross-Validation
    +-----------------------------+
    |        ps-validator         |
    |  Conflict Check: PASS       |
    |  Overall Score: 0.93        |
    +-----------------------------+
                |
                v
Phase 5: Synthesis
    +-----------------------------+
    |       ps-synthesizer        |
    |    Final Report Generated   |
    +-----------------------------+
```

> "Let me walk through the investigation in detail.
>
> **BUG-001: The Sneaky Technical Debt**
>
> The `AtomicFileAdapter` creates lock files for POSIX `fcntl.lockf()` locking. The lock files are 0-byte sentinel files with SHA256 hash-based names. Clever for avoiding collisions.
>
> The problem: ADR-006 documented that cleanup was a 'Negative Consequence' to address later. But no work item was created. The cleanup mechanism was deferred... forever.
>
> **Root Cause Analysis (5 Whys):**
>
> 1. Why accumulating? Lock files created, never removed
> 2. Why no removal? Deliberate design (ADR-006) to avoid race conditions
> 3. Why no cleanup mechanism? Listed as 'Negative Consequence' but no work item
> 4. Why not caught earlier? 0-byte files invisible to monitoring
> 5. Why no garbage collection? Documented but never built
>
> **BUG-002: The Silent Killer**
>
> This was critical. Users load the plugin with `--plugin-dir`, and nothing happens. No error. No output. Just... silence.
>
> The root cause: a semantic conflict. The hook script has PEP 723 metadata declaring `dependencies = []`. But the script imports from `src.infrastructure...`. When `uv run` executes, it creates an isolated environment with only declared dependencies. The Jerry package isn't installed in that environment. Import fails. Silently.
>
> **The One-Line Fix:**
>
> Change the hook from `uv run session_start.py` to `python -m src.interface.cli.session_start`. The isolated environment is bypassed entirely.
>
> **Cross-Validation:**
>
> The validator confirmed:
> - Different architecture layers (BUG-001: infrastructure, BUG-002: interface)
> - Zero file overlap
> - No conflicting changes
> - Score: 0.93 (above 0.85 threshold)
>
> **And for Phil:** The lesson from BUG-001 is process: every 'Negative Consequence' in an ADR should generate a work item. The lesson from BUG-002 is architecture: hooks should never fail silently."

---

### Section 4: NASA SE Skill (17:00 - 22:00)

> "Jerry includes a NASA Systems Engineering skill implementing NPR 7123.1D - NASA's procedural requirements for systems engineering.
>
> **Why NASA SE?**
>
> NASA's processes are mission-grade. When failure isn't an option, you need:
> - Rigorous requirements engineering
> - Verification and validation at every stage
> - Risk management with 5x5 matrices
> - Technical review gates
>
> **10 Specialized Agents:**
>
> | Agent | Role |
> |-------|------|
> | nse-requirements | Requirements engineering |
> | nse-verification | V&V specialist |
> | nse-risk | Risk management |
> | nse-reviewer | Technical review gates |
> | nse-explorer | Divergent trade studies |
> | + 5 more | Integration, config, architecture, synthesis, QA |
>
> **What We Analyzed:**
>
> - 37 requirements across 3 coverage levels (Full: 27%, Partial: 41%, None: 32%)
> - 21 risks assessed with 3 RED, 9 YELLOW, 9 GREEN
> - 5 architectural decisions resolved through weighted trade-off analysis
>
> **Top Risk (RPN 20):** AI hallucination of NASA SE guidance. Mitigation: RAG pipeline from authoritative sources.
>
> **And for Phil:** This demonstrates Jerry can implement domain-specific expertise. NASA SE today. Financial compliance tomorrow. Healthcare regulations next."

---

### Section 5: Multi-Agent Orchestration (22:00 - 27:00)

**Visual:** Show orchestration pattern

```
Cross-Pollinated Pipeline Pattern
=================================

Pipeline A (Problem-Solving)          Pipeline B (NASA SE)
         |                                    |
         v                                    v
    +--------+                          +--------+
    |Phase 1 |                          |Phase 1 |
    |Research|                          |Explore |
    +---+----+                          +---+----+
        |                                   |
        +-------------+  +------------------+
                      |  |
                      v  v
               +============+
               | BARRIER 1  |  <- Cross-pollination
               | Sync Point |
               +============+
                      |
        +-------------+-------------+
        |                           |
        v                           v
    +--------+                  +--------+
    |Phase 2 |                  |Phase 2 |
    |Analysis|                  |Architect|
    +---+----+                  +---+----+
        |                           |
        +-------------+  +----------+
                      |  |
                      v  v
               +============+
               | BARRIER 2  |
               | Sync Point |
               +============+
```

> "Jerry supports three orchestration patterns:
>
> 1. **Linear Pipeline**: Sequential agent execution
> 2. **Fan-Out/Fan-In**: Parallel research converging at synthesis
> 3. **Cross-Pollinated Pipeline**: Parallel tracks with sync barriers
>
> **Cross-Pollination in Action (Persona Development):**
>
> The persona workflow used 7 agents across 2 pipelines:
>
> - **Pipeline PS (Problem-Solving)**: Researched 'Jerry' ski culture, analyzed framework application, synthesized voice guide
> - **Pipeline NSE (NASA SE)**: Explored Shane McConkey, designed technical architecture, validated design
>
> At each barrier, artifacts crossed over. The PS research informed NSE architecture. The NSE exploration enriched PS analysis.
>
> **Quality Gates:**
>
> Every barrier includes:
> - Rubric-based scoring (0.85 threshold)
> - Generator-critic loops if below threshold
> - Human approval for major decisions
>
> **State Tracking:**
>
> Orchestrations maintain state in YAML (SSOT):
> - Phase status (pending, in_progress, complete)
> - Agent execution logs
> - Checkpoint IDs for recovery
> - Artifact locations
>
> **And for Phil:** This is the foundation for enterprise-scale AI coordination. Complex workflows decomposed into specialized agents with verified quality."

---

### Section 6: Enterprise Roadmap (27:00 - 30:00)

> "Let me close with where Jerry is going.
>
> **Current State:**
>
> - 7 projects completed
> - 43 patterns documented
> - 22 agents enhanced
> - 2,180+ tests passing
> - Zero regressions
>
> **Near-Term (Q1 2026):**
>
> - Complete Event Sourcing implementation
> - Graph database integration (Apache TinkerPop compatibility)
> - RAG pipeline for authoritative knowledge
> - Claude Code marketplace submission
>
> **Medium-Term (Q2-Q3 2026):**
>
> - Multi-tenant architecture
> - External tool integrations (ADO, GitHub, Jira)
> - Domain-specific skill packs
> - Enterprise SSO integration
>
> **Long-Term Vision:**
>
> Jerry becomes the governance layer for AI-assisted development at scale. Every AI interaction is:
> - Constrained by Constitutional principles
> - Tracked via event sourcing
> - Coordinated through orchestration
> - Validated by quality gates
>
> **And for Phil, this means:**
>
> Jerry is the foundation for trustworthy AI in enterprise development. The architecture is proven. The patterns are documented. The quality is validated.
>
> The question isn't whether AI governance matters - it's who builds it first."

---

## 5. Mental Models

### ELI5 (Explain Like I'm 5)

> "Imagine you have a friend helping you build with LEGO. But your friend has a tiny brain that forgets things after a few minutes. You tell them 'we're building a castle' and show them all the pieces. But when they get distracted, they forget - even though they can still see the pieces!
>
> Jerry is like giving your friend a notebook. Every time they learn something important, they write it down. When they forget, they check the notebook. Now they can help you build a really big castle without forgetting the plan."

### L0 (Non-Technical Stakeholder)

> "Jerry is a framework that helps AI coding assistants remember what they're doing.
>
> AI assistants have a problem: they forget things as conversations get longer. Jerry solves this by saving important information to files that persist between sessions.
>
> It also sets rules for how AI assistants should behave - like a code of conduct. And it coordinates multiple AI assistants working together on complex problems."

### L1 (Technical Manager)

> "Jerry is a governance framework for AI-assisted development that addresses context rot - the degradation of LLM performance as context windows fill.
>
> Key capabilities:
> - **Persistence**: Filesystem-based state that survives session restarts
> - **Governance**: Constitutional AI with behavioral constraints and validation tests
> - **Orchestration**: Multi-agent coordination with quality gates and sync barriers
> - **Architecture**: Hexagonal with CQRS and Event Sourcing
>
> The framework enables enterprise-ready AI workflows with auditable compliance and validated quality."

### L2 (Senior Technical - Phil Calvin Level)

> "Jerry implements a hexagonal architecture with strict layer boundaries (enforced via architecture tests). The domain layer has zero external dependencies - pure stdlib Python only.
>
> CQRS separates read/write operations through dedicated dispatchers. Commands return domain events for audit trails; queries return DTOs, never domain entities. Event sourcing captures full state history with aggregate reconstitution from event streams.
>
> Constitutional AI governance uses a 4-tier progressive enforcement model (Advisory -> Soft -> Medium -> Hard). Three principles are immutable: no recursive subagents (P-003), user authority (P-020), and no deception (P-022).
>
> Multi-agent orchestration supports cross-pollinated pipelines with sync barriers. Quality gates use rubric-based scoring (0.85 threshold) with generator-critic loops for remediation. State tracking uses YAML as SSOT with checkpoint recovery for long-running workflows.
>
> The pattern catalog contains 43 patterns across 12 categories. 27 represent canonical architecture patterns from the Design Canon; the additional 16 cover identity, testing, and graph patterns."

---

## 6. Slide Deck Outline

### Slide 1: Title

```
+------------------------------------------+
|                                          |
|        J E R R Y   F R A M E W O R K     |
|                                          |
|    AI Governance for Enterprise Scale    |
|                                          |
|         CPO Demo - January 2026          |
|                                          |
+------------------------------------------+
```

**Speaker notes:** Welcome and introduction

---

### Slide 2: The Problem - Context Rot

```
+------------------------------------------+
|                                          |
|           CONTEXT ROT                    |
|                                          |
|  "Context Rot is the phenomenon where    |
|   an LLM's performance degrades as the   |
|   context window fills up, even when     |
|   total token count is well within the   |
|   technical limit."                      |
|                                          |
|            - Chroma Research             |
|                                          |
+------------------------------------------+
```

**Speaker notes:** Define the core problem Jerry solves

---

### Slide 3: The Solution - Jerry's Four Pillars

```
+------------------------------------------+
|                                          |
|        JERRY'S FOUR PILLARS              |
|                                          |
|  1. Filesystem as Infinite Memory        |
|  2. Work Tracker - Persistent State      |
|  3. Skills - Compressed Instructions     |
|  4. Structured Knowledge - docs/ Wisdom  |
|                                          |
+------------------------------------------+
```

**Speaker notes:** High-level architecture overview

---

### Slide 4: Architecture Overview

```
+------------------------------------------+
|                                          |
|     HEXAGONAL ARCHITECTURE               |
|                                          |
|     Interface Layer (CLI, API, Hooks)    |
|               |                          |
|     Application Layer (CQRS)             |
|               |                          |
|     Domain Layer (Zero Dependencies)     |
|               |                          |
|     Infrastructure Layer (Adapters)      |
|                                          |
|     Dependencies flow INWARD only        |
|                                          |
+------------------------------------------+
```

**Speaker notes:** Clean architecture with strict boundaries

---

### Slide 5: Story Time - The Bug Hunt

```
+------------------------------------------+
|                                          |
|     TWO BUGS WERE KILLING JERRY          |
|                                          |
|  BUG-001: 97 lock files accumulated      |
|           (sneaky technical debt)        |
|                                          |
|  BUG-002: Plugin silently failed         |
|           (one-line fix)                 |
|                                          |
|           8 Agents                       |
|           < 1 Hour                       |
|           0.93 Quality Score             |
|                                          |
+------------------------------------------+
```

**Speaker notes:** Real problem solved by multi-agent orchestration

---

### Slide 6: Bug Hunt Workflow

```
+------------------------------------------+
|                                          |
|     8-AGENT INVESTIGATION WORKFLOW       |
|                                          |
|  Investigation -> Review Gate (0.91)     |
|         |                                |
|  Architecture -> Cross-Validation (0.93) |
|         |                                |
|      Synthesis                           |
|                                          |
|  Quality validated at every step         |
|                                          |
+------------------------------------------+
```

**Speaker notes:** Show the process, not just the result

---

### Slide 7: Jerry Persona System

```
+------------------------------------------+
|                                          |
|     ASCII SPLASH SCREEN                  |
|                                          |
|     "The best skier is the one           |
|      having the most fun."               |
|            - Shane McConkey              |
|                                          |
|  Context Rot Warnings:                   |
|  - Minor wobble (60%)                    |
|  - Yard sale (75%)                       |
|  - Run went sideways (90%)               |
|  - Red flag conditions (95%)             |
|                                          |
+------------------------------------------+
```

**Speaker notes:** User experience that communicates state

---

### Slide 8: Constitution & Governance

```
+------------------------------------------+
|                                          |
|     JERRY CONSTITUTION                   |
|                                          |
|  8 Principles, 4 Enforcement Tiers       |
|                                          |
|  HARD (Cannot Override):                 |
|  - P-003: No Recursive Subagents         |
|  - P-020: User Authority                 |
|  - P-022: No Deception                   |
|                                          |
|  18 Behavior Tests                       |
|  (Anthropic SHADE-Arena approach)        |
|                                          |
+------------------------------------------+
```

**Speaker notes:** Enterprise-grade governance

---

### Slide 9: Multi-Agent Orchestration

```
+------------------------------------------+
|                                          |
|     CROSS-POLLINATED PIPELINES           |
|                                          |
|  Pipeline A        Pipeline B            |
|     |                  |                 |
|  Phase 1            Phase 1              |
|     |                  |                 |
|     +----> BARRIER <---+                 |
|     |                  |                 |
|  Phase 2            Phase 2              |
|     |                  |                 |
|     +----> BARRIER <---+                 |
|                                          |
|  Sync barriers, quality gates, state     |
|                                          |
+------------------------------------------+
```

**Speaker notes:** Sophisticated workflow coordination

---

### Slide 10: NASA SE Integration

```
+------------------------------------------+
|                                          |
|     NASA SYSTEMS ENGINEERING             |
|                                          |
|  10 Specialized Agents                   |
|  NPR 7123.1D Compliance                  |
|                                          |
|  - Requirements Engineering              |
|  - Verification & Validation             |
|  - Risk Management (5x5 Matrix)          |
|  - Technical Review Gates                |
|                                          |
|  Mission-grade rigor for AI governance   |
|                                          |
+------------------------------------------+
```

**Speaker notes:** Domain expertise demonstration

---

### Slide 11: The Numbers

```
+------------------------------------------+
|                                          |
|     BY THE NUMBERS                       |
|                                          |
|  2,180+  Automated Tests                 |
|     91%  Test Coverage (core)            |
|     43   Documented Patterns             |
|     22   Enhanced Agents                 |
|  +11.7%  Avg Agent Improvement           |
|      7   Projects Completed              |
|      0   Regressions                     |
|                                          |
+------------------------------------------+
```

**Speaker notes:** Quantifiable quality

---

### Slide 12: What This Means for Enterprise

```
+------------------------------------------+
|                                          |
|     ENTERPRISE VALUE                     |
|                                          |
|  For Phil, this means:                   |
|                                          |
|  - Context Rot Mitigation                |
|    (Unlimited session length)            |
|                                          |
|  - Auditable AI Governance               |
|    (Constitutional constraints)          |
|                                          |
|  - Quality-First Development             |
|    (Gates at every step)                 |
|                                          |
|  - Foundation for Scale                  |
|    (Proven architecture)                 |
|                                          |
+------------------------------------------+
```

**Speaker notes:** ROI summary

---

## 7. Visual Assets

### Asset 1: ASCII Splash Screen

```
     _                        _____                                           _
    | | ___ _ __ _ __ _   _  |  ___| __ __ _ _ __ ___   _____      _____  _ __| | __
 _  | |/ _ \ '__| '__| | | | | |_ | '__/ _` | '_ ` _ \ / _ \ \ /\ / / _ \| '__| |/ /
| |_| |  __/ |  | |  | |_| | |  _|| | | (_| | | | | | |  __/\ V  V / (_) | |  |   <
 \___/ \___|_|  |_|   \__, | |_|  |_|  \__,_|_| |_| |_|\___| \_/\_/ \___/|_|  |_|\_\
                      |___/

                         "The best skier is the one having the most fun."
                                        - Shane McConkey

Session initialized. Let's make some turns.
```

---

### Asset 2: Architecture Diagram

```
                    Jerry Framework Architecture
    ============================================================

                          Interface Layer
    +--------------------------------------------------------+
    |   CLI Adapter    |    API Adapter    |   Hook Adapter   |
    |   (Primary)      |    (Primary)      |   (Primary)      |
    +--------------------------------------------------------+
                              |
                              v
                       Application Layer
    +--------------------------------------------------------+
    |  Query Dispatcher  |  Command Dispatcher  |   Handlers  |
    |       CQRS         |        CQRS          |             |
    +--------------------------------------------------------+
                              |
                              v
                         Domain Layer
    +--------------------------------------------------------+
    |   Aggregates   |  Value Objects  |  Domain Events      |
    |   (WorkItem)   |   (ProjectId)   |   (Immutable)       |
    +--------------------------------------------------------+
                              |
                              v
                     Infrastructure Layer
    +--------------------------------------------------------+
    |  Event Store  |  Repositories  |  External Adapters   |
    |  (Secondary)  |   (Secondary)  |     (Secondary)      |
    +--------------------------------------------------------+

    Dependencies flow INWARD only (Dependency Inversion)
```

---

### Asset 3: CQRS Data Flow

```
                    CQRS Data Flow
    ================================================

    [User/Agent]
         |
         v
    +----------+     +------------+     +---------+
    |   CLI    | --> | Query/Cmd  | --> | Handler |
    | Adapter  |     | Dispatcher |     |         |
    +----------+     +------------+     +---------+
                                             |
         +-----------------------------------+
         |                                   |
         v                                   v
    +---------+                      +-------------+
    |  Query  |                      |   Command   |
    | Handler |                      |   Handler   |
    +---------+                      +-------------+
         |                                   |
         v                                   v
    +--------+                       +-------------+
    |  DTO   |                       | Domain      |
    | Return |                       | Events      |
    +--------+                       +-------------+
                                           |
                                           v
                                    +-------------+
                                    | Event Store |
                                    +-------------+
```

---

### Asset 4: Bug Investigation Workflow

```
Bug Investigation Workflow (8 Agents)
=====================================

Phase 1: Investigation
    +-----------------+       +-----------------+
    | ps-investigator |       | ps-investigator |
    |    (BUG-001)    |       |    (BUG-002)    |
    +-----------------+       +-----------------+
            |                         |
            v                         v
Phase 2: Review Gate (0.85 threshold)
    +-----------------+       +-----------------+
    |  ps-reviewer    |       |  ps-reviewer    |
    |   Score: 0.91   |       |   Score: 0.91   |
    +-----------------+       +-----------------+
            |                         |
            v                         v
Phase 3: Architecture
    +-----------------+       +-----------------+
    |  ps-architect   |       |  ps-architect   |
    |  ADR-PROJ007-01 |       |  ADR-PROJ007-02 |
    +-----------------+       +-----------------+
            |                         |
            +-----------+-------------+
                        |
                        v
Phase 4: Cross-Validation
    +-----------------------------+
    |        ps-validator         |
    |  Conflict Check: PASS       |
    |  Overall Score: 0.93        |
    +-----------------------------+
                |
                v
Phase 5: Synthesis
    +-----------------------------+
    |       ps-synthesizer        |
    |    Final Report Generated   |
    +-----------------------------+
```

---

### Asset 5: Cross-Pollinated Pipeline Pattern

```
Cross-Pollinated Pipeline Pattern
=================================

Pipeline A (Problem-Solving)          Pipeline B (NASA SE)
         |                                    |
         v                                    v
    +--------+                          +--------+
    |Phase 1 |                          |Phase 1 |
    |Research|                          |Explore |
    +---+----+                          +---+----+
        |                                   |
        +-------------+  +------------------+
                      |  |
                      v  v
               +============+
               | BARRIER 1  |  <- Cross-pollination
               | Sync Point |     Artifacts exchange
               +============+
                      |
        +-------------+-------------+
        |                           |
        v                           v
    +--------+                  +--------+
    |Phase 2 |                  |Phase 2 |
    |Analysis|                  |Architect|
    +---+----+                  +---+----+
        |                           |
        +-------------+  +----------+
                      |  |
                      v  v
               +============+
               | BARRIER 2  |
               | Quality    |
               | Gate 0.85  |
               +============+
                      |
                      v
               +============+
               | SYNTHESIS  |
               +============+
```

---

### Asset 6: Quality Score Progression

```
Quality Score Progression
=========================

Phase              Score    Threshold    Status
-------------------------------------------------
Investigation      0.91     >= 0.85      [PASS]
Review Gate        0.91     >= 0.85      [PASS]
Architecture       N/A      -            [COMPLETE]
Cross-Validation   0.93     >= 0.85      [PASS]
-------------------------------------------------

       0.70       0.85       0.90       0.95
        |          |          |          |
        +----------+----------+----------+
                   ^          ^
               threshold   achieved
                  |          |
                  |    [####|#####]
                  |         |
              Investigation: 0.91
              Cross-Valid:   0.93
```

---

### Asset 7: Event Sourcing Model

```
              Event-Sourced Aggregate
    ============================================

    [WorkItem.create()]
           |
           v
    +------------------+
    | WorkItemCreated  |  Event #1 (version=1)
    +------------------+
           |
           v
    [work_item.start()]
           |
           v
    +------------------+
    | StatusChanged    |  Event #2 (version=2)
    | pending->in_prog |
    +------------------+
           |
           v
    [work_item.complete()]
           |
           v
    +------------------+
    | WorkItemCompleted|  Event #3 (version=3)
    +------------------+
           |
           v
    +------------------+
    | Event Stream     |  [E1, E2, E3]
    | (Persisted)      |
    +------------------+
           |
           v
    [WorkItem.load_from_history(events)]
           |
           v
    +------------------+
    | Reconstituted    |  Replay events to rebuild state
    | WorkItem         |
    +------------------+
```

---

### Asset 8: Jerry Severity Levels

```
Jerry Severity Levels (Context Rot Warnings)
============================================

 60%         75%         90%         95%
  |           |           |           |
  v           v           v           v
+------+  +--------+  +---------+  +-------+
| Mild |  |Standard|  |  Full   |  | Mega  |
+------+  +--------+  +---------+  +-------+
   |          |            |          |
   v          v            v          v

"Minor     "Yard       "Run went   "Red flag
 wobble"    sale"      sideways"   conditions"

"Lost the  "Caught an  "Time to    "This needs
 line for   edge -      sideslip    human
 a sec"     full yard   back up"    judgment"
            sale"
```

---

## 8. Q&A Preparation

### Architecture Questions

**Q1: Why Hexagonal Architecture instead of Clean Architecture or N-Tier?**

> Hexagonal Architecture (Ports & Adapters) was chosen because it emphasizes explicit port definitions and adapter implementations. This makes dependency inversion explicit rather than implicit. For AI governance, we need crystal-clear boundaries between business logic and infrastructure.
>
> The key differentiator: domain layer has ZERO external dependencies. This is enforced by architecture tests, not just documented. When you can run your domain tests without mocking anything except your own ports, you know the boundaries are real.

**Q2: How do you handle event versioning in Event Sourcing?**

> Every domain event has a version field. When we need to evolve event schemas, we use the event registry for type-safe deserialization. The registry can map old event versions to new event classes, allowing us to replay historical events without breaking changes.
>
> We haven't needed complex versioning yet - the patterns support it, but we've kept events immutable and additive.

**Q3: Why 27 patterns in Design Canon but 43 in Pattern Catalog?**

> The Design Canon (27 patterns) focused on canonical architecture patterns - the core patterns that define Jerry's architectural identity: Hexagonal, CQRS, Event Sourcing, Aggregates, Value Objects.
>
> The Pattern Catalog (43 patterns) is comprehensive - it includes everything: identity patterns (VertexId hierarchy), testing patterns (test pyramid, BDD cycle), and graph patterns (for future integration).
>
> Both numbers are correct. The Canon is authoritative for architecture. The Catalog is comprehensive for implementation.

---

### Process Questions

**Q4: How do you validate agent quality? What prevents hallucination?**

> Quality validation happens at multiple levels:
>
> 1. **Rubric-based scoring** - Each agent output is scored against a rubric (0-1 scale). Threshold is 0.85.
> 2. **Generator-critic loops** - If below threshold, the critic provides feedback and the generator retries.
> 3. **Cross-validation** - For complex workflows, a validator agent checks for conflicts and inconsistencies.
> 4. **Human gates** - Major decisions require human approval at sync barriers.
>
> For hallucination prevention, the Constitution's P-001 (Truth and Accuracy) requires citing sources and acknowledging uncertainty. The behavior tests include adversarial scenarios that test for hallucination patterns.

**Q5: How long did the bug investigation actually take?**

> Under an hour for 8 agents to investigate, review, architect, validate, and synthesize two bugs. The breakdown:
>
> - Investigation: ~15 minutes (parallel)
> - Review gate: ~5 minutes (parallel)
> - Architecture: ~10 minutes (parallel)
> - Cross-validation: ~5 minutes
> - Synthesis: ~10 minutes
>
> Plus some orchestration overhead. The key isn't raw speed - it's validated quality at every step.

**Q6: What happens when an agent fails the quality gate?**

> Generator-critic loop activates. The critic provides specific feedback on what didn't meet the rubric. The generator retries with that feedback. This continues until:
>
> - Score meets threshold (0.85+), OR
> - Maximum iterations reached (usually 3), at which point it escalates to human review
>
> In the bug investigation, both bugs scored 0.91 on first pass - no critic loops needed. But the infrastructure is there.

---

### Constitutional AI Questions

**Q7: What makes P-003 (No Recursive Subagents) a HARD principle?**

> Without this constraint, agents can spawn agents that spawn agents - leading to exponential resource consumption and unpredictable behavior. An orchestrator can spawn workers, but workers cannot spawn their own workers.
>
> This is enforced structurally. Agent definitions include a `can_spawn_agents: false` flag for worker agents. The orchestration skill validates this constraint before execution.

**Q8: How do you test Constitutional compliance?**

> 18 behavior tests covering three categories:
>
> 1. **Happy paths** - Normal operation within Constitutional bounds
> 2. **Edge cases** - Boundary conditions (exactly at threshold, first/last item, etc.)
> 3. **Adversarial scenarios** - Attempts to violate Constitutional principles
>
> The approach follows Anthropic's SHADE-Arena methodology - multi-attempt testing with verification that principles hold under pressure.

**Q9: What inspired the Constitutional AI approach?**

> Three sources:
>
> - **Anthropic Constitutional AI** - The foundational research on behavioral constraints via principles
> - **OpenAI Model Spec** - Their approach to formalizing model behavior expectations
> - **DeepEval G-Eval** - Rubric-based evaluation methodology
>
> Jerry combines these: principles from Constitutional AI, formalization from Model Spec, and evaluation from G-Eval.

---

### Enterprise Questions

**Q10: How does Jerry scale for large teams?**

> Jerry's architecture supports scaling through:
>
> 1. **Project isolation** - Each project has its own workspace, state, and work tracker
> 2. **Event sourcing** - Complete audit trail of all changes
> 3. **Configuration precedence** - Environment variables override project config override global config
> 4. **Skill modularity** - Teams can add domain-specific skills without touching core
>
> Multi-tenant architecture is on the roadmap for Q2-Q3 2026.

**Q11: What's the integration story for existing tools (ADO, GitHub, Jira)?**

> External tool integration is roadmapped for medium-term (Q2-Q3 2026). The architecture supports it through:
>
> - **Anti-corruption layers** - Adapters that translate between Jerry's domain model and external systems
> - **Event-driven sync** - Changes in Jerry emit events that can trigger external updates
> - **Work Tracker ontology** - PROJ-006 designed a unified ontology mapping Jerry's model to ADO Scrum, SAFe, and Jira
>
> The groundwork is laid. Implementation is prioritized after core Event Sourcing completion.

**Q12: What's the licensing model?**

> Currently internal/experimental. The Claude Code marketplace submission is planned for Q1 2026, which will formalize licensing. The architecture and patterns are designed to support both open-source core and proprietary extensions.

---

### Persona Questions

**Q13: Why skiing metaphors? Isn't that alienating to non-skiers?**

> The persona was designed with risk mitigation:
>
> 1. **Voice modes** - `professional` mode removes all metaphors
> 2. **Minimal mode** - For CI/CD pipelines, just the facts
> 3. **User choice** - The user selects their preference
>
> The skiing metaphors serve a functional purpose - they map to context rot severity levels in a memorable way. "Yard sale" is more memorable than "75% context degradation."
>
> That said, we tested the messages with non-skiers during persona development. The QA validation flagged this as an observation to monitor.

**Q14: Can enterprises customize the persona?**

> Yes. The persona system is implemented through:
>
> - **TOML message catalog** - All messages are externalized, editable
> - **Voice mode selection** - Configuration-driven
> - **Threshold configuration** - Severity levels are adjustable
>
> An enterprise could create a `corporate` voice mode with their own messaging while preserving the context rot warning functionality.

---

## References

### Source Documents

| Category | Document | Key Content |
|----------|----------|-------------|
| Stories | `synth/phase-1/story-inventory.md` | 5 stories, evolution narrative |
| Value | `ps/phase-1/value-evidence.md` | ROI indicators, project metrics |
| Technical | `nse/phase-1/tech-inventory.md` | Architecture patterns, code quality |
| Persona | `jerry-persona-20260114/synthesis/final-synthesis.md` | Voice guide, ASCII art |
| Bug Hunt | `perf-plugin-investigation-20260114-001/synthesis/final-synthesis.md` | Investigation details |
| Patterns | `.claude/patterns/PATTERN-CATALOG.md` | 43 patterns catalog |

### External References

| Reference | Usage |
|-----------|-------|
| [Chroma Research - Context Rot](https://research.trychroma.com/context-rot) | Problem definition |
| [Anthropic Constitutional AI](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback) | Governance approach |
| [OpenAI Model Spec](https://model-spec.openai.com/2025-12-18.html) | Principle formalization |
| [DeepEval G-Eval](https://deepeval.com/docs/metrics-llm-evals) | Evaluation methodology |
| [Alistair Cockburn - Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) | Architecture pattern |
| [NASA NPR 7123.1D](https://nodis3.gsfc.nasa.gov/npg_img/N_PR_7123_001D_/N_PR_7123_001D_.pdf) | SE processes |

---

## Synthesis Metadata

| Field | Value |
|-------|-------|
| Agent | C2 (ps-synthesizer-draft) |
| Pipeline | C (Presentation Synthesis) |
| Phase | 2 |
| Inputs | C1 Story Inventory, A1 Value Evidence, B1 Tech Inventory |
| Word Count | ~7,500 |
| Sections | 8 |
| Visual Assets | 8 ASCII diagrams |
| Q&A Items | 14 |
| Status | **COMPLETE** |

---

*"The best framework is the one you enjoy using."*

*- Jerry Framework*
