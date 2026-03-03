# Quality Score Report: diataxis-standards.md (Round 5 — Final)

## L0 Executive Summary

**Score:** 0.937/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Traceability (0.92)
**One-line assessment:** SR4-001 fully resolved — Internal Consistency jumped from 0.90 to 0.95 with the EAP-01/Section 3 heuristic threshold reconciliation and corrected alignment claim — but two persistent open items (SR3-007: subsection navigation; SR3-008: "use judgment" unverifiable heuristic) hold the composite at 0.937, 0.013 short of the 0.95 threshold; targeted fixes to both remaining items are required to cross the line.

---

## Scoring Context

- **Deliverable:** `skills/diataxis/rules/diataxis-standards.md`
- **Deliverable Type:** Other (Quality Standards Rule File)
- **Criticality Level:** C3
- **Scoring Strategy:** S-014 (LLM-as-Judge), S-007 (Constitutional AI Critique), S-010 (Self-Refine)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Prior Score:** 0.919 (Round 4)
- **Iteration:** Round 5 (Final)
- **Scored:** 2026-02-27

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.937 |
| **Threshold** | 0.95 (user-specified) |
| **Verdict** | REVISE |
| **Delta from Round 4** | +0.018 (0.919 → 0.937) |
| **Strategy Findings Incorporated** | Yes — S-007 (Constitutional), S-010 (Self-Refine) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.93 | 0.186 | SR4-001 corrected EAP-01 specification; SR3-007 nav still absent from 282-line document |
| Internal Consistency | 0.20 | 0.95 | 0.190 | SR4-001 RESOLVED: EAP-01 now "Minor (1-2) / Major (3+)" consistent with Section 3 "Minor (1-2), Major (3+)"; alignment claim corrected to "3+" |
| Methodological Rigor | 0.20 | 0.94 | 0.188 | SR4-001 removes actively misleading threshold claim; SR3-008 "use judgment" borderline still unverifiable |
| Evidence Quality | 0.15 | 0.94 | 0.141 | Factually inaccurate alignment claim removed by SR4-001; all 29 criteria and 20 anti-patterns retain Test/Pass/Detection Signal columns |
| Actionability | 0.15 | 0.93 | 0.140 | EAP-01 severity contradiction at 2-instance boundary resolved; SR3-007 navigation friction persists for agents |
| Traceability | 0.10 | 0.92 | 0.092 | Criterion IDs (T-01 through EAP-05) stable; SR3-007 absent — no document index maps IDs to locations |
| **TOTAL** | **1.00** | | **0.937** | |

---

## Detailed Dimension Analysis

### Completeness (0.93/1.00)

**Evidence:**
The document continues to provide complete coverage of all four Diataxis quadrants:
- 29 quality criteria: T-01 through T-08 (8), H-01 through H-07 (7), R-01 through R-07 (7), E-01 through E-07 (7)
- 20 anti-patterns: TAP-01 through TAP-05 (5), HAP-01 through HAP-05 (5), RAP-01 through RAP-05 (5), EAP-01 through EAP-05 (5)
- 7 detection heuristics with agent actions and severity bands
- False-Positive Handling Protocol with 3 override conditions
- Writer Agent Self-Review (4 steps including reclassification escalation threshold)
- Classification Decision Guide: 2-axis test, confidence derivation with rationale, 5 borderline cases, multi-quadrant decomposition
- Voice Guidelines: universal markers, 4 per-quadrant voice sections with before/after examples, Voice Quality Gate, Severity Derivation section

SR4-001 completeness improvement (confirmed): EAP-01 (line 106) now fully specifies graduated severity "Minor (1-2) / Major (3+)" consistent with Section 3. The specification is complete for this anti-pattern.

**Gaps:**
- SR3-007 persists (entering Round 5 unfixed): The document is approximately 282 lines with a navigation table covering only 5 `##`-level sections. The `###`-level subsections (Tutorial Quality Criteria, How-To Guide Quality Criteria, Reference Quality Criteria, Explanation Quality Criteria, Tutorial Anti-Patterns, How-To Guide Anti-Patterns, Reference Anti-Patterns, Explanation Anti-Patterns) have no navigation entries. Agents and readers seeking specific criteria must scan the full document. This is a structural completeness gap for a standards document consumed by automated agents.

