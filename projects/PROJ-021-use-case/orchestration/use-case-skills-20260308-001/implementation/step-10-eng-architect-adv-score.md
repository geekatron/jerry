# G-10-ADV-1 Score Report: /test-spec Architecture

> Iteration: 1 | Threshold: 0.95 | Date: 2026-03-09

## Scoring Context

- **Deliverable:** `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/implementation/step-10-test-spec-architecture.md`
- **Deliverable Type:** Architecture Design (Skill Architecture)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge) with all 10 C4 strategies
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-09
- **Phase 2 References Checked:** agent-decomposition.md (v1.1.0), file-organization.md (v2.1.0)
- **Step 9 Pattern Reference Checked:** step-9-use-case-architecture.md (v1.2.0)

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.91 | 0.182 | All 8 required sections present; 14-file manifest complete; agent specs both full; L0/L1/L2 all present; one gap: `rules/clark-transformation-rules.md` content not specified (F-12 deferred to eng-backend with no content outline) |
| Internal Consistency | 0.20 | 0.93 | 0.186 | ORCHESTRATION.yaml reconciliation fully addressed; agent naming rationale consistent throughout; one minor tension: tspec-analyst described as T1 then corrected to T2 within the same section — correction is transparent but the initial wrong statement remains in the published text |
| Methodological Rigor | 0.20 | 0.94 | 0.188 | Clark transformation implemented as deterministic lookup table matching agent-decomposition.md exactly; two-layer validation gate mirrors Step 9 pattern; 7 Cs framework correctly applied; agent split justified by 4 independent criteria matching Phase 2 contingency conditions; S-002/S-004 adversarial self-checks present |
| Evidence Quality | 0.15 | 0.92 | 0.138 | Clark (2018) cited with specific algorithm reference; Phase 2 SSOT cited by version and quality score; SD-07/SD-08 schema decisions cited by ID; JSON path notation used throughout; gap: "Clark (2018)" cited without full bibliographic reference (title, publication venue) -- matches Phase 2 pattern but still an evidence gap at C4 |
| Actionability | 0.15 | 0.95 | 0.143 | File Responsibility Matrix assigns every file to a specific sub-step and reviewer; governance YAML content is copy-paste ready; template skeletons are complete and implementable; ORCHESTRATION.yaml reconciliation table is exact; composition file schema reference links to canonical YAML schema; only marginal gap: F-12 clark-transformation-rules.md content is deferred without specifying what the content outline should be |
| Traceability | 0.10 | 0.93 | 0.093 | Lineage block at top traces all 5 upstream documents with versions and scores; Risk IDs trace to source documents (DI-05, PAT-008, CF-04 etc.); Clark mapping table traces every UC schema field to Gherkin element with Clark rule reference; ORCHESTRATION.yaml reconciliation table traces all 7 ORCH deliverables; minor gap: "7 Cs quality framework" attributed to "DI-06, PAT-004" but these internal IDs are not resolvable without the research document index |

**TOTAL** | **1.00** | | **0.930** |

---

## Weighted Composite

```
composite = (completeness    × 0.20) + (internal_consistency × 0.20) + (methodological_rigor × 0.20)
          + (evidence_quality × 0.15) + (actionability        × 0.15) + (traceability         × 0.10)

         = (0.91 × 0.20) + (0.93 × 0.20) + (0.94 × 0.20)
         + (0.92 × 0.15) + (0.95 × 0.15) + (0.93 × 0.10)

         = 0.182 + 0.186 + 0.188 + 0.138 + 0.143 + 0.093

         = 0.930
```

**Weighted Composite: 0.930 / 1.00**
**Threshold: 0.95 (C4, user override C-008)**
**Delta to threshold: -0.020**

---

## Verdict: REVISE

Score 0.930 does not meet the 0.95 threshold. The deliverable is strong and close to threshold, but specific gaps across multiple dimensions prevent acceptance at C4 quality.

---

## C4 Strategy Findings

### S-014 (LLM-as-Judge) — Primary Scoring

Applied across all 6 dimensions above. Leniency bias check: scores were initially drafted at 0.93-0.96 before evidence review; downward adjustments applied to Completeness (0.94 -> 0.91, F-12 content gap) and Evidence Quality (0.94 -> 0.92, bibliographic gap). The 0.95 threshold is the user-specified C-008 override; at the standard 0.92 threshold this deliverable would PASS.

