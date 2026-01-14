# ORCHESTRATION_PLAN: Performance and Plugin Bug Investigations (v2)

> **Workflow ID:** perf-plugin-investigation-20260114-001
> **Project:** PROJ-007-jerry-bugs
> **Pattern:** Fan-Out → Review Gate → Generator-Critic → Architecture → Synthesis
> **Status:** ACTIVE
> **Created:** 2026-01-14
> **Version:** 2.0.0 (Enhanced with Critic Loops)
> **Constitutional Compliance:** Jerry Constitution v1.0 (P-003: No Recursive Subagents)

---

## L0: Executive Summary (ELI5)

This orchestration coordinates a **comprehensive investigation pipeline** for two critical Jerry Framework bugs:

1. **BUG-001 (Performance):** Lock files accumulating in `.jerry/local/locks/` causing slowdowns
2. **BUG-002 (Plugin Loading):** Jerry plugin not loading when started via `--plugin-dir`

**What makes this different from a simple investigation?**

- **Parallel investigations** for efficiency
- **Review gates** to ensure quality before proceeding
- **Generator-Critic loops** to iteratively improve if quality is insufficient
- **Architecture proposals** to design proper fixes (not just identify problems)
- **Cross-validation** to ensure fixes meet requirements
- **Final synthesis** to identify cross-cutting patterns and recommendations

---

## L1: Workflow Diagram (Enhanced v2)

