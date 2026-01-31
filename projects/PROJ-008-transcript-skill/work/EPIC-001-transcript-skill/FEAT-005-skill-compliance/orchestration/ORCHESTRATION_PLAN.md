# Orchestration Plan: FEAT-005 Skill Compliance

> **Workflow ID:** feat-005-compliance-20260130-001
> **Version:** 3.1.0
> **Status:** APPROVED
> **Created:** 2026-01-30T22:00:00Z
> **Updated:** 2026-01-31T05:00:00Z
> **Location:** FEAT-005-skill-compliance/orchestration/
> **Execution Mode:** Background for parallel tracks (DEC-003)

---

## Version History

| Version | Date | Change | Rationale |
|---------|------|--------|-----------|
| 1.0.0 | 2026-01-30 | Initial creation | Workflow established |
| 2.0.0 | 2026-01-30 | Added parallel tracks | Optimize execution time |
| 2.1.0 | 2026-01-31 | Added adversarial prompting | Quality gate rigor |
| 2.2.0 | 2026-01-31 | Added feedback loop config | Iteration tracking |
| 3.0.0 | 2026-01-31 | TASK-419 as Phase 0 sequential gate | DISC-003: Dependency chain flaw correction |
| **3.1.0** | **2026-01-31** | **Background execution for parallel tracks** | **DEC-003: True parallelism enabled** |

---

## Executive Summary (L0)

This orchestration plan coordinates **execution** of the 25 pre-designed tasks for FEAT-005 skill compliance.

**CRITICAL CHANGE in v3.0:** TASK-419 (Model Parameter Validation) is now a **Phase 0 sequential prerequisite** that MUST complete successfully before ANY parallel work begins. This corrects the dependency chain flaw identified in [DISC-003](../FEAT-005--DISC-003-orchestration-dependency-chain-flaw.md).

### Key Principles (v3.1)

1. **Phase 0 Gate:** TASK-419 validates Task tool model parameter BEFORE anything else
2. **Phase 0 Failure = Hard Blocker:** If TASK-419 fails, escalate to user - do NOT proceed
3. **Background Execution (v3.1):** Track agents run in background to enable TRUE parallelism
4. **Adversarial Critic:** ps-critic evaluates after EACH enabler with 6 adversarial patterns
5. **No Ambiguity:** Cross-pollination points fully documented with explicit triggers and artifacts

### Execution Mode (v3.1 - DEC-003)

| Component | Mode | Rationale |
|-----------|------|-----------|
| Phase 0 (TASK-419) | Foreground | Blocking gate - must know PASS/FAIL first |
| Track A agents | **Background** | Enable true parallelism with Track B |
| Track B agents | **Background** | Enable true parallelism with Track A |
| ps-critic | Foreground | Quick evaluation, simpler iterative refinement |

**Key Insight:** Each Task agent gets its own context window. Background execution does NOT degrade quality because agents read/write files, not shared memory. Foreground execution would make parallel tracks impossible.

### Decision References

- [DISC-003: Orchestration v2.x Dependency Chain Flaw](../FEAT-005--DISC-003-orchestration-dependency-chain-flaw.md)
- [DEC-002: Orchestration v3.0 Design Decisions](../FEAT-005--DEC-002-orchestration-v3-design-decisions.md)
- [DEC-003: Background Execution for Parallel Tracks](../FEAT-005--DEC-003-background-execution-for-parallelism.md)

---

## Workflow Diagram (v3.0)