### S-003 (Steelman) — Strongest Elements

The deliverable's strongest property is its **complete implementation fidelity to Phase 2 SSOT**. The Clark transformation mapping table in Section 5 achieves exact correspondence with agent-decomposition.md lines 248-259 (Clark Mapping Table). Every schema field mapped to a Gherkin element has a specific Clark rule citation (Step 2, Step 3 SD-07, Step 4, Step 5 SD-08). The agent split justification presents 4 independent criteria — cognitive mode distinction, methodology token count, I/O profile difference, and invocation frequency difference — none of which is circular or dependent on the others. This is textbook multi-criteria justification per P-011.

The ORCHESTRATION.yaml reconciliation section is exemplary: it proactively identifies every naming discrepancy between the preliminary ORCHESTRATION.yaml and the SSOT architecture, provides exact mappings for all 7 ORCH deliverables, and lists 7 additional files with rationale. This transparency directly addresses a known failure mode (teams implementing from ORCHESTRATION.yaml while the architecture specifies different names).

### S-013 (Inversion) — What Would Make This Fail?

**Inversion applied:** "What would a downstream implementer do wrong from this architecture that the architecture failed to prevent?"

1. **F-12 content gap.** `clark-transformation-rules.md` is listed in the file manifest (F-12) and cited in the agent's methodology section as the operational reference: "Reference: `skills/test-spec/rules/clark-transformation-rules.md` for operational rules." However, the architecture provides no content outline for this file. An implementer (eng-backend, sub-step 10e) has to author it from scratch with only "encodes the Clark transformation algorithm as agent rules" as guidance. There is no skeleton, no expected section structure, no list of the 7 mapping steps to include. Compare this to the templates (F-10, F-11), which have complete skeletons, and the agent markdown bodies (F-02, F-04), which have XML-tagged section outlines. F-12 is treated as a black box. Since tspec-generator's methodology section explicitly defers the transformation details to F-12 ("Reference: `skills/test-spec/rules/clark-transformation-rules.md` for operational rules"), the correctness of the Clark transformation in the final implementation depends entirely on F-12 being authored correctly — which this architecture provides no guidance for.

2. **Disambiguation of "1 Scenario per basic_flow step vs. 1 Scenario for the entire basic_flow."** The post-completion checks include `verify_one_scenario_per_basic_flow`, and the Clark mapping table shows `$.basic_flow[*]` -> "Happy path Scenario" with cardinality 1:1. An implementer could read "1:1" as "one scenario per flow step" rather than "one scenario for the entire flow comprising all steps." Clark's algorithm produces 1 happy path scenario from the entire basic flow (not one per step). The template (F-10) correctly shows a single Happy Path scenario. But if an implementer reads the Clark Mapping Table's "1:1" cardinality notation for `$.basic_flow[*]` as per-step, they will generate N scenarios instead of 1. The notation is potentially ambiguous under adversarial reading.

3. **`$.slice_state >= ANALYZED` guardrail missing.** Step 9 flagged this as a GATE-2 issue: "tspec-generator `$.slice_state >= ANALYZED` guardrail noted as /test-spec scope, not implemented here." The Step 10 deliverable does not implement this guardrail. `tspec-generator` could generate scenarios from a use case with `$.slice_state = SCOPED` (no slices prepared, no test cases defined), potentially generating feature files before the use case has been prepared for implementation. The architecture's pre-conditions table (Section 6) does not include `$.slice_state` as a validation condition. This is a functional gap carried forward from Step 9 without resolution.

### S-007 (Constitutional AI) — P-003/P-020/P-022 Compliance

**P-003 (No recursive subagents):** Both agents correctly exclude the Task tool from their `tools` arrays. Both `forbidden_actions` lists include explicit P-003 violations with NPT-009-complete format. The integration point table explicitly notes "MUST NOT invoke /worktracker via Task -- P-003." Full compliance.

**P-020 (User authority):** Status is PROPOSED. ORCHESTRATION.yaml reconciliation naming changes are documented as deviations from the preliminary plan, preserving user awareness. The agent split (2 vs. 1) is flagged as an architectural decision with the Phase 2 contingency cited. The tspec-analyst T1->T2 revision is transparently documented mid-section. Full compliance.