**Improvement Path:**
Expand the navigation table with `###`-level subsection anchors for the 8 primary subsections (4 criteria + 4 anti-patterns), or add a quick-reference criterion ID index. Would raise this dimension to approximately 0.95-0.96.

---

### Internal Consistency (0.95/1.00)

**Evidence:**
SR4-001 is fully resolved in Round 5. This was the sole blocking Major inconsistency from Round 4.

**SR4-001 RESOLVED (confirmed at line 106):**

EAP-01 now reads: `"Severity: Minor for 1-2 isolated instances; Major for 3+ instances or when imperative verbs form a procedural sequence. This aligns with the Section 3 heuristic threshold (3+ imperative sentences per paragraph = Major)."`

Section 3 heuristic (line 120): `"Minor (1-2), Major (3+)"`

These are now fully consistent. An agent applying EAP-01 and the Section 3 heuristic will reach the same severity conclusion for any count of imperative instances:
- 1 instance: Both say Minor.
- 2 instances: Both say Minor.
- 3+ instances or procedural sequence: Both say Major.

The factually inaccurate claim (previously "2+ = Major") has been corrected to "3+ = Major." The note now accurately describes the heuristic.

All prior consistency fixes from Rounds 3-4 remain intact:
- T-04 / FPP OS-conditional exception: Consistent (SR3-001 persists fixed)
- Case 5 decomposition order vs. canonical sequence: Consistent (SR3-004 persists fixed)
- Writer Agent Self-Review step ordering: Correct (SR3-003 persists fixed)

**Gaps:**
No remaining logical contradictions between stated rules. SR3-008 ("use judgment" at line 37) is an ambiguity issue affecting methodological rigor and actionability, not an internal contradiction between two independently stated rules.

**Improvement Path:**
No internal consistency fixes required. This dimension has reached its practical ceiling given the current content scope.

---

### Methodological Rigor (0.94/1.00)

**Evidence:**
The SR4-001 fix contributes genuine methodological rigor improvement: the false alignment claim was actively directing agents to an incorrect severity threshold (2+ = Major) that contradicted the actual heuristic table. Removing this inaccurate claim means the methodology now coheres — agents following the documented methodology will apply a single consistent threshold.

Methodological rigor foundations remain strong:
- Deterministic 2-axis classification test with operationalized confidence levels (1.00, 0.85, 0.70, <0.70) and documented rationale for each threshold
- 7 heuristic detection signals with detection method specificity (sentence counts, verb forms, exempt contexts)
- False-Positive Handling Protocol with 3 named override conditions (sufficient for programmatic matching)
- Writer Agent Self-Review with correctly ordered steps: apply during H-15 (step 1) → apply False-Positive Protocol before flagging (step 2) → flag when not suppressed (step 3) → reclassify after 3+ ACKNOWLEDGED markers (step 4)
- 5 borderline cases with explicit reasoning chains
- Multi-quadrant decomposition with documented canonical sequence rationale

**Gaps:**
- SR3-008 persists (partially mitigated, minor): Line 37 still reads "1-2 sentence digressions are below mandatory-flag threshold; use judgment when they substantially interrupt action flow." The "use judgment" instruction is not computable by automated agents. The document specifies H-02 pass condition as "Zero 'why' digressions (3+ sentences)" — a concrete threshold — but the exception for 1-2 sentences is unverifiable. This is the only remaining methodology gap.

**Improvement Path:**
Replace "use judgment when they substantially interrupt action flow" with a structural rule: "1-2 sentence digressions do not require flagging unless they appear between two numbered steps (not at the end of a step block); treat as Minor in that position." Would raise this dimension to approximately 0.95-0.96.

---

### Evidence Quality (0.94/1.00)

**Evidence:**
The factually inaccurate alignment claim that was the primary evidence quality defect in Round 4 has been corrected by SR4-001. The EAP-01 note now accurately states "This aligns with the Section 3 heuristic threshold (3+ imperative sentences per paragraph = Major)" — which correctly describes both the EAP-01 graduated severity and the Section 3 heuristic band.

