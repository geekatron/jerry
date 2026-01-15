# ORCHESTRATION_PLAN: CPO Demo Package Development

> **Workflow ID:** cpo-demo-20260114
> **Pattern:** 3-Pipeline Cross-Pollinated with Critic Loops
> **Project:** PROJ-007-jerry-bugs
> **Feature:** SE-003/FT-001
> **Status:** PLANNING
> **Created:** 2026-01-14

---

## Executive Summary (L0)

This orchestration produces a comprehensive demo package to showcase Jerry Framework to executive and technical leadership. Using 13 agents across 3 parallel pipelines with quality gates, we'll create everything needed to wow the CPO: elevator pitch, executive summary, ROI framework, architecture documentation, mental models, and demo scripts.

---

## Strategic Context

### The Goal

Secure executive buy-in for Jerry Framework by demonstrating:
1. **The Problem:** Context rot destroys AI productivity and trust
2. **The Solution:** Jerry's persistent memory, guardrails, and traceability
3. **The Value:** ROI through saved time, prevented errors, preserved knowledge
4. **The Quality:** NASA-grade rigor, hexagonal architecture, constitution-based governance

### Target Audience

| Stakeholder | Focus | Key Interests |
|-------------|-------|---------------|
| Phil Calvin (CPO) | Strategic | ROI, competitive advantage, risk mitigation |
| Senior Principal SDE | Technical | Architecture quality, patterns, practical applicability |

---

## Workflow Design

### Pattern: 3-Pipeline Cross-Pollinated with Critic Loops

```
                           ┌─────────────────────────────────────────┐
                           │         CPO DEMO ORCHESTRATION          │
                           │       Workflow: cpo-demo-20260114       │
                           └─────────────────────────────────────────┘

     PIPELINE A (ps)              PIPELINE B (nse)             PIPELINE C (synth)
     Value & ROI Focus            Technical Depth              Presentation Synthesis
     ═══════════════              ═══════════════              ════════════════════

┌─────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: RESEARCH & EXPLORATION                                          PARALLEL  │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐              │
│  │ A1: ps-researcher│     │B1: nse-explorer │     │C1: ps-researcher│              │
│  │                 │     │                 │     │                 │              │
│  │ Study Projects  │     │ Explore Arch    │     │ Gather Stories  │              │
│  │ PROJ-001→007    │     │ src/, docs/,    │     │ docs/, projects/│              │
│  │ Extract value   │     │ .claude/        │     │ investigations/ │              │
│  │ evidence        │     │ Catalog patterns│     │ Success cases   │              │
│  │                 │     │                 │     │                 │              │
│  │ → value-        │     │ → tech-         │     │ → story-        │              │
│  │   evidence.md   │     │   inventory.md  │     │   inventory.md  │              │
│  └────────┬────────┘     └────────┬────────┘     └────────┬────────┘              │
│           │                       │                       │                        │
└───────────┴───────────────────────┴───────────────────────┴────────────────────────┘
                                    │
                         ┌──────────▼──────────┐
                         │     BARRIER 1       │
                         │  Research Exchange  │
                         │  + Critic Review    │
                         │  Target: 0.80+      │
                         └──────────┬──────────┘
                                    │
┌───────────┬───────────────────────┴───────────────────────┬────────────────────────┐
│ PHASE 2: ANALYSIS & DRAFTING                                             PARALLEL  │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐              │
│  │ A2: ps-analyst  │     │B2: nse-architect│     │C2: ps-synthesizer│             │
│  │                 │     │                 │     │                 │              │
│  │ ROI Analysis    │     │ Architecture    │     │ Draft Materials │              │
│  │ Competitive     │     │ Documentation   │     │ Mental Models   │              │
│  │ landscape       │     │ Create diagrams │     │ ELI5/L0/L1/L2   │              │
│  │ Strategic fit   │     │ Pattern examples│     │ Slide outline   │              │
│  │                 │     │                 │     │                 │              │
│  │ → roi-          │     │ → arch-         │     │ → draft-        │              │
│  │   analysis.md   │     │   documentation │     │   materials.md  │              │
│  └────────┬────────┘     └────────┬────────┘     └────────┬────────┘              │
│           │                       │                       │                        │
└───────────┴───────────────────────┴───────────────────────┴────────────────────────┘
                                    │
                         ┌──────────▼──────────┐
                         │     BARRIER 2       │
                         │  Analysis Exchange  │
                         │  + Critic Review    │
                         │  Target: 0.85+      │
                         └──────────┬──────────┘
                                    │
┌───────────┬───────────────────────┴───────────────────────┬────────────────────────┐
│ PHASE 3: SYNTHESIS & VALIDATION                                          PARALLEL  │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐              │
│  │A3: ps-synthesizer│    │ B3: nse-qa      │     │C3: ps-synthesizer│             │
│  │                 │     │                 │     │                 │              │
│  │ Executive       │     │ Validate all    │     │ Final Polish    │              │
│  │ Summary         │     │ technical claims│     │ Demo script     │              │
│  │ Value prop      │     │ Ensure accuracy │     │ Runbook         │              │
│  │ narrative       │     │                 │     │ Speaker notes   │              │
│  │                 │     │                 │     │                 │              │
│  │ → executive-    │     │ → validation-   │     │ → demo-         │              │
│  │   summary.md    │     │   report.md     │     │   package.md    │              │
│  └────────┬────────┘     └────────┬────────┘     └────────┬────────┘              │
│           │                       │                       │                        │
└───────────┴───────────────────────┴───────────────────────┴────────────────────────┘
                                    │
                         ┌──────────▼──────────┐
                         │     BARRIER 3       │
                         │  Final Review       │
                         │  + Critic Loop      │
                         │  Target: 0.90+      │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │  FINAL SYNTHESIS    │
                         │  orch-synthesizer   │
                         │                     │
                         │  Unified Demo       │
                         │  Package            │
                         │                     │
                         │  → cpo-demo-        │
                         │    package.md       │
                         └─────────────────────┘
```

