# Strategy Execution Report: Red Team Analysis

## Execution Context
- **Strategy:** S-001 (Red Team Analysis)
- **Template:** `.context/templates/adversarial/s-001-red-team.md`
- **Deliverables:**
  - `skills/use-case/agents/uc-author.md` + `uc-author.governance.yaml`
  - `skills/use-case/agents/uc-slicer.md` + `uc-slicer.governance.yaml`
  - `skills/test-spec/agents/tspec-generator.md` + `tspec-generator.governance.yaml`
  - `skills/test-spec/agents/tspec-analyst.md` + `tspec-analyst.governance.yaml`
  - `skills/contract-design/agents/cd-generator.md` + `cd-generator.governance.yaml`
  - `skills/contract-design/agents/cd-validator.md` + `cd-validator.governance.yaml`
  - `skills/use-case/SKILL.md`, `skills/test-spec/SKILL.md`, `skills/contract-design/SKILL.md`
  - `docs/schemas/use-case-realization-v1.schema.json`
  - `docs/schemas/test-specification-v1.schema.json`
- **Prior Security Assessment:** `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/verification/red-team-security-assessment.md`
- **Executed:** 2026-03-12T00:00:00Z
- **H-16 Compliance:** S-003 Steelman confirmed in C4 tournament prior strategy outputs per orchestrator instruction. This execution proceeds as part of the C4 tournament sequence.

---

## Threat Actor Profile

**Goal:** An adversary who wants to (a) produce incorrect, incomplete, or misleading artifacts from the use-case/test-spec/contract-design pipeline without triggering any validation rejections, or (b) cause the pipeline to silently skip quality gates, or (c) inject guidance into agent reasoning that manipulates their behavior in unsafe ways.

**Capability:** Full read access to all agent definitions, schema files, and SKILL.md files. Insider knowledge of every validation rule, every fallback path, and every "warn and proceed" behavior. Ability to craft input artifacts that are syntactically valid but semantically adversarial. Operates within the same-trust-boundary model (same user session, same filesystem).

**Motivation:** Ship a use case pipeline artifact -- whether a use case, Feature file, or OpenAPI contract -- that appears compliant but either omits critical behavioral coverage, contains misleading quality signals, or bypasses downstream quality gates, thus causing downstream implementers to build against incomplete or incorrect specifications.

---

## Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| RT-001-20260312 | Critical | fallback_location path traversal bypasses JERRY_PROJECT isolation | uc-author.md `<output>`, uc-slicer.md `<capabilities>`, all governance YAML `output.fallback_location` |
| RT-002-20260312 | Critical | uc-author del-after-elaborate can be triggered to delete a rejection artifact that was not consumed | uc-author.md "Post-elaboration cleanup" |
| RT-003-20260312 | Critical | test-specification-v1 schema allows source_goal_level SUBFUNCTION with 60% coverage target enabling silent quality gate bypass | `docs/schemas/test-specification-v1.schema.json` |
| RT-004-20260312 | Major | tspec-analyst coverage denominator is computed from loaded artifact state, not from the Feature file's snapshot -- allows stale UC to inflate apparent coverage | tspec-analyst.md Step 2 |
| RT-005-20260312 | Major | cd-generator missing_elements checklist extraction has no cap -- oversized rejection artifact bloats context silently | uc-author.md step 2f, uc-slicer.md rejection artifact template |
| RT-006-20260312 | Major | tspec-generator slice_id scoped generation silently reduces coverage denominator without user notification | tspec-generator.md "Slice-Scoped Generation Mode" |
| RT-007-20260312 | Major | cd-validator Step 8 provider interaction check is non-critical fail -- adversary can omit all internal operations documentation without blocking PASS | cd-validator.md Step 8 |
| RT-008-20260312 | Major | uc-slicer Rejection Artifact Protocol has no check for path traversal in `rejected_artifact` field -- adversary can point rejection at a different artifact | uc-slicer.md "Rejection Artifact Protocol" |
| RT-009-20260312 | Minor | test-specification-v1 `generated_by: const: tspec-generator` is not validated against any trusted source -- any agent can write a conformant feature file YAML and claim tspec-generator provenance | test-specification-v1.schema.json `generated_by` |
| RT-010-20260312 | Minor | uc-author breadth-first authoring rule PAT-001 has no machine-enforceable gate -- adversary can skip steps 1-4 without schema rejection | uc-author.md "Breadth-First Authoring (PAT-001)" |

---

## Detailed Findings

### RT-001-20260312: fallback_location Path Traversal Bypasses JERRY_PROJECT Isolation [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | `uc-author.md <output>`, `uc-slicer.md <capabilities>`, all governance YAML `output.fallback_location` and `output.location` |
| **Strategy Step** | Step 2 (Enumerate Attack Vectors) -- Boundary Violation category |

**Attack Vector:**

All six agents declare an `output.fallback_location` that resolves to `work/...` when `JERRY_PROJECT` is not set. The agent definitions state:

> "Output path resolves to `projects/${JERRY_PROJECT}/...` when JERRY_PROJECT is set. Falls back to `work/...` when JERRY_PROJECT is not set."

