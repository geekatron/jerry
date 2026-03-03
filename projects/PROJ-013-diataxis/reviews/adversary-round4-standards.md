# Quality Score Report: diataxis-standards.md (Round 4)

## L0 Executive Summary

**Score:** 0.919/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.90)
**One-line assessment:** Round 4 fixes resolved the two highest-RPN findings (SR3-001 T-04/FPP conflict, SR3-003 step ordering inversion, SR3-004 Case 5 ordering, SR3-005 severity derivation, SR3-006 voice rule tier) and the score jumped from 0.886 to 0.919, but a residual internal inconsistency in EAP-01 vs. Section 3 heuristic severity thresholds at the 2-instance boundary — combined with a factually inaccurate alignment claim in the EAP-01 note — prevents crossing the 0.95 threshold.

---

## Scoring Context

- **Deliverable:** `skills/diataxis/rules/diataxis-standards.md`
- **Deliverable Type:** Other (Quality Standards Rule File)
- **Criticality Level:** C3
- **Scoring Strategy:** S-014 (LLM-as-Judge) with S-007 (Constitutional AI Critique), S-004 (Pre-Mortem Analysis), S-010 (Self-Refine)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Prior Score:** 0.886 (Round 3)
- **Iteration:** Round 4
- **Scored:** 2026-02-27

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.919 |
| **Threshold** | 0.95 (user-specified) |
| **Verdict** | REVISE |
| **Delta from Round 3** | +0.033 (0.886 → 0.919) |
| **Strategy Findings Incorporated** | Yes — S-007 (Constitutional), S-004 (Pre-Mortem), S-010 (Self-Refine) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.93 | 0.186 | T-04/FPP conflict resolved; EAP-01 graduated; SR3-007 subsection nav still absent |
| Internal Consistency | 0.20 | 0.90 | 0.180 | SR3-001/SR3-004 resolved; residual EAP-01 vs. heuristic threshold misalignment at 2-instance boundary |
| Methodological Rigor | 0.20 | 0.93 | 0.186 | SR3-003 step ordering fixed; SR3-008 "use judgment" persists as minor |
| Evidence Quality | 0.15 | 0.91 | 0.137 | All criteria retain test+pass; EAP-01 note contains factually inaccurate alignment claim |
| Actionability | 0.15 | 0.92 | 0.138 | T-04/FPP conflict resolved; step ordering fixed; EAP-01 2-instance contradiction remains |
| Traceability | 0.10 | 0.92 | 0.092 | SR3-005 severity derivation added; SR3-006 MEDIUM tier labeled; SR3-007 persists |
| **TOTAL** | **1.00** | | **0.919** | |

---

## Detailed Dimension Analysis

### Completeness (0.93/1.00)

**Evidence:**
The document covers all four quadrants with full criteria tables (T-01 through T-08, H-01 through H-07, R-01 through R-07, E-01 through E-07), anti-patterns (20 total), 7 detection heuristics, False-Positive Handling Protocol with 3 override conditions, Writer Agent Self-Review (4 steps with reclassification escalation), Classification Decision Guide with 2-axis test, confidence derivation rationale, 5 borderline cases, multi-quadrant decomposition, and voice guidelines scoped to Diataxis deliverables.

Round 4 completeness improvements:
- SR3-001 resolved: T-04 (line 26-27) now explicitly states the OS-conditional exception. The `"Zero 'alternatively' or 'you could also' constructions. Exception: OS-conditional paths (macOS/Windows/Linux) are legitimate platform branching per the False-Positive Handling Protocol, not alternatives."` completes the specification for the most common tutorial authorship pattern.
- SR3-002 addressed: EAP-01 (line 106) now graduated — "Severity: Minor for 1 isolated instance; Major for 2+ instances or when imperative verbs form a procedural sequence." The completeness of EAP-01's severity specification improves.
- SR3-005 resolved: Severity Derivation section (lines 276-281) adds Critical/Major/Minor definitions referenced by all anti-pattern tables.

**Gaps:**
- SR3-007 persists (entering Round 5): The file is now approximately 282 lines with no `###`-level subsection navigation. Readers and agents seeking "How-To Guide Quality Criteria" or "Reference Anti-Patterns" must scroll through the full document. This is a moderate completeness gap for a standards document consumed by automated agents.

**Improvement Path:**
Add `###`-level anchors to the main navigation table or a quick-reference criterion ID table mapping T-01, H-03, etc. to section locations. Would raise this dimension to approximately 0.95.

---

### Internal Consistency (0.90/1.00)

**Evidence:**
Significant improvement from Round 3 (0.83). Three of four Round 3 internal consistency conflicts are resolved:

- **SR3-001 RESOLVED:** T-04 and False-Positive Protocol are now consistent. T-04 explicitly excepts OS-conditional alternatives; FPP's override condition aligns with the T-04 exception text. An agent applying both will reach the same conclusion.
- **SR3-004 RESOLVED:** Case 5 decomposition order (line 190-193) now reads "1. How-To Guide, 2. Reference, 3. Explanation" — consistent with the canonical sequence at line 199 ("Tutorial first (if present), then How-To Guide, then Reference, then Explanation"). Case 5 has no Tutorial, so the corrected How-To → Reference → Explanation order matches the canonical rule.

**Gaps:**
The SR3-002 fix introduced a residual inconsistency not fully resolved in Round 4.

**EAP-01 vs. Section 3 heuristic severity threshold at 2 instances (OPEN):**

EAP-01 (line 106): `"Severity: Minor for 1 isolated instance; Major for 2+ instances or when imperative verbs form a procedural sequence."`

Section 3 heuristic table (line 120): The signal fires at `"2+ imperative sentences"` within a single paragraph with severity `"Minor (1-2), Major (3+)"`.

These two specifications are inconsistent at the 2-instance boundary:
- EAP-01 says: 2 instances = **Major**
- Section 3 heuristic says: 1-2 = **Minor**, 3+ = **Major** → at 2 instances = **Minor**

An explanation document containing exactly 2 imperative sentences in the same paragraph will receive conflicting severity signals from the two tables. EAP-01 escalates to Major; the heuristic assigns Minor.

**Compounding problem:** The EAP-01 note explicitly claims `"This aligns with the Section 3 heuristic threshold (2+ imperative sentences per paragraph = Major)"` — but this claim is factually wrong. The Section 3 heuristic does NOT show 2+ = Major; it shows Minor (1-2) / Major (3+). The note misrepresents the heuristic, potentially causing agents to rely on the claim rather than checking the table directly.

**Improvement Path:**
Reconcile the two thresholds. Two options:
- Option A (preferred): Change EAP-01 to match the heuristic: "Minor for 1-2 isolated instances; Major for 3+ instances or when imperative verbs form a procedural sequence." Update the alignment claim accordingly.
- Option B: Change the Section 3 heuristic to match EAP-01: Change "Minor (1-2), Major (3+)" to "Minor (1), Major (2+)." Update the "2+ imperative sentences" trigger accordingly.
Either option removes the contradiction. Correct the alignment claim to accurately describe the reconciled thresholds. Would raise this dimension to approximately 0.95.

---

### Methodological Rigor (0.93/1.00)

**Evidence:**
Strong round-over-round improvement. The methodology now includes:
- Deterministic 2-axis classification test with operationalized confidence levels and rationale
- 7 heuristic detection signals with specific agent actions and severity bands
- False-Positive Handling Protocol with 3 named override conditions
- Writer Agent Self-Review Behavior with correctly ordered steps (SR3-003 RESOLVED)
- 5 borderline case resolution examples with explicit reasoning
- Multi-quadrant decomposition sequence with rationale
- Graduated severity for EAP-01 and aligned `[ACKNOWLEDGED]` reclassification threshold

**SR3-003 RESOLVED:** Writer Agent Self-Review steps (lines 139-143) now correctly sequence: Step 1 (apply during H-15 self-review), Step 2 (apply False-Positive Protocol before flagging), Step 3 (when signal not suppressed, flag and engage user). The logical order is now correct — check before flag, not flag then retract.

**Gaps:**
- SR3-008 persists (minor, partially mitigated): Line 37 still reads "1-2 sentence digressions are below mandatory-flag threshold; use judgment when they substantially interrupt action flow." The "use judgment" instruction is unverifiable for automated agents. No structural heuristic replaces this for borderline 1-2 sentence digression cases. The Round 3 note clarified the threshold boundary but did not provide a decision rule for borderline cases.

**Improvement Path:**
Replace "use judgment when they substantially interrupt action flow" with: "1-2 sentence digressions do not require flagging unless they appear between two numbered steps (not at the end of a step block); in that case, treat as Minor." Would raise this dimension to approximately 0.95.

---

### Evidence Quality (0.91/1.00)

**Evidence:**
The document maintains strong evidence quality foundations established across prior rounds:
- All 29 quality criteria (T-01 through E-07) include explicit Test and Pass Condition columns
- 20 anti-patterns include specific Detection Signal patterns
- 7 heuristic signals include detection method specifications with agent actions
- 5 borderline case examples provide concrete resolution reasoning
- Before/after voice examples are specific and illustrative
- Confidence derivation rationale column present in classification guide
- False-positive override conditions are specific enough for programmatic matching
- T-08 `[UNTESTED]` flag mechanism is well-targeted

