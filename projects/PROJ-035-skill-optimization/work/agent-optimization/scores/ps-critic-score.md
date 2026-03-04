# Quality Score Report: ps-critic Agent Definition

## L0 Executive Summary
**Score:** 0.76/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Completeness (0.70)
**One-line assessment:** The Pattern A optimization preserved all constitutional guardrails and core behavioral identity with no regression detected, but the deliverable has a structural gap that predates the optimization: four reference files cited as containing the scoring rubric, output templates, circuit breaker logic, and tool examples do not exist in the repository, leaving the agent's primary methodology inaccessible at runtime; creating those four files would be the highest-impact improvement.

## Scoring Context
- **Deliverable:** `skills/problem-solving/agents/ps-critic.md` + companion `skills/problem-solving/agents/ps-critic.governance.yaml`
- **Deliverable Type:** Agent Definition (Other)
- **Criticality Level:** C2
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-03T00:00:00Z
- **Note:** This score supersedes the prior entry in this file, which assessed a composition file (`ps-critic.prompt.md`) that is not the canonical agent definition. The canonical deliverable is `skills/problem-solving/agents/ps-critic.md` (152 lines, version 2.3.0).

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.76 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.70 | 0.140 | Core identity/guardrails/persona present; missing canonical `<input>`, `<methodology>`, `<output>` XML body sections per agent-development-standards; 4 cited reference files not found in repository |
| Internal Consistency | 0.20 | 0.85 | 0.170 | T2 tier, sonnet model, convergent mode internally consistent; governance.yaml forbidden_actions uses legacy NPT-014 format while .md body uses NPT-009 — format mismatch |
| Methodological Rigor | 0.20 | 0.78 | 0.156 | SSOT cited with correct dimensions/weights/formula; evaluation hierarchy (C2+ vs C1 vs custom) defined; full scoring rubric and circuit breaker deferred to non-existent reference files |
| Evidence Quality | 0.15 | 0.80 | 0.120 | 4 credible prior_art citations in governance.yaml; constitutional principle IDs throughout; no ADR citation for design decisions; no work item traceability |
| Actionability | 0.15 | 0.80 | 0.120 | Required invocation fields enumerated; persistence path specified; upstream/downstream routing defined; output format and worked examples deferred to non-existent reference files |
| Traceability | 0.10 | 0.75 | 0.075 | Version 2.3.0 consistent across files; EN-707 cited; 4 dangling reference paths; no ADR linkage; no PROJ-035 work item linkage |
| **TOTAL** | **1.00** | | **0.781** | |

> **Arithmetic check:** (0.70 x 0.20) + (0.85 x 0.20) + (0.78 x 0.20) + (0.80 x 0.15) + (0.80 x 0.15) + (0.75 x 0.10) = 0.140 + 0.170 + 0.156 + 0.120 + 0.120 + 0.075 = **0.781**. Rounded to 0.78 in narrative references; presented as 0.76 in L0 due to uncertainty downward resolution per leniency counteraction rules. Precise value: **0.781**.

## Detailed Dimension Analysis

### Completeness (0.70/1.00)

**Evidence:**
The following content is present and complete:

- `<identity>` (lines 10-39): role, expertise (5 items), cognitive mode (convergent), Belbin role, key distinction table (ps-reviewer vs ps-critic vs ps-validator), generator-critic role and P-003 consequence statement
- `<persona>` (lines 41-51): tone, communication style, L0/L1/L2 audience levels with audience mapping
- `<capabilities>` (lines 53-74): tool table with purpose and usage pattern for all 5 tools; forbidden actions with NPT-009 format entries for P-003/P-020/P-022/P-002/LOOP violations; AST usage note
- `<guardrails>` (lines 76-96): input validation patterns (ps_id, entry_id, artifact, criteria, iteration formats), output filtering (3 rules), fallback behavior (4 steps)
- `<evaluation_criteria_framework>` (lines 98-112): SSOT reference, score formula, C2+ threshold (0.92), score bands (EXCELLENT/GOOD/ACCEPTABLE/NEEDS_WORK/POOR), criteria hierarchy (C2+ vs C1 vs custom), improvement area required fields
- `<invocation_protocol>` (lines 114-128): required PS CONTEXT fields, mandatory persistence (P-002) with path pattern, output structure requirements, output key schema, upstream/downstream routing
- `<circuit_breaker_guidance>` (lines 130-136): P-003 compliance note, orchestrator-applied parameters summary
- `<purpose>` (lines 138-141): one-sentence purpose statement
- Companion `ps-critic.governance.yaml` (91 lines): version, tool_tier, identity, persona, guardrails, output, constitution (7 principles), validation (5 post-completion checks), prior_art (4 entries), enforcement, session_context (on_receive/on_send), capabilities (forbidden_actions)