**P-022 (No deception):** The tspec-analyst tool tier analysis explicitly documents the initial T1 consideration and the correction to T2 with reasoning. RISK-15 (2-agent split may prove unnecessary) is openly disclosed. The F-12 gap is visible in the file manifest (listed but no content outline). No deceptive omissions detected. Full compliance.

**H-34 (Dual-file architecture):** Both agents have `.md` frontmatter (Claude Code official fields only) and `.governance.yaml` (recommended fields including version, tool_tier, identity, persona, capabilities, guardrails, output, constitution, validation, session_context, enforcement). Both agents have >= 3 `forbidden_actions` in NPT-009-complete format. Both declare P-003, P-020, P-022 in `constitution.principles_applied`. Full compliance.

**H-35 (Constitutional compliance per H-35/H-34 sub-item b):** Satisfied. Both agents have `forbidden_actions` with minimum 3 entries referencing constitutional triplet. Neither worker agent has `Task` in the `tools` array.

### S-002 (Devil's Advocate) — Challenging the Strongest Claims

**Challenge 1: "The 2-agent split is justified."**

The architecture's strongest claim is that the split satisfies the Phase 2 contingency condition. The contingency states: "If methodology section exceeds 1,500 tokens during Phase 3, split." The architecture estimates: Clark algorithm 1,200 tokens + 7 Cs framework 800 tokens + coverage gap analysis 600 tokens = 2,600 tokens total, exceeding 1,500.

Devil's Advocate: These are estimated token counts, not measured counts. The 1,200-token estimate for the Clark algorithm is plausible given 7 steps + lookup table. However, the 7 Cs quality framework is also documented in `clark-transformation-rules.md` (F-12) — so tspec-analyst's methodology could reference that rules file rather than embedding it, potentially keeping tspec-analyst under 1,500 tokens. The claim that both agents exceed 1,500 tokens is not independently verifiable from the architecture document. The other 3 criteria (cognitive modes, I/O profiles, invocation frequency) are stronger and stand on their own.

**Challenge 2: "Priority 14 places /test-spec safely below /use-case."**

The architecture states priority 14 is "one level below /use-case (priority 13)" and that keyword sets are disjoint. Review confirms the positive keyword sets are largely disjoint. However, the word "extension" appears in BOTH /use-case positive keywords (Step 9: "extension, extension handling") AND /test-spec's Clark transformation context — though "extension" alone is not in /test-spec's positive keyword list. This is not a collision risk but worth noting.

More substantively: /test-spec negative keywords include "unit test" and "pytest" but not "acceptance test" or "user story." A request like "write acceptance tests for this use case" could trigger /test-spec ("test specification" compound trigger) when the user might intend something else. The compound trigger "test specification" could match "acceptance test specifications."

**Challenge 3: "The coverage formula is correct."**

The formula `coverage = mapped_scenarios / total_mappable_flows` where `total_mappable_flows = 1 + count(alt_flows) + count(extensions)` treats each extension as generating exactly 1 scenario. Clark's algorithm (Step 5) produces exactly 1 scenario per extension. This is consistent. However, slice-scoped generation changes the denominator: if generating for a specific slice, `total_mappable_flows` should be computed against the flows in that slice, not the entire use case. The architecture acknowledges slice-scoped generation but does not address how coverage is computed for slice-scoped feature files. The tspec-analyst coverage report may report incorrect coverage percentages for slice-scoped feature files.

### S-004 (Pre-Mortem) — Downstream Failure Modes

**"It is 6 months later. The /test-spec skill was implemented but generates incorrect Gherkin for use cases with extensions that have outcome=rejoin:{N}."**

Root cause chain from this architecture: The `clark-transformation-rules.md` (F-12) was authored by eng-backend without a content skeleton. The implementer correctly mapped `outcome=failure` -> negative scenario and `outcome=success` -> alternate success scenario, but for `outcome=rejoin:{N}`, the Clark mapping is less intuitive (it generates "an additional scenario that merges to step N"). Without an explicit example in F-12 showing how `rejoin:{N}` produces a scenario whose `Then` clause references "rejoins at step N," the implementer treated rejoin outcomes as identical to success outcomes. The tspec-analyst catches this during coverage analysis (the scenario type is wrong) but only after feature files have been generated.

