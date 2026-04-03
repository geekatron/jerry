# Quality Score Report: STORY-017 Rule File Updates (Iteration 3)

## L0 Executive Summary

**Score:** 0.916/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Traceability (0.88)

**One-line assessment:** Iteration 3 closes all four priority gaps from iteration 2 except the schema $id version bump, producing a +0.047 composite gain that brings the deliverable above the H-13 standard threshold (0.92) on most dimensions but still below the C4 threshold (0.95); the remaining gap is the JSON schema $id still reads `v1.0.0` despite STORY-017 modifying the `tool_tier` description, leaving schema consumers unable to detect the semantic change via the $id.

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
- **Iteration:** 3 (re-score after targeted revision)
- **Prior Score:** 0.869 (iteration 2)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.916 |
| **C4 Threshold** | 0.95 (per STORY-017 AC, ADR-STORY015-001) |
| **Standard Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Delta vs. Iteration 2** | +0.047 |
| **Strategy Findings Incorporated** | No — standalone scoring |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.92 | 0.184 | All normative scope items now present including eng-*/red-* Tier Constraints row; schema $id not bumped (provenance gap, partial P2) |
| Internal Consistency | 0.20 | 0.94 | 0.188 | All iter-2 contradictions resolved: header/footer both 1.3.0/2026-03-28; mcp-tool-standards Full Name usage is documented convention; new Tier Constraints row consistent with Selection Guideline 4 |
| Methodological Rigor | 0.20 | 0.92 | 0.184 | Risk-ordering rationale intact; new Tier Constraints row includes rationale column; schema $id minor gap persists |
| Evidence Quality | 0.15 | 0.90 | 0.135 | mcp-tool-standards.md bumped to 1.4.0/STORY-017 (iter-2 gap resolved); schema $id still v1.0.0 despite STORY-017 modifying tool_tier description |
| Actionability | 0.15 | 0.91 | 0.137 | eng-*/red-* MK exclusion row added to Tier Constraints table with clear constraint + rationale + sources; schema $id undiscoverable version change has minor actionability impact |
| Traceability | 0.10 | 0.88 | 0.088 | ADS header now 1.3.0/STORY-017; mcp header now 1.4.0/STORY-017; schema $id still v1.0.0 — one of three iter-2 traceability gaps remains |
| **TOTAL** | **1.00** | | **0.916** | |

---

## Detailed Dimension Analysis

### Completeness (0.92/1.00)

**Evidence (iter-3 improvements):**

The eng-*/red-* Tier Constraints row is now present at line 248 of agent-development-standards.md:

```
| eng-\* and red-\* agents MUST NOT use Memory-Keeper despite T4 classification | Engagement-scoped output requires file-based persistence per P-002; MK would create cross-project state pollution | mcp-tool-standards.md, ADR-STORY015-001 RISK-002 |
```

This was the primary iter-2 Completeness gap (P3 recommendation). The Tier Constraints table is now the complete single-view authority for tier-level constraints: Worker/T5, MK namespace for T3+, citation guardrails for T4+, eng-*/red-* MK exclusion, and the tool-count monitoring advisory.

The ADS header VERSION comment is fixed (line 3 now reads `VERSION: 1.3.0 | DATE: 2026-03-28 | SOURCE: ADR-STORY015-001, STORY-017`). Header and footer are now consistent.

All 10 original STORY-017 scope items verified present:
1. Tier table Short Names (T3=Persistent, T4=External, T5=Orchestration)
2. Selection guidelines with T3/T4 narrative boundary
3. Tier Constraints MK namespace row (T3+ scoped)
4. Cognitive mode table T4/T5 tier assignments
5. Guardrail selection table tier references
6. L2-REINJECT comment with updated tier names
7. mcp-tool-standards.md MCP-M-001 updated
8. eng-*/red-* exclusion notes in mcp-tool-standards.md Not Included section
9. JSON schema tool_tier description
10. eng-*/red-* Tier Constraints explicit row (added iter 3)

**Gaps:**

