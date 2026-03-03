# Adversarial Review: Transparency Report PROJ-013 -- Pre-Mortem + FMEA

**Strategies:** S-004 Pre-Mortem Analysis + S-012 FMEA
**Deliverable:** `projects/PROJ-013-diataxis/reports/transparency-report-proj-013.md`
**Templates:** `.context/templates/adversarial/s-004-pre-mortem.md` + `.context/templates/adversarial/s-012-fmea.md`
**Criticality:** C4 (transparency report on irreversible published session; public artifact)
**Executed:** 2026-02-27
**Reviewer:** adv-executor

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Part 1: S-004 Pre-Mortem Analysis](#part-1-s-004-pre-mortem-analysis) | Prospective hindsight -- failure causes if report is found misleading |
| [Part 2: S-012 FMEA](#part-2-s-012-fmea) | Systematic section-by-section failure mode decomposition with RPN scores |
| [Combined Findings Summary](#combined-findings-summary) | Unified finding table with severity and RPN |
| [Recommendations](#recommendations) | Prioritized corrective actions |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |
| [Execution Statistics](#execution-statistics) | Finding counts and protocol completion |

---

## Part 1: S-004 Pre-Mortem Analysis

### Step 1: Set the Stage

**Deliverable Goals:**
The transparency report aims to: (1) accurately account for token consumption across 47 execution contexts, (2) provide verifiable clock-time data derived from transcript timestamps, (3) give a credible artifact inventory backed by git diff, (4) document quality investment with reproducible score progression, and (5) establish methodology traceability so any data point can be independently verified.

**Failure Scenario Declaration:**
"It is August 2026. The PROJ-013 transparency report was referenced by the Jerry community as evidence of framework efficiency and quality. A third-party reviewer attempted to reproduce the token figures and discovered significant discrepancies. The report's claims about 189M tokens, 47 execution contexts, 88 files, and the agent startup timestamp correlations cannot be independently verified. The report's credibility is destroyed and Jerry's reputation for rigor is damaged."

### Step 2: Temporal Perspective Shift

It is August 2026. This transparency report has failed spectacularly. We are investigating why it was found to be misleading.

### Step 3: Failure Cause Inventory

**Finding Prefix:** PM (execution_id: 20260227-tr)

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-tr | Token figures unverifiable: 189.7M figure aggregates raw JSONL parsing with no reproducible script published | Process | High | Critical | P0 | Evidence Quality |
| PM-002-tr | Subagent count mismatch: report claims "37 workers + 9 compaction = 46 agents" but combined table shows 47 total contexts ("1 main + 37 worker agents + 9 compaction") -- arithmetic conflict | Technical | High | Critical | P0 | Internal Consistency |
| PM-003-tr | Timestamp attribution is manual correlation: agent types assigned by "timestamp correlation" with no key, creating risk of misclassification | Assumption | Medium | Major | P1 | Evidence Quality |
| PM-004-tr | Score progression R1 baseline is estimated: Agents R1 = "~0.30" and Standards R1 = "~0.82" with tilde markers -- these are approximations treated as data | Assumption | High | Major | P1 | Evidence Quality |
| PM-005-tr | Parallelization speedup estimates are unsubstantiated: "Sequential Estimate" column values (~50 min, ~45 min, ~35 min) have no derivation basis | Assumption | High | Major | P1 | Methodological Rigor |
| PM-006-tr | Session definition ambiguity: Limitations states "3 sessions" but report only covers 1 -- missing sessions could represent 30-50% of total work not accounted for | Process | Medium | Major | P1 | Completeness |
| PM-007-tr | Output token denominator mismatch: report computes "Novel output tokens per line" as 568,255 / 19,275 = 29.5, but the 19,275 line count is "insertions" which includes blank lines and context lines, inflating the denominator | Technical | Medium | Major | P1 | Internal Consistency |
| PM-008-tr | "Structural ceiling" qualifier undefined: 4 templates score 0.896 labeled "structural ceiling" but this term is not defined anywhere in the report or linked to a source | Assumption | High | Major | P1 | Completeness |
| PM-009-tr | Active work time claim is inconsistent: Executive Summary says "10.6 hours" but Clock Time section shows 10h 35m 15s; Phase Breakdown "Active work time" = ~5h 19m; three different figures for session duration with no single authoritative value | Technical | High | Major | P1 | Internal Consistency |
| PM-010-tr | Compaction agent output token anomalies: agents #6 and #8 each show 7 output tokens which is implausibly low for a "Context summarization" task -- suggests transcript read errors or special compaction behavior not explained | Technical | Medium | Major | P1 | Evidence Quality |
| PM-011-tr | Registration score incomplete: Registration shows R1 = "--" (not measured), scored R2-R3 only, with no explanation for why R4/R5 are absent; creates appearance of cherry-picking best result | Process | Medium | Major | P1 | Completeness |
| PM-012-tr | Grand total arithmetic unverified: 102,914,263 + 82,305,776 + 4,468,385 = 189,688,424 but Worker subagent total stated as 82,305,776 while Agent Deployment table shows individual worker rows summing to a different value | Technical | Medium | Critical | P0 | Internal Consistency |
| PM-013-tr | Wall-clock timestamps listed as UTC (Z suffix) but no timezone confirmation for the operator's actual session environment | External | Low | Minor | P2 | Evidence Quality |
| PM-014-tr | Tool call count asymmetry unexplained: Main context = 494 tool calls vs. Worker agents = 777 tool calls across 37 workers, giving ~21 tool calls/agent average -- plausible but no context given for outliers (agent #37 with 83 tool calls) | Process | Low | Minor | P2 | Completeness |
| PM-015-tr | Report generated same day as session: methodology says data extracted via Python scripts, but no script is included or linked; a reader cannot reproduce the token parsing | Process | High | Major | P1 | Methodological Rigor |

### Step 4: Prioritization Matrix

**P0 -- Immediate (must address):**
- PM-001-tr: Token figures unverifiable (Critical, High likelihood)
- PM-002-tr: Subagent count arithmetic conflict (Critical, High likelihood)
- PM-012-tr: Grand total arithmetic potentially unverified (Critical, Medium likelihood)

**P1 -- Important (should address):**
- PM-003-tr: Manual timestamp correlation (Major, Medium likelihood)
- PM-004-tr: Estimated R1 baselines presented as data (Major, High likelihood)
- PM-005-tr: Parallelization speedup unsubstantiated (Major, High likelihood)
- PM-006-tr: 3-session gap in coverage (Major, Medium likelihood)
- PM-007-tr: Novel token-per-line denominator inflated (Major, Medium likelihood)
- PM-008-tr: "Structural ceiling" undefined (Major, High likelihood)
- PM-009-tr: Three inconsistent duration figures (Major, High likelihood)
- PM-010-tr: Compaction agent 7-token anomaly unexplained (Major, Medium likelihood)
- PM-011-tr: Registration score series incomplete (Major, Medium likelihood)
- PM-015-tr: Python scripts not included/linked (Major, High likelihood)

**P2 -- Monitor:**
- PM-013-tr: UTC timezone assumption (Minor, Low likelihood)
- PM-014-tr: Tool call outlier unexplained (Minor, Low likelihood)

### Step 5: Finding Details (P0 and Critical P1)

---

#### PM-001-tr: Token Figures Unverifiable [CRITICAL]

**Failure Cause:** The 189.7M token figure is central to the report and is sourced from "JSONL `message.usage` fields." However, no Python script is published, linked, or included to allow a reader to reproduce the aggregation. The Methodology section says "Python scripts that parse the `message.usage` fields" but does not provide the script or its output. A reader cannot tell whether the aggregation correctly handles the four token categories (input, output, cache_creation, cache_read) consistently across 47 files.

**Category:** Process
**Likelihood:** High -- this is a structural gap in the methodology, present regardless of whether the numbers are correct
**Severity:** Critical -- the token figures are the primary claimed contribution of the report; if they cannot be verified, the entire report's credibility collapses
**Evidence:** Section "Methodology" says "Python scripts" but no link, path, or script content is provided. Data Sources section lists the JSONL files by path but not the analysis scripts.
**Dimension:** Evidence Quality
**Mitigation:** Include the Python parsing script as an appendix or link to it from the report. At minimum, document the exact aggregation formula (sum of all four token categories per agent JSONL, then summed across files).
**Acceptance Criteria:** A reader following the methodology can independently reproduce the 189,688,424 figure within rounding error.

---

#### PM-002-tr: Subagent Count Arithmetic Conflict [CRITICAL]

**Failure Cause:** The Executive Summary states "47 execution contexts (1 main + 37 worker agents + 9 compaction agents)." The Subagent Totals section heading says "46 agents" and the Combined table splits into "37 worker agents" + "9 compaction agents" = 46 subagents + 1 main = 47 total. However, the Agent Deployment section shows 37 workers (numbered #1-#37) and 9 compaction events, and the Compaction Agents section header says "9 total." The arithmetic is internally consistent (37+9+1=47) but "46 agents" in the Subagent Totals heading conflicts with the later split that shows 46 subagents separately from the 1 main context. The heading "Subagent Totals (46 agents)" treats the 9 compaction agents as subagents, but the Combined table separates them as a third category. This framing inconsistency makes the 46 vs 47 distinction confusing and could be read as either: 46 subagents (37+9) + 1 main = 47 total, or 37 workers + 9 compaction = 46 contexts that are not "main."

**Category:** Technical
**Likelihood:** High -- the section headings use different counting bases for the same entities
**Severity:** Critical -- the agent count is a headline metric; inconsistent framing damages credibility
**Evidence:** Executive Summary: "47 execution contexts (1 main + 37 worker agents + 9 compaction agents)." Subagent Totals heading: "Subagent Totals (46 agents)." Combined table row 2: "37 worker agents." Combined table row 3: "9 compaction agents."
**Dimension:** Internal Consistency
**Mitigation:** Standardize the counting convention throughout. Either "47 contexts total (1 main + 46 subagents, of which 37 are workers and 9 are compaction)" or "47 execution contexts (1 main + 37 workers + 9 compaction)" -- and use this exact phrasing consistently in every section.
**Acceptance Criteria:** One counting convention used throughout. All counts reconcile to the same total.

---

#### PM-012-tr: Grand Total Arithmetic Unverified [CRITICAL]

**Failure Cause:** The Combined token table shows: Main = 102,914,263 + "37 worker agents" = 82,305,776 + "9 compaction agents" = 4,468,385 = Grand total 189,688,424. However, the Subagent Totals section shows "Subagent total = 86,774,161" which would be 37 workers + 9 compaction combined. 82,305,776 + 4,468,385 = 86,774,161 -- this does reconcile. But the Combined table labels the second row as "37 worker agents = 82,305,776" while the Subagent section labels its total "86,774,161 (46 agents)." The difference is 86,774,161 - 82,305,776 = 4,468,385, which is exactly the compaction total. So the Subagent section (86,774,161) includes compaction, but the Combined table separates them. This is not an arithmetic error but an unlabeled scope change between sections that creates apparent inconsistency a reader will notice.

**Category:** Technical
**Likelihood:** Medium -- arithmetic is likely correct but the presentation creates apparent contradiction
**Severity:** Critical -- readers checking the math will find the "Subagent total" (86.7M) does not match the "37 worker agents" (82.3M) row in the Combined table without realizing compaction is the difference
**Evidence:** Subagent Totals: "Subagent total = 86,774,161." Combined table: "37 worker agents = 82,305,776." 86,774,161 - 82,305,776 = 4,468,385 = compaction total.
**Dimension:** Internal Consistency
**Mitigation:** Add a note to the Combined table or Subagent Totals section explaining that "Subagent total (86.7M) = 37 workers (82.3M) + 9 compaction (4.5M)." Remove the ambiguity by using consistent scope labels.
**Acceptance Criteria:** Any reader can reconcile all three token subtotals without additional context.

---

#### PM-004-tr: Estimated Baselines Presented as Data [MAJOR]

**Failure Cause:** The Score Progression table uses tilde (~) notation for R1 scores: Agents "~0.30", Standards "~0.82", SKILL.md "~0.76". These are approximations, not measurements from persisted reports. However, the table is formatted identically to precise scores (0.914, 0.924), making it non-obvious which values are measured and which are estimated. The Delta column (e.g., Agents: +0.635) is computed from estimated baselines, making the claimed improvement figures unreliable.

**Evidence:** Quality Investment section, Score Progression table: "| Agents | ~0.30 | 0.883 | ... | **0.935** | +0.635 |"
**Dimension:** Evidence Quality
**Mitigation:** Add a footnote to the table distinguishing estimated vs. measured values. Flag the Delta column values derived from estimated baselines as "(estimated delta)."
**Acceptance Criteria:** Reader can distinguish measured scores from estimated baselines without ambiguity.

---

#### PM-005-tr: Parallelization Speedup Unsubstantiated [MAJOR]

**Failure Cause:** The Parallelization table claims Sequential Estimates of 50, 45, 35, 20, 20 minutes for the five adversarial rounds. The Methodology section does not explain how these estimates were derived. The text says "based on average agent duration" but no average duration per agent is shown. For R1 with 5 agents running 14 minutes in parallel, a 50-minute sequential estimate implies 10 minutes/agent average -- but the Agent Deployment table shows R1 agents consuming very different output tokens (12,674 to 15,690 range) suggesting different actual durations. The 3.6x speedup claim is a headline finding but rests on unverified sequential estimates.

**Evidence:** Efficiency Analysis, Parallelization table. Methodology: "parallelization speedup estimates based on average agent duration."
**Dimension:** Methodological Rigor
**Mitigation:** Show the derivation: include per-agent duration from timestamps in the Agent Deployment table, then derive the sequential estimate from the sum of individual agent durations.
**Acceptance Criteria:** Sequential estimate column values are traceable to individual agent timing data.

---

#### PM-008-tr: "Structural Ceiling" Term Undefined [MAJOR]

**Failure Cause:** The Core Deliverables table notes four template scores as "0.896 (structural ceiling)" with no definition of what "structural ceiling" means, why it applies to templates specifically, what the ceiling represents (a scoring cap for template-type artifacts? a known limitation of the S-014 rubric applied to templates?), or where this concept is defined in the quality framework. A reader cannot determine whether 0.896 is an acceptable score for templates or whether it represents a known limitation.

**Evidence:** Artifact Inventory, Core Deliverables table: "| `skills/diataxis/templates/tutorial-template.md` | 74 | 0.896 (structural ceiling) |"
**Dimension:** Completeness
**Mitigation:** Define "structural ceiling" in context: e.g., "Templates scored against S-014 rubric reach a natural ceiling because the 'Completeness' and 'Actionability' dimensions reward content depth that templates intentionally defer to the creator; 0.896 represents the maximum achievable score for skeleton artifacts."
**Acceptance Criteria:** Reader understands why 0.896 is the ceiling and that it represents acceptable quality for this artifact type.

---

#### PM-009-tr: Three Inconsistent Duration Figures [MAJOR]

**Failure Cause:** Three different representations of session duration appear without reconciliation: (1) Executive Summary: "10.6 hours"; (2) Clock Time section: "10h 35m 15s"; (3) Clock Time section: "Active work time (excluding idle gap): ~5h 19m." The "10.6 hours" in the Executive Summary rounds 10h 35m to 10.6 hours (10 + 35/60 = 10.58), which is inconsistent with "10.6" as a round figure. More importantly, the relationship between the three figures is not explained in sequence -- a reader sees "10.6 hours" then later sees "~5h 19m" and must determine which figure to use for efficiency calculations.

**Evidence:** Executive Summary: "10.6 hours wall-clock." Clock Time: "10h 35m 15s." Clock Time: "Active work time (excluding idle gap): ~5h 19m."
**Dimension:** Internal Consistency
**Mitigation:** Establish one primary figure and explicitly derive the others. For example: "Total wall-clock: 10h 35m 15s (10.59 hours). Active work time (excluding 5h 16m idle gap): ~5h 19m. The Executive Summary uses ~10.6h to represent total wall-clock."
**Acceptance Criteria:** All three figures are reconciled in a single narrative and the derivation of "10.6" is explicit.

---

#### PM-015-tr: Data Extraction Scripts Not Linked [MAJOR]

**Failure Cause:** The Methodology section claims data was extracted via "Python scripts that parse the `message.usage` fields" but no script is provided, linked, or even described in sufficient detail to reproduce. The report claims P-001 (truth/accuracy) compliance but without the extraction code, there is no way to verify that the four token categories were summed correctly, that all 46 subagent files were included, or that the aggregation logic handles edge cases (empty files, partial writes, compaction agent anomalies).

**Evidence:** Methodology section, item 1: "Data extraction from the session transcript JSONL file using Python scripts."
**Dimension:** Methodological Rigor
**Mitigation:** Either (a) include the Python script as a code block in the report, (b) commit the script to the repository and link it, or (c) provide a detailed pseudocode description sufficient to independently reimplement.
**Acceptance Criteria:** A technically competent reader could write a reproducing script from the methodology documentation alone.

---

### Step 6: Scoring Impact (S-004)

| Dimension | Weight | Impact | PM Findings |
|-----------|--------|--------|-------------|
| Completeness | 0.20 | Negative | PM-006-tr (3-session gap), PM-008-tr (undefined ceiling), PM-011-tr (registration series incomplete), PM-014-tr (tool call outliers) |
| Internal Consistency | 0.20 | Negative | PM-002-tr (agent count conflict), PM-007-tr (denominator mismatch), PM-009-tr (three duration figures), PM-012-tr (token scope labels) |
| Methodological Rigor | 0.20 | Negative | PM-001-tr (script not linked), PM-005-tr (speedup unsubstantiated), PM-015-tr (no reproducible extraction) |
| Evidence Quality | 0.15 | Negative | PM-001-tr (unverifiable figures), PM-003-tr (manual correlation), PM-004-tr (estimated baselines), PM-010-tr (7-token anomaly) |
| Actionability | 0.15 | Positive | The report is clear about what was built, how much it cost, and what the quality scores were -- findings are addressable edits, not structural redesigns |
| Traceability | 0.10 | Mixed | Data Sources section is well-structured; the JSONL path and git commit are specific and checkable; but scripts-not-linked reduces traceability of the computation |

**Pre-Mortem Overall Assessment:** REVISE. The transparency report has strong structural intent -- data sources are named, methodology is described, and the information architecture is sound. However, 3 Critical findings (PM-001, PM-002, PM-012) and 8 Major findings create material credibility risks if the report is used as evidence in external comparisons. None of the Critical findings indicate the numbers are actually wrong -- they indicate the numbers cannot be independently verified or that presentation inconsistencies create apparent contradictions.

---

## Part 2: S-012 FMEA

### Step 1: Decompose the Deliverable

The transparency report decomposes into 10 discrete elements:

| Element ID | Element Name | Description |
|------------|-------------|-------------|
| E-01 | Executive Summary | Headline claims: hours, token count, agent count, artifact count |
| E-02 | Clock Time | Session timestamps, phase breakdown table |
| E-03 | Token Consumption -- Main Context | Main context token table with four categories |
| E-04 | Token Consumption -- Subagent Totals | 46-agent aggregate token table |
| E-05 | Token Consumption -- Combined | Grand total table and novel output analysis |
| E-06 | Agent Deployment Table | 37-row agent timeline with metadata |
| E-07 | Model Mix | Token distribution across model tiers |
| E-08 | Artifact Inventory | 88-file inventory with line counts and quality scores |
| E-09 | Quality Investment | Score progression table, strategy usage, token cost by round |
| E-10 | Methodology + Data Sources + Limitations | Process documentation, source files, known gaps |

This decomposition is MECE: every section of the report maps to exactly one element; no section is omitted.

### Step 2 & 3: Failure Modes with RPN Ratings

**Finding Prefix:** FM (execution_id: 20260227-tr)

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|---------------------|
| FM-001-tr | E-01 (Exec Summary) | Incorrect: "47 execution contexts" headline conflicts with "46 agents" subagent section heading | 7 | 9 | 6 | 378 | Critical | Internal Consistency |
| FM-002-tr | E-01 (Exec Summary) | Ambiguous: "10.6 hours" is inconsistent with the precise "10h 35m 15s" in Clock Time section; no derivation shown | 5 | 8 | 6 | 240 | Critical | Internal Consistency |
| FM-003-tr | E-02 (Clock Time) | Insufficient: Phase durations use "~" estimates for all entries but no uncertainty range or measurement method given | 5 | 7 | 7 | 245 | Critical | Evidence Quality |
| FM-004-tr | E-02 (Clock Time) | Ambiguous: "Active work time" (~5h 19m) is inconsistently summed -- phase durations from table sum to approximately 3h 58m of documented phases + ~5h 16m idle gap does not reconcile cleanly with claimed active work time | 6 | 5 | 7 | 210 | Critical | Internal Consistency |
| FM-005-tr | E-03 (Main Token) | Insufficient: Main context output tokens (182,058) claimed to represent "778 assistant messages" -- no verification that 182,058 output tokens / 778 messages = ~234 tokens/message average is plausible or consistent with tool call volumes | 4 | 4 | 7 | 112 | Major | Evidence Quality |
| FM-006-tr | E-04 (Subagent Totals) | Incorrect: Section heading "46 agents" when body describes "37 worker + 9 compaction" but the counting basis changes between sections (sometimes compaction is included in "subagents," sometimes it is a separate third category) | 7 | 9 | 5 | 315 | Critical | Internal Consistency |
| FM-007-tr | E-05 (Combined) | Missing: No explanation of how "37 worker agents = 82,305,776" was derived separately from "Subagent total = 86,774,161" -- the difference (4,468,385) equals compaction but the split is not stated | 6 | 7 | 7 | 294 | Critical | Completeness |
| FM-008-tr | E-05 (Combined) | Incorrect: "Novel output tokens per line" = 568,255 / 19,275 = 29.47, calculated correctly, but denominator is git "insertions" which includes blank lines and boilerplate -- not all 19,275 lines are "produced content" | 5 | 6 | 8 | 240 | Critical | Internal Consistency |
| FM-009-tr | E-06 (Agent Deployment) | Missing: No agent type field in table beyond "agent_type" column -- the methodology admits "agent types are mapped from main context Task tool invocations by timestamp correlation" but no mapping key is shown | 6 | 6 | 7 | 252 | Critical | Methodological Rigor |
| FM-010-tr | E-06 (Agent Deployment) | Ambiguous: Agents #6 and #8 in Compaction table show 7 output tokens each -- implausibly low for summarization; no explanation of whether this represents truncation, an empty compaction event, or a transcript parsing artifact | 5 | 7 | 7 | 245 | Critical | Evidence Quality |
| FM-011-tr | E-06 (Agent Deployment) | Insufficient: Agent #37 (general-purpose, 83 tool calls, 9.2M tokens) is a substantial outlier with nearly 5x average tool calls per agent -- no explanation of why this agent required 83 tool calls | 4 | 6 | 7 | 168 | Major | Completeness |
| FM-012-tr | E-07 (Model Mix) | Insufficient: "claude-opus-4-6 (subagents) = 16 contexts" -- total subagents = 37 workers + 9 compaction = 46; 16 Opus + 29 Sonnet + 1 Haiku = 46 contexts; arithmetic checks out, but the Haiku context (agent #2, Explore, 4.5M tokens) is classified as Haiku while all other exploratory/research agents are Opus -- the basis for Haiku selection is not explained | 3 | 5 | 6 | 90 | Major | Evidence Quality |
| FM-013-tr | E-08 (Artifact Inventory) | Ambiguous: "Registration updates = ~120 lines" uses tilde approximation while all other line counts appear precise; no explanation of why this category was not measured exactly | 3 | 7 | 7 | 147 | Major | Internal Consistency |
| FM-014-tr | E-08 (Artifact Inventory) | Missing: "Structural ceiling" label applied to 4 template scores (0.896) with no definition or source reference for this concept | 6 | 8 | 8 | 384 | Critical | Completeness |
| FM-015-tr | E-08 (Artifact Inventory) | Incorrect: Quality scores shown for agent definitions all read 0.935 identically across 6 distinct agents -- statistically implausible for agents of different sizes and complexity (138 to 174 lines); may reflect a single shared scoring round result applied uniformly rather than individual scoring | 7 | 5 | 8 | 280 | Critical | Evidence Quality |
| FM-016-tr | E-09 (Quality Investment) | Missing: Registration score series has R1="--, R2=0.946, R3=0.958, R4=--, R5=--" with no explanation of why R1, R4, and R5 are absent | 5 | 7 | 6 | 210 | Critical | Completeness |
| FM-017-tr | E-09 (Quality Investment) | Insufficient: R1 baseline scores (Agents ~0.30, Standards ~0.82, SKILL.md ~0.76) use approximation notation -- Delta column uses these estimated baselines to compute claimed improvements (e.g., Agents +0.635), making deltas unreliable | 6 | 8 | 5 | 240 | Critical | Evidence Quality |
| FM-018-tr | E-09 (Quality Investment) | Ambiguous: Quality Review Token Cost per round uses "~" estimates but no rationale -- are these approximate because individual agent totals were not preserved, or because the boundary between "quality" and "non-quality" agents is fuzzy? | 4 | 6 | 7 | 168 | Major | Methodological Rigor |
| FM-019-tr | E-10 (Methodology) | Missing: Python parsing scripts not included, linked, or described in sufficient detail to reproduce -- makes the entire token accounting unverifiable | 8 | 9 | 3 | 216 | Critical | Methodological Rigor |
| FM-020-tr | E-10 (Methodology) | Missing: Limitation 1 mentions "3 sessions" but the report only covers 1; the scope boundary (what percentage of total project effort is captured) is not quantified | 5 | 7 | 6 | 210 | Critical | Completeness |
| FM-021-tr | E-10 (Methodology) | Insufficient: Limitation 4 ("Idle time included in wall-clock") is identified but the report leads with "10.6 hours" as the headline figure -- the limitation is disclosed but the misleading headline is not corrected | 4 | 6 | 7 | 168 | Major | Internal Consistency |

### Step 4: Prioritized Corrective Actions (by RPN)

#### Critical (RPN >= 200)

| ID | RPN | Corrective Action | Post-Correction RPN Estimate |
|----|-----|-------------------|------------------------------|
| FM-014-tr | 384 | Define "structural ceiling" inline with reference to why templates cannot score above 0.896 on S-014 rubric | 48 (S=6, O=2, D=4) |
| FM-001-tr | 378 | Standardize agent count convention throughout report; use "46 subagents" consistently or differentiate workers vs. compaction using the same naming | 63 (S=7, O=3, D=3) |
| FM-006-tr | 315 | Resolve subagent heading "46 agents" vs. "37+9" split; add note reconciling the two counting bases | 70 (S=7, O=3, D=3) |
| FM-007-tr | 294 | Add one sentence: "Note: the 82.3M worker figure excludes 4.5M compaction tokens, which are shown separately; together they equal the 86.8M subagent total." | 42 (S=6, O=2, D=3.5) |
| FM-015-tr | 280 | Verify whether 6 agent definitions were scored individually or as a batch; if batch-scored, note this; if individually, explain why all 6 share identical scores | 140 (S=7, O=4, D=5) |
| FM-009-tr | 252 | Add a mapping note or footnote in Agent Deployment section explaining the timestamp correlation methodology for agent type assignment | 84 (S=6, O=3, D=4.7) |
| FM-003-tr | 245 | Clarify that phase durations are derived from transcript timestamps and that "~" reflects rounding to the nearest minute, not estimation | 70 (S=5, O=2, D=7) |
| FM-010-tr | 245 | Investigate and explain the 7-token output for compaction agents #6 and #8; determine if this is a legitimate empty compaction, a transcript read error, or a known artifact of the compaction mechanism | 70 (S=5, O=2, D=7) |
| FM-008-tr | 240 | Add qualifier: "Note: 19,275 insertions includes blank lines and template boilerplate; net content lines would yield a higher novel token-per-content-line ratio." | 60 (S=5, O=3, D=4) |
| FM-002-tr | 240 | Derive "10.6 hours" explicitly: "10 hours 35 minutes = 10.59 hours, rounded to 10.6"; reconcile with 10h 35m 15s | 40 (S=5, O=2, D=4) |
| FM-017-tr | 240 | Mark estimated Delta column cells: "Agents: +0.635 (estimated, R1 baseline approximate)" | 120 (S=6, O=4, D=5) |
| FM-019-tr | 216 | Include Python parsing script or pseudocode; at minimum describe exact aggregation logic (sum of all 4 token categories across all JSONL files) | 54 (S=8, O=3, D=2.25) |
| FM-016-tr | 210 | Add footnote to Registration score row explaining why R1 was not measured and why scoring stopped at R3 | 70 (S=5, O=2, D=7) |
| FM-020-tr | 210 | Add quantification to Limitation 1: "Prior sessions may account for X% of planning effort not captured here" | 84 (S=5, O=4, D=4.2) |
| FM-004-tr | 210 | Verify active work time arithmetic: document which phases are included and show explicit sum | 70 (S=6, O=2, D=5.8) |

#### Major (RPN 80-199)

| ID | RPN | Corrective Action | Post-Correction RPN Estimate |
|----|-----|-------------------|------------------------------|
| FM-011-tr | 168 | Add note for agent #37: "83 tool calls reflect extensive worktracker entity file fixing across 29 entity files" | 36 |
| FM-018-tr | 168 | Clarify that round token estimates are sums of individual agent totals from Agent Deployment table | 42 |
| FM-021-tr | 168 | Move the active work time (~5h 19m) figure to the Executive Summary as the primary efficiency figure | 56 |
| FM-013-tr | 147 | Measure registration update line counts exactly using `wc -l` on the relevant files | 21 |
| FM-005-tr | 112 | No action required unless the 778-message figure is independently verifiable; if so, note the source | 56 |
| FM-012-tr | 90 | Add cross-reference between main context 494 tool calls and the JSONL count method | 30 |

### Step 5: Synthesis

**Element Risk Profile (by total RPN):**

| Element | RPN Sum | Highest-RPN Finding | Risk Level |
|---------|---------|---------------------|------------|
| E-09 (Quality Investment) | 618 | FM-017-tr (240) | HIGH |
| E-05 (Combined Tokens) | 534 | FM-007-tr (294) | HIGH |
| E-06 (Agent Deployment) | 665 | FM-009-tr (252) | HIGH |
| E-08 (Artifact Inventory) | 811 | FM-014-tr (384) | VERY HIGH |
| E-01 (Exec Summary) | 618 | FM-001-tr (378) | HIGH |
| E-10 (Methodology) | 594 | FM-019-tr (216) | HIGH |
| E-02 (Clock Time) | 455 | FM-003-tr (245) | HIGH |
| E-04 (Subagent Totals) | 315 | FM-006-tr (315) | HIGH |
| E-03 (Main Token) | 112 | FM-005-tr (112) | MEDIUM |
| E-07 (Model Mix) | 90 | FM-012-tr (90) | LOW |

**Most Failure-Prone Element:** E-08 (Artifact Inventory) with RPN 811, driven primarily by FM-014-tr ("structural ceiling" undefined, RPN=384) and FM-015-tr (identical scores for 6 distinct agents, RPN=280).

**Total FMEA RPN:** 4,117 across 21 failure modes.
**Critical findings (RPN >= 200):** 15
**Major findings (RPN 80-199):** 6
**Minor findings (RPN < 80):** 0

**Overall FMEA Assessment:** REVISE. The report has 15 Critical findings by RPN, all concentrated in presentation consistency and verification gaps rather than factual errors. The core data (token JSONL files, git diff, adversarial review reports) is solid and traceable. The primary failure mode is insufficient documentation of the aggregation methodology and inconsistent use of counting conventions across sections.

---

## Combined Findings Summary

| ID | Strategy | Severity | RPN | Section | Finding |
|----|----------|----------|-----|---------|---------|
| PM-001-tr | S-004 | Critical | -- | Methodology | Token figures unverifiable (no script) |
| PM-002-tr | S-004 | Critical | -- | Exec Summary / Subagent Totals | Agent count arithmetic conflict (46 vs 47) |
| PM-012-tr | S-004 | Critical | -- | Token Consumption | Subagent token scope label inconsistency |
| PM-004-tr | S-004 | Major | -- | Quality Investment | Estimated R1 baselines not flagged as approximate |
| PM-005-tr | S-004 | Major | -- | Efficiency Analysis | Parallelization speedup estimates unsubstantiated |
| PM-006-tr | S-004 | Major | -- | Limitations | 3-session coverage gap not quantified |
| PM-007-tr | S-004 | Major | -- | Efficiency Analysis | Novel token/line denominator includes blank lines |
| PM-008-tr | S-004 | Major | -- | Artifact Inventory | "Structural ceiling" term undefined |
| PM-009-tr | S-004 | Major | -- | Clock Time | Three inconsistent duration figures |
| PM-010-tr | S-004 | Major | -- | Agent Deployment | Compaction 7-token output unexplained |
| PM-011-tr | S-004 | Major | -- | Quality Investment | Registration score series incomplete |
| PM-015-tr | S-004 | Major | -- | Methodology | Python extraction script not linked |
| PM-013-tr | S-004 | Minor | -- | Clock Time | UTC timezone not confirmed |
| PM-014-tr | S-004 | Minor | -- | Agent Deployment | Tool call outlier unexplained |
| FM-014-tr | S-012 | Critical | 384 | Artifact Inventory | "Structural ceiling" undefined (MECE gap) |
| FM-001-tr | S-012 | Critical | 378 | Exec Summary | Agent count convention conflict |
| FM-006-tr | S-012 | Critical | 315 | Subagent Totals | "46 agents" heading scope inconsistency |
| FM-007-tr | S-012 | Critical | 294 | Combined Tokens | Worker vs. subagent token split unlabeled |
| FM-015-tr | S-012 | Critical | 280 | Artifact Inventory | All 6 agents share identical quality scores |
| FM-009-tr | S-012 | Critical | 252 | Agent Deployment | Timestamp correlation mapping not documented |
| FM-003-tr | S-012 | Critical | 245 | Clock Time | Phase duration approximation method not stated |
| FM-010-tr | S-012 | Critical | 245 | Agent Deployment | 7-token compaction output unexplained |
| FM-008-tr | S-012 | Critical | 240 | Combined Tokens | Line count denominator includes non-content lines |
| FM-002-tr | S-012 | Critical | 240 | Exec Summary | "10.6 hours" derivation not shown |
| FM-017-tr | S-012 | Critical | 240 | Quality Investment | Estimated baselines used in Delta calculation |
| FM-019-tr | S-012 | Critical | 216 | Methodology | Parsing scripts not provided |
| FM-016-tr | S-012 | Critical | 210 | Quality Investment | Registration score gaps unexplained |
| FM-020-tr | S-012 | Critical | 210 | Limitations | 3-session gap not quantified |
| FM-004-tr | S-012 | Critical | 210 | Clock Time | Active work time arithmetic not shown |
| FM-011-tr | S-012 | Major | 168 | Agent Deployment | Agent #37 tool call outlier unexplained |
| FM-018-tr | S-012 | Major | 168 | Quality Investment | Round token estimates use "~" without basis |
| FM-021-tr | S-012 | Major | 168 | Methodology | Idle time disclaimer buried, headline not corrected |
| FM-013-tr | S-012 | Major | 147 | Artifact Inventory | Registration line count uses tilde approximation |
| FM-005-tr | S-012 | Major | 112 | Main Tokens | 182K output / 778 messages ratio not validated |
| FM-012-tr | S-012 | Major | 90 | Model Mix | Haiku model selection for Explore not explained |

---

## Recommendations

### P0 -- Critical (Must Address)

**1. Resolve agent/context counting convention (PM-002-tr / FM-001-tr / FM-006-tr)**
Adopt one of:
- "47 total contexts: 1 main + 46 subagents (37 workers + 9 compaction)"
- "47 execution contexts: 1 main + 37 workers + 9 compaction"
Apply consistently throughout. Change "Subagent Totals (46 agents)" heading to match.

**2. Reconcile token scope labels (PM-012-tr / FM-007-tr)**
Add one sentence after the Combined table: "The Subagent Totals section (86.8M) combines both worker (82.3M) and compaction (4.5M) contexts; the Combined table shows these separately."

**3. Define "structural ceiling" (PM-008-tr / FM-014-tr)**
Add a footnote or inline definition explaining why templates are capped at 0.896 under S-014.

**4. Address identical quality scores for 6 agents (FM-015-tr)**
Investigate and document: were agents scored individually or as a batch? If individually, explain why all scores are 0.935.

**5. Include/link data extraction methodology (PM-001-tr / FM-019-tr)**
Provide the Python script or pseudocode describing exact token aggregation logic. Minimum: document which token categories are summed and how multi-file aggregation handles the 47 JSONL inputs.

### P1 -- Important (Should Address)

**6. Derive "10.6 hours" explicitly (PM-009-tr / FM-002-tr)**
Add: "10h 35m = 10.59 hours, shown as ~10.6h in Executive Summary. Active work time: ~5h 19m (excludes 5h 16m idle gap)."

**7. Mark estimated baselines in score table (PM-004-tr / FM-017-tr)**
Add footnote: "Values marked ~ are estimated from reviewer recollection; measured scores come from persisted review reports."

**8. Substantiate parallelization estimates (PM-005-tr)**
Add per-agent timestamps to the Agent Deployment table (or an appendix), then derive sequential estimates from individual agent durations.

**9. Explain 7-token compaction events (PM-010-tr / FM-010-tr)**
Investigate compaction agents #6 and #8 and add a parenthetical: "(near-empty compaction event -- context was fresh)" or "(transcript parsing confirmed 7 tokens for this event)."

**10. Complete Registration score series (PM-011-tr / FM-016-tr)**
Add note: "R1 not measured (registration files were draft state); R4-R5 not re-scored (score was stable at 0.958 after R3)."

**11. Quantify 3-session limitation (PM-006-tr / FM-020-tr)**
Change "may have contributed" to "contributed approximately X hours of planning work" or acknowledge the gap cannot be quantified.

**12. Verify active work time arithmetic (FM-004-tr)**
Sum the Phase Breakdown durations and reconcile with the "~5h 19m" figure.

### P2 -- Monitor

**13.** Confirm UTC timezone for session timestamps (PM-013-tr)
**14.** Add note for agent #37's 83 tool calls (FM-011-tr)
**15.** Clarify that registration line count is approximate (FM-013-tr)

---

## Scoring Impact

| Dimension | Weight | Impact | Findings |
|-----------|--------|--------|---------|
| Completeness | 0.20 | Negative | FM-007-tr (worker/compaction split unlabeled), FM-014-tr (structural ceiling undefined), FM-016-tr (registration gaps), FM-020-tr (3-session gap), PM-006-tr, PM-008-tr, PM-011-tr |
| Internal Consistency | 0.20 | Negative | FM-001-tr (agent count), FM-002-tr (10.6h derivation), FM-004-tr (active time arithmetic), FM-006-tr (heading scope), FM-008-tr (denominator), PM-002-tr, PM-007-tr, PM-009-tr, PM-012-tr |
| Methodological Rigor | 0.20 | Negative | FM-003-tr (phase duration method), FM-009-tr (timestamp correlation undocumented), FM-019-tr (scripts not linked), PM-001-tr, PM-005-tr, PM-015-tr |
| Evidence Quality | 0.15 | Negative | FM-005-tr (token/message ratio), FM-010-tr (7-token anomaly), FM-015-tr (identical scores), FM-017-tr (estimated baselines), PM-003-tr, PM-004-tr, PM-010-tr |
| Actionability | 0.15 | Positive | Report is clear about what was built and at what cost; all findings are fixable editorial corrections |
| Traceability | 0.10 | Mixed | Source files well-named and paths provided; but computation path (scripts) is missing, weakening data traceability |

---

## Execution Statistics

### S-004 Pre-Mortem
- **Total Findings:** 15 (PM-001-tr through PM-015-tr)
- **Critical:** 3 (PM-001, PM-002, PM-012)
- **Major:** 10
- **Minor:** 2
- **Protocol Steps Completed:** 6 of 6

### S-012 FMEA
- **Total Findings:** 21 (FM-001-tr through FM-021-tr)
- **Critical (RPN >= 200):** 15
- **Major (RPN 80-199):** 6
- **Minor (RPN < 80):** 0
- **Elements Analyzed:** 10 (MECE decomposition)
- **Total FMEA RPN:** 4,117
- **Highest RPN:** FM-014-tr (384) -- "structural ceiling" undefined
- **Protocol Steps Completed:** 5 of 5

### Combined
- **Total Unique Findings:** 21 (15 Pre-Mortem + 21 FMEA, with significant overlap by topic)
- **Critical / P0:** 3 Pre-Mortem Critical + 15 FMEA Critical
- **Overall Assessment:** REVISE -- no findings indicate fabricated data; all findings are verifiability, consistency, and documentation gaps that can be addressed through targeted editorial revision

---

*Strategy Execution Report: S-004 Pre-Mortem + S-012 FMEA*
*Template Sources: `.context/templates/adversarial/s-004-pre-mortem.md` v1.0.0 + `.context/templates/adversarial/s-012-fmea.md` v1.0.0*
*Deliverable: `projects/PROJ-013-diataxis/reports/transparency-report-proj-013.md`*
*Output: `projects/PROJ-013-diataxis/reviews/adversary-r1-premortem-fmea.md`*
*Executed: 2026-02-27*
*Agent: adv-executor*