```
╔═══════════════════════════════════════════════════════════════════════════════════╗
║          WORKFLOW: perf-plugin-investigation-20260114-001 (v2)                     ║
║          PATTERN: Fan-Out → Review Gate → Generator-Critic → Architecture          ║
╠═══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                   ║
║                              ┌─────────────────────┐                              ║
║                              │    ORCHESTRATOR     │                              ║
║                              │   (Main Context)    │                              ║
║                              └──────────┬──────────┘                              ║
║                                         │                                         ║
║  ════════════════════════════════════════════════════════════════════════════════ ║
║  PHASE 1: INVESTIGATION (Fan-Out - PARALLEL)                                      ║
║  ════════════════════════════════════════════════════════════════════════════════ ║
║                                         │                                         ║
║                       ┌─────────────────┴─────────────────┐                       ║
║                       │                                   │                       ║
║                       ▼                                   ▼                       ║
║        ┌──────────────────────────┐       ┌──────────────────────────┐           ║
║        │  ps-investigator-bug-001 │       │  ps-investigator-bug-002 │           ║
║        │  (Lock File Accumulation)│       │  (Plugin Not Loading)    │           ║
║        │  Severity: MEDIUM        │       │  Severity: HIGH          │           ║
║        └────────────┬─────────────┘       └────────────┬─────────────┘           ║
║                     │                                   │                         ║
║                     └─────────────┬─────────────────────┘                         ║
║                                   ▼                                               ║
║                         ╔══════════════════╗                                      ║
║                         ║   CHECKPOINT 1   ║                                      ║
║                         ╚════════╤═════════╝                                      ║
║                                  │                                                ║
║  ════════════════════════════════════════════════════════════════════════════════ ║
║  PHASE 2: REVIEW GATE (Fan-Out - PARALLEL)                                        ║
║  ════════════════════════════════════════════════════════════════════════════════ ║
║                                  │                                                ║
║                    ┌─────────────┴─────────────┐                                  ║
║                    │                           │                                  ║
║                    ▼                           ▼                                  ║
║       ┌─────────────────────┐     ┌─────────────────────┐                        ║
║       │ ps-reviewer-bug-001 │     │ ps-reviewer-bug-002 │                        ║
║       │ (Quality Assessment)│     │ (Quality Assessment)│                        ║
║       └──────────┬──────────┘     └──────────┬──────────┘                        ║
║                  │                           │                                    ║
║           ┌──────┴──────┐             ┌──────┴──────┐                            ║
║           ▼             ▼             ▼             ▼                            ║
║       [PASS≥0.85]  [FAIL<0.85]   [PASS≥0.85]  [FAIL<0.85]                        ║
║           │             │             │             │                            ║
║           │             ▼             │             ▼                            ║
║           │    ┌────────────────┐    │    ┌────────────────┐                    ║
║           │    │ CRITIC LOOP    │    │    │ CRITIC LOOP    │                    ║
║           │    │ (max 2 iter)   │    │    │ (max 2 iter)   │                    ║
║           │    │ ps-investigator│    │    │ ps-investigator│                    ║
║           │    │ + ps-critic    │    │    │ + ps-critic    │                    ║
║           │    └───────┬────────┘    │    └───────┬────────┘                    ║
║           │            │             │            │                              ║
║           └────────────┼─────────────┴────────────┘                              ║
║                        ▼                                                          ║
║              ╔══════════════════╗                                                ║
║              ║   CHECKPOINT 2   ║                                                ║
║              ╚════════╤═════════╝                                                ║
║                       │                                                          ║
║  ════════════════════════════════════════════════════════════════════════════════ ║
║  PHASE 3: ARCHITECTURE PROPOSALS (Fan-Out - PARALLEL)                             ║
║  ════════════════════════════════════════════════════════════════════════════════ ║
║                       │                                                          ║
║         ┌─────────────┴─────────────┐                                            ║
║         │                           │                                            ║
║         ▼                           ▼                                            ║
║  ┌──────────────────┐     ┌──────────────────┐                                   ║
║  │ps-architect-001  │     │ps-architect-002  │                                   ║
║  │(Lock File Fix    │     │(Plugin Loading   │                                   ║
║  │ ADR Proposal)    │     │ Fix ADR Proposal)│                                   ║
║  └────────┬─────────┘     └────────┬─────────┘                                   ║
║           │                         │                                            ║
║           └────────────┬────────────┘                                            ║
║                        ▼                                                          ║
║              ╔══════════════════╗                                                ║
║              ║   CHECKPOINT 3   ║                                                ║
║              ╚════════╤═════════╝                                                ║
║                       │                                                          ║
║  ════════════════════════════════════════════════════════════════════════════════ ║
║  PHASE 4: CROSS-VALIDATION (Sequential)                                           ║
║  ════════════════════════════════════════════════════════════════════════════════ ║
║                       │                                                          ║
║                       ▼                                                          ║
║            ┌─────────────────────┐                                               ║
║            │    ps-validator     │                                               ║
║            │ (Validates both     │                                               ║
║            │  proposals against  │                                               ║
║            │  requirements)      │                                               ║
║            └──────────┬──────────┘                                               ║
║                       │                                                          ║
║              ╔════════╧═════════╗                                                ║
║              ║   CHECKPOINT 4   ║                                                ║
║              ╚════════╤═════════╝                                                ║
║                       │                                                          ║
║  ════════════════════════════════════════════════════════════════════════════════ ║
║  PHASE 5: FINAL SYNTHESIS (Fan-In)                                                ║
║  ════════════════════════════════════════════════════════════════════════════════ ║
║                       │                                                          ║
║                       ▼                                                          ║
║            ┌─────────────────────┐                                               ║
║            │   ps-synthesizer    │                                               ║
║            │ (Combines findings, │                                               ║
║            │  patterns, and      │                                               ║
║            │  recommendations)   │                                               ║
║            └──────────┬──────────┘                                               ║
║                       │                                                          ║
║                       ▼                                                          ║
║                  ┌─────────┐                                                     ║
║                  │COMPLETE │                                                     ║
║                  └─────────┘                                                     ║
║                                                                                   ║
╚═══════════════════════════════════════════════════════════════════════════════════╝

LEGEND:
  ┌──────┐  Agent execution (Task tool with subagent_type="general-purpose")
  │      │
  └──────┘

  ╔══════╗  Checkpoint (state saved to ORCHESTRATION.yaml)
  ║      ║
  ╚══════╝

  [PASS]   Quality gate condition (threshold: 0.85)
  [FAIL]   Triggers Generator-Critic loop
```

