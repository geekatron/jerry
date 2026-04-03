# Quality Score Report: STORY-017 Rule File Updates (Iteration 2)

## L0 Executive Summary

**Score:** 0.869/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.83)

**One-line assessment:** Iteration 2 fixes the primary Evidence Quality defect (T1/T2 example agents now factually correct, ADR reference added) and scores +0.020 composite vs. iteration 1, but the incomplete version-header fix introduced a new internal contradiction (header says 1.2.0, footer says 1.3.0) that lowered Internal Consistency, and three iteration-1 recommendations remain unaddressed.

---

## Scoring Context

- **Deliverable:** Three-file cohesive change set:
  - `.context/rules/agent-development-standards.md`
  - `.context/rules/mcp-tool-standards.md`
  - `docs/schemas/agent-governance-v1.schema.json`
- **Deliverable Type:** Governance Rule Files
- **Criticality Level:** C4 (AE-002 auto-escalation: modifying `.context/rules/` files)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Custom Threshold:** 0.95 (C4 per ADR-STORY015-001 and STORY-017 AC)
- **Scored:** 2026-03-28T00:00:00Z
- **Iteration:** 2 (re-score after targeted revision)
- **Prior Score:** 0.849 (iteration 1)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.869 |
| **C4 Threshold** | 0.95 (per STORY-017 AC, ADR-STORY015-001) |
| **Standard Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Delta vs. Iteration 1** | +0.020 |
| **Strategy Findings Incorporated** | No — standalone scoring |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.90 | 0.180 | All 10 scope items implemented; T1/T2 examples corrected; eng-*/red-* constraint row still absent from Tier Constraints table |
| Internal Consistency | 0.20 | 0.83 | 0.166 | NEW DEFECT: header VERSION comment reads 1.2.0 while footer VERSION comment reads 1.3.0 — direct factual contradiction in same file |
| Methodological Rigor | 0.20 | 0.91 | 0.182 | Risk-ordering rationale intact; Short/Full Name convention documented; no methodology regressions |
| Evidence Quality | 0.15 | 0.88 | 0.132 | T1/T2 example agents verified against .governance.yaml files: pe-scorer=T1, diataxis-classifier=T1, sb-voice=T1, ps-critic=T2, adv-scorer=T2, uc-author=T2 — all correct; mcp-tool-standards.md and schema $id not version-bumped |
| Actionability | 0.15 | 0.86 | 0.129 | Unchanged from iteration 1; eng-*/red-* MUST NOT use MK constraint remains prose-only, absent from Tier Constraints table |
| Traceability | 0.10 | 0.80 | 0.080 | ADR-STORY015-001 added to References (positive); footer VERSION 1.3.0 with STORY-017 attribution (positive); header VERSION still 1.2.0 (contradiction); mcp-tool-standards.md header unchanged (1.3.1/2026-02-20); schema $id unchanged (v1.0.0) |
| **TOTAL** | **1.00** | | **0.869** | |

---

## Detailed Dimension Analysis

### Completeness (0.90/1.00)

**Evidence (improvements from iteration 1):**

The T1 example agent correction is confirmed complete. The iteration 2 tier table now reads:

```
| T1 | Read-Only    | ... | pe-scorer, diataxis-classifier, sb-voice    |
| T2 | Read-Write   | ... | ps-critic, adv-scorer, uc-author            |
```

This directly addresses the most-cited completeness/accuracy gap from iteration 1. The ADR-STORY015-001 reference row was added to the References section (line 453) with the correct absolute path. These are the two stated P1/P2 fixes, both verified implemented.

All 10 original STORY-017 scope items remain intact from iteration 1 (tier table names, selection guidelines, tier constraints MK namespace row, cognitive mode table, guardrail selection table, L2-REINJECT comment, mcp-tool-standards.md MCP-M-001, eng-*/red-* exclusion notes in mcp-tool-standards.md, schema `tool_tier` description).