**Root cause: F-12 has no content specification in this architecture document.**

Mitigation available but not implemented: Section 4 (Template Design) provides complete skeletons for F-10 and F-11 with `**Source:** EXT-{STEP}{LETTER} (anchor_step: {N}, outcome: failure)` annotations. Adding an equivalent level of specification to F-12 would close this risk.

**"It is 6 months later. tspec-analyst is never invoked — nobody calls it."**

The architecture acknowledges this in RISK-15 (invocation rate < 20%) and provides a merge-back path. However, there is no actionable trigger in the SKILL.md routing table that would prompt automatic tspec-analyst invocation after tspec-generator completes. The routing table says "if the user says 'generate and check coverage', invoke tspec-generator first, then tspec-analyst" — this requires the user to explicitly request coverage analysis. A more proactive pattern would be for tspec-generator's `on_send` session context to recommend tspec-analyst invocation. The architecture includes `on_send` fields for tspec-generator that already list "Flag if coverage is incomplete" but do not recommend tspec-analyst by name.

### S-010 (Self-Refine) — Is the Scoring Itself Consistent?

Consistency check applied:

1. **Completeness scored 0.91.** Primary evidence: F-12 has no content outline. Supporting evidence: all other files have content specifications. This is a genuine gap in a C4 deliverable targeting 0.95. Score is consistent with the calibration anchor: 0.85 = "strong with minor refinements," 0.92 = "genuinely excellent." The F-12 gap is a real implementation risk, not cosmetic.

2. **Methodological Rigor scored 0.94.** The Clark algorithm implementation is correct and complete. The 7 Cs framework is properly operationalized. The two-layer validation gate mirrors Step 9 exactly. The slice-scoped coverage gap (coverage computation not defined for slice-scoped generation) is a real methodological gap that prevents a score above 0.94.

3. **Internal Consistency scored 0.93.** The T1-then-T2 tspec-analyst tool tier revision is transparent and the final specification is correct. However, a published architecture document with a retracted statement within the same section introduces reader confusion even if the final answer is correct. This is a minor but real consistency issue.

4. **Composite 0.930.** This is mathematically consistent with the dimension scores. The composite correctly reflects a deliverable that is very close to the threshold but has specific, identifiable gaps that are not merely cosmetic.

Leniency check: No dimension was scored above 0.95. The 0.95 assigned to Actionability is the highest score and is justified by the copy-paste-ready governance YAML, complete template skeletons, and exact ORCHESTRATION.yaml reconciliation table.

### S-012 (FMEA) — Failure Modes in the Architecture

| ID | Failure Mode | Effect | Severity | Likelihood | RPN | Mitigation Status |
|----|-------------|--------|----------|------------|-----|-------------------|
| FM-01 | F-12 authored without Clark rejoin:{N} example | tspec-generator produces wrong Gherkin for extensions with outcome=rejoin | HIGH | MEDIUM | HIGH | Not mitigated (no F-12 content specification) |
| FM-02 | "1:1 cardinality" misread as per-step for basic_flow | tspec-generator generates N happy path scenarios instead of 1 | MEDIUM | LOW | LOW | Partially mitigated by template F-10 showing single Happy Path section |
| FM-03 | $.slice_state guardrail absent | tspec-generator processes SCOPED use cases before preparation | MEDIUM | LOW | LOW | Not mitigated in this architecture |
| FM-04 | tspec-analyst never invoked by implementers | Coverage gaps go undetected in production | MEDIUM | MEDIUM | MEDIUM | Partially mitigated by RISK-15 merge-back path |
| FM-05 | Coverage formula incorrect for slice-scoped generation | tspec-analyst reports inflated coverage for partial feature files | LOW | LOW | LOW | Not addressed |
| FM-06 | clark-transformation-rules.md becomes context-budget violation | CB-05 violation if rules file > 500 lines | LOW | LOW | LOW | RISK-16 documents this risk with mitigation |

**FMEA verdict:** FM-01 has the highest RPN and is the primary gap for REVISE recommendation.

### S-011 (Chain-of-Verification) — Verifiable References

Verifying key cited references:

| Claim | Reference | Verifiable? | Finding |
|-------|-----------|-------------|---------|
| "Clark (2018) UC2.0-to-Gherkin mapping algorithm" | "S-03 (Clark mapping table)" | Partial | Clark is cited in agent-decomposition.md as the methodology source, but no full citation (journal/conference/book title) is provided in this document or any Phase 2 document visible in the codebase. The research phase (S-03) presumably captured the full citation, but it is not surfaced here. |
| Phase 2 documents "v1.1.0, 0.963 PASS" | agent-decomposition.md lineage | Verified | agent-decomposition.md v1.1.0 confirmed present. Quality scores are internal workflow metadata — not independently verifiable by external reviewer but consistent with the workflow record. |
| "SD-07: actor_action -> When, system_response -> Then, validation -> Then" | "PAT-008, SD-07" | Verified | file-organization.md SD-07 entry confirmed: "Clark mapping requires distinguishing actor actions (When) from system responses (Then)." |
| "SD-08: extension outcome determines scenario type" | "PAT-008, SD-08" | Verified | file-organization.md SD-08 entry confirmed: "Clark mapping: extensions with outcome=failure become negative test scenarios; extensions with outcome=rejoin become additional scenarios." |
| "7 Cs quality framework" attributed to "DI-06, PAT-004" | Internal research IDs | Not independently verifiable | DI-06 and PAT-004 are internal research document IDs from the Phase 1 synthesis. These are not resolvable without the research document index. However, the 7 Cs framework is consistently applied with enough specificity (C1-C7 named with assessment methods) that the unresolvable citation does not undermine the quality of the specification itself. |
| "scripts/extract-gherkin.sh" from file-organization.md | "file-organization.md line 286" | Verified | file-organization.md was read. The script reference is in the file-organization architecture document as an item in the `/test-spec` directory tree. |
| "AD-M-001 kebab-case pattern" for agent naming | agent-development-standards.md | Verified | agent-development-standards.md AD-M-001 confirmed: "Agent name SHOULD follow the {skill-prefix}-{function} kebab-case pattern." |

**Chain-of-Verification verdict:** Primary concern is Clark (2018) full citation absent. All structural and schema references verify correctly.

### S-001 (Red Team) — Attacking the Weakest Dimension

**Target: Completeness (0.91 -- lowest dimension score).**

Red Team attack: An implementer following this architecture would correctly create all 14 files. They would have complete guidance for F-01 through F-11, F-13, and F-14. However, for F-12 (`clark-transformation-rules.md`), they receive only:
- File manifest entry: "Clark (2018) mapping as agent rules"
- System prompt outline reference: "Reference: `skills/test-spec/rules/clark-transformation-rules.md` for operational rules"
- Risk Register entry: "Targets < 500 lines. The Clark mapping is a 7-step algorithm with a deterministic lookup table."

This is insufficient to implement F-12 correctly for the following reasons:

1. The 7 steps are documented in agent-decomposition.md (lines 236-246) and in Section 5 of this architecture, but they are documented as high-level methodology steps, not as agent-operational rules in the imperative format that rules files use.

2. The Clark Mapping Table (SD-07, SD-08) is documented in Section 5, but its representation as agent-rule imperatives (e.g., "WHEN basic_flow step has type=actor_action, GENERATE When clause using the step.action text") is not specified.

3. Compare to F-14 (BEHAVIOR_TESTS.md): Step 9 sets the template for behavior tests. Step 10's F-14 inherits the same pattern. But F-12 is the only file in the architecture with a dependency on correctly encoding a 3rd-party academic algorithm, and it gets the least specification of any file in the manifest.

**Red Team verdict:** F-12 is the most critical implementation risk in this architecture and the gap is not mitigated by any content outline, skeleton, or example rules. The red team attack is valid and aligns with S-004 Pre-Mortem FM-01 finding.

---

## Specific Gaps (REVISE)

The following gaps must be addressed before this architecture can achieve >= 0.95 and proceed.

### Gap 1 — HIGH Severity | Completeness + Actionability

**Gap:** `clark-transformation-rules.md` (F-12) has no content specification.

**Dimension impact:** Completeness (primary), Actionability (secondary)

