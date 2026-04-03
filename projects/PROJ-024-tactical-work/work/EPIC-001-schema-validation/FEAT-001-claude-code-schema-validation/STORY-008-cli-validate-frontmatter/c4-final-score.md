# Quality Score Report: FEAT-001 Claude Code Schema Validation (C4 Final)

## L0 Executive Summary

**Score:** 0.884/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Traceability (0.82)

**One-line assessment:** A substantially complete and methodologically rigorous deliverable set that falls short of the 0.92 threshold due to unresolved WORKTRACKER integrity failures (STORY-007 and STORY-008 remain "pending" despite implementation being complete) and the CLI command lacking full hexagonal architecture placement — the handler lives in `application/commands/` but is not wired through a proper infrastructure adapter layer, and the test suite does not invoke the command via the CLI entry point as specified in STORY-008 AC.

---

## Scoring Context

- **Deliverable:** FEAT-001 deliverable set (6 artifacts)
- **Deliverable Type:** Design + Code + Analysis (composite)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** .context/rules/quality-enforcement.md
- **Scored:** 2026-03-26T00:00:00Z
- **Iteration:** 3 (first: 0.790, second: 0.823, third: this score)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.884 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (standalone scoring pass) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.87 | 0.174 | 38/38 tests passing; CLI wired in parser+main; script deleted; schema v1.1.0 covers all 33 documented fields; WORKTRACKER status stale on 2 stories |
| Internal Consistency | 0.20 | 0.88 | 0.176 | Gap analysis review reconciliation section resolves prior 0/2-Critical discrepancy; "38 tests" claim in gap analysis confirmed by count; "pending" WORKTRACKER entries contradict implemented reality |
| Methodological Rigor | 0.20 | 0.92 | 0.184 | Hexagonal architecture followed for command/handler; positive+negative+round-trip+integrity test classes; allOf/not reserved-word pattern is JSON Schema 2020-12 idiomatic; STORY-008 AC requires test-via-CLI-entry-point which is not yet done |
| Evidence Quality | 0.15 | 0.89 | 0.134 | Schema $id versioned; 119 agents scanned with 4 defects found/fixed; 36 GitHub issues analyzed; known limitations table with issue numbers cited (#4700, #29677, #25200, etc.); model pattern regex is valid and observable |
| Actionability | 0.15 | 0.88 | 0.132 | `uv run pytest tests/schemas/test_frontmatter_schemas.py` is runnable; `jerry agents validate-frontmatter` command exists; maintenance process documented with changelog URL; 2 open items (model-typo CI validator, runtime behavioral constraints) are explicitly deferred with named mechanisms |
| Traceability | 0.10 | 0.82 | 0.082 | EN-001/EN-002/EN-003 references present; STORY-008 acceptance criteria defined but WORKTRACKER shows all 6 tasks as "pending" despite CLI delivery; gap analysis v1.1.0 status column cross-references each resolved item; `--json` flag declared in AC but not confirmed implemented in CLI handler |
| **TOTAL** | **1.00** | | **0.884** | |

---

## Detailed Dimension Analysis

### Completeness (0.87/1.00)

**Evidence:**

The feature set covers all originally scoped work: both schemas at v1.1.0 with 33 total fields documented (16 agent, 17 skill), the test suite at 38 tests (3+12+2+9+5+7 across five test classes), the CLI command implemented in `src/agents/application/commands/validate_frontmatter_command.py` with full handler, the gap analysis updated with reconciliation section and 38-test count, and `scripts/validate_all_frontmatter.py` deleted (glob returns no match).

**Gaps:**

1. WORKTRACKER.md shows STORY-007 and STORY-008 as `status: pending` with all sub-tasks pending. The worktracker is the authoritative state record per WTI rules. The implementation exists on disk, but the tracker was not updated.
2. STORY-008 Acceptance Criteria item: "Existing test suite updated to invoke via CLI" — the test file at `tests/schemas/test_frontmatter_schemas.py` still invokes `validate()` directly from `jsonschema`, not via the CLI entry point. This AC is unmet.
3. STORY-008 AC: `--json` flag is defined in the parser but not verified in the test suite.

**Improvement Path:**

Mark STORY-007 and STORY-008 as `completed` in WORKTRACKER.md with completion timestamps. Add at least one test that invokes the CLI via `subprocess` or a direct `main()` call to cover the `--json` flag and exit-code behavior.

---

### Internal Consistency (0.88/1.00)

**Evidence:**

The gap analysis Recommended Changes section lists 10 items; the v1.1.0 Status column shows all 10 resolved or explicitly deferred. The Review Artifact Reconciliation section correctly explains the 0-Critical vs 2-Critical discrepancy between eng-security and red-vuln scopes. The test count "38 tests" stated in the gap analysis matches the actual parametrized count (3+12+2+9+5+7=38). The schema description field accurately states "additionalProperties: true" and "NOT a security boundary" — consistent with the Scope and Limitations section of the gap analysis.

**Gaps:**

1. WORKTRACKER shows STORY-007 and STORY-008 as "pending"; the scoring context says they were completed; the actual filesystem shows the CLI is implemented. Three sources contradict each other. The authoritative source (WORKTRACKER) is wrong.
2. The gap analysis Maintenance Process section states "89 agent definitions and 30 SKILL.md files" but the STORY-005 context says "119 definitions" were validated. One of these counts is stale or misdefined (agent files only vs agent+skill files combined). This is a minor discrepancy but reduces reader trust.

**Improvement Path:**

Update WORKTRACKER to match implementation state. Reconcile the "89 agent definitions" vs "119 definitions" count discrepancy in the gap analysis Maintenance Process section by clarifying whether 119 = 89 agents + 30 skills.

---

### Methodological Rigor (0.92/1.00)

**Evidence:**

Both schemas use JSON Schema Draft 2020-12 (`$schema` header present). The `allOf/not` pattern for reserved word rejection is semantically correct and idiomatic for the draft version. The `oneOf` for `mcpServers` correctly models the two observed runtime formats (object with boolean values vs array). Test classes separate concerns cleanly: positive fixtures from production files, negative fixtures per constraint, live round-trip tests, schema integrity tests. The command/handler separation follows hexagonal architecture — `ValidateFrontmatterCommand` is a frozen dataclass (pure data), `ValidateFrontmatterCommandHandler` owns the logic. The `_schema_errors` method uses `Draft202012Validator.iter_errors()` which is the correct jsonschema API for collecting all errors rather than fail-fast.

**Gaps:**

1. The CLI handler is in `src/agents/application/commands/` not `src/interface/` per H-07 architecture. The STORY-008 AC explicitly states: "Command follows hexagonal architecture (H-07): command in interface/, handler in application/, schema loading in infrastructure/". The command is in `application/commands/` (correct placement for the command dataclass) and the handler is co-located rather than having a separate infrastructure adapter for schema loading. The schema loading (`json.loads(path.read_text(...))`) happens inside `__init__` of the handler rather than being injected through an infrastructure port — acceptable for current scope but the AC says "schema loading in infrastructure/" which is not done.
2. STORY-008 AC: "Update tests to use CLI entry point" — not done.

**Improvement Path:**

These are deliberate scope decisions or oversights rather than methodological failures. The handler co-location is defensible for this command's scope. The rigor is genuinely high; the gaps are AC compliance issues rather than methodology failures, hence the score does not drop below 0.90 on this dimension.

---

### Evidence Quality (0.89/1.00)

**Evidence:**

All KNOWN ISSUE annotations in both schemas cite specific GitHub issue numbers (e.g., `#4700`, `#29677`, `#25200`, `#31292`, `#18392`, `#17283`, `#22161`, `#13905`, `#18837`, `#18737`). The gap analysis cites version-pinned documentation URLs (code.claude.com/docs March 2026). The model pattern regex is testable and confirmed by the negative fixture `agent-model-typo` (rejects "opuis") and `agent-model-invalid-underscore` (rejects "claude_3_sonnet"). The 4 defects found in STORY-005 (tools vs allowed-tools, multiline descriptions) are referenced but not documented in the deliverable set directly — the gap analysis mentions "4 skill defects found and fixed" in the scoring context but this is not in the gap analysis itself.

**Gaps:**

1. The STORY-005 finding ("found and fixed 4 skill defects") is not documented anywhere in the six deliverables. The gap analysis Maintenance Process section mentions "89 agent definitions" but does not document the 4 defects found or which files were fixed.
2. The model pattern `^(sonnet|opus|haiku|inherit|default|claude-[a-z0-9-]+(\[1m\])?|opusplan)$` accepts "opusplan" — this appears to be an undocumented enum value. The skill schema description mentions it but the evidence for its existence is thin (no GitHub issue citation).

**Improvement Path:**

Add a brief "STORY-005 findings" section to the gap analysis documenting the 4 defects found and fixed (which files, what was wrong, what was changed). Add a GitHub issue number or source citation for "opusplan" in both schemas.

---

### Actionability (0.88/1.00)

**Evidence:**

The gap analysis Maintenance Process section gives a concrete 4-step process (Monitor, Trigger, Review, Validate) with a specific URL. The Scope and Limitations table gives concrete "Required Mechanism" entries for each non-enforceable constraint (e.g., "CI allowlist of approved MCP server names", "Custom validator script or CI gate reading .governance.yaml"). The CLI command accepts `--agent` and `--skill` filters enabling targeted validation. Exit code 1 on failure is documented. `uv run pytest tests/schemas/test_frontmatter_schemas.py` is a directly executable command.

**Gaps:**

1. The two open gaps ("model typos pass validation" and "schema cannot enforce behavioral H-34 constraints") are correctly identified but the "Required Mechanism" entries are descriptions, not work items. They do not link to a follow-on story or enabler to close them.
2. The `--json` flag is in the CLI AC and parser but it is not confirmed implemented in the handler (the `json_output` parameter is passed to `_handle_agents_validate_frontmatter` but I could not verify JSON formatting output in `main.py` from available excerpts).

**Improvement Path:**

Create follow-on STORY or EN work items for the two named open gaps in Scope and Limitations. Verify the `--json` flag produces machine-readable output and add a test case for it.

---

### Traceability (0.82/1.00)

**Evidence:**

The gap analysis has a v1.1.0 Status column on every gap row providing direct traceability from each identified gap to its resolution status. Schema `$id` fields contain version numbers. Test file module docstring cites EN-003, H-20, H-34, and both schema file paths. The CLI command module docstring cites PROJ-024, and both schema file paths.

**Gaps:**

1. STORY-007 and STORY-008 show `status: pending` in WORKTRACKER with all sub-tasks pending. Per WTI rules, WORKTRACKER is the authoritative state record. If these stories are complete, the traceability chain is broken — the worktracker cannot be used to verify what was delivered.
2. STORY-008 has 6 defined sub-tasks (TASK-001 through TASK-006) all marked `pending`. There is no evidence in the deliverable set that these tasks completed — the CLI command exists, but TASK-005 (update tests to CLI entry point) and TASK-006 (delete script) are the only ones verifiable from disk. TASK-001 through TASK-004 are implemented but not checked off.
3. The gap analysis Maintenance Process section's "89 agent definitions" count does not trace to a specific run or scan artifact.

**Improvement Path:**

Update WORKTRACKER.md: mark STORY-007 and STORY-008 as `completed` with dates; mark TASK-001 through TASK-006 as completed or re-scope the ACs to match what was actually delivered. This is the single highest-leverage improvement for this dimension.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Traceability | 0.82 | 0.92 | Update WORKTRACKER.md: mark STORY-007 and STORY-008 as `completed` with 2026-03-27 completion date; mark all 6 TASK-001–006 as completed |
| 2 | Completeness | 0.87 | 0.92 | Add at least one CLI integration test invoking `_handle_agents_validate_frontmatter` or via subprocess to satisfy STORY-008 AC "Existing test suite updated to invoke via CLI" |
| 3 | Internal Consistency | 0.88 | 0.92 | Reconcile "89 agent definitions" (gap analysis Maintenance Process) with "119 definitions" (STORY-005 context) by adding a parenthetical: "89 agent .md files + 30 SKILL.md files = 119 total" |
| 4 | Actionability | 0.88 | 0.92 | Verify `--json` flag produces machine-readable output and add a test; create follow-on work items for the two open Scope and Limitations gaps |
| 5 | Evidence Quality | 0.89 | 0.92 | Document the 4 STORY-005 defects found/fixed in the gap analysis; add source citation for "opusplan" model alias |

---

## Score Delta from Prior Iterations

| Iteration | Composite | Delta | Key Changes |
|-----------|-----------|-------|-------------|
| Pass 1 | 0.790 | -- | Baseline: schemas only, no tests, no CLI |
| Pass 2 | 0.823 | +0.033 | Tests added (34 tests), reserved word enforcement, scope/limitations section, review reconciliation |
| Pass 3 (this) | 0.884 | +0.061 | CLI command wired and deployed, script deleted, 38 tests (4 new), STORY-007 rename edits complete |
| **Threshold** | **0.920** | **-0.036 gap** | WORKTRACKER integrity and CLI integration test are the remaining blockers |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score — specific file paths, line counts, AC items
- [x] Uncertain scores resolved downward (Traceability: chose 0.82 not 0.85 given broken WORKTRACKER state)
- [x] Third-pass calibration applied — 0.884 is consistent with a near-complete feature with two specific process/traceability gaps remaining
- [x] No dimension scored above 0.95 — Methodological Rigor at 0.92 is the highest, supported by specific schema design evidence
- [x] WORKTRACKER status contradiction was not glossed over — it materially reduced Traceability and Internal Consistency scores

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.884
threshold: 0.92
weakest_dimension: Traceability
weakest_score: 0.82
critical_findings_count: 0
iteration: 3
improvement_recommendations:
  - "Update WORKTRACKER.md: mark STORY-007 and STORY-008 as completed with 2026-03-27 date"
  - "Add CLI integration test satisfying STORY-008 AC 'test suite updated to invoke via CLI'"
  - "Reconcile 89 vs 119 definition count discrepancy in gap analysis Maintenance Process section"
  - "Verify --json flag output and add test case"
  - "Document 4 STORY-005 defects in gap analysis; add opusplan citation"
```
