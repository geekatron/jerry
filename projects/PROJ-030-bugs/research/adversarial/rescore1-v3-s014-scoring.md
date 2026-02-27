# Quality Score Report: Claude Code MCP Tool Permission Model (Re-score 2 / Iteration 3)

## L0 Executive Summary

**Score:** 0.919/1.00 | **Verdict:** REVISE | **Weakest Dimensions:** Evidence Quality (0.90) / Traceability (0.90) (tied)
**One-line assessment:** Revision cycle 2 closed all four targeted blockers and produced meaningful gains across Internal Consistency (+0.03), Methodological Rigor (+0.04), Evidence Quality (+0.08), and Traceability (+0.08), but the composite of 0.919 is 0.001 below the H-13 standard threshold (0.92) and 0.031 below the C4 user-specified threshold (0.95); remaining gaps are narrow and targeted: the `allowed_tools` citation gap, the CLI verification command absence, and the informal worktracker next-steps.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-030-bugs/research/context7-permission-model.md`
- **Deliverable Type:** Research
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Quality Threshold (user-specified):** 0.95 (C4)
- **Standard H-13 Threshold:** 0.92 (C2+)
- **Prior Score:** 0.893 (Iteration 2)
- **Scored:** 2026-02-26T00:00:00Z
- **Iteration:** 3 (second re-score after two revision cycles)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.919 |
| **H-13 Standard Threshold** | 0.92 (C2+) |
| **C4 User-Specified Threshold** | 0.95 |
| **Verdict** | REVISE (below both thresholds) |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.92 | 0.184 | All 4 RQs answered; 35-file inventory; empirical verification; scope selection added; no new gaps introduced; CLI verification command still absent from migration step 6 |
| Internal Consistency | 0.20 | 0.93 | 0.186 | Scope selection paragraph added (lines 326-334); user-scope vs project-scope tension resolved; risk table mitigation now consistent; residual `allowed_tools`/HIGH credibility tension minor but present |
| Methodological Rigor | 0.20 | 0.92 | 0.184 | Wildcard timeline explicitly pinned (July vs December 2025 issue closure dates at line 117); risk likelihood cells now include parenthetical rationale; both targeted gaps from P3 closed |
| Evidence Quality | 0.15 | 0.90 | 0.135 | L1 body `~/.claude/settings.json` absence claim corrected to "could not be verified (permission denied)" (line 221); `.mcp.json` Glob note added; prior contradiction eliminated; Context7 GitHub source coarseness and formula-generalizability limitation persist |
| Actionability | 0.15 | 0.93 | 0.1395 | 6-step migration, acceptance criteria, rollback procedure unchanged from iteration 2; none of the P5 actionability gaps were in scope for this revision cycle; formal action items list and CLI verification command still absent |
| Traceability | 0.10 | 0.90 | 0.090 | BUG-001 entity file path now present (line 460); repo-relative paths used throughout prose for `.context/rules/mcp-tool-standards.md` and `.context/rules/agent-development-standards.md`; `mcpServers` back-citation added (line 371); `allowed_tools` "NOT a standard field" claim still uncited |
| **TOTAL** | **1.00** | | **0.919** | |

---

## Detailed Dimension Analysis

### Completeness (0.92/1.00)

**Evidence:**
This dimension is unchanged from iteration 2. All four research questions are answered. The 35-file affected inventory, Memory-Keeper note, Empirical Verification section, and `allowed_tools` status discussion remain fully present. The scope selection paragraph (new in this revision) adds explanatory depth to the migration path. No regression observed.

The verification gap from iteration 2 persists: migration step 6 says "In a new Claude Code session, confirm" but specifies no CLI command (e.g., `claude mcp list`, `--debug` flag invocation, or equivalent). The acceptance criteria state *what* to confirm but not *how* to observe it. A developer executing the migration must determine the observation method independently.

**Gaps:**
- Migration step 6 lacks a specific CLI command or observation method for post-migration verification. The acceptance criteria specify correct outcomes but no mechanism to check them.

**Improvement Path:**
Add one line to step 6: `# Observation: run \`claude mcp list\` in a new session and confirm mcp__context7__ tools appear (not mcp__plugin_context7_context7__).`

