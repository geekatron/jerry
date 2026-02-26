# Quality Score Report: GitHub Issue — Use Case Capability (Iteration 4)

## L0 Executive Summary

**Score:** 0.906/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.89)
**One-line assessment:** The deliverable is substantially stronger after iteration 4 but falls short of the C4 threshold (0.95) due to a persistent Gherkin/BDD internal inconsistency, incomplete methodology cross-references in Skills 2 and 3, and residual traceability gaps for the non-core skills; targeted single-pass fixes to these three areas are the remaining path to PASS.

---

## Scoring Context

- **Deliverable:** `/Users/anowak/workspace/github/jerry/.claude/worktrees/001-oss-release-gh-issues/work/gh-issues/issue-use-case-skill.md`
- **Deliverable Type:** Design (GitHub Issue for 3-skill capability)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **C4 Threshold:** 0.95 (not 0.92 — C4 requires higher bar)
- **Iteration:** 4 (prior scores: 0.858 → 0.907)
- **Scored:** 2026-02-26T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.906 |
| **C4 Threshold** | 0.95 |
| **Standard Threshold (C2+)** | 0.92 |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (standalone scoring) |
| **Delta from Iteration 3** | -0.001 (0.907 → 0.906) |

**Iteration trajectory note:** The scoring delta is effectively flat from iteration 3 to 4 (−0.001, within rounding). The iteration 4 revisions addressed real gaps but the Gherkin/BDD inconsistency introduced in the document — or left unresolved — is actively suppressing Internal Consistency and Evidence Quality. The gains and the loss roughly cancel.

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.91 | 0.182 | All 17 ACs present with chapter references and trigger keywords; "Gherkin" in Skill 2 agents section is an unresolved incompleteness in the BDD specification |
| Internal Consistency | 0.20 | 0.90 | 0.180 | Direct contradiction: Skill 2 agents section says "BDD/Gherkin specifications" (line 185) while Skill 2 capabilities (line 175) and TDD/BDD AC say "Given/When/Then format" with "specific BDD framework is an implementation decision" |
| Methodological Rigor | 0.20 | 0.92 | 0.184 | Research-first, gated phases, author-synthesis disclaimer, P-003 topology — strong; minor gap in schema validation approach |
| Evidence Quality | 0.15 | 0.89 | 0.1335 | Skill 1 has chapter-level citations in capabilities; Skills 2 and 3 capabilities lack methodology cross-references; Gherkin in agents section contradicts BDD framework evidence in capabilities |
| Actionability | 0.15 | 0.91 | 0.1365 | 14-step phased approach with gates, sample use case minimum requirements, 5-exchange minimum; Gherkin inconsistency creates implementer ambiguity on BDD framework decision |
| Traceability | 0.10 | 0.90 | 0.090 | Full AC-to-approach table (17 rows) and capability-to-agent mapping (9 rows); Skill 2 and Skill 3 capabilities lack Cockburn/Jacobson chapter references; trigger keyword rationale untraced |
| **TOTAL** | **1.00** | | **0.906** | |

---

## Detailed Dimension Analysis

### Completeness (0.91/1.00)

**Evidence:**
The issue covers all required elements for a C4 planning document: vision narrative, dual-pillar methodology with chapter-level citations, 3 skills with full capability lists, capability-to-agent mapping table (9 rows, complete), file structure, 7 Jerry integration requirements, 5 explicit exclusions, 17 ACs with checkboxes, AC-to-approach traceability table (17 rows), 4-phase approach with 14 named steps and inter-step gates, and "why now" rationale. The iteration 4 additions (trigger map keywords, strategic overview specification, Step 9 5-exchange minimum, sample use case minimum requirements, capability-to-chapter cross-references in Skill 1) are all present and correct.

**Gaps:**
1. The Skill 2 agents section (line 185) still contains "BDD/**Gherkin** specifications" — a holdover from pre-iteration-4 text that was not updated when the BDD framework clarification was applied to the capabilities section and AC. This leaves the BDD framework specification incomplete (the AC says implementation decision; the agents section says Gherkin).
2. The trigger map AC specifies suggested keywords for all 3 skills but explicitly defers "negative keywords and priority" to implementation. For a C4 issue, this is the appropriate scoping, but it means the trigger map registration AC is partially specified.