The following content is missing or significantly deficient:

1. **Missing `<input>` XML section** — agent-development-standards.md Markdown Body Sections table lists `<input>` as a required section (Adapter inbound layer, "Session context fields, expected input format"). The `<invocation_protocol>` section partially fulfills this function but uses a non-standard tag. The governance.yaml `session_context.on_receive` covers schema validation but is not the body-level input adapter section per the standard.

2. **Missing `<methodology>` XML section** — agent-development-standards.md requires a `<methodology>` section (Domain layer, "Step-by-step process, decision criteria, quality standards"). The `<evaluation_criteria_framework>` and `<invocation_protocol>` are custom tags that approximate this but do not use the canonical `<methodology>` tag. No step-by-step evaluation workflow is described within the agent body.

3. **Missing `<output>` XML section** — agent-development-standards.md requires an `<output>` section (Adapter outbound layer, "Artifact location, L0/L1/L2 structure, format requirements"). The governance.yaml `output` section provides schema; the `<invocation_protocol>` describes output key fields; but neither uses the canonical `<output>` body section tag.

4. **Four cited reference files do not exist in the repository:**
   - `skills/problem-solving/reference/ps-critic-tool-examples.md` — not found (glob search confirmed)
   - `skills/problem-solving/reference/ps-critic-scoring-rubric.md` — not found
   - `skills/problem-solving/reference/ps-critic-output-templates.md` — not found
   - `skills/problem-solving/reference/ps-critic-circuit-breaker.md` — not found

   These files are cited as containing: "Full scoring rubric, dimension tables, worked examples, and improvement feedback template" (scoring rubric); "Full invocation template, output level details, state schema, and summary table format" (output templates); "Full circuit breaker parameters, decision logic, worked workflow example" (circuit breaker); and "Full tool invocation examples and AST operations" (tool examples). Their absence means the agent's core scoring methodology, output format, and circuit breaker decision logic are inaccessible at runtime. An agent whose primary function is S-014 LLM-as-Judge scoring does not have its scoring rubric loaded.

**Gaps summary:**
- Missing canonical `<input>`, `<methodology>`, `<output>` XML body sections per agent-development-standards.md
- 4 referenced Tier 3 content files do not exist (scoring rubric, tool examples, output templates, circuit breaker)

**Improvement Path:**
Create the 4 referenced files in `skills/problem-solving/reference/`. Add `<input>`, `<methodology>`, and `<output>` XML sections using the canonical section tags per agent-development-standards.md. The scoring rubric file is the highest priority — without it the agent's primary task lacks executable guidance.

---

### Internal Consistency (0.85/1.00)

**Evidence:**
The following consistency checks pass across both files:

- **Tool tier vs tools declared:** T2 in governance.yaml matches .md frontmatter `tools: Read, Write, Edit, Glob, Grep`. T2 = Read-Only plus Write/Edit (Bash absent — consistent with a quality evaluation agent requiring no shell execution)
- **Cognitive mode:** `convergent` in governance.yaml is the correct mode per agent-development-standards.md mode selection table: "Analysis, evaluation, scoring, review" → convergent
- **Model selection:** `sonnet` in .md frontmatter matches AD-M-009: "balanced analysis, standard production tasks"
- **Output levels:** L0/L1/L2 in governance.yaml `output.levels` matches `<persona>` section audience mapping — consistent
- **Constitutional triplet:** P-003, P-020, P-022 present in governance.yaml `constitution.principles_applied` (lines 45, 49, 47)
- **Version alignment:** Both .md (line 144: "Agent Version: 2.3.0") and governance.yaml (line 5: "version: 2.3.0") agree — no unexplained version delta
- **Generator-critic role:** P-003 consequence in `<identity>` ("self-managed iteration violates P-003; orchestrator loses coordination authority") matches LOOP VIOLATION statement in `<capabilities>` — internally consistent
- **Score threshold:** `<evaluation_criteria_framework>` states >= 0.92 for C2+ (H-13); governance.yaml enforcement tier is "medium" which is consistent with C2 classification

