# ORCHESTRATION_PLAN: Performance and Plugin Bug Investigations

> **Workflow ID:** perf-plugin-investigation-20260114-001
> **Project:** PROJ-007-jerry-bugs
> **Pattern:** Fan-Out / Fan-In
> **Status:** ACTIVE
> **Created:** 2026-01-14
> **Constitutional Compliance:** Jerry Constitution v1.0 (P-003: No Recursive Subagents)

---

## L0: Executive Summary (ELI5)

This orchestration coordinates **two parallel investigations** into critical Jerry Framework bugs:

1. **BUG-001 (Performance):** Lock files accumulating in `.jerry/local/locks/` causing slowdowns
2. **BUG-002 (Plugin Loading):** Jerry plugin not loading when started via `--plugin-dir`

Both investigations run **in parallel** using the ps-investigator agent, then findings are **synthesized** to identify cross-cutting patterns or shared root causes.

---

## L1: Workflow Diagram

```
+============================================================================+
|                    WORKFLOW: perf-plugin-investigation-20260114-001         |
|                    PATTERN: Fan-Out / Fan-In                                |
+============================================================================+
|                                                                             |
|                         ┌─────────────────────┐                             |
|                         │    ORCHESTRATOR     │                             |
|                         │   (Main Context)    │                             |
|                         └──────────┬──────────┘                             |
|                                    │                                        |
|                    ┌───────────────┴───────────────┐                        |
|                    │                               │                        |
|                    ▼                               ▼                        |
|     ┌──────────────────────────┐   ┌──────────────────────────┐            |
|     │  PHASE 1A: BUG-001       │   │  PHASE 1B: BUG-002       │            |
|     │  ps-investigator         │   │  ps-investigator         │            |
|     │  (Lock File Accumulation)│   │  (Plugin Not Loading)    │            |
|     │                          │   │                          │            |
|     │  Severity: MEDIUM        │   │  Severity: HIGH          │            |
|     └────────────┬─────────────┘   └────────────┬─────────────┘            |
|                  │                               │                          |
|                  │       ╔═══════════════╗       │                          |
|                  └──────►║  CHECKPOINT   ║◄──────┘                          |
|                          ║    CP-001     ║                                  |
|                          ╚═══════════════╝                                  |
|                                  │                                          |
|                                  ▼                                          |
|                    ┌─────────────────────────┐                              |
|                    │      PHASE 2:           │                              |
|                    │   SYNTHESIS             │                              |
|                    │   (Combine Findings)    │                              |
|                    └────────────┬────────────┘                              |
|                                 │                                           |
|                                 ▼                                           |
|                    ┌─────────────────────────┐                              |
|                    │      COMPLETE           │                              |
|                    │   Investigation Reports │                              |
|                    │   + Synthesis Document  │                              |
|                    └─────────────────────────┘                              |
|                                                                             |
+============================================================================+

LEGEND:
  ┌──────┐  Agent execution (Task tool)
  │      │
  └──────┘

  ╔══════╗  Checkpoint (state saved)
  ║      ║
  ╚══════╝
```

---

## L2: Execution Details

### Phase 1: Parallel Investigations (Fan-Out)

**Execution Mode:** PARALLEL

| Agent ID | Bug | Topic | Severity | Output Location |
|----------|-----|-------|----------|-----------------|
| `ps-investigator-bug-001` | BUG-001 | Lock file accumulation | MEDIUM | `investigations/bug-001-e-001-investigation.md` |
| `ps-investigator-bug-002` | BUG-002 | Plugin not loading | HIGH | `investigations/bug-002-e-001-investigation.md` |

**PS CONTEXT for each agent:**

```yaml
# BUG-001
PS_CONTEXT:
  PS_ID: bug-001
  Entry_ID: e-001
  Topic: "Lock file accumulation in .jerry/local/locks/ causing performance degradation"
  Severity: MEDIUM

# BUG-002
PS_CONTEXT:
  PS_ID: bug-002
  Entry_ID: e-001
  Topic: "Jerry plugin not loading when started via claude --plugin-dir"
  Severity: HIGH
```

### Phase 2: Synthesis (Fan-In)

**Execution Mode:** SEQUENTIAL (after Phase 1 complete)

| Step | Action | Output |
|------|--------|--------|
| 2.1 | Read both investigation reports | - |
| 2.2 | Identify cross-cutting patterns | - |
| 2.3 | Create synthesis document | `synthesis/investigation-synthesis.md` |

---

## Agent Invocation Templates

### ps-investigator-bug-001