The JSON schema `$id` at line 3: `"$id": "https://jerry-framework.dev/schemas/agent-governance/v1.0.0"`. The `tool_tier` enum description was updated for STORY-017 (now includes T3=Persistent, T4=External, T5=Orchestration, and the "includes MK" notation at T4). The schema semantic content changed but the $id remains at v1.0.0. This is a provenance completeness gap: the schema's self-reported identifier does not reflect that it was modified. The iter-2 recommendation P2 called for bumping the $id to v1.1.0; only the mcp-tool-standards.md portion of P2 was executed.

**Improvement Path:**

Update `$id` to `"https://jerry-framework.dev/schemas/agent-governance/v1.1.0"`. Score would reach 0.94.

---

### Internal Consistency (0.94/1.00)

**Evidence:**

All iter-2 contradictions are resolved:

1. **Header/footer VERSION resolved:** Line 3 now `VERSION: 1.3.0 | DATE: 2026-03-28 | SOURCE: ADR-STORY015-001, STORY-017`. Line 458 footer also `VERSION: 1.3.0 | DATE: 2026-03-28 | SOURCE: ADR-STORY015-001, STORY-017`. Direct match — the contradiction that cost 0.07 in iteration 2 is eliminated.

2. **New Tier Constraints row consistent with Selection Guideline 4:** The new row states "MUST NOT use Memory-Keeper despite T4 classification." Selection Guideline 4 footnote states "eng-\* and red-\* agents are classified T4 but MUST NOT use Memory-Keeper." Both carry identical semantic content. mcp-tool-standards.md lines 174 and 176 also consistent.

3. **mcp-tool-standards.md Full Name usage documented as convention:** Line 43 uses "T4 (Persistent + External)" and lines 174/176 use the same. ADS line 233 explicitly establishes this as the Full Name form: "T4's Full Name is 'Persistent + External' (cumulative capability), used in DX communication contexts to signal that T4 inherits T3's Memory-Keeper capability." This is not a contradiction — it is a documented dual-naming convention.

4. **Cognitive mode table parenthetical refined:** Line 279 now reads "T4 (external research with cross-session persistence)." This correctly conveys that T4 agents doing external research also have MK (via cumulative inheritance), eliminating the iter-2 concern that "T4+ (external access + persistence)" could be read as implying MK first appears at T4.

5. **Cross-file tier naming:** T3=Persistent, T4=External, T5=Orchestration consistent across ADS, mcp-tool-standards.md, and schema description.

**Gaps:**

None substantive. The 0.94 ceiling (vs 1.00) reflects that two minor consistency risks exist at the edge of detection: (a) "Orchestration (T3-T5)" in the Guardrail Selection table at line 348 remains an accurate but slightly ambiguous range reference — it correctly means orchestration agents can range from T3 to T5 depending on delegation needs; (b) the schema `$id` inconsistency (v1.0.0 body vs STORY-017 changes) is primarily a traceability/evidence issue, not an internal logical contradiction.

**Improvement Path:**

No substantive changes needed. Score of 0.94 reflects near-complete consistency with documented conventions for the dual-naming pattern. To approach 0.96, the Guardrail Selection "T3-T5" range could be expanded to "(T3=Persistent, T4=External, T5=Orchestration) depending on delegation needs" for maximum precision.

---

### Methodological Rigor (0.92/1.00)

**Evidence:**

The principle-of-least-privilege methodology is well-expressed across five guidelines. The risk-ordering rationale ("Memory-Keeper internal MCP, lower-risk than web tools") is intact. The new Tier Constraints row adds methodological depth: it includes both a constraint statement and a rationale column ("Engagement-scoped output requires file-based persistence per P-002; MK would create cross-project state pollution"), which is methodologically sounder than a bare constraint.

The Short Name / Full Name convention is documented with ADR cross-reference (line 233). This meta-documentation of the naming convention is itself a methodological improvement over having undocumented naming variability.

The mcp-tool-standards.md "Not included (by design)" explanations for eng-*/red-* (lines 174/176) provide reasoning: "T4 tier permits MK as a ceiling; the `.md` frontmatter and this exclusion note prevent actual MK access." This is correct: the tier ceiling represents maximum capability, and agent-specific frontmatter restricts below that ceiling.

**Gaps:**

The JSON schema file has no changelog comment or description version field. A methodology-aware reader auditing the schema has no in-file signal that STORY-017 modified the `tool_tier` description. The schema's `description` field for `tool_tier` (line 17-18) is updated and correct, but there is no provenance mechanism inside the JSON file itself. This was noted in iter 2 as a minor gap.

