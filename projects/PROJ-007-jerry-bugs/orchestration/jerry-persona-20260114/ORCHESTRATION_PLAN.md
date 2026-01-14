# ORCHESTRATION_PLAN: Jerry Persona Development

> **Workflow ID:** jerry-persona-20260114
> **Pattern:** Cross-Pollinated Pipeline
> **Project:** PROJ-007-jerry-bugs
> **Feature:** FT-001 (ASCII Splash Screen) / SE-002 (Fun Enhancements)
> **Status:** IN PROGRESS
> **Created:** 2026-01-14
> **Last Updated:** 2026-01-14

---

## L0: Executive Summary (ELI5)

We're researching two things in parallel to give Jerry Framework a personality:
1. **"Jerry of the Day"** - ski culture phenomenon where "Jerrys" make clueless mistakes
2. **Shane McConkey** - legendary skier who created "Saucer Boy" persona

The framework helps prevent "Jerry moments" caused by context rot. Shane embodies the "wise fool" archetype - playful but brilliant. We want Jerry to have that same spirit.

**Why Two Tracks?** Different perspectives (research + exploration) that exchange findings at barriers to create richer output.

---

## L1: Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    JERRY PERSONA DEVELOPMENT WORKFLOW                        │
│                    Workflow ID: jerry-persona-20260114                       │
└─────────────────────────────────────────────────────────────────────────────┘

   Pipeline A (ps)                              Pipeline B (nse)
   Problem-Solving Track                        NASA SE Track
   ─────────────────                            ────────────────
         │                                            │
         ▼                                            ▼
   ┌─────────────┐                              ┌─────────────┐
   │   PHASE 1   │                              │   PHASE 1   │
   │─────────────│                              │─────────────│
   │ps-researcher│                              │nse-explorer │
   │             │                              │ (divergent) │
   │ Jerry of    │                              │             │
   │ the Day     │                              │ Shane       │
   │ Research    │                              │ McConkey    │
   └──────┬──────┘                              └──────┬──────┘
          │                                            │
          │         ╔════════════════════════╗         │
          └────────►║     BARRIER 1          ║◄────────┘
                    ║ Cross-Pollination      ║
                    ║                        ║
                    ║ ps→nse: Jerry insights ║
                    ║ nse→ps: Shane insights ║
                    ╚════════════╤═══════════╝
          ┌────────────────────┬─┴─┬────────────────────┐
          │                    │   │                    │
          ▼                    │   │                    ▼
   ┌─────────────┐             │   │            ┌─────────────┐
   │   PHASE 2   │             │   │            │   PHASE 2   │
   │─────────────│             │   │            │─────────────│
   │ ps-analyst  │             │   │            │nse-architect│
   │             │             │   │            │             │
   │ Analyze how │             │   │            │ Design      │
   │ to apply    │             │   │            │ persona     │
   │ to framework│             │   │            │ integration │
   └──────┬──────┘             │   │            └──────┬──────┘
          │                    │   │                   │
          │         ╔══════════╧═══╧══════════╗        │
          └────────►║     BARRIER 2           ║◄───────┘
                    ║ Cross-Pollination       ║
                    ║                         ║
                    ║ ps→nse: Analysis results║
                    ║ nse→ps: Design decisions║
                    ╚═══════════╤═════════════╝
          ┌─────────────────────┴─────────────────────┐
          │                                           │
          ▼                                           ▼
   ┌─────────────┐                            ┌─────────────┐
   │   PHASE 3   │                            │   PHASE 3   │
   │─────────────│                            │─────────────│
   │ps-synthesize│                            │  nse-qa     │
   │             │                            │             │
   │ Create      │                            │ Validate    │
   │ persona     │                            │ persona     │
   │ guide       │                            │ consistency │
   └──────┬──────┘                            └──────┬──────┘
          │                                          │
          │         ╔════════════════════════╗       │
          └────────►║   FINAL SYNTHESIS      ║◄──────┘
                    ║                        ║
                    ║ Unified Jerry Persona  ║
                    ║ Voice Guide + ASCII    ║
                    ╚════════════════════════╝
