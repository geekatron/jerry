# Strategy Execution Report: Chain-of-Verification (Arithmetic Audit)

## Execution Context

- **Strategy:** S-011 (Chain-of-Verification)
- **Template:** `.context/templates/adversarial/s-011-cove.md`
- **Deliverable:** `projects/PROJ-013-diataxis/reports/transparency-report-proj-013.md` (R3)
- **Executed:** 2026-02-27T00:00:00Z
- **Criticality:** C2
- **Iteration:** R3 post-R2 arithmetic corrections
- **Focus:** Exclusive arithmetic audit — every derived number verified against its source numbers

---

## Chain-of-Verification Header

**Strategy:** S-011 Chain-of-Verification
**Deliverable:** `transparency-report-proj-013.md` (R3)
**Criticality:** C2
**Date:** 2026-02-27
**Reviewer:** adv-executor
**H-16 Compliance:** S-003 not applied (H-16 indirect for CoVe; acceptable per template)
**Claims Extracted:** 33 | **Verified:** 30 | **Discrepancies:** 3

---

## Summary

R3 successfully corrected all arithmetic errors flagged in R2: the grand total (189,688,424), worker output (344,964), compaction output (41,233), and average speedup (3.8x) are all arithmetically consistent with their source numbers. Thirty of 33 derived claims verify cleanly. Three discrepancies remain: (1) the tokens-per-line figure (report: 9,839; verified: 9,841 — a rounding artifact); (2) the per-table worker output sum (report's stated 344,457 vs. my calculated 345,457 from the table — a 1,000-token difference in the reconciliation note only, not in the authoritative JSONL-derived figure); (3) a large unexplained gap between the sum of the 37-row Agent Deployment table (85,786,400) and the claimed JSONL-derived worker total (80,297,543) — a 5.49M token delta the report does not acknowledge. Overall recommendation: **REVISE** — the main token totals and quality metrics are sound, but the agent deployment table's total-token column does not sum to the stated worker total, and this gap is not disclosed.

---

## Claim Inventory

Below is the complete set of arithmetic claims extracted from the deliverable, with verification result for each.

| CL-ID | Section | Claim | Verification | Result |
|-------|---------|-------|--------------|--------|
| CL-001 | Combined table | Grand total = 189,688,424 | 102,914,263 + 80,297,543 + 6,476,618 = 189,688,424 | VERIFIED |
| CL-002 | Combined table | Main = 54.3% of grand | 102,914,263 / 189,688,424 = 54.25% → 54.3% | VERIFIED |
| CL-003 | Combined table | Workers = 42.3% of grand | 80,297,543 / 189,688,424 = 42.33% → 42.3% | VERIFIED |
| CL-004 | Combined table | Compaction = 3.4% of grand | 6,476,618 / 189,688,424 = 3.41% → 3.4% | VERIFIED |
| CL-005 | Combined note | 102,914,263 + 80,297,543 + 6,476,618 = 189,688,424 | Computed above | VERIFIED |
| CL-006 | Combined note | Alternative path: 102,914,263 + 86,774,161 = 189,688,424 | 102,914,263 + 86,774,161 = 189,688,424 | VERIFIED |
| CL-007 | Subagent totals | Subagent total = 86,774,161 | 32,247 + 386,197 + 22,393,305 + 63,962,412 = 86,774,161 | VERIFIED |
| CL-008 | Novel output | Worker output = 344,964 = 386,197 − 41,233 | 386,197 − 41,233 = 344,964 | VERIFIED |
| CL-009 | Novel output | Total novel output = 568,255 = 182,058 + 344,964 + 41,233 | 182,058 + 344,964 + 41,233 = 568,255 | VERIFIED |
| CL-010 | Novel output reconciliation | Per-table worker output stated as 344,457 | My row-by-row sum of 37 output_token values = 345,457 | MINOR DISCREPANCY |
| CL-011 | Novel output reconciliation | Per-table compaction output = 40,740 | 4,439+5,207+7,386+6,111+5,554+7+6,507+7+5,522 = 40,740 | VERIFIED |
| CL-012 | Compaction table | Compaction total = 6,476,618 | Row-by-row sum of 9 compaction total_token values | VERIFIED |
| CL-013 | Quality table note | R1 total = 21,351,312 (10 agents) | Sum agents #6-15 from Agent Deployment table | VERIFIED |
| CL-014 | Quality table note | R2 total = 7,428,197 (5 agents) | Sum agents #17-21 from Agent Deployment table | VERIFIED |
| CL-015 | Quality table note | R3 total = 6,562,907 (5 agents) | Sum agents #24-28 from Agent Deployment table | VERIFIED |
| CL-016 | Quality table note | R4 total = 5,093,720 (4 agents) | Sum agents #29-32 from Agent Deployment table | VERIFIED |
| CL-017 | Quality table note | R5 total = 6,499,554 (4 agents) | Sum agents #33-36 from Agent Deployment table | VERIFIED |
| CL-018 | Quality table | Quality total = 46,935,690 | 21,351,312+7,428,197+6,562,907+5,093,720+6,499,554 | VERIFIED |
| CL-019 | Quality table note | Quality = 24.7% of grand | 46,935,690 / 189,688,424 = 24.74% → 24.7% | VERIFIED |
| CL-020 | Quality text | Remediation total = 53.0M tokens (27.9%) | 46,935,690 + 5,341,512 + 735,363 = 53,012,565; 53,012,565/189,688,424 = 27.95% → 27.9% | VERIFIED |
| CL-021 | Model mix | Model mix sum = 189,688,424 | 102,914,263+33,621,129+48,683,647+4,469,385 = 189,688,424 | VERIFIED |
| CL-022 | Model mix % | Opus main 54.3%, Opus sub 17.7%, Sonnet 25.7%, Haiku 2.4% | 54.25%, 17.72%, 25.66%, 2.36% — all round correctly | VERIFIED |
| CL-023 | Parallelization | R1 speedup = 5.0x | 70 min / 14 min = 5.0 | VERIFIED |
| CL-024 | Parallelization | R2 speedup = 3.5x | 45 min / 13 min = 3.46 → 3.5 | VERIFIED |
| CL-025 | Parallelization | R3 speedup = 3.9x | 35 min / 9 min = 3.89 → 3.9 | VERIFIED |
| CL-026 | Parallelization | R4 speedup = 3.3x | 20 min / 6 min = 3.33 → 3.3 | VERIFIED |
| CL-027 | Parallelization | R5 speedup = 3.3x | 20 min / 6 min = 3.33 → 3.3 | VERIFIED |
| CL-028 | Parallelization | Average speedup = 3.8x | (5.0+3.5+3.9+3.3+3.3)/5 = 19.0/5 = 3.8 | VERIFIED |
| CL-029 | Efficiency | Tokens per line = 9,839 | 189,688,424 / 19,275 = 9,841.2 | MINOR DISCREPANCY |
| CL-030 | Efficiency | Novel output per line = 29.5 | 568,255 / 19,275 = 29.48 → 29.5 | VERIFIED |
| CL-031 | Efficiency | Core deliverables ratio = 197.7 | 568,255 / 2,875 = 197.65 → 197.7 | VERIFIED |
| CL-032 | Tool calls | Total tool calls = 1,271 | 494 + 777 = 1,271 | VERIFIED |
| CL-033 | Agent Deployment table | Sum of 37 worker agent total_tokens = (unstated) | My row-by-row sum = 85,786,400 vs claimed JSONL worker total 80,297,543 | MATERIAL DISCREPANCY |

---

## Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| CV-001-r3arith | Minor | Tokens per line stated as 9,839; arithmetic gives 9,841 | Efficiency Analysis |
| CV-002-r3arith | Minor | Per-table worker output reconciliation note states 344,457; row-sum yields 345,457 | Token Consumption |
| CV-003-r3arith | Major | Agent Deployment table 37-row sum (85,786,400) exceeds claimed worker total (80,297,543) by 5,488,857; gap undisclosed | Agent Deployment / Token Consumption |

---

## Detailed Findings

### CV-001-r3arith: Tokens Per Line Off by 2 [Minor]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Efficiency Analysis — Tokens Per Artifact table |
| **Strategy Step** | Step 4 (Consistency Check) |

**Evidence:**
From the report: "**Tokens per line** | **9,839** | Dominated by cache reads"

Source numbers from the same report: Grand total = 189,688,424; Total lines = 19,275.

**Analysis:**

Independent arithmetic: 189,688,424 / 19,275

- 19,275 × 9,841 = 189,685,275
- 19,275 × 9,842 = 189,704,550
- 189,688,424 falls between these two values at 189,688,424 − 189,685,275 = 3,149 above 9,841
- Therefore 189,688,424 / 19,275 = 9,841.2 (rounds to 9,841, not 9,839)

The report states 9,839, which corresponds to: 19,275 × 9,839 = 189,646,725 — a shortfall of 189,688,424 − 189,646,725 = 41,699 tokens. That is a ~0.022% understatement.

**Recommendation:**
Correct "9,839" to "9,841" in the Efficiency Analysis — Tokens Per Artifact table. The footnote logic ("dominated by cache reads") is unaffected.

---

### CV-002-r3arith: Per-Table Worker Output Reconciliation Note Off by 1,000 [Minor]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Token Consumption — "What 189 Million Tokens Actually Means" |
| **Strategy Step** | Step 4 (Consistency Check) |

**Evidence:**
From the report: "Per-agent output tokens in the Agent Deployment tables sum to 385,197 across all 46 agents (344,457 workers + 40,740 compaction) -- a 1,000-token reconciliation gap versus the JSONL-derived 386,197."

The report explicitly checks: 344,457 + 40,740 = 385,197.

**Analysis:**

Independent row-by-row sum of output_tokens for all 37 worker agents from the Agent Deployment table:

```
Agents 1-5:   12,674 + 15,299 + 17,028 + 8,097 + 768    = 53,866
Agents 6-10:  12,729 + 15,214 + 15,690 + 12,430 + 15,446 = 71,509
Agents 11-15: 22,215 + 13,631 + 11,170 + 3,069 + 12,545  = 62,630
Agents 16-20: 14,777 + 1,328 + 15,115 + 16,206 + 1,080   = 48,506
Agents 21-25: 15,815 + 4,638 + 1,710 + 818 + 952          = 23,933
Agents 26-30: 2,837 + 1,529 + 2,591 + 11,072 + 19,286    = 37,315
Agents 31-35: 2,244 + 11,718 + 12,531 + 436 + 3,830      = 30,759
Agents 36-37: 1,002 + 15,937                               = 16,939
Total:                                                       345,457
```

Compaction output sum (independently verified in CL-011): 40,740.

My per-table total = 345,457 + 40,740 = 386,197.

The report states the per-table total is 385,197 (a 1,000-token gap vs. JSONL). My calculation finds the per-table total is 386,197, which exactly matches the JSONL-derived total — meaning the reconciliation gap may not exist if my sum is correct. The discrepancy is in the reconciliation note's stated 344,457 (should be 345,457 per my calculation).

Note: this is a discrepancy in the reconciliation note only. The authoritative JSONL-derived worker output figure (344,964) and total novel output (568,255) are derived independently of this table and verified correct (CL-008, CL-009).

**Recommendation:**
Re-verify the per-table worker output sum (344,457 vs. 345,457). Identify which agent's output token value accounts for the 1,000-token difference. If my sum of 345,457 is correct, revise the reconciliation note to read "(345,457 workers + 40,740 compaction) -- zero reconciliation gap versus the JSONL-derived 386,197" and remove the unexplained 1,000-token gap narrative.

---

### CV-003-r3arith: Agent Deployment Table Totals Do Not Sum to Claimed Worker Total [Major]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Agent Deployment (37-worker table) / Token Consumption Combined table |
| **Strategy Step** | Step 4 (Consistency Check) |

**Evidence:**
From the Combined table: "37 worker agents | 80,297,543 | 42.3%"

The Agent Deployment table presents 37 rows with a "Total Tokens" column for each worker agent.

**Analysis:**

Independent row-by-row sum of the "Total Tokens" column for all 37 worker agents:

```
Agent  1:  2,944,971
Agent  2:  4,469,385
Agent  3:  7,918,201
Agent  4:  5,026,247
Agent  5:    832,694
Agent  6:  2,063,193
Agent  7:  1,756,108
Agent  8:  1,514,652
Agent  9:  2,099,633
Agent 10:  1,914,921
Agent 11:  2,885,867
Agent 12:  3,638,097
Agent 13:  1,684,614
Agent 14:  2,437,336
Agent 15:  1,356,891
Agent 16:  2,387,091
Agent 17:  1,015,685
Agent 18:  1,678,393
Agent 19:  1,221,393
Agent 20:  1,111,561
Agent 21:  2,401,165
Agent 22:  5,341,512
Agent 23:    735,363
Agent 24:    952,613
Agent 25:  1,368,003
Agent 26:  1,405,553
Agent 27:  1,272,710
Agent 28:  1,564,028
Agent 29:  1,206,613
Agent 30:  1,640,649
Agent 31:  1,266,653
Agent 32:    979,805
Agent 33:  1,137,367
Agent 34:    955,178
Agent 35:  3,308,000
Agent 36:  1,099,009
Agent 37:  9,195,246
Running total: 85,786,400
```

Claimed worker total (Combined table): **80,297,543**

Discrepancy: 85,786,400 − 80,297,543 = **5,488,857 tokens** (~6.4%)

The report does not acknowledge this gap anywhere. The grand total arithmetic (CL-001, CL-005) is internally consistent — the issue is that the 37 values in the Agent Deployment table do not sum to the JSONL-derived worker total of 80,297,543. Possible causes:
1. Some rows in the worker table contain incorrect Total Token values (inflated individual agent entries).
2. Some agents in the 37-row table are actually compaction agents that should be excluded, and their tokens are already counted in the 6,476,618 compaction total (which would mean double-counting).
3. The JSONL-derived 80,297,543 figure is incorrect.

The compaction table contains 9 separate agents not in the worker table, so cause (2) appears unlikely but cannot be ruled out without JSONL access. The most likely cause is that some per-agent Total Token values in the table are incorrect.

The report explicitly claims the grand total is verified via two independent paths (CL-005 and CL-006), both of which use the JSONL-derived 80,297,543 — not the table sum. The table-to-total discrepancy undermines reader confidence in the per-agent breakdown even though the aggregate totals are self-consistent.

**Severity justification:** Major — the per-agent token breakdown is a key auditability feature of the transparency report. A 5.49M-token unexplained gap between the table and the claimed total significantly weakens the Evidence Quality dimension. It does not invalidate the grand total (which is independently verified via subagent total path), but it means the agent-level attribution cannot be verified from the table as presented.

**Recommendation:**
1. Re-verify each agent's Total Tokens value against its source JSONL file.
2. Add a "Table total" row at the bottom of the Agent Deployment table showing the column sum.
3. If the table sum does not match the JSONL-derived 80,297,543, identify and correct the specific rows with incorrect values.
4. Add an explicit reconciliation note (analogous to the output token reconciliation note) disclosing any gap and its cause.

---

## Verification Arithmetic: Complete Reference

The following section documents the independent arithmetic for every PASS finding, providing full transparency for the audit.

### Grand Total (Three-Part Sum)
102,914,263 + 80,297,543 = 183,211,806
183,211,806 + 6,476,618 = 189,688,424 **PASS**

### Alternative Grand Total Path
102,914,263 + 86,774,161 = 189,688,424 **PASS**

### Subagent Total (From Categories)
32,247 + 386,197 + 22,393,305 + 63,962,412 = 86,774,161 **PASS**

### Worker Output (Subtraction)
386,197 − 41,233 = 344,964 **PASS**

### Total Novel Output
182,058 + 344,964 + 41,233 = 568,255 **PASS**

### Compaction Row-Level Total Token Sum
607,753 + 676,430 = 1,284,183
1,284,183 + 930,558 = 2,214,741
2,214,741 + 824,408 = 3,039,149
3,039,149 + 693,768 = 3,732,917
3,732,917 + 578,327 = 4,311,244
4,311,244 + 798,041 = 5,109,285
5,109,285 + 494,261 = 5,603,546
5,603,546 + 873,072 = 6,476,618 **PASS**

### Compaction Output Token Sum
4,439 + 5,207 + 7,386 + 6,111 + 5,554 + 7 + 6,507 + 7 + 5,522 = 40,740 **PASS** (matches report's per-table value)

### R1 Quality Total (Agents 6-15)
2,063,193 + 1,756,108 = 3,819,301
3,819,301 + 1,514,652 = 5,333,953
5,333,953 + 2,099,633 = 7,433,586
7,433,586 + 1,914,921 = 9,348,507
9,348,507 + 2,885,867 = 12,234,374
12,234,374 + 3,638,097 = 15,872,471
15,872,471 + 1,684,614 = 17,557,085
17,557,085 + 2,437,336 = 19,994,421
19,994,421 + 1,356,891 = 21,351,312 **PASS**

### R2 Quality Total (Agents 17-21)
1,015,685 + 1,678,393 = 2,694,078
2,694,078 + 1,221,393 = 3,915,471
3,915,471 + 1,111,561 = 5,027,032
5,027,032 + 2,401,165 = 7,428,197 **PASS**

### R3 Quality Total (Agents 24-28)
952,613 + 1,368,003 = 2,320,616
2,320,616 + 1,405,553 = 3,726,169
3,726,169 + 1,272,710 = 4,998,879
4,998,879 + 1,564,028 = 6,562,907 **PASS**

### R4 Quality Total (Agents 29-32)
1,206,613 + 1,640,649 = 2,847,262
2,847,262 + 1,266,653 = 4,113,915
4,113,915 + 979,805 = 5,093,720 **PASS**

### R5 Quality Total (Agents 33-36)
1,137,367 + 955,178 = 2,092,545
2,092,545 + 3,308,000 = 5,400,545
5,400,545 + 1,099,009 = 6,499,554 **PASS**

### Quality Grand Total
21,351,312 + 7,428,197 = 28,779,509
28,779,509 + 6,562,907 = 35,342,416
35,342,416 + 5,093,720 = 40,436,136
40,436,136 + 6,499,554 = 46,935,690 **PASS**

### Quality as % of Grand Total
46,935,690 / 189,688,424 = 0.24742 → 24.7% **PASS**

### Remediation Total and %
5,341,512 + 735,363 = 6,076,875 (agents #22-23)
46,935,690 + 6,076,875 = 53,012,565
53,012,565 / 189,688,424 = 0.27947 → 27.9% **PASS**

### Model Mix Sum
102,914,263 + 33,621,129 = 136,535,392
136,535,392 + 48,683,647 = 185,219,039
185,219,039 + 4,469,385 = 189,688,424 **PASS**

### Average Speedup
(5.0 + 3.5 + 3.9 + 3.3 + 3.3) / 5 = 19.0 / 5 = 3.8 **PASS**

Individual speedup ratios:
- R1: 70 / 14 = 5.0 **PASS**
- R2: 45 / 13 = 3.46 → 3.5 **PASS**
- R3: 35 / 9 = 3.89 → 3.9 **PASS**
- R4: 20 / 6 = 3.33 → 3.3 **PASS**
- R5: 20 / 6 = 3.33 → 3.3 **PASS**

### Novel Output Per Line
568,255 / 19,275 = 29.48 → 29.5 **PASS**

### Core Deliverables Ratio
568,255 / 2,875 = 197.65 → 197.7 **PASS**

### Tokens Per Line (FAIL)
189,688,424 / 19,275:
- 19,275 × 9,841 = 189,685,275
- 189,688,424 − 189,685,275 = 3,149
- 3,149 / 19,275 = 0.163
- Result: 9,841.16 → rounds to **9,841**
- Report states: **9,839** → **FAIL (off by 2)**

### Tool Calls
494 + 777 = 1,271 **PASS**

### Main Context Category Sum
2,159 + 182,058 + 6,271,433 + 96,458,613 = 102,914,263 **PASS**

---

## Recommendations

### Critical (MUST correct before acceptance)
None.

### Major (SHOULD correct)

**CV-003-r3arith:** Agent Deployment table total-token column sum (85,786,400) does not match the claimed JSONL-derived worker total (80,297,543). The 5,488,857-token gap (6.4%) is not disclosed.
- Re-verify each of the 37 agent Total Token values against source JSONL.
- Add a column-sum row to the Agent Deployment table.
- Add a reconciliation note if any gap remains after correction.

### Minor (MAY correct)

**CV-001-r3arith:** Tokens per line in the Efficiency Analysis table: change "9,839" to "9,841". The correct value is 189,688,424 / 19,275 = 9,841.2, which rounds to 9,841.

**CV-002-r3arith:** Reconciliation note for per-table worker output tokens: re-verify whether the correct per-table sum is 344,457 (as stated) or 345,457 (per my row-by-row calculation). If the correct sum is 345,457, remove the "1,000-token reconciliation gap" narrative and revise to note that per-table and JSONL-derived totals match exactly.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | All arithmetic claims are present; no missing derivations |
| Internal Consistency | 0.20 | Negative | CV-003: Agent Deployment table totals do not reconcile with Combined table worker total; the two representations of the same data contradict each other |
| Methodological Rigor | 0.20 | Positive | R3 correctly addressed all R2 arithmetic errors; grand total, quality totals, speedup, and novel output verified correct |
| Evidence Quality | 0.15 | Negative | CV-003: The per-agent token breakdown is not independently verifiable from the table as presented; a 5.49M token unexplained gap weakens auditability |
| Actionability | 0.15 | Neutral | Corrections are specific and achievable (re-verify JSONL values, fix one rounding, re-verify one reconciliation sum) |
| Traceability | 0.10 | Negative | CV-001 and CV-002 introduce minor traceability noise; CV-003 means the agent-level attribution cannot be confirmed from the table alone |

---

## Execution Statistics

- **Total Claims Extracted:** 33
- **VERIFIED:** 30 (90.9%)
- **MINOR DISCREPANCY:** 2 (CV-001, CV-002)
- **MATERIAL DISCREPANCY:** 1 (CV-003)
- **UNVERIFIABLE:** 0
- **Total Findings:** 3
- **Critical:** 0
- **Major:** 1
- **Minor:** 2
- **Protocol Steps Completed:** 5 of 5

---

*Strategy: S-011 Chain-of-Verification*
*Template: `.context/templates/adversarial/s-011-cove.md` v1.0.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Deliverable revision: R3*
*Execution ID: r3arith*
