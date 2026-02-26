# Quality Score Report: GitHub Issue — Use Case Capability (Iteration 3)

## L0 Executive Summary

**Score:** 0.907/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.87)
**One-line assessment:** A substantially improved issue with all critical iteration 1/2 gaps addressed — INVEST language removed, chapter citations added, agent decomposition symmetric, AC-to-approach table complete, integration sequence resolving Jacobson-Cockburn tension — but the score is 0.907 against the C4 target of 0.95, held back by remaining evidence gaps (author-constructed synthesis unreferenced, file organization uncited, Gherkin ecosystem unspecified) and implicit rather than explicit capability-to-agent traceability.

## Scoring Context

- **Deliverable:** `/Users/anowak/workspace/github/jerry/.claude/worktrees/001-oss-release-gh-issues/work/gh-issues/issue-use-case-skill.md`
- **Deliverable Type:** GitHub Issue (Enhancement) for OSS release
- **Criticality Level:** C4 (public-facing, OSS release gate, irreversible once published)
- **Scoring Strategy:** S-014 (LLM-as-Judge) with 6-dimension weighted composite
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-02-26T00:00:00Z
- **Iteration:** 3 (prior scores: iteration 1 = 0.858, iteration 2 = strategy execution only; this is the first formal re-score after revisions)

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.907 |
| **Threshold** | 0.95 (C4 target) / 0.92 (H-13 minimum) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | Yes — iteration 2 S-004/S-012/S-001 findings applied by author |
| **Delta from Iteration 1** | +0.049 (0.858 → 0.907) |

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.90 | 0.180 | All three skills now symmetric; 17 ACs covering all requirements; trigger map and frontmatter schema added; strategic overview content requirements still underspecified |
| Internal Consistency | 0.20 | 0.93 | 0.186 | Quality scope separation resolves main iteration 1 gap; worktracker "can/must" language aligned; agent decomposition symmetric; minor gap between AC 5-exchange minimum and approach Step 9 narrative |
| Methodological Rigor | 0.20 | 0.93 | 0.186 | INVEST removed and replaced with Jacobson's criteria; chapter-level citations throughout; AsyncAPI grounded in use case constructs; integration sequence explicitly resolves Jacobson-Cockburn tension; six principles remain paraphrase but chapter-cited |
| Evidence Quality | 0.15 | 0.87 | 0.1305 | Major improvement: INVEST removed, chapter citations added for all key claims; methodology integration sequence is author-constructed synthesis without attribution; file organization entirely author-originated; Gherkin ecosystem unspecified |
| Actionability | 0.15 | 0.90 | 0.135 | Guided experience AC now testable (5-exchange minimum, completeness checker verification); shared frontmatter schema is named AC with design step; dependency graph dynamically generated (specified); Phase 3 gates make implementation path clear; no timeline signal |
| Traceability | 0.10 | 0.89 | 0.089 | AC-to-approach table maps all 17 ACs; chapter citations create traceable methodology claims; P-003 constraint explicit in all agent sections; capability-to-agent mapping remains implicit (inference required from agent names) |
| **TOTAL** | **1.00** | | **0.907** | |

## Detailed Dimension Analysis

### Completeness (0.90/1.00)

**Evidence:**

The three-skill structure is now symmetric. `/use-case` has 9 capabilities and 4 named agents (lines 143-151). `/test-spec` has 5 capabilities and 2 named provisional agents (lines 169-174). `/contract-design` has 6 capabilities and 2 named provisional agents (lines 196-201). All three skills include explicit P-003 compliance constraints. The 17 acceptance criteria (lines 266-283) cover: research deliverable, skill definitions, agent definitions, guided experience (with testable proxy), template support, slicing, individual file organization, dependency graph, index, strategic overview, TDD/BDD generation, contract generation, worktracker integration, cross-referencing, shared frontmatter schema, trigger map registration, and quality compliance. The AC-to-approach table (lines 286-304) maps all 17 ACs to phases and steps. The "What this does NOT include" section (lines 257-263) actively manages scope.

**Gaps:**

1. The strategic overview AC (line 275) states "A concise overview shows actor-goal mapping and implementation progress." The content requirements remain vague — "implementation progress" is not specified (percentages? status counts? slice lifecycle state distribution? a list of in-scope vs. completed use cases?). An implementer cannot verify this AC without knowing what the artifact must contain.

