# EN-006: Context Injection Design

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
-->

> **Type:** enabler
> **Status:** awaiting_approval
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-01-26T00:00:00Z
> **Due:** TBD
> **Completed:**
> **Parent:** FEAT-001
> **Owner:** Claude
> **Target Sprint:** Sprint 2
> **Effort Points:** 13
> **Gate:** GATE-4 (Design Review)
> **Quality Score:** 0.935 (ps-critic: 0.93, nse-qa: 0.94)
> **Workflow ID:** en006-ctxinj-20260126-001

---

## Summary

Design a context injection mechanism that allows existing Jerry agents (ps-researcher, ps-analyst, ps-synthesizer, etc.) to be leveraged with transcript-specific context and prompts. This is an advanced feature that enables reuse of battle-tested agents while specializing their behavior for transcript processing.

**Technical Justification:**
- Reuses proven agent implementations
- Reduces new code/agent development
- Provides flexibility for different transcript types
- Enables orchestration-driven specialization

---

## Benefit Hypothesis

**We believe that** designing a context injection mechanism for existing agents

**Will result in** flexible agent reuse without duplicating agent logic

**We will know we have succeeded when:**
- 5W2H analysis documents when/why/how users would use this
- Context injection specification is complete
- Orchestration integration is designed
- Human approval received at GATE-4

---

## Acceptance Criteria

### Definition of Done

**Phase 0 (Research): ✅ COMPLETE**
- [x] Deep research synthesis with citations and sources (en006-research-synthesis.md)
- [x] Trade space analysis documented (en006-trade-space.md)
- [x] Context7 and web research completed (LangChain, CrewAI, industry patterns)

**Phase 1 (Requirements & Analysis): ✅ COMPLETE**
- [x] 5W2H analysis for context injection use cases (en006-5w2h-analysis.md)
- [x] Ishikawa (root cause) analysis for failure modes (en006-ishikawa-pareto-analysis.md)
- [x] Pareto (80/20) prioritization of use cases (en006-ishikawa-pareto-analysis.md)
- [x] Formal requirements documented (en006-requirements-supplement.md, 20 NASA SE requirements)

**Phase 2 (Design & Architecture): ✅ COMPLETE**
- [x] TDD-context-injection.md created with quality >= 0.90 (**0.93 achieved in 2 iterations**)
- [x] SPEC-context-injection.md created with quality >= 0.90 (**0.96 achieved in 1 iteration**)
- [x] JSON schema for context injection payload validated (context-injection-schema.json)

**Phase 3 (Integration, Risk & Examples): ✅ COMPLETE**
- [x] Orchestration integration design complete (en006-orchestration-integration.md)
- [x] FMEA risk assessment with RPN scores (18 failure modes, 16 risks)
- [x] 8D problem-solving for high-RPN items (5 reports for RPN > 100)
- [x] 6 domain context specifications created (34 files total)

**Phase 4 (Quality & Synthesis): ✅ COMPLETE**
- [x] ps-critic + nse-qa quality review passed (>= 0.90) - **ps-critic: 0.93, nse-qa: 0.94**
- [x] Final synthesis with patterns and themes (GATE-4-consolidated-approval-package.md)
- [ ] Human approval at GATE-4 (AWAITING)

### Technical Criteria (5W2H)

| # | Criterion | Framework | Verified |
|---|-----------|-----------|----------|
| AC-1 | Who: Target users identified with personas | 5W2H | [x] 4 personas in en006-5w2h-analysis.md |
| AC-2 | What: Mechanism clearly defined with schema | 5W2H | [x] TDD + SPEC + JSON Schema |
| AC-3 | When: Trigger conditions with decision tree | 5W2H | [x] 7 triggers in en006-5w2h-analysis.md |
| AC-4 | Where: Integration points with diagrams | 5W2H | [x] 6 IPs in TDD Section 3 |
| AC-5 | Why: Value proposition with evidence | 5W2H | [x] Trade space + Pareto analysis |
| AC-6 | How: Implementation approach with TDD | 5W2H | [x] TDD + SPEC + orchestration |
| AC-7 | How much: Performance impact assessed | 5W2H | [x] REQ-CI-P-001, P-002 in requirements |

### Quality Criteria

| # | Criterion | Threshold | Verified |
|---|-----------|-----------|----------|
| QC-1 | TDD quality score | >= 0.90 | [x] **0.93** |
| QC-2 | Specification quality score | >= 0.90 | [x] **0.96** |
| QC-3 | Overall deliverable quality | >= 0.90 | [x] **0.935** (combined ps-critic/nse-qa) |
| QC-4 | EN-003 requirements traceability | 100% | [x] 19/20 covered (95%), 1 deferred |
| QC-5 | ADR compliance (ADR-001..ADR-005) | 100% | [ ] |
| QC-6 | NASA SE process compliance | P1,2,3,4,7,8,11,13-17 | [ ] |