**Gaps:**

- Iteration 1 recommendation P3 (eng-*/red-* explicit row in Tier Constraints table) not addressed. A new eng-* agent author reading the Tier Constraints table sequentially encounters no constraint about Memory-Keeper exclusion. The constraint exists in Selection Guideline 4 prose and in mcp-tool-standards.md, but the Tier Constraints table is the canonical single-view constraint reference for the tier model.
- Header VERSION comment inconsistency (see Internal Consistency) is a completeness gap in the provenance metadata, though it does not affect normative content.

**Improvement Path:**

Add a fourth row to the Tier Constraints table: "eng-* and red-* agents classified T4 MUST NOT use Memory-Keeper; file-based persistence per P-002 (P-002, mcp-tool-standards.md)." Score would reach 0.93.

---

### Internal Consistency (0.83/1.00)

**Evidence (new defect introduced in iteration 2):**

The version fix is incomplete. The file now contains two conflicting VERSION comments:

- **Line 3 (header):** `<!-- VERSION: 1.2.0 | DATE: 2026-02-22 | SOURCE: ADR-PROJ007-001, PROJ-007 Phase 3 Synthesis, V&V Plan, EN-003 | REVISION: EN-003 gap closures (ET-M-001 extended thinking, FC-M-001 fresh context review) -->`
- **Line 457 (footer):** `<!-- VERSION: 1.3.0 | DATE: 2026-03-28 | SOURCE: ADR-STORY015-001, STORY-017 | REVISION: STORY-017 tier model renumbering: T3=Persistent, T4=External, T5=Orchestration -->`

This is a direct factual contradiction. A reader scanning the header encounters 1.2.0/2026-02-22/EN-003. A reader scanning the footer encounters 1.3.0/2026-03-28/STORY-017. The two statements cannot both be true as the current version declaration. This was not present in iteration 1 (where only the header comment existed at 1.2.0 and no footer comment was present).

**Remaining evidence (unchanged from iteration 1):**

- Zero orphaned T3=External / T4=Persistent / T5=Full references in normative content — still holds.
- Cross-file naming consistency still intact (T3=Persistent, T4=External, T5=Orchestration in all three files).
- Line 278 parenthetical "T4+ (external access + persistence)" — still the minor clarity issue noted in iteration 1, unchanged.
- Line 347 "Orchestration (T3-T5)" — still accurate, unchanged.

**Gaps:**

The header/footer VERSION contradiction is the primary gap. It is the only substantive Internal Consistency defect present.

**Improvement Path:**

Update line 3 header comment to match the footer: `<!-- VERSION: 1.3.0 | DATE: 2026-03-28 | SOURCE: ADR-STORY015-001, STORY-017 | REVISION: STORY-017 tier model renumbering: T3=Persistent, T4=External, T5=Orchestration -->`. Score would reach 0.92.

---

### Methodological Rigor (0.91/1.00)

**Evidence:**

No changes to methodology sections in iteration 2. All evidence from iteration 1 holds:

1. Principle of least privilege: "Default to T1" remains first guideline.
2. Risk-ordering rationale: "Memory-Keeper (internal MCP, governed namespace) is lower-risk than web tools (external network, arbitrary URLs); T3 before T4 reflects this risk ordering."
3. Short Name/Full Name convention: documented at line 233 with ADR cross-reference.
4. eng-*/red-* exception mechanism explained in both files.
5. Namespace constraint scoped to "T3+ agents with Memory-Keeper" (precise).

**Gaps:**

Same as iteration 1: the JSON schema file carries no methodology note explaining the description update. Minor.

**Improvement Path:**

No substantive changes needed to reach 0.93. The ADR-STORY015-001 addition to References also raises methodological perception.

---

### Evidence Quality (0.88/1.00)

**Evidence (P1 fix verified):**

The T1 and T2 example agent corrections are verified against actual `.governance.yaml` files:

T1 examples — `pe-scorer, diataxis-classifier, sb-voice`:
- `skills/prompt-engineering/agents/pe-scorer.governance.yaml` line 6: `tool_tier: T1` — CONFIRMED
- `skills/diataxis/agents/diataxis-classifier.governance.yaml` line 2: `tool_tier: T1` — CONFIRMED
- `skills/saucer-boy/agents/sb-voice.governance.yaml` line 6: `tool_tier: T1` — CONFIRMED

T2 examples — `ps-critic, adv-scorer, uc-author`:
- `skills/problem-solving/agents/ps-critic.governance.yaml` line 6: `tool_tier: T2` — CONFIRMED
- `skills/adversary/agents/adv-scorer.governance.yaml` line 6: `tool_tier: T2` — CONFIRMED
- `skills/use-case/agents/uc-author.governance.yaml` line 7: `tool_tier: "T2"` — CONFIRMED

All six example agents are factually correct. The iteration 1 Critical finding (adv-scorer misclassified as T1) is resolved.

T3-T5 examples unchanged from iteration 1 and remain accurate:
- T3: ts-parser, ts-extractor (both T3 per ADR motivation)
- T4: ps-researcher, eng-architect, red-recon (all T4 per ADR migration table)
- T5: ux-orchestrator (T5 per governance file)

**Remaining gaps:**

- `mcp-tool-standards.md` header VERSION comment not updated (still `1.3.1 | DATE: 2026-02-20`) despite receiving new STORY-017 content in iteration 1 (eng-*/red-* exclusion notes, lines 174 and 176). These notes are new additions from STORY-017 but carry no version attribution.
- `docs/schemas/agent-governance-v1.schema.json` `$id` unchanged: `"$id": "https://jerry-framework.dev/schemas/agent-governance/v1.0.0"`. The `tool_tier` enum description was modified for STORY-017 but the schema $id was not bumped. This is a provenance gap for schema consumers relying on the $id for version detection.
- The header VERSION contradiction (1.2.0 vs 1.3.0) in agent-development-standards.md weakens provenance evidence, though it is a consistency defect rather than a factual accuracy defect.

**Improvement Path:**

Bump mcp-tool-standards.md version to 1.4.0 with STORY-017 notation. Bump schema $id to v1.1.0. Resolve the header VERSION contradiction. Score would reach 0.93.

---

### Actionability (0.86/1.00)

**Evidence:**

No changes to actionability-relevant content in iteration 2. Evidence from iteration 1 holds:

- Five selection guidelines clear and sequentially deterministic.
- T3/T4 boundary explicitly stated: "If your agent also needs web tools, use T4 instead of T3."
- Risk-ordering rationale present.

**Remaining gap (P3 unaddressed):**

The Tier Constraints table (lines 241-249) still contains only three constraint rows and the monitoring note:

```
| Worker agents MUST NOT be T5 (no Agent tool)          | ...
| T3+ agents with MK MUST follow MCP key namespace      | ...
| T4+ agents MUST declare citation guardrails            | ...
| Monitor per-agent tool count; alert at 15 tools        | ...
```

The eng-*/red-* MK exclusion constraint is not in this table. An agent author using the Tier Constraints table as their checklist would not see this constraint. The constraint is discoverable via Selection Guideline 4 footnote and mcp-tool-standards.md, but the Tier Constraints table is the expected single-view authority for tier-level constraints. This is the same gap as iteration 1 — not addressed.

**Improvement Path:**

Add to Tier Constraints table: "eng-* and red-* agents MUST NOT use Memory-Keeper despite T4 classification; file-based persistence per P-002 | Engagement-scoped output, no cross-engagement state | P-002, mcp-tool-standards.md". Score would reach 0.91.

---

### Traceability (0.80/1.00)

**Evidence (improvements from iteration 1):**

