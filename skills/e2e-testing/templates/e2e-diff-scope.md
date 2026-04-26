---
template: e2e-diff-scope.md
version: 1.0.0
operationalizes_principles: [P-E2E-01, P-E2E-03]
produced_by: eng-qa (Phase 4 Step B)
consumed_by: e2e-analyst (primary), e2e-author (fallback when analyst absent)
inputs:
  - GIT_DIFF_PATH
  - FEATURE_INVENTORY_GLOB
  - WSTG_COVERAGE_PATH
  - FULL_SUITE_FLAG
  - CALL_GRAPH_PATH
  - TESTRUN_ID
outputs:
  - "scope-document.json"
  - "coverage-gap-report.json"
---

# Template: E2E Diff-Scope Analysis

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

Drive `e2e-analyst` (or `e2e-author` in fallback mode when analyst is absent) through change-impact analysis: given a `git diff`, classify changed files by layer, map them to adjacent user flows, identify coverage gaps against the existing Gherkin inventory, check WSTG mandatory category gaps, and produce a prioritised scope document for `e2e-author`. This template enforces P-E2E-03's HARD confirmation gate: the scope document is NOT passed to `e2e-author` until the user explicitly confirms scope.

---

## When to Use

Invoke this template when:
- A `git diff` is available and test scope must be determined before authoring begins
- The user invokes `/e2e-testing scope` or `/e2e-testing generate-tests --diff`
- An existing test suite needs a coverage gap analysis against recent code changes

Do NOT invoke when no diff is available and the user has explicitly requested a `--full-suite` run. In that case, `e2e-test-generation.md` is invoked directly with a user-confirmed scope.

---

## Input Parameters

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `GIT_DIFF_PATH` | file path or diff text | YES | Path to diff file or raw `git diff` text | none -- must be supplied; absence triggers user prompt per P-E2E-03 |
| `FEATURE_INVENTORY_GLOB` | glob pattern | YES | Glob for existing `.feature` files (e.g., `skills/e2e-testing/output/**/*.feature`) | none |
| `WSTG_COVERAGE_PATH` | file path | NO | Path to current `wstg-coverage-history.json`; empty on first run | empty (all six categories treated as gaps on first run) |
| `FULL_SUITE_FLAG` | boolean | NO | Whether user has explicitly requested full-suite generation | `false` |
| `CALL_GRAPH_PATH` | file path | NO | Optional dependency map in JSON or dot format for flow-adjacency analysis | empty -- semantic heuristic used if absent |
| `TESTRUN_ID` | string | YES | Run identifier matching `^E2E-\d{4}$` | none |

---

## Template Body