---

## L2: Phase Execution Details

### Phase 1: Investigation (Fan-Out - PARALLEL)

**Purpose:** Root cause analysis for both bugs using 5 Whys, Ishikawa, and FMEA methodologies.

| Agent ID | Bug | Topic | Severity | Output |
|----------|-----|-------|----------|--------|
| `ps-investigator-bug-001` | BUG-001 | Lock file accumulation | MEDIUM | `investigations/bug-001-e-001-investigation.md` |
| `ps-investigator-bug-002` | BUG-002 | Plugin not loading | HIGH | `investigations/bug-002-e-001-investigation.md` |

**Execution Mode:** PARALLEL (independent investigations)

---

### Phase 2: Review Gate (Fan-Out - PARALLEL)

**Purpose:** Quality assessment of investigations before proceeding. Ensures L0/L1/L2 completeness, evidence quality, and corrective action feasibility.

| Agent ID | Reviews | Criteria | Output |
|----------|---------|----------|--------|
| `ps-reviewer-bug-001` | Investigation BUG-001 | Quality threshold ≥ 0.85 | `reviews/bug-001-review.md` |
| `ps-reviewer-bug-002` | Investigation BUG-002 | Quality threshold ≥ 0.85 | `reviews/bug-002-review.md` |

**Review Criteria (Quality Score Components):**
- 5 Whys completeness (0.20)
- Evidence chain quality (0.25)
- L0/L1/L2 coverage (0.20)
- Corrective action feasibility (0.20)
- Root cause clarity (0.15)

**Execution Mode:** PARALLEL

---

### Phase 2B: Generator-Critic Loop (Conditional)

**Purpose:** Iterative improvement if review quality score < 0.85.

**Pattern:** Generator-Critic (Pattern 8)

```yaml
circuit_breaker:
  max_iterations: 2
  quality_threshold: 0.85
  escalation: human_review
```

| Iteration | Generator | Critic | Output |
|-----------|-----------|--------|--------|
| 1 | ps-investigator (revises based on feedback) | ps-critic (validates revision) | Updated investigation |
| 2 | ps-investigator (final revision) | ps-critic (final validation) | Final investigation |

**Exit Conditions:**
1. Quality score ≥ 0.85 → Proceed to Phase 3
2. Max iterations (2) reached → Escalate to human review

---

### Phase 3: Architecture Proposals (Fan-Out - PARALLEL)

**Purpose:** Design architectural solutions (ADRs) for both bug fixes.

| Agent ID | Bug | Deliverable | Output |
|----------|-----|-------------|--------|
| `ps-architect-bug-001` | BUG-001 | Lock file cleanup ADR | `decisions/ADR-PROJ007-001-lock-file-cleanup.md` |
| `ps-architect-bug-002` | BUG-002 | Plugin loading fix ADR | `decisions/ADR-PROJ007-002-plugin-loading-fix.md` |

**Execution Mode:** PARALLEL

---

### Phase 4: Cross-Validation (Sequential)

**Purpose:** Validate both proposed solutions meet requirements and don't conflict.

| Agent ID | Validates | Criteria | Output |
|----------|-----------|----------|--------|
| `ps-validator` | Both ADRs | Requirements compliance, no conflicts | `validation/cross-validation-report.md` |

**Validation Checks:**
- Proposed solutions address root causes
- No conflicting changes
- Backward compatibility
- Implementation feasibility
- Test strategy adequate

---

### Phase 5: Final Synthesis (Fan-In)

**Purpose:** Combine all findings into comprehensive synthesis with patterns and recommendations.

| Agent ID | Inputs | Output |
|----------|--------|--------|
| `ps-synthesizer` | All investigation reports, reviews, ADRs, validation | `synthesis/final-synthesis.md` |

**Synthesis Contents:**
- L0: Executive summary for stakeholders
- L1: Technical findings and solutions
- L2: Systemic patterns and prevention strategies
- Cross-cutting concerns
- Implementation roadmap

