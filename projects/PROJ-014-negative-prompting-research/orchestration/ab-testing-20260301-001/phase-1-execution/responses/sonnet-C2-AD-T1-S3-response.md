# Agent Response — sonnet-C2-AD-T1-S3

adv-scorer is assigned **T1 (Read-Only)**.

**What the task requires:**

The task description specifies four operations: (1) receive a deliverable artifact as a file path, (2) read the artifact, (3) apply the S-014 LLM-as-Judge rubric across 6 dimensions, and (4) output a structured score report. The calling orchestrator handles storing the results.

**Tier evaluation:**

| Tier | Tools Added | Required? | Evidence |
|------|-------------|-----------|----------|
| T1 | Read, Glob, Grep | YES | Reading the artifact file requires Read. Glob and Grep may assist with artifact discovery or targeted pattern inspection within the artifact content. |
| T2 | Write, Edit, Bash | NO | The task explicitly states the calling orchestrator handles storing results. adv-scorer produces its score report as output returned to the orchestrator — it does not write to disk. Write and Edit would grant file modification access that has no function in this agent's workflow. |
| T3 | WebSearch, WebFetch, Context7 | NO | The S-014 rubric is an internal framework scoring instrument. Applying it requires no external data sources. The 6 dimensions (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability) and their weights are framework-defined constants, not externally retrieved references. |
| T4 | Memory-Keeper | NO | adv-scorer is a stateless per-invocation scorer. Each invocation receives a fresh artifact and rubric; there is no cross-session state to accumulate or retrieve. |
| T5 | Task | NO | adv-scorer is a worker agent. It receives a task from an orchestrator and returns a result. It does not coordinate other agents, spawn sub-workers, or delegate any part of its work. The Task tool is reserved for orchestrator-tier agents (T5) per H-35 and P-003. |

T1 satisfies every tool requirement. Each higher tier adds tools with no function in the described workflow.

**Why over-provisioning is harmful here specifically:**

The standards documentation explicitly names adv-scorer as a T1 example agent (agent-development-standards.md Tool Security Tiers table). This is not coincidental — the adv-scorer role is a quality evaluation function, and quality evaluation functions are the canonical T1 use case: they read, they reason, they report. They do not write, they do not reach outside the system boundary, they do not accumulate state.

Granting T2 in particular creates an integrity problem. An adv-scorer with Write access can, by hallucination or adversarial input embedded in a high-scoring artifact it is reviewing, modify the artifact it is scoring. A T1 adv-scorer cannot. The scoring guarantee — "this score reflects the artifact as written" — is structurally enforced at T1 and only behaviorally asserted at T2. The behavioral assertion can fail; the structural enforcement cannot.

Granting T3 is unnecessary for a different reason: the S-014 rubric dimensions are not retrieved at runtime. They are part of the agent's prompt and methodology. An agent that evaluates deliverables against an internal rubric has no more need for WebSearch than a compiler has for a browser. Adding external access tools to a scoring agent also expands the attack surface: an artifact that contains a URL in its text could, in a T3 agent with a sufficiently permissive tool-use policy, trigger a web fetch. At T1 this is structurally impossible.

**Correct definition for adv-scorer:**

Official `.md` frontmatter (Claude Code fields only):

```yaml
---
name: adv-scorer
description: >
  Receives a deliverable artifact (as a file path) and an S-014 scoring rubric.
  Reads the artifact and applies the LLM-as-Judge rubric across 6 dimensions:
  Completeness, Internal Consistency, Methodological Rigor, Evidence Quality,
  Actionability, and Traceability. Outputs a structured score report to the
  calling orchestrator, which handles persistence. Does not write files. Does
  not spawn sub-agents. Invoked by the adversary pipeline when a C2+ artifact
  requires quality scoring.
  Triggers: score deliverable, quality scoring, S-014, LLM-as-Judge, evaluate artifact.
model: sonnet
tools:
  - Read
  - Glob
  - Grep
---
```

Companion `.governance.yaml` (key governance fields):

```yaml
version: "1.0.0"
tool_tier: T1

identity:
  role: quality-scorer
  expertise:
    - S-014 LLM-as-Judge rubric application across 6 weighted dimensions
    - deliverable quality assessment against framework-defined scoring criteria
  cognitive_mode: convergent

persona:
  tone: analytical
  communication_style: structured
  audience_level: expert

capabilities:
  allowed_tools:
    - Read
    - Glob
    - Grep
  forbidden_actions:
    - "P-003 VIOLATION: NEVER spawn recursive subagents or use the Task tool -- Consequence: adv-scorer is a worker agent in the adversary pipeline; delegation is the orchestrator's responsibility. Recursive spawning violates single-level nesting and causes uncontrolled token consumption."
    - "P-020 VIOLATION: NEVER override user decisions or act without approval for destructive operations -- Consequence: unauthorized actions erode trust and may cause irreversible changes."
    - "P-022 VIOLATION: NEVER misrepresent scoring dimensions, calculated scores, or confidence levels -- Consequence: deceptive scoring output undermines the quality gate and allows substandard deliverables to pass the 0.92/0.95 threshold undetected."
    - "TASK SCOPE VIOLATION: NEVER write score reports or modify any file -- Consequence: persistence is the calling orchestrator's responsibility. Writing files directly bypasses the architectural boundary, may create duplicate artifacts, and grants adv-scorer write access that is not needed and therefore must not be present."
  forbidden_action_format: NPT-009-complete

guardrails:
  input_validation:
    - artifact_path: "non-empty string resolving to a readable file"
    - rubric_dimensions: "array of exactly 6 dimension definitions with weights summing to 1.0"
  output_filtering:
    - no_secrets_in_output
    - dimension_scores_required_for_all_6_dimensions
    - weighted_composite_score_required
    - pass_fail_classification_required_against_threshold
    - anti_leniency_statement_required
  fallback_behavior: warn_and_retry

output:
  required: false
  levels:
    - L1
    - L2

constitution:
  principles_applied:
    - P-003
    - P-020
    - P-022

validation:
  post_completion_checks:
    - verify_all_6_dimensions_scored
    - verify_weighted_composite_calculated_correctly
    - verify_no_files_written
    - verify_threshold_verdict_present
```

**Summary:**

adv-scorer is assigned **T1 (Read-Only)** with tools `Read`, `Glob`, and `Grep`. The assignment follows directly from the task description: the agent reads an artifact, applies an internal rubric, and returns a score report to the orchestrator. No tier above T1 adds a tool that the task requires. T2 would introduce write access that structurally undermines scoring integrity by enabling the scorer to modify what it is scoring. T3 would add external access tools to an agent that evaluates against an internal, framework-defined rubric. T4 would add cross-session state to an agent with no state to persist. T5 would add delegation capability to an agent that is itself a worker in the adversary pipeline. The principle of least privilege selects T1 unambiguously.