```
---
TESTRUN_ID: {{TESTRUN_ID}}
GIT_DIFF_PATH: {{GIT_DIFF_PATH}}
FEATURE_INVENTORY_GLOB: {{FEATURE_INVENTORY_GLOB}}
WSTG_COVERAGE_PATH: {{WSTG_COVERAGE_PATH}}
FULL_SUITE_FLAG: {{FULL_SUITE_FLAG}}
CALL_GRAPH_PATH: {{CALL_GRAPH_PATH}}
---

You are e2e-analyst in scope-analysis mode.
(If e2e-analyst is absent, you are e2e-author operating in analyst-fallback mode. Flag all outputs with "analyst-absent mode" for reporter.)

CONSTITUTIONAL REFERENCE:
- P-003: You MUST NOT spawn sub-agents. Flow-adjacency analysis is a single-agent analytical task.
- P-022: If call-graph tool is unavailable, flag output as "call-graph absent -- semantic heuristic used". Do not present heuristic results as structural analysis.
- P-E2E-03 (HARD): If {{FULL_SUITE_FLAG}} is false AND no diff is present, DO NOT produce a scope document. Emit an interactive prompt asking the user for a diff before proceeding.

GUARD: If GIT_DIFF_PATH is empty AND FULL_SUITE_FLAG = false:
  STOP. Emit:
  "P-E2E-03 ENFORCEMENT: No diff provided and --full-suite not requested.
   Please provide a git diff:
   Option A: Run `git diff HEAD~1..HEAD` and paste the output.
   Option B: Provide a path to a diff file.
   Option C: Explicitly confirm --full-suite to generate tests for all flows (requires user confirmation at the next step)."
  Do NOT proceed to Step 1 until diff or explicit confirmation is received.

---

STEP 1 — CHANGED-FILE CLASSIFICATION

Parse the diff at {{GIT_DIFF_PATH}} and classify each changed file by layer:

| Layer | Classification | Description |
|-------|---------------|-------------|
| ui_component | React/Vue/Angular components, HTML templates, CSS | Directly renders user-facing elements |
| api_handler | Route handlers, controllers, REST endpoints | Mediates between UI and business logic |
| business_logic | Domain services, use cases, validators | Implements application rules |
| infrastructure | Database, cache, queue, config, environment | Not directly user-facing |
| test | Existing test files, fixtures, factories | Changes to test code itself |

For each changed file:
  file_classification:
    path: <file_path>
    layer: <ui_component | api_handler | business_logic | infrastructure | test>
    change_type: <added | modified | deleted | renamed>
    change_summary: <1-sentence description of what changed>

Every changed file MUST receive a classification. No file may be left unclassified.
If layer is ambiguous, choose the most-user-visible layer and note the ambiguity.

---

STEP 2 — FLOW ADJACENCY MAPPING

For each changed file, identify which Gherkin Features and Rules are adjacent (i.e., would test behaviour that exercises the changed code).

If {{CALL_GRAPH_PATH}} is provided:
  - Load the call graph and trace from the changed file to its callers and callees
  - A Feature is adjacent if any path through the changed file is reachable from a Feature's Given or When clause
  - Proximity score: 0.95 for direct call, 0.80 for one hop, 0.60 for two hops, 0.40 for three or more hops

If {{CALL_GRAPH_PATH}} is absent:
  - Use semantic heuristic: compare changed file path and name against Feature file descriptions and scenario names
  - A Feature is adjacent if its name, description, or @basis: tags semantically overlap with the changed file's path and change_summary
  - Flag output: "call-graph absent -- semantic heuristic used; flow adjacency confidence is MEDIUM, not HIGH"

For each changed file, produce:
  flow_adjacency:
    changed_file: <path>
    adjacent_flows:
      - feature: <Feature name from .feature file>
        rule: <Rule name, if applicable>
        proximity_score: <0.0-1.0>
        adjacency_method: <call-graph | semantic-heuristic>

---

STEP 3 — COVERAGE GAP IDENTIFICATION

Load existing .feature files matching {{FEATURE_INVENTORY_GLOB}}.

For each adjacent flow identified in Step 2:
  - Check if a .feature file already covers that flow
  - If covered: note the existing .feature path
  - If not covered: flag as a coverage gap

coverage_gap_analysis:
  covered_flows:
    - flow: <flow name>
      feature_file: <path to existing .feature>
  uncovered_flows:
    - flow: <flow name>
      reason: <"no existing .feature" | "existing .feature does not cover adjacent scenario">

---

STEP 4 — WSTG MANDATORY CATEGORY GAP CHECK

Load {{WSTG_COVERAGE_PATH}} (current WSTG coverage state). If file is absent (first run), treat all six mandatory categories as uncovered.

Mandatory WSTG categories that MUST have at least one scenario per P-E2E-08:
  - ATHN (Authentication)
  - ATHZ (Authorization)
  - SESS (Session Management)
  - INPV (Input Validation)
  - BUSL (Business Logic)
  - APIT (API Testing)

For each category:
  - Check if at least one @wstg:WSTG-v42-{CATEGORY}-NN tag exists in the current .feature inventory
  - If absent: flag as a WSTG coverage gap

wstg_gap_check:
  covered_categories: [<list of covered categories>]
  gap_categories: [<list of uncovered categories>]

Even if no gaps exist, the `wstg_gap_categories` field MUST appear in scope-document.json (may be an empty list).

---

STEP 5 — PRIORITISED SCOPE DOCUMENT CONSTRUCTION

Construct the prioritised scope document by ordering flows using:
  Priority score = risk_level_weight × change_proximity_score

risk_level_weight:
  HIGH = 3
  MEDIUM = 2
  LOW = 1

Risk level assignment:
  - ui_component changes adjacent to authentication flows: HIGH
  - business_logic changes: HIGH
  - api_handler changes: MEDIUM
  - infrastructure changes: LOW (unless directly security-relevant)
  - test changes: LOW (test-only changes rarely require new scenarios)

The scope document lists flows in descending priority order.

---

STEP 6 — CONFIRMATION PROMPT (P-E2E-03 HARD REQUIREMENT)

If {{FULL_SUITE_FLAG}} = false:

DO NOT pass scope-document.json to e2e-author yet. Display the following confirmation prompt to the user:

"SCOPE CONFIRMATION REQUIRED (P-E2E-03)

Test scope derived from diff analysis:
[Display top 5 flows by priority, with flow name, risk_level, and reason]

WSTG coverage gaps found: {{wstg_gap_categories}}

Total flows to test: <N>
Estimated scenarios: <M>

Options:
  A: CONFIRM this scope -- e2e-author will generate tests for these flows only
  B: ADD flows -- specify additional flows to include
  C: REMOVE flows -- specify flows to exclude from this run
  D: FULL SUITE -- generate tests for all flows (requires explicit confirmation of scope expansion)

Please select an option (A/B/C/D):"

Only after receiving Option A (or a modified scope confirmed via B/C) should scope-document.json be written and passed to e2e-author.

If {{FULL_SUITE_FLAG}} = true: Skip this prompt. Log "full-suite mode confirmed by user" in scope-document.json.

---

STEP 7 — OUTPUT PERSISTENCE (P-002 REQUIRED)

Write artifacts to disk ONLY AFTER user scope confirmation:
1. `skills/e2e-testing/output/{{TESTRUN_ID}}/scope-document.json` -- prioritised scope for e2e-author
2. `skills/e2e-testing/output/{{TESTRUN_ID}}/coverage-gap-report.json` -- coverage gap details

Emit: "ARTIFACTS PERSISTED: [file paths]"
```

