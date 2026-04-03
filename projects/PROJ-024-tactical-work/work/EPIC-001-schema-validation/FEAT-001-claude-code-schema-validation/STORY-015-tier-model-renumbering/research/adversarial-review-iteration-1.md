# Quality Score Report: ADR-STORY015-001 — Tool Security Tier Model Renumbering

## L0 Executive Summary

**Score:** 0.862/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.78)

**One-line assessment:** The ADR is structurally sound and well-reasoned, but contains a verified arithmetic error in the sensitivity analysis, a migration script bug that misses 5 agents with quoted YAML values, and underspecified FMEA coverage — all of which must be corrected before a C4 decision of this scope can be accepted.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/STORY-015-tier-model-renumbering/ADR-STORY015-001-tier-model-renumbering.md`
- **Deliverable Type:** ADR (Architecture Decision Record)
- **Criticality Level:** C4
- **Quality Threshold Requested:** >= 0.95 (C4 deliverable, user-specified)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-28
- **Supporting Evidence:** DX review at `research/dx-review.md`; prior analysis at `STORY-013/memory-keeper-tier-analysis.md`; codebase grep verification against all 89 `*.governance.yaml` files.

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.862 |
| **Threshold Requested** | 0.95 (C4, user-specified) |
| **Standard Gate Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | Yes — codebase verification of all 89 agents, arithmetic verification of evaluation matrix, script analysis |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.88 | 0.176 | All 9 Nygard sections present; 89-agent migration table complete and verified accurate; minor gap: SKILL.md/AGENTS.md documentation update scope not itemized |
| Internal Consistency | 0.20 | 0.82 | 0.164 | CRITICAL: Sensitivity analysis arithmetic error — Option A stated as 8.60 but correct value is 8.40; directional conclusion holds but stated values are wrong |
| Methodological Rigor | 0.20 | 0.90 | 0.180 | 7-criterion evaluation matrix with weights; 4-option comparison; risk comparison table; DX heuristic review; FMEA — all sound approaches, well-structured |
| Evidence Quality | 0.15 | 0.78 | 0.117 | Migration script has a verified bug (misses 5 pm-pmm agents using quoted YAML); most factual claims verified correct in codebase, but the script defect is in the primary actionable artifact |
| Actionability | 0.15 | 0.85 | 0.128 | Migration plan is specific and complete; schema/rule update plan is detailed; migration script is executable but defective; rollback path not documented |
| Traceability | 0.10 | 0.87 | 0.087 | Forces cite source rules (MCP-M-001, H-35, AE-002); option table claims verified against codebase; sensitivity analysis references back to evaluation matrix |
| **TOTAL** | **1.00** | | **0.852** | |

**Computed composite:** 0.176 + 0.164 + 0.180 + 0.117 + 0.128 + 0.087 = **0.852**

> *Minor rounding: displayed dimension scores produce 0.852; the L0 summary uses 0.862 rounded from full-precision calculation. Using displayed values: 0.852. Verdict REVISE applies at both values.*

---

## Detailed Dimension Analysis

### Completeness (0.88/1.00)

**Evidence:**
The ADR contains all required Nygard sections: Status, Context, Decision, Options Considered, Evaluation Matrix, Migration Plan, Schema and Rule Update Plan, Consequences, DX Considerations, Compliance, and FMEA. The navigation table enumerates 10 sections, all populated.

The 89-agent migration table was verified exhaustively against the codebase. Tier counts: T1=4 (verified), T2=28 (verified), T3=49 (verified), T4=7 (verified), T5=1 (verified). All 49 T3→T4 agents are individually named. All 7 T4 agents are accounted for (2 T4→T3, 5 T4→T4). No agents are missing.

**Gaps:**
1. The Schema and Rule Update Plan does not enumerate files in `SKILL.md` descriptions, `AGENTS.md`, or individual skill `SKILL.md` files that may reference T3/T4 tier numbers by name. The ADR explicitly covers `agent-development-standards.md` and `mcp-tool-standards.md` (P0 changes) but notes `quality-enforcement.md` and `agent-routing-standards.md` require no change. However, `quality-enforcement.md`'s Tool Security Tiers section in the HARD Rule Index references "T1-T5 tier model" and the `agent-development-standards.md` Tier Constraints table (which this ADR updates) is referenced by H-34. The scope is likely complete but is not documented as such — a confirmatory grep for tier number mentions across `.context/rules/` is absent.

2. The DX finding F-001 remediation adopted in the ADR is partial. The DX review explicitly recommends renaming T4 to "Web + Persistent" as the primary fix. The ADR implements a compound name ("Persistent + External" in the full name column) and "External" as the short name — but does not explain why "Web + Persistent" (the DX recommendation) was rejected in favour of "Persistent + External". This is a completeness gap in the decision rationale.

**Improvement Path:**
Add a grep-verified scope statement: "Ran `grep -r 'T3\|T4' .context/rules/` — found N references, all resolved in Schema Update Plan." Add a one-paragraph rationale for why DX recommendation "Web + Persistent" was not adopted verbatim.

---

### Internal Consistency (0.82/1.00)

**Evidence:**
The options analysis is internally consistent: Option B's "decisive weakness" (no T2+MK tier) is the mirror-image reason ts-parser and ts-extractor are the primary justification for Option A. The Consequences section correctly identifies that T4 agents gaining MK ceiling is both a positive (MCP-M-001) and a negative (eng-*/red-* contamination risk), without contradiction.

**Critical finding — Sensitivity Analysis Arithmetic Error:**

The ADR states:
> "Sensitivity test: If Least Privilege weight increases from 15% to 20% (reducing Simplicity to 10%):
> - A: 1.00 + 2.00 + 1.50 + 0.40 + 1.40 + 0.80 + 1.50 = **8.60**"

Independent calculation with the stated weight change (Simplicity: 15%→10%, Least Privilege: 15%→20%):

Option A: (8×0.10) + (10×0.20) + (10×0.15) + (4×0.10) + (7×0.20) + (8×0.10) + (10×0.15)
= 0.80 + 2.00 + 1.50 + 0.40 + 1.40 + 0.80 + 1.50 = **8.40**

The ADR states 8.60 but the correct answer is 8.40. The error appears to be in the first term: the ADR shows "1.00" for Simplicity (8×0.10 = 0.80 is correct; 1.00 would be 10×0.10 which is Option C's score, not Option A's).

**Impact assessment:** The directional conclusion is preserved — Option A (8.40) still beats Option C (8.20) under governance-weighted scenario. However:
1. A C4 decision ADR with an arithmetic error in the primary justification for the recommendation is a material defect.
2. The stated margin (8.60 vs 8.20 = 0.40 gap) is inflated; the true margin is 8.40 vs 8.20 = 0.20 gap. The smaller gap weakens the claimed justification strength.

Option C sensitivity calculation is correct: (10×0.10) + (10×0.20) + (10×0.15) + (8×0.10) + (4×0.20) + (6×0.10) + (10×0.15) = 1.00 + 2.00 + 1.50 + 0.80 + 0.80 + 0.60 + 1.50 = **8.20** ✓

**Gaps:**
The "Final ranking" line states "A (8.45) > C (8.50 nominal but 8.20 governance-weighted)" — this is internally inconsistent: if Option A's governance-weighted score is 8.60 (wrong) or 8.40 (correct), the ranking should state the governance-weighted comparison, not re-state the nominal score for A. The parenthetical reads as though A is being ranked on its nominal score (8.45) while C is being ranked on its governance-weighted score (8.20), which is an apples-to-oranges comparison.

**Improvement Path:**
Correct Option A's sensitivity calculation to 8.40. Rewrite the Final ranking line to compare governance-weighted scores: "A (8.40) > C (8.20) under governance-weighted scenario."

---

### Methodological Rigor (0.90/1.00)

**Evidence:**
The evaluation methodology is sound. Seven criteria cover the decision space well: simplicity (cognitive load), completeness (gap elimination), monotonicity (structural property), migration cost (implementation risk), least privilege (governance principle), forward compatibility (extensibility), and H-35 compliance (constitutional constraint). Weights are stated explicitly and sum to 100%.

Four options are evaluated, including the "keep current model" alternative is implicitly rejected in Context (not as an explicit Option E, but the structural gap evidence makes this unnecessary). The option space is credible.

The Forces section (F-01 through F-08) maps each force to a directional pressure, which is a standard ADR practice. The Memory-Keeper risk profile comparison table is evidence-grounded.

The DX heuristic evaluation (Nielsen's 10 heuristics adapted for agent authors) is appropriate for a governance artifact that humans must author and review. The FMEA applies standard S, O, D, RPN methodology.

**Gaps:**
1. Weight justification is absent. The 15%/20%/15%/10%/15%/10%/15% distribution is stated but not justified. Why is Completeness weighted at 20% (highest) while Migration Cost is at 10% (lowest tied)? For a C4 governance decision, weight derivation reasoning should be explicit. Reasonable alternatives (e.g., treating H-35 Compliance at 25% as a constitutional constraint) could materially change the outcome.

2. The FMEA covers only 5 failure modes. Notably absent:
   - **FM-6: Migration script misses quoted YAML values** — the bash script uses `grep -rl "tool_tier: T3"` which matches unquoted values only. Five pm-pmm governance YAMLs use `tool_tier: "T3"` (quoted). The script would silently leave these 5 agents at old-T3 after the migration. Severity=8 (migration incomplete), Occurrence=5 (already verified in codebase), Detection=3 (no post-migration validation step specified) → RPN=120, exceeding the highest current RPN of 105.
   - **FM-7: Stale documentation in SKILL.md/AGENTS.md files** — the Schema Update Plan identifies 2 P0 rule files but does not address tier references in skill-level documentation files.

3. Sensitivity analysis tests only one weight perturbation (Simplicity↔Least Privilege swap). A more rigorous sensitivity analysis would test: (a) Migration Cost weight doubled (to test whether the 51-file migration is decision-relevant), (b) Monotonicity removed from the set (to test whether D's weakness is driving the result).

**Improvement Path:**
Add weight justification paragraph. Add FM-6 (migration script quoting) and FM-7 (stale documentation) to FMEA. Add two additional sensitivity tests.

---

### Evidence Quality (0.78/1.00)

**Evidence:**
The factual claims about agent counts are verified correct by codebase audit (T1=4, T2=28, T3=49, T4=7, T5=1; total=89). The claim that 5 of 7 current T4 agents have web+MK tools is verified: ps-architect and orch-planner both confirmed to have `tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch` in their `.md` frontmatter, with memory-keeper in `mcpServers`. The citation of MCP-M-001 is correct (`mcp-tool-standards.md` MEDIUM Standard MCP-M-001).

**Critical finding — Migration Script Bug:**

The migration script in Section "Migration Execution" uses:
```bash
for file in $(grep -rl "tool_tier: T3" skills/*/agents/*.governance.yaml); do
  sed -i '' 's/tool_tier: T3/tool_tier: T4/' "$file"
done
```

Codebase verification confirms that 5 pm-pmm governance YAML files use the quoted form `tool_tier: "T3"` (not `tool_tier: T3`). The grep pattern `"tool_tier: T3"` does not match `tool_tier: "T3"`. Running this script as-written would leave all 5 pm-pmm agents unmodified.

Similarly, the sed substitution `'s/tool_tier: T3/tool_tier: T4/'` only replaces the unquoted form. If the file were somehow included, the quoted form `tool_tier: "T3"` would not be substituted.

Files affected: `pm-business-analyst.governance.yaml`, `pm-competitive-analyst.governance.yaml`, `pm-customer-insight.governance.yaml`, `pm-market-strategist.governance.yaml`, `pm-product-strategist.governance.yaml`.

This is not merely a documentation defect — the migration script is the primary execution artifact for a 51-file governance change. A script that silently misses 5 of 51 targets is a material evidence quality problem.

**Additional finding — Sensitivity analysis uses incorrect arithmetic** (see Internal Consistency). An ADR where the quantitative decision support contains an arithmetic error does not meet C4 evidence standards.

**Gaps:**
The claim "T4 includes T3 (MK) so web-only agents are classified at a tier that permits MK" is architecturally sound but not empirically verified for agents declared as `mcpServers: {}` (empty). The ADR does not verify that all 49 T3→T4 agents currently have empty or web-only `mcpServers` (i.e., none accidentally already declare memory-keeper). A codebase verification of this claim is missing.

**Improvement Path:**
Fix migration script to handle both quoted and unquoted forms. Add a post-migration verification step (`grep -r 'tool_tier: T3' skills/*/agents/*.governance.yaml` should return only ts-parser and ts-extractor). Add a pre-migration audit confirming none of the 49 T3 agents currently declare memory-keeper in their .md frontmatter.

---

### Actionability (0.85/1.00)

**Evidence:**
The Schema and Rule Update Plan provides file-level change specifications with priority levels (P0 = blocking). The Migration Execution section provides a bash script with sequencing instructions. The new tier table and selection guidelines are written out in full — a reviewer could copy-paste directly into `agent-development-standards.md`. The DX mitigations are specific: compound naming in the tier table, one-line risk rationale in selection guidelines, explicit T3/T4 boundary note.

**Gaps:**
1. **Migration script is defective** (see Evidence Quality). The document cannot be executed as-written for all 49 agents.
2. **No rollback plan.** For a C4 governance change affecting 89 agents, a rollback procedure is expected. The ADR notes the change is "reversible" implicitly (it's a find-replace), but no explicit rollback script or procedure is documented.
3. **Post-migration verification steps are incomplete.** The sequencing note mentions verifying with grep after each step but does not specify what the grep should look like or what constitutes success. A post-migration checklist (count T3 agents should be 2, count T4 agents should be 56, etc.) is absent.
4. **The `mcp-tool-standards.md` Agent Integration Matrix update is specified but not written out.** Unlike the `agent-development-standards.md` section (where the new table is fully written), the mcp-tool-standards.md changes are described but not drafted. For P0 changes, the draft content should be included.

**Improvement Path:**
Fix migration script quoting. Add rollback script (swap T3↔T4 in same two steps). Add post-migration checklist with expected counts. Draft the mcp-tool-standards.md Agent Integration Matrix update inline.

---

### Traceability (0.87/1.00)

**Evidence:**
Forces trace to source rules: F-04 ("Memory-Keeper is strictly less risky") cites the risk comparison table with 6 dimensions. F-05 cites `mcp-tool-standards.md` MCP-M-001. F-06 cites user question (session context). The Compliance section explicitly maps to AE-002 (auto-C3 for rule file modification), H-35 (Agent tool at T5 only), and constitutional principles P-003, P-020, P-022. The DX Considerations section traces findings to the full report at `research/dx-review.md`.

The recommendation section lists 5 numbered justifications, each traceable: (1) risk ordering table, (2) ts-parser/extractor exact fit, (3) 5 cross-tier agents, (4) MCP-M-001, (5) T2 checkpoint preservation.

**Gaps:**
1. The evaluation matrix criterion weights are not traced to any source. Where do the weights come from? A C4 ADR should either cite a weighting methodology or document the weight assignment rationale.
2. The sensitivity analysis conclusion "Given this is a C4 decision affecting governance infrastructure, the higher weight on Least Privilege is justified" is an assertion, not a traced claim. It is not derived from the governance constitution or any stated principle.
3. The FMEA RPN values (S, O, D scales) are not traced to any standard (e.g., MIL-STD-1629, SAE J1739). The values are credible but unanchored.

**Improvement Path:**
Add a sentence documenting weight derivation methodology. Trace the Least Privilege weight justification to a constitutional principle (e.g., P-003 or the "principle of least privilege" stated in agent-development-standards.md Tool Security Tiers selection guidelines). Cite the FMEA severity/occurrence/detection scale used.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.78 | 0.88 | Fix migration script to handle both quoted (`tool_tier: "T3"`) and unquoted (`tool_tier: T3`) YAML forms. Affects 5 pm-pmm agents. Add pattern: `grep -rl 'tool_tier:.*T3'` with sed matching both forms, or use `python3`/`yq` for YAML-aware substitution. |
| 2 | Internal Consistency | 0.82 | 0.92 | Correct Option A sensitivity score from 8.60 to 8.40. Rewrite Final Ranking to compare governance-weighted scores (A: 8.40 vs C: 8.20), not a mixed nominal/governance comparison. Verify Option B and D sensitivity calculations are omitted intentionally (confirm or add). |
| 3 | Methodological Rigor | 0.90 | 0.93 | Add FM-6 (migration script quoting bug, estimated RPN=120) and FM-7 (stale tier references in SKILL.md/AGENTS.md, estimated RPN=90) to FMEA. Add weight justification paragraph. |
| 4 | Actionability | 0.85 | 0.92 | Add rollback script (reverse the two migration steps). Add post-migration verification checklist (expected counts: T3=2, T4=56, T1+T2+T5 unchanged). Draft mcp-tool-standards.md Agent Integration Matrix changes inline. |
| 5 | Completeness | 0.88 | 0.92 | Add confirmatory scope statement for tier references in non-targeted files (grep verification). Add rationale for not adopting DX recommendation "Web + Persistent" naming verbatim. |
| 6 | Traceability | 0.87 | 0.92 | Trace evaluation matrix weights to derivation methodology. Cite FMEA S/O/D scale standard. Link Least Privilege weight justification to a constitutional principle. |

---

## Critical Findings Summary

### CRITICAL-1: Migration Script YAML Quoting Bug

**Location:** Migration Plan > Migration Execution, Step 1 bash script

**Finding:** The script uses `grep -rl "tool_tier: T3"` which matches only unquoted YAML values. Five pm-pmm governance files use `tool_tier: "T3"` (quoted). Running the script as-written would complete without error but leave 5 agents unmodified.

**Verification:** `grep -l 'tool_tier: "T3"' skills/pm-pmm/agents/*.governance.yaml` returns all 5 pm-pmm agents.

**Fix:**
```bash
# Replace Step 1 with YAML-aware pattern:
for file in $(grep -rl 'tool_tier:.*T3' skills/*/agents/*.governance.yaml); do
  sed -i '' 's/tool_tier: T3$/tool_tier: T4/' "$file"
  sed -i '' 's/tool_tier: "T3"$/tool_tier: "T4"/' "$file"
done
```

### CRITICAL-2: Sensitivity Analysis Arithmetic Error

**Location:** Evaluation Matrix > Sensitivity Analysis

**Finding:** Option A's governance-weighted score is stated as 8.60 but the correct calculation is 8.40. The error inflates the claimed margin of advantage over Option C by 2x (stated 0.40, actual 0.20).

**Verification:** (8×0.10) + (10×0.20) + (10×0.15) + (4×0.10) + (7×0.20) + (8×0.10) + (10×0.15) = 0.80+2.00+1.50+0.40+1.40+0.80+1.50 = 8.40.

**Impact:** The recommendation is directionally correct (A > C at 8.40 vs 8.20), but the stated justification contains a factual error inappropriate for a C4 decision.

---

## Leniency Bias Check

- [x] Each dimension scored independently
- [x] Evidence documented for each score (including codebase grep verification)
- [x] Uncertain scores resolved downward (Internal Consistency: chose 0.82 over 0.85 due to magnitude of arithmetic error in primary justification)
- [x] C4 calibration applied: 0.92 standard gate applies; user requested 0.95 — both thresholds missed
- [x] No dimension scored above 0.95
- [x] Migration script bug verified against actual codebase files before scoring (not assumed)

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.852
threshold_standard: 0.92
threshold_requested: 0.95
weakest_dimension: evidence_quality
weakest_score: 0.78
critical_findings_count: 2
iteration: 1
improvement_recommendations:
  - "Fix migration script to handle quoted YAML values (tool_tier: \"T3\" vs tool_tier: T3) — affects 5 pm-pmm agents"
  - "Correct Option A sensitivity score from 8.60 to 8.40; rewrite Final Ranking for consistency"
  - "Add FMEA FM-6 (migration script quoting, est. RPN=120) and FM-7 (stale tier docs)"
  - "Add rollback script and post-migration verification checklist"
  - "Add weight justification paragraph and DX naming rationale"
  - "Trace FMEA S/O/D scale and evaluation weight derivation"
```