2. The trigger map registration AC (line 281) specifies that all three skills must be registered with "trigger keywords, negative keywords, and priority per the enhanced 5-column format" — but the issue does not provide candidate trigger keywords for any of the three skills. This is appropriate (the implementer should define them), but it means the AC is complete-on-structure while underspecified-on-content. This is a boundary judgment call: for a planning issue, leaving keywords to the implementer is reasonable; the AC verifies that registration happens.

3. The research AC (line 266) requires "at least 3 additional industry sources" beyond Jacobson and Cockburn, but does not specify any candidate categories (e.g., model-driven development, domain-specific modeling, requirements management tooling). An implementer has full latitude here — which is intentional — but means the AC could be satisfied with three sources of varying relevance.

**Improvement Path:**

Define minimum content requirements for the strategic overview artifact: e.g., "actor-goal table listing all actors and their primary use cases," "use case status counts by lifecycle state (Scoped/Prepared/Analyzed/Implemented/Verified)," and "slice completion rate." This gives the index agent implementer a verifiable target.

---

### Internal Consistency (0.93/1.00)

**Evidence:**

The primary consistency gap from iteration 1 — ambiguity between quality enforcement for implementation deliverables vs. skill-produced artifacts — is explicitly resolved at line 244: "(a) *Implementation deliverables* (SKILL.md files, agent definitions, templates) are subject to Jerry's quality gate (>= 0.92 for C2+)... (b) *Use case artifacts produced by the skill* (individual use cases, slices, test specs, contracts) should have quality validation workflows built into the skill." This is unambiguous. The worktracker integration language is now consistently MUST (line 238: "File structure MUST work with `/worktracker` entity hierarchy"; line 242: "Use cases and slices MUST integrate with the worktracker entity hierarchy"). The agent decomposition is symmetric across all three skills. The AC-to-approach table maps consistently — no AC is unmapped and no approach step produces no AC.

The pipeline narrative ("understand what the system does → define how to verify it → specify how to build it") at line 50 is consistent with the Phase 3 skill-by-skill sequencing (steps 9 → 10 → 11 with gates).

**Gaps:**

1. The "Guided experience" AC at line 269 specifies "minimum 5 exchanges" as the verifiable proxy. The approach section at Step 9 (line 326) says "Implement `/use-case` skill — SKILL.md, agent definitions, templates, guided workflow" and the gate says "verify that the `/use-case` skill produces a complete use case artifact." The 5-exchange minimum does not appear in the approach step — an implementer reading Step 9 would not know to measure the exchange count. This is a minor consistency gap between the AC specification and the approach description.

2. Line 48 states "Each skill stands alone." But the Phase 3 gates (steps 9-11) establish that `/test-spec` must be built against the "validated `/use-case` output format from step 9" and `/contract-design` similarly. The gate language implies a dependency that is slightly in tension with "each skill stands alone." The intent (implementation dependency, not runtime dependency) is discernible from context but not explicitly stated.

**Improvement Path:**

In Step 9 (approach), add a parenthetical or note: "(Verify the guided workflow achieves a complete creation through a minimum 5-exchange prompt sequence before proceeding.)" This aligns the approach step with the AC without adding significant content. Add a clarifying note near "each skill stands alone": "Each skill is independently usable at runtime; implementation order follows the pipeline for dependency reasons."

---

### Methodological Rigor (0.93/1.00)

**Evidence:**

The INVEST language has been completely removed and replaced with Jacobson's own criteria: "independently implementable, independently testable, and delivering demonstrable value to a stakeholder" (line 128), echoed at line 271 and in the synthesis table at line 102 ("Slice quality: independently implementable, testable, valuable (per Jacobson Ch. 5)"). The AsyncAPI inclusion is now grounded in use case constructs (line 186): "For asynchronous communication patterns identified in use case scenarios — such as event-triggered extensions, background processing steps, and notification flows described in alternative paths." This explicitly connects AsyncAPI to Cockburn's extension scenario structure. The methodology integration sequence (lines 106-116) is substantively rigorous — it defines exactly when slicing (Jacobson) occurs relative to precision levels (Cockburn), and the rationale at line 116 explicitly names the tension being resolved ("between Cockburn's breadth-first progressive refinement and Jacobson's vertical slicing"). Chapter-level citations are present throughout: Jacobson Ch. 2, 3, 4, 5; Cockburn Ch. 1, 3, 4, 5, 6-7, 10, Appendix A.

**Gaps:**

