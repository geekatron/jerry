# EN-001: Demo Orchestration Planning

> **Enabler ID:** EN-001
> **Feature:** FT-001 (CPO Demo and Stakeholder Presentation)
> **Solution Epic:** SE-003 (Demo and Stakeholder Engagement)
> **Project:** PROJ-007-jerry-bugs
> **Status:** IN PROGRESS
> **Created:** 2026-01-14
> **Last Updated:** 2026-01-14

---

## Objective

Design and execute a comprehensive orchestration workflow to produce all demo materials needed to wow the CPO (Phil Calvin) and technical leadership. The orchestration will study Jerry's entire codebase, extract value propositions, and synthesize demo-ready artifacts.

---

## Background

**The Challenge:**
Creating a demo that resonates at multiple levels:
- **Executive (CPO):** Strategic value, ROI, competitive advantage
- **Technical (Principal SDE):** Architecture quality, patterns, implementation depth
- **Emotional:** Delight and personality that makes Jerry memorable

**The Approach:**
Use Jerry's own capabilities (problem-solving, NASA SE, orchestration) to demonstrate Jerry's value. The orchestration workflow itself becomes proof of concept.

---

## Orchestration Design

### Workflow ID: `cpo-demo-20260114`
### Pattern: 3-Pipeline Cross-Pollinated with Critic Loops

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CPO DEMO ORCHESTRATION WORKFLOW                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐               │
│  │  PIPELINE A  │    │  PIPELINE B  │    │  PIPELINE C  │               │
│  │   (ps)       │    │   (nse)      │    │  (synth)     │               │
│  │  Value &     │    │  Technical   │    │  Presentation│               │
│  │  ROI Focus   │    │  Depth       │    │  Synthesis   │               │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘               │
│         │                   │                   │                        │
│    ┌────▼────┐         ┌────▼────┐         ┌────▼────┐                  │
│    │ Phase 1 │         │ Phase 1 │         │ Phase 1 │                  │
│    │Research │         │ Explore │         │ Gather  │   PARALLEL       │
│    └────┬────┘         └────┬────┘         └────┬────┘                  │
│         │                   │                   │                        │
│         └───────────────────┼───────────────────┘                        │
│                             │                                            │
│                    ┌────────▼────────┐                                   │
│                    │   BARRIER 1     │                                   │
│                    │ Research Share  │                                   │
│                    │ + Critic Review │                                   │
│                    └────────┬────────┘                                   │
│                             │                                            │
│         ┌───────────────────┼───────────────────┐                        │
│         │                   │                   │                        │
│    ┌────▼────┐         ┌────▼────┐         ┌────▼────┐                  │
│    │ Phase 2 │         │ Phase 2 │         │ Phase 2 │                  │
│    │ Analyze │         │Architect│         │ Draft   │   PARALLEL       │
│    └────┬────┘         └────┬────┘         └────┬────┘                  │
│         │                   │                   │                        │
│         └───────────────────┼───────────────────┘                        │
│                             │                                            │
│                    ┌────────▼────────┐                                   │
│                    │   BARRIER 2     │                                   │
│                    │ Analysis Share  │                                   │
│                    │ + Critic Review │                                   │
│                    └────────┬────────┘                                   │
│                             │                                            │
│         ┌───────────────────┼───────────────────┐                        │
│         │                   │                   │                        │
│    ┌────▼────┐         ┌────▼────┐         ┌────▼────┐                  │
│    │ Phase 3 │         │ Phase 3 │         │ Phase 3 │                  │
│    │Synthesize│        │Validate │         │ Polish  │   PARALLEL       │
│    └────┬────┘         └────┬────┘         └────┬────┘                  │
│         │                   │                   │                        │
│         └───────────────────┼───────────────────┘                        │
│                             │                                            │
│                    ┌────────▼────────┐                                   │
│                    │   BARRIER 3     │                                   │
│                    │ Final Review    │                                   │
│                    │ + Critic Loop   │                                   │
│                    └────────┬────────┘                                   │
│                             │                                            │
│                    ┌────────▼────────┐                                   │
│                    │ FINAL SYNTHESIS │                                   │
│                    │ Demo Package    │                                   │
│                    └─────────────────┘                                   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Pipeline Definitions

### Pipeline A: Value & ROI (ps)

**Focus:** Business value, strategic alignment, ROI quantification

| Phase | Agent | Task | Output |
|-------|-------|------|--------|
| 1 | ps-researcher | Study all projects (PROJ-001 to PROJ-007) + docs | Value evidence |
| 2 | ps-analyst | ROI analysis, competitive landscape, strategic fit | ROI framework |
| 3 | ps-synthesizer | Executive narrative, value proposition | Exec summary |

