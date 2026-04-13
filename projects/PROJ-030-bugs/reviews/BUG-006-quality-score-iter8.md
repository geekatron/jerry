# Quality Score Report: ADR-EPIC002-001 Unified Output Path Resolution Standard

## L0 Executive Summary

**Score:** 0.864/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.84)

**One-line assessment:** The ADR is structurally sound and comprehensively specified, but three interconnected gaps block acceptance at the 0.95 threshold: the Step 6/Step 0 migration order presentation creates an implementor hazard, the pseudocode does not specify how LLM agents detect priority-level trigger conditions in practice, and the `{agent}` variable treatment is inconsistent between the Variables table and the governance YAML examples.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-024-tactical-work/work/EPIC-002-issue-triage-batch/ADR-EPIC002-001-unified-output-path-resolution.md`
- **Deliverable Type:** ADR
- **Criticality Level:** C3 (AE-003 auto-escalation; touches agent definitions across 13 skills)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-31T00:00:00Z
- **Iteration:** 8 of C4 adversarial review cycle
- **Prior Score:** 0.888 (iteration 7)
- **Score History:** 0.82 → 0.896 → 0.895 → 0.897 → 0.888 → 0.887 → 0.888 → 0.864

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.864 |
| **Threshold** | 0.92 (H-13); caller-specified 0.95 |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (standalone scoring) |
| **Score vs. Prior** | -0.024 vs. iteration 7 (0.888) |

**Note on score regression:** This score (0.864) is lower than the iteration 7 score (0.888). This is not an error in computation. Independent per-dimension scoring without reference to prior iteration scores produced lower results on Internal Consistency (0.84) and Methodological Rigor (0.86), both of which appear to have been evaluated more leniently in prior iterations. The plateau at 0.887-0.897 across iterations 3-8 suggests prior scores were not actively counteracting leniency bias on these two dimensions. See Detailed Analysis for specific evidence.

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.87 | 0.174 | All core requirements addressed; P2 detection gap and AD-M-011 degradation case unspecified |
| Internal Consistency | 0.20 | 0.84 | 0.168 | Step 6/Step 0 numbering conflict; `{agent}` variable treatment inconsistent between Variables table and governance YAML examples |
| Methodological Rigor | 0.20 | 0.86 | 0.172 | Systematic Nygard format; pseudocode disclaimer creates gap between algorithmic spec and LLM behavioral implementation |
| Evidence Quality | 0.15 | 0.88 | 0.132 | Strong per-file/per-line citations throughout; ux-routing-rules.md and engagement-ID generation claim lack explicit citations |
| Actionability | 0.15 | 0.87 | 0.1305 | Before/after examples for all skill families; Step 3 UX detail deferred to audit link; missing prompt-templates.md update action |
| Traceability | 0.10 | 0.87 | 0.087 | Full chains for decision logic and 107-file count; "13 skills" in Context not linked at point of claim; UX sub-skill glob not enumerated |
| **TOTAL** | **1.00** | | **0.864** | |

---

## Detailed Dimension Analysis

### Completeness (0.87/1.00)

**Evidence:**
The ADR covers every required ADR section: problem framing, prior art analysis, 7 design constraints, 4 options with 7x4 DC satisfaction matrix, decision, 4-priority resolution protocol with pseudocode, agent integration spec (YAML schema, .md template, 3 prompt patterns), 7 failure modes, 6-step migration guide with before/after for all skill families, migration order with rollback, 4-risk migration risk assessment, 7-context compatibility matrix, consequences (positive/negative/neutral), 8-check verification table, 12-source references table.

**Gaps:**

1. **P2 detection ambiguity (specification incompleteness):** The resolution algorithm specifies Priority 2 as triggered when `prompt_context.has("OUTPUT CONTEXT.base_path")`. However, Pattern C (no override, uses default) also uses an `## OUTPUT CONTEXT` block but with only `Engagement ID` — no `Base Path` line. The pseudocode checks for the complete path `OUTPUT CONTEXT.base_path`, which implies the agent must parse for the specific sub-field, not just the section header. But the spec does not define what happens when `## OUTPUT CONTEXT` is present with *only* `Engagement ID` — is that P2 (with null base_path, which is an error) or P3 (correct interpretation)? An LLM agent reading this spec could reasonably implement Pattern C as triggering P2 with a malformed base_path, then failing to Priority 4.