---

## Pipeline Specifications

### Pipeline A: Value & ROI (Problem-Solving Track)

**Objective:** Extract and articulate Jerry's business value

| Phase | Agent ID | Agent Type | Task | Input | Output |
|-------|----------|------------|------|-------|--------|
| 1 | A1 | ps-researcher | Study all projects, extract value evidence | PROJ-001→007, docs/ | `ps/phase-1/value-evidence.md` |
| 2 | A2 | ps-analyst | ROI analysis, competitive landscape, strategic fit | A1 output, B1 output | `ps/phase-2/roi-analysis.md` |
| 3 | A3 | ps-synthesizer | Executive summary, value proposition narrative | A2, B2, C2 outputs | `ps/phase-3/executive-summary.md` |

### Pipeline B: Technical Depth (NASA SE Track)

**Objective:** Document architecture quality and technical rigor

| Phase | Agent ID | Agent Type | Task | Input | Output |
|-------|----------|------------|------|-------|--------|
| 1 | B1 | nse-explorer | Explore architecture, patterns, design decisions | src/, docs/design/, .claude/ | `nse/phase-1/tech-inventory.md` |
| 2 | B2 | nse-architect | Create architecture diagrams, document patterns | B1 output, A1 output | `nse/phase-2/arch-documentation.md` |
| 3 | B3 | nse-qa | Validate technical claims, ensure accuracy | All Phase 2 outputs | `nse/phase-3/validation-report.md` |

### Pipeline C: Presentation Synthesis

**Objective:** Transform insights into demo-ready materials