An adversary can deliberately ensure that `JERRY_PROJECT` is not set in the environment when invoking the pipeline. The fallback path `work/use-cases/`, `work/test-specs/`, and `work/contracts/` is not scoped to any project, creating two exploit paths:

1. **Isolation bypass:** By unsetting `JERRY_PROJECT`, the adversary routes all generated artifacts to a shared `work/` directory outside project isolation. Multiple projects' artifacts co-mingle, enabling cross-contamination where uc-slicer or tspec-generator reads the wrong artifact.

2. **Path traversal via fallback_location:** The `fallback_location` field value is defined in governance YAML as a template string (`work/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md`). The `{slug}` is derived from the use case title. An artifact with a title containing `../` characters (e.g., `title: "../../../etc/passwd"`) could produce a slug that traverses the filesystem when the slug is interpolated into the fallback path. No slug sanitization is defined in any agent specification.

**Evidence:**
- `uc-author.governance.yaml` line 52: `fallback_location: "work/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md"`
- `uc-slicer.governance.yaml` line 53: `fallback_location: "work/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md"`
- `tspec-generator.governance.yaml` line 62: `fallback_location: "work/test-specs/UC-{DOMAIN}-{NNN}-{slug}.feature.md"`
- `cd-generator.governance.yaml` line 77: `fallback_location: "work/contracts/UC-{DOMAIN}-{NNN}-{slug}.openapi.yaml"`
- `uc-author.md <capabilities>`: "Falls back to `work/...` when JERRY_PROJECT is not set."
- No slug sanitization spec in any agent definition or schema

**Existing Defense:** None. The agents trust the slug derivation process entirely. The schema's `id` field pattern (`^UC-[A-Z]+-\d{3}$`) constrains the ID component but the slug is derived from the free-text `title` field with `maxLength: 120`.

**Dimension:** Internal Consistency (isolation contract broken), Traceability (artifacts written to unexpected locations)