```
Task(
  description="ps-investigator: Lock file accumulation",
  subagent_type="general-purpose",
  prompt="""
You are the ps-investigator agent (v2.1.0).

<agent_context>
<role>Investigation Specialist with expertise in root cause analysis</role>
<task>Investigate lock file accumulation causing performance degradation</task>
<constraints>
<must>Create file with Write tool at projects/PROJ-007-jerry-bugs/investigations/bug-001-e-001-investigation.md</must>
<must>Include L0/L1/L2 output levels</must>
<must>Complete 5 Whys with evidence</must>
<must>Define corrective actions with owners</must>
<must_not>Spawn subagents (P-003)</must_not>
<must_not>Return transient output only (P-002)</must_not>
<must_not>Conclude without evidence (P-001)</must_not>
</constraints>
</agent_context>

## PS CONTEXT (REQUIRED)
- **PS ID:** bug-001
- **Entry ID:** e-001
- **Topic:** Lock file accumulation in .jerry/local/locks/ causing performance degradation
- **Severity:** MEDIUM

## EVIDENCE ALREADY GATHERED
- 97 lock files in .jerry/local/locks/ (all 0 bytes)
- AtomicFileAdapter creates lock files at line 72-76 but never removes them
- ADR-006 acknowledges "Lock file cleanup needed for crashed processes" but was never implemented
- session_start.py uses AtomicFileAdapter.read_with_lock() creating more lock files

## INVESTIGATION TASK
1. Apply 5 Whys methodology to determine root cause
2. Use Ishikawa diagram to categorize contributing factors
3. Propose corrective actions (immediate, short-term, long-term)
4. Create investigation report with L0/L1/L2 output levels
5. Persist report to: projects/PROJ-007-jerry-bugs/investigations/bug-001-e-001-investigation.md
"""
)
```

### ps-investigator-bug-002

```
Task(
  description="ps-investigator: Plugin not loading",
  subagent_type="general-purpose",
  prompt="""
You are the ps-investigator agent (v2.1.0).

<agent_context>
<role>Investigation Specialist with expertise in root cause analysis</role>
<task>Investigate Jerry plugin not loading when started via --plugin-dir</task>
<constraints>
<must>Create file with Write tool at projects/PROJ-007-jerry-bugs/investigations/bug-002-e-001-investigation.md</must>
<must>Include L0/L1/L2 output levels</must>
<must>Complete 5 Whys with evidence</must>
<must>Define corrective actions with owners</must>
<must_not>Spawn subagents (P-003)</must_not>
<must_not>Return transient output only (P-002)</must_not>
<must_not>Conclude without evidence (P-001)</must_not>
</constraints>
</agent_context>

## PS CONTEXT (REQUIRED)
- **PS ID:** bug-002
- **Entry ID:** e-001
- **Topic:** Jerry plugin not loading when started via claude --plugin-dir
- **Severity:** HIGH

## EVIDENCE ALREADY GATHERED
- hooks.json SessionStart uses: PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" uv run ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py
- session_start.py PEP 723 metadata has dependencies = [] (empty)
- session_start.py imports from src.infrastructure.* (lines 50-57)
- PROJ-005-plugin-bugs fixed manifest validation and added uv run
- User reports no initialization message or interaction when running claude --plugin-dir

## INVESTIGATION TASK
1. Apply 5 Whys methodology to determine root cause
2. Test hook execution manually if possible
3. Verify PYTHONPATH expansion and uv run behavior
4. Propose corrective actions (immediate, short-term, long-term)
5. Create investigation report with L0/L1/L2 output levels
6. Persist report to: projects/PROJ-007-jerry-bugs/investigations/bug-002-e-001-investigation.md
"""
)
```

---

## State Management

### Checkpoints

| ID | Trigger | Recovery Point |
|----|---------|----------------|
| CP-001 | Both Phase 1 agents complete | Before synthesis |
| CP-002 | Synthesis complete | Workflow done |

### Blockers

Any agent failure will create a blocker entry in ORCHESTRATION.yaml.

---

## Constitutional Compliance

| Principle | Requirement | Implementation |
|-----------|-------------|----------------|
| P-002 | File Persistence | All state persisted to ORCHESTRATION.yaml and agent outputs |
| P-003 | No Recursive Subagents | Main context invokes ps-investigator workers only; workers do NOT spawn agents |
| P-010 | Task Tracking | ORCHESTRATION_WORKTRACKER.md updated after each phase |
| P-022 | No Deception | Honest status and progress reporting |

---

## Related Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| ORCHESTRATION.yaml | `orchestration/perf-plugin-investigation-20260114-001/` | Machine-readable SSOT |
| ORCHESTRATION_WORKTRACKER.md | `orchestration/perf-plugin-investigation-20260114-001/` | Tactical execution tracking |
| Investigation BUG-001 | `investigations/bug-001-e-001-investigation.md` | Lock file investigation report |
| Investigation BUG-002 | `investigations/bug-002-e-001-investigation.md` | Plugin loading investigation report |
| Synthesis | `orchestration/.../synthesis/investigation-synthesis.md` | Combined findings |

---

*Plan Version: 1.0.0*
*Created: 2026-01-14*
