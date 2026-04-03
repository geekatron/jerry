# Quality Score Report: STORY-017 Rule File Updates (Tier Model Renumbering)

## L0 Executive Summary

**Score:** 0.849/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.73)

**One-line assessment:** The tier renaming implementation is structurally sound and internally consistent, but fails the C4 quality gate (0.95) due to a factual error in T1 example agents (`adv-scorer` misclassified as T1 when the ADR's own migration table places it at T2), missing ADR traceability in the References section of all three files, and a modest actionability gap for eng-* skill authors.

---

## Scoring Context

- **Deliverable:** Three-file cohesive change set:
  - `.context/rules/agent-development-standards.md`
  - `.context/rules/mcp-tool-standards.md`
  - `docs/schemas/agent-governance-v1.schema.json`
- **Deliverable Type:** Analysis/Governance Rule Files
- **Criticality Level:** C4 (AE-002 auto-escalation: modifying `.context/rules/` files)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Custom Threshold:** 0.95 (C4 per ADR-STORY015-001 and STORY-017 AC)
- **Scored:** 2026-03-28T00:00:00Z
- **Iteration:** 1 (first score)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.849 |
| **C4 Threshold** | 0.95 (per STORY-017 AC, ADR-STORY015-001) |
| **Standard Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No — standalone scoring |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.88 | 0.176 | All 10 STORY-017 scope changes implemented; T1 example agent error is illustrative inaccuracy |
| Internal Consistency | 0.20 | 0.90 | 0.180 | Zero orphaned T3=External / T4=Persistent / T5=Full references; all cross-file references coherent |
| Methodological Rigor | 0.20 | 0.91 | 0.182 | Risk-ordering rationale explicit; eng-*/red-* exception documented in two files with mechanism |
| Evidence Quality | 0.15 | 0.73 | 0.110 | `adv-scorer` listed as T1 example agent; ADR migration table confirms adv-scorer is T2 |
| Actionability | 0.15 | 0.86 | 0.129 | T3/T4 boundary explicit; risk rationale present; eng-* exception requires footnote navigation |
| Traceability | 0.10 | 0.72 | 0.072 | ADR-STORY015-001 cited once (naming convention note) but absent from References in all 3 files |
| **TOTAL** | **1.00** | | **0.849** | |

---

## Detailed Dimension Analysis

### Completeness (0.88/1.00)

**Evidence (what was implemented):**

All changes specified in STORY-017 Scope are present in the deliverable:

1. Tool Security Tiers table: T3=Persistent (+MK), T4=External (+Web), T5=Orchestration. Lines 223-229 of agent-development-standards.md. Correct.
2. Selection Guidelines: Fully rewritten with five guidelines. Guideline 3 includes risk-ordering rationale ("Memory-Keeper (internal MCP, governed namespace) is lower-risk than web tools"). Naming convention note with ADR-STORY015-001 cross-reference. Line 233-239.
3. Tier Constraints table: Row updated from "T4+ agents" to "T3+ agents with Memory-Keeper MUST follow MCP key namespace." Line 246.
4. Cognitive Mode table: divergent = T4+, integrative = T2 or T3, forensic = T2 or T4. Lines 278-282.
5. Guardrail Selection table: "Research (divergent, T4)" replaces old "Research (divergent, T3)". Line 344.
6. L2-REINJECT comment: Updated to "T3=Persistent (+MK), T4=External (+Web, includes MK), T5=Orchestration (+Agent)". Line 7.
7. mcp-tool-standards.md MCP-M-001: Updated to reference "T4 (Persistent + External) agents" and "T3 (Persistent) agents". Line 43.
8. mcp-tool-standards.md eng-* exclusion note: "T4 (Persistent + External) under the new tier model but MUST NOT use Memory-Keeper." Line 174.
9. mcp-tool-standards.md red-* exclusion note: Parallel construction to eng-* note. Line 176.
10. docs/schemas/agent-governance-v1.schema.json tool_tier description: "T3=Persistent (+MK), T4=External (+Web, includes MK), T5=Orchestration (+Agent)". Line 17.

**Gaps:**

- The STORY-017 scope also specified "Changes are atomic: both files updated in the same commit" (eng-lead AC). The JSON schema (`docs/schemas/agent-governance-v1.schema.json`) is a third file; the AC mentions only two files. The schema change is present and correct but was not explicitly listed as atomic-with-the-rule-files in the AC. Not a scoring gap, but worth noting for commit strategy.
- T1 Example Agents: The tier table lists `adv-scorer` under T1 example agents. Per the ADR migration table (line 391-392: "adv-scorer | T2 | None"), adv-scorer is T2. This is a factual inaccuracy in illustrative content (not a missing requirement), but it means a reader consulting the table to understand tier assignment would receive incorrect information. The old table also had this error (system-context version: T1 = "adv-executor, adv-scorer, wt-auditor"); STORY-017 changed T1 examples to "adv-scorer, pe-scorer, wt-auditor" but did not correct the adv-scorer misclassification.

**Improvement Path:**

Replace `adv-scorer` in T1 example agents with an agent confirmed T1 by the ADR migration table (diataxis-classifier, diataxis-auditor, pe-scorer, sb-voice are all confirmed T1). Score would reach 0.93+.

---

### Internal Consistency (0.90/1.00)

**Evidence:**

Systematic scan for orphaned old-model references (T3=External, T4=Persistent, T5=Full):

- `grep "T3.*External|T4.*Persistent|T5.*Full"` on agent-development-standards.md: Zero matches in normative content. The only T3/T4/T5+Name occurrences are the new-model names (T3=Persistent, T4=External, T5=Orchestration).
- `grep "T3.*External|T4.*Persistent|T5.*Full"` on mcp-tool-standards.md: Zero matches.
- All three files agree on tier naming: T3=Persistent, T4=External (Short Name) / "Persistent + External" (Full Name), T5=Orchestration.
- Internal cross-references are consistent: Pattern 2 (line 189) "T5 (Orchestration) tier" — correct. Line 188 "declare only T1-T4 tier tools; the Agent tool is reserved for T5 orchestrator agents" — correct.
- "T4+ (external access + persistence)" in the cognitive mode table (line 278): The parenthetical is semantically accurate — T4 agents in the new model have both web access (External) and Memory-Keeper (inherited from T3). "Persistence" in this context means cross-session state, which T4+ includes. Technically sound.

**Gaps:**

- Line 278 "divergent | T4+ (external access + persistence)": A reader might misinterpret this as T4 being the first tier where persistence appears. T3 also has persistence. The label would be clearer as "T4+ (external + persistence)" or simply "T4+ (cumulative: MK + web)". This is a minor clarity issue, not a factual error.
- The "Orchestration (T3-T5)" row in Guardrail Selection (line 347): Under the new model, orchestration agents range from T3 (state only) to T5 (full delegation). The range T3-T5 is accurate.

**Improvement Path:**

Refine the cognitive mode table parenthetical from "T4+ (external access + persistence)" to "T4+ (external + persistence)" to avoid implying persistence begins at T4. Score would reach 0.93.

---

### Methodological Rigor (0.91/1.00)

**Evidence:**

The implementation follows the ADR's stated design principles with fidelity:

1. **Principle of least privilege preserved:** "Default to T1" is the first selection guideline. The T3/T4 progression is defined by capability need, not tier-number proximity.
2. **Risk ordering made explicit:** Guideline 3 states: "Memory-Keeper (internal MCP, governed namespace) is lower-risk than web tools (external network, arbitrary URLs); T3 before T4 reflects this risk ordering." This directly operationalizes ADR Force F-04.
3. **Short Name/Full Name convention:** Documented with ADR cross-reference. The T4 Short Name "External" (what's new at tier) vs. Full Name "Persistent + External" (cumulative) distinction is explained and cross-referenced to ADR-STORY015-001 DX Considerations. This addresses the DX risk F-001 identified in the ADR.
4. **eng-*/red-* exception governance mechanism explained:** Both mcp-tool-standards.md and agent-development-standards.md include the mechanism explanation: "The T4 tier permits MK as a ceiling; the `.md` frontmatter and this exclusion note prevent actual MK access." This is accurate and prevents a future agent author from misunderstanding why eng-* agents don't appear in the MK columns of the Agent Integration Matrix.
5. **Namespace constraint scoped precisely:** "T3+ agents with Memory-Keeper MUST follow MCP key namespace" is more precise than the old "T4+ agents MUST follow MCP key namespace" — it correctly identifies that the constraint applies to all agents using Memory-Keeper, regardless of whether they also have web tools.

**Gaps:**

- The Tier Constraints table still reads "T4+ agents MUST declare citation guardrails" (line 247). Under the new model, T4=External is where web tools enter. This is correct: T4 is the tier that introduces external data ingestion. However, the wording "T4+" covers T4 and T5 only. Since T3 (Persistent) agents have no web tools, there are no citation guardrail requirements at T3. This is methodologically correct and consistent with the new model.
- No explicit methodology note in the schema file explaining why the description was updated. Minor.

**Improvement Path:**

No substantive methodological changes needed. Score is at near-maximum for this dimension. Adding ADR-STORY015-001 to References (traceability improvement) would also raise rigor perception.

---

### Evidence Quality (0.73/1.00)

**Evidence:**

**Critical inaccuracy — T1 Example Agents:**

The tier table (line 225) lists T1 example agents as: `adv-scorer, pe-scorer, wt-auditor`.

The ADR migration table (ADR-STORY015-001, lines 391-392) explicitly classifies:
```
adv-scorer | T2 | None
adv-selector | T2 | None
```

This is confirmed by the ADR T2->T2 unchanged section (line 388-418) which lists adv-scorer under "28 agents staying at T2." The old version of agent-development-standards.md (system-context, pre-STORY-017) also listed adv-scorer in the T1 example column, which was the pre-existing error. STORY-017 changed the T1 examples but preserved the adv-scorer misclassification.

This matters for evidence quality because: (a) the tier table is the primary reference for agent authors classifying new agents; (b) an incorrect example in T1 contradicts the ADR that these changes implement; (c) the error could cause future agent authors to classify T2-equivalent agents as T1.

**Supporting evidence (accurate):**

- T2 examples: `ps-critic, wt-auditor, uc-author` — wt-auditor is confirmed T2 per ADR. ps-critic is confirmed T2 per ADR. uc-author is confirmed T2 per ADR.
- T3 examples: `ts-parser, ts-extractor` — these are the two agents that specifically motivated Option A per ADR. Perfect match.
- T4 examples: `ps-researcher, eng-architect, red-recon` — ps-researcher is confirmed T4 (T3->T4 per ADR). eng-architect is confirmed T4 (T3->T4 per ADR). red-recon is confirmed T4 (T3->T4 per ADR).
- T5 example: `ux-orchestrator` — confirmed T5 (T5->T5 per ADR).

**Gaps:**

- One confirmed factual error in T1 example agents (adv-scorer at T2, not T1).
- No other example agent inaccuracies found in T2-T5 rows.

**Improvement Path:**

Replace `adv-scorer` in T1 examples with a confirmed T1 agent: `diataxis-classifier`, `pe-scorer`, or `sb-voice`. Score would reach 0.88+.

---

### Actionability (0.86/1.00)

**Evidence:**

**Selection guidelines are actionable:**

- "Default to T1" — single clear instruction, no ambiguity.
- "T2 when the agent produces artifacts" — triggers on file output requirement.
- "T3 when cross-session persistence is needed" — triggers on memory requirement with examples (research caching, phase checkpointing, transcript persistence).
- "T4 when external information is needed" — triggers on web tool requirement; explicitly states "use T4 instead of T3" for the combinatorial case.
- "T5 requires explicit justification" — appropriate barrier for the highest tier.

**T3/T4 boundary:**

Explicitly stated: "If your agent also needs web tools, use T4 instead of T3 (T4 includes all T3 capabilities including Memory-Keeper)." This directly satisfies STORY-017 AC: "The T3/T4 boundary is explicit."

**Risk-ordering rationale:**

Present: "Memory-Keeper (internal MCP, governed namespace) is lower-risk than web tools (external network, arbitrary URLs); T3 before T4 reflects this risk ordering." Directly satisfies STORY-017 AC.

**Gaps:**

- **eng-*/red-* exception discoverability:** A new eng-* agent author reading only the tier table would see `eng-architect, red-recon` as T4 examples. They would read Guideline 4 and note "T4 agents MUST include citation guardrails." The eng-*/red-* exception (MUST NOT use Memory-Keeper) is in the footnote text of Guideline 4 (`eng-\* and red-\* agents are classified T4 but MUST NOT use Memory-Keeper`) and in mcp-tool-standards.md. However, it is not in the Tier Constraints table where it would be most visible as a constraint. An agent author who reads the tier table and selection guidelines sequentially will encounter the exception. An author who reads only the constraints table would miss it.
- The Guardrail Selection table "Orchestration (T3-T5)" (line 347) is correct but may confuse an author who sees T3 as "Persistent" and wonders how T3 orchestration agents differ from T4/T5. The T3 minimum for orchestration (needing only MK, not web) is a valid case that could use one sentence of clarification.

**Improvement Path:**

Add an eng-*/red-* constraint row to the Tier Constraints table: "eng-* and red-* agents classified T4 MUST NOT use Memory-Keeper; file-based persistence only (P-002)." Score would reach 0.91.

---

### Traceability (0.72/1.00)

**Evidence:**

**Present:**

- Naming convention note in Selection Guidelines: "See ADR-STORY015-001 [DX Considerations] for the naming framework." Single explicit ADR cross-reference.
- `tool_tier` description in JSON schema cites "agent-development-standards.md Tool Security Tiers" for the definition. Intra-framework traceability present.
- mcp-tool-standards.md References section: cites FEAT-028-mcp-tool-integration as source for MCP-001/MCP-002 HARD rules. No STORY-017 or ADR-STORY015-001 reference.
- L2-REINJECT comment does not carry a version or source attribution.

**Gaps:**

1. **ADR-STORY015-001 not in References section of agent-development-standards.md:** The References section (lines 441-448) lists ADR-PROJ007-001, Phase 3 Synthesis, V&V Plan, Integration Patterns, Barrier 3 Handoff, quality-enforcement.md, mandatory-skill-usage.md, mcp-tool-standards.md, agent-routing-standards.md. The ADR that drove the tier model change is not listed. This breaks the traceability chain: a reviewer asking "why does T3 mean Persistent?" must know to look at ADR-STORY015-001 rather than finding it cited in References.

2. **agent-development-standards.md version header not updated:** Line 3: `<!-- VERSION: 1.2.0 | DATE: 2026-02-22 | SOURCE: ADR-PROJ007-001, PROJ-007 Phase 3 Synthesis, V&V Plan, EN-003 | REVISION: EN-003 gap closures (ET-M-001 extended thinking, FC-M-001 fresh context review) -->`. The version and date were not incremented for STORY-017 changes. For a C4 governance change, version provenance should be updated (e.g., VERSION: 1.3.0 | DATE: 2026-03-28 | REVISION: STORY-017 tier renumbering per ADR-STORY015-001).

3. **mcp-tool-standards.md version header shows 1.3.1 / 2026-02-20:** No update for STORY-017 changes. The exclusion notes (lines 174, 176) are new content without attribution.

4. **JSON schema `$id` unchanged:** `"$id": "https://jerry-framework.dev/schemas/agent-governance/v1.0.0"` — the schema was modified but the ID version was not bumped. This is a traceability gap in schema versioning.

**Improvement Path:**

Add ADR-STORY015-001 to References in agent-development-standards.md. Bump version headers in all three files with STORY-017 revision notes. Score would reach 0.85.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.73 | 0.88 | Replace `adv-scorer` in T1 example agents with a confirmed T1 agent (diataxis-classifier, pe-scorer, or sb-voice). adv-scorer is T2 per ADR migration table. |
| 2 | Traceability | 0.72 | 0.85 | Add `ADR-STORY015-001` to References section in agent-development-standards.md. Bump version header in all 3 files: agent-development-standards.md -> 1.3.0 / 2026-03-28 / STORY-017 tier renumbering. Bump mcp-tool-standards.md to 1.4.0. Bump schema $id to v1.1.0. |
| 3 | Actionability | 0.86 | 0.91 | Add an eng-*/red-* explicit constraint row to the Tier Constraints table: "eng-* and red-* agents classified T4 MUST NOT use Memory-Keeper; file-based persistence per P-002." Currently this constraint lives only in prose (Selection Guideline 4 footnote and mcp-tool-standards.md). |
| 4 | Completeness | 0.88 | 0.93 | Review whether any Tier Constraint table rows need updating for mcp-tool-standards.md Change 1 (namespace constraint). Confirm the "T3 agents MUST follow the MCP key namespace" wording in Selection Guideline 3 covers the intent. |
| 5 | Internal Consistency | 0.90 | 0.93 | Refine cognitive mode table: "divergent | T4+ (external access + persistence)" — the parenthetical could be read as T4 introducing persistence. Consider "T4+ (cumulative: MK + web)" to align with the cumulative capability framing used throughout. |

---

## Gap Against C4 Threshold

The C4 threshold for this deliverable is 0.95 (per STORY-017 AC and ADR-STORY015-001). The composite score of 0.849 is 0.101 below the C4 threshold and 0.071 below the standard H-13 threshold of 0.92.

The primary blockers to threshold passage:

| Gap Item | Current Score Impact | Estimated Score After Fix |
|----------|---------------------|--------------------------|
| Fix P1 (adv-scorer T1 error) | EQ: 0.73 -> ~0.88 | +0.023 composite |
| Fix P2 (version headers + ADR Reference) | TR: 0.72 -> ~0.85 | +0.013 composite |
| Fix P3 (eng-*/red-* constraint row) | AC: 0.86 -> ~0.91 | +0.008 composite |
| Fix P5 (cognitive mode parenthetical) | IC: 0.90 -> ~0.93 | +0.006 composite |

Estimated score after P1-P4 fixes: ~0.849 + 0.044 = ~0.893 (approaching H-13 threshold but still below C4 threshold).

To reach 0.95 (C4 threshold), all five improvement recommendations must be addressed AND the fixes must also raise methodological rigor to ~0.95. The current methodological rigor (0.91) is the ceiling constraint for a C4 threshold.

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite computed
- [x] Evidence documented for each score with specific line references
- [x] Uncertain scores resolved downward: Evidence Quality borderline 0.73/0.75 -> took 0.73; Traceability borderline 0.72/0.75 -> took 0.72
- [x] C4 calibration applied: the deliverable is a first implementation pass (not 3+ iterations), so baseline expectation of 0.65-0.80; the 0.849 reflects genuinely strong work on the core renaming but with concrete correctible gaps
- [x] No dimension scored above 0.95 without exceptional evidence
- [x] The adv-scorer T1 error is not a minor stylistic issue — it is a factual contradiction between the tier table and the ADR that the tier table is meant to reflect; Evidence Quality penalty is justified

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.849
threshold: 0.95  # C4 per STORY-017 AC; H-13 standard is 0.92
weakest_dimension: Evidence Quality
weakest_score: 0.73
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Replace adv-scorer in T1 example agents with confirmed T1 agent (diataxis-classifier, pe-scorer, or sb-voice)"
  - "Add ADR-STORY015-001 to References in agent-development-standards.md; bump version headers in all 3 files"
  - "Add eng-*/red-* explicit Tier Constraints table row (MUST NOT use Memory-Keeper)"
  - "Verify completeness of mcp-tool-standards.md Change 1 scope"
  - "Refine divergent cognitive mode parenthetical to avoid implying persistence begins at T4"
```