### Pipeline B: Technical Depth (nse)

**Focus:** Architecture quality, patterns, implementation rigor

| Phase | Agent | Task | Output |
|-------|-------|------|--------|
| 1 | nse-explorer | Explore architecture, patterns, design decisions | Tech inventory |
| 2 | nse-architect | Document architecture for demo, create diagrams | Arch documentation |
| 3 | nse-qa | Validate technical claims, ensure accuracy | Validation report |

### Pipeline C: Presentation Synthesis (synth)

**Focus:** Transform insights into demo-ready materials

| Phase | Agent | Task | Output |
|-------|-------|------|--------|
| 1 | ps-researcher | Gather prior art, examples, success stories | Story inventory |
| 2 | ps-synthesizer | Draft mental models (ELI5/L0/L1/L2), slides outline | Draft materials |
| 3 | ps-synthesizer | Polish final materials, create scripts | Final package |

### Critic Loops (at each barrier)

| Barrier | Critic Focus | Quality Target |
|---------|--------------|----------------|
| 1 | Research completeness, source quality | 0.80+ |
| 2 | Analysis rigor, ROI credibility | 0.85+ |
| 3 | Demo readiness, clarity, wow factor | 0.90+ |

---

## Deliverables

### Primary Deliverables (for UoW-001)

| ID | Deliverable | Owner | Format |
|----|-------------|-------|--------|
| D-001 | Elevator Pitch Script | Pipeline C | Markdown + speaker notes |
| D-002 | Executive Summary | Pipeline A | 1-2 page document |
| D-003 | ROI Framework | Pipeline A | Document with metrics |
| D-004 | Architecture Overview | Pipeline B | Diagrams + narrative |
| D-005 | Mental Models (ELI5/L0/L1/L2) | Pipeline C | Layered document |
| D-006 | Demo Script/Runbook | Pipeline C | Step-by-step guide |
| D-007 | Slide Deck Outline | Pipeline C | Presentation structure |
| D-008 | Success Stories | Pipeline C | Case studies from projects |

### Supporting Artifacts

| ID | Artifact | Purpose |
|----|----------|---------|
| S-001 | Project Analysis | Evidence from PROJ-001 to PROJ-007 |
| S-002 | Docs Inventory | Prior art from docs/ folder |
| S-003 | Technical Inventory | Architecture patterns catalog |
| S-004 | Competitor Analysis | Market positioning |
| S-005 | Critic Reviews | Quality validation at each barrier |

---

## Execution Plan

### Phase 1: Parallel Research (3 agents, background)

```
┌─────────────────────────────────────────────────────────────────┐
│ LAUNCH IN PARALLEL (background=true)                            │
├─────────────────────────────────────────────────────────────────┤
│ Agent A1: ps-researcher-value                                   │
│   - Study PROJ-001 through PROJ-007                            │
│   - Extract value evidence, problems solved                     │
│   - Output: ps/phase-1/value-evidence.md                       │
│                                                                 │
│ Agent B1: nse-explorer-tech                                     │
│   - Explore src/, docs/design/, .claude/                       │
│   - Catalog architecture, patterns, decisions                   │
│   - Output: nse/phase-1/tech-inventory.md                      │
│                                                                 │
│ Agent C1: ps-researcher-stories                                 │
│   - Study docs/, projects/, investigations/                     │
│   - Gather success stories, prior art                          │
│   - Output: synth/phase-1/story-inventory.md                   │
└─────────────────────────────────────────────────────────────────┘
```

### Barrier 1: Research Share + Critic Review

```
┌─────────────────────────────────────────────────────────────────┐
│ BARRIER 1 (sequential)                                          │
├─────────────────────────────────────────────────────────────────┤
│ 1. Create cross-pollination handoffs                           │
│ 2. ps-critic reviews all Phase 1 outputs                       │
│    - Target: 0.80+ quality score                               │
│    - If < 0.80: iterate with feedback                          │
│ 3. Proceed to Phase 2 when all pass                            │
└─────────────────────────────────────────────────────────────────┘
```

### Phase 2: Parallel Analysis (3 agents, background)

```
┌─────────────────────────────────────────────────────────────────┐
│ LAUNCH IN PARALLEL (background=true)                            │
├─────────────────────────────────────────────────────────────────┤
│ Agent A2: ps-analyst-roi                                        │
│   - ROI framework, competitive analysis                        │
│   - Strategic fit assessment                                   │
│   - Output: ps/phase-2/roi-analysis.md                         │
│                                                                 │
│ Agent B2: nse-architect-demo                                    │
│   - Create architecture diagrams for demo                      │
│   - Document key patterns with examples                        │
│   - Output: nse/phase-2/arch-documentation.md                  │
│                                                                 │
│ Agent C2: ps-synthesizer-draft                                  │
│   - Draft mental models (ELI5/L0/L1/L2)                        │
│   - Create slide outline                                       │
│   - Output: synth/phase-2/draft-materials.md                   │
└─────────────────────────────────────────────────────────────────┘
```

