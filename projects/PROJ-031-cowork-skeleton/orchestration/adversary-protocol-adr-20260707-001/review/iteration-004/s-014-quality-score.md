# Quality Score Report: ADR-adversary-tournament-protocol-001 (Verified-Criticals Tournament Methodology) — Iteration 4

## Navigation

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Plain-language verdict and top action item |
| [Scoring Context](#scoring-context) | Deliverable, criticality, protocol, inputs read |
| [VERIFIED-CRITICALS Panel Reconciliation](#verified-criticals-panel-reconciliation) | Panel outcome, per-lens tallies |
| [Score Summary](#score-summary) | Dual-protocol composite, threshold, verdict |
| [Dimension Scores](#dimension-scores) | Weighted 6-dimension table |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Evidence, gaps, improvement path per dimension |
| [Delta-Reconciliation](#delta-reconciliation) | Explicit comparison against iteration-3 (0.72) |
| [Disclosed Residuals (Advisory)](#disclosed-residuals-advisory) | Unrefuted/out-of-scope Majors/Minors — advisory, not gating |
| [Improvement Recommendations](#improvement-recommendations-priority-ordered) | Priority-ordered, mapped to VERIFIED Criticals |
| [Leniency Bias Check](#leniency-bias-check) | H-15 self-review |
| [Session Context Handoff](#session-context-handoff) | Structured summary for orchestrator |

---

## L0 Executive Summary

**Composite (VERIFIED protocol):** 0.75/1.00 | **Composite (old protocol):** 0.73/1.00 | **Verdict:** REVISE
**Verified Criticals:** 1 of 2 claimed Criticals (50%) | **Weakest Dimension:** Internal Consistency (0.64)

**One-line assessment:** All 3 of iteration-3's VERIFIED Criticals (C1–C2 gate-unreachability, WI-8 generalization-gate scope mismatch, the omitted-iteration-007 evidence gap) show zero recurrence — genuine convergence — but a fresh, panel-confirmed (3-of-3 unanimous) Critical surfaced on independent blind rotation: RSK-1's own risk-register mitigation #3 claims the convergence discriminator (D-4) "re-surfaces a wrongly-refuted defect in a later round," yet the ADR's own Figure 3 — redrawn in iteration 2 for a related reason — confines that recurrence check to the pre-verified/old-protocol branch only, leaving no path back to a REFUTED claim once the verified protocol is running (DA-001-iter4). A second claimed Critical (CC-001-iter4, alleging the MEDIUM-tier thesis is contradicted by "REQUIRED" vocabulary in the proposed `adv-scorer.md` edit) was unanimously REFUTED 0-of-3 as a misapplication of the Tier Vocabulary SSOT's actual scope (it governs the HARD Rule Index registry, not every imperative word in agent-behavioral prose). Seven unrefuted advisory Majors — several converging independently across Steelman, Devil's Advocate, and Chain-of-Verification on the same risk-register paragraph (RSK-1/RSK-2) and on evidentiary precision (the unsourced "~250 agent runs" aggregate; the overstated "reaffirmed across iterations 6, 7, 8, and 9" claim; the cost-model formula's dropped terms) — keep Internal Consistency and Evidence Quality the two dimensions most in need of a further pass.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md` (v0.4, iteration-3 remediation applied, 1,055 lines)
- **Deliverable Type:** ADR (Nygard format, L0/L1/L2), status PROPOSED
- **Criticality Level:** C3 (per invoking task; ADR self-declares auto-C3-minimum at its own c-007)
- **Scoring Strategy:** S-014 (LLM-as-Judge), VERIFIED-CRITICALS protocol, iteration 4
- **SSOT Reference:** `.context/rules/quality-enforcement.md` (Quality Gate, 6-dimension weighted composite)
- **Quality Threshold:** >= 0.92 (H-13)
- **Inputs read:**
  - `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md` (deliverable, full text, 1,055 lines)
  - `.../review/iteration-004/s-002-findings.md` (S-002 Devil's Advocate: 1 Critical, 3 Major, 1 Minor)
  - `.../review/iteration-004/s-003-findings.md` (S-003 Steelman: 0 Critical, 2 Major, 2 Minor — improvement suggestions, not defects)
  - `.../review/iteration-004/s-007-findings.md` (S-007 Constitutional AI Critique: 1 Critical, 1 Major, 2 Minor)
  - `.../review/iteration-004/s-011-findings.md` (S-011 Chain-of-Verification: 0 Critical, 1 Major, 1 Minor)
  - `.../review/iteration-004/verify/s-002 devil's advocate-{factual,materiality,remediation-value}.md` (3 refutation-panel files, S-002's 1 Critical)
  - `.../review/iteration-004/verify/s-007-{factual,materiality,remediation-value}.md` (3 refutation-panel files, S-007's 1 Critical)
  - `.../review/iteration-003/s-014-quality-score.md` (prior score, 0.72, for delta-reconciliation)
- **Prior score:** 0.72 (iteration 3) — see [Delta-Reconciliation](#delta-reconciliation)

---

## VERIFIED-CRITICALS Panel Reconciliation

Per the ADR's own D-1/D-2 decision (applied to its own review, per the Meta-Note's dogfooding), every claimed Critical this round was adjudicated by a 3-lens blind refutation panel (factual-accuracy / materiality / remediation-value), 2-of-3 majority, DEFAULT-REFUTED. S-003 (Steelman) and S-011 (Chain-of-Verification) raised zero Criticals this round, so neither report required a panel.

### Per-lens tally

| Finding ID | Source Strategy | Factual | Materiality | Remediation-Value | Majority | **Panel Verdict** |
|---|---|---|---|---|---|---|
| DA-001-iter4 | S-002 | VERIFIED | VERIFIED | VERIFIED | 3-of-3 | **VERIFIED** |
| CC-001-iter4 | S-007 | REFUTED | REFUTED | REFUTED | 0-of-3 | **REFUTED** |

**Result: 1 of 2 claimed Criticals VERIFIED (50%). 1 REFUTED-to-zero-weight (unanimous). 0 unpanelled.** DA-001-iter4 (S-002) was independently confirmed by all three lenses: the factual lens confirmed the cited line ranges resolve exactly as the finder described; the materiality lens held the contradiction is load-bearing for the ADR's own honest-risk-bounding differentiator, not a style nitpick; the remediation-value lens confirmed the fix is a low-cost documentation reconciliation (not machinery-adding) with real decision-quality value. CC-001-iter4 (S-007) was unanimously REFUTED: all three lenses independently concluded the finding conflates the Tier Vocabulary SSOT's actual scope (registration in the enumerated HARD Rule Index, capped at 25) with a blanket prohibition on imperative vocabulary anywhere in agent-behavioral prose — a scope the cited SSOT text does not support, and a reading the ADR's own diff-based WI-7 acceptance criterion ("zero change to HARD rules... verified by diff" against the HARD Rule Index table) already anticipates. Majors/Minors this round (DA-002-iter4, DA-003-iter4, DA-004-iter4, DA-005-iter4, CC-002-iter4, CC-003-iter4, CC-004-iter4, CV-001-20260707iter4, CV-002-20260707iter4, and the 4 Steelman SM-NNN-iter4 improvement suggestions) remain outside the Critical-only panel gate — see [Disclosed Residuals](#disclosed-residuals-advisory).

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite (VERIFIED protocol)** | **0.75** |
| **Weighted Composite (old protocol — every claimed Critical gates, no verification discount)** | **0.73** |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | **REVISE** (score-band REVISE at 0.70–0.84, *and* automatic-REVISE per 1 VERIFIED Critical — both triggers agree) |
| **Strategy Findings Incorporated** | Yes — 4 finder reports (S-002, S-003, S-007, S-011) + 6 refutation-panel files |
| **Verified Criticals** | 1 of 2 claimed (50%) |

**Why the two protocols differ only modestly this round:** unlike rounds where a majority of claimed Criticals were discarded (e.g., 5-of-10 or 6-of-7 elsewhere in the tournament record), this round discards exactly one claimed Critical (CC-001-iter4) out of two. CC-001-iter4's own underlying observation (mixed HARD/MEDIUM vocabulary in one proposed edit) was not frivolous — it was refuted only after all three lenses traced the Tier Vocabulary table's actual registration scope — so counting it at face value under the old protocol still meaningfully depresses Internal Consistency (the same dimension DA-001-iter4 already weakens), producing a small (~0.02) but real dual-protocol delta, smaller than the ~0.18–0.21 deltas observed in rounds with larger REFUTED fractions.

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-------------------|
| Completeness | 0.20 | 0.86 | 0.172 | Structure remains comprehensive (18-section nav, L0/L1/L2, 4 diagrams, 8-item backlog); all 3 of iteration-3's Completeness-relevant gaps (Alignment table now enumerates all 8 items) are closed. Only DA-005-iter4 (unrefuted Minor) touches this dimension. |
| Internal Consistency | 0.20 | 0.64 | 0.128 | Weakest dimension, again. DA-001-iter4 (VERIFIED, primary) is a genuine contradiction between RSK-1's own claimed safety net and Figure 3's corrected scope. Compounded by 2 unrefuted Majors on the identical risk-register pairing: SM-003-20260707iter4 (blindness-ordering clause overclaims structural-guarantee status for a procedural fallback branch) and DA-002-iter4 (RSK-1's "independent lenses" claim in tension with RSK-2's own correlated-error admission two lines later). |
| Methodological Rigor | 0.20 | 0.73 | 0.146 | DA-001-iter4 (VERIFIED, secondary — "the risk register's own citation of D-4 as a mitigation for RSK-1 is not methodologically supported by D-4's actual scope"). 2 unrefuted Majors: SM-003-iter4 (dispatch-ordering guarantee claimed for both a structural and a procedural branch, undifferentiated) and DA-004-iter4 (WI-8's single-sample, reactive validation design lacks a pre-registered falsification criterion beyond "≥1 refuted / ≥1 verified"). |
| Evidence Quality | 0.15 | 0.70 | 0.105 | No VERIFIED Critical lands here, but 3 unrefuted Majors converge independently across three different strategies: SM-001-iter4 (Steelman — the headline "~250 agent runs" aggregate has no visible derivation trail); DA-003-iter4 (Devil's Advocate — the token-cost formula's worked example prices only the "deliverable size" term, silently zeroing "cited-evidence size" and "rubric"); CV-001-20260707iter4 (CoVe — the "reaffirmed across iterations 6, 7, 8, and 9" claim overstates independent re-verification, which the ADR's own cited source, `post-ceiling-fix-notes.md:57`, states more precisely as 6-and-7-only). |
| Actionability | 0.15 | 0.80 | 0.120 | No VERIFIED Critical or direct unrefuted Major lands here; only secondary touches (DA-003-iter4: downstream cost-consumers inherit an understated figure; DA-004-iter4: WI-8's AC bar is clearable by chance on a single artifact). The 8-item backlog otherwise remains sized, dependency-mapped, and actionable. |
| Traceability | 0.10 | 0.77 | 0.077 | CC-002-iter4 (unrefuted Major — `adv-verifier`'s declared "T2" tool tier does not match the canonical T1+Write+Edit+Bash definition in `agent-development-standards.md`) is the primary gap. DA-004-iter4 (secondary) and DA-005-iter4 (Minor — "C4 all / C3 Criticals-only" implies a gradient the implementation does not have) compound it modestly. Citation discipline otherwise strong (CV-002-20260707iter4's line-range imprecision is trivial and Minor). |
| **TOTAL** | **1.00** | | **0.748 -> 0.75** | |

---

## Detailed Dimension Analysis

### Completeness (0.86/1.00)

**Evidence:** All Nygard sections remain present and populated (18-section nav table, 4 mmdc-validated diagrams, 8-item Work-Item Decomposition with all 8 items now enumerated in the Alignment table's Implementation Effort cell — closing iteration-3's CC-001-iter3). No structural section was removed or left unpopulated this round.

**Gaps:** DA-005-iter4 (unrefuted Minor): "C4 all Criticals; C3 Criticals only" (D-1 decision row) reads as if the two tiers panel Criticals at different rates, when L1 item 4 clarifies both tiers panel every claimed Critical in scope — a labeling-completeness gap, not a substantive one.

**Improvement Path:** Reword the D-1 decision-row phrasing to state explicitly that C3 and C4 panel identically on Criticals (the real binary is C1–C2 no-panel vs. C3/C4 panel), consistent with L1 item 4's own wording.

---

### Internal Consistency (0.64/1.00)

**Evidence:** One VERIFIED Critical and two unrefuted Majors, all three converging on the same risk-register paragraph (RSK-1/RSK-2):

1. **DA-001-iter4** (VERIFIED 3-of-3) — RSK-1 mitigation #3 ("the convergence discriminator (D-4) re-surfaces a genuinely recurring defect in a later round if it is wrongly refuted once," deliverable line ~903) is contradicted by Figure 3's own mermaid source and caption (lines 616–641): the recurrence check (`Q2`) lives only in the `PROTO -- "No (old protocol, no panels yet)"` branch; once the verified protocol is running, the only downstream paths from `Q1` are `FIX` or `PASS`/`BAND` — no path re-examines a REFUTED verdict. Refutation (and therefore any false-negative) can only exist under the verified protocol, which is exactly the regime the cited diagram shows has no recurrence path. All three panel lenses independently confirmed this is a genuine, load-bearing textual contradiction, not a misread.
2. **SM-003-20260707iter4** (unrefuted Major, Steelman) — the L1 "Blindness ordering" clause (lines 716–721) claims "a dispatch-ordering guarantee, not merely a prompt instruction" for *both* a true-parallelism branch and a fallback "documented ordering barrier" branch, even though the ADR's own later vocabulary (L2 Architectural Implications: "Independence as architecture, not discipline... structural... rather than behavioral") treats the ordering-barrier branch as exactly the behavioral kind of control the ADR elsewhere argues is weaker.
3. **DA-002-iter4** (unrefuted Major, Devil's Advocate) — RSK-1 mitigation #1 ("two of three **independent** lenses must both fail") is in unacknowledged tension with RSK-2's own admission two rows later that "context isolation delivers context independence, not reasoning independence... a systematic model bias can produce correlated errors."

**Gaps:** All three findings concentrate on the risk register's presentation of RSK-1 (the register's own highest-consequence entry), and two of the three (DA-001, DA-002) touch the identical two-row RSK-1/RSK-2 pairing without cross-referencing each other. This is a narrower defect footprint than iteration 3 (3 VERIFIED Criticals spread across the C1–C2 gate, the WI-8 dependency graph, and the evidence chain) but is concentrated in the section a ratifying user is most likely to rely on for honest risk-bounding.

**Improvement Path:** (a) Narrow RSK-1 mitigation #3 to state it applies only during the pre-verified-protocol transition window, or add a genuine cross-round recurrence check for REFUTED Criticals and reflect it in Figure 3 (resolves DA-001-iter4). (b) Scope the blindness-ordering clause's "structural guarantee" language to the true-parallelism branch only; name the ordering-barrier branch as procedural (resolves SM-003-iter4). (c) Add a forward cross-reference from RSK-1 mitigation #1 to RSK-2's correlated-error caveat (resolves DA-002-iter4).

---

### Methodological Rigor (0.73/1.00)

**Evidence:** DA-001-iter4 (VERIFIED, secondary) — the risk register cites D-4 as an operative mitigation for RSK-1 without that citation being methodologically supported by D-4's actual (pre-verified-mode-only) scope. Two unrefuted Majors: SM-003-20260707iter4 (the dispatch-ordering guarantee is claimed uniformly for a structural and a procedural mechanism); DA-004-iter4 — WI-8's validation design commits to "≥1 claimed Critical correctly refuted and ≥1 correctly verified" as its acceptance bar, which a lenient or a strict panel could both clear by chance on a single artifact, and RSK-7's own "genuine safeguard" framing does not fully square with its own adjacent admission that the escape-hatch "caps the cost of a transfer failure, not its likelihood."

**Gaps:** The six-decision Nygard analysis (steelman-first per H-16) and the tournament's own dogfooding structure remain independently sound; the gaps found are specification-level (how mitigations are diagrammed, how a validation pass is bounded), not method failures.

**Improvement Path:** Apply the DA-001-iter4/SM-003-iter4 corrections above. Either commit WI-8 to more than one non-ADR-genre deliverable, or soften "genuine safeguard" language to explicitly state it bounds the *cost* of a transfer failure, not its *likelihood*, consistent with RSK-7's own probability-rating caveat (resolves DA-004-iter4).

---

### Evidence Quality (0.70/1.00)

**Evidence:** No VERIFIED Critical lands here this round, but three independent strategies converge on evidentiary-precision gaps: **SM-001-20260707iter4** (Steelman, Major) — the L0/footer "~250 agent runs" aggregate is the one headline quantitative claim in an otherwise exceptionally well-cited document that carries no visible derivation trail (independent reconstruction during the Steelman pass landed in the 230–270 range, confirming plausibility but not traceability). **DA-003-iter4** (Devil's Advocate, Major) — the cost-model's worked example ("3 × ~32k" ≈ 90–105k tokens/report) prices only the deliverable-size term of its own declared three-term formula (deliverable + cited-evidence + rubric), silently zeroing the cited-evidence term for a document that itself cites 18 evidence files. **CV-001-20260707iter4** (CoVe, Major) — the "reaffirmed across iterations 6, 7, 8, and 9" claim (and its echoes in Positive Consequence #2 and RSK-2) overstates independent re-verification; direct search of the iteration-008 and iteration-009 report sets found no fresh Glob/filesystem check of the PR-template claim in either round, and the ADR's own cited source (`post-ceiling-fix-notes.md:57`) already states the more precise "reaffirmed at iter-6, iter-7... carried unchallenged through iter-8/9" distinction.

**Gaps:** All three are precision/traceability gaps in a document whose own thesis is "verify before you count" — none fabricates evidence, and CV-001-20260707iter4's own verification log independently confirmed 20 of 22 checked claims accurate, including several deliberately-precise figures (the disclosed "12" vs. "18" panel-file correction, the full 0.66→0.68→0.72→0.83→0.86→0.88 score chain). The residual gap is that the one headline aggregate and one flagship narrative claim are less rigorously sourced than the rest of the document's citation discipline.

**Improvement Path:** Add a one-line order-of-magnitude accounting for the "~250 agent runs" figure (resolves SM-001-iter4). Supply a separate estimate for the cited-evidence cost term, or explicitly disclose the ~90–105k figure as a lower bound (resolves DA-003-iter4). Correct "reaffirmed across iterations 6, 7, 8, and 9" to distinguish the 2–3 genuine independent reaffirmations (iter-6, iter-7) from the 2 rounds where the claim simply went unchecked (resolves CV-001-20260707iter4).

---

### Actionability (0.80/1.00)

**Evidence:** No VERIFIED Critical or primary unrefuted Major lands on this dimension. Secondary touches only: DA-003-iter4 (the Alignment table's "Implementation Effort" and RSK-4's cost-blowup assessment inherit a possibly-understated cost figure) and DA-004-iter4 (WI-8's AC bar is satisfiable by chance on a single artifact, a planning-clarity gap rather than a missing action).

**Gaps:** The 8-item backlog (WI-1 through WI-8), draft GitHub Issues A–G, and dependency graph remain sized, dependency-mapped, and directly implementable; no new actionability regression was found this round.

**Improvement Path:** Resolving DA-003-iter4 and DA-004-iter4 (per Evidence Quality and Methodological Rigor above) removes both secondary touches without requiring any new backlog item.

---

### Traceability (0.77/1.00)

**Evidence:** CC-002-iter4 (unrefuted Major) — `adv-verifier`'s declared "T2" tool tier (`Read, Glob, Grep, Write`) does not match the canonical T2 definition ("T1 + Write, Edit, Bash") in `agent-development-standards.md`'s Tool Security Tiers table; the ADR's own CC-001-iter2 rationale note already acknowledges this is a bespoke "T1 + Write, minus Edit/Bash" tier the canonical table does not define, labeled T2 anyway, with no corresponding amendment to the tier table proposed. DA-004-iter4 (secondary) and DA-005-iter4 (Minor) compound it modestly.

**Gaps:** Citation discipline is otherwise strong — CV-002-20260707iter4 (Minor) found only a trivial line-range imprecision (`adv-scorer.md:166-167` vs. the exact quote at `:166` alone), and CoVe's clean-verification log independently confirmed 20 of 22 spot-checked claims resolve exactly to their cited file+line sources.

**Improvement Path:** Either relabel `adv-verifier`'s tier honestly as a documented restriction ("T1 + Write, write-of-new-files only; no Edit/Bash"), or propose a scoped amendment to `agent-development-standards.md`'s Tool Security Tiers table introducing a named restricted sub-tier (resolves CC-002-iter4). Narrow the `adv-scorer.md:166-167` citation to `:166` (resolves CV-002-20260707iter4, Minor).

---

## Delta-Reconciliation

Per D-5 (mandatory delta-reconciliation against the prior iteration), iteration 3 scored **0.72** with 3 of 3 claimed Criticals VERIFIED. This iteration scores **0.75** with 1 of 2 claimed Criticals VERIFIED. The +0.03 net delta is the arithmetic result of two independent, opposite-signed movements:

- **Genuine convergence (positive, dominant this round):** All 3 of iteration-3's VERIFIED Criticals show **zero recurrence** this round under independent blind re-derivation by different strategies than found them originally. The v0.4 changelog documents, and this round's independent evidence confirms, substantive remediation: the C1–C2 auto-REVISE-fallback gap (DA-001-i3) is closed via the explicit D-2 scoping and WI-3 AC language; the WI-8/RSK-7 generalization-gate scope mismatch (DA-002-i3) is closed via the honestly-rescoped RSK-7 mitigation text; the omitted-iteration-007 evidence gap (CV-001-20260707iter3) is closed via the added Context paragraph and the corrected "0.72–0.88, non-monotonic" L0 range. This is a clean instance of the D-4 "recurrence vs. fresh stream" discriminator correctly identifying durable fixes.
- **Fresh stream (negative, partially offsetting):** One new Critical-severity defect surfaced this round (DA-001-iter4, VERIFIED 3-of-3), discovered in territory the iteration-3 remediation did not touch (the RSK-1 mitigation-#3 vs. Figure-3-scope contradiction). A second claimed Critical (CC-001-iter4) was raised but unanimously REFUTED — a correct discard, not evidence of manufactured churn, since the panels traced the underlying scope question carefully rather than defaulting to acceptance. Seven unrefuted advisory Majors also surfaced (more than iteration 3's residual count), several clustering on the same RSK-1/RSK-2 pairing DA-001-iter4 targets — a signal that the risk register's honest-bounding narrative, specifically, still needs a further pass even though the rest of the document (Completeness, Actionability) continues to improve.

Per the ADR's own D-4 convergence discriminator: this round's pattern (0 of 3 prior VERIFIED Criticals recurring, 1 fresh genuine Critical surfacing and unanimously confirmed, 1 fresh claimed Critical correctly discarded, 100% panel completion) falls on the "recurring defects get fixed, new genuine defects keep appearing" side, not the "non-convergent manufactured stream" side (which would show a roughly constant volume of claims regardless of remediation quality, and would include claims the panel fails to discriminate). The correct interpretation is that the document continues to converge incrementally, but has not yet reached a round with zero VERIFIED Criticals, which is the condition (alongside composite >= 0.92) for PASS.

---

## Disclosed Residuals (Advisory)

The following are unrefuted or out-of-panel-scope Major/Minor findings and Steelman improvement suggestions. Per D-2, these are **advisory inputs to scoring, not gating findings** (panels adjudicate Critical-severity claims only):

| ID | Source | Severity | Summary | Advisory dimension |
|---|---|---|---|---|
| DA-002-iter4 | S-002 | Major | RSK-1 mitigation #1 ("independent lenses") is in unacknowledged tension with RSK-2's own correlated-error admission two rows later | Internal Consistency / Evidence Quality |
| DA-003-iter4 | S-002 | Major | Token-cost formula's worked example prices only "deliverable size," silently zeroing "cited-evidence size" and "rubric" | Evidence Quality / Actionability |
| DA-004-iter4 | S-002 | Major | WI-8's single-sample, reactive validation design lacks a pre-registered falsification criterion beyond "≥1 refuted / ≥1 verified" | Methodological Rigor / Traceability |
| DA-005-iter4 | S-002 | Minor | "C4 all Criticals; C3 Criticals only" implies a panelling-rate gradient the described implementation does not have | Traceability / Completeness |
| CC-002-iter4 | S-007 | Major | `adv-verifier`'s declared "T2" tool tier does not match the canonical T2 definition (T1 + Write, Edit, Bash) | Traceability |
| CC-003-iter4 | S-007 | Minor | Compound cognitive-mode value ("forensic/convergent") not resolvable against the single-enum schema | Actionability |
| CC-004-iter4 | S-007 | Minor | `adv-scorer.md:166-167` citation broader than the 1-line quote; D-6 rationale's "~9–10 reports at C4" vs. the enumerated 9 finder strategies | Evidence Quality |
| CV-001-20260707iter4 | S-011 | Major | "Reaffirmed across iterations 6, 7, 8, and 9" overstates independent re-verification (only 6 and 7 show fresh checks) | Evidence Quality |
| CV-002-20260707iter4 | S-011 | Minor | `adv-scorer.md:166-167` line-range citation broader than the 1-line quote | Traceability |
| SM-001-20260707iter4 | S-003 (Steelman) | Major (improvement, not defect) | "~250 agent runs" aggregate lacks a visible derivation trail | Evidence Quality |
| SM-002-20260707iter4 | S-003 (Steelman) | Minor (improvement, not defect) | Self-referential "~950-line ADR" cost estimate has drifted from the document's current (~1,055-line) length | Evidence Quality / Traceability |
| SM-003-20260707iter4 | S-003 (Steelman) | Major (improvement, not defect) | Blindness-ordering clause claims structural-guarantee status for both a parallel-dispatch and a procedural branch | Methodological Rigor / Internal Consistency |
| SM-004-20260707iter4 | S-003 (Steelman) | Minor (improvement, not defect) | WI-8 sized "M" against a three-orthogonal-axis acceptance criterion | Actionability |

**Refuted this round (explicitly reviewed, zero weight):** CC-001-iter4 (Critical, S-007) — unanimous 0-of-3 REFUTED. All three lenses independently concluded the finding conflates the Tier Vocabulary SSOT's HARD Rule Index registration scope with a blanket lexical prohibition, a reading the cited SSOT text does not support, and both of the finding's own proposed remediations (downgrade to SHOULD, or route through the Exception Mechanism) were assessed by the remediation-value lens as net-negative or disproportionate relative to a one-line clarifying-sentence alternative the finding itself did not offer.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Underlying Defect (VERIFIED Criticals) | Current Impact | Target | Recommendation |
|----------|------|---------|--------|----------------|
| 1 | Internal Consistency / Methodological Rigor (0.64/0.73) — RSK-1 mitigation #3 does not exist once the verified protocol is running (DA-001-iter4, VERIFIED 3-of-3) | The ADR's central "residual risk is honestly bounded" claim is weaker than presented: one of RSK-1's four named counterweights is scoped out of the only regime (verified-protocol operation) in which the risk it purports to mitigate can occur | 0.85+ | Either narrow RSK-1 mitigation #3 to state it applies only during the pre-verified-protocol transition window and honestly re-price the residual risk, or add a genuine cross-round recurrence check for REFUTED Criticals under the verified protocol and reflect it in Figure 3 (source + caption). |
| 2 (advisory) | Internal Consistency (0.64) — RSK-1 "independent lenses" claim vs. RSK-2's correlated-error admission (DA-002-iter4) | A reader relying on RSK-1 alone walks away with stronger confidence in the 2-of-3 rule's protective value than RSK-2 (two rows later) supports | 0.85+ | Add a forward cross-reference from RSK-1 mitigation #1 to RSK-2's correlated-error caveat. |
| 3 (advisory) | Internal Consistency / Methodological Rigor (0.64/0.73) — blindness-ordering clause overclaims structural-guarantee status for a procedural fallback (SM-003-iter4) | WI-1's acceptance criteria and WI-6's runner guide risk operationalizing an undifferentiated dispatch requirement | 0.90+ | Scope the "structural guarantee" language to the true-parallelism branch only; name the ordering-barrier branch as procedural, consistent with the ADR's own L2 "architecture, not discipline" doctrine. |
| 4 (advisory) | Evidence Quality (0.70) — "reaffirmed across iterations 6, 7, 8, and 9" overstates independent re-verification (CV-001-20260707iter4) | Overstates the evidentiary support for RSK-2's correlated-error framing and the general severity framing of the fabricated-claim incident | 0.90+ | Correct to distinguish the 2–3 genuine independent reaffirmations (iter-6, iter-7) from the 2 rounds (8, 9) where the claim went unchecked, per the ADR's own cited `post-ceiling-fix-notes.md:57`. |
| 5 (advisory) | Evidence Quality (0.70) — "~250 agent runs" aggregate lacks a derivation trail (SM-001-iter4); cost formula drops 2 of 3 declared terms (DA-003-iter4) | The one headline aggregate and one worked cost example are less rigorously sourced than the rest of the document's citation discipline | 0.90+ | Add a one-line order-of-magnitude accounting for "~250 agent runs"; supply a separate cited-evidence cost estimate or explicitly disclose the ~90–105k figure as a lower bound. |
| 6 (advisory) | Traceability (0.77) — `adv-verifier`'s "T2" label does not match the canonical tier definition (CC-002-iter4) | A future H-34 compliance audit would find the agent missing 2 of T2's 3 tools while still labeled T2, with no corresponding tier-table amendment proposed | 0.90+ | Relabel honestly as a documented restriction ("T1 + Write, write-of-new-files only"), or propose a scoped amendment introducing a named restricted sub-tier. |
| 7 (advisory) | Methodological Rigor (0.73) — WI-8's single-sample validation design lacks a falsification criterion (DA-004-iter4) | The bar ("≥1 refuted / ≥1 verified") is clearable by chance on a single artifact; "genuine safeguard" language sits in tension with RSK-7's own cost-vs-likelihood caveat | 0.90+ | Commit WI-8 to more than one non-ADR-genre deliverable, or soften "genuine safeguard" language to state it bounds cost of failure, not likelihood. |
| 8 (advisory) | Completeness / Actionability / minor Traceability (0.86/0.80/0.77) — D-1 phrasing gradient (DA-005-iter4); compound cognitive-mode value (CC-003-iter4); citation-range nits (CC-004-iter4, CV-002-20260707iter4); stale cost self-reference (SM-002-iter4); WI-8 sizing (SM-004-iter4) | Minor labeling, schema-resolution, and precision gaps | 0.90+ | Reword D-1's tier-gradient phrasing; resolve `cognitive_mode` to a single enum value (`forensic`); narrow the `adv-scorer.md` citation to `:166`; re-true the "~950-line" self-reference; re-size or split WI-8. |

---

## Leniency Bias Check

- [x] Each dimension scored independently against the VERIFIED-Critical evidence and unrefuted advisory findings before computing the composite
- [x] Evidence documented for each score, with file+line citations reproduced from the underlying finder/panel reports (not re-derived from this scoring pass alone)
- [x] Uncertain scores resolved downward — Internal Consistency held at 0.64 (not higher) despite only 1 VERIFIED Critical this round (vs. 3 last round), because two additional unrefuted Majors concentrate on the identical risk-register pairing the VERIFIED Critical targets; Evidence Quality held at 0.70 given three independently-converging strategies (Steelman, Devil's Advocate, CoVe) each found a distinct precision gap
- [x] Fourth-iteration calibration considered — a +0.03 delta against a 0.72 baseline, with 100% of prior VERIFIED Criticals showing zero recurrence but a fresh unanimous Critical and a larger advisory-Major count surfacing, is treated as modest genuine convergence, not rounded up toward the ADR's own stated "target >=0.92" aspiration
- [x] No dimension scored above 0.95; highest score (Completeness, 0.86) reflects genuine structural strength with a disclosed Minor gap remaining
- [x] Automatic-REVISE rule applied independent of composite score: 1 of 2 panelled Criticals VERIFIED (unanimous 3-of-3) -> REVISE regardless of where composite fell
- [x] Old-protocol composite computed and reported per the dual-protocol transparency clause (D-2); the ~0.02 delta is explained (one Critical discarded, not several) rather than asserted

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.75
composite_old_protocol: 0.73
threshold: 0.92
weakest_dimension: internal_consistency
weakest_score: 0.64
critical_findings_count: 2
verified_criticals: 1
refuted_criticals: 1
unpanelled_criticals: 0
iteration: 4
prior_score: 0.72
delta: 0.03
improvement_recommendations:
  - "Narrow RSK-1 mitigation #3 to the pre-verified-protocol transition window, or add a genuine cross-round recurrence check for REFUTED Criticals under the verified protocol and reflect it in Figure 3 (DA-001-iter4, VERIFIED)"
  - "(advisory) Cross-reference RSK-1 mitigation #1 to RSK-2's correlated-error caveat (DA-002-iter4)"
  - "(advisory) Scope the blindness-ordering clause's structural-guarantee language to the true-parallelism branch only (SM-003-iter4)"
  - "(advisory) Correct the 'reaffirmed across iterations 6, 7, 8, and 9' claim to distinguish 2 genuine reaffirmations from 2 unchecked rounds (CV-001-20260707iter4)"
  - "(advisory) Add a derivation trail for '~250 agent runs'; reconcile the cost formula's worked example with its own 3 declared terms (SM-001-iter4 / DA-003-iter4)"
  - "(advisory) Relabel adv-verifier's tool tier honestly or propose a scoped restricted sub-tier amendment (CC-002-iter4)"
  - "(advisory) Add a falsification criterion or a second non-ADR-genre sample to WI-8's validation design (DA-004-iter4)"
  - "(advisory) Minor labeling/citation/sizing polish (DA-005-iter4, CC-003-iter4, CC-004-iter4, CV-002-20260707iter4, SM-002-iter4, SM-004-iter4)"
```

---

*Scoring performed per S-014 (LLM-as-Judge), VERIFIED-CRITICALS protocol dogfooded against its own proposing ADR, iteration 4. P-003: no subagents invoked. P-020: all writes confined to `projects/PROJ-031-cowork-skeleton/`; the deliverable itself was not edited by this scoring pass. P-022: every dimension score is tied to file+line evidence reproduced from the four blind finder reports and six refutation-panel files; inference (e.g., dimension-impact weighting, composite-delta interpretation) is labeled as such and distinguished from independently-verified panel fact. No employer-internal tokens or absolute filesystem paths appear in this report.*
