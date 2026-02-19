# ORCHESTRATION_PLAN.md

> **Document ID:** PROJ-001-FEAT-023-ORCH-PLAN
> **Project:** PROJ-001-oss-release
> **Feature:** FEAT-023 — Claude Code Birthday Showcase — Promotional Video
> **Workflow ID:** `feat023-showcase-20260218-001`
> **Pipeline Alias:** `showcase`
> **Status:** ACTIVE
> **Criticality:** C4 (public-facing, irreversible, Anthropic leadership audience)
> **Quality Target:** >= 0.95 weighted composite
> **Version:** 1.0
> **Created:** 2026-02-18
> **Last Updated:** 2026-02-18
> **Deadline:** TODAY — Feb 18, 2026

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#1-executive-summary) | What, why, and current state |
| [Workflow Architecture](#2-workflow-architecture) | Pipeline diagram and pattern |
| [Phase Definitions](#3-phase-definitions) | All 5 phases with agent registry |
| [C4 Tournament Protocol](#4-c4-tournament-protocol) | All 10 adversarial strategies |
| [Quality Gate Specification](#5-quality-gate-specification) | Thresholds, dimensions, revision cycle |
| [State Management](#6-state-management) | Artifact paths and checkpoint strategy |
| [Execution Constraints](#7-execution-constraints) | Hard rules, constitutional compliance |
| [Success Criteria](#8-success-criteria) | Phase and workflow completion criteria |
| [Risk Mitigations](#9-risk-mitigations) | Key risks with mitigations |
| [Resumption Context](#10-resumption-context) | Current state and next actions |

---

## 1. Executive Summary

This orchestration plan governs the end-to-end production of the Jerry Framework promotional video for Claude Code's 1st Birthday Party and Showcase (Feb 21, 2026 at Shack15, San Francisco). The audience is Anthropic leadership, top investors, and developers — the highest-stakes public representation Jerry will have received.

The deliverable is a **2-minute hype reel script** in Saucer Boy persona (Shane McConkey: technically brilliant, wildly fun) built for production in InVideo AI. The meta narrative centers on the most compelling fact about Jerry: **Claude Code built its own quality guardrails**. Jerry is AI governing AI — with soul.

**Current State:** Workflow initialized. Phase 1 (Research) ready to execute.

**Orchestration Pattern:** Sequential with Quality Gates (Pattern 2). Five phases execute in order, each passing a quality gate before the next phase begins. Phase 3 is an embedded C4 adversarial tournament with fan-out across all 10 strategies.

### 1.1 Workflow Identification

| Field | Value | Source |
|-------|-------|--------|
| Workflow ID | `feat023-showcase-20260218-001` | user |
| ID Format | `{feature}-{purpose}-{YYYYMMDD}-{NNN}` | semantic-date-seq |
| Pipeline Alias | `showcase` | user |
| Base Path | `orchestration/feat023-showcase-20260218-001/` | Dynamic |
| Feature Path | `FEAT-023-showcase-video/orchestration/feat023-showcase-20260218-001/` | Canonical |

**Artifact Output Location:**
```
projects/PROJ-001-oss-release/work/EPIC-001-oss-release/FEAT-023-showcase-video/
  orchestration/
    feat023-showcase-20260218-001/
      ORCHESTRATION_PLAN.md           (this file)
      ORCHESTRATION.yaml              (machine-readable state SSOT)
      showcase/
        phase-1-research/
        phase-2-script/
        phase-3-tournament/
          strategies/                 (10 strategy outputs, one dir each)
          scores/
          revisions/
        phase-4-application/
        phase-5-synthesis/
```

---

## 2. Workflow Architecture

### 2.1 Pipeline Diagram

```
  FEAT-023: Claude Code Birthday Showcase — Promotional Video
  Workflow: feat023-showcase-20260218-001 | Alias: showcase
  Pattern: Sequential with Quality Gates | Criticality: C4
  ============================================================

┌─────────────────────────────────────────────────────────────┐
│ PHASE 1: RESEARCH & REQUIREMENTS                            │
│ ─────────────────────────────────────────────────────────── │
│  Agent: ps-researcher                                       │
│  • Tech showcase video best practices (2-min format)        │
│  • InVideo AI hype reel capabilities + script format        │
│  • Jerry key stats and differentiators for pitch            │
│  • EPIC-005 Saucer Boy philosophy + voice                   │
│  Output: research-brief.md                                  │
│  STATUS: PENDING                                            │
└──────────────────────────────┬──────────────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │   QUALITY GATE 1    │
                    │   S-014 >= 0.95     │
                    │   (Research brief   │
                    │    ready for        │
                    │    script phase)    │
                    └──────────┬──────────┘
                               │ PASS
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 2: SCRIPT CREATION                                    │
│ ─────────────────────────────────────────────────────────── │
│  Agent: ps-architect                                        │
│  • 2-minute hype reel script, scene-by-scene                │
│  • Visual direction + narration + overlays + music cues     │
│  • Saucer Boy persona throughout                            │
│  • ~280 words narration (140 WPM / 2 min)                   │
│  • Meta narrative: Claude Code built its own guardrails     │
│  Output: script-v1.md                                       │
│  STATUS: BLOCKED (Gate 1)                                   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │   QUALITY GATE 2    │
                    │   Self-review S-010 │
                    │   before tournament │
                    └──────────┬──────────┘
                               │ PASS
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 3: C4 ADVERSARIAL TOURNAMENT                          │
│ ─────────────────────────────────────────────────────────── │
│                                                             │
│  adv-selector  ──► Confirm C4 strategy set (all 10)        │
│                                                             │
│  Fan-out: adv-executor × 10 strategies (SEQUENTIAL)        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │ S-014    │ │ S-003    │ │ S-013    │ │ S-007    │      │
│  │ LLM-     │ │ Steelman │ │ Inversion│ │ Constit. │      │
│  │ as-Judge │ │          │ │          │ │ AI       │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │ S-002    │ │ S-004    │ │ S-010    │ │ S-012    │      │
│  │ Devil's  │ │ Pre-     │ │ Self-    │ │ FMEA     │      │
│  │ Advocate │ │ Mortem   │ │ Refine   │ │          │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
│  ┌──────────┐ ┌──────────┐                                 │
│  │ S-011    │ │ S-001    │                                 │
│  │ Chain-of-│ │ Red Team │                                 │
│  │ Verif.   │ │          │                                 │
│  └──────────┘ └──────────┘                                 │
│                                                             │
│  Fan-in: adv-scorer                                        │
│  • Composite score from all 10 strategies                   │
│  • Target >= 0.95 weighted composite                        │
│  • Up to 5 revision cycles                                  │
│                                                             │
│  ╔═══════════════════════════════════════════════════╗      │
│  ║  REVISION CYCLE (if score < 0.95)                 ║      │
│  ║  Creator (ps-architect) → Critic (adv-executor)   ║      │
│  ║  → Revision → Re-score                            ║      │
│  ║  Max 5 iterations → Human escalation              ║      │
│  ╚═══════════════════════════════════════════════════╝      │
│                                                             │
│  Output: tournament-report.md, script-final.md             │
│  STATUS: BLOCKED (Gate 2)                                   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │   QUALITY GATE 3    │
                    │   S-014 >= 0.95     │
                    │   Tournament PASS   │
                    └──────────┬──────────┘
                               │ PASS
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 4: APPLICATION MATERIALS                              │
│ ─────────────────────────────────────────────────────────── │
│  Agent: ps-architect                                        │
│  • 2-3 sentence project description for submission          │
│  • Opus 4.6 capabilities highlighted                        │
│  • GitHub URL and deployed URL                              │
│  • Platform-specific formatting for application             │
│  Output: application-materials.md                           │
│  STATUS: BLOCKED (Gate 3)                                   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │   QUALITY GATE 4    │
                    │   S-010 self-review │
                    │   materials ready   │
                    └──────────┬──────────┘
                               │ PASS
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 5: SYNTHESIS                                          │
│ ─────────────────────────────────────────────────────────── │
│  Agent: orch-synthesizer                                    │
│  • Final synthesis: all artifacts + scores + revision hist  │
│  • Executive summary (L0) for user                          │
│  • Production checklist for InVideo AI                      │
│  • Application submission package                           │
│  Output: showcase-synthesis.md                              │
│  STATUS: BLOCKED (Gate 4)                                   │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Orchestration Pattern Classification

| Pattern | Applied | Description |
|---------|---------|-------------|
| Sequential | Yes | All 5 phases execute in order |
| Concurrent | No | Single pipeline, no parallel branches |
| Barrier Sync | No | Quality gates replace sync barriers |
| Hierarchical | Yes | Orchestrator delegates to worker agents |
| Fan-Out/Fan-In | Yes | Phase 3 fans out to 10 strategies, fans in to scorer |
| Quality Gate | Yes | S-014 >= 0.95 at each phase transition |

---

## 3. Phase Definitions

### 3.1 Phase Summary

| Phase | Name | Agent | Key Output | Status |
|-------|------|-------|------------|--------|
| 1 | Research & Requirements | ps-researcher | research-brief.md | PENDING |
| 2 | Script Creation | ps-architect | script-v1.md | BLOCKED |
| 3 | C4 Adversarial Tournament | adv-selector + adv-executor(×10) + adv-scorer | tournament-report.md, script-final.md | BLOCKED |
| 4 | Application Materials | ps-architect | application-materials.md | BLOCKED |
| 5 | Synthesis | orch-synthesizer | showcase-synthesis.md | BLOCKED |

### 3.2 Phase 1 — Research & Requirements

**Agent:** ps-researcher
**Goal:** Establish the strategic foundation for the script — what makes a 2-minute tech hype reel land with Anthropic leadership and investors.

**Deliverables:**
- Analysis of 2-minute tech showcase video best practices (hooks, pacing, call to action)
- InVideo AI script format requirements and hype reel template constraints
- Jerry's key differentiators: stats, capabilities, meta narrative
- Saucer Boy persona voice reference (EPIC-005 philosophy)
- Recommended narrative arc: problem / meta twist / solution / call to action

**Artifact Path:**
```
showcase/phase-1-research/ps-researcher/ps-researcher-research-brief.md
```

**Exit Criteria:** Research brief covers all 4 topic areas. Quality gate 1 passes.

### 3.3 Phase 2 — Script Creation

**Agent:** ps-architect
**Goal:** Write the complete 2-minute hype reel script using research brief as input.

**Deliverables:**
- Scene-by-scene script with numbered scenes
- Per-scene: VISUAL direction, NARRATION text, TEXT OVERLAY, MUSIC CUE
- Total narration: ~280 words (140 WPM × 2 minutes)
- Saucer Boy persona: irreverent, technically precise, adrenaline-infused
- Meta narrative arc: context rot → Jerry → AI governing AI → call to action
- Hook in first 5 seconds; payoff in final 10 seconds

**Artifact Path:**
```
showcase/phase-2-script/ps-architect/ps-architect-script-v1.md
```

**Exit Criteria:** Script has all scenes. Self-review (S-010) passes. Word count ~280. Quality gate 2 passes.

### 3.4 Phase 3 — C4 Adversarial Tournament

**Agents:** adv-selector, adv-executor (×10), adv-scorer
**Goal:** Apply all 10 C4 adversarial strategies to the script. Iterate up to 5 times. Achieve >= 0.95 composite score.

**Tournament Execution (SEQUENTIAL — each strategy builds on prior findings):**

| Step | Agent | Strategy | Focus |
|------|-------|----------|-------|
| 3.1 | adv-selector | — | Confirm C4 strategy set; order execution |
| 3.2 | adv-executor | S-014 LLM-as-Judge | Baseline quality scoring |
| 3.3 | adv-executor | S-003 Steelman | Identify strongest version of the argument |
| 3.4 | adv-executor | S-013 Inversion | What does failure look like? Work backwards |
| 3.5 | adv-executor | S-007 Constitutional AI | Constitutional/governance compliance |
| 3.6 | adv-executor | S-002 Devil's Advocate | Challenge core claims and framing |
| 3.7 | adv-executor | S-004 Pre-Mortem | Imagine it bombed — what went wrong? |
| 3.8 | adv-executor | S-010 Self-Refine | Targeted self-correction pass |
| 3.9 | adv-executor | S-012 FMEA | Failure modes in production/delivery |
| 3.10 | adv-executor | S-011 Chain-of-Verification | Verify all factual claims |
| 3.11 | adv-executor | S-001 Red Team | Adversarial audience attack |
| 3.12 | adv-scorer | S-014 composite | Final weighted score; revision decision |

**Revision Cycle (if score < 0.95):**
```
adv-scorer issues critique → ps-architect revises script → adv-executor re-runs
failing strategies → adv-scorer re-scores → repeat (max 5 cycles)
```

**Artifact Paths:**
```
showcase/phase-3-tournament/adv-selector/adv-selector-strategy-plan.md
showcase/phase-3-tournament/strategies/s-014-llm-judge/s-014-execution.md
showcase/phase-3-tournament/strategies/s-003-steelman/s-003-execution.md
showcase/phase-3-tournament/strategies/s-013-inversion/s-013-execution.md
showcase/phase-3-tournament/strategies/s-007-constitutional/s-007-execution.md
showcase/phase-3-tournament/strategies/s-002-devils-advocate/s-002-execution.md
showcase/phase-3-tournament/strategies/s-004-pre-mortem/s-004-execution.md
showcase/phase-3-tournament/strategies/s-010-self-refine/s-010-execution.md
showcase/phase-3-tournament/strategies/s-012-fmea/s-012-execution.md
showcase/phase-3-tournament/strategies/s-011-chain-of-verification/s-011-execution.md
showcase/phase-3-tournament/strategies/s-001-red-team/s-001-execution.md
showcase/phase-3-tournament/scores/adv-scorer-tournament-report.md
showcase/phase-3-tournament/revisions/revision-{N}/script-v{N+1}.md  (if needed)
```

**Exit Criteria:** adv-scorer composite >= 0.95. Quality gate 3 passes. Final script written to script-final.md.

### 3.5 Phase 4 — Application Materials

**Agent:** ps-architect
**Goal:** Produce the submission package for the Claude Code Birthday Showcase application.

**Deliverables:**
- Project description: 2-3 sentences, punchy, highlights Opus 4.6 capabilities
- GitHub repo URL
- Deployed URL
- Opus 4.6 capability highlights (what Jerry uses from Opus 4.6)
- Any additional fields required by the application form

**Artifact Path:**
```
showcase/phase-4-application/ps-architect/ps-architect-application-materials.md
```

**Exit Criteria:** All required fields populated. Self-review (S-010) passes. Quality gate 4 passes.

### 3.6 Phase 5 — Synthesis

**Agent:** orch-synthesizer
**Goal:** Assemble all artifacts into a final synthesis. Produce a clean production-ready package for the user.

**Deliverables:**
- L0 executive summary: what was created, key scores, final script
- Final script ready to paste into InVideo AI
- Application submission text ready to paste
- Tournament scorecard (all 10 strategies, final composite, iteration count)
- Production checklist: InVideo AI steps, music notes, duration target

**Artifact Path:**
```
showcase/phase-5-synthesis/orch-synthesizer/orch-synthesizer-showcase-synthesis.md
```

**Exit Criteria:** All artifacts present. Synthesis readable as standalone document. User can take it to InVideo AI immediately.

---

## 4. C4 Tournament Protocol

C4 criticality requires all 10 selected strategies (per quality-enforcement SSOT). No strategies are optional at C4.

### 4.1 Strategy Execution Order (per H-16: Steelman before Devil's Advocate)

| Order | Strategy ID | Name | Application to Script |
|-------|-------------|------|----------------------|
| 1 | S-014 | LLM-as-Judge | Establish baseline score before any critique |
| 2 | S-003 | Steelman | Articulate the strongest version of the script's argument |
| 3 | S-013 | Inversion | What would a script that guarantees failure look like? |
| 4 | S-007 | Constitutional AI | Verify no governance/constitutional violations in claims |
| 5 | S-002 | Devil's Advocate | Aggressively challenge: is the meta narrative believable? |
| 6 | S-004 | Pre-Mortem | Imagine it bombed at Shack15 — reconstruct what failed |
| 7 | S-010 | Self-Refine | Creator self-correction using all critique so far |
| 8 | S-012 | FMEA | Failure mode analysis: tech demo, timing, audience cold read |
| 9 | S-011 | Chain-of-Verification | Verify every factual claim in the script |
| 10 | S-001 | Red Team | Adversarial investor/skeptic attack on Jerry's credibility |

### 4.2 Revision Cycle Budget

| Iteration | Trigger | Action |
|-----------|---------|--------|
| 0 | Initial score | First tournament run |
| 1-4 | Score < 0.95 | Creator revision + targeted re-run of failing strategies |
| 5 | Score still < 0.95 | Human escalation per AE-006 |

### 4.3 Score Tracking

Per quality-enforcement SSOT S-014 dimensions:

| Dimension | Weight | Note for Script Context |
|-----------|--------|------------------------|
| Completeness | 0.20 | All scenes present, all InVideo fields covered |
| Internal Consistency | 0.20 | Persona consistent, narrative arc coherent |
| Methodological Rigor | 0.20 | Script structure follows hype reel best practices |
| Evidence Quality | 0.15 | Claims about Jerry are accurate and verifiable |
| Actionability | 0.15 | User can immediately produce with InVideo AI |
| Traceability | 0.10 | Script maps to research brief findings |

---

## 5. Quality Gate Specification

### 5.1 Gate Summary

| Gate | After Phase | Mechanism | Threshold | Escalation |
|------|------------|-----------|-----------|------------|
| QG-1 | Phase 1 — Research | S-014 | >= 0.95 | Human review if 3 revisions fail |
| QG-2 | Phase 2 — Script | S-010 self-review | >= 0.95 | Revision by ps-architect |
| QG-3 | Phase 3 — Tournament | S-014 composite | >= 0.95 | Up to 5 cycles then human |
| QG-4 | Phase 4 — Application | S-010 self-review | >= 0.95 | Revision by ps-architect |

### 5.2 Gate Outcomes

| Band | Score | Action |
|------|-------|--------|
| PASS | >= 0.95 | Proceed to next phase |
| REVISE | 0.90 - 0.94 | Targeted revision; re-score |
| REJECTED | < 0.90 | Significant rework; escalate after 3 failures |

Note: The standard framework threshold is 0.92. This workflow raises it to 0.95 for all gates given C4 criticality and the public nature of the deliverable.

---

## 6. State Management

### 6.1 State Files

| File | Purpose |
|------|---------|
| `ORCHESTRATION.yaml` | Machine-readable state (SSOT) |
| `ORCHESTRATION_PLAN.md` | This file — strategic context |

### 6.2 Artifact Path Structure

```
projects/PROJ-001-oss-release/work/EPIC-001-oss-release/FEAT-023-showcase-video/
  orchestration/
    feat023-showcase-20260218-001/
      ORCHESTRATION_PLAN.md
      ORCHESTRATION.yaml
      showcase/
        phase-1-research/
          ps-researcher/
            ps-researcher-research-brief.md
        phase-2-script/
          ps-architect/
            ps-architect-script-v1.md
        phase-3-tournament/
          adv-selector/
            adv-selector-strategy-plan.md
          strategies/
            s-014-llm-judge/
              s-014-execution.md
            s-003-steelman/
              s-003-execution.md
            s-013-inversion/
              s-013-execution.md
            s-007-constitutional/
              s-007-execution.md
            s-002-devils-advocate/
              s-002-execution.md
            s-004-pre-mortem/
              s-004-execution.md
            s-010-self-refine/
              s-010-execution.md
            s-012-fmea/
              s-012-execution.md
            s-011-chain-of-verification/
              s-011-execution.md
            s-001-red-team/
              s-001-execution.md
          scores/
            adv-scorer-tournament-report.md
          revisions/
            (revision-N/ directories created as needed)
        phase-4-application/
          ps-architect/
            ps-architect-application-materials.md
        phase-5-synthesis/
          orch-synthesizer/
            orch-synthesizer-showcase-synthesis.md
```

### 6.3 Checkpoint Strategy

| Trigger | When | Purpose |
|---------|------|---------|
| PHASE_COMPLETE | After each phase exits quality gate | Phase-level rollback |
| TOURNAMENT_ITERATION | After each revision cycle in Phase 3 | Tournament recovery |
| MANUAL | User-triggered | Debug and inspection |

---

## 7. Execution Constraints

### 7.1 Hard Constraints (Jerry Constitution)

| Constraint | ID | Enforcement |
|------------|----|----|
| Single agent nesting | P-003 | Orchestrator invokes workers only; no recursive subagents |
| File persistence | P-002 | All state and artifacts persisted to filesystem |
| No deception | P-022 | Honest quality scores; no grade inflation |
| User authority | P-020 | User approves human escalation decisions |
| Quality threshold | H-13 | Standard 0.92 raised to 0.95 for C4 public deliverable |
| Creator-critic cycle | H-14 | Minimum 3 iterations enforced in Phase 3 tournament |
| Self-review before presenting | H-15 | S-010 applied before each quality gate |
| Steelman before critique | H-16 | S-003 runs before S-002 and S-001 in tournament |
| Quality scoring required | H-17 | S-014 scoring at every gate |
| Constitutional check | H-18 | S-007 is strategy 4 in tournament |
| Proactive skill invocation | H-22 | /adversary and /problem-solving invoked per trigger map |
| Worktracker templates | WTI-007 | Entity files use canonical templates |

### 7.2 Auto-Escalation Conditions

| Condition | Rule | Action |
|-----------|------|--------|
| Token exhaustion during Phase 3 | AE-006 | Mandatory human escalation; save state checkpoint |
| Score < 0.90 after 3 iterations | H-13 | Human escalation |
| Score < 0.95 after 5 iterations | AE-006 | Mandatory human escalation |

### 7.3 Soft Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max revision cycles | 5 | Deadline pressure — TODAY |
| Narration word count | ~280 words | 140 WPM × 2 minutes |
| Scene count | 8-12 scenes | Hype reel pacing (10-15 sec/scene) |
| Tournament strategy execution | Sequential | Each strategy informs the next |

---

## 8. Success Criteria

### 8.1 Phase Exit Criteria

| Phase | Required | Validation |
|-------|----------|------------|
| 1 — Research | research-brief.md complete; all 4 topic areas covered | QG-1 S-014 score >= 0.95 |
| 2 — Script | ~280-word narration; scene-by-scene with all fields; Saucer Boy voice | QG-2 S-010 self-review passes |
| 3 — Tournament | All 10 strategies executed; composite score >= 0.95 | QG-3 adv-scorer report |
| 4 — Application | All required fields present; Opus 4.6 capabilities highlighted | QG-4 S-010 self-review passes |
| 5 — Synthesis | Standalone synthesis; InVideo AI ready; application package | Synthesizer complete |

### 8.2 Workflow Completion Criteria

| Criterion | Validation |
|-----------|------------|
| All 5 phases complete | All phase status = COMPLETE in ORCHESTRATION.yaml |
| Quality gate achieved | Tournament composite score >= 0.95 |
| Script production-ready | User can paste directly into InVideo AI |
| Application materials complete | All submission fields populated |
| Final synthesis exists | showcase-synthesis.md present and readable |
| Delivered before deadline | Completed by end of Feb 18, 2026 |

---

## 9. Risk Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Score stuck below 0.95 through 5 iterations | Low | High | Human escalation per AE-006; raise to user for manual revision guidance |
| Saucer Boy persona too obscure for Anthropic audience | Medium | Medium | S-004 Pre-Mortem and S-001 Red Team explicitly test audience cold read |
| InVideo AI format constraints not accommodated | Low | High | Phase 1 research explicitly targets InVideo AI capabilities and format |
| Word count drift from 280 (too long/short) | Medium | Medium | S-011 Chain-of-Verification checks word count; explicit exit criterion |
| Meta narrative ("AI governing AI") feels forced | Medium | High | S-003 Steelman strengthens it; S-002 Devil's Advocate challenges it directly |
| Token exhaustion during Phase 3 tournament | Low | High | AE-006: checkpoint after each strategy execution; resume from last checkpoint |
| GitHub/deployed URL unavailable | Low | High | Phase 4 agent confirms URL status; escalate to user if invalid |
| Deadline breach (today) | Medium | Critical | Sequential pattern with no wasted work; escalate immediately if Phase 1 blocked |

---

## 10. Resumption Context

### 10.1 Current Execution State

```
WORKFLOW STATUS AS OF 2026-02-18
=================================

Workflow: feat023-showcase-20260218-001
Status:   ACTIVE — not started

Phase 1 (Research):           PENDING — ready to execute
Phase 2 (Script Creation):    BLOCKED — waiting on QG-1
Phase 3 (C4 Tournament):      BLOCKED — waiting on QG-2
Phase 4 (Application):        BLOCKED — waiting on QG-3
Phase 5 (Synthesis):          BLOCKED — waiting on QG-4

Quality Gates:
  QG-1: PENDING
  QG-2: PENDING
  QG-3: PENDING
  QG-4: PENDING

Deadline: TODAY (Feb 18, 2026)
Event:    Feb 21, 2026 @ Shack15, SF
```

### 10.2 Next Actions

1. Execute Phase 1: Invoke ps-researcher agent. Read EPIC-005 Saucer Boy context. Produce research-brief.md.
2. Apply QG-1: Score research brief with S-014. Confirm >= 0.95 or iterate.
3. Execute Phase 2: Invoke ps-architect with research brief as input. Write 2-min script.
4. Apply QG-2: Self-review with S-010. Confirm script is tournament-ready.
5. Execute Phase 3: Invoke adv-selector to confirm C4 strategy set. Fan-out to all 10 adv-executor runs. Fan-in to adv-scorer.

### 10.3 Key Reference Materials

| Resource | Purpose |
|----------|---------|
| `skills/adversary/SKILL.md` | Adversarial skill agent specs |
| `.context/templates/adversarial/` | All 10 strategy templates |
| `.context/rules/quality-enforcement.md` | Quality gate constants (SSOT) |
| `projects/PROJ-001-oss-release/work/EPIC-001-oss-release/FEAT-023-showcase-video/EN-945-video-script/` | Prior script work (reference) |
| `docs/governance/JERRY_CONSTITUTION.md` | Constitutional compliance reference |

---

*Document ID: PROJ-001-FEAT-023-ORCH-PLAN*
*Workflow ID: feat023-showcase-20260218-001*
*Version: 1.0*
*Criticality: C4 — All 10 adversarial strategies required*
*Cross-Session Portable: All paths are repository-relative*