```
FEAT-005 SKILL COMPLIANCE EXECUTION (v3.0)
═══════════════════════════════════════════

                        ┌─────────────────────────────────┐
                        │        WORKFLOW START           │
                        │   feat-005-compliance-20260130  │
                        └───────────────┬─────────────────┘
                                        │
                                        ▼
╔═══════════════════════════════════════════════════════════════════════════════╗
║                     PHASE 0: SEQUENTIAL HARD GATE                              ║
║                     TASK-419: Validate Task tool model parameter               ║
║                     Effort: 2h | CRITICAL - Must complete first                ║
╚═══════════════════════════════════════════════════════════════════════════════╝
                                        │
                                        ▼
                    ┌───────────────────────────────────────┐
                    │      PHASE 0 RESULT CHECK             │
                    │                                       │
                    │   ┌─────────────┐  ┌─────────────┐   │
                    │   │    PASS     │  │    FAIL     │   │
                    │   └──────┬──────┘  └──────┬──────┘   │
                    │          │                │          │
                    └──────────┼────────────────┼──────────┘
                               │                │
                               │                ▼
                               │      ╔════════════════════════════╗
                               │      ║   HARD BLOCKER             ║
                               │      ║   Escalate to User         ║
                               │      ║   DO NOT PROCEED           ║
                               │      ║                            ║
                               │      ║   Options:                 ║
                               │      ║   a) Provide workaround    ║
                               │      ║   b) Descope EN-031        ║
                               │      ║   c) Manual intervention   ║
                               │      ╚════════════════════════════╝
                               │
                               ▼
         ┌─────────────────────────────────────────────────────────────┐
         │               CROSS-POLLINATION POINT CP-1                  │
         │  TASK-419 results → inform EN-027 agent definition design   │
         │  Artifact: EN-031.../TASK-419-validate-task-model.md        │
         └─────────────────────────────────────────────────────────────┘
                               │
                               ▼
              ╔════════════════════════════════════════════════╗
              ║   PHASE 1+: PARALLEL TRACKS BEGIN HERE         ║
              ║   (Only after Phase 0 PASS)                    ║
              ╚════════════════════════════════════════════════╝
                               │
              ┌────────────────┴────────────────┐
              │                                 │
              ▼                                 ▼
╔═══════════════════════════════════════╗   ╔═══════════════════════════════════════╗
║  TRACK A: SEQUENTIAL COMPLIANCE       ║   ║  TRACK B: MODEL SELECTION (PARALLEL)  ║
║  EN-027 → EN-028 → EN-029 → EN-030    ║   ║  EN-031 Phases 2-3 (After TASK-419)   ║
║  33 hours sequential                  ║   ║  32 hours remaining                   ║
╚═══════════════════════════════════════╝   ╚═══════════════════════════════════════╝
              │                                 │
              ▼                                 ▼
┌─────────────────────────────────────┐   ┌─────────────────────────────────────┐
│  EN-027: Agent Definition (10h)     │   │  EN-031 Phase 2: Implementation     │
│  ───────────────────────────────────│   │  ───────────────────────────────────│
│  TASK-400: Add identity section     │   │  TASK-420: Add CLI model params     │
│  TASK-401: Add capabilities section │   │  TASK-421: Update SKILL.md docs     │
│  TASK-402: Add guardrails section   │   │  TASK-422: Update agent definitions │
│  TASK-403: Add validation section   │   │  TASK-423: Implement profiles       │
│  TASK-404: Add constitution section │   │                                     │
│  TASK-405: Add session_context      │   │  Effort: 24h                        │
│  TASK-406: Validate compliance      │   │                                     │
│                                     │   │  ┌───────────────────────────────┐  │
│  ┌───────────────────────────────┐  │   │  │ CP-3: TASK-420 results inform │  │
│  │ 🔄 ps-critic GATE G-027       │  │   │  │      SKILL.md documentation   │  │
│  │    Threshold: >= 0.90         │  │   │  └───────────────────────────────┘  │
│  │    Adversarial Mode: ENABLED  │  │   └──────────────────┬──────────────────┘
│  └───────────────────────────────┘  │                      │
└──────────────────┬──────────────────┘                      │
                   │                                         │
    ┌──────────────┴──────────────────────────┐             │
    │ CP-2: EN-027 agent patterns inform      │             │
    │       TASK-422 agent definitions        │             │
    └──────────────┬──────────────────────────┘             │
                   │                                         │
                   ▼                                         │
┌─────────────────────────────────────┐                      │
│  EN-028: SKILL.md Compliance (9h)   │                      │
│  ───────────────────────────────────│                      │
│  TASK-407: Add invoking section     │                      │
│  TASK-408: Enhance state passing    │                      │
│  TASK-409: Add persistence section  │                      │
│  TASK-410: Add self-critique        │                      │
│  TASK-411: Restructure persona      │                      │
│                                     │                      │
│  ┌───────────────────────────────┐  │                      │
│  │ 🔄 ps-critic GATE G-028       │  │                      │
│  │    Threshold: >= 0.90         │  │                      │
│  │    Adversarial Mode: ENABLED  │  │                      │
│  └───────────────────────────────┘  │                      │
└──────────────────┬──────────────────┘                      │
                   │                                         │
                   ▼                                         ▼
┌─────────────────────────────────────┐   ┌─────────────────────────────────────┐
│  EN-029: Documentation (9h)         │   │  EN-031 Phase 3: Testing            │
│  ───────────────────────────────────│   │  ───────────────────────────────────│
│  TASK-412: Add L2 architect section │   │  TASK-424: Integration testing      │
│  TASK-413: Create anti-patterns     │   │                                     │
│  TASK-414: Declare pattern refs     │   │  Effort: 8h                         │
│  TASK-415: Add constraints section  │   │                                     │
│                                     │   │  ┌───────────────────────────────┐  │
│  ┌───────────────────────────────┐  │   │  │ 🔄 ps-critic GATE G-031       │  │
│  │ 🔄 ps-critic GATE G-029       │  │   │  │    Threshold: >= 0.90         │  │
│  │    Threshold: >= 0.90         │  │   │  │    Adversarial Mode: ENABLED  │  │
│  │    Adversarial Mode: ENABLED  │  │   │  └───────────────────────────────┘  │
│  └───────────────────────────────┘  │   └──────────────────┬──────────────────┘
└──────────────────┬──────────────────┘                      │
                   │                                         │
                   ▼                                         │
┌─────────────────────────────────────┐                      │
│  EN-030: Documentation Polish (5h)  │                      │
│  ───────────────────────────────────│                      │
│  TASK-416: Add tool examples        │                      │
│  TASK-417: Add design rationale     │                      │
│  TASK-418: Add cross-skill refs     │                      │
│                                     │                      │
│  ┌───────────────────────────────┐  │                      │
│  │ 🔄 ps-critic GATE G-030       │  │                      │
│  │    Threshold: >= 0.95         │  │                      │
│  │    Adversarial Mode: ENABLED  │  │                      │
│  └───────────────────────────────┘  │                      │
└──────────────────┬──────────────────┘                      │
                   │                                         │
                   └─────────────────┬───────────────────────┘
                                     │
                                     ▼
                   ╔═════════════════════════════════════════╗
                   ║         FINAL QUALITY GATE G-FINAL      ║
                   ║    ps-critic aggregate >= 0.90          ║
                   ║    All 25 tasks complete                ║
                   ║    Compliance score >= 95%              ║
                   ║    Adversarial Mode: ENABLED            ║
                   ╚═════════════════════════════════════════╝
                                     │
                                     ▼
                   ┌─────────────────────────────────────────┐
                   │          WORKFLOW COMPLETE              │
                   │     FEAT-005 at 95%+ Compliance         │
                   └─────────────────────────────────────────┘

LEGEND:
═══════
🔄  ps-critic quality gate (adversarial validation)
→   Sequential dependency
CP-x Cross-pollination point (see detailed spec below)
```