1. ADR-STORY015-001 added to References table (line 453) with full path: `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/STORY-015-tier-model-renumbering/ADR-STORY015-001-tier-model-renumbering.md`. This resolves the primary traceability gap from iteration 1.

2. Footer VERSION comment added at lines 457-458 with STORY-017 attribution: `<!-- VERSION: 1.3.0 | DATE: 2026-03-28 | SOURCE: ADR-STORY015-001, STORY-017 | REVISION: STORY-017 tier model renumbering -->`. This provides provenance for the STORY-017 changes.

3. Footer Standards Version text updated to 1.3.0 with ADR-STORY015-001 source attribution in the Source line (line 460).

**Remaining gaps:**

1. **Header VERSION comment not updated (internal contradiction):** Line 3 still reads `VERSION: 1.2.0 | DATE: 2026-02-22`. A reviewer reading the header finds version 1.2.0; a reviewer reading the footer finds version 1.3.0. The canonical version of this file is ambiguous from traceability standpoint.

2. **mcp-tool-standards.md header unchanged:** Line 3: `<!-- VERSION: 1.3.1 | DATE: 2026-02-20 | SOURCE: FEAT-028-mcp-tool-integration -->`. The STORY-017 content additions to this file (eng-*/red-* exclusion notes at lines 174 and 176) are not attributed in the version header. A reviewer auditing mcp-tool-standards.md would not know STORY-017 modified this file.

3. **JSON schema $id unchanged:** `"$id": "https://jerry-framework.dev/schemas/agent-governance/v1.0.0"` — the `tool_tier` enum description was updated for STORY-017 but the schema identifier remains at v1.0.0. Schema consumers relying on $id for version detection will not detect the semantic change.

**Improvement Path:**

Three targeted fixes to reach 0.90: (a) update line 3 header VERSION to 1.3.0/2026-03-28; (b) bump mcp-tool-standards.md version to 1.4.0 with STORY-017 notation; (c) bump schema $id to v1.1.0 or add `version` field comment.

---

## Gap Analysis vs. C4 Threshold (0.95)

Current composite: 0.869. Gap to C4 threshold: 0.081. Gap to H-13 standard: 0.051.

| Gap Item | Dimension | Current Score | Score After Fix | Composite Delta |
|----------|-----------|---------------|-----------------|-----------------|
| Fix header VERSION 1.2.0->1.3.0 | IC, TR | IC: 0.83, TR: 0.80 | IC: 0.92, TR: 0.88 | +0.026 |
| Add eng-*/red-* Tier Constraints row | CO, AC | CO: 0.90, AC: 0.86 | CO: 0.93, AC: 0.91 | +0.013 |
| Bump mcp-tool-standards.md + schema $id | EQ, TR | EQ: 0.88, TR: 0.80 (combined w/ above) | EQ: 0.92, TR: 0.88 | +0.010 |
| Refine cognitive mode parenthetical (P5) | IC | IC: 0.83 -> 0.93 (combined w/ header fix) | — | included above |

Estimated composite after all fixes: ~0.869 + 0.026 + 0.013 + 0.010 = ~0.918 (would pass H-13 but not C4 threshold 0.95).

