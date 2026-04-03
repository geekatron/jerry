# Quality Score Report: ADR-STORY015-001 — Tool Security Tier Model Renumbering (Iteration 2)

## L0 Executive Summary

**Score:** 0.889/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.86)

**One-line assessment:** All 7 iteration 1 findings are correctly addressed, raising the composite from 0.852 to 0.889, but three new issues introduced by the revisions — a T5 naming inconsistency in the DX table, a confusing "91 agent" claim in the verification checklist, and the still-undrafted mcp-tool-standards.md P0 content — prevent the ADR from clearing the 0.95 C4 threshold.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/STORY-015-tier-model-renumbering/ADR-STORY015-001-tier-model-renumbering.md`
- **Deliverable Type:** ADR (Architecture Decision Record)
- **Criticality Level:** C4
- **Quality Threshold Requested:** >= 0.95 (C4 deliverable, user-specified)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-28
- **Iteration:** 2 (re-score after 6 fixes from iteration 1 report)
- **Prior Score:** 0.852 (iteration 1, REVISE)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.889 |
| **Threshold (C4 user-specified)** | 0.95 |
| **Standard Gate Threshold (H-13)** | 0.92 |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | Yes — prior adversarial review iteration 1 |
| **Delta from Iteration 1** | +0.037 (0.852 → 0.889) |

---

## Fix Verification (Iteration 1 Findings)

Before scoring, each iteration 1 finding was verified against the revised ADR:

| Finding | Status | Verification |
|---------|--------|-------------|
| CRITICAL-1: Migration script YAML quoting bug | **FIXED** | Three-step protection pattern added (lines 452–478). `grep -rl 'tool_tier:.*T3'` catches both quoted and unquoted. Two sed commands per file: `s/tool_tier: T3$/tool_tier: T4/` and `s/tool_tier: "T3"$/tool_tier: "T4"/`. Verified 5 pm-pmm agents do use quoted form in codebase. |
| CRITICAL-2: Sensitivity analysis arithmetic error | **FIXED** | Option A governance-weighted score corrected to 8.40 (line 280). Final ranking rewrites to compare governance-weighted scores: "A (8.40) > C (8.20)" (line 295). Verified: (8×0.10)+(10×0.20)+(10×0.15)+(4×0.10)+(7×0.20)+(8×0.10)+(10×0.15) = 8.40 ✓. |
| FMEA gaps (FM-6, FM-7) | **FIXED** | FM-6 (quoting bug, S=8, O=5, D=3, RPN=120) added at line 680. FM-7 (stale docs, S=4, O=6, D=4, RPN=96) added at line 681. SAE J1739 scale cited at line 683. |
| Rollback missing | **FIXED** | Full three-step rollback script added (lines 487–499). Handles quoted and unquoted forms symmetrically with forward migration. T4_HOLD protection pattern correctly excludes ts-parser/ts-extractor from the bulk rename step. |
| Weight justification missing | **FIXED** | Three-band derivation added (lines 237–242): Band 1 = 20% for Completeness (primary ADR motivation), Band 2 = 15% each for 4 structural principles, Band 3 = 10% each for implementation concerns. Traces to agent-development-standards.md design principles. |
| DX naming rationale | **FIXED** | Lines 631–633 explain why "Persistent + External" was adopted over DX recommendation "Web + Persistent": accumulation-order readability, "External" continuity for migrating authors, Context7 not strictly "web". |
| Scope verification | **FIXED** | Lines 533–538 provide file-by-file grep verification of tier references across all rule files, confirming change boundary. |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.90 | 0.180 | All 7 iteration 1 gaps addressed; mcp-tool-standards.md P0 content still described-not-drafted; T5 naming inconsistency in DX table |
| Internal Consistency | 0.20 | 0.86 | 0.172 | Arithmetic errors corrected; new inconsistencies: T5 "Full" in DX table vs "Orchestration" everywhere else; "91 agents" in verification total vs "89 agents" throughout |
| Methodological Rigor | 0.20 | 0.91 | 0.182 | FM-6/FM-7 added; SAE J1739 cited; weight derivation added; second sensitivity test added; governance-weighted interpretation sound |
| Evidence Quality | 0.15 | 0.88 | 0.132 | Migration script now correct and executable; rollback covers all cases; pre-migration MK audit still absent |
| Actionability | 0.15 | 0.88 | 0.132 | Rollback script complete; verification checklist added with expected counts; mcp-tool-standards.md Agent Integration Matrix draft still absent |
| Traceability | 0.10 | 0.91 | 0.091 | SAE J1739 cited; weight bands trace to agent-development-standards.md; governance-weighted justification traces to stated principle |
| **TOTAL** | **1.00** | | **0.889** | |

**Composite:** 0.180 + 0.172 + 0.182 + 0.132 + 0.132 + 0.091 = **0.889**

---

## Detailed Dimension Analysis

### Completeness (0.90/1.00)

**Evidence:**
All 9 Nygard sections remain present and populated. All 7 iteration 1 completeness gaps have been resolved: weight derivation added, DX naming rationale added, scope verification added, FMEA FM-6/FM-7 added, rollback added, post-migration checklist added, second sensitivity test added. The 89-agent migration tables are complete and verified accurate.

**New gaps introduced by revision:**

1. **mcp-tool-standards.md Agent Integration Matrix draft still absent.** The Schema and Rule Update Plan (line 525) describes what the change should be ("Update Agent Integration Matrix tier references; add MCP-M-001 reference to T3 tier; update constraint language") but does not provide the replacement content inline. This was flagged in iteration 1 as Priority 4 with the note "For P0 changes, the draft content should be included." Iteration 2 does not resolve this. The agent-development-standards.md changes are fully drafted (lines 558–583); the mcp-tool-standards.md changes are not. Asymmetric treatment of two P0 files reduces completeness.

2. **T5 naming in DX table.** The DX Considerations tier table (line 629) shows T5 Full Name as "Full (Persistent + External + Agent)". Every other section in the ADR names T5 "Orchestration": the New Tier Model table (line 114), the Options diagram (line 153), the Migration table (line 312), the agent-development-standards.md draft (line 566). The DX table uses "Full" — a leftover from the old model name. This is a minor but visible incompleteness in the DX section treatment.

**Improvement Path:**
Draft the mcp-tool-standards.md Agent Integration Matrix changes inline (similar to the agent-development-standards.md draft at lines 558–583). Change the T5 Full Name in the DX table from "Full (Persistent + External + Agent)" to "Orchestration (Persistent + External + Agent)" or "Orchestration."

---

### Internal Consistency (0.86/1.00)

**Evidence:**
The CRITICAL-2 arithmetic error is fully corrected. The governance-weighted score for Option A is now 8.40 (line 280), verified independently: (8×0.10)+(10×0.20)+(10×0.15)+(4×0.10)+(7×0.20)+(8×0.10)+(10×0.15) = 0.80+2.00+1.50+0.40+1.40+0.80+1.50 = 8.40 ✓. The final ranking line (295) now compares governance-weighted scores consistently: "A (8.40) > C (8.20)." Sensitivity test 2 arithmetic verified: A=7.85 ✓, C=8.30 ✓. The three-scenario summary table (lines 287–291) is internally consistent.

**New inconsistencies introduced by revision:**

1. **T5 naming conflict: "Full" vs "Orchestration"** (Severity: MEDIUM). The DX Considerations tier table (line 629) names T5 with Short Name "Orchestration" and Full Name "Full (Persistent + External + Agent)." This directly contradicts the Migration Plan (line 312: "Renamed from 'Full' to 'Orchestration'") and the Tier Reclassification Summary (line 436: "Renamed from 'Full' to 'Orchestration'"). The ADR states T5 is being renamed FROM "Full" TO "Orchestration." Yet the DX table's Full Name column uses "Full" as a component of the new T5 name. A reader of only the DX section would conclude the new T5 name includes "Full"; a reader of the Migration section would conclude "Full" is the deprecated old name.

2. **Verification total "91" inconsistency** (Severity: MEDIUM). The Post-Migration Verification Checklist (line 513) states: "Total | Sum of all counts | 91 (89 skills/ + 2 projects/ pm-pmm drafts)." The migration script glob is `skills/*/agents/*.governance.yaml` — this glob does not recurse into `projects/`. If 2 pm-pmm draft governance YAMLs exist in `projects/`, they would not be caught by the migration script, would not appear in the post-migration verification counts, and the actual count from the script would be 89. The "91" claim is inconsistent with: (a) the stated agent count "89 agents" throughout the ADR, (b) the migration script's glob pattern, and (c) the post-migration counts shown in Step 4's echo commands (lines 468–473, which also use the same `skills/*/agents/` glob). A reader following the checklist would see 89 from the script but compare against an expected 91, suggesting a defect when there is none — or would be confused about the 2 extra files.

**Gaps:**
No residual arithmetic errors found. The sensitivity analysis three-scenario table is correctly interpreted. The options analysis structural claims are mutually consistent. The T5 and "91" issues are the only material inconsistencies.

**Improvement Path:**
In the DX table, change T5 Full Name from "Full (Persistent + External + Agent)" to "Orchestration (Persistent + External + Agent)" to match the migration-established name. In the verification checklist, either: (a) remove the "91" claim and explain that the migration script covers only `skills/*/agents/` (89 files), or (b) clarify that 2 additional governance files exist in `projects/` outside the migration scope and that the migration does not and should not touch them (with a corresponding pre-verification note).

---

### Methodological Rigor (0.91/1.00)

**Evidence:**
The weight justification is now explicit and principled (lines 237–242). Three-band derivation traces to the ADR's own decision type ("governance infrastructure restructuring") and maps to agent-development-standards.md design principles. The FMEA now covers 7 failure modes including the two highest-RPN items (FM-6=120, FM-5=105). SAE J1739 is cited as the scale reference. The second sensitivity test (migration-weighted) tests the migration cost dimension specifically, which was the only dimension where Option C has a large advantage over Option A — a well-targeted perturbation. The three-scenario interpretation correctly identifies governance-weighted as the most appropriate for a C4 rule-file change, tracing to AE-002.

**Minor gaps:**

1. The FMEA FM-5 mitigation ("Strengthen MCP-002 key namespace governance; add collision detection in MK usage") references future tooling that does not yet exist. The ADR should note whether this mitigation is pre-migration (required before the PR can merge) or post-migration (tracked separately). As written, it is ambiguous.

2. Iteration 1 suggested three sensitivity test variations; the revision added one additional test (2 total). The third suggested test (Monotonicity removed) was not added. At 2 tests, the coverage is materially stronger than iteration 1 (which had 1 test), and the chosen tests target the most relevant weight perturbations. This is an acceptable scope decision, not a gap requiring correction at this quality level.

**Improvement Path:**
Clarify whether FM-5 mitigation is required before migration PR merge or a separate follow-on item. This would sharpen the FMEA from a risk documentation tool to an actionable gate list.

---

### Evidence Quality (0.88/1.00)

**Evidence:**
The migration script is now correct and executable. The three-step protection pattern (T3_HOLD) elegantly solves the ordering problem for ts-parser and ts-extractor. The `grep -rl 'tool_tier:.*T3'` broad pattern correctly catches both `tool_tier: T3` and `tool_tier: "T3"`. The two sed commands per file (`s/tool_tier: T3$/tool_tier: T4/` and `s/tool_tier: "T3"$/tool_tier: "T4"/`) correctly handle both quoted and unquoted forms with end-of-line anchors to prevent partial matches.

The rollback script mirrors the forward migration with symmetric T4_HOLD protection. A subtle point: the rollback Step 2 `grep -rl 'tool_tier:.*T4'` pattern would include the T4_HOLD files in its file list (since T4_HOLD contains "T4"), but the sed commands `s/tool_tier: T4$/tool_tier: T3/` and `s/tool_tier: "T4"$/tool_tier: "T3"/` use end-of-line anchors, so T4_HOLD would not match. The rollback is correct, though this interaction is not documented in the script comments — a reader reviewing the rollback would need to reason through this behavior.

Codebase verification confirmed: 5 pm-pmm agents (`pm-product-strategist`, `pm-market-strategist`, `pm-customer-insight`, `pm-competitive-analyst`, `pm-business-analyst`) do use `tool_tier: "T3"` (quoted form).

**Remaining gap:**

The pre-migration audit for Memory-Keeper declarations in current T3 agents is still absent. Iteration 1 flagged: "Add a pre-migration audit confirming none of the 49 T3 agents currently declare memory-keeper in their .md frontmatter." The Consequences section (line 601) states "actual MK access requires adding `mcpServers: memory-keeper: true` in the .md frontmatter" — implying no current T3 agents have this. But this claim is not verified. If any T3 agent already declares `mcpServers: memory-keeper: true` in its frontmatter, it would be operating outside its declared tier today (a T3 agent with MK tools). The pre-migration audit would surface this. Without the audit, the evidence for the claim "the migration is entirely governance classification, no agent gains actual tool access" (Consequences Neutral #2) is incomplete.

**Improvement Path:**
Add pre-migration audit command to Migration Execution Step 0: `grep -rl 'memory-keeper' skills/*/agents/*.md` — any hits outside the known 7 T4 agents would indicate an anomaly requiring investigation before the PR merges.

---

### Actionability (0.88/1.00)

**Evidence:**
The migration is now fully actionable. The three-step migration script is executable and handles all known edge cases. The rollback script mirrors it completely. The post-migration verification checklist (7 checks, lines 504–513) provides expected counts after migration. The pre-migration Step 0 echo block (lines 444–450) establishes a baseline for comparison. The new tier table and selection guidelines for agent-development-standards.md are written out in full and ready to copy-paste (lines 558–583).

**Remaining gap:**

The mcp-tool-standards.md Agent Integration Matrix draft is still absent. The Schema and Rule Update Plan describes the required change (line 525): update tier references, add MCP-M-001 reference to T3, update constraint language from "T4 agents MUST follow MCP key namespace" to "T3+ agents with Memory-Keeper MUST follow MCP key namespace." But unlike the agent-development-standards.md changes which are drafted in full (new tier table, selection guidelines, tier constraints — ready for implementation), the mcp-tool-standards.md changes require a reviewer to independently author the replacement content. For a P0 change to a file with 15+ tier references, this is a meaningful actionability gap. The ADR author would need to open mcp-tool-standards.md, identify each reference, and determine the appropriate replacement — work that should be done in the ADR.

**Improvement Path:**
Draft the mcp-tool-standards.md Tier Constraints section update inline, parallel to the agent-development-standards.md draft. At minimum, provide: (1) the replacement Tier Constraints table row for the MK namespace rule, and (2) the replacement summary line in the Selection Guidelines T3/T4 section. This would make the P0 change immediately implementable by a developer who has only read the ADR.

---

### Traceability (0.91/1.00)

**Evidence:**
All three iteration 1 traceability gaps are closed:
- FMEA S/O/D scale now cites SAE J1739 (line 683): "Scale adapted from SAE J1739 for governance artifacts."
- Weight derivation traces to agent-development-standards.md design principles ("Always select the lowest tier that satisfies requirements" = least privilege, "Each tier strictly adds capability" = monotonicity, H-35 = constitutional constraint) — lines 238–241.
- Governance-weighted justification (line 293) traces to "principle of least privilege explicitly stated as a tier selection guideline in agent-development-standards.md."

The recommendation section's 5 justifications each trace to a specific artifact: (1) risk comparison table, (2) ts-parser/extractor count, (3) 5 cross-tier agents, (4) MCP-M-001, (5) T2 checkpoint preservation. The Compliance section maps to AE-002, H-35, and constitutional principles P-003, P-020, P-022.

**Minor gap:**

The scope verification note (lines 533–538) claims grep-verified counts ("30+ references," "15+ references") but these are approximate and not attributed to a specific grep invocation that could be reproduced. For a C4 ADR, the exact command and output would provide stronger traceability than qualitative approximations. This is a minor issue at this quality level.

**Improvement Path:**
Replace qualitative approximations ("30+ references," "15+ references") with exact grep invocations and output counts. Example: "As of 2026-03-28: `grep -c 'T[1-5]' .context/rules/agent-development-standards.md` → 47 matches."

---

## New Issues Introduced by Revision (Priority Ordered)

| # | Issue | Dimension Impact | Severity |
|---|-------|-----------------|---------|
| N-1 | T5 naming conflict: DX table Full Name uses "Full" (old model name) while every other section uses "Orchestration" (new name) | Internal Consistency, Completeness | MEDIUM |
| N-2 | Verification checklist total "91" inconsistent with "89 agents" claimed throughout; migration script glob covers only 89 files in `skills/*/agents/` | Internal Consistency | MEDIUM |
| N-3 | mcp-tool-standards.md P0 content described but not drafted inline (pre-existing gap, not resolved in iteration 2) | Completeness, Actionability | MEDIUM |
| N-4 | Pre-migration MK audit absent (pre-existing gap, not resolved in iteration 2) | Evidence Quality | LOW |
| N-5 | Rollback Step 2 T4_HOLD-T4 interaction undocumented (subtle correctness point not apparent to casual reviewer) | Evidence Quality | LOW |
| N-6 | FM-5 mitigation ambiguity: pre-migration required vs post-migration optional | Methodological Rigor | LOW |

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.86 | 0.92 | Fix T5 Full Name in DX table from "Full (Persistent + External + Agent)" to "Orchestration (Persistent + External + Agent)". Resolve "91 vs 89" by removing the "(89 skills/ + 2 projects/ pm-pmm drafts)" claim and replacing with a note that the script covers `skills/*/agents/*.governance.yaml` (89 files; projects/ excluded from migration scope). |
| 2 | Completeness + Actionability | 0.90/0.88 | 0.93/0.92 | Draft the mcp-tool-standards.md Agent Integration Matrix tier-reference updates inline (tier constraints table row for MK namespace rule, updated selection guideline for T3/T4). This is a P0 change that should be immediately implementable from the ADR without opening the target file. |
| 3 | Evidence Quality | 0.88 | 0.92 | Add pre-migration audit command to Step 0: `grep -rl 'memory-keeper' skills/*/agents/*.md` — expected: only the 7 known T4 agents. Any additional hits indicate a governance anomaly requiring investigation before the PR merges. |
| 4 | Evidence Quality | 0.88 | 0.90 | Add a comment to Rollback Step 2 explaining that T4_HOLD files will be returned by the grep but will not be modified by the sed (end-of-line anchors prevent T4_HOLD from matching T4$). This prevents a reviewer from incorrectly flagging the rollback as buggy. |
| 5 | Methodological Rigor | 0.91 | 0.93 | Clarify FM-5 mitigation (MK collision detection): state whether this must be implemented before the migration PR merges (blocking) or is a separate tracked item (non-blocking). |
| 6 | Traceability | 0.91 | 0.93 | Replace qualitative scope approximations ("30+ references") with exact grep commands and counts. |

---

## Score Delta Analysis (Iteration 1 → Iteration 2)

| Dimension | Iter 1 Score | Iter 2 Score | Delta | Change Driver |
|-----------|-------------|-------------|-------|--------------|
| Completeness | 0.88 | 0.90 | +0.02 | 7 gaps closed; new T5/mcp gaps partially offset improvement |
| Internal Consistency | 0.82 | 0.86 | +0.04 | Arithmetic fixed; new T5 and "91" inconsistencies introduced |
| Methodological Rigor | 0.90 | 0.91 | +0.01 | FM-6/FM-7 + SAE J1739 + weight derivation + 2nd sensitivity test |
| Evidence Quality | 0.78 | 0.88 | +0.10 | CRITICAL-1 script bug fixed; rollback added; pre-MK audit still absent |
| Actionability | 0.85 | 0.88 | +0.03 | Rollback + verification checklist added; mcp draft still absent |
| Traceability | 0.87 | 0.91 | +0.04 | SAE J1739 + weight bands + governance-weighted justification |
| **Composite** | **0.852** | **0.889** | **+0.037** | |

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite computation
- [x] Evidence documented for each score with specific line references
- [x] Uncertain scores resolved downward (Internal Consistency: chose 0.86 not 0.88 given two new inconsistencies; Evidence Quality: chose 0.88 not 0.90 given pre-MK audit gap)
- [x] C4 calibration applied: 0.95 user threshold; neither standard gate (0.92) nor C4 threshold (0.95) is met
- [x] No dimension scored above 0.95
- [x] Fix verification performed independently against actual ADR content before scoring, not taken at face value from task description
- [x] New issues (N-1 through N-6) actively searched for, not just iteration 1 confirmation

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.889
threshold_standard: 0.92
threshold_requested: 0.95
weakest_dimension: internal_consistency
weakest_score: 0.86
critical_findings_count: 0
new_issues_count: 3
iteration: 2
delta_from_iteration_1: +0.037
improvement_recommendations:
  - "Fix T5 naming in DX table (Full Name uses old 'Full'; should be 'Orchestration (Persistent + External + Agent)')"
  - "Resolve '91 vs 89 agents' inconsistency in verification checklist total"
  - "Draft mcp-tool-standards.md Agent Integration Matrix changes inline (P0 change, currently described-not-drafted)"
  - "Add pre-migration MK audit command to Step 0 (verify no current T3 agents declare memory-keeper)"
  - "Add comment to Rollback Step 2 explaining T4_HOLD/T4$ end-of-line anchor interaction"
  - "Clarify FM-5 mitigation as blocking vs non-blocking for migration PR"
```