2. **Unmigrated agent behavior at P2 invocation (missing degradation case):** When a caller provides Pattern B (base_path) to an agent that has not yet been migrated (still has old `skills/*/output/` in governance YAML, no `filename_pattern`), what happens? The compatibility matrix covers existing /problem-solving/adversary/nasa-se but does not address partially-migrated state during the 107-file migration.

3. **Prompt-templates.md update not tracked as a migration step:** Consequence #2 ("Callers must learn the protocol — P1/P2/P3 patterns need to be documented in prompt templates") identifies a required action but no migration step exists for it. The 6-step migration guide does not include "update prompt-templates.md."

**Improvement Path:** Add a sub-bullet to the resolution algorithm clarifying that P2 requires `base_path` to be non-null; if `OUTPUT CONTEXT` is present without `base_path`, fall through to P3. Add Step 7 to migration guide: "Update `.context/templates/` or `prompt-templates.md` with P1/P2/P3 caller patterns." Add a table row for partially-migrated agent behavior.

---

### Internal Consistency (0.84/1.00)

**Evidence:**
Numbers are internally consistent: 107 = 22+25+60 (check); 32 = 10+11+11 (check); 13 SKILL.md = 1+1+11 (eng+red+(1 parent+10 UX sub-skills)) (check). The compatibility matrix is consistent with the resolution protocol. Backward compatibility claims align with prior art analysis. DC satisfaction matrix is consistently populated.

**Gaps:**