**Improvement Path:**
Fix line 185: change "TDD plans and BDD/Gherkin specifications" to "TDD plans and BDD specifications (in Given/When/Then format; specific framework is an implementation decision)." This single line fix resolves the incompleteness and brings Completeness to ~0.94.

---

### Internal Consistency (0.90/1.00)

**Evidence of inconsistency:**
The document makes two contradictory claims about the BDD framework in Skill 2:

- **Line 175 (Skill 2, Capability 2):** "generates BDD specifications using Given/When/Then format. The specific BDD framework (Cucumber/Gherkin, Behave, or framework-agnostic plain text) is an **implementation decision** for the research phase."
- **Line 185 (Skill 2, Agents section):** "Test plan generator agent — Converts use case scenarios into TDD plans and BDD/**Gherkin** specifications"

The AC (line 290) correctly says: "BDD scenarios (in Given/When/Then format; specific BDD framework is an implementation decision)." The agents section contradicts both the capability description and the AC by asserting Gherkin specifically.

**Other consistency checks (passing):**
- Strategic overview content specified identically in capability #6 and in the AC (3-part: actor-goal matrix, domain coverage, slice status counts) — consistent.
- Step 9 "minimum 5 exchanges" consistent with AC minimum.
- Step 13 sample reuse from Step 9 consistent with Step 9 text.
- Capability-to-agent mapping consistent with agents listed.
- P-003 constraint stated for Skill 1 and referenced ("same P-003 constraint applies") for Skills 2 and 3 — consistent.

**Improvement Path:**
Fix line 185 as noted above. This single change restores internal consistency to ~0.96.

---

### Methodological Rigor (0.92/1.00)

**Evidence:**
- Research-first sequence (Phase 1: 5 research steps before Phase 2 design before Phase 3 implementation)
- Explicit gates between Steps 9→10→11 with stated gate criteria
- Author-synthesis disclaimer for the methodology integration sequence is present and well-phrased: "synthesis by the issue author, not a prescription from either source... the implementer may adjust based on research findings"
- Epistemic honesty on BDD framework in the capabilities section
- P-003 compliance topology stated and enforced
- Quality criticality explicitly classified (C3+ for implementation deliverables, user-determined for skill-produced artifacts)
- "What this does NOT include" section with 5 explicit exclusions prevents scope creep
- Design principles distinguished from recommended file structure ("design principles are the constraints; the specific directory layout is not")

**Gaps:**
- Step 7 calls for designing the shared frontmatter schema but does not specify a validation approach (JSON Schema validation? Jerry AST validation per H-33?). This is a methodological gap — the issue creates a deliverable (the frontmatter schema) without specifying how it will be validated as part of the methodology.
- No conflict resolution mechanism specified for cases where Jacobson and Cockburn guidance conflicts beyond the integration sequence (which only covers sequencing, not content conflicts).

**Improvement Path:**
Add to Step 7: "The shared frontmatter schema should be defined as a JSON Schema file (for programmatic validation) and validated via `jerry ast validate` per H-33." This closes the schema validation gap and brings Methodological Rigor to ~0.95.

---

### Evidence Quality (0.89/1.00)

**Evidence present:**
- Jacobson citations: Ch. 2 (six principles), Ch. 3 (seven activities), Ch. 4 (slice lifecycle), Ch. 5 (slicing patterns + quality criteria)
- Cockburn citations: Ch. 1 (template spectrum), Ch. 3 (actor classification), Ch. 4 (goal-level hierarchy), Ch. 5 (precision levels), Ch. 6-7 (scenario structure), Ch. 10 (completeness heuristics)
- Iteration 4 added capability-to-chapter cross-references in Skill 1: "(Cockburn Ch. 5 for guided creation, Ch. 4 for goal-level management, Ch. 10 for completeness checking)"
- Full bibliographic references for both sources
- Author-synthesis disclaimer prevents false attribution