---

## Expected Output

**`scope-document.json`** -- Machine-readable prioritised scope consumed by e2e-author:

```json
{
  "testrun_id": "E2E-NNNN",
  "diff_ref": "<git diff reference>",
  "changed_files": [{"path": "...", "classification": "business_logic"}],
  "flow_adjacency": [{"flow": "...", "adjacent_files": [...], "proximity_score": 0.95}],
  "coverage_gaps": [{"flow": "...", "reason": "no existing .feature"}],
  "wstg_gaps": ["BUSL"],
  "prioritised_scope": [{"flow": "...", "risk_level": "HIGH", "criticality": "C2", "priority_rank": 1}],
  "full_suite_requested": false,
  "confirmation_received": true,
  "analyst_mode": "e2e-analyst | analyst-absent-fallback"
}
```

**`coverage-gap-report.json`** -- Human-readable gap analysis for reporter consumption.

---

## Validation Rules

| Rule | Principle | Check |
|------|-----------|-------|
| No scope-document without diff or confirmation | P-E2E-03 | Reject if FULL_SUITE_FLAG=false and no diff provided and scope-document.json would be written |
| Every changed file classified | P-E2E-01 | Reject if any changed file has no layer classification |
| wstg_gap_categories field present | P-E2E-08 | Reject scope-document.json if wstg_gap_categories field absent (may be empty list) |
| Confirmation received before output written | P-E2E-03 | scope-document.json must have confirmation_received: true |
| Priority ordering by risk_level x proximity | P-E2E-01 | Validate prioritised_scope is ordered descending by priority score |
| Call-graph fallback flagged | P-022 | Flag "call-graph absent" in scope-document.json if CALL_GRAPH_PATH empty |