**Assessment against C4 threshold:** Reaching 0.95 requires all five gap items addressed AND Methodological Rigor to approach 0.95 (currently 0.91). Methodological Rigor ceiling: the deliverable correctly implements the ADR decision and documents the rationale; the 0.91 reflects the absence of a methodology note in the schema file and no additional rigor improvements. To push above 0.92 on Methodological Rigor would require: explicit schema changelog, or deeper treatment of T3-vs-T4 boundary edge cases in the guardrail selection table. These are achievable but require deliberate content additions beyond the current scope.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.83 | 0.92 | Update line 3 header VERSION comment to match footer: `<!-- VERSION: 1.3.0 \| DATE: 2026-03-28 \| SOURCE: ADR-STORY015-001, STORY-017 \| REVISION: STORY-017 tier model renumbering: T3=Persistent, T4=External, T5=Orchestration -->`. Eliminates the 1.2.0 vs 1.3.0 contradiction. |
| 2 | Traceability | 0.80 | 0.88 | Bump mcp-tool-standards.md header VERSION to 1.4.0 with STORY-017 notation. Bump schema $id to v1.1.0 (or add `// Version: 1.1.0 (STORY-017)` comment). These two files received STORY-017 changes but carry no STORY-017 attribution. |
| 3 | Actionability | 0.86 | 0.91 | Add eng-*/red-* constraint row to the Tier Constraints table: `\| eng-* and red-* agents MUST NOT use Memory-Keeper despite T4 classification \| Engagement-scoped output; file-based persistence per P-002 \| P-002, mcp-tool-standards.md \|`. Currently only accessible via prose footnote and cross-file reference. |
| 4 | Evidence Quality | 0.88 | 0.92 | Version bumps (P2 above) resolve the provenance gaps that suppress EQ. No independent action needed beyond P2. |
| 5 | Internal Consistency | 0.83 | 0.93 | Refine cognitive mode table parenthetical (line 278): change "T4+ (external access + persistence)" to "T4+ (external + persistence)" or "T4+ (cumulative: MK + web)" to avoid implying persistence begins at T4. Minor but improves precision. |

---

## Iteration Delta Summary

| Dimension | Iteration 1 | Iteration 2 | Delta | Cause |
|-----------|-------------|-------------|-------|-------|
| Completeness | 0.88 | 0.90 | +0.02 | T1/T2 example agents corrected |
| Internal Consistency | 0.90 | 0.83 | -0.07 | New defect: header VERSION 1.2.0 vs footer 1.3.0 |
| Methodological Rigor | 0.91 | 0.91 | 0.00 | No changes |
| Evidence Quality | 0.73 | 0.88 | +0.15 | T1/T2 examples verified correct; ADR reference added |
| Actionability | 0.86 | 0.86 | 0.00 | P3 not addressed |
| Traceability | 0.72 | 0.80 | +0.08 | ADR reference added; footer VERSION attributed |
| **Composite** | **0.849** | **0.869** | **+0.020** | Net improvement despite IC regression |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific line references and .governance.yaml verification
- [x] Uncertain scores resolved downward: IC was 0.83 not 0.87 — the header/footer contradiction is a genuine factual conflict, not a minor style issue; the lower score is warranted
- [x] Iteration calibration: iteration 2 fixes were targeted (P1, P2) — appropriate to expect +0.02 to +0.04 composite, not a jump to 0.92+
- [x] Internal Consistency score reduction from 0.90 to 0.83 reflects real regression: the dual-version comment is a new defect that was not present in iteration 1; it cannot be ignored because it contradicts directly
- [x] No dimension scored above 0.95 without exceptional evidence
- [x] The 0.869 composite is below both H-13 (0.92) and C4 threshold (0.95) — REVISE verdict is correct; this is expected for a two-fix targeted iteration on a multi-gap deliverable

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.869
threshold: 0.95  # C4 per STORY-017 AC; H-13 standard is 0.92
weakest_dimension: Internal Consistency
weakest_score: 0.83
critical_findings_count: 0
iteration: 2
improvement_recommendations:
  - "Fix header VERSION comment (line 3): update to 1.3.0/2026-03-28/STORY-017 to match footer"
  - "Bump mcp-tool-standards.md version to 1.4.0 with STORY-017 attribution"
  - "Bump schema $id to v1.1.0 (STORY-017 modified tool_tier description)"
  - "Add eng-*/red-* MK exclusion row to Tier Constraints table"
  - "Refine cognitive mode parenthetical: T4+ (external + persistence) or T4+ (cumulative: MK + web)"
delta_vs_prior: +0.020
regression_introduced: "Internal Consistency -0.07 (header VERSION 1.2.0 vs footer 1.3.0)"
```