```

---

## L2: Execution Queue

### Group 1: Research Phase (PARALLEL)

| Agent ID | Pipeline | Phase | Task | Status |
|----------|----------|-------|------|--------|
| ps-researcher-001 | ps | 1 | Jerry of the Day research | PENDING |
| nse-explorer-001 | nse | 1 | Shane McConkey exploration | PENDING |

**Execution Mode:** PARALLEL (no dependencies)

### Barrier 1: Research Exchange

| Direction | Artifact | Status |
|-----------|----------|--------|
| ps → nse | Jerry insights for Shane context | PENDING |
| nse → ps | Shane insights for Jerry context | PENDING |

### Group 2: Analysis Phase (PARALLEL)

| Agent ID | Pipeline | Phase | Task | Status |
|----------|----------|-------|------|--------|
| ps-analyst-001 | ps | 2 | Framework application analysis | PENDING |
| nse-architect-001 | nse | 2 | Persona integration design | PENDING |

**Execution Mode:** PARALLEL (after Barrier 1)

### Barrier 2: Analysis Exchange

| Direction | Artifact | Status |
|-----------|----------|--------|
| ps → nse | Analysis findings | PENDING |
| nse → ps | Design decisions | PENDING |

### Group 3: Synthesis Phase (PARALLEL)

| Agent ID | Pipeline | Phase | Task | Status |
|----------|----------|-------|------|--------|
| ps-synthesizer-001 | ps | 3 | Create persona voice guide | PENDING |
| nse-qa-001 | nse | 3 | Validate persona consistency | PENDING |

**Execution Mode:** PARALLEL (after Barrier 2)

### Final Synthesis

| Agent ID | Task | Status |
|----------|------|--------|
| orch-synthesizer | Unified Jerry Persona + ASCII Art Options | PENDING |

---

## Agent Mapping to Enablers

| Enabler | Primary Agent | Phase |
|---------|---------------|-------|
| EN-001: Jerry of the Day | ps-researcher-001 | 1 |
| EN-002: Shane McConkey | nse-explorer-001 | 1 |

---

## Deliverables

| ID | Deliverable | Phase | Agent |
|----|-------------|-------|-------|
| D-001 | Jerry of the Day research | 1 | ps-researcher |
| D-002 | Shane McConkey exploration | 1 | nse-explorer |
| D-003 | Framework application analysis | 2 | ps-analyst |
| D-004 | Persona integration design | 2 | nse-architect |
| D-005 | Persona voice guide | 3 | ps-synthesizer |
| D-006 | Persona validation report | 3 | nse-qa |
| D-007 | Unified Jerry Persona | Final | orch-synthesizer |
| D-008 | ASCII art options | Final | orch-synthesizer |

---

## Constitutional Compliance

| Principle | Implementation |
|-----------|----------------|
| P-002: File Persistence | All agents persist to `orchestration/jerry-persona-20260114/` |
| P-003: No Recursive Subagents | Main context invokes agents directly |
| P-010: Task Tracking | ORCHESTRATION_WORKTRACKER.md updated after each agent |
| P-022: No Deception | Honest progress reporting in ORCHESTRATION.yaml |

---

## Recovery Points

| Checkpoint | Trigger | Recovery Point |
|------------|---------|----------------|
| CP-001 | Barrier 1 complete | Start Group 2 |
| CP-002 | Barrier 2 complete | Start Group 3 |
| CP-003 | Final synthesis complete | Workflow complete |

---

## Related Artifacts

| Type | Location |
|------|----------|
| State (SSOT) | `ORCHESTRATION.yaml` |
| Worktracker | `ORCHESTRATION_WORKTRACKER.md` |
| Feature | `work/SE-002-fun-enhancements/FT-001-ascii-splash-screen/FEATURE-WORKTRACKER.md` |
| EN-001 | `work/SE-002-fun-enhancements/FT-001-ascii-splash-screen/en-001-research-jerry-of-the-day.md` |
| EN-002 | `work/SE-002-fun-enhancements/FT-001-ascii-splash-screen/en-002-research-shane-mcconkey.md` |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-14 | Orchestration plan created | Claude |
| 2026-01-14 | Cross-pollinated pipeline designed | Claude |
| 2026-01-14 | Agent mapping to enablers defined | Claude |