1. The six first principles are characterized as: "(1) Keep it simple by telling stories, (2) Understand the big picture, (3) Focus on value, (4) Build the system in slices, (5) Deliver the system in increments, (6) Adapt to meet the team's needs." These are cited to "Jacobson, Ch. 2" which is sufficient for verification — but these are paraphrases of Jacobson's exact formulations. An implementer checking the source will find similar but not identical language. This is a minor methodological precision gap; the chapter citation allows resolution.

2. The methodology integration sequence (lines 106-116) is the author's synthesis — a recommended ordering not cited to either Jacobson or Cockburn. The sequence is logically sound (Level 2 outline before slicing; Level 3 detail on per-slice basis), but its attribution is unclear. A reader cannot verify whether this sequence is standard practice or the issue author's construction. The word "Recommended" signals it is not canonical, but no source is provided.

3. The "system context" note for `/contract-design` (lines 192-194) — "Contract generation from use case text alone may produce incomplete specifications... for brownfield systems with existing API conventions" — is methodologically sound reasoning but ungrounded in any source. This is author reasoning; appropriate for an issue document but lower evidence quality than the Jacobson/Cockburn-grounded sections.

**Improvement Path:**

For the integration sequence, add: "(Synthesized from both sources; no single source prescribes this exact ordering.)" This transparency converts an unattributed claim into an acknowledged synthesis, which is more methodologically honest. For the six principles, a brief note that these are paraphrased (not quoted verbatim) would prevent implementer confusion when consulting the source.

---

### Evidence Quality (0.87/1.00)

**Evidence:**

The chapter-level citations are a substantial improvement. Key Jacobson claims now trace to specific chapters: six first principles (Ch. 2), seven activities (Ch. 3), slice lifecycle states (Ch. 4), slicing patterns and slice quality criteria (Ch. 5). Key Cockburn claims trace to: template spectrum (Ch. 1, Appendix A), goal hierarchy (Ch. 4), precision levels (Ch. 5), actor classification (Ch. 3), scenario structure (Ch. 6-7), completeness heuristics (Ch. 10). The INVEST claim — the most significant unsupported assertion in iteration 1 — is entirely removed. The research AC (line 266) now requires "specific findings that influenced design decisions — not just source enumeration." The synthesis table at lines 96-103 correctly maps both pillars to orthogonal concerns, a characterization consistent with the source material.

**Gaps:**

1. The methodology integration sequence (lines 106-116) is author-constructed synthesis without attribution. The sequence is logically derivable from the source material, but the specific five-step ordering (Discover → Outline → Slice → Detail → Verify) is not present as a unified sequence in either Jacobson or Cockburn. As a synthesis, it should be labeled as such — e.g., "(Author synthesis from Jacobson Ch. 3-5 and Cockburn Ch. 5-7; not a direct quote from either source.)"

2. The file organization structure (lines 208-230) is entirely author-originated. No external source is cited for the recommended directory layout. This is appropriate for a planning document where the author explicitly says it's "a recommended starting point" (line 261), but it means the architecture section carries no external validation weight.

3. The Gherkin ecosystem remains unspecified. Line 162 says "Gherkin-formatted Given/When/Then specifications" without naming a target framework (Cucumber, Behave, SpecFlow, pytest-bdd, etc.). For an OSS-focused skill, this matters — different frameworks have different step-definition conventions and expect different file structures. This is a modest gap; it is appropriate to leave it to the implementer, but the AC (line 276) for TDD/BDD generation does not acknowledge the ecosystem ambiguity.

4. The "system context" reasoning for `/contract-design` (lines 192-194) is author reasoning, not sourced. API stub generation with TODO markers is reasonable practice, but no source is cited for this approach. This is a low-stakes gap for a planning document.

**Improvement Path:**

Label the methodology integration sequence explicitly as an author synthesis (one line addition). Add a note in the TDD/BDD AC acknowledging that framework-specific Gherkin conventions are left to the implementer based on the target ecosystem. These are low-cost additions that improve evidence transparency without requiring additional research.

---

### Actionability (0.90/1.00)

**Evidence:**

The "guided experience" AC is now testable: "structured prompt sequence (minimum 5 exchanges)" with "Verification: the skill completes a full creation workflow for a simple use case (single actor, single goal, 1-2 extensions) and produces an artifact that passes the completeness checker against Cockburn's heuristics" (line 269). This is a concrete, verifiable proxy. The shared frontmatter schema is a named AC (line 280) with a dedicated design step (Step 7, line 321) that specifies its content: "The schema defines required fields (ID, type, status, actor, goal-level, cross-references) and how they map to `/worktracker` entity metadata." The dependency graph is specified as "dynamically generated by the index agent reading use case frontmatter — not a static file that goes stale" (line 273). Phase 3 has three explicit gates (lines 326-328) with verifiable conditions before proceeding to the next skill. The AC-to-approach table maps all 17 ACs to phases and steps, giving an implementer a complete work order. The "What this does NOT include" section (lines 257-263) actively reduces scope ambiguity.