**Improvement Path:**

Adding a `"$comment": "Last modified: STORY-017 (2026-03-28) - tier renumbering to T3=Persistent, T4=External, T5=Orchestration"` to the `tool_tier` property, or updating the `$id` to v1.1.0, would give schema auditors a methodology trail. Score would reach 0.94.

---

### Evidence Quality (0.90/1.00)

**Evidence:**

The mcp-tool-standards.md version bump to 1.4.0 is confirmed: line 3 reads `<!-- VERSION: 1.4.0 | DATE: 2026-03-28 | SOURCE: FEAT-028-mcp-tool-integration, ADR-STORY015-001, STORY-017 | REVISION: STORY-017 tier renumbering: MCP-M-001 T3/T4 refs, eng-*/red-* MK exclusion notes -->`. This was the primary iter-2 Evidence Quality gap (mcp-tool-standards.md carrying STORY-017 content without version attribution). Now resolved.

All T1-T5 example agents verified correct in iter 2 and unchanged in iter 3:
- T1: pe-scorer, diataxis-classifier, sb-voice — all confirmed T1 in .governance.yaml files
- T2: ps-critic, adv-scorer, uc-author — all confirmed T2 in .governance.yaml files
- T3: ts-parser, ts-extractor — per ADR motivation
- T4: ps-researcher, eng-architect, red-recon — per ADR migration table
- T5: ux-orchestrator — per governance file

ADR-STORY015-001 reference in ADS References section (line 453) provides a traceable source for the tier renumbering decision.

**Remaining gap:**

The JSON schema `$id` remains `"https://jerry-framework.dev/schemas/agent-governance/v1.0.0"`. The `tool_tier` enum description (lines 17-18) was modified: STORY-017 changed it from the pre-renumbering description to "T1=Read-Only, T2=Read-Write, T3=Persistent (+MK), T4=External (+Web, includes MK), T5=Orchestration (+Agent)." Schema consumers relying on the `$id` for version detection (e.g., validation tooling comparing cached schema by ID) will not detect this semantic change. The actual claims in the schema are accurate and evidence-supported; this is a provenance evidence gap rather than an accuracy gap. Scored at 0.90 (rubric: "most claims supported, minor gap") — the substantive evidence is solid; the provenance trail for schema changes is incomplete.

**Improvement Path:**

Bump `$id` to `v1.1.0`. Score would reach 0.93.

---

### Actionability (0.91/1.00)

**Evidence:**

The primary iter-2 actionability gap is resolved. The Tier Constraints table now contains the eng-*/red-* MK exclusion as an explicit constraint row with three components:

- **Constraint:** "eng-\* and red-\* agents MUST NOT use Memory-Keeper despite T4 classification"
- **Rationale:** "Engagement-scoped output requires file-based persistence per P-002; MK would create cross-project state pollution"
- **Sources:** "mcp-tool-standards.md, ADR-STORY015-001 RISK-002"

An agent author implementing a new eng-* or red-* agent and consulting the Tier Constraints table as their checklist will now encounter this constraint directly. In iter 2, the constraint was only accessible via Selection Guideline 4 prose footnote and mcp-tool-standards.md cross-reference — requiring two extra reading steps. The table placement eliminates that navigation requirement.

The five Selection Guidelines remain clear and sequentially deterministic. T3/T4 boundary is explicit: "If your agent also needs web tools, use T4 instead of T3 (T4 includes all T3 capabilities including Memory-Keeper)." The cumulative inheritance model is actionable.

**Minor remaining gap:**

A new eng-* agent author reading only the schema file would find no actionable signal about the MK exclusion in the schema itself. The schema `tool_tier` description correctly lists T4 as "External (+Web, includes MK)" — accurate for the general case — but includes no exception notation for eng-*/red-* agents. Schema-only readers must also consult ADS. This is an inherent cross-file dependency, not a defect in ADS or mcp-tool-standards.md, but it slightly constrains actionability at the schema layer. Resolved by bumping $id to draw attention to the semantic change, though that does not add the exception text itself.

**Improvement Path:**