| Phase | Agent ID | Agent Type | Task | Input | Output |
|-------|----------|------------|------|-------|--------|
| 1 | C1 | ps-researcher | Gather success stories, prior art, examples | docs/, projects/, investigations/ | `synth/phase-1/story-inventory.md` |
| 2 | C2 | ps-synthesizer | Draft mental models (ELI5/L0/L1/L2), slide outline | A1, B1, C1 outputs | `synth/phase-2/draft-materials.md` |
| 3 | C3 | ps-synthesizer | Polish demo script, runbook, speaker notes | All Phase 2 outputs | `synth/phase-3/demo-package.md` |

---

## Barrier Specifications

### Barrier 1: Research Exchange

**Trigger:** All Phase 1 agents complete
**Activities:**
1. Cross-pollination handoffs (A1↔B1↔C1)
2. ps-critic review of all Phase 1 outputs
3. Quality gate: 0.80+ score required

**Artifacts:**
- `barriers/barrier-1/a1-to-b1-handoff.md`
- `barriers/barrier-1/b1-to-c1-handoff.md`
- `barriers/barrier-1/critic-review.md`

### Barrier 2: Analysis Exchange

**Trigger:** All Phase 2 agents complete
**Activities:**
1. Cross-pollination handoffs (A2↔B2↔C2)
2. ps-critic review focusing on ROI credibility
3. Quality gate: 0.85+ score required

**Artifacts:**
- `barriers/barrier-2/a2-to-b2-handoff.md`
- `barriers/barrier-2/b2-to-c2-handoff.md`
- `barriers/barrier-2/critic-review.md`

### Barrier 3: Final Review

**Trigger:** All Phase 3 agents complete
**Activities:**
1. ps-critic comprehensive package review
2. Quality gate: 0.90+ score (wow factor)
3. Iteration if needed

**Artifacts:**
- `barriers/barrier-3/critic-review.md`
- `barriers/barrier-3/iteration-feedback.md` (if needed)

---

## Critic Loop Protocol

At each barrier, ps-critic evaluates outputs against these criteria:

| Criterion | Weight | Phase 1 | Phase 2 | Phase 3 |
|-----------|--------|---------|---------|---------|
| Completeness | 20% | All projects covered | All analyses complete | All deliverables present |
| Accuracy | 25% | Sources cited | Claims validated | No errors |
| Clarity | 20% | Readable | Well-structured | CPO-ready |
| Value | 20% | Evidence gathered | ROI quantified | Compelling |
| Wow Factor | 15% | - | - | Memorable, quotable |

**Iteration Protocol:**
1. If score < target, critic provides specific feedback
2. Relevant agent(s) re-execute with feedback incorporated
3. Maximum 2 iterations per barrier
4. Escalate to user if 2 iterations insufficient

---

## Study Scope

### Projects to Analyze (PROJ-001 through PROJ-007)

| Project | Key Value Evidence |
|---------|-------------------|
| PROJ-001 | Plugin cleanup, initial framework development |
| PROJ-002 | (if exists) Additional context |
| PROJ-003 | (if exists) Additional context |
| PROJ-004 | (if exists) Additional context |
| PROJ-005 | Plugin bugs, investigation workflow |
| PROJ-006 | (if exists) Additional context |
| PROJ-007 | Performance bugs, orchestration workflow, persona development |

### Documentation to Review

| Location | Content |
|----------|---------|
| `docs/design/` | ADRs, design decisions |
| `docs/governance/` | Jerry Constitution, behavior tests |
| `docs/knowledge/` | Patterns, exemplars |
| `docs/wisdom/` | Best practices |
| `.claude/` | Rules, patterns, agent definitions |
| `skills/` | Problem-solving, NASA SE, orchestration |

### Architecture to Document

| Component | Key Patterns |
|-----------|--------------|
| `src/domain/` | Pure business logic, no dependencies |
| `src/application/` | CQRS, handlers |
| `src/infrastructure/` | Adapters, persistence |
| `src/interface/` | CLI, hooks |

---

## Deliverables Mapping