---

## Children (Tasks)

### Task Inventory

| ID | Title | Phase | Status | Owner | Effort | Blocked By | Link |
|----|-------|-------|--------|-------|--------|------------|------|
| TASK-030 | Deep Research & Exploration | 0 | **DONE** | ps-researcher + nse-explorer | 2 | EN-003 | [TASK-030](./TASK-030-deep-research.md) |
| TASK-031 | 5W2H Analysis | 1 | **DONE** | ps-analyst | 1 | BARRIER-0 | [TASK-031](./TASK-031-5w2h-analysis.md) |
| TASK-032 | Ishikawa & Pareto Analysis | 1 | **DONE** | ps-analyst | 1 | TASK-031 | [TASK-032](./TASK-032-ishikawa-pareto.md) |
| TASK-033 | Formal Requirements | 1 | **DONE** | ps-analyst | 1 | TASK-032 | [TASK-033](./TASK-033-formal-requirements.md) |
| TASK-034 | TDD Creation (Iterative) | 2 | **DONE (0.93)** | ps-architect + nse-architecture + ps-critic | 2 | BARRIER-1 | [TASK-034](./TASK-034-tdd-creation.md) |
| TASK-035 | Specification Creation (Iterative) | 2 | **DONE (0.96)** | ps-architect + nse-architecture + ps-critic | 2 | TASK-034 ✓ | [TASK-035](./TASK-035-spec-creation.md) |
| TASK-036 | Orchestration Integration Design | 3 | **DONE** | ps-architect | 2 | BARRIER-2 | [TASK-036](./TASK-036-orchestration-integration.md) |
| TASK-037 | FMEA & Risk Assessment | 3 | **DONE** | nse-risk | 2 | BARRIER-2 | [TASK-037](./TASK-037-fmea-risk.md) |
| TASK-038 | Domain Context Specifications | 3 | **DONE** | ps-architect + ps-validator + nse-verification | 2 | BARRIER-2 | [TASK-038](./TASK-038-example-plans.md) |
| TASK-039 | Quality Review | 4 | **DONE** | ps-critic + nse-qa | 2 | TASK-036,037,038 | [TASK-039](./TASK-039-quality-review.md) |
| TASK-040 | Final Synthesis & GATE-4 Prep | 4 | **DONE** | ps-synthesizer | 2 | BARRIER-3 | [TASK-040](./TASK-040-synthesis-gate4.md) |
| TASK-041 | Remediate 8D Terminology (REM-001) | 4.1 | **DONE** | Claude | 1 | TASK-039 | [TASK-041](./TASK-041-remediate-8d-terminology.md) |
| TASK-042 | Remediate DISC-001 Reference (REM-002) | 4.1 | **DONE** | Claude | 1 | TASK-039 | [TASK-042](./TASK-042-remediate-disc001-reference.md) |

### Workflow Architecture

**Pattern:** Cross-Pollinated Pipeline + Generator-Critic
**Quality Threshold:** >= 0.90