**Gaps:**

1. No timeline signal or milestone relationship. The "Why now" section (lines 337-344) establishes OSS prep context but provides no milestone date, blocking relationship to the release, or priority relative to other OSS prep issues. An implementer cannot determine the schedule urgency or plan their effort allocation.

2. Step 13 (end-to-end verification, line 333) says "create a sample use case" without specifying whether a sample fixture will be provided (a pre-written use case that the implementer runs through all three skills) or created from scratch during verification. Creating from scratch may yield a too-simple fixture. A pre-written fixture would be more rigorous but is out of scope for the issue itself.

3. The "strategic overview" AC (line 275) remains weakly specified for actionability — "actor-goal mapping and implementation progress" without content requirements. The index agent implementer cannot verify this AC precisely.

4. The approach treats the four phases as sequential with no guidance on iteration within phases. Step 8 (design agent decomposition) might surface insights requiring revision of step 6 or 7 (file organization and frontmatter schema). The issue says nothing about how to handle design decisions that require backtracking.

**Improvement Path:**

For the timeline gap: add one sentence under "Why now" — e.g., "This issue is a blocking dependency for the OSS launch; implementation should begin before [milestone]." For the strategic overview: specify three minimum content elements (e.g., actor-goal table, use case status summary, slice completion rate). These are bounded additions.

---

### Traceability (0.89/1.00)

**Evidence:**

The AC-to-approach table (lines 286-304) maps all 17 acceptance criteria to phases and key steps. This is the primary gap resolved from iteration 1. Chapter-level citations throughout the methodology section (lines 73-90) make each methodological claim traceable to a specific chapter in the source. P-003 compliance is explicitly stated in the agent sections for all three skills (lines 151, 174, 201). The navigation table (lines 3-22) includes all major document sections with anchor links. The methodology integration sequence (lines 106-116) explicitly traces which Cockburn level and which Jacobson activity applies at each integration step. The design principles section (lines 233-238) explicitly references the file structure compatibility requirement against the worktracker hierarchy, with a pointer to the entity hierarchy file.

**Gaps:**

1. Capability-to-agent mapping remains implicit. For `/use-case`, the four agents (author, slicer, reviewer, index) imply ownership of specific capabilities by name, but the mapping is not explicit: which capabilities does the "Use case author agent" own? Presumably capabilities 1-3 and 7 (guided creation, template support, slicing, goal-level management)? And the "Use case index agent" owns capabilities 5-6 and 9 (index, strategic overview, cross-referencing)? And the "Use case reviewer agent" owns capability 8 (completeness checking)? A simple table would resolve this. For `/test-spec` and `/contract-design`, the agent names ("Test plan generator agent", "Contract generator agent") are sufficiently self-describing to imply capability ownership, but the mapping is still implicit.

2. The methodology-to-capability tracing remains implicit. Cockburn Ch. 10 completeness heuristics → "Completeness checking" capability (line 138): inferable but not stated. Jacobson Ch. 5 slicing patterns → "Use case slicing" capability (line 128): implied by the text sequence but not explicitly cross-referenced. The chapter citations help, but the connection chain from "Cockburn says X" to "the skill implements X as capability Y" is not drawn.

3. The shared frontmatter schema content requirements (Step 7, line 321) list "ID, type, status, actor, goal-level, cross-references" but the AC for frontmatter schema (line 280) does not enumerate these same fields. An implementer could satisfy the AC with a schema that differs from the Step 7 description. A forward reference from the AC to Step 7 would make this traceable.

**Improvement Path:**