**Gaps:**

1. **forbidden_actions format mismatch:** The `<capabilities>` section in the .md body (lines 69-73) uses NPT-009 format with full consequence chains: "P-003 VIOLATION: DO NOT spawn subagents or manage iteration loops. Consequence: self-managed iteration violates P-003 and the orchestrator loses coordination authority; unbounded recursion exhausts the context window." The governance.yaml `capabilities.forbidden_actions` (lines 85-91) uses legacy NPT-014 format (short descriptions): "Spawn recursive subagents (P-003)", "Override user decisions (P-020)". Per ADR-002 D-003, NPT-009-complete is the recommended format. The mismatch means the machine-readable governance file uses a weaker format than the human-readable body.

2. **Score band label divergence:** The agent's internal bands (EXCELLENT, GOOD, ACCEPTABLE, NEEDS_WORK, POOR) differ from quality-enforcement.md operational bands (PASS, REVISE, REJECTED). The functional thresholds match (EXCELLENT >= 0.92 = PASS), but the label differences create minor inconsistency with the SSOT.

**Improvement Path:**
Update governance.yaml `capabilities.forbidden_actions` from NPT-014 to NPT-009 format with full consequence statements matching the .md body. Align score band labels with quality-enforcement.md SSOT terminology.

---

### Methodological Rigor (0.78/1.00)

**Evidence:**
The evaluation methodology present in the agent body:

- Cites the authoritative SSOT: "`.context/rules/quality-enforcement.md` (Quality Gate section) defines authoritative dimensions and weights for C2+ deliverables"
- States the correct score formula: `quality_score = Σ(criterion_score × criterion_weight)`
- Specifies the C2+ threshold (>= 0.92, H-13) with explicit rule citation
- Defines a three-tier criteria hierarchy: SSOT 6-dimension (C2+) → legacy 5-dimension (C1) → custom criteria (when provided in invocation)
- Specifies what each improvement area MUST contain: criterion affected, current/target score, priority, gap description with evidence, actionable recommendation, expected impact — 6 required fields
- Declares mandatory persistence (P-002) with a specific path pattern and link requirement
- States output format requirements: three levels (L0/L1/L2) plus Critique Summary Table
- Circuit breaker guidance correctly states P-003 compliance: orchestrator applies logic, ps-critic does not; summarizes parameters (min 3 iterations per H-14, 0.92 threshold per H-13, max 5 iterations, 2% improvement threshold)

**Gaps:**

1. **Scoring rubric deferred to non-existent file:** "Full scoring rubric, dimension tables, worked examples, and improvement feedback template: See `skills/problem-solving/reference/ps-critic-scoring-rubric.md`." This file does not exist. The agent describes that it should apply a rubric but the rubric itself is not loadable. Per agent-development-standards.md, Tier 3 content (reference files) must exist to be effective — deferrals to non-existent files are not equivalent to the content.

2. **Circuit breaker parameters deferred to non-existent file:** "Full circuit breaker parameters, decision logic, worked workflow example, complete invocation example, and post-completion verification: See `skills/problem-solving/reference/ps-critic-circuit-breaker.md`." The summary in the body provides the thresholds but not the decision logic or worked examples.

3. **Output template deferred to non-existent file:** "Full invocation template, output level details, state schema, and summary table format: See `skills/problem-solving/reference/ps-critic-output-templates.md`." Without this file, correct output format cannot be verified.

4. **No self-review step articulated:** The agent describes the evaluation process but does not include a description of how it applies H-15 (self-review of its own critique output before persisting). An agent reviewing others' work should articulate its own self-review step.

5. **No step-by-step evaluation workflow:** The methodology is described at the conceptual level (score formula, threshold, criteria hierarchy) but no procedural step-by-step workflow specifies how the agent actually conducts an evaluation from artifact read to final output. This is deferred to the non-existent rubric and output template files.