Round 4 improvement: SR3-005 resolved — "Severity Derivation for Anti-Pattern Tables" section (lines 276-281) provides Critical/Major/Minor definitions with impact criteria. This adds substantive evidence for the severity assignments across all anti-pattern tables.

**Gap:**
The EAP-01 note (line 106) contains a factually inaccurate claim: `"This aligns with the Section 3 heuristic threshold (2+ imperative sentences per paragraph = Major)"`. The Section 3 heuristic actually shows Minor (1-2) / Major (3+), not 2+ = Major. An agent reading this alignment claim as authoritative will be misled about the actual heuristic values. This is a direct evidence quality defect — a factual misrepresentation within the document's own specification.

**Improvement Path:**
Correct the alignment claim in EAP-01 to accurately describe the reconciled threshold after resolving the Internal Consistency gap above. For example: "This aligns with Section 3: single-instance = Minor; the heuristic escalates to Major at 3+ instances per paragraph, or when imperative verbs form a procedural sequence at 2+." Would raise this dimension to approximately 0.94.

---

### Actionability (0.92/1.00)

**Evidence:**
Round 4 resolved the two primary actionability blockers from Round 3:

- T-04/FPP conflict RESOLVED: Agents evaluating OS-conditional tutorials now have clear, non-contradictory guidance. T-04 exception text and FPP override condition give the same answer.
- Writer Agent Self-Review step ordering FIXED: Step 2 now instructs false-positive check before step 3 instructs flagging. Agents following the numbered list in sequence will perform the correct actions in the correct order.

The document remains highly actionable overall:
- Per-criterion test and pass conditions are mechanically applicable
- False-Positive Handling Protocol provides specific override conditions
- Reclassification escalation (step 4) gives a concrete threshold (3+ `[ACKNOWLEDGED]` markers)
- Voice Quality Gate provides a 4-step process with explicit flag notation

**Gaps:**
- EAP-01 two-instance severity contradiction: At exactly 2 imperative sentences, agents applying EAP-01 (Major) and Section 3 heuristic (Minor) will produce different severity outputs. This is an actionability gap for the borderline case.
- SR3-007 persists: No subsection navigation means agents and users must scan the full 282-line document to locate specific criteria. Minor but recurring friction.

**Improvement Path:**
Resolve the EAP-01/heuristic threshold alignment (see Internal Consistency). Add subsection navigation. Would raise this dimension to approximately 0.95.

---

### Traceability (0.92/1.00)

**Evidence:**
Strong improvement from Round 3 (0.88):
- SR3-005 RESOLVED: Severity Derivation section (lines 276-281) now provides documented criteria for Critical/Major/Minor severity ratings. The anti-pattern tables' severity assignments are now derivable from explicit criteria rather than undocumented judgment.
- SR3-006 RESOLVED: Voice Quality Gate (line 270) now reads "This gate is a MEDIUM-tier standard (override with documented justification)." Rule tier is now explicit, agents can treat voice violations as MEDIUM (not HARD).
- All criterion IDs (T-01 through E-07), anti-pattern IDs (TAP-01 through EAP-05), and detection signal entries remain stable and traceable.
- Decomposition sequence rationale added in Round 3 (persists).
- T-03 scope boundary defined in Round 3 (persists).

**Gaps:**
- SR3-007 persists: No `###`-level subsection navigation. Criterion IDs exist but no document-level index maps T-01 to its line or section. This is a traceability gap — criterion IDs are cited in quality reports but require full document scan to locate their definitions.

**Improvement Path:**
Add a quick-reference criterion ID table or `###`-level subsection anchors in the navigation table. Would raise this dimension to approximately 0.95.

---

## S-007 Constitutional Compliance

**Applicable principles evaluated:**

| Principle | Tier | Status | Evidence |
|-----------|------|--------|----------|
| H-23 (navigation table) | HARD | COMPLIANT | Lines 5-13: "Document Sections" navigation table with 5 entries |
| H-24 (anchor links) | HARD | COMPLIANT | All 5 entries use `[Section N: ...]( #section-N-... )` anchor syntax |
| NAV-002 (placement) | MEDIUM | COMPLIANT | Navigation table at lines 5-13, immediately after title and tagline |
| NAV-004 (`##` headings) | MEDIUM | COMPLIANT | All 5 `##` primary sections listed |
| NAV-004 (`###` advisory) | MEDIUM | PARTIAL (persists Round 1) | 282-line file; `###` subsection anchors absent |

