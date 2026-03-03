# Agent Response — sonnet-C1-AD-T1-S3

The appropriate tool tier for adv-scorer, given this task description, is **T1 (Read-Only)**.

**Task requirements analysis:**

The task description specifies three operations:

1. Receives a deliverable artifact as a file path — no tool needed for receiving inputs
2. Reads the artifact and applies the S-014 rubric — requires Read
3. Outputs a structured score report — explicitly delegated: "The calling orchestrator will handle storing the results"

The phrase "the calling orchestrator will handle storing the results" is the key architectural statement. It means adv-scorer returns its output in-context to the orchestrator, which then decides where and how to persist it. adv-scorer does not write to the filesystem.

**Tier evaluation:**

| Tier | Tools Added | Needed? | Reason |
|------|-------------|---------|--------|
| T1 | Read, Glob, Grep | YES | Reading the deliverable artifact (Read), optionally locating related files like rubric definitions (Glob, Grep) |
| T2 | Write, Edit, Bash | NO | The task explicitly delegates storage to the calling orchestrator. adv-scorer produces a score report as output, not a persisted file. |
| T3 | WebSearch, WebFetch, Context7 | NO | The rubric is provided as input. No external documentation lookup is required. |
| T4 | Memory-Keeper | NO | No cross-session state required. The orchestrator manages any persistence. |
| T5 | Task | NO | No delegation needed. This is a single-agent evaluation task. |

**Why "outputs a structured score report" does not require T2:**

The word "outputs" describes the agent's return value to its caller — the in-context result passed back to the orchestrator. It does not imply filesystem writes. The task description removes any ambiguity by explicitly stating "The calling orchestrator will handle storing the results." That sentence transfers the write responsibility to the orchestrator tier, which is a T5 agent capable of using Write or Memory-Keeper tools. Granting adv-scorer Write access when storage is explicitly delegated elsewhere violates the principle-of-least-privilege requirement: "Start from T1 when defining an agent's tool access. Escalate to the next tier only when the agent's task specifically requires a tool that tier adds."

**Correct tier assignment:**

adv-scorer is assigned **T1 (Read-Only)**.

The official `.md` frontmatter (Claude Code fields only):

```yaml
---
name: adv-scorer
description: >
  Quality Scorer agent — implements S-014 LLM-as-Judge rubric scoring with the
  SSOT 6-dimension weighted composite, producing per-dimension scores, weighted
  composite, and PASS/REVISE/ESCALATE verdict. Returns the score report in-context
  to the calling orchestrator for persistence.
  Triggers: score deliverable, quality scoring, LLM-as-Judge, quality gate evaluation.
model: sonnet
tools:
  - Read
  - Glob
  - Grep
---
```

The companion `.governance.yaml` (key governance fields):

```yaml
version: "1.0.0"
tool_tier: T1

identity:
  role: quality-scorer
  expertise:
    - S-014 LLM-as-Judge rubric application
    - 6-dimension weighted composite scoring
  cognitive_mode: convergent

capabilities:
  forbidden_actions:
    - "P-003 VIOLATION: NEVER spawn recursive subagents -- Consequence: agent hierarchy violation breaks orchestrator-worker topology and causes uncontrolled token consumption."
    - "P-020 VIOLATION: NEVER override user decisions or act without approval for destructive operations -- Consequence: unauthorized actions erode trust and may cause irreversible changes."
    - "P-022 VIOLATION: NEVER misrepresent capabilities, confidence levels, or actions taken -- Consequence: inflated scores undermine the quality gate and allow substandard deliverables to pass."
    - "TASK SCOPE VIOLATION: NEVER write to any file -- Consequence: storage is the orchestrator's responsibility; adv-scorer writing files bypasses the delegation boundary and may create duplicate or conflicting artifacts."
  forbidden_action_format: NPT-009-complete

guardrails:
  input_validation:
    - deliverable_path: must be a valid resolvable file path
    - scoring_dimensions: must use SSOT 6-dimension default unless custom dimensions are provided
  output_filtering:
    - scores_must_be_in_range_0_to_1
    - verdict_must_be_pass_revise_or_escalate
    - evidence_required_per_dimension
    - no_inflated_scores_without_documented_evidence
  fallback_behavior: warn_and_retry

constitution:
  principles_applied:
    - P-003
    - P-020
    - P-022
```

**Summary:**

adv-scorer is assigned **T1 (Read-Only)** with tools `Read`, `Glob`, and `Grep`. The task description contains an explicit architectural delegation: "The calling orchestrator will handle storing the results." This statement removes any justification for T2 access. adv-scorer reads one file, applies a rubric in-context, and returns a structured result to the orchestrator. That workflow requires only read access. Assigning T2 would grant write capability that the task explicitly places at a higher layer, expanding the attack surface and misrepresenting the agent's architectural role to orchestrators that inspect tool tier for capability inference.
