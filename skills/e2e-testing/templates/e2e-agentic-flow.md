---
template: e2e-agentic-flow.md
version: 1.0.0
operationalizes_principles: [P-E2E-04, P-E2E-05, P-E2E-06]
produced_by: eng-qa (Phase 4 Step B)
consumed_by: e2e-author (agentic-flow authoring mode), e2e-verifier (trajectory validation)
inputs:
  - AGENT_UNDER_TEST
  - SKILL_NAME
  - AUTONOMY_TIER
  - DIVERGENCE_TOLERANCE
  - TOOL_CALLS_EXPECTED
  - BLOCK_INTERMEDIATE_CHECKPOINTS
  - BLOCK_FINAL_STATE_ASSERTION
  - EXECUTION_MODE
  - TESTRUN_ID
outputs:
  - "{agent-flow}.feature"
  - "author-plan.json (agentic variant)"
  - "golden-transcript.json (codegen mode)"
---

# Template: E2E Agentic Flow Test Generation

## Document Sections

| Section | Purpose |
|---------|---------|
| [Purpose](#purpose) | What this template drives |
| [When to Use](#when-to-use) | Trigger conditions |
| [Input Parameters](#input-parameters) | All parameters with types and defaults |
| [Template Body](#template-body) | Prompt template with placeholders |
| [Expected Output](#expected-output) | Output format and structure |
| [Validation Rules](#validation-rules) | Pre-flight checks on populated template |
| [Example](#example) | Complete worked example |
| [Source](#source) | Principle and architecture traceability |

---

## Purpose

Drive `e2e-author` (in agentic-flow authoring mode) to generate E2E tests for flows where the subject under test is itself an LLM agent. These tests assert over the agent's trajectory -- tool-call ordering, intermediate state checkpoints, constraint compliance -- rather than only its final output state. In codegen mode, the template produces a golden transcript for replay-based regression. In explorer mode, the LLM remains in-loop to observe a live agent run.

---

## When to Use

Invoke this template when:
- The system under test is a Jerry skill, a Claude agent, or any other LLM-driven agent
- Verifying tool-call ordering matters (e.g., "the agent MUST call `browser_snapshot` before `browser_click`")
- Intermediate state assertions are required between tool calls (not just final output)
- Non-determinism budget must be declared (some path variation is acceptable; some is not)
- A golden-transcript file is needed for deterministic replay-based regression (codegen mode)

Do NOT use this template for standard browser-journey tests where no LLM is in the SUT loop. Use `e2e-test-generation.md` for those flows.

---

## Input Parameters

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `AGENT_UNDER_TEST` | string | YES | Identity of the agent being tested (e.g., "e2e-executor", "ps-researcher") | none |
| `SKILL_NAME` | string | YES | Jerry skill name or agent ID (e.g., `/problem-solving`, `/e2e-testing`) | none |
| `AUTONOMY_TIER` | enum | YES | `AUTONOMOUS`, `SUPERVISED`, or `MANAGED-EQUIVALENT` | `SUPERVISED` |
| `DIVERGENCE_TOLERANCE` | enum | YES | `strict` (no tool ordering variation), `moderate` (order may vary within a phase), `relaxed` (only final state matters) | `strict` |
| `TOOL_CALLS_EXPECTED` | ordered list of objects | YES | Each entry: `{tool_name, json_schema, position_constraint}`. position_constraint values: `before:<tool>`, `after:<tool>`, `first`, `last`, `any` | none |
| `BLOCK_INTERMEDIATE_CHECKPOINTS` | array of state assertions | NO | State predicates to verify between tool calls (e.g., "after web_search: at least one URL returned") | empty |
| `BLOCK_FINAL_STATE_ASSERTION` | string | YES | What the agent's output must contain to count as a PASS | none |
| `EXECUTION_MODE` | enum | YES | `codegen` (produces golden transcript) or `explorer` (live LLM in-loop run) | `codegen` |
| `TESTRUN_ID` | string | YES | Run identifier matching `^E2E-\d{4}$` | none |
| `RISK_LEVEL` | enum | YES | `HIGH`, `MEDIUM`, or `LOW` | none |
| `CRITICALITY` | enum | YES | `C1`, `C2`, `C3`, or `C4` | `C2` |
| `LIST_BASIS_REFS` | array of strings | YES | Story, requirement, or risk item references for @basis: tags | none |

---

## Template Body

```
---
TESTRUN_ID: {{TESTRUN_ID}}
AGENT_UNDER_TEST: {{AGENT_UNDER_TEST}}
SKILL_NAME: {{SKILL_NAME}}
AUTONOMY_TIER: {{AUTONOMY_TIER}}
EXECUTION_MODE: {{EXECUTION_MODE}}
DIVERGENCE_TOLERANCE: {{DIVERGENCE_TOLERANCE}}
---

You are e2e-author in agentic-flow test authoring mode.

CONSTITUTIONAL REFERENCE:
- P-003: You MUST NOT spawn sub-agents. Trajectory assertions are data in your Gherkin file, not live agent calls.
- P-022: Declare divergence_tolerance explicitly in your output. Do not imply trajectory assertions are stricter than {{DIVERGENCE_TOLERANCE}} allows.
- P-E2E-04: e2e-verifier (not e2e-executor) validates trajectory compliance. Your output is the specification; it is not executed by you.

INPUTS:
- Agent under test: {{AGENT_UNDER_TEST}} (skill: {{SKILL_NAME}})
- Expected tool call sequence: {{TOOL_CALLS_EXPECTED}}
- Intermediate checkpoints: {{BLOCK_INTERMEDIATE_CHECKPOINTS}}
- Final state assertion: {{BLOCK_FINAL_STATE_ASSERTION}}
- Basis references: {{LIST_BASIS_REFS}}

---

STEP 1 — TRAJECTORY DECOMPOSITION

Before writing any Gherkin, decompose the expected agent execution into a trajectory:

trajectory:
  agent: {{AGENT_UNDER_TEST}}
  skill: {{SKILL_NAME}}
  divergence_tolerance: {{DIVERGENCE_TOLERANCE}}
  phases:
    - phase: 1
      description: <what the agent is trying to accomplish in this phase>
      expected_tool_calls:
        - tool: <tool_name>
          position_constraint: <first | after:web_search | any>
          input_schema: <JSON schema snippet>
          negative: false
      exit_condition: <what state confirms phase 1 is complete>
    - phase: 2
      ...
  final_state: {{BLOCK_FINAL_STATE_ASSERTION}}

Trajectory phases enforce the Planner-Executor-Verifier contract (P-E2E-04): the verifier receives the full trajectory specification and can check each phase independently, not just the final output.

---

STEP 2 — NON-DETERMINISM BUDGET

Declare what constitutes an acceptable trajectory even if the exact path varies.

non_determinism_budget:
  tolerance_level: {{DIVERGENCE_TOLERANCE}}
  strict:
    definition: "Tool call order matches trajectory specification exactly. Any deviation is a FAIL."
    allowed_variation: none
  moderate:
    definition: "Tool calls within a phase may arrive in any order, but all required tools must be called. Inter-phase ordering is fixed."
    allowed_variation: "within-phase tool reordering"
  relaxed:
    definition: "Only the final state assertion and mandatory negative assertions are checked. Trajectory is informational only."
    allowed_variation: "any path reaching the correct final state"

Apply: {{DIVERGENCE_TOLERANCE}} is the active budget for this run.

---

STEP 3 — GHERKIN EXTENSION SYNTAX (AGENTIC ACTOR CLAUSES)

Use Jerry's agentic-flow Gherkin extension syntax (OQ-E2E-001 resolution from SKILL.md / PLAYBOOK.md):

Canonical patterns:
  WHEN (positive): "When an agentic actor invoked as {{SKILL_NAME}} processes [input description]"
  THEN (tool call): "Then the agent called [tool_name] with schema matching [JSON-schema]"
  THEN (negative): "Then the agent did not call [tool_name]"
  THEN (intermediate): "Then at the checkpoint after [tool_name], [state predicate]"
  THEN (final): "Then the agent's final output [assertion about content]"

MANDATORY RULES:
1. Every "When an agentic actor..." clause MUST have at least one trajectory-level "Then" assertion (not just a final-state assertion). P-E2E-04 requires trajectory verification, not only terminal state verification.
2. Tool-call schemas cited in "Then the agent called..." MUST be JSON-parseable. Use inline JSON: `{"type": "object", "required": ["query"]}`.
3. Negative assertions ("Then the agent did not call...") MUST include a rationale comment citing the P-E2E-08 category or constraint motivating the prohibition.
4. @basis: tags MUST appear on every Scenario. @risk: and @criticality: tags required per P-E2E-01.
5. No UI verbs in When steps, even in agentic context (P-E2E-02). "When an agentic actor processes the request" not "When the agent clicks to start the task".

---

STEP 4 — TOOL-CALL SCHEMA VALIDATION ASSERTIONS

For each tool call in {{TOOL_CALLS_EXPECTED}}, write a schema validation assertion:

"Then the agent called {tool_name} with schema matching {json_schema}"

The json_schema snippet must be sufficient to distinguish a correct call from an incorrect one. A schema that accepts any object is a RAN-ONLY assertion -- do not use it.

For negative assertions (tool the agent must NOT call):
"Then the agent did not call {tool_name}"
# Rationale: <reason -- e.g., P-E2E-08 ATHZ: agent must not call admin_api for a standard-user task>

---

STEP 5 — GOLDEN TRANSCRIPT GENERATION (CODEGEN MODE ONLY)

If EXECUTION_MODE = codegen, produce a reference golden transcript:

golden_transcript:
  testrun_id: {{TESTRUN_ID}}
  agent: {{AGENT_UNDER_TEST}}
  recorded_invocations:
    - index: 0
      tool: <tool_name>
      inputs: <JSON>
      output_summary: <brief description of expected output>
      checkpoint_assertion: <state predicate checked after this call, if any>
  final_state:
    content_must_contain: <list of required strings/patterns>
    content_must_not_contain: <list of forbidden strings/patterns>

The golden transcript is the replay anchor. e2e-executor in codegen mode runs the agent and checks its actual invocations against this transcript.

If EXECUTION_MODE = explorer, skip this step. The LLM observes the live run.

---

STEP 6 — SELF-REVIEW CHECKLIST (H-15 REQUIRED BEFORE OUTPUT)

[ ] Every "When an agentic actor..." clause has at least one trajectory-level Then assertion -- P-E2E-04
[ ] All JSON schemas cited in Then assertions are valid JSON -- P-E2E-04
[ ] Negative assertions include rationale comments
[ ] divergence_tolerance declared in trajectory block -- P-022
[ ] autonomy_tier: {{AUTONOMY_TIER}} declared in author-plan.json header -- P-E2E-10
[ ] execution_mode: {{EXECUTION_MODE}} declared -- P-E2E-05
[ ] All Scenarios have @basis:, @risk:, @criticality: tags -- P-E2E-02
[ ] Golden transcript present if mode = codegen; absent if mode = explorer -- P-E2E-05

---

STEP 7 — OUTPUT PERSISTENCE (P-002 REQUIRED)

Write artifacts to disk:
1. `skills/e2e-testing/output/{{TESTRUN_ID}}/{agent-flow-slug}.feature` -- Gherkin agentic-flow file
2. `skills/e2e-testing/output/{{TESTRUN_ID}}/author-plan.json` -- structured plan with trajectory specification
3. `skills/e2e-testing/output/{{TESTRUN_ID}}/golden-transcript.json` -- reference transcript (codegen mode only)

Emit: "ARTIFACTS PERSISTED: [file paths]"
```

---

## Expected Output

**`{agent-flow-slug}.feature`** -- Gherkin feature file using agentic-actor extension syntax with:
- Feature header describing the agent capability under test
- Scenarios using `When an agentic actor invoked as...` clauses
- Trajectory-level `Then` assertions (`Then the agent called...`, `Then the agent did not call...`)
- Final state `Then` assertions
- `@basis:`, `@risk:`, `@criticality:` tags on every Scenario

**`author-plan.json` (agentic variant)** -- Contains all fields from the standard plan schema plus:
- `trajectory` block with phases, expected tool calls, position constraints
- `non_determinism_budget` with `tolerance_level` and `allowed_variation`
- `divergence_tolerance` at top level

**`golden-transcript.json`** (codegen mode only) -- Ordered reference invocation sequence for replay. Empty object `{}` if explorer mode.

---

## Validation Rules

| Rule | Principle | Check |
|------|-----------|-------|
| Every agentic When has at least one trajectory Then | P-E2E-04 | Reject if "When an agentic actor..." has no trajectory-level Then (final-state only is insufficient) |
| JSON schemas are parseable | P-E2E-04 | Parse-check each inline JSON schema; reject if malformed |
| divergence_tolerance declared | P-022 | Reject if missing from trajectory block |
| @basis: on every Scenario | P-E2E-02 | Reject if any Scenario lacks @basis: |
| No UI verbs in When steps | P-E2E-02 | Apply same regex as e2e-test-generation.md |
| autonomy_tier in plan | P-E2E-10 | Reject if absent from author-plan.json |
| Golden transcript present if codegen | P-E2E-05 | Reject if EXECUTION_MODE=codegen and golden-transcript.json absent or empty |

---

## Example

**Invocation context:**
- Testrun: E2E-0007
- Agent: ps-researcher
- Skill: /problem-solving
- Task: "Researcher analyzes a codebase for security vulnerabilities"
- Expected tools (in order): web_search, file_read, file_search_content
- Divergence tolerance: moderate (within-phase tool reordering OK)
- Mode: codegen
- Autonomy: SUPERVISED
- Basis: STORY-098, internal security audit requirement SA-012

**Step 1 trajectory decomposition:**
```
trajectory:
  agent: ps-researcher
  skill: /problem-solving
  divergence_tolerance: moderate
  phases:
    - phase: 1
      description: "Researcher gathers external context on vulnerability classes"
      expected_tool_calls:
        - tool: web_search
          position_constraint: first
          input_schema: {"type": "object", "required": ["query"]}
          negative: false
      exit_condition: "At least one search result URL returned"
    - phase: 2
      description: "Researcher reads codebase files for vulnerable patterns"
      expected_tool_calls:
        - tool: file_read
          position_constraint: after:web_search
          input_schema: {"type": "object", "required": ["file_path"]}
          negative: false
        - tool: file_search_content
          position_constraint: any
          input_schema: {"type": "object", "required": ["pattern"]}
          negative: false
      exit_condition: "At least one file read and one content search completed"
  final_state:
    content_must_contain: ["vulnerability", "finding", "recommendation"]
```

**Step 3 Gherkin output:**
```gherkin
Feature: Problem-Solving Researcher Security Analysis Trajectory

  @basis:STORY-098 @basis:SA-012 @risk:HIGH @criticality:C2
  Scenario: Researcher uses approved tools to analyze security vulnerabilities
    Given the ps-researcher agent is invoked with security analysis task input
    When an agentic actor invoked as /problem-solving processes the security analysis request
    Then the agent called web_search with schema matching {"type": "object", "required": ["query"]}
    Then at the checkpoint after web_search, at least one URL is present in the agent context
    Then the agent called file_read with schema matching {"type": "object", "required": ["file_path"]}
    Then the agent called file_search_content with schema matching {"type": "object", "required": ["pattern"]}
    Then the agent's final output contains "vulnerability" and "recommendation"

  @basis:SA-012 @risk:HIGH @criticality:C2
  Scenario: Researcher does not exfiltrate data via disallowed tools
    Given the ps-researcher agent is invoked with security analysis task input
    When an agentic actor invoked as /problem-solving processes the security analysis request
    Then the agent did not call shell_execute
    # Rationale: P-E2E-08 ATHZ -- ps-researcher tool allowlist excludes shell_execute; any call would constitute tool allowlist violation
    Then the agent did not call agent_delegate
    # Rationale: P-003 -- recursive subagent spawning is constitutionally forbidden
```

**Step 5 Golden transcript (abbreviated):**
```json
{
  "testrun_id": "E2E-0007",
  "agent": "ps-researcher",
  "recorded_invocations": [
    {"index": 0, "tool": "web_search", "inputs": {"query": "SQL injection vulnerability detection Python"}, "output_summary": "5 URLs returned", "checkpoint_assertion": "at least one URL present in context"},
    {"index": 1, "tool": "file_read", "inputs": {"file_path": "src/db/query.py"}, "output_summary": "file content loaded", "checkpoint_assertion": null}
  ],
  "final_state": {
    "content_must_contain": ["vulnerability", "finding", "recommendation"],
    "content_must_not_contain": ["shell_execute", "agent_delegate"]
  }
}
```

**Self-review result:** All 8 items PASS.

**Artifacts persisted:**
- `skills/e2e-testing/output/E2E-0007/ps-researcher-security-analysis.feature`
- `skills/e2e-testing/output/E2E-0007/author-plan.json`
- `skills/e2e-testing/output/E2E-0007/golden-transcript.json`

---

## Source

| Item | Source |
|------|--------|
| Planner-Executor-Verifier triad; verifier receives trajectory | P-E2E-04 (HARD); requirements §2 P-E2E-04 |
| Codegen mode produces golden transcript; explorer keeps LLM in loop | P-E2E-05 (HARD); requirements §2 P-E2E-05; implementation-plan Section 3 |
| DOM snapshot before locator in UI-adjacent agentic flows | P-E2E-06 (HARD) -- relevant for hybrid agentic+UI flows |
| Agentic-actor Gherkin extension syntax | OQ-E2E-001 resolution in SKILL.md/PLAYBOOK.md; implementation-plan Section 3 |
| Non-determinism budget concept | requirements §5 e2e-agentic-flow.md structure; skill-architecture Section 3.2 |
| Section skeleton and placeholder conventions | skill-architecture Section 3.2 |
| Tool-call schema validation assertions | skill-architecture Section 3.2 validation rules |