---

## Example

**Invocation context:**
- Testrun: E2E-0003
- Diff: HEAD~1..HEAD (2 files changed: src/auth/login.ts, src/pages/LoginPage.tsx)
- Feature inventory: `skills/e2e-testing/output/**/*.feature` (2 files found)
- WSTG coverage: prior run covered ATHN, ATHZ; SESS, INPV, BUSL, APIT are gaps
- Full-suite: false
- Call graph: absent

**Step 1 -- file classification:**
```json
[
  {"path": "src/auth/login.ts", "layer": "business_logic", "change_type": "modified", "change_summary": "added account lockout after 5 failed attempts"},
  {"path": "src/pages/LoginPage.tsx", "layer": "ui_component", "change_type": "modified", "change_summary": "updated error message display component"}
]
```

**Step 2 -- flow adjacency (semantic heuristic, call graph absent):**
```json
[
  {"changed_file": "src/auth/login.ts", "adjacent_flows": [
    {"feature": "User Authentication Journey", "rule": "Invalid credentials are rejected", "proximity_score": 0.85, "adjacency_method": "semantic-heuristic"}
  ]},
  {"changed_file": "src/pages/LoginPage.tsx", "adjacent_flows": [
    {"feature": "User Authentication Journey", "rule": "Valid credentials grant access", "proximity_score": 0.80, "adjacency_method": "semantic-heuristic"}
  ]}
]
```

**Step 4 -- WSTG gap check:**
```json
{"covered_categories": ["ATHN", "ATHZ"], "gap_categories": ["SESS", "INPV", "BUSL", "APIT"]}
```

**Step 5 -- prioritised scope (excerpt):**
```json
[
  {"flow": "auth-journey/account-lockout", "risk_level": "HIGH", "criticality": "C2", "priority_rank": 1, "reason": "business_logic change + HIGH risk"},
  {"flow": "auth-journey/login-error-display", "risk_level": "MEDIUM", "criticality": "C2", "priority_rank": 2, "reason": "ui_component change"}
]
```

**Step 6 -- confirmation prompt displayed to user:**
```
SCOPE CONFIRMATION REQUIRED (P-E2E-03)

Test scope derived from diff (HEAD~1..HEAD):

1. [HIGH] auth-journey/account-lockout -- business_logic change to login.ts
2. [MEDIUM] auth-journey/login-error-display -- ui_component change to LoginPage.tsx

WSTG coverage gaps found: SESS, INPV, BUSL, APIT (4 of 6 mandatory categories uncovered)

Total flows to test: 2
Estimated scenarios: 6-8

Note: call-graph absent -- semantic heuristic used; confidence MEDIUM.

Options: A (confirm) / B (add) / C (remove) / D (full suite)
```

User selects A. scope-document.json written with `confirmation_received: true`.

**Artifacts persisted:**
- `skills/e2e-testing/output/E2E-0003/scope-document.json`
- `skills/e2e-testing/output/E2E-0003/coverage-gap-report.json`

---

## Source

| Item | Source |
|------|--------|
| Diff-scoped entry with user confirmation gate | P-E2E-03 (HARD); requirements §2 P-E2E-03 |
| Risk × change_proximity prioritisation | P-E2E-01 (HARD); requirements §2 P-E2E-01 |
| WSTG gap check against six mandatory categories | P-E2E-08 (HARD); requirements §2 P-E2E-08 |
| Section skeleton and placeholder conventions | skill-architecture Section 3.4; implementation-plan Section 3 |
| Changed-file layer classification | implementation-plan Section 3 e2e-diff-scope.md output structure |
| Call-graph vs semantic heuristic fallback | skill-architecture Section 2.5 failure modes; implementation-plan Section 2 (e2e-analyst shell_execute permission) |
| Confirmation prompt format | P-E2E-03 HARD requirement; skill-architecture Section 3.4 validation rules |
