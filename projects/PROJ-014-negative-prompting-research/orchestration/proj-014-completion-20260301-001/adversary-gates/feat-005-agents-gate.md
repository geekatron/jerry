# Quality Score Report: FEAT-005 Agent Definitions (pe-builder, pe-constraint-gen, pe-scorer)

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Score, verdict, top action |
| [Scoring Context](#scoring-context) | Deliverable metadata |
| [Score Summary](#score-summary) | Dimension scores and composite |
| [Dimension Scores](#dimension-scores) | Weighted scores table |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Per-dimension evidence and gaps |
| [Improvement Recommendations](#improvement-recommendations) | Priority-ordered action items |
| [Leniency Bias Check](#leniency-bias-check) | Anti-leniency verification |

---

## L0 Executive Summary

**Score:** 0.879/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Completeness (0.84)
**One-line assessment:** Six agent definition files demonstrate strong structural compliance with H-34/H-35 and excellent NPT-009 formatting, but a confirmed XML nesting defect in pe-builder.md (guardrails and p003_self_check incorrectly nested inside the output section), the absence of the recommended enforcement field in all three governance YAMLs, and missing explicit model-selection rationale documentation prevent this deliverable from reaching the C4 threshold of 0.95.

---

## Scoring Context

- **Deliverable:** 6 files across `skills/prompt-engineering/agents/` (pe-builder.md, pe-builder.governance.yaml, pe-constraint-gen.md, pe-constraint-gen.governance.yaml, pe-scorer.md, pe-scorer.governance.yaml)
- **Deliverable Type:** Agent Definition (6-file set)
- **Criticality Level:** C4 (applied per user-specified gate — architecture/governance artifacts)
- **Quality Threshold Applied:** 0.95 (user-specified C4 gate; SSOT minimum is 0.92)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`, `.context/rules/agent-development-standards.md`, `docs/schemas/agent-governance-v1.schema.json`
- **Scored:** 2026-03-01T00:00:00Z
- **Iteration:** 1 of max 5

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.879 |
| **C4 Threshold (user-specified)** | 0.95 |
| **SSOT Minimum Threshold (H-13)** | 0.92 |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (standalone scoring) |
| **Gap to C4 Threshold** | -0.071 |
| **Gap to SSOT Threshold** | -0.041 |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.84 | 0.168 | XML nesting defect in pe-builder.md; all H-34/H-35 required fields present across all 6 files |
| Internal Consistency | 0.20 | 0.88 | 0.176 | Strong cross-file alignment; pe-builder XML nesting deviates from agent-development-standards.md section architecture |
| Methodological Rigor | 0.20 | 0.90 | 0.180 | All schema required fields present; appropriate tier/mode/model selection; missing enforcement field (recommended) |
| Evidence Quality | 0.15 | 0.87 | 0.1305 | Specific SSOT citations throughout; model selection rationale not explicitly documented in governance YAMLs |
| Actionability | 0.15 | 0.91 | 0.1365 | Highly actionable methodology in all three agents; T1 inline-output persistence responsibility for pe-scorer implicit but undocumented |
| Traceability | 0.10 | 0.88 | 0.088 | Full constitutional cross-reference chain; missing enforcement field breaks quality tier traceability; PROJ-014 finding reference lacks document path |
| **TOTAL** | **1.00** | | **0.879** | |

---

## Detailed Dimension Analysis

### Completeness (0.84/1.00)

**Evidence:**

Strengths (present and correct):
- Dual-file architecture (H-34): All 3 agents have `.md` + `.governance.yaml` pairs. Confirmed.
- Official frontmatter fields only: pe-builder.md uses `name`, `description`, `model`, `tools` — all 4 are official Claude Code fields. pe-constraint-gen.md same. pe-scorer.md same. No unofficial fields in `.md` frontmatter.
- H-34 required governance fields: `version` (pattern `^\d+\.\d+\.\d+$`), `tool_tier` (enum T1-T5), `identity.role`, `identity.expertise` (minItems:2), `identity.cognitive_mode` (enum) — all present in all 3 governance YAMLs.
- H-35 Task tool excluded: pe-builder.md tools list = `Read, Write, Edit, Glob, Grep` (no Task). pe-constraint-gen.md same. pe-scorer.md = `Read, Glob, Grep` (no Task). Confirmed worker compliance.
- H-35 constitutional triplet: P-003, P-020, P-022 present in `constitution.principles_applied` for all three. Confirmed.
- H-35 minimum 3 forbidden_actions: pe-builder=5 entries, pe-constraint-gen=6 entries, pe-scorer=5 entries. All exceed minimum.
- NPT-009 format: All forbidden_actions entries use `{PRINCIPLE} VIOLATION: NEVER {action} -- Consequence: {impact}` structure. `forbidden_action_format: NPT-009-complete` declared explicitly.
- Tool tier compliance: pe-builder=T2 (produces file artifacts via Write/Edit), pe-constraint-gen=T2 (produces file artifacts), pe-scorer=T1 (read-only evaluation). All match specification.
- Cognitive mode: pe-builder=integrative, pe-constraint-gen=systematic, pe-scorer=convergent. All match specification.
- Model selection: pe-builder=opus, pe-constraint-gen=sonnet, pe-scorer=haiku. All match specification.
- 7 XML-tagged sections: pe-builder and pe-constraint-gen have identity, purpose, input, capabilities, methodology, output, guardrails, p003_self_check (8 sections including p003_self_check). pe-scorer adds scoring_rubric and anti_pattern_detection as domain-specific extensions. Required sections present.
- schema.guardrails.fallback_behavior: `warn_and_retry` in all three — matches `^[a-z_]+$` pattern.
- schema.constitution.principles_applied: minItems:3 met (all have 4 entries).

**Gaps:**

1. **XML nesting defect in pe-builder.md (STRUCTURAL):** The `<output>` section opens at line 144 and does NOT close before `<guardrails>` opens at line 187. The `<p003_self_check>` section also appears nested inside the unclosed `<output>` tag. The final `</output>` at line 235 is the only closing tag, meaning `<guardrails>` and `<p003_self_check>` are sibling-or-child nodes of `<output>` rather than top-level siblings. Per agent-development-standards.md (Markdown Body Sections table), all 7 section tags are defined as top-level siblings, each mapping to a distinct hexagonal architecture layer. This nesting deviation means pe-builder's guardrails and P-003 runtime check are structurally misclassified as output content.

2. **Missing `enforcement` field in all 3 governance YAMLs:** AD-M-008 states agents "SHOULD declare `validation.post_completion_checks`" (present) but the `enforcement` object (`tier`, `escalation_path`) is also listed as a "Recommended field" in the agent-definition-schema table. None of the three governance YAMLs declare this field. While optional per schema, it is recommended and its absence means quality tier traceability is incomplete.

3. **pe-scorer `output.required: false` without `location`:** Technically correct (schema `if/then` only requires `location` when `required: true`), and deliberately designed for T1 inline return. However, AD-M-004 says agents producing stakeholder-facing deliverables "SHOULD declare all three output levels (L0, L1, L2)." pe-scorer declares `levels: [L0, L1]` only — missing L2. Minor gap.

**Improvement Path:**

- Fix `</output>` nesting in pe-builder.md: Close `<output>` at line ~185, then have `<guardrails>` and `<p003_self_check>` as top-level siblings.
- Add `enforcement` block to all 3 governance YAMLs (e.g., `enforcement: { tier: hard, escalation_path: quality-gate }`)
- Add `L2` to pe-scorer output.levels if strategic implications are applicable for the scorer's audience.

---

### Internal Consistency (0.88/1.00)

**Evidence:**

Strengths:
- pe-builder: cognitive_mode=integrative declared in both `.md` identity section and `.governance.yaml`. Model=opus in both. Tool list (Read, Write, Edit, Glob, Grep) matches T2 tier declaration. Constitutional compliance table in `<guardrails>` lists P-002, P-003, P-020, P-022 — exactly matching the 4 entries in `constitution.principles_applied` YAML.
- pe-constraint-gen: cognitive_mode=systematic everywhere. Model=sonnet. output.levels=[L1] in YAML; markdown body output section shows a flat "# Generated Constraints" format without L0 summary. Consistent — no L0 claimed, no L0 produced.
- pe-scorer: T1 declared in YAML, enforced by tools list (Read, Glob, Grep only), confirmed in `<output>` body ("This agent is read-only (T1). The score report is returned inline to the orchestrator."). output.required=false. Fully consistent across all surfaces.
- Cross-agent consistency: All three use identical text for the base 3 constitutional forbidden actions. This ensures governance homogeneity across the skill.
- The 7-criterion rubric embedded in pe-scorer's `<scoring_rubric>` section matches the structure from `.context/rules/prompt-quality.md` (the SSOT), with all 7 criteria, weights, and score levels accurately reproduced.

**Gaps:**

1. **pe-builder.md XML nesting inconsistency with standards:** The agent-development-standards.md Markdown Body Sections table defines 7 sections as distinct top-level XML-tagged regions each mapping to a specific hexagonal layer. pe-builder's structure deviates by leaving `<guardrails>` and `<p003_self_check>` inside an unclosed `<output>` section. This is inconsistent with the published standard for how agent markdown bodies should be organized, and inconsistent with pe-constraint-gen and pe-scorer (which correctly have separate top-level sections).

2. **pe-builder output section scope ambiguity:** The `<output>` section in pe-builder (line 144) includes the Output Format specification AND (due to nesting) the Guardrails content. The guardrails content at line 187+ covers Input Validation, Output Filtering, Failure Modes, and Constitutional Compliance — these belong to the Domain layer (guardrails), not the Adapter (outbound) layer. Having them nested under `<output>` mixes hexagonal architecture layers.

**Improvement Path:**

- Close `<output>` after the output format specification (approximately line 185). Open `<guardrails>` as a new top-level sibling. Open `<p003_self_check>` as a new top-level sibling after `</guardrails>`.

---

### Methodological Rigor (0.90/1.00)

**Evidence:**

Strengths:
- pe-builder: 6-step numbered methodology referencing specific source files at each step. Step 2 provides per-element decision criteria. Step 3 distinguishes NPT-009 vs NPT-013 selection. Step 5 embeds H-15 self-review with all 7 criteria explicitly listed. Step 6 specifies L0 and L1 output levels. Rigorous and complete.
- pe-constraint-gen: 7-step methodology with anti-pattern examples at Step 4 ("Too vague: 'bad things happen' -> Instead: 'downstream agents build analysis on nonexistent evidence'"). Binary-testable criterion defined ("Specific enough that compliance is binary"). Decision table for NPT-009 vs NPT-013 selection. Step 7 includes 6-point self-review checklist. Rigorous.
- pe-scorer: leniency counteraction explicitly instructed in methodology ("When uncertain between adjacent scores, choose the LOWER one. This is critical — casual prompts routinely score 30-50, not 60-70."). Step 6 prioritizes improvement suggestions by weight ("C1 and C2 first — they account for 38% of total score"). Step 7 includes 6-point pre-delivery self-review.
- Schema required field compliance: All 3 governance YAMLs pass `version`, `tool_tier`, `identity.role`, `identity.expertise` (minItems:2), `identity.cognitive_mode` schema validation.
- Tool tier selection justification traceable: T1 for pe-scorer (read-only evaluation — no artifact production), T2 for pe-builder and pe-constraint-gen (produce file artifacts). Matches "Select the lowest tier satisfying requirements" guideline.
- Cognitive mode-to-design alignment: integrative/opus for pe-builder (cross-source synthesis of user intent + templates), systematic/sonnet for pe-constraint-gen (procedural step-by-step), convergent/haiku for pe-scorer (focused evaluation to a score). Matches the Cognitive Mode Taxonomy table in agent-development-standards.md.

**Gaps:**

1. **Missing `enforcement` field in all 3 governance YAMLs:** The Recommended Fields table in agent-development-standards.md lists `enforcement` (with `tier` and `escalation_path`) as a recommended governance field. Its absence means there is no machine-readable declaration of which quality tier (hard/medium/soft) governs each agent, and no documented escalation path. For C4 deliverables, this is a significant omission — the enforcement tier should be `hard` for worker agents in a C4-critical skill.

2. **AD-M-009 model selection not explicitly justified in governance:** AD-M-009 states "Agent model selection SHOULD be justified per cognitive demands." The standard provides a mapping table (opus=complex reasoning, sonnet=balanced, haiku=fast repetitive). All three agents select the correct model per this table, but the governance YAMLs contain no documentation of the selection rationale. A reviewer must infer correctness from the cognitive_mode field rather than reading an explicit justification.

3. **pe-builder.md XML structure deviation:** Per agent-development-standards.md "Hexagonal dependency rule," domain-layer sections (`<guardrails>`) MUST NOT be nested within adapter-layer sections (`<output>`). The current nesting violates this architectural rule.

**Improvement Path:**

- Add `enforcement: { tier: hard, escalation_path: quality-gate }` to all 3 governance YAMLs.
- Add a `# Model Selection Rationale` comment in each governance YAML adjacent to the `identity.cognitive_mode` field.
- Fix pe-builder.md XML structure (as noted above).

---

### Evidence Quality (0.87/1.00)

**Evidence:**

Strengths:
- pe-builder references 3 specific codebase files with accurate paths: `.context/rules/prompt-templates.md`, `.context/rules/prompt-quality.md`, `.context/rules/mandatory-skill-usage.md`. All verified as real files in the repository.
- pe-constraint-gen references `skills/prompt-engineering/rules/npt-pattern-reference.md` and `docs/governance/JERRY_CONSTITUTION.md` — the latter is a confirmed real file. (npt-pattern-reference.md is a new file created as part of this project deliverable — confirmed path convention is correct.)
- pe-scorer's `<scoring_rubric>` section explicitly cites `.context/rules/prompt-quality.md` (The Quality Rubric section) as its SSOT, and the rubric content (7 criteria, weights, score levels) matches exactly what is in the loaded system context from that file.
- All governance YAMLs: `# Validated by: docs/schemas/agent-governance-v1.schema.json` header comment — schema file confirmed to exist at that path.
- pe-constraint-gen forbidden action: "...per PROJ-014 findings" — references the research project that produced NPT-013 pattern evidence.
- Constitutional principle references (P-003, P-020, P-022) trace to real principles documented in the Jerry Constitution.
- NPT pattern codes (NPT-009, NPT-013) are referenced in context of the pattern catalog that pe-constraint-gen and pe-builder cite.

**Gaps:**

1. **Model selection rationale not documented in governance files:** AD-M-009 SHOULD be met with documented justification. Three governance YAMLs declare `model: opus/sonnet/haiku` in the companion `.md` frontmatter but provide no evidence (in the YAML) for why that model was selected. The evidence exists in agent-development-standards.md (the mode-to-design table) but is not referenced.

2. **PROJ-014 findings reference lacks document path:** pe-constraint-gen's forbidden action states: "specific consequences produce measurably higher compliance per PROJ-014 findings." This is a research-backed claim, but the specific document path within PROJ-014 is not cited (e.g., `projects/PROJ-014-negative-prompting-research/research/...`). A reviewer cannot verify this claim without knowing which PROJ-014 artifact contains this evidence.

3. **pe-scorer outputs.required: false claims inline delivery** but provides no evidence (session_context protocol reference, handoff schema reference) explaining what "inline" means in the orchestrator-worker topology. This leaves the mechanism implicit.

**Improvement Path:**

- Add a comment in each governance YAML mapping cognitive_mode to the model selection rationale (e.g., `# integrative mode -> opus per agent-development-standards.md mode-to-design table`).
- Cite the specific PROJ-014 document supporting the compliance claim in pe-constraint-gen's forbidden action.
- Add a reference in pe-scorer's governance YAML or output section to the session_context protocol explaining inline delivery.

---

### Actionability (0.91/1.00)

**Evidence:**

Strengths:
- pe-builder: Users have a 6-step process with specific decision criteria at each step. The Template Quick-Select decision tree is reproduced as a bulleted list. Element selection has explicit threshold ranges (0.80-0.85 exploratory, 0.85-0.90 code review, 0.90-0.92 ADRs, 0.92-0.95 security). Output template is fully specified with placeholder variable names. Self-review score table is a concrete, computable checklist. Immediately usable.
- pe-constraint-gen: Binary-testability criterion ("compliance is binary — either you did or you did not") gives developers a concrete test for whether their NEVER statement is correct. Anti-patterns in consequence writing provide before/after examples ("Too vague: 'bad things happen' -> Instead: specific cascade"). The 7-step self-review checklist is a binary-verifiable pre-delivery gate. XML format examples for both YAML and markdown contexts are copy-paste ready.
- pe-scorer: Anti-pattern detection table includes specific detection signals for each AP (e.g., "No `/skill` syntax anywhere in prompt" for AP-01). Improvement suggestions are templated to include current score, target score, and specific action. Tier classification is unambiguous (score ranges with no overlap). The leniency counteraction instruction ("choose the LOWER one") is concrete and actionable.
- post_completion_checks in all governance YAMLs are machine-readable assertions that can be automated (verify_file_created, verify_five_elements_present, verify_composite_matches_sum).

**Gaps:**

1. **pe-scorer inline output responsibility not documented for orchestrators:** pe-scorer's `<output>` section states "the score report is returned inline to the orchestrator. If persistence is required, the orchestrator must use a T2+ agent or persist directly." This creates an actionability gap — what does the orchestrator need to do? There is no guidance on how to invoke pe-scorer in a way that captures its output (e.g., via Task tool, direct invocation). An orchestrator consuming pe-scorer results needs to know the handoff protocol.

2. **pe-builder failure mode for sub-75 self-review is underdefined:** Step 5 states "If any criterion scores below 2/3, revise before presenting." The methodology jumps from Step 5 (self-review) to Step 6 (present output) without specifying a maximum revision iteration count for the self-review loop, nor what happens if revision cannot raise the score above 75.

**Improvement Path:**

- Add a note in pe-scorer's `<output>` section: "When invoked via Task, the orchestrator captures the score report from the agent's response. When invoked directly, the score report is delivered inline. In both cases, if persistence is required, the calling context must use Write with T2 tools."
- Add to pe-builder Step 5: "Maximum 2 self-review iterations. If score remains below 75/100 after 2 iterations, present with the score and flag improvement areas in the Construction Notes section."

---

### Traceability (0.88/1.00)

**Evidence:**

Strengths:
- All 3 governance YAMLs: `# Validated by: docs/schemas/agent-governance-v1.schema.json` — full schema path cited, schema confirmed to exist.
- All 3 governance YAMLs: `# Runtime config: {agent}.md` — bidirectional cross-reference between companion files.
- All 3 governance YAMLs: `constitution.reference: docs/governance/JERRY_CONSTITUTION.md` — complete path.
- All 3 agent `.md` footers: `*Constitutional Compliance: Jerry Constitution v1.0*` and `*SSOT: ...*` with specific file paths.
- SSOT paths are distinct per agent: pe-builder cites prompt-quality.md + prompt-templates.md (correct — it uses both); pe-constraint-gen cites npt-pattern-reference.md (correct — constraint generation SSOT); pe-scorer cites prompt-quality.md (correct — scoring rubric SSOT).
- Forbidden action principle labels (P-003, P-020, P-022) are traceable to specific constitutional principles.
- `forbidden_action_format: NPT-009-complete` in all 3 provides format-level traceability to ADR-002 D-003 specification.
- pe-scorer `<scoring_rubric>` cites "(The Quality Rubric section)" — sub-section traceability.
- session_context.on_receive and on_send in all governance YAMLs provide input/output traceability for handoff protocol.

**Gaps:**

1. **Missing `enforcement` field breaks quality tier traceability:** Without `enforcement.tier` in the governance YAMLs, there is no machine-readable record of which quality tier governs these agents. An automated compliance check cannot confirm that these agents were reviewed at the C4 tier they are intended for.

2. **PROJ-014 citation in pe-constraint-gen lacks document path:** "per PROJ-014 findings" in the forbidden action does not cite a specific document path, making the claim unverifiable without manual project exploration.

3. **Schema validation claim is asserted, not verified:** The governance YAML header says "# Validated by: docs/schemas/agent-governance-v1.schema.json" but this is a documentation claim — no CI gate or pre-commit hook has been established to continuously enforce this. At C4 criticality, L5 (CI) verification should be in place. This is a gap in the enforcement chain.

**Improvement Path:**

- Add `enforcement: { tier: hard, escalation_path: quality-gate }` to all 3 governance YAMLs.
- Add specific document path to PROJ-014 citation in pe-constraint-gen forbidden action.
- Establish or confirm L5 CI gate validates governance YAMLs against the schema on commit.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Completeness | 0.84 | 0.90 | Fix pe-builder.md XML nesting: close `</output>` after line ~185 (end of output format template), then place `<guardrails>` and `<p003_self_check>` as top-level siblings. This eliminates the structural defect causing the lowest dimension score. |
| 2 | Completeness / Traceability / Methodological Rigor | — | — | Add `enforcement: { tier: hard, escalation_path: quality-gate }` block to all 3 governance YAMLs. This resolves the shared gap across 3 dimensions simultaneously. |
| 3 | Evidence Quality | 0.87 | 0.92 | Add `# Model selection rationale` comments in each governance YAML (e.g., `# integrative mode -> opus per agent-development-standards.md Cognitive Mode Taxonomy section`). Add specific PROJ-014 document path to pe-constraint-gen's vague research citation. |
| 4 | Actionability | 0.91 | 0.95 | Add explicit orchestrator consumption guidance to pe-scorer's `<output>` section: explain how inline output is received when invoked via Task vs. direct invocation. Add max-iteration bound (2 cycles) to pe-builder's Step 5 self-review failure path. |
| 5 | Internal Consistency | 0.88 | 0.93 | After fixing the XML nesting (Priority 1), confirm pe-builder's `<guardrails>` hexagonal layer classification matches the Domain layer assignment in agent-development-standards.md. |
| 6 | Completeness | 0.84 | 0.90 | Add `L2` to pe-scorer `output.levels` if strategic implications reporting is applicable, or document explicitly why L2 is not applicable for a read-only scorer. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing weighted composite
- [x] Evidence documented for each score with specific file line references and quoted content
- [x] Uncertain scores resolved downward (Completeness held at 0.84 despite only one structural defect; Methodological Rigor held at 0.90 despite overall strong methodology due to missing recommended field)
- [x] First-draft calibration considered (iteration 1 of max 5; score of 0.879 is consistent with strong first-draft range 0.80-0.90)
- [x] No dimension scored above 0.95 without exceptional evidence
- [x] XML nesting defect in pe-builder.md confirmed against actual file content (lines 144-235) before penalizing Completeness
- [x] C4 threshold (0.95) applied as user-specified; SSOT threshold (0.92) noted as secondary reference

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.879
threshold: 0.95
ssot_threshold: 0.92
weakest_dimension: Completeness
weakest_score: 0.84
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Fix pe-builder.md XML nesting: close </output> before <guardrails> opens"
  - "Add enforcement field to all 3 governance YAMLs"
  - "Add model selection rationale comments to governance YAMLs"
  - "Cite specific PROJ-014 document path in pe-constraint-gen forbidden action"
  - "Add pe-scorer orchestrator consumption guidance to <output> section"
  - "Add max-iteration bound to pe-builder Step 5 self-review failure path"
```

---

*Score Report Version: 1.0*
*Scoring Agent: adv-scorer*
*SSOT: `.context/rules/quality-enforcement.md`*
*Schema Reference: `docs/schemas/agent-governance-v1.schema.json`*
*Scored: 2026-03-01*