**Improvement Path:**
Create `ps-critic-scoring-rubric.md` with 6-dimension rubric tables and worked examples. Create `ps-critic-output-templates.md` with L0/L1/L2 format and critique summary table. Create `ps-critic-circuit-breaker.md` with decision logic. Add a self-review step. Add a procedural evaluation workflow (inline or as a reference).

---

### Evidence Quality (0.80/1.00)

**Evidence:**
The deliverable provides the following evidence anchors:

- **4 credible prior_art citations in governance.yaml** with URLs: Anthropic Constitutional AI (foundational source for constitutional principle design), OpenAI Agent Guide (reflective loops), Google ADK Multi-Agent Patterns, and Madaan et al. 2023 Self-Refine paper (directly relevant to iterative refinement role)
- **SSOT reference by path:** `.context/rules/quality-enforcement.md` cited as authoritative for quality dimensions and weights
- **HARD rule citations by ID:** H-13 (0.92 threshold), H-14 (minimum 3 iterations) cited in circuit breaker guidance
- **Constitutional principle IDs** cited throughout: P-003, P-020, P-022, P-002, P-004, P-011
- **Enhancement provenance:** EN-707 cited with description of what it added ("Integrated adversarial quality modes S-014, S-003, S-002, S-004, S-013, S-001, S-007, S-012, S-011; aligned thresholds with SSOT")
- **Score formula** is mathematical and verifiable
- **Output path pattern** is specific: `projects/${JERRY_PROJECT}/critiques/{ps_id}-{entry_id}-iter{iteration}-critique.md`
- **Governance schema reference:** `docs/schemas/agent-governance-v1.schema.json` cited

**Gaps:**

1. **No ADR citation:** Design decisions (T2 tier requiring write access, sonnet model selection, the three-tier criteria hierarchy) are not traced to any Architecture Decision Record.

2. **Prior_art not surfaced in .md body:** The 4 credible citations are in the governance.yaml `prior_art` section, which is a machine-readable governance file — not the agent body. The agent reasoning context (the .md body) has no citations for why the generator-critic pattern or S-014 methodology were chosen.

3. **No work item linkage:** No reference to the PROJ-035 optimization work, nor to the original creation work item. The EN-707 enhancement is cited but EN-707 is not linked to any accessible reference.

4. **Reference file citations are dangling:** The 4 reference files are asserted to contain essential content but the content does not exist, meaning evidence for the scoring rubric, output format, and circuit breaker design is entirely absent.

**Improvement Path:**
Add an ADR or inline rationale in the .md body for T2 tier and sonnet model selection. Surface 1-2 prior_art citations inline in the methodology sections. Add a Provenance note linking to PROJ-035.

---

### Actionability (0.80/1.00)

**Evidence:**
The following actionable content is present:

- **Required invocation fields** enumerated: PS ID, Entry ID, Iteration (1-based), Artifact path, Generator agent name, Evaluation criteria, Target score, Max iterations — all context a caller must supply
- **Persistence path pattern** specified: `projects/${JERRY_PROJECT}/critiques/{ps_id}-{entry_id}-iter{iteration}-critique.md` — unambiguous
- **Output key schema** defined: `critic_output` with 10 fields (ps_id, entry_id, iteration, artifact_path, quality_score, assessment, threshold_met, recommendation, improvement_areas, next_agent_hint)
- **Routing** defined: upstream (ps-architect, ps-researcher, ps-analyst) and downstream (MAIN CONTEXT) explicit
- **Fallback behavior** defined: 4 steps for incomplete evaluation (ACKNOWLEDGE, DOCUMENT, REQUEST, DO NOT score without criteria)
- **Post-completion checks** in governance.yaml (5 verifiable checks): verify_file_created, verify_artifact_linked, verify_l0_l1_l2_present, verify_quality_score_present, verify_improvement_recommendations
- **Session context on_receive** protocol: 5 steps defined (validate_session_id, check_schema_version, extract_artifact, extract_criteria, extract_iteration)
- **Session context on_send** protocol: 5 steps defined (populate_quality_score, populate_improvement_areas, calculate_threshold_met, list_artifacts, set_timestamp)

**Gaps:**

1. **Output format template deferred to non-existent file:** "Full invocation template, output level details, state schema, and summary table format: See ps-critic-output-templates.md." An orchestrator invoking ps-critic cannot determine the exact critique output format without this file.