```
CROSS-POLLINATED PIPELINE ARCHITECTURE
══════════════════════════════════════

Pipeline A (PS)                                    Pipeline B (NSE)
═══════════════                                    ════════════════

PHASE 0: Deep Research
┌───────────────────┐                              ┌───────────────────┐
│ TASK-030:         │                              │ TASK-030:         │
│ ps-researcher     │◄────── BARRIER-0 ──────────►│ nse-explorer      │
│ Context7 + Web    │        (Research)            │ NASA SE Process 1 │
└───────────────────┘                              └───────────────────┘
        │                                                  │
        └──────────────────────┬───────────────────────────┘
                               ▼
PHASE 1: Requirements & Analysis
┌───────────────────┐                              ┌───────────────────┐
│ TASK-031: 5W2H    │                              │ TASK-033:         │
│ TASK-032: Ishikawa│◄────── BARRIER-1 ──────────►│ nse-requirements  │
│         + Pareto  │        (Requirements)        │ NASA SE Process 2 │
└───────────────────┘                              └───────────────────┘
        │                                                  │
        └──────────────────────┬───────────────────────────┘
                               ▼
PHASE 2: Design & Architecture (Iterative Loops)
┌─────────────────────────────────────────────────────────────────────────┐
│ TASK-034: TDD Creation                                                   │
│ ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                  │
│ │ps-architect │───►│nse-architect│───►│ ps-critic   │──► Quality       │
│ │ (Generate)  │◄───│ (Validate)  │◄───│ (Score)     │    >= 0.90?      │
│ └─────────────┘    └─────────────┘    └─────────────┘    Max 3 iter    │
├─────────────────────────────────────────────────────────────────────────┤
│ TASK-035: Spec Creation                                                  │
│ ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                  │
│ │ps-architect │───►│nse-architect│───►│ ps-critic   │──► Quality       │
│ │ (Generate)  │◄───│ (Validate)  │◄───│ (Score)     │    >= 0.90?      │
│ └─────────────┘    └─────────────┘    └─────────────┘    Max 3 iter    │
└─────────────────────────────────────────────────────────────────────────┘
        │                                                  │
        └──────────────────────┬───────────────────────────┘
                               ▼
                        ╔═══════════════╗
                        ║   BARRIER-2   ║
                        ║    (Design)   ║
                        ╚═══════════════╝
                               │
        ┌──────────────────────┼───────────────────────────┐
        ▼                      ▼                           ▼
PHASE 3: Integration, Risk & Examples (Parallel)
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│ TASK-036:     │      │ TASK-037:     │      │ TASK-038:     │
│ Orchestration │      │ FMEA + 8D     │      │ Examples      │
│ Integration   │      │ nse-risk      │      │ ps-arch +     │
│ ps-architect  │      │ Process 13    │      │ nse-verify    │
└───────┬───────┘      └───────┬───────┘      └───────┬───────┘
        │                      │                       │
        └──────────────────────┼───────────────────────┘
                               ▼
                        ╔═══════════════╗
                        ║   BARRIER-3   ║
                        ║   (Quality)   ║
                        ╚═══════════════╝
                               │
                               ▼
PHASE 4: Quality Review & Synthesis
┌───────────────────────────────────────────────────────────────────────────┐
│ TASK-039: Quality Review (parallel)                                        │
│ ┌───────────────────┐                  ┌───────────────────┐              │
│ │ ps-critic         │   Cross-         │ nse-qa            │              │
│ │ Quality Scoring   │   Pollination    │ NASA SE P14,15,16 │              │
│ └───────────────────┘                  └───────────────────┘              │
├───────────────────────────────────────────────────────────────────────────┤
│ TASK-040: Final Synthesis (ps-synthesizer)                                 │
│ - Pattern extraction                                                       │
│ - Knowledge crystallization                                                │
│ - GATE-4 approval request                                                  │
└───────────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
                        ╔═══════════════╗
                        ║    GATE-4     ║
                        ║Human Approval ║
                        ╚═══════════════╝
```

### Frameworks Applied

| Framework | Applied In | Purpose |
|-----------|-----------|---------|
| 5W2H | TASK-031 | Comprehensive use case analysis |
| Ishikawa | TASK-032 | Root cause analysis for failure modes |
| Pareto (80/20) | TASK-032 | Prioritize high-impact use cases |
| FMEA | TASK-037 | Failure mode risk assessment |
| 8D | TASK-037 | Problem-solving for high RPN items |
| NASA SE NPR 7123.1D | All NSE tasks | Process 1,2,3,4,7,8,11,13,14,15,16,17 |

### Barrier Definitions

| Barrier | Name | Entry Criteria | Exit Criteria |
|---------|------|----------------|---------------|
| BARRIER-0 | Research | Phase 0 agents complete | Research synthesis created, trade space documented |
| BARRIER-1 | Requirements | Phase 1 agents complete | 5W2H done, Ishikawa done, Pareto done, Requirements mapped |
| BARRIER-2 | Design | Phase 2 agents complete, quality >= 0.90 | TDD validated, Spec validated, schemas valid |
| BARRIER-3 | Quality | Phase 3 agents complete | Integration designed, FMEA done, examples created |

### Orchestration Artifacts

| Artifact | Purpose | Location |
|----------|---------|----------|
| ORCHESTRATION_PLAN.md | Workflow strategy | [ORCHESTRATION_PLAN.md](./orchestration/ORCHESTRATION_PLAN.md) |
| ORCHESTRATION.yaml | Machine-readable state | [ORCHESTRATION.yaml](./orchestration/ORCHESTRATION.yaml) |

---

## 5W2H Analysis Framework

### Who (Target Users)

**Primary Users:**
- Power users wanting custom transcript analysis
- Developers extending transcript skill capabilities
- Teams with domain-specific entity extraction needs

**Use Cases:**
1. Legal team wants legal-specific term extraction
2. Sales team wants deal-related action item focus
3. Engineering team wants technical debt identification

### What (Mechanism Definition)

**Context Injection** is the ability to:
1. Provide domain-specific context to existing agents
2. Override default prompts with specialized versions
3. Pass artifacts between agents with additional metadata

**Components:**
- Context Payload: Domain knowledge, entity definitions, extraction rules
- Prompt Templates: Customizable agent instructions
- Artifact Metadata: Additional context attached to outputs

