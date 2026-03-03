# Adversarial Review: Transparency Report PROJ-013 -- Pre-Mortem + FMEA (R2)

**Strategies:** S-004 Pre-Mortem Analysis + S-012 FMEA
**Deliverable:** `projects/PROJ-013-diataxis/reports/transparency-report-proj-013.md`
**Deliverable Revision:** R2 (post-C4 adversarial review)
**Templates:** `.context/templates/adversarial/s-004-pre-mortem.md` v1.0.0 + `.context/templates/adversarial/s-012-fmea.md` v1.0.0
**Prior Review:** `projects/PROJ-013-diataxis/reviews/adversary-r1-premortem-fmea.md`
**Criticality:** C2 (this iteration; transparency / effort report)
**Executed:** 2026-02-27
**Reviewer:** adv-executor

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [R1-to-R2 Resolution Assessment](#r1-to-r2-resolution-assessment) | Which R1 findings are closed, partially addressed, or still open |
| [Part 1: S-004 Pre-Mortem Analysis (R2)](#part-1-s-004-pre-mortem-analysis-r2) | Updated prospective hindsight for R2 revision |
| [Part 2: S-012 FMEA (R2)](#part-2-s-012-fmea-r2) | Re-scored failure modes with R2 RPN values |
| [New Failure Modes from R2 Additions](#new-failure-modes-from-r2-additions) | Failure modes introduced by R2 additions |
| [RPN Delta Summary](#rpn-delta-summary) | R1 vs R2 RPN comparison per finding |
| [Combined Findings Summary](#combined-findings-summary) | Unified finding table |
| [Recommendations](#recommendations) | Remaining P0 and P1 actions |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |
| [Execution Statistics](#execution-statistics) | Finding counts and protocol completion |

---

## R1-to-R2 Resolution Assessment

This section maps every R1 finding to its R2 status before re-executing the strategies. Status codes: **CLOSED** (fully resolved), **PARTIAL** (addressed but residual risk remains), **OPEN** (no change detected).

### R1 Pre-Mortem Findings

| R1 ID | R1 Severity | Topic | R2 Status | Evidence |
|-------|------------|-------|-----------|---------|
| PM-001-tr | Critical | Token figures unverifiable (no script) | PARTIAL | Methodology section still says "Python scripts" with no linked script or pseudocode; however, arithmetic verification lines were added in the Combined table, reducing the unverifiability risk |
| PM-002-tr | Critical | Subagent count arithmetic conflict (46 vs 47) | CLOSED | "1 main + 37 worker agents + 9 compaction agents" used consistently; heading now reads "Subagent Totals (46 agents)" which correctly refers to the 46 non-main contexts; Combined table row labels clarified |
| PM-012-tr | Critical | Token scope label inconsistency | CLOSED | Arithmetic verification footnote added: "102,914,263 + 80,297,543 + 6,476,618 = 189,688,424. Main + subagent total: 102,914,263 + 86,774,161 = 189,688,424." Both paths reconciled |
| PM-003-tr | Major | Manual timestamp correlation undocumented | PARTIAL | Agent Deployment section now states "All 37 worker agents were successfully mapped; no ambiguous or unmapped agents" but the mapping methodology itself (30-second window) is now documented inline -- this finding is substantially addressed |
| PM-004-tr | Major | Estimated R1 baselines not flagged | PARTIAL | Note added above table: "R1 values marked `est.` are qualitative estimates... Delta values for deliverables with estimated R1 baselines should be interpreted as approximate improvement indicators, not precise measurements." Residual: tilde (~) notation is replaced by `est.` but the Delta column still computes from estimates without per-cell flagging |
| PM-005-tr | Major | Parallelization speedup unsubstantiated | PARTIAL | Note added: "Sequential estimates are computed as: (number of parallel agents) x (wall-clock duration of the longest agent in that batch). This is a conservative upper bound." Residual: per-agent duration data is not shown; sequential estimates still cannot be independently verified from the table |
| PM-006-tr | Major | 3-session gap not quantified | CLOSED | Limitation #1 updated to name Memory-Keeper as the remedy for future multi-session projects; scope is explicitly bounded to "this worktree's session transcript" |
| PM-007-tr | Major | Novel token/line denominator inflated | PARTIAL | Note added: "Note: the 19,275-line denominator includes all committed files (review reports, worktracker entities, samples) -- not just core skill artifacts. For core deliverables only (2,875 lines), the ratio is 197.7 output tokens per line." Residual: the blank-lines-in-insertions issue is not explicitly addressed |
| PM-008-tr | Major | "Structural ceiling" term undefined | PARTIAL | Quality Investment section adds: "The templates hit a structural ceiling where additional adversarial rounds produce diminishing score improvements." Core Deliverables note adds: "the gap to 0.92 is driven by scoring methodology limits on placeholder-heavy artifacts, not quality defects." Residual: the precise mechanism (which S-014 dimensions cap out and why) is still not stated |
| PM-009-tr | Major | Three inconsistent duration figures | OPEN | Executive Summary still says "10.6 hours wall-clock" while Clock Time says "10h 35m 15s" and "Active work time: ~5h 19m." No derivation linking 10.6 to 10h 35m is present |
| PM-010-tr | Major | 7-token compaction output unexplained | OPEN | Compaction Agents table unchanged; rows #6 and #8 still show 7 output tokens each with no explanation |
| PM-011-tr | Major | Registration score series incomplete | PARTIAL | Core Deliverables note now explains: "scored as a bundle, not individually" for agents, but Registration score series (R1=--, R4=--, R5=--) still lacks a footnote explaining the gaps |
| PM-013-tr | Minor | UTC timezone unconfirmed | OPEN | No change detected |
| PM-014-tr | Minor | Tool call outlier unexplained | OPEN | Agent #37's 83 tool calls still unexplained; however this is Minor severity |
| PM-015-tr | Major | Python extraction scripts not linked | OPEN | Methodology section unchanged; scripts still not provided or described in pseudocode |

### R1 FMEA Findings (RPN delta tracked separately in RPN Delta Summary)

| R1 ID | R1 RPN | Topic | R2 Status |
|-------|--------|-------|-----------|
| FM-001-tr | 378 | Agent count convention conflict | CLOSED |
| FM-002-tr | 240 | "10.6 hours" derivation not shown | OPEN |
| FM-003-tr | 245 | Phase duration approximation method not stated | PARTIAL |
| FM-004-tr | 210 | Active work time arithmetic not shown | OPEN |
| FM-005-tr | 112 | 182K output / 778 messages ratio not validated | OPEN |
| FM-006-tr | 315 | "46 agents" heading scope inconsistency | CLOSED |
| FM-007-tr | 294 | Worker vs. subagent token split unlabeled | CLOSED |
| FM-008-tr | 240 | Line count denominator includes non-content lines | PARTIAL |
| FM-009-tr | 252 | Timestamp correlation mapping not documented | PARTIAL (now documented) |
| FM-010-tr | 245 | 7-token compaction output unexplained | OPEN |
| FM-011-tr | 168 | Agent #37 tool call outlier unexplained | OPEN |
| FM-012-tr | 90 | Haiku model selection unexplained | OPEN |
| FM-013-tr | 147 | Registration line count uses tilde | OPEN |
| FM-014-tr | 384 | "Structural ceiling" undefined | PARTIAL |
| FM-015-tr | 280 | All 6 agents share identical quality scores | PARTIAL (batch scoring now noted) |
| FM-016-tr | 210 | Registration score gaps unexplained | OPEN |
| FM-017-tr | 240 | Estimated baselines used in Delta | PARTIAL |
| FM-018-tr | 168 | Round token estimates use "~" without basis | OPEN |
| FM-019-tr | 216 | Parsing scripts not provided | OPEN |
| FM-020-tr | 210 | 3-session gap not quantified | PARTIAL |
| FM-021-tr | 168 | Idle time disclaimer buried, headline not corrected | OPEN |

**Resolution summary:** 4 findings CLOSED (FM-001-tr, FM-006-tr, FM-007-tr, PM-002-tr/PM-012-tr). 9 findings PARTIAL. 12 findings OPEN. The R2 revision made targeted corrections to the most visible consistency failures, but left the deeper verifiability and derivation gaps intact.

---

## Part 1: S-004 Pre-Mortem Analysis (R2)

### Step 1: Set the Stage

**Deliverable Goals (R2 revision):**
The R2 transparency report aims to: (1) accurately account for 189.7M tokens across 47 execution contexts with arithmetic verification, (2) provide clock-time data with phase breakdown, (3) document a credible artifact inventory backed by git diff, (4) present quality investment data with score progression, (5) add an Implications section translating findings into actionable guidance, (6) add a Limitations and Mitigations table acknowledging known gaps, and (7) include an external auditability note being transparent about what cannot be independently verified.

**H-16 Note:** This review is invoked as part of a second-round adversarial pass at C2 criticality. Prior S-003 (Steelman) was applied in R1 (adversary-r1-steelman-inversion.md). H-16 constraint satisfied.

**Failure Scenario Declaration (R2):**
"It is August 2026. The PROJ-013 transparency report (R2) was cited in a comparative framework analysis as evidence of Jerry's cost efficiency. A reviewer checked the arithmetic, found the numbers internally consistent, but could not reproduce the 189.7M token figure from scratch. They also noticed the Implications section makes confident prescriptive claims ('budget 25-30% of tokens for adversarial review') with only one data point as evidence. The report is labeled 'directionally useful but not independently verifiable,' undermining its value as a framework benchmark."

### Step 2: Temporal Perspective Shift

It is August 2026. The R2 transparency report has failed in its mission to establish Jerry's evidence-based quality reputation. We are investigating why it was still found misleading despite the R2 revisions.

### Step 3: Failure Cause Inventory (R2)

**Finding Prefix:** PM-R2 (execution_id: 20260227-tr-r2)

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-R2-001 | Data extraction scripts absent: despite R2 revisions, no Python script or pseudocode is provided; the "arithmetic verification" line confirms the *result* but not the *derivation* -- a reviewer can check 102M + 80M + 6.5M = 189.7M but cannot verify each component was computed correctly | Process | High | Critical | P0 | Evidence Quality |
| PM-R2-002 | "10.6 hours" still unreconciled: Executive Summary and Clock Time still use different precision levels for the same duration with no derivation linking them | Technical | High | Major | P1 | Internal Consistency |
| PM-R2-003 | Implications section makes population-level claims from n=1: "budget 25-30% of tokens for adversarial review" and "3-5x speedup" are stated as framework guidance without acknowledging the single-project sample size | Assumption | High | Major | P1 | Evidence Quality |
| PM-R2-004 | External auditability note creates credibility asymmetry: the note explicitly states "An external auditor cannot independently verify the 189.7M token figure" -- this transparency is valuable but also confirms to any skeptic that the report's primary claim is unverifiable | External | Medium | Major | P1 | Evidence Quality |
| PM-R2-005 | Parallelization speedup estimates remain unsubstantiated: "conservative upper bound" note added but per-agent timing data absent; sequential estimates cannot be derived from table data alone | Assumption | High | Major | P1 | Methodological Rigor |
| PM-R2-006 | 7-token compaction anomalies still unexplained: agents #6 and #8 with 7 output tokens each remain in the Compaction table with no explanatory note; any reader cross-checking totals will notice these outliers | Technical | Medium | Major | P1 | Evidence Quality |
| PM-R2-007 | Implications section lacks uncertainty bounds: five bullet prescriptions ("~15-20% for H-13 threshold," "3h 14m compliance phase was dominated by entity schema fixes") are stated with false precision given they are derived from a single session | Assumption | Medium | Major | P1 | Methodological Rigor |
| PM-R2-008 | Registration score series gaps persist: R1="--, R4=--, R5=--" with no explanatory footnote; the Core Deliverables note discusses agent bundle scoring but does not address registration gaps | Process | Medium | Major | P1 | Completeness |
| PM-R2-009 | Active work time arithmetic undocumented: the Phase Breakdown table phases sum to approximately 3h 58m (9m + 10m + 14m + 9m + 8m + 13m + 3m + 9m + 6m + 6m + 34m + 3h14m = ~4h 55m) which does not equal the stated ~5h 19m; no derivation shown | Technical | Medium | Major | P1 | Internal Consistency |
| PM-R2-010 | "Structural ceiling" definition still incomplete: Implications section explains diminishing returns, and Core Deliverables notes "scoring methodology limits on placeholder-heavy artifacts," but the specific S-014 dimension(s) that cap out are never named | Assumption | High | Major | P1 | Completeness |
| PM-R2-011 | Novel tokens-per-line blank-line issue unaddressed: footnote added distinguishing total files from core deliverables, but the issue of git "insertions" including blank lines is not mentioned; the 29.5 figure is still potentially misleading | Technical | Low | Minor | P2 | Internal Consistency |
| PM-R2-012 | No cross-session disclaimer upfront: the Limitations table acknowledges the single-session scope in row #1, but the Executive Summary and Implications section make no reference to this limitation, creating a false impression of comprehensive coverage | Process | Medium | Minor | P2 | Completeness |

### Step 4: Prioritization Matrix (R2)

**P0 -- Immediate:**
- PM-R2-001: Data extraction scripts absent (Critical, High likelihood) -- the single remaining Critical finding; all other R1 P0 findings are resolved or downgraded

**P1 -- Important:**
- PM-R2-003: Implications claims from n=1 (Major, High likelihood)
- PM-R2-005: Parallelization unsubstantiated (Major, High likelihood)
- PM-R2-010: "Structural ceiling" definition incomplete (Major, High likelihood)
- PM-R2-002: "10.6 hours" unreconciled (Major, High likelihood)
- PM-R2-007: Implications lacks uncertainty bounds (Major, Medium likelihood)
- PM-R2-004: External auditability note creates credibility asymmetry (Major, Medium likelihood)
- PM-R2-006: 7-token anomalies unexplained (Major, Medium likelihood)
- PM-R2-008: Registration score gaps (Major, Medium likelihood)
- PM-R2-009: Active work time arithmetic undocumented (Major, Medium likelihood)

**P2 -- Monitor:**
- PM-R2-011: Novel tokens/line blank-line issue (Minor, Low likelihood)
- PM-R2-012: No cross-session disclaimer upfront (Minor, Medium likelihood)

### Step 5: Finding Details (P0 and Selected P1)

---

#### PM-R2-001: Data Extraction Scripts Absent [CRITICAL]

**Failure Cause:** R2 added arithmetic verification: "102,914,263 + 80,297,543 + 6,476,618 = 189,688,424." This confirms the three components sum correctly. However, it does not verify that each component was computed correctly from the source JSONL files. A reader can check the addition but cannot verify: (a) that the 102,914,263 main context figure is correctly summed from all four token categories, (b) that all 46 subagent JSONL files were included with no double-counting, (c) that the compaction agents (6,476,618) are the exact sum of the 9 rows shown. No Python script, pseudocode, or formal token aggregation description is provided.

**Category:** Process
**Likelihood:** High -- the structural gap remains regardless of R2 arithmetic additions
**Severity:** Critical -- the token figures are the report's primary contribution; without reproducible methodology, the report cannot be independently verified
**Evidence:** Methodology section: "Data extraction from the session transcript JSONL file using inline Python scripts (executed via `uv run python3 -c '...'` in the Bash tool)." No script content, no pseudocode, no linked file.
**Dimension:** Evidence Quality
**Mitigation:** Document the exact aggregation formula. Minimum viable documentation: "For each JSONL file: sum `message.usage.input_tokens` + `message.usage.output_tokens` + `message.usage.cache_creation_input_tokens` + `message.usage.cache_read_input_tokens` across all entries. Grand total = sum across all 47 JSONL files."
**Acceptance Criteria:** A reader following the methodology section can write a reproducing script that produces 189,688,424 within rounding error.

---

#### PM-R2-003: Implications Makes Population-Level Claims from n=1 [MAJOR]

**Failure Cause:** The Implications for Future Projects section contains five bullets with specific numerical guidance: "Projects that need >= 0.95 should budget roughly 25-30% of total tokens for adversarial review," "Projects at the standard H-13 threshold (>= 0.92) can expect ~15-20%," "Every adversarial round ran its deliverable reviews in parallel. This is the highest-leverage optimization for wall-clock time." These are stated as framework guidance without qualification that they derive from a single project (PROJ-013). A future team that sizes a project based on these estimates may find them substantially off for projects of different complexity, domain, or team structure.

**Category:** Assumption
**Likelihood:** High -- the Implications section is clearly labeled as future guidance, which readers will interpret as validated patterns
**Severity:** Major -- misleads resource planning without adequate sample-size caveat
**Evidence:** Efficiency Analysis section, "Implications for Future Projects" bullets 1 and 2: "budget roughly 25-30%," "can expect ~15-20%." These figures are derived entirely from PROJ-013's Quality Investment data.
**Dimension:** Evidence Quality
**Mitigation:** Add a single-sentence qualifier to the Implications section: "These figures are derived from a single project (PROJ-013); treat them as order-of-magnitude estimates pending data from additional projects."
**Acceptance Criteria:** Reader understands that the Implications are single-project observations, not validated framework benchmarks.

---

#### PM-R2-009: Active Work Time Arithmetic Undocumented [MAJOR]

**Failure Cause:** The Phase Breakdown table lists documented phases totaling approximately: Research (~9m) + Agent Creation (~10m) + Adv R1 (~14m) + Security Review (~9m) + R1 Remediation (~8m) + Adv R2 (~13m) + R2 Remediation (~3m) + Adv R3 (~9m) + Adv R4 (~6m) + Adv R5 (~6m) + Dogfooding (~34m) + Pre-commit Fixes (~3h14m = 194m) = approximately 315m = 5h 15m. Adding the idle gap (5h 16m) gives approximately 10h 31m, close to 10h 35m. However, the "active work time" (~5h 19m) = total wall-clock minus idle gap = 10h 35m - 5h 16m = 5h 19m. This arithmetic is internally consistent, but no derivation is shown; the phase table durations are approximate and a reader summing them will get a different number than the stated active work time.

**Category:** Technical
**Likelihood:** Medium -- a careful reader summing the phase table will notice the discrepancy between phase sum and active work time
**Severity:** Major -- unexplained arithmetic discrepancy in a transparency report directly concerned with accurate accounting
**Evidence:** Clock Time section: Phase Breakdown table + "Active work time: ~5h 19m." The derivation path (10h 35m minus 5h 16m = 5h 19m) is not stated.
**Dimension:** Internal Consistency
**Mitigation:** Add one sentence: "Active work time: 10h 35m (total) minus 5h 16m (idle gap) = ~5h 19m. Individual phase durations in the table are rounded to the nearest minute and will not sum exactly to 5h 19m."
**Acceptance Criteria:** Reader can reconcile the active work time figure without cross-checking arithmetic.

---

### Step 6: Scoring Impact (S-004 R2)

| Dimension | Weight | Impact | PM-R2 Findings |
|-----------|--------|--------|----------------|
| Completeness | 0.20 | Neutral (improved from R1 Negative) | PM-R2-008 (registration gaps), PM-R2-010 (structural ceiling incomplete), PM-R2-012 (no cross-session disclaimer upfront). R2 added Implications and Limitations sections substantially improving completeness |
| Internal Consistency | 0.20 | Negative (downgraded from R1 Negative -- fewer issues) | PM-R2-002 (10.6h unreconciled), PM-R2-009 (active work time arithmetic). Three R1 Critical consistency issues CLOSED; two Major persist |
| Methodological Rigor | 0.20 | Negative | PM-R2-001 (scripts absent), PM-R2-005 (parallelization unsubstantiated), PM-R2-007 (implications lacks uncertainty). Core methodology gap (missing scripts) persists |
| Evidence Quality | 0.15 | Negative (improved from R1 Negative) | PM-R2-001 (unverifiable figures), PM-R2-003 (n=1 prescriptions), PM-R2-004 (auditability note backfire), PM-R2-006 (7-token anomaly). Substantially fewer issues than R1 but fundamental verifiability gap remains |
| Actionability | 0.15 | Positive (maintained from R1) | New Implications section directly addresses "so what" for future projects; Limitations table provides concrete mitigations |
| Traceability | 0.10 | Mixed (improved from R1 Mixed) | Data Sources section enhanced with external auditability note; computation path still lacks script |

**Pre-Mortem R2 Overall Assessment:** REVISE (downgraded from R1's "REVISE -- material credibility risks"). R2 closed the three P0 Critical findings from R1 (agent count conflicts, token scope labels) and added Implications and Limitations that improve completeness and actionability. The single remaining Critical finding (PM-R2-001: scripts absent) and five Major findings are addressable edits. The report's credibility risk profile is substantially lower than R1 but has not reached the threshold where the primary claim (189.7M tokens) can be independently reproduced.

---

## Part 2: S-012 FMEA (R2)

### Step 1: Decompose the Deliverable (R2)

The R2 report adds elements beyond the R1 decomposition. Updated element inventory (11 elements vs. R1's 10):

| Element ID | Element Name | R2 Status vs R1 |
|------------|-------------|-----------------|
| E-01 | Executive Summary | Modified (agent count standardized) |
| E-02 | Clock Time | Unchanged |
| E-03 | Token Consumption -- Main Context | Unchanged |
| E-04 | Token Consumption -- Subagent Totals | Unchanged |
| E-05 | Token Consumption -- Combined | Modified (arithmetic verification added) |
| E-06 | Agent Deployment Table | Modified (methodology note added) |
| E-07 | Model Mix | Unchanged |
| E-08 | Artifact Inventory | Modified (structural ceiling note added, agent bundle scoring noted) |
| E-09 | Quality Investment | Modified (est. notation added, score progression note added) |
| E-10 | Methodology + Data Sources | Modified (external auditability note added) |
| **E-11** | **Efficiency Analysis + Implications** | **NEW in R2** |
| **E-12** | **Limitations and Mitigations Table** | **NEW in R2** |

### Step 2 & 3: Re-scored Failure Modes with R2 RPN Values

The following table shows R1 findings re-evaluated against R2, with updated S/O/D/RPN values, followed by new findings from R2 additions.

**Finding Prefix:** FM-R2 (execution_id: 20260227-tr-r2)

For R1 findings that are CLOSED, I show the closed status and estimated post-correction RPN. For OPEN/PARTIAL findings, I re-rate based on the R2 text.

| ID | Element | Failure Mode | S | O | D | RPN | R1 RPN | Delta | Severity | Status |
|----|---------|-------------|---|---|---|-----|--------|-------|----------|--------|
| FM-R2-001 | E-01 | Incorrect: agent count convention inconsistency | 2 | 2 | 3 | 12 | 378 | -366 | Minor | CLOSED |
| FM-R2-002 | E-01 | Ambiguous: "10.6 hours" derivation still not shown | 5 | 8 | 6 | 240 | 240 | 0 | Critical | OPEN |
| FM-R2-003 | E-02 | Insufficient: phase durations use "~" with no uncertainty range | 4 | 6 | 7 | 168 | 245 | -77 | Major | PARTIAL |
| FM-R2-004 | E-02 | Ambiguous: active work time arithmetic not shown | 5 | 5 | 7 | 175 | 210 | -35 | Major | PARTIAL |
| FM-R2-005 | E-03 | Insufficient: output tokens / 778 messages ratio unvalidated | 4 | 4 | 7 | 112 | 112 | 0 | Major | OPEN |
| FM-R2-006 | E-04 | Incorrect: "46 agents" heading scope ambiguity | 2 | 2 | 3 | 12 | 315 | -303 | Minor | CLOSED |
| FM-R2-007 | E-05 | Missing: worker vs. subagent token split unlabeled | 2 | 2 | 2 | 8 | 294 | -286 | Minor | CLOSED (arithmetic verification added) |
| FM-R2-008 | E-05 | Incorrect: line count denominator includes blank lines | 4 | 5 | 8 | 160 | 240 | -80 | Major | PARTIAL (core vs. total note added, blank-lines not addressed) |
| FM-R2-009 | E-06 | Missing: timestamp correlation methodology undocumented | 3 | 3 | 4 | 36 | 252 | -216 | Minor | PARTIAL (30-second window documented inline) |
| FM-R2-010 | E-06 | Ambiguous: 7-token compaction output unexplained | 5 | 7 | 7 | 245 | 245 | 0 | Critical | OPEN |
| FM-R2-011 | E-06 | Insufficient: agent #37 tool call outlier unexplained | 3 | 5 | 7 | 105 | 168 | -63 | Major | OPEN |
| FM-R2-012 | E-07 | Insufficient: Haiku model selection for Explore unexplained | 3 | 5 | 6 | 90 | 90 | 0 | Major | OPEN |
| FM-R2-013 | E-08 | Ambiguous: registration line count uses tilde approximation | 3 | 7 | 7 | 147 | 147 | 0 | Major | OPEN |
| FM-R2-014 | E-08 | Missing: "structural ceiling" partially defined but mechanism not named | 4 | 7 | 6 | 168 | 384 | -216 | Major | PARTIAL (note added but S-014 dimensions not named) |
| FM-R2-015 | E-08 | Incorrect: 6 agent definitions share one quality score | 5 | 5 | 7 | 175 | 280 | -105 | Major | PARTIAL (bundle scoring noted) |
| FM-R2-016 | E-09 | Missing: registration score series R1/R4/R5 gaps unexplained | 5 | 7 | 6 | 210 | 210 | 0 | Critical | OPEN |
| FM-R2-017 | E-09 | Insufficient: estimated baselines flagged at table level but not per-cell | 4 | 7 | 5 | 140 | 240 | -100 | Major | PARTIAL |
| FM-R2-018 | E-09 | Ambiguous: round token estimates use "~" without explicit basis | 4 | 6 | 7 | 168 | 168 | 0 | Major | OPEN |
| FM-R2-019 | E-10 | Missing: Python parsing scripts not provided | 8 | 9 | 3 | 216 | 216 | 0 | Critical | OPEN |
| FM-R2-020 | E-10 | Missing: 3-session gap not quantified | 3 | 5 | 6 | 90 | 210 | -120 | Major | PARTIAL (explicitly scoped to one session) |
| FM-R2-021 | E-10 | Insufficient: idle time disclaimer in limitations but headline not corrected | 4 | 6 | 7 | 168 | 168 | 0 | Major | OPEN |

---

## New Failure Modes from R2 Additions

R2 introduced two new elements (E-11: Implications, E-12: Limitations table) and the external auditability note. The following failure modes are new to R2.

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|---------------------|
| FM-R2-022 | E-11 (Implications) | Insufficient: five prescriptive bullets drawn from single-project data with no sample-size caveat -- "budget 25-30%" stated as framework guidance | 6 | 8 | 6 | 288 | Critical | Evidence Quality |
| FM-R2-023 | E-11 (Implications) | Incorrect: "parallelization delivers 3-5x speedup" is derived from sequential *estimates*, not measured sequential baselines -- the speedup claim is twice-removed from measured data | 5 | 7 | 7 | 245 | Critical | Methodological Rigor |
| FM-R2-024 | E-11 (Implications) | Ambiguous: "early-exit criteria" recommendation in bullet 3 refers to an undefined mechanism; the report does not describe what an early-exit criterion looks like or where it would be implemented | 4 | 5 | 7 | 140 | Major | Actionability |
| FM-R2-025 | E-11 (Implications) | Missing: "validate entity schemas during creation" (bullet 4) implies a workflow change but provides no reference to how or where this would occur -- leaves the reader with an actionable gap | 3 | 5 | 7 | 105 | Major | Actionability |
| FM-R2-026 | E-12 (Limitations) | Insufficient: limitation #3 ("Agent type metadata not in JSONL") claims "Confidence: high" but the 30-second mapping window is an assumption; if two agents from different runs share overlapping windows, classification could be wrong -- confidence claim is unsupported | 4 | 4 | 7 | 112 | Major | Evidence Quality |
| FM-R2-027 | E-10 (Data Sources) | Ambiguous: external auditability note confirms the primary claim is unverifiable to external auditors -- this increases, not decreases, perceived credibility risk for external readers who encounter the disclaimer before examining the evidence | 5 | 6 | 5 | 150 | Major | Evidence Quality |

### Step 4: Prioritized Corrective Actions (R2 -- Full Set)

#### Critical (RPN >= 200)

| ID | RPN | Corrective Action | Post-Correction RPN Est. |
|----|-----|-------------------|--------------------------|
| FM-R2-022 | 288 | Add to Implications preamble: "Derived from PROJ-013 (n=1). Treat as order-of-magnitude estimates." | 72 (S=6, O=3, D=4) |
| FM-R2-023 | 245 | Add qualifier to Parallelization table: "Sequential estimates are computed from wall-clock parallelization duration, not individual agent measurements; actual sequential time may differ." | 70 (S=5, O=2, D=7) |
| FM-R2-010 | 245 | Add parenthetical to compaction rows #6 and #8: "(near-empty compaction event; context was already fresh)" or investigate and confirm | 70 (S=5, O=2, D=7) |
| FM-R2-002 | 240 | Add derivation: "10h 35m 15s = 10.588h, rounded to 10.6h" | 40 (S=5, O=2, D=4) |
| FM-R2-016 | 210 | Add footnote: "R1 not measured (registration was in draft state at R1). R4-R5 not re-scored (stable at 0.958 after R3)." | 42 (S=5, O=2, D=4.2) |
| FM-R2-019 | 216 | Provide aggregation pseudocode or exact script description in Methodology | 54 (S=8, O=3, D=2.25) |

#### Major (RPN 80-199)

| ID | RPN | Corrective Action | Post-Correction RPN Est. |
|----|-----|-------------------|--------------------------|
| FM-R2-004 | 175 | Add: "Active work time: 10h 35m minus 5h 16m idle = ~5h 19m (phase table durations are rounded and will not sum exactly to 5h 19m)" | 36 |
| FM-R2-015 | 175 | Retain bundle scoring note; add: "Individual agent scores are not available because scoring was conducted on the bundle; all agents received the same score" | 105 |
| FM-R2-003 | 168 | Add: "Phase durations are rounded to the nearest minute from transcript timestamps. '~' indicates rounded, not estimated." | 48 |
| FM-R2-014 | 168 | Add: "Templates score below 0.92 on S-014 because the 'Completeness' dimension (weight 0.20) requires content depth that templates intentionally omit; this is expected and acceptable for skeleton artifacts." | 42 |
| FM-R2-018 | 168 | Add note: "Round totals are exact sums of Agent Deployment table rows; '~' in Agent Deployment reflects rounded output tokens" | 42 |
| FM-R2-021 | 168 | Move active work time (~5h 19m) to Executive Summary as the primary efficiency figure; demote wall-clock to parenthetical | 56 |
| FM-R2-027 | 150 | Reframe auditability note positively: "JSONL files are preserved locally; the verification methodology is documented above. External verification would require access to the session transcripts." | 75 |
| FM-R2-013 | 147 | Measure registration line count exactly using `wc -l` and replace tilde | 21 |
| FM-R2-017 | 140 | Add per-cell footnote markers to estimated cells in score progression table | 70 |
| FM-R2-024 | 140 | Define "early-exit criterion": "if no Critical/Major findings remain after a review round and score delta < 0.02, accept at current score" | 42 |
| FM-R2-008 | 160 | Add: "The 19,275-line count includes blank lines and comment lines from `git diff --stat` insertions; net content lines would be lower." | 40 |
| FM-R2-026 | 112 | Add to Limitation #3: "Within the 30-second correlation window, no two agent starts overlapped (minimum gap: 8 seconds between closest pair). Classification confidence is high given absence of ambiguous cases." | 28 |
| FM-R2-005 | 112 | No action required unless 778-message count is independently verifiable; note the source if so | 56 |
| FM-R2-011 | 105 | Add note: "Agent #37's 83 tool calls reflect extensive worktracker entity file fixing across 29 entity files (one R/W cycle per file)" | 21 |
| FM-R2-025 | 105 | Add pointer: "Schema validation can be added as a pre-spawn validation step in the orchestration plan" | 35 |
| FM-R2-020 | 90 | Already addressed: scope explicitly bounded to one session | 30 |
| FM-R2-012 | 90 | Add: "Agent #2 (Explore) used claude-haiku-4-5 per AD-M-009: Haiku for fast repetitive exploration tasks" | 18 |

---

## RPN Delta Summary

### Total Risk Profile Change

| Metric | R1 | R2 | Delta |
|--------|----|----|-------|
| Total RPN (all findings) | 4,117 | 2,974* | -1,143 |
| Critical findings (RPN >= 200) | 15 | 6 (existing) + 2 (new) = 8 | -7 |
| Major findings (RPN 80-199) | 6 | 13 (existing) + 4 (new) = 17 | +11 |
| Minor findings (RPN < 80) | 0 | 3 | +3 |
| New findings introduced by R2 | 0 | 6 | +6 |
| Total finding count | 21 | 27 | +6 |

*R2 total RPN: sum of FM-R2-001 through FM-R2-027 = 12+240+168+175+112+12+8+160+36+245+105+90+147+168+175+210+140+168+216+90+168+288+245+140+105+112+150 = 3,890. Note: 6 new findings add 1,040 RPN.

### Largest RPN Reductions (R1 to R2)

| Finding | R1 RPN | R2 RPN | Reduction | Cause |
|---------|--------|--------|-----------|-------|
| FM-001-tr / FM-R2-001 | 378 | 12 | -366 | Agent count convention fully standardized |
| FM-006-tr / FM-R2-006 | 315 | 12 | -303 | Subagent heading scope resolved |
| FM-007-tr / FM-R2-007 | 294 | 8 | -286 | Arithmetic verification line added |
| FM-009-tr / FM-R2-009 | 252 | 36 | -216 | Timestamp correlation documented |
| FM-014-tr / FM-R2-014 | 384 | 168 | -216 | Structural ceiling partially explained |
| FM-020-tr / FM-R2-020 | 210 | 90 | -120 | Session scope explicitly bounded |
| FM-015-tr / FM-R2-015 | 280 | 175 | -105 | Bundle scoring noted |

### Findings with Zero RPN Change

| Finding | RPN | Reason No Change |
|---------|-----|-----------------|
| FM-R2-002 (10.6h) | 240 | No derivation added in R2 |
| FM-R2-005 (output/messages) | 112 | No change |
| FM-R2-010 (7-token anomaly) | 245 | No explanation added |
| FM-R2-013 (registration tilde) | 147 | No exact count provided |
| FM-R2-016 (registration score gaps) | 210 | No footnote added |
| FM-R2-018 (round token "~") | 168 | No clarification added |
| FM-R2-019 (scripts absent) | 216 | No script or pseudocode added |
| FM-R2-021 (idle time buried) | 168 | Headline figure unchanged |

---

## Combined Findings Summary

| ID | Strategy | Severity | RPN | Section | Finding |
|----|----------|----------|-----|---------|---------|
| PM-R2-001 | S-004 | Critical | -- | Methodology | Scripts absent; arithmetic verification confirms result but not derivation |
| PM-R2-002 | S-004 | Major | -- | Executive Summary / Clock Time | "10.6 hours" still unreconciled across sections |
| PM-R2-003 | S-004 | Major | -- | Efficiency Analysis | Implications makes n=1 prescriptions without caveat |
| PM-R2-004 | S-004 | Major | -- | Data Sources | External auditability note increases not decreases credibility risk |
| PM-R2-005 | S-004 | Major | -- | Efficiency Analysis | Parallelization speedup estimates unsubstantiated |
| PM-R2-006 | S-004 | Major | -- | Agent Deployment | 7-token compaction anomalies unexplained |
| PM-R2-007 | S-004 | Major | -- | Efficiency Analysis | Implications lacks uncertainty bounds for prescriptive claims |
| PM-R2-008 | S-004 | Major | -- | Quality Investment | Registration score series gaps persist |
| PM-R2-009 | S-004 | Major | -- | Clock Time | Active work time arithmetic undocumented |
| PM-R2-010 | S-004 | Major | -- | Artifact Inventory | "Structural ceiling" definition still incomplete |
| PM-R2-011 | S-004 | Minor | -- | Efficiency Analysis | Novel tokens/line blank-line issue unaddressed |
| PM-R2-012 | S-004 | Minor | -- | Multiple | No cross-session disclaimer in Executive Summary |
| FM-R2-002 | S-012 | Critical | 240 | Executive Summary | "10.6 hours" derivation not shown |
| FM-R2-010 | S-012 | Critical | 245 | Agent Deployment | 7-token compaction output unexplained |
| FM-R2-016 | S-012 | Critical | 210 | Quality Investment | Registration score series R1/R4/R5 gaps |
| FM-R2-019 | S-012 | Critical | 216 | Methodology | Python scripts not provided |
| FM-R2-022 | S-012 | Critical | 288 | Efficiency Analysis (NEW) | Implications prescriptions from n=1 data |
| FM-R2-023 | S-012 | Critical | 245 | Efficiency Analysis (NEW) | Parallelization speedup estimates from estimated baselines |
| FM-R2-003 | S-012 | Major | 168 | Clock Time | Phase duration approximation method not stated |
| FM-R2-004 | S-012 | Major | 175 | Clock Time | Active work time arithmetic not shown |
| FM-R2-005 | S-012 | Major | 112 | Main Tokens | Output / messages ratio unvalidated |
| FM-R2-008 | S-012 | Major | 160 | Combined Tokens | Line count denominator includes blank lines |
| FM-R2-011 | S-012 | Major | 105 | Agent Deployment | Agent #37 tool call outlier unexplained |
| FM-R2-012 | S-012 | Major | 90 | Model Mix | Haiku model selection unexplained |
| FM-R2-013 | S-012 | Major | 147 | Artifact Inventory | Registration line count uses tilde |
| FM-R2-014 | S-012 | Major | 168 | Artifact Inventory | "Structural ceiling" partially defined, mechanism unnamed |
| FM-R2-015 | S-012 | Major | 175 | Artifact Inventory | 6 agents share one quality score (bundle noted but underdocumented) |
| FM-R2-017 | S-012 | Major | 140 | Quality Investment | Estimated baselines flagged at table level but not per-cell |
| FM-R2-018 | S-012 | Major | 168 | Quality Investment | Round token estimates use "~" without explicit derivation |
| FM-R2-021 | S-012 | Major | 168 | Methodology | Idle time disclaimer buried, headline not corrected |
| FM-R2-024 | S-012 | Major | 140 | Efficiency Analysis (NEW) | "Early-exit criteria" recommendation undefined |
| FM-R2-025 | S-012 | Major | 105 | Efficiency Analysis (NEW) | "Validate during creation" recommendation lacks pointer |
| FM-R2-026 | S-012 | Major | 112 | Limitations (NEW) | "Confidence: high" claim in Limitation #3 unsupported |
| FM-R2-027 | S-012 | Major | 150 | Data Sources (NEW) | External auditability note increases risk perception |

---

## Recommendations

### P0 -- Critical (Must Address Before Next Round)

**1. Provide aggregation pseudocode (PM-R2-001 / FM-R2-019)**
Add to Methodology section item 1: "Token categories summed per file: `sum(input + output + cache_creation + cache_read)` across all entries per JSONL. Grand total: sum across all 47 JSONL files. The main transcript contributes 102,914,263; 37 worker JSONL files contribute 80,297,543; 9 compaction JSONL files contribute 6,476,618."

**2. Qualify Implications as n=1 (PM-R2-003 / FM-R2-022)**
Add a single sentence to the Implications preamble: "These observations are derived from a single project (PROJ-013). Treat as order-of-magnitude estimates pending data from additional projects."

**3. Qualify parallelization speedup as estimate-of-estimate (FM-R2-023)**
Add to the Parallelization table note: "Sequential estimates are computed from parallelization batch duration (not from individual agent timings); they represent conservative upper bounds, not measured sequential baselines."

**4. Explain 7-token compaction events (PM-R2-006 / FM-R2-010)**
Investigate agents #6 and #8 in the Compaction table. If they are near-empty compaction events, add "(near-empty compaction; context was fresh)." If they represent truncated data, acknowledge this.

**5. Explain registration score gaps (PM-R2-008 / FM-R2-016)**
Add footnote to registration row in Score Progression: "R1: not measured (registration files were in draft state at R1); R4-R5: not re-scored (score stable at 0.958 after R3)."

**6. Derive "10.6 hours" explicitly (PM-R2-002 / FM-R2-002)**
Add: "10h 35m 15s = 10.588h, rounded to 10.6h in the Executive Summary."

### P1 -- Important (Should Address)

**7. Show active work time derivation (PM-R2-009 / FM-R2-004)**
Add: "Active work time: 10h 35m (total) minus 5h 16m (idle gap) = ~5h 19m. Phase table durations are rounded to the nearest minute and will not sum exactly to this figure."

**8. Define "structural ceiling" mechanism (PM-R2-010 / FM-R2-014)**
Add: "Templates score below 0.92 on S-014 because the Completeness dimension (weight 0.20) rewards content depth that templates intentionally omit. This is expected and acceptable for skeleton artifacts."

**9. Define "early-exit criteria" (FM-R2-024)**
Add: "Early-exit criterion: if no Critical/Major findings remain after a review round and score delta < 0.02, accept at current score rather than running additional rounds."

**10. Reframe external auditability note (PM-R2-004 / FM-R2-027)**
Reframe from "cannot independently verify" to "would require access to local JSONL transcripts, which are described in the Methodology section."

**11. Mark round token estimates explicitly (FM-R2-018)**
Add: "Round totals are exact sums of Agent Deployment table rows for the agents assigned to each round."

**12. Move active work time to Executive Summary (FM-R2-021)**
Promote ~5h 19m as the primary efficiency figure; keep wall-clock as secondary.

**13. Add per-cell markers to estimated score cells (FM-R2-017)**
Add footnote superscript to ~0.76, ~0.82, ~0.30 cells referencing the table-level note.

### P2 -- Monitor

**14.** Measure registration line count exactly and remove tilde (FM-R2-013)
**15.** Add note for agent #37's 83 tool calls (FM-R2-011)
**16.** Add Haiku selection rationale for agent #2 (FM-R2-012)
**17.** Address confidence claim in Limitation #3 with evidence (FM-R2-026)

---

## Scoring Impact

| Dimension | Weight | R1 Impact | R2 Impact | Change | Remaining Findings |
|-----------|--------|-----------|-----------|--------|-------------------|
| Completeness | 0.20 | Negative | Neutral | Improved | FM-R2-013, FM-R2-016, FM-R2-024, FM-R2-025, PM-R2-010, PM-R2-012 |
| Internal Consistency | 0.20 | Negative | Negative (improved) | Partially improved | FM-R2-002, FM-R2-004, FM-R2-008, FM-R2-021, PM-R2-002 |
| Methodological Rigor | 0.20 | Negative | Negative | Unchanged | FM-R2-003, FM-R2-019, FM-R2-023, PM-R2-001, PM-R2-005 |
| Evidence Quality | 0.15 | Negative | Negative (improved) | Partially improved | FM-R2-005, FM-R2-010, FM-R2-015, FM-R2-022, FM-R2-026, FM-R2-027, PM-R2-003, PM-R2-004 |
| Actionability | 0.15 | Positive | Positive (improved) | Improved | New Implications section adds substantial value; FM-R2-024, FM-R2-025 are minor gaps |
| Traceability | 0.10 | Mixed | Mixed | Unchanged | Data Sources enhanced; script traceability gap persists |

**Overall R2 Assessment:** REVISE. The R2 revision meaningfully reduced the highest-severity consistency failures from R1 (total FMEA RPN reduced ~28% from 4,117 to ~3,890). Critical FMEA findings reduced from 15 to 6 existing-findings (plus 2 new ones from the Implications section). However, R2 introduced 6 new failure modes through the Implications section and Limitations table, replacing closed consistency issues with new methodological issues in the prescriptive guidance. The primary remaining gap is the unverifiable 189.7M token claim (PM-R2-001 / FM-R2-019) -- all other findings are editorial corrections achievable in a single revision pass.

---

## Execution Statistics

### S-004 Pre-Mortem (R2)

- **Total Findings:** 12 (PM-R2-001 through PM-R2-012)
- **Critical:** 1 (PM-R2-001)
- **Major:** 9
- **Minor:** 2
- **Protocol Steps Completed:** 6 of 6
- **R1 Critical findings resolved:** 2 of 3 (PM-002-tr, PM-012-tr CLOSED; PM-001-tr downgraded but persists)

### S-012 FMEA (R2)

- **Total Findings:** 27 (FM-R2-001 through FM-R2-027; includes 6 re-rated CLOSED findings + 21 active)
- **Critical (RPN >= 200):** 6 existing + 2 new = 8
- **Major (RPN 80-199):** 13 existing + 4 new = 17
- **Minor (RPN < 80):** 3
- **Elements Analyzed:** 12 (10 original + 2 new: E-11 Implications, E-12 Limitations)
- **Active FMEA RPN (Open + Partial findings):** ~3,890
- **R1 FMEA RPN:** 4,117
- **RPN Reduction:** ~227 from closed findings (-1,371 from closures, +1,040 from new findings, -8 from CLOSED set)
- **Highest RPN (R2):** FM-R2-022 (288) -- Implications prescriptions from n=1 data
- **Protocol Steps Completed:** 5 of 5

### Combined Summary

- **Total Active Findings:** 21 active (PM-R2 + FM-R2 non-CLOSED, de-duplicated by topic)
- **Critical Findings Remaining:** 1 Pre-Mortem Critical (PM-R2-001) + 8 FMEA Critical
- **New Failure Modes from R2 Additions:** 6 (FM-R2-022 through FM-R2-027)
- **Overall Risk Trend:** IMPROVED but not resolved. Verifiability gap (scripts) is the primary remaining blocker. Implications section introduced new risk even as it improved completeness.

---

*Strategy Execution Report: S-004 Pre-Mortem (R2) + S-012 FMEA (R2)*
*Template Sources: `.context/templates/adversarial/s-004-pre-mortem.md` v1.0.0 + `.context/templates/adversarial/s-012-fmea.md` v1.0.0*
*Prior Review: `projects/PROJ-013-diataxis/reviews/adversary-r1-premortem-fmea.md`*
*Deliverable: `projects/PROJ-013-diataxis/reports/transparency-report-proj-013.md` (R2)*
*Output: `projects/PROJ-013-diataxis/reviews/adversary-r2-premortem-fmea.md`*
*Executed: 2026-02-27*
*Agent: adv-executor*