**Evidence:** Section 2 (Agent Routing Table) says tspec-generator uses systematic cognitive mode applying Clark's algorithm, and "Reference: `skills/test-spec/rules/clark-transformation-rules.md` for operational rules." RISK-16 says it "targets < 500 lines" and contains "a 7-step algorithm with a deterministic lookup table." But the architecture provides no:
- Section structure (headings, organization)
- Imperative rule format (RULE-N: WHEN condition, DO action)
- Example rules showing the actor_action -> When clause mapping
- Example rules showing the extension outcome=rejoin:{N} -> scenario generation
- Expected rule count or coverage criteria

**Fix required:** Add a subsection in Section 4 (Template Design) or Section 5 (Shared Schema Integration) titled "F-12: clark-transformation-rules.md" providing:
- Content outline with section headings (Input Validation Rules, Clark Mapping Rules [7 entries], Step-Type-to-Clause Rules for SD-07, Outcome-Type-to-Scenario Rules for SD-08, Slice-Scoped Generation Rules)
- At least 2 example rules in the imperative format the agent will read (e.g., "RULE-C3-01: Basic flow mapped. When generating the happy path scenario, combine ALL basic_flow steps into a SINGLE Scenario. Do NOT generate one Scenario per step.")
- Explicit coverage criterion: "F-12 MUST cover all 7 Clark mapping steps, the SD-07 step type lookup table, and the SD-08 outcome type lookup table."

### Gap 2 — MEDIUM Severity | Completeness

**Gap:** `$.slice_state >= ANALYZED` input precondition not implemented.

**Dimension impact:** Completeness

**Evidence:** Step 9 architecture (GATE-2 Issue Resolution) documents: "tspec-generator `$.slice_state >= ANALYZED` guardrail -- noted as /test-spec scope, not implemented here." The Step 10 architecture does not implement this guardrail. Section 6 (Integration Pre-Conditions) lists 6 pre-conditions but does not include `$.slice_state` validation.

**Why this matters:** Per agent-decomposition.md's Progressive Realization Matrix, `tspec-generator` requires `STORY_DEFINED` minimum input. The `STORY_DEFINED` realization level is set by `uc-slicer` after completing Activities 2+4 (slice creation with test cases defined). However, `$.detail_level >= ESSENTIAL_OUTLINE` can be true at the `OUTLINED` realization level — a use case can have ESSENTIAL_OUTLINE detail without having any slices. If `tspec-generator` only checks `$.detail_level` and not `$.realization_level`, it can process use cases that have not been sliced and analyzed, generating feature files from use cases with no corresponding implementation stories.

**Fix required:** Add to Section 6 (Integration Pre-Conditions) table:
- Pre-Condition: `$.realization_level >= STORY_DEFINED` (optional but recommended for slice-aligned test generation)
- Or alternatively: explicitly document that `$.realization_level` check is deferred and explain why (e.g., "tspec-generator can operate on OUTLINED use cases; STORY_DEFINED check is recommended but not required because use case tests can be written before implementation slicing")

If the decision is NOT to require STORY_DEFINED, that decision must be explicitly justified here, because the Phase 2 architecture (agent-decomposition.md, line 396) states: "Reads: ... Requires STORY_DEFINED minimum input."

### Gap 3 — MEDIUM Severity | Methodological Rigor

**Gap:** Coverage computation formula not defined for slice-scoped generation.

**Dimension impact:** Methodological Rigor

**Evidence:** Section 7 (Quality Strategy) defines:
```
total_mappable_flows = 1 (basic_flow) + count($.alternative_flows) + count($.extensions)
```
This formula applies to whole-use-case generation. However, Section 2 (Integration Points) and Section 6 document slice-scoped generation where `tspec-generator` generates "a Feature file covering only the steps in `$.slices[N].steps_included[*]`."

For a slice-scoped feature file, the coverage denominator should be the flows included in that slice, not the full use case. If `tspec-analyst` uses the whole-use-case formula against a slice-scoped feature file, it will compute artificially low coverage (e.g., 20% instead of 100% for a feature file correctly covering a single basic-flow-only slice).

**Fix required:** Add a subsection to Section 7 (Quality Strategy) titled "Coverage Computation for Slice-Scoped Feature Files" defining:
- Modified formula: when feature file frontmatter has `slice_id != null`, denominator = count of flow elements whose steps are included in `$.slices[slice_id].steps_included`
- Guidance for tspec-analyst: check `slice_id` frontmatter field before selecting coverage formula
- Expected behavior: slice-scoped coverage 100% means all flows in that slice are mapped, not all flows in the use case