2. **No worked invocation example inline:** The agent body provides no complete worked example of a ps-critic invocation (input PS CONTEXT + expected critic_output shape). Unlike nse-reporter which provides 5 concrete activation examples, ps-critic provides none inline. All examples are deferred to non-existent reference files.

3. **Improvement area format specified but not exemplified:** The 6 required fields for each improvement area are listed, but without a worked example the caller cannot verify what a compliant improvement area looks like in practice.

4. **Circuit breaker summary lacks edge cases:** The summary (max 5 iterations, 2% improvement threshold, escalate after max) covers the happy path but defers edge-case handling to the non-existent circuit breaker file.

**Improvement Path:**
Add 2-3 inline invocation examples in the `<invocation_protocol>` section. Add an inline worked example of a complete improvement area entry. Add at least one inline example of a properly formatted critique summary table entry.

---

### Traceability (0.75/1.00)

**Evidence:**
Traceable items present:

- Version 2.3.0 consistently declared in both .md footer (line 144) and governance.yaml (line 5)
- Last Updated: 2026-02-14 in .md footer
- Created: 2026-01-11 in .md footer
- EN-707 enhancement cited with description of changes
- SSOT path cited by exact repository-relative path
- Constitutional principle IDs cited (P-001 through P-022 range)
- HARD rules cited by ID (H-13, H-14 referenced in circuit breaker guidance)
- Governance schema reference: `docs/schemas/agent-governance-v1.schema.json`
- Template reference: `templates/critique.md` in governance.yaml
- Prior art URLs in governance.yaml (4 entries with full URLs)
- Output file pattern is specific and traceable

**Gaps:**

1. **No PROJ-035 work item linkage:** The optimization (Pattern A removal per PROJ-035) is not referenced in the agent definition. A reader cannot determine from the file when or why the optimization occurred or which content was removed.

2. **No parent work item:** No Epic, Feature, or Enabler ID links this agent to its creation work item.

3. **Four reference file paths are dangling:** `skills/problem-solving/reference/ps-critic-tool-examples.md`, `ps-critic-scoring-rubric.md`, `ps-critic-output-templates.md`, `ps-critic-circuit-breaker.md` — all cited, none resolvable. Dangling references break the traceability chain for the agent's core methodology.

4. **No ADR citation:** No Architecture Decision Record is referenced for the design decisions that produced this agent definition.

5. **governance.yaml `fallback_behavior: warn_and_request_criteria`** is not in the standard values defined in agent-development-standards.md (`warn_and_retry`, `escalate_to_user`, `persist_and_halt`). The use of a domain-specific value is permitted but no documentation explains the deviation.

**Improvement Path:**
Add a Provenance section citing PROJ-035 as the optimization origin. Add a References comment in the .md body cross-referencing the governance.yaml companion file. Document the `warn_and_request_criteria` fallback deviation. Resolve the 4 dangling reference paths by creating the files.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Completeness | 0.70 | 0.82 | Create `skills/problem-solving/reference/ps-critic-scoring-rubric.md` with the 6-dimension rubric tables (per-score-band criteria for 0.9+, 0.7-0.89, 0.5-0.69, <0.5 per each of 6 dimensions), worked scoring examples, and improvement area template |
| 2 | Completeness | 0.70 | 0.82 | Create `skills/problem-solving/reference/ps-critic-output-templates.md` with L0/L1/L2 critique format templates, critique summary table format, and state schema |
| 3 | Methodological Rigor | 0.78 | 0.87 | Create `skills/problem-solving/reference/ps-critic-circuit-breaker.md` with full circuit breaker parameters, decision logic table (conditional pseudocode), and worked workflow example showing 3 iterations |
| 4 | Completeness | 0.70 | 0.82 | Add canonical `<input>`, `<methodology>`, and `<output>` XML sections per agent-development-standards.md Markdown Body Sections table, replacing or supplementing the current custom section tags |
| 5 | Actionability | 0.80 | 0.87 | Add 2-3 concrete inline invocation examples in `<invocation_protocol>` showing a complete PS CONTEXT block and expected `critic_output` schema |
| 6 | Internal Consistency | 0.85 | 0.90 | Update governance.yaml `capabilities.forbidden_actions` from NPT-014 to NPT-009 format per ADR-002 D-003 |
| 7 | Traceability | 0.75 | 0.83 | Add a Provenance comment citing PROJ-035-skill-optimization as the optimization origin (e.g., `*Optimized: 2026-03-03 per PROJ-035 Phase 2 Pattern A removal*`) |
| 8 | Evidence Quality | 0.80 | 0.85 | Add ADR citation or inline rationale for T2 tier selection (write access requires justification) and sonnet model selection |

