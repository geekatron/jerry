# ps-critic Circuit Breaker Guidance

> Circuit breaker logic for orchestrator-managed generator-critic loops, including parameters, decision logic, and worked workflow example. The ps-critic agent itself does NOT implement this logic (P-003 compliant); this is reference material for the orchestrating context.

## Default Parameters

> **SSOT Reference:** Threshold and minimum iterations defined in `.context/rules/quality-enforcement.md` (H-13, H-14).

```yaml
circuit_breaker:
  min_iterations: 3              # H-14 HARD rule: minimum 3 iterations
  max_iterations: 5              # Safety limit
  improvement_threshold: 0.02    # 2% improvement required to continue past min
  acceptance_threshold_c2: 0.92  # H-13 HARD rule: >= 0.92 for C2+ deliverables
  acceptance_threshold_c1: 0.85  # Legacy threshold for C1 (Routine) deliverables
  consecutive_no_improvement_limit: 2
```

## Decision Logic (for Orchestrator)

```
IF iteration < min_iterations (3):
    → REVISE (minimum iterations not met, H-14)
ELIF quality_score >= acceptance_threshold (0.92 for C2+):
    → ACCEPT (threshold met)
ELIF iteration >= max_iterations:
    → ESCALATE_TO_USER (threshold not met after max iterations)
ELIF (current_score - previous_score) < improvement_threshold AND consecutive_no_improvement >= 2:
    → ACCEPT_WITH_CAVEATS (no further improvement likely, document residual gaps)
ELSE:
    → REVISE (send feedback to generator)
```

## Orchestrator Workflow Example (C2+ Deliverable)

```
Iteration 1:
  1. Creator (ps-architect) produces design.md, applies S-010 Self-Refine (H-15)
  2. Orchestrator invokes ps-critic with design.md
  3. ps-critic applies S-003 Steelman (H-16), then S-014 LLM-as-Judge
  4. ps-critic returns: score=0.72, threshold_met=false
  5. Orchestrator: iteration=1 < 3 (min) → REVISE (H-14)
  6. Orchestrator sends dimension-level feedback to ps-architect

Iteration 2:
  1. Creator (ps-architect) produces design-v2.md, applies S-010 (H-15)
  2. Orchestrator invokes ps-critic with design-v2.md
  3. ps-critic applies S-003 (H-16), then S-014 + S-002 Devil's Advocate
  4. ps-critic returns: score=0.85, threshold_met=false
  5. Orchestrator: iteration=2 < 3 (min) → REVISE (H-14)
  6. Orchestrator sends critique to ps-architect

Iteration 3:
  1. Creator (ps-architect) produces design-v3.md, applies S-010 (H-15)
  2. Orchestrator invokes ps-critic with design-v3.md
  3. ps-critic applies S-003 (H-16), then S-014 final scoring
  4. ps-critic returns: score=0.94, threshold_met=true
  5. Orchestrator: 0.94 >= 0.92 AND iteration >= 3 → ACCEPT
```

## Example Complete Invocation

```python
Task(
    description="ps-critic: Design critique",
    subagent_type="general-purpose",
    prompt="""
You are the ps-critic agent (v2.0.0).

## Agent Context

<role>Quality Evaluator specializing in iterative refinement</role>
<task>Critique authentication design for iteration 2</task>
<constraints>
<must>Create file with Write tool at projects/${JERRY_PROJECT}/critiques/</must>
<must>Include L0/L1/L2 output levels</must>
<must>Calculate quality score (0.0-1.0)</must>
<must>Provide actionable improvement recommendations</must>
<must>Call link-artifact after file creation</must>
<must_not>Return transient output only (P-002)</must_not>
<must_not>Hide quality issues (P-022)</must_not>
<must_not>Manage iteration loop (P-003 - orchestrator's job)</must_not>
</constraints>

## PS CONTEXT (REQUIRED)
- **PS ID:** work-024
- **Entry ID:** e-400
- **Iteration:** 2
- **Artifact to Critique:** projects/PROJ-002/decisions/work-024-e-399-auth-design-v2.md
- **Generator Agent:** ps-architect

## EVALUATION CRITERIA
Use default criteria:
- Completeness (0.25)
- Accuracy (0.25)
- Clarity (0.20)
- Actionability (0.15)
- Alignment (0.15)

## IMPROVEMENT THRESHOLD
- **Target Score:** 0.92
- **Max Iterations:** 5
- **Previous Score:** 0.65 (iteration 1)

## CRITIQUE TASK
Evaluate the authentication design document against the criteria above.
Provide quality score, specific improvement recommendations, and threshold assessment.
"""
)
```

## Post-Completion Verification

```bash
# 1. File exists
ls projects/${JERRY_PROJECT}/critiques/{ps_id}-{entry_id}-iter{iteration}-critique.md

# 2. Has L0/L1/L2 sections
grep -E "^### L[012]:" projects/${JERRY_PROJECT}/critiques/{ps_id}-{entry_id}-iter{iteration}-critique.md

# 3. Has quality score
grep -E "Quality Score.*[0-9]\.[0-9]+" projects/${JERRY_PROJECT}/critiques/{ps_id}-{entry_id}-iter{iteration}-critique.md

# 4. Has recommendation
grep -E "Recommendation.*(ACCEPT|REVISE|ESCALATE)" projects/${JERRY_PROJECT}/critiques/{ps_id}-{entry_id}-iter{iteration}-critique.md

# 5. Artifact linked
python3 scripts/cli.py view {ps_id} | grep {entry_id}
```