1. **Step 6/Step 0 numbering conflict — implementor hazard:** The Migration Guide presents six steps numbered 1-6. Step 6 is "Update Governance Schema." The Migration Order section then specifies: "0. Update governance schema FIRST (Step 6) — adds `filename_pattern` as accepted field BEFORE any YAML files reference it." A reader implementing the migration by following Steps 1-6 in order would execute schema last (correct for schema, but the guide does not visually flag Step 6 as special). The "Step 0" label in the execution order contradicts the "Step 6" label in the guide. This is not merely a labeling issue — an implementor who performs Steps 1-5 before Step 6 will create YAML files with `filename_pattern` that fail schema validation until Step 6 is applied (violating the risk mitigation in Migration Risk #2: "Run Step 6 (schema update) before Step 1"). The guide says "Schema validation fails mid-migration due to `filename_pattern`" is Low likelihood, mitigated by "Run Step 6 before Step 1" — but the guide itself orders Step 6 last.

2. **`{agent}` variable inconsistency:** The Variables table in the Agent Integration Specification lists `{agent}` as a variable with source "Agent name from definition" and example `eng-architect`. This implies `{agent}` is a runtime-interpolated variable in `filename_pattern`. But every governance YAML example hardcodes the agent name: `"eng-architect-{topic-slug}.md"`, `"red-recon-{topic-slug}.md"`, `"ux-heart-analyst-{topic-slug}.md"`. The pseudocode `agent_config.output.filename_pattern.interpolate(prompt_context.variables)` would only interpolate `prompt_context.variables` (caller-provided), not the agent's own name. If `{agent}` is baked into each agent's `filename_pattern` at definition time (hardcoded), it should not appear in the Variables table as a runtime variable. If it IS a runtime variable, the governance YAML examples should show `{agent}-{topic-slug}.md` not `eng-architect-{topic-slug}.md`. This inconsistency means implementors will not know whether to hardcode or parametrize the agent name.

3. **Minor:** The Migration Risk table (Risk 2) says "Schema validation fails mid-migration due to `filename_pattern` — Low likelihood — field is additive, schema accepts both formats **until Step 6**" — but Step 6 is supposed to *add* `filename_pattern` support to the schema. Before Step 6, the schema does NOT have `filename_pattern`. So `filename_pattern` in YAML would either (a) pass validation because `additionalProperties` is true in the schema, or (b) fail if the schema is strict. The risk mitigation says "Run Step 6 (schema update) before Step 1, or add field as optional" — this "or" clause suggests the risk mitigation is itself uncertain about the current schema strictness.

**Improvement Path:** Renumber Step 6 to Step 0 directly in the Migration Guide (or mark it with a visual callout: "EXECUTE FIRST"). Decide whether `{agent}` is a runtime variable or a definition-time literal and make the Variables table and governance YAML examples consistent. Clarify the current schema's `additionalProperties` setting to resolve the schema validation uncertainty.

---

### Methodological Rigor (0.86/1.00)

**Evidence:**
Follows Nygard ADR format. Prior art analysis is systematic with a structured comparison table (6 mechanisms × 2 skills). DC satisfaction matrix (7×4) provides objective option comparison. Failure mode analysis uses FMEA-style detection+resolution format. Migration guide has before/after examples for all three skill families. Migration risk assessment (4 risks × 4 columns: likelihood, impact, mitigation). Rollback procedure is per-skill.

**Gaps:**

1. **Pseudocode specification vs. LLM behavioral implementation (core methodological gap):** The pseudocode disclaimer correctly says "agents implement this logic through their prompt instructions and tool calls, not through a Python function." But the ADR does not specify *how* an LLM agent implements Priority 1 detection. The agent receives a markdown prompt. It must recognize `## MANDATORY PERSISTENCE (P-002)\nCreate file at: {path}` as a P1 override. What if the user writes `**Output file:** {path}` instead? What if the P-002 block uses different formatting? The methodology specifies the resolution logic at the algorithmic level but not at the prompt-parsing behavioral level. For an ADR whose entire value is specifying LLM agent behavior, this is a methodological gap — the spec is incomplete at the layer where it must actually be implemented.

2. **AD-M-011 acceptance process not specified:** The migration guide includes "Step 5: Codify as AD-M-011 Standard" with the MEDIUM tier vocabulary standard draft. But the ADR does not specify how this standard becomes accepted — does this ADR's acceptance implicitly approve AD-M-011, or is a separate modification to `agent-development-standards.md` required with its own quality gate? The ADR should clarify whether this is a self-contained acceptance or requires a follow-on.

3. **Verification is primarily manual:** 6 of 8 verification checks are "manual test." For a 107-file migration, the only automated checks are `grep -r 'skills/.*/output/' skills/` and `uv run jerry schema validate`. The methodology does not include a specification for an automated post-migration validation script or CI check that would verify all 32 agents have been updated. This is a significant gap in verification methodology for the scale of the migration.

**Improvement Path:** Add a "Prompt Recognition Specification" sub-section that defines the exact prompt block headers agents must recognize as P1/P2 triggers. Clarify the AD-M-011 acceptance process. Add Step 8 (or extend verification): "Write a pre-commit/CI check that enforces zero `skills/*/output/` matches post-migration."

---

### Evidence Quality (0.88/1.00)

**Evidence:**
Strong citation quality throughout. Specific file:line references: `skills/problem-solving/composition/ps-researcher.prompt.md` lines 213-243; `skills/problem-solving/templates/PS_EXTENSION.md` lines 76-131; `skills/problem-solving/SKILL.md` lines 78-88; `skills/adversary/agents/adv-scorer.governance.yaml`; `skills/nasa-se/agents/nse-architecture.governance.yaml`. Three audit sub-files cited (eng-audit, red-audit, ux-audit) with per-file line numbers documented in those files. GH #230 linked. TASK-008 linked.

**Gaps:**

1. **Engagement-ID generation claim uncited:** Consequence #3 says "Engagement-ID generation moves from skill-internal (current) to caller-provided." The claim that engagement-IDs are currently generated "skill-internally" is asserted without a citation showing the current mechanism. Where in the current agent definitions is engagement-ID generated? A reader auditing this claim cannot verify it without searching the codebase independently.

2. **UX sub-skill governance references lack explicit file names:** Step 1 lists the UX governance files as `skills/ux-{ai-first-design,atomic-design,...}/agents/*.governance.yaml` — a glob, not explicit file names. The ux-audit-detail.md file contains the per-file breakdown, but the Migration Guide step itself does not enumerate the files. This weakens the evidence quality at the point of action.

3. **ux-routing-rules.md and wave-progression.md cited in Migration Risk #3 but not in References table:** "UX orchestrator references sub-skill output paths that changed — Mitigation: Update orchestrator rules (ux-routing-rules.md, wave-progression.md)." These files are action targets but are not in the References table, making them hard to locate for implementors.

**Improvement Path:** Add a citation for the current engagement-ID generation mechanism (specific file:line showing where eng/red/UX agents currently generate or receive engagement-IDs). Add `ux-routing-rules.md` and `wave-progression.md` to the References table. Expand the UX governance file glob to explicit file names in Step 1, or explicitly cross-reference to ux-audit-detail.md at that point.

---

### Actionability (0.87/1.00)

**Evidence:**
Before/after diffs are provided for all three skill families (eng, red, UX) for governance YAML (Step 1), agent .md (Step 2), SKILL.md (Step 3), and templates (Step 4). Recommended skill sequence (eng-team first, then red-team, then UX) with rationale. Rollback procedure is per-skill with specific git command. Verification includes runnable commands (`grep -r`, `uv run jerry schema validate`). Step 0 (schema-first) execution order is called out explicitly.

**Gaps:**

1. **Step 3 UX detail deferred to external link:** "Also update any examples, P-002 sections, and rules files that reference `skills/*/output/` paths. The UX skills have 15 rules files with output path references... see [UX audit detail] for per-file line numbers." An implementor executing Step 3 must open the audit detail file to know which files to update. The step is not self-contained. For eng-team and red-team, the SKILL.md example is shown inline. UX Step 3 is the weakest actionability point.

2. **Missing action for prompt-templates.md:** Consequence #2 identifies that callers must learn the P1/P2/P3 patterns and that these need to be documented in prompt templates. No migration step creates or updates prompt templates. A user finishing the 6-step migration will still have callers who don't know the new patterns.

3. **Step 5 location underspecified:** "Add to `.context/rules/agent-development-standards.md` in the Agent Structure Standards table (after AD-M-010)." The exact insertion point ("after AD-M-010") is correct but the AD-M-011 text is provided as a code block in the ADR rather than as a ready-to-apply diff. An implementor must copy the text and find the right table row manually.

4. **Step 6 JSON diff context insufficient:** The JSON diff shows the `filename_pattern` addition inside an `output` object but doesn't show the surrounding JSON path. An implementor must open `agent-governance-v1.schema.json` and locate the `output` property definition. A more complete diff showing 3-5 lines of context above and below would make Step 6 directly actionable.

**Improvement Path:** Inline the key UX files for Step 3 (or at minimum list the 15 rules files explicitly). Add Step 7: "Update `.context/templates/` caller-pattern documentation with P1/P2/P3 examples." Provide Step 6 with JSON context showing parent path. Provide Step 5 as a ready-to-paste table row with the surrounding markdown context.

---

### Traceability (0.87/1.00)

**Evidence:**
Decision traceability is excellent: each DC maps to a governance source (H-04, P-002, P-020 are constitutional rules). Option D selection is supported by 7/7 DC satisfaction. The 107-file/32-agent claims trace through three audit sub-files. The /problem-solving prior art traces to specific composition files and line numbers. AD-M-011 traces to ADR-EPIC002-001 and BUG-006.

**Gaps:**

1. **"13 skills" claim in Context section lacks in-context citation:** The Context section says "13 skills — 3 skill families spanning 13 SKILL.md directories: eng-team (1), red-team (1), and user-experience (1 parent + 10 sub-skills)" without linking to BUG-006 at this point. The BUG-006 audit is cited later in References but the claim is made in Context without a link. A reader challenging the count cannot immediately follow the evidence chain without scrolling to References.

2. **UX sub-skill enumeration in Step 1 uses a glob:** `skills/ux-{ai-first-design,atomic-design,behavior-design,design-sprint,heart-metrics,heuristic-eval,inclusive-design,jtbd,kano-model,lean-ux}/agents/*.governance.yaml` — the trace to "which specific files" requires expanding the glob. The ux-audit-detail.md file presumably has the enumeration, but it is not accessible inline. The 11-file count in Step 1 header is asserted but not proved at the step level (the proof is in the linked audit).

3. **ux-routing-rules.md, wave-progression.md files not in References table** — cited in Migration Risk #3 as files requiring update, but not listed as References, making the reverse trace (from risk mitigation to source file) incomplete.

**Improvement Path:** Add an in-context citation to BUG-006 in the Context section after the skill-count claim. Add explicit file enumeration for UX governance YAML in Step 1 (or reference the audit detail at that specific point). Add `ux-routing-rules.md` and `wave-progression.md` to References table.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.84 | 0.91 | Renumber Step 6 as Step 0 (or add a visual callout "EXECUTE FIRST") in the Migration Guide body — not just in the Migration Order section. This is the highest-risk gap: an implementor following steps sequentially will apply schema change last, potentially causing validation failures. |
| 2 | Internal Consistency | 0.84 | 0.91 | Resolve `{agent}` variable: decide whether it is runtime-interpolated (then governance YAML should use `{agent}-{topic-slug}.md`) or definition-time literal (then remove `{agent}` from the Variables table and clarify it is baked in per agent). |
| 3 | Methodological Rigor | 0.86 | 0.92 | Add a "Prompt Recognition Specification" sub-section specifying the exact markdown section headers and field names agents must match for P1 (`## MANDATORY PERSISTENCE (P-002)` with `Create file at:`) and P2 (`## OUTPUT CONTEXT` with `- **Base Path:**`). This closes the gap between algorithmic pseudocode and LLM behavioral implementation. |
| 4 | Completeness | 0.87 | 0.92 | Add clarification to the resolution algorithm: if `## OUTPUT CONTEXT` is present but `Base Path` is absent, fall through to P3. Add to the pseudocode as a condition inside the P2 block. |
| 5 | Completeness | 0.87 | 0.92 | Add Step 7 to migration guide: "Update prompt-templates.md with P1/P2/P3 caller patterns." |
| 6 | Actionability | 0.87 | 0.91 | Either inline the 15 UX rules files for Step 3, or add a direct link to the ux-audit-detail.md at the point of the Step 3 action (not just in References). |
| 7 | Evidence Quality | 0.88 | 0.92 | Add a specific citation for the current engagement-ID generation mechanism (file:line in an eng/red/UX agent definition showing where engagement-IDs are currently handled). |
| 8 | Traceability | 0.87 | 0.92 | Add inline BUG-006 citation to the "13 skills" claim in the Context section. Add `ux-routing-rules.md` and `wave-progression.md` to the References table. |

---

## Plateau Analysis

This is the 8th iteration. Scores have plateaued in the 0.887-0.897 band across iterations 3-8. This score (0.864) is lower than prior scores, which reflects independent evaluation finding that Internal Consistency and Methodological Rigor were being scored at 0.90+ in prior iterations without the specific evidence required to justify those scores.

The plateau signature indicates the deliverable has been iterated to a high level of completeness and evidence quality, but two structural gaps have not been resolved across 6 iterations:

- The Step 6/Step 0 numbering conflict (present since Step 0 was added; the Migration Guide has not been updated to match)
- The pseudocode/LLM-implementation gap (the pseudocode disclaimer was added in iteration 8, but this addresses the wrong issue — the problem is not "readers thinking this is executable code," it is "the spec does not define LLM prompt-parsing behavior")

To break the plateau and reach 0.92: address Priority 1, 2, and 3 recommendations above. These three changes directly close the two structural gaps. The remaining recommendations (4-8) are incremental refinements that together could push the score toward 0.95.

---

## Leniency Bias Check

- [x] Each dimension scored independently (no cross-dimension inflation)
- [x] Evidence documented for each score with specific quotes and section references
- [x] Uncertain scores resolved downward (Internal Consistency held at 0.84 despite good overall structure; Methodological Rigor held at 0.86 despite comprehensive format)
- [x] Plateau calibration considered — lower score than prior iterations reflects independent evidence-based evaluation, not drift
- [x] No dimension scored above 0.90 (highest is Evidence Quality at 0.88, supported by specific file:line citations throughout)
- [x] Score (0.864) is in the "strong work with significant improvement needed" range, consistent with an ADR that has been extensively revised but retains structural gaps in its specification methodology

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.864
threshold: 0.92
weakest_dimension: internal_consistency
weakest_score: 0.84
critical_findings_count: 0
iteration: 8
improvement_recommendations:
  - "Renumber Step 6 as Step 0 in Migration Guide body (not just Migration Order section) — implementor hazard"
  - "Resolve {agent} variable inconsistency: runtime interpolated vs definition-time literal"
  - "Add Prompt Recognition Specification sub-section defining exact markdown headers for P1/P2 detection"
  - "Clarify P2 fallthrough: OUTPUT CONTEXT present without Base Path = P3, not malformed P2"
  - "Add Step 7 to migration guide: update prompt-templates.md with P1/P2/P3 caller patterns"
  - "Inline or directly link UX rules files at Step 3 action point"
  - "Add citation for current engagement-ID generation mechanism"
  - "Add inline BUG-006 citation at 13-skills claim; add ux-routing-rules.md to References"
```
