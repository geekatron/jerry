# Quality Score Report: Diataxis Audit — Jerry Framework User-Facing Documentation (2026-04-20)

## L0 Executive Summary

**Score:** 0.940/1.00 | **Verdict:** REVISE | **Weakest Dimensions:** Completeness (0.94), Evidence Quality (0.93), Actionability (0.93), Traceability (0.93)
**One-line assessment:** Iteration 3 closed all 9 mechanical blockers from iter-2 (all EV cross-references added, Addresses Gap column added throughout, INSTALLATION.md criterion sweep completed, scope count corrected, P1-5 named) and reached 0.940, leaving a 0.010 gap to the 0.95 C4 threshold — four residual minor issues prevent passage: EV-014 lacking exact glob call notation, P1-5 tutorial scenario still somewhat generic, Internal Consistency and Methodological Rigor are at ceiling; targeted micro-fixes to Completeness, Evidence Quality, Actionability, and Traceability are required.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-040-documentation/reports/diataxis-audit-20260420.md`
- **Deliverable Type:** Analysis (Audit Report)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **User-Specified Threshold:** 0.95 (overrides H-13 default of 0.92)
- **Scored:** 2026-04-17T00:00:00Z
- **Iteration:** 3 of creator-critic-revision cycle (max 6)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.940 |
| **Prior Composite (iter-2)** | 0.911 |
| **Delta vs iter-2** | +0.029 |
| **Prior Composite (iter-1)** | 0.844 |
| **Delta vs iter-1** | +0.096 |
| **Threshold** | 0.95 (user-specified) |
| **Gap to threshold** | 0.010 |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Delta vs Iter-1 | Delta vs Iter-2 | Evidence Summary |
|-----------|--------|-------|----------|-----------------|-----------------|-----------------|
| Completeness | 0.20 | 0.94 | 0.188 | 0.87 → 0.94 (+0.07) | 0.91 → 0.94 (+0.03) | All 9 iter-2 blockers addressed; EV-014 exact glob notation still informal; INSTALLATION.md H-04 partial sweep acknowledged |
| Internal Consistency | 0.20 | 0.95 | 0.190 | 0.82 → 0.95 (+0.13) | 0.92 → 0.95 (+0.03) | 15 vs 16 count corrected throughout; R-02 double-count removed from Doc 15 verdict; all cross-references now consistent |
| Methodological Rigor | 0.20 | 0.95 | 0.190 | 0.84 → 0.95 (+0.11) | 0.93 → 0.95 (+0.02) | INSTALLATION.md full H-01/H-07 table added; Docs 1/2 NA notation added; all 15 docs have complete or explicitly-scoped criterion evaluation |
| Evidence Quality | 0.15 | 0.93 | 0.1395 | 0.82 → 0.93 (+0.11) | 0.90 → 0.93 (+0.03) | EV-026/027/028/029 added with verbatim quotes; EV-024 corrected to lines 74-84; P3-4 citations corrected; EV-014 lacks exact function-call form |
| Actionability | 0.15 | 0.93 | 0.1395 | 0.88 → 0.93 (+0.05) | 0.90 → 0.93 (+0.03) | "Addresses Gap" column added to all P1/P2/P3 tables; P1-5 named "Your First Research Spike"; tutorial scenario still somewhat generic |
| Traceability | 0.10 | 0.93 | 0.093 | 0.83 → 0.93 (+0.10) | 0.89 → 0.93 (+0.04) | All four missing EV cross-references resolved (Doc 12 H-07, Doc 14 H-01/H-07, Doc 15 R-07); Addresses Gap column closes gap→remediation chain; EV-014 notation minor |
| **TOTAL** | **1.00** | | **0.940** | +0.096 | +0.029 | |

**Weighted composite math:**
```
(0.94 × 0.20) = 0.188
(0.95 × 0.20) = 0.190
(0.95 × 0.20) = 0.190
(0.93 × 0.15) = 0.1395
(0.93 × 0.15) = 0.1395
(0.93 × 0.10) = 0.093
──────────────────────
Total           0.940
```

---

## Detailed Dimension Analysis

### Completeness (0.94/1.00)

**Evidence — what iter-3 fixed:**
- All 9 mechanical blockers from iter-2 are confirmed addressed by the Revision Log and verified in the document body:
  - "16 new skills" corrected throughout (Executive Summary, Scope Reconciliation, Coverage Matrix, Delta, trajectory statement)
  - EV-024 updated to cite lines 74-84 with verbatim architecture explanation quote
  - EV-026/027/028/029 added (four new evidence entries)
  - AGENTS.md line count: "703 (verified: 703 lines per wc -l)"
  - INSTALLATION.md: full H-01 through H-07 criterion table added (Document 3)
  - Documents 1 and 2: "Per-criterion evaluation: Documents are multi-quadrant landing pages... H-01 through H-07 and R-01 through R-07 are not separately evaluated" — explicit NA notation
  - Document 15 verdict: "1 Major — R-02 agent count accuracy; 2 Minor — R-04 explanation mixing, R-07 coverage gaps" — duplicate R-02 removed
  - EV cross-references added to Doc 12 H-07 (→EV-026), Doc 14 H-01 (→EV-028), Doc 14 H-07 (→EV-027), Doc 15 R-07 (→EV-029)
  - "Addresses Gap" column added to all P1/P2/P3 remediation tables
  - P1-5 named: "Tutorial: 'Your First Research Spike with /problem-solving'"

**Remaining gaps:**
- EV-014 notation: The entry reads "`skills/*/SKILL.md` glob | 30 SKILL.md files found; none have corresponding `docs/tutorial/`, `docs/how-to/`, or `docs/explanation/` peer documents." The iter-2 recommendation was to cite the exact function-call form ("`Glob('skills/*/SKILL.md')` returning 30 files; `Glob('docs/tutorial/*.md')` returning empty"). The glob path is present but not the function-call invocation form. Minor.
- INSTALLATION.md H-04 sweep: The criterion table correctly marks H-04 FAIL with evidence at lines 4-5, and P2-4 honestly notes "Before implementing, re-read the full document to enumerate all H-04 violations — only lines 4-5 were documented in this audit; additional blocks may exist." This is an acknowledged audit scope limitation, not an error — but it is still present.

**Improvement Path:**
- Update EV-014 to cite the exact glob command form: "`Glob('skills/*/SKILL.md')` returning 30 files; `Glob('docs/tutorial/*.md')` returning empty."
- Either complete a full H-04 scan of INSTALLATION.md or explicitly document the decision to scope out blocks beyond lines 4-5 (current honest note in P2-4 is close but could be elevated to the criterion table row itself).

---

### Internal Consistency (0.95/1.00)

**Evidence — what iter-3 fixed:**
- Count correction: "exactly 16 skills as (N)" — the list in Scope Reconciliation now enumerates 16 items (contract-design through ux-lean-ux); text says "16"; Coverage Matrix has 16 (N) rows. Fully consistent.
- Coverage ratio corrected: 4/14 = 29% at PROJ-015 → 5/30 = 17% current. Both fractions verified: Coverage Matrix shows 14 (P) skills, 30 total; How-To coverage summary shows 5 partial. All figures agree.
- Document 15 verdict: "1 Major — R-02 agent count accuracy; 2 Minor — R-04 explanation mixing, R-07 coverage gaps." The duplicate R-02 Minor entry is removed. Finding count is now internally consistent with the criterion table (R-02 Major, R-04 Minor, R-07 Minor = 3 issues, not 4).
- Trajectory statement corrected from "~27% to ~17%" to "~29% to ~17%" consistently in Scope Reconciliation, Coverage Matrix delta row, and Net trajectory section.
- Coverage Summary: "5 (partial, mixed: problem-solving, orchestration, transcript, plugin-development, bootstrap)" — consistent with Coverage Matrix rows 4, 9, 11, 14, 17.

**Remaining gaps:**
- Document 3 (INSTALLATION.md) criterion table includes two "Marketing voice: title blockquote" and "Marketing voice: 'battle-tested'" rows below the H-01/H-07 block. These are structurally outside the H-01 through H-07 column format but are reasonable additions as sub-findings of H-02. No internal contradiction, but the formatting slightly breaks the criterion table pattern (other tables have 7 criterion rows; Document 3 has 9). This is structural rather than a consistency error.
- No other internal contradictions found in a full document read.

**Improvement Path:**
- Optionally fold the two "Marketing voice" sub-findings into the H-02 FAIL row as evidence (they are already cited in EV-003), removing the table row duplication and standardizing the 7-row format.

---

### Methodological Rigor (0.95/1.00)

**Evidence — what iter-3 fixed:**
- Document 3 (INSTALLATION.md) now has a full H-01 through H-07 criterion table (7 rows) with Results, Evidence, and Status vs PROJ-015 columns. Previously only H-02 and H-04 were evaluated.
- Documents 1 and 2 now have an explicit "Per-criterion evaluation" note confirming that H-01 through H-07 / R-01 through R-07 are inapplicable to multi-quadrant landing pages and that findings are structural only.
- Document 6 (getting-started.md) has explicit T-04 False-Positive Protocol analysis confirming the exception does not apply.
- Git Verification methodology is fully documented with a per-file table (8 files, commit hashes, dates, evidence command noted).
- All 15 documents now have either complete criterion tables (7/7 or full R set) or explicit documented rationale for abbreviated evaluation.

**Remaining gaps:**
- The INSTALLATION.md H-04 partial scope is the one remaining methodological limitation. The criterion table correctly marks H-04 FAIL but the scope note "only lines 4-5 were documented" is in P2-4, not in the Document 3 criterion table row itself. For C4, a cross-reference in the criterion table row would make the limitation maximally visible.
- No other methodology gaps found.

**Improvement Path:**
- In Document 3 H-04 FAIL row, add a note: "(Note: only lines 4-5 audited; full H-04 sweep of remaining document is out of scope for this audit — see P2-4 for re-read recommendation.)"

---

### Evidence Quality (0.93/1.00)

**Evidence — what iter-3 fixed:**
- EV-026: Verbatim Available Agents table content (orch-planner, orch-tracker, orch-synthesizer with full Agent/Role/Primary Output descriptions for each row). High specificity — quotes the actual table content rather than describing it abstractly.
- EV-027: Three reference items from PLUGIN-DEVELOPMENT.md Quick Reference section enumerated verbatim (Development Commands bash block with 5 commands, Settings Locations table with 4 scope/location/purpose rows, Plugin Component Discovery table with 4 component rows). Excellent specificity.
- EV-028: PLUGIN-DEVELOPMENT.md line 1 title quote "Plugin Development Playbook" — parallel structure to EV-018, EV-021, EV-023. Adequate.
- EV-029: AGENTS.md navigation table + skills glob — cites the three missing skills (architecture, bootstrap, ast) and the structural reason (agents defined within SKILL.md, no separate agents/ directory). Adequate.
- EV-024: Corrected from wrong line range to lines 74-84; now contains the verbatim cost-basis calculation paragraph. Excellent.
- P3-4 Evidence column: Updated from "EV-018, EV-020, EV-025" to "EV-026, EV-027" — the misdirected H-01 citation (EV-018) is replaced with the HAP-05 evidence entries that actually support the reference-table-decomposition recommendation.

**Remaining gaps:**
- EV-014: The entry still does not use function-call notation for the glob evidence. Currently: "`skills/*/SKILL.md` glob | 30 SKILL.md files found; none have corresponding `docs/tutorial/`, `docs/how-to/`, or `docs/explanation/` peer documents." The recommended form ("`Glob('skills/*/SKILL.md')` returning 30 files; `Glob('docs/tutorial/*.md')` returning empty") would make the evidence reproducible by a future auditor. Minor.

**Improvement Path:**
- Update EV-014 to cite the exact glob invocations used, making the evidence independently reproducible.

---

### Actionability (0.93/1.00)

**Evidence — what iter-3 fixed:**
- "Addresses Gap" column added to all three remediation tiers (P1 table has 6 rows each with a gap reference; P2 table has 7 rows; P3 table has 6 rows). Each entry links to a specific gap description from the Gap Analysis section by name, not just by implication.
- P1-5 named: "Tutorial: 'Your First Research Spike with /problem-solving' — new user runs ps-researcher on a single library evaluation task, producing artifact at project path. Scope: `jerry session start` → invoke ps-researcher → output verification at `docs/research/`. Covers T-01 through T-08." The tutorial now has a title, a scope boundary, entry/exit conditions, and criterion coverage specification.
- P3-4 Evidence column corrected to EV-026, EV-027 — the implementing agent can now trace to the correct HAP-05 evidence.

**Remaining gaps:**
- P1-5 tutorial scenario: "new user runs ps-researcher on a single library evaluation task" — "library evaluation task" is still somewhat generic. The prior iter-2 recommendation was to name a specific topic (e.g., "evaluating Python async frameworks for a microservice"). The named tutorial title "Your First Research Spike" is helpful, but a writer using only P1-5 must still choose the concrete research subject.
- P2-4 note: "Before implementing, re-read the full document to enumerate all H-04 violations — only lines 4-5 were documented in this audit; additional blocks may exist." This honest scoping note means the implementer faces an unknown quantity of additional work. Not a flaw in the audit — but it reduces actionability precision for this specific item.

**Improvement Path:**
- P1-5: Name a concrete research subject (e.g., "evaluating a Python library for a new project dependency") to give the tutorial writer a zero-decision starting point.

---

### Traceability (0.93/1.00)

**Evidence — what iter-3 fixed:**
- Document 12 H-07 finding table row now cites EV-026 ("See EV-026.") — the HAP-05 pattern for orchestration.md Available Agents table is now traced to evidence.
- Document 14 H-01 finding table row now cites EV-028 ("See EV-028.") — parallel to EV-018, EV-021, EV-023.
- Document 14 H-07 finding table row now cites EV-027 ("See EV-027.") — the HAP-05 pattern for PLUGIN-DEVELOPMENT.md Quick Reference section.
- Document 15 R-07 finding table row now cites EV-029 ("See EV-029.") — the architecture/bootstrap/ast coverage gap.
- "Addresses Gap" column in remediation tables: the full traceability chain is now finding → EV entry → finding table → remediation item → gap analysis item. All four links are now present.
- P3-4 Evidence column corrected: the misdirected EV-018 (H-01 title finding) is replaced with EV-026, EV-027 (HAP-05 mixing evidence).

**Remaining gaps:**
- EV-014 glob notation: minor impact on reproducibility of the evidence for the 30-skills coverage gap claim.
- "Addresses Gap" column links by description string, not by a formal gap ID (e.g., "Gap-P1-A"). Description-based linkage is sufficient but slightly more fragile than ID-based linkage if gap descriptions change. Not a current error, but a structural fragility.

**Improvement Path:**
- Update EV-014 with exact glob function-call form for independent reproducibility.
- Optionally assign short IDs to gap analysis items (e.g., "Gap-P1-Tutorial", "Gap-P1-HowTo") and use those IDs in the "Addresses Gap" column rather than free-text descriptions.

---

## Improvement Recommendations (Priority Ordered for Iter-4)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.93 | 0.95 | Update EV-014: add exact glob function-call form — "`Glob('skills/*/SKILL.md')` returning 30 files; `Glob('docs/tutorial/*.md')` returning empty; `Glob('docs/how-to/*.md')` returning empty" |
| 2 | Traceability | 0.93 | 0.95 | EV-014 update (same as #1 closes this gap too); optionally assign short IDs to Gap Analysis items and use them in "Addresses Gap" column |
| 3 | Actionability | 0.93 | 0.95 | P1-5: replace "single library evaluation task" with a named concrete research subject (e.g., "evaluating a Python concurrency library for a microservice project") |
| 4 | Completeness | 0.94 | 0.96 | In Document 3 H-04 FAIL row, add cross-reference note: "(only lines 4-5 audited; full sweep deferred — see P2-4)"; update EV-014 exact glob notation |
| 5 | Internal Consistency | 0.95 | 0.96 | Optional: fold Document 3 "Marketing voice" sub-rows into H-02 FAIL evidence to standardize 7-row criterion table format across all documents |
| 6 | Methodological Rigor | 0.95 | 0.96 | Add cross-reference in Document 3 H-04 row noting the partial scope limitation (same as #4) |

---

## Trajectory Assessment

**Is convergence to 0.95 achievable in iter-4?**

**Yes — and it is close. The gap is 0.010 from a single iteration of targeted micro-fixes.**

The trajectory over three iterations:
- Iter-1: 0.844
- Iter-2: 0.911 (+0.067)
- Iter-3: 0.940 (+0.029)

The rate of improvement is decelerating as expected when approaching a ceiling — the deliverable is now genuinely strong. The remaining blockers are:

1. **EV-014 exact glob notation** (1 line edit) — closes Evidence Quality and Traceability simultaneously
2. **P1-5 concrete research subject** (1 phrase replacement) — closes Actionability
3. **Document 3 H-04 row cross-reference note** (1 sentence addition) — closes Completeness and Methodological Rigor

These three micro-fixes touch 5 dimensions. If all three are implemented, projected iter-4 composite is approximately:
- Completeness: 0.94 → 0.95
- Internal Consistency: 0.95 (no change needed)
- Methodological Rigor: 0.95 → 0.96
- Evidence Quality: 0.93 → 0.95
- Actionability: 0.93 → 0.95
- Traceability: 0.93 → 0.95

Projected iter-4 composite: (0.95×0.20) + (0.95×0.20) + (0.96×0.20) + (0.95×0.15) + (0.95×0.15) + (0.95×0.10) = 0.190 + 0.190 + 0.192 + 0.1425 + 0.1425 + 0.095 = **0.952**, which meets the 0.95 threshold.

**Plateau risk: Low.** The iter-3 improvements were substantive and mechanical. All remaining blockers are genuinely minor (line-level edits and one phrase replacement). No dimension shows signs of stagnation — each dimension either hit or closely approached its ceiling.

**Caution:** Iter-4 must not introduce new inconsistencies while making these micro-fixes. Particular care needed when editing the Document 3 H-04 row (avoid disrupting the INSTALLATION.md criterion table structure) and when replacing EV-014 content (verify the new glob notation matches the actual commands used during the audit).

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite computed
- [x] Evidence documented for each score — specific document sections, EV entries, and finding-table rows cited per dimension
- [x] Uncertain scores resolved downward — Evidence Quality, Actionability, and Traceability held at 0.93 despite large improvements (EV-014 notation gap is genuinely present and prevents 0.95)
- [x] First-draft calibration considered — this is iteration 3; 0.940 is within expected 0.92-0.95 range for a third-iteration C4 deliverable
- [x] No dimension scored above 0.95 without exceptional evidence — Internal Consistency and Methodological Rigor are at 0.95, both justified: all major blockers for these dimensions are fully resolved with no residual issues found
- [x] Delta cross-check: +0.029 from iter-2 is plausible for closing 9 mechanical blockers while introducing no new issues; the deceleration from +0.067 (iter-2) to +0.029 (iter-3) is expected as the deliverable approaches ceiling quality

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.940
prior_score_iter2: 0.911
prior_score_iter1: 0.844
delta_from_iter2: +0.029
delta_from_iter1: +0.096
threshold: 0.95
weakest_dimensions:
  - name: Evidence Quality
    score: 0.93
  - name: Actionability
    score: 0.93
  - name: Traceability
    score: 0.93
  - name: Completeness
    score: 0.94
critical_findings_count: 0
iteration: 3
improvement_recommendations:
  - "Update EV-014: cite exact glob calls — Glob('skills/*/SKILL.md') returning 30 files; Glob('docs/tutorial/*.md') returning empty; Glob('docs/how-to/*.md') returning empty"
  - "P1-5: replace 'single library evaluation task' with a named concrete research subject"
  - "Document 3 H-04 FAIL row: add note '(only lines 4-5 audited; full sweep deferred — see P2-4)'"
trajectory: "Strongly positive, decelerating normally. Gap is 0.010 from 3 micro-fixes (EV-014, P1-5 topic, Doc 3 H-04 note). PASS achievable in iter-4. Plateau risk: low."
projected_iter4_score: 0.952
```