---

## Phase 0: Sequential Hard Gate (CRITICAL)

> **RATIONALE:** DISC-003 identified that TASK-419 must complete BEFORE parallel tracks begin.
> If TASK-419 fails, the entire model selection feature (EN-031) may be invalid, and we should
> not waste effort on Track A agent definitions that assume model selection works.

### TASK-419: Validate Task Tool Model Parameter

| Attribute | Value |
|-----------|-------|
| **ID** | TASK-419 |
| **Title** | Validate Task tool model parameter |
| **Effort** | 2h |
| **Priority** | CRITICAL |
| **Phase** | 0 (Sequential Hard Gate) |
| **Blocks** | ALL downstream work (Track A and Track B Phase 2-3) |

**Acceptance Criteria:**
1. Confirm `model` parameter exists in Task tool schema
2. Test invocation with `model: "haiku"` - verify haiku model is used
3. Test invocation with `model: "sonnet"` - verify sonnet model is used
4. Document exact parameter values (e.g., "haiku" vs "claude-3-haiku")
5. Document any limitations or edge cases discovered

**Output Artifact:**
- Path: `EN-031-model-selection-capability/TASK-419-validate-task-model.md`
- Must include: Test results, exact parameter syntax, validation status

### Phase 0 Failure Handling

```
IF TASK-419 FAILS:
┌─────────────────────────────────────────────────────────────────────────────┐
│                           HARD BLOCKER PROTOCOL                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. DO NOT PROCEED with ANY parallel work                                   │
│                                                                             │
│  2. Create IMPEDIMENT document:                                             │
│     Path: FEAT-005--IMP-001-task-tool-model-param-failure.md                │
│     Content: Failure details, attempted tests, exact error messages         │
│                                                                             │
│  3. Escalate to User via AskUserQuestion:                                   │
│     ┌─────────────────────────────────────────────────────────────────────┐│
│     │ "CRITICAL: TASK-419 (Model Parameter Validation) FAILED.            ││
│     │                                                                      ││
│     │ Finding: {detailed failure description}                              ││
│     │                                                                      ││
│     │ This blocks the entire EN-031 Model Selection feature and affects   ││
│     │ how EN-027 agent definitions should be structured.                   ││
│     │                                                                      ││
│     │ Options:                                                             ││
│     │ a) Provide workaround or alternative approach                        ││
│     │ b) Descope EN-031 entirely, proceed with Track A only               ││
│     │ c) Pause workflow for manual investigation                           ││
│     │ d) Accept limitation and document as known constraint"              ││
│     └─────────────────────────────────────────────────────────────────────┘│
│                                                                             │
│  4. WAIT for user decision before ANY further work                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Cross-Pollination Specification (No Ambiguity)

> **Reference:** DEC-002:D-005 requires detailed cross-pollination with no ambiguity.

### CP-1: TASK-419 → Track A (EN-027)

| Attribute | Value |
|-----------|-------|
| **ID** | CP-1 |
| **Trigger** | TASK-419 completion (PASS or FAIL) |
| **Source** | Phase 0 (TASK-419) |
| **Target** | Track A (EN-027 specifically) |
| **Information Transferred** | Model parameter validation results |

**Detailed Information Flow:**

```
TASK-419 OUTPUT (Source)                          EN-027 CONSUMPTION (Target)
─────────────────────────                         ────────────────────────────
TASK-419-validate-task-model.md contains:         EN-027 agent definitions use:

1. Model parameter syntax                    →    1. Correct model override syntax
   e.g., "model: haiku" or "model: claude-3-haiku"   in agent YAML sections

2. Validation status (PASS/FAIL)             →    2. Whether to include model
                                                     override capability at all

3. Edge cases discovered                     →    3. Guardrails for model selection
   e.g., "opus not available for subagents"          input_validation rules

4. Recommended default values                →    4. Default model in agent
   e.g., "haiku for simple tasks"                    definitions
```

**Artifact Path:** `EN-031-model-selection-capability/TASK-419-validate-task-model.md`

**If PASS:** EN-027 proceeds with model override capability in agent definitions
**If FAIL:** HARD GATE - escalate to user for decision (see Phase 0 Failure Handling)

---

### CP-2: EN-027 → TASK-422

| Attribute | Value |
|-----------|-------|
| **ID** | CP-2 |
| **Trigger** | EN-027 quality gate G-027 PASS |
| **Source** | Track A (EN-027) |
| **Target** | Track B (TASK-422) |
| **Information Transferred** | Agent YAML schema patterns for model override |

**Detailed Information Flow:**

```
EN-027 OUTPUT (Source)                            TASK-422 CONSUMPTION (Target)
─────────────────────                             ──────────────────────────────
Agent definition files contain:                   TASK-422 uses these patterns to:

1. Standard YAML structure for agents        →    1. Add model_override section
   (identity, capabilities, guardrails...)           using consistent structure

2. session_context.schema definition         →    2. Add model configuration to
   showing how state is passed                       session_context schema

3. Constitution compliance patterns          →    3. Ensure model selection follows
   (principles_applied section)                      P-020 (user authority)