---

## Agent Invocation Templates

### ps-investigator-bug-001 (Phase 1)

```
Task(
  description="ps-investigator: Lock file accumulation",
  subagent_type="general-purpose",
  prompt="""
You are the ps-investigator agent (v2.1.0).

## PS CONTEXT (REQUIRED)
- **PS ID:** bug-001
- **Entry ID:** e-001
- **Topic:** Lock file accumulation in .jerry/local/locks/ causing performance degradation
- **Severity:** MEDIUM

## EVIDENCE ALREADY GATHERED
- 97 lock files in .jerry/local/locks/ (all 0 bytes)
- AtomicFileAdapter creates lock files at line 72-76 but never removes them
- ADR-006 acknowledges "Lock file cleanup needed" but was never implemented
- session_start.py uses AtomicFileAdapter.read_with_lock() creating more lock files

## TASK
1. Apply 5 Whys methodology with evidence for each Why
2. Create Ishikawa diagram categorizing factors
3. Perform FMEA for related risks
4. Propose corrective actions (immediate, short-term, long-term)
5. Create L0/L1/L2 investigation report

## OUTPUT (MANDATORY - P-002)
Write to: projects/PROJ-007-jerry-bugs/investigations/bug-001-e-001-investigation.md

<constraints>
<must_not>Spawn subagents (P-003)</must_not>
<must_not>Return transient output only (P-002)</must_not>
</constraints>
"""
)
```

### ps-investigator-bug-002 (Phase 1)

```
Task(
  description="ps-investigator: Plugin not loading",
  subagent_type="general-purpose",
  prompt="""
You are the ps-investigator agent (v2.1.0).

## PS CONTEXT (REQUIRED)
- **PS ID:** bug-002
- **Entry ID:** e-001
- **Topic:** Jerry plugin not loading when started via claude --plugin-dir
- **Severity:** HIGH

## EVIDENCE ALREADY GATHERED
- hooks.json SessionStart: PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" uv run ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py
- session_start.py PEP 723 metadata: dependencies = [] (empty)
- session_start.py imports from src.infrastructure.* (lines 50-57)
- PROJ-005 fixed manifest validation and added uv run
- User reports no initialization message when running claude --plugin-dir

## TASK
1. Apply 5 Whys methodology with evidence for each Why
2. Test hook execution if possible (or document testing approach)
3. Analyze PYTHONPATH expansion in plugin context
4. Propose corrective actions (immediate, short-term, long-term)
5. Create L0/L1/L2 investigation report

## OUTPUT (MANDATORY - P-002)
Write to: projects/PROJ-007-jerry-bugs/investigations/bug-002-e-001-investigation.md

<constraints>
<must_not>Spawn subagents (P-003)</must_not>
<must_not>Return transient output only (P-002)</must_not>
</constraints>
"""
)
```

### ps-reviewer (Phase 2)

```
Task(
  description="ps-reviewer: Investigation quality review",
  subagent_type="general-purpose",
  prompt="""
You are the ps-reviewer agent.

## TASK
Review the investigation report at: projects/PROJ-007-jerry-bugs/investigations/{bug-id}-e-001-investigation.md

## QUALITY CRITERIA (Score 0.0-1.0)
1. 5 Whys Completeness (0.20): All 5 levels with evidence?
2. Evidence Chain Quality (0.25): Each claim supported?
3. L0/L1/L2 Coverage (0.20): All three levels present and appropriate?
4. Corrective Action Feasibility (0.20): Actions are implementable?
5. Root Cause Clarity (0.15): Root cause is clear and actionable?

## OUTPUT (MANDATORY - P-002)
Write review to: projects/PROJ-007-jerry-bugs/reviews/{bug-id}-review.md

Include:
- Quality score (0.0-1.0)
- Score breakdown by criteria
- Specific feedback for improvement (if score < 0.85)
- PASS/FAIL determination

<constraints>
<must_not>Spawn subagents (P-003)</must_not>
</constraints>
"""
)
```