**Constitutional Compliance Score: 0.97** (unchanged — no HARD violations; one persistent MEDIUM advisory gap, now in its fourth round open)

**CC-001 (Minor, Round 4):** No HARD rule violations. MEDIUM advisory gap for `###`-level subsection navigation in a 282-line document entering its fourth round without resolution. The gap is low impact (no HARD constraint violated) but now demonstrates pattern of persistent deferral.

---

## S-004 Pre-Mortem Analysis (Post-Round 4)

**Failure scenario:** It is 2026-08-27. diataxis-standards.md Round 4 is deployed. Writer agents are evaluating explanation documents that contain exactly 2 imperative sentences in a paragraph. Agent A applies EAP-01: "2+ instances = Major." Agent B applies the Section 3 heuristic: "Minor (1-2)." They produce different severity reports. Users receiving inconsistent quality feedback raise tickets. The EAP-01 alignment note ("This aligns with the Section 3 heuristic threshold (2+ imperative sentences per paragraph = Major)") is quoted as authoritative, confusing the issue further.

**Remaining failure causes:**

| ID | Failure Cause | Likelihood | Severity | Priority |
|----|---------------|------------|----------|----------|
| PM4-001 | EAP-01 "2+ = Major" vs. Section 3 heuristic "Minor (1-2)" at exactly 2 instances — contradictory severity | Medium | Major | P1 |
| PM4-002 | EAP-01 note incorrectly claims alignment with Section 3; agents may trust the note over the table | Medium | Minor | P1 |
| PM4-003 | SR3-008: H-02 "use judgment" borderline case unverifiable for automated agents | Low | Minor | P3 |
| PM4-004 | SR3-007: 282-line document without subsection navigation — sustained navigation friction | Medium | Minor | P2 |

---

## S-010 Self-Refine Findings

### Round 4 Remediation Verification

| SR3 ID | Finding | Status | Evidence |
|--------|---------|--------|----------|
| SR3-001 | T-04 / False-Positive Protocol conflict | **FIXED** | Line 26-27: T-04 exception added: "Exception: OS-conditional paths (macOS/Windows/Linux) are legitimate platform branching per the False-Positive Handling Protocol, not alternatives." FPP remains consistent. |
| SR3-002 | EAP-01 vs. heuristic threshold inconsistency | **PARTIALLY FIXED** | EAP-01 now graduated (Minor/Major) but the threshold values do not match Section 3 heuristic (EAP-01: 2+ = Major; Section 3: Minor 1-2, Major 3+). Alignment claim in EAP-01 note is factually inaccurate. |
| SR3-003 | Writer Agent Self-Review step ordering inversion | **FIXED** | Lines 139-142: Step 2 now "Apply the False-Positive Handling Protocol above before flagging," step 3 now "When a mixing signal is detected (and not suppressed by step 2): flag." Logical order correct. |
| SR3-004 | Case 5 decomposition order vs. canonical sequence | **FIXED** | Lines 190-193: Order corrected to How-To Guide → Reference → Explanation, consistent with canonical sequence for no-Tutorial multi-quadrant documents. |
| SR3-005 | Severity derivation undocumented | **FIXED** | Lines 276-281: "Severity Derivation for Anti-Pattern Tables" section added with Critical/Major/Minor criteria definitions. |
| SR3-006 | Voice Quality Gate lacks rule tier | **FIXED** | Line 270: "This gate is a MEDIUM-tier standard (override with documented justification)" explicitly added. |
| SR3-007 | No `###`-level subsection navigation | **OPEN** (Round 4 deferral) | 282-line file; no new anchors added in Round 4. Persists from Round 1. |
| SR3-008 | H-02 "use judgment" unverifiable | **OPEN** (partially mitigated) | Line 37: "use judgment when they substantially interrupt action flow" still present. No structural heuristic replacement added in Round 4. |

### New Findings (Round 4)