4. Guardrails patterns                       →    4. Add model-specific input
   (input_validation, output_filtering)              validation rules
```

**Artifact Paths:**
- Source: `skills/transcript/agents/ts-*.md` (5 agent files)
- Target: `EN-031-model-selection-capability/TASK-422-update-agent-definitions.md`

**When Available:** After G-027 passes (EN-027 complete)

---

### CP-3: TASK-420 → SKILL.md Documentation

| Attribute | Value |
|-----------|-------|
| **ID** | CP-3 |
| **Trigger** | TASK-420 completion |
| **Source** | Track B (TASK-420) |
| **Target** | Track A (influences EN-028/TASK-421 documentation) |
| **Information Transferred** | CLI parameter design (--model-* flags) |

**Detailed Information Flow:**

```
TASK-420 OUTPUT (Source)                          SKILL.md CONSUMPTION (Target)
─────────────────────                             ─────────────────────────────
CLI parameter implementation contains:            SKILL.md documentation needs:

1. Exact CLI flag syntax                     →    1. Usage examples in SKILL.md
   e.g., "--model-parser haiku"                      "Invoking the Skill" section

2. Parameter validation rules                →    2. Input validation documentation
   e.g., "must be: haiku|sonnet|opus"               in "Parameters" table

3. Default behavior                          →    3. Default values documented
   e.g., "if not specified, inherit"                in parameter descriptions

4. Profile definitions                       →    4. Model profile documentation
   e.g., "economy: haiku for all"                   in new "Model Profiles" section
```

**Artifact Path:** `EN-031-model-selection-capability/TASK-420-add-cli-model-params.md`

**When Available:** After TASK-420 complete

---

## Execution Timeline (v3.0)

```
Day 0 (2h):    PHASE 0 - SEQUENTIAL HARD GATE
               └── TASK-419: Validate Task tool model parameter

               IF FAIL → ESCALATE TO USER, STOP
               IF PASS → CONTINUE

Day 1-2:       PARALLEL TRACKS BEGIN
               ├── Track A: EN-027 tasks (TASK-400 through TASK-406)
               │   Uses CP-1 results for model override design
               │
               └── Track B: TASK-420, TASK-421 (CLI + docs)
                   Parallel with EN-027

Day 2:         CROSS-POLLINATION CHECKPOINT
               ├── CP-2: EN-027 complete → inform TASK-422
               │   Agent YAML patterns feed into agent definition updates
               │
               └── CP-3: TASK-420 complete → inform EN-028 docs
                   CLI design informs SKILL.md documentation

Day 2-3:       CONTINUE PARALLEL
               ├── Track A: EN-027 ps-critic gate G-027 (adversarial)
               │   Then EN-028 tasks (TASK-407 through TASK-411)
               │
               └── Track B: TASK-422, TASK-423 (agent defs + profiles)

Day 3-4:       CONTINUE PARALLEL
               ├── Track A: EN-028 ps-critic gate G-028 (adversarial)
               │   Then EN-029 tasks (TASK-412 through TASK-415)
               │
               └── Track B: TASK-424 (integration testing)

Day 4-5:       TRACK A COMPLETION
               ├── Track A: EN-029 ps-critic gate G-029 (adversarial)
               │   Then EN-030 tasks (TASK-416 through TASK-418)
               │
               └── Track B: ps-critic gate G-031 (adversarial)

Day 5-6:       FINAL CONVERGENCE
               ├── Track A: EN-030 ps-critic gate G-030 (adversarial, threshold 0.95)
               │
               └── FINAL QUALITY GATE G-FINAL (adversarial)
                   All 25 tasks complete, aggregate >= 0.90
