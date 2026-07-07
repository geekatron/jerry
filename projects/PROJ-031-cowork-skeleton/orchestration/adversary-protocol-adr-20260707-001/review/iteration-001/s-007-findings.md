# Constitutional Compliance Report: ADR-adversary-tournament-protocol-001 (Verified-Criticals Tournament Methodology)

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All findings at a glance |
| [Finding Details](#finding-details) | Full evidence, analysis, remediation per finding |
| [Recommendations](#remediation-plan) | Prioritized remediation plan |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions + constitutional compliance score |

---

**Strategy:** S-007 Constitutional AI Critique
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
**Criticality:** C3
**Date:** 2026-07-07
**Reviewer:** adv-executor (blind, S-007 lane)
**Constitutional Context:** `docs/governance/JERRY_CONSTITUTION.md` (P-001, P-020, P-022 in scope); `.context/rules/quality-enforcement.md` (SSOT: H-13, H-14, H-16, RT-M-010, HARD Rule Index, Retired Rule IDs, HARD Rule Ceiling); `.context/rules/agent-development-standards.md` (H-34/H-35 compound); `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (Scheme B / ADR-M-001..013); `skills/adversary/agents/adv-scorer.md`, `adv-selector.md`, `SKILL.md` (cited change surface, verified against live files)

---

## Summary

**PARTIAL compliance.** No HARD-rule text is edited and the 25/25 ceiling claim holds; Scheme-B ID/frontmatter compliance (ADR-M-001/M-013) is correct. However, the review surfaced **2 Critical** and **1 Major** evidentiary/internal-consistency defects that are self-referentially serious for an ADR whose entire thesis is "don't trust an unverified claim" — including one risk-mitigation statement that is the logical inverse of the mechanism it describes, and a cost-model claim that is empirically false against the ADR's own cited files (filesystem-verified in this review). Plus **2 Minor** findings (naming collision, retired-rule-ID citation). Recommend **REVISE** before this ADR is presented for user ratification.

---

## Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| CC-001-20260707-iter1 | P-001/P-022 (Truth/No Deception) | HARD | Critical | RSK-1 mitigation ("DEFAULT-REFUTED biases toward *keeping* claims") contradicts the ADR's own definition of DEFAULT-REFUTED (anti-inflation default) at 3 other locations | Internal Consistency |
| CC-002-20260707-iter1 | P-001 (Truth/Accuracy); Methodological Rigor | HARD (evidentiary) | Critical | Verification-call granularity is stated three incompatible ways, and the Cost Model formula is falsified by the ADR's own cited panel-file evidence (filesystem-verified) | Methodological Rigor |
| CC-003-20260707-iter1 | P-001 (Truth/Accuracy) | MEDIUM (evidentiary) | Major | "18 verification-panel files" for FU-log iteration-008 is false; actual count is 12 (filesystem-verified twice) | Evidence Quality |
| CC-004-20260707-iter1 | Internal Consistency (naming) | SOFT | Minor | "Group D — Verify" (existing finder strategies) and the new "Verify stage" (refutation panels) reuse the word "Verify" for two different pipeline concepts | Internal Consistency |
| CC-005-20260707-iter1 | Traceability | SOFT | Minor | ADR cites "per H-35" for the constitutional-triplet/forbidden-actions requirement; H-35 is a retired ID (folded into H-34 sub-item b, EN-002, 2026-02-21) | Traceability |

**Finding ID format:** `CC-{NNN}-20260707-iter1` (execution_id = review date + iteration marker, this blind S-007 lane).

---

## Finding Details

### CC-001-20260707-iter1: RSK-1 Mitigation Is the Logical Inverse of DEFAULT-REFUTED [CRITICAL]

**Principle:** P-001 (Truth/Accuracy) and P-022 (No Deception) — a risk register entry that materially misdescribes how its own named mechanism behaves misinforms the user who relies on it for the P-020 ratification decision.

**Location:** `decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:707` (Risks table, row RSK-1).

**Evidence (exact quote, line 707):**
> "2-of-3 majority + DEFAULT-REFUTED biases toward *keeping* claims; factual lens is evidence-anchored (file+line); anti-leniency mandate inherited from `adv-scorer.md:68-91`; convergence discriminator re-surfaces a genuinely recurring defect in a later round."

**Contradicting evidence — the ADR's own three other definitions of DEFAULT-REFUTED:**
- Line 74 (L0 Executive Summary): "a claim only counts if two of the three agree (**default is: does not count**)."
- Line 381 (Decision table, D-1): "2-of-3 majority, **DEFAULT-REFUTED**, blind to each other."
- Line 590 (L1 Technical Implementation): "Default rule: **REFUTED on uncertainty (the anti-inflation default)**."

**Impact:** RSK-1 is specifically the risk that **a real Critical is wrongly refuted and slips the gate** — a false negative. By the ADR's own consistent definition everywhere else, DEFAULT-REFUTED biases *toward discarding* claims under uncertainty (it is explicitly named "the anti-inflation default"). That is the *opposite* of "biases toward keeping claims." As written, the stated mitigation for the single most dangerous failure mode in the entire proposal — the exact failure mode the fabricated PR-template incident (iterations 6–9) demonstrated under the old protocol — is not merely weak, it is describing the mechanism backwards. A reader evaluating whether RSK-1 is adequately mitigated is given a false sense of protection: the true mechanism (DEFAULT-REFUTED) if anything *raises*, not lowers, the probability of exactly the RSK-1 failure mode on a genuinely close call, and the mitigation list does not otherwise name a control for that direction of error (2-of-3 vs. unanimity affects both directions symmetrically; it is not itself an argument for "keeping" claims either).

**Remediation:** Rewrite the RSK-1 mitigation to either (a) honestly state that DEFAULT-REFUTED does *not* protect against this specific risk and rely instead on the other three listed controls (evidence-anchored factual lens, inherited anti-leniency mandate, convergence discriminator), or (b) if the intent was to argue that requiring only 2-of-3 (rather than unanimity) makes it *easier* to verify a real Critical, state that argument directly without invoking DEFAULT-REFUTED, which argues the opposite direction.

---

### CC-002-20260707-iter1: Verification Invocation Granularity Is Self-Contradictory and Empirically Falsified [CRITICAL]

**Principle:** P-001 (Truth/Accuracy), Methodological Rigor — the WI-1 implementation contract must be unambiguous and evidence-grounded; it is neither.

**Location:** `decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md` lines 585-589 (invocation contract), 624-626 (cost model), 362-364 (D-6 rationale), 144-150 (Context section).

**Evidence — three incompatible statements of the same quantity:**
1. Line 586-588 (L1 Technical Implementation, item 1): "Invocation contract: one call **per lens per Critical-bearing report**. Input = **the single claimed Critical** (id, severity, evidence, affected dimension) + the deliverable path + the lens name."
2. Line 624-626 (Cost model, c-004): "panels run only on Critical-bearing reports. Per round, cost ≈ **3 × (number of claimed Criticals)** at C4, 3 × (Criticals) at C3, 0 at C1–C2."
3. Line 362-364 (D-6 rationale): "the empirical panels are *separate blind files per lens* (`.../iteration-009/`: '**15 refutation-panel files**' = **3 lenses × 5 Criticals**...)."

These three statements cannot all be true simultaneously. Statement 1 says the unit of work is one call per **report**, but its own input schema restricts that call to **one Critical** ("the single claimed Critical," singular) — incoherent if a report contains more than one Critical. Statement 2 says cost scales with the **count of Criticals**, implying one call per individual finding. Statement 3 mislabels its own arithmetic: iteration-009's Context section (line 144-150 of this ADR, and the cited `iteration-009/s-014-quality-score.md:21,36-37`) states **10 Criticals were claimed** across **5 strategy reports** (S-001×2, S-002×2, S-004×2, S-011×1, S-012×3); "15 = 3 lenses × 5" is arithmetically 3 lenses × 5 **reports**, not 3 lenses × 5 **Criticals** (which would require 30 files for 10 Criticals, or 15 files for only 5 of the 10 claimed Criticals — either reading is wrong as stated).

**Independent filesystem verification performed in this review (Glob, this session):**
- `orchestration/adr-convention-20260702-001/adversary/iteration-009/verify/` contains exactly **15 files**, organized as 5 strategy-prefixed groups (`s-001`, `s-002`, `s-004 pre-mortem analysis`, `s-011`, `s-012`) × 3 lens suffixes (`-refutation-factual`, `-refutation-materiality`, `-refutation-remediation-value`). Reading `s-012-refutation-factual.md` confirms **one file adjudicates all three of that report's Criticals (012-001, 012-002, 012-003) together** — directly contradicting the "Input = the single claimed Critical" clause in statement 1.
- This confirms the empirical unit-of-work was **one call per lens per Critical-bearing report** (batching all of that report's Criticals into one verdict file), **not** one call per lens per individual Critical. The Cost Model formula in statement 2 ("3 × number of claimed Criticals") is therefore not what was actually done and does not match the cited evidence: 10 Criticals at 3-per-Critical would be 30 files; only 15 exist.

**Impact:** WI-1's acceptance criteria ("one-invocation-per-lens contract") does not resolve which of the two incompatible granularities (per-report vs. per-Critical) is intended, so the agent contract as specified is not implementable without further clarification — directly undermining the "implementable specification" fitness criterion for this ADR. The cost-proportionality argument in Force 2, c-004, and RSK-4's mitigation ("Panels run only on Critical-bearing reports... subtraction-first remediation drives Critical counts down") is built on a formula the ADR's own evidence does not support.

**Remediation:** Pick one granularity and make all three passages agree. Given the filesystem evidence, the accurate model is **one call per lens per Critical-bearing report** (batching that report's Criticals into a single verdict), which is also cheaper and matches every actual empirical instance. Rewrite the "Input" bullet to "the report's claimed Critical(s)" (plural-capable) and rewrite the Cost Model formula to "3 × (number of Critical-bearing reports)," then re-verify the "~15-18 files per C4 round" empirical claim against the corrected formula (5 reports × 3 = 15 matches iteration-009; see CC-003 for the second data point).

---

### CC-003-20260707-iter1: "18 Verification-Panel Files" for FU-Log Iteration-008 Is False [MAJOR]

**Principle:** P-001 (Truth/Accuracy) — an unverified numeric claim, ironic given the ADR's central case study is precisely about an unverified "Glob-verified" claim surviving four rounds.

**Location:** `decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:364` (D-6 rationale: "`.../fu-log .../iteration-008/`: '18 verification-panel files'") and line 625 ("Empirically ~15–18 verifier files per C4 round").

**Evidence:** Independent filesystem verification (Glob, this session, run twice with different patterns) of `orchestration/fu-log-convention-20260705-001/adversary/iteration-008/verify/` returns exactly **12 files**: 4 strategy-prefixed groups (`s-001 red team analysis`, `s-002`, `s-004 pre-mortem analysis (iteration 8, verified-criticals protocol)`, `s-012 (fmea - failure mode and effects analysis)`) × 3 lens suffixes = 12. The "18" figure is not a copy error introduced by this ADR alone — it is already present in the underlying `iteration-008/s-014-quality-score.md:36`, which itself states "18 verification-panel files under `adversary/iteration-008/verify/` (factual / materiality / remediation-value lenses × **4** Critical-bearing reports...)" — 3 × 4 = 12, not 18, an internal arithmetic error at the source that this ADR repeats without independent verification.

**Impact:** This is the exact class of error the ADR's Evidence-Chain section (lines 168-176) names as the central motivating incident for the whole proposal — a "verified"/cited claim that is false and was not independently checked. The ADR's own D-6 rationale, arguing for independence and evidence-anchoring as the load-bearing property of the new mechanism, cites a number that a one-command Glob check falsifies. This does not invalidate D-6's chosen option, but it weakens the credibility of the "~15-18 files" empirical support cited for the Cost Model (c-004) and RSK-4.

**Remediation:** Correct "18" to "12" (or re-derive after fixing CC-002's granularity model), and re-state the empirical range as "12-15 files per C4 round" (or "N reports × 3" generally) with a note that both real instances match a per-report, not per-Critical, cost model.

---

### CC-004-20260707-iter1: "Verify" Naming Collision Between Existing Group D and the New Verify Stage [MINOR]

**Principle:** Internal Consistency (clarity for implementers).

**Location:** Figure 1, lines 424-431 (`FINDERS` subgraph: `"Group D - Verify-strategies<br/>S-007 / S-011"`) vs. lines 437-446 (`VERIFY` subgraph: `"NEW: Refutation-Panel Verify stage (criticality-gated)"`).

**Evidence:** The existing, unchanged tournament already has a "Group D — Verify" step (S-007 Constitutional AI Critique, S-011 Chain-of-Verification — strategies that verify the *deliverable's content*). The ADR's new mechanism is also named "Verify stage" (refutation panels that verify *claimed findings*, not the deliverable). Both appear in the same diagram (Fig. 1) with overlapping vocabulary ("Verify-strategies" immediately followed downstream by "Verify stage").

**Impact:** A reader or implementer skimming SKILL.md/adv-selector.md after this ADR ships could conflate the two "Verify" stages — one is an unchanged finder-strategy group (Groups A-E), the other is the new post-finder adjudication stage. This is a documentation-clarity issue, not a design flaw.

**Remediation:** Rename the new stage (e.g., "Refutation Panel stage" or "Adjudication stage") to avoid colliding with the existing "Group D — Verify" label, or add a one-line disambiguation note in Figure 1's caption.

**Dimension impact:** Internal Consistency (0.20 weight) — Minor.

---

### CC-005-20260707-iter1: Citation of Retired Rule ID H-35 [MINOR]

**Principle:** Traceability.

**Location:** `decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:591`: "Constitutional triplet (P-003/P-020/P-022) + ≥3 forbidden actions per H-35."

**Evidence:** `.context/rules/quality-enforcement.md` Retired Rule IDs table: "H-35 | H-34 (sub-item b) | Constitutional compliance in agent definitions | 2026-02-21" — with the explicit governing text: "Rule IDs below were retired during EN-002 consolidation (2026-02-21). These IDs MUST NOT be reassigned." `.context/rules/agent-development-standards.md` itself still uses "H-35" as an internal sub-item label but annotates every occurrence with "(H-35 retired as sub-item b)" / "H-35 retired into compound parent H-34."

**Impact:** Low — `agent-development-standards.md` itself uses this same shorthand consistently, so the ADR's usage matches an existing (if slightly confusing) local convention rather than inventing a new error. Still, citing the bare ID without the "(H-34 sub-item b)" qualifier used elsewhere in the codebase is a small traceability gap for a document whose subject matter is tournament rigor.

**Remediation:** Change "per H-35" to "per H-34(b)" or "per H-35 (H-34 sub-item b)" to match the qualifier convention used in `agent-development-standards.md`.

---

## Remediation Plan

**P0 (Critical):**
- CC-001: Correct the RSK-1 mitigation description so it does not claim DEFAULT-REFUTED "biases toward keeping claims" when the ADR itself defines DEFAULT-REFUTED as the anti-inflation (discard-biased) default.
- CC-002: Resolve the three-way contradiction on verification-call granularity (per-report vs. per-Critical) and correct the Cost Model formula to match the ADR's own cited evidence (per-report, not per-Critical).

**P1 (Major):**
- CC-003: Correct "18 verification-panel files" to the filesystem-verified "12," and re-derive the "~15-18" empirical range.

**P2 (Minor):**
- CC-004: Rename the new "Verify stage" to avoid colliding with the existing "Group D — Verify-strategies" label.
- CC-005: Qualify "per H-35" as "per H-34(b)" per the retired-ID convention.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | No constitutional findings affect completeness of coverage. |
| Internal Consistency | 0.20 | Negative | CC-001 (Critical): RSK-1 mitigation contradicts the ADR's own repeated definition of DEFAULT-REFUTED. CC-002 (Critical): three incompatible statements of verification-call granularity. CC-004 (Minor): "Verify" naming collision. |
| Methodological Rigor | 0.20 | Negative | CC-002 (Critical): the WI-1 invocation contract is not implementable as specified; the cost-proportionality argument (c-004) rests on a formula the ADR's own cited files do not support. |
| Evidence Quality | 0.15 | Negative | CC-003 (Major): "18 verification-panel files" is filesystem-verifiably false (actual 12) — a citation-accuracy failure in a document whose thesis is independent fact-checking of exactly this kind of claim. |
| Actionability | 0.15 | Negative | CC-001/CC-002 leave the single highest-stakes risk (false-negative Critical slipping the gate) and the core new-agent contract (WI-1) without an actionable, internally consistent specification until revised. |
| Traceability | 0.10 | Negative | CC-005 (Minor): citation of a retired rule ID without the compound-parent qualifier used elsewhere in the codebase. |

**Constitutional Compliance Score:** `1.00 - (2 × 0.10 + 1 × 0.05 + 2 × 0.02) = 1.00 - 0.29 = 0.71`

**Threshold Determination:** REJECTED band (< 0.85) per S-007 Step 5 thresholds. This score reflects the *constitutional/evidentiary* sub-assessment only; it is not the tournament's overall S-014 composite (produced separately by adv-scorer, which weighs this report as one input among several strategy findings).

**Recommendation:** REVISE. The two Critical findings (CC-001, CC-002) are narrow, text-only, no-new-machinery fixes fully consistent with the ADR's own subtraction-first doctrine (D-3) — they do not require re-opening the six D-1..D-6 decisions themselves, only correcting a risk-mitigation description and reconciling the verification-cost model with the ADR's own cited filesystem evidence.