| ID | Severity | Finding | Dimension |
|----|----------|---------|-----------|
| SR4-001 | **Major** | EAP-01 severity threshold (2+ = Major) contradicts Section 3 heuristic severity band (Minor 1-2, Major 3+) at the 2-instance boundary. EAP-01 note's claim of alignment is factually inaccurate. | Internal Consistency, Evidence Quality |

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.90 | 0.95 | **SR4-001:** Reconcile EAP-01 severity threshold with Section 3 heuristic. Preferred fix: change EAP-01 from "Major for 2+" to "Major for 3+ or when imperative verbs form a procedural sequence" to match Section 3's Minor (1-2) / Major (3+) bands. Update the alignment claim to accurately describe the reconciled thresholds. |
| 2 | Evidence Quality | 0.91 | 0.94 | **SR4-001 (same fix):** Correct EAP-01 note from "This aligns with the Section 3 heuristic threshold (2+ imperative sentences per paragraph = Major)" to an accurate description after threshold reconciliation above. |
| 3 | Completeness | 0.93 | 0.96 | **SR3-007:** Add `###`-level subsection anchors in the navigation table for the four quadrant criteria subsections and four anti-pattern subsections, enabling direct navigation to "Tutorial Quality Criteria," "How-To Guide Anti-Patterns," etc. |
| 4 | Traceability | 0.92 | 0.95 | **SR3-007 (same fix):** Navigation anchors also resolve traceability gap for criterion ID lookups. |
| 5 | Actionability | 0.92 | 0.95 | **SR3-007 (same fix):** Subsection navigation reduces agent document-scan friction. EAP-01 fix also removes the 2-instance severity contradiction. |
| 6 | Methodological Rigor | 0.93 | 0.95 | **SR3-008:** Replace "use judgment when they substantially interrupt action flow" with a structural heuristic: "1-2 sentence digressions do not require flagging unless they appear between two numbered steps (not at the end of a step block); treat as Minor in that position." |

---

## Round 4 Scoring Summary

### Progress Across Rounds

| Round | Score | Delta | Status | Key Gap |
|-------|-------|-------|--------|---------|
| Round 1 | 0.816 | -- | REVISE | 15 open findings, 7 Priority 1 |
| Round 2 | 0.816 | 0.000 | REVISE | All Priority 1 partially addressed |
| Round 3 | 0.886 | +0.070 | REVISE | 4 new conflicts introduced by R2 fixes |
| Round 4 | 0.919 | +0.033 | REVISE | EAP-01 threshold misalignment; inaccurate alignment claim |

### Gap to Threshold Analysis

**Threshold:** 0.95 | **Current:** 0.919 | **Gap:** 0.031

The gap is driven by two dimensions below 0.92:
1. **Internal Consistency (0.90):** EAP-01 vs. Section 3 heuristic severity threshold mismatch at 2-instance boundary + inaccurate alignment claim. Fixing SR4-001 alone would raise this dimension to approximately 0.95 (eliminating the only remaining Major inconsistency).
2. **Evidence Quality (0.91):** Inaccurate alignment claim in EAP-01 note. Resolved together with SR4-001.

With SR4-001 resolved plus SR3-007 (subsection navigation) and SR3-008 (use judgment heuristic), projected Round 5 composite:
- Internal Consistency: ~0.95
- Evidence Quality: ~0.94
- Completeness: ~0.95
- Methodological Rigor: ~0.95
- Actionability: ~0.94
- Traceability: ~0.95
- **Projected composite: ~0.946** — still marginally below 0.95 due to residual SR3-008 minor issue.

For confident PASS at 0.95: SR4-001 (Major), SR3-007 (navigation), and SR3-008 (use judgment heuristic) must all be addressed.

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific line references
- [x] Uncertain scores resolved downward (Internal Consistency: could have scored 0.91 but confirmed 0.90 given the factually inaccurate alignment claim; Evidence Quality: could have scored 0.92 but confirmed 0.91 given same claim)
- [x] Fourth-iteration calibration considered — this is revision cycle 4; the calibration anchors apply: 0.92 = genuinely excellent; scoring at 0.919 reflects real remaining defects, not arbitrary deduction
- [x] No dimension scored above 0.95 without exceptional evidence
- [x] Mathematical check: (0.93 × 0.20) + (0.90 × 0.20) + (0.93 × 0.20) + (0.91 × 0.15) + (0.92 × 0.15) + (0.92 × 0.10) = 0.186 + 0.180 + 0.186 + 0.137 + 0.138 + 0.092 = **0.919** ✓
- [x] Verdict matches score range: 0.919 < 0.95 threshold = REVISE ✓

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.919
threshold: 0.95
weakest_dimension: Internal Consistency
weakest_score: 0.90
critical_findings_count: 0
iteration: 4
improvement_recommendations:
  - "SR4-001 (P1 Major): Reconcile EAP-01 severity threshold with Section 3 heuristic Minor(1-2)/Major(3+); correct inaccurate alignment claim in EAP-01 note"
  - "SR3-007 (P2 Minor): Add ###-level subsection navigation anchors to 282-line document"
  - "SR3-008 (P3 Minor): Replace 'use judgment' in H-02 with structural heuristic for 1-2 sentence digression borderline cases"
```