```

**Efficiency:** ~6 days total vs ~8 days pure sequential (25% improvement)
**Phase 0 overhead:** +2h but prevents potential rework from invalid assumptions

---

## Adversarial Critic Integration

> **Reference:** DISC-002 documents 6 adversarial patterns
> **Reference:** DEC-002:D-002 mandates adversarial critic after each enabler

### When ps-critic Runs

| Trigger | Gate | Threshold | Adversarial Patterns |
|---------|------|-----------|----------------------|
| TASK-419 complete | (Validation only) | - | N/A (simple pass/fail) |
| EN-027 complete | G-027 | 0.90 | All 6 patterns |
| EN-028 complete | G-028 | 0.90 | All 6 patterns |
| EN-029 complete | G-029 | 0.90 | All 6 patterns |
| EN-030 complete | G-030 | 0.95 | All 6 patterns |
| EN-031 complete | G-031 | 0.90 | All 6 patterns |
| All complete | G-FINAL | 0.90 | All 6 patterns |

### Adversarial Prompt Template (v3.0)

```markdown
## ADVERSARIAL EVALUATION MODE ACTIVATED

You are operating as an ADVERSARIAL CRITIC for quality gate {GATE_ID}.
Apply ALL six adversarial patterns:
1. Red Team Framing - Assume problems exist until proven otherwise
2. Mandatory Findings - Identify ≥3 issues (any severity)
3. Devil's Advocate - Challenge each claim with counter-examples
4. Checklist Enforcement - No partial credit, evidence required
5. Counter-Examples - Find failure scenarios for each decision
6. Score Calibration - First-pass typically 0.60-0.80

**Iteration:** {N} of 3
**Previous Score:** {score or N/A}
**Threshold:** {threshold}
**Gate:** {GATE_ID}

Evaluate the following deliverables against {CRITERIA}:
{deliverable_list}