### Gap 4 — LOW Severity | Internal Consistency

**Gap:** tspec-analyst tool tier presented as T1, then corrected to T2 within the same section, with both versions of the frontmatter YAML remaining in the document.

**Dimension impact:** Internal Consistency

**Evidence:** Section 3.2 contains two separate YAML blocks for `tspec-analyst.md` official frontmatter. The first block (lines ~344-363 in the document) shows `tools: [Read, Glob, Grep, Bash]` and is followed by a paragraph explaining why T1 was initially considered and why T2 is actually required. The second YAML block (lines ~370-389) shows the corrected T2 frontmatter `tools: [Read, Write, Edit, Glob, Grep, Bash]`. The first block should be removed or clearly marked as a retracted draft — its presence in the published architecture creates implementer confusion about which YAML to use.

**Fix required:** Remove the first (T1) YAML block for tspec-analyst.md official frontmatter, or prefix it with `> RETRACTED: Initial T1 consideration, superseded by T2 specification below.` The reasoning paragraph explaining the T1->T2 decision is valuable and should be retained.

### Gap 5 — LOW Severity | Evidence Quality

**Gap:** "Clark (2018)" cited without full bibliographic reference.

**Dimension impact:** Evidence Quality

**Evidence:** Throughout the document, "Clark (2018)" is cited as the source of the UC2.0-to-Gherkin transformation algorithm. The agent-decomposition.md also cites "Clark (2018)" as "S-03 (Clark mapping table)" without a full citation. At C4 criticality, claims about a named academic methodology should have verifiable citations. The research phase presumably captured the full reference, but it does not appear in any Phase 2 or Phase 3 architecture document.

**Fix required:** Add at minimum the full citation to the L2 section or a References section: author, year, title, publication venue, URL if available. Example: "Clark, T. D. (2018). Automated Generation of Test Cases from Use Cases. [Conference/Journal]." If the full citation is available in the Phase 1 research documents, it should be surfaced here.

---

## Leniency Bias Check

- [x] Each dimension scored independently
- [x] Evidence documented for each score
- [x] Uncertain scores resolved downward (Completeness: 0.94 -> 0.91; Evidence Quality: 0.94 -> 0.92)
- [x] First-draft calibration considered (this is v1.0.0, first iteration)
- [x] No dimension scored above 0.95 without exceptional evidence (Actionability at 0.95 justified by copy-paste-ready governance YAML, complete template skeletons)
- [x] C4 threshold (0.95) correctly applied vs. standard 0.92 threshold

**Calibration anchor verification:**
- 0.85 = strong with minor refinements needed — Completeness at 0.91 reflects one specific missing content specification (F-12), not broad incompleteness. Score correctly above 0.85.
- 0.92 = genuinely excellent across the dimension — Methodological Rigor at 0.94 reflects genuinely excellent Clark transformation implementation with one specific gap (slice-scoped coverage formula). Score correctly above 0.92.
- 0.95 = exceptional (the C4 threshold set by user override C-008) — Only Actionability achieves 0.95, justified by the copy-paste-ready implementation artifacts.

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.930
threshold: 0.95
weakest_dimension: completeness
weakest_score: 0.91
critical_findings_count: 0
high_findings_count: 1
medium_findings_count: 2
low_findings_count: 2
iteration: 1
improvement_recommendations:
  - "Gap 1 (HIGH): Add F-12 clark-transformation-rules.md content specification with section outline, 2+ example imperative rules, and coverage criterion for the 7 Clark steps + SD-07 + SD-08 tables"
  - "Gap 2 (MEDIUM): Implement or explicitly defer $.realization_level >= STORY_DEFINED guardrail with documented rationale reconciling agent-decomposition.md line 396 requirement"
  - "Gap 3 (MEDIUM): Define coverage computation formula for slice-scoped feature files in Section 7 Quality Strategy"
  - "Gap 4 (LOW): Remove retracted T1 YAML block from tspec-analyst specification or mark clearly as superseded"
  - "Gap 5 (LOW): Add full bibliographic reference for Clark (2018) in L2 section or References section"
delta_to_threshold: -0.020
next_action: "Revise architecture document addressing Gaps 1-3 (HIGH+MEDIUM); Gaps 4-5 are LOW severity and may be addressed in the same pass"
```