### ps-architect (Phase 3)

```
Task(
  description="ps-architect: Fix architecture proposal",
  subagent_type="general-purpose",
  prompt="""
You are the ps-architect agent.

## TASK
Based on the investigation report at: projects/PROJ-007-jerry-bugs/investigations/{bug-id}-e-001-investigation.md

Create an Architecture Decision Record (ADR) proposing the fix.

## ADR STRUCTURE
1. Context: Problem being solved
2. Decision Drivers: Constraints and requirements
3. Considered Options: At least 3 options
4. Decision Outcome: Recommended option with rationale
5. Consequences: Positive, negative, neutral
6. Implementation Plan: Steps to implement

## OUTPUT (MANDATORY - P-002)
Write to: projects/PROJ-007-jerry-bugs/decisions/ADR-PROJ007-{nnn}-{slug}.md

<constraints>
<must_not>Spawn subagents (P-003)</must_not>
</constraints>
"""
)
```

---

## State Management

### Checkpoints

| ID | After Phase | Recovery Point |
|----|-------------|----------------|
| CP-001 | Phase 1 complete | Both investigations done |
| CP-002 | Phase 2 complete | Reviews done, critic loops complete |
| CP-003 | Phase 3 complete | ADRs created |
| CP-004 | Phase 4 complete | Validation done |
| CP-005 | Phase 5 complete | Synthesis done, workflow complete |

### Circuit Breaker (Generator-Critic Loop)

```yaml
circuit_breaker:
  max_iterations: 2
  quality_threshold: 0.85
  escalation: human_review

  # If after 2 iterations quality still < 0.85:
  # 1. Mark phase as BLOCKED
  # 2. Create blocker entry
  # 3. Notify for human review
```

---

## Constitutional Compliance

| Principle | Requirement | Implementation |
|-----------|-------------|----------------|
| P-002 | File Persistence | All outputs persisted to files |
| P-003 | No Recursive Subagents | Only main context spawns agents; agents do NOT spawn subagents |
| P-010 | Task Tracking | ORCHESTRATION_WORKTRACKER.md updated after each phase |
| P-022 | No Deception | Honest quality scores and progress reporting |

---

## Expected Artifacts

| Phase | Artifact | Location |
|-------|----------|----------|
| 1 | Investigation BUG-001 | `investigations/bug-001-e-001-investigation.md` |
| 1 | Investigation BUG-002 | `investigations/bug-002-e-001-investigation.md` |
| 2 | Review BUG-001 | `reviews/bug-001-review.md` |
| 2 | Review BUG-002 | `reviews/bug-002-review.md` |
| 3 | ADR Lock File | `decisions/ADR-PROJ007-001-lock-file-cleanup.md` |
| 3 | ADR Plugin | `decisions/ADR-PROJ007-002-plugin-loading-fix.md` |
| 4 | Validation | `validation/cross-validation-report.md` |
| 5 | Synthesis | `synthesis/final-synthesis.md` |

---

## Resumption Instructions

If context compaction occurs, resume by:

1. Read `ORCHESTRATION.yaml` (SSOT)
2. Check `metrics.phases_complete` to determine current phase
3. Check agent statuses within current phase
4. Resume from last checkpoint

```yaml
resumption:
  files_to_read:
    - "orchestration/perf-plugin-investigation-20260114-001/ORCHESTRATION.yaml"
    - "orchestration/perf-plugin-investigation-20260114-001/ORCHESTRATION_PLAN.md"
    - "orchestration/perf-plugin-investigation-20260114-001/ORCHESTRATION_WORKTRACKER.md"
```

---

*Plan Version: 2.0.0*
*Pattern: Fan-Out → Review Gate → Generator-Critic → Architecture → Synthesis*
*Created: 2026-01-14*
*Enhanced: 2026-01-14 (Added critic loops, review gates, architecture phase)*