REMEMBER: A review finding zero issues requires explicit justification.
A score >= 0.95 requires heavy justification with cited evidence.
```

### Feedback Loop (3 Iterations Max)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ADVERSARIAL FEEDBACK LOOP (Max 3 iterations per gate)                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. Complete enabler tasks                                                  │
│  2. Submit to ps-critic with adversarial prompt                             │
│  3. ps-critic returns score and findings                                    │
│                                                                             │
│  IF score >= threshold:                                                     │
│     → PASS, proceed to next enabler                                         │
│                                                                             │
│  IF score < threshold AND iteration < 3:                                    │
│     → REFINE: Address findings, re-submit                                   │
│                                                                             │
│  IF score < threshold AND iteration >= 3:                                   │
│     → ESCALATE: Create impediment, ask user for decision                    │
│                                                                             │
│  Critique artifacts: orchestration/critiques/{gate-id}-iteration-{n}.md    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Quality Gates Summary

| Gate | Enabler | Threshold | Criteria | Max Iterations |
|------|---------|-----------|----------|----------------|
| (Phase 0) | TASK-419 | PASS/FAIL | Model param works | 1 (hard gate) |
| G-027 | EN-027 | 0.90 | Agent Compliance Checklist A-001 to A-043 | 3 |
| G-028 | EN-028 | 0.90 | SKILL.md Compliance S-001 to S-051 | 3 |
| G-029 | EN-029 | 0.90 | PLAYBOOK.md Triple-Lens Checklist | 3 |
| G-030 | EN-030 | 0.95 | Final polish, no regressions | 3 |
| G-031 | EN-031 | 0.90 | Model selection requirements | 3 |
| G-FINAL | All | 0.90 | Aggregate >= 95%, all 25 tasks | 1 |

---

## Task Inventory (25 Tasks Total)

### Phase 0: Sequential Gate (1 task, 2h)

| Task ID | Title | Effort | Enabler | Phase |
|---------|-------|--------|---------|-------|
| TASK-419 | Validate Task tool model parameter | 2h | EN-031 | 0 (Hard Gate) |

### Track A: Sequential Compliance Chain (19 tasks, 33h)

**EN-027: Agent Definition Compliance (7 tasks, 10h)**

| Task ID | Title | Effort |
|---------|-------|--------|
| TASK-400 | Add identity section | 1h |
| TASK-401 | Add capabilities section | 1.5h |
| TASK-402 | Add guardrails section | 3h |
| TASK-403 | Add validation section | 2h |
| TASK-404 | Add constitution section | 1h |
| TASK-405 | Add session_context section | 1h |
| TASK-406 | Validate agent compliance | 0.5h |

**EN-028: SKILL.md Compliance (5 tasks, 9h)**

| Task ID | Title | Effort |
|---------|-------|--------|
| TASK-407 | Add invoking section | 1h |
| TASK-408 | Enhance state passing | 2h |
| TASK-409 | Add persistence section | 1h |
| TASK-410 | Add self-critique | 1h |
| TASK-411 | Restructure persona/output | 2h |

**EN-029: Documentation Compliance (4 tasks, 9h)**

| Task ID | Title | Effort |
|---------|-------|--------|
| TASK-412 | Add L2 architect section | 3h |
| TASK-413 | Create anti-patterns | 3h |
| TASK-414 | Declare pattern refs | 2h |
| TASK-415 | Add constraints section | 1h |

**EN-030: Documentation Polish (3 tasks, 5h)**

| Task ID | Title | Effort |
|---------|-------|--------|
| TASK-416 | Add tool examples | 2h |
| TASK-417 | Add design rationale | 2h |
| TASK-418 | Add cross-skill refs | 1h |

### Track B: Model Selection (5 tasks, 32h after Phase 0)

**EN-031 Phase 2: Implementation (4 tasks, 24h)**

| Task ID | Title | Effort |
|---------|-------|--------|
| TASK-420 | Add CLI model params | 8h |
| TASK-421 | Update SKILL.md docs | 4h |
| TASK-422 | Update agent definitions | 4h |
| TASK-423 | Implement profiles | 8h |

**EN-031 Phase 3: Testing (1 task, 8h)**

| Task ID | Title | Effort |
|---------|-------|--------|
| TASK-424 | Integration testing | 8h |

---

## Checkpoints

| ID | Trigger | Recovery Point | Artifacts |
|----|---------|----------------|-----------|
| CP-PHASE0 | TASK-419 complete | Phase 0 done | Validation results |
| CP-001 | EN-027 complete | Agent definitions done | Backup of agent .md files |
| CP-002 | EN-028 complete | SKILL.md stable | SKILL.md backup |
| CP-003 | EN-029 complete | Docs structure done | PLAYBOOK.md, RUNBOOK.md |
| CP-004 | EN-030 complete | Track A done | All documentation |
| CP-005 | EN-031 complete | Track B done | CLI + profiles |
| CP-FINAL | All complete | Workflow done | Full artifact set |

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Phase 0 Pass | PASS | TASK-419 validates model param works |
| Compliance Score | >= 95% | Checklist completion |
| Tasks Complete | 25/25 | All TASK-4xx files marked complete |
| Quality Gates Passed | 7/7 | Phase 0 + G-027 through G-FINAL |
| Parallel Efficiency | >= 25% | Days saved vs pure sequential |

---

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| TASK-419 fails | Medium | Critical | **Phase 0 hard gate; user decision required** |
| ps-critic rejection loop | Low | Medium | Max 3 iterations; escalate with documented gaps |
| Cross-pollination timing | Low | Medium | Explicit trigger points with artifact paths |
| Breaking existing pipelines | Medium | High | Checkpoint before each enabler |

---

## References

- [DISC-003: Orchestration v2.x Dependency Chain Flaw](../FEAT-005--DISC-003-orchestration-dependency-chain-flaw.md)
- [DEC-002: Orchestration v3.0 Design Decisions](../FEAT-005--DEC-002-orchestration-v3-design-decisions.md)
- [DISC-002: Adversarial Prompting Protocol](../../FEAT-003-future-enhancements/FEAT-003--DISC-002-adversarial-prompting-protocol.md)
- [FEAT-005 Feature Definition](../FEAT-005-skill-compliance.md)
- [EN-027 Agent Definition Compliance](../EN-027-agent-definition-compliance/EN-027-agent-definition-compliance.md)
- [EN-031 Model Selection](../EN-031-model-selection-capability/EN-031-model-selection-capability.md)

---

*Orchestration Plan Version: 3.1.0*
*Status: APPROVED*
*Key Changes: Phase 0 sequential hard gate (v3.0) + Background execution for parallelism (v3.1)*
*Constitutional Compliance: P-002, P-003, P-020*
*Created: 2026-01-30*
*Updated: 2026-01-31 - v3.1.0 adds background execution per DEC-003*
