# Design Decision Analysis: PM-001, FM-001, FM-002

**Analysis Type:** Trade-off (all three findings require design decisions before implementation)
**Analyst:** ps-analyst
**Source Findings:** `adversary-agent-findings.md` (2026-03-11)
**Date:** 2026-03-11
**Criticality:** C3 (Significant -- all three findings rated Critical by adversary)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [PM-001 Analysis](#pm-001-analysis) | Error propagation path between uc-author and uc-slicer |
| [FM-001 Analysis](#fm-001-analysis) | cd-generator cross-reference validation governance YAML gap |
| [FM-002 Analysis](#fm-002-analysis) | uc-slicer realization_level enforcement sufficiency |
| [Cross-Cutting Observations](#cross-cutting-observations) | Systemic patterns across all three findings |
| [Evidence Summary](#evidence-summary) | All cited evidence |

---

## L0: Executive Summary

Three adversary findings require design decisions before the issues can be fixed. This analysis provides the root cause, trade-off evaluation, and recommended option for each.

**PM-001** (no error propagation between uc-author and uc-slicer): The pipeline has no structured way to tell uc-author "your artifact was rejected by uc-slicer and needs to be elaborated." The user gets an error message but must manually understand what to do next. The recommended fix is a lightweight structured rejection artifact -- a small YAML block uc-slicer writes alongside its error message -- rather than extending the full session context handoff schema.

**FM-001** (cd-generator cross-reference validation incomplete in governance YAML): The validation rule exists in the governance YAML but is missing a critical qualifier: it does not state that the full UC artifact must be loaded (not just the interactions block) to execute the check. This is a documentation precision problem, not a missing rule. The recommended fix is a targeted wording update to the existing governance YAML entry plus a mirroring addition to the .md capabilities section.

**FM-002** (uc-slicer realization_level enforcement behavioral only): The allOf schema constraint added to `use-case-realization-v1.schema.json` closes roughly 60% of the enforcement gap. The constraint catches the case where `realization_level: INTERACTION_DEFINED` is set with an empty or absent `interactions[]`. However, it does not catch the case where interactions are present but semantically incomplete. A CLI-level validation step invoked post-creation closes the remaining gap at acceptable cost.

---

## PM-001 Analysis

### Finding Summary

When uc-author produces an artifact at `detail_level: BULLETED_OUTLINE` and uc-slicer rejects it (requires `ESSENTIAL_OUTLINE` minimum), the rejection is communicated only as a human-readable error message. There is no machine-readable state that an orchestrator or uc-author invocation can consume to understand why the artifact was rejected and what elaboration is needed to proceed.

### Root Cause Analysis (5 Whys)

| Level | Question | Answer | Evidence |
|-------|----------|--------|----------|
| Why 1 | Why does the pipeline break when uc-slicer rejects an artifact? | Because uc-slicer's rejection produces only a human-readable error, not a structured signal | `uc-slicer.md` Failure Modes table: "Reject with actionable error: 'Input artifact is at {current_level}...'" |
| Why 2 | Why is the rejection only human-readable? | Because neither agent defines an `on_reject` protocol in `session_context` | `uc-author.governance.yaml` and `uc-slicer.governance.yaml` `session_context.on_send` -- no error/reject path defined |
| Why 3 | Why is there no `on_reject` protocol? | Because the agents were designed for the success path; error propagation between paired agents was not modeled | No `on_error` or `on_reject` field exists in `agent-governance-v1.schema.json` `session_context` definition |
| Why 4 | Why was the error path not modeled? | Because the handoff schema (`session_context.json`) models only the success-path handoff (key_findings, artifacts, confidence) -- the `blockers` array is the closest construct but is not semantically matched to "rejection of upstream output" | `docs/schemas/session_context.json` -- `blockers` array is defined but semantically mapped to "issues that may prevent the target agent from completing," not "this target rejected the source's output" |
| Why 5 | Why does the blockers array not serve this purpose? | Because a rejection context flows in the opposite direction (downstream back to upstream), while `blockers` is a forward-facing signal. The schema has no backward error channel. | `session_context.json` schema: source_agent -> target_agent unidirectional; no provision for target returning structured rejection to source |

**Root Cause:** The inter-agent handoff architecture is unidirectional. There is no backward channel in the session context schema for a downstream agent (uc-slicer) to return a structured rejection that an upstream agent (uc-author) or orchestrator can consume programmatically.

### Steelman of Alternative Hypotheses (H-16)

**Alternative hypothesis A: The session message is sufficient.** Argument: uc-slicer already produces an actionable human-readable error message with the current level and required level. A user reading it knows exactly what to do. Adding machine-readable structure would add implementation overhead without improving the user experience for the most common case (direct human invocation). Strength: valid for the single-user case. Weakness: fails for orchestrated pipelines where no human reads intermediate error messages, and fails the PM-001 diagnostic: if a user cannot understand why the pipeline failed, the skill is unusable on first attempt.

**Alternative hypothesis B: Document a convention, don't change the schema.** Argument: Add a documentation note in SKILL.md stating that the user must re-invoke uc-author with `target_detail_level: ESSENTIAL_OUTLINE` after a uc-slicer rejection. No structural change needed. Strength: zero implementation cost. Weakness: relies on the user knowing the internal detail level enum and the correct invocation pattern -- this is exactly the UX failure PM-001 identifies.

### Options and Trade-offs

**Option A: Structured Rejection Artifact (Recommended)**

uc-slicer writes a lightweight YAML rejection artifact alongside its error message:

```yaml
# UC-slicer rejection: {artifact_path}-rejection.yaml
rejection:
  rejected_artifact: "{path_to_rejected_artifact}"
  rejection_reason: "detail_level_insufficient"
  current_level: "BULLETED_OUTLINE"
  required_level: "ESSENTIAL_OUTLINE"
  missing_elements:
    - "extensions[] (at least 1 required)"
    - "Step 9 Cockburn quality indicators not verified"
  recommended_action: "Re-invoke uc-author with target_detail_level: ESSENTIAL_OUTLINE"
  timestamp: "{ISO-8601}"
```

uc-author's `session_context.on_receive` adds a step: "Check for rejection artifact at `{artifact_path}-rejection.yaml`; if present, load `recommended_action` and `missing_elements` to set target detail level automatically."

| Criterion | Assessment |
|-----------|------------|
| Addresses PM-001 root cause | Yes -- provides machine-readable backward channel |
| Orchestrator usability | Yes -- orchestrator can check for rejection artifact and re-route |
| User experience | Improved -- rejection file is human-readable too |
| Schema change required | No -- the rejection artifact uses a standalone YAML format, not the session context schema |
| Implementation complexity | **Low** -- uc-slicer writes a small YAML file; uc-author checks for it on load |
| Risk | Low -- additive change; does not affect the success path |
| Maintenance cost | Low -- one additional file per rejection event |

**Option B: Extend session_context Schema with on_reject Protocol**

Add an `on_reject` block to the `session_context` section of the governance YAML schema:

```yaml
# addition to agent-governance-v1.schema.json
session_context:
  on_reject:
    - "Write rejection context to {artifact_path}-rejection.yaml"
    - "Include current_level, required_level, missing_elements"
```

And extend `session_context.json` (the ps/nse handoff schema) to support a backward error channel with `rejection_context` field in the payload.

| Criterion | Assessment |
|-----------|------------|
| Addresses PM-001 root cause | Yes -- formally models backward error channel |
| Schema change required | Yes -- `agent-governance-v1.schema.json` and `session_context.json` require modification |
| Consistency | High -- all future agent pairs would benefit from a formal reject protocol |
| Implementation complexity | **Medium** -- schema versioning, backward compatibility, updates to existing governance YAMLs |
| Risk | Medium -- schema changes require CI gate updates, existing agent validation |
| Maintenance cost | Medium -- schema evolution overhead |

**Option C: SKILL.md Documentation Only**

Document in `/use-case` SKILL.md that uc-slicer invocation requires `detail_level >= ESSENTIAL_OUTLINE` and that the user should check uc-author's L0 output for the detail level achieved before invoking uc-slicer.

| Criterion | Assessment |
|-----------|------------|
| Addresses PM-001 root cause | Partially -- helps informed users; does not help orchestrated pipelines |
| Implementation complexity | **Low** -- documentation only |
| Orchestrator usability | No |
| User experience (first-time) | Marginal improvement only |

### Recommended Option: A (Structured Rejection Artifact)

**Justification:** Option A addresses the root cause (no machine-readable backward channel) with the lowest implementation cost (Low complexity) and no schema changes. It produces a human-readable file that serves both user and orchestrator consumers. It aligns with Jerry's "filesystem as infinite memory" principle -- using a file-based artifact for error state is consistent with how all other inter-agent communication works.

Option B would be the better architectural choice if PM-001 were a systemic gap affecting many agent pairs. Currently it affects one pair (uc-author/uc-slicer) and potentially tspec-generator/tspec-analyst (PM-003). The schema overhead of Option B is not warranted for two agent pairs.

Option C does not close the orchestrator usability gap and should not be used as the sole fix.

**Implementation complexity:** Low

**Specific implementation steps:**
1. Add to `uc-slicer.md` Failure Modes table: rejection writes `{artifact_path}-rejection.yaml` with the fields above.
2. Add to `uc-slicer.governance.yaml` `session_context.on_send`: "Write structured rejection artifact to `{artifact_path}-rejection.yaml` when rejecting for detail_level < ESSENTIAL_OUTLINE."
3. Add to `uc-author.governance.yaml` `session_context.on_receive`: "Check for `{artifact_path}-rejection.yaml`; if present, load `required_level` and `missing_elements` to inform elaboration target."
4. Add to `/use-case` SKILL.md a note about the rejection artifact pattern.
5. Add `post_completion_checks` entry to `uc-slicer.governance.yaml`: "verify_rejection_artifact_written_on_detail_level_rejection."

**What this does NOT address:** The deeper Pattern 4 (inter-agent error propagation is underdefined across all 6 agents) identified in the adversary report. That is a systemic gap that warrants a separate analysis and potentially Option B as a longer-term solution. This analysis scopes to the PM-001 specific case.

---

## FM-001 Analysis

### Finding Summary

cd-generator's governance YAML `input_validation` array contains an entry for cross-reference validation (`source_step` must exist in referenced flow), but the entry does not specify that the full UC artifact must be loaded to execute this check. If cd-generator is invoked with only the interactions block provided as input context (not the full artifact file), the validation will silently pass because there is no flow data to cross-reference against.

The adversary RPN: S=9, O=5, D=8 = 360.

### Root Cause Analysis (5 Whys)

| Level | Question | Answer | Evidence |
|-------|----------|--------|----------|
| Why 1 | Why does the cross-reference validation have high detection difficulty (D=8)? | Because the validation requires loading and parsing a referenced flow section, which requires the full artifact -- a multi-step operation not implied by the validation entry string | `cd-generator.governance.yaml` input_validation entry 5: "Each $.interactions[*].source_step must reference an existing step in the flow identified by $.interactions[*].source_flow (cross-reference validation)" -- does not mention loading requirement |
| Why 2 | Why does the governance YAML entry not mention the loading requirement? | Because governance YAML `input_validation` entries are written as declarative constraint statements, not as procedural execution instructions | `agent-governance-v1.schema.json` `guardrails.input_validation` -- accepts string array; no standard for expressing prerequisites |
| Why 3 | Why can an agent be invoked with only the interactions block? | Because the `<input>` section specifies "use case artifact file at $.realization_level = INTERACTION_DEFINED" but the validation operates on the artifact's parsed content, not the file load operation itself | `cd-generator.md` `<input>` section -- specifies file requirement; `<methodology>` Step 1 Layer 2 references `<guardrails>` but doesn't explicitly call "load full file before semantic checks" |
| Why 4 | Why is the full-file load requirement not explicit? | Because the .md methodology describes the algorithm steps but treats artifact loading as assumed; the governance YAML documents the constraint without the prerequisite for executing it | Cross-checking `cd-generator.md` Step 1 against `cd-generator.governance.yaml` -- the .md says "validate the input use case artifact"; the governance YAML documents what to validate but not the loading prerequisite |
| Why 5 | Why did the loading prerequisite not surface as a governance YAML concern during authoring? | Because the dual-file architecture (behavioral instructions in .md, machine-readable constraints in .governance.yaml) creates a natural boundary that tends toward documenting WHAT to validate in the YAML without documenting the HOW prerequisite | H-34 dual-file architecture: .md carries behavioral completeness; .governance.yaml carries machine-readable governance. The boundary is correctly positioned but the cross-reference check has a pre-condition that falls into the gap |

**Root Cause:** The governance YAML documents the constraint (what to check) but not the pre-condition (what must be loaded before the check can execute). This is not a missing validation rule -- it is a precision gap in how the existing rule is expressed. The .md behavioral instructions are complete; the governance YAML entry is incomplete by omission.

### Steelman of Alternative Hypotheses (H-16)

**Alternative hypothesis: Governance YAML should not document procedural prerequisites.** Argument: governance YAML is a machine-readable schema for what the agent validates, not a runbook for how the agent executes. The pre-condition (load full artifact) is an execution detail that belongs in the .md methodology. Adding pre-conditions to governance YAML entries conflates two concerns and makes the YAML harder to parse programmatically. Strength: architecturally sound argument about separation of concerns. Weakness: the adversary finding specifically concerns CI gates reading the governance YAML independently -- if the gate reads the governance YAML and sees a cross-reference check, it may attempt to execute that check without loading the full artifact, producing a false pass. The governance YAML must be self-sufficient for its purpose.

### The Boundary Question: When Does a Behavioral Constraint Belong in Governance YAML?

This is the central design question raised by FM-001. The adversary identified three instances of the same pattern (FM-001, FM-002, FM-004). A principled answer is needed.

**Proposed boundary rule:**

| Constraint Type | Location | Rationale |
|----------------|----------|-----------|
| Structural validation (field presence, type, pattern) | governance YAML `input_validation` + schema | Deterministic; CI-executable without LLM |
| Semantic validation (cross-reference checks, derived field consistency) | governance YAML `input_validation` WITH explicit prerequisites + .md guardrails | Requires LLM execution but should be declared in governance YAML for CI gate awareness |
| Behavioral instructions (HOW to execute a check) | .md only | Not machine-readable; execution is LLM-driven |
| Pre-conditions for semantic validation | governance YAML WITH the validation entry | CI gates must know what to load to execute the check |

Under this boundary rule, cross-reference validation belongs in governance YAML because it is a semantic constraint that CI can declare awareness of -- but the governance YAML entry must include its pre-condition.

**Implication:** The adversary finding is correct. The governance YAML entry for cross-reference validation is incomplete because it omits the pre-condition. Fixing the entry does not expand governance YAML scope -- it corrects an incomplete expression of an already-present rule.

### Options and Trade-offs

**Option A: Update Existing Governance YAML Entry (Recommended)**

Update `cd-generator.governance.yaml` input_validation entry 5 from:
```yaml
- "Each $.interactions[*].source_step must reference an existing step in the flow identified by $.interactions[*].source_flow (cross-reference validation)"
```
to:
```yaml
- "Full UC artifact must be loaded (not just the interactions block) before executing cross-reference validation: each $.interactions[*].source_step must reference an existing step in the flow identified by $.interactions[*].source_flow"
```

Also add to `cd-generator.md` `<capabilities>` section: "Always load the full UC artifact file (not just the interactions block) before executing Step 1 Layer 2 semantic validation, to enable cross-reference of source_step against actual flow steps."

| Criterion | Assessment |
|-----------|------------|
| Addresses root cause | Yes -- adds the missing prerequisite to the existing rule |
| CI gate impact | Improved -- CI reading governance YAML now sees the loading requirement |
| Scope | Minimal -- targeted change to one entry |
| Behavioral change | None -- the .md already implies full artifact loading; this makes it explicit |
| Implementation complexity | **Low** |
| Risk | Very low -- documentation precision improvement only |

**Option B: Move Semantic Checks Out of Governance YAML**

Remove all semantic (LLM-evaluated) validation entries from governance YAML input_validation, leaving only structural (schema-verifiable) entries. Document in an ADR that governance YAML input_validation is for structural constraints only.

| Criterion | Assessment |
|-----------|------------|
| Addresses root cause | Indirectly -- removes the misleading entry |
| CI gate impact | Negative -- CI gates lose visibility of semantic constraints |
| Consistency | Low -- tspec-generator and uc-slicer also have semantic validation entries |
| Scope | Large -- requires revisiting all 6 governance YAML files |
| Implementation complexity | **High** |

**Option C: Add Separate `semantic_validation` Block to Governance YAML**

Extend the governance YAML schema to support a separate `semantic_validation` array distinct from `input_validation`, where semantic checks and their prerequisites are documented.

| Criterion | Assessment |
|-----------|------------|
| Addresses root cause | Yes -- explicit structural separation of check types |
| Schema change required | Yes -- `agent-governance-v1.schema.json` update |
| CI gate impact | Good -- clear separation helps CI gate authors |
| Consistency | High -- applies the boundary rule systematically |
| Implementation complexity | **Medium** -- schema versioning + updates to all governance YAMLs |

### Recommended Option: A (Update Existing Entry)

**Justification:** The root cause is a precision gap in one governance YAML entry. Option A addresses it directly with minimal scope. Option C is architecturally better but requires schema versioning overhead that is not warranted for fixing one imprecise entry. Option B degrades CI gate visibility.

The underlying boundary question (when do behavioral constraints belong in governance YAML?) is answered by the proposed boundary rule above. If that rule is adopted as a standard, Option C becomes relevant for future agent definitions and a governance YAML v1.1 can incorporate the semantic_validation block. For now, Option A fixes the immediate gap.

**FMEA reduction analysis:** If Option A is implemented, D decreases from 8 to 5 (the prerequisite is now visible to CI gate operators). S remains 9 (incorrect contracts are still high severity if the check is bypassed). O remains 5. New RPN: 9 x 5 x 5 = 225, a 37.5% reduction. Further D reduction would require the CLI validation gate proposed in FM-002.

**Implementation complexity:** Low

**Specific implementation steps:**
1. Update `cd-generator.governance.yaml` input_validation entry 5 with the prerequisite wording above.
2. Add one sentence to `cd-generator.md` `<capabilities>` explicitly stating full artifact load is required.
3. No schema changes required.
4. Document the boundary rule (structural vs. semantic validation placement) in a comment in `cd-generator.governance.yaml` or in an ADR note.

---

## FM-002 Analysis

### Finding Summary

uc-slicer's methodology states "NEVER set `realization_level: INTERACTION_DEFINED` before populating `interactions[]`." The allOf constraint in `use-case-realization-v1.schema.json` (lines 489-502) now enforces that when `realization_level: INTERACTION_DEFINED` is present, `interactions[]` must be present and non-empty. The adversary's finding (D=9) predates or assumed absence of this constraint. The question is: does the schema constraint alone close the enforcement gap, or is additional validation needed?

The adversary RPN: S=9, O=4, D=9 = 324.

### Root Cause Analysis (5 Whys)

| Level | Question | Answer | Evidence |
|-------|----------|--------|----------|
| Why 1 | Why does setting `realization_level: INTERACTION_DEFINED` without populating interactions[] have D=9 (very hard to detect)? | Because the enforcement mechanism is a behavioral LLM instruction ("NEVER set...") which may not fire under context pressure or conflicting instructions | `uc-slicer.md` REALIZATION VIOLATION forbidden action -- behavioral instruction only at time of adversary review |
| Why 2 | Why is behavioral instruction insufficient as sole enforcement? | Because LLM behavioral instruction compliance degrades under context pressure, long sessions, and conflicting instructions -- it is not deterministic | General LLM instruction-following reliability properties; adversary report D=9 assessment |
| Why 3 | Why is there no structural enforcement gate? | At time of adversary review, the allOf constraint was not yet in the schema | The adversary report states "there is no enforcement mechanism that cross-checks the value against actual array population at runtime" -- this was accurate before the schema update |
| Why 4 | Why does the allOf constraint (now present) not fully close the gap? | The allOf constraint `if realization_level = INTERACTION_DEFINED then interactions minItems: 1` catches the empty array case but does not catch: (a) interactions present but source_step references broken, (b) interactions present but required fields missing, (c) interactions populated by a previous session and realization_level set incorrectly for the current state | `use-case-realization-v1.schema.json` allOf constraint at lines 489-502 -- verified present; structural check only |
| Why 5 | Why does schema validation not catch all semantic violations? | JSON Schema validates structure (field presence, type, cardinality), not semantics (is the source_step value valid given the flow content?). Semantic validation requires an agent or CLI that loads and cross-checks the artifact. | JSON Schema Draft 2020-12 semantic scope limitations; the allOf constraint is structural |

**Root Cause:** The enforcement gap has two layers: (Layer 1) structural enforcement -- whether `interactions[]` is present and non-empty when `realization_level: INTERACTION_DEFINED`. The schema allOf constraint now closes this layer. (Layer 2) semantic enforcement -- whether the content of `interactions[]` is coherent (source steps reference real steps, required sub-fields are meaningful). Layer 2 requires a CLI validation step.

**Updated D estimate with schema constraint:** D decreases from 9 to 6. The structural violation (empty interactions[] with INTERACTION_DEFINED) is now caught by schema validation. The semantic violation (malformed or disconnected interactions[]) remains at D=7-8. New RPN for the remaining gap: 9 x 4 x 6 = 216 (structural), 9 x 3 x 7 = 189 (semantic).

### Steelman of Alternative Hypotheses (H-16)

**Alternative hypothesis: The schema constraint is sufficient.** Argument: The allOf constraint eliminates the most dangerous failure mode (setting INTERACTION_DEFINED with empty interactions[]). The remaining semantic gap (malformed interactions) will be caught by cd-generator's Layer 1 structural validation before any contract is generated. The pipeline has defense-in-depth: schema validation, then uc-slicer post-completion checks, then cd-generator input validation. Adding a CLI step at uc-slicer output is redundant. Strength: the defense-in-depth argument is correct and the pipeline is not broken by the remaining gap. Weakness: the adversary's D=9 assessment was about preventing the violation, not catching it downstream. If uc-slicer produces a structurally valid but semantically broken artifact, the error will surface at cd-generator with less context about what went wrong (the user will receive a cd-generator error, not a uc-slicer error). Catching the violation at uc-slicer is better UX.

### Schema Constraint vs. CLI Validation: Detailed Gap Analysis

**What the allOf constraint closes:**

| Failure Mode | Before Schema Constraint | After Schema Constraint |
|-------------|--------------------------|------------------------|
| `realization_level: INTERACTION_DEFINED` + `interactions: []` (empty) | Not caught | Caught by allOf (minItems: 1) |
| `realization_level: INTERACTION_DEFINED` + `interactions` field absent | Not caught | Caught by allOf (required: interactions) |
| `realization_level: INTERACTION_DEFINED` + `interactions` present, non-empty, but `source_step` references non-existent flow step | Not caught | Still not caught |
| `realization_level: INTERACTION_DEFINED` + `interactions` present, non-empty, but required sub-fields (id, actor_role, etc.) incomplete | Partially caught (interaction schema validates required fields) | Same -- interaction schema validates structure |
| `realization_level: INTERACTION_DEFINED` + detail_level < ESSENTIAL_OUTLINE | Not caught | Caught by allOf (the incompatibility constraint at lines 538-547) |

**What the allOf constraint does not close:**

The schema validates that interactions[] is non-empty and each interaction has the 7 required fields. It does not validate that `source_step` references a real step in `source_flow` (the cross-reference validation problem, similar to FM-001). This is a semantic check.

### Options and Trade-offs

**Option A: Schema Constraint Only (Baseline -- Already Done)**

Accept the schema allOf constraint as the full fix. Rely on cd-generator's input validation (Layer 2 semantic check) to catch source_step inconsistencies downstream.

| Criterion | Assessment |
|-----------|------------|
| Structural violation detection | Closed |
| Semantic violation detection | Partially closed (sub-field structure); cross-reference still open |
| User experience | Moderate -- error surfaces at cd-generator, not uc-slicer |
| Implementation complexity | Zero (already done) |
| Remaining RPN (structural) | 9 x 4 x 4 = 144 (acceptable) |
| Remaining RPN (semantic) | 9 x 3 x 7 = 189 (elevated) |

**Option B: Schema Constraint + Post-Creation CLI Validation Step (Recommended)**

After uc-slicer sets `realization_level: INTERACTION_DEFINED`, add an explicit post-creation verification step:

```bash
uv run jerry ast validate {artifact_path} --schema use_case_realization
```

This invokes the CLI schema validator (H-05 compliant) against the updated artifact. Any allOf constraint violation is caught immediately at the uc-slicer output boundary, before the artifact is considered complete.

Add to `uc-slicer.md` methodology Step 8: "After setting `realization_level: INTERACTION_DEFINED`, run `uv run jerry ast validate {artifact_path} --schema use_case_realization` to verify the allOf constraint. Only set the realization level if validation passes."

Add to `uc-slicer.governance.yaml` `validation.post_completion_checks`: `"verify_realization_level_allOf_constraint_via_jerry_ast_validate"`.

| Criterion | Assessment |
|-----------|------------|
| Structural violation detection | Fully closed |
| Semantic violation detection | Structural + sub-field structural fully closed; source_step cross-reference still requires LLM semantic check |
| User experience | Good -- error surfaces at uc-slicer output with artifact path context |
| Implementation complexity | **Low** -- two documentation additions + one CLI call |
| Remaining RPN (structural) | 9 x 4 x 2 = 72 (low) |
| Remaining RPN (semantic/cross-ref) | 9 x 3 x 6 = 162 (reduced by improved detection) |

**Option C: Schema Constraint + CLI Validation + Explicit Cross-Reference Check**

Extend the CLI validator to perform cross-reference checking (verify each `source_step` in `interactions[]` exists in the referenced `source_flow`). This mirrors the cd-generator requirement but moves it earlier in the pipeline.

| Criterion | Assessment |
|-----------|------------|
| Full enforcement closure | Yes -- both structural and semantic source_step gaps closed |
| CLI development required | Yes -- `jerry ast validate` would need a semantic cross-reference mode |
| Implementation complexity | **High** -- requires framework CLI change |
| Remaining RPN | 9 x 4 x 2 = 72 (structural), 9 x 3 x 3 = 81 (semantic) |

### Recommended Option: B (Schema Constraint + Post-Creation CLI Validation)

**Justification:** Option A (schema constraint only) is already implemented and closes the structural gap. It is a necessary but not sufficient fix. The remaining D=7 for semantic violations is elevated enough to warrant Option B's low-cost improvement.

Option B adds one CLI call and two documentation additions. This is consistent with how cd-generator handles its own post-creation verification (the methodology already calls `uv run jerry ast validate`). uc-slicer should follow the same pattern at the moment of the state transition, not after the artifact is handed off.

Option C's value depends on whether `jerry ast validate` supports cross-reference mode. If this is a planned feature, Option C should be evaluated at that time. For now, the cross-reference semantic check remains in LLM behavioral territory (acceptable given that the structural enforcement now catches the most common error case).

**Updated FMEA assessment after Options A+B:**
- Structural violation (empty interactions + INTERACTION_DEFINED): S=9, O=4, D=2 (caught by schema validation + CLI) = RPN 72 (acceptable)
- Semantic violation (broken source_step + INTERACTION_DEFINED): S=9, O=3, D=6 (partially caught by CLI structural check, uncaught semantic) = RPN 162 (monitor)
- Total RPN reduction from original 324: approximately 55% for structural case, 50% for semantic case

**Implementation complexity:** Low

**Specific implementation steps:**
1. No schema changes required (allOf constraint already present and verified in `use-case-realization-v1.schema.json` lines 489-502).
2. Add to `uc-slicer.md` methodology Step 8 (Activity 5 completion): "Run `uv run jerry ast validate {artifact_path} --schema use_case_realization` before finalizing realization_level: INTERACTION_DEFINED."
3. Add to `uc-slicer.governance.yaml` `validation.post_completion_checks`: `"verify_realization_level_allOf_constraint_via_jerry_ast_validate"`.
4. Update `uc-slicer.governance.yaml` `output_filtering` entry `realization_level_must_match_populated_blocks` to include: "(enforced by allOf schema constraint + jerry ast validate post-creation check)".

**Assumption stated explicitly:** This analysis assumes `uv run jerry ast validate` with `--schema use_case_realization` is functional and can execute the allOf constraint against a YAML frontmatter file. If this CLI command does not currently support this validation mode, Option B requires CLI development that moves it from Low to Medium complexity.

---

## Cross-Cutting Observations

### Observation 1: The Dual-File Architecture Boundary is Under-Specified

All three findings expose the same underlying tension: the H-34 dual-file architecture divides agent definition content between a .md behavioral file and a .governance.yaml machine-readable file, but the boundary for what goes in each file is not precisely specified for semantic constraints.

The boundary rule proposed in FM-001 (structural vs. semantic vs. behavioral) provides a principled answer. If adopted, it should be documented in `agent-development-standards.md` under the "Agent Definition Schema" section as a MEDIUM standard for input_validation content placement.

### Observation 2: Enforcement Depth Matters More Than Enforcement Presence

FM-001 and FM-002 both demonstrate that having a rule documented is not the same as having the rule enforced. FM-001's governance YAML has the cross-reference rule but is missing its prerequisite. FM-002's governance YAML has the realization_level rule but has no executable enforcement mechanism.

For high-RPN failure modes (RPN > 200), behavioral instructions alone are insufficient. The threshold for adding a CLI validation step should be: RPN > 200 OR the failure mode cascades into a downstream agent's input (which is the case for both FM-001 and FM-002).

### Observation 3: PM-001 Pattern Applies to tspec-generator/tspec-analyst

The adversary's PM-003 finding (tspec-generator and tspec-analyst have no structured handoff format) is structurally identical to PM-001. The Option A solution (structured rejection artifact) should be designed to apply to both agent pairs. This is additional justification for Option A over Option C (SKILL.md documentation only) -- a general pattern is worth the minimal implementation cost.

---

## Evidence Summary

| Evidence ID | Type | Source | Relevance |
|-------------|------|--------|-----------|
| E-001 | Agent definition | `skills/use-case/agents/uc-slicer.md` Failure Modes table | PM-001: rejection is human-readable text only |
| E-002 | Governance YAML | `skills/use-case/agents/uc-author.governance.yaml` session_context | PM-001: no on_reject protocol defined |
| E-003 | Governance YAML | `skills/use-case/agents/uc-slicer.governance.yaml` session_context | PM-001: no on_reject protocol defined |
| E-004 | Schema | `docs/schemas/session_context.json` blockers array definition | PM-001: blockers are forward-facing (source to target), not backward-facing |
| E-005 | Adversary finding | `adversary-agent-findings.md` PM-001 | PM-001: finding evidence and analysis |
| E-006 | Governance YAML | `skills/contract-design/agents/cd-generator.governance.yaml` input_validation entry 5 | FM-001: cross-reference check present but missing prerequisite |
| E-007 | Agent definition | `skills/contract-design/agents/cd-generator.md` guardrails Layer 2 | FM-001: behavioral check present and complete |
| E-008 | Adversary finding | `adversary-agent-findings.md` FM-001 | FM-001: RPN 360, D=8 assessment |
| E-009 | Schema | `docs/schemas/agent-governance-v1.schema.json` guardrails.input_validation | FM-001: schema accepts string arrays without prerequisite format requirement |
| E-010 | Schema | `docs/schemas/use-case-realization-v1.schema.json` allOf lines 489-502 | FM-002: allOf constraint IS present and enforces INTERACTION_DEFINED requires interactions minItems:1 |
| E-011 | Agent definition | `skills/use-case/agents/uc-slicer.md` REALIZATION VIOLATION forbidden action | FM-002: behavioral enforcement present |
| E-012 | Governance YAML | `skills/use-case/agents/uc-slicer.governance.yaml` output_filtering | FM-002: realization_level_must_match_populated_blocks as string constraint |
| E-013 | Governance YAML | `skills/use-case/agents/uc-slicer.governance.yaml` validation.post_completion_checks | FM-002: verify_interactions_present check exists but no CLI command invocation |
| E-014 | Adversary finding | `adversary-agent-findings.md` FM-002 | FM-002: RPN 324, D=9 assessment |
| E-015 | Schema | `docs/schemas/use-case-realization-v1.schema.json` allOf lines 538-547 | FM-002: additional constraint blocking INTERACTION_DEFINED at BRIEFLY_DESCRIBED/BULLETED_OUTLINE detail level |

---

## PS Integration

**PS ID:** Not yet assigned (analysis produced as part of PROJ-021 verification phase)
**Entry context:** Adversary review of PROJ-021 agent definitions (use-case, test-spec, contract-design skills)
**Analysis type:** Trade-off (design decisions required before fixes can be implemented)
**Analyst output key:** `analyst_output`

```yaml
analyst_output:
  analysis_type: "trade-off"
  artifact_path: "projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/verification/pm001-fm001-fm002-analysis.md"
  recommendations:
    PM-001: "Option A -- Structured Rejection Artifact (Low complexity)"
    FM-001: "Option A -- Update existing governance YAML entry precision (Low complexity)"
    FM-002: "Option B -- Schema constraint (done) + post-creation CLI validation step (Low complexity)"
  confidence: "high"
  next_agent_hint: "ps-architect for deciding whether to adopt the boundary rule as a MEDIUM standard in agent-development-standards.md"
```

---

*Analysis produced by ps-analyst*
*Frameworks applied: 5 Whys (root cause), Trade-off Matrix (options), FMEA (RPN assessment)*
*Evidence base: adversary-agent-findings.md, 3 agent definitions (.md), 3 governance YAMLs (.governance.yaml), 2 schemas (agent-governance-v1, use-case-realization-v1), session_context schema*
*Constitutional compliance: P-001 (all conclusions evidence-based, E-001 through E-015), P-002 (persisted to file), P-022 (assumptions explicitly stated, uncertainty acknowledged)*
*H-15 self-review: completed -- conclusions follow from evidence; causal claims verified against cited files; assumption about jerry ast validate CLI capability explicitly flagged*
*Date: 2026-03-11*