**Gaps:**
1. **Skill 2 capabilities lack methodology references.** Capability 1 (TDD plan generation) cites no Jacobson chapter for postcondition mapping. Capability 2 (BDD generation) has no Cockburn chapter citation for scenario-to-test mapping. Capability 5 (test slice alignment) cites Jacobson implicitly but no chapter reference.
2. **Skill 3 capabilities lack methodology references.** All 6 capabilities assert design choices without chapter citations.
3. **Agents section contradiction:** Line 185 says "BDD/Gherkin" — this contradicts the capability section evidence on line 175 that frames framework as an implementation decision. The agents section is the only place in the document where a specific BDD framework is asserted definitively.
4. The trigger map suggested keywords (line 295) lack rationale tracing to what methodology concepts drove those specific keyword choices.

**Improvement Path:**
Fix the Gherkin line (immediate, high impact). Add Cockburn/Jacobson chapter references to at least the primary capabilities of Skills 2 and 3 (e.g., for TDD plan generation: "per Jacobson's slice testing activity, Ch. 3"). This brings Evidence Quality to ~0.93.

---

### Actionability (0.91/1.00)

**Evidence:**
- 14 steps with clear phase sequencing
- Gates: "verify that the `/use-case` skill produces a complete use case artifact with frontmatter cross-references before proceeding" (Step 9), "verify that `/test-spec` can consume a `/use-case` artifact and produce test specifications with bidirectional traceability" (Step 10), "verify contract artifacts trace to use case interactions" (Step 11)
- Step 13 specifies sample use case minimum requirements: "sea-level use case with a primary actor, 2+ extensions, and a supporting actor"
- Step 9 references "minimum 5 exchanges per the Guided Experience AC"
- Step 13 notes sample reuse: "using the sample use case created in Step 9"
- Strategic overview specified as 3-part dashboard in both capabilities and AC
- Frontmatter schema fields named in Step 7: "ID, type, status, actor, goal-level, cross-references"
- Trigger map keywords suggested for all 3 skills

**Gaps:**
1. The Gherkin/BDD inconsistency in line 185 creates direct implementer confusion: if the agents section is the guidance for what the agent does, and it says "Gherkin," the implementer may implement Gherkin despite the capability description and AC saying "implementation decision." This is a genuine actionability ambiguity.
2. The TDD/BDD AC uses "and/or" in the contract generation AC: "generates OpenAPI/Swagger, CloudEvents, **and/or** JSON Schema" — slightly ambiguous about minimum required scope for compliance.
3. Step 7 lacks specification of how to validate the frontmatter schema (see Methodological Rigor).

**Improvement Path:**
Fix line 185 (highest impact). Clarify the contract generation AC to specify at minimum one of the three contract types must be implemented (or all three if that is the intent). Score would reach ~0.94.

---

### Traceability (0.90/1.00)

**Evidence:**
- AC-to-approach traceability table: 17 rows, every AC mapped to a producing phase and key steps. Complete.
- Capability-to-agent mapping: 9 rows, all capabilities from the capability list accounted for.
- Capability-to-chapter cross-references: 3 references in Skill 1 capabilities (Cockburn Ch. 5, Ch. 4, Ch. 10).
- Jerry integration references: specific rule files named (H-25, H-26, H-34, H-35, WTI-001-009, quality-enforcement.md).
- Methodology integration sequence traces each step to the originating pillar and precision level.

**Gaps:**
1. **Skills 2 and 3 capability traceability is absent.** All 5 Skill 2 capabilities and all 6 Skill 3 capabilities lack Cockburn/Jacobson chapter-level references. Skill 1 sets the bar at 0.92+ for this dimension; Skills 2 and 3 are at 0 for methodology traceability in their capabilities.
2. The trigger map suggested keywords (line 295) are not traced to why those keywords were selected (which methodology concepts they capture).
3. The "Why now" section's gap analysis ("What's missing is the front end of the pipeline") is not traced to a specific project document or planning artifact — it reads as editorial rather than traceable.