---

### Internal Consistency (0.93/1.00)

**Evidence:**
Fix 4 is fully applied. Lines 326-334 add an explicit "Scope selection" paragraph that states: "User scope (`--scope user`) is recommended as the primary installation method because it is consistent with how Memory-Keeper is configured (standalone MCP server) and applies across all projects without per-project setup." The project-scope alternative is acknowledged and positioned as valid for team environments. The risk table mitigation (line 362) now reads "Add to project-scoped `.mcp.json` for automatic configuration" — correctly framed as a fallback/alternative rather than a contradiction of the user-scope recommendation. The tension flagged in iteration 2 is resolved.

Residual gap: The L3 section characterizes `.claude/settings.json` as credibility HIGH (as a primary source for the `enabledPlugins` finding) while simultaneously characterizing the `allowed_tools` field within that same file as "NOT a standard Claude Code permission field" and "likely ignored." A careful reader may wonder why one field of a HIGH-credibility file is trusted and another is disclaimed. The answer — that different fields serve different consumers (runtime vs. documentation) — is not stated. This is a minor expository gap, not a factual contradiction.

**Gaps:**
- The `allowed_tools` vs HIGH-credibility-source framing is not explicitly reconciled. A one-sentence clarification ("Note that `.claude/settings.json` is HIGH credibility as a primary source for the `enabledPlugins` field; the `allowed_tools` field within that file is a documentation-only construct not consumed by the Claude Code runtime.") would close this.

**Improvement Path:**
Add a clarifying sentence to the Level 3 section or the Methodology table entry for `.claude/settings.json` distinguishing which fields the runtime processes from which are documentation-only.

---

### Methodological Rigor (0.92/1.00)

**Evidence:**
Fix 3 is fully applied across both sub-gaps.

**Sub-gap 3a (wildcard version pinning):** Line 117 now explicitly states: "Issues #3107 and #2928 were closed in July 2025 (wildcards still broken), while #13077 and #14730 were closed in December 2025 (likely when the fix shipped)." This is a significant improvement from the prior "later release" vagueness. The inference is clearly labeled ("likely when the fix shipped") and grounded in the issue closure timeline data already present in the document.

**Sub-gap 3b (risk rating rationale):** Each risk likelihood cell in the risk table now includes a parenthetical rationale:
- "Medium (Claude Code release cadence is rapid; plugin manifest formats are lightly documented and subject to change without deprecation notice)"
- "Low (Context7 tools have short names; the longest observed is ~55 chars)"
- "Medium (one-time manual step per developer; no CI enforcement currently exists)"
- "Low (appears fixed in late-2025 releases based on issue closure timeline; see Section 2 above)"

These are appropriate 1-line justifications. They satisfy the C4 rigor requirement stated in the iteration 2 analysis.

Residual gap: The trade-off analysis still lacks a formal evaluation method name (e.g., weighted scoring, elimination-by-aspect). The 4-point numbered justification for Approach A implicitly demonstrates criteria-based reasoning, which partially mitigates this gap. This is the lowest-severity remaining methodological gap.

**Gaps:**
- Trade-off analysis methodology remains informal (no named decision framework). The implicit criteria-based reasoning is present but not labeled.

**Improvement Path:**
Add a one-sentence preamble to the Trade-Off Analysis: "Evaluated using criteria-based comparison across four dimensions: tool name stability, operational overhead, compliance with principle of least privilege, and team onboarding burden."

---

### Evidence Quality (0.90/1.00)

**Evidence:**
Fix 1 is the most impactful correction in this revision cycle and is fully applied.

**Prior contradiction resolved:** Line 221 now reads: "No `.mcp.json` file exists at the project root (confirmed via Glob search). User-level MCP configuration (`~/.claude/settings.json`) could not be verified (permission denied); it is unknown whether Context7 is also configured as a standalone MCP server at user scope." The Limitations section (line 398) states the same. There is no longer a contradiction between L1 body and Limitations. The iteration 2 critical gap ("These two statements remain in tension") is closed.

**`.mcp.json` Glob note added:** The parenthetical "(confirmed via Glob search)" at line 221 provides the evidence trail for the `.mcp.json` absence claim that was missing in iteration 2.