**Countermeasure:** (P0 -- MUST mitigate before acceptance)
1. Define slug sanitization rules: slugs MUST be generated by lowercasing the title and replacing all non-alphanumeric characters (including `/`, `.`, `\`) with hyphens. Truncate at 80 characters.
2. Add input validation entry to each agent: "Validate that the computed slug contains no path separator characters (`/`, `\`, `..`) before writing to any output path."
3. Consider removing `fallback_location` entirely and requiring JERRY_PROJECT to be set (H-04 enforcement).

**Acceptance Criteria:** Each agent definition includes an explicit slug sanitization step that rejects or replaces path-unsafe characters before any file write. An artifact with `title: "../../../malicious"` must not produce a write attempt outside the project directory.

---

### RT-002-20260312: uc-author Post-Elaboration Cleanup Can Delete a Rejection Artifact That Was Not Fully Consumed [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | uc-author.md "Post-elaboration cleanup" |
| **Strategy Step** | Step 2 (Enumerate Attack Vectors) -- Rule Circumvention category |

**Attack Vector:**

uc-author's post-elaboration cleanup protocol states:

> "After successfully producing an artifact at or above `required_state.detail_level`: 1. Verify the produced artifact's `$.detail_level >= required_state.detail_level` from the rejection artifact. 2. If yes: delete `{artifact_path}-rejection.yaml` using Bash (`rm "{artifact_path}-rejection.yaml"`)."

The cleanup decision is purely level-comparison based, and the level comparison is performed against `required_state.detail_level` from the rejection artifact. An adversary can exploit this in two ways:

**Exploit Path 1 -- Schema-valid but semantically hollow artifact:**
uc-author produces a use case artifact that satisfies `$.detail_level = ESSENTIAL_OUTLINE` in the YAML frontmatter (passing the level comparison), but whose `extensions[]` array contains a single extension with an empty or minimally valid `steps[]` array. The schema requires `extensions` to exist with `minItems: 1` at ESSENTIAL_OUTLINE, but the extension's `steps` array has `minItems: 1` -- meaning a single-step extension with an empty `action` field of length 1 satisfies the schema. The cleanup fires. The rejection artifact is deleted. The information that uc-slicer requires ESSENTIAL_OUTLINE quality is permanently lost. On the next uc-slicer invocation, it will either reject again (writing a new rejection artifact) or accept a marginally-valid artifact.

**Exploit Path 2 -- Rejection artifact from a different invocation cycle:**
The adversary runs uc-author twice: first pass produces a valid ESSENTIAL_OUTLINE artifact but the rejection artifact from an older failed run (pointing to a different `required_state`) is still on disk. uc-author reads the stale rejection artifact, finds `required_state.detail_level = ESSENTIAL_OUTLINE`, compares to the freshly produced artifact at `ESSENTIAL_OUTLINE`, concludes the condition is met, and deletes the rejection artifact. The stale rejection artifact (which contained important missing_elements guidance that was never acted upon) is silently destroyed.

The prior red-team assessment noted VULN-PM-003 (Low) for this -- the adversary S-001 analysis reveals this is more severe because it enables **silent loss of the backward error channel** without user awareness, not merely a "cleanup on failure" scenario.

**Evidence:**
- `uc-author.md` post-elaboration cleanup step 1: "Verify the produced artifact's `$.detail_level >= required_state.detail_level` from the rejection artifact."
- `uc-author.md` post-elaboration cleanup step 2: "If yes: delete `{artifact_path}-rejection.yaml` using Bash"
- `docs/schemas/use-case-realization-v1.schema.json` line 538: `extensions.minItems: 1` at ESSENTIAL_OUTLINE (allOf constraint 6) -- does not require semantic completeness
- Rejection artifact protocol has no freshness correlation between rejection artifact content and the current artifact content

**Existing Defense:** Partial -- the T3 staleness check (step 2d) warns about stale timestamps, but it fires based on filesystem mtime comparison, not on semantic completeness of the produced artifact.

**Dimension:** Completeness (backward error channel destroyed), Internal Consistency (cleanup condition too weak)

**Countermeasure:** (P0 -- MUST mitigate before acceptance)
1. Before deleting the rejection artifact, verify that ALL items in `missing_elements[]` from the rejection artifact are satisfied in the produced artifact (not just the level). For each `missing_element`, check the corresponding field is non-empty.
2. Add a semantic completeness check: if `missing_elements` included "extensions[] empty or absent", verify that `$.extensions` is now non-empty and each extension has a non-trivial `steps[]` (length >= 1 with non-empty `action` fields).
3. Log the deletion action to the user: "Rejection artifact deleted after confirming artifact at ESSENTIAL_OUTLINE with {N} extensions meeting {M} of {M} required elements."

**Acceptance Criteria:** uc-author produces a schema-valid artifact with a minimal single-extension skeleton at ESSENTIAL_OUTLINE but with only a one-character action field. The rejection artifact must NOT be deleted if the rejection artifact's missing_elements listed substantive content requirements that are clearly not met by the minimal artifact.

---

### RT-003-20260312: test-specification-v1 Schema Allows SUBFUNCTION Goal Level With Silent 60% Coverage Floor [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | `docs/schemas/test-specification-v1.schema.json` `source_goal_level` description |
| **Strategy Step** | Step 2 (Enumerate Attack Vectors) -- Ambiguity Exploitation category |

**Attack Vector:**

The `test-specification-v1.schema.json` schema defines coverage targets in the `source_goal_level` field description:

> "Goal level of the source use case. Determines coverage target: USER_GOAL=100%, SUBFUNCTION=80%, SUMMARY=60%."

However, the `tspec-analyst.md` methodology section defines a **different** set of coverage targets:

> "Coverage targets by goal level: USER_GOAL: 100%, SUMMARY: 80%+, SUBFUNCTION: 100%"

These are contradictory. The schema says SUBFUNCTION needs 80%, the analyst says it needs 100%. The schema says SUMMARY needs 60%, the analyst says 80%+.

An adversary who understands this contradiction can exploit it in two directions:

**Exploit Path 1 -- Force SUMMARY target to 60% via schema assertion:**
An adversary creates a use case artifact at SUMMARY goal level, generates a Feature file with only 60% flow coverage, and writes a test-specification-v1 conformant frontmatter that claims `coverage_target_met: true` (the `quality.coverage_target_met` field is a boolean that the adversary sets directly). tspec-analyst reads the Feature file, sees the schema-valid frontmatter with `coverage_target_met: true`, and may defer to the frontmatter's claim rather than recomputing from the schema target.

**Exploit Path 2 -- SUBFUNCTION UC pipeline bypass:**
A use case at SUBFUNCTION goal level is expected to have granular, fully-testable flows. The schema claims 80% is acceptable for SUBFUNCTION. The adversary creates a SUBFUNCTION use case with 5 extensions, generates Feature file scenarios for only 4 of them (80% coverage), and the schema-defined target of 80% is technically met. But the tspec-analyst methodology requires 100% for SUBFUNCTION -- the adversary who knows the schema will argue against the analyst's report using the schema's stated target.

This is a Critical finding because the schema is the machine-enforceable artifact (used for L5 CI validation) while the analyst's methodology section is advisory. The schema's lower thresholds can be used to argue that coverage gaps are within specification.

**Evidence:**
- `docs/schemas/test-specification-v1.schema.json` `source_goal_level` description: "USER_GOAL=100%, SUBFUNCTION=80%, SUMMARY=60%"
- `tspec-analyst.md` Step 5: "Coverage targets by goal level: USER_GOAL: 100%, SUMMARY: 80%+, SUBFUNCTION: 100%"
- The schema's `quality.coverage_target_met` is a boolean set by the generator, not computed by a validator
- The coverage object has `additionalProperties: false` so no additional enforcement fields can be added without a schema change

**Existing Defense:** tspec-analyst is instructed to use the methodology table. But the schema says different things. A schema-valid Feature file with `coverage_target_met: true` and 60% coverage passes L5 schema validation.

**Dimension:** Internal Consistency (schema contradicts methodology), Methodological Rigor (thresholds not consistent across artifacts)

**Countermeasure:** (P0 -- MUST mitigate before acceptance)
1. Update `test-specification-v1.schema.json` to use coverage targets consistent with `tspec-analyst.md`: USER_GOAL=100%, SUMMARY=80%, SUBFUNCTION=100%.
2. Add a `coverage_target_minimum_percentage` field to the schema (computed property) that encodes the minimum numeric floor for the goal_level, enabling deterministic validation.
3. Remove the free-text `coverage_target_met` boolean or enforce it is set only by tspec-analyst, not tspec-generator.

**Acceptance Criteria:** The schema description for `source_goal_level` lists the same targets as the tspec-analyst methodology section. No artifact can be schema-valid with `coverage_target_met: true` and coverage below the goal-level target.

---

### RT-004-20260312: tspec-analyst Coverage Denominator Uses Live UC State, Not Feature File Snapshot [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | tspec-analyst.md Step 2 (Enumerate Mappable Flow Elements) |
| **Strategy Step** | Step 2 (Enumerate Attack Vectors) -- Dependency Attack category |

**Attack Vector:**

tspec-analyst computes coverage using the **live source UC artifact** as the coverage baseline:

> "Step 2: Enumerate Mappable Flow Elements. total_mappable_flows = 1 (basic_flow) + count($.alternative_flows) + count($.extensions)"

This count comes from reading the source UC artifact at analysis time, not from any snapshot embedded in the Feature file's YAML frontmatter. The Feature file's `coverage` block contains `total_flows` and `mapped_flows` as recorded by tspec-generator at generation time.

**Exploit Chain:**

1. Adversary runs tspec-generator on UC-AUTH-001 which has 5 extensions. Feature file records `total_flows: 7` (1 basic + 1 alternative + 5 extensions).
2. Adversary modifies the source UC artifact, removing 3 extensions (which had no corresponding scenarios in the Feature file). The UC now has 2 extensions.
3. Adversary runs tspec-analyst. tspec-analyst reads the live UC: `total_mappable_flows = 1 + 1 + 2 = 4`. The Feature file has 4 mapped scenarios (the basic flow + 1 alternative + 3 extension scenarios that WERE covered).
4. tspec-analyst computes coverage as 4/4 = 100% -- PASS.
5. The 2 removed extensions (which had no BDD coverage) are invisible to tspec-analyst because they are no longer in the UC. The Feature file's original `total_flows: 7` metadata is not consulted.
6. The result: a Feature file that originally had 57% coverage (4/7 flows mapped) appears to have 100% coverage after the adversary removes 3 extensions from the UC.

This attack is particularly dangerous because it produces a PASS verdict from tspec-analyst for a Feature file that does not cover all of the UC's original behavior.

**Evidence:**
- `tspec-analyst.md` Step 2: "total_mappable_flows = 1 (basic_flow) + count($.alternative_flows) + count($.extensions)" -- reads live UC, not Feature file snapshot
- `test-specification-v1.schema.json` Feature file frontmatter includes `coverage.total_flows` (integer, recorded at generation time), but tspec-analyst does not cross-reference this against the live UC count
- `tspec-analyst.md` Step 3: "Parse each Gherkin Scenario block from the Feature file" -- correctly reads the Feature file for mapped scenarios, but uses a different denominator than what was recorded at generation time

**Existing Defense:** Missing. The Feature file records `total_flows` at generation time, but tspec-analyst ignores this field in its coverage computation.

**Dimension:** Internal Consistency (coverage denominator inconsistency), Evidence Quality (coverage report does not reflect original UC completeness)

**Countermeasure:** (P1 -- SHOULD mitigate)
1. tspec-analyst Step 2 MUST cross-reference the live UC flow count against the Feature file's `coverage.total_flows`. If they differ, warn: "UC has been modified since Feature file was generated. Feature file recorded {N} total flows; current UC has {M} flows. Coverage is computed against current UC ({M} flows), but the original Feature file may have unmapped flows from when the UC had {N} flows. Recommend re-running tspec-generator before accepting coverage results."
2. Add a `source_use_case_version` field to the Feature file frontmatter (sourced from UC's `version` field) and verify it matches at analysis time.

**Acceptance Criteria:** When the live UC has fewer extensions than when the Feature file was generated, tspec-analyst detects the discrepancy and warns the user, preventing silent coverage inflation from UC regression.

---

### RT-005-20260312: Rejection Artifact missing_elements Array Has No Count Cap -- Context Saturation Attack [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | uc-author.md step 2f, uc-slicer.md "Rejection Artifact Protocol" |
| **Strategy Step** | Step 2 (Enumerate Attack Vectors) -- Dependency Attack category |

**Attack Vector:**

uc-author step 2f states:

> "Extract `missing_elements[]` as the elaboration checklist -- use these as the specific content gaps to address during elaboration."

uc-slicer's rejection artifact template defines `missing_elements` as an array with no `maxItems` constraint. An adversary with write access to a rejection artifact (or an adversarially crafted UC that causes uc-slicer to write a pathological rejection artifact) can write a `missing_elements` array with hundreds of entries.

**Exploit Chain:**

1. Adversary creates a UC artifact at BRIEFLY_DESCRIBED with a trigger that causes uc-slicer to enumerate a very large missing_elements list (e.g., an artifact with 9 flow steps each generating a distinct missing element).
2. uc-slicer writes a rejection artifact with `missing_elements: [200 entries]`.
3. uc-author reads the rejection artifact and extracts the full `missing_elements[]` checklist into its working context.
4. The 200-item checklist consumes a significant portion of uc-author's context window, degrading the quality of the actual elaboration work.
5. The adversary repeats this by ensuring the UC artifact remains at BRIEFLY_DESCRIBED (easy, since uc-author must still write content), cycling the oversized rejection artifact into uc-author's context on every invocation.

This is an amplification attack: the adversary does not need to inject malicious instructions (T1 injection), only large benign-looking data. The context saturation degrades uc-author's quality outputs without triggering any guardrail.

**Evidence:**
- `uc-slicer.md` rejection artifact template: `missing_elements:` array with no `maxItems` constraint
- `uc-author.md` step 2f: "Extract `missing_elements[]` as the elaboration checklist -- use these as the specific content gaps to address during elaboration." -- no length truncation specified
- `uc-author.governance.yaml` session_context.on_receive: "extract missing_elements[] as elaboration checklist" -- no length cap
- Prior red-team assessment VULN-PM-005 (Info): flagged this as an Info finding; adversarial analysis reveals it is exploitable with higher severity in repeated-invocation contexts

**Existing Defense:** Missing. No cap on `missing_elements` array size in either uc-slicer (writer) or uc-author (consumer).

**Dimension:** Completeness (context saturation degrades elaboration quality), Methodological Rigor (no context budget protection)

**Countermeasure:** (P1 -- SHOULD mitigate)
1. Add to uc-slicer rejection artifact protocol: "If missing_elements would exceed 10 items, consolidate to the 10 most actionable items and append a count note: 'and {N-10} additional elements -- run uc-author and address these first.'"
2. Add to uc-author step 2f: "If `missing_elements[]` contains more than 10 items, truncate to first 10 and warn user: 'Rejection artifact has {N} missing elements; elaborating against first 10.'"
3. Add `maxItems: 20` to the rejection artifact YAML template in uc-slicer.

**Acceptance Criteria:** A rejection artifact with 50 missing_elements entries is processed by uc-author using only the first 10 items. The user is warned about the truncation.

---

### RT-006-20260312: tspec-generator Slice-Scoped Generation Silently Reduces Coverage Denominator [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | tspec-generator.md "Slice-Scoped Generation Mode" |
| **Strategy Step** | Step 2 (Enumerate Attack Vectors) -- Circumvention category |

**Attack Vector:**

tspec-generator's slice-scoped generation mode states:

> "Coverage denominator is scoped to the filtered flows, not the full UC"

When `slice_id` is specified, tspec-generator filters `basic_flow`, `alternative_flows`, and `extensions` to only those whose anchor step is in the slice's `steps_included`. The coverage denominator shrinks accordingly. The L0 summary reports coverage against this filtered denominator.

**Exploit Chain:**

1. UC-AUTH-001 has 3 extensions: EXT-2A (failure), EXT-3A (rejoin), EXT-5A (failure). The happy path slice (Slice S1) includes steps 1-3. Slice S2 includes steps 4-5.
2. Adversary invokes tspec-generator with `slice_id: UC-AUTH-001-S1`. This filters to: basic flow (step 1-3 covered), EXT-2A, EXT-3A. EXT-5A (anchored at step 5) is excluded from the denominator.
3. tspec-generator generates scenarios for basic flow + EXT-2A + EXT-3A. Coverage: 3/3 = 100% for slice S1.
4. The adversary never invokes tspec-generator for slice S2. EXT-5A (a failure extension) is never covered.
5. tspec-analyst is later run against the slice-S1 Feature file and confirms 100% coverage -- which is technically correct for that slice.
6. No agent, schema, or process flags that slice S2 was never tested. EXT-5A remains uncovered.

The attack produces a pipeline where individual slices show 100% coverage but the full UC has uncovered failure paths. No validation gate requires aggregate coverage across all slices.

**Evidence:**
- `tspec-generator.md` Slice-Scoped Generation Mode: "Coverage denominator is scoped to the filtered flows, not the full UC"
- `tspec-analyst.md` Step 2 slice-scoped coverage formula: denominator is filtered to slice steps only
- Neither tspec-generator nor tspec-analyst requires or checks that all slices have been tested
- The SKILL.md does not mention a requirement for aggregate slice coverage before the UC is considered fully tested
- `docs/schemas/test-specification-v1.schema.json`: `slice_id` field is `type: ["string", "null"]` -- slice coverage is optional

**Existing Defense:** Missing. No cross-slice coverage aggregation mechanism exists. Each slice Feature file is analyzed independently.

**Dimension:** Completeness (aggregate coverage gap not detected), Evidence Quality (slice coverage appears complete when UC coverage is not)

**Countermeasure:** (P1 -- SHOULD mitigate)
1. Add to tspec-analyst output: when analyzing a slice-scoped Feature file, compute and report "aggregate UC coverage gap: the following flows from the full UC are not covered by any slice Feature file: {list}". This requires tspec-analyst to also read other Feature files for the same UC.
2. Add a SKILL.md requirement: "For full UC BDD coverage, all slices MUST have corresponding Feature files. Invoke tspec-analyst with the full UC artifact (not individual slices) as the final coverage verification step."
3. Add a post-completion check to tspec-generator governance: `verify_all_uc_extensions_covered_across_all_slice_feature_files`.

**Acceptance Criteria:** When a UC has 3 slices and only 2 slice Feature files exist, tspec-analyst explicitly flags that the third slice has no corresponding Feature file and lists its uncovered flows.

---

### RT-007-20260312: cd-validator Step 8 Provider Interaction Documentation Is Non-Critical Fail [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | cd-validator.md Step 8: Internal Operations Documentation |
| **Strategy Step** | Step 2 (Enumerate Attack Vectors) -- Circumvention category |

**Attack Vector:**

cd-validator Step 8 states:

> "Failure action: List each provider interaction with no `x-internal-operations` entry. Report as a documentation gap (not a critical FAIL unless all provider interactions are undocumented)."

This creates an exploitable loophole. The adversary can craft a UC with multiple provider interactions and deliberately omit all but one from the `x-internal-operations` block in the generated contract. cd-validator will document the gap but will NOT produce a FAIL verdict, because "not a critical FAIL unless all provider interactions are undocumented."

**Exploit Chain:**

1. UC has 3 provider interactions (INT-02, INT-04, INT-06) representing internal system calls.
2. cd-generator includes `x-internal-operations` for only INT-02. INT-04 and INT-06 are omitted.
3. cd-validator Step 8: INT-04 and INT-06 have no `x-internal-operations` entry. But INT-02 is documented. Therefore "not all provider interactions are undocumented" -- cd-validator does not FAIL.
4. The overall cd-validator verdict is PASS (assuming all other 8 steps pass).
5. Downstream implementers see a PASS contract with only 1/3 internal operations documented. They implement only the visible behavior, silently missing INT-04 and INT-06.

The explicit "not a critical FAIL unless all provider interactions are undocumented" exception creates a safe harbor for partial internal operations omission. An adversary who provides exactly 1 internal operations entry (regardless of how many provider interactions exist) can prevent Step 8 from producing a FAIL.

**Evidence:**
- `cd-validator.md` Step 8: "Report as a documentation gap (not a critical FAIL unless all provider interactions are undocumented)"
- `cd-validator.md` methodology: "Report a combined PASS verdict only if all 9 steps pass" -- contradicted by Step 8's partial FAIL exception
- `cd-validator.md` Step 8 failure action does not specify a coverage threshold (e.g., "FAIL if <80% of provider interactions are documented")

**Existing Defense:** Missing. The non-critical exception is explicit and unconditional except for the all-undocumented case.

**Dimension:** Internal Consistency (PASS/FAIL criteria inconsistent), Completeness (internal API surface documentation not enforced)

**Countermeasure:** (P1 -- SHOULD mitigate)
1. Remove the "not a critical FAIL unless all" exception and replace with: "FAIL if any provider interaction has no `x-internal-operations` entry. All provider interactions must be documented for a complete contract." This aligns with the completeness guarantee the contract is supposed to provide.
2. If partial internal documentation is intentionally acceptable, define an explicit threshold (e.g., "FAIL if fewer than 80% of provider interactions are documented") and add a corresponding coverage metric to the validation report.

**Acceptance Criteria:** A contract with 3 provider interactions where 2 lack `x-internal-operations` entries produces a FAIL verdict from cd-validator Step 8.

---

### RT-008-20260312: uc-slicer Rejection Artifact `rejected_artifact` Field Has No Canonical Path Validation [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | uc-slicer.md "Rejection Artifact Protocol" step 2, uc-author.md "Rejection Artifact Check" step 2d |
| **Strategy Step** | Step 2 (Enumerate Attack Vectors) -- Boundary Violation category |

**Attack Vector:**

uc-slicer writes the rejection artifact with `rejected_artifact: "{repository-relative path to the artifact}"`. uc-author validates this field:

> "**Validate `rejected_artifact` matches the current artifact path (T2 path-traversal mitigation)** -- if the paths do not match, log a warning ('Rejection artifact rejected_artifact field does not match current artifact path -- ignoring') and proceed without rejection context."

However, the check is a string equality comparison between `rejected_artifact` and the `current artifact path`. This comparison is sensitive to:

1. **Relative vs absolute path mismatch:** uc-slicer writes a repository-relative path (`projects/PROJ-021/use-cases/UC-AUTH-001-authenticate-user.md`). uc-author may receive the artifact path as an absolute path (`/home/user/workspace/jerry/projects/PROJ-021/use-cases/UC-AUTH-001-authenticate-user.md`). The string comparison fails, uc-author logs a warning, and proceeds without rejection context. The adversary can then provide a different artifact path to uc-author that makes the absolute/relative comparison succeed for an incorrect target.

2. **Symlink traversal:** If the artifact is accessed via a symlink and uc-author resolves the symlink to the canonical path but uc-slicer records the symlink path in `rejected_artifact`, the comparison fails and the rejection context is silently ignored.

3. **Case sensitivity:** On case-insensitive filesystems (macOS HFS+), `UC-AUTH-001.md` and `uc-auth-001.md` refer to the same file but produce different path strings, causing the comparison to fail.

These mismatches cause uc-author to proceed WITHOUT rejection context -- meaning a rejected artifact is elaborated without the guidance from uc-slicer about what was missing. The rejection artifact still exists on disk, creating a stale artifact for future invocations.

**Evidence:**
- `uc-slicer.md` Rejection Artifact Protocol step 2: `rejected_artifact: "{repository-relative path to the artifact}"`
- `uc-author.md` step 2d: "Validate `rejected_artifact` matches the current artifact path" -- string comparison, no path normalization specified
- `uc-author.governance.yaml` on_receive step 4: "(T2 path-traversal mitigation -- ignore and warn if mismatch)" -- no canonical path normalization before comparison

**Existing Defense:** Partial -- the T2 mitigation is present but relies on exact string match without canonicalization.

**Dimension:** Internal Consistency (path comparison fragile), Evidence Quality (rejection context silently ignored on path mismatch)

**Countermeasure:** (P1 -- SHOULD mitigate)
1. Specify in both uc-slicer and uc-author that paths must be normalized before comparison: resolve to canonical absolute path (following symlinks, applying case normalization for case-insensitive filesystems) before the `rejected_artifact` match check.
2. uc-slicer should write the canonical absolute path in `rejected_artifact` (not the repository-relative path), or write both and have uc-author check either form.
3. Add an explicit step: "Canonicalize both `rejected_artifact` and the `current artifact path` to absolute paths before comparison."

**Acceptance Criteria:** A rejection artifact with `rejected_artifact: "projects/PROJ-021/use-cases/UC-AUTH-001.md"` is correctly matched against a uc-author invocation with an absolute path (`/home/user/.../projects/PROJ-021/use-cases/UC-AUTH-001.md`) pointing to the same file.

---

### RT-009-20260312: `generated_by: const: tspec-generator` Claim Not Verified Against Trusted Source [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `docs/schemas/test-specification-v1.schema.json` `generated_by` field |
| **Strategy Step** | Step 2 (Enumerate Attack Vectors) -- Dependency Attack category |

**Evidence:**

The `test-specification-v1.schema.json` schema enforces `generated_by: const: "tspec-generator"`. This creates a false provenance guarantee: the schema requires the string to be exactly "tspec-generator" but does not verify that the Feature file was actually produced by the tspec-generator agent. Any entity (human, other agent, script) that writes a conformant Feature file YAML frontmatter can claim tspec-generator authorship.

This enables adversaries to write Feature files that appear to be from tspec-generator (and thus appear to have Clark transformation traceability) but are actually hand-authored with fabricated Source annotations and coverage metrics.

**Analysis:** The schema cannot enforce authorship -- that is architecturally impossible with static JSON Schema validation. However, the absence of any signed or unforgeable provenance mechanism means the `generated_by` field provides false assurance. tspec-analyst trusts `generated_by: tspec-generator` as a signal that Clark traceability rules were followed, but this is unverifiable.

**Recommendation:** Add a documentation note to the schema: "`generated_by` is a self-reported provenance claim and is not cryptographically verified. tspec-analyst MUST verify Source annotations are present on every scenario rather than relying on `generated_by` as evidence of traceability."

---

### RT-010-20260312: PAT-001 Breadth-First Authoring Has No Machine-Enforceable Gate [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | uc-author.md "Breadth-First Authoring (PAT-001)" |
| **Strategy Step** | Step 2 (Enumerate Attack Vectors) -- Degradation category |

**Evidence:**

uc-author defines PAT-001:

> "Always apply Steps 1-4 for all use cases BEFORE elaborating ANY single use case to deeper levels. Never write the full basic flow (Step 5) before identifying all actors (Step 3). This prevents missed actors and incorrect goal level classification."

No machine-enforceable gate enforces PAT-001. The schema does not require that ALL use cases in a domain have been identified before any single use case advances beyond BULLETED_OUTLINE. The allOf constraints enforce per-artifact structural requirements but not cross-artifact ordering constraints.

An adversary who wants to produce a use case with incorrect goal classification or missed actors can simply skip PAT-001 and proceed depth-first. The artifact will validate against the schema. The missed actors only become visible in downstream failures (e.g., uc-slicer finds an actor referenced in extensions that was not declared in `supporting_actors`).

**Analysis:** This is inherently difficult to enforce mechanically without a worktracker integration that tracks all identified use cases for a given actor-goal list. The finding is Minor because the consequence (missed actors, incorrect goal levels) is correctable in subsequent elaboration cycles. The recommendation is to document PAT-001 as an advisory procedural constraint rather than a structural guarantee.

**Recommendation:** Add to PAT-001 specification: "Note: PAT-001 is a procedural constraint that cannot be enforced by schema validation. It relies on uc-author's reasoning about system scope. Non-compliance is observable when downstream /test-spec scenarios reference actors not declared in `$.supporting_actors[]`."

---

## Defense Gap Assessment

| Finding | Defense | Priority | Exploitability |
|---------|---------|----------|----------------|
| RT-001 (path traversal via slug) | Missing | P0 | Medium -- requires title with path chars |
| RT-002 (cleanup deletes stale rejection artifact) | Partial (staleness check) | P0 | Medium -- requires stale rejection artifact |
| RT-003 (schema vs. methodology coverage contradiction) | Missing | P0 | High -- contradiction is deterministic |
| RT-004 (live UC vs. snapshot denominator) | Missing | P1 | High -- requires UC modification after generation |
| RT-005 (missing_elements context saturation) | Missing | P1 | Medium -- requires many extensions in UC |
| RT-006 (slice coverage denominator reduction) | Missing | P1 | High -- any slice-scoped generation exploits this |
| RT-007 (Step 8 partial documentation PASS) | Missing | P1 | High -- one `x-internal-operations` entry bypasses FAIL |
| RT-008 (path comparison without canonicalization) | Partial (string equality check) | P1 | Medium -- relative/absolute path mismatch |
| RT-009 (provenance claim unverifiable) | Missing | P2 | Low -- requires crafting conformant YAML |
| RT-010 (PAT-001 unenforced) | Missing | P2 | Low -- consequences are correctable |

---

## Recommendations

### P0 -- MUST Mitigate Before Acceptance

**RT-001 (Critical) -- Slug sanitization:**
- Specification: add slug sanitization rules to all six agent definitions and governance YAML output location computation
- Action: define sanitization as lowercase + replace non-alphanumeric chars with hyphens + truncate to 80 characters
- Add input validation entry: "verify computed slug contains no path separators before any file write"

**RT-002 (Critical) -- Rejection artifact cleanup semantic check:**
- Before `rm "{artifact_path}-rejection.yaml"`, verify ALL items in `missing_elements[]` are addressed in the produced artifact (not just the level comparison)
- Log deletion to user with confirmation of satisfied items

**RT-003 (Critical) -- Schema/methodology coverage target alignment:**
- Update `test-specification-v1.schema.json` source_goal_level description to match tspec-analyst.md targets exactly: USER_GOAL=100%, SUMMARY=80%, SUBFUNCTION=100%
- Add `coverage_target_minimum_percentage` as a schema field with values enforced by the enum

### P1 -- SHOULD Mitigate

**RT-004 (Major) -- Live UC vs. generation-time snapshot:**
- tspec-analyst Step 2: cross-reference live UC flow count against Feature file `coverage.total_flows`; warn on discrepancy
- Add `source_use_case_version` to Feature file frontmatter

**RT-005 (Major) -- Context saturation via missing_elements:**
- uc-slicer: cap `missing_elements` at 10 items with a consolidation note
- uc-author step 2f: truncate at 10 items with user warning

**RT-006 (Major) -- Slice coverage denominator:**
- tspec-analyst: when analyzing slice-scoped Feature file, also compute and report aggregate UC coverage gap
- Add SKILL.md requirement for full-UC coverage verification step

**RT-007 (Major) -- Step 8 non-critical exception:**
- Remove the "not a critical FAIL unless all undocumented" exception; FAIL on any undocumented provider interaction
- Or define explicit coverage threshold (80%) and apply consistently

**RT-008 (Major) -- Path canonicalization:**
- Specify canonical path normalization (absolute path, symlink resolution, case normalization) before `rejected_artifact` match comparison

### P2 -- Monitor

**RT-009 (Minor):** Add documentation note that `generated_by` is self-reported. tspec-analyst should verify Source annotations independently.

**RT-010 (Minor):** Document PAT-001 as advisory, not structurally enforced.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | RT-006 (slice denominator reduction), RT-007 (provider interaction gap) create completeness illusions in multiple output artifacts |
| Internal Consistency | 0.20 | Negative | RT-003 (schema/methodology contradiction on coverage targets), RT-007 (inconsistent PASS/FAIL criteria in 9-step protocol) are direct internal consistency violations |
| Methodological Rigor | 0.20 | Negative | RT-004 (stale baseline), RT-008 (path comparison fragility), RT-010 (PAT-001 unenforced) undermine the rigorous methodology claims |
| Evidence Quality | 0.15 | Negative | RT-002 (rejection artifact deleted before semantic check), RT-003 (schema contradicts methodology) degrade evidence reliability |
| Actionability | 0.15 | Neutral | The agents provide actionable REJECT messages; countermeasures defined above are specific and implementable |
| Traceability | 0.10 | Negative | RT-001 (path traversal disrupts output location), RT-008 (rejection artifact path mismatch silently drops context), RT-009 (provenance claim unverifiable) weaken the traceability guarantees |

**Overall Assessment: REVISE -- targeted remediation required before acceptance.**

The pipeline has strong structural foundations: input validation gates, rejection artifact pattern, PROTOTYPE label, schema-validated frontmatter. However, the 3 Critical findings (RT-001, RT-002, RT-003) represent fundamental vulnerabilities that can cause the pipeline to silently produce misleading quality signals. The 5 Major findings represent meaningful circumvention paths that a motivated adversary can exploit without triggering any existing guardrail.

---

## Execution Statistics

- **Total Findings:** 10
- **Critical:** 3 (RT-001, RT-002, RT-003)
- **Major:** 5 (RT-004, RT-005, RT-006, RT-007, RT-008)
- **Minor:** 2 (RT-009, RT-010)
- **Protocol Steps Completed:** 5 of 5

---

*Strategy: S-001 Red Team Analysis*
*Finding Prefix: RT-NNN-20260312*
*Template: `.context/templates/adversarial/s-001-red-team.md` v1.0.0*
*Executed by: adv-executor*
*Constitutional Compliance: P-001 (all findings evidence-based with specific citations), P-002 (report persisted to file), P-003 (no subagents spawned), P-011 (evidence cited for every finding), P-022 (severity not minimized or inflated)*
