# Quality Score Report: ADR-STORY015-001 — Tool Security Tier Model Renumbering (Iteration 3)

## L0 Executive Summary

**Score:** 0.919/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.88)

**One-line assessment:** All 7 iteration 2 fixes are confirmed present and correct, raising the composite from 0.889 to 0.919, but a new T4 naming inconsistency — Decision table uses "Persistent + External" as the canonical Name while the agent-development-standards.md P0 draft uses "External" — prevents the ADR from clearing the 0.92 standard gate or the 0.95 C4 threshold; resolving this single inconsistency with an explicit disambiguation statement would likely push the composite to 0.93+.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/STORY-015-tier-model-renumbering/ADR-STORY015-001-tier-model-renumbering.md`
- **Deliverable Type:** ADR (Architecture Decision Record)
- **Criticality Level:** C4
- **Quality Threshold Requested:** >= 0.95 (C4 deliverable, user-specified)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-28
- **Iteration:** 3 (re-score after 7 fixes from iteration 2 report)
- **Prior Score:** 0.889 (iteration 2, REVISE)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.919 |
| **Threshold (C4 user-specified)** | 0.95 |
| **Standard Gate Threshold (H-13)** | 0.92 |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | Yes — prior adversarial reviews iterations 1 and 2 |
| **Delta from Iteration 2** | +0.030 (0.889 → 0.919) |

---

## Fix Verification (Iteration 2 Findings)

All 7 claimed fixes were verified against the ADR content independently before scoring.

| Finding | Claimed Fix | Verification Status | Notes |
|---------|------------|--------------------|-|
| N-1: T5 DX table Full Name uses "Full" (old model) | "DX table now uses 'Orchestration (Persistent + External + Agent)'" | **VERIFIED FIXED** | Line 678: `T5 \| Orchestration \| Orchestration (Persistent + External + Agent)`. Consistent with Migration Plan (line 312), Tier Reclassification (line 436). |
| N-2: Verification checklist total "91" inconsistent with "89 agents" | "Total changed to 89 with scope note excluding 2 projects/ drafts" | **VERIFIED FIXED** | Line 524: Total row shows "89". Scope note at line 526 explicitly explains that pm-pmm skill development project drafts are excluded from migration scope. No longer claims "91." |
| N-3: mcp-tool-standards.md P0 content described-not-drafted | "Full P0 draft added inline" | **VERIFIED FIXED** (with caveat — see N-3 residual below) | Lines 598-633: Four specific changes drafted inline: (1) Tier Constraints table update, (2) MCP-M-001 reference update, (3) Agent Integration Matrix annotations, (4) eng-*/red-* exclusion note reinforcement. Parallel structure to agent-development-standards.md draft. |
| N-4: Pre-migration MK audit absent | "Step 0b grep checking for T3 agents with memory-keeper declarations" | **VERIFIED FIXED** | Lines 452-458: Step 0b added. Uses `grep -rl 'memory-keeper' skills/*/agents/*.md` piped to check companion `.governance.yaml` for T3 tier. Logic is correct — `${f%.md}.governance.yaml` path substitution verified. |
| N-5: Rollback T4_HOLD comment undocumented | "Added explanation that end-of-line anchors prevent T4_HOLD from matching T4$" | **VERIFIED FIXED** | Lines 500-502: Three-line comment explains that grep returns T4_HOLD files but sed end-of-line anchors prevent them from matching. Reader can now verify rollback correctness without reasoning through it independently. |
| N-6: FM-5 classification ambiguous (blocking vs non-blocking) | "Marked 'Non-blocking (post-migration)' with separate ENABLER tracking rationale" | **VERIFIED FIXED** | Line 728: FM-5 mitigation text now reads "**Non-blocking** (post-migration): Strengthen MCP-002 key namespace governance; add collision detection in MK usage. Track as separate ENABLER work item. The existing MCP-002 namespace standard provides adequate governance for migration; enhanced collision detection is a defense-in-depth improvement." |
| Scope grep counts (qualitative "30+", "1+") | "Updated to verified counts (30 lines for agent-development-standards.md, 1 for mcp-tool-standards.md)" | **VERIFIED FIXED** | Lines 547-548: Exact counts provided with reproducible grep commands cited inline. "30 lines with tier references (`grep -c 'T[1-5]' .context/rules/agent-development-standards.md`)" and "1 direct tier reference (`grep -c 'T[1-5]' .context/rules/mcp-tool-standards.md`)". |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.93 | 0.186 | All 7 fixes present; mcp draft now inline; T4 short-vs-full naming ambiguity in draft not explicitly resolved |
| Internal Consistency | 0.20 | 0.88 | 0.176 | T5 and "91/89" fixes confirmed; new residual: Decision table names T4 "Persistent + External" while agent-development-standards.md draft names T4 "External" — unreconciled |
| Methodological Rigor | 0.20 | 0.93 | 0.186 | FM-5 non-blocking status explicit; SAE J1739 cited; 2 sensitivity tests; weight derivation principled |
| Evidence Quality | 0.15 | 0.93 | 0.1395 | Step 0b MK audit added and logically verified; rollback comment added; scope counts exact and reproducible |
| Actionability | 0.15 | 0.92 | 0.138 | mcp draft immediately implementable; Agent Integration Matrix item 3 vague ("Update if tier shown in matrix") but footnote clarifies no structural change needed |
| Traceability | 0.10 | 0.93 | 0.093 | Exact grep counts; SAE J1739; FM-5 ENABLER reference mentioned but no ID assigned |
| **TOTAL** | **1.00** | | **0.919** | |

**Composite:** 0.186 + 0.176 + 0.186 + 0.1395 + 0.138 + 0.093 = **0.919** (REVISE — below both 0.92 standard gate and 0.95 C4 threshold)

---

## Detailed Dimension Analysis

### Completeness (0.93/1.00)

**Evidence:**
All 9 Nygard sections remain present and well-populated. All 7 iteration 2 completeness gaps are addressed:
- mcp-tool-standards.md P0 draft: lines 598-633, four changes specified with replacement text (change 1 is a find-replace, change 2 is a MCP-M-001 text extension, change 3 is an annotation table, change 4 is an exclusion note addition)
- The agent-development-standards.md draft (lines 571-596) remains complete and immediately implementable
- The FMEA, sensitivity analysis, options analysis, migration plan, and rollback are all present and complete

**Gaps:**

1. **T4 Name in agent-development-standards.md draft is "External" while the Decision New Tier Model table uses "Persistent + External".** The DX table (line 672) introduces a Short Name / Full Name distinction, and "External" maps to the Short Name column. But neither the agent-development-standards.md draft (lines 571-579) nor its surrounding prose explicitly states that the draft uses the Short Name as the `Name` column value. An implementer looking at the Decision table (which has a single `Name` column reading "Persistent + External") and then at the draft (which has a single `Name` column reading "External") will see inconsistency without a disambiguation statement. This reduces completeness because the draft's relationship to the canonical Decision table is not explicitly resolved.

2. **FM-5 references "separate ENABLER work item" but assigns no ID.** The ADR identifies this as a post-migration tracking item but leaves its creation to the reader. This is a minor gap; in practice it means the mitigation is deferred but not blocked.

**Improvement Path:**
Add a sentence to the agent-development-standards.md draft section clarifying that the `Name` column uses the Short Name form ("External") from the DX Considerations table, while the cumulative DX table's Full Name ("Persistent + External") is the compound form used in documentation and communication artifacts. This would take one sentence and resolve the ambiguity.

---

### Internal Consistency (0.88/1.00)

**Evidence:**
Both iteration 2 MEDIUM inconsistencies are resolved:
- T5 DX table Full Name: now "Orchestration (Persistent + External + Agent)" — matches all other sections
- Verification checklist total: now "89" with scope note, no longer claims "91"

Arithmetic verification: all weighted totals independently verified:
- Option A: (8×0.15)+(10×0.20)+(10×0.15)+(4×0.10)+(7×0.15)+(8×0.10)+(10×0.15) = 1.20+2.00+1.50+0.40+1.05+0.80+1.50 = 8.45 ✓
- Option C: (10×0.15)+(10×0.20)+(10×0.15)+(8×0.10)+(4×0.15)+(6×0.10)+(10×0.15) = 1.50+2.00+1.50+0.80+0.60+0.60+1.50 = 8.50 ✓
- Sensitivity test 1 Option A: 0.80+2.00+1.50+0.40+1.40+0.80+1.50 = 8.40 ✓
- Sensitivity test 1 Option C: 1.00+2.00+1.50+0.80+0.80+0.60+1.50 = 8.20 ✓
- Sensitivity test 2 Option A: 1.20+1.00+1.50+0.80+1.05+0.80+1.50 = 7.85 ✓
- Sensitivity test 2 Option C: 1.50+1.00+1.50+1.60+0.60+0.60+1.50 = 8.30 ✓

Agent counts verified: T3→T4 table has 49 entries (counted); T2→T2 table has 28 entries (counted); Total: 4+28+49+2+5+1 = 89 ✓.

**New residual inconsistency:**

**T4 Name conflict between Decision table and agent-development-standards.md draft (Severity: MEDIUM).**

The primary New Tier Model table (line 113) uses a single `Name` column with value "**Persistent + External**" for T4. This is described as the compound name chosen for DX reasons (line 116). The agent-development-standards.md draft (line 578) also uses a single `Name` column but with value "**External**" for T4. The DX table (lines 672-678) introduces Short Name / Full Name columns and assigns Short Name = "External", Full Name = "Persistent + External" — but this is only in the DX section, not in the Decision section or the draft.

The mcp-tool-standards.md draft (lines 612, 632) uses "T4 (Persistent + External)" — the compound form — in narrative text. This is internally consistent with the Decision table but conflicts with the agent-development-standards.md draft.

A developer implementing this ADR will encounter:
- Decision section says T4 Name = "Persistent + External"
- agent-development-standards.md replacement content uses Name = "External"
- mcp-tool-standards.md replacement text uses "T4 (Persistent + External)"

The DX table provides a resolution but it is buried in the DX section and not cross-referenced from the Schema and Rule Update Plan. A developer following the Plan would use the draft content (Name = "External") without knowing to reconcile it against the Decision table.

**Gaps:**
No arithmetic errors remain. No logical contradictions in the options analysis. The T4 naming ambiguity is the only material internal consistency issue at this iteration.

**Improvement Path:**
One approach: add a parenthetical to the agent-development-standards.md draft noting "(using Short Name form per DX Considerations section; Full Name 'Persistent + External' is used in documentation/communication contexts)." Another approach: change the Decision New Tier Model table to use the short name "External" in the Name column, matching the draft, and add a note that "Persistent + External" is the compound form for DX communication. Either approach resolves the reader-facing ambiguity.

---

### Methodological Rigor (0.93/1.00)

**Evidence:**
The weight justification is principled (lines 237-242): three bands trace to the ADR's own decision type with specific references to agent-development-standards.md design principles. FMEA covers 7 failure modes (lines 722-730); SAE J1739 is cited; the highest-RPN item (FM-6=120) has the strongest mitigation (three-step script plus verification checklist). The second sensitivity test (migration-weighted) was specifically designed to test the dimension where Option C has maximum advantage over A — a well-targeted perturbation. FM-5 is explicitly marked non-blocking with rationale.

**Minor gaps:**

1. The "separate ENABLER work item" for FM-5 is mentioned but not created. This is consistent with the ADR's scope (the ADR documents the migration, not post-migration tracking). The FM-5 note is sufficient for this purpose. Minor.

2. The sensitivity analysis interprets "governance-weighted is most appropriate for C4 rule-file changes per AE-002" (line 293) — this interpretation is sound and traceable. The option of testing other weight perturbations (e.g., removing Monotonicity as a distinguishing factor) was identified in iteration 1 but not added. At 2 sensitivity tests, coverage is adequate for a C4 decision. The two tests target the most influential weight dimensions (governance rigor vs. migration cost) and are sufficient.

**Improvement Path:**
No material improvement needed for Methodological Rigor at this quality level. The FM-5 ENABLER reference is a post-ADR action item that appropriately belongs outside this document.

---

### Evidence Quality (0.93/1.00)

**Evidence:**
The migration script is correct and executable. The Step 0b MK audit (lines 452-458) uses a well-constructed pipeline: `grep -rl 'memory-keeper' skills/*/agents/*.md | while read f; do` followed by a companion YAML check `grep -q 'tool_tier:.*T3' "${f%.md}.governance.yaml"`. The path substitution `${f%.md}.governance.yaml` is correct: strips `.md` extension and appends `.governance.yaml`. The expected output is documented ("Expected: no output. Any hits require investigation before migration.").

The rollback script is now fully documented. The T4_HOLD/T4$ anchor interaction comment (lines 500-502) correctly explains why the rollback grep includes T4_HOLD files but the sed does not modify them. A reviewer can now verify the rollback without reasoning through the end-of-line anchor behavior independently.

Scope verification (lines 547-548) provides exact reproducible grep invocations with confirmed counts (30 for agent-development-standards.md, 1 for mcp-tool-standards.md).

**Gaps:**

1. The mcp-tool-standards.md draft Change 3 (Agent Integration Matrix, lines 614-628) includes a note: "The Agent Integration Matrix does not currently show tier numbers inline... The matrix requires no structural change; only the cross-reference text needs updating." This claim is asserted without providing the actual grep or file evidence to support it. The claim may be correct but is stated without verification evidence, unlike the scope verification for agent-development-standards.md and mcp-tool-standards.md which cite exact counts.

**Improvement Path:**
Add one line confirming that a grep of mcp-tool-standards.md for tier numbers in the Agent Integration Matrix table returns zero hits (confirming the matrix does not show tier numbers inline), supporting the "no structural change needed" claim with reproducible evidence.

---

### Actionability (0.92/1.00)

**Evidence:**
The migration is fully actionable. The three-step forward migration script handles all edge cases. The rollback mirrors it. The post-migration verification checklist (lines 515-524) provides 7 explicit checks with expected values. Step 0 establishes a baseline (lines 444-450). Step 0b provides a pre-migration anomaly check (lines 452-458).

The agent-development-standards.md draft (lines 571-596) is complete: new tier table, new selection guidelines, new tier constraints — all ready for copy-paste replacement.

The mcp-tool-standards.md draft (lines 598-633) provides 4 specific changes with before/after text for changes 1 and 2, an annotation table for change 3, and exact replacement text for change 4.

**Residual gap:**

Change 3 of the mcp-tool-standards.md draft (lines 614-628) ends with: "Update if tier shown in matrix." This instruction is vague for an implementer — they must open mcp-tool-standards.md, check whether the matrix shows tier numbers, and decide what to update (or not). The footnote at lines 628-629 partially resolves this by concluding "The matrix requires no structural change" — but only after a parenthetical that itself uses the conditional "Update if tier shown." A developer following only the change 3 annotation table header might not scroll to the footnote before opening the file.

**Improvement Path:**
Restructure change 3: replace the conditional "Update if tier shown in matrix" with a definitive action: "No changes required to the Agent Integration Matrix table rows. Only the footnote below the table (T4 MK namespace requirement text) requires updating as specified in Change 1." This removes the conditional and makes the action deterministic.

---

### Traceability (0.93/1.00)

**Evidence:**
All iteration 2 traceability gaps are resolved. Scope verification now provides exact grep invocations with counts. SAE J1739 is cited for the FMEA scale. Weight band derivation traces to agent-development-standards.md design principles with specific principle names ("least privilege," "monotonicity," "H-35"). The governance-weighted sensitivity interpretation traces to AE-002 and the explicitly stated tier selection guideline in agent-development-standards.md.

The compliance section (lines 700-716) maps the decision to P-003, P-020, P-022, MCP-002, MCP-M-001 — a complete constitutional alignment table.

**Minor gap:**

The FM-5 "separate ENABLER work item" is mentioned as a mitigation but has no ID or tracking reference. This is a forward-looking trace that is incomplete by definition at ADR authoring time. Acceptable for this type of document.

**Improvement Path:**
No material improvement needed for Traceability. The FM-5 ENABLER is a post-ADR item appropriately deferred.

---

## New Issues Found in Iteration 3

| # | Issue | Dimension Impact | Severity |
|---|-------|-----------------|---------|
| R-1 | T4 Name inconsistency: Decision table Name column = "Persistent + External" (compound); agent-development-standards.md draft Name column = "External" (short); mcp-tool-standards.md draft uses "T4 (Persistent + External)" in narrative. DX section introduces Short/Full form but does not cross-reference from the rule update plan. | Internal Consistency, Completeness | MEDIUM |
| R-2 | mcp-tool-standards.md draft Change 3 uses conditional "Update if tier shown in matrix" — implementer must open file to determine whether action is needed; footnote resolves but is separated from the instruction | Actionability | LOW |
| R-3 | mcp-tool-standards.md draft Change 3 "no structural change needed" claim lacks verification evidence (no grep cited confirming matrix has no tier numbers inline) | Evidence Quality | LOW |

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.88 | 0.93 | Add one explicit sentence in the Schema and Rule Update Plan section (near lines 567-568 or the agent-development-standards.md draft header) stating: "The draft below uses the Short Name form ('External') for the T4 Name column per the DX Considerations Short Name/Full Name framework (section below). The compound Full Name 'Persistent + External' is used in documentation and DX communication contexts; the rule file name field uses the Short Name." This resolves the T4 name ambiguity with zero structural change to the ADR. |
| 2 | Actionability | 0.92 | 0.94 | In mcp-tool-standards.md Change 3, replace conditional "Update if tier shown in matrix" with a definitive: "No row changes needed in the Agent Integration Matrix. The matrix does not currently show tier numbers inline (confirmed: zero matches for `grep 'T[1-5]' .context/rules/mcp-tool-standards.md` in matrix table rows). Only the footnote text referencing 'T4 agents MUST follow MCP key namespace' requires updating per Change 1." |
| 3 | Completeness | 0.93 | 0.95 | Cross-reference the Short Name / Full Name framework from the Schema and Rule Update Plan. A line like "> T4 Short Name: 'External'. T4 Full Name: 'Persistent + External'. See [DX Considerations](#dx-considerations) for naming rationale." in the New Tier Model section would provide an explicit anchor for the naming decision. |
| 4 | Evidence Quality | 0.93 | 0.95 | Add grep evidence for the Change 3 "no structural change" claim: `grep -n 'T[1-5]' .context/rules/mcp-tool-standards.md | grep -i 'matrix\|agent'` → expected: 0 matches in the matrix table section. This converts the asserted claim to verified evidence. |

---

## Score Delta Analysis (Iteration 2 → Iteration 3)

| Dimension | Iter 2 Score | Iter 3 Score | Delta | Change Driver |
|-----------|-------------|-------------|-------|--------------|
| Completeness | 0.90 | 0.93 | +0.03 | mcp draft added; T4 naming ambiguity partially mitigated by DX Short/Full Name framework |
| Internal Consistency | 0.86 | 0.88 | +0.02 | T5 DX table fix + "89/91" fix close 2 MEDIUM gaps; new T4 naming inconsistency partially offsets |
| Methodological Rigor | 0.91 | 0.93 | +0.02 | FM-5 non-blocking status explicit; otherwise no change from iter 2 |
| Evidence Quality | 0.88 | 0.93 | +0.05 | Step 0b MK audit added; rollback comment added; scope counts exact |
| Actionability | 0.88 | 0.92 | +0.04 | mcp draft provides 4 concrete changes; residual "Update if" vagueness in Change 3 |
| Traceability | 0.91 | 0.93 | +0.02 | Exact grep counts added; all prior gaps closed |
| **Composite** | **0.889** | **0.919** | **+0.030** | |

---

## Path to 0.95 (C4 Threshold)

The ADR is 0.031 below the C4 threshold. The primary blocking dimension is Internal Consistency (0.88 → needs ~0.95 to push composite to 0.95). Secondary contributions needed from Completeness, Actionability, Evidence Quality, and Traceability.

| What must change | Dimension | Expected score | Composite contribution |
|-----------------|-----------|---------------|----------------------|
| Resolve T4 naming inconsistency (R-1) | Internal Consistency | 0.88 → 0.94 | +0.012 |
| Add Short/Full Name disambiguation statement | Completeness | 0.93 → 0.96 | +0.006 |
| Fix Change 3 conditional → deterministic | Actionability | 0.92 → 0.95 | +0.0045 |
| Add grep evidence for Change 3 claim | Evidence Quality | 0.93 → 0.95 | +0.003 |
| **Projected composite** | | | **0.944** |

At 0.944, the ADR would exceed the standard gate (0.92) and approach but not quite reach 0.95. One more pass addressing the four items above plus any additional polish on Evidence Quality and Traceability could reach 0.95.

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite computation
- [x] Evidence documented for each score with specific line references
- [x] Uncertain scores resolved downward (Internal Consistency held at 0.88 not 0.90 given T4 naming inconsistency; uncertain whether "External" or "Persistent + External" is canonical in the rule file)
- [x] C4 calibration applied: 0.95 user threshold; neither standard gate (0.92) nor C4 threshold (0.95) is met
- [x] No dimension scored above 0.95 without exceptional evidence
- [x] All 7 fixes verified independently against actual ADR content, not taken at face value from task description
- [x] New issues (R-1 through R-3) actively searched for; arithmetic independently re-verified; agent counts manually confirmed (49 T3→T4, 28 T2→T2)
- [x] First-draft calibration not applicable (this is iteration 4 of the ADR document); calibration applied against C4 high-bar standard

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.919
threshold_standard: 0.92
threshold_requested: 0.95
weakest_dimension: internal_consistency
weakest_score: 0.88
critical_findings_count: 0
new_issues_count: 3
iteration: 3
delta_from_iteration_2: +0.030
improvement_recommendations:
  - "Add one sentence disambiguating T4 Name: draft uses Short Name 'External'; Decision table uses Full Name 'Persistent + External'; cross-reference DX Short/Full Name framework"
  - "Fix mcp-tool-standards.md Change 3 instruction from conditional 'Update if tier shown in matrix' to definitive 'No row changes needed; grep confirms zero tier numbers in matrix table'"
  - "Add cross-reference from Schema and Rule Update Plan to DX Considerations Short/Full Name table"
  - "Add verification evidence for Change 3 'no structural change' claim (grep showing zero tier-number matches in Agent Integration Matrix)"
```