Strong evidence foundations established in prior rounds continue:
- All 29 quality criteria: Test column (how to check) + Pass Condition column (what passes). Each criterion is independently testable.
- 20 anti-patterns: Detection Signal column with specific observable patterns (e.g., `"Paragraph between numbered steps that contains no imperative verbs and explains rationale"`)
- 7 heuristic detection signals: Detection Method column with agent-level specificity (sentence counts, verb forms, exemptions)
- Confidence derivation rationale column in classification guide — threshold values (1.00, 0.85, 0.70, <0.70) are each justified
- 5 borderline cases with specific primary signal, secondary signal, and resolution reasoning
- False-positive override conditions specific enough for pattern matching
- Severity Derivation section (lines 276-281): Critical/Major/Minor definitions with impact criteria grounding the anti-pattern severity assignments
- T-08 `[UNTESTED]` flag mechanism provides a concrete evidentiary handle for unverified steps

**Gaps:**
- SR3-008 (minor residual): The "use judgment" note at H-02 passes evidence quality threshold — it is not a false claim, merely vague. Evidence quality does not score claims that are true-but-ambiguous as defects. No remaining factual inaccuracies identified.

**Improvement Path:**
Evidence quality is at near-ceiling for the current scope. The SR3-008 fix would eliminate the remaining vagueness but is primarily a methodological rigor improvement, not an evidence quality fix. No targeted evidence quality improvements beyond SR3-008.

---

### Actionability (0.93/1.00)

**Evidence:**
Round 5 resolves the primary actionability gap from Round 4. The EAP-01 severity contradiction at exactly 2 instances is now resolved — agents applying EAP-01 and the Section 3 heuristic will now produce consistent severity outputs at all instance counts.

The document remains highly actionable for writer agents:
- Per-criterion test and pass conditions are mechanically applicable
- False-Positive Handling Protocol provides specific override conditions
- Reclassification escalation: concrete threshold of 3+ `[ACKNOWLEDGED]` markers
- Voice Quality Gate: 4-step process with explicit flag notation `[VOICE: {description}]`
- Writer Agent Self-Review: numbered steps with correct logical ordering
- Decomposition sequence: explicit canonical order with rationale

**Gaps:**
- SR3-007 persists: Writer agents navigating to specific criteria (e.g., H-03 real-world variations, R-06 examples) must scan the full 282-line document. No subsection anchors or criterion-ID index enables direct navigation. For automated agents loading the document by section, this is non-trivial friction.
- SR3-008 minor: "use judgment" at H-02 means agents have no deterministic decision rule for borderline 1-2 sentence digressions between steps.

**Improvement Path:**
SR3-007 (subsection navigation) addresses the primary actionability friction. SR3-008 (structural heuristic for H-02) addresses the remaining undecidable case. Together these would raise this dimension to approximately 0.95-0.96.

---

### Traceability (0.92/1.00)

**Evidence:**
Strong traceability foundations persist from prior rounds:
- All criterion IDs (T-01 through E-07) and anti-pattern IDs (TAP-01 through EAP-05) are stable and consistent across the document
- Severity Derivation section (lines 276-281) grounds anti-pattern severity assignments in explicit Critical/Major/Minor criteria definitions
- Voice Quality Gate explicitly labeled as MEDIUM-tier standard (override with documented justification)
- Decomposition sequence rationale documented in Section 4
- T-03 scope boundary explicitly defined ("Earlier means content appearing before the current step within this document")
- Confidence derivation rationale column documents why each threshold value was selected

**Gaps:**
- SR3-007 persists: Criterion IDs (T-01, H-03, EAP-01, etc.) are stable and cited in quality reports, but no document-level index maps IDs to their section locations. An agent or reviewer searching for "EAP-01 definition" must scan all 282 lines rather than navigating directly. This is the only remaining traceability gap.

**Improvement Path:**
Add `###`-level subsection anchors in the navigation table or a quick-reference criterion ID table. Would raise this dimension to approximately 0.95.