### When (Trigger Conditions)

**Scenarios where context injection is valuable:**
1. Processing transcripts from specialized domains
2. Needing custom entity types beyond standard set
3. Requiring specific output formats
4. Integrating with domain-specific systems

### Where (Integration Points)

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONTEXT INJECTION POINTS                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ORCHESTRATION_PLAN.yaml                                        │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ context_injection:                                         │ │
│  │   domain: "transcript-legal"                              │ │
│  │   context_files:                                           │ │
│  │     - legal-terms.yaml                                    │ │
│  │     - jurisdiction-rules.md                               │ │
│  │   prompt_overrides:                                        │ │
│  │     entity_extraction: legal-entity-prompt.md             │ │
│  └───────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                   AGENT EXECUTION                            ││
│  │  ┌──────────────────┐    ┌──────────────────┐              ││
│  │  │  Base Agent      │ + │ Injected Context │ = Specialized ││
│  │  │  (ps-analyst)    │    │ (legal-terms)    │   Behavior    ││
│  │  └──────────────────┘    └──────────────────┘              ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Why (Value Proposition)

1. **Reuse:** Don't rebuild agent logic for each domain
2. **Flexibility:** Adapt to new domains via configuration
3. **Maintainability:** Core agents stay stable, customization is separate
4. **Testability:** Can test context configurations independently

### How (Implementation Approach)

**Phase 1 (Design):** This enabler
- Specify context payload format
- Define prompt template mechanism
- Design orchestration integration

**Phase 2 (Implementation):** EN-013 in FEAT-002
- Implement context loader
- Implement prompt merger
- Implement metadata passing

### How Much (Performance/Complexity Impact)

| Aspect | Impact | Mitigation |
|--------|--------|------------|
| Context loading | ~100-500ms | Cache context files |
| Prompt merging | ~10ms | Pre-compile templates |
| Metadata overhead | ~5% token increase | Optimize payload |

---

## Example Orchestration Plan

```yaml
# ORCHESTRATION_PLAN: legal-transcript-analysis.yaml

orchestration:
  name: "Legal Transcript Analysis"
  version: "1.0.0"

context_injection:
  domain: "legal"
  context_files:
    - path: contexts/legal-terms.yaml
      type: entity_definitions
    - path: contexts/legal-extraction-rules.md
      type: extraction_rules
  prompt_overrides:
    entity_extraction:
      template: prompts/legal-entity-extraction.md
      variables:
        jurisdiction: "{{jurisdiction}}"
        case_type: "{{case_type}}"

pipeline:
  - stage: parse
    agent: transcript-parser
    # No context injection - standard parsing

  - stage: extract
    agent: ps-analyst  # Existing Jerry agent
    context_injection: true  # Apply legal context

  - stage: synthesize
    agent: ps-synthesizer  # Existing Jerry agent
    context_injection: true
```

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: Analysis & Design](../FEAT-001-analysis-design.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | EN-003 | Requirements inform use cases |
| Depends On | EN-004 | ADRs guide mechanism design |
| Blocks | EN-013 | Implementation needs this design |

### Decisions

| ID | Title | Status | Path |
|----|-------|--------|------|
| DEC-001 | Phase 1 Execution Strategy | ACCEPTED | [DEC-001](./EN-006--DEC-001-phase1-execution-strategy.md) |
| DEC-002 | Implementation Approach - Claude Code Skills | **ACCEPTED** | [DEC-002](./EN-006--DEC-002-implementation-approach.md) |

**DEC-002 Impact:** FEAT-002 implementation will use Claude Code Skills (SKILL.md, AGENT.md, contexts/*.yaml, hooks) NOT Python CLI modules. TDD Python code represents conceptual patterns.

### Related Enablers

- EN-013: Context Injection Implementation (FEAT-002)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-26 | Claude | pending | Enabler created |
| 2026-01-26 | Claude | pending | Task files created (TASK-030..034), orchestration artifacts added |
| 2026-01-26 | Claude | BACKLOG | **Major redesign:** Cross-pollinated pipeline (PS + NSE), 11 tasks (TASK-030..040), 4 barriers, Generator-Critic loops, full framework rigor (5W2H, Ishikawa, Pareto, FMEA, 8D, NASA SE) |
| 2026-01-26 | Claude | IN_PROGRESS | Phase 0 complete, Phase 1 complete (DEC-001 forward-feeding), TASK-034 complete (TDD 0.93), TASK-035 ready |
| 2026-01-26 | Claude | IN_PROGRESS | **DEC-002 created:** Claude Code Skills implementation approach. FEAT-002 will NOT use Python CLI modules. |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Product Backlog Item (tagged Architecture) |
| **SAFe** | Enabler Story |
| **JIRA** | Task |