Remaining gaps:

**Gap 1 (formula generalizability):** The Empirical Verification section confirms the plugin naming formula for the specific case of `context7` plugin + `context7` server. The formula `mcp__plugin_{plugin-name}_{server-name}__{tool-name}` is still derived primarily from GitHub issue #23149. The runtime observation confirms one instance; the general formula remains issue-derived. This is acknowledged in Limitations (line 399: "The formula is derived from observed behavior reported in GitHub issues, not from an official naming specification document") and is appropriately disclosed.

**Gap 2 (Context7 GitHub source coarseness):** Reference 12 cites `https://github.com/upstash/context7` with "Installation methods" as the key insight but specifies no file, README section, or commit. A reader cannot navigate directly to the cited installation guidance. This is an unchanged gap from iteration 2.

**Score justification:** The elimination of the L1/Limitations contradiction is a material evidence integrity repair. The two remaining gaps are acknowledged limitations, not suppressions. The rubric for 0.9+ ("All claims with credible citations") is substantially met — the main claims are well-evidenced; the two remaining gaps affect secondary supporting material. The score moves from 0.82 to 0.90. Scoring at 0.90 rather than 0.92 reflects the coarse GitHub source and the formula-generalizability caveat, which are real limitations at C4 rigor.

**Gaps:**
- Context7 GitHub source (Reference 12) cites the repository URL only; no specific file, README section, or version is identified.
- Formula B generalizability: runtime observation covers one plugin/server combination; the general formula relies on issue reports.

**Improvement Path:**
Update Reference 12 to cite a specific README section or documentation file path (e.g., `README.md#installation` or the relevant section heading). Add a note in Empirical Verification acknowledging that the formula is confirmed for the `context7` case and inferred from issue patterns for other plugins.

---

### Actionability (0.93/1.00)

**Evidence:**
The actionability dimension is unchanged from iteration 2. The 6-step migration with acceptance criteria and rollback procedure remain present and represent strong actionable guidance. The scope selection paragraph (new this revision) marginally improves actionability by disambiguating the installation command for developers.

None of the iteration 2 P5 actionability gaps were in scope for this revision cycle, per the stated fix targets:

**Remaining gap 1 (informal worktracker hint):** The PS Integration section still closes with "Next agent hint: ps-architect for decision on Context7 installation method." This is an informal prose note, not a formal action item. No worktracker entity creation instruction, no GitHub issue reference, no traceable work item.

**Remaining gap 2 (Approach B file-level specifics):** The affected-file inventory identifies 35 files but does not specify what change each file needs under Approach B (which string to replace, at what location). A developer choosing Approach B has file locations but not edit instructions.

**Remaining gap 3 (CLI verification command):** Step 6 of the migration specifies acceptance criteria but no specific command to run. Cross-references with the Completeness gap.

**Score justification:** 0.93 is unchanged from iteration 2. The scope selection paragraph adds minor actionability value (clarifies which `mcp add` command variant to use) but does not close any of the three listed gaps. Holding at 0.93.

**Gaps:**
- No formal action items list with traceable worktracker entries or GitHub issues.
- Approach B does not specify per-file edit details.
- No CLI command in migration step 6 for post-migration verification.

**Improvement Path:**
Add a numbered "Action Items" list at the end of L2: (1) Create worktracker story for Context7 migration decision, (2) ps-architect decision task on Approach A vs B, (3) Update `TOOL_REGISTRY.yaml` after decision. Add `claude mcp list` to step 6.

---

### Traceability (0.90/1.00)

**Evidence:**
Fix 2 is substantially applied and represents a material improvement.

**BUG-001 entity file path (gap 1, closed):** Line 460 now contains: `Entity File: projects/PROJ-030-bugs/work/bugs/BUG-001-memory-keeper-tool-name-mismatch/BUG-001-memory-keeper-tool-name-mismatch.md`. A reader can navigate from this report to the source work item without filesystem searching. This is a complete closure of the top traceability gap.

**Repo-relative paths (gap 2, closed):** Throughout the prose, `.context/rules/mcp-tool-standards.md` and `.context/rules/agent-development-standards.md` appear with full repo-relative paths. The Affected Files Inventory table (rules section) lists `.context/rules/mcp-tool-standards.md`, `.claude/settings.local.json`, and `TOOL_REGISTRY.yaml` with correct paths. Consistent path referencing is achieved.

