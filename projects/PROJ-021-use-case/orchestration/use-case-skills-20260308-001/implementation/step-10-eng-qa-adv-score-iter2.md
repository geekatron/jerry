# Quality Score Report: Security QA Review -- /test-spec Skill (Iter-2)

## L0 Executive Summary

**Score:** 0.944/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Traceability (0.93)
**One-line assessment:** All three targeted iter-1 gaps are confirmed fixed (L0 finding count, FIND-QA-003 Gherkin scaffold, distribution math observation), pushing the composite from 0.904 to 0.944, but two secondary gaps from iter-1 remain unaddressed -- the "minimum 7 scenarios" architecture citation and the non-standard L2 recommendations format -- and together prevent the 0.95 C4 threshold from being crossed by 0.006.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/implementation/step-10-eng-qa-review.md`
- **Deliverable Type:** Security QA Review (for /test-spec skill)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge) + all 10 adversarial strategies (S-003, S-013, S-007, S-002, S-004, S-010, S-012, S-011, S-001)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-09T00:00:00Z
- **Iteration:** 2 (G-10-ADV-4 iter-2)
- **Threshold:** 0.95 (C-008 user override, not standard 0.92)
- **Prior Score:** 0.904 (iter-1) -- delta: +0.040

### Iter-1 Gap Verification

| Gap (iter-1 priority) | Fix Required | Fix Applied | Status |
|-----------------------|-------------|-------------|--------|
| P1: L0 summary lists 4 findings, body has 5 (FIND-QA-005 absent from L0) | Update L0 count to "Five findings"; add FIND-QA-005 to findings table | Lines 32 ("Five findings are raised"), lines 47-53 (FIND-QA-005 added to table) | CONFIRMED FIXED |
| P2: FIND-QA-003 lacks Gherkin template for G-008 | Add complete Gherkin scaffold (Given/When/Then covering deviation + rejoin resumption) | Lines 413-437: 16-line scaffold with Given (preconditions + rejoin:3 extension), When (invocation), Then (7 assertions including rejoin point + continuation steps) | CONFIRMED FIXED |
| P3: Distribution inconsistency (2+3+4=9 vs 8 scenarios) not flagged | Flag as inline observation or new FIND-QA-006 | Lines 84-86: verbatim claim followed by bordered QA observation block noting 9-vs-8 discrepancy, percentage correction, and LOW severity label | CONFIRMED FIXED |
| P4: "Minimum 7 scenarios" architecture citation missing | Add specific file path + section for architecture requirement | NOT addressed in v1.1.0 -- H-20-01 row still reads "(8 scenarios)" with no architecture source citation | NOT FIXED |
| P5: L2 recommendations non-standard format | Reformat as priority-ordered `| Priority | Dimension | Current | Target | Recommendation |` table | NOT addressed -- L2 still uses separate Coverage ROI, Coverage Gaps, and Regression Suite tables | NOT FIXED |

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.944 |
| **Threshold** | 0.95 (H-13 + C-008 override) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | Yes -- 10 strategies applied (S-001 through S-014 selected set) |
| **Critical Findings (adv-executor)** | 0 |
| **Gap to Threshold** | 0.006 |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.95 | 0.190 | All 8 assessment areas present; FIND-QA-003 Gherkin scaffold added; distribution observation added; P4/P5 non-critical |
| Internal Consistency | 0.20 | 0.96 | 0.192 | L0 now accurately states "Five findings"; distribution inconsistency explicitly flagged; no remaining internal contradictions detected |
| Methodological Rigor | 0.20 | 0.95 | 0.190 | Template consistency restored (all 3 MEDIUM findings now have Gherkin scaffolds); "min 7" citation still lacks source file -- minor gap |
| Evidence Quality | 0.15 | 0.93 | 0.140 | "Minimum 7 scenarios" architecture source still unanchored; all other claims independently verifiable |
| Actionability | 0.15 | 0.93 | 0.140 | G-008 scaffold is actionable and copy-paste ready; L2 format still non-standard (separate tables vs priority-ordered table) |
| Traceability | 0.10 | 0.93 | 0.093 | "Min 7" normative claim still lacks specific file/section; coverage matrix E-001 gap still admitted; otherwise strong |
| **TOTAL** | **1.00** | | **0.944** | |

**Composite calculation:**
(0.95 × 0.20) + (0.96 × 0.20) + (0.95 × 0.20) + (0.93 × 0.15) + (0.93 × 0.15) + (0.93 × 0.10)
= 0.190 + 0.192 + 0.190 + 0.140 + 0.140 + 0.093
= **0.944**

---

## Detailed Dimension Analysis

### Completeness (0.95/1.00)

**Evidence:**
The review addresses all eight assessment areas. The three targeted completeness fixes from iter-1 are fully applied: (1) FIND-QA-005 appears in the L0 findings summary table at lines 47-53; (2) FIND-QA-003 Recommended Fix now contains a full 16-line Gherkin scaffold (lines 413-437) with Given/When/Then structure covering the rejection precondition, the deviation handling When, and seven Then clauses including the rejoin assertion and continuation steps; (3) the coverage distribution paragraph (lines 84-86) now includes an inline QA observation block that correctly identifies the 9-vs-8 discrepancy and provides the mathematically correct percentages (25%/37.5%/50%). The document is structurally complete: L0/L1/L2 present, S-010 self-review present, revision history present.

**Gaps:**
- The H-20-01 acceptance criterion ("Minimum 7 scenarios present in Given/When/Then format") cites "(8 scenarios)" as evidence but does not identify the architecture document source for the minimum-7 requirement. For a C4 deliverable, every normative threshold should be traceable. This was Priority 4 in iter-1 and remains unaddressed. The gap is minor (the 7-minimum is a well-known H-20 requirement) but at the 0.95 threshold level, unanchored normative claims are a completeness gap.
- The scope table for RULE-OT-02 (success outcome) is explicitly noted as out of scope with rationale, but FIND-QA-003 Recommended Fix asks this be updated -- the body of FIND-QA-003 (line 438) says "Additionally, update the scope table to explicitly include or exclude RULE-OT-02 (success outcome)..." but this update is not present in the revised document. The scope table itself has not been updated.

**Improvement Path:**
Add specific architecture document reference for "minimum 7" threshold (e.g., `step-10-test-spec-architecture.md Section 7`). In FIND-QA-003, either remove the scope-table update instruction (since it cannot be actioned in this document -- the scope table is in BEHAVIOR_TESTS.md) or reframe it as a separate action item distinct from the G-008 scaffold.

---

### Internal Consistency (0.96/1.00)

**Evidence:**
The L0 summary text at line 32 now reads "Five findings are raised, none CRITICAL, all addressable without architectural change." The L0 findings table (lines 47-53) lists all five findings including FIND-QA-005 ("Sample output has validation steps in When block"). The body contains five fully documented findings. The Coverage ROI table in L2 (lines 526-534) lists all five findings. The S-010 self-review at line 580 states "all 5 findings cite exact file names." All three occurrence points are now aligned. The distribution inconsistency is explicitly flagged as an inline observation with the correct math (2+3+4=9; correct 8-scenario percentages are 25%/37.5%/50%). The revision history accurately describes the three changes applied.

**Gaps:**
- FIND-QA-003 Recommended Fix (lines 411-438) includes the instruction "Additionally, update the scope table to explicitly include or exclude RULE-OT-02 (success outcome) with documented rationale to match the pattern established for alternative_flows." This instruction refers to a change in BEHAVIOR_TESTS.md, not in this document, so it is a valid recommendation. However, the Coverage Gaps table in L2 (line 543) notes "RULE-C4-01 (alternative flows) scenario absent -- LOW -- Structurally identical to extension mapping" which is correctly classified. No internal contradiction.
- One micro-inconsistency: the S-010 self-review (line 584) states "PASS -- no CRITICAL (no executable code, no auth surface), 3 MEDIUM (behavioral gaps), 2 LOW" -- this count (3 MEDIUM + 2 LOW = 5 total) is now consistent with the corrected finding count. Previously it was inconsistent. CONFIRMED FIXED.

**Improvement Path:**
Internal consistency is strong after iter-2 fixes. No high-priority inconsistencies remain.

---

### Methodological Rigor (0.95/1.00)

**Evidence:**
The finding-template consistency issue (iter-1 Priority 2) is resolved. FIND-QA-001 provides G-006 template (18 lines), FIND-QA-002 provides G-007 template (14 lines), FIND-QA-003 now provides G-008 template (16 lines). All three MEDIUM findings apply the same "Recommended Fix = complete Gherkin scaffold" methodology. The OWASP category framework is applied consistently. The Clark rule coverage matrix is methodologically sound. The H-20 and H-34 compliance tables use binary PASS/FAIL with specific evidence. The injection attack surface analysis (lines 141-143), path traversal assessment (lines 143-144), constitutional compliance table, and SESS N/A rationale are all methodologically appropriate for this skill's threat model.

**Gaps:**
- The "Minimum 7 scenarios" acceptance criterion (H-20-01, line 261) lacks a source citation in the evidence column. The criterion is stated as given, without citing the architecture document that establishes this minimum. For a methodologically rigorous document, normative thresholds should cite their source. This was identified in iter-1 (Priority 4) and remains unaddressed.
- The G-008 scaffold in FIND-QA-003 is technically correct but uses a slightly different table style than G-006 and G-007. G-006 and G-007 use a two-column `| Field | Value |` Given table; G-008 also uses this format but includes multi-value fields (`| extensions | 1 entry with outcome "rejoin:3" |`). This is not a defect but is a mild structural variation in the template pattern.

**Improvement Path:**
Add architecture document source citation to H-20-01 criterion row. The methodology otherwise meets the 0.95 threshold criteria well.

---

### Evidence Quality (0.93/1.00)

**Evidence:**
All five findings continue to provide multi-point citations verified in iter-1: FIND-QA-001 cites RULE-IV-02 from clark-transformation-rules.md + tspec-generator.md guardrails + BEHAVIOR_TESTS.md coverage matrix. FIND-QA-002 follows the same pattern. FIND-QA-003 quotes the specific distinguishing RULE-OT-03 language ("Do NOT treat rejoin outcomes identically to success outcomes"). FIND-QA-004 cites schema lines 89-97 and step-9 precedent RISK-04. FIND-QA-005 cites sample-test-specification.md lines 44-52 and BEHAVIOR_TESTS.md G-003 assertions 208-210. The distribution QA observation (lines 84-86) provides the mathematical evidence directly: "The scenario counts (2 happy path + 3 negative + 4 edge cases) sum to 9, but the file contains 8 scenarios" with correct percentage derivation. The H-34 verification evidence cites specific YAML field names for both agents.

**Gaps:**
- "Minimum 7 scenarios" normative claim remains unanchored to a specific file and section. This is the sole remaining unanchored claim. For a C4 deliverable aiming for 0.95, one unanchored normative claim is an evidence quality gap that cannot be overlooked.
- The G-008 scaffold was not independently verified against the actual UC-LIB-003 artifact (which is a fictional artifact created for the scenario, so verification against a real file is not possible -- this is acceptable). The scenario is internally consistent with RULE-OT-03.

**Improvement Path:**
Add `step-10-test-spec-architecture.md, Section [N], Quality Strategy` as the specific source for the "minimum 7 scenarios" requirement. This is a single-line change to the H-20-01 evidence cell.

---

### Actionability (0.93/1.00)

**Evidence:**
FIND-QA-001 provides G-006 (copy-paste Gherkin). FIND-QA-002 provides G-007 (copy-paste Gherkin). FIND-QA-003 now provides G-008 (copy-paste Gherkin) at lines 413-437. The G-008 scaffold specifies: a named scenario title, a Given table with 4 fields, extension condition and step specification, output path, a When invocation step, and 7 Then/And clauses that cover feature file existence, scenario title, Given block content, When block deviation handling, rejoin assertion, continuation steps, and coverage reporting. FIND-QA-004 provides the specific `$comment` JSON string. FIND-QA-005 provides the corrected Gherkin block. All five findings are now actionable with specific fixes.

**Gaps:**
- The L2 section presents its recommendations in three separate tables (Coverage ROI estimate, Coverage Gaps and Risk Implications, Regression Suite Maintenance) rather than the priority-ordered `| Priority | Dimension | Current | Target | Recommendation |` format specified in the adv-scorer output spec. This was Priority 5 in iter-1 and remains unaddressed. The information is present but requires more effort to extract in priority order. This is a minor format deviation since a QA review document is not the same artifact type as a score report, and the three tables provide equivalent information organized by dimension rather than priority.
- The FIND-QA-003 recommendation (line 438) to "update the scope table to explicitly include or exclude RULE-OT-02" is an action on BEHAVIOR_TESTS.md, not on this document. While the recommendation is valid, it creates an implicit open action item not clearly enumerated alongside the five documented findings.

**Improvement Path:**
The L2 format deviation is low impact given the document type. Adding a single consolidated Priority table at the top of L2 would close this gap. The RULE-OT-02 scope table action should either be documented as FIND-QA-006 (LOW) or labeled as a separate action item distinct from the main findings.

---

### Traceability (0.93/1.00)

**Evidence:**
The document header cites all three upstream inputs with version and pass score. The footer (lines 603-604) lists 8 key files examined. Each of the five findings provides minimum two traceable citations. The step-9 QA review is cited as structural and pattern precedent. The distribution QA observation is traceable to the BEHAVIOR_TESTS.md Overview section claim. The S-010 self-review confirms P-002 compliance with explicit output file path. Clark rule IDs throughout are traceable to clark-transformation-rules.md (verified in iter-1). The revision history (lines 593-598) provides complete version traceability with change descriptions.

**Gaps:**
- "Minimum 7 scenario requirement from the architecture document" (H-20-01) remains the only normative claim without a specific traceable source. The requirement appears in three places in this document (L0 scenario count table at line 43, H-20-01 acceptance criterion at line 261) with no citation to a specific architecture document section. This is the same gap as iter-1 Priority 4.
- Coverage Matrix E-001 continues to note "Schema validation not explicitly verified" -- this is an honest admission and is minor, but means one coverage matrix row remains unverified as noted in iter-1.

**Improvement Path:**
Cite the specific architecture document section for the minimum-7 threshold. If the section cannot be identified without rereading the architecture document, note it explicitly as an unresolved traceability gap rather than presenting the threshold as given.

---

## Adversarial Strategy Findings

### S-003 (Steelman Applied First per H-16)

The strongest interpretation of iter-2: This is a genuinely strong QA review that correctly prioritized its three targeted fixes. The L0 fix (Priority 1) eliminates the highest-impact consistency defect. The G-008 scaffold (Priority 2) is technically correct and more detailed than G-006/G-007 -- it includes 7 Then/And clauses vs 3-4 for the simpler input validation scenarios, appropriately reflecting the greater complexity of the rejoin outcome type. The distribution QA observation (Priority 3) is well-placed as an inline note rather than a separate finding, which is proportionate to its LOW severity and avoids inflating the finding count. The revision history accurately describes all three changes with sufficient specificity for traceability.

### S-002 (Devil's Advocate)

Counter-arguments:
1. The G-008 scaffold (lines 413-437) uses fictional UC-LIB-003 with `| basic_flow | 4 typed steps (step 1-4) |` as an abstract field value. G-006 and G-007 use similarly abstract shorthand (`| basic_flow | 5 typed steps |`, `| extensions | [] (empty array) |`). This is consistent but means none of the scaffolds are runnable without further elaboration. This is acceptable for a BDD design document but noted for completeness.
2. The QA observation for distribution inconsistency (lines 84-86) is inline as a blockquote, not as a formal finding. This is correct per the "LOW severity, documentation only, no functional impact" characterization. However, the inline observation is not cross-referenced in the L0 findings summary (it is not FIND-QA-006), so a reviewer scanning only the findings section would not encounter it. The observation is visible only in the L1 scenario coverage section.
3. The iter-2 S-010 self-review (lines 574-590) does not include an item verifying that iter-1 gaps were addressed. For a revision document, a self-review item confirming "all prior scorer gaps addressed: [P1 FIXED, P2 FIXED, P3 FIXED, P4 NOT ADDRESSED, P5 NOT ADDRESSED]" would be expected at C4 quality level.

### S-013 (Inversion)

What must be true for the review to reach 0.95? Every normative threshold must be traceable to a source. Currently "minimum 7 scenarios" is stated without source. The inversion reveals: the smallest remaining gap (single-line architecture citation) is the only thing preventing threshold attainment on the Evidence Quality and Traceability dimensions. The cost of the fix is approximately 15 characters in one table cell.

### S-007 (Constitutional AI)

P-003: QA review makes no recursive delegation. P-020: Findings are presented as findings; user retains full authority over which to action. P-022: The L0 summary now accurately states "Five findings are raised" -- the iter-1 P-022 concern is resolved. No remaining deception issues. The distribution observation is honest about its source (verbatim from BEHAVIOR_TESTS.md Overview) and the mathematical derivation is transparent.

### S-004 (Pre-Mortem)

If this review is accepted without iter-3 revision, the most likely failure mode is: a developer actioning the findings cites "minimum 7 scenarios" as an H-20 requirement when challenged, and cannot point to the architecture document to prove the threshold. In a C4 context, the inability to source a normative claim is an audit finding. The distribution observation is in the body text but not in the findings table, so a developer using only the findings section for their implementation checklist would not see it. Neither failure mode is severe, but both are avoidable.

### S-012 (FMEA)

| Risk | Severity | Probability | Detection | RPN |
|------|----------|-------------|-----------|-----|
| "min 7" accepted without architecture citation -> audit gap | LOW | LOW | MEDIUM (visible to careful reviewer) | LOW |
| Distribution observation not acted upon (not a named finding) | LOW | MEDIUM | LOW (in body text only) | MEDIUM |
| L2 format deviation -> harder to extract priority-ordered actions | LOW | LOW | LOW (requires knowing the spec format) | LOW |
| G-008 scaffold using abstract field values (not runnable as-is) | LOW | LOW | MEDIUM (consistent with G-006/G-007 style) | LOW |

### S-011 (Chain-of-Verification)

Verified against v1.1.0:
- "Five findings are raised, none CRITICAL" (L0 line 32) -- CONSISTENT with body (5 findings documented)
- FIND-QA-005 in L0 findings table (lines 47-53) -- CONFIRMED PRESENT
- G-008 Gherkin scaffold present (lines 413-437) -- CONFIRMED, 16 lines with 7 Then clauses
- Distribution QA observation (lines 84-86) -- CONFIRMED, identifies 2+3+4=9 vs 8-scenario discrepancy
- S-010 severity count "3 MEDIUM, 2 LOW" (line 584) -- CONSISTENT with 5 findings (FIND-QA-001/-002/-003 MEDIUM; FIND-QA-004/-005 LOW)
- "Minimum 7 scenarios from architecture document" (H-20-01) -- SOURCE CITATION ABSENT (not fixed)
- L2 recommendations format -- NON-STANDARD (not fixed)
- Revision history (lines 593-598) -- CONSISTENT with 3 changes described

### S-010 (Self-Refine Assessment)

The deliverable's S-010 self-review (lines 574-590) has 10 items. None of the 10 items explicitly verifies that prior scorer gaps have been addressed. The checklist includes "Actionability: Does each finding include a recommended fix? -- PASS -- FIND-QA-001 through FIND-QA-005 each include recommended fix or code sample" which is now accurate after the G-008 fix. The S-010 checklist correctly passes on all items when assessed against v1.1.0 state. However, a C4 revision document should include a self-review item for "Prior iteration gaps addressed: [gap-by-gap status]" to provide explicit traceability of the revision cycle.

### S-001 (Red Team)

Attack vectors checked on v1.1.0:
1. L0 finding count mismatch -- RESOLVED: "Five findings are raised" + 5-row findings table.
2. FIND-QA-003 template absent -- RESOLVED: G-008 scaffold with 7 Then clauses.
3. Distribution math not flagged -- RESOLVED: inline QA observation with correct math.
4. "Minimum 7" uncited -- STILL PRESENT: H-20-01 row evidence column says "(8 scenarios)" with no source.
5. L2 format deviation -- STILL PRESENT: three separate tables, not priority-ordered table.
6. New vector: S-010 self-review does not reference prior iteration gaps -- minor gap.
7. New vector: FIND-QA-003 recommendation to "update the scope table" refers to a BEHAVIOR_TESTS.md change that is not tracked as a formal finding or action item.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Traceability / Evidence Quality | 0.93 / 0.93 | 0.95 | In H-20-01 acceptance criterion row (and optionally L0 scenario count table), add architecture source: `step-10-test-spec-architecture.md, Section [N], Quality Strategy, minimum scenario count specification`. This is a single-cell change. |
| 2 | Actionability | 0.93 | 0.95 | At the top of the L2 section, add a consolidated priority-ordered recommendation table `| Priority | Finding | Effort | Risk if Unfixed | Recommendation |` that maps the five findings to prioritized actions. The existing Coverage ROI and Coverage Gaps tables can remain as supporting detail. |
| 3 | Completeness / Methodological Rigor | 0.95 | 0.96 | In FIND-QA-003 Recommended Fix, add a clarifying note: "Note: the scope table update instruction refers to a change in BEHAVIOR_TESTS.md, not in this document. Track as action item [BEHAVIOR_TESTS-001] separate from the G-008 scenario addition." Or convert to a sixth finding FIND-QA-006 (LOW) targeting the scope table documentation gap. |
| 4 | Internal Consistency | 0.96 | 0.97 | Add a self-review item to S-010: "Prior iteration gaps addressed: P1 FIXED (L0 count), P2 FIXED (G-008 scaffold), P3 FIXED (distribution observation), P4 NOT ADDRESSED (min-7 citation), P5 NOT ADDRESSED (L2 format)" to make the revision cycle explicitly traceable. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score (specific line references for all claims)
- [x] Uncertain scores resolved downward: Traceability, Evidence Quality, and Actionability held at 0.93 (not rounded to 0.94) given the "min 7" citation gap affects all three dimensions
- [x] Calibration anchor applied: 0.92 = genuinely excellent, 0.95 = essentially perfect in domain -- the deliverable is strong but two secondary gaps (uncited normative claim, non-standard L2 format) prevent the 0.95 bar
- [x] No dimension scored above 0.96: highest is Internal Consistency at 0.96, justified by complete resolution of the two iter-1 internal consistency defects
- [x] C4 threshold (0.95) applied per C-008 override, not standard 0.92
- [x] Score gap from threshold: 0.95 - 0.944 = 0.006. Two secondary gaps prevent threshold attainment; both are minimal changes (one table cell citation, one format addition)
- [x] Iter-1 improvements confirmed (+0.040 delta): Internal Consistency from 0.87 to 0.96 (+0.09), Completeness from 0.91 to 0.95 (+0.04), Methodological Rigor from 0.91 to 0.95 (+0.04), Actionability from 0.89 to 0.93 (+0.04); Evidence Quality and Traceability unchanged at 0.93 (iter-1 Priorities 4/5 not addressed)

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.944
threshold: 0.95
weakest_dimension: Traceability
weakest_score: 0.93
critical_findings_count: 0
iteration: 2
improvement_recommendations:
  - "Add architecture document source citation to H-20-01 evidence cell: 'step-10-test-spec-architecture.md Section [N] Quality Strategy minimum scenario count specification'"
  - "Add consolidated priority-ordered recommendation table at top of L2 section (existing tables remain as detail)"
  - "Clarify FIND-QA-003 scope-table instruction: note it targets BEHAVIOR_TESTS.md change, not this document; optionally add as FIND-QA-006 (LOW)"
  - "Add S-010 self-review item for prior iteration gap status (P1/P2/P3 FIXED, P4/P5 NOT ADDRESSED)"
```

---

*Score Report Version: 1.0.0 | Agent: adv-scorer | Date: 2026-03-09T00:00:00Z*
*SSOT: `.context/rules/quality-enforcement.md` | Threshold: 0.95 (C-008)*
*Strategies Applied: S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014 (all 10 C4 selected)*
*Prior score: 0.904 (iter-1) | Delta: +0.040 | Gap remaining: 0.006*