**Improvement Path:**
Add at least one chapter-level reference per skill for Skills 2 and 3 primary capabilities. The traceability table and mapping table already exist and are complete. Adding references for Skills 2 and 3 brings Traceability to ~0.93.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.90 | 0.96 | Fix line 185: change "BDD/Gherkin specifications" to "BDD specifications (in Given/When/Then format; specific framework is an implementation decision)" — one line change, eliminates the only genuine contradiction in the document |
| 2 | Evidence Quality | 0.89 | 0.93 | Add chapter-level Cockburn/Jacobson references to Skill 2 primary capability (TDD plan: Jacobson Ch. 3 testing activity; BDD: Cockburn scenario structure Ch. 6-7) and Skill 3 primary capability (API contract: trace to Jacobson's use case interaction concept) |
| 3 | Traceability | 0.90 | 0.93 | Same change as Priority 2 — chapter references in Skills 2 and 3 capabilities simultaneously resolve both Evidence Quality and Traceability gaps |
| 4 | Methodological Rigor | 0.92 | 0.95 | Add to Step 7: specify the frontmatter schema validation approach — "defined as a JSON Schema file validated via `jerry ast validate` per H-33" |
| 5 | Actionability | 0.91 | 0.94 | After fixing line 185, consider clarifying "and/or" in contract generation AC to specify minimum scope; low priority compared to items 1-4 |
| 6 | Completeness | 0.91 | 0.94 | Fixed by Priority 1 (line 185 fix); no separate action needed beyond items above |

---

## Score Projection

If all Priority 1-4 recommendations are applied:

| Dimension | Current | Projected | Delta |
|-----------|---------|-----------|-------|
| Completeness | 0.91 | 0.94 | +0.03 |
| Internal Consistency | 0.90 | 0.96 | +0.06 |
| Methodological Rigor | 0.92 | 0.95 | +0.03 |
| Evidence Quality | 0.89 | 0.93 | +0.04 |
| Actionability | 0.91 | 0.94 | +0.03 |
| Traceability | 0.90 | 0.93 | +0.03 |

Projected composite:
- (0.94 × 0.20) + (0.96 × 0.20) + (0.95 × 0.20) + (0.93 × 0.15) + (0.94 × 0.15) + (0.93 × 0.10)
- = 0.188 + 0.192 + 0.190 + 0.1395 + 0.141 + 0.093
- = **0.944**

The projected composite (0.944) still falls short of the C4 threshold (0.95). This means iteration 5 would also require scoring to confirm passage. The primary constraint is that no dimension is projected above 0.96, and the C4 threshold demands excellence across all dimensions simultaneously.

**What would reach 0.95:**
Every dimension at 0.95 produces: (0.95 × 1.00) = 0.95 exactly. The current weakest dimensions (Evidence Quality and Internal Consistency) need to reach 0.95 minimum. Evidence Quality reaching 0.95 requires comprehensive chapter references in all three skills, not just Skills 2 and 3. Internal Consistency at 0.95+ requires zero contradictions after the Gherkin fix. Methodological Rigor at 0.95 requires the schema validation specification.

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score — specific line references provided
- [x] Uncertain scores resolved downward (Internal Consistency: chose 0.90 not 0.91 due to the concrete Gherkin contradiction)
- [x] C4 calibration applied — 0.906 is significantly below 0.95; this is appropriate given remaining gaps
- [x] No dimension scored above 0.95 (highest is 0.92 for Methodological Rigor, which has documented gaps)
- [x] Delta from iteration 3 is essentially flat (0.907 → 0.906) — consistent with the analysis showing gains in some areas cancelled by the unresolved Gherkin inconsistency
- [x] Score projection explicitly shows iteration 5 would STILL be below 0.95 — anti-leniency applied to projection

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.906
threshold: 0.95
weakest_dimension: Evidence Quality
weakest_score: 0.89
critical_findings_count: 1
iteration: 4
improvement_recommendations:
  - "Fix line 185: change 'BDD/Gherkin specifications' to 'BDD specifications (in Given/When/Then format; specific framework is an implementation decision)'"
  - "Add Cockburn/Jacobson chapter references to Skill 2 primary capabilities (TDD: Jacobson Ch. 3; BDD: Cockburn Ch. 6-7)"
  - "Add Cockburn/Jacobson chapter reference to Skill 3 primary capability (API contract: Jacobson use case interactions)"
  - "Add to Step 7: frontmatter schema validation approach — JSON Schema file validated via jerry ast validate per H-33"
  - "Consider clarifying 'and/or' in contract generation AC to specify minimum scope"
```

**Critical finding:** The Gherkin/BDD inconsistency (line 185 vs. line 175 and AC line 290) is classified as a Critical finding because it directly contradicts the issue's stated design decision about framework independence. This finding blocks PASS per scoring protocol regardless of composite score.
