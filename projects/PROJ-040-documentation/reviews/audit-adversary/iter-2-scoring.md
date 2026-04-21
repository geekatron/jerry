# Quality Score Report: Diataxis Audit — Jerry Framework User-Facing Documentation (2026-04-20)

## L0 Executive Summary

**Score:** 0.911/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Traceability (0.89)
**One-line assessment:** Iteration 2 made substantial, verifiable improvements across all six dimensions — especially Internal Consistency (+0.10) and Methodological Rigor (+0.09) — but three traceability gaps (Document 12 H-07, Document 14 H-01/H-07 missing EV entries; no "Addresses Gap" linkage in remediation table) and two evidence gaps keep the score at 0.911, 0.039 below the 0.95 C4 threshold.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-040-documentation/reports/diataxis-audit-20260420.md`
- **Deliverable Type:** Analysis (Audit Report)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **User-Specified Threshold:** 0.95 (overrides H-13 default of 0.92)
- **Scored:** 2026-04-17T00:00:00Z
- **Iteration:** 2 of creator-critic-revision cycle (max 6)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.911 |
| **Prior Composite (iter-1)** | 0.844 |
| **Delta** | +0.067 |
| **Threshold** | 0.95 (user-specified) |
| **Gap to threshold** | 0.039 |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Delta vs Iter-1 | Evidence Summary |
|-----------|--------|-------|----------|-----------------|-----------------|
| Completeness | 0.20 | 0.91 | 0.182 | 0.87 → 0.91 (+0.04) | Line counts verified for all 15 docs; scope reconciled 15 vs 26 skills; bootstrap counted as 5th partial how-to; P1-5 scenario specified |
| Internal Consistency | 0.20 | 0.92 | 0.184 | 0.82 → 0.92 (+0.10) | EV-012 fully rewritten resolving 82/87/88/89 to verified 88 vs claimed 89 (discrepancy = 1); exec summary updated; scope 15/26 resolved |
| Methodological Rigor | 0.20 | 0.93 | 0.186 | 0.84 → 0.93 (+0.09) | Full H-01 through H-07 for all four playbooks and R-01 through R-07 for AGENTS.md completed; T-04 False-Positive Protocol explicitly addressed |
| Evidence Quality | 0.15 | 0.90 | 0.135 | 0.82 → 0.90 (+0.08) | EV-019 through EV-025 added with verbatim quotes; EV-009 replaced with substantive evidence; EV-012 resolved — PLUGIN-DEVELOPMENT.md H-07 and AGENTS.md R-07 still lack dedicated EV entries |
| Actionability | 0.15 | 0.90 | 0.135 | 0.88 → 0.90 (+0.02) | EV cross-references added to P2-1 through P2-4; P1-5 scenario specified; effort methodology footnote added — "Addresses Gap" linkage and P1-5 topic naming remain open |
| Traceability | 0.10 | 0.89 | 0.089 | 0.83 → 0.89 (+0.06) | EV-019 through EV-025 added for playbook findings; but Document 12 H-07, Document 14 H-01/H-07 finding table rows still cite no EV entry; "Addresses Gap" column not added to remediation table |
| **TOTAL** | **1.00** | | **0.911** | +0.067 | |

**Weighted composite math:**
```
(0.91 × 0.20) = 0.182
(0.92 × 0.20) = 0.184
(0.93 × 0.20) = 0.186
(0.90 × 0.15) = 0.135
(0.90 × 0.15) = 0.135
(0.89 × 0.10) = 0.089
─────────────────────
Total           0.911
```

---

## Detailed Dimension Analysis

### Completeness (0.91/1.00)

**Evidence — what was fixed:**
- All four playbook line counts replaced with verified figures: problem-solving.md = 233, orchestration.md = ~263, transcript.md = ~278, PLUGIN-DEVELOPMENT.md = ~429.
- Scope Reconciliation subsection added to Methodology with explicit count derivation: 15 (N) skills confirmed via Coverage Matrix, "26 new skills" retracted and corrected throughout.
- Coverage Summary bootstrap fix: "5 (partial, mixed: problem-solving, orchestration, transcript, plugin-development, bootstrap)" — previously omitted bootstrap; now consistent with Coverage Matrix row 4.
- P2-4 remediation item now explicitly notes: "only lines 4-5 were documented in this audit; additional blocks may exist" — honest scoping.
- P1-5 scenario improved: "researcher uses ps-researcher to produce a research spike on a chosen topic, starting from `jerry session start` and ending at a persisted artifact in `docs/research/`."

**Remaining gaps:**
- Document 15 (AGENTS.md) line count listed as "~200+" — approximate rather than verified. Minor.
- INSTALLATION.md explanation block enumeration deferred to implementer (P2-4): the audit does not read the full INSTALLATION.md to catalog all H-04 violations, only the two already documented in PROJ-015. This is an acknowledged gap but not resolved.
- README.md and docs/index.md receive structural evaluation rather than full H-01 through H-07 criterion sweeps. The audit justifies this with the multi-quadrant landing page rationale, which is defensible; however, the evidence for the mixed-quadrant classification rests on description rather than systematic criterion application.

**Improvement Path:**
- Verify AGENTS.md line count (replace "~200+" with an exact number from a Read operation).
- Either perform a complete H-04 sweep of INSTALLATION.md or explicitly scope it out with rationale (rather than deferred discovery).

---

### Internal Consistency (0.92/1.00)

**Evidence — what was fixed:**
- EV-012 completely rewritten with a dated, three-number analysis: baseline count (82, 2026-03-09), current filesystem glob result (88, 2026-04-17), per-skill sum from AGENTS.md (89). Discrepancy narrowed to 1 (88 filesystem vs 89 claimed). The 82-to-88 growth (6 agents in 39 days) explained.
- Executive Summary now reads: "88 agent files found via filesystem glob (AGENTS.md per-skill sum claims 89 — discrepancy of 1; see EV-012)" — contested figure is flagged in the summary, not presented as settled.
- Scope: all references to "26 new skills" corrected to "15 new skills"; Scope Reconciliation subsection provides explicit resolution.
- Coverage Summary: 5 partial how-to skills now matches Coverage Matrix (was 4 in iter-1, missing bootstrap).
- All "UNCHANGED" claims now backed by Git verification table with commit hashes and dates.

**Remaining gaps:**
- Document 15 (AGENTS.md) verdict line: "1 Major — R-02 agent count accuracy; 3 Minor — R-04 explanation mixing, R-07 coverage gaps, **R-02 stale verification date**." The verdict statement cites R-02 twice — once as Major (agent count accuracy) and once as Minor (stale verification date). Both issues *are* R-02 (wholly authoritative criterion), so the stale verification date is already subsumed in the Major finding. The duplicate citation is a minor label error that creates the impression of 4 findings when there are 3.
- The Coverage Matrix note on UX sub-skill denominator explains 21 vs 30 denominators — but the Scope Reconciliation section lists 16 items as (N) skills in the text ("contract-design, diataxis, prompt-engineering, test-spec, use-case, user-experience, ux-ai-first-design, ux-atomic-design, ux-behavior-design, ux-design-sprint, ux-heart-metrics, ux-heuristic-eval, ux-inclusive-design, ux-jtbd, ux-kano-model, ux-lean-ux") — that is 16 items, yet the text says "exactly 15 skills as (N)." Counting: contract-design(1), diataxis(2), prompt-engineering(3), test-spec(4), use-case(5), user-experience(6), ux-ai-first-design(7), ux-atomic-design(8), ux-behavior-design(9), ux-design-sprint(10), ux-heart-metrics(11), ux-heuristic-eval(12), ux-inclusive-design(13), ux-jtbd(14), ux-kano-model(15), ux-lean-ux(16). That is **16 items** listed but the text claims 15. The Coverage Matrix (rows 5-6, 12, 16, 18-29) should be counted to adjudicate; the text says the Coverage Matrix (N) entries are authoritative. This is a minor arithmetic issue that partially re-introduces the counting confusion the revision was meant to resolve.

**Improvement Path:**
- Fix Document 15 verdict line: remove the duplicate "R-02 stale verification date" from the Minor list (it is already captured in the Major R-02 finding). Restate as "3 Minor — R-04, R-07 (two issues)."
- Recount the (N) items in the Scope Reconciliation list: if it is 16, change "exactly 15" to "exactly 16"; if one item was listed in error, remove it. The Coverage Matrix is authoritative — use it to confirm the number.

---

### Methodological Rigor (0.93/1.00)

**Evidence — what was fixed:**
- Document 11 (problem-solving.md): Full H-01 through H-07 table added. Results: H-01 FAIL (EV-018), H-02 PASS, H-03 PASS, H-04 FAIL (EV-019), H-05 PASS, H-06 PASS, H-07 FAIL (EV-020). All 7 criteria evaluated with evidence and severity.
- Document 12 (orchestration.md): Full H-01 through H-07 table. Results: H-01 FAIL (EV-021), H-02 PASS, H-03 PASS, H-04 FAIL (EV-022), H-05 PASS, H-06 PASS, H-07 FAIL. All 7 criteria.
- Document 13 (transcript.md): Full H-01 through H-07 table. All 7 criteria with evidence.
- Document 14 (PLUGIN-DEVELOPMENT.md): Full H-01 through H-07 table. Results: H-01 FAIL, H-02 PASS, H-03 PASS, H-04 **PASS** (notable — the Gotchas section is correctly classified as troubleshooting, not teaching), H-05 PASS, H-06 PASS, H-07 FAIL.
- Document 15 (AGENTS.md): Full R-01 through R-07 table. Results: R-01 PASS, R-02 FAIL (Major — agent count), R-03 PASS, R-04 FAIL (Minor — explanation mixing), R-05 PASS, R-06 PASS, R-07 FAIL (Minor — 3 skills not documented).
- T-04 False-Positive Protocol: Document 6 section explicitly states "The getting-started.md branching is plugin-install vs. CLI-clone — not an OS conditional — so the exception does not apply. The T-04 finding stands." This was a specific iter-1 request and is now addressed.
- Git Verification section added with methodology explanation (T1 auditor limitation disclosed; parent workflow Bash execution cited).

**Remaining gaps:**
- README.md and docs/index.md evaluated structurally, not against full criterion sets. The audit states "evaluated structurally" with a rationale note, which is methodologically defensible, but a C4 audit could include even a brief "T-01 through T-04 not applicable; H-01 through H-07 partially applicable" note per document to make the abbreviated evaluation explicit and auditable.
- INSTALLATION.md full criterion re-evaluation is incomplete — only the PROJ-015 findings are re-verified; no new H-01, H-02, H-03, H-05, H-06, H-07 criterion checks performed. Only H-02 and H-04 are evaluated. This is not a new blocker (it was present in iter-1 too) but it remains.

**Improvement Path:**
- For Documents 1 and 2, add a one-line notation per criterion: "H-01 through H-07 evaluated; non-applicable to multi-quadrant landing pages for H-01 (goal-framing) and H-03 (competence assumption); remaining criteria [applied/not applied]."
- For INSTALLATION.md, at minimum check H-01, H-03, H-05, H-06, H-07 and add pass/fail to the criterion table.

---

### Evidence Quality (0.90/1.00)

**Evidence — what was fixed:**
- EV-019: Verbatim quote for problem-solving.md H-04: "For C2+ deliverables (reversible in up to 1 day, touching 3–10 files), the problem-solving skill enforces a minimum 3-iteration creator-critic-revision cycle per H-14 (HARD rule). You will observe this cycle when: An agent produces a deliverable, then another pass critiques it and provides a quality score — the agent revises and re-scores, repeating until the quality threshold is met." Full sentence, strong specificity.
- EV-020: problem-solving.md H-07 reference table — description of the 9-row Agent Reference table with column names. Adequate specificity.
- EV-021: orchestration.md H-01 — title quote.
- EV-022: orchestration.md H-04 — verbatim from Workflow Patterns section: "Two or more pipelines run in parallel. At synchronization barriers, each pipeline shares its findings with the other (cross-pollination). Work after the barrier incorporates insights from both pipelines." Excellent.
- EV-023: transcript.md H-01 — title.
- EV-024: transcript.md H-04 — verbatim blockquote: "The transcript skill uses a hybrid Python+LLM architecture: the Python CLI parser runs automatically for VTT files (~1,250x cheaper than LLM parsing), while SRT and plain text files use LLM-based parsing directly." Excellent.
- EV-025: transcript.md H-07 — domain contexts and input formats tables described with line ranges.
- EV-009: Replaced "Empty" with substantive evidence: scope statement line 5 verbatim quote and E-06 rationale.
- EV-012: Fully rewritten with dated baseline, current count, and net discrepancy analysis.

**Remaining gaps:**
- Document 12 (orchestration.md) H-07 finding: the finding table entry notes "HAP-05 pattern" without citing an EV entry. There is no EV entry for orchestration.md's H-07 (Available Agents table at lines 156-165). EV-022 covers H-04; no EV covers H-07 for this document.
- Document 14 (PLUGIN-DEVELOPMENT.md) H-07 finding: the finding table notes "HAP-05 pattern" without citing an EV entry. EV-025 covers transcript.md H-07; PLUGIN-DEVELOPMENT.md H-07 (Quick Reference section lines 378-419) has no dedicated EV entry with a verbatim quote.
- Document 14 H-01 finding: no EV entry cited (the finding table row for H-01 does not reference an EV-NNN).
- Document 15 R-07 finding (coverage gap for architecture, bootstrap, ast skills): no EV entry. The finding cites specific agents and skill names but no evidence log entry.
- Remediation table P3-4 cites "EV-018, EV-020, EV-025" — EV-018 is the problem-solving playbook H-01 title finding, not an HAP-05 mixing pattern reference. The citation is technically accurate (the title failure is documented) but the connection to P3-4 (decompose embedded reference tables) is indirect.

**Improvement Path:**
- Add EV-026: orchestration.md lines 156-165 — verbatim description or quote from the Available Agents table header, confirming it is a reference lookup table embedded in how-to context.
- Add EV-027: PLUGIN-DEVELOPMENT.md lines 378-419 — verbatim description of the Quick Reference section confirming reference content classification.
- Add EV entry for Document 14 H-01 (title quote: "Plugin Development Playbook") — currently implicit in EV-018 by analogy but should have its own entry for Document 14.
- Add EV entry for AGENTS.md R-07: cite the three missing skills (architecture, bootstrap, ast) with the glob evidence that they have SKILL.md files but no AGENTS.md entry.

---

### Actionability (0.90/1.00)

**Evidence — what was fixed:**
- P2-1 Evidence column: "EV-004, EV-005, EV-006" — context-architecture extraction targets now have EV cross-references.
- P2-2 Evidence column: "EV-003" — hooks-architecture source lines identified.
- P2-3 Evidence column: "EV-004, EV-005" — BOOTSTRAP.md sections identified.
- P2-4 Evidence column: "EV-003" plus honest note: "Before implementing, re-read the full document to enumerate all H-04 violations — only lines 4-5 were documented in this audit; additional blocks may exist."
- P1-5 scenario: "covering a concrete end-to-end scenario: researcher uses ps-researcher to produce a research spike on a chosen topic, starting from `jerry session start` and ending at a persisted artifact in `docs/research/`." Substantially more actionable than iter-1.
- Effort estimate methodology footnote added: expert-vs-novice calibration noted (2-3x for inexperienced practitioner).

**Remaining gaps:**
- P1-5 still specifies "a chosen topic" without naming it. The scenario describes the user journey but leaves the topic open. Naming a concrete topic (e.g., "evaluating Python async frameworks for a new microservice") would remove the last decision step before a writer can begin. This is minor — the diataxis-tutorial agent can select a topic — but it is the one remaining specificity gap.
- "Addresses Gap" linkage: the remediation table does not cross-reference gap analysis items. Iter-1 recommended adding a column or note like "Addresses Gap: Zero tutorial documents (P1)" to close the traceability chain from finding → gap → remediation. Not added.
- P3-4 remediation item (decompose playbook reference tables) cites EV-018, EV-020, EV-025 — EV-018 is the H-01 title finding, not the HAP-05 mixing evidence. The EV cross-references for P3-4 should be the HAP-05 entries, not the H-01 entries. Once EV-026 and EV-027 are added (see Evidence Quality improvement path), P3-4 should update its Evidence column.

**Improvement Path:**
- P1-5: name the tutorial topic (e.g., "researching Python async frameworks for a microservice").
- Add "Addresses Gap" notation to P1-P3 remediation items linking each to its source gap in the Gap Analysis section (P1-5 → "Zero tutorial documents"; P2-1 → "Missing docs/explanation/context-architecture.md"; etc.).
- P3-4 Evidence: replace "EV-018" with EV-026 (orchestration.md H-07) and EV-027 (PLUGIN-DEVELOPMENT.md H-07) once those entries are created.

---

### Traceability (0.89/1.00)

**Evidence — what was fixed:**
- EV-019 through EV-025 added, extending the evidence log from 18 to 25 entries.
- All playbook H-01 and H-04 finding table rows in Documents 11-13 now cite EV entries.
- Document 11: H-01 → EV-018; H-04 → EV-019; H-07 → EV-020. Full EV coverage.
- Document 12: H-01 → EV-021; H-04 → EV-022; H-07 → no EV cited.
- Document 13: H-01 → EV-023; H-04 → EV-024; H-07 → EV-025.
- Document 14: H-01 → no EV; H-07 → no EV.
- Document 15: R-02 → EV-012; R-04 → EV-013; R-07 → no EV.

**Remaining gaps:**
- Document 12 H-07 finding table row has no EV cross-reference (HAP-05 pattern noted but no EV-NNN cited).
- Document 14 H-01 and H-07 finding table rows have no EV cross-references.
- Document 15 R-07 has no EV cross-reference.
- "Addresses Gap" column: remediation items are not linked back to their source gap analysis items. The traceability chain runs: finding → EV entry → remediation item, but the gap analysis → remediation link is implicit, not explicit.
- Remediation table for P3-4 cites EV-018 (H-01 title finding) rather than the HAP-05 mixing evidence entries — traceability from remediation to evidence is partially misdirected.
- EV-014 ("30 SKILL.md files found; none have corresponding docs/tutorial/...") still notes glob result without specifying the exact glob command. This was flagged in iter-1 and not resolved.

**Improvement Path:**
- Add EV cross-references to Document 12 H-07, Document 14 H-01 and H-07, and Document 15 R-07 finding table rows (using existing EV entries where applicable; new EV-026/EV-027 once added).
- Add "Addresses Gap" notation to the remediation table (either a column or a parenthetical in each row).
- Update EV-014 to cite the exact glob command used (e.g., "`Glob('skills/*/SKILL.md')` returning 30 files; `Glob('docs/tutorial/*.md')` returning empty").
- Correct P3-4 Evidence column once EV-026/EV-027 are added.

---

## Improvement Recommendations (Priority Ordered for Iter-3)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Traceability | 0.89 | 0.93 | Add EV cross-references to Document 12 H-07, Document 14 H-01/H-07, Document 15 R-07 finding table rows; add "Addresses Gap" notation to remediation table; update EV-014 with exact glob command |
| 2 | Evidence Quality | 0.90 | 0.94 | Add EV-026 (orchestration.md H-07 verbatim) and EV-027 (PLUGIN-DEVELOPMENT.md H-07 verbatim); add EV for Document 14 H-01 title; add EV for AGENTS.md R-07 (architecture/bootstrap/ast not in AGENTS.md) |
| 3 | Internal Consistency | 0.92 | 0.95 | Fix Document 15 verdict line (remove duplicate R-02 Minor citation); recount (N) skills in Scope Reconciliation list — text claims 15 but lists 16 items (contract-design through ux-lean-ux) |
| 4 | Completeness | 0.91 | 0.94 | Verify AGENTS.md line count (replace "~200+"); either complete H-04 sweep of INSTALLATION.md or explicitly scope it out with rationale |
| 5 | Methodological Rigor | 0.93 | 0.96 | Add brief per-criterion notes for Documents 1 and 2 (multi-quadrant — note which criteria are applicable/not applicable); add H-01/H-03/H-05/H-06/H-07 checks for INSTALLATION.md |
| 6 | Actionability | 0.90 | 0.94 | Name a concrete topic in P1-5; add "Addresses Gap" linkage in remediation table; fix P3-4 Evidence column to reference HAP-05 EV entries once created |

---

## Trajectory Assessment

**Is convergence toward 0.95 achievable in future iterations?**

**Yes — trajectory is strongly positive and the remaining blockers are mechanical.**

The +0.067 improvement from iter-1 to iter-2 (0.844 → 0.911) demonstrates that the auditor is engaging substantively with each blocker. The gap from 0.911 to 0.95 is 0.039, which requires an average lift of ~0.026 per dimension. This is achievable because:

1. The remaining blockers are all **mechanical** (add EV entries, fix a counting error, add "Addresses Gap" notation, verify a line count). None require rethinking the audit's methodology, scope, or conclusions.
2. The three highest-weighted dimensions (Completeness, Internal Consistency, Methodological Rigor — total weight 0.60) are already at 0.91/0.92/0.93. A single-point improvement in each to 0.94/0.95/0.95 would add ~0.021 to the composite.
3. The remaining EV gaps (4 missing entries) are small, targeted additions that can be verified immediately by reading the specific file lines cited.

**Risk:** The Scope Reconciliation (N) skills count (text claims 15, list contains 16) is a consistency issue that could indicate the Coverage Matrix also has an error. If the Coverage Matrix has 16 (N) rows rather than 15, the delta figures (15 skills added → coverage declined from 27% to 17%) need recomputation. This should be verified before iter-3.

**Projected iter-3 score:** 0.93-0.96 if all six recommendations above are addressed. PASS is achievable in iter-3.

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite computed
- [x] Evidence documented for each score — specific file:line references cited per dimension
- [x] Uncertain scores resolved downward (Internal Consistency held to 0.92 despite large improvement, due to residual (N) count discrepancy; Traceability held to 0.89 despite 7 new EV entries, due to 4 finding-table rows still missing EV cross-references)
- [x] First-draft calibration considered — this is iteration 2; 0.911 is within expected 0.85-0.92 range for second drafts with substantial improvements
- [x] No dimension scored above 0.95 without exceptional evidence — highest dimension is 0.93 (Methodological Rigor) which is warranted given the complete criterion sweep added
- [x] Improvements verified specifically: EV-019 through EV-025 text confirmed by reading the Evidence Log section; Scope Reconciliation text read directly for the (N) count discrepancy; Document 12, 13, 14, 15 finding tables read to confirm which rows have/lack EV cross-references

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.911
prior_score: 0.844
delta: +0.067
threshold: 0.95
weakest_dimension: Traceability
weakest_score: 0.89
critical_findings_count: 0
iteration: 2
improvement_recommendations:
  - "Add EV cross-references to Document 12 H-07, Document 14 H-01/H-07, Document 15 R-07 finding table rows"
  - "Add EV-026 (orchestration.md H-07 verbatim) and EV-027 (PLUGIN-DEVELOPMENT.md H-07 verbatim)"
  - "Fix Document 15 verdict line: remove duplicate R-02 Minor citation"
  - "Recount (N) skills in Scope Reconciliation list — text claims 15 but enumerates 16 items; adjudicate via Coverage Matrix"
  - "Add Addresses Gap notation to remediation table (each P1/P2/P3 item → source gap)"
  - "Verify AGENTS.md line count (replace ~200+ with exact count)"
  - "Add EV for Document 14 H-01 title and AGENTS.md R-07 coverage gap"
trajectory: "Strongly positive. Remaining blockers are mechanical. PASS achievable in iter-3 if all 6 recommendations addressed."
```