**`mcpServers` back-citation (gap 3, closed):** Line 371 concludes: "However, empirical verification confirms that `mcpServers: { context7: true }` does resolve correctly for plugin-installed servers at runtime [see Empirical Verification, point 3]." The traceability loop from the Level 5 claim to its supporting evidence is closed.

**Remaining gap (`allowed_tools` field claim):** Level 3 states the `allowed_tools` field in `.claude/settings.json` is "NOT a standard Claude Code permission field" and "likely ignored by Claude Code's permission system." No documentation citation confirms or denies this. The claim derives from direct file inspection plus inference from the official settings schema, but neither of these sources is cited. A note of the form "Source: direct inspection of `.claude/settings.json`; no matching field appears in the official Claude Code settings schema at [URL]" would complete the traceability chain.

**Score justification:** From 0.82 to 0.90. Three of four substantive traceability gaps are closed. The sole remaining gap (`allowed_tools` citation) is a minor omission relative to the overall traceability posture of the document. The rubric for 0.9+ ("Full traceability chain") is substantially met; the one uncited assertion prevents a higher score.

**Gaps:**
- `allowed_tools` "NOT a standard field" claim lacks a documentation or schema citation.

**Improvement Path:**
Add to the Level 3 `allowed_tools` paragraph: "(Source: direct inspection of `.claude/settings.json`; this field does not appear in the Claude Code official settings schema at [https://code.claude.com/docs/en/settings]; it is treated as documentation-only metadata.)"

---

## Score Progression

| Iteration | Composite | Threshold | Verdict | Key Changes |
|-----------|-----------|-----------|---------|-------------|
| 1 (Baseline) | 0.823 | 0.95 (C4) | REVISE | Initial draft |
| 2 (After revision 1) | 0.893 | 0.95 (C4) | REVISE | Empirical verification added; 35-file inventory; 6-step migration; acceptance criteria; rollback procedure |
| **3 (After revision 2)** | **0.919** | **0.95 (C4)** | **REVISE** | **Scope selection paragraph; wildcard timeline pinned; risk rationale added; `~/.claude/settings.json` claim corrected; BUG-001 entity path added; repo-relative paths; `mcpServers` back-citation** |

**Total gain across 3 iterations:** +0.096 (+11.7%)
**Gain in revision cycle 2:** +0.026 (+2.9%)
**Remaining gap to C4 threshold:** 0.031
**Position vs H-13 standard (0.92):** 0.001 below (effectively at threshold; rounded 0.919)

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.90 | 0.93 | Update Reference 12 to cite specific README section in `upstash/context7`. Add one sentence to Empirical Verification acknowledging formula generalizability scope (confirmed for `context7`; inferred for other plugins). Estimated gain: +0.015 on EQ dimension = +0.002 composite. |
| 2 | Traceability | 0.90 | 0.94 | Add documentation/schema citation for `allowed_tools` "NOT a standard field" claim in Level 3. Estimated gain: +0.020 on Traceability = +0.002 composite. |
| 3 | Completeness + Actionability | 0.92 / 0.93 | 0.95 / 0.96 | Add `claude mcp list` observation command to migration step 6. This closes both the Completeness verification gap and the Actionability verification gap simultaneously. Estimated gain: +0.015 on Completeness, +0.015 on Actionability = +0.005 composite. |
| 4 | Actionability | 0.93 | 0.96 | Replace "Next agent hint: ps-architect" with a numbered formal Action Items list: (1) Create worktracker story for Context7 migration, (2) ps-architect decision task, (3) TOOL_REGISTRY.yaml update after decision. Estimated gain: +0.020 on Actionability = +0.003 composite. |
| 5 | Internal Consistency | 0.93 | 0.95 | Add one sentence distinguishing runtime-consumed fields from documentation-only fields in `.claude/settings.json` (resolves the `allowed_tools`/HIGH-credibility-source framing tension). Estimated gain: +0.015 on IC = +0.003 composite. |
| 6 | Methodological Rigor | 0.92 | 0.94 | Add a one-sentence named evaluation framework to the Trade-Off Analysis preamble. Estimated gain: +0.010 on MR = +0.002 composite. |

