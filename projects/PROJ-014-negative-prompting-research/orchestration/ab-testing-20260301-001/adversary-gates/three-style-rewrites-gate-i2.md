# Quality Score Report: Three-Style Rewrites — PROJ-014 A/B Testing (Iteration 2)

## L0 Executive Summary

**Score:** 0.882/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.80)
**One-line assessment:** Iteration 2 resolved all four iteration-1 defects (D-001 through D-004), but introduced a dual-neutral inconsistency for H-22 and carries two residual scope asymmetries (H-31 "irreversible" omission, H-01 C2-vs-C3 clause count) that together keep Internal Consistency below the 0.95 threshold required for a C4 artifact.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/ab-testing-20260301-001/phase-0-design/three-style-rewrites.md`
- **Deliverable Type:** Analysis / Experimental Design Artifact
- **Criticality Level:** C4 (Critical — irreversible architectural impact on A/B experiment validity)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Iteration:** 2 (revision addressing D-001 through D-004 from iteration 1)
- **Scored:** 2026-03-01

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.882 |
| **Threshold** | 0.95 (C4 adversary gate) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (adv-executor reports not provided; direct artifact scoring) |
| **Prior Score (Iteration 1)** | 0.856 |
| **Score Delta** | +0.026 |

---

## Iteration 1 Defect Resolution Status

| Defect | Severity | Status | Evidence |
|--------|----------|--------|----------|
| D-001 | Critical | **RESOLVED** | H-07 C3 `<prohibition>` now contains all three sub-rules: "NEVER import from infrastructure/, application/, or interface/ within src/domain/. NEVER import from infrastructure/ or interface/ within src/application/. NEVER instantiate infrastructure adapters outside src/bootstrap.py." (lines 155-156) |
| D-002 | Significant | **PARTIALLY RESOLVED** | H-22 C1 narrowed to /problem-solving only (line 262). H-22 C2/C3 already /problem-solving only. BUT: the Neutral Descriptions table (line 356) still lists all four skills. The inline neutral (lines 256-257) correctly shows /problem-solving only. Two inconsistent neutrals exist in the same document — this is a new defect (D-005). |
| D-003 | Borderline | **RESOLVED** | H-02 C2: "NEVER override user instructions. NEVER substitute a different action..." — no "without Y". H-31 C2: "NEVER proceed on a request that has...NEVER assume intent..." — no "without Y". H-22 C2: "NEVER skip...NEVER delay..." — no "without Y". H-15 C2: "NEVER present an unreviewed deliverable. NEVER pass an unreviewed deliverable..." — no "without Y". All four pass bare NPT-014 form. |
| D-004 | Minor | **RESOLVED** | H-07 neutral (lines 135-137): "Domain code imports only from stdlib and shared_kernel. Application code imports only from domain. Infrastructure adapters are instantiated exclusively in bootstrap.py." Positive factual language throughout. No "does not" present. |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.92 | 0.184 | All 30 rewrites + 10 neutrals present; validation checklist fully populated; navigation table with anchors; source citations for all 10 constraints |
| Internal Consistency | 0.20 | 0.80 | 0.160 | D-005 (new): H-22 table neutral lists 4 skills vs inline neutral + C1/C2/C3 covering 1; D-006: H-31 C1 includes "irreversible" trigger absent from C2/C3; D-007: H-01 C2 has 2 prohibition clauses, C3 has 1 |
| Methodological Rigor | 0.20 | 0.88 | 0.176 | C1 all-positive confirmed; C2 bare NEVER form confirmed post-D-003; C3 all-four-tag confirmed; dual-neutral inconsistency indicates incomplete harmonization across the document during revision |
| Evidence Quality | 0.15 | 0.90 | 0.135 | All constraints cite source files; C3 consequence fields trace to documented consequences; S-010 self-review documents specific revision decisions with rationale; no invented consequences |
| Actionability | 0.15 | 0.90 | 0.135 | All rewrites operationally clear; C3 `<verify>` tags provide scorable criteria; concrete tool names, file paths, thresholds included where applicable; H-31 C3 "at least one" slightly softens specificity |
| Traceability | 0.10 | 0.92 | 0.092 | Source rules cited in checklist for all 10; parent document (constraint-selection.md) referenced; workflow and document ID provenance present; self-review revision decisions documented |
| **TOTAL** | **1.00** | | **0.882** | |

---

## Detailed Dimension Analysis

### Completeness (0.92/1.00)

**Evidence:**
- All 30 rewrites present and organized by constraint (10 constraints × 3 conditions). Confirmed by heading count and validation checklist items at lines 367-377.
- All 10 neutral descriptions present in both inline form (above each C1/C2/C3 trio) and table form (lines 347-358).
- Navigation table with anchor links present (lines 14-21).
- Validation checklist covers all required dimensions: count verification, C1 negative-language check, C2 format check, C3 four-tag check, neutral quality check, condition-label absence check, semantic equivalence check, source verification check.
- S-010 self-review section present (lines 466-485) with documented corrections.

**Gaps:**
- The existence of two neutrals per constraint (inline + table) creates a structural redundancy. The table entries for H-22 are inconsistent with the inline version — this is captured as an Internal Consistency defect (D-005). From a pure completeness standpoint all required elements are present; the issue is their consistency, not presence.

**Improvement Path:**
- Remove structural redundancy by either: (a) deleting the inline neutrals and relying solely on the table, or (b) eliminating the standalone table and relying solely on the inline neutrals. Either approach eliminates the dual-source inconsistency risk.

---

### Internal Consistency (0.80/1.00)

**Evidence:**
D-005 (New, Significant): The Neutral Descriptions table entry for H-22 (line 356) reads: "The framework maps task types to specific skills. Research and analysis tasks are handled by `/problem-solving`, multi-phase workflows by `/orchestration`, requirements and design by `/nasa-se`, and adversarial quality reviews by `/adversary`. Skills are expected to be invoked at task initiation rather than partway through or after completion."

This contradicts the inline neutral for H-22 (lines 256-257): "The framework maps research and analysis tasks to the `/problem-solving` skill. The skill is expected to be invoked at task initiation rather than partway through or after completion."

The table neutral lists all four skills; the inline neutral lists one. The C1, C2, and C3 rewrites all cover only `/problem-solving`. Phase 2 scorers are instructed to use the neutral description table for orientation. If a scorer uses the table neutral to understand what the constraint covers, they will evaluate compliance against a four-skill scope, while the actual conditions only test /problem-solving invocation. This is an informational confound residue of D-002 — D-002 was partially resolved (C1 narrowed) but the table neutral was not updated.

D-006 (New, Borderline): H-31 trigger conditions are asymmetric across conditions:
- C1 (line 231): "when a request has multiple valid interpretations, when scope is unclear, or when the implied action is destructive or irreversible"
- C2 (lines 236-237): "a request that has multiple valid interpretations, unclear scope, or destructive implications"
- C3 (lines 245-246): "multiple valid interpretations exist, scope is unclear, or the action is destructive"
- Source rule (H-31): "destructive or irreversible action"

C1 accurately includes "irreversible" as a fourth trigger condition; C2 and C3 omit it, using only "destructive." A model receiving C1 would treat irreversibility as a standalone trigger; a model receiving C2 or C3 would not. This is a minor content confound — the trigger condition set is not identical across conditions.

D-007 (New, Borderline): H-01 has scope asymmetry between C2 and C3:
- C2 (lines 58-59): Two NEVER clauses — (1) "NEVER spawn sub-agents from within a worker agent" and (2) "NEVER include the Task tool in a worker agent's allowed tools."
- C3 `<prohibition>` (line 65): One clause — "NEVER spawn sub-agents from a worker agent." The Task tool declaration prohibition is absent from `<prohibition>`.
- C3 `<verify>` (line 68): "No Task tool call appears in the worker agent's output" — this covers tool invocation in output, not tool declaration in allowed_tools.

C2 prohibits both the behavior (spawning) and the structural configuration (Task tool in allowed_tools declaration). C3 prohibits only the behavior. A model receiving C2 would understand that tool declaration is prohibited; a model receiving C3 would only understand that spawning behavior is prohibited. This is a structural-vs-behavioral prohibition asymmetry.

**Gaps:**
Three defects affecting cross-condition equivalence, which is the primary validity requirement for the A/B experiment. D-005 is significant (table neutral vs conditions mismatch). D-006 and D-007 are borderline but real.

**Improvement Path:**
- D-005: Update the H-22 Neutral Descriptions table entry to match the inline neutral: "The framework maps research and analysis tasks to the `/problem-solving` skill. The skill is expected to be invoked at task initiation rather than partway through or after completion."
- D-006: Add "or irreversible" to H-31 C2 and C3. C2: "NEVER proceed on a request that has multiple valid interpretations, unclear scope, or destructive or irreversible implications." C3 `<prohibition>`: "...or the action is destructive or irreversible."
- D-007: Add the Task tool clause to H-01 C3 `<prohibition>`: "NEVER spawn sub-agents from a worker agent. NEVER include the Task tool in a worker agent's tool declarations." Update `<verify>` accordingly.

---

### Methodological Rigor (0.88/1.00)

**Evidence:**
NPT-007 (C1) compliance: All 10 C1 rewrites confirmed positive-only. The validation checklist at lines 381-390 systematically checks each. Independent verification confirms no negative language in any C1 rewrite. The H-07 C1 revision (noted in self-review: "Initial draft used 'you should import only...' — revised to 'Keep domain code isolated: import only from...'") demonstrates methodological care.

NPT-014 (C2) compliance: All 10 C2 rewrites use NEVER X form. Post-D-003 revision, the four previously flagged C2 rewrites (H-02, H-31, H-22, H-15) now use pure NEVER X without Y qualifications. The self-review at line 477 confirms awareness of the confound risk: "C2 rewrites: Reviewed each for absence of explanatory text." H-07 C2 correctly uses three NEVER clauses covering all sub-rules, which is NPT-014 compliant (multiple NEVER X statements are permitted).

NPT-013 (C3) compliance: All 10 C3 rewrites contain all four required XML tags (`<prohibition>`, `<consequence>`, `<instead>`, `<verify>`). Validated at lines 407-416.

Neutral format compliance: Inline neutrals are factual/passive throughout. The self-review at line 479 correctly addresses the H-22 borderline case ("H-22 neutral uses 'are expected to be invoked' — borderline; reread confirms this describes a framework behavior pattern (factual) rather than instructing the scorer").

**Gaps:**
The D-005 issue (H-22 table neutral retaining four-skill scope) indicates that the revision process did not harmonize content across both neutral presentation surfaces. The methodology for keeping neutrals consistent across inline and table was not fully applied. This is a process gap, not a format violation — the table neutral is still factual/passive, but it is factually inconsistent with the inline neutral and the conditions.

**Improvement Path:**
Add a check to the validation methodology: "For each constraint, verify that the table neutral and the inline neutral encode the same scope." Currently the validation checklist covers neutral format (no imperative, no prohibition) but not neutral scope consistency.

---

### Evidence Quality (0.90/1.00)

**Evidence:**
All 10 constraints have source file citations in the validation checklist (lines 453-462). Citations include specific file paths, section names, and where applicable, line numbers. Example: "H-07 verified against: `.context/rules/architecture-standards.md` (HARD Rules table, line 34) and L2-REINJECT rank=4" (line 456).

The C3 consequence fields trace to documented source consequences: "CI blocks merge" from H-07 (line 156), "environment corruption" from H-05 (line 126), "context window exhaustion" from H-01 (line 66). The self-review at line 474 explicitly states: "No consequences were invented."

The S-010 self-review (lines 466-485) documents specific revision decisions with rationale — three concrete examples of what was changed and why (H-07 C1 "you should" hedge removed; H-22 C3 `<verify>` tag refined; T1-T5 C3 `<instead>` tag refined). This provides an auditable evidence trail for the revision.

**Gaps:**
For D-006 (H-31 "irreversible" omission), the self-review checks for semantic equivalence (line 447: "H-31: All three encode 'ask when ambiguous (multiple interpretations, unclear scope, destructive action)' — passes") but does not catch the "irreversible" missing from C2 and C3. The source verification check for H-31 (line 459) cites the source rule but does not perform a term-by-term comparison between source and rewrites. Evidence quality would improve with a more rigorous source-vs-rewrite diff check.

**Improvement Path:**
Add a term-by-term comparison step to source verification: for each trigger condition in the source rule, confirm each condition is present in all three framing conditions and the neutral. A brief diff table (source term | C1 | C2 | C3) would catch the D-006 class of issue.

---

### Actionability (0.90/1.00)

**Evidence:**
All rewrites are operationally clear and provide sufficient context for an agent to act on them. C3 rewrites include concrete alternatives and verifiable criteria:
- H-05 C3 `<instead>`: "Use uv run for all execution (e.g., uv run pytest tests/) and uv add for all dependency management (e.g., uv add requests)" — includes working examples.
- H-07 C3 `<verify>`: "No infrastructure/ or application/ import statement appears in any file under src/domain/; no infrastructure/ or interface/ import statement appears in any file under src/application/; no adapter instantiation appears outside src/bootstrap.py." — fully specific and checkable.
- H-10 C3 `<instead>`: "Create a separate .py file for each public class, named after the class it contains (e.g., money.py for class Money)" — includes a concrete example.

C1 rewrites provide actionable positive instructions with specifics: thresholds (0.92), tool names (`uv run`, `uv add`), file locations (`src/bootstrap.py`), format details (S-014 six-dimension rubric).

**Gaps:**
H-31 C3 `<prohibition>` (line 245): "NEVER proceed on an ambiguous request without asking at least one clarifying question" — the "at least one" qualifier softens specificity compared to C1 ("ask one targeted clarifying question") and the source rule. An agent receiving C3 might ask multiple clarifying questions, whereas C1 specifies exactly one. This is a minor actionability gap — C3 is slightly less prescriptive than C1 on this specific point.

**Improvement Path:**
Change H-31 C3 `<prohibition>` to: "NEVER proceed on an ambiguous request without asking one clarifying question..." (remove "at least") to match C1 and the source rule's "one targeted clarifying question" specification.

---

### Traceability (0.92/1.00)

**Evidence:**
- Document ID, phase, workflow, parent task, date, and author present in frontmatter (lines 3-9).
- Source verification for all 10 constraints documented in validation checklist (lines 453-462) with specific file paths.
- Parent document (constraint-selection.md / PROJ-014-AB-PHASE0-01) referenced in multiple locations (lines 28, 491).
- S-010 self-review section documents the self-review process and specific corrections made.
- Iteration 2 status documented in author field: "revised by design-agent-002-r2" (line 8).
- Status field explicitly states: "REVISED — iteration 2 addressing C4 adversary gate defects D-001 through D-004" (line 9).
- Document version and workflow step present (lines 488-492).

**Gaps:**
The revision history does not include a reference to the iteration 1 score report path. Tracing the revision chain requires knowing where the iteration 1 gate report lives; that path is not cited in this document. Minor gap — the source evidence for the defects addressed is described but not linked.

**Improvement Path:**
Add the iteration 1 gate report path to the document header: "Prior Gate Report: `projects/PROJ-014-negative-prompting-research/orchestration/ab-testing-20260301-001/adversary-gates/three-style-rewrites-gate-i1.md`" (or equivalent path).

---

## New Defects Found (D-005 through D-007)

| ID | Severity | Dimension Impacted | Description | Required Fix |
|----|----------|-------------------|-------------|--------------|
| D-005 | Significant | Internal Consistency | H-22 Neutral Descriptions table (line 356) lists all four skills (/problem-solving, /orchestration, /nasa-se, /adversary). The inline neutral for H-22 (lines 256-257) and all three conditions (C1/C2/C3) cover only /problem-solving. Phase 2 scorers use the table for orientation — a four-skill neutral creates an informational confound if scorers evaluate against broader scope than the conditions test. This is a residual D-002 fix: C1 was narrowed but the table neutral was not. | Update the H-22 row in the Neutral Descriptions table to: "The framework maps research and analysis tasks to the `/problem-solving` skill. The skill is expected to be invoked at task initiation rather than partway through or after completion." |
| D-006 | Borderline | Internal Consistency | H-31 trigger conditions asymmetric: C1 includes "or irreversible" as a trigger condition (line 231); C2 and C3 omit it, using only "destructive." Source rule H-31 specifies "destructive or irreversible action." C1 is more faithful to the source. A model receiving C1 treats irreversibility as a standalone trigger; models receiving C2 or C3 do not. Minor content confound. | Add "or irreversible" to H-31 C2: "NEVER proceed on a request that has multiple valid interpretations, unclear scope, or destructive or irreversible implications." Add "or irreversible" to H-31 C3 `<prohibition>`: "...or the action is destructive or irreversible." |
| D-007 | Borderline | Internal Consistency | H-01 C2 has two prohibition clauses: (1) "NEVER spawn sub-agents from within a worker agent" and (2) "NEVER include the Task tool in a worker agent's allowed tools." H-01 C3 `<prohibition>` has only one clause: "NEVER spawn sub-agents from a worker agent." The Task tool declaration prohibition is absent from C3 `<prohibition>`. C3 `<verify>` checks tool calls in output but not tool declarations in configuration. C2 prohibits both behavior and structural configuration; C3 prohibits only behavior. | Add to H-01 C3 `<prohibition>`: "NEVER spawn sub-agents from a worker agent. NEVER declare the Task tool in a worker agent's allowed tools." Update `<verify>` to: "No Task tool call appears in the worker agent's output, and the Task tool does not appear in the agent's declared tool list." |

---

## Improvement Recommendations (Priority Ordered)

| Priority | Defect | Dimension | Current | Target | Recommendation |
|----------|--------|-----------|---------|--------|----------------|
| 1 | D-005 | Internal Consistency | 0.80 | 0.88+ | Update H-22 Neutral Descriptions table entry (line 356) to match the inline neutral: remove references to /orchestration, /nasa-se, /adversary and retain only /problem-solving scope. Single-line edit. |
| 2 | D-006 | Internal Consistency | 0.80 | 0.88+ | Add "or irreversible" to H-31 C2 and H-31 C3 `<prohibition>`. Two-line edit across two rewrites. |
| 3 | D-007 | Internal Consistency | 0.80 | 0.88+ | Add Task tool declaration prohibition to H-01 C3 `<prohibition>` and update `<verify>` tag. Two-line edit within one rewrite. |
| 4 | H-31 C3 "at least" | Actionability | 0.90 | 0.92 | Change "at least one clarifying question" to "one clarifying question" in H-31 C3 `<prohibition>` (line 245) to match C1 and source rule specificity. Single-word deletion. |
| 5 | Traceability gap | Traceability | 0.92 | 0.95 | Add iteration 1 gate report path to document header for complete revision chain traceability. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific line references
- [x] Uncertain scores (Internal Consistency 0.80 vs 0.82) resolved downward — three documented defects (D-005 significant, D-006/D-007 borderline) justify the lower score
- [x] C4 calibration considered: 0.95 is the threshold; this artifact scores 0.882, which is below threshold. The three new defects are real and independently identifiable.
- [x] No dimension scored above 0.95
- [x] Prior score (0.856) not allowed to anchor current scoring — each dimension evaluated fresh against artifact content

**Anti-leniency note on Internal Consistency:** The temptation is to treat D-006 and D-007 as negligible and score Internal Consistency at 0.87+. However, this artifact is an experiment design document where cross-condition equivalence is the primary validity requirement. A model receiving H-31 C1 has one more trigger condition ("irreversible") than a model receiving H-31 C2 or C3. Even if the behavioral difference is small, any content confound in an experiment designed to isolate framing effects is a genuine validity threat. The 0.80 score reflects that three independent cross-condition inconsistencies exist, with the D-005 inconsistency being significant enough to affect Phase 2 scoring validity.

---

## Session Context (Orchestrator Handoff)

```yaml
verdict: REVISE
composite_score: 0.882
threshold: 0.95
weakest_dimension: internal_consistency
weakest_score: 0.80
critical_findings_count: 0
iteration: 2
improvement_recommendations:
  - "D-005: Update H-22 Neutral Descriptions table entry to /problem-solving scope only (line 356)"
  - "D-006: Add 'or irreversible' to H-31 C2 and C3 <prohibition> to match source rule and C1"
  - "D-007: Add Task tool declaration prohibition to H-01 C3 <prohibition> and update <verify>"
  - "H-31 C3: Remove 'at least' from 'at least one clarifying question' to match C1 specificity"
  - "Traceability: Add iteration 1 gate report path to document header"
```

---

*Score Report Version: 1.0.0*
*Agent: adv-scorer*
*Strategy: S-014 (LLM-as-Judge)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Workflow: ab-testing-20260301-001 / Adversary Gate Iteration 2*
*Scored: 2026-03-01*