### Barrier 2: Analysis Share + Critic Review

```
┌─────────────────────────────────────────────────────────────────┐
│ BARRIER 2 (sequential)                                          │
├─────────────────────────────────────────────────────────────────┤
│ 1. Create cross-pollination handoffs                           │
│ 2. ps-critic reviews all Phase 2 outputs                       │
│    - Target: 0.85+ quality score                               │
│    - Focus: ROI credibility, technical accuracy                │
│ 3. Proceed to Phase 3 when all pass                            │
└─────────────────────────────────────────────────────────────────┘
```

### Phase 3: Parallel Synthesis (3 agents, background)

```
┌─────────────────────────────────────────────────────────────────┐
│ LAUNCH IN PARALLEL (background=true)                            │
├─────────────────────────────────────────────────────────────────┤
│ Agent A3: ps-synthesizer-exec                                   │
│   - Create executive summary                                   │
│   - Finalize value proposition narrative                       │
│   - Output: ps/phase-3/executive-summary.md                    │
│                                                                 │
│ Agent B3: nse-qa-validate                                       │
│   - Validate all technical claims                              │
│   - Ensure accuracy of architecture docs                       │
│   - Output: nse/phase-3/validation-report.md                   │
│                                                                 │
│ Agent C3: ps-synthesizer-final                                  │
│   - Polish all demo materials                                  │
│   - Create demo script/runbook                                 │
│   - Output: synth/phase-3/demo-package.md                      │
└─────────────────────────────────────────────────────────────────┘
```

### Barrier 3: Final Review + Critic Loop

```
┌─────────────────────────────────────────────────────────────────┐
│ BARRIER 3 (sequential)                                          │
├─────────────────────────────────────────────────────────────────┤
│ 1. ps-critic reviews complete package                          │
│    - Target: 0.90+ quality score                               │
│    - Focus: Wow factor, clarity, completeness                  │
│ 2. If < 0.90: iterate with specific feedback                   │
│ 3. When pass: proceed to final synthesis                       │
└─────────────────────────────────────────────────────────────────┘
```

### Final Synthesis

```
┌─────────────────────────────────────────────────────────────────┐
│ FINAL SYNTHESIS (orch-synthesizer)                              │
├─────────────────────────────────────────────────────────────────┤
│ Combine all pipeline outputs into unified demo package:        │
│                                                                 │
│ 1. Executive Summary (from A3)                                 │
│ 2. ROI Framework (from A2)                                     │
│ 3. Architecture Overview (from B2, B3)                         │
│ 4. Mental Models (from C2, C3)                                 │
│ 5. Demo Script (from C3)                                       │
│ 6. Slide Deck Outline (from C2, C3)                            │
│ 7. Success Stories (from C1)                                   │
│                                                                 │
│ Output: synthesis/cpo-demo-package.md                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Agent Count

| Pipeline | Phase 1 | Phase 2 | Phase 3 | Total |
|----------|---------|---------|---------|-------|
| A (ps) | 1 | 1 | 1 | 3 |
| B (nse) | 1 | 1 | 1 | 3 |
| C (synth) | 1 | 1 | 1 | 3 |
| Critic | - | 1 | 1 | 3 |
| Final | - | - | - | 1 |
| **Total** | **3** | **4** | **4** | **13** |

---

## Success Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| Research completeness | All 7 projects analyzed | Checklist |
| ROI credibility | Quantifiable metrics | Reviewer assessment |
| Technical accuracy | 100% claims validated | nse-qa report |
| Wow factor | CPO-ready quality | Critic score 0.90+ |
| Deliverables complete | 8/8 primary deliverables | Checklist |

---

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| UoW | [./uow-001-demo-planning-execution.md](./uow-001-demo-planning-execution.md) | Parent work item |
| Feature | [./FEATURE-WORKTRACKER.md](./FEATURE-WORKTRACKER.md) | FT-001 tracker |
| Solution Epic | [../SOLUTION-WORKTRACKER.md](../SOLUTION-WORKTRACKER.md) | SE-003 tracker |
| Orchestration Plan | TBD | ORCHESTRATION_PLAN.md |
| Orchestration State | TBD | ORCHESTRATION.yaml |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-14 | EN-001 created with orchestration design | Claude |
| 2026-01-14 | 3-pipeline cross-pollinated pattern designed | Claude |
| 2026-01-14 | 13 agents planned across 3 phases + critic loops | Claude |