| Deliverable | Source Pipeline | Phase | UoW-001 Task |
|-------------|-----------------|-------|--------------|
| Elevator Pitch Script | C | 3 | T-001 to T-004 |
| Executive Summary | A | 3 | T-012, T-013 |
| ROI Framework | A | 2 | T-010, T-011 |
| Architecture Overview | B | 2+3 | Deep dive content |
| Mental Models (ELI5/L0/L1/L2) | C | 2+3 | T-014 to T-017 |
| Demo Script/Runbook | C | 3 | T-007 |
| Slide Deck Outline | C | 2+3 | T-009, T-018, T-019 |
| Success Stories | C | 1 | Examples for demo |

---

## Execution Timeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                    EXECUTION FLOW                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Phase 1 ─────────────> Barrier 1 ─────> Phase 2 ─────> Barrier 2   │
│  [A1,B1,C1]   ↓         [Critic]         [A2,B2,C2]     [Critic]    │
│  PARALLEL    SYNC       SEQUENTIAL       PARALLEL       SEQUENTIAL   │
│              ↓                                                       │
│              ↓                                                       │
│  ────────────> Phase 3 ─────────> Barrier 3 ────> Final Synthesis   │
│               [A3,B3,C3]          [Critic]        [orch-synthesizer]│
│               PARALLEL            SEQUENTIAL      SEQUENTIAL         │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Project coverage | 7/7 projects analyzed | Checklist in Phase 1 |
| Quality scores | 0.80 → 0.85 → 0.90 | Critic reviews |
| Deliverables | 8/8 complete | Final synthesis check |
| CPO readiness | "Wow" factor | Final critic assessment |
| Technical accuracy | 100% validated | nse-qa report |

---

## Risk Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Scope creep | Medium | High | Fixed deliverable list, barrier gates |
| Quality miss | Low | High | Critic loops with iteration |
| Technical inaccuracy | Low | High | nse-qa validation phase |
| Timeline slip | Medium | Medium | Parallel execution, background agents |

---

## File Structure

```
orchestration/cpo-demo-20260114/
├── ORCHESTRATION_PLAN.md           # This document
├── ORCHESTRATION_WORKTRACKER.md    # Execution tracking
├── ORCHESTRATION.yaml              # Machine-readable SSOT
├── ps/                             # Pipeline A artifacts
│   ├── phase-1/
│   │   └── value-evidence.md
│   ├── phase-2/
│   │   └── roi-analysis.md
│   └── phase-3/
│       └── executive-summary.md
├── nse/                            # Pipeline B artifacts
│   ├── phase-1/
│   │   └── tech-inventory.md
│   ├── phase-2/
│   │   └── arch-documentation.md
│   └── phase-3/
│       └── validation-report.md
├── synth/                          # Pipeline C artifacts
│   ├── phase-1/
│   │   └── story-inventory.md
│   ├── phase-2/
│   │   └── draft-materials.md
│   └── phase-3/
│       └── demo-package.md
├── barriers/                       # Barrier artifacts
│   ├── barrier-1/
│   ├── barrier-2/
│   └── barrier-3/
├── checkpoints/                    # Recovery points
└── synthesis/
    └── cpo-demo-package.md         # Final unified deliverable
```

---

## References

- **Enabler:** `work/SE-003-demo-stakeholder-engagement/FT-001-cpo-demo/en-001-demo-orchestration-planning.md`
- **UoW:** `work/SE-003-demo-stakeholder-engagement/FT-001-cpo-demo/uow-001-demo-planning-execution.md`
- **Orchestration Skill:** `skills/orchestration/SKILL.md`
- **Problem-Solving Skill:** `skills/problem-solving/SKILL.md`
- **NASA SE Skill:** `skills/nasa-se/SKILL.md`

---

*Created: 2026-01-14*
*Pattern: 3-Pipeline Cross-Pollinated with Critic Loops*
*Agents: 13 (9 pipeline + 3 critic + 1 final)*