---

## S-007 Constitutional Compliance

**Applicable principles evaluated:**

| Principle | Tier | Status | Evidence |
|-----------|------|--------|----------|
| H-23 (navigation table) | HARD | COMPLIANT | Lines 5-13: "Document Sections" navigation table with 5 entries; all 5 `##`-level sections listed |
| H-24 (anchor links) | HARD | COMPLIANT | All 5 entries use `[Section N: ...]( #section-N-... )` anchor syntax |
| NAV-002 (placement) | MEDIUM | COMPLIANT | Navigation table at lines 5-13, immediately after title and tagline |
| NAV-004 (`##` headings) | MEDIUM | COMPLIANT | All 5 `##` primary sections listed |
| NAV-004 (`###` advisory) | MEDIUM | PARTIAL (persists Round 1-5) | 282-line file; `###` subsection anchors absent across 5 rounds without resolution |
| P-001 (Truth/Accuracy) | Constitutional | IMPROVED | SR4-001 corrected factually inaccurate alignment claim in EAP-01. Document no longer contains false factual statements. |

**Constitutional Compliance Score: 0.97** (unchanged HARD compliance; MEDIUM advisory gap persists fifth round)

**CC-001 (Minor, Round 5):** No HARD rule violations. The NAV-004 advisory gap for `###`-level subsection navigation in a 282-line document has now been open for five revision rounds without resolution. No HARD constraint is violated; the pattern of persistent deferral is noted.

---

## S-010 Self-Refine Findings

### Round 5 Remediation Verification

| ID | Finding | Status | Evidence |
|----|---------|--------|----------|
| SR4-001 | EAP-01 threshold vs. Section 3 heuristic mismatch; inaccurate alignment claim | **FIXED** | Line 106: EAP-01 now "Minor for 1-2 isolated instances; Major for 3+ instances." Alignment claim now reads "3+ imperative sentences per paragraph = Major." Section 3 (line 120) reads "Minor (1-2), Major (3+)." Fully consistent. |
| SR3-007 | No `###`-level subsection navigation | **OPEN** (Round 5 deferral) | Navigation table still covers only 5 `##` sections. No `###` anchors added. Persists from Round 1. |
| SR3-008 | H-02 "use judgment" unverifiable | **OPEN** (Round 5 deferral) | Line 37: "use judgment when they substantially interrupt action flow" persists. No structural heuristic added. |

### New Findings (Round 5)

No new findings identified. SR4-001 resolution did not introduce any new inconsistencies. The EAP-01 change is internally coherent: both the severity cell ("Minor (1-2) / Major (3+)") and the alignment claim text ("3+ imperative sentences per paragraph = Major") now accurately reflect the Section 3 heuristic.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Completeness / Actionability / Traceability | 0.93 / 0.93 / 0.92 | 0.95+ | **SR3-007:** Add `###`-level subsection navigation. Expand the navigation table with entries for: Tutorial Quality Criteria, How-To Guide Quality Criteria, Reference Quality Criteria, Explanation Quality Criteria, Tutorial Anti-Patterns, How-To Guide Anti-Patterns, Reference Anti-Patterns, Explanation Anti-Patterns. Each entry requires `[Subsection Name](#anchor)` format per NAV-006. |
| 2 | Methodological Rigor | 0.94 | 0.96 | **SR3-008:** Replace "use judgment when they substantially interrupt action flow" in H-02 pass condition note with: "1-2 sentence digressions do not require flagging unless they appear between two numbered steps (not at the end of a step block); treat as Minor in that position." This converts an unverifiable instruction into a deterministic structural rule. |

---

## Gap to Threshold Analysis

**Threshold:** 0.95 | **Current:** 0.937 | **Gap:** 0.013

**SR4-001 impact confirmed:** Internal Consistency moved from 0.90 to 0.95 (+0.05 on dimension; +0.010 weighted). Evidence Quality moved from 0.91 to 0.94 (+0.03 on dimension; +0.005 weighted). Net improvement: +0.015 weighted. Actual composite delta: 0.919 → 0.937 = +0.018 (consistent with projections).