**Estimated composite after all P1-P6 fixes:** 0.919 + 0.002 + 0.002 + 0.005 + 0.003 + 0.003 + 0.002 = **~0.936**

**Gap analysis to 0.95:** The composite estimates above are conservative. Even with all six improvements applied, the document is projected to reach approximately 0.936, not 0.95. The gap between 0.936 and 0.95 reflects dimensions that are structurally near their ceiling given the inherent evidence constraints of this research:

- **Evidence Quality** is ceiling-limited by the plugin naming formula being derived from bug reports rather than an official specification. This is a real limitation of the research domain, not a document quality failure. Without an official specification from Anthropic, this dimension cannot exceed ~0.93.
- **Actionability** is ceiling-limited by the absence of a formal decision (the research deliberately defers to ps-architect). An "Action Items" list can raise the score but a research report cannot substitute for the architecture decision it is feeding.

**Realistic ceiling:** ~0.940-0.945 with a focused P1-P4 revision cycle, given the inherent evidence constraints. Reaching 0.95 would require either (a) official Anthropic documentation confirming the plugin naming formula, or (b) the report being repositioned from "research feeding a decision" to "research + decision" (which would require incorporating the ps-architect output and is out of scope for this artifact).

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing weighted composite
- [x] Evidence documented for each score with specific line-number references
- [x] Uncertain scores resolved downward: Evidence Quality scored 0.90 (not 0.92) because Context7 GitHub coarseness and formula-generalizability limitation are real gaps at C4 rigor; Traceability scored 0.90 (not 0.92) because the `allowed_tools` assertion remains uncited
- [x] Score movements calibrated against actual changes: IC +0.03 (scope paragraph is a real improvement); MR +0.04 (two targeted gaps fully closed); EQ +0.08 (primary contradiction eliminated); Traceability +0.08 (three of four gaps closed)
- [x] No dimension scored above 0.93 without strong justification
- [x] Actionability held at 0.93 (unchanged from iteration 2 because none of the targeted P5 gaps were in this revision's scope)
- [x] 0.919 composite is appropriately placed in the "strong work approaching threshold" band; it reflects a document that has resolved nearly all prior gaps while encountering the inherent evidence ceiling of this research domain
- [x] The realistic ceiling assessment (~0.940-0.945) is stated and its basis explained; this counteracts leniency toward claiming 0.95 is achievable with the existing evidence base

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.919
threshold: 0.950
standard_h13_threshold: 0.920
position_vs_h13: -0.001 (essentially at H-13 threshold; below by rounding margin)
weakest_dimension: Evidence Quality / Traceability (tied at 0.90)
weakest_score: 0.90
critical_findings_count: 0
iteration: 3
score_progression:
  - iteration: 1
    score: 0.823
    verdict: REVISE
  - iteration: 2
    score: 0.893
    verdict: REVISE
  - iteration: 3
    score: 0.919
    verdict: REVISE
improvement_recommendations:
  - "P1 Evidence Quality: Cite specific README section in upstash/context7 for Reference 12; add formula generalizability scope note to Empirical Verification"
  - "P2 Traceability: Cite documentation or schema source for allowed_tools NOT-a-standard-field claim in Level 3"
  - "P3 Completeness+Actionability: Add `claude mcp list` command to migration step 6 (closes both CLI verification gaps simultaneously)"
  - "P4 Actionability: Replace informal next-agent hint with numbered formal Action Items list"
  - "P5 Internal Consistency: Add one sentence distinguishing runtime-consumed vs documentation-only fields in .claude/settings.json"
  - "P6 Methodological Rigor: Name the evaluation framework in Trade-Off Analysis preamble"
estimated_composite_after_p1_p6: 0.936
realistic_ceiling_given_evidence_constraints: 0.940-0.945
above_h13_standard_threshold: false
note: "0.919 is 0.001 below H-13 standard threshold. P1+P2 targeted fixes alone would likely push above H-13. C4 threshold of 0.95 requires inherent evidence gaps to be resolved (official Anthropic plugin naming spec does not currently exist)."
```