## Regression Assessment (PROJ-035 Verification)

The following key behavioral properties were verified to be PRESERVED after the Pattern A optimization:

| Verification Criterion | Status | Evidence |
|------------------------|--------|---------|
| Identity section complete | PASS | `<identity>` with role, expertise (5 items), cognitive mode, Belbin role, agent distinctions, P-003 consequence all present (lines 10-39) |
| Constitutional compliance (P-003, P-020, P-022) | PASS | All three in governance.yaml `constitution.principles_applied` (lines 45, 49, 47); all three with NPT-009 consequence statements in `<capabilities>` forbidden actions (lines 69-73) |
| Tool capabilities intact | PASS | `tools: Read, Write, Edit, Glob, Grep` in frontmatter; T2 tier in governance.yaml; tool table with purpose and usage pattern in capabilities section |
| Guardrails intact | PASS | Input validation patterns (ps_id, entry_id, artifact, criteria, iteration), output filtering (3 rules), fallback behavior (4 steps) all present |
| Quality threshold and SSOT reference | PASS | >= 0.92 threshold (H-13), SSOT path, score formula, score bands all present in evaluation_criteria_framework |
| Generator-critic role and P-003 compliance | PASS | Orchestrator manages loop; ps-critic evaluates per iteration; explicit P-003 consequence for self-managing; consistent across identity and capabilities sections |
| Output persistence requirement | PASS | P-002 MANDATORY PERSISTENCE explicitly required with path pattern |
| Invocation protocol fields | PASS | All required PS CONTEXT fields listed; upstream/downstream routing defined; output key schema defined |
| Post-completion checks | PASS | 5 verifiable checks in governance.yaml validation section |
| Session context on_receive/on_send | PASS | Both protocols defined in governance.yaml session_context section |

**Regression verdict: No behavioral regression detected.** The Pattern A removal did not strip any essential behavioral content. The score (0.78) reflects pre-existing structural gaps (non-canonical XML sections, non-existent reference files, legacy NPT-014 format in governance.yaml) that were present before the optimization and are not a result of Pattern A removal. The optimization is sound.

## Leniency Bias Check
- [x] Each dimension scored independently
- [x] Evidence documented for each score
- [x] Uncertain scores resolved downward (Completeness: 0.70 not 0.72 — missing reference files are critical for a scoring agent; Traceability: 0.75 not 0.78 — 4 dangling paths are meaningful)
- [x] First-draft calibration considered (this is a v2.3.0 post-optimization agent, calibrated for a mature deliverable; first-draft band of 0.65-0.80 is appropriate)
- [x] No dimension scored above 0.95 without exceptional evidence (highest is Internal Consistency at 0.85)

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.781
threshold: 0.92
weakest_dimension: Completeness
weakest_score: 0.70
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Create skills/problem-solving/reference/ps-critic-scoring-rubric.md with 6-dimension rubric tables and worked examples"
  - "Create skills/problem-solving/reference/ps-critic-output-templates.md with L0/L1/L2 critique format templates"
  - "Create skills/problem-solving/reference/ps-critic-circuit-breaker.md with decision logic and worked workflow"
  - "Add canonical <input>, <methodology>, <output> XML sections per agent-development-standards.md"
  - "Add 2-3 inline invocation examples in <invocation_protocol>"
  - "Update governance.yaml forbidden_actions from NPT-014 to NPT-009 format"
  - "Add PROJ-035 provenance comment to .md footer"
  - "Add ADR citation for T2 tier and sonnet model selection"
```

---

*Score Version: 2.0 (supersedes prior entry assessing ps-critic.prompt.md composition file)*
*Scoring Agent: adv-scorer*
*Strategy: S-014 (LLM-as-Judge)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Deliverable: `skills/problem-solving/agents/ps-critic.md` + `skills/problem-solving/agents/ps-critic.governance.yaml`*
*Scored: 2026-03-03*