Add a capability-to-agent table for `/use-case` (6 rows: agent name → capability numbers owned). This is compact and high-value for traceability. For the shared frontmatter schema, add a forward reference in the AC to Step 7's field list, or repeat the minimum fields in the AC itself.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.87 | 0.93 | Label the methodology integration sequence as author synthesis (one line: "Synthesized from Jacobson Ch. 3-5 and Cockburn Ch. 5-7; not a direct quote from either source"). Acknowledge in TDD/BDD AC that Gherkin framework conventions are ecosystem-specific and left to implementer. |
| 2 | Traceability | 0.89 | 0.94 | Add a capability-to-agent table for `/use-case` (4-agent × 9-capability mapping). Add forward reference from shared frontmatter schema AC to Step 7 field enumeration. |
| 3 | Completeness | 0.90 | 0.94 | Define minimum content requirements for strategic overview artifact: e.g., actor-goal table, use case status counts by lifecycle state, slice completion rate. |
| 4 | Actionability | 0.90 | 0.94 | Add one sentence in "Why now" linking to OSS milestone. Define strategic overview content requirements (overlaps with priority 3). Clarify "each skill stands alone" means runtime independence, not implementation order independence. |
| 5 | Internal Consistency | 0.93 | 0.96 | Add 5-exchange minimum verification note in Step 9 of the approach. Clarify the "each skill stands alone" vs. Phase 3 implementation dependency tension. |
| 6 | Methodological Rigor | 0.93 | 0.96 | Label six first principles as paraphrase in parenthetical. Label integration sequence as author synthesis. These are transparency improvements, not methodology corrections. |

---

## Score Calibration Against Rubric

Applying the rubric calibration anchors:

- **0.92 = Genuinely excellent across the dimension** — Methodological Rigor and Internal Consistency are at or near this level with the chapter citations and integration sequence.
- **0.85 = Strong work with minor refinements needed** — Evidence Quality at 0.87 is here: strong with the INVEST removal and chapter citations, but the unreferenced synthesis and Gherkin gap keep it below 0.90.
- **0.92 composite = genuinely excellent** — The 0.907 composite is below this. This is accurate: the deliverable is strong but the remaining gaps (especially the evidence quality and traceability gaps) are real, not impressionistic.

The document has improved from 0.858 to 0.907 (+0.049). The improvement is genuine and substantial. The remaining gap to 0.95 (C4 target) is 0.043 — achievable with the targeted recommendations in this report, most of which are low-effort additions (one-line labels, a small table, a sentence in approach step 9).

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing the composite
- [x] Evidence documented for each score with line-level references
- [x] Uncertain scores resolved downward: Evidence Quality at 0.87 not bumped to 0.90 despite INVEST removal; Traceability at 0.89 not bumped to 0.92 despite AC-to-approach table addition
- [x] Calibration against anchors: 0.90+ scores require evidence of genuinely excellent work in that dimension — Internal Consistency and Methodological Rigor at 0.93 reflect genuinely resolved gaps, not grade inflation
- [x] No dimension scored above 0.95 without exceptional evidence (none are)
- [x] Delta validation: +0.049 from iteration 1 is consistent with the number and significance of revisions applied — major changes to Evidence Quality (+0.15) and Traceability (+0.13) drive most of the improvement, with smaller gains in Completeness (+0.05), Internal Consistency (+0.05), Methodological Rigor (+0.03), Actionability (+0.05)

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.907
threshold: 0.95  # C4 target; 0.92 H-13 minimum
weakest_dimension: Evidence Quality
weakest_score: 0.87
critical_findings_count: 0  # No single finding blocks acceptance; all are targeted refinements
iteration: 3
improvement_recommendations:
  - "Label methodology integration sequence as author synthesis, not sourced claim (Evidence Quality)"
  - "Acknowledge Gherkin framework ecosystem is left to implementer in TDD/BDD AC (Evidence Quality)"
  - "Add capability-to-agent table for /use-case (4 agents x 9 capabilities) (Traceability)"
  - "Add forward reference from shared frontmatter schema AC to Step 7 field list (Traceability)"
  - "Define minimum content requirements for strategic overview artifact (Completeness + Actionability)"
  - "Add 5-exchange minimum note to Step 9 approach description (Internal Consistency)"
  - "Clarify 'each skill stands alone' = runtime independence, not implementation order (Internal Consistency)"
  - "Add one sentence in Why Now linking to OSS milestone or blocking dependency (Actionability)"
delta_from_prior: +0.049  # 0.858 -> 0.907
delta_by_dimension:
  completeness: +0.05  # 0.85 -> 0.90
  internal_consistency: +0.05  # 0.88 -> 0.93
  methodological_rigor: +0.03  # 0.90 -> 0.93
  evidence_quality: +0.15  # 0.72 -> 0.87
  actionability: +0.05  # 0.85 -> 0.90
  traceability: +0.13  # 0.76 -> 0.89
path_to_pass:
  remaining_gap: 0.043  # 0.907 -> 0.95
  feasibility: HIGH  # All remaining recommendations are low-effort additions
  estimated_iterations: 1  # Iteration 4 should reach >= 0.95 with targeted additions
```