**Remaining gap drivers:**

| Dimension | Current Score | Score After SR3-007 Fix | Score After SR3-008 Fix | Projected After Both |
|-----------|---------------|------------------------|------------------------|---------------------|
| Completeness | 0.93 | 0.96 | 0.93 | 0.96 |
| Internal Consistency | 0.95 | 0.95 | 0.95 | 0.95 |
| Methodological Rigor | 0.94 | 0.94 | 0.96 | 0.96 |
| Evidence Quality | 0.94 | 0.94 | 0.94 | 0.94 |
| Actionability | 0.93 | 0.95 | 0.94 | 0.96 |
| Traceability | 0.92 | 0.96 | 0.92 | 0.96 |

**Projected composite after SR3-007 only:**
(0.96×0.20) + (0.95×0.20) + (0.94×0.20) + (0.94×0.15) + (0.95×0.15) + (0.96×0.10)
= 0.192 + 0.190 + 0.188 + 0.141 + 0.1425 + 0.096 = **0.950** — exactly at threshold.

**Projected composite after both SR3-007 and SR3-008:**
(0.96×0.20) + (0.95×0.20) + (0.96×0.20) + (0.94×0.15) + (0.96×0.15) + (0.96×0.10)
= 0.192 + 0.190 + 0.192 + 0.141 + 0.144 + 0.096 = **0.955** — above threshold.

**Conclusion:** SR3-007 (subsection navigation) is the single most valuable remaining fix. It is load-bearing — fixing SR3-007 alone brings the projected composite to exactly 0.950. Fixing both SR3-007 and SR3-008 reaches approximately 0.955, providing margin above the threshold.

---

## Progress Across Rounds

| Round | Score | Delta | Status | Key Gap |
|-------|-------|-------|--------|---------|
| Round 1 | 0.816 | -- | REVISE | 15 open findings, 7 Priority 1 |
| Round 2 | 0.816 | 0.000 | REVISE | All Priority 1 partially addressed |
| Round 3 | 0.886 | +0.070 | REVISE | 4 new conflicts introduced by R2 fixes |
| Round 4 | 0.919 | +0.033 | REVISE | EAP-01 threshold misalignment; inaccurate alignment claim |
| Round 5 | 0.937 | +0.018 | REVISE | SR3-007 subsection nav; SR3-008 use judgment |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific line references (line 37, line 106, line 120)
- [x] Uncertain scores resolved downward: Actionability could have been 0.94 (SR4-001 removed severity ambiguity) but SR3-007 navigation persists; held at 0.93. Internal Consistency at 0.95 — checked that no remaining contradictions exist before scoring at ceiling.
- [x] Fifth-iteration calibration applied: 0.937 reflects two concrete open items, not arbitrary deduction. Each dimension score is justified by specific evidence.
- [x] No dimension scored above 0.95: Internal Consistency at exactly 0.95 — justified by complete elimination of all identified contradictions. No inflation beyond what evidence supports.
- [x] Mathematical verification: (0.93×0.20) + (0.95×0.20) + (0.94×0.20) + (0.94×0.15) + (0.93×0.15) + (0.92×0.10) = 0.186 + 0.190 + 0.188 + 0.141 + 0.1395 + 0.092 = **0.9365 ≈ 0.937** ✓
- [x] Verdict matches score range: 0.937 < 0.95 threshold = REVISE ✓

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.937
threshold: 0.95
weakest_dimension: Traceability
weakest_score: 0.92
critical_findings_count: 0
iteration: 5
improvement_recommendations:
  - "SR3-007 (P1 Minor): Add ###-level subsection navigation anchors for 8 primary subsections — Tutorial/How-To/Reference/Explanation Quality Criteria and their corresponding Anti-Patterns. This single fix is projected to raise the composite to exactly 0.950."
  - "SR3-008 (P2 Minor): Replace 'use judgment when they substantially interrupt action flow' in H-02 pass condition with structural heuristic: '1-2 sentence digressions do not require flagging unless they appear between two numbered steps; treat as Minor in that position.' Together with SR3-007, projected composite ~0.955."
```