The schema $id bump would indirectly improve actionability by alerting schema consumers that the tier model changed and they should re-read the authoritative prose. Direct improvement would be adding a `$comment` to the `tool_tier` property noting the eng-*/red-* exception with a reference to ADS. Score would reach 0.93.

---

### Traceability (0.88/1.00)

**Evidence (iter-3 improvements):**

1. **ADS header VERSION resolved:** Line 3 now `VERSION: 1.3.0 | DATE: 2026-03-28 | SOURCE: ADR-STORY015-001, STORY-017`. The ambiguous dual-version state (1.2.0 header, 1.3.0 footer) from iter 2 is eliminated. A reviewer reading either end of the file encounters the same version.

2. **mcp-tool-standards.md version bumped:** Line 3 now `VERSION: 1.4.0 | DATE: 2026-03-28 | SOURCE: FEAT-028-mcp-tool-integration, ADR-STORY015-001, STORY-017 | REVISION: STORY-017 tier renumbering: MCP-M-001 T3/T4 refs, eng-*/red-* MK exclusion notes`. A reviewer auditing which files STORY-017 modified can now identify mcp-tool-standards.md by reading its header. This was the most significant iter-2 traceability gap.

3. **ADR-STORY015-001 reference:** Present in ADS References section (line 453) with full path. Provides a traceable source for the tier renumbering rationale.

4. **ADS footer Standards Version:** `*Standards Version: 1.3.0*` with `ADR-STORY015-001 (tier renumbering)` in the Source line.

**Remaining gap:**

The JSON schema $id remains `v1.0.0`. This is the sole remaining traceability gap. The schema's `tool_tier` description was changed in STORY-017 but the $id identifier does not reflect this. Schema consumers cannot determine from the $id alone whether they have the pre- or post-renumbering version. The schema body itself is correct; only the version identifier is stale. Score 0.88 (rubric: "most items traceable, minor gap") is appropriate — two of three iter-2 traceability gaps are resolved; one persists.

**Improvement Path:**

Update `$id` to `"https://jerry-framework.dev/schemas/agent-governance/v1.1.0"`. Score would reach 0.92.

---

## Iter-3 vs Iter-2 Delta Summary

| Dimension | Iter-2 | Iter-3 | Delta | Cause |
|-----------|--------|--------|-------|-------|
| Completeness | 0.90 | 0.92 | +0.02 | eng-*/red-* Tier Constraints row added; header VERSION fixed |
| Internal Consistency | 0.83 | 0.94 | +0.11 | Header/footer VERSION contradiction resolved; parenthetical refined |
| Methodological Rigor | 0.91 | 0.92 | +0.01 | New Tier Constraints row adds rationale column |
| Evidence Quality | 0.88 | 0.90 | +0.02 | mcp-tool-standards.md version bumped to 1.4.0/STORY-017 |
| Actionability | 0.86 | 0.91 | +0.05 | eng-*/red-* MK exclusion now in Tier Constraints table |
| Traceability | 0.80 | 0.88 | +0.08 | ADS header fixed; mcp-tool-standards.md version bumped |
| **Composite** | **0.869** | **0.916** | **+0.047** | Four of five iter-2 gaps addressed |

---

## Gap Analysis vs. C4 Threshold (0.95)

Current composite: 0.916. Gap to C4 threshold: 0.034. Gap to H-13 standard: -0.004 (fractionally below).

| Remaining Gap | Dimension | Current Score | Score After Fix | Composite Delta |
|---------------|-----------|---------------|-----------------|-----------------|
| Bump schema $id from v1.0.0 to v1.1.0 | EQ, TR, CO, AC | EQ:0.90, TR:0.88, CO:0.92, AC:0.91 | EQ:0.93, TR:0.92, CO:0.94, AC:0.93 | +0.017 |
| Add schema $comment for tool_tier STORY-017 attribution | MR | MR:0.92 | MR:0.94 | +0.004 |

Estimated composite after schema fixes: ~0.916 + 0.017 + 0.004 = ~0.937 (would pass H-13 comfortably but still below C4 threshold 0.95).

**Assessment against C4 threshold (0.95):** Reaching 0.95 requires that all six dimensions score >= 0.94 on average. After the schema fix, the estimated dimension floor would be ~0.92 (Completeness, Traceability post-fix). To reach 0.95, additional improvements would be needed in Methodological Rigor (currently 0.92 ceiling) and Traceability (estimated 0.92 post-schema-fix). Specific paths:

- Methodological Rigor to 0.95+: Add schema changelog comment + add a formal per-file changelog section documenting what each STORY modified. Currently the VERSION comment provides one line; a structured changelog section would provide full audit trail.
- Completeness to 0.95+: Schema $id fix addresses the only remaining normative gap; beyond that, completeness is at ceiling.
- Internal Consistency is already at 0.94; no further action needed.
- Evidence Quality to 0.93+: Schema $id fix + optional schema $comment.

**Honest gap assessment:** The C4 threshold of 0.95 is a genuinely high bar. The current 0.916 represents a well-executed tier renumbering implementation with documented rationale, consistent cross-file naming, accurate example agents, and a complete constraint table. The delta to 0.95 is real: the schema file has no version-bump mechanism and no in-file changelog, creating a provenance blind spot that affects four of six dimensions simultaneously.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Traceability / Evidence Quality | TR:0.88, EQ:0.90 | TR:0.92, EQ:0.93 | Bump schema `$id` from `v1.0.0` to `v1.1.0`. This is a one-line change in `docs/schemas/agent-governance-v1.schema.json` line 3: `"$id": "https://jerry-framework.dev/schemas/agent-governance/v1.1.0"`. Affects four dimensions simultaneously (CO, EQ, AC, TR). Estimated composite delta: +0.017. |
| 2 | Methodological Rigor | 0.92 | 0.94 | Add `"$comment"` to `tool_tier` property in schema (after line 17): `"$comment": "STORY-017 (2026-03-28): tier renumbering to T3=Persistent, T4=External, T5=Orchestration. eng-*/red-* agents are T4 but MUST NOT use Memory-Keeper per mcp-tool-standards.md."` Gives schema auditors an in-file methodology trail without changing the schema's validating semantics. |
| 3 | Completeness | 0.92 | 0.94 | Addressed by Recommendation 1 (schema $id). No independent action needed. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific line references
- [x] Uncertain scores resolved downward: Completeness was considered at 0.93 (iter-2 improvement path predicted 0.93 after Tier Constraints row added); resolved to 0.92 because the schema $id gap (partial P2) prevents full completion of the provenance scope
- [x] Actionability was considered at 0.92; resolved to 0.91 because the schema layer has no eng-*/red-* exception notation (minor but real limitation for schema-only readers)
- [x] Iteration calibration: iter 3 addressed four of five iter-2 recommendations; appropriate to expect +0.04 to +0.06 composite gain; actual +0.047 is within that range
- [x] Internal Consistency recovery from 0.83 to 0.94 (+0.11) is justified by eliminating a direct factual contradiction (two conflicting VERSION statements) and resolving the parenthetical ambiguity — these were genuine defects whose removal produces a large score recovery
- [x] No dimension scored above 0.95 without exceptional evidence
- [x] The 0.916 composite is just below H-13 (0.92) and materially below C4 threshold (0.95); REVISE verdict is correct

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.916
threshold: 0.95  # C4 per STORY-017 AC; H-13 standard is 0.92
weakest_dimension: Traceability
weakest_score: 0.88
critical_findings_count: 0
iteration: 3
prior_score: 0.869
delta_vs_prior: +0.047
improvement_recommendations:
  - "Bump schema $id from v1.0.0 to v1.1.0 (docs/schemas/agent-governance-v1.schema.json line 3)"
  - "Add $comment to tool_tier property with STORY-017 attribution and eng-*/red-* MK exception note"
gaps_remaining:
  - "JSON schema $id still v1.0.0 despite STORY-017 modifying tool_tier description — affects EQ, TR, CO, AC simultaneously"
gaps_closed_this_iteration:
  - "ADS header VERSION 1.2.0->1.3.0 (IC gap resolved)"
  - "mcp-tool-standards.md version bumped to 1.4.0/STORY-017 (EQ, TR gap resolved)"
  - "eng-*/red-* Tier Constraints row added to ADS (CO, AC gap resolved)"
  - "Cognitive mode parenthetical refined to T4 (external research with cross-session persistence) (IC precision improved)"
estimated_composite_after_remaining_fixes: 0.937
```
